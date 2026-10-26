# RAC RP2 — Grask formal closure record

**Date:** 2026-10-26
**Order:** `reviews/chatgpt-rac-rp2-closure-and-rp3-marchfolk-baseline-order.md` (d18ff2a), Part A
**Last RP2 return:** 02468aa

## 1. Disposition

**Grask RP2 — RETOPOLOGY / PRODUCTION-MESH PILOT: AUTHOR ACCEPTED / FROZEN / VALIDATED FOR PROGRAM CONTINUATION.**

| Item | Value |
|---|---|
| Accepted production mesh | `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Grask/RP2/GR_U_REF_RP2_retopo_v003.blend` |
| SHA-256 | `03bfe7d924ff5b8b61a4c10095af5d16ca29d41667d7f61d0abeca14e1f07ce0` |
| Geometry hash | `f9c4a7ac98e86d98017376b9d67c85428503d2d6385258471d99bc766bfe702f` |
| Sidecars | `GR_U_REF_RP2_retopo_v003.json`, `_landmarks.json`, `_FREEZE.json`. Unchanged and re-hashed in every RP2 diagnostic cycle; last verified identical at 02468aa. |
| Topology failure demonstrated by the deformation studies | **None** |

The asset is not modified by this record or by anything in RP3.

## 2. Carry-forward items for later production rigging

### Elbow

- **60–120°:** H2 is the preferred diagnostic direction (helper + reduced pose-space corrective). Record: `reviews/rac-rp2-evidence/grask_rig_diagnostic_v005/`.
- **130° deep flexion:** open production-rig / contact-corrective item.
  - VC3 is the best numeric 130° reference: physical volume −170 / −182 cm³ vs the straight elbow; ring girth ≤ base + 0.30 cm; crease 2.9 / 0.3 mm; 0 non-contact.
  - VC3 was rejected visually for contact-interface rumpling. Record: `grask_rig_diagnostic_v006/`; cleanup attempts F1 / F2 in `grask_rig_diagnostic_v007/`.
- **Authoritative engineering volume measures:**
  - overlap-aware physical volume relative to the straight elbow (generalised winding number, `elbow_overlap_volume.py`);
  - local ring girth / mean ring radius by station (`elbow_girth.py`).
  - The old closed-mesh divergence volume vs interpenetrating W0 is secondary only.
- RP2 elbow experimentation is **closed**.

### Shoulder

- **SW3** is the accepted Grask shoulder production direction (`grask_rig_diagnostic_v007/trackS2/`):
  - girdle-only bounded weight diffusion (clavicle / scapula / upper-arm columns, 22 cm region around GH);
  - a 0.5 LBS / DQS preserve-volume blend over the shoulder;
  - the S1 abduction girdle / scapular rule as secondary mechanics.
- **Left flex90 anterior axillary-fold residual:** named production-rig corrective item. Best diagnostic reference is **LF2** (`grask_rig_diagnostic_v008/`):

| LF2 metric | Value |
|---|---|
| Non-contact pairs | 0 |
| Crease depth | 1.3 mm |
| Orientation | 111 |
| Local inversions | 2 |
| Folds outside | 4 |
| Loop | 0.525 |
| p95 / max strain | 49.7 / 103 % |
| Zone proxy | −31.7 % |

- RP2 shoulder experimentation is **closed**.

### Other retained decisions

- v002 knees remain the diagnostic baseline.
- Nail Plate Rigidity v2 remains the nail diagnostic criterion (Nail Cap Historical v1 report-only).
- GH remains at the accepted diagnostic location (v002 landmarks).
- No carry-forward item implies reopening source anatomy or retopology.

## 3. Program transition

- Gorrund RP1: owner-frozen, closed.
- Grask RP2: closed (this record).
- **RP3 Marchfolk begins:** the MPFB-family production-base pilot.
- Final Grask production rigging is deferred to the program's later handoff stage.
