# Session 27 — attendance + diarisation notes

⚠ **Second rename 2026-10-11:** `dia 23.flac` is now understood to be S27's audio (not S26's). The actual S26 was unrecorded; `session-26/` is the empty lost-audio folder. This file (formerly in `session-26/`) now lives in `session-27/`. The attendance mismatch previously flagged against "calendar S26" was downstream of the S26↔S27 mislabel and should be re-read against the real S27 slot.

⚠ **Original note (2026-10-09):** originally titled "Session 24" and placed in the then-named `session-25/` folder, under the assumption that `dia 23.flac` was S24's audio. After S24 was confirmed unrecorded (Craig failed; `dia 22` through `dia 31` all shifted down by one session each), `dia 23` was taken as S26's audio. Superseded by the 2026-10-11 correction above.

## Attendance

Updated after full-transcript review:

- **Sinsong (Gonzalo)** — absent; character paused by GM. GM briefly parks Sinsong (and one other PC) from acting at `[01:03]` scene, `[01:10:47]` PC-listing, and `[01:51:04]` "voy a meter a los que no están metidos en la partida también, a Sinsong y Amidamaru" — but note this latter line is a diarisation moment, not a full-session absence claim.
- **Amidamaru (Pablo)** — **confirmed present and active** (revised from initial "possibly silent"). SPEAKER_02 self-narrates as Amidamaru repeatedly (e.g. `[00:31:24]` "Bueno, en fin, Amidamaru", `[00:31:27]` "Amidamaru al escuchar a Mia gritar Nyx…", `[00:50:52]` "Yo creo que antes de eso Amidamaru haría todo lo posible…"). Uses Amidamaru's pistols + spells throughout.
- Other PCs (**Kaelthar, Nuberroca, Eguzkilore, Mialee, Nyx**) — all present and active.

Voice count on the recording: GM + 5 = 6 → diarisation `SPEAKERS=6`.

## Diarisation labels

Six clusters detected + `UNKNOWN` gap-fills (line counts):

- `SPEAKER_04` — 568 (25%)
- `SPEAKER_03` — 538 (24%)
- `SPEAKER_02` — 364 (16%)
- `SPEAKER_05` — 352 (15%)
- `SPEAKER_01` — 275 (12%)
- `SPEAKER_00` — 170 (7%)
- `UNKNOWN` — 5

Textual-evidence hints (verify by ear against contiguous cluster chunks per the S18 lesson; player→PC map in [reference_pc_players.md](../../.claude/memory/reference_pc_players.md)):

- **GM likely spans `SPEAKER_03` + `SPEAKER_04`** (combined 1106 lines = 48%, matching the S19 GM-dominance pattern). Session-closer at `[02:55:19]` is SPEAKER_03; extensive world/NPC narration runs through SPEAKER_04. Diarisation almost certainly split the GM into two clusters (as happened in S19 for Nuberroca's voice-profile change).
- **`SPEAKER_02` = Amidamaru (Pablo)** — see Attendance.
- **`SPEAKER_00` = Nuberroca (Sergio)** — likely. Uses Reckless Attack / Rage (Barbarian features) at `[00:23:32]` and `[01:17:00]`.
- **`SPEAKER_01` = Eguzkilore (Richy)** — likely. GM addresses "Richi" at `[02:21:40]`; handles the wolf mount and Champion-Fighter actions.
- **`SPEAKER_05`** — remaining player (Mialee/Nyx/Kaelthar). Also carries some early lines that may be Nuberroca on a bad connection before he switched devices at `[00:22:58]` "acabo de iniciar el ordenador".

## Canonicalisations applied

- `Langded → Langdedrosa` (line 930, `[01:06:52]`) — unambiguous truncation of the known NPC name.
- `Sulesdeth → Sulesdeg` (line 1397, `[01:48:56]`) — known NPC per [sulesdeg.md](../../campaign/npcs/sulesdeg.md).
- `Sensony → Sinsong` (line 1421, `[01:51:04]`) — GM PC-listing garble.
- `Redmere → Rezmir` (line 2154, `[02:48:08]`) — enemy mage invokes his boss. Known NPC per [rezmir.md](../../campaign/npcs/rezmir.md). GM confirmed this is mic garble, not plot-critical.

**Not touched (player table-talk decoding the name they just heard):**
- Line 2172 `SPEAKER_02: Red Mill.` and line 2173 `SPEAKER_02: RZMR.` — Amidamaru's player is speaking/spelling phonetic guesses at the villain's name. Left verbatim; this reads naturally alongside the canonicalised `Rezmir` line above.

## Follow-ups for `/draft 27`

**Plot-relevant:**
- **The blue-skinned humanoid** revealed on the fake-Nyx's death (`[00:34:17]` "la forma de Nyx se va convirtiendo en un bicho azul… un humano de tamaño humano azulado y medio azul oscuro") is **almost certainly a doppelganger** (GM-confirmed). The transcript also refers to it as "Doppelganger" at `[01:05:02]` and once as "el cuerpo del dragón" at `[00:56:27]` (probable garble of "cuerpo del bicho").
- **Trailing hallucination** — final line `[04:15:24] UNKNOWN: Hola, muy bien.` (raw confidence 0.05) is 1h20m after the natural session close at `[02:55:26]`. Drop at triage.

**Unresolved probable STT garbles left verbatim (no unambiguous canonical target):**

*Body-text / non-name:*
- `me meto a Mundath` (`[00:01:09]`) — unknown referent, mechanical context; not the NPC Frulam Mondath.
- `Nyx es un hackle` (`[00:02:52]`) — Nyx is a halfling; `hackle` reads like a species-term garble.
- `Ni Alex fue a avisar… A Nyx, usando mensaje` (`[00:17:37]`) — likely *Mialee*, but could be a GM self-correction stumble.
- `haciéndose pasta por Nyx` (`[00:17:53]`) — clearly *pasar*. Body-text STT, not a name.
- `Daniela solo estaba localizada en esa zona` (`[02:34:02]`) — almost certainly "de la niebla" (the fog was localised to that zone; matches the `[02:26:19]` "una niebla bastante bella").
- `listos para ir a las palomitas` (`[00:54:52]`) — probably *peleas*.

*NPC name variants (likely all real NPCs the STT can't lock down):*
- `Sondra y Pinto` (`[00:18:16]`) — not in campaign files.
- `Enki` (many lines from `[00:05:34]` onward) — Nuberroca's carried "bebé"/"teleñeco"; homebrew mechanic, not in files.
- `Cryja` (`[00:05:41]`, `[00:05:47]`) — "el clon de Cryja"; unclear.
- `Elfking` (`[01:08:48]`, `[01:08:55]`) — an NPC being consulted; possibly related to [edhelri-lewel.md](../../campaign/npcs/edhelri-lewel.md).
- `Miguel` (canonical, [miguel.md](../../campaign/npcs/miguel.md)) plus `Fenwir`/`Fenwyr`/`Fender` (`[01:10:58]` onwards) — one recurring NPC guard, spelling drifts.
- `Antón`/`Anthony` — one NPC (caravan protector), spelling drifts (`[02:09:23]` etc.).
- `Checo` and `Arne`/`Mane` (`[01:21:59]`, `[01:22:48]`) — two captive-soldier NPCs.
- `Calamara` (`[01:20:29]`) — unclear.
- `Karmato` (`[01:47:29]`) — "un trapo de la Karmato"; possibly *carreta*.
- `Betxo` (`[01:51:23]`) — unknown, possibly an NPC or wolf name.
- `Dalga` (`[00:41:03]`) — a Darla variant one-off.
- `Miale` (many lines) vs. `Mia` (frontmatter nickname) vs. `Mialee` (canonical) — GM and players alternate; treat all as Mialee.
- `Bluhoose` (`[01:30:49]`) / `Hanma` (`[01:45:45]`) / `Han` (`[02:07:53]`) / `Yemna Janma` (`[02:07:08]`) / `la llama maestra` (`[01:30:14]`) — all likely one NPC: the hooded Harper contact who reveals herself over `[01:29:00]-[01:41:58]`.
- `Abbad` (`[02:35:17]`) — enemy villain (the hooded mage attacking the caravan); not in campaign files, may need creation.
- `Bael` (`[01:39:11]`) — mentioned in Harper NPC dialogue; possibly *Bael* the villain or a garble.
- `Berenber` (`[01:38:53]`) — "el enorme Berenber está intentando reconstruirla"; unknown, in NPC's exposition about Waterdeep-area politics.

*Location variants:*
- `Daggerforce` (`[00:17:31]`) → probably **Daggerford**.
- `Nébrega` (`[01:39:20]`) → probably **Neverwinter**.
- `Karnaz` / `Nombre de Karnaz` (`[01:38:12]`) → probably **Carnath** (Carnath Roadhouse, ToD canon).
- `Valdivia` (`[01:23:59]`) — "el camino de Valdivia"; unclear.
- `las Márimas` (`[01:33:22]`, `[01:34:40]`) → **las Marismas** (Mere of Dead Men, ToD).
- `Naerytar` (`[01:27:17]` onwards) — correctly spelled; canonical ToD castle location.

Delete this file once `/draft 27` has folded these notes into triage.
