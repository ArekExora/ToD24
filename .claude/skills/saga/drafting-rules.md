# Recap drafting rules

These rules govern the player-facing recap drafted from an approved session minutes by [`/saga`](SKILL.md). They describe **the recap's output shape** — voice, exclusions, EPIC handling, Spanish conventions, the final-pass checklist. I/O contract (which files the drafter reads) is owned by `/saga`'s SKILL.md, not here.

## Output format

- **Language:** Spanish.
- **Length: one Homebrewery page (~800–1200 words) is the target, not the ceiling to press against.** The recap is a distillation, not a summary — a 3-hour session that produced a 3000-word minutes file collapses to one page. Most minutes beats stay silent in the recap; only load-bearing ones make it. A saga running to two rendered pages needs an explicit justification (a session with two or three distinct climaxes, a major faction reveal that changes the campaign shape, etc.) — the default is one page. **Overshoot is the drafter's demonstrated failure mode.** Historical drift: S1–S4 landed at 750–1200 words (correct); S5 onward climbed steadily to 2000–2400 (too long — each saga became the anchor for the next, compounding the drift). When a paragraph reads "this beat is nice colour but not load-bearing," cut it. When two paragraphs cover the same arc (setup + resolution), merge them into one. Aim to leave the reader wanting the next line, not looking for the end.
- **[Homebrewery v3](https://homebrewery.naturalcrit.com/) markdown** — the file is meant to be pasted into Homebrewery's editor and rendered to PDF. See [SKILL.md → Output](SKILL.md#output) for the full file skeleton (H1 with floated date, per-paragraph `{{wide ...}}` blocks, foot with `{{pageNumber,auto}}` + `{{footnote ...}}`).
- **Emphasis (`**bold**` / `*italics*`) is allowed but rationed.** Use sparingly — see SKILL.md's body conventions for the exact rules: bold on dramatic peaks (3–5 per saga), italics on verbatim Spanish quotes from the minutes and on a few atmospheric grace notes (2–4 per saga). The prose still carries the saga on its own; emphasis is a marker, not a crutch. If a sentence needs bold to land, rewrite the sentence first.
- **Verbatim Spanish quotes from the minutes are wrapped in `*italics*`** (e.g., `*"esperaba a un grupo de héroes, no me han pagado para esto."*`). The italics signal "this is a memorable in-fiction line" to the reader; the wording inside is unchanged from the minutes.
- **No other Markdown structure.** No headers beyond the H1 title, no bullet lists, no tables, no blockquotes, no horizontal rules. The body is one flowing prose narrative wrapped paragraph-by-paragraph in `{{wide ...}}` blocks.
- **Structure:** single flowing prose narrative; paragraphs separated by blank lines. The minutes' `## Scene N` headers map loosely to recap paragraphs — the drafter may merge adjacent scenes, **merge several minutes beats into a single sentence or passage**, or split a long scene at a natural beat for narrative rhythm, but **never reorders events**. Chronology is preserved at the **event** level, not the beat level: nothing from scene 4 may appear before scene 3, but multiple scene-3 beats can flow together in one passage.

## Voice

- **Third-person omniscient narrator.**
- **Tense:** narrative present (historical present) — Spanish saga style. Present for session events; past only for things that happened *before* this session.
- **Tone:** heroic-saga, grounded — flowing oral-epic narration, not a checklist of beats. Dramatic flourishes mark turning points (*"la marisma no perdona"* style); connective tissue (causality, consequence, in-fiction reactions) carries prose between them. Vary sentence rhythm: long multi-clause sentences with embedded imagery for narrative passages, short sentences reserved for climactic moments or impact. If three sentences in a row share a subject-verb-object pattern, rewrite for rhythm.
- **Register anchor: validated prior sagas are binding for voice, not for length.** The adjectives above ("heroic-saga, grounded") are an approximation. The authoritative target for **voice, tense, rhythm, ornament level, verb-noun collocations** is the **two or three most recent validated `sessions/session-<NN>/saga-<NN>.md` files** — these are GM-approved, manually-corrected Spanish. [example.md](example.md) is a fallback only when no prior sagas exist. Before drafting, read those prior sagas and sample sentences aloud — that rhythm is what the recap must hit. **But do NOT anchor length on the prior sagas.** Recent sagas have drifted long (S5–S12 run 1800–2400 words, roughly double the target); using them as a length calibration compounds the drift. Length calibration comes from the one-page rule in *Length* above, not from prior-saga word counts. If a draft sentence reads as more literary, more poetic, more telegraphic, or more ornate than the prior sagas, it overshoots the register; rewrite simpler. When in doubt between "more grounded" and "more epic", pick more grounded.

## The minutes as canon

- The minutes are the undisputed source of truth. **Beats and dialogue** must come from the minutes — never invent, modify, or contradict them. **Atmospheric detail** (weather, time-of-day texture, sensory beats, NPC micro-reactions) may be added under saga's gloss budget, but only when the addition respects the minutes' tale (no contradicting or modifying minutes facts). See [feedback_gloss_budget.md](../../memory/feedback_gloss_budget.md) for the rephrasing-vs-info test.
- **Render the minutes at face value.** Recurring details (a blue glow on cuts, an unexplained warmth after a rest, a strange wind) appear as plain observations — not riddles, mysteries, or anything that telegraphs hidden agency. Forbidden phrasings: *"sin explicación"*, *"sin que nadie la reclame"*, *"como si alguien..."*, *"que nadie reconoce"*, and similar nudges. The reader notices recurring detail on their own; the prose never editorializes on it.
- **Memorable Spanish lines from the minutes stay verbatim**, in quotes. The minutes preserve them in Spanish for this purpose — do not translate, paraphrase, or polish.
- **In-fiction reactions from the minutes** — praise, critique, or commentary spoken at the table by a player or NPC — are dialogue, not editorialization. They belong in the recap when they carry a beat.
- **EPIC tags are production metadata.** Beats prefixed `[EPIC]` in the minutes carry the session's peak beats (applied by `/draft`, curated by the GM during manual review). **Strip the literal `[EPIC]` text** — it never appears in the recap. The tagged beat itself is presumptively load-bearing and should land in the recap with prose weight proportional to its stakes, unless rendering it would violate another rule.

## Cast naming and identity

- **Descriptors used in the recap (species, class, background, gender, appearance) must trace to public-facing identity references** available to the drafter. Anything not anchored in those references is invention — forbidden.
- **Hidden NPCs are never named.** The minutes already render their actions as natural in-fiction observations (the misattribution lives in the minutes); the recap inherits that as-is.


## Spanish translations and conventions

These are the GM's stylistic standards for the campaign — most are subtle distinctions that affect tone or precision in Spanish but are easy to miss without correction. This table is the single source of truth; the rules apply to the recap only (Spanish output). Minutes / gm / triage stay in English with imperial units verbatim, since those are canonical D&D distances.

| English (source) | Use (Spanish) | Don't use | Reason |
|---|---|---|---|
| drake (e.g. *guard drake*, *ambush drake*) | **draco** (*draco de presa*, *draco emboscador*) | dragón | A drake is not a dragon — it's a separate creature category. Calling it *dragón* misclassifies the creature for the player. |
| ambusher / hidden cultist | **cultista oculto** (pl. *cultistas ocultos*) | emboscado | *Emboscados* in Spanish reads as "people who got ambushed," the wrong direction. Use *ocultos* for hidden attackers. |
| sally port | **postigo** | poterna | *Poterna* exists but reads stilted/archaic. *Postigo* is the natural Spanish for the small sortie-gate. |
| dragonborn / draconic | **dracónido / dracónida** | dragónido / dragónida | Standard Spanish 5e canon spelling uses *dracónido* (with c). |
| goliath (species name) | **goliath** (untranslated, lowercase) | goliat | Keep the species name in English; *goliat* sounds like the biblical name and reads off-tone for the species. |
| imperial units (feet, pounds, miles) | **metric** (metros, kilos, kilómetros) | pies, libras, millas | *"siete pies"* in Spanish reads as "seven legs/feet (body part)." Convert at draft time (e.g., 7 ft → *más de dos metros*, 50 ft → *unos quince metros*). |

### Idiomatic-Spanish audit

The drafter is not a native Spanish speaker. Default first-pass renderings tend to be word-for-word translations of the English source — grammatical Spanish, but reads as translator-prose to a native ear. The drafter has been shown to spot these issues on review when explicitly asked, but doesn't catch them on first draft. This audit makes the question explicit: *"does this read as Spanish-native, or as English-translated?"*

Apply the four heuristics below to **every sentence** of the draft, in order. Each one targets a distinct failure mode the drafter has demonstrably produced. When a heuristic fires, rewrite the sentence — do not soften, do not leave a "best-effort" version. The audit is mandatory before delivery; budget the extra drafting time.

1. **No bare English game terms in plain prose.** D&D mechanic names (*Guidance*, *Command*, *Fire Bolt*, *Spare the Dying*, *Mage Hand*, *Sacred Flame*, *Second Wind*, *Action Surge*, *Rage*, *Bless*, *Cure Wounds*, etc.) must not appear unitalicized in the Spanish narration. Two valid renderings:
   - **Paraphrase the in-fiction effect** (preferred for saga voice): *Guidance* → *un susurro de guía sobre el oído de Mialee*; *Command* → *una orden mágica que dobla la voluntad del goliath*; *Fire Bolt* → *un dardo de fuego*; *Spare the Dying* → *un gesto que sostiene el pulso del moribundo*; *Action Surge* → *un arrebato que le concede una segunda andanada de golpes*.
   - **Italicize as a foreign term** (use sparingly — saga voice prefers paraphrase): *bajo un susurro de* Guidance → italics on the term only.
   The drafter must pick one of these two; it must not leave the bare English term in plain prose.

2. **Translator-shape sentences get rewritten from native-Spanish thought.** If a sentence's word order, phrasing, or word choice maps phrase-for-phrase onto the English source — *the trap springs* → *la trampa salta*, *from cover* → *desde cobertura*, *in a burst of* → *en una ráfaga de*, *grapples and throws* → *atrapa y lo lanza*, *separates toward* → *se separa hacia*, *parts cleanly* → *parte limpio*, *the party retreats* → *la partida se retira* — rewrite the thought from scratch in Spanish, not the English mirror. The native-Spanish version may use a different verb, a different word order, or a different metaphor entirely — that's the point. **Single-word calques count too**: a Spanish word with the right denotation but the wrong sense for the context (e.g., *partida* for an adventuring group, on the model of English *party*) is the same failure mode as a translator-shape sentence. Examples of the rewrite direction:
   - *la trampa salta* → *la emboscada cae* / *se cierra la trampa* / *se dispara la trampa*
   - *desde cobertura* → *desde su escondite* / *al amparo de la maleza* / *agazapada*
   - *Mialee se separa hacia la sala* → *Mialee se desvía hacia la sala* / *se aparta hacia la sala*
   - *la última de las cuales parte limpio* → *la última conecta de pleno* / *la última acierta limpia*
   - *el asalto se rinde con su retirada* → *el asalto sobre Greenest cesa con su retirada* / *se desmorona*
   - *la partida se retira* → *el grupo se retira* / *los aventureros se retiran* / *los seis se retiran* (or the named characters as the subject)

3. **Register-consistency check.** Saga voice in this campaign is *grounded heroic* — flowing oral-epic narration, but not pseudo-archaic and not modern-urban. Flag and rewrite any phrase that breaks register in either direction:
   - **Too archaic / bookish for the surrounding prose:** *sendas* (use *dos*), *poterna* (use *postigo*), *áncora* (use *ancla*), *en derredor* (use *alrededor*), *engarzadas en un mismo símbolo* (use *unidas en un mismo símbolo* or simpler), constructions with *cual* / *do* / *empero* / *otrora* in modern-feeling sentences.
   - **Too urban / modern for a medieval setting:** *azotea* for a medieval keep (use *adarve* / *almenas* / *parapeto*), *trasero* / *cuarto* for a fortress chamber (use *sala* / *aposento*), Anglicisms in dialogue.
   - The test: read the sentence aloud against the surrounding paragraph. If it sounds like it stepped out of a different century or genre, rewrite it.

4. **Forced-literary collocations.** Distinct from the archaic-register check above: this heuristic targets phrases that are grammatical, not archaic, and not obvious calques — but read as imagined-saga prose rather than written-Spanish prose. The verb and noun don't collocate naturally in Spanish; the result sounds like the drafter reaching for "epic" diction rather than writing the sentence a native would write. The drafter has consistently overshot the register in this direction; default to ordinary verbs.
   - **Verb-noun pairings that don't collocate naturally**: *tender un susurro* (susurros se envían / se dejan caer, no se tienden), *llamar un susurro de curación* (curaciones se envían / se conjuran / se susurran), *moldear una silueta sobre la pendiente* (las ilusiones se proyectan, no se moldean), *florece una espada* (use *aparece* / *se materializa*), *el calor lo bordea* (use *el calor lo esquiva*), *cae atrás varios alientos* (alientos as a time unit is poetic overreach; use *segundos* / *instantes*), *moldea sobre la pendiente* (use *proyecta sobre la pendiente*), *evoca su mano arcana* (use *invoca su mano arcana*), *Sinsong devuelve fuego al mago* (use *Sinsong le responde al mago con un dardo de fuego*), *Sinsong lo devuelve sentado y respirando* (calque of "returns him to sitting"; use *lo cura y el goliath se incorpora*).
   - **Forced-metaphor descriptors**: *hace de ancla viva para los que siguen* (use *baja primero y sostiene a los demás*), *con la mano firme de quien aprendió a rastrear antes que a leer* (one such flourish per recap maximum, not as a paragraph-closing tic), *amasa entre los dedos un puñado de bayas* (*amasar* is for dough; use *prepara con los dedos*).
   - **Telegraphic fragments**: *Cuerno desde la torre central.* / *Cultistas corriendo, ojos hacia arriba.* — fragments work sparingly for impact, but the drafter strings them together. Default to complete sentences (*Un cuerno suena desde la torre central*); use fragments only at genuine climactic peaks.
   - **Anthropomorphic flourishes**: *el filo se niega a salir*, *el resplandor azul sigue intentándolo*, *el grupo se parte* — saga voice can carry one per scene; the drafter strings them. Cap at one per scene, use ordinary verbs (*el filo no sale*, *el resplandor azul no llega a cerrar la herida*, *el grupo se divide*) otherwise.
   - **Repeated formal adverbs as emphasis**: *manifiestamente un mago y manifiestamente de tierras lejanas* — formal adverbs repeated for emphasis read stilted. Use *claramente, claramente* or restructure.
   - **English-idiom calques on stock phrases**: *acepta una mano libre* (English "a free hand"; use *acepta que le echen una mano*), *con cuatro cazadores en cola* (English "in tow"; use *a la zaga*), *los pies contra la roca* (English "feet-up against the rock"; use *atado contra la roca*), *La causa que se publica* (English "the official line"; use *La causa pregonada* / *La causa que pregonan*).
   - The test: would a native Spanish writer, drafting from scratch (no English source in front of them), reach for this verb-noun pairing? If the answer is "probably not — they'd use a different verb entirely", the phrase is forced-literary. Rewrite with the more ordinary verb.

**Self-correct, do not interrupt the GM.** The audit's primary mode is to land idiomatic prose on the drafter's own — pick the most natural alternative and commit. Surfacing a phrase to the GM for ruling is a last resort, reserved for cases where the drafter has tried two or three rewrites and none read natively. The GM has explicitly asked not to be prompted on phrasing decisions during drafting; the drafter is expected to deliver clean prose without per-phrase consultation. If in doubt across the audit as a whole, prefer the *more grounded, less ornate* alternative — the calibrated register is closer to plain narrative than to literary saga.

## Excluded (must NOT appear)

- **Markdown structure beyond the prescribed Homebrewery skeleton** — no headers below H1, no bullet lists, no tables, no blockquotes, no horizontal rules, no backticks. The only markup permitted in the body is `**bold**`, `*italics*`, and the `{{wide ...}}` paragraph wrappers (plus the foot's `{{pageNumber,auto}}` + `{{footnote ...}}`). See SKILL.md's *Output* section for the full skeleton.
- **Numeric mechanical detail** — HP, AC, DC, save numbers, attack rolls, damage rolls, spell slot levels, spell save DCs.
- **Numeric Honor changes.** When the minutes mention an Honor delta (*"+1 Honor each PC"*), render allegorically (*"sus actos honorables son alabados"*) — never the number.
- **Per-PC mechanical roll-call** (*"Mialee gasta una poción, Sinsong un slot"*). Mechanical state leaks into prose only when it drives a beat (*"al borde del desmayo, bebe una poción y se yergue"*).
- **Headers, sub-headers, bullet lists** — single flowing prose only.
- **GM-only knowledge** — only what the *characters* witnessed in fiction.
- **Heavy or running editorial commentary on player decisions.** Brief flourishes are fine in either direction — heroic-saga voice naturally frames its protagonists, and one or two sparing notes per recap (*"el grupo demuestra astucia"*, *"con valor inesperado"*, or occasionally *"una decisión imprudente"* when the moment warrants) fit the tone. Use sparingly in both directions; the actual exclusion is *running commentary on each decision*, not the polarity. Voice should skew positive overall — negative grading is allowed but should not be abused.

## Combat

Outcome-focused, never beat-by-beat. A few signature moments (the crit, the near-death, the clever maneuver, the duel's climactic round) carry the scene. The math behind rolls never appears.

**Mechanical detail rides on narrative payoff — and the bar is higher than in the minutes.** The minutes preserve color-rich detail; the recap keeps only the moments that carry the saga forward. A PC dropping to single-digit HP and reviving with a potion → in (genuine tension). The exact damage from a kobold rock → out.

## Pacing and shape

- **Climactic weight.** The session's climax (the duel, the rescue, the betrayal — whatever the minutes build toward) gets prose space proportional to its stakes. A one-sentence climax is wrong; rewrite to give it room.
- **Paragraph purpose.** Each paragraph earns its space — it carries new ground, a turn, or an emotional shift. A paragraph that just continues describing what the previous one started should be merged or cut.
- **Tension shape.** The recap reads as having rising tension, climax, and resolution — even if the minutes' beat sequence is uneven. Shape the arc within paragraphs and across paragraph breaks.
- **Failed / abandoned plans** appear only if they shaped the canon outcome materially. A worth-a-phrase mention if it explains a downstream decision; otherwise drop.

## Minutes-trace audit

The minutes-as-canon rule is the most fundamental constraint on the recap, but the drafter has demonstrated that reading the rule is not enough to enforce it. Without a mechanical trace step, rendered beats drift from minutes facts in characteristic ways — a *"shows the pendant"* beat becomes a *"hands the pendant to X"* beat, an adjacent observer becomes the actor, a "could have happened" inference becomes a stated event. This audit makes the no-invention rule load-bearing instead of aspirational.

Apply the audit by going through the draft **sentence by sentence** and naming, for each clause, the minutes scene + beat it came from. Anything that cannot be cited is invention — rewrite to match the minutes, or cut. Verbatim quotes must trace to a minutes line that already carries the same wording in quotes; paraphrases must trace to a beat in the minutes whose substance the paraphrase preserves.

Common drift patterns to watch for:

- **Conflated subjects.** Minutes name PC A as the doer of one beat and PC B as the recognizer / observer / addressee of an adjacent beat; drafter renders both with PC A (or PC B) as a single actor. *Example: minutes have Nesim "show the party" the pendant and Mialee "recognize" the symbol; drafter renders it as Nesim handing the pendant to Mialee.*
- **Action substitution.** Minutes have an NPC *show* / *display* / *describe* something; drafter substitutes a stronger verb (*hand over* / *gift* / *transfer*) that reads better but isn't in the source. The strength of the verb is in the source, not the drafter's discretion.
- **Inferred causality.** Minutes have two adjacent beats; drafter inserts a bridging cause/effect that the minutes don't claim (*"and so X did Y"* when the minutes don't link the two).
- **Color drift.** Minutes describe a setting one way; drafter substitutes a stronger or sharper detail that reads better but isn't in the source.
- **Unattributed dialogue or reaction.** Drafter renders a line or in-fiction reaction that doesn't appear in the minutes (no matter how plausible at the table).

When uncertain on a clause, surface to the GM with the minutes citation rather than commit. Treat the audit as mandatory; budget the time. The audit is the first review pass for a reason — if a beat shouldn't exist, no other audit matters.

## Final pass before delivery

1. **Homebrewery skeleton** — file opens with `# Sesión <N> {{float:"right" <real-world date>}}` followed on the next line by the `{wide}` single-brace injector (which makes the H1 span full width), followed by `{{wide _<in-fiction date>_ }}`, followed by per-paragraph `{{wide ... }}` blocks, with `{{pageNumber,auto}}` + `{{footnote Tiranía de Dragones | Sesión <N>}}` at the foot. No other Markdown structure (headers below H1, lists, tables, blockquotes, horizontal rules, backticks).
2. **Emphasis rationed** — bold (`**...**`) on 3–5 dramatic peaks max; italics (`*...*`) on verbatim Spanish quotes from minutes (mandatory) and on 2–4 atmospheric grace notes max. If a sentence relies on emphasis to land, the sentence itself is the fix — rewrite, don't lean on `**`.
3. **No `[EPIC]` literal text** in output (the marker is production metadata; the beat survives, the tag does not).
4. **Hidden agency** never telegraphed; recurring details rendered as plain observation.
5. **Honor changes** allegorical, never numeric.
6. **Imperial measurements** converted to metric.
7. **Chronology** preserved at the event level.
8. **Length** at ~800–1200 words (one Homebrewery page). If the draft is over ~1400, do a compression pass before delivery: identify the least load-bearing paragraph(s) and cut or merge. Overshoot is the drafter's demonstrated failure mode — do not treat prior sagas' word counts as the target.
9. **Saga voice, not checklist** — sentences vary in rhythm, beats merge into flowing passages, no run of subject-verb-object short sentences.
10. **Minutes-trace audit complete** — every clause has been traced back to a specific minutes scene + beat per the [Minutes-trace audit](#minutes-trace-audit) section; nothing in the recap is unsourced.
11. **Idiomatic-Spanish audit complete** — all four heuristics from the [Idiomatic-Spanish audit](#idiomatic-spanish-audit) section have been applied sentence by sentence: no bare English game terms in plain prose, no translator-shape sentences (including single-word calques), register consistent throughout, no forced-literary collocations.
