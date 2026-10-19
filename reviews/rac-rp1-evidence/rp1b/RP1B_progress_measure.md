# RP1-B progress measurement (diagnostic, not a gate) — 2026-10-18

**Order:** `reviews/chatgpt-rac-rp1-gorrund-manual-retopo-execute-order.md` §7. This checks the §7 STOP clause: can the manual plan meet the accepted deviation gates without changing anatomy?

## Checkpoint measured
- **File:** `RaceBodies\production\Gorrund\RP1\GO_U_REF_RP1_retopo_v002.blend`, sha256 `e2ee2efe…0fe3`. It is staged read-only and never saved by the tools.
- **Cage:** manual cage object `Cylinder` with 1,462 vertices and 1,440 faces.
  - All faces are quads: 0 triangles, 0 n-gons, 0 non-manifold edges.
  - It has 48 boundary edges. These are the four open ends still to be closed: the wrists (10 + 10) and the ankles (14 + 14).
  - Built so far: trunk, legs (crotch gusset), arms (shoulder holes), neck and head (11 shaped rings plus a grid-filled cap) and tail (14 extrusions along the source tail chain).
  - Not built yet: hands, feet, ear / face feature loops and joint support loops.
- **Evaluation:** Catmull-Clark subdivision level 3 inserted before the existing Shrinkwrap (nearest surface point onto weldsrc). This gives 92,350 vertices.
- **Tools:**
  - `tools/rac/rp/rp1_ck_export.py` (bpy, read-only);
  - `tools/rac/rp/rp1_ck_measure.py` (two-way deviation by T-2 zone).
- **Results:** `v002_L3_dev.json`, heat map `v002_heat.png`.

## Result
- **Where the cage reaches the source, the error is already inside tolerance.**
  - Median source→checkpoint distance: trunk 0.18 mm, forearms 0.05–0.06 mm, thighs and shins 0.05 mm.
  - The tail root zone passes T-2: max 0.785 mm both ways.
- **The out-of-tolerance error comes from regions the cage does not cover yet:**
  - shoulder caps / deltoids;
  - upper back and trapezius;
  - ear tips;
  - groin gusset;
  - tail-tip tuft;
  - hands and feet, which are not built (src→prod ≈ 86–150 mm).
- Every one of these is missing cage geometry. None is something the method cannot reach.

## STOP-clause reading
**Not triggered.** Nothing so far shows that the manual plan cannot meet the gates without changing anatomy. The gaps close by adding manual cage coverage. Work continues under §7: RP1-B coverage at the shoulder / back / groin, then RP1-C.

The real risk for T-2 is unchanged from RP1-A §5: ear rims, lips / nostrils / eyelids, between-digit crevices and nail-plate edges. These need feature-following loops.
