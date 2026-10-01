# Aelari Character Customization v1.5 (first-pass complete)

This is the Aelari (High Elf) specification at v1.5, first-pass complete. v1.0 covers elven lineage, core anatomy, limbs, composition and initial validation. v1.1 covers detailed proportions, skeletal relationships and Fenn and Aelari differentiation. v1.2 covers craniofacial anatomy, ear morphology, aging and individuality. v1.3 covers complexion, hair, eyes, personal appearance and cultural presentation. v1.4 covers presets, population-aware randomization and racial validation. v1.5 covers final validation, animation, equipment, world compatibility and technical handoff. It is design only, with no UE5 changes. Aelari share deeper ancestry with Fenn but have their own population anatomy, defined by whole-body vertical elongation. Each version arrived in parts, kept together here. The next race is Vael (Dark Elf), who must never be dark-skinned Aelari or subterranean Fenn, and the Elf Comparative Review follows Vael v1.5.

## 1. Core identity

Aelari are High Elves sharing deeper ancestry with Fenn, with their own population-level anatomical identity. They are never taller Fenn, thin humans with pointed ears, universally beautiful, universally pale, or biologically aristocratic or proud.

## 2. Provisional shared elven foundation

Fenn and Aelari may share ancestral themes:

- a more gracile skeleton than humans
- non-human limb-to-torso relationships
- less apparent joint mass
- distinct hands and fingers
- elven craniofacial foundations
- non-human external ears
- non-human shoulder, ribcage and pelvis relationships

These are provisional themes, not final universal elf anatomy. Shared elven anatomy isn't finalized until Vael have a biological design pass.

## 3. Height (provisional)

| Minimum | Reference | Maximum |
| --- | --- | --- |
| 168 cm (about 5'6") | 190 cm (about 6'3") | 221 cm (about 7'3") |

Height supports Aelari identity but doesn't create it. A minimum-height Aelari is still anatomically Aelari.

## 4. Overall proportional identity

Aelari are built around whole-body vertical elongation, distributed coherently through the cranium, neck, torso, arms and legs. They're never a uniformly scaled human or Fenn with stretched legs.

## 5. Aelari versus Fenn (provisional)

| Race | Proportional identity |
| --- | --- |
| Fenn | More compact-centered elven proportions with relatively long extremities |
| Aelari | Vertical elongation throughout the body, including a longer torso and neck, while keeping elven long limbs |

They look ancestrally related, never like two presets of one elf body.

## 6–8. Torso, shoulders and neck

| Region | Aelari tendency | Guard rails |
| --- | --- | --- |
| Torso | Longer than Fenn relative to height, longer waist transition, moderate chest breadth, relatively shallow depth, elven ribcage relationships | Believable thoracic volume, never implausibly shallow |
| Shoulders and clavicles | Relatively long clavicles, broad shoulder variation, all three frames, lighter shoulder joints than humans or Skarn | Broad Aelari stay Aelari. Gracile never means narrow shoulders |
| Neck | Somewhat longer on average than humans and Fenn. The shoulder-to-neck-to-skull line adds subtly to verticality | Believable range, never exaggerated |

## 9–11. Arms, hands, legs and feet

| Region | Aelari tendency | Provisional Fenn contrast |
| --- | --- | --- |
| Arms | Longer than humans, with elongation spread evenly across upper arm and forearm, and broad variation | Fenn may lean more on forearm length. Not final until comparative validation |
| Hands | Long hands and fingers, relatively narrow breadth, gracile wrists | Exact differences provisional. Grips stay believable for weapons, tools and environments |
| Legs and feet | Distinctly long-legged while keeping the longer torso, with even elongation through thigh and lower leg (not lower leg alone) | Humanoid feet following Aelari skeletal relationships. Exact differences provisional |

## 12. Physical composition

The full system applies: overall muscle, fat distribution, regional development and conditioning. Explicitly supported: Narrow and lean, Narrow and muscular, Balanced, Broad, Broad and highly muscular, high body fat, and elder composition. Aelari identity never depends on thinness.

## 13. Anatomy versus body language (universal)

| Concept | Source |
| --- | --- |
| Anatomical resting alignment | Skeletal and body relationships |
| Cultural and personal body language | Culture, personality, training, occupation, emotion and circumstance |

Aelari anatomy may give an upright neutral silhouette. Pride, nobility, refinement, arrogance and aristocratic posture are never biological.

## 14. Complexion

Complexion isn't finalized in v1.0. Aelari get a dedicated pigmentation, complexion, hair and eye pass. "High Elf = pale skin" is explicitly rejected: white-tower architecture, magic, prestige, clothing and institutions never set biological pigmentation. The Fenn, Aelari and Vael comparative review stays.

## 15. Equal-height Fenn and Aelari test

Compare Fenn and Aelari at about equal height, matched on frame, muscle, fat, age, clothing and pose, with ears hidden. They should look related but anatomically distinct in torso share, neck, shoulders and clavicles, ribcage, arm and leg proportions, joint scale and overall vertical distribution.

## 16. Initial validation characters

| ID | Configuration |
| --- | --- |
| AE-01 | Reference: 190 cm, Balanced |
| AE-02 | Minimum height, 168 cm |
| AE-03 | Maximum height, 221 cm |
| AE-04 | Narrow and lean |
| AE-05 | Broad |
| AE-06 | Broad and high muscle |
| AE-07 | High body fat |
| AE-08 | Elder |
| AE-09 | Short Aelari, human-overlap test |
| AE-10 | Equal-height Fenn comparison |
| AE-11 | Long-torso stress test |
| AE-12 | Valid extreme proportional test |

## 17. Technical foundation

OPEN DECISION: MetaHuman isn't assumed to be the Aelari solution, and the foundation is candidate-only per the conflict audit. Approved anatomy drives later technical evaluation and is never changed to fit the current prototype.

## 18. Status

Aelari v1.0 is complete.

# v1.1 Detailed proportions, skeletal relationships and Fenn/Aelari differentiation

This is design only, preserving v1.0. It arrived in two parts: torso, shoulders, pelvis and joints (§1–8), and limbs, hands, feet and comparative validation (§9–19).

## 1. Core proportional rule (provisional)

| Race | Where the elongation sits |
| --- | --- |
| Fenn | Concentrated in the extremities, around a compact-centered torso |
| Aelari | Distributed continuously through the neck, torso, arms and legs |

The result is related but distinct elven silhouettes, and the difference never comes down to height alone.

## 2–5. Skeletal regions

| Region | Aelari tendency | Guard rails |
| --- | --- | --- |
| Ribcage | Vertically longer than Fenn, moderate width, relatively shallow depth | A functional 3D structure with enough thoracic volume, never an extremely flat or narrow chest |
| Torso and spine | Longer overall torso and waist transition than Fenn. Controls: torso length, ribcage length, width and depth, waist and lumbar length, shoulder width, pelvic width | Spine and ribcage relationships stay coherent |
| Shoulders and clavicles | Relatively long clavicles, broad width variation, light shoulder joints, coherent shoulder-to-neck transition | Broad Aelari gain real skeletal breadth, not just muscle or fat |
| Pelvis | A distinct elven pelvis, not a stock human pelvis with longer legs attached. Stable with long femurs, coherent with the spine, Narrow to Broad variation, plausible muscle attachment, natural locomotion | Exact shape awaits prototyping. No mandatory hip width by race or anatomy configuration |

## 6. Joint scale

Shoulders, elbows, wrists, hips, knees and ankles are gracile compared with humans but structurally sufficient. Gracile never means fragile, and hard minimum boundaries prevent implausibly tiny joints.

## 7. Frame interaction

Narrow, Balanced and Broad change the real skeleton: clavicle, ribcage and pelvic breadth, joint relationships and overall skeletal presence. Frame stays separate from muscle, fat, anatomy configuration, height and presentation.

## 8. Anatomical coupling

The controls are coupled:

- Shoulder width moves the clavicles, upper back and shoulder joints.
- Ribcage width and depth set torso volume.
- Torso length moves the spine, ribcage and waist transition.
- Pelvic width sets hip articulation and upper-leg alignment.
- Limb thickness keeps the joint transitions.

The player sets the intended proportion, and bounded supporting changes keep the anatomy.

## 9–12. Limbs, hands and feet

| Region | Aelari tendency | Controls and guard rails |
| --- | --- | --- |
| Arms | Fairly even elongation across upper arm and forearm | Total length, upper-arm and forearm proportion, thickness, regional muscle. Shoulder, elbow, wrist and hand stay coherent, with no independent segment stretching |
| Hands | Elven hands, not stretched human ones: longer hands, palms and fingers, relatively narrow breadth, gracile wrists | Overall scale, palm length and breadth, finger-length proportion, finger thickness. No per-finger controls yet. Knuckles, finger bases, palm and wrist stay believable. Weapon, tool, shield, object and environment tests later |
| Legs | Elongation spread evenly, not one extremely long segment | Total length, thigh and lower-leg proportion, thigh and calf thickness, regional muscle. Hip, knee, ankle and foot stay coherent |
| Feet | Humanoid, somewhat longer, moderate to narrow breadth, gracile ankle | Foot length and breadth. No prehensile or animal-like feet or exaggerated toes. Exact Fenn and Aelari differences provisional |

## 13. Composition stress test

The tests cover Narrow with low muscle and fat, Narrow and high muscle, Balanced and high fat, Broad and low muscle, Broad and high muscle, Broad and high fat, Elder and athletic, and Elder and high fat. Soft tissue never erases the Aelari skeleton, and muscle never turns Aelari into Skarn.

## 14. Combined-proportion validation (universal rule applied)

Individually valid parameters can combine into an invalid character. Extreme neck, torso, arm, hand, leg and foot length together is the Aelari risk case. Relationship-aware validation or soft constraints are required, and the implementation is unresolved.

## 15–17. Boundary tests

| Test | Compared against | Expected result |
| --- | --- | --- |
| Equal-height, permanent, about 190 cm, ears hidden, matched frame, muscle, fat, age, pose and clothing | Fenn | Fenn more compact-centered with stronger extremities. Aelari more vertically continuous, with a longer torso and neck and evenly spread limb elongation. Related, not identical |
| Human boundary | Similarly tall Marchfolk and Sagekin | Aelari never read as the tallest end of human customization. Check robustness, joints, ribcage, clavicles, pelvis, limbs, hands, feet, and neck and torso |
| Skarn boundary | Skarn, using tall, Broad, muscular Aelari | Aelari keep elven gracility, different joints, torso and ribcage, hands and feet, and mass distribution. Broad muscular Aelari never become narrow Skarn |

## 18. Expanded validation characters

AE-01 to AE-12 stay, and these are added:

| ID | Configuration |
| --- | --- |
| AE-13 | Narrow, low muscle, low fat |
| AE-14 | Narrow and high muscle |
| AE-15 | Balanced and high body fat |
| AE-16 | Broad and low muscle |
| AE-17 | Broad and high muscle |
| AE-18 | Broad and high body fat |
| AE-19 | Maximum supported hand proportions |
| AE-20 | Maximum supported leg and foot combination |
| AE-21 | Equal-height Sagekin comparison |
| AE-22 | Equal-height Fenn comparison |
| AE-23 | Broad muscular Skarn-boundary comparison |
| AE-24 | Maximum-height combined-proportion stress test |

## 19. Status

Aelari v1.1 is complete.

# v1.2 Craniofacial anatomy, ear morphology, aging and individuality

This is design only, preserving v1.0–v1.1. It arrived in two parts: craniofacial anatomy and population identity (§1–8), and ear morphology, aging and individuality (§9–20).

**Classification (race-specific facial-control organization status):** where this spec defines facial regions, editing levels, control groupings, slider organization or other creator-facing control structure (including ear controls), that material is **APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION.** Aelari craniofacial anatomy, population tendencies, valid biological variation, anatomical relationships, ear biology, facial identity, validation, required customization capability and preset and randomization requirements stay approved as established. Only their organization into a final facial-control system is provisional, and the section is kept as input to the Universal Facial Customization Architecture Review after all 13 first-pass races are complete.

## 1. Facial identity principle

Aelari faces come from combined craniofacial relationships, never from pointed ears alone, one eye shape, one nose, one jaw, conventional attractiveness or cultural styling. They're related to Fenn but a distinct population.

## 2–8. Facial regions

| Region | Aelari tendency (population, not mandatory) | Supported variation and guard rails |
| --- | --- | --- |
| Cranium | Slightly greater cranial height, somewhat longer face, longer forehead-to-chin line, somewhat narrower lower face, relatively light jaw | No exaggerated alien proportions |
| Forehead and brow | Smoother, lighter brow on average than robust humans such as Skarn | Forehead height and slope, temple width, brow height, shape and prominence. Delicate or weak brows never required |
| Eyes and orbits | Shared elven orbital foundation. Provisionally, Aelari eyes read somewhat longer and narrower, and Fenn eyes more open | Size, depth, spacing, angle, lids, opening, brow-to-eye distance. No mandatory upturned, almond, oversized or glowing eyes |
| Cheeks and mid-face | Somewhat vertically oriented cheek and mid-face relationships | High or low, broad or narrow, strong or subtle, full or hollow, soft or angular. Composition and age shift soft tissue, not ancestry |
| Nose | No Aelari nose type | Short or long, narrow or broad, low or high bridge, straight, convex or concave, projection, tip, nostrils, alar structure. "High Elf = small, narrow, straight nose" is rejected |
| Jaw and chin | Relatively light jaw on average | Broad, narrow, strong, soft, angular or rounded jaws, and all chins. Broad or muscular Aelari may have substantial jaws |
| Mouth and lips | No Aelari lip type | Width, fullness, projection, Cupid's bow, philtrum, corners, natural asymmetry |

## 9–10. Ears

Fenn and Aelari ears share plausible ancestry without being identical, and both are genuinely non-human (not human ears with stretched tips). Exact universal elven ear anatomy waits for the Vael design.

| Race | Ear tendency (overlapping distributions) |
| --- | --- |
| Aelari | Somewhat more upward orientation, clean gradual taper, slightly closer to the skull, moderate to long length |
| Fenn | Somewhat more outward and backward projection, broad individual variation |

These are never rigid species markers. A short-eared Aelari and a long-eared Fenn are both valid.

## 11–12. Ear customization, asymmetry and damage

The controls are overall length, base width, tip length and sharpness, vertical angle, forward and backward sweep, projection, upper-ear curvature, and lobe structure and attachment, all keeping coherent anatomy. Subtle asymmetry covers height, angle, projection and shape, with Restore Symmetry available. Notches, healed tears, missing tip portions, scarring and piercing damage stay acquired appearance.

## 13. Aging

Aelari visibly age: facial volume, skin elasticity, eye area, cheeks, jawline, neck, wrinkles, hair density and color, and ear tissue where appropriate. High Elves are never assumed to stay permanently youthful. Lifespan and aging rate are an OPEN DECISION.

## 14. Individuality and beauty (universal)

No race is biologically required to be conventionally attractive. Aelari can be attractive, plain, rugged, soft-featured, severe, broad-faced, strong-nosed, strong-jawed, scarred, asymmetrical, elderly or high body fat. Any Aelari cultural beauty ideal belongs to culture, not biological validity.

## 15–16. Facial tests

In the hidden-ear facial test, Aelari are compared with Fenn, Sagekin and Marchfolk, with age and composition matched and hair and presentation neutralized. Aelari identity stays statistically present through cranial, orbital, mid-face and jaw relationships, and perfect classification isn't required. The expression tests cover neutral, speech, smile, anger, fear, surprise, sadness, blink and eye movement, keeping individual and racial anatomy.

## 17. Ear mobility (open)

Aelari ears aren't assumed to move just because they're elves. This is compared across Fenn, Aelari and Vael in the elven anatomy review.

## 18. Halvren implication

Aelari and Fenn faces and ears will inform Halvren later. Halvren aren't designed now and are never assumed to be humans with medium-length ears. The architecture stays flexible for genuinely intermediate ancestry.

## 19. Expanded validation characters

AE-01 to AE-24 stay, and these are added:

| ID | Configuration |
| --- | --- |
| AE-25 | Soft-featured |
| AE-26 | Broad-faced |
| AE-27 | Strong-jawed |
| AE-28 | Large, broad nose |
| AE-29 | High-body-fat facial test |
| AE-30 | Elder |
| AE-31 | Minimum, subtle ear |
| AE-32 | Maximum ear |
| AE-33 | Ear asymmetry |
| AE-34 | Hidden-ear Fenn comparison |
| AE-35 | Hidden-ear Sagekin comparison |
| AE-36 | Facial-expression stress test |

## 20. Status

Aelari v1.2 is complete.

# v1.3 Complexion, hair, eyes, personal appearance and cultural presentation

This is design only, preserving v1.0–v1.2. It arrived in three parts: complexion, pigmentation and eyes (§1–8), hair, grooming and personal identity (§9–16), and white-tower civilization and cultural presentation (§17–27).

## 1. Natural-appearance principle

Aelari are a believable population, never "High Elf = pale skin + blond hair + blue or glowing eyes". White towers, magic, prestige and cultural history never set biological pigmentation.

## 2. Pigmentation range (provisional, valid possibilities only)

| Feature | Valid range |
| --- | --- |
| Skin | Very light or fair, light, warm or neutral beige, golden, olive, bronze, medium brown, deeper brown |
| Undertones | Cool, neutral, warm, golden, olive, and reddish where appropriate |

These are not frequencies.

## 3. Elf population rule

Shared ancestry doesn't mean one elven complexion. Fenn, Aelari and Vael each have their own distributions with expected overlap, and Fenn aren't the default. Aelari frequencies wait for Vael and the Elf Comparative Review.

## 4–5. Skin layers and regional appearance

The universal three layers stay: natural (pigmentation, undertone, complexion, freckles, moles, birthmarks), environmental (tanning, sun, weathering, dryness, roughness, calluses) and applied or acquired (scars, tattoos, makeup, paint, dirt, markings). Natural pigmentation stays separate from tanning. Face, hands, forearms, exposed feet and general exposed skin each show their own history, with no automatic occupation or culture.

## 6. Eyes

Valid iris colors are brown, dark brown, amber, hazel, green, gray, blue, and other grounded elven colors set during the comparative review. Frequencies are unresolved. Blue, pale or luminous eyes are never required.

## 7. Biological iris versus magical eye effects (proposed universal)

| Concept | Source |
| --- | --- |
| Biological iris appearance | Inherited pigmentation and anatomy |
| Magical or supernatural eye effects | Magic, conditions, abilities, artifacts or other non-biological systems |

Magical glow is never baked into normal racial iris color unless explicitly approved. An Aelari with ordinary brown eyes is fully authentic.

## 8. Validity versus frequency

A trait can be valid while being Common, Uncommon or Rare. Rarity never blocks a player's manual choice.

## 9. Hair biology versus hairstyle

| Biological | Presentation |
| --- | --- |
| Texture, density, natural color, hairline | Length, cut, styling, parting, braiding, tying, shaving, accessories, formal and personal grooming |

Long hair is never biologically required.

## 10–11. Texture and natural color

Texture covers straight, wavy, curly, and coiled where valid. Elves aren't universally straight-haired. Natural colors may include black, dark brown, brown, lighter brown, auburn, red, blond and light, plus naturally silver-like or white hair if it's later validated as Aelari biology. Frequencies are OPEN.

## 12. Natural light hair versus aging

If natural silver or white hair becomes a valid inherited trait, it stays distinct from age-related graying. A young Aelari with naturally pale hair and an elder with gray hair are different biological states. This is recorded for the future material and data architecture.

## 13. Facial hair

Facial hair is independent of hairstyle and frame, covering presence, density, style, length, color and graying. Aelari are neither required to be clean-shaven nor required to have facial hair. Frequency is provisional.

## 14. Hair and anatomy independence (universal)

Hairstyle, length and grooming are never locked to sex-related anatomy, frame, physique or occupation.

## 15–16. Personal appearance and cultural hair

Presentation can be meticulous, practical, shaved, short, long, elaborate, weathered, scarred, tattooed, foreign-influenced, minimalist or highly decorated. None of these sets authenticity. Traditional cuts, braids, ties, ornaments, and ceremonial, institutional, military and religious styles are cultural options only, and an Aelari raised elsewhere may use none.

## 17. Biology versus civilization

The old description ("proud elves of the white towers, deeply wise, gifted in magic") becomes inspiration for civilization and reputation. Pride, wisdom, education, status and magical scholarship are never biological. An individual Aelari can be educated or not, magical or not, humble or proud, wealthy or poor, urban or rural, and a soldier, farmer, artisan, sailor, laborer, merchant, scholar or anything else.

## 18. Cultural pillars (provisional)

| Pillar | Covers |
| --- | --- |
| Continuity | Long institutional memory, ancestry, preservation, historical continuity |
| Record | Archives, law, scholarship, documentation, libraries, preserved knowledge |
| Mastery | Long traditions of specialized craft, study, training and refinement |
| Form | Architecture, art, geometry, design, ceremony, intentional aesthetics |
| Arcana | Magical institutions, scholarship and craft |

These are civilizational traditions, not a description of every individual.

## 19. White towers

The white towers are an architectural and cultural tradition, not biology. Possible themes include vertical building, pale stone or other light materials, tall windows, terraces, bridges, courtyards, geometric planning, gardens, observatories and magical structures, public towers, and defensive and civic architecture. Nothing is final now, and not every settlement is identical.

## 20. Cultural visual language

Motifs include vertical lines, arches, layered geometry, symmetry with controlled asymmetry, celestial forms, abstract magical geometry, historical and institutional symbols, regional botanical motifs, and lineage symbolism. Aelari design is never reduced to crowns, gold trim and white robes.

## 21–23. Clothing, jewelry and markings

Clothing varies by region, climate, wealth, occupation, institution, military role, religion, travel, ceremony and taste, from structured layers and fine textiles to work clothes, armor, ceremonial garments and imported materials. Robes aren't universal. Jewelry and objects (rings, earrings, necklaces, bracelets, brooches, circlets, hair ornaments, signets, lineage tokens, insignia, magical implements, craft tools, scholarly instruments, keepsakes) belong to culture, background and identity. Tattoos, paint and markings (decoration, lineage, memorials, institutions, service, religion, magic, life events, regional custom) are never universally required.

## 24. Presentation presets (provisional)

The presets are White-Tower Formal, Artisan Practical, Arcane Institutional, Military Formal, Traveler, Rural/Provincial, Foreign/Urban and Ceremonial. They affect grooming, hair, markings, accessories and clothing, and never overwrite ancestry, skeleton, height, frame, muscle, fat, face, ears or natural pigmentation.

## 25. Cross-cultural validation

| Ancestry | Presentation |
| --- | --- |
| Aelari | Aelari |
| Aelari | Marchfolk |
| Aelari | Sagekin |
| Aelari | Fenn |
| Non-Aelari | Aelari |

Culture never alters biological ancestry.

## 26. Elf Comparative Review

This review is mandatory once Fenn, Aelari and Vael finish first pass. It compares shared ancestry, race-specific skeletons, craniofacial distributions, ears, skin, undertones, hair color and texture, eye color and aging. No Aelari frequencies are final before it.

## 27. Status

Aelari v1.3 is complete.

# v1.4 Presets, population-aware randomization and racial validation

This is design only, preserving v1.0–v1.3. It arrived in three parts: character and presentation presets (§1–5), population-aware randomization (§6–13), and population and racial validation (§14–26).

## 1. Preset architecture

Character presets are complete, editable starting people using the same system as custom characters and NPCs. Presentation presets cover grooming, hairstyle, markings, accessories, clothing and cultural or personal appearance only, and never redefine ancestry.

## 2. Aelari character presets (provisional)

| Preset | Demonstrates |
| --- | --- |
| White-Tower Archivist | An institutional, urban Aelari, without making scholarship biological |
| Provincial Artisan | Practical working presentation outside elite institutions |
| Tower Guard | Physically developed, martial Aelari anatomy |
| Heavyset Merchant | High-body-fat Aelari validity |
| Broad Craftworker | Broad skeletal frame and physical development |
| Traveling Aelari | Practical cross-regional presentation |
| Foreign-Raised Aelari | Aelari ancestry without traditional presentation |
| Elder Waykeeper | Visible age, with Aelari identity kept |

The names are inspiration only. They never permanently assign class, stats, personality, occupation, background, abilities or social status.

## 3. Preset diversity

The library as a whole varies height, frame, muscle, fat, age, face, ears, natural pigmentation, hair texture and color, eye color, grooming and cultural presentation. It must never teach players that there's one authentic Aelari look.

## 4. Presentation presets (provisional)

The presets are White-Tower Formal, Institutional Practical, Artisan, Military, Traveler, Provincial, Ceremonial and Foreign/Urban. They may change hair and grooming, markings, accessories, clothing and styling. They never overwrite ancestry, height, skeleton, frame, proportions, muscle, fat, face, ears or natural skin pigmentation.

## 5. Editable preset rule

Every preset is a reproducible configuration of the player's system, with no preset-only anatomy. Simple and Advanced modes share the same appearance data.

## 6–8. Biological randomization, frequency and strength

Population-aware distributions cover height, frame, proportions, craniofacial anatomy, ears, natural pigmentation, hair color and texture, eye color and other inherited traits. Frequencies stay provisional until the Elf Comparative Review. Validity and frequency are separate (Very Common, Common, Uncommon, Rare): frequency shapes NPCs and randomization and never blocks a manual choice. The strengths are Subtle (near population centers), Diverse (broad validated variation) and Extreme (near valid boundaries, mainly for development and testing). Extreme never means invalid.

## 9. Relationship-aware randomization

Sliders are never rolled independently. The linked relationships are:

- neck, shoulders and skull
- shoulder width, clavicles and upper back
- ribcage and torso
- spine and pelvis
- pelvis and upper-leg alignment
- arm length, upper arm, forearm and hand
- leg length, femur, lower leg and foot
- limb thickness and joint scale
- cranial and facial regions
- ear base and skull attachment

Combined-proportion validation applies.

## 10–11. Selective randomization, and biology versus presentation

Players can randomize the entire character, body, face, ears, hair, natural appearance, skin details, markings or presentation, and lock parameters or groups. For example, they can keep height, face and ears while randomizing hair and presentation. Biological randomization uses ancestry distributions and validity. Presentation randomization uses culture, birthplace, background, region and personal style, and never alters ancestry.

## 12–13. Soft correlations and deterministic generation

Inherited traits may use soft probabilistic correlations, but never rigid phenotype packages ("if skin X, then hair Y and eyes Z"). Aelari stay internally diverse. Generated appearances are reproducible from stored data or seeds, for NPC persistence, save and load, testing, bug reproduction, presets and multiplayer. The implementation is unresolved for both.

## 14. Generic-elf convergence test

Generate a large randomized Aelari sample. It **fails** if it keeps converging on tall, thin, pale, young, conventionally beautiful, narrow-faced, small-nosed, long-haired, light-haired, blue-eyed Aelari with identically pointed ears. Each trait is valid on its own, but together they must never become the only recognizable template.

## 15–16. Composition and ear tests

The composition tests are Narrow and lean, Narrow and muscular, Balanced and high fat, Broad and lean, Broad and muscular, Broad and high fat, Elder and muscular, and Elder and high fat, all keeping Aelari identity. The ear tests use minimum, population-reference and maximum valid ears plus strong valid asymmetry. Identity survives subtle ears, and maximum ears never become caricature.

## 17. Hidden-ear population test

Generate Marchfolk, Sagekin, Fenn and Aelari populations with ears, hair, cultural presentation and clothing differences neutralized. Aelari stay statistically distinguishable through skeletal and craniofacial distributions. Perfect classification isn't required.

## 18–20. Boundary tests

| Compared with | Shared ground | The distinction |
| --- | --- | --- |
| Sagekin (especially important) | Both can be tall, long-limbed and linear | Sagekin stay fully human. Aelari have elven skeletal and craniofacial architecture: joints, ribcage, clavicles, pelvis, neck and torso, limb segmentation, hands, feet, face. Never solved by exaggerating Aelari ears |
| Fenn | Deeper shared ancestry | Compared at equal height, frame, muscle, fat, age and presentation. Fenn are compact-centered with stronger extremities. Aelari are vertically continuous, with a longer torso and neck. Neither is a scaled version of the other |
| Skarn | Can match height, and both can be broad and muscular | Skarn are large, robust humans with more skeletal and mass presence. Aelari are tall, gracile elves with a different mass distribution. Broad muscular Aelari never become lean Skarn |

## 21–22. Cultural neutralization and cross-cultural tests

With White-Tower clothing, institutional symbols, jewelry, traditional hair, cultural markings, magical accessories and ceremonial dress removed, Aelari ancestry stays visible. The cross-cultural pairs are Aelari with Aelari, Marchfolk, Sagekin and Fenn presentation, plus non-Aelari ancestry with Aelari presentation. Culture never alters anatomy.

## 23. Additional permanent validation characters

AE-01 to AE-36 stay, and these are added:

| ID | Configuration |
| --- | --- |
| AE-37 | Short and Broad |
| AE-38 | Short and high muscle |
| AE-39 | Minimum ears, neutral presentation |
| AE-40 | Maximum ears, neutral presentation |
| AE-41 | Dark hair, dark eyes, neutral presentation |
| AE-42 | High body fat, short hair |
| AE-43 | Elder, culturally neutral |
| AE-44 | Foreign-raised presentation |
| AE-45 | Sagekin boundary |
| AE-46 | Fenn boundary |
| AE-47 | Skarn boundary |
| AE-48 | Generic-elf convergence counterexample |
| AE-49 | Diverse randomized Aelari |
| AE-50 | Extreme valid randomized Aelari |

## 24. Failure conditions

Aelari design fails if:

- [ ] Pointed ears are needed to tell them from humans.
- [ ] They're simply taller Fenn.
- [ ] They're simply stretched humans.
- [ ] Broad or muscular Aelari lose elven identity.
- [ ] High-body-fat Aelari lose racial identity.
- [ ] Elder Aelari stop reading as Aelari.
- [ ] Randomization keeps producing one "pretty High Elf" template.
- [ ] Pale skin becomes mandatory.
- [ ] Light hair becomes mandatory.
- [ ] One eye, nose or jaw shape dominates.
- [ ] Cultural presentation is needed to identify ancestry.
- [ ] Valid sliders combine into invalid anatomy.
- [ ] Prototype technical limits redefine approved anatomy.

## 25. Elf Comparative Review

The review isn't performed yet. It happens after Vael's first-pass design and decides what is genuinely shared elven ancestry versus Fenn-, Aelari- or Vael-specific, across anatomy, ears, pigmentation, hair, eyes and aging.

## 26. Status

Aelari v1.4 is complete.

# v1.5 Final validation and technical handoff

This is design and technical handoff planning only, with no UE5 changes. It arrived in three parts: skeleton, animation and movement (§1–8), equipment, cameras and world compatibility (§9–19), and architecture, final validation and completion (§20–29). Aelari v1.0–v1.5 are **first-pass complete**, making Aelari the fifth finished race after Marchfolk, Skarn, Sagekin and Fenn.

## 1. Technical foundation (OPEN DECISION)

None of these is assumed: stock MetaHuman, a stock human skeleton, the Fenn skeleton, uniformly scaled human anatomy, or a fully unique skeleton. Candidate approaches include MetaHuman-derived systems, modified human-compatible systems, a shared hierarchy with race-specific proportions, a race-specific skeleton, retargeting, procedural adjustment, IK, custom deformation and hybrids. None is chosen.

## 2–3. Current state and target requirement

| Label | Statement |
| --- | --- |
| CURRENT IMPLEMENTATION | Aelari use the shared human animation system with uniform scaling, like the other prototype races. This may stay for now, and it isn't the approved Aelari architecture |
| TARGET DESIGN | Animation keeps the approved height, neck, torso, shoulders and clavicles, ribcage, pelvis, arms, forearms, hands, femurs, lower legs, feet and joint scale. Approved anatomy is never distorted to fit the existing animation system |

## 4–5. Landmarks and locomotion

The landmarks checked are shoulder centers, elbows, wrists, hands, spine, pelvis, hip joints, knees, ankles, feet, neck and head, at minimum, reference and maximum height and across Narrow, Balanced and Broad frames. The locomotion tests cover idle, walk, jog and run, sprint if supported, acceleration, deceleration, turning, strafing, crouching, jumping, landing, stairs, slopes, uneven terrain and foot placement. Longer legs never mean simply faster playback or uniform stride scaling.

## 6. Movement identity

Anatomy may shape stride length, step relationships, center of mass, turning, acceleration and deceleration, arm swing and foot placement. Grace, nobility, pride, elegance and magical movement are never biological. They come from training, culture, personality, animation style or circumstance.

## 7–8. IK, contact and grips

The contact tests cover foot IK, hand placement, doors, levers, containers, tables, counters, ladders, climbing and mantling if supported, sitting, sleeping, pickup and contextual points. A 168 cm and a 221 cm Aelari can't share unadjusted contact positions. The grip tests cover one- and two-handed weapons, bows, shields, staves and poles, tools, small objects and environment grips, with no floating or misplaced grips. Canonical equipment never grows with the wielder.

## 9. Clothing and armor

Shirts and tunics, coats, robes, chest and shoulder armor, belts, gloves, pants, leg armor, boots and full-body garments are tested at minimum, reference and maximum height, all three frames, low and high muscle, low and high fat, across ages and at extreme valid proportions. They must avoid clipping, floating, implausible stretching, broken joint deformation and loss of the approved silhouette.

## 10–12. Headgear, hair and ears, gloves and boots

Aelari ears pose the same equipment problem as Fenn ears. The options include ear openings, gear shaped around the ears, internal clearance, race-compatible variants where justified, and hoods for different ear shapes. The ruled-out shortcuts are clipping, universal hiding, flattening and Aelari-only helmets. Hair and headgear combinations are validated across short, long, braided, tied, curly and coiled hair, bald and shaved states, helmets, hoods, hats, circlets, hair ornaments and ear accessories. Gloves and boots follow Aelari hand length, fingers, wrist, foot length and breadth and ankle, never uniformly enlarged human gear.

## 13–14. Cameras and first-person

The creator, third-person, dialogue, cinematic, interaction and first-person (if supported) cameras are validated, with no universal camera height. The maximum-height Aelari needs special attention for doorways, low ceilings, conversation framing, nearby characters and interior cameras. If visible first-person arms exist, they keep Aelari arm, forearm and hand proportions, skin and equipment, and are never generic human arms. First-person support stays in the Decision Register.

## 15–16. World compatibility

The universal rule applies: doors, ceilings, corridors, stairs, chairs, benches, beds, ladders, tables, counters, tunnels and interaction points. The 221 cm Aelari is a mandatory stress case. Aelari-built places may reflect their height distribution while staying usable by intended visitors, and Aelari must function in Marchfolk, Sagekin, Fenn and other shared spaces. Any restriction is deliberate.

## 17–19. Collision, reach, equipment dimensions and mounts

Collision, melee and interaction reach, step height, climbing reach and other size effects stay OPEN. Under the audit rule, individual cosmetic variation within a race gives no automatic gameplay effect, and racial size is a dedicated balance decision. Canonical equipment never scales: the same sword for Marchfolk, Fenn, Aelari and Skarn, with grip, attachment and animation adapting instead. Mounts stay OPEN: height, pelvis, leg length, foot position, proportions, equipment, saddle and harness, and mount anatomy all matter, and there's no generic human riding pose.

## 20–21. Unified data and race-owned biology

Aelari use the same conceptual record as every race: ancestry, skeleton and body, composition, face, age and identity, skin and natural appearance, hair, markings and presentation. They don't have to share a skeleton, mesh, morph implementation, deformation or animation solution. The architecture avoids both 13 unrelated creators and one generic humanoid body. Shared controls are used where they fit, and each race owns its biology, ranges, relationships, distributions, presets, randomization, validation and, where needed, technical implementation.

## 22. Appearance schema and reproducibility

The kept requirements are appearance-data versioning and migration, reproducible generation, preset reproducibility, save and load continuity, Basic and Advanced continuity, and selective randomization locks. The implementation is unresolved.

## 23–24. Validation suite and maximum-height stress character

AE-01 to AE-50 together cover every range, frame, composition, extreme, boundary, cultural, population, animation, expression, IK, grip, equipment, headgear, camera, world and save-reproduction test above. AE-03 (221 cm) is a permanent technical stress character for doors, ceilings, stairs, beds, seating, dialogue, cinematics, all cameras, interaction points, equipment, grips, locomotion and IK. The approved maximum height is never cut to suit the prototype's human scale. A genuine unsolved problem goes back for explicit design review.

## 25. Cross-race technical comparison

| Race | Population |
| --- | --- |
| Marchfolk | Baseline broad human customization |
| Sagekin | Subtly shifted, fully human population |
| Skarn | Large, robust human population |
| Fenn | Compact-centered, gracile elven population |
| Aelari | Vertically elongated, gracile elven population |

This comparison shows whether the technical architecture keeps real anatomy or produces scaled versions of one body.

## 26. Current prototype protection

No changes now to uniform race scaling, the human animation placeholder, Manny and Quinn, serialization, collision, camera, reach, weapons, stats, class restrictions or race models. They remain documented prototype systems, known gaps or open decisions.

## 27. Elf Comparative Review

The review isn't performed until Vael v1.0–v1.5 are complete. It then settles shared elven anatomy, race-specific skeletons, craniofacial distributions, ears, pigmentation and undertones, hair color and texture, eye color, aging and any shared technical architecture. Shared ancestry never automatically means one skeleton.
