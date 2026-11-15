---
name: translate
description: Translate accepted `minutes-<NN>.md` into Spanish, producing `resumen-<NN>.md` — a faithful but natural literary translation that preserves Homebrewery markup and the campaign's established Spanish glossary. After the first pass, dispatches three parallel review subagents (fidelity, idiom/naturalness, glossary) in a single message to catch translation errors in clean context, then renders the PDF. Use whenever the GM asks for a Spanish version, translation, "resumen", or "apuntes" of a session's minutes, or wants the Spanish counterpart to the English minutes file.
---

# /translate

Translate the GM-accepted `minutes-<NN>.md` into Spanish. The output, `resumen-<NN>.md`, carries the same facts, cadence, and author intent as the minutes — rendered in literary Spanish that matches the register the campaign's existing sagas have established.

**Operates on accepted canon only.** The minutes file is the undisputed source of truth; the session transcript is never re-read. The Spanish artifact is a translation, not a re-draft — the drafter's job is to render the minutes faithfully, not to reinterpret them.

## Output

`sessions/session-<NN>/resumen-<NN>.md` — Spanish translation of the minutes, no YAML frontmatter. (Status is tracked on the English `minutes-<NN>.md`; `resumen-<NN>.md` is a derived artifact and does not carry a separate status field.)

Rendered PDF: `sessions/session-<NN>/outputs/S<NN> - Resumen.pdf` (produced by `render_pdf.py`, which has `resumen-<NN>.md` in its `ROLE_PATTERNS`).

## Required inputs

- **Session number** (NN).
- `sessions/session-<NN>/minutes-<NN>.md` — must exist and carry `status: accepted` in its frontmatter.

### Pre-flight (stop if any fails)

1. If `minutes-<NN>.md` does not exist, or the `status` field is missing / not `accepted`, surface a clear error and stop. A `drafted`-status minutes file is not canon yet and must not be translated.
2. If `resumen-<NN>.md` already exists at the target path, overwrite it. The skill runs unattended given only `<NN>` — no confirmation prompts. Overwrites are recoverable from git; name the overwrite in the completion report so the GM can diff if they want to see what changed.

## Before translating

1. **Read `minutes-<NN>.md` end-to-end.** This is the single source of truth. Note the Homebrewery markup, scene structure, per-bullet content, EPIC markers, bold names, italic timestamps.
2. **Read the two most recent sagas** — `sessions/session-<N-1>/saga-<N-1>.md` and `sessions/session-<N-2>/saga-<N-2>.md`. These are GM-validated Spanish and the **binding register anchor**: match their tone, cadence, verb-noun collocations, and glossary. They tell you what the campaign's Spanish actually sounds like when the GM has signed off on it.
3. **Skim the Glossary section below** before writing any bullet so established term choices are fresh.

## Translating

Translate scene by scene, bullet by bullet. The structure is mechanical; the prose is where judgement lives.

### Structural preservation

Copy these verbatim — do not localise, re-order, or embellish:

- All Homebrewery markup: `{wide}`, `\column`, `\page`, `{{float:"..." ...}}`, `{{pageNumber,auto}}`, `{{footnote ...}}`.
- Scene header count, order, and numbering (`## 1 - ...`, `## 2 - ...`).
- Numbered-bullet count per scene — if the English has eight bullets in a scene, the Spanish has eight, in the same order.
- `***[EPIC]***` markers — same bullet position, same emphasis form.
- Bold on character / NPC names (`**Name**`) — same names, same positions. Names themselves are not translated.
- Italics on in-fiction timestamps (`_~12:00, 23 Nightal 1489 DR_`) and on in-fiction quoted speech or magical-message text.

### Translation-specific substitutions

- **Session title**: `# Session <N>` → `# Sesión <N>`. Preserve the `{{float:"right" <date>}}` injector verbatim (the real-world date stays as the ISO `YYYY-MM-DD` form the minutes carry — matches the Homebrewery convention the existing files use).
- **Scene titles**: translate idiomatically, following the register of the saga corpus (*"Dangerous breakfast"* → *"Desayuno peligroso"*, *"Whispers from a box"* → *"Susurros de una caja"*).
- **Footnote**: `{{footnote Tyranny of Dragons | Session <N>}}` → `{{footnote Tiranía de Dragones | Sesión <N>}}`.
- **YAML frontmatter**: drop entirely. The output starts with `# Sesión <N> ...`.

### Register and voice

Match the campaign's existing sagas: present-tense narration, grounded-literary, dramatic on the peaks but never purple on the valleys. The minutes' register is slightly drier than the saga's — translate the minutes' register, not the saga's. Think of it as *saga-adjacent*: the same vocabulary and sentence shapes, but holding to the minutes' bullet-list cadence and factual tone.

**Avoid translator-shape sentences.** When a bullet reads like a calque (prepositions mapping 1:1, idioms transliterated, verb-noun pairs that don't collocate in native Spanish), rewrite the thought from scratch in Spanish rather than editing the calque — the English skeleton under a Spanish surface is the drafter's default failure mode.

### Glossary — proper nouns and campaign terms

Grep `sessions/session-*/saga-*.md` to confirm precedent for anything uncertain. Do not guess.

**Preserve untranslated** (proper nouns): all PC names (Eguzkilore, Mialee, Nuberroca, Nyx, Sinsong, Amidamaru, Kaelthar, Targutai, etc.); all NPC names (Elodin, Enki, Jamna, Arietta, Zelina, Darla, Gus, Carlon, etc.); Faerûnian calendar months (Nightal, Marpenoth, Eleasis, etc.); Forgotten Realms place names (Daggerford, Waterdeep, Greenest, etc.); the Dale Reckoning year marker (`1489 DR`).

**Translated with established renderings:**

| English | Spanish |
|---|---|
| Trade Way | Camino del Comercio |
| Company of the Boar | Compañía del Jabalí |
| Order of the Gauntlet | Orden del Guantelete |
| Tyranny of Dragons | Tiranía de Dragones |
| Session N | Sesión N |
| Lady Dragon | Señora Dragón |

**D&D race / class / role terms**: *halfling* → *mediana* (f.) / *mediano* (m.); *goliath* → *goliath* (preserved); *dwarf* → *enano/a*; *elf* → *elfo/a*; *tortle* → *tortle* (preserved — corpus established the loanword, not *tortuga*); *barbarian* → *bárbaro/a*; *cleric* → *clérigo/a*; *cultist* → *cultista*; *gnome* → *gnomo/a*. Use the gendered form the character takes in the campaign.

**Preserve source styling, always.** Capitalisation, italics, and bold on any word or phrase are inherited from the English source — never added, never dropped, never overridden by corpus precedent. If the English minutes write `Lady Dragon` plain, the Spanish writes `Señora Dragón` plain. If the English italicises `*Castle Naerytar*`, the Spanish italicises `*Castillo Naerytar*`. If a prior saga rendered the same term differently (lowercase, italicised, whatever), the source wins — the saga corpus is a register anchor, not a style override. This rule covers titles, epithets, spell names, place names, in-fiction quotes, and anything else the drafter might be tempted to restyle.

**Weapons and gear**: *halberd* → *alabarda*; *scimitar* → *cimitarra*; *crossbow* → *ballesta*; *crossbow bolt* → *virote de ballesta*; *shackles* → *grilletes*; *gag* → *mordaza*; *breastplate* → *peto*.

**Spells**: render with the Spanish conventional name — *Message* → *Mensaje*, *Zone of Truth* → *Zona de Verdad*, *Sleep* → *Sueño*, *Heroism* → *Heroísmo*, *Command* (the verb form) → italicised Spanish verb (*venir* / *ven*) matching how the minutes italicise the command word. Match the source's capitalisation: capitalise when the English minutes capitalise the spell as a proper noun (*the Sleep*); lowercase when the minutes use it as a common verb (*casts slumber*).

**Modern-RAE orthography**: do not accent demonstrative pronouns (*este*, *ese*, *aquel*). `sólo` as adverb is permitted — it appears in the saga corpus and is the campaign's established style.

## Review passes

Once the first-pass translation is written to `resumen-<NN>.md`, dispatch **three review subagents in a single assistant message** — all three Agent tool calls fire in parallel, each in fresh context. The clean-context separation matters: the drafter has already committed to its translation choices, and a second look in the same context tends to confirm the first pass rather than catch its mistakes.

Use `subagent_type: general-purpose` for each. Below are the exact prompt templates; substitute `<NN>` and `<N-1>` / `<N-2>` concretely before dispatch.

### Pass 1 — Fidelity (Agent, general-purpose)

> Review the Spanish translation of a D&D session recap for **fidelity to the English source**.
>
> Read both files end-to-end:
> - Source (English): `sessions/session-<NN>/minutes-<NN>.md`
> - Translation (Spanish): `sessions/session-<NN>/resumen-<NN>.md`
>
> Walk through each numbered bullet in order. For each bullet, verify every content noun / verb / adjective in the Spanish traces to something in the English. Flag:
> - **Added information** — detail present in Spanish but absent in English.
> - **Dropped information** — detail present in English but absent in Spanish.
> - **Meaning drift** — a word or clause that renders the English with a different sense (e.g., *crossbow bolt* translated as *arrow*; *backswing* translated as *downswing*; a declaration cited as an outcome).
>
> Also verify the Homebrewery markup matches structurally:
> - Same count and order of `##` scene headers.
> - Same count and order of numbered bullets within each scene.
> - `{wide}`, `\column`, `\page`, `{{pageNumber,auto}}`, `{{footnote ...}}` present in the same positions.
> - `***[EPIC]***` markers on the same bullets.
> - Bold `**Name**` emphasis on the same character names in the same positions.
> - Italic `_timestamp_` present at the top of the same scenes.
>
> **Report format**: a numbered list of findings. Each finding: scene.bullet, the English span, the Spanish span, the kind of break (added / dropped / drift / markup), and the minimal-edit fix. Keep findings fact-level, not stylistic — stylistic concerns belong to a different pass. If a scene is clean, write "Scene N — clean." If there are no findings at all, write "No fidelity breaks found."

### Pass 2 — Idiom and naturalness (Agent, general-purpose)

> Review the Spanish translation of a D&D session recap for **idiomatic Spanish and naturalness**.
>
> Read:
> - Translation (Spanish): `sessions/session-<NN>/resumen-<NN>.md`
> - Register anchors: `sessions/session-<N-1>/saga-<N-1>.md` and `sessions/session-<N-2>/saga-<N-2>.md` (the two most recent GM-validated Spanish files).
>
> Read the Spanish as a native speaker would. Flag:
> - **Calques from English** — word-for-word renderings where the Spanish is grammatical but reads as translator-prose (e.g., *break for the hills* → *rompen hacia las colinas*; *in a burst of* → *en una ráfaga de*).
> - **Awkward phrasing** — grammatically correct but odd word order, cluster, or preposition choice.
> - **Incorrect preposition** — wrong connector for the verb.
> - **Verb-tense inconsistency** within a scene — flipping between preterite and present without reason.
> - **Register drift** — phrasing too modern, too archaic, or too clinical for the saga register the two anchors establish.
>
> **Do NOT flag** stylistic choices that already appear in the saga corpus — those are the GM-validated register. If you're unsure whether a phrasing is a calque or an accepted stylistic choice, grep the saga files before flagging. If the phrasing has precedent in the corpus, don't flag it.
>
> **Report format**: a numbered list of findings. Each finding: scene.bullet, the current Spanish, a suggested rewrite, and one sentence on why the current reads as non-native. If there are no findings, write "No naturalness flags."

### Pass 3 — Glossary consistency (Agent, general-purpose)

> Review the Spanish translation of a D&D session recap for **glossary consistency with prior campaign artifacts**.
>
> Read:
> - Translation (Spanish): `sessions/session-<NN>/resumen-<NN>.md`
> - Source (English): `sessions/session-<NN>/minutes-<NN>.md`
> - Corpus precedent: `grep` across `sessions/session-*/saga-*.md` for any term you're uncertain about.
>
> Verify these conventions:
> - **Proper nouns preserved untranslated**: PC names, NPC names, Faerûnian calendar months (Nightal, Marpenoth, Eleasis, etc.), Forgotten Realms place names (Daggerford, Waterdeep, Greenest, etc.), the `DR` year marker.
> - **Campaign-specific translations fixed**:
>   - Trade Way → Camino del Comercio
>   - Company of the Boar → Compañía del Jabalí
>   - Tyranny of Dragons → Tiranía de Dragones
>   - Session N → Sesión N
> - **Footnote form**: `{{footnote Tiranía de Dragones | Sesión <N>}}` — exact wording and separator.
> - **D&D terminology**: halfling → mediana/mediano; halberd → alabarda; scimitar → cimitarra; crossbow → ballesta; shackles → grilletes; gag → mordaza; breastplate → peto.
> - **Spell names**: use Spanish conventional names — *Mensaje*, *Zona de Verdad*, *Sueño*, *Heroísmo*. Match source capitalisation (uppercase when English uses the spell as a proper noun; lowercase when used as a verb).
>
> For any convention you're uncertain about, grep the saga corpus before flagging. Report what precedent (if any) says.
>
> **Report format**: a numbered list of findings. Each finding: scene.bullet, the English term, the current Spanish rendering, the established Spanish rendering (with a precedent citation when relevant), and the fix. If nothing to flag, write "No glossary breaks."

### After the three reports

Apply **all findings from all three passes** automatically. Pass 1 (fidelity) and Pass 3 (glossary) findings are facts; Pass 2 (naturalness) findings are a native-speaker's read of the prose and have been reliable in practice — applying them all gives the GM a cleaner draft to review than leaving the drafter's first-pass translator-prose in place. The GM's final editorial pass on the file is the backstop; the skill does not gate itself on their input here.

If a Pass 2 finding directly conflicts with a Pass 1 or Pass 3 finding (rare — e.g. Pass 2 suggests a rewrite that drops a term Pass 3 requires), the fact wins. Note the conflict in the completion report so the GM can revisit if desired.

Keep an internal count of findings applied per pass; report them in one line each at the end.

If all three passes report "no findings", skip straight to render.

## Render PDF

After accepted edits land in `resumen-<NN>.md`:

```
python3 .claude/skills/render_pdf.py sessions/session-<NN>/resumen-<NN>.md
```

This writes `sessions/session-<NN>/outputs/S<NN> - Resumen.pdf`. `render_pdf.py` has `resumen-<NN>.md` in its `ROLE_PATTERNS` list, so no custom wrapper is needed.

## Layout check

Spanish is typically 20–30% longer than English; the same Homebrewery markup that fit the English source can push the Spanish past its column or page. Run the layout check immediately after render:

```
python3 .claude/skills/check_layout.py \
    sessions/session-<NN>/minutes-<NN>.md \
    sessions/session-<NN>/resumen-<NN>.md
```

The check renders both files, compares per-scene geometry, and treats the source as the ground-truth layout. It reports three failure modes:

- **`title wrap`** — a scene title renders taller than the source's; the Spanish title line-broke. Shown as `page N — scene '…': title wraps … → shorten the title`.
- **`column shift`** — a scene's title x-position in the translation sits one column further right than in the source. Shown as `page N — scene '…': shifted <px>px right (one column over) → tighten '<root-cause-scene>'[, '<another>'…]`. **The `→ tighten` names the scenes to shorten — not the shifted scene itself.** The shifted scene is downstream of the real cause (the preceding scene that overflowed its column and pushed everything over).
- **`page overflow`** — the final scene on a page extends past the page's bottom edge. Shown as `page N — content past page bottom … → tighten any of: '<root-cause-scene>'[, …]`.

Exit 0 and you're done — report the PDF path and stop.

### Why the check points at a different scene than the one that flagged

When Homebrewery lays out a `\column`-split page, the `\column` directive pushes content to *the next column after wherever the preceding content ended*. If the preceding scene (e.g. scene 1) was supposed to fit column 1 but ran one line long, `\column` doesn't push scene 2 into column 2 — it pushes scene 2 past column 2 into a nonexistent column 3, which gets clipped by `page.pdf()`. Shortening scene 2 would not help. Shortening scene 1 by one line gives scene 1 its column back and lets scene 2 land in column 2.

Flow pages (no `\column`) have the same dynamic: on page 2 of a typical minutes file, scenes 3, 4, 5 flow across two columns. If scene 5 ends up pushed into a third column, the cause is that scenes 3 and 4 *together* exceed column 1's capacity. Either (or both) can be shortened to resolve it; the check names both.

### What to tighten

**Scene prose**: tighten *without changing the content meaningfully*. The scene's facts, names, dialogue, EPIC markers, and bold/italic emphasis positions stay; the prose carries the same information in fewer words.

**Tightening heuristics for scene prose** (apply only what the root-cause scene needs):

- **Drop discourse markers that carry no information** — *entonces*, *luego*, *también*, *además*, *ya*, *otra vez* / *de nuevo* when the beat is already clear without them.
- **Collapse periphrastic verbs** — *está + gerundio* → simple present (*está lanzando* → *lanza*); *va a + infinitivo* → simple future or present with time marker.
- **Replace multi-word phrases with single words** when meaning is preserved — *en el momento en que* → *cuando*; *a lo largo de* → *por*; *con el fin de* → *para*.
- **Trim decorative adverbs** — *todavía*, *aún*, *muy*, *incluso*, *propio/a* in weak positions, *mismo/a* when redundant.
- **Elide function words** the Spanish allows to drop — definite articles in list / headline / stage-direction contexts; prepositional *de* where juxtaposition reads native.
- **Drop re-establishing descriptors** on later mentions of the same NPC within a scene (e.g. *el cultista cabecilla* → *el cabecilla* on the third mention within scene 1).

**Scene titles**: rewrite freely. Scene titles are decorative labels — autogenerated by `/draft`, rarely consulted by players, carry no fidelity constraint. Drop articles, swap for shorter synonyms, abbreviate the beat, or replace the whole title with a shorter one. The only test is that someone scanning the recap can tell which scene it is.

**Never**:

- Drop or modify any proper noun (PC, NPC, location, faction).
- Drop or modify a fact, number, or outcome from the scene prose.
- Change dialogue content or alter quoted Spanish.
- Remove an EPIC marker or move it.
- Change the position of bold / italic emphasis.
- Touch Homebrewery markup (`\column`, `\page`, `{{...}}`).

### Tighten-and-reloop

The skill runs this loop autonomously — no user input between iterations.

1. Read the check's findings. For each one, apply the fix the finding's `→` arrow names:
   - **`title wrap`** → shorten the named scene's title.
   - **`column shift`** → tighten the prose of every scene listed after `→ tighten` (multiple scenes = any or all of them contribute; tightening more than one compounds).
   - **`page overflow`** → tighten the prose of any scene listed after `→ tighten any of`.
2. Re-run `render_pdf.py` and `check_layout.py`.
3. Repeat. **Cap at 3 iterations.**

If findings still persist after three rounds, don't block on GM input — complete the run, keep the PDF the third render produced, and name the remaining findings in the completion report. The GM's editorial pass is the backstop; they can rerun `/translate <NN>` after editing the minutes, add a `\page` break manually, or accept the overflow. Burning more iterations risks stripping fidelity for diminishing layout returns.

## Completion report

End the run with a compact status block the GM can scan:

```
→ sessions/session-<NN>/resumen-<NN>.md (overwritten / new)
→ sessions/session-<NN>/outputs/S<NN> - Resumen.pdf
   fidelity: N edits applied | naturalness: N applied | glossary: N applied
   layout: clean | needed N iterations | unresolved after 3 iterations: <findings>
```

One line per piece of information. No prose. The GM reads this in a glance.

## Reference

- **Register anchor**: the two most recent `saga-*.md` files in `sessions/session-*/`.
- **Language convention**: [`feedback_language.md`](../../memory/feedback_language.md) — Spanish for transcripts / recaps.
- **Orthography**: Spanish content follows RAE standard; the British-English memory does not apply.
- **Worked example**: session 26 (`sessions/session-26/minutes-26.md` → `sessions/session-26/resumen-26.md`) — the first validated run of this skill, produced before the skill existed and used to calibrate its rules.
