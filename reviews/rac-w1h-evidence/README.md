# RAC W1h evidence

Order: `reviews/chatgpt-rac-w1g-author-decisions-w1h-continuation-order.md`. Gate: `reviews/claude-rac-w1h-author-acceptance-gate.md`. Nothing here is canon. Before / after comparisons read `reviews/rac-w1g-evidence`.

| Path | Contents | Produced by |
|---|---|---|
| `tables.md` | All tables (generated) | `tools/rac/w1/gen_w1h_docs.py` |
| `cib/<ID>_cib.json` | Composition-infimum bony stations, W1h method (fixed reference levels, plane sections); every body incl. stress / frame bodies | `bony_envelope.py`, `w1g_drivers/cib_all.py`, `w1g_drivers/gn3.py`, `w1h_drivers/stress5.py` |
| `skeletal/<ID>_skp.json`, `skeletal/t*/` | Skeletal readings per soft-tissue allowance t (reference bodies) | `skeletal_proxy.py` |
| `skeletal/skeletal_checks.json` | Accepted pelvic / girdle / ALPC relations on the skeleton, all races | `skeletal_checks.py` |
| `skeletal/alpc_w1h.json` | ALPC-5 frames, stature series (208 / 215 / 222 / 251 cm), ALPC-7 at 10 Gorrund / Broad Skarn height pairs, ALPC-6 skeletal + skin halves | `w1g_drivers/alpc_w1g.py` |
| `skeletal/alpc8.*` | ALPC-8 matched-display silhouette test vs Durrim | `silhouette_test.py` |
| `skeletal/skeleton_flank_flare.json` | Flank flare of the minimum-composition (skeleton) bodies, GO W1g / W1h vs references | `w1h_drivers/skel_flare.py` |
| `skeletal/contour_clearance.json` | Chest-lead, buttock-lead, flank flare; arm trunk-section test and arm-tube test | `profile_bump.py`, `arm_clearance.py` (`w1h_drivers/post2.sh`) |
| `skeletal/frame_shaft_diagnostic_W1g.log` | W1g frame shaft / lower-thorax rows with and without the frame pelvis write | `w1h_drivers/framediag.py` |
| `skeletal/gor03_generator_diagnostic_W1g.json` | W1g generator-corner diagnosis for GOR-BODY-03 (copied for the AD-W1H-3 trace) | W1g |
| `candidates/`, `geometry/`, `skeleton/` | GO and GR W1h: measurements, pose invariance, evidence sheets, R-6 geometry, minimum-composition skeleton bodies | `build_variant.py`, `run_candidate.py`, `w1g_drivers/gn3.py` |
| `go-variants/` | GOR-BODY-02 / -03 / -04 / -05 / -12 / -14 / -16, GO 215 / 222 cm, Broad Skarn 215 / 222 cm; `stress_builds.json`; `skp/` readings | `w1h_drivers/stress5.py` |
| `solver/` | gn5 logs H1–H8, `p0.*` (W1g parameters read with the W1h method), `probeTB*` and `probe_ordinary.*` (thoracic-breadth probes T0–T4, T6, T7, T9, T10; reference body only), `GO_params.json` (final), `sensitivity.json` (R-14) | `w1h_drivers/gn5.py`, `sensitivity.py`, `sens_tb.py` |
| `ae_vertical_budget.json` | Aelari vertical budget at the 1 % convention | `w1h_drivers/ae_budget.py` (verifies the rows and adds the maximum uniform margin) |
| `ocular/`, `ears/` | O-1 rings and globes on the W1h set; v2 ear direction checks | `ocular_w1f.py`, `ear_attach_sheet.py`, `ear_checks.py` |
| `directional_checks.json`, `w1e_checks.json` | Cross-race directional checks; skin diagnostics | `directional_checks.py`, `w1e_checks.py` |
| `sheets/*.jpg` | GO render review (front / side / 3/4 back), stature series, frame bodies, GR before-after, skeletal proxy, side lineup, ALPC-8, ears | `compare_sheet.py`, `skeleton_sheet.py`, `side_lineup.py` |

Reproduction: `w1h_drivers/rebuild.py` rebuilds the scratch layout from committed build JSONs; `w1h_drivers/final.sh <params.json>` builds and evaluates the final set.
