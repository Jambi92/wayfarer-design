# RAC W1j evidence

Order: `reviews/chatgpt-rac-w1i-author-decisions-w1j-robustness-order.md`. Gate: `reviews/claude-rac-w1j-author-acceptance-gate.md`. Nothing here is canon. The retained candidate is the W1i point; its full W1i evaluation (frames, composition, ALPC-0…8, arm tests, directional and skin rows, ocular, ears) is in `reviews/rac-w1i-evidence/` and applies unchanged (identical geometry).

| Path | Contents | Produced by |
|---|---|---|
| `tables.md` | All tables (generated) | `tools/rac/w1/gen_w1j_docs.py` |
| `sensitivity/sens_W.json`, `sens_D.json`, `sens_C.json` | ±2 % protocol on the W1j stature series for the retained W1i point (W) and the two lower-femur candidates (D, C); `base` = the candidate itself rebuilt and checked on the full series | `w1j_drivers/sens7.py` (`sens_AS_RUN.sh`) |
| `candidates/cand_*.json` | Candidate values and how each was derived | `w1j_drivers/maxmin.py`, `femur_trade2.py`, W1i |
| `femur_trade.json` | Femur-ceiling trade: linear-model points and their built, ordinary-rule checks | `w1j_drivers/femur_trade2.py` |
| `interior_analysis.json` | First-order interior analysis: which values can be ±2 %-robust together, the best reachable tolerance for the rest, binding relations | `w1j_drivers/interior_analysis.py`, `maxmin.py` |
| `interior_bounds.json` | Same programme with the 2 % gap, without it, and with every search bound widened by 0.5 (step limit 0.25): joint tolerance, active limits, binding relations | `w1j_drivers/interior_bounds.py` |
| `geometry_identity.json` | Max vertex difference between the W1j rebuild of the retained point and the W1i meshes (reference, true 208, 215, 222, 251 donors, skeleton) — all 0 | `w1j_drivers/geometry_identity.py` |
| `low_comp_references.json`, `skb_continuity.json` | MF / SK continuity at the same low composition; Broad Skarn continuity | `w1i_drivers/gn6.cont`, `waist_rise`; `w1i_drivers/skb_continuity.py` |
| `solver/gn7_J1.log`, `gn7_J2.log`, `gn7_*_pt*.json`, `gn7_*_J*.npy` | Robust re-solve logs; constraint values and Jacobians at the W1i point (J1 pt0), the first robust step (J1 pt1) and the femur-1.294 point (J2 pt0) | `w1j_drivers/gn7.py` |
| `sheets/*.jpg` | Retained candidate four-view (reference, true 208, 253 cm, Narrow, Broad, low composition, skeleton); Broad Skarn comparison; trunk crop with same-composition references; femur trade hip crop | `w1i_drivers/sheet4.py` (`w1j_drivers/render_AS_RUN.sh`) |
