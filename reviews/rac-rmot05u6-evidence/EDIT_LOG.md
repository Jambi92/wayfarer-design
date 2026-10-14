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

## Checkpoint 2: planned, not executed (desktop editing blocked)

The plan, from `diagnostics/cp1_remaining_offenders.txt`:
- lift 61559 by 0.30 along its normal, to (28.915, −12.359, 167.679);
- lift 61581 by 0.10, to (28.860, −12.883, 168.652); crease A margin is 0.22 cm;
- lift 61750 by 0.10, to (29.031, −13.434, 169.968), aimed at 61580's outlier face 130133 without moving the crease-B anchor.

The first Blender action of checkpoint 2 (entering Edit Mode and selecting 61559) was **denied by the session's automatic safety check** ("Security Weaken"). Tyler had approved the checkpoint 1 edits in chat after an earlier denial. Following the rule not to work around a denial, no further desktop action was attempted.

Blender was left in Object Mode on the saved `GO-05U6_cp1.blend`, with nothing unsaved.

**Budget:** 1 of 3 U6 checkpoints used; 2 remain unspent. The 05U5 budget is preserved as completed evidence and was not reset.
