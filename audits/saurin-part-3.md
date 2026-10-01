# Audit: Saurin v1.0 Part 3, Surface phenotype, integument, eyes and extremity detail

**Auditor:** Claude
**Audited file:** `specs/saurin/SAURIN_V1.md` §§78–125 at commit `cc36c85`
**Request:** `reviews/saurin-part-3-audit-request.md` (`ba5d00f`)
**Compared against:**
- Saurin Parts 1–2 (accepted)
- `rules/character-creation-brief.md` §3–4, §16.13
- `decisions/PROJECT_RULES.md`
- `register/decision-register.md`
- the approved surface sections of Pipkin and Cogling

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS WITH CLARIFICATIONS.** Regional Scale Architecture is a real positive system, not a texture. It has three field types:
- structural fields where the body deforms little
- articulation fields at joints
- fine expressive fields on the face

It also has an integrated ventral field. Scale size is coupled to region (§85), so no single global slider can break it.

Strengths:
- Pigmentation is broad and explicitly not "green lizard" (§87–88).
- Patterns follow body topology and carry no culture or morality (§90–93).
- The horn, frill, venom and hair firewalls are clean (§100–103, §110, §116–117).
- Claws preserve grasp and the plantigrade stance (§104–106).
- The tongue is correctly left OPEN rather than defaulting to forked (§108).
- Tail surface integration is mandatory (§114).
- Tyler's tail rule is kept to racial validation, with garment coverage and injury OPEN (§113, §115). That resolves my Part 1 re-audit note 2.
- Presets are demonstrations, not subraces (§120).

There's no blocking contradiction. Two items should be fixed before acceptance:
- **4a.** The body surface isn't mapped to the AGREED Skin Appearance Layers. Pipkin and Cogling were both corrected for this.
- **4b.** Part 1 deferred the palm and sole surface to this part, and Part 3 doesn't deliver it.

Two clarifications are recommended: 4c and 4d.

## 2. The twenty-one requested checks

| # | Check | Result |
| --- | --- | --- |
| 1 | Regional Scale Architecture is positive and coherent | PASS (§79–80, §85) |
| 2 | Structural, articulation, fine expressive and ventral fields are separated | PASS (§81–84) |
| 3 | Morphology supports motion and expression, not armor or plastic | PASS (§82, §86, SAU-SURF-03, 06) |
| 4 | Broad pigmentation, no green default | PASS (§87–89, SAU-SURF-08) |
| 5 | Topology-aware inherited patterns vs presentation | PASS (§90–92, §118, SAU-SURF-21) |
| 6 | Vertical pupils without a sinister read | PASS on the firewall (§95, §99). Rationale in 4c |
| 7 | Nictitating membrane without aquatic or sensory gameplay | PASS on the firewall (§98–99). Rationale in 4c |
| 8 | Low-profile ridges vs horns and dragon silhouette | PASS (§100–102, SAU-SURF-14). Domain question in 4d |
| 9 | No baseline large frills | PASS (§103) |
| 10 | Claws preserve grasp and plantigrade stance | PASS (§104–106, SAU-SURF-15, 16). Palm and sole surface missing (4b) |
| 11 | Tongue left OPEN | PASS (§108) |
| 12 | Venom firewall | PASS (§109–110, SAU-SURF-26) |
| 13 | Aging, scarring and renewal | PASS (§111–113). Minor note in 4e |
| 14 | Mandatory tail surface integration | PASS (§114, SAU-SURF-10, 22) |
| 15 | Visible-tail rule limited to validation; garments and injury OPEN | PASS (§113, §115) |
| 16 | No mammalian hair or facial hair | PASS (§116–117). Creator note in 4e |
| 17 | FD domain separation | Partly. Facial mapping PASS (§122); body surface missing (4a) |
| 18 | Randomization and presets create no cultures or subraces | PASS (§119–120) |
| 19 | SAU-SURF-01 to 26 | Good. Additions in 4b and 4e |
| 20 | No automatic armor, venom, perception, climbing or combat | PASS (§81, §99, §104, §110, §125) |
| 21 | No UE5 | PASS |

## 3. Contradictions

There's no design contradiction with Parts 1–2 or the brief. §122 conflicts with an AGREED register rule by leaving the body surface unmapped (4a).

## 4. Findings

### 4a. Body surface isn't mapped to the Skin Appearance Layers (should be fixed before acceptance)

The register (AGREED, from Pipkin Part 4) says FD domains are for facial analysis only, and **whole-body surface uses the Skin Appearance Layers (Natural, Environmental, Applied or Acquired)**. Cogling Part 4 was flagged for the same gap and fixed it in §132.

Part 3 is almost entirely whole-body surface: scales, pigment, patterns, claws, the tail surface, scars and aging. But §122 maps only the FD domains, and FD-SURF is written as if it covered body scales and patterns.

**Recommended:** add a short section, following the Cogling §132 pattern:
- **Natural:** scale architecture, pigmentation, inherited patterns, claw keratin, ridges and age-related surface change.
- **Environmental:** dirt, wetness, abrasion, sun and weathering. This is distinct from FD-OBS lighting.
- **Applied or Acquired:**
  - Applied: paint, dye, cosmetics and claw treatment (§118)
  - Acquired: scars, damaged scale fields, chipped claws and damaged ridges (§113)

State that FD domains apply to the face only, and that §122's FD-SURF is the facial part of the Natural layer.

### 4b. Palm and sole surface isn't delivered (should be fixed before acceptance)

Part 1 §15 listed "pad/sole organization" as one of the carriers that make Saurin feet non-human, and deferred surface anatomy to a later part (§16, §18). Part 3 assigns scale fields to the dorsal hands and feet (§81) and to finger and toe joints (§82), and it adds claws. It never says what the **palms and soles** are.

That surface matters for:
- grip and weapon handling (brief §9 compatibility)
- footwear and plantigrade contact
- the hand closing in first-person view

It's also where a uniform-scale default would look most wrong.

**Recommended:** give palmar and plantar surfaces a positive description. One option is finer, flexible, pad-like contact surfaces, distinct from the dorsal scale fields. Either state that this is the first-pass direction or mark the details OPEN. Add SAU-SURF-27, a grip and stance contact test: closed fist, weapon grip and planted foot, with the surface remaining plausible.

### 4c. Pupils and nictitating membrane: say why they were chosen (clarification)

Part 2 §45 said the membrane "cannot be assumed from 'reptilian.'" Part 3 now approves it, with the rationale "an additional protective ocular closure," and calls vertical pupils "a positive sensory phenotype."

The request asked me to flag traits combined only because they're reptilian:
- In real animals, vertical slit pupils correlate mainly with ambush hunters whose eyes sit low to the ground. Tall, upright animals with forward-facing eyes tend to have round or horizontal pupils.
- Combined on a 188 cm upright biped, the slit is not a biological consequence of the approved body.

That's acceptable in fantasy, and slit eyes are a strong part of the Iksar heritage in brief §16.13. But calling it "sensory" invites a sensory gameplay reading that §99 then has to deny.

**Recommended:** record vertical pupils and the membrane as **identity choices** that support the Iksar-inspired eye read, not as derived sensory adaptations. The firewalls stay as written. If ChatGPT prefers a biological rationale, that's fine; the point is that "reptilian" alone doesn't justify the choice.

### 4d. Which domain the keratinous ridges belong to (clarification)

§100 calls the ridges "continuous with the integument **and underlying cranial architecture**," while §122 puts them in FD-SURF.
- If a ridge has a bony base, it's FD-STRUCT, and neutralizing the surface wouldn't remove it.
- If it's keratin over an unchanged skull, it's FD-SURF.

This affects SAU-SURF-19 and 25 and the Part 2 surface-neutral test.

**Recommended:** state which it is. Integumentary keratin over the approved skull, perhaps with a slight underlying bony rugosity, is the simplest choice and keeps Part 2's FD-STRUCT closed.

### 4e. Minor, non-blocking

- **Gaze readability.** §94 leaves sclera visibility open. Combined with slit pupils, low sclera visibility can make gaze direction hard to read in dialogue. Add a validation case alongside SAU-FACE-23: dialogue at conversation distance, with gaze direction readable.
- **Thermoregulation.** "Cold-blooded" is the most common assumption players make about reptile races. The spec doesn't mention metabolism or thermoregulation anywhere. Add it to §124 OPEN with the usual line: no automatic cold vulnerability or heat bonus.
- **Creator categories.** The brief's Individual layer and the Randomize options include "Hair," and Presentation includes hairstyles and facial hair. Note that for Saurin these categories are empty or replaced by the ridge and surface controls, so the creator doesn't show empty or human options.
- **Occupational wear.** The brief lists calluses as occupational appearance. §113 covers scars but not the scaled equivalent of a callus, such as thickened or worn scales on grip or knee-contact areas. One line under Acquired (4a) would cover it.
- **Ventral wording (§84).** "More regular transverse organization" is literally how a snake or crocodile belly is organized, and the next line says it isn't one. Suggest adding "without continuous belly-scute plating" so the intended difference is stated.

## 5. Cross-race summary

| Race | Status |
| --- | --- |
| All races | Overlapping pigmentation doesn't make populations interchangeable (§121). Anatomy carries race (SAU-SURF-05, 19, 25) |
| Grask | Brief: "thick textured skin." Saurin scales are a separate regional keratin system, so there's no conflict |
| Vael | The cool gray and blue-gray families overlap, as §121 permits |

## 6. Completion recommendation

1. ChatGPT patches 4a (Skin Appearance Layers) and 4b (palms, soles, SAU-SURF-27).
2. Recommended alongside: 4c, 4d and 4e.
3. I re-audit.
4. On a PASS and Tyler's approval, Part 3 is accepted.

Part 4 should not begin until then.
