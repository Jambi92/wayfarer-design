# Halvren Character Design v1.0 (first-pass biological foundation complete)

This is the Halvren specification, the mixed human and elven ancestry population. It's design only, with no UE5 changes. It builds on Marchfolk v1.0–v1.5 and its consistency resolutions, Skarn, Sagekin, Fenn, Aelari and Vael v1.0–v1.5, the Elf Comparative Review v1.0 with all clarifications, the universal character creation amendment, and the conflict audit and authority rules. v1.0 arrives in parts. Part 1 (mixed-ancestry biological foundation), Part 2 (body architecture, height and skeletal inheritance), Part 3 (craniofacial anatomy, eyes and mixed external-ear inheritance), Part 4 (pigmentation, hair, iris and mixed-ancestry appearance inheritance) and Part 5 (lifecycle, culture separation, presets, randomization, validation and technical handoff) are complete. Together these five parts are the authoritative Halvren v1.0 set, and the first-pass biological foundation is complete. The consistency review against the source specs and its resolution patch follow Part 5, and v1.1 isn't begun.

# Part 1 Mixed-ancestry biological foundation

## 1–4. Core identity and inheritance principles

Halvren are a biologically viable mixed human and elven ancestry population. **They aren't humans with pointed ears, generic elves with human proportions, or automatic 50/50 anatomical averages.** Their appearance emerges from inheritance across two related but distinct humanoid families: human (Marchfolk, Skarn, Sagekin) and elven (Fenn, Aelari, Vael).

**There's no single mandatory Halvren body or face (locked).** Two Halvren may express mixed ancestry very differently and both be valid. One might express stronger elven ancestry in limb relationships and stronger human ancestry in torso structure, and another the reverse, and craniofacial, ear, pigmentation and other systems may vary the same way. These systems can't combine arbitrarily, though, since developmental relationships keep the anatomy coherent.

**Ancestry isn't arithmetic averaging (locked).** Halvren are never generated as human value plus elven value divided by two for each parameter. Inheritance may be polygenic, dominance-like, recessive-like, additive or nonlinear, with trait correlations, developmental constraints, population-specific inheritance and multigenerational recombination. Genetic simulation depth is unresolved. **Halvren aren't necessarily 50/50:** valid histories include first-generation human and elven ancestry, Halvren plus human, Halvren plus elf, Halvren plus Halvren, multigenerational mixing and more complex family histories, so anatomy is never hardcoded to equal contribution.

## 5–9. Compatibility, populations and scope

| Topic | Direction |
| --- | --- |
| Family compatibility (§5, provisional) | Human-family and elven-family populations are compatible enough to produce viable mixed descendants. This is a worldbuilding rule, with no chromosome counts, molecular genetics, reproductive mechanisms or fertility probabilities unless later design benefits from them |
| Multigenerational viability (§6, locked provisionally) | Halvren can form persistent multigenerational populations and aren't biological dead ends, allowing Halvren families, communities, long-established mixed populations and recombination across generations. Fertility biology is out of scope for this first pass |
| Population versus ancestry category (§7) | Halvren are both a playable race or population identity and a biological mixed-ancestry category. Who counts as Halvren culturally or legally isn't defined yet, biological ancestry and social identity stay separate, and later lore decides how societies use the term |
| Source populations (§8) | The architecture supports contributions from Marchfolk, Skarn and Sagekin (human family) and Fenn, Aelari and Vael (elven family). Not every Halvren visibly shows traits from one named human and one named elven population, since multigenerational ancestry may blur, preserve or recombine signals |
| Validity versus frequency (§9) | Combinations may be common, uncommon, rare, regionally concentrated, historically established or recent, and aren't all equally common just because biology allows them |

## 10–14. Expression domains, genealogy and coherence

There's no single human-to-elf slider for the whole body. Inheritance may express differently across domains: overall skeletal architecture, torso, shoulders, pelvis, arms, legs, hands, feet, craniofacial anatomy, orbits and eyes, external ears, skin pigmentation, hair biology, iris pigmentation, lifecycle biology, and physiology where later established. These domains stay biologically coordinated.

**Genealogical ancestry** (the individual's actual family ancestry) and **phenotypic expression** (how inherited ancestry shows physically) aren't identical. Someone with substantial elven genealogy may not strongly express every visibly elven trait, and one conspicuous elven trait doesn't prove an ancestry percentage. Genealogy is never inferred from one visible feature.

**Developmental coherence (locked):** inheritance is relationship-aware, and a character can't inherit unrelated extremes from different populations if the result is implausible. If limb proportions strongly express Fenn ancestry, connected shoulders, pelvis, joints, hands and feet may need compatible ranges. That doesn't mean they all express the same ancestry strength, only that development produces one coherent organism.

| Candidate soft inheritance cluster (§13) | Contents |
| --- | --- |
| Axial skeleton | Spine, ribcage, torso relationships |
| Appendicular skeleton | Shoulders, pelvis, arms, legs, joint relationships |
| Distal anatomy | Hands, feet |
| Craniofacial | Cranium, orbits, midface, jaw |
| External ear | Ear foundation and morphology |

These are conceptual biological groupings, not creator sliders or code architecture yet. **Mosaic expression without patchwork:** a Halvren could plausibly have relatively human-like torso depth, moderately elven limbs, strongly elven ears and intermediate craniofacial architecture, valid only when the transitions stay developmentally coherent. It fails if the result looks like body parts copied from separate race meshes and attached together.

## 15–18. Human and elven structural contributions

| Source | Contributes tendencies toward | Population nuance |
| --- | --- | --- |
| Human family (§15) | Human-family skeletal architecture and structural distributions (not universal "robustness," per the consistency resolution), torso, joint and hand-foot relationships, craniofacial architecture and external-ear architecture | Specific populations shift distributions, for example Skarn ancestry carries different structural tendencies than Sagekin. Human ancestry never collapses into one identical source |
| Elven family (§16) | The shared elven foundation from the Elf Comparative Review: more gracility than equivalent robust human populations such as Skarn, non-human torso and shoulder relationships, elven pelvic foundation, relatively elongated limbs, distinct hand-foot relationships, elven craniofacial and non-human ear architecture | Fenn extremity-emphasized, Aelari vertically distributed, Vael deeper with compact continuity |

There's **no generic elf parent**: no averaged elven source that erases Fenn, Aelari and Vael differences, though shared elven ancestry may provide common constraints. There's **no generic human parent** either: Marchfolk stay the primary Human Reference Population, but Skarn and Sagekin are also valid human-family ancestry.

## 19–22. Height, frame, composition and sex-related anatomy

**Height isn't locked in Part 1.** Source populations span very different ranges, so a fixed midpoint would be misleading, and height is reviewed once the inheritance architecture exists. Halvren keep the **Skeletal Frame** (continuous skeletal configuration) versus **Frame Preset** (creator starting configuration) distinction, with Narrow, Balanced and Broad as possible presets. Valid underlying ranges may depend partly on ancestry, so a Broad Halvren isn't assumed identical to a Broad Marchfolk or Broad Aelari. Muscle and fat aren't ancestry percentages: Halvren vary broadly in muscularity, body-fat amount and distribution and regional development, a strongly elf-expressing Halvren may be muscular or heavy, a strongly human-expressing one may be lean, and thinness is never shorthand for elven ancestry. Sex-related anatomy stays separate from frame, height, muscle, fat, face, hair and presentation, mixed ancestry doesn't change that, and exact sex-related inheritance stays within the broader unresolved anatomical-system review.

## 23–29. Genealogy labels, player freedom, modes, randomization and presets

A Halvren is never labeled "25% elf-looking" or "75% human-looking" from phenotype. If ancestry is ever shown to the player, genealogy and visible expression stay distinct. Players get substantial freedom to make distinctive Halvren inside a biological validity system: the goal isn't "every combination is valid" but "many combinations are valid because the inheritance system was designed to support them coherently." Simple Mode never requires understanding genetics, so a player can pick a preset and play, with presets showing varied expression patterns without exposing inheritance logic. Advanced Mode may offer meaningful customization without literal genetic editing, possibly through ancestry-informed presets, individual anatomical controls and selective randomization. ("Population-influence controls" is reinterpreted by the consistency resolution: any control that changes genealogical ancestry is an ancestry-editing control, clearly separate from editing physical expression, never an appearance slider). The UI is OPEN, and **there's no "Elf Percentage" slider** at this stage.

Randomization must eventually be ancestry-aware, population-aware, relationship-aware, developmentally constrained and reproducible where required. It fails if it produces humans with random pointy ears, generic elves with slightly human faces, anatomical patchwork, repeated exact 50/50 averages, or one stereotypical half-elf phenotype. Future character presets should show the valid range: human-leaning anatomy with subtle elven expression, balanced mixed expression, elf-leaning anatomy with clear human contribution, a multigenerational Halvren with no obvious first-generation look, broad or heavy, lean, and elder. These are appearance starting points that don't define genealogy, culture or background. Presentation presets (human or elven cultural influence, Halvren community traditions, cross-cultural upbringing, regional fashion, personal style) never determine ancestry.

## 30–31. Core validation and anti-stereotype rules

> **Hide the ears, neutralize pigmentation and remove cultural presentation. A Halvren should still be able to read as a biologically coherent person whose anatomy can plausibly contain both human and elven ancestry.**

Not every Halvren must look identifiably mixed at a glance, and subtle expression is valid. Halvren aren't universally attractive, young-looking, slim, graceful, narrow-faced, light-skinned, long-haired, socially conflicted, charismatic, diplomatic, outcast, or "caught between two worlds." Those may describe individuals or stories, not biological requirements.

## 32–33. Technical architecture and save data (OPEN)

Whether Halvren need a human, elven or dedicated Halvren skeleton, a shared hierarchy, procedural skeletal blending, morph-based inheritance, multiple base meshes, MetaHuman, modified MetaHuman, custom architecture or a hybrid isn't decided. The system must reproduce approved mixed anatomy, and convenience never redefines Halvren biology. Future appearance data distinguishes, where necessary, genealogical ancestry inputs, phenotypic expression, final anatomical state, physical composition and presentation, since storing final slider values alone may not preserve future inheritance features. The exact schema is OPEN.

## 34–35. Open questions and status

OPEN, never silently resolved: target height envelope, reference height and distribution, torso, limb, pelvic, hand and foot, craniofacial, ear, pigmentation, hair, iris and lifecycle inheritance, physiology, genetic simulation depth, ancestry UI, random-generation weighting, population frequencies, the social and lore definition, technical skeleton architecture, and gameplay racial attributes. **Halvren v1.0 Part 1 is complete**, and v1.0 as a whole isn't. No UE5 changes, and Part 2 isn't drafted independently.

# Part 2 Body architecture, height and skeletal inheritance

## 1–2. Core body principle and population envelope

> **A Halvren body is neither an averaged human and elf body nor a collection of independently inherited race parts.**

Mixed ancestry can produce substantial variation, but the final anatomy functions as one organism. Halvren don't inherit the union of every source population's valid extremes, or a Halvren creator could reproduce a pure Skarn, Marchfolk, Fenn, Aelari or Vael body with only the label changed. **Halvren have their own mixed-population validity envelope**, and source ancestry shifts variation inside it.

## 3–6. Height

| Minimum | Reference | Maximum |
| --- | --- | --- |
| About 152 cm (5'0") | About 178 cm (5'10") | About 213 cm (7'0") |

This is a **provisional first-pass range**, revised by the consistency resolution into the **Halvren central population envelope**, not an absolute biological wall (ancestry-dependent tails are allowed). It overlaps strongly with both families without covering every source extreme.

| Source population | Range | Reference |
| --- | --- | --- |
| Marchfolk | 147–203 cm | About 173 cm |
| Skarn | 183–229 cm | About 208 cm |
| Sagekin | 152–208 cm | About 178 cm |
| Fenn | 157–211 cm | About 181 cm |
| Aelari | 168–221 cm | About 190 cm |
| Vael | 157–203 cm | About 178 cm |

Height is never an average of parental or reference heights. It's a complex trait shaped by multiple ancestry contributions, individual variation, multigenerational inheritance, development, sex-related population distributions where later appropriate, and setting-specific mechanisms. A child of a very tall Skarn parent and an Aelari parent isn't automatically their midpoint, and a multigenerational Halvren may be unexpectedly tall or short relative to recent ancestors while staying valid. Genealogy may shift the probability distribution: more Skarn or Aelari ancestry toward the taller part of the envelope, Marchfolk toward a broad human-centered spread, and Sagekin, Fenn and Vael toward their own population tendencies. **Probability isn't validity**, so height is never locked to ancestry. Halvren near 152 or 213 cm stay proportionally coherent, never reached by uniform scaling, with torso, legs, arms, neck, head, hands, feet and joints all compatible.

## 7–8. Mixed skeletal family and structural presence

Halvren occupy a mixed developmental space between the human and elven skeletal families, which may affect skeletal visual mass, long-bone proportions, joint scale, shoulders, ribcage, spine, pelvis, limbs, hands and feet. Neither an unchanged human nor an unchanged elven skeleton is their biological definition, and implementation is OPEN. Skeletal expression spans a broad mixed distribution between human-family structural presence and elven-family gracility (strongly gracile, moderately gracile, intermediate or relatively robust), emerging from coordinated relationships, never a global "Elf Gracility" slider. Halvren don't normally reproduce the most population-specific skeletal extremes of a pure source population.

## 9–14. Source-population contributions

| Ancestry | May contribute tendencies toward | Guard |
| --- | --- | --- |
| Skarn (§9) | Greater skeletal robustness, broader clavicles, deeper ribcage, more substantial neck and pelvis, heavier joints, larger absolute skeletal hand and foot dimensions, a shifted muscular development capacity (not current muscularity, per the consistency resolution), taller height distribution | Not a smaller Skarn with pointed ears, since elven ancestry stays developmentally integrated. Skarn ancestry gets explicit protection against simplification |
| Fenn (§10) | Greater skeletal gracility, compact-centered relationships, stronger relative extremity contribution, greater forearm share of arm length, greater lower-leg share of leg length, longer and narrower hands and feet, shallower ribcage | Fenn traits needn't all be inherited together |
| Aelari (§11) | Greater vertical skeletal continuity, taller height distribution, longer proportional neck contribution, greater torso and waist vertical contribution, evenly elongated limb segments, long hands and fingers, elongated feet, strong gracility | Never a generic "tall and elegant" phenotype |
| Vael (§12) | Greater thoracic depth than Fenn and Aelari ancestry, more compact torso-pelvis continuity than Aelari ancestry, more joint and base presence than Fenn and Aelari ancestry, moderate limb elongation, stronger wrist-hand and ankle-foot transitions, somewhat broader hands and feet | Never equated with muscularity, heaviness or sinister posture |
| Marchfolk (§13) | Broad human-family skeletal architecture and structural distributions, torso, limb, joint and hand-foot relationships | Highly diverse, so never one narrow phenotype |
| Sagekin (§14) | Somewhat greater linearity, somewhat longer-limbed human proportions, somewhat narrower ribcage | Broad, muscular and heavy Sagekin-derived Halvren stay valid. Scholarship, intelligence, frailty, "soft hands" and magical aptitude aren't inherited, since they aren't Sagekin biology |

## 15–19. Torso, shoulders, neck and pelvis

Torso inheritance is relationship-aware and population-aware, covering ribcage width, depth and vertical length, waist-transition length, spine and torso proportions and torso-pelvis integration. It's never reduced to "human torso versus elf torso," because Fenn, Aelari and Vael already differ substantially. Plausible examples, not packages: more human-like thoracic depth with somewhat elven vertical relationships; a shallower thorax with stronger human shoulder breadth; Vael-influenced thoracic depth with otherwise mixed limbs; Aelari-influenced vertical continuity moderated by human ancestry; Fenn-influenced compact-centered anatomy moderated by human torso structure.

Shoulders vary in clavicle length, breadth, joint scale, ribcage integration and neck-shoulder transition, and shoulder width alone isn't ancestry: broad shoulders can have gracile joints, and narrow shoulders a robust structure. The neck keeps absolute length, length relative to torso, circumference, skeletal structure and muscular development separate. Aelari ancestry may raise proportional neck contribution and Skarn ancestry structural neck presence and neck Muscular Development Capacity (never current neck muscularity), which are different tendencies, never one "neck size" control. **Pelvis:** humans and elves have different pelvic foundations and the shared elven pelvis is unresolved, so only the principle is locked: **the Halvren pelvis is a developmentally viable mixed structure, not a linear morph between stock human and stock elven pelvis geometry.** Detailed pelvic inheritance is OPEN, requiring prototypes and further anatomical design.

## 20–26. Limbs, joints, hands and feet

Arms and legs may express ancestry through total limb contribution to height, upper-arm, forearm, femur and lower-leg contribution, long-bone gracility and joint scale. Segments needn't share one ancestry strength, but coupling keeps transitions coherent.

| Area | Example valid relationships (not templates) |
| --- | --- |
| Arms (§21) | Human-like total arm length with a greater Fenn-like forearm share; moderately elongated Aelari-influenced arms with more human structural presence; Vael-influenced moderate elongation with a stronger wrist transition; Skarn-influenced structural mass with moderate elven elongation |
| Legs (§22) | Human-like femur relationship with a greater Fenn-like lower-leg share; Aelari-influenced overall elongation moderated by human ancestry; Vael-influenced balanced segments with more structural presence; Skarn-influenced robustness with restrained elven elongation |

Joints (shoulders, elbows, wrists, hips, knees, ankles) bridge connected long bones coherently and respond to connected anatomy. It fails if a highly gracile long bone connects through an implausibly massive joint just because two ancestry values were inherited independently. Hands vary in absolute length, length relative to forearm and body, palm breadth and length, finger length and proportions and wrist presence, never one "hand size" parameter: the human family gives broad human variation, Fenn greater elongation and narrowness, Aelari long hands and fingers within vertical anatomy, Vael moderate elongation with broader palms and stronger hand-base presence, and Skarn greater structural scale and robustness, all overlapping. Feet vary in absolute length, length relative to leg and body, breadth, skeletal depth, toe relationships and ankle-foot transition, never one "foot size" scalar. Halvren stay humanoid, and no current source creates prehensile feet, claws or animal feet.

## 27–31. Frame, composition, mass and expression

Narrow, Balanced and Broad remain **Frame Presets, not ancestry categories**: a Broad Halvren isn't automatically human-leaning and a Narrow one isn't automatically elf-leaning. Two Broad Halvren may differ, one with broad skeletal breadth and relatively gracile elven joints and another with broad breadth and more human-family structural presence, so ancestry is never encoded into the presets. Physical composition (muscle amount, body-fat amount and distribution, regional development) stays fully separate from skeletal inheritance, with no stereotype shortcuts: elven expression isn't lean, human expression isn't heavier, Skarn ancestry isn't muscular, Aelari ancestry isn't thin, Vael ancestry isn't dense, and Fenn ancestry isn't athletic. Visual mass comes from height, frame, skeletal structural presence, muscle, fat and regional composition, never one ancestry-dependent scale. The body is never conceptualized as "62% human body, 38% elf body": it holds multiple correlated expression domains, and even if a future system tracks ancestry influence for generation, final anatomy is stored as a coherent anatomical state.

## 32–36. Boundaries and validation

**Phenotypic boundary protection:** ancestry controls can't simply recreate another playable race. A Halvren may strongly resemble a source population, and that's valid, but the complete configuration stays inside the Halvren envelope. Not every feature must look intermediate, and the whole system is evaluated.

| Test | Requirement |
| --- | --- |
| Source-passing | Generate Halvren near expression boundaries, hide ears, neutralize pigment, remove hair and cultural cues, match height and composition, and compare with the relevant source populations. Some hard-to-classify individuals are fine, but systematic exact duplication means the mixed-ancestry constraints are too weak |
| Mixed silhouette | At matched height, frame, muscle, fat and age against Marchfolk, Skarn, Sagekin, Fenn, Aelari and Vael, Halvren show a broad mixed distribution, not one mandatory silhouette |
| Equal height | Height isn't the primary ancestry signal. A tall Marchfolk, a short Skarn, Fenn, Aelari, Vael and Halvren at overlapping heights still differ anatomically where their biology calls for it |
| Extreme combinations | Very tall with Narrow or Broad, short with Broad or Narrow, high muscle with a gracile skeleton, high fat with elven-leaning skeleton, low fat with human-leaning robust skeleton, Skarn structure with Fenn extremities, Aelari verticality with human structure, Vael thoracic depth with gracile limbs. Reject only invalid combined anatomy, never combinations that are just uncommon |

## 37–41. World, equipment, animation, gameplay and architecture

World validation covers the full approved Halvren envelope: doors, ceilings, stairs, ladders, chairs, beds, tables, counters, tunnels, interactions, cameras, equipment, weapons, mounts, collision, navigation, animation and IK, and prototype limits don't redefine anatomy. Equipment accommodates height, shoulders, torso, limbs, hands, feet, frame and composition without uniform scaling by height or ancestry. Movement follows final anatomy (limb and torso proportions, structural presence, joints, height, mass distribution), not a generic "half-elf animation style." Halvren aren't automatically graceful, agile, light-footed, fast, diplomatic-looking, or more human or elven in body language, and body language stays separate from anatomy. Anatomy never converts directly to stats: Skarn ancestry doesn't grant Strength, Fenn ancestry Stealth, Aelari ancestry Wisdom or Magic, Sagekin ancestry Intelligence, or Vael ancestry low-light bonuses, all pending the Race to Biology to Gameplay Attributes Review. Technical architecture stays OPEN (one or multiple skeletons, shared hierarchy, dedicated Halvren skeleton, procedural bone proportions, morph targets, custom meshes, MetaHuman, modified MetaHuman, retargeting, hybrids). The approved body system is the requirement.

## 42–43. Part 2 decisions and status

First-pass approved: Halvren have their own mixed-population envelope; the provisional height range is **152–213 cm (5'0"–7'0")** with reference **about 178 cm (5'10")**; height is ancestry-informed, not ancestry-locked; Halvren occupy a mixed human and elven skeletal developmental space; gracility and robustness are multidimensional, not one slider; torso inheritance is population-aware; shoulder inheritance is multidimensional; exact pelvic inheritance is unresolved; limb segments may express ancestry differently but stay coupled; hands and feet need multidimensional inheritance; Narrow, Balanced and Broad are frame presets, not ancestry categories; composition is independent of ancestry; exact source-race duplication is prevented at the system level without demanding visible hybridity from every individual; movement follows final anatomy; and gameplay consequences are OPEN. **Halvren v1.0 Part 2 is complete**, and v1.0 as a whole isn't.

# Part 3 Craniofacial anatomy, eyes and mixed external-ear inheritance

## 1–4. Core facial rule and mixed foundation

> **A Halvren is not a human face with pointed ears.**

With ears hidden, pigmentation neutralized, hair removed and cultural presentation removed, the system must still be able to produce faces that plausibly express mixed human and elven ancestry. Not every Halvren must look obviously mixed at a glance, and subtle expression is valid. Halvren craniofacial anatomy occupies a developmentally coherent mixed space between human-family and elven-family architecture, covering cranium, forehead, brow, orbits, external eye anatomy, cheeks, midface, nose, mouth and lips, jaw, chin and ears, with no single interpolation value for the whole face.

Expression is **regional but coupled.** One Halvren might have stronger elven cranial and orbital relationships, a more human-like nose, an intermediate midface, more human-like mandibular mass and strongly elven ears, and another a different combination. That's valid as long as the face stays developmentally coherent, never a patchwork of disconnected source-race face parts. There's **no single Halvren face**: no mandatory face length or width, eye shape, nose, cheeks, jaw, chin, lips, ear length or beauty standard. Broad, narrow, long and compact faces, strong and light jaws, large, small, broad and narrow noses, soft and rugged features, asymmetry and aging are all supported.

## 5–10. Source-population facial contributions

Human-family ancestry contributes the established Marchfolk, Sagekin and Skarn craniofacial distributions, never collapsed into one "human face": Marchfolk give broad human variation, Sagekin their population-level facial tendencies, and Skarn greater craniofacial structural presence where the Skarn spec supports it. None of this means personality, intelligence or culture. Elven ancestry contributes the shared elven craniofacial family from the Elf Comparative Review (cranium, forehead, brow and orbits, midface, cheeks, nose, jaw and chin, external eye presentation, ears), and no single feature defines elven ancestry.

| Ancestry | May contribute tendencies toward | Never translated into |
| --- | --- | --- |
| Fenn (§7) | More compact facial relationships, more open visible orbital and eye presentation than Aelari and Vael populations, somewhat reduced lower-face structural mass, distinct cheek placement, relatively light mandibular presence within the elven range | A childlike, cute or feminized face, huge eyes, a tiny jaw, mandatory beauty |
| Aelari (§8) | Greater facial verticality, longer forehead-to-chin, somewhat narrower lower face, more vertically oriented midface, relatively light mandibular presence, longer and narrower visible eyes than Fenn | An aristocratic face, perfect symmetry, a tiny nose, mandatory beauty, an aloof expression, feminized anatomy |
| Vael (§9) | Less facial elongation than Aelari, more compact craniofacial vertical distribution, stronger midface integration, somewhat broader cheeks and orbits than Aelari, somewhat more mandibular presence than Fenn and Aelari, still elven | A permanent scowl, villainous features, gauntness, a predatory expression, mandatory sharpness |
| Skarn (§10) | Where the Skarn spec establishes it, a probability shift toward more craniofacial structural presence: brow structure, jaw presence, cranial and facial skeletal robustness, neck-head integration | A required square jaw, heavy brow, large nose, angry expression or masculinized look. A tendency is never a mandatory phenotype |

## 11–14. Cranium, brow, orbits and eyes

Cranial inheritance covers cranial height, length and breadth, cranial-to-face relationship and forehead relationships, shifted by specific ancestry, never a "human skull to elf skull" slider. Four eye-area systems stay separate and are never one "eye" control: **brow structure** (skeletal anatomy around the orbit), **orbital anatomy** (skeletal socket relationships), **external eye anatomy** (visible lids and opening) and **ocular anatomy** (the eye itself). Elven ancestry doesn't automatically mean larger eyeballs or openings, upturned or almond eyes, or glowing eyes. Fenn ancestry may raise the probability of a more open visible eye presentation, Aelari ancestry a longer and narrower one, Vael ancestry its established orbital and cheek relationships, and human ancestry may moderate or combine with these. Personality is never encoded into eye anatomy: Halvren don't automatically look mysterious, sad, wise, seductive, alert, suspicious or gentle. Neutral anatomy stays neutral, and expression belongs to animation and emotional state.

## 15–20. Midface, nose, jaw, chin, mouth and asymmetry

| Region | Inheritance may involve | Rule |
| --- | --- | --- |
| Midface and cheeks | Midface height, breadth and projection, cheek breadth and placement, orbital-cheek integration | "High cheekbones" isn't a universal mixed-elf marker, and each source population stays able to influence these |
| Nose | Nasal root, bridge height and width, length, projection, tip, alar width, nostrils | No universal "half-elf nose" (small, narrow, straight, delicate or upturned), and source frequencies follow their own specs |
| Jaw | Mandibular breadth, ramus relationships, mandibular body mass, jaw angle, lower-face height | Elven ancestry may lower average apparent mandibular mass relative to robust human populations such as Skarn, but strong jaws are valid. Vael ancestry (more presence than Fenn and Aelari ancestry) and Skarn ancestry (a human-family mechanism) can both give stronger jaws, and they aren't treated as the same mechanism |
| Chin | Width, height, projection, shape, independently variable within compatible relationships | No required pointed elf chin, square human chin or intermediate half-elf chin |
| Mouth and lips | Mouth width, lip volume, upper-lower lip relationship, philtrum, projection | No mandatory Halvren morphology, and lips are never a simplistic ancestry marker |
| Asymmetry | Brow, eyes, cheeks, nose, mouth, jaw, chin, ears | Natural asymmetry is supported, and mixed ancestry never produces deformity or exaggerated asymmetry, since it's normal viable biology |

## 21–32. External ears

> **Halvren ears are not human ears with a pointiness slider.**

Human and elven ear architectures differ at the foundation, so inheritance accounts for the whole ear. Human-family ancestry contributes the human auricular root and base, helix, antihelix, concha, tragus and antitragus, lobe, and human projection, curvature and vertical orientation ranges, with broad human variation. Elven ancestry contributes the shared non-human foundation from the Elf Comparative Review, with length, base width, tip length and sharpness, vertical angle, sweep, lateral projection, curvature, lobe and skull-root integration as separate variables. Example mixed ears (not fixed packages): mostly human length with subtle elven taper; moderate elongation with human-like projection; stronger elven length with a broader human-influenced base; a short elven-derived ear that's still visibly non-human up close; a more human-like lobe with otherwise mixed structure. Ear parameters are coupled, so extremes combined (a very narrow human-like base with extreme elven length, projection and sweep) may be implausible and need relationship-aware constraints.

| Ancestry | May raise the probability of | Guard |
| --- | --- | --- |
| Fenn | Greater lateral projection from the skull than Aelari and Vael ancestry, rearward sweep, population-specific length and shape | Projection and sweep stay separate, and Fenn ancestry isn't just sideways ears |
| Aelari | More upward and backward orientation, relatively low lateral projection, moderate-to-long length, gradual taper | Overlaps Vael on projection, with no strict Aelari-Vael ranking |
| Vael | Broader ear base, lateral and backward orientation, moderately shorter taper than Aelari, stronger skull-root integration | No bat-like, monstrous or mandatorily short ears |

**Ear length isn't a genealogy meter.** A Halvren with substantial elven genealogy may have subtle ears, and one with less recent elven genealogy may inherit conspicuous ears, so no ancestry percentage is inferred from ears. Natural left-right variation in length, angle, projection, curvature and lobe stays separate from damage such as tears, cuts or missing tissue. **Ear mobility is OPEN**: Halvren ears aren't assumed mobile, elven mobility is unresolved, and if it's established later, inheritance sets musculature and range rather than an animation toggle. **No automatic enhanced hearing:** ear shape alone doesn't set hearing range, sensitivity, directional advantage or perception bonuses, which need later biological review.

## 33–37. Ocular biology, iris, facial hair and aging

Halvren ocular anatomy may eventually express mixed inheritance, but pupil morphology, retinal differences, low-light sensitivity, color perception, reflective structures and daylight response aren't finalized, since shared elven ocular physiology is partly unresolved. Vael low-light adaptation stays a candidate inherited system, so Vael ancestry doesn't automatically give glowing eyes, slit pupils, eyeshine, giant eyes, night vision or daylight weakness, pending Vael ocular design and later inheritance review. The biological iris (inherited anatomy and pigmentation) stays separate from magical or supernatural eye effects, and Halvren ancestry doesn't produce glowing or magical eyes. Facial-hair biology will follow ancestry distributions, without assuming elves can't grow facial hair, Halvren always have sparse facial hair, or human ancestry dominates, with exact distributions unresolved where not specified. Halvren faces visibly age (skin elasticity, facial volume, eye region, cheeks, jawline, neck, hair density and pigmentation, ear tissue where appropriate) and are never permanently youthful. The exact aging rate is OPEN.

## 38–44. Face presets and validation

Future face presets show broad mixed expression: subtle mixed expression; strong human-family craniofacial expression with clearly mixed ears; strong elven craniofacial expression with subtle ears; broad or robust and light or gracile mixed faces; Fenn-, Aelari-, Vael-, Skarn- and Sagekin-influenced mixed faces; and elder Halvren. They're creator starting points that don't define genealogy.

| Test | Requirement |
| --- | --- |
| Hidden-ear (permanent) | Across the valid distribution, with ears hidden, hair removed, pigment neutralized, neutral expression and standard lighting, the system still produces plausible mixed human and elven craniofacial anatomy. It fails if every Halvren becomes indistinguishable from Marchfolk |
| Ear-only | With face, pigment, hair and presentation neutralized, Halvren ears show mixed variation against Marchfolk, Fenn, Aelari and Vael, never one midpoint ear, random human ears with pointed tips, or unrestricted copies of every source ear |
| Equal face structure | At comparable height, age, frame, composition, pigmentation and hair, cranial relationships, orbits, midface, nose, jaw, chin and ears are compared with source populations, and no single feature carries all ancestry readability |
| Strong-expression stress | Near source boundaries (strong Fenn face with subtle ears, strong Aelari face with human-like ear length, strong Vael midface and jaw with moderate mixed ears, strong Skarn facial structure with strongly elven ears, strong Sagekin influence with elven orbits), mosaic expression works without patchwork |
| Anti-beauty | It fails if large populations systematically get more symmetry, smoother skin, smaller noses, narrower jaws, larger eyes, younger apparent age or more conventional attractiveness. Mixed ancestry isn't a beauty filter |
| Anti-generic-half-elf (permanent) | It fails if random Halvren keep converging on a human face, slightly narrow jaw, slightly larger eyes, small straight nose, perfect skin, young age, thin body, medium-length pointed ears, long hair and conventional attractiveness |

## 45–47. Technical, creator and source-race protection

Technical architecture is OPEN: shared or multiple topologies, morph targets, bone-driven or procedural deformation, dedicated Halvren head meshes, source-population morph spaces, MetaHuman-derived, custom or hybrid systems, with nothing chosen now. Advanced Mode exposes facial customization without requiring genetics, possibly organized as face preset, overall facial relationships, brow and orbit, eyes, cheeks and midface, nose, mouth, jaw and chin, ears and asymmetry, with ancestry-aware constraints underneath. Not every internal inheritance variable is exposed just because it exists. A Halvren may strongly resemble any source population, which is biologically acceptable, but the system shouldn't give an unrestricted way to exactly recreate another population's complete craniofacial distribution, judged on the whole face, not one trait.

**Classification (race-specific facial-control organization status):** the possible Advanced Mode facial organization above (face preset, overall relationships, brow and orbit, eyes, cheeks and midface, nose, mouth, jaw and chin, ears, asymmetry) and any other creator-facing facial structure in Halvren v1.0 are **APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION.** Halvren facial anatomy, inheritance rules, validation and required capability stay approved, and only the final control organization waits for the Universal Facial Customization Architecture Review after all 13 first-pass races are complete.

**UFCA status (UFCA Phase 2, October 5, 2026):** the universal facial creator organization is now canonical in `decisions/UFCA_V1.md`. The Halvren facial control organization in this spec stays as approved requirements and is routed to its UFCA slots (`reviews/claude-ufca-08-phase1-architecture-audit.md` Appendix A); Halvren anatomy, tendencies, validators, tests and OPEN items are unchanged. "Overall relationships" maps to UFCA slot 1 (facial soft tissue); no broad relationship tools exist in v1 (UFCA AD-U3). Genealogy, ancestry-derived constraints and phenotype follow UFCA §11, consistent with the critical system distinction in the consistency resolution below.

## 48–49. Part 3 decisions and status

First-pass approved: genuine mixed human and elven craniofacial anatomy; regional but developmentally coupled inheritance; no single Halvren face; distinct human and distinct elven source populations; brow, orbit, external eye and ocular anatomy as separate systems; broad nasal diversity; multidimensional jaw and chin inheritance; genuine mixed ear anatomy, never a pointiness slider, with relationship-aware parameters; ear length isn't an ancestry percentage; ear mobility, hearing and Vael-derived low-light physiology are OPEN; biological iris stays separate from magical effects; Halvren visibly age, with the exact aging rate OPEN; and the hidden-ear and anti-generic-half-elf tests become permanent validation concepts. **Halvren v1.0 Part 3 is complete**, and v1.0 as a whole isn't.

# Part 4 Pigmentation, hair, iris and mixed-ancestry appearance inheritance

## 1–3. Core pigmentation rule and layers

> **Mixed ancestry does not mean averaging two RGB values.**

Halvren skin, hair and iris pigmentation are inherited biological expression, never a blend of two source populations' visible colors. Inheritance works through meaningful appearance parameters and population distributions. Skin is multidimensional, never one color value: pigmentation amount and distribution, undertone, perfusion, local and regional variation, surface and translucency relationships where technically appropriate, and age and environmental effects. The shader is OPEN. The four Skin Appearance Layers stay separate: **Natural** (inherited and developmental), **Environmental** (tanning, weathering, exposure), **Applied** (tattoos, cosmetics) and **Acquired** (scars, acquired markings). Mixed ancestry mainly affects the Natural layer, and tattoos, cosmetics and scars are never genetically inherited.

## 4–8. Source pigmentation contributions

| Source | Skin families | Undertones | Guard |
| --- | --- | --- | --- |
| Human family (Marchfolk envelope, with Marchfolk, Sagekin and Skarn distributions later) | Very light or fair, light, intermediate, olive, tan and bronze, brown, deep or dark brown | Cool, neutral, warm, golden, olive, reddish where appropriate | Exact frequencies are population-specific or OPEN |
| Fenn (corrected spec) | Fair or light, beige and tan, olive, copper and bronze, brown, rich deeper brown | Cool, neutral, warm, olive, golden, reddish or copper where appropriate | Never universally tan, brown, olive, bronze, warm-toned, green or "forest colored" |
| Aelari | Very light or fair through intermediate into deeper brown | Cool, neutral, warm, golden, olive, reddish where appropriate | Overlaps heavily with Fenn, so complexion alone needn't distinguish them |
| Vael | Charcoal, slate, cool, neutral and warm gray, blue-gray, muted or desaturated violet, ash-brown, desaturated brown, related grounded variants, with real light-to-dark variation | — | Vael ancestry never means dark skin |

**Vael pigmentation in Halvren** is never color blending: human warm brown plus Vael blue-gray doesn't make an arbitrary purple-brown midpoint. Inheritance affects separate underlying dimensions, so a Halvren with Vael ancestry might show mainly human-range pigmentation with subtle cool or desaturated undertones, ash or desaturated brown, gray-brown relationships, more visibly Vael gray or slate moderated by other ancestry, little obvious Vael pigmentation despite substantial Vael genealogy, or strong Vael pigmentation despite distant Vael genealogy. Exact probabilities are OPEN.

## 9–16. Latent ancestry, living skin, lighting and frequency

**Ancestry can be visually latent (locked).** An ancestry contribution needn't show in every domain: a Halvren may have Vael ancestry without gray skin, white hair or violet eyes, Fenn ancestry without bronze or tan skin, or Aelari ancestry without fair skin. Phenotype isn't a genealogy report. Across generations, traits may be weak in one generation, strong in another, or appear in combinations not visible in either parent, without literal genetic rules yet: **inheritance must support non-midpoint multigenerational expression.** There's **no default Halvren complexion**, and it fails if Halvren keep converging on light tan, beige, olive, "halfway gray" or one fantasy mixed-race complexion.

Every Halvren's skin reads as living tissue (perfusion, local redness, regional pigment, lip, eye-region and ear coloration, palm and sole relationships where appropriate, freckles, moles, birthmarks or setting equivalents, age and environmental changes), and unusual pigmentation is never flat painted material. Lighting invariance holds: stored pigmentation doesn't change under sun, shade, overcast, firelight, moonlight, cave or magical light, since lighting only changes the rendered observation. Pigmentation is judged under neutral reference light first, then warm, cool, daylight, overcast, firelight, low and magical light, which matters most for subtle Vael-derived pigmentation. Validity isn't frequency: manual creation generally allows valid rare traits, while random generation follows population frequency, with exact Halvren frequencies OPEN. Soft probabilistic correlations are allowed where justified, never rigid packages (gray skin, white hair, violet eyes; fair skin, blond hair, blue eyes; bronze skin, dark hair, green eyes) unless a specific biological mechanism requires it.

## 17–24. Hair

**Hair biology** (natural pigmentation, texture, density, hairline, growth, age changes) stays strictly separate from **hair presentation** (length, cut, styling, shaving, braiding, ties, accessories, cultural grooming), and hairstyles are never genetically inherited. Human-family ancestry supports black, dark brown, brown, light brown, blond, auburn and red, and related intermediates, with straight, wavy, curly and coiled textures. Elven populations also support broad variation, with no Aelari-straight-blond-or-silver, Fenn-brown-wavy or Vael-white stereotypes, though population frequencies may differ later. Where valid, **inherited natural silver or white hair stays separate from age-related depigmentation**: a young character can have inherited light, silver or white hair without being old, an older character can depigment regardless of ancestry, and the two aren't stored as the same state. Hair color inheritance never averages parental or source colors, and multigenerational expression may allow dark hair despite a light-haired parent, light hair reappearing after weak expression, auburn or red from inherited combinations, and natural silver or white where ancestry supports it (model OPEN). Texture is inherited biology, never a midpoint, and hairstyle availability isn't tied to texture unless technically necessary: presentation accommodates biology, never redefines it. Density, hairline shape, age thinning and individual variation apply, and elven ancestry doesn't mean universally thick, perfect or youthful hair. Facial hair depends on population inheritance, with no assumptions that Halvren can't grow it, elven ancestry always reduces it, human ancestry always dominates, or density reveals ancestry percentage.

## 25–31. Iris, pupils and magical eye effects

Iris inheritance is independent of orbital anatomy, external eye anatomy, pupil morphology, ocular physiology and magical effects, drawing from valid human and elven distributions.

| Source | Iris families | Rule |
| --- | --- | --- |
| Human family | Dark brown, brown, hazel-like, amber where appropriate, green, gray, blue, related intermediates | Frequencies population-specific or OPEN |
| Elven family (Elf Comparative Review) | Brown, dark brown, amber, hazel-like, green, gray, blue, blue-gray, green-gray, muted violet, other approved grounded variants | Not every color equally common in every elven population |
| Vael ancestry | Brown, amber, hazel-like, gray, blue-gray, green-gray, muted violet, very dark | Vael ancestry doesn't require unusual iris color, and unusual color doesn't prove recent Vael ancestry |

Iris colors are never averaged: a blue-eyed human and a muted-violet-eyed elf don't automatically produce blue-violet, with dominance and polygenic rules OPEN. Pupil morphology is OPEN, never tied to iris color and never made exotic just for distinctiveness, with round pupils a valid conservative candidate. Magical effects (luminescence, glow, arcane coloration, supernatural overlays, temporary magical changes) are completely separate, never inherited iris traits, and never overwrite the underlying biological eye data.

## 32–36. Natural marks, scars, tattoos, environment and geography

Freckles, moles, birthmarks and setting-appropriate natural markings belong to natural appearance where appropriate, without genetic simulation, and aren't ancestry labels. Scars are acquired, never inherited: presets may include them for inspiration, but they stay separate from ancestry generation. Tattoos and cosmetics are Applied and may communicate culture, religion, community, profession, taste or history, but not biological ancestry unless a society uses them symbolically, and they're never auto-applied by ancestry. Environment (sun, weathering, dryness; scarring is Acquired) may change appearance, so a surface-raised and a subterranean-raised Vael-descended Halvren can differ environmentally despite similar ancestry, but environment doesn't rewrite genealogy. Regional Halvren trait frequencies over generations (founder populations, migration, isolation, intermarriage patterns, local human and elven populations) are **OPEN, future population design.**

## 37–40. Creator, ancestry controls, selective randomization and determinism

Players never manipulate melanin genes, alleles, dominance tables, loci or molecular biology. The system may be ancestry-aware underneath while offering intuitive controls such as skin, undertone, hair pigmentation, hair texture, iris pigmentation and natural markings (UI OPEN). **Ancestry controls never become color locks:** more Vael ancestry doesn't slide skin toward gray, more Aelari ancestry toward pale, or more Fenn ancestry toward bronze, since ancestry changes distributions and compatibility, not one deterministic color target. Selective randomization covers pigmentation, hair biology, iris or natural markings only, while preserving anatomy, ancestry history where applicable and selected traits, respecting validity and correlations. Biological randomization is reproducible where save and load, NPC persistence, testing, networking or bug reproduction need it (implementation OPEN).

## 41–52. Validation, siblings and family resemblance

| Test | Pass or fail condition |
| --- | --- |
| Population sampling | Pigmentation is never judged from a few presets. Large generated populations are checked for pigmentation breadth, hair and iris variation, frequencies, correlations, rare traits, accidental stereotypes and source convergence, since population identity is statistical |
| Vael mix | Fails if known-Vael-ancestry Halvren keep converging on gray skin, white or silver hair and violet eyes, or get arbitrary blended fantasy colors with no biological logic. Expect subtle, moderate and strong Vael-derived expression |
| Fenn mix | Fails if Fenn-descended Halvren keep converging on tan or bronze skin, brown hair and green eyes, and the corrected broad Fenn range is kept |
| Aelari mix | Fails if Aelari-descended Halvren keep converging on pale skin, blond or silver hair and blue eyes |
| Human mix | Fails if human ancestry always acts as a generic beige or brown "normalizer" pulling unusual elven pigmentation to a midpoint. Human ancestry isn't a neutral color value |
| Pigmentation neutralization | With skin, hair and iris normalized, the Part 2–3 anatomical inheritance still reads. Different valid pigmentation on similar anatomy changes appearance without rewriting skeletal ancestry |
| Hair neutralization | With hair removed or standardized, the face still works. It fails if ancestry or identity depends mainly on stereotypical hairstyles or colors |
| Lighting stress | Under neutral, warm and cool daylight, overcast, firelight, low-light interiors, moonlight and magical light, unusual pigmentation stays living skin, never paint, stone, plastic or emissive |
| Anti-exoticism | Fails if randomization over-selects unusual traits (violet eyes, silver hair, gray skin, extreme ears) to advertise mixed ancestry. Mixed ancestry isn't "maximize exotic traits" |
| Anti-midpoint | Fails if first-generation and multigenerational skin, hair, iris or undertone always sit halfway between sources. Inheritance gives a distribution, not a midpoint algorithm |

**Sibling test (future requirement):** siblings sharing ancestry may differ substantially in pigmentation, undertone, hair, iris, face, ears and body proportions while keeping plausible family resemblance, with the family-generation system OPEN. **Familial resemblance principle:** if the game ever generates relatives, inheritance supports shared family resemblance without cloning, through correlated face, body, pigmentation, hair, eye and ear traits. This is recorded as a future requirement, not solved technically now.

## 53–55. Aging, lifecycle and technical architecture

Inherited pigmentation and aging interact without becoming one system: hair depigmentation and thinning, skin changes and local pigment changes don't rewrite ancestral pigmentation. Since human and elven lifecycles are partly unresolved, chronological age is never inferred from appearance alone, and chronological age, apparent biological age and age presentation stay distinct, which matters especially for Halvren. Shader, texture, material-layer, morph, hair-system, eye-shader, genetic-simulation and randomization architecture are all OPEN, and the approved biological behavior is the requirement.

## 56–57. Part 4 decisions and status

First-pass approved: pigmentation is inherited biological expression, not RGB interpolation; skin is multidimensional; Natural, Environmental, Applied and Acquired layers stay separate; human, Fenn, Aelari and Vael distributions are distinct inputs; Vael ancestry supports subtle through strong expression without forced gray skin; ancestry may be visually latent; multigenerational traits may reappear without midpoint behavior; there's no default Halvren complexion; living-skin variation is required; biology stays separate from lighting; validity and frequency stay separate; hair biology and presentation stay separate; hair color and texture are inherited without midpoint averaging; natural silver or white hair stays separate from aging; iris stays separate from eye anatomy, pupils and magic; magical eye effects stay separate from biology; geographic subpopulations are future design; large population sampling is required; and sibling variation and familial resemblance are future inheritance requirements. **Halvren v1.0 Part 4 is complete**, and v1.0 as a whole isn't.

# Part 5 Lifecycle, culture separation, presets, randomization, validation and technical handoff

## 1–8. Population, fertility, identity and culture

> **Halvren must function biologically as a sustainable mixed-ancestry population, not as one fixed hybrid template.**

Halvren include first-generation individuals, multigenerational and long-established families, Halvren communities, and people with recent human, recent elven or many-generation mixed ancestry. **First-pass setting assumption:** Halvren are biologically viable and can have descendants (human plus elf, Halvren plus human, Halvren plus elf, Halvren plus Halvren, and more complex combinations), not inherently sterile, with reproductive biology out of scope and no chromosome or genetic pseudo-detail. "Halvren" never automatically means 50% human and 50% elf: the name may have historical, cultural, linguistic, legal or social origins that aren't genetic math, and its lore origin is OPEN.

**Biological mixed ancestry** (inherited human and elven ancestry) is separate from **Halvren social identity** (whether the character or society calls them Halvren). They may overlap strongly but aren't identical, and who calls themselves Halvren, who societies consider Halvren, whether some mixed people identify primarily with another population, and whether cultures use different terms are lore questions, never answered by anatomy. **No mandatory Halvren culture (locked):** a Halvren may be raised in Marchfolk, Skarn, Sagekin, Fenn, Aelari or Vael society, a mixed or Halvren-established community, another regional culture or a multicultural environment, and culture is chosen or generated separately from ancestry. Long-established Halvren communities can still develop traditions, dialects, architecture, clothing, cuisine, art, family structures, social, religious and political institutions and shared historical identity, which come from history and community, not biology, with specific cultures left to future worldbuilding. Ancestry never assigns diplomacy, charisma, adaptability, curiosity, restlessness, alienation, internal conflict, social skill, rebelliousness, empathy, wisdom or intelligence. **"Caught between two worlds" isn't required:** a Halvren may be secure, rooted in one or several cultures, raised among Halvren, uninterested in or fascinated by ancestry, accepted or marginalized, famous or ordinary, and social conflict is never a racial requirement.

## 9–12. Lifecycle

Halvren visibly mature, age and grow older, never permanently youthful. Lifecycle timing is OPEN because human and elven rates are unresolved, and there's no arithmetic-midpoint lifespan. Chronological age, apparent biological age and age presentation stay distinct. Future lifecycle design decides how ancestry affects maturation, adult aging, senescence, hair and skin changes, facial volume, skeletal aging, fertility where relevant and maximum lifespan, without assuming every property inherits at the same strength, since lifecycle may involve several correlated systems. **No lifespan percentage slider:** 60% elven ancestry never means 60% of the human-to-elf lifespan difference, since lifecycle inheritance may be nonlinear, with the mechanism OPEN.

## 13–16. Presets

Character presets are legitimate outputs of the same system as customized characters, with no hidden geometry, preset-only morphs, impossible ancestry combinations or rules unavailable to players.

| Code | First-pass preset target |
| --- | --- |
| A | Subtle mixed expression, not immediately obvious |
| B | Strong human-family expression with coherent elven contribution |
| C | Strong elven-family expression with coherent human contribution |
| D | Broad and structurally strong, showing Halvren aren't universally thin |
| E | Heavyset, valid higher body fat |
| F | Lean, without implying stronger elven ancestry |
| G | Elder, visible aging |
| H | Multigenerational, not reading as an exact first-generation midpoint |
| I | Skarn-influenced: more structural presence without becoming a small Skarn |
| J | Fenn-influenced: extremity expression without becoming Fenn with human ears |
| K | Aelari-influenced: vertical influence without the generic tall beautiful half-elf |
| L | Vael-influenced: mixed anatomy and pigmentation without default gray skin, white hair and violet eyes |
| M | Sagekin-influenced: human population influence without scholarship or intelligence stereotypes |

These are validation and preset targets, not fixed subraces. **Choosing a preset never implies genealogy** ("this character had a Skarn father and Aelari mother"), and preset names avoid falsely specifying parentage unless the player deliberately picks a genealogy option in a future ancestry system. Presentation presets (human, elven, Halvren-community, regional, cross-cultural, occupational and personal styles) stay separate and never rewrite ancestry.

## 17–22. Randomization

**Biological randomization** generates anatomy, frame, proportions, face, ears, natural pigmentation, hair biology, iris, natural markings and biological age appearance, ancestry-, population- and relationship-aware and developmentally constrained. **Presentation randomization** separately generates hairstyle, grooming, clothing, cosmetics, tattoos where appropriate, accessories and other presentation, never mixed with biological randomization. Strength modes are **Subtle** (common, central expression), **Diverse** (broader valid distribution) and **Extreme** (uncommon valid combinations near approved boundaries), where Extreme never means deformed, impossible, every slider at maximum or maximum exotic traits. Advanced Mode supports selective randomization (face, body, ears, pigmentation, hair biology or presentation only) with trait locks. When genealogy is set, randomization respects it but still allows multiple valid phenotypes, never one deterministic appearance per ancestry history. Biological generation is reproducible where save and load, NPC persistence, networking, testing, bug reproduction and family generation need it, with the method OPEN.

## 23–45. Permanent validation characters and families

| ID | Purpose |
| --- | --- |
| HV-FAMILY-01 | Several biological siblings from the same parental context, showing shared resemblance with individual face, body, pigmentation, ear, hair and iris differences. Fails if they're clones or look completely unrelated |
| HV-FAMILY-02 | Multigenerational family (older generation, adult and younger adult descendants), validating trait persistence and reappearance, resemblance, non-midpoint inheritance, aging and multigenerational ancestry, with genealogy designed later |
| HV-01 | Strong human expression: strongly human-leaning anatomy, subtle but coherent elven ancestry, ears not necessarily dramatically pointed, no cultural cues, never a literal human preset under another label |
| HV-02 | Strong elven expression with coherent human contribution, never exactly reproducing Fenn, Aelari or Vael anatomy |
| HV-03 | Broad mixed expression across several systems, where "balanced" never means every parameter at 50/50 |
| HV-04 | Subtle expression that may be hard to identify, so Halvren needn't advertise mixed ancestry |
| HV-05 | Stronger elven ears with more human-leaning face (mosaic expression) |
| HV-06 | Subtle ears with stronger mixed or elven face, proving ears aren't the sole marker |
| HV-07 | Broad frame preset with strong structural presence, rejecting the thin half-elf |
| HV-08 | Higher body-fat amount with valid distribution and readable mixed skeleton |
| HV-09 | High muscularity with valid Halvren skeleton, never confused with human or Skarn ancestry |
| HV-10 | Clearly older apparent age, rejecting the permanently youthful half-elf |
| HV-11 | About 152 cm, validating proportions, face, hands and feet, equipment and world, never uniform scaling |
| HV-12 | About 213 cm, same checks, never uniform scaling |
| HV-13 to HV-17 | Fenn-influenced (extremities, face, ears), Aelari-influenced (verticality, neck and torso, face, ears, never a smaller Aelari), Vael-influenced (structure, face, ears, pigmentation, avoiding clichés), Skarn-influenced (structural presence, height tendency, joints, hand and foot scale), Sagekin-influenced (no intelligence, scholarship, frailty or social class) |
| HV-18 to HV-25 | Pigmentation: broad human range, Fenn- and Aelari-influenced, subtle and stronger Vael, natural silver or white hair without old age, unusual but valid iris, strong ancestry with latent pigmentation |
| HV-26 to HV-35 | Face and ear: strong face with subtle ears, subtle face with strong ears, human-like ear length with elven structure, moderate length with high or low projection, Fenn-, Aelari- and Vael-influenced ears, strong and light facial structure, all relationship-aware |
| HV-36 to HV-43 | Composition: Narrow muscular, Narrow heavy, Broad lean, Broad muscular, Broad heavy, tall heavy, short muscular, gracile skeleton with high muscularity |
| HV-44 to HV-48 | Several apparent biological adult ages (chronological mapping unresolved), with systemic aging, not just wrinkles, gray hair or a texture overlay |

## 46–51. Population, ancestry, neutralization and integrity tests

| Test | Requirement |
| --- | --- |
| Random population | Large populations are reviewed for convergence toward human with pointed ears, tall and thin, young, conventionally attractive, pale skin, small straight noses, narrow jaws, long hair, silver hair, unusual eyes or exact 50/50 anatomy |
| Ancestry distribution | Different known ancestry histories change distributions without dictating appearance, different histories can overlap, and similar histories can produce different individuals |
| Source neutralization | With hair, pigmentation, ears, clothing, cosmetics, tattoos and expression removed or standardized, the underlying anatomy is compared with all six source populations to confirm mixed ancestry lives in the anatomy itself |
| Culture neutralization | One biological Halvren wears Marchfolk-, Fenn-, Aelari-, Vael-associated, Halvren-community and neutral traveling presentation, and the biology stays unchanged |
| Preset integrity | Every preset survives Preset, Advanced Mode, Edit, Save, Reload with no hidden geometry, inaccessible values, ancestry corruption, appearance loss or presentation contaminating biology |
| Randomization integrity | Repeated large randomization is checked for validity, diversity, correlations, rare-trait frequency, relationship-aware anatomy, reproducibility and locks, and fails if it's just independent random sliders |

## 52–58. World, equipment, animation and gameplay

The approved Halvren envelope is validated against doors, ceilings, stairs, ladders, chairs, beds, tables, counters, tunnels, interactions, conversation scenes, cameras, equipment, weapons, mounts, collision, navigation, animation and IK, using target anatomy, not just what the prototype can reach. Equipment accommodates height, frame, torso, shoulders, limbs, hands, feet, ears, head shape and hair without uniform scaling, with special attention to helmets, hoods, circlets, earrings, head coverings and hair-ear-headgear interaction. Animation respects final anatomy (height, limb and torso proportions, joints, structural presence, mass distribution), with no universal "half-elf graceful animation set," and culture, occupation, personality and training shape body language separately. **OPEN:** camera, collision, interaction, combat and weapon reach and hit detection (never set automatically by uniform scale), mounts, gameplay attributes (no automatic averaging of human and elven bonuses and no prototype stats inherited by percentage, pending the Race to Biology to Gameplay Attributes Review), and race and class restrictions (never inferred from human or elven ancestry, culture or existing prototype restrictions).

## 59–63. Data, schema and technical authority

Halvren strengthen the need for unified appearance data, which may preserve race, genealogical ancestry context where used, population influences, final anatomy, skeletal frame, physical composition, face, ears, natural pigmentation, hair biology, iris, natural markings, chronological age, apparent biological age and presentation (schema OPEN). **Ancestry data survives appearance editing:** changing appearance never silently rewrites genealogy, and changing genealogy in a future creator never arbitrarily destroys player-made appearance without explicit design behavior, which needs future UX and system design. Appearance data needs schema and version tracking, migration and backward compatibility where practical, especially as inheritance systems evolve. The technical foundation is fully OPEN (modified human or elven foundation, dedicated Halvren foundation, shared hierarchy, multiple meshes, procedural bones, morphs, retargeting, MetaHuman-derived, custom or hybrid). **Approved Design Specification > Open Decision Register > Prototype Implementation:** current limits never redefine Halvren anatomy, design drives technical evaluation, and convenience never silently simplifies Halvren into humans with pointed ears.

## 64–65. Permanent failure and success conditions

| The design fails if the system systematically becomes | The system succeeds when |
| --- | --- |
| Human with pointed ears; generic elf with human coloring; exact 50/50 averages; one fixed body, face or ear shape; one default complexion; one ancestry slider controlling everything; universally attractive, thin, young, graceful or culturally conflicted; disconnected source-race parts; six or more rigid crossbreed subraces | Halvren clearly belong to mixed ancestry; individuals differ substantially; strongly human-leaning, strongly elven-leaning, subtle and multigenerational expression are all valid; sources shape distributions without templates; body, face, ears and pigmentation express ancestry differently; coherence prevents patchwork; culture and composition stay independent; aging is visible; presets use the same system; randomization gives broad valid populations; genealogy and phenotype stay distinct; technical architecture stays subordinate to approved anatomy |

## 66–68. v1.0 decision summary and status

| Area | Approved first-pass design |
| --- | --- |
| Biological identity | Viable mixed human and elven ancestry people |
| Sources | Human: Marchfolk, Skarn, Sagekin. Elven: Fenn, Aelari, Vael |
| Generational model | Not restricted to first-generation 50/50 ancestry |
| Fertility | Multigenerational viability provisionally approved |
| Height | Provisional 152–213 cm (5'0"–7'0"), reference about 178 cm (5'10") |
| Anatomy | Mixed, regional, relationship-aware and developmentally coherent |
| Face and ears | Genuine mixed craniofacial and external-ear anatomy, never a pointiness slider |
| Pigmentation | Inherited multidimensional expression, not RGB blending |
| Hair and eyes | Hair biology separate from presentation. Iris separate from anatomy, physiology and magical effects |
| Lifecycle | Visible aging approved, exact rates unresolved |
| Culture | Separate from ancestry |
| Presets and randomization | Presets from the same system. Randomization ancestry-, population- and relationship-aware |
| Gameplay | No automatic ancestry averaging, future review required |
| Technical architecture | OPEN |

**Keep open (§67), never silently closed:** Halvren lifecycle; human and elven lifecycle numbers; the mixed-ancestry genetic model; genealogy representation; player-facing ancestry UI; inheritance correlations; ancestry population frequencies; regional subpopulations; the social definition and the origin and etymology of "Halvren"; pelvic details; ear mobility; hearing, ocular physiology, Vael-derived low-light inheritance and pupil morphology; hair, facial-hair, pigmentation and iris frequencies; skeleton architecture, MetaHuman suitability, mesh, morph and deformation, animation, IK, equipment fitting, headgear and ear interaction, first-person representation; camera, collision, interaction and combat reach, hit detection and mounts; racial gameplay attributes; race and class restrictions; and networking requirements.

**HALVREN CHARACTER DESIGN v1.0: first-pass biological foundation complete.** The authoritative set is Parts 1–5, preserved together. No UE5 changes, no implementation, and v1.1 isn't begun independently.

# Halvren v1.0 consistency review (findings, now resolved by the consistency resolution patch below)

This reviews Parts 1–5 against Marchfolk v1.0–v1.5 and its resolutions, Skarn, Sagekin, Fenn, Aelari and Vael v1.0–v1.5, the Elf Comparative Review and its clarifications, the universal amendment and the conflict audit. **No blocking issues. There's no direct contradiction with any source spec, and every source trait Halvren cite matches its spec.** The items below are internal tensions and ambiguities.

| # | Category | Finding |
| --- | --- | --- |
| 1 | Direct contradiction (internal, not with sources) | **Skarn muscle.** Part 2 §9 lets Skarn ancestry contribute "greater natural muscle-volume potential," and §18 "structural/muscular neck presence" (both match the Skarn spec's "more natural muscle volume"). Part 1 §21, Part 2 §29 ("Skarn ancestry = muscular" is a stereotype) and Part 5 HV-09 (muscularity never confused with Skarn ancestry) say composition is independent of ancestry. These reconcile only if "potential" means a shifted valid range or distribution, not a default amount, which isn't stated |
| 2 | Ambiguous comparative wording | Unnamed comparison targets: Skarn "greater skeletal robustness," "deeper ribcage," "larger hands/feet" (absolute or proportional?) (Part 2 §9); Fenn "greater skeletal gracility," "shallower ribcage" (§10); Aelari "taller height distribution," "longer average neck contribution" (§11); Sagekin "greater linearity," "longer-limbed," "narrower ribcage" (presumably than Marchfolk) (§14); Fenn "somewhat reduced lower-face structural mass" and Aelari "greater facial verticality," "narrower lower face" (Part 3 §7–8). Also, Part 1 §15 attributes "human skeletal robustness" to the whole human family, while the Elf Review compares elves with "equivalent robust human populations" and Sagekin trend linear, so whether "robust" means all humans or robust human populations is ambiguous |
| 3 | Tendency turned into a hard rule | None found outright. Every source contribution is phrased "may," "tendency" or "probability," and Part 2 §8 uses "should not normally." The closest is item 1, where the Skarn muscle tendency could be read as ancestry setting composition |
| 4 | Genealogy and phenotype conflated | (a) **Preset names.** Part 5 §14 targets I–M ("Skarn-Influenced Halvren" and so on) and Part 3 §38 face presets ("Fenn-influenced mixed face") use source-population names, while Part 5 §15 says preset names should avoid implying parentage. Fine as internal validation labels, but they'd conflict if shown to players as preset names. (b) **"Population-influence controls."** Part 1 §26 lists them as possible Advanced Mode controls, but it isn't said whether they edit genealogy or phenotype. That matters for Part 5 §60, where appearance edits must not rewrite genealogy |
| 5 | Culture and biology conflated | **Which envelope applies.** Part 2 §2 gives Halvren their own biological validity envelope, tied to the race label. Part 5 §4 separates biological mixed ancestry from Halvren social identity. So it's undefined which body envelope applies to a mixed-ancestry character who identifies as, or is played as, Marchfolk or Fenn, or to a mostly-Marchfolk multigenerational character who identifies as Halvren. Otherwise culture and biology stay separate throughout |
| 6 | Height envelope compared with source logic | The 152–213 cm range is intentional (§2, "not the union"), but it has two edge effects. **Lower edge:** Marchfolk reach 147 cm, so a strongly human-leaning or mostly-Marchfolk multigenerational Halvren (HV-01, Halvren plus human lines) can't be as short as the shortest Marchfolk, and no elven source goes below 157 cm. **Upper edge:** Skarn run 183–229 cm (reference 208) and Aelari reach 221 cm. §9 and §5 shift Skarn and Aelari ancestry toward the tall end, so a Skarn-parent Halvren's likely heights crowd against the 213 cm cap. The minimum Skarn (183 cm) is already above the Halvren reference (178 cm). The spec doesn't say whether ancestry-shifted distributions are truncated at the envelope edge or compressed within it |
| 7 | Missing source information that would block parts of v1.1 | (a) Human and elven lifecycle numbers, blocking Halvren lifecycle inheritance. (b) The shared elven pelvis, blocking pelvic inheritance. (c) Elven ocular physiology and the Vael low-light mechanism, blocking ocular inheritance. (d) Elven ear mobility. (e) Skin, undertone, hair and iris frequencies for all six sources: Skarn and Sagekin pigmentation distributions are "to be established later" (Part 4 §4), and Sagekin has only a possible population center. These block randomization weighting. (f) Facial-hair distributions for humans and elves. (g) The Marchfolk hair-texture list: the pre-inheritance resolution lists human hair colors but not textures, while Halvren Part 4 §18 lists straight, wavy, curly and coiled. (h) Vael sun and UV response, which affects the environmental layer for Vael-descended Halvren. (i) The sex-related anatomy system (Part 1 §22). Whether these block v1.1 depends on its scope, but each gates a specific inheritance topic |

**Prototype notes (not changes):** the game's Halvren description, 1.0 scale, Agility- and Dexterity-leaning attributes and class restrictions stay as prototype (no Part 1 notes section is retained; Part 5 §52–58 and §59–63 govern gameplay and prototype authority).

# Halvren v1.0 consistency resolution (pre-v1.1 clarification patch)

This patch applies clarifications to Halvren v1.0 without reopening it: v1.0 stays **first-pass biological foundation complete.** It's design only, with no UE5 changes, and the affected wording in Parts 1–2 is updated in place with a reference back here.

## 1. Skarn muscle: capacity versus current composition (AGREED)

**Muscular development capacity** (the biological range or tendency for how much muscular development an anatomy can plausibly support) is separate from **current muscularity** (present physical composition). Skarn ancestry may shift the valid distribution or upper potential for muscular development, but never automatically makes a Halvren muscular, athletic, strong-looking or trained. A Halvren with substantial Skarn ancestry can have low current muscularity, and one without Skarn ancestry can be highly muscular within their own valid range. Composition stays independent in the sense that ancestry never prescribes current build.

## 2–3. Comparative anatomy normalization and human-family "robustness" (AGREED)

| Term in Halvren design | Normalized meaning |
| --- | --- |
| Skarn "deeper ribcage" | Greater average skeletal thoracic depth relative to equivalently sized Marchfolk |
| Skarn "larger hands/feet" | Greater average absolute skeletal hand and foot dimensions, with proportional relationships also following Skarn anatomy, never one uniform hand and foot scale |
| Fenn "greater gracility" | Greater average skeletal gracility than equivalent Marchfolk and, provisionally, than Aelari and Vael within the elven family |
| Fenn "shallower ribcage" | Reduced average skeletal thoracic depth relative to equivalent Marchfolk and Vael, with no strict Fenn-Aelari thoracic ranking unless already established |
| Aelari "taller" | Population height distribution trends taller than Marchfolk, Fenn and Vael reference populations, with overlapping individuals |
| Aelari "longer neck contribution" | Greater average neck contribution to total vertical body proportion than Fenn and Vael, distinct from absolute neck length |
| Sagekin "more linear" | A tendency toward relatively elongated, less compact human body relationships compared with the Marchfolk reference distribution |
| Sagekin "narrower ribcage" | Somewhat reduced average skeletal ribcage breadth relative to equivalent Marchfolk, not shallow thoracic depth unless separately established |
| Fenn and Aelari face (Part 3) | Keep the Elf Comparative Review reference relationships, and use no unnamed "more, less, larger, smaller, longer, narrower, lighter, stronger" wording where it could be ambiguous |

The whole human family isn't simply "robust" relative to elves. Human and elven families have different skeletal architectures and distributions: some human populations or individuals have much greater structural presence than elven equivalents, but Sagekin may trend linear, Marchfolk span broad variation, and Skarn trend strongly toward structural presence. Generalized "human robustness" becomes **human-family skeletal architecture and structural distributions** where misleading. Elven gracility stays a meaningful family tendency, compared against a named human population or equivalent anatomy where needed.

## 4–5. Labels and ancestry controls (AGREED)

Skarn-, Fenn-, Aelari-, Vael- and Sagekin-Influenced Halvren are **internal validation labels only**, unless a future system deliberately exposes known genealogy, and aren't approved player-facing preset names. Player-facing presets describe appearance (build, silhouette, facial structure, overall visual character) without asserting genealogy, with exact names left to future work. **Critical system distinction:** **A. genealogical ancestry** (actual biological family history), **B. ancestry-derived biological constraints** (the valid distributions that genealogy produces) and **C. phenotypic expression** (actual anatomy and appearance within those distributions). Editing visible phenotype never silently rewrites genealogy, and a control that changes genealogy is never merely an appearance slider. Part 1's "population-influence controls" is reinterpreted accordingly, and future UI clearly separates editing ancestry and history from editing physical expression, with the ancestry UI OPEN.

## 6–9. Biology, playable classification and social identity (locked)

| Concept | Meaning |
| --- | --- |
| Biological ancestry | Which populations contribute to the character's inherited biology |
| Playable biological classification | Which character-creation biological ruleset or envelope builds and validates the character |
| Social or cultural identity | Which population, community or culture the character identifies with or is recognized as belonging to |

These are related but not identical. Selecting **Halvren** means using the approved Halvren mixed-ancestry biological ruleset, not merely "I socially identify as Halvren," and selecting **Marchfolk** currently means Marchfolk biological validation, not just a Marchfolk upbringing. The setting may include people with mixed human and elven genealogy who identify with, or are considered members of, Marchfolk, Fenn, Aelari, Vael or another population. Social identity never erases biological ancestry. Whether a player may pick a non-Halvren ruleset while also specifying mixed genealogy is **OPEN character-creator design**, not solved yet. **Race terminology warning:** "race" currently means biological population, playable creation category, cultural identity and social identity all at once, which will become ambiguous as mixed ancestry grows. A future terminology review may separate species or biological family, population or ancestry, playable lineage, culture and social identity. The current races aren't renamed now.

## 10–14. Height envelope revision

The 152–213 cm range is **no longer an absolute hard biological envelope.** It becomes the **Halvren central population envelope**: about 152–213 cm (5'0"–7'0"), with a provisional central reference around 178 cm (5'10"), describing the expected primary playable and population distribution. Valid ancestry-dependent tails may fall outside it: strong ancestry from shorter human-family distributions may allow some Halvren below 152 cm, and strong Skarn or Aelari ancestry may allow some above 213 cm. These limits are never set by hard clipping, compressing all inherited heights into 152–213, uniform scaling or parental averaging. The conceptual model is **central Halvren distribution plus ancestry-informed probability shifts plus biologically constrained tails**, where 152–213 cm stays the primary first-pass validation range, and exact tail limits and frequencies are OPEN. **Guardrail:** tails don't make any source-race height automatically valid. The mixed developmental system still governs validity, so strong Skarn ancestry may support unusually tall Halvren without authorizing the full Skarn height and structure distribution, and likewise for Aelari or Marchfolk extremes.

| ID | Validation character |
| --- | --- |
| HV-11 | Central short boundary, about 152 cm (renamed from short boundary) |
| HV-12 | Central tall boundary, about 213 cm (renamed from tall boundary) |
| HV-49 | Lower-tail Halvren below 152 cm where ancestry supports it, not automatically a minimum |
| HV-50 | Upper-tail Halvren above 213 cm where ancestry supports it, not automatically a maximum |

Exact tail heights are unresolved until the ancestry-dependent distribution is designed.

## 15–16. Missing source information and the source-first rule

| Class | Items | Handling |
| --- | --- | --- |
| A. Blocks specific future systems, not Halvren v1.1 body refinement | Human and elven lifespan numbers, elven eye biology, Vael low-light mechanism, elven ear mobility, pigmentation, hair and iris frequencies, facial-hair distributions, Marchfolk hair-texture distribution, Vael sunlight response | Stay OPEN until their Halvren subsystem needs them |
| B. Potentially blocks detailed anatomical work | Shared elven pelvic anatomy, the sex-related anatomy system | Never invented inside Halvren. If v1.1 needs either for a definitive rule, that section stops, the dependency is recorded, and only the parts that don't need it continue |

> **Source-first dependency rule (locked, permanent for mixed-ancestry design):** Halvren must not invent missing human or elven biology and then retroactively make that invention canonical for the source populations.

When mixed-ancestry design exposes missing source biology: identify the dependency, return to the relevant source population or family, define the source biology, validate it, then resume Halvren inheritance design.

## 17–18. Status

Halvren v1.0 stays first-pass biological foundation complete, and this is recorded as the **Halvren v1.0 consistency resolution and pre-v1.1 clarification.** No UE5 changes and no implementation. The next step was then Halvren Character Design v1.1 (detailed body proportions and mixed-ancestry morphology); current sequencing is in `specs/STATUS.md`.
