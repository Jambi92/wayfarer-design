# RAC RP2 — Grask nail binding and left-elbow weight isolation — gate return

**Date:** 2026-10-26
**Order:** `reviews/chatgpt-rac-rp2-grask-baseline-nail-binding-and-elbow-weight-isolation-order.md` (b303b9e)
**Parent return:** 9703fd2
**Status:** retopology frozen; nail/elbow diagnostic review pending; production deformation not accepted.

**Evidence:** `reviews/rac-rp2-evidence/grask_rig_diagnostic_v003/`
**Tools:** `tools/rac/rp/grask_rigprep_v001/`. New this cycle:
- `weights_nail.py`
- `nail_inspect.py`
- `nail_plate_inspect.py`
- `nail_skin_check.py`
- `pair_judge.py`
- `elbow_weights.py`
- `run_elbow.sh`
- `elbow_judge.py`
- `elbow_penetration.py`
- `elbow_sheets.py`
- `face_inspect.py`
- `rig_tag.py`

`diag_lib.py` gained one optional pose, `D2_l_flex45`, built only when `ELBOW_SET=1`. The 43-pose suite is unchanged.

## 0. Outcome in one paragraph

**W0 remains the diagnostic baseline.**

**WN (nail binding only) is not adopted.**
- WN uses the corrected, groove-bounded nail-plate selection.
- It is bit-identical to W0 outside 778 nail vertices.
- Across all 43 poses it changes no retained criterion and causes no regression. The 20/43 passes are identical.
- The reason: under W0 the nail plate is already rigid to ≤ 0.012 mm in fist and pinch.
- The 0.44–0.71 mm "nail rigidity" failures come from periungual skin that the documented cap mask includes: the proximal and lateral nail fold and the groove ring. They do not come from the plate.

**WNcap (the documented cap set bound as-is) is rejected.**
- It does pass the nail criterion, with no new criterion failures.
- But it achieves that by binding that fold skin rigidly, which moves deformation into the surrounding skin:
  - p95 skin strain rises by 4.4–7.1 percentage points around the four finger caps;
  - in pinch, a new 20.1° dihedral change appears beside the thumb nail, against 5.7° under W0.

**Neither left-elbow candidate is selected.**
- E1 uses a uniform tapered re-split.
- E2 uses a crease-biased tapered re-split.
- Both are continuous to zero across a documented band and leave the sentinels unchanged.
- E2 cuts the 90° orientation disagreement (LBS 135 → 84, DQS 125 → 19), but:
  - it deepens the retained crease-depth metric at 90° and 130°;
  - it worsens 130° on orientation and intersections;
  - it raises p95 strain.
- E1 is worse than W0 on every integrity measure except an equal 90° LBS loop ratio.

Because no elbow candidate was selected, the conditional full-suite rerun (§4) and the v003-knee verification (§4) were not triggered.

## 1. Immutable assets — verified before and after

Files: `hashes/hashes_before.txt` and `hashes/hashes_after.txt`. The after-hashes come from parents freshly re-staged from the PC at the end. The two files are identical.

| Asset | SHA-256 | Geometry |
|---|---|---|
| retopo v003 blend | `03bfe7d9…7ce0` ✔ | `f9c4a7ac…702f` ✔ |
| SOURCE_3D v005 blend | `7bba8d2d…ab14` ✔ | `2697929d…d7bc` ✔ |
| v003 json / landmarks / FREEZE, v002 and v001 records, v005 json / masks / glb | unchanged ✔ | — |
| DIAG rigdiag_v001 | `59ca4fda…e485` ✔ | — |
| DIAG rigdiag_v002 | `9e2d078a…acdf` ✔ | — |
| W0 `weights_v001c.npz` | `74cbfb95…` ✔ | — |
| W1 | `8a62be1f…` ✔ | — |
| W2 | `a2642b46…` ✔ | — |

**New derived diagnostic blend:** `E:/…/RP2/DIAG/GR_U_REF_RP2_rigdiag_v003.blend`.
- SHA-256 `4ab743fe0750982da4d9ba6757aa18f784208569b4e4a05b06eae976f0b6b2db`. The PC copy, re-staged, has the same SHA.
- Read-back body geometry `f9c4a7ac…702f` equals frozen v003 (170,466 vertices / 170,464 faces).
- Landmarks: **v002**.
- Weights: **W0**, read back bit-identical.
- Skeleton: identical to rig v001 (`matrix_local` max diff 0.0).
- Custom properties record the landmark version, the weight version, the cycle outcome and the status line.
- Manifest: `rig/GR_U_REF_RP2_rigdiag_v003_manifest.json`.

**Transient Blender-DQS evaluation copies** (`el_W0` / `el_E1` / `el_E2`):
- Each also reads back `f9c4a7ac…`, with weights bit-identical to the npz.
- They stay in the cloud workspace and are not delivered. Their SHAs are in the manifest.

Nothing violated §2:
- no geometry, rest-shape or skeleton edits;
- no correctives or helper bones;
- no production weights;
- no facial work, morphs, UVs, LODs or UE5 work.

## 2. Nail-only candidate (§3)

### 2.1 Documented selection, inspected

The documented distal-cap selection was reused unchanged. Each nail vertex is bound with weight 1.0 to the distal bone (`{f}_p3_{s}`; thumb `thumb_p2_{s}`). The selection rule:
- DIP (thumb IP) → tip axis;
- 0.35·L3 < along < L3 + 0.5 cm;
- radial < 1.6 cm;
- dorsal offset > 0.6 × the median candidate radius.

The selection covers 1,105 vertices over both hands: 102–122 per digit, all on that digit's own part.

**Visual inspection** (`sheets/N_nail_selection_documented_cap_overview.jpg`, `sheets/N_nail_selection_cap_vs_plate.jpg`, which show clay without wire, class colours and wireframe from four views per digit):
- The sculpted nail plate is bounded by a U-shaped groove (proximal + lateral). The groove is visible as concavity in the clay renders.
- The documented set crosses that groove. It includes:
  - the groove ring;
  - proximal-fold "ears" toward the DIP;
  - lateral-fold skin;
  - tip skin.
- Under W0 those vertices carry 0.95–0.99 on the distal bone; the remainder is on the middle phalanx. That blend is what bends in the fist.

This is the surrounding-skin inclusion the order asks to be reported.

### 2.2 Correction (subset only; nothing added)

- Per vertex, concavity = umbrella Laplacian · outward normal / mean edge length.
- Groove vertices = concavity > 0.08.
- Within the documented set, the plate is the connected region grown by edge adjacency from the most dorsal vertex at 0.6·L3, without crossing groove vertices.
- The code asserts that every selected vertex is in the documented set.

**Result: WN = 778 vertices**, of which 69–92 are on each digit. The removed vertices keep their W0 rows:
- the groove ring: 15–27 per digit;
- fold skin beyond the groove: 10–16 per digit.

The groove is open distally, so the plate keeps the documented distal limit. There is no free-edge groove in the sculpt. Per-digit vertex IDs, the bone, the removed IDs, the groove-ring IDs and every per-vertex before/after row are in `weights/weights_WN_log.json`. The same data for the uncorrected set is in `weights/weights_WNcap_log.json`.

### 2.3 Bit identity, normalisation and hashes

| Array | Selected | Non-selected rows bit-identical to W0 (float32 bytes) | Selected row sums | Negative | max \|Δ\| | weights sha256 |
|---|---|---|---|---|---|---|
| **WN** | 778 | 169,688 / 169,688 ✔ | 1.0 / 1.0 | 0 | 0.027 | `34136743…7982` |
| WNcap (record) | 1,105 | 169,361 / 169,361 ✔ | 1.0 / 1.0 | 0 | 0.052 | `b66817cf…c51f` |

Only the selected rows were normalised. No wrist, palm, thumb-base or transition edits were made.

### 2.4 Full 43-pose suite

Setup:
- Rig v001 matrices, v002 pivots, the same poses and an unchanged `diag_run.py`.
- W0 was re-run in this cycle, and it reproduces the 9703fd2 results for all 43 poses exactly.
- Files: `diag/diag_results_full_{W0,WN,WNcap}.json`, `diag/judge_W0_vs_WN*.{json,md}`.

| | W0 | WN | WNcap |
|---|---|---|---|
| poses passing | 20/43 | 20/43 | 20/43 |
| regressions (newly failing criteria) | — | none | none |
| criteria fixed | — | none | nail rigidity in D4_l_fist and D5_l_oppose_pinch |
| any retained metric changed | — | none at table precision | D4_l_fist: p95 41.4 → 42.2 %, zone −17.15 → −17.16 %; D5_l_oppose_pinch: zone −4.43 → −4.42 % |

D4_l_fist and D5_l_oppose_pinch still fail other criteria under all three arrays.

### 2.5 Nail residuals (Kabsch rigid-fit residual, mm)

The retained criterion is ≤ 0.3 mm on the original cap mask. The mask is not relabelled. The plate-subset values are recomputed from the posed meshes.

| Pose / digit | W0 cap mask | WN cap mask | WNcap cap mask | W0 plate | WN plate |
|---|---|---|---|---|---|
| fist index | 0.607 | 0.607 | 0.000 | 0.000 | 0.000 |
| fist middle | 0.549 | 0.549 | 0.000 | 0.0004 | 0.000 |
| fist ring | **0.714** | **0.714** | 0.000 | 0.000 | 0.000 |
| fist pinky | 0.557 | 0.558 (+0.0016) | 0.000 | 0.0115 | 0.000 |
| pinch thumb | 0.442 | 0.442 | 0.000 | 0.000 | 0.000 |

**Where the W0 cap-mask residual lives** (per-vertex deviation from the cap's best rigid fit, fist; `diag/nailskin_*.json`):

| Region | Deviation |
|---|---|
| plate | ≤ 0.12 mm |
| groove ring | 0.33–0.41 mm |
| fold skin beyond the groove | **0.55–0.71 mm** |

Pinch thumb: plate 0.09, groove 0.23, fold 0.44 mm.

**Demonstrated:** the plate is rigid under W0. The cap-mask failure is fold-skin bending inside the mask.

### 2.6 Surrounding skin

Measured on the skin ring within 1 cm outside the cap, never in the cap.

| | W0 | WN | WNcap |
|---|---|---|---|
| fist p95 \|strain\| index / middle / ring / pinky (%) | 22.7 / 24.1 / 24.3 / 27.1 | identical | **27.1 / 29.7 / 31.3 / 34.2** |
| fist max dihedral change | 6.8–8.0° | identical | identical |
| pinch thumb p95 strain / max dihedral change | 21.2 % / 5.7° | identical | 22.2 % / **20.1°** |

Sheet: `sheets/N_nail_fist_pinch.jpg` (fist index and ring, pinch thumb; W0 / WN / WNcap; dorsal and oblique; wire; plate and cap sets outlined; identical cameras).

### 2.7 Adoption decision

- **WN — not adopted.**
  - It shows no demonstrated rigidity improvement at the retained criterion. The only change is ≤ 0.012 mm on one plate that W0 already holds rigid.
  - It has no new failures.
- **WNcap — rejected.**
  - It passes the criterion only by binding the periungual skin, which §2.2 removed.
  - Its surrounding-skin artifact is demonstrated: strain +4.4–7.1 pp, and the 20° thumb fold.

Both arrays and their hashes are preserved. **The elbow parent is therefore W0.**

## 3. Left elbow only (§4)

### 3.1 Construction

Source: `elbow_weights.py`; logs in `weights/weights_E{1,2}_log.json`; maps in `weights/weights_E{1,2}_maps.npz`.

**Parent and fixed elements**
- Parent: W0.
- The pivot (v002 elbow), skeleton, geometry and poses are fixed.

**Support region**
- `arm_l` vertices within 13 cm of the elbow pivot.
- Kept as one connected component: 8,209 vertices.
- A 5-vertex `arm_l` island at the axilla side was excluded and logged.

**Taper**
- α = 1 in the core (≤ 9 cm: 4,425 vertices).
- Across the boundary band (9–13 cm: 3,784 vertices), α goes from 1 to 0 by smoothstep of the distance.
- α = 0 outside the band.

**Target re-split**
- Only the upperarm_l / forearm_l pair is re-split.
- Pair total P is kept; every other bone's weight is untouched.
- forearm = P · smoothstep(0.5 + 0.5·s/h), where s is the signed distance along the elbow bisector axis.
- **E1:** h = 4.5 cm all round. This regularises the bone-heat split, which spreads 0.17–0.53 at one axial slab.
- **E2:** h = 6.0 cm on the flexor (anterior, inner-crease) side and 3.0 cm on the olecranon side, cosine-interpolated around the axis.

**Final blend**
- W = W0 + α·(Wt − W0), a convex combination of two normalised, non-negative rows. Outside the support, rows are copied bit-identical.

How continuity is enforced:
- α is C¹ in distance and reaches exactly 0 at the band edge.
- The target split is a C¹ function of position.
- No hard cutoff is followed by local smoothing.

| Check | E1 | E2 |
|---|---|---|
| changed vertices (all inside the support) | 4,269 | 4,269 |
| max \|Δ\| upperarm_l / forearm_l / any other bone | 0.114 / 0.114 / 0.0 | 0.190 / 0.190 / 0.0 |
| row-sum change (max) / negative weights | 3·10⁻⁸ (float32) / 0 | 3·10⁻⁸ / 0 |
| non-support rows bit-identical | ✔ | ✔ |
| max per-edge change in Δ: core / band / edges crossing the support boundary | 0.074 / 0.021 / **0.000** | 0.065 / 0.021 / **0.000** |
| max \|Δ\| in the outer 1 cm of the band | 0.000 | 0.000 |
| weights sha256 | `c5306f3f…ef18` | `73630236…f416` |

Sheet: `sheets/E_weight_maps.jpg`, rest pose, front / back / lateral views. It shows:
- the W0 forearm weight;
- the support α with the band tinted;
- per-bone forearm weight and Δ for upperarm_l and forearm_l;
- total |Δ|;
- the max per-edge Δ change.

The largest per-edge Δ change (0.074 for E1) is a single core spot on the olecranon side, where the bone-heat split is locally irregular.

### 3.2 Tests

Setup:
- Poses: reference `D2_l_base_abd45`, then flexion 45 / 90 / 130, all from the disclosed abd45 shoulder setup.
- Return to rest: `rest_return_T1_mm` = 0.0000 for every pose and candidate.
- Sentinels: D1_l_abd90, D1_l_flex90, D3_l_flex60, D3_l_ext60, D4_l_fist, D5_l_oppose_pinch.
- LBS: numpy, identical to Blender. DQS: Blender preserve-volume on derived copies carrying identical arrays.
- Run: `run_elbow.sh`. Table: `diag/elbow_table.md`.

Each cell gives: non-contact intersections / crease intersections (crease depth, mm) / orientation disagreement / p95 strain % / loop-spacing ratio.

| Pose | Method | W0 | E1 | E2 |
|---|---|---|---|---|
| 45° | LBS | 0 / 0 / 0 / 33 / 0.65 | 0 / 0 / 0 / 41 / 0.60 | 0 / 0 / 0 / 39 / 0.65 |
| 45° | DQS | 0 / 0 / 0 / 36 / 0.69 | 0 / 0 / 0 / 44 / 0.61 | 0 / 0 / 0 / 39 / 0.67 |
| 90° | LBS | 0 / 116 (4.2) / 135 / 44 / 0.32 | 0 / 118 (5.6) / 157 / 58 / 0.32 | 0 / 95 (4.9) / **84** / 63 / 0.36 |
| 90° | DQS | 0 / 100 (3.3) / 125 / 62 / 0.40 | 0 / 113 (5.6) / 164 / 71 / 0.36 | 0 / 93 (3.7) / **19** / 69 / 0.44 |
| 130° | LBS | 173 / 112 (5.3) / 211 / 43 / 0.20 | 176 / 116 (6.5) / 232 / 58 / 0.18 | 176 / 110 (6.2) / 235 / 57 / 0.18 |
| 130° | DQS | 173 / 103 (4.8) / 257 / 70 / 0.20 | 176 / 117 (5.0) / 369 / 86 / 0.23 | 176 / 116 (5.0) / 295 / 78 / 0.28 |

Local fold/inversion indicator: 0 in every elbow cell, except W0 DQS 130°, which has 1.

**Criteria-level changes**
- The only newly failing criterion is the zone cone-volume proxy for E2 under DQS at 90° and 130°. It is reported as a historical proxy and was not used for selection.
- Otherwise every candidate fails exactly the criteria W0 fails.
- **Sentinels:** bit-identical metrics for E1 and E2 vs W0 under both methods. There is no leakage or regression.

**Penetration vs proximity** (`elbow_penetration.py`, `diag/elbow_penetration.json`)

| Measure | W0 | E1 | E2 |
|---|---|---|---|
| 130° non-contact pairs (both methods) | 173 | 176 | 176 |
| 130° non-contact depth max / p95 (mm) | 4.5 / 4.0 | 4.5 / 4.0 | 4.5 / 4.0 |
| 90° crease pairs, plane-depth max (mm), LBS | 3.8 | 4.9 | 2.8 |
| 2 mm proximity faces without intersection, 90° LBS | 35 | 64 | 102 |

- The 130° non-contact pairs are forearm flesh against biceps flesh, 9.6–16 cm from the pivot. Their depth is identical across all three arrays, so the penetration is independent of the elbow weights within this support.
- On the 90° crease, the plane-depth estimate shows E2 reducing penetration. The retained crease-depth metric instead rises from 4.2 to 4.9 mm. The two methods disagree, and this is reported as inconclusive.
- In the proximity count, E2 converts penetration partly into close contact without intersection.
- Expected anatomical proximity is therefore distinguished from demonstrated penetration: only BVH-overlap pairs are counted as penetration.

### 3.3 Selection

The order asks for selection by geometric integrity and visual quality across poses.

**E1 — not selected.** At 90° and 130° it is worse than W0 on orientation disagreement, crease depth and p95 strain under both methods, and adds 3 non-contact pairs at 130°. Its loop ratio is equal at 90° LBS (0.323 vs 0.321) and lower everywhere else.

**E2 — not selected.**
- It improves 90° orientation disagreement, the 90° crease-pair count (116 → 95 LBS) and the 90° loop-spacing ratio.
- But it:
  - deepens the retained crease depth (90°: 4.2 → 4.9 mm LBS, 3.3 → 3.7 mm DQS; 130°: 5.3 → 6.2 mm LBS, 4.8 → 5.0 mm DQS);
  - adds 3 non-contact pairs at 130°;
  - increases 130° orientation disagreement (LBS 211 → 235, DQS 257 → 295);
  - raises p95 strain everywhere (90° LBS 44 → 63 %).
- In the flexion-plane sections, E2 enlarges the inner pocket loop at 130° and bulges the outer contour.
- Under the order's rule, a candidate that is better at one pose and worse at the deeper pose and on crease depth is not an improvement.

**The baseline is retained.** No full-suite rerun or v003-knee verification was triggered.

Sheets:
- `sheets/E_failures_D2_l_flex90.jpg` and `sheets/E_failures_D2_l_flex130.jpg`:
  - W0 / E1 / E2 × LBS / DQS with identical cameras;
  - inner crease, outer contour and side views, plus inner-crease wireframe;
  - failure IDs and the support boundary / band edge drawn;
  - failure-ID lists printed beside each row.
- `sheets/E_contour_crease.jpg`:
  - flexion-plane cross-sections at 90° and 130°, LBS and DQS, with W0 / E1 / E2 overlaid;
  - the outer (olecranon) contour on −x and the inner crease on +x; crossing lines are penetration;
  - LBS inner-crease close-ups with intersections and compressed-loop vertices.

WN is bit-identical to W0 on the whole arm, so its elbow renders are W0's. That is why no separate WN elbow row appears on the identical-camera sheets.

## 4. Metric and evidence policy (§5)

**Labels**
- "Orientation" is reported throughout as **skinned-reference-normal orientation disagreement**.
- Neighbour-normal opposition is reported as the **local fold/inversion indicator**.
- Neither is called a proven inversion.

**Representative flagged faces** (`sheets/I_flagged_face_inspection.jpg`, `face_inspect.py`): five W0 faces. Each panel shows:
- three posed views;
- an indexed wireframe with vertex IDs;
- both triangulations' areas, rest vs posed;
- the triangle-normal agreement;
- dihedral angles to the edge neighbours;
- the intersecting faces.

| Face | Pose | Demonstrated | Suspected / not demonstrated |
|---|---|---|---|
| 6720 | D2_l_flex90 | No inversion and no intersection. The quad is compressed to 37 % of its rest area. | Orientation disagreement only: the face is consistent with its neighbours (dot +1.00) but turned −0.19 from rest — a tilted, compressed sheet, not proven inverted. |
| 49521 | D2_l_flex130 | Self-intersection with 6 non-adjacent arm faces (the forearm–biceps penetration). | The face itself is unfolded and at full area. |
| 9092 | D4_l_fist | Local fold (dihedral 127–128° to two neighbours). The quad has collapsed to 9 % of its rest area. | Its normal is still within 90° of rest (+0.70). |
| 1919 | D6_l_flex90 | The quad itself is folded: its triangles oppose (−0.97 / −0.99). Dihedral 152–153°, intersecting one crease face. | — |
| 48669 | D1_l_flex90 | Self-intersection with 2 faces, without fold or inversion. | — |

**Cone-volume proxy**
- Kept as a historical proxy, with its reference sensitivity disclosed: a 1 cm reference shift moves it by −7.8 / +2.2 / −4.4 % at the shoulder, ≤ 0.7 % at the elbow, −3.6 % at the hip and ≤ 0.6 % at the knee.
- It was not used for selection.

**Rigid sanity check, re-run this cycle** (root rotated 30°): 0 intersections, 0 orientation disagreements, 0 local inversions, 0 new folds, strain 1·10⁻¹⁰ %, zone proxies 0.000 % (`diag/metric_check_v003cycle.json`).

**Masks:** original contact masks and classifications, unchanged. No pass was relabelled.

## 5. Evidence index (`reviews/rac-rp2-evidence/grask_rig_diagnostic_v003/`)

1. `hashes/` — before and after hashes (identical). `rig/` — the v003 manifest, `rig_v003.json`, the custom properties, and the build logs of the transient DQS copies.
2. `weights/weights_WN*` — the corrected plate array, log (IDs, bone, per-vertex deltas, removed and groove IDs), changed-ID list and selection diagnostics. `weights/weights_WNcap*` — the same for the documented-set record.
3. `weights/weights_E{1,2}*` — the arrays, logs (method, support, band, boundary checks, hashes) and per-vertex maps (α, Δupperarm, Δforearm, per-edge Δ change, support mask).
4. `diag/` — results and IDs:
   - full-suite results for W0 / WN / WNcap with their judge tables and JSON;
   - elbow results for W0 / E1 / E2 × LBS / DQS with the elbow table, judgement and penetration;
   - nail skin checks and the rigid metric check;
   - per-pose failure-ID files (`ids/`);
   - one-line summaries.
5. A full-suite regression check for a selected elbow candidate is not applicable: none was selected.
6. `sheets/` — `N_nail_selection_documented_cap_overview`, `N_nail_selection_cap_vs_plate`, `N_nail_fist_pinch`, `E_failures_D2_l_flex90`, `E_failures_D2_l_flex130`, `E_contour_crease`, `E_weight_maps`, `I_flagged_face_inspection`.

Reproduce, with the cloud workspace `/tmp/claude-0/rt/r3`:
1. Run `weights_nail.py … WN plate` and `weights_nail.py … WNcap cap`.
2. Run the WN and WNcap full suites with `diag_run.py`, `TAG=_full_{W0,WN,WNcap}`.
3. Run `pair_judge.py`.
4. Run `nail_skin_check.py`.
5. Run `elbow_weights.py … E1 uniform` and `elbow_weights.py … E2 crease`.
6. Run `run_elbow.sh`, then `elbow_judge.py` and `elbow_penetration.py`.
7. Run `elbow_sheets.py`, `nail_plate_inspect.py` and `face_inspect.py`.

## 6. Qualified conclusions

**1. Nail plates**
- The nail plates already move rigidly under bone-heat W0.
- The retained nail-rigidity failure is a property of the documented cap mask, which includes nail-fold skin.
- Binding that skin rigidly "passes" the metric but demonstrably pushes strain and a new fold into the neighbouring skin.
- Binding the plate alone changes nothing measurable.

**2. Left elbow**
- A continuous, connected, tapered re-split of the upperarm/forearm pair cannot improve geometric integrity at both 90° and 130°.
- A crease-biased split trades 90° orientation disagreement for deeper crease penetration, more strain, and a worse 130°.
- The forearm–biceps penetration at 130° (4.5 mm) is unchanged by any weight change in this support.
- This is consistent with the 9703fd2 finding that weights alone do not resolve the elbow under LBS or DQS. It does not prove that topology or correctives are required.

**3. Unchanged, unexempted failures:** the persistent elbow loop compression (`elbow_l_21|22`, ratio 0.18–0.32) and the crease depth (4.2–6.5 mm).

## 7. Decisions for review

- **N-1** Nail criterion mask.
  - The retained mask includes periungual skin.
  - Options: keep it as is (W0 fails, and only skin-binding can pass), or adopt the groove-bounded plate mask (W0 passes, 0.000–0.012 mm) as a new, separately labelled criterion.
  - Either way, no retroactive relabelling of past results.
- **N-2** WN status: discard it, or keep it as a no-op record. WNcap stays rejected.
- **E-1** Accept that the left-elbow weights-only experiment is exhausted within the two-candidate limit.
  - The next evidence options are outside this order: a pose-space corrective or helper-bone study, an LBS/DQS hybrid, or a topology loop-density check at `elbow_l_21|22`.
- **E-2** Classification of the 130° forearm–biceps overlap.
  - It is same-part self-contact 10–16 cm from the pivot, currently counted as non-contact.
  - Any reclassification would need an explicit, new, pre-declared contact rule, not a relabel.
- **E-3** Whether E2's 90°-only gain (orientation disagreement 135 → 84 LBS, 125 → 19 DQS) merits a later bounded study in combination with a corrective, rather than as weights alone.

**STOP FOR CHATGPT REVIEW.**
