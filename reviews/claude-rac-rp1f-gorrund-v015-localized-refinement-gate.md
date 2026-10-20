# RAC RP1F — Gorrund v015 localized aesthetic refinement gate

**Date:** 2026-10-20
**Order:** `reviews/chatgpt-rac-rp1f-gorrund-v015-localized-aesthetic-refinement-order.md`
**Baseline:** RP1E v014 (`GO_U_REF_RP1E_retopo_v014.blend`). It is frozen and unchanged.
**Candidate:** `GO_U_REF_RP1F_refine_v015.blend`
**Result line:** **RP1F GORRUND LOCALIZED REFINEMENT COMPLETE / READY FOR AUTHOR VISUAL REVIEW**

## Summary

v015 is the v014 production mesh with four local author edits:
- feline claw/sheath treatment on the hand digits;
- narrower, more tapered toe claws;
- softer whisker pads;
- a rippling diagnostic, which found that no polish was needed.

The topology is identical to v014: same 1 427 072 quads, genus 1, 0 self-intersections. Only vertex positions inside the five author masks moved; nothing outside them moved. v015 is not frozen as final anatomy until Tyler approves the renders.

**Method decision (Tyler, in chat):** the first scripted attempt deformed the human nail plates directly and left crease lines and the old nail borders. Tyler chose "build proper claw geometry". The claws were therefore rebuilt as modelled claw/sheath target surfaces (§3).

## 1. Refinement D — rippling diagnostic (done first, on v014 unchanged)

**Renders:** `diagnostic/diag_0.png` (face front / three-quarter / profile / muzzle) and `diag_1.png` (R hand, L hand web, L axilla, R axilla). Each region is shown three ways:
- Workbench smooth, no cavity;
- Cycles neutral skin;
- Cycles short-fur stand-in (sheen plus fine bump).

**Result:** the directional rippling in the cavity-shaded v014 close-ups disappears under the skin and fur-like shading in every region, so no geometry was changed (§7.2). There are no D_POLISH masks.

One faint thin crease at the L hand web knuckle stays just visible. It reads as a real skin crease, so it was left alone and is flagged for the author.

## 2. Refinement C — whisker pads (`C_WHISKER_PADS`)

**Method:**
- Two ellipsoidal masks, one on each pad lobe cluster: centres (−2.7, −62.8, 183.2) and (6.8, −62.6, 183.2), radii 3.9 × 3.2 × 1.9 cm, smooth falloff. They exclude the nose, philtrum and lip line.
- The broad pad mass is a Taubin-smoothed base (80 iterations).
- The lobe detail above that base is scaled by **0.85**, a 15 % reduction.

**Effect:**
- 922 vertices moved, by at most 0.28 mm.
- Muzzle width and length, nose, lip line, philtrum and jaw are unchanged (see the bbox and stature in §5).
- The lobes stay readable but blend more into one mass (`renders/07_muzzle_close.png`). If more reduction is wanted, the same mask can go to 25 %.

## 3. Refinement A — hand claws (`A_HAND_CLAWS_L`, `A_HAND_CLAWS_R`)

The order's construction method (§8) was followed: a bounded final-resolution override, with no topology change, recorded per nail.

### 3.1 Per-digit frame

- For each of the 10 digits (5 per hand), the nail free-edge point and plate centre were ray-cast picks on the v014 surface (`design/hand_frames.json`).
- For the L little finger, L index and R little finger, the frame comes from the digit's geodesic tip.
- From these: dorsal normal n, distal axis e1, lateral axis e2.

### 3.2 Target surface (`tools/clawsdf.py`)

The target is built on a local grid, 0.18–0.24 mm voxels:

1. **Body:** the signed distance to v014.
2. **Erase the plate border:** the human nail-plate border is relaxed away by Gaussian-blurring that distance field over the plate area: 1.1 mm on the fingers, 2 mm on the thumbs.
3. **Claw:** a laterally compressed (0.7) tapering keratin cone along a quadratic Bézier centreline.
   - It starts under the dorsal skin, 4.5 mm proximal to the free edge and 1.4 mm deep.
   - It arches slightly and exits at the fingertip with a 3 mm distal extension and a 1 mm downward hook.
   - Base radius is 2.4 mm (thumbs 2.7 mm); tip radius 0.12 mm.
4. **Sheath:** a smooth union (k = 0.7 mm) of body and claw, so the sheath/lip around the claw root is the blend fillet.

### 3.3 Transfer onto the production mesh (`tools/projn.py`)

- The production vertices in a ball around the claw move along their own normals onto the target, with weight falling to 0 at the rim.
- They are then relaxed tangentially and re-projected.

### 3.4 Result

- **Moved vertices:** L 15 754, R 17 123. Max displacement 2.5 mm (L) and 2.7 mm (R).
- **Read:** a small, mostly retracted pointed claw now emerges from a soft sheath at each fingertip, and the human nail plate is largely softened away. Finger length, hand size, the R-hand slit and the L-hand web are unchanged (`renders/12_Rhand_slit_close.png`, `18_Lhand_web_close.png`).
- **Recorded dimensions:** `design/claw_dimensions.json`, which is the proposed next reference if approved.

### 3.5 Weak spots for the author

1. **R thumb (`11_Rthumb_claw_close`).** The claw sits slightly proximal to the free edge. The old plate outline is still partly visible, and local crossing relaxation smoothed it there. This is the weakest digit.
2. **L thumb (`16`).** A faint plate outline remains.
3. **Fingers.** On some, the outline of the old plate root still shows faintly at close range.

A second pass on the thumbs, or a hand sculpt pass, is recommended if these read wrong.

## 4. Refinement B — toe claws (`B_FOOT_CLAWS_L`, `B_FOOT_CLAWS_R`)

**Method** (`tools/claw.py`, frames from the AW4 nail-plate masks):
- The plate margins slide inward along the surface, by 0.35 × the plate half-width per side and strongest at the base, so the keratin base is narrower.
- A 0.3–0.4 mm dorsal keel gives a stronger taper.
- The free-edge apex extends 0.8 mm with a 35° downward curl.
- There is no added length beyond that small tip extension.

**Effect:**
- Moved vertices: L 12 754, R 21 182. Max displacement 1.85 mm (L) and 1.70 mm (R).
- Foot length and width and toe length are unchanged: bbox delta 0 and stature delta 0.
- The claws are narrower and more tapered (`renders/20`–`23`).
- The old ±0.15 mm nail-to-GO-05AW4 gate is superseded for these regions (order §10). The new values are in `design/claw_dimensions.json`.

## 5. Gate

### 5.1 Topology

| Check | Result |
|---|---|
| Faces | 1 427 072 quads (100 %), identical to v014 |
| Components | 1 |
| Boundary edges | 0 |
| Non-manifold edges | 0 |
| Euler characteristic / genus | 0 / **genus 1** |
| Degenerate faces | 0 (2 found and relaxed) |
| Directed-edge duplicates | 0 |
| **Production self-intersections** | **0** (global quad BVH) |

The local claw transfers first created crossings: 1093 pairs at the R thumb, plus 62–137 at a few toe tips. Bounded collision-free relaxation (`fixall.py`, no projection) removed them all. Two near-coincident vertex pairs at toe tips were relaxed apart; the minimum vertex separation is 0.0023 mm, the same as v014.

### 5.2 Delta control (`masks/delta_v014_to_v015.json`)

| Mask | Moved vertices | Max displacement |
|---|---|---|
| `A_HAND_CLAWS_L` | 15 754 | 2.51 mm |
| `A_HAND_CLAWS_R` | 17 123 | 2.68 mm |
| `B_FOOT_CLAWS_L` | 12 754 | 1.85 mm |
| `B_FOOT_CLAWS_R` | 21 182 | 1.70 mm |
| `C_WHISKER_PADS` | 922 | 0.28 mm |
| **Outside all masks** | **0** | — |

- Bbox delta vs v014: 0.000 mm on every axis.
- Stature delta: 0.000 mm.

### 5.3 Measurements unchanged from v014

| Item | Result |
|---|---|
| T-3 vs source | stature −0.027 mm |
| T-6 (ruled method) | max 1.122 mm (tail_00 / tail_05 reported); all others ≤ 0.79 |
| T-7 IoU | front 0.99857, profile 0.99786, rear 0.99859 |
| Silhouette | preserved |

### 5.4 Edited regions vs author intent

- The claw/sheath geometry is coherent at every digit except the R thumb (§3.5).
- The whisker-pad reduction is 15 %.
- No new contacts.
- The claws are small and mostly retracted, so they should not obstruct grip or locomotion.
- Left and right are treated identically.

## 6. Freeze and import

### 6.1 Candidate files

- `reviews/rac-rp1f-evidence/gorrund_v015/design/design_v015_production_L4.npz` (sha 4463939d…).
- The cage is unchanged: design_v014. The v015 changes are recorded final-resolution overrides.
- Claw targets per nail (`claw_targets/`), parameters (`hand_sdf.json`, `toe_claws.json`) and tools (`tools/`).

### 6.2 Blender UI import (Tyler's PC, Blender 5.2.2)

1. Opened `v014.blend` and deleted the v014 production object (in memory only).
2. File > Import > Stanford PLY with `RP1F_production_v015_part1.ply` and `part2.ply`.
3. Ctrl+J; Merge by Distance at 0.000001 m (seam duplicates only).
4. Renamed the object `RP1F_production_v015`.
5. Save As `GO_U_REF_RP1F_refine_v015.blend` (sha dfba363e…5e75).
6. Closed Blender and the Explorer window that was opened to launch it.

`v014.blend` is unchanged on disk.

### 6.3 Verification (`import/verify_v015.json`)

- Production: 1 427 072 V, bijective vertex match, faces identical, max 0.00012 mm, identity matrix.
- Cage: index-identical, 0.00024 mm.

## 7. Required visual return (`renders/`)

Every image is labelled "v014 PASSED BASELINE" | "v015 FAMILY-PILOT REFINEMENT".

| Group | Renders |
|---|---|
| Whole body | 01 front, 02 left profile, 03 rear |
| Face | 04 front, 05 three-quarter, 06 profile, 07 muzzle close |
| R hand | 08 front, 09 outside, 10 claws close, 11 thumb claw, 12 slit close |
| L hand | 13 front, 14 outside, 15 claws close, 16 thumb claw, 17 finger claw side, 18 web close |
| Feet | 19 top, 20 L claws, 21 R claws, 22 L toe claw side, 23 R toe claw oblique |

The contact sheet is `00_contact_sheet.png`. The diagnostic before/after comparison is in `diagnostic/`. No region needed polish, so there is no polish before/after.

## 8. Scope

- No RP2, rigging, creator or UE5 work.
- No propagation to other bodies.
- v014 is kept as the frozen technical-pass baseline.
