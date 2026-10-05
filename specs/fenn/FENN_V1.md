# Fenn Character Customization v1.5 (first-pass complete)

This is the Fenn (Wood Elf) specification at v1.5, first-pass complete: v1.0 covers elven anatomy and the physical foundation, v1.1 covers detailed body proportions, hands and feet, and anatomical relationships, v1.2 covers facial anatomy, ear anatomy, age and individual identity, v1.3 covers skin, hair, forest adaptation and cultural presentation, v1.4 covers presets, population-aware randomization and racial validation, and v1.5 covers final validation and technical handoff. It is design only, with no UE5 implementation. Fenn are the first playable race with a genuinely non-human skeleton, and they are never thin humans with pointed ears. The next race was Aelari (High Elf), who must never simply be taller Fenn.

## 1. Core biological identity

Fenn identity comes from the whole anatomical system:

- limb-to-torso relationships
- long-bone proportions
- skeletal robustness and joint scale
- ribcage, shoulder and clavicle relationships
- pelvis and leg relationships
- hands, fingers and feet
- craniofacial anatomy
- external ears

Pointed ears are only one part.

## 2. Height (provisional)

| Minimum | Reference | Maximum |
| --- | --- | --- |
| 157 cm (about 5'2") | 181 cm (about 5'11") | 211 cm (about 6'11") |

There's substantial overlap with Marchfolk and Sagekin, and height never defines Fenn. These values await visual and technical validation.

## 3. Skeletal foundation

Compared with humans, Fenn trend toward:

- a more gracile skeleton, with lower skeletal mass for their height
- narrower joints and slenderer long bones
- longer limbs relative to the torso
- longer hands and fingers
- longer, somewhat narrower feet
- different shoulder and clavicle relationships
- different pelvis-to-leg relationships

Gracile never means fragile. The anatomy looks naturally adapted, not like weakened human anatomy.

## 4. Skeletal frames

Narrow, Balanced and Broad all apply inside Fenn anatomy. A Broad Fenn is still biologically Fenn, and Narrow isn't the only authentic look.

## 5–7. Region tendencies and controls

| Region | Fenn tendency | Individual controls |
| --- | --- | --- |
| Torso | Slightly smaller torso share of height, somewhat less ribcage depth, more compact chest, longer waist transition | Torso length, ribcage width and depth, shoulder width, waist, pelvis width |
| Arms and hands | Longer arms relative to torso, slightly longer forearms, longer hands and fingers, narrower wrists | Arm length, upper-arm and forearm proportion, hand length and breadth, finger proportion |
| Legs and feet | Greater leg share of height, slightly longer lower legs, narrower ankles, somewhat longer feet than same-height humans | Leg length, thigh and lower-leg proportion, thigh and calf development, foot length and breadth |

Joints and anatomy stay coherent throughout, and nothing is exaggerated into animal-like anatomy.

## 8. Physical composition

Muscle, fat, regional development and conditioning all vary. Very lean, average, Broad-framed, highly muscular, high-body-fat and elder Fenn are all explicitly allowed. Fenn identity never depends on thinness, and muscle and fat modify the Fenn foundation rather than replace it.

## 9. External ears

The ears are real racial anatomy, not an accessory. Possible controls are ear length, width and projection, tip length and angle, upper-ear curvature, and lobe structure. Every setting stays attached and plausible, with no single mandatory oversized ear shape.

## 10. Balance and movement implications (to investigate)

Longer limbs, different torso proportions, a lighter skeleton and different joints may change balance, center of mass and locomotion. Later investigation covers walking, running, turning, crouching, jumping and landing, climbing, balance, swimming and combat stance. Movement differences aren't implemented yet, and cosmetic body settings never give automatic gameplay advantages or penalties.

## 11. Existing gameplay traits

Fenn keep two traits: harder to notice while sneaking, and a somewhat faster swimmer. These aren't implemented, balanced or quantified during design, and no invented anatomy justifies them.

## 12. Human and elf boundary

Sagekin stay fully human, and Fenn have genuinely different elven anatomical relationships. Individual measurements may overlap, but the complete foundations stay distinct.

## 13. Hidden-ear validation

Compare Marchfolk, Sagekin and Fenn of about equal height, matched on frame, muscle, body fat, age, clothing and pose, with Fenn ears hidden. The Fenn must still stand out through limb proportions, joint scale, hands, feet, torso, shoulders, pelvis and legs, and craniofacial anatomy. If a Fenn looks human with ears hidden, the anatomy needs more work.

## 14. Initial validation characters

| ID | Configuration |
| --- | --- |
| FN-01 | Reference: 181 cm, Balanced |
| FN-02 | Minimum height, 157 cm |
| FN-03 | Maximum height, 211 cm |
| FN-04 | Narrow and very lean |
| FN-05 | Broad |
| FN-06 | Broad and highly muscular |
| FN-07 | High body fat |
| FN-08 | Long torso, against the population average |
| FN-09 | Short-limbed, near the racial boundary |
| FN-10 | Hidden-ear human-overlap stress test |

More will be added as the spec develops.

# v1.1 Detailed body proportions, hands and feet, and anatomical relationships

This is design only, preserving v1.0 and all universal rules.

## 1. Structural proportion rule

Proportions behave as connected anatomy, not independent mesh stretching. Changing one region may bring bounded supporting changes in related anatomy. The player sets the intended proportion, and the system keeps it coherent.

## 2–4. Skeletal regions

| Region | Fenn reference direction | Guard rails |
| --- | --- | --- |
| Shoulders and clavicles | Moderately long clavicles, a shallower upper torso than humans, less massive shoulder joints, a clean shoulder-to-neck line, broad individual width variation | Broad Fenn shoulders stay light-boned, never Skarn-like |
| Ribcage and spine | Somewhat shallower front to back, moderately narrow for height, somewhat vertically compact, with a relatively longer waist and lumbar transition | Enough thoracic volume, never an implausibly tiny chest |
| Pelvis and hips | A distinct elven pelvis, not a scaled human one, supporting longer femurs, stable hips, light visual build, Narrow to Broad frames, plausible muscle attachment and natural locomotion | Exact shape awaits prototyping, and not every Fenn has narrow hips |

## 5. Joint scale

Wrists, elbows, knees and ankles look smaller relative to limb length than on same-height humans, with minimum anatomical boundaries. A Narrow, low-muscle, low-fat Fenn never gets implausibly tiny or fragile joints.

## 6–9. Limbs, hands and feet

| Region | Fenn tendency | Controls |
| --- | --- | --- |
| Arms | Longer arms, somewhat greater forearm share | Total length, upper-arm and forearm proportion, thickness, regional muscle. Shoulder, elbow and wrist alignment is kept |
| Hands | Longer palms and fingers, somewhat narrower hands and wrists | Overall hand scale, palm length and breadth, finger length and thickness. No per-finger length controls yet |
| Legs | Greater leg share, slightly greater lower-leg share | Total length, thigh and lower-leg proportion, thigh and calf thickness, regional muscle. Hip, knee and ankle relationships are kept |
| Feet | Somewhat longer and narrower, with normal humanoid toes | Foot length and breadth. No prehensile, gripping or animal-like feet |

Hands stay compatible with weapon grips, shields, tools, environment interactions, animation and IK. Forest and canopy skill doesn't need biological gimmicks.

## 10. Muscle and fat validation

The same composition settings act on each race's own foundation. Highly muscular Marchfolk, Skarn, Sagekin and Fenn are compared: all strongly muscular, all with distinct silhouettes. High-body-fat Fenn are validated too, and soft tissue never erases the Fenn skeleton.

## 11. Combined-proportion validation (proposed universal)

Each parameter can be legal on its own while an extreme combination isn't. For example, maximum arm length, forearm proportion, hand length and finger length together may exceed the supported range. Future customization needs relationship-aware soft constraints or combined-proportion validation. The method isn't chosen yet.

## 12. Human and elf boundary

Sagekin are the long-limbed end of fully human variation, and Fenn have a genuinely different elven skeleton. The difference comes from long-bone relationships, joint scale, hands, feet, ribcage, shoulders and clavicles, and pelvis and legs combined, never just from longer human sliders.

## 13. Expanded validation characters

FN-01 to FN-10 from v1.0 stay, and these are added:

| ID | Configuration |
| --- | --- |
| FN-11 | Broad and high muscle |
| FN-12 | Narrow and high muscle |
| FN-13 | Broad and high body fat |
| FN-14 | Narrow, low muscle and low fat: joint stress test |
| FN-15 | Maximum supported arm and hand combination |
| FN-16 | Maximum supported leg and foot combination |
| FN-17 | Sagekin and Fenn proportional-boundary comparison |

# v1.2 Facial anatomy, ear anatomy, age and individual identity

This is design only, preserving v1.0–v1.1 and all universal rules.

**Classification (race-specific facial-control organization status):** where this spec defines facial regions, editing levels, control groupings, slider organization or other creator-facing control structure (including ear controls), that material is **APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION.** Fenn craniofacial anatomy, population tendencies, valid biological variation, anatomical relationships, ear biology, facial identity, validation, required customization capability and preset and randomization requirements stay approved as established. Only their organization into a final facial-control system is provisional, and the section is kept as input to the Universal Facial Customization Architecture Review after all 13 first-pass races are complete.

**UFCA status (UFCA Phase 2, October 5, 2026):** the universal facial creator organization is now canonical in `decisions/UFCA_V1.md`. The Fenn facial control organization in this spec stays as approved requirements and is routed to its UFCA slots (`reviews/claude-ufca-08-phase1-architecture-audit.md` Appendix A); Fenn anatomy, tendencies, validators, tests and OPEN items are unchanged. Brow structure and brow-to-eye distance are bound as stated in §2–7; the final-closure note below adds the forehead transition and further brow controls. Under UFCA AC-U1, "eye size" in this spec means bony orbit size (direct control) plus visible eye aperture (direct control); eyeball size is derived from the orbit and is never an independent slider.

**UFCA final closure (author decision, October 5, 2026; `reviews/chatgpt-ufca-final-closure-order.md`):** A Fenn-specific forehead-to-cranium transition contour is bound, expressing the smoother forehead-to-cranium relationship in §2–7 inside the Fenn craniofacial envelope, preserving existing broad individual variation where canon supports it. It is not a generic forehead-height/slope package and imports no Marchfolk forehead architecture; forehead height and other forehead dimensions stay hidden unless later canon authorizes them. Additional anatomical brow controls are bound (brow prominence, brow contour/shape, brow vertical position relative to the orbit, medial/lateral brow relationship where needed for coherent regional editing), inside the Fenn craniofacial envelope. These are brow/orbital anatomy, not eyebrow grooming, and they preserve the Fenn compact face and approved visible-eye/orbital relationships, with no Marchfolk default range and no permanent surprised, delicate, severe, youthful, feminine, masculine or other personality or presentation read. Eyebrow-hair biology is bound in UFCA slot 11 (ordinary variation in density/fullness, distribution/coverage, strand/coarseness character where ordinary hair biology supports it, and natural colour relationship to the individual's hair/pigmentation). Grooming, trimming, shaping, cosmetics, dye, styling and deliberate removal stay Personal Presentation. Eyebrows encode no culture, personality, class, attractiveness or sex stereotype, and no race-specific eyebrow morphology is implied; no numeric ranges are set.

## 1. Facial identity principle

Fenn faces never depend only on pointed ears. With the ears hidden, subtle elven craniofacial traits remain. There's no single canonical "beautiful elf face", and identity comes from many relationships together.

## 2–7. Facial regions

| Region | Fenn tendency (population, not mandatory) | Supported variation |
| --- | --- | --- |
| Cranium | Slightly greater cranial height relative to face, somewhat narrower skull, slightly less lower-face mass, smoother forehead-to-cranium line | Broad individual variation |
| Eyes and orbits | Slightly larger orbits, slightly more eye prominence, wide eye-angle range, distinct brow and orbit relationships | Size, spacing, depth, angle, opening, lids, brow-to-eye distance, brow structure. Never anime-like oversized eyes as the marker |
| Cheeks and mid-face | Somewhat higher cheekbones, slightly lighter mid-face | Broad or narrow, high or low within Fenn limits, strong or subtle projection, full or hollow, soft or angular |
| Nose | No mandatory small or straight nose | Length, width, bridge height and width, profile curve, projection, tip structure and rotation, nostril width, alar structure |
| Jaw and chin | Somewhat lighter jaw than humans on average | Narrow, broad, angular, rounded, strong or subtle jaws, and all chin sizes and projections. Broad or muscular Fenn stay valid |
| Mouth and lips | No mandatory mouth shape | Width, lip fullness and projection, Cupid's bow, philtrum, corners, natural asymmetry |

Body composition and age can influence facial soft tissue without replacing skeletal identity.

## 8. External ear morphology

Fenn ears are their own external-ear anatomy, not human ears with stretched tips. **Population tendency (Elf Comparative Review, final clarification §3; Pass 2 AC-5):** Fenn have the greatest average lateral (outward) ear projection of Fenn, Aelari and Vael, with individual overlap and the Fenn ear bounds (§9) preserved. Future work keeps coherent structures analogous to the helix, antihelix, concha, tragus region, lobe, upper-ear extension and tip. The point emerges naturally from the whole ear.

## 9. Ear customization

The controls are overall length, base width, tip length and sharpness, vertical angle, forward and backward sweep, projection from the skull, upper-ear curvature, lobe size and lobe attachment. Everything stays within coherent Fenn ranges, with no single mandatory oversized silhouette.

## 10. Ear asymmetry

Subtle natural asymmetry covers height, angle, projection and minor shape. Defaults are conservative, and Restore Symmetry applies.

## 11. Acquired ear damage

Notches, healed tears, missing tip portions, ear scars and piercing damage belong to scars and acquired appearance, never to racial anatomy.

## 12. Aging

Fenn visibly age. Age can affect facial volume, skin elasticity, the eye area, cheeks, jawline, neck tissue, wrinkles, hair density and color, ear tissue (subtly), and body composition and posture. Lifespan and aging rate aren't set yet and are logged for lore review.

## 13. Appearance diversity (universal)

No playable race is biologically required to be conventionally attractive. Fenn can be attractive, plain, weathered, soft-featured, severe, scarred, elderly, heavy, asymmetrical, broad-faced, narrow-faced or otherwise distinctive. There's no fantasy-figurine uniformity.

## 14. Facial animation validation

Faces are tested in neutral, speech, smile, anger, fear, surprise, sadness, blink and eye movement, with particular attention to eyelids and orbits. Individual and racial anatomy is kept through expression.

## 15. Ear movement (open)

Whether Fenn ears move voluntarily or involuntarily, and what anatomy or animation would support it, is decided later. Nothing is implemented now.

## 16. Hidden-ear facial test

Marchfolk, Sagekin and Fenn are compared at equal age and composition with Fenn ears hidden. The test checks whether Fenn identity survives through the cranium, orbits, cheeks, mid-face, jaw and so on, without requiring every individual to be identifiable.

## 17. Expanded validation characters

FN-01 to FN-17 stay, and these are added:

| ID | Configuration |
| --- | --- |
| FN-18 | Soft-featured |
| FN-19 | Broad-faced |
| FN-20 | Strong-jawed |
| FN-21 | Large, broad nose |
| FN-22 | High-body-fat facial validation |
| FN-23 | Elder |
| FN-24 | Maximum supported ear length |
| FN-25 | Minimum, subtle ear length |
| FN-26 | Ear asymmetry test |
| FN-27 | Hidden-ear facial comparison |

# v1.3 Skin, hair, forest adaptation and cultural presentation

This is design only, preserving v1.0–v1.2 and all universal rules.

## 1. Elven population principle (proposed, for the elven races)

Shared elven ancestry doesn't mean one elven complexion. Fenn, Aelari and Vael each get their own pigmentation, complexion and hair distributions. Fenn aren't the default elf template just because they're designed first. Individuals may overlap, and racial identity never rests on one skin value.

## 2. Fenn natural pigmentation

The broad range runs across fair and light, warm beige, golden and tan, olive, copper, bronze, light to deep brown, and rich darker brown, with broad warm and neutral undertones and some cooler ones. There's no naturally green skin as a default Fenn trait. Frequencies are unresolved.

## 3. Other elven populations

Aelari pigmentation isn't finalized here, and Vael aren't constrained by Fenn. The existing Vael direction stays: charcoal, gray, violet, blue-gray, desaturated brown and related tones. Aelari and Vael each get their own full complexion pass.

## 4. Comparative elf review (future checkpoint)

Once Fenn, Aelari and Vael each have a first-pass design, review all three together before finalizing frequencies for skin, undertones, hair color and texture, and eye color. Valid ranges can be set earlier, and the relative frequencies are tuned side by side.

## 5. Skin layers

The universal four layers stay: natural (pigmentation, undertone, complexion, freckles, moles, birthmarks), environmental (sun and tanning, weathering, roughness, dryness, calluses, localized wear, dirt), applied (tattoos, body paint, makeup, ceremonial markings) and acquired (scars). Natural pigmentation and tanning stay separate.

## 6. Regional environmental appearance

The face, hands, forearms, feet and general exposed skin keep regional controls where feasible. Fenn aren't automatically weathered for living in or coming from forests. Individual history decides.

## 7. Hair biology

Texture covers straight, wavy, curly, and tightly curled or coiled. Natural colors may include black, dark brown, brown, lighter brown, auburn, red, and blond or light shades where valid. Frequencies wait for the comparative elf review.

## 8. Hair presentation

Long hair, braids, and leaves, flowers, feathers, twigs or other forest decoration are never biologically required. Fenn can wear short, long, shaved, practical, elaborate or foreign styles, or go bald or closely shaved where appropriate. A Fenn without Fenn-style hair still looks Fenn.

## 9. Forest adaptation

There are no extra biological adaptations just because Fenn are wood elves, and no gimmicks to explain forest competence. **Unresolved:** whether Fenn have moderately better low-light vision than humans. Space stays open for Vael to have much stronger subterranean low-light adaptation.

## 10. Cultural foundation (provisional)

| Concept | Covers |
| --- | --- |
| Canopy | Vertical settlement, travel, observation, forest life |
| Path | Navigation, communication, exploration, hunting, movement |
| Stewardship | Long-term management and understanding of forest resources and ecology |
| Craft | Sophisticated use of local and traded materials |
| Memory | History, ancestry, mapping, oral and written tradition, songs and stories, meaningful places |

Fenn civilization is never portrayed as primitive for being forest-based.

## 11. Settlements and architecture (direction only)

Sophisticated multi-level settlements combine forest floor, trunks, platforms, canopy, bridges, suspended paths, stairs, ramps, lifts, rope systems and integrated structures. They reflect generations of engineering and stay practical for children, elders, the injured, cargo, merchants, visitors and other playable races. Nothing is final during character design.

## 12. Clothing and materials

Clothing responds to climate, rain and humidity, vegetation, mobility, occupation, wealth, region, ceremony, warfare and taste. Materials can include textiles, plant fibers, leather, fur where culturally and ecologically fitting, wood, worked metal, bone and horn, stone, beads and imports. There's no universal primitive or "leaf" clothing.

## 13. Cultural visual language

The recurring motifs are branching forms, interwoven lines, concentric growth forms, vertical patterns, flowing asymmetry, and selective plant and animal imagery. They can appear across textiles, jewelry, architecture, weapons, armor, tattoos, paint and decorative objects, with no excessive literal leaf motifs.

## 14. Tattoos, paint and markings

Possible meanings are family and lineage, settlement, life events, spiritual and hunting traditions, military service, memorials, craft affiliation and personal decoration. They're cultural and acquired, never required for Fenn ancestry.

## 15. Cross-cultural validation

| Ancestry | Presentation |
| --- | --- |
| Fenn | Neutral |
| Fenn | Fenn |
| Fenn | Marchfolk |
| Fenn | Sagekin |
| Marchfolk | Fenn |

Culture never changes biology. A Marchfolk raised among Fenn stays anatomically Marchfolk, and a Fenn raised abroad stays Fenn.

# v1.4 Presets, population-aware randomization and racial validation

This is design only, preserving v1.0–v1.3 and all universal rules. It arrived in three parts (§1–5, §6–10, §11–16), kept together here as one complete specification.

## 1. Character presets (provisional)

1. Canopy Pathfinder.
2. Forest Artisan.
3. Broad Warden.
4. River Traveler.
5. Heavyset Trader.
6. Elder Storykeeper.
7. Foreign-Raised Fenn.
8. Young Wanderer.

These are visual starting characters only. They never assign class, stats, personality, permanent occupation, background or abilities, and all are reproducible and fully editable.

## 2. Presentation presets (provisional)

The presentation presets are Canopy Practical, Forest Formal, Trail-Worn, Ceremonial, Artisan and Foreign/Urban. They never overwrite race, skeleton, face, ears, height, composition or natural pigmentation.

## 3. Population-aware generation (conceptual sequence, not a pipeline)

Fenn biological foundation → skeletal and frame variation → body proportions → physical composition → facial anatomy → ear anatomy → pigmentation and hair → individual details → cultural and personal presentation.

## 4. Relationship-aware randomization

Sliders are never randomized independently. Randomized Fenn keep limb-to-torso, upper and lower limb, joint-scale, hand and wrist, foot and ankle, shoulder and ribcage, pelvis and leg, craniofacial, and ear-to-skull relationships. The combined-proportion validity principle applies.

## 5. Ear independence

Randomization never produces a human body plus a human face plus pointed ears. Minimum-ear Fenn keep Fenn anatomy, and maximum-ear Fenn stay coherent, not caricatured.

## 6. Composition stress testing

The tests cover Narrow and lean, Narrow and muscular, Balanced and high fat, Broad and lean, Broad and muscular, Broad and high fat, Elder and muscular, and Elder and high fat. The Fenn skeleton survives every supported composition.

## 7. Hidden-ear population test

Generate 100 Marchfolk, 100 Sagekin and 100 Fenn with presentation neutralized and Fenn ears hidden, then judge population-level differences. Perfect individual classification isn't required and some ambiguity is fine, but the Fenn population must never collapse into ordinary human anatomy.

## 8. Silhouette validation

At medium distance, or with facial detail neutralized, Fenn read through limb length, forearm and lower-leg proportions, torso share, ribcage, shoulders, joint scale, hands and feet combined. Broad and highly muscular Fenn get special attention and must never become muscular human silhouettes.

## 9. Facial population validation

Compare randomized Marchfolk, Sagekin and Fenn portraits with ears hidden and hair neutralized where practical. Fenn identity comes from cranial, orbital, cheek, mid-face, jaw and other relationships together, never from one mandatory eye, nose, jaw, cheekbone or "elf face".

## 10. Subtle-ear validation

A permanent minimum-ear test checks that the character stays Fenn through the rest of the anatomy. A maximum-ear test checks that the ears stay coherent.

## 11. Cross-cultural randomization

| Ancestry | Presentation |
| --- | --- |
| Fenn | Fenn |
| Fenn | Marchfolk |
| Fenn | Sagekin |
| Marchfolk | Fenn |

This extends to Aelari and Vael once their cultures are designed.

## 12. Biology versus presentation randomization (proposed universal)

| Type | Draws on |
| --- | --- |
| Biological randomization | Race or ancestry, and population distributions |
| Presentation randomization | Culture, background, region, personal style and other presentation data |

Choosing Fenn ancestry never permanently forces Fenn cultural presentation.

## 13. Elf comparative review

Exact Fenn frequencies for skin, undertones, hair color and texture, eye color and overlapping facial traits aren't finalized here. They wait for the dedicated review once Fenn, Aelari and Vael all have first-pass designs. Shared ancestry stays plausible, and each population keeps its own biological history.

## 14. Expanded validation set

FN-01 to FN-27 stay, and these are added:

| ID | Configuration |
| --- | --- |
| FN-28 | Broad and high-muscle silhouette |
| FN-29 | Broad and high-body-fat silhouette |
| FN-30 | Elder and muscular |
| FN-31 | Elder and high body fat |
| FN-32 | Minimum-ear full-body test |
| FN-33 | Maximum-ear full-body test |
| FN-34 | Neutral-presentation randomized Fenn |
| FN-35 | Marchfolk-culture Fenn |
| FN-36 | Sagekin-culture Fenn |
| FN-37 | Hidden-ear randomized boundary case |
| FN-38 | Valid extreme randomization |

## 15. Failure conditions

Generation fails if it consistently produces:

- [ ] Human bodies with pointed ears.
- [ ] One repeated elf face.
- [ ] Mandatory thin physiques.
- [ ] Mandatory youthful appearances.
- [ ] Mandatory conventional attractiveness.
- [ ] Identical noses or eye shapes.
- [ ] Excessively similar pigmentation.
- [ ] Mandatory long hair or braids.
- [ ] Mandatory forest decoration.
- [ ] Implausible extreme proportion combinations.
- [ ] Broad or muscular Fenn that lose their elven skeleton.

## 16. Status

Fenn v1.4 is complete.

# v1.5 Final validation and technical handoff

This is design and technical planning only, with no UE5 implementation. It arrived in three parts, kept together here: skeleton, animation and movement (§1–8); equipment, cameras, world and mounts (§10–18); and architecture, final validation and completion (§20–27). Fenn v1.0–v1.5 are **first-pass complete**, making Fenn the fourth finished race after Marchfolk, Skarn and Sagekin.

## 1. Skeleton architecture

Fenn are the first race that explicitly needs a genuinely non-human skeleton. None of these is assumed: that a scaled human skeleton is enough, that human bones can simply be stretched, that human animation stays correct, or that MetaHuman or another human-oriented system is the final answer. Later investigation compares shared skeletons, modified shared hierarchies, race-specific skeletons, retargeting, procedural adjustment, IK and hybrids. None is chosen yet.

## 2. Anatomical landmarks

Shoulders, elbows, wrists, hands, spine, pelvis, hips, knees, ankles, feet, neck and head keep coherent placement and articulation across the full valid range.

## 3. Animation validation

The tests cover idle, walk, jog and run, sprint if supported, acceleration, deceleration, turning, strafing, crouching, jumping, landing, stairs, slopes, foot placement and combat locomotion. Scaled human animation isn't assumed to work.

## 4. Movement identity

Movement may reflect longer limbs, different torso proportions and center of mass, a lighter skeleton, different joints and individual composition. There's no exaggerated "graceful elf" animation just because they're elves. Movement comes from anatomy, physical state, equipment, training and gameplay needs.

## 5. IK and environmental contact

The tests cover feet on uneven ground, hands on surfaces, doors, levers, containers, tables and counters, ladders, climbing surfaces, sitting, sleeping, object pickup and contextual interactions. Human interaction offsets aren't assumed to fit the whole Fenn range.

## 6. Hands and weapon grips

The tests cover one- and two-handed weapons, bows, shields, tools, staves and pole weapons, small objects and environment grips. Canonical weapon dimensions never scale with hand size, and grip adaptation is investigated separately.

## 7. Climbing

If climbing exists, it matters especially for Fenn. Reach, hand and foot placement, body clearance, mantling and ledge transitions get validated. Cosmetic proportions never give climbing advantages without a dedicated gameplay review.

## 8. Swimming

The faster-swimmer concept stays. Swimming animation must work across Fenn heights, limb proportions, frames, muscle, fat and age. The gameplay values are unresolved, with no implementation or rebalance now.

## 10. Clothing and armor

Shirts and tunics, coats, robes, chest and shoulder armor, belts, gloves, pants, leg armor, boots and full outfits must fit every valid Fenn height, frame, limb proportion, muscle, fat and age, without unacceptable clipping, floating, deformation or stretching.

## 11. Helmets, hoods and ears

Fenn ears are a dedicated equipment problem. Options to investigate include ear openings, gear shaped around the ears, roomy ear-covering designs, race-specific variants where justified, and other solutions. What's never done automatically: ears clipping through helmets, ears hidden or deleted for every helmet, ears flattened unnaturally, or all headgear made Fenn-only. The architecture is unresolved.

## 12. Hair and headgear

Hair, ears, helmets, hoods, hats, circlets and accessories are validated together, respecting Fenn skull and ear anatomy.

## 13. Footwear

Boots, shoes, sandals where appropriate, armor and barefoot setups are checked against the longer, narrower Fenn feet. Human footwear deformation isn't assumed to hold up.

## 14. Cameras

The third-person, creator, dialogue, cinematic, interaction and first-person (if supported) cameras are validated. There's no single camera height for every race and body.

## 15. First-person arms

If visible first-person arms exist, Fenn keep their own arm, forearm and hand proportions, skin and equipment. They're never silently swapped for generic human arms. The architecture is unresolved.

## 16. World compatibility

The playable-race world-compatibility rule applies: doors, ceilings, stairs, ladders, chairs, benches, beds, tables, counters, tunnels, interaction points and climbing spaces. Fenn environments stay usable by visiting races unless a restriction is deliberate.

## 17. Mounts (unresolved)

Fenn height, pelvis, leg length, foot position, proportions, equipment and mount size or type all matter. Human riding poses aren't assumed to work.

## 18. Collision and reach (unresolved)

The capsule, height, width, melee reach, interaction reach, step height and climbing reach are still to decide. Cosmetic differences never automatically become gameplay effects.

## 20. Unified character data

Fenn use the same conceptual record as every race: ancestry, skeleton and body, composition, face, age and identity, skin, hair, markings and presentation. That doesn't require the same skeleton, mesh, morph system or deformation as human races.

## 21. Shared concepts, race-specific biology

| Shared across races | Owned by each race |
| --- | --- |
| Height, frame, muscle, fat, face customization, age, skin, hair, markings, presentation, presets, randomization | Biological foundation, ranges, anatomical relationships, skeleton needs, morph and deformation needs, animation needs, equipment-fitting needs |

The goal is neither 13 unrelated creators nor one generic humanoid body for every race.

## 22. Deterministic generation

The proposed reproducibility rule applies: randomly generated Fenn can be recreated from stored data or seeds, for NPC persistence, save and load, testing, bug reproduction, presets and networking.

## 23. Final Fenn validation gate

Before any implementation approval, Fenn must pass:

- [ ] Hidden-ear body test
- [ ] Hidden-ear facial test
- [ ] Minimum-ear test
- [ ] Maximum-ear test
- [ ] Narrow-frame test
- [ ] Broad-frame test
- [ ] High-muscle test
- [ ] High-body-fat test
- [ ] Elder test
- [ ] Extreme-valid-proportion test
- [ ] Animation test
- [ ] Facial-expression test
- [ ] IK and contact test
- [ ] Weapon-grip test
- [ ] Equipment-fit test
- [ ] Headgear and ear test
- [ ] World-compatibility test
- [ ] Cross-cultural presentation test
- [ ] Save and load reproduction test
- [ ] Population-randomization test

## 24. Cross-race validation

Fenn are compared against Marchfolk, Sagekin and Skarn now, and Aelari and Vael later. The Sagekin and Fenn boundary is protected: Sagekin are fully human long-limbed variation, and Fenn have a genuinely elven skeleton and face.

## 25. Elf comparative review

Once Fenn, Aelari and Vael finish first pass, a dedicated review compares shared elven ancestry, race-specific skeletal differences, craniofacial distributions, ear morphology, skin, undertones, hair color and texture, eye color, age appearance and population overlap, before frequencies are final. Fenn are never the default elf.
