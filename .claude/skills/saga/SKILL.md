---
name: saga
description: Draft the player-facing Spanish heroic-saga recap (`saga-<NN>.md`) from the GM-approved (accepted) `minutes-<NN>.md`. Operates on accepted canon only; if the minutes look unaccepted or incomplete, surfaces a clear error.
---

# /saga

Draft the player-facing recap from the GM-approved minutes. Operates on accepted canon only — the approved `minutes-<NN>.md` is the undisputed source of truth; the session transcript is never re-read.

## Output

`sessions/session-<NN>/saga-<NN>.md` — the player-facing canonical recap, written in **[Homebrewery v3](https://homebrewery.naturalcrit.com/) markdown** so the GM can paste it into Homebrewery and render a styled PDF. Spanish, single flowing prose, heroic-saga voice. **Target length: one Homebrewery page (~720–1080 words) only.** The default is one page — never more — unless the GM's `/saga` invocation explicitly requests a different page count (e.g., *"/saga 17, two pages"*). Absent that explicit ask, a two-page recap is a failure to compress, not a judgment call the skill gets to make. See [drafting-rules.md](drafting-rules.md#output-format) for the compression discipline; overshoot has been the recap-writer's demonstrated failure mode. The `.md` extension is retained for consistency with other session files; the *rendered* artifact is a PDF.

### File skeleton

```
# Sesión <N> {{float:"right" <DD Mes YYYY>}}
{wide}

{{wide _<DD Mes YYYY DR>_ }}

{{wide
<paragraph 1 prose>
}}

{{wide
<paragraph 2 prose>
}}

… (one {{wide ...}} block per paragraph)

{{pageNumber,auto}}
{{footnote Tiranía de Dragones | Sesión <N>}}
```

Header conventions:

- **Session number `<N>`** — no leading zero in the rendered output (e.g., `Sesión 1`, not `Sesión 01`). Folder/file paths still use the zero-padded form (`session-01/saga-01.md`).
- **Wide H1** — the `{wide}` single-brace injector sits on its own line directly below the H1 (no blank line between them). It applies the `wide` class to the heading element above it so the title spans the full page. This is distinct from the `{{wide ...}}` *block* used for the paragraphs: single braces inject a class into the preceding element; double braces open a styled block. Do **not** append `{{wide}}` to the end of the H1 line — that renders an empty wide span, not a wide heading.
- **Real-world date** — pulled from `minutes-<NN>.md`'s `date` frontmatter field; rendered in Spanish as `DD Mes YYYY` (capitalised month, no "de", e.g., `9 Febrero 2025`). Goes inside `{{float:"right" ...}}` so it sits in the H1's right margin.
- **In-fiction date** — pulled from `minutes-<NN>.md`'s `in_fiction_date` frontmatter field; rendered as `DD Mes YYYY DR` (e.g., `23 Marpenoth 1489 DR`); Faerûnian month names stay as-is. Wrapped in `{{wide _..._ }}` so it sits italic and full-width below the title.

Body conventions:

- **`{{wide ... }}` block per paragraph.** Narrative prose reads badly in Homebrewery's default two-column layout; each paragraph spans the page.
- **Bold (`**...**`) sparingly on dramatic peaks** — climactic reveals, key deaths / falls / revivals, nickname coinage, single-line setpiece moments. Aim for 3–5 per saga; not more.
- **Italics (`*...*`) on two things, sparingly otherwise:**
  - **Verbatim Spanish quotes** preserved from the minutes (in-fiction dialogue, NPC lines). The minutes already protect these verbatim; the recap renders them as `*"..."*`.
  - **Atmospheric grace notes** — closing-line lyricism, sensory beats, short reflective phrases. Aim for 2–4 per saga.
- **Per-saga footer** — `{{pageNumber,auto}}` followed by `{{footnote Tiranía de Dragones | Sesión <N>}}` at the foot of the file. If the saga overflows one rendered page in Homebrewery, the GM inserts `\page` at the break point and repeats the same `{{pageNumber,auto}}` + `{{footnote ...}}` pair on each page (manual judgment — the drafter doesn't predict page boundaries).

### Full-campaign brew

To rebuild the full-campaign brew (every saga concatenated into one Homebrewery file the GM can render to a single PDF):

```
python3 .claude/skills/saga/build_full_saga.py
```

This writes `sessions/outputs/full_saga.md` — the verbatim concatenation of every `saga-<NN>.md` separated by `\page` lines so each session starts on a new rendered page. Each saga's own internal `\page` breaks and per-page footers survive intact.

The `sessions/session-<NN>/outputs/` folder also holds the rendered PDFs the GM exports from Homebrewery. The `.md` source lives at the session root; everything derived from it lives under `outputs/`. The campaign-wide `sessions/outputs/` holds cross-session artifacts (the full-campaign brew, and the corresponding rendered PDF).

| File | Audience | Lifetime |
|---|---|---|
| `saga-<NN>.md` | GM (paste into Homebrewery → render PDF) | Canon — archived |
| `outputs/saga-<NN>.pdf` (or similar) | Players (rendered) | Derived — re-export from Homebrewery |
| `sessions/outputs/full_saga.md` | GM (paste into Homebrewery → render full-campaign PDF) | Derived — regenerable from the per-session `.md` files |

## Required inputs (ask if missing)

- **Session number** (NN) — the session folder under `sessions/` to draft from.

The session folder must already contain:

- `minutes-<NN>.md` — must carry `status: accepted` in its frontmatter. The recap is drafted from this.

**If `minutes-<NN>.md` does not exist, or the `status` field is missing / not `accepted`, surface a clear error and stop.** Do not draft against `drafted` minutes — that state means the GM has not yet signed off and the content is not canon.

## Before drafting

**Always gather context before drafting.** The recap is a distillation of the minutes, not a new authoring pass. **The approved minutes are the undisputed source of truth — never consult the session transcript.** If the minutes seem incomplete or contradictory, stop and surface to the GM (they can edit the minutes directly or re-run `/draft`); do not reach back into the transcript to fill gaps.

1. **Drafting rules** — read [drafting-rules.md](drafting-rules.md) end-to-end. Authoritative spec for the recap's output shape (voice, tense, length, exclusions, EPIC handling, Spanish conventions, final-pass checklist).
2. **Minutes file** — read `minutes-<NN>.md` end-to-end. This is the input the recap is drafted from.
3. **Reference samples — the two or three most recent validated sagas** (`sessions/session-<NN-1>/saga-<NN-1>.md`, `sessions/session-<NN-2>/saga-<NN-2>.md`, ...). Read them end-to-end before drafting. These are GM-approved, manually-corrected canon Spanish and are the **binding register anchor** for the new recap — match their tone, tense, paragraph rhythm, detail level, ornament level, and verb-noun collocations. [example.md](example.md) is a fallback only when no prior sagas exist (i.e., session 1). The drafter has a documented tendency to overshoot toward imagined-saga prose more ornate than the GM-validated baseline; the prior sagas are the calibration that prevents this.
4. **PC + NPC canon (digests)** — load `campaign/pcs/_context.md` + `campaign/npcs/_context.md`. These are the **default source** for species, class, gender, factions, nicknames, status, and (for PCs) signature / notable items. Regenerated by `python3 .claude/skills/draft/_regen_context.py` — deterministic, zero-LLM, safe to run unconditionally if any source file was recently edited.
   - Use **public-generic descriptors** (*el guerrero elfo*, *la pícara halfling*, *el paladín dragonborn*) only when the matching `species` / `class` / `background` / `factions` / `gender` field is populated in the digest.
   - Confirm which PCs carry `status: hidden` — their names must not appear in the recap (the minutes already render their actions as natural in-fiction observations; the recap inherits that as-is).
5. **PC source-file fallbacks** — read `campaign/pcs/<name>.md` only for sections the digest does not carry:
   - `## Concept` — when the recap renders a PC's voice, motive, or self-conception and the digest's signature / notable items aren't enough grounding.
   - `## Full sheet → ### Identity` / `### Appearance` — only when a specific descriptor the recap is about to render needs verification beyond the digest's public fields.
6. **NPC source-file fallbacks** — read `campaign/npcs/<name>.md` (frontmatter + opening paragraph) only when the digest is missing a beat-critical descriptor (role nuance, public allegiance shading, distinguishing appearance not captured by `species` alone).

## Drafting

Follow [drafting-rules.md](drafting-rules.md). It is the authoritative spec for the recap's output shape; everything below in this file is `/saga`-specific scaffolding (identity sources, review passes) that complements those rules.

**Identity sources for `/saga`** (used by drafting-rules.md's *Cast naming and identity* section):

- **PC identity** → `campaign/pcs/_context.md` digest is the default source (frontmatter: species, class, gender, factions, nicknames, status; plus signature + notable items). Fall back to `campaign/pcs/<name>.md ## Concept` for character voice, or `## Full sheet → ### Identity` / `### Appearance` when a specific descriptor needs verification beyond the digest's public fields.
- **NPC identity** → `campaign/npcs/_context.md` digest is the default source. Fall back to `campaign/npcs/<name>.md` (frontmatter + opening paragraph) only when the digest lacks a beat-critical descriptor.

**Descriptor sourcing rule.** A PC's public species / class / background from their PC file is fair game in the recap, even if the minutes don't explicitly reuse the descriptor — calling Eguzkilore *"el guerrero"* or *"el elfo"* is fine because Fighter and Wood Elf are his public class and species.

**Gloss budget — atmospheric detail permitted.** Saga's gloss budget is wider than minutes' — it permits **info-adding** (introducing in-fiction detail beyond what the minutes establish: weather, time-of-day texture, sensory beats, NPC micro-reactions) **provided the addition respects the minutes' tale** — no contradicting, no modifying, no inventing facts that would override the minutes' canon. See [feedback_gloss_budget.md](../../memory/feedback_gloss_budget.md) for the rephrasing-vs-info distinction.

## Review passes

**Pass 1 — Minutes-trace audit.** Apply the [Minutes-trace audit](drafting-rules.md#minutes-trace-audit) from drafting-rules.md. Go through the draft sentence by sentence and name, for each clause, the minutes scene + beat it came from. Anything that cannot be cited is invention — rewrite to match the minutes, or cut. This pass is first because if a beat shouldn't exist, no other audit matters. Apply fixes before Pass 2.

**Pass 2 — Filter check.** Apply the [final-pass checklist](drafting-rules.md#final-pass-before-delivery) from drafting-rules.md. Additional `/saga`-specific check:

- **Descriptors traced** — every PC/NPC species / class / background / appearance reference matches the *public* fields of the PC or NPC file.

**Pass 2.5 — Idiomatic-Spanish audit.** Apply the four heuristics from drafting-rules.md's [Idiomatic-Spanish audit](drafting-rules.md#idiomatic-spanish-audit) section, sentence by sentence:

- **No bare English game terms in plain prose** (*Guidance*, *Command*, *Fire Bolt*, *Sacred Flame*, *Action Surge*, *Rage*, etc.) — paraphrase as the in-fiction effect, or italicize as a foreign term. Saga voice prefers paraphrase.
- **Translator-shape sentences get rewritten from native-Spanish thought** — if the Spanish word order, phrasing, or word choice maps phrase-for-phrase onto the English source (*the trap springs* → *la trampa salta*, *from cover* → *desde cobertura*, *in a burst of* → *en una ráfaga de*, *the party retreats* → *la partida se retira*), rewrite the thought from scratch in Spanish, not the English mirror. Single-word calques count: a Spanish word with the right denotation but wrong sense for the context (e.g., *partida* for an adventuring group, on the model of English *party*) is the same failure mode.
- **Register consistency** — flag and rewrite phrases that break the *grounded heroic* register in either direction (too archaic: *sendas*, *poterna*, *empero*; too urban/modern for a medieval setting: *azotea* for a keep, *cuarto* for a fortress chamber).
- **Forced-literary collocations** — grammatical phrases that read as imagined-saga prose rather than written-Spanish prose because the verb and noun don't collocate naturally (e.g., *tender un susurro*, *florece una espada*, *amasa un puñado de bayas*). Default to ordinary verbs; cap anthropomorphic flourishes at one per scene. See drafting-rules.md for the full set of patterns.

The drafter is not a native Spanish speaker; this pass exists because first-pass renderings tend to be word-for-word translations that read as translator-prose. Treat the audit as mandatory — when uncertain on a phrase, surface two or three rewrite options to the GM rather than committing. Apply fixes before Pass 3.

**Pass 3 — Narrative pass.** Read the recap as story, not as a list of events. Check:

- **Pacing.** Combat scenes are outcome-focused, not blow-by-blow. The session's biggest beat lands with rhythm and detail proportional to its stakes; minor scenes don't bloat. A slow paragraph at a tense moment kills the tension; a rushed paragraph at the climax wastes it.
- **Causality.** Each transition between paragraphs has a *why*. *"Y entonces"* doesn't carry causal weight on its own — the connective tissue (decisions, consequences, in-fiction reactions) makes one event lead to the next. If two adjacent paragraphs feel disconnected, add the causal link from the minutes or merge them.
- **Climactic weight.** The session's climax (the duel, the rescue, the betrayal — whatever the minutes build toward) gets the prose space it deserves. If the climax is a single sentence, something's wrong; rewrite to give it room.
- **Paragraph purpose.** Each paragraph earns its space — it carries new ground, a turn, or an emotional shift. A paragraph that just continues describing what the previous one started should be merged or cut.
- **Tension shape.** The recap reads as having rising tension, climax, and resolution — even if the the minutes' beat sequence is messy. The drafter shapes within paragraphs (and across paragraph breaks) to make the arc visible.

If a check fails, rewrite the affected passages. Apply fixes before Pass 4.

**Pass 4 — Cold read.** Read the recap as a player who wasn't at the table. Are NPCs, locations, items, and prior-session references self-explanatory or do they assume context the reader doesn't have? Does each beat land without consulting the minutes? Trim, clarify, and tighten.

**Pass 5 — Page-fit check.** Render a WIP PDF and verify the saga fits a single Homebrewery page:

```
python3 .claude/skills/render_pdf.py sessions/session-<NN>/saga-<NN>.md --wip
```

This writes `sessions/session-<NN>/outputs/S<NN> - Saga_WIP.pdf` — the `_WIP` suffix keeps the drafting-time render separate from the canonical `S<NN> - Saga.pdf`. Read the WIP PDF back and look for overflow: a final paragraph that truncates mid-sentence, text bleeding into the footer ribbon, or a last line sitting flush against (or past) the ornamental border all mean the content runs long. If overflow, compress per [drafting-rules.md § length](drafting-rules.md#output-format) (merge paragraphs, trim atmospheric detail, shorten sentences) and re-run `--wip` until the final line ends with a visible gap above the footer. Pypdf reporting `Pages: 1` is not sufficient — the headless renderer forces a single Letter page and clips what doesn't fit; verify visually. The `_WIP` file is drafting scratch — delete it (or let the next `/saga` run overwrite it) once the GM accepts the saga.

## Reference

[sessions/README.md](../../../sessions/README.md) carries the directory layout and pipeline orientation. The output-shape rules live in [drafting-rules.md](drafting-rules.md).
