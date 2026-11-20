# Campaign arcs

Single source of truth for arc metadata — title, description, open date, page-break positions, and the shared page footer. **Maintained manually by the GM.** The `/timeline` skill and `build_full_timeline.py` only read this file; neither ever writes to it.

When the GM declares a new arc opening during a `/timeline` run, the skill prompts the GM to update this file manually after the session. The per-session `timeline-<NN>.md` files reference arcs by title only — the title in those files must match a `##` heading here exactly.

## Field reference

Each arc has three fields:

- **Opened:** `DD <Month> YYYY DR (S<NN>)` — in-fiction open date and the session the arc was opened in.
- **Description:** one short sentence, in the GM's voice. Rendered as the arc's intro paragraph in `campaign/timeline.md`.
- **Page breaks after:** list of positions where the page breaks. Each entry is `<date>, <session>, <index>` — identifying the exact event that ends the current page. `<date>` is the full FR form (`DD <Month> YYYY DR`). `<session>` is `S<NN>`. `<index>` is **1-based** within events that share the same (date, session) — e.g. `3` means "the 3rd event on that date belonging to that session". Most entries use index `1`. Use `(none)` when the arc fits on one page.

  Multi-line form (one entry per sub-bullet):

  ```
  - **Page breaks after:**
    - 23 Marpenoth 1489 DR, S03, 3
    - 25 Marpenoth 1489 DR, S06, 1
  ```

**The close date is derived, not stored.** An arc closes at the date of its last event. The chronologically-last arc (no later arc opened yet) is rendered as ongoing (`→ ` with empty right side). Once a later arc is added, the earlier one automatically takes a close date at the next rebuild.

## Page-break behaviour

When a page break fires, the current page closes with the footer defined in § Footer below followed by `\page`. The next page **always** re-emits the month sub-header.

The **arc frame emits exactly once per arc**, on the arc's first appearance — never on subsequent pages. Pages after the first show only month tables.

New arcs do not automatically start on a new page. If you want a clean page per arc, list the prior arc's last event (date, session, index) as a page break on that arc.

## Footer

Emitted on every page immediately before `\page`. The build script reads the literal lines inside the fenced code block below. Edit to change the rendered footer.

```
{{pageNumber,auto}}
{{footnote Tyranny of Dragons | Timeline}}
```

## Greenest in flames
- **Opened:** 22 Marpenoth 1489 DR (S01)
- **Description:** Greenest is burning, bandits and a blue dragon are raiding the town. The cult of the dragon must be stopped.
- **Page breaks after:** (none)

## Catching the Cult
- **Opened:** 27 Marpenoth 1489 DR (S11)
- **Description:** The cult has dispersed with the stolen cargo. The party tries to find them.
- **Page breaks after:** 
    - 2 Uktar 1489 DR, S12, 2

## The Trade Way
- **Opened:** 6 Uktar 1489 DR (S14)
- **Description:** A long caravan journey up the Trade Way, with the heroes riding alongside the suspected cultists.
- **Page breaks after:** (none)
