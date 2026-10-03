# Saurin Gate 7: Surface Anatomy and Racial Identity (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/chatgpt-saurin-gate7-surface-anatomy-order.md` (c753730)
**Base:** `saurin_gate6_closed` (7c97c10), frozen. Head scale is +8 %. DESIGN / DIAGNOSTIC only: no pigmentation, sex anatomy, age, sliders, rigging, animation, clothing or UE5.

**Images** are in `reviews/images/saurin-gate7/`:

| Required item | File |
|---|---|
| 1. Whole organism: front, profile, rear, front 3/4, rear 3/4, plus mid-distance front 3/4 and rear 3/4 (Gate 6 vs Gate 7, identical cameras) | `g7_01_whole_organism.jpg` |
| 2. Head close-ups: front, profile, front 3/4, rear 3/4, eye (neutral naked baseline; Gate 6 row for comparison) | `g7_02_head.jpg` |
| 3. Display comparison: baseline plus 5 variants × front, profile, front 3/4, rear 3/4, top (identical skull, camera, lighting) | `g7_03_display_comparison.jpg` |
| 4. Scale-field map, colour-coded with a legend | `g7_04_scale_field_map.jpg` |
| 5. Tail root: rear, profile, rear 3/4, low rear 3/4, root → free tail | `g7_05_tail_root.jpg` |
| 6. Hands/feet: dorsal, palmar, palmar 3/4, fingertips/claws; foot dorsal, sole, lateral, 3/4 | `g7_06_hands_feet.jpg` |
| 7. Silhouette Gate 6 vs Gate 7 | `g7_07_silhouette.jpg` |
| 8. Change accounting | `g7_08_accounting.jpg`, `g7_accounting.json` |

**Mesh on Tyler's PC** (`RaceBodies/out/`):
- `saurin_gate7_surface_delta.npz` and `rebuild_gate7.py`: the exact full-resolution surface, 4,477,610 vertices and 8,955,216 triangles (about 0.9 mm edges). At about 200 MB the full mesh is too large to transfer directly, so it is shipped as a per-vertex offset. `rebuild_gate7.py` takes the existing `saurin_gate6_closed.npz`, upsamples it once (libigl), and adds the offset. Rebuild error is under 0.001 mm (checked).
- `SaurinGate7_Surface.blend` / `.fbx`: a preview decimated to about 1.1 M triangles. Large scales survive; the finest facial, palmar and plantar units are softened. Use the rebuild for inspection.

**Scripts:** `tools/rodin/gate1/`
- `g7reg.py`: the region/family map.
- `g7surf.py`: the scale surface.
- `g7geo.py`: claw, pad, eye and skeleton references.
- `wf_saurin_head65.py`: the display variants. `wf_saurin_head64.py` now imports it; with no `DISPLAY_VARIANT` set, the skull is the Gate 6 skull exactly.
- `g7var.sh`: the display batch.
- `ev10.py`, `ev10r.sh`, `ac10.py`, `crop7.py`, `rclose_rgb.py`, `compose10.py`, `dec10.py`.

## Method (surface only, structure untouched)

1. **Resolution.** The frozen Gate 6 mesh is upsampled once (1.12 M → 4.48 M vertices). Nothing is re-meshed, and the Gate 6 field is not touched.
2. **Region map** (`g7reg.py`). Every vertex is assigned one of seven families from anatomical position, surface normal and distance to the Gate 6 skeleton, claw and pad references:
   - protective structural;
   - transitional articulation;
   - fine expressive;
   - ventral;
   - palmar/plantar contact;
   - claw keratin;
   - eye.

   Each family carries a unit size, relief, elongation and flow direction. Family boundaries and parameters are smoothed over the surface, so unit size grades across a boundary instead of switching abruptly.
3. **Scales** (`g7surf.py`). Size-weighted anisotropic Voronoi cells give each scale a domed profile, an inter-scale groove and a slight caudal overlap tilt on structural and transitional units. Ventral units are stretched transversely.
   - The result is applied as displacement **along the normal only**, with zero mean, so no region is inflated or shrunk.
   - Claws and display keratin are left smooth.
   - Contact pads are added as local thickenings at the hand and foot pad centres from the Gate 5/6 builders.
   - A sole clamp keeps the standing ground plane and height.
4. **Eye.** A vertical slit pupil is grooved into the existing eye, and a resting nictitating-membrane fold sits at the rostral canthus. No emissive or special material.
5. **Display variants** (`wf_saurin_head65.py`). Each structure is an SDF anchored by bisection onto the skull surface and blended into it, only inside a local box. The skull field elsewhere is unchanged. Every variant is meshed, upsampled, region-mapped and scaled through the identical pipeline and rendered with identical cameras.

## Measurements

| Family | Vertices | Out max | In max | Mean | RMS |
|---|---|---|---|---|---|
| Protective structural | 2,343,653 | 0.71 mm | 0.80 mm | +0.09 mm | 0.40 mm |
| Transitional articulation | 1,311,041 | 0.48 | 0.72 | −0.09 | 0.22 |
| Fine expressive | 115,667 | 0.24 | 0.58 | −0.17 | 0.21 |
| Ventral (transverse) | 532,369 | 0.49 | 0.74 | −0.08 | 0.26 |
| Palmar/plantar contact (incl. pads) | 147,162 | 1.33 | 0.48 | −0.05 | 0.23 |
| Claw keratin | 25,983 | 0 | 0 | 0 | 0 |
| Eye | 1,735 | 0.60 | 1.10 | +0.02 | 0.23 |
| **All** | **4,477,610** | **1.33** | **1.10** | **+0.005** | **0.33** |

- **Height:** 187.89 cm (Gate 6: 187.88). The 0.1 mm difference is scale relief on the cranial roof.
- **Width:** 90.56 cm (unchanged).
- **Depth:** 161.52 cm (Gate 6: 161.48). The 0.4 mm difference is scale relief at the tail tip.
- **Silhouette pixels changed** (identical cameras): front 0.19 %, profile 0.21 %, rear 0.18 %, front 3/4 0.24 %, rear 3/4 0.21 %. All of it is a 1-pixel outline flicker from scale relief; there is no regional drift (`g7_07`).
- **What did not change:** skeleton, proportions, skull, tail path, sacral station, load paths and pelvic floor all come from the Gate 6 surface unchanged. Gate 7 adds at most 1.3 mm along the normal anywhere.

## Required answers

**1. Does the organism now read as scaled biology rather than a smooth humanoid or a humanoid in reptile texture?**
Yes at close and mid distance (`g7_01` mid views, `g7_02`, `g7_05`).
- The units change size, shape and direction with the anatomy underneath: large, slightly imbricate dorsal units on the back and tail; small domed units on the hands, feet and face; transverse ventral units. That is what separates it from a uniform texture.
- The scales follow the Gate 6 load paths and muscle forms rather than hiding them.
- **Honest limit:** at full-body distance (`g7_01` top five views) relief of ≤ 0.8 mm is below render resolution, and the body still reads mainly by silhouette. The texture read at that distance will come from material and pigment response in a later pass, which is out of scope here.

**2. Are scale fields regionally functional rather than uniformly tiled?**
Yes. `g7_04` shows the map:
- **Protective structural:** dorsal and posterolateral cranium, upper posterior neck, dorsal trunk, lateral trunk, dorsal tail, lateral forearm, shin, dorsal hands and feet.
- **Transitional articulation:** neck flexion zone, axilla and shoulder, elbow, wrist, inguinal and lower trunk, knee, ankle, tail-root band, digit joints. Transitional units are smaller and flatter.
- **Fine expressive:** lids and periorbit, rostral sides, mouth margin, jaw corner, throat.
- **Ventral:** ventral neck and trunk, and the tail underside. These are broad transverse units, not a continuous belly-scute plate.

Unit size grades across each boundary.

**3. Does the face keep the approved non-human cranial architecture?**
Yes. The skull is the frozen Gate 6 +8 % skull, unchanged (`g7_02` Gate 6 row vs Gate 7 row).
- **Surface emphasis:**
  - structural units on the roof and posterolateral cranium give the low-to-moderate vault;
  - fine units around the orbit keep the brow shelf and orbital platform crisp;
  - the rostral dorsum carries small structural units that keep the compact rostrum firm;
  - the jaw corner and quadrate region use fine expressive units, so the hinge stays legible;
  - the auricular opening stays recessed (only fine units at most, no added structure).
- No nose, lips or pinnae.
- **Eye:** vertical slit pupil and nictitating fold (`g7_02`, eye close-up).

**4. Is the naked head complete without display structures?**
Yes. The neutral baseline (`g7_03` row 1, `g7_02`) reads as a finished head: the vault, brow shelf, triangular orbital-temporal front, rostrum and hinge are all present and surfaced. It does not look like it is missing horns. The plainest remaining area is the rear cranial mass seen from straight behind, which Gate 6 already noted as a surface-richness item.

**5. Which display families are credible on the frozen skull, and where do they attach?**

| Variant | Attachment | Credibility |
|---|---|---|
| 1. Minimal cranial ridges | Temporal line / parietal margin, paired | **Weak as a display.** Credible anatomy, but at this height it barely registers against the brow shelf and roof scales. It reads as a slightly stronger skull rather than a phenotype choice. Fine as a "near-naked" option. |
| 2. Low hornlets | Postorbital corner, squamosal corner, posterior parietal | **Credible.** Small conical keratin on existing bony corners. It sharpens the triangular front and side read without competing with the face. The most "native" of the five. |
| 3. Swept-back paired | Squamosal/temporal corner, sweeping caudally past the occiput | **Credible.** It follows the head's long axis and extends the profile rearward, reinforcing the low vault. It needs the attachment on the squamosal corner; placed further forward it would read as goggles or antennae. |
| 4. Crest-dominant | Dorsal midline of the roof (frontoparietal), with low side ridges | **Credible but strongest.** A thin keratin blade on the midline. It reads clearly as display, but it is the variant most likely to read as "dragon/dinosaur" convention. Keep it lower (≤ 2.5 cm) if retained. |
| 5. Mixed / asymmetric | Posterior cranial margin (up-curving pair, left ~15 % shorter) plus unequal brow hornlets | **Credible.** The asymmetry reads as individual variation, not damage. It supports the idea that display behaves like hair: individual, not uniform. |

None of the five reshapes the skull: outside the attachment boxes, every variant's skull field is identical to the baseline.

**Recommendation for the author's decision:** 2, 3 and 5 are the strongest canon candidates. Keep 4 as a lower-height option. Treat 1 as the "near-naked" end of the range.

**6. Do the hands and feet stay functional plantigrade anatomy while reading distinctly Saurin?**
Yes (`g7_06`).
- **Dorsal surfaces:** small structural scales, with transitional units over the knuckle and digit joints.
- **Palm and sole:** fine flexible contact scales with localized thickening at the thenar, hypothenar, distal palm and digital pads, and at the heel, metatarsal band and digital pads of the foot. These are low swellings inside the scale field, not separate mammalian paw pads.
- **Claws:** smooth keratin from the terminal phalanx, unchanged in length from Gate 6, so not oversized talons.
- The plantigrade stance and ground contact are preserved by the sole clamp: height and ground plane are unchanged.
- **Honest limit:** the palmar and plantar pad relief is subtle (≤ 1.3 mm) and reads best in grazing light. It could be raised slightly if the author wants a stronger pad read.

**7. Does the tail surface reinforce the Gate 6 pelvic/caudal integration?**
Yes (`g7_05`).
- Dorsal structural units run continuously from the lumbar trunk over the sacral base into the tail; there is no seam and no separate tail texture.
- A transitional band sits over the root and caudofemoral flexion zone, so the root reads as a mobile but load-bearing junction.
- The tail underside carries the ventral transverse field, continuous with the ventral trunk.
- Scale direction follows the caudofemoral slips and the root taper, which makes the tail → sacrum → femur paths read more clearly than on the smooth Gate 6 surface.

**8. Did any Gate 6 anatomy regress?**
No.
- Displacement is ≤ 1.3 mm along the normal with near-zero mean.
- Height, width and depth are unchanged within 0.4 mm.
- Silhouette change is ≤ 0.24 % (outline flicker only).
- Skull, tail, sacral station, load paths, proportions, neutral pelvic floor and plantigrade stance are all inherited unchanged.

## Notes and open items

- **Full-body read:** scale relief is invisible at full-body distance. That is expected at real-scale relief and belongs to the material/pigment pass.
- **Display meshes are head-only renders.** They use the same pipeline and cameras as the baseline. Splicing a variant onto the full body is a mechanical step that was not needed for this comparison.
- **Map colours** are diagnostic only. They are not pigmentation proposals.

**STOP: Gate 7 diagnostic package. Awaiting author review. No pigmentation, sex anatomy, age, sliders, rigging, animation, clothing or UE5.**

— Claude
