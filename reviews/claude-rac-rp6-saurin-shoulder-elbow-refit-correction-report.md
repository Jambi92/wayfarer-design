# Saurin RP6 — shoulder / elbow refit correction report (order 07a3f24c)

**Status: RP6 RIG PILOT / NOT FROZEN.** This report answers `reviews/chatgpt-rac-rp6-saurin-shoulder-elbow-refit-correction-order.md`, and stops here for review.

- **Rig v002** is selected by `RP6_RIG=v002`.
- **Rig v001** and all its artifacts are unchanged; they are the comparison baseline.
- **Evidence:** `reviews/rac-rp6-evidence/saurin/rig_pilot/rig_v002/`.
- **Recipe:** the bake standard is `tools/rac/rp/saurin_rp6_v001/BAKE_STANDARD.md`; the v002 additions are in §8.

<!-- RESULTS-TABLE -->

## 1. Shoulder (SAURIN-RP6-DEF-SHOULDER-1)

The full record is `SA_RP6_shoulder_v002_record.json`.

**Diagnosis:**
- The rig v001 glenohumeral pivot was the RP5 "glenohumeral" landmark. That landmark is a shoulder-section centroid at armpit height, about 8.4 cm below the cap.
- So abduction and flexion bent the arm inside the armpit instead of rotating it at the top of the joint.
- `clavicle` never moved, and it carried about 0.43 mean weight over the whole upper chest.

**Rig v002:**
- **Pivot:** the GH centre now sits on the upper-arm centreline, moved up to where the tissue cover straight above it equals the lateral cover. That centres the joint under the shoulder cap. It is the mean of both sides, applied on each side's own centreline.
- **Girdle coupling:** the clavicle rotates about the same axis by g = 0.5 × max(0, humeral swing − 30°), with humeral + girdle = total arm angle. That gives a 2:1 glenohumeral : scapulothoracic rhythm above 30°.
- **Clavicle weight:** it is limited to 0.45 × upper-arm length from GH.
- **Armpit:** axillary transition weights were added.
- **Weight audit:** `SA_RP6_weight_audit_v002.json`.

**Base correctives v003:** refit on rig v002, as the M and F evaluations in `base_v003_eval/` show.
- All 34 anatomical poses and all special gates are clean on both configurations. That includes the new combined shoulder + elbow gates on both sides: abd90 + elbow90, flex60 + elbow130 and abd45 + elbow130.
- **Fold alignment** (`Solver.align`): a local L-BFGS pass on the remaining fold / tear quads. It cleared the smooth-sheet fold at abd90_xneg that the ARAP / Laplacian steps cycled on.
- **Fairing** (`FAIR`): a Laplacian low-pass of each clean solve, kept only when it stays clean with no worse volume. It removed the lumpy shoulder cap that no metric had flagged.
- **Corrective audit:** `base_v003_eval/SA_RP6_corrective_audit_v003.json`.

**Before / after visuals** (`visual/shoulder_before_after/`):
- M and F, rig v001 vs v002;
- abd45, abd90 xneg / xpos, flex60, flex90, and the two combined poses;
- flip counts and the clavicle / upper-arm split for each in `stats_v001.json` and `stats_v002.json`.

**Outside the gated range:** flex90 is beyond the gated flex60 and shows 9–12 flips on v002 (`stats_v002.json`). That is carried forward (§7), not fixed.

## 2. Elbow muscle layer (SAURIN-RP6-DEF-ELBOW-MUSCLE-1)

The record is `SA_RP6_muscle_validation_v002.json`, and it **passes**.

**What the layer is:** families tagged `layer: muscle` that ride on elbow flexion. They give biceps contraction and bulge, and triceps stretch. They are part of base correctives v003 and of every state layer.

**Checks, on M, F, FAHI, MUFAHI and MUHI, both arms:**
- neutral is 0;
- the effect stays local, with landmarks fixed;
- the size is bounded;
- the biceps rises monotonically and holds beyond 130°;
- it is independent of the shoulder pose;
- the volume change stays within 1 % of the upper arm (max 0.32 %).

**Close-ups** (`visual/elbow_muscle/`):
- elbow 0 / 45 / 90 / 130°, lateral and anterolateral views, with and without the layer, plus a heat map of the layer itself;
- a combined abd90 + elbow 0 / 90 / 130 strip;
- bodies: base M, base F, and the heavy FAHI and MUFAHI on their pass-7 state layers.

## 3. Convergence (order §3)

The details are in `convergence_regression/README.md`, using END_MUFAHI with the archived v001 inputs.

- **Ping-pong between neighbouring contact samples:** fixed by local contact clearance (`BAKE_LOCAL_MARGIN` 0.03 cm, `BAKE_LOCAL_NEAR` 0.02). The fit converged with MAXIT and thresholds unchanged.
- **Widening motion-feedback tear:** fixed by a motion-fed refit. The pose restarts from the initialisation layer and its keys and family samples are rebuilt on the step grid. The fit converged in 2 rounds, and the motion review passes.
- **Rejected variants:** grid keys on every pose, restart without keys, doubled-floor grid. Each one failed.

Both fixes are standard-recipe defaults (`BAKE_STANDARD.md` §8).

## 4. Rebuild (order §4)

### 4.1 Base protected set held on state and body rigs
The END_MUFAHI bake of an earlier package showed rigid-landmark drift.
- **Cause:** state layers moved base-rigid vertices (up to 0.141 cm, MUFAHI), because the state / body rigs had re-found landmarks on their own geometry.
- **Fix:** state and body rigs now also hold the **base** configuration's protected set by vertex id (`sa6_correctives.base_protect`).
- **Clean-up:** the drift was zeroed (`sa6_zero_protect.py`) and the layers refit (pass 6).
- **Result:** the protected-set displacement is 0 on all 19 states (`SA_RP6_state_layer_rigid_check_rigv002.json`).

### 4.2 Special gates in the state-layer / knot fits (pass 7)
The first v002 standard bakes found a regression (`pass7_gates/README.md`). On the pass-6 package, the unbaked END_FAHI / END_MUFAHI failed the special gates:
- 584 rig flips, plus contacts and tears;
- at the ankle dorsi / plantar, foot push-off / curl and jaw 32 gates;
- the v004 package gave 0 on the same bodies.

**Cause:**
- The state layers and knots were fitted on the anatomical poses only.
- Their family samples beyond the anatomical range had been carried over from the rig v001 state sets.
- Those samples differed from base v003 by up to 2.75 cm.

**Fix:**
- `sa6_gate_reset.py` resets exactly those samples to base v003.
- Pass 7 refits all 19 states and 20 knots **with the 56 special gates** (`PD2_GATES=1`), as the base fit already did.

**Results, all 19 states and 20 knots converged:**
- **PD-2 recheck:** 19/19 clean (`SA_RP6_pd2_recheck_pass7_rigv002.json`).
- **Protected-set displacement:** 0, with 0 rig-owned special-gate flips on all 19 (`SA_RP6_state_checks_pass7_rigv002.json`).
- **Layer identity:** exact on every state (`SA_RP6_layer_identity_rigv002.json`).

### 4.3 Package
- Creator layers v005 = `SA_RP6_creator_layers_v005.json` + `_part1 … _part8.npz`.
- Each part is under 25 MB, and `array_sha256` hashes each part.
- The runtime contract is in the PD-2 interface doc, in the rig v002 section.

<!-- BAKES -->

<!-- HELDOUT -->

<!-- PACKAGES -->

<!-- CARRY -->
