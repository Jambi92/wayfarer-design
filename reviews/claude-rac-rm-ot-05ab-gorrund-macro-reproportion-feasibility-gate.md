# RAC RM-OT-05AB — rig-assisted macro-reproportion feasibility from donor C: gate

**Order:** `reviews/chatgpt-rac-rm-ot-05ab-gorrund-macro-reproportion-feasibility-order.md` (58d9e99).
**Date:** 2026-10-15.
**Evidence:** `reviews/rac-rmot05ab-evidence/`.
**Tools (additive):** `tools/rac/w1/rmot05ab_drivers/`.

## Outcome

**05AB MACRO REPROPORTION FEASIBLE — NOT PASSED ON ONE LISTED CRITERION: NEW ARMPIT-WEB SELF-INTERSECTIONS (112 faces, bounded) / AUTHOR RULING REQUIRED**

### Met at checkpoint 2, the best and final checkpoint (budget 2/2 used)

**Targets:**
- Crotch at **48.5 %** of height (target 48.5 ± 0.5).
- Lowest fingertip at **44.5 %** (target 44.3 ± 0.5). Relative reach is now far *less* than Grask E3's (37.0 %), so the Gorrund-vs-Grask rule holds.

**Joints reproduce the W1 shares where the order asks:**

| Joint | Checkpoint 2 | W1 |
|---|---|---|
| Knee | 26.9 % | 26.9 % |
| Wrist, R | 55.0 % | 55.0 % |
| Wrist, L | 57.1 % | — |
| Elbow, L / R | 67.0 / 65.1 % | 68.2 % |
| Ankle | 4.5 % | 4.3 % |

**Topology:**
- Triangle index arrays are identical to the donor's.
- 1 welded component; 0 boundary edges; 0 non-manifold edges.
- Single-body gate PASS.

**Terminal anatomy is unchanged:**
- Hands, feet, head and the free tail move rigidly. Best-fit residual is ≤ 0.065 mm; rotation is ≤ 0.01°.
- Extents and digit topology are identical.

**Visual:** no rubber-hose limbs, collapsed joints, pinched pelvis, stair-steps or shearing in the whole, body-only or close-up views.

### Not met

**112 new self-intersecting faces** (the donor had 0), all in the **armpit webs**: 105 faces on the left at about raw (24, −38, 126) and 7 on the right.
- There, C's inner upper arm is fused to, or lies against, the latissimus. Shortening the upper arm towards the shoulder pushes the arm surface into the lat.
- 27 faces flip in the same two patches.
- The order lists "new intersections" as a reject trigger, so I do not declare PASS.
- The defect is a few cm² per side and invisible at review scale (`06`). It is the kind a sculptor removes with Grab and Smooth, and the later composition sculpt reduces exactly that lat/biceps volume.

Calling the route "not credible" would misreport it, so neither order phrase is used unqualified. The author decides; see §8.

The donor (`513bc9e2…`) and the AA baseline (`c17ac3c2…`) were read only. The derivative is new and separate.

Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**.

## 1. Inputs (pinned, verified)

- **Donor** `Gorrund_Neutral.glb`, `513bc9e2…`. Not opened for writing.
- **AA baseline** `GO-05AA_C_baseline.blend`. SHA-256 `c17ac3c2…` was checked by every script before reading.
- **Macro guide:** W1 ARM `reviews/rac-w1i-evidence/geometry/GO_r6.npz`. Joint record shares: shoulder 81.2, elbow 68.2, wrist 55.0, hip 52.5, knee 26.9, ankle 4.3 % of height. AA0 levels: crotch 48.5 %, fingertip 44.3 %. Used for numbers only; no W1 surface was copied or targeted.

## 2. Where C's proportions differ (`joints_C.json`, section-estimated)

| Joint (raw cm, % of 189.8) | C | Method |
|---|---|---|
| Shoulder (glenohumeral) | 144.3 (76.0 %) | 0.04 H medial to the most lateral deltoid point |
| Elbow L / R | 118.6 / 114.8 (62.5 / 60.5 %) | Arm-perimeter minimum between the upper-arm and forearm maxima |
| Wrist L / R | 95.1 / 91.3 | Arm-perimeter minimum above the hand flare |
| Crotch | 84.5 (44.5 %) | Section merge |
| Knee | 52.4 (27.6 %) | Leg-perimeter minimum between thigh and calf |
| Ankle | 9.1 | Shin-loop centre |

Re-measuring the shoulders confirmed that C's **trunk and shoulder height shares already match W1**. Shoulder-cap top is 82.4 % against 83.3 %, and crotch-to-shoulder is 35.2 % of the corrected height against 34.8 %.

C's errors are therefore:
- **short thighs:** femur segment only about 21 % of height, against 25.7 % for W1;
- **long arms:** each limb needs about 13–14 % less shoulder-to-wrist length.

This sets the method: lengthen the legs (thigh mostly), shorten the humerus and forearm equally per side, leave the trunk alone. The order's trunk deferral holds.

## 3. Method (order §4)

### Temporary armature (`ab_rig.py`)

- **Bones:** trunk (root; pelvis, spine, neck, head and tail rigid); upper arm, forearm and hand per side; thigh, shin and foot per side. Bones sit on the estimated joint centres.
- **Deformation:** Blender's **Armature modifier** only (linear-blend skinning). Pose scale is applied along each bone's own axis.
  - thigh **×1.370**, shin **×1.058**;
  - upper arm and forearm **×0.858 (L) / ×0.877 (R)**;
  - hands and feet use inherit-scale NONE, so they stay rigid.
- **Grounding:** the trunk root is lifted 14.73 cm so the soles return to z = 0.
- **What scripts did:** placed the bones, assigned the vertex groups, computed the scales and verified metrics. They wrote **no per-vertex shape**.

### Vertex groups (`ab_weights.py`)

- **Hard labels:** each vertex is labelled by **geodesic surface distance** to seed loops placed symmetrically either side of each joint, so label boundaries fall on the joints.
- **Blending:** labels are then blended with a geodesic softmax (T = 1.5 cm, two strongest groups).
- **UV-seam duplicates** receive identical weights, so no cracks appear.
- Diagnostic: `views/08_temp_rig_vertex_groups_cp*.png`.

**Nothing forbidden was used:** no Dyntopo, remesh, decimation, shrinkwrap, W1 vertex fitting, global non-segmented warp or other race's surface.

## 4. Checkpoints (2 of 2)

| | Checkpoint 1 | Checkpoint 2 |
|---|---|---|
| Change | Thigh pivot at the estimated hip joint (crotch + 4 % H) | Trunk also seeded at the pelvic ring (crotch + 1 cm). Thigh pivot moved onto the crotch plane, so the groin stays with the rigid pelvis. |
| Crotch | **47.5 %** (miss): the groin was weighted to the thigh and pulled down | **48.5 %** |
| Fingertip | 44.5 % | 44.5 % |
| Height (raw) | 204.5 | 204.5 |
| Self-intersections | 112 (armpit webs) | 112 (same; arm settings unchanged) |

Both are recorded in `checkpoints/plan_input_cp*.json` (plan inputs), `plan_result_cp*.json` (scales and joints before and after) and `macro_cp*.json`.

## 5. Preservation checks (§6; `checks/`)

| Check | Result |
|---|---|
| Topology identity | **Identical** triangle arrays: 556,391 vertices, 1,000,000 triangles |
| Components / boundary / non-manifold | 1 / 0 / 0, both before and after (`preservation_cp2.json`). Single-body gate PASS (`single_body_gate_cp2.json`). |
| Self-intersections | **0 → 112**: armpit webs only, L 105 and R 7 (`inspection_cp2.json`). Genus unchanged at 3. |
| Head | Rigid. Residual 0.0001 mm; translation +14.73 cm z; extents 35.4 × 35.8 × 21.5 unchanged. |
| Hands L / R | Rigid. RMS 0.023 / 0.019 mm; rotation 0.009° / 0.003°; extents unchanged; digit topology identical. |
| Feet L / R | Rigid. RMS 0.002 / 0.003 mm; extents unchanged. The feet move 2.2–2.3 cm laterally, because the thigh and shin axes are slightly oblique, which slightly widens the stance. |
| Tail free portion | Rigid with the pelvis, residual 0. The root/gluteal fusion is untouched, as deferred. |
| Pelvis landmarks | Groin and gluteal crease stay with the rigid trunk. The lateral ends of the gluteal fold show a slight new crease (`07`). |
| Joint continuity: elbow / knee / wrist / ankle | Smooth (`03`–`05`). Forearm edge ratio 0.78–1.04. Shin 0.91–1.39. |
| Thigh | Median edge ratio 1.22; 99th percentile 1.67–1.73. **A ≈2 cm band at the thigh top** (raw z 79–82 before) reaches 1.6–2.1 because the geodesic weight boundary sits slightly below the pivot plane. It is not visible at review scale (`07`). |
| Face normals | 27 flipped and 52 rotated > 60°, all in the two armpit patches |

## 6. Visual artifact gate (§7)

`views/`, identical cameras for donor and derivative:
- `01_whole_F_P_B_Q`;
- `02_bodyonly_F_P_B_Q`: the same donor face mask was removed from both, and all 8 tiles are clean;
- `03_close_shoulder_elbow_wrist`;
- `04_close_pelvis_hip_knee`;
- `05_close_ankle_foot`;
- `06_zoom_armpit_web`;
- `07_zoom_thigh_top_gluteal_fold`;
- `09_equal_height_C_CP2_W1_controls`: donor C, checkpoint 2, W1 ARM and the frozen Skarn, Marchfolk and Grask E3, at 1.90 m displayed height with crotch and fingertip lines.

Close-ups are centred on each mesh's own joints (rest vs posed), at identical scale.

| Reject trigger | Finding |
|---|---|
| Rubber-hose limbs | No. Segments shorten or lengthen along their axes; elbows, wrists and knees keep their form. |
| Collapsed joints | No |
| Stretched / compressed hands or feet | No (rigid, measured) |
| Pinched pelvis | No. Pelvis rigid; groin unchanged. |
| Surface shearing | Not visible. The thigh-top stretch band is measurable but not visible. |
| Stair-step transitions | No |
| Major fold artifacts | No. There are micro-folds (27 faces) in the armpit webs, and a slight crease at the lateral gluteal-fold ends. |
| **New intersections** | **Yes: 112 faces, armpit webs** |

## 7. What the derivative is and is not

The derivative carries C's surface on a **W1-compatible macro skeleton**: legs long enough, arms short enough, joints at W1 shares.

**Unchanged by design**, and still to be handled:
- **Heroic soft tissue.** Deferred to the composition sculpt.
- **Thigh muscle forms.** These are vertically elongated, because the thigh segment is now 37 % longer along its axis. They are part of the soft-tissue sculpt anyway.
- **Head preserved at C's absolute size.** It is now **10.5 %** of height, against W1's 12.6 %, so it reads proportionally small. This is a possible separate author decision; nothing here changes it.
- **Hands preserved.** About 11.6 % of the new height, against W1's 10.7 %. Large; acceptable under "very large hands".
- **Feet.** 19.3 % of height, down from 20.8 %.
- **Tail root fusion and heel lift.** Still deferred.

## 8. For the author

1. **Accept the armpit-web intersections as bounded and sculpt-cleanable.** Freeze checkpoint 2 as the macro-corrected baseline. The first manual step of the composition sculpt is then to separate the inner arm from the lat and smooth the two micro-fold patches and the gluteal-fold ends. This is my recommendation: it is the only defect, and it is about 2 cm² per side, in a region the composition sculpt rebuilds anyway.
2. **Authorize one more rig checkpoint** limited to the arm–trunk weights: a wider trunk/upper-arm blend at the web, or the web assigned to the trunk. This would aim at 0 intersections without touching the met targets. It is outside this order's budget of 2.
3. **Treat it as FAIL.** Not supported by the evidence: the macro correction itself is clean.

## 9. Frozen outputs (not committed; stored on E:, split in 29 MB parts with `REJOIN.txt`)

| File | SHA-256 | Contents |
|---|---|---|
| `GO-05AB_macro_corrected_cp2.blend` | `082952ea17f7f9be7a0fa13cc4f86fe198510b1b4aba85c08e5b47cf4dd1ad46` | **Frozen macro-corrected baseline**: object `GO-05AB_macro_corrected`, with the deformation applied, no rig, and donor/baseline hashes as properties |
| `GO-05AB_macro_corrected_rig_cp2.blend` | `8fc584af6c9ee16130ee5ac50d8a9c8a4422df8093288e829f363eafb2c922db` | Non-destructive scene: working copy, temporary armature, vertex groups, Armature modifier |
| `GO-05AB_macro_corrected_cp2.glb` | `f44e70aab5d735d1f1005c98e848ae412cd560eff00d55061e4e3140a0fa2bde` | Geometry export for the review tools |

All three are stored at `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Neutral-C\05AB\`. They were saved with Blender 5.0.1.

**STOP.** No composition sculpt, no tail or heel repair, no LOW, blind, scaffold, D4, UE5, rigging or creator work.
