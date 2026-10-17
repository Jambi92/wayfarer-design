# RAC RM-OT-05AL — predictive limb quality pre-pass, then one AK1 filter rerun

**Authority:** Tyler authorizes Claude to perform the Gorrund AC2 mesh-quality preparation and retry.
**Date:** 2026-10-16.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05ak-gorrund-ac2-mesh-filter-gate.md` (aafa9f4).

## 1. Ruling

05AK proved that AC2 is blocked by distributed limb source-mesh quality, not by the Surface Smooth filter itself.

One conservative UI Surface Smooth application moved the limbs only:
- median 0.29 mm;
- p95 0.86 mm;
- max 3.12 mm;

yet produced 15 isolated flips across all four limbs.

Therefore authorize a **predictive limb-quality pre-pass** before any further AC2 authoring.

The objective is:

> Identify and repair every discrete limb face likely to flip under the exact AK1 masked Surface Smooth operation, using the proven bounded 05AI local-quality method, until a diagnostic dry-run predicts zero flips. Then perform one real UI AK1 filter rerun from that repaired baseline.

No AK2 / stronger bulk-reduction filter is authorized in this order.

## 2. Geometry source

Start only from the passed 05AJ preflight baseline:

`GO-05AJ_preflight_baseline.blend`
SHA-256:
`453ee2ba8b39e1678cd63ff9cc682f34b7de244c47ec6daa84ab45fe560dd6d5`

Review GLB:
`GO-05AJ_preflight_baseline.glb`
SHA-256:
`6a6eb730903fbf89480b40b3c748ea7fc145078289bd35668752612a63fb46a1`

This already contains the two accepted 05AJ local repairs and derives from passed 05AI AC1.

Do not use rejected 05AJ or 05AK geometry as the repair source.

## 3. Mask source

The verified mask layout from:

`GO-05AK_working.blend`

may be used as a **diagnostic mask reference only** because its geometry is unchanged from the 05AJ preflight baseline.

Its saved mask read-back already proved:
- all protected regions = 1.0;
- torso / glute / pelvis_other = 1.0;
- joint centres more protected than mid-belly tissue;
- limb muscle bellies remain sculptable.

If topology is locally retriangulated during 05AL, transfer / rebuild masks by shared vertex IDs and re-verify before the real UI filter.

## 4. Predictive dry-run

Use a scratch/in-memory copy only.

Reproduce the **AK1 Surface Smooth deformation diagnostically** using the exact 05AK saved mask values and the closest available numerical equivalent to the UI settings:

- Surface Smooth;
- Strength 1.000;
- Shape Preservation 0.500;
- Per Vertex Displacement 0.500;
- one equivalent application.

This diagnostic may be scripted because it is not saved or promoted and is used only to predict instability.

Also run one slightly stronger diagnostic stress case approximating the upper end of the next safe step, but do not author it:
- target roughly **2× AK1 displacement tendency**, or the closest reproducible diagnostic equivalent.

The purpose is to avoid repairing only the exact 15 observed AK1 flips and immediately discovering another set at the next small increase.

Record all faces that:
- flip in AK1-equivalent diagnostic;
- flip in the 2× diagnostic;
- or are directly adjacent to a flipped face and show a fold > 60° after the dry-run.

Deduplicate overlapping two-ring neighborhoods.

## 5. Repair budget

Maximum:
- **60 discrete repair neighborhoods** total;
- union of their two-ring vertex sets only.

If >60 non-overlapping neighborhoods are required, STOP:

**05AL PREDICTIVE REPAIR BUDGET EXCEEDED / AUTHOR RULING REQUIRED**

Do not perform broad optimization or generalized remeshing.

## 6. Local repair method

Use the proven 05AI / 05AJ local-quality method only.

Within each authorized two-ring neighborhood:

Allowed:
- tiny uniform-Laplacian / local relax of genuinely crimped corner vertices;
- vertex movement capped at **0.5 mm from the 05AJ preflight source**;
- near-coplanar edge rotations;
- local retriangulation only where necessary to remove a predicted inversion;
- repeated local passes only until the neighborhood no longer flips in the dry-run.

Required edge-rotation conditions:
- convex local quad;
- new diagonal not already present;
- near-coplanar incident faces;
- orientation preserved;
- local triangle quality not worsened overall.

Forbidden:
- movement outside authorized neighborhood union;
- broad limb smoothing;
- broad mesh optimization;
- remesh / voxel / Dyntopo / decimate / shrinkwrap;
- silhouette redesign;
- joint repositioning;
- changing hand/foot/head/tail/pelvis topology.

## 7. Repair preservation limits

Outside the repair-neighborhood union:
- **0.000 mm** movement required.

Inside:
- max vertex movement <= **0.5 mm**;
- target patch nearest-surface deviation <= **0.5 mm** in both directions;
- no visible silhouette change in identical-camera views.

Required global integrity:
- 0 self-intersections;
- 0 flipped faces;
- 0 degenerates;
- 0 duplicate faces;
- 1 position-welded component;
- 0 boundary;
- 0 non-manifold;
- all protected regions 0.000 mm;
- stature / bbox unchanged;
- macro joint/segment relationships unchanged.

## 8. Iterative predictive gate

After the first repair set:

1. rerun AK1-equivalent dry-run;
2. rerun 2× diagnostic stress case;
3. collect any newly predicted flips;
4. if within the 60-neighborhood total budget, repair only those new discrete neighborhoods;
5. repeat until either:
   - AK1-equivalent predicts **0 flips**, and
   - 2× stress predicts **0 flips**, or
   - budget / preservation limit is exceeded.

Maximum **3 repair-analysis cycles**.

Do not chase cosmetic quality scores; repair only instability demonstrated by the diagnostics.

## 9. Freeze predictive-safe baseline

If both diagnostics reach 0 predicted flips and all preservation gates pass, freeze:

`GO-05AL_predictive_limb_safe_baseline.blend`
`GO-05AL_predictive_limb_safe_baseline.glb`

Record exact hashes.

Return interim status:

**05AL PREDICTIVE LIMB PREP PASS / AK1 UI RERUN AUTHORIZED**

## 10. Rebuild and verify AK masks

Open the passed 05AL baseline in Blender UI.

Recreate the same joint-banded limb mask strategy used in 05AK:

- limb zones sculptable;
- elbows/wrists/knees/ankles strongly protected;
- passed 05AI torso hard-protected;
- glutes/pelvis/genital/perineal hard-protected;
- head hard-protected;
- hands/feet hard-protected;
- tail/tail junction hard-protected.

Any feathering must happen before final hard masks.

No Smooth Mask after final hard masks.

Read back the saved mask before filter authoring.

Required:
- protected regions min mask 1.0;
- torso/glute/pelvis_other min mask 1.0;
- joint centres materially more protected than muscle bellies;
- geometry unchanged from the frozen 05AL baseline before the filter.

## 11. One real UI AK1 rerun

Use Blender Sculpt Mode Mesh Filter through the normal UI only.

Settings:
- Filter Type: **Surface Smooth**
- Strength: **1.000**
- Deform Axis: XYZ
- Orientation: Local
- Shape Preservation: **0.500**
- Per Vertex Displacement: **0.500**
- one comparable application to 05AK AK1.

No scripted invocation.
No extra brush sculpting.

Save:

`GO-05AL_AK1.blend`

Export review GLB.

## 12. Real AK1 gate

Required:
- 0 opened seams;
- 0 self-intersections;
- 0 flipped faces;
- 0 degenerates;
- 1 / 0 / 0 topology;
- protected head / torso / pelvis / glute / genital / perineal / hands / feet / tail = 0.000 mm;
- stature / bbox unchanged;
- macro joint relationships preserved;
- no new shelf / ridge / dent / melted patch.

Displacement should remain in the same order of magnitude as 05AK AK1.
If substantially larger, disclose and STOP before any further filter.

## 13. Visual outcome

This AK1 rerun is primarily a **stability proof**, not expected to finish AC2 visually.

Compare to passed 05AI AC1:
- no stroke shelves;
- no filter artifacts;
- limb relief may be only subtly softer.

If technically clean, return:

**05AL AK1 STABILITY PASS / READY FOR CONTROLLED AC2 FILTER BUILDUP**

Then STOP.

Do not perform AK2 / AK3 in this order.

If the real UI AK1 still flips any faces after predictive prep:

**05AL PREDICTIVE PREP FAILED TO STABILIZE REAL AK1 / STOP**

Revert to passed 05AI AC1 as active checkpoint and STOP.

## 14. Evidence

Return:
- all predicted flip-face sets by diagnostic cycle;
- repair neighborhood union and count;
- exact changed vertices/faces/edges;
- movement and surface-deviation reports;
- AK1-equivalent and 2× dry-run results before/after;
- frozen 05AL baseline hashes;
- mask read-back;
- real AK1 gate JSON;
- identical-camera limb and whole comparisons.

## 15. State

Until later AC2 completion, Q1/Q2 and Tyler visual acceptance:
- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED;
- no LOW / blind final acceptance / scaffold;
- no D4 / UE5 / production rigging / creator implementation.

## 16. Return

Commit:

`reviews/claude-rac-rm-ot-05al-predictive-limb-quality-prep-gate.md`

Evidence:

`reviews/rac-rmot05al-evidence/`
