#!/usr/bin/env python3
"""Pre-flight track health check — flag broken-looking tracks before kicking off WhisperX.

Usage: python3 track_health.py <clean_dir>

Reads every *.wav in <clean_dir>, prints duration / mean-volume / max-volume per file,
and flags tracks that look short, quiet, or clipping. Surfaced before Step 2 so the GM
can catch a busted recording before spending an hour transcribing it.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def probe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True,
    ).stdout.strip()
    return float(out) if out else 0.0


def probe_volume(path: Path) -> tuple[float | None, float | None]:
    """Return (mean_db, max_db) from ffmpeg's volumedetect filter."""
    result = subprocess.run(
        ["ffmpeg", "-nostdin", "-hide_banner", "-i", str(path),
         "-af", "volumedetect", "-vn", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    mean_db = max_db = None
    for line in result.stderr.splitlines():
        if "mean_volume:" in line:
            mean_db = float(line.split("mean_volume:")[1].split("dB")[0].strip())
        elif "max_volume:" in line:
            max_db = float(line.split("max_volume:")[1].split("dB")[0].strip())
    return mean_db, max_db


def main(clean_dir: str) -> None:
    files = sorted(Path(clean_dir).glob("*.wav"))
    if not files:
        sys.exit(f"No .wav files in {clean_dir}")

    rows = []
    for f in files:
        rows.append((f.name, probe_duration(f), *probe_volume(f)))

    longest = max((r[1] for r in rows), default=0)

    print(f"{'Track':<28} {'Duration':>10} {'Mean':>9} {'Max':>9}  Flags")
    print("-" * 78)
    for name, dur, mean_db, max_db in rows:
        flags = []
        if longest > 0 and len(rows) > 1 and dur < 0.5 * longest:
            flags.append(f"short ({dur / longest * 100:.0f}% of longest)")
        if mean_db is not None and mean_db < -35:
            flags.append("quiet")
        if max_db is not None and max_db > -1:
            flags.append("clipping")
        mean_s = f"{mean_db:+6.1f}dB" if mean_db is not None else "      n/a"
        max_s = f"{max_db:+6.1f}dB" if max_db is not None else "      n/a"
        print(f"{name:<28} {dur:>9.0f}s {mean_s:>9} {max_s:>9}  {'; '.join(flags) or 'ok'}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 track_health.py <clean_dir>")
    main(sys.argv[1])
