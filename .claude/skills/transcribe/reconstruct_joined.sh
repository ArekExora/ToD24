#!/usr/bin/env bash
# reconstruct_joined.sh — sum per-speaker tracks into a single joined MP3.
#
# For each sessions/session-NN/ where inputs/audios/tracks/ has ≥2 files and
# no other audio exists at inputs/audios/ root, sum the tracks with ffmpeg's
# amix filter and write:
#   sessions/session-NN/inputs/audios/dia-NN-joined.mp3
#
# Craig-style multi-track recorders pad each speaker's track with silence to
# session start, so summing the tracks reconstructs a functional joined stream.
# The `-joined` suffix distinguishes this from a physical joined recording
# (dia NN.flac): a reconstruction has no room ambience or mic bleed.
#
# Non-destructive: sources are never modified.
# Idempotent: existing output is skipped; sessions with a physical joined audio
# at audios/ root are skipped entirely.
#
# Encoding: libmp3lame, mono, VBR quality 5. `amix normalize=0` sums the tracks
# at recording level (matches Craig's own merged output); dividing by input
# count would leave each speaker ~1/N as loud.
#
# Usage:
#   .claude/skills/transcribe/reconstruct_joined.sh                # scan all sessions
#   .claude/skills/transcribe/reconstruct_joined.sh 11 12 15       # only specified sessions
#   .claude/skills/transcribe/reconstruct_joined.sh --dry-run      # preview
#   .claude/skills/transcribe/reconstruct_joined.sh --force 11     # regenerate existing

set -eo pipefail

DRY_RUN=0
FORCE=0
SESSION_FILTER=()

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    --force) FORCE=1; shift ;;
    -h|--help) sed -n '2,28p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) SESSION_FILTER+=("$1"); shift ;;
  esac
done

REPO=$(git rev-parse --show-toplevel)

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "error: ffmpeg not on PATH" >&2
  exit 1
fi
if ! command -v ffprobe >/dev/null 2>&1; then
  echo "error: ffprobe not on PATH" >&2
  exit 1
fi

run() {
  if [ "$DRY_RUN" -eq 1 ]; then
    printf '  [dry-run] '
    printf '%q ' "$@"
    printf '\n'
  else
    "$@"
  fi
}

# Determine list of session dirs to process.
if [ ${#SESSION_FILTER[@]} -gt 0 ]; then
  session_dirs=()
  for n in "${SESSION_FILTER[@]}"; do
    NN=$(printf "%02d" "$((10#$n))")
    d="$REPO/sessions/session-$NN"
    if [ ! -d "$d" ]; then
      echo "warning: $d does not exist, skipping" >&2
      continue
    fi
    session_dirs+=("$d")
  done
else
  shopt -s nullglob
  session_dirs=("$REPO"/sessions/session-*/)
  shopt -u nullglob
fi

reconstructed=0
skipped=0
no_tracks=0
for sess_dir in "${session_dirs[@]}"; do
  sess_dir="${sess_dir%/}"
  base=$(basename "$sess_dir")
  NN="${base#session-}"

  audios="$sess_dir/inputs/audios"
  tracks_dir="$audios/tracks"

  shopt -s nullglob
  track_files=("$tracks_dir"/*)
  shopt -u nullglob

  # Filter to actual files (skip subdirs, dotfiles).
  filtered=()
  for f in "${track_files[@]}"; do
    [ -f "$f" ] || continue
    case "$(basename "$f")" in .*) continue ;; esac
    filtered+=("$f")
  done
  track_files=("${filtered[@]}")

  if [ ${#track_files[@]} -lt 2 ]; then
    no_tracks=$((no_tracks+1))
    continue
  fi

  # Detect physical joined audio at audios/ root — but tolerate our own output.
  shopt -s nullglob
  root_audio=()
  for ext in flac wav ogg mp3 m4a aac opus; do
    for f in "$audios"/*."$ext"; do
      [ "$(basename "$f")" = "dia-$NN-joined.mp3" ] && continue
      root_audio+=("$f")
    done
  done
  shopt -u nullglob

  out="$audios/dia-$NN-joined.mp3"

  if [ ${#root_audio[@]} -gt 0 ]; then
    echo "[$base] skip: joined already present (${root_audio[0]##*/})"
    skipped=$((skipped+1))
    continue
  fi

  if [ -f "$out" ] && [ "$FORCE" -eq 0 ]; then
    echo "[$base] skip: $(basename "$out") already exists (--force to regenerate)"
    skipped=$((skipped+1))
    continue
  fi

  echo "[$base] reconstruct from ${#track_files[@]} track(s):"
  for f in "${track_files[@]}"; do echo "         $(basename "$f")"; done

  # Sanity check: track durations should be close (Craig-style tracks share t=0).
  durations=()
  for f in "${track_files[@]}"; do
    d=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null || echo "0")
    durations+=("$d")
  done
  read -r min max <<<"$(printf '%s\n' "${durations[@]}" | awk '
    BEGIN{min=1e18; max=0}
    {if($1+0<min)min=$1+0; if($1+0>max)max=$1+0}
    END{printf "%d %d\n", min, max}')"
  diff=$((max - min))
  if [ "$diff" -gt 5 ]; then
    echo "         warning: durations differ by ${diff}s (min=${min}s max=${max}s) — tracks may not be time-aligned; reconstruction quality may suffer"
  fi

  ff_args=()
  for f in "${track_files[@]}"; do ff_args+=(-i "$f"); done
  N=${#track_files[@]}
  ff_args+=(
    -filter_complex "amix=inputs=$N:duration=longest:normalize=0"
    -ac 1 -codec:a libmp3lame -q:a 5
    "$out"
  )

  echo "         -> $(basename "$out")"
  run ffmpeg -hide_banner -loglevel error -n "${ff_args[@]}"
  reconstructed=$((reconstructed+1))
done

echo
echo "done: reconstructed=$reconstructed skipped=$skipped no-tracks=$no_tracks"
if [ "$DRY_RUN" -eq 1 ]; then echo "(dry-run — nothing written)"; fi
