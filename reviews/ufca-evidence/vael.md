> UFCA Phase 1 evidence appendix to `reviews/claude-ufca-01-requirements-matrix.md`. Line references are to the canonical race spec as of commit c076294. Extraction only: no canon is changed, and nothing here is new anatomy. Tags: [ANAT] anatomical requirement · [CTRL] creator-facing control requirement · [VAL] dependency/validator · [PRES] presentation · [DIAG] measurement/diagnostic · [OPEN] open/not authorized.

# UFCA-01 evidence: Vael (Dark Elf)

Source: `specs/vael/VAEL_V1.md` (v1.5, first-pass complete, L1-L3). Facial material lives in v1.2 (L217-L347: craniofacial §1-9, eyes/low-light §10-19, ears/aging/validation §20-32), with facial items also in v1.3 (L349-L443), v1.4 (L445-L552) and v1.5 (L554-L616).
Comparative authority: `reviews/elf-comparative-review.md` (ECR; accepted, authority level 3). It is the comparative biological authority, and the race spec stays authoritative where the ECR doesn't explicitly clarify or supersede it (ECR L3, L302, L346). Refs: `Lnnn` = VAEL_V1.md, `ECR Lnnn` = review.

Status of facial control organization: v1.2 classification block (L221). Facial regions, editing levels, control groupings, slider organization and creator-facing control structure (including ears) = **APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION**. Anatomy, tendencies, variation, relationships, ear biology, identity, validation, required capability, preset and randomization requirements stay approved. Only the final control organization is provisional (input to the UFCA Review).

---

## 0. What the Elf Comparative Review settles for the Vael face

- [ANAT] Shared elven craniofacial ancestry; no universal elf face; no single superficial-morph "Elf Head" unless proven; shared cranial tendencies vs equivalent/robust humans; not enlarged skulls (ECR L77).
- [ANAT] Vael overall face (D): "Less facial elongation than Aelari, compact craniofacial vertical distribution, stronger midface integration, somewhat broader cheeks and orbits than Aelari, more mandibular presence than Fenn and Aelari" (ECR L83).
- [ANAT] Vael brow and orbits (D): "Stronger brow-orbit integration, more orbital definition than Aelari" (ECR L84).
- [ANAT] Vael cheeks and midface (D): "Stronger cheek-midface integration, more structural depth than Aelari"; exact ancestral midface E (ECR L85).
- [ANAT] Nose: shared principle not shape; "Elf = small narrow nose" rejected; Vael nasal frequencies E (ECR L86).
- [ANAT] Jaw/chin (D): "Somewhat more mandibular presence than Fenn and Aelari, still elven" (ECR L87). Clarified: "somewhat greater average mandibular structural presence than Fenn and Aelari, while staying gracile relative to robust human populations" (ECR L142). Shared: lower average mandibular mass than robust humans; never weak, pointed, V-shaped, narrow, feminized or mandatorily delicate (ECR L87).
- [ANAT] Mouth/lips E (ECR L88).
- [ANAT] "Vael traits never equal harsh or villainous faces, permanent angularity or scowls, and Vael orbital structure must never create a permanent angry expression." (ECR L90)
- [ANAT] Eyes: five systems separate (ECR L94). Pupil E — round pupils conservative baseline; no slit/vertical/horizontal for exoticism; non-round needs biological justification and cross-elf review (ECR L99).
- [ANAT] Vael low-light adaptation (D + E): Vael-specific candidate, mechanism unresolved; not retroactively given to Fenn/Aelari; "doesn't require larger eyes, glow, eye shine, slit pupils or daylight blindness"; gameplay OPEN (ECR L100). Environmental adaptation D + E: mechanism candidates pupil response, retinal/photoreceptor sensitivity, light gathering, neural processing, fantasy equivalents; eye shine, tapetum, slit pupils, giant eyes, daylight weakness, color-vision tradeoffs, gameplay bonuses not finalized (ECR L189). Surface-raised Vael may keep inherited ocular biology (ECR L191).
- [ANAT] Ears (D): "Somewhat broader base, more lateral and backward orientation, moderately shorter taper than Aelari, strong skull-attachment integration"; guard "Never universally short, thick or bat-like" (ECR L110). Final clarification: projection "An overlapping, intermediate or broad distribution, characterized more by a broader average ear base and lateral and backward orientation than by one fixed projection value"; no strict Aelari-Vael projection ranking (ECR L324-L330). Matrix: "Broader base, lateral and backward orientation, moderately shorter taper than Aelari" (ECR L283).
- [VAL] Ear overlap locked ("some Vael long ears"); mobility E (ECR L112).
- [ANAT] Pigmentation isn't identity (locked): Vael identity must survive pigmentation neutralization (ECR L161). Iris: no universal elven iris palette; muted violet among possible grounded variants; magic separate (ECR L179).
- [VAL] Three-elf neutral face: "Vael compact vertical distribution and stronger midface" (ECR L122); expression neutrality — fails if Vael look "permanently angry or sinister" (ECR L125).
- [ANAT] Final matrix craniofacial: "More compact vertical distribution than Aelari, more midface and mandibular presence than Fenn and Aelari" (ECR L282); eyes: "Low-light adaptation candidate, mechanism unresolved" (ECR L286).
- [ANAT] Facial hair not prohibited for any elf (ECR L175).
- [OPEN] ECR unresolved register: shared ocular physiology, pupil morphology, Vael low-light mechanism and daylight response (ECR L298).

## 1. Cranial vault / cranial proportions
- [ANAT] "Moderate cranial height, less vertical elongation than Aelari, strong cranium-to-mid-face continuity, moderate to broad width variation, more mid-face presence than Aelari"; guard "Not wide by default. Narrow, balanced and broad faces" (v1.2 §3-8, L239).
- [ANAT] Three-elf facial direction: Vael "Stronger mid-face presence, somewhat broader cheeks and orbits, more compact vertical distribution" (L233); overlapping, no rigid packages (L227).
- [CTRL] Neck: no short, thick-neck stereotype; keeps head support (L123).

## 2. Forehead
- [CTRL] "Forehead height, width and slope, temple width" (L240).

## 3. Brow / supraorbital
- [ANAT] "Somewhat more brow and orbital definition than Aelari, still elven" (L240).
- [CTRL] "brow height, shape and prominence" (L240).
- [ANAT] "No mandatory heavy brows or permanent scowl" (L240).
- [CTRL] Natural asymmetry includes brow height (L294).

## 4. Orbit
- [ANAT] "Orbits trend moderate to somewhat large within elven anatomy, with strong definition and broad eye-size variation" (v1.2 §10-12, L252).
- [ANAT] "somewhat broader cheeks and orbits" (L233).
- [VAL] Randomization preserves "eye to orbit" (L482).

## 5. External eye
- [CTRL] "Eye size, opening, depth, spacing, angle, lids and brow-to-eye distance all vary" (L252).
- [ANAT] "no required upturned, almond, predatory, narrow or giant eyes" (L252); "Enormous eyes are never required, and a small-eyed Vael stays valid if it fits the eventual adaptation" (L252).
- [CTRL] Asymmetry: eye height and opening (L294).
- [VAL] VL-35 Small-eyed valid Vael; VL-36 Larger-eyed valid Vael (L320-L321).
- Canthi / folds: SILENT.

## 6. Ocular anatomy
- [ANAT] Low-light principle: underground history "may plausibly support stronger biological low-light adaptation: grounded, compatible with expressive humanoid faces, subtle rather than nocturnal-animal caricature, and distinct from magic. The mechanism isn't final." (L252); earlier "major design question", nothing assumed about giant/glowing eyes, magical darkvision, daylight blindness, nocturnal anatomy (v1.0 §14, L55).
- [OPEN] Mechanism candidates: pupil dilation range, retinal sensitivity, rod/cone (or fantasy-equivalent) balance, light-gathering efficiency, neural processing; none chosen; "No tapetum-like eye shine unless reviewed" (L258).
- [OPEN] Pupil shape unresolved; not automatically vertical, horizontal or permanently enlarged; round human-like pupils a valid candidate (L259).
- [OPEN] Daylight: no assumed severe weakness; sensitivity, adaptation speed, discomfort, gameplay open; Vael function in shared above-ground spaces (L260).
- [ANAT] Iris vs magic split holds; never biologically required to have glowing eyes; "pigmentation never stands in for actual ocular anatomy" (L264).
- [ANAT] Iris families: brown, amber, muted hazel-like, gray, blue-gray, green-gray, muted violet where validated, very dark, other grounded variants; frequencies provisional; "Natural Vael eyes never glow automatically, and emissive eyes are never used just to make them visible in the dark"; eye shine not assumed (v1.3 §16-18, L399).
- [OPEN] Gameplay low-light vision OPEN; anatomy never automatically a gameplay bonus (L59, L268).
- [VAL] Low-light validation lighting set: bright daylight, overcast, interior, firelight, moonlight, very low light, magical, creator studio, cinematic close-ups (L272); VL-41 Low-light eye test, VL-42 Bright-daylight eye test (L326-L327); VL-59 Neutral daylight, VL-60 Very low light (L543-L544).
- [VAL] Daylight/low-light test: no arbitrary eye glow, skin glow, color shift or magical effect; ocular response from approved eye biology and rendering (L509).
- [ANAT] Technical handoff eyes: no emissive eyes, cat pupils, eye shine, giant eyes or severe daylight weakness assumed; biological vs magical separate (L580).
- [OPEN] Aging vs specialized eye anatomy: must be tested; elderly vision effects unresolved (L290).
- [PRES] Eye materials are protected prototype systems (L608).
- Sclera, nictitating membrane: SILENT.

## 7. Cheek / zygomatic
- [ANAT] "Strong cheek-to-mid-face integration, moderate to high placement, somewhat broader than Aelari" (L241).
- [CTRL] "Narrow or broad, strong or subtle, full or hollow" (L241).
- [ANAT] "Never gaunt by default" (L241).
- [CTRL] Asymmetry: cheek position and fullness (L294).

## 8. Midface
- [ANAT] "Stronger mid-face presence" (L233); "strong cranium-to-mid-face continuity", "more mid-face presence than Aelari" (L239).
- [VAL] Three-elf face test: Vael "Stronger midface integration, more compact craniofacial vertical distribution" (L503).

## 9. Nasal
- [ANAT] "Somewhat stronger nasal and mid-face presence than Aelari" (L242).
- [CTRL] "Full diversity: length, width, bridge, profile, projection, tip, nostrils, alar structure" (L242).
- [ANAT] "Never 'one large nose type'" (L242).
- [CTRL] Asymmetry: nose deviation (L294).
- [VAL] VL-28 Strong-nosed (L313).

## 10. Mouth / lips
- [ANAT] "No Vael lip type" (L244).
- [CTRL] "Width, fullness, projection, Cupid's bow, philtrum, corners, asymmetry" (L244).
- [CTRL] Asymmetry: mouth-corner height (L294).
- [ANAT] Living skin regional differences include lips (L367).

## 11. Jaw / mandible
- [ANAT] "Somewhat more jaw presence than Aelari or Fenn, still elven" (L243).
- [CTRL] "All jaw and chin variation" (L243).
- [ANAT] "No required sharp jaw, pointed chin or V-shaped face" (L243).
- [CTRL] Asymmetry: jaw and chin (L294).
- [VAL] VL-29 Strong-jawed (L314).

## 12. Chin
- [CTRL] All chin variation (L243); no required pointed chin (L243).

## 13. External ear
- [ANAT] Vael tendency (overlapping, never a rigid classifier): "Somewhat broader base, more lateral and backward orientation, moderately shorter taper" (v1.2 §20-22, L280); Fenn and Aelari comparators L278-L279.
- [ANAT] "Vael ears are genuine non-human anatomy" (L282).
- [CTRL] Controls: "overall length, base width, tip length and sharpness, vertical angle, forward and backward sweep, lateral projection, upper-ear curvature, and lobe size and attachment, coherent from skull attachment to tip" (L282).
- [ANAT] "Subtle, reference and long ears are all supported, identity survives subtle ears, and maximum ears stay believable. Vael ears aren't automatically shorter than every Fenn or Aelari ear, since distributions overlap." (L282)
- [CTRL] Asymmetry: height, angle, projection, shape + Restore Symmetry (L286).
- [PRES] Notches, tears, missing tip portions, scarring, piercing damage = acquired (L286).
- [OPEN] Ear mobility unresolved, to ECR (L286, L612); ECR E (ECR L112).
- [VAL] VL-32 Min subtle ears; VL-33 Max ears; VL-34 Ear asymmetry (L317-L319); VL-32/33 in permanent stress set (L604).
- [VAL] Randomization preserves "ear base to skull" (L482).
- [VAL] Headgear: ears never universally clipped, hidden, flattened or shortened (L584).
- [ANAT] Living skin regional differences include ears (L367).

## 14. Teeth / dentition
- SILENT.

## 15. Cranial displays / keratin / horns
- SILENT (none). N/A.

## 16. Skin/surface structures that materially alter facial anatomy
- SILENT for anatomy. Related surface items (pigmentation, not anatomy):
- [ANAT] Living skin: blood-flow influence, perfusion, subsurface variation, regional differences (lips, eyes, ears, palms), freckles/moles/birthmarks or Vael equivalents; never flat or monochrome (L367).
- [VAL] Lighting invariance (proposed universal): stored pigmentation never changes under lighting; neutral-light reference first; never design colors from cave lighting (L371). ECR makes it universal (A) (ECR L165).
- [PRES] Creator neutral reference lighting plus warm/cool/brighter/lower options, future requirement (L588).

## 17. Natural asymmetry
- [CTRL] "The subtle controls are brow height, eye height and opening, cheek position and fullness, nose deviation, mouth-corner height, jaw and chin, and ears. Restore Symmetry stays, and Naturalize Face stays a proposed universal feature pending testing." (v1.2 §27, L294)
- [CTRL] Mouth asymmetry (L244); ear asymmetry (L286).
- [ANAT] Asymmetrical Vael validated (L248).

## 18. Age-related facial change
- [ANAT] "Vael visibly age: facial volume, skin elasticity, eye area, cheeks, jawline, neck, wrinkles, hair density and color, and ear tissue where appropriate." (L290)
- [OPEN] Lifespan and aging rate OPEN DECISION (L290, L612).
- [VAL] If specialized eye anatomy, aging tested against it; elderly vision unresolved (L290).
- [ANAT] Inherited silver vs age depigmentation distinct (L391).
- [VAL] VL-08 Elder; VL-31 Elder face; VL-50 Elder culturally neutral; failure "Aging destroys Vael identity" (L341); preset Deep-City Elder (L463).
- Age triad: SILENT in spec; ECR biological age vs age presentation (ECR L245).

## 19. Sex-related facial tendency
- SILENT for the face. Sex-related statements only for frame (L128) and hair/grooming (L403). ECR: jaw never "feminized" (ECR L87).

## 20. Facial hair biology (incl. eyebrows)
- [ANAT] "Presence, density, texture, length, style, color and graying are all biologically appropriate variation. Facial hair is neither required nor prohibited by Vael ancestry." (v1.3 §15, L395)
- [ANAT] ECR L175 consistent.
- Eyebrows (hair): SILENT (brow controls structural).

## 21. Inherited / mixed development
- N/A. Note L616: Halvren built from established foundations, not humans with pointed ears, 50/50 slider average, Aelari with shorter ears or generic half-elves; mixed ancestry needs its own review. Mixed ancestry listed OPEN (L612).

## 22. Locked validation tests touching the face
- [VAL] Hidden-ear, neutral-complexion test (strict): ears, pigmentation, hair, eye color, presentation neutralized; vs Fenn, Aelari, Sagekin, Marchfolk; identity via craniofacial anatomy (v1.2 §28, L298).
- [VAL] Expression validation: neutral, speech, smile, anger, fear, surprise, sadness, blink, eye movement; never permanently angry, sinister, predatory or suspicious; expression independent of ancestry (L302).
- [VAL] Ordinary-face requirement: plain, soft-featured, broad-faced, narrow-faced, strong-nosed, strong-jawed, round-faced, asymmetrical, elderly validated (v1.2 §9, L248).
- [VAL] Low-light validation (L272).
- [VAL] VL-14 Hidden-ear elven comparison (L94); VL-25 Soft-featured; VL-26 Broad-faced; VL-27 Narrow-faced; VL-28 Strong-nosed; VL-29 Strong-jawed; VL-30 High-body-fat facial; VL-31 Elder face; VL-32 Min ears; VL-33 Max ears; VL-34 Ear asymmetry; VL-35 Small-eyed; VL-36 Larger-eyed; VL-37/38/39 Hidden-ear neutral-complexion Fenn/Aelari/Sagekin comparisons; VL-40 Expression stress; VL-41 Low-light eye; VL-42 Bright-daylight eye (L310-L327).
- [VAL] VL-43 Surface-raised, subtle ears; VL-55 Cliché-convergence counterexample; VL-58 Full-neutralization; VL-59 Neutral daylight; VL-60 Very low light (L527-L544). Permanent stress set includes VL-32, VL-33, VL-43, VL-58, VL-59, VL-60 (L604).
- [VAL] Facial failure conditions (L333-L343): skin color or ears needed; recolored Aelari; subterranean Fenn; require glowing eyes; require enormous eyes; permanently sinister; one facial phenotype dominates; aging destroys identity; low-light becomes animal caricature; technical convenience determines biology.
- [VAL] Surface-Raised validation preset must still read as Vael (counterpart to hidden-ear neutral-complexion face test) (L470).
- [VAL] Cliché-convergence: fails on convergence to charcoal skin, white hair, violet eyes, glowing eyes, lean bodies, sharp/severe faces, identical long ears, sinister presentation, dark clothing (L490).
- [VAL] Full neutralization test, three-elf face row (L498-L505).
- [VAL] Human boundary: "the face isn't exaggerated to make classification easy" (L515).
- [VAL] v1.4 failure (L548).
- [VAL] Camera: faces and eyes read without exaggerated lighting (L588).
- [VAL] ECR tests apply (ECR L122-L125).

## 23. Explicitly OPEN biology touching the face
- [OPEN] Ocular mechanism, pupil shape, daylight sensitivity, gameplay low-light vision (L258-L260, L268, L580, L612).
- [OPEN] Ear mobility (L286, L612).
- [OPEN] Lifespan / aging rate (L290); elderly vision (L290).
- [OPEN] Eye color frequencies (L264, L399, L612); hair frequencies.
- [OPEN] Sun response (L375).
- [OPEN] Nasal frequencies, ancestral midface, ancestral ear (ECR L85-L86, L104).

## 24. Pass 1 provisional creator-control list for the face
(Status provisional, L221.)
- Cranium: narrow, balanced and broad faces; not wide by default (L239).
- Forehead and brow: forehead height, width and slope, temple width, brow height, shape and prominence (L240).
- Cheeks and mid-face: narrow/broad, strong/subtle, full/hollow (L241).
- Nose: length, width, bridge, profile, projection, tip, nostrils, alar structure (L242).
- Jaw and chin: all jaw and chin variation (L243).
- Mouth and lips: width, fullness, projection, Cupid's bow, philtrum, corners, asymmetry (L244).
- Eyes: eye size, opening, depth, spacing, angle, lids, brow-to-eye distance (L252).
- Ears: overall length, base width, tip length and sharpness, vertical angle, forward/backward sweep, lateral projection, upper-ear curvature, lobe size and attachment (L282); asymmetry + Restore Symmetry (L286).
- Natural asymmetry: brow height, eye height and opening, cheek position and fullness, nose deviation, mouth-corner height, jaw and chin, ears; Restore Symmetry; Naturalize Face proposed universal (L294).
- [VAL] Randomization preserves cranial-to-facial, ear base-to-skull, eye-to-orbit (L482); selective groups incl. face, ears, eyes with locks (L482).
- [PRES] Creator lighting options (future) (L588).
- No master slider explicitly forbidden; "Sliders aren't rolled independently" (L482).

## 25. Prohibited / forbidden controls and anti-patterns
- [ANAT] Never dark-skinned Aelari, subterranean Fenn, universally sinister, biologically evil (L7).
- [ANAT] Facial identity never from dark complexion, pointed ears, glowing eyes, one eye/nose/jaw, attractiveness, sinister expressions, cultural styling (L225).
- [ANAT] No mandatory heavy brows or permanent scowl (L240); never gaunt by default (L241); never one large nose type (L242); no required sharp jaw, pointed chin or V-shaped face (L243).
- [ANAT] No required upturned, almond, predatory, narrow or giant eyes (L252); no tapetum eye shine unless reviewed (L258); no emissive eyes for dark visibility (L399); no cat pupils, eye shine, giant eyes, severe daylight weakness assumed (L580).
- [VAL] Rigid packages forbidden (charcoal skin, white hair, violet eyes, etc.) (L486).
- [VAL] Colors never sampled from stylized cave lighting (L371).
- [PRES] Presentation presets never alter anatomy (L439); no preset-exclusive anatomy (L474).
- [VAL] Human boundary: face not exaggerated for easy classification (L515).
- [ANAT] ECR: never universally short, thick or bat-like ears (ECR L110); orbital structure never creates permanent angry expression (ECR L90).

## 26. Positive identity statement
- "Vael faces come from combined craniofacial relationships, never from dark complexion, pointed ears, glowing eyes, one eye, nose or jaw, conventional attractiveness, sinister expressions or cultural styling. With ears hidden, presentation neutral and complexion neutralized, a Vael still belongs to a recognizable Vael distribution." (L225)
- "Vael identity stays statistically present through craniofacial anatomy, so complexion never does the racial-design work." (L298)
- ECR: "More compact vertical distribution than Aelari, more midface and mandibular presence than Fenn and Aelari" (ECR L282).

## 27. Cross-population facial boundary tests / comparators
- Fenn, Aelari, Sagekin, Marchfolk (L298, VL-37/38/39, VL-51/52/53); Skarn (body/face L516); Durrim warning (body, L179).
- ECR three-elf neutral face and human boundary (ECR L122, L124).

## 28. Measurement-deferred items (RM-*)
- None. No RM-* refs.

## 29. Presets / randomization / Simple-Advanced
- [CTRL] Character presets (provisional): Deep-City Engineer, Surface Merchant, Broad Craftworker, Lean Wayfinder, Heavyset Trader, Surface-Raised Vael, Deep-City Elder, Cross-Cultural Traveler; together vary face, ears, eye color etc. (L455-L466).
- [VAL] Surface-Raised validation preset: subtle ears, non-glowing eyes, must still read as Vael (L470).
- [VAL] "Every character preset must be reproducible with the player's own tools, with no preset-exclusive anatomy, and Simple and Advanced Mode keep the same underlying data." (L474)
- [VAL] Strength levels Subtle / Diverse / Extreme (proposed universal) (L478); validity vs frequency (L478).
- [VAL] Soft correlations allowed; rigid packages not (L486). Deterministic generation future (L494).
- [VAL] Appearance data: Simple and Advanced continuity, randomization locks (L600).

## Extraction notes
- Vael orbit wording: spec "somewhat broader cheeks and orbits" (L233), "Orbits trend moderate to somewhat large" (L252); ECR names comparator: "somewhat broader cheeks and orbits than Aelari", "more orbital definition than Aelari" (ECR L83-L84). The size statement "moderate to somewhat large within elven anatomy" is not repeated by ECR.
- Jaw: spec "more jaw presence than Aelari or Fenn" (L243) = ECR (ECR L87, L142), with ECR adding "staying gracile relative to robust human populations".
- Ear projection: spec lists "lateral and backward orientation" (L280); ECR final clarification frames Vael projection as overlapping/intermediate/broad, no strict ranking vs Aelari (ECR L324-L330).
- Vael spec's comparative Aelari ear entry ("upward and backward orientation, longer taper", L279) differs slightly from Aelari's own (AELARI L224); ECR L109 governs.
- Pupil: spec says round human-like pupils "a valid candidate" (L259); ECR upgrades to "conservative baseline" (ECR L99).
- "Naturalize Face" is a proposed universal feature pending testing (L294) — only Vael names it.
- Low-light is the only face-relevant race-specific physiological system among the elves; all mechanism decisions OPEN.
- Lighting invariance proposed universal at L371, made universal (A) by ECR L165.
