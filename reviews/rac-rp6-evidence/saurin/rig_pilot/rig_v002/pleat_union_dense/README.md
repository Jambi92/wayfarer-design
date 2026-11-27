# Dense pleat allowance for END_MUFAHI (pass 9c) — RP6 RIG PILOT / NOT FROZEN

**Why.** The pass-9b END_MUFAHI standard bake on package `b9f3b808` never converged on hip_flex70_xpos. Its it1 and it2 fits ended `converged False`, and it2 failed motion at 1.09 cm/frame with K up to 6.0 cm. The cloud refits of that pose with the 1/3 and 0.5 key grids also stayed at about 110–120 entering samples per round.

**Cause.** The bake's pleat gate allowance (`PLEAT_ALLOW_UNION`, `sa6_pleat_union.py`) was the union of edges the body's rig v001 references pleat at 0.25 / 0.5 / 0.75 / 1.0 only. The sweep, motion and dense stages sample far finer: 0.025, 1/30 and 0.0025.
- On this heavy body the belly fold at deep hip flexion moves across neighbouring edges between those four fractions. The unbaked body's 21 sweep failures on the pose were 1–4 such edges, with v006 pleat counts equal to v001's at the same fraction (62.5 %: 22 vs 22).
- The fit then fought a fold rig v001 also has.

| Hip_flex70_xpos, unbaked v006, pleated edges outside the allowance | 4-fraction union | dense union |
|---|---|---|
| fractions with any (0.025 step) | 17 | 3 (0.575, 0.6, 0.625: 1 edge each) |

**Allowance.**
- `pleat_union_END_MUFAHI.npz` = the 4-fraction union (680 edges) OR the per-edge maximum over every anatomical pose and special gate at every 0.0125 (`v001_*_max_d0125.npz`, `sa6_pleat_audit.py measure` with `PLEAT_MAXONLY=1`, `PLEAT_FRACS` 0.0125…1.0) > 88 deg. The result is 825 edges.
- It is a superset of the 4-fraction rule, so bakes accepted under the old allowance also pass the new one.
- The per-pose verdict is unchanged: the pleat audit of the baked artifact against v001 at 0.25 / 0.5 / 0.75 / 1.0.

**Files.**
- `*_hip70xpos_d025.npz`: the 0.025-step diagnostic of the pose (v001 state MUFAHI and unbaked v006 END_MUFAHI).
- `diag.py`: the defect breakdown of the checkpoints. It shows K on the 1/3 grid making 34 folds and 42 tear/pleat edges at 0.8, against 7–10 folds with no tears on the plain blend.

**Run.** `portable/START_P9C_END_MUFAHI.bat` stops the 9b END_MUFAHI run (its record stays in `out_std_b9f3b808\END_MUFAHI`) and starts a fresh standard bake. It uses `tools11`, `STD_UNION=data9c\union` and `STD_OUT_TAG=_u2`, so the output goes to `out_std_b9f3b808_u2\END_MUFAHI`. STD_MAXIT is the standard 3.
