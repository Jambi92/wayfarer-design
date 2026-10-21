# RP1F v015b — thumb-claw second pass (candidate, pending Tyler's review)

v015b = v015 with the two thumb claws redone; everything else identical to v015.

Why: in v015 the thumb nail plates were under-sized in the erase mask (true plate width is about 2.5–2.8 cm), so the old plate outline survived, and the R thumb claw was about 2.6 mm off the free-edge centre.

Fix:
- Thumb free-edge and plate-centre points re-picked from nail-facing views (`design/hand_frames.json`).
- Erase mask sized to the real plate: half-width 1.5 / 1.6 cm, length 1.75 cm, distance-field blur 2.5 mm.
- Claw base radius 3 mm, 3.5 mm extension.
- Bounded crossing relaxation: 278 crossing pairs removed at the R thumb, 2 at the L thumb.

Gate (`gate/`):
- 1 component, 0 boundary, 0 non-manifold, genus 1, 0 degenerates, 100 % quads, 0 self-intersections.
- Masks: 0 vertices moved outside the five author masks; bbox and stature delta vs v014 are 0.
- T-3, T-6 (max 1.122 mm) and T-7 are unchanged.

Renders: `renders/` (v014 left, v015b right).

Remaining weak spot: a faint lateral plate-fold line on the L thumb.

PC:
- `RP1F_production_v015b_part1.ply` and `part2.ply` are in the RP1 folder.
- `GO_U_REF_RP1F_refine_v015b.blend` will be made through the Blender UI when Tyler is off his computer. The compressed `.blend` (about 55 MB) is over the 30 MB file-link limit, so it cannot be copied over directly.
- v014.blend and v015.blend are not overwritten.
