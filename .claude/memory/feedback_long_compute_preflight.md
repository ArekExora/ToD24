---
name: Pre-flight verification before long unrecoverable compute
description: Before emitting any command that triggers >30min compute with external auth/network dependencies, print a pre-flight verification block (curl, env-var check, etc.) so failures surface in seconds, not hours.
type: feedback
---

For any printed command that triggers long, unrecoverable compute *and* depends on external auth, gating, or network resources, emit a pre-flight verification block before the long command. Failures should be detectable in seconds, not after hours of wasted compute.

**Why:** On 2026-05-09 the GM lost ~3h of compute on session-44 Path B WhisperX due to two stacked HuggingFace auth gotchas — first a missing model gating acceptance, then a fine-grained token without gated-repo read permission. WhisperX writes its JSON only after all stages complete, so each failure invalidated the entire transcription+alignment run. A 1-line `curl` against the gated config.yaml would have caught both before launch.

**How to apply:**
- Long-compute, unrecoverable, external-dep skills: `/transcribe` Path B (WhisperX diarization), and any future skill that hits gated HF repos, paid APIs, or hours-long jobs.
- Verification should test the actual failing path (e.g., `curl` the gated resource the long command will request), not just check that env vars are non-empty.
- Two specific HF auth traps to remember:
  1. Fine-grained tokens need an explicit "Read access to contents of all public gated repos you can access" permission — accepting model gating is necessary but not sufficient.
  2. Don't pass tokens via CLI args (`--hf_token $HF_TOKEN`); they leak via `ps aux`. Rely on env-var fallback (`HF_TOKEN`) or stored credentials (`huggingface-cli login`).
- Document expected harmless warnings (e.g., WhisperX's "No --hf_token provided…") inline so future-me doesn't second-guess and re-add the leaky flag.
