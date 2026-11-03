<!--
minutes-NN.md — Session minutes

PURPOSE
  The verified record of the whole session, in chronological order — the
  durable artifact once the transcript is gone. Also shared with players
  as a detailed reference.

SELF-CONTAINED — assumes the cast is identifiable by name; does not
re-introduce PCs or recurring NPCs each session.

THE TWO PRINCIPLES — apply to anyone writing to or verifying the minutes.

  1. COMPLETENESS — every story-relevant beat must be present: actions,
     decisions, dialogue, in-fiction reactions, mechanical tension,
     character-state transitions. The minutes are the undisputed source of
     truth once accepted; the transcript is never re-read. When in doubt,
     INCLUDE.

  2. TRACEABILITY — every claim traces to a source: a transcript line
     ([T:N], [Td:N]), GM input ([GM]), or synthesis of multiple transcript
     observations ([derived:T:N1+T:N2+...]). SYNTHESIS IS PERMITTED —
     what's forbidden is BARE PROSE with no source. See
     .claude/memory/feedback_no_invention.md and the GLOSS BUDGET section
     below.

  The CITATION CASCADE (below) reconciles both. DROP IS THE LAST RESORT,
  NOT THE DEFAULT — shortcutting to drop creates structural gaps (a
  character unconscious in beat N and walking in beat N+3 with no recovery
  between).

FILE-LEVEL CONVENTIONS

  LANGUAGE — English narration. Specially memorable / funny / character-defining
  lines kept verbatim in Spanish inside quotes; rest translated. Each
  Spanish quote gets a triage *Verbatim Spanish dispositions* entry
  (keep / translate / drop).

  NO UNQUOTED SPANISH IN NARRATIVE PROSE. Spanish appears ONLY inside
  quotes or as canon proper nouns (PC/NPC names, locations). Translate
  loanwords (*meseta* → plateau, *barranco* → ravine).
  Exception: in-fiction proper nouns with no English equivalent
  ("dragonclaw" as a cult rank stays).

  FORMAT
    - H1 pair: "# Session NN {{float:"right" YYYY-MM-DD}}" followed on
      the next line by "{wide}". NN is the session number; YYYY-MM-DD is
      the real-world session date (mirrors frontmatter `date`). Both
      {{…}} and {…} are Homebrewery directives; render harmlessly
      elsewhere.
    - Scene header: "## N - <Title>" — bare integer, ASCII hyphen-minus,
      ~20-char title. No "Scene" prefix.
    - Date line: italic, on the next line when anchored:
      _~HH:MM, DD <Month> YYYY DR_. ~ for approximate; trailing ? for
      derived (e.g. _~08:00?, 24 Marpenoth 1489 DR_) — derived times need
      a triage *Date / continuity references* entry. Omit when the scene
      continues the previous clock.
    - Beats: ordered list (1., 2., …, restarting each scene). Addressable
      as <scene>.<beat> (e.g. "3.5 needs fixing"). NO BLANK LINE between
      consecutive beats — they sit one after another. The blank line
      appears only before the next scene header or the closing block.
    - Closing block: "{{pageNumber,auto}}" + "{{footnote Tyranny of Dragons
      | Session NN}}" at the file end (same NN substitution as the H1).
      Homebrewery page-footer pair; renders harmlessly elsewhere. GM
      repeats the pair before each "\page" during manual review.

  MARKDOWN STYLING — light embellishment for Homebrewery rendering.
    - Bold (**…**) — NPC names on FIRST MENTION PER SESSION (repeats stay
      plain); plus a few high-impact phrases per session (numbers,
      directions, decisive beats). PC names are NEVER bolded.
    - Italic (*…*) — in-fiction quotes (especially Spanish); key terms
      the GM wants to land (*hatchery*); short sensory flourishes
      (*paralysed*, *soft purple light*).
    - EMBELLISHMENT IS FORMATTING-ONLY. Don't paraphrase, add, or remove
      content to fit emphasis. If nothing is worth bolding, don't
      manufacture it.

  EPIC TAG — ***[EPIC]*** prefix immediately after the beat number. Marks
  a peak heroic / dramatic / unforgettable beat.

  CHRONOLOGY IS CANONICAL — beats in the order events happened at the
  table, within and across scenes. Never reorder for thematic grouping.

CITATION CASCADE

  Every beat traces to the transcript — and the trace is PER-CLAIM, not
  per-beat. Each distinct factual claim (who acted, what they did, on
  whom, with what direction, position, outcome) is independently grounded.
  Atmospheric prose, scene-setting flavor, and inferred details are
  subject to the same rule.

  PER-CLAIM CITATIONS appear inline at the point of the claim, not as a
  single tag at the end of the bullet. A bullet with three independent
  facts carries three inline citations. CLAIMS THAT CANNOT CITE CANNOT SHIP.

    ✗ Wrong — single span:
      1. Eguzkilore holds the unconscious Sinsong; Nuberroca rages at the
         doorway; Frulam and Langdedrosa are in the chamber beyond. [T:1-23]

    ✓ Right — one citation per claim:
      1. Eguzkilore holds the unconscious Sinsong [T:5]; Nuberroca rages
         at the doorway [T:9]; Frulam and Langdedrosa are in the chamber
         beyond [T:12], with two berserkers still standing [T:16-18].

  Why per-claim: a wide span covers all claims but verifies none
  individually — cross-claim contradictions slip through.

  SPAN WIDTH. [T:N-M] covers ONE continuous claim, typically ≤3 lines.
  Wider spans almost certainly bundle distinct claims — split them. If
  two claims share a line, repeat ([T:42], [T:42]) rather than widen.

  THE CASCADE — applied PER CLAIM, in order:
    1. DIRECT [T:N] / [Td:N] — the line stating the claim. Default.
    2. DERIVED [derived:T:N1+T:N2+...] — synthesised from multiple lines.
       REQUIRED whenever synthesis is involved (a flat span on a
       synthesised claim hides the synthesis). Logged in triage
       *Derived beats*.
    3. ?-FLAG TO TRIAGE — when the inference is too thin even for
       [derived:...] but continuity demands the claim. Logged in triage
       *Date / continuity references* or *Derived beats*.
    4. DROP — only when 1–3 all fail.

CITATION LIFECYCLE

  Citations are the audit trail for the DRAFTED phase — they exist so
  the trace audit and the GM's manual review can verify every claim
  against the transcript. They are NOT a permanent fixture of the file.

  When the GM reviews the minutes, the citations may be stripped by hand 
  as part of that review. Minutes at `status: accepted` MAY CARRY NO 
  CITATIONS AT ALL.

  IMPLICATIONS:
    - /draft (write and audit modes) ALWAYS emits and preserves inline
      citations; the file leaves /draft at `status: drafted` with full
      citations intact.
    - Downstream skills (/gm, /saga) MUST NOT require citations on
      accepted minutes. The accepted prose IS canon; absence of trace
      tags is not a defect.

CITATION TAXONOMY

  [T:N] / [T:N-M] — line(s) in transcript-<NN>.txt (primary witness).
    Default. Regular hyphen, not en-dash. GM rulings voiced on mic use
    [T:N], not [GM].
  [Td:N] / [Td:N-M] — line(s) in transcript-dia-<NN>.txt (secondary).
    Use only when present in dia but not in primary.
  [GM] — info from the GM OUTSIDE the transcript. If it's in the transcript,
    cite [T:N].
  [derived:<source>] — synthesised claim. Two forms:
      - DERIVED ANCHOR (time/date): [derived:rest+1d],
        [derived:calendar-2025-03-09]. Used on frontmatter values and
        scene-header times. Tracked in triage *Date / continuity
        references*.
      - DERIVED BEAT (event): [derived:T:N1+T:N2+T:N3] — multiple lines
        together support the synthesis. Tracked in triage *Derived beats*.
  CUMULATIVE combinations: [T:1248, GM] means "line 1248 + GM input
    together", not "either alone."

  TAG-TO-FILE MAPPING IS STRICT. [T:N] is line N of transcript-<NN>.txt;
  [Td:N] is line N of transcript-dia-<NN>.txt. A citation pointing at a
  file not present is a trace-audit failure.

  THREE TRANSCRIPT CASES — A: primary only → [T:N] only; B: dia only →
  [Td:N] only; C: both → [T:N] by default, [Td:N] when dia-only.

  CITATION ANCHORS TO OCCURRENCE, NOT RETROSPECTION. Cite where the
  action *occurred*, not where it was later discussed. Players sometimes
  recap an earlier moment from a later line — that's not a new beat;
  it folds into the original citation.

GLOSS BUDGET — REPHRASING ONLY

  Vivid restatement of a fact already in the transcript is permitted.
  INFO-ADDING (introducing facts not in the transcript) is FORBIDDEN,
  however natural the prose reads.

  TEST: would removing the phrase leave a gap in the established record?
  If yes, the fact was already there — rephrasing is fine. If no, the
  fact exists only because of this prose — cut.

  THE DAWN FAILURE PATTERN: transcript silent on time → "at dawn" asserts
  a fact not in the transcript. See feedback_dawn_pattern.md and
  feedback_gloss_budget.md.

PROSE STYLE — BEATS AS FLOWING IN-FICTION NARRATIVE

  Each beat is one coherent narrative piece, not a chain of bullet-style
  sentences. Connect with temporal/causal connectives (then, and, while,
  as, in answer) where the source supports it. Don't merge across beat
  boundaries.

  IN-FICTION LANGUAGE — render mechanics as what the characters do, not
  as the rules entry being invoked.

    - Class / subclass / species features verbatim (Cloud's Jaunt, Action
      Surge, Second Wind, Rage, Pack Tactics, Multi-Attack, etc.) — render
      the effect.
        ✗ "Eguzkilore uses Action Surge."
        ✓ "Eguzkilore swings again in the same breath."
    - Spell names (Entangle, Goodberry, Healing Word, Hunter's Mark,
      Spiritual Weapon, etc.) — render as the in-fiction effect.
        ✗ "Nyx casts Goodberry and revives him."
        ✓ "Nyx pops one of her berries into his mouth and he comes around."
      Named-spell form may stand when the beat hinges on the name itself
      (a verbal component the GM dramatised, a named-spell taunt).
    - Action / mechanic jargon (bonus action, opportunity attack, saving
      throw, advantage / disadvantage, heavy cover, temporary HP, death
      save, the check, PC, Foundry) — replace with the in-fiction effect.
        ✗ "Eguzkilore takes opportunity attacks moving out."
        ✓ "Two blades catch Eguzkilore as he pulls back."
      Action verbs that double as plain English (hide, grapple, dodge,
      disengage, critical) may stay when they read naturally — apply the
      recognisability test below.
    - Conditions — restrained, frightened, invisible, prone, grappled are
      plain English and MAY STAY. Swap to in-fiction effect (pinned, held,
      terrified, flat on the stones, out of sight) only when the prose flows
      better as effect, or when the condition name reads as obviously
      mechanical to a lay reader.
    - Dice / range references ("rolls a 20", "long range", "30 feet") —
      render as prose.
        ✗ "The throw goes wide at long range."
        ✓ "The throw goes wide at the distance."

  KEEP COMMON ENGLISH that overlaps with mechanics — party, dash, rest,
  damage, attack, hit, miss, save (verb), cover, roar. Don't swap
  reflexively.

  PROPER-NOUN RECOGNISABILITY TEST. If a 5e-experienced reader would
  cross-reference the term to a rules entry, swap it; otherwise keep it.
  When in doubt, KEEP — over-correction reads stilted.

REQUIRED CONTENT

  - Spells — rendered as in-fiction effect by default (PROSE STYLE
    above); named form when the name is part of the moment. Spell-source
    provenance (class / slot / feature) excluded.
  - Weapons / ammo / quantities WHEN THEY ADD TEXTURE (a longbow shot
    from a tree, 20 arrows, the rum bottle). Drop when they don't.
  - Mechanical moments that drove tension — near-deaths, crits with
    notable outcomes, interrogation pressure. Outcome-focused.
  - Dialogue snippets (1–2 per scene max), verbatim Spanish in quotes
    when truly memorable.
  - Sensory detail — the bald-head glow on cast, smoke between rocks,
    an NPC's nervousness.
  - Failed plans and abandoned threads — they explain WHY canon outcomes
    happened.

EXCLUDED

  - Turn-by-turn combat. Only narratively-relevant moments.
  - Out-of-character table activity — initiative chatter, sheet lookups,
    rules debates, scheduling, off-topic table joking. Only what happened 
    IN FICTION.
  - Numeric dice results — to-hit totals, damage, HP, AC, save DCs, roll
    values. The narrative outcome (hit / miss / crit / fumble / near-death
    / unconscious) is in scope; the math is not. Resource counts (gold,
    potions, ammo) and explicit awards are NOT dice results — leave them in.
  - Proper-noun game mechanics in prose — see PROSE STYLE above.
  - Spell-source / feature-provenance explanations — no "(Magic Initiate
    Wizard cantrip)", "(1st-level slot)". Spells either appear on the
    sheet (and stand) or belong in triage *Mechanical / rules flags*.
  - Hedging / production language ("possibly", "presumably", "confirm
    with GM"). Unverified content → triage, not the minutes.
  - STT canonicalization debate, calendar corrections, file-update
    artifacts → triage.
  - AI editorial conclusions ("the party demonstrated good tactical
    sense"). Show actions; let the recap draw conclusions.
    EXCEPTION: praise / critique / mockery FROM THE TRANSCRIPT — said by
    a player or NPC at the table — IS source material; capture as
    dialogue.
  - Speculation framed as fact. If the transcript doesn't support it, it
    doesn't go in the minutes.
  - Atmospheric prose that doesn't trace — same rule as plot beats.
    Wordsmithing what the transcript shows is fine; manufacturing
    atmosphere (it's dawn, there's smoke, he's on a shoulder) is not.
    See GLOSS BUDGET above.
  - Inferred details propagated as canon. A LOAD-BEARING inference — one
    that other beats depend on — must be EITHER anchored ([derived:...])
    OR flagged (?-tag with a triage *Date / continuity references* entry).
    Never bare narrative.

BOUNDARY RULES

  - Mechanical detail rides on narrative payoff. Include if cutting
    weakens the beat; cut if it just adds clutter.
  - Combat sequencing matters; combat math doesn't.
  - Length is unbounded. A 4-hour session can produce a long minutes
    file; that's expected.

FRONTMATTER FIELDS

  status — lifecycle marker; gate for downstream skills.
    drafted (/draft writes) → accepted (GM sets by hand).
  date — real-world. Append "HH:MM - HH:MM" range when known, "HH:MM"
    when only start known, plain date otherwise. TIMES ROUND TO THE NEAREST
    10-MINUTE SEGMENT (17:35 → 17:30, 20:43 → 20:40, 20:39 → 20:40).
    The intent is a general sense of the session's shape,
    not clock precision.
  in_fiction_date — FR calendar (Hammer, Alturiak, Ches, Tarsakh, Mirtul,
    Kythorn, Flamerule, Eleasis, Eleint, Marpenoth, Uktar, Nightal).
    Format mirrors the gm file's In-fiction date row: comma before each
    HH:MM, "~" prefix on approximate times, "→" between start and end.
    When the day rolls over within the same year, do NOT repeat the year
    and "DR" on the end side — day and month only (e.g.
    "22 Marpenoth 1489 DR, ~22:00 → 23 Marpenoth, ~02:00"). Repeat the
    year only when the range crosses into a new year. Single timestamp if
    the session covers <1 in-fiction day (e.g.
    "23 Marpenoth 1489 DR, ~02:00 → ~14:00").
  party_present — PCs whose player attended and ran the PC for at least
    part of the session. Alphabetical. YAML BLOCK STYLE (- per line),
    never flow form [a, b]. SCOPE: only PCs whose status is `active` AND
    joined_at <= NN. Hidden NPCs (status: hidden in `campaign/npcs/`) are
    separate from this roster — they never appear here, and their presence
    at the table surfaces only in the GM file's §10 Secrets.
    Edge cases:
      - Player attends but PC is silent / takes no actions → present
        (they were on stage, available to act).
      - PC is NPC'd by the GM because the player is absent → absent
        (the player did not run them).
      - PC name appears in transcript only because another player
        referenced them → absent (not actually on stage).
  party_absent — visible roster minus party_present. Alphabetical, or
    "none". SCOPE: only PCs whose status is `active` AND joined_at <= NN.
  locations — top-level location names only ("Greenest", not
    "Greenest keep / Greenest mill"). Chronological. YAML block style.

  TENTATIVE-VALUE MARKER. Append ? to any date/time component that is
  DERIVED (back-calculated) rather than directly anchored.
    in_fiction_date: 23 Marpenoth 1489 DR, ~18:30 → 24 Marpenoth, ~15:30?
  ?-tagged values need a triage *Date / continuity references* entry with
  the calculation chain.
-->

---
status: drafted    # drafted → accepted
date: YYYY-MM-DD HH:MM - HH:MM
in_fiction_date: DD <Month> YYYY DR, ~HH:MM → DD <Month>, ~HH:MM
party_present:
  - <Alice>
  - <Bob>
  - <Charlie>
party_absent: none
locations:
  - <Location>
---

# Session NN {{float:"right" YYYY-MM-DD}}
{wide}

## 1 - <First scene title>
_~HH:MM, DD <Month> YYYY DR_

1. <Beat>. <Inline citations [T:N], [Td:N], [GM], [derived:...]>.
2. <Beat>. <Inline citations>.
3. ***[EPIC]*** <Beat text>. <Citations>.

## 2 - <Next scene title>

1. <Beat>. <Inline citations>.

{{pageNumber,auto}}
{{footnote Tyranny of Dragons | Session NN}}
