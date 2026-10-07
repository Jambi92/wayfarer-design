# RAC W1i evidence

Order: `reviews/chatgpt-rac-w1i-gorrund-structural-continuity-resolve-order.md`. Gate: `reviews/claude-rac-w1i-author-acceptance-gate.md`. Nothing here is canon. Before / after comparisons read `reviews/rac-w1h-evidence`. Only Gorrund changed; every other body is the W1h body.

| Path | Contents | Produced by |
|---|---|---|
| `tables.md` | All tables (generated) | `tools/rac/w1/gen_w1i_docs.py` |
| `cib/<ID>_cib.json` | Composition-infimum bony stations (W1h method), every body incl. stress / frame bodies | `bony_envelope.py`, `w1g_drivers/gn3.py`, `w1i_drivers/stress6.py` |
| `skeletal/<ID>_skp.json`, `skeletal/t*/` | Skeletal readings per soft-tissue allowance t | `skeletal_proxy.py` |
| `skeletal/skeletal_checks.json` | Accepted pelvic / girdle / ALPC relations on the skeleton, all races | `skeletal_checks.py` |
| `skeletal/alpc_w1i.json` | ALPC-5 frames, stature series 208 / 215 / 222 / 251 cm, ALPC-7 at 10 height pairs, ALPC-6 skeletal + skin halves | `w1g_drivers/alpc_w1g.py` (`w1i_drivers/evalall.sh`) |
| `skeletal/alpc6_attrib_W1h.json`, `alpc6_attrib_W1i.json`, `waist_slab_vs_section.log` | ALPC-6 skin half read with the official vertex slabs and re-read on plane sections (method attribution) | `w1i_drivers/alpc6_attrib.py`, `restation.py`, `waist_slab_vs_section.py` |
| `skeletal/true208.json`, `skeletal/skb_continuity.json` | True 208 cm body readings; Broad Skarn continuity readings | `w1i_drivers/true208.py`, `skb_continuity.py` |
| `skeletal/alpc8.*` | ALPC-8 matched-display silhouette test vs Durrim | `silhouette_test.py` |
| `skeletal/contour_clearance.json` | Chest-lead, buttock-lead, flank flare, arm trunk-section and arm-tube tests, continuity readings + reference limits, low-composition waist | `w1i_drivers/post3.sh`, `trunk_profile.py`, `gn6.cont`, `gn6.waist_rise` |
| `candidates/`, `geometry/`, `skeleton/` | GO W1i: measurements, pose invariance, evidence sheet, R-6 geometry, minimum-composition skeleton body | `run_candidate.py`, `w1g_drivers/gn3.py` |
| `go-variants/` | GOR-BODY-02 / -03 / -04 / -05 / -12 / -14 / -16, GO 215 / 222 cm, Broad Skarn 215 / 222 cm; `stress_builds.json`; `skp/` | `w1i_drivers/stress6.py` |
| `solver/` | gn6 logs I1–I9, `GO_W1i_x.json` (final point), `GO_params.json` (final build), `ref_continuity.json` (reference continuity readings), `sensitivity_w1i.json` | `w1i_drivers/gn6.py`, `sens6.py` |
| `ocular/`, `ears/` | O-1 rings / globes and v2 ear checks on the W1i set | `ocular_w1f.py`, `ear_attach_sheet.py`, `ear_checks.py` |
| `directional_checks.json`, `w1e_checks.json` | Cross-race directional checks; skin diagnostics | `directional_checks.py`, `w1e_checks.py` |
| `sheets/*.jpg` | Four-view sheets (side / front / front 3/4 / back 3/4): stature series, frames + composition + skeleton, references; trunk crop without arms; axilla close-up with horizontal sections; skeletal proxy; side lineup; ALPC-8; ears | `w1i_drivers/sheet4.py`, `skeleton_sheet.py`, `side_lineup.py` |

Reproduction: `w1h_drivers/rebuild.py` rebuilds the scratch layout; `w1i_drivers/final6.sh solver/GO_W1i_x.json`, then `w1i_drivers/evalall.sh` and `w1i_drivers/post3.sh`.
