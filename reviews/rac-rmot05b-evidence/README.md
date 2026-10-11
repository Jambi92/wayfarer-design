# RAC RM-OT-05B — Grask / Gorrund surface-anatomy evidence

NON-CANON diagnostics for `reviews/claude-rac-rm-ot-05b-grask-gorrund-surface-anatomy-gate.md`. Every candidate is PENDING AUTHOR. The gate did not pass.

## Recipe

- **`cfg_final.json`:** the final recipe. It contains:
  - the 05A architecture (`GR`, `GO`), with the 05B Gorrund knee, lumbar-depth, S5/S2 and PV-D14 corrections and the Narrow knee / elbow holds;
  - the race surface-anatomy stage (`surface.GR`, `surface.GO`), applied by `tools/rac/w1/race_surface.py` through `skeleton_envelope.make(surface=…)`.
- **Route:** accepted skeleton → 05A architecture → race surface (tissue + base-surface relief topology, skeleton-guarded, volume-renormalized per region) → composition → surface.

## Directory contents

| Path | Contents |
|---|---|
| `sheets/b_<H>_<F\|P\|Q\|RQ>_body.jpg`, `b_<H>_<F\|P>_sil.jpg`, `b_<H>_Q_grey.jpg` | W2 → 05A → 05B lineups at 208 / 218 / 229, against Marchfolk and Skarn controls |
| `sheets/b_stature_GR_*.jpg`, `sheets/b_stature_GO_*.jpg` | stature transport: Grask 198–239; Gorrund 208–251, including 230.9 |
| `sheets/b_frames_comp_*.jpg` | Narrow / reference / Broad and low-composition states, with Skarn controls |
| `sheets/c_229_*.jpg`, `sheets/c_218_*.jpg` | close anatomical sheets |
| `blind/` | set Q (the 05B set, plus Marchfolk and Skarn controls), grey and silhouette, `key_B05.json`, and `blind_results.json`. The results file holds all three scored runs; "final" is the gate result. |
| `validators/` | W2C and W2D reruns (`w2c.json`, `w2d.json`, registries, joint inputs, logs), `tables.json`, `contour.txt`, `arm_clearance.txt` |
| `construction/` | build records of every candidate and every transported `B_*` body |
| `search/` | surface recipes `surf_s1`–`s7`, the pre-guard configuration `cfg_B1.json`, preview sheets `p_s*` and the uninformed-reviewer probe `blindq_s7` |

## Drivers

All in `tools/rac/w1/rmot05b_drivers/`:

| Driver | Builds |
|---|---|
| `b_build.py` | the candidates |
| `b_transport.py` | named extremes and composition states |
| `b_eval.py` | the validator reruns |
| `b_package.py` | the evidence sheets |
| `b_blind.py` | the blind sets |
| `b_evidence.py` | this directory |
| `b_preview.py`, `b_try.py`, `b_blindq.py` | search tools |
