# RAC RM-OT-05AJ — AC2 arms and legs from the passed 05AI AC1 checkpoint

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05AI PASS.
**Date:** October 16, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05ai-local-flip-fix-and-ac1-gate.md` (f5cedd3).

## 1. Advancement baseline

Advance only from the passed AC1 checkpoint:

`GO-05AI_AC1.blend`
SHA-256:
`89a19ba2721e80662dc5f09dfa3c0782e975b2e69291bea3439f619391810dae`

Review GLB:
`GO-05AI_AC1.glb`
SHA-256:
`68d876df38b39bc3f1d1f87cdc1a991d678cdb1da08114f9e1165f9b133f5e36`

The local-quality prep baseline remains frozen:

`GO-05AI_local_quality_baseline.blend`
SHA-256:
`eb50d6e48027ce53e2d71d12eacee7ba27c2b96952741e6f1db3cdbf126df5df`

All rejected 05AC/AD/AE/AG/AH sculpt attempts remain evidence only.

## 2. AC1 preservation contract

The passed AC1 torso is now protected history.

Do not intentionally alter:
- chest / pec result;
- abs / serratus result;
- torso / flank result;
- deltoid changes already accepted in AC1;
- head / upper neck;
- tail / tail junction;
- genital / perineal protected interfaces;
- hands beyond wrist buffers;
- feet beyond ankle buffers;
- glutes / posterior pelvis (reserved for AC3).

No rollback toward the heroic torso is allowed.

## 3. AC2 goal

Neutralize the heroic muscle treatment in the **arms and legs** while preserving the corrected Gorrund macro skeleton and large-joint identity.

Target read:

**large-framed, load-bearing Gorrund limbs with ordinary untrained soft tissue**

Not:
- bodybuilder;
- powerlifter;
- superhero;
- stringy / weak;
- human-average skeletal scale.

### Arms
Reduce:
- biceps peak;
- triceps separation;
- forearm cord / vein-like anatomy;
- hard muscle-groove transitions.

Preserve:
- elbow size;
- wrist scale;
- hand scale;
- broad skeletal frame;
- believable limb mass.

### Legs
Reduce:
- quadriceps separation;
- teardrop / vastus-medialis emphasis;
- vertical heroic thigh grooves;
- calf-belly bulge;
- sharp gastrocnemius separation.

Preserve:
- knee size;
- ankle size;
- foot scale;
- thigh/calf load-bearing mass;
- corrected limb lengths and stance.

Do not make the limbs thin merely to remove definition.

## 4. Hard protection / masks

Use the proven protection strategy.

Before sculpting:
1. Any mask feathering/smoothing must happen **before** final hard protection masks are applied.
2. Final hard-protect:
   - head / upper neck;
   - complete AC1 torso except the smallest shoulder-to-upper-arm continuity band needed for transition;
   - hands beyond the 05AF wrist buffer;
   - feet beyond the 05AF ankle buffer;
   - genital region;
   - perineal fold;
   - tail / tail junction;
   - gluteal / posterior pelvis reserved for AC3.
3. No global Smooth Mask after those hard masks exist.

The wrist and ankle buffer zones may be sculpted lightly only to create a smooth transition into the protected hands/feet.

## 5. Mesh-quality preflight

The 05AI local quality fix proved that small source-mesh crimps/slivers can invert under otherwise valid UI sculpting.

Before desktop AC2 strokes, run a **diagnostic-only** quality scan of the intended arm/leg sculpt zones.

Report:
- faces with quality < 0.15;
- any face folded > 60 degrees against all immediate neighbours;
- any clearly repeated micro-crimp analogous to the three 05AI crimp faces.

### Automatic repair authority

Do **not** broadly optimize the limbs.

If and only if the diagnostic finds a discrete pre-existing micro-crimp that is likely to invert under ordinary smoothing, Claude may apply the already-proven 05AI local repair method to that specific neighborhood:
- maximum two-ring neighborhood;
- local relax capped at **0.5 mm**;
- near-coplanar edge rotations only;
- no movement outside the neighborhood;
- local surface deviation <= **0.5 mm**;
- no silhouette change in review views.

Maximum:
- **8 discrete repair neighborhoods total** across both arms and both legs.

If more than 8 such neighborhoods require repair, STOP before sculpting and report:
**05AJ AC2 PREFLIGHT EXCEEDS LOCAL-REPAIR BUDGET / AUTHOR RULING REQUIRED**

Do not perform a blanket sliver-remesh or generalized optimization.

If no discrete crimp requires repair, proceed directly to AC2.

Any preflight repair must pass:
- 0 SI;
- 0 flips;
- 0 degenerates;
- 1 / 0 / 0 topology;
- protected regions unchanged;
- stature / bbox / macro proportions unchanged.

Freeze any repaired AC2 working baseline and record its hash before sculpting.

## 6. UI sculpt method

Real Blender UI sculpt only.

Allowed:
- Smooth / Surface Smooth / Relax;
- restrained Flatten / Scrape;
- restrained Grab / Elastic Deform for soft-tissue volume;
- masks / face sets.

Forbidden:
- Python console;
- scripting workspace;
- shell;
- scripted brush strokes;
- Dyntopo;
- voxel remesh;
- broad procedural deformation;
- automated limb slimming;
- joint repositioning;
- topology change during the sculpt itself.

Diagnostic / gate scripts are allowed outside the authoring step.

## 7. AC2 checkpoint

Save as:

`GO-05AJ_AC2.blend`

Export:

`GO-05AJ_AC2.glb`

Record exact hashes.

Maximum **one deliberate AC2 production checkpoint** in this order, plus at most two tiny UI-only continuity cleanup cycles if a technical gate identifies an isolated local defect that can be corrected without broad resculpting.

## 8. AC2 technical gate

Required:

- 0 opened seams;
- 0 self-intersections;
- 0 flipped faces;
- 0 degenerate faces;
- 1 position-welded component;
- 0 boundary / 0 non-manifold;
- head: 0.000 mm;
- AC1 torso outside allowed shoulder transition: 0.000 mm intentional displacement;
- tail / tail junction / genital / perineal: 0.000 mm;
- protected hands / feet: 0.000 mm;
- gluteal/posterior reserved region: 0.000 mm intentional displacement;
- stature and bbox unchanged;
- macro crotch / fingertip / knee / ankle relationships preserved within the existing diagnostic tolerance;
- no joint-centre drift;
- no new dents / ridges / shelves / melted regions.

If a few torso vertices move only because they are inside the explicitly allowed shoulder transition band, disclose and map them.

## 9. AC2 visual gate

Compared with passed 05AI AC1:

Required:
- biceps/triceps separation clearly softer;
- forearms less corded;
- quads less separated;
- teardrop above knee materially softened;
- calf bulges less heroic;
- limbs still visibly large-framed and load-bearing;
- elbow/knee/wrist/ankle scale preserved;
- no skinny/human-average collapse.

Produce identical-camera:
- whole F / P / B / 3/4;
- body-only F / P / B / 3/4;
- both arms front/3/4/profile;
- both thighs/knees front/3/4;
- both calves profile/back;
- comparison against 05AI AC1.

## 10. Decision

### PASS

Return:

**05AJ AC2 PASS / READY FOR AC3 DECISION**

Then STOP.

Do not start AC3 in this order.

### FAIL

If AC2 cannot meet technical gates without damaging the passed AC1 or macro structure:

**05AJ AC2 NOT CREDIBLE / STOP**

Revert to the passed 05AI AC1 checkpoint and STOP.

## 11. State

Until later Q1/Q2 and Tyler visual acceptance:
- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED;
- no LOW / blind final acceptance / scaffold;
- no D4 / UE5 / production rigging / creator implementation.

## 12. Return

Commit:

`reviews/claude-rac-rm-ot-05aj-gorrund-ac2-arms-legs-gate.md`

Evidence:

`reviews/rac-rmot05aj-evidence/`
