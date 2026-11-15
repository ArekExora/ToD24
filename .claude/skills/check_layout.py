#!/usr/bin/env python3
"""Layout check: compare source vs translation Homebrewery rendering.

Renders both files through the same Playwright + Homebrewery stack
`render_pdf.py` uses and compares per-scene geometry. The source is the
ground-truth layout — any scene in the translation that occupies more
columns, extends past the page edge, or whose title wraps to more lines
than in the source is a translation-length problem (prose too long for
the slot the source carved out).

Three failure modes:

  1. Column spill — translation's scene content reaches further right
     than source's (e.g. source scene fits in column 1, translation
     bleeds into column 2 or beyond).
  2. Page overflow — translation's scene content extends past the page's
     right or bottom edge (content clipped by `page.pdf()`).
  3. Title wrap — translation's `h2` scene title renders taller than
     source's (title wrapped onto a second line).

Exit 0 = layout matches. Exit 1 = findings printed. Exit 2 = usage error.

Usage:

    python3 .claude/skills/check_layout.py \\
        sessions/session-25/minutes-25.md \\
        sessions/session-25/resumen-25.md

The check assumes the two files share identical Homebrewery markup
structure (`\\column`, `\\page`, scene count). The `/translate` skill
enforces this by construction — the translator never touches those
directives.
"""
from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

from render_pdf import (
    HOMEBREWERY_BASE,
    extract_title,
    hb_create,
    hb_delete,
)

# Pixel tolerance for layout comparisons. Sub-pixel rendering and small
# font-metric differences between the two renders can introduce a few px
# of noise even when the layout is effectively identical; anything under
# this threshold is treated as equal.
TOLERANCE_PX = 5


def strip_frontmatter(text: str) -> str:
    """Drop a leading `---`...`---` YAML block if present (minutes-NN.md
    carries one; resumen-NN.md doesn't)."""
    stripped = text.lstrip("\n")
    if not stripped.startswith("---"):
        return text
    lines = stripped.splitlines(keepends=True)
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "".join(lines[i + 1:]).lstrip("\n")
    return text


# Inside the share page (after we unwrap the iframe content into the top-level
# document), walk each `.page` and emit per-scene geometry: for every `h2`,
# record which page it sits on, its rendered box, and the bounding box of
# every descendant up to the next `h2` (that span is the scene). We also
# record each page's own bounds so the Python side can compare without
# re-scraping.
INSPECT_JS = """
() => {
    const pages = Array.from(document.querySelectorAll('.page'));
    const pageMeta = pages.map((pg, i) => {
        const r = pg.getBoundingClientRect();
        return { idx: i, left: r.left, right: r.right, top: r.top, bottom: r.bottom };
    });
    // Collect every h2 in reading order, tagged with its page index.
    const h2s = [];
    pages.forEach((pg, pageIdx) => {
        pg.querySelectorAll('h2').forEach(h => {
            h2s.push({ el: h, pageIdx });
        });
    });
    // For each h2, the scene spans from the h2 up to (but not including)
    // the next h2 in the document. Collect the right/bottom extent of
    // every descendant in that span, scoped to the same page as the h2.
    const scenes = h2s.map((entry, i) => {
        const h = entry.el;
        const hRect = h.getBoundingClientRect();
        const nextH = i + 1 < h2s.length ? h2s[i + 1].el : null;
        // Walk all elements in document order starting after `h`, stop at
        // `nextH` or at the last element whose page differs.
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
        walker.currentNode = h;
        let maxRight = hRect.right;
        let maxBottom = hRect.bottom;
        let node = walker.nextNode();
        while (node && node !== nextH) {
            const r = node.getBoundingClientRect();
            if (r.width > 0 && r.height > 0) {
                if (r.right > maxRight) maxRight = r.right;
                if (r.bottom > maxBottom) maxBottom = r.bottom;
            }
            node = walker.nextNode();
        }
        return {
            sceneIdx: i,
            pageIdx: entry.pageIdx,
            titleText: h.textContent.trim(),
            titleHeight: Math.round(hRect.height),
            titleWidth: Math.round(hRect.width),
            titleLeft: Math.round(hRect.left),  // x of the h2 — key signal for column shift
            titleTop: Math.round(hRect.top),
            maxRight: Math.round(maxRight),
            maxBottom: Math.round(maxBottom),
        };
    });
    return { pages: pageMeta, scenes: scenes };
}
"""


def inspect_file(src: Path) -> dict:
    """Upload src to an anonymous HB brew, render in Playwright headless,
    return the inspection payload. Deletes the brew on the way out."""
    text = strip_frontmatter(src.read_text(encoding="utf-8"))
    title = extract_title(text, fallback=src.stem)
    share_id, edit_id = hb_create(title, text)
    try:
        share_url = f"{HOMEBREWERY_BASE}/share/{share_id}"
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.goto(share_url, wait_until="load", timeout=60_000)
                page.wait_for_selector("iframe#BrewRenderer", timeout=30_000)
                frame = next(f for f in page.frames if f.name == "BrewRenderer")
                frame.wait_for_selector(".page", timeout=30_000)
                frame.evaluate(
                    "document.querySelectorAll('img[loading=\"lazy\"]')"
                    ".forEach(i => i.loading = 'eager')"
                )
                page.wait_for_timeout(3000)
                page.evaluate("""
                    () => {
                        const frame = document.getElementById('BrewRenderer');
                        const src = frame.contentDocument;
                        document.head.innerHTML = src.head.innerHTML;
                        document.body.innerHTML = src.body.innerHTML;
                    }
                """)
                page.wait_for_selector(".page", timeout=30_000)
                page.evaluate("document.fonts.ready")
                page.wait_for_timeout(3000)
                page.emulate_media(media="print")
                return page.evaluate(INSPECT_JS)
            finally:
                browser.close()
    finally:
        hb_delete(edit_id)


def detect_column_width(scenes: list[dict]) -> int:
    """Infer the effective column width from the source scene geometry.

    Homebrewery pages use a two-column layout. Scenes on the same page
    either share an h2.left (same column) or differ by one column width.
    Pick the largest pairwise same-page delta — that's the column span.
    Falls back to 500px if no pair of scenes differ in the source (every
    scene in column 1).
    """
    deltas = []
    for i, a in enumerate(scenes):
        for b in scenes[i + 1:]:
            if a["pageIdx"] != b["pageIdx"]:
                continue
            delta = abs(a["titleLeft"] - b["titleLeft"])
            if delta > 50:  # meaningful difference; not sub-pixel noise
                deltas.append(delta)
    return max(deltas) if deltas else 500


def compare(source: dict, translation: dict) -> list[dict]:
    """Walk scene-by-scene, identify translation-only overflows.

    The two files share identical markup, so scene counts and page
    assignments match. The question for each scene is: does the
    translation reach further right / wrap its title / overflow the
    page bottom relative to the source?

    When a column shift is detected (translation scene N sits in a
    column further right than the source has it), the *root cause*
    isn't scene N — it's one or more earlier scenes on the same page
    that overflowed their source column and pushed scene N over.
    Report the root-cause scenes, not the downstream ones.
    """
    findings = []
    if len(source["scenes"]) != len(translation["scenes"]):
        findings.append({
            "kind": "structure-mismatch",
            "message": (
                f"scene count differs: source has {len(source['scenes'])}, "
                f"translation has {len(translation['scenes'])} — "
                "check \\column / \\page markup"
            ),
        })
        return findings

    col_width = detect_column_width(source["scenes"])
    shift_threshold = col_width // 2  # need at least a half column to count

    # Title wraps first — these are per-scene facts, no root-cause walk.
    for s, t in zip(source["scenes"], translation["scenes"]):
        if t["titleHeight"] > s["titleHeight"] + TOLERANCE_PX:
            findings.append({
                "kind": "title-wrap",
                "scene_idx": t["sceneIdx"],
                "page_idx": t["pageIdx"],
                "title": t["titleText"],
                "source_title_height": s["titleHeight"],
                "translation_title_height": t["titleHeight"],
            })

    # Detect column shifts: either the h2 itself moved to a further-right
    # column (title shift), OR the h2 stayed put but the scene's content
    # extends far past where the source's same scene ends (content shift —
    # the scene bled into the next column even if the title is in the
    # "right" place). Both signal the same failure mode: content laid out
    # one column further right than source has it, which clips at the
    # page edge or pushes subsequent scenes over.
    #
    # Only act on the FIRST shift per page — everything after it on the
    # same page is downstream of that first push.
    reported_pages: set[int] = set()
    for i, (s, t) in enumerate(zip(source["scenes"], translation["scenes"])):
        if t["pageIdx"] in reported_pages:
            continue
        shifted_right = t["titleLeft"] > s["titleLeft"] + shift_threshold
        shifted_page = t["pageIdx"] > s["pageIdx"]
        content_shifted = t["maxRight"] > s["maxRight"] + shift_threshold
        if not (shifted_right or shifted_page or content_shifted):
            continue
        reported_pages.add(t["pageIdx"])
        # Root-cause walkback. Two cases:
        #
        #   Title shift (shifted_right) — scene i's title landed one column
        #   right of source. The push came from an earlier scene in the
        #   column immediately preceding i's source column. Root causes:
        #   scenes j < i in that preceding column.
        #
        #   Content shift (content_shifted without title shift) — scene i's
        #   title is where source has it, but its own content extended past
        #   the column into the next one. Scene i itself contributed, along
        #   with any earlier scenes in the same flow column (their length
        #   left less room for scene i to fit its column).
        #
        # On flow pages (no \column), scenes sharing an h2.left share a
        # column — walking earlier scenes with matching h2.left picks up
        # the whole flow block that overflowed.
        target_col_left = s["titleLeft"] - col_width if shifted_right else None
        # Include scene i itself when the overflow is on its own content.
        search_upper_bound = (i + 1) if (content_shifted and not shifted_right
                                          and not shifted_page) else i
        root_causes = []
        for j in range(search_upper_bound):
            s_j = source["scenes"][j]
            if s_j["pageIdx"] != s["pageIdx"]:
                continue
            if shifted_page:
                # Page shift: everything on the source page before
                # scene i contributed.
                root_causes.append({
                    "scene_idx": j,
                    "title": source["scenes"][j]["titleText"],
                })
            elif target_col_left is not None and abs(s_j["titleLeft"] - target_col_left) < 50:
                # Same column as the slot that overflowed (title-shift case).
                root_causes.append({
                    "scene_idx": j,
                    "title": source["scenes"][j]["titleText"],
                })
            elif abs(s_j["titleLeft"] - s["titleLeft"]) < 50:
                # Same column as scene i (content-shift case and flow-page
                # title-shift case: scenes 3, 4 in col 1 feed scene 5 in
                # col 2 — a shift on scene 5 blames 3 AND/OR 4).
                root_causes.append({
                    "scene_idx": j,
                    "title": source["scenes"][j]["titleText"],
                })
        findings.append({
            "kind": "column-shift",
            "shifted_scene_idx": i,
            "shifted_scene": t["titleText"],
            "page_idx": t["pageIdx"],
            "shift_px": t["titleLeft"] - s["titleLeft"]
                        if shifted_right else None,
            "content_overflow_px": t["maxRight"] - s["maxRight"]
                                    if content_shifted else None,
            "page_shift": shifted_page,
            "root_causes": root_causes,
        })

    # Page-bottom overflow for the final scene on each page: if the
    # translation's last-on-page scene extends past the page bottom while
    # the source's doesn't, content is being clipped off the bottom.
    # (Column shifts usually catch this via the x-axis signal, but a
    # pure-vertical overflow on a single-column page needs its own check.)
    last_on_page: dict[int, int] = {}
    for i, t in enumerate(translation["scenes"]):
        last_on_page[t["pageIdx"]] = i
    for page_idx, scene_idx in last_on_page.items():
        if page_idx in reported_pages:
            continue  # already reported via column-shift
        t = translation["scenes"][scene_idx]
        s = source["scenes"][scene_idx]
        page = source["pages"][page_idx] if page_idx < len(source["pages"]) else None
        if page is None:
            continue
        if (
            t["maxBottom"] > page["bottom"] + TOLERANCE_PX
            and t["maxBottom"] > s["maxBottom"] + TOLERANCE_PX
        ):
            findings.append({
                "kind": "page-overflow",
                "scene_idx": scene_idx,
                "page_idx": page_idx,
                "title": t["titleText"],
                "page_bottom": round(page["bottom"]),
                "translation_max_bottom": t["maxBottom"],
                # Tighten this scene or any earlier scene on the page.
                "root_causes": [
                    {"scene_idx": i, "title": translation["scenes"][i]["titleText"]}
                    for i in range(scene_idx + 1)
                    if translation["scenes"][i]["pageIdx"] == page_idx
                ],
            })

    return findings


def report(source_path: Path, translation_path: Path, findings: list[dict]) -> int:
    if not findings:
        print(f"✓ layout OK: {translation_path.name} matches {source_path.name}")
        return 0
    print(f"✗ layout overflow in {translation_path.name} (vs {source_path.name}):")
    for f in findings:
        kind = f["kind"]
        if kind == "structure-mismatch":
            print(f"  structure: {f['message']}")
            continue
        page = f["page_idx"] + 1
        if kind == "title-wrap":
            print(
                f"  page {page} — scene {f['title']!r}: title wraps "
                f"(source {f['source_title_height']}px, "
                f"translation {f['translation_title_height']}px) → "
                "shorten the title"
            )
        elif kind == "column-shift":
            roots = ", ".join(repr(r["title"]) for r in f["root_causes"])
            if f["page_shift"]:
                reason = "pushed to a later page than source has it"
            elif f["shift_px"] is not None:
                reason = f"title shifted {f['shift_px']}px right (one column over)"
            else:
                reason = (
                    f"content overflows +{f['content_overflow_px']}px past source "
                    "(bleeds into the next column)"
                )
            action = (
                f"tighten {roots}"
                if f["root_causes"]
                else "tighten preceding content"
            )
            print(
                f"  page {page} — scene {f['shifted_scene']!r}: {reason} → {action}"
            )
        elif kind == "page-overflow":
            roots = ", ".join(repr(r["title"]) for r in f["root_causes"])
            print(
                f"  page {page} — content past page bottom "
                f"({f['translation_max_bottom']}px vs page bottom "
                f"{f['page_bottom']}px) → tighten any of: {roots}"
            )
    return 1


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    source_path = Path(argv[1]).resolve()
    translation_path = Path(argv[2]).resolve()
    for p in (source_path, translation_path):
        if not p.exists():
            print(f"not found: {p}", file=sys.stderr)
            return 2
    print(f"→ source:      {source_path.name}")
    source = inspect_file(source_path)
    print(f"→ translation: {translation_path.name}")
    translation = inspect_file(translation_path)
    findings = compare(source, translation)
    return report(source_path, translation_path, findings)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
