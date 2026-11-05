# Session status

Tracker for the per-session pipeline state. One row per session; keep it in ascending order.

## How to fill the table

- **Session #** — the session number. Match the `session-NN/` folder name.
- **Transcript** — has the canonicalised transcript been produced?
  - ✅ done — `transcript-NN.txt` (and/or `transcript-dia-NN.txt`) exists in `session-NN/inputs/transcripts/`
  - ⚠️ unavailable — no audio file for the session
  - ❌ missing — no transcript yet
- **Minutes** — state of `minutes-NN.md`:
  - ❌ missing — file does not exist
  - ⚠️ drafted — file exists with `status: drafted`
  - ✅ accepted — file exists with `status: accepted`
- **Outputs** — combined state of the three PDFs (minutes PDF, saga PDF, GM PDF):
  - ❌ missing — none of the three PDFs have been generated
  - ⚠️ in progress — at least one PDF exists but not all three
  - ✅ done — all three PDFs have been generated
- **start** — the session's in-fiction start, taken from the `in_fiction_date` frontmatter of `minutes-NN.md`. Month abbreviated (Marp / Ukt / Nig / Hamm); year dropped. Empty when no minutes exist.
- **end** — the session's in-fiction end, same source and format. Empty when no minutes exist.
- **delta** — in-fiction gap between the previous session's end (S<sub>N-1</sub>) and this session's start (S<sub>N</sub>). ✅ when exactly 0; signed duration otherwise (e.g., `+10h`, `-30m`, `-17d21h`); `—` when either side has no minutes. A `?` suffix propagates if either input time was marked uncertain.

## Status


| Session # | Transcript  | Minutes  | Outputs  | start           | end             | delta      |
| --------- | ----------- | -------- | -------- | --------------- | --------------- | ---------- |
| 01        | ⚠️          | ✅       | ✅       | 22 Marp ~18:00  | 22 Marp ~22:00  | —          |
| 02        | ⚠️          | ✅       | ✅       | 22 Marp ~22:00  | 23 Marp ~02:00  | ✅         |
| 03        | ✅          | ✅       | ✅       | 23 Marp ~02:00  | 23 Marp ~14:00  | ✅         |
| 04        | ✅          | ✅       | ✅       | 23 Marp ~14:00  | 23 Marp ~18:30  | ✅         |
| 05        | ✅          | ✅       | ✅       | 23 Marp ~18:30  | 24 Marp ~17:00  | ✅         |
| 06        | ✅          | ✅       | ✅       | 24 Marp ~17:00  | 25 Marp ~15:00  | ✅         |
| 07        | ✅          | ✅       | ✅       | 25 Marp ~15:00  | 26 Marp ~00:30  | ✅         |
| 08        | ✅          | ✅       | ✅       | 26 Marp ~00:30  | 26 Marp ~01:00  | ✅         |
| 09        | ✅          | ✅       | ✅       | 26 Marp ~01:00  | 26 Marp ~11:00  | ✅         |
| 10        | ✅          | ✅       | ✅       | 26 Marp ~11:00  | 27 Marp ~10:00  | ✅         |
| 11        | ✅          | ✅       | ✅       | 27 Marp ~10:00  | 1 Ukt ~22:30    | ✅         |
| 12        | ✅          | ✅       | ✅       | 1 Ukt ~22:30    | 2 Ukt ~10:00    | ✅         |
| 13        | ✅          | ✅       | ✅       | 2 Ukt ~10:00    | 5 Ukt ~12:30    | ✅         |
| 14        | ✅          | ✅       | ✅       | 5 Ukt ~12:30    | 6 Ukt ~13:30    | ✅         |
| 15        | ✅          | ✅       | ✅       | 6 Ukt ~13:30    | 7 Ukt ~08:00    | ✅         |
| 16        | ✅          | ✅       | ✅       | 7 Ukt ~08:00    | 9 Ukt ~12:30    | ✅         |
| 17        | ✅          | ✅       | ✅       | 9 Ukt ~12:30    | 10 Ukt ~20:00   | ✅         |
| 18        | ✅          | ✅       | ✅       | 10 Ukt ~20:00   | 12 Ukt ~08:00   | ✅         |
| 19        | ⚠️          | ✅       | ✅       | 12 Ukt ~08:00   | 14 Ukt ~06:00   | ✅         |
| 20        | ✅          | ✅       | ✅       | 14 Ukt ~06:00   | 17 Ukt ~06:30   | ✅         |
| 21        | ✅          | ✅       | ✅       | 17 Ukt ~06:30   | 27 Ukt ~12:00   | ✅         |
| 22        | ⚠️          | ✅       | ⚠️       | 27 Ukt ~12:00   | 11 Nig ~13:30   | ✅         |
| 23        | ✅          | ✅       | ⚠️       | 11 Nig ~13:30   | 13 Nig ~12:00   | ✅         |
| 24        | ⚠️          | ⚠️       | ❌       | 13 Nig ~12:00   | 21 Nig ~14:00?  | ✅         |
| 25        | ✅          | ⚠️       | ❌       | 21 Nig ~14:00?  | 23 Nig ~09:00?  | ✅?        |
| 26        | ⚠️          | ⚠️       | ❌       | 23 Nig ~09:00?  | 25 Nig ~09:00?  | ✅?        |
| 27        | ✅          | ⚠️       | ❌       | 25 Nig ~09:00?  | 29 Nig ~09:30?  | ✅?        |
| 28        | ✅          | ⚠️       | ❌       | 29 Nig ~09:30?  | 29 Nig ~14:30?  | ✅?        |
| 29        | ✅          | ⚠️       | ❌       | 29 Nig ~14:30?  | 30 Nig ~06:00?  | ✅?        |
| 30        | ✅          | ⚠️       | ❌       | 30 Nig ~09:00?  | 1 Hamm ~12:00?  | +3h?       |
| 31        | ✅          | ⚠️       | ❌       | 2 Hamm ~09:00?  | 4 Hamm ~08:30   | +21h?      |
| 32        | ✅          | ⚠️       | ❌       | 4 Hamm ~07:00?  | 9 Hamm ~12:00   | -1h30m?    |
| 33        | ✅          | ⚠️       | ❌       | 9 Hamm ~12:00   | 10 Hamm ~06:30  | ✅         |
| 34        | ✅          | ⚠️       | ❌       | 10 Hamm ~06:30  | 10 Hamm ~21:00  | ✅         |
| 35        | ✅          | ⚠️       | ❌       | 11 Hamm ~07:00  | 11 Hamm ~10:30? | +10h       |
| 36        | ✅          | ⚠️       | ❌       | 11 Hamm ~11:00? | 11 Hamm ~16:15? | +30m?      |
| 37        | ✅          | ⚠️       | ❌       | 11 Hamm ~16:30  | 12 Hamm ~05:30  | +15m?      |
| 38        | ✅          | ⚠️       | ❌       | 12 Hamm ~06:00  | 13 Hamm ~22:00? | +30m       |
| 39        | ✅          | ⚠️       | ❌       | 14 Hamm ~09:00  | 15 Hamm ~21:00? | +11h?      |
| 40        | ✅          | ✅       | ❌       | 15 Hamm ~08:00  | 15 Hamm ~15:00? | -13h?      |
| 41        | ✅          | ⚠️       | ❌       | 15 Hamm ~11:00  | 15 Hamm ~14:00? | -4h?       |
| 42        | ✅          | ⚠️       | ❌       | 15 Hamm ~12:20  | 16 Hamm ~11:00? | -1h40m?    |
| 43        | ✅          | ⚠️       | ❌       | 16 Hamm ~08:00? | 16 Hamm ~15:00? | -3h?       |
| 44        | ✅          | ✅       | ✅       | 15 Hamm ~08:00  | 15 Hamm ~15:00  | -1d7h?     |
| 45        | ✅          | ⚠️       | ❌       | 15 Hamm ~15:00  | 15 Hamm ~16:20  | ✅         |
| 46        | ✅          | ⚠️       | ❌       | 15 Hamm ~16:20  | 15 Hamm ~19:20  | ✅         |
| 47        | ✅          | ⚠️       | ❌       | 15 Hamm ~19:20  | 16 Hamm ~07:40  | ✅         |
| 48        | ✅          | ⚠️       | ❌       | 16 Hamm ~07:40  | 16 Hamm ~10:00? | ✅         |
| 49        | ✅          | ⚠️       | ❌       | 16 Hamm ~09:50  | 16 Hamm ~10:45  | -10m?      |
| 50        | ✅          | ⚠️       | ❌       | 16 Hamm ~10:45  | 16 Hamm ~12:15  | ✅         |
| 51        | ✅          | ⚠️       | ❌       | 16 Hamm ~12:15  | 16 Hamm ~12:30  | ✅         |
| 52        | ✅          | ⚠️       | ❌       | 16 Hamm ~12:30  | 16 Hamm ~12:31  | ✅         |
| 53        | ✅          | ⚠️       | ❌       | 16 Hamm ~12:31  | 16 Hamm ~13:00? | ✅         |
| 54        | ✅          | ⚠️       | ❌       | 16 Hamm ~12:40? | 16 Hamm ~22:00  | -20m?      |
| 55        | ✅          | ✅       | ✅       | 16 Hamm ~22:00  | 17 Hamm ~08:20  | ✅         |
| 56        | ✅          | ✅       | ✅       | 17 Hamm ~08:20  | 17 Hamm ~13:20  | ✅         |
