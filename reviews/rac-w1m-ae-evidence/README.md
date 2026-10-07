# RAC W1m — Aelari W1 acceptance gate evidence

Order: GitHub Issue #1, final author ruling comment (Aelari next; recorded in `reviews/chatgpt-rac-w1l-grask-order-issue1-record.md`). Gate: `reviews/claude-rac-w1m-aelari-acceptance-gate.md`. Nothing here is canon or accepted.

| Path | Contents | Produced by |
|---|---|---|
| `tables.md` | All tables (generated) | `tools/rac/w1/gen_w1m_docs.py` |
| `central_<tag>.json` | Directional and skin rows (accepted Gorrund and Grask in their slots), leg-evenness row, elongation distribution; tags W1g (as built), AEL1, NARROW, BROAD, LOWMUS, HIMUS, HIFAT, HIBOTH, LOW | `w1m_drivers/ae_eval.py` |
| `skeletal_<tag>.json` | CIB skeletal rows on the W1i skeletal base with the accepted Grask; W1g (control: reproduces W1i exactly), AEL1, NARROW, BROAD | `w1m_drivers/ae_skel.py` (CIB via `w1g_drivers/cib_all.py`; grids `w1m_drivers/ae_grid.sh`, `ae_variants.py`) |
| `composition.json` | Trunk continuity readings and the same-composition low check | `w1m_drivers/ae_comp.py` |
| `separation.json` | % difference of AE (AEL1) from MF, SG, FN, VA, SK and accepted Grask | `w1m_drivers/ae_sep.py` |
| `sheets/*.jpg` | Separation lineup; legs before / after; AEL1 frames and minimum composition; composition variants | `w1m_drivers/render_AS_RUN.sh` |

Construction record: `tools/rac/w1/cfg/w1m/AE.json`. AE as-built geometry = W1g (`reviews/rac-w1g-evidence/geometry/AE_r6.npz`, sha256 880b4f0b…; build record matches the documented scales). FN and VA geometry verified identical to their W1g evidence files (VA file metadata differs; vertices max |ΔV| = 0).
