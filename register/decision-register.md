# Character System Decision Register

This register tracks every character-system decision and its status: 14 agreed, 3 preliminary and 7 open as of September 30, 2026. Nothing here is implemented in UE5 yet.

| Decision | Status | Source |
| --- | --- | --- |
| Biological anatomy, skeletal frame, physical composition and personal presentation are four separate, independent layers | AGREED | Universal amendment v0.1 |
| Marchfolk skeletal frames are Narrow, Balanced and Broad. Athletic is a physical-composition preset | AGREED | Amendment v0.1 (supersedes v1.1 §2 and v1.4 §1) |
| Race is the biological foundation. Individuals vary within each race's range, and customization never erases racial identity | AGREED | Brief §1–7 |
| One unified appearance framework serves presets, randomized characters, player characters, saved appearances and NPCs | AGREED | Brief §14, §19; amendment v0.1 |
| Presets are saved outputs of the standard customizer, with no separate models and no preset-only features | AGREED | Brief §10; Marchfolk v1.4 |
| Simple mode (Race → Preset → Confirm) and Advanced mode (adds Customize) share data, and switching keeps the appearance | AGREED | Brief §11; Marchfolk v1.1, v1.4 |
| Every trait is classed as LOCKED, CONSTRAINED or FREE | AGREED | Brief §20 |
| Race design order runs Marchfolk, then Skarn and Sagekin, the elves and Halvren, the small races, the large races, and Saurin | AGREED | Brief §20 |
| Muscularity and body fat are independent controls, not one thin-to-heavy slider | AGREED | Marchfolk v1.1 |
| Regional muscle emphasis is cosmetic, with no gameplay advantage | AGREED | Marchfolk v1.1 |
| The initial creator covers adults only. Age is continuous and carries no gameplay penalties | AGREED | Marchfolk v1.4 |
| Skin has three independent layers: natural, environmental, and applied or acquired | AGREED | Marchfolk v1.3 |
| Facial-hair color is linked to hair color by default and can be unlinked | AGREED | Marchfolk v1.3 |
| Body frame, apparent age, presets and class stay uncoupled | AGREED | Marchfolk v1.4; amendment v0.1 |
| Marchfolk height is 147 cm minimum, 173 cm baseline, 203 cm maximum, with no separate limits by anatomy | PRELIMINARY | Marchfolk v1.1; amendment v0.1 |
| Race height and mass multipliers (§16) are references, not stats | PRELIMINARY | Brief §16 |
| Marchfolk preset themes are Frontier Settler, Traveling Scholar, Veteran Soldier, Rural Laborer, Merchant and Elder Wanderer | PRELIMINARY | Marchfolk v1.4 |
| Specific anatomical options, terminology and deformation methods | OPEN | Amendment v0.1 |
| Morph-target architecture for the face | OPEN | Marchfolk v1.2 |
| Sex-related anatomy for each non-human race | OPEN | Amendment v0.1 §4 |
| Whether a first-person view is planned | OPEN | Brief §9 |
| EverQuest-style race and class restrictions | OPEN | Built into the current implementation, but the final design is open (audit gap 8): neither removed nor approved |
| Whether culture is fixed by race or chosen separately | OPEN | Brief §18 |
| Whether size affects hitboxes and reach in combat | OPEN | Brief §16 |

**Architecture**

| Decision | Status | Source |
| --- | --- | --- |
| Character design requirements determine technical architecture. Technical convenience never redefines approved anatomy without explicit design review | AGREED | Architecture note, Sep 30 2026 |
| No race has a committed technical foundation. MetaHuman and the others are candidates only. Aelari and Vael aren't assumed to match Fenn, and Halvren stays especially open | AGREED | Architecture note, Sep 30 2026 |
| Plan statements are labeled CURRENT IMPLEMENTATION, TARGET DESIGN REQUIREMENT or CANDIDATE TECHNICAL APPROACH, never interchangeably | AGREED | Architecture note, Sep 30 2026 |
| The shared human animation set with uniform scaling is a prototype placeholder. No premature refactor until specs and prototypes justify it | AGREED | Architecture note, Sep 30 2026 |
| Racial attribute bonuses, via a future Race → Biology → Gameplay Attributes Review separating biology from culture, background, training and class. Current stats aren't canon, and the Sagekin Intelligence bonus is especially under review | OPEN | Known gap 7 in the main plan |

| Decision | Status | Source |
| --- | --- | --- |
| Authority rule: Approved Design Specification > Open Decision Register > Prototype Implementation. Implementation never overrides a spec or resolves an OPEN item | AGREED | Audit resolution, part 1 |
| Four plan labels: CURRENT IMPLEMENTATION, TARGET DESIGN, OPEN DECISION, CANDIDATE TECHNICAL APPROACH | AGREED | Audit resolution, part 1 |
| Future appearance data supports schema and version tracking with migration | AGREED | Audit resolution, gap 2 |
| Visual anatomy, equipment dimensions, collision, interaction reach, combat reach and camera placement are separate. Equipment never scales with the holder | AGREED | Audit resolution, gap 6 |
| Individual cosmetic variation within a race gives no automatic gameplay advantage or penalty (refines the earlier cosmetic-size rule) | AGREED | Audit resolution, gap 6 |
| Whether major racial size differences affect collision, reach, movement or combat | OPEN | Audit resolution, gap 6 (open balance decision). Deferred until all 13 races are done |
| Whether creator race descriptions are neutral, in-world or both. Deferred until all 13 races are done | OPEN | Audit resolution, gap 9 |
| Creator race descriptions distinguish biological ancestry from culture and reputation | AGREED | Audit resolution, gap 9 |

**Skarn**

| Decision | Status | Source |
| --- | --- | --- |
| Skarn identity comes from underlying anatomy, not from height or muscle. They are not scaled-up Marchfolk | AGREED | Skarn v1.0 §1 |
| Frames and composition work inside Skarn limits, and a Broad Skarn stays distinct from Gorrund | AGREED | Skarn v1.0 §4–5 |
| Skarn keep the 1.5× breath-hold trait, with no rebalance yet | AGREED | Skarn v1.0 §9 |
| Skarn height is 183 cm minimum, 208 cm reference, 229 cm maximum | PRELIMINARY | Skarn v1.0 §2 |
| Skarn craniofacial ranges | OPEN | Skarn v1.0 §8 (later spec) |

| Decision | Status | Source |
| --- | --- | --- |
| Skarn baseline is slightly torso-dominant, with deeper chest, broader back and heavier joints, while long-legged Skarn stay possible | AGREED | Skarn v1.1 §1–2 |
| Regional muscle stays tied to overall muscularity and is cosmetic | AGREED | Skarn v1.1 §6 |
| Universal (proposed): body weight is derived from height, frame, muscle, fat and proportions, never set directly | PRELIMINARY | Skarn v1.1 §7, awaiting confirmation |

| Decision | Status | Source |
| --- | --- | --- |
| All races use the same seven facial regions. Race changes the ranges, not the editor | AGREED | Skarn v1.2 §2 |
| Skarn facial traits are tendencies, never mandatory. Facial hair isn't needed for identity | AGREED | Skarn v1.2 §1, §11 |
| Old age isn't frailty, and older, imposing Skarn stay possible | AGREED | Skarn v1.2 §8 |
| Universal (proposed): body composition gently influences facial soft tissue without overriding facial choices | PRELIMINARY | Skarn v1.2 §7, pending validation |
| Universal (proposed): a Naturalize Face option adds small, bounded asymmetry | PRELIMINARY | Skarn v1.2 §9, pending testing |

| Decision | Status | Source |
| --- | --- | --- |
| Skarn have full natural human skin-tone variation, with no single mandatory color | AGREED | Skarn v1.3 §2 |
| Race never applies cultural hairstyles, markings or facial hair automatically | AGREED | Skarn v1.3 §4–7 |
| Appearance never assumes a race shares one culture, and it stays compatible with separate race, culture, background and class | AGREED | Skarn v1.3 §9 |
| Universal (proposed): race is biology, culture is presentation, history is acquired appearance, kept separate | PRELIMINARY | Skarn v1.3 §1 |
| Universal (proposed): environmental weathering varies by body region | PRELIMINARY | Skarn v1.3 §3 |
| Universal (proposed): presentation presets, separate from anatomy presets | PRELIMINARY | Skarn v1.3 §8, pending design review |

| Decision | Status | Source |
| --- | --- | --- |
| Skarn preset themes: Northern Hunter, Mountain Laborer, Seasoned Traveler, Clan Veteran, Skarn Scholar, Heavyset Merchant, Young Wanderer and Elder Wayfarer. Visual only | PRELIMINARY | Skarn v1.4 §1 |
| Randomization respects anatomical relationships and never sets sliders independently | AGREED | Skarn v1.4 §4 |
| Skarn must pass the silhouette, equal-height and anti-stereotype tests | AGREED | Skarn v1.4 §5–7, §9 |
| Marchfolk, Skarn and Gorrund are never scaled versions of one anatomy | AGREED | Skarn v1.4 §8 |
| Universal (proposed): randomization strengths Subtle, Diverse and Extreme (Extreme possibly for development only) | PRELIMINARY | Skarn v1.4 §2 |
| Universal (proposed): selective randomization with parameter and group locks | PRELIMINARY | Skarn v1.4 §3 |

| Decision | Status | Source |
| --- | --- | --- |
| Skarn visual and customization design is first-pass complete (v1.0–v1.5) | AGREED | Skarn v1.5 §11 |
| Skarn validation set SK-01 to SK-12 is kept as reproducible test configurations | AGREED | Skarn v1.5 §1 |
| Uniform mesh scaling is not assumed to give acceptable movement, and weapons keep true dimensions | AGREED | Skarn v1.5 §2, §5 |
| Cross-race architecture: shared customization concepts, with each race defining its own foundation, ranges, relationships, presets, randomization and validation | AGREED | Skarn v1.5 §8 |
| Sagekin: scholarly culture is never biological frailty or a universally thin body | AGREED | Skarn v1.5 §11; brief §16.3 |
| Universal (proposed): every playable race is validated against doorways, stairs, furniture, ladders, tunnels and interaction points | PRELIMINARY | Skarn v1.5 §6 |
| Skeleton strategy and deformation architecture (morphs versus alternatives) | OPEN | Skarn v1.5 §10 |
| Animation approach: shared, retargeted, procedural, IK or specialized | OPEN | Skarn v1.5 §2, §10 |
| Equipment fitting, including grip and attachment adaptation | OPEN | Skarn v1.5 §5, §10 |
| Camera heights per race (third-person, conversation, creator, first-person) | OPEN | Skarn v1.5 §3 |
| Character-data serialization, networking, LOD and performance | OPEN | Skarn v1.5 §10 |
| Mount support, with the data preserved: skeleton, height, leg length, pelvis, mass category | OPEN | Skarn v1.5 §7 |

**Sagekin**

| Decision | Status | Source |
| --- | --- | --- |
| Sagekin ancestry is biological, and their scholarly tradition is cultural. Intelligence, frailty and occupation are never anatomy | AGREED | Sagekin foundation §2, §8 |
| Sagekin are fully human, with overlapping population tendencies and no mandatory single trait | AGREED | Sagekin foundation §3, §9 |
| Sagekin support every frame and physique, wide height and full age variation, and hair is never a racial marker | AGREED | Sagekin foundation §4, §6 |
| Homeland is a warm southern or southeastern maritime civilization across the sea | PRELIMINARY | Sagekin foundation §1 (worldbuilding pending) |
| Somewhat longer-limbed tendency, and a pigmentation center of warm beige to deeper brown | PRELIMINARY | Sagekin foundation §4–5, pending validation |
| Exact Sagekin ranges: height, pigmentation, hair and craniofacial | OPEN | Sagekin v1.0 (next) |

| Decision | Status | Source |
| --- | --- | --- |
| Sagekin differences from Marchfolk are subtler than Skarn's, and some individuals may be ambiguous without context | AGREED | Sagekin v1.0 §1, §9 |
| Individual Marchfolk and Sagekin pairs don't have to look unmistakably different, only population-level distinct | AGREED | Sagekin v1.0 §10 |
| Sagekin height is 152 cm minimum, 178 cm reference, 208 cm maximum | PRELIMINARY | Sagekin v1.0 §2 |
| Sagekin proportion tendencies: slightly taller, slightly longer limbs, a more linear silhouette, possibly a narrower ribcage | PRELIMINARY | Sagekin v1.0 §3, §5 |

| Decision | Status | Source |
| --- | --- | --- |
| Sagekin stay within human proportions and never reproduce Fenn or Aelari anatomy. No elven traits are used to distinguish them | AGREED | Sagekin v1.1 §2 |
| Sagekin validation set SG-01 to SG-14, including a deliberate Marchfolk-overlap case (extended in v1.5) | AGREED | Sagekin v1.1 §10 |
| Sagekin body tendencies: longer legs, forearms and fingers, a slightly shorter and shallower torso, slightly narrower hands | PRELIMINARY | Sagekin v1.1 §1, §3–5 |
| No estimated weight shown to players until the system can calculate it credibly | AGREED | Sagekin v1.1 §8 |

| Decision | Status | Source |
| --- | --- | --- |
| Sagekin facial identity is a multi-trait population pattern, with no canonical face and no mandatory eye, nose or jaw type | AGREED | Sagekin v1.2 §1–7 |
| Sagekin pigmentation centers: skin warm beige to deeper brown, hair mostly black or dark brown, eyes mostly brown | PRELIMINARY | Sagekin v1.2 §9, pending worldbuilding |
| Universal (proposed): validity and frequency are separate (Very Common, Common, Uncommon, Rare per Sagekin v1.4), shaping NPCs and randomization, never limiting manual choice | PRELIMINARY | Sagekin v1.2 §8 |
| Mixed-ancestry support: not designed now, but architecture must not rule it out | OPEN | Sagekin v1.2 §11 |

| Decision | Status | Source |
| --- | --- | --- |
| Sagekin homeland pillars: Sea, Written Word, Heavens and Craft, a whole civilization rather than just libraries | PRELIMINARY | Sagekin v1.3 §1 |
| No universal Sagekin robes, hairstyles or tattoos. Unmarked Sagekin are normal, and Sagekin abroad may dress locally | AGREED | Sagekin v1.3 §4, §7, §9 |
| Sagekin presentation presets: Academy Formal, Harbor Practical, Merchant Urban, Traveler, Observatory Ceremonial, Working Artisan | PRELIMINARY | Sagekin v1.3 §10 |
| Universal (proposed): natural pigmentation and tanning or sun exposure are separate systems | PRELIMINARY | Sagekin v1.3 §2 |
| Universal (proposed): four identity layers (ancestry, birthplace, culture and background), none derived from another | PRELIMINARY | Sagekin v1.3 §11; extends Skarn v1.3 §9 |

| Decision | Status | Source |
| --- | --- | --- |
| Sagekin character presets: Academy Lecturer, Harbor Navigator, Urban Artisan, Merchant Traveler, Coastal Soldier, Heavyset Archivist, Young Wayfarer, Elder Astronomer | PRELIMINARY | Sagekin v1.4 §2 |
| Sagekin must pass the large-sample, clone and stereotype, cultural-neutralization and cross-cultural presentation tests | AGREED | Sagekin v1.4 §7–10 |
| Presentation never changes anatomy, and randomization keeps race unless the player changes it | AGREED | Sagekin v1.4 §10–11 |
| Universal (proposed): character presets and presentation presets are distinct categories | PRELIMINARY | Sagekin v1.4 §1 |
| Universal (proposed): soft trait correlations, with no rigid phenotype packages | PRELIMINARY | Sagekin v1.4 §5 |
| Population-aware randomization for inherited traits, while manual choice keeps the full valid range | AGREED | Sagekin v1.4 §3 |
| Sagekin regional subpopulations (coastal, interior, island, city) | OPEN | Sagekin v1.4 §6, future worldbuilding |

| Decision | Status | Source |
| --- | --- | --- |
| Sagekin visual and customization design is first-pass complete (v1.0–v1.5) | AGREED | Sagekin v1.5 §12 |
| Sagekin recognizability never comes from exaggeration, and they stay fully human, never pushed toward elves | AGREED | Sagekin v1.5 §2, §9, §12 |
| There's no universal movement style from ancestry alone, and movement follows anatomy, composition and equipment | AGREED | Sagekin v1.5 §3 |
| NPC generation layers are kept separate: ancestry, inherited appearance, individual variation, birthplace and culture, background, presentation | AGREED | Sagekin v1.5 §6 |
| Universal (proposed): customized faces are validated across speech, blink, eye movement and strong expressions | PRELIMINARY | Sagekin v1.5 §4 |
| Universal (proposed): generated characters are exactly reproducible (stored data or seeds) | PRELIMINARY | Sagekin v1.5 §7 |
| Birthplace system structure | OPEN | Sagekin v1.3 §11, v1.5 §11 |
| Background system structure | OPEN | Sagekin v1.3 §11, v1.5 §11 |
| Population-generation implementation (weights, constraints, soft correlations) | OPEN | Sagekin v1.4–v1.5 |

**Fenn**

| Decision | Status | Source |
| --- | --- | --- |
| Fenn have a genuinely non-human skeletal foundation. They are never thin humans with pointed ears | AGREED | Fenn v1.0 §1, §12 |
| Gracile never means fragile, and Fenn identity never depends on thinness. All frames and physiques are supported | AGREED | Fenn v1.0 §3–4, §8 |
| Fenn ears are real anatomy with their own controls, and no single mandatory ear shape | AGREED | Fenn v1.0 §9 |
| Fenn keep the sneak and swim traits, not rebalanced during design. Cosmetic body settings give no gameplay effect | AGREED | Fenn v1.0 §10–11 |
| Fenn height is 157 cm minimum, 181 cm reference, 211 cm maximum | PRELIMINARY | Fenn v1.0 §2 |
| Fenn proportion tendencies: longer limbs, hands, fingers and feet, a smaller torso share, narrower joints | PRELIMINARY | Fenn v1.0 §3, §5–7 |
| Fenn movement differences from anatomy (balance, center of mass, locomotion) | OPEN | Fenn v1.0 §10, to investigate |

| Decision | Status | Source |
| --- | --- | --- |
| Connected-anatomy rule applied to Fenn: the player sets the proportion, and the system keeps coherence | AGREED | Fenn v1.1 §1; master brief §7 |
| Fenn joints have minimum boundaries, so no fragile-looking joints at the lean extreme | AGREED | Fenn v1.1 §5 |
| Fenn feet are normal humanoid feet (no prehensile or animal-like feet), and there are no per-finger controls yet | AGREED | Fenn v1.1 §7, §9 |
| Fenn validation set FN-01 to FN-38 | AGREED | Fenn v1.0 §14, v1.1 §13 |
| Universal (proposed): combined-proportion validation, where legal parameters can form an illegal combination | PRELIMINARY | Fenn v1.1 §11 |
| Fenn pelvis morphology | OPEN | Fenn v1.1 §4, pending prototyping |

| Decision | Status | Source |
| --- | --- | --- |
| Fenn faces keep elven traits with the ears hidden. There's no canonical "beautiful elf face" and no mandatory nose, jaw, mouth or anime-like eyes | AGREED | Fenn v1.2 §1–7 |
| Fenn ears are their own anatomy (not stretched human ears), with conservative asymmetry. Ear damage belongs to acquired appearance | AGREED | Fenn v1.2 §8–11 |
| Fenn visibly age | AGREED | Fenn v1.2 §12 |
| Universal: no race is biologically required to be conventionally attractive | AGREED | Fenn v1.2 §13; master brief §17 |
| Fenn, Aelari and Vael lifespan and aging rate. None is assumed permanently youthful, and Vael aging is also tested against any special eye anatomy | OPEN | Fenn v1.2 §12, lore review |
| Elven ear mobility and expression (Fenn, Aelari and Vael), not assumed, settled in the Elf Comparative Review | OPEN | Fenn v1.2 §15 |
| Helmet and hood fit for long elven ears | OPEN | Fenn v1.2 §8–9; Marchfolk v1.2 |

| Decision | Status | Source |
| --- | --- | --- |
| No green skin as a default Fenn trait, and no mandatory long hair, braids or forest decoration | AGREED | Fenn v1.3 §2, §8 |
| Fenn culture is never primitive, with no universal leaf clothing. Forest life isn't explained by biological gimmicks | AGREED | Fenn v1.3 §9–10, §12 |
| Fenn pigmentation range: fair through rich darker brown, broad undertones | PRELIMINARY | Fenn v1.3 §2, frequencies unresolved |
| Fenn cultural pillars: Canopy, Path, Stewardship, Craft, Memory | PRELIMINARY | Fenn v1.3 §10 |
| Elven races (proposed): Fenn, Aelari and Vael each get their own pigmentation and hair distributions, and there's no default elf template | PRELIMINARY | Fenn v1.3 §1, §3 |
| Fenn low-light or canopy vision (paired with the Vael low-light question) | OPEN | Fenn v1.3 §9 |
| Exact Fenn pigmentation, hair and eye frequencies | OPEN | Fenn v1.3 §2, §7 |
| Comparative Fenn, Aelari and Vael pigmentation review | OPEN | Fenn v1.3 §4, after all three first passes |
| Detailed Fenn homeland regions and cultures | OPEN | Fenn v1.3 §16 |
| Culture architecture implementation | OPEN | Fenn v1.3 §16; Skarn v1.3 §9; Sagekin v1.3 §11 |

| Decision | Status | Source |
| --- | --- | --- |
| Fenn randomization never produces "human with pointed ears". Minimum-ear Fenn stay Fenn, and maximum-ear Fenn stay coherent | AGREED | Fenn v1.4 §5, §10 |
| Fenn must pass the composition stress, hidden-ear population, silhouette and facial population tests, plus the §15 failure checks | AGREED | Fenn v1.4 §6–9, §15 |
| Fenn character presets: Canopy Pathfinder, Forest Artisan, Broad Warden, River Traveler, Heavyset Trader, Elder Storykeeper, Foreign-Raised Fenn, Young Wanderer | PRELIMINARY | Fenn v1.4 §1 |
| Fenn presentation presets: Canopy Practical, Forest Formal, Trail-Worn, Ceremonial, Artisan, Foreign/Urban | PRELIMINARY | Fenn v1.4 §2 |
| Universal (proposed): biological randomization (ancestry and population) is separate from presentation randomization (culture, background, region, style) | PRELIMINARY | Fenn v1.4 §12 |

| Decision | Status | Source |
| --- | --- | --- |
| Fenn visual and customization design is first-pass complete (v1.0–v1.5) | AGREED | Fenn v1.5 §27 |
| No scaled human skeleton, stretched bones, human animation or MetaHuman is assumed final for Fenn | AGREED | Fenn v1.5 §1, §3 |
| No "graceful elf" animation just for being elves. Movement comes from anatomy, state, equipment and training | AGREED | Fenn v1.5 §4 |
| Headgear never automatically clips, hides or flattens Fenn ears, and not all headgear is Fenn-only | AGREED | Fenn v1.5 §11 |
| Fenn must pass the 20-item validation gate before implementation approval | AGREED | Fenn v1.5 §23 |
| Aelari must never simply be taller Fenn: shared deeper elven ancestry, but their own anatomical identity | AGREED | Fenn v1.5 §27 |
| First-person arms keep race proportions, never generic human arms (if first-person is supported) | OPEN | Fenn v1.5 §15 |

**Aelari**

| Decision | Status | Source |
| --- | --- | --- |
| Aelari are never taller Fenn, thin humans with ears, universally beautiful or pale, or biologically aristocratic or proud | AGREED | Aelari v1.0 §1 |
| Aelari identity is whole-body vertical elongation (cranium, neck, torso, arms, legs), never uniform scaling or stretched Fenn legs | AGREED | Aelari v1.0 §4–5 |
| Aelari support every frame and composition, identity never depends on thinness, and gracile never means narrow shoulders | AGREED | Aelari v1.0 §7, §12 |
| "High Elf = pale skin" is rejected. Culture, magic and prestige never set pigmentation | AGREED | Aelari v1.0 §14 |
| Universal: anatomical resting alignment is separate from cultural and personal body language, and pride or nobility is never biological | AGREED | Aelari v1.0 §13 |
| Aelari height is 168 cm minimum, 190 cm reference, 221 cm maximum | PRELIMINARY | Aelari v1.0 §3 |
| Provisional shared elven themes (gracile skeleton, joints, hands, ears, craniofacial) | PRELIMINARY | Aelari v1.0 §2, pending the Vael pass |
| Fenn and Aelari contrast: Fenn compact-centered with long extremities (forearm-weighted), Aelari elongated throughout (even arm elongation) | PRELIMINARY | Aelari v1.0 §5, §9, pending comparative validation |
| Aelari pigmentation, complexion, hair and eyes | OPEN | Aelari v1.0 §14, dedicated pass pending |
| Aelari technical foundation and MetaHuman suitability. Not assumed: stock MetaHuman, stock human skeleton, Fenn skeleton, uniform scaling or a fully unique skeleton | OPEN | Aelari v1.0 §17; audit |

| Decision | Status | Source |
| --- | --- | --- |
| Frame (Narrow, Balanced, Broad) changes the real skeleton (clavicle, ribcage, pelvic breadth, joints) and stays separate from muscle, fat, anatomy, height and presentation | AGREED | Aelari v1.1 §7; amendment v0.1 |
| Aelari joints have hard minimum boundaries, and there's no mandatory hip width by race or anatomy configuration | AGREED | Aelari v1.1 §5–6 |
| Aelari must pass the composition stress, equal-height Fenn, human boundary and Skarn boundary tests. Broad muscular Aelari never become narrow Skarn | AGREED | Aelari v1.1 §13, §15–17 |
| Aelari validation set AE-01 to AE-50 | AGREED | Aelari v1.0 §16, v1.1 §18 |
| Aelari proportion tendencies: longer ribcage and torso than Fenn, shallow chest, evenly elongated arms and legs, longer narrow hands and feet | PRELIMINARY | Aelari v1.1 §2–5, §9–12 |
| Elven pelvis morphology (Fenn and Aelari) | OPEN | Aelari v1.1 §5; Fenn v1.1 §4, pending prototyping |

| Decision | Status | Source |
| --- | --- | --- |
| Aelari faces come from combined relationships. There's no mandatory eye, nose, jaw or lip type, and "High Elf = small straight nose" and glowing or almond eyes are rejected | AGREED | Aelari v1.2 §1–8 |
| Aelari visibly age and aren't assumed permanently youthful. Cultural beauty ideals never set biological validity | AGREED | Aelari v1.2 §13–14 |
| Fenn and Aelari ear tendencies overlap and are never rigid species markers. A short-eared Aelari and a long-eared Fenn are both valid | AGREED | Aelari v1.2 §10 |
| Aelari facial and ear tendencies: taller cranium, longer face, lighter jaw, longer and narrower eyes, upward, close-set, tapered ears | PRELIMINARY | Aelari v1.2 §2–4, §10 |
| Halvren are never humans with medium-length ears, and the architecture stays flexible for intermediate ancestry | AGREED | Aelari v1.2 §18 |

| Decision | Status | Source |
| --- | --- | --- |
| "High Elf = pale + blond + blue or glowing eyes" is rejected. Blue, pale or luminous eyes and long hair are never required | AGREED | Aelari v1.3 §1, §6, §9 |
| Pride, wisdom, education, status and magic are civilization and reputation, never biology. White towers are architecture | AGREED | Aelari v1.3 §17, §19 |
| No universal robes, cultural hairstyles or markings, and Aelari raised elsewhere may use none | AGREED | Aelari v1.3 §15–16, §21–23 |
| Universal: hairstyle, length and grooming are never locked to sex-related anatomy, frame, physique or occupation | AGREED | Aelari v1.3 §14; Marchfolk v1.3 |
| Universal (proposed): biological iris color is separate from magical or supernatural eye effects, and there's no baked-in racial glow | PRELIMINARY | Aelari v1.3 §7 |
| Aelari skin and undertone range (fair through deeper brown; cool through olive and reddish undertones) | PRELIMINARY | Aelari v1.3 §2 |
| Aelari cultural pillars: Continuity, Record, Mastery, Form, Arcana | PRELIMINARY | Aelari v1.3 §18 |
| Aelari presentation presets: White-Tower Formal, Institutional Practical, Artisan, Military, Traveler, Provincial, Ceremonial, Foreign/Urban (v1.4 list, replacing v1.3 §24) | PRELIMINARY | Aelari v1.3 §24 |
| Whether naturally silver or white hair is a valid trait (Aelari, Vael, and any other applicable population), always kept distinct from age graying in the data | OPEN | Aelari v1.3 §11–12 |
| Aelari hair, eye and facial-hair frequencies | OPEN | Aelari v1.3 §6, §10–13, after the Elf Comparative Review |

| Decision | Status | Source |
| --- | --- | --- |
| Aelari must pass the generic-elf convergence test: randomization never keeps producing the tall, thin, pale, young, beautiful, blond, blue-eyed template | AGREED | Aelari v1.4 §14 |
| Aelari must pass the composition, ear, hidden-ear, Sagekin, Fenn and Skarn boundary, cultural neutralization and cross-cultural tests, plus the §24 failure checks | AGREED | Aelari v1.4 §15–22, §24 |
| The preset library must never teach one authentic Aelari look, and there's no preset-only anatomy | AGREED | Aelari v1.4 §3, §5 |
| Aelari character presets: White-Tower Archivist, Provincial Artisan, Tower Guard, Heavyset Merchant, Broad Craftworker, Traveling Aelari, Foreign-Raised Aelari, Elder Waykeeper | PRELIMINARY | Aelari v1.4 §2 |

| Decision | Status | Source |
| --- | --- | --- |
| Aelari visual and customization design is first-pass complete (v1.0–v1.5) | AGREED | Aelari v1.5 §29 |
| Grace, nobility, pride, elegance and magical movement are never biological. Longer legs never mean faster playback or uniform stride scaling | AGREED | Aelari v1.5 §5–6 |
| AE-03 (221 cm) is a permanent technical stress character, and the approved maximum height is never cut to fit the prototype's human scale | AGREED | Aelari v1.5 §24 |
| Gloves and boots follow each race's hand and foot anatomy, never uniformly enlarged human gear | AGREED | Aelari v1.5 §12 |
| Vael must never be dark-skinned Aelari or subterranean Fenn: deeper shared ancestry, but their own anatomy and pigmentation | AGREED | Aelari v1.5 §29 |
| Shared elven ancestry never automatically means one skeleton | AGREED | Aelari v1.5 §27 |
| Networking and multiplayer appearance synchronization | OPEN | Aelari v1.5 §28; Skarn v1.5 §10 |

**Vael**

| Decision | Status | Source |
| --- | --- | --- |
| Vael are never dark-skinned Aelari, subterranean Fenn, humans with ears, universally sinister or thin, or biologically evil, secretive or cruel | AGREED | Vael v1.0 §1 |
| "Compact" never means short, dwarven, stocky or automatically muscular, and Vael are never compact Skarn | AGREED | Vael v1.0 §4, §7 |
| Vael support every frame and composition, and identity never depends on thinness, muscle or fat | AGREED | Vael v1.0 §13 |
| No gimmick anatomy for underground life: no gripping toes, clawed feet, giant or glowing eyes, or daylight blindness assumed | AGREED | Vael v1.0 §12, §14 |
| Universal: ancestral biology, environmental adaptation, individual environmental exposure and culture are four separate layers | AGREED | Vael v1.0 §16 |
| Vael height is 157 cm minimum, 178 cm reference, 203 cm maximum (newer than the brief's \~1.05×) | PRELIMINARY | Vael v1.0 §3 |
| Three elven branches: Fenn compact-centered with strong extremities, Aelari elongated throughout, Vael compact, deep-bodied with more joint and extremity-base presence | PRELIMINARY | Vael v1.0 §4–12, §17 |
| Vael low-light biological adaptation, if any | OPEN | Vael v1.0 §14, face and eye design pending |
| Vael gameplay vision effect (versus humans and Fenn, or none) | OPEN | Vael v1.0 §15 |
| Vael pelvis morphology | OPEN | Vael v1.0 §8, pending prototyping |
| Vael technical foundation (MetaHuman not assumed) | OPEN | Vael v1.0 §20; audit |

| Decision | Status | Source |
| --- | --- | --- |
| Vael torso depth is skeletal (ribcage depth and curvature, spine, shoulders, torso-to-pelvis), never faked with fat, muscle or uniform scaling | AGREED | Vael v1.1 §2 |
| Three-elf silhouette matrix is a permanent test: same height, frame, muscle, fat, age and pose, with ears, hair, pigmentation and culture neutralized | AGREED | Vael v1.1 §20 |
| Durrim anatomy is never used to solve Vael compactness | AGREED | Vael v1.1 §27 |
| Vael must pass VL-16 to VL-18 (lean, muscular, high fat), the human, Skarn and Durrim boundaries, and the §29 failure checks | AGREED | Vael v1.1 §16–18, §25–29 |
| Vael validation set VL-01 to VL-42 | AGREED | Vael v1.0 §19, v1.1 §28 |
| Vael proportion tendencies: deeper, slightly shorter ribcage, shorter relative neck, somewhat less limb elongation, broader palms and feet, more joint presence, lower center of mass than Aelari | PRELIMINARY | Vael v1.1 §3–14, §23 |

| Decision | Status | Source |
| --- | --- | --- |
| Vael faces never depend on complexion, ears, glowing eyes, one feature type, attractiveness or a sinister look, and ordinary faces are explicitly supported | AGREED | Vael v1.2 §1, §9 |
| Strict hidden-ear, neutral-complexion test: Vael identity must survive with complexion neutralized | AGREED | Vael v1.2 §28 |
| Vael never look permanently angry, sinister, predatory or suspicious, and expression stays independent of ancestry | AGREED | Vael v1.2 §29 |
| No enormous eyes, eye shine, cat pupils or severe daylight weakness assumed. Vael function in shared above-ground spaces | AGREED | Vael v1.2 §11–15 |
| Vael facial and ear tendencies: stronger mid-face, broader cheeks and orbits, compact vertical face, broader-based, lateral, shorter-taper ears | PRELIMINARY | Vael v1.2 §2–8, §20 |
| Vael low-light eye mechanism (dilation, retina, photoreceptors, light gathering, neural processing) | OPEN | Vael v1.2 §13 |
| Vael pupil shape (round is a valid candidate) | OPEN | Vael v1.2 §14 |
| Vael daylight sensitivity, adaptation speed and bright-light discomfort | OPEN | Vael v1.2 §15 |

| Decision | Status | Source |
| --- | --- | --- |
| "Dark Elf = gray skin" is rejected. Vael skin is living tissue (perfusion, subsurface, regional variation), never flat or painted-stone monochrome | AGREED | Vael v1.3 §1–4 |
| Vael skin colors are never designed from cave lighting, and every approved family has a neutral-light reference | AGREED | Vael v1.3 §7 |
| Underground history never implies evil, cruelty, secrecy, fanaticism, hierarchy, magic or personality. There's no monolithic Vael culture, and not every Vael is a cave-dweller | AGREED | Vael v1.3 §8, §21, §30 |
| No glowing or emissive eyes to aid visibility, no required white or silver hair, and no universal black armor or dark robes | AGREED | Vael v1.3 §13, §17, §27 |
| Universal (proposed): biological appearance is separate from observed lighting, and the creator provides neutral lighting | PRELIMINARY | Vael v1.3 §6 |
| Vael pigmentation families: charcoal, slate, grays, blue-gray, muted violet, ash and desaturated brown, with broad undertones | PRELIMINARY | Vael v1.3 §1–3 |
| Vael cultural pillars: Depth, Flow, Craft, Light, Exchange, with civilization designed first around underground practicalities | PRELIMINARY | Vael v1.3 §22–23 |
| Vael presentation presets: Deep-City Practical, Surface Traveler, Artisan/Industrial, Merchant, Formal Urban, Military, Ceremonial, Foreign-Raised | PRELIMINARY | Vael v1.3 §31 |
| Vael sun response (tanning, burning, pigment change) | OPEN | Vael v1.3 §9 |
| Vael hair, iris and pigmentation frequencies | OPEN | Vael v1.3 §10, §13, §16, Elf Comparative Review |

| Decision | Status | Source |
| --- | --- | --- |
| Presentation presets never alter anatomy or inherited pigmentation, every character preset is reproducible with player tools, and there's no preset-exclusive anatomy | AGREED | Vael v1.4 §1, §5–6 |
| A Surface-Raised Vael (subtle ears, brownish skin, dark hair, ordinary clothing) must still read as Vael | AGREED | Vael v1.4 §4, §20 |
| Biological randomization follows ancestry, presentation randomization follows culture, and there are no rigid trait packages | AGREED | Vael v1.4 §12–13 |
| Randomization must not converge on one Dark Elf template (charcoal skin, white hair, violet or glowing eyes, lean, severe, dark clothing) | AGREED | Vael v1.4 §14 |
| Vael character presets: Deep-City Engineer, Surface Merchant, Broad Craftworker, Lean Wayfinder, Heavyset Trader, Surface-Raised Vael, Deep-City Elder, Cross-Cultural Traveler | PRELIMINARY | Vael v1.4 §2 |
| Three-elf face tendencies: Fenn open orbits and compact face, Aelari facial verticality, Vael midface integration and compact vertical distribution | PRELIMINARY | Vael v1.4 §19 |
| Universal (proposed): Subtle, Diverse and Extreme randomization strengths, with relationship-aware and lockable groups | PRELIMINARY | Vael v1.4 §9–11 |
| Deterministic, reproducible generation (required for co-op consistency) | PRELIMINARY | Vael v1.4 §16 |

| Decision | Status | Source |
| --- | --- | --- |
| Vael first pass (v1.0–v1.5) is complete, with six races done: Marchfolk, Skarn, Sagekin, Fenn, Aelari and Vael | AGREED | Vael v1.5 §31 |
| Shared ancestry doesn't automatically require one shared skeleton | AGREED | Vael v1.5 §25 |
| Movement comes from anatomy and physical state, with sneaking, grace, menace, aggression and underground expertise never biological | AGREED | Vael v1.5 §5 |
| Underground spaces grant no automatic Vael access or movement advantages, and any race-specific access restriction must be deliberate | AGREED | Vael v1.5 §19–20 |
| Detailed Halvren anatomy waits for the Elf Comparative Review, and Halvren are never pointed-ear humans, a 50/50 average or short-eared Aelari | AGREED | Vael v1.5 §34 |
| Universal (proposed): the character creator offers neutral, warm, cool, brighter and lower lighting for inspection without changing stored data | PRELIMINARY | Vael v1.5 §16 |
| Vael technical foundation (MetaHuman, shared elven hierarchy, race skeletons, retargeting, hybrid) and elf skeleton architecture | OPEN | Vael v1.5 §1, §25 |
| Vael ocular low-light mechanism, gameplay low-light vision and daylight sensitivity | OPEN | Vael v1.5 §9, §30 |
| Whether Vael torso depth and joint presence affect balance, turning, stride or weight transfer | OPEN | Vael v1.5 §6 |
| Networked appearance sync for the eventual richer appearance data (co-op) | OPEN | Vael v1.5 §30 |

Elf Comparative Review v1.0

| Decision | Status | Source |
| --- | --- | --- |
| Fenn, Aelari and Vael share a distinct, non-human elven skeletal family (A), which doesn't imply one technical skeleton | AGREED | Elf Review Part 1 §2 |
| Elven gracility is shared (A), and gracile never means fragile, weaker, less durable or thin | AGREED | Elf Review Part 1 §3 |
| Height and long necks aren't elven traits, and body composition isn't ancestry | AGREED | Elf Review Part 1 §5, §12, §23 |
| Broad frames are valid for all elves, within each population's own range | AGREED | Elf Review Part 1 §24 |
| Provisional shared-elven skeletal signal: gracility, torso, shoulders, pelvis foundation, elongated limbs, joints, hands and feet, taken together | PRELIMINARY | Elf Review Part 1 §25 |
| Population divergence: Fenn extremity-emphasized, Aelari vertically distributed, Vael deeper with compact continuity (B, C, D) | PRELIMINARY | Elf Review Part 1 §4, §7–22, §26 |
| Exact shared pelvic shape, per-race pelvis detail, and elf technical architecture (E) | OPEN | Elf Review Part 1 §13–14, §30 |

| Decision | Status | Source |
| --- | --- | --- |
| Comparative anatomical terms name the comparison population or the reference relationship being measured, keeping absolute versus proportional, width versus depth, projection versus sweep, skeletal versus muscular mass, orbital size versus visible opening, and body size versus composition distinct. This applies to all race specs and reviews (strengthened in the Part 2 clarification) | AGREED | Elf Review Part 1, waist clarification |
| Waist transition: Aelari have the greatest vertical torso and waist continuity, Fenn a gradual transition within a compact torso (not longer than Aelari), and Vael a deeper torso with compact torso-pelvis continuity (depth isn't waist length) | PRELIMINARY | Elf Review Part 1, waist clarification |

| Decision | Status | Source |
| --- | --- | --- |
| Shared non-human elven craniofacial and external-ear ancestry (A), with no universal elf face and no single "Elf Head" with superficial morphs unless prototyping proves it | AGREED | Elf Review Part 2 §1–3, §20 |
| Ear distributions overlap across the three elves, no single ear identifies ancestry, and every elf stays recognizable with minimal or hidden ears | AGREED | Elf Review Part 2 §26–27 |
| Elves visibly age, with no permanent youth unless lore establishes a mechanism | AGREED | Elf Review Part 2 §30 |
| No elven race is biologically required to be beautiful, and resting anatomy never encodes startled, aloof or sinister personality | AGREED | Elf Review Part 2 §32, §36 |
| Not universally elven: tall, large or narrow eyes, small or narrow noses, high or hollow cheeks, pointed chins, narrow faces, long necks, pale skin, light or straight hair, blue or glowing eyes, long ears, beauty, graceful expression | AGREED | Elf Review Part 2 §38 |
| Provisional shared elven facial signal (cranium, orbits, midface, gracile construction, diverse mandibles, ear ancestry as a system) | PRELIMINARY | Elf Review Part 2 §37 |
| Craniofacial, orbital, jaw and ear divergence for Fenn (B), Aelari (C) and Vael (D), with round pupils as the conservative baseline | PRELIMINARY | Elf Review Part 2 §4–14, §18, §23–25 |
| Exact ancestral midface, ear shape and ocular physiology, nasal and lip population frequencies, pupil shape, ear mobility, and elven lifespan and aging rates (E) | OPEN | Elf Review Part 2 §9, §12, §15, §17–18, §22, §29, §31 |
| Vael low-light adaptation as a Vael-only candidate (D + E), not given to Fenn or Aelari, with gameplay open | OPEN | Elf Review Part 2 §19 |

| Decision | Status | Source |
| --- | --- | --- |
| Fenn trend toward more open visible eye presentation than Aelari and Vael, and greater lateral ear projection from the skull than Aelari and Vael. Vael trend toward more mandibular presence than Fenn and Aelari. All with overlap | PRELIMINARY | Elf Review Part 2 clarification |
| Fenn-versus-Aelari mandibular ranking (not established, distributions may overlap heavily) | OPEN | Elf Review Part 2 clarification |

| Decision | Status | Source |
| --- | --- | --- |
| No universal modern elven complexion, hair color or eye color, and no elf population is the pigmentation baseline. Shared elven identity is anatomical, not cosmetic | AGREED | Elf Review Part 3 §1, §8, §34 |
| Lighting invariance, the neutral-reference-first workflow, and the silver-versus-aging hair distinction are universal (all races where applicable) | AGREED | Elf Review Part 3 §9–10, §14 |
| Ancestral biology, population adaptation, individual exposure and culture stay four separate concepts, and culture and birthplace never rewrite ancestry | AGREED | Elf Review Part 3 §19, §23 |
| Facial hair isn't biologically prohibited for elves, and clean-shaven isn't universally elven | AGREED | Elf Review Part 3 §15 |
| Elf populations overlap on individual traits, no cosmetic trait perfectly classifies race, and there are no rigid phenotype packages | AGREED | Elf Review Part 3 §25–26 |
| Skin directions: Fenn the full approved range from fair and light through olive, copper, bronze and rich deeper brown, cool to warm undertones (B, corrected), Aelari fair through deeper brown (C), Vael gray, blue-gray, muted violet and desaturated brown (D) | PRELIMINARY | Elf Review Part 3 §5–7 |
| Pigmentation, undertone, hair texture, hair color and iris frequencies, ancestral elven pigmentation, skin physiology and geographic subpopulations (E) | OPEN | Elf Review Part 3 §2–3, §12–13, §17, §27, §35 |
| Which Fenn traits are ancestry, adaptation, learned skill or gameplay abstraction (including sneak and swim), and Vael bright-light response | OPEN | Elf Review Part 3 §20, §22, §35 |

| Decision | Status | Source |
| --- | --- | --- |
| Fenn and Aelari may substantially overlap in valid skin values and undertones, and Vael may approach them too. Distinction comes from frequencies, combinations and subpopulations, with no color reserved for one race just to differentiate | AGREED | Elf Review Part 3 clarification §2–3 |
| Validity (can it occur) and frequency (how often in this population) are separate, a shared valid trait needn't be equally common, and pigmentation is judged on large generated populations, never one preset | AGREED | Elf Review Part 3 clarification §4–5 |
| The biology review doesn't validate or remove prototype stats (Aelari Wisdom, Fenn sneak and swim). They stay untouched until the Race to Biology to Gameplay Attributes Review | AGREED | Elf Review Part 3 clarification §6–7, §10 |
| What the Fenn sneak and swim traits and the Aelari Wisdom value represent (biology, adaptation, training, hybrid or abstraction), and final racial attributes | OPEN | Elf Review Part 3 clarification §8–9 |

| Decision | Status | Source |
| --- | --- | --- |
| Elf Comparative Review v1.0 is complete (Parts 1–4 plus four clarifications, including the final consistency clarification) and is the comparative biological authority for Fenn, Aelari and Vael, with race specs authoritative where not clarified or superseded | AGREED | Elf Review Part 4 §36 |
| Movement has five distinct layers (anatomical biomechanics, learned movement, cultural and personal body language, emotional state). Racial locomotion encodes neither personality nor culture, and there's no universal elf animation style | AGREED | Elf Review Part 4 §4–8, §31 |
| Biomechanical differences never automatically grant gameplay advantages (speed, jump, stealth, balance, dodge, stamina, attack speed) | AGREED | Elf Review Part 4 §10 |
| Related but distinct: overlap between individual elves isn't failure, and weak readability is fixed by checking the anatomy is implemented correctly, not by exaggerating ears, eyes, color, angularity, height or jaw | AGREED | Elf Review Part 4 §32–34 |
| Halvren aren't pointed-ear humans, 50/50 averages, slider midpoints or one fixed hybrid. Mixed ancestry needs explicit inheritance rules, and Halvren waits for its own instruction | AGREED | Elf Review Part 4, next phase |
| Final shared-ancestry matrix (skeletal family, gracility, height, torso, limbs, hands and feet, craniofacial, ears, pigmentation, hair, eyes, aging, movement) | PRELIMINARY | Elf Review Part 4 §18–31 |
| Final elven-biology unresolved register (29 items, including lifespan, skeleton architecture, MetaHuman viability, collision and reach, racial attributes and mixed-ancestry inheritance), never silently resolved during implementation | OPEN | Elf Review Part 4 §2, §11–17, §35 |

| Decision | Status | Source |
| --- | --- | --- |
| World compatibility is validated against approved target anatomy for every playable race, not just what the prototype creator can reach. Prototype limits never silently become world constraints, and approved extremes are tested before world metrics lock | AGREED | Elf Review final clarification §6 |
| Aelari approved height (168–221 cm) stays authoritative over the prototype (1.02 scale, about ±7.5%), a known gap with no scale or height-system change now. Maximum-height Aelari (about 221 cm) join permanent validation when prototyping is authorized | AGREED | Elf Review final clarification §4–5 |
| Skeletal gracility ordering on average: Fenn (most gracile), then Aelari, then Vael (most structural presence), with overlap, never fixed presets, and never implying weakness or frailty | PRELIMINARY | Elf Review final clarification §1 |
| Aelari have greater average neck length and proportional neck contribution than Fenn and Vael. Ear lateral projection is greatest in Fenn and lower in Aelari than Fenn, with Vael overlapping and no strict Aelari-Vael ranking | PRELIMINARY | Elf Review final clarification §2–3 |

Marchfolk v1.0 (recovered)

| Decision | Status | Source |
| --- | --- | --- |
| Marchfolk are the baseline human reference for comparing other races, but not the default anatomy for every humanoid race, and they represent the breadth of human diversity, not one idealized body | AGREED | Marchfolk v1.0 §1–2 |
| Marchfolk height envelope 147 / 173 / 203 cm (approved first pass), coming from proportions, not uniform scaling, with no hard sex-specific height limit | AGREED | Marchfolk v1.0 §4–5 |
| Individually valid controls can still make an invalid body, so customization needs relationship-aware constraints or validation. Visible mass comes from height, frame, muscle, fat and regions, never one scale value | AGREED | Marchfolk v1.0 §9–11 |
| Frontier-settler reputation (ruggedness, labor, toughness, weathering, scars, muscularity) isn't Marchfolk anatomy | AGREED | Marchfolk v1.0 §14 |
| Marchfolk v1.0 is complete, recovered as the foundation of v1.1–v1.4 without replacing them. v1.5 is still awaited | AGREED | Marchfolk v1.0 §19 |

Marchfolk v1.5 (recovered)

| Decision | Status | Source |
| --- | --- | --- |
| Marchfolk first-pass character design (v1.0–v1.5) is complete and is the primary human biological reference, with all six first-pass races (Marchfolk, Skarn, Sagekin, Fenn, Aelari, Vael) now having complete sources | AGREED | Marchfolk v1.5 §21 |
| One unified conceptual appearance record for presets, advanced customization, random generation and NPCs, with schema and version tracking and migration. Presets must survive Preset, Advanced, Edit, Save, Reload unchanged | AGREED | Marchfolk v1.5 §9, §11–12 |
| Validation runs in three stages (anatomy, facial and individual identity, gameplay and world), across min, reference and max height and all frames, with combined extremes tested | AGREED | Marchfolk v1.5 §1–6 |
| Marchfolk camera, collision, reach, hit detection, height-dependent camera placement and mounts (never set automatically by visual scale) | OPEN | Marchfolk v1.5 §17–18 |
| Marchfolk consistency findings 7–10 before Halvren (human color families, ear baseline, lifespan, which humans), now resolved enough to begin Halvren by pre-inheritance Part 2, with the remaining subtopics tracked there | OPEN | Marchfolk tab, consistency review |

Marchfolk consistency resolution, Part 1 (findings 1–6 resolved)

| Decision | Status | Source |
| --- | --- | --- |
| Athletic is exclusively a physical-composition preset and never automatically changes skeletal-frame parameters. Marchfolk have three skeletal-frame starting categories plus independent composition presets (v1.1 and v1.4 text corrected) | AGREED | Consistency resolution Part 1 §1 |
| Body-fat amount and body-fat distribution are separate parameters, Basic Mode conceptually supports both, and distribution never substitutes for amount | AGREED | Consistency resolution Part 1 §2 |
| "Thickness" isn't used alone: specs distinguish skeletal breadth, muscle, adipose and total circumference. Hand and foot size distinguish absolute from proportional, skeletal from soft tissue, and length, breadth and depth | AGREED | Consistency resolution Part 1 §3–4 |
| "Frame" (Skeletal Frame) is the continuous anatomical layer, and "Frame Preset" (Narrow, Balanced, Broad) is an editable starting configuration, never an immutable biological caste | AGREED | Consistency resolution Part 1 §5 |
| Marchfolk are the primary Human Reference Population, and about 173 cm is the Marchfolk Reference Height. "Baseline" isn't used for both | AGREED | Consistency resolution Part 1 §6 |
| Character Architecture Layers (Anatomy, Skeletal Frame, Physical Composition, Personal Presentation) are distinct from Skin Appearance Layers (Natural, Environmental, Applied or Acquired). Inheritance names the architecture layer, and skin layers aren't inheritance categories | AGREED | Consistency resolution Part 1 §7 |
| Age has three distinct concepts: chronological age, apparent biological age and age presentation | AGREED | Consistency resolution Part 1 §8 |
| Halvren inheritance must name what each inherited trait affects (anatomy, frame, composition tendencies, pigmentation, hair, ocular, ears, lifecycle). Personal presentation is never genetically inherited, and cultural inheritance is separate from biological | AGREED | Consistency resolution Part 1 §9 |

Marchfolk and Halvren pre-inheritance resolution, Part 2 (findings 7–10 resolved enough to begin Halvren)

| Decision | Status | Source |
| --- | --- | --- |
| Marchfolk pigmentation envelope: skin fair through deep brown, undertones cool to reddish, hair black through blond and auburn or red, iris brown through blue and gray. Validity isn't frequency, and Marchfolk aren't any one real-world population | AGREED | Pre-inheritance Part 2 §1–2 |
| Marchfolk have ordinary human ear architecture. Human and elven ears are different architectures, not pointiness 0% versus 100%, and mixed ears are never a linear pointiness interpolation | AGREED | Pre-inheritance Part 2 §3–4 |
| Human family is Marchfolk, Skarn and Sagekin (Human never equals Marchfolk), and elven family is Fenn, Aelari and Vael (Elf never equals one generic phenotype). Halvren are flexible mixed human and elven ancestry from any of these, which sets capability, not frequency | AGREED | Pre-inheritance Part 2 §7–10 |
| Halvren aren't fixed crossbreed sub-races, the system supports multigenerational ancestry, the phenotype is never hardcoded to 50/50, and inheritance is never slider averaging | AGREED | Pre-inheritance Part 2 §11–13 |
| Ancestry never determines culture, birthplace, language, clothing, religion, occupation, personality, social identity or community | AGREED | Pre-inheritance Part 2 §14 |
| Terms: "human ancestry" and "elven ancestry" plus specific population names. "Half" never implies an exact percentage unless warranted, and "Halvren" stays the race name. Lifecycle inheritance may be nonlinear, with no midpoint lifespan assumed | AGREED | Pre-inheritance Part 2 §6, §15 |
| Marchfolk frequencies, human and elven lifecycle numbers, Halvren lifecycle expression, genetic model, dominance, multigenerational math, combination frequencies, who counts as Halvren socially, and how ancestry shows to the player | OPEN | Pre-inheritance Part 2 §1, §5, §16 |

Halvren v1.0

| Decision | Status | Source |
| --- | --- | --- |
| No single mandatory Halvren body or face, never per-parameter averaging, never hardcoded to 50/50, and no single human-to-elf slider for the whole body | AGREED | Halvren v1.0 Part 1 §2–4, §10 |
| Inheritance is developmentally coherent: mosaic expression across domains is valid, patchwork anatomy (parts copied from separate race meshes) fails | AGREED | Halvren v1.0 Part 1 §12, §14 |
| Genealogical ancestry and phenotypic expression are distinct, genealogy is never inferred from one feature, and there are no "X% elf-looking" labels and no "Elf Percentage" slider | AGREED | Halvren v1.0 Part 1 §11, §23, §26 |
| No generic elf parent and no generic human parent: Fenn, Aelari, Vael, Marchfolk, Skarn and Sagekin ancestry each stay representable | AGREED | Halvren v1.0 Part 1 §15–18 |
| Halvren anti-stereotype rule (not universally attractive, young-looking, slim, graceful, light-skinned, conflicted, charismatic, outcast or "caught between two worlds"), and thinness never signals elven ancestry | AGREED | Halvren v1.0 Part 1 §21, §31 |
| Human and elven families are compatible enough for viable descendants, and Halvren form persistent multigenerational populations (worldbuilding rules, no genetic mechanics) | PRELIMINARY | Halvren v1.0 Part 1 §5–6 |
| Candidate soft inheritance clusters: axial skeleton, appendicular skeleton, distal anatomy, craniofacial, external ear | PRELIMINARY | Halvren v1.0 Part 1 §13 |
| Detailed inheritance by domain, lifecycle, physiology, genetic depth, ancestry UI, randomization weighting, frequencies, social definition, skeleton architecture, save schema and racial attributes | OPEN | Halvren v1.0 Part 1 §19, §32–34 |

| Decision | Status | Source |
| --- | --- | --- |
| Halvren have their own mixed-population envelope and can't systematically reproduce a pure source-race body, while individuals may still strongly resemble a source population | AGREED | Halvren v1.0 Part 2 §2, §32–33 |
| Height is never averaged and ancestry shifts probability, not validity. Extremes are never reached by uniform scaling | AGREED | Halvren v1.0 Part 2 §4–6 |
| Narrow, Balanced and Broad are frame presets, not ancestry categories, composition stays independent of ancestry with no stereotype shortcuts, and the body isn't a single human-versus-elf percentage | AGREED | Halvren v1.0 Part 2 §27–31 |
| Anatomy never converts directly to stats (Skarn Strength, Fenn Stealth, Aelari Wisdom or Magic, Sagekin Intelligence, Vael low-light), and movement follows final anatomy, not a half-elf animation style | AGREED | Halvren v1.0 Part 2 §39–40 |
| Halvren height 152 / 178 / 213 cm, now the central population envelope rather than a hard wall (revised by the consistency resolution) | PRELIMINARY | Halvren v1.0 Part 2 §3 |
| Source-population contributions (Skarn, Fenn, Aelari, Vael, Marchfolk, Sagekin), multidimensional torso, shoulder, neck, limb, joint, hand and foot inheritance with coupling, and the Halvren pelvis as a viable mixed structure, not a linear morph | PRELIMINARY | Halvren v1.0 Part 2 §7–26 |
| Detailed Halvren pelvic inheritance (needs prototypes and further anatomical design) | OPEN | Halvren v1.0 Part 2 §19 |
| RESOLVED by the consistency resolution: Skarn ancestry shifts muscular development capacity, never current muscularity | OPEN | Halvren v1.0 Part 2 §9, §29 |

| Decision | Status | Source |
| --- | --- | --- |
| A Halvren isn't a human face with pointed ears. Craniofacial inheritance is regional but coupled, never patchwork, there's no single Halvren face, and human and elven source populations stay distinct | AGREED | Halvren v1.0 Part 3 §1–6 |
| Halvren ears are genuine mixed anatomy, never a pointiness slider, with relationship-aware parameters, and ear length is never a genealogy meter | AGREED | Halvren v1.0 Part 3 §21–29 |
| Brow, orbit, external eye and ocular anatomy are separate systems, personality is never encoded in eye anatomy, and no automatic glowing or magical eyes, night vision or enhanced hearing | AGREED | Halvren v1.0 Part 3 §12–14, §32–35 |
| Hidden-ear, anti-beauty and anti-generic-half-elf tests (hidden-ear and anti-generic-half-elf are permanent validation concepts), and Halvren visibly age | AGREED | Halvren v1.0 Part 3 §37, §39, §43–44 |
| Source-population facial and ear tendencies for Halvren (Fenn, Aelari, Vael, Skarn, Sagekin, Marchfolk), and face presets | PRELIMINARY | Halvren v1.0 Part 3 §7–10, §26–28, §38 |
| Halvren ear mobility, hearing physiology, ocular biology (including Vael-derived low-light), facial-hair distributions, aging rate and face and ear technical architecture | OPEN | Halvren v1.0 Part 3 §31–37, §45 |

| Decision | Status | Source |
| --- | --- | --- |
| Halvren pigmentation is inherited biological expression across separate dimensions, never RGB averaging, and there's no default Halvren complexion | AGREED | Halvren v1.0 Part 4 §1–2, §8, §11 |
| Ancestry may be visually latent (phenotype isn't a genealogy report), and inheritance supports non-midpoint multigenerational expression | AGREED | Halvren v1.0 Part 4 §9–10 |
| Ancestry controls never become color locks (more Vael doesn't mean gray, more Aelari doesn't mean pale, more Fenn doesn't mean bronze), and players never edit genes | AGREED | Halvren v1.0 Part 4 §37–38 |
| Hair biology is separate from presentation, hair color, texture and iris are never averaged, and tattoos, cosmetics and scars are never inherited | AGREED | Halvren v1.0 Part 4 §3, §17–28, §33–34 |
| Pigmentation validation: population sampling, Vael, Fenn, Aelari and human mix stress tests, neutralization, hair, lighting, anti-exoticism and anti-midpoint tests | AGREED | Halvren v1.0 Part 4 §41–50 |
| Sibling variation and familial resemblance without cloning as future inheritance requirements | PRELIMINARY | Halvren v1.0 Part 4 §51–52 |
| Halvren pigmentation, hair and iris frequencies and probabilities, dominance and polygenic rules, facial hair distributions, pupil morphology, geographic subpopulations, family-generation system, and shader, hair and eye technical architecture | OPEN | Halvren v1.0 Part 4 §8, §15, §21, §24, §28, §30, §36, §51, §55 |

| Decision | Status | Source |
| --- | --- | --- |
| Halvren v1.0 first-pass biological foundation is complete (Parts 1–5), with seven races through first pass (Marchfolk, Skarn, Sagekin, Fenn, Aelari, Vael, Halvren) | AGREED | Halvren v1.0 Part 5 §68 |
| No mandatory Halvren culture. Biological mixed ancestry is separate from Halvren social identity, ancestry never assigns personality, and "caught between two worlds" is never required | AGREED | Halvren v1.0 Part 5 §4–8 |
| No lifespan percentage slider, lifecycle inheritance may be nonlinear, and Halvren visibly age | AGREED | Halvren v1.0 Part 5 §9–12 |
| Presets never imply genealogy, and biological and presentation randomization stay separate. One genealogy allows multiple valid phenotypes, and appearance editing never silently rewrites genealogy | AGREED | Halvren v1.0 Part 5 §15–21, §60 |
| Permanent Halvren failure and success conditions, and no automatic averaging of human and elven racial bonuses or percentage-inherited prototype stats | AGREED | Halvren v1.0 Part 5 §57, §64–65 |
| Halvren are biologically viable and have descendants (first-pass setting assumption), and the name "Halvren" never literally means 50/50 | PRELIMINARY | Halvren v1.0 Part 5 §2–3 |
| Halvren preset targets A–M and permanent validation characters HV-FAMILY-01, HV-FAMILY-02 and HV-01 to HV-48 | PRELIMINARY | Halvren v1.0 Part 5 §14, §23–45 |
| Halvren v1.0 keep-open list (§67): lifecycle, genetic model, genealogy representation and UI, correlations, frequencies, subpopulations, social definition and etymology, pelvis, ears, hearing, ocular, pupils, hair and pigment frequencies, technical architecture, cameras, collision, reach, hit detection, mounts, attributes, class restrictions, networking | OPEN | Halvren v1.0 Part 5 §67 |
| Halvren v1.0 consistency review findings: Skarn muscle potential, unnamed comparison targets, preset names and population-influence controls against genealogy, which envelope applies to mixed characters of another social identity, height-envelope edges (147 cm Marchfolk floor, Skarn and Aelari crowding the 213 cm cap), and missing source prerequisites | OPEN | Halvren tab, consistency review |

Halvren v1.0 consistency resolution (pre-v1.1 clarification)

| Decision | Status | Source |
| --- | --- | --- |
| Muscular development capacity is separate from current muscularity. Skarn ancestry may shift capacity, never current build | AGREED | Halvren resolution §1 |
| Normalized comparative terms (Skarn thoracic depth and absolute hand-foot size against Marchfolk; Fenn gracility and shallower thorax; Aelari height and proportional neck; Sagekin linearity and ribcage breadth against Marchfolk), and the human family isn't universally "robust" | AGREED | Halvren resolution §2–3 |
| "X-Influenced Halvren" are internal validation labels only, and player-facing presets describe appearance, never genealogy | AGREED | Halvren resolution §4 |
| Genealogical ancestry, ancestry-derived constraints and phenotypic expression are distinct. Editing phenotype never rewrites genealogy, and genealogy controls aren't appearance sliders | AGREED | Halvren resolution §5 |
| Biological ancestry, playable biological classification (which ruleset validates the character) and social or cultural identity are distinct, and social identity never erases biological ancestry | AGREED | Halvren resolution §6–8 |
| Halvren height tails beyond the central envelope are allowed, never hard-clipped, compressed, uniformly scaled or averaged, and the mixed developmental system still governs validity | AGREED | Halvren resolution §10–13 |
| Source-first dependency rule (permanent): mixed-ancestry design never invents source biology. Stop, return to the source population, define and validate it, then resume. Missing pelvis or sex-related anatomy stops only the dependent section | AGREED | Halvren resolution §15–16 |
| HV-49 lower-tail and HV-50 upper-tail validation characters, with HV-11 and HV-12 renamed central boundaries | PRELIMINARY | Halvren resolution §14 |
| Whether a player may pick a non-Halvren biological ruleset while specifying mixed genealogy | OPEN | Halvren resolution §8 |
| Future "race" terminology review (species or family, population or ancestry, playable lineage, culture, social identity), with no renaming now | OPEN | Halvren resolution §9 |
| Exact Halvren height-tail limits and frequencies | OPEN | Halvren resolution §12 |

Durrim v1.0

| Decision | Status | Source |
| --- | --- | --- |
| Durrim are a genuinely distinct compact humanoid population, never scaled-down humans, compressed skeletons or short height plus maximum muscle | AGREED | Durrim v1.0 Part 1 §1–3, §7 |
| Durrim adults are never visually infantilized (head-body, face, hands, shoulders, pelvis, limbs, movement) | AGREED | Durrim v1.0 Part 1 §8, §48 |
| Durrim skeletal structural presence is never represented through muscle alone, composition varies fully, and Durrim aren't universally stocky in composition | AGREED | Durrim v1.0 Part 1 §27, §31–32 |
| The short playable races must not be three scales of one humanoid body. Durrim direction is compact structural power and high skeletal presence relative to stature | AGREED | Durrim v1.0 Part 1 §43 |
| Culture separation (mining, smithing, mountains, clans, drinking, stubbornness, honor, greed, craft, warrior culture), beards not biological requirements, and no automatic gameplay bonuses from compact anatomy | AGREED | Durrim v1.0 Part 1 §38–41 |
| Durrim height 122 / 137 / 152 cm (provisional first-pass range), with intentional overlap with short Marchfolk | PRELIMINARY | Durrim v1.0 Part 1 §4–5 |
| Durrim skeletal tendencies: greater thoracic breadth and depth and lower limb contribution than equivalent-height Marchfolk, substantial long bones and joints relative to length and stature, substantial hands and feet, low center of mass. The legacy mass multiplier is replaced by "unusually high body volume and structural mass relative to stature" | PRELIMINARY | Durrim v1.0 Part 1 §11–25, §36 |
| Durrim pelvic morphology, sex-related anatomy, facial-hair biology and technical foundation | OPEN | Durrim v1.0 Part 1 §15, §37–38, §55 |
| Legacy Durrim breath (longer) and swimming (poor) traits, kept as prototype gameplay pending review | OPEN | Durrim v1.0 Part 1 §42 |

| Decision | Status | Source |
| --- | --- | --- |
| No Durrim body part is shortened, widened or enlarged in isolation, every parameter distinguishes absolute, height-relative and adjacent-relative dimensions, and combined-proportion validity is mandatory | AGREED | Durrim v1.0 Part 2 §1–3, §50 |
| Frame, height and composition are independent for Durrim, Balanced isn't the canonical body, and Narrow never collapses into short Marchfolk | AGREED | Durrim v1.0 Part 2 §36–40 |
| Low-muscle and lean Durrim stay recognizably Durrim, there's no artificial body-fat minimum, and heavy Durrim never become the comedic round dwarf | AGREED | Durrim v1.0 Part 2 §42–47 |
| Substantial Durrim hands never reduce dexterity or grant crafting skill, and occupation never sets inherited hand anatomy | AGREED | Durrim v1.0 Part 2 §24–25 |
| Durrim proportion tendencies: greater torso and lower limb contribution than equivalent-height Marchfolk, a compact torso, independent but coupled limb segments, multidimensional hands and feet, a provisional greater palm share | PRELIMINARY | Durrim v1.0 Part 2 §4–35 |
| RESOLVED: the Durrim, Marchfolk and Sagekin equal-height test runs at about 152 cm as a Cross-Population Equal-Height Boundary Test (a 150 cm Sagekin was below the approved range) | OPEN | Durrim v1.0 Part 2 §54 |

| Decision | Status | Source |
| --- | --- | --- |
| A Durrim must still look Durrim when bald, clean-shaven, with neutral expression and ears hidden, and Durrim faces always read as adult | AGREED | Durrim v1.0 Part 3 §1–2 |
| Large noses, heavy brows and square or heavy jaws aren't Durrim requirements, and skeleton stays separate from muscle, fat and beard | AGREED | Durrim v1.0 Part 3 §9, §16–24 |
| A clean-shaven Durrim is fully valid and unmistakably adult. Beard length and style are presentation, and no beard tradition is inferred from biology | AGREED | Durrim v1.0 Part 3 §41–42, §49 |
| Durrim ears are broadly humanoid and non-elven, never pointed, with no comic projecting-ear shorthand | AGREED | Durrim v1.0 Part 3 §29–33 |
| Durrim craniofacial tendencies: greater cranial breadth relative to height than Marchfolk, compact vertical face relative to Marchfolk, substantial midface and mandibular presence, soft face-frame correlation | PRELIMINARY | Durrim v1.0 Part 3 §3–7, §15, §21, §26 |
| Durrim facial-hair sex-related distributions, body-hair biology, ear-size distributions, hair texture frequencies and face technical architecture | OPEN | Durrim v1.0 Part 3 §32, §36, §43, §45, §63 |

| Decision | Status | Source |
| --- | --- | --- |
| Universal Facial Customization Architecture is deferred until all 13 first-pass races are complete, and race specs define craniofacial identity and relationships, not player-facing controls, until then | AGREED | Durrim Part 3 clarification 1 §1–2, §22–23 |
| Durrim facial identity is a system (compact adult cranium, integrated midface, craniofacial depth and presence, mandibular support, head-neck-body integration). Nose, beard and ears are never primary identifiers, and readability never depends on one feature | AGREED | Durrim Part 3 clarification 1 §3, §13–17 |
| Universal principle: structural anatomy, biological soft tissue, surface appearance, presentation, expression and observed lighting appearance are separate concepts | AGREED | Durrim Part 3 clarification 2 §25 |
| Craniofacial depth is validated through multiple regional relationships (brow and orbit, orbit, zygoma, midface and maxilla, mandible) with nose, chin, width and verticality exclusions, absolute versus proportional depth, and no numerical thresholds before prototype calibration | AGREED | Durrim Part 3 clarification 3 |
| Racial craniofacial structure is never faked mainly through normal maps, displacement, ambient occlusion, baked shadow or skin materials, and large-scale depth lives in geometry or deformation | AGREED | Durrim Part 3 clarification 2 §18 |
| Durrim trend toward greater craniofacial skeletal depth relative to facial vertical height than equivalent Marchfolk (multiregional, not nasal or chin projection), plus head-neck integration as a major identifier. Diagnostic characters DU-FACE-01 to 11 and DU-DEPTH-01 to 03 | PRELIMINARY | Durrim Part 3 clarifications 1–3 |
| Durrim craniofacial depth numerical ranges (after prototype calibration) | OPEN | Durrim Part 3 clarification 3 §36–37 |
| RESOLVED: facial layer letters renamed to Facial Diagnostic Domains, and Marchfolk v1.2 and Skarn facial-editor wording classed as approved first-pass functional requirements with provisional control organization | OPEN | Durrim tab notes |

| Decision | Status | Source |
| --- | --- | --- |
| Facial diagnostic terminology: FD-STRUCT, FD-SOFT, FD-SURF, FD-HAIR, FD-PRES and FD-OBS replace the A–F facial layers, and a Facial Diagnostic Domain is never called "Layer A" and so on | AGREED | Durrim consistency-resolution patch §1 |
| Existing facial editor specs: Marchfolk's three-level, seven-region organization and Skarn's reference to it are approved first-pass functional requirements with provisional control organization, and the final universal hierarchy is deferred until all 13 races are complete | AGREED | Durrim consistency-resolution patch §2–5 |
| Durrim, Marchfolk and Sagekin equal-height test at about 152 cm, classified as a Cross-Population Equal-Height Boundary Test | AGREED | Durrim consistency-resolution patch §6–9 |
| General rule: a cross-population equal-height test uses a stature inside every included population's approved range, and if none exists, another normalization is used | AGREED | Durrim consistency-resolution patch §11 |

| Decision | Status | Source |
| --- | --- | --- |
| Soot, stone dust and mining grime are never Durrim racial features, and environmental appearance comes from activity and location for every race | AGREED | Durrim v1.0 Part 4 §40–41, §57 |
| Durrim pigmentation is independent of the skeleton, ruddiness is never required, red hair is neither required nor privileged, and iris color isn't a racial identifier | AGREED | Durrim v1.0 Part 4 §3–7, §15, §22 |
| Durrim visibly age, aging affects more than wrinkles and hair color, and age surface changes are never mistaken for structural depth | AGREED | Durrim v1.0 Part 4 §29–39 |
| Scars and injuries are acquired, tattoos and cosmetics are presentation (never sex-locked by default), and presentation layers over biological pigmentation | AGREED | Durrim v1.0 Part 4 §43–47 |
| Durrim first-pass skin, hair and iris envelopes (broad, frequencies to be set deliberately) and no hidden pigmentation-phenotype packages | PRELIMINARY | Durrim v1.0 Part 4 §4, §15, §22, §61 |
| Durrim skin thickness or toughness, environmental adaptation, sun response, specialized low-light vision, lifecycle, heterochromia frequency and appearance technical architecture | OPEN | Durrim v1.0 Part 4 §10–12, §25, §28, §30, §64 |

Cross-race

| Decision | Status | Source |
| --- | --- | --- |
| **Race-specific facial-control organization status:** any race-specific first-pass spec that proposes facial editing levels, regions, control groups, slider organization or creator-facing hierarchy before all 13 first-pass races are complete is an approved functional requirement with provisional control organization, unless explicitly stated otherwise. This applies retroactively and prospectively to Marchfolk, Skarn, Sagekin, Fenn, Aelari, Vael, Halvren where applicable, Durrim and all remaining races. Craniofacial anatomy, population tendencies, valid variation, anatomical relationships, ear biology, facial identity, validation, required customization capability and preset and randomization requirements stay approved. Existing sections are kept as input to the Universal Facial Customization Architecture Review, which is decided only after all 13 races complete first pass, and no race is reopened for this clarification | AGREED | Facial-control classification (all races) |

Durrim v1.0 Part 5 and final review

| Decision | Status | Source |
| --- | --- | --- |
| **Durrim Character Design v1.0 FIRST-PASS COMPLETE** (approved first-pass race spec; open questions, gameplay, technical architecture and UE5 implementation not resolved or authorized) | AGREED | Durrim Part 5 §86–88 |
| Movement emerges from anatomy; anatomical movement constraints stay separate from cultural or personal body language; no stomping, waddling, permanent crouch or child locomotion | AGREED | Durrim Part 5 §1–4, §76 |
| Canonical weapon dimensions stay independent of the wielder; no scaled weapons, armor, gloves, helmets or items; armor fits Durrim anatomy and its variation | AGREED | Durrim Part 5 §35–53 |
| Retargeting adapts animation to approved anatomy, never the reverse | AGREED | Durrim Part 5 §64 |
| Anatomical, interaction, combat and camera-targeting reach stay separate concepts | AGREED | Durrim Part 5 §32, §37 |
| Final first-pass Durrim identity statement and "What Durrim are NOT" list | AGREED | Durrim Part 5 §82–83 |
| Lower center of mass as an emergent biomechanical consequence, with no automatic gameplay effect | PRELIMINARY | Durrim Part 5 §5 |
| Swimming and breath traits: gameplay traits subject to later review, never justified by invented biology | OPEN | Durrim Part 5 §24–25 |
| Movement speed, sprint, jump and climbing performance; racial size gameplay consequences; collision, hitboxes and combat reach | OPEN | Durrim Part 5 §9–16, §58–60 |
| Animation architecture, IK solution, equipment-fitting implementation, mount compatibility | OPEN | Durrim Part 5 §57, §61–63 |
| Furniture strategy (shared, adjustable, population-specific or improvised) and dialogue framing and eye-line system | OPEN | Durrim Part 5 §27, §55–56 |
| Anatomy-based equipment practicality or restrictions (large two-handed weapons, bows, shields) and the beard-physics and beard-armor clipping solution | OPEN | Durrim Part 5 §38–41, §50 |
| NPC visual LOD strategy (only if later performance architecture requires it) | OPEN | Durrim Part 5 §81 |

Durrim housekeeping patch

| Decision | Status | Source |
| --- | --- | --- |
| Part 5 header says "the next race" instead of Pipkin; the Durrim, Pipkin and Cogling Short-Race Comparative Anatomy Review stays approved | AGREED | Durrim housekeeping patch |
| Next first-pass race in roster order is **Grask — Troll** (not started) | AGREED | Durrim housekeeping patch |
| The Gorrund dialogue-framing mention is a validation reminder only; Gorrund height, scale, proportions and structure are set in Gorrund's own first pass | AGREED | Durrim housekeeping patch |
| "Deep lungs from the mines" is PROTOTYPE / NON-AUTHORITATIVE; the breath trait stays under gameplay review with no invented mechanism or mining justification, and player text is rewritten if it survives | AGREED | Durrim housekeeping patch |

Grask v1.0 Part 1

| Decision | Status | Source |
| --- | --- | --- |
| Grask are a distinct non-human humanoid population defined by rangy skeletal architecture, high limb contribution and substantial reach; not enlarged humans, Skarn with troll faces or monster rigs | AGREED | Grask Part 1 §1–2, §6, §53 |
| Upright plantigrade bipeds; no permanent hunch; no knuckle-walking; digitigrade legs need explicit reopening | AGREED | Grask Part 1 §15, §32, §58–59 |
| Height variation is anatomical, never uniform scaling; minimum-height Grask read as adults | AGREED | Grask Part 1 §4–5 |
| Grask stay identifiable with the head neutralized; body identity never depends on a troll face | AGREED | Grask Part 1 §50, §60 |
| Culture, intelligence and fantasy-troll traits are never inferred from biology | AGREED | Grask Part 1 §51–52 |
| Grask aquatic specialization NOT ESTABLISHED; breath 2× and faster swimming are gameplay traits subject to later review, with no invented biology; prototype whole-body scale values are non-authoritative placeholders | AGREED | Grask Part 1 §54–56, §80 |
| Provisional adult height 198–239 cm, reference about 218 cm (first-pass range, subject to cross-race validation) | PRELIMINARY | Grask Part 1 §3 |
| Lower torso contribution, greater leg contribution, long arms, substantial arm span and possible proportional lower-leg and forearm emphasis (Part 2 validation) | PRELIMINARY | Grask Part 1 §8, §18–26 |
| Moderate thoracic breadth with meaningful depth; moderate-to-long neck relative to Durrim and Skarn; shoulders large in absolute terms but less broad relative to height than Skarn | PRELIMINARY | Grask Part 1 §9–14 |
| Exact pelvic morphology and shoulder morphology | OPEN | Grask Part 1 §12, §16 |
| Grask muscular-development capacity; sex-related anatomy and dimorphism | OPEN | Grask Part 1 §40, §46–47 |
| Hand and foot digit count and digital anatomy (to confirm in Part 2) | OPEN | Grask Part 1 §33 |
| Gameplay consequences of Grask center of mass, reach and stature; collision; technical architecture | OPEN | Grask Part 1 §17, §27, §76–79 |
| Whether the Grask overlap and equal-height tests should also name Fenn, Vael and Halvren (all overlap 198 cm and up) | OPEN | Grask Part 1 audit |

Grask Part 1 comparative anatomy clarification

| Decision | Status | Source |
| --- | --- | --- |
| **Grask overlap framework:** Grask stature overlaps Marchfolk, Skarn, Sagekin, Fenn, Aelari, Vael and Halvren configurations where biologically valid; height alone never determines Grask readability (resolves the OPEN overlap-list row above) | AGREED | Grask Part 1 clarification §1–2 |
| **Grask arm-length direction:** greater arm length and arm span relative to total standing height than Marchfolk and Skarn reference anatomy; long-arm identity isn't just an artifact of reduced torso contribution | AGREED | Grask Part 1 clarification §10–14 |
| **Grask/Aelari neck distinction:** moderate-to-long neck is possible, but the primary elongation signal is limb-dominant, not Aelari-style vertically distributed elongation | AGREED | Grask Part 1 clarification §15–16 |
| **Equal-height comparison classification:** boundary-overlap comparisons are labeled as such, never treated as central-population comparisons | AGREED | Grask Part 1 clarification §3–9 |
| **Current world-validation ceiling:** about 239 cm Grask are the tallest approved playable anatomy, without setting a permanent project maximum | AGREED | Grask Part 1 clarification §19 |
| Gorrund references in Grask are future comparative placeholders only; Grask prototype scale, stats, trait, environmental and aquatic text are PROTOTYPE / NON-AUTHORITATIVE | AGREED | Grask Part 1 clarification §20–21 |
| Exact arm-span, arm-length and forearm ratios (pending prototype validation, no invented numbers) | OPEN | Grask Part 1 clarification §12–13, §22 |

Grask v1.0 Part 2

| Decision | Status | Source |
| --- | --- | --- |
| Grask anatomy is a coordinated rangy skeletal system, not a human skeleton with stretched limbs; elongation is limb-dominant, not every axial region | AGREED | Grask Part 2 §1, §3 |
| Grask arms are genuinely longer relative to height, and arm span trends greater relative to height, than Marchfolk and Skarn; arm span is multiregional, never one slider | AGREED | Grask Part 2 §21–23 |
| Lower-leg proportional emphasis is an approved first-pass tendency; femur and lower leg both contribute, with no single fixed relationship | AGREED | Grask Part 2 §15–17 |
| Five digits per hand and per foot (resolves the Part 1 OPEN digit-count row); no claws assumed; ordinary nails; no prehensile feet | AGREED | Grask Part 2 §33–34, §42–43 |
| Grask hand proportions don't imply reduced fine motor control | AGREED | Grask Part 2 §35 |
| Grask pelvis coordinates long legs, upright locomotion and torso without scaling or narrowing a human pelvis | AGREED | Grask Part 2 §12 |
| Grask validity is relationship-aware, not slider-by-slider; no maximum-everything character; no fixed subtypes | AGREED | Grask Part 2 §59–61 |
| Forearm proportional contribution meaningfully emphasized; fingers somewhat longer relative to palm than Marchfolk and Skarn | PRELIMINARY | Grask Part 2 §25–26, §31 |
| Hands and feet large in absolute terms but not oversized; thorax less broad relative to stature than Skarn; Narrow frames may trend narrower feet (soft correlation) | PRELIMINARY | Grask Part 2 §7, §28, §38–41 |
| Exact limb, span, foot and hand ratios; pelvic and scapular morphology; fat-distribution tendencies | OPEN | Grask Part 2 §10, §12, §22, §40, §56 |
| Whether Grask muscular-development capacity differs from humans; any gameplay effect of base of support, reach or long legs | OPEN | Grask Part 2 §44, §53, §81 |

Grask Part 2 minor clarification

| Decision | Status | Source |
| --- | --- | --- |
| Hand and foot cross-race tests include Fenn and compare structure, not finger or foot length alone; Grask hands and feet never exaggerated to force a difference | AGREED | Grask Part 2 clarification §1–2 |
| Grask upper arms trend longer in absolute terms and relative to standing height than Marchfolk and Skarn; upper-arm share of total arm length varies with forearm contribution; forearms needn't exceed upper arms | AGREED | Grask Part 2 clarification §3–4 |
| Gorrund shorthand in Grask establishes no Gorrund property; Grask variation never presumes an unfinished population's anatomy | AGREED | Grask Part 2 clarification §5 |
| Skeletal frame doesn't directly determine Grask foot breadth; any correlation lives in distributions, presets and randomization | AGREED | Grask Part 2 clarification §6 |
| **Project-wide:** a population-level anatomical correlation doesn't automatically create a hard creator-control dependency (weighted distributions, conditional probabilities and relationship-aware envelopes instead) | AGREED | Grask Part 2 clarification §7 |

Grask v1.0 Part 3

| Decision | Status | Source |
| --- | --- | --- |
| Grask stay recognizable bald, clean-shaven, neutral, ears partly obscured and without presentation; identity never depends on ugliness, tusks, fangs, big noses, underbites, warts, green skin or monster expressions | AGREED | Grask Part 3 §1, §60 |
| **Grask biology does not require conventional unattractiveness** | AGREED | Grask Part 3 §37 |
| Tusks aren't required Grask anatomy; no required prognathism, underbite or misaligned jaw | AGREED | Grask Part 3 §15, §21–22 |
| Facial hair gives zero required recognition; baldness valid; no male-coded troll face; no invented troll hairstyles | AGREED | Grask Part 3 §51–56 |
| Grask ears are not part of the elven ear family and are never enlarged Fenn ears; ear damage is acquired, never default | AGREED | Grask Part 3 §39–46 |
| Grask facial control organization is provisional; required coverage listed; facial validity relationship-aware; no "troll" slider | AGREED | Grask Part 3 §57–60 |
| Elongated, structurally grounded craniofacial foundation: greater facial and midface vertical contribution than Marchfolk and Skarn, vertically integrated zygomatics, substantial vertically organized mandible | PRELIMINARY | Grask Part 3 §2–14, §23 |
| Grask ears: elongated humanoid ears with backward or upward taper (the "broader base than elves" wording is superseded by the AGREED Grask ear architecture row below) | PRELIMINARY | Grask Part 3 §39, §44 |
| Functional humanoid dentition as a baseline ("omnivorous-style" wording removed; see the AGREED dentition and diet row below) | PRELIMINARY | Grask Part 3 §20 |
| Detailed dentition; possible limited tusk-like canine variation; maxillary and mandibular projection distribution | OPEN | Grask Part 3 §15, §20–21 |
| Positive definition of what makes a Grask ear non-elven (elves already cover broader base, upward and backward taper and strong attachment); ear length ranges | OPEN | Grask Part 3 audit, §42 |
| Hair density and texture distributions; pattern hair loss; sex-related facial anatomy and facial-hair distribution; body hair; head-to-height ratio | OPEN | Grask Part 3 §48–55, §82–83 |

Grask Part 3 ear and craniofacial clarification

| Decision | Status | Source |
| --- | --- | --- |
| **Grask ear architecture:** robust folded auricular cartilage, upper-ear structural volume sustained farther outward, a later terminal taper and a recognizable lower auricular or lobular region; length and orientation alone never distinguish Grask from elven ears (resolves the OPEN non-elven ear definition row above; ear length ranges stay OPEN) | AGREED | Grask Part 3 clarification §1–14 |
| **Grask facial verticality:** multiregional, never defined solely by facial-height-to-width ratio; broad faces don't reduce Graskness; absolute and proportional facial height stay distinct | AGREED | Grask Part 3 clarification §16–20 |
| **Grask dentition and diet separation:** functional humanoid dentition is the first-pass baseline; no diet inferred | AGREED | Grask Part 3 clarification §21–22 |
| **Terminology:** "long-planed" isn't project terminology; use specific anatomical language (for example elongated, vertically organized craniofacial architecture) | AGREED | Grask Part 3 clarification §15 |
| Exact tooth morphology, canine prominence distributions, dietary specialization and biological dietary range | OPEN | Grask Part 3 clarification §22 |

Grask v1.0 Part 4

| Decision | Status | Source |
| --- | --- | --- |
| Surface appearance reinforces but never primarily creates Grask recognition; Grask read under a neutral material; no single mandatory fantasy color | AGREED | Grask Part 4 §1–2 |
| Green only through undertones and pigment relationships, never saturated fantasy green by default; gray never implies stone, death, disease, age or underground ancestry; brown and umber fully valid | AGREED | Grask Part 4 §5–7 |
| No invented pigment biochemistry; no habitat-derived pigmentation; default skin is biological (no warts, scales, rock, slime); warts and growths aren't racial anatomy | AGREED | Grask Part 4 §9–10, §14, §17 |
| Environmental states, scars, tattoos, cosmetics and paint aren't phenotype; no swamp-grime default; clean-character test for every preset; biological appearance separate from lighting | AGREED | Grask Part 4 §49–57 |
| No skin, hair, iris or anatomy phenotype packages; no stereotype presets; no invented genetics | AGREED | Grask Part 4 §25, §64–73 |
| Grask pigmentation envelope: earth-toned, low-to-moderate chroma with olive, moss, umber, ochre, clay, gray-green and stone-like undertones; natural hair envelope of blacks, browns, muted reddish-brown and dark gray-brown; iris envelope of browns, amber, hazel, gold-brown, olive-hazel, gray and muted green | PRELIMINARY | Grask Part 4 §3–4, §23, §30 |
| Humanoid sclera and round pupils as first-pass baseline; Grask visibly age with systemic, not overlay, aging | PRELIMINARY | Grask Part 4 §33–34, §38–46 |
| Pigment mechanisms, skin thickness and durability, blood biology, flushing, freckle and mole distributions | OPEN | Grask Part 4 §8, §16, §18, §20–21 |
| Grask low-light visual adaptation; lifespan, maturation, fertility and senescence; graying timing; age-related hair loss pattern | OPEN | Grask Part 4 §27, §35, §39, §48 |
| Sex-related pigmentation and hair biology; normal scleral tint range | OPEN | Grask Part 4 §33, §74–75 |

Grask Part 4 pigmentation overlap clarification

| Decision | Status | Source |
| --- | --- | --- |
| **Cross-population surface overlap (project-wide):** populations may overlap in skin, hair, iris and other surface phenotypes; recognition never depends on artificially exclusive palettes | AGREED | Grask Part 4 clarification §4, §8 |
| **Grask/human pigmentation relationship:** some individual Grask skin colors overlap ordinary human appearance; the Grask envelope as a whole extends into undertone and color relationships (moss-olive, gray-olive, muted gray-green) not approved for ordinary humans; skin alone never classifies an individual as Grask | AGREED | Grask Part 4 clarification §1–3 |
| **Grask/Vael surface overlap:** gray and desaturated Grask and Vael may overlap or sit adjacent; anatomy distinguishes them, including at the 198–203 cm boundary; needing pigmentation to separate them fails | AGREED | Grask Part 4 clarification §5–7 |
| **Clarified — regional pigmentation consistency:** natural regional variation is valid; technical discontinuity between body regions isn't | AGREED | Grask Part 4 clarification §9–10 |
| **Clarified — white Grask hair:** bright white isn't a central ordinary adult family but may occur through aging, premature whitening or later-approved individual biology; hair color never sets age | AGREED | Grask Part 4 clarification §11–12 |
| Marchfolk and Vael pigmentation ranges unchanged by this patch | AGREED | Grask Part 4 clarification §5, §14 |

Grask v1.0 Part 5 and final review

| Decision | Status | Source |
| --- | --- | --- |
| **Grask Character Design v1.0 FIRST-PASS COMPLETE** (approved first-pass race spec; open questions, gameplay, technical architecture and UE5 implementation not resolved or authorized) | AGREED | Grask Part 5 §106–107 |
| Grask movement emerges from anatomy, not a troll animation style; resting alignment is upright, bipedal and plantigrade; no permanent hunch or lowered head to fit the world; body language stays separate from anatomy | AGREED | Grask Part 5 §1–5 |
| Grask anatomy establishes no movement speed, jump, climbing, fall or stealth performance; anatomical reach never silently becomes interaction, combat or targeting reach | AGREED | Grask Part 5 §7, §17, §19, §23, §27–30, §70 |
| Weapons never scale with the wielder; Grask armor, gloves, boots, helmets and clothing are never uniformly enlarged human gear; ears never clip through helmets | AGREED | Grask Part 5 §31–50 |
| The world is validated against approved Grask anatomy (tallest current anatomy about 239 cm, not a permanent maximum); no shortening, crouching or deforming to fit prototype spaces or collision | AGREED | Grask Part 5 §4, §15, §51–60, §67 |
| Retargeting adapts animation to anatomy; a shared animation system that only works by compressing Grask relationships is unacceptable; NPCs, presets and randomization use one biological system | AGREED | Grask Part 5 §74–80 |
| Final first-pass Grask identity statement and "What Grask are NOT" list | AGREED | Grask Part 5 §101–102 |
| Grask swimming and breath traits: legacy gameplay traits under later review, no biological explanation | OPEN | Grask Part 5 §24–26, §103 |
| Movement, jump and climbing performance; size effects on gameplay; collision, crouch capsule, hitboxes and combat and interaction reach; camera architecture | OPEN | Grask Part 5 §7, §15, §27–30, §63–69 |
| Equipment practicality and restrictions; furniture and accommodation strategy; intentionally constraining low spaces; mounts and vehicles | OPEN | Grask Part 5 §36, §39, §53, §57, §71–72 |
| Animation architecture, IK and retargeting; stealth design; shared saved-appearance schema and versioning | OPEN | Grask Part 5 §70, §73–76, §82 |

Grask final housekeeping patch

| Decision | Status | Source |
| --- | --- | --- |
| Grask Part 5 §104 is MAJOR OPEN DECISIONS — NON-EXHAUSTIVE; the Decision Register is authoritative for the complete set of unresolved Grask questions, and smaller OPEN items stay open unless explicitly resolved | AGREED | Grask final housekeeping §1 |
| The §101 identity statement is a summary; stone-brown, cool stone-gray-brown and other valid Grask pigmentation stay approved, and the envelope isn't narrowed | AGREED | Grask final housekeeping §2 |
| Grask stealth is never inferred from stature; prototype stealth values stay non-authoritative; no stealth bonus or penalty approved | AGREED | Grask final housekeeping §3 |
| Minor Grask biological uncertainties still open: limited tusk-like canine variation, exact ear-length ranges, blood biology, visible flushing, normal scleral tint range, graying timing and prevalence, premature whitening distributions | OPEN | Grask final housekeeping §1 |

Gorrund v1.0 Part 1

| Decision | Status | Source |
| --- | --- | --- |
| Gorrund are a distinct large non-human humanoid population whose identity comes from massive load-bearing skeletal architecture, not muscle, fat, ugliness, posture, intelligence, culture or monster anatomy | AGREED | Gorrund Part 1 §1–2, §98 |
| Large-race identity triangle: Skarn large-scale powerful human, Grask rangy reach-oriented non-human, Gorrund massive load-bearing non-human (comparative identities, not gameplay classes) | AGREED | Gorrund Part 1 §3 |
| "Massive" means skeletal structural scale first; skeletal massiveness is independent of Current Muscularity and Body-Fat Amount; "thick-boned" isn't technical language | AGREED | Gorrund Part 1 §4–5, §43 |
| Upright plantigrade humanoid bipeds; no required hunch, forward head or bent knees; no permanent crouch to fit the world | AGREED | Gorrund Part 1 §22, §39, §76 |
| Load-bearing architecture sets no speed, tempo, strength, stability, reach or intelligence; no gameplay inferred from size; legacy slow-swimming and easy-to-spot traits stay gameplay-only with no invented biology | AGREED | Gorrund Part 1 §25, §63–71 |
| Gorrund validity is relationship-aware; no maximum-everything character; height never uniform scaling and never the identifier | AGREED | Gorrund Part 1 §7, §9, §88–89 |
| Provisional adult height 208–251 cm, reference about 229 cm (subject to cross-race and world validation); if it survives, 251 cm becomes the current world-validation ceiling, not a permanent maximum | PRELIMINARY | Gorrund Part 1 §6–8 |
| Broad skeletal thorax with substantial depth relative to stature and breadth; substantial shoulder girdle and pelvis; moderate neck with high shoulder-torso integration | PRELIMINARY | Gorrund Part 1 §12–24 |
| Lower proportional limb and greater axial contribution than Grask at equal height; large absolute but not reach-dominant arms; substantial joint structural presence as a strongest body signal | PRELIMINARY | Gorrund Part 1 §26–41 |
| Five digits per hand and foot expected, confirmed at the Part 2 audit | PRELIMINARY | Gorrund Part 1 §40 |
| Torso-to-limb proportions, including whether Gorrund limb contribution is lower than Marchfolk and Skarn or only than Grask (Durrim convergence risk) | OPEN | Gorrund Part 1 §13, §27, audit |
| Ribcage, shoulder and pelvic morphology; femur-to-lower-leg and upper-arm-to-forearm relationships; hand and foot architecture | OPEN | Gorrund Part 1 §17–23, §29–38 |
| Muscular-development capacity; sex-related anatomy and dimorphism; face, ears, pigmentation, hair biology, lifecycle | OPEN | Gorrund Part 1 §50, §58–61, §99 |
| Movement performance, size gameplay consequences, collision, camera and equipment architecture | OPEN | Gorrund Part 1 §64, §69–79 |
| Whether Gorrund equal-height tests should also name Fenn (overlap about 208–211 cm) | OPEN | Gorrund Part 1 audit |

Gorrund v1.0 Part 2

| Decision | Status | Source |
| --- | --- | --- |
| Gorrund anatomy is a coordinated massive load-bearing skeletal system, never a uniformly enlarged human or generic width and depth sliders; axial means spine, ribcage, girdles and transitions, never a torso overwhelming the limbs | AGREED | Gorrund Part 2 §1–3 |
| Five digits per hand and foot (four fingers and opposable thumb, five toes), locked (resolves the Part 1 expectation); ordinary nails; non-prehensile humanoid toes | AGREED | Gorrund Part 2 §40, §46, §55–56 |
| Gorrund hands are large, substantial and fully dexterous; large anatomy never implies poor dexterity | AGREED | Gorrund Part 2 §39, §45, §48, §106 |
| Thoracic skeletal depth is separate from abdominal projection; no ogre belly; narrow breadth never means low depth; broad frame never hard-links to maximum depth, muscle, fat or strength | AGREED | Gorrund Part 2 §9, §14, §62, §64–65 |
| Frame, current muscularity, fat amount and fat distribution stay distinct; frame correlations are weighted distributions, never hard locks | AGREED | Gorrund Part 2 §59–60, §69 |
| Relationship-aware validity is mandatory; no max-everything preset; joints scale with bones; hand-wrist and foot-ankle correlate inside envelopes | AGREED | Gorrund Part 2 §86–91, §108 |
| Greater torso contribution and lower proportional leg contribution than Grask at matched height, with fully functional adult limbs; Grask have greater relative arm length and span | PRELIMINARY | Gorrund Part 2 §4–5, §23, §31 |
| Thoracic depth relative to stature as a strongest signal; substantial load-bearing pelvis; palms broad and deep relative to hand length (tendency) | PRELIMINARY | Gorrund Part 2 §8, §17, §42 |
| Gorrund limb and torso contribution relative to Marchfolk and Skarn (needed as the positive anchor for the Durrim and Skarn tests) | OPEN | Gorrund Part 2 audit |
| Numerical ratios (femur and lower leg, upper arm and forearm, arm span); pelvic morphology; fat-distribution tendencies; muscular-development capacity | OPEN | Gorrund Part 2 §17, §27, §32, §36, §74, §76 |
| Movement performance (speed, acceleration, jump, agility, stamina); equipment practicality for large hands | OPEN | Gorrund Part 2 §95, §97 |

Gorrund Part 2 boundary and arm clarification

| Decision | Status | Source |
| --- | --- | --- |
| **Clarified — Gorrund arm architecture:** large arms with substantial absolute length from overall stature; increased arm length or reach relative to height isn't a Gorrund identifier; "long arms" shorthand superseded (spec > register > prototype and earlier shorthand) | AGREED | Gorrund Part 2 clarification §3–6 |
| **Classified — Gorrund/Aelari:** about 208–221 cm is a Cross-Population Equal-Height Boundary Test | AGREED | Gorrund Part 2 clarification §1 |
| **Classified — Gorrund/Sagekin:** about 208 cm is a Cross-Population Equal-Height Boundary Test | AGREED | Gorrund Part 2 clarification §2 |
| **Added — Gorrund/Fenn:** about 208–211 cm is a Cross-Population Equal-Height Boundary Test, with Fenn added to hand and foot tests (resolves the OPEN Fenn row above) | AGREED | Gorrund Part 2 clarification §7–12 |

Gorrund v1.0 Part 3

| Decision | Status | Source |
| --- | --- | --- |
| Gorrund stay recognizable bald, clean-shaven, neutral, ears partly obscured and without presentation; identity never depends on tusks, fangs, giant jaw, underbite, huge nose, tiny eyes, heavy brow, scars, warts, ugliness, aggression or fantasy skin | AGREED | Gorrund Part 3 §1, §82 |
| Gorrund can be attractive, ordinary, unusual, severe, soft-featured or weathered; "Gorrund" never means ugly | AGREED | Gorrund Part 3 §49–51, §109 |
| Tusks not required; no mandatory fangs or exposed teeth; underbite, overbite and misalignment not racial; functional humanoid dentition baseline with no diet inferred | AGREED | Gorrund Part 3 §26–30 |
| Facial hair gives zero required recognition; baldness valid but not required; no cultural hairstyles in biology | AGREED | Gorrund Part 3 §70–79 |
| Gorrund face-control organization is provisional; coverage listed; relationship-aware validity with envelopes; no "ogre" control; broad face never hard-links to broad nose | AGREED | Gorrund Part 3 §24, §80–84 |
| Broad, deep, structurally integrated craniofacial architecture: cranial breadth and depth, broad orbital and zygomatic organization, deep integrated midface, substantial mandible, head-neck-body integration; not primarily vertical elongation | PRELIMINARY | Gorrund Part 3 §2–9, §17–19, §31, §36–37 |
| Gorrund ears: broad, structurally substantial humanoid auricles with strong attachment, meaningful cartilage depth, rounded-to-angular upper contour, short-to-moderate projection and a recognizable lobe; not elven, not short Grask ears | PRELIMINARY | Gorrund Part 3 §53–67 |
| Limited tusk-like canine variation (separate from Grask's); detailed dentition; prognathism distribution | OPEN | Gorrund Part 3 §21, §26–28 |
| A positive craniofacial and ear anchor separating Gorrund from Durrim and from large human ears (cartilage relationship that differs; face relationship Durrim lack) | OPEN | Gorrund Part 3 audit |
| Head-to-height ratio; ear projection range; hair density, texture and pattern loss; body hair; sex-related facial anatomy and facial-hair distribution | OPEN | Gorrund Part 3 §4, §55, §71–78, §117 |
| Lifecycle and aging detail; technical face, ear, hair, beard and skin architecture | OPEN | Gorrund Part 3 §118–119 |

Gorrund Part 3 craniofacial and ear clarification

| Decision | Status | Source |
| --- | --- | --- |
| **Gorrund craniofacial specialization: Transverse Structural Continuity** across lateral brow and orbital margins, zygomatic region and posterior mandible, with depth supporting rather than dominating; project terminology, not a slider (resolves the OPEN Gorrund–Durrim face anchor) | AGREED | Gorrund Part 3 clarification §2–5, §39 |
| **Durrim vs Gorrund face:** Durrim compact depth-dominant, Gorrund transversely distributed broad and deep; not depth-versus-width sliders; matched-scale and body-context diagnostics required; approved Durrim anatomy unchanged | AGREED | Gorrund Part 3 clarification §6–18, §38 |
| **Gorrund skull breadth:** greater cranial breadth relative to cranial height than Marchfolk (tendency), with surrounding transverse organization distinguishing it from Durrim | AGREED | Gorrund Part 3 clarification §19–20 |
| **Gorrund ear anatomy:** deep auricular bowl, strongly expressed antihelical folds, broad continuous non-tapering rim, rounded to mildly angular upper contour, broad attachment sitting relatively close to the skull; never enlarged human ears; no Gorrund traits added to Durrim (resolves the OPEN human and Durrim ear anchor) | AGREED | Gorrund Part 3 clarification §21–36 |
| Grask and Gorrund tusk-like canine questions stay separate and never merge into one non-human dental decision | AGREED | Gorrund Part 3 clarification §37 |
| Gorrund body-level relationship distinguishing them from Durrim (limb and torso contribution relative to Marchfolk and Skarn) — still unresolved after the face clarification | OPEN | Gorrund Parts 1–2 audit |

Gorrund v1.0 Part 4

| Decision | Status | Source |
| --- | --- | --- |
| Gorrund surface phenotype never primarily creates recognition; neutral-material recognition; overlapping surface phenotypes with humans, Grask and Vael are valid; no exclusive palettes | AGREED | Gorrund Part 4 §1–2, §6–8 |
| No ordinary green or pure fantasy gray Gorrund; no invented pigment mechanism; no stone, undead or mineral skin | AGREED | Gorrund Part 4 §9–12 |
| Default skin is biological, never warty, rocky, leathery or callused everywhere; growths and calluses aren't racial; smooth skin valid; no thick skin or armor from size | AGREED | Gorrund Part 4 §21–27 |
| Biological humanoid eyes, round pupils and humanoid sclera; no monster eyes; aging never increases caricature; younger adults already fully Gorrund | AGREED | Gorrund Part 4 §40–47, §51–61 |
| Environment, scars, tattoos and cosmetics aren't biology; clean-dry-neutral test; no stereotype presets (Classic Ogre, Brute, Gentle Giant and others); no skin-hair-eye packages; transverse face must read under flat light | AGREED | Gorrund Part 4 §66–72, §90, §94–96 |
| Gorrund pigmentation envelope: strongly earth-toned, overlapping human browns, umbers, ochres, olives and taupes, with some muted low-chroma edges | PRELIMINARY | Gorrund Part 4 §3–5 |
| Gorrund hair envelope (blacks, browns, dark auburn, muted reddish-brown, dark gray-brown) and iris envelope (browns, amber, hazel, gold-brown, olive-hazel, gray, gray-brown, muted green) | PRELIMINARY | Gorrund Part 4 §28–31, §41 |
| Whether the Gorrund pigmentation and hair envelopes should include lighter and intermediate complexions (currently brown and dark tones only, unlike Durrim, Marchfolk and the elves) | OPEN | Gorrund Part 4 audit |
| Bright blond and bright red boundaries; graying, premature whitening and pattern-loss distributions; hair texture and density | OPEN | Gorrund Part 4 §30–36, §63–64 |
| Pigment biology; skin thickness and durability; blood biology; flushing; freckles and moles; scleral tint; low-light adaptation | OPEN | Gorrund Part 4 §11, §18–20, §23–24, §46, §48 |
| Lifecycle; genetics; sex-related surface biology; technical surface architecture | OPEN | Gorrund Part 4 §52, §98–100 |

Gorrund Part 4 pigmentation envelope clarification

| Decision | Status | Source |
| --- | --- | --- |
| **Gorrund complexion envelope:** lighter, intermediate, darker and deep natural complexions are all biologically valid; the earth-toned center remains; "earth-toned" doesn't mean dark; no light- or dark-skin exclusion; no pigmentation subgroups; pigmentation is never a racial identifier (resolves the OPEN lighter-complexion row above) | AGREED | Gorrund Part 4 clarification §1–8, §17–19 |
| New diagnostics GOR-SKIN-11 to 13; light- and dark-skin cross-population tests fixed through anatomy, never skin; presets include lighter, intermediate and darker complexions | AGREED | Gorrund Part 4 clarification §9–13 |
| Gorrund complexion frequencies and randomization weighting | OPEN | Gorrund Part 4 clarification §2, §14 |

Gorrund v1.0 Part 5 and final review

| Decision | Status | Source |
| --- | --- | --- |
| Gorrund movement emerges from anatomy, not an ogre style; upright plantigrade resting alignment; load-bearing never means hunched; body language separate from anatomy | AGREED | Gorrund Part 5 §1–5 |
| Anatomy never sets gameplay performance: no automatic slowness, sprint, jump, fall, stealth, noise, strength or reach effect; mass shown through momentum and contact, not slow motion or stomps | AGREED | Gorrund Part 5 §2, §10, §15, §19, §21, §29–35, §133 |
| Canonical weapons never scale; Gorrund armor, gloves, boots, helmets and clothing are never uniformly scaled human gear; baldness isn't the helmet fix; fine dexterity kept | AGREED | Gorrund Part 5 §36–58 |
| World validated against approved Gorrund anatomy; 251 cm is the current highest first-pass stature if it survives validation, not a permanent maximum; no default crouching; no accidental access restrictions; no monster camera | AGREED | Gorrund Part 5 §59–75 |
| Animation architecture adapts to anatomy; retargeting never pulls Gorrund toward Marchfolk; presets, randomization and NPCs share one biological system | AGREED | Gorrund Part 5 §83–84, §128–130 |
| Final first-pass Gorrund identity statement (§134); first-pass completion pending two clarification gaps | AGREED | Gorrund Part 5 §134, §137 |
| Gap 1: body-level Gorrund–Durrim proportional anchor (limb and torso contribution relative to Marchfolk and Skarn, or a body relationship Durrim lack) | OPEN | Gorrund Part 5 audit |
| Gap 2: prototype conflict audit of the in-game Gorrund class (not re-read this session) | OPEN | Gorrund Part 5 audit |
| Slow-swimmer and easy-to-spot legacy traits; movement, jump, climb and sprint performance; size gameplay; collision; camera; mounts; furniture; access restrictions; NPC and LOD strategy | OPEN | Gorrund Part 5 §15–29, §63–81, §131–132, §135 |

Gorrund final clarification

| Decision | Status | Source |
| --- | --- | --- |
| **Gorrund Character Design v1.0 FIRST-PASS COMPLETE** (approved first-pass spec; implementation-level prototype verification DEFERRED; no UE5 implementation authorized) | AGREED | Gorrund final clarification §25 |
| **Axial Load-Path Continuity:** shoulder girdle, thorax, lower trunk, pelvis and proximal lower limbs form an integrated vertical load-bearing chain; project terminology, not a slider; readable at low muscle and narrow frame (resolves Gap 1) | AGREED | Gorrund final clarification §2–11 |
| **Durrim vs Gorrund body:** Durrim compact structural concentration, vertically compact torso and shorter limb contribution; Gorrund axial load-path continuity, vertically developed torso and fully substantial tall-body limbs; never a vertically scaled Durrim; matched-display and equalized-breadth tests (resolves the OPEN limb-and-torso contribution row) | AGREED | Gorrund final clarification §12–17 |
| Axial Load-Path Continuity (body) and Transverse Structural Continuity (face) stay separate systems with no hard coupling | AGREED | Gorrund final clarification §19–20 |
| **Gorrund prototype audit scope:** final audit complete at design-specification level; known conflicts (slow swimming, easy to spot, "long arms") resolved at design level; unknown prototype assumptions aren't approved by existing (resolves Gap 2 as scoped) | AGREED | Gorrund final clarification §21–23 |
| **Gorrund Prototype Implementation Conflict Audit** — DEFERRED until UE5 project files can be inspected; no implementation changes unless separately authorized | OPEN | Gorrund final clarification §21, §24 |

Pipkin v1.0 Part 1

| Decision | Status | Source |
| --- | --- | --- |
| Pipkin are a distinct short adult humanoid population, never scaled-down humans, child-proportioned adults, slender Durrim or small Cogling | AGREED | Pipkin Part 1 §1, §3, §116 |
| Every adult Pipkin reads as a mature adult, never a human child; no child skull, eyes, jaw, face, shoulders, pelvis, limbs, hands, feet or fat distribution; the pelvis is never a scaled juvenile pelvis | AGREED | Pipkin Part 1 §8–9, §24 |
| Short-race triangle: Durrim compact structural concentration, Pipkin light compact adult proportionality, Cogling not yet designed and never pre-defined | AGREED | Pipkin Part 1 §2, §94 |
| Five digits per hand and foot, ordinary nails, plantigrade, non-prehensile toes; no caricature feet; barefoot and hairy feet aren't biology | AGREED | Pipkin Part 1 §40–49 |
| "Light" skeletal construction never means weak or fragile; no strength, agility, balance, stealth or speed effect from size; culture, personality and intelligence never encoded; body fat and food tropes aren't identity | AGREED | Pipkin Part 1 §4, §50, §54, §62, §69–75 |
| Legacy "harder to notice while sneaking" stays a gameplay trait subject to review; equipment and world never scale to Pipkin | AGREED | Pipkin Part 1 §72–79 |
| Provisional adult height 91–122 cm, reference about 107 cm; about 122 cm is a Cross-Population Equal-Height Boundary Test with Durrim; 91 cm would be the new lower playable stature (not permanent) | PRELIMINARY | Pipkin Part 1 §5–6, §114–115 |
| Relative to Durrim at matched height: lighter skeleton, less compact torso, smaller joints, lighter long bones, greater proportional limb contribution, more moderate hands | PRELIMINARY | Pipkin Part 1 §13–14, §29, §35, §51–53, §83 |
| Somewhat greater head contribution than taller humans without an oversized head; modestly larger feet relative to stature without caricature | PRELIMINARY | Pipkin Part 1 §10, §42–43 |
| A positive Pipkin body relationship versus Marchfolk (needed for the scaled-human and human-child tests) | OPEN | Pipkin Part 1 §88, audit |
| Head-to-body ratio; torso ratios; shoulder and pelvic morphology; limb-segment, hand and foot proportions; joint dimensions | OPEN | Pipkin Part 1 §10, §23, §31, §117 |
| Muscular-development capacity; sex-related anatomy and dimorphism; face, ears, pigmentation, hair, eyes, lifecycle | OPEN | Pipkin Part 1 §66–68, §117 |
| Movement, stealth, reach and size gameplay; equipment practicality; collision; camera; furniture; mounts; technical architecture | OPEN | Pipkin Part 1 §36, §72–81, §117 |

Pipkin v1.0 Part 2

| Decision | Status | Source |
| --- | --- | --- |
| **Low-Set Compact Trunk Architecture:** moderate thorax → compact lower trunk → mature structurally broad pelvis → proportionally sustained limbs; project terminology, not a slider; distinguishes Pipkin positively from scaled Marchfolk (resolves the OPEN positive-body-vs-Marchfolk row) | AGREED | Pipkin Part 2 §1–6 |
| The Pipkin pelvis carries greater structural importance relative to the thorax than Marchfolk; mature adult pelvis mandatory; pelvic breadth never the sole identifier; skeletal pelvis separate from fat and muscle | AGREED | Pipkin Part 2 §8–12, §64, §80 |
| Greater relative head contribution is never a maturity signal; the "large head" brief shorthand is superseded (oversized head not a racial trait) | AGREED | Pipkin Part 2 §71–74 |
| Durrim vs Pipkin at matched size: Durrim vertically compact, broad and deep thorax, reduced limbs; Pipkin moderate thorax, low-set trunk, pelvis-weighted, lighter, greater limb contribution; 122 cm is a single-height boundary test | AGREED | Pipkin Part 2 §16–17, §75–77 |
| Moderate adult dexterous hands; feet with modestly elevated contribution as a secondary identifier; five digits per hand and foot; plantigrade; no flat feet inferred | AGREED | Pipkin Part 2 §36–54 |
| Frame, muscle, fat amount and distribution separate; no hidden physique packages; no "human → Pipkin" master slider; relationship-aware validity mandatory | AGREED | Pipkin Part 2 §55–68, §84–86 |
| Pipkin leg contribution greater than Durrim at matched height without exceeding ordinary human proportions by default; no unusual arm span | PRELIMINARY | Pipkin Part 2 §19–27 |
| Whether the Pipkin pelvis-to-thorax tendency is measured within sex (male vs male, female vs female) and kept separate from sex dimorphism, so male Pipkin don't read female-coded | AGREED (resolved by the Part 2 patch below) | Pipkin Part 2 audit; patch `da3692b` |
| Pelvic and arch morphology; femur-to-lower-leg balance; arm span; muscular-development capacity; fat-distribution patterns (a concrete measure for "low-set" is resolved by the Part 2 patch below) | OPEN | Pipkin Part 2 §10, §22, §27, §50, §61, §63 |

Pipkin v1.0 Part 2 author resolution (approved by Tyler September 30; §§2–3 patched into the spec at `da3692b`)

| Decision | Status | Source |
| --- | --- | --- |
| Low-Set Compact Trunk Architecture includes a modestly reduced vertical central-trunk share versus Marchfolk, a compact lumbar and waist transition, and a pelvis whose vertical height, depth and 3D integration stay substantial relative to the thorax; it persists at Marchfolk-like pelvic breadth; never Durrim-like compression; no slider or fixed ratio (closes the concrete "low-set" measure item); reduced trunk share is absorbed mainly by limbs and pelvic height, not head enlargement | AGREED | Pipkin Part 2 patch `da3692b`; re-audit §3.1–3.2, §4a |
| Pelvis-to-thorax comparisons use like-for-like sex-related anatomical configurations; the trait is expressed through pelvic structure, never shoulder-to-hip ratio, hip circumference or a feminized silhouette; male and female Pipkin vs Marchfolk validation pair; PIP-BODY-28 and PIP-BODY-29; dimorphism magnitude stays OPEN (closes the within-sex item) | AGREED | Pipkin Part 2 patch `da3692b`; re-audit §3.3 |
| The 122 cm Durrim boundary is carried jointly by torso vertical organization, thoracic presence, limb contribution, joints, long-bone robusticity, hand, wrist, foot and ankle structure and the two trunk systems; pelvic breadth is not primary (approved, but not yet written into the spec) | AGREED | Author resolution §4; re-audit §3.4; Part 3 audit §2 |
| Canonical race file location is `specs/<race>/<RACE>_V1.md` (Tyler, September 30); the author resolution's §1 wording naming `races/` is stale, and ChatGPT's Part 3 request treats `specs/` as authoritative | AGREED | Tyler; Part 3 audit request; re-audit §2a |

Pipkin v1.0 Part 3 (FIRST-PASS ACCEPTED; Tyler approved September 30)

| Decision | Status | Source |
| --- | --- | --- |
| Adult Pipkin faces read mature and Pipkin before hair, facial hair, wrinkles, cosmetics, expression, clothing or scale context; no beauty standard is biological | AGREED | Pipkin Part 3 §1, §14 |
| **Integrated Mature Facial Architecture** (renamed from Compact Mature Facial Integration): moderately broad cranial base → temple and zygoma → central midface → mature lower face; nasal, maxillary, dental-arch, ramus and gonial structures never juvenile-shortened; depth relative to facial height within the Marchfolk adult range (not Durrim depth-dominance); lateral support ends at the central midface with no ramus participation (not Gorrund Transverse Structural Continuity); not a single control | AGREED | Pipkin Part 3 §2, §5–6; re-audit |
| Head contribution secondary; no enlarged vault; no biologically oversized eyes; larger valid orbit and aperture stay within the adult Marchfolk-compatible range; orbit separate from visible aperture; small or upturned nose isn't a Pipkin trait; moderately scaled mature mandible | AGREED | Pipkin Part 3 §3–8 |
| **Compact Rounded Auricular Architecture:** non-elven ears; no elven point, Grask taper or Gorrund deep bowl; no mandatory tiny or comic ears; a central tendency only, overlapping Marchfolk and Durrim ears, not an identifier | AGREED | Pipkin Part 3 §9 |
| Hair, facial-hair, brow and lash biology separate from presentation; facial hair never required for adult or male recognition; sex-related facial-hair distributions OPEN; no hairy-feet requirement | AGREED | Pipkin Part 3 §11–13 |
| Facial controls are APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION; no "Pipkin Face" master slider; tendencies bias randomization only | AGREED | Pipkin Part 3 §15 |
| Facial identity is supporting; Low-Set Compact Trunk Architecture is the primary identifier; the facial vertical envelope is primarily skeletal, with soft tissue only modulating it | AGREED | Pipkin Part 3 status note; re-audit §3a–3b |

Pipkin v1.0 Part 4 (FIRST-PASS ACCEPTED; Tyler approved September 30)

| Decision | Status | Source |
| --- | --- | --- |
| No surface phenotype is required to identify a Pipkin; overlap with other populations is expected; identity stays structural | AGREED | Pipkin Part 4 §1, §21 |
| Broad skin pigmentation with no complexion default; tanning, freckling, vascularity and localized pigment independent of base pigmentation; no ruddy or freckled-halfling default | AGREED | Pipkin Part 4 §2–4 |
| No eye color, hair color or texture identifies a Pipkin; dye is presentation; graying optional and premature graying valid | AGREED | Pipkin Part 4 §5, §7–8 |
| Body hair varies; hairy feet and hairy bodies not required; body hair never encodes rusticity, masculinity, youth or femininity | AGREED | Pipkin Part 4 §11 |
| Mature adult humanoid dentition; no oversized incisors, tusks, fangs, rodent or childlike teeth; ordinary nails | AGREED | Pipkin Part 4 §12–13 |
| No hidden phenotype bundle; biological and presentation randomization stay separate | AGREED | Pipkin Part 4 §18 |
| FD domains used for facial analysis only, with their AGREED meanings; whole-body surface uses the Skin Appearance Layers (Natural, Environmental, Applied or Acquired) | AGREED | Pipkin Part 4 §16, §18; re-audit |
| Pipkin iris may span a broad natural humanoid range; validity limits, rare colors and frequencies OPEN | AGREED | Pipkin Part 4 §5; re-audit |
| Skin aging and environmental weathering are covered; Apparent Biological Age is distinct from surface aging; young-looking adults stay structurally mature without wrinkles; no fixed regional-weathering map; Pipkin lifecycle timing OPEN | AGREED | Pipkin Part 4 §16; PIP-SURF-21 |
| Pipkin dentition follows the existing functional adult humanoid baseline with no diet inferred; tooth count, replacement and lifecycle OPEN | AGREED (count and lifecycle OPEN) | Pipkin Part 4 §13; re-audit |
| Pipkin skin, hair and iris frequencies; interim randomization is broad and explicitly not an approved distribution; tanning and freckling distributions; sex-related body and facial hair distributions | OPEN | Pipkin Part 4 §2–3, §5, §11, §18; audit 4e |

Marchfolk v1.0 and v1.5 are referenced but haven't been received here. Send them and their decisions go into this register.
