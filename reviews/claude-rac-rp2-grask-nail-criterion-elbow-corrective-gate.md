# RAC RP2 — Grask nail criterion and elbow corrective recovery — gate return

**Date:** 2026-10-26
**Order:** `reviews/chatgpt-rac-rp2-grask-nail-criterion-elbow-corrective-recovery-order.md` (6c38d75)
**Parent return:** 44e1ec6

## RETURN STATUS

**RP2 GRASK ELBOW CORRECTIVE RECOVERY PASS / NEXT DEFORMATION FAILURES READY FOR TRIAGE**

What this status means:
- The left corrective (C2) passes every §17 selection check.
- A right counterpart was built and tested.
- The full 43-pose suite shows no regression, and every pose with the corrective inactive is bit-identical to W0.

What it does not mean:
- It does **not** accept Grask production deformation.
- Retained failures remain at the elbow and elsewhere (see §9).
- Three items need an author ruling (§10):
  - closed volume is not preserved at deep flexion;
  - the LBS-designed keys regress crease depth under DQS at 130°;
  - the right side needed a 21 cm support.

**Evidence:** `reviews/rac-rp2-evidence/grask_rig_diagnostic_v004/`
**Tools:** `tools/rac/rp/grask_rigprep_v001/`. New this cycle:
- `corr_solve.py` — the solver;
- `run_corr.sh`, `run_v004.sh` — evaluation runs (`run_v004.sh` reproduces the whole cycle);
- `corr_blend.py` — Blender shape keys and drivers;
- `corr_judge.py`, `full_judge_v004.py`, `corr_field_check.py` — judging and field checks;
- `topo_audit.py`, `hash_all_v004.sh`, `make_v004.sh`, `v004_sheets.py` — audit, hashes, blend build, sheets.

Evaluator changes this cycle:
- `diag_run.py` gained the Nail Plate Rigidity v2 mask and optional `CORR` (a rest-space shape-key delta applied before skinning).
- `judge.py` gates on v2 whenever a result carries it.
- `diag_lib.py` gained env-gated poses: `ELBOW_ARC` (60 / 75 / 110 / 120°) and `ELBOW_SET_R` (right arc).
- The 43-pose suite itself is unchanged.

## 1. Rulings recorded (from the order)

| Item | Ruling |
|---|---|
| N-1 | **Nail Plate Rigidity v2** (groove-bounded plate mask, ≤ 0.3 mm Kabsch max deviation) gates every new run. **Nail Cap Historical v1** (the old distal cap, which includes periungual fold skin) is report-only. The cap criterion is *superseded*, not "passed". No retroactive relabel. |
| N-2 | W0 remains the baseline. WN is kept as a no-op record. WNcap stays rejected. |
| E-1 | Weights-only left-elbow work is exhausted; no further re-splits. |
| E-2 | The 130° forearm–biceps overlap stays a failure; no reclassification. |
| E-3 | E2 is not adopted; its 90° gain is design evidence only. |

## 2. Immutable parents

**Before:** `hashes/hashes_before.txt` (PC re-staged at start). **After:** `hashes/hashes_after.txt` (PC re-staged at end). The two are **identical**.
- v003 `03bfe7d9…7ce0` / geometry `f9c4a7ac…702f`.
- v005 `7bba8d2d…ab14` / geometry `2697929d…d7bc`.
- All sidecars, the freeze record and the retopo v001 / v002 records.
- rigdiag v001 `59ca4fda`, v002 `9e2d078a`, v003 `4ab743fe`.
- W0 / W1 / W2 / WN / WNcap / E1 / E2: file and array SHA unchanged.

There were no rest-mesh, topology, vertex-count, face-count, UV, material, LOD or UE5 changes.

## 3. Derived diagnostic file — `E:/…/RP2/DIAG/GR_U_REF_RP2_rigdiag_v004.blend`

| Property | Value |
|---|---|
| File SHA-256 | `859b1e8635688230acbcbb4df87727d03a812ba902f5e4fd665d726097dbb255` (PC copy re-staged: identical) |
| Rest (Basis) geometry | `f9c4a7ac…702f` = frozen v003 (also read back from the PC copy) |
| Skeleton | 86 bones / 83 deforming. Names, deform order and `matrix_local` are identical to rig v001 (max diff 0.0). Matrix SHA `0e3da2cf…99e6c` |
| Weights | W0, read back **bit-identical** (array SHA `2189375b…df2e`) |
| Landmarks | v002 |
| Corrective | Six shape keys `RAC_DIAG_elbow_{l,r}_flex{90,110,130}`; full-array SHAs are in `rig/props_v004.json` |

Each shape key is driven by a Blender **simple-expression** driver (no Python auto-run needed). The left 90° key, for example, uses `smoothstep(45, 90, abs(degrees(r))) - smoothstep(90, 110, abs(degrees(r)))`, where `r` is `forearm_s` local ROT_X (swing-twist).

The file is tagged DIAGNOSTIC / non-production.

**Production-mechanism proof:** the Blender armature modifier plus the driven shape keys reproduces the evaluator's posed mesh to ≤ 0.0006 mm (float32). This holds for 11 poses: left and right arcs, plus D1 / D3 / D4 with the keys at 0 (`rig/v004_checks.json`).

The corrective is therefore a practical shape-key mechanism that leaves the frozen rest mesh untouched.

## 4. Nail criterion implementation (§12)

Every new result carries:
- `nail_plate_v2_mm` (gating);
- `nail_cap_historical_v1_mm` (report-only; periungual skin included).

| Pose | Nail Plate v2 (max mm) | Nail Cap Historical v1 (mm) |
|---|---|---|
| W0 D4_l_fist | index 0.000, middle 0.003, ring 0.000, pinky **0.069** | 0.61 / 0.55 / 0.71 / 0.56 |
| W0 D5_l_oppose_pinch | thumb 0.000 | 0.44 |

v2 passes in both poses.

Mask sanity sheet: `sheets/N_nail_mask_sanity_plate_v2_vs_cap_v1.jpg`. It shows the plate, the groove ring, the excluded fold and tip skin, and the original cap, in four views per digit.

Full-suite counts:
- W0 passes 20/43 under v2 and 20/43 under historical v1.
- D4 and D5 fail other criteria either way.

## 5. Topology-density audit — analysis only (§13)

Files: `topology/topology_density_audit.json`, `sheets/V_topology_audit.jpg`.

**Method.** I walked rings by quad strips from the tagged `LOOP_elbow_l_22`. That gave 123 closed edge rings across the arm, from s = −17.7 to +32.2 cm along the elbow bisector axis.

**Topology quality**
- Every ring in the flexion zone has 120 vertices, all valence 4.
- There are no poles. Along-ring edges are 0.25–0.29 cm.

**Density**

| Location | Rest spacing |
|---|---|
| Upper arm toward the elbow | 0.33 cm |
| Rising through the crease | 0.36 (21) → 0.48 (22) → 0.55 cm |
| Forearm | ≈ 0.58 cm |
| Dense band at s ≈ −10 cm | 0.14 cm |
| Flexion zone (±6 cm) | 25 rings |

The tagged loops `elbow_l_18…22` are every 4th ring (≈ 1.2–1.6 cm apart).

**Where W0 LBS compresses**
- Only 2–3 rings either side of the pivot: P1 / 22 at s ≈ −2 cm, and D5 at +0.9 cm. Their minimum posed/rest ratio is 0.12–0.19.
- Neighbouring rings stay at ≥ 0.85.

**Mechanism.** The topology has no shortage of rings. The collapse comes from the localised LBS transition, which is consistent with the corrective restoring loop spacing to 0.60 using the same rings.

The audit does **not** demonstrate a topology limitation at the elbow.

There is one notable feature: the density step from 0.33 to 0.58 cm sits exactly at the crease. It is reported for the author; it does not block anything.

## 6. Corrective method and candidates (§5–§9)

### 6.1 Mechanism

Each keyed angle has a rest-space delta **D_k** = Lin_v⁻¹ (X\*_k − LBS(V0)). Here Lin_v is the per-vertex LBS linear part, so LBS(V0 + D_k) = X\*_k exactly. This is a shape key applied before the armature.

- Key poses are **elbow flexion only**. The test poses' abd45 shoulder base is removed, so the keys carry no shoulder correction.
- Keys sit at 90 / 110 / 130°. The driver is a smooth (C¹) smoothstep partition:
  - 0 at rest and up to 45°;
  - 90° key 0.259 at 60° and 0.741 at 75°;
  - 120° = 0.5 / 0.5 between the 110° and 130° keys;
  - the 130° key holds beyond 130°;
  - the weights return smoothly to 0 on extension.
- Curve: `sheets/V_driver_curve.jpg`. Tested activations: `diag/driver_curve_and_activations.json`.

### 6.2 Target X\*_k (projective least squares, `corr_solve.py`)

1. **Delta-mush base.** 15 smoothing iterations inside the support, with the rest detail re-applied in local frames. This un-crumples LBS.
2. **Harmonic correction.** The Laplacian of X equals the Laplacian of the base.
3. **Anchoring.** (1 − τ) anchoring in the taper band.
4. **Side-vs-side contact.** Upper-arm flesh against forearm flesh, using W0 forearm share > 0.5:
   - contacts are detected by signed distance to the other side's surface;
   - only facing surfaces, rest separation ≥ 1 cm, depth ≤ 1.5 cm;
   - push share 0.5, ≤ 2 mm per iteration, persistent targets.
5. **Contact at 110 / 130°.** Inner-side flesh beyond 6 cm from the pivot is held on its own side of the posed bisector plane of the joint angle. This flattens the forearm–biceps contact interface.
6. **Loop floor.** The retained metric's own loop pairs are kept at ≥ 0.6× their rest distance.
7. **Local-inversion fairing.** Persistent neighbour-mean targets for faces flagged by the local fold/inversion indicator.
8. **Final local repair.** Up to 30 relaxation passes on still-flagged faces.

### 6.3 Support

- One connected `arm_l` region within 18 cm of the pivot: 11,534 vertices (core ≤ 14 cm 9,036; band 2,498). One 5-vertex island was dropped.
- τ is a C² smootherstep taper from 14 to 18 cm.
- An **exact-zero guard** multiplies the delta:
  - 1 cm radial;
  - × 1.5 cm surface (geodesic) distance from *any* support boundary, including the arm/torso and arm/hand **part seams**.
- The support touches a part seam on 37 edges (left) and 55 (right). Without the guard, the first run left a non-zero step there. It was caught in the field audit, fixed, and everything was re-run.

**Field statistics** (`diag/corr_field_C2.json`, `sheets/V_corrective_field.jpg`)

| Key | max \|D\| | outside support | outer 1 cm of band | gradient max core / band / boundary edges |
|---|---|---|---|---|
| K90_l | 0.78 cm | 0 | 0 | 1.05 / 0.003 / 0.000 |
| K110_l | 3.07 cm | 0 | 0 | 2.05 / 0.056 / 0.000 |
| K130_l | 3.23 cm | 0 | 0.24 cm | 3.54 / 0.70 / 0.000 |

Gradient is |ΔD| per cm of rest edge. The 130° key reaches the band because the forearm–biceps contact extends to 16.4 cm.

### 6.4 Candidates

All candidates use identical pivots, W0, poses and metrics. Configs are in `config/`.

| Candidate | Definition |
|---|---|
| **C1** | Delta-mush + contact (no loop floor, no fairing / repair) |
| **C2** | C1 + loop floor + inversion fairing + final repair |
| **C3** | C2 + volume restoration: a smooth outward bump on the medial / lateral elbow returning 25 % of the corrective's closed-volume loss |

C2 was refined internally once: the loop floor went from 0.55 to 0.6, to keep 120° (interpolated) at ≥ 0.5. The r1 config is kept.

Before the three candidates, the solver itself was developed through several internal variants, all of which were discarded:
- face-plane contact pushes and KD contacts, which diverged or folded at 130°;
- a rotated-rest-detail Laplacian;
- solved keys at 110° without the plane;
- a full volume restoration.

## 7. Results — left elbow, LBS

Files: `diag/corr_tables.md`, `diag/corr_judgement.json`.

Each cell gives:
- non-contact / crease intersections (crease depth, mm);
- orientation disagreement / local fold-inversion indicator;
- loop min / p95 strain %;
- closed-volume change caused by the corrective (cm³).

| Angle | W0 | C1 | **C2 (selected)** | C3 |
|---|---|---|---|---|
| 45 | 0/0 · 0/0 · 0.65 · 33 | identical (activation 0) | **identical, bit-for-bit** | identical |
| 60 | 0/38 (0.6) · 20/1 · 0.53 · 40 | 0/0 · 0/0 · 0.53 | **0/0 · 0/0 · 0.59 · 40 · −7** | 0/0 · 0/0 · 0.58 |
| 75 | 0/80 (2.9) · 85/2 · 0.42 · 44 | 0/0 · 0/0 · 0.41 | **0/0 · 0/0 · 0.57 · 43 · −20** | 0/0 · 0/0 · 0.54 |
| 90 | 0/116 (4.2) · 135/0 · 0.32 · 44 | 0/0 · 4/0 · 0.32 | **0/0 · 0/0 · 0.60 · 46 · −27** | 0/0 · 0/0 · 0.54 |
| 110 | 69/109 (4.0) · 188/0 · 0.23 · 40 | 0/115 (6.0) · 79/2 · 0.21 | **0/71 (3.1) · 59/0 · 0.60 · 57 · −119** | 0/82 (5.9) · 45/0 · 0.44 |
| 120 | 124/104 (4.5) · 202/0 · 0.20 · 42 | 0/176 (2.7) · 94/1 · 0.22 | **0/67 (1.9) · 45/0 · 0.54 · 56 · −218** | 0/59 (3.8) · 61/2 · 0.33 |
| 130 | 173/112 (5.3) · 211/0 · 0.20 · 43 | 0/199 (5.1) · 158/4 · 0.20 | **0/41 (3.2) · 93/0 · 0.60 · 56 · −319** | 0/71 (4.0) · 115/0 · 0.23 |

**Failing retained criteria**

| | 60 | 75 | 90 | 110 | 120 | 130 |
|---|---|---|---|---|---|---|
| W0 | 2 | 4 | 4 | 5 | 5 | 5 |
| C2 | 1 | 1 | 1 | 3 | 2 | 3 |

C2 has **no newly failing criterion at any angle**. What remains:
- 60–90°: the zone cone-volume proxy only;
- 110°: orientation, zone proxy and crease depth (3.1 mm);
- 120°: orientation and zone proxy;
- 130°: orientation (93), zone proxy and crease depth (3.2 mm).

**C2 §17 checks** (`selection_checks_C2`), all true:
- no newly failing criterion;
- 45° identical;
- 90° integrity improves;
- 130° improves (non-contact, crease depth, orientation, loop);
- no new local fold/inversion indicator faces at any angle (0 everywhere; W0 had 1–2 at 60–75°);
- no folds outside the crease;
- rest-return T-1 = 0.

**Why C1 and C3 lose**
- C1 does not fix the loops. It also introduces local inversions at 110–130° (2 / 1 / 4) and deepens the crease at 110° (6.0 mm).
- C3's bulge restores some volume but drops the loops below 0.5 at 110–130° (0.44 / 0.33 / 0.23). It deepens the crease at 110° and adds inversions at 120°.

**C2 selected.**

**Disclosed costs of C2**
- **In-crease folds (dihedral > 120°)** rise from +4…+6 to +16…+41. They sit in the crease zone, where the criterion allows them.
- **They do not hide penetration.** At 90° there are 0 intersections and 0 orientation disagreements, the folds lie along the crease line, and there are no local inversions.
- **Zone strain is higher:** p95 46–57 % (W0 40–44 %); max edge strain 92–130 % (W0 93 %).
- **Volume loss — not preserved, see §10.**
  - The zone cone-volume proxy goes from −16.5…−27.9 % to −21…−44 %.
  - The **closed-mesh volume falls by 27 cm³ at 90° and 319 cm³ at 130°**, caused by flattening the forearm–biceps contact interface.
  - C3 shows that restoring it with a side bulge degrades the loops and crease.

### Visuals

**Identical cameras** (`sheets/V_elbow_45.jpg`, `V_elbow_90.jpg`, `V_elbow_130.jpg`)
- W0 vs C2, under LBS and DQS.
- Views: inner crease, outer (olecranon) contour, front three-quarter, inner-crease wireframe close-up.
- Overlays: non-contact / crease / fold / orientation / inversion / compressed-loop IDs and the support boundary and band edge, with ID lists printed.

**Sections** (`sheets/V_sections.jpg`)
- Flexion-plane cross-sections at 90° and 130°, LBS and DQS, W0 vs C2, with BVH-intersecting faces drawn thick.
- **The LBS outer contour is nearly unchanged.** Outer-side vertices within 10 cm of the pivot move p95 2.5 / max 3.9 mm at 90° and p95 3.1 / max 5.0 mm at 130°. Under DQS at 130° they move p95 5.9 / max 11.6 mm.
- **The inner pocket closes** at 130°: W0's open crease pocket becomes a flat contact interface. This is the expected proximity, now with no penetration.

## 8. DQS, right side, knee, full suite

### 8.1 LBS vs DQS (§10)

The same keys and activation are applied as Blender shape keys under preserve-volume (`diag_results_c_dqs_*`).

**Where C2 helps under DQS (60–120°)**
- Non-contact pairs go to 0 everywhere (W0 70 / 124 / 173 at 110 / 120 / 130°).
- 60–90° becomes clean: 0 intersections and 0–1 orientation faces.
- Orientation at 110 / 120° drops from 194 / 214 to 77 / 116.

**Where it regresses (130°)**
- Crease depth **9.8 mm** vs 4.8 mm.
- Orientation 268 vs 257.
- 3 local-inversion faces vs 1.
- The outer contour moves inward by up to 11.6 mm (p95 5.9 mm).
- The DQS zone proxy, which is +1.7 % under W0 DQS, becomes −4.4 to −13.6 %. That triggers the "zone volume ±3 %" criterion at 90–130°.

**Reading.** The keys are skinning-method specific: they were solved against LBS. They do not fail catastrophically under DQS, but a DQS policy would need its own keys. No skinning policy is selected here.

### 8.2 Right elbow (§11)

**Mapping check.** The mirror mapping is not valid: the nearest-vertex residual after x-mirroring is median 5.6 mm and max 47 mm. The right-solved keys also differ from the mirrored left keys: K130 RMS 3.9 mm, max 33 mm (`corrective/mirror_compare.json`).

So the right counterpart was **solved on the right geometry** with the same class and parameters (C2r, 18 cm).

| Right side | W0 | C2r (18 cm) | **C2rx (21 cm, selected right)** |
|---|---|---|---|
| 60–75° | 2 / 4 fails | 1 / 1 | 1 / 1 |
| 90° | 0/126 (3.9) · 156 · 0.38 | 0/0 · 15 · 0.60 | same |
| 110° | 107/105 · 214 · 0.31 | 0/6 (1.3) · 19 · 0.59 | same |
| 120° | 160/106 · 224 · 0.29 | 0/22 (1.7) · 22 · 0.50 | same |
| 130° | 205/109 (3.1) · 230 · 0.31 | **174**/52 (3.1) · 79 · 0.46 | **0**/52 (3.1) · 79 · 0.46 |

- **Why the support grew.** The right forearm–biceps contact reaches **19.9 cm** from the pivot, against 16.4 cm on the left. This is a real asymmetry. The 18 cm support cannot reach it, so C2rx extends the support to 21 cm (core 17 cm). That exceeds the "about 18 cm" suggestion and is disclosed here.
- **What is left at 130°.** The loop ratio is 0.46 (fails; W0 0.31). Crease depth equals W0 (3.1 mm).
- **Rejected tweak.** A stronger loop weight passes the loop check but deepens the crease to 5.3 mm, so it was not used.
- **Result.** The right side has no new failure and fixes 1–3 criteria per angle.
- Sheet: `sheets/V_right_elbow.jpg`.

### 8.3 Knee verification (§14)

W0, corrective inactive (D7 has no elbow flexion).

**Landmark difference**

| Knee | v003 − v002 | Compliance |
|---|---|---|
| knee_l | (−0.97, +2.58, 0) mm = **2.75 mm** | v003 sits at exactly the 5.0 mm AD-R2 cap against the v001 consensus; compliant |
| knee_r | 0.83 mm | The suite has no right-knee poses, so it is not tested |

**Deformation** (unrestricted v002 → bounded v003)

| Pose | Non-contact | Crease depth | Orientation | Local inv | Zone proxy | Contacts |
|---|---|---|---|---|---|---|
| D7_l_flex90 | 0 → **3** | 6.9 → 7.0 mm | 192 → 209 | 2 → 1 | −25.0 → −27.3 % | — |
| D7_l_flex140 | — | — | 283 → 297 | — | −44.2 → −45.7 % | 270 → 285 |

The bounded v003 knee **does not improve deformation and adds 3 non-contact intersections**. It is **not promoted**; v002 remains the diagnostic baseline. Files are in `knee/`.

### 8.4 Full-suite regression gate (§15)

W0 baseline vs W0 + selected corrective (left C2 + right C2rx), v002 pivots, Nail Plate v2 gating, 43 poses (`diag/full_suite_judgement_v004.json`, `diag/full_suite_table_v004.md`).

| Check | Result |
|---|---|
| Passes | 20/43 → 20/43 |
| Regressions | **none** |
| Corrective active | only D2_l_flex90 and D2_l_flex130 |
| Fixed criteria, D2_l_flex90 | crease depth, loop spacing, orientation (135 → 0) |
| Fixed criteria, D2_l_flex130 | non-contact (173 → 0), loop spacing |
| The other 41 poses (activation 0) | **bit-identical posed meshes** |
| Unexpected unrelated changes | none |

The 45° and intermediate elbow angles were run as supplemental diagnostics (§7), not as replacements.

## 9. Exact unresolved failures after this cycle

**Left elbow, C2, LBS**
- 90°: zone proxy (−21.0 %).
- 110°: orientation 59, zone proxy, crease depth 3.1 mm.
- 120°: orientation 45, zone proxy.
- 130°: orientation 93, zone proxy, crease depth 3.2 mm.

**Right elbow, C2rx**
- 90–120°: orientation 15–22, zone proxy.
- 130°: orientation 79, zone proxy, crease depth 3.1 mm, loop ratio 0.46.

**Rest of the suite: unchanged W0 failures (23 poses)**
- Shoulder: D1 abd / flex and the girdle variants.
- Wrist D3; fist D4 (crease and orientation); thumb D5.
- Hip D6, knee D7, ankle and toes D8.

These are now ready for triage.

## 10. Decisions for review

- **C-1 Volume.**
  - C2 removes 27–319 cm³ of closed volume from 90° to 130° by flattening the contact interface.
  - The zone proxy is worse: −44 % vs −28 % at 130°.
  - A side-bulge restoration (C3) damages the loops and crease.
  - Should volume be (a) accepted as contact flattening for the diagnostic, (b) addressed by a later bounded volume-preserving corrective (for example a bulge solved jointly with the loop constraints), or (c) treated as pointing to a helper-bone study?
- **C-2 DQS.** The LBS-solved keys regress the 130° crease depth under DQS (9.8 vs 4.8 mm). Keys are method-specific, so the skinning policy decides which key set to author.
- **C-3 Right support.** The right side needs a 21 cm support because the contact reaches 19.9 cm. Accept the asymmetric extent?
- **C-4 Strain and crease folds.** p95 rises to 46–57 % and in-crease folds increase (allowed by the criterion). Acceptable for the diagnostic?
- **C-5 Next triage target.** The shoulder (D1 / girdle) and the fist / thumb (D4 / D5) carry the most remaining failures.
- **K-1** Keep v002 knees. The bounded v003 knee brings no improvement and adds 3 non-contact pairs.

No retopology edit, helper bones, production freeze, facial work, morphs, UVs or UE5 work.

**STOP FOR CHATGPT REVIEW.**
