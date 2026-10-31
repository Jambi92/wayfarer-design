# ChatGPT Standing Directive — Claude Internal Audit Must Pass Before Submission

**Repository:** `Jambi92/wayfarer-design`  
**Applies to:** all future Claude production / audit work unless an order explicitly overrides it  
**Status:** ACTIVE WORKFLOW RULE

## Submission gate

Claude must **not** return work to ChatGPT / Tyler for review while Claude's own required audit still reports:

- NEEDS REVISION;
- FAIL;
- incomplete mandatory checks;
- unresolved blocker that Claude is already authorized to attempt;
- missing required evidence;
- unfinished closure steps.

Claude must continue iterating internally until one of these is true:

### A. Internal audit PASS
Claude's own gate says the work passes the ordered requirements and is ready for ChatGPT / author review.

### B. Genuine author decision required
Claude has reached a true decision that cannot be resolved under the existing order without changing canon, accepted tolerances, scope, architecture, or an explicit author choice.

### C. Hard external blocker
A required resource, permission, source, tool, or dependency is unavailable and Claude cannot proceed without external action.

## Required behavior

1. Do not submit intermediate WIP states merely because progress was made.
2. If a local technical blocker is fixable under the current order, fix it and rerun the audit.
3. If the audit itself identifies bounded corrective actions already within scope, perform them before returning.
4. Repeat this loop until the internal gate is PASS, genuine AUTHOR DECISION, or hard EXTERNAL BLOCKER.
5. Every final handoff must state one of:
   - PASS — READY FOR CHATGPT / AUTHOR REVIEW;
   - REQUIRES AUTHOR DECISION — [exact decision];
   - BLOCKED — [exact external blocker].
6. "NEEDS REVISION" is an internal working state, not a submission state, unless the revision would require a new author order.
7. Do not begin the next race / phase while the current ordered work is still below its submission gate.

## ChatGPT / author role

Once Claude's own audit passes:
- ChatGPT independently checks the evidence;
- ChatGPT either approves the work or sends corrective changes.

Claude's own PASS is necessary for submission, but does not guarantee ChatGPT approval.

This standing rule restores the previous Wayfarer review cadence.
