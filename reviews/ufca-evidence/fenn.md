> UFCA Phase 1 evidence appendix to `reviews/claude-ufca-01-requirements-matrix.md`. Line references are to the canonical race spec as of commit c076294. Extraction only: no canon is changed, and nothing here is new anatomy. Tags: [ANAT] anatomical requirement · [CTRL] creator-facing control requirement · [VAL] dependency/validator · [PRES] presentation · [DIAG] measurement/diagnostic · [OPEN] open/not authorized.

# UFCA-01 evidence: Fenn (Wood Elf)

Source: `specs/fenn/FENN_V1.md` (v1.5, first-pass complete, L1-L3). Facial material lives in v1.2 (L154-L228), with facial items also in v1.3 (L230-L308), v1.4 (L310-L423) and v1.5 (L425-L544).
Comparative authority: `reviews/elf-comparative-review.md` (ECR; accepted, authority level 3). The ECR is "the current comparative biological authority for Fenn, Aelari and Vael, and the individual race specs stay authoritative wherever the review doesn't explicitly clarify or supersede them" (ECR L3, L302, L346). Refs below are `Lnnn` = FENN_V1.md and `ECR Lnnn` = review.

Status of facial control organization: v1.2 classification block (L158). Facial regions, editing levels, control groupings, slider organization and other creator-facing control structure (including ear controls) = **APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION**. Anatomy, tendencies, variation, relationships, ear biology, identity, validation, required capability, preset and randomization requirements "stay approved as established". Only the organization into a final facial-control system is provisional, kept as input to the UFCA Review.

---

## 0. What the Elf Comparative Review settles for the Fenn face

- [ANAT] Shared elven craniofacial ancestry (A): an elven face is "not a human face with pointed ears, a reduced jaw and conventional attractiveness"; ancestry from combined cranium, forehead, brow and orbits, midface, cheeks, nose, jaw and chin, eyes and ears; no single feature defines an elf (ECR L77).
- [ANAT] "There is no universal elf face": no mandatory eye, nose, jaw, chin, cheekbone, lip or brow shape, face width or attractiveness standard (ECR L77).
- [VAL] A single "Elf Head" with superficial morphs for all three isn't used unless prototyping proves it can reproduce the approved diversity (ECR L77).
- [ANAT] Shared cranial tendencies (provisional): somewhat greater cranial-height contribution than equivalent humans; different cranial-to-face relationships; elven integration of forehead, orbit and midface; lower apparent craniofacial skeletal mass than robust human populations. "Elves aren't defined by enlarged skulls." (ECR L77)
- [ANAT] Fenn overall face (B): compact facial relationships, relatively open visible orbits, somewhat reduced lower-face mass, distinct cheek placement, lighter mandible than equivalent humans (ECR L83).
- [ANAT] Fenn brow and orbits (B): more open visible orbital and eye presentation (ECR L84). Clarified: "open presentation" = combined visible relationship of orbital anatomy, eyelids and exposed eye area, **not eyeball size**; trend vs Aelari and Vael on average with substantial overlap; does NOT mean every Fenn has larger eyes / larger opening or any individual Fenn must have more open eyes than an Aelari or Vael (ECR L141).
- [ANAT] Fenn cheeks and midface (B): distinct cheek placement tied to compact face; exact ancestral midface E; no universal high, hollow, flat or projected cheeks (ECR L85).
- [ANAT] Nose: shared principle, not shared shape; broad diversity; "Elf = small narrow nose" rejected; Fenn population nasal frequencies E (ECR L86).
- [ANAT] Jaw and chin: shared lower average mandibular mass than robust humans (A), never weak, pointed, V-shaped, narrow, feminized or mandatorily delicate; strong-jawed elves valid; Fenn = lighter lower-face mass (ECR L87). Clarified: Fenn keep relatively light average lower-face and mandibular presence within the elven range; **no strict Fenn-versus-Aelari mandibular ranking** (ECR L142).
- [ANAT] Mouth and lips: E, no shared morphology required, broad variation (ECR L88).
- [ANAT] Overlap: distributions overlap substantially (ECR L90).
- [ANAT] Eyes: orbital, external eye, ocular, pigmentation and magical effects stay separate (ECR L94). Round pupils conservative baseline; no slit/vertical/horizontal pupils for exoticism (E, ECR L99). Vael low-light "isn't retroactively given to Fenn or Aelari" (ECR L100). Fenn low-light vs Marchfolk remains open (ECR L298).
- [ANAT] Ears: shared non-human ancestry (A); conceptual control family length, base width, tip length, tip sharpness, vertical angle, sweep, lateral projection, curvature, lobe size and attachment "without identical ranges or morphs"; ancestral ear shape E (ECR L104). Fenn (B): greater outward and backward projection, broad variation; guard "No mandatory horizontal spear ears" (ECR L108). Clarified: Fenn greater average **lateral** projection than Aelari and Vael, often with backward sweep; projection and sweep are separate measurements (ECR L143); "Greatest average lateral (outward) projection of the three" (ECR L328); "Closer to skull" isn't a separate ear shape (ECR L332).
- [VAL] Ear overlap locked; must stay recognizable with minimum, masked or hair-covered ears (ECR L112). Ear mobility E (ECR L112).
- [ANAT] Aging shared (A); individual identity locked: plain, attractive, soft, rugged, narrow, broad, strong-jawed, strong-nosed, rounder, scarred, asymmetrical, high-body-fat, elderly all supported (ECR L116, L245).
- [VAL] Tests: three-elf neutral face (Fenn compact face and open orbits) (ECR L122); ear-only distribution (ECR L123); human boundary (ECR L124); expression neutrality — fails if resting anatomy makes Fenn look "permanently startled" (ECR L125).
- [ANAT] Final matrix craniofacial: Fenn "More compact facial relationships and more open visible orbits than Aelari and Vael" (ECR L282); ears row (ECR L283).
- [VAL] Anti-exaggeration: fix readability by checking multi-region anatomy before enlarging ears or eyes or pushing jaw shape etc. (ECR L294).
- [VAL] Comparative terminology rule: comparative language must name the comparison population or reference relationship; keep orbital size vs visible eye opening, projection vs sweep, absolute vs proportional distinct (ECR L51, L145).
- [ANAT] Facial hair: not biologically prohibited for any elf; clean-shaven not universally elven (A) (ECR L175). This fills a Fenn-spec silence.

## 1. Cranial vault / cranial proportions
- [ANAT] Population tendency (not mandatory): "Slightly greater cranial height relative to face, somewhat narrower skull, slightly less lower-face mass, smoother forehead-to-cranium line"; supported variation "Broad individual variation" (v1.2 §2-7, L168).
- [ANAT] Craniofacial anatomy is part of core identity (L15) and part of hidden-ear distinction (L78).
- [ANAT] ECR shared cranial tendencies apply (ECR L77; see §0).

## 2. Forehead
- [ANAT] "smoother forehead-to-cranium line" (L168). Otherwise SILENT (no forehead height/slope controls listed in Fenn spec).

## 3. Brow / supraorbital
- [ANAT] "distinct brow and orbit relationships" (L169).
- [CTRL] Supported variation includes "brow-to-eye distance, brow structure" (L169).
- [ANAT] ECR: Fenn more open visible orbital presentation (ECR L84, L141). Brow height/prominence controls SILENT in Fenn spec.

## 4. Orbit
- [ANAT] "Slightly larger orbits, slightly more eye prominence, wide eye-angle range, distinct brow and orbit relationships" (L169).
- [CTRL] Size, spacing, depth, angle (L169).
- [ANAT] ECR clarification: "open presentation" is not eyeball size and not a per-individual rule (ECR L141). Note tension with "slightly larger orbits" (L169) — ECR does not repeat "larger orbits" for Fenn (see Extraction notes).
- [VAL] Facial animation validation pays "particular attention to eyelids and orbits" (L203).

## 5. External eye (aperture, lids, canthi, folds)
- [CTRL] "opening, lids" variation (L169).
- [ANAT] "Never anime-like oversized eyes as the marker" (L169).
- [VAL] Failure: "Identical noses or eye shapes" (L414).
- [ANAT] Aelari spec (comparative, provisional): "Aelari eyes read somewhat longer and narrower, and Fenn eyes more open" (AELARI L212) — consistent with ECR L84.
- Canthi / folds: SILENT.

## 6. Ocular anatomy (iris, sclera, pupil, nictitating membrane, low-light, magic)
- [OPEN] "Unresolved: whether Fenn have moderately better low-light vision than humans." Space kept for Vael stronger subterranean adaptation (v1.3 §9, L268). Retained in ECR unresolved register (ECR L298).
- [OPEN] Eye color frequencies wait for comparative elf review (L248, L385, L544).
- [ANAT] Pupil: SILENT in Fenn spec; ECR round pupils conservative baseline (ECR L99).
- Iris palette: SILENT in Fenn spec; ECR no universal elven iris palette, list of possible colors across populations (ECR L179).
- Magic vs biology: SILENT in Fenn spec; ECR biological iris separate from magical effects (ECR L179).
- Sclera, nictitating membrane: SILENT.

## 7. Cheek / zygomatic
- [ANAT] "Somewhat higher cheekbones, slightly lighter mid-face" (L170).
- [CTRL] "Broad or narrow, high or low within Fenn limits, strong or subtle projection, full or hollow, soft or angular" (L170).
- [ANAT] ECR: distinct cheek placement tied to compact face; no universal high cheeks (ECR L85).

## 8. Midface
- [ANAT] "slightly lighter mid-face" (L170).
- [ANAT] ECR: exact ancestral midface E (ECR L85).

## 9. Nasal
- [ANAT] "No mandatory small or straight nose" (L171).
- [CTRL] "Length, width, bridge height and width, profile curve, projection, tip structure and rotation, nostril width, alar structure" (L171).
- [VAL] FN-21 Large, broad nose (L221). Failure "Identical noses" (L414).
- [OPEN] Fenn nasal population frequencies E (ECR L86).

## 10. Mouth / lips
- [ANAT] "No mandatory mouth shape" (L173).
- [CTRL] "Width, lip fullness and projection, Cupid's bow, philtrum, corners, natural asymmetry" (L173).

## 11. Jaw / mandible
- [ANAT] "Somewhat lighter jaw than humans on average" (L172); "slightly less lower-face mass" (L168).
- [CTRL] "Narrow, broad, angular, rounded, strong or subtle jaws" (L172).
- [ANAT] "Broad or muscular Fenn stay valid" (L172).
- [VAL] FN-20 Strong-jawed (L220).
- [ANAT] ECR L87, L142 (see §0).

## 12. Chin
- [CTRL] "all chin sizes and projections" (L172).
- [ANAT] ECR: never pointed (ECR L87).

## 13. External ear
- [ANAT] Ears are "real racial anatomy, not an accessory" (v1.0 §9, L62); "their own external-ear anatomy, not human ears with stretched tips" (L179).
- [ANAT] Future work keeps coherent structures analogous to helix, antihelix, concha, tragus region, lobe, upper-ear extension and tip; "The point emerges naturally from the whole ear" (L179).
- [ANAT] Population tendency (inserted from ECR final clarification §3; Pass 2 AC-5): "Fenn have the greatest average lateral (outward) ear projection of Fenn, Aelari and Vael, with individual overlap and the Fenn ear bounds (§9) preserved" (L179).
- [CTRL] v1.0 possible controls: "ear length, width and projection, tip length and angle, upper-ear curvature, and lobe structure" (L62) — superseded/expanded by v1.2 §9.
- [CTRL] v1.2 controls: "overall length, base width, tip length and sharpness, vertical angle, forward and backward sweep, projection from the skull, upper-ear curvature, lobe size and lobe attachment" within coherent Fenn ranges (L183).
- [ANAT] "no single mandatory oversized ear shape" (L62); "no single mandatory oversized silhouette" (L183).
- [CTRL] Ear asymmetry: height, angle, projection, minor shape; conservative defaults; Restore Symmetry (L187).
- [PRES] Acquired ear damage (notches, healed tears, missing tip portions, scars, piercing damage) belongs to scars/acquired appearance, never racial anatomy (L191).
- [OPEN] Ear movement (voluntary/involuntary) decided later (L207); ECR E (ECR L112).
- [VAL] Ear independence: randomization never produces human body + human face + pointed ears; minimum-ear Fenn keep Fenn anatomy; maximum-ear Fenn coherent, not caricatured (L341).
- [VAL] Headgear/ear equipment problem; never auto clip, hide/delete, flatten, or make all headgear Fenn-only (L467); hair/ears/headgear validated together respecting skull and ear anatomy (L471).
- [ANAT] Aelari spec's comparative Fenn ear tendency: "Somewhat more outward and backward projection, broad individual variation" (AELARI L225); Vael spec same (VAEL L278).

## 14. Teeth / dentition
- SILENT.

## 15. Race-specific cranial displays / keratin / horns
- SILENT (none). N/A.

## 16. Skin/surface structures that materially alter facial anatomy
- SILENT. (Skin layers L252 and regional face controls L256 are pigmentation/weathering, not anatomy.)
- [PRES] Face keeps regional environmental controls where feasible; Fenn not automatically weathered (L256).
- [ANAT] "No naturally green skin as a default Fenn trait" (L240).

## 17. Natural asymmetry
- [CTRL] Mouth "natural asymmetry" (L173).
- [CTRL] Ear asymmetry with conservative defaults + Restore Symmetry (L187).
- [ANAT] Asymmetrical Fenn valid (L199).
- [VAL] FN-26 Ear asymmetry test (L226).
- Whole-face asymmetry control list: SILENT (contrast Vael §27).

## 18. Age-related facial change
- [ANAT] "Fenn visibly age": facial volume, skin elasticity, eye area, cheeks, jawline, neck tissue, wrinkles, hair density and color, ear tissue (subtly), body composition and posture (L195).
- [OPEN] Lifespan and aging rate not set; logged for lore review (L195).
- [ANAT] "Body composition and age can influence facial soft tissue without replacing skeletal identity" (L175).
- [VAL] FN-23 Elder (L224); failure "Mandatory youthful appearances" (L412); Elder test in gate (L525).
- Age triad (chronological / apparent / presentation): SILENT in Fenn spec; ECR: biological age separate from age presentation (ECR L245).

## 19. Sex-related facial tendency
- SILENT. The Fenn spec contains no sex-related statement (no occurrence of "sex").

## 20. Facial hair biology (incl. eyebrows)
- SILENT in Fenn spec (hair biology L260 covers scalp hair only). ECR fills: facial hair not prohibited for any elf; clean-shaven not universally elven; distributions unresolved (ECR L175).
- Eyebrows: SILENT (only "brow structure" as skeletal, L169).

## 21. Inherited / mixed development
- N/A (Halvren only). Note ECR: elven conclusions inform Halvren "not as move human sliders halfway toward elf" (ECR L129).

## 22. Locked validation tests touching the face
- [VAL] FN-10 Hidden-ear human-overlap stress test (L93).
- [VAL] Hidden-ear validation (v1.0 §13, L78): with ears hidden, Fenn stand out incl. craniofacial anatomy.
- [VAL] Hidden-ear facial test (v1.2 §16, L211): vs Marchfolk and Sagekin at equal age/composition; identity via cranium, orbits, cheeks, mid-face, jaw; not every individual identifiable.
- [VAL] Facial animation validation (v1.2 §14, L203): neutral, speech, smile, anger, fear, surprise, sadness, blink, eye movement; attention to eyelids and orbits.
- [VAL] FN-18 Soft-featured; FN-19 Broad-faced; FN-20 Strong-jawed; FN-21 Large, broad nose; FN-22 High-body-fat facial validation; FN-23 Elder; FN-24 Max ear length; FN-25 Min subtle ear length; FN-26 Ear asymmetry; FN-27 Hidden-ear facial comparison (L219-L228).
- [VAL] FN-32 Minimum-ear full-body test; FN-33 Maximum-ear full-body test; FN-34 Neutral-presentation randomized Fenn; FN-37 Hidden-ear randomized boundary case; FN-38 Valid extreme randomization (L398-L403).
- [VAL] Hidden-ear population test: 100 Marchfolk/100 Sagekin/100 Fenn, presentation neutralized, ears hidden (v1.4 §7, L349).
- [VAL] Facial population validation: randomized portraits, ears hidden, hair neutralized; never one mandatory eye, nose, jaw, cheekbone or "elf face" (v1.4 §9, L357).
- [VAL] Subtle-ear validation: permanent minimum-ear and maximum-ear tests (v1.4 §10, L361).
- [VAL] Failure conditions touching face (L409-L419): human bodies with pointed ears; one repeated elf face; mandatory youthful appearances; mandatory conventional attractiveness; identical noses or eye shapes.
- [VAL] Final gate (v1.5 §23, L517-L536): hidden-ear facial test, minimum-ear, maximum-ear, elder, facial-expression, headgear and ear, cross-cultural presentation, save/load reproduction, population-randomization.
- [VAL] Cross-race: Sagekin/Fenn boundary protected — Fenn have "a genuinely elven skeleton and face" (L540).
- [VAL] ECR tests (ECR L122-L125) apply (see §0).

## 23. Explicitly OPEN biology touching the face
- [OPEN] Fenn low-light vision vs humans (L268; ECR L298).
- [OPEN] Ear movement (L207; ECR L112).
- [OPEN] Lifespan and aging rate (L195).
- [OPEN] Eye color, overlapping facial trait frequencies (L385; ECR L213); nasal population frequencies (ECR L86); ancestral ear shape, exact ancestral midface (ECR L85, L104); pupil morphology (ECR L99, L298).
- [OPEN] Skeleton / MetaHuman not assumed (L431).

## 24. Pass 1 provisional creator-control list for the face
(Status: provisional organization, L158.)
- Cranium: no controls itemized; "Broad individual variation" (L168).
- Eyes and orbits: size, spacing, depth, angle, opening, lids, brow-to-eye distance, brow structure (L169).
- Cheeks and mid-face: broad/narrow, high/low within Fenn limits, strong/subtle projection, full/hollow, soft/angular (L170).
- Nose: length, width, bridge height and width, profile curve, projection, tip structure and rotation, nostril width, alar structure (L171).
- Jaw and chin: narrow/broad, angular/rounded, strong/subtle jaw; all chin sizes and projections (L172).
- Mouth and lips: width, lip fullness and projection, Cupid's bow, philtrum, corners, natural asymmetry (L173).
- Ears: overall length, base width, tip length and sharpness, vertical angle, forward/backward sweep, projection from skull, upper-ear curvature, lobe size, lobe attachment (L183); asymmetry height/angle/projection/minor shape + Restore Symmetry (L187).
- [VAL] Relationship-aware randomization keeps craniofacial and ear-to-skull relationships (L337).
- No editing levels / Simple-Advanced structure stated (SILENT). No master slider explicitly forbidden, but "never just from longer human sliders" (L138, body) and "Sliders are never randomized independently" (L337).

## 25. Prohibited / forbidden controls and anti-patterns
- [ANAT] Never anime-like oversized eyes as the marker (L169).
- [ANAT] No mandatory small or straight nose (L171); no mandatory mouth shape (L173).
- [ANAT] No single mandatory oversized ear shape/silhouette (L62, L183); not human ears with stretched tips (L179).
- [ANAT] No single canonical "beautiful elf face" (L162); no conventional-attractiveness requirement (L199).
- [VAL] Randomization never human body + human face + pointed ears (L341); never independent sliders (L337).
- [PRES] Ear damage never racial anatomy (L191).
- [PRES] Presentation presets never overwrite race, skeleton, face, ears, height, composition, natural pigmentation (L329).
- [VAL] Headgear never auto clips, hides/deletes, flattens ears (L467).
- [ANAT] No green skin default (L240); no forest gimmicks (L268).
- [ANAT] ECR: no mandatory horizontal spear ears (ECR L108); not "permanently startled" resting anatomy (ECR L125).

## 26. Positive identity statement
- "Fenn faces never depend only on pointed ears. With the ears hidden, subtle elven craniofacial traits remain. There's no single canonical 'beautiful elf face', and identity comes from many relationships together." (L162)
- "Fenn identity comes from cranial, orbital, cheek, mid-face, jaw and other relationships together, never from one mandatory eye, nose, jaw, cheekbone or 'elf face'." (L357)
- "the Fenn population must never collapse into ordinary human anatomy" (L349).
- ECR: "More compact facial relationships and more open visible orbits than Aelari and Vael" (ECR L282).

## 27. Cross-population facial boundary tests / comparators
- Marchfolk, Sagekin (hidden-ear tests L78, L211, L349, L357); Sagekin/Fenn boundary protected (L540); FN-17 (body), FN-27, FN-37.
- Aelari and Vael "later" (L540); ECR three-elf neutral face, human boundary (ECR L122, L124).
- Skarn (cross-race body, L540).

## 28. Measurement-deferred items (RM-*)
- None. No RM-* refs in the Fenn spec.

## 29. Presets / randomization / Simple-Advanced
- [CTRL] Character presets (provisional): Canopy Pathfinder, Forest Artisan, Broad Warden, River Traveler, Heavyset Trader, Elder Storykeeper, Foreign-Raised Fenn, Young Wanderer; visual only, reproducible, fully editable (L316-L325).
- [PRES] Presentation presets never overwrite face or ears (L329).
- [VAL] Generation sequence: ... → facial anatomy → ear anatomy → pigmentation and hair → ... (L333).
- [VAL] Relationship-aware randomization incl. craniofacial and ear-to-skull (L337).
- [VAL] Biology vs presentation randomization (L376-L381).
- [VAL] Deterministic generation via seeds (L511).
- Simple/Advanced mode: SILENT.

## Extraction notes
- Ear projection: v1.2 §8 L179 has an inline insertion from ECR final clarification §3 (Pass 2 AC-5) stating Fenn greatest average lateral projection. This post-dates the original v1.2 text and is consistent with ECR L328.
- Orbits: Fenn spec says "Slightly larger orbits, slightly more eye prominence" (L169); ECR frames Fenn as "more open visible orbital and eye presentation" and explicitly says open presentation is "not eyeball size" and not an individual rule (ECR L141). ECR does not settle orbital (skeletal socket) size for Fenn; treat "larger orbits" as Fenn-spec tendency, read through ECR terminology rule (comparison target unnamed in Fenn spec: vs humans implied by "Compared with humans" framing only for body §3).
- "Somewhat higher cheekbones" (L170) vs ECR "No universal high ... cheeks" (ECR L85, shared level) — not a contradiction (Fenn tendency vs shared universality) but ECR's Fenn cell says only "distinct cheek placement".
- Fenn jaw: "lighter jaw than humans" (L172); ECR names target as "equivalent humans"/"robust human populations" (ECR L83, L142).
- Forehead, brow height/prominence, chin shape, facial hair, eyebrows, sex: Fenn spec lacks these (Aelari/Vael have forehead/brow controls). Facial hair filled only by ECR L175.
- Ear control list evolved: v1.0 L62 ("width", "tip length and angle", "lobe structure") → v1.2 L183 (fuller list). v1.2 governs.
- No Simple/Advanced mode statement in Fenn (Aelari/Vael have it).
