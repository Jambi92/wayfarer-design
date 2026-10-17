# RAC RM-OT-05AU — post-acceptance deferred-item audit from frozen 05AT body

**Authority:** Tyler has author-approved the 05AT Gorrund body composition.
**Date:** 2026-10-17.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Author acceptance:** `reviews/tyler-rac-rm-ot-05at-gorrund-body-composition-author-acceptance.md`
**Accepted source:** `GO-05AT_AC3`

## 1. Purpose

The Gorrund body composition is now AUTHOR ACCEPTED / FROZEN.

Do not reopen AC1, AC2 or AC3.

This order is a **diagnostic and recommendation block only** for the previously deferred Gorrund items that were intentionally held until composition acceptance.

No geometry authoring is authorized in 05AU.

## 2. Frozen advancement source

Use:

`GO-05AT_AC3.blend`
SHA-256:
`d462f36c08a3b528aff5b4408539f7dfe704b513585da6f2923136c60b7ea618`

Review GLB:
`GO-05AT_AC3.glb`
SHA-256:
`8ae6ccedffa5098ceb1fad18583edb18d2243060faf942bec933e79899c9fc0d`

The accepted body composition must remain byte/geometry unchanged throughout this audit.

## 3. Deferred items to audit

Audit these one at a time:

1. **Head share / head proportion**
2. **Tail-root final visual judgment**
3. **Heel lift**
4. **Final foot-size judgment**
5. **Genus handles / remaining morph handles**
6. Any other Gorrund item explicitly logged as deferred in the RM-OT-05 evidence/history

Do not invent new open issues.

## 4. Head-share audit

Verify from current 05AT geometry:

- total stature;
- head-height definition used in prior W1/AB comparisons;
- current head share as % of stature;
- accepted W1 reference head share;
- absolute and percentage difference.

Prior project notes indicated roughly:
- current post-reproportion head share ≈ 10.5%;
- accepted W1 ≈ 12.6%.

Treat those only as historical pointers. Recalculate from source evidence.

Produce:
- whole front/profile/3-4;
- head/shoulder crop;
- silhouette overlay current 05AT vs accepted W1 guide, aligned by stature and pelvis/shoulder landmarks;
- one optional **visual-only mock comparison** showing what the accepted W1 head share would imply.

Do not alter the mesh.

Return recommendation:
- KEEP 05AT HEAD SHARE
- or HEAD-SHARE LOCAL CORRECTION RECOMMENDED

State why in visual/anatomical terms, not only percentages.

## 5. Tail-root audit

The AC3 continuity treatment is accepted as part of the body composition and must not be broadly reopened.

Audit only:
- emergence position;
- midline relationship;
- fused-root length before free tail separates;
- root angle;
- transition into sacrum/glutes;
- whether it still reads as a natural leonine tail origin.

Compare:
- accepted 05AT;
- accepted W1 guide;
- any prior canonical tail-root description.

Do not move the tail.

Return:
- KEEP 05AT TAIL ROOT
- or BOUNDED TAIL-ROOT LOCAL CORRECTION RECOMMENDED

Any recommended correction must explicitly preserve the accepted AC3 posterior and identify a maximum local region.

## 6. Heel-lift audit

Measure:
- plantar contact points;
- heel vertical offset relative to forefoot/ground plane;
- left/right symmetry;
- current raw heel lift in mm/cm;
- stance consequence.

Prior notes mentioned approximately 1–1.6 cm raw heel lift. Recalculate.

Determine whether this is:
- anatomically acceptable for this Gorrund design;
- merely a source-pose artifact;
- likely to cause future rig/ground-contact issues.

Return:
- KEEP
- or LOCAL HEEL/FOOT CORRECTION RECOMMENDED

No changes yet.

## 7. Final foot-size audit

Compare foot size against:
- stature;
- lower-leg length;
- ankle size;
- accepted W1 macro proportions;
- broad-frame/load-bearing Gorrund identity.

Measure:
- foot length / stature;
- foot width / stature;
- foot length / tibial segment;
- left/right symmetry.

Produce whole-body and foot close views.

Return:
- KEEP CURRENT FOOT SIZE
- or LOCAL FOOT-SIZE CORRECTION RECOMMENDED

Do not alter toes/feet in 05AU.

## 8. Genus handles / morph-handle audit

Identify every Gorrund morphology parameter / genus handle still OPEN after the race-design and W1 work.

For each:
- exact name;
- purpose;
- whether current 05AT geometry already demonstrates a viable neutral midpoint;
- whether author input is still required;
- whether it can safely remain OPEN until creator implementation.

Do not invent a handle merely because a dimension can be measured.

Return a table:
- HANDLE
- STATUS
- CURRENT EVIDENCE
- RECOMMENDATION
- AUTHOR DECISION NEEDED? yes/no

## 9. Canon / race-identity audit

Confirm the accepted 05AT body still satisfies the established Gorrund identity:

- beastfolk;
- leonine/lion-like head;
- tail;
- large skeletal frame;
- ordinary/untrained soft tissue rather than bodybuilder;
- plantigrade body guardrails unless later canon explicitly superseded them.

Flag any actual contradiction.

Do not reinterpret the race.

## 10. No-authoring rule

05AU is diagnostics only.

Forbidden:
- sculpting;
- filtering;
- vertex movement;
- topology change;
- remesh;
- tail edits;
- head scaling;
- foot scaling;
- pose changes that are saved into the advancement source.

Temporary camera/viewport/measurement setup is allowed.

Any derived visual mock must be clearly labeled NON-AUTHORED / VISUAL ONLY.

## 11. Deliverable

Return:

`reviews/claude-rac-rm-ot-05au-gorrund-deferred-item-audit.md`

Evidence:

`reviews/rac-rmot05au-evidence/`

Include:
- exact measurements;
- comparison sheets;
- recommendation for each deferred item;
- list of any additional historically deferred Gorrund items found in repo evidence;
- a final compact decision matrix.

## 12. Stop condition

After the audit, STOP.

Do not perform any correction until ChatGPT/Tyler reviews the recommendations.

Return status:

**05AU DEFERRED-ITEM AUDIT COMPLETE / AUTHOR REVIEW REQUIRED**

## 13. State

- Gorrund BODY COMPOSITION: AUTHOR ACCEPTED / FROZEN
- Gorrund overall mesh: NOT YET FINAL
- Grask E3: FROZEN
- RM-OT-05: OPEN
- Stage C: BLOCKED
- no D4 / UE5 / production rigging / creator implementation
