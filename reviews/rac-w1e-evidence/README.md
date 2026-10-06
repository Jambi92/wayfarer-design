# RAC W1e evidence

Order: `reviews/chatgpt-rac-w1d-author-decisions-continuation-order.md`. Diagnostics only; nothing here is canon.

| Path | Contents | Produced by |
|---|---|---|
| `candidates/` | Rebuilt W1e candidates FN, AE, VA, GR, GO, DU-NAT, PK-NAT: build record, measurements, invariance, evidence sheet | `build_arm.py` / `native_short.py` + `run_candidate.py`, configs in `tools/rac/w1/cfg/w1e/` |
| `geometry/` | R-6 geometry of the rebuilt candidates (npz) | as above |
| `remeasured/` | Unchanged accepted / earlier bodies (MF-M-R, MF-F-R, MF-FACE-PROJ-MAX, SK, SG, HV, CG-NAT) re-measured with the W1e readings added (geometry hashes identical to the W1c / W1d files; all earlier values identical) | `run_candidate.py` |
| `directional_checks.json` | 134 cross-race directional checks incl. HV source span | `directional_checks.py` (DU/PK/CG read from DU-NAT/PK-NAT/CG-NAT; the 1 % NOT DEMONSTRATED rule is applied in `tables.md`) |
| `w1e_checks.json` | 75 rows of the accepted pelvic / girdle / ALPC relations (skin readings: diagnostic, PV-D16) | `w1e_checks.py` |
| `orbit/` | MF/FN landmark orbital-margin rings (O-1), FN increment proposal δ = 0.02 | `orbit_ring.py` |
| `globe_fit_pkcg.json` | S-D3 adult-globe fit test (MF, PK-NAT, CG-NAT, plus DU-NAT, GR, GO) | `globe_fit.py` |
| `ears/` | Ear-family v2 sculpt-detail geometry (OBJ, ear-local frame), landmark readings, sheets; attached-ear head sheet and readings; direction checks | `ear_families_v2.py`, `ear_attach_sheet.py`, `ear_checks.py` |
| `side_lineup.jpg` | Left-side lineup (visual check, PV-D17) | `side_lineup.py` |
| `go_skin_trial_*` | Rejected GO skin-only trial: config, GO check rows, side/front comparison with the candidate | `build_arm.py`, `run_candidate.py`, `w1e_checks.py` |
| `tables.md` | All tables (generated) | `gen_w1e_docs.py` |
