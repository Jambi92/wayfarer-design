# Pass 7 — special gates in the state-layer and knot fits (order 07a3f24c §4) — RP6 RIG PILOT / NOT FROZEN

## What the v002 standard bakes found
On the PC, the first standard bakes of the pass-6 package (`out_std_7bf72d1d`) ran the special-gate stage on the unbaked END bodies (`GT_END_*_pass6_unbaked.json`).

- **END_FAHI and END_MUFAHI fail it:** 584 rig flips, 77 contacts and 74 tears.
  - Poses: ankle dorsi / plantar 25, foot push-off / curl, jaw_open_32 and jaw32_head_pitch_up.
  - Fractions: 0.75 and 1.0.
  - The layer v004 package gave 0 on the same bodies (`offline_bake/bodies/END_FAHI/unbaked/GT_END_FAHI.json`).
- **BASE_c1 and BASE_c2 pass**, because base v003 is fitted with the gates.

## Cause
- The state layers and knots were fitted on the 34 anatomical poses only.
- Their family samples beyond the anatomical driver range were therefore never refitted. These are angles only the special gates reach: foot ±25°, jaw −24° / −32°, and so on.
- Those samples still held the rig v001 state values, which differ from base v003 by up to 2.75 cm (`SA_RP6_gate_reset_pass7.json`).
- The check on FAHI shows the two versions behave the same:
  - pass-5 and pass-6 layers give identical gate flips;
  - base v003 alone gives 0 at the ankle and foot.

## Fix
1. `sa6_gate_reset.py` resets exactly those samples to base v003. This leaves every anatomical result unchanged: the hat at an anatomical angle never reaches them.
   - FAHI after the reset: 584 → 38 flips.
   - Remaining: jaw32 (9, the same as base alone) and ankle dorsi xneg (97).
2. **Pass 7** refits all 19 state layers and all 20 knots **with the 56 special gates** (`PD2_GATES=1`, `sa6_pd2_fit.gate_set`), exactly as the base fit does.
   - Runner: `portable/run_v2_gates.py`, starting from the reset sets.
   - It runs on the PC from a separate `tools7\` copy, so the running BASE bakes keep their verified tools.
3. The END_FAHI and END_MUFAHI bakes of the pass-6 package were stopped (`STOP_END_BAKES.bat`). The BASE_c1 and BASE_c2 bakes are unaffected and continue.
