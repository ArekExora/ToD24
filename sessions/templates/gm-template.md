<!--
gm-NN.md — GM event log

PURPOSE
  Canonical record of world-state deltas. The GM re-reads in ~60 seconds before next session.
  Structural digest of the accepted minutes — NOT a parallel narrative.

FILE-LEVEL CONVENTIONS
  - Language: English.
  - Numbered lists throughout. Each section restarts numbering at 1.
  - Sections explicitly numbered (## 1. Summary, ## 2. Metadata, …); items
    addressed as <section>.<item> (e.g. "4.3 needs fixing").
  - No gloss. No atmospheric prose, no narrative flavour, no scene-setting,
    no re-narration of beats already in the minutes. If a sentence neither
    changes the world nor summarises a minutes beat into a quick-glance form,
    cut it. Tighter than minutes; tighter than saga. See
    .claude/memory/feedback_gloss_budget.md.
  - EMPTY SECTIONS render the literal phrase "None this session." under the
    section header — plain text, no bold, no italic. Do NOT omit any section.
    Sections 1, 2, 4 (Summary, Metadata, Events) are always populated by
    construction; the rule applies to any section that may end up with no
    content for this session. For sections rendered as a table (§6), the
    phrase replaces the table entirely (no header row, no empty body).

FILE-LEVEL EXCLUSIONS (must NOT appear anywhere in the file)
  - HP, AC, DC, save numbers, attack rolls, damage rolls.
  - Spell slot levels, spell save DCs, turn-by-turn combat.
  - Per-PC mechanical roll-call ("Mialee used a potion, Sinsong used a 1st-level slot")
    — state-update artifact, lives in triage.
  - Inline color, exact dialogue, narrative phrasing.
  - STT canonicalization notes, garbled-passage flags, "confirm with GM" hedging
    — all triage concerns, already closed by the time /gm runs.

EXCEPTION — critical rolls and blunders: include a crit/fumble in Events when the
  *outcome* is itself a notable canon delta (crit-killing a named foe, critical
  lockpick, fumbled stealth triggering the ambush). Crit-killing one of many
  kobolds → out.

BOUNDARY RULES for ambiguous cases:
  - Combat OUTCOMES only, not combat PROCESS. "Killed 3 cultists, captured 1 alive"
    → in. "Nuberroca crit on first attack" → minutes only.
  - Mechanical detail when it IS canon stays. "Party reached level 3" → in.
    "Mialee took 6 damage from rocks" → out. "Mialee enters next session under
    a curse Greater Restoration can't dispel" → in (carries forward).
-->

# Session NN — GM event log

<!--
SECTION 1 — Summary

2–5 items, one per notable beat of the session. Each item is one tight clause
(typically 3–10 words): a **bold key phrase** followed by a brief context fragment.
Bulleted events, not a paragraph; not a re-narration. If a reader could mistake
the section for a mini-recap, it's too long. Address as 1.<item>.
-->
## 1. Summary

1. **<bold key phrase>** — <short context fragment>.
2. **<bold key phrase>** — <short context fragment>.
3. **<bold key phrase>** — <short context fragment>.

<!--
SECTION 2 — Metadata

Numbered items, copied verbatim from minutes frontmatter (the frontmatter is
canonical for session metadata).

  - Real-world date: YYYY-MM-DD, with start and end times appended when known
    (e.g. "2025-02-09, 17:00 – 19:00"). Use start time alone when end unknown.
    Plain date alone if no times known.
  - In-fiction date: range with start and end including times when known.
    When the day rolls over within the same year, do NOT repeat the year and
    "DR" on the end side — just the day and month (e.g.
    "22 Marpenoth 1489 DR, ~22:00 → 23 Marpenoth, ~02:00"). Repeat the year
    only when the range crosses into a new year. Single timestamp if the
    session covers <1 in-fiction day (e.g. "23 Marpenoth 1489 DR, ~02:00 →
    ~14:00").
  - Locations: chronologically ordered list of locations visited during the session.
    Include the top-level umbrella location (e.g. [Greenest]) ONLY when the party
    operated across the broader location — typically when scenes move between
    sub-locations. Skip the umbrella when scenes never leave a single sub-location.
  - Party present: only PCs who were both in-fiction-active AND handled by their
    player, listed alphabetically. Skip PCs the GM was puppeting (absent player,
    off-staged in-fiction). Those appear in other sections (Secrets,
    Status changes) as needed.
  - Party absent: the active visible roster minus Party present, comma-separated
    and alphabetical. SCOPE: only PCs whose joined_at <= NN AND status != hidden.
    Use the literal "none" when everyone on the visible roster played.
-->
## 2. Metadata

1. **Real-world date:** YYYY-MM-DD[, HH:MM – HH:MM]
2. **In-fiction date:** DD <Month> YYYY DR[, HH:MM → DD <Month>, HH:MM]
3. **Locations:**
   1. [<Location name>](../../campaign/locations/<location>.md)
4. **Party present:** <Alice>, <Bob>, <Charlie>
5. **Party absent:** none

<!--
SECTION 3 — Epic moments

Peak heroic / dramatic / unforgettable beats, indexed for cross-session lookup.
EXACTLY the subset of minutes beats carrying the [EPIC] tag. The gm § Epic
moments list mirrors what's tagged in the accepted minutes — do NOT introduce
new candidates here; if a beat isn't [EPIC]-tagged in minutes, it does not
appear in this section.

Each entry: scene.beat coordinate rendered as a markdown link to the minutes
scene's anchor — [<scene>.<beat>](minutes-<NN>.md#<scene>--<slug>) — plus a
one-line short description matching the tagged beat in the minutes.

NAME EMPHASIS — bold the name(s) of the character(s) performing the epic deed
in the description. PCs and NPCs alike, as long as they are the *primary actor*
of the beat. This is the only styling §3 uses; it makes the actor scannable at
a glance and propagates verbatim into the player-shareable Homebrewery render
(where the scene.beat link wrapper is stripped, leaving the bolded name as the
entry's visual anchor).

  - Single actor: **<name>** <verb phrase>… (e.g. "**Nyx** threads a longbow
    shot into one of the dragon's eyes." / "**Langdedrosa Cyanwrath's**
    return, calling out Nuberroca…").
  - Multiple actors: bold each name in the same beat ("**Nuberroca** and
    **Eguzkilore** hold the corridor while…").
  - Targets, witnesses, or incidental mentions do NOT get bolded — only the
    primary actor(s). In "**Mialee** walks past the hidden Langdedrosa, who
    catches her twice with the sword," Mialee is the actor of the epic beat
    (walking into the trap); Langdedrosa is the trap, not the deed.
  - Group / unnamed actor (no single character carrying the moment): no bold;
    the beat's noun phrase carries it (e.g. "The party survives the dragon's
    second pass…").
-->
## 3. Epic moments

1. [<scene>.<beat>](minutes-<NN>.md#<scene>--<slug>) — **<name>** <one-line short description of the deed>.
2. [<scene>.<beat>](minutes-<NN>.md#<scene>--<slug>) — **<name>** <one-line short description of the deed>.

<!--
SECTION 4 — Events

Chronological skeleton of the session, readable AT A GLANCE. ONE bullet per
scene; ONE SENTENCE per bullet. A bullet is a single, tight sentence that
captures the scene's outcome — not its beats. Sub-clauses can be joined
however reads cleanly — em-dash, comma, semicolon, "and". The bound is the
sentence count: don't chain two complete sentences with a period (that's the
minutes' job).

HARD WORD LIMIT: 20 words per bullet. If a bullet exceeds 20 words, condense
or split into adjacent scene-level bullets — the bullet is doing the minutes'
job. Count hyphenated tokens, possessives, and numeric ranges (e.g. "200–300")
as one word each. Bare "Short rest." / "Long rest." bullets are not exempt
from the cap but will never reach it.

TARGET LENGTH: 6–10 bullets for a typical session. More than 10 means scenes
are being unpacked into their beats — collapse aggressively (a multi-encounter
fight is one bullet, not five). Fewer than 6 means distinct scenes are being
merged that should sit on their own line.

Time stamps inline at the start of a bullet where the corresponding minutes
scene has them; omit when not anchored. DO NOT duplicate the session's
in-fiction start time on the first event — that information is already in
§2 Metadata (the In-fiction date row). The first event bullet carries a
timestamp only if it diverges meaningfully from the metadata start; otherwise
it leads with the event description directly. Same rule for the last event
and the session end time. Subsequent in-session timestamps (a long-rest
wake-up, a scene that resumes "the next morning", etc.) are kept inline as
usual.

Both short and long rests use the SAME FORMAT: "Short rest." / "Long rest." as
the base entry, OPTIONALLY followed by short relevant info ("Long rest. In the
barracks." / "Short rest. Cult map studied (X southeast of Greenest).").
Always their own bullet. The trailing info is still a fragment, not a second
sentence.

Combat at encounter level, not round-by-round: outcome, turning points,
casualties, status changes. A multi-round fight collapses to ONE bullet
shaped as "<encounter name> — <outcome and any key turning point / casualty /
status change>". Per-round mechanics, per-PC actions, spell names, and
condition swaps live in the minutes, NOT here. A multi-encounter scene (e.g.
a cave clearance) gets one bullet per ENCOUNTER, never one per phase, never
one per round.

WHAT BELONGS IN §4 vs WHERE IT BELONGS:
  - Reward / fee terms → §6 Missions & rewards (not the briefing bullet).
  - Fallback contact / future rendezvous → §5 NPCs or §9 Loose ends.
  - Items acquired → §8 Status changes.
  - Per-PC mechanical detail → minutes only.
  Keep the §4 bullet to the scene's chronological fact.

STYLING — plain text by default. Bold (**…**) and italic (*…*) are permitted
ONLY when something SPECIAL is being highlighted (a decisive turn of the
session, a named magic item acquired, a death). Do NOT auto-bold every entry,
do not bold timestamps or rest lines, do not stylise just for visual rhythm.
The default for any line is plain prose; reach for emphasis only when the
beat genuinely warrants it.

Don't re-narrate what's in minutes. The Events section is a skeleton for fast
scanning, not a parallel narrative. For any given line, ask "would removing
this leave a gap in the chronology?" If no, cut it. Color, atmosphere,
in-fiction reactions, dialogue snippets, character beats, turn-by-turn combat
detail belong in minutes, not here.

In-fiction visible only — section 10 reveals hidden-NPC mechanisms. If a beat's
"true" cause is a hidden agent's action, this section narrates the visible
effect; section 10 names the agent.
-->
## 4. Events

1. <short event description>.
2. <short event description>.
3. Short rest.
4. <short event description>.
5. Long rest. In <location>.
6. ~HH:MM — <short event description after a time-of-day shift>.

<!--
SECTION 5 — NPCs

Only NPCs RELEVANT to this session. An NPC qualifies if any of these hold:

  1. Their NPC sheet is being created as a result of this session. (Tracking
     event itself — a new sheet means a new tracked entity. "Warrants a sheet"
     is the bar: a passing gatekeeper named once does not; an off-screen
     faction contact named as a future destination does. Re-mentions in
     subsequent sessions do not re-trigger this — once the sheet exists, the
     NPC needs one of the other criteria.)
  2. Delivered information important to the party — mission, warning, lore.
  3. Gave or received a mission, briefing, or charge.
  4. Fought the party. ONLY NPCs with a sheet. Unnamed mooks → Events entries,
     not here.
  5. Died or had a meaningful status change. Same sheet constraint.
  6. Made a decision or commitment the party could plausibly follow up on.

ENTRY CONTENT — SHORT, readable AT A GLANCE. Hard word budgets apply.

  FIRST APPEARANCE in the campaign — the entry carries TWO short fragments:
    1. A 3–5 word IDENTITY descriptor (role / faction / species-and-role).
       Examples: "Wounded keep guard.", "Black half-dragon, camp chief.",
       "Half-elf Harper monk, Berdusk.", "Cleric of Chauntea, Greenest temple."
    2. A 3–10 word ACTION fragment for what they did this session.
       Examples: "Recruited as guide.", "Sighted at the central tent.",
       "Performed Sinsong's resurrection on credit.", "Gave the tunnel keys."

    Combined shape: **<Name>** — <identity, 3–5 words>. <action, 3–10 words>.

  RECURRING APPEARANCE — the entry carries ONLY the action fragment, 3–10
  words. Identity is already in the linked NPC file; don't restate.
    Examples: "**Tarbaw Nighthill** — assigns the recon mission."
              "**Escobert the Red** — interrogated the captured cultist to
              death overnight."
              "**Langdedrosa Cyanwrath** — shielded Frulam, called out
              Nuberroca by sight."

  BAR for the action fragment: "does this change how the GM treats this NPC
  next session?" If yes, write it (3–10 words). If no, leave the entry bare
  (linked name on its own line) — the bullet still documents that the NPC
  was on stage; the link sends the GM to the sheet for everything else.

  ✓ Keep an action: significant deltas. Killed a PC. Captured. Switched
    sides. Gave or received a mission. Revealed a faction tie. Promised
    something. Moved to a new location. Died.
  ✗ Drop the action (leave entry bare): tactical fluff. Attacked with
    surprise. Used Multi-Attack. Took a hit. Held the line for a round.
    Spoke first in a dialogue. Generic combat presence is already in §4
    Events; do not duplicate it here.

DETAILS LIVE IN THE MINUTES, NOT HERE. If the entry needs more than the
identity + action fragments to make sense, the extra context belongs in
minutes — write it there and trim the §5 entry. Do NOT restate character
traits, stat-block details, species/class/weapons/spells, or backstory —
those live in `campaign/npcs/<name>.md`. The link sends the GM there for
everything beyond the two fragments above.
-->
## 5. NPCs

1. **[<NPC name>](../../campaign/npcs/<stem>.md)** — <identity, 3–5 words>. <action this session, 3–10 words>.
2. **[<NPC name>](../../campaign/npcs/<stem>.md)** — <action this session, 3–10 words>.
3. **[<NPC name>](../../campaign/npcs/<stem>.md)**

<!--
SECTION 6 — Missions & rewards

Cross-session tracking. Rendered as a MARKDOWN TABLE with fixed columns; one row
per entry; rows chronological by opening session.

  | # | Status | Mission | Reward | Giver | Sessions | Notes |

  - # — positional row number (1, 2, 3, …). Refers to *this session's* table
    position; rows renumber from 1 when closed missions drop from next session's §6.
  - Status — Open, Completed, Failed, Abandoned. Capitalised.
  - Mission — canonical name set at opening, NEVER renamed mid-flight. Plain
    in-fiction phrasing, the GM's own words (e.g. "Clear the keep's old tunnel").
    Do NOT frame by published-module chapter or sub-mission.
  - Reward — promised (open) or paid (closed). Literal "None" when none exists
    (debts paid BY the party); "Not stated" when terms were silent; otherwise
    actual value.
  - Giver — counterparty (NPC for missions, creditor for obligations, payer for
    disbursements).
  - Sessions — lifecycle. "S<N> →" (trailing arrow) for open. "S<N> → S<NN>"
    for closed. Same-session open-and-close: "S<N> → S<N>".
  - Notes — short clause(s) reflecting the LIVE mission state at a glance,
    NOT only this-session deltas. Rewrite / recondense each session as
    needed; this is a tracker cell, not an append-only journal. May carry
    any of:
      * Standing intel the party already holds about the mission ("Target
        in Berdusk; contact is Avara (tiefling).").
      * Useful context for next-session prep (terms, deadlines, known
        complications, who's chasing them, where they were last seen).
      * A meaningful outcome from this session, noted as such and kept
        SHORT ("Tunnel cleared." / "Rendezvous missed").
      * Closed rows: outcome / what was paid / how it resolved.
    Quiet session on a row with NO delta of any kind — no action taken, no
    new intel, no movement, no complication — use the literal "No progress."
    Do NOT carry forward the prior session's live-state clause when the row
    was untouched; the literal is the signal that this session added nothing.
    Rows with ANY delta (even partial, even a dead-end lead) take a fresh
    short clause instead.

ENTRY TYPES under one schema:
  1. Missions — explicit NPC asks with terms.
  2. Obligations — debts or oaths owed BY the party. Reward column is always "None".

NON-TRANSACTIONAL encounters (e.g. a duel against a named foe) belong in
Events / Epic moments / NPCs, not here.

CARRY-FORWARD. Open rows are listed in every session until they
close. Rows that closed *this* session appear in this session's table only —
drop from §6 in subsequent sessions. Walk gm-<N-1>.md §6 at draft time and copy
every open row forward.
-->
## 6. Missions & rewards

| # | Status | Mission | Reward | Giver | Sessions | Notes |
|---|---|---|---|---|---|---|
| 1 | Open | <Mission name> | <reward or None / Not stated> | <Giver> | S<N> → | <one short clause> |

<!--
SECTION 7 — Knowledge gained

What the party now knows about plot / factions / NPCs / locations. Drives
next-session prep. FACTS ONLY — what they observed or were told. Do NOT
extrapolate ("the raiders must have killed defenders to get the livery") or
rush to conclusions; leave inferences for the GM. If a fact has multiple
plausible explanations, state the fact and stop.
-->
## 7. Knowledge gained

1. **<bold key phrase>.** <fact, observed or told, no inference>.

<!--
SECTION 8 — Status changes

Alliances formed/broken; conditions carried forward (curses, lasting injuries
that don't heal at a long rest, marks like Hunter's Mark); deaths; level-ups;
honour changes (numeric delta per PC); magic items or items of special
significance acquired/lost; party composition changes (recruits / departures).

MUNDANE wounds and low HP at session end are NOT tracked — they reset on the
next long rest.

MUNDANE LOOT EXCLUDED. Healing potions, generic weapons, torches, ammo, food,
gold, replaceable / consumable goods do NOT go here. Status changes records
ONLY: magic items, intel items (maps, letters, insignia), named/sentimental
items, items of explicit plot significance.

CURIOS AND ODDITIES default to MUNDANE — looted trinkets of unknown function
(a glowing worm, a ball of grease, a piece of bark, etc.) are NOT tracked in
§8 unless the GM has explicitly flagged the item as magical or plot-significant
(in which case it qualifies as a magic item or intel item under the rule
above). A passing mention in §4 Events is permitted; full §8 tracking is not.
Do not promote unidentified curios to status changes on speculation that they
"might do something" — if their nature is not yet established, they are
mundane until proven otherwise.
-->
## 8. Status changes

1. **<bold key phrase>.** <one clause describing the change>.

<!--
SECTION 9 — Loose ends

Open threads the GM may need to resurface: undisposed captives, unidentified
names or figures, unexplained clues, pending decisions, asked-but-unanswered
player questions.

FORMAT. Each entry: "**Standardised name** — short description of what surfaced
this session." Bold the standardised name.

STANDARDISED NAMES are short identifying phrases ("Captured cultist",
"X southeast of Greenest", "Mondath", "Dragon Woman") reused across sessions
whenever the same thread resurfaces. Same name → same thread → greppable across
sessions/*/gm-*.md.

NO status field. NO IDs. NO automatic carry-forward. A loose end appears in
session N's gm only if it surfaced in session N. The GM scans past gm files to
revive cold threads; the AI does not auto-carry-forward.

TEST: would the GM act on the item next session — surface it to players, plan a
scene, drop a hint, follow up an NPC? If no, cut. Specifically, do NOT include:
  - Items already tracked in Missions & rewards, NPCs, Knowledge gained, or
    Status changes — no cross-section duplication.
  - Active campaign context ("the assault is ongoing") — natural state of next
    session's opening, not a discrete thread.
  - Atmospheric color — flavour belongs in minutes.
  - Backwards-looking annotations ("resolved in SX") — once a loose end resolves,
    drop the entry; don't annotate.
-->
## 9. Loose ends

1. **<Standardised name>** — <short description of what surfaced this session>.

<!--
SECTION 10 — Secrets

GM-only index of agents and events acting outside player awareness. Three
sub-categories under one section:

  - HIDDEN NPC ACTIONS — actions a `status: hidden` NPC took, already rendered in
    the minutes via GM-supplied misattribution as natural in-fiction beats (the
    GM handoff in /draft wrote them in). This section indexes those beats 
    by <scene>.<beat> coordinate.
  - OFFSTAGE NPC ACTIONS — actions players didn't witness (e.g. an NPC
    interrogating a prisoner overnight, a hired creature withdrawing for
    reasons the party never learns). GM-authored; the GM adds these entries
    directly to the gm file. Not in transcript, not in minutes, not in triage.
  - FACTION / WORLD EVENTS — moves players don't perceive but that affect
    downstream sessions. GM-authored, same as offstage NPC actions.

FORMAT. Each agent gets one top-level numbered item (the agent's name, bold),
with their actions as a nested ordered list. Group by agent, one top-level item
per agent who acted; skip agents who didn't act. Group recurring instances of
the SAME action under one nested item with comma-separated coordinates.

When the action is rendered in minutes via misattribution, include the
<scene>.<beat> coordinate(s) and a brief description of how the misattribution
appears (paraphrase or short quoted snippet). When the action is NOT in minutes
(offstage NPC, faction move), give the description only — no coordinate.
-->
## 10. Secrets

1. **[<Hidden NPC name>](../../campaign/npcs/<stem>.md)**
   1. <Action> — Scenes <N.M>, <N.M> (<brief in-fiction tell or paraphrase>).
   2. <Action> — Scene <N.M> ("<short quoted snippet from minutes>").

2. **<Offstage NPC name>**
   1. <Description of off-screen action> — <reason / outcome>.
