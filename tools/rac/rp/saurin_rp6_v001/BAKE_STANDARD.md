# Saurin RP6 — standard per-body offline bake (instructions)

**Status:** RP6 RIG PILOT / NOT FROZEN.
**Decided by:** [standards approval order](../../../../reviews/chatgpt-rac-rp6-saurin-offline-bake-standards-approval-order.md) (c65e6c93, 2026-11-20).
**Evidence:** [offline bake validation report](../../../../reviews/claude-rac-rp6-saurin-offline-bake-validation-report.md), evidence commit `c74bbe5c`.
**Closure:** [closure report](../../../../reviews/claude-rac-rp6-saurin-offline-bake-standards-closure.md).

Offline per-body baking is the adopted Saurin RP6 workflow. Each body ships as

  baked(T) = packaged blend v004 (T) + K_body(T),  with K_body = 0 at neutral.

The initialisation layer is `SA_RP6_creator_layers_v004.json`. K_body is a pose-driven corrective set fitted on that exact body. Running a new bake batch needs its own order.

## 1. Approved standard recipe

| Setting | Value | Meaning |
|---|---|---|
| `BAKE_PK_MINW` | **0.25** | Minimum **half-width** of a pose-key tent, as a fraction of the pose's full angle. A key at driver angle s ramps over s − w → s → s + w, with w ≥ 0.25 × full angle (`sa6_bake.BakeProxy.add_pose_key`; tent weight in `sa6_correctives.pk_weight`). |
| `BAKE_DENSE` / `DENSE_STEP` | **1 / 0.0025** | Dense between-sample audit (`sa6_bake_dense.py`), described below. |
| `BAKE_GATE_ALIGNED_ALLOW` | 1 | The fit's composition allowance is the gate ownership rule: pre-rig defects that plain LBS also shows, within 1.0 cm of a pre-rig defect point. |
| `BAKE_MOTION` / `BAKE_MOTION_RULE` | 1 / **local** | Provisional local motion rule (§3). |
| Adaptive refits | ≤ **3** | After the third refit, any remaining failure is reported for review. |

**Dense audit scope.** Every bake-affected anatomical pose plus the heavy-joint risk set, on a 0.0025 grid. Samples are kept at ±0.25° around every active baked and initialisation-layer driver transition within the supported range.

**Where the recipe lives.** These are the defaults of the normal entry point, `sa6_bake_full.py` (`BAKE_RECIPE=standard`).
- `python sa6_bake_full.py --recipe` prints the effective recipe.
- The standard PC runner is `pc_bake/run_standard.py` (+ `START_STANDARD.bat`). It forces the standard and removes any stray override. It also writes `RECIPE.json` beside each body's output before the worker starts.

## 2. Validation, from the first pass (every iteration)

Each iteration reopens the artifact from disk and runs (`sa6_bake_full.py`):

| Stage | What runs |
|---|---|
| EV | All 34 anatomical poses × 25 / 50 / 75 / 100 %, plus neutral. |
| GT | All 50 special-gate poses × 25 / 50 / 75 / 100 %, plus neutral. |
| SW | Full anatomical sweep: 0.025 steps on the heavy-joint and bake-affected poses, 0.125 elsewhere, ±0.25° at every baked and initialisation-layer transition. |
| GS | Every special pose that entered the fit, swept at 0.025 plus its transitions. |
| MO | Motion rule (§3). |
| DS | Dense audit, once the stages above are clean. |

**Final stages:**
- IN: integrity. That means frozen RP5 hashes, cage topology, semantic order, the body file, neutral exactly 0, and the pose-range signatures.
- RL: RP5-literal diagnostics, recorded but not gated.
- BA: before/after at the same body, pose and fraction for every unbaked failure.

**Gates (unchanged):**
- rig-owned folds, contact and tears;
- |dV| ≤ 100 cm³, jaw exempt;
- rigid landmarks ≤ 0.05 cm;
- neutral 0.

Composition ownership needs the pre-rig evidence: within 1.0 cm of a pre-rig defect point and shown by plain LBS, or the winding test.

**Feedback into the adaptive fit.** Each refit starts from the previous artifact.
- **Gate, sweep and dense failures** become fit samples. A failing special gate enters as `gate:<pose>`.
- **A motion-rule failure** enters as `motion:<pose>`:
  - the failing frame pair's fractions become fit samples of that pose;
  - that pose's key half-width floor doubles, to min(1, 2 × max(floor, sample step));
  - existing keys of the pose are widened to it.

  It is tested to fix the motion failure. Convergence of the full refit loop after widening is not yet demonstrated (standards closure §1).

## 3. Provisional motion rule (`sa6_bake_motion.py`)

For every frame pair (f, g) one frame apart and every vertex v:

```text
e_bake(f, g, v) <= max(0.50 cm, e_initialization(f, g, v) + 0.05 cm)
```

- **Excursion** is the corrected surface's change relative to plain LBS, between f and g.
- **Test speed** is the pose's full range in 1 s at 30 fps, so one frame is 1/30 of the full angle.
- **Grid** is 1/240 of the full angle, plus every driver transition.
- **Diagnostics:** the first rule's verdict (`pass_original`) and the bake-only excursion `k` are kept.

**Scope.** This is a regression check of frame excursion at that speed. It inherits any motion already in the initialisation layer. It says nothing about acceleration or other speeds; claims about those need their own evidence.

**Before a new body's bake is accepted**, review its worst cases in playback with `sa6_bake_playback.py`:
- the three tightest poses under the local rule;
- the pose with the largest bake-only excursion;
- `elbow_130_xneg`.

The playback runs at the test speed (30 fps, full range in 1 s, forward + reverse). It also writes a ×4 slow GIF, a still sheet around the worst frame, a sheet around the largest slope break, and a per-frame curve.

Record the playback speed and the visual conclusion in the acceptance notes.

Show a person whole-body playback as well (`sa6_bake_playback_view.py`: plain skin, fixed camera, real time plus ×4 slow), and record their verdict. The close-up review images are hard to read for anyone but the tool's author. The 2026-11-20 author review found visible defects that no gate measures: SAURIN-RP6-DEF-SHOULDER-1 and DEF-ELBOW-MUSCLE-1 (carry-forward register).

## 4. Provisional tail criterion (`sa6_tail_criterion.py`)

**Scope.** The frozen Saurin tail topology only: 181 rings, an 11-junction window, and the sampled tail special-gate motions.

C = the maximum deformation-added turning concentration, relative to the same body's neutral tail.

| Result | Criterion |
|---|---|
| PASS | C ≤ 2.0° and ring-area retention ≥ 0.95 |
| REVIEW | 2.0° < C ≤ 2.5° and area retention ≥ 0.95. Visual review of the centreline and the shaded mesh in motion at the flagged frame (`sa6_tail_render.py`). |
| FAIL | C > 2.5°, or area retention < 0.95 |

The raw 2.51 kink ratio stays a recorded diagnostic. A visible hard kink, root collapse, tearing or inversion is an open defect even when C passes.

To run it: `sa6_tail_calib.py` per body on the final artifact (every tail special-gate pose, every 0.025 fraction), then `sa6_tail_criterion.py`. Render the worst baked case.

## 5. Acceptance record

The driver writes `ACCEPT_<body>.json` with:
- `accepted_candidate`: final iteration clean and integrity clean;
- the effective recipe;
- sha256 of every `sa6_*.py` tool;
- body inputs: `bodies.json`, the body npz, the vertex hash and the body recipe;
- rig inputs: the initialisation layers and base arrays, with their sha256;
- the artifact json and npz sha256;
- the sampled motions and fractions per stage (EV, GT, SW, GS, MO, DS) with their verdicts.

**Acceptance also needs** the motion playback review and the tail review above, recorded with the run.

**Before a standard run on the PC,** copy the repo's tool folder into `SaurinRP6_offline\tools`. Check the tool hashes in `ACCEPT_*.json` against the repo commit.

**Earlier artifacts.** The PC fits for the offline bake order ran `sa6_bake.py` at commit 35c120d8. That version did not write `pk_min_width` into the artifact, so the floor for those artifacts is evidenced by the runner settings and by the key widths.

## 6. Retained artifacts (accepted, not rebaked)

| Body | Artifact (offline bake evidence `c74bbe5c`, `bodies/<body>/it1/`) | sha256 json / npz |
|---|---|---|
| BASE_c1 | `BK_BASE_c1` | `8ba88348d2d6f037441f363aa4ef4f12ece84e73dbf8b8d6f629758573c6b2b9` / `0e6a0197f578f681c91f76afbf9415d36f6e732a83fa684e487ba9c771634cc9` |
| BASE_c2 | `BK_BASE_c2` | `acf789e3e93b253855d24206f5e443da3a16c9ee4184c4858d59eda449819b84` / `b4bd5980fefdb7ea8fb2ec35ba1245b5107127c29f18e543e97be418313f7b2c` |

**Accepted existing-artifact exception.** Both were fitted with the pass-2 floor of 1/8 (`run_v2.py`, `BAKE_PK_MINW=0.125`), not the standard 1/4. Their keys' actual half-widths are:
- BASE_c1 `shoulder_abd90_xneg@1.0`: 22.5° = 0.25 × 90°.
- BASE_c2 `elbow_130_xneg@1.0`: 16.25° = 0.125 × 130°.
- BASE_c2 `elbow_90_xneg@1.0`: 22.5° = 0.25 × 90°.

Both pass the final dense audit, the local motion rule, the full suites and integrity. That evidence is reused as is.

**Regression controls** keep their recorded recipes and results:
- END_FAHI (repair 2, it3);
- END_MUFAHI (repair 2, it2).

No shipping-preset roster is designated; that is an author decision.

## 7. Reproducing the archived runs

`BAKE_RECIPE=archived` restores the pre-standard defaults:
- `BAKE_PK_MINW=0`;
- `BAKE_DENSE=0`;
- unaligned allowance;
- motion verdict = `BAKE_MOTION_RULE`, default `original`;
- motion failures reported but not fed back.

Set the run's recorded values on top:

| Run (evidence) | Runner | Settings |
|---|---|---|
| Pass 1 (`pass1/`) | `run_full.py` | `BAKE_RECIPE=archived BAKE_MOTION=0`, MAXIT 3, 4 shards |
| Pass 2 (bases; superseded endpoints) | `run_v2.py` | `BAKE_RECIPE=archived BAKE_PK_MINW=0.125 BAKE_GATE_ALIGNED_ALLOW=1 BAKE_MOTION_RULE=original`, MAXIT 3, 4 shards |
| END_FAHI repair 1 | `run_fahi_w25.py` | `BAKE_RECIPE=archived BAKE_PK_MINW=0.25 BAKE_GATE_ALIGNED_ALLOW=1 BAKE_MOTION_RULE=original`, MAXIT 3, 8 shards |
| END_MUFAHI repair 1 | `run_mufahi_dense.py` | `BAKE_RECIPE=archived BAKE_PK_MINW=0.125 BAKE_GATE_ALIGNED_ALLOW=1 BAKE_DENSE=1 BAKE_MOTION_RULE=local BAKE_SEED_EXTRA=seed_mufahi_dense.json`, MAXIT 6, 8 shards |
| END_MUFAHI repair 2 (final) | `run_mufahi_v3.py` | `BAKE_RECIPE=archived BAKE_PK_MINW=0.25 BAKE_GATE_ALIGNED_ALLOW=1 BAKE_DENSE=1 BAKE_MOTION_RULE=local BAKE_SEED_EXTRA=seed_mufahi_v3.json`, MAXIT 6, 8 shards |
| END_FAHI repair 2 (final) | `run_fahi_dense.py` | `BAKE_RECIPE=archived BAKE_PK_MINW=0.25 BAKE_GATE_ALIGNED_ALLOW=1 BAKE_DENSE=1 BAKE_MOTION_RULE=local BAKE_SEED_EXTRA=seed_fahi_dense.json`, MAXIT 6, 8 shards |

**Notes on the table:**
- The pass-1 runs predate the motion gate.
- The pass-2 motion verdicts in their own records are the first rule. The bases' local-rule results are in `out_mo/v2L`, `MO_*.local.json`.
- The fit tool for every row is `sa6_bake.py` at 35c120d8.

## 8. Rig v002 (shoulder / elbow refit correction, order 07a3f24c) — RP6 RIG PILOT / NOT FROZEN

Rig v002 is selected by `RP6_RIG=v002`. Without it every tool keeps the archived rig v001 behaviour above, bit for bit.

  baked(T) = packaged blend v006 (T) + K_body(T),  with K_body = 0 at neutral.

**Package (`reviews/rac-rp6-evidence/saurin/rig_pilot/rig_v002/`):**
- skeleton and weights v002: GH pivot at the shoulder cap, girdle coupling girdle = 0.5·max(0, humeral swing − 30°) with humeral + girdle = total (`sa6_pose.girdle_split`), axillary transition weights;
- base correctives `SA_RP6_correctives_v004.json` (+ M / F npz; `RP6_BASE_CORR`): the corrected shoulder / elbow systems of v003 (families on clavicle_* / upperarm_* / forearm_*, including the elbow muscle layer tagged `layer: muscle`, and the pose keys those bones drive) merged by `sa6_base_merge.py` with every other system from the unfaired pass 4. v003 had faired every system and left hidden pleats at the ankle, toes, tail root, pelvis and thumb (see *Pleat gate* below); v003 and layers v005 are superseded;
- creator layers `SA_RP6_creator_layers_v006.json` (`RP6_LAYERS`) + `_part*.npz`, fitted on base v004 by passes 8 and 9. `arrays` maps each part file to its states and `array_sha256` hashes each part. Loaders resolve a state's arrays with `sa6_layer_harness.layer_arrays`. Each part stays under 25 MB.

**Recipe additions (defaults of `sa6_bake_full.py`, `BAKE_RECIPE=standard`; `--recipe` prints them):**

| Setting | Value | Meaning |
|---|---|---|
| `BAKE_MOTION_REFIT` / `_MODE` / `BAKE_MOTION_GRID` | 1 / grid / step | A motion-fed pose restarts from the initialisation layer: its keys and the families on its joints are dropped, and keys and family samples are rebuilt on the sample-step grid. This replaces the doubled-floor widening of §2 that diverged (convergence regression `motion_feedback/`). |
| `BAKE_LOCAL_MARGIN` / `BAKE_LOCAL_NEAR` | 0.03 cm / 0.02 | Local contact clearance for neighbouring samples that ping-pong (convergence regression `pingpong/`). |

MAXIT 3 and all gate thresholds are unchanged.

**Fit-side corrections (rig v002 only):**
- *Fold alignment* (`FOLD_ALIGN`, `Solver.align`): a local L-BFGS pass on the remaining fold / tear quads after the cascade. It runs with fallbacks (ring, μ, ν, iterations) = (6, 20, .05, 300), (10, 20, .05, 300), (4, 2, .01, 600), (6, .2, .005, 1000).
- *Fairing* (`FAIR`, `FAIR_IT=20`): a Laplacian low-pass of the fitted displacement after each clean solve. It is kept only if the solve stays clean and |dV| is no worse. This removes the lumpy shoulder cap that no metric caught. `FAIR_SCOPE=arm` restricts it to poses that drive the corrected shoulder / elbow: fairing the unaffected systems weakened their accepted v001 shapes.
- *Pleat gate* (`PLEAT_GATE=1`, `PLEAT_DEG=90`, `Solver.pleat_edges`): an edge whose dihedral changes by more than 90° from rest counts as a tear and is repaired by the tear fix / fold align. The quad-flip gate (relcos < 0) cannot see a pleat: two neighbouring quads turned to opposite sides, each just short of flipping (relcos 0.13–0.86). Edges of the mouth slit (both quads on `head` / `rostrum_cap`) are exempt: plain LBS of the jaw poses already opens them.
- *Pleat audit* (`sa6_pleat_audit.py`): every anatomical pose and special gate at 0.25 / 0.5 / 0.75 / 1.0 on the base, each state and each knot body, against the same measurement on rig v001. A pleat outside the corrected systems that v001 does not have is a regression; mouth-slit edges that plain LBS already pleats are not counted. Evidence `rig_v002/pleat_audit/`.
- *Base protected set*: state and body rigs also hold the **base** configuration's rigid set by vertex id (`sa6_correctives.base_protect`: head unit, rigid claw caps, rigid landmarks + 2 rings), so state layers and bakes cannot drift rigid landmarks.
- *Combined gates*: shoulder_abd90 + elbow90, shoulder_flex60 + elbow130 and shoulder_abd45 + elbow130, on both sides.

**Running it on the PC:** use `portable/run_standard_v2.py` (+ `START_STANDARD_V2.bat`) in the `SaurinRP6_v2` bundle. It forces `RP6_RIG=v002` and the standard recipe, and removes stray overrides. It also records hardware, worker settings, tool and package sha256 and timings in `run_meta.json` / `timings.jsonl`.

Output goes to `out_std_<sha8 of correctives v004 json + layers v006 json>` (`STD_BASE` / `STD_LAYERS`; `STD_REPO` / `STD_TOOLS` select the deployed package and tools, `STD_PLEAT=1` the pleat gate), so a resumed run never mixes packages. Before running, verify the deployed tools against the commit, byte for byte.

**Acceptance** needs everything in §5, plus the motion playback (real time and ×4 slow) and the tail review, both on the v002 artifact.
