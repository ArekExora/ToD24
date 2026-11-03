#!/usr/bin/env python3
"""Concatenate every `sessions/session-NN/saga-NN.md` into one Homebrewery
brew at `sessions/outputs/full_saga.md`.

Each saga's content is included verbatim. Sagas are separated by a `\\page`
line so each session starts on a new rendered page in Homebrewery.

Usage:
    python3 .claude/skills/saga/build_full_saga.py
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SAGA_NAME_RE = re.compile(r"^saga-(\d+)\.md$")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def saga_sort_key(path: Path) -> int:
    m = SAGA_NAME_RE.match(path.name)
    return int(m.group(1)) if m else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--max",
        type=int,
        default=None,
        metavar="NN",
        help="Include only sagas with session number <= NN (default: all).",
    )
    args = parser.parse_args()

    root = repo_root()
    paths = sorted(
        (p for p in (root / "sessions").glob("session-*/saga-*.md") if SAGA_NAME_RE.match(p.name)),
        key=saga_sort_key,
    )
    if args.max is not None:
        paths = [p for p in paths if saga_sort_key(p) <= args.max]
    if not paths:
        print("no saga-*.md files found under sessions/", file=sys.stderr)
        return 1

    chunks: list[str] = []
    for p in paths:
        body = p.read_text(encoding="utf-8").rstrip()
        chunks.append(body)

    out = "\n\n\\page\n\n".join(chunks) + "\n"

    out_dir = root / "sessions" / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "full_saga.md"
    out_path.write_text(out, encoding="utf-8")

    rel = out_path.relative_to(root)
    print(f"wrote {rel} ({len(paths)} sagas, {len(out):,} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
