# RAC RM-OT-05AS — AC3 final short-cleanup rerun with dihedral gate

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05AR.
**Date:** 2026-10-17.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05ar-gorrund-ac3-continuity-gate.md` (4ebf8bd).

## 1. Author ruling

05AR solved the tail-root continuity problem.

The remaining failure is now isolated to **over-smoothing of the lateral hip/front-thigh transition band**:
- tail plateau eliminated;
- tail core exact;
- continuity ring within limit;
- topology numerically clean;
- posterior volume visually correct;
- but ~144–150 Smooth events created visible bilateral transition folds.

The 05AR diagnostics show:
- transient deflate-only SI is already gone after about 10 Smooth events;
- increasing Smooth events mainly increases lateral transition dihedral/folding;
- buttock-depth improvement changes only modestly between ~25 and ~175 events.

Therefore the final AC3 attempt shall:
1. keep the successful ~8 mm deflate;
2. keep the 05AR tail core/ring and seam solution;
3. widen the front/lateral feather;
4. use only the **minimum Smooth cleanup needed for technical stability**;
5. gate visible fold formation using a strict edge-dihedral-increase metric.

## 2. Advancement source

Start only from:

`GO-05AO_AC2.blend`
SHA-256:
`ba129999cfe71c1ab7afc2f11c1b911bd1e85fc06f301e1bad9a483fcba4f6f3`

Review GLB:
`GO-05AO_AC2.glb`
SHA-256:
`1f60fb33fa0c75c9d0f9aa0c1315143005473fd5c72ada67ad922782240de434`

Do not advance from rejected 05AR geometry.

05AR AR1r is evidence only.

## 3. Reuse the proven 05AR structural solution

Reuse exactly:

### Immutable tail core
- all free-tail vertices;
- tail-junction vertices within 8 mm of the tail/junction interface;
- core centroid/emergence/axis/width/depth remain 0.000 mm.

### Tail continuity ring
- outer tail-junction continuity tissue;
- max movement <= 3.0 mm.

### Duplicate-position seams
- duplicate seam copies must carry identical mask values;
- pin duplicate-position seam vertices to 1.0;
- maintain >= 30 mm seam ramp.

These parts are considered solved and should not be redesigned unless the predictor proves a necessary local change.

## 4. Posterior field / feather refinement

Reuse the 05AR posterior field, but widen the troublesome front/lateral transition.

Required:

- lateral hip feather >= **80 mm**;
- front-lateral thigh feather >= **80 mm**;
- posterior-thigh feather >= **50 mm**;
- tail/root continuity ramp unchanged except where needed to preserve the solved result;
- graph Lipschitz slope no steeper than:
  - 1 / 80 mm in the lateral/front-thigh transition;
  - 1 / 50 mm elsewhere.

The active region may extend farther onto low-curvature side/front thigh tissue so the transition no longer terminates along the visible hip crease line.

Hard protect:
- tail core;
- genital;
- perineal;
- pelvis/sacral skeletal core;
- torso outside AC3 field;
- arms;
- knee/lower leg;
- hands/feet.

## 5. Deflate stage

Use the already calibrated AC3 deflate direction:

- Mesh Filter: Inflate;
- negative drag;
- Strength approximately 0.020;
- approximately -100 px;
- target about 7.9 mm x (1-mask) at fully sculptable belly tissue.

Do not increase deflate strength.

The posterior volume target is already correct.

## 6. Cleanup calibration — short only

The cleanup must be the **minimum Smooth amount required to remove transient technical defects**.

Before real authoring, simulate:

- 10 events;
- 15 events;
- 20 events;
- 25 events;
- 30 events;
- 40 events.

Also test one conservative Surface Smooth alternative if it is predicted to preserve the envelope better.

For each candidate record:
- new SI;
- flips;
- degenerates/collapse;
- max new edge-dihedral increase;
- max absolute edge dihedral;
- tail ring displacement;
- pelvis/hip/thigh metrics;
- buttock-depth change.

### Selection rule

Choose the **lowest event count** that gives:
- 0 SI;
- 0 flips;
- 0 degenerates/collapse;
- clean topology;
- visually usable posterior continuity.

Do not choose a larger cleanup merely because it looks marginally smoother.

## 7. New dihedral predictor gate

The old >60° fold gate was too permissive.

For every candidate cleanup, compare shared edges to GO-05AO_AC2.

Required before real authoring:

- no new edge-dihedral increase > **20°** in the active posterior transition field;
- no transition edge with absolute dihedral > **35°** unless that edge was already >=35° in GO-05AO_AC2;
- no coherent vertical chain of increased-dihedral edges along lateral hip/front thigh.

If 10–40 Smooth events cannot satisfy this gate, test one conservative Surface Smooth cleanup.

If neither route satisfies the gate:
**05AS SHORT-CLEANUP PLAN NOT CREDIBLE / STOP**
Do not author.

## 8. Real authoring

Maximum:
- one primary attempt;
- one bounded rerun only if a small technical/mask issue appears.

### AS1

From GO-05AO_AC2:

1. apply the refined mask;
2. perform the same ~8 mm UI deflate;
3. apply the selected **short cleanup** from §6;
4. save and gate.

Do not add broad manual smoothing afterward.

### AS1r

Allowed only if AS1 fails due to a small localized technical issue:
- revert to GO-05AO_AC2;
- refine mask / local protection;
- rerun at the same or lower deflate and cleanup strength.

No longer cleanup count is allowed on the rerun.

## 9. Optional tiny continuity touch

Only after an otherwise passing AS1/AS1r:

If there is **one small isolated residual line**, Claude may use one very light UI Smooth/Surface Smooth touch.

Not authorized for bilateral long creases or broad transition problems.

Full gate afterward.

## 10. Shape gates

Against GO-05AO_AC2:

### Tail core
- centroid/emergence/axis/width/depth: unchanged;
- free tail: 0.000 mm.

### Tail continuity ring
- max <= 3.0 mm.

### Pelvis
- width change <= 0.5%.

### Skeletal hip
- drift <= 0.5 mm.

### Upper posterior thigh
- mean-radius loss <= 3.0%.

### Other finished anatomy
- arms = 0.000 mm;
- torso outside field = 0.000 mm;
- lower legs = 0.000 mm;
- genital/perineal = 0.000 mm;
- hands/feet = 0.000 mm.

## 11. Technical gate

Required:

- 0 opened seams;
- 0 self-intersections;
- 0 flips;
- 0 degenerates;
- 1 component / 0 boundary / 0 non-manifold;
- duplicate seam pairs remain closed;
- tail core unchanged;
- continuity ring <= 3.0 mm;
- stature / bbox unchanged;
- pelvis / hip / thigh gates pass;
- **new edge-dihedral increase <= 20°** in transition field;
- no coherent lateral/front-thigh crease chain;
- no new shelf / dent / mask outline.

## 12. Visual gate

Compare:
- GO-05AO_AC2;
- rejected AQ1r;
- rejected AR1r;
- new AS result.

Required:
- keep AR1r's solved tail-root blend;
- keep the improved, natural posterior volume;
- eliminate the bilateral lateral hip/front-thigh crease;
- no jagged tail plateau;
- no patch outline;
- no front/3/4 vertical stripe;
- profile stays natural;
- buttocks substantial, not heroic and not flat;
- posterior thigh robust.

This is the final AC3 continuity cleanup. Do not chase microscopic smoothness at the expense of new folds.

## 13. Final output

If PASS, freeze:

`GO-05AS_AC3.blend`
`GO-05AS_AC3.glb`

Record exact hashes.

## 14. Decision

### PASS

Return:

**05AS AC3 PASS / READY FOR FINAL Q1-Q2 + TYLER VISUAL REVIEW**

Then STOP.

Do not alter:
- head share;
- tail redesign beyond the already-authorized continuity ring;
- heel lift;
- final foot size;
- genus handles.

### FAIL

Return:

**05AS AC3 FINAL CLEANUP NOT CREDIBLE / STOP**

Revert active composition state to GO-05AO_AC2.

## 15. Evidence

Return:
- refined mask visualization/readback;
- 10/15/20/25/30/40-event simulation table;
- Surface Smooth comparison if tested;
- dihedral-increase maps and chain detection;
- exact UI deflate and cleanup settings;
- topology gates;
- tail core/ring metrics;
- pelvis/hip/thigh metrics;
- buttock-depth change;
- identical-camera whole/body/posterior views;
- AO2 vs AR1r vs AS comparison;
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

`reviews/claude-rac-rm-ot-05as-gorrund-ac3-short-cleanup-gate.md`

Evidence:

`reviews/rac-rmot05as-evidence/`
