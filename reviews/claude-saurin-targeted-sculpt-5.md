# Saurin Targeted Sculpt 5 — Reptile Reference Study, Cranial Keratin Display, Tail Variation

**Author:** Claude
**Responds to:** `reviews/claude-saurin-targeted-sculpt-5-directive.md` (including the §14 tail addendum)
**Status:** DIAGNOSTIC, NOT FINAL. Returned for Tyler/ChatGPT review.
**Scope:** Saurin head, cranial display and tail phenotype only. Gorrund and the other races are untouched. No Pass 2 work, no UE5 work.

## 1. Canon update (done, as directed)

`specs/saurin/SAURIN_V1.md` now records Tyler's October 1, 2026 revision (commit `954d1a8`):
- **§100–102 — Cranial Keratin Display System.** This replaces the old "no true horns / low ridges only" rule, which is kept only as marked superseded history. It covers:
  - attachment regions;
  - the integration requirements;
  - the FD-STRUCT/FD-SURF split;
  - the Biological / Acquired / Applied layers;
  - the sex, culture and gameplay firewalls.
- **§101a — optional cranial-to-caudal display continuity.**
- **§11a — tail individuality and customization**, with coupled validity, firewalls and the "not easier to hit" ruling.
- **Related edits:**
  - §58 marked superseded;
  - §116 (hair-equivalent) and §150 (now Cranial Display creator controls) updated;
  - §145 tail creator controls extended;
  - SAU-SURF-14 and SAU-SURF-25 test rows updated;
  - the surface summary line updated.

## 2. Reference study (synthesized, no species copied)

| Source family | What I took from it |
|---|---|
| Lizards generally (monitor, iguanid, agamid) | Nostrils sit **laterally near the snout tip**, on the edge where the dorsal and lateral snout planes meet (the canthus rostralis). They are not on a frontal pad. That edge also makes the rostrum narrower on top than at the jaw line. |
| Varanids (Komodo skull study) | A blunt pyramidal skull. The mandible thickens posteriorly into a free **retroarticular process** behind the jaw joint. The jaw-adductor mass fills the region between the orbit, temporal arch and jaw angle. |
| Crocodilians | The upper jaw and mandible read as two masses, and the upper jaw overhangs the lower. (Already in TS4; kept.) |
| Horned lizards (*Phrynosoma*) | Cranial horns grow from **parietal (occipital) and squamosal (temporal)** regions, on broad skull bases. I used these as the valid attachment regions for the display system. |

## 3. Skull changes (TS5)

- **Rostral tip:**
  - Frontal nostrils removed. The nares now sit laterally at the canthus, in shallow narial fossae.
  - The rostrum is trapezoidal in section (narrower dorsally).
  - The dorsal planes fade before the tip, so it ends in one continuous form.
- **Mandible:**
  - Deeper body.
  - A retroarticular process behind the hinge.
  - A pterygoid/adductor "jowl" at the jaw angle.
  - A gular fold that separates the mandible's ventral edge from the throat.
- **Occiput:** a new posterior profile flows into the nape. TS2–TS4 had a rounded knob at the back of the skull, and it is removed.
- **Not changed:** TS4's two-volume jaw (upper overhangs lower), the level oral margin, TS3/TS4 orbits and pupils, hands and feet.

## 4. Cranial Keratin Display exploration

The seven configurations below are all built on **one** skull. They are grown out of the skull surface with blended base footprints, not attached separately.
- `saurin5_display_1-4.jpg`:
  1. minimal paired parietal ridges
  2. low hornlets (postorbital, temporal, occipital)
  3. swept-back paired horns from the squamosal corners
  4. crest-dominant (midline blade plus low side ridges)
- `saurin5_display_5-6.jpg`:
  5. plate- and spike-dominant (posterior spike crown plus temporal keratin plates)
  6. mixed, with **mild natural asymmetry** (left horn about 15% shorter) and brow hornlets
  - 6b. the **same individual with acquired breakage** (left horn snapped to a stump), labelled separately
  - the bare skull with no display

These are exploratory examples. They are not subraces, not final hairstyle slots, and carry no sex or gameplay meaning.

`saurin5_{Masc,Fem}_integrated.jpg` shows configurations 3 and 6 integrated on the full body, with:
- Regional Scale Architecture;
- vertical pupils;
- a neutral expression;
- front, profile, 3/4 and head/neck/upper-torso views.

## 5. Tail variation concept sheet

`saurin5_{Masc,Fem}_tail_variants.jpg` shows six tails on the same accepted body and pelvis. Each tail is complete and shown in side view. Masculine values (feminine within about 1 cm):

| Variant | Length | Base diameter | Volume |
|---|---|---|---|
| 1 Reference / balanced | 128 cm | 23 cm | 18 L |
| 2 Shorter / heavier | 107 cm | 26 cm | 22 L |
| 3 Longer / gradual taper | 149 cm | 25 cm (base increased to carry the length) | 30 L |
| 4 Laterally broad, mass proximal | 132 cm | 24 cm | 15 L, fine distal tail |
| 5 Restrained dorsal keratin scutes | same as reference | — | — |
| 6 Slender with inherited banding | 137 cm | 22 cm | — |

Variant 5's scutes shrink distally and are absent at the root and the last third. Base, length, mass and carriage were coupled by hand for each example. All are labelled exploratory phenotypes, not subraces and not gameplay variants.

## 6. Skull package (both sexes)

| File | Contents |
|---|---|
| `saurin5_*_head_bare.jpg` | Bare head: front, profile, 3/4 and low 3/4 (underside) |
| `saurin5_*_jaw_front.jpg` | Front rostrum and mouth (bare and scaled), jaw and hinge in profile and 3/4 |
| `saurin5_*_head_comparison.jpg` | TS4 vs TS5, identical camera |

## 7. Self-check (honest)

| Gate | Result |
|---|---|
| Looks human or mammalian without scales and horns | **Pass** in profile and 3/4. |
| Rostral tip reads as a separate nose button | **Partial / still the weakest point.** The nostrils are no longer on it, but head-on under frontal light the tip is still a bright rounded patch. |
| Upper and lower jaw inferable from bare geometry | **Pass** in profile and 3/4 (overhang, gular fold, retroarticular process). **Partial** from the front. |
| Mouth reads as a carved seam | **Improved.** Only a hairline contact line remains. |
| Front view collapses to an eyes + nose + mouth hierarchy | **Partial**, because of the tip patch. |
| Display structures look glued on | **Pass.** They grow from blended bases at valid regions. |
| Horns required for a reptilian read | **Pass.** The bare skull reads Saurin. |
| One forced horn silhouette | **Pass.** Seven configurations, including minimal. |
| Display or tail encodes sex, culture or gameplay | **Pass.** Masculine and feminine use identical configurations. |
| Direct species copying or generic dragonborn | **Pass**, in my judgement. Configuration 6's upswept horns come closest to a "fantasy horned" read. |
| Tail variation is only colour | **Pass.** Silhouettes differ. Variant 5's scutes are deliberately small and only subtle at full-body scale. |

## 8. Recommendation

The structure and canon now support the display and tail systems. The front-view rostral tip remains the one persistent failure across TS3–TS5. My recommendation from TS4 stands: finish the tip and front jaw read with a hand-sculpt pass on `RaceBodies/out/SaurinSculpt5_*.blend` rather than more scripted passes.

## Sources

- [Skull morphology of the Komodo dragon — digital-dissection study (ScienceDirect)](https://www.sciencedirect.com/org/science/article/pii/S2535073024000123)
- [Digimorph — Horned Lizards (parietal and squamosal horns)](https://digimorph.org/resources/horned.phtml)
- [Digimorph — Horned Lizard Skulls](http://digimorph.org/resources/hornedskulls.phtml)
- [Homology of the jaw muscles in lizards and snakes (Anatomical Record)](https://anatomypubs.onlinelibrary.wiley.com/doi/10.1002/ar.22857)
- [The roles of joint tissues and jaw muscles in the savannah monitor (JEB)](https://journals.biologists.com/jeb/article/222/18/jeb201459/223478/The-roles-of-joint-tissues-and-jaw-muscles-in)
