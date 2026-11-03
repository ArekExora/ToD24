#!/usr/bin/env python3
"""Realign Path A per-track timestamps to Path B (merged single-clock) times.

Path A produces one WhisperX pass per speaker track. Each track has its own
recording-clock drift (typically ±1-2 min over a ~4h session), which scrambles
cross-speaker ordering when merge_tracks.py sorts globally by timestamp
(same-speaker order stays correct — only cross-speaker order breaks).

Path B is a single merged audio with a single clock, so its timestamps are
globally consistent. This script matches each Path A line to the most similar
Path B line (bounded time window + token-set Jaccard, monotonically
constrained), fits a per-A-track linear drift function
(B_time ≈ slope * A_time + intercept) from the matched anchors, and re-times
every A line through its track's fit. Cross-speaker ordering after re-sorting
by corrected time aligns with real time (overlap noise aside).

Silent-player guard: if a track has fewer than MIN_ANCHORS matches, coverage
below MIN_COVERAGE, or a fit slope more than MAX_SLOPE_DEV from 1.0
(unphysical), that track's timestamps are left untouched and a warning is
emitted to stderr. Its lines may end up out of order relative to corrected
tracks — the alternative (dropping content or applying a bad model) is worse.

Usage:
    python3 realign_a_to_b.py <a_raw> <b_raw> > <a_raw_realigned>

Inputs share the format both merge_tracks.py and split_merged.py produce:
    [HH:MM:SS] speaker: text[ ~0.XX]
"""
from __future__ import annotations

import re
import sys
from bisect import bisect_left, bisect_right
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

# --- Config -----------------------------------------------------------------

BAND_S = 300              # search window (± seconds) for candidate matches
MIN_SIMILARITY = 0.4      # Jaccard threshold for a candidate to count
TOP_K_CANDIDATES = 5      # keep at most this many B candidates per A line
MIN_ANCHORS = 10          # per-track: min high-quality matches to fit drift
MIN_COVERAGE = 0.15       # per-track: min fraction of a-lines matched
MAX_SLOPE_DEV = 0.05      # per-track: reject fit if |slope - 1| > this

# Small Spanish stopword set: remove tokens that dominate short lines without
# carrying content. Keeps proper nouns, spells, place names.
STOPWORDS = frozenset({
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    "de", "del", "al", "que", "con", "sin", "por", "para", "en",
    "es", "son", "era", "eran", "ser", "fue", "sido",
    "se", "me", "te", "le", "les", "lo", "nos", "os",
    "mi", "tu", "su", "sus", "mis", "tus",
    "esta", "este", "estos", "estas",
    "eso", "esto", "esa", "ese", "esas", "esos",
    "muy", "más", "mas", "también", "tambien",
    "como", "cuando", "donde", "porque", "pero",
    "aún", "aun", "así", "asi",
    "ha", "he", "han", "has", "hay",
    "voy", "va", "vas", "van", "vamos", "vais",
    "sí", "no", "pues", "bueno", "vale",
})

LINE_RE = re.compile(
    r"^\[(\d{2}):(\d{2}):(\d{2})\]\s+([^:]+):\s*(.*?)(?:\s*~\d+\.\d+)?\s*$"
)
TS_PREFIX_RE = re.compile(r"^\[\d{2}:\d{2}:\d{2}\]")


# --- Types ------------------------------------------------------------------

@dataclass
class Line:
    idx: int                 # position in original file
    time_s: int              # timestamp, seconds
    speaker: str
    tokens: frozenset[str]   # content tokens for similarity
    raw: str                 # original line, verbatim


# --- Parsing ----------------------------------------------------------------

def tokenize(text: str) -> frozenset[str]:
    toks = re.findall(r"\w+", text.lower())
    return frozenset(t for t in toks if len(t) > 2 and t not in STOPWORDS)


def parse(path: Path) -> list[Line]:
    lines: list[Line] = []
    for idx, raw in enumerate(path.read_text().splitlines()):
        m = LINE_RE.match(raw)
        if not m:
            continue
        h, mnt, s, speaker, text = m.groups()
        t = int(h) * 3600 + int(mnt) * 60 + int(s)
        lines.append(Line(idx, t, speaker.strip(), tokenize(text), raw))
    return lines


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


# --- Matching ---------------------------------------------------------------

def find_candidates(
    a_track: list[Line], b_lines: list[Line], b_times: list[int]
) -> list[list[tuple[int, float]]]:
    """For each a_track line, return (b_index, similarity) candidates within
    ±BAND_S and above MIN_SIMILARITY, capped to top-K by similarity."""
    per_line: list[list[tuple[int, float]]] = []
    for a in a_track:
        lo = bisect_left(b_times, a.time_s - BAND_S)
        hi = bisect_right(b_times, a.time_s + BAND_S)
        cands: list[tuple[int, float]] = []
        for j in range(lo, hi):
            s = jaccard(a.tokens, b_lines[j].tokens)
            if s >= MIN_SIMILARITY:
                cands.append((j, s))
        cands.sort(key=lambda p: -p[1])
        per_line.append(cands[:TOP_K_CANDIDATES])
    return per_line


def best_monotonic_matches(
    candidates: list[list[tuple[int, float]]]
) -> list[tuple[int, int, float]]:
    """DP: select at most one B match per A line, monotonically increasing in
    both a-index and b-index, maximising total similarity. Returns
    (a_track_idx, b_idx, sim) triples."""
    flat: list[tuple[int, int, float]] = []
    for ai, cands in enumerate(candidates):
        for bj, s in cands:
            flat.append((ai, bj, s))
    if not flat:
        return []
    flat.sort()
    n = len(flat)
    best: list[tuple[float, int]] = [(f[2], -1) for f in flat]
    for k in range(n):
        ai_k, bj_k, s_k = flat[k]
        for p in range(k):
            ai_p, bj_p, _ = flat[p]
            if ai_p < ai_k and bj_p < bj_k:
                cand = best[p][0] + s_k
                if cand > best[k][0]:
                    best[k] = (cand, p)
    end = max(range(n), key=lambda i: best[i][0])
    chosen: list[tuple[int, int, float]] = []
    while end != -1:
        chosen.append(flat[end])
        end = best[end][1]
    chosen.reverse()
    return chosen


# --- Fitting ----------------------------------------------------------------

def linear_fit(pairs: list[tuple[float, float]]) -> tuple[float, float]:
    """Least-squares fit y ≈ slope * x + intercept."""
    n = len(pairs)
    sx = sum(x for x, _ in pairs)
    sy = sum(y for _, y in pairs)
    sxx = sum(x * x for x, _ in pairs)
    sxy = sum(x * y for x, y in pairs)
    denom = n * sxx - sx * sx
    if denom == 0:
        return 1.0, 0.0
    slope = (n * sxy - sx * sy) / denom
    intercept = (sy - slope * sx) / n
    return slope, intercept


def realign_track(
    a_track: list[Line], b_lines: list[Line], b_times: list[int], speaker: str
) -> dict[int, int]:
    """Return {a_line_original_idx: corrected_time_s}. Empty if the track
    fails the silent-player guard (caller leaves those timestamps as-is)."""
    if not a_track:
        return {}

    candidates = find_candidates(a_track, b_lines, b_times)
    chosen = best_monotonic_matches(candidates)

    if len(chosen) < MIN_ANCHORS:
        print(
            f"[realign] {speaker}: only {len(chosen)} anchors "
            f"(<{MIN_ANCHORS}); leaving track untouched",
            file=sys.stderr,
        )
        return {}

    coverage = len(chosen) / len(a_track)
    if coverage < MIN_COVERAGE:
        print(
            f"[realign] {speaker}: coverage {coverage:.1%} "
            f"(<{MIN_COVERAGE:.0%}); leaving track untouched",
            file=sys.stderr,
        )
        return {}

    pairs = [
        (float(a_track[ai].time_s), float(b_lines[bj].time_s))
        for ai, bj, _ in chosen
    ]
    slope, intercept = linear_fit(pairs)

    if abs(slope - 1.0) > MAX_SLOPE_DEV:
        print(
            f"[realign] {speaker}: fit slope {slope:.4f} deviates from 1.0 "
            f"by >{MAX_SLOPE_DEV}; leaving track untouched",
            file=sys.stderr,
        )
        return {}

    t0, t1 = a_track[0].time_s, a_track[-1].time_s
    drift_start = slope * t0 + intercept - t0
    drift_end = slope * t1 + intercept - t1
    print(
        f"[realign] {speaker}: {len(chosen)} anchors, coverage "
        f"{coverage:.1%}, slope {slope:.5f}, drift "
        f"{drift_start:+.1f}s @ start → {drift_end:+.1f}s @ end",
        file=sys.stderr,
    )

    return {
        line.idx: max(0, int(round(slope * line.time_s + intercept)))
        for line in a_track
    }


# --- Output -----------------------------------------------------------------

def fmt_ts(s: int) -> str:
    h, rem = divmod(s, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def emit(a_lines: list[Line], corrections: dict[int, int]) -> None:
    """Emit A lines with corrected timestamps where available, sorted by
    corrected time. Original file order breaks ties, preserving intra-speaker
    ordering (which is monotonic in original file order per track)."""
    out: list[tuple[int, int, str]] = []
    for line in a_lines:
        t = corrections.get(line.idx, line.time_s)
        new_raw = TS_PREFIX_RE.sub(f"[{fmt_ts(t)}]", line.raw, count=1)
        out.append((t, line.idx, new_raw))
    out.sort()
    for _, _, raw in out:
        print(raw)


# --- Main -------------------------------------------------------------------

def main(a_path: str, b_path: str) -> int:
    a_lines = parse(Path(a_path))
    b_lines = parse(Path(b_path))
    if not a_lines:
        print("[realign] empty A input; nothing to do", file=sys.stderr)
        return 1
    if not b_lines:
        print(
            "[realign] empty B input; skipping realignment, emitting A as-is",
            file=sys.stderr,
        )
        for line in a_lines:
            print(line.raw)
        return 0

    b_times = [b.time_s for b in b_lines]

    by_speaker: dict[str, list[Line]] = defaultdict(list)
    for line in a_lines:
        by_speaker[line.speaker].append(line)

    untouched_speakers: list[str] = []
    corrections: dict[int, int] = {}
    for speaker, track in by_speaker.items():
        result = realign_track(track, b_lines, b_times, speaker)
        if not result:
            untouched_speakers.append(speaker)
        corrections.update(result)

    if untouched_speakers:
        n = sum(len(by_speaker[s]) for s in untouched_speakers)
        print(
            f"[realign] {len(untouched_speakers)} track(s) untouched "
            f"({n} lines); their cross-speaker order relative to corrected "
            f"tracks may be off: {', '.join(untouched_speakers)}",
            file=sys.stderr,
        )

    emit(a_lines, corrections)
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} <a_raw> <b_raw>", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
