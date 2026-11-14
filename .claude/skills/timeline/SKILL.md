---
name: timeline
description: Generate the arc-indexed per-session timeline (`timeline-<NN>.md`) from GM-accepted `minutes-<NN>.md`. Groups significant in-fiction events from the session under the campaign arc they belong to. Carries the active arc forward from the prior session's timeline file unless the GM declares a new arc opens, or the current arc closes, this session. Use this whenever the GM asks for the session's timeline, arc log, or a record of how a session fits into the broader campaign arcs — even if they don't explicitly name the skill.
---

# /timeline

**Generates** `sessions/session-<NN>/timeline-<NN>.md` — the arc-indexed event log for a single session. Significant in-fiction beats from the accepted minutes are grouped under one (usually) or two (rarely) **campaign arcs**. The arc carries forward from the previous session's timeline file by default; the GM declares arc openings and closings during the handoff.

The file is an audit-trail artifact: a per-session chronicle, read by the GM later to see how the session fits into the broader arc.

## Output

`sessions/session-<NN>/timeline-<NN>.md` — canon, archived.

## Required inputs (ask if missing)

- **Session number** (NN).
- `sessions/session-<NN>/minutes-<NN>.md` — must carry `status: accepted` in its frontmatter. **If the file does not exist, or the `status` field is missing / not `accepted`, surface a clear error and stop.**
- `sessions/session-<N-1>/timeline-<N-1>.md` — read-only, consulted for the arc-continuity handoff. **If N > 1 and this file is missing**, surface a clear note and treat the handoff as if no prior arc were active.
- `campaign/npcs/` — read the directory listing to know which NPCs have sheets. Only NPCs with a sheet qualify for the *Named recurring NPCs* event category. No sheet bodies are read; just filenames.

## If `timeline-<NN>.md` already exists

Switch to **audit mode**, never overwrite. An existing file has almost certainly been GM-edited after generation, and those edits are canon.

In audit mode:

1. Read the existing file.
2. Walk the same *Before writing* inputs.
3. Re-derive the expected arc state (carry-forward title / description / start-date, or the GM-declared opening / closing) and the expected event list under the event-inclusion rules. Compare.
4. Surface a numbered finding for each divergence: arc title or description mismatch, arc date-range inconsistency, missing event, surplus event (present in file but with no minutes support), event that misrepresents the cited scene, out-of-order events, NPC-named event where the NPC has no sheet.
5. Stop and hand the list to the GM. Iterate per-finding — the GM decides which to address; `/timeline` does not auto-edit in audit mode.

## Before writing

1. **Read accepted minutes end-to-end.** The minutes are the only content source for events. Note: scene structure, titles, in-fiction date lines, named NPCs, party location shifts, mission / faction references, PC state changes.
2. **Read `sessions/session-<N-1>/timeline-<N-1>.md`** (if N > 1) — extract the **last arc section** in full: title, date-range line, description. This is the arc the party enters session NN under unless the GM declares otherwise.
3. **List `campaign/npcs/`** — the filename stems are the set of NPCs with sheets. Cache this for the event-inclusion check.
4. **Do not read the transcript. Do not read triage. Do not consult any other canon files.** The accepted minutes are the single source of truth for events; the prior timeline file is consulted only for arc carry-forward; the NPC directory is consulted only for the sheet-existence check.

## Arc continuity handoff

After loading inputs — and only after — ask the GM about arc state, exactly once. Phrase the ask with the carry-forward as the default so a quiet answer suffices:

> *"Prior arc (from `timeline-<N-1>.md`): **\<title\>** — opened \<start date\> (S\<N-prev-open\>).*
>
> *Default: carry forward through session NN. Any change this session?*
> - *No (default) → the arc continues, no state change.*
> - *Closes this session → in-fiction close date (defaults to session end).*
> - *New arc opens this session → title, one-line description, open date (defaults to session start), and whether it opens from the start of the session or after a specific scene.*
> - *Prior arc closes AND a new one opens → both sets of info; name the transition point."*

If no prior timeline file exists (N == 1, or the prior file is missing), ask instead:

> *"No prior timeline file found. What arc is session NN played under? Need: title, one-line description, open date (defaults to session's in-fiction start)."*

The GM's answer determines the arc headers and date-range lines in the file. A session with a **mid-session arc transition** produces two H2 arc sections; events before the transition sit under the first, events from the transition onward sit under the second. Never split events across arcs without a GM transition.

## Event inclusion rules

Events are **arc-driving facts** — the handful of developments the GM would want to find later when reconstructing how the arc moved forward. Not every scene, not every sheeted-NPC appearance, not every memorable moment. **When in doubt, include** — trimming a borderline event during GM review is cheap; recovering a dropped one later requires re-reading the minutes.

**Include:**

- **Party location changes.** Settlement / region / dungeon transitions; durable relocations.
- **Party-stance commitments.** The session's one-line answer to "what did the party commit to?" — joining a town's defense, pledging to a cause, aligning with or breaking from a faction.
- **Arc-driving NPC events.** A sheet NPC (filename in `campaign/npcs/`) **and** the event changes something that outlives the session: NPC killed, freed, allied with, betrayed, recruited, defected, revealed as X, resurrected; or mission handed off / completed / revoked through them. **No sheet, no entry.** **Sheet but no arc-level change, no entry** — a castellan handing over keys to clear a same-session dungeon is not an event, even though he has a sheet.
- **Character-defining PC events.** Death, resurrection, oath or faction induction, level milestone unlocking a class-defining ability, lasting injury or blessing, reputation shift.
- **Mission / faction state changes.** A sheet NPC tasks the party with something — defending a keep, clearing a tunnel, infiltrating a cell, delivering a message. Mission accepted, completed, abandoned, revoked. Faction allegiance sworn or broken. Plot-item received, delivered, or destroyed. **A same-session mission (opened and closed in one session) still counts** if a sheet NPC was the one who tasked the party — the arc-level fact is that the NPC chose them, not whether the mission outlived the session.

**Exclude:**

- **`[EPIC]` tags do not qualify an event on their own.** Most EPIC beats are aesthetic highlights with no durable arc weight. An EPIC beat makes the timeline only if it independently satisfies one of the Include categories above — then the event is included for *that* reason, not for being EPIC. Never preserve the EPIC marker in the output.
- Tactical detail (chest contents, trap triggers, spell spends, round-by-round combat, HP / AC / roll numbers).
- Per-encounter outcomes (a hunt completed, an ambush survived, a camp defended, a patrol dispatched). These happen constantly; filing each one buries the arc-level story. Only promote to an event when the encounter outcome *is* a sheet-NPC / location / mission / faction / PC state change under the Include list.
- Pacing / meta beats (*"party rests for the night"*, *"cliffhanger into S<N+1>"*, *"session ended mid-combat"*).
- Hospitality, small talk, flavour cameos, local-colour dialogue.
- Speculation, unverified rumours, GM-side secrets. If it isn't in the accepted minutes, it doesn't go here.

**Merge related events.** A death and a same-session resurrection are **one event**, not two (*"**Sinsong** killed by a spider swarm, resurrected at the keep by a cleric"*). A mission accepted and completed in the same session is one event (and typically fails the Include filter above, so cut entirely). Arrivals and immediate commitments at the same location may stay separate when the commitment is the point (arriving at a burning town is a location change; joining its defense is a stance commitment — both can stand).

**Target density:** a typical session yields **1–4 events**. A low-action or travel session may have 0; a plot-heavy session may have 5–6. Terseness is the virtue — if the session boils down to "we arrived somewhere and lost nothing durable", that may be zero events.

## Writing each event — quote-anchor first

Before writing any event line, locate the minutes span that supports it and **quote the key factual tokens verbatim in a scratchpad**. The event text is then written as a faithful paraphrase of those tokens. If a noun or verb in your drafted event text isn't traceable to a word or phrase in the quoted span, it's invented — cut, re-anchor, or rewrite.

This prevents two recurring failure modes observed in practice:

- **Memory drift.** Reading the minutes once at planning time and writing events later from internal summary substitutes plausible-sounding but wrong tokens. Observed: *"killed by a spider swarm"* (minutes) became *"killed by giant-spider venom"* (drafted event) — the drafter pointed at the correct scene.beat but used words the beat didn't carry. **Quoting at write-time forces a re-read of the actual span.**
- **Level-of-description substitution.** When the event is a mission, task, oath, or named outcome, the exact wording of the task matters. Picking a plausible high-level paraphrase slides the fact. Observed: Ontharr's mission to *"trace the caravan to Baldur's Gate"* (minutes) became *"infiltrate the cult"* (drafted event) — the general plot direction swapped in for the specific task. **Quote the verbs and nouns the NPC actually used.**

**Scratchpad format** (internal, not in output):

```
Event <N>: [source: scene <s>, beat(s) <b>]
  Minutes tokens: <verbatim short quotes of the key facts>
  Draft: <the event text being written>
  Trace: <each key noun/verb in the draft → the minutes token it rests on>
```

The scratchpad is throwaway — once the event is written and the trace check passes, drop it. Its only job is to keep writing anchored to the minutes' actual words rather than the drafter's summary of them.

## File structure

No frontmatter — all metadata lives in `minutes-<NN>.md`; duplicating it here would create a second maintenance point for no benefit.

```markdown
# Session NN timeline

## Arc: <Arc Title>
<Open date> (S<N-open>) → [<Close date> (S<N-close>)]
<One-line description.>

- <DD Month> (S<NN>) — <Event text. Bold main actor / central noun only.>
- <DD - DD Month> (S<NN>) — <Event that spans several in-fiction days.>
- …

## Arc: <Second Arc Title>    # only when a mid-session arc transition occurred
<Open date> (S<NN>) →
<One-line description.>

- <DD Month> (S<NN>) — <First event under the new arc.>
- …
```

**Rules:**

- **Arc header: `## Arc: <Title>`.** The `Arc:` prefix makes files searchable across sessions.
- **Date-range line directly below the arc header.** Format: `<Open date> (S<N-open>) → <Close date> (S<N-close>)`. When the arc has not yet closed, the right-hand side is empty — just the trailing `→ ` with no close date. Open and close dates use the **full** FR calendar form (`DD <FullMonth> YYYY DR`, e.g. `22 Marpenoth 1489 DR`) — month names from the `Full` column of [`campaign/calendar.md`](../../../campaign/calendar.md). This is the single place the year appears in the file, so the arc date-range line always carries it.
- **Description on the next line.** One short sentence, in the GM's words, carried forward verbatim from the file that opened the arc. Do not rewrite or elaborate.
- **Blank line, then events.** Events are a flat ordered list under each arc, chronological by in-fiction time at the table. Never regroup thematically.
- **Event line format:** `- <date> (<session>) — <event text>`.
  - **Date** uses the **abbreviated** FR month names from [`campaign/calendar.md`](../../../campaign/calendar.md) (the `Abbr` column — e.g. `Marp`, `Ukta`, `Nigh`, `Hamm`). Full month names are reserved for the arc date-range line and for minutes-file prose. Forms:
    - single day: `22 Marp`
    - range within one month: `22 - 24 Marp`
    - range crossing months: `30 Marp - 2 Ukta`
    - **intercalary day** (no day number): render with the **full name** per `calendar.md`'s example — `- Feast of the Moon (S22) — <event>`. The calendar file also lists an intercalary abbreviation column for use in `sessions/status.md`, but event lines keep the full name because intercalaries are rare and read more clearly spelled out.
  - **No time prefix.** Date granularity only — the arc date-range line and the per-event date together give enough chronology; clocks belong in minutes.
  - **No year, no `DR`** on event lines — the year is on the arc date-range line above; repeating it on every event adds noise for no information.
  - **Session column** takes `(S<NN>)` for events that happened entirely in one session, or `(S<N1> - S<N2>)` for events that spanned sessions (a multi-session travel leg, a dungeon delve resolved across two sessions). The session range mirrors the date range.
  - `— ` (em-dash + space) separates the date / session prefix from the event text.
- **Event text is terse.** One short clause, not a sentence with multiple clauses. Prefer merging a death and its same-session resurrection into a single clause over splitting. If the event text runs to more than ~20 words, re-grain it: either it bundles distinct events (split and reconsider which qualify), or it carries tactical colour that belongs in the minutes (trim).
- **Bold the main actor and central noun of the event, nothing else.** A PC, sheet NPC, faction, or key location gets `**bold**` only when they are the **main actor** performing the event, or the **central noun** the event is about (a location arrived at, a faction joined, an NPC killed or freed). A name appearing in a **passive role** stays plain: a sponsor in a *"by X"* construction (`sworn into the **Order of the Gauntlet** by Ontharr`), a bystander, an NPC named in passing. Rule of thumb: the event text should still read as a coherent summary if someone scans only the bolded names. No other emphasis. No `[EPIC]` markers.
- **Neutral past tense.** No editorial spin, no in-fiction flourish, no invention beyond what the minutes support.
- **No citations.** The file is downstream of accepted canon; no `[T:…]`, `[GM]`, or `[derived:…]` tags.

## Internal self-verification (run before write)

Mechanical checks. If any fails, fix the entry or surface as a clear error — do not write a file with known violations.

1. **Every event has a verified quote-anchor.** Per the *Writing each event* section, each event line must have (a) a named supporting minutes line range, AND (b) a confirmed trace of each key noun / action-verb / named entity in the event text to a word or phrase inside that range. A bare scene.beat pointer is not enough — the words themselves must match. If a token in your event has no corresponding minutes token, cut, re-anchor, or re-word. **This is the check that catches both memory drift and level-of-description substitution** (the two failure modes documented in *Writing each event*).
2. **Every NPC-named event's NPC has a sheet.** Cross-check against the cached `campaign/npcs/` listing. No sheet → cut the entry (or recast without naming the NPC, if the event qualifies under a different Include category). The sheet existence is a **hard filter**; everything else is a soft-include-under-doubt call that the GM will trim at review.
3. **Event chronology is non-decreasing within each arc.** In-fiction dates and times rise or stay flat as the list proceeds. Never regroup thematically.
4. **Arc header count matches GM input.** One `## Arc: <title>` section when no mid-session transition; two when the GM named a transition.
5. **Arc date-range line is consistent with GM input.** If the GM said the arc continues, the line matches the carry-forward from the prior timeline file. If the GM said the arc closes, the close date and `(S<NN>)` are filled in. If the GM opened a new arc, the open date and `(S<NN>)` are filled in and the close side is empty.
6. **Arc description carries forward verbatim.** When the arc was already open before session NN, its description reads exactly as in the prior timeline file — no rewrites.
7. **No year, no `DR`, no clock time on event lines.** Scan every `-` event bullet; the date prefix carries day(s) + month (+ month if the range crosses months), and nothing else. A `~HH:MM`-style time prefix is a leak from minutes — strip it.
8. **No transcript-level or triage content leaks in.** Scan for HP / AC / roll numbers, slot levels, hedges (*"presumably"*, *"possibly"*), `[T:…]` / `[Td:…]` / `[derived:…]` / `[GM]` tags, `[EPIC]` markers. All forbidden.
9. **Named entities use the spelling from minutes.** Don't normalise or correct — accepted minutes is the canon spelling.
10. **No frontmatter block.** The file opens directly with `# Session NN timeline`.

Print a one-line status (file written + arc count + event count) and stop.

## Reference

- **Calendar:** [`campaign/calendar.md`](../../../campaign/calendar.md) — authoritative source for FR month names, abbreviations (used in event lines), and intercalary days. **Do not inline month names in this file or rely on memory — the calendar file is the single source of truth.**
- **Minutes schema:** [`sessions/templates/minutes-template.md`](../../../sessions/templates/minutes-template.md).
- Memory: [feedback_gloss_budget.md](../../memory/feedback_gloss_budget.md), [feedback_no_invention.md](../../memory/feedback_no_invention.md).
