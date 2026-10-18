# RAC RM-OT-05AW2 — Gorrund local-subdivision toenail rebuild: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05aw2-gorrund-local-subdivision-nail-order.md` (10fc89c)
**Source:** `GO-05AW1_T.blend` (sha `63aa8e74…7f1b`). It was revalidated and frozen as `GO-05AW2_base`.
**Executor:** Claude.
- All topology and shape edits were authored in the Blender 5.2.2 UI on Tyler's PC: Edit-mode Subdivide and Sculpt-mode Mesh Filters.
- Cloud scripts were used only for vertex groups and sculpt masks (0.000 mm geometry change), prediction, read-back, gates, evidence and the GLB export.
- Blender is closed (single instance).

## Verdict

**05AW2 HIGH-RES TOENAIL REBUILD FAILED / AUTHOR REVIEW REQUIRED**

The final closure (05AX2) must not run.

This is a near-pass, and the author can turn it into a pass.

**Technical gate: passes in full.** The final candidate (checkpoint AW2-C) has:
- 0 self-intersections, 0 opened seams, 0 degenerates, 0 folded faces;
- 1 component, 0 boundary, 0 non-manifold, genus 3 (unchanged);
- 0.000 mm change outside the nail support;
- feet, heels, ankles and ground contact preserved.

**Visual gate.** I can confirm 8 of the 11 §11 items:
- nails visibly present;
- crack/split/chip read gone;
- outline readable;
- tapered pointed distal end;
- clean free edge;
- not human-flat;
- not exaggerated;
- left and right consistent.

**Two items are not met, and one is only partly met:**
1. **"Mild projection/curve is natural": not met.** The nails are 1.7 mm raised shields lying on the toe tip. They do not project past the toe and have no downward curve.
   - Toe-tip extent vs 05AV: L −0.08 mm, R +1.29 mm.
   - In profile (`views/AW2_final_profiles_latmed.jpg`) the nails barely show.
2. **"No bump/ridge/groove read": partly not met.** From the front they read as raised plates. In 3/4 views (`views/AW2_final_34_fullres.jpg`) the side walls read as **carved outline grooves**, so the nails look inlaid rather than sitting proud.
3. **"Smooth and continuous": mostly met.** Some Stage A residue remains:
   - a horizontal shelf line across the lower L1 tip;
   - small specks and creases on L4, R2 and R3 outside the plates.

The order allows 4 checkpoints (AW2-S, A, B, C), and all four are used. I cannot add a projection or curl pass without a further order.

**Author option.** The candidate files are already frozen with hashes (§1).
- If Tyler accepts this look as is, the result becomes "05AW2 HIGH-RES TOENAIL REBUILD PASS", and 05AX2 can run on `GO-05AW2_nails_final`. No further work is needed.
- If not, a short follow-up order could allow one more checkpoint:
  - a 1.5–2.5 mm distal projection with a mild down-curl at the nail tips (masked Grab/Inflate along the toe axis);
  - softening of the side-wall groove into a raised wall.

## 1. Files (PC `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Neutral-C\05AW2\`; `checks/AW2_files_and_operations.json`)

| File | sha256 | Role |
|---|---|---|
| `GO-05AW2_base.blend` | `20153daec6e31524914ebe4b026cfc5c0f79558a56e9de5f0fc4192bb2865bda` | T + group `AW2_subd` (8 168 vertices); 0.000 mm change |
| `GO-05AW2_subdiv_base.blend` | `827d9c9ceefc4dbaf463d094605c2376266fefbcd2db637add8c1e72a5a8bd37` | **checkpoint AW2-S**: 2-cut local subdivision |
| `GO-05AW2_A_mask.blend` | `3f92ec95…` | S + Stage A mask |
| `GO-05AW2_A.blend` | `9e0490520fc752d3382092421d9f92163ceaa1d5d7dfc5f5b8bfba548c7e88d6` | **checkpoint AW2-A**: surface restoration |
| `GO-05AW2_B_mask.blend` | `ebff5b98…` | A + Stage B mask |
| `GO-05AW2_B.blend` | `b3705d7fac991e4f9e006f7009c2591c8d79a57c2a2202a7c2aa1fc9c60587b4` | **checkpoint AW2-B**: feline nail plates |
| `GO-05AW2_C_mask.blend` | `34db6dc7…` | B + fold-cleanup mask |
| `GO-05AW2_C.blend` | `e07ac7c633b7781fc624628239ea9f75a6ba1bbd6200f0388711ae6803c95b97` | **checkpoint AW2-C**: local fold cleanup |
| `GO-05AW2_nails_final.blend` | `75734a39b922f656ecc767b65c0263fa85cfde0e2e35600831b4f9830b1b9206` | **candidate** (geometry = C, mask attribute removed) |
| `GO-05AW2_nails_final.glb` | `2c7c560cf2f7d84f191309806cdbc17b5e8ea0431f9f3264a3cbc399172d1a09` | candidate GLB (27.8 MB) |

**About the candidate files.** They were frozen before the final visual review, using the order's PASS names. Under this FAIL verdict they are **candidates awaiting author decision**, not an accepted final.
- `GO-05AV_feet_final` remains the active frozen source until Tyler rules.
- `GO-05AW2_Aw.blend` is a Stage A working save, not a deliverable.

## 2. Revalidation of GO-05AW1_T (`checks/AW2_T_revalidation_gate.json`)

| Check | Result |
|---|---|
| Self-intersections / seams opened / degenerates | 0 / 0 / 0 |
| Flips | 0 |
| Welded components / boundary / non-manifold | 1 / 0 / 0 |
| Genus | 3 |
| Moved vertices vs 05AV | none (only the 05AW1 merge/dissolve removals) |

Frozen as `GO-05AW2_base`.

## 3. Local subdivision (`checks/AW2_topology_edit_log.json`, `checks/AW2S_subdivision_gate.json`, `views/AW2S_subdivision_region.jpg`)

**Region.** Vertex group `AW2_subd` = the 05AW1 nail support on all eight toes, with an enlarged big-toe support: 8 168 vertices.

**UI.** Edit Mode, select the group, Edge › Subdivide:
- Number of Cuts 2;
- Smoothness 0;
- Create N-Gons **off**;
- Quad Corner Inner Vert.

The read-back is identical to the cloud simulation (faces equal, vertex max difference 0.0).

| | Before | After |
|---|---|---|
| Vertices | 536 005 | 598 717 (**+62 712**) |
| Triangles | 999 114 | 1 124 538 |

The 05AW1 estimate was +45 244 for an 8 850-vertex support. The larger big-toe region accounts for the difference.

**Subdivision gate:**

| Check | Result |
|---|---|
| Welded components / boundary / non-manifold | 1 / 0 / 0 |
| Genus | 3 |
| Seams opened / degenerates | 0 / 0 |
| Geometry change | 0.000 mm |
| **Self-intersecting faces** | **46** |

The 46 self-intersections are existing crack-wall contacts in T's cracked nail plates that become detectable once the faces are split. **All are removed in Stage A (SI 0).**

No other topology edit was made in 05AW2. Merge-by-distance and dissolve are inherited from AW1-T.

## 4. Stage A — surface restoration (AW2-A; `views/AW2A_stageA_real.jpg`, `checks/AW2A_gate.json`)

**Mask.** Cloud-written: the support with an 11 mm margin and 5 mm ramp (24 mm on the big toes), plus repair seeds (1 mm + 2 mm ramp) around the self-intersection and fold sites.

**UI.** Mesh Filter:
1. **Smooth**: about 57 iterations.
2. **Surface Smooth**: Shape Preservation 0.0, Per Vertex Displacement 0.6, about 70 iterations.

**Result.** The cracked plates are removed and the toe tips are continuous.

| Check | Result |
|---|---|
| Self-intersections | 0 |
| Moved vertices | 46 549, max 4.54 mm, 0 outside the support |
| Lowest moved vertex | 2.62 mm above the floor |
| Folded faces vs local surface | 4, carried to C |

## 5. Stage B — feline nail plates (AW2-B; `views/AW2B_stageB_real.jpg`, `checks/AW2B_gate.json`)

**Design** (`stageB3.py`). Per nail, a shield plate placed from the toe's frontmost point along the foot axis:
- rounded root;
- convex side walls (power 2.2);
- tapered pointed tip (tip width 0.15);
- slight keel;
- height growing toward the tip;
- length 19 mm (25 mm on the big toes), half-width 0.40 × toe width.

**UI.** Mesh Filter **Inflate**, strength 0.002, one 212 px drag. Measured peak: **1.680 mm**.

Gate: SI 0, nothing outside the support; the same 4 local folds as in A.

## 6. Stage C — fold cleanup (AW2-C; `checks/AW2C_final_gate.json`)

**Mask.** 1.5 mm geodesic around the 4 folded faces (502113, 517452, 1000379, 1008749).

**UI.** Mesh Filter **Smooth**, about 20 iterations. In simulation the result was robust from 12 to 50 iterations.

## 7. Final technical gate (AW2-C = candidate)

| Check | Result |
|---|---|
| Self-intersections | 0 |
| Seams opened | 0 |
| Degenerates | 0 (min face 0.0014 mm²) |
| Welded components / boundary / non-manifold | 1 / 0 / 0 |
| Genus | 3 (unchanged) |
| **Folded / flipped faces vs the local surface** | **0** |
| Old vertices moved outside the support | 0, max 0.000 mm |
| New vertices outside the support | 0 |
| Moved vertices | 46 825, max 4.54 mm (all inside the nail supports) |
| Ankle ring drift L / R | 0.0 / 0.0 mm |
| Stature | unchanged (204.52 cm) |
| Lowest moved vertex | 2.62 mm above the floor; no ground intersection |
| Toe-to-toe contact | none new (SI 0) |
| Foot length vs 05AV | L −0.09 mm, R +1.0 mm (limit 3 mm). *Corrected 2026-10-18: the gate reports length in cm; the first version of this table misread 0.1 cm as 0.1 mm.* |
| Footprint width | 0.0 / 0.0 (limit 1 mm) |
| Heel lift / heel | 0.0 / 0.0 (limit 0.1 cm) |
| Toe-tip extent | L −0.08 mm, R +1.29 mm |

**Flip accounting.**
- 25 faces face the opposite way to their *base* face. All now agree with the smoothed local surface (dot 0.09–1.00).
- They are crack-wall faces whose base orientation was itself reversed, e.g. 505316 and its 9 subdivided pieces (base · local −0.31). The edit corrected them; it did not flip them.
- The older "inverted vs source surface" metric still lists 8 faces: 281520, plus 7 new crevice faces left untouched (now · base 1.00).
- That metric compares against the coarse source surface across the crevice. It is unreliable there, and none of these faces is folded against its own neighbourhood.

**Protected regions.** Everything outside the eight nail supports is 0.000 mm: heels, soles, ankles, legs and the whole body above the toes. See `views/AW2_final_whole_body.jpg` and `views/AW2_final_feet_front.jpg`.

## 8. Evidence (`reviews/rac-rmot05aw2-evidence/`)

**Views:**
- `views/AW2S_subdivision_region.jpg`: subdivided region in red (on the cracked T plates).
- `views/AW2A_stageA_real.jpg`, `views/AW2B_stageB_real.jpg`: Stage A and B closeups.
- `views/AW2_final_front_fullres.jpg`, `views/AW2_final_top_fullres.jpg`, `views/AW2_final_34_fullres.jpg`, `views/AW2_final_profiles_latmed.jpg`: per-nail front / top / 3-4 / lateral and medial profiles.
- `views/AW2_comparison_05AV_05AW_AW1A_AW1B_AW2.jpg`
- `views/AW2_final_feet_front.jpg`, `views/AW2_final_whole_body.jpg`

**Checks:**
- `checks/AW2_T_revalidation_gate.json`
- `checks/AW2S_subdivision_gate.json`
- `checks/AW2A_gate.json`, `checks/AW2B_gate.json`
- `checks/AW2C_final_gate.json`: includes the protected-region and foot/heel numbers.
- `checks/AW2_topology_edit_log.json`
- `checks/AW2_files_and_operations.json`

**Tools:** `tools/rac/w1/rmot05aw2_drivers/`
- `aw2gate.py`: topology-aware gate, including the new-vertex mapping and the local-surface fold metric.
- `subsim.py`, `repairseeds.py`, `stageA4.py`, `stageB3.py`, `glbexp.py`, `extrarender.py`, `aw1lib.py`

## 9. State

STOP. 05AX2 is not run.

| Item | Status |
|---|---|
| Gorrund BODY COMPOSITION | AUTHOR ACCEPTED / FROZEN |
| Head share; tail root; foot size and heel stance | AUTHOR APPROVED / FROZEN |
| Toenail morphology | **HIGH-RES REBUILD — AUTHOR REVIEW REQUIRED**. Candidate `GO-05AW2_nails_final` is technically clean; the open visual points are projection/curl and the side-wall groove read. |
| Active frozen source | `GO-05AV_feet_final` (until author ruling) |
| RM-OT-05 | OPEN |
| Stage C Gorrund blocker | BLOCKED |
| Grask E3 | FROZEN |
| Connectivity cleanup | CARRIED TO RETOPOLOGY / RIG PREP |
