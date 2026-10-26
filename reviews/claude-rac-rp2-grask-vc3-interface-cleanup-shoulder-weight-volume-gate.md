# RAC RP2 — Grask VC3 interface cleanup + shoulder weight/volume refinement — gate return

**Date:** 2026-10-26
**Order:** `reviews/chatgpt-rac-rp2-grask-vc3-interface-cleanup-and-shoulder-weight-volume-order.md` (28dd8d3)
**Parent return:** bb029bb

## RETURN SUMMARY (§24)

### Elbow (Track E2)

| Item | Result |
|---|---|
| Selected cleanup candidate | **none** |
| VC3 rumpling removed? | **No.** VC3F1 and VC3F2 measurably lower the band curvature variation and ripple, but the irregular contact-interface texture is still visible in same-camera clay. |
| New artifacts | **Yes.** Both candidates add local inversions at 130°: F1 2 L / 1 R, F2 2 L / 1 R (VC3 had 0). F1 left loop is 0.493 (< 0.50); F1 left orientation is 106. |
| Corrected physical volume (overlap-aware, vs straight elbow) | VC3 −170 / −182 cm³; F1 −170 / −182; F2 −171 / −182. C2 / C2rx −498 / −694. Gain kept: ≥ 99.8 %. |
| Ring girth | Max ring radius change vs straight base: F2 +0.26 cm (L) / +0.30 cm (R), against the 0.35 limit. No station shrinks below C2. |
| Crease / orientation / loop / p95 (max) at 130° | F2 L: 2.8 mm / 100 / 0.516 / 59.3 (96) %. F2 R: 1.6 mm / 82 / 0.579 / 59.9 (97) %. |
| 130° status | **Carried forward unresolved.** Per §11, RP2 elbow experimentation is **closed**; 130° becomes a production-rig contact-corrective item. |

### Shoulder (Track S2)

| Item | Result |
|---|---|
| Selected SW candidate | **none meets every §18 target.** SW3 is the best production-direction result. It meets every target on the right side and on every left pose except **left flex90**. |
| flex90 crease (W0 → SW3) | L 16.6 → **7.9 mm** (target 0–2: **miss**); R 14.3 → **0.0 mm** |
| abd90 crease | L 4.5 → 0.0; R 1.0 → 0.0 mm |
| Orientation (W0 → SW3) | flex90 L 359 → 122 (target ≤ 100: miss), R 259 → 88. abd90 0 / 0. |
| Non-contact intersections | 0 everywhere except left flex90: 6 (W0 38) |
| New local inversions | left flex90 2 (W0 0); 0 on every other pose. |
| Loop spacing (shoulder fan) | 0.53–0.87 on every D1 pose (W0 0.19–0.83) |
| Volume (zone proxy) | flex90 L −32.1 % / R −28.6 % (W0 −33.9 / −30.6; S2 −48.9 / −49.0). Recovers 112 % / 111 % of S2's excess loss. abd90 L −14.2 / R −15.5 (S2 −29.1 / −30.8). |
| Max strain | ≤ 135 % on every D1 pose (S2 up to 209 %); S2's spikes removed |
| Weighting-dominant classification | **Remains.** Girdle-only weight diffusion plus a bounded LBS / DQS volume field fixes 11 of 12 D1 poses. |
| Topology issue demonstrated? | **No.** Fan loops reach 0.53–0.87. The left flex90 residual is an anterior-fold arm–arm overlap that moves with weighting and blend strength. |

### Global

| Item | Result |
|---|---|
| Parent integrity | **Identical.** `hashes_before.txt` = `hashes_after.txt` (v003, v005, sidecars, rigdiag v001–v004, all prior weight / corrective records, and the v006 VC3 / S2 records). |
| Regression | E2: only the K130 key changes, so angles ≤ 120° are bit-identical to VC3 (verified 45–120°). SW3 full 43-pose suite: no new retained-criterion failure outside D1. D7 / D8 deviate ≤ 2e-5 cm; D9 / D10 ≤ 0.08 cm (girdle-only weights). D1 new failures: zone ±5 % at abd45 L/R (−5.0 / −5.7 %) and abd90_girdle L (−12.6 %, W0 +0.3). |
| Production deformation accepted? | **No.** |
| Next ChatGPT decision | §6 |

**Evidence:** `reviews/rac-rp2-evidence/grask_rig_diagnostic_v007/` (`trackE2/`, `trackS2/`, `hashes/`).

**Tools** (`tools/rac/rp/grask_rigprep_v001/`):
- Track E2: `vc3_fair.py`, `e2_texture.py`, `e2_sheets.py`;
- Track S2: `sw_dqs.py`, `sw_maps.py`, `sw_strain.py`;
- extended: `shoulder_s2.py` (region-graph diffusion, girdle-only column option), `shoulder_judge.py` and `shoulder_sheets.py` (configurable tags).

No derived .blend was built, because no candidate was selected. Nothing was written to the PC.

## 1. Rulings applied

- H2 stays the 60–120° diagnostic configuration. VC3 is not promoted. No C/H search reopened. No helper bones added.
- Primary elbow volume metric is now the overlap-aware physical change vs the straight elbow, plus ring girth. The closed-mesh divergence volume is reported only for continuity.
- The shoulder stays WEIGHTING-DOMINANT. GH is not moved. The S1 abduction girdle rule is retained. No topology reinterpretation.

## 2. Track E2 method and results

**Method (VC3F1, §6).** `vc3_fair.py` fairs only the VC3 130° key:
1. The interface seam is every arm vertex whose nearest vertex on the other segment (posed bisector plane side) is < 1 cm away.
2. The support is the rest-geodesic band around the seam (F1: 4 cm, full inside 2.5 cm), stored as `fair_support_*`.
3. The corrective displacement field Δ = X_VC3 − X_W0 is Taubin-smoothed on that support (20 × λ 0.5 / μ −0.53), Dirichlet outside.
4. A volume lock gives back the tiny closed-volume change as a smooth normal offset.
5. The result is mapped back to the rest-space key exactly: round trip 9e-14 cm. Outside the support the key is bit-identical.

**VC3F2** is the single bounded refinement:
- a 7 cm band (full inside 5 cm);
- 150 iterations;
- the tight contact itself held (Dirichlet within 0.3 cm of the other side, 0.7 cm ramp);
- a contact guard against crossing the bisector plane.

Each candidate moves the posed surface by at most 0.29 / 0.41 cm (F1) and 0.39 / 0.71 cm (F2).

**130° results, left / right** (`trackE2/diag/`):

| | nc | crease (mm) | orientation | local inv | folds outside | loop | p95 (max) % | zone % | physical dV (cm³) | max ring Δr (cm) |
|---|---|---|---|---|---|---|---|---|---|---|
| VC3 L | 0 | 28 (2.9) | 85 | 0 | 0 | 0.577 | 60.5 (104) | −28.9 | −170 | +0.24 |
| F1 L | 0 | 73 (1.9) | 106 | **2** | 0 | **0.493** | 60.0 (96) | −29.0 | −170 | +0.25 |
| F2 L | 0 | 143 (2.8) | 100 | **2** | 0 | 0.516 | 59.3 (96) | −28.9 | −171 | +0.26 |
| VC3 R | 0 | 6 (0.3) | 68 | 0 | 0 | 0.588 | 60.6 (96) | −26.8 | −182 | +0.28 |
| F1 R | 0 | 51 (1.7) | 90 | **1** | 0 | 0.549 | 60.2 (97) | −26.8 | −182 | +0.28 |
| F2 R | 0 | 204 (1.6) | 82 | **1** | 0 | 0.579 | 59.9 (97) | −26.7 | −182 | +0.30 |

At 120° and below, F1 / F2 are identical to VC3 on both sides. Rest return is 1.4e-12 mm in every row.

**Texture metrics (§10, support only).** Interface band, left / right:

| | curvature variation, mean (1/cm) | gradient across / along, mean | ripple p95 (mm) |
|---|---|---|---|
| C2 | 0.021 / 0.023 | 0.093 / 0.055 (L) | 0.95 / 1.00 |
| VC3 | 0.033 / 0.036 | 0.140 / 0.105 (L) | 1.20 / 1.45 |
| F1 | 0.023 / 0.025 | 0.139 / 0.103 (L) | 1.11 / 1.39 |
| F2 | 0.031 / 0.028 | 0.141 / 0.108 (L) | 1.08 / 1.32 |

F1 brings the band curvature variation back to the C2 level. The gradients do not change, though: the mid-frequency undulation (wavelength of a few cm) that reads as rumpling is still there, and it remains visible in `E2_closeup_{l,r}.jpg` (inner crease and outer views, both sides).

**Explicit §11 answers**
1. VC3 rumpling visibly removed? **No.** Reduced in the high-frequency metric only.
2. All numeric VC3 gains preserved? **No.** Volume, girth, nc, crease ≤ 3.5 mm and strain are preserved. Local inversions are new on both sides (F1, F2), and F1 left loop drops to 0.493.
3. Corrected physical volume still improved vs C2 / C2rx? **Yes.** −171 / −182 vs −498 / −694 cm³; ≥ 99.8 % of VC3's gain kept.
4. New artifact? **Yes**: the local inversions above. No shelf, wall, balloon or faceted band.
5. 130° status? **Still unresolved.** RP2 elbow experimentation is **closed** per §11. 130° is carried forward as a production-rig / contact-corrective item.

**Evidence** (`trackE2/sheets/`):
- `E2_closeup_{l,r}.jpg`: clay + IDs (inner / three-quarter contact line / outer), wire close-up, strain map, |X − X_VC3| map;
- `E2_support.jpg`: support mask;
- `E2_sections.jpg`: contact cross-sections;
- `E2_metrics.jpg`: curvature variation, gradients, ripple, physical volume;
- `E2_girth.jpg`: ring radius by station.

The keys are stored as delta rows over the v006 VC3 keys, with full-array SHA-256.

## 3. Track S2 method

**Mechanics.** S1 girdle rule (v006) unchanged, and GH fixed:
- abduction: ST share ⅓·(e − 30°);
- flex90 also keeps the S1 rule: ST 21 / 19°, glenohumeral motion 90 → 85 / 86°, clavicle 19 / 17°, scapula 28 / 29°.
- Without it, every weighting trial leaves the left flex90 chest non-contact (37–38 pairs; T1, T3-SW). That is the honest reading of §19: in this architecture flex90 remains mainly weight- and field-driven, but the moderate girdle share is still needed.

**Weighting trials** (bounded; all logged in `trackS2/config` and `diag`):

| Trial | Configuration | Result |
|---|---|---|
| T1 | girdle columns, 18 cm, W0 flex mechanics | abduction clean; flex90 L crease 18.8 mm, nc 38 |
| T2 | all columns, 18 cm | torso-column spikes (max 245 %); flex90 L crease 23.6 mm |
| **SW1** (= T3) | girdle columns only (clavicle / scapula / upper arm), 22 cm region (full inside 14 cm), 600-iteration region-graph diffusion, Dirichlet W0 outside, S1 mechanics | rows outside the region are bit-identical; spine / thoracic / neck columns unchanged |

**Volume-preservation mechanism (§16).** A bounded LBS / DQS blend: X = (1 − b)·LBS + b·DQS, with the same weights and pose matrices (`sw_dqs.py`). This is the production mechanism behind Blender's armature "Preserve Volume" with a mixing vertex group.
- b is a C2 bump around GH: 1·strength inside 14 cm, 0 at 22 cm, arm_s + axial only.
- Vertices with b = 0 are LBS bit-for-bit.
- Single-bone vertices match LBS to 1.6e-4 cm (float32 storage).
- **SW2:** strength 1.0. **SW3:** strength 0.5 (the single bounded refinement: SW2 over-restored at left flex90, nc 14, crease 7.7 mm, 6 inversions, 14 folds outside).

## 4. Track S2 tables

Full tables: `trackS2/diag/trackS2_tables.md` (W0, S1, S2, T1, T2, SW1, SW2, SW3, all D1 poses).

Cells read: nc / crease (mm) / orientation / local inversions / folds outside / loop / p95 (max) % / zone %.

| Pose | W0 | S2 | SW1 | SW2 | **SW3** |
|---|---|---|---|---|---|
| L abd90 | 0/49 (4.5)/49/0/0/0.23/54 (99)/−6.6 | 0/0/0/0/0/0.51/44 (130)/−29.1 | 0/0/0/0/0/0.61/36 (74)/−25.0 | 4/0/0/0/0/0.72/31 (107)/−2.7 | **0/0/0/0/0/0.67/32 (90)/−14.2** |
| L flex90 | 38/71 (16.6)/359/0/10/0.19/62 (103)/−33.9 | 4/0/115/1/4/0.41/57 (140)/−48.9 | 7/57 (14.3)/128/2/3/0.44/53 (96)/−49.4 | 14/36 (7.7)/108/6/14/0.59/48 (116)/−11.7 | **6/38 (7.9)/122/2/4/0.53/49 (104)/−32.1** |
| L flex90_girdle | 0/48 (12.8)/195/0/0/0.26/58 (84)/−27.5 | 0/0/57/0/0/0.61/39 (84)/−26.5 | 0/0/59/0/0/0.65/37 (77)/−25.5 | 0/0/60/0/0/0.72/33 (79)/−6.8 | **0/0/60/0/0/0.69/35 (79)/−16.4** |
| R abd90 | 0/19 (1.0)/9/0/0/0.28/58 (98)/−13.4 | 0/0/0/0/0/0.44/44 (209)/−30.8 | 0/0/0/0/0/0.55/36 (119)/−26.5 | 0/0/0/0/0/0.69/29 (149)/−3.6 | **0/0/0/0/0/0.62/32 (134)/−15.5** |
| R flex90 | 0/64 (14.3)/259/0/0/0.35/66 (121)/−30.6 | 0/0/84/1/0/0.41/53 (193)/−49.0 | 0/0/91/0/0/0.46/49 (99)/−47.8 | 13/0/82/0/3/0.61/47 (122)/−5.8 | **0/0/88/0/0/0.55/45 (110)/−28.6** |
| R flex90_girdle | 0/35 (9.7)/86/1/0/0.46/59 (100)/−22.8 | 0/0/27/0/0/0.61/40 (118)/−26.7 | 0/0/31/0/0/0.67/34 (69)/−24.8 | 0/0/27/0/0/0.75/32 (77)/−3.2 | **0/0/30/0/0/0.72/32 (73)/−14.4** |

abd45, ext30 and abd90_girdle are clean in every SW cell. Rest return is 0 everywhere.

**SW3 left flex90 residual:**
- 6 arm–arm non-contact pairs at the anterior fold, about (17.7, 5.2, 173.5), i.e. in front of and medial to GH;
- 38 crease pairs (7.9 mm);
- 2 local inversions and 4 folds outside.
The right side is clean at the same settings; the left is the side that already had the deeper W0 failure (nc 38, 16.6 mm).

**Kinematics:** S1 readout as in v006 (clavicle 15–19°, scapula 28–30°, GH displacement 5.8–7.3 cm, inferior-angle proxy 3.7–8.5 cm). GH–acromion distance is constant (5.21 cm).

**Evidence** (`trackS2/sheets/`):
- `SW_{abd90,flex90}_{l,r}.jpg`: front / rear / three-quarter front / three-quarter rear / axillary close-up / wire close-up, with landmark and weight-boundary overlays and IDs;
- `SW_overview_{l,r}.jpg`: all six D1 poses × W0 / S1 / S2 / SW1–3;
- `SW_sections.jpg`;
- `SW_strain.jpg`: strain maps;
- `SW_maps.jpg`: weight change, upper-arm weight, DQS blend mask.

Visual read for SW3:
- smooth axillary fold;
- continuous deltoid with no cap collapse or inflation (zone −14 to −16 % at abd90, versus W0 −7 / −13);
- no arm–torso tearing;
- girdle slope preserved.
The left flex90 anterior fold still shows the residual overlap.

## 5. Regression (§23)

- **E2:** only `K130_*` changes. Every pose ≤ 120° and every non-elbow pose is bit-identical to VC3 by construction (corrective activation is elbow-only); checked on 45–120°. Since no candidate was selected, no full-suite run was needed.
- **SW3 full 43-pose suite** (`trackS2/diag/full_regress_SW3.json`):
  - D2–D6 move up to 2.1–2.5 cm through the abd45 arm set-up inside the shoulder region;
  - D9 / D10 ≤ 0.08 cm;
  - D7 / D8 ≤ 2e-5 cm.
- **New retained failures:** only D1 zone ±5 % (abd45 L −5.04 %, abd45 R −5.70 %, abd90_girdle L −12.6 %). Nothing outside D1.
- **Fixed by SW3:**
  - crease: abd90 L; flex90 R; flex90_girdle L/R;
  - flips: abd90 L/R;
  - loop: abd90 L/R; abd90_girdle L/R; flex90 L/R; flex90_girdle L/R.

## 6. Next ChatGPT decision

1. **Elbow:** experimentation is closed per §11. Record 130° as a production-rig contact-corrective item with these inputs:
   - the overlap-aware volume metric and girth bounds;
   - VC3 as the numeric reference (physical −170 / −182 cm³, girth ≤ base + 0.30 cm);
   - the finding that field smoothing alone cannot remove the mid-frequency interface undulation without new local inversions.
2. **Shoulder:** decide whether SW3 is accepted as the diagnostic production direction (girdle-only weight diffusion + 0.5 LBS / DQS preserve-volume blend + S1 abduction rule) with the left flex90 anterior-fold residual as a named open item, or whether one more bounded left-flex90 order is wanted.

Production deformation is not accepted. STOP for ChatGPT review.
