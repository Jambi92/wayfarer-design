# RAC RM-OT-05AB1 — armpit-web weight cleanup (cp3): gate

**Order:** `reviews/chatgpt-rac-rm-ot-05ab1-gorrund-armpit-weight-cleanup-order.md` (15b5942).
**Date:** 2026-10-15.
**Evidence:** `reviews/rac-rmot05ab1-evidence/`.
**Tools (additive):** `tools/rac/w1/rmot05ab1_drivers/`.

## Outcome

**05AB1 PASS — CLEAN MACRO-CORRECTED BASELINE FROZEN / READY FOR MANUAL COMPOSITION SCULPT**

| Requirement (§4–§5) | cp2 | **cp3** |
|---|---|---|
| Self-intersecting faces (whole mesh, pymeshlab) | 112 (L web 105, R web 7) | **0** |
| Flipped faces vs rest (whole mesh) | 27 | **0** |
| Welded components / boundary / non-manifold | 1 / 0 / 0 | **1 / 0 / 0** |
| Triangle index arrays | = donor | **= donor = cp2** |
| Single-body gate | PASS | **PASS** |
| Crotch (48.5 ± 0.2) | 48.5 % | **48.5 %** |
| Fingertip (window 43.8–44.8) | 44.5 % | **44.5 %** |
| Knee (26.9 ± 0.2) | 26.88 % | **26.88 %** |
| Ankle (4.3 ± 0.3) | 4.45 % | **4.45 %** |
| Elbow / wrist, L and R | 67.0 / 65.1 and 57.1 / 55.0 % | **Identical** (bones and pose unchanged) |
| Reach vs Grask E3 (37.0 %) | Shorter | **Shorter** |
| Head / hands / feet / tail | Rigid | **Rigid**, same residuals (≤ 0.065 mm) |
| Donor `513bc9e2…`, AA baseline `c17ac3c2…`, cp2 files | Untouched | **Untouched** (hashes re-verified) |

Only one checkpoint (cp3) was produced. Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**.

## 1. What was wrong in cp2

In each armpit web, C's inner upper arm lies against the latissimus. The cp2 geodesic labels gave the two touching surfaces different trunk : upper-arm splits. When the upper arm was shortened towards the shoulder, the arm surface moved up and in, and passed through the stationary lat.

## 2. The change: weights only (`ab1_web_weights.py`, `ab1_apply_cp3.py`)

### Contact zone

Per side, the contact zone is:
- upper-arm-dominant vertices within 1.5 cm of trunk-dominant vertices, and the reverse;
- excluding the ordinary cp2 label seam, which is already a blend.

Contact centres (rest, raw cm):
- **L:** (24.6, −39.1, 125.5), 248 vertices.
- **R:** (−18.5, −33.0, 125.3), 185 vertices.

### Web region

The web region is the vertices within 11 cm of the contact zone: a 5 cm core plus a 6 cm fade.

Inside it, only the **trunk : upper-arm split** of each vertex's trunk + upper-arm weight mass was replaced by its **Euclidean Gaussian average** (σ = 3 cm). Touching surfaces therefore carry matching splits and move together. The result fades back to the cp2 split with a smoothstep.

Any other group's weight on those vertices was kept exactly. This applies, for example, to a small forearm share near the elbow.

### Sliver equalisation

Two near-degenerate source triangles were flipping:
- area 0.08 mm² at the L posterior shoulder seam, (14.4, −21.6, 145.2);
- 0.29 mm² at the back of the R upper-arm web, (−24.1, −22.3, 135.8).

Their vertices, 8 and 6 including seam duplicates, were given one common trunk : upper-arm split. A triangle whose vertices share weights maps affinely through positive-determinant bone transforms, so it cannot invert.

**Disclosure:** the L shoulder sliver lies about 20 cm above the web, at the cp2 shoulder label seam. It was one of the 27 cp2 flipped faces that the order counted "in the same bounded patches". Its 8 vertices' trunk / upperarm_L split changed by at most 0.0098.

### Amounts (`weights/apply_cp3.json`, `weights/changed_weights_cp2_to_cp3.npz`)

| Item | Value |
|---|---|
| Changed vertices | **32,995** (UV-seam duplicates counted; L web 18,230, R web 14,072, plus the slivers) |
| Changed weight entries | **65,988** |
| trunk | 32,995 entries |
| upperarm_L | 18,588 entries |
| upperarm_R | 14,405 entries |
| Largest single change | 0.512 (L), 0.412 (R) |
| Removed entries | 0 |
| All other groups (forearm, hand, thigh, shin, foot) | **Max change 0.0** |

Weights are quantised to 1e-4. Exact-position duplicates have identical weights (maximum mismatch 0).

### What was not changed

- bones, joint centres, segment scales, pose and root lift (all read from the cp2 rig);
- the Armature modifier;
- topology;
- no surface coordinate was set.

The surface comes only from Blender's Armature modifier evaluating the new weights.

Movement against cp2: 29,908 vertices moved by more than 0.01 mm, at most **13.4 mm**, all inside the two webs.

### Design preview

The weight design was previewed with an exact numpy reproduction of the cp2 Armature deformation (`ab1_preview.py`; matches Blender to 0.0003 mm). Two smoothing widths were tried in that preview:

- An earlier variant that excluded mixed-weight vertices created weight jumps and many flips. It was discarded before any checkpoint.
- The variant that keeps the split mass gave 0 intersections and 2–3 sliver flips.
- That variant plus sliver equalisation gave 0 / 0.

Only the final weight set was written into Blender, producing the single cp3 result. All gates were re-run on the Blender output.

## 3. Checks (`checks/`)

| Check | Result |
|---|---|
| `single_body_gate_cp3.json` | PASS: 1 component, 0 boundary / non-manifold |
| `inspection_cp3.json` | **0 self-intersecting faces** (whole welded mesh). Genus 3, unchanged. |
| `intersection_and_flip_faces_cp2_vs_cp3.json` | cp2: 112 face ids and 27 flipped ids, with clusters. cp3: none. |
| `preservation_cp3.json`: topology | Identical to the donor; 1 / 0 / 0 before and after |
| `preservation_cp3.json`: normals | **0 flipped**; 4 faces rotated more than 60° (cp2: 52) |
| `preservation_cp3.json`: rigid blocks | Head 0.0001 mm; hands 0.023 / 0.019 mm RMS; feet 0.002 / 0.003 mm; tail 0. Extents unchanged. |
| `preservation_cp3.json`: upper-arm edge ratios | Minimum **0.62 / 0.65** (cp2: 0.28 / 0.19). No edge below 0.6 anywhere (cp2: 1,052). |
| `macro_targets_cp3.json` | All windows met (table above) |
| `tile_check_bodyonly_cp3.json` | 4 body-only tiles clean |

The trunk still has 1,418 edges stretched more than 1.6×. This is the cp2 thigh-top / gluteal-fold band at the pelvis weight boundary. cp3 does not touch it, and it is not an intersection or a flip.

## 4. Visual gate (`views/`, cp2 vs cp3 with identical cameras)

Views:
- `01_whole_F_P_B_Q`;
- `02_bodyonly_F_P_B_Q`;
- `03_armpit_webs_close`;
- `03b_web_left_tight`, `03c_web_right_tight` (tight F / B / underside / two oblique views per web);
- `04_shoulder_elbow_wrist`;
- `05_pelvis_knee_unchanged`;
- `06_equal_height_C_cp2_cp3_W1_controls`;
- `07_web_weight_maps_cp2_vs_cp3`.

Findings:
- **No new defect** in either web: no shelf, hole, ridge, lip, crease or dent, and no detached-looking arm.
- **Left web:** cp2's crossing compression lines on the inner arm are smoothed out in cp3.
- **Right web:** cp2's dark flipped-face dot at the back of the upper arm is gone.
- **Elsewhere:** shoulders, elbows, wrists, pelvis and legs are unchanged.

## 5. Frozen clean baseline (the only advancement baseline)

| File | SHA-256 | Contents |
|---|---|---|
| **`GO-05AB1_macro_corrected_clean.blend`** | **`79727daa2552842ddb0ec80505334a4c091ccc026c469e35de7c6c1b7d098a61`** | Applied cp3 mesh, object `GO-05AB1_macro_corrected_clean`. No rig. Donor, AA and rig-cp2 hashes stored as properties. |
| **`GO-05AB1_macro_corrected_clean.glb`** | **`03693479be311e72fd608728e6d978ee24169f7fefd679bbc872990061b35e0b`** | Geometry-review GLB |
| `GO-05AB1_macro_corrected_rig_cp3.blend` | `a20d11fe6294738096e6fe587ff959f222519e2e5b5e599548d820b9454220b1` | Non-destructive cp3 scene: working copy, temporary rig, cleaned vertex groups |

All three are stored at `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Neutral-C\05AB1\`. The .blend files are split into parts with `REJOIN.txt`. They were saved with Blender 5.0.1.

The cp2 files (`082952ea…`, `8fc584af…`, `f44e70aa…`) remain historical evidence, unchanged.

## 6. Carried open items (not repaired here)

- heroic soft-tissue composition;
- elongated heroic thigh muscle forms;
- **head share about 10.5 %** of corrected height against W1's about 12.6 %: OPEN FOR LATER VISUAL / AUTHOR REVIEW; not scaled;
- tail-root / gluteal-cleft fusion;
- heel lift;
- final foot-size judgement;
- genus handles;
- minor gluteal-fold-end crease and the thigh-top stretch band at the pelvis weight boundary.

**STOP.** The composition sculpt does not begin until this clean baseline is reviewed. No LOW, blind, scaffold, D4, UE5, rigging or creator work.
