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

## Custom cavity rebuild under ruling 3816926 (cloud design, 2026-10-19 session 4)
Baseline = UI cage v006 (`cage_g5b`), provisional colours `cage_b4_col`, targets `tg_b4`, sim `bsim3.sh … 3` (L1–L3).
Head over-limit at L3 before: 12.2 % (L ear 19.1 %, R ear 16.9 %), head self-x 1393.

### Ears (designed sub-cages, `eardesign4.py`)
- Source study (`earslice.py`, `sl2.py`): the pinna is a lateral blade from x ≈ 15 to 19.9 (L; R mirrored about x = 2.0, tip −15.5), crescent cross-sections in x-slices, cup facing −y; the concha continues into a blind canal along +y (closed y-slice loops from y −47 to −43.3, centre ≈ (12.5, y, 198)).
- Design per ear:
  - hole = the coarse ear lump + 1 face ring (+ faces of 2 named cage verts on the L/R back head) → 26-vertex (L) / 24-vertex (R) base loop of existing cage verts;
  - transition ring T (lerp ½ base→first crescent, 2 smoothing passes);
  - 7 crescent rings = source x-slice loops at x = 15.6…19.6 (R 15.6…19.25 mirrored), resampled to the base count, cyclically aligned;
  - tip cap zipped from the horn (farthest point);
  - canal: the T–R0 faces over the canal mouth are removed (L ring indices 1–6, R 10–14); T on the mouth's inner edge at y −48; 5 canal rings = source y-slice loops at y −47 … −43.9; zip cap.
- Result `cage_ELR` (both ears): 0 coarse self-x, closed, consistently oriented.
  - L3 self-x: L ear 424 → 0, R ear 552 → 0.
  - L ear over 1.5 mm 19.1 % → 1.8 % (max 37.9 → 5.5 mm); R ear 16.9 % → 2.1 % (max 34.9 → 8.5).
  - head over 12.2 % → 4.6 %.

### Jaw / chin–neck corners (`jawrings2.py`, spec `jspec1.json`)
- The over-limit "jaw pocket" is two re-entrant corners where the narrow lower-jaw tongue (x −7…10, y −45…−62) meets the neck front (y ≈ −46), z 174–181; the cage rings there were wide ellipses enclosing the tongue and the air beside it.
- Rings z 172/175/178/181 (24 verts each, topology unchanged) re-placed on the source z-outlines (z 172, 175.3, 178, 181) with anchors at the tongue tip corners, tongue sides and the two neck corners.
- Result `cage_JS1`: 0 coarse self-x; L3 head self-x 417 → **0**; corner over-limit 37 % → 1.8–2.8 % (max 20 → 2.4 mm); head over 4.6 % → 2.0 %, head max 8.5 mm (R ear), p95 0.98.
- Rejected variants: full-ring loop cut at the throat (J1/J2, +2000 self-x in the cage lobe at the neck sides), vertex moves into the hook (M1–M3), arc-length rings without anchors (JR1–JR6, columns twist, 248–434 self-x).

### Pouch (in progress)
- Source study (y/x/z slices, renders): the inner thighs nearly meet below the crotch (min gap 0.6 cm at z 94–98); the crotch roof is the underside of the belly flap (z ≈ 99–100, y −55…−44); on both sides the groin creases are slits ≈ 0.3–0.9 cm wide running up/outward 3–5 cm from the gap's top corners (tips x −4.7 / 6.3, z 102–103) — the pockets under the flap. The cage bridges all of it with one coarse saddle (centre verts 626/471/473 at z 100).
- Thigh rings z 89/94 fitted to the source outlines (`ringfit.py`): no change in the crotch deviation (it is the roof and the slits, not the thighs).
- General-zone clusters over 3 mm at L3 (`clusters.py`): pouch front 2859 pts (max 33.8), perineum back ridge 1676 (29.1), R axilla 1217 (29.1), L axilla 569 (18.7), R back axilla 183, L arm 123, small others.
- Corrected reading of the pouch (y/z slices, renders): the inner thighs nearly meet in the crotch (gap ≥ 0.6 cm); the crotch roof is the belly-flap underside (z ≈ 99–100); the "pockets" are the two **groin creases** — narrow slits (width 0.5–0.75 cm) running from the thigh gap's top corners (z ≈ 99.5) up and laterally to the front surface (tips x −6.2 / 8.4 at z 105), depth ≤ 2.9 cm (`crease.py` z-slice spikes, `featpts.py`).
- Pelvis-front/crotch sub-cage `crotch4.py` + design `pdesign7.json` (cage `cage_P9r`):
  - hole = 12 faces (crotch saddle + 2 lowest belly-front faces + 2 back faces); boundary = ring 105.7 front (5 verts), thigh-top inner chains (5 + 5), back (5);
  - 8 rows from the belly front (z-rows 104.2/102.8/101.4) down and back through the crotch (y-rows −48.1/−46/−44.5/−40.5/−35.2); 9 columns per row: thigh lip, crease tip (thigh wall), crease tip (flap wall), flap lip, centre, mirrored; the crease columns start at the ring-105.7 crease-top vertices (fan quads), 6 side triangles;
  - thigh-top inner verts slid along the source outline to the row positions (`slidering.py`);
  - 0 coarse self-x, closed, oriented.
- Ownership colours regenerated (`recolour.py` source by connected component, `cagerecol.py` cage): trunk 1, head 2, L/R arm 4/5, L/R hand 3/12, L/R leg 10/11, L/R foot 6–8/13–15, flap underside 9. Targets `tg_r1m5` (margin 5 cm: the 2.5 cm margin left cage verts beyond the target edge, which crushed the mesh into pleats at the target boundary).
- L4 (full stack): the pouch/groin deviation clusters are gone (general over-3 mm list no longer has them; pelvis-box over 1.5 mm 4.0 %).
- Self-x mechanism found: pure subdivision of the cage has 0 self-x at every level; all L4 self-x come from the projection stack. The final-level `Project ±2 cm` step makes most of them (pleats: faces 3–10 rings apart folded onto each other). Final level Nearest-only: perineum 2086 → 104, axillae 11794 → 7521, hands 572 → 115, head 168 → 106 — at the cost of more deviation (general over 3 mm 0.66 → 1.29 %, ears over 1.5 mm ≈ 5 %). The stack mode per colour is still to be chosen.
- Axilla source (z-slices `axz2.png`): below z ≈ 141 the arm hangs free beside the trunk (contact gap); from z 142 to 154 arm and trunk are one cross-section with a **front crease** (V notch, tip ≈ (−19.5, −38), ≈ 4 cm deep, a hook at z 150–152) and a **back crease** (notch at x −19.5, y ≈ −24…−31, 1–7 cm deep at z 142, shallower above). The cage arm rings (10 verts, tilted, medial part at z ≈ 138) cross both creases with no vertices in them.

### Axillae (designed annulus sub-cages, `axrings.py` + `axdesign.py`, cage `cage_X2`)
- Region per side: the faces touching arm rings 3–8 plus two face rings outward on the trunk side (126 faces, all quads); inner boundary = arm ring 2 (10 verts, z ≈ 135–138, kept), outer boundary = 34-vertex trunk/shoulder loop (kept).
- Designed rings (18 verts each, same angular columns about the arm-root axis; columns spaced by arc length on J):
  - A3, A4 — arm surface between ring 2 and the arm lip (⅓, ⅔, projected onto the arm colour);
  - JA — arm-side lip; J — the junction ring = apex line (z ≈ 141.5, three designed points) + front crease tips (z 142.5–153, `axcrease.py` z-slice spikes) + shoulder top (7 designed points, z 155–161) + back crease tips (R: detected, z 142.5–151.5; L: the back crease is a shallow step, 6 designed points); JT — trunk-side lip (lips at least 1.2 cm from J);
  - T1 — between JT and the outer loop.
- Transitions ring 2 (10) → A3 (18) and T1 (18) → outer (34) by angle/arc-length cells (fans + triangles: 34 (R) / 72 (L) triangles). Ownership: A3–J arm colour, JT/T1 trunk.
- Result: 0 coarse self-x, closed, oriented. L4 self-x in the axillae (final level Nearest-only): R 5418 → 639, L 2103 → 203; full stack with final Project: axillae 11794 → 2242; p2s max 61 → 10 mm (the result no longer folds across the slit).

### Tail root + natal cleft (designed annulus, `tailrings.py` + `axdesign.py`, cage `cage_Y5`)
- Source: the tail hangs free below z ≈ 104.75 (its underside separate from the buttocks); from z 104.8 to 117 it joins the back with two narrow lateral creases (tips x ≈ −2 / 6.5, y ≈ −23.5…−26); the creases converge at a concave kink (2.5, −27.3, 117.1). Below the tail the natal cleft is a V notch at x = 2 whose tip runs from (−29, z 104.5) to (−36, z 100).
- Tail colour 16 added (source: the trunk component on the tail side of the junction ring; cage: tail-tube verts by nearest source colour).
- Annulus from the tail ring at y −11.5 (8 verts) to a 30-vertex body loop (crotch-patch back row, buttocks, back ring z 123); rings A3, A4 (tail), JA (tail lip), J (junction: crease tips z 105–116, kink top, bottom at the tail/cleft meeting point (2, −27.6, 104.8)), JT (body lip), T1 (bottom columns placed on the cleft: tip (2, −30, 103.4), walls y −28).
- The first version folded at L1 because the old back ring (z 117.4) lies inside the body below the junction top; the hole was grown up to the z 123 ring.
- Result: 0 coarse self-x; tail-root self-x 0 at L1–L4; back-pelvis cluster over 3 mm 1395 pts (max 24 mm) → 37 pts (max 7 mm, cleft top).

### UI import v007 (ruling 3816926 §3) — DONE
- Whole designed cage (cage_Y5 with the 1664 v006 vertices snapped to their v006 coordinates) frozen as `design_v007` (2708 V / 2755 F) and imported in the Blender UI (File > Import > Wavefront, Apply Rotation, replace Cylinder, rename) into `GO_U_REF_RP1E_retopo_v007.blend` (sha 349c7504…7d41). v005/v006 untouched.
- Verification: index-identical vertex order and faces, max deviation 0.00025 mm, closed, manifold, Euler 2, 1 component, consistent orientation, 0 coarse self-x. Record: `import_v007/PROVENANCE.md`.
- Found: one degenerate triangle in the design (L axilla verts 2596/2597 coincide) → class A; fixed in design v008a.

### Progressive gate on the UI cage v007 (stack PN, FINALN = all but head, FNSMR 0, SMR 2) — `gate_v007/`
| level | self-x | axilla | perineum | head | hands L/R | feet L/R |
|---|---|---|---|---|---|---|
| L1 | 6 | 2 | 4 | 0 | 0/0 | 0/0 |
| L2 | 49 | 38 | 4 | 0 | 0/0 | 0/7 |
| L3 | 299 | 185 | 24 | 15 | 8/9 | 0/58 |
| L4 | 1563 | 848 | 139 | 169 | 11/99 | 5/292 |
- L4 deviation (s2p median/p95/max mm, over-limit %): general 0.022/0.26/20.3, 0.38 %; head 0.028/0.45/10.6, 1.24 %; hand L 2.78 %, hand R 1.29 %; feet 1.07/0.93 %; tail root 0.00 %.
- L4 clusters (`classify.py`, `gate_v007/cls_V7PN.json`): contact-type (opposed normals, dot < −0.7, source gap ≤ 1.5 mm): R axilla front apex 369 / R apex 187 / L apex 163 / R back 45, R foot web 254, R hand bridge 92 — candidates for class B (to be measured per §6). Fold-type (dot > 0 or no source gap) = class A: ear horn roots L 70+12 / R 86, perineum crush lines 96+18, R axilla back crease (gap 12 mm) 30, flap lip 17+5, small 1–6-pair clusters.
- Not yet at the §6 checkpoint: class-A items remain. Next: repair them in design v008 (cloud), re-import.

### Design v008 (cloud, after the v007 gate) — repairs in progress
Chain: design_v007 → v008a (degenerate tri fixed: L axilla verts 2596/2597 respaced) → v008h (both axilla junction bands re-laid out, `axslit.py`) → v008m/p (groin crease extensions, `xpatch.py groinL.json groinR.json`). Each step: closed, manifold, 0 coarse self-x. Sim stack unchanged (PN, FINALN all but head, FNSMR 0, SMR 2).
- Axilla slits (`axrings2.py` + `axslit.py`): the junction band (JA/J/JT, 18 uniform columns) replaced by 30 columns sampled on the junction polyline with crease weight 3 (front) / 1.5 (back), lips carried along J by arc length (keeps lip order; the angle-interpolated lips crossed at L1), and one slit-wall ring on each side (WA/WT at half lip→tip, projected to the arm / trunk colour on the creases). Front-crease tips re-detected every 0.5 cm in z including enclosed void loops of the L slit (`deeptip.py`), smoothed ±1 sample.
  - R axilla (box x −30…−14): dev max 20.3 → 4.6 mm, points > 3 mm 406 → 37; self-x 639 → 721 (contact pairs inside the slit, gap ≤ 1.6 mm, faces crushed to ~0.1 mm).
  - L axilla: dev max 17.6 → 13.1 mm, > 3 mm 498 → 168; self-x 202 → 610. Residual: the L front slit is pinched shut at z 146–148 (source contact, enclosed void) and has a 1 cm deep spike at z 153.
- Groin crease tops (explicit patches): the creases run on 2–4 cm above the crotch sub-cage top (tips to (−7.8, −53.5, 107.1) and (10.8, −54.2, 107.7)); new tip/lip rows at x −6.4/−6.8 and 8.4/9.2 plus a crease end vertex per side. Dev max L 11.7 → 3.0 mm, R 8.5 → 3.8 mm.
- Muzzle (tried, not kept yet): midline philtrum slot + mouth line between the lip pads and the lower-lip lobe (x 0…4, z 180–183, 2 cm deep). Vertex insertions cut the > 3 mm count 245 → 77 but left 10.4 mm at the left mouth end and 115 contact pairs; needs an explicit patch (pending, priority 5).
- Stack: regional final relaxation — one Smooth modifier (factor 0.5, 3 iterations) after the final projection, restricted by vertex group `fsm_v2.txt` (axilla JA…JT bands, perineum slot rows, verts near the ear/axilla-top fold clusters). Axilla self-x L 610 → 242, R 721 → 417, perineum 110 → 6; deviation p95 +0.03 mm. (Global smoothing doubled p95 and is not used.)
- Ears (v008r–v): the front helix rim/crus was spanned by 3.5–5.8 cm faces (no cage between the x −11.6 / 15.6 crescent ring and the attach ring). `loopcut.py` adds two loops in that strip with the crest/upper/lower points of the blade placed from x-slices (`crestpts.py`); the three tragus-front knobs (≈1 cm, (13.6, −50.6, 200.9), (12.9, −49.6, 198.7), (13.2, −48.35, 197.35) and mirrored) get a vertex each (`edgeins.py`). Ear self-x 81 → 24 (folds, amplitude 0.3–0.7 mm); ear deviation p95 0.66 → 0.17 mm, max 2.3 → 2.2 mm.
- Mouth (v008u/w): the mouth line is a lateral wedge pocket between the upper-lip pads and the lower-lip lobe (x −1.3…5.3, depth ≈1.2 cm, tip (0.8, −61.1, 180.6)) plus the philtrum slot at x 2.1 (z 181.2–182.7). Vertical loop cut (2 loops) + horizontal loop at z ≈180.3, then `pathbevel.py` splits the new loop into upper lip / tip / lower lip (3 columns) and two philtrum verts. Mouth box > 3 mm 245 → 31, max 10.6 → 7.7 mm; head over-1.5 mm 1.24 → 0.69 %.
- Jaw rim loop (176.6), L elbow-tip vertex, natal-cleft tip vertex: jaw max 4.2 → 2.1 mm, elbow 5.3 → 2.7 mm, cleft 7.0 → 5.0 mm.
- Design v008/v009 frozen and imported in the UI → `GO_U_REF_RP1E_retopo_v009.blend` (verified identical, `import_v009/`). `v008.blend` received a stale OBJ copy (5 pre-fix slit-wall vertices; degenerate) and is superseded, kept unchanged.
- Degenerate slit walls found and fixed before v009: lip/wall coincidences at the R back crease (JA/WA col 5–6, JT/WT col 3) and the L back crease (WT/JT col 25–26).
- v010c (cloud): axilla trunk ring T1 rebuilt with 30 columns (`t1rebuild.py`; L placed 1 cm beyond JT); one sliver pair at the L back neck merged into a quad. L1 self-x 25 → 6 (= v007 baseline: slit-wall contacts only).
- **Checkpoint report:** `reviews/claude-rac-rp1e-custom-cavity-checkpoint.md` — v010c L4 self-x 992 (B candidates 786, A ≈ 206), T-1 general over 0.07 %, T-2 head over 0.49 %; main A block = hand/foot inter-digit clefts (bridged webs, some exposed). Not the stop line; repairs continue.

### Class-A recovery order (4e2b1a9) — session 6
- **v010c imported** through the UI → `GO_U_REF_RP1E_retopo_v010.blend` (sha 2e015133…36af): index-identical to the design (0.00025 mm), closed, manifold, Euler 2, 1 component, consistent normals, 0 coarse self-x (`import_v010/`). This is the authoritative PC cage. v009 untouched. (Blender relaunched from E:\Tools\Blender via a new Explorer tab; the original Explorer tab was left as it was.)
- Hand/foot cleft experiments (cloud only, `exp_v011/`):
  - Finger-cleft creases (`cleft.py`: P4 crossing edge + P3 neighbours, `pathbevel` lips): hand R max 13.9 → 6.3 mm, over 1.29 → 0.72–0.95 %, but self-x +95…+440 (tip folds); hand L creases made it worse (max 16 mm) — the L "cleft" A-clusters are mostly dorsal knuckle lobes missed by the 4-vertex digit tubes (P4 dorsal row ~2–4 cm inside the dorsal surface), not cleft floors.
  - P3–P4 loop cut (L hand): hand L max 12.9 → 10.3 mm, over 2.78 → 2.58 %, self-x 10 → 184.
  - Toe-cleft creases (`midcleft.py`: slit tips and walls from source z-slices): foot over 1.07 → 0.87 % (L), 0.93 → 0.67 % (R); self-x feet +680, mostly contact pairs inside 2–4 mm wide toe slits (dot −0.8…−1, amp ≤ 0.3 mm). The mandatory R cluster (−33.9, −43.3, 2.0) is a product sheet running inside the toe near the sole (crotch bottom faces), amplitude 12.9 mm — still A.
  - Conclusion so far: the frozen 4-vertex digit/toe tubes cannot carry the clefts and knuckle lobes; local creases trade bridging for tip folds. Next: re-author the hand/foot digit bases with 8-vertex rings and designed saddles (palm/digit proportions preserved).
- Design v011g (cloud): 8-vertex toe/finger tubes via longitudinal loops (`tubecut.py`); R foot mandatory cluster removed (foot R max 13.5 → 5.5 mm).

### Class-A recovery — session 6 (cont.): design v011 → `GO_U_REF_RP1E_retopo_v011.blend`
- Build (exact, `tools/rac/rp/rp1e/build_c3.sh`): v011g → `fitcage.py` local limit-surface fit (hands/head: t_fitH1 centres (40.61,-55.04,101.27),(41.94,-50.91,100.64),(27.94,-56.95,98.97),(5.82,-46.36,175.3),(12.98,-48.25,197.39) R4 L3 lam1 4 it; then t_fitH3 centres (40.66,-55.18,101.3),(5.96,-46.28,175.17),(12.96,-48.28,197.38),(7.59,-58.45,193.69),(-26.95,-48.89,97.86),(13.3,-50,200) R4 L3 lam1 5 it; HOLD = hand crotch verts) → `midcleft.py` L toe clefts 1557/1550, 1558/1563 → L axilla pinch columns 8–9 moved to the pinch mouth → front-crease J ring ownership → trunk colour 1 (L cols 5–15, R cols 15–28).
- v011: 3475 V / 3605 F, closed, genus 0, 0 coarse self-x; OBJ 1d3d378e…; UI import verified 0.00025 mm, faces identical by index; blend sha 5792e5d9…1857 (`import_v011/`).
- Gate V12c: L1/L2/L3/L4 self-x 14/82/513/1109 (axilla 553 → 162, L pinch 117 → 16, R front slit contacts removed; toe-web contacts up). L4 over-limit: general 0.09 % (max 16.1 = hidden pinch void), head 0.48 %, hand L 2.78 → 1.74 %, hand R 1.31 %, foot L 1.07 → 0.85 %, foot R 0.93 → 0.42 %.
- Diagnosis: Subdivision limit surface at L1 retracts pocket tips ~half the cage-edge depth; Nearest then snaps to the mouth. Trials not kept (`exp_v012/`): crotch splits/lifts, overshoot, exact L1-limit solve, nostril creases/pockets, third toe-cleft crease, limit surface off.
- **Report:** `reviews/claude-rac-rp1e-class-a-recovery-gate.md` — RP1E CLASS-A RECOVERY BLOCKED / AUTHOR DECISION REQUIRED (source micro-cavities + sub-cage rebuild authorisation).

### Non-local sub-cage rebuild order (a2f5ee5) — session 7
- New generator `tools/rac/rp/rp1e/toegen.py` (+ `cleftfloor.py`): removes everything distal to a clean attachment ring, then builds attach → M → M1 → O (outer loop of the digit bases) → 12-vertex digit tubes. Adjacent digits share a 5-vertex crotch path on the traced cleft floor (z-slices; fan-search floor refinement); two wall support rings at 0.35 / 0.9 cm from the floor (min 0.15 cm into the toe); free rings from slices; 4-vertex tip cap. Alternating toe colours as in the source.
- R1 L foot (attach ring K'' 1508–1521): coarse self-x 0; sim V13c: foot L L4 self-x 316 → **0**, deviation max 11.4 → 2.1 mm, over 0.85 → 0.03 %.
- R foot (same generator, frame rotated 36.9° about z): V13e foot R self-x 431 → **13**, max 5.5 → 2.0 mm, over 0.42 → 0.06 %. Total L4 self-x 1109 → 375 (design `exp_v013/design_v012a_feet.npz`, cloud only).
- Hands (in progress): `diggen.py` generalises the toe generator (oblique cleft planes spanned by adjacent finger axes and the web direction; free rings marched along the curled finger axis with oblique slices; per-digit frames for top/bottom/outer-side points). L hand trials V14a–d (attach palm ring P1, thumb kept): best V14d — index/middle web pocket 8.5 → 1.8 mm, little/ring palmar web still 8.9 mm, web-contact pairs 2359; not adopted yet.

### Non-local sub-cage rebuild — session 7 (cont.): design v012 → `GO_U_REF_RP1E_retopo_v012.blend`
- Hands rebuilt with `diggen.py` (L spec `hand_L_c_used.json`, R `hand_R_c_used.json`; finger colours 17–24, targets tg_r3m5): R web 3/4 pocket cleared; hand L over 1.74 → 0.94 %.
- L axilla z153 crevice: pocket tube (`pockgen.py`, `pocket_Lax153.json`) 12.7 → 2.0 mm.
- Muzzle (`chain.py exp_v014/chain_face.json` from `design_pC_axilla.npz`): nostril pockets L/R (8-ring tubes, rims; ring orientation now by signed area), philtrum slit band, full-width mouth-line slit band (8 cols) → nostrils and mouth corners cleared, head over 0.38 → 0.13 %, max 7.7 → 2.9 mm.
- L thumb web: slit band (6 cols, facev patch) → 6.8 mm cleared, hand L over 0.63 %.
- R thumb web is a thin fin, not a slit: fin-band trial cleared the deviation but folded at L1 (hand R self-x 506 → 6600) — not kept.
- fitcage on chin/ear: no gain, 1 coarse self-x — rejected.
- v012: 5043 V / 5170 F, 0 coarse self-x; OBJ 4d35546d…; UI import verified 0.00025 mm, faces identical; blend sha 25e9b53c…7f9c.
- Gate G12 L1/L2/L3/L4 self-x 23/121/926/1104; L4 over: general 0.07 % (16.1 deferred void), head 0.13 % (2.9), hand L 0.63 % (9.8 deferred tunnel), hand R 1.17 % (8.4 fused zone), feet 0.03/0.06 %.
- Checkpoint report `reviews/claude-rac-rp1e-nonlocal-subcage-rebuild-gate.md` (no §11 line yet; remaining list §4).

### v013 Class-A closure order — session 8: design v013 → `GO_U_REF_RP1E_retopo_v013.blend` → BLOCKED
- New tools: `refine.py` (local Catmull-Clark graded support refinement, nested), `extend.py` (digit tube extension from source sections), `rfl.py` (refinement batches), `srcgap.py`, `sxdiff.py`, `t6diag.py`, `gate_nonail.py` (rp1_gate without the nail block).
- Kept: R thumb-web 2-level support (4.9 → 2.4 mm), R fused digit C extended into the fused block (exposed gap 8.4 → 3.65 mm), refinements at chin, L thumb tip/wrist, L toe 4, R toes, L axilla 149.6, L ear, R groin ridge, R hand radial, R axilla B tip, natal (1 level).
- Rejected (two attempts each): fin band on support (L1 fold), philtrum slot band / refinement, upper-lip, ear-rim, L axilla knob, R axilla A tip, natal 2-level, L palm, R ulnar web, fused-edge refinements — all reduce deviation but multiply opposed-sheet contacts or fold at L1.
- v013: 5476 V / 5669 F, 0 coarse self-x; OBJ 181a3227…; UI import verified 0.00025 mm; blend sha 230c7b3a…d778.
- Gate G13: L1/L2/L3/L4 self-x 30/137/961/1492; L4 over: general 0.05 % (15.5 D void), head 0.05 % (2.57), hand L 0.49 % (9.8 D tunnel), hand R 0.24 % (3.65), feet 0.01/0.04 %. T-3 and T-7 pass; T-6 hip_R 6.98 mm (section includes the R hand; hip part 0.01 mm); nails not measurable in the cloud (AW4 plate masks missing). Source genus 3 vs contract genus 0.
- Report `reviews/claude-rac-rp1e-v013-class-a-closure-gate.md` — RP1E NON-LOCAL SUB-CAGE REBUILD BLOCKED / AUTHOR DECISION REQUIRED.

### v014 local-stack ruling — session 9: pilots → LOCAL PROJECTION-STACK RECOVERY FAILED
- P1 per-sheet ownership (`own.py`) + P2 local order (`sim.py` REGCOLS/REGV) on three pilots (`exp_v016_pilots/`): L axilla knob 4.39 → 1.95 mm but 150+ region pairs (pinch-mouth zero-gap contact); R thumb fin 2.41 → 0.21 mm but 794–1005 pairs (stitch fold / membrane taper); L ear rim worse (normal-sign split fails on the curl). No variant reached regional self-x 0; no v014 promoted.
- T-6: component-filtered hip_R 0.086 mm (`rp1_landmarks_comp.py`); tails existing method 1.11/1.27/1.51 (tail_12 fails), exact-clip diagnostic max 1.12.
- Nails: tooling regenerated from GO-05AW4 AW3 groups + fitted axes (8 source tips reproduced ≤0.003 mm); v013 nails −0.12…−0.71 mm (7 fail).
- D masks: exterior-visibility mask (`dmask.py`) strongly beam-width dependent; not applied. Source genus 3 handles localised (R hand B–C through-slit, L hand tunnel, L axilla void).
- Report `reviews/claude-rac-rp1e-v014-local-stack-recovery-gate.md`.
