# RAC RM-OT-05E — Gorrund structural-readability closure evidence

Non-canon diagnostics for `reviews/claude-rac-rm-ot-05e-gorrund-structural-readability-closure-gate.md`. Every candidate is **NOT ACCEPTED**. Gorrund failed the replicated gate, so Stage C did not run.

Route: the 05D route is unchanged (accepted 05B skeleton route, `race_base` organization, true skeletal floor, volume restoration) with 05E Gorrund specs. Baseline: Gorrund 05D E1.

| Path | What |
|---|---|
| `candidates.json` | Gorrund P1 / P2 / P3 specs |
| `sheets/e_GO_{F,Q,P,RQ}_grey`, `e_GO_{F,P}_sil` | reference candidates with Marchfolk, Skarn 229, Grask E3, Gorrund E1 and E2 |
| `sheets/e_GO_low_*`, `e_GO_frames_*` | low composition; Narrow / reference / Broad |
| `sheets/c_229_*` | close strips: knee / shank / ankle, elbow / forearm / wrist, back / sacrum / thorax, pelvis |
| `sections/` | limb rms-radius profiles and taper index (`e_limb_profiles.*`), exact sections at skeleton-anchored heights, posterior sagittal profile |
| `guards/guard_all.json` | §8 guards for 12 bodies |
| `blind/` | run A (set J) and run B (set K): sheets, keys, raw scorer outputs (`blind_results_run{A,B}.md`), `blind_summary.json` |
| `search/` | preview specs F / G / H / I, their generators and preview sheets |
| `construction/` | build, guard and package logs |

Drivers are in `tools/rac/w1/rmot05e_drivers/`: `e_guard.py`, `e_package.py`, `e_sections.py`, `e_blind.py`. The builds use `rmot05d_drivers/d_build.py`.
