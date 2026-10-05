> UFCA Phase 1 evidence appendix to `reviews/claude-ufca-01-requirements-matrix.md`. Line references are to the canonical race spec as of commit c076294. Extraction only: no canon is changed, and nothing here is new anatomy. Tags: [ANAT] anatomical requirement · [CTRL] creator-facing control requirement · [VAL] dependency/validator · [PRES] presentation · [DIAG] measurement/diagnostic · [OPEN] open/not authorized.

# UFCA-01 evidence: Aelari (High Elf)

Source: `specs/aelari/AELARI_V1.md` (v1.5, first-pass complete, L1-L3). Facial material lives in v1.2 (L196-L274), with eye, hair and facial-hair items in v1.3 (L276-L396), presets/randomization in v1.4 (L398-L531) and technical items in v1.5 (L533-L610).
Comparative authority: `reviews/elf-comparative-review.md` (ECR; accepted, authority level 3). It is the comparative biological authority, and the race spec stays authoritative where the ECR doesn't explicitly clarify or supersede it (ECR L3, L302, L346). Aelari spec L527 and L610 confirm the review has been "performed and accepted". Refs: `Lnnn` = AELARI_V1.md, `ECR Lnnn` = review.

Status of facial control organization: v1.2 classification block (L200). Facial regions, editing levels, control groupings, slider organization and creator-facing control structure (including ears) = **APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION**. Anatomy, tendencies, variation, relationships, ear biology, identity, validation, required capability, preset and randomization requirements stay approved. Only the final control organization is provisional (input to the UFCA Review).

---

## 0. What the Elf Comparative Review settles for the Aelari face

- [ANAT] Shared elven craniofacial ancestry, no universal elf face, no single "Elf Head" with superficial morphs unless proven (ECR L77).
- [ANAT] Shared cranial tendencies: somewhat greater cranial-height contribution than equivalent humans; different cranial-to-face relationships; elven forehead/orbit/midface integration; lower apparent craniofacial skeletal mass than robust human populations; not enlarged skulls (ECR L77).
- [ANAT] Aelari overall face (C): "Greater facial verticality, longer forehead-to-chin, somewhat narrower lower face, vertical midface, somewhat lighter mandible, longer and narrower visible eyes than Fenn" (ECR L83).
- [ANAT] Aelari brow and orbits (C): "Somewhat longer and narrower visible eyes, lighter brow" (ECR L84). Shared: size, opening, depth, brow and angle vary; large eyes not universal (ECR L84).
- [ANAT] Aelari cheeks and midface (C): "More vertical midface orientation"; exact ancestral midface E (ECR L85).
- [ANAT] Nose: shared principle not shape; "Elf = small narrow nose" rejected; Aelari population nasal frequencies E (ECR L86).
- [ANAT] Jaw/chin: shared lower average mandibular mass than robust humans; never weak, pointed, V-shaped, narrow, feminized or mandatorily delicate; strong-jawed elves valid. Aelari "Lighter mandible with greater verticality" (ECR L87). Clarified: relatively light average mandibular presence with greater facial verticality; no strict Fenn-vs-Aelari mandibular ranking (ECR L142).
- [ANAT] Mouth/lips: E, no shared morphology (ECR L88).
- [ANAT] "Aelari traits never equal beauty, refinement or nobility" (ECR L90).
- [ANAT] Eyes: five systems separate (orbital, external eye, ocular, pigmentation, magical) (ECR L94); round pupils baseline (ECR L99); Vael low-light not retroactively given to Aelari (ECR L100).
- [ANAT] Ears (C): "More upward and backward orientation, somewhat closer-to-skull profile, moderate-to-long length, more gradual taper"; guard "Long elegant ears aren't mandatory" (ECR L109). Final clarification §3: Aelari lower average lateral projection than Fenn; vs Vael overlap with "no strict universal ranking yet"; "'Closer to skull' isn't a separate ear shape"; projection, sweep, vertical angle, base width, taper, length separate variables (ECR L324-L332; matrix L283).
- [VAL] Ear overlap locked; recognizable with minimum/masked/hair-covered ears; mobility E (ECR L112).
- [ANAT] Aging shared; individual identity locked (ECR L116, L245).
- [VAL] Three-elf neutral face (Aelari facial verticality) (ECR L122); expression neutrality — fails if resting anatomy makes Aelari "permanently aloof" (ECR L125).
- [ANAT] Final matrix craniofacial: "Greater average facial verticality" (ECR L282).
- [ANAT] Facial hair not prohibited for any elf (ECR L175); iris: no universal elven palette, magic separate (ECR L179).
- [ANAT] Aelari neck (adjacent to head): greater average neck length and proportional neck contribution than Fenn and Vael; absolute vs proportional distinct (ECR L320). Relevant to "shoulder-to-neck-to-skull line" (L50).

## 1. Cranial vault / cranial proportions
- [ANAT] "Slightly greater cranial height, somewhat longer face, longer forehead-to-chin line, somewhat narrower lower face, relatively light jaw"; guard "No exaggerated alien proportions" (v1.2 §2-8, L210).
- [ANAT] Whole-body vertical elongation "distributed coherently through the cranium, neck, torso, arms and legs" (L33).
- [ANAT] Neck: "shoulder-to-neck-to-skull line adds subtly to verticality" (L50).
- [ANAT] "elven craniofacial foundations" as provisional shared theme (L17).

## 2. Forehead
- [ANAT] Forehead and brow: "Smoother, lighter brow on average than robust humans such as Skarn" (L211).
- [CTRL] "Forehead height and slope, temple width" (L211).
- [ANAT] "longer forehead-to-chin line" (L210).

## 3. Brow / supraorbital
- [ANAT] "Smoother, lighter brow on average than robust humans such as Skarn" (L211).
- [CTRL] "brow height, shape and prominence" (L211).
- [ANAT] "Delicate or weak brows never required" (L211).
- [ANAT] ECR "lighter brow" (ECR L84).

## 4. Orbit
- [ANAT] "Shared elven orbital foundation" (L212).
- [CTRL] Size, depth, spacing, angle, brow-to-eye distance (L212).

## 5. External eye
- [ANAT] "Provisionally, Aelari eyes read somewhat longer and narrower, and Fenn eyes more open" (L212). Settled by ECR as "longer and narrower visible eyes than Fenn" (ECR L83-L84).
- [CTRL] Lids, opening (L212).
- [ANAT] "No mandatory upturned, almond, oversized or glowing eyes" (L212).
- [VAL] Failure: one eye shape dominates (L520).
- Canthi / folds: SILENT.

## 6. Ocular anatomy
- [ANAT] Valid iris colors: brown, dark brown, amber, hazel, green, gray, blue, and other grounded elven colors set during the comparative review; frequencies unresolved; blue, pale or luminous eyes never required (v1.3 §6, L303).
- [ANAT] Biological iris vs magical eye effects (proposed universal): iris = inherited pigmentation and anatomy; magical effects = magic, conditions, abilities, artifacts; "Magical glow is never baked into normal racial iris color unless explicitly approved. An Aelari with ordinary brown eyes is fully authentic." (v1.3 §7, L305-L312)
- [ANAT] "High Elf = pale skin + blond hair + blue or glowing eyes" rejected (L282).
- [VAL] AE-41 Dark hair, dark eyes, neutral presentation (L497).
- Pupil, sclera, low-light, nictitating membrane: SILENT in Aelari spec; ECR round pupils baseline, Vael low-light not given to Aelari (ECR L99-L100).

## 7. Cheek / zygomatic
- [ANAT] "Somewhat vertically oriented cheek and mid-face relationships" (L213).
- [CTRL] "High or low, broad or narrow, strong or subtle, full or hollow, soft or angular" (L213).
- [ANAT] "Composition and age shift soft tissue, not ancestry" (L213).

## 8. Midface
- [ANAT] Vertically oriented mid-face (L213); ECR "vertical midface" (ECR L83, L85).
- [VAL] Hidden-ear facial test identity through "cranial, orbital, mid-face and jaw relationships" (L243).

## 9. Nasal
- [ANAT] "No Aelari nose type" (L214).
- [CTRL] "Short or long, narrow or broad, low or high bridge, straight, convex or concave, projection, tip, nostrils, alar structure" (L214).
- [ANAT] "'High Elf = small, narrow, straight nose' is rejected" (L214).
- [VAL] AE-28 Large, broad nose (L264); generic-elf convergence includes "small-nosed" (L464).

## 10. Mouth / lips
- [ANAT] "No Aelari lip type" (L216).
- [CTRL] "Width, fullness, projection, Cupid's bow, philtrum, corners, natural asymmetry" (L216).

## 11. Jaw / mandible
- [ANAT] "Relatively light jaw on average" (L215); "relatively light jaw" (L210).
- [CTRL] "Broad, narrow, strong, soft, angular or rounded jaws" (L215).
- [ANAT] "Broad or muscular Aelari may have substantial jaws" (L215).
- [VAL] AE-27 Strong-jawed (L263).

## 12. Chin
- [CTRL] "and all chins" (L215).
- [ANAT] ECR: never pointed (ECR L87).

## 13. External ear
- [ANAT] Fenn and Aelari ears share plausible ancestry without being identical; both genuinely non-human, "not human ears with stretched tips" (L220). (Exact universal elven ear anatomy "waits for the Vael design" — superseded by ECR L104.)
- [ANAT] Aelari tendency: "Somewhat more upward orientation, clean gradual taper, slightly closer to the skull, moderate to long length" (L224). Fenn contrast: "Somewhat more outward and backward projection" (L225).
- [ANAT] "These are never rigid species markers. A short-eared Aelari and a long-eared Fenn are both valid." (L227)
- [CTRL] Controls: "overall length, base width, tip length and sharpness, vertical angle, forward and backward sweep, projection, upper-ear curvature, and lobe structure and attachment" (L231).
- [CTRL] Subtle asymmetry: height, angle, projection, shape; Restore Symmetry (L231).
- [PRES] Notches, healed tears, missing tip portions, scarring, piercing damage = acquired (L231).
- [OPEN] Ear mobility: "Aelari ears aren't assumed to move just because they're elves" (L247); ECR E (ECR L112).
- [VAL] Ear tests: minimum, population-reference and maximum valid ears plus strong valid asymmetry; identity survives subtle ears; max never caricature (L468).
- [VAL] Headgear: same equipment problem as Fenn; ruled out clipping, universal hiding, flattening, Aelari-only helmets (L566).
- [ANAT] ECR refinement: "slightly closer to the skull" re-expressed as lower average lateral projection than Fenn; "Closer to skull" not a separate shape (ECR L324-L332). Vael spec's comparative version adds "upward and backward orientation, longer taper" (VAEL L279).

## 14. Teeth / dentition
- SILENT.

## 15. Cranial displays / keratin / horns
- SILENT (none). N/A.

## 16. Skin/surface structures that alter facial anatomy
- SILENT. (Skin layers L299 are pigmentation/environment; face shows own history, L299.)

## 17. Natural asymmetry
- [CTRL] Mouth "natural asymmetry" (L216); ear asymmetry + Restore Symmetry (L231).
- [ANAT] Asymmetrical Aelari valid (L239).
- [VAL] AE-33 Ear asymmetry (L267); strong valid asymmetry ear test (L468).
- Whole-face asymmetry list: SILENT.

## 18. Age-related facial change
- [ANAT] "Aelari visibly age: facial volume, skin elasticity, eye area, cheeks, jawline, neck, wrinkles, hair density and color, and ear tissue where appropriate. High Elves are never assumed to stay permanently youthful." (L235)
- [OPEN] Lifespan and aging rate OPEN DECISION (L235).
- [ANAT] Natural silver/white hair (if validated) distinct from age graying (L332).
- [VAL] AE-08 Elder (L92), AE-30 Elder (L264), AE-43 Elder culturally neutral (L499); failure "Elder Aelari stop reading as Aelari" (L516); preset Elder Waykeeper (L417).
- Age triad: SILENT in spec; ECR biological age vs age presentation (ECR L245).

## 19. Sex-related facial tendency
- SILENT for the face. Sex-related statements exist only for body/hair: "No mandatory hip width by race or sex-related anatomy" (L126); frame separate from sex-related anatomy (L134); hairstyle never locked to sex-related anatomy (L340). ECR: jaw never "feminized" (ECR L87).

## 20. Facial hair biology (incl. eyebrows)
- [ANAT] "Facial hair is independent of hairstyle and frame, covering presence, density, style, length, color and graying. Aelari are neither required to be clean-shaven nor required to have facial hair. Frequency is provisional." (v1.3 §13, L336)
- [ANAT] ECR facial hair not prohibited for any elf (ECR L175).
- Eyebrows (hair): SILENT (brow controls L211 are structural).

## 21. Inherited / mixed development
- N/A. Note L251: Aelari and Fenn faces and ears will inform Halvren; Halvren never "humans with medium-length ears"; architecture flexible for genuinely intermediate ancestry.

## 22. Locked validation tests touching the face
- [VAL] Hidden-ear facial test vs Fenn, Sagekin, Marchfolk; age/composition matched; hair/presentation neutralized; identity statistically present through cranial, orbital, mid-face and jaw relationships (v1.2 §15, L243).
- [VAL] Expression tests: neutral, speech, smile, anger, fear, surprise, sadness, blink, eye movement (L243).
- [VAL] AE-25 Soft-featured; AE-26 Broad-faced; AE-27 Strong-jawed; AE-28 Large, broad nose; AE-29 High-body-fat facial test; AE-30 Elder; AE-31 Min subtle ear; AE-32 Max ear; AE-33 Ear asymmetry; AE-34 Hidden-ear Fenn comparison; AE-35 Hidden-ear Sagekin comparison; AE-36 Facial-expression stress test (L259-L270).
- [VAL] AE-39 Min ears neutral presentation; AE-40 Max ears neutral; AE-41 Dark hair, dark eyes; AE-43 Elder culturally neutral; AE-45 Sagekin boundary; AE-46 Fenn boundary; AE-48 Generic-elf convergence counterexample; AE-49 Diverse randomized; AE-50 Extreme valid randomized (L495-L505).
- [VAL] Generic-elf convergence test: fails if sample converges on tall, thin, pale, young, conventionally beautiful, narrow-faced, small-nosed, long-haired, light-haired, blue-eyed with identically pointed ears (v1.4 §14, L464).
- [VAL] Hidden-ear population test with Marchfolk, Sagekin, Fenn, Aelari (L472).
- [VAL] Sagekin boundary: elven craniofacial architecture incl. face; "Never solved by exaggerating Aelari ears" (L478).
- [VAL] Cultural neutralization: ancestry stays visible with presentation removed (L484).
- [VAL] Failure conditions (L511-L523): pointed ears needed; simply taller Fenn; elders stop reading; one "pretty High Elf" template; one eye, nose or jaw shape dominates; cultural presentation needed.
- [VAL] ECR tests apply (ECR L122-L125).

## 23. Explicitly OPEN biology touching the face
- [OPEN] Ear mobility (L247; ECR L112).
- [OPEN] Lifespan and aging rate (L235).
- [OPEN] Eye color frequencies, hair color frequencies, natural silver/white hair validity (L303, L328).
- [OPEN] Facial hair frequency provisional (L336).
- [OPEN] Nasal population frequencies E, ancestral midface E, ancestral ear E, pupil E (ECR L85-L86, L99, L104).
- [OPEN] Technical foundation / MetaHuman candidate-only (L100, L539).

## 24. Pass 1 provisional creator-control list for the face
(Status provisional, L200.)
- Cranium: no controls; guard no exaggerated alien proportions (L210).
- Forehead and brow: forehead height and slope, temple width, brow height, shape and prominence (L211).
- Eyes and orbits: size, depth, spacing, angle, lids, opening, brow-to-eye distance (L212).
- Cheeks and mid-face: high/low, broad/narrow, strong/subtle, full/hollow, soft/angular (L213).
- Nose: short/long, narrow/broad, low/high bridge, straight/convex/concave, projection, tip, nostrils, alar structure (L214).
- Jaw and chin: broad, narrow, strong, soft, angular, rounded; all chins (L215).
- Mouth and lips: width, fullness, projection, Cupid's bow, philtrum, corners, natural asymmetry (L216).
- Ears: overall length, base width, tip length and sharpness, vertical angle, forward/backward sweep, projection, upper-ear curvature, lobe structure and attachment; asymmetry + Restore Symmetry (L231).
- [VAL] Relationship-aware randomization incl. "neck, shoulders and skull", "cranial and facial regions", "ear base and skull attachment" (L441-L450).
- [VAL] Selective randomization groups incl. face and ears, with locks (L456).
- No master slider explicitly forbidden; "Sliders are never rolled independently" (L439).

## 25. Prohibited / forbidden controls and anti-patterns
- [ANAT] No exaggerated alien proportions (L210); delicate/weak brows never required (L211).
- [ANAT] No mandatory upturned, almond, oversized or glowing eyes (L212).
- [ANAT] No Aelari nose type; "High Elf = small, narrow, straight nose" rejected (L214); no Aelari lip type (L216).
- [ANAT] Not universally beautiful, pale, biologically aristocratic or proud (L7); pride/nobility never biological (L71); cultural beauty ideal is culture, not validity (L239).
- [ANAT] "High Elf = pale skin + blond hair + blue or glowing eyes" rejected (L282); magical glow never baked into iris (L312).
- [VAL] Rigid phenotype packages forbidden (L460).
- [PRES] Presentation presets never overwrite face, ears, natural pigmentation (L376, L427).
- [VAL] No preset-only anatomy (L431).
- [VAL] Never solve Sagekin boundary by exaggerating ears (L478).
- [ANAT] ECR: long elegant ears not mandatory (ECR L109); not "permanently aloof" (ECR L125); traits never equal beauty/refinement/nobility (ECR L90).

## 26. Positive identity statement
- "Aelari faces come from combined craniofacial relationships, never from pointed ears alone, one eye shape, one nose, one jaw, conventional attractiveness or cultural styling. They're related to Fenn but a distinct population." (L204)
- "Aelari identity stays statistically present through cranial, orbital, mid-face and jaw relationships" (L243).
- ECR: "Greater average facial verticality" (ECR L282); "Greater facial verticality, longer forehead-to-chin, somewhat narrower lower face, vertical midface, somewhat lighter mandible, longer and narrower visible eyes than Fenn" (ECR L83).

## 27. Cross-population facial boundary tests / comparators
- Fenn (AE-34, AE-46; L243, L479), Sagekin (AE-35, AE-45; L478 "especially important"), Marchfolk (L243, L472), Skarn (brow comparator L211; body L480).
- ECR three-elf neutral face and human boundary (ECR L122, L124).

## 28. Measurement-deferred items (RM-*)
- None. No RM-* refs.

## 29. Presets / randomization / Simple-Advanced
- [CTRL] Character presets (provisional): White-Tower Archivist, Provincial Artisan, Tower Guard, Heavyset Merchant, Broad Craftworker, Traveling Aelari, Foreign-Raised Aelari, Elder Waykeeper (L406-L417).
- [VAL] Preset library varies face, ears, eye color etc.; never teaches one authentic look (L423).
- [VAL] "Every preset is a reproducible configuration of the player's system, with no preset-only anatomy. Simple and Advanced modes share the same appearance data." (L431)
- [VAL] Randomization strengths Subtle / Diverse / Extreme; Extreme never invalid; frequency never blocks manual choice (L435).
- [VAL] Soft correlations, never rigid packages (L460); deterministic generation (L460).
- [VAL] Appearance schema: Simple Mode and Advanced Mode continuity, selective randomization locks (L586).

## Extraction notes
- Ear tendency: Aelari spec "slightly closer to the skull" (L224) is re-expressed by ECR final clarification as lower average lateral projection than Fenn, with no strict ranking vs Vael and "closer to skull" not a separate shape (ECR L324-L332). ECR governs.
- Vael spec's comparative description of Aelari ears ("upward and backward orientation, longer taper", VAEL L279) slightly differs from Aelari's own ("upward orientation", L224); ECR L109 ("more upward and backward orientation") settles it.
- Eyes: Aelari L212 calls "longer and narrower" provisional; ECR L83-L84 classifies it as C (Aelari-specific tendency), with comparison target Fenn.
- Jaw: L210/L215 "relatively light"; ECR clarifies no strict Fenn-vs-Aelari ranking (ECR L142).
- "Exact universal elven ear anatomy waits for the Vael design" (L220) and "Shared elven anatomy isn't finalized until Vael" (L21) are superseded by the ECR (ancestral ear shape still E, ECR L104).
- Brow comparator is named ("than robust humans such as Skarn", L211) — compliant with the terminology rule.
- Cranium "Slightly greater cranial height" (L210) — comparison target unnamed; ECR shared tendency names "equivalent humans" (ECR L77).
