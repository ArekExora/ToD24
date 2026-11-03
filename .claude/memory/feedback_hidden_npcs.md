---
name: Hidden NPCs — never named in transcripts
description: Hidden NPC names never appear in transcripts, but their actions ARE narrated by the GM as in-fiction events that players witness.
type: feedback
---

Hidden NPCs (NPCs with `status: hidden` in `campaign/npcs/`) are never named at the table. By design, their actions are narrated by the GM live as in-fiction events — players witness the visible effect (e.g., a "blue glow" healing, an arrow from somewhere, an unexplained recovery) but don't know who actually caused it. The NPC's name never reaches the table, so the transcript never carries it.

**Why:** hidden NPCs are concealed agents. The illusion only works if no one at the table — and therefore no transcript — names them.

**How to apply:**

- The in-fiction effect IS in the transcript (the GM narrated it live as players witnessed it). [`/draft`](../skills/draft/SKILL.md) renders it as an ordinary transcript-derived beat in minutes, with the same per-claim citations as any other beat. No speculation about hidden-NPC identity is required — or permitted — at draft time.
- Hidden NPCs are NEVER referenced by name in minutes (the minutes are player-safe). The hidden NPC's identity is a GM-only fact.
- The trace-audit subagent ([`agents/trace-audit.md`](../agents/trace-audit.md)) audits hidden-NPC misattribution beats like any other — they carry citations because they came from the transcript.
