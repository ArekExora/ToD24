---
name: NPC sheet conventions
description: How to structure character files in campaign/npcs/ — frontmatter, body sections (all required), stance enum, campaign-note date+session format. Mechanical detail (when relevant) lives in the body sections; full stat blocks live elsewhere.
type: feedback
---

When creating or editing NPC files in `campaign/npcs/`:

## File location and identity

**Filename:** lowercase given-name and surname joined with a hyphen (e.g., `tarbaw-nighthill.md`, `ontharr-frume.md`, `lai-angesstun.md`). Include the surname whenever the NPC has one. NPCs with a single name use just that name (`miguel.md`, `recaredo.md`). Do NOT include epithets in the filename (`escobert.md` for *Escobert the Red*, `rezmir.md` for *Rezmir the Black*). Module-canonical names use the published spelling.

**Frontmatter fields (in order):** `name`, `full_name`, `nicknames` (list), `gender`, `species`, `subspecies`, `background`, `class`, `subclass`, `alignment`, `languages` (list), `factions` (list), `status`, `source`.

**`name` vs `full_name`.** `name` is the table-name (what players actually call the NPC); `full_name` is the most ceremonial form (`Tarbaw Nighthill`, `Frulam Mondath`, `Mambrok Eguzkilore`). When the NPC has only one name, `full_name` equals `name`. The H1 heading uses `full_name`.

**`nicknames`** (list, always present). In-fiction or table nicknames. Empty list `[]` when none — keep the field present.

**`status` enum:** `alive` / `dead`. Anything in between (missing, captured, off-stage, fled) lives in Campaign notes as a session-dated bullet — not in this field.

**`source` enum:** `ToD` (Tyranny of Dragons module) / `Homebrew`. Used to flag module-canonical NPCs as reference; the campaign timeline is authoritative.

**`factions:`** — list of faction memberships. Empty `[]` when unaffiliated.

**`class`, `subclass`, `background`, `alignment`, `gender`, `subspecies`** — optional in frontmatter; populate when narratively relevant or available in the source. Empty fields stay present (e.g., `class:` with no value) for shape consistency.

## Body structure

**All body sections are required.** Empty sections render with a placeholder (`None.` or `Not defined.` per section) so the file structure is consistent across NPCs and the recap pipeline can rely on a stable shape. Section order, top to bottom:

1. `# {Full name}` — H1 heading; uses `full_name`.
2. `## Concept` — 1–2 sentence pitch: identity, role, faction tie, why they matter. **Public-facing** (no spoilers — what a player who read the file would learn must be in-fiction-knowable). **Non-temporal** (doesn't change session-to-session except for major reveals like a faction defection).
3. `## Goal` — one-line motivation / agenda. Use `None.` for **service NPCs** whose motivation is implicit in their role (Miguel guards Greenest; Tarbaw governs; Escobert runs the keep — implicit, no separate goal). Populate for **plot-drivers** and **antagonists** (cult priests, faction recruiters, Harpers on missions).
4. `## Appearance` — bullet list of canonical / observable visual features (ToD-canonical for module NPCs; GM-set for homebrew). Use `Not defined.` as the section body when no visual canon exists.
5. `## Role and party stance` — bullet list. **First bullet always carries the party stance** as a labeled enum: `- **Stance:** Hostile / Friendly / Neutral / Wary / Unknown`. Subsequent bullets describe the NPC's function in the world and what they do for / to the party.
6. `## Campaign notes` — chronological session beats. Each bullet: `<in-fiction date> (S<N>) — <event>`. Use `None.` as the section body when the NPC has not yet appeared at the table.
7. `## Notes` — GM-meta annotations: rule deviations, name changes, off-stage status, stat-block tweaks, pre-written future events not yet at the table. Use `None.` when nothing to note.

## Stance values

The **Stance** bullet under `## Role and party stance` is a single-word enum:

- **Hostile** — actively opposed to the party; antagonist.
- **Friendly** — supportive, on the party's side; ally or trusted contact.
- **Neutral** — no strong stance; transactional or undecided.
- **Wary** — cautious, not yet committed; suspicious or testing.
- **Unknown** — not yet established at the table; pre-encounter.

When stance has nuance (dueling-honour convention, sworn-to-faction-but-personally-respectful), call it out in subsequent role bullets — the Stance value stays a single word.

## Campaign-note format

Each bullet under `## Campaign notes` is a **plain-text** line in the form: `<in-fiction date> (S<N>) — <event>`. Bullets are not wrapped in backticks; render as normal Markdown list items.

- **Date:** Faerûnian calendar; `<day> <month> <year>` form (e.g., 23 Marpenoth 1489); no `DR` suffix.
- **Session:** `(S<N>)` — natural session number, no zero-padding (S1, S12).
- **Event:** short past-tense statement of what happened. **KEEP IT ONE LINE.** No multi-sentence explanations, no "established retroactively in" prose, no double-context. A campaign note is a one-line canon record, not a mini-recap.

**Why:** The GM has repeatedly pushed back on verbose Campaign-notes entries — the correct scale is a single terse sentence (`26 Marpenoth 1489 (S9) — Killed in the Tiamat shrine.` is the reference form). Anything longer belongs in the session GM file, not here.

Multi-day events use a date range: 22-23 Marpenoth 1489 (S2) — ...

Append-only — don't rewrite history. When an NPC's status changes (becomes captured, dies, defects), add a new bullet rather than editing prior ones.

## Pre-written future events

When the GM has written speculative or planned events (e.g., a planned encounter, a foreshadowed reveal) that haven't yet happened at the table, those go in `## Notes` with a leading marker:

```
- (Pre-written; not yet at the table.) {description}
```

They do **not** go in `## Campaign notes` — that section is canon-only, populated post-session.

## Why / how to apply

These conventions exist so all NPC files have one consistent shape — the recap pipeline (`/draft`, `/gm`, `/saga`) can rely on a stable structure when reading the cast, descriptors, and Concept verbatim without parsing prose.

Treat `campaign/npcs/_template.md` as the canonical structure; any deviation should be intentional and discussed first.
