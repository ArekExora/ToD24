---
name: Grep-after-edit consistency check
description: After any edit that retracts, drops, or renames a distinctive term, grep the same file (and wider when the term spans files) for downstream references before claiming the edit is done. Edits that name a thing must propagate; this is the check.
type: feedback
---

After any edit that **retracts, drops, or renames** a distinctive term — a section name, a tag, a rule, a fix-it artifact, a follow-up — grep the same file (and the wider repo when the term spans files) for downstream references, and either update or remove every stale mention **before** claiming the edit is done.

**Why:** during the S6 retro work, the GM asked me to drop the `## Blocking issues` digest from the priority-taxonomy decision. I edited the decision section but left a follow-up action item still naming the digest. The GM caught it: *"you left the Blocking issues in the follow up actions.... Why do I have to babysit every step you take?"* This is the same class as [[feedback_no_invention]] — the rule (consistency) was understood; enforcement was missing. A single grep on the dropped term would have caught it pre-claim.

**How to apply:**
- Trigger: any edit whose substance is a *retraction* (this thing is gone), *rename* (this thing is now called X), or *narrowing* (this thing now applies only in case Y). Additive edits — pure new content — don't need the check.
- Action: `grep -n <distinctive-term> <edited-file>` before sending "done". If the term plausibly spans the repo (a tag name, a file convention, a shared identifier), widen to `grep -rn` across the affected tree.
- Distinctive matters: short or generic terms (`done`, `apply`) will drown the grep in noise; pick the term that uniquely identifies the dropped thing (`Blocking issues`, `[T:N]`, `## Tentative anchors`). If nothing is distinctive enough to grep cleanly, scroll the file end-to-end instead.
- This is **enforcement**, not a vibes-check. Don't substitute *"I'm pretty sure I caught all the references"* for the actual command. The same prose-fluency reflex that drives invention also makes incomplete-propagation feel complete.
- The grep is part of the edit, not a separate task. "Done" is reserved for after the grep has returned clean (or every stale hit has been updated).
