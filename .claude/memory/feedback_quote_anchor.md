---
name: feedback-quote-anchor-paraphrase
description: When producing a derived artifact that paraphrases from a source document, quote the supporting span verbatim in a scratchpad before writing the paraphrase; if a token in the draft doesn't trace to the quote, it's invented.
metadata:
  type: feedback
---

When producing a derived artifact that paraphrases from a source document (minutes → timeline / gm / saga, transcript → minutes, spec → code), **quote the supporting span verbatim in a scratchpad before writing the paraphrase**. Each key noun / action-verb / named entity in the draft must trace to a word or phrase inside the quoted span. If a token doesn't trace, it's invented — cut, re-anchor, or rewrite.

**Why:** two drift patterns observed in `/timeline` generation on 2026-11-14 (S01 and S12 runs):

- *Memory drift* — reading source once at planning time and writing events later from internal summary produced *"killed by giant-spider venom"* in the draft where `minutes-01.md` said *"spider swarm boils over him in a rush — fangs and venom finding every gap"*. The drafter had the right scene.beat pointer (6.10) but substituted the wrong agent of death (giant spider for swarm).
- *Level-of-description substitution* — picking a plausible high-level paraphrase (*"infiltrate the cult for the alliance"*) instead of the specific task Ontharr named in `minutes-12.md` (*"trace the caravan to Baldur's Gate"* / *"trying to trace the destination"*). The general plot direction swapped in for the specific mission wording.

A bare scene.beat pointer catches neither — the pointer can be right while the words still drift.

**How to apply:**

- Baked into [.claude/skills/timeline/SKILL.md](.claude/skills/timeline/SKILL.md)'s *Writing each event — quote-anchor first* section, mandatory before each event is written; self-verification rule 1 enforces the trace check.
- **Generalisable beyond `/timeline`.** Any paraphrase-from-source workflow benefits from the same discipline. When writing or updating a skill that derives one artifact from another, propose or include a quote-anchor step. When the user flags a factual error in a derived artifact, the fix is usually a write-time quote-anchor step, not a "be more careful" exhortation.
- The scratchpad is throwaway (internal), but showing it to the user when they ask for verification is a trust-builder — makes the discipline visible rather than hidden. The S2–S5 `/timeline` run demonstrated this: user had called out factual errors in the S01 and S12 runs, the quote-anchor fix was documented in SKILL.md, then the next four files landed with one minor bolding tweak and the user said *"I'm VERY PROUD of you, good work"*.

Related: [[feedback_no_invention]], [[feedback_gloss_budget]], [[feedback_dawn_pattern]], [[feedback_egg_pattern]].
