# RAC RM-OT-05AC — manual composition neutralization from the clean 05AB1 macro baseline

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05AB1 PASS.
**Date:** October 15, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05ab1-gorrund-armpit-weight-cleanup-gate.md` (61fc012).

## 1. Advancement baseline

05AB1 is accepted as the sole advancement baseline for the composition-sculpt phase.

### Frozen applied baseline
`GO-05AB1_macro_corrected_clean.blend`
SHA-256:
`79727daa2552842ddb0ec80505334a4c091ccc026c469e35de7c6c1b7d098a61`

### Review GLB
`GO-05AB1_macro_corrected_clean.glb`
SHA-256:
`03693479be311e72fd608728e6d978ee24169f7fefd679bbc872990061b35e0b`

### Non-destructive rig history
`GO-05AB1_macro_corrected_rig_cp3.blend`
SHA-256:
`a20d11fe6294738096e6fe587ff959f222519e2e5b5e599548d820b9454220b1`

The donor, AA baseline, cp2 and cp3 rig-history files remain immutable evidence.

Do not return to Rodin and do not reopen macro reproportion unless this order explicitly fails on a macro-preservation gate.

## 2. Goal

Manually sculpt the 05AB1 body from **heroic/bodybuilder soft tissue** to **Gorrund reference composition** while preserving the now-correct macro skeleton and the real sculptural quality of the donor.

The target read is:

> **large structural frame + ordinary untrained soft tissue**

The body should look large because of:
- broad/deep load-bearing thorax;
- robust pelvis;
- large joints;
- large hands/feet;
- Gorrund-specific proportions;

not because of:
- pectoral/deltoid hypertrophy;
- separated abs/serratus;
- biceps/triceps/forearm definition;
- quad teardrops;
- calf bellies;
- large projected gluteals;
- obesity or belly mass.

## 3. Protected macro contract

The following 05AB1 values are frozen as the composition-sculpt macro contract:

- crotch: **48.5 % of height**;
- fingertip: **44.5 % of height**;
- knee: **26.88 %**;
- ankle: **4.45 %**;
- elbow/wrist shares: preserve within measurement noise of 05AB1;
- Gorrund relative reach must remain shorter than Grask E3;
- topology: identical triangle connectivity;
- one welded component;
- no boundary/non-manifold edges;
- zero self-intersections;
- zero flipped faces.

Diagnostic preservation tolerance:
- crotch / fingertip / knee / ankle: **±0.2 percentage points** from 05AB1 unless a local surface change makes a section-based reading unstable; in that case disclose and verify the actual joint/segment geometry did not move.

Do not move joint centres to make the sculpt easier.

## 4. Protected regions

Do not intentionally alter in 05AC:

- head / muzzle / ears;
- neck length;
- hands / digits;
- feet / toes;
- terminal hand/foot scale;
- free tail;
- tail-root/gluteal-cleft fusion;
- heel lift;
- final foot-size decision;
- genus handles.

### Head share
The corrected body's head is approximately **10.5 % of height** versus about 12.6 % on W1.

**Do not scale or reshape the head in this order.**

Reason: the body is still severely heroic. First neutralize composition, then judge the head visually against the corrected final body. Head scaling now would confound that review.

## 5. Manual sculpt method

This must be **real Blender sculpt/edit work on the applied 05AB1 mesh**.

Allowed:
- Sculpt Mode Smooth / Surface Smooth / Relax;
- restrained Flatten / Scrape;
- restrained Grab / Elastic Deform for soft-tissue volume only;
- Edit Mode vertex movement for local continuity;
- masks and face sets.

Forbidden:
- Dyntopo;
- voxel remesh;
- topology replacement;
- decimation;
- global remesh;
- scripted per-vertex coordinate shaping;
- solver-generated surface candidates;
- SDF / primitive reconstruction;
- shrinkwrap to W1 or another body;
- non-anatomical whole-body scaling;
- automated "reduce muscle" deformation;
- copying another race's surface.

Scripts may only:
- generate masks / face sets;
- verify preservation;
- render identical cameras;
- measure gates;
- report geometry.

They may not author the final sculpt shape.

## 6. Reference material

Use, in this priority order:

1. accepted W1i/W1j Gorrund ARM for macro/frame identity;
2. candidate 09 only as a **soft-tissue visual direction** (flat chest, low shoulder cap, slim-to-average limb tissue, not chubby);
3. A/B/C body-only exhibits as **negative heroic references**;
4. Marchfolk / Skarn / Grask frozen controls to ensure Gorrund does not collapse into another race.

Candidate 09 is not a silhouette target and must not be directly projected onto the mesh.

## 7. Sculpt checkpoints

Maximum **three deliberate production checkpoints**.

### AC1 — torso + shoulder girdle

Focus:
- flatten pectoral projection;
- remove central pec split and hard lower-pec shelf;
- reduce deltoid cap;
- soften trapezius/shoulder bodybuilder read without altering neck length;
- remove abdominal block segmentation;
- soften/remove serratus grooves;
- reduce love handles;
- preserve broad/deep rib cage and integrated thorax–lumbar–pelvis load-bearing identity.

Also clean any residual armpit compression fold that becomes visible as the lat/deltoid mass decreases.

Do not alter arms/legs beyond tiny continuity touches.

### AC2 — arms + legs

Focus:
- reduce biceps/triceps separation;
- neutralize corded forearm / vein-like surface definition;
- soften quad separation / teardrop;
- reduce calf belly definition;
- neutralize the vertically elongated heroic thigh forms created by the macro lengthening;
- preserve large joint scale and credible load-bearing limb mass.

Do not make limbs thin, weak or human-average in skeletal scale.

### AC3 — posterior / gluteal mass

Only if still needed after AC2.

Focus:
- reduce round projected gluteal bulk to natural untrained volume;
- soften bodybuilder posterior-thigh transition;
- preserve robust pelvis;
- preserve gluteal crease landmarks;
- clean the minor lateral gluteal-fold-end crease;
- visually soften the thigh-top stretch band if possible **without moving the pelvis/joint structure**.

Do **not** repair the tail-root fusion in AC3.

## 8. Geometry gates after every checkpoint

After each checkpoint:

1. save a distinct Blender scene;
2. export a review GLB;
3. run:
   - topology identity;
   - single-body gate;
   - boundary/non-manifold;
   - whole-mesh self-intersections;
   - flipped-face check;
   - macro-target preservation;
   - rigid-region comparison for head/hands/feet/free-tail;
4. render identical-camera:
   - whole F / P / B / 3/4;
   - body-only F / P / B / 3/4;
   - chest/shoulder/axilla;
   - abdomen/lumbar/pelvis;
   - arms;
   - thighs/knees/calves;
   - posterior/gluteal.

Reject a checkpoint that introduces:
- new intersections;
- new flips;
- melted or mannequin anatomy;
- flattened anatomical landmarks;
- dents/ridges/shelves;
- joint drift;
- obvious left/right asymmetry not present in the baseline;
- pinched waist;
- obesity compensation.

A failed checkpoint may be reverted; it does not require promoting it.

## 9. Q1 / Q2 decisive gate

After the best safe checkpoint, rerun the whole-source gate.

### Q1 — required YES
Does the body express the accepted Gorrund structural identity at **reference composition**?

### Q2 — required YES
With head and tail hidden, does it avoid reading as:
- enlarged human;
- bodybuilder;
- strongman;
- ogre/brute;
- Grask;

while preserving Gorrund's large structural frame?

### Additional decisive comparisons

Against donor A/B/C and 05AB1:
- clearly less heroic muscle definition;
- clearly less gluteal projection;
- no belly/fat compensation;
- broad/deep frame retained;
- joint scale retained;
- no loss of real sculptural anatomy.

## 10. Stop conditions

### Success

Return:

**05AC COMPOSITION NEUTRALIZATION PASS / AUTHOR VISUAL REVIEW REQUIRED**

Then STOP for Tyler's visual ruling.

Do not repair:
- head share;
- tail root;
- heels;
- feet;
- genus handles

until Tyler visually accepts the body composition.

### Failure

If three checkpoints cannot produce Q1/Q2 without damaging the macro structure or anatomical credibility:

**05AC MANUAL COMPOSITION LIMIT REACHED / HUMAN SCULPTOR REQUIRED**

Then STOP. No new generator loop.

## 11. State

Until Tyler visually accepts a successful 05AC return:

- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED;
- no LOW / blind final acceptance / scaffold;
- no D4 / UE5 / production rigging / creator implementation.

## 12. Return

Commit:

`reviews/claude-rac-rm-ot-05ac-gorrund-manual-composition-neutralization-gate.md`

Evidence:

`reviews/rac-rmot05ac-evidence/`

Preserve all prior source / AA / AB / AB1 history unchanged.
