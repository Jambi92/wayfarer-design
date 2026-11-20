# Saurin RP6 — Offline Bake Validation Report

**Order:** [chatgpt-rac-rp6-saurin-offline-bake-validation-order.md](chatgpt-rac-rp6-saurin-offline-bake-validation-order.md) (8e3b7b4d)
**Continues:** [per-body bake feasibility report](claude-rac-rp6-saurin-per-body-bake-feasibility-report.md) (evidence e2de557b)
**Evidence:** [`rac-rp6-evidence/saurin/rig_pilot/offline_bake/`](rac-rp6-evidence/saurin/rig_pilot/offline_bake/)
- results: `SA_RP6_offline_bake_results_v001.json`
- sha256 of every file: `SA_RP6_offline_bake_manifest_v001.json`

**Status:** **RP6 RIG PILOT / NOT FROZEN**

## Verdict

**All four roster bodies have a clean offline bake, and the rules found nothing left unresolved.** The roster is the order's fallback: BASE_c1, BASE_c2, and END_FAHI / END_MUFAHI as regression controls.

Every final artifact was reopened from disk and is clean on all of the following:
- **Gates:**
  - 34 anatomical poses × 4 fractions;
  - all 50 special gates × 4 fractions;
  - the full-suite sweep;
  - the gate sweep where one was needed;
  - neutral exactly 0;
  - rigid landmarks ≤ 0.0013 cm (limit 0.05).
- **Integrity:** frozen RP5 hashes, topology, semantic order, geometry, neutral and pose-range signatures.
- **Before / after:** every known unbaked failure was re-evaluated at the same body, pose and fraction. 89 were failing before and 0 after.
- **Two checks added during this order:**
  - a **dense between-sample audit** on a 0.0025 grid;
  - a **motion gate** that limits surface movement per animation frame.

**What it took:**
- **The base bodies** were clean after one adaptive refit in pass 2.
- **The endpoint controls each needed a documented per-body repair** (§3.4):
  - wider pose keys, because narrow ones made pops in motion;
  - refit samples from the dense audit, because the blend's own defect leaked between the sweep's samples.

Both added checks are my proposals, and so is the tail criterion in §6. **None is adopted until the author approves it.**

**Flagged for the author:**
- **No author-designated Saurin shipping roster exists** (§1).
- The first motion rule was revised during this order (§4.1); both verdicts are kept.

## 1. Roster and provenance (recorded before fitting, b6bcc437)

**No author-designated Saurin shipping preset roster exists in the repository.** I searched `register/`, `reviews/`, `docs/` and the RP6 evidence for shipping, designated or approved preset rosters and found none. **Flagged for the author.**

The order's fallback applies: both base configurations, plus FAHI and MUFAHI as regression controls for the known endpoint failures. The controls carry no shipping designation.

| Body | Role | Recipe | Body file sha256 |
|---|---|---|---|
| BASE_c1 | base c1 SA-M188 | config M, no state weight | `f79dd9d2ff5d148a…` |
| BASE_c2 | base c2 SA-F188 | config F, no state weight | `0a8e8a8ddb29a9dd…` |
| END_FAHI | regression control | config M, FAHI 1.0 | `cfd4d76700b4e2ac…` |
| END_MUFAHI | regression control | config M, MUFAHI 1.0 | `c4a9c82e3b790731…` |

Full hashes, the neutral vertex hashes and the pre-rig composition counts are in `SA_RP6_offline_bake_roster_v001.json`.

**Initialisation.** Every bake starts from `SA_RP6_creator_layers_v004.json` (sha256 `95fb5d6b…333c1`) on the exact body. It uses that body's base weights and joints derived on the body. The workspace is the verified clean RP5 workspace.

## 2. Method

The driver is `sa6_bake_full.py`, one independent worker per body. Every stage is resumable.

1. **Unbaked reference.** The full suite runs on the same body with an empty K, so baked equals the packaged blend v004. This reproduces the known failures.
2. **Fit (it0).** A bounded pose-driven fit starts from v004 on the exact body. The artifact is saved, reopened from disk, and checked with the full suite:
   - **EV:** 34 anatomical poses × 25/50/75/100 %, plus neutral.
   - **GT:** all 50 special gates × 4 fractions, plus neutral. The gates are in the first pass.
   - **SW:** the full-suite sweep. Heavy-joint and K poses are sampled at 0.025 and every other pose at 0.125. Samples sit ±0.25° around every active baked and initialisation-layer driver transition.
   - **GS:** every special gate that entered the fit, swept at 0.025 plus its transitions.
   - **MO:** the motion gate (§4.1).
   - **DS:** the dense audit (§4.2), run once the stages above are clean (`BAKE_DENSE=1`).
3. **Adaptive refit (≤ 3).** Every failing (pose, fraction) from the previous iteration becomes a fit sample. Special gates enter as `gate:<pose>`. The refit starts from the previous artifact, which is reopened, and the whole suite is rerun.
4. **Final checks:**
   - **Integrity (`sa6_bake_integrity.py`):**
     - every frozen RP5 file in `SAURIN_RP5_FREEZE.json` re-hashed (11 files, all match);
     - cage topology;
     - semantic face array, semantic map and quad-label order;
     - body file hash against the roster;
     - neutral: corrective exactly 0, and baked neutral equal to plain-LBS neutral exactly;
     - signatures of the anatomical, special-gate and RP5-literal pose ranges.
   - **RP5-literal diagnostics:** `EVAL_SUITE=rp5`, recorded and not gated, as in the pilot.
   - **Before/after (`sa6_bake_beforeafter.py`):** every unbaked failure re-evaluated on the final artifact at the same body, pose and fraction.

**Gates.** The existing RP6 closure rules are unchanged:
- rig-owned folds, contact and tears;
- |dV| ≤ 100 cm³, jaw exempt;
- rigid landmarks ≤ 0.05 cm;
- neutral 0.

Pre-rig composition defects that LBS also shows are counted separately in every evaluation.

**Fit setting (`BAKE_GATE_ALIGNED_ALLOW=1`, e03956e7).** The fit's composition allowance now uses the same ownership rule as the gate (also within 1.0 cm of a pre-rig defect point). Before this, the fit could chase defects the gate does not count.

**Play direction.** The evaluator is stateless: the corrective depends on the pose only, so reverse playback equals forward playback by construction. `sa6_motion_gif.py` plays the elbow segment forward and then reversed (§5).

**No export or read-back path changed,** so no Blender rerun was needed. The package identities are unchanged.

## 3. Results per body

### 3.1 Final bakes

| Body | Final run | Unbaked failing samples | Failing samples per iteration | Families / pose keys | Pose-key widths | Sweep samples | Gate sweep | Dense audit (0.0025) | Motion (local rule) | Integrity |
|---|---|---|---|---|---|---|---|---|---|---|
| BASE_c1 | pass 2, it1 | 1 | 1 → 0 | 1 / 1 | 22.5° | 728, clean | not needed | 4030 samples, 0 failing (blend 1) | clean; tightest 0.050 cm under | clean |
| BASE_c2 | pass 2, it1 | 1 | 1 → 0 | 1 / 2 | 16.25°, 22.5° | 798, clean | not needed | 4840 samples, 0 failing (blend 69) | clean; tightest 0.073 cm under | clean |
| END_FAHI | repair 2, it3 | 31 | 31 → 1 → 14 → 0 | 6 / 6 | 6.25°, 15°, 17.5° | 763, clean | not needed | 4053 samples, 0 failing (blend 328) | clean; tightest 0.030 cm under | clean |
| END_MUFAHI | repair 2, it2 | 56 | 56 → 1 → 0 | 23 / 10 | 6.25°, 17.5°, 22.5°, 32.5° | 1012, clean | clean, 82 samples | 6898 samples, 0 failing (blend 664) | clean; tightest 0.043 cm under | clean |

Every final artifact is also clean on:
- EV: 34 poses × 4 fractions;
- GT: 50 special gates × 4 fractions;
- neutral: 0.0 for base, states, blend and bake;
- rigid landmarks: 0.00 cm, except 0.0013 cm on END_MUFAHI (limit 0.05).

Artifact sha256 (json):

| Body | sha256 |
|---|---|
| BASE_c1 | `8ba88348d2d6f037…` |
| BASE_c2 | `acf789e3e93b2538…` |
| END_FAHI | `8bf951a2488a1ca4…` |
| END_MUFAHI | `6405626a68d06f85…` |

Full hashes, including the npz, are in the results file.

**Reading the END_FAHI row.** Repair 2 continues the w25 run (§3.4):
- **it1:** 1 sample failed. That iteration also failed the first motion rule; the record is kept as run.
- **it2:** clean on samples. The dense audit, taken from `out_dense/v2w`, found 14 between-sample leaks.
- **it3:** the refit cleared them, and every stage is clean, including its own dense stage.

**Refits.** Each final run used at most three adaptive refits (END_FAHI 3, END_MUFAHI 2, bases 1).

### 3.2 Before / after (same body, pose and fraction, same evaluator)

| Body | Pose | Fractions failing before | After |
|---|---|---|---|
| BASE_c1 | `shoulder_abd90_xneg` | 1 | 0 |
| BASE_c2 | `elbow_130_xneg` | 1 | 0 |
| END_FAHI | `shoulder_flex60_xneg` | 6 | 0 |
| END_FAHI | `hip_flex70_xpos` | 12 | 0 |
| END_FAHI | `hip_flex70_xneg` | 6 | 0 |
| END_FAHI | `trunk_twist_30` | 2 | 0 |
| END_FAHI | `lower_axial_flex_25` | 5 | 0 |
| END_MUFAHI | `shoulder_abd90_xneg` | 3 | 0 |
| END_MUFAHI | `hip_flex70_xpos` | 9 | 0 |
| END_MUFAHI | `hip_flex70_xneg` | 17 | 0 |
| END_MUFAHI | `trunk_twist_30` | 14 | 0 |
| END_MUFAHI | `lower_axial_flex_25` | 8 | 0 |
| END_MUFAHI | `elbow_130_xpos` | 1 | 0 |
| END_MUFAHI | `elbow_130_xneg` | 2 | 0 |
| END_MUFAHI | `gate:tail_up_60` | 1 | 0 |
| END_MUFAHI | `gate:tail_down_60` | 1 | 0 |

Total: 89 failing before, 0 after. Each body's rows are in `BA_<body>.json`.

### 3.3 RP5-literal diagnostics (recorded, not gated)

| Body | Rig folds | Rig contact | Rig tears | Volume fails | Composition | Rigid max |
|---|---|---|---|---|---|---|
| BASE_c1 | 1500 | 3670 | 15 | 10 | 0 | 0.00 cm |
| BASE_c2 | 1527 | 3727 | 2 | 10 | 0 | 0.00 cm |
| END_FAHI | 1744 | 4048 | 27 | 14 | 69 | 0.00 cm |
| END_MUFAHI | 2335 | 4824 | 36 | 27 | 120 | 0.00 cm |

These are the RP5 pose definitions run through the RP6 rules. The pilot keeps them as records, and its gates are on the anatomical suite. They are preserved here exactly as the order requires, with the range signature hashed in the integrity check.

### 3.4 Per-body deviations (endpoint controls)

The base bodies used the pass-2 recipe as is. The endpoint controls did not, and every superseded run is kept under `superseded/` with its reason.

**END_FAHI:**

| Run | Result |
|---|---|
| Pass 2 (floor 1/8) | Clean on samples. Failed the first motion rule on `hip_flex70_xpos` by 0.0022 cm (0.6205 vs 0.6183, the blend's own ramp). |
| Repair 1 (`run_fahi_w25.py`, floor 1/4) | Clean on samples. Passes the local motion rule. The dense audit found **14 leaks** of the blend's own defect, none added by the bake: `hip_flex70_xpos` 0.905–0.9175, `shoulder_abd45_xneg` 0.98–0.985, `shoulder_abd90_xneg` 0.49–0.58. |
| **Repair 2 (`run_fahi_dense.py`, final)** | Continued repair 1 with those fractions as refit samples and the dense stage on. **it3 clean on everything.** |

**END_MUFAHI:**

| Run | Result |
|---|---|
| Pass 2 (floor 1/8) | 2 sweep samples left: `trunk_twist_30` 0.59166 / 0.59167. The fit did not converge, alternating between neighbouring samples. The dense audit found **11 leaks**: `trunk_twist_30` 0.585–0.5925 and 0.64–0.6475, and `hip_flex70_xpos` 0.2125. |
| Repair 1 (`run_mufahi_dense.py`) | Continued pass 2 with the dense failures as seeds. it4 cleared the trunk leaks; it5 was clean on samples. **The local motion gate failed `shoulder_abd90_xneg`.** The full-abduction pose key (2.77 cm, width 11.25° = 1/8 of 90°) moved the trunk 0.73 cm in one frame (78.75–81.75°): bake 0.5033 cm against an allowance of 0.50. The first rule had passed this, and the same key was in pass 2. |
| **Repair 2 (`run_mufahi_v3.py`, final)** | Rebaked from v004 with the floor at 1/4, every dense failure found so far as seeds, and the dense stage on. **it2 clean on everything.** |

**Experiment not adopted (cloud).** A fit contact margin (`BAKE_PEN_MARGIN` 0.03 cm) was tried against the END_MUFAHI non-convergence. The fit converged, but a 0.0025-grid check of `trunk_twist_30` still found 7 failures (pass-2 it3: 10). The experiment was not taken further, and the switch stays off by default.

**Recipe difference.** The bases used floor 1/8 and had their dense audit and local-rule motion run afterwards on the same artifacts. Both are clean. The endpoints used floor 1/4 with the dense stage inside the run. Whether to make floor 1/4 plus `BAKE_DENSE=1` the uniform recipe is a decision item (§9).

## 4. Motion and between-sample checks (added during this order)

Two kinds of failure can pass every sampled gate. Both were found while validating, and each now has its own stage in the driver.

### 4.1 Motion pops (motion gate, `sa6_bake_motion.py`)

**Finding (pass 1).** Adaptive refits placed very narrow pose keys. On END_FAHI and END_MUFAHI, keys of 0.2–1.8 cm switched on inside 0.25–1.75°. Every sampled pose was clean, but the surface jumped during playback. This is recorded under `pass1/motion_pops/`.

**Fixes:**
- **Pose-key width floor** (`BAKE_PK_MINW`). A pose key is never narrower than this fraction of its pose's full angle: 1/8 in pass 2, and 1/4 in the endpoint repairs.
- **Motion gate.** Each anatomical pose is played from 0 to 1 on a 1/240 grid plus every driver transition. One frame is 1/30 of the full angle (30 fps, full move in one second). The measure is the corrected surface's movement relative to plain LBS between any two samples within one frame.

**Rule as first proposed:** the bake's worst frame on a pose must be ≤ max(0.50 cm, the packaged blend's worst frame on that pose).

**Rule as revised (made local).** For every frame pair and every vertex:

  bake(f, g, v) ≤ max(0.50 cm, prod(f, g, v) + 0.05 cm)

Above the 0.50 cm cap, the bake may add at most half a millimetre to what the packaged blend does at that place and frame. 0.05 cm is the RP6 rigid-gate resolution.

**Why it was changed.** The first rule compares two worst cases that can sit at different vertices and frames, and that goes wrong both ways:
- **It failed a bake that adds nothing visible.** END_FAHI `hip_flex70_xpos` failed by 0.0015 cm: 0.6198 against 0.6183. The frame (67.7–70°) and vertex are the same as the packaged blend's own steady ramp, and the bake's share there is 0.002 cm.
- **It passed a real pop.** END_MUFAHI repair 1 passed it on `shoulder_abd90_xneg`, because the blend's worst frame (0.5558 cm at 87–90°) is elsewhere. The 0.73 cm pop described in §3.4 was caught by the local rule.

Every motion file keeps both verdicts (`pass_original`, `pass`) and the bake's own frame excursion `k` (bake minus blend, a diagnostic).

**Final bakes:**

| Body | Tightest pose (local rule) | At | Bake / allowance (cm) | Worst bake frame (blend) | First rule | Largest own K move (diagnostic) |
|---|---|---|---|---|---|---|
| BASE_c1 | `shoulder_abd90_xneg` | 72.0–75.0° | 0.453 / 0.503 | 0.510 (0.510) `shoulder_abd90_xneg` | pass | 0.174 cm, `shoulder_abd90_xneg` 87.0–90.0° |
| BASE_c2 | `elbow_130_xneg` | 89.9–94.2° | 0.427 / 0.500 | 0.427 (0.427) `elbow_130_xneg` | pass | 0.165 cm, `elbow_130_xneg` 124.0–128.4° |
| END_FAHI | `hip_flex70_xpos` | 54.2–56.6° | 0.481 / 0.510 | 0.620 (0.618) `hip_flex70_xpos` | FAIL `hip_flex70_xpos` (0.0015 cm) | 0.371 cm, `hip_flex70_xpos` 54.5–56.9° |
| END_MUFAHI | `hip_flex70_xpos` | 52.5–54.8° | 0.463 / 0.506 | 0.556 (0.556) `shoulder_abd90_xneg` | pass | 0.507 cm, `hip_flex70_xneg` 47.2–49.6° |

Where the bake's own move is large (`k` up to 0.51 cm per frame), the total surface motion still stays within the allowance at that place and frame. Any visible pop would show in the total, so the gate tests the total, not `k`.

**The rule needs author approval.** The 0.50 cm cap and the 0.05 cm margin are mine. The 0.50 cm cap covers the v004 elbow slope break recorded in §5.

### 4.2 Between-sample leaks (dense audit, `sa6_bake_dense.py`)

**Finding.** The full sweep samples heavy-joint and K poses every 0.025 of the full angle, plus ±0.25° around every transition. A 0.0025-grid check of END_MUFAHI pass 2 found rig-owned failures between those samples on `trunk_twist_30`: contact at 0.585–0.5925 and a fold at 0.64–0.6475. The bake had cleared the blend's defect only at the fractions it was fitted on.

**Audit.** The audit plays the sweep's dense pose set (every bake-touched pose plus the heavy-joint risk set) on a 0.0025 grid (1/400 of the full angle) plus transitions. The rules are the same closure gates and ownership as everywhere else. The blend is evaluated on the same grid, so a leak (both fail) can be told apart from a defect the bake adds.

**In the driver.** With `BAKE_DENSE=1`, this audit runs once an iteration is otherwise clean, and its failures become refit samples.

| Bake | Poses | Samples | Bake failing | Added by bake | Blend failing (same grid) |
|---|---|---|---|---|---|
| BASE_c1 final | 10 | 4030 | 0 | 0 | 1 |
| BASE_c2 final | 12 | 4840 | 0 | 0 | 69 |
| END_FAHI final | 10 | 4053 | 0 | 0 | 328 |
| END_MUFAHI final | 17 | 6898 | 0 | 0 | 664 |
| END_FAHI repair 1 (superseded) | 10 | 4049 | 14 | 0 | 326 |
| END_MUFAHI pass 2 (superseded) | 17 | 6919 | 11 | 0 | 675 |

**No bake added a defect anywhere on the dense grid.** Every leak was the packaged blend's own failure surviving between fitted fractions.

**Limit.** 0.0025 is a finite grid; a narrower failure band could still fall between its samples. Its spacing in degrees is 0.075° on a 30° pose and 0.325° on the 130° elbow.

## 5. Elbow corrective-rate spike in motion

The benchmark's rate ratio of 7.6 on `elbow_130_xneg` compared sweep segments up to 16° long. Played densely (0.33° steps over 65–130°, `sa6_motion_rate.py`), it turns out to be a **slope break, not a jump**:
- **Where.** The rest-space corrective rate steps from about 0.02 to 0.155 cm/deg at 90.0°, where the elbow driver crosses its 90° family sample. The corrective is piecewise linear in the driver angle.
- **What you see.** The corrected surface's own motion relative to plain LBS rises from about 0.09 to 0.42–0.45 cm per 30 fps frame, for a full 130° bend in one second. This is at the elbow crease; over the same frames the forearm travels about 3 cm.
- **No positional discontinuity** in either play direction.

Unbaked (packaged blend):

| Body | Peak (cm/deg) | At | × playback median | Per 30 fps frame |
|---|---|---|---|---|
| BASE_c1 | 0.096 | 90.0–90.3° | 1.19 | 0.42 cm |
| BASE_c2 | 0.104 | 90.0–90.3° | 1.30 | 0.45 cm |
| END_FAHI | 0.096 | 90.0–90.3° | 1.19 | 0.42 cm |
| END_MUFAHI | 0.090 | 93.9–94.3° (upper arm) | 1.00 | 0.39 cm |

**On the final bakes** (motion gate, `elbow_130_xneg`, blend → bake frame excursion):

| Body | Blend | Bake |
|---|---|---|
| BASE_c1 | 0.394 cm | 0.394 cm |
| BASE_c2 | 0.427 cm | 0.427 cm |
| END_FAHI | 0.394 cm | 0.394 cm |
| END_MUFAHI | 0.391 cm | 0.391 cm |

On `elbow_130_xpos`, END_MUFAHI's elbow keys add 0.004 cm (0.362 → 0.366). The bake does not change the profile; the break belongs to the v004 elbow driver. The motion gate's figures differ slightly from the playback figures above because it uses a different grid and frame window.

**Recorded for review:** a C¹ break, not a defect under any current gate. Smoothing it would mean adding an intermediate driver sample (about 100–110°) to the elbow family. That is a layer change, outside this order.

Evidence is under `motion/`:
- `unbaked/`: dense rate curves and filmstrip (`MR_*`), plus a forward-and-reverse playback (`MG_*.gif`).
- `baked_pass1/`: the same curves for the pass-1 bakes.

## 6. Tail-kink calibration

**Why the pilot measure misfires.** The pilot's kink ratio (2.51) divides the turning at one ring junction by the mean turning of the 11 junctions around it. The frozen tail has 181 rings about 0.69 cm apart, and its neutral shape already scores about 2.5, mostly from the tip taper. A frame can therefore cross 2.51 without any kink made by deformation. On the benchmark, the raw ratio is above 2.51 on 4196 of 7920 packaged-blend frames (53 %).

**Proposed criterion** (`sa6_tail_criterion.py`): use the same rings and window, but measure only the concentration the pose adds on top of neutral.

C = max over junctions k of [(θ_k − window_k) − (θ0_k − window0_k)] in degrees, where θ0 is the neutral tail.

| Verdict | Rule |
|---|---|
| PASS | C ≤ 2.0° and ring-area retention ≥ 0.95 |
| REVIEW | 2.0° < C ≤ 2.5°: look at the centreline and shaded mesh at that frame |
| FAIL | C > 2.5°, or area retention < 0.95 |

Folds, tears, inversion and contact stay with the existing RP6 gates. The raw ratio is kept as a diagnostic only.

**Calibration (visual anchors).** The thresholds come from renders of the worst frames (`tail/renders/`: centreline and profile panels `TR_*`, shaded mesh panels `TM_*`).
- A visible crease line at the tail root appears for plain LBS on `tail_root_biased_60` at C = 2.12°, 2.53° and 3.23°.
- No crease is visible at C = 1.15° and 1.20° (distal), or at 1.62°, 1.92°, 1.99° and 2.45° (`tail_combined`, where the bend spreads along the tail).
- The REVIEW band therefore exists because concentration alone does not separate the 2.45° `tail_combined` frame (no crease) from the 2.12° root-biased frame (crease).

**Data.** Every tail special-gate pose (11 poses) at every 0.025 fraction, for plain LBS, the packaged blend v004 and the bake:
- Benchmark (18 bodies of the feasibility study, 7920 frames per column): `tail/TK_benchmark.json`.
- Roster (the four final bakes, 1760 frames per column): `tail/TC_*.json`, `tail/TK_roster.json`.

| Set | Column | PASS | REVIEW | FAIL | Raw > 2.51 | Raw > 3.07 |
|---|---|---|---|---|---|---|
| Benchmark | plain LBS | 7860 | 45 | 15 | 4511 | 56 |
| Benchmark | packaged blend | 7920 | 0 | 0 | 4196 | 38 |
| Benchmark | bake | 7920 | 0 | 0 | 4196 | 38 |
| Roster | plain LBS | 1758 | 2 | 0 | 1112 | 1 |
| Roster | packaged blend | 1760 | 0 | 0 | 1125 | 0 |
| **Roster** | **bake** | **1760** | **0** | **0** | 1124 | 0 |

**Flagged frames.** All are plain LBS, so none comes from the packaged blend or the bake:
- **Roster:** BASE_c1 `tail_root_biased_60` at 0.975 and 1.0, C = 2.05° and 2.13°, both REVIEW. This is the same crease anchor as above.
- **Benchmark:**
  - 45 REVIEW, on `tail_root_biased_60` and `tail_combined` across 11 bodies: BK-X2a, BK-X3, c1-FAHI, c1-M208-B, c1-MUFAHI, c1-MUHI and c1-T80.
  - 15 FAIL, all on `tail_root_biased_60`:
    - c1-M208-B@0.75: 10 frames from 0.775 upward;
    - BK-X3: 4 frames from 0.925 upward;
    - c1-T80@0.375: 1 frame.
  - The maximum is C = 3.23°, the crease anchor above.

**The nine benchmark rows above raw 3.07** (worst packaged-blend frame per case; C for blend / LBS / bake):

| Case | Pose | Fraction | Raw (blend) | C blend | Raw LBS | C LBS | C bake | Area min |
|---|---|---|---|---|---|---|---|---|
| BK-X2c | tail_down_60 | 0.975 | 3.189 | 0.63° | 3.188 | 0.63° | 0.63° | 0.991 |
| BK-X3 | tail_down_60 | 1.0 | 3.150 | 0.63° | 3.150 | 0.63° | 0.63° | 0.991 |
| BK-X3 | tail_combined | 1.0 | 3.284 | 1.72° | 3.324 | 2.10° | 1.72° | 0.994 |
| c1-M208-B@0.25 | tail_down_60 | 1.0 | 3.084 | 0.62° | 3.084 | 1.05° | 0.62° | 0.991 |
| c1-M208-B@0.75 | tail_down_60 | 1.0 | 3.102 | 0.62° | 3.102 | 0.98° | 0.62° | 0.991 |
| c1-MUHI@0.375 | tail_down_60 | 1.0 | 3.096 | 0.62° | 3.096 | 1.09° | 0.62° | 0.991 |
| c1-MUHI@0.625 | tail_down_60 | 1.0 | 3.110 | 0.62° | 3.110 | 1.11° | 0.62° | 0.991 |
| c1-T80@0.375 | tail_down_60 | 1.0 | 3.165 | 0.63° | 3.165 | 0.63° | 0.63° | 0.991 |
| c1-T80@0.375 | tail_combined | 1.0 | 3.280 | 1.62° | 3.249 | 1.92° | 1.62° | 0.994 |

All nine pass the proposed criterion for the blend and the bake. The raw ratio is high because of the neutral tip taper.

**The pilot's case.** BASE_c1 `tail_down_60` at 100 % reproduces the pilot's raw 3.0736 (pilot 3.074). Its concentration is 0.62° for both the packaged blend and the bake, and 1.06° for plain LBS: a PASS.

**Scope.** This criterion is proposed, not adopted. It covers the frozen tail topology only, and it would replace the raw 2.51 ratio as a gate only on author approval.

**No tail defect needs a corrective or a base-rig change.** The only frames above 2.0° on the roster are plain LBS.

## 7. Timings (Tyler's PC: AMD 16 logical CPUs, 63 GB, Windows 11; one thread per process, below-normal priority)

| Run | Workers / shards | Wall time |
|---|---|---|
| Pass 1, all four bodies in parallel (superseded) | 4 × 4 | 6.9 h |
| Pass 2: BASE_c1 / BASE_c2 / END_FAHI / END_MUFAHI | 4 × 4 | 4.0 / 4.1 / 7.3 / 9.8 h |
| END_FAHI repair 1 (w25) | 8 shards | 3.5 h |
| Dense audit, pass-2 END_MUFAHI + BASE_c1 + BASE_c2 | 6 workers | 9.7 h |
| END_MUFAHI repair 1 (superseded) | 8 shards | 9.2 h |
| Motion re-run, local rule (BASE_c1, BASE_c2, END_FAHI repair 1) | 4 workers | 1.3 h (final run) |
| Dense audit, END_FAHI repair 1 | 6 workers | 2.3 h |
| **END_MUFAHI repair 2 (final)** | 8 shards | 7.3 h |
| **END_FAHI repair 2 (final)** | 8 shards | 2.6 h |

**Final runs, by stage:**

| Stage | BASE_c1 | BASE_c2 | END_FAHI | END_MUFAHI |
|---|---|---|---|---|
| Fit | 0.5 h | 0.5 h | 0.8 h | 1.4 h |
| Sweep | 1.4 h | 1.4 h | 1.4 h | 1.4 h |
| Motion | 1.4 h | 1.4 h | 1.1 h | 1.0 h |
| Dense | separate | separate | 1.5 h | 2.6 h |

Many runs overlapped on the PC, so their wall times are longer than they would be alone.

- **Peak memory per process:** about 3.5 GB in the motion stage, 1.1–1.3 GB elsewhere.
- **Retries:** no stage needed one, in any run.

**Interruptions and incidents:**
1. **Stale tool copy.** When the motion rule was made local, the first copy to the PC did not replace the file; the copy tool reused an earlier staged version. Two motion runs, and END_MUFAHI repair 1's it4 motion stage, used the previous rule. Every affected shard was cleared and recomputed. The PC tool files were then checked byte-for-byte against the repo before use.
2. **Cloud restarts.** The cloud workspace restarted twice. Only cloud waits were lost; no PC work was affected.

**Off-PC work (cloud, 2 cores):**
- tail calibration on the roster, 4–5 min per body;
- the elbow and pop playback analyses;
- the contact-margin experiment: a 17 min fit and a `trunk_twist_30` dense check of about 40 min per artifact;
- one motion spot-check (3 min);
- tail renders;
- evidence building.

## 8. Evidence layout

`rac-rp6-evidence/saurin/rig_pilot/offline_bake/` contains:
- **`SA_RP6_offline_bake_results_v001.json`:** per body:
  - roster, run and recipe;
  - unbaked failures;
  - every iteration;
  - final gates;
  - dense audit;
  - motion (local rule and first rule);
  - integrity;
  - before/after;
  - RP5-literal diagnostics;
  - pose-key widths;
  - artifact sha256;
  - stage timings.
- **`SA_RP6_offline_bake_manifest_v001.json`:** sha256 of every file.
- **`SA_RP6_offline_bake_roster_v001.json`:** recorded before fitting.
- **`bodies/<body>/`:** the final run: unbaked reference, every iteration, and the final artifact (BK json + npz) with EV, GT, SW, gate sweep, MO, DS, IN, BA and rp5lit. For the bases, `DS_*.json` and `MO_*.local.json` were added from the separate audits.
- **`superseded/`:** END_FAHI pass 2 and repair 1, END_MUFAHI pass 2 and repair 1, each with its reason.
- **`pass1/`:** pass-1 evidence, motion-pop measurements and the stopped END_MUFAHI repair.
- **`tail/`:**
  - TC per roster body;
  - TK roster and benchmark;
  - the benchmark frames;
  - `renders/`.
- **`motion/`:** elbow rate curves and playback.
- **PC runners and logs:**
  - `run_*.py`, `START_*.bat`, seeds and job lists;
  - `pc_*.log`;
  - `timings.jsonl`, `hardware.jsonl`;
  - `build_ob_evidence.py`, which builds this folder.

**Tools** in `tools/rac/rp/saurin_rp6_v001/`:

| Tool | Commits |
|---|---|
| `sa6_bake_full.py`: driver with MO, DS, `BAKE_SEED_EXTRA` | 35c120d8, c4ef7621, 19cf2360 |
| `sa6_bake_motion.py` | 35c120d8, 19cf2360, 56f4656f |
| `sa6_bake_dense.py` | c4ef7621 |
| `sa6_bake.py`: `BAKE_PK_MINW`, aligned allowance, experiment switches | e03956e7, 35c120d8, c4ef7621 |
| `sa6_tail_calib.py`, `sa6_tail_criterion.py`, `sa6_motion_rate.py`, `sa6_motion_gif.py` | — |

## 9. Remaining items and decisions for the author

1. **Shipping roster.** None exists. These four bakes cover the bases and two regression controls only. Designate the shipping presets to bake.
2. **Motion gate (§4.1).** Approve, adjust or reject the local rule: bake ≤ max(0.50 cm, blend + 0.05 cm) per frame and vertex, with a frame of 1/30 of the full angle.
3. **Dense audit (§4.2).** Approve it as a standing stage (`BAKE_DENSE=1`) at the 0.0025 grid, or set another grid or budget. It roughly doubles a body's validation time: 1.5–2.6 h of the final runs.
4. **Uniform recipe.** Decide whether pose-key floor 1/4 plus the dense stage becomes the default. If so, the bases need a rebake under it: they pass every check now, but were fitted with floor 1/8.
5. **Tail criterion (§6).** Approve C ≤ 2.0° PASS, 2.0–2.5° REVIEW and > 2.5° or area < 0.95 FAIL as the gate, replacing the raw 2.51 ratio.
6. **Elbow C¹ break (§5).** Accept it as is, or authorise an intermediate elbow-family driver sample. That is a v004 layer change.
7. **Fit non-convergence.** On END_MUFAHI pass 2, the fit alternated between neighbouring contact samples. It was bypassed by the rebake, not fixed in the solver. The fit-margin experiment is not adopted.

Status remains **RP6 RIG PILOT / NOT FROZEN**. Stopping for ChatGPT and author review.
