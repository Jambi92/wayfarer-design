# Saurin Gate 7: Closure Verification

**Author:** Claude
**Responds to:** `reviews/chatgpt-saurin-gate7-closure-order.md` (1820a5d)
**Base:** the Gate 7 diagnostic (d5f903d) on the frozen `saurin_gate6_closed`. Closure pass only. DESIGN / DIAGNOSTIC, no UE5.

**Images** are in `reviews/images/saurin-gate7-closure/`:

| Required item | File |
|---|---|
| 1. Whole organism: front, profile, rear, front 3/4, rear 3/4 (Gate 6 / Gate 7 diagnostic / closure, identical cameras) | `c7_01_whole_organism.jpg` |
| 2. Head: front, profile, front 3/4, rear 3/4 (diagnostic vs closure) | `c7_02_head.jpg` |
| 3. Scale-transition close-ups: trunk → ventral, shoulder/axilla, lower trunk/inguinal, posterior neck → cranium, forearm/wrist → hand, shin/ankle → foot, sacral base → tail root | `c7_03_transitions.jpg` |
| 4. Hands/feet contact surfaces (diagnostic vs closure) | `c7_04_hands_feet.jpg` |
| 5. Display families with the accepted disposition | `c7_05_display_families.jpg` |
| 6. Diagnostic vs closure change accounting | `c7_06_accounting.jpg`, `c7_accounting.json` |
| 7. Silhouette vs frozen Gate 6 | `c7_07_silhouette.jpg` |

**Mesh on Tyler's PC** (`RaceBodies/out/`):
- `saurin_gate7_closed_delta.npz` with `rebuild_gate7.py`: the exact full-resolution closure surface (4,477,610 vertices, 8,955,216 triangles). The script rebuilds it from `saurin_gate6_closed.npz`; error is under 0.001 mm (checked).
- `SaurinGate7_Closed.blend` / `.fbx`: a preview decimated to 1.12 M triangles; the finest scales are softened.

**Scripts:** `tools/rodin/gate1/`
- `g7regc.py`, `g7surfc.py`, `seedpd.py`: the closure region map and surface. The diagnostic `g7reg.py` / `g7surf.py` are kept unchanged.
- `wf_saurin_head65.py`: adds `CREST_H`. The previous version is kept as `wf_saurin_head65_diag.py`.
- `g7varc.sh`, `crop8.py`, `ev11r.sh`, `ev11.py`, `ac11.py`, `compose11.py`, `dec11.py`.

## What changed (surface only)

1. **Graded transitions.**
   - **Blending:** scale spacing, relief, elongation, plate-ness and imbrication now blend over about 2 cm on the body and about 1 cm on the head, hands and feet. Before, the blend was about 0.7 cm everywhere. The smaller distance on head, hands and feet keeps small structures distinct.
   - **Seeding:** seeds are now placed by variable-radius Poisson-disk sampling along the graded size field. The old per-size-bin grid created density steps and duplicate seeds along size iso-lines; those are gone.
   - **Measured:** the 99.9th-percentile change in scale spacing per cm of surface fell from 0.85 to 0.34 (−60 %). For relief it fell from 0.074 to 0.030 mm/cm (−60 %).
   - The families are unchanged: same assignment, same vertex counts.
2. **Facial hierarchy.**
   - **Fine expressive units** (lids, mouth margin, jaw corner, rostral sides) are smaller and about 40 % lower in relief.
   - **Cranial roof, posterolateral and rostral-dorsum units** are now planar plates: flatter crowns, less imbrication tilt and slightly larger units on the roof, so they reinforce the low vault instead of rounding it. The rostrum carries low plates rather than pebbling.
   - **Plane edges:** scale relief is reduced wherever the skull bends sharply (brow shelf, orbital rim, jugal, quadrate/hinge), down to 35 % at the sharpest edges, so the cranial planes read before the microstructure.
   - **Tympanic area:** the auricular area is a smooth recess 0.7 mm deep with no rim and almost no scale relief, so it cannot read as a pinna.
3. **Contact anatomy.** Pad thickening is raised slightly (pad relief 1.6 → 2.1 mm). It is still a low swelling inside the fine contact scale field, at the same load areas. The sole ground clamp is kept.
4. **Crest.** The crest blade is lowered to **2.43 cm** above the cranial roof (diagnostic: 3.27 cm). All other display structures are unchanged.
5. **Unchanged:** the Gate 6 geometry underneath, the eye (slit pupil and nictitating fold; 0.0 mm change), the claws (0.0 mm), every family's location, and the displacement-only, zero-mean method.

## Accounting

| Family | Closure relief out / in / mean / RMS vs Gate 6 (mm) | Moved vs diagnostic, median / 99th pct (mm) |
|---|---|---|
| Protective structural | 0.67 / 1.04 / +0.10 / 0.38 | 0.19 / 1.33 |
| Transitional articulation | 0.53 / 0.78 / −0.09 / 0.22 | 0.11 / 0.68 |
| Fine expressive | 0.07 / 0.69 / −0.28 / 0.29 | 0.15 / 0.35 |
| Ventral | 0.44 / 0.77 / −0.07 / 0.25 | 0.15 / 0.78 |
| Palmar/plantar contact | 1.76 / 0.54 / −0.04 / 0.29 | 0.04 / 0.38 |
| Claw keratin | 0 | 0 |
| Eye | 0.60 / 1.10 / +0.02 / 0.23 | 0 |
| **All** | **1.76 / 1.10 / +0.007 / 0.32** | **0.15 / 1.26** |

- **Height:** 187.86 cm (Gate 6: 187.88; diagnostic: 187.89). The −0.2 mm is the flatter roof plates at the apex.
- **Width:** 90.56 cm (unchanged).
- **Depth:** 161.51 cm (Gate 6: 161.48).
- **Silhouette change vs Gate 6:** front 0.19 %, profile 0.21 %, rear 0.18 %, front 3/4 0.23 %, rear 3/4 0.19 %. This is a one-pixel outline flicker from scale relief, the same as the diagnostic.
- **Honest note:** the fine expressive field now sits on average 0.28 mm below the Gate 6 surface (diagnostic: 0.17 mm). This comes from the lower, recessed-groove facial units plus the tympanic recess. It is a sub-millimetre surface effect, not a reshaping of the face.

## Required answers

- **Are all Gate 6 structures still unchanged?** **Yes.** Both Gate 7 versions sit on the identical Gate 6 surface: same skeleton, skull, tail path, root taper, sacral station, load paths, pelvic floor and stance. The closure moves the surface by at most 1.76 mm along the normal (pads), and 0.32 mm RMS.
- **Are scale-family boundaries now graded without erasing regional function?** **Yes.** Measured size and relief gradients at boundaries fell by about 60 % (elongation and orientation are blended the same way but not separately measured), and the seed grid's density steps are gone. In `c7_03`, all seven listed zones now change scale size over several units instead of at a line. Away from the boundaries the families keep their diagnostic sizes: large dorsal and tail units, small hand and face units, transverse ventral units.
- **Do cranial planes read before the scale microstructure?** **Yes.** In `c7_02` the brow shelf, orbital platform, rostral planes, jugal/quadrate transition and hinge are crisper in the closure row. The roof reads as low plates, the face as a finer and subtler field, and the rostrum stays planar. The tympanic area is a smooth recess with no rim.
- **Do palms and soles read as functional reptilian contact anatomy without mammalian paw pads?** **Yes.** The thickening is slightly stronger at real load areas, sits inside the fine contact scales, and grades from dorsal to joint to contact (`c7_04`). There are no separate pads, and claws and digits are unchanged. It remains subtle; it reads best in grazing light.
- **Is tail-root continuity preserved?** **Yes.** The root geometry, caudofemoral slips and tail curve are untouched. The transitional band now blends into the sacral and free-tail fields, so the read is trunk → sacral base → mobile load-bearing root → free tail, with no seam (`c7_03` last column; `c7_01`).
- **Are all five display states viable under the disposition?** **Yes** (`c7_05`, identical skull and cameras, closure surface on every head):

  | Display state | Disposition | Attachment |
  |---|---|---|
  | Naked baseline | Canonical and complete | — |
  | Minimal ridges | Near-naked / minimal end | Temporal line / parietal margin |
  | Low hornlets | Accepted, primary | Postorbital, squamosal corner, posterior parietal |
  | Swept-back paired | Accepted, primary | Squamosal / temporal corner |
  | Mixed / asymmetric | Accepted, primary | Posterior cranial margin plus brow |
  | Crest | Retained at low profile, 2.43 cm (≤ 2.5 cm reference) | Dorsal midline |

  None reshapes the skull, and none is required for a complete head. Cranial keratin/display anatomy is recorded as the Saurin hair-analogue customization category. No slider architecture has been built.
- **Did any broad silhouette or body proportion change?** **No.** The outline differs from Gate 6 by at most 0.23 % (relief flicker only), and height, width and depth are within 0.3 mm.

## GATE 7 CLOSED

Stopped. No pigmentation/patterning, sex-related anatomy, age variation, creator sliders, rigging, animation, clothing or UE5 until the author reviews this closure package.

— Claude
