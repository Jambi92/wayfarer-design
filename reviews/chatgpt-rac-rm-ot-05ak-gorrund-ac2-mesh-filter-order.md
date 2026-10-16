# RAC RM-OT-05AK — bounded UI Mesh Filter AC2 from the clean 05AJ preflight baseline

**Authority:** Tyler authorizes Claude to perform the AC2 limb neutralization.
**Date:** 2026-10-16.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05aj-gorrund-ac2-arms-legs-gate.md` (e34402b).

## 1. Ruling

The 05AJ manual mouse-drag AC2 is rejected and must not be advanced.

The failure was methodological:
- light brush passes stayed technically clean but barely changed the heroic limb forms;
- repeated dense passes created stroke shelves/lumps and eventually 4 flipped faces.

Claude is now authorized to use Blender's **UI-applied Mesh Filter** inside the existing verified limb masks so the limb surface can be neutralized uniformly rather than by repeated remote mouse-drag strokes.

This is still interactive Blender authoring. It is not scripted vertex shaping.

## 2. Advancement source

Start only from the **passed 05AJ preflight baseline**, which already contains the two bounded micro-crimp repairs:

`GO-05AJ_preflight_baseline.blend`
SHA-256:
`453ee2ba8b39e1678cd63ff9cc682f34b7de244c47ec6daa84ab45fe560dd6d5`

Review GLB:
`GO-05AJ_preflight_baseline.glb`
SHA-256:
`6a6eb730903fbf89480b40b3c748ea7fc145078289bd35668752612a63fb46a1`

This baseline derives from the passed 05AI AC1 and preserves its accepted torso result.

Do not start from:
- `GO-05AJ_AC2.blend`;
- any p1-p6 rejected brush checkpoint;
- any earlier rejected AC1.

## 3. Frozen history

Preserve:
- 05AI local-quality baseline;
- passed 05AI AC1;
- 05AJ preflight baseline;
- rejected 05AJ AC2 and intermediate brush attempts as evidence only.

No overwrite.

## 4. AC2 visual target

The desired limb read is:

**large-framed / large-jointed Gorrund + ordinary untrained soft tissue**

Reduce:
- biceps peak and triceps groove;
- forearm cord/vein-like relief;
- quad separation and vertical heroic channels;
- teardrop above the knee;
- calf-belly bulge and gastrocnemius separation.

Preserve:
- large elbows, wrists, knees and ankles;
- hand and foot scale;
- corrected segment lengths;
- stance;
- overall load-bearing limb mass.

Do not make the limbs skinny, weak or human-average.

## 5. Mask contract

Recreate or reuse the verified 05AJ limb masks.

### Hard-protect
- head / upper neck;
- all passed 05AI AC1 torso;
- pelvis / genital region;
- glutes / posterior pelvis;
- tail / tail junction;
- perineal fold;
- hands beyond the 05AF wrist buffers;
- feet beyond the 05AF ankle buffers.

### Joint-preservation bands
Before running a shrinking/smoothing Mesh Filter, add extra protection around:
- elbows;
- wrists;
- knees;
- ankles.

Use a soft/feathered transition into the muscle bellies.

The point is to preserve joint scale while allowing muscle-belly soft tissue to relax.

### Mask-order rule
Any mask feathering must occur before the final hard protection masks are laid down.

No global Smooth Mask after final hard protections exist.

Read back the saved `.sculpt_mask` before the first filter and prove:
- protected regions = 1.0;
- intended limb muscle zones are sculptable;
- joint centres are more protected than mid-belly tissue.

## 6. Authoring method

Use Blender Sculpt Mode **Mesh Filter through the normal UI only**.

Allowed filter families:
1. **Surface Smooth** or **Relax** for relief neutralization while preserving the broad envelope.
2. A restrained **Smooth** filter may be used only if Surface Smooth / Relax leaves the limb circumference materially too heroic.

Forbidden:
- Python console;
- scripting workspace;
- shell;
- scripted operator invocation for the authoring filter;
- scripted vertex shaping;
- Dyntopo;
- voxel remesh;
- broad proportional scaling;
- automated limb slimming outside the masked filter;
- mouse-drag zigzag smoothing like the rejected 05AJ method.

Scripts remain allowed only for validation, metrics and evidence after a saved checkpoint.

## 7. Filter budget

Maximum **three deliberate Mesh Filter applications total** for AC2.

Recommended progression:

### AK1 — relief neutralization
One Surface Smooth or Relax filter over the masked limb soft-tissue zones.

Use a conservative UI strength.

After saving, measure displacement versus the 05AJ preflight baseline.

Target diagnostic envelope:
- median moved limb vertex <= **1.5 mm**;
- p95 moved limb vertex <= **3.5 mm**;
- max <= **6.0 mm**.

This is a safety envelope, not a required amount of movement.

Run the complete technical and visual gate.

If the limb definition is already sufficiently neutralized, stop and PASS.

### AK2 — controlled bulk reduction, only if needed
If AK1 is technically clean but the biceps/quads/calves still project too strongly, apply one restrained **Smooth Mesh Filter** to the muscle-belly zones only.

Joint-preservation masks stay in place.

Cumulative displacement from the preflight baseline:
- p95 <= **5.0 mm**;
- max <= **9.0 mm**.

Run the full gate again.

### AK3 — optional final uniform blend
Only if AK2 is clean and the anatomy is close but a uniform transition is still needed.

Use one conservative Surface Smooth / Relax application.

Do not use AK3 merely to chase minor cosmetic perfection.

Cumulative hard ceiling from the preflight baseline:
- p95 <= **6.0 mm**;
- max <= **10.0 mm**.

If the visual target is not achieved within this budget, STOP rather than over-filtering.

## 8. No stroke shelves

The entire reason for 05AK is to avoid the rejected 05AJ stroke-boundary artefacts.

Do not add broad Smooth/Flatten brush strokes after the Mesh Filter.

A maximum of **two tiny UI-only continuity touches** is allowed only if:
- a filter leaves a single obvious transition ridge at a mask boundary;
- the correction is local and does not author broad limb shape.

Disclose any such touch.

## 9. One-time sliver reaction authority

The source still contains many low-quality triangles.

If a filter checkpoint is visually promising but fails **only** because of at most **6 isolated flipped/sliver faces**, with:
- 0 opened seams;
- 0 self-intersections;
- 0 degenerates;
- all protected regions unchanged;

then Claude may:

1. revert to the clean pre-filter checkpoint;
2. identify those exact faces;
3. apply the proven 05AI bounded local-quality repair to only those discrete two-ring neighbourhoods:
   - <= 0.5 mm vertex movement;
   - near-coplanar edge rotations only;
   - <= 0.5 mm patch surface deviation;
   - 0.000 mm outside the repair neighbourhoods;
4. freeze the repaired local baseline;
5. rerun the **same Mesh Filter application once** at the same or lower effective strength.

This is allowed **once total** in 05AK.

If:
- more than 6 isolated flips occur;
- a self-intersection appears;
- broad surface damage appears;
- or the rerun still fails;

STOP:
**05AK AC2 FILTER ROUTE NOT CREDIBLE / STOP**

Do not begin another repair loop.

## 10. Technical gate after every saved filter checkpoint

Required:

- 0 opened seams;
- 0 self-intersections;
- 0 flipped faces;
- 0 degenerate faces;
- 1 position-welded component;
- 0 boundary / 0 non-manifold;
- head: 0.000 mm;
- passed 05AI torso: 0.000 mm except explicitly mapped shoulder-transition vertices if unavoidable;
- glute/pelvis/genital/perineal: 0.000 mm;
- tail / tail junction: 0.000 mm;
- protected hands / feet: 0.000 mm;
- stature and bbox unchanged;
- crotch / fingertip / knee / ankle macro relationships preserved within prior diagnostic tolerance;
- no joint-centre drift;
- no new shelf, ridge, dent or melted patch.

## 11. Visual gate

Compare against passed 05AI AC1, not against the rejected 05AJ final.

Required:
- biceps/triceps separation clearly softer;
- forearms clearly less corded;
- quad channels materially softened;
- teardrop above knee materially reduced;
- calf bellies materially less heroic;
- overall limb silhouette still robust;
- joints remain visibly large;
- left/right treatment coherent;
- no obvious filter over-smoothing or mannequin look.

Use whole-body views to ensure the limbs now harmonize with the passed AC1 torso.

## 12. Output

Best passing AC2 checkpoint:

`GO-05AK_AC2.blend`
`GO-05AK_AC2.glb`

Record exact hashes.

Evidence must include:
- mask verification;
- filter type(s) and visible UI settings/strength for every application;
- per-checkpoint displacement metrics;
- per-checkpoint geometry gates;
- any local repair list if the one-time authority was used;
- identical-camera whole F/P/B/3/4;
- body-only F/P/B/3/4;
- arm front/3/4/profile;
- thighs/knees front/3/4;
- calves profile/back;
- comparison to passed 05AI AC1.

## 13. Decision

### PASS
Return:

**05AK AC2 FILTER PASS / READY FOR AC3 DECISION**

Then STOP.

Do not begin AC3 in this order.

### FAIL
Return:

**05AK AC2 FILTER ROUTE NOT CREDIBLE / STOP**

Revert to the passed 05AI AC1 as the active checkpoint and STOP.

## 14. State

Until later Q1/Q2 and Tyler visual acceptance:
- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED;
- no LOW / blind final acceptance / scaffold;
- no D4 / UE5 / production rigging / creator implementation.

## 15. Return

Commit:

`reviews/claude-rac-rm-ot-05ak-gorrund-ac2-mesh-filter-gate.md`

Evidence:

`reviews/rac-rmot05ak-evidence/`
