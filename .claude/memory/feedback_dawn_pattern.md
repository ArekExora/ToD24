---
name: The dawn pattern — gloss-budget violation repeat
description: "Writing 'at dawn' (or any time / date / location rider) when the transcript is silent on that fact is the canonical gloss-budget failure. Committed at least three times — S6 (*at dawn*), S7 (*at dawn* again), and S9 (*Marpenoth-16 captivity*). Treat any time / date / location assertion in the draft as an audit-step trigger that demands a transcript hit on the *exact* fact, not on the surrounding claim."
metadata:
  type: feedback
---

**The pattern:** transcript shows event E happened (e.g., party wakes, prisoner is interrogated). Draft renders E with a rider like *"at dawn"*, *"on Marpenoth-16"*, *"in the watch-cave"*. The cited line supports E. The rider rides through because the citation "covers" the bullet — but the rider is its own factual claim about the state of the world (date / time / place), and the transcript does not anchor it.

**Why:** This is the pipeline's highest-recall hole. Recurrence log:

- **S6 retro** — *at dawn* (time rider).
- **S7 retro** — *at dawn* again, same word, despite the S6 retro logging it. Failed three review passes:
  - Pass 1 was structurally broken — the audit ran in the same conversation as drafting, so the drafter's aesthetic attachment to its own prose survived into the review. Same-context audit catches obvious errors but is structurally blind to the drafter's own glosses.
  - Pass 2 (file-role check) caught other gloss-budget violations in the same draft (*"twelve points of vitality"*, *"the day before"*, unquoted Spanish in narration) but missed this one — same context = same blind spot.
  - Pass 3 (trace-audit subagent) is structurally vulnerable to this class. The subagent checks `[T:N]` resolves and the line supports *the claim*; it does not reliably audit every micro-fact inside the claim. *"wakes at dawn [T:2037]"* passes because *wakes* traces — the *at dawn* rider rides through.
- **S9 audit (2026-05-26)** — *"during his Marpenoth-16 captivity [T:1026-1029]"* in [minutes-09.md:39](../../sessions/session-09/minutes-09.md#L39) beat 2.4 (and mirrored in triage §8.2 and §8.7). The "Marpenoth-16" date is pure invention — T:1026-1029 contains no date at all; the actual captivity was 25–26 Marpenoth per [campaign/timeline.md:14-15](../../campaign/timeline.md). Survived **two** independent `/draft` runs (write mode + audit-mode re-invocation in fresh context), three audit passes each, and two trace-audit subagent invocations. The S9 recurrence is also a *date* rider, not just time-of-day — confirming the class is broader than "time-of-day phrases" (the original S6/S7 framing). Mutual reinforcement across minutes + triage §8.2 + triage §8.7 also hid it from any cross-file check.

**SKILL fix landed (2026-05-26):**

- Pass 1 in [draft/SKILL.md](../skills/draft/SKILL.md) now lists *Dates, times, and locations* as an explicit failure category and extends per-claim trace to triage §8 (so drafter inventions seeded in three places no longer reinforce each other).
- Pass 2 now has a *Date / time / location / atmospheric scan* sub-pass with explicit grep targets (Faerûnian month names, numeric date forms, time-of-day tokens, atmospheric phrases, location proper nouns) — mechanical, not vibes-read.
- GM handoff §4 now scans the minutes prose for historical date / location riders not tied to a §4 anchor, and re-surfaces unsupported riders for GM disposition rather than silent fixes.
- The [trace-audit subagent](../agents/trace-audit.md) prompt now mandates explicit atomic-sub-claim decomposition for any bullet containing a calendar / time / location token, with the dawn pattern cited as the recall hole to guard against.

**How to apply (still load-bearing alongside the SKILL fix):**

- **`/draft` audit-mode runs in a fresh context. No exceptions.** Write-mode `/draft` runs Pass 1+2 in-context as an early-detection layer — useful for typos and format errors, but biased by the drafter's own glosses. The rigorous audit is the audit-mode re-invocation in a new conversation. If the GM intends to bump straight to `accepted` without running audit mode, they are trusting the write-mode self-audit; the dawn pattern is exactly what that trust risks.
- **At draft time, before committing any time-of-day, date, location, weather, or sensory atmospheric phrase, run the gloss-budget test inline on that phrase.** Not at the end. Not in a separate pass. Inline — at the moment of writing. The test: *would removing this phrase leave a factual gap in the established record?* If no, cut. Default to cutting. **And ask: does the citation I'm about to attach actually contain this exact rider?** If not, anchor via `[derived:...]` against the calendar / timeline, or drop.
- **When in doubt, drop the time / date / location / atmospheric phrase.** The recap is rich on purpose, but the richness comes from the in-fiction beats, not from atmospheric embroidery. Cutting an unverified rider is preferable to keeping it under the protection of an adjacent citation.

Related: [[feedback_gloss_budget]] (the underlying test), [[feedback_no_invention]] (the broader rule).
