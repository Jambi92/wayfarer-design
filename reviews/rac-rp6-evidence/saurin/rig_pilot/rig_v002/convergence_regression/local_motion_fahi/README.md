# END_FAHI local-motion miss after the third refit (pass 9b, package b9f3b808) — RP6 RIG PILOT / NOT FROZEN

## Finding
On your PC, `out_std_b9f3b808\END_FAHI` ended it3 with every stage clean except one motion pose:
- **The miss:** hip_flex70_xpos, bake 0.544 cm/frame against production 0.618. The pose-level limit passes, but the **local** rule fails by 0.044 cm.
- **Where:** pelvis vertex 28547 at 56.9–59.2° (fractions 0.8125 → 0.8458). There the bake moves 0.544 cm in one frame while production moves 0.343, so the allowance is the 0.50 cm cap.
- **Why more refits won't clear it:** it2 and it3 were essentially identical (local excess 0.041 / 0.044). Their motion-feedback sample lists are the same, so a further refit on the step grid repeats the result.

## Experiments (cloud, `run*.sh`)
Each refit is restricted to hip_flex70_xpos (`BAKE_ONLY_POSES`), initialised from the PC it2 artifact (as it3 was), with the it3 extra list.

| variant | motion-fed key grid | fit | hip_flex70_xpos motion |
|---|---|---|---|
| control | the PC it3 artifact | — | FAIL, local excess +0.0440 (reproduces the PC) |
| A | doubled floor, 0.5 (`BAKE_MOTION_GRID=floor`) | **diverged** (56 entering at round 7) | PASS −0.0347 |
| B | 0.125 | converged | FAIL +0.1925 (bake 0.773) |
| C | 0.25, keys only (`gridkeys`: family samples not snapped) | not converged (stopped at the time limit, rounds 5–30 entering) | — |
| **D** | **1/3 (0.3333, 0.6667, 1.0)** | **converged** | **PASS −0.0022** (bake 0.498, k 0.384) |
| E | 0.2 | converged | FAIL +0.1679 |

## Adopted
D, for this pose only: `BAKE_MOTION_GRID_POSE=hip_flex70_xpos=0.33333` (`sa6_bake.py`; every other motion-fed pose keeps the standard step grid).
- **How it runs:** END_FAHI is resumed with `STD_MAXIT=4` (`RESUME_P9B_END_FAHI.bat`, tools11). it0–it3 are reused, and it4 is the full fit plus every stage of the standard (EV, gates, sweep, gate transitions, motion, dense, integrity).
- **Grid note:** the 1/3 grid holds the key 1.0 twice (a rounding effect of the 0.33333 spacing). It is kept, because that is the tested configuration.
