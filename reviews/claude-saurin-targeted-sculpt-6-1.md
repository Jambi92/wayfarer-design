# Saurin TS6.1 — Refinement of the TS6 Foundation

**Author:** Claude
**Responds to:** `reviews/saurin-ts6-1-refinement-directive.md`
**Status:** DIAGNOSTIC, NOT FINAL. Returned for Tyler/ChatGPT review. No UE5 work.

TS6 is the base. This is a refinement, not a new head.

## What changed

**Faceting → grown transitions.** I kept the plane hierarchy but lowered the edge sharpness and changed the ridges:
- the cranium is still broad, and the rostrum is still decisive but no longer machined;
- the rostral tip plane is softer;
- the ridges (canthal, temporal line, jugal/maxillary, occipital, mandibular) are wider and fade in gradually, with depths that differ by region instead of being one uniform crease;
- the temporal-plane blend is softer, and the supraorbital shelf blends more.

**Mouth and jaw:**
- **Margin:** follows the maxilla. It rises toward the oral corner and dips slightly mid-jaw, so it is not one straight incision.
- **Contact line:** tight anteriorly, deeper toward the corner.
- **Thickness variation:** supralabial and infralabial scale rows above and below the margin, varying along the jaw. These are not lips.
- **Oral corner:** a rictal soft-tissue fold where the opening ends, in front of the hinge.
- **Rostral tip:** the premaxilla closes slightly over the mandible tip, as in anterior closure.
- **Mandible:** deeper toward the front, so it no longer thins to a blade.

**Neck:**
- **Head side:** lateral cervical attachment masses from the jaw angle into the neck, and dorsolateral nuchal masses from the occiput.
- **Body side:** a lateral cervical line and a throat-to-sternum notch.
- **Posture:** upright carriage is kept.

**Kept from TS6:** hands, feet, claws, the body structure key, the tail keel, Regional Scale Architecture, vertical pupils and the recessed ears.

## Package

All images are in `reviews/images/targeted-sculpt-6-1/`.

| Directive item | File |
|---|---|
| A. TS6 vs TS6.1 head, bare and scaled | `saurin61_{Masc,Fem}_head_comparison.jpg` |
| B. Mouth/jaw (bare profile and 3/4, front mouth, hinge) | `saurin61_*_mouth_jaw.jpg` |
| C. Head/neck/shoulders, bare and scaled | `saurin61_*_neck.jpg` |
| D. Complete masculine Saurin at 188 cm (front, profile, rear 3/4, front 3/4), with low hornlets and a restrained dorsal-keratin tail | `saurin61_Masc_complete.jpg` |
| E. Complete feminine Saurin, same views, with a different phenotype: crest-dominant display and a long, gradual tail | `saurin61_Fem_complete.jpg` |
| F. Seven display configurations on one unchanged TS6.1 skull, including acquired breakage | `saurin61_display_a.jpg`, `saurin61_display_b.jpg` |
| G. Six tail phenotypes on one body | `saurin61_*_tails.jpg` |

## Honest self-check (§16)

**Pass:**
- 1, 2, 5, 8, 9: still non-human, same TS6 design, integrated rostrum, no mammalian lips/chin/nose, neutral expression.
- 11, 12: minimal-display Saurin identifiable; display varies on one unchanged skull.
- 14, 15: tail inevitable and mandatory; claws non-human but functional.
- 17, 18, 19: no gameplay, culture or personality encoded; no UE5 work.

**Partial:**
- **4 (faceting).** The change is deliberately subtle. Planes are softer, but the front still reads somewhat mask-like at the brow/rostral root.
- **6 / 7 (mouth and hinge).** The margin now varies and has a defined corner. At diagnostic resolution it still reads as a fine line in profile.
- **10 (neck and skull as one organism).** Improved at the skull end, but the visible neck below the join is still the base body's fairly cylindrical neck. A faint join line remains.
- **13 (body structure continuity).** Present, but subtle at full-body scale.

**Flag for Tyler — criterion 16:**
- The feminine diagnostic body still carries the generator's human-derived breast shape.
- The directive says Saurin sex-related anatomy is non-human and not yet defined.
- I didn't invent a replacement, because that is a biology decision. Should it be neutralised for the next diagnostics, or left until Saurin sex-related anatomy is designed?

**Not delivered:** the optional open-mouth diagnostic. I tried rotating the mandible about the hinge, but without a modelled oral cavity the result was misleading (a thin plate under an empty gap), so I left it out. A proper open-mouth test needs the inner mouth to be modelled.

## Recommendation

TS6.1 is about as far as scripted refinement usefully goes on the head. The remaining items are surface-quality work that a hand-sculpt pass on `SaurinSculpt61_*.blend` handles better:
- the mask-like front transitions;
- the mouth line read at close range;
- the neck join.

## Spec

No spec change. §36a stays PROVISIONAL until Tyler/ChatGPT accept.
