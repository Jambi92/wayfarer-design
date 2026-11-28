# END_FAHI hip_flex70_xpos motion grid from it5 (pass 9c, PC) — RP6 RIG PILOT / NOT FROZEN

**Setup.**
- END_FAHI it5 (MAXIT 5, 1/3 motion grid) ended with two failures, both on hip_flex70_xpos:
  - a local-motion excess of 0.055 cm at pelvis vertex 1309, frames 0.825–0.858;
  - one pleat edge at 0.325–0.35.
- `portable/exp_grid_v2.py` refits that pose from it5 with the it6 sample list (`extra_it6`), once per key grid. It then runs the standard motion (local rule), sweep (0.025) and dense (0.0025) stages on the pose.

| grid | converged | motion local excess (cm) | K max (cm) | sweep failing | dense failing |
|---|---|---|---|---|---|
| 0.5 | yes (6 rounds) | **-0.028 (pass)** | 5.19 | none | 0.6625 / 0.665 / 0.6675 |
| 0.4 | yes | +0.105 | 2.16 | none | none |
| 1/3 | yes | +0.055 | 2.69 | none | none |
| 0.3 | yes | +0.372 | 2.30 | 3 | 29 (0.4025–0.47) |
| 0.25 | yes | +0.034 | 3.32 | none | none |

**Motion ramp.** `BAKE_MOTION_RAMP` (`exp_fahi_ramp_it6`, stopped) was run with beta 0.8 on the 0.4 grid. The ramp phase had 0 entering samples, but motion was identical to the plain 0.4 grid. The excursion comes from the thigh families, not the pose keys, so the ramp option stays off; it remains in the tools at its default of 0.

**Decision.** `portable/RESUME_P9C_END_FAHI.bat` resumes END_FAHI with STD_MAXIT 7 and hip_flex70_xpos grid 0.5 (tools13). The three dense samples feed it7.
