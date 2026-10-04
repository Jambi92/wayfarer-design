# Saurin Post-Gate-8 Anatomical Polish (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/chatgpt-saurin-post-gate8-anatomical-polish-order.md` (36c442c)
**Base:** frozen Gate 6 anatomy (`saurin_gate6_closed`), Gate 7 closure surface (a6a5fb9) and the Gate 8 model (dfaba91).
**Scope:** two pre-authorized geometry corrections (tail taper, supraorbital integration). Everything else is inspected and documented, not changed. No UE5.

**Images** are in `reviews/images/saurin-polish/`:

| Required item | File |
|---|---|
| 1. Tail before/after (profile, tail profile, top, dorsal oblique, rear 3/4, root rear 3/4) | `p9_01_tail_before_after.jpg` |
| 2. Tail taper measurement: radius, area and taper-rate graphs, silhouette overlays, numbers | `p9_02_tail_taper_graph.jpg`, `p9_taper.json` |
| 3. Brow/supraorbital before/after, neutral material (front, profile, front 3/4, rear 3/4, top, two brow close-ups) | `p9_03_brow_before_after.jpg` |
| 4. Neutral whole organism, identical cameras, before/after | `p9_04_whole_neutral.jpg` |
| 5. Representative pigmented whole body after (Gate 8 vs polish; P1, P2, P7, P9) | `p9_05_pigmented_whole.jpg` |
| 6. Representative pigmented head after | `p9_06_pigmented_head.jpg` |
| 7. Pattern flow over the corrected tail | `p9_07_pattern_flow.jpg` |
| 8. Regional Scale Architecture preservation | `p9_08_rsa_preservation.jpg` |
| 9. Geometry-change accounting and heat map | `p9_09_change_accounting.jpg`, `p9_accounting.json` |
| 10. 4K detail-ceiling audit | `p9_10_4k_detail_audit.jpg`, plus §5 below |
| 11. "Grown, not assembled" findings, not changed | `p9_11_grown_findings.jpg`, plus §3 below |

**Mesh on Tyler's PC** (`RaceBodies/out/`):
- `saurin_polish_base.npz`: the polished anatomical base. 1,121,082 vertices, watertight: 0 boundary edges, 0 non-manifold.
- `saurin_polish_surface_delta.npz` with `rebuild_polish.py`: rebuilds the full 4.48 M-vertex scaled surface exactly (error under 0.001 mm).
- `SaurinPolish.blend` / `.fbx`: a preview decimated to 1.12 M triangles.

**Tools** are in `tools/rodin/polish/`:

| Tool | What it does |
|---|---|
| `tailfix.py` | Tail taper remap |
| `tailprof.py` | Outline profile measurement |
| `slicearea.py` | Planar cross-section measurement |
| `taper_graph.py` | Taper graphs and numbers |
| `seedmap.py` | Carries the Gate 7 scale seeds onto the new mesh |
| `acct.py` | Change accounting |
| `mkmaps.py` | Colour maps (scale families, heat map) |
| `compose13.py` | Sheet layout |
| `build.sh`, `r12.sh` | Build and render scripts |

`tools/rodin/gate1/` holds:
- `wf_saurin_head63.py`: adds `BROW_INT`. `BROW_INT=0` reproduces the Gate 7 skull exactly; the previous file is kept as `wf_saurin_head63_g7.py`.
- `efield14.py` and `assemble14.py`: the brow field-difference surgery.
- `g7surfc.py` and `seedpd.py`: now accept carried seeds.

## 1. Tail taper continuity (geometry correction)

**Diagnosis.**
- I measured true planar cross-sections perpendicular to the anatomical axis, from sacral base to tip.
- In Gate 8 the area rises slowly to ~120 cm² at s ≈ 55 cm (s = distance from the tail tip). It then jumps to ~300 cm² within ~15 cm (s 55–70, f ≈ −65 to −72) and plateaus to the root. That jump plus plateau is the bulb.
- Peak taper rate is **23.1 cm²/cm**. In the outline there is a dorsal knob and a ventral pinch at f ≈ −65.

**Method.** Volume redistribution, not shrinking:
- **Target taper.** A smooth Hermite equivalent-radius curve runs from the unchanged terminal taper (s = 12 cm) to the unchanged root (s = 98 cm). It matches value and slope at both ends and holds the **same volume** over s = 12–98 cm.
- **Outline smoothing.** In every direction around the tail, the outline radius is smoothed along the axis (σ ≈ 6 cm), which removes the knob and the pinch. Each section is then scaled to the target.
- **Applied as** a radial, per-direction remap about the unchanged axis, with the remap field smoothed over the surface. A first attempt left a ring artefact where the axis bends; smoothing the remap field fixed it.
- **Untouched:** the sacral base, caudofemoral slips and root (s ≥ 98) and the terminal taper (s ≤ 12).

**Result** (`p9_01`, `p9_02`):

| Measure | Gate 8 | Polish |
|---|---|---|
| Volume, s 12–98 cm | 17,683 cm³ | 17,696 cm³ (+0.08 %) |
| Peak taper rate | 23.1 cm²/cm | 11.2 cm²/cm |
| Max \|d²r/ds²\| | 0.197 | 0.127 |
| Root equivalent radius at s = 100 | 12.95 cm | 12.95 cm |
| Tail tip position | — | identical (shift 0.0 cm) |

- The taper now reads as integrated muscular root → long progressive taper → slender distal tail → fine terminal taper.
- Length, path and direction are preserved; the tip is in the same place.
- The largest vertex move is 2.3 cm, at the old bulb. Mass moved from the old plateau (s 65–92) into the mid tail (s 40–65).

## 2. Supraorbital/brow-shelf integration (geometry correction)

**Diagnosis.**
- The Gate 7 brow was a constant-radius capsule ridge. Its rear end stood out laterally as a rounded block.
- It met the vertical postorbital bar in a hard L/T corner, sitting on a flat temporal plane with a concave crease underneath.
- So it read as a bar placed on the skull.

**Change** (skull SDF, `BROW_INT=2`; nothing else in the skull touched):
- **Sharp crest kept:** the ridge is now a tapering cone, 0.60 → 0.40 cm.
- **Broad root:**
  - a broad, low root web into the frontal/interorbital roof;
  - a lateral web filling the concave crease under the ridge's outer face.
- **No slab end:** the ridge continues as a thin, tapering line that dissolves into the temporal line.
- **Postorbital junction:** the bar tapers toward the brow and joins it with a filleted root.

**Method.** Field-difference surgery, as at the Gate 6 closure:
- Only vertices whose field changed by more than 0.8 mm were re-surfaced: 5,777 field-changed vertices, an 11.0 k-vertex patch.
- The patch was zipped with a largest gap of 2.6 mm; 4,581 seam-band copies were relaxed, by at most 1.9 mm.
- Everything else is copied bit for bit.

**Result** (`p9_03`, neutral material, identical cameras):
- The crest and the crisp orbital plane change are still there, and the front view keeps the angular reptilian brow.
- The ridge now grows out of the frontal roof and runs back into the temporal line. The lateral knobs and the slab end are gone, and the L-corner is filleted.
- Skull proportions, rostrum, jaw and the +8 % scale are unchanged.
- Base change in the head: max 9.6 mm, 99th percentile 5.3 mm, all at the brow/postorbital junction.

**Residual:** the postorbital bar still reads as a distinct vertical bar in pure profile. It is a real bony bar, and its junction is now filleted, but see finding 8.

## 3. "Grown, not assembled" inspection (documented, NOT changed)

These are from neutral views of the polished base (`p9_11`), listed by priority. Each needs an author decision before anything is changed.

| # | Location | What reads as assembled | Suggested fix (for authorization) |
|---|---|---|---|
| 1 | Sternum / chest | Raised Y/chevron strips and a vertical bar on the sternum read as applied inlays (Gate 5 load-path detail) | Lower and broaden them into the pectoral sheet, or carry them in normal maps only |
| 2 | Dorsal neck / upper thorax | A raised midline rod between the scapulae ends abruptly mid-back, like a peg | Taper it continuously into the dorsal spine line |
| 3 | Shoulder top | A sharp, narrow crease along the acromial edge reads like a cut seam | Widen the crease into a graded fold |
| 4 | Upper arm (lateral) | Path grooves read as straps or bands rather than muscle | Soften and lengthen them, or move them to normal maps |
| 5 | Inguinal / hip | Narrow creases at the thigh/pelvis boundary, plus the faint residual hip fold from Gate 6 | Fillet the creases |
| 6 | Heel / Achilles | A localized lump above the heel with a step at its top; also one tiny dark speck (mesh defect) on the front of the ankle | Blend the lump into the calcaneal tendon; repair the speck |
| 7 | Head–neck junction | A faint faceted band on the side of the neck where the head re-mesh meets the body (visible in close-up) | Re-mesh the neck band across the splice |
| 8 | Postorbital bar | Integrated at the brow but still a separate-looking vertical peg in profile | Taper it into the jugal more strongly (outside this order's brow authorization) |

The caudofemoral slips, tail root, hands, feet and knee read as grown. No other block, swelling, step or appendage-on-humanoid read was found.

## 4. Surface preservation and re-projection

- **Scale seeds** are carried from the Gate 7 closure.
  - 135,248 of 138,497 are kept: every scale outside the brow patch is the same scale.
  - On the tail the scales are carried with the taper deformation (re-projection), so they stretch or compress slightly with girth.
  - 4,156 new seeds were placed only inside the re-meshed brow patch.
- **Surface outside the two corrected zones:** identical to Gate 7 (max difference 0.00 mm over 3.42 M vertices).
- **Scale-family agreement with Gate 7:**

  | Zone | Agreement |
  |---|---|
  | Everywhere else | 100.0 % |
  | Head | 99.1 % |
  | Tail | 97.5 % |

  The tail figure moves because the underside/side ventral boundary follows the new section shape (+8 k ventral vertices). Family identities and graded boundaries are unchanged (`p9_08`).
- **Gate 8:** the model is re-evaluated on the corrected geometry: fields rebuilt, the same phenotype code, the same cameras.
  - Tail bands and stripes still flow trunk → sacral base → root → free tail. The band period now shortens smoothly, with no crowding at the old bulb (`p9_07`).
  - Facial pattern still respects the brow, orbital and rostral planes (`p9_06`).
  - The corrections are judged in neutral material first (`p9_01`, `p9_03`, `p9_04`). No scale, pattern or lighting change was used to hide geometry.

## 5. 4K detail-ceiling audit

This separates what future production detail needs from today's diagnostic fidelity. Diagnostic today means a ~4.5 M-vertex displaced surface with 0.9 mm edges and procedural vertex colour. Production should carry detail in layers, not in an ever-denser base mesh.

**By viewing distance:**

| Distance | Approx. size at 4K | What carries the read |
|---|---|---|
| Normal gameplay | body ~300–700 px tall | Silhouette, value pattern, scale-field breakup in normal and roughness maps. A base mesh of ~60–120 k triangles with LODs is enough; no scale geometry. |
| Dialogue / cinematic | head ~1,200–1,800 px | Planes in the base mesh (done here). Scales as displacement plus normal maps (4K head maps, tiled 4K body maps). Roughness micro-variation. An eye shader with refraction. |
| Extreme face or hand close-up | feature fills the frame | Per-scale edge irregularity, interscale tissue, lid folds, cornea/iris parallax and keratin growth lines. These need ~8K-equivalent texel density (UDIMs) plus tessellated displacement or a hero sculpt. |

**Where each feature should live** (full table on `p9_10`):

| Feature | Where it belongs |
|---|---|
| Major planes, brow, tail taper | Base geometry (done this pass) |
| Scale field and scale height/shape variation | 16-bit displacement plus normal maps, never base mesh |
| Individual scale-edge irregularity | Sculpt or procedural displacement, plus edge wear in roughness |
| Interscale tissue | Groove depth in displacement; rougher, paler albedo; thin-skin SSS |
| Articulation folds | Primary folds in base geometry; secondary folds in displacement and normal maps; later, corrective blendshapes |
| Facial microstructure | Head UDIM displacement, normal, roughness and albedo maps; SSS at lid and labial margins |
| Eyelid/socket transitions | Lid thickness and aperture in geometry; detail in displacement; a moist margin in roughness |
| Cornea / iris / nictitating membrane | Separate eye meshes: cornea shell, iris disc, membrane sheet. Refractive cornea material, iris relief and maps, and a transmissive membrane. This needs new geometry; today's membrane is shading only. |
| Keratin growth and wear | Horn/claw form in geometry; growth ridges in displacement; banding in albedo; roughness 0.30–0.45; tip translucency |
| Claw/digit transitions | Nail-bed fold geometry plus displacement |
| Contact surfaces | Pad volume in geometry (done); fine tubercles in displacement; matte 0.7–0.8 roughness |
| Roughness breakup | Tileable detail roughness, not geometry |

**Current gaps** that block a production close-up:
- the eye is a single surface;
- scales are regular Voronoi cells;
- there is no interscale micro-texture;
- there is no lid or claw fold geometry;
- colour is per-vertex (about one sample per 0.9 mm) rather than UDIM maps;
- the head–neck splice band (finding 7).

## 6. Closure criteria

| Criterion | Result |
|---|---|
| Tail keeps a powerful integrated root and tapers continuously, with no bulb | **Yes.** Root unchanged; the area curve is monotone and smooth; the taper-rate spike is halved; volume is preserved. |
| Supraorbital shelf stays sharp and reptilian while reading as part of the skull | **Yes.** Crest kept; root broadened; the slab end and lateral knobs are removed. The postorbital bar remains a flagged residual. |
| Accepted proportions and identity intact | **Yes.** Height, width and depth unchanged (187.88 / 90.56 / 161.48 cm base); silhouette change confined to the tail mid-section. |
| No unapproved anatomy changed | **Yes.** Base vertices outside the brow box and the tail: max change 0.00 mm (856,200 vertices). |
| Gate 7 scale architecture coherent | **Yes.** Same scales carried; 100 % family agreement outside the two zones. |
| Gate 8 pigmentation/pattern logic survives | **Yes**, on the representative phenotypes P1, P2, P7, P9 and the banded and axial patterns. |
| 4K audit separates future production detail from current fidelity | **Yes** (§5, `p9_10`). |

**Not re-rendered:** the Gate 7/8 display-variant heads were not re-built on the polished skull. Their attachments are anchored to the skull surface, so they would re-seat automatically, but they have not been re-checked.

**STOP: polish package. Awaiting author review.** No sex anatomy, age system, creator sliders, clothing/equipment, rigging, animation, gameplay, final microdetail production or UE5.

— Claude
