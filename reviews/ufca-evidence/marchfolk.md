> UFCA Phase 1 evidence appendix to `reviews/claude-ufca-01-requirements-matrix.md`. Line references are to the canonical race spec as of commit c076294. Extraction only: no canon is changed, and nothing here is new anatomy. Tags: [ANAT] anatomical requirement · [CTRL] creator-facing control requirement · [VAL] dependency/validator · [PRES] presentation · [DIAG] measurement/diagnostic · [OPEN] open/not authorized.

# UFCA-01 evidence: Marchfolk facial / craniofacial extraction

Source: `specs/marchfolk/MARCHFOLK_V1.md` (332 lines, read in full). Citations are `§section Lnnn` from that file unless prefixed `PR` (= `decisions/PROJECT_RULES.md`). Project-rules context is kept in its own section at the end and is not merged into spec claims.

Spec structure relevant to the face: v1.0 (L7–43), v1.2 facial anatomy (L98–143), v1.3 skin/hair (L145–189), v1.4 age/presets (L191–231), v1.5 validation (L233–269), Consistency Resolution Part 1 (L271–288), Part 2 pigmentation/ears/lifecycle/ancestry (L290–333).

Marchfolk are the **primary Human Reference Population** (v1.0 §1–3 L13–15; Part 1 §6 L282). Most facial content is functional/organizational rather than tendency-based. The spec gives no numeric facial ranges.

---

## 1. Cranial vault / cranial proportions
- [ANAT] Marchfolk keep "recognizably human skeletal and cranial architecture … face …, with variation inside believable human boundaries" (v1.0 §1–3 L15).
- [ANAT] They serve as the grounded reference for judging other races' "craniofacial anatomy" (v1.0 §1–3 L15). This "doesn't make Marchfolk the default anatomy for every humanoid race" (L15).
- [CTRL] There is a "head and skull" detailed region (v1.2 §2 L116). The spec lists no sub-controls for it.
- [ANAT] "Edits keep believable relationships between neighboring features and the underlying skull" (v1.2 §2 L116).
- [VAL] Body-relationship constraint covers "head and body" (v1.0 §9–11 L31).
- [VAL] The face validation row includes "Cranial relationships, face width and length" (v1.5 §2–6 L248).

## 2. Forehead
- SILENT. No forehead item. Forehead could fall under "head and skull" (L116), but the spec does not say so.

## 3. Brow / supraorbital
- [CTRL] There is a "brow and eyes" detailed region (v1.2 §2 L116).
- [CTRL] Brow height has an independent left/right asymmetry adjustment (v1.2 §3 L120).
- [VAL] The face validation row includes "brow" (v1.5 L248).

## 4. Orbit
- [VAL] The face validation row includes "orbits and eyes" (v1.5 L248). No other orbital anatomy is given.

## 5. External eye (aperture, lids, canthi, folds)
- [CTRL] "Eye opening" has an independent left/right asymmetry adjustment (v1.2 §3 L120).
- [ANAT] Age affects "under-eye anatomy" (v1.2 §4 L124), and adult aging may affect the "eye region" (v1.5 §7–8 L253).
- Lids, canthi and folds: SILENT.

## 6. Ocular anatomy
- [ANAT] Valid iris families are "Brown, dark brown, hazel-like, amber where appropriate, green, gray, blue, related grounded intermediates" (Part 2 §1–2 L301). This is AGREED (L294).
- [OPEN] Exact Marchfolk frequencies are OPEN (L303).
- [VAL] Locked: "Validity isn't frequency" (L303).
- [ANAT] "Ocular biology" is named as a category that Halvren inheritance must address (Part 1 §9 L286). This is a pointer only, with no content.
- Sclera, pupil, nictitating membrane, low-light vision and the magical-versus-biological distinction: SILENT.

## 7. Cheek / zygomatic
- [CTRL] There is a "cheeks" detailed region (v1.2 §2 L116).
- [CTRL] Cheek fullness has a left/right asymmetry adjustment (v1.2 §3 L120).
- [ANAT] Age affects "cheek fullness" (v1.2 §4 L124).
- [VAL] The face validation row includes "cheeks" (v1.5 L248).

## 8. Midface
- [VAL] The face validation row includes "midface" (v1.5 L248). The spec has no midface control region (the seven regions at L116 do not name it).

## 9. Nasal anatomy
- [CTRL] There is a "nose" detailed region (v1.2 §2 L116).
- [VAL] The face validation row includes "nose" (v1.5 L248). No sub-controls are listed.

## 10. Mouth / lips
- [CTRL] There is a "mouth and lips" detailed region (v1.2 §2 L116).
- [CTRL] Mouth corner position has a left/right asymmetry adjustment (v1.2 §3 L120).
- [VAL] The face validation row includes "mouth and lips" (v1.5 L248).

## 11. Jaw / mandible
- [CTRL] There is a "jaw and chin" detailed region (v1.2 §2 L116).
- [CTRL] Jaw contour has a left/right asymmetry adjustment (v1.2 §3 L120).
- [ANAT] Age affects "jawline definition" (v1.2 §4 L124) and the "jawline" (v1.5 L253).
- [VAL] The face validation row includes "jaw" (v1.5 L248).

## 12. Chin
- [CTRL] Chin falls in the "jaw and chin" region (v1.2 §2 L116).
- [VAL] The face validation row includes "chin" (v1.5 L248).

## 13. External ear / auricular
- [ANAT] AGREED: "ordinary human external-ear anatomy within broad natural variation: coherent skull attachment, auricular base or root, helix, antihelix, concha, tragus and antitragus region, lobe, projection, vertical orientation and curvature" (Part 2 §3–4 L307).
- [ANAT] Ears vary in "ear length and breadth, lobe size and attachment, projection from the skull, vertical position, angle, curvature and natural asymmetry" (L307).
- [ANAT] They "don't naturally have the elongated, tapered non-human elven ear architecture" (L307).
- [VAL] Locked: "human and elven ears aren't 'pointiness 0% versus 100%.' They're different architectures …, and mixed ear inheritance is never solved by linearly interpolating one pointiness slider" (L307).
- [CTRL] There is an "ears" detailed region (v1.2 §2 L116).
- [CTRL] Ear projection has a left/right asymmetry adjustment (v1.2 §3 L120).
- [VAL] The face validation row includes "ears" (v1.5 L248).

## 14. Teeth / dentition
- SILENT.

## 15. Race-specific cranial displays / keratin / horns
- N/A. SILENT (none stated).

## 16. Skin/surface structures that materially alter facial anatomy
- SILENT. The spec lists no surface structure that alters facial anatomy.
- Related, non-anatomical items:
  - [PRES] Skin Appearance Layers are Natural / Environmental / Applied / Acquired (v1.3 §1 L149–158; Part 1 §7 L283).
  - [PRES] Markings and scars use a placement system that "respects anatomical regions" (v1.3 §4 L181).
  - [ANAT] Valid skin pigmentation and undertone families are listed (Part 2 L298–299).

## 17. Natural asymmetry
- [CTRL] Detailed controls give "Subtle independent left and right adjustment" of brow height, eye opening, cheek fullness, mouth corner position, ear projection and jaw contour (v1.2 §3 L120).
- [CTRL] Asymmetry "stays subtle by default, and a restore-symmetry option is included" (L120).
- [CTRL] Optional asymmetry belongs to the Detailed level (v1.2 §1 L112).
- [ANAT] Ears show natural asymmetry (Part 2 L307).
- [VAL] The face validation row includes "natural asymmetry" (v1.5 L248).

## 18. Age-related facial change (and age triad)
- [ANAT] Age affects "facial structure, volume, skin elasticity, wrinkles, under-eye anatomy, cheek fullness, jawline definition, neck structure and hair", and "Age changes keep the face recognizably the same person" (v1.2 §4 L124).
- [CTRL] The creator covers adults only. Age is "a continuous adjustment, not only fixed categories" (v1.4 §2 L206).
- [PRES] Visual reference points are young adult, mature adult, middle-aged, older adult and elder (L206).
- [ANAT] Age affects facial volume, skin elasticity, hair color and density, "while keeping the character recognizable" (v1.4 §2 L208).
- [VAL] "Adult aging must do more than wrinkles and gray hair, and may affect facial volume, skin elasticity, eye region, jawline, neck, hair density and pigmentation … with exact implementation later" (v1.5 §7–8 L253).
- Age triad (Part 1 §8 L284):
  - [VAL] **Chronological age**, **apparent biological age** and **age presentation** "all … stay distinct".
  - Earlier v1.4 L208 ("actual age and apparent age are separate") is refined by Part 1 L284.
- [OPEN] Lifecycle numbers are "E, OPEN" (Part 2 §5–6 L311).

## 19. Sex-related facial tendency
- SILENT on any sex-related facial tendency.
- The spec's only sex statements are body-level:
  - Biological anatomy layer "including relevant sex-related characteristics" (v1.0 §12–14 L35).
  - "no hard sex-specific height restriction" (v1.0 §4–5 L23).
- No R-SEX reference appears in the spec (see project-rules context below).

## 20. Facial hair biology (incl. eyebrows)
- [PRES] Facial hair is in the Personal Presentation layer (v1.0 §12–14 L35).
- [CTRL] Facial hair has "its own style, length, density and color controls". Its color is linked to hair color by default and can be unlinked (v1.3 §3 L177).
- [ANAT] Natural hair-color families are listed (Part 2 L300). "Age-related depigmentation stays separate" (L300).
- [VAL] Facial hair is included in skin/hair validation combinations (v1.5 L253).
- Facial-hair biology as anatomy: SILENT. Eyebrows: SILENT.

## 21. Inherited / mixed development
- N/A (Halvren only).
- Pointers in this spec that constrain Halvren:
  - The ear architecture rule (L307).
  - The inheritance-layer requirement naming "ocular biology, external ears" (L286).
  - "Never … 50/50" (L324).
  - Ancestry scope (L315–320).

## 22. Locked validation tests touching the face
The spec has no test IDs. Named tests and locks:
- [VAL] Stage B "facial and individual identity (broad diversity without one preferred face)" (v1.5 §1 L239).
- [VAL] Face test: covers cranial relationships through natural asymmetry, "not optimized only for conventionally attractive faces" (v1.5 L248).
- [VAL] Identity stress: "fails if generation keeps producing one face with minor tweaks, one attractive template … one age, one pigmentation family or one hair type" (v1.5 L249).
- [VAL] Age validation: aging must do more than wrinkles and gray hair (v1.5 L253).
- [VAL] Preset round-trip "Preset, Advanced Mode, Edit, Save, Reload without unexpected change" (v1.5 §9–13 L257).
- [VAL] Randomization sample test covers validity, diversity, convergence and locks (L257).
- [VAL] Locked: ears are not a "pointiness" slider (Part 2 L307).
- [VAL] Locked: "Validity isn't frequency" (L303).
- [VAL] Combined-validity rule: "Individually valid controls can still create an invalid combined body" (v1.0 L31; v1.5 L247). This is body-scoped, but head/body is included.

## 23. Explicitly OPEN biology touching the face
- [OPEN] Pigmentation frequencies, including iris (Part 2 L303, L332).
- [OPEN] Lifecycle numbers: lifespan, maturation and senescence (L311, L332).
- [OPEN] Morph-target architecture "not finalized" (v1.2 L100). Technical architecture is unchosen (v1.0 §18 L43; v1.5 §19–20 L265).
- [OPEN] Saved appearance schema implementation (L257).
- [OPEN] Race-level biological gameplay differences (L39).
- [OPEN] Mixed-ancestry genetic model / trait dominance (L324, L332).

## 24. Pass 1 provisional creator-control list for the face
Classification (L102): **"APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION"**. These are "not the final universal facial-control hierarchy", "never constrain later races", and are reconciled in the UFCA Review.

- [CTRL] Three levels using the same character data (v1.2 §1 L106–112):
  - Face presets: "Curated starting faces showing meaningful variation in human facial anatomy".
  - Quick controls: "Accessible adjustments to the major features".
  - Detailed controls: "Detailed regional controls, anatomical proportions and optional asymmetry".
- [CTRL] Seven detailed regions (v1.2 §2 L116): head and skull; brow and eyes; nose; cheeks; jaw and chin; mouth and lips; ears.
- [CTRL] Asymmetry pairs (L120): brow height, eye opening, cheek fullness, mouth corner, ear projection, jaw contour, plus restore-symmetry.
- [CTRL] Facial hair: style, length, density and color, with color linked or unlinked (v1.3 §3 L177).
- [CTRL] Hair: style, length, texture, color, hairline, density, parting and accessories (v1.3 §2 L164–171).
- [PRES] Player experience features (v1.2 §5 L130–135): before/after comparison, undo/redo, lighting previews, expression previews, front/side/three-quarter views, zoom and free rotation.
- [VAL] Technical compatibility: facial animation, speech, expressions, age morphs, skin materials, presets, saving, headwear and UE5 performance (v1.2 §7 L143).
- No master facial slider is explicitly forbidden. The analogous body rule is "without a single thin-to-heavy slider" (v1.1 §4 L68).
- Universal facial sub-controls are not enumerated (the Skarn spec enumerates them).

## 25. Prohibited / forbidden controls and anti-patterns
- [VAL] The face must not be "optimized only for conventionally attractive faces" (v1.5 L248). The identity-stress test fails on "one face with minor tweaks, one attractive template" (L249).
- [VAL] Ear inheritance must not be a "pointiness 0% versus 100%" slider and must not use linear interpolation (Part 2 L307).
- [VAL] Body anti-patterns: avoid "disconnected morph targets, excessive mesh stretching and implausible combinations" (v1.1 §6 L81).
- [VAL] Height must not be uniform scaling (v1.0 L23).
- [VAL] Randomization must not converge on "one default fantasy human" (v1.0 §15–17 L39).
- [VAL] Presets must have no hidden models and no preset-only features (v1.4 §3 L212). No hidden geometry (v1.5 L257).
- [VAL] Dragon's Dogma 2 is never a source of copied assets or UI (v1.2 §6 L139).
- [VAL] Marchfolk are not "one idealized fantasy-human body" or "one ethnicity or phenotype" (v1.0 L13).
- [PRES] Weathering and scars are never forced by class or occupation (v1.3 §5 L185).

## 26. Positive identity statement for the face
- "They represent the breadth of believable human physical diversity, not one idealized fantasy-human body … highly variable, with broad body, facial and pigmentation diversity" (v1.0 L13).
- "Marchfolk keep recognizably human skeletal and cranial architecture … face, skin and hair biology … with variation inside believable human boundaries" (L15).
- "The priorities are realistic human variation, believable anatomy, expressive faces, natural asymmetry and meaningful individuality" (v1.2 §6 L139).
- Identity stress requires "Clearly different people who are still biologically human" (v1.5 L249).
- Note: Marchfolk identity is breadth, not a neutralization-surviving distinct feature. The spec defines no neutralization test for Marchfolk.

## 27. Cross-population facial boundary tests / comparators
- [VAL] Marchfolk are the comparator for other races' craniofacial anatomy (L15; Part 1 §6 L282).
- [VAL] The human-versus-elven ear architecture distinction (L307).
- [ANAT] Ancestry families: Human = Marchfolk, Skarn, Sagekin; "Human never equals Marchfolk". Elven = Fenn, Aelari, Vael (Part 2 §7–9 L315–318).
- Marchfolk has no named cross-population facial test of its own. Comparative tests are carried by the other race specs.

## 28. Measurement-deferred items (RM-*)
- None. No RM-* references in the spec.
- "Exact mass calculation is a future problem" (L31) is body-level only.

## 29. Presets / randomization / Simple-Advanced statements touching the face
- [CTRL] Simple = Race, Preset, Confirm. Advanced = Race, Preset, Customize, Confirm (v1.0 L39; v1.4 §4 L223).
- [CTRL] Face presets are a facial editing level (v1.2 §1 L110).
- [CTRL] Presets "vary in … age, face, skin, hair, markings" and are fully reproducible in the standard customizer (v1.4 §5 L227).
- [PRES] Preset themes are Frontier Settler, Traveling Scholar, Veteran Soldier, Rural Laborer, Merchant and Elder Wanderer. These are not classes (v1.4 §3 L212–219).
- [CTRL] Randomization is full or selective, with locks, race-aware validity and reproducibility (v1.0 L39).
- [CTRL] Target operations include randomizing face, body, or hair and presentation only, and preserving "age, frame, selected facial traits" (v1.5 L257). The UI is undesigned.
- [VAL] One unified conceptual appearance record covers preset, custom, random and NPC characters (L257).

## Project-rules context (decisions/PROJECT_RULES.md; not spec claims)
- PR L31–33: race-specific facial control organizations are APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION. "Do not delete them." The UFCA Review follows all 13 races.
- PR L39: the UFCA Review is the next authorized phase and uses `reviews/claude-pass2-r3-craniofacial-framework.md` as its measurement framework (not creator controls).
- PR L42–50: authority order puts race specs above PROJECT_RULES. "Terminology normalization never rewrites a race's positive anatomical identity."
- PR L54: unqualified "human" means Marchfolk HRP at matched normalized height. PR L55: "near-human" means within the Marchfolk adult envelope at normalized height.
- PR L56: "Baseline" is retired as a comparator term.
- PR L16: the age triad is restated.
- PR L65–71: R-SEX. Bounds are available to either sex unless race canon says otherwise, and sex never forces face "unless explicit race canon defines a tendency". "'No shift' is a valid complete state." The Marchfolk spec defines no facial sex tendency.

## Extraction notes
- Facial content is mostly organizational (levels, regions, asymmetry, previews) and validation lists. There are no facial anatomical tendencies (expected for the reference population) and no numbers.
- The v1.2 seven regions omit "forehead", "orbit" and "midface", but the v1.5 face test (L248) names orbits and midface. Validation coverage is therefore broader than the region list. Treat this as a coverage gap, not a contradiction.
- The age wording in v1.4 L208 ("actual age and apparent age") is refined by Part 1 §8 L284 (three-way triad).
- Part 1 corrects only frame/Athletic wording in v1.1/v1.4, with no facial impact.
- The richest biological facial content is in Part 2: ear architecture (L307) and iris families (L301).
- No asymmetry for nose or eyes beyond "eye opening" is stated.
