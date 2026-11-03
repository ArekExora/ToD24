#!/usr/bin/env python3
"""Concatenate every `sessions/session-NN/minutes-NN.md` into one Homebrewery
brew at `sessions/outputs/full_minutes.md`.

Each minutes file's body is included verbatim (YAML frontmatter is stripped —
it would render as raw text in Homebrewery). Files are separated by `\\page`
so each session starts on a new rendered page.

Usage:
    python3 .claude/skills/draft/build_full_minutes.py
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


MINUTES_NAME_RE = re.compile(r"^minutes-(\d+)\.md$")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def minutes_sort_key(path: Path) -> int:
    m = MINUTES_NAME_RE.match(path.name)
    return int(m.group(1)) if m else 0


def strip_frontmatter(text: str) -> str:
    """Remove the leading YAML frontmatter block delimited by `---` lines.
    Returns the file body. Leaves the text untouched if no frontmatter."""
    if not text.startswith("---"):
        return text
    # Skip past the second `---` line.
    parts = text.split("---", 2)
    if len(parts) < 3:
        return text
    return parts[2].lstrip("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--max",
        type=int,
        default=None,
        metavar="NN",
        help="Include only minutes with session number <= NN (default: all).",
    )
    args = parser.parse_args()

    root = repo_root()
    paths = sorted(
        (
            p
            for p in (root / "sessions").glob("session-*/minutes-*.md")
            if MINUTES_NAME_RE.match(p.name)
        ),
        key=minutes_sort_key,
    )
    if args.max is not None:
        paths = [p for p in paths if minutes_sort_key(p) <= args.max]
    if not paths:
        print("no minutes-*.md files found under sessions/", file=sys.stderr)
        return 1

    chunks: list[str] = [
        strip_frontmatter(p.read_text(encoding="utf-8")).rstrip() for p in paths
    ]
    out = "\n\n\\page\n\n".join(chunks) + "\n"

    out_dir = root / "sessions" / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "full_minutes.md"
    out_path.write_text(out, encoding="utf-8")

    rel = out_path.relative_to(root)
    print(f"wrote {rel} ({len(paths)} minutes, {len(out):,} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
