---
name: PC sheet conventions
description: How to structure character files in campaign/pcs/ — filename, frontmatter, body order, authoring sources, language rules. Mechanical detail lives in Foundry, not here.
type: feedback
---

When creating or editing PC files in `campaign/pcs/`:

## File location and identity

**Filename:** lowercase given name (e.g., `nuberroca.md`). Surnames or epithets are acceptable when the user prefers them (e.g., `eguzkilore.md`). If the form is ambiguous or you're unsure which to use, **ask before writing**.

**Frontmatter fields (in order):** `name`, `full_name`, `nicknames` (list), `gender`, `species`, `subspecies`, `background`, `class`, `subclass`, `alignment`, `languages` (list), `factions` (list), `status`, `player`, `joined_at`. Do **not** include `level` — party level is campaign-wide, tracked in Foundry.

**`subspecies`.** The 2024 PHB splits some species into subspecies (Wood elf, High elf, Shield dwarf, Cloud-giant-ancestry goliath, Red dragonborn, etc.). When a subspecies applies, set `species:` to the parent (e.g., *Elf*, *Dwarf*, *Goliath*, *Dragonborn*) and `subspecies:` to the specific form including the parent noun (e.g., *Wood elf*, *Shield dwarf*, *Cloud giant ancestry*, *Red dragonborn*). Leave `subspecies:` empty when the species has no relevant subdivision.

**`name` vs `full_name`.** `name` is the **table-name** (what players actually call this PC at the table — `Mialee`, `Nuberroca`, `Sinsong`). `full_name` is the most ceremonial form available (`Mambrok Eguzkilore`, `Nuberroca Quebrantacielos`). When the PC has only one name, `full_name` equals `name`. The `# H1` heading inside the file uses the `full_name` form.

**`nicknames`** (list, always present). In-fiction or table nicknames the players or other PCs use for this character — e.g., *Cabezabombilla* for Sinsong, *Tortuga gigante* / *Tortuga* for Amidamaru. Recurring nicknames go in this list so the recap workflow can render them verbatim without flagging as STT garble. Single-form names get a single entry; same character in multiple forms gets multiple entries (most common first). Use the empty-list form `nicknames: []` when the character has no nicknames — keep the field present like `factions:`.

**`joined_at`** is the **session number** at which this PC joined the party. Used by the recap workflow to check whether a PC was present at a given session — when generating session-N's recap, exclude PCs whose `joined_at > N`. Use `null` if unknown; those PCs need GM input before they can be filtered correctly.

**`status` values:** `active` (currently played), `inactive` (player has left or PC is benched — flag context in `## Notes`), `dead` (in-fiction death). GM-controlled characters concealed from the players live in `campaign/npcs/` as hidden NPCs, not here — see [feedback_hidden_npcs.md](feedback_hidden_npcs.md).

**`player` field:** the controlling player's first name.

**Hidden truths.** When `species` or another structured field reflects a hidden truth (e.g., Aasimar passing as Dwarf), put the truth in frontmatter and explain the gap in Notes.

## Mechanical detail lives in Foundry

The PC markdown files at `campaign/pcs/<name>.md` are not a parallel character sheet — **Foundry is**. The markdown carries only what's load-bearing for AI verification (named class / species / feat features, spells, senses, resistances) or for narrative reference (Concept, Goal, Current state, Signature, Secrets, Identity, Ideals / Bonds / Flaws / Personality traits, Appearance, Biography).

**Do not add to PC markdown:** HP, AC, Initiative, Speed, Hit Dice, ability scores, saving-throw proficiencies, skill proficiencies, weapon / armor / tool proficiencies, weapon masteries. These live in Foundry and are looked up there during play.

**Recap-pipeline corollary — no ephemeral state in `## Current state`.** When applying triage's `## 8. File updates needed` (during `/draft`'s audit-mode canon-updates step), do **not** add post-session wound state, HP remaining, low-HP-mid-retreat status, expended potions / scrolls / ammunition, expended-or-recharging magic-item charges, or anything that resets at a long rest. All of that is Foundry-tracked. The `## Current state` section captures durable, narrative-level deltas only: new permanent magic items, new key relationships, new plot knowledge, new trauma, new open hooks — not the "Mialee took a potion this fight" / "Sinsong's tattoo recharges at dawn" / "Nuberroca is heavily wounded going into next session" detail. If a `## 8. File updates needed` item lists wound state or consumables for any PC, drop it.

**Magic items** (and any plot-significant items the PC currently has) live under `## Current state → Notable items`, not in a separate `### Magic items` section. Format: bullet with name + brief description + (charges / uses / quirks if mechanical). Mundane gear (clothes, rope, signal whistle) is not tracked.

**Item-derived effects** (resistances, immunities, senses, condition advantages, etc.) granted by a magic item are documented inside the Notable-items entry, **not duplicated** in the `### Senses` or `### Resistances` sections of the Full sheet — those sections capture only species- and feat-derived traits.

**Why:** mechanical-stat duplication between Foundry and markdown was clutter — the AI doesn't read it, the GM uses Foundry for table play, and dual maintenance invited drift. The markdown file's job is narrative reference and named-feature verification.

## Body structure

**Section order, top to bottom:**

1. `# {Name}` — uses `full_name`
2. `## Concept` — 1–2 sentence pitch (public-facing, no secrets); Claude-authored
3. `## Goal` — north-star motivation
4. `## Current state` — dynamic block: `Knowledge of the plot`, `Key relationships`, `Notable items`, `Trauma` (optional), `Open hooks`. Status and faction membership are read from frontmatter (`status`, `factions`), not duplicated here. Recaps update this section.
5. horizontal rule
6. `## Notes` _(optional)_ — GM-relevant meta annotations (rule deviations, hidden identities, IC-propaganda framings, player departures); omit if empty
7. `## Signature` — defining abilities / traits / feats; GM-authored from observed player actions
8. `## Secrets` — hidden knowledge, or "None"
9. `## Full sheet` — feature-verification reference + voice / role-play reference. Subsections, in order: `### Senses`, `### Resistances`, `### Class features`, `### Species features`, `### Feats`, `### Spells`, `### Identity`, `### Ideals`, `### Bonds`, `### Flaws`, `### Personality traits`, `### Appearance`, `### Biography`. Mechanical stats live in Foundry, not here.

## Sources of content

- **Concept** — Claude-authored from the inputs. Public-facing — no character secrets.
- **Goal, Secrets** — seeded from the GM-pasted brief (AI-generated). Can be revised if Forge content reframes them.
- **Signature** — GM-authored from observed player actions. Preserve verbatim. Never overwrite.
- **Full sheet** — feature names from Forge / player; voice content (Ideals, Bonds, Flaws, Personality traits, Appearance, Biography) preserved verbatim from Forge.
- **Notes** — Claude/GM annotations.

**Conflict resolution.** The AI brief is a pitch. The Forge sheet is the player's canonical character. When the brief contradicts Forge, **Forge wins** for mechanical facts. Update structured fields accordingly; keep Forge content verbatim in the Full sheet's voice sections; flag contradictions to the GM.

**IC-propaganda exception.** For some characters, the player-written Forge narrative (Ideals, Bonds, Flaws, Personality traits, Biography, Appearance) is in-character self-promotion rather than literal truth. When the GM flags this, the Forge content stays verbatim in the Full sheet, but a Notes line records the GM's read of who the character actually is, and the Concept reflects the GM-observed reality.

## Language

Curated sections (Goal, Current state, Concept, Notes, Signature, Secrets) are written in **English**.

The Full sheet preserves source language verbatim — if Forge / the AI brief had Spanish text, leave it Spanish under English headings.

**Identity-block standardization.** Five fields are normalized for cross-PC consistency rather than preserved verbatim:

- **Alignment** — English, title case (e.g., "Legal Neutral" → "Lawful Neutral").
- **Gender** — capitalized English (Male / Female / Nonbinary / etc.).
- **Age** — number only (years assumed); strip language-specific suffixes ("35 años" → "35").
- **Height** — `X' Y" (Z m)` format. Pure-feet values omit the inches part: `9' (2.74 m)`.
- **Weight** — `X lb (Y kg)` format.

Other Identity fields (Faith, Eyes, Hair, Skin) preserve source language verbatim.

## Misc

**Multiclass PCs** — list classes in **chronological order** (the class taken first comes first) in `class:` and in the Full-sheet snapshot line (e.g., "Snapshot at level 5 (Artificer 1 / Wizard 4)"). The first class determines saving-throw proficiencies, so order is mechanically meaningful.

**2024 nomenclature.** Use D&D 5e 2024 names for classes, subclasses, features, and feats — even when the AI brief or other input uses 2014 names (e.g., "Way of the Open Hand" → "Warrior of the Open Hand").

**Honor.** This campaign uses the optional Honor stat. Honor changes are tracked per session in `gm-NN.md` (numeric delta per PC) and surfaced allegorically in `saga-NN.md` per `/draft` rules (gm file spec — Honor row in *Boundary rules for ambiguous cases*) — the PC markdown does **not** carry the numeric Honor score.

**Proficiency Bonus** is a campaign-wide value, not a PC field. This table uses dice-based proficiency (`1D6` instead of the standard `+3` at level 5). Tracked in Foundry; changes on level-up — not in PC sheets.

## Workflow

**Always ask** for missing details before writing a PC file (player name, faction affiliations, alignment, languages, any field the user hasn't supplied). Do not invent placeholders silently.

## Why / how to apply

These conventions exist so all PC files have one consistent shape — recaps and faction reasoning can rely on a stable structure, and AI-generated background text stays isolated from authoritative game data.

Treat `campaign/pcs/_template.md` as the canonical structure; any deviation should be intentional and discussed first.
