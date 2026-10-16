# RAC RM-OT-05AB1 — one-checkpoint armpit-web weight cleanup and macro-baseline freeze

**Authority:** Author ruling on RM-OT-05AB return.
**Date:** October 15, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05ab-gorrund-macro-reproportion-feasibility-gate.md` (4b53ea2).

## 1. Author ruling

The 05AB macro-reproportion method is **accepted as feasible**.

Checkpoint 2 successfully restores the intended Gorrund macro relationships:
- crotch 48.5 %;
- fingertip 44.5 %;
- knee 26.9 %;
- terminal anatomy rigid/preserved;
- topology preserved;
- no visible rubber-hose, collapsed-joint, pelvis or hand/foot distortion.

However, checkpoint 2 is **not yet frozen as the clean macro baseline** because the order's no-new-intersections gate is still violated:

- 112 new self-intersecting faces;
- 105 left armpit web, 7 right;
- 27 flipped faces in the same bounded patches.

Do not waive this technical defect when a bounded mechanical correction is available.

Authorize **one and only one additional checkpoint**, designated **05AB1 / cp3**, limited to the arm-trunk skinning weights around the armpit webs.

## 2. Starting point

Use the non-destructive cp2 rig scene:

`GO-05AB_macro_corrected_rig_cp2.blend`
SHA-256:
`8fc584af6c9ee16130ee5ac50d8a9c8a4422df8093288e829f363eafb2c922db`

The applied cp2 geometry remains preserved separately:

`GO-05AB_macro_corrected_cp2.blend`
SHA-256:
`082952ea17f7f9be7a0fa13cc4f86fe198510b1b4aba85c08e5b47cf4dd1ad46`

`GO-05AB_macro_corrected_cp2.glb`
SHA-256:
`f44e70aab5d735d1f1005c98e848ae412cd560eff00d55061e4e3140a0fa2bde`

Do not modify or overwrite these cp2 records.

## 3. Scope — weights only

Allowed changes:

- adjust the **trunk / upperarm_L / upperarm_R** blend weights in the two armpit-web patches;
- widen the geodesic blend band locally if needed;
- assign the deepest web vertices more strongly to the trunk if that produces the cleaner anatomical result;
- make a symmetric method where anatomy supports it, while allowing side-specific weight magnitudes if required by C's source asymmetry.

No bone length, joint centre, bone scale, root lift, limb target, pose or topology change is authorized.

Do not alter:
- thigh/shin/foot groups;
- forearm/hand groups except unavoidable shared transition vertices immediately adjacent to the upper-arm group;
- pelvis/trunk geometry;
- head;
- hands;
- feet;
- tail;
- any surface vertex coordinates directly.

The surface must still be produced only by the existing armature modifier from changed weights.

## 4. Frozen macro targets

cp3 must preserve:

- crotch: **48.5 % ± 0.2 pp**;
- fingertip: **44.3 % target, accepted diagnostic window 43.8–44.8 %**;
- knee: **26.9 % ± 0.2 pp**;
- ankle: **4.3 % target, within 0.3 pp**;
- wrist / elbow shares no worse than cp2;
- Gorrund relative reach remains shorter than Grask E3 under the established reading.

If any target regresses outside those windows, cp3 fails even if intersections improve.

## 5. Required technical result

The purpose of cp3 is narrow:

**new armpit-web self-intersections: 112 → 0**

Also require:
- flipped faces in the two patches: **0**;
- 1 welded component;
- 0 boundary edges;
- 0 non-manifold edges;
- topology / triangle index arrays identical;
- single-body gate PASS;
- no new self-intersections anywhere else;
- no new visible web shelf, armpit hole, ridge, lip, crease, dent or detached-looking arm;
- no hand/foot/head deformation;
- donor and AA baselines remain untouched.

If zero intersections cannot be achieved through weights alone in this one checkpoint without violating the frozen macro targets, STOP. Do not add a fourth rig checkpoint.

## 6. Evidence

Provide before/after cp2 vs cp3:

- whole F / P / B / 3/4;
- body-only F / P / B / 3/4;
- close left and right armpit webs;
- shoulder/elbow/wrist close-up;
- equal-height C / cp2 / cp3 / W1 / frozen controls;
- weight visualization in each web;
- exact changed vertex count / changed weight count;
- intersection-face list before and after;
- normals / flipped-face report;
- macro target report;
- topology and preservation checks.

## 7. PASS and baseline freeze

If cp3 meets every requirement, return:

**05AB1 PASS — CLEAN MACRO-CORRECTED BASELINE FROZEN / READY FOR MANUAL COMPOSITION SCULPT**

Freeze a new applied baseline such as:

`GO-05AB1_macro_corrected_clean.blend`

and an equivalent geometry-review GLB.

Record exact SHA-256 hashes.

The cp2 files remain historical evidence; cp3 becomes the only advancement baseline.

### Carried open items

Do **not** repair these in 05AB1:
- heroic soft-tissue composition;
- elongated heroic thigh muscle forms;
- head proportion now ~10.5 % of corrected height vs W1 ~12.6 %;
- tail-root / gluteal-cleft fusion;
- heel lift;
- final foot-size judgement;
- genus handles;
- minor gluteal-fold-end crease if it persists.

The head-share difference remains **OPEN FOR LATER VISUAL/AUTHOR REVIEW**; do not scale the head here.

## 8. FAIL

If weights alone cannot produce zero intersections while preserving macro targets, return:

**05AB1 WEIGHT CLEANUP LIMIT REACHED — MACRO METHOD VALID / LOCAL SCULPT CLEANUP REQUIRED**

In that case preserve cp2. Do not abandon the entire macro route merely because this local web needs manual sculpt cleanup.

## 9. State

Until a clean macro baseline is frozen and composition sculpt succeeds:
- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED;
- no LOW / blind final scoring / scaffold;
- no D4 / UE5 / production rigging / creator implementation.

## 10. Return

Commit:

`reviews/claude-rac-rm-ot-05ab1-gorrund-armpit-weight-cleanup-gate.md`

Evidence:

`reviews/rac-rmot05ab1-evidence/`

STOP after the cp3 ruling. Do not begin the composition sculpt until the clean baseline is reviewed.
