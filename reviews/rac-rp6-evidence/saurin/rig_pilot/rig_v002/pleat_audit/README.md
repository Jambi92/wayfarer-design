# Hidden-pleat audit and base correctives v004 (order 07a3f24c §4) — RP6 RIG PILOT / NOT FROZEN

## What was found
The v002 tail review showed a visible crease at the tail root on BASE_c1, tail_root_biased_60 (`tail_review/renders/TM_BASE_c1_*`). The rig v001 bake has no such crease there.
- Tail concentration at ring 1 went from 0.49° (v001) to 1.73° (v003). The criterion still says PASS (≤ 2.0°), but the crease is visible.
- **Cause:** base correctives v003 (PC pass 5) started from `sa6_fair_keys.py`, which low-pass filtered *every* corrective key of the body, and the refit then faired after every clean solve. Fairing was meant for the shoulder cap. Applied to the unaffected systems, it weakened their accepted v001 shapes, and the fold align then cleared the LBS folds only just past the flip threshold. The result is near-vertical **pleats** between neighbouring quads: posed dihedral change > 90°, relcos about 0.15 on both sides.
- These pleats are at the ankle, toes, tail root, pelvis, thumb and jaw. No gate sees them, because no quad flips.

## The audit
`sa6_pleat_audit.py`:
- Measures, on every quad edge, |posed − rest dihedral| for the 34 anatomical poses and all special gates, at 0.25 / 0.5 / 0.75 / 1.0 (the first audits used 0.5 and 1.0 only and missed a pleat at 0.75).
- Counts pleats (> 90°) on edges outside the corrected systems (clavicle / upperarm / forearm) and compares the count with the accepted rig v001 baseline.
- Pleats inside the corrected systems are reported for visual review.
- Mouth-slit edges that plain LBS of the pose already pleats are the jaw opening and are not counted. Poses rig v001 does not have (the combined shoulder + elbow gates) count against zero.

| Base set | M: poses with new pleats outside the shoulder / elbow | F |
|---|---|---|
| v003 (pass 5) | 49 poses, +859 pleat edges | 50 poses, +854 |
| **v004** | **0** | **0** |

## Base correctives v004
`sa6_base_merge.py`:
- clavicle / upperarm / forearm families (including the elbow muscle layer) and the pose keys they drive come from v003;
- every other family and pose key comes from pass 4, before fairing, which equals the accepted v001 shapes.

A variant that took the forearm from pass 4 as well was rejected: its elbow at 130° renders broken (jagged forearm cuff).

**Evaluation** (`base_v004_eval/`, `sa6_eval.py`, 34 anatomical + RP5-literal + 56 special gates, each at 0.25 / 0.5 / 0.75 / 1.0):
- 0 corrected flips, 0 new penetration and 0 tears on every realisable pose, M and F.
- The only residuals are on the three non-realisable RP5-literal tail poses and the literal jaw closure, the same class as v003 / v001. They are not gated.

**Inside the corrected systems:** elbow_90 has 2 / 7 (M) and 6 / 13 (F) pleat edges in the antecubital flexion crease, against 0–2 on v001. They are the same as v003, whose close-ups were reviewed as a natural fold (`visual/elbow_muscle/`).

Recheck at all four fractions with the mouth rule: M and F clean (`SA_RP6_pleat_audit_base_{M,F}_v004_4frac.json`).

## State layers: passes 8, 9 and 9b
**Pass 8** (`portable/run_v2_pass8.py`, base v004, `FAIR_SCOPE=arm`): regressions on BRD, B-T80 (toe_flex30 6, foot_pushoff 2, ankle_plantar25 1), LT90 (toe, jaw 32) and MUFAHI (lower_axial_flex_25 57 → 71). The init layers were clean; the pass-8 fit made them (`SA_RP6_pleat_audit_state_*_pass8.json`).

**Pass 9** (`run_v2_pass9.py`): pleat gate in the fit (`PLEAT_GATE=1`, `sa6_correctives.Solver.pleat_edges`): an edge turned > 90° from rest counts as a tear and is repaired. Findings:
- the first mouth exemption (every head / rostrum_cap edge, 25k) let LT90 grow 10 pleats under the jaw (jaw / neck_02 blend, LBS 1–8°, layer 94–143°) at gate:jaw_open_32. The exemption is now the slit proper (`Solver._slit`: head / rostrum_cap edges plain LBS pleats in a jaw pose, 83 edges);
- F-N, DSP-LOW and LT90 stayed unconverged on 4 edges each: knuckle creases that v001 also has (fist / hand_opposition), and a deep skin fold at the F-N shoulder at abd90 (upperarm / spine_02 seam: LBS 67–75° with 21 flips, layer ~100°) that neither the tear fix, the fold align nor local smoothing removes.

**Pass 9b** (`run_v2_pass9b.py`): gate scope = this audit's regression scope: edges outside the corrected systems, less the edges the v001 state already turns > 88° at that pose (`sa6_pleat_allow.py`: 90° less 2° tolerance; one MUFAHI hip_flex70_xpos pelvis edge sat at v001 90.0° / layer 90.x° through every round). Starts: the most advanced pass-9 result per state; MUFAHI and FAHI from pass 8 (`RESTART_9B_HEAVY.bat`, `RESTART_9B_MUFAHI.bat`: the pass-9 strict fits had left corrective pleats and volume misses in their composition-masked belly / pelvis, e.g. MUFAHI hip_flex70_xpos 50 % dV −1435 cm³).

**Result:** 19 / 19 state layers converged, 19 / 19 clean against rig v001 at all four fractions (`SA_RP6_pleat_audit_state_*_pass9b.json`). <!-- KNOTS9B -->

**Corrected-system pleats for visual review** (`arm/`): MUHI shoulder_abd90_xneg 14 edges at the armpit fold, where plain LBS pleats too; F-N 4 (the shoulder fold above); FAHI 12; elbow_130 on NAR / ORB+3 / RDG0.90 / RDG1.30 / FAHI 4–25, the range base v004 has at the elbow crease. <!-- ARMREVIEW -->

## Downstream
- Creator layers v006 = the pass-9b layers and knots; then the standard bakes and the held-out recheck are rerun.
- The `248508ec` package, and the bakes and held-out run made on it, are superseded.
