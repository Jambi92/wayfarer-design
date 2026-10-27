# RAC RP3 — Marchfolk v005 active MPFB family base — freeze report

**Date:** 2026-10-27
**Order:** `reviews/chatgpt-rac-rp3-mpfb-family-base-v005-final-freeze-order.md` (78a109f)
**Freeze record:** `MPFB_FAMILY_BASE_v005_FREEZE.json`
- `E:/…/production/Marchfolk/RP3/` and `…/Skarn/RP3/`;
- copy in `reviews/rac-rp3-evidence/mpfb_family_base_v005_freeze/`.

**Evidence:** `reviews/rac-rp3-evidence/mpfb_family_base_v005_freeze/`

## Result

**MARCHFOLK RP3 v005 — AUTHOR ACCEPTED / FROZEN — ACTIVE MPFB FAMILY BASE.** Frozen by record: neither file was re-saved.

| Question | Answer |
|---|---|
| Marchfolk v005 frozen successfully? | **Yes.** Both PC files read back exactly. |
| Skarn frozen successfully? | **Yes** (`reviews/claude-rac-rp3-skarn-family-freeze-report.md`). |
| Active family topology / hash? | 57,842 V / 57,840 Q, 100 % quads. Face topology hash `ec768ae210ea3ee1c053d0c4cd3256d57dad6db35d515502706b74f64281bee0`. hm08 → v005 map `e690fbafb53adc27…`. Full hashes are in the freeze record. |
| D1 / D3 / D4 / D5 authoritative? | **Yes.** `validator_v2.py --scale-ref 173.143 --d5`; 69 / 69 recomputed at freeze. |
| Accepted toe-extension exception recorded? | **Yes.** MPFB-CF-1 (MF-F, 3 faces) and MPFB-CF-2 (SK-F, 2 faces) are in the freeze record and in `specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md`. |
| Standard promoted? | **Yes.** `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md` is now AUTHOR-ACCEPTED TECHNICAL STANDARD v1 (15 sections + checklist). |
| Next recommended race? | **Sagekin** (§4). |
| Any freeze / read-back mismatch? | **None.** |
| Any new blocker? | **None** for the freeze. One prerequisite for Sagekin (§4). |

## 1. Frozen files

Read back on the PC copies with `freeze_v5_verify.py`, which uses `freeze_check.py` in Blender without saving.

| File | SHA-256 | Geometry hash | V / Q |
|---|---|---|---|
| `MF_M_REF_RP3_retopo_v005.blend` | `e560386cf0412…` (= manifest) | `= manifest` | 57,842 / 57,840 |
| `MF_F_REF_RP3_retopo_v005.blend` | `f2f2f9dc4bb1d…` (= manifest) | `= manifest` | 57,842 / 57,840 |

Both files:

| Check | Result |
|---|---|
| Quads | 100 % |
| Components | 1 |
| Boundary edges | 0 |
| Non-manifold edges / vertices | 0 / 0 |
| Degenerate faces | 0 |
| Normals | outward |
| Face list | equals the candidate |
| Geometry | equals the candidate to ≤ 6e-8 m |

**Map compatibility.**
- The PC hm08 map equals the manifest map.
- The map arrays equal the candidate.
- Candidate V = M5 @ race hm08 exactly (0.0).

## 2. Gates re-confirmed at freeze

| Gate | MF-M | MF-F |
|---|---|---|
| D1 + D3 + D4 + D5 firm | 69 / 69 | 69 / 69 |
| T-1 / T-2 / T-3 / T-7 | pass | pass |
| Density, 9 zones | pass | pass |
| Face: mouth / orbit rings, corner poles | 35 / 43 / 43, 0 | 35 / 43 / 43, 0 |

**Sources unchanged:**

| Item | SHA-256 prefix |
|---|---|
| MF-M-R R-6 / build | `2caaf056` / `c5be9ca0` |
| MF-F-R R-6 / build | `c254fb4b` / `252907fd` |

**Provenance unchanged** (`freeze_hashes.txt`):
- v003 blends `5b793eda` / `a5d8adfe` and freeze record `4af62f81`;
- v004 files `398dbd26` / `2729750d`;
- all v005 evidence.

## 3. Recorded status

| Version | Status |
|---|---|
| v003 | historical accepted MPFB Family Base v1 (frozen, unchanged) |
| v004 | margin-hardening provenance |
| **v005** | **active MPFB Family Base v2 / final margin-hardened base** |

The freeze record is authoritative over the sidecar and embedded `RAC_status` strings. Those still say "CANDIDATE – NOT FROZEN" because the files were deliberately not re-saved.

## 4. Next-race recommendation

**Sagekin first**, keeping the master-plan order. It is the lowest-risk next propagation.

Why Sagekin fits:
- Human-family anatomy, so no ear or skeleton branch is expected: Sagekin use the Marchfolk human auricle (AC-4), human hands and feet, and a subtly longer-limbed, linear human silhouette (`specs/sagekin/SAGEKIN_V1.md`).
- MPFB route on the shared hm08 topology (RP0).
- The W2E boundary foundation is accepted.

Why Fenn and the other elves should come later:
- Fenn is the first race with a genuinely non-human skeleton and real pointed-ear anatomy.
- Ear branches are explicitly outside the technical standard, so Fenn is likely to need an author-ordered race-specific branch.
- Aelari and Vael inherit the same elf risks.

**Prerequisite before the Sagekin order** (from RP0 and the RM-OT-05 register):
- Sagekin **configuration 2 has no accepted central reference**.
- Only diagnostic builds (`SGF152-NAT`, `SGF178`, `SGF208`) exist.
- The author needs to name the configuration-2 reference (for example SGF178), or authorise configuration 1 only (accepted `SG`).

**STOP FOR CHATGPT REVIEW.** No race propagation, rig, morph, UV, LOD or UE5 work was started.
