# RAC W1p — Fenn W1 acceptance gate evidence

Order: `reviews/chatgpt-vael-final-acceptance-fenn-w1-order.md` (= GitHub Issue #1 comment 2026-10-07T16:06Z). Gate: `reviews/claude-rac-w1p-fenn-acceptance-gate.md`. Nothing here is canon or accepted.

| Path | Contents | Produced by |
|---|---|---|
| `tables.md` | All tables (generated) | `tools/rac/w1/gen_w1p_docs.py` |
| `central_<tag>.json` | Directional (incl. every accepted-AE / accepted-VA row against Fenn), skin and added canon-derived rows; tags W1g, FNL1–FNL4, frames, composition | `w1p_drivers/fn_eval.py` |
| `skeletal_<tag>.json` | CIB skeletal rows on the W1i base with accepted AE, VA and GR; W1g (control reproduces W1i to 3e-13), FNL4, NARROWB, BROADB, BROADB_P112 | `w1p_drivers/fn_skel.py`, grids `fn_grid.py` |
| `composition.json`, `separation.json` | Continuity readings, same-composition low check; % difference of FNL4 from each population (elf-family chain) | `w1p_drivers/fn_comp.py` |
| `sheets/*.jpg` | Elf-family lineup; joints before / after; FNL4 frames and minimum composition; composition variants | `w1p_drivers/render_AS_RUN.sh` |

Construction record: `tools/rac/w1/cfg/w1p/FN.json`. FN as-built geometry = W1g (sha256 1495f5a0…; build record matches `cfg/w1g/FN.json`).
