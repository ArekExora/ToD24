---
name: The egg pattern — action declaration cited as outcome
description: "Citing a player's action declaration (or the GM's acknowledgment of that intent) as if it were evidence the action succeeded. The drafter takes 'I attack the egg' + GM 'yes, you want to give a blow that bursts it' as proof the egg broke; the actual outcome is a separate transcript moment (or visual/implicit) that must be cited independently. Committed in S9 — the third dragon egg, cited to T:3933 (GM acknowledging Mialee's intent), claimed as 'cracks the egg open with a sharp blow' in minutes / saga / GM file, propagated through three audit passes and delivered to players before being caught in S10 drafting."
metadata:
  type: feedback
---

**The pattern:** transcript shows the player declaring an action ("I attack X / I break Y") and the GM acknowledging the *attempt* ("yes, you want to give a blow that bursts it, sí"). The drafter cites the GM's acknowledgment line and writes the bullet in outcome language ("cracks the egg open"). The cited line technically backs *the attempt* — but the **outcome** is a different transcript moment (or visual / implicit at the table) that was never cited. Audit reads the citation, sees it locally supports the verb, and passes.

This is **not** a GM retraction. The GM said exactly what they said; the drafter mistook acknowledgment-of-intent for description-of-outcome. The transcript distinguishes three role-types around any action:

- **(D) Player declaration** — "I attack the egg", "I want to break it"
- **(A) GM acknowledgment of intent** — "yes, you swing", "y me quieres dar un golpe que lo revienta, sí" (confirming the attempt is happening, not the result)
- **(O) GM outcome description** — "the shell holds", "the strike kills", "el huevo no se ha roto"

A bullet using outcome language must rest on (O), not (D) or (A).

**Why:** Recurrence log so far:

- **S9 egg-break (2026-05-28 caught)** — Mialee declared an egg-strike at T:3932-3934; GM acknowledged the *attempt* at T:3933 (*"me quieres dar un golpe que lo revienta, sí"*). The GM's later **outcome** description at T:4317 (*"no se ha roto, porque ninguno de ellos se ha roto porque se cuezan"*) was never cited. The minutes wrote *"cracks the egg open with a sharp blow [T:3933]"*; the saga and gm-file inherited the claim ("hatchery destroyed", "all eggs destroyed"). All three artifacts survived `/draft` audit passes 1+2+3 and were delivered to players. Caught only when S10 drafting flagged a continuity contradiction (S10 transcript shows the party returning to finish off the still-living dragonling). User had to walk back delivered S9 outputs.

**Why the audit missed it:** Pass 1 looks for unverified claims (this one had a citation). Pass 2 token-checks the claim against the cited line (T:3933 contains *golpe* and *revienta* — looks like a match). Pass 3 (trace-audit subagent) verifies that the citation supports the bullet — and at the role-undifferentiated level it does: T:3933 *does* contain "blow that bursts it". None of the passes decompose the cited line by role-type (D / A / O) and verify the bullet's verb against an (O) line.

**Important caveat:** outcomes are often **visual or implicit at the table** — the GM moves a token, points at a map, or nods — and no transcript line describes the result. In those cases there is no (O) line to cite, and the bullet must use **attempt-language** ("strikes at", "swings at", "tries to break") instead of outcome-language ("cracks", "kills", "destroys"), **or** the outcome must be flagged to GM at handoff for explicit confirmation. The fix is not "always find an (O) line"; it is "if the verb claims an outcome, either cite an (O) line or downshift to attempt-language or flag for GM".

**Important downstream constraint:** `/gm` and `/saga` consume accepted minutes only — they do not re-read the transcript. So integrity must be locked in at `/draft` audit time. There is no second chance downstream.

**Proposed SKILL fix (pending GM sign-off):**

- Pass 1 in [draft/SKILL.md](../skills/draft/SKILL.md) gains a *Declaration vs. outcome separation* category. For every bullet with an outcome verb (cracks / breaks / kills / destroys / opens / captures / wounds / drops / etc.), the auditor classifies each cited line as (D), (A), or (O), and verifies at least one (O) line in the citation range. If only (D) and (A) lines exist and no (O) line is findable elsewhere in the transcript: re-word to attempt-language, **or** flag for GM at handoff.
- The trace-audit subagent decomposes outcome-verb bullets by role-type during per-citation verification — not just "citation supports claim", but "(O) line for outcome verbs must exist among citations".
- The category is named in the SKILL alongside *Dates, times, and locations* (the dawn pattern) so it is a structural check, not vibes.

**How to apply (at draft time):**

- When writing an outcome-verb bullet, **identify the GM's outcome line** (the (O) moment) before committing the verb. If you find only (D) and (A) lines in the relevant transcript range — and no (O) line further along — your verb is wrong. Downshift to attempt-language ("strikes at", "tries to break") or flag for GM.
- Treat *"yes, you want to do X"* and *"and you swing"* and *"y me quieres dar un golpe que lo revienta, sí"* as evidence the action is **being attempted**, not that it succeeded. The egg-pattern is the canonical failure case.
- For consequential outcomes (death, destruction, key item state changes), the (O) line is non-negotiable — implicit/visual outcomes for these must be GM-confirmed at handoff, not assumed.

Related: [[feedback_no_invention]] (the broader rule), [[feedback_dawn_pattern]] (the structural sibling — both classes ride through audit passes on citations that locally appear to cover the claim), [[feedback_gloss_budget]].
