#!/usr/bin/env python3
"""Strip transcript citations from `sessions/session-NN/minutes-NN.md` and
flip `status: drafted` → `status: accepted`. The GM's manual-review step
rendered as a deterministic script.

Removes inline citation tags matching the taxonomy in the minutes template:
  [T:N], [T:N-M], [Td:N], [Td:N-M], [GM], [derived:...]
Cumulative forms with internal commas are supported:
  [Td:34-48, GM], [T:1248, GM], [T:117-118, Td:248-253]

Preserves everything else byte-for-byte except for:
  - the citation tags (and the single leading space that precedes them, so
    `beat text [Td:12].` becomes `beat text.` with no double space)
  - the status field (`drafted` → `accepted`)

Idempotent: running on an already-accepted / already-stripped file is a
no-op.

Usage:
    python3 .claude/skills/draft/accept_minutes.py 23
    python3 .claude/skills/draft/accept_minutes.py 23 --dry-run
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# One citation tag. Content inside the brackets:
#   - starts with T:N(-M), Td:N(-M), GM, or derived:anything-not-closing-bracket
#   - may be followed by further comma-separated tags of the same shape
# The leading space (if any) is consumed so no double space is left before
# the terminating punctuation (period, comma, question mark, etc.).
CITATION_RE = re.compile(
    r" ?\[(?:T:[0-9-]+|Td:[0-9-]+|GM|derived:[^\]]+)"
    r"(?:,\s*(?:T:[0-9-]+|Td:[0-9-]+|GM|derived:[^\]]+))*"
    r"\]"
)

STATUS_LINE_RE = re.compile(r"^status:\s*drafted\s*$", re.MULTILINE)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def strip_citations(text: str) -> str:
    return CITATION_RE.sub("", text)


def flip_status(text: str) -> str:
    return STATUS_LINE_RE.sub("status: accepted", text, count=1)


def transform(text: str) -> str:
    return flip_status(strip_citations(text))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "session",
        type=int,
        help="Session number (NN). Target: sessions/session-NN/minutes-NN.md.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the transformed file to stdout instead of writing it.",
    )
    args = parser.parse_args()

    path = (
        repo_root()
        / "sessions"
        / f"session-{args.session}"
        / f"minutes-{args.session}.md"
    )
    if not path.exists():
        print(f"error: {path} does not exist", file=sys.stderr)
        return 1

    original = path.read_text()
    transformed = transform(original)

    if args.dry_run:
        sys.stdout.write(transformed)
        return 0

    if transformed == original:
        print(f"{path}: already accepted / no citations to strip (no-op).")
        return 0

    citations_removed = len(CITATION_RE.findall(original))
    status_flipped = bool(STATUS_LINE_RE.search(original))
    path.write_text(transformed)
    print(
        f"{path}: stripped {citations_removed} citation tag(s); "
        f"status {'drafted → accepted' if status_flipped else 'unchanged'}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
