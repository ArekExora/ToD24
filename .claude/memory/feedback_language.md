---
name: Language conventions for the campaign project
description: Spanish for session transcripts and recaps; English for everything else in the project
type: feedback
originSessionId: 047e7b49-771f-44be-b233-5e7564028529
---
In the Tyranny of Dragons project: session **transcripts** and the **sagas** generated from them are in **Spanish**. Everything else (timeline, faction files, NPC/location notes, skill definitions, internal docs, conversation with the GM) is in **English**.

**Why:** Transcripts come from a Spanish-speaking table; the user wants sagas in the same language so they can be shared or re-read in context. The rest of the project is for the GM alone, who prefers English for tooling and structured notes.

**How to apply:** When invoking `/saga`, output Spanish for the player saga (`saga-NN.md`). All other files produced by `/draft` and `/gm` (`gm-NN.md`, `minutes-NN.md`, `triage-NN.md`) and all campaign files (`timeline.md`, faction files, NPC and location files) are in English — even if the source transcript was Spanish, translate event descriptions to English on the way into structured notes. **Exception:** memorable / character-defining lines may be quoted verbatim in the source language inside English text. Never mix languages outside of these scoped quotes.
