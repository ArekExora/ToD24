---
name: use-pipeline-scripts
description: Use the pipeline's build/convert scripts for derived artifacts — don't hand-craft outputs the script already generates
metadata:
  type: feedback
---

Derived artifacts in this project (Homebrewery brews, full-minutes builds, PC/NPC context digests) are produced by scripts in `.claude/skills/<skill>/`. Use the script, don't hand-craft.

**Why:** Hand-crafting duplicates work the script already handles deterministically, drifts from the shared format over time, and burns tokens on a task that's ~1 shell command. In 2026-07 I hand-wrote `gm-hb-10.md` when `gm_to_homebrewery.py` already existed for exactly this — a script the user pointed me to only after I'd written the file.

**How to apply:** Before generating any player-facing brew, `_context.md` digest, or `full-minutes-*.md`, grep `.claude/skills/*/` for a script matching the artifact name. Known ones:

- `.claude/skills/gm/gm_to_homebrewery.py` — `gm-NN.md` → `outputs/gm-hb-NN.md`
- `.claude/skills/gm/build_full_gm.py` — full-gm builds
- `.claude/skills/saga/build_full_saga.py` — full-saga brew
- `.claude/skills/draft/build_full_minutes.py` — full-minutes builds
- `.claude/skills/draft/_regen_context.py` (also under `campaign/pcs/`) — regenerate the PC context digest
- `.claude/skills/render_pdf.py` — `saga-NN.md` / `outputs/gm-hb-NN.md` / `minutes-NN.md` → `outputs/S<NN> - {Saga,GM,Minutes}.pdf` via headless Homebrewery; replaces the manual *paste into Homebrewery → Get PDF → rename → move* loop. Each run POSTs an anonymous brew, renders the PDF, deletes the brew — no persisted state. `--wip` writes to `S<NN> - <Role>_WIP.pdf` for draft-time one-page-fit checks.

If a script exists, run it. If it doesn't, only then hand-craft — and consider whether the artifact deserves a script.
