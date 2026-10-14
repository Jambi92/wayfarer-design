# RM-OT-05U7 EDIT_LOG (real desktop Blender 5.2.2 LTS on Tyler's computer)

**Start state.** `GO-05U7_handoff.blend` (sha `ad610624a2dc866eaae44b8b9351d90b08bf6c98fcfef932a4a874f1c8eb20ca`).
- Built by `u7_build_handoff.py` from the accepted U6A cp3 scene `GO-05U6_cp3.blend` (`22345d4d…`).
- Positions are bit-identical to cp3. It adds vertex groups `EDIT_upper_crease_U7` (5) and `FROZEN_ring_U7` (14), plus text `RAC_U7_README`.
- It was precheck-verified: every U7 gate passes, and the result is byte-identical to cp3.
- It was delivered next to `GO-05T_references.blend` in `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/sheets/gorrund_05U5_bounded_sculpt/scene/` and opened in Blender with File > Open; the reference library loaded.

**Method.** Order §5, direct Edit Mode vertex movement:
- Front Orthographic view (posterior), vertex select.
- Each vertex was picked by clicking and **confirmed by its coordinates** in the sidebar Item panel.
- The local surface was inspected in a zoomed view before typing.
- The new position was typed into the Vertex X / Y / Z fields (cm).

No Grab, Smooth, Dyntopo, remesh, script, solver, sweep or projection was used. Only the 5 U7 target vertices were eligible. **61522 was held frozen**: it is an endpoint of the frozen crease-B entry edge.

**How positions were chosen.** By hand, from read-only descriptions of the current geometry: a dented vertex is lifted part of the way along its own vertex normal, keeping the groove. No position was tried offline before it was entered.

## Checkpoint 1: `GO-05U7_cp1.blend` (sha `d2546bcaa3214c476bb7e2fa843a6d635a4ae8edf3ca020500be07b8d0e8a738`)

| S3 vertex | cp3 (cm) | Dent (inside neighbour centroid) | Typed (cm) | Moved |
|---|---|---|---|---|
| 61771 | (29.0226, −13.8314, 171.2155) | 0.164 | (29.068, −13.930, 171.165) = +0.12 along n (0.382, −0.823, −0.421) | 0.120 cm |
| 61586 | (28.8009, −14.1649, 171.5079) | 0.087 | (28.840, −14.208, 171.491) = +0.06 along n (0.646, −0.712, −0.276) | 0.060 cm |
| 62063 | (29.4131, −14.0766, 172.1260) | 0.100 | (29.422, −14.144, 172.109) = +0.07 along n (0.125, −0.961, −0.248) | 0.070 cm |

Verified with `check_return_u7.sh`: **all U7 safety gates PASS, exit 0.**
- Crease A 0.7890; crease B 0.3620 (cp3 0.3658).
- U7 local minimum angle 12.68.
- U6 no-regression: target roughness max 35.29, cap minimum 13.41.

Facet diagnostic (dihedral, no threshold), cp3 → cp1:
- max 35.64 → 35.40; p95 30.42 → 33.22; mean 10.25 → 9.41.
- 61771's edges dropped from 35.6 to 18.7, but **62027 became a relative pit**: edges 62027–62063 at 35.4 and 62027–62086 at 33.2.

Visual: the U7-area cut at z ≈ 171.5 is softer. Not resolved, so checkpoint 2 followed.

## Checkpoint 2 (final; budget 2 of 2): `GO-05U7_cp2.blend` (sha `1de9d0ac88f0011062a37f75eed6b6811a5288ae1ef80cc632bfc18c38bfb667`)

| S3 vertex | cp1 (cm) | Dent | Typed (cm) | Moved |
|---|---|---|---|---|
| 62027 | (29.3640, −13.8471, 171.3431) | 0.093 | (29.374, −13.902, 171.321) = +0.06 along n (0.17, −0.92, −0.36) | 0.060 cm |

Verified: **all U7 safety gates PASS, exit 0.**
- Crease A 0.7890; crease B 0.3503 (threshold 0.2743).
- U7 local minimum angle 12.68.
- U6 target roughness max 35.29; cap minimum 13.41.

Facet diagnostic, cp3 → cp2:
- **max 35.64 → 33.56; p95 30.42 → 23.50; mean 10.25 → 9.38.**
- The remaining sharpest edges run to frozen-ring vertices 61735 (33.56) and 61940 (30.89).

Blender was left in Object Mode on the saved `GO-05U7_cp2.blend`.
