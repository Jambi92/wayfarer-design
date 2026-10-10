# RAC W3A1 — Halvren tail closure evidence (NON-CANON diagnostics)

Order `reviews/chatgpt-rac-w3a1-halvren-tail-closure-order.md`; report `reviews/claude-rac-w3a1-halvren-tail-final-closure-report.md`; cfg `tools/rac/w1/cfg/w3a/HV-tails.json` (`w3a1`); drivers `tools/rac/w1/w3a1_drivers/` (`AS_RUN.sh`).

| File | Content |
|---|---|
| `w3a1.json` | values + checks (`w2g_drivers/w2g_eval.py`): A coupled family, O onset, Z coupling sweep, F / M endpoint stress, Q collisions, K Skarn guard (report), C continuity, G W1 rows (report) |
| `spec.json`, `registry.json` | comparison specification (`w3a1_spec.py`); body registry (`w3a1_reg.py`: W3A registry + W3A1 bodies + new grids) |
| `construction.json` | every W3A1 build: route, macro, targets (incl. the coupled femur system), bone scales, composition |
| `joint_sections.json` | exact-plane joint sections of the W3A1 bodies |
| `rs.json` | AD-W3A-4 complete-body validity: 68 W3A lower-tail samples (22 on the full 24 readings), 12 central native-range confirmation bodies, 16 coupled upper samples vs their W3A twins |
| `sheets/*.jpg` | neutralized renders: coupled Skarn endpoint, coupled Aelari / combined endpoints with frames, central-range validity corner |

Coupling rates, strengths, coordinates and measurements are diagnostic construction parameters, never species constants.
