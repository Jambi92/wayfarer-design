# RAC RM-OT-05AG — resume full manual composition sculpt from the 05AF sculpt-safe baseline

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05AF PASS.
**Date:** October 16, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05af-full-sculpt-safe-retopology-prep-gate.md` (ebf9c52).

## 1. Advancement baseline

05AF is now the sole sculpt-working baseline for composition work.

### Frozen 05AF baseline
`GO-05AF_full_sculpt_safe_baseline.blend`
SHA-256:
`6ef02c298db3cd89d93d8aafc6f2a3580f568945c869cbf7af445b51ff93edb8`

### Review GLB
`GO-05AF_full_sculpt_safe_baseline.glb`
SHA-256:
`d72d93b22a3bb7a6089c119642c2976f449236197257e1067223e0b9c9b85a38`

All rejected 05AC/05AD/05AE sculpt attempts remain evidence only.

## 2. 05AF sculpt-safety contract

05AF has:
- 0 SAFE duplicate groups remaining inside AC1–AC3 sculpt zones;
- 0 coincident pairs touching any sculpt-zone vertex;
- 0 self-intersections;
- 0 flips;
- 0 degenerates;
- 1 position-welded component;
- 0 boundary / 0 non-manifold;
- 0.000 mm surface displacement from seam consolidation.

Do not re-open or alter the seam preparation.

## 3. Protected interfaces

Hard-protect throughout all checkpoints:

- head / muzzle / ears above approximately 172 cm;
- hands beyond the 5 cm wrist buffers;
- feet beyond the 5 cm ankle buffers;
- genital landmark box;
- free tail + fused root;
- tail junction;
- perineal midline fold at 05AF indices:
  `144700, 144701, 144702, 144703`.

The one perineal fold is intentionally unwelded and must remain masked during AC3.

Do not change:
- neck length;
- head size/share;
- finger/toe anatomy;
- tail-root fusion;
- heel lift;
- final foot-size decision;
- genus handles.

Those remain later review items.

## 4. Sculpt goal

Convert the heroic/bodybuilder soft tissue into:

**large Gorrund structural frame + ordinary untrained soft tissue**

Preserve:
- broad/deep thorax;
- robust pelvis;
- large joints;
- Gorrund macro proportions;
- large hands/feet;
- accepted reach/leg-share relationships.

Remove or soften:
- hypertrophic pecs;
- deltoid caps;
- hard traps/bodybuilder shoulder silhouette;
- segmented abs / serratus;
- biceps/triceps/forearm definition;
- quad teardrops / separation;
- calf bellies;
- large round projected glutes;
- bodybuilder posterior-thigh transition;
- love-handle / strongman bulk.

Do not compensate by making him:
- chubby;
- obese;
- weak-looking;
- narrow-framed;
- smooth/mannequin-like.

## 5. Method

Real Blender UI sculpt only.

Allowed:
- Smooth / Surface Smooth / Relax;
- restrained Flatten / Scrape;
- restrained Grab / Elastic Deform for soft-tissue volume;
- masks / face sets;
- tiny Edit Mode continuity corrections if a local surface defect appears.

Forbidden:
- Python console;
- scripting workspace;
- shell;
- scripted strokes;
- scripted vertex shaping;
- Dyntopo;
- voxel remesh;
- topology replacement;
- shrinkwrap;
- solver-generated anatomy;
- procedural body replacement;
- broad non-anatomical scaling.

Scripts remain allowed only for:
- checks;
- measurements;
- renders;
- masks/region maps prepared outside the desktop sculpt;
- validation.

## 6. Checkpoint AC1 — torso / shoulders

Start from the frozen 05AF baseline.

Focus:
- flatten pectoral projection;
- remove the central pec split and hard lower-pec shelf;
- further reduce deltoid cap;
- soften trap/shoulder bodybuilder read;
- remove abdominal block segmentation;
- soften serratus grooves;
- reduce love-handle / flank bulk;
- preserve thoracic breadth/depth and trunk integration.

Do not alter limbs below the shoulder transition except tiny continuity touches.

### AC1 technical gate

Require:
- 0 opened seams;
- 0 self-intersections;
- 0 flips;
- 0 degenerates;
- 1 component / 0 boundary / 0 non-manifold;
- stature/bbox unchanged;
- macro targets unchanged within prior tolerance;
- protected interfaces unmoved;
- no new dents/ridges/shelves;
- visible torso improvement over 05AF and the rejected AC1 attempts.

If AC1 fails, revert to 05AF and STOP:
**05AG AC1 NOT CREDIBLE / STOP**

If AC1 passes, continue automatically to AC2.

## 7. Checkpoint AC2 — arms / legs

From the passed AC1:

Focus:
- reduce biceps/triceps separation;
- neutralize forearm cord/vein-like definition;
- soften quad separation and teardrop;
- reduce calf belly definition;
- neutralize elongated heroic thigh forms;
- preserve large knees/ankles/elbows/wrists and Gorrund load-bearing mass.

Hands/feet beyond the buffers stay protected.

### AC2 gate

Same zero-defect geometry requirements as AC1.

Also require:
- limb soft tissue clearly less heroic;
- no skinny/human-average collapse;
- joint scale preserved;
- no hand/foot deformation.

If AC2 fails, revert to the passed AC1 checkpoint and STOP:
**05AG AC2 NOT CREDIBLE / STOP**

If AC2 passes, continue automatically to AC3 if posterior/gluteal heroism remains materially visible.

## 8. Checkpoint AC3 — posterior / gluteal

Only if needed.

Focus:
- reduce round projected gluteal mass to ordinary untrained volume;
- soften posterior-thigh bodybuilding transition;
- preserve robust pelvis;
- preserve real gluteal crease landmarks;
- reduce the minor gluteal-fold-end crease if safely possible;
- visually soften the thigh-top stretch band without shifting hip/joint structure.

Hard-protect:
- tail root / fused tail interface;
- tail junction;
- genital landmark;
- perineal fold indices 144700–144703.

### AC3 gate

Same zero-defect geometry requirements.

If AC3 fails, revert to passed AC2 and STOP:
**05AG AC3 NOT CREDIBLE / STOP**

## 9. Decisive Q1 / Q2 gate

After the best passed checkpoint, rerun the whole-source review.

### Q1 required YES
Does the body express Gorrund structural identity at reference composition?

### Q2 required YES
With head and tail hidden, does the body avoid reading as:
- enlarged human;
- bodybuilder;
- strongman;
- ogre/brute;
- Grask;

while retaining a large, structurally distinct Gorrund frame?

Compare directly against:
- 05AF baseline;
- donor A/B/C body-only exhibits;
- accepted W1 ARM;
- Marchfolk / Skarn / Grask controls.

Required visual outcome:
- clearly less heroic than 05AF;
- ordinary untrained soft tissue;
- no obesity compensation;
- no melted/mannequin anatomy;
- broad/deep frame and joint scale retained.

## 10. Author review stop

If Q1 = YES and Q2 = YES:

Return:

**05AG COMPOSITION SCULPT PASS / AUTHOR VISUAL REVIEW REQUIRED**

Then STOP for Tyler's visual review.

Do not touch:
- head share;
- tail root;
- heel lift;
- final foot size;
- genus handles

until Tyler accepts the composition.

## 11. Failure stop

If all safe checkpointing is exhausted without Q1/Q2:

**05AG MANUAL COMPOSITION LIMIT REACHED / HUMAN SCULPTOR REQUIRED**

Then STOP. No generator reset.

## 12. Evidence

For every passed checkpoint:
- distinct .blend;
- review GLB;
- hashes;
- identical-camera whole F/P/B/3/4;
- body-only F/P/B/3/4;
- targeted torso/limb/posterior views;
- geometry-gate JSON;
- protected-region displacement report;
- macro-target report.

Final report:

`reviews/claude-rac-rm-ot-05ag-gorrund-composition-sculpt-gate.md`

Evidence:

`reviews/rac-rmot05ag-evidence/`

## 13. State

Until Tyler visually accepts a 05AG PASS:
- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED;
- no LOW / blind final acceptance / scaffold;
- no D4 / UE5 / production rigging / creator implementation.
