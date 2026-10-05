# Marchfolk Character Customization v1.5 (first pass complete)

This is the Marchfolk working specification at v1.5, with the first pass complete: v1.0 covers the biological foundation and body architecture, v1.1 covers body proportions and how body regions affect each other, v1.2 covers facial anatomy and individuality, v1.3 covers skin, hair and personal identity, v1.4 covers age, body frames and presets, and v1.5 covers validation, technical handoff and first-pass completion. It is a design update only, pending further refinement, with nothing implemented in UE5. v1.0 was recovered later and sits first, with v1.1–v1.4 preserved as the approved sections that follow it. v1.5 was also recovered and closes the first pass.

**Universal amendment v0.1 applies to every version here (see the Character Creation & Race Design tab).** The character is set in four independent layers: biological anatomy, skeletal frame, physical composition and personal presentation. Marchfolk skeletal frames are Narrow, Balanced and Broad. Athletic is a physical-composition preset, alongside Lean, Muscular, Heavy and Custom. Anatomy doesn't change the 147–203 cm height range. The v1.1 and v1.4 wording that listed Athletic as a frame has been corrected to match.

# v1.0 Biological foundation and body architecture

This is the recovered opening section that v1.1–v1.4 build on, recorded without replacing them. It's a design specification only, with no UE5 changes, and v1.0 is complete.

## 1–3. Core identity, Human Reference Population role and locked foundation

Marchfolk are the primary broad-spectrum human population and the primary Human Reference Population for the playable races. **They represent the breadth of believable human physical diversity, not one idealized fantasy-human body:** fully human, anatomically grounded, highly variable, with broad body, facial and pigmentation diversity. They aren't biologically defined by heroic proportions, conventional attractiveness, one ethnicity or phenotype, one body composition, culture, occupation or personality. Their adaptability is a population and cultural identity, never an excuse to make them biologically generic.

As the Human Reference Population, Marchfolk are the grounded reference for judging how another race differs in skeletal proportions, craniofacial anatomy, joints, limbs, hands and feet, composition, movement, height and mass. This doesn't make Marchfolk the default anatomy for every humanoid race, and non-human races depart from it wherever their approved biology requires. Marchfolk keep recognizably human skeletal and cranial architecture, shoulders, ribcage, spine, pelvis, limbs, joints, hands, feet, face, skin and hair biology and human locomotor anatomy, with variation inside believable human boundaries.

## 4–5. Height

| Minimum | Reference | Maximum |
| --- | --- | --- |
| About 147 cm (4'10") | About 173 cm (5'8") | About 203 cm (6'8") |

This is the approved first-pass playable envelope. It isn't produced by uniformly scaling the whole character, and height should come from anatomically appropriate proportional relationships. There's no hard sex-specific height restriction from the selected sex-related anatomy or starting frame: population distributions may differ where appropriate, individual overlap stays broad, and a player character can sit anywhere in the supported range.

## 6–8. Frame and physical composition

The skeletal frames are Narrow, Balanced and Broad. Frame describes skeletal structure (shoulder breadth, ribcage dimensions, pelvic breadth, joint scale, skeletal visual mass) and isn't muscularity, body fat, fitness or personality. **Athletic isn't a skeletal frame:** under the universal amendment it belongs to physical composition presets (Lean, Athletic, Muscular, Heavy, Custom), and the layers aren't merged. Muscularity, body-fat amount and distribution, regional muscle and overall physique vary independently of frame, for example Narrow and muscular, Narrow and heavy, Balanced and lean, Balanced and muscular, Broad and lean, or Broad with high body fat.

## 9–11. Regional variation, relationships and mass

The target system supports believable regional variation in shoulders, chest, upper arms, forearms, abdomen, waist, hips, gluteal region, thighs, calves and neck, without parts looking independently stretched, inflated or detached. **Individually valid controls can still create an invalid combined body**, so customization needs relationship-aware constraints or validation across shoulder width and ribcage, ribcage and waist, pelvis and hips, upper arm and forearm, femur and lower leg, hand and wrist, foot and ankle, neck and shoulders, and head and body. Sliders aren't fully independent. Visible mass comes from height, frame, muscle, fat and regional composition together, never one generic scale value, and exact mass calculation is a future problem.

## 12–14. Individuality, layers and culture

Marchfolk support short, tall, narrow, broad, lean, muscular, heavy, soft-bodied, rugged, plain, conventionally and unconventionally attractive, young-adult and older-adult individuals, with no single correct body. The four layers stay distinct, and choosing one never determines another: **biological anatomy** (including relevant sex-related characteristics), **skeletal frame** (Narrow, Balanced, Broad), **physical composition** (muscle, fat distribution, regional development, physique) and **personal presentation** (hair, facial hair, clothing, makeup, scars, tattoos, accessories). The hardy frontier-settler reputation isn't anatomy: ruggedness, manual labor, survival skill, toughness, frontier clothing, weathering, scars and muscularity come from culture, background, occupation, environment or history.

## 15–17. Presets, randomization and gameplay neutrality

Premade Marchfolk are legitimate outputs of the same system as custom characters, with no privileged models. Simple Mode is Race, Preset, Confirm, and Advanced Mode is Race, Preset, Customize, Confirm, where a preset is a starting configuration, not a separate architecture. Randomization supports full and selective randomization, locks, race-aware validity and reproducible results where needed, and never keeps converging on one default fantasy human. Individual cosmetic variation within a race grants no automatic gameplay advantage or penalty: a taller Marchfolk doesn't get more melee reach and a heavier-looking one isn't slower just because of appearance. Race-level biological gameplay differences are a separate OPEN review.

## 18. Technical status

No architecture is chosen. Candidates include MetaHuman, modified MetaHuman, custom meshes, morph targets, bone and proportion adjustment, procedural deformation and hybrids. Design requirements drive the architecture, and technical convenience never redefines approved anatomy.

# v1.1 Body proportions and region relationships

## 1. Two-tier body editing

Quick and detailed body controls (both within Advanced Mode's Customize step) use the same character data, so switching between them keeps the character's appearance.

| Tier | Controls |
| --- | --- |
| Quick controls | Starting body frame, height, overall muscularity, overall body-fat distribution, general physique adjustments |
| Detailed controls | All quick controls, plus individual body regions, detailed anatomical proportions and regional muscle development |

## 2. Starting body frames

There are three skeletal-frame starting categories plus independent physical-composition presets: the frame presets are Narrow, Balanced and Broad, and Athletic is a physical-composition preset (corrected per the consistency resolution). Frame presets are editable starting points, not permanent biological categories.

## 3. Height (preliminary)

| Minimum | Reference height | Maximum |
| --- | --- | --- |
| 147 cm | 173 cm | 203 cm |

## 4. Independent physical composition

Muscularity and body-fat distribution adjust separately, giving a wide range of plausible physiques without a single thin-to-heavy slider.

## 5. Detailed body regions

| Group | Controls |
| --- | --- |
| Upper body | Shoulder width, chest width and depth, neck thickness, arm thickness, hand size |
| Core and pelvis | Waist width, abdomen, torso length, hip width, pelvis proportions |
| Lower body | Leg length, thigh thickness, calf thickness, foot size |
| Physical composition | Overall muscularity, overall body-fat distribution, regional muscle emphasis |

## 6. Anatomical relationships

Each slider makes an anatomically coherent change. Avoid disconnected morph targets, excessive mesh stretching and implausible combinations.

- **Shoulder width:** clavicles, upper back and shoulder-joint position.
- **Chest depth:** ribcage and upper-torso structure.
- **Waist:** smooth transitions through the abdomen and lower torso.
- **Hip width:** pelvis structure and upper-leg alignment.
- **Limb thickness:** believable joint transitions.
- **Torso and leg length:** plausible overall proportions.

## 7. Regional muscle emphasis

This lets builds be physically distinctive: developed shoulders and forearms, a stronger lower body, broad overall conditioning, or a leaner upper body. It starts cosmetic, with no automatic gameplay advantage.

## 8. Design requirement

The target is customization depth similar in philosophy to Dragon's Dogma 2, with our own visual identity, anatomy standards, interface and technical architecture. Every control must eventually be validated against animation, equipment fitting, character proportions and performance.

# v1.2 Facial anatomy and individuality

This is a design update only, pending further refinement. The morph-target architecture is not finalized.

**Classification (Durrim consistency-resolution patch):** the three-level facial editing model and seven-region organization below are **APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION**, meaning approved design proposals that demonstrate required functionality, not the final universal facial-control hierarchy. They stay as requirements and reference, never constrain later races, and will be reconciled in the Universal Facial Customization Architecture Review after all 13 first-pass races are complete.

**UFCA status (UFCA Phase 2, October 5, 2026):** the universal facial creator organization is now canonical in `decisions/UFCA_V1.md`. The Marchfolk facial control organization in this spec stays as approved requirements and is routed to its UFCA slots (`reviews/claude-ufca-08-phase1-architecture-audit.md` Appendix A); Marchfolk anatomy, tendencies, validators, tests and OPEN items are unchanged. The three editing levels map to Starting Face / Quick controls / Detailed controls, and the seven regions to UFCA slots 2–9 with asymmetry in slot 13. Orbit and midface controls are bound, as required by the v1.5 face validation (§2–6). Forehead controls: see the final-closure note below.

**UFCA final closure (author decision, October 5, 2026; `reviews/chatgpt-ufca-final-closure-order.md`):** Ordinary human forehead variation is bound as regional DIR controls in UFCA slot 2 (not global face-shape controls; no numeric bounds): forehead height, forehead slope/contour, forehead-to-brow relationship and forehead-to-cranium transition. They stay inside believable Marchfolk adult human anatomy, with relationship validity keeping the brow, orbit, cranium and hairline region coherent. There is no preferred or ideal forehead, no sex, personality, attractiveness, culture, age or ancestry stereotype, and Marchfolk does not become a template for other populations. Eyebrow-hair biology is bound in UFCA slot 11 (ordinary variation in density/fullness, distribution/coverage, strand/coarseness character where ordinary hair biology supports it, and natural colour relationship to the individual's hair/pigmentation). Grooming, trimming, shaping, cosmetics, dye, styling and deliberate removal stay Personal Presentation. Eyebrows encode no culture, personality, class, attractiveness or sex stereotype, and no race-specific eyebrow morphology is implied; no numeric ranges are set.

## 1. Three levels of facial editing

All three levels use the same character data.

| Level | What it offers |
| --- | --- |
| Face presets | Curated starting faces showing meaningful variation in human facial anatomy |
| Quick controls | Accessible adjustments to the major features |
| Detailed controls | Detailed regional controls, anatomical proportions and optional asymmetry |

## 2. Facial regions

Detailed editing is split into seven regions: head and skull, brow and eyes, nose, cheeks, jaw and chin, mouth and lips, and ears. Edits keep believable relationships between neighboring features and the underlying skull.

## 3. Natural asymmetry (detailed controls)

Subtle independent left and right adjustment covers brow height, eye opening, cheek fullness, mouth corner position, ear projection and jaw contour. Asymmetry stays subtle by default, and a restore-symmetry option is included.

## 4. Age-aware facial anatomy

Age affects facial structure, volume, skin elasticity, wrinkles, under-eye anatomy, cheek fullness, jawline definition, neck structure and hair. Age changes keep the face recognizably the same person.

## 5. Player experience

Planned features:

- before and after comparison
- undo and redo
- several lighting previews
- expression previews
- front, side and three-quarter views
- zoom and free rotation

## 6. Visual direction

Dragon's Dogma 2 is a reference for customization depth and flexibility only, never a source of copied assets or UI. The priorities are realistic human variation, believable anatomy, expressive faces, natural asymmetry and meaningful individuality.

## 7. Technical compatibility

The face system must eventually work with facial animation, speech and expressions, age morphs, skin materials, presets, appearance saving, equipment and headwear, and UE5 performance limits.

# v1.3 Skin, hair and personal identity

This is a design update only, pending further refinement.

## 1. Skin layers

The four layers stay independently editable.

| Layer | Covers |
| --- | --- |
| Natural | Base pigmentation, undertone, complexion, freckles, moles, birthmarks, natural pigmentation variation |
| Environmental | Sun exposure, tanning, weathering, dryness, roughness, calluses, minor discoloration, dirt |
| Applied | Tattoos, makeup, paint, decorative markings |
| Acquired | Scars |

## 2. Hair

Planned controls:

- hairstyle
- style-dependent length
- texture
- color
- hairline
- density
- parting, where the style supports it
- accessories

Body frame doesn't needlessly restrict which hairstyles are available.

## 3. Facial hair

Facial hair has its own style, length, density and color controls. Its color is linked to hair color by default, with an option to unlink them.

## 4. Marking placement (future)

This is a layered system for multiple scars, tattoos and markings. Each marking has position, scale, rotation, color where it fits, opacity, mirroring, layer order and independent removal. Scars get different healed appearances. Placement respects anatomical regions and avoids heavy texture distortion.

## 5. History through appearance

Occupation and personal history can show through weathering, scars, calluses and grooming. These stay player-controlled cosmetic options, never forced by class or occupation.

## 6. Technical compatibility

The system must eventually handle skin-material layering, hair and headwear compatibility, markings that persist, appearance save and load, presets, LOD and performance, body-morph compatibility, and multiplayer sync.

# v1.4 Age, body frames and presets

This is a design update only, pending further refinement.

## 1. Body frames (refines v1.1 §2)

There are three skeletal-frame starting categories plus independent physical-composition presets (corrected per the consistency resolution).

- **Narrow, Balanced and Broad** are different starting anatomical proportions.
- **Athletic** is a physical-composition preset: a curated combination of physical-composition relationships (not skeletal proportions) and muscularity values, not a skeletal-frame category.

Every frame stays fully editable. A frame never restricts customization beyond the race's normal biological limits.

## 2. Age

The initial creator covers adults only. Age is a continuous adjustment, not only fixed categories. The visual reference points are young adult, mature adult, middle-aged, older adult and elder.

Age affects facial volume, skin elasticity, hair color and density, body composition, posture and similar traits, while keeping the character recognizable. A character's actual age and apparent age are separate ideas where that matters. Cosmetic age carries no automatic gameplay penalties.

## 3. Presets

Every preset is a saved configuration of the same system players use. There are no hidden models and no preset-only features. The initial Marchfolk themes are starting concepts, not classes, occupations or required histories:

1. Frontier Settler.
2. Traveling Scholar.
3. Veteran Soldier.
4. Rural Laborer.
5. Merchant.
6. Elder Wanderer.

## 4. Creation flow

Simple mode is Race → Preset → Confirm. Advanced mode is Race → Preset → Customize → Confirm. Both use identical character data.

## 5. Preset requirements

Presets vary in height, frame, muscularity, fat distribution, age, face, skin, hair, markings and silhouette. Every preset can be fully reproduced in the standard customizer.

## 6. Principle

Body frame, apparent age, occupation-themed presets and class stay uncoupled, so players can make unconventional but believable people.

# v1.5 Validation, technical handoff and first-pass completion

This is the recovered closing section of the v1.0–v1.5 sequence. It's design and technical handoff only, with no UE5 changes.

## 1. Validation philosophy

Marchfolk are validated as a complete anatomical system, not slider by slider, in three stages: **A, anatomy** (believable construction across the envelope), **B, facial and individual identity** (broad diversity without one preferred face), and **C, gameplay and world compatibility** (supported anatomy works in the world without prototype limits redefining the design).

## 2–6. Body, face and identity validation

| Test | Requirement |
| --- | --- |
| Permanent height characters | About 147, 173 and 203 cm, each tested with several frame and composition combinations, never only the reference height |
| Frame | Narrow, Balanced and Broad, each with very different compositions (lean, muscular, high body fat), to verify frame and composition stay independent |
| Proportion stress | Minimum and maximum limb relationships, torso, shoulders, pelvis and hips, neck, hand and foot scale and proportion, regional development. Combined extremes are tested, and combinations that are invalid overall are rejected even when each parameter is valid alone |
| Face | Cranial relationships, face width and length, brow, orbits and eyes, cheeks, midface, nose, mouth and lips, jaw, chin, ears and natural asymmetry, not optimized only for conventionally attractive faces |
| Identity stress | Clearly different people who are still biologically human. It fails if generation keeps producing one face with minor tweaks, one attractive template, one body type, one age, one pigmentation family or one hair type |

## 7–8. Age and skin, hair and marking validation

Adult aging must do more than wrinkles and gray hair, and may affect facial volume, skin elasticity, eye region, jawline, neck, hair density and pigmentation, and body composition where appropriate, with exact implementation later. Broad combinations of natural pigmentation, undertones, hair color and texture, facial hair, freckles, moles, birthmarks, scars, tattoos, makeup and weathering are tested, keeping the Natural, Environmental, Applied and Acquired layers separate.

## 9–13. Presets, randomization and appearance data

Every preset is reproducible through the normal system, tested as Preset, Advanced Mode, Edit, Save, Reload without unexpected change, and no preset uses hidden geometry. Randomization testing inspects large samples for validity, diversity, distributions, extremes, accidental correlations, repeated convergence, selective randomization and locks, and is reproducible where testing, persistence or networking need it. **One unified conceptual appearance record** describes the final appearance whether the character came from a preset, advanced customization, random generation or NPC generation, with no separate systems for presets and custom characters. Saved appearance data needs schema and version tracking, a migration strategy and deterministic interpretation where required, so saves don't silently break or change as the system evolves, with implementation OPEN. Target operations include randomizing face, body or hair and presentation only, and preserving age, frame, selected facial traits or chosen body attributes, with the UI still to be designed.

## 14–18. World, equipment, movement, cameras and mounts

World validation covers doors, ceilings, stairs, chairs, beds, ladders, tables, counters, tunnels, interaction points, conversation framing, cameras, equipment, weapons, mounts, collision, navigation, animation and IK, against approved target anatomy, not just what the prototype can reach. Equipment accounts for height, frame, composition, hands, feet, head and face, hair and deformation, without scaling every piece with height. Canonical equipment dimensions stay independent of cosmetic whole-character scaling unless explicitly designed otherwise. Movement visually respects height, limb proportions, mass, frame and composition, but tall or heavy-looking characters aren't automatically slower, muscular ones faster, or narrow ones more agile, since gameplay effects need explicit review. **OPEN:** first-person and third-person camera implications, collision, interaction and combat reach, hit detection and height-dependent camera placement, and none of these is set automatically by whole-character visual scale. Mounts are OPEN and must fit the approved envelope, with no single saddle or rider pose assumed to work across all races or even all Marchfolk extremes.

## 19–20. Technical handoff and prototype authority

No choice is made among MetaHuman, modified MetaHuman, custom architecture, shared or modified skeletons, morph-heavy, bone-driven proportions, procedural deformation or hybrids. The evaluation criteria are approved anatomy, animation quality, clothing and equipment, IK, cameras, collision, networking, save and load, performance and maintainability. The existing UE5 character stays a prototype, and known differences don't override the design under Approved Design Specification > Open Decision Register > Prototype Implementation. Nothing is refactored just because the spec differs, and implementation begins only when explicitly authorized.

## 21. First-pass completion

**MARCHFOLK FIRST-PASS CHARACTER DESIGN is complete.** v1.0–v1.5 together define it, and it's the primary human biological reference for comparative race design. Unresolved decisions stay in the Decision Register. Before Halvren, v1.0 and v1.5 are compared against v1.1–v1.4, and the findings are recorded below.

# Marchfolk consistency resolution, Part 1: terminology and character-system normalization

These clarify the approved design and aren't UE5 instructions. They resolve consistency findings 1–6, and all resolutions are AGREED.

| Topic | Resolution |
| --- | --- |
| Athletic (§1) | Skeletal frame describes skeletal structure, and Marchfolk frame presets stay Narrow, Balanced and Broad. Athletic belongs exclusively to physical-composition presets and may initialize muscularity, body-fat amount and distribution, regional muscle and other non-skeletal parameters. It never automatically changes skeletal shoulder breadth, ribcage or pelvic dimensions, limb-bone proportions, joint scale or other frame parameters. v1.4's "proportions" means physical-composition relationships, and "four frames" becomes three skeletal-frame starting categories plus independent physical-composition presets (the v1.1 and v1.4 text is corrected) |
| Body fat (§2) | **Body-fat amount** (how much adipose tissue overall) and **body-fat distribution** (where it's preferentially represented) are separate parameters, and the quick body controls (v1.1 §1) conceptually support both. v1.1's "overall body-fat distribution" is incomplete wording, not a removal of amount. Detailed controls may add regional distribution, and distribution never substitutes for amount |
| Thickness (§3) | "Thickness" isn't used alone where several tissues could produce the visible dimension. Specs distinguish skeletal breadth or diameter, muscular development, adipose contribution and total external circumference or visible volume. Neck, upper-arm, forearm, thigh and calf "thickness" aren't automatically skeletal controls, and a control that changes circumference through several systems documents which components contribute |
| Hand and foot size (§4) | These distinguish absolute dimensions (measured size) from proportional dimensions (relative to height, limb length or neighboring anatomy), plus skeletal dimensions, soft-tissue contribution, length, breadth and depth where relevant. One generic size scalar isn't a sufficient biological definition, and exact controls are future work |
| Frame (§5) | **Skeletal Frame** is the underlying continuous configuration of shoulder, ribcage, pelvis, joints and related structural dimensions. A **Frame Preset** is a starting configuration within that space: Narrow, Balanced and Broad are editable starting points, not immutable biological castes, and players may customize away from them within valid Marchfolk anatomy. "Frame" means the anatomical layer when discussing biology, and "Frame Preset" means the starting configurations |
| Baseline (§6) | Marchfolk are the primary **Human Reference Population**, and about 173 cm (5'8") is the Marchfolk **Reference Height**. Minimum and maximum remain the approved playable envelope, and "baseline" isn't used for both where it could be ambiguous (the v1.0 section, v1.1 height table and notes now use these terms) |
| Layers (§7) | **Character Architecture Layers** are A, Biological Anatomy; B, Skeletal Frame; C, Physical Composition; and D, Personal Presentation. **Skin Appearance Layers** are 1, Natural; 2, Environmental; 3, Applied; and 4, Acquired. Inheritance discussions name the relevant Character Architecture Layer, and Skin Appearance Layers organize appearance state and aren't inheritance categories |
| Age (§8) | **Chronological age** is elapsed time since birth. **Apparent biological age** is the physical age state expressed by the character's biology, which may not map one-to-one to chronological age if populations mature or age at different rates. **Age presentation** is social or personal presentation through hair, grooming, clothing, cosmetics and similar choices. All three stay distinct: the same chronological age can mean different apparent biological ages across populations, and similar apparent ages can be presented differently |

**Halvren importance (§9).** These corrections are required before mixed-ancestry design. Halvren inheritance must say whether an inherited characteristic affects biological anatomy, skeletal frame, physical-composition tendencies, pigmentation, hair biology, ocular biology, external ears or lifecycle biology. Personal presentation is never treated as genetically inherited, and cultural inheritance is separate from biological inheritance.

**Status (§10).** Findings 1–6 are resolved. No UE5 changes, and Halvren waits for the Marchfolk and Halvren pre-inheritance resolution, Part 2.

# Marchfolk and Halvren pre-inheritance resolution, Part 2: human pigmentation, ears, lifecycle and ancestry scope

This is design only. It resolves consistency findings 7–10 sufficiently to begin the Halvren first pass, with the listed subtopics still OPEN. No UE5 changes, and full Halvren anatomy isn't begun.

## 1–2. Marchfolk pigmentation (AGREED, broad human biological envelope)

| Trait | Valid families |
| --- | --- |
| Skin | Very light or fair, light, intermediate, olive, tan and bronze, brown, deep or dark brown |
| Undertones | Cool, neutral, warm, golden, olive, reddish where appropriate |
| Natural hair color | Black, dark brown, brown, light brown, blond, auburn and red, related natural intermediates. Age-related depigmentation stays separate |
| Iris | Brown, dark brown, hazel-like, amber where appropriate, green, gray, blue, related grounded intermediates |

Exact Marchfolk frequencies are OPEN. Not every valid trait is equally common, and Marchfolk aren't defined by any one modern real-world population. **Validity isn't frequency (locked):** the envelope sets what may occur, while future population design may add frequencies, geographic subpopulations, correlations, migration and regional ancestry, with no rigid phenotype packages.

## 3–4. Human external ear (AGREED)

Marchfolk have ordinary human external-ear anatomy within broad natural variation: coherent skull attachment, auricular base or root, helix, antihelix, concha, tragus and antitragus region, lobe, projection, vertical orientation and curvature. They vary in ear length and breadth, lobe size and attachment, projection from the skull, vertical position, angle, curvature and natural asymmetry. They don't naturally have the elongated, tapered non-human elven ear architecture. **Locked:** human and elven ears aren't "pointiness 0% versus 100%." They're different architectures (human versus related non-human elven), and mixed ear inheritance is never solved by linearly interpolating one pointiness slider.

## 5–6. Lifecycle (partially open)

Marchfolk follow broadly human-like maturation and aging, and stay the human lifecycle reference. Average and maximum lifespan, maturation milestones, fertility span and senescence rate are E, OPEN, and no years are invented just to enable Halvren. Halvren design can proceed without lifespan numbers if the inheritance architecture preserves chronological age, apparent biological age and population-specific maturation and aging relationships. A Halvren lifespan isn't assumed to be the arithmetic midpoint, and lifecycle inheritance may be nonlinear.

## 7–9. Ancestry scope (AGREED)

| Family | Populations | Rule |
| --- | --- | --- |
| Human | Marchfolk, Skarn, Sagekin | Marchfolk are the primary Human Reference Population, not the only human population, so Human never equals Marchfolk |
| Elven | Fenn, Aelari, Vael | Elf never equals one generic elven phenotype, and the Elf Comparative Review defines shared ancestry and divergence |

**Halvren are a flexible mixed human and elven ancestry population or category, not just Marchfolk crossed with a generic elf.** The framework can represent ancestry from any established human-family and elven-family population. This sets biological capability, not lore frequency.

## 10–13. Possibility, frequency and inheritance architecture

**Locked:** a biologically possible combination needn't be equally common. Lore may make combinations common, uncommon, rare, regionally concentrated, historically recent or established, but valid ancestry is never prohibited just for being uncommon, and not every combination is equally represented. Halvren aren't six (or more) fixed crossbreeds such as Marchfolk-Fenn or Skarn-Fenn. Those combinations may inform generation but aren't separate playable races, and Halvren stay capable of individual variation. **Multigenerational ancestry:** not every Halvren has one fully human and one fully elven parent. The system must eventually represent first-generation, Halvren plus human, Halvren plus elf, Halvren plus Halvren and more complex histories, without Mendelian percentages or genetic simulation yet. **The Halvren phenotype is never hardcoded to exactly 50/50 ancestry.** Inheritance is never human trait plus elf trait divided by two, and may involve polygenic expression, dominance-like and recessive-like relationships, trait correlations, developmental constraints, population distributions and setting-specific mechanisms. Genetic simulation depth is OPEN.

## 14–15. Culture and terminology

Biological ancestry never determines culture, birthplace, language, clothing, religion, occupation, personality, social identity or community membership. A Halvren with Fenn ancestry needn't be forest-raised, with Aelari ancestry needn't follow Aelari culture, with Vael ancestry needn't be subterranean-raised, and with Skarn ancestry needn't belong to Skarn culture. Until lore review, **human ancestry** and **elven ancestry** name the families, with specific population names where relevant (Marchfolk, Skarn, Sagekin, Fenn, Aelari or Vael ancestry). "Half" isn't used to imply an exact percentage unless the character's ancestry actually warrants it, and "Halvren" stays the playable race and population name.

## 16–17. Still open, and status

These stay open and don't block the Halvren first pass: Marchfolk pigmentation frequencies, human and elven lifecycle numbers, Halvren lifecycle expression, the mixed-ancestry genetic model, trait dominance, multigenerational inheritance math, population frequency of specific combinations, the social and lore definition of who counts as Halvren, and whether ancestry shows to the player as percentages, family populations, neither or something else. **Findings 7–10 are resolved sufficiently to begin the Halvren first pass**, with those subtopics OPEN. Preserved: Marchfolk v1.0–v1.5, consistency resolution Part 1, this Part 2, and the Elf Comparative Review v1.0 with all clarifications. The next step then waited for Halvren Character Design v1.0 (mixed-ancestry biological foundation), since completed.
