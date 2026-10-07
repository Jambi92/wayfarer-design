# RAC W1q — Pipkin W1 acceptance gate evidence

Order: `reviews/chatgpt-fenn-final-acceptance-pipkin-w1-order.md` (= GitHub Issue #1 comment 2026-10-07T17:19Z). Gate: `reviews/claude-rac-w1q-pipkin-acceptance-gate.md`. Nothing here is canon or accepted.

| Path | Contents | Produced by |
|---|---|---|
| `tables.md` | All tables (generated) | `tools/rac/w1/gen_w1q_docs.py` |
| `central_<tag>.json` | Directional, skin and added canon-derived rows (accepted comparators in their slots; DU / CG unaccepted), stance readings, child-proxy comparison; tags W1g (central), frames, Broad-vs-Narrow-DU, composition | `w1q_drivers/pk_eval.py` |
| `skeletal_<tag>.json` | CIB skeletal rows on the W1i base with accepted AE, VA, FN, GR: central, Narrow, Broad, Broad vs Narrow DU | `w1q_drivers/pk_skel.py`, grids `pk_grid.py`, `du_grid.py` |
| `composition.json`, `separation.json` | Continuity readings, same-composition low check; % difference of PK from MF, SG, FN, DU, Narrow DU, CG, child proxy | `w1q_drivers/pk_comp.py` |
| `sheets/*.jpg` | Short-race lineup (PK, child proxy, CG, DU); frames and minimum composition; Broad PK vs Narrow DU; composition | `w1q_drivers/render_AS_RUN.sh` |

Diagnostic bodies (not canon): human-child proxy `CHILD6` (MF-M-R generator, age macro ≈ 6 y, stature re-solved to 107 cm); Narrow Durrim (DU-NAT + breadth-only Narrow write). PK-NAT geometry identical to `reviews/rac-w1e-evidence/geometry/PK-NAT_r6.npz` (max |ΔV| = 0). Record: `tools/rac/w1/cfg/w1q/PK-NAT.json`.
