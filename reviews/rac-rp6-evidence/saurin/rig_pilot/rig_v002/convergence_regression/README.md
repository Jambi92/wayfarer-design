# Convergence regression checks (order 07a3f24c §3) — RP6 RIG PILOT / NOT FROZEN

Both checks ran on END_MUFAHI with the archived rig v001 inputs, using the same tools as the standard bake. They are isolated regression checks for the two convergence failures recorded in the standards closure. The v002 rebakes on the PC repeat them through `sa6_bake_full.py`.

## pingpong/ — neighbouring-sample contact ping-pong (trunk_twist_30, fractions 0.58333 / 0.59167)
- `fitA.log`: baseline. The two neighbouring dense samples alternate (each solve clears its own sample and re-breaks the other), so the fit stays at 2 entering for every round until MAXIT. This is the reproduced failure.
- `fitB.log`: variant with grid keys on every pose (`BAKE_PK_GRID_ALL`). Same alternation, so it was rejected.
- `fitC.log`: **adopted**. Local contact clearance `BAKE_LOCAL_MARGIN=0.03` (neighbour window `BAKE_LOCAL_NEAR=0.02`). When the two samples ping-pong, both are solved with a 0.03 cm local margin. Result: converged True, 0 entering, MAXIT and thresholds unchanged.
- `dsC.log` / `DS_END_MUFAHI.json`: dense audit of trunk_twist_30 after fitC (429 samples). The bake fails 8 samples against 138 for the production reference; the 8 sit at 0.58334–0.59 and 0.64–0.6475. They are reported, not hidden.
- `extra.json`, `extra_it4.json`: the motion / dense feedback sample lists fed to the fits.

## motion_feedback/ — widening motion-feedback tear (shoulder_abd90_xneg)
- `fit.log`: the motion-fed pose restarts from the initialisation layer (`BAKE_MOTION_REFIT=1`, mode `grid`, `BAKE_MOTION_GRID=step`). Its pose keys and the families on its joints are dropped, and keys and family samples are rebuilt on the step grid. Result: converged in 2 rounds.
- `chk.log`: 0 failing quads at every fraction checked (0.25 … 1.00) for abd90, abd45 and flex60.
- `mo.log`, `MO_END_MUFAHI.json`: motion review PASS for all three poses.
- Variants that failed and were rejected:
  - restart dropping keys only: geometry clean, motion failed;
  - doubled-floor grid: diverged;
  - no keys: motion failed.
