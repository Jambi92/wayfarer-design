# RAC W1l — Grask corrective pass evidence

Order: GitHub Issue #1 (author order and confirmation, option b). Gate: `reviews/claude-rac-w1l-grask-acceptance-gate.md`. Nothing here is canon or accepted.

| Path | Contents | Produced by |
|---|---|---|
| `tables.md` | All tables (generated) | `tools/rac/w1/gen_w1k_docs.py` with `EVDIR` = this folder |
| `eval.json` | Rows for the W1l candidate (GRL925_1200), the minimum passing alternative (GRL930_1170), frames GR-BODY-04 / -05 and low composition; accepted Gorrund in the GO slot | `w1k_drivers/gr_eval.py` (`EVDIR`) |
| `probe/probe_summary.json`, `probe/GRL*_rows.json` | Pelvis X × femur cross-section probes with the lumbar narrowing removed | `w1k_drivers/gr_probe2.py` |
| `matched_height.json` | W1l GR vs accepted Gorrund 217.0 / 224.1 cm and Broad Skarn 215.1 / 222.1 cm | `w1k_drivers/gr_matched.py` (`GRMEAS`, `EVDIR`) |
| `composition.json` | Continuity readings, W1l vs W1h vs references; same-composition low check | `w1k_drivers/gr_comp.py` (`W1L=1`) |
| `arm_clearance.json` | GR-G3 readings for the W1l central, Narrow and Broad bodies | `arm_clearance.clear`, `arm_tube_test` |
| `sheets/*.jpg` | W1l central / skeleton / frames; hip before-after with SK and Gorrund; composition; matched height | `w1k_drivers/render_w1l_AS_RUN.sh` |

Construction record: `tools/rac/w1/cfg/w1l/GR.json`. Builds: `w1k_drivers/gr_probe2.py` (central), `gr_build.py` with `CAND=w1l` (frames, composition).
