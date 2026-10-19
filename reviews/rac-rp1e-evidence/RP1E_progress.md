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

## Feet authored in the UI (2026-10-19 session 3) — `GO_U_REF_RP1E_retopo_v006.blend`
- Working file v006 (copy of v005; v005 unchanged). All shape changes made in the Blender UI by vertex click + N-panel typing.
- Order: delete faces below ring A (both feet) → extrude S1…S5, K ring by ring (alt+H, Non-Manifold select, median check, E/Esc, G Z −0.03, Hide Unselected, place each vertex; `uigen2.py` Top/Front planner) → toe tubes.
- Cap: the design's 6 cap quads are all consumed by the toes, so K gets no faces. Instead 3 split edges per foot (d2–p2, d3–p3, d4–p4, made with F on 2 verts) cut K into the 4 toe base loops.
- Toe tubes (`toes_ui.py` planner, Front ortho, sx = 598.25 + 10.6·x, sy = 427.5 − 10.6·z in cm):
  - Round 1: t1 + t3 of both feet (base loops click-selected; the implicitly selected d2–d3/p2–p3 bridge edges were deselected in edge mode before E).
  - Round 2: t2 + t4 (Non-Manifold select). Here the bridge edges d3–d4/p3–p4 were implicitly selected and got extruded with the loops, giving a 3-ring strip per side (12 stray faces).
    Fix: Non-Manifold (multiple faces) select → face mode → Delete Faces removed the strips but also the t2/t4 side walls (12 faces, all corners selected); the 4 resulting ladder holes were refilled one at a time with Grid Fill (Span 1; offset 0 for the L walls, 3 for R t2, 0 for R t4), each checked against the design.
  - Every ring checked after saving with `cktoes.py` (all new verts on target); low-clearance clicks (< 10 px) verified in the N panel before typing; tips closed with F (6-vertex tips as 2 quads, as designed).
  - Normals: Recalculate Outside over the whole mesh.
- Result (cloud check of the saved file, `cmpg5b.py`): 2096 V, 2094 quads, 0 boundary, 0 non-manifold, Euler 2, consistent orientation, positive volume.
  - Identical topology to the frozen design cage `cage_g5b` (every face matches); max vertex deviation 0.081 mm (typing precision).
  - Coarse-cage self-intersections (`selfx_npz.py`): **0** (was 2 at the R foot in v005).
- v006 sha256 after the feet: 46fc46ce8f850d5a69576f5e7b1362f3bc9d522a7a3e5bc513ad302ace15f79c.
- Next: perineum, head (jaw line / ear cups), hand residual webs and thumb crotches; then colour groups (feet as 6/7/8) + stack, progressive gates.

## Full-body diagnosis after the feet (cloud sim of the v006 cage, 2026-10-19 session 3)
Provisional colours (hand digits not separated — the hand segmentation files were lost with the old scratch space; hands = colour 3 for now):
trunk 1; limbs + head/neck (> 183.4) 2; hands 3; feet 6/7/8 (= col_foot2 3/4/5 + 3, so the feet keep Nearest + Smooth at the final level while the body gets Project ± + Nearest). Targets `targets.py … 2.5 0.7`. Sim `sim.py` now has `FINALN=6,7,8` (per-colour final mode).
- Coarse cage: 0 self-intersections.
- Self-intersections by zone (L1 / L2 / L3): axillae 42 / 262 / 2278; head 28 / 130 / 1393; perineum 0 / 0 / 27; hands (provisional colours) – / – / 273; R toes 0 / 7 / 61.
- T-1/T-2 at L3 (source→result median / p95 / max mm, share over max): general 0.065 / 0.89 / 33.8, 2.0 %; head 0.097 / 13.9 / 37.9, **12.2 %**; hands 0.6–1.6 %; feet 1.9 %; tail root 0 %.
- Where the large source→result deviations are (clusters, Blender frame; y < 0 is front):
  - **Mouth slit** at the muzzle sides (x ±6…20, y −43…−53, z 193–205): median 15–17 mm, p95 35 mm (≈ 3100 source points). The cage does not enter the mouth.
  - **Pouch** (x −9…12, y −22…−55, z 98–115): median 12.6 mm, p95 30 mm (≈ 3250 points). Mid-sagittal sections show a thin belly flap at z ≈ 99–100 overhanging a pocket; the cage bridges under the flap.
  - **Axilla front slits** (R x ≈ −19, L x ≈ 24; y −38…−44; z 142–155): median 10–12 mm. The slit is a 1–2 mm pocket that opens backwards into the armpit cavity and is sealed at the front; its top crease rises from z ≈ 141 (back) to ≈ 154 (front).
  - **Under the jaw / chin–chest** (x −7…11, y −44…−56, z 173–182): median 7–8 mm.
  - Lower muzzle front (z ≈ 182, y ≈ −62) ≈ 4 mm; nostril region (z ≈ 192, y ≈ −57) ≈ 3 mm.
- Axilla analysis:
  - Within the slit both walls carried the trunk colour (weight-based colours), so both cage sheets projected onto the same target. Wall-orientation ownership (`axcol2.py`) fixes most of it, but alone does not reduce the folds.
  - The folds are single-colour sheets folding (L2: arm–arm 126, trunk–trunk 112, arm–trunk 24) from cage faces with mixed vertex colours that straddle the crease (e.g. R faces 495, 509, 484; L 715 [2,1,2,1]).
  - Automatic relayouts (`axfit.py` min-cut, `axfit2.py` junction ring on the crease, `axfit3.py` crease path + flood colours) all made it worse (coarse 2–7, L2 401–583). The arm root is a nest of tilted 10-vertex rings (rings 9–11 near-vertical loops about the arm root, ring 11 ≈ the crease U at 1–4.6 cm, ring 12 = shoulder junction). Junction-on-crease needs explicit pocket topology, not just moves.
- Conclusion: four cavities — mouth slit, pouch, both axilla slits, and the jaw/chest contact — need explicit pocket topology in the cage (an inward-extruded invagination following each cavity, with the colour boundary at its mouth/crease) before the progressive gates can pass. The perineum itself is clean (0 self-intersections through L2), but the pouch deviation is large.

## Ear / pocket prototypes (cloud, 2026-10-19 session 3)
- The head's over-limit points (> 1.5 mm, L3) split as: L ear 1631, R ear 2014, jaw underside ≈ 1850, lower muzzle front ≈ 210, nostril ≈ 110.
- Source ear (`srcview.py`, `earsec.py`): a detailed pinna. The helix is a ≈ 1 cm thick blade rising to z 204.5 and folding forward (y −48…−54). Below it are the antihelix ridges and a concha pocket ≈ 4 cm deep, axis (−0.29, 0.94, 0.17) for L, hidden under the helix. The coarse head cage has no ear at all.
- `earpocket.py` (inset of 2 cage faces + 3 section rings + cap), L ear, `INS=0.3 SINK=0.3`, faces 1162+1013:
  - 0 coarse self-intersections;
  - L-ear over-limit share 19.1 % → 9.6 % (p95 23 → 8.6 mm);
  - the concha itself is now covered (y −48…−42: 1581 → 137 points over);
  - the rest is the uncovered helix blade (y −48…−54, median 10–21 mm).
- Generic generators failed:
  - `pocket.py` auto region: jaw pockets +35/+46 and R ear +11 coarse self-intersections, the regions being badly placed;
  - `eardesign.py` radial mug: 30, because the hole boundary is not star-shaped about the concha axis;
  - `hpatch.py` harmonic radial patch: 148, the source patch not being a disk.
  - The coarse head cage has no clean loop around the ear; the ears need hand-designed sub-cages with their own base ring and transition strip.
- Interim decision memo for the author: `reviews/claude-rac-rp1e-interim-status-and-decision-memo.md`.
