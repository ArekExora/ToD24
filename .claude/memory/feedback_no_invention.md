---
name: No invention or extrapolation
description: Never add unverified facts to minutes/gm/triage/saga canon files; flag uncertainty in triage instead. Trace each clause back to its source mechanically — reading the rule is not enough.
type: feedback
---

Never add facts to `minutes-NN.md`, `gm-NN.md`, or `saga-NN.md` that aren't directly traceable to their declared source (transcript / calendar / PC sheet for `/draft` write mode; the same plus the existing drafts during `/draft` audit mode; approved minutes for `/saga`). The file specs and exclusions for canon files are owned by [`/draft`](../skills/draft/SKILL.md), the audit passes that enforce them are documented in the same skill (Pass 1 + Pass 2 + Pass 3 trace-audit subagent), and the saga-side trace by [`/saga`](../skills/saga/drafting-rules.md#minutes-trace-audit) (Minutes-trace audit). This memory carries the campaign-specific reasoning that motivated them.

**Why:** invention has been caught in both directions of the pipeline.
- Drafting side (S1): the *"full HP on level-up"* claim was carried from `source-DRAFT.md`'s trailing `Session-end state` block into `gm-01.md` during finalization (incorrect — the party did not recover full HP); the *"defenders compromised or killed"* inference was added to Knowledge-gained from the cultist-livery observation (extrapolation, not fact). Both required the GM to spot and correct.
- `/saga` (S4): the recap rendered Nesim "handing the pendant to Mialee" when the minutes only have him *showing* it and Mialee *recognizing* the symbol — pendant stayed with Nesim. A retrospective trace audit found ~10 other drift items in the same draft (time-of-day shift, wrong action verb, inverted ordering, "lieutenant" descriptor sourced from NPC-file metadata not the minutes, etc.). All would have been caught by a sentence-by-sentence trace that wasn't part of the original review passes.

The pipeline's contract is that canon files are locked once approved, so unflagged invention becomes uncorrectable canon.

**How to apply:**
- *"It was already in the prior draft"* is not justification for promoting a claim to canon. Verify against the declared source or flag it in triage.
- *Reading the no-invention rule is not enforcement.* Run the explicit trace audit (Pass 1 in `/saga`; Pass 1 in `/draft`'s audit-mode runs) — go clause by clause and name the source line. Anything uncited is invention; rewrite or cut. Treating the rule as a vibes-check is what produced the S4 saga drift.
- Common drift patterns: conflated subjects (one PC's beat collapsed into another's adjacent beat); action substitution (*shows* → *hands over*); inferred causality (bridging cause/effect the source doesn't claim); descriptor leakage (NPC/PC file metadata bleeding in when the source doesn't carry it).
- Stick to facts; let the GM make inferences. If multiple explanations are plausible, state the fact and stop — *Knowledge gained* is for what the party observed or was told, not what could be deduced.
- Mechanical claims (HP recovery, AC, condition removal, resource counts) default to **omitting** unless directly attested by the transcript, calendar, or PC sheet. *"Probably"* and *"presumably"* belong in triage, not in the minutes/gm.
