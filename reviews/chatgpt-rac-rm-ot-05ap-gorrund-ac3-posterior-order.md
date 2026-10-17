# RAC RM-OT-05AP — AC3 posterior/glute neutralization from frozen 05AO AC2

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05AO AC2 PASS.
**Date:** 2026-10-16.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05ao-gorrund-upper-arm-neutralization-gate.md` (f7fc142).

## 1. Advancement source

Advance only from the frozen AC2 checkpoint:

`GO-05AO_AC2.blend`
SHA-256:
`ba129999cfe71c1ab7afc2f11c1b911bd1e85fc06f301e1bad9a483fcba4f6f3`

Review GLB:
`GO-05AO_AC2.glb`
SHA-256:
`1f60fb33fa0c75c9d0f9aa0c1315143005473fd5c72ada67ad922782240de434`

All earlier rejected AC2 attempts remain evidence only.

## 2. AC3 decision

AC3 is required.

05AO visual evidence shows:
- glutes remain strongly round and projected in back/profile;
- the posterior thigh/glute transition still carries a heroic donor read;
- this remains inconsistent with the target:
  **large-frame Gorrund + ordinary untrained soft tissue**.

Do not reopen AC1 or AC2 regions except for tiny required continuity bands.

## 3. AC3 artistic target

Reduce the posterior heroic read while preserving the Gorrund pelvis and load-bearing frame.

### Reduce
- rounded bodybuilder glute projection;
- hard upper-glute shelf;
- strong gluteal cleft side bulges;
- lower-glute / posterior-thigh bodybuilder separation;
- hamstring groove definition if still visibly heroic.

### Preserve
- robust pelvis width/depth;
- sacral / pelvic structure;
- natural buttock volume;
- posterior thigh mass;
- stance;
- leg lengths;
- tail-root identity;
- tail-root fusion;
- genital/perineal interfaces.

Do **not** produce:
- flat buttocks;
- narrow pelvis;
- tucked-under pelvis;
- sagging / deflated glutes;
- hollowed sacrum;
- pinched tail root;
- altered tail angle;
- hamstring thinning.

## 4. Hard-protected regions

Hard protect:
- head / neck;
- entire passed AC1 torso;
- entire passed AC2 arms and legs except the smallest posterior-thigh continuity band needed at the glute fold;
- pelvis core / hip-joint centres;
- genital region;
- perineal fold;
- free tail;
- fused tail root;
- tail junction;
- hands / feet.

The tail root / junction are absolutely out of scope.

No sculpt/filter may change:
- tail root fusion;
- tail emergence height;
- tail angle;
- tail cross-section;
- genital landmark;
- perineal protected fold.

Required displacement for those regions:
**0.000 mm**

## 5. Posterior sculpt mask

Build a glute/posterior-thigh mask that is independent of front thigh/leg work.

Preferred:
- rig-label / vertex-ID based mask if box masking overlaps protected pelvis/tail geometry;
- feathered mask transitions.

### Sculptable
- gluteal soft-tissue bellies;
- lower glute fold;
- upper posterior thigh / hamstring belly only where needed for continuity.

### Strongly protected
- sacrum / pelvis core;
- hip joint centre;
- tail root and junction;
- genital / perineal region;
- lower posterior thigh and knee;
- already-neutralized leg muscle bellies outside the AC3 continuity band.

### Feathering
Use wide feathering at:
- glute-to-pelvis core;
- lower-glute-to-posterior-thigh;
- lateral glute-to-hip.

No hard mask edge may run through the middle of a buttock or glute fold.

Read back the saved mask and verify protected regions before any authoring.

## 6. Predictive stability gate

Use the cumulative-reference predictive workflow established in 05AL–05AO.

Before every authored AC3 step:
1. simulate the exact proposed filter/stroke behavior as closely as possible;
2. compare cumulatively against the current accepted AC2 reference;
3. flag:
   - flips;
   - >60° normal rotations;
   - new local inversions;
   - adjacent >60° folds;
4. repair only discrete predicted neighborhoods using the proven local method.

### Repair authority
Maximum across 05AP:
- 40 discrete repair neighborhoods;
- 3 repair-analysis cycles per proposed step;
- <= 0.5 mm vertex movement;
- <= 0.5 mm patch surface deviation;
- near-coplanar edge rotations only;
- 0.000 mm outside the repair union.

No generalized retopology.

## 7. Authoring method

Prefer uniform, mask-controlled UI filters over broad mouse-drag sculpt strokes.

Allowed:
- Mesh Filter Smooth;
- Mesh Filter Surface Smooth;
- tiny restrained Flatten/Smooth brush only for one isolated residual shelf;
- tiny Grab/Elastic only if absolutely needed for soft-tissue projection and if the tail/pelvis are fully protected.

Forbidden:
- Dyntopo;
- voxel remesh;
- broad pelvis scaling;
- tail-root reshaping;
- scripted final vertex shaping;
- broad posterior-thigh thinning.

All final shape authoring must occur through Blender UI.

## 8. AC3 buildup

Maximum **2 deliberate AC3 checkpoints**.

### AP1 — glute relief/projection reduction

Use a calibrated glute-only Smooth or Surface Smooth Mesh Filter.

Simulation should choose an event count that:
- clearly reduces glute roundness/projection;
- preserves pelvis width/depth;
- keeps posterior thigh mass;
- creates no tail-root or perineal displacement.

Suggested visual aim:
- glute projection reduced enough to stop reading bodybuilder;
- preserve a clearly substantial, natural Gorrund glute volume.

After AP1:
- run complete technical gate;
- render back/profile/3/4;
- if AC3 visual target is met, PASS.

### AP2 — one final refinement if needed

If AP1 is clean but residual heroic shelf/groove remains:
use one of:
- second restrained Smooth/Surface Smooth filter;
- one tiny local continuity touch at the lower glute fold.

Do not perform a third AC3 checkpoint.

## 9. Shape/mass preservation gates

Because the goal is soft-tissue neutralization, some glute volume reduction is expected.

Track:
- posterior pelvis width;
- buttock projection in profile;
- glute mean radius / local envelope;
- upper posterior thigh radius.

Hard constraints:
- pelvis bony/core width change <= **0.5%**
- hip-joint-centre drift <= **0.5 mm**
- upper posterior thigh mean-radius loss <= **3.0%**
- glute projection reduction may be larger, but must not create a flat/deflated appearance
- tail root/junction = 0.000 mm
- genital/perineal = 0.000 mm

Do not accept a result that solves the visual problem by shrinking the pelvis.

## 10. Technical gate after each checkpoint

Required:
- 0 opened seams;
- 0 self-intersections;
- 0 flipped faces;
- 0 degenerates;
- 1 position-welded component;
- 0 boundary / 0 non-manifold;
- head/torso/arms = 0.000 mm;
- passed leg regions outside allowed posterior continuity band = 0.000 mm;
- pelvis core within preservation limits;
- tail / tail root / tail junction = 0.000 mm;
- genital / perineal = 0.000 mm;
- hands / feet = 0.000 mm;
- stature / bbox unchanged;
- no new ridge, dent, hard mask line, or melted area.

If a real checkpoint fails technically:
- revert;
- one predictive-repair-and-rerun of that exact step is allowed.
If it fails again, STOP.

## 11. Visual gate

Compare:
- 05AO AC2;
- accepted W1 macro guide;
- body-only back/profile/3/4.

Required:
- glutes no longer read bodybuilder/heroic;
- buttocks remain substantial and natural;
- pelvis still reads broad/robust;
- lower-glute fold becomes softer;
- posterior thigh transition looks ordinary rather than sculpted;
- no tail-root pinching;
- no flattened or tucked pelvis;
- no obvious asymmetry;
- whole body reads consistently as:
  **large-frame Gorrund + ordinary untrained soft tissue**.

## 12. Output

If AC3 passes, freeze:

`GO-05AP_AC3.blend`
`GO-05AP_AC3.glb`

Record exact hashes.

## 13. Decision

### PASS
Return:

**05AP AC3 PASS / READY FOR FINAL Q1-Q2 + TYLER VISUAL REVIEW**

Then STOP.

Do not alter:
- head share;
- tail root;
- heel lift;
- final foot size;
- genus handles.

### FAIL
If AC3 cannot meet the visual target within two checkpoints without damaging protected anatomy:

**05AP AC3 NOT CREDIBLE / STOP**

Revert active composition state to `GO-05AO_AC2` and STOP.

## 14. Final evidence

Return:
- mask readback;
- predictor/repair logs;
- exact filter settings/event counts;
- glute projection metrics;
- pelvis width/hip drift;
- posterior-thigh radius change;
- geometry gates;
- identical-camera:
  - whole F/P/B/3/4;
  - body-only F/P/B/3/4;
  - close posterior B/P/3/4;
  - 05AO AC2 vs 05AP AC3 comparisons;
- Q1/Q2 pre-review sheet.

## 15. State

Until Tyler visually accepts final composition:
- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED;
- no LOW / blind final acceptance / scaffold;
- no D4 / UE5 / production rigging / creator implementation.

## 16. Return

Commit:

`reviews/claude-rac-rm-ot-05ap-gorrund-ac3-posterior-gate.md`

Evidence:

`reviews/rac-rmot05ap-evidence/`
