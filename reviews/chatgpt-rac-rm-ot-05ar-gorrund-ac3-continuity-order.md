# RAC RM-OT-05AR — AC3 posterior continuity-ring correction and final deflate rerun

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05AQ.
**Date:** 2026-10-17.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05aq-gorrund-ac3-deflate-gate.md` (4fae001).

## 1. Author ruling

05AQ proved that the posterior volume direction is correct.

The numerically clean AQ1r result:
- reduced bodybuilder-like glute projection;
- preserved substantial buttock volume;
- preserved pelvis width;
- preserved skeletal hip;
- preserved upper-posterior thigh mass;
- preserved all hard-protected anatomy.

Its failure is isolated to **mask-boundary continuity**:
1. a jagged raised plateau tracing the irregular hard tail-junction border;
2. a vertical lateral hip/thigh crease tracing the lateral feather boundary.

Therefore:
- retain the ~8 mm deflate direction;
- do **not** increase deflate strength;
- redesign only the boundary continuity contract.

## 2. Advancement source

Start only from the frozen AC2 checkpoint:

`GO-05AO_AC2.blend`
SHA-256:
`ba129999cfe71c1ab7afc2f11c1b911bd1e85fc06f301e1bad9a483fcba4f6f3`

Review GLB:
`GO-05AO_AC2.glb`
SHA-256:
`1f60fb33fa0c75c9d0f9aa0c1315143005473fd5c72ada67ad922782240de434`

Do not advance from rejected AQ1 or AQ1r geometry.

AQ1r is evidence and visual target only.

## 3. Preserve the successful volume target

Use the AQ1r direction as the visual target:

- deflate calibration approximately:
  - Mesh Filter Inflate;
  - Strength 0.020;
  - ~−100 px drag;
  - ≈ 7.9 mm × (1 − mask) at the fully sculptable belly;
- followed by approximately the successful Smooth cleanup range.

Do not increase toward the old 15 mm feasibility state.

Required result should stay visually closer to **AQ1r / the 8 mm feasibility direction** than to the flatter 15 mm state.

## 4. Split tail protection into CORE vs CONTINUITY RING

The old all-or-nothing hard tail-junction mask is superseded.

### 4A. Immutable tail core — 0.000 mm

Define and hard-protect the true structural tail core:

- all free-tail vertices;
- the central/fused root tissue necessary to preserve:
  - tail emergence height;
  - root axis;
  - root cross-section;
  - root centreline;
  - tail angle;
  - tail thickness;
- the innermost tail-root interface where changing geometry would alter tail identity.

Required movement:
**0.000 mm**

No direct sculpting or filtering may move this core.

### 4B. Tail-junction continuity ring — limited motion allowed

The **outer soft-tissue ring** around the structural root is now continuity tissue rather than absolute hard protection.

This ring may move only to blend the buttock surface smoothly into the frozen tail core.

Maximum displacement from GO-05AO_AC2:

**3.0 mm**

Target is less whenever possible.

The ring must use a smooth mask ramp:
- 1.0 at the immutable tail core;
- progressively lower toward the glute soft-tissue field;
- no jagged binary outline.

### 4C. Core validation

Before authoring, prove numerically that the immutable core preserves:

- root centroid: 0.000 mm;
- emergence height: 0.000 mm;
- root axis / angle: unchanged within measurement precision;
- cross-sectional width/depth: unchanged within measurement precision;
- free tail: 0.000 mm.

The continuity ring is **not** allowed to redefine the tail root.

## 5. Duplicate-position seam rule

Retain the AQ lesson:

Blender Smooth treats split duplicate-position seam vertices as open boundaries.

Therefore:
- keep at least a **30 mm feather/ramp** around duplicate-position seam vertices;
- no hard 1.0 → low-mask jump at any duplicate seam;
- predictor must explicitly check edge collapse at these sites.

## 6. Wider posterior/lateral feather

The AQ1r lateral transition is too narrow.

Rebuild the broader posterior mask so that:

- lateral hip feather width is at least **50 mm**;
- posterior-thigh feather width is at least **50 mm**;
- the transition ends on low-curvature side/front thigh tissue rather than the lateral glute edge;
- no hard edge lies on the buttock belly, glute fold, lateral hip, or upper hamstring.

The broader field may include:
- glute soft tissue;
- lateral hip soft tissue outside pelvis core;
- posterior upper thigh down toward mid-thigh;
- a small amount of side-thigh continuity tissue where needed.

Still hard-protect:
- pelvis/sacral skeletal core;
- genital;
- perineal protected fold;
- lower thigh/knee;
- torso outside posterior continuity field;
- arms;
- lower legs;
- hands/feet.

## 7. Optional local continuity touch

If the wide feather plus filter sequence leaves **one isolated residual crease** after an otherwise passing result, authorize one tiny UI-only continuity touch:

Allowed:
- light Smooth / Surface Smooth brush;
- narrow line only;
- no broad resculpting.

Requirements:
- predictor / gate afterward;
- no shelf;
- no visible stroke mark;
- no protected-core movement.

This does not authorize repeated manual cleanup passes.

## 8. Predictor before authoring

Before any real filter:

Simulate the exact proposed:
1. negative Inflate / deflate;
2. Smooth cleanup.

Check:
- flips;
- >60° cumulative normal rotations;
- new local inversions;
- self-intersections;
- degenerate/near-collapse edges;
- non-manifold risk;
- tail-core displacement;
- continuity-ring displacement;
- duplicate-seam collapse.

Required before authoring:
- predicted 0 flips;
- 0 new SI;
- 0 degenerates/collapse;
- immutable tail core 0.000 mm;
- continuity ring <= 3.0 mm;
- pelvis/skeletal hip gates pass.

### Repair authority
Maximum:
- 40 local repair neighborhoods;
- 3 analysis/repair cycles;
- <= 0.5 mm local vertex movement;
- <= 0.5 mm patch deviation;
- 0.000 mm outside repair unions.

Mask refinement is preferred over geometry repair where possible.

## 9. Real authoring sequence

Maximum **one primary attempt plus one bounded rerun**.

### AR1
From GO-05AO_AC2 with the new mask:

1. UI Inflate-negative using the previously calibrated ~8 mm belly-centre direction.
2. UI Smooth cleanup calibrated to the predictor.
3. Save and gate.

If clean technically and visually:
PASS.

### AR1r
Only if AR1 fails due to a small local boundary/fold issue:

- revert to GO-05AO_AC2;
- refine mask / bounded local prep only;
- rerun the same deflate strength at equal or lower effective strength.

Do not increase deflate magnitude during the rerun.

If AR1r fails:
STOP.

## 10. Shape-preservation gates

Against GO-05AO_AC2:

### Immutable tail core
- all metrics: 0.000 mm / unchanged.

### Tail continuity ring
- max movement <= **3.0 mm**.

### Pelvis
- core width change <= **0.5%**.

### Skeletal hip
- drift <= **0.5 mm**.

### Upper posterior thigh
- mean-radius loss <= **3.0%**.

### Buttock depth
Report left/right mean posterior-depth reduction.

No fixed minimum; visual gate governs.

### Other finished anatomy
- arms: 0.000 mm;
- torso outside AC3 field: 0.000 mm;
- lower legs: 0.000 mm;
- genital/perineal core: 0.000 mm;
- hands/feet: 0.000 mm.

## 11. Technical gate

Required:

- 0 opened seams;
- 0 self-intersections;
- 0 flipped faces;
- 0 degenerates;
- 1 position-welded component;
- 0 boundary / 0 non-manifold;
- immutable tail core 0.000 mm;
- continuity ring <= 3.0 mm;
- no duplicate-seam collapse;
- stature / bbox unchanged;
- pelvis width within limit;
- skeletal hip within limit;
- posterior thigh radius within limit;
- no visible hard mask shelf;
- no vertical lateral crease;
- no dent/melted patch.

## 12. Visual gate

Compare:
- GO-05AO_AC2;
- rejected AQ1r;
- new AR result.

Required:
- retain AQ1r's improved posterior volume;
- eliminate the jagged tail-root plateau;
- eliminate the vertical lateral hip/thigh crease;
- tail root still reads unchanged in identity;
- buttocks substantial and natural;
- no bodybuilder projection;
- no flat/deflated read;
- lower glute fold soft and continuous;
- no patch outline;
- posterior thigh robust.

This is a **continuity correction**, not another volume-reduction pass.

## 13. Final AC3 output

If passing, freeze:

`GO-05AR_AC3.blend`
`GO-05AR_AC3.glb`

Record exact hashes.

## 14. Decision

### PASS

Return:

**05AR AC3 PASS / READY FOR FINAL Q1-Q2 + TYLER VISUAL REVIEW**

Then STOP.

Do not alter:
- head share;
- heel lift;
- final foot size;
- genus handles;
- any deferred tail redesign beyond the continuity ring authorized here.

### FAIL

Return:

**05AR AC3 CONTINUITY CORRECTION NOT CREDIBLE / STOP**

Revert active composition state to GO-05AO_AC2.

## 15. Evidence

Return:
- immutable tail-core vertex definition;
- tail continuity-ring definition;
- mask visual/readback;
- duplicate-seam ramp verification;
- predictor/repair logs;
- exact UI deflate and Smooth settings;
- core/ring displacement metrics;
- tail emergence/axis/cross-section metrics;
- pelvis width;
- skeletal hip drift;
- thigh radius;
- buttock-depth change;
- complete geometry gates;
- identical-camera:
  - whole F/P/B/3/4;
  - body-only F/P/B/3/4;
  - posterior close B/P/3/4;
  - AO2 vs AQ1r vs AR comparison;
  - tail-root close comparison.

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

`reviews/claude-rac-rm-ot-05ar-gorrund-ac3-continuity-gate.md`

Evidence:

`reviews/rac-rmot05ar-evidence/`
