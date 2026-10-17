# RAC RM-OT-05AT — AC3 two-mask posterior finish

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05AS.
**Date:** 2026-10-17.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05as-gorrund-ac3-short-cleanup-gate.md` (78e6b76).

## 1. Author ruling

05AS established the core conflict:

- a short cleanup with the wide boundary mask passes every technical and dihedral gate but leaves the posterior too round/heroic;
- a long cleanup creates the desired softer glute volume/fold but folds the lateral transition band.

Therefore AC3 will now use **two separate masks for two separate jobs**:

1. **Mask A — belly authoring mask:** allow deflate + long Smooth only on the glute/posterior soft-tissue belly while keeping the transition band strongly protected.
2. **Mask B — boundary blend mask:** after the belly shape is authored, swap only the `.sculpt_mask` attribute on the saved geometry, then perform a short Smooth pass across the wide feathered transition.

This directly separates interior volume shaping from boundary continuity.

## 2. Advancement source

Start only from:

`GO-05AO_AC2.blend`
SHA-256:
`ba129999cfe71c1ab7afc2f11c1b911bd1e85fc06f301e1bad9a483fcba4f6f3`

Review GLB:
`GO-05AO_AC2.glb`
SHA-256:
`1f60fb33fa0c75c9d0f9aa0c1315143005473fd5c72ada67ad922782240de434`

Do not advance from rejected AQ/AR/AS geometry.

Those states are evidence only.

## 3. Reuse solved structural rules

Reuse the 05AR solution exactly:

### Immutable tail core
- all free-tail vertices;
- tail-junction vertices within 8 mm of the tail/junction interface;
- centroid, emergence height, root axis, root width/depth, free tail = **0.000 mm**.

### Tail continuity ring
- outer junction continuity tissue;
- max displacement <= **3.0 mm**.

### Duplicate seams
- duplicate-position seam copies must have identical mask values;
- pin duplicate seam vertices to mask 1.0;
- maintain at least a 30 mm ramp.

These rules are solved and are not to be redesigned unless simulation shows a mandatory local correction.

## 4. Mask A — belly authoring mask

Mask A exists to create the desired posterior volume/fold without allowing the lateral/front-thigh transition to participate in the long Smooth.

### Sculptable core
Include:
- glute belly;
- lower-glute soft-tissue belly;
- medial/lateral glute interior away from boundary bands;
- posterior upper-thigh belly only where required to soften the lower fold.

### Strongly protected boundary band
Mask A must keep the following at or near 1.0:
- lateral hip transition;
- front-lateral thigh transition;
- lower posterior-thigh transition;
- pelvis/sacral core;
- tail core;
- duplicate seams;
- genital/perineal;
- torso/arms/lower legs.

Use a broad protective band around the edge of the belly zone so long smoothing cannot pull against fixed neighbours and create the 05AR stripe.

### Tail transition
The continuity ring may retain the proven distance-driven ramp from 05AR, but the belly Smooth must not produce a visible tail plateau.

## 5. Stage A authoring — deflate + belly-only long Smooth

### Deflate
Use the proven UI deflate:

- Mesh Filter: Inflate;
- Strength approximately 0.020;
- negative ~100 px drag;
- about 7.9 mm x (1-mask) in fully sculptable belly tissue.

Do not increase strength in 05AT unless simulation proves the exact two-mask route otherwise cannot reach the visual target and all hard limits remain safe. Default is **same deflate as AQ/AR**.

### Belly Smooth
Use UI Smooth Mesh Filter with Mask A.

Simulate candidate counts:
- 80;
- 100;
- 120;
- 140;
- 160 events.

The belly-only long Smooth may be longer than AS because the transition band is protected.

Choose the **lowest** count that produces:
- no heroic roundness;
- softer lower-glute fold;
- no interior dents;
- no tail plateau;
- no lateral boundary crease in the simulated result.

### Stage A predictor
Before authoring, require:
- 0 SI;
- 0 flips;
- 0 collapse/degenerates;
- no new internal dihedral increase > 25° inside the sculptable belly;
- no transition-band dihedral increase > 12° because the band should be nearly static;
- continuity ring <= 3.0 mm;
- tail core 0.000 mm;
- pelvis/hip/thigh gates pass.

### Stage A output
Save:

`GO-05AT_A.blend`

Export review GLB.

Run full technical and visual gate before proceeding.

If Stage A cannot produce a credible belly shape without defects, STOP:
**05AT MASK-A BELLY AUTHORING NOT CREDIBLE / STOP**

## 6. Authorized mask-only swap between UI stages

If Stage A passes:

Claude is explicitly authorized to create a copy of the **saved Stage A geometry** and replace only its `.sculpt_mask` point attribute with Mask B using the existing validated mask-writing script method.

This operation is allowed because:
- it must produce **0.000 mm geometry change**;
- it does not author final vertex positions;
- all final shape changes remain Blender-UI filter operations.

Required proof before Stage B:
- vertex coordinates identical byte-for-byte or numerically 0.000 mm;
- topology identical;
- only mask attribute differs;
- Stage A geometry hash/source recorded.

Save mask-swapped working file as:

`GO-05AT_B_prep.blend`

## 7. Mask B — wide boundary blend mask

Mask B exists only to blend Stage A into the surrounding protected anatomy.

Reuse/improve the successful AS wide feather:

- lateral hip transition >= **80 mm**;
- front-lateral thigh transition >= **80 mm**;
- posterior-thigh transition >= **50 mm**;
- solved tail-core/ring ramp;
- duplicate seams pinned;
- graph Lipschitz slopes no steeper than 1/80 mm in lateral/front thigh and 1/50 mm elsewhere.

### Critical difference from Mask A
The Stage A belly interior should be **strongly protected or only lightly sculptable** under Mask B.

Stage B is not allowed to repeat the long belly shrink.

Its job is only to blend the boundary.

## 8. Stage B authoring — short boundary Smooth

Run simulation from actual Stage A geometry with Mask B.

Test:
- 3;
- 5;
- 8;
- 10;
- 15;
- 20 events.

Choose the lowest count that gives clean continuity.

Required predictor gate:
- 0 SI;
- 0 flips;
- 0 collapse;
- max new transition-edge dihedral increase <= **20°**;
- no new absolute transition edge > 35° unless already >=35° at Stage A;
- no coherent crease chain > 40 mm;
- tail core 0.000 mm;
- continuity ring <= 3.0 mm.

Then author exactly that short Smooth in Blender UI.

No long Stage B cleanup is allowed.

## 9. One bounded rerun

05AT allows:
- one primary Stage A + Stage B sequence;
- one bounded rerun only if a small technical/mask issue is found.

A rerun must restart from GO-05AO_AC2.

Allowed adjustments:
- Mask A boundary protection;
- Mask B feather;
- local predictive protection;
- lower/equal Smooth counts.

Not allowed on rerun:
- stronger deflate without explicit diagnostic justification;
- broader redesign;
- extra third mask;
- repeated brush cleanup.

## 10. Shape-preservation gates

Against GO-05AO_AC2:

### Tail core
- 0.000 mm.

### Tail continuity ring
- <= 3.0 mm.

### Pelvis
- width change <= 0.5%.

### Skeletal hip
- drift <= 0.5 mm.

### Upper posterior thigh
- mean-radius loss <= 3.0%.

### Other finished anatomy
- arms = 0.000 mm;
- torso outside AC3 field = 0.000 mm;
- lower legs = 0.000 mm;
- genital/perineal = 0.000 mm;
- hands/feet = 0.000 mm.

### Buttock depth
Report left/right mean posterior-depth reduction.
Visual gate governs; do not chase a number.

## 11. Technical gate

Final Stage B result must have:

- 0 opened seams;
- 0 SI;
- 0 flips;
- 0 degenerates;
- 1 component / 0 boundary / 0 non-manifold;
- duplicate seam pairs closed;
- tail core unchanged;
- ring <= 3.0 mm;
- stature / bbox unchanged;
- pelvis/hip/thigh gates pass;
- transition-edge dihedral increase <= 20°;
- no coherent crease chain;
- no tail plateau;
- no lateral stripe;
- no mask shelf/dent.

## 12. Visual gate

Compare:
- GO-05AO_AC2;
- rejected AR1r;
- predicted AS short-cleanup state;
- final 05AT.

Required:
- retain AR1r-like posterior softening;
- avoid AR1r's lateral/front-thigh folds;
- tail-root blend remains smooth;
- no jagged plateau;
- lower-glute fold soft and continuous;
- buttocks remain substantial/natural;
- no bodybuilder roundness;
- no flat/deflated read;
- no vertical lateral stripe;
- pelvis remains broad;
- posterior thigh remains robust.

The desired result is essentially:
**AR1r's posterior softness + AS's clean boundaries.**

## 13. Final AC3 output

If PASS, freeze:

`GO-05AT_AC3.blend`
`GO-05AT_AC3.glb`

Record exact hashes.

## 14. Decision

### PASS
Return:

**05AT AC3 PASS / READY FOR FINAL Q1-Q2 + TYLER VISUAL REVIEW**

Then STOP.

Do not alter:
- head share;
- tail redesign beyond the authorized continuity ring;
- heel lift;
- final foot size;
- genus handles.

### FAIL
Return:

**05AT TWO-MASK AC3 NOT CREDIBLE / STOP**

Revert active composition state to GO-05AO_AC2.

## 15. Evidence

Return:
- Mask A visualization/readback;
- Stage A simulation table;
- exact Stage A UI settings;
- Stage A gates/renders;
- proof of 0.000 mm geometry change during mask-only swap;
- Mask B visualization/readback;
- Stage B simulation table;
- exact Stage B UI settings;
- final geometry/dihedral gates;
- tail core/ring metrics;
- pelvis/hip/thigh metrics;
- buttock-depth change;
- identical-camera:
  - whole F/P/B/3/4;
  - body-only F/P/B/3/4;
  - posterior close B/P/3/4;
  - AO2 vs AR1r vs AS-predicted vs AT;
- final Q1/Q2 pre-review sheet if PASS.

## 16. State

Until Tyler visually accepts final composition:
- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED;
- no LOW / blind final acceptance / scaffold;
- no D4 / UE5 / production rigging / creator implementation.

## 17. Return

Commit:

`reviews/claude-rac-rm-ot-05at-gorrund-ac3-two-mask-gate.md`

Evidence:

`reviews/rac-rmot05at-evidence/`
