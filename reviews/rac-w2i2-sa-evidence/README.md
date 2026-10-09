# RAC W2I2 — Saurin canon-restoration candidate study evidence

Order `reviews/chatgpt-rac-w2i2-saurin-canon-restoration-order.md`; gate `reviews/claude-rac-w2i2-saurin-canon-restoration-gate.md`. CANDIDATES ARE COPIES; no source anatomy changed.

| File | Driver (`tools/rac/w1/w2i2_drivers/`) | Content |
|---|---|---|
| `ledger.json` | `sa_ledger.py` | vertical stature-budget ledger, Saurin + comparators |
| `bodies_{AS,L1,L2,L3,F1,F2,F3}.json` | `sa_w2i2_build.py CAND core` | core body set per candidate (W2I measure + J-2 limbs + ledger) |
| `bodies_ASfull.json`, `bodies_L1F2.json` | `sa_w2i2_build.py AS|L1+F2 full` | full W2I body list, as-built re-run and combined candidate |
| `compare_*.json` | W2I `sa_compare.py` (unchanged) | lower-trunk floor, matched-height directions, passing, never-Gorrund |
| `eval_*.json` | `sa_w2i2_eval.py` | limb / budget criteria and limb cross-race rows |
| `saeval_{ASfull,L1F2}.json` | W2I `sa_eval.py` (unchanged) | stature / frame / composition / sex / tail / balance checks |
| `tailcap_L1F2.json` | `run_tailcap_cand.py` (W2I1 `sa_tailcap2.py`) | same-state tail caps on the combined candidate |
| `rootcarriage.json` | `sa_rootcarriage.py` | root-carriage family 0-+8 deg (LP choice, silhouette, invariance, lean) |
| `sheets/*.jpg` | `sa_w2i2_render.py`, inline split render | before / after and root-carriage sheets; tail split diagnostic |
| `tables.md` | `../../tools/rac/w1/gen_w2i2_docs.py` | generated tables |

Candidate warps: `sa_cand.py` (L: thigh +G, thorax -0.4G, neck -0.6G; F: elbow delta toward shoulder; root pitch in-memory extension of vary.warp). Superseded construction trials (thorax / neck 25 / 75 split with a u153 neck band; forearm remap without the axillary taper) are described in the gate §2 and not kept.
