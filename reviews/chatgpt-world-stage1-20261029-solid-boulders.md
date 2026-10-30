# Stage 1: solid cavern boulders — v043

The reported walk-through rocks were traced to a 73-boulder field with actor collision disabled and a NoCollision profile. Its geometry also had inward-facing triangles and open pole seams, which contributed to the hollow appearance. Earlier route checks did not test pushing into each off-route boulder.

The isolated v043 development level replaces that field with closed, outward-facing geometry and Pawn-blocking collision using the full-detail mesh. Non-pole surface vertices, boulder bounds and placements are retained. Earlier levels and assets are preserved.

Validation:
- All 318 components across five major rock groups are closed and face outward.
- 3,816 direct native line/capsule probes passed from six directions, using the Pawn collision profile.
- Six normal-time walking/jumping trials across three repaired boulders completed with grounded landings. All 510 recorded capsule-center and camera samples remained outside the repaired solid volumes.
- The saved level was reopened; collision and retained route/boundary checks passed again. Its native mesh export matches the repaired source and the pre-reopen export.
- Map Check reported zero errors and zero warnings.
- Lit player views and unlit diagnostic close-ups were inspected. Normal cave lighting was restored.
- A compressed checkpoint was verified, and all 43 earlier preservation manifests passed.

This accepts the focused collision and surface-integrity repair. It does not declare final cavern art, all possible player interactions, combat behavior or shipping performance complete. Character work and canonical design were not changed.

Next world-building work should continue the approved cavern direction after this collision repair, with direct obstacle-contact checks included in future traversal passes.
