# RAC RP2 — Grask anatomical source v003 bounded extremity refinement — final gate

- **Date:** 2026-10-23
- **Order:** `reviews/chatgpt-rac-rp2-grask-3d-source-v003-extremity-refinement-order.md` (b00ac6b)
- **Parent:** `GR_U_REF_RP2_SOURCE_3D_v002.blend` (74c6ce4)
- **Status:** **RP2 GRASK 3D ANATOMICAL SOURCE V003 EXTREMITY REFINEMENT PASS / READY FOR AUTHOR FREEZE REVIEW**

## 1. Deliverables

| Item | Location | SHA-256 |
|---|---|---|
| Source v003 | `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Grask/RP2/SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v003.blend` | `aad25f89b92480d8eca4de1290e012daf3f30988ef3be99be245b72e681acbd1` (PC readback matches) |
| GLB copy | same folder, `…_v003.glb` | `064a2f1c0ec830646532f75bef2f80995a9b5bc26a059d46ebdeff38c5b34a50` (PC readback matches) |
| Geometry hash | — | `784ff2da2581666ed19bfbd9cfdfcb8bdeabe6f71ae50a18821aebdd63ce37e9` |
| Sidecar | `…_v003.json` | `52c16852…b909` |
| Masks | `…_v003_refinement_masks.npz` | `40046f3a…2c3c` |
| Repo GLB copy | `reviews/rac-rp2-evidence/grask_3d_source_v003_extremity/source_copy/…_v003.glb.gz` | `6f066713…8b48` |
| Source v002 (parent) | unchanged | `0651765f…755a` (re-verified) |
| Source v001 | unchanged | `2315d5c1…cf86` (re-verified) |

RP2 production v001–v006 were not touched.

## 2. Scope discipline (§7 hard freeze)

Every v003 operation is restricted to hands, feet, the eye/brow window and the ears (ears: cleanup only). Each vertex is measured against the v002 surface by closest-point distance.

| Region | Vertices | Max move | p95 move | Moved > 0.1 mm |
|---|---|---|---|---|
| Hands | 76,663 | 4.22 mm | 1.06 mm | 52,724 |
| Feet | 53,487 | 3.97 mm | 1.75 mm | 38,742 |
| Eye / brow | 8,929 | 4.27 mm | 0.80 mm | 1,866 |
| Ears | 3,687 | 0.06 mm | 0.00 mm | 0 |
| **Rest of body** | 88,023 | **0.47 mm** | **0.00 mm** | 497 |

The 497 rest-of-body vertices are the blend rings at the wrist (z ≈ 111) and the subdivision boundary beside the hands (outer thigh, z ≈ 60). They are interpolated, not reshaped. Torso, pelvis, limbs, back, neck, cranium, stature and limb lengths are unchanged: see sheet A, with identical cameras.

## 3. What was done

Tools are in `tools/`; parameters are in `production/sculpt_params_v003.json` and `production/eye_params_v003.json`.

1. **Mesh-quality groundwork (hands, feet, eyes, ears only)**
   - **Poke vertices removed.** The generator mesh carried 2,513 valence-3 poke vertices, which render as dark pits and nicks. 1,351 of them in these regions were removed by merging each fan back into one triangle (max height 0.71 mm).
   - **Resolution raised.** Hands, forefoot/toes and the eye window received a conforming 1:4 subdivision, taking edges from about 3.5 mm to about 1.75 mm so joints and nail folds can exist. Midpoints use PN-triangles, falling back to linear at finger contacts.
   - **Noise removed without shrinking.** A fine-band clean was run with its own low-pass subtracted. A first version without that step shrank the digits by 25–40 % and was rejected.
   - Micro-triangle clusters were faired, and folded faces were removed.
2. **Digit anatomy (hands and feet)**
   - Each finger is segmented automatically with a geodesic merge tree (5 digits per hand), and the thumb is identified by the earliest web.
   - Toes are given axes from the forefoot outline: hallux plus 4.
   - A centreline frame per digit drives the following:
     - **Joints:** PIP/DIP joint swelling on the fingers, IP on the thumb and hallux, PIP/DIP on the lesser toes.
     - **Knuckles:** dorsal knuckle prominences on those joints, and an MCP knuckle hierarchy on the dorsal hand (middle > index > ring > pinky; σ 0.8 cm, 2.8–4.6 mm).
     - **Palm side:** soft palmar joint creases, segment pads and fingertip pads, plus thenar mass.
     - **Shafts:** dorsal shaft planes, so a joint reads wider than its shaft.
     - **Nails:** nail beds made from a flattened dorsal dome, a proximal nail fold and lateral nail grooves.
     - **Toes:** dorsal interdigital separation between the toes, and tip taper so the toes stop reading as round blobs.
   - All displacement runs along smoothed normals and is low-passed, with no tertiary skin detail.
   - **Size check (median digit radius, v002 → v003):**

     | | Thumb | Index | Middle | Ring | Pinky |
     |---|---|---|---|---|---|
     | Left hand | 0.73 → 0.72 | 1.28 → 1.25 | 1.49 → 1.48 | 1.11 → 1.09 | 0.91 → 0.89 |
     | Right hand | 0.86 → 0.86 | 1.23 → 1.17 | 1.27 → 1.28 | 1.27 → 1.29 | 1.00 → 0.96 |

     - Hand size and digit mass are preserved, within −5 % to +2 %.
     - Visible digit length measured from the web reads 0.2–0.5 cm shorter. That is the redefined web/MCP transition plus tip shaping; arm length and hand scale are unchanged.
     - Toe tips sit about 0.2 cm further back (taper). Foot length, width, heel and arch are unchanged.
3. **Eyes (§6).**
   - The profile scan of v002 showed the "eye" as a crease directly under the brow, with a flat plane below and no eyeball volume or lid seating.
   - Conclusion: generator compression.
   - A minimal correction added an eyeball volume (ellipsoid 4.0 × 2.7 × 2.5 cm), seated the lower and upper lids around it, and kept the fissure narrow (0.48 cm max opening). The tilt, stern squint, heavy brow, nose and cheek are preserved.
   - Displacement is max 4.3 mm, low-passed, and restricted to forward-facing surface below the brow guard.
   - Two earlier attempts left steps or a pinched inner canthus and were rejected.
4. **Ears (§5).** Inspected close up; only the poke-vertex cleanup was applied (≤ 0.06 mm).
   - Helix and antihelix are continuous; the conchal bowl has depth.
   - The tragus/antitragus equivalents and the lobe are present.
   - The posterior attachment and the mirrored seam are clean.
   - Darker shading on one ear is the studio light, confirmed earlier with a mirrored render.
5. **Ground.** The fine clean had lifted the right sole contact by 0.32 mm. It was restored locally to z = 0. The left foot keeps its natural 3.5 mm stance lift inherited from v002.

## 4. Technical gate (Blender readback)

| Check | v003 |
|---|---|
| Vertices / triangles | 230,789 / 461,574 (local subdivision of extremities and eyes) |
| Components | 1 |
| Boundary / non-manifold edges | 0 / 0 (watertight) |
| Euler / genus | 2 / 0 |
| Degenerate / coincident / duplicate | 0 / 0 / 0 |
| Floating fragments, cloth, duplicate shells, holes | none |
| Normals | consistent, outward (+130.53 L; v002 130.60 L) |
| Self-intersections | **0** |
| Edge (cm) | median 0.304, min 0.013, max 2.65 |
| Height | **218.000 cm** |
| Bbox (cm) | [−36.76, −20.36, 0.00] – [34.74, 27.02, 218.00] |

**Masks** (npz):
- `extremity_move_mm`
- `ext_clean_move_mm`
- `microfix_weight`
- `defold_weight`
- `eye_move_mm`
- `eye_weight`
- `ground_fix_mm`
- `dist_from_v002_mm`

Region statistics are in `production/region_movement.json`.

## 5. Self-audit (order §10)

| # | Item | Result |
|---|---|---|
| 1 | Hand size preserved | **PASS.** Radii −5…+2 %; scale unchanged. |
| 2 | Fingers no longer read tubular/melted | **PASS.** Joint swelling, dorsal planes and knuckles break the tube; nail beds read (sheet B dorsal, 3/4). |
| 3 | Knuckle hierarchy visible but not over-carved | **PASS.** MCP row middle > index > ring > pinky, with soft PIP/DIP knuckles. |
| 4 | Finger joints bend with believable phalange structure | **PASS.** Joints placed at 0.40 / 0.72 of the visible length, with palmar creases at the bends. |
| 5 | Thumb root and thenar coherent | **PASS.** Thenar mass added; thumb IP joint and nail. |
| 6 | Hands still read as Grask, not scaled human | **PASS.** Same heavy palm and long, heavy digits as v002. |
| 7 | Foot size and planted silhouette preserved | **PASS.** Sheet A and side views; heel and arch unchanged. |
| 8 | Toe hierarchy clear | **PASS.** Hallux dominant; toes 2–5 shorter and smaller. |
| 9 | Toe bases and phalange rhythm coherent | **PASS.** Dorsal interdigital separation, PIP/IP joints. |
| 10 | Nail-bed regions properly seated | **PASS.** Flattened nail plane, proximal fold and lateral grooves on all digits. |
| 11 | Toes no longer read as rounded blobs | **PASS.** Tip taper, side planes and nails (sheet C). |
| 12 | Ears remain organic and intentional | **PASS.** Preserved. |
| 13 | Eye/brow decision documented and justified | **PASS.** See the line below. |
| 14 | No accepted v002 body region regressed | **PASS.** Rest-of-body p95 0.00 mm, max 0.47 mm. |
| 15 | No global silhouette drift | **PASS** (sheet A). |
| 16 | All technical source gates pass | **PASS** (§4). |

**`EYE OPENING CORRECTED — GENERATOR COMPRESSION REMOVED`**

The eye was a crease with no eyeball volume. Eyeball volume and lid seating were restored, and the fissure was kept narrow and stern.

## 6. Evidence (`reviews/rac-rp2-evidence/grask_3d_source_v003_extremity/sheets/`)

- `sheet_A_body_regression_v002_v003.jpg`: front, profile, back, 3/4 front and 3/4 back, identical cameras.
- `sheet_B_hands_v002_v003.jpg`: palm, dorsal, 3/4, outer/ulnar, thumb root, finger side, knuckle close-up, fingertip close-up.
- `sheet_C_feet_v002_v003.jpg`: top/front, side outer, side inner, 3/4, heel, sole, toe close-up, toe 3/4, nail-bed close-up.
- `sheet_D_ears.jpg`: profile, 3/4, rear attachment, L/R comparison, with the conclusion line.
- `sheet_E_eye_brow.jpg`: face front, 3/4, profile, close front orbital, close 3/4 orbital, with the conclusion line.

## 7. Stop

No production retopology, no RP2 v007, no rig, no creator morphs, no other race.

**RP2 GRASK 3D ANATOMICAL SOURCE V003 EXTREMITY REFINEMENT PASS / READY FOR AUTHOR FREEZE REVIEW**
