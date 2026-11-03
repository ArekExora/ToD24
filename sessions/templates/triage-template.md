<!--
triage-NN.md — Production artifacts (working)

PURPOSE
  Disposable workspace for items the GM must verify, decide, or address.
  NOT canon. Archived (resolved items marked [x]) — the file is its own audit trail.

FILE-LEVEL CONVENTIONS

  FORMAT — sectioned numbered markdown checklist. Sections explicitly
  numbered (## 1. STT canonicalizations, ## 2. Mechanical / rules flags, …);
  items numbered 1., 2., … restarting in each section. Addressable as
  <section>.<item> (e.g. "2.4 needs fixing").

  SECTION ORDER — canonical numerical order (1 → 9), regardless of
  priority distribution. Sections 1–8 are populated by /draft (write mode
  seeds the initial set; audit mode walks them as part of the GM
  handoff); §9 is appended by /draft's trace-audit subagent.

  EMPTY SECTIONS — render the literal phrase "None this session." under
  the section header (plain text, no bold, no italic). Do NOT omit any
  section.

  CITATION RULE — items requiring transcript verification cite the
  transcript line(s) using the same form as the minutes: [T:N], [T:N-M]
  for spans, [Td:N] for dia track.

PRIORITY TAXONOMY — bold prefix immediately after the checkbox:
  - [P0] blocks-recap : resolve before minutes ships to the GM (e.g.
    canonicalisation affecting drafted quotes, rules flag changing a
    scene's outcome).
  - [P1] blocks-saga : resolve before /saga runs (date/continuity
    confirmations, derived-beat confirmations).
  - [P2] post-publication : campaign/* file edits after the recap
    (timeline.md, NPC sheets, faction docs, location sheets, calendar).
  - [P3] informational : already resolved or audit trail (closed STT
    garbles, completed Spanish dispositions, no-discrepancy audits).

  Items within a section sort P0 → P1 → P2 → P3. Section position itself
  is canonical (by section number), never reordered by item priorities.

EXCLUDED
  - Anything canonical (events, NPCs introduced, knowledge gained) — those
    go in minutes / gm.
  - AI rumination or audit notes ("I considered X but went with Y").
  - Items already verified — triage is uncertainty, not certainty.
  - STT garbles that don't matter to canon (background dialogue, table
    joking) — cut entirely.

BOUNDARY RULE
  AI uncertain → triage; AI certain → minutes. Unverified beats become
  triage questions, never hedged minutes prose.
-->

<!--
SECTION 1 — STT canonicalizations

Name/term variants observed during drafting and the canonical form chosen.
Default P3 (informational log); promote to P0 only when a canonicalisation
changes a quote already in minutes or affects a name propagating to NPC
sheets.
-->
## 1. STT canonicalizations

1. - [ ] **[P3]** "Verdusque", "Verdusk", "Berduzca" → Berdusk
2. - [ ] **[P3]** "Talbot", "Tarval", "Tarpau" → Tarbaw Nighthill

<!--
SECTION 2 — Mechanical / rules flags

Spells, features, feats, or class abilities used inconsistently with the
rules or the PC's sheet.

Each entry MUST include TWO citations:
  1. Transcript line ([T:N]).
  2. PC digest citation — `campaign/pcs/_context.md` line range(s)
     checked (e.g. `_context.md:142-189` for Nyx's Spells / Feats blocks).

The digest citation is mandatory — a flag without it is incomplete and must
NOT be surfaced.

DO NOT FLAG when the ability appears anywhere in the digest block.
-->
## 2. Mechanical / rules flags

1. - [ ] **[P0]** Nyx casts "Fireball" [T:717]. Checked `_context.md:574-631`. Fireball absent from every block. Likely STT mishear of Fire Bolt or Faerie Fire — confirm intended spell.

<!--
SECTION 3 — Unclear / garbled passages

Sections unreadable across all transcript files. Cite the line range.
-->
## 3. Unclear / garbled passages

1. - [ ] **[P1]** [T:993-1047] garbled exchange between Tompu and Atzi about "Coatl". STT loops "Y ya está".

<!--
SECTION 4 — Date / continuity references

EVERY date/time reference (real-world or in-fiction) observed in the
transcript lands here — whether the AI used it for the minutes
(frontmatter, scene headers, derived anchors) OR not. Each item: the
GM's (or player's) words verbatim, the [T:N] citation, and a brief note
on how the anchor was used (or "not used — kept for continuity").

Includes:
  - Real-world date / start / end time (frontmatter `date`).
  - In-fiction date / time span (frontmatter `in_fiction_date`), including
    date roll-overs.
  - Per-scene `_~HH:MM, …_` date-line values — derived anchors MUST SHOW
    THE CALCULATION (e.g. "midnight + 8h long rest → 08:00 wake").
  - In-passing time references not used in the minutes (the GM may want
    them for future continuity).
  - Calendar conflicts and date-related contradictions with prior-session
    canon.
-->
## 4. Date / continuity references

1. - [ ] **[P1]** **In-fiction date roll-over** (frontmatter `in_fiction_date`). Session opens ~18:00 of 23 Marpenoth 1489 DR; long rest crosses midnight; ends ~15:30 of 24 Marpenoth. Frontmatter carries the range.
2. - [ ] **[P1]** **Scene 3 midnight anchor.** GM [T:1094]: *"Son las doce."* — used as scene 3 header.
3. - [ ] **[P1]** **Long rest duration anchor.** GM [T:1121]: *"Hacedme un descanso largo y avanzamos 8 horas."* — combined with the midnight anchor above to derive scene 4's *"~08:00, 24 Marpenoth"*.
4. - [ ] **[P1]** **Post-fight anchor.** GM [T:3251]: *"son las 10 de la mañana, habéis pasado el día, sería un poco más tarde, serían las 11 de la mañana."* — self-corrects to 11:00; back-calculated to put scene 7's debate-and-deer at ~10:00.
5. - [ ] **[P1]** **Greenest arrival time.** GM [T:3296]: *"aproximadamente las tres y media"* — used as scene 11 end / frontmatter end.
6. - [ ] **[P2]** **Calendar conflict.** `sessions/inputs/calendar.md` S5 row says **23 Marpenoth**; actual span is **23 Marpenoth ~18:00 → 24 Marpenoth ~15:30**. Apply on calendar.
7. - [ ] **[P3]** **Session start time at the table.** Per `calendar.md` the session was scheduled at 17:00; transcript runs 03:39 of recorded audio. No end-time recorded — frontmatter currently carries only the start time.

<!--
SECTION 5 — Prior-session audit

Factual discrepancies between the players' opening table-recap and N-1
canon (minutes-<N-1>.md / gm-<N-1>.md).

OPENING SEGMENT — from the first in-session line until the GM starts the
session's opener (first scene-setting, first in-character NPC line, or
first call for player action).

BAR — contradictions and material omissions only. Compression, paraphrase,
simplification, reordering are NOT discrepancies.

DIMENSIONS — NPC identities/roles, locations, outcomes, missions &
rewards, items, knowledge claimed. Each item: what players said vs what
N-1 says, with [T:N] citation and the N-1 scene.beat or gm-table row when
applicable.
-->
## 5. Prior-session audit

1. - [ ] **[P1]** Players said the wounded brother was sent to Candlekeep [T:12]; N-1 minutes 4.3 says Berdusk. Amend N-1, or close as misremembered?
2. - [ ] **[P3]** Players omitted the courtyard-well grapple entirely [T:18]; N-1 minutes 6.5 (an EPIC-tagged beat). Likely compression — confirm close.

<!--
SECTION 6 — Verbatim Spanish dispositions

One item per Spanish quote in the minutes draft. Each item: minutes
scene.beat, quoted text, [T:N] citation, proposed disposition.

THREE DISPOSITIONS:
  - keep — leave verbatim in the minutes (short signature lines).
  - translate — render meaning in English narration; drop the verbatim.
  - drop — paraphrase or remove entirely.

Default: keep for short character-defining lines; translate for longer
or expository dialogue; drop for incidental remarks.

Populate one item per Spanish quote in the minutes, including ones already
decided to translate or drop, so the GM can override.
-->
## 6. Verbatim Spanish dispositions

1. - [ ] **[P1]** 2.9 — "¿Quién era el dragonclaw a cargo de vuestra operación?" [T:1040]. Proposed: translate.
2. - [ ] **[P1]** 5.3 — "Me dejé capturar. Necesitaba infiltrarme." [T:1356]. Proposed: translate.
3. - [ ] **[P1]** 9.6 — "Somos legión. Somos más de los que podréis jamás derrotar..." [T:3109-3113]. Proposed: keep.
4. - [ ] **[P1]** 9.7 — "La gloria de Tiamat." [T:3144]. Proposed: translate.

<!--
SECTION 7 — Derived beats

One item per minutes claim citing [derived:T:N1+T:N2+...]. Each item: the
minutes <scene>.<beat>, verbatim claim, constituent transcript citations,
one-line synthesis description. Distinct from section 4 (date/time
derived anchors).

MANDATORY 1:1 with minutes [derived:...] citations. A flat span ([T:N-M])
on a synthesised claim hides the synthesis — fix the minutes citation
before shipping. Default P1 — GM must confirm.
-->
## 7. Derived beats

1. - [ ] **[P1]** 4.7 — "The cult leaders left ahead of the rank-and-file, mounted; the rest moved out with the heavy loads on foot." Sources: [T:1140] (leaders' tent stripped), [T:1162] (four mounted hunters riding east), [T:1188] (foot tracks west with heavy loads). Synthesis: leaders mounted ahead, rank-and-file on foot behind. Confirm?

<!--
SECTION 8 — File updates needed

Downstream checklist for campaign/* canon files. Populated by /draft in
write mode (initial seed) and walked by /draft in audit mode as part of
the GM handoff (NPC file confirmations populate the NPC entries; the GM
confirms each item and the canon update is applied during the same audit-
mode run).

INCLUSION FILTER — items must clear the File updates inclusion rules in
.claude/skills/draft/SKILL.md before being seeded (write mode) or
presented to the GM (audit mode). Hospitality, one-off flavour,
expository colour, ephemeral PC state (HP / consumables / hours-duration
effects) do NOT belong here — they already live in the minutes. Audit-
mode auto-closes clear exclude-test failures as
`[x] not sheet-worthy — <rule>` so the GM sees the closure, not another
decision request.

CREATE-IF-MISSING — campaign/* canon files are populated through the recap
workflow, not pre-created. Faction files are flat at campaign/factions/;
subfactions are siblings (<parent>-<subfaction>.md). Default P2 —
post-publication.
-->
## 8. File updates needed

1. - [ ] **[P2]** PC `Current state`: Mialee — Honor +1 (keep defence); Eguzkilore — gained the *Tankard of Sobriety* (magic item).
2. - [ ] **[P2]** `campaign/timeline.md` — append session entry (create if missing)
3. - [ ] **[P2]** NPC files: create Miguel, Leosin Erlanthar
4. - [ ] **[P2]** Location files: create Berdusk, Candlekeep, southern defile
5. - [ ] **[P2]** Faction: `campaign/factions/cult-of-the-dragon.md` — append ideology + alert state (create if missing)
6. - [ ] **[P2]** `sessions/inputs/calendar.md` — correct date / mapping if needed

<!--
SECTION 9 — Trace audit (APPENDED BY /draft'S TRACE-AUDIT SUBAGENT)

The trace-audit subagent invoked by /draft's Pass 3 walks every minutes
bullet, resolves citations against the named transcript file, runs the
per-file chronology check, and appends this section with one P1 item per
finding. See .claude/agents/trace-audit.md for the subagent's contract.

When the audit is clean, the section body is the literal line "Clean —
every bullet's citation resolves and supports its claim; no chronology
decreases." instead of a numbered list.
-->
## 9. Trace audit

1. - [ ] **[P1]** [scene 3.5] missing-citation — bullet has no citation tag.
2. - [ ] **[P1]** [scene 5.7] chronology decrease — citation [T:1820] decreases from previous [T:1855] in scene 5; `?ord` applied. Verify placement.

