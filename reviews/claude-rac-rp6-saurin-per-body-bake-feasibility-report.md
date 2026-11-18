# Saurin RP6 — per-body bake feasibility report

Order: [chatgpt-rac-rp6-saurin-per-body-bake-feasibility-order.md](chatgpt-rac-rp6-saurin-per-body-bake-feasibility-order.md) (a13cae71)
Continues: [corrective layer validation report](claude-rac-rp6-saurin-corrective-layer-validation-report.md) (0caf0974)
Evidence: [`rac-rp6-evidence/saurin/rig_pilot/bake_feasibility/`](rac-rp6-evidence/saurin/rig_pilot/bake_feasibility/)
Status: **RP6 RIG PILOT / NOT FROZEN**

## 1. Verdict

**Feasible on the benchmark: all 18 baked bodies pass every gate, but only with adaptive refits.**

- **Test set.** The 18 test bodies were fixed before fitting (`SA_RP6_bake_test_bodies_v001.json`). They cover every failure from the v003/v004 validation plus five new held-out blends.
- **How each bake is checked.** Each bake starts from the packaged blend v004 and is written as a versioned artifact. It is then reopened from disk and gated with the closure ownership rules of `sa6_blend.evaluate`.
- **Final artifacts.** Every final artifact has 0 rig-owned folds, contact, tears and volume failures:
  - on all 34 anatomical poses at 25 / 50 / 75 / 100 %;
  - on all 50 special-gate poses (tail, hand, foot/toe, jaw/head) at the same four fractions;
  - on a between-sample sweep (§2.3) of 729–1040 samples per body;
  - for the 5 gate-refit bodies, also on a dense check of every refit gate pose: 36 fractions, every 0.025.
- **Neutral and rigid displacement.** Neutral corrective displacement is exactly 0.0 on every body. The largest protected-rigid displacement is 0.0011 cm (gate 0.05 cm).
- **Convergence was not automatic.** Only 5 of 18 bodies were clean straight from the four-fraction fit through every later check. Two pass-1 fits had to be redone from scratch.
  - 10 needed one or two refits at angles *between* the gated fractions (§5).
  - 5 needed a refit because the special gates failed (§6). One of these, MUFAHI@0.875, also needed a between-angle refit, so 13 bodies were refit in total.
  - Every special-gate failure was in the packaged blend v004 itself: the bake added nothing on those poses.
  - All refits closed within the iteration limit.
- **Cost.** On the PC, one worker took 49–295 min per body (median 60 min) for the first three passes. Total PC time was 24.6 h. The gate refits each took 84–130 min of cloud (OFF_PC) time (§8).
- **Controls.** The base controls and the accepted endpoints are clean at the four gated fractions, as accepted. All four fail *between* those fractions in the packaged blend v004 (§7). So the between-sample gap is a property of the shipped layer, not of the bake.
- **Decision needed** (§10): whether per-body bake at creator commit becomes the production path, on what sweep standard and compute budget, and whether the packaged blend's own between-angle and special-gate failures are acceptable on bodies that are not baked.

## 2. Method

### 2.1 Bake model (unchanged from the order)

baked(T) = P0(T) + K(T), where:

- P0 is the packaged blend v004 (`SA_RP6_creator_layers_v004.json`);
- K is a per-body correction made of driver families keyed by bone and axis, plus pose keys with fraction-local tents;
- K(neutral) = 0, which is checked on every artifact.

The bake changes no export or read-back path. It is the same corrective format the layer already ships. No Blender rerun was needed.

### 2.2 Gates (identical for every column)

These are the closure rules of `sa6_blend.evaluate`:

- **Rig-owned folds, contact and tears.** A defect counts as rig-owned unless it sits on a pre-rig composition defect that LBS also shows. A tear is > 2.5× stretch and > 0.75 cm.
- **Volume:** |dV| ≤ 100 cm³; jaw poses are exempt.
- **Protected rigid set:** ≤ 0.05 cm.
- **Neutral displacement:** 0.

The special gates run the same rules on the 50 poses of `sa6_gates.gate_poses` using `sa6_bake_gates.py`, which also records the rig-pilot audit metrics at 100 %.

### 2.3 Passes

| Pass | What | Where |
|---|---|---|
| 1 | Fit at 25/50/75/100 % from P0, then reopen and evaluate 34 poses × 4 fractions | PC |
| 2 | Adaptive loop on the heavy-joint risk set plus every pose K touches: sweep at 0.025 and ±0.25° around every transition → failing angles become extra fit samples → refit from the artifact → evaluate → sweep (≤ 3 iterations) | PC |
| 3 | The same adaptive loop on the full suite (`SWEEP_SET=all`): 0.025 on risk/K poses, 0.125 on every other pose, ±0.25° around every bake **and** packaged-blend transition | PC (12 bodies), cloud OFF_PC (6 bodies) |
| Gates | 50 special-gate poses × 4 fractions on the pass-3 final artifact | cloud OFF_PC |
| Gate refit | Each failing gate pose (`gate:<pose>` in `BAKE_EXTRA`) joins the fit → reopen and evaluate 34 × 4 → full pass-3 sweep → all 50 gates → dense gate check (0.025–0.975) | cloud OFF_PC |
| Controls | Full pass-3 sweep of BASE_c1, BASE_c2, END_FAHI, END_MUFAHI (empty K: baked ≡ packaged blend) | PC |

### 2.4 Commands and runners (all committed)

- **Tools** (`tools/rac/rp/saurin_rp6_v001/`):
  - `sa6_bake.py fit|eval`;
  - `sa6_bake_adapt.py`;
  - `sa6_bake_sweep.py` (with the `SWEEP_SET`, `SWEEP_STEP_OTHER` and `SWEEP_SHARD` settings), plus `sa6_bake_sweep_merge.py`;
  - `sa6_bake_gates.py` (with the `GATES_ONLY`, `GATES_FRACS` and `GATES_CKPT` settings).
- **PC runners** (`pc_bake/`): `START_BAKE.bat` + `run_bake.py` (pass 1), `START_ADAPT.bat` + `run_adapt.py` (pass 2), `START_ADAPT2.bat` + `run_adapt2.py` (pass 3), and `controls/START_CTRL.bat` + `run_ctrl.py` (controls).
- **Cloud runners** (`cloud_bake/`, see its README):
  - `gates_lane.sh` + `gates_lists.txt`;
  - `gate_refit.sh` + `gate_refit_extra_<body>.json`;
  - `gate_dense.sh`;
  - `fn_finish.sh`;
  - `pc_bake/cloud_adapt2.sh`.
- **Tool commits in this order:** 548a6bf2, 77ecff30, add7793b, 738284a6, c9f8b7ff, 0889d6bc, 34b9ae67, 14a1fe58, 3c5b0c86, 438dc562, 5475a01d.
  - The last two only add resume and parallelism. Both were checked to reproduce the unsharded and uninterrupted results:
    - 0 total mismatches over the 25 existing gate files;
    - a resumed gate run identical to the full run;
    - shards covering the same 34 poses with the same sample counts.
  - No gating rule changed during the order.

## 3. Inputs and hashes

- **Package:** `SA_RP6_creator_layers_v004.json`, sha256 `95fb5d6baf9bc6a9e99d444af7738db73da2028faf53daba56864ef14fe333c1`
- **Base layer:** `SA_RP6_correctives_v002.json`; arrays M `9ed2428e…4aa78b`, F `3dda4817…e7e260`
- **Test bodies:** `SA_RP6_bake_test_bodies_v001.json`, sha256 `c48a9e51…41d03ada`. Each body's geometry sha256 is in `bodies.json`.
- **Every artifact, evaluation, sweep and gate file:** sha256 in `SA_RP6_bake_results_v001.json` (`bodies[*].sha`, `special_gates[*].sha256`, `controls[*].sha256`).
- **Control artifacts:** before the sweep, their `recipe` metadata was corrected from `bodies.json`, adding a `recipe_note` field. The earlier copies carried the F-N@0.25 recipe by mistake. K is empty and the geometry comes from `bodies.json`, so no result depends on that field.

## 4. Per-body results (final artifacts)

Column notes:
- **K fam / keys:** driver families / pose keys in the final K.
- **Sweep:** between-sample samples, all clean.
- **Gates:** clean, with K active on n of the 50 poses (max |K| on those poses).
- **Refits:** P1 redo = pass-1 refit from scratch, P2 / P3 = between-angle passes, G = special-gate refit.

| Body | K fam / keys | 34×4 eval | Sweep | Gates | Rigid max (cm) | Refits | PC min |
|---|---|---|---|---|---|---|---|
| c1-MUHI@0.375 | 1 / 0 | clean | 741 | clean, 0 | 0.0000 | — | 58 |
| c1-MUHI@0.625 | 2 / 0 | clean | 745 | clean, 0 | 0.0000 | P2×1 | 81 |
| c1-FAHI@0.375 | 4 / 0 | clean | 832 | clean, 8 (0.204) | 0.0000 | — | 65 |
| c1-FAHI@0.625 | 5 / 4 | clean | 836 | clean, 2 (0.006) | 0.0000 | P1 redo, P2×2 | 186 |
| c1-FAHI@0.9375 | 6 / 2 | clean | 749 | clean, 0 | 0.0000 | P2×2 | 147 |
| c1-MUFAHI@0.0625 | 1 / 0 | clean | 747 | clean, 0 | 0.0001 | — | 49 |
| c1-MUFAHI@0.375 | 4 / 5 | clean | 754 | clean, 0 | 0.0005 | P2×1 | 106 |
| c1-MUFAHI@0.625 | 7 / 1 | clean | 753 | clean, 0 | 0.0008 | P1 redo, P2×2, P3×1 | 295 |
| c1-MUFAHI@0.875 | 12 / 6 | clean | 992 | clean, 6 (0.123) | 0.0011 | P2×1, P3×1, G | 206 |
| c1-T80@0.375 | 2 / 1 | clean | 729 | clean, 0 | 0.0000 | P3×1 | 103 |
| c1-M208-B@0.25 | 6 / 0 | clean | 902 | clean, 11 (0.970) | 0.0000 | G | 10 |
| c1-M208-B@0.75 | 14 / 2 | clean | 1040 | clean, 15 (1.009) | 0.0000 | P3×1, G | 10 |
| c2-F-N@0.25 | 1 / 2 | clean | 808 | clean, 0 | 0.0000 | P3×1 | 10 |
| c2-F-N@0.40 | 1 / 2 | clean | 813 | clean, 0 | 0.0000 | P3×1 | 10 |
| BK-X2a | 2 / 0 | clean | 747 | clean, 0 | 0.0000 | — | 59 |
| BK-X2b | 2 / 0 | clean | 750 | clean, 0 | 0.0006 | — | 62 |
| BK-X2c | 4 / 0 | clean | 821 | clean, 4 (0.925) | 0.0000 | G | 9 |
| BK-X3 | 5 / 0 | clean | 881 | clean, 6 (0.953) | 0.0000 | G | 11 |

- **PC minutes** cover passes 1–3 on the PC. The six bodies at 9–11 min ran only pass 1 on the PC and finished in the cloud (§8).
- **Pass 1, first fit,** was clean on 16 of 18 bodies:
  - FAHI@0.625 had 5 rig flips and 15 rig tears;
  - MUFAHI@0.625 had 2 rig flips.
  
  Both were refit from scratch with the fit fallback (add7793b), listed in `redo.txt`, and came out clean. The superseded evaluations are kept as `artifacts/<body>/pass1_superseded_EV_<body>.json`.
- **The ownership columns** (`base_rig`, `blend_rig`, `lbs_rig`, `composition`) of every evaluation are in the results JSON. Neutral displacement is 0.0 on all 18.

## 5. Between-angle findings (passes 2–3)

Four-fraction gating alone missed failures between the gated fractions on 10 of the 18 bodies:

- **Pass 2 (risk set):**
  - FAHI@0.625: hip / trunk, 2 iterations.
  - FAHI@0.9375: `shoulder_flex60_xneg` / `lower_axial_flex_25`, 2 iterations.
  - MUFAHI@0.375: hip / shoulder, 1 iteration.
  - MUFAHI@0.625: hip, 2 iterations.
  - MUFAHI@0.875: `hip_xneg` / trunk / lower axial, 1 iteration.
  - MUHI@0.625: shoulder, 1 iteration.
- **Pass 3 (full suite):**
  - MUFAHI@0.625: `trunk_twist_30` at 0.30–0.35 and `lower_axial_flex_25` at 0.95.
  - MUFAHI@0.875: `elbow_130` at 0.875, both sides.
  - T80@0.375: `shoulder_abd90_xneg` at 0.5028, which is a ±0.25° transition sample. The same spot fails on BASE_c1 (§7).
  - M208-B@0.75, F-N@0.25 and F-N@0.40: `elbow_130_xneg` at 0.875.
- **Continuity.** The largest rate ratio (max / median corrective change per degree) is 7.6, on `elbow_130_xneg`. It occurs on bodies where K is 0 on that pose, and on BASE_c1 (7.56), so it comes from the packaged blend. No gate covers it. It is recorded, not gated.
- **Return sweeps** equal the forward sweeps by construction, because the evaluator is stateless.

## 6. Special gates and gate refits

**First run on the pass-3 artifacts:** 13 of 18 bodies clean. Five failed at 100 % (M208-B@0.75 also at 75 % on the jaw), all with K = 0 on the failing pose, so the packaged blend v004 fails there:

| Body | Failing gate poses (all with K = 0) | Defects |
|---|---|---|
| c1-MUFAHI@0.875 | `tail_root_biased_60` @1.00 | 1 tail fold (LBS has 2) |
| BK-X2c | `foot_curl_xpos` @1.00 | 1 tear |
| BK-X3 | `ankle_plantar25_xpos`, `foot_pushoff_xpos`, `foot_curl_xpos` @1.00; `ankle_dorsi25_xneg` @1.00 | 5 ankle folds, 3 tears |
| c1-M208-B@0.25 | same 4 ankle/foot poses @1.00; `jaw_open_32`, `jaw32_head_pitch_up` @1.00 | 14 folds (11 head), 5 tears |
| c1-M208-B@0.75 | all 8 ankle/foot poses, both sides @1.00; both jaw poses @0.75 and @1.00 | 102 folds (83 head), 17 tears |

**The refit.** Each failing gate pose was added to the fit as a `gate:<pose>` sample, initialised from the pass-3 artifact; earlier between-angle samples were kept.

**Result.** All five refits are clean:
- on the 34 × 4 evaluation;
- on the full between-angle sweep;
- on all 50 gates at the four fractions;
- on the dense check: every refit gate pose at 36 fractions, 0.025–0.975, with 0 defects.

Corrections are at most 1.01 cm, and the protected-rigid set does not move. The artifact from before each refit and its failing gate file are kept under `artifacts/<body>/pre_gate_refit/`.

**Renders.** `renders/` holds three-panel close-ups (plain LBS | packaged blend v004 | baked) of three refit gate poses, before (`_it0` / `_it1`) and after (`_it2`) the gate refit, each with its fold count in the title:
- M208-B@0.75 `jaw_open_32`: 32 → 0;
- BK-X3 `ankle_plantar25_xpos`;
- MUFAHI@0.875 `tail_root_biased_60`: 1 → 0.

The other renders are pass-3 between-angle cases.

**Rig-pilot audit metrics at 100 %** (bake, all 18 bodies):

| Metric | Range |
|---|---|
| Tail ring-area ratio | 0.985–0.998 |
| Palm volume ratio | 0.982–1.046 |
| Foot volume ratio | 0.991–1.076 |
| Sole down-facing fraction | 0.81–0.87 |
| Upper-head rigid error | 0.000 cm |

**Tail kink ratio: 2.26–3.28. This one needs a decision.**
- The rig-pilot report states kink ≤ 2.51. The pilot's own audit file reaches 3.07 on `tail_down_60` (c1 and c2), so that bound was never met as written.
- On the blended bodies, 96 of 198 tail rows exceed 2.51, and 9 exceed 3.07.
- In all 9 rows above 3.07, LBS exceeds 3.07 as well. On 8 of them the bake adds nothing to the tail. On the ninth (BK-X3 `tail_combined`) the bake slightly *lowers* the kink: 3.284 against LBS 3.324.
- Kink is therefore a property of the skinning or the body geometry, not of the bake. It is recorded and not used as a pass/fail gate here.
- Where K is active on a tail pose, it raises kink above LBS by at most 0.035 (FAHI@0.625 `tail_down_60`: 2.945 against 2.91).

## 7. Controls and endpoint recheck (PC)

These are full pass-3 sweeps of the controls with empty K, so baked equals the packaged blend v004. They used the same tools and the same gates as the bodies.

| Control | Samples | At 25/50/75/100 % | Between the gated fractions |
|---|---|---|---|
| BASE_c1 | 725 | clean | `shoulder_abd90_xneg` @0.50278: 1 rig contact |
| BASE_c2 | 731 | clean | `elbow_130_xneg` @0.875: 5 rig folds |
| END_FAHI | 735 | clean | 31 failing samples: `shoulder_flex60_xneg`, `hip_flex70` both sides, `trunk_twist_30`, `lower_axial_flex_25` |
| END_MUFAHI | 746 | clean | 54 failing samples: the same poses plus `shoulder_abd90_xneg` and `elbow_130` both sides (up to 11 folds + 11 contact at `elbow_130_xpos` @0.875) |

- **Accepted results reconfirmed.** All four are clean at every gated fraction, consistent with the committed v004 acceptance (eval_layers_v004).
- **The between-sample failures are in the shipped layer.** They fall on the same poses and angles the bakes had to refit (§5). The earlier unrecorded END_FAHI claim (shoulder 35–60 %, trunk 65–85 %, hip 55–90 %) is now on record, in `controls/SW_END_FAHI.json`.
- **Volume and rigid set.** No control has a volume or rigid-set failure.

## 8. Timings

**PC: TylersPC.**
- **Hardware:** AMD64 Family 25 Model 97, 16 logical CPUs, 63.1 GB, Windows 11 (26300), Python 3.13.18.
- **Passes 1–3:** 1 worker, 1 numerical thread, BELOW_NORMAL priority, no pauses.

| Stage (PC) | n | min | median | max | total |
|---|---|---|---|---|---|
| Pass 1 fit (incl. 2 redos) | 20 | 175 s | 575 s | 2869 s | 4.36 h |
| Pass 1 reopen + evaluate | 20 | 339 s | 364 s | 400 s | 2.03 h |
| Pass 2, non-vacuous bodies | 12 | 114 s | 1263 s | 5474 s | 7.63 h |
| Pass 3 | 12 | 2031 s | 2255 s | 6665 s | 10.55 h |
| Controls, 4 bodies × 4 pose shards in parallel | 16 | 3171 s | — | 3260 s | **54 min wall** |

- **PC total for passes 1–3:** 24.6 h of single-worker time.
- **Retries:** the 2 pass-1 refits from scratch (FAHI@0.625, MUFAHI@0.625; §4). No unconverged fit needed the retry path.
- **Peak memory:**

  | Stage | Peak memory |
  |---|---|
  | PC fit | 1221–1246 MB |
  | PC evaluate | 856–886 MB |
  | Cloud fit | 840–878 MB |
  | Cloud gates | 844–849 MB |

**Off-PC: Anthropic cloud container** (Linux, 2 vCPU, 7 GB; 1 thread per process; 2 h job cap, all stages resumable). These timings are labelled OFF_PC in `SA_RP6_bake_timings_v001.json` and are not comparable 1:1 with the PC timings.

| Stage (cloud, OFF_PC) | n | min | median | max | total |
|---|---|---|---|---|---|
| Pass 3, six bodies (incl. F-N in bounded chunks) | 6 | — | — | — | 13.0 h |
| Special gates, 50 poses × 4 | 18 | 741 s | 1410 s | 1551 s | 6.5 h |
| Gate refit, per body (fit + evaluate + sweep + gates + dense) | 5 | 84 min | 111 min | 130 min | 8.9 h |

- **Gate-refit stages:**

  | Stage | Range |
  |---|---|
  | Fit | 1369–3089 s |
  | Evaluate | 1015–1571 s |
  | Sweep | 318–3568 s |
  | Gates | 539–968 s |
  | Dense check | 213–1215 s |

- **Throughput on the PC.** The PC passes used one worker by design, to leave the PC usable. The control run shows the same work spread over the PC's 16 threads: 4 full sweeps in 54 min of wall time. A production bake on that PC could run at roughly 8–16 bodies or shards in parallel. Each process peaks at about 1.2 GB.

## 9. Limitations — what this does not establish

- **The benchmark is 18 bodies chosen to be hard.** The pass rate on arbitrary creator bodies is not measured. 13 of 18 needed at least one refit.
- **"Clean" is clean on the sampled set.**
  - The sampled set: 0.025 on heavy-joint, K and refit-gate poses, 0.125 elsewhere, and ±0.25° around every transition.
  - A finer grid or other pose combinations could still find failures. The density of the sweep is a standard to agree on, not a proof.
- **The special gates are not part of the default fit.** They entered only after failing. A production bake would have to gate and refit on them from the start, which adds about 15–25 min per body on one core.
- **The tail kink criterion is unresolved (§6),** and the rate-ratio continuity spike (7.6) is not gated.
- **Bodies that are not baked keep the packaged blend's between-angle and special-gate failures (§6–7).**
- **Cost figures are single-thread.** Off-PC figures come from a different and slower machine.

## 10. Decision needed

1. **Adoption.** Adopt per-body bake at creator commit as the production path for RP6 (baked = packaged blend v004 + K, with K stored per body)?
2. **Standard.** If adopted, which sweep standard and gate set are required before a body is committed?
   - Proposed: the pass-3 sweep, plus the 50 special gates from the start, with an adaptive refit limit of 3.
3. **Budget.** What is the per-body compute budget?
   - Measured: a median of about 1 h of single-worker PC time, about 5 h in the worst case.
   - Parallel workers on a 16-thread machine cut wall time roughly 8–16×.
4. **Unbaked bodies.** Is the packaged blend v004 acceptable on bodies that are *not* baked? It fails between gated angles on both base controls and both accepted endpoints, and fails special gates at 100 % on 4 of the 18 test blends. The alternative is to repair the shipped layer.
5. **Tail kink.** Restate the tail-kink criterion. The rig-pilot "≤ 2.51" is exceeded by the pilot's own audit and by LBS on the blended bodies.

Status remains **RP6 RIG PILOT / NOT FROZEN**. Stopping for review.
