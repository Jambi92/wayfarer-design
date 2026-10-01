# Saurin Targeted Sculpt 4 — Jaw Architecture Pass

**Author:** Claude
**Responds to:** `reviews/claude-saurin-targeted-sculpt-4-directive.md`
**Status:** DIAGNOSTIC, NOT FINAL. Returned for Tyler/ChatGPT review.
**Scope:** Saurin head only. Hands and feet are held as the TS3 design, and the body, tail, scale architecture and other races are untouched. No spec edits, no Pass 2 work, no UE5 work.

## What changed

**Two jaw masses, not a carved line.** The head is now built from two separate volumes:
- an **upper jaw**, the rostral-maxillary complex continuous with the cranium. Its ventral face *is* the oral margin, and its lateral wall slightly overhangs the mandible.
- a **mandible**, its own narrower volume. It deepens toward the back and has a posterior ramus rising to the hinge and a mandibular angle.

The two volumes meet with only a small blend, so the mouth boundary comes from where they meet. The carved TS3 seam and labial ridges are removed. Only a hairline contact shadow remains, plus subtle scalloping of the margin.

**Front smile removed.** The oral margin now runs nearly level from the rictus to the tip, so the front view no longer forms a smile curve.

**Nose pad reduced.** The changes at the rostral tip are:
- it is tapered into a flatter spade;
- the nostrils are smaller openings set in shallow narial fossae on the rostral surface;
- the mandible now ends behind the upper-jaw tip;
- on the scaled head, the anterior rostrum is no longer a separate smooth scale field (fine scales now sit only along the oral margin, eyes, ear and throat).

**Posterior jaw.** The jaw-closing muscle volume sits between the orbit, temporal platform and hinge. The quadrate/hinge mass is larger, and the mandibular angle is deeper.

**Not changed:** the TS3 orbital seating, vertical pupils, recessed ear, cranial length and neck treatment.

## Diagnostic package (both sexes)

All images are in `reviews/images/targeted-sculpt-4/` and are labelled DIAGNOSTIC, NOT FINAL.

| Directive item | File |
|---|---|
| 1. Bare head geometry (front, profile, 3/4) | `saurin4_{Masc,Fem}_head_bare.jpg` |
| 2–3. Jaw structure (bare profile, 3/4) and front-mouth closeup (bare and scaled) | `saurin4_{Masc,Fem}_jaw_front.jpg` |
| 4. Hinge, temporal platform and throat closeup | `saurin4_{Masc,Fem}_hinge.jpg` |
| 5. TS3 vs TS4, identical camera, scale and lighting | `saurin4_{Masc,Fem}_head_comparison.jpg` |
| 6–7. Final reference head (scales, pupils) and head/neck/upper torso | `saurin4_{Masc,Fem}_head_final_neck.jpg` |

## Self-check against Section 12 (honest)

| Gate | Result |
|---|---|
| Mouth reads as a groove cut into one mass | **Improved, not solved.** The volumes are separate, but in bare geometry the upper/lower jaw boundary is still subtle. |
| Front view smiles | **Pass.** The margin is level from the front. |
| Rostral tip reads as a mammalian nose pad | **Fail.** In the straight-on front closeup the tip still reads as a rounded pale pad. |
| Upper and lower jaw volumes distinguishable | **Partial.** Clear in 3/4, weak in front view. |
| Posterior jaw and hinge weak relative to the snout | **Partial.** Stronger than TS3, but the snout still dominates. |
| Margin perfectly uniform | **Pass.** It has small curvature and thickness changes. |
| Human lips, chin or nose return | **Pass.** None returned. |
| Regresses toward a human morph | **Pass.** |
| Mascot/gecko simplification | **Partial.** |
| Orbital seating kept | **Pass.** |
| Reads as Saurin without scales or pupils | **Pass.** |

## Assessment and recommendation

Over four passes the structure has moved in the right direction. The remaining failures are now surface-form problems:
- the tip form;
- the subtle plane changes that separate the jaws in front view;
- the hinge musculature.

Signed-distance blockout scripting resolves these poorly. Each further numeric pass trades one artifact for another, as with the rostral tip in this pass.

Following Tyler's earlier decision (script fixes, then hand-sculpt), I recommend ending the scripted iterations here. The next step would be a hand-sculpt pass in Blender, using `RaceBodies/out/SaurinSculpt4_{Masc,Fem}.blend` as the structural base, with this checklist:
1. Sculpt the anterior rostrum as one tapered keratinized plane system, with no pad.
2. Cut a clear upper-jaw and mandible plane change visible from the front.
3. Sculpt the hinge musculature and the throat transition.
4. Clean the neck join line.

## Spec/model conflicts

None found. No spec was edited.
