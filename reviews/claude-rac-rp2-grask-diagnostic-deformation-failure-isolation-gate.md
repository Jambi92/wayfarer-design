# RAC RP2 — Grask diagnostic deformation failure isolation — gate

**Date:** 2026-10-26  
**Order:** `reviews/chatgpt-rac-rp2-grask-diagnostic-deformation-failure-isolation-order.md` (8918cea)  
**Reviewed return:** 2a0df3c  
**State:** **retopology frozen; diagnostic deformation follow-up awaiting review.**

This was one bounded diagnostic cycle on new derived copies. It changed:
- no geometry, rest shape or skeleton architecture;
- no corrective shapes or helper bones;
- no production rig or weights;
- no facial work, UE5 work or other race.

The previous gate (`claude-rac-rp2-grask-rig-landmark-adjudication-diagnostic-gate.md`) is preserved as history. **Its categorical statement "no result indicates a topology defect" is withdrawn** and replaced by §8 here.

**Evidence:** `reviews/rac-rp2-evidence/grask_rig_diagnostic_v002/`  
**Tools:** `tools/rac/rp/grask_rigprep_v001/`

| Step | Script |
|---|---|
| Landmarks | `lm_v003.py` |
| Weights | `weights_dev.py` |
| Rig | `rig_build.py` (with `WEIGHTS_NPZ`) |
| Runs | `run_iso.sh` (select / full / alt / dqs) |
| Judgement | `iso_judge.py` |
| Metric checks | `metric_check.py` |
| Sheets | `iso_sheets.py`, `render_attr.py` |

---

## 1. Integrity

Parents were re-staged fresh from the PC before and after the work (`hashes/`). All are unchanged:

| File | SHA-256 | Geometry |
|---|---|---|
| v003 | `03bfe7d9…` | `f9c4a7ac…` |
| v005 | `7bba8d2d…` | `2697929d…` |
| v001 / v002 / sidecars / landmarks / freeze record | unchanged | |
| diagnostic `rigdiag_v001.blend` | `59ca4fda…` | untouched |

**New file:** `GR_U_REF_RP2_rigdiag_v002.blend`
- SHA-256 `9e2d078ac496a5194b0836d922608a74bcdf3919e964f837ccf88d5924caacdf`
- on the PC at `E:/…/Grask/RP2/DIAG/`
- **rest geometry read back from the PC copy: `f9c4a7ac…`**, identical to frozen v003
- weights read back from the file are bit-equal to the W2 array
- Blender armature = numpy LBS within 0.0007 mm; rest-return 0.0002 mm; bone lengths = landmark segments within 0.0001 mm
- manifest: `rig/GR_U_REF_RP2_rigdiag_v002_manifest.json`

## 2. AD-R2 resolved: `GR_U_REF_RP2_rigprep_landmarks_v003.json`

This is the one authorised landmark revision.
- **What changed:** each knee is placed at the consensus level, as close as possible to the horizontal leg-section centroid, with the **total** displacement from the exact v001 consensus capped at 5.0 mm.
- **The two requirements conflict.** The knee therefore cannot sit on the section centre. The residual to the centre is **2.75 mm (L) / 0.83 mm (R)**.
- **Status:** the bounded knee is an experimental candidate pending review.
- **The former unrestricted v002 knee** (7.8 / 5.8 mm displacement) is kept only as a labelled comparison and is **not approved**.

**Full displacement audit** (`landmarks/displacement_compliance_v003.md`):

| id | reference | reference (prod cm) | chosen (prod cm) | displacement (cm) | norm cm | cap cm | compliant | residual to section centre cm |
|---|---|---|---|---|---|---|---|---|
| hip_l | v001 consensus (AD-R1, cap 5 mm) | [12.108, 2.847, 119.027] | [12.025, 3.333, 118.942] | [-0.0823, 0.4857, -0.0854] | 0.5 | 0.5 | yes | — |
| knee_l | v001 consensus (AD-R2, cap 5 mm total) | [13.658, 1.005, 71.166] | [13.834, 0.537, 71.166] | [0.1762, -0.4679, 0.0] | 0.5 | 0.5 | yes | 0.2752 |
| elbow_l | v001 cubital target (AD-R4, cap 5 mm) | [26.059, -2.621, 142.772] | [26.317, -2.503, 142.772] | [0.2581, 0.1177, 0.0] | 0.2836 | 0.5 | yes | — |
| ankle_l | v001 consensus level (AD-R2: section-centreline placement, no cap stated) — disclosed | [15.528, 0.232, 13.5] | [15.528, 1.333, 13.5] | [0.0, 1.1014, 0.0] | 1.1014 | — | — | — |
| hip_r | v001 consensus (AD-R1, cap 5 mm) | [-12.111, 2.758, 119.157] | [-12.039, 3.248, 119.09] | [0.0721, 0.4902, -0.067] | 0.5 | 0.5 | yes | — |
| knee_r | v001 consensus (AD-R2, cap 5 mm total) | [-13.159, 1.253, 71.197] | [-13.442, 0.841, 71.197] | [-0.2827, -0.4124, 0.0] | 0.5 | 0.5 | yes | 0.0826 |
| elbow_r | v001 cubital target (AD-R4, cap 5 mm) | [-26.82, -2.875, 142.987] | [-26.945, -2.927, 142.987] | [-0.1246, -0.052, 0.0] | 0.1351 | 0.5 | yes | — |
| ankle_r | v001 consensus level (AD-R2: section-centreline placement, no cap stated) — disclosed | [-15.496, -1.105, 13.75] | [-15.608, -0.123, 13.75] | [-0.1124, 0.9829, 0.0] | 0.9893 | — | — | — |
| pelvis | v001 pelvis proposal (AD-R7, cap 5 mm) | [0.0, 2.802, 123.928] | [0.009, 3.302, 123.928] | [0.0089, 0.4999, 0.0] | 0.5 | 0.5 | yes | — |
| glenohumeral_l | rule-based (AD-R3; no displacement cap) | — | [21.049, -4.704, 175.718] | — | — | — | — | — |
| sternoclavicular_l | rule-based (AD-R5; exactly 3.0 cm posterior) | — | [3.582, 8.35, 178.268] | — | — | — | — | — |
| glenohumeral_r | rule-based (AD-R3; no displacement cap) | — | [-22.747, -1.28, 174.035] | — | — | — | — | — |
| sternoclavicular_r | rule-based (AD-R5; exactly 3.0 cm posterior) | — | [-2.426, 8.346, 178.366] | — | — | — | — | — |


**Other disclosure:** the AD-R2 ankle placement (section centreline, no cap stated) is **11.0 / 9.9 mm** from the v001 xy. It would exceed a 5 mm cap if one were intended. GH and SC are rule-based placements without a cap.

## 3. Weight work: baseline and two candidates

**Baseline W0:** the v001 array (bone heat plus the midline cleanup), SHA-256 `2189375b…df2e`. Every run records its weight-array hash (`weights_sha256` in each result).

**Candidates W1 and W2** (`weights_dev.py`). Both are local only, in the shoulder/axilla, elbow, wrist, hand/thumb/fingers, hip/groin and knee regions, and both change 38,264 vertices:

1. **Leakage removal:** a limb vertex keeps only weights from its own chain plus the girdle / pelvis roots.
2. **Smooth joint transitions:** within the joint region, the parent/child split becomes a smoothstep of the signed axial distance. The half-width is K × the local limb radius: **K = 0.6 for W1, K = 1.0 for W2**.
3. **Smoothing:** three Laplacian passes inside the edited regions, then normalisation of edited vertices only. All other vertices stay bit-identical.
4. **Nail binding:** 102–122 nail-cap vertices per digit are bound to the distal bone. The selection is the distal-phalanx dorsal cap: 0.35·L3 to L3 + 0.5 cm, radius < 1.6 cm, dorsal offset > 0.6 × the median radius.

The changed vertex ID lists and logs are in `weights/`. The before/after maps are in `sheets/W_weight_maps.jpg`.

**Selection** (16 difficult poses, same v002 pivots):

| Candidate | Failing criteria |
|---|---|
| W0 | 60 |
| W1 | 63 |
| W2 | 63 |

**W2 was chosen over W1** because it had fewer intersections and orientation failures in most poses. For example:
- D1_l_abd90: 55 intersections against 82 for W1;
- D3: 0 against 55;
- D4 fist: 1479 against 1718;
- D7 flex 90: 116 against 147.

**W2 is selected only as the better of the two candidates.** It is **not better than the baseline.**

**Full 43-pose suite, same pivots:**

| Weights | Poses passing |
|---|---|
| **W0** | **20 / 43** |
| **W2** | **12 / 43** |

W2 regresses 20 poses. Every regression is listed in §4.

**What W2 does improve:**
- nail rigidity: 0.44–0.71 mm → 0.00 mm, passing;
- wrist 60° intersections and orientation failures: 6–9 → 0;
- a few volume-proxy values.

**Why W2 regresses:** the weight maps show the mechanism. Editing only inside fixed regions leaves **weight discontinuities at the region boundaries**: a jagged upper-arm edge at the shoulder, a band across the thigh, patches at the hand. The axial-projection transitions are also narrower than the heat weights at the shoulder and hip, which raises crease penetration. For example, hip flexion 90° goes from 1.8 mm with W0 to 20.6 mm with W2.

**Conclusion on weights:** this cycle **did not produce a better diagnostic weight set than the baseline.** The only clearly supported change is the **nail binding**. A "baseline + nail binding only" candidate would be the natural next test, but it would be a third candidate, which this order does not allow. That is decision **D-3**.

## 4. Full-suite before / after (W0 → W2, v002 pivots; regressions in bold)

| pose | W0 | W2 | W0 nc / crease(mm) / folds-out / orient / inv / zone % / p95 / loop / nail | W2 same | newly failing criteria (REGRESSION) | criteria fixed |
|---|---|---|---|---|---|---|
| D1_l_abd45 | PASS | PASS | 0 / 0(0.0) / 0 / 0 / 0 / 0.9 / 28 / 0.54 / None | 0 / 0(0.0) / 0 / 0 / 0 / 2.1 / 32 / 0.53 / None | — | — |
| D1_l_abd90 | fail | fail | 0 / 49(4.5) / 0 / 49 / 0 / -6.6 / 54 / 0.23 / None | 0 / 55(5.3) / 0 / 84 / 5 / -4.0 / 57 / 0.24 / None | — | zone volume within ±5% |
| D1_l_flex90 | fail | fail | 38 / 71(16.6) / 10 / 359 / 0 / -33.9 / 62 / 0.19 / None | 94 / 147(16.6) / 31 / 414 / 32 / -35.6 / 65 / 0.32 / None | — | — |
| D1_l_ext30 | PASS | fail | 0 / 0(0.0) / 0 / 0 / 0 / 4.7 / 33 / 0.83 / None | 0 / 0(0.0) / 4 / 9 / 3 / 5.9 / 38 / 0.82 / None | **no new flipped faces; no new folds outside crease/contact zones; zone volume within ±5%** | — |
| D6_l_flex45 | fail | fail | 0 / 1(1.0) / 1 / 7 / 7 / -6.6 / 41 / 0.79 / None | 0 / 25(2.8) / 7 / 30 / 20 / -6.9 / 54 / 0.88 / None | **crease contact depth <= 2 mm** | — |
| D6_l_flex90 | fail | fail | 0 / 13(1.8) / 0 / 49 / 10 / -24.5 / 70 / 0.8 / None | 0 / 220(20.6) / 9 / 104 / 18 / -24.4 / 89 / 0.88 / None | **crease contact depth <= 2 mm; no new folds outside crease/contact zones** | — |
| D6_l_abd30 | PASS | fail | 0 / 0(0.0) / 0 / 0 / 0 / -1.2 / 40 / 1.0 / None | 0 / 0(0.0) / 2 / 5 / 1 / 1.4 / 41 / 0.93 / None | **no new flipped faces; no new folds outside crease/contact zones** | — |
| D1_r_abd45 | PASS | fail | 0 / 0(0.0) / 0 / 0 / 0 / -2.4 / 29 / 0.62 / None | 0 / 0(0.0) / 0 / 0 / 0 / -0.3 / 36 / 0.46 / None | **joint-loop spacing >= 50% of rest** | — |
| D1_r_abd90 | fail | fail | 0 / 19(1.0) / 0 / 9 / 0 / -13.4 / 58 / 0.28 / None | 0 / 76(6.4) / 0 / 130 / 1 / -8.1 / 58 / 0.32 / None | **crease contact depth <= 2 mm** | — |
| D1_r_flex90 | fail | fail | 0 / 64(14.3) / 0 / 259 / 0 / -30.6 / 66 / 0.35 / None | 17 / 160(19.9) / 8 / 355 / 21 / -31.9 / 68 / 0.34 / None | **0 non-contact intersections; no new folds outside crease/contact zones** | — |
| D1_r_ext30 | PASS | fail | 0 / 0(0.0) / 0 / 0 / 0 / 1.4 / 28 / 0.76 / None | 1 / 0(0.0) / 5 / 10 / 4 / 3.0 / 34 / 0.82 / None | **0 non-contact intersections; no new flipped faces; no new folds outside crease/contact zones** | — |
| D6_r_flex45 | fail | fail | 0 / 2(1.3) / 0 / 8 / 7 / -6.8 / 41 / 0.81 / None | 0 / 39(5.5) / 10 / 31 / 13 / -6.7 / 52 / 0.89 / None | **crease contact depth <= 2 mm; no new folds outside crease/contact zones** | — |
| D6_r_flex90 | fail | fail | 0 / 15(1.7) / 3 / 48 / 10 / -24.5 / 69 / 0.85 / None | 0 / 209(15.2) / 12 / 104 / 23 / -23.6 / 89 / 0.87 / None | **crease contact depth <= 2 mm** | — |
| D6_r_abd30 | PASS | fail | 0 / 0(0.0) / 0 / 0 / 0 / -1.5 / 42 / 0.99 / None | 0 / 0(0.0) / 0 / 1 / 0 / -1.3 / 39 / 0.93 / None | **no new flipped faces** | — |
| D2_l_flex90 | fail | fail | 0 / 116(4.2) / 0 / 135 / 0 / -16.5 / 44 / 0.32 / None | 0 / 135(6.5) / 0 / 206 / 21 / -11.5 / 63 / 0.3 / None | — | — |
| D2_l_flex130 | fail | fail | 173 / 112(5.3) / 0 / 211 / 0 / -27.9 / 43 / 0.2 / None | 173 / 127(7.7) / 0 / 316 / 33 / -19.4 / 63 / 0.19 / None | — | — |
| D3_l_flex60 | fail | fail | 0 / 0(0.0) / 0 / 9 / 0 / -5.9 / 34 / 0.45 / None | 0 / 0(0.0) / 0 / 0 / 0 / -5.2 / 47 / 0.46 / None | — | no new flipped faces |
| D3_l_ext60 | fail | fail | 0 / 0(0.0) / 0 / 6 / 0 / -9.3 / 35 / 0.42 / None | 0 / 0(0.0) / 0 / 0 / 0 / -6.4 / 46 / 0.44 / None | — | no new flipped faces |
| D3_l_radial20 | PASS | PASS | 0 / 0(0.0) / 0 / 0 / 0 / -0.6 / 14 / 0.76 / None | 0 / 0(0.0) / 0 / 0 / 0 / -0.8 / 20 / 0.81 / None | — | — |
| D3_l_ulnar20 | PASS | PASS | 0 / 0(0.0) / 0 / 0 / 0 / -1.3 / 14 / 0.76 / None | 0 / 0(0.0) / 0 / 0 / 0 / -0.7 / 19 / 0.68 / None | — | — |
| D4_l_fist | fail | fail | 2 / 668(4.7) / 0 / 194 / 14 / -17.2 / 41 / 0.26 / 0.71 | 2 / 785(18.1) / 0 / 329 / 50 / -21.3 / 57 / 0.05 / 0.0 | — | nail rigidity <= 0.3 mm |
| D4_l_spread_p10 | PASS | PASS | 0 / 0(0.0) / 0 / 0 / 0 / 0.1 / 5 / 0.87 / 0.0 | 0 / 0(0.0) / 0 / 0 / 0 / 0.6 / 6 / 0.66 / 0.0 | — | — |
| D4_l_spread_m10 | PASS | fail | 0 / 0(0.0) / 0 / 0 / 0 / -0.5 / 4 / 0.85 / 0.0 | 0 / 0(0.0) / 0 / 11 / 1 / -1.0 / 6 / 0.68 / 0.0 | **no new flipped faces** | — |
| D5_l_oppose_pinky | fail | fail | 4 / 181(8.9) / 3 / 235 / 0 / -2.0 / 31 / 1.0 / 0.0 | 4 / 183(8.9) / 3 / 246 / 10 / -5.2 / 36 / 1.0 / 0.0 | — | — |
| D5_l_oppose_pinch | fail | fail | 0 / 29(0.9) / 0 / 9 / 1 / -4.4 / 38 / 0.46 / 0.44 | 0 / 21(4.7) / 0 / 49 / 15 / -5.3 / 47 / 0.33 / 0.0 | **crease contact depth <= 2 mm** | nail rigidity <= 0.3 mm |
| D7_l_flex90 | fail | fail | 0 / 116(6.9) / 0 / 192 / 2 / -25.0 / 63 / 0.18 / None | 0 / 116(13.4) / 0 / 271 / 10 / -19.5 / 80 / 0.24 / None | — | — |
| D7_l_flex140 | fail | fail | 0 / 0(0.0) / 0 / 283 / 1 / -44.2 / 59 / 0.3 / None | 0 / 0(0.0) / 0 / 349 / 23 / -35.2 / 83 / 0.35 / None | — | — |
| D8_l_dorsi20 | PASS | PASS | 0 / 0(0.0) / 0 / 0 / 0 / -2.4 / 6 / 0.58 / None | 0 / 0(0.0) / 0 / 0 / 0 / -2.4 / 6 / 0.58 / None | — | — |
| D8_l_plantar40 | PASS | PASS | 0 / 0(0.0) / 0 / 0 / 0 / -1.0 / 16 / 0.54 / None | 0 / 0(0.0) / 0 / 0 / 0 / -1.0 / 16 / 0.54 / None | — | — |
| D8_l_toes_ext30 | PASS | fail | 0 / 0(0.0) / 0 / 0 / 0 / -3.3 / 13 / 0.74 / None | 0 / 0(0.0) / 0 / 1 / 0 / -3.3 / 13 / 0.74 / None | **no new flipped faces** | — |
| D8_l_toes_flex30 | PASS | fail | 0 / 0(0.0) / 0 / 0 / 0 / 0.5 / 13 / 0.7 / None | 0 / 0(0.0) / 0 / 2 / 1 / 0.5 / 13 / 0.7 / None | **no new flipped faces** | — |
| D2_l_base_abd45 | PASS | PASS | 0 / 0(0.0) / 0 / 0 / 0 / 0.0 / 0 / 1.0 / None | 0 / 0(0.0) / 0 / 0 / 0 / 0.0 / 0 / 1.0 / None | — | — |
| D1_l_abd90_girdle | fail | fail | 0 / 0(0.0) / 0 / 0 / 0 / 0.3 / 50 / 0.24 / None | 0 / 0(0.0) / 0 / 2 / 0 / 2.4 / 56 / 0.29 / None | **no new flipped faces** | — |
| D1_l_flex90_girdle | fail | fail | 0 / 48(12.8) / 0 / 195 / 0 / -27.5 / 58 / 0.26 / None | 7 / 56(12.8) / 22 / 251 / 27 / -29.1 / 60 / 0.22 / None | **0 non-contact intersections; no new folds outside crease/contact zones** | — |
| D1_r_abd90_girdle | fail | fail | 0 / 0(0.0) / 0 / 0 / 0 / -5.5 / 49 / 0.41 / None | 0 / 25(0.7) / 0 / 22 / 0 / -1.6 / 58 / 0.18 / None | **no new flipped faces** | zone volume within ±5% |
| D1_r_flex90_girdle | fail | fail | 0 / 35(9.7) / 0 / 86 / 1 / -22.8 / 59 / 0.46 / None | 0 / 116(16.8) / 0 / 165 / 16 / -24.4 / 62 / 0.27 / None | — | — |
| D9_twist_p30 | PASS | fail | 0 / 0(0.0) / 0 / 0 / 0 / -0.5 / 4 / None / None | 2 / 0(0.0) / 2 / 5 / 1 / -0.5 / 4 / None / None | **0 non-contact intersections; no new flipped faces; no new folds outside crease/contact zones** | — |
| D9_twist_m30 | fail | fail | 2 / 0(0.0) / 0 / 0 / 0 / -0.2 / 4 / None / None | 2 / 0(0.0) / 6 / 5 / 2 / -0.2 / 4 / None / None | **no new flipped faces; no new folds outside crease/contact zones** | — |
| D9_flex30 | fail | PASS | 2 / 0(0.0) / 0 / 0 / 0 / 4.7 / 14 / None / None | 0 / 0(0.0) / 0 / 0 / 0 / 4.7 / 14 / None / None | — | 0 non-contact intersections |
| D10_flex30 | PASS | PASS | 0 / 0(0.0) / 0 / 0 / 0 / -2.3 / 16 / 0.7 / None | 0 / 0(0.0) / 0 / 0 / 0 / -2.3 / 16 / 0.7 / None | — | — |
| D10_ext30 | PASS | PASS | 0 / 0(0.0) / 0 / 0 / 0 / 0.9 / 16 / 0.86 / None | 0 / 0(0.0) / 0 / 0 / 0 / 0.9 / 16 / 0.86 / None | — | — |
| D10_rot_p45 | PASS | PASS | 0 / 0(0.0) / 0 / 0 / 0 / -3.5 / 15 / 0.79 / None | 0 / 0(0.0) / 0 / 0 / 0 / -3.5 / 15 / 0.79 / None | — | — |
| D10_rot_m45 | PASS | PASS | 0 / 0(0.0) / 0 / 0 / 0 / -3.6 / 15 / 0.79 / None | 0 / 0(0.0) / 0 / 0 / 0 / -3.6 / 15 / 0.79 / None | — | — |


## 5. Controlled comparisons

### 5.1 Alternate pivots (identical W2 array; same local angle definitions; world-space endpoints disclosed)

| alternative pivot (W2 weights) | pose | alt nc / crease(mm) / folds-out / orient / inv / zone % / p95 / loop | v002 pivot same | pass alt / v002 | world endpoints alt vs v002 (cm) |
|---|---|---|---|---|---|
| inguinalA_hip_l | D6_l_flex45 | 0 / 0(0.0) / 6 / 40 / 7 / 14.1 / 61 / 0.93 | 0 / 25(2.8) / 7 / 30 / 20 / -6.9 / 54 / 0.88 | f / f | shin_l [13.6, 28.3, 79.0] vs [13.5, 29.3, 83.0]; foot_l [14.4, 69.8, 39.0] vs [14.3, 70.8, 43.0] |
| inguinalA_hip_l | D6_l_flex90 | 5 / 8(5.1) / 19 / 67 / 21 / 2.4 / 111 / 0.86 | 0 / 220(20.6) / 9 / 104 / 18 / -24.4 / 89 / 0.88 | f / f | shin_l [12.4, 46.6, 108.4] vs [12.1, 45.4, 115.9]; foot_l [11.6, 104.3, 109.4] vs [11.3, 103.1, 116.9] |
| inguinalA_hip_l | D6_l_abd30 | 0 / 0(0.0) / 0 / 22 / 0 / -3.2 / 35 / 0.94 | 0 / 0(0.0) / 2 / 5 / 1 / 1.4 / 41 / 0.93 | f / f | shin_l [36.2, -5.0, 78.5] vs [37.7, -5.0, 78.5]; foot_l [66.3, -3.4, 29.3] vs [67.8, -3.4, 29.3] |
| inguinalA_hip_r | D6_r_flex45 | 0 / 0(0.0) / 9 / 61 / 11 / 12.1 / 59 / 0.93 | 0 / 39(5.5) / 10 / 31 / 13 / -6.7 / 52 / 0.89 | f / f | shin_r [-13.1, 28.7, 79.7] vs [-13.0, 29.7, 83.5]; foot_r [-14.6, 68.7, 38.4] vs [-14.5, 69.7, 42.2] |
| inguinalA_hip_r | D6_r_flex90 | 2 / 12(4.6) / 20 / 95 / 24 / 0.3 / 106 / 0.86 | 0 / 209(15.2) / 12 / 104 / 23 / -23.6 / 89 / 0.87 | f / f | shin_r [-12.1, 46.5, 109.4] vs [-11.9, 45.4, 116.6]; foot_r [-12.5, 104.0, 108.5] vs [-12.2, 102.9, 115.7] |
| inguinalA_hip_r | D6_r_abd30 | 0 / 0(0.0) / 0 / 38 / 0 / -5.5 / 33 / 0.94 | 0 / 0(0.0) / 0 / 1 / 0 / -1.3 / 39 / 0.93 | f / f | shin_r [-35.7, -4.6, 78.2] vs [-37.2, -4.6, 78.3]; foot_r [-66.2, -5.0, 29.5] vs [-67.7, -5.0, 29.6] |
| oldE3_gh_l | D1_l_abd45 | 0 / 0(0.0) / 0 / 0 / 0 / -3.6 / 34 / 0.63 | 0 / 0(0.0) / 0 / 0 / 0 / 2.1 / 32 / 0.53 | P / P | forearm_l [46.4, -8.9, 152.8] vs [45.2, -8.9, 152.6]; hand_l [73.0, -0.2, 125.4] vs [71.9, -0.1, 125.2] |
| oldE3_gh_l | D1_l_abd90 | 0 / 0(0.0) / 0 / 39 / 5 / -7.2 / 66 / 0.12 | 0 / 55(5.3) / 0 / 84 / 5 / -4.0 / 57 / 0.24 | f / f | forearm_l [56.6, -10.6, 177.6] vs [54.6, -10.5, 176.3]; hand_l [95.1, -3.6, 177.1] vs [93.2, -3.5, 175.9] |
| oldE3_gh_l | D1_l_flex90 | 118 / 74(20.8) / 28 / 432 / 32 / -43.7 / 70 / 0.41 | 94 / 147(16.6) / 31 / 414 / 32 / -35.6 / 65 / 0.32 | f / f | forearm_l [21.0, 25.0, 179.3] vs [21.2, 22.9, 177.9]; hand_l [18.3, 63.0, 188.4] vs [18.5, 61.0, 187.0] |
| oldE3_gh_l | D1_l_abd90_girdle | 0 / 0(0.0) / 0 / 3 / 1 / -0.7 / 59 / 0.35 | 0 / 0(0.0) / 0 / 2 / 0 / 2.4 / 56 / 0.29 | f / f | forearm_l [54.9, -13.4, 182.6] vs [53.4, -13.4, 181.5]; hand_l [93.6, -9.5, 178.1] vs [92.2, -9.6, 177.0] |
| oldE3_gh_l | D1_l_flex90_girdle | 8 / 55(17.1) / 24 / 271 / 25 / -37.3 / 61 / 0.31 | 7 / 56(12.8) / 22 / 251 / 27 / -29.1 / 60 / 0.22 | f / f | forearm_l [26.7, 20.2, 169.0] vs [26.8, 18.3, 168.7]; hand_l [30.4, 57.4, 157.1] vs [30.6, 55.4, 156.7] |
| oldE3_gh_r | D1_r_abd45 | 0 / 0(0.0) / 0 / 0 / 0 / -6.8 / 38 / 0.55 | 0 / 0(0.0) / 0 / 0 / 0 / -0.3 / 36 / 0.46 | f / f | forearm_r [-46.7, -8.1, 152.7] vs [-44.7, -8.2, 151.8]; hand_r [-72.7, 2.1, 124.9] vs [-70.7, 2.0, 123.9] |
| oldE3_gh_r | D1_r_abd90 | 0 / 0(0.0) / 0 / 117 / 4 / -13.2 / 72 / 0.39 | 0 / 76(6.4) / 0 / 130 / 1 / -8.1 / 58 / 0.32 | f / f | forearm_r [-57.0, -6.8, 177.3] vs [-54.0, -7.0, 173.9]; hand_r [-94.7, 4.8, 175.8] vs [-91.7, 4.6, 172.4] |
| oldE3_gh_r | D1_r_flex90 | 54 / 158(16.3) / 12 / 511 / 24 / -59.3 / 74 / 0.47 | 17 / 160(19.9) / 8 / 355 / 21 / -31.9 / 68 / 0.34 | f / f | forearm_r [-21.8, 25.3, 178.6] vs [-22.6, 24.3, 172.4]; hand_r [-19.6, 63.5, 188.0] vs [-20.4, 62.6, 181.8] |
| oldE3_gh_r | D1_r_abd90_girdle | 0 / 0(0.0) / 0 / 1 / 0 / -5.9 / 62 / 0.33 | 0 / 25(0.7) / 0 / 22 / 0 / -1.6 / 58 / 0.18 | f / f | forearm_r [-54.3, -14.9, 182.6] vs [-52.3, -15.1, 179.7]; hand_r [-93.2, -10.3, 177.5] vs [-91.1, -10.5, 174.6] |
| oldE3_gh_r | D1_r_flex90_girdle | 13 / 44(12.2) / 3 / 348 / 15 / -50.8 / 61 / 0.33 | 0 / 116(16.8) / 0 / 165 / 16 / -24.4 / 62 / 0.27 | f / f | forearm_r [-28.6, 18.9, 170.4] vs [-30.3, 16.4, 166.3]; hand_r [-35.1, 56.6, 160.9] vs [-36.7, 54.1, 156.8] |
| v003bounded_knee_l | D7_l_flex90 | 3 / 121(14.5) / 0 / 286 / 12 / -21.8 / 78 / 0.24 | 0 / 116(13.4) / 0 / 271 / 10 / -19.5 / 80 / 0.24 | f / f | foot_l [14.0, -62.9, 70.4] vs [14.0, -63.1, 70.1] |
| v003bounded_knee_l | D7_l_flex140 | 0 / 0(0.0) / 0 / 363 / 22 / -36.8 / 81 / 0.35 | 0 / 0(0.0) / 0 / 349 / 23 / -35.2 / 83 / 0.35 | f / f | foot_l [12.8, -42.9, 114.8] vs [12.8, -43.3, 114.7] |


**Shoulder, old E3 GH (comparison only):**
- **Pure-GH 90° abduction:** E3 has no crease contacts, against 55 / 76 for v002. Its orientation failures are lower on the left (39 vs 84) and slightly lower on the right (117 vs 130). Its zone proxy loss is worse (−7.2 / −13.2 % vs −4.0 / −8.1 %).
- **90° flexion:** E3 is worse, with 118 / 54 non-contact intersections against 94 / 17, and more orientation failures.
- **Endpoints:** the elbow / hand endpoints differ by 1–6 cm between pivots for the same named angle.
- **Girdle-assisted variants:** these move the clavicle by 20°, which carries the scapula bone (medial proxy → acromion) as its child. They reduce flexion crease depth for both pivots but do not make either pass.
- **Not accepted as mechanics:** the 20° split is a test setting, not accepted scapulohumeral mechanics.
- **The v002 GH remains the baseline.**

**Hip, inguinal-axis alternative (sensitivity only, not approved):**
- **Flexion:** it removes most crease penetration (45°: 0 vs 25; 90°: 8 vs 220), but has more folds outside the crease (19 vs 9) and a zone proxy of +14 % at 45°.
- **Abduction:** it regresses, with 22 / 38 orientation failures against 5 / 1.
- **Endpoints:** it moves the knee endpoint 4–7.5 cm lower in 90° flexion. Equal named angles are therefore not equal motion.
- **No pivot is optimal across flexion and abduction, and none passes.**

**Knee, bounded v003 vs unrestricted v002 (W2):** D7 results are almost identical: 3 vs 0 non-contact pairs, 286 vs 271 orientation failures, −21.8 vs −19.5 %, the same 0.24 loop. The ankle endpoints differ by 0.2–0.4 cm. **The knee failures are not sensitive to this 5–8 mm placement question.** Neither placement establishes internal joint-centre accuracy.

### 5.2 LBS vs DQS (rig v002, identical pivots / weights / poses)

| pose (rig v002, W2) | LBS nc / crease(mm) / folds-out / orient / inv / zone % / p95 / loop | DQS same | pass LBS / DQS |
|---|---|---|---|
| D1_l_abd90 | 0 / 55(5.3) / 0 / 84 / 5 / -4.0 / 57 / 0.24 | 0 / 0(0.0) / 0 / 71 / 2 / 12.0 / 72 / 0.07 | f / f |
| D1_l_flex90 | 94 / 147(16.6) / 31 / 414 / 32 / -35.6 / 65 / 0.32 | 58 / 55(37.8) / 20 / 407 / 23 / -27.1 / 79 / 0.21 | f / f |
| D6_l_flex45 | 0 / 24(2.9) / 7 / 30 / 20 / -6.9 / 54 / 0.88 | 0 / 5(1.7) / 4 / 37 / 7 / 0.5 / 58 / 0.84 | f / f |
| D6_l_flex90 | 0 / 212(20.5) / 9 / 104 / 17 / -24.4 / 90 / 0.88 | 0 / 72(14.5) / 10 / 110 / 28 / 0.8 / 120 / 0.74 | f / f |
| D6_l_abd30 | 0 / 0(0.0) / 2 / 5 / 1 / 1.4 / 41 / 0.93 | 0 / 0(0.0) / 1 / 21 / 0 / 4.6 / 42 / 0.94 | f / f |
| D1_r_abd90 | 0 / 76(6.4) / 0 / 130 / 1 / -8.1 / 58 / 0.32 | 0 / 53(3.2) / 0 / 136 / 1 / 6.2 / 72 / 0.17 | f / f |
| D1_r_flex90 | 17 / 160(19.9) / 8 / 355 / 21 / -31.9 / 68 / 0.34 | 10 / 67(61.3) / 9 / 311 / 15 / -18.4 / 84 / 0.16 | f / f |
| D6_r_flex90 | 0 / 213(15.2) / 12 / 104 / 23 / -23.6 / 89 / 0.87 | 0 / 101(27.8) / 15 / 111 / 30 / 0.7 / 116 / 0.76 | f / f |
| D6_r_abd30 | 0 / 0(0.0) / 0 / 1 / 0 / -1.3 / 39 / 0.93 | 0 / 0(0.0) / 0 / 26 / 0 / 1.8 / 40 / 0.94 | f / f |
| D2_l_flex90 | 0 / 135(6.5) / 0 / 206 / 21 / -11.5 / 63 / 0.3 | 0 / 121(7.2) / 0 / 219 / 5 / 0.6 / 77 / 0.33 | f / f |
| D2_l_flex130 | 173 / 127(7.7) / 0 / 316 / 33 / -19.4 / 63 / 0.19 | 173 / 119(6.2) / 0 / 401 / 6 / 0.7 / 102 / 0.2 | f / f |
| D3_l_flex60 | 0 / 0(0.0) / 0 / 0 / 0 / -5.2 / 47 / 0.46 | 0 / 0(0.0) / 0 / 0 / 0 / 0.5 / 52 / 0.42 | f / f |
| D3_l_ext60 | 0 / 0(0.0) / 0 / 0 / 0 / -6.4 / 46 / 0.44 | 0 / 0(0.0) / 0 / 0 / 0 / -1.0 / 54 / 0.38 | f / f |
| D4_l_fist | 2 / 785(18.1) / 0 / 329 / 50 / -21.3 / 57 / 0.0 | 3 / 624(16.2) / 0 / 275 / 31 / -6.8 / 70 / 0.0 | f / f |
| D5_l_oppose_pinky | 4 / 183(8.9) / 3 / 246 / 10 / -5.2 / 36 / 1. | 10 / 170(8.8) / 1 / 270 / 7 / -5.7 / 33 / 1. | f / f |
| D5_l_oppose_pinch | 0 / 21(4.7) / 0 / 49 / 15 / -5.3 / 47 / 0.3 | 0 / 15(4.2) / 0 / 49 / 13 / 1.9 / 51 / 0.3 | f / f |
| D7_l_flex90 | 3 / 121(14.4) / 0 / 286 / 12 / -21.2 / 78 / 0.24 | 0 / 108(18.7) / 0 / 310 / 2 / -1.8 / 106 / 0.14 | f / f |
| D7_l_flex140 | 0 / 0(0.0) / 0 / 363 / 22 / -36.4 / 81 / 0.34 | 0 / 0(0.0) / 1 / 515 / 14 / -3.5 / 169 / 0.22 | f / f |


**DQS results:**
- **What improves:** DQS removes most of the volume-proxy loss.
- **What does not:**
  - orientation failures are mostly unchanged and rise in several poses (e.g. D2 130°: 316 → 401; D7 140°: 363 → 515);
  - p95 strain rises: knee 140° 81 → 169 %, hip 90° 90 → 120 %;
  - loop compression gets worse at the knee and shoulder;
  - the hip still folds outside the crease (10 / 15).
- **No pose passes under DQS.** DQS was evaluated only on these 18 poses, not the full suite.

## 6. Metric validation

**Orientation test (the old "flips"):**
- **What it measures:** a face normal opposed to the **skinned reference normal**, that is, the rest normal carried by the blended linear transform. It is **not** a demonstrated surface inversion.
- **Geometric check added:** a face whose normal opposes the sum of its 4 edge-neighbours' normals.
- **Result:** of the **2,343** baseline orientation failures across the 43 poses, only **53 (2.3 %)** are local inversions. Shoulder and elbow failures have 0. The 53 real local inversions are in the fist (14), hip flexion (34), knee (3), thumb pinch (1) and one girdle variant (1).
- The historical numbers are retained and still fail the retained "no new flipped faces" criterion. The geometric evidence shows that **most of them are not fold-overs**.

**Intersections:**
- BVH overlap of the posed quads, excluding face pairs that share vertices.
- **Classification:**
  - *contact* = a declared part pair between different parts (e.g. hand–leg, arm–axial, calf–thigh in deep knee flexion);
  - *crease* = within the crease radius of the tested joint;
  - otherwise *non-contact*.
- **Depth:** per pair, the deepest vertex of one face behind the plane of the other.
- Representative pairs with face IDs are in every `diag_results_*.json` (`representative_pairs`) and on the overlays.

**Zone volume:**
- It is an **open-patch cone-volume proxy**: tetrahedra from the posed joint centre to the zone's own-tissue faces, with no cap. It is **not** tissue volume.
- **Rigid sanity check (`metric_check.json`):** the whole body rotated 30° gives 0 intersections, 0 orientation failures, 0 inversions, 0 folds and 0 strain, and **0.000 % change for all four zone proxies**.
- **Reference sensitivity (moving the reference 1 cm):**

  | Zone | Change |
  |---|---|
  | Shoulder | up to 7.8 % (unreliable there) |
  | Hip | 3.6 % |
  | Elbow / knee | ≤ 0.7 % |

- The historical numbers are retained.

**Masks:**
- The crease and contact classes are drawn on the geometry in every overlay (red / orange / yellow).
- **No mask was enlarged and no threshold was relaxed.**
- **Forearm–upper-arm proximity at 130° elbow flexion** is declared a *candidate expected contact region*. Its 173 pairs (representative depth 1.9 mm) keep their original **non-contact** classification and still fail.

## 7. Failure overlays (exact IDs) and sheets

`sheets/F_shoulder_l`, `F_shoulder_r`, `F_elbow`, `F_hip_groin_l`, `F_hip_groin_r`, `F_knee` and `F_thumb_fist`:
- W0 and W2 for each pose, three identical cameras, neutral clay;
- face colours by failure type;
- IDs printed beside each row: non-contact pairs, inversion faces, fold pairs, compressed-loop vertices;
- complete ID arrays in `diag/ids/*.npz`.

**Display offsets:** none. The hip sheets hide that side's arm and hand, which is disclosed on the sheet.

`sheets/W_weight_maps.jpg`: W0 / W2 weight maps for upperarm, forearm, hand, thigh, shin, thumb_p1 and index_p3.

## 8. Qualified conclusions and failure classification

**Topology cannot be excluded as a contributor, and neither is it shown to be a cause.**
- **What the evidence supports:** a substantial contribution from diagnostic weights and the skinning method.
  - Weight changes move the results in both directions.
  - DQS changes the volume behaviour.
  - Pivot changes move the hip crease penetration a great deal.
- **What persists:** under every tested condition (W0 / W2, LBS / DQS, v002 / v003 knee, E3 / v002 GH), localized **inner-crease loop compression** remains at the same tagged loops.

**Implicated loops:**

| Location | Loops | Worst compression |
|---|---|---|
| Shoulder | `shoulder_fan_l_2–4` | 7–32 % |
| Elbow | `elbow_l_21|22` | 30–33 % |
| Knee | `knee_l_71|73` | 14–35 % |
| Palm (fist) | `mcp_palm_l_4–6` | 5–26 % |
| Wrist | `wrist_palm_l_0|1` | 42–46 % |

- **Mechanism:** consecutive rings on the flexion side converge as the crease closes. Some of this is physically expected compression. Whether the loop spacing and density at these joints also limits the result cannot be separated with LBS / DQS and diagnostic weights alone.
- **Corrective shapes** might address it. That was not tested, and no claim is made that they would suffice.

**Per-failure classification (baseline W0):**

| pose | W0 failed criteria | classification | confidence |
|---|---|---|---|
| D1_l_abd90 | no new flipped faces (49 (49 in crease)); zone volume within ±5% (-6.6%); joint-loop spacing >= 50% of rest (0.23); crease contact depth <= 2 mm (4.5 mm) | combination: diagnostic weights + skinning method + test setup (pure-GH); possible topology contribution at shoulder_fan_l/r_2-4 not excluded | medium |
| D1_l_flex90 | 0 non-contact intersections (38); no new flipped faces (359 (269 in crease)); no new folds outside crease/contact zones (+22 (outside 10)); zone volume within ±5% (-33.9%); joint-loop spacing >= 50% of rest (0.19); crease contact depth <= 2 mm (16.6 mm) | combination: diagnostic weights + skinning method + test setup (pure-GH); possible topology contribution at shoulder_fan_l/r_2-4 not excluded | medium |
| D6_l_flex45 | no new flipped faces (7 (7 in crease)); no new folds outside crease/contact zones (+18 (outside 1)); zone volume within ±5% (-6.6%) | placement sensitivity (inguinal pivot removes most crease penetration but adds orientation failures / folds and changes the knee path by 4-7.5 cm) + weights + skinning method; DQS adds folds outside the crease | medium |
| D6_l_flex90 | no new flipped faces (49 (47 in crease)); zone volume within ±5% (-24.5%) | placement sensitivity (inguinal pivot removes most crease penetration but adds orientation failures / folds and changes the knee path by 4-7.5 cm) + weights + skinning method; DQS adds folds outside the crease | medium |
| D1_r_abd90 | no new flipped faces (9 (9 in crease)); zone volume within ±5% (-13.4%); joint-loop spacing >= 50% of rest (0.28) | combination: diagnostic weights + skinning method + test setup (pure-GH); possible topology contribution at shoulder_fan_l/r_2-4 not excluded | medium |
| D1_r_flex90 | no new flipped faces (259 (175 in crease)); zone volume within ±5% (-30.6%); joint-loop spacing >= 50% of rest (0.35); crease contact depth <= 2 mm (14.3 mm) | combination: diagnostic weights + skinning method + test setup (pure-GH); possible topology contribution at shoulder_fan_l/r_2-4 not excluded | medium |
| D6_r_flex45 | no new flipped faces (8 (6 in crease)); zone volume within ±5% (-6.8%) | placement sensitivity (inguinal pivot removes most crease penetration but adds orientation failures / folds and changes the knee path by 4-7.5 cm) + weights + skinning method; DQS adds folds outside the crease | medium |
| D6_r_flex90 | no new flipped faces (48 (46 in crease)); no new folds outside crease/contact zones (+39 (outside 3)); zone volume within ±5% (-24.5%) | placement sensitivity (inguinal pivot removes most crease penetration but adds orientation failures / folds and changes the knee path by 4-7.5 cm) + weights + skinning method; DQS adds folds outside the crease | medium |
| D2_l_flex90 | no new flipped faces (135 (135 in crease)); zone volume within ±3% (-16.5%); joint-loop spacing >= 50% of rest (0.32); crease contact depth <= 2 mm (4.2 mm) | weights + skinning method (DQS lowers the volume proxy, not penetration/orientation); at 130 deg forearm-upper-arm candidate expected contact with real penetration; loop compression elbow_l_21|22 persistent | medium |
| D2_l_flex130 | 0 non-contact intersections (173); no new flipped faces (211 (211 in crease)); zone volume within ±3% (-27.9%); joint-loop spacing >= 50% of rest (0.20); crease contact depth <= 2 mm (5.3 mm) | weights + skinning method (DQS lowers the volume proxy, not penetration/orientation); at 130 deg forearm-upper-arm candidate expected contact with real penetration; loop compression elbow_l_21|22 persistent | medium |
| D3_l_flex60 | no new flipped faces (9 (9 in crease)); zone volume within ±5% (-5.9%); joint-loop spacing >= 50% of rest (0.45) | weights / skinning (W2 removes intersections + orientation failures at 60 deg; volume proxy and wrist_palm loop compression remain) | medium |
| D3_l_ext60 | no new flipped faces (6 (6 in crease)); zone volume within ±5% (-9.3%); joint-loop spacing >= 50% of rest (0.42) | weights / skinning (W2 removes intersections + orientation failures at 60 deg; volume proxy and wrist_palm loop compression remain) | medium |
| D4_l_fist | 0 non-contact intersections (2); no new flipped faces (194 (194 in crease)); zone volume within ±5% (-17.2%); joint-loop spacing >= 50% of rest (0.26); crease contact depth <= 2 mm (4.7 mm); nail rigidity <= 0.3 mm (0.71 mm) | weights (nail rigidity fixed by binding), crease compression at mcp_palm loops persists under all methods; possible topology contribution not excluded | low-medium |
| D5_l_oppose_pinky | 0 non-contact intersections (4); no new flipped faces (235 (176 in crease)); no new folds outside crease/contact zones (+8 (outside 3)); crease contact depth <= 2 mm (8.9 mm) | weights + test setup (searched pose); thenar crease self-contact; nail fixed by binding | medium |
| D5_l_oppose_pinch | no new flipped faces (9 (9 in crease)); joint-loop spacing >= 50% of rest (0.46); nail rigidity <= 0.3 mm (0.44 mm) | weights + test setup (searched pose); thenar crease self-contact; nail fixed by binding | medium |
| D7_l_flex90 | no new flipped faces (192 (192 in crease)); zone volume within ±5% (-25.0%); joint-loop spacing >= 50% of rest (0.18); crease contact depth <= 2 mm (6.9 mm) | weights + skinning method; placement-insensitive (bounded v003 vs v002 knee identical within noise); persistent knee_l_71|73 loop compression to 14-35 % under every method - possible topology contribution not excluded | medium |
| D7_l_flex140 | no new flipped faces (283 (283 in crease)); zone volume within ±5% (-44.2%); joint-loop spacing >= 50% of rest (0.30) | weights + skinning method; placement-insensitive (bounded v003 vs v002 knee identical within noise); persistent knee_l_71|73 loop compression to 14-35 % under every method - possible topology contribution not excluded | medium |
| D1_l_abd90_girdle | joint-loop spacing >= 50% of rest (0.24) | combination: diagnostic weights + skinning method + test setup (pure-GH); possible topology contribution at shoulder_fan_l/r_2-4 not excluded | medium |
| D1_l_flex90_girdle | no new flipped faces (195 (140 in crease)); zone volume within ±5% (-27.5%); joint-loop spacing >= 50% of rest (0.26); crease contact depth <= 2 mm (12.8 mm) | combination: diagnostic weights + skinning method + test setup (pure-GH); possible topology contribution at shoulder_fan_l/r_2-4 not excluded | medium |
| D1_r_abd90_girdle | zone volume within ±5% (-5.5%); joint-loop spacing >= 50% of rest (0.41) | combination: diagnostic weights + skinning method + test setup (pure-GH); possible topology contribution at shoulder_fan_l/r_2-4 not excluded | medium |
| D1_r_flex90_girdle | no new flipped faces (86 (57 in crease)); zone volume within ±5% (-22.8%); joint-loop spacing >= 50% of rest (0.46); crease contact depth <= 2 mm (9.7 mm) | combination: diagnostic weights + skinning method + test setup (pure-GH); possible topology contribution at shoulder_fan_l/r_2-4 not excluded | medium |
| D9_twist_m30 | 0 non-contact intersections (2) | diagnostic weights at the axilla (2 arm self-contacts) | medium |
| D9_flex30 | 0 non-contact intersections (2) | diagnostic weights at the axilla (2 arm self-contacts) | medium |


## 9. Decisions needed from ChatGPT

1. **D-1 Topology question.** Accept the qualified conclusion: weights / skinning contribute substantially and topology is not excluded. Decide whether the persistent loop compression at `knee_l_71|73`, `elbow_l_21|22`, `shoulder_fan_2–4` and `mcp_palm_4–6` warrants a dedicated test. Options are corrective-shape or helper-joint diagnostics in a later order, or an author decision that the compression is expected crease behaviour.
2. **D-2 Knee.** Accept the bounded v003 knee as the diagnostic knee. The deformation is insensitive to it. Alternatively, rule how the section-centre requirement and the 5 mm cap should be reconciled (residual 2.75 / 0.83 mm).
3. **D-3 Weights.** Authorise one more weight candidate. The baseline plus nail binding is the only supported change. Region-boundary blending would be needed for any further local transition edits.
4. **D-4 Hip.** Keep v002. The inguinal alternative helps flexion penetration but regresses abduction and changes the limb path.
5. **D-5 Shoulder.** Define the girdle-participation test policy (what moves, and how much) before more shoulder elevation tests. E3 stays a comparison only.
6. **D-6 Ankle cap.** Confirm whether the AD-R2 ankle placement, 1.0–1.1 cm from the v001 xy, was meant to be capped.
7. **D-7 Metric policy.** Decide whether the retained "no new flipped faces" criterion should be paired with the geometric local-inversion test in future gates. The historical results stay unchanged.

**STOP FOR CHATGPT REVIEW.** No diagnostic candidate is frozen or declared final, and production deformation is not accepted.
