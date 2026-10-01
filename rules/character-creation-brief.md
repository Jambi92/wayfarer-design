# Character Creation & Race Design

This is the agreed direction from Tyler's four-part brief, received September 30, 2026. Race provides the biological foundation, individual customization creates the person, and presentation creates the character's identity. Nothing here is implemented yet, and every number is a design reference, not a final value.

## Status of the brief

All of sections 1–20 have been received. The missing §16.11–16.13 (Pipkin, Cogling and Saurin) were restored on September 30. Part 1 ended mid-sentence at "The final system" in §9, but Part 2 continues §9, so at most that one sentence is lost.

## Principles (§1–8, §17–19)

- **Race is biology, not a costume.** Skeleton, proportions, limbs, joints, scale, musculature, skull, racial face, skin or scales, ears, tails, horns, center of gravity and movement all come from race.
- **Each race is a range, not one body.** Customization changes the individual without destroying racial identity.
- **Race reads through silhouette, proportions, face, anatomy and movement.** Height alone never defines race: a tall Marchfolk and a short Skarn still look different.
- **Sliders are anatomically linked.** Muscle, mass and height reshape the whole body coherently. They never stretch one region on its own.
- **Movement is identity.** Skarn transfer weight heavily. Fenn place their feet quietly and keep their balance. Durrim are low and compact. Gorrund carry big momentum. Pipkin accelerate quickly with a short stride. **SUPERSEDED for Pipkin:** see `specs/pipkin/PIPKIN_V1.md` Part 5 §37; quick acceleration is not an automatic racial property, while shorter absolute stride may emerge from anatomy. Saurin move like reptiles, with the tail as a counterbalance.
- **Appearance has five sources:**
  - race: biology
  - culture: clothing, jewelry, grooming, gestures
  - occupation: muscle, calluses, scars, posture, wear
  - age: a real system variable affecting skin, hair, muscle, posture, face and movement
  - genetics: face, proportions and asymmetry
- **Grounded fantasy.** Avoid plastic skin, perfectly symmetrical faces, bodybuilder proportions, weightless movement, generic armor, oversized weapons, ornament with no purpose, racial caricature, casts where everyone is young and attractive, one body type per race, glowing magic everywhere, and non-humans made by bolting features onto a human body.
- **The central test (§19).** Two characters of the same race and class, at about the same height and mass, still look like different people. Two very different characters still read as the same race.

## Three layers (§3–4)

| Layer | Covers | Freedom |
| --- | --- | --- |
| Race | Skeleton, proportions, racial face, height and mass range, unique anatomy, skin or scales, ears, tail | Locked or heavily constrained |
| Individual | Body: height, weight, muscle, fat distribution, shoulder, chest, waist and hip width, limb and neck thickness, hand and foot size. Face: head size, jaw, chin, cheekbones, brow, nose, eyes, lips, face width and length, ears within limits, asymmetry. Also age, hair, skin (tone, freckles, moles, scars, birthmarks), tattoos and makeup | Within racial limits |
| Presentation | Hairstyles, facial hair, clothing, armor, jewelry, weapons, accessories, dyes, cultural items | Highly flexible, respecting race, culture, occupation and equipment |

## Character creator (§9–14)

- **One framework.** Presets, randomized characters, player characters, saved appearances and NPCs are all outputs of the same system.
- **Presets.** Each race has curated presets. They are real outputs of the customizer, not separate models, and players can edit them. They show variety rather than Default Male and Default Female. Illustrative examples:
  - Marchfolk: Frontier, Noble, Laborer, Wanderer, Scholar, Soldier
  - Fenn: Forest Hunter, Canopy Scout, Woodland Artisan, Warrior, Elder
  - Durrim: Miner, Smith, Soldier, Merchant, Elder
- **Modes.** Simple is Race → Preset → Confirm. Advanced is Race → Preset → Customize → Confirm.
- **Randomize.** Options are Everything, Face, Body, Hair, Appearance, Clothing, and Scars and Tattoos. Players can lock chosen traits, and results always stay within the race's limits.
- **Saving.** Players can save, load, duplicate and modify appearances. Import and sharing may come later.
- **Compatibility (§9).** The system must work with skeletons, meshes, animation and retargeting, IK, collision, hitboxes, camera height, first- and third-person views, traversal, mounting, equipment and armor fitting, weapon handling, physics, networking and performance.

## The 13 races (§15–16)

Height and mass are relative to an average Marchfolk adult. They are references, not stats.

| # | Race | Archetype | Height | Mass | Foundation |
| --- | --- | --- | --- | --- | --- |
| 1 | Marchfolk | Human | 1.00× | 1.00× | The baseline for movement, equipment and customization, with broad variation |
| 2 | Skarn | Barbarian | \~1.20× | \~1.40× | Broad clavicles, deep ribcage, thick joints, large hands and feet, heavy weight transfer. Enormous humans, not mini-ogres |
| 3 | Sagekin | Erudite | Human | Human | Human skeleton and variation. Scholarly identity comes from culture and lifestyle, not frailty |
| 4 | Fenn | Wood elf | \~1.05× | \~0.85× | Lean, long limbs, strong legs, tapered ears, pronounced cheekbones, quiet feet, controlled landings |
| 5 | Aelari | High elf | \~1.10× | \~0.90× | Tall, refined, upright, narrow waist, precise and deliberate movement. Not all young or aristocratic |
| 6 | Vael | Dark elf | \~1.05× | \~0.90× | Lean and controlled, slightly larger eyes. Skin in charcoal, cool gray, dusky violet, blue-gray or desaturated brown |
| 7 | Halvren | Half-elf | \~0.98–1.03× | \~0.95× | An in-between skeleton with wide variation in face, ears and limbs. Not humans with pointed ears |
| 8 | Durrim | Dwarf | \~0.65× | \~1.05× | Broad torso, short limbs, thick joints, powerful hips, large hands, low center of gravity. Not scaled-down humans |
| 9 | Grask | Troll | \~1.15× | \~1.40× | Heavy torso, thick textured skin, dense muscle, strong swimmers. Regeneration shows without being grotesque |
| 10 | Gorrund | Ogre | \~1.45×+ | \~2.00×+ | Massive frame, huge hands and feet, long arms, their own momentum, turning and landing. Giant-kin, not scaled humans |
| 11 | Pipkin | Halfling | \~0.55× | \~0.50× | Small compact adults: large head, strong legs, substantial feet, dexterous hands, low center of gravity. Not children or comic relief |
| 12 | Cogling | Gnome | \~0.45× | \~0.40× | Very small: compact torso, long fingers, narrow limbs, expressive face, fine motor control. Tinkering shows through culture, not caricature |
| 13 | Saurin | Iksar-inspired | \~1.05× | \~1.00× | Truly reptilian: own skull, jaw, teeth, scales and a working tail. Not humans with lizard heads |

### 16.11 Pipkin (halflings)

- Height about 0.55×, mass about 0.50× the human baseline.
- Small, compact adult anatomy: a relatively large head, strong legs, substantial feet, dexterous hands and a low center of gravity.
- Short stride, quick acceleration, rapid turns and excellent balance. **SUPERSEDED:** see `specs/pipkin/PIPKIN_V1.md` Part 5 §37. Only anatomy-derived stride/cadence relationships remain; acceleration, turning and balance are separate gameplay decisions.
- They are adults of a naturally small race, not human children or comic relief.
- Individuals vary in height, physique, face, muscle, body fat, age and overall appearance.

### 16.12 Cogling (gnomes)

- Height about 0.45×, mass about 0.40× the human baseline.
- Very small, compact, dexterous anatomy: a compact torso, relatively long fingers, narrow limbs, an expressive face and fine motor control.
- Quick steps, frequent turns, efficient climbing, precise hand movements and small physical adjustments.
- Engineering and tinkering show through culture, occupation, clothing, tools and equipment, not biological stereotypes.
- Avoid universally oversized noses, enormous hats, giant goggles and comedic proportions.
- Individuals vary meaningfully within the race's anatomy.

### 16.13 Saurin (reptilian people)

- Height about 1.05×, mass about 1.00× the human baseline.
- A genuinely reptilian foundation: a distinct skull, jaw, teeth, scales and musculature, a tail, and possibly a modified leg and foot structure.
- Scale size, texture, thickness, pattern and pigmentation vary across body regions.
- The tail works biologically: balance, turning, swimming, acceleration and body language.
- Locomotion reflects different hip, shoulder, torso and tail mechanics.
- The head has a recognizably reptilian skull, not a human face covered in scales. The eyes and face stay expressive within that biology.
- They are not humans with lizard heads or scales painted onto a human mesh. They may need a substantially different skeleton, rig and animation approach in UE5.
- Customization is extensive: body proportions, facial anatomy, scale patterns, pigmentation, markings, age and other fitting traits.

### Reminder for all races

The height and mass multipliers are preliminary design references, not final dimensions or gameplay statistics. The descriptions set each race's general physical identity, not a mandatory look for every individual. Players get real freedom within those biological boundaries. Actual ranges, restrictions, presets and race-specific controls are set in the next design phase.

Each race will get three formal specifications: its racial foundation, its character creation range and its preset library.

## Next phase: race specifications (§20)

Each race specification covers 14 items:

- what is locked, strongly restricted and free
- minimum, average and maximum ranges
- face, body and age variation
- hair and facial hair
- skin, scales and markings
- movement
- gear fit
- presets
- randomization rules
- UE5 requirements

Every trait is classed as LOCKED, CONSTRAINED or FREE. The phases below are a design sequence, not a ranking:

1. Marchfolk: the human baseline.
2. Skarn and Sagekin: human variations.
3. Fenn, Aelari, Vael and Halvren: the elven and mixed-ancestry foundations.
4. Durrim, Pipkin and Cogling: small bodies.
5. Grask and Gorrund: large bodies.
6. Saurin: reptilian anatomy and movement.

Each race is then checked visually with a few characters at the extremes of height, mass, muscle, age, face and silhouette.

The next task is the Marchfolk Character Customization Specification v1.0, worked out together. There is no character-system code or final numbers until then.

## Universal amendment v0.1: four independent layers

This is agreed as a universal design principle for all 13 races. It is a design decision only: specific anatomical options, terminology, deformation methods and technical implementation are still to be finalized.

| Layer | Controls | Marchfolk starting options |
| --- | --- | --- |
| A. Biological anatomy | The underlying anatomical configuration, including relevant sex-related physical traits, within the race's biological foundation | To be defined |
| B. Skeletal frame | Starting skeletal proportions | Narrow, Balanced, Broad (editable, not permanent categories) |
| C. Physical composition | Muscularity, fat distribution, regional muscle development, overall physique | Lean, Athletic, Muscular, Heavy, Custom |
| D. Personal presentation | Hair, facial hair, clothing, makeup, scars, tattoos, accessories | Not restricted by frame |

- **Independence.** Choosing an anatomy doesn't automatically set height, frame, muscularity, fat distribution, hairstyle, facial structure, clothing, class, occupation or personality. Any biological limit comes from the race's established anatomy, never from arbitrary preset rules.
- **Height.** Marchfolk stays at 147–173–203 cm, with no separate limits by anatomical configuration.
- **Other races.** Each race may need different anatomical configurations and limits. Non-human races are not assumed to share human sex-related anatomy.
- **Data.** The four layers are distinct parameter groups in the one unified appearance record, so presets, player characters, randomized characters and NPCs stay compatible.
- **Creator.** Simple mode picks a complete curated preset. Advanced mode exposes the four layers separately. Switching modes keeps the appearance.
- **Supersedes.** Athletic is no longer a skeletal frame. It belongs to physical composition.

## Contradictions with the earlier plan

- **Race scales.** The game's placeholder scales run from 0.7× (Pipkin) to 1.22× (Gorrund). The brief runs from 0.45× (Cogling) to 1.45× or more, with Durrim at 0.65×. The game code is unchanged until the specifications set real ranges.
- **Starting from MetaHuman.** The plan had Durrim, Grask and Gorrund starting from reshaped MetaHuman bodies. The brief says Durrim must not be scaled-down humans and Gorrund cannot use scaled-up human locomotion. MetaHuman can still supply a starting mesh, but each needs its own proportions and movement set. This gets decided in phases 4 and 5.
- **Race descriptions.** The old descriptions contradicted or went beyond the brief: Durrim "beards", Halvren "slightly pointed ears", Sagekin "slimmer builds", Grask "hunched, long arms" and Gorrund "small head". The hunch and small head were my guesses. The main tab now uses the brief's wording.
- **Race checklist.** The old per-race checklist is superseded by the 14-point specification above.
- **Order of work.** The creator plumbing was next in the old plan. It is on hold per the brief's final instruction.

## Details the brief leaves open

- **Sex and body type.** Partly settled by amendment v0.1: biological anatomy is its own layer and doesn't set height or build. Each race's specific anatomical options are still open.
- **First-person view.** §9 lists first-person, but the game is third-person only today. Is a first-person view planned?
- **Race and class limits.** The brief doesn't cover EverQuest-style race and class restrictions.
- **Culture.** Is culture fixed by race, or a separate choice, such as a Marchfolk raised among the Fenn?
- **Size in gameplay.** Does size affect reach, hitboxes or stats? The brief says the multipliers are not gameplay statistics, but a Gorrund's larger hitbox still matters in combat.
- **Mounts.** Mounting is listed, but the game has no mounts yet.
