# Saurin Targeted Sculpt 6 — Structural Plane and Ridge Architecture

**Author:** Claude
**Responds to:** `reviews/claude-saurin-targeted-sculpt-6-directive.md`
**Status:** DIAGNOSTIC, NOT FINAL. Returned for Tyler/ChatGPT review.
**Scope:** Saurin only. No Pass 2 work, no UE5 work.

## Head: from rounded volumes to a hierarchy of planes

The head's sections are now rounded polygons rather than ellipses. Edge sharpness runs from broad and organic on the cranium to decisive on the rostrum, so the dorsal, dorsolateral, lateral and ventrolateral faces read as planes.

The rostrum ends in an anterior terminal plane rather than a rounded cap. The nostrils stay lateral.

Structural ridges are raised from the skull surface itself. They are not separate parts, so they appear on every Saurin regardless of display:

| Ridge | Where it runs |
|---|---|
| Canthus rostralis | Orbit to nostril; the dorsal/lateral rostral edge |
| Temporal line | Postorbital bar to occiput; the dorsolateral cranial edge |
| Jugal/maxillary ridge | Rostral base, under the orbit, to the hinge |
| Occipital transition | Across the rear of the cranial roof |
| Mandibular lateral/inferior ridge | Along the mandible, turning up toward the hinge |

Other head changes:
- **Orbit:** a tighter supraorbital rim and a postorbital bar, so the eye is housed by the skull rather than by a brow. The lid line is neutral, with no scowl.
- **Temporal plane:** the side of the cranium is flattened between the temporal line and the jaw.
- **Posterior skull:** lower, with a slimmer posterior lower cranium. The old rounded "bulb" behind the jaw is removed.
- **Jaw:** the mandible is narrowed to sit inside the skull's width. The ramus, angle and hinge are tucked in, and the retroarticular process is kept small.

## Body and tail (restrained)

A `WF_SaurinStructure` shape key adds edges where anatomy supports them:
- tibial crest;
- ulnar border;
- clavicular edge;
- scapular spine;
- iliac crest;
- olecranon, patellar edge and malleoli;
- a low dorsal vertebral line.

Composition is unchanged. There is no plating and no sharpened muscles.

Tail:
- a dorsal caudal line and a slightly flatter venter;
- the keel begins only after the tail leaves the body;
- the tail root is now closed and sunk deeper into the sacral mass, which fixes a visible open edge at the root.

## Package (both sexes)

All images are in `reviews/images/targeted-sculpt-6/`.

| Directive item | File |
|---|---|
| A. Bare skull: front, profile, 3/4, high 3/4, low 3/4, jaw 3/4 | `saurin6_*_skull_bare.jpg` |
| B. Structural region annotation | `saurin6_*_structure_regions.jpg` |
| C. TS5 vs TS6 (scaled and bare), identical camera | `saurin6_*_comparison.jpg` |
| D. Minimal-display test (bare and scaled) and E. integrated swept-back, crest and mixed/asymmetric | `saurin6_*_displays.jpg` |
| F. Full body TS5 vs TS6, true scale | `saurin6_*_body.jpg` |
| F/G. Bare body, back/leg/forearm closeups, tail base | `saurin6_*_body_structure.jpg` |

The display bases were re-seated on the new, lower TS6 cranium so they emerge from the surface.

The B annotation is approximate diagnostic colouring. Its boundaries are hand-set zones, not computed plane edges.

## Self-check against §20 (honest)

| Gate | Result |
|---|---|
| Bare geometry still smooth mammalian volumes | **Pass.** Planes and ridges now carry the read. |
| Collapses without scales or horns | **Pass.** The minimal-display bare skull reads Saurin. |
| Front view: eyes + nose + mouth | **Much improved.** The front now shows orbital rims, rostral planes and the jaw boundary. The terminal tip plane still catches light as a pale patch head-on. |
| Rostrum a single rounded wedge | **Pass.** |
| Orbit lacks structural integration | **Pass.** |
| Posterior skull an inflated sphere | **Pass.** |
| Mandible disappears into the throat | **Partial.** Clear in profile, softer in the low view. |
| Sharpness comes only from spikes | **Pass.** |
| Forced angry expression | **Pass**, in my judgement. The supraorbital rim is a shelf, not a brow. |
| Body uniformly cylindrical | **Partial.** The body structure is deliberately subtle; it is visible in closeups but faint at full-body scale. |
| Body excessively armoured | **Pass.** |
| Tail keratin confused with structural ridges | **Pass.** The keel is structural; scutes stay in the display system. |
| Gameplay or target-size implications | **Pass.** None. |

**Open quality issues:**
- Some plane edges at the cranium/temporal junction read slightly faceted. This is the "low-poly" risk the directive warned about, and a hand pass should soften them.
- The neck join line remains.

## Spec

The provisional **§36a Craniofacial Ridge-and-Plane Architecture** is added to `specs/saurin/SAURIN_V1.md`. It is marked **PROVISIONAL pending acceptance of these diagnostics**, per the directive's "if successful" condition. It does not alter §36, §100–102, §11a or any firewall.
