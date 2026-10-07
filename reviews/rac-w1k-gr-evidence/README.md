# RAC W1k — Grask W1 acceptance gate evidence

Order: `reviews/chatgpt-rac-w1-remaining-bodies-continuation-order.md` §2–§4. Gate: `reviews/claude-rac-w1k-grask-acceptance-gate.md`. Nothing here is canon or accepted.

| Path | Contents | Produced by |
|---|---|---|
| `tables.md` | All tables (generated) | `tools/rac/w1/gen_w1k_docs.py` |
| `eval.json` | Skeletal (CIB), skin and directional rows for the central GR (W1h geometry as built), the documented construction (GRS01, lumbar narrowing removed), frames GR-BODY-04 / -05 and composition bodies GR-BODY-06…09 and GR-LOW; accepted Gorrund (W1i/W1j point) in the GO slot | `w1k_drivers/gr_eval.py` |
| `matched_height.json` | GR 218 cm vs accepted Gorrund at 217.0 / 224.1 cm and Broad Skarn at 215.1 / 222.1 cm | `w1k_drivers/gr_matched.py` |
| `composition.json` | Trunk continuity readings (all GR bodies, MF / SK / SG references and skeletons) and the same-composition low check | `w1k_drivers/gr_comp.py` |
| `probe/pelvis_probe.json`, `probe/*_rows.json` | Documented construction with pelvis X 0.92–1.05: GR-P2b / GR-P5 / GR-P6 | `w1k_drivers/gr_probe.py` |
| `sheets/*.jpg` | Central, skeleton, Narrow, Broad; composition bodies; matched-height lineup; trunk crop | `w1i_drivers/sheet4.py` (`w1k_drivers/render_AS_RUN.sh`) |

Builds: `w1k_drivers/gr_build.py` (stages `s01`, `frames`, `comp`; same AD-G14 route as `w1h_drivers/grfin.sh`). Central geometry is unchanged from W1h (`reviews/rac-w1h-evidence/geometry/GR_r6.npz`, sha256 702c40ea…; re-checked in this pass).
