#!/usr/bin/env python3
"""Merge per-player WhisperX JSONs into one chronological speaker-labeled transcript.

Usage: python3 merge_tracks.py <whisperx_dir>

Reads every *.json in <whisperx_dir>; each filename stem becomes the speaker
label (e.g. DM.json -> "DM"). Prints the merged transcript to stdout.

Algorithm:
  1. Per segment, split into sub-segments on sentence-final punctuation and on
     inter-word pauses > PAUSE_THRESHOLD_S. Each sub-segment carries the
     first word's start time and avg per-word confidence.
  2. Drop or collapse known STT hallucinations (Amara subtitle credits, single-
     character cascades, repetition loops, numeric runaway). See _clean.py.
  3. Sort sub-segments chronologically across tracks.
  4. Cross-track bleed dedup: when two different speakers produce near-
     identical text within BLEED_TIME_WINDOW_S, drop the lower-confidence side
     (mic bleed on the other player's track).
  5. Append a `~0.XX` tag to lines whose avg confidence is below
     LOW_CONF_THRESHOLD so the canonicalisation step can spot suspect lines.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _clean import avg_confidence, clean_text, conf_marker  # noqa: E402

SENTENCE_END = re.compile(r"[.!?]['\"”’»]?$")
PAUSE_THRESHOLD_S = 0.8
BLEED_TIME_WINDOW_S = 2.0
BLEED_JACCARD = 0.7
BLEED_MIN_CONF_GAP = 0.15


def fmt_ts(s):
    h, rem = divmod(int(s), 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def _flush(buf, seg_start):
    start = next((w.get("start") for w in buf if w.get("start") is not None), seg_start)
    text = " ".join((w.get("word") or "").strip() for w in buf if w.get("word")).strip()
    conf = avg_confidence(buf)
    return start, text, conf


def iter_subsegments(seg):
    """Yield (start, text, conf) per sentence- or pause-bounded sub-segment."""
    words = seg.get("words") or []
    seg_start = seg.get("start")

    if not words:
        text = (seg.get("text") or "").strip()
        if text:
            yield seg_start, text, None
        return

    buf = []
    prev_end = None
    for w in words:
        s = w.get("start")
        if buf and prev_end is not None and s is not None and (s - prev_end) > PAUSE_THRESHOLD_S:
            yield _flush(buf, seg_start)
            buf = []

        buf.append(w)
        if w.get("end") is not None:
            prev_end = w["end"]

        wt = (w.get("word") or "").strip()
        if wt and SENTENCE_END.search(wt):
            yield _flush(buf, seg_start)
            buf = []

    if buf:
        yield _flush(buf, seg_start)


def _normalize_tokens(text):
    return set(re.findall(r"\w+", text.lower()))


def dedupe_bleed(items):
    """Drop cross-track bleed: near-identical text on different speakers within
    a small time window. Keep the higher-confidence side."""
    keep = [True] * len(items)
    for i in range(len(items)):
        if not keep[i]:
            continue
        ti, si, txi, ci = items[i]
        toks_i = _normalize_tokens(txi)
        if len(toks_i) < 2:
            continue
        j = i + 1
        while j < len(items) and items[j][0] - ti < BLEED_TIME_WINDOW_S:
            if keep[j]:
                tj, sj, txj, cj = items[j]
                if si != sj:
                    toks_j = _normalize_tokens(txj)
                    union = toks_i | toks_j
                    if union:
                        sim = len(toks_i & toks_j) / len(union)
                        if sim >= BLEED_JACCARD:
                            ci_s = ci if ci is not None else 0.0
                            cj_s = cj if cj is not None else 0.0
                            if abs(ci_s - cj_s) >= BLEED_MIN_CONF_GAP:
                                if ci_s >= cj_s:
                                    keep[j] = False
                                else:
                                    keep[i] = False
                                    break
            j += 1
    return [it for it, k in zip(items, keep) if k]


def main(whisperx_dir):
    items = []
    for jf in Path(whisperx_dir).glob("*.json"):
        speaker = jf.stem
        data = json.loads(jf.read_text())
        for seg in data.get("segments", []):
            # Whole-segment hallucination check first — catches cases where the
            # silence-hallucination text gets fragmented by the pause-split (e.g.
            # "Subtítulos por la comunidad de" / "Amara.org" on two lines).
            if clean_text(seg.get("text", "")) is None:
                continue
            for start, text, conf in iter_subsegments(seg):
                if start is None or not text:
                    continue
                cleaned = clean_text(text)
                if cleaned is None:
                    continue
                items.append((start, speaker, cleaned, conf))
    items.sort(key=lambda x: x[0])
    items = dedupe_bleed(items)
    for start, speaker, text, conf in items:
        print(f"[{fmt_ts(start)}] {speaker}: {text}{conf_marker(conf)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 merge_tracks.py <whisperx_dir>")
    main(sys.argv[1])
