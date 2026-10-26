# RAC RP2 — Grask final left-flex90 anterior-fold cleanup — gate return

**Date:** 2026-10-26
**Order:** `reviews/chatgpt-rac-rp2-grask-final-left-flex90-cleanup-order.md` (bd11ab0)
**Parent return:** da4e892

## RETURN SUMMARY (§13)

| Item | Result |
|---|---|
| Selected candidate | **None.** Neither LF1 nor LF2 meets every §8 target. |
| Shoulder experimentation | **Closed for RP2** (§12). SW3 remains the accepted shoulder production direction. Left flex90 is carried forward as a named production-rig corrective item. |
| Topology failure demonstrated? | **No.** |
| Parent integrity | **Identical** (before = after, 43 records). |
| Regression | Neither candidate has any influence outside left flex90. The other 11 D1 poses and all 42 other suite poses are bit-identical to SW3 (§4). |
| Production deformation accepted? | **No.** |

**Left flex90 values** (W0 → SW3 → LF1 → LF2; §8 target in brackets):

| Metric | W0 | SW3 | LF1 | LF2 | Target |
|---|---|---|---|---|---|
| Non-contact pairs | 38 | 6 | 1 | **0** | 0 |
| Crease depth (pairs) | 16.6 mm (71) | 7.9 mm (38) | **0.7 mm (2)** | **1.3 mm (4)** | ≤ 2.0 |
| Orientation disagreement | 359 | 122 | 113 | 111 | ≤ 100 — **miss** |
| Local inversions | 0 | 2 | 3 | 2 | 0 — **miss** |
| Folds outside crease/contact | 10 | 4 | 2 | 4 | 0 — **miss** |
| Loop ratio | 0.19 | 0.525 | 0.525 | 0.525 | ≥ 0.50 |
| p95 / max strain | 62 / 103 % | 49.2 / 104 % | 49.3 / 104 % | 49.7 / 103 % | ≤ SW3 + 3 pp / ≤ 125 % |
| Zone proxy | −33.9 % | −32.1 % | −31.8 % | −31.7 % | ≥ −35 % |
| Allowed arm–torso contact pairs | 89 | 63 | 34 | 29 | — |

**Visual judgement** (`LF_flex90_l.jpg`, `LF_fields_strain.jpg`):
- LF1 and LF2 both read as smooth soft-tissue compression at the anterior fold. The red and orange contact/crease marks are essentially gone.
- There is no shelf, spike, seam, ridge, tear or inflated deltoid; the girdle slope and long-limbed read are unchanged.
- Visually they are better than SW3. The remaining failures are numeric:
  - two local inversions;
  - two to four folds outside the declared zone;
  - orientation 111–113.

**Where the residual sits:**
- **Inversions:** face 75106 (rest GH + (−3.5, 8.0, −13.2)) is SW3's own inversion. It survives both candidates. Face 112631 / 123285 sits just beside it.
- **Orientation disagreements:** they extend below the fold, down to GH −24 cm along the anterior axillary line, where the SW3 skinning itself already disagrees with the reference normals.

## 1. Rulings recorded

- **Elbow:** closed for RP2. H2 stays the 60–120° configuration; VC3 is the 130° numeric reference; 130° is a production-rig contact-corrective carry-forward. VC3F1 / F2 are rejected. The overlap-aware physical volume plus ring girth is the primary metric. No retopology failure. No elbow work was done.
- **Shoulder:** SW3 is accepted as the production direction, with these parts:
  - girdle-only bounded weight diffusion;
  - 0.5 LBS / DQS preserve-volume blend;
  - S1 abduction girdle mechanics;
  - current GH and v002 landmark architecture.
- This is not final rig or skin acceptance. Nothing in that architecture was changed.

## 2. Mechanism (§6): one small pose-space corrective

`lf_corr.py` (+ `dqs_blend.py`) builds a rest-space shape key D, evaluated through the unchanged SW3 skinning:

X = (1 − b)·LBS(V0 + a·D) + b·DQS(V0 + a·D)

**Driver.** Left-arm humeral forward elevation, θ_f = asin(forward component of the world humerus direction). Activation a = smoothstep(70°, 85°, θ_f):

| Pose | θ_f | a |
|---|---|---|
| flex90 | 86.2° | 1 |
| flex90_girdle | 61.3° | 0 |
| abd45 / abd90 / abd90_girdle | ≤ 3° | 0 |
| ext30 | −26° | 0 |
| every right-arm pose and every non-D1 pose | — | 0 |

**Support.**
- rest vertices of arm_l / axial within 13 cm of the fold centre (GH_l + (−1.5, 9, −13) cm), full inside 7 cm, C2 taper;
- left of x = 10 cm;
- exact-zero guard: the 3 rings next to the outside are forced to 0.
- Size: 3134 vertices, 3291 faces, 589 cm² of rest surface.
- Rest shape is exact: the key is applied only when a > 0, and D is 0 outside the support.

**Solve (posed, at flex90).**
- Self-contact push: support vertices that face each other and are more than 3 cm apart at rest are pushed to a 0.5 mm gap (LF2: 1 mm).
- The accumulated displacement is Laplacian-smoothed with a Dirichlet boundary and C2-tapered.
- The key is fitted through the blended linear part (fit error 9e-14 cm).
- **LF2** is the single bounded refinement: it adds fold / inversion fairing, pulling vertices whose normal disagrees with their one-ring (cos < 0.5), plus their ring, toward the one-ring mean. It also uses more iterations.

| | LF1 | LF2 |
|---|---|---|
| Changed vertices | 2954 | 3134 |
| Max posed delta | 0.37 cm | 0.67 cm |
| Max rest key | 0.41 cm | 0.79 cm |
| Max delta at the support boundary (β < 0.05) | 7.5e-7 cm | 1.7e-5 cm |

There is no visible support seam (`LF_fields_strain.jpg`, β panel). The key rows are stored with the full-array SHA-256.

## 3. Why the candidates stop here

- LF1 cleared the crease and nearly all non-contact pairs. Its one localized defect class was folds and inversions, which is what LF2 targeted.
- LF2 cleared non-contact to 0 and kept the crease at 1.3 mm. But SW3's own inversion (face 75106) and the folds around it persist, and orientation stayed at 111.
- The order allows no third candidate (§7). Per §12, shoulder experimentation closes.

The residual is a tightly folded patch of the anterior axillary line. It does not respond to contact separation or one-ring fairing at this support size. That points to a production-rig corrective (a sculpted flex90 corrective shape, or a dedicated anterior-axillary helper) rather than further diagnostic iteration.

No result points to topology:
- the fan loops hold at 0.525–0.86 on every pose;
- the defect moves and shrinks with every deformation change tried.

## 4. Regression (§9)

- **Activation is exactly 0** for all 42 suite poses other than left flex90. Their posed inputs are **byte-identical** copies of SW3 (`filecmp`, 42 / 43).
- The 11 other D1 poses re-evaluated with LF1 / LF2 are **bit-identical** posed arrays with identical metrics: right flex90, all left abd / ext / girdle poses, and every right pose.
- Influence never reaches outside D1, so the full suite is unchanged from the v007 SW3 run. That run has no new retained failure outside D1.

## 5. Evidence

Location: `reviews/rac-rp2-evidence/grask_rig_diagnostic_v008/`.

- `sheets/LF_flex90_l.jpg`: W0 / S2 / SW3 / LF1 / LF2 at identical cameras (front, rear, three-quarter front, three-quarter rear, anterior axillary close-up, wire close-up). Overlays: non-contact, crease, contact, orientation, inversion, folds, compressed loops, girdle weight boundary, landmarks.
- `sheets/LF_flex90_r.jpg`, `LF_abd90_{l,r}.jpg`, `LF_overview_{l,r}.jpg`: regression visuals.
- `sheets/LF_fields_strain.jpg`: strain maps for all five cells, |X − X_SW3| for LF1 / LF2, and the LF support β with its boundary.
- `sheets/LF_sections.jpg`: sagittal section through GH at flex90, i.e. the anterior-fold contour.
- `config/LF1.json`, `config/LF2.json`, `corrective/lf{1,2}_key_rows.npz` + logs (driver angles and activations for all 43 poses), `diag/` results and summaries, `hashes/`.

**Tools** (`tools/rac/rp/grask_rigprep_v001/`): `lf_corr.py`, `dqs_blend.py`, `lf_maps.py`. `shoulder_sheets.py` is used with `config/sheets.json`.

## 6. Exact next ChatGPT decision

Record the final RP2 deformation disposition:
- retopology frozen;
- elbow closed with 130° as a production contact-corrective item;
- SW3 as the shoulder production direction, with **left flex90 anterior-axillary fold** as a named production-rig corrective item. Inputs for it: LF2 is the best diagnostic reference (0 non-contact pairs, 1.3 mm crease, smooth visual read); the residual is 2 inversions, 4 folds outside and orientation 111.

Then decide the next stage, outside this order's scope: production rig planning, or the next race / RP stage.

Production deformation is not accepted. STOP for ChatGPT review.
