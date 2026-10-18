# RAC RP1 Gorrund — author release decisions

Date: 2026-10-18
Authority: Tyler approval via ChatGPT.
Parent: specs/RAC_PRODUCTION_MESH_CONTRACT.md
Pilot: reviews/chatgpt-rac-rp1-gorrund-production-retopo-pilot-HOLD.md

## Method
Use M-B: fully manual retopology in Blender.

For RP1, do not use QuadriFlow or automatic remesh as the production topology generator. Manual polygon construction with snapping/projection to the derived welded working copy is the governing method.

## Accepted production tolerances
These are technical production tolerances, not biology canon.

- T-1 general surface deviation: median <= 0.5 mm; p95 <= 1.5 mm; maximum <= 3.0 mm.
- T-2 identity zones (head/muzzle, ears, hands, feet/toes/nails, tail root): median <= 0.3 mm; p95 <= 0.8 mm; maximum <= 1.5 mm.
- T-3 stature: +/-1.0 mm. Bounding box: +/-2.0 mm per axis.
- T-6 landmark drift: target <= 1.0 mm; none above 1.5 mm. Any value above 1.0 mm is individually reported.
- T-7 silhouette IoU: >= 0.995 in front/profile/rear at identical camera and scale.
- Gorrund nail projection: +/-0.15 mm from the frozen source measurement.
- T-4 / T-5 are accepted as RP1 quality targets.

## Micro-detail
Allowed exemption only for fine skin creases and nail-plate micro-edge detail that does not change projection, taper, curl or silhouette. All exemptions must be listed and shown.

## Visual veto
A numeric pass does not override visible identity change. Head/muzzle, tail origin and taper, hand/foot read, nail read, body composition, accepted proportions and plantigrade foot read must remain visually unchanged.

## Source
Immutable:
E:/UnrealProjects/Wayfarer 5.8/RaceBodies/source/Gorrund-Neutral-C/05AW4/GO-05AW4_nails_final.blend
SHA-256: 5a4e45d40158e7dc92f6f8ba13d67ada2403e3e3dcda9048382323ee43a22d5e

## State
RP0 PASS/CLOSED.
RP1 Gorrund AUTHORIZED.
RP2+ HOLD.
UE5, final production rigging and creator implementation remain unauthorized by this release.
