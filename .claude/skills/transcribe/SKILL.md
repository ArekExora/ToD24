---
name: transcribe
description: Produce a session's canonicalised speaker-labelled transcript from one of three GM-selected sources — A (multi-track audio), B (merged single-track audio), or C (player-supplied STT). Prints ffmpeg/WhisperX commands for the GM to run on paths A and B, runs the merge/split scripts, then canonicalises names against the campaign roster.
---

# /transcribe

## Required input

- **Session number** (NN). Ask if absent.
- **Path**: `A` | `B` | `C`. Ask if absent. Folder contents do **not** determine the path.

| Path | Input | Final output |
|------|-------|--------------|
| A | `audios/tracks/*.{audio}` (one file per speaker) | `transcripts/transcript-NN.txt` |
| B | merged audio at `audios/` root | `transcripts/transcript-dia-NN.txt` |
| C | `transcripts/external/dia <AUDIO_NN>.json` (or `.txt + .tsv` fallback) | `transcripts/transcript-dia-NN.txt` |

B and C are mutually exclusive (both produce a dia witness); if both are run, the later run wins.

## Step rules

- **Idempotent.** Re-read disk on every invocation; skip steps whose outputs exist; emit ffmpeg/WhisperX loops that `continue` past existing outputs.
- **Halt before long-running compute** (ffmpeg, WhisperX) and after merge/split. Before each halt, summarise in one line what was found (e.g. *"5/7 tracks already cleaned"*).
- Ask before overwriting any existing target file — it may have been hand-corrected.

## Naming convention

Two numbers may differ for a single session: the **session number** (folder name `session-<NN>`) and the **audio number** embedded in the upstream filename (e.g. `dia 41 2026-05-01.m4a` → `41`). Players number recordings on their own count, which drifts from the campaign's session count.

- **Raw transcript** (`raw/*.txt`) — carries the **audio number**. Path B: `raw/dia-<AUDIO_NN>.txt`. Path C: `raw/dia-<AUDIO_NN>.txt` where `<AUDIO_NN>` is the number in `external/dia <AUDIO_NN>.json`. Path A has no shared audio number (tracks are keyed by speaker), so its raw uses the session number: `raw/session-<NN>.txt`.
- **Final (canonicalised) transcript** (`transcripts/transcript*.txt`) — always carries the **session number**: `transcript-<NN>.txt` (Path A) or `transcript-dia-<NN>.txt` (Paths B and C).

Before emitting any B4/C2 command, read the audio file's stem to extract `<AUDIO_NN>`; substitute it in the output path. Never conflate it with the session's `<NN>`.

---

## Path A — Multi-track

### A1 — Scaffold

Ensure `audios/{tracks,clean,whisperx}/` exists (`mkdir -p`). If `tracks/` is empty, halt and ask the GM to drop one audio file per speaker, named with the **character name as the stem** (e.g. `Amidamaru.ogg`, `GM.ogg`). The stem becomes the speaker label downstream — misnaming costs an unrecoverable rewrite.

### A2 — Cleanup

Validate each `tracks/*.{ext}` stem against `GM` + every active PC `name` in `campaign/pcs/*.md` (case-sensitive). Halt and surface mismatches; do not auto-rename. Then print, substituting `<NN>` and `<EXT>` (separate loop per extension if mixed):

```bash
cd "$(git rev-parse --show-toplevel)/sessions/session-<NN>/inputs/audios"
for f in tracks/*.<EXT>; do
  out="clean/$(basename "${f%.*}").wav"
  [ -f "$out" ] && continue
  ffmpeg -i "$f" -ac 1 -ar 16000 -c:a pcm_s16le "$out"
done
```

### A3 — WhisperX (per-track)

Pre-flight: run [track_health.py](track_health.py) on `clean/` and surface any `short`/`quiet`/`clipping` flags before launching ~1.5h × N tracks of compute.

```bash
cd "$(git rev-parse --show-toplevel)/sessions/session-<NN>/inputs/audios/clean"
VOCAB=$(cat "$(git rev-parse --show-toplevel)/.claude/skills/transcribe/vocab.txt")
for f in *.wav; do
  out="../whisperx/${f%.wav}.json"
  [ -f "$out" ] && continue
  whisperx "$f" --model large-v2 --language es --compute_type int8 \
    --initial_prompt "$VOCAB" --output_format json --output_dir ../whisperx
done
```

### A4 — Merge

```bash
cd "$(git rev-parse --show-toplevel)"
python3 .claude/skills/transcribe/merge_tracks.py sessions/session-<NN>/inputs/audios/whisperx/ > sessions/session-<NN>/inputs/transcripts/raw/session-<NN>.txt
```

Spot-check the head; flag if only one speaker appears or proper nouns look garbled.

### A5 — Canonicalise

[Canonicalisation](#canonicalisation): `raw/session-NN.txt` → `transcripts/transcript-NN.txt`.

---

## Path B — Merged single track

### B1 — Scaffold

Ensure `audios/{clean,whisperx}/` exists. Halt if no audio at audios/ root; ask the GM to drop the merged file (preserve the upstream name like `dia <AUDIO_NN>.mp3` or `Dia <AUDIO_NN> YYYY-MM-DD.m4a`; `<AUDIO_NN>` is the player's count, not the session number).

### B2 — Cleanup

```bash
cd "$(git rev-parse --show-toplevel)/sessions/session-<NN>/inputs/audios"
ffmpeg -i "<original-filename>" -ac 1 -ar 16000 merged.wav
```

Preserve quotes around the filename (it may contain spaces).

### B3 — WhisperX with diarisation

**Pre-flight** — any failure costs the full ~1.5h run. See [feedback_long_compute_preflight.md](../../memory/feedback_long_compute_preflight.md).

1. `$HF_TOKEN` is in the env (source `.env`; confirm with `echo $HF_TOKEN`).
2. Token has gated-repo read permission. Fine-grained tokens need this enabled at huggingface.co/settings/tokens; or use a legacy "Read" token.
3. The pyannote model is gating-accepted on its HF page. Default is `pyannote/speaker-diarization-community-1`; override to `pyannote/speaker-diarization-3.1` if needed.
4. Verify with one curl before running:

   ```bash
   source "$(git rev-parse --show-toplevel)/.env"
   curl -sI -H "Authorization: Bearer $HF_TOKEN" \
     https://huggingface.co/pyannote/speaker-diarization-community-1/resolve/main/config.yaml | head -1
   ```

   Want `HTTP/2 200` or a `302` redirect.

Ask the GM for the speaker count (DM + N players), then print:

```bash
cd "$(git rev-parse --show-toplevel)/sessions/session-<NN>/inputs/audios"
source "$(git rev-parse --show-toplevel)/.env"
VOCAB=$(cat "$(git rev-parse --show-toplevel)/.claude/skills/transcribe/vocab.txt")
SPEAKERS=<N>
whisperx merged.wav --model large-v2 --language es --diarize \
  --min_speakers $SPEAKERS --max_speakers $SPEAKERS \
  --initial_prompt "$VOCAB" --output_format json --output_dir whisperx
```

WhisperX logs `No --hf_token provided, needs to be saved in environment variable…` — expected. The token must come from the env, not the CLI, because `--hf_token` would leak through `ps aux`.

### B4 — Split

Read the audio file's stem to get `<AUDIO_NN>` (the number the player wrote in the upstream name, e.g. `dia 41 2026-05-01.m4a` → `41`). Then:

```bash
cd "$(git rev-parse --show-toplevel)"
python3 .claude/skills/transcribe/split_merged.py sessions/session-<NN>/inputs/audios/whisperx/merged.json > sessions/session-<NN>/inputs/transcripts/raw/dia-<AUDIO_NN>.txt
```

Halt if every line is the same speaker (failed diarisation).

### B5 — Canonicalise

[Canonicalisation](#canonicalisation): `raw/dia-<AUDIO_NN>.txt` → `transcripts/transcript-dia-<NN>.txt`.

---

## Path C — External dia witness

### C1 — Verify input

Look in `transcripts/external/`. Prefer `dia <AUDIO_NN>.json`; fall back to `dia <AUDIO_NN>.txt + dia <AUDIO_NN>.tsv` (loses confidence scores). Halt if neither set is present. `<AUDIO_NN>` is the number the player wrote on the file — it typically differs from `<NN>`.

### C2 — Split or pair

**With `.json`** (same script as Path B):

```bash
cd "$(git rev-parse --show-toplevel)"
python3 .claude/skills/transcribe/split_merged.py "sessions/session-<NN>/inputs/transcripts/external/dia <AUDIO_NN>.json" > sessions/session-<NN>/inputs/transcripts/raw/dia-<AUDIO_NN>.txt
```

**Fallback** (`.txt + .tsv` only): read both; halt if line counts disagree. For each paired entry: format `start_ms` from the `.tsv` as `[HH:MM:SS]`; pass the line body through [_clean.py](_clean.py); keep `[SPEAKER_NN]` verbatim; write `[HH:MM:SS] SPEAKER_NN: cleaned-text` to `raw/dia-<AUDIO_NN>.txt`. No confidence tags in this mode.

### C3 — Canonicalise

[Canonicalisation](#canonicalisation): `raw/dia-<AUDIO_NN>.txt` → `transcripts/transcript-dia-<NN>.txt`.

---

## Canonicalisation

Reads a `raw/` file, writes the corresponding `transcripts/` file. Files under `raw/` and `external/` are immutable — only `transcripts/` root is written.

### Context to gather

- **PC files** (`campaign/pcs/*.md`) — `name`, `player`, `nicknames`, `joined_at`. Drives speaker-handle → character-name conversion (Path A) and PC name canonicalisation (all paths). Exclude PCs with `joined_at > NN`.
- **NPC files** (`campaign/npcs/*.md`) — `name`, `full_name`. Any in-fiction form (full, short, surname) is valid output; speakers naturally pick whichever they're using.
- **Location files** (`campaign/locations/*.md`).
- **Prior session canon** (`sessions/session-<N-1>/{minutes,gm}-<N-1>.md`) and **calendar** for recurring names not yet in their own files.

### Per line

Input format: `[HH:MM:SS] handle-or-name: text`, optionally with a trailing ` ~0.XX` low-confidence marker.

1. **Strip the `~0.XX` marker.** It's advisory only — lines with the marker warrant a closer read for proper-noun garble during processing.
2. **Path A only**: convert lowercase player handles to canonical PC `name` (`gonzalo` → `Sinsong`); rewrite `DM:` → `GM:`. Paths B/C: keep `SPEAKER_NN` verbatim.
3. **Body text**: variants → canonical (e.g. *Talbot* → *Tarbaw*, *Busquilore* → *Eguzkilore*). PC `nicknames` from frontmatter are legitimate in-fiction handles — keep verbatim.
4. Write `[HH:MM:SS] speaker: cleaned-text`.

Hallucination filtering happened at merge/split time — don't re-run. If a hallucination slips through, surface to the GM rather than dropping silently.

## Boundary rules

- Never run ffmpeg or WhisperX inline — always print and halt.
- Every printed command starts with `cd "$(git rev-parse --show-toplevel)/<path>"` so the GM can paste from any cwd.
- Never inline [vocab.txt](vocab.txt) — use `$(cat …vocab.txt)` so the GM's edits are picked up at run time.
- Preserve upstream audio filenames (`dia <AUDIO_NN>.mp3`, `Dia <AUDIO_NN> YYYY-MM-DD.m4a`) in printed commands; do not rename. The audio's embedded number is the player's own count and often differs from the session's `<NN>` — see [Naming convention](#naming-convention).
