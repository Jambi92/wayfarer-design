# RAC RM-OT-05AF — full sculpt-safe seam consolidation: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05af-full-sculpt-safe-retopology-prep-order.md` (12f97c1).
**Date:** 2026-10-16.
**Evidence:** `reviews/rac-rmot05af-evidence/`.

## Outcome

**05AF FULL SCULPT-SAFE RETOPOLOGY PREP PASS / READY FOR NEW 05AC SCULPT ORDER**

STOP. No AC1, AC2 or AC3 was performed.

## Method

- Source: `GO-05AE_sculpt_safe_baseline.blend`, sha `f1df5b33…`, verified before use.
- Ran in Blender 5.2.2 (bpy) in the cloud workspace. Nothing ran on Tyler's PC except the final file write via the device file tool.
- Tools in `tools/rac/w1/rmot05af_drivers/`:
  - `af_classify.py` — enumeration and classification;
  - `af_weld.py` — weld;
  - `ad_weld_gates.py` (05AD) — §8 gates;
  - `af_safety.py` — sculpt-safety diagnostic and dry test;
  - `af_map_sheet.py` — map.
- Only exact duplicates were collapsed, with bmesh `weld_verts`. No remesh, decimation, smoothing, projection, sculpting or moved vertices.

## §6 classification (`checks/af_classification.json`, `maps/af_duplicate_groups_classified_05AE_indices.json.gz`)

- **All remaining coincident groups:** 32,620 groups / 81,840 vertices. **Max spread 0.000 mm**: every group is an exact duplicate.
- **Region:** taken from the 05AB rig vertex groups stored in the .blend. Geometric landmarks:
  - head above 172 cm;
  - free tail + fused root from the 05AC protection mask;
  - tail junction = within 3 cm of it;
  - genital box = |x − midline| < 9 cm, in front of the pelvis centre, z 93.8–110.8 cm;
  - gluteal = trunk behind the pelvis centre and below 117 cm;
  - a 5 cm wrist/ankle buffer inside the hands and feet, so mask falloff at the wrist or ankle never meets an unwelded seam.
- **Interface test:** each group is collapsed on the position-welded mesh and the link of the merged vertex is examined.
  - **SAFE_SCULPT_SEAM:** one simple closed cycle, with member fans not opposed (min dot > −0.5). This is one continuous surface stored twice.
  - **PROTECTED_INTERFACE:** more than one cycle (distinct surfaces touching), or inside a protected landmark zone.
  - **UNKNOWN:** anything else.

| Region | SAFE | PROTECTED | UNKNOWN | z (cm) | Action |
|---|---|---|---|---|---|
| shin | 1,407 | — | — | 8.0–55.2 | **welded** |
| thigh | 921 | — | — | 54.4–96.1 | **welded** |
| pelvis / flank (incl. the 05AE groin failure seam) | 431 | — | — | 94.8–117.0 | **welded** |
| gluteal | 248 | **1** (perineal fold, see below) | — | 95.8–117.0 | **welded** (fold kept) |
| forearm | 353 | — | — | 112.5–120.2 | **welded** |
| wrist buffer (5 cm into hands) | 1,422 | — | — | 90.6–116.8 | **welded** |
| ankle buffer (5 cm into feet) | 531 | — | — | 3.5–9.7 | **welded** |
| torso / neck base / upper arm | 0 remaining (welded in 05AD/05AE) | — | — | — | — |
| hand (beyond buffer) | 6,816 | — | 29 | 90.7–112.8 | left (non-sculpt, passive) |
| foot (beyond buffer) | 4,677 | — | 4 | 0.1–7.7 | left (non-sculpt, passive) |
| head (face, muzzle, ears, eyelids, lips, nostrils) | — | 5,937 | — | 172.0–204.4 | left (protected) |
| free tail + fused root | — | 8,675 | — | 61.1–114.9 | left (protected) |
| tail junction (3 cm) | — | 106 | — | 100.4–116.6 | left (protected) |
| genital landmark box | — | 1,062 | — | 95.5–107.2 | left (protected) |

### The one sculpt-zone UNKNOWN

A 4-vertex group on the **perineal midline** at x 1.9, y −32.1, z 102.4 cm. Its link is one cycle, so the surface is continuous, but the fans are opposed (min dot −0.508), meaning a sharp fold. It was reclassified **PROTECTED_INTERFACE**, left unwelded and mapped: 05AF indices 144700–144703. **A future AC3 order should mask it.**

## Weld (`checks/af_weld_report.json`)

- 5,313 SAFE groups welded, all inside the sculpt zones and buffers.
- Vertices 549,216 → **542,522** (6,694 collapsed). Triangles 1,000,000 unchanged.
- Old→new map: `maps/old_to_new_05AE_to_05AF.npz`.
- Protected-interface map: `maps/protected_interface_map_05AE_indices.json.gz`.

## §8 gates (`checks/af_weld_gates.json`, `checks/af_safety.json`)

| Gate | Result |
|---|---|
| Old→new / new→old vertex deviation | **0.000 / 0.000 mm** |
| Triangles position-identical after remap | **yes**; max corner shift 0.000 mm |
| Stature / bounding box | 204.52246 cm; extents identical |
| Macro proportions | unchanged (no vertex moved) |
| Position-welded components / boundary / non-manifold | **1 / 0 / 0** |
| Self-intersections / flipped / degenerate faces | **0 / 0 / 0** |
| Head / hands / feet / free tail / pelvis landmarks: positional change | **0.000 mm** (0 protected vertices moved) |
| Merges inside protected interfaces / outside sculpt zones | **0 / 0** |
| Hand / foot vertices merged | 5,337, all in the 5 cm wrist/ankle buffer: duplicate-only collapse, 0.000 mm |
| Digit counts | unchanged: no face changed, no vertex moved; fingers and toes beyond the buffer untouched |

## §8–9 sculpt safety

| Diagnostic | Result |
|---|---|
| SAFE duplicate groups remaining in AC1–AC3 sculpt zones | **0** |
| Coincident pairs touching any sculpt-zone vertex (285,623 zone vertices) | **0**; the only listed exception is the perineal fold, which is excluded and mapped |
| Dry test on 05AF (in memory, never saved) | **0** pairs separated, **0** boundary edges |
| Same dry test on 05AE (control) | 5,060 pairs separated, 7,810 boundary edges |

The dry test applied 0.5× topological Laplacian plus 0.2 mm jitter to every sculpt-zone vertex. It reproduces the failure on the old baseline and shows none on 05AF.

### Topological argument

A brush moves each vertex independently. A seam can open only where two distinct vertices share a position. Inside the 05AF sculpt zones no such pair exists, so no brush, mask edge or falloff inside those zones can open a seam. Zone edges against protected regions must still be masked, as before: head ≥ 172 cm, hands and feet beyond the buffers, the genital box, the tail junction and the perineal fold.

## Frozen

- `GO-05AF_full_sculpt_safe_baseline.blend`, sha256 `6ef02c298db3cd89d93d8aafc6f2a3580f568945c869cbf7af445b51ff93edb8`. The PC copy was re-hashed and matches.
- `GO-05AF_full_sculpt_safe_baseline.glb`, sha256 `d72d93b22a3bb7a6089c119642c2976f449236197257e1067223e0b9c9b85a38`.
- Location: `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Neutral-C\05AF\`.
- Seam map: `views/af_seam_map.jpg`.

All 05AB1, 05AD and 05AE baselines and rejected AC1 attempts are unchanged.

## Notes for the next sculpt order

- Mask edges may now sit anywhere inside the green zone with soft falloff.
- Keep hard protection on: head above about 172 cm; hands and feet beyond the wrist/ankle buffers; genital box; tail junction; perineal fold (05AF 144700–144703).

## State

- No canon promotion.
- Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**.
