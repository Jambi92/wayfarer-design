# Vael Character Customization v1.5 (first pass complete)

This is the Vael (Dark Elf) specification at v1.5, and the Vael first pass is complete. v1.0 covers elven lineage, the core physical foundation, limbs, composition, low-light adaptation and initial validation. v1.1 covers detailed body proportions, skeletal relationships and three-elf differentiation. v1.2 covers craniofacial anatomy, eyes and low-light adaptation, ears, aging and facial validation. v1.3 covers complexion, pigmentation, lighting, hair, eyes, the subterranean environment and cultural presentation. v1.4 covers presets, population-aware randomization and racial boundary validation. v1.5 covers skeleton, animation, movement, eyes, equipment, world compatibility, cameras, lighting and technical handoff. It is design only, with no UE5 changes. Vael share deeper ancestry with Fenn and Aelari as a third distinct elven branch: more compact and deeper-bodied, with somewhat greater structural presence. Each version arrived in parts, kept together here. The Elf Comparative Review v1.0 followed (`reviews/elf-comparative-review.md`).

## 1. Core identity

Vael are Dark Elves sharing deeper ancestry with Fenn and Aelari, with their own population-level anatomy. They are never dark-skinned Aelari, subterranean Fenn, humans with pointed ears, universally sinister or thin elves, or biologically evil, secretive or cruel.

## 2. Provisional shared elven foundation

The provisional ancestral themes stay: a more gracile skeleton than humans, non-human limb and torso relationships, less joint mass, distinct hands and fingers, elven craniofacial foundations, non-human ears, and non-human shoulder, ribcage and pelvis relationships. Universal elven anatomy isn't final until the Vael first pass and the Elf Comparative Review.

## 3. Height (provisional)

| Minimum | Reference | Maximum |
| --- | --- | --- |
| 157 cm (about 5'2") | 178 cm (about 5'10") | 203 cm (about 6'8") |

Height never defines Vael, and minimum, reference and maximum-height Vael share one population identity.

## 4. Three elven branches (provisional)

| Race | Structural direction |
| --- | --- |
| Fenn | Compact-centered, with relatively strong extremity contribution |
| Aelari | Whole-body vertical elongation |
| Vael | More compact, deeper-bodied, with somewhat more structural presence through torso, joints and extremity bases |

"Compact" never means short, dwarven, stocky or automatically muscular.

## 5–8. Torso, shoulders, robustness and pelvis

| Region | Vael tendency | Guard rails |
| --- | --- | --- |
| Torso | Greater torso share than Fenn, deeper ribcage than Fenn or Aelari, moderate width, strong torso-to-pelvis continuity, less elongated than Aelari | Believable thoracic volume, broad variation |
| Shoulders and neck | Moderate clavicles, strong shoulder-to-neck integration, broad width variation, slightly more shoulder-joint presence than Fenn or Aelari | Never automatically broad. Narrow, Balanced and Broad all supported |
| Skeletal robustness | Gracile next to humans (especially Skarn), but more joint presence than Fenn or Aelari at wrists, elbows, knees, ankles, shoulders and hand and foot bases | Never compact Skarn |
| Pelvis | Their own elven pelvis (not human, Fenn or Aelari): stable leg articulation, torso-to-pelvis continuity, Narrow to Broad support, plausible muscle attachment, natural locomotion | Exact shape awaits prototyping |

## 9–12. Arms, hands, legs and feet

| Region | Vael tendency | Guard rails |
| --- | --- | --- |
| Arms | Long relative to humans, less extreme elongation than Fenn or Aelari, balanced upper arm and forearm, a somewhat sturdier wrist transition | Broad variation. Never made by shortening Fenn arms with a slider |
| Hands | Elven proportions, moderately long fingers, somewhat broader palms than Fenn or Aelari, a sturdier wrist and hand base | Controls: overall scale, palm length and breadth, finger-length proportion, finger thickness. No per-finger controls yet |
| Legs | Long relative to humans, somewhat smaller leg share of height than Fenn or Aelari, balanced femur and lower leg, more knee and ankle presence | Hip, knee, ankle and foot stay coherent |
| Feet | Humanoid, moderately elongated, somewhat broader than Fenn or Aelari, stronger ankle-to-foot transition | No prehensile feet, clawed feet or cave-gripping toes. Underground competence needs no gimmicks |

## 13. Physical composition

Vael support the full range of muscle, fat, regional development and conditioning: Narrow and lean, Narrow and muscular, Balanced, Broad, Broad and highly muscular, high body fat, and elder composition (Narrow/Balanced/Broad are Skeletal Frame presets combined with composition). Identity never depends on thinness, muscle or fat.

## 14. Low-light adaptation (major design question)

Vael population history may plausibly include biological adaptation to low light, explored carefully in the later face and eye design. Nothing is assumed about giant eyes, glowing eyes, magical darkvision, daylight blindness or weakness, or nocturnal animal anatomy. Any adaptation stays grounded and keeps faces expressive and humanoid.

## 15. Gameplay vision (OPEN)

The options are better low-light vision than humans, better than Fenn, environmental adaptation with no gameplay bonus, or another balanced approach. No numbers are set and nothing is implemented.

## 16. Anatomy, environment and culture

| Layer | Meaning |
| --- | --- |
| Ancestral biology | Inherited physical traits |
| Environmental adaptation | Biological traits that plausibly developed across populations over time |
| Individual environmental exposure | Weathering or acclimatization within one lifetime |
| Culture | Learned behavior, technology, clothing, architecture, beliefs and traditions |

Underground culture is never automatic biology.

## 17–18. Cross-elf and human boundary tests

Compare Fenn, Aelari and Vael at about equal height, matched on frame, muscle, fat, age, clothing and pose, with ears and presentation hidden. Fenn show a compact center with strong extremities, Aelari whole-body vertical continuity, and Vael a compact, deep-bodied structure with more joint and extremity-base presence. They look related, never recolors or scaled versions of each other. Against similarly sized Marchfolk and Sagekin, Vael stay elven through combined skeletal relationships, not ears or pigmentation.

## 19. Initial validation characters

| ID | Configuration |
| --- | --- |
| VL-01 | Reference: 178 cm, Balanced |
| VL-02 | Minimum height, 157 cm |
| VL-03 | Maximum height, 203 cm |
| VL-04 | Narrow and lean |
| VL-05 | Broad |
| VL-06 | Broad and high muscle |
| VL-07 | High body fat |
| VL-08 | Elder |
| VL-09 | Long-limbed, near the racial boundary |
| VL-10 | Compact-proportioned |
| VL-11 | Equal-height Fenn comparison |
| VL-12 | Equal-height Aelari comparison |
| VL-13 | Equal-height Sagekin comparison |
| VL-14 | Hidden-ear elven comparison |
| VL-15 | Valid extreme proportional test |

## 20. Technical foundation (OPEN DECISION)

MetaHuman isn't assumed to be the Vael solution, and the foundation is candidate-only per the conflict audit. Approved anatomy drives technical evaluation.

## 21. Status

Vael v1.0 is complete.

# v1.1 Detailed body proportions, skeletal relationships and three-elf differentiation

This is design only, preserving v1.0. It arrived in three parts: torso, ribcage, spine, shoulders and pelvis (§1–9), limbs, joints, hands, feet and composition (§10–19), and the three-elf silhouette matrix and boundary validation (§20–30).

## 1. Core proportional rule (refined)

Fenn are compact-centered with strong extremities. Aelari carry elongation vertically through neck, torso, arms and legs. Vael have more compact structural continuity, a deeper torso and somewhat more skeletal presence, still recognizably elven. Vael never become stocky or dwarf-like elves, shortened Skarn, muscular by default, or humans with pointed ears.

## 2. Torso depth is skeletal

Vael torso depth comes from ribcage depth and curvature, the spine-to-ribcage relationship, shoulder placement and the torso-to-pelvis transition. It's never faked with body fat, muscle, an oversized chest or uniform torso scaling. A Narrow, lean Vael keeps it.

## 3–7. Skeletal regions

| Region | Vael tendency | Guard rails |
| --- | --- | --- |
| Ribcage | Deeper front to back than Fenn or Aelari, moderate width, slightly shorter vertically than Aelari, strong 3D volume, smooth into shoulders and waist | No barrel-chest caricature, flat human scaling or Skarn-like mass |
| Spine and waist | Moderate torso length, less extended waist than Aelari, strong torso-to-pelvis continuity, natural lumbar curve. Controls: torso length, ribcage length, width and depth, waist and lumbar length | All relationship-aware |
| Shoulders and clavicles | Moderate clavicles and breadth, strong neck and shoulder integration, more shoulder-joint presence than Fenn or Aelari, broad variation | Frame changes the skeleton, and a Narrow Vael is never a scaled-down Broad Vael |
| Neck | Somewhat shorter relative to the torso than Aelari (relative, not absolute), with broad variation | Keeps head support, shoulder integration, cervical anatomy and full movement. No short, thick-neck stereotype |
| Pelvis | A distinct elven pelvis: torso-to-pelvis continuity, stable with long legs, all three frames, plausible muscle attachment, natural locomotion | No human pelvis plus a slider. Awaits prototype validation |

## 8–9. Frame and coupling

Frame changes the clavicles, ribcage, pelvis, joints and skeletal presence, and stays independent of muscle, fat, height, sex-related anatomy and presentation. The coupled relationships are neck and shoulders, shoulders and clavicles, clavicles and upper back, ribcage width and depth, ribcage and spine, torso length and waist, waist and pelvis, and pelvis and hip. The player sets intent, and the system keeps coherence.

## 10. Joint scale

Shoulders, elbows, wrists, hips, knees and ankles are gracile compared with humans, with somewhat more presence than Fenn or Aelari, always in proportion. Joints are never oversized, and hard bounds prevent thin limbs on implausibly tiny or oversized joints.

## 11–14. Limbs, hands and feet

| Region | Vael tendency | Controls and guard rails |
| --- | --- | --- |
| Arms | Somewhat less relative elongation than Fenn or Aelari, still elven | Total length, upper-arm and forearm proportion, thickness, regional muscle. The chain from shoulder to hand stays coherent |
| Hands | Elven fingers, moderate elongation, broader palm than Fenn or Aelari, stronger wrist-to-hand transition. Never shortened human hands | Scale, palm length and breadth, finger-length proportion, finger thickness. No per-finger controls |
| Legs | Long next to humans, somewhat smaller leg share than Fenn or Aelari | Total length, femur and lower-leg proportion, thigh and calf thickness, regional muscle. Compactness never comes from just shortening legs |
| Feet | Moderate elongation, broader than Fenn or Aelari, stronger ankle-to-foot transition | Length and breadth. Ankle, heel, arch, forefoot and toes stay believable. No prehensile or gripping adaptations |

## 15–18. Composition and stress tests

Muscle, fat, regional development and conditioning stay fully independent. The Vael skeleton survives very low or high muscle, low or high fat, mixed regional development and aging.

| Test | Configuration | Must show |
| --- | --- | --- |
| VL-16 | Narrow, low muscle, low fat | Vael ribcage, torso continuity, joints, limb segmentation, hands and feet, elven ancestry. If identity disappears, the design has failed |
| VL-17 | Broad, high muscle | Still Vael, never Skarn, Durrim or a generic muscular human. Skeleton is judged before soft tissue |
| VL-18 | Balanced or Broad, high fat | Silhouette may change a lot. Vael stay recoverable through skeleton, joints, limbs, hands and feet, head and neck, and movement |

## 19. Combined-proportion validation (universal rule applied)

The Vael risk combinations are: deep ribcage with a Narrow frame, Broad frame with long limbs, short torso with long legs, long torso with shorter valid limbs, large hands with narrow wrists, broad feet with gracile ankles, and maximum height with extreme proportions. The implementation isn't chosen.

## 20–23. Three-elf silhouette matrix (permanent test)

Fenn, Aelari and Vael are tested at the same height, frame, muscle, fat, age, pose and clothing, with ears, hair, pigmentation and cultural presentation neutralized. The goal is population-level differentiation, not perfect individual identification.

| Race | Expected structural signal (provisional) |
| --- | --- |
| Fenn | Compact-centered torso, stronger extremities, longer arms, hands, legs and feet, lower joint mass, relatively shallow torso |
| Aelari | Whole-body vertical continuity, longer neck, torso and waist, evenly long arms and legs, gracile joints, vertically elongated silhouette |
| Vael | Deeper torso, more compact torso-to-limb continuity, more joint presence, sturdier wrist, hand, ankle and foot transitions, moderate elongation, lower center of mass than Aelari |

Differences are never exaggerated until the races look like unrelated species.

## 24. Shared-ancestry test

All three should still plausibly share ancestry. The possible shared signals are gracility compared with humans, elven limb relationships, hand and finger structure, craniofacial and ear ancestry, joint relationships, and shoulder, ribcage and pelvis patterns. All are provisional until the Elf Comparative Review.

## 25–27. Boundaries

| Compared with | Expected result |
| --- | --- |
| Marchfolk and Sagekin (matched height and composition, ears, pigmentation, hair and clothing hidden) | Vael never become human when cultural and fantasy signals are removed |
| Skarn (tall, Broad, muscular Vael against a matched Skarn) | Skarn keep human ancestry, greater robustness and skeletal mass, larger joints and a different torso. Vael keep elven ancestry, gracility, limb segmentation, hands and feet, and torso and pelvis relationships |
| Durrim (warning) | Durrim anatomy is never used to solve Vael compactness. They'll differ in stature, bone proportions, limb share, center of mass, joints, hands and feet, and torso construction. Durrim weren't designed when this was written, so flexibility stayed; Durrim v1.0 is now FIRST-PASS COMPLETE and the comparison uses it |

## 28. Expanded validation characters

VL-01 to VL-15 stay, and these are added:

| ID | Configuration |
| --- | --- |
| VL-16 | Narrow, low muscle, low body fat |
| VL-17 | Broad and high muscle |
| VL-18 | High body fat |
| VL-19 | Equal-height Fenn body comparison |
| VL-20 | Equal-height Aelari body comparison |
| VL-21 | Equal-height Sagekin comparison |
| VL-22 | Broad muscular Skarn boundary |
| VL-23 | Deep ribcage with Narrow frame stress test |
| VL-24 | Maximum-height combined-proportion stress test |

## 29. Failure conditions

Vael body design fails if:

- [ ] Identity depends on skin color.
- [ ] Identity depends on ears.
- [ ] They become recolored Aelari.
- [ ] They become shortened Fenn.
- [ ] "Compact" becomes dwarf-like.
- [ ] "Deep-bodied" becomes high body fat.
- [ ] They require muscle.
- [ ] Narrow, lean Vael become generic elves.
- [ ] Broad, muscular Vael become Skarn.
- [ ] Valid controls produce incoherent anatomy.
- [ ] Technical convenience overrides approved biology.

## 30. Status

Vael v1.1 is complete.

# v1.2 Craniofacial anatomy, eyes and low-light adaptation, ears and aging

This is design only, preserving v1.0–v1.1. It arrived in three parts: craniofacial anatomy and population identity (§1–9), eyes and low-light adaptation (§10–19), and ear morphology, aging and facial validation (§20–32).

**Classification (race-specific facial-control organization status):** where this spec defines facial regions, editing levels, control groupings, slider organization or other creator-facing control structure (including ear controls), that material is **APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION.** Vael craniofacial anatomy, population tendencies, valid biological variation, anatomical relationships, ear biology, facial identity, validation, required customization capability and preset and randomization requirements stay approved as established. Only their organization into a final facial-control system is provisional, and the section is kept as input to the Universal Facial Customization Architecture Review after all 13 first-pass races are complete.

## 1. Facial identity principle

Vael faces come from combined craniofacial relationships, never from dark complexion, pointed ears, glowing eyes, one eye, nose or jaw, conventional attractiveness, sinister expressions or cultural styling. With ears hidden, presentation neutral and complexion neutralized, a Vael still belongs to a recognizable Vael distribution.

## 2. Three-elf facial direction (overlapping tendencies, no rigid packages)

| Race | Facial tendency |
| --- | --- |
| Fenn | Relatively open orbits, less lower-face mass, compact facial relationships |
| Aelari | Greater facial verticality, long forehead-to-chin line, lighter jaw |
| Vael | Stronger mid-face presence, somewhat broader cheeks and orbits, more compact vertical distribution |

## 3–8. Facial regions

| Region | Vael tendency | Supported variation and guard rails |
| --- | --- | --- |
| Cranium | Moderate cranial height, less vertical elongation than Aelari, strong cranium-to-mid-face continuity, moderate to broad width variation, more mid-face presence than Aelari | Not wide by default. Narrow, balanced and broad faces |
| Forehead and brow | Somewhat more brow and orbital definition than Aelari, still elven | Forehead height, width and slope, temple width, brow height, shape and prominence. No mandatory heavy brows or permanent scowl |
| Cheeks and mid-face | Strong cheek-to-mid-face integration, moderate to high placement, somewhat broader than Aelari | Narrow or broad, strong or subtle, full or hollow. Never gaunt by default |
| Nose | Somewhat stronger nasal and mid-face presence than Aelari | Full diversity: length, width, bridge, profile, projection, tip, nostrils, alar structure. Never "one large nose type" |
| Jaw and chin | Somewhat more jaw presence than Aelari or Fenn, still elven | All jaw and chin variation. No required sharp jaw, pointed chin or V-shaped face |
| Mouth and lips | No Vael lip type | Width, fullness, projection, Cupid's bow, philtrum, corners, asymmetry |

## 9. Ordinary-face requirement

Plain, soft-featured, broad-faced, narrow-faced, strong-nosed, strong-jawed, round-faced, asymmetrical and elderly Vael are all explicitly validated. Vael never require "exotic", severe or conventionally attractive faces.

## 10–12. Low-light principle, orbits and eye shape

Vael underground history may plausibly support stronger biological low-light adaptation: grounded, compatible with expressive humanoid faces, subtle rather than nocturnal-animal caricature, and distinct from magic. The mechanism isn't final. Orbits trend moderate to somewhat large within elven anatomy, with strong definition and broad eye-size variation. Enormous eyes are never required, and a small-eyed Vael stays valid if it fits the eventual adaptation. Eye size, opening, depth, spacing, angle, lids and brow-to-eye distance all vary, with no required upturned, almond, predatory, narrow or giant eyes.

## 13–15. Mechanism, pupils and daylight (all OPEN)

| Question | Current position |
| --- | --- |
| Mechanism | Candidates: pupil dilation range, retinal sensitivity, rod and cone (or fantasy-equivalent) balance, light-gathering efficiency, neural processing, others. None chosen. No tapetum-like eye shine unless reviewed |
| Pupil shape | Unresolved. Not automatically vertical, horizontal or permanently enlarged. Round human-like pupils are a valid candidate, and alternatives need anatomical and visual justification |
| Daylight | No assumed severe daylight weakness. Sensitivity, adaptation speed, bright-light discomfort and gameplay effects are open. Vael are assumed to function in shared above-ground spaces unless design changes that |

## 16–17. Iris versus magic, and eye color

The universal split holds: biological iris appearance is separate from magical or supernatural eye effects. Vael are never biologically required to have glowing eyes. Iris color frequencies wait for v1.3 and the Elf Comparative Review, and pigmentation never stands in for actual ocular anatomy.

## 18. Gameplay vision (OPEN)

No numbers are set. It will be weighed against lore, player readability, usefulness, accessibility, balance, lighting design, rendering and other racial abilities. Anatomical adaptation never automatically means a gameplay bonus.

## 19. Low-light validation

The lighting tests are bright daylight, overcast daylight, interior, firelight, moonlight, very low light, magical lighting, creator studio lighting and cinematic close-ups. The eyes stay believable and readable in all of them.

## 20–22. Ears

| Race | Ear tendency (overlapping, never a rigid classifier) |
| --- | --- |
| Fenn | Somewhat more outward and backward projection, broad variation |
| Aelari | Somewhat more upward and backward orientation, longer taper |
| Vael | Somewhat broader base, more lateral and backward orientation, moderately shorter taper |

Vael ears are genuine non-human anatomy. The controls are overall length, base width, tip length and sharpness, vertical angle, forward and backward sweep, lateral projection, upper-ear curvature, and lobe size and attachment, coherent from skull attachment to tip. Subtle, reference and long ears are all supported, identity survives subtle ears, and maximum ears stay believable. Vael ears aren't automatically shorter than every Fenn or Aelari ear, since distributions overlap.

## 23–24. Ear asymmetry, damage and mobility

Natural asymmetry covers height, angle, projection and shape, with Restore Symmetry available. Notches, tears, missing tip portions, scarring and piercing damage stay acquired. Ear mobility is unresolved, isn't assumed, and goes to the Elf Comparative Review.

## 25–26. Aging

Vael visibly age: facial volume, skin elasticity, eye area, cheeks, jawline, neck, wrinkles, hair density and color, and ear tissue where appropriate. Lifespan and aging rate are an OPEN DECISION. If Vael have specialized eye anatomy, aging must be tested against it. Elderly Vael aren't assumed to lose or keep the same vision, and the gameplay effects are unresolved.

## 27. Natural asymmetry

The subtle controls are brow height, eye height and opening, cheek position and fullness, nose deviation, mouth-corner height, jaw and chin, and ears. Restore Symmetry stays, and Naturalize Face stays a proposed universal feature pending testing.

## 28. Hidden-ear, neutral-complexion test (strict)

With ears, skin pigmentation, hair, eye color where practical and cultural presentation neutralized, compare Vael against Fenn, Aelari, Sagekin and Marchfolk. Vael identity stays statistically present through craniofacial anatomy, so complexion never does the racial-design work.

## 29. Expression validation

The expressions are neutral, speech, smile, anger, fear, surprise, sadness, blink and eye movement. Vael never look permanently angry, sinister, predatory or suspicious, and expression stays independent of ancestry.

## 30. Expanded validation characters

VL-01 to VL-24 stay, and these are added:

| ID | Configuration |
| --- | --- |
| VL-25 | Soft-featured face |
| VL-26 | Broad-faced |
| VL-27 | Narrow-faced |
| VL-28 | Strong-nosed |
| VL-29 | Strong-jawed |
| VL-30 | High-body-fat facial test |
| VL-31 | Elder face |
| VL-32 | Minimum, subtle ears |
| VL-33 | Maximum ears |
| VL-34 | Ear asymmetry |
| VL-35 | Small-eyed valid Vael |
| VL-36 | Larger-eyed valid Vael |
| VL-37 | Hidden-ear, neutral-complexion Fenn comparison |
| VL-38 | Hidden-ear, neutral-complexion Aelari comparison |
| VL-39 | Hidden-ear, neutral-complexion Sagekin comparison |
| VL-40 | Expression stress test |
| VL-41 | Low-light eye test |
| VL-42 | Bright-daylight eye test |

## 31. Failure conditions

Vael facial design fails if:

- [ ] Skin color is needed to identify them.
- [ ] Pointed ears are needed to identify them.
- [ ] They're recolored Aelari.
- [ ] They're subterranean Fenn.
- [ ] They require glowing eyes.
- [ ] They require enormous eyes.
- [ ] They look permanently sinister.
- [ ] One facial phenotype dominates.
- [ ] Aging destroys Vael identity.
- [ ] Low-light adaptation becomes animal caricature.
- [ ] Technical convenience determines biology.

## 32. Status

Vael v1.2 is complete.

# v1.3 Complexion, hair, eyes, subterranean environment and cultural presentation

This is design only, preserving v1.0–v1.2. It arrived in three parts: complexion, pigmentation and lighting (§1–10), hair, eyes and personal appearance (§11–20), and the subterranean environment and cultural presentation (§21–33).

## 1–3. Pigmentation (directional families, not final swatches)

Vael have a distinctive inherited pigmentation family without being reduced to "Dark Elf = gray skin".

| Aspect | Direction |
| --- | --- |
| Color families | Charcoal, slate, cool gray, neutral gray, warmer gray, blue-gray, muted or desaturated violet, ash-brown, desaturated brown, and other grounded tones found in prototyping |
| Light to dark | Meaningful variation from lighter to deeper values. Not every Vael is extremely dark or gray, and two Vael can differ a lot while clearly one population |
| Undertones | Cool, neutral, warm, blue, violet, reddish, and brown or earth where appropriate. No highly saturated fantasy colors unless testing justifies them |

The target is living tissue, not painted stone.

## 4–5. Living skin and layers

Vael skin shows blood-flow influence, localized redness or equivalent perfusion, subsurface variation, regional differences (lips, eyes, ears, palms), freckles, moles, birthmarks or Vael equivalents, aging and environmental effects. It's never flat or monochrome. The universal Natural, Environmental, Applied and Acquired layers stay.

## 6–7. Lighting invariance and the cave-lighting trap

**Proposed universal:** biological appearance parameters and observed lighting are separate. Stored pigmentation never changes under daylight, moonlight, firelight, magical light, blue cave light or warm interiors, since lighting changes only the rendered look. The creator needs neutral lighting to judge natural appearance. Vael colors are never designed by sampling stylized underground lighting. Every approved family gets a neutral-light reference first, then is tested in other lighting.

## 8–9. Environment and sun

Vael may live deep underground, near the surface, above ground, in mixed settings or abroad, and environmental appearance varies with that. Not every Vael is personally a cave-dweller. Sun response (tanning, burning, pigment change, other reactions) is OPEN, resolved only if useful.

## 10. Elf Comparative Review

Vael pigmentation frequencies aren't final. After Vael v1.5, Fenn, Aelari and Vael are compared for range, undertones, frequencies, shared signals and race-specific adaptations.

## 11–13. Hair

| Aspect | Direction |
| --- | --- |
| Biological versus presentation | Biology: texture, density, natural color, hairline, age changes. Presentation: length, cut, styling, shaving, braiding, tying, accessories, cultural grooming |
| Texture | Straight, wavy, curly, and coiled where valid. Not universally straight. Frequencies provisional |
| Natural color | Black, very dark brown, brown, ash-brown, muted reddish or auburn where valid, inherited gray or silver-like, white or very light where valid. Frequencies OPEN, and white or silver is never required |

## 14. Inherited silver versus aging

If natural silver or white hair is valid, it stays distinct from age-related depigmentation. A young, naturally white-haired Vael and an elderly gray-haired Vael are different states. The same rule applies to Aelari and any other applicable population.

## 15. Facial hair

Presence, density, texture, length, style, color and graying are all biologically appropriate variation. Facial hair is neither required nor prohibited by Vael ancestry.

## 16–18. Eyes

Natural iris families, independent of magic, may include brown, amber, muted hazel-like tones, gray, blue-gray, green-gray, muted violet where validated, very dark, and other grounded Vael variants. Frequencies are provisional. Natural Vael eyes never glow automatically, and emissive eyes are never used just to make them visible in the dark. Any light-dependent eye response must follow the eventual approved eye anatomy, and eye shine isn't assumed.

## 19–20. Personal appearance

Vael can be meticulously groomed, practical, short-haired, long-haired, shaved, elaborately styled, weathered, scarred, tattooed, minimally or highly decorated, or foreign-influenced. None of these determines authenticity. Hair and grooming are never locked to sex-related anatomy, frame, muscle, fat, class or occupation.

## 21. Biology versus culture

Underground history never implies evil, cruelty, secrecy, treachery, religious fanaticism, social hierarchy, magical affinity or personality. These are cultural, historical, institutional or individual possibilities, never biological consequences of living underground.

## 22. Civilization first

Vael civilization is designed first around the practical problems of living underground: air and ventilation, water, food, waste, artificial light, structural stability, excavation, vertical transport, navigation, heat, fuel and energy, materials, trade, communication and defense. Their visual culture partly grows from how they solved these.

## 23. Cultural pillars (provisional)

| Pillar | Covers |
| --- | --- |
| Depth | Knowledge of layered underground spaces, routes, geology and hidden infrastructure |
| Flow | Moving water, air, heat, people and goods through constrained spaces |
| Craft | Stonework, excavation, metallurgy, ceramics, glass, textiles and other regional industries |
| Light | Practical and symbolic traditions of illumination, visibility and controlled darkness |
| Exchange | Trade and contact between underground communities, surface settlements and foreign peoples |

These are civilizational themes, not a description of every Vael.

## 24–26. Settlements, food and lighting (direction only)

Settlements may use natural caverns, excavated chambers, vertical shafts, terraced districts, bridges, tunnels, water channels, wells and reservoirs, ventilation, surface gates, trade stations, farms and industrial districts. Not every settlement is a giant cave city. Food may come from underground farming, fungi or fantasy equivalents, root crops, surface farming, livestock, fishing, trade and magical agriculture if justified, never mushrooms alone. Lighting may be controlled rather than uniformly bright: fire, oil, candles, bioluminescence, magic, reflectors and other setting-appropriate technology. Nothing is final, and lighting will account for Vael vision once low-light adaptation is settled.

## 27–29. Clothing, presentation and markings

Clothing varies by climate, depth, occupation, wealth, region, institution, surface exposure, trade access, ceremony and taste. It answers practical needs: temperature, abrasion, dust, moisture, climbing, industrial work and surface travel. Black armor and dark robes are never universal. Presentation can be workwear, travel gear, surface clothing, formal urban, industrial or craft, military, ceremonial or foreign-influenced. Accessories may reflect trade, guilds and institutions, family, region, navigation, light sources, tools and personal history. Tattoos, paint, jewelry and markings (decoration, family, region, memorials, craft, service, philosophy and religion, life events, surface or underground community) are never universally required.

## 30. Cultural diversity

There's no single monolithic Vael culture. The civilization supports different underground regions, surface communities, border settlements, trade cities, isolated communities, mixed settlements, foreign-raised Vael and internal political and cultural differences.

## 31–32. Presentation presets and cross-cultural validation

The provisional presentation presets are Deep-City Practical, Surface Traveler, Artisan/Industrial, Merchant, Formal Urban, Military, Ceremonial and Foreign-Raised, and they never alter anatomy. The cross-cultural tests pair Vael ancestry with Vael, Fenn, Aelari and Marchfolk or Sagekin presentation, plus non-Vael ancestry with Vael presentation. Culture never determines ancestry.

## 33. Status

Vael v1.3 is complete.

# v1.4 Presets, population-aware randomization and racial validation

This is design only, preserving v1.0–v1.3. It arrived in three parts: character and presentation presets (§1–6), population-aware randomization (§7–16), and racial boundary and stress validation (§17–29).

## 1. Preset architecture

Character presets are complete, editable starting people built with the same system as custom characters and NPCs. Presentation presets cover grooming, hair, markings, accessories, clothing and cultural styling only, and never redefine ancestry or inherited pigmentation.

## 2–3. Character presets (provisional)

| Preset | Demonstrates |
| --- | --- |
| Deep-City Engineer | Practical urban or subterranean presentation, without making engineering biological |
| Surface Merchant | A Vael who regularly works above ground |
| Broad Craftworker | Broad skeletal frame and physical development |
| Lean Wayfinder | Narrow, lean Vael anatomy without gauntness |
| Heavyset Trader | High-body-fat Vael are valid |
| Surface-Raised Vael | Largely non-Vael presentation, a critical ancestry test |
| Deep-City Elder | Visible aging without losing Vael identity |
| Cross-Cultural Traveler | Mixed regional and personal presentation |

The names are inspiration only and never assign class, stats, personality, occupation, background, abilities or social status. Together the presets vary height, frame, muscularity, body fat, age, face, ears, skin, undertone, hair texture and color, eye color, grooming and presentation, so the library never teaches one "correct" Vael.

## 4. Surface-Raised validation preset

This preset uses reference height, a Balanced or Narrow frame, moderate composition, brownish or desaturated natural pigmentation, dark natural hair, non-glowing eyes, subtle ears, ordinary above-ground clothing and no subterranean decoration. It must still read as Vael, or identity is leaning on presentation. It's the body-and-presentation counterpart to the v1.2 hidden-ear, neutral-complexion face test.

## 5–6. Presentation presets and the editable rule

The presentation presets are Deep-City Practical, Surface Traveler, Artisan/Industrial, Merchant, Formal Urban, Military, Ceremonial and Foreign-Raised. Every character preset must be reproducible with the player's own tools, with no preset-exclusive anatomy, and Simple and Advanced Mode keep the same underlying data.

## 7–9. Population-aware randomization

Biological randomization uses population distributions for height, frame, proportions, craniofacial anatomy, ears, pigmentation, undertones, hair color and texture, eye color and other inherited traits. Frequencies stay provisional until the Elf Comparative Review. Validity and frequency stay separate: a valid trait can be Very Common, Common, Uncommon or Rare, which affects procedural generation but never blocks manual selection. The strength levels (proposed universal) are Subtle (central), Diverse (broad validated) and Extreme (near validated boundaries, never invalid).

## 10–11. Relationship-aware and selective randomization

Sliders aren't rolled independently. Randomization preserves neck to shoulders, shoulders to clavicles, ribcage to spine, torso to pelvis, pelvis to legs, limb thickness to joints, arms to hands, legs to feet, cranial to facial regions, ear base to skull and eye to orbit, with combined-proportion validation. The groups are entire character, body, face, ears, natural pigmentation, hair, eyes, skin details, markings and presentation, and any parameter or group can be locked.

## 12–13. Biology versus presentation, and soft correlations

Biological randomization follows ancestry, while presentation randomization follows culture, region, background and style. A Vael raised in Marchfolk society keeps a Vael skeleton. Soft probabilistic correlations are allowed where justified, but rigid packages (charcoal skin, white hair, violet eyes; or brownish skin, dark hair, brown eyes) aren't.

## 14–15. Cliché-convergence and pigmentation distribution tests

A large randomized population fails if it keeps converging on charcoal or dark-gray skin, white or silver hair, violet eyes, glowing eyes, lean bodies, sharp or severe faces, identical long ears, sinister presentation and dark clothing. Each trait is individually valid, but the combination can't become the only Vael template. Generated Vael must also span lighter, mid and deeper values across gray, blue-gray, violet-influenced and brown or desaturated-brown families, all reading as living skin.

## 16. Deterministic generation

Reproducible generation is a future requirement for NPC persistence, save and load, testing, bug reproduction, presets and multiplayer consistency. No implementation is chosen yet.

## 17–19. Neutralization and three-elf tests

In the full neutralization test, representative Marchfolk, Sagekin, Fenn, Aelari and Vael populations are compared with pigmentation, ears, hair, eye color, clothing, presentation and expression neutralized. Vael must stay statistically distinguishable through skeleton, torso, ribcage, joints, limb segmentation, hands and feet, and craniofacial structure, though perfect individual classification isn't required.

| Test | Fenn | Aelari | Vael |
| --- | --- | --- | --- |
| Body (matched height, frame, muscle, fat, age, pose) | Compact center, stronger extremity contribution | Whole-body vertical elongation | Greater torso depth, compact structural continuity, more joint and extremity-base presence |
| Face (ears, pigment, hair, eye color, expression neutralized) | Open orbital presentation, compact facial relationships | Greater facial verticality | Stronger midface integration, more compact craniofacial vertical distribution |

These are distributions, not mandatory individual markers, and none of the three is a scaled or recolored version of another.

## 20–21. Daylight and low-light tests

Under neutral daylight, with no glow, ordinary clothing, minimal accessories, subtle ears, non-white hair and non-extreme pigmentation, the character must still read as Vael. The same character is then tested under progressively lower light, with no arbitrary eye glow, skin glow, color shift or magical effect. Any ocular response must come from the approved eye biology and rendering.

## 22–26. Boundary, composition and culture tests

| Test | Requirement |
| --- | --- |
| Human boundary | Against similarly sized Marchfolk and Sagekin, Vael stay elven without ears, pigmentation or fantasy clothing, and the face isn't exaggerated to make classification easy |
| Skarn boundary | Broad, high-muscle Vael keep elven gracility and Vael torso, joints, hands, feet and face, while Skarn keep robust human anatomy |
| Composition stress | Narrow lean or muscular, Balanced with high fat, Broad lean, muscular or high-fat, and Elder lean, muscular or high-fat all stay Vael |
| Cultural neutralization | With underground clothing, craft cues, jewelry, markings, traditional hair and lighting cues removed, the character stays biologically Vael |
| Cross-cultural | Vael ancestry in Vael, Fenn, Aelari, Marchfolk and Sagekin presentation, plus non-Vael ancestry in Vael presentation. Culture never alters ancestry |

## 27. Additional validation characters

VL-01 to VL-42 are retained. The new characters are:

| ID | Test |
| --- | --- |
| VL-43 | Surface-raised, subtle ears, neutral clothing |
| VL-44 | Brown or desaturated-brown pigmentation with dark hair |
| VL-45 | Lighter valid pigmentation |
| VL-46 | Deep valid pigmentation |
| VL-47 | Broad, low muscle |
| VL-48 | Broad, high body fat |
| VL-49 | Narrow, high muscularity |
| VL-50 | Elder, culturally neutral |
| VL-51 | Fenn boundary |
| VL-52 | Aelari boundary |
| VL-53 | Sagekin boundary |
| VL-54 | Skarn boundary |
| VL-55 | Cliché-convergence counterexample |
| VL-56 | Diverse randomized Vael |
| VL-57 | Extreme valid randomized Vael |
| VL-58 | Full-neutralization Vael |
| VL-59 | Neutral daylight |
| VL-60 | Very low light |

## 28. Failure conditions

Vael design fails if skin color, ears or underground presentation is needed for recognition; if white hair or glowing eyes are treated as mandatory; if Vael become recolored Aelari or compact Fenn; if narrow or lean Vael become generic elves; if broad or muscular Vael become humans or Skarn; if high-body-fat Vael or elders lose identity; if randomization keeps producing one Dark Elf stereotype; if lighting changes stored pigmentation; or if technical convenience overrides approved anatomy.

## 29. Status

Vael v1.4 is complete.

# v1.5 Technical handoff, validation and completion

This is design and technical handoff planning only, preserving v1.0–v1.4. It arrived in three parts: skeleton, animation, movement and eyes (§1–10), equipment, world compatibility, cameras and lighting (§11–23), and architecture, final validation and completion (§24–35).

## 1–3. Technical foundation

**OPEN DECISION.** Vael aren't assumed to use stock MetaHuman, a stock human skeleton, the Fenn or Aelari skeleton, uniformly scaled human anatomy, or a fully unique skeleton. The candidates are MetaHuman-derived systems, modified human-compatible systems, a shared elven hierarchy with race-specific proportions, race-specific skeletons, retargeting, procedural adjustment, IK, custom deformation and hybrids. None is chosen.

**CURRENT IMPLEMENTATION.** Vael use the shared human animation system with uniform scaling (0.95), like the other prototype races. This may stay untouched for now and isn't the final Vael architecture.

**TARGET DESIGN.** Animation and deformation must preserve Vael height, neck, shoulders and clavicles, ribcage depth, spine, torso, pelvis, arms, elbows and wrists, hands and fingers, femurs, lower legs, knees and ankles, and feet. The torso isn't flattened and joint differences aren't reduced just to fit existing animation.

## 4–8. Landmarks, movement, IK and grips

| Area | Validate |
| --- | --- |
| Landmarks | Head and neck, shoulder centers, elbows, wrists, hands, spine, ribcage, pelvis, hips, knees, ankles and feet, across height, frame, muscle, fat and extreme proportions |
| Locomotion | Idle, walk, jog or run, sprint, acceleration, deceleration, turning, strafing, crouch, jump, land, stairs, slopes, uneven terrain, foot placement |
| Center of mass | Whether torso depth, compact continuity and joint presence meaningfully change balance, turning, acceleration, stride or weight transfer. No bonuses or penalties are invented |
| IK and contact | Foot IK, hand placement, doors, levers, containers, tables, ladders, climbing or mantling, sitting, sleeping, pickups, interaction points |
| Weapons and tools | One-handed, two-handed, bows, shields, staves and poles, tools, small objects, environmental grips, with no floating or misplaced grips |

Movement comes from anatomy and physical state. Sneaking, sinister or predatory movement, grace, aggression and underground expertise are never biological, and can come from skill, training, culture, personality or circumstance instead.

## 9–10. Eyes (technical handoff)

The low-light mechanism stays unresolved biologically and in gameplay. Research areas are pupil behavior, light gathering, retinal and photoreceptor differences, neural processing and fantasy-biological alternatives, with no emissive eyes, cat pupils, eye shine, giant eyes or severe daylight weakness assumed. Approved eyes are later tested under neutral creator light, daylight, overcast, firelight, interiors, moonlight, very low light, magical light and cinematic closeups. Biological eye appearance stays separate from magical or supernatural eye effects.

## 11–14. Clothing, headgear, gloves and boots

Clothing and armor (tunics, coats, robes, chest and shoulder armor, belts, gloves, pants, leg armor, boots, full-body garments) are tested across frame, height, muscle, fat, elder anatomy and extreme proportions. They're watched especially around the deeper Vael ribcage for chest flattening, stretching, floating, clipping, broken joint deformation and loss of silhouette. Headgear options include ear openings, ear-compatible helmets, internal clearance, hoods, hats, circlets and justified race variants, and ears are never universally clipped, hidden, flattened or shortened. Hair (short, long, straight, wavy, curly or coiled, braids, tied, shaved or bald) is tested with helmets, hoods, hats, circlets, ornaments and ear accessories. Gloves and boots must fit Vael hand length, palm breadth, fingers, wrists, foot length and breadth and ankles, so uniformly scaled human gloves and boots aren't assumed to be enough.

## 15–17. Cameras and lighting

The creator, third-person, dialogue, cinematic, interaction and optional first-person cameras are validated, and Vael faces and eyes must read without exaggerated lighting. **Future requirement:** the character creator provides neutral reference lighting plus warm, cool, brighter and lower options for inspection, without changing stored appearance. This isn't implemented yet. Lighting invariance is retained.

## 18–20. World compatibility

Under the universal rule, Vael across their full range must work with doors, ceilings, corridors, stairs, chairs, benches, beds, ladders, tables, counters, tunnels and interaction points. Vael-built spaces may reflect local engineering, but not every Vael location is cramped, not every tunnel fits only Vael, Vael don't automatically reach tiny spaces others can't, and underground doesn't grant automatic movement advantages. Any race-specific access restriction must be deliberate. Shared Marchfolk, Sagekin, Fenn, Aelari and future spaces must work for Vael, and shared Vael settlements must work for others, which matters more once Gorrund, Durrim, Pipkin and Cogling are designed.

## 21–23. Collision, reach, equipment and mounts

**OPEN DECISION:** collision, melee reach, interaction reach, step height, climbing reach and other size effects. Individual cosmetic variation within a race grants no gameplay advantage or penalty, and major racial differences are a separate balance decision. Canonical equipment dimensions don't scale with the holder, though grip, attachment and animation may adapt. Mounts are **OPEN** (pelvis, leg length, foot position, composition, equipment, saddle, mount anatomy, contact points), and generic human riding poses aren't assumed.

## 24–26. Architecture and appearance data

Vael share the high-level character system (ancestry, skeleton and body, composition, face, age, skin, hair, markings, presentation), and shared concepts don't require identical implementation. **Shared ancestry does not automatically require one shared skeleton.** Fenn, Aelari and Vael could use one adaptable elven architecture, closely related race-specific skeletons, a shared hierarchy with different proportions, different skeletons with retargeting, or a hybrid, to be settled by testing. The future appearance-data requirements are unified concepts, schema and version tracking, migration, preset reproducibility, deterministic generation, save and load continuity, Simple and Advanced continuity, and randomization locks, all unresolved.

## 27–28. Validation suite and stress characters

VL-01 to VL-60 together validate height, frame, muscle, fat, age, proportions, combined extremes, faces, ears, pigmentation, hair, eyes, low and bright light, hidden-ear and neutralized-pigment identity, three-elf, human and Skarn boundaries, cultural neutralization, cross-cultural presentation, randomization, cliché convergence, expressions, animation, IK, equipment, headgear, cameras, world compatibility and save and load reproduction. The permanent technical stress set is VL-03 (maximum height), VL-16 (Narrow, low muscle, low fat), VL-17 (Broad, high muscle), VL-18 and VL-48 (high body fat), VL-32 (minimum ears), VL-33 (maximum ears), VL-43 (surface-raised), VL-58 (full neutralization), VL-59 (neutral daylight) and VL-60 (very low light).

## 29. Prototype protection

The following stay untouched as prototype systems, known gaps or open decisions: uniform race scaling, the human animation placeholder, Manny and Quinn, character serialization, collision, camera, reach, weapons, stats, class restrictions, race models, lighting systems and eye materials.

## 30. Open decisions

The open items are Vael lifespan and aging rate; elven lifespan relationships; elven ear mobility; the Vael ocular mechanism and gameplay low-light vision; Vael daylight sensitivity, if any; skin, hair color, hair texture and eye color frequencies; the shared elven ancestry definition; elf skeleton architecture; MetaHuman suitability; morph and deformation architecture; animation and retargeting; equipment fitting; headgear and ear compatibility; first-person support; collision and reach; mounts; race and class restrictions; culture and background architecture; mixed ancestry; gameplay racial attributes; and networked appearance sync.

## 31–35. Completion and next steps

**Vael v1.0–v1.5 first pass is complete.** The completed first-pass races are Marchfolk, Skarn, Sagekin, Fenn, Aelari and Vael. The Elf Comparative Review v1.0 came next (`reviews/elf-comparative-review.md`), sorting features into shared elven ancestry, Fenn-specific, Aelari-specific, Vael-specific and unresolved. It must not force similarities just because all three are elves, or exaggerate differences just to make each instantly identifiable: the goal is believable shared ancestry with believable divergence. Detailed Halvren anatomy waits for the review, and Halvren must be built from established human and elven foundations, not humans with pointed ears, a 50/50 slider average, Aelari with shorter ears or generic half-elves. Mixed ancestry needs its own biological design review.
