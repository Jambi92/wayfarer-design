# RAC RP2 — Grask anatomical source v004 extremity reconstruction — final gate

- **Date:** 2026-10-24
- **Order:** `reviews/chatgpt-rac-rp2-grask-3d-source-v004-extremity-reconstruction-order.md` (7fa3b44)
- **Parent:** `GR_U_REF_RP2_SOURCE_3D_v003.blend` (`aad25f89…acbd1`). v003 is not approved; v004 replaces only its extremities.
- **Status:** **RP2 GRASK 3D ANATOMICAL SOURCE V004 EXTREMITY RECONSTRUCTION PASS / READY FOR AUTHOR FREEZE REVIEW**

## 1. Deliverables

| Item | Location | SHA-256 |
|---|---|---|
| Source v004 | `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Grask/RP2/SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v004.blend` | `ed83bf92ca9a20355f28fc6d5c92e99e4c03815a317165a124d75985da168000` (PC readback matches) |
| GLB copy | same folder, `…_v004.glb` | `696f756f12953e61e24a70c1646bcfeec370a6035d0d77019f98bb9c69b84148` (PC readback matches) |
| Geometry hash | — | `6bb4e67b93c5ea5da4f63cf7c2eb87b158fb2016b2ec3e259b90b810c41634d2` |
| Sidecar | `…_v004.json` | `15936d0a…2e95` (PC readback matches) |
| Masks | `…_v004_reconstruction_masks.npz` | `0bb7bf76…f60b` (PC readback matches) |
| Repo GLB copy | `reviews/rac-rp2-evidence/grask_3d_source_v004_extremity_reconstruction/source_copy/…_v004.glb.gz` | `73eb876f…99be` |
| v003 / v002 / v001 | unchanged on PC | `aad25f89…acbd1` / `0651765f…755a` / `2315d5c1…cf86` (re-verified) |

The .blend is saved with Blender's compression so it fits the 30 MB transfer limit. Readback geometry is bit-identical to the uncompressed export. RP2 production v001–v006 were not touched.

The masks file holds:
- `replaced`: rebuilt vertices;
- `seam`: the stitch bands;
- `ground_fix_mm`;
- `dist_from_v003_mm`.

## 2. Reconstruction method

v003's hands and toes were displacement-sculpted mittens and paddles. They had no digit roots, nails or phalange construction, so this pass rebuilds them as new anatomy. Everything else is the v003 mesh, untouched, vertex for vertex.

1. **Anatomical model.** Each hand and forefoot is modelled as an anatomical implicit surface built from bone-like segments. Tools are in `tools/`; `hand_model.py` and `foot_model.py` hold every parameter.
   - **Hand:**
     - palm/metacarpal mass with a dorsal metacarpal fan;
     - thenar and hypothenar masses, and the first web;
     - four fingers, each built as three phalanges with PIP/DIP joint widening, dorsal knuckles and palmar creases;
     - an MCP head row: middle > index > ring > pinky;
     - fingertip pulp pads and a flattened nail bed;
     - a nail on every digit: a recessed U fold (proximal fold plus lateral folds that run out before the tip) and a slightly proud nail plate;
     - a 3-segment thumb from the CMC joint, with its tip reaching toward the proximal index.
   - **Finger pose:** relaxed flexion at MCP/PIP/DIP (index 18/26/14°, middle 20/30/16°, ring 24/34/18°, pinky 28/38/20°), with no hooking.
   - **Finger lengths:** middle > ring ≥ index > pinky.
   - **Foot:**
     - five toes on an oblique MTP line, with MTP heads and dorsal metatarsal ramps;
     - a dominant two-phalanx hallux; lesser toes with three phalanges each and PIP/DIP rhythm;
     - plantar pulp pads, nail beds and toenails;
     - toes sit flat on the ground plane.
2. **Blending into v003.**
   - **Hands:** the new hand is blended into the frozen forearm by a signed-distance cross-fade 1.5–5 cm proximal to the wrist.
   - **Feet:** the original v003 forefoot, ball, arch and heel are kept. The toes and MTP row join them along an oblique cut with a wide smooth blend (k 2.0), so the toe roots carry no crease.
3. **Meshing.**
   - marching cubes at 0.5 mm, then 20 Taubin iterations (no shrink);
   - topology-preserving quadric decimation: hands about 147k V each, feet about 95k V each;
   - genus 0 is checked after both steps.
4. **Stitching.** Each part is stitched into v003 at the plane hand axis u = −6 cm (forearm) and f = 10.5 cm (foot), in five steps:
   - split the v003 faces exactly on the plane;
   - trim the part;
   - snap the loops together (mean offset 0.47 mm);
   - zipper the seam;
   - fair the seam band.
5. **Ground.** The new right toes sat 1.2 mm high. The right forefoot (f > 15 cm only) was lowered by a ramped weight so the sole touches z = 0 exactly. The heel and arch keep v003's positions. The left foot keeps v003's natural stance lift: its new toes clear the ground by 0.5 mm.

Regions rebuilt: both hands distal to the wrist, and both feet distal to the MTP row (toes, MTP heads, toe roots and webs). Nothing else was regenerated.

## 3. Movement vs v003 and scale

Closest-point distance from v004 to the v003 surface (`production/region_movement.json`):

| Region | Vertices | Max | p95 |
|---|---|---|---|
| Head / face | 11,881 | 0.000 mm | 0.000 mm |
| Eyes | 9,117 | 0.000 mm | 0.000 mm |
| Ears | 3,626 | 0.000 mm | 0.000 mm |
| Torso / pelvis / back | 19,329 | 0.000 mm | 0.000 mm |
| Arms above the wrist | 23,320 | 1.231 mm (seam fairing band only) | 0.000 mm |
| Legs above the forefoot | 40,981 | 0.494 mm | 0.104 mm |
| Rest of body (all) | 116,861 | 1.231 mm | 0.000 mm |
| Hand L / R (rebuilt) | 143,883 / 145,192 | 35.1 / 34.1 mm | 17.4 / 21.9 mm |
| Foot L / R (rebuilt) | 91,335 / 91,122 | 24.3 / 20.0 mm | 13.9 / 13.4 mm |

Overall hand and foot scale is preserved (`production/dims4.json`):

| | v003 | v004 |
|---|---|---|
| Hand L, wrist → tip | 26.50 cm | 26.71 cm |
| Hand R, wrist → tip | 26.46 cm | 26.71 cm |
| Fingertip height L / R | 77.68 / 77.74 cm | 77.57 / 77.63 cm |
| Foot L, length / width | 42.31 / 18.90 cm | 41.43 / 18.26 cm |
| Foot R, length / width | 42.42 / 19.91 cm | 42.57 / 19.07 cm |

The feet are slightly narrower because v003's fused toe paddle is now separate toes with webs. The heel, arch, ankle and stance are identical.

## 4. Technical gate (Blender readback)

| Check | v004 |
|---|---|
| Vertices / triangles | 588,393 / 1,176,782 |
| Bodies (components) | 1 |
| Boundary / non-manifold edges | 0 / 0 (watertight) |
| Euler / genus | 2 / 0 |
| Degenerate / coincident / duplicate | 0 / 0 / 0 |
| Seams, holes, floating fragments | none |
| Normals | consistent, outward (+128.89 L in Blender frame) |
| Self-intersections | **0** (BVH triangle-pair test, source and readback) |
| Edge (cm) | median 0.100, min 0.009, max 2.65 |
| Height | **218.000 cm** (z 0.000 – 218.000) |
| Bbox (cm) | [−35.38, −20.36, 0.00] – [34.99, 26.13, 218.00] |

## 5. Evidence (`reviews/rac-rp2-evidence/grask_3d_source_v004_extremity_reconstruction/`)

Every v003/v004 sheet uses identical cameras.
- **A** — `sheet_A_body_v003_v004.jpg`: front, profile, back, 3/4 front, 3/4 back.
- **B1** — `sheet_B1_hands_v003_v004.jpg`: palm, dorsal, 3/4, outer, thumb root, thumb profile, index side.
- **B2** — `sheet_B2_hand_closeups_v003_v004.jpg`: middle side, MCP row, PIP/DIP, fingertip, fingernail, web.
- **B3** — `sheet_B3_hand_pose_check.jpg`: relaxed source pose, opened flatter and fist preview. These are the same anatomy re-posed by joint angles only, as a diagnostic.
- **C1** — `sheet_C1_feet_v003_v004.jpg`: top/front, outer, inner, 3/4, heel, sole.
- **C2** — `sheet_C2_foot_closeups_v003_v004.jpg`: forefoot, hallux, hallux top, lesser toes, lesser top, toe roots/webs, toenail, ground contact.
- **D** — `sheet_D_wireframe.jpg` and `wireframes/`: hand dorsal, fingertip/nail, wrist seam, forefoot top, toes, foot seam, thumb web.
- **E** — `sheet_E_freeze_proof.jpg`: head front, profile/ear and 3/4 for v003 vs v004, plus the regional movement table.

## 6. Internal checklist (order §12)

| # | Item | Result |
|---|---|---|
| 1 | Palm/metacarpal structure coherent | **PASS.** Metacarpal fan, thenar and hypothenar read on palm and dorsal views (B1). |
| 2 | Five digit roots distinct | **PASS.** Separate roots with MCP heads (B1 dorsal, B2 MCP row). |
| 3 | Web spaces natural | **PASS.** Rounded webs between fingers, and a first web at the thumb (B2 web, B1 thumb root). |
| 4 | Finger-length hierarchy coherent | **PASS.** Middle > ring ≥ index > pinky; the thumb reaches the proximal index. |
| 5 | MCP/PIP/DIP structure readable | **PASS.** Knuckle row, joint widening and palmar creases (B2). |
| 6 | Neutral pose relaxed, not hook-like | **PASS.** Graded flexion that increases toward the pinky (B1 outer, B3). |
| 7 | Fingertips structured, not bulbous | **PASS.** Pulp pad, nail bed, tapered tip (B2 fingertip). |
| 8 | Nails visibly readable | **PASS.** Recessed fold plus plate on all five digits (B1, B2). |
| 9 | Thumb root/thenar/opposition coherent | **PASS.** CMC to thenar mass, with the thumb lying along the index (B1 thumb views). |
| 10 | Hand remains large and Grask-like | **PASS.** Wrist → tip 26.7 cm vs 26.5 cm; heavy palm. |
| 11 | Hand plausibly opens/closes/grips | **PASS.** Opened-flat and fist previews close without collapse (B3). |
| 12 | Forefoot structurally load-bearing | **PASS.** Ball and MTP row are planted; the forefoot blends smoothly into the toes (C1, C2). |
| 13 | Hallux distinct | **PASS.** Largest digit, separated, with a nail (C2). |
| 14 | Lesser-toe hierarchy coherent | **PASS.** Toes 2–5 step down in length and girth. |
| 15 | Toe roots/webs distinct | **PASS.** Separate roots with shallow webs and no cut-line crease (C2 toe roots). |
| 16 | Phalange rhythm readable | **PASS.** IP joint on the hallux, PIP/DIP on toes 2–5. |
| 17 | Plantar pads grounded | **PASS.** Toe pads flat on the ground; right sole touches exactly z = 0 (C2 ground contact, C1 sole). |
| 18 | Toenails visibly readable | **PASS.** All ten (C2 toenail). |
| 19 | Toes no longer blob-like | **PASS.** Articulated, tapered toes (C1 top/front). |
| 20 | Foot scale and stance preserved | **PASS.** Length −0.9 / +0.15 cm; heel, arch and ankle identical. |
| 21 | Body/head/eyes/ears did not regress | **PASS.** 0.000 mm on all of them (E). |
| 22 | 218 cm stature preserved | **PASS.** 218.000 cm. |
| 23 | All technical mesh gates pass | **PASS** (§4). |

**23/23 PASS.**

Notes for review:
- The left palm frame is tilted 4.5° so the relaxed hand clears the thigh.
- The rebuilt extremities are denser than the body (0.1 cm median edge). This is a source asset, so the density is intentional and production retopology will normalise it.

## 7. Stop

No production retopology, no RP2 v007, no rig, no creator morphs, no next race.

**RP2 GRASK 3D ANATOMICAL SOURCE V004 EXTREMITY RECONSTRUCTION PASS / READY FOR AUTHOR FREEZE REVIEW**
