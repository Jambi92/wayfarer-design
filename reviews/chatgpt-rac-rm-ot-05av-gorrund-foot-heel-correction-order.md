# RAC RM-OT-05AV — bounded Gorrund foot-size and heel-stance correction

**Authority:** Tyler-approved 05AU deferred-item ruling.
**Date:** 2026-10-17.
**Repository:** Jambi92/wayfarer-design, main.
**Author ruling:** reviews/tyler-rac-rm-ot-05au-gorrund-deferred-item-author-ruling.md
**Audit:** reviews/claude-rac-rm-ot-05au-gorrund-deferred-item-audit.md

## 1. Purpose

Perform the one authorized local correction remaining before final Gorrund closure review:

- reduce oversized feet to the approved neutral target;
- correct the asymmetric heel lift;
- preserve the accepted body, head, tail, ankles and lower-leg proportions.

Do not reopen AC1, AC2 or AC3.

## 2. Frozen source

Start only from:

GO-05AT_AC3.blend
SHA-256:
d462f36c08a3b528aff5b4408539f7dfe704b513585da6f2923136c60b7ea618

Review GLB:
GO-05AT_AC3.glb
SHA-256:
8ae6ccedffa5098ceb1fad18583edb18d2243060faf942bec933e79899c9fc0d

## 3. Author-approved neutral targets

Using the current accepted stature:

### Foot length
Target each foot:
- approximately 17.0% of stature;
- target approximately 34.8 cm;
- final left/right difference <= 0.3 cm.

### Foot width
Target each footprint:
- approximately 7.5% of stature;
- target approximately 15.3 cm;
- final left/right difference <= 0.3 cm.

A small tolerance is allowed if needed to preserve clean anatomy:
- length: 34.5–35.1 cm;
- width: 15.0–15.6 cm.

Do not return to the W1 15.1% foot length. Gorrund feet should remain visibly large in absolute terms.

### Heel stance
Target each heel:
- heel-pad clearance relative to the ground / forefoot: 0.3–0.5 cm;
- heel and ball must both participate in plantigrade ground contact;
- left/right heel-lift difference <= 0.15 cm.

### Preserve
- five toes;
- ordinary nails;
- non-prehensile form;
- ankle breadth and ankle joint location;
- accepted shin/calf form above the ankle;
- accepted stance width and leg length.

## 4. Hard-protected anatomy

Required 0.000 mm movement:
- head;
- torso;
- pelvis;
- tail and tail root;
- arms/hands;
- thighs/knees;
- shin/calf above the ankle-transition buffer;
- genital/perineal;
- ankle joint centres.

The local working region is:
- foot geometry;
- heel;
- toes;
- sole;
- only the minimum ankle-foot transition buffer needed for continuity.

Do not resize the ankle to make the smaller foot look easier.

## 5. Pre-authoring measurement and transform plan

Before changing geometry, recompute independently from the frozen source:

For each foot:
- local long axis;
- local width axis;
- length;
- footprint width;
- heel minimum;
- ball minimum;
- heel lift versus ball;
- ankle joint centre;
- plantar contact span.

Then build a diagnostic-only proposed transform.

Preferred approach:
- non-uniform local foot scaling around a stable ankle/heel pivot;
- length and width controlled independently;
- transition weight fades to zero before the protected ankle joint;
- vertical/plantar correction handled separately from length/width reduction.

Do not blindly scale all three axes uniformly.

Predict the proposed result before UI authoring.

## 6. Authoring method

Final shape authoring must occur in Blender UI.

Allowed:
- Edit Mode local scaling;
- proportional/local transform with protected ankle selection;
- masked Grab / Elastic Deform;
- restrained Smooth for continuity;
- local rotate/settle of foot soft-tissue geometry around the fixed ankle if needed for plantigrade contact.

Diagnostic scripts may:
- calculate axes/measurements;
- create selection lists / vertex groups;
- simulate transforms;
- validate geometry;
- generate evidence.

Forbidden:
- scripted final vertex positioning;
- whole-body scale;
- shin shortening;
- ankle relocation;
- Dyntopo;
- voxel remesh;
- broad remeshing.

## 7. Recommended sequence

### AV1 — size correction

Correct one foot at a time or both symmetrically.

Bring:
- length into 34.5–35.1 cm;
- footprint width into 15.0–15.6 cm.

Preserve:
- toe count;
- toe spacing hierarchy;
- natural forefoot taper;
- heel shape;
- ankle joint location.

Do not create a rectangular slab or narrow human foot.

Save and gate.

### AV2 — heel/ground correction

From a clean AV1 result:

Bring both heels to:
- 0.3–0.5 cm heel-pad clearance;
- full plantigrade support with heel and ball participating in contact.

Correct the current right-foot hover/asymmetry.

The ankle joint itself remains fixed.

Save and gate.

### AV3 — optional continuity pass

Only if needed:
- one tiny UI Smooth/Grab cleanup at the ankle-foot transition or plantar surface.

No broad foot resculpt.

## 8. Symmetry rule

The feet should be neutral counterparts.

Required:
- length difference <= 0.3 cm;
- width difference <= 0.3 cm;
- heel-lift difference <= 0.15 cm;
- visually matched toe spread and heel stance.

Do not mirror one entire foot blindly if that would overwrite valid left/right anatomy. Use measurements and local matching.

## 9. Technical gates after every checkpoint

Required:

- 0 opened seams;
- 0 self-intersections;
- 0 flipped faces;
- 0 degenerates;
- 1 position-welded component;
- 0 boundary;
- 0 non-manifold;
- all protected anatomy 0.000 mm;
- ankle joint centres <= 0.2 mm drift, target 0.000 mm;
- stature unchanged;
- body bbox above the feet unchanged;
- no new toe contact/fusion;
- no sole collapse;
- no heel dent;
- no ankle shelf;
- no visible transform seam.

The three known topological connectivity defects from 05AU are out of scope and remain carried to retopology/rig prep. Do not repair them here.

## 10. Visual gate

Compare frozen 05AT against the corrected result.

Required:
- feet still look large enough for a broad-frame beastfolk;
- no oversized monster-foot/slab read;
- width now harmonizes with the ankle and lower leg;
- length no longer dominates the short lower leg;
- both feet sit naturally under the body;
- heels read plantigrade rather than forefoot-only;
- toes remain believable and non-prehensile;
- no obvious left/right mismatch;
- accepted body above the ankles looks unchanged.

## 11. Final output

If the correction passes, freeze:

GO-05AV_feet_final.blend
GO-05AV_feet_final.glb

Record exact hashes.

## 12. Decision

### PASS

Return:

**05AV FOOT/HEEL CORRECTION PASS / READY FOR FINAL GORRUND CLOSURE REVIEW**

Then STOP.

Do not begin:
- hand/axilla connectivity repairs;
- retopology;
- rigging;
- creator implementation;
- Stage C.

### FAIL

If the target cannot be reached without damaging ankle/lower-leg anatomy:

**05AV FOOT/HEEL CORRECTION NOT CREDIBLE / STOP**

Revert active geometry to GO-05AT_AC3 and STOP.

## 13. Evidence

Return:

reviews/claude-rac-rm-ot-05av-gorrund-foot-heel-correction-gate.md

Evidence:

reviews/rac-rmot05av-evidence/

Include:
- before/after measurements L/R;
- local transform plan;
- exact UI operations;
- technical gates;
- protected-region displacement report;
- plantar profile plots;
- foot front/back/profile/3-4 views;
- whole-body F/P/B/3-4 before/after comparison;
- final symmetry metrics.

## 14. State

- Gorrund BODY COMPOSITION: AUTHOR ACCEPTED / FROZEN
- Head share: AUTHOR APPROVED / FROZEN
- Tail root: AUTHOR APPROVED / FROZEN
- Feet + heel stance: IN CORRECTION
- Connectivity cleanup: CARRIED TO RETOPOLOGY / RIG PREP
- Gorrund overall mesh: NOT YET FINAL
- Grask E3: FROZEN
- RM-OT-05: OPEN
- Stage C: BLOCKED
- no D4 / UE5 / production rigging / creator implementation
