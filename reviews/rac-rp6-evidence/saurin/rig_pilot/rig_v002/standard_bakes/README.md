# Rig v002 standard bakes (order 07a3f24c §4) — RP6 RIG PILOT / NOT FROZEN

The bakes ran on the PC (TylersPC, AMD 16 logical CPUs) with `portable/run_standard_v2.py`, using the approved standard recipe, 8 shards per stage, 1 thread per process.

## BASE_c1 and BASE_c2
- **Run:** `out_std_7bf72d1d`, started 2026-11-22 06:46.
- **Package hash:** `7bf72d1d` = base correctives v003 + the pass-6 creator layers v005.
  - A BASE body has every creator weight at 0.
  - The layer identity check shows that zero influence reproduces the base exactly (`weight0_minus_base_cm` 0.0 on all 19 states, `SA_RP6_layer_identity_rigv002.json`).
  - So these bakes are unchanged by pass 7: the pass-7 package differs only in its creator layers.
- **BASE_c1:** accepted candidate at it1.
  - The unbaked sweep had 1 failing sample: a knee_90_xpos contact at 0.99722.
  - it1 added 1 family.
  - it1 is clean on all stages: EV, the 56 special gates, the sweep, motion, dense (4457 samples, 0 bake failing), integrity, and before/after (1 failing → 0).
- **BASE_c2:** accepted candidate at it1.
  - The unbaked sweep had 8 failing samples:
    - shoulder_abd90_xneg volume failures, +131 to +273 cm³ at 0.55–0.70 (the v003 base between its fit samples);
    - the knee contact at 0.99722.
  - it1 added 2 families and 6 pose keys.
  - it1 is clean on all stages: dense 4474 samples with 0 bake failing (84 prod failing), integrity, and before/after (8 → 0).
- `it0` is the plain fit, which added nothing; its failures were fed to it1.
- The final `rp5lit` line in each log is the RP5-literal diagnostic. It is not a gate.

## END_FAHI and END_MUFAHI
- **Run:** `out_std_248508ec`, on the pass-7 package from `repo7\` and `tools7\`.
- These rows are filled in when that run finishes.
