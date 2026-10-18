# RAC RM-OT-05AW1 — dedicated Gorrund feline toenail rebuild from clean 05AV

**Authority:** Tyler visual rejection of 05AW and explicit request for a proper rework.
**Date:** 2026-10-17.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Author rejection / reopen:** `reviews/tyler-rac-rm-ot-05aw-05ax-author-rejection-and-reopen.md`

## 1. Purpose

Rebuild the Gorrund toenail morphology from the clean 05AV feet.

The prior 05AW result is REJECTED because it reads as:
- cracked / chipped toenails;
- split nail plates;
- pinched central grooves;
- faceted damaged keratin rather than clean feline nail anatomy.

This order is a deeper local toenail rework, not another bounded Hook-only deformation.

## 2. Mandatory source

Start only from:

`GO-05AV_feet_final.blend`
SHA-256:
`45a04787c4760e95b9a9bef52837a516788670f1f1bade92c380ffcea74ab9a6`

Review GLB:
`GO-05AV_feet_final.glb`
SHA-256:
`b595f11e2cb4d6f69cdc38954fc9f422dadda9e8e46cee8aed57869face92b4b`

Do not use GO-05AW_nails_final as an advancement source.

It may be used only as rejected evidence.

## 3. Locked accepted anatomy

Do not change:
- foot length;
- foot width;
- heel stance;
- plantar contact;
- toe count;
- toe spacing;
- toe length;
- toe base size;
- ankle size or position;
- lower-leg proportions;
- body composition;
- head;
- tail;
- hands.

All accepted 05AV geometry outside the nail work regions is frozen.

## 4. Final visual target

The toenails must read as **clean, continuous, naturalistic large-feline nail forms**.

Required visual language:
- smooth keratin surface;
- no crack / split read;
- no chipped edge read;
- no recessed broken-plate appearance;
- clean proximal nail-bed integration;
- controlled taper from root toward tip;
- visibly sharper distal end than a human toenail;
- modest forward/downward curvature;
- modest projection beyond the soft toe;
- coherent species language across both feet.

The goal is a large-wild-cat influence in a neutral standing presentation.

## 5. Stage A — nail-surface restoration

Before shaping a feline tip, first fix the source plate defects.

On each visible nail:
- smooth / fill the inherited central split;
- remove the recessed broken rim read;
- restore a single continuous convex nail surface;
- remove chipped/faceted silhouettes;
- preserve the surrounding toe pad.

Preferred Blender-UI tools:
- Smooth / Surface Smooth;
- Inflate / Clay / Fill where needed to restore the sunken plate;
- restrained Flatten only to remove a local break;
- local Grab for nail-bed continuity.

Do not sharpen or project the nail until the surface-restoration gate passes.

### Stage A gate

For each nail:
- one continuous visible nail surface;
- no obvious center crack;
- no chipped rim;
- no deep recessed plate;
- no toe deformation outside the immediate nail bed;
- 0 SI / flips / degenerates.

Render close orthographic and 3/4 comparisons.

If the crack/split read is not removed, do not proceed to Stage B.

## 6. Stage B — feline shaping

From a passing Stage A checkpoint:

Shape each restored nail into a restrained feline form.

Target:
- narrow distal taper;
- smooth point or rounded point;
- slight forward projection;
- slight downward curve;
- no deep center line;
- no exaggerated hook;
- no fantasy talon.

The largest toe may have the broadest / most substantial nail, but the same anatomy language should carry across all visible toes.

Allowed:
- local Grab;
- local scale/taper in Edit Mode;
- restrained Pinch/Crease only if it does not recreate a crack-like groove;
- Smooth to preserve continuous surface;
- local masks / vertex groups.

## 7. Optional local topology exception

If the inherited Rodin nail plate cannot be made continuous by sculpting alone, Claude is authorized to perform a **strictly local nail-plate topology repair** on that nail only.

Allowed:
- dissolve / retriangulate obviously broken sliver faces inside the nail plate;
- bridge or fill a tiny local nail-surface defect;
- local edge rotation;
- merge coincident nail-plate vertices if they are part of the visible split.

Forbidden:
- remeshing the toe;
- Dyntopo;
- voxel remesh;
- broad retopology;
- changing toe silhouette.

Any topology change must:
- remain inside the nail plate + immediate nail-bed transition;
- preserve foot and toe dimensions;
- produce 0 boundary / non-manifold / SI / flips / degenerates.

Record every topology edit.

## 8. Iteration budget

Tyler is away and authorizes substantial autonomous work.

Claude may use up to **3 deliberate nail checkpoints**:

- AW1-A: surface restoration;
- AW1-B: feline shaping;
- AW1-C: one final cleanup / symmetry refinement if needed.

Do not stop after the first technically valid attempt if the nails still visibly read cracked, chipped or human-like.

Self-review the evidence after each checkpoint.

Choose the best technically clean and visually credible result.

## 9. Projection and dimension limits

The accepted foot dimensions remain the priority.

Hard limits versus 05AV:
- foot-length increase <= **3 mm** per foot;
- footprint width change <= **1 mm**;
- heel lift change <= **0.1 cm**;
- ankle joint-centre drift <= **0.2 mm**.

No nail may intersect the ground plane.

No nail may intersect an adjacent toe.

## 10. Technical gate

Final candidate requires:

- 0 opened seams;
- 0 self-intersections;
- 0 flipped faces;
- 0 degenerates;
- 1 component / 0 boundary / 0 non-manifold;
- no new toe fusion/contact;
- no ground intersection;
- no movement outside nail + immediate nail-bed support;
- accepted 05AV foot dimensions within §9;
- heel and plantar stance preserved;
- ankle unchanged;
- everything above the feet unchanged.

Known hand/axilla connectivity debt remains out of scope.

## 11. Visual gate

PASS only if all of these are true:

- cracked toenail read is gone;
- central split read is gone;
- chipped/broken-plate read is gone;
- nail surface is smooth and continuous;
- distal taper is clearly feline;
- tip is sharper than a human toenail;
- curve/projection are restrained and believable;
- feet still read natural, large and plantigrade;
- left/right result is coherent;
- no exaggerated fantasy appearance.

If the result still reads cracked/chipped in close views, it is FAIL even if technical gates pass.

## 12. Output

If PASS, freeze:

`GO-05AW1_nails_final.blend`
`GO-05AW1_nails_final.glb`

Record exact hashes.

## 13. Evidence

Return:

`reviews/claude-rac-rm-ot-05aw1-gorrund-toenail-rework-gate.md`

Evidence:

`reviews/rac-rmot05aw1-evidence/`

Include:
- rejected 05AW vs 05AV vs 05AW1 comparison;
- close front/top/profile/3-4 views of both feet;
- per-nail closeups;
- Stage A restoration evidence;
- Stage B shaping evidence;
- exact UI operations;
- any topology-edit log;
- technical gates;
- protected-region displacement;
- final foot measurements;
- whole-body confirmation sheet.

## 14. Decision

### PASS

Return:

**05AW1 TOENAIL REWORK PASS / READY FOR FINAL GORRUND CLOSURE REVIEW**

Then STOP 05AW1.

### FAIL

Return:

**05AW1 TOENAIL REWORK FAILED / AUTHOR REVIEW REQUIRED**

Do not run final closure.

## 15. State

- Gorrund BODY COMPOSITION: AUTHOR ACCEPTED / FROZEN
- Head share: AUTHOR APPROVED / FROZEN
- Tail root: AUTHOR APPROVED / FROZEN
- Foot size + heel stance: AUTHOR APPROVED / FROZEN
- Toenail morphology: IN REWORK
- RM-OT-05: OPEN
- Stage C Gorrund blocker: BLOCKED
- Grask E3: FROZEN
- connectivity cleanup: CARRIED TO RETOPOLOGY / RIG PREP
