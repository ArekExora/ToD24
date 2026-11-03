---
name: Transcript handling — STT artifacts, not player fault
description: When transcripts show ambiguous content, suspect STT garble first; don't blame player shorthand or imprecision.
type: feedback
---

When the transcript shows something mechanically suspect (a spell the caster shouldn't have, a name that varies between lines, a beat that contradicts itself), default to **STT artifact**, not player error.

**Why:** the STT engine has significant artifacts on Spanish-language audio. *"Fireball"* and *"Fire Bolt"* sound near-identical in Spanish pronunciation — players at the table sometimes have to ask each other to clarify. Misattributing STT errors to "player shorthand at the table" insults the players and frames the wrong problem.

**How to apply:**
- In triage and review-pass language, attribute mechanical/spell ambiguities to STT, not to the player.
- Cross-check spell names against the caster's actual spell list and current level before committing them.
- Flag near-homophones (Fireball/Fire Bolt, etc.) as candidates for transcription error even when the transcript looks unambiguous.
- Do not write text that implies the player was unclear or imprecise.
