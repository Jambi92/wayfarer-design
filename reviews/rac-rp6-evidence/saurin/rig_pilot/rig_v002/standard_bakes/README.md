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
- **Run:** `out_std_248508ec`, on the pass-7 package from `repo7\` and `tools7\`. Started 2026-11-22 19:03 (PC time); finished 11-24 00:08 (END_FAHI) and 00:34 (END_MUFAHI); 29.5 h wall for the pair.
- **END_FAHI:** accepted candidate at it3.
  - The unbaked run had 28 failing samples: shoulder_abd45_xneg 6, shoulder_abd90_xneg 3, hip_flex70_xpos 16, hip_flex70_xneg 3.
  - it1 added 3 families and 1 pose key; 1 sweep sample remained.
  - it2 added 3 pose keys; dense audit found 2 hip_flex70_xpos samples at 0.915 / 0.9175.
  - it3 is clean on every stage, including the dense audit (4094 samples, 0 bake failing; 294 prod failing) and integrity.
  - Before / after: 28 failing → 0.
- **END_MUFAHI:** accepted candidate at it3.
  - The unbaked run had 18 failing samples.
  - it1 added 5 families and 4 pose keys.
  - it2's dense audit found 4 hip_flex70_xpos samples.
  - it3 is clean on every stage, including the dense audit (0 bake failing) and integrity.
  - Before / after: 18 failing → 0.
- **Motion review (both):** passes. The worst case is END_MUFAHI shoulder_abd90_xpos at 0.93 cm/frame, with bake = prod. The baked body adds no motion of its own there.
- **Before/after label:** the `unbaked` field in `BA_*.json` says "packaged blend v004". That is a fixed label in `sa6_bake_beforeafter.py`, now corrected to name the package actually loaded. These runs loaded v005 (`RP6_LAYERS`, `run_meta_248508ec.json` package_sha256).

## Pass 9b rebakes on package `b9f3b808` (base correctives v004 + creator layers v006) — `b9f3b808/`
These supersede the bakes above. Those were baked on base correctives v003, which pass 8 replaced with v004 (§4.5 of the report), so the BASE bodies had to be rebaked too.
- **Run:** `out_std_b9f3b808` (`run_meta_b9f3b808.json`), started 2026-11-25 07:24 (PC time) from `START_P9B_BAKES.bat`: `repo9\` + `tools10\`, `PLEAT_GATE=1` with the per-body v001 crease union (`PLEAT_ALLOW_UNION`, `data9b\union`). The four bodies ran in parallel beside the 18-body held-out recheck.
- **Per-pose pleat audit of each final baked artifact** against rig v001 (`sa6_pleat_audit.py` with `BAKE_ART`, 360 poses / fractions): `../pleat_audit/SA_RP6_pleat_audit_bake_<body>_b9f3b808_it*.json`.
- **BASE_c1:** accepted candidate at it2 (finished 11-26 01:09; 17.7 h of stage wall; every stage attempt 0).
  - Unbaked / it0 sweep: 3 failing samples, fist_xpos tears at 0.825–0.875 (3–4 tear edges; LBS-owned, no region).
  - it1 added 2 families and 1 pose key, which cleared them, but left 1 rig flip at gate:hand_opposition_f2_xpos.
  - it2 is clean on every stage: EV, the 56 special gates, the sweep, gate transitions, motion (worst shoulder_abd90_xneg 0.73 cm/frame), dense (4863 samples, 0 bake failing; 80 prod failing), integrity. Before / after 3 → 0.
  - Pleat audit of the it2 artifact: clean.
- **BASE_c2:** accepted candidate at it2 (finished 11-26 01:31; 18.1 h).
  - Unbaked / it0 sweep: 10 failing samples, shoulder_abd90_xneg 7 and fist_xpos 3.
  - it1 added 3 families and 7 pose keys; 1 rig flip remained at gate:hand_opposition_f2_xpos.
  - it2 is clean on every stage: motion worst shoulder_abd90_xneg 0.66 cm/frame, dense 4880 samples with 0 bake failing (161 prod failing), integrity. Before / after 10 → 0.
  - Pleat audit of the it2 artifact: clean.
- Peak memory per process: 3.58 GB (the motion stage), the same as the earlier bakes.
- The `clean False` line before BEFORE/AFTER in each log is the RP5-literal diagnostic (`rp5lit`), not a gate.
