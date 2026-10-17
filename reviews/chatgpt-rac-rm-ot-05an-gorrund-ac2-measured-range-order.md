# RAC RM-OT-05AN — AC2 measured-range finish with feathered masks and cumulative predictive gate

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05AM.
**Date:** 2026-10-16.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05am-gorrund-ac2-controlled-filter-buildup-gate.md` (d961fa3).

## 1. Author ruling

05AM established that the old AC2 displacement limits were not physically sufficient to reach the required visual target on this dense source mesh.

The diagnostic evidence shows:
- within the old limits, the limbs remain visually near AC1;
- a clearly softened AC2 read appears around:
  - cumulative limb median ≈ **7 mm**;
  - cumulative limb p95 ≈ **18 mm**;
  - cumulative limb max ≈ **28 mm**;
- the same simulation also showed hard steps at the shoulder-top and thigh/hip mask-box edges.

Therefore authorize a measured-range AC2 finish with:
1. feathered shoulder/hip transitions;
2. cumulative-reference flip prediction before every real authoring step;
3. larger displacement limits matching the demonstrated need;
4. explicit radius/joint preservation so larger smoothing cannot turn into limb slimming.

This does **not** authorize general remeshing, automatic body replacement, or uncontrolled over-smoothing.

## 2. Active source

The active technically passed AC2 checkpoint remains:

`GO-05AL_AK1.blend`
SHA-256:
`a23364426da9866f315d132fe995b19a2ca274c6b45e8d9cf84b25f166eb37cc`

Review GLB:
`GO-05AL_AK1.glb`
SHA-256:
`23d5dec3c5d4a291b4e26b5aca2550ddf7a35dffc94b0806547b195d78879955`

The frozen 05AL predictive-safe baseline remains historical reference:

`GO-05AL_predictive_limb_safe_baseline.blend`
SHA-256:
`dcffb0dc5509f03faf6865b8818a88398225157a872702cfe3c8208d57907881`

Do not use rejected `GO-05AM_AM1.blend` as an advancement source.

## 3. 05AM predictive-repair candidate

05AM produced:

`GO-05AM_AK1_predictive_repair.blend`
SHA-256:
`cc3adee1a9d37c9faf55a742f47346a3702365ab389ed63a33b74a8dec522a24`

This is not automatically promoted.

Before use, independently rerun the full preservation gate and confirm:
- source is exactly GO-05AL_AK1;
- 0 seams;
- 0 self-intersections;
- 0 degenerate faces;
- 0 locally inverted repair faces;
- 1 / 0 / 0 topology;
- protected regions and 05AI torso/glute/pelvis_other = 0.000 mm;
- max repair move <= 0.5 mm;
- movement outside repair union = 0.000 mm;
- patch deviation <= 0.5 mm;
- stature / bbox unchanged.

The report disclosed:
- two stable >60° margin faces (224765, 549805);
- one pre-existing micro-crimp face 262682 that smoothing improves.

These may remain only if they are still predicted stable under the proposed next real step.

If the candidate fails independent revalidation, rebuild the same repair from GO-05AL_AK1 rather than patching the candidate blindly.

Freeze the validated repair as:

`GO-05AN_start.blend`
`GO-05AN_start.glb`

## 4. Replace hard shoulder/hip mask edges with feathered transitions

The 05AM simulation showed mask-boundary steps at:
- shoulder-top / upper-arm transition;
- upper-thigh / hip transition.

Build a new limb mask in Blender UI on GO-05AN_start.

### Preserve hard masks for:
- head / upper neck;
- central passed 05AI torso core;
- pelvis / genital / perineal;
- gluteal/posterior region reserved for AC3;
- tail / tail junction;
- hands beyond wrist buffers;
- feet beyond ankle buffers.

### Feather transitions for:
- shoulder-top into upper arm;
- lateral upper thigh into hip/pelvis protection;
- wrist/ankle transition bands;
- knee/elbow preservation bands.

The feathering must be broad enough that the simulation no longer shows a visible hard step, while the protected torso/pelvis core remains exactly masked at 1.0.

### Mask-order rule
1. create sculptable limb zones;
2. create joint-preservation zones;
3. feather the allowed transition zones;
4. only then apply final hard protection to torso core / pelvis core / head / hands / feet / tail / genital / perineal;
5. no global Smooth Mask after final hard protection.

Read back the mask before authoring.

Required:
- all protected core sets min mask 1.0;
- joint centres more protected than bellies;
- feathered shoulder/hip transition verified numerically and visually;
- geometry unchanged before authoring.

## 5. Predictor upgrade remains mandatory

Use the corrected cumulative-reference predictor from 05AM:
- compare proposed faces against the frozen 05AL baseline reference normals;
- flag:
  - flips;
  - >60° cumulative normal rotation;
  - adjacent >60° folds;
- treat rotated/retriangulated faces using the repaired checkpoint's own local reference when no direct baseline triangle correspondence exists.

Before **every** real filter build-up step:
1. simulate the exact proposed filter behavior using the saved current mask;
2. collect instability;
3. repair only discrete predicted neighborhoods with the proven bounded method;
4. rerun until 0 predicted flips and no unresolved progressive inversion.

## 6. Predictive repair authority

Maximum additional prep across 05AN:
- **80 discrete repair neighborhoods total**;
- 3 repair-analysis cycles per proposed filter stage.

Local repair method:
- <= 0.5 mm vertex movement from the current saved checkpoint;
- near-coplanar edge rotations;
- <= 0.5 mm patch surface deviation;
- 0.000 mm movement outside authorized neighborhoods;
- no protected-region movement;
- no visible silhouette change.

If >80 neighborhoods are required before a real authoring step:
**05AN PREDICTIVE REPAIR BUDGET EXCEEDED / STOP**

Do not broaden to generic retopology.

## 7. Measured displacement envelope

The old limits are superseded.

Final cumulative limb displacement from the frozen 05AL predictive-safe baseline may reach:

- median <= **8.0 mm**
- p95 <= **20.0 mm**
- max <= **32.0 mm**

These are hard safety ceilings, not targets.

Claude should stop as soon as the visual AC2 gate is met.

### Limb-mass preservation
For every segment:
- upper arm L/R;
- forearm L/R;
- thigh L/R;
- shin L/R;

mean-radius change from the frozen 05AL predictive-safe baseline must remain:

**>= -3.0%**

and no segment may gain > +2.0% mean radius unless needed only as a local volume-preserving correction.

Joint-centre drift:
- <= 0.5 mm hard ceiling;
- target << 0.5 mm.

If the filter achieves softer relief only by shrinking the entire limb envelope beyond these limits, reject the step.

## 8. Preferred authoring route

Favor a **volume-preserving smoothing buildup**, not raw Smooth alone.

Preferred sequence:

### AN1 — repeated Surface Smooth buildup
Use multiple UI Surface Smooth applications/events with:
- Strength 1.000;
- Shape Preservation 0.500 or higher if needed to preserve envelope;
- Per Vertex Displacement 0.500;
- XYZ / Local.

Use simulation to select a number of events that produces meaningful visual change while staying well below final ceilings.

Do not jump straight to the ~420-event diagnostic state.

Choose a first meaningful increment, then gate/render.

### AN2 — additional Surface Smooth or restrained Smooth
If AN1 is safe but the heroic relief remains:
- use another predicted Surface Smooth buildup; or
- use a restrained Smooth Mesh Filter only if diagnostics show it is more effective without violating mean-radius preservation.

### AN3 — optional volume correction
If the visual target is close but a segment has thinned toward the -3% radius limit:
- a restrained **Inflate** or equivalent UI volume-correction filter may be applied only inside that segment's feathered muscle-belly mask;
- predictor and geometry gate required;
- no joint enlargement;
- no silhouette overshoot;
- final segment radius must return inside the allowed band.

Do not use Inflate merely to restore bodybuilding bulk.

## 9. UI-only authoring requirement

All final authoring filters must be invoked through Blender UI.

Allowed:
- Mesh Filter Surface Smooth;
- Mesh Filter Smooth;
- restrained Inflate for volume correction;
- UI mask editing.

Diagnostic scripts may simulate filters and calculate safe event counts.

Forbidden:
- scripted final vertex shaping;
- scripted execution of the authoring filter;
- Dyntopo;
- voxel remesh;
- shrinkwrap;
- proportional whole-limb scaling;
- automated body replacement.

## 10. Checkpoint cadence

Maximum **3 authored buildup checkpoints** in 05AN.

After every checkpoint:
- save distinct .blend;
- export review GLB;
- run complete gates;
- calculate cumulative displacement;
- calculate segment mean-radius changes;
- calculate joint drift;
- render identical cameras.

If a checkpoint fails:
- revert to last passed checkpoint;
- one predictive-repair-and-rerun of that exact stage is allowed.
If it fails again, STOP.

## 11. Technical gate

Required after each authored checkpoint:

- 0 opened seams;
- 0 self-intersections;
- 0 flipped faces;
- 0 degenerates;
- 1 position-welded component;
- 0 boundary / 0 non-manifold;
- head = 0.000 mm;
- passed torso core = 0.000 mm;
- pelvis / glute / genital / perineal core = 0.000 mm;
- tail / tail junction = 0.000 mm;
- protected hands / feet = 0.000 mm;
- stature / bbox unchanged;
- joint-centre drift <= 0.5 mm;
- segment mean-radius >= -3.0%;
- cumulative displacement within §7;
- no hard mask steps;
- no shelves / ridges / dents / melted patches.

Feather transition vertices may move as intended; map and disclose them.

## 12. Visual AC2 gate

Compare to:
- passed 05AI AC1;
- 05AL AK1;
- 05AM feasibility simulations.

Required:
- biceps/triceps separation clearly no longer heroic;
- forearms substantially less corded;
- quad channels largely neutralized;
- teardrop above knee substantially reduced;
- calf bellies visibly softer;
- no hard shoulder/hip mask steps;
- limbs remain robust and load-bearing;
- large joints remain obvious;
- no mannequin / melted look;
- left/right coherent;
- whole body now reads as large-frame, ordinary-untrained rather than bodybuilder.

Do not accept purely because the displacement target was reached.

## 13. Final AC2 output

Freeze best passing checkpoint as:

`GO-05AN_AC2.blend`
`GO-05AN_AC2.glb`

Record exact hashes and filter sequence.

## 14. Decision

### PASS
Return:

**05AN AC2 PASS / READY FOR AC3 DECISION**

Then STOP.

Do not begin AC3.

### FAIL
If the 3-checkpoint authoring budget is exhausted, or the visual target requires exceeding:
- p95 20 mm;
- max 32 mm;
- mean-radius loss >3%;
- or joint drift >0.5 mm;

return:

**05AN AC2 MEASURED-RANGE BUILDUP NOT CREDIBLE / STOP**

Revert to the last technically passed checkpoint and STOP.

## 15. Evidence

Return:
- revalidation of GO-05AM_AK1_predictive_repair;
- mask readback and feather-transition visualization;
- predictor result before every authored step;
- repair neighborhoods and changes;
- exact UI filter settings / event counts;
- cumulative displacement;
- mean-radius change per limb segment;
- joint drift;
- geometry gate;
- identical-camera whole/body/arms/thighs/calves comparisons;
- final AC2 body-only comparison against 05AI AC1.

## 16. State

Until later Q1/Q2 and Tyler visual acceptance:
- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED;
- no LOW / blind final acceptance / scaffold;
- no D4 / UE5 / production rigging / creator implementation.

## 17. Return

Commit:

`reviews/claude-rac-rm-ot-05an-gorrund-ac2-measured-range-gate.md`

Evidence:

`reviews/rac-rmot05an-evidence/`
