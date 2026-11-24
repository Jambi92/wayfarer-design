# Hidden-pleat audit and base correctives v004 (order 07a3f24c §4) — RP6 RIG PILOT / NOT FROZEN

## What was found
The v002 tail review showed a visible crease at the tail root on BASE_c1, tail_root_biased_60 (`tail_review/renders/TM_BASE_c1_*`). The rig v001 bake has no such crease there.
- Tail concentration at ring 1 went from 0.49° (v001) to 1.73° (v003). The criterion still says PASS (≤ 2.0°), but the crease is visible.
- **Cause:** base correctives v003 (PC pass 5) started from `sa6_fair_keys.py`, which low-pass filtered *every* corrective key of the body, and the refit then faired after every clean solve. Fairing was meant for the shoulder cap. Applied to the unaffected systems, it weakened their accepted v001 shapes, and the fold align then cleared the LBS folds only just past the flip threshold. The result is near-vertical **pleats** between neighbouring quads: posed dihedral change > 90°, relcos about 0.15 on both sides.
- These pleats are at the ankle, toes, tail root, pelvis, thumb and jaw. No gate sees them, because no quad flips.

## The audit
`sa6_pleat_audit.py`:
- Measures, on every quad edge, |posed − rest dihedral| for the 34 anatomical poses and all special gates, at 0.5 and 1.0.
- Counts pleats (> 90°) on edges outside the corrected systems (clavicle / upperarm / forearm) and compares the count with the accepted rig v001 baseline.
- Pleats inside the corrected systems are reported for visual review.

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

## Downstream
- Pass 8 refits the 19 state layers and 20 knots on v004 (`portable/run_v2_pass8.py`, `FAIR_SCOPE=arm`).
- Creator layers v006 follow, then the standard bakes and the held-out recheck are rerun.
- The `248508ec` package, and the bakes and held-out run made on it, are superseded.
