# RP1F hand-claw proportion mockups (toward v016) — status and next steps

**Date:** 2026-10-20
**Author:** Claude. This is a handoff for ChatGPT, which Tyler asked to take over this step.
**Status:** 3 direction mockups rendered and sent to Tyler. **Tyler has not picked a direction yet.** Nothing new is frozen and nothing has been imported on the PC.

## 1. Where things stand

| Item | State |
|---|---|
| v014 (`GO_U_REF_RP1E_retopo_v014.blend`) | Frozen technical baseline. Do not overwrite. |
| v015 (`GO_U_REF_RP1F_refine_v015.blend`) | On the PC. It passes every gate (see `reviews/claude-rac-rp1f-gorrund-v015-localized-refinement-gate.md`). Do not overwrite. |
| v015b (thumb second pass) | Cloud only: `../gorrund_v015b/`. Gate clean. PLY halves are on E: in the RP1 folder. The `.blend` was **never made**, and it is probably superseded by the new claws. |
| **Tyler's verdict on v015/v015b hand claws** | *"that retractable nail look really silly with such a big finger. the two don't really match at all in proportion."* The claws are far too small for the huge Gorrund fingers. He asked to see 2–3 mockups first. |
| Toe claws, whisker pads | Tyler has not objected. Keep them as in v015. |

## 2. The mockups (`renders/`)

Each image is 2×2: **CURRENT v015b | A | B | C**. The left hand only.

- `1_hand_top.png` is the best overall read.
- `4_fingertips_top.png` and `5_fingertips_side.png` are close-ups.
- `2_hand_front.png` and `3_hand_outside.png` are also included.

| Variant | Idea | Parameters (`params/mock2_sdf.json`, via `tools/mockgen.py`) |
|---|---|---|
| **A — bigger sheathed claw** | A cat-like retractable claw at about 2× the v015 size, coming out of a soft sheath | root 0.9, depth 0.35, ext 0.9, hook 0.45, arch 0.15, r0 0.5, lat 0.6, taper 0.7, k 0.15, blur 0.12 |
| **B — thick hooked claw** | The biggest. A wide-based, long, hooked claw with no sheath, growing straight from the fingertip | root 0.8, depth 0.1, ext 1.4, hook 0.8, arch 0.3, r0 0.75, lat 0.6, taper 0.8, k 0.05, blur 0.15 |
| **C — claw-shaped nail** | Bear- or badger-like. A broad, thick nail that ends in a blunt point, with nothing retractable | root 1.0, depth 0.55, ext 0.5, hook 0.25, arch 0.05, r0 0.75, lat 0.75, taper 0.9, k 0.08, blur 0.0 |

- All values are in cm, in the clawsdf frame (§4).
- The thumbs use ×1.15 on root, depth, ext, hook, arch and r0, with half 2.4, h 0.04 and c0back = 0.3·L.

**The mockups are render-only.** `splice.py` deletes the base-mesh faces within 1.8 cm of each claw and pastes the marching-cubes target triangles in their place. That explains the faint square outlines, the stair-step lines (0.4 mm voxels) and the seams. **They are not production geometry.**

## 3. Next steps (what Claude was going to do)

1. **Get Tyler's pick.** The choice is A, B, C, or a mix (for example "C's shape at B's length"), plus any size up or down. Do not build before he picks.
2. **Generate parameters for all 10 digits.** Use the chosen variant's values in `mockgen.py` style. Apply them to all 10 nails in `params/hand_frames.json`:
   - A_L17–A_L20 and A_Lthumb;
   - A_R21–A_R24 and A_Rthumb.

   Keep the v015b thumb erase settings (`erase_ru` 1.5/1.6, `erase_rs` 1.75, blur 0.25), and keep the thumbs at ×1.15. Use h ≈ 0.02 cm for the final targets, not 0.04: it is finer and removes the stair-steps.
3. **Build the targets.** Run `clawsdf.py t3.npz <sdf.json> <name> tg_<name>.npz` for each nail. Get `t3.npz` from `tools/make_t3.py` (v014 plus v015 pads and toes, with the hands still at v014).
4. **Transfer onto the production mesh, with the topology unchanged.** This is the hard part.
   - `projn.py` (Blender Python; Claude ran it with `/home/claude/stc/bin/python3`, which is bpy as a module) ray-casts each vertex along its normal, **max 0.5 cm**. That works for v015's small claws, but **the first mockup transfer failed for the bigger claws**: B extends about 1.4 cm past the tip, and the normals cannot reach it.
   - Planned fix:
     - (a) raise the ray limit to about 2 cm and use more tangential relax and re-project rounds (NREL 15–25), with radius R about 1.6–2.0 and R ≤ half − 0.25;
     - or (b) do a two-stage transfer: first a coarse closest-point pull of the tip-region vertices along e1 toward the claw centreline, then `projn` onto the target.
   - The production quad density at the fingertip has to stretch over a longer claw, so check that the quads don't collapse. Count degenerate faces, and look at the min edge length at the claw tip.
5. **Repair self-intersections.** Use `fixall.py` (in `tools/`; env `REG=x,y,z,R`, args `IN OUT 60 0.0 0.7`) locally, for each digit. v015 needed this: the R thumb had 1093 crossing pairs before the repair.
6. **Gate, the same way as v015** (scripts are in `../gorrund_v015/tools/` and `../gorrund_v015b/`):
   - genus 1, 0 boundary, 0 non-manifold, 0 degenerate faces, **0 global self-intersections**;
   - the quad count stays 1 427 072;
   - 0 vertices moved outside the masks (`delta15b.py`; the hand masks can grow to about 3.8 cm radius around each T);
   - bbox and stature delta 0, unless a claw now sets the bbox (fingers point down at the sides, so check this);
   - T-6 max no more than 1.122 mm and T-7 IoU no less than 0.997, or explain why not.
7. **Freeze as v016** in a new folder (`reviews/rac-rp1f-evidence/gorrund_v016/`):
   - renders labelled "v015 | v016", following the v015 §7 list (`cmp.py` and `pair.py`);
   - a gate report and `claw_dimensions.json`.

   Do **not** overwrite v014, v015 or v015b.
8. **Import on the PC, and only when Tyler says he is free.** Split the mesh into PLY halves with `writeply2.py` (each PLY must be under 30 MB to cross the file link). Then, in the Blender UI:
   1. Open v014.blend and delete the production object.
   2. Import both PLYs.
   3. Ctrl+J, then Merge by Distance at 0.000001. Type the digits as separate key presses.
   4. Rename the object `RP1F_production_v016`.
   5. Save As `GO_U_REF_RP1F_refine_v016.blend` in the RP1 folder.
   6. Close Blender, and close the Explorer window you opened.

   Then stage the `.blend` back to the cloud and verify it with `verify15.py`.

## 4. Claw model (`tools/clawsdf.py`, in short)

**Local frame.**
- C is the plate centre and T is the nail free edge (both are picks in `hand_frames.json`).
- n is the dorsal normal: the mean of the vertex normals within 2.5 mm of C.
- e1 is the distal axis: (T − C) projected off n.
- e2 = n × e1.

**Target.** The body signed distance is computed on a grid (box half-width `half`, centred at T − c0back·e1). The human nail-plate border is erased by Gaussian-blurring the SDF over the plate ellipse (`erase_rs` and `erase_ru`).

**Claw.** The claw is an elliptical cone along a quadratic Bézier:
- p0 = T − root·e1 − depth·n
- p1 = T + 0.15·ext·e1 + arch·n
- p2 = T + ext·e1 − hook·n

Its radius is r0·(1−t)^taper + rtip, and it is laterally squashed by `lat`.

**Surface.** The claw is joined to the body by smooth-min with k, and that fillet forms the sheath. A marching-cubes run gives the target mesh.

**Frames and paths.**
- Mesh files are stored with y flipped relative to the Blender frame; `V*[1,-1,1]` converts between them.
- All scripts have hard-coded paths under `/tmp/claude-0/rp1f/`. Change those paths to your own folder.

## 5. Standing rules from Tyler

- Do Blender work in the cloud. Use his screen only when he says he is free (he is writing music).
- Close every Blender and Explorer window you open, and leave the old Explorer window alone.
- Downloads go to E:.
- `GO-05AW4_nails_final.blend` (the source) is read-only.
- Don't relax the contract.
