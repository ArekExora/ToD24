#!/usr/bin/env python3
"""Convert a /gm output (`gm-NN.md`) into a player-shareable Homebrewery brew
(`outputs/gm-hb-NN.md`).

The Secrets section is excluded by construction. Everything else is preserved
verbatim — the script only rearranges layout: numbered lists become bullets,
sections drop their `## N.` prefix, link wrappers are removed, the missions
table is reflowed, layout markers are injected, and the §2 Metadata block is
expanded into the Homebrewery title strip + party note.

The output is a *starting point*, not a finished brew — visual polish (bold on
lead-action phrases, custom spacing) is the editor's job. Re-running the
script overwrites the previous output, so iterate freely.

Usage:
    python3 .claude/skills/gm/gm_to_homebrewery.py sessions/session-NN/gm-NN.md
    python3 .claude/skills/gm/gm_to_homebrewery.py --all
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def extract_session_n(md: str) -> int:
    m = re.search(r"^#\s+Session\s+0*(\d+)", md, re.MULTILINE)
    if not m:
        raise ValueError("could not find `# Session N` in the file")
    return int(m.group(1))


def parse_sections(md: str) -> dict[str, str]:
    """Split a gm file on `## N. Section Name` headers; return name -> body."""
    out: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    for line in md.splitlines():
        m = re.match(r"^##\s+\d+\.\s+(.+?)\s*$", line)
        if m:
            if current is not None:
                out[current] = "\n".join(buf).strip()
            current = m.group(1).strip()
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        out[current] = "\n".join(buf).strip()
    return out


def parse_metadata(meta_body: str) -> dict[str, str]:
    """Pull realworld date, in-fiction date string, top-level location, and
    party present/absent from the §2 Metadata block. Location is set from the
    first item of the §2 sub-list as a fallback; the caller can override it
    with the minutes' top-level umbrella by calling `umbrella_from_minutes`."""
    info: dict[str, str] = {}
    lines = meta_body.splitlines()

    for line in lines:
        m = re.match(
            r"^\d+\.\s+\*\*Real-world date:\*\*\s+(\d{4}-\d{2}-\d{2})", line
        )
        if m:
            info["realworld_iso"] = m.group(1)
            continue
        m = re.match(r"^\d+\.\s+\*\*In-fiction date:\*\*\s+(.+)$", line)
        if m:
            info["infiction"] = m.group(1).strip()
            continue
        m = re.match(r"^\d+\.\s+\*\*Party present:\*\*\s+(.+)$", line)
        if m:
            info["party_present"] = m.group(1).strip()
            continue
        m = re.match(r"^\d+\.\s+\*\*Party absent:\*\*\s+(.+)$", line)
        if m:
            info["party_absent"] = m.group(1).strip()
            continue

    # First entry under "Locations:" — fallback for the brew header umbrella.
    in_locs = False
    for line in lines:
        if re.match(r"^\d+\.\s+\*\*Locations:\*\*", line):
            in_locs = True
            continue
        if in_locs:
            m = re.match(r"^\s+\d+\.\s+\[([^\]]+)\]", line)
            if m:
                info["location"] = m.group(1).strip()
                break
            if re.match(r"^\d+\.\s+", line):
                break

    return info


def umbrella_from_minutes(minutes_path: Path) -> str | None:
    """Return the comma-joined `locations:` list from the minutes YAML
    frontmatter (e.g. "Greenest, Raiders hideout"). The minutes list uses
    generic top-level location names (e.g. "Greenest" rather than "Greenest
    hills"), which is the right anchor for the brew's title strip.

    Returns None if the file is missing or has no `locations:` list."""
    if not minutes_path.exists():
        return None
    text = minutes_path.read_text(encoding="utf-8")
    # Frontmatter is between the first two `---` delimiters.
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    fm = parts[1]
    locs: list[str] = []
    in_locs = False
    for raw in fm.splitlines():
        if re.match(r"^\s*locations\s*:\s*$", raw):
            in_locs = True
            continue
        if in_locs:
            m = re.match(r"^\s+-\s+(.+?)\s*$", raw)
            if m:
                locs.append(m.group(1).strip())
                continue
            # First non-list-item line ends the locations block.
            if raw.strip():
                break
    return ", ".join(locs) if locs else None


def renumber_to_bullets(body: str) -> str:
    """Convert top-level `1. ...` / `2. ...` numbered items into `- ...`
    bullets. Indented sub-items are left untouched."""
    out: list[str] = []
    for line in body.splitlines():
        m = re.match(r"^(\d+)\.\s+(.*)$", line)
        if m:
            out.append(f"- {m.group(2)}")
        else:
            out.append(line)
    return "\n".join(out)


def strip_links(line: str) -> str:
    """`**[Name](path)**` -> `**Name**`; epic-moment `- [N.M](path) — text`
    -> `- text` (drop the coordinate prefix entirely)."""
    line = re.sub(r"\*\*\[([^\]]+)\]\([^)]+\)\*\*", r"**\1**", line)
    line = re.sub(r"^-\s+\[[\d.]+\]\([^)]+\)\s*[—-]\s*", "- ", line)
    return line


def transform_missions_table(table_body: str) -> str:
    """Drop the `#` column and force left-alignment on the separator row."""
    out: list[str] = []
    for line in table_body.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            out.append(line)
            continue
        cells = s.strip("|").split("|")
        cells = cells[1:]  # drop the `#` column
        if all(re.match(r"^\s*:?---:?\s*$", c) for c in cells):
            out.append("|" + "|".join(":---" for _ in cells) + "|")
        else:
            out.append("| " + " | ".join(c.strip() for c in cells) + " |")
    return "\n".join(out)


def transform(md: str, location_override: str | None = None) -> str:
    n = extract_session_n(md)
    sections = parse_sections(md)
    meta = parse_metadata(sections.get("Metadata", ""))

    required = ["realworld_iso", "infiction", "location", "party_present"]
    missing = [k for k in required if k not in meta]
    if missing:
        raise ValueError(f"§2 Metadata is missing fields: {', '.join(missing)}")
    meta.setdefault("party_absent", "none")
    if location_override:
        meta["location"] = location_override

    lines: list[str] = []

    # ── Title strip ────────────────────────────────────────────────────────
    # H2 with curly-injection on the next line applies the `wide` class to the
    # header (the inline `{{wide}}` form is parsed as an empty span and does
    # NOT propagate to the header). The wide H2 gives the floated date room
    # to push to the page's right edge.
    lines.append(
        f'## Session {n} GM {{{{float:"right" {meta["realworld_iso"]}}}}}'
    )
    lines.append("{wide}")
    lines.append("")
    lines.append(
        f'{{{{wide **{meta["location"]}** '
        f'{{{{float:"right" _{meta["infiction"]}_}}}} }}}}'
    )
    lines.append("")

    # ── Party note ─────────────────────────────────────────────────────────
    lines.append("{{note")
    lines.append(f'**Party present:** _{meta["party_present"]}_')
    lines.append("")
    lines.append(f' {{{{float:"left" **Party absent**: _{meta["party_absent"]}_ }}}}')
    lines.append("}}")
    lines.append("")

    # ── Summary (descriptive block) ────────────────────────────────────────
    summary = renumber_to_bullets(sections.get("Summary", "")).strip()
    lines.append("{{descriptive")
    lines.append("#### Summary")
    lines.append(summary)
    lines.append("")
    lines.append("}}")
    lines.extend(["", "", ""])

    # ── Events (left column) ───────────────────────────────────────────────
    events = renumber_to_bullets(sections.get("Events", "")).strip()
    lines.append("### Events")
    lines.append(events)
    lines.append("")
    lines.append("::::")
    lines.append("")
    lines.append("\\column")
    lines.append("")

    # ── Epic moments (right column, note) ──────────────────────────────────
    epic = renumber_to_bullets(sections.get("Epic moments", "")).strip()
    epic_lines = [strip_links(l) for l in epic.splitlines()]
    lines.append("{{note")
    lines.append("##### Epic moments")
    lines.extend(epic_lines)
    lines.append("}}")
    lines.append("")
    lines.append("::::")
    lines.append("::::")
    lines.append("")

    # ── NPCs ──────────────────────────────────────────────────────────────
    npcs = renumber_to_bullets(sections.get("NPCs", "")).strip()
    npc_lines = [strip_links(l) for l in npcs.splitlines()]
    lines.append("### NPCs")
    lines.extend(npc_lines)
    lines.append("")

    # ── Knowledge / Status / Loose ends ────────────────────────────────────
    for header, key in [
        ("Knowledge gained", "Knowledge gained"),
        ("Status changes", "Status changes"),
        ("Loose ends", "Loose ends"),
    ]:
        body = renumber_to_bullets(sections.get(key, "")).strip()
        lines.append(f"### {header}")
        lines.append(body)
        lines.append("")

    lines.extend(["", ""])

    # ── Missions table (wide, # column dropped, left-aligned) ──────────────
    missions = sections.get("Missions & rewards", "").strip()
    lines.append("{{wide")
    lines.append("### Missions & rewards")
    lines.append("")
    lines.append(transform_missions_table(missions))
    lines.append("}}")
    lines.append("")

    # ── Footer ────────────────────────────────────────────────────────────
    lines.append("{{pageNumber,auto}}")
    lines.append("{{footnote Tyranny of Dragons}}")

    return "\n".join(lines) + "\n"


def session_nn(md_path: Path) -> str:
    """Extract `NN` from a `gm-NN.md` filename."""
    m = re.match(r"^gm-(\d+)\.md$", md_path.name)
    if not m:
        raise ValueError(f"not a gm-NN.md file: {md_path.name}")
    return m.group(1)


def process_one(md_path: Path) -> Path:
    md = md_path.read_text(encoding="utf-8")
    nn = session_nn(md_path)
    minutes_path = md_path.parent / f"minutes-{nn}.md"
    umbrella = umbrella_from_minutes(minutes_path)
    out_dir = md_path.parent / "outputs"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"gm-hb-{nn}.md"
    out_path.write_text(transform(md, location_override=umbrella), encoding="utf-8")
    return out_path


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2

    if argv[1] == "--all":
        paths = sorted(
            p for p in (repo_root() / "sessions").glob("session-*/gm-*.md")
            if re.match(r"^gm-\d+\.md$", p.name)
        )
        if not paths:
            print("no gm-*.md files found under sessions/", file=sys.stderr)
            return 1
        for p in paths:
            out = process_one(p)
            print(f"wrote {out.relative_to(repo_root())}")
        return 0

    md_path = Path(argv[1]).resolve()
    if not md_path.exists():
        print(f"not found: {md_path}", file=sys.stderr)
        return 1
    out = process_one(md_path)
    try:
        rel = out.relative_to(repo_root())
        print(f"wrote {rel}")
    except ValueError:
        print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
