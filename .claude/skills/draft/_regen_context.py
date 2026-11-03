#!/usr/bin/env python3
"""Regenerate PC and NPC context digests under campaign/pcs/ and campaign/npcs/.

Outputs:
    campaign/pcs/_context.md   — per active PC: frontmatter + Signature + Full
                                  sheet names (class/species features, feats,
                                  spells) + Notable items names.
    campaign/npcs/_context.md  — per NPC: frontmatter only.

Loaded by `/draft` as context before reading the transcript.
Run after editing any campaign/pcs/*.md or campaign/npcs/*.md file.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent              # .claude/skills/draft/
PROJECT_ROOT = ROOT.parents[2]                       # repo root (…/ToD)
CAMPAIGN_DIR = PROJECT_ROOT / "campaign"
PCS_DIR = CAMPAIGN_DIR / "pcs"
NPCS_DIR = CAMPAIGN_DIR / "npcs"
PCS_OUT = PCS_DIR / "_context.md"
NPCS_OUT = NPCS_DIR / "_context.md"

FM_FENCE = "---\n"

# Frontmatter fields dropped from the digest. `factions` is intentionally
# retained — it gates faction-based public-generic descriptors at draft time.
DROPPED_FIELDS = {"subspecies", "subclass", "alignment", "languages", "source"}

# Trailing italic parenthetical annotating a spell's non-class source
# (e.g., `_(via Sending Stone)_`). Stripped from the digest — the drafter
# only needs the spell name to verify list membership.
SOURCE_ANNOTATION = re.compile(r"\s*_\(via [^)]*\)_")


def filter_frontmatter(fm: str) -> str:
    """Drop excluded top-level keys (and their indented continuations) from a fenced YAML block."""
    out: list[str] = []
    skip = False
    for line in fm.splitlines(keepends=True):
        if line.startswith("---"):
            out.append(line)
            skip = False
            continue
        if line and not line[0].isspace() and ":" in line:
            key = line.split(":", 1)[0].strip()
            skip = key in DROPPED_FIELDS
            if not skip:
                out.append(line)
            continue
        if not skip:
            out.append(line)
    return "".join(out)


def bump_headings(text: str, by: int = 1) -> str:
    """Add `by` hashes to every markdown heading line (so `#### X` → `##### X` for by=1)."""
    return re.sub(r"^(#+)(\s)", lambda m: ("#" * by) + m.group(1) + m.group(2), text, flags=re.MULTILINE)


def name_from_frontmatter(fm: str) -> str:
    """Extract the `name:` value from a frontmatter block."""
    m = re.search(r"^name:\s*(.+?)\s*$", fm, re.MULTILINE)
    return m.group(1).strip() if m else ""


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith(FM_FENCE):
        return "", text
    end = text.find("\n" + FM_FENCE, len(FM_FENCE))
    if end < 0:
        return "", text
    fm = text[: end + 1 + len(FM_FENCE)]
    return fm, text[len(fm):]


def section(body: str, level: int, prefix: str) -> str:
    """Return body of `<level> <prefix>...` up to next heading at same/shallower level."""
    hashes = "#" * level
    pat = rf"^{re.escape(hashes)} {re.escape(prefix)}.*?$"
    m = re.search(pat, body, re.MULTILINE)
    if not m:
        return ""
    start = m.end() + 1
    stop = re.search(rf"^#{{1,{level}}} ", body[start:], re.MULTILINE)
    end = start + stop.start() if stop else len(body)
    return body[start:end].strip("\n")


def notable_items(current_state: str) -> list[str]:
    """Extract item names from the `- **Notable items:**` bullet block."""
    items: list[str] = []
    in_block = False
    block_indent = 0
    for line in current_state.splitlines():
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if not in_block:
            if stripped.startswith("- **Notable items:**"):
                in_block = True
                block_indent = indent
                inline = stripped[len("- **Notable items:**"):].strip()
                if inline and inline.lower() not in {"none tracked yet", "none.", "none"}:
                    items.append(inline)
            continue
        if not stripped:
            continue
        # End of block: another top-level `- **Key:**` bullet at the same indent.
        if indent <= block_indent and stripped.startswith("- **"):
            break
        # Collect sub-bullets — strip the trailing ` — description` if present.
        if stripped.startswith("- "):
            content = stripped[2:].strip()
            name = re.split(r"\s+—\s+", content, maxsplit=1)[0].strip()
            items.append(name)
    return items


def pc_digest(pc: Path) -> str:
    text = pc.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    if not fm:
        print(f"  ! {pc.name}: no frontmatter, skipped", file=sys.stderr)
        return ""

    sig = section(body, 2, "Signature")
    cs = section(body, 2, "Current state")
    items = notable_items(cs) if cs else []
    fs = section(body, 2, "Full sheet")
    class_f = section(fs, 3, "Class features")
    species_f = section(fs, 3, "Species features")
    feats = section(fs, 3, "Feats")
    spells = section(fs, 3, "Spells")

    filtered_fm = filter_frontmatter(fm)
    name = name_from_frontmatter(fm) or pc.stem
    out = [f"## {name}\n", "\n", filtered_fm.rstrip() + "\n", "\n"]
    if sig:
        out += ["### Signature\n", "\n", sig + "\n", "\n"]
    if items:
        out += ["### Notable items\n", "\n"]
        for it in items:
            out += [f"- {it}\n"]
        out += ["\n"]
    if any([class_f, species_f, feats, spells]):
        out += ["### Full sheet (names only)\n", "\n"]
        for label, blob in [
            ("Class features", class_f),
            ("Species features", species_f),
            ("Feats", feats),
            ("Spells", spells),
        ]:
            if blob:
                if label == "Spells":
                    # H4 spell-level headings → H5 for strict nesting under H4 label.
                    # Strip trailing `_(via …)_` source annotations — drafter needs names only.
                    body = bump_headings(SOURCE_ANNOTATION.sub("", blob), by=1)
                else:
                    body = blob
                out += [f"#### {label}\n", "\n", body + "\n", "\n"]
    return "".join(out).rstrip() + "\n"


def npc_digest(npc: Path) -> str:
    text = npc.read_text(encoding="utf-8")
    fm, _ = split_frontmatter(text)
    if not fm:
        print(f"  ! {npc.name}: no frontmatter, skipped", file=sys.stderr)
        return ""
    filtered_fm = filter_frontmatter(fm)
    name = name_from_frontmatter(fm) or npc.stem
    return f"## {name}\n\n{filtered_fm.rstrip()}\n"


def main() -> None:
    pcs = sorted(p for p in PCS_DIR.glob("*.md") if not p.name.startswith("_"))
    npcs = sorted(p for p in NPCS_DIR.glob("*.md") if not p.name.startswith("_"))

    header = (
        "<!-- Auto-generated by campaign/_regen_context.py. Do not hand-edit. -->\n"
        "<!-- Regenerate after editing any campaign/{kind}/*.md file. -->\n\n"
    )

    pc_blocks = [header.format(kind="pcs")]
    for p in pcs:
        d = pc_digest(p)
        if d:
            pc_blocks += [d, "\n"]
    PCS_OUT.write_text("".join(pc_blocks).rstrip() + "\n", encoding="utf-8")

    npc_blocks = [header.format(kind="npcs")]
    for p in npcs:
        d = npc_digest(p)
        if d:
            npc_blocks += [d, "\n"]
    NPCS_OUT.write_text("".join(npc_blocks).rstrip() + "\n", encoding="utf-8")

    pc_in = sum(p.stat().st_size for p in pcs)
    npc_in = sum(p.stat().st_size for p in npcs)
    pc_out = PCS_OUT.stat().st_size
    npc_out = NPCS_OUT.stat().st_size
    print(f"PCs:  {len(pcs):2d} files, {pc_in:>6,} B  →  {PCS_OUT.relative_to(PROJECT_ROOT)} ({pc_out:,} B, {pc_out / pc_in:.0%})")
    print(f"NPCs: {len(npcs):2d} files, {npc_in:>6,} B  →  {NPCS_OUT.relative_to(PROJECT_ROOT)} ({npc_out:,} B, {npc_out / npc_in:.0%})")


if __name__ == "__main__":
    main()
