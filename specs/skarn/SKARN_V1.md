# Skarn Character Customization v1.5 (first-pass complete)

This is the Skarn specification at v1.5, first-pass complete: v1.0 covers racial anatomy and the physical foundation, v1.1 covers body proportions, mass and anatomical relationships, v1.2 covers facial anatomy, age and individuality, v1.3 covers skin, hair, scars, weathering and cultural presentation, v1.4 covers presets, randomization and racial validation, and v1.5 covers final validation and technical handoff. It is design only, built on universal amendment v0.1 (four independent layers), with nothing implemented in UE5. The next race was Sagekin, and scholarly culture must never be confused with biological frailty or a universally thin body.

## 1. Racial identity

Skarn are biologically human: a naturally larger, heavier, more powerfully built population than Marchfolk. They are not scaled-up Marchfolk and not automatically muscular. Their identity comes from underlying anatomy, so a lean, elderly, narrow-framed or high-body-fat Skarn still reads as Skarn.

## 2. Height (provisional)

| Minimum | Reference | Maximum |
| --- | --- | --- |
| 183 cm (6'0") | 208 cm (about 6'10") | 229 cm (7'6") |

The overlap with tall Marchfolk (up to 203 cm) is intentional: a short Skarn must still be anatomically distinct from a Marchfolk of the same height. Biological anatomy sets no separate height limits. These values await visual and technical validation.

## 3. Skeletal foundation

Compared with Marchfolk, Skarn ranges trend toward:

- broader clavicles
- a deeper ribcage and more thoracic volume
- a more substantial neck base and pelvis
- heavier joints
- larger hands and feet
- greater skeletal robustness and a higher Muscular Development Capacity (biological range; Current Muscularity stays free, §5)

These are ranges, not identical proportions for every Skarn.

## 4. Skeletal frames

The universal frames apply: Narrow, Balanced and Broad, all inside Skarn limits. A Narrow Skarn is still structurally Skarn. A Broad Skarn can be extremely substantial but stays visibly distinct from Gorrund.

## 5. Physical composition

Composition is independent of frame: low or high muscle, low or high fat, regional development and different conditioning levels. Muscle modifies Skarn anatomy rather than creating racial identity. Exaggerated bodybuilder anatomy is not the default.

## 6. Anatomical scaling

Height is never a uniform whole-body scale. Height changes keep believable relationships between the head, torso, pelvis, arms, legs, hands, feet and joint positions. Hands, feet, joints and torso carry much of the Skarn sense of scale.

## 7. Movement direction

Movement shows greater mass, powerful weight transfer, strong strides, fitting momentum, convincing acceleration and deceleration, and grounded landings. Size is not clumsiness, and there are no gameplay movement penalties yet.

## 8. Face

Skarn faces are fully human and diverse. There are no mandatory square jaws, heavy brows or facial hair, and facial hair belongs to personal presentation. Detailed craniofacial ranges come in a later spec.

## 9. Racial trait

Skarn hold their breath about 1.5× as long as the baseline (read as the Marchfolk Human Reference Population). This is kept as is, with no rebalance yet.

## 10. Validation comparisons (later)

These side-by-side pairs confirm that racial identity survives independently of height and muscle:

| Marchfolk | Skarn |
| --- | --- |
| Narrow | Narrow |
| Balanced | Balanced |
| Broad | Broad |
| Maximum height (203 cm) | Minimum height (183 cm) |
| Low muscle | Low muscle |
| High muscle | High muscle |

# v1.1 Body proportions, mass and anatomical relationships

This is design only. It adds to v1.0 and universal amendment v0.1 without replacing either.

## 1. Core proportional identity

Skarn are never uniformly scaled Marchfolk. Relative to Marchfolk, the Skarn central tendency trends toward:

- a slightly larger torso share of total height and greater torso depth
- broader clavicles, a wider and deeper ribcage, and a broader upper back
- a thicker neck base and a more substantial pelvis
- more substantial limbs and larger joints
- larger hands and feet
- a higher Muscular Development Capacity (not a default Current Muscularity)

Individual variation stays essential.

## 2. Torso and leg relationships

Torso, leg and arm length, shoulder width, chest width and depth, and hip and pelvis width all vary. The Skarn central tendency is slightly more torso-dominant than Marchfolk, but Skarn aren't universally short-legged. Long-legged and long-torso Skarn are both possible.

## 3. Upper body

Shoulders, clavicles, chest, upper back and neck act as one connected system, with no simple mesh stretching. Wider shoulders keep believable shoulder-joint placement. Deeper chests change ribcage volume, not just surface muscle.

## 4. Lower body

The pelvis, hips, thighs, knees, calves, ankles and feet plausibly carry the greater mass at every setting. There is no default "huge upper body, tiny legs" silhouette.

## 5. Hands and feet (detailed controls)

Detailed controls to explore: hand size and breadth, finger proportions, foot length and breadth. All stay anatomically constrained, and they matter for both racial identity and equipment.

## 6. Regional muscle development

Overall muscularity stays. Advanced regional emphasis covers neck and traps, shoulders, arms, forearms, chest, back, core, glutes, thighs and calves. Regional values stay tied to overall muscularity so no single group becomes implausible. They are cosmetic unless gameplay effects are designed later.

## 7. Physical mass (proposed universal principle)

Body weight is not a primary slider. Mass comes from height, frame, muscularity, body fat and regional proportions. The game may show an estimated weight derived from the anatomy, never used to generate it.

## 8. Anatomical interdependencies

Controls are linked subtly rather than disconnected:

- Shoulder width moves the upper back and clavicles.
- Chest depth changes ribcage volume.
- Pelvis width sets upper-leg alignment.
- Hand size keeps the wrist transition.
- Foot size keeps the ankle and lower-leg relationship.
- Limb thickness keeps joint transitions.
- Torso and leg length keep overall proportions coherent.

These protect plausibility without taking away meaningful control.

## 9. Validation characters (later)

Each is compared against an equivalent Marchfolk:

1. **Short Skarn:** 183 cm, Narrow, low muscle.
2. **Ranging Skarn:** tall, Narrow, long-legged, lean.
3. **Heavy Skarn:** Balanced, substantial body fat, moderate muscle.
4. **Laborer:** developed forearms, back and legs, without bodybuilder proportions.
5. **Broad Skarn:** Broad frame, low to moderate muscle.
6. **Powerhouse:** Broad with very high muscle.
7. **Elder Skarn:** age changes composition while racial anatomy stays.
8. **Maximum Skarn:** 229 cm at the supported extremes.

## 10. Design goal

No single factor of height, muscularity or body fat decides whether a character reads as Skarn. The underlying anatomy stays recognizable across the whole range.

# v1.2 Facial anatomy, age and individuality

This is design only, preserving v1.0–v1.1 and the universal rules.

## 1. Facial principle

Skarn faces are biologically human. Their identity comes from population ranges and combinations, not mandatory features. The Skarn facial central tendency trends toward:

- a slightly larger, more robust skull suited to body size
- a somewhat stronger brow
- more jaw mass
- a more substantial mid-face and cheeks
- a somewhat larger nose
- a more substantial neck-to-jaw transition

These are tendencies, not requirements. Skarn are not all square-jawed, heavy-browed, bearded or angry-looking.

## 2. Facial editor

The editor uses the same seven regions as Marchfolk: head and skull, brow and eyes, nose, cheeks, jaw and chin, mouth and lips, and ears. Race changes the supported ranges, not how the editor works.

**Ears (Pass 2 AC-4):** Skarn follow the Marchfolk human-family auricular anatomical foundation (Marchfolk Part 2 §3–4) unless this spec explicitly modifies a tendency. This does not make Skarn head anatomy Marchfolk-equivalent.

**Interpretation (Durrim consistency-resolution patch):** "the same seven regions as Marchfolk" means Skarn must support at least the facial anatomical coverage represented by the Marchfolk first-pass regions, subject to later reorganization in the Universal Facial Customization Architecture Review. The final creator needn't keep seven regions, their names, nesting, UI layout or control grouping. Skarn biological requirements stay approved, and only the final control organization is deferred (APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION).

**UFCA status (UFCA Phase 2, October 5, 2026):** the universal facial creator organization is now canonical in `decisions/UFCA_V1.md`. The Skarn facial control organization in this spec stays as approved requirements and is routed to its UFCA slots (`reviews/claude-ufca-08-phase1-architecture-audit.md` Appendix A); Skarn anatomy, tendencies, validators, tests and OPEN items are unchanged. Mouth and lips are bound through normal human-family coverage (UFCA AD-U12; a coverage clarification, not new Skarn anatomy). Ears use the human-auricle family (Pass 2 AC-4). Under UFCA AC-U1, "eye size" in this spec means bony orbit size (direct control) plus visible eye aperture (direct control); eyeball size is derived from the orbit and is never an independent slider.

**UFCA final closure (author decision, October 5, 2026; `reviews/chatgpt-ufca-final-closure-order.md`):** Eyebrow-hair biology is bound in UFCA slot 11 (ordinary variation in density/fullness, distribution/coverage, strand/coarseness character where ordinary hair biology supports it, and natural colour relationship to the individual's hair/pigmentation). Grooming, trimming, shaping, cosmetics, dye, styling and deliberate removal stay Personal Presentation. Eyebrows encode no culture, personality, class, attractiveness or sex stereotype, and no race-specific eyebrow morphology is implied; no numeric ranges are set.

## 3–6. Region controls

| Region | Controls to explore | Skarn tendency |
| --- | --- | --- |
| Head and skull | Head width, depth and length, cranial height, forehead height and slope, temple width, face length | Believable from front, profile and three-quarter views |
| Brow and eyes | Brow prominence, shape and height; eye depth, spacing, size and angle; upper and lower lid shape; lid opening | Somewhat stronger brow on average, never mandatory |
| Nose and mid-face | Bridge height and width, length, projection, tip width and rotation, nostril width and shape | Somewhat larger on average, not a requirement |
| Cheeks, jaw and chin | Cheekbone width, height and projection; fullness; jaw width, angle and depth; chin width, height and projection | Soft, angular, narrow, broad, youthful and weathered faces all allowed |

## 7. Body-to-face relationships (proposed universal principle)

Body composition gently influences facial soft tissue without overriding facial choices. Fat can add facial fullness, muscle can affect neck and jaw tissue, age changes facial volume, and body scale sets head-to-body proportion. Players keep independent facial control. This is pending validation.

## 8. Age

Age keeps both Skarn anatomy and the individual face. It affects facial volume, skin elasticity, under-eyes, cheeks, jawline, wrinkles, neck tissue, and hair density and color. Old age is not frailty: older, muscular, imposing Skarn stay possible.

## 9. Asymmetry

Subtle Advanced asymmetry and Restore Symmetry remain. A proposed universal feature, **Naturalize Face**, would add very small, bounded, plausible asymmetries to a very symmetrical face without changing its identity. It isn't final until tested.

## 10. Expression validation

Extreme faces are tested in neutral, smile, anger, surprise, blink and speech. A face that only looks right in neutral isn't valid.

## 11. Facial hair

Facial hair is presentation, not racial identity. Clean-shaven Skarn are fully recognizable as Skarn.

# v1.3 Skin, hair, scars, weathering and cultural presentation

This is design only, preserving v1.0–v1.2 and all universal rules.

## 1. Identity principle (proposed universal)

Race defines the biological foundation, culture influences presentation, and personal history influences acquired appearance. These aren't conflated. A character reads as their race without culturally stereotyped hair, tattoos, clothing, scars or accessories.

## 2. Skin layers

The four layers stay, as in Marchfolk v1.3 (as conformed).

| Layer | Covers |
| --- | --- |
| Natural | Base pigmentation, undertone, complexion, freckles, moles, birthmarks, natural variation |
| Environmental | Sun exposure, wind and weather, dryness, roughness, calluses, localized wear, dirt |
| Applied | Tattoos, paint, makeup, decorative markings |
| Acquired | Scars |

Skarn have full natural human skin-tone variation. A northern origin never means one mandatory skin color.

## 3. Regional weathering (proposed universal)

Environmental appearance can differ by region: face, hands, forearms, feet and general skin. For example, heavily callused hands don't force an equally weathered face.

## 4. Hair

Skarn have broad hairstyle and texture variation: style, length where supported, texture, hairline, density, color, graying and accessories. Traditional Skarn styles may later be cultural presets, never biological restrictions. Hair isn't locked to anatomy, frame or physique.

## 5. Facial hair

Facial hair is independent presentation: clean-shaven, stubble, or short, full, long or styled and braided beards. Where it applies, it has style, length, density, color and graying controls. Skarn identity never depends on it.

## 6. Scar system (to explore)

This is cosmetic representation, not medical simulation.

| Aspect | Options |
| --- | --- |
| Injury type | Cut, puncture, burn, abrasion, other healed injuries |
| Age | Recent or healing, healed, old or faded |
| Surface | Flat, raised, recessed |
| Placement | Position, rotation, scale, mirroring where it fits |

## 7. Tattoos, paint and markings

Markings may later be grouped into tagged collections: Skarn traditional, regional, religious or spiritual, military, guild, decorative and personal. Choosing a race never applies cultural markings automatically, and markings aren't race-locked unless lore or tech later requires it.

## 8. Presentation presets (proposed universal)

These are separate from anatomical presets. They apply coordinated cosmetics: hair, grooming, markings, accessories and environmental appearance. They never replace face, height, frame, biological anatomy, muscularity or body fat. Possible Skarn examples are Traditional Northern, Traveler, Urban, Veteran and Ceremonial. Pending design review.

## 9. Culture architecture

Culture selection isn't final. The system stays compatible with a future where race, culture, background and class are separate concepts, and it never assumes every member of a race shares one culture.

# v1.4 Presets, randomization and racial validation

This is design only, preserving v1.0–v1.3 and all universal rules.

## 1. Starting presets (provisional)

1. Northern Hunter.
2. Mountain Laborer.
3. Seasoned Traveler.
4. Clan Veteran.
5. Skarn Scholar.
6. Heavyset Merchant.
7. Young Wanderer.
8. Elder Wayfarer.

The names are visual inspiration only. They never set class, stats, background, occupation, personality or abilities. Every preset is built from and fully editable in the normal Skarn customizer.

## 2. Randomization strength (proposed universal)

| Strength | Samples |
| --- | --- |
| Subtle | Close to the racial reference values |
| Diverse | A broad share of validated racial variation |
| Extreme | Near the validated boundaries, still legal. Possibly for development and testing only |

## 3. Selective randomization and locks (proposed universal)

You can randomize the whole character, or only the body, face, hair, skin details, markings or presentation. Individual parameters or groups can be locked, for example height and face locked while hair is randomized.

## 4. Relationship-aware randomization

Sliders are never randomized independently. Results respect the anatomical links: shoulders and ribcage, pelvis and upper-leg alignment, joint transitions, height and proportions, body-to-face soft tissue, and coherent age. Every result is valid with no manual repair.

## 5. Silhouette test (future)

Remove or neutralize hair, facial hair, tattoos, scars, markings, accessories, distinctive clothing and weathering. Then compare Marchfolk and Skarn anatomy in standard neutral presentation. Skarn must still read as Skarn.

## 6. Equal-height test (future)

Compare a 190 cm Marchfolk with a 190 cm Skarn, matched as closely as possible on apparent age, muscle, body fat, pose and presentation. The Skarn must stand out by anatomy, not height, beard, clothing or styling.

## 7. Anti-stereotype validation

All of these must still read as the same population: lean, heavy, elderly, soft-featured, clean-shaven, scholarly-presenting, urban-presenting, scar-free, narrow-frame and extremely muscular Skarn.

## 8. Marchfolk, Skarn and Gorrund separation (cross-race requirement)

The three are never differently scaled versions of one anatomy. Skarn are large, robust humans. Gorrund are giant-kin on their own anatomical foundation. Even extreme Skarn settings must not recreate Gorrund anatomy.

Skarn–Grask separation is carried by the Grask spec (Part 1 §60–70 and Part 5 comparative tests) and the Pass 2 Large-Race Comparative Anatomy Review (`reviews/claude-pass2-r2-large-race-comparative-review.md`). This pointer adds no Skarn anatomy (Pass 2 AD-5).

## 9. Acceptance criteria

Skarn v1.x succeeds when:

- [ ] Racial identity survives removing cultural presentation.
- [ ] Racial identity survives low muscle, high body fat and advanced age.
- [ ] Overlapping Marchfolk and Skarn heights stay anatomically distinct.
- [ ] Extreme customization stays anatomically coherent.
- [ ] Presets use standard customization data.
- [ ] Randomization respects racial biology.
- [ ] Facial expressions work across supported faces.
- [ ] Supported bodies are ready for later animation and equipment validation.

# v1.5 Final validation and technical handoff

This is design and technical planning only, with no UE5 implementation. v1.0–v1.5 form the initial complete Skarn framework, and Skarn visual and customization design is **first-pass complete**.

## 1. Permanent validation set

These become reproducible saved test configurations:

| ID | Configuration |
| --- | --- |
| SK-01 | Reference Skarn |
| SK-02 | Short Skarn, the Marchfolk height-overlap test |
| SK-03 | Maximum height, 229 cm |
| SK-04 | Narrow, lean, long-legged |
| SK-05 | High body fat |
| SK-06 | Regional-development laborer |
| SK-07 | Broad frame, moderate muscle |
| SK-08 | Maximum supported muscle |
| SK-09 | Elder |
| SK-10 | Soft-featured |
| SK-11 | Neutralized cultural presentation |
| SK-12 | A valid extreme-randomization result |

## 2. Animation validation

The test set covers idle, walk, run, acceleration and deceleration, turning, jumping and landing, crouching, stairs, slopes, foot IK, combat, hand-to-object alignment and environment interactions. Uniform mesh scaling is not assumed to work. The mix of shared animation, retargeting, procedural correction, IK and specialized animation is decided later, not now.

## 3. Camera validation

Height affects third-person framing, conversation cameras, cinematics, the creator camera, interaction cameras and first-person eye height, if first-person exists. There's no single universal camera height. First-person is still unresolved.

## 4. Collision, reach and gameplay size (unresolved)

Height- and width-dependent collision, melee and interaction reach, step height, and the gameplay effects of size all stay open in the Decision Register. Cosmetic anatomy never automatically gives gameplay advantages or penalties.

## 5. Equipment validation

Armor, clothing, belts, gloves, boots, helmets, weapons, shields and attachment points are tested across the full body range for clipping, floating, stretching and deformation. Weapon dimensions don't scale with body size. Grip and attachment adaptation is investigated separately.

## 6. World compatibility (proposed universal)

Every playable race is checked against doorways, ceilings, stairs, chairs, benches, beds, ladders, tables, counters, tunnels and interaction points. A supported character must never be accidentally locked out of critical content. Any race-specific restriction is a deliberate design choice.

## 7. Mount compatibility (unresolved)

The character data keeps what a future mount system may need: race and skeleton, height, leg length, pelvis position, relevant proportions and a derived mass category. The mount solution isn't designed yet.

## 8. Cross-race architecture

Marchfolk and Skarn set the universal pattern.

| Shared across races | Defined by each race |
| --- | --- |
| Height, skeletal frame, muscularity, body fat, regional development, facial regions, age, skin, hair, markings, presentation | Biological foundation, defaults, valid ranges, anatomical relationships, presets, randomization rules, validation requirements |

The goal is neither 13 independent creators nor one generic anatomy forced on every race.

## 9. Cross-race validation

Compare equal-height and equal-physique Marchfolk and Skarn, minimum and maximum configurations, neutralized presentation, shared equipment and animation where they apply, and environment interactions. Skarn identity survives through anatomy.

## 10. Universal technical questions (tracked, unresolved)

Open questions: deformation architecture, skeleton strategy, morph targets versus alternatives, animation retargeting, IK and procedural correction, equipment fitting, character-data serialization, LOD and performance, networking, collision and reach, first-person, and mount support. None is resolved without a dedicated review.

**UCCA status (UCCA Phase 2, October 5, 2026):** the universal whole-character creator organization is canonical in `decisions/UCCA_V1.md` (15-slot navigation, control classes, Skeletal Frame and Physical Composition separation, presets, randomization, locks, saved appearance and validation). The Skarn body-control organization in this spec stays as approved requirements routed to UCCA slots (`reviews/claude-ucca-11-phase1-architecture-audit.md` Appendix A); Skarn anatomy, tendencies, bounds, validators, tests and OPEN items are unchanged. Natural subtle body asymmetry is available as ordinary individual variation (UCCA §16); body hair follows UCCA §13.
