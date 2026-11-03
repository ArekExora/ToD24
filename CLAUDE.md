# Tyranny of Dragons — Campaign GM Toolkit

Personal GM toolkit for running a D&D 5e 2024 *Tyranny of Dragons* campaign. The project covers session-transcript processing, campaign-state tracking, and faction-behavior reasoning.

## Main functionality — session recaps

The project's primary function is turning session transcripts into recaps. Each session lives in `sessions/session-<NN>/` and produces three canonical artifacts (`saga-<NN>.md`, `gm-<NN>.md`, `minutes-<NN>.md`) plus an `inputs/` subfolder for working materials. See [sessions/README.md](sessions/README.md) for the per-session layout, file roles, naming conventions, and cross-session inputs.

The pipeline:

1. [`/transcribe`](.claude/skills/transcribe/SKILL.md) — session audio → raw merged transcript → canonicalised witnesses (`transcript-NN.txt`, `transcript-dia-NN.txt`). Hallucination filtering, cross-track bleed dedup, and name canonicalisation are folded in.
2. [`/draft`](.claude/skills/draft/SKILL.md) **write mode** (unattended) — cleaned transcripts → `minutes-<NN>.md` (written with `status: drafted`) and `inputs/triage-<NN>.md`. Loads campaign context (PC/NPC digests, state, homebrew), drafts with per-bullet citations, runs the in-context audit passes plus the trace-audit subagent, snapshots, notifies, stops. No GM in the loop.
3. [`/draft`](.claude/skills/draft/SKILL.md) **audit mode** (re-invoked in a fresh conversation, GM present) — same skill, auto-switches to audit mode when minutes already exist at `status: drafted`. Conducts the interactive GM handoff (prior-session audit, Spanish dispositions, NPC file confirmations, date / continuity references), applies dispositions, re-runs Pass 0 + 1 + 2 + 3, propagates the *File updates needed* checklist into the campaign's living canon files. Idempotent — safe to re-invoke until everything is clean.
4. **Manual GM review and acceptance** — minutes stay at `status: drafted` through every `/draft` invocation. The GM reads the file, edits anything that needs touching by hand, and bumps `status: drafted` → `status: accepted` when satisfied. As part of this review the GM strips the transcript anchors (`[T:xxx]`, `[GM]`, `[derived:...]`) — they're working metadata for `/draft`'s audit passes, not part of accepted canon. Downstream skills refuse to consume anything not at `status: accepted`.
5. [`/gm`](.claude/skills/gm/SKILL.md) — accepted minutes + triage → `gm-<NN>.md` (canon). Structural digest of minutes; no transcript reads. Run after the GM has bumped minutes to `accepted`; parallelisable with `/saga`. If `gm-<NN>.md` already exists, switches to audit mode (compare-and-report; never overwrites).
6. [`/saga`](.claude/skills/saga/SKILL.md) — accepted minutes → player-facing recap.

`/draft` is one skill with two modes — write produces the artifacts unattended; audit-mode re-invocations (in fresh context) catch the bias the drafter introduces. Pass 3 (the trace-audit subagent) is context-isolated by construction and runs in both modes. `/gm` derives from accepted minutes rather than raw transcript.

The minutes file's `status` field is the gate that sequences the pipeline: every `/draft` invocation (write or audit mode) leaves the file at `drafted`; the GM bumps to `accepted` by hand. See the [minutes template](sessions/templates/minutes-template.md) for the field spec and the [gm template](sessions/templates/gm-template.md) for the gm file's schema.

Each skill's `SKILL.md` is the authoritative spec for its outputs, rules, and exclusions; this file does not duplicate them. When a question is about *what goes in / out of a file* or *how a step behaves*, read the relevant skill.

**Hidden characters** (NPCs with `status: hidden`) are never named in the minutes or the player-facing recap. Their actions reach the players as the GM's live table-narration — a visible effect without an attributed actor (e.g., *"a keep cleric tended their wounds"*) — which `/draft` renders as an ordinary transcript-derived beat in the minutes. The hidden NPC's actual identity is indexed only in the GM file's §10 *Secrets* section, paired with the minutes scene.beat where the misattribution lives; the beat-to-identity mapping is collected during `/gm`'s Hidden-NPC handoff. See [gm/SKILL.md](.claude/skills/gm/SKILL.md) for the handoff workflow and [gm-template.md](sessions/templates/gm-template.md) for the Secrets section format.

## Persistent memory — read first

Project memory lives in [.claude/memory/](.claude/memory/) (versioned with the repo, not in Claude's external memory store). The index is [.claude/memory/MEMORY.md](.claude/memory/MEMORY.md); individual files contain user preferences, language conventions, and campaign context.

When saving new memories, write them into [.claude/memory/](.claude/memory/) and add a one-line index entry to [.claude/memory/MEMORY.md](.claude/memory/MEMORY.md). Do **not** write to the default external memory location (`~/.claude/projects/.../memory/`) — keeping memory in-repo is intentional so it travels with the project and survives directory renames.

@.claude/memory/MEMORY.md
