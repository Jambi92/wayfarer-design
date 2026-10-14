# RM-OT-05U8A EDIT_LOG (real desktop Blender 5.2.2 LTS on Tyler's computer)

**Start state.** `GO-05U8A_handoff.blend` (sha `1ec2240d22df4dcea320d2e49389e0187bf775e4661a0d043cf0d3963f0dcb7a`).
- Built by `u8a_build_handoff.py` from the accepted U8 cp1 scene `GO-05U8_cp1.blend` (`2341d554…`).
- Positions are bit-identical to U8 cp1. It adds vertex groups `EDIT_crease_anchors_U8A` (61580, 61581) and `FROZEN_ring_U8A` (12), plus text `RAC_U8A_README`.
- It was precheck-verified: every U8A gate passes, and the result is byte-identical to U8 cp1.
- It was delivered next to `GO-05T_references.blend` and opened in Blender with File > Open.

**Method.** Order §5, direct Edit Mode vertex movement:
- Front Orthographic view, vertex select.
- The vertex was picked by clicking and **confirmed by its coordinates** in the sidebar Item panel; the local surface was inspected zoomed.
- The new position was typed into the Vertex X / Y / Z fields (cm).

No other tool or script was used. The crease reference file was not touched.

## Checkpoint 1 (crease-A anchor 61581 only): `GO-05U8A_cp1.blend` (sha `5e07e11d676b859b09210ba8a0e55010a2ff50eb6fb3d3eb2fca0ecb2d950067`)

| S3 vertex | U8 cp1 (cm) | Dent at U8 cp1 | Typed (cm) | Moved |
|---|---|---|---|---|
| 61581 | (28.860, −12.883, 168.652) | 0.121 | (28.897, −12.923, 168.627) = +0.06 along n (0.620, −0.670, −0.410) | **0.05995 cm** (limit 0.06) |

Saved with Save As `GO-05U8A_cp1.blend` and verified with `check_return_u8a.sh`: **all 24 U8A safety gates PASS, exit 0.**
- 61580 not moved. Step within limit.
- **Crease A 0.7788 → 0.7210** (threshold 0.6713). Crease B 0.3503 (unchanged).
- U8A local minimum angle 13.41. Face 130139 minimum angle 14.87 → 16.09.
- U6 target roughness max 33.64.

**Dihedral (diagnostic), U8 cp1 → U8A cp1:**

| Edge or measure | U8 cp1 | U8A cp1 |
|---|---|---|
| **61219–61581** | 34.16 | **45.90** |
| **61219–61405** | 30.51 | **38.13** |
| 61405–61581 | 22.11 | 27.15 |
| 61562–61580 | 32.28 | 32.28 |
| Corridor max | 34.16 | 45.90 |
| Corridor p95 | 31.83 | 36.69 |
| Corridor mean | 15.62 | 17.81 |

**Visual** (identical cameras, lower-close / zoom / posterior / 3-4):
- The lower dark wedge is **essentially unchanged** at yaw 0, yaw 20 and pitch −45. There is no material improvement.
- Lifting the anchor moved the fold onto the crease-wall edge 61219–61581 instead of removing it.

## Checkpoint 2: not spent

Order §5 permits checkpoint 2 only if checkpoint 1 "materially improves the wedge". It did not. The facets got sharper and crease A gave up 0.058 cm of margin for no visible gain, so 61580 was not moved.

**Result:** U8A LIMIT REACHED / PRESERVE CREASE OVER FURTHER FACET REDUCTION. The preserved return is the unchanged U8 cp1 scene. The U8A cp1 attempt is kept as evidence only.

Blender was left in Object Mode on `GO-05U8A_cp1.blend` (the attempt). The preserved scene is `GO-05U8_cp1.blend`.
