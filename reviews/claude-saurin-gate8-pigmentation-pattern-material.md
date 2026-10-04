# Saurin Gate 8: Pigmentation, Biological Patterning and Material Response (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/chatgpt-saurin-gate8-pigmentation-pattern-material-order.md` (6496be9)
**Base:** frozen Gate 6 (`saurin_gate6_closed`) and Gate 7 closure (a6a5fb9), with display families as reconciled in d67309f.
**Scope:** visual development only. No geometry, no UE5.

**Images** are in `reviews/images/saurin-gate8/`:

| Required item | File |
|---|---|
| 1. Neutral material calibration (roughness 0.30 / 0.45 / 0.55 / 0.72; whole body, torso, scale close-up) | `g8_01_material_calibration.jpg` |
| 2. Pigmentation families (10 phenotypes) | `g8_02_pigmentation_families.jpg` |
| 3. Pattern families (9 families: same pigments, same individual; profile and rear 3/4) | `g8_03_pattern_families.jpg` |
| 4. Whole-organism phenotypes (10 individuals, identical pose, camera and light) | `g8_04_whole_organism.jpg` |
| 5. Head close-ups (8 phenotypes, front 3/4 and profile) | `g8_05_heads.jpg` |
| 6. Tail/root pattern flow (6 pattern types) | `g8_06_tail_flow.jpg` |
| 7. Regional Scale Architecture material response | `g8_07_rsa_material.jpg` |
| 8. Cranial display keratin (5 display families × 3 keratin relationships × 2 phenotypes) | `g8_08_display_keratin.jpg` |
| 9. Eye and nictitating membrane (4 irises × 3 membrane states) | `g8_09_eyes.jpg` |
| 10. Failure controls, with measured safeguards | `g8_10_failure_controls.jpg`, `g8_safeguards.json` |

**Tools:** `tools/rodin/gate8/`
- `g8axis.py`: the anatomical centreline, saved as `axis.npy`.
- `g8fields.py` (with `fixlw.py`): per-vertex anatomical fields.
- `g8pheno.py`: the phenotype → colour/material model.
- `g8lib.py`: the phenotype library.
- `g8render.py`: Cycles renderer.
- `mkjobs.py`, `g8metrics.py`, `compose12.py`, `runall.sh`, `rerun.sh`, `hvfields.sh`.

**Rendering:** Blender 5.0 Cycles (CPU, 40 samples, denoised, AgX view transform). Every image uses the same three-light studio rig and grey world. Hand/foot crops add an underside fill so the contact surfaces can be seen, and are marked as such.

## How it works

Colour is computed from anatomy, never painted on.

1. **Anatomical coordinates.**
   - A centreline runs from tail tip through the pelvis and neck to the snout. Every axial vertex gets an arc-length position, an angle around the body (0 = dorsal, ±π = ventral, sign = side) and the local girth.
   - Each limb has its own chain (shoulder → elbow → wrist → fingertip, hip → knee → ankle → toe), with a position along the limb, an angle and the limb girth.
   - Patterns are evaluated in girth-normalized coordinates. So a band or blotch scales with the body part it sits on: it shrinks along the tail and is finer on the neck and face. Patterns wrap around the body, continue trunk → sacral base → tail with no seam, and are bilaterally symmetric, with a controllable asymmetric component.
   - A blend weight merges the trunk and limb pattern systems over about 12 cm from each limb root. The first render pass blended over only about 1 cm and showed a visible colour line on the upper thigh. I found it in review, fixed it, and re-rendered every affected sheet; it is reported here as a caught error.
2. **Scale-aware edges.** Every vertex knows its Gate 7 scale cell: the identical Poisson seeds, regenerated. Pattern edges can be quantized to whole scales, as in real reptile pattern, or left soft. This "edge softness" is a phenotype control. Per-scale value and saturation jitter is small (±3.5 %), so no scale is individually multicoloured.
3. **Pigmentation layers.** These are the phenotype parameters:
   - dominant hue family (primary);
   - secondary pigment;
   - pattern family, contrast, element scale, edge softness and asymmetry;
   - dorsal/ventral value relationship: smooth countershading, with the pattern fading but continuing across the ventral field;
   - dorsal darkening;
   - facial accent: a post-orbital stripe from the eye to the tympanic recess, following the jugal plane;
   - facial pattern damping: × 0.5 on the head, × 0.3 on the rostrum;
   - distal shift on hands, feet and distal tail;
   - keratin base colour and keratin-to-body relationship;
   - two-tone iris.
4. **Material.** These are Principled BSDF roughness offsets by Gate 7 family, with no metallic, no emission and no glossy coat on scales:

   | Region | Roughness |
   |---|---|
   | Base (dry satin) | 0.55 |
   | Articulation | +0.05 |
   | Fine expressive | +0.02 |
   | Ventral | +0.04 |
   | Contact | +0.18 (matte, paler) |
   | Interstitial skin between scales | +0.15 (slightly paler) |
   | Keratin | 0.32–0.40, slight subsurface translucency toward tips, faint growth banding along the growth axis |
   | Eye | clear corneal coat over the iris |

## Required answers

**1. What is the natural roughness/material envelope?**
- Scales sit at roughness **0.45–0.72** (dry satin to matte). The default is 0.55 with the family offsets above, which gives 0.54–0.59 median on scaled skin and 0.70–0.80 at contact fields and in grooves.
- **0.30** is the lower bound, for "modest localized sheen" only (`g8_01`).
- Keratin is smoother, at 0.32–0.40. Only the cornea is glossy.
- Metallic, emission and coat on skin are all zero in every accepted phenotype.
- Wet (0.06 plus coat), metallic, gem and plastic responses are rejected (`g8_10`).
- **Honest note:** under this soft studio rig the visible difference between 0.45 and 0.72 is small. Sheen first becomes noticeable at 0.30. The envelope should be re-checked under harder in-game lighting.

**2. Which pigmentation dimensions are independent and which should be coupled?**
- **Independent** (inherited separately): dominant hue family, overall value, saturation, pattern family, pattern contrast, pattern element scale, edge softness, asymmetry, iris colour, and the keratin-to-body relationship. Keratin can be independent, as in the neutral-horn and dark-keratin examples, or partly matched to the body.
- **Coupled:**
  - Secondary pigment stays in the primary's hue family (darker or lighter) unless a high-contrast phenotype is chosen.
  - Ventral value follows the primary: lighter, same hue family, never white.
  - Interstitial skin follows the local scale colour.
  - Contact fields are a paler, desaturated version of the local colour.
  - Facial pattern contrast is tied to body pattern contrast but always damped.
  - Distal shifts follow the body hue.
  - Keratin tips lighten relative to the base.
- **Never coupled:** colour to sex, class, culture, biome, profession, temperament or gameplay.

**3. Which biological pattern families are viable?**
All ten tested are viable as inherited patterns (`g8_03`, `g8_04`): near-uniform, dorsal mottling, lateral blotching, banding, broken banding, axial (dorsolateral) striping, speckling, regional contrast fields, mixed, and naturally asymmetric. Two caveats:
- **Distance:** speckling and low-contrast mottling almost vanish at whole-body distance and read as near-uniform there. That is acceptable biologically, but they only express at close range.
- **Limb bands:** band frequency was lowered once during this pass. In the slate phenotype (P2) the bands still sit slightly darker near the knees by chance (joint-ring index 0.82). This should be watched.

**4. How are pattern scale and orientation tied to anatomy?**
- Element size is normalized to local girth on the body axis and on each limb axis, so pattern elements shrink along the tail and neck and are finer on the face.
- Orientation follows the body axis: bands run transverse, stripes run longitudinal, and both stay aligned through the neck bend and the tail curve.
- Pattern edges can lock to Gate 7 scale cells, so larger structural scales carry larger, cleaner pattern masses and fine facial units carry fine variation.
- Countershading follows the body angle, so the ventral field changes gradually. The pattern fades into it rather than stopping.

**5. Does any phenotype erase the Gate 6/7 structural identity at normal gameplay distance?**
**No** (`g8_04`, `g8_05`). Silhouette, head architecture, tail and stance read in all ten individuals, including the darkest (P4 charcoal) and the lowest-contrast (P10). P4 loses some interior form under this lighting, but it does not lose identity. High-contrast banding (P2, P7) is the strongest surface read and still follows anatomy.

**6. Does the ventral field remain biological rather than cartoon belly plating or colour blocking?**
**Yes.**
- **Accepted:** ventral luminance is 1.2–2.4 × dorsal (linear), in the same hue family, with the pattern continuing at reduced contrast. The largest angular luminance step across the trunk is ≤ 0.21 for countershading. The axial-stripe phenotype reaches 0.53, but that step comes from its stripes, not the belly.
- **Rejected cartoon belly:** ventral luminance is 16 × dorsal, with a step of 1.54 (`g8_10`).

**7. Do facial patterns preserve the rostral/orbital/jaw hierarchy?**
**Yes** (`g8_05`).
- Facial pattern is damped (× 0.5 on the head, × 0.3 on the rostrum) and limited to accents that follow the planes.
- Brow shelf, orbital platform, rostral planes, jugal/quadrate transition and hinge read in all eight phenotypes, and the vertical pupil is legible in every iris.
- **Measured:** face-to-trunk cell contrast is 0.63–1.15 in the library, against 1.39 for the rejected face-noise control.

**8. Does tail pigmentation preserve root continuity?**
**Yes** (`g8_06`).
- The body-axis coordinate is continuous through the sacral base, so bands, stripes, blotches and mottling run trunk → root → free tail with no restart, and band period shortens smoothly with girth.
- The Gate 7 root articulation band gets no separate colour.
- **Measured:** the luminance jump across the root is ≤ 0.11 in the library, against 0.22 for the rejected tail-seam control. The pattern-variance ratio across the root is 0.94–1.22.

**9. How does keratin differ materially from scales?**
Keratin (claws and display) is smoother (0.32–0.40 vs 0.55), slightly translucent toward the tips, unscaled, and carries faint growth banding along its growth axis (`g8_07`, `g8_08`).

Three relationships to the body were tested on every display family:
- independent neutral horn;
- partly body-matched;
- dark keratin.

All three read as natural. None is bright, sexually coded, decorated, magical or weapon-like. Display attachments are the Gate 7 ones, unchanged.

**10. Are the phenotype examples broad enough to support individual identity without implying subraces?**
**Yes, for a first pass.**
- **Range:** the ten individuals span warm, cool and neutral hue families; light to near-black values; low to high saturation, all well below neon (99th-percentile saturation ≤ 0.69); low to high contrast; and uniform to strongly patterned.
- **Independence:** hue, pattern, contrast, iris and keratin are drawn independently, so no hue is tied to a pattern or eye type. This is what prevents fixed "types."
- **Labels:** names describe colour and pattern only. No individual is labelled by geography, ancestry, culture, sex or temperament.
- **Caveat:** ten examples is a small sample. A creator would sample continuous ranges rather than pick from these ten.

**11. Did any geometry, proportion, scale-field assignment or display attachment change?**
**No.**
- Every body render uses the Gate 7 closure mesh as is: it is byte-identical to `g7_surfc` (checked).
- Every display render uses the Gate 7 closure display heads (byte-identical to `hvsc_*`).
- Scale cells are regenerated from the same seeds (138,497, identical count).
- The Gate 7 region map is read, not written.
- The eye and membrane states are shading only.
- No mesh was written in Gate 8.

## Measured safeguards (accepted library vs rejection controls)

Full table: `g8_safeguards.json`.

| Safeguard | Accepted library | Rejected control |
|---|---|---|
| Roughness, scaled skin (min / median) | 0.54 / 0.59 | wet/plastic 0.06; dragon 0.15 |
| Metallic / emission | 0 / 0 | metallic 1.0; dragon 0.35 |
| Saturation (99th pct, sRGB) | 0.13–0.69 | dragon 1.00 |
| Ventral boundary step | 0.05–0.21 (axial stripes 0.53) | cartoon belly 1.54; dragon 1.30 |
| Joint-ring index (near-joint vs limb luminance) | 0.82–1.02 | joint rings 0.41 |
| Face/trunk cell contrast | 0.63–1.15 | face noise 1.39 |
| Tail-root luminance jump | 0.01–0.11 | tail seam 0.22 |

- **Paint-mask borders:** world-plane stripes are rejected visually (`g8_10`). They cut across limbs, face and tail regardless of anatomy. Every accepted pattern instead lives in body or limb coordinates.
- **Dragon colouring:** saturated red with a gold belly, gloss and pale keratin is rejected on saturation, gloss and hard-belly grounds together.

## Open items for the author

- **Distance:** fine patterns (speckling, low-contrast mottling) are close-range features. Decide whether whole-body readability should be required of every pattern family.
- **Eyes:** iris fibre detail is faint at this resolution. The membrane is a shading state, because Gate 7 has no membrane geometry; if animation needs one, membrane geometry is a later geometry question.
- **Lighting:** the roughness envelope should be re-checked under a harder in-game lighting rig.

**STOP: Gate 8 diagnostic package. Awaiting author review.** No sex-related anatomy, age system, creator sliders, clothing/equipment, rigging, animation, gameplay or UE5.

— Claude
