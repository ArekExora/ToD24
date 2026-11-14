# Calendar of Harptos — reference

The in-fiction calendar used across the campaign. Faerûnian Dale Reckoning (DR). Single source of truth for month names, abbreviations, and intercalary days — referenced by minutes, timeline, gm, saga, and status files so spellings and short forms stay aligned.

## Year form

- Year number followed by `DR`: *1489 DR*, *1490 DR*.
- Full-form dates: `DD <Month> YYYY DR` (`22 Marpenoth 1489 DR`).

## Months

Twelve months, 30 days each. Day numbering is `1` through `30`, no `0`.

Full names are canonical and used in minutes, arc date-range lines, and anywhere a date is spelled out in prose. Abbreviations are used in `sessions/status.md` and in `timeline-<NN>.md` event lines.

| # | Full | Abbr | Season |
|---|---|---|---|
| 1 | Hammer | Hamm | Winter |
| 2 | Alturiak | Altu | Winter |
| 3 | Ches | Ches | Winter - Spring |
| 4 | Tarsakh | Tars | Spring |
| 5 | Mirtul | Mirt | Spring |
| 6 | Kythorn | Kyth | Spring - Summer |
| 7 | Flamerule | Flam | Summer |
| 8 | Eleasias | Elea | Summer |
| 9 | Eleint | Elei | Summer - Autumn |
| 10 | Marpenoth | Marp | Autumn |
| 11 | Uktar | Ukta | Autumn |
| 12 | Nightal | Nigh | Autumn - Winter |

## Intercalary days

Six special days that sit **between** months, not counted as part of any month and not given a day number. Written in dates with the **full name** — e.g. a scene date line reads `_~11:00, Feast of the Moon 1489 DR_`, and a timeline event line reads `- Feast of the Moon (S22) — <event>`.

| Full | Abbr | Falls between | Notes |
|---|---|---|---|
| Midwinter | Midw | 30 Hammer → 1 Alturiak | - |
| Greengrass | Gree | 30 Tarsakh → 1 Mirtul | - |
| Midsummer | Mids| 30 Flamerule → 1 Eleasis | - |
| Shieldmeet | Shie | after Midsummer, before 1 Eleasis | **Leap-day** — present only when year ≡ 0 (mod 4). *1492 DR has it.* |
| Highharvestide | High | 30 Eleint → 1 Marpenoth | - |
| The Feast of the Moon | FMoo | 30 Uktar → 1 Nightal | - |

## How to use this file

- **Spelling checks:** when a draft file names a month or intercalary, cross-check against the tables above.
- **Abbreviation lookup:** `sessions/status.md` and `timeline-<NN>.md` event lines pull the `Abbr` column.
- **Intercalary placement:** when a session frontmatter date suggests a crossing (e.g., 30 Uktar → 1 Nightal), check whether an intercalary falls between — if yes, it is a full in-fiction day.
