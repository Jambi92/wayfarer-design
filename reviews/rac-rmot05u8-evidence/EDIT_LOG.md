# RM-OT-05U8 EDIT_LOG (real desktop Blender 5.2.2 LTS on Tyler's computer)

**Start state.** `GO-05U8_handoff.blend` (sha `d71cba0716a3356005005c6095a6fb0b0c5d3a3b1ace6b4f99789f34fda1effc`).
- Built by `u8_build_handoff.py` from the accepted U7 cp2 scene `GO-05U7_cp2.blend` (`1de9d0ac…`).
- Positions are bit-identical to cp2. It adds vertex groups `EDIT_lower_cut_U8` (4) and `FROZEN_ring_U8` (15, including 61580), plus text `RAC_U8_README`.
- It was precheck-verified: every U8 gate passes, and the result is byte-identical to cp2.
- It was delivered next to `GO-05T_references.blend` and opened in Blender with File > Open.

**Method.** Order §6, direct Edit Mode vertex movement:
- Front Orthographic view (posterior), vertex select.
- Each vertex was picked by clicking and **confirmed by its coordinates** in the sidebar Item panel; the local surface was inspected zoomed.
- The new position was typed into the Vertex X / Y / Z fields (cm).

No Grab, Smooth, Relax, Dyntopo, remesh, script, solver, sweep or projection was used. **61580 was never moved**: crease-B anchor, frozen.

**How positions were chosen.** By hand, from read-only descriptions of the cp2 geometry: each dented vertex is lifted part of the way along its own vertex normal, keeping the groove. No position was tried offline before it was entered.

## Checkpoint 1: `GO-05U8_cp1.blend` (sha `2341d55445a448e24852f98fd9df3984ab12d706ef0b455cb4a2cdb0782860d6`)

| S3 vertex | U7 cp2 (cm) | Dent at cp2 | Typed (cm) | Moved |
|---|---|---|---|---|
| 61562 | (28.7734, −13.2015, 169.2494) | 0.156 | (28.845, −13.262, 169.216) = +0.10 along n (0.718, −0.609, −0.336) | 0.0995 cm |
| 61727 (support) | (28.979, −12.919, 169.128) | 0.151 | (29.011, −12.981, 169.090) = +0.08 along n (0.40, −0.78, −0.48) | 0.0792 cm |
| 61735 | (28.9873, −14.3945, 172.8225) | 0.089 | (29.016, −14.435, 172.815) = +0.05 along n (0.582, −0.799, −0.149) | 0.0502 cm |
| 61940 | (29.2581, −14.2689, 172.9069) | 0.134 | (29.277, −14.346, 172.893) = +0.08 along n (0.228, −0.959, −0.171) | 0.0806 cm |

Saved with Save As `GO-05U8_cp1.blend` and verified with `check_return_u8.sh`: **all 22 U8 safety gates PASS, exit 0.**
- 61580 unmoved.
- Crease A 0.7788; crease B 0.3503 (unchanged).
- U8 local minimum angle 16.16; U7 local quality 12.68.
- U6 target roughness max 32.41 (cp2 35.29); cap minimum 13.41.

**Dihedral, U7 cp2 → U8 cp1:**

| Measure | cp2 | cp1 |
|---|---|---|
| 61562–61580 | 41.82 | **32.28** |
| Corridor max | 41.82 | 32.28 |
| Corridor p95 | 35.32 | 29.53 |
| Corridor mean | 14.31 | 13.64 |
| Worst edge at 61735 | 33.56 | 29.20 |
| Worst edge at 61940 | 30.89 | 22.59 |

**Visual.** The lower cut is softer but **still visible**: a dark wedge at yaw 0, yaw 20 and pitch −45. In the 6 cm close view its apex sits at about (28.7, 168.6). Read-only offsets at cp1 (`diagnostics/cp1_anchor_offsets.txt`):

| Vertex | Role | Offset (inside neighbour centroid) |
|---|---|---|
| **61581** | Crease-A anchor; U6-edited; U8 ring | **0.121 cm** (outlier face 130139 at 29.9°) |
| **61580** | Crease-B anchor | **0.117 cm** |
| 61562 | U8 target | 0.066 cm, after its lift |
| 61727 | U8 target | 0.107 cm |
| 61405 | Ring | 0.062 cm |
| 61219 | Ring | 0.003 cm |

The remaining cut is carried by the two frozen crease-anchor dents. Further lifting inside the U8 set would deepen their relative pits rather than remove the cut.

## Checkpoint 2: not spent

Per order §7, checkpoint 2 is not spent "merely to move unrelated vertices" when the reason is the frozen anchor endpoint. Blender was left in Object Mode on the saved `GO-05U8_cp1.blend`.
