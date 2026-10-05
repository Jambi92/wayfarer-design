> UFCA Phase 1 evidence appendix to `reviews/claude-ufca-01-requirements-matrix.md`. Line references are to the canonical race spec as of commit c076294. Extraction only: no canon is changed, and nothing here is new anatomy. Tags: [ANAT] anatomical requirement · [CTRL] creator-facing control requirement · [VAL] dependency/validator · [PRES] presentation · [DIAG] measurement/diagnostic · [OPEN] open/not authorized.

# UFCA-01 evidence: Skarn facial / craniofacial extraction

Source: `specs/skarn/SKARN_V1.md` (376 lines, read in full). Citations are `§section Lnnn` from that file unless prefixed `PR` (= `decisions/PROJECT_RULES.md`) or `MF` (= Marchfolk spec, only where the Skarn spec itself points to it). Project-rules context is kept in its own section at the end.

Spec structure relevant to the face: v1.0 §8 Face (L46–48), v1.2 facial anatomy (L139–191), v1.3 skin/hair (L193–247), v1.4 presets/validation (L249–311), v1.5 handoff (L313–376).

Skarn are "biologically human: a naturally larger, heavier, more powerfully built population than Marchfolk … not scaled-up Marchfolk" (v1.0 §1 L7). Facial content is tendencies only. The spec gives no numeric facial ranges.

---

## 1. Cranial vault / cranial proportions
- [ANAT] Central tendency (not requirement): "a slightly larger, more robust skull suited to body size" (v1.2 §1 L147). These are "tendencies, not requirements" (L154).
- [CTRL] Head and skull controls to explore: "Head width, depth and length, cranial height, forehead height and slope, temple width, face length" (v1.2 §3–6 L168).
- [VAL] The head must be "Believable from front, profile and three-quarter views" (L168).
- [ANAT] "body scale sets head-to-body proportion" (v1.2 §7 L175). This is a proposed universal principle, pending validation.
- [ANAT] Height changes keep believable head and torso relationships. Height is never uniform scale (v1.0 §6 L40).
- [ANAT] v1.0 deferred: "Detailed craniofacial ranges come in a later spec" (v1.0 §8 L48). v1.2 then supplies tendencies, not numeric ranges.

## 2. Forehead
- [CTRL] "forehead height and slope" falls in the head and skull region (L168).
- No Skarn forehead tendency is stated (beyond the skull/brow items).

## 3. Brow / supraorbital
- [ANAT] Tendency: "a somewhat stronger brow" (v1.2 §1 L148).
- [CTRL] "Brow prominence, shape and height" (L169).
- [ANAT] Brow is "Somewhat stronger brow on average, never mandatory" (L169).
- [ANAT] "There are no mandatory square jaws, heavy brows or facial hair" (v1.0 §8 L48). "Skarn are not all square-jawed, heavy-browed …" (L154).

## 4. Orbit
- [CTRL] "eye depth, spacing" falls in the brow and eyes region (L169).
- No orbital anatomy tendency is stated. SILENT beyond the controls.

## 5. External eye (aperture, lids, canthi, folds)
- [CTRL] "eye depth, spacing, size and angle; upper and lower lid shape; lid opening" (L169).
- [ANAT] Age affects "under-eyes" (v1.2 §8 L179).
- [VAL] Expression validation includes blink (v1.2 §10 L187).
- Canthi and folds: SILENT.

## 6. Ocular anatomy
- SILENT. No iris, sclera, pupil or low-light content.
- Pigmentation: "Skarn have full natural human skin-tone variation" (v1.3 §2 L212). That statement is skin only. Eye color is not stated.

## 7. Cheek / zygomatic
- [ANAT] Tendency: "a more substantial mid-face and cheeks" (v1.2 §1 L150).
- [CTRL] "Cheekbone width, height and projection; fullness" (L171).
- [ANAT] "Soft, angular, narrow, broad, youthful and weathered faces all allowed" (L171).
- [ANAT] Age affects "cheeks" (v1.2 §8 L179).
- [ANAT] "Fat can add facial fullness" (v1.2 §7 L175). This is proposed and pending validation.

## 8. Midface
- [ANAT] "a more substantial mid-face" (L150).
- [CTRL] The "Nose and mid-face" region is combined in the control table (L170). No separate midface sub-controls are listed.

## 9. Nasal anatomy
- [ANAT] Tendency: "a somewhat larger nose" (v1.2 §1 L151).
- [CTRL] "Bridge height and width, length, projection, tip width and rotation, nostril width and shape" (L170).
- [ANAT] Nose is "Somewhat larger on average, not a requirement" (L170).

## 10. Mouth / lips
- [CTRL] "mouth and lips" is named as one of the seven regions (v1.2 §2 L158).
- The §3–6 control table has no mouth/lips row. No Skarn mouth tendency is stated.
- [VAL] Expression validation covers smile and speech (L187).

## 11. Jaw / mandible
- [ANAT] Tendency: "more jaw mass" (v1.2 §1 L149).
- [ANAT] Tendency: "a more substantial neck-to-jaw transition" (L152).
- [CTRL] "jaw width, angle and depth" (L171).
- [ANAT] "muscle can affect neck and jaw tissue" (v1.2 §7 L175). This is proposed.
- [ANAT] Age affects "jawline, … neck tissue" (v1.2 §8 L179).
- [ANAT] There are "no mandatory square jaws" (L48, L154).

## 12. Chin
- [CTRL] "chin width, height and projection" (L171).
- No Skarn chin tendency is stated.

## 13. External ear / auricular
- [ANAT] Pass 2 AC-4: "Skarn follow the Marchfolk human-family auricular anatomical foundation (Marchfolk Part 2 §3–4) unless this spec explicitly modifies a tendency. This does not make Skarn head anatomy Marchfolk-equivalent" (v1.2 §2 L160). The Skarn spec modifies no ear tendency.
  - For the pointed-to content, see MF Part 2 L307: human auricle components, variation axes, and the "not pointiness" lock.
- [CTRL] "ears" is named as one of the seven regions (L158). There is no ears row in the §3–6 table.

## 14. Teeth / dentition
- SILENT.

## 15. Race-specific cranial displays / keratin / horns
- N/A. SILENT (none stated).

## 16. Skin/surface structures that materially alter facial anatomy
- SILENT. No anatomical surface structures are stated.
- Related, non-anatomical items:
  - [PRES] Four Skin Appearance Layers (v1.3 §2 L203–210).
  - [PRES] Regional weathering: the face can differ from the hands, for example "heavily callused hands don't force an equally weathered face" (v1.3 §3 L216). This is proposed universal.
  - [PRES] Scar system: type, age, surface (flat/raised/recessed) and placement. It is "cosmetic representation, not medical simulation" (v1.3 §6 L228–235).

## 17. Natural asymmetry
- [CTRL] "Subtle Advanced asymmetry and Restore Symmetry remain" (v1.2 §9 L183).
- [CTRL] Proposed universal **Naturalize Face**: "would add very small, bounded, plausible asymmetries to a very symmetrical face without changing its identity. It isn't final until tested" (L183).

## 18. Age-related facial change (and age triad)
- [ANAT] "Age keeps both Skarn anatomy and the individual face. It affects facial volume, skin elasticity, under-eyes, cheeks, jawline, wrinkles, neck tissue, and hair density and color" (v1.2 §8 L179).
- [ANAT] "Old age is not frailty: older, muscular, imposing Skarn stay possible" (L179).
- [ANAT] "age changes facial volume" (v1.2 §7 L175).
- [VAL] Elder Skarn: "age changes composition while racial anatomy stays" (v1.1 §9 L132). SK-09 Elder (v1.5 L331).
- [VAL] Acceptance: identity survives "advanced age" (L305).
- [VAL] Randomization respects "coherent age" (v1.4 §4 L280).
- Age triad: SILENT in the Skarn spec (see PR L16).

## 19. Sex-related facial tendency
- SILENT. The Skarn spec makes no sex-related statement.
- No R-SEX reference appears in the spec (see project-rules context).

## 20. Facial hair biology (incl. eyebrows)
- [PRES] "facial hair belongs to personal presentation" (v1.0 §8 L48).
- [PRES] "Facial hair is presentation, not racial identity. Clean-shaven Skarn are fully recognizable as Skarn" (v1.2 §11 L191).
- [CTRL] Range runs from "clean-shaven, stubble, or short, full, long or styled and braided beards", with "style, length, density, color and graying controls" (v1.3 §5 L224).
- [VAL] "Skarn identity never depends on it" (L224).
- Facial-hair biology and eyebrows: SILENT.

## 21. Inherited / mixed development
- N/A (Halvren only).

## 22. Locked validation tests touching the face
- [VAL] SK-10 Soft-featured (v1.5 §1 L332).
- [VAL] SK-09 Elder (L331).
- [VAL] SK-11 Neutralized cultural presentation (L333).
- [VAL] SK-12 Valid extreme-randomization result (L334).
- [VAL] SK-01 Reference Skarn (L323).
- [VAL] SK-02 Short Skarn, the Marchfolk height-overlap test (L324).
- [VAL] Expression validation: extreme faces are tested in neutral, smile, anger, surprise, blink and speech. "A face that only looks right in neutral isn't valid" (v1.2 §10 L187).
- [VAL] Silhouette test: neutralize hair, facial hair, tattoos, scars, markings, accessories, clothing and weathering. Skarn "must still read as Skarn" (v1.4 §5 L284).
- [VAL] Equal-height test: 190 cm Marchfolk versus 190 cm Skarn. The Skarn "must stand out by anatomy, not height, beard, clothing or styling" (v1.4 §6 L288).
- [VAL] Anti-stereotype: "soft-featured, clean-shaven, scholarly-presenting …" Skarn all read as the same population (v1.4 §7 L292).
- [VAL] Acceptance criteria (v1.4 §9 L304–311):
  - Identity survives removing presentation (L304).
  - "Facial expressions work across supported faces" (L310).
- [VAL] Relationship-aware randomization includes "body-to-face soft tissue" (v1.4 §4 L280).
- Note: the SK-xx items are "reproducible saved test configurations" (L319). The spec does not call them "locked".

## 23. Explicitly OPEN biology touching the face
- [OPEN] Body-to-face soft-tissue relationships are "pending validation" (v1.2 §7 L175).
- [OPEN] Naturalize Face "isn't final until tested" (L183).
- [OPEN] Morph targets versus alternatives, deformation and serialization are unresolved (v1.5 §10 L376).
- [OPEN] Culture selection is "not final" (v1.3 §9 L247).
- [OPEN] Presentation presets are "Pending design review" (v1.3 §8 L243).
- [OPEN] Height values are provisional, "await visual and technical validation" (v1.0 §2 L15).

## 24. Pass 1 provisional creator-control list for the face
Classification (v1.2 §2 L162): the "same seven regions as Marchfolk" means Skarn "must support at least the facial anatomical coverage represented by the Marchfolk first-pass regions". The final creator "needn't keep seven regions, their names, nesting, UI layout or control grouping". **APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION.** "Race changes the supported ranges, not how the editor works" (L158).

- [CTRL] Seven regions (L158): head and skull; brow and eyes; nose; cheeks; jaw and chin; mouth and lips; ears.
- [CTRL] Controls to explore (§3–6 L166–171):
  - Head/skull: head width, depth and length; cranial height; forehead height and slope; temple width; face length.
  - Brow/eyes: brow prominence, shape and height; eye depth, spacing, size and angle; upper and lower lid shape; lid opening.
  - Nose/mid-face: bridge height and width; length; projection; tip width and rotation; nostril width and shape.
  - Cheeks/jaw/chin: cheekbone width, height and projection; fullness; jaw width, angle and depth; chin width, height and projection.
- [CTRL] Asymmetry and Restore Symmetry (Advanced). Naturalize Face is proposed (L183).
- [CTRL] Facial hair: style, length, density, color and graying (L224).
- [CTRL] Hair: style, length, texture, hairline, density, color, graying and accessories (v1.3 §4 L220).
- [VAL] Body-to-face influence "without overriding facial choices … Players keep independent facial control" (L175).
- [VAL] Cross-race architecture: "facial regions" are shared across races. Each race defines "defaults, valid ranges, anatomical relationships" (v1.5 §8 L366).
- No master slider prohibition is stated for the face.

## 25. Prohibited / forbidden controls and anti-patterns
- [VAL] No mandatory square jaw, heavy brow or facial hair (L48, L154).
- [VAL] Not "angry-looking" by default (L154).
- [VAL] Not scaled-up Marchfolk. "Height is never a uniform whole-body scale" (L7, L40, L73).
- [VAL] Facial hair, cultural hair, tattoos and scars must not carry racial identity (L191, L199, L224, L288).
- [VAL] "Choosing a race never applies cultural markings automatically" (v1.3 §7 L239).
- [VAL] Presentation presets "never replace face, height, frame, biological anatomy …" (v1.3 §8 L243).
- [VAL] "Sliders are never randomized independently … Every result is valid with no manual repair" (v1.4 §4 L280).
- [VAL] "Even extreme Skarn settings must not recreate Gorrund anatomy" (v1.4 §8 L296).
- [VAL] A face valid only in neutral is invalid (L187).
- [VAL] "The goal is neither 13 independent creators nor one generic anatomy forced on every race" (L368).

## 26. Positive identity statement for the face
- "Skarn faces are fully human and diverse" (v1.0 §8 L48).
- "Skarn faces are biologically human. Their identity comes from population ranges and combinations, not mandatory features" (v1.2 §1 L145).
- Central tendency: larger, more robust skull; somewhat stronger brow; more jaw mass; more substantial mid-face and cheeks; somewhat larger nose; more substantial neck-to-jaw transition (L147–152).
- "Their identity comes from underlying anatomy, so a lean, elderly, narrow-framed or high-body-fat Skarn still reads as Skarn" (v1.0 §1 L7).
- "Racial identity survives removing cultural presentation" (L304).
- "Skarn identity survives through anatomy" (v1.5 §9 L372).
- Note: much of the identity is skeletal/body. The face supplies tendencies only.

## 27. Cross-population facial boundary tests / comparators
- [VAL] Marchfolk: silhouette test (L284), 190 cm equal-height test (L288), and Marchfolk/Skarn validation pairs (v1.0 §10 L56–65).
- [VAL] The SK-02 height-overlap test (L324). Cross-race validation (v1.5 §9 L372).
- [VAL] Gorrund: "never differently scaled versions of one anatomy … Even extreme Skarn settings must not recreate Gorrund anatomy" (L296).
- [VAL] Grask: separation is carried by the Grask spec and the Large-Race review. "This pointer adds no Skarn anatomy (Pass 2 AD-5)" (L298).
- "Baseline" in L52 is read as Marchfolk HRP. That item is a breath-holding trait, not facial.

## 28. Measurement-deferred items (RM-*)
- None. No RM-* references in the spec.
- Detailed craniofacial ranges were deferred at L48. v1.2 supplies tendencies but no numbers.

## 29. Presets / randomization / Simple-Advanced statements touching the face
- [PRES] Starting presets: Northern Hunter, Mountain Laborer, Seasoned Traveler, Clan Veteran, Skarn Scholar, Heavyset Merchant, Young Wanderer and Elder Wayfarer (v1.4 §1 L255–262). These are visual inspiration only and fully editable (L264).
- [CTRL] Randomization strength (proposed universal): Subtle, Diverse, Extreme. Extreme is "Possibly for development and testing only" (v1.4 §2 L268–272).
- [CTRL] Selective randomization covers the whole character or only body, face, hair, skin details, markings or presentation. Locks are available, "for example height and face locked" (v1.4 §3 L276).
- [VAL] Relationship-aware randomization includes body-to-face soft tissue and coherent age (L280).
- [PRES] Presentation presets (proposed): Traditional Northern, Traveler, Urban, Veteran and Ceremonial. These never replace the face (L243).
- [VAL] "Presets use standard customization data" (L308).
- Simple/Advanced: SILENT in the spec. Universal amendment v0.1 is referenced (L3). The flow is in PR L8–9.

## Project-rules context (decisions/PROJECT_RULES.md; not spec claims)
- PR L31–33: facial control organizations are provisional. The UFCA Review follows.
- PR L37: Large-Race Comparative Review is ACCEPTED/COMPLETE. AD-1–AD-5 were reconciled into Skarn. In this spec only AD-5 (L298) and AC-4 (L160) are visible.
- PR L54: unqualified "human" means Marchfolk HRP at matched normalized height. PR L56: "baseline" is retired (relevant to Skarn L52).
- PR L59: Muscular Development Capacity is distinct from Current Muscularity (reflected at L26, L80).
- PR L16: the age triad. The Skarn spec is silent.
- PR L65–71: R-SEX. The Skarn spec defines no facial sex tendency, so per PR L69 "no shift" is a valid complete state. This is a project-rule inference and not a Skarn spec claim.

## Extraction notes
- **Region table vs. region list:** L158 names seven regions including "mouth and lips" and "ears". The §3–6 table (L166–171) has only four rows ("Nose and mid-face" and "Cheeks, jaw and chin" are combined) and no mouth/lips or ears rows. Ears are covered by AC-4 (L160). Mouth/lips has no Skarn-specific controls or tendencies.
- v1.0 §8 (L48) deferred "detailed craniofacial ranges" to a later spec. v1.2 provides tendencies only, so numeric ranges remain absent.
- Body-to-face soft-tissue coupling (L175) is "proposed universal", "pending validation", yet is used as a constraint in randomization (L280). Its status is mixed.
- Naturalize Face, randomization strength, selective randomization, presentation presets and regional weathering are all labelled "proposed universal". They are not settled canon.
- SK-10 "Soft-featured" is the only SK fixture that is explicitly facial.
- The AC-4 ear pointer is explicitly not a head-equivalence claim (L160).
