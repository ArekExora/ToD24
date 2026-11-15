#!/usr/bin/env python3
"""Compose `campaign/timeline.md` from per-session timelines + `campaign/arcs.md`.

Reads
-----
  campaign/arcs.md                   arc metadata (title, open, close, description,
                                     page-break positions) + the shared footer
  sessions/session-*/timeline-*.md   per-session event tables

Writes
------
  sessions/outputs/timeline.md       Homebrewery source, fully regenerated;
                                     rendered to sessions/outputs/Timeline.pdf
                                     by `.claude/skills/render_pdf.py`

The output is composed from scratch each run — any prior contents of
`campaign/timeline.md` are overwritten. Page breaks are driven entirely by the
`Page breaks after:` field in each arc's entry in `arcs.md`; the script never
infers breaks on its own, and new arcs do not automatically start a new page.

Each page-break entry identifies a specific event as `<date>, S<NN>, <index>`,
where `<index>` is 1-based among events sharing the same (date, session).

The arc frame emits exactly once per arc, on the arc's first appearance;
subsequent pages continue with month tables only.

Run
---
  python3 .claude/skills/timeline/build_full_timeline.py
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[3]
ARCS_PATH = ROOT / "campaign" / "arcs.md"
SESSIONS_DIR = ROOT / "sessions"
OUT_PATH = ROOT / "sessions" / "outputs" / "timeline.md"

# ---------------------------------------------------------------------------
# Calendar (mirrors `campaign/calendar-of-harptos.md` — Full column, in order)
# ---------------------------------------------------------------------------

MONTHS_FULL: List[str] = [
    "Hammer", "Alturiak", "Ches", "Tarsakh", "Mirtul", "Kythorn",
    "Flamerule", "Eleasias", "Eleint", "Marpenoth", "Uktar", "Nightal",
]
MONTH_INDEX: Dict[str, int] = {m: i for i, m in enumerate(MONTHS_FULL)}

# Intercalary days placed BETWEEN months. Value = index of the month that
# precedes the intercalary (0-based).
INTERCALARY_AFTER: Dict[str, int] = {
    "Midwinter": 0,          # between Hammer and Alturiak
    "Greengrass": 3,         # between Tarsakh and Mirtul
    "Midsummer": 6,          # between Flamerule and Eleasias
    "Highharvestide": 8,     # between Eleint and Marpenoth
    "Feast of the Moon": 10, # between Uktar and Nightal
}

# Sentinel sort value for intercalary rows: comes after day 30 of the anchor
# month so events on an intercalary display at the bottom of that month's table.
INTERCALARY_SORT: int = 100

# Default footer used when `## Footer` is missing from arcs.md.
DEFAULT_FOOTER: List[str] = [
    "{{pageNumber,auto}}",
    "{{footnote Tyranny of Dragons | Timeline}}",
]

PAGE_BREAK_LINE = r"\page"

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

# A page break identifies a specific event as the last on its page.
# Tuple: (day, month, year, session, index_within_date_session)
BreakEntry = Tuple[int, str, int, str, int]

@dataclass
class Arc:
    title: str
    opened: str                                   # "22 Marpenoth 1489 DR (S01)"
    description: str
    page_breaks_after: List[BreakEntry] = field(default_factory=list)
    opened_sort: Tuple[int, float, int] = (0, 0.0, 0)


@dataclass
class Event:
    arc_title: str
    year: int
    month: str
    day_sort: int            # leading day number; INTERCALARY_SORT for intercalary rows
    day_text: str            # Date cell as written
    session: str             # "S01"
    session_num: int
    text: str                # Event cell text


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

ARC_FIELD_RE = re.compile(r"^- \*\*(?P<key>[^:*]+?):\*\*\s*(?P<val>.*)$")
FR_DATE_RE = re.compile(r"^(?P<day>\d+)\s+(?P<month>\w+)\s+(?P<year>\d+)\s*DR\b")
OPENED_PART_RE = re.compile(r"^(?P<date>.+?)\s*(?:\((?P<sess>S\d+)\))?\s*$")
INDENTED_BULLET_RE = re.compile(r"^\s{2,}-\s+(?P<val>.+?)\s*$")
SESSION_RE = re.compile(r"^S\d+$")


def die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def warn(msg: str) -> None:
    print(f"WARNING: {msg}", file=sys.stderr)


def parse_fr_date(s: str) -> Optional[Tuple[int, str, int]]:
    """Parse an FR date to (day, month, year). Intercalary days use day=0."""
    s = s.strip()
    m = FR_DATE_RE.match(s)
    if m:
        return int(m["day"]), m["month"], int(m["year"])
    for intercalary in INTERCALARY_AFTER:
        if s.startswith(intercalary):
            rest = s[len(intercalary):].strip()
            m = re.match(r"(?P<year>\d+)\s*DR\b", rest)
            if m:
                return 0, intercalary, int(m["year"])
    return None


def month_sort_key(month: str, year: int) -> Tuple[int, float]:
    if month in MONTH_INDEX:
        return year, float(MONTH_INDEX[month])
    if month in INTERCALARY_AFTER:
        return year, INTERCALARY_AFTER[month] + 0.5
    return year, 99.0


def opened_sort_key(opened: str) -> Tuple[int, float, int]:
    m = OPENED_PART_RE.match(opened.strip())
    date_part = m["date"] if m else opened
    parsed = parse_fr_date(date_part)
    if not parsed:
        return 9999, 99.0, 99
    day, month, year = parsed
    _, idx = month_sort_key(month, year)
    return year, idx, day


def parse_break_entry(raw: str, arc_title: str) -> Optional[BreakEntry]:
    """Parse '23 Marpenoth 1489 DR, S03, 3' -> (23, 'Marpenoth', 1489, 'S03', 3)."""
    parts = [p.strip() for p in raw.split(",")]
    if len(parts) != 3:
        warn(f"arc '{arc_title}': break '{raw}' has {len(parts)} fields, expected 3 (date, session, index); skipped")
        return None
    date_part, session_part, index_part = parts
    parsed = parse_fr_date(date_part)
    if parsed is None:
        warn(f"arc '{arc_title}': break '{raw}' date '{date_part}' unparseable; skipped")
        return None
    day, month, year = parsed
    if not SESSION_RE.match(session_part):
        warn(f"arc '{arc_title}': break '{raw}' session '{session_part}' not in S<NN> form; skipped")
        return None
    try:
        index = int(index_part)
    except ValueError:
        warn(f"arc '{arc_title}': break '{raw}' index '{index_part}' not a number; skipped")
        return None
    if index < 1:
        warn(f"arc '{arc_title}': break '{raw}' index must be >= 1; skipped")
        return None
    return day, month, year, session_part, index


def parse_arc_body(body_lines: List[str], arc_title: str) -> Dict[str, object]:
    """Parse the lines of an arc's body into a {key: value} dict.

    Handles single-line fields and the multi-line `Page breaks after:` form
    where the value is an indented bullet list on subsequent lines.
    """
    body: Dict[str, object] = {}
    i = 0
    while i < len(body_lines):
        line = body_lines[i]
        stripped = line.strip()
        m = ARC_FIELD_RE.match(stripped)
        if not m:
            i += 1
            continue

        key = m["key"].strip().lower()
        val = m["val"].strip()

        if key == "page breaks after":
            # Multi-line form: field line has empty value; subsequent indented
            # bullets each hold one entry.
            if not val:
                entries: List[BreakEntry] = []
                j = i + 1
                while j < len(body_lines):
                    sub = body_lines[j]
                    if not sub.strip():
                        j += 1
                        continue
                    m2 = INDENTED_BULLET_RE.match(sub)
                    if not m2:
                        break
                    parsed = parse_break_entry(m2["val"], arc_title)
                    if parsed is not None:
                        entries.append(parsed)
                    j += 1
                body["page breaks after"] = entries
                i = j
                continue

            # Single-line form: either "(none)" or missing.
            if val.lower() in ("(none)", "none"):
                body["page breaks after"] = []
            else:
                # Single-line comma-separated would collide with field commas,
                # so we only accept "(none)" or the multi-line form.
                warn(
                    f"arc '{arc_title}': inline 'Page breaks after:' values must be "
                    f"'(none)' or move to indented sub-bullets; value '{val}' ignored"
                )
                body["page breaks after"] = []
        else:
            body[key] = val
        i += 1

    return body


def parse_footer(text: str) -> List[str]:
    """Extract the fenced code block under `## Footer`."""
    m = re.search(r"(?m)^## Footer\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if not m:
        return DEFAULT_FOOTER
    section = m.group(1)
    m2 = re.search(r"```(?:[^\n]*)\n(.*?)\n```", section, re.DOTALL)
    if not m2:
        warn("arcs.md § Footer has no fenced code block; using default footer")
        return DEFAULT_FOOTER
    body = m2.group(1).strip("\n")
    lines = [ln for ln in body.split("\n") if ln.strip()]
    if not lines:
        warn("arcs.md § Footer code block is empty; using default footer")
        return DEFAULT_FOOTER
    return lines


# Sections whose titles are not arcs. Case-insensitive match.
RESERVED_SECTION_TITLES: Set[str] = {
    "field reference",
    "page-break behaviour",
    "page break behaviour",
    "footer",
    "configuration",
}


def parse_arcs(path: Path) -> Tuple[Dict[str, Arc], List[str]]:
    if not path.exists():
        die(f"arcs file not found: {path}")
    text = path.read_text(encoding="utf-8")

    footer = parse_footer(text)

    arcs: Dict[str, Arc] = {}
    blocks = re.split(r"(?m)^## ", text)
    for block in blocks[1:]:
        lines = block.rstrip("\n").split("\n")
        title = lines[0].strip()
        if title.lower() in RESERVED_SECTION_TITLES:
            continue
        body_lines = lines[1:]
        body = parse_arc_body(body_lines, title)
        # Minimum field check — an arc section must have Opened.
        if "opened" not in body:
            continue
        page_breaks = body.get("page breaks after", [])
        if not isinstance(page_breaks, list):
            page_breaks = []
        arcs[title] = Arc(
            title=title,
            opened=str(body.get("opened", "")),
            description=str(body.get("description", "")),
            page_breaks_after=page_breaks,
            opened_sort=opened_sort_key(str(body.get("opened", ""))),
        )
    return arcs, footer


# Per-session parser --------------------------------------------------------

H2_RE = re.compile(r"^## (?P<title>.+?)\s*$")
H3_MONTH_RE = re.compile(r"^### (?P<month>[\w ]+?)\s+(?P<year>\d+)\s*DR\s*$")
SESSION_CELL_RE = re.compile(r"^S(?P<n>\d+)$")


def parse_session_timeline(path: Path, arc_titles: Set[str]) -> List[Event]:
    text = path.read_text(encoding="utf-8")
    events: List[Event] = []
    current_arc: Optional[str] = None
    current_month: Optional[str] = None
    current_year: Optional[int] = None
    in_table = False

    for line in text.split("\n"):
        stripped = line.strip()

        m = H2_RE.match(stripped)
        if m:
            current_arc = m["title"].strip()
            if current_arc not in arc_titles:
                die(f"{path.name}: arc '{current_arc}' not found in arcs.md")
            in_table = False
            continue

        m = H3_MONTH_RE.match(stripped)
        if m:
            current_month = m["month"].strip()
            current_year = int(m["year"])
            if (current_month not in MONTH_INDEX
                    and current_month not in INTERCALARY_AFTER):
                die(f"{path.name}: unknown month '{current_month}' in sub-header")
            in_table = False
            continue

        if stripped.startswith("|") and (
            ":--" in stripped or stripped.lower().startswith("| date")
        ):
            in_table = True
            continue

        if in_table and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cells) < 3:
                continue
            day_text, session, event_text = cells[0], cells[1], cells[2]
            m_sess = SESSION_CELL_RE.match(session)
            if not m_sess:
                die(f"{path.name}: malformed Session cell '{session}'")
            if current_arc is None or current_month is None or current_year is None:
                die(f"{path.name}: event row outside arc/month context")
            if day_text in INTERCALARY_AFTER:
                day_sort = INTERCALARY_SORT
            else:
                m_day = re.match(r"(\d+)", day_text)
                day_sort = int(m_day.group(1)) if m_day else 0
            events.append(Event(
                arc_title=current_arc,
                year=current_year,
                month=current_month,
                day_sort=day_sort,
                day_text=day_text,
                session=session,
                session_num=int(m_sess["n"]),
                text=event_text,
            ))
        elif in_table and not stripped.startswith("|"):
            in_table = False

    return events


# ---------------------------------------------------------------------------
# Composition
# ---------------------------------------------------------------------------

TABLE_HEADER = "| Date    | Session  | Event                      |"
TABLE_ALIGN  = "|:--------|:---------|:---------------------------|"


def group_events_by_arc_month(
    events: List[Event],
) -> Dict[str, Dict[Tuple[int, str], List[Event]]]:
    grouped: Dict[str, Dict[Tuple[int, str], List[Event]]] = {}
    for e in events:
        grouped.setdefault(e.arc_title, {}).setdefault((e.year, e.month), []).append(e)
    return grouped


def sort_events_in_month(events: List[Event]) -> List[Event]:
    return sorted(events, key=lambda e: (e.day_sort, e.session_num))


def flatten_arc_events(
    arc_events_by_month: Dict[Tuple[int, str], List[Event]],
) -> List[Event]:
    months_sorted = sorted(
        arc_events_by_month.keys(),
        key=lambda k: month_sort_key(k[1], k[0]),
    )
    flat: List[Event] = []
    for key in months_sorted:
        flat.extend(sort_events_in_month(arc_events_by_month[key]))
    return flat


def compute_break_indices(arc: Arc, events: List[Event]) -> Set[int]:
    """Resolve each (date, session, index) break to the matching event index.

    Enumerates the matching events in appearance order and picks the one at
    position `index - 1`. Logs a warning if a break has no match or the
    index is out of range.
    """
    indices: Set[int] = set()
    for brk in arc.page_breaks_after:
        bd_day, bd_month, bd_year, bd_sess, bd_idx = brk
        matches = [
            i for i, e in enumerate(events)
            if e.day_sort == bd_day
            and e.month == bd_month
            and e.year == bd_year
            and e.session == bd_sess
        ]
        if not matches:
            warn(
                f"arc '{arc.title}': page-break {_fmt_break(brk)} matches no event; skipped"
            )
            continue
        if bd_idx > len(matches):
            warn(
                f"arc '{arc.title}': page-break {_fmt_break(brk)} index {bd_idx} "
                f"exceeds matching event count ({len(matches)}); skipped"
            )
            continue
        indices.add(matches[bd_idx - 1])
    return indices


def _fmt_break(brk: BreakEntry) -> str:
    day, month, year, sess, idx = brk
    if day == 0:
        return f"'{month} {year} DR, {sess}, {idx}'"
    return f"'{day} {month} {year} DR, {sess}, {idx}'"


def format_row(e: Event) -> str:
    # Pad Date and Session for source-level column alignment.
    return f"| {e.day_text:<7} | {e.session:<8} | {e.text} |"


def derive_close(
    arc: Arc,
    arc_order: List[Arc],
    grouped: Dict[str, Dict[Tuple[int, str], List[Event]]],
) -> str:
    """Return the formatted close marker for an arc, or '' for ongoing.

    An arc is considered ongoing iff no later arc has opened yet (it's the
    last entry in `arc_order`). Otherwise the close is derived from the
    date of the arc's last event — the day the arc's narrative concluded.
    """
    try:
        idx = arc_order.index(arc)
    except ValueError:
        return ""
    if idx == len(arc_order) - 1:
        return ""  # latest arc → ongoing
    events_by_month = grouped.get(arc.title)
    if not events_by_month:
        return ""  # arc has no events yet — render ongoing so user notices
    flat = flatten_arc_events(events_by_month)
    if not flat:
        return ""
    last = flat[-1]
    # Extract the END day of the last event's Date cell. For a range
    # ("22 - 23", "30 - 2 Uktar"), use the far side; for a single day, use
    # the day_sort; for an intercalary row, use the intercalary name alone.
    if last.month in INTERCALARY_AFTER:
        return f"{last.month} {last.year} DR ({last.session})"
    end_day, end_month = _parse_date_end(last.day_text, last.month)
    if end_month in INTERCALARY_AFTER:
        return f"{end_month} {last.year} DR ({last.session})"
    return f"{end_day} {end_month} {last.year} DR ({last.session})"


def _parse_date_end(day_text: str, default_month: str) -> Tuple[int, str]:
    """Return (end_day, end_month) for a Date cell."""
    s = day_text.strip()
    if s in INTERCALARY_AFTER:
        return 0, s
    # Cross-month range: "DD - DD Month"
    m = re.match(r"^(\d+)\s*-\s*(\d+)\s+(\w[\w ]*?)\s*$", s)
    if m:
        return int(m.group(2)), m.group(3).strip()
    # Cross-month to intercalary: "DD - Feast of the Moon" — rare
    for intercal in INTERCALARY_AFTER:
        m = re.match(rf"^(\d+)\s*-\s*{re.escape(intercal)}\s*$", s)
        if m:
            return 0, intercal
    # Within-month range: "DD - DD"
    m = re.match(r"^(\d+)\s*-\s*(\d+)\s*$", s)
    if m:
        return int(m.group(2)), default_month
    # Single day
    m = re.match(r"^(\d+)", s)
    if m:
        return int(m.group(1)), default_month
    return 0, default_month


_ARC_DATE_WITH_SESSION = re.compile(r"^(.+?)\s*(\(S\d+\))\s*$")


def _bold_arc_date(s: str) -> str:
    """Bold the FR date portion of an arc-header `<date> (S<NN>)` string,
    leaving the session tag plain so the date reads like a heading date and
    the session anchor stays visually subordinate."""
    if not s:
        return s
    m = _ARC_DATE_WITH_SESSION.match(s)
    if m:
        return f"**{m.group(1).strip()}** {m.group(2)}"
    return f"**{s.strip()}**"


def format_arc_frame(arc: Arc, closed: str) -> List[str]:
    opened_bold = _bold_arc_date(arc.opened)
    if closed:
        date_range = f"{opened_bold} → {_bold_arc_date(closed)}"
    else:
        date_range = f"{opened_bold} → "
    return [
        "{{runeTable,wide,frame",
        "  {{note",
        f"  ## {arc.title}",
        f"  {date_range}",
        "  }}",
        arc.description,
        "}}",
    ]


def compose_arc_events_block(
    arc: Arc,
    arc_events_by_month: Dict[Tuple[int, str], List[Event]],
    footer: List[str],
) -> List[str]:
    """Emit one arc's full events section, including internal page breaks."""
    flat = flatten_arc_events(arc_events_by_month)
    breaks = compute_break_indices(arc, flat)

    out: List[str] = []
    current_my: Optional[Tuple[int, str]] = None
    inside_wide = False

    for i, e in enumerate(flat):
        this_my = (e.year, e.month)
        need_wide_open = not inside_wide
        need_month_header = (this_my != current_my) or need_wide_open

        if need_wide_open:
            out.append("{{wide")
            inside_wide = True

        if need_month_header:
            if not need_wide_open and current_my is not None:
                out.append("")  # blank line between tables within one wide block
            out.append(f"### {e.month} {e.year} DR")
            out.append(TABLE_HEADER)
            out.append(TABLE_ALIGN)
            current_my = this_my

        out.append(format_row(e))

        if i in breaks:
            out.append("}}")
            out.append("")           # blank line before footer, for human readability
            out.extend(footer)
            out.append(PAGE_BREAK_LINE)
            out.append("")           # blank line after \page, before the next wide block
            inside_wide = False
            current_my = None        # force month header to re-emit on next page

    if inside_wide:
        out.append("}}")

    return out


def compose_timeline(arcs: Dict[str, Arc], events: List[Event], footer: List[str]) -> str:
    # Inline CSS pins the Date and Session column widths so every event table
    # across every page lines up visually, regardless of its own content width.
    # All tables in this brew are event tables with the same three columns.
    style_block = [
        "<style>",
        "  table { table-layout: fixed; width: 100%; }",
        "  table th:nth-child(1), table td:nth-child(1) { width: 4em; }",
        "  table th:nth-child(2), table td:nth-child(2) { width: 5em; }",
        "</style>",
    ]
    out: List[str] = ["# Campaign timeline", "{wide}", ""] + style_block + [""]
    grouped = group_events_by_arc_month(events)
    arc_order = sorted(arcs.values(), key=lambda a: a.opened_sort)

    arc_sections_emitted = 0
    for arc in arc_order:
        if arc.title not in grouped:
            continue
        if arc_sections_emitted > 0:
            # Vertical spacer between arcs (not before the first one). `::`
            # is a Homebrewery V3 directive that opens up blank vertical room
            # on the page so arc frames don't visually collide.
            out.append("")
            out.append("::")
        closed = derive_close(arc, arc_order, grouped)
        out.extend(format_arc_frame(arc, closed))
        out.extend(compose_arc_events_block(arc, grouped[arc.title], footer))
        arc_sections_emitted += 1

    # Always close the last page with a footer. If the final lines include a
    # `\page` directive or trailing blanks (the last page break fell on the
    # final event), strip them — there's no next page to separate. If the
    # footer is then already in place, leave it; otherwise emit a fresh
    # footer preceded by a blank line (for human readability).
    while out and (out[-1] == PAGE_BREAK_LINE or not out[-1].strip()):
        out.pop()
    if len(out) < len(footer) or out[-len(footer):] != footer:
        out.append("")
        out.extend(footer)

    return "\n".join(out).rstrip("\n") + "\n"


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main() -> int:
    arcs, footer = parse_arcs(ARCS_PATH)
    print(f"Loaded {len(arcs)} arc(s) from {ARCS_PATH.relative_to(ROOT)}")
    print(f"Footer: {len(footer)} line(s)")

    arc_titles = set(arcs.keys())
    events: List[Event] = []
    timeline_files = sorted(SESSIONS_DIR.glob("session-*/timeline-*.md"))
    for timeline_file in timeline_files:
        events.extend(parse_session_timeline(timeline_file, arc_titles))
    print(f"Parsed {len(events)} event(s) across {len(timeline_files)} per-session file(s)")

    output = compose_timeline(arcs, events, footer)
    OUT_PATH.write_text(output, encoding="utf-8")
    print(f"Wrote {OUT_PATH.relative_to(ROOT)} ({len(output.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
