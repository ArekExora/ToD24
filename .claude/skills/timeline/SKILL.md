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
- [`campaign/arcs.md`](../../../campaign/arcs.md) — arc registry (title, description, open / close dates). Read-only here; the GM maintains it by hand. Used to validate arc names referenced from per-session files.
- `campaign/npcs/` — read the directory listing to know which NPCs have sheets. Only NPCs with a sheet qualify for the *Named recurring NPCs* event category. No sheet bodies are read; just filenames.

## If `timeline-<NN>.md` already exists

Switch to **audit mode**, never overwrite. An existing file has almost certainly been GM-edited after generation, and those edits are canon.

In audit mode:

1. Read the existing file.
2. Walk the same *Before writing* inputs.
3. Re-derive the expected arc title(s) (carry-forward from `timeline-<N-1>.md`, or the GM-declared opening / closing) and the expected event list under the event-inclusion rules. Compare.
4. Surface a numbered finding for each divergence: arc title mismatch, arc title not present in `campaign/arcs.md`, missing event, surplus event (present in file but with no minutes support), event that misrepresents the cited scene, out-of-order events, NPC-named event where the NPC has no sheet.
5. Stop and hand the list to the GM. Iterate per-finding — the GM decides which to address; `/timeline` does not auto-edit in audit mode.

## Before writing

1. **Read accepted minutes end-to-end.** The minutes are the only content source for events. Note: scene structure, titles, in-fiction date lines, named NPCs, party location shifts, mission / faction references, PC state changes.
2. **Read `sessions/session-<N-1>/timeline-<N-1>.md`** (if N > 1) — extract the **last arc title** (the last `## <Title>` H2). That's the arc the party enters session NN under unless the GM declares otherwise.
3. **Read [`campaign/arcs.md`](../../../campaign/arcs.md)** — cache the set of known arc titles (each `## <Title>` heading). Used to validate that any arc title referenced in the per-session file exists in the registry.
4. **List `campaign/npcs/`** — the filename stems are the set of NPCs with sheets. Cache this for the event-inclusion check.
5. **Do not read the transcript. Do not read triage. Do not consult any other canon files.** The accepted minutes are the single source of truth for events; the prior timeline file is consulted only for arc carry-forward; `arcs.md` and `npcs/` are consulted only for registry / sheet checks.

## Arc continuity handoff

**Arc transitions are rare.** Most sessions silently continue the active arc, so the skill carries the prior session's arc forward **without prompting** by default. Only prompt the GM when the session's identified events carry one or more **arc-transition signals**.

### Arc-transition signals

Scan the drafted event list (after applying the event inclusion rules and quote-anchoring) for any of these. If none are present, carry the prior arc forward silently and move on.

- **Durable location change.** Party permanently relocates to a new settlement, region, or stronghold — not a brief visit or a dungeon delve expected to end at that session's close. *(e.g., leaving Greenest for good and arriving at Elturel, Baldur's Gate, Waterdeep.)*
- **Major mission completion.** A multi-session objective wraps up — the driving motivation of the current arc is resolved.
- **Major mission acceptance.** The party commits to a new multi-session objective that redefines what the party is doing *going forward*. Same-session missions do not qualify — the Tarbaw tunnel-clearing in S01 is not an arc opener.
- **Faction oath or defection.** A PC joins or breaks from a named faction. *(e.g., Nuberroca sworn into the Order of the Gauntlet.)*
- **Chapter-end feel.** The session reads as a clean break — *"and the party departed X"* with a clear elsewhere in view.

Err toward silence. If the signals are ambiguous, carry forward and let the GM re-open the question on a later session if they want.

### When one or more signals are present

Ask the GM, once, with the carry-forward still the default so a quiet answer suffices:

> *"This session's events suggest a possible arc shift — \<brief reason citing the signal(s)\>.*
>
> *Default: continue the current arc **\<title\>**. Any change?*
> - *No (default) → continue under **\<title\>**.*
> - *Current arc closes this session — **reminder: update `campaign/arcs.md`** by hand to record the close date.*
> - *New arc opens this session → provide the arc **title** and the transition point (start of session, or after a specific scene). **Reminder: add the new arc to `campaign/arcs.md`** by hand with description + open date.*
> - *Both — close and open; name the transition point and update `arcs.md` for both."*

### First-session exception

If no prior timeline file exists (`N == 1`, or the prior file is missing), there's no arc to carry forward — always ask for the initial title, regardless of signals:

> *"No prior timeline file found. What arc is session NN played under? Provide the **title** only; add full metadata to `campaign/arcs.md` by hand afterwards."*

### File-shape rules

The GM's answer determines the H2 arc headers in the file. A session with a **mid-session arc transition** produces two H2 arc sections; events before the transition sit under the first, events from the transition onward sit under the second. Never split events across arcs without an explicit GM transition.

The per-session file carries arc **titles only** — no description, no date-range line. Those live in [`campaign/arcs.md`](../../../campaign/arcs.md) and are picked up at campaign-render time by `build_full_timeline.py`. The skill **reminds the GM** when `arcs.md` needs a manual update; it never writes to `arcs.md` itself.

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

The per-session file carries the **data layer only** — arc title(s), month sub-header(s), and event table rows. No Homebrewery directives, no frontmatter, no arc description, no date-range line. All presentation / decoration lives in the build script that composes `campaign/timeline.md` from per-session files + [`campaign/arcs.md`](../../../campaign/arcs.md).

```markdown
# Session NN timeline

## <Arc Title>

### <Month> <YYYY> DR
| Date    | Session  | Event                      |
|:--------|:---------|:---------------------------|
| <DD>    | S<NN>    | <Event text. Bold main actor / central noun only.> |
| <DD - DD> | S<NN>  | <Event that spans several in-fiction days.> |

### <Next Month> <YYYY> DR    <!-- only when the session crosses a month boundary -->
| Date    | Session  | Event                      |
|:--------|:---------|:---------------------------|
| <DD>    | S<NN>    | <First event in the new month.> |

## <Second Arc Title>    <!-- only when a mid-session arc transition occurred -->

### <Month> <YYYY> DR
| Date    | Session  | Event                      |
|:--------|:---------|:---------------------------|
| <DD>    | S<NN>    | <First event under the new arc.> |
```

**Rules:**

- **H1 title:** `# Session NN timeline` — single H1, zero-padded `NN`, blank line after.
- **Arc title.** `## <Title>` (H2). Must match a `##` heading in [`campaign/arcs.md`](../../../campaign/arcs.md) exactly. No "Arc:" prefix. No description, no date-range line, no Homebrewery frame — those live in `arcs.md` and are added by the build script when rendering the campaign timeline. One arc section per arc the session touches (usually one).
- **Month sub-header.** `### <FullMonth> <YYYY> DR` — month name from the `Full` column of [`campaign/calendar.md`](../../../campaign/calendar.md). One per in-fiction month the session touches; most sessions touch only one. A fresh event table starts under each sub-header.
- **Event table.** Markdown table with three left-aligned columns directly below each month sub-header:

  ```
  | Date    | Session  | Event                      |
  |:--------|:---------|:---------------------------|
  | 22      | S01      | Party arrives at **Greenest** during a raid. |
  ```

  Column widths in the source may be padded for readability; they don't affect rendering. The three column headers are literally *Date*, *Session*, *Event*.
- **Date cell.** Day number(s) only. Forms:
  - single day: `22`
  - range within one month: `22 - 23`
  - range crossing months: write the crossing month explicitly on the far side of the range (`30 - 2 Uktar`). The row still sits under the earlier month's sub-header. Use sparingly.
  - **intercalary day** (no day number): render with the **full name** per [`campaign/calendar.md`](../../../campaign/calendar.md), e.g. `Feast of the Moon`. Place the row under whichever `### <Month>` sub-header is semantically closest; when in doubt, use the month **before** the intercalary.
  - No month name unless the range crosses months. No year. No `DR`. No `~HH:MM` time prefix.
- **Session cell.** `S<NN>` only — no parentheses, no prefix. Zero-padded to two digits (`S01`, `S07`, `S12`). The explicit session cell lets a row be copy-pasted or merged into `campaign/timeline.md` without losing its session anchor.
- **Event cell.** The event text. One short clause, not a sentence with multiple clauses. Prefer merging a death and its same-session resurrection into a single clause over splitting. If the event text runs to more than ~20 words, re-grain it: either it bundles distinct events (split and reconsider which qualify), or it carries tactical colour that belongs in the minutes (trim).
- **No em dashes (`—`) in event text.** Em dashes take visible space in the rendered table cell and read as stilted prose. Use **colon** when the second clause names or elaborates (*"Cult leadership named: **Rezmir** …"*), **semicolon** when two clauses are related but independent (*"attacks the keep and withdraws wounded; parting line reveals it was hired"*), **period + new sentence** when the second clause stands on its own (*"Cult camp located in the hills south of **Greenest**. Strength roughly 200–300."*), or restructure to avoid the dash entirely. Hyphens (`-`) for compounds (*"black half-dragon"*) are fine.
- **Bold the main actor and central noun of the event, nothing else.** A PC, sheet NPC, faction, or key location gets `**bold**` only when they are the **main actor** performing the event, or the **central noun** the event is about (a location arrived at, a faction joined, an NPC killed or freed). A name appearing in a **passive role** stays plain: a sponsor in a *"by X"* construction (`sworn into the **Order of the Gauntlet** by Ontharr`), a bystander, an NPC named in passing. Rule of thumb: the event text should still read as a coherent summary if someone scans only the bolded names. No other emphasis. No `[EPIC]` markers.
- **Neutral past tense.** No editorial spin, no in-fiction flourish, no invention beyond what the minutes support.
- **Travel: departure, not journey.** When the party travels between locations, tag the **departure date** and phrase the event as the departure (`Party departed **X**, bound for **Y**`). The arrival belongs to its own date and is often best merged into whatever first happens on arrival (`Party arrived at **Y**, where **Z** joined them`). Prefer a single departure date over a range spanning the journey — the journey's midpoints usually carry no event and clutter the timeline.
- **No citations.** The file is downstream of accepted canon; no `[T:…]`, `[GM]`, or `[derived:…]` tags.

## Internal self-verification (run before write)

Mechanical checks. If any fails, fix the entry or surface as a clear error — do not write a file with known violations.

1. **Every event has a verified quote-anchor.** Per the *Writing each event* section, each event line must have (a) a named supporting minutes line range, AND (b) a confirmed trace of each key noun / action-verb / named entity in the event text to a word or phrase inside that range. A bare scene.beat pointer is not enough — the words themselves must match. If a token in your event has no corresponding minutes token, cut, re-anchor, or re-word. **This is the check that catches both memory drift and level-of-description substitution** (the two failure modes documented in *Writing each event*).
2. **Every NPC-named event's NPC has a sheet.** Cross-check against the cached `campaign/npcs/` listing. No sheet → cut the entry (or recast without naming the NPC, if the event qualifies under a different Include category). The sheet existence is a **hard filter**; everything else is a soft-include-under-doubt call that the GM will trim at review.
3. **Event chronology is non-decreasing within each arc.** In-fiction dates and times rise or stay flat as the list proceeds. Never regroup thematically.
4. **Arc section count matches GM input.** One `## <Title>` H2 when no mid-session transition; two when the GM named a transition. Each arc section contains one or more `### <Month> <YYYY> DR` sub-headers with their own event tables.
5. **Every arc title exists in `campaign/arcs.md`.** For each `## <Title>` in the file, grep `campaign/arcs.md` for a matching `## <Title>` heading. If the GM declared a new arc this session and `arcs.md` hasn't been updated yet, surface a visible reminder to update `arcs.md` by hand — do not auto-add.
6. **Event row format.** Each `|`-delimited row below a `### <Month>` sub-header matches `| <date> | S<NN> | <text> |`. Enforce:
   - Three cells (Date / Session / Event) with leading and trailing `|`.
   - **Date cell:** day number(s) only. No month name unless the range crosses into a new month (`30 - 2 Uktar`). No year. No `DR`. No `~HH:MM` time prefix (that's a leak from minutes — strip it).
   - **Session cell:** exactly `S<NN>` — no parentheses, no prefix, zero-padded to two digits (`S01`, `S12`).
   - **Event cell:** a single short clause with main-actor / central-noun bolding.
7. **Table header + alignment row present under each `### <Month>` sub-header.** The two header lines are literally:

   ```
   | Date    | Session  | Event                      |
   |:--------|:---------|:---------------------------|
   ```

   Column widths may be padded differently in the source for readability, but the three column headers must be named *Date*, *Session*, *Event* in that order, all left-aligned (`:---`). A fresh header pair appears under every `### <Month>` sub-header (never share a table across sub-headers).
8. **Every row sits under the correct month sub-header.** Walk each table row; the leading day number (or the first day of a range) must belong to the month named by the preceding `### <Month> <YYYY> DR` sub-header. Cross-month ranges name the far month in the Date cell (`30 - 2 Uktar`) but still sit under the start month's table. Intercalary rows sit under the month semantically closest.
9. **No em dashes in event cells.** Grep each Event cell for `—` (U+2014). Any hit: rewrite the clause with colon, semicolon, period, or restructured sentence per the *Event cell* rule.
10. **No Homebrewery directives.** The per-session file must contain **no** `{{…}}` blocks, **no** `\page` or `\column`, **no** `{wide}` markers. All presentation lives in the build script.
11. **No transcript-level or triage content leaks in.** Scan for HP / AC / roll numbers, slot levels, hedges (*"presumably"*, *"possibly"*), `[T:…]` / `[Td:…]` / `[derived:…]` / `[GM]` tags, `[EPIC]` markers. All forbidden.
12. **Named entities use the spelling from minutes.** Don't normalise or correct — accepted minutes is the canon spelling.
13. **No frontmatter block.** The file opens directly with `# Session NN timeline`.

Print a one-line status (file written + arc count + event count) and stop.

## Reference

- **Arcs registry:** [`campaign/arcs.md`](../../../campaign/arcs.md) — single source of truth for arc title, description, open date, close date. GM-maintained manually. The skill reads but never writes.
- **Calendar:** [`campaign/calendar.md`](../../../campaign/calendar.md) — authoritative source for FR month names, abbreviations (used in event lines), and intercalary days. **Do not inline month names in this file or rely on memory — the calendar file is the single source of truth.**
- **Minutes schema:** [`sessions/templates/minutes-template.md`](../../../sessions/templates/minutes-template.md).
- **Campaign build script:** `build_full_timeline.py` (planned sibling of `build_full_gm.py` / `build_full_saga.py`) composes `campaign/timeline.md` from per-session files + `arcs.md`. Additive by design — preserves manual GM edits to `campaign/timeline.md` (e.g. page breaks) and only inserts new events as sessions are added. Per-session files are the data layer; `arcs.md` is the arc metadata; `campaign/timeline.md` is the rendered output.
- Memory: [feedback_gloss_budget.md](../../memory/feedback_gloss_budget.md), [feedback_no_invention.md](../../memory/feedback_no_invention.md), [feedback_quote_anchor.md](../../memory/feedback_quote_anchor.md).
