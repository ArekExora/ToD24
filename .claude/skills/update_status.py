#!/usr/bin/env python3
"""Regenerate sessions/status.md from the sessions/ tree.

Scans each session-NN/ directory, derives the status columns, and rewrites
the table below `## Status` in status.md. Column rules are documented in
the "How to fill the table" preamble of status.md.

Usage:
    python3 .claude/skills/update_status.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[2] / "sessions"
STATUS_FILE = ROOT / "status.md"

MONTHS = [
    "Hammer", "Alturiak", "Ches", "Tarsakh",
    "Mirtul", "Kythorn", "Flamerule", "Eleasis",
    "Eleint", "Marpenoth", "Uktar", "Nightal",
]
MONTH_ABBR = {
    "Hammer": "Hamm", "Alturiak": "Alt", "Ches": "Ches", "Tarsakh": "Tars",
    "Mirtul": "Mirt", "Kythorn": "Kyth", "Flamerule": "Flame", "Eleasis": "Elea",
    "Eleint": "Elei", "Marpenoth": "Marp", "Uktar": "Ukt", "Nightal": "Nig",
}

# Harptos calendar: twelve 30-day months with five intercalary days between.
# Build a flat day-of-year lookup so ordering is trivial.
_SCHEDULE = [
    ("month", "Hammer"), ("intercalary", "Midwinter"),
    ("month", "Alturiak"), ("month", "Ches"),
    ("month", "Tarsakh"), ("intercalary", "Greengrass"),
    ("month", "Mirtul"), ("month", "Kythorn"),
    ("month", "Flamerule"), ("intercalary", "Midsummer"),
    ("month", "Eleasis"), ("month", "Eleint"),
    ("intercalary", "Highharvestide"),
    ("month", "Marpenoth"), ("month", "Uktar"),
    ("intercalary", "Feast of the Moon"),
    ("month", "Nightal"),
]
_DAY_OF_YEAR: dict[str, int] = {}
_doy = 0
for _kind, _name in _SCHEDULE:
    if _kind == "month":
        for _d in range(1, 31):
            _DAY_OF_YEAR[f"{_name}-{_d}"] = _doy
            _doy += 1
    else:
        _DAY_OF_YEAR[_name] = _doy
        _doy += 1
YEAR_LEN = _doy  # 365

INTERCALARY_NAMES = tuple(n for k, n in _SCHEDULE if k == "intercalary")

TIME_ONLY_RE = re.compile(r"^~?\d{1,2}:\d{2}\??$")
TIME_RE = re.compile(r"^(~)?(\d{1,2}):(\d{2})(\?)?$")
DATE_RE = re.compile(r"^(\d+)(\?)?\s+([A-Za-z]+)(\?)?(?:\s+(\d+)\s*DR\??)?$")


# ---------- Frontmatter ----------

def read_frontmatter(path: Path) -> dict[str, str]:
    """Top-level scalar keys only — block lists and nested keys are ignored."""
    if not path.exists():
        return {}
    m = re.match(r"^---\n(.*?)\n---", path.read_text(), re.DOTALL)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if not line or line.startswith((" ", "-")) or ":" not in line:
            continue
        key, _, value = line.partition(":")
        out[key.strip()] = value.strip()
    return out


# ---------- in_fiction_date ----------

def parse_time(s: str) -> Optional[dict]:
    m = TIME_RE.match(s.strip()) if s else None
    if not m:
        return None
    return {
        "approx": bool(m.group(1)),
        "hour": int(m.group(2)),
        "minute": int(m.group(3)),
        "derived": bool(m.group(4)),
    }


def parse_date(s: str) -> Optional[dict]:
    s = s.strip()
    for name in INTERCALARY_NAMES:
        if s.startswith(name):
            rest = s[len(name):].strip()
            derived_day = rest.startswith("?")
            if derived_day:
                rest = rest[1:].strip()
            m = re.match(r"(\d+)\s*DR\??$", rest)
            return {
                "day": name,
                "month": "intercalary",
                "year": int(m.group(1)) if m else None,
                "derived_day": derived_day,
            }
    m = DATE_RE.match(s)
    if not m or m.group(3) not in MONTHS:
        return None
    return {
        "day": int(m.group(1)),
        "month": m.group(3),
        "year": int(m.group(5)) if m.group(5) else None,
        "derived_day": bool(m.group(2)),
    }


def parse_side(s: str, inherit: Optional[dict] = None) -> Optional[dict]:
    s = s.strip()
    if not s:
        return None
    if "," in s:
        date_part, time_part = (p.strip() for p in s.split(",", 1))
    elif TIME_ONLY_RE.match(s):
        date_part, time_part = "", s
    else:
        date_part, time_part = s, ""

    date = parse_date(date_part) if date_part else None
    if date is None:
        if inherit is None:
            return None
        date = {k: inherit[k] for k in ("day", "month", "year", "derived_day")}
    elif date["year"] is None and inherit is not None:
        date["year"] = inherit["year"]

    return {**date, "time": parse_time(time_part)}


def parse_in_fiction_date(ifd: str):
    if not ifd:
        return None, None
    left, _, right = ifd.partition("→")
    start = parse_side(left)
    if start is None:
        return None, None
    end = parse_side(right, inherit=start) if right.strip() else start
    return start, end or start


# ---------- Formatting ----------

def format_side(info: Optional[dict]) -> str:
    if info is None:
        return ""
    if info["month"] == "intercalary":
        date_part = info["day"]
    else:
        day_suffix = "?" if info.get("derived_day") else ""
        date_part = f"{info['day']}{day_suffix} {MONTH_ABBR[info['month']]}"
    t = info.get("time")
    if t is None:
        return date_part
    time_str = f"{'~' if t['approx'] else ''}{t['hour']:02d}:{t['minute']:02d}{'?' if t['derived'] else ''}"
    return f"{date_part} {time_str}"


def side_minutes(info: Optional[dict]) -> Optional[int]:
    if info is None or info.get("year") is None:
        return None
    key = info["day"] if info["month"] == "intercalary" else f"{info['month']}-{info['day']}"
    doy = _DAY_OF_YEAR[key]
    t = info.get("time")
    h, m = (t["hour"], t["minute"]) if t else (0, 0)
    return info["year"] * YEAR_LEN * 24 * 60 + doy * 24 * 60 + h * 60 + m


def _derived(info: dict) -> bool:
    t = info.get("time")
    return bool(info.get("derived_day") or (t and t.get("derived")))


def format_delta(prev_end: Optional[dict], this_start: Optional[dict]) -> str:
    if prev_end is None or this_start is None:
        return "—"
    a, b = side_minutes(prev_end), side_minutes(this_start)
    if a is None or b is None:
        return "—"
    suffix = "?" if (_derived(prev_end) or _derived(this_start)) else ""
    delta = b - a
    if delta == 0:
        return "✅" + suffix
    sign = "+" if delta > 0 else "-"
    days, rem = divmod(abs(delta), 24 * 60)
    hours, minutes = divmod(rem, 60)
    parts = [f"{n}{u}" for n, u in ((days, "d"), (hours, "h"), (minutes, "m")) if n]
    return f"{sign}{''.join(parts) or '0m'}{suffix}"


# ---------- Column checks ----------

def check_transcript(dir_: Path, n: int) -> str:
    tdir = dir_ / "inputs" / "transcripts"
    for stem in (f"transcript-{n:02d}.txt", f"transcript-dia-{n:02d}.txt"):
        if (tdir / stem).exists():
            return "✅"
    # No canonical transcript: decide ⚠️ (no audio captured) vs ❌ (audio
    # exists, transcript pending) by looking at inputs/audios/. Audio-present
    # sessions have real media files (.mp3, etc.); audioless sessions carry
    # only text markers like s<NN>_YYYY-MM-DD_NO-AUDIO.txt.
    audios = dir_ / "inputs" / "audios"
    if audios.is_dir():
        for f in audios.iterdir():
            if f.is_file() and f.suffix.lower() != ".txt":
                return "❌"
        return "⚠️"
    return "❌"


def check_minutes(dir_: Path, n: int) -> tuple[str, str]:
    fm = read_frontmatter(dir_ / f"minutes-{n:02d}.md")
    glyph = {"accepted": "✅", "drafted": "⚠️"}.get(fm.get("status", ""), "❌")
    return glyph, fm.get("in_fiction_date", "")


def check_outputs(dir_: Path, n: int) -> str:
    out = dir_ / "outputs"
    if not out.exists():
        return "❌"
    want = [f"S{n} - Minutes.pdf", f"S{n} - Saga.pdf", f"S{n} - GM.pdf"]
    found = sum(1 for name in want if (out / name).exists())
    return "❌" if found == 0 else "⚠️" if found < 3 else "✅"


# ---------- Table assembly ----------

def main() -> int:
    sessions = sorted(
        (p for p in ROOT.iterdir() if p.is_dir() and re.match(r"session-\d+$", p.name)),
        key=lambda p: int(p.name.split("-")[1]),
    )

    header = ["Session #", "Transcript", "Minutes", "Outputs", "start", "end", "delta"]
    rows: list[list[str]] = []
    prev_end: Optional[dict] = None

    for s in sessions:
        n = int(s.name.split("-")[1])
        minutes_glyph, ifd = check_minutes(s, n)
        start, end = parse_in_fiction_date(ifd)
        rows.append([
            f"{n:02d}",
            check_transcript(s, n),
            minutes_glyph,
            check_outputs(s, n),
            format_side(start),
            format_side(end),
            format_delta(prev_end, start) if start else "—",
        ])
        prev_end = end

    # Emoji glyphs render as two cells wide in most monospace editors;
    # VS16 (U+FE0F) is invisible. Everything else is one cell.
    WIDE = {"✅", "❌", "⚠"}

    def visual_len(s: str) -> int:
        w = 0
        for ch in s:
            if ch == "️":          # VS16 (invisible)
                continue
            w += 2 if ch in WIDE else 1
        return w

    floors = [9, 11, 8, 8, 15, 15, 10]
    widths = [max(floors[i], max(visual_len(r[i]) for r in [header, *rows])) for i in range(7)]

    def pad(s: str, width: int) -> str:
        return s + " " * (width - visual_len(s))

    row = lambda cells: "| " + " | ".join(pad(cells[i], widths[i]) for i in range(7)) + " |"
    sep = "| " + " | ".join("-" * w for w in widths) + " |"
    table = [row(header), sep, *(row(r) for r in rows)]

    current = STATUS_FILE.read_text()
    marker = "## Status\n"
    i = current.find(marker)
    if i < 0:
        print("status.md: '## Status' marker not found.", file=sys.stderr)
        return 1
    prefix_end = current.find("\n", i) + 1
    if current[prefix_end:prefix_end + 1] == "\n":
        prefix_end += 1
    STATUS_FILE.write_text(current[:prefix_end] + "\n" + "\n".join(table) + "\n")
    print(f"Wrote {len(rows)} session rows to {STATUS_FILE.relative_to(ROOT.parent)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
