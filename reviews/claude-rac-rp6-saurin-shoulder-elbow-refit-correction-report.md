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

### 4.4 Standard bakes (BASE_c1, BASE_c2, END_FAHI, END_MUFAHI)
The record is `standard_bakes/README.md`; the per-body `ACCEPT_*.json`, `FULL_*.json`, logs and the final-iteration records are next to it.

**Where and how:**
- They ran on the PC (TylersPC, 16 logical CPUs) with `portable/run_standard_v2.py`: standard recipe (`BAKE_PK_MINW=0.25`, `BAKE_DENSE=1`, `DENSE_STEP=0.0025`), 8 shards per stage, 1 thread per process, below-normal priority, MAXIT 3.
- Each run records the hash of every deployed tool and package file (`run_meta_*.json`). The tools were checked against the committed versions before each run.
- **Stages per iteration:** the 34 anatomical poses at 25 / 50 / 75 / 100 % plus neutral, the 56 special gates (the 50 named in the order, plus the 6 combined shoulder + elbow gates) at the same fractions, the full sweep, gate transitions, motion at the documented playback speed, and the dense audit. Then integrity (save, reopen, re-evaluate) and before / after.

| Body | Package | Accepted at | Unbaked failing samples | After | Dense audit (bake failing) | Wall | Peak memory per process |
|---|---|---|---|---|---|---|---|
| BASE_c1 | `7bf72d1d` | it1 | 1 (knee_90_xpos contact) | 0 | 4457 samples, 0 | 14.1 h | 3.57 GB |
| BASE_c2 | `7bf72d1d` | it1 | 8 (shoulder_abd90_xneg volume, knee contact) | 0 | 4474 samples, 0 | 14.9 h | 3.57 GB |
| END_FAHI | `248508ec` | it3 | 28 (shoulder abd45 / abd90, hip_flex70) | 0 | 4094 samples, 0 | 29.1 h | 3.60 GB |
| END_MUFAHI | `248508ec` | it3 | 18 | 0 | 0 | 29.5 h | 3.62 GB |

- Wall is the sum of the stage wall times. The two pairs ran in parallel.
- **Why BASE uses `7bf72d1d`:** a BASE body has every creator weight at 0, and zero influence reproduces the base exactly. So pass 7, which changed only the creator layers, does not change a BASE bake.
- **Motion review:** passes on all four. The worst case is END_MUFAHI shoulder_abd90_xpos at 0.93 cm/frame, where bake = prod.
- **Integrity:** clean on all four. Neutral is 0, and the rigid landmarks stay at 0.

**Interruptions:**
- The first END_FAHI and END_MUFAHI bakes ran on the pass-6 package. They were stopped when their unbaked special gates failed (§4.2), and then rebaked from scratch on the pass-7 package.
- No other stage was restarted: `attempt` is 0 on every stage of every `FULL_*.json`.

<!-- BAKES-V006 -->

### 4.5 Hidden pleats: base v004, passes 8, 9 and 9b (creator layers v006)
The v002 tail review of the bakes above found a crease at the tail root. The cause, and further findings, are in `rig_v002/pleat_audit/README.md`.

**What no gate saw.** Two neighbouring quads folded into a near-vertical ridge, each just short of the flip test (relcos 0.13–0.86): a **pleat**. `sa6_pleat_audit.py` measures, for every quad edge, the change of its dihedral angle from rest on every anatomical pose and special gate at 0.25 / 0.5 / 0.75 / 1.0, and compares with the same measurement on the accepted rig v001. A pleat (> 90°) outside the corrected systems (clavicle / upperarm / forearm) that v001 does not have is a regression. Pleats on the corrected systems are listed for visual review; v002-only gates (the combined shoulder + elbow gates) count against zero.

**Base v003 → v004.** Base v003 had been faired everywhere (meant for the shoulder cap only). That weakened the unaffected systems and left pleats at the ankle, toes, tail root, pelvis and thumb. Base v004 (`sa6_base_merge.py`) = the corrected shoulder / elbow systems of v003 + every other system from the unfaired pass 4. M and F are clean at all four fractions.

**Pass 8** refit the 19 states and 20 knots on base v004 with fairing limited to the arm poses (`FAIR_SCOPE=arm`). Its audit found new pleats on BRD, B-T80 (toe flex, foot push-off, ankle plantar), LT90 (toe, jaw 32) and MUFAHI (lower axial flex) — created by the fit itself.

**Pass 9** added a pleat gate to the fit (`PLEAT_GATE=1`: an edge turned > 90° from rest is repaired like a tension tear). Two mismatches with the audit surfaced:
- It exempted every head / rostrum_cap edge as "mouth" (25k edges); LT90 then grew 10 new pleats under the jaw at gate:jaw_open_32. The exemption is now the slit proper: head / rostrum_cap edges that plain LBS pleats in a jaw pose (83 edges).
- It demanded zero pleats where v001 itself has them (knuckle creases) and on the corrected systems, where a deep skin fold forms (F-N shoulder_abd90: plain LBS 67–75° with 21 flips, layer ~100°; local smoothing only deepens it). F-N, DSP-LOW and LT90 cycled on the same 4 edges for 8 rounds.

**Pass 9b** gives the gate exactly the audit's scope: edges outside the corrected systems, less the edges the v001 state already turns > 88° at that pose (`sa6_pleat_allow.py`; 90° less 2° measurement tolerance). Each state started from its most advanced pass-9 result. MUFAHI and FAHI restarted from pass 8: the pass-9 strict gate had left corrective pleats and volume losses in their composition-masked belly / pelvis (MUFAHI hip_flex70_xpos 50 %: dV −1435 cm³) that the 9b refit could not remove.

**Results, pass 9b:** all 19 state layers converged; all 19 are clean against rig v001 at all four fractions (`SA_RP6_pleat_audit_state_*_pass9b.json`). <!-- KNOTS9B -->

**Arm pleats for visual review** (not regressions by the audit rule; renders in `rig_v002/pleat_audit/arm/`): MUHI shoulder_abd90_xneg 14 edges (plain LBS has pleats at the same armpit fold), F-N 4, FAHI 12; elbow_130 on NAR, ORB+3, RDG0.90, RDG1.30, FAHI 4–25, the range base v004 itself has at the elbow crease (14–25, v001 25–27). <!-- ARMREVIEW -->

**Tail review** (`tail_review/`): <!-- TAIL -->

**Playback** (`visual/playback/`):
- region and whole-body views, real-time and slow, forward / reverse, with stills at key angles;
- BASE_c1 and BASE_c2: shoulder_abd90_xneg, shoulder_flex60_xneg, elbow_130_xneg;
- END_FAHI and END_MUFAHI: their worst motion poses; these are the worst heavy-body cases. <!-- PB -->

<!-- HELDOUT -->

## 6. Packages and readback

**Blender** (`SA_M_REF_RP6_rigpilot_v002.blend.xz`, `SA_F_REF_RP6_rigpilot_v002.blend.xz`; readback in `blender_readback/`):
- Each file was reopened in a fresh Blender process and read back against the npz data and the external evaluator.

| Check | M | F |
|---|---|---|
| Bones (deform), parents, head / tail error | 108 (107), match, 7.4e-6 cm | 108 (107), match, 7.4e-6 cm |
| Weights vs npz, max influences | 0.0, 4 | 0.0, 4 |
| Shape keys (expected), delta error vs npz | 210 (210), 1.5e-5 cm | 211 (211), 1.5e-5 cm |
| Drivers valid | 292 / 292 | 293 / 293 |
| Basis = frozen RP5 neutral; corrective values at rest | yes; 0 | yes; 0 |
| Posed geometry vs external evaluator, max error | 0.000394 cm | 0.000194 cm |
| Flips in the Blender evaluation | 0 | 0 |

- The girdle coupling is driver-owned in Blender: clavicle_l and clavicle_r follow the upper arm with ratio 0.5 from 30°.

**Portable package:**
- **The PC bundle** (`sa6_portable_v2.py`): tools, the frozen RP5 files the loaders need, the rig v002 skeleton, weights and joint placements, and the cage-level data. `bundle_manifest.json` lists SHA-256 for every file.
- **Readback of PC outputs:** every layer and knot the PC produced was checked in the cloud before packaging (the PD-2 recheck, state checks and layer identity in §4.2).

**Frozen sources:** <!-- FROZEN -->

**Manifest:** <!-- MANIFEST -->

<!-- CARRY -->
