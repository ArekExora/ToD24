#!/usr/bin/env python3
"""Render a session artifact to PDF via the hosted Homebrewery and headless
Chromium. Replaces the manual *paste into Homebrewery → Get PDF → rename →
move* loop.

Inputs accepted (filename pattern determines PDF name):

    sessions/session-NN/saga-NN.md           → outputs/S<NN> - Saga.pdf
    sessions/session-NN/outputs/gm-hb-NN.md  → outputs/S<NN> - GM.pdf
    sessions/session-NN/minutes-NN.md        → outputs/S<NN> - Minutes.pdf

Minutes files have their YAML frontmatter stripped before upload; saga and
gm-hb files are uploaded verbatim.

Each run POSTs a fresh anonymous brew to Homebrewery, renders the PDF via
headless Chromium, then DELETEs the brew. No state is persisted — the brew
exists only for the few seconds needed to grab the PDF. Delete runs in a
`finally` block so even a render failure doesn't orphan the brew.

Flags:

    --wip   Write to S<NN> - <Role>_WIP.pdf. Use during drafting to verify
            one-page fit without clobbering the canonical PDF. Delete the
            WIP output once the saga/gm/minutes is accepted.

Dependencies (one-time install):

    pip install playwright requests pyyaml
    playwright install chromium

Usage:

    python3 .claude/skills/render_pdf.py sessions/session-55/outputs/gm-hb-55.md
    python3 .claude/skills/render_pdf.py sessions/session-55/saga-55.md
    python3 .claude/skills/render_pdf.py sessions/session-55/minutes-55.md
    python3 .claude/skills/render_pdf.py sessions/session-55/saga-55.md --wip
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import requests
from playwright.sync_api import sync_playwright

HOMEBREWERY_BASE = "https://homebrewery.naturalcrit.com"
CLIENT_VERSION = "3.24.2"  # must match server's packageJSON.version

# The homebrewery.naturalcrit.com editor homepage loads welcome_msg.md, whose
# leading ```css block becomes the brew's style and trims .page padding-bottom
# from the theme default (1.7cm) down to 1.1cm. That extra ~22px per column is
# load-bearing for whether tight content (e.g. a long final bullet) fits in
# column 1 or spills into column 2. An anonymous POST to /api doesn't carry
# any style, so the resulting share page renders with less column height than
# the editor's "Get PDF" would. Pass the style explicitly so our PDFs match.
DEFAULT_STYLE = ".page {\n  padding-bottom : 1.1cm;\n}\n"

# Filename → (role, PDF suffix, strip frontmatter?)
ROLE_PATTERNS = [
    (re.compile(r"^saga-(\d+)\.md$"), ("saga", "Saga", False)),
    (re.compile(r"^gm-hb-(\d+)\.md$"), ("gm", "GM", False)),
    (re.compile(r"^minutes-(\d+)\.md$"), ("minutes", "Minutes", True)),
]


@dataclass
class Target:
    session_nn: str   # zero-padded, e.g. "55"
    role: str         # "saga" | "gm" | "minutes"
    pdf_suffix: str   # "Saga" | "GM" | "Minutes"
    strip_frontmatter: bool
    src_path: Path
    pdf_path: Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def classify(src: Path, wip: bool = False) -> Target:
    for pattern, (role, suffix, strip) in ROLE_PATTERNS:
        m = pattern.match(src.name)
        if not m:
            continue
        nn = m.group(1)
        # gm-hb lives under outputs/; others at session root.
        session_dir = src.parent.parent if role == "gm" else src.parent
        suffix_name = f"{suffix}_WIP" if wip else suffix
        pdf_path = session_dir / "outputs" / f"S{nn} - {suffix_name}.pdf"
        return Target(
            session_nn=nn,
            role=role,
            pdf_suffix=suffix,
            strip_frontmatter=strip,
            src_path=src,
            pdf_path=pdf_path,
        )
    raise ValueError(
        f"filename does not match saga-NN.md, gm-hb-NN.md, or minutes-NN.md: {src.name}"
    )


def load_text(target: Target) -> str:
    text = target.src_path.read_text(encoding="utf-8")
    if not target.strip_frontmatter:
        return text
    # Strip the first `---`...`---` YAML block if present at the top of the file.
    stripped = text.lstrip("\n")
    if not stripped.startswith("---"):
        return text
    lines = stripped.splitlines(keepends=True)
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return text  # malformed frontmatter — leave as-is
    return "".join(lines[end_idx + 1:]).lstrip("\n")


def extract_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        m = re.match(r"^#\s+(.+?)\s*$", line)
        if m:
            return m.group(1)
        if line.strip() and not line.startswith("```"):
            break
    return fallback


def hb_delete(edit_id: str) -> None:
    url = f"{HOMEBREWERY_BASE}/api/remove/{edit_id}"
    r = requests.get(
        url,
        headers={"Homebrewery-Version": CLIENT_VERSION},
        timeout=20,
    )
    if r.status_code not in (200, 204, 404):
        print(f"  warn: delete returned HTTP {r.status_code} ({r.text[:160]})", file=sys.stderr)


def hb_create(title: str, text: str) -> tuple[str, str]:
    url = f"{HOMEBREWERY_BASE}/api"
    r = requests.post(
        url,
        headers={
            "Homebrewery-Version": CLIENT_VERSION,
            "Content-Type": "application/json",
        },
        json={"text": text, "title": title, "renderer": "V3", "style": DEFAULT_STYLE},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    return data["shareId"], data["editId"]


def render_pdf(share_id: str, pdf_path: Path) -> None:
    """The share page nests the brew inside a srcdoc `#BrewRenderer` iframe:
    `page.pdf()` on the parent flattens all brew pages into one Letter page,
    and replaying the iframe HTML on a fresh page blocks the PHB fonts under
    cross-origin ORB. Fix: *unwrap* the iframe content into the share page's
    top-level document — pagination works, and fonts stay same-origin."""
    share_url = f"{HOMEBREWERY_BASE}/share/{share_id}"
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.goto(share_url, wait_until="load", timeout=60_000)
            page.wait_for_selector("iframe#BrewRenderer", timeout=30_000)
            frame = next(f for f in page.frames if f.name == "BrewRenderer")
            frame.wait_for_selector(".page", timeout=30_000)
            # Mirror printCurrentBrew: force lazy images eager before capture.
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
            page.pdf(
                path=str(pdf_path),
                format="Letter",
                print_background=True,
                prefer_css_page_size=True,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            )
        finally:
            browser.close()


def process(src: Path, wip: bool = False) -> None:
    target = classify(src, wip=wip)
    if not target.src_path.exists():
        raise FileNotFoundError(target.src_path)

    body_text = load_text(target)
    title = extract_title(
        body_text, fallback=f"Session {int(target.session_nn)} — {target.pdf_suffix}"
    )

    share_id, edit_id = hb_create(title, body_text)
    print(f"  created brew shareId={share_id}")
    try:
        render_pdf(share_id, target.pdf_path)
        print(f"  wrote {target.pdf_path.relative_to(repo_root())}")
    finally:
        hb_delete(edit_id)
        print(f"  deleted brew editId={edit_id}")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    args = argv[1:]
    wip = "--wip" in args
    args = [a for a in args if a != "--wip"]
    for arg in args:
        src = Path(arg).resolve()
        print(f"→ {src.relative_to(repo_root()) if src.is_relative_to(repo_root()) else src}")
        process(src, wip=wip)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
