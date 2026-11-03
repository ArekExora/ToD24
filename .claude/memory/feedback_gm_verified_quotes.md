---
name: GM-verified canon supersedes transcript
description: When minutes-NN.md or gm-NN.md has been manually edited by the GM, those edits are canonical — propagate them to derived files (NPC sheets, faction files, location files, timeline) instead of reverting to transcript-original wording.
type: feedback
---

When the GM has manually verified or corrected a quote, fact, or detail in `sessions/session-NN/minutes-NN.md` or `gm-NN.md`, that GM-edited version is the canonical truth. When propagating the same content to other files (NPC sheets, faction files, location files, timeline entries, character bios, etc.), **use the GM-verified version**, not the raw transcript wording it originated from. If the same quote appears in multiple files and they diverge, propagate the GM's edit so all files match.

**Why:** GM edits encode in-fiction context the transcript can't always capture — a player's verbal slip the table corrected, a phrasing the GM remembers more accurately than STT, an in-fiction grammar fix (e.g. *"les" → "nos"* on a cultist's first-person line in S3), canonicalization over a DM's verbal slip (*"Greenfields"* → *"Greenest"*). Once GM-edited, the minutes/gm version is canon. Reverting to transcript-original loses that signal and reintroduces errors the GM already cleared.

**How to apply:** Before adding a quote, name, or detail from the transcript to a derived file, check whether `minutes-NN.md` or `gm-NN.md` for the same session already has that content. If it does, copy the minutes/gm version verbatim, not the transcript version. When minutes/gm and a derived file diverge, minutes/gm wins — propagate the canonical version to the derived file. Watch especially for Spanish quotes that may have been corrected (verb forms, pronouns, place names).
