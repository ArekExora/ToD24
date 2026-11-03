# Session Transcription Guide

How to turn session audio into a clean, canonicalised transcript. Two paths: **multi-track** (one audio file per player — preferred) and **merged-track** (a single mixed file — fallback). The output files (`transcript-<NN>.txt`, `transcript-dia-<NN>.txt`) are the end of this skill's responsibility.

> **Tip:** [`/transcribe <NN>`](SKILL.md) walks the GM through this pipeline, scaffolds the folders, detects the path, and prints the exact ffmpeg/whisperx commands customized to the session. The skill doesn't replace this guide (which explains *why* each step exists) — it just removes the copy-paste.

Files in this folder (siblings of [SKILL.md](SKILL.md)):
- [README.md](README.md) — this guide
- [vocab.txt](vocab.txt) — campaign vocabulary fed to Whisper as `--initial_prompt`; **edit when new important names appear**
- [merge_tracks.py](merge_tracks.py) — combines per-player WhisperX JSONs into one chronological transcript (Path A)
- [split_merged.py](split_merged.py) — converts a Path B `merged.json` into a `SPEAKER_NN`-labeled, sentence-per-line transcript by splitting on word-level speaker changes

Per-session content lives under `sessions/session-<NN>/inputs/`:
- `inputs/audios/` — raw audio + intermediate WhisperX JSONs (audio gitignored by extension; JSONs committed)
- `inputs/transcripts/raw/` — `/transcribe`'s merge output: `session-<NN>.txt` (Path A) or `dia-<NN>.txt` (Path B), speaker-labeled, hallucination-filtered, committed
- `inputs/transcripts/external/` — player-supplied raw transcripts (`dia <NN>.json`, `dia <NN>.txt + .tsv`, and companions); not produced by `/transcribe`'s audio paths but consumed by Path C (external dia witness)
- `inputs/transcripts/transcript-<NN>.txt` and `transcript-dia-<NN>.txt` — `/transcribe`'s canonicalised outputs at the root (final step of each path); the durable, committed witnesses for the session

---

## What you'll need (one-time setup)

Install once on the Mac. Copy-paste each block into Terminal.

### 1. Homebrew tools

```bash
brew install ffmpeg python@3.11
```

`ffmpeg` does audio preprocessing. Python is for WhisperX.

### 2. WhisperX

```bash
python3.11 -m venv ~/.venvs/whisperx
source ~/.venvs/whisperx/bin/activate
pip install whisperx
echo 'alias whisperx="$HOME/.venvs/whisperx/bin/whisperx"' >> ~/.zshrc
source ~/.zshrc
```

This creates an isolated Python environment so WhisperX doesn't conflict with anything else, and aliases `whisperx` to the venv binary so you can call it from any new shell without re-activating the venv. (Pip-installed entry points have an absolute-path shebang to the venv's Python, so the alias resolves dependencies correctly without `source ...activate`.)

### 3. HuggingFace token (only needed for merged tracks)

Diarization (figuring out who said what on a merged track) uses a gated model. Skip this if you only ever use multi-track.

1. Make a free account at https://huggingface.co
2. Visit https://huggingface.co/pyannote/speaker-diarization-3.1 and click **Agree and access**
3. Visit https://huggingface.co/pyannote/segmentation-3.0 and click **Agree and access**
4. Generate a token at https://huggingface.co/settings/tokens (read access is enough)
5. Save it in your shell profile:

   ```bash
   echo 'export HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxx"' >> ~/.zshrc
   source ~/.zshrc
   ```

### 4. Verify

```bash
ffmpeg -version
whisperx --help
echo $HF_TOKEN   # should print your token (only needed for merged tracks)
```

If all three work, you're set.

---

## Keep [vocab.txt](vocab.txt) up to date

This is the single most impactful tweak. Whisper biases its vocabulary toward terms it sees in an `--initial_prompt`, which is how you fix garbled PC names, NPC names, places, and homebrew terms like *carnomorfo*.

[vocab.txt](vocab.txt) is one comma-separated line. Add new important names (PCs, recurring NPCs, locations, factions, homebrew terms) as the campaign introduces them. Keep it under ~200 words — Whisper truncates long prompts.

---

## Path A: Multi-track (one file per player)

Use this whenever you have separate audio files (Craig bot, OBS, Audacity, Riverside, etc.).

### Step 1 — Organize the files

Put the raw audio in the session's audios folder:

```
sessions/session-42/inputs/audios/
  ├── tracks/        ← raw per-player audio (input)
  │   ├── DM.ogg
  │   ├── pablo.ogg
  │   ├── richy.ogg
  │   ├── javier.ogg
  │   ├── alfonso.ogg
  │   ├── sergio.ogg
  │   ├── victor.ogg
  │   └── gonzalo.ogg
  ├── clean/         ← populated in Step 2
  └── whisperx/      ← populated in Step 3
```

The filename (minus extension) becomes the speaker label in the final transcript. Use the player's real first name or `DM`. Any format ffmpeg can read works (`.ogg`, `.flac`, `.wav`, `.m4a`, `.mp3`) — they all become `.wav` after cleanup.

### Step 2 — Clean each track

Run this loop from the session's audios folder. It normalizes loudness, removes background noise, and trims silence, writing the cleaned WAVs into the sibling `clean/` folder.

```bash
cd "$(git rev-parse --show-toplevel)/sessions/session-42/inputs/audios"
for f in tracks/*.ogg; do
  [ -f "$f" ] || continue
  base=$(basename "$f")
  ffmpeg -i "$f" \
    -af "highpass=80,lowpass=8000,afftdn=nr=12,loudnorm=I=-16:LRA=11:TP=-1.5" \
    -ar 16000 -ac 1 -c:a pcm_s16le \
    "clean/${base%.*}.wav"
done
```

What each filter / option does:
- `highpass=80` — cuts rumble below 80 Hz (table thumps, AC hum)
- `lowpass=8000` — cuts hiss above 8 kHz (voice doesn't need it)
- `afftdn=nr=12` — FFT-based denoising, ~12 dB reduction
- `loudnorm` — broadcast-standard loudness so quiet players come up
- `-ar 16000 -ac 1 -c:a pcm_s16le` — downmix to mono 16 kHz 16-bit PCM. Whisper resamples to this internally anyway, and it keeps each cleaned file well under WAV's 4 GB header limit (a 4-hour track ends up ~450 MB instead of multi-gigabyte).

### Step 3 — Transcribe each track

```bash
cd "$(git rev-parse --show-toplevel)/sessions/session-42/inputs/audios/clean"
VOCAB=$(cat "$(git rev-parse --show-toplevel)/.claude/skills/transcribe/vocab.txt")
for f in *.wav; do
  whisperx "$f" \
    --model large-v3 \
    --language es \
    --vad_method silero \
    --initial_prompt "$VOCAB" \
    --output_format json \
    --output_dir ../whisperx
done
```

This produces one JSON per player in `sessions/session-42/inputs/audios/whisperx/`. Each segment has start/end timestamps.

> **Heads up:** the first run downloads the `large-v3` model (~3 GB). Subsequent runs are fast. On Apple Silicon, expect roughly 0.3–0.5x realtime — a 4-hour session takes ~1.5 hours per track, but they can run sequentially overnight.

### Step 4 — Merge into one transcript

[merge_tracks.py](merge_tracks.py) combines all per-player JSONs into one chronological file with speaker labels. Generate it inside the audios folder first so you can review it before promoting it to the sibling `transcripts/`:

```bash
cd "$(git rev-parse --show-toplevel)/sessions/session-42/inputs/audios"
python3 "$(git rev-parse --show-toplevel)/.claude/skills/transcribe/merge_tracks.py" whisperx/ > session-42.txt
```

Output looks like:

```
[00:14:32] DM: Os encontráis ante las puertas de Greenest...
[00:14:40] pablo: ¿Veo guardias en la muralla?
[00:14:45] DM: Veis tres figuras patrullando...
```

Eyeball the head and tail of the file (`head -50` / `tail -20`) — confirm speaker labels look right and proper nouns came through (Greenest, Langdedrosa, carnomorfo, etc.). Once you're happy, move it into the sibling `transcripts/raw/` folder:

```bash
mkdir -p ../transcripts/raw
mv session-42.txt ../transcripts/raw/
```

That moved file is the Path A primary witness — the cleaned, canonicalised transcript. Transcription ends here.

---

## Path B: Merged track (one mixed file)

Use this when you only have a single combined recording.

### Step 1 — Put the file in place

```
sessions/session-42/inputs/audios/
  └── dia 42.mp3   # or whatever your original filename is — keep it as-is
```

The merged file lives at the root of the audios folder. Filename can be anything (`dia 42.mp3`, `Dia 41 2026-05-01.m4a`, etc.) — substitute your actual filename in the commands below.

### Step 2 — Convert to a clean WAV

Merged recordings from Discord, Zoom, etc. are already normalized and compressed. Heavy ffmpeg processing on top can blur voices and *hurt* speaker separation. Just convert to WAV at Whisper's expected sample rate:

```bash
cd "$(git rev-parse --show-toplevel)/sessions/session-42/inputs/audios"
ffmpeg -i "dia 42.mp3" -ac 1 -ar 16000 merged.wav
```

(`-ac 1` makes it mono, `-ar 16000` matches Whisper's expected sample rate — both reduce compute without hurting quality. The output is always called `merged.wav` so the next steps work without changes.)

### Step 3 — Transcribe with diarization

Set the speaker count to the **exact number of distinct voices** at the table (DM + N players). Pinning this makes diarization much more accurate.

```bash
cd "$(git rev-parse --show-toplevel)/sessions/session-42/inputs/audios"
VOCAB=$(cat "$(git rev-parse --show-toplevel)/.claude/skills/transcribe/vocab.txt")
SPEAKERS=8   # adjust to your actual count
whisperx merged.wav \
  --model large-v3 \
  --language es \
  --diarize \
  --min_speakers $SPEAKERS \
  --max_speakers $SPEAKERS \
  --hf_token $HF_TOKEN \
  --initial_prompt "$VOCAB" \
  --output_format json \
  --output_dir whisperx
```

You get a single JSON at `sessions/session-42/inputs/audios/whisperx/merged.json` with anonymous labels (`SPEAKER_00`, `SPEAKER_01`, …).

### Step 4 — Convert to a speaker-labeled transcript

[split_merged.py](split_merged.py) walks `merged.json`'s per-word speaker labels and emits one line per contiguous same-speaker run, writing directly to the final `raw/` location:

```bash
cd "$(git rev-parse --show-toplevel)"
mkdir -p sessions/session-42/inputs/transcripts/raw
python3 .claude/skills/transcribe/split_merged.py sessions/session-42/inputs/audios/whisperx/merged.json > sessions/session-42/inputs/transcripts/raw/dia-42.txt
```

Speaker labels stay as raw `SPEAKER_NN` cluster IDs. **Don't try to map them to character names** — per-line attribution is unreliable on merged audio (overlap, short utterances, diarisation flicker), and downstream consumers discard these labels in-context anyway. The value of the Path B output is timestamps + content + decoupled cross-talk, not trustworthy speaker attribution.

### Step 5 — Review

Spot-check the head (`head -50 sessions/session-42/inputs/transcripts/raw/dia-42.txt`) — flag if every line is the same speaker (failed diarisation) or if speaker labels look obviously broken on the first ~50 lines. Transcription ends here once the file looks clean.

---

## Quick decision tree

```
Do you have one audio file per player?
├── Yes  → Path A (multi-track)
└── No   → Path B (merged)

Is this a long campaign session (>3h)?
├── Yes  → Run transcription overnight, not in the foreground
└── No   → Foreground is fine
```

---

## Common pitfalls

- **Whisper invents "*subtítulos por la comunidad de Amara.org*"** — that's the silence-hallucination signature. Make sure VAD is on (`--vad_method silero`) and that you didn't skip the `afftdn` step on noisy tracks.
- **All tracks come out misaligned in the merge.** Per-player tracks need to be sample-aligned at recording time. Craig and OBS handle this; manual recordings often don't. Verify by playing two tracks together — they should sync perfectly.
- **Diarization assigns the DM to two clusters.** Usually means `--max_speakers` was too high. Re-run with the exact count.
- **Fantasy names still come out wrong.** Add them to [vocab.txt](vocab.txt) and re-run — the prompt is the lever.
- **Fireball vs Fire Bolt** — Whisper can't disambiguate them phonetically in Spanish. This is by design; downstream recap tooling handles it via [feedback_transcript_handling.md](../../memory/feedback_transcript_handling.md).
- **Cross-talk on a merged track is lost.** When two people speak at once, diarization picks the louder one. There's no fix — note any missing player lines manually during GM review.

---

## Audio files: storage, restoration, naming

Audio files (`.mp3`, `.flac`, `.m4a`, `.wav`, `.ogg`) are **gitignored by extension** — too large to commit (~100–200 MB each) and would prevent the repo from being publishable. WhisperX `.json` outputs in `whisperx/` are **committed** so the transcript can be regenerated without re-running Whisper.

**Restoring audio on a new machine:**
1. Clone the repo as normal.
2. Download the audio files from cloud storage (Google Drive / Dropbox / wherever the GM keeps the originals).
3. Drop them into the appropriate `sessions/session-<NN>/inputs/audios/` folder, preserving the original filename.

**Filename → session date mapping** is canonical in [`sessions/inputs/calendar.md`](../../../sessions/inputs/calendar.md).

**Naming conventions for the merged-track filename** (the file at the root of `inputs/audios/`):

- **Older style** (sessions 3–~36): `dia <NN>.<ext>` — only the session number. The number tracks the uploader's local count, which **may carry forward earlier numbering errors** and is therefore not a reliable session-ID anchor on its own. Cross-reference against the calendar to map filename → canonical session.
- **Newer style** (recent sessions): `Dia <NN> <YYYY-MM-DD>.<ext>` — session number plus the play date (e.g., `Dia 41 2026-05-01.m4a`). When the date is present, **the date is canonical** and supersedes the number for identification purposes.

Other quirks:
- Format varies by session (mp3 / flac / m4a) — depends on the recorder/uploader's tool at the time. Any audio extension ffmpeg reads is fine.
- Side scenes / interludes get fractional numbers (e.g., `dia 37,5 (interrogatorio de Sinsong).m4a`).
- Capitalization and accents drift (`dia` / `día` / `Dia`) — preserve the upstream filename verbatim, **do not rename** the merged track.

## Output of this skill

```
sessions/session-NN/inputs/audios/   ← raw + intermediate audio
   │  ├── dia NN.<ext>                  merged track (gitignored; Path B input)
   │  ├── tracks/*.ogg                  per-player raw tracks (gitignored; Path A input)
   │  ├── clean/*.wav                   cleaned per-player WAVs (gitignored; Path A, Step 2)
   │  └── whisperx/*.json               per-player transcripts (committed; Path A, Step 3)
   │
   ├── (Path A or B)
   ▼
sessions/session-NN/inputs/transcripts/raw/session-NN.txt   ← speaker-labeled, hallucination-filtered, committed (Path A)
sessions/session-NN/inputs/transcripts/raw/dia-NN.txt       ← merged-track output, committed (Path B; only when no external dia)
   │
   ▼ (canonicalisation step: name canonicalisation + speaker handle conversion)
transcripts/transcript-NN.txt        (canonicalised session — primary witness)
transcripts/transcript-dia-NN.txt    (canonicalised dia, secondary; from external dia or Path B raw)
```

Transcription ends with the two canonicalised files at the bottom. The full recap pipeline (where these files are consumed) is documented in the project root — see [CLAUDE.md](../../../CLAUDE.md) and [sessions/README.md](../../../sessions/README.md).
