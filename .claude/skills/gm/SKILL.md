---
name: gm
description: Generate the GM event log (`gm-<NN>.md`) — a structural digest of GM-accepted `minutes-<NN>.md`. Mechanical pass with one narrow GM ask (hidden-NPC labeling) when hidden NPCs were active; every gm entry traces back to a minutes scene, an EPIC-tagged beat, or a hidden-NPC misattribution beat in minutes.
---

# /gm

**Generates** `gm-<NN>.md` — the canonical GM event log — by digesting GM-accepted `minutes-<NN>.md`. The gm file is a **structural digest** of minutes, not a parallel narrative. No transcript reads; no invention. One narrow GM ask collects the hidden-NPC labeling when hidden NPCs were active.

## Output

`sessions/session-<NN>/gm-<NN>.md` — canon, archived after GM sign-off.

## Required inputs (ask if missing)

- **Session number** (NN).
- `sessions/session-<NN>/minutes-<NN>.md` — must carry `status: accepted` in its frontmatter. **If the file does not exist, or the `status` field is missing / not `accepted`, surface a clear error and stop.**

## If `gm-<NN>.md` already exists

Switch to **audit mode**, never overwrite. Any existing `gm-<NN>.md` has almost certainly been GM-edited after the initial generation, and those edits are canon.

In audit mode:

1. Read the existing file.
2. Walk the same *Before writing* inputs and run the *Internal self-verification* checks against the existing file.
3. **Skip the hidden-NPC handoff** — in audit mode, the §10 *Secrets* entries already exist and `/gm` verifies them mechanically (does each entry point at a real minutes scene.beat?) rather than re-collecting them from the GM.
4. Surface a numbered finding for each rule violation, missing entry, stale content, or material gap between what `/gm` would write and what's actually there. Each finding names the section, what differs, and what the template / rules expect.
5. Stop and hand the list to the GM. Iterate per-finding — the GM decides which to address; `/gm` does not auto-edit in audit mode.

## Before writing

1. **Read accepted minutes end-to-end.** Note: scene structure and titles (`## N - <Title>`), `[EPIC]` tags, NPCs named in beats, time anchors.
2. **Read minutes frontmatter** for metadata copy (real-world date, in-fiction date, party present, locations).
3. **Read `sessions/session-<N-1>/gm-<N-1>.md`** (if N > 1) — needed for **Missions & rewards** carry-forward (see template *Missions & rewards*). No other carry-forward — gm sections are session-scoped.
4. **Do not read the transcript. Do not read triage.**

## Hidden-NPC handoff

Once the inputs are loaded, read `campaign/npcs/_context.md` (the digest) and identify any NPC with `status: hidden`. **If any qualify**, scan the accepted minutes for beats whose visible effect matches each hidden NPC's role or class, and surface them as suggestions:

> *"Hidden NPCs potentially active this session: \<names\>.*
>
> *Based on their class / subclass / factions, candidate beats:*
> *- \<scene.beat\> — "\<short minutes paraphrase\>" — possibly \<NPC name\> (matches \<class / subclass / faction role\>).*
>
> *Confirm, reject, or add others. For each accepted beat, name the visible tell (the misattribution the players saw)."*

**How to scan.** Use the hidden NPC's frontmatter alone — `class`, `subclass`, `background`, `factions` — to infer the kinds of visible effects they would plausibly produce at the table. A Life Domain Cleric matches a downed PC *"comes around at 1 HP"* with no PC heal cited; a Warrior-of-the-Open-Hand Monk matches a sudden incapacitating strike from somewhere behind an enemy line; a Harpers-aligned agent matches a faction-coded tell the visible party isn't responsible for. No digest body is needed — the frontmatter is sufficient for the match heuristic.

Hidden-NPC actions are already in the minutes as in-fiction prose — the GM narrated them at the table, players witnessed the visible effect, and `/draft` rendered them as ordinary transcript-derived beats. This step indexes which existing beats correspond to which hidden NPC so the §10 *Secrets* section can be populated.

If no hidden NPCs qualify (none exist, or the GM confirms none were active this session), skip this step.

Offstage NPC and faction/world events are **not** collected here — those are GM-authored and the GM adds them directly to `gm-<NN>.md` after this skill writes the file. The audit mode treats their absence-or-presence as a GM decision, not a verification finding.

## File structure

The authoritative schema lives in [`sessions/templates/gm-template.md`](../../../sessions/templates/gm-template.md) — a commented skeleton with file-level conventions, file-level exclusions, per-section rules for all ten sections, and boundary rules. Read it before drafting; the schema has a single source of truth so producers and verifiers stay aligned.

## Internal self-verification (run before write)

Mechanical checks. If any fails, fix the entry or surface as a clear error — do not write a file with known violations.

1. **Every Events bullet traces to a minutes scene, ONE sentence each, 6–10 total.** Each `## 4. Events` line must correspond to a scene or scene-fragment in minutes (if you can't point to the source scene, the bullet is invented — cut it); each bullet is ONE tight sentence — em-dash, comma, semicolon, "and" all fine for joining sub-clauses; the bound is the sentence count, so no `. ` chaining two complete sentences (that's the minutes' job); total bullet count is 6–10 (collapse round-by-round beats into encounter-level outcomes; merge non-distinct scenes; move reward terms to §6, items to §8, fallback contacts to §5/§9 per the template).
2. **Epic moments is exactly the `[EPIC]`-tagged subset of minutes.** Walk minutes for `[EPIC]` tags; gm § Epic moments must list precisely those beats as `[<scene>.<beat>](minutes-<NN>.md#<scene>--<slug>)` links. No additions, no omissions. **Bold the primary actor's name(s)** (PC or NPC) in each description per the template's *Name emphasis* rule — single actor (`**Nyx** threads…` / `**Langdedrosa Cyanwrath's** return…`), multiple actors (`**Nuberroca** and **Eguzkilore** hold…`), incidental targets/witnesses left plain, group / unnamed actor (no bold).
3. **Hidden NPC entries reference a minutes beat.** Each hidden NPC action in §10 *Secrets* points at the scene.beat where its in-fiction misattribution lives in minutes; verify the coordinate exists and matches what the GM identified during the hidden-NPC handoff. Offstage NPC and faction/world entries are GM-authored (not in minutes) and carry no reference — they are not mechanically verifiable.
4. **All ten sections present.** The template lists them and defines the empty-state rendering (`None this session.`); this check is just that none was skipped.
5. **No transcript-level claims.** Scan for HP/AC numbers, roll totals, spell-slot levels — all forbidden by the template's file-level exclusions. If present, you read or remembered the transcript when you shouldn't have; cut.
6. **Missions & rewards carry-forward intact.** Walk `gm-<N-1>.md` *Missions & rewards* (if N > 1); every `Open` row appears in this session's *Missions & rewards*, renumbered as needed, with the Notes cell updated per the template's *Missions & rewards* Notes rule (live state).
7. **NPC link targets exist.** Each NPC referenced in §5 must have a file at `campaign/npcs/<stem>.md` (or be in the process of being created — flag in self-output if missing).
8. **NPC entries respect the word budgets.** First appearance: a 3–5 word identity descriptor *and* a 3–10 word action fragment ("**Miguel** — wounded keep guard. Recruited as guide."). Recurring appearance: action fragment alone, 3–10 words ("**Tarbaw Nighthill** — assigns the recon mission."). Anything longer is doing the minutes' job — trim. Stat-block details, species/class/spells, backstory: do not appear; the NPC link sends the GM there.

Print a one-line status (file written + count of Epic moments + count of Secrets) and stop.

## Reference

- **Schema:** [`sessions/templates/gm-template.md`](../../../sessions/templates/gm-template.md).
- Memory: [feedback_gloss_budget.md](../../memory/feedback_gloss_budget.md), [feedback_no_invention.md](../../memory/feedback_no_invention.md).
