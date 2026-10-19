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
