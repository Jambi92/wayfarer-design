# RAC RP2 — Grask rig-landmark adjudication and diagnostic-rig validation — gate

**Date:** 2026-10-25  
**Order:** `reviews/chatgpt-rac-rp2-grask-rig-landmark-adjudication-and-diagnostic-rig-order.md` (bf7d664)  
**Parent:** readiness gate 2558dc0  
**State:** **retopology frozen; v002 diagnostic landmarks built; one diagnostic-rig cycle executed — awaiting ChatGPT review.**

This was a diagnostic cycle only:
- no final skeleton, no production weights;
- no facial/oral mesh change, no morphs, UVs, LODs or UE5 work;
- no other race;
- no change to any frozen asset.

**Evidence:** `reviews/rac-rp2-evidence/grask_rig_diagnostic_v001/`  
**Tools:** `tools/rac/rp/grask_rigprep_v001/`

| Step | Script |
|---|---|
| Landmarks | `adjudicate.py`, `package.py`, `overlay2.py` |
| Rig | `rig_build.py`, `rig_clean.py`, `rig_check.py` |
| Diagnostics | `diag_lib.py`, `diag_run.py`, `dqs_eval.py`, `run_diag.sh`, `judge.py`, `evidence.py`, `cmp_sheet.py` |

---

## 1. Parent integrity

All parents were re-staged fresh from the PC and hashed before work, then re-staged and hashed again after work (`hashes/`).
- **Result:** before = after = the accepted values.
  - v003: `03bfe7d9…7ce0`, geometry `f9c4a7ac…702f`
  - v005: `7bba8d2d…ab14`, geometry `2697929d…d7bc`
  - v001 / v002 / sidecars / landmarks / freeze record: unchanged
- **How the rig was made:** the diagnostic rig was built from a *work copy* of the staged v003, and written only with save-as to a new path.
- **Rest mesh:** inside the rig file the body still has the frozen geometry hash `f9c4a7ac…`.

## 2. Author rulings implemented (all 12)

The v002 package (`GR_U_REF_RP2_rigprep_landmarks_v002.json` + `_tables.md` / `.csv`) validates **27/27** order checks (tables §Validation).

| Ruling | Implementation |
|---|---|
| AD-R1 hips | v001 consensus moved **5.0 mm** toward the proximal-thigh load axis, which lies 4.8 / 4.9 cm away. Sides not mirrored (x-sum 0.21 cm) |
| AD-R2 knee / ankle | Knee at z 71.17 / 71.20 and ankle at z 13.50 / 13.75, each on the horizontal limb-section centroid. Mediolateral axes, recorded as diagnostic engineering axes. The level is kept exactly; the section-centre AP/ML moved 0.58–1.10 cm from the v001 xy (see §6) |
| AD-R3 GH | Acromion anchor. The free upper-arm shaft line comes from 18 / 16 sections (z 145.8–154.1 / 146.0–153.4), extrapolated, with the centre **4.0 cm below the acromion** (3-D distance 4.89 / 5.21 cm). Depth 3.64 / 4.73 cm. Half-fit extrapolation spread 0.99 / 0.86 cm. The rule was satisfied, so no STOP. L/R asymmetry kept |
| AD-R4 elbow | v001 cubital target, moved 2.8 / 1.4 mm toward the reference-stance hinge. Bend-axis X kept |
| AD-R5 SC | Jugular/clavicular skin summit moved **3.0 cm straight posterior**. Depth 2.58 / 2.64 cm; SC–GH 21.96 / 22.90 cm; SC–acromion 23.96 / 25.49 cm |
| AD-R6 spine | spine_01–03 and neck_base are the frozen records, unchanged. thoracic_01/02/03 sit at 25 / 50 / 75 % of the interval (z 159.82 / 169.59 / 179.37), each on the torso-section centroid clipped to the trunk half-width (19.98 cm) so the arms do not bias it |
| AD-R7 root / pelvis | Root at the production origin. Pelvis = v001 proposal moved **5.0 mm** toward the section centroid → (0.01, 3.30, 123.93) |
| AD-R8 eyes / jaw | Eyes are non-deforming aim bones with no weights. No jaw bone. Jaw is **DEFERRED — REQUIRES FACIAL/ORAL COMPONENT STAGE** |
| AD-R9 scapula proxy | `scapula_medial_proxy_l/r`, class `manual-author-rig-proxy`: 60 % level (z 174.44 / 173.35), x = 45 % (10.78 / −11.09 source), projected onto the posterior surface |
| AD-R10 axes | Right-handed Blender frames; X = flexion axis toward +X on both sides; Y = toward the child; Z = X × Y. Bone rolls are aligned to frame Z |
| AD-R11 jaw label | v002 class is "deferred facial placeholder (rule-based)". The frozen record is unchanged |
| AD-R12 suite | D1–D10 run with the v001 thresholds as engineering diagnostics (§5) |

**Classes used in v002:**
- frozen surface marker / proxy;
- copied construction coordinate (surface-validated);
- `manual-author-rig`;
- `manual-author-rig-proxy`;
- deferred facial placeholder;
- rig control.

Every record carries:
- coordinates in the source, production and Blender frames;
- local frame, parent / children and segment length;
- construction rule and limitation;
- suitability.

## 3. Final diagnostic joint coordinates (production cm / Blender m)

| joint | production cm (x, f, u) | Blender m | depth in v005 cm | provenance |
|---|---|---|---|---|
| root | (0.00, 0.00, 0.00) | (0.0000, -0.0000, 0.0000) | 10.87 | rig control |
| pelvis | (0.01, 3.30, 123.93) | (0.0001, -0.0330, 1.2393) | 11.80 | manual-author-rig |
| spine_01 | (0.02, -2.76, 133.88) | (0.0002, 0.0276, 1.3388) | 5.62 | frozen package marker |
| spine_02 | (-0.22, -0.80, 142.42) | (-0.0022, 0.0080, 1.4242) | 6.53 | frozen package marker |
| spine_03 | (-0.47, -1.33, 150.04) | (-0.0047, 0.0133, 1.5004) | 6.86 | frozen package marker |
| thoracic_01 | (-0.34, 1.07, 159.82) | (-0.0034, -0.0107, 1.5982) | 12.31 | manual-author-rig |
| thoracic_02 | (-0.16, 0.28, 169.59) | (-0.0016, -0.0028, 1.6959) | 12.62 | manual-author-rig |
| thoracic_03 | (-0.23, -0.62, 179.37) | (-0.0023, 0.0062, 1.7937) | 7.95 | manual-author-rig |
| neck_base | (0.31, 1.37, 189.14) | (0.0031, -0.0137, 1.8914) | 4.79 | frozen package marker |
| head_pivot | (-0.08, 8.49, 200.18) | (-0.0008, -0.0849, 2.0018) | 7.37 | fitted joint-centre estimate |
| hip_l | (12.03, 3.33, 118.94) | (0.1203, -0.0333, 1.1894) | 7.00 | manual-author-rig |
| hip_r | (-12.04, 3.25, 119.09) | (-0.1204, -0.0325, 1.1909) | 6.95 | manual-author-rig |
| knee_l | (13.93, 0.28, 71.17) | (0.1393, -0.0028, 0.7117) | 5.84 | manual-author-rig |
| knee_r | (-13.49, 0.77, 71.20) | (-0.1349, -0.0077, 0.7120) | 5.93 | manual-author-rig |
| ankle_l | (15.53, 1.33, 13.50) | (0.1553, -0.0133, 0.1350) | 4.30 | manual-author-rig |
| ankle_r | (-15.61, -0.12, 13.75) | (-0.1561, 0.0012, 0.1375) | 4.29 | manual-author-rig |
| sternoclavicular_l | (3.58, 8.35, 178.27) | (0.0358, -0.0835, 1.7827) | 2.58 | manual-author-rig |
| sternoclavicular_r | (-2.43, 8.35, 178.37) | (-0.0243, -0.0835, 1.7837) | 2.64 | manual-author-rig |
| glenohumeral_l | (21.05, -4.70, 175.72) | (0.2105, 0.0470, 1.7572) | 3.64 | manual-author-rig |
| glenohumeral_r | (-22.75, -1.28, 174.04) | (-0.2275, 0.0128, 1.7404) | 4.73 | manual-author-rig |
| elbow_l | (26.32, -2.50, 142.77) | (0.2632, 0.0250, 1.4277) | 3.31 | manual-author-rig |
| elbow_r | (-26.94, -2.93, 142.99) | (-0.2694, 0.0293, 1.4299) | 3.69 | manual-author-rig |
| wrist_l | (30.79, 6.92, 105.00) | (0.3079, -0.0692, 1.0500) | 2.82 | copied construction coordinate |
| wrist_r | (-31.31, 6.72, 105.00) | (-0.3131, -0.0672, 1.0500) | 2.82 | copied construction coordinate |
| scapula_medial_proxy_l | (10.66, -13.09, 174.44) | (0.1066, 0.1309, 1.7444) | 0.00 | manual-author-rig-proxy |
| scapula_medial_proxy_r | (-11.21, -12.97, 173.35) | (-0.1121, 0.1297, 1.7335) | 0.00 | manual-author-rig-proxy |
| eye_l | (3.54, 16.12, 203.85) | (0.0354, -0.1612, 2.0385) | 1.17 | copied construction coordinate |
| eye_r | (-3.76, 16.12, 203.85) | (-0.0376, -0.1612, 2.0385) | 1.33 | copied construction coordinate |

Hand, foot and toe construction joints are unchanged from v001; all 122 records are in the JSON and tables.

## 4. Diagnostic rig

**File:** `GR_U_REF_RP2_rigdiag_v001.blend`
- SHA-256 `59ca4fdaedab42a2151ce6a9e699559bf3023bc4fb9c699b1af3b8975913e485`
- on the PC at `E:/…/Grask/RP2/DIAG/`; the PC copy was read back and the hash matches
- manifest: `rig/GR_U_REF_RP2_rigdiag_v001_manifest.json`

**Armature:** 86 bones, 83 deforming.

| Region | Bones |
|---|---|
| root | root |
| pelvis / spine / neck / head | pelvis, spine_01–03, thoracic_01–03, neck, head |
| legs | thigh, shin, foot, and 3 bones per toe (2 for the hallux) |
| arms | clavicle, scapula (medial proxy → acromion), upperarm, forearm, hand, 3 bones per finger, thumb metacarpal + 2 |
| eyes | eye_l/r, non-deforming |

**Weights:** Blender automatic (bone heat), computed in 41 s with no unweighted vertex.
- **One logged cleanup, in the diagnostic copy only:** side bones were zeroed more than 3 cm across the midline. This affected heat leakage of thigh / clavicle / scapula onto the opposite groin, sternum and upper back, at most 0.19 weight on 285–1101 vertices per bone.
- No other weight edits were made.

**Verification (`rig/rig_check.json`):**
- Blender armature deformation equals the numpy LBS used for every measurement: max 0.0006 mm over six poses.
- Pose → clear pose returns to the frozen mesh: **T-1 0.0002 mm**.
- Bone lengths equal the v002 landmark segment lengths: max 0.0001 mm, so **T-6 holds**.
- The surface landmarks on the returned mesh are therefore unchanged, with 0 drift.

## 5. D1–D10 results

**Setup:** 43 poses, run with linear-blend skinning and the diagnostic weights.

**Measurements:**
- non-contact / crease / contact intersections (BVH overlap, by part pair);
- crease penetration depth;
- new folds (dihedral > 120°), split into inside vs outside the crease;
- flipped faces against the skinned rest normal;
- total and tested-segment zone volume (the cone volume about the posed joint, restricted to that segment's own tissue);
- p95 edge strain in the zone;
- minimum joint-loop spacing ratio, on the frozen `LOOP_` groups;
- nail rigidity (Kabsch residual);
- rest-return.

**Test-setup choices (logged):**
- D2–D5 start from 45° shoulder abduction, because in the reference stance the palm lies on the thigh.
- D6 starts with that side's arm at 45°, because the hanging arm is against the lateral thigh.
- D5 is run as opposition to the pinky base, and as a pinch with the index flexed. The extended index tip is out of reach: CMC → index tip is 22.9 cm, against a thumb length of 15.7 cm.
- D1 also has girdle-assisted variants, in which the clavicle takes 20° of the elevation.
- D7 deep-flexion calf–thigh contact is treated as declared contact, as in v001.

The angles are technical tests, not range-of-motion canon.

**Comparison skinning:** the same weights were evaluated with Blender preserve-volume (dual-quaternion) on the 11 heaviest poses. **Placement comparison:** GH and hip pivots were swapped to the rejected / old alternatives, keeping the same weights.

**Result: 20 / 43 poses pass all retained criteria.**

| test | poses passed | passing | failing |
|---|---|---|---|
| D1 | 4 / 12 | D1_l_abd45, D1_l_ext30, D1_r_abd45, D1_r_ext30 | D1_l_abd90, D1_l_flex90, D1_r_abd90, D1_r_flex90, D1_l_abd90_girdle, D1_l_flex90_girdle, D1_r_abd90_girdle, D1_r_flex90_girdle |
| D2 | 1 / 3 | D2_l_base_abd45 | D2_l_flex90, D2_l_flex130 |
| D3 | 2 / 4 | D3_l_radial20, D3_l_ulnar20 | D3_l_flex60, D3_l_ext60 |
| D4 | 2 / 3 | D4_l_spread_p10, D4_l_spread_m10 | D4_l_fist |
| D5 | 0 / 2 | — | D5_l_oppose_pinky, D5_l_oppose_pinch |
| D6 | 2 / 6 | D6_l_abd30, D6_r_abd30 | D6_l_flex45, D6_l_flex90, D6_r_flex45, D6_r_flex90 |
| D7 | 0 / 2 | — | D7_l_flex90, D7_l_flex140 |
| D8 | 4 / 4 | D8_l_dorsi20, D8_l_plantar40, D8_l_toes_ext30, D8_l_toes_flex30 | — |
| D9 | 1 / 3 | D9_twist_p30 | D9_twist_m30, D9_flex30 |
| D10 | 4 / 4 | D10_flex30, D10_ext30, D10_rot_p45, D10_rot_m45 | — |

D2_l_base_abd45 is the abduction reference pose for D2–D5; it is counted under D2.

### 5.1 Per-pose pass / fail and failure classification

| pose | result | failed criteria | likely cause |
|---|---|---|---|
| D1_l_abd45 | PASS | — | — |
| D1_l_abd90 | **FAIL** | no new flipped faces (49 (49 in crease)); zone volume within ±5% (-6.6%); joint-loop spacing >= 50% of rest (0.23); crease contact depth <= 2 mm (4.5 mm) | diagnostic weights / linear-blend skinning: crease-zone compression at large angle (flips, crease interpenetration, loop compression confined to the crease zone) |
| D1_l_flex90 | **FAIL** | 0 non-contact intersections (38); no new flipped faces (359 (269 in crease)); no new folds outside crease/contact zones (+22 (outside 10)); zone volume within ±5% (-33.9%); joint-loop spacing >= 50% of rest (0.19); crease contact depth <= 2 mm (16.6 mm) | diagnostic rig configuration: pure GH flexion without girdle participation pinches the pectoral / anterior-axillary tissue (the girdle-assisted variant has 0 non-contact intersections) / diagnostic weights / linear-blend skinning: crease-zone collapse at large angle (the same weights with dual-quaternion preserve-volume reduce the zone volume change from -33.9% to -23.3%; flips / contact remain where tissue must meet) / diagnostic weights: fold outside the crease radius adjacent to the crease (see sheet) |
| D1_l_ext30 | PASS | — | — |
| D6_l_flex45 | **FAIL** | no new flipped faces (7 (7 in crease)); no new folds outside crease/contact zones (+18 (outside 1)); zone volume within ±5% (-6.6%) | diagnostic weights / linear-blend skinning: crease-zone compression at large angle (flips, crease interpenetration, loop compression confined to the crease zone) / diagnostic weights: fold outside the crease radius adjacent to the crease (see sheet) |
| D6_l_flex90 | **FAIL** | no new flipped faces (49 (47 in crease)); zone volume within ±5% (-24.5%) | diagnostic weights / linear-blend skinning: crease-zone collapse at large angle (the same weights with dual-quaternion preserve-volume reduce the zone volume change from -24.5% to +1.9%; flips / contact remain where tissue must meet) |
| D6_l_abd30 | PASS | — | — |
| D1_r_abd45 | PASS | — | — |
| D1_r_abd90 | **FAIL** | no new flipped faces (9 (9 in crease)); zone volume within ±5% (-13.4%); joint-loop spacing >= 50% of rest (0.28) | diagnostic weights / linear-blend skinning: crease-zone collapse at large angle (the same weights with dual-quaternion preserve-volume reduce the zone volume change from -13.4% to +3.1%; flips / contact remain where tissue must meet) |
| D1_r_flex90 | **FAIL** | no new flipped faces (259 (175 in crease)); zone volume within ±5% (-30.6%); joint-loop spacing >= 50% of rest (0.35); crease contact depth <= 2 mm (14.3 mm) | diagnostic weights / linear-blend skinning: crease-zone collapse at large angle (the same weights with dual-quaternion preserve-volume reduce the zone volume change from -30.6% to -14.1%; flips / contact remain where tissue must meet) |
| D1_r_ext30 | PASS | — | — |
| D6_r_flex45 | **FAIL** | no new flipped faces (8 (6 in crease)); zone volume within ±5% (-6.8%) | diagnostic weights / linear-blend skinning: crease-zone compression at large angle (flips, crease interpenetration, loop compression confined to the crease zone) |
| D6_r_flex90 | **FAIL** | no new flipped faces (48 (46 in crease)); no new folds outside crease/contact zones (+39 (outside 3)); zone volume within ±5% (-24.5%) | diagnostic weights / linear-blend skinning: crease-zone collapse at large angle (the same weights with dual-quaternion preserve-volume reduce the zone volume change from -24.5% to +1.5%; flips / contact remain where tissue must meet) / diagnostic weights: fold outside the crease radius adjacent to the crease (see sheet) |
| D6_r_abd30 | PASS | — | — |
| D2_l_flex90 | **FAIL** | no new flipped faces (135 (135 in crease)); zone volume within ±3% (-16.5%); joint-loop spacing >= 50% of rest (0.32); crease contact depth <= 2 mm (4.2 mm) | diagnostic weights / linear-blend skinning: crease-zone collapse at large angle (the same weights with dual-quaternion preserve-volume reduce the zone volume change from -16.5% to +1.2%; flips / contact remain where tissue must meet) |
| D2_l_flex130 | **FAIL** | 0 non-contact intersections (173); no new flipped faces (211 (211 in crease)); zone volume within ±3% (-27.9%); joint-loop spacing >= 50% of rest (0.20); crease contact depth <= 2 mm (5.3 mm) | source-contact anatomy: forearm mass against the upper-arm mass in deep (130 deg) flexion — undeclared in v001, analogous to the declared calf–thigh contact / diagnostic weights / linear-blend skinning: crease-zone collapse at large angle (the same weights with dual-quaternion preserve-volume reduce the zone volume change from -27.9% to +1.7%; flips / contact remain where tissue must meet) |
| D3_l_flex60 | **FAIL** | no new flipped faces (9 (9 in crease)); zone volume within ±5% (-5.9%); joint-loop spacing >= 50% of rest (0.45) | diagnostic weights / linear-blend skinning: crease-zone compression at large angle (flips, crease interpenetration, loop compression confined to the crease zone) |
| D3_l_ext60 | **FAIL** | no new flipped faces (6 (6 in crease)); zone volume within ±5% (-9.3%); joint-loop spacing >= 50% of rest (0.42) | diagnostic weights / linear-blend skinning: crease-zone compression at large angle (flips, crease interpenetration, loop compression confined to the crease zone) |
| D3_l_radial20 | PASS | — | — |
| D3_l_ulnar20 | PASS | — | — |
| D4_l_fist | **FAIL** | 0 non-contact intersections (2); no new flipped faces (194 (194 in crease)); zone volume within ±5% (-17.2%); joint-loop spacing >= 50% of rest (0.26); crease contact depth <= 2 mm (4.7 mm); nail rigidity <= 0.3 mm (0.71 mm) | crease-adjacent self contact just outside the 2.6 cm crease radius (pad region) — diagnostic weights / diagnostic weights / linear-blend skinning: crease-zone collapse at large angle (the same weights with dual-quaternion preserve-volume reduce the zone volume change from -17.2% to -2.3%; flips / contact remain where tissue must meet) / diagnostic weights: the distal phalanx / nail cap is shared between the middle and distal phalanx bones (heat weights), so the nail bends with the DIP; production weights would bind the nail rigidly to the distal bone |
| D4_l_spread_p10 | PASS | — | — |
| D4_l_spread_m10 | PASS | — | — |
| D5_l_oppose_pinky | **FAIL** | 0 non-contact intersections (4); no new flipped faces (235 (176 in crease)); no new folds outside crease/contact zones (+8 (outside 3)); crease contact depth <= 2 mm (8.9 mm) | palm / thenar or index self-fold contact just outside the 3.5 cm crease radius during opposition — diagnostic weights (thenar crease) / diagnostic weights / linear-blend skinning: crease-zone compression at large angle (flips, crease interpenetration, loop compression confined to the crease zone) / diagnostic weights: fold outside the crease radius adjacent to the crease (see sheet) |
| D5_l_oppose_pinch | **FAIL** | no new flipped faces (9 (9 in crease)); joint-loop spacing >= 50% of rest (0.46); nail rigidity <= 0.3 mm (0.44 mm) | diagnostic weights / linear-blend skinning: crease-zone compression at large angle (flips, crease interpenetration, loop compression confined to the crease zone) / diagnostic weights: the distal phalanx / nail cap is shared between the middle and distal phalanx bones (heat weights), so the nail bends with the DIP; production weights would bind the nail rigidly to the distal bone |
| D7_l_flex90 | **FAIL** | no new flipped faces (192 (192 in crease)); zone volume within ±5% (-25.0%); joint-loop spacing >= 50% of rest (0.18); crease contact depth <= 2 mm (6.9 mm) | diagnostic weights / linear-blend skinning: crease-zone collapse at large angle (the same weights with dual-quaternion preserve-volume reduce the zone volume change from -25.0% to -0.3%; flips / contact remain where tissue must meet) |
| D7_l_flex140 | **FAIL** | no new flipped faces (283 (283 in crease)); zone volume within ±5% (-44.2%); joint-loop spacing >= 50% of rest (0.30) | diagnostic weights / linear-blend skinning: crease-zone collapse at large angle (the same weights with dual-quaternion preserve-volume reduce the zone volume change from -44.2% to -1.0%; flips / contact remain where tissue must meet) |
| D8_l_dorsi20 | PASS | — | — |
| D8_l_plantar40 | PASS | — | — |
| D8_l_toes_ext30 | PASS | — | — |
| D8_l_toes_flex30 | PASS | — | — |
| D2_l_base_abd45 | PASS | — | — |
| D1_l_abd90_girdle | **FAIL** | joint-loop spacing >= 50% of rest (0.24) | diagnostic weights / linear-blend skinning: crease-zone compression at large angle (flips, crease interpenetration, loop compression confined to the crease zone) |
| D1_l_flex90_girdle | **FAIL** | no new flipped faces (195 (140 in crease)); zone volume within ±5% (-27.5%); joint-loop spacing >= 50% of rest (0.26); crease contact depth <= 2 mm (12.8 mm) | diagnostic weights / linear-blend skinning: crease-zone compression at large angle (flips, crease interpenetration, loop compression confined to the crease zone) |
| D1_r_abd90_girdle | **FAIL** | zone volume within ±5% (-5.5%); joint-loop spacing >= 50% of rest (0.41) | diagnostic weights / linear-blend skinning: crease-zone compression at large angle (flips, crease interpenetration, loop compression confined to the crease zone) |
| D1_r_flex90_girdle | **FAIL** | no new flipped faces (86 (57 in crease)); zone volume within ±5% (-22.8%); joint-loop spacing >= 50% of rest (0.46); crease contact depth <= 2 mm (9.7 mm) | diagnostic weights / linear-blend skinning: crease-zone compression at large angle (flips, crease interpenetration, loop compression confined to the crease zone) |
| D9_twist_p30 | PASS | — | — |
| D9_twist_m30 | **FAIL** | 0 non-contact intersections (2) | diagnostic weights: axillary arm–arm contact dragged by the trunk rotation |
| D9_flex30 | **FAIL** | 0 non-contact intersections (2) | diagnostic weights: axillary arm–arm contact dragged by the trunk rotation |
| D10_flex30 | PASS | — | — |
| D10_ext30 | PASS | — | — |
| D10_rot_p45 | PASS | — | — |
| D10_rot_m45 | PASS | — | — |


### 5.2 Preserve-volume (dual-quaternion) comparison, same weights

```
D1_l_abd90         int   27 (nc 0, crease 27 / 2.9mm, contact 0) folds+7 out 0 flips 35 vol +6.16% zone +9.9% strain p95 66.8% loop 0.12
D1_l_flex90        int  143 (nc 44, crease 46 / 16.3mm, contact 53) folds+7 out 4 flips 376 vol -1.82% zone -23.3% strain p95 78.3% loop 0.24
D6_l_flex90        int    8 (nc 7, crease 1 / 4.6mm, contact 0) folds+68 out 42 flips 45 vol +2.15% zone +1.9% strain p95 92.4% loop 0.68
D1_r_abd90         int    0 (nc 0, crease 0 / 0.0mm, contact 0) folds+0 out 0 flips 0 vol +6.01% zone +3.1% strain p95 59.5% loop 0.35
D1_r_flex90        int   69 (nc 0, crease 32 / 12.6mm, contact 37) folds+1 out 0 flips 255 vol -0.72% zone -14.1% strain p95 79.2% loop 0.48
D6_r_flex90        int   29 (nc 6, crease 2 / 10.3mm, contact 21) folds+81 out 45 flips 49 vol +2.14% zone +1.5% strain p95 91.8% loop 0.71
D2_l_flex90        int  100 (nc 0, crease 100 / 3.3mm, contact 0) folds+10 out 0 flips 125 vol +2.82% zone +1.2% strain p95 62.4% loop 0.39
D2_l_flex130       int  276 (nc 173, crease 103 / 4.8mm, contact 0) folds+3 out 0 flips 257 vol +2.82% zone +1.7% strain p95 69.9% loop 0.20
D4_l_fist          int 1024 (nc 3, crease 622 / 4.6mm, contact 399) folds+28 out 0 flips 177 vol +2.77% zone -2.3% strain p95 53.3% loop 0.31
D7_l_flex90        int   95 (nc 0, crease 95 / 5.6mm, contact 0) folds+6 out 0 flips 163 vol -0.12% zone -0.3% strain p95 86.3% loop 0.10
D7_l_flex140       int  224 (nc 0, crease 0 / 0.0mm, contact 224) folds+5 out 0 flips 369 vol -0.17% zone -1.0% strain p95 134.0% loop 0.22
```

### 5.3 Joint-placement comparison (shoulder and pelvis), same weights, pivot only

| alternative pivot | pose | int (nc) | crease depth mm | flips | folds outside | zone vol % | strain p95 % | loop | v002 int (nc) / depth / flips / folds out / zone / p95 / loop |
|---|---|---|---|---|---|---|---|---|---|
| inguinalA_hip_l | D6_l_flex90 | 0 (0) | 0.0 | 15 | 8 | -0.4 | 95 | 0.78 | 43 (0) / 1.8 / 49 / 0 / -24.5 / 70 / 0.80 |
| inguinalA_hip_l | D6_l_abd30 | 0 (0) | 0.0 | 0 | 0 | -5.6 | 35 | 0.99 | 0 (0) / 0.0 / 0 / 0 / -1.2 / 40 / 1.00 |
| inguinalA_hip_r | D6_r_flex90 | 0 (0) | 0.0 | 17 | 10 | -1.8 | 93 | 0.80 | 43 (0) / 1.7 / 48 / 3 / -24.5 / 69 / 0.85 |
| inguinalA_hip_r | D6_r_abd30 | 0 (0) | 0.0 | 0 | 0 | -6.1 | 36 | 0.99 | 0 (0) / 0.0 / 0 / 0 / -1.5 / 42 / 0.99 |
| oldE3_gh_l | D1_l_abd90 | 3 (0) | 0.3 | 19 | 0 | -10.5 | 62 | 0.15 | 49 (0) / 4.5 / 49 / 0 / -6.6 / 54 / 0.23 |
| oldE3_gh_l | D1_l_flex90 | 176 (53) | 20.8 | 382 | 8 | -40.8 | 68 | 0.30 | 198 (38) / 16.6 / 359 / 10 / -33.9 / 62 / 0.19 |
| oldE3_gh_r | D1_r_abd90 | 0 (0) | 0.0 | 0 | 0 | -17.6 | 61 | 0.41 | 19 (0) / 1.0 / 9 / 0 / -13.4 / 58 / 0.28 |
| oldE3_gh_r | D1_r_flex90 | 84 (15) | 12.8 | 404 | 1 | -54.0 | 71 | 0.28 | 100 (0) / 14.3 / 259 / 0 / -30.6 / 66 / 0.35 |
| oldE3_hip_l | D6_l_flex90 | 184 (18) | 6.9 | 348 | 18 | -52.9 | 66 | 0.93 | 43 (0) / 1.8 / 49 / 0 / -24.5 / 70 / 0.80 |
| oldE3_hip_l | D6_l_abd30 | 0 (0) | 0.0 | 0 | 0 | 2.2 | 48 | 1.00 | 0 (0) / 0.0 / 0 / 0 / -1.2 / 40 / 1.00 |
| oldE3_hip_r | D6_r_flex90 | 179 (15) | 7.7 | 348 | 16 | -51.6 | 66 | 0.84 | 43 (0) / 1.7 / 48 / 3 / -24.5 / 69 / 0.85 |
| oldE3_hip_r | D6_r_abd30 | 0 (0) | 0.0 | 0 | 0 | 2.0 | 49 | 1.00 | 0 (0) / 0.0 / 0 / 0 / -1.5 / 42 / 0.99 |
| v001cons_gh_l | D1_l_abd90 | 107 (0) | 8.2 | 203 | 0 | 6.1 | 52 | 0.40 | 49 (0) / 4.5 / 49 / 0 / -6.6 / 54 / 0.23 |
| v001cons_gh_l | D1_l_flex90 | 174 (34) | 15.3 | 224 | 6 | 25.7 | 74 | 0.39 | 198 (38) / 16.6 / 359 / 10 / -33.9 / 62 / 0.19 |
| v001cons_gh_r | D1_r_abd90 | 109 (0) | 6.4 | 285 | 0 | -8.6 | 57 | 0.13 | 19 (0) / 1.0 / 9 / 0 / -13.4 / 58 / 0.28 |
| v001cons_gh_r | D1_r_flex90 | 39 (0) | 1.9 | 133 | 1 | 23.0 | 75 | 0.59 | 100 (0) / 14.3 / 259 / 0 / -30.6 / 66 / 0.35 |
| v001sphereA_gh_l | D1_l_abd90 | 107 (0) | 8.9 | 223 | 0 | 6.2 | 52 | 0.38 | 49 (0) / 4.5 / 49 / 0 / -6.6 / 54 / 0.23 |
| v001sphereA_gh_l | D1_l_flex90 | 174 (35) | 15.0 | 226 | 6 | 28.5 | 74 | 0.38 | 198 (38) / 16.6 / 359 / 10 / -33.9 / 62 / 0.19 |
| v001sphereA_gh_r | D1_r_abd90 | 150 (0) | 10.9 | 424 | 0 | -9.4 | 59 | 0.22 | 19 (0) / 1.0 / 9 / 0 / -13.4 / 58 / 0.28 |
| v001sphereA_gh_r | D1_r_flex90 | 35 (2) | 1.9 | 130 | 1 | 50.4 | 80 | 0.62 | 100 (0) / 14.3 / 259 / 0 / -30.6 / 66 / 0.35 |


**Reading of the comparison:**
- **The old frozen E3 hip is mechanically untenable**, which confirms the AD-R1 rejection. At 90° hip flexion it gives 184 intersections (18 non-contact), 348 flips and −53 % zone volume, against 43 (0), 49 and −24.5 % for v002.
- **The v002 GH centre beats the rejected v001 sphere / consensus centres in 90° abduction:**

  | Pivot | Intersections (L / R) | Flips (L / R) |
  |---|---|---|
  | v002 | 49 / 19 | 49 / 9 |
  | v001 sphere / consensus | 107–150 | 203–424 |

- **The old E3 GH is mixed.** It has fewer abduction crease contacts than v002 (3 / 0 against 49 / 19). In 90° flexion it is worse: 53 / 15 non-contact intersections against 38 / 0 for v002, and 382 / 404 flips against 359 / 259.
- **Shoulder flexion 90° fails for every pivot.** With the v002 pivot, the girdle-assisted variant removes all non-contact intersections.
- **Placement finding for the author:** the inguinal-axis hip (alternative A, which AD-R1 excluded as a sole choice) gives 0 intersections and about −1 % zone volume at 90° flexion, against 43 and −24.5 % for v002. Its cost is 8–10 folds outside the crease and a higher p95 strain (93–95 %).

## 6. Bounded landmark revision

**Not used.** No v003 landmark revision was needed: no v002 placement is mechanically untenable. Every v002 pose has 0 non-contact intersections except the classified cases, and the alternatives are not uniformly better.

**Hip finding (§5.3):** the hip result is reported, not applied, because moving the hip toward the inguinal axis would exceed the AD-R1 5 mm bound.

**Knee interpretation to confirm:** AD-R2's "max 5 mm adjustment" was read as applying to the *level*. The AP/ML placement is the section centroid as ruled, which lies 0.78 / 0.58 cm from the v001 xy. If the cap was meant for AP/ML as well, that is a one-line revision.

## 7. Topology vs rig / weights / placement

**No result indicates a topology defect.**
- **Small and moderate poses are clean.** These include:
  - abduction to 45°, extension 30°;
  - wrist radial / ulnar deviation 20°, finger spread ±10°;
  - hip abduction 30°;
  - all ankle and toe poses;
  - trunk twist +30°;
  - every neck pose.
- **The failures sit in the crease zones at ≥ 60–90°.** They are flips, crease interpenetration, joint-loop compression and zone volume loss.
- **Those failures follow the skinning method, not the mesh.** With the same weights and topology, dual-quaternion skinning removes most of the volume loss:

  | Pose | Zone volume, LBS | Zone volume, DQS |
  |---|---|---|
  | elbow 90° | −16.5 % | +1.2 % |
  | knee 90° | −25.0 % | −0.3 % |
  | knee 140° | −44.2 % | −1.0 % |
  | hip 90° | −24.5 % | +1.9 % / +1.5 % |

  At the hip, DQS adds 42–45 folds outside the crease.

- **What remains under DQS** is compression and contact on the inner crease side, which tissue must undergo at these angles. Fixing it needs production-quality weights and corrective shapes, not topology changes.
- **Non-contact intersections are explained by setup or contact anatomy:**
  - shoulder flexion without girdle participation (0 with the girdle variant);
  - forearm–upper-arm mass contact at 130° elbow flexion (undeclared contact anatomy);
  - 2–4 axillary / palm self-contacts.
- **The nail failure (0.44–0.71 mm against 0.3 mm) is a weights problem.** Heat weights share the distal phalanx between two bones.
- **Verdict:** the accepted v003 topology is not shown to be inadequate. The diagnostic weights and plain LBS are. Equally, nothing here proves production deformation quality.

## 8. Visual evidence

**Diagnostic landmark sheets** (`landmark_sheets/`):

| Sheet | Content |
|---|---|
| `V0` | Whole-body diagnostic skeleton |
| `V1` | Shoulder girdle: acromion, inferior proxy, medial proxy, SC, GH, against the rejected alternatives |
| `V2` | Thoracic chain |
| `V3` | Pelvis / hip / root |
| `V4_l/r` | Hand chains |

**D1–D10 sheets** (`diag_sheets/`, `D1_l` … `D10`):
- each shows the reference row plus every pose, three identical cameras, clay + wire;
- metrics are printed beside each row, with DQS numbers where measured.

**Placement comparison sheets:** `S_shoulder_l_abd90`, `S_shoulder_l_flex90`, `S_shoulder_r_abd90`, `S_pelvis_l_flex90`, `S_pelvis_r_flex90`. The pelvis sheets hide that side's arm so the hip is unobstructed; this is disclosed on the sheet.

**Raw data:** `diag/diag_results*.json`, `judgement.json`, `summary_*.txt`.

## 9. Decisions needed from ChatGPT

1. **Topology:** accept the diagnostic conclusion that the v003 topology is not the limiting factor. The failures are weights / LBS / contact.
2. **Hip pivot:** keep the v002 hip, or authorise moving toward the inguinal-axis hip (beyond the 5 mm AD-R1 bound) in a bounded landmark revision.
3. **Contact anatomy:** declare the forearm–upper-arm contact at deep elbow flexion as contact anatomy, alongside calf–thigh and belly–thigh.
4. **Shoulder elevation:** confirm that shoulder elevation above 45° is evaluated with girdle participation (scapulohumeral rhythm), not pure GH rotation.
5. **Next stage:** the next authorised stage should address skinning (weight authoring strategy, DQS / hybrid, corrective-shape policy for ≥ 90° flexion, rigid nail binding) together with the deferred facial / oral component stage (jaw, eyes), before any final skeleton or UE5 work.
6. **Knee:** confirm the AD-R2 knee AP/ML interpretation (§6).

**STOP FOR CHATGPT REVIEW.**
