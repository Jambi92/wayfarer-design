# Saurin Targeted Sculpt 2 — Dedicated Head and Distal Digits

**Author:** Claude
**Responds to:** `reviews/claude-saurin-targeted-sculpt-2-directive.md`
**Status:** RETURNED FOR TYLER / CHATGPT REVIEW. Not declared final.
**Scope:** Saurin head, mouth/jaw, fingers and toes only.
- Gorrund is held as accepted, and the other eleven races are untouched.
- No spec edits, no Pass 2 work, no UE5 work.

All images are in `reviews/images/targeted-sculpt-2/`. Each item comes in both sexes.

| # | Requested item | File |
|---|---|---|
| 1 | Bare-geometry head (front, profile, 3/4; scale relief off; one neutral material) | `saurin2_{Masc,Fem}_head_bare.jpg` |
| 2 | Final-reference head (scales, vertical pupils) | `saurin2_{Masc,Fem}_head_final.jpg` |
| 3 | Head comparison, Targeted Sculpt 1 vs 2, same camera and scale | `saurin2_{Masc,Fem}_head_comparison.jpg` |
| 4 | Mouth/jaw closeup (profile, 3/4) | `saurin2_{Masc,Fem}_jaw.jpg` |
| 5–6 | Hands (front, palm, back, side) and feet (front, side, 3/4) | `saurin2_{Masc,Fem}_hands_feet.jpg` |
| 7 | Whole body, true scale, complete tail | `saurin2_{Masc,Fem}_true_scale.jpg` |

## Head: rebuilt, not morphed

The human-derived MPFB head and upper neck are **deleted**. In their place is a **dedicated Saurin head mesh**, as the directive authorized:
- built from a signed-distance construction of Layered Rostral-Cranial Integration, then meshed;
- skinned to the `head` and `neck_01` bones;
- source in `RaceBodies/wf_saurin_head.py`.

No human topology survives above the neck: no nose, nasal bridge, alar or nasolabial forms, philtrum, vermilion lips, chin, brow pads or pinnae.

**One integrated skull section.** The head is one tapering section from occiput to rostral tip, with the deep jaw as its lower half. A rostrum no longer sticks out of a human face.
- **Vault:** low to moderate and long front-to-back.
- **Orbital/temporal platform:** broad, widest behind the eyes, with a temporal/postorbital contribution.
- **Rostrum:** compact. Its root starts back at the temporal and orbital region and tapers moderately to a blunt tip.

**Orbits.** The eyes sit in orbital mounds on the dorsolateral corners of the skull platform.
- They are forward-facing, angled about 27° outward, so gaze stays readable for dialogue.
- A low supraorbital shelf sits above them. There is no scowl and no oversized eyes.

**Nasal openings.** These are two small openings on the rostral tip. They are not a modified nose.

**Oral seam.**
- It runs from the rostral tip back to the jaw hinge, under the temporal platform, which is much further back than a human mouth.
- At rest it is closed and neutral.
- It is drawn as a shallow seam with no lips, so the tissue above and below can later deform for speech.

**Jaw.**
- The posterior mandible is deep, and its hinge sits under the temporal platform.
- The lower jaw is the lower half of the same skull, so there is no chin.

**Auricular region.** A recessed opening with a shallow rim on the posterolateral skull. There is no pinna, lobule or point.

**Stature.** The new skull is lower than the old head. The whole body was rescaled about 2.6% so that standing height stays 188 cm. The tail stays at 128 cm (68%).

**Front-view check (bare geometry).** These features carry the identity without scales, pupils or tail:
- a broad flat-topped skull;
- an orbital platform with eyes on its corners;
- the rostral wedge;
- a wide jaw line with no nose, lips or chin.

## Fingers and toes

**Fingers and thumb.**
- The distal phalanges now taper to a point before the claw starts: about 55% radius reduction toward the tip, plus a small extension.
- Each claw continues the digit's own axis from the tapered tip, rather than sitting on the back of a human fingertip.
- Claws are short to moderate (about 1.6 cm), pointed and slightly curved down.
- Five digits and the opposable thumb are kept.

**Toes.**
- The same principle applies, slightly more robust.
- Each toe tapers toward its tip, with a claw of about 1.5 cm continuing the toe axis forward and down.
- The foot stays broad and plantigrade, with a longer forefoot.

No gameplay meaning is attached to the claws.

## Unchanged (accepted, holding)

These are carried over as accepted:
- body architecture;
- sacral sculpt and tail-base integration;
- the complete 128 cm tail;
- Regional Scale Architecture (the new head has its own fine and structural fields);
- vertical pupils.

## Known limits, for the reviewers

1. **Head is a procedural blockout.** The new head comes from a signed-distance blockout, not a hand sculpt. Proportions and architecture are the point of this pass; surface refinement is not.
   - The snout tip still reads somewhat bulbous head-on.
   - The orbital mounds are simple.
2. **Neck join.** The head joins the body neck through a blended band below a cut plane. A faint join line and a slight thickening remain at the base of the throat. The neck also reads thicker than in Targeted Sculpt 1.
3. **Nictitating membrane.** It is still not rendered; this renderer has no translucency. The identity decision is unchanged.
4. **Mouth.** No inner mouth or teeth are modeled yet. The seam is a closed-mouth reference only.

## Spec/model conflicts

None found. No spec was edited.

Saurin is not declared final. This is returned for Tyler/ChatGPT visual approval.
