# RP1E progress log (Claude) — design phase, cloud only (nothing authored on the PC yet)

Order: reviews/chatgpt-rac-rp1e-gorrund-contact-zone-recovery-order.md (a11c939). Working file on PC: _retopo_v004.blend (212e7508…), untouched so far.

## Method decided
- **Colour-ownership projection.** Every source vertex gets a colour so that touching parts never share a colour:
  1 trunk + tail, 2 head/neck (above neck_min z 183.4) + arms + legs, 3 palms + middle + pinky + feet,
  4 index + ring (toes 2/4 later), 5 thumbs.
  - Targets per colour = colour core + margin (geodesic < M, Euclidean > 0.7 × geodesic so nothing across a contact gap).
  - Tool: `tools/rac/rp/rp1e/targets.py`.
  - Cage vertex groups col1..col5 drive one Shrinkwrap per colour.
- **Stack per level (best so far):** Subdivision 1 → Shrinkwrap Nearest per colour → 2 × [Smooth (0.5, 2) → Nearest per colour].
  - The final level uses Project (±normal, limit 2 cm) + Nearest, with no smoothing.
  - Simulated by `sim.py` (SIMMODE=N SMR=2 FINALMODE=PN).
- **Hands rebuilt as sub-cages.** Design scripts: `handseg.py` → `digitcl.py` → `handdesign.py` → `buildcage.py`.
  - Palm rings W0 (existing 10-ring) → P1 → P2 → P3 → P4, with P4 capped by 4 quads (index…pinky).
  - Thumb extruded from the palmar radial quad P2–P3, which faces down under the thenar.
  - Digit tubes: 4-vertex rings fitted to source sections (`secring`); width k 0.85, thickness 0.6; tip ring added.
  - P4 web vertices sit at the measured cleft tops (`webprof.py`).
  - Parameters: `reviews/rac-rp1e-evidence/pR.json`, `pL.json`.
- **Bug found:** the extruded thumb base face had been left in place. It is now removed; this alone removed the thumb-crotch folds.

## Numbers (cloud simulation, cage e21 + hand targets)
| Measure | RP1 v001 | RP1E now |
|---|---|---|
| hand_R T-2 over-max share | 18.5 % | 0.02 % (max 1.78 mm) |
| hand_L T-2 over-max share | 14 % | 0.56 % |
| hand_R L4 self-intersections | ~54 k | ~550 |
| hand_L L4 self-intersections | ~46 k | ~270 |

Remaining hand folds: R middle/ring fused tips (repair zone), thumb crotches, finger webs.

## Source features that make 0 self-intersections hard (measured)
- R middle/ring distal phalanges are fused (contact handle). Separating them leaves about 1.2–1.8 mm at the bridge.
- The armpit front slit (arm pressed to chest) is about 1–2 mm wide and rises to z ≈ 154 (L) and 152–159 (R).
  - The armpit dome is at z ≈ 140–142.
  - The cage shoulder junction ring medial arc was at z 149–152, inside the trunk; this is the cause of the RP1 axilla folds.
- The finger webs are narrow slits; the dorsal index–middle cleft top is at z ≈ 102.

## Axilla work in progress
`zonefit.py` places the medial junction vertices on the arm/trunk label boundary and the other vertices 0.6 cm inside their own colour core.
- Coarse-cage axilla intersections: 32 → 3.
- L1 general self-intersections: 205 → 71.

## Next
1. Finish the axillae.
2. Perineum.
3. Head: jaw line and ear cups.
4. Feet: toe segmentation and clefts.
5. Hands: residual webs and crotch.
6. UI build.

## UI build log (Blender UI on the author PC, working file `GO_U_REF_RP1E_retopo_v005.blend`)
- 2026-10-19: R hand sub-cage authored in the UI (manual vertex typing, no scripts in Blender):
  - Wrist W0 → P1–P4 palm rings (10 verts each), P4 grid-fill cap (4 quads).
  - Index (6 rings), middle (8), ring (8), pinky (6) tubes extruded from the cap quads; thumb (5 rings) extruded from the palmar radial P2–P3 quad.
  - Each ring checked against the design median in the N panel.
  - One defect found and fixed: the index cap face survived its extrusion (non-manifold) and the index tip was open; the cap face was deleted and the tip filled.
- Cloud check of the saved file (`blendcage.py`): 1858 verts, 1856 quads, 0 boundary, 0 non-manifold, 1 component, genus 0, no duplicate faces.
- R hand UI vertices vs design cage e21: max 0.08 mm, mean 0.04 mm (176 verts).
- UI method: per-ring Hide Unselected in Top ortho; vertices clicked at known screen positions and typed in the N panel (`tubes_ui.py`, `pb.py`).
- Next: L hand (same method), then axillae, perineum, head, feet.
- 2026-10-19: L hand sub-cage authored in the UI with the same method:
  - Wrist W0 → P1–P4 palm rings, P4 grid-fill cap.
  - Index (7 rings), middle (7), ring (7), pinky (6) and thumb (5) tubes.
  - Every ring median matched the design in the N panel.
  - Same first-tube defect as R (surviving index cap face, open tip). Fixed the same way.
  - Normals recalculated outside.
- Cloud check of the saved file: 1894 verts, 1892 quads, 0 boundary, 0 non-manifold, 1 component, genus 0. Edge orientation is consistent and the volume is positive.
- L hand UI vertices vs design: max 0.09 mm, mean 0.04 mm (168 verts).
- Coarse-cage self-intersections (`selfx.py`, BVH face pairs with no shared vertex): 34.
  - Both hands: 0.
  - The rest are in the L and R axillae (z 137–150) plus 2 at the R foot (z ≈ 2).
- Next: axillae (UI moves from the zonefit design), R foot, then perineum, head, feet.
- 2026-10-19: Axillae (L and R) authored in the UI.
  - Moved 136 cage vertices (69 L, 67 R) to the `cage_e30` axilla re-layout (zonefit design). The indices are identical in both cages; `axilla_ui_moves_e30.json` lists them.
  - UI method:
    1. Box-select the axilla region in a calibrated Front ortho view and use Hide Unselected. The calibration uses the 3D-cursor positions plus Center View to Cursor. The visible set is confirmed exactly by the N-panel median.
    2. Click each vertex in a calibrated Right, Top or Front view, ordered greedily by screen clearance (≥14 px, or checked in the N panel when below that), and type its coordinates (`movegen.py`).
    3. Save after each batch of about 16, stage it, and check with `chk.py`: every changed vertex must equal its design target and nothing else may move.
  - Result: all 136 vertices on target. Max deviation from the design cage is 0.05 mm, from 0.1 mm typing precision.
  - Cage: 1894 V, 1892 quads, 0 boundary, 0 non-manifold, genus 0.
  - Coarse-cage self-intersections: 34 → 2. The 2 left are at the R foot (z ≈ 2, toe region), deferred to the feet/toe work.
- Next: feet/toes (also fixes the 2 R-foot pairs), perineum, head (jaw / ear cups), then the progressive projection gates.

## Feet design (cloud, 2026-10-19 session 2) — design frozen as `g5b`, UI authoring next
- Source toes: segmentation by a radial sweep about the ankle centroid (`footseg.py`) finds **4 free toe digits per foot**.
  The fifth toe is fused into the lateral forefoot in the frozen source (no separate digit; 05AW already noted no separate fifth-toe nail plate). The cage follows the source; it does not add a fifth toe.
  - Measured toe-to-toe gaps: min 0.8–3.6 mm. The source feet have 0 self-intersections.
- Topology per foot (`footdesign.py` → `buildfoot.py`):
  - The existing 14-vertex lower-shin ring A (z ≈ 14; L 266…475 step 15, R 56…265) is kept. Everything below it is replaced.
  - A is followed by 5 sections S1–S5. Each is a plane through a dorsal profile point and a heel/sole profile point at the same arc fraction, so the leg tube bends forward into the foot and the back half of each ring sweeps round the heel onto the sole. Vertices are placed by angular transport from A to the cap.
  - Cap ring K has 7 dorsal and 7 plantar vertices on toe-column boundaries, in a radial frame about the ankle centroid, with webs at the measured toe roots. It is filled with 6 cap quads.
  - Toe tubes: hallux and toe 4 use 2 quads (6-vertex rings); toes 2 and 3 use 1 quad (4-vertex rings). The rings are parallel, fitted to source sections, with width factor 0.95 and thickness 0.85 of the measured half-extents, plus a tip ring.
  - A small cloud untangle (`separate.py`, ≤1.2 cm) leaves 0 coarse-cage self-intersections.
- Projection stack, simulated (`sim.py`): Subdivision → Nearest per colour → 2 × [Smooth → Nearest] at every level, **including the last** (final Project ± made the feet worse: 556 vs 154 at L3).
  - Feet colours: forefoot/sole 3; hallux and toe 3 → 5; toes 2 and 4 → 4.
  - Hand colours 3/4/5 must therefore become separate foot groups (6/7/8) in the UI, or the final level must be Nearest-only for everyone.
- Results, feet only (old RP1 / first design f3 / current g5b):
  - Coarse-cage self-intersections: 2 / 0 / 0.
  - L2 self-intersections: — / 944 / 5.
  - L3: — / 9 746 / 61.
  - L4: 358 (L 14, R 344). All are in the narrow plantar web clefts (hallux/2nd mainly, R).
  - L4 deviation, foot zones: median 0.02 mm, p95 0.17–0.20 mm, over-max share 0.8–1.0 % (RP1: 45–55 %). The maxima (9–13 mm) are nail spikes and deep inter-toe cleft walls.
