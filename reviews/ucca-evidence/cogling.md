> UCCA Phase 1 evidence appendix to `reviews/claude-ucca-01-requirements-matrix.md`. Line references are to the canonical race spec (or the named source) as of commit 89ca8f7. Extraction only: no canon is changed and nothing here is new biology. Tags: [ANAT] anatomical requirement · [DIR] direct control · [DER] derived/coupled · [SOFT] tendency · [VAL] validator · [LAT] latent/preset · [PRES] presentation · [DIAG] diagnostic · [OPEN] open/not authorized.

# UCCA extraction — Cogling (non-facial / whole-character)

Source: `specs/cogling/COGLING_V1.md` (3245 lines, read fully; status FIRST-PASS COMPLETE L3, L3245; "Implementation: Not authorized" L5). Comparative source: `reviews/short-race-comparative-anatomy-v1.md` (SR-COMP; 274 lines, read fully). Craniofacial anatomy (Part 3, §74–§104) is NOT re-extracted (UFCA-covered, L1566); face items appear only where they touch whole-character systems.

Body identity anchor: **Fine-Scale Elongated Articulation** (§3 L31–35) — "anatomical design terminology, not a creator-facing master slider" (L37). Sequence: "narrow stable central core → near-human total limb contribution → fine limb shafts → within-limb distal redistribution → proportionally emphasized hands/fingers" (L41).

---

## A. Stature and proportions

### A1 Standing height
- [ANAT] Smallest playable humanoid population in current roster (§4 L47).
- [ANAT] Provisional adult envelope: **Minimum ~76 cm / 2'6"; Reference ~91 cm / 3'0"; Maximum ~107 cm / 3'6"** (§4 L53–55). Provisional pending body validation, Short-Race Comparative Review, full-roster world-scale/accessibility validation, camera/collision/interaction review (L57–61).
- [DIAG] Old brief "~0.45× human-height reference is preliminary and non-authoritative" (L49). "No whole-body scale multiplier is authoritative." (L67)
- [ANAT] Intentional Pipkin overlap zone "approximately 91–107 cm"; "not a single-height boundary" (L63); ~91 cm Cogling ref = provisional Pipkin minimum; ~107 cm Cogling max = Pipkin reference (L65). SR-COMP §3 L26–33 restates: Cogling ~76–107 (ref ~91); Pipkin ~91–122 (ref ~107); Durrim ~122–152 (ref ~137); Cogling/Durrim do not overlap; height "cannot be the primary biological discriminator" (L35). Short-race span "roughly 76–152 cm, approximately a twofold difference" (SR-COMP L204).
- [DIAG] Prototype ~0.72× Marchfolk (~125 cm) is PROTOTYPE/NON-AUTHORITATIVE; exceeds Cogling max, overlaps/exceeds Durrim min (~122 cm), above prototype Pipkin (~0.70×/~121 cm) (§31 L443–445; §173 L2668; §207C L3228; COG-WORLD-20 L3078).
- Distribution: SILENT (no frequency distribution given). [OPEN] "exact height distribution and final min/reference/max after world/animation validation" (§207 L3160).
- [DER] Height interaction: range "does not scale every body dimension uniformly"; min/ref/max preserve the same anatomical system with "biologically plausible allometry"; height must not automatically change head size or hand/finger emphasis "by identical percentage", frame, muscularity, fat, sex-related anatomy (§62 L883–893).
- [VAL] Height cannot be implemented as "simple whole-body uniform scale"; must preserve/vary head/body relationships, core, total limb contribution, distal redistribution, hand/finger proportions, joint scale, frame, composition; "Height and body shape are related but distinct" (§175 L2685–2697).
- [ANAT] Age does not change stature beyond plausible age effects; cannot make young adults taller/older dramatically shorter (§123 L1943–1947).

### A2 Torso
- [ANAT] "narrow stable central core" (§6 L98). At normalized displayed height, total torso contribution "remains broadly near the Marchfolk adult range rather than becoming strongly limb-dominant" (L100).
- [ANAT] Core = thorax, spinal trunk, pelvis as integrated adult structure; "comparatively narrow transverse core while retaining sufficient depth and pelvic maturity" (§44 L647–649). "Narrow" = skeletal breadth relationships, not low body fat (L651). "Stable" = coherent structure, not gameplay balance (L653).
- [ANAT] Thorax: fully adult, moderate depth, narrow-to-moderate transverse (L102); §45 L657–661: narrow-to-moderate transverse breadth; moderate adult depth; "clear but not exaggerated ribcage-to-waist transition"; full adult respiratory volume for body size. Must not be flattened, pinched, childlike, Durrim-deep, Gorrund-massive, "or an hourglass device" (L663–669).
- [ANAT] Waist/lumbar: readable transition allowed, "no narrow-waist stereotype is required"; "not a cosmetic cinch point" (§46 L675–677); frame/muscle/adipose/sex anatomy may alter external appearance (L679).
- [ANAT] Axial: no shortened spine, long waist or compressed vertebral column; "Total axial contribution remains adult and broadly balanced with the near-human total limb share" (§49 L705–707).
- [ANAT] Overlap-zone Cogling trait: "adult axial/trunk contribution broadly near the Marchfolk adult range" (§63 L901); SR-COMP-01/02 (L133, L136) require "near-Marchfolk Cogling axial/trunk share versus modestly reduced Pipkin vertical central-trunk share".
- [OPEN] Exact thorax-to-pelvis and torso-to-limb ratios (L110); exact ribcage geometry (L671); thoracic dimensions (§207 L3162).

### A3 Limbs and segment proportions
- [ANAT] Total limb: at normalized displayed height, total arm and leg contribution "remains broadly within the Marchfolk adult envelope"; "Cogling are not defined by greater total limb share" (§38 L558–560).
- [ANAT] Distal emphasis "within a broadly near-human total arm and leg contribution to stature" (§8 L136); population trends: greater forearm share in arm; greater lower-leg share in leg; hands larger share of arm than normalized Marchfolk; fingers long relative to palm; feet supporting distal system "without becoming oversized" (L138–143). Proximal segments accommodate redistribution so race is not globally limb-dominant (L145). Not permission for "extreme spider-like limbs, giant hands, giant feet or implausibly thin bones" (L147).
- [ANAT] Arm segments (§39 L571–575): somewhat reduced upper-arm share; somewhat increased forearm share; increased hand share; increased finger contribution within hand. "continuous and adult" (L577). Must not create extremely short humeri, ape-like reach, dangling hands, spider fingers, or mismatched-scale look (L579–584).
- [ANAT] Leg segments (§42 L619–626): somewhat reduced femoral share; somewhat increased lower-leg share; adult plantigrade foot. "within-limb redistribution, not longer legs overall"; coherent locomotor chain pelvis→femur→knee→tibia/fibula→ankle→foot. §12 L201–213: legs fully adult and plantigrade; not digitigrade, stilt-legged, "unusually tall for their torso", miniature Fenn, spring-loaded jumpers, inherently fast; femur-to-lower-leg balance needs validation.
- [OPEN] Exact segment ratios (L149; §207 L3161); numerical envelopes (L567).

### A4 Shoulder / pelvic relationships
- [ANAT] Shoulders adult, coherent with thorax/arms; trend away from Durrim breadth/mass; "must not become juvenile sloped shoulders by default" (§15 L246–248). Population tendency "moderate clavicular breadth compatible with the narrow core, but shoulder breadth is not forced narrow in every individual" (§48 L697). Narrow frame retains adult shoulder development (L701).
- [VAL] "No single shoulder-to-hip ratio defines Cogling identity." (L252; also §61 L877 for sex-related).
- [ANAT] Pelvis fully mature adult (§16 L256; §47 L683); not childlike/narrow through immaturity, not Pipkin's primary lower-trunk mechanism, not Durrim mass, not external hip-width stereotype (L258–262). Pelvis "integrated without becoming the dominant silhouette anchor" (L102); vs Pipkin does not carry the same primary silhouette role relative to thorax (L685); vs Durrim lower mass/breadth/depth (L687); capable of broad sex-related/individual variation (L689).
- [OPEN] Clavicular breadth, scapular relationship, shoulder-thorax integration (L250); pelvic breadth/depth/height/inlet/outlet/external soft tissue (L691; §207 L3163–3164).

### A5 Neck
- [ANAT] Supports adult head without toy-like oversized-head silhouette or Durrim/Gorrund-thick neck (§17 L268–270). Length/circumference vary with frame, sex-related anatomy, muscularity, genetics (L272).
- [ANAT] §50 L715–723: variation in length, circumference, muscular development, visible tendon/soft tissue; "No mandatory thin neck, thick neck or forward-head posture is approved."
- [OPEN] Neck numeric values: SILENT (not listed in §207).

### A6 Hands / feet
- Hands (pointer to fine-scale distal articulation §38–§42):
  - [ANAT] "major supporting anatomical identifier" (§10 L163); "supporting—not sole—racial identifier" (§40 L588). Fully adult; noticeable without huge; structurally fine (not Durrim-like); broad hand-shape variation; long fingers (L165–170).
  - [ANAT] Hand architecture (§40 L590–595): fully mature palm; fine metacarpal/phalangeal construction; increased finger length relative to palm; adult knuckle/tendon relationships; five digits.
  - [DIR/VAL] "Palm width, palm length, finger length and finger segment proportions must not collapse into one control." (L599). Finger length "may vary substantially inside the Cogling-valid envelope" (L597).
  - [ANAT] Finger variation (§41 L605–611): total finger length; proximal/middle/distal phalanx contribution; taper; joint prominence; digit-to-digit relationships; soft-tissue fullness. Thumb opposable, functionally adult (L613).
  - [ANAT] Long fingers must not become claws, talons, skeletal caricatures, "universally thin fingers", or engineering symbol (L174–179). Digits/nails: five fingers, five toes, ordinary humanoid nails; no claws/talons/gripping pads/tool-use structures (§24 L356–361). Five digits "first-pass humanoid default unless later evidence establishes otherwise" (L172).
  - [ANAT] Hand firewall: "Finger length is anatomy. What a Cogling learns to do with those fingers is culture" (L181); no dexterity/craft/lockpick/spell precision biology (§11 L187–197; §41 L615; §141 L2196–2208).
- Feet:
  - [ANAT] Adult plantigrade; support stable stance, lower-leg relationship, normal footwear, broad variation (§13 L217–223); must not become tiny feet (Pipkin stereotype inversion), giant halfling feet, child feet, prehensile, automatic climbing adaptations (L225–230). "moderate adult humanoid feet"; "not required to be unusually small or large relative to stature" (§43 L630–632).
  - [DIR] Foot controls eventually distinguish skeletal length, width, arch, heel, forefoot, toe length, soft tissue (L634–641). Not a climbing adaptation or "racial balance mechanism" (L643).
- [OPEN] hand/palm/finger proportions (§207 L3165); foot proportions/arch (L3166; L232).

### A7 Reach-related anatomy
- [ANAT] Arms adult humanoid; total arm near Marchfolk at normalized height; "not a reach-specialized population in the Grask sense" (§9 L153–155). Primary distinction "segment distribution and distal articulation, not maximum reach" (L157). "no fixed reach superiority is approved until comparative validation" vs equal-height Pipkin (L159).
- [DER] Absolute reach short despite near-human proportional limb contribution; "cannot be assumed equal to Marchfolk"; "Approved anatomy must not be distorted to normalize reach" (§156 L2402–2408). No hidden arm extension (§182 L2804; §188 L2875–2879).
- [OPEN] arm span/reach distribution (L514); interaction reach, combat reach (§207 L3192–3193).

### A8 Posture / Anatomical Resting Alignment
- [ANAT] "Posture is not used to create apparent smallness." "Neutral anatomical alignment remains upright" (§49 L709–711).
- [ANAT] Anatomical Resting Alignment distinct from Cultural/Personal Body Language; emerges from spine, pelvis, shoulder, limb, foot relationships; "No racial hunch, crouch, bounce, fidget or 'ready-to-tinker' pose is approved." (§162 L2486–2496).
- [ANAT] Adulthood must never depend on posture (L80).

### A9 Population-specific axial structures
- SILENT (no tail or other population-specific axial structure defined). Axial column explicitly ordinary adult (§49 L705).

### A10 Head-to-stature (whole-body only)
- [ANAT] Head may occupy "somewhat greater fraction of total stature" than Marchfolk "simply because of allometric scaling", but "racial identity cannot depend on deliberate head enlargement" (§18 L280); envelope must "survive direct comparison with a human child" (L282). Head size "cannot be used as the main mechanism that makes Cogling look small" (§17 L274).
- [VAL] Avoid infant/toddler head share, bobble-head silhouette, oversized cranium shorthand (§51 L731–734).
- [ANAT] Adult-valid head size "roughly 11–13 cm" (L522; §99 L1583; §207 L3172) — readability solved by camera/animation/lighting, not biological enlargement of eyes, head, nose, ears, mouth (L1585–1594).
- [OPEN] Exact head-to-body ratio / head allometry (L284; L736; §207 L3170).

## B. Skeletal Frame
- [ANAT] "fine skeletal construction" (§7 L114): narrow long-bone shafts; smaller absolute joints; lower breadth/depth than Durrim; lower structural mass than height-normalized Marchfolk; clean segment transitions (L116–121). Fine ≠ brittle, weak, undernourished, sickly, hollow-boned, low-density, or incapable of substantial muscle (L123–130). "Bone material properties are not inferred from visual gracility." (L132)
- [ANAT] Joints: relatively small absolute, "visually articulated" (= transitions at wrist, elbow, ankle, knee remain legible rather than "uniform scaled-down forms"), not fragile; no knobby joints/exposed-bone caricature (§14 L236–240). §52 L740: "fine in scale but fully adult".
- [DIR] Joint controls must distinguish skeletal breadth, skeletal depth, articular-region scale, muscular/tendinous coverage, adipose/soft-tissue coverage (§52 L742–747). Fine wrist/ankle ≠ weak material (L749). Elbow/wrist/knee/ankle coherent with distal redistribution (L751).
- [DIR] Long-bone robusticity "a distinct biological parameter from limb length and muscularity"; population favors fine shafts; individuals range in Cogling envelope; high muscularity must not thicken bone to Durrim proportions; low muscularity must not make bones implausibly thin (§53 L755–761).
- [DIR] Frames: "Narrow, Balanced and Broad may be used as provisional creator-facing starting concepts ... not human frame copies" (§19 L290); "Provisional starting frames: Narrow / Balanced / Broad" — "Cogling-specific configurations, not copied Marchfolk measurements" (§54 L767–772). Frame changes must preserve Fine-Scale Elongated Articulation (L294).
- [DER] Frame "may influence": clavicular breadth; thoracic breadth; pelvic breadth; long-bone robusticity within limits; joint dimensions (L774–779). Frame must not automatically determine height, muscle, fat, face, sex-related anatomy, culture, personality (L781).
- [SOFT] **Clarification (Pass 2 AC-9, L783):** "Skeletal Frame may set starting correlated values or distribution tendencies for long-bone robusticity and joint dimensions inside the valid population envelope, but those parameters remain separately adjustable (§53, §69) and are never hard-determined by Narrow, Balanced or Broad. Combined-proportion validity governs the result." → governs L774–779 (frame→robusticity/joints is a starting tendency, not a hard dependency).
- [ANAT/VAL] Broad boundary (§55 L789–801): may have greater thoracic/pelvic breadth, somewhat greater joint dimensions, greater robusticity within envelope; must retain narrow-core relationship relative to structural-mass races, near-human limb total, distal redistribution, fine-scale articulation. "Broad does not mean Durrim." Also L292: "A Broad Cogling remains fine-scale relative to Durrim structural concentration."
- [ANAT/VAL] Narrow boundary (§56 L805–814): may reduce breadth/joint dimensions within limits; must not become Fenn, childlike, fragile, undernourished, implausible; distal redistribution present "as a population tendency without requiring maximum expression". L292: "A Narrow Cogling remains healthy and adult".
- [SOFT] Structural-mass axis (SR-COMP §4 L41): Cogling → Pipkin → Durrim "broadly progresses from finer to greater skeletal structural presence" — "not a universal linear morph" (L43).
- [OPEN] Joint breadth/depth ranges (L242); joint dimensions and long-bone robusticity distribution (§207 L3167).

## C. Physical Composition
- [ANAT] Current muscularity and body-fat amount/distribution separate from frame (§20 L298). Valid: low-muscle and highly muscular; low- and high-fat; regional physiques; varied soft tissue (L300–304). High muscle must not erase fine skeleton; high fat must not erase joint/limb organization or produce Pipkin/Durrim caricature; low muscle/fat ≠ frailty (L306–310).
- [DIR] Muscular Development Capacity (biological potential/envelope) vs Current Muscularity (present mass) distinguished (§21 L314–316; §57 L818). "Fine bones do not logically require low muscular-development capacity." (L320). Substantial muscle on fine skeleton allowed (L820); muscle shape follows attachment/segment geometry, not scaled Marchfolk musculature (L822); preserve wrist/ankle and long-bone identity (L824).
- [DIR] Current muscularity ranges broadly (minimal/moderate/high/regional) (§58 L830–836); not a proxy for age, sex, occupation, racial authenticity (L838).
- [DIR] Body-fat amount and distribution are distinct controls (§22 L324; §60 L856). Broad healthy variation; amount does not automatically determine face shape, frame, movement style, personality, culture, health status (§59 L842–850). [DIAG] At higher amounts, skeletal/segment relationships "must remain recoverable diagnostically" (L852).
- [ANAT] Regional adipose may affect abdomen, hips, thighs, upper arms, chest, face, other regions (L858–865). No required round belly, thin/soft body, childlike fat pattern, "tiny old inventor" silhouette (L326–331); "No required round belly, soft-cheeked gnome look or childlike distribution" (L867).
- [ANAT] Thorax "or an hourglass device" prohibited (L669); waist not a cinch point (L677).
- Population-specific tissue systems (e.g. Saurin E/B): SILENT — none defined.
- [ANAT] Center of mass derived from anatomy/composition; frame/muscle/adipose must "meaningfully affect body mass distribution without erasing racial anatomy" (§150 L2335–2343).
- [OPEN] Muscular Development Capacity distribution; body-fat distribution tendencies (L318, L826, L869; §207 L3168–3169); center-of-mass values (L2345; §207 L3183).

## D. Biological surface
- [ANAT] Principle: "broad, naturally overlapping and secondary to anatomy. No required skin color, hair color, eye color, freckling pattern, complexion or age cue defines the race." (§106 L1706). Part 1 boundary: traits "cannot be invented here to rescue anatomical distinctiveness"; recognizable in neutral gray, hair/clothing/tools removed (§25 L365–369).
- Integument family: ordinary humanoid skin (implicit; no scales/homologues). Scales/homologues: SILENT (none).
- [ANAT] Pigmentation (§107 L1712–1722): very light through very deep melanin; warm/neutral/cool undertones; natural regional variation; individual variation; no mandatory tone/palette; no "pale workshop-dwellers, ruddy comic gnomes" coding.
- [DIR] Pigmentation must distinguish biological parameters, not one flat color: baseline melanin; undertone contributors; localized vascular visibility; sun-response/tanning; regional variation (§108 L1726–1733). Implementation deferred (L1735).
- [ANAT] Freckles absent→extensive; not required; don't indicate youth/personality/occupation/culture/ancestry purity (§109 L1739–1746). "No mandatory fantasy marking pattern" (L1750).
- [ANAT] Skin texture: age, hydration, pores, fine lines, exposure, individual (§110 L1756–1762); small scale ≠ doll-like/poreless; texture not exaggerated to prove adulthood (L1764–1766).
- [PRES] Scale readability: no exaggeration of freckles, pores, wrinkles, iris saturation, brow thickness, hair strand scale; close-view may reveal subtle detail (§130 L2021–2029).
- [SOFT] Ancestry correlations probabilistic; weighted/conditional distributions not hard rules (e.g. "dark skin requires dark hair") (§125 L1964–1971).
- [ANAT] Four Skin Appearance Layers (§132 L2052–2059): 1 Natural (pigmentation, undertones, freckles, natural markings, vascular visibility); 2 Environmental (tanning, weathering); 3 Applied (tattoos, cosmetics, paint); 4 Acquired (scars, burns). Separate from Character Architecture Layers and from facial-only FD domains (L2059).
- [OPEN] pigmentation frequencies; ancestry distributions (§136 L2120–2121; §207 L3175–3176).

## E. Hair / homologues
- [ANAT] Scalp hair (§111 L1772–1782): strand thickness, density, straight/wavy/curly/coily, growth direction, hairline, crown, length potential, age changes; no texture/style required.
- [ANAT] Hair pigment (§112 L1788–1794): black, brown, blond, red/auburn, gray/white through aging, intermediates; fantasy/artificial = presentation (L1798).
- [ANAT] Facial hair: pointer only — may grow where individual biology supports; not mandatory, not adult-read requirement, not sex-defining, not racial; no "bearded tinkerer" default (§113 L1802–1813).
- [ANAT] Body hair: amount/distribution vary individually; "not determined by scalp hair, facial hair, sex-related anatomy, muscularity, age presentation or culture" (§114 L1817–1819). [SOFT/OPEN] Sex/hormonal hair distributions OPEN; if approved "must use soft correlations rather than hard creator dependencies" (L1821). No hairy/hairless stereotype (L1823).
- [ANAT] Eyebrows/eyelashes independent (§115; facial; pointer only).
- [DIAG] Hair strand rendering respects actual scale; biological diameter "not assumed to scale linearly with total body height" (§131 L2033–2037).
- Display structures / other homologues: SILENT.
- [OPEN] hair-strand properties; facial/body-hair growth distributions (L2122–2123; §207 L3177).

## F. Age
- [ANAT] Adult scope: every valid playable Cogling reads adult "from anatomy alone" (§5 L71); adulthood never depends on facial hair, wrinkles, clothing, occupation, voice, tools, posture, personality, culture (L73–82). "Very small stature is not juvenile anatomy." (L94)
- [ANAT] Age architecture: Chronological Age, Apparent Biological Age, Age Presentation — "cannot be collapsed into one slider or one visual stereotype" (§119 L1894–1899; also §94 L1509).
- [ANAT] Young adult already fully mature structurally; cannot rely on enlarged eyes, reduced jaw, shortened midface, doll-like skin, child fat (§120 L1905–1914).
- [ANAT] Mature adult: fine lines, texture, soft-tissue redistribution, hair graying/density; no single marker mandatory (§121 L1918–1925).
- [ANAT] Older adult: wrinkles/folds, texture, soft-tissue redistribution, graying/whitening, density change, "age-related posture only where individually appropriate and not biologically mandatory" (§122 L1931–1937); no wizard/inventor/elder archetype (L1939).
- [ANAT] Hair aging: graying, density reduction, recession, thinning; baldness individual; gray hair not required for older look nor to distinguish adults from children (§124 L1951–1960).
- [ANAT] Age & stature: §123 L1943–1947 (see A1).
- [ANAT] Age & movement: no automatic frailty/vigor; older not required to stoop/shuffle/slow (§165 L2524–2530).
- [OPEN] lifecycle; lifespan; maturation timing; detailed age progression; age-related skeletal change (L525; §136 L2125–2128; §207 L3181–3182).

## G. Sex-related anatomy
- [ANAT] Follows "universal four-layer character-creation amendment" (§23 L337). Sex-related anatomy may affect pelvis, thorax, soft tissue, other structures; does not automatically determine height, frame, muscularity, fat, facial identity, hairstyle, clothing, class, culture, occupation, personality (L339–350).
- [VAL] Race recognizable in like-for-like comparisons; "No single shoulder-to-hip ratio, chest form, waist shape or external hip width defines either Cogling sex-related anatomy or Cogling racial identity." (§61 L875–877). Pelvis must provide "adult locomotor and sex-related anatomy" (L258).
- [DIR] Face: no face-level sex slider; capability met by body-level sex-related anatomy selection plus permitted soft facial distribution (UFCA AC-U2, L1566).
- [ANAT] Movement: sex anatomy does not prescribe gait, hip sway, stride confidence, aggression, delicacy, gesture (§164 L2512–2520).
- [VAL] SR-COMP like-for-like rule (SR-COMP L168–169).
- Reproductive biology status: SILENT beyond "sex-related anatomy" in pelvis.
- R-SEX pointers: SILENT (no R-SEX IDs in Cogling spec).
- [OPEN] Magnitude/morphology of dimorphism (L352, L879; §207 L3174).

## H. Asymmetry & acquired history (non-facial)
- Natural body asymmetry: SILENT (only facial asymmetry §96 L1528–1532).
- [PRES/ANAT] Scars, burns, weathering, acquired marks "may be available broadly"; do not define race, occupation, prove adulthood, imply combat/personality (§127 L1985–1992). Biological scar behavior later unless race-specific healing approved (L1994). Acquired layer = Skin Appearance Layer 4 (L2057).
- Missing/damaged structures: SILENT. Tail injury/loss: N/A (no tail).

## I. Presentation
- [PRES] Makeup, dyes, tattoos, piercings, scars, jewelry, goggles, hats → Personal Presentation, not biology; none required for recognition (§126 L1977–1981).
- [PRES] Tattoos/body mod cultural; no required Cogling tattoo/piercing/engineering mod (§128 L1998–2002).
- [PRES] Fantasy hair color = presentation (L1798).
- [PRES] Body language: Anatomical Resting Alignment distinct from Cultural/Personal Body Language (§162 L2486). Animation must not express intelligence, curiosity, industriousness, eccentricity, nervousness, cheerfulness, craft obsession, mischievousness (§161 L2470–2478). No constant fidgeting (§149 L2331). Movement/personality variation not in Biological Randomization (§166 L2534–2541).
- [PRES] Culture firewall: tinkering/engineering cultural; biology does not require inventiveness, goggles, tools, hats, etc.; farmer/soldier/sailor/courtier/hunter/scholar/laborer equally valid (§27 L389–406).
- [PRES] Clothing/gear preview — see J/equipment: armor/clothing must avoid crushed torsos, misplaced elbows/knees, sleeves erasing distal redistribution, gloves erasing fingers, boots distorting feet, helmets enlarging/compressing head (§177 L2725–2731); gloves respect palm/finger length/phalanx distribution/joint placement/spacing, cannot shorten or exaggerate fingers (§178 L2739–2748); headwear preserves cranial envelope, ear placement, actual scale; no oversized "gnome head" shell (§179 L2752–2760). Goggles/caps = optional presentation (L2758).

## J. Creator system
- [DIR] Modes (§191 L2915–2917): **Simple Mode: Race → Preset → Confirm; Advanced Mode: Race → Preset → Customize → Confirm.** "A preset is a legitimate output of the same biological system used by Advanced Mode and NPC generation." (L2919; also §134 L2083).
- [LAT] Preset library spans (§192 L2925–2935): min/ref/max stature neighborhoods; Narrow/Balanced/Broad; low/moderate/high muscularity; low/moderate/high adiposity; multiple face breadth/depth; multiple nose/jaw/orbit configs; varied ears; broad surface phenotypes; multiple adult age presentations; varied hair/facial-hair. No preset may require tinkerer clothing/goggles/tools (L2937). Surface preset list (§134 L2086–2093): pigmentation ranges, hair architectures, iris colors, freckled/non-freckled, facial-hair/non, multiple ages, attractive/ordinary/unusual faces, no tinkerer dependence.
- [LAT/VAL] Neutral biological preset set (§193 L2941–2952): **small/narrow; small/broad; reference/balanced; reference/high muscularity; reference/high adiposity; tall/narrow; tall/broad; multiple sex-related anatomical configurations; young-adult; mature-adult; older-adult** — "validation coverage targets, not social archetypes or fixed creator categories" (L2954).
- [LAT] Randomization: race-aware, relationship-aware, ancestry-aware when defined, separated Biological vs Presentation (§194 L2958–2962); "cannot generate invalid combinations merely because each individual slider value is valid" (L2964); interim weights "testing distributions only" (L2966; also §133 L2072). Biological randomization uses valid structural anatomy first, broad surface distributions, overlap with other races, no stereotype bundles (§133 L2063–2070). No systematic "cute Cogling" pairing (large eyes, tiny noses, freckles, smooth skin, rosy cheeks, bright hair) (§129 L2008–2015). SR-COMP §14 L195–200: no forcing Cogling toward "thinness/freckles/goggles/old age"; overlap/boundary heights preserve full relationship system.
- [DIR] Selective randomization (§195 L2972–2979): face while preserving body/height/age; surface preserving face; hair only; body composition preserving frame and height; presentation preserving all biology; dependency rules may constrain where anatomy requires. Also §133 L2074–2079: surface only, hair only, eyes only, age presentation only, without rewriting anatomy.
- [DIR/VAL] Locks (§196 L2983–2989): lockable; respect validity; if no valid solution, "preserve the lock and communicate/resolve the constraint rather than silently changing the locked value". [OPEN] exact UI (L2989; §207 L3202).
- [DIR] Saved appearances (§197 L2993–3005): savable in unified appearance-data architecture; preserve semantic info to reconstruct **race; biological anatomy; frame; composition; face; surface phenotype; age presentation; hair/presentation selections**. Schema versioning/migration required future (L3005; [OPEN] §207 L3203).
- [DIR] Cross-race reuse (§198 L3009–3013): no numeric application to another race; any future transfer via "semantic mapping and race-valid reinterpretation rather than raw slider copying"; not required in first pass.
- [ANAT] Character data (§174 L2672–2681): unified conceptual model with race-specific validity; shared schema does not require one skeleton, mesh, morph topology, uniform scaling, identical control ranges. SR-COMP §13 L173–189: no shared short-race master morph; shared semantic dimensions (height, frame, muscularity, adiposity, regional proportions, facial domains) but per-race envelopes, constraints, distributions, response curves.
- [VAL] NPC parity (§199 L3017–3027): same validity system; no stereotype generator making all Cogling tiny/narrow, old, freckled, goggle-wearing, tinkers, quick/fidgety; culture distributions separate.
- [DIR] Creator camera (§200 L3031–3041): whole-body proportion review; face close-up; ear close-up; hand/finger inspection; feet; surface detail; "Close inspection is preferable to biologically exaggerating features". Fine ear folds are close-view trait (L1596).
- [OPEN] First-person: OPEN; if supported, actual eye height, hand geometry, reach truthful (§160 L2462–2464; §189 L2895; §207 L3195). Third-person/dialogue cameras frame actual height; cannot lift to Marchfolk eye height (§160 L2460; §189 L2885–2893).
- [DIR] Interaction-point architecture separates visual anatomy, collision, interaction reach, combat reach, IK target, animation contact, camera — "cannot be collapsed into one whole-body scale factor" (§186 L2846–2855).
- [ANAT] Equipment: very small stature does not authorize automatic scaling of weapons/tools/world objects; fit ≠ feasibility (§29 L427–431); canonical object dimensions retained unless distinct variant (§180 L2766); fit accounts for shoulder, thorax, pelvis, limb segments, joint locations, hands, fingers, feet, head/ear geometry; no "generic scaled human underneath equipment" (§176 L2703–2714). World adapts to approved anatomy, Cogling not made taller for Marchfolk geometry (§30 L439). World validation vs approved target anatomy incl. extreme combinations; prototype not authority (§201 L3045–3053). Stairs/doors/ladders/furniture solutions: "No solution is chosen here" (L2824).

## K. Locked validation tests (body / whole-character)
COG-BODY (§32 L451–471; §71 L1061–1076):
- COG-BODY-01 ref adult ~91 cm neutral (L453); -02 min ~76 cm unmistakably adult (L454); -03 max ~107 cm distinct from equal-height Pipkin (L455); -04 Narrow low-muscle healthy not childlike/fragile (L456); -05 Broad high-muscle not Durrim (L457); -06 higher-fat no child-fat/round-gnome (L458); -07 hands hidden still Cogling (L459); -08 head/hands/feet hidden core+limb organization distinct (L460); -09 same-height Cogling/Pipkin (L461); -09A max Cogling ~107 vs central-ref Pipkin ~107 (L462); -10 normalized Broad high-muscle Cogling vs Narrow Durrim (L463); -10A actual-height max Cogling ~107 beside min Durrim ~122 (L464); **-11 min Cogling ~76 cm beside ~1–2-year-old toddler** — adult skeletal, pelvic, facial-development boundary, limb organization (L465); -12 long-finger high end functional (L466); -13 distal-emphasis low end identity survives (L467); -14 like-for-like sex comparisons (L468); -15 culture removal no tinkerer cues (L469); -16 vs Fenn normalized ears hidden (L470); -17 vs Grask normalized hands neutralized (L471); -18 normalized Marchfolk without stature cue (L1063); -19 max forearm redistribution, total arm near-human, no Grask reach (L1064); -20 max lower-leg redistribution, total leg near-human (L1065); -21 max finger emphasis, tool-free neutral hand (L1066); -22 Broad high-muscle no Durrim (L1067); -23 Narrow low-muscle no child/Fenn/fragility (L1068); -24 high adiposity structure diagnostic (L1069); **-25, -26 RETIRED** (duplicates of -11 / -09A) (L1070–1071; §207A L3211); -27 ref Cogling vs min Pipkin ~91 cm (L1072); -28 like-for-like sex normalized vs Marchfolk (L1073); -29 extreme combined proportions validator rejects (L1074); -30 head/hands hidden core+segment identity (L1075); -31 vs Sagekin normalized (L1076).
Whole-character face-adjacent: COG-FACE-02 min-height adult (L1639); COG-FACE-15 face-neutralized silhouette body remains Cogling (L1652); COG-FACE-20 min-height vs ~1–2-year-old toddler (L1657); COG-FACE-24 camera readability without enlargement (L1662).
COG-SURF-01…17 (§135 L2099–2115) — key: -01 light↔deep same anatomy; -05 facial hair removed adult survives; -06 bald; -08 young smooth no child read; -09/-10 older adult; -12 neutral gray FD-STRUCT; -13 presentation stripped; -14 randomized batch no cute/tinkerer bundle; -15 close vs gameplay no exaggeration; -16/-17 vs Marchfolk/Pipkin overlap.
COG-MOVE-01…27 (§169 L2585–2611) — whole-character: -07/-08/-09 frame/muscle/adipose; -10/-11 grasp & no object scaling; -18 idle no fidget; -22 camera actual scale; -23 weapon no auto-scale; -24 reach no hidden extension; **-25 min Cogling vs ~1–2-year-old toddler walk** (L2609); -26 Cogling/Pipkin 91–107 cm movement (L2610); -27 honest gait transition (L2611).
COG-WORLD-01…20 (§202 L3059–3078) — doors, handles, stairs, ladders, seating, beds, counters, shelves, passages/collision, dialogue (Marchfolk, Gorrund), object pickup, weapon, helmet (-15 no head inflation), gloves (-16 finger anatomy), sleeves/trousers (-17 joints/distal redistribution), camera (-18), mounts (-19), prototype ~125 cm vs ~76–107 cm (-20).
COG-CC-01…15 (§203 L3084–3098): -01 Simple preset valid; -02 Advanced no hidden race swap; -03 race-aware full randomization valid only; -04 face-only preserves body/height/age; -05 body-only preserves face/surface; -06 surface-only preserves FD-STRUCT; -07 hair-only; -08 presentation-only no biology change; -09 locks unchanged; -10 invalid combined extremes rejected; -11 save/reload semantic; -12 preset stripped readable; -13 NPC no stereotype bundle; -14 neutral preset set spans envelope; -15 creator camera without exaggeration.
Suite: all active COG-BODY/FACE/SURF/MOVE/WORLD/CC cases (§207A L3209).

## L. Positive body identity statements
- §3 L33: "Cogling possess a very-small adult humanoid architecture organized around a narrow stable central core and near-human total limb contribution, with comparatively fine skeletal shafts and a distinctive redistribution within the limbs toward the forearms, lower legs, hands and fingers. Their identity comes from where limb length and articulation are distributed, not from becoming globally limb-dominant or reach-specialized."
- §37 L545: "Cogling body identity is carried by a narrow stable adult core combined with broadly near-human total limb contribution whose internal segment distribution shifts distally. The body is not globally elongated; its distinctive rhythm comes from redistribution inside otherwise adult, balanced limb totals." ("This distinction is mandatory." L547)
- §34 L498 (Part 1), §73 L1105 (Part 2) identity statements; §206 L3155 final: "...defined in the body by Fine-Scale Elongated Articulation: a narrow stable central core supports broadly near-human total limb contribution while length is redistributed within the limbs toward the forearms, lower legs, hands and especially fingers through comparatively fine skeletal shafts and clearly articulated distal joints. ... Broad frame, composition, surface phenotype and adult age variation remain valid. Their small size changes real reach, stride geometry, equipment fit and world interaction, but does not biologically require child proportions, miniature objects, quickness, dexterity, tinkering, cuteness or any other behavioral stereotype."
- SR-COMP L261: "Cogling redistribute fine-scale articulation distally within a narrow stable adult body."

## M. Cross-population boundary tests / comparators (body)
- **Pipkin** (§63 L897–914): overlap ~91–107 cm; multi-factor; "**Leg segmentation alone cannot separate Cogling from Pipkin**" (L914). Tests: COG-BODY-03 (~107), -09, -09A (~107 vs ~107), -27 (~91), COG-MOVE-26 (91–107). SR-COMP-01 (~91 cm, matched frame/muscle/adiposity/age/surface/presentation; near-Marchfolk Cogling axial/trunk share vs modestly reduced Pipkin vertical central-trunk share) L132–133; SR-COMP-02 (~107 cm) L135–136; SR-COMP §6 boundary rule L74; composition failure "Narrow/low-fat Pipkin becoming Cogling", "High-fat Cogling ... reading as Pipkin solely through softness" (L124, L127); SR-COMP-10 lean Pipkin vs higher-fat Cogling (L160).
- **Durrim** (§64 L918–933): no current stature overlap; normalized comparison mandatory; frame/muscle must not erase boundary. Tests: COG-BODY-05, -10 (normalized), -10A (~107 vs ~122 actual), -22. SR-COMP §5 boundary rule L61; failures "Broad Cogling reading as Durrim", "High-muscle Cogling losing fine skeletal identity" (L123, L128); SR-COMP-10 Broad/high-muscle Cogling vs Narrow/low-muscle Durrim (L160).
- **Fenn** (§65 L937–951): distinction must survive without ears; "Fine skeletal construction alone cannot carry the distinction." Tests: COG-BODY-16, -20, -23.
- **Grask** (§66 L955–969): no limb dominance/reach specialization. Tests: COG-BODY-17, -19.
- **Marchfolk** (§67 L973–983): normalized; identity may arise from coordinated relationship; not every trait outside human range. Tests: COG-BODY-18, -28.
- **Sagekin** (§67A L987–1001): Sagekin may have longer forearms/hands/fingers, linear silhouette, greater leg share but human bone/joint scale and no compensating proximal reduction; "No individual long forearm, long finger or narrow silhouette is sufficient". Test: COG-BODY-31.
- **Human toddler** (§68 L1005–1017): min-height vs ~1–2-year-old: adult cranial/body proportionality, shoulder, thorax, pelvis, limb segmentation, hand/foot maturity, joints, fat distribution. Tests COG-BODY-11, COG-FACE-20, COG-MOVE-25; SR-COMP-11 (L162–163).
- SR-COMP all-three tests involving Cogling: -04 normalized all three (L141–142, diagnostic only, "not a valid in-world body state"); -05 silhouette (L144–145); -06 torso obscured (L147–148); -07 extremities obscured (L150–151); -08 face only (L153–154); -09 surface swap (L156–157); -12 movement neutralization (L165–166).
- Final anti-convergence (§204 L3102–3125).

## N. Forbidden controls / anti-patterns (body)
- No "Cogling Proportion" master slider (§33 L494); Fine-Scale Elongated Articulation not a master slider (L37); no "Cogling Face" slider (§98 L1570); no shared short-race master morph (SR-COMP L173).
- No uniform whole-body scale for height (§175 L2685); no authoritative whole-body scale multiplier (L67); no single whole-body scale factor for interaction/collision/camera (§186 L2855); no universal scale transform for mounts (L2909); no single "short race" interaction offset (SR-COMP L220).
- Valid Cogling cannot be made by shrinking Marchfolk, lengthening every limb, enlarging hands, thinning body, or Pipkin stature + Fenn gracility (§37 L549–554).
- Palm/finger dimensions must not collapse into one control (L599).
- Juvenile combination ban (§5 L84–92); head enlargement ban (L280, L733); biological enlargement for readability ban (L1585–1590).
- Invalid combination examples (§70 L1050–1055): min height + max head share + min shoulder/pelvic maturity (toddler); max forearm + max hand + max finger without proximal compensation; min joints + max muscularity; broad frame + max robusticity → Durrim; narrow frame + min soft tissue → fragile caricature. "Validation must evaluate relationships, not isolated slider legality." (L1057). Combined-proportion validity list (§33 L479–492).
- Camera cannot lift Cogling to Marchfolk height (L2460, L2893); no hidden arm extension/weapon enlargement/hitbox inflation (L2875–2879); no Marchfolk-sized invisible capsule merely for convenience (L2867); animation warping cannot hide inaccessible geometry (L2454).
- No stereotype bundles in randomization/NPCs (§129, §199, SR-COMP §14); stereotype firewall list (§205 L3129–3149).
- Hair/body-hair sex correlations never hard creator dependencies (L1821); surface correlations never hard rules (L1966–1971).

## O. Explicitly OPEN / DEFERRED (body / whole-character)
§207 consolidated list governs (L3157–3205) — body/whole-character items: exact height distribution & final min/ref/max; body segment ratios; thoracic dimensions; pelvic morphology (breadth/depth/height/inlet/outlet); shoulder/clavicular dimensions; hand/palm/finger proportions; foot proportions/arch; joint dimensions and long-bone robusticity distribution; Muscular Development Capacity distribution; body-fat distribution tendencies; exact head allometry; face readability at ~11–13 cm head; sex-related dimorphism magnitude/morphology; ancestry/population structure; surface frequencies; hair/iris frequencies; lifespan/maturation; detailed age progression; center-of-mass (§150); locomotion speeds; acceleration/turning; jump/climb/swim; stealth/balance/fall; strength/leverage; racial gameplay traits & stat bonuses; race/class restrictions; collision; interaction reach; combat reach; equipment compatibility/restrictions; first-person; mounting/vehicles; technical skeleton/mesh/morph architecture; camera/rendering; animation/IK/warping; networking; attribute-lock UI (§196); schema/version migration; race-description revision; culture/background.
- Other in-body OPEN statements: gameplay dexterity/interaction/crafting effects (L197); physical interaction consequences of hand proportions (L2210); armor/clothing technical method (L2733); world-access solutions for stairs etc. "No solution is chosen here" (L2824).
- §207B dependencies (L3215–3223): Short-Race Comparative Review ACCEPTED/COMPLETE; UFCA canonicalized (closure pending author review); cross-race pigmentation review; race-biology-gameplay review; full-roster world-scale/accessibility review; technical character-architecture review. Unregistered dependency → question stays OPEN (L3223).
- RM-* refs: SILENT (none in Cogling spec). "No UE5 implementation is authorized" (L532, L1109, L2644, L3243).

## P. Provisional creator-control lists (body) and status
- No list labelled "Pass 1" exists in the Cogling spec. Nearest equivalents:
- **§69 Body-control architecture (L1021–1044)** — "Part 2 does not finalize creator-facing sliders, but the eventual system must be capable of representing at least": height; frame; thoracic breadth/depth; pelvic breadth/depth/height; shoulder/clavicular breadth; axial contribution; total arm contribution; upper-arm/forearm distribution; palm/hand contribution; finger length and internal distribution; total leg contribution; femur/lower-leg distribution; foot dimensions; joint breadth/depth; long-bone robusticity; neck; muscular-development capacity; current muscularity; body-fat amount; body-fat distribution; sex-related anatomy. "Controls may later be merged or reorganized, but the biological relationships cannot be lost." Status: capability requirement (Part 2 FIRST-PASS ACCEPTED, L1107), not finalized sliders.
- **Frames** Narrow/Balanced/Broad — "provisional creator-facing starting concepts" (L290); "Provisional starting frames" (L767); AC-9 clarification (L783).
- Sub-control requirements: joint controls 5-way distinction (§52 L742–747); foot controls 7-way (§43 L634–641); hand non-collapse (L599); finger variation dims (§41 L605–611); pigmentation dims (§108 L1728–1733).
- Face controls (§97 L1538–1562) routed to UFCA (L1566) — out of scope.

---

## Extraction notes
1. **Supersessions:** Part 1 OPEN list (§35 L502) and Part 2 OPEN list (§72 L1080) are explicitly historical; §207 governs. Legacy movement brief ("quick steps", "fine motor control", etc.) superseded as racial traits by Tyler decision Sept 30 2026 (§140 L2177–2179); §28 L412 earlier "subject to later review" is resolved by §140. Old ~0.45× reference non-authoritative (L49). COG-BODY-25/-26 retired (L1070–1071, L3211). Frame→robusticity/joint "may influence" (L774–779) is qualified by Pass 2 AC-9 (L783) as starting tendency only.
2. **Status drift:** §4 L59 says SR-COMP acceptance "tracked in specs/STATUS.md"; §207B L3216 states it ACCEPTED/COMPLETE. §208 gate (L3241) requires SR-COMP be authored — satisfied per L3245.
3. **No "Pass 1" body-control list** exists; §69 is the capability list. Pass 2 audit tags appear only as AC-8 (L2046, FD-HAIR) and AC-9 (L783); Part 2 audit clarifications "4a–4c" (L1107) not individually labeled in text.
4. **Not in §207 but stated OPEN elsewhere:** hand-proportion interaction consequences (L2210), gameplay dexterity (L197), armor technical method (L2733), world-access solutions (L2824) — arguably subsumed under §207 equipment/gameplay/technical items. Frame naming/semantics described as "provisional" (L290, L767) but not listed in §207. Neck numeric values never listed OPEN. "ear mobility" appears only in §207 L3173 with no body text.
5. **SILENT areas:** height distribution shape; natural body asymmetry; missing/damaged structures; tail/axial specializations; body homologues/display; reproductive specifics; R-SEX IDs; RM-* refs; Saurin-style tissue systems.
6. **Pipkin overlap phrasing:** Cogling spec says overlap "approximately 91–107 cm" (L63); COG-BODY-09A calls ~107 cm Pipkin "central-reference" (L462), consistent with SR-COMP Pipkin ref ~107 (L27).
7. "Very-small" toddler comparator is specifically **~1–2-year-old** (L465, L1007, L2609, SR-COMP L163); Pipkin uses a generic "human child of similar height" — do not merge.
8. Head size "roughly 11–13 cm" is the only head absolute number; it is described as adult-valid, not a ratio — head-to-stature ratio itself OPEN.
