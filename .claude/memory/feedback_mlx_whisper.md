---
name: MLX-whisper unsuitable for transcription
description: Don't propose mlx-whisper as a speedup for /transcribe; it hallucinates on silence and we've already tested and rejected it
type: feedback
---

Do not propose `mlx-whisper` (Apple Silicon GPU acceleration) as a speedup option for the `/transcribe` skill, even though it would be ~10× faster than CPU WhisperX.

**Why:** `mlx-whisper` has no built-in VAD. WhisperX's value isn't just the whisper model — it's that pyannote/silero VAD pre-segments the audio so silence never reaches the decoder. On long D&D sessions (every session has long silent stretches: idle chat, dice rolls, GM thinking), raw whisper falls into hallucination loops where it decodes silence as a repeated token. Tested 2026-05-08 on session 4's DM track: mlx-whisper transcribed ~40 continuous minutes as just "y, y, y, y..." Output was unusable. Anti-hallucination flags (`--condition-on-previous-text False`, `--no-speech-threshold 0.8`, `--logprob-threshold -0.5`) reduce but don't fix the problem.

**How to apply:** If the GM brings up speed of `/transcribe`, point to this memory rather than re-investigating. The architectural fix (hybrid pyannote-VAD + mlx-whisper) is real engineering work — only worth proposing if the GM explicitly wants to invest in it. For one-off speed needs, suggest renting a short-lived CUDA VM and running stock WhisperX with `--compute_type float16` instead.
