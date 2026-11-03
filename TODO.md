# TODO

Project-wide cleanup and follow-up work that doesn't belong in a single skill or canon file. Append as items surface; cross out or remove once done.

## Pending

- **Build a downstream-canon-update skill and clarify the pipeline process.** Post-acceptance updates to `campaign/timeline.md`, PC `Current state` blocks, NPC `Campaign notes`, location and faction sheets, and `sessions/inputs/calendar.md` are nominally handled in `/verify`'s After-writing pass + triage §9 *File updates needed* — but this step is under-specified and inconsistently executed. A dedicated skill should consume the accepted `minutes-<NN>.md` + `gm-<NN>.md` + closed triage §9 and apply each downstream update mechanically. Pair with a pipeline-process clarification: where the manual GM acceptance step fits, when `/clear-scene` runs and how often, what the `status:` transitions are (`drafted` → `verified` → `accepted`), which skill owns each canon delta, and what artifacts gate each step.
- **Rethink and shorten `campaign/timeline.md`.** The current entry shape (verbose context clauses) won't scale once 30+ sessions have been recapped. Decide on a tighter row format, or split into eras / arcs. Defer until enough sessions have been processed to see the actual shape of the data.
- **Audit PC `joined_at` values against `sessions/inputs/calendar.md`.** Every PC's `joined_at` field may be mis-anchored after session-numbering changes. Quick check once the calendar is final.
- **Compose Location sheets properly (like PC sheets).** Establish a standard file structure for campaign locations mirroring the PC-sheet conventions, and ensure every location has the necessary fields populated.
- **Compose Faction sheets properly**
- **Build a `/npc` skill to flesh out NPC sheets from session info.** Triage §9 ("File updates needed", applied during `/verify`'s After-writing step) currently just lists NPCs to create/update with no scaffolding — the GM does it by hand. A dedicated skill would take a session's `minutes-NN.md` / `gm-NN.md` (plus the NPC template) and produce a draft NPC file, or append to an existing one's `Campaign notes` section while proposing frontmatter updates for GM approval.

  **Companion change to `/draft`:** during the drafting pass, extract every transcript detail relevant to each NPC — descriptions, dialogue, observed actions, traits, mentions of role / faction / equipment — and dump it into a new triage section (one block per NPC). That gives `/npc` rich pre-staged source material to flesh sheets from, without having to re-read the full transcript per NPC later.

  Open design questions before writing the spec:
  - Single name, batch list, or auto-pull from triage's File-updates checklist? (Lean: support all three; default to triage when no args.)
  - Existing-file policy — append-only to body and propose-only for frontmatter, or allow direct rewrites?
  - Cross-session lookup — just the current session, or scan all prior sessions where the NPC appeared? (Lean: current-only by default; `--all-sessions` flag to widen.)
  - Trigger placement — standalone skill invoked from `/verify`'s After-writing step, or integrated into `/verify` (or `/draft` for the NPC-detail extraction half)?
- **Sohey and their tribe.** Sohey is a goblin monk (12 levels monk, 1 barbarian, 1 rogue). Several linked work items:
  - **Create Sohey in Foundry.** Full statblock per the class breakdown above.
  - **Write Sohey's NPC sheet** under `campaign/npcs/` following the standard conventions.
  - **Create the tribe's faction sheet** under `campaign/factions/` (pending the faction-sheet structure decision above). Include the tribe's territory, leadership, numbers, and current standing with the party.
  - **Flesh out what the tribe knows about the Cult of the Dragon.** Decide the extent and specificity of their intel — sightings, movements, named cultists, dragon-related activity in their territory — and where the knowledge came from. Anchor to what's already been established in-fiction; don't invent contradictions.
  - **Flesh out the tribe's motivation for allying (or dealing) with the party.** Core hook: a four-armed troll hunts their people for sport, and the tribe hates it for that. Decide how long this has been going on, casualties, prior attempts to deal with the troll, and what the tribe is willing to trade or risk for help against it.
- **Review calendar WhatsApp notes from S13 to today, in batches.** Walk the WhatsApp log entries between session 13 and the current date, batching the review so no single pass gets too large.
- **Update the archiving method to include the generated PDFs so it can be handed fully to players.** Consider splitting into two `.rar` archives (or folders): one with the full merged audio + transcript, the other with the separate per-player tracks + the generated PDFs.
- timeline events file per session, with defined arcs (1 - 2 can be played in a session, generally only one), then collapse them in the timeline file, that should have 2 columns (left arc name, description, start-end date and session, right a list of single event or smaller span events)
- **Read Amidamaru's Westgate letters and write responses (if applicable).** Three letters dispatched east across S11–S12 with expected arrival dates 29 Uktar, 11 Nightal, and 21 Nightal 1489 DR (see `campaign/pcs/amidamaru.md` *Open hooks*). Ask the player for contents and intended recipient(s), then decide whether any reply comes back via the reverse courier chain — and if so, draft the in-fiction letter and pencil arrival into `sessions/inputs/calendar.md`.
