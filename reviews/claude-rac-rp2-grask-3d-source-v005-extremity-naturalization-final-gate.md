# RAC RP2 — Grask anatomical source v005 extremity naturalization — final gate

- **Date:** 2026-10-24
- **Order:** `reviews/chatgpt-rac-rp2-grask-3d-source-v005-extremity-naturalization-order.md` (6c7691d)
- **Parent:** `GR_U_REF_RP2_SOURCE_3D_v004.blend` (`ed83bf92…8000`)
- **Status:** **RP2 GRASK 3D ANATOMICAL SOURCE V005 EXTREMITY NATURALIZATION PASS / READY FOR AUTHOR FREEZE REVIEW**

## 1. Deliverables

| Item | Location | SHA-256 |
|---|---|---|
| Source v005 | `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Grask/RP2/SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v005.blend` | `7bba8d2d5f081c077351b2e79e7e5fcce91b4f376cd6b2cfc76f1c2eb052ab14` (PC readback matches) |
| GLB copy | same folder, `…_v005.glb` | `81f872e7dd2c3d8e92623273bc50d8abbcc24acd251948421c2f2916bc0cc548` (PC readback matches) |
| Geometry hash | — | `2697929d90c9ed708997a594502a4d5edeaebb8f4ae39deefcc0802dc7c1d7bc` |
| Sidecar | `…_v005.json` | `77498cdb…bfbf6` (PC readback matches) |
| Masks | `…_v005_naturalization_masks.npz` (`replaced`, `seam`, `ground_fix_mm`, `dist_from_v004_mm`) | `b5640e79…6cbd` (PC readback matches) |
| Repo GLB copy | `reviews/rac-rp2-evidence/grask_3d_source_v005_extremity_naturalization/source_copy/…_v005.glb.gz` | `da18f75e…10ff5` |
| v004 / v003 / v002 / v001 | unchanged on PC | `ed83bf92…8000` / `aad25f89…acbd1` / `0651765f…755a` / `2315d5c1…cf86` (re-verified) |

The .blend uses Blender's compression (zstd) so it fits the transfer limit; readback geometry is identical. RP2 production v001–v006 were not touched.

## 2. Method: naturalization, not reconstruction

v004's extremities are defined by a parametric anatomical model (`tools/hand_model.py`, `tools/foot_model.py`). v005 keeps every architectural parameter of that model identical:
- digit count;
- MCP, PIP and DIP joint coordinates;
- phalanx lengths;
- finger-root positions, splay and flexion;
- thumb CMC position, direction and flexion;
- toe MTP positions, lengths and flexion;
- nail locations.

Only the soft-tissue shaping terms (the `nat` parameter block) change. The extremities are then re-evaluated with exactly the v004 pipeline:
- 0.5 mm marching cubes;
- Taubin 20;
- topology-preserving decimation;
- stitched into v004 at the same wrist and MTP planes.

Everything outside the hands distal to the wrist seam and the toes/MTP row is the v004 mesh.

What changed:

1. **Joint beading removed.** In v004 every phalanx junction was a smooth union of two shafts plus a joint ellipsoid plus a dorsal knuckle. Each union added a ring of extra volume (inflation of about k/4), which is what read as "collars".
   - v005 joins phalanges with a near-continuous taper (blend 0.25 → 0.10).
   - Joint widening is now broad and axially long, set at or slightly below the shaft width (PIP 0.97, DIP 0.93; axis 1.2×).
   - The dorsal knuckle is a low, broad joint plane (bisector-oriented, slightly asymmetric) instead of a raised bump.
   - The articulation stays readable through the bend line, the joint plane and the palmar hinge creases.
2. **Finger mass and taper.** Phalanx radii were increased with an anatomical taper:
   - proximal +13 %, middle +10 %, distal +6 %, tip +4 %;
   - the tip stays broad.
3. **Non-cylindrical cross-sections.** Each proximal and middle phalanx gets a palmar pad mass, offset to the palm side. Combined with the existing dorsal flattening, the section becomes D-shaped: flat dorsal plane, lateral planes, padded palmar side. See D2 cross-sections.
4. **Soft palmar hinges.** The creases were widened and shallowed (r 0.26 → 0.28, 0.07 cm shallower, blend 0.10 → 0.16).
5. **Webs.** Finger-to-palm blending was raised from a uniform 0.8 to variable per-finger values (index 1.15, middle 1.30, ring 1.25, pinky 1.05). Roots stay distinct, and the webs read grown rather than cut.
6. **Thumb and thenar.**
   - thenar mass ×1.15 with a softer blend (1.0 → 1.3);
   - proximal thumb radii ×1.10 (distal ×1.05);
   - CMC-to-palm blend 1.1 → 1.5;
   - thumb-to-hand blend 0.45 → 0.65.
   - The opposition direction, MCP/IP positions, nail and reach are unchanged.
7. **Nails.**
   - The nail-bed flattening now ramps in over 70 % of the distal phalanx, starting at 5 %; v004 used a 15 % step starting at 25 %. This removes the ledge that made the DIP read as a band.
   - The fold is softer (groove blend 0.12 → 0.15, plate blend 0.04 → 0.06, trough lift 0.09 → 0.11).
   - The plate stays proud and visible.
8. **Toes.**
   - The same joint treatment: phalanx blend 0.2, joint width 0.94, axis 1.3×, low joint plane.
   - A plantar pad under each proximal and middle phalanx, so the toes read weight-bearing.
   - The same long nail-bed ramp.
   - Hallux size, toe hierarchy, MTP row and forefoot are unchanged. Heel, arch and ankle are v004 (untouched).
9. **Right hand tilted 2.0°** about its own axis, dorsal-ward, matching the left hand's 4.5° fix. The fuller thumb otherwise grazed the thigh (30 triangle pairs). The digit architecture is unchanged.

Exact edited regions: both hands distal to the wrist seam (hand axis u > −6 cm), and both feet distal to f = 10.5 cm (toes, MTP row, toe roots and webs).

## 3. Movement vs v004 and scale

Closest-point distance from v005 to the v004 surface (`production/region_movement.json`):

| Region | Vertices | Max | p95 |
|---|---|---|---|
| Head / face | 11,881 | 0.000 mm | 0.000 mm |
| Eyes | 9,117 | 0.000 mm | 0.000 mm |
| Ears | 3,626 | 0.000 mm | 0.000 mm |
| Torso / pelvis / back | 19,329 | 0.000 mm | 0.000 mm |
| Arms above the wrist | 23,325 | 0.351 mm (seam band) | 0.000 mm |
| Legs above the forefoot | 43,123 | 0.166 mm | 0.053 mm |
| Rest of body (all) | 119,008 | 0.351 mm | 0.000 mm |
| Hand L (naturalized) | 145,124 | 6.41 mm | 3.48 mm |
| Hand R (naturalized, +2° tilt) | 143,763 | 8.81 mm | 6.51 mm |
| Foot L (toes naturalized) | 91,566 | 2.05 mm | 0.79 mm |
| Foot R (toes naturalized) | 91,303 | 2.07 mm | 0.83 mm |

Scale (`production/dims5.json`):

| | v004 | v005 |
|---|---|---|
| Hand L, wrist → tip | 26.71 cm | 26.74 cm |
| Hand R, wrist → tip | 26.71 cm | 26.74 cm |
| Fingertip height L / R | 77.57 / 77.63 cm | 77.54 / 77.44 cm |
| Foot L, length / width | 41.43 / 18.26 cm | unchanged |
| Foot R, length / width | 42.57 / 19.07 cm | unchanged |
| Ground (right sole / left toes) | 0.000 / 0.053 cm | unchanged |

## 4. Technical gate (Blender readback)

| Check | v005 |
|---|---|
| Vertices / triangles | 590,764 / 1,181,524 |
| Bodies (components) | 1 |
| Boundary / non-manifold edges | 0 / 0 (watertight) |
| Euler / genus | 2 / 0 |
| Degenerate / coincident / duplicate | 0 / 0 / 0 |
| Floating fragments, holes, duplicate shells, visible seams | none |
| Normals | consistent, outward (+129.10 L in Blender frame) |
| Self-intersections | **0** (BVH triangle-pair test on source and readback) |
| Edge (cm) | median 0.101, min 0.007, max 2.65 |
| Height | **218.000 cm** |
| Bbox (cm) | [−35.94, −20.36, 0.00] – [35.11, 26.13, 218.00] |

## 5. Evidence (`reviews/rac-rp2-evidence/grask_3d_source_v005_extremity_naturalization/sheets/`)

All v004/v005 pairs use identical cameras.

- **A** — `sheet_A_body_v004_v005.jpg`: front, profile, back, 3/4 front, 3/4 back.
- **B1** — `sheet_B1_hands_v004_v005.jpg`: palm, dorsal, 3/4, outer, thumb root, thumb profile, index side.
- **B2** — `sheet_B2_hand_closeups_v004_v005.jpg`: middle side, MCP row, PIP/DIP, fingertip, fingernail, web.
- **B3** — `sheet_B3_hand_pose_check.jpg`: relaxed full-hand silhouette, opened-flat and fist/grip diagnostics. These re-pose the same v005 anatomy by joint angles only.
- **C1** — `sheet_C1_feet_v004_v005.jpg`: top/front, outer, inner, 3/4, heel, sole.
- **C2** — `sheet_C2_foot_closeups_v004_v005.jpg`: forefoot, hallux, hallux top, lesser toes, lesser top, toe roots/webs, toenail, ground contact.
- **D1** — `sheet_D1_shape_language_v004_v005.jpg`: PIP/DIP with no collars, finger side planes, proximal finger mass, thumb → thenar, toe joints, toe dorsal planes.
- **D2** — `sheet_D2_cross_sections_v004_v005.png`: true mesh cross-sections (v004 grey, v005 red) through the index, middle and ring proximal phalanx, PIP joint and middle phalanx, plus toe 2.
  - v005 sections are larger, with a flat dorsal plane and a fuller palmar pad.
  - Joint sections are only marginally wider than the shafts.
- **E** — `sheet_E_freeze_proof.jpg`: head front, profile/ear and 3/4 for v004 vs v005, plus the regional movement table.

## 6. Internal checklist (order §13)

| # | Item | Result |
|---|---|---|
| 1 | v004 digit architecture preserved | **PASS.** Joint coordinates, lengths, roots and flexion are identical parameters. |
| 2 | Overall hand scale preserved | **PASS.** Wrist → tip 26.74 vs 26.71 cm. |
| 3 | Fingers thick/powerful, not spindly | **PASS.** Radii +4…+13 % (B1, D1). |
| 4 | Taper anatomical, not cylindrical | **PASS.** Broad proximal, moderate middle, controlled distal taper, broad tip. |
| 5 | MCP/PIP/DIP readable | **PASS.** Bend lines, joint planes and palmar creases (B1 outer, B2). |
| 6 | No bead/collar joints | **PASS.** Junction inflation removed; joints sit inside the flesh (B2, D1). |
| 7 | Dorsal/palmar/lateral planes readable | **PASS.** D-shaped sections (D2). |
| 8 | Finger roots distinct | **PASS** (B1 dorsal, B2 MCP row). |
| 9 | Webs organic, not trench-cut | **PASS.** Variable-depth soft webs (B2 web). |
| 10 | Fingertips structured | **PASS.** Pulp pad, broad tip, nail seat (B2 fingertip). |
| 11 | Nails clearly visible | **PASS.** All five digits, in clay light. |
| 12 | Nails seated organically | **PASS.** Long nail-bed ramp, softer fold, no socket (B2 fingernail). |
| 13 | Thumb/thenar integration stronger | **PASS.** Fuller thenar, thicker proximal thumb, deeper CMC blend (B1 thumb root, D1). |
| 14 | Hand recognizably Grask | **PASS.** Large, heavy, thick-digited; not human-delicate, not a claw. |
| 15 | Hand plausibly opens/closes/grips | **PASS** (B3 open-flat and fist). |
| 16 | v004 foot architecture preserved | **PASS.** Identical toe parameters; heel and arch untouched. |
| 17 | Foot scale and stance preserved | **PASS.** Length and width unchanged. |
| 18 | Hallux dominant | **PASS** (C2). |
| 19 | Lesser toes no longer finger-like | **PASS.** Plantar pads, continuous shafts, low joint planes (C2 lesser views, D2 toe 2). |
| 20 | Toe joints readable without ring bands | **PASS** (D1 toe joints). |
| 21 | Toe roots distinct and weight-bearing | **PASS** (C2 toe roots, forefoot). |
| 22 | Toenails visible and integrated | **PASS** (C2 toenail). |
| 23 | Ground contact preserved | **PASS.** Right sole 0.000; left toes 0.053 cm (as in v004). |
| 24 | Body/head/eyes/ears unchanged | **PASS.** 0.000 mm (E). |
| 25 | 218 cm stature | **PASS.** 218.000 cm. |
| 26 | All technical gates | **PASS** (§4). |

**26/26 PASS.**

## 7. Stop

No production retopology, no RP2 v007, no rig, no creator morphs, no other race.

**RP2 GRASK 3D ANATOMICAL SOURCE V005 EXTREMITY NATURALIZATION PASS / READY FOR AUTHOR FREEZE REVIEW**
