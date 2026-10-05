> UFCA Phase 1 evidence appendix to `reviews/claude-ufca-01-requirements-matrix.md`. Line references are to the canonical race spec as of commit c076294. Extraction only: no canon is changed, and nothing here is new anatomy. Tags: [ANAT] anatomical requirement · [CTRL] creator-facing control requirement · [VAL] dependency/validator · [PRES] presentation · [DIAG] measurement/diagnostic · [OPEN] open/not authorized.

# UFCA-01 evidence — Gorrund (specs/gorrund/GORRUND_V1.md, 745 lines)

Status: FIRST-PASS COMPLETE; implementation-level prototype verification DEFERRED (L3, L699, L745). Facial content: Part 1 head rule (L84–90), Part 3 (L285–413), Part 3 clarification "Craniofacial and ear identity" (L415–483), Part 4 eyes/skin/aging (L485–591), Part 5 equipment and final tests (L639–695), final clarification face-body relationship (L733–737). ID prefix: GOR- (formerly GRR- before Pass 2, stated for GOR-BODY/GOR-STRESS, L125).

Class tags: [ANAT] anatomical requirement · [CTRL] creator-facing control requirement · [VAL] internal dependency/validator · [PRES] presentation control · [DIAG] measurement/diagnostic only · [OPEN] open/not authorized.

## 1. Cranial vault / cranial proportions
- [ANAT] Head scale: "Suited to the very large body, avoiding the tiny-head giant, the oversized fantasy-ogre head and a uniformly scaled human head; head-to-height ratio **OPEN**." (Pt3 table, L299)
- [ANAT] Cranial vault: "Suits an intelligent population, never a small braincase, receding primitive skull or extreme sloping forehead to imply brutishness." (L300)
- [ANAT] "> **Gorrund body size, cranial appearance, posture and movement must not be used to imply intelligence.**" (L90)
- [ANAT] Cranial breadth (as corrected): "> **Gorrund trend toward greater cranial breadth relative to cranial height than Marchfolk human reference anatomy, while remaining subject to broad individual variation and relationship-aware validity.**" Population tendency, not every Gorrund exceeding every Marchfolk; at similar displayed head scale, Gorrund cranial breadth "never simply reproduces Durrim's." (Clar. §19–20, L441–443; Pt3 L301 notes "wording corrected"; narrower-headed Gorrund valid)
- [ANAT] Cranial depth: "Meaningful front-to-back depth contributing to three-dimensional identity, never equated with prognathism, a huge nose or a muzzle." (L302)
- [ANAT] Transverse Structural Continuity includes cranial breadth and "temporal and lateral facial transition." (L425)
- [VAL] Relationship: "cranial breadth affects orbit spacing, zygomatic position and jaw breadth." (L371)
- [VAL] Head-body integration test — fails if head designed in isolation from torso, shoulders, moderate neck, all frames and min/ref/max height (L405); Maximum height ~251 cm — fails on "tiny-head giant syndrome" (L406); Minimum height ~208 cm — head-body must still read Gorrund (L407).
- [ANAT] Neck: "moderate vertical neck contribution with high structural integration into the shoulder/torso complex"; no required missing/bull/extremely short neck; never enlarged Durrim. (L46–47, L192)

## 2. Forehead
- [ANAT] "Forehead height, breadth, curvature and hairline vary, with no required low or sloping forehead or heavy frontal bossing." (L308)
- [ANAT] "a low forehead or hairline is never used for an ogre look." (L365)

## 3. Brow / supraorbital
- [ANAT] "Gorrund may have substantial bony brows within their cranial scale, but a heavy brow isn't required, and brow skeleton, eyebrow hair, expression, age and lighting stay separate; a low-brow Gorrund that becomes a generic human fails." (L308)
- [ANAT] Transverse Structural Continuity spans "the lateral brow/orbital margins." (L423, L425)
- [ANAT] Aging never requires a larger brow. (L527)
- [DIAG] GOR-FACE-06 lower brow presence ("proves a heavy brow is unnecessary"); GOR-FACE-07 greater brow presence "without permanent aggression." (L384–385)

## 4. Orbit
- [ANAT] "Orbits integrate into the broad and deep system, varying in dimensions, orientation, spacing, visible opening and soft-tissue coverage." (L308)
- [ANAT] "**bony orbital dimensions are not the same as visible eye opening**." (L308)
- [ANAT] "Eye spacing varies, relationship-aware with cranial breadth, nasal root and zygomatics, never requiring extremely wide or close set." (L308)
- [ANAT] TSC includes "lateral brow and orbital margins, orbital spacing and placement"; TSC "never means … maximum eye spacing." (L425)

## 5. External eye (aperture, lids, canthi, folds)
- [ANAT] "Tiny eyes are never required or used to make Gorrund look large, and smaller, moderate and larger valid openings are supported." (L308)
- [ANAT] "Tiny eyes aren't required, surface phenotype works across the approved eye-opening range." (L521)
- [ANAT] Facial aging affects periorbital tissue. (L527); periorbital soft tissue separate from skeleton (L338).
- Canthi / lid folds specifically: SILENT.

## 6. Ocular anatomy
- [ANAT] "Gorrund eyes are biological humanoid eyes, never made supernatural for non-human identity." (Pt4 §40–50, L521)
- [ANAT] Iris families: "deep, medium and light brown, amber, hazel-like, muted gold-brown, olive-hazel, gray, gray-brown and muted green, with no ordinary glowing yellow, luminous orange, red, pure white, neon green or black-void eyes (separate systems if ever used)." Pigment amount, inner/outer relationships, radial patterning, heterogeneity, limbal appearance vary; never hard-linked to skin. (L521)
- [ANAT] "Sclera are recognizably humanoid, never black, yellow, red or green, with the normal tint range **OPEN**." (L521)
- [ANAT] "Pupils are conventional round, never slit, horizontal or predator for exoticism." (L521)
- [OPEN] "Low-light adaptation is **OPEN**, never inferred from mythology, habitat, iris color or size." (L521)
- [ANAT] Eye surfaces: realistic moisture, tear film, scleral vascularity, reflections "without a wet or slimy monster look." (L521)
- [PRES] Magic-vs-biology: "magical eye glow, emission, veins, markings, hair or coloration layer over biology without redefining it." (L537)
- Nictitating membrane: SILENT.

## 7. Cheek / zygomatic
- [ANAT] "> **Gorrund possess substantial zygomatic structural integration contributing to facial breadth and depth without requiring sharply protruding cheekbones.**" Lateral/forward projection and vertical position vary; prominent cheekbones not mandatory. (L310–312)
- [ANAT] Clarification: "The zygomatic region becomes especially important for Gorrund, not through more cheekbone projection but through coordinated placement and continuity among orbit, zygomatic arch, temporal transition, midface and posterior mandible (morphology for prototyping)." (L435)
- [ANAT] TSC "never means … giant cheekbones." (L425)

## 8. Midface
- [ANAT] "The midface has substantial depth and integration across orbits, zygomatics, maxilla, nasal root and upper dental region, never reduced to 'big nose'; moderate forward projection may be valid without a muzzle, snout or ape-like prognathism." (L312)
- [OPEN] "the prognathism distribution is **OPEN** (limited or moderate variation may exist, extreme isn't required)." (L312)
- [ANAT] Clarification: midface "Participates in a broader transverse framework connecting orbital, zygomatic and maxillary relationships across a large three-dimensional face, never a flat broad midface." (L432)
- [ANAT] Facial depth: "A major multiregional dimension (brow and orbit, zygomatics, midface, maxilla, nasal root, mandible, soft tissue), never one Face Depth slider." (L304)
- [ANAT] Depth role (revised): "Their substantial facial depth supports this broad framework without becoming the dominant proportional specialization." (L293, L423)
- [ANAT] "**Gorrund facial identity is NOT primarily vertical elongation** … Gorrund emphasize **breadth, depth and structural integration** more than verticality, but no individual must maximize breadth and depth together." (L324)
- [ANAT] Facial breadth: "Trends substantial, but **broad-faced is not synonymous with Gorrund**." (L303)
- [CTRL] Required coverage lists "midface depth and vertical contribution." (L371)
- [DIAG] GOR-FACE-04 lower facial depth; 05 greater facial depth "never a muzzle, ape-like face or extreme prognathism"; 14 lower breadth with greater depth (critical); 15 greater breadth with lower depth (critical reciprocal). (L381–382, L391–392)

## 9. Nasal anatomy
- [ANAT] "Nose root height, bridge length and breadth, projection, nasal breadth, tip and nostril dimensions and orientation vary separately, with no mandatory 'ogre nose'; large noses may be valid, moderate ones must be, and a moderate-nosed Gorrund stays recognizable. Greater nasal breadth may occur naturally, but broad face never hard-links to broad nose." (L316)
- [ANAT] Aging never requires a larger nose. (L527)
- [DIAG] GOR-FACE-10 moderate/lower nose size ("proves a large nose is unnecessary"); 11 greater nose size "without becoming the identifier." (L387–388)

## 10. Mouth / lips
- [ANAT] "Mouth width, lip dimensions and projection and commissure position vary, never requiring a huge mouth, thin or thick lips, a downturned mouth or a permanent snarl." (L316)
- [ANAT] "no mandatory fangs or exposed teeth in neutral presentation." (L320)
- [ANAT] Lower-face identity "comes from mandible, chin, mouth and maxilla together, never the jaw alone." (L324)

## 11. Jaw / mandible
- [ANAT] "> **Gorrund possess a structurally substantial mandible with meaningful breadth and depth, integrated into the broad/deep craniofacial system without requiring extreme jaw projection or width.**" (L322)
- [ANAT] "Jaw breadth ranges from lower through moderate to greater, and not every Gorrund is square-jawed; mandibular depth contributes presence without meaning a huge chin, underbite or forward jaw." (L324)
- [ANAT] Clarification: "The ramus and posterior jaw participate more strongly in the transverse framework linking lower-face breadth to the rest of the face, without requiring an extremely broad jaw body, square chin or huge jaw." (L433)
- [ANAT] "underbite, overbite and dental misalignment aren't racial requirements." (L320)
- [ANAT] Aging never requires a larger jaw or prognathism. (L527)
- [DIAG] GOR-FACE-08 narrower jaw ("proves a broad square jaw is unnecessary"); 09 broader jaw "without caricature." (L385–386)

## 12. Chin
- [ANAT] "Chin width, height, projection and shape vary, with no mandatory giant, receding or cleft chin." (L324)

## 13. External ear
- [ANAT] Pt3: "Gorrund need a positive ear identity, never enlarged human ears, elf ears, Grask ears or tiny ogre ears." (L346) "> **Broad, structurally substantial humanoid auricles with strong cranial attachment, meaningful cartilage depth and a rounded-to-angular upper contour rather than an elongated terminal point.**" (L348)
- [ANAT] Projection "generally **short-to-moderate relative to elven and Grask long-ear possibilities** (range **OPEN**)"; never flat circular "ogre ears"; internal cartilage complex; not uniformly thick. Silhouette "strong attachment → broad structured auricle → rounded or mildly angular upper termination." A visibly elongated pointed ear "triggers cross-population review." Lobular region recognizable, varies, no giant lobes. (L350)
- [ANAT] Clarified positive anatomy (governs): "> **Gorrund ears possess a broad, deep auricular bowl with a strongly expressed inner antihelical fold system, while the outer rim remains comparatively broad and structurally continuous rather than narrowing into an elongated point. The auricle sits relatively close to the broad lateral skull through a substantial attachment region, producing a deep, folded ear rather than a thin projecting human or tapered elven silhouette.**" (L449)
- [ANAT] Feature table (L451–458): Auricular bowl — "**Meaningful depth relative to overall ear size**" tendency, never a cavity or funnel (L453); Inner folds — antihelical system clearly expressed, biological cartilage, "never decorative ridges, horn-like structures or armor-like folds" (L454); Outer rim — broadly continuous, non-tapering, never elven/Grask terminal taper (L455); Upper contour — rounded to mildly angular, "a strongly pointed tip is outside the ordinary envelope" (L456); Ear-to-skull — "relatively close to the lateral skull despite substantial absolute size" (L457); Projection — lower, moderate, greater all valid, not hard-locked flat (L458).
- [ANAT] Ear pigmentation coherent across bowl, folds, rim; "no dark ear interiors as a racial marking"; no glowing or fantasy-translucent ears. (L511)
- [ANAT] Ears "never carry the whole race." (L359); "Stronger ear traits never make ears the primary identifier." (L469)
- [VAL] Equipment: close-set, broad-attached deep folded ears validated with helmets, hoods, head wraps, circlets (solutions OPEN). (L640); helmets account for ear anatomy (L639).
- [VAL] Ear material test: rim, inner folds, deep bowl, lobe, attachment "without plastic, stone or excessive translucency." (L553)

## 14. Teeth / dentition
- [ANAT] "Dentition is **functional humanoid** as the first-pass default, detailed dental morphology is **OPEN**, and no specialized diet is set from face shape." (L316)
- [ANAT] "> **Tusks are NOT required for Gorrund racial identity.** A completely non-tusked Gorrund is fully valid and immediately recognizable." (L318)
- [OPEN] "Limited tusk-like canine variation is **OPEN**, kept out of ordinary presets until reviewed and not assumed to resolve the same way as Grask." (L320)
- [OPEN] "Grask possible limited tusk-like canine variation and Gorrund possible limited enlarged or tusk-like canine variation stay **separately OPEN**, never merged into one non-human dental decision or assumed to carry over." (L473)
- [ANAT] No mandatory fangs or exposed teeth in neutral presentation; underbite/overbite/misalignment not racial. (L320)
- [ANAT] Older Gorrund not "toothless" by default. (L527)
- [OPEN] Listed: "detailed dentition and possible limited tusk-like canines." (L695)

## 15. Race-specific cranial displays / keratin / horns
- SILENT / N/A. Only negative: inner ear folds never "horn-like structures." (L454)

## 16. Skin/surface structures that materially alter facial anatomy
- [ANAT] "Default skin is biological humanoid skin, never inherently warty, rocky, leathery, cracked, scaly, bark-like, slimy or callused everywhere." (L513)
- [ANAT] "Warts, lesions, cysts and growths aren't racial identifiers, and 'ogre skin' is never made through pathology." Calluses acquired. (L513)
- [ANAT] No mandatory spots, stripes, mottling, patches or camouflage. (L511)
- [OPEN] Skin thickness and soft-tissue durability OPEN, "never … turning large anatomy into armor." (L513)
- [VAL] Transverse architecture test: "Under flat neutral light, Transverse Structural Continuity stays readable through geometry; fails if only shadows create it." (L555)
- [VAL] Facial depth lighting: "never needing dramatic lighting for the face to read." (L554)

## 17. Natural asymmetry
- [ANAT] "Natural asymmetry in brow, eyes, nose, mouth, jaw and ears is supported." (L342)
- [CTRL] "natural asymmetry" in required coverage. (L371)

## 18. Age-related facial change (and age triad)
- [ANAT] "> **Gorrund visibly age, but aging must not turn them into an increasingly exaggerated ogre caricature.**" (L525)
- [ANAT] Age triad: "Chronological age, apparent biological age and age presentation stay separate, validated across younger, mature and older adults (conceptual states, not brackets)." (L527)
- [OPEN] Lifespan, maturation, fertility, senescence, developmental timing OPEN, no numbers. (L527; also L411)
- [ANAT] "Facial aging can affect fine lines, wrinkles, periorbital, cheek, mouth, jawline and neck tissue, elasticity and texture, while craniofacial identity persists: age never requires a larger brow, jaw, prognathism, nose or ears for ogre effect, and natural cartilage and soft-tissue change is never exaggerated into fantasy growth." (L527)
- [ANAT] "Younger adults already have full skeletal identity, never looking nearly human and 'growing into' the anatomy"; older not warty, toothless, bald, gray or hunched by default. (L527)
- [ANAT] Pt3: "never ageless, permanently old, early-wrinkling or with giant facial growth over time." (L411)
- [OPEN] Graying/whitening onset, progression, prevalence OPEN. (L527)
- [VAL] Age and age-composition matrices — identity preserved "without increasing caricature." (L551)

## 19. Sex-related facial tendency
- [OPEN] "Sex-related facial anatomy is **OPEN**, never assuming human dimorphism transfers, and future differences stay within one Gorrund foundation." (L411)
- [OPEN] Pt1: sex-related anatomy and dimorphism OPEN; never one sex broad/other soft. (L82)
- [OPEN] Sex relationships of facial-hair density/distribution/pattern OPEN (L365); sex-related pigmentation, facial and body hair, pattern loss OPEN, "never assuming human patterns" (L560).
- No R-SEX pointer in this spec. SILENT on any sex facial tendency.

## 20. Facial hair biology (incl. eyebrows)
- [ANAT] "Facial-hair biology stays separate from style, culture and gender presentation, never assuming all or no Gorrund grow heavy beards or that facial hair is coarse or sparse." (L365)
- [ANAT] "A clean-shaven Gorrund is fully recognizable, and facial hair contributes **zero required racial recognition**." (L365)
- [OPEN] Body hair OPEN, never inferred as heavy from size. (L365, L517)
- [ANAT] Scalp, eyebrow, facial, body hair related in color without exact matching. (L517)
- [ANAT] Facial-hair biology never assumes "a mandatory beard, mandatory clean-shaven state or coarse ogre beard (sex and age distributions **OPEN**)." (L517)
- [PRES] Haircuts, braids, shaving, grooming, dye, ornamentation = personal presentation, never biology. (L517)
- [ANAT] Eyebrow hair separate from brow skeleton. (L308)
- [VAL] Facial hair with chin straps, closed helmets, neck armor, high collars — strategy OPEN. (L641)

## 21. Inherited / mixed development
- N/A (Halvren only).

## 22. Locked validation tests touching the face
- [VAL] Core rule: "recognizably Gorrund when bald, clean-shaven, neutrally posed, with neutral expression, ears partially obscured, ordinary pigmentation and no cultural presentation." (L289)
- [VAL] Pt1: body identity recognizable "even if the head is visually neutralized" (L86); identity never relies on tusks, giant jaw, tiny eyes, huge nose, monster face (L88).
- [DIAG] GOR-FACE-01 Neutral Gorrund (moderate everything, central soft tissue, bald, clean-shaven, neutral expression); must read Gorrund. (L375)
- [DIAG] GOR-FACE-02 narrower face; 03 broader face; 04 lower depth; 05 greater depth; 06 lower brow; 07 greater brow; 08 narrower jaw; 09 broader jaw; 10 moderate/lower nose; 11 greater nose; 12 soft-featured; 13 severe-featured ("one valid individual, not canonical"); 14 lower breadth + greater depth (critical); 15 greater breadth + lower depth (critical reciprocal). (L379–392)
- [DIAG] GOR-EAR-01 lower projection/compact; 02 moderate projection; 03 greater auricular breadth; 04 lower valid breadth; 05 more rounded upper contour; 06 more angular upper contour — all keep bowl depth, strong inner folds, substantial rim, broad attachment, non-elongated termination. (L361, L469)
- [VAL] Face test table (L394–407): nose/brow/jaw neutralization (L396); ear neutralization (L397); hair and facial hair (L398); Soft-feature GOR-FACE-12 mandatory — fails if "not ogre enough" (L399); Attractiveness — fails if attractive Gorrund requires moving toward human anatomy (L400); Cross-race neutral faces vs Marchfolk, Skarn, Sagekin, Fenn, Aelari, Vael, Durrim, Grask (L401); vs Skarn — fails if needs tusks, huge brow or fantasy skin (L402); vs Grask — fails if reduced to "vertical-versus-horizontal sliders" (L403); vs Durrim — fails if "one shared dwarf-ogre recipe at different sizes" (L404); Head and body integration (L405); Maximum height (L406); Minimum height (L407).
- [VAL] Ear comparison tests: Grask (fails as "short Grask ears"), Vael, Aelari, Fenn, Humans, Ear neutralization (L352–359); clarified ear comparisons Human, Durrim, Grask, Vael, Aelari, Fenn (L460–467).
- [VAL] Matched-scale diagnostic (head images normalized; fails if distinction disappears when head size normalized) and Body-context diagnostic (body reinforces but never creates identity). (L437)
- [VAL] Updated Durrim/Gorrund face test — fails "if the only distinction is a bigger head, taller body, wider face or different ears." (L475–479)
- [VAL] Part 4: Human overlap, Grask overlap (anatomy incl. "transverse craniofacial architecture and Gorrund ears"), Vael-adjacent, Brown-skin recognition (mandatory), Ear material, Facial depth lighting, Transverse architecture, light/dark-skin cross-population tests. (L545–555, L582–583)
- [VAL] Part 5: Durrim (face) — Durrim compact depth-dominant, Gorrund transversely distributed broad and deep; "absolute size never carries it" (L682); Neutralized recognition (L683); Minimum-stereotype (mandatory) — lower facial breadth, lower brow, moderate nose and jaw, no tusks, softer features, lighter complexion: "still unmistakably Gorrund" (L684); Maximum-caricature risk — max breadth, depth, brow, jaw … "never automatically one valid combination" (L685); Adult read (L686); Biological diversity incl. softer/severe, clean-shaven/facial-haired (L687).
- [VAL] AD-1: Gorrund/Skarn boundary (208 cm Gorrund vs Broad Skarn through 229 cm) passes only on proportional/architectural carriers incl. "craniofacial identity (Transverse Structural Continuity) and ear architecture"; fails if relies on absolute size or Current Muscularity. (L271)
- [VAL] AD-3: GOR-BODY-12/14 vs Broad Grask — "Ears, face, surface phenotype, muscle and absolute height never rescue an otherwise collapsed body architecture." (L244)
- [VAL] GOR-EQUIP-07 helmet across craniofacial and ear variation. (L667)

## 23. Explicitly OPEN biology touching the face
- [OPEN] Head-to-height ratio. (L299)
- [OPEN] Prognathism distribution. (L312)
- [OPEN] Detailed dental morphology; limited tusk-like canine variation (separately from Grask). (L316, L320, L473, L695)
- [OPEN] Ear projection range. (L350)
- [OPEN] Hair density frequencies, texture distribution, pattern hair loss prevalence; body hair; bright blond and bright red boundaries. (L365, L517)
- [OPEN] Sex-related facial anatomy, facial-hair distributions. (L411, L365, L560)
- [OPEN] Scleral tint range; low-light adaptation. (L521)
- [OPEN] Lifecycle; graying timing. (L411, L527)
- [OPEN] Skin thickness/durability; blood biology; flushing; pigment mechanisms. (L506, L511, L513)
- [OPEN] Technical: "Morph implementation, bone-based controls, blendshapes, ear deformation, hair and beard attachment, skin materials and LOD strategy." (L411); "technical facial-control and surface architecture" (L695).
- [OPEN] Ear/headgear and facial-hair/helmet solutions. (L640–641)
- Note: Decision Register authoritative for smaller items (L695).

## 24. Pass 1 provisional creator-control list for the face
- [CTRL] "> **Gorrund face-control organization is an APPROVED FIRST-PASS FUNCTIONAL REQUIREMENT / PROVISIONAL CONTROL ORGANIZATION.** The universal hierarchy waits for the review after all 13 races." (L369)
- [CTRL] "Required coverage (grouping and naming may change): cranial breadth and depth, forehead, brow, orbits, eye spacing, zygomatic breadth and projection, midface depth and vertical contribution, nose, mouth, mandible, chin, ears, biological facial soft tissue and natural asymmetry." (L371)
- [VAL] Relationship-aware validity: "cranial breadth affects orbit spacing, zygomatic position and jaw breadth; facial depth affects midface, nasal root, mandible and soft tissue" — "using valid envelopes rather than hard-locking every correlation"; "maximum cranial breadth, facial depth, brow, nose, jaw and ear breadth together aren't assumed valid." (L371)
- [CTRL]/[VAL] Terminology not sliders: "**Transverse Structural Continuity** is project anatomical terminology, not a creator-facing slider name." (L425); "**Axial Load-Path Continuity** is project anatomical terminology, not a creator-facing slider." (L709)
- [VAL] Face-body: "Axial Load-Path Continuity (body) and Transverse Structural Continuity (face) describe different anatomical systems and never collapse into one universal Gorrund slider … more body continuity never requires more facial continuity, each varying independently within relationship-aware Gorrund limits." (L737)
- [VAL] Soft tissue: "**body-fat amount does not require one deterministic facial-fat value** (weighted, relationship-aware behavior later)." (L338); facial soft tissue responds to composition "coherently but not deterministically" (L228).
- [CTRL] Multidimensional anatomy statements: breadth, depth, height separate (L324); never one Face Depth slider (L304); no "Gorrund width" scalar (L295).
- No named slider list is given; Gorrund supplies coverage only.

## 25. Prohibited controls and anti-patterns
- [VAL] "There's no Ogre-ness, Brutality, Monster, Savagery, Ugliness, Primitive or Toughness control." (L371)
- [VAL] No TSC slider (L425); no ALPC slider (L709); no single Face Depth slider (L304); no "Gorrund width" scalar (L295); TSC "never means a flat face, a wide-face slider, maximum eye spacing, giant cheekbones, a square jaw, horizontal scaling, a rectangular head or reduced depth" (L425).
- [VAL] Not "Durrim = depth, Gorrund = width" (L435); not "wide Grask" (L331); not "giant Durrim head" (L330); not "vertical-versus-horizontal sliders" (L403).
- [VAL] Stereotype preset packages prohibited: "Classic Ogre," "Brute," "Green Ogre," "Fat Ogre," "War Ogre," "Primitive Giant," and "Gentle Giant" or "Civilized Gorrund" as biological phenotypes. (L560)
- [VAL] No preset-only phenotypes/anatomy (L560, L691); never uniform full-range sampling (L560); no hard skin/hair/eye packages (L517, L560).
- [VAL] No separate "generic ogre NPC" system (L691).
- [VAL] Identity never from tusks, fangs, giant jaw, underbite, huge nose, tiny eyes, heavy brow, baldness, scars, warts, ugliness, aggressive expression, fantasy skin color (L291).
- [VAL] Tusk-like canine kept "out of ordinary presets until reviewed." (L320)
- [VAL] Never solve light-skin humanization by darkening skin (L582).

## 26. Positive identity statement for the face
- [ANAT] Pt3 (revised): "> **Gorrund possess a broad, deep and structurally integrated adult craniofacial architecture distinguished by transverse structural continuity across the lateral brow/orbital, zygomatic and posterior mandibular regions. Their substantial facial depth supports this broad framework without becoming the dominant proportional specialization, producing a large three-dimensional craniofacial system rather than a widened human, enlarged Durrim or broadened Grask face.**" (L293)
- [ANAT] Clarification: "> **Gorrund craniofacial architecture emphasizes transverse structural continuity across the upper and middle face: the lateral brow/orbital margins, zygomatic region and posterior mandibular structure participate in a broad load-distributed facial framework, while facial depth remains substantial but is not the primary proportional specialization.**" (L423)
- [ANAT] Clarification summary: "> **Gorrund possess a large broad/deep craniofacial architecture whose distinctive specialization is transverse structural continuity across the lateral brow/orbital, zygomatic and posterior mandibular framework. Their facial depth supports this system without reproducing Durrim compact depth-dominant anatomy. Their ears possess a deep auricular bowl, strongly expressed inner fold architecture, a substantial continuous outer rim and broad skull attachment terminating in a rounded-to-mildly-angular rather than elongated pointed contour.**" (L481)
- [ANAT] "> **Gorrund can be conventionally attractive, ordinary, unusual, severe-featured, soft-featured or weathered.**" (L340)
- [ANAT] Final identity (face portion): "Their craniofacial anatomy is broad and deep but distinguished specifically by transverse structural continuity … rather than Durrim-like compact depth dominance. Their ears possess a deep auricular bowl …" (L693)

## 27. Cross-population facial boundary tests / comparators
- [VAL] Comparison table (L328–334): Durrim — never "giant Durrim head" (L330); Grask (critical) — fails as "wide Grask" (L331); Skarn — distinct "never tusks, giant brow or ugliness" (L332); Aelari (L333); Fenn (L334).
- [VAL] Durrim vs Gorrund regional table: Overall (Durrim compact depth-dominant; Gorrund transversely distributed broad and deep, diagnosis on cranial breadth, lateral orbital framework, zygomatic placement, temporal and lateral structure, ramus and posterior jaw, "none alone"), Midface, Mandible. (L429–433)
- [VAL] Relationship-aware cases: narrower Gorrund keeps TSC within narrower envelope; "a broad-faced Durrim never automatically becomes Gorrund-like (a critical relationship-aware case)"; greater-depth Gorrund keeps transverse framework. (L435)
- [VAL] Matched-scale and body-context diagnostics. (L437)
- [VAL] Ear comparators: Human, Durrim, Grask, Vael, Aelari, Fenn. (L460–467)
- [VAL] Cross-race neutral faces vs Marchfolk, Skarn, Sagekin, Fenn, Aelari, Vael, Durrim, Grask. (L401)
- [VAL] AD-1 Skarn boundary relies on TSC and ear architecture. (L271)
- [VAL] Grask overlap pigmentation test relies on "vertically organized face and Grask ears" vs "transverse craniofacial architecture and Gorrund ears." (L546)
- [VAL] Large-Race Comparative Anatomy Review accepted (Pass 2, AD-1–AD-5); AD-4: Skarn–Gorrund distinction architectural "plus the established craniofacial and auricular differences." (L671)

## 28. Measurement-deferred items (RM-*)
- [DIAG] RM-LR-04: "Numeric validator deferred to approved reference meshes" for GOR-BODY-12/14 vs Broad Grask (body; face/ears cannot rescue). (L244) No facial RM-* item.
- [DIAG] Head-to-height ratio OPEN (L299); zygomatic morphology "for prototyping" (L435).
- [DIAG] FD-STRUCT, FD-SOFT, FD-SURF, FD-HAIR, FD-PRES, FD-OBS; neutral diagnostic state: neutral expression, bald or controlled hair, clean-shaven, no cosmetics/tattoos/scars, neutral lighting, controlled camera, ordinary pigmentation, ears partly obscured. (L371)
- [DIAG] Matched-scale diagnostic normalizes displayed head size. (L437)
- [DIAG] Implementation-level prototype verification DEFERRED; Gorrund Prototype Implementation Conflict Audit pending. (L743–745)

## 29. Presets / randomization / Simple-Advanced statements touching the face
- [CTRL] "Presets sample the same system as custom characters, with no preset-only phenotypes, and eventually span height, frame, composition, facial breadth and depth, transverse architecture, ears, skin, hair, iris and apparent age." (L560)
- [CTRL] "Biological randomization uses Gorrund-valid distributions, frequencies, trait relationships, conditional probabilities and combined-proportion constraints, never uniform full-range sampling"; surface randomization separates validity, frequency and correlation; presentation randomization separate. (L560)
- [CTRL] "Every preset is a legitimate output of the same system available in Advanced customization, with no preset-only anatomy; race-aware randomization preserves anatomy, relationship-aware validity, population distributions, composition independence and surface validity, with no stereotype bundles." (L691)
- [CTRL] NPCs use same foundations; future LOD may simplify facial detail "while keeping recognizable anatomy at intended distances (strategy OPEN)." (L691)
- [CTRL] Tusk-like canines kept out of ordinary presets until reviewed. (L320)
- [CTRL] Presets include at least one lighter complexion (pigmentation, L584).
- Simple Mode: SILENT.

## Extraction notes
- Supersessions: Pt3 identity quote at L293 is explicitly "Revised by the craniofacial and ear clarification" — depth demoted from co-specialization to supporting role; Transverse Structural Continuity is the specialization (L423). Cranial breadth wording "corrected" (L301 → L441: comparator is Marchfolk human reference anatomy). Pt3 ear statement (L348–350) is retained but the clarification (L449–458) adds the deep-bowl/inner-fold/continuous-rim/close-to-skull architecture as the positive definition because L348 alone could overlap human and Durrim ears (L447).
- Pt3 L350 says projection "generally short-to-moderate"; clarification L458 says lower, moderate and greater valid projection all occur and ears aren't hard-locked flat; the tendency concerns size/attachment/projection relationship. Read L458 as governing scope.
- Pigmentation: L495 revised by envelope clarification (L570–589); "earth-toned doesn't mean dark" (L574). Not face-anatomy, but brown-skin and light-skin recognition tests directly load the face (L549, L580–583).
- "Massive"/"long arms" shorthand superseded at body level (L277–283); not facial.
- Two named Gorrund-specific concepts must stay uncoupled: TSC (face) and ALPC (body) (L737).
- Tusk-like canine: OPEN, kept out of ordinary presets, separate from Grask (L320, L473). Spec also says "enlarged or tusk-like" for Gorrund (L473) vs "tusk-like canine" at L320 — minor wording variance.
- GRR- prefix note (L125) explicitly covers GOR-BODY and GOR-STRESS only; GOR-FACE/GOR-EAR/GOR-SKIN/GOR-MOVE etc. have no stated legacy prefix.
- No canthi/eyelid-fold, nictitating membrane, horn/keratin or Simple Mode statements; recorded SILENT.
