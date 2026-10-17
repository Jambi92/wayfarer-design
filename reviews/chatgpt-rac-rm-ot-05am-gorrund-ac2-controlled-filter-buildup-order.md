# RAC RM-OT-05AM — controlled AC2 filter buildup from the stable 05AL AK1 checkpoint

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05AL PASS.
**Date:** 2026-10-16.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05al-predictive-limb-quality-prep-gate.md` (fdd42e6).

## 1. Advancement baseline

Advance from the technically passed AC2 stability checkpoint:

`GO-05AL_AK1.blend`
SHA-256:
`a23364426da9866f315d132fe995b19a2ca274c6b45e8d9cf84b25f166eb37cc`

Review GLB:
`GO-05AL_AK1.glb`
SHA-256:
`23d5dec3c5d4a291b4e26b5aca2550ddf7a35dffc94b0806547b195d78879955`

Frozen predictive-safe source:

`GO-05AL_predictive_limb_safe_baseline.blend`
SHA-256:
`dcffb0dc5509f03faf6865b8818a88398225157a872702cfe3c8208d57907881`

The passed 05AI AC1 torso is preserved inside these files.

Do not advance from any rejected 05AJ/05AK state.

## 2. Goal

Finish AC2 visually while preserving the now-stable limb mesh.

Required final read:

**large-jointed, large-framed Gorrund limbs with ordinary untrained soft tissue**

Reduce materially:
- biceps / triceps separation;
- forearm cord relief;
- quad channels;
- teardrop above the knee;
- calf-belly / gastrocnemius projection.

Preserve:
- elbow / wrist / knee / ankle scale;
- hand / foot scale;
- limb lengths and stance;
- overall load-bearing limb mass;
- passed 05AI torso.

## 3. Predict-before-author rule

Before **every additional real filter application**, run a diagnostic prediction on the exact current saved checkpoint using the exact current saved `.sculpt_mask`.

The predictive pass must estimate the proposed next filter application and identify:
- flipped faces;
- adjacent >60° fold faces;
- any new micro-crimp likely to invert.

If prediction is nonzero:
1. repair only those discrete two-ring neighborhoods with the proven 05AL method;
2. max vertex move <= 0.5 mm from that checkpoint;
3. near-coplanar edge rotations only;
4. 0.000 mm outside the neighborhood union;
5. patch deviation <= 0.5 mm;
6. rerun prediction until 0 flips or stop limits are reached.

Maximum across 05AM:
- 40 additional discrete repair neighborhoods;
- 3 repair-analysis cycles per filter step.

If a proposed step cannot be driven to 0 predicted flips within that budget, do not author the filter.

## 4. Existing watch-list

The 05AL real AK1 left 5 faces whose normals rotated >60° without inverting:

- 262682
- 431821
- 549806
- 962795
- 406794

Treat these as mandatory watch-list faces in the first 05AM prediction. Do not preemptively move them unless the predictor flags them or their immediate fold neighborhood.

## 5. Masks

Reuse the 05AL joint-banded limb mask strategy.

Hard-protect:
- head / neck;
- passed 05AI torso;
- pelvis / genital / perineal;
- glutes / posterior pelvis;
- tail / tail junction;
- hands beyond wrist buffers;
- feet beyond ankle buffers.

Joint centres remain much more protected than muscle bellies.

Any mask feathering must happen before final hard masks.

No global Smooth Mask after final hard protection.

Read back the mask before each authored filter if the mask file changes.

## 6. Filter buildup sequence

The sequence is adaptive. Stop as soon as the visual AC2 gate is met.

### AM1 — second Surface Smooth

Proposed filter:
- Mesh Filter: **Surface Smooth**
- same settings as 05AL AK1:
  - Strength 1.000
  - Shape Preservation 0.500
  - Per Vertex Displacement 0.500
  - XYZ
  - Local
- one comparable UI application.

Before authoring:
- run predictor on the current 05AL AK1;
- repair only predicted instability;
- require 0 predicted flips.

After authoring:
- save checkpoint;
- run the full technical gate;
- render identical-camera comparisons.

If AC2 visual target is met, STOP and PASS.

If technically clean but still clearly too heroic, continue to AM2.

### AM2 — restrained Smooth Mesh Filter calibration

Surface Smooth is primarily reducing relief and may converge before enough muscle-belly bulk is removed.

Authorize one **restrained Smooth Mesh Filter** application to muscle-belly zones only.

Requirements:
- same joint-preservation and protected masks;
- use a conservative UI drag/strength calibrated so the proposed incremental displacement remains approximately:
  - limb median <= 0.6 mm;
  - p95 <= 1.8 mm;
  - max <= 4.0 mm.
- do not exceed these limits merely to chase the visual target.

Before authoring:
1. build/calibrate a diagnostic predictor for this exact Smooth Mesh Filter behavior against a scratch copy or sufficiently conservative reference;
2. predict on the current checkpoint;
3. repair any predicted instability under §3;
4. require 0 predicted flips.

After authoring:
- run the complete gate and visual review.

If visual target is met, STOP and PASS.

If technically clean but still materially too heroic, continue to AM3.

### AM3 — one final controlled buildup

Choose **one**:
- another Surface Smooth application, or
- another restrained Smooth application,

based on which one the previous evidence shows will reduce the remaining heroic form without damaging envelope/joints.

Before authoring:
- predictive gate and bounded repair are mandatory.

Cumulative displacement from the frozen 05AL predictive-safe baseline must remain:
- p95 limb displacement <= **6.0 mm**;
- max <= **10.0 mm**.

Do not authorize any fourth filter application.

## 7. Local continuity cleanup

After a passing filter checkpoint, maximum **two tiny UI-only continuity touches** are allowed only to remove an isolated mask-boundary ridge.

Allowed:
- light Smooth / Surface Smooth brush;
- tiny local Flatten.

Forbidden:
- broad manual limb resculpting;
- zigzag passes;
- repeated mouse-drag smoothing;
- any correction that creates stroke shelves.

Any cleanup must be validated afterward.

## 8. Technical gate after every authored checkpoint

Required:

- 0 opened seams;
- 0 self-intersections;
- 0 flipped faces;
- 0 degenerate faces;
- 1 position-welded component;
- 0 boundary / 0 non-manifold;
- head = 0.000 mm;
- passed torso = 0.000 mm except previously disclosed transition band;
- pelvis / glute / genital / perineal = 0.000 mm;
- tail / tail junction = 0.000 mm;
- protected hands / feet = 0.000 mm;
- stature / bbox unchanged;
- joint-centre drift <= 0.2 mm;
- macro crotch / fingertip / knee / ankle relationships preserved;
- no new shelves / ridges / dents / melted patches.

If a technically failed authored checkpoint occurs:
- revert to the last passed checkpoint;
- use the predictor to diagnose;
- only one bounded repair-and-rerun of that exact step is allowed.
If it fails again, STOP.

## 9. Visual AC2 gate

Compare against passed 05AI AC1 and the current prior checkpoint.

Required:
- biceps/triceps separation materially softer;
- forearms materially less corded;
- quad channels materially softer;
- teardrop above knee materially reduced;
- calf bellies materially less heroic;
- no stroke shelves/lumps;
- joints remain visually large;
- limbs remain robust, not skinny;
- left/right result coherent;
- whole body now reads closer to large-frame/untrained rather than heroic/bodybuilder.

Do not accept a merely technical pass if the limb anatomy still looks essentially unchanged.

## 10. Final AC2 output

Freeze the best passing checkpoint as:

`GO-05AM_AC2.blend`
`GO-05AM_AC2.glb`

Record exact hashes and which filter sequence produced it.

## 11. Decision

### PASS

Return:

**05AM AC2 PASS / READY FOR AC3 DECISION**

Then STOP.

Do not begin AC3 in this order.

### FAIL

If the three-filter budget is exhausted without reaching the visual target, or a step cannot be stabilized under the predictive repair limits:

**05AM AC2 CONTROLLED BUILDUP NOT CREDIBLE / STOP**

Revert active AC2 status to the last technically passed checkpoint and STOP.

## 12. Evidence

For every step:
- predictor result before authoring;
- repair neighborhoods and changes, if any;
- filter UI settings;
- displacement metrics;
- geometry gate;
- mask/protected-region report;
- identical-camera whole/body/arm/thigh/calf comparisons.

Final report:

`reviews/claude-rac-rm-ot-05am-gorrund-ac2-controlled-filter-buildup-gate.md`

Evidence:

`reviews/rac-rmot05am-evidence/`

## 13. State

Until later Q1/Q2 and Tyler visual acceptance:
- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED;
- no LOW / blind final acceptance / scaffold;
- no D4 / UE5 / production rigging / creator implementation.
