# Saurin Targeted Sculpt 3 — Head, Orbit, Jaw, Neck, Hands and Feet

**Author:** Claude
**Responds to:** `reviews/claude-saurin-targeted-sculpt-3-directive.md`
**Status:** DIAGNOSTIC, NOT FINAL. Returned for Tyler/ChatGPT review.
**Scope:** Saurin head and distal anatomy only. Body, tail, scale architecture, Gorrund and all other races are untouched. No spec edits, no Pass 2 work, no UE5 work.

## Tyler's decision on method

Tyler chose this route on October 1, 2026: script fixes now, then a hand-sculpt pass.

The head is still procedural, built from a signed-distance construction. That approach can address the directive's structural points, but I don't expect it to reach the "close photorealistic dialogue shot" bar in Section D on its own. That level of surface needs hand sculpting, with these files as its base. Sculpt 3 is therefore a corrected structural base, not a candidate final head.

## Deliverables (both sexes)

All images are in `reviews/images/targeted-sculpt-3/` and are labelled DIAGNOSTIC, NOT FINAL.

| # | Requested item | File |
|---|---|---|
| 1 | Bare head geometry | `saurin3_{Masc,Fem}_head_bare.jpg` |
| 2 | Final-reference head | `saurin3_{Masc,Fem}_head_final.jpg` |
| 3 | Sculpt 2 vs Sculpt 3, same camera, scale and lighting | `saurin3_{Masc,Fem}_head_comparison.jpg` |
| 4 | Orbit closeups (front, 3/4, profile) | `saurin3_{Masc,Fem}_orbit.jpg` |
| 5–6 | Jaw closeups and head/neck integration to the upper chest | `saurin3_{Masc,Fem}_jaw_neck.jpg` |
| 7–8 | Hands (front, palm, back, side) and feet (front, profile, 3/4) | `saurin3_{Masc,Fem}_hands_feet.jpg` |
| 9 | Whole-body true scale with the complete tail | `saurin3_{Masc,Fem}_true_scale.jpg` |

## What changed

**Orbits (A1).**
- The eyes are seated lower and further back, inside a bony orbital frame.
- That frame is built from a supraorbital ridge, a postorbital bar running down to a jugal arch, and a lid rim continuous with the skull.
- The aperture is almond-shaped.
- Gaze is still forward-readable, with vertical pupils and no scowl.

**Rostrum (A2).**
- The dorsal and upper-lateral rostrum now has planar transitions from the orbital platform, blending into rounded jaw sections.
- The tip is a little narrower.
- The broad root and the projection floor are kept.

**Jaw and oral margin (A3).**
- The seam now follows a curve that rises at the rictus under the jugal arch, and its width varies along the jaw.
- Low supralabial and infralabial ridges run beside it, with no lips and no chin.
- The upper jaw overhangs a slightly narrower lower jaw.
- A quadrate/hinge mass and the mandibular angle sit under the temporal platform.
- The mouth stays closed and neutral, with no teeth added.

**Cranial roof and posterior skull (A4).**
- The vault is slightly lower.
- Jaw-closing muscle volume sits behind the orbit.
- The occiput continues into the neck.

**Neck (A5).**
- The neck column now tapers toward the skull.
- A dorsal nuchal mass and a gular (throat) slope tie the jaw to the neck.
- Posture is still upright.

**Hands (B).**
- Claws are 15% shorter (1.6 → 1.35 cm).
- The tapered distal phalanges and the claws continuing the digit axis are kept.

**Feet (C).**
- The forefoot is longer by about 2 cm.
- Each toe is longer, tapers about 55%, and has visible joint constrictions at two segment points.
- Claws continue the toe axes.
- The plantar contact surface is held flat, so the foot stays plantigrade, with no webbing and no talons.

## Self-check against Section F (my honest read)

| Gate | Result |
|---|---|
| Human with a reptile muzzle? | **Pass.** No human structure remains. |
| Cartoon or gecko mascot? | **Partial.** Sculpt 3 is less mascot-like than Sculpt 2, but the forms are still simplified. |
| Eyes housed rather than perched? | **Mostly pass.** The orbital frame and lid rim now enclose the eye. |
| Ruler-straight mouth? | **Partial.** The seam now curves and varies in width, but it still reads clean and diagrammatic in profile. |
| Bulbous rostral tip? | **Partial.** It is improved in profile, but is still rounded head-on. |
| Neck a cylinder? | **Partial.** The taper, nuchal mass and throat help, but the neck is still thick and tubular from the front. A faint join line remains at its base. |
| Hands regress? | **Pass.** |
| Foot still a human foot with claws? | **Improved.** The toes are clearly separate and segmented, but the heel and arch are still the base mesh's. |
| Bare head recognizable as Saurin? | **Pass.** |
| Holds up in a close photoreal dialogue shot? | **Fail.** This needs the hand-sculpt pass Tyler chose. |

## Proposed next step

Use the Sculpt 3 `.blend` as the base for a hand-sculpt pass on these areas:
- head surface;
- rostral tip;
- oral margin;
- neck and throat;
- heel and arch.

The structural relationships above stay as the guide. I didn't start that pass; it waits for Tyler and ChatGPT to review this one.

## Spec/model conflicts

None found. No spec was edited.
