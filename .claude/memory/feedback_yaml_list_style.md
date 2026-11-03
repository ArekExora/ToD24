---
name: YAML list style — block, not flow
description: Project convention is block-style YAML lists (one item per indented hyphenated line) for languages/factions/etc., never inline [a, b, c] flow style
type: feedback
---

YAML lists in this repo's frontmatter (PC sheets, NPC sheets, session frontmatter, etc.) use **block style only**:

```yaml
languages:
  - Common
  - Elvish
factions:
  - Harpers
```

**Never** flow style:

```yaml
languages: [Common, Elvish]
factions: [Harpers]
```

**Why:** consistency across PC and NPC sheets. The PC template `campaign/pcs/_template.md` uses block style; user expects NPC sheets to match. Both forms are valid YAML, but mixing them in the same project creates churn during reviews.

**How to apply:** when creating or editing any frontmatter list field — `languages`, `factions`, `party_present`, `locations`, etc. — always use the block form, even for single-item lists. A single-item list still gets one hyphenated line, not `[item]`.
