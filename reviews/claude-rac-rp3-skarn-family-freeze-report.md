# RAC RP3 — Skarn family freeze report

**Date:** 2026-10-27
**Order:** `reviews/chatgpt-rac-rp3-mpfb-family-base-v005-final-freeze-order.md` (78a109f) §6
**Freeze record:** `MPFB_FAMILY_BASE_v005_FREEZE.json` (the same record covers Marchfolk and Skarn)
**Evidence:** `reviews/rac-rp3-evidence/mpfb_family_base_v005_freeze/`

## Result

**SKARN RP3 — AUTHOR ACCEPTED / FROZEN — MPFB FAMILY PROPAGATION PASS.**
- Frozen by record on the active v005 family topology.
- Not re-saved; no anatomy or topology change.

## 1. Frozen files (PC read-back)

| File | SHA-256 | Geometry hash | Face hash | V / Q |
|---|---|---|---|---|
| `SK_M_REF_RP3_retopo_v003.blend` (SK208-C1R) | `76229b35c913f…` (= manifest) | = manifest | `ec768ae2…` (= family) | 57,842 / 57,840 |
| `SK_F_REF_RP3_retopo_v003.blend` (SKF208) | `4ff0ce6fcb0f2…` (= manifest) | = manifest | `ec768ae2…` (= family) | 57,842 / 57,840 |

Both files:
- 100 % quads, 1 component;
- 0 boundary edges, 0 non-manifold edges or vertices, 0 degenerate faces;
- outward normals;
- geometry equals the candidate to ≤ 1.2e-7 m;
- the hm08 map equals the family map;
- V = M5 @ race hm08 exactly.

## 2. Gates

| Gate | SK-C1R | SK-F |
|---|---|---|
| D1 + D3 + D4 + D5 firm | 69 / 69 | 69 / 69 |
| T-1 / T-2 / T-3 / T-7 | pass (feet T-2 1.195 mm) | pass (0.865 mm) |
| Density, 9 zones | pass | pass |
| Face readiness: mouth / orbit rings, corner poles | 29 / 43 / 43, 0 | 35 / 43 / 43, 0 |
| C1R identity | **preserved**. Face → C1R median 0.000 / p95 0.089 / max 1.016 mm; → pre-C1R median 1.10 mm. | n/a |
| Deformation | no topology-class failure | only the accepted MPFB-CF-2 (toe ext 30°, 2 faces) |

**Sources unchanged:**

| Item | SHA-256 prefix |
|---|---|
| SK208-C1R R-6 / build | `fd8a43d2` / `c1c54d28` |
| SKF208 R-6 / build | `0245683e` / `ddf77a84` |

The Skarn v001 / v002 candidates are kept as provenance (v002 `05616b80` / `e595a6c6`, unchanged).

## 3. Carry-forward

**MPFB-CF-2:** SK-F toe extension 30°, 2 topology-attributable faces in the toe-2 MTP crease. Class: rig / toe weighting. Recorded in `specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md`. Not topology-blocking.

**STOP FOR CHATGPT REVIEW.**
