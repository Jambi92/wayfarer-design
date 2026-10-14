# RM-OT-05U6 EDIT_LOG (real desktop Blender 5.2.2 LTS on Tyler's computer)

**Start state.** `GO-05U5_sculpt_RETURN.blend` (sha `b45f42ae…`), which is 05U5 checkpoint 0, geometrically identical to the 05U baseline. It sits beside `GO-05T_references.blend` in `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/sheets/gorrund_05U5_bounded_sculpt/scene/`.

**Method.** Direct Edit Mode movement of specific local notch vertices, as permitted by order §3:
- Front Orthographic view (looking at the posterior, −Y).
- Vertex select. Each vertex was picked by clicking and confirmed by its coordinates in the sidebar Item panel before any change.
- The new position was typed into the sidebar Vertex X / Y / Z fields (displayed in cm, identical to S3 cm).
- No brush, Grab, Dyntopo, remesh, global smoothing, projection, script, solver, sweep or candidate generation.

**How positions were chosen.** By hand, from a read-only description of the baseline local geometry (`diagnostics/baseline_local_geometry.txt`, tool `u6_local_diagnostic.py`):
- a dent vertex is lifted part of the way along its own vertex normal;
- the valence-3 sliver vertex goes to the centroid of its three neighbours.

No position was tried offline before it was entered.

## Checkpoint 1: `GO-05U6_cp1.blend` (sha `6262620e18732d1672ea4b62d53581eda2a34e4329144a91936cc51f42ddf2dd`)

| S3 vertex | Reason | Baseline (cm) | Typed (cm) | Moved |
|---|---|---|---|---|
| 61303 | Lower notch dent: 0.51 cm inside its neighbour centroid; roughness 47.95° | (28.4065, −12.2459, 167.4383) | (28.589, −12.416, 167.458) = +0.25 along its normal | 0.2502 cm |
| 62065 | Strip dent: 0.45 cm inside; roughness 36.57° | (29.4131, −11.9516, 167.5247) | (29.391, −12.150, 167.517) = +0.20 along its normal | 0.1998 cm |
| 61405 | Valence-3 vertex forming sliver 130139 (6.24°) | (28.5595, −13.3114, 168.7177) | (28.620, −13.378, 168.827) = centroid of 61219 / 61562 / 61581 | 0.1416 cm |

- Left Edit Mode, then Save As `GO-05U6_cp1.blend` (a distinct checkpoint).
- Verified with `bash tools/rac/w1/rmot05u6_drivers/check_return_u6.sh` on a staged copy beside the reference.
- **Every U6 gate passes except R1 target roughness.**
  - 61559 is at 54.23°: a pit left between the two lifted neighbours.
  - 61581 is at 42.43° (was 47.85°).
  - 61580 is at 40.95° (unchanged; crease-B anchor, deliberately not moved).
- R2 passes: face 130139 rose from 6.24° to **13.61°**; minimum cap angle 13.61°; no new edge outside the band.
- Crease A and B are unchanged (0.8951 / 0.3658).
- The three exceptions are bit-exact, and nothing outside the target moved.

## First attempt at checkpoint 2 (05U6): blocked

The first Blender action of checkpoint 2 was denied by the session's automatic safety check ("Security Weaken"). No desktop action followed, and Blender stayed on the saved checkpoint 1.

## Checkpoint 2 (05U6A, resumed from cp1 sha `6262620e…`): `GO-05U6_cp2.blend` (sha `6cdc401c16693e13db5755b49c7a52b4240750c8adb657eff36e693f21b0ee79`)

Under order `reviews/chatgpt-rac-rm-ot-05u6a-resume-remaining-desktop-checkpoints-order.md`, desktop control was permitted.

Before typing, the local surface was inspected in Edit Mode: 61559 sits in a visible recess at the crease edge. The documented plan was executed as written; current normals at cp1 equal the planned ones.

| S3 vertex | cp1 position (cm) | Typed (cm) | Moved |
|---|---|---|---|
| 61559 | (28.7675, −12.1007, 167.7268) | (28.915, −12.359, 167.679) = +0.30 along its normal | 0.3012 cm |
| 61581 | (28.7970, −12.8169, 168.6922) | (28.860, −12.883, 168.652) = +0.10 | 0.0998 cm |
| 61750 | (28.9971, −13.3585, 170.0225) | (29.031, −13.434, 169.968) = +0.10 | 0.0991 cm |

**Verification:** every U6 gate passes except R1 target roughness, on **61581 only (45.44°)**.
- 61559: 54.23 → 16.64.
- 61580: 40.95 → 26.38, through the indirect 61750 move; 61580 itself was not moved.
- Crease A: 0.8951 → 0.7890 (margin 0.118). Crease B: 0.3658, unchanged.
- R2: minimum cap angle 13.63; face 130139 at 14.87.
- Visually safe and materially closer: no new dent, lip or spike.

The remaining outlier is face 130354 (61581, 61652, 62052), where 62052 is on the frozen ring. Its neighbour 61652 was a 0.22 cm dent (`diagnostics/cp2_remaining_offender.txt`).

## Checkpoint 3 (final; one small correction inside the target): `GO-05U6_cp3.blend` (sha `22345d4d270b84753d3cdf32086d66846644448105aba1db710faaa083746029`)

| S3 vertex | cp2 position (cm) | Typed (cm) | Moved |
|---|---|---|---|
| 61652 | (28.8853, −12.5128, 168.3566) | (28.929, −12.608, 168.298) = +0.12 along its normal (0.37, −0.79, −0.49) | 0.1201 cm |

The crease anchors 61581 and 61580 were deliberately not moved in this checkpoint.

**Verification: every U6 mandatory gate PASSES; the aggregate exits 0.**
- Target roughness max 35.29 (61562); 61581 at 32.07.
- Crease A 0.7890 and B 0.3658, both PASS.
- R2 PASS.

**Budget:** cp1, cp2 and cp3 are all spent. No further checkpoint is possible.

Blender was left in Object Mode on the saved `GO-05U6_cp3.blend`.
