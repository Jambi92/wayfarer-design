# RAC RM-OT-05AW1 — Gorrund toenail rework: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05aw1-gorrund-toenail-rework-order.md` (6c035cc)
**Author rejection:** `reviews/tyler-rac-rm-ot-05aw-05ax-author-rejection-and-reopen.md` (f507bf0)
**Source:** `GO-05AV_feet_final.blend` (sha `45a04787…b9a6`, verified before the prep write). The rejected 05AW files were not used.
**Executor:** Claude.
- All topology and shape changes were authored in the Blender 5.2.2 UI on Tyler's PC: Edit-mode menu operators and Sculpt-mode Mesh Filters.
- Cloud scripts were used only for vertex groups and sculpt masks (0.000 mm geometry change), prediction, read-back, gates and evidence.
- Both Blender instances are closed. A second, empty instance had been started by the launcher; it was closed too.

## Verdict

**05AW1 TOENAIL REWORK FAILED / AUTHOR REVIEW REQUIRED**

The final closure (05AX1) must not run.

**What worked: Stage A.** The cracked, split, chipped and recessed nail plates are gone on all eight nails. Each toe tip is now one continuous, smooth convex surface (`views/AW1A_src_vs_A_closeups.jpg`, `views/AW1A_front_fullres.jpg`).

**What failed: Stage B.** I could not produce a credible feline nail form within the allowed operations.
- The raised, tapered sheath I authored (checkpoint B) reads as **soft ridges or bumps on the toe tips, not as nails** (`views/AW1B_fullres.jpg`).
- It does not meet the order's visual target of "clean, continuous, naturalistic large-feline nail forms".

**Root cause: mesh resolution.**
- The toe tips carry about 1.3 mm edge spacing. A 10–14 mm nail is only about 8–10 vertices across.
- That cannot hold a defined nail outline (cuticle, side walls, free edge). Every bounded deformation I tried produced blobs, soft ridges, or V-shaped crease lines that read as grooves.
- The order allows only local repair: dissolve/retriangulate, bridge/fill, edge rotation, merge. It forbids broad retopology, and it does not allow adding resolution. So a rebuilt nail with real definition is out of scope.

**Technical status.**
- Both checkpoints are clean on seams, self-intersections, manifoldness, foot dimensions and protected regions.
- **Not fully clean:**
  - checkpoint A has **2 inverted faces**;
  - checkpoint B has **3 inverted faces**, plus **81 vertices moved by up to 0.37 mm just outside the declared support**. The Stage B mask was not clipped to the support; this is my error.
- Neither checkpoint is frozen as a nail final.

## 1. Files (PC `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Neutral-C\05AW1\`; `checks/AW1_files_and_operations.json`)

| File | sha256 | Role |
|---|---|---|
| `GO-05AW1_prep.blend` | `949d49ea…3183` | 05AV + vertex groups `AW1_weld`, `AW1_v3`, `AW1_support` (0.000 mm change) |
| `GO-05AW1_T.blend` | `63aa8e74…7f1b` | after the topology repair (UI) |
| `GO-05AW1_A_mask.blend` | `2abbfa2b…553b` | T + Stage A sculpt mask |
| **`GO-05AW1_A.blend`** | `0207bc72…5415` | **checkpoint AW1-A** (surface restoration) |
| `GO-05AW1_B_mask.blend` | `b3c72133…55b6` | A + Stage B sculpt mask |
| **`GO-05AW1_B.blend`** | `d877e426…bac4` | **checkpoint AW1-B** (feline shaping attempt) |
| `GO-05AW1_As.blend` | — | scratch file used to calibrate the filters; not a deliverable |

`GO-05AV_feet_final` remains the active frozen source.

## 2. Topology-edit log (order §7)

Both edits were made in Edit Mode on prepared vertex groups. The read-back is identical to the cloud simulation (F equal, V max difference 0.0).

1. **Merge by Distance**, 0.00001 m, on group `AW1_weld`. This group is the toe region of both feet: the foot set within 10 cm of the toe tips, with all duplicate partners.
   - Removed 6 074 vertices. These are exact duplicate-position UV-seam copies (the nearest distinct pair is 150 µm apart), so there is no position change.
   - It joins the shattered UV islands that made the old plates behave as separate pieces, including the "central split", which was partly a seam.
   - This is wider than "the visible split" alone, because without it the boundary seams pinned smoothing and recreated spikes.
2. **Dissolve Vertices** on group `AW1_v3`: 443 valence-3 vertices inside the nail support (faces split 1-to-3). These caused folds under smoothing.
   - Geometry effect: about 0.1 mm local flattening.
   - The removed vertices lie within 2.2 mm of the support.

Result: 536 005 vertices, 999 114 triangles. Welded: 1 component, 0 boundary, 0 non-manifold, genus 3 (unchanged).

## 3. Stage A — surface restoration (checkpoint AW1-A)

**Support.** A geodesic ellipse on each of the eight nails (foci at the old nail root and distal edge).
- Margin: 12 mm on lesser toes, 22 mm on big toes.
- Ramp: 6 mm.
- The mask is the inverse weight, written to `.sculpt_mask` (`views/AW1_masks_A_B.jpg`).

**UI.** Sculpt Mode, Mesh Filter:
1. **Smooth**: about 40 Laplacian iterations, fitted from read-back.
2. **Surface Smooth**: Shape Preservation 0.0, Per Vertex Displacement 0.6, about 88 iterations as 60 short drags.
   - Read-backs show the filter coalesces mouse events, so I fitted the iteration count to each read-back. The model fit error is about 0.1 mm.
   - The Surface Smooth (HC) pass removes the shrinkage ledge that plain smoothing leaves at the region edge.

**Gate** (`checks/AW1A_gate.json`, vs 05AV):

| Check | Result |
|---|---|
| Self-intersections | 0 |
| Opened seams | 0 |
| Degenerate faces | 0 |
| Welded components / boundary / non-manifold | 1 / 0 / 0 |
| Genus | 3 |
| Moved vertices | 4 607, max 6.9 mm, **0 outside the support** |
| Heels, ankle ring, everything above the feet | 0.000 mm |
| Foot length | L −0.04 mm, R 0.0 |
| Footprint width | unchanged |
| Lowest moved vertex | 4.9 mm above the floor |
| **Inverted faces vs the source surface** | **2** (faces 278606 and 490276, both at the support edge) |

Separately, 3 source faces reversed orientation. They were crack-wall faces in 05AV; one was already inverted there, and all three now face outward with the surface.

**Visual.**
- The crack, central split, chipped rim and recessed plate are gone on all eight nails, giving one continuous convex surface.
- Faint residue: a soft horizontal line where the L1 free edge used to be, and a tiny notch at the R1 tip.
- At this checkpoint the toes carry **no visible nail at all**.

## 4. Stage B — feline shaping attempt (checkpoint AW1-B)

**Design.** A tapered, slightly keeled sheath plate per nail, thicker toward the tip:
- half-width 0.36 × nail width, taper 0.7;
- 1.2× on the big toes;
- inflate height 3.0 mm at the tip.

**UI.** Mesh Filter **Inflate**, strength 0.005, one 152 px drag.
- Measured displacement: **3.007 mm** (predicted 3.0).
- Maximum difference from the prediction: 0.075 mm.

**Gate** (`checks/AW1B_gate.json`):

| Check | Result |
|---|---|
| Self-intersections / seams / degenerates | 0 / 0 / 0 |
| Welded components / boundary / non-manifold | 1 / 0 / 0 |
| Foot length / width / heels / ankle | unchanged |
| Lowest moved vertex | 2.9 mm above the floor |
| **Inverted faces** | **3** |
| **Moved outside the support** | **81 vertices, max 0.365 mm** (mask not clipped to the support) |

**Visual: FAIL.** The forms read as soft tapered ridges or bumps. On L1 the bump reads as a raised lump on top of the toe. There is no nail outline, so the toes look nail-less with odd ridges rather than clawed.

**Other Stage B designs tried in the cloud** (none authored, because none read better):
- shield inflate plus Hook taper (pinched V-lines and tip notches);
- dome sheaths (blobs);
- plateau plates (V-shaped outlines that read as grooves);
- plates re-placed from the toe geometry. At the true nail size these are only about 50–60 vertices per nail, which gives small bumps (`views/AW1_rejected_plate_placements.jpg`).

## 5. Why the bounded approach cannot pass, and options for the author

The source nails were readable only because their recessed, cracked edges gave them an outline. Removing that damage, which Stage A does, also removes the outline. Re-creating a clean outline needs either more resolution or a separate surface.

Options:
1. **Authorise a local resolution increase.** Subdivide only the nail supports, 2 cuts (8 850 support vertices, +45 244 vertices across both feet). Simulated in the cloud, the welded mesh stays 1 component, 0 boundary, 0 non-manifold, genus 3. Then sculpt the nail outline and form at about 0.4 mm spacing.
   - This needs an explicit order change, because §7 does not list subdivision.
2. **Defer the nail form to retopology / texturing.** Model nails as clean geometry, or as a normal map, on the retopologised mesh. Stage A could serve as the interim neutral, once its 2 inverted faces are repaired (≤ 2 local edge rotations, inside the support).
3. **Accept AW1-A as is**, with no visible nails, if a nail-less neutral is acceptable for now.

Checkpoint B is not recommended.

## 6. Evidence (`reviews/rac-rmot05aw1-evidence/`)

**Views:**
- `views/AW1A_src_vs_A_closeups.jpg`: 05AV vs AW1-A, front / 3-4 / top, both feet.
- `views/AW1A_front_fullres.jpg`: front views at full resolution.
- `views/AW1B_A_vs_B_closeups.jpg`, `views/AW1B_fullres.jpg`
- `views/AW1_masks_A_B.jpg`
- `views/AW1_rejected_plate_placements.jpg`

The rejected 05AW nails are shown in `reviews/rac-rmot05aw-evidence/views/BA_nails_*.jpg`.

**Checks:** `checks/AW1A_gate.json`, `checks/AW1B_gate.json`, `checks/AW1_files_and_operations.json`.

**Tools:** `tools/rac/w1/rmot05aw1_drivers/`
- `aw1gate.py`: the topology-aware gate. It maps through the merge and dissolve, and reports flips both against the source surface and against the base faces.

No whole-body sheet was made. The gates show 0.000 mm everywhere outside the toe supports, apart from the AW1-B leak noted above, which is under 0.4 mm and inside the toe region.

## 7. State

STOP. 05AX1 is not run.

| Item | Status |
|---|---|
| Gorrund BODY COMPOSITION | AUTHOR ACCEPTED / FROZEN |
| Head share; tail root; foot size and heel stance | AUTHOR APPROVED / FROZEN |
| Toenail morphology | **REWORK FAILED — AUTHOR REVIEW REQUIRED**; clean crack-free surface available as AW1-A |
| Active frozen source | `GO-05AV_feet_final` |
| RM-OT-05 | OPEN |
| Stage C Gorrund blocker | BLOCKED |
| Grask E3 | FROZEN |
| Connectivity cleanup | CARRIED TO RETOPOLOGY / RIG PREP |
