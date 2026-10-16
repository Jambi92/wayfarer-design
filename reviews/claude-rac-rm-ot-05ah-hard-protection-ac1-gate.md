# RAC RM-OT-05AH — hard-protection AC1 retry: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05ah-hard-protection-ac1-order.md` (6a49cb0).
**Date:** 2026-10-16.
**Evidence:** `reviews/rac-rmot05ah-evidence/`.

## Outcome

**05AH AC1 HARD-PROTECTION RETRY FAILED / HUMAN SCULPTOR REQUIRED**

STOP. No further autonomous AC1 loop. 05AF is untouched.

Every failure mode from 05AC–05AG is now fixed:
- seams;
- head leak;
- protected regions.

The only remaining failure is **4 flipped faces created at the edges of the hard flip-site masks themselves**.

## Method (UI only)

- Opened the 05AF baseline (sha `6ef02c29…`) with File > Open; Save As `05AF\GO-05AH_working.blend`; Sculpting workspace; front orthographic view.
- **Mask order (§3):**
  1. Box Mask on both arms below the shoulder cap and on the hips/legs;
  2. **Mask > Smooth Mask** (only these masks existed);
  3. **then** a hard head/upper-neck Box Mask;
  4. **then** three hard flip-site Box Masks;
  5. a hard central hip/tail-junction box.
- **No Smooth Mask after the hard masks.**
- **Mask verification before any stroke.** The saved working file's `.sculpt_mask` was read in the cloud workspace:
  - head (above 172 cm), tail, tail junction, genital box, hands, feet and perineal fold: **all 1.0**;
  - head hard edge at about 170.5 cm;
  - the first head box left 948 vertices at 172.0–172.5 cm open, so it was extended down a few pixels and re-checked.
- **Masked flip-site faces (§4), 05AF indices; all one-ring vertices at mask 1.0:**
  - face **643992**: one-ring 10 vertices, centre (15.75, −53.91, 146.34) cm, triangle quality 0.12;
  - face **686657**: one-ring 13 vertices, centre (12.76, −55.73, 146.47), quality 0.21;
  - face **907533**: one-ring 11 vertices, centre (−19.42, −40.28, 153.65), quality 0.08.
  - Full vertex IDs: `checks/recurring_flip_sites_masked_05AF.json`.
- **Sculpt:**
  - Smooth (0.5): abs, pec split, lower-pec shelf.
  - Flatten (0.35): pecs and deltoid fronts (front view), double passes; chest profile and deltoid cap (right view).
  - Smooth from the three-quarter view: serratus, flank, lateral abs, lower-pec edge.
  - **No trapezius strokes.**
- Saved `05AF\GO-05AH_AC1.blend` (sha256 `86f1c1f93a0d8431ce187ee61be642a8fd3518a0d3e57a98c11cc7eccf06ddf8`).

## §7 gates (`checks/ac1_gates.json`)

| Gate | Required | Result |
|---|---|---|
| Topology vs 05AF | identical | **PASS** |
| Opened seams | 0 | **PASS — 0** |
| Self-intersections | 0 | **PASS — 0** |
| Degenerate faces | 0 | **PASS — 0** |
| Components / boundary / non-manifold | 1 / 0 / 0 | **PASS — 1 / 0 / 0** |
| Head displacement | 0.000 mm | **PASS — 0.000** |
| Tail / tail junction / genital / hands / feet / perineal fold | 0.000 mm | **PASS — all 0.000** |
| Stature / bounding box | unchanged | **PASS** (204.5225 cm; extents identical) |
| Moved band | — | z 117.0–170.0 cm only; max 12.7 mm, p99 8.1 mm |
| The 3 recurring flip faces | protected | **PASS** (none flipped) |
| **Flipped faces** | **0** | **FAIL — 4 new** |
| Visual vs 05AF | clear improvement | abs and serratus largely gone, pec split softer, pec projection and deltoid cap moderately reduced, no seam creases (`views/ah_ac1_compare.jpg`) |

### The 4 new flips (`checks/new_flips_at_mask_edges.json`)

| Face | Quality | Vertex masks | Max vertex move |
|---|---|---|---|
| 441095 | 0.08 | 1 / 0 / 0 | 4.6 mm |
| 448814 | 0.80 | 1 / 0 / 1 | 4.0 mm |
| 468838 | 0.42 | 1 / 0 / 1 | 6.5 mm |
| 919029 | 0.22 | 1 / 1 / 0 | 2.5 mm |

Every one straddles the **hard edge of a flip-site box**: a pinned vertex (mask 1) next to a vertex moved several millimetres by Flatten or Smooth. They sit at x ≈ 19.5–19.9 cm (right box edge) and x ≈ −24.0 cm (left box edge). The hard protection §4 required moves the inversion risk to the box boundary.

The sculpt zone also contains **2,784 faces with quality < 0.25** (958 below 0.15). Any hard mask edge or strong stroke near such slivers can invert one.

## Interpretation for the author

- The sculpt direction now works without any seam, head or protected-region damage.
- What remains is **mesh quality**: sliver triangles in the source.
- A zero-flip guarantee for UI sculpting needs one of:
  1. a human sculptor, who can watch for and fix single-face folds as they go;
  2. an authorized local remedy for flips at mask edges — for example, a tiny Edit-mode fix of the 4 faces, or a soft (feathered) mask edge local to each flip site instead of a hard box;
  3. an authorized sliver-quality pass on the sculpt zone (edge flips / local relax with 0 macro change) before sculpting.

## Files

- `05AF\GO-05AH_working.blend` and `05AF\GO-05AH_AC1.blend`: evidence only, **not promoted**.
- 05AF baseline unchanged.

## Housekeeping

- My Blender window was closed.
- The frozen Blender window and File Explorer window from this morning are still open for Tyler to close.

## State

- Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**.
