# RAC W1f evidence

Order: `reviews/chatgpt-rac-w1e-author-decisions-w1f-continuation-order.md`. Gate: `reviews/claude-rac-w1f-author-acceptance-gate.md`. Nothing here is canon.

| Path | Contents | Produced by |
|---|---|---|
| `tables.md` | All tables (generated) | `gen_w1f_docs.py` |
| `candidates/`, `geometry/` | Rebuilt GO (AD-G14), GR (AD-G14), VA: measurements, invariance, evidence sheets, R-6 geometry | `skeleton_envelope.py`, `build_variant.py`, `run_candidate.py`; drivers in `tools/rac/w1/w1f_drivers/` |
| `skeleton/` | Skeletal-envelope bodies (minimum composition, same skeleton) for every body, R-6 | `build_variant.py` (+ trunk sculpt for GO) |
| `skeletal/*_skp.json`, `skeletal/t*/` | Skeletal-proxy readings per body and per soft-tissue allowance t | `skeletal_proxy.py` |
| `skeletal/skeletal_checks.json` | Accepted pelvic / girdle / ALPC relations on the skeleton, t sweep | `skeletal_checks.py` |
| `skeletal/alpc_invariance.json` | ALPC-5 (GOR-BODY-04/-12/-14), ALPC-6 (skeleton + GOR-BODY-16 skin vs composition-matched MF), ALPC-7 at 229 and 208 cm vs equal-height Broad Skarn | `alpc_invariance.py` |
| `skeletal/alpc8.*` | ALPC-8 / GO L775 matched-display silhouette test vs Durrim | `silhouette_test.py` |
| `skeletal/contour_clearance.json` | Chest-lead / buttock-lead contour diagnostics; GR-G3 arm clearance | `profile_bump.py`, `arm_clearance.py` |
| `go-variants/` | GOR-BODY-02/04/12/14/16, Broad Skarn 208/229, low-composition MF/SK readings, human-tissue sensitivity | `w1f_drivers/frames.py`, `build_variant.py`, `skeleton_envelope.py` |
| `directional_checks.json`, `w1e_checks.json` | Cross-race directional checks (O-1 ring replaces the FN E-proxy; E-proxy kept as historical) and skin diagnostics | `directional_checks.py`, `w1e_checks.py` |
| `ocular/` | O-1 rings (FN δ = 0.03), species-scaled PK/CG ocular geometry, DU/GR/GO globe fit and presentation | `ocular_w1f.py`, `ocular_sheet.py` |
| `ears/` | v2 ear families re-attached to the W1f bodies; direction checks | `ear_attach_sheet.py`, `ear_checks.py` |
| `*.jpg` | Skeletal-proxy sheet, GO / GR before-after, GO frame bodies, lineup | `skeleton_sheet.py`, `compare_sheet.py`, `side_lineup.py` |
