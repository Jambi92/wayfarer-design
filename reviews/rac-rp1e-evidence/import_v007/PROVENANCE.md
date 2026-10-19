# RP1E v007 — UI import provenance (ruling 3816926 §3)

## Before import (frozen design)
- Design: `design_v007.npz` (sha256 f74a70ac…00af), colours `design_v007_col.npy` (fada0a10…b009).
- Content: cage_Y5 (ears, jaw rings, thigh rings, pelvis-front/crotch, both axilla annuli, tail-root annulus — each authored by the design scripts in tools/rac/rp/rp1e/) with the 1664 vertices kept from v006 snapped exactly to their v006 coordinates (≤ 0.008 cm), 1044 new vertices.
- Counts: V 2708, F 2755 (2657 quads, 98 tris). 0 coarse self-x, 0 boundary, Euler 2.
- Import artefact: `RP1E_cage_v007_design.obj` (Y-up, metres; sha256 5dcb2947…f97b), placed on the PC at `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\production\Gorrund\RP1\`.

## Blender UI step (Tyler's PC, Blender 5.2.2, no Python console)
1. File > Open `GO_U_REF_RP1E_retopo_v006.blend` (sha 46fc46ce…5f79c; unchanged on disk).
2. File > Import > Wavefront (.obj), defaults (scale 1, forward −Z, up Y).
3. Object > Apply > Rotation (importer's X 90° → identity; location 0, scale 1).
4. Old object "Cylinder" deleted (it is entirely replaced; accepted regions are carried bit-for-bit through the snapped coordinates, not re-shaped). Imported object renamed to "Cylinder" (F2).
5. No join/merge needed (the design is already the one closed body cage); no other edits.
6. File > Save As `GO_U_REF_RP1E_retopo_v007.blend` (sha256 349c7504e44b060b22c15fde6369809330341de9a663033cc2c59a682abe7d41). v005 and v006 untouched.

## After import (staged v007, `v007.npz`, sha 96760e5d…5dcb)
- Object Cylinder: 2708 V, no modifiers, identity matrix; weldsrc unchanged (562,265 V).
- Vertex order and face list identical to the design (index-matched); max deviation 0.00025 mm (float32 round-off) ≤ 0.10 mm.
- 0 boundary, 0 non-manifold, Euler 2 (genus 0), 1 component, 0 inconsistently oriented edges, 0 coarse self-intersections.
- Finding: the design itself carries one degenerate triangle — verts 2596/2597 coincide (L axilla annulus, (20.8, −22.6, 160.4)), face (2597, 476, 2596) area 0. The import reproduced it faithfully. It violates the "0 degenerates" contract item → class A, repaired in design v008 (2596/2597 respaced at 1/3 and 2/3 of 2595→2598; 0 coarse self-x).

Verification script: `verify_import.py design_v007.npz v007.npz verify_v007.json`.
