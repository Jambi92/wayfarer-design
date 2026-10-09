# RAC W2I3 — Saurin reference-quality rebuild / caudal-base closure evidence

Order `reviews/chatgpt-rac-w2i3-saurin-reference-rebuild-order.md`; gate `reviews/claude-rac-w2i3-saurin-reference-rebuild-gate.md`. CANDIDATE COPIES; no source anatomy changed.

| File | Driver (`tools/rac/w1/w2i3_drivers/`) | Content |
|---|---|---|
| `bodies_R.json` | `sa_w2i3_build.py R full` | full W2I body list rebuilt (clean L1 + F2), W2I measure + J-2 limbs + ledger |
| `compare_R.json`, `saeval_R.json` | W2I `sa_compare.py`, `sa_eval.py` (unchanged) | cross-race and internal suites |
| `eval_R.json` | W2I2 `sa_w2i2_eval.py` (unchanged) | limb / budget rows vs the frozen re-run (`rac-w2i2-sa-evidence/bodies_AS.json`) |
| `strain.json` | `sa_strain.py` | edge-length strain and flipped faces, W2I2 diagnostic vs W2I3 rebuild |
| `caudal.json` | `sa_caudal.py` | caudal-base contour family C0-C3 on six bodies |
| `canon_preview.json` | `sa_canon_preview.py` | candidate hashes (preview only) |
| `sheets/*.jpg` | `sa_w2i3_render.py`; inline split render | rebuilt 188 / family sheets, caudal family sheets, zone-removal diagnostic |
| `tables.md` | `../../tools/rac/w1/gen_w2i3_docs.py` | generated tables |

Rebuild fields: `sa_rebuild.py` (thigh / thorax / neck vertical fields with shoulder-cap follow; forearm redistribution; caudal contour). The frozen and W2I2 comparison sets live in `reviews/rac-w2i2-sa-evidence/`.
