#!/usr/bin/env python3
"""Generate manifest.json at the repo root for the public session index.

Scans sessions/session-NN/outputs/ for per-session PDFs and sessions/outputs/
for campaign-wide compilation PDFs. Reads each session's minutes-NN.md
frontmatter for the real-world and in-fiction dates. Writes a single
manifest.json consumed by index.html.

Run after any PDF or minutes-frontmatter edit, or wire into CI.
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]          # .claude/skills/publish/ → repo root
SESSIONS_DIR = ROOT / "sessions"
CAMPAIGN_OUTPUTS = SESSIONS_DIR / "outputs"
MANIFEST = ROOT / "manifest.json"

FM_PATTERN = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
SESSION_DIR_PATTERN = re.compile(r"session-(\d+)$")


def read_frontmatter(md_path: Path) -> dict:
    if not md_path.is_file():
        return {}
    text = md_path.read_text(encoding="utf-8")
    m = FM_PATTERN.match(text)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line[0].isspace():
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    return fm


def pretty_real_date(raw: str) -> str:
    # "2025-09-28 17:50 - 20:30" → "2025-09-28"
    return raw.split()[0] if raw else ""


def pretty_fiction_date(raw: str) -> str:
    # "11 Nightal 1489 DR, ~13:30 → 13 Nightal, ~12:00" → "11 Nightal 1489 DR"
    return raw.split(",", 1)[0].strip() if raw else ""


def rel_pdf(path):
    return str(path.relative_to(ROOT)) if path.is_file() else None


def build_session(n: int) -> dict:
    sdir = SESSIONS_DIR / f"session-{n:02d}"
    fm = read_frontmatter(sdir / f"minutes-{n:02d}.md")
    outputs = sdir / "outputs"
    return {
        "n": n,
        "real_date": pretty_real_date(fm.get("date", "")),
        "in_fiction_date": pretty_fiction_date(fm.get("in_fiction_date", "")),
        "pdfs": {
            "saga": rel_pdf(outputs / f"S{n} - Saga.pdf"),
            "gm": rel_pdf(outputs / f"S{n} - GM.pdf"),
            "minutes": rel_pdf(outputs / f"S{n} - Minutes.pdf"),
        },
    }


def main() -> None:
    session_nums = sorted(
        int(m.group(1))
        for d in SESSIONS_DIR.iterdir()
        if d.is_dir() and (m := SESSION_DIR_PATTERN.match(d.name))
    )

    manifest = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "campaign": {
            "pdfs": {
                "saga": rel_pdf(CAMPAIGN_OUTPUTS / "Saga.pdf"),
                "gm": rel_pdf(CAMPAIGN_OUTPUTS / "GM.pdf"),
                "minutes": rel_pdf(CAMPAIGN_OUTPUTS / "Minutes.pdf"),
            },
        },
        "sessions": [build_session(n) for n in session_nums],
    }

    MANIFEST.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    counts = {"full": 0, "partial": 0, "empty": 0}
    for s in manifest["sessions"]:
        got = sum(1 for v in s["pdfs"].values() if v)
        counts["full" if got == 3 else "empty" if got == 0 else "partial"] += 1
    campaign_got = sum(1 for v in manifest["campaign"]["pdfs"].values() if v)

    print(
        f"manifest.json: {len(session_nums)} sessions "
        f"({counts['full']} full, {counts['partial']} partial, {counts['empty']} empty) "
        f"+ campaign ({campaign_got}/3)"
    )


if __name__ == "__main__":
    main()
