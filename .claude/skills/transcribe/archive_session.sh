#!/usr/bin/env bash
# archive_session.sh — stage a session's audio + transcripts for RAR archival.
#
# For session NN played on YYYY-MM-DD, produces
# sessions/outputs/archive/session-NN_YYYY-MM-DD/ containing:
#   - tracks/sNN_<Speaker>.mp3      from inputs/audios/tracks/<Speaker>.{wav,ogg,flac,...}
#   - sNN_YYYY-MM-DD.mp3            from inputs/audios/dia\ NN.{flac,wav,mp3,m4a,...}
#   - transcript-NN.txt             the canonical transcript — prefers
#                                   inputs/transcripts/transcript-NN.txt (Path A),
#                                   falls back to transcript-dia-NN.txt (Path B/C).
#                                   raw/ and external/ are excluded.
#
# The play-date is read from the `date:` field in sessions/session-NN/minutes-NN.md
# frontmatter, or --date YYYY-MM-DD if minutes don't exist yet.
#
# Encoding: libmp3lame, mono, VBR quality 5 (~90–110 kbps mono for speech).
# Non-destructive: sources are never modified or deleted. Existing MP3s in the
# archive are kept in place (not re-encoded), so re-runs are cheap and safe.
#
# Usage:
#   .claude/skills/transcribe/archive_session.sh 15
#   .claude/skills/transcribe/archive_session.sh 15 --date 2025-05-11
#   .claude/skills/transcribe/archive_session.sh 15 --dry-run
#
# After this succeeds, from the repo root:
#   rar a sessions/outputs/archive/session-15_<DATE>.rar sessions/outputs/archive/session-15_<DATE>/

set -euo pipefail

if [ $# -lt 1 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'
  exit 2
fi

DRY_RUN=0
DATE_OVERRIDE=""
POSITIONAL=()
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    --date) DATE_OVERRIDE="$2"; shift 2 ;;
    --date=*) DATE_OVERRIDE="${1#--date=}"; shift ;;
    *) POSITIONAL+=("$1"); shift ;;
  esac
done
set -- "${POSITIONAL[@]}"

NN=$(printf "%02d" "$((10#$1))")
REPO=$(git rev-parse --show-toplevel)
SESS_DIR="$REPO/sessions/session-$NN"
AUDIOS_DIR="$SESS_DIR/inputs/audios"
TRANSCRIPTS_DIR="$SESS_DIR/inputs/transcripts"
MINUTES_FILE="$SESS_DIR/minutes-$NN.md"

if [ ! -d "$SESS_DIR" ]; then
  echo "error: $SESS_DIR does not exist" >&2
  exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "error: ffmpeg not on PATH" >&2
  exit 1
fi

# Resolve the play-date: --date wins, else read `date:` from minutes frontmatter.
if [ -n "$DATE_OVERRIDE" ]; then
  PLAY_DATE="$DATE_OVERRIDE"
elif [ -f "$MINUTES_FILE" ]; then
  # First `date:` line inside the opening YAML block; grab the leading YYYY-MM-DD.
  PLAY_DATE=$(awk '
    /^---$/ { f++; if (f==2) exit; next }
    f==1 && /^date:/ { print; exit }
  ' "$MINUTES_FILE" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -1)
  if [ -z "$PLAY_DATE" ]; then
    echo "error: could not extract YYYY-MM-DD from $MINUTES_FILE 'date:' field" >&2
    echo "       pass --date YYYY-MM-DD to override" >&2
    exit 1
  fi
else
  echo "error: $MINUTES_FILE does not exist and no --date given" >&2
  echo "       pass --date YYYY-MM-DD (the real-world session date)" >&2
  exit 1
fi

if ! [[ "$PLAY_DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "error: play-date '$PLAY_DATE' is not YYYY-MM-DD" >&2
  exit 1
fi

SLUG="session-${NN}_${PLAY_DATE}"
SHORT="s${NN}"
ARCHIVE_DIR="$REPO/sessions/outputs/archive/$SLUG"
echo "session $NN, played $PLAY_DATE"
echo "archive: $ARCHIVE_DIR"
echo

run() {
  if [ "$DRY_RUN" -eq 1 ]; then
    printf '  [dry-run] '
    printf '%q ' "$@"
    printf '\n'
  else
    "$@"
  fi
}

encode_mp3() {
  local src="$1" out="$2"
  if [ -f "$out" ]; then
    echo "skip   $out"
    return 0
  fi
  local ext="${src##*.}"
  ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
  # For mp3 sources, copy only when already compliant (mono, <=128 kbps);
  # otherwise re-encode so every archive mp3 has the same q:a 5 mono shape.
  if [ "$ext" = "mp3" ]; then
    local chan kbps
    chan=$(ffprobe -v error -show_entries stream=channels -of default=noprint_wrappers=1:nokey=1 "$src" 2>/dev/null | head -1)
    kbps=$(ffprobe -v error -show_entries format=bit_rate -of default=noprint_wrappers=1:nokey=1 "$src" 2>/dev/null | awk '{printf "%d", $1/1000}')
    if [ "$chan" = "1" ] && [ "${kbps:-999}" -le 128 ] 2>/dev/null; then
      echo "copy   $src (compliant: ${kbps} kbps mono)"
      echo "    -> $out"
      run cp "$src" "$out"
      return 0
    fi
    echo "encode $src (non-compliant mp3: ${kbps} kbps, ${chan}ch)"
  else
    echo "encode $src"
  fi
  echo "    -> $out"
  run ffmpeg -hide_banner -loglevel error -n \
    -i "$src" -ac 1 -codec:a libmp3lame -q:a 5 "$out"
}

run mkdir -p "$ARCHIVE_DIR"

# --- 1. per-speaker tracks -------------------------------------------------
# Filter to known audio extensions so stray Notes.txt / .DS_Store / etc.
# don't get fed to ffmpeg (which would abort the whole run).
shopt -s nullglob nocaseglob
track_files=()
for ext in flac wav ogg mp3 m4a aac opus; do
  for f in "$AUDIOS_DIR"/tracks/*."$ext"; do
    track_files+=("$f")
  done
done
shopt -u nullglob nocaseglob

if [ ${#track_files[@]} -eq 0 ]; then
  echo "-- tracks: none at $AUDIOS_DIR/tracks (skipping)"
else
  echo "-- tracks: ${#track_files[@]} file(s) at $AUDIOS_DIR/tracks"
  run mkdir -p "$ARCHIVE_DIR/tracks"
  for src in "${track_files[@]}"; do
    [ -f "$src" ] || continue
    stem=$(basename "${src%.*}")
    encode_mp3 "$src" "$ARCHIVE_DIR/tracks/${SHORT}_${stem}.mp3"
  done
fi

# --- 2. joined audio (any audio file at audios/ root) ----------------------
# Ignore macOS .DS_Store cruft and whisperx intermediates (merged.wav,
# merged-*.wav). If multiple sources remain, archive each with its own stem.
shopt -s nullglob
joined_files=()
for ext in flac wav ogg mp3 m4a aac opus; do
  for f in "$AUDIOS_DIR"/*."$ext"; do
    base=$(basename "$f")
    case "$base" in
      .DS_Store) continue ;;
      merged.wav|merged-*.wav) continue ;;
    esac
    joined_files+=("$f")
  done
done
shopt -u nullglob

if [ ${#joined_files[@]} -eq 0 ]; then
  echo "-- joined: no audio at $AUDIOS_DIR root (skipping)"
elif [ ${#joined_files[@]} -eq 1 ]; then
  echo "-- joined: 1 file at $AUDIOS_DIR root"
  encode_mp3 "${joined_files[0]}" "$ARCHIVE_DIR/${SHORT}_${PLAY_DATE}.mp3"
else
  # Multi-file: the largest is the main session audio (gets the canonical
  # sNN_YYYY-MM-DD.mp3 name); supplementary files get a descriptor derived
  # from a parenthetical in the source name, or part2/part3/... as fallback.
  # Example: dia 37,5 (interrogatorio de Sinsong).m4a → sNN_YYYY-MM-DD_interrogatorio.mp3
  echo "-- joined: ${#joined_files[@]} files at $AUDIOS_DIR root (largest = main, others supplementary)"
  sorted=()
  while IFS= read -r line; do sorted+=("$line"); done < <(
    for f in "${joined_files[@]}"; do
      s=$(stat -f "%z" "$f" 2>/dev/null || stat -c "%s" "$f" 2>/dev/null)
      printf '%s\t%s\n' "$s" "$f"
    done | sort -rn | cut -f2-
  )
  idx=1
  for src in "${sorted[@]}"; do
    if [ "$idx" -eq 1 ]; then
      encode_mp3 "$src" "$ARCHIVE_DIR/${SHORT}_${PLAY_DATE}.mp3"
    else
      stem=$(basename "${src%.*}")
      if [[ "$stem" =~ \(([^\)]+)\) ]]; then
        descriptor=$(echo "${BASH_REMATCH[1]}" | awk '{print $1}' | tr '[:upper:]' '[:lower:]')
      else
        descriptor="part${idx}"
      fi
      encode_mp3 "$src" "$ARCHIVE_DIR/${SHORT}_${PLAY_DATE}_${descriptor}.mp3"
    fi
    idx=$((idx+1))
  done
fi

# --- 3. transcripts (canonical + variants) --------------------------------
# Canonical: transcript-NN.txt or transcript-dia-NN.txt.
# Variants: transcript-NN-<tag>.txt, transcript-dia-NN-<tag>.txt (e.g. per-session
# GM corrections, interrogatorios), and the legacy transcript-joined-NN.txt.
# Each matching file is copied verbatim so the archive preserves the full set.
shopt -s nullglob
transcript_srcs=()
for pattern in \
  "$TRANSCRIPTS_DIR/transcript-$NN.txt" \
  "$TRANSCRIPTS_DIR/transcript-$NN"-*.txt \
  "$TRANSCRIPTS_DIR/transcript-dia-$NN.txt" \
  "$TRANSCRIPTS_DIR/transcript-dia-$NN"-*.txt \
  "$TRANSCRIPTS_DIR/transcript-joined-$NN.txt"; do
  for f in $pattern; do
    [ -f "$f" ] && transcript_srcs+=("$f")
  done
done
shopt -u nullglob

if [ ${#transcript_srcs[@]} -eq 0 ]; then
  echo "-- transcript: none at $TRANSCRIPTS_DIR (skipping)"
else
  echo "-- transcript: ${#transcript_srcs[@]} file(s)"
  for src in "${transcript_srcs[@]}"; do
    out="$ARCHIVE_DIR/$(basename "$src")"
    echo "    -> $out"
    run cp "$src" "$out"
  done
fi

# --- 4. NO_AUDIO sentinel for lost-audio sessions -------------------------
# Empty file named sNN_YYYY-MM-DD_NO-AUDIO.txt — the filename self-describes;
# the body stays blank. Sorts alongside the session's other files and
# self-identifies by session+date even when extracted standalone.
if [ ${#track_files[@]} -eq 0 ] && [ ${#joined_files[@]} -eq 0 ]; then
  sentinel="$ARCHIVE_DIR/${SHORT}_${PLAY_DATE}_NO-AUDIO.txt"
  echo "-- NO_AUDIO sentinel: generating (no audio sources found)"
  run touch "$sentinel"
fi

# --- summary ---------------------------------------------------------------
echo
if [ "$DRY_RUN" -eq 1 ]; then
  echo "dry-run complete. re-run without --dry-run to write."
else
  echo "done. archive:"
  du -h -d 1 "$ARCHIVE_DIR" | sed 's/^/  /'
  echo
  echo "next:"
  echo "  rar a $ARCHIVE_DIR.rar $ARCHIVE_DIR/"
fi
