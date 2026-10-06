# RAC W1g evidence

Order: `reviews/chatgpt-rac-w1f-author-decisions-w1g-continuation-order.md`. Gate: `reviews/claude-rac-w1g-author-acceptance-gate.md`. Nothing here is canon.

| Path | Contents | Produced by |
|---|---|---|
| `tables.md` | All tables (generated) | `tools/rac/w1/gen_w1g_docs.py` |
| `cib/<ID>_cib.json` (incl. `GO-W1f`, `GR-W1f` for the method attribution) | Composition-infimum bony stations: per-grid-body stations, minimum, argmin, tissue per side | `bony_envelope.py`, `w1g_drivers/cib_all.py`, `w1g_drivers/gn3.py`, `w1g_drivers/stress.py` |
| `skeletal/<ID>_skp.json`, `skeletal/t*/` | Skeletal readings with CIB stations (W1f-method stations kept as `w1f_stations`) per soft-tissue allowance t | `skeletal_proxy.py` (5th argument = CIB file) |
| `skeletal/skeletal_checks.json` | Accepted pelvic / girdle / ALPC relations on the skeleton, all races | `skeletal_checks.py` |
| `skeletal/method_attribution_checks.json` | Same checks with the unchanged W1f GO and GR bodies read through CIB | `skeletal_checks.py` |
| `skeletal/alpc_w1g.json` | ALPC-5 frames, stature stress (208 / 251 cm), ALPC-7 at 10 Gorrund / Broad Skarn height pairs, ALPC-6 skeletal + skin halves | `w1g_drivers/alpc_w1g.py` |
| `skeletal/alpc8.*` | ALPC-8 matched-display silhouette test vs Durrim | `silhouette_test.py` |
| `skeletal/contour_clearance.json` | Chest-lead / buttock-lead; arm-to-trunk section clearance (W1g interpenetration test, decidable only where the trunk section is closed) | `profile_bump.py`, `arm_clearance.py` |
| `skeletal/gor03_generator_diagnostic.json` | Generator GO-input bodies at the 229 / 251 cm height macros (GOR-BODY-03 diagnosis) | inline, `bony_envelope.fast_stations` |
| `candidates/`, `geometry/`, `skeleton/` | Corrected AE, VA, FN, GR, GO: measurements, pose invariance, evidence sheets, R-6 geometry, skeletal (minimum-composition) bodies | `build_variant.py`, `run_candidate.py`, `w1g_drivers/gn3.py` |
| `go-variants/` | GOR-BODY-02 / -03 / -04 / -12 / -14 / -16, GO 215 / 222 cm, Broad Skarn 215 / 222 cm | `w1g_drivers/stress.py` |
| `solver/` | GO re-solve logs (gn4 S1–S4), probes (probe2–5: hand-set ALPC-1 start, arm-clearance upper-thorax values), least-extreme pass (`shrink.log`), final parameters | `w1g_drivers/gn4.py`, `shrink.py` |
| `ocular/` | O-1 rings and globes; G-S1 minimal-globe search (PK, CG; SK / SG method check) | `ocular_w1f.py`, `ocular_gs1.py`, `ocular_sheet.py` |
| `joints/bony_joints.json` | Skarn vs MF bony joint robusticity | `bony_joints.py` |
| `ears/` | v2 ear families on the W1g bodies; direction checks | `ear_attach_sheet.py`, `ear_checks.py` |
| `directional_checks.json`, `w1e_checks.json` | Cross-race directional checks; skin diagnostics | `directional_checks.py`, `w1e_checks.py` |
| `*.jpg` | GO / GR / AE-VA-FN before-after, GO stress bodies, skeletal proxy sheet, side lineup | `compare_sheet.py`, `skeleton_sheet.py`, `side_lineup.py` |

Notes: `skeletal_proxy_sheet.jpg` draws the crest hoop from the minimum-composition surface (the CIB values are numbers in the tables). In `go_stress_bodies.jpg` the render window is fixed at 245 cm, so the head of the 251 cm body is cropped.
