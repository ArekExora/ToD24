#!/usr/bin/env python3
"""Convert a diarised WhisperX JSON into a SPEAKER_NN-labeled, sentence-per-line transcript.

Used by both Path B (our internal merged-track WhisperX output at
`inputs/audios/whisperx/merged.json`) and Path C (player-supplied external STT at
`inputs/transcripts/external/dia NN.json`). Both inputs share the same WhisperX schema —
`segments` with per-word `speaker` labels.

Pyannote groups multiple players' utterances into one VAD segment and assigns it a
single segment-level speaker label, but it *does* attribute each word to a speaker, and
~17% of segments have words spanning multiple speakers. This script walks `segment.words`,
splits each segment into contiguous same-speaker runs, and emits one line per run —
recovering the speaker attribution that the segment-level rollup loses.

Short runs (default <2 words) are treated as diarisation flicker and merged into the
previous run (or the next, if the flicker is at the start of a segment). Adjacent runs
that end up sharing a speaker after that merge are coalesced.

Usage:
    python3 split_merged.py path/to/whisperx.json [min_run] > dia-NN.txt

    min_run: minimum word count per emitted run (default 2). Lower this to retain more
    granularity at the cost of more flicker noise.

Each emitted line is passed through the shared cleanup in _clean.py (Amara/silence
hallucinations dropped, repetition loops collapsed) and tagged with a low-confidence
marker `~0.XX` when the avg per-word score is below LOW_CONF_THRESHOLD.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _clean import avg_confidence, clean_text, conf_marker  # noqa: E402

DEFAULT_MIN_RUN = 2


def fmt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def group_by_speaker(words: list, fallback_speaker: str | None) -> list[dict]:
    """Group consecutive words by speaker. Each group: {speaker, words: [word,...]}."""
    groups: list[dict] = []
    for w in words:
        sp = w.get("speaker") or fallback_speaker
        if not groups or groups[-1]["speaker"] != sp:
            groups.append({"speaker": sp, "words": []})
        groups[-1]["words"].append(w)
    return groups


def suppress_flicker(groups: list[dict], min_run: int, fallback_speaker: str | None) -> list[dict]:
    """Merge small (<min_run) groups into a neighbor; coalesce same-speaker adjacents.

    When *every* group in the segment is below threshold (e.g., a 2-word segment with
    one word per speaker), collapse to a single group labeled with the segment-level
    fallback speaker — that case is almost always pyannote flicker on a short utterance.
    """
    if min_run <= 1 or not groups:
        return groups

    # Pass 1: merge small groups into a neighbor.
    merged: list[dict] = []
    pending_prefix: list = []  # words from a leading small group, prepended to next normal group
    for g in groups:
        if len(g["words"]) < min_run:
            if merged:
                # Merge into the previous (keeps previous speaker label).
                merged[-1]["words"].extend(g["words"])
            else:
                # First group is small; defer its words to be prepended to the next group.
                pending_prefix.extend(g["words"])
            continue
        if pending_prefix:
            g = {"speaker": g["speaker"], "words": pending_prefix + g["words"]}
            pending_prefix = []
        merged.append(g)
    # All groups were below threshold — collapse to one group with the segment-level speaker.
    if pending_prefix and not merged:
        return [{"speaker": fallback_speaker, "words": pending_prefix}]

    # Pass 2: coalesce adjacent groups that ended up with the same speaker.
    final: list[dict] = []
    for g in merged:
        if final and final[-1]["speaker"] == g["speaker"]:
            final[-1]["words"].extend(g["words"])
        else:
            final.append(g)
    return final


def emit_segment(seg: dict, min_run: int) -> list[tuple[float | None, str, str, float | None]]:
    """Return [(start_seconds, speaker, text, conf), ...] for a segment."""
    words = seg.get("words") or []
    seg_speaker = seg.get("speaker") or "UNKNOWN"
    seg_start = seg.get("start")
    seg_text = (seg.get("text") or "").strip()

    if not words:
        if seg_text:
            return [(seg_start, seg_speaker, seg_text, None)]
        return []

    groups = group_by_speaker(words, fallback_speaker=seg_speaker)
    groups = suppress_flicker(groups, min_run, fallback_speaker=seg_speaker)

    out: list[tuple[float | None, str, str, float | None]] = []
    for g in groups:
        if not g["words"]:
            continue
        text = " ".join(w.get("word", "").strip() for w in g["words"] if w.get("word")).strip()
        if not text:
            continue
        start = next((w.get("start") for w in g["words"] if w.get("start") is not None), seg_start)
        out.append((start, g["speaker"] or seg_speaker, text, avg_confidence(g["words"])))
    return out


def main(json_path: str, min_run: int) -> int:
    data = json.loads(Path(json_path).read_text())
    segments = data.get("segments") or []
    for seg in segments:
        # Drop whole segment if its full text is a known hallucination — catches
        # cases where the per-speaker split fragments the canned phrase.
        if clean_text(seg.get("text", "")) is None:
            continue
        for start, speaker, text, conf in emit_segment(seg, min_run):
            cleaned = clean_text(text)
            if cleaned is None:
                continue
            ts = fmt_time(start) if start is not None else "??:??:??"
            print(f"[{ts}] {speaker}: {cleaned}{conf_marker(conf)}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print(f"usage: {sys.argv[0]} path/to/merged.json [min_run]", file=sys.stderr)
        sys.exit(2)
    min_run = int(sys.argv[2]) if len(sys.argv) == 3 else DEFAULT_MIN_RUN
    sys.exit(main(sys.argv[1], min_run))
