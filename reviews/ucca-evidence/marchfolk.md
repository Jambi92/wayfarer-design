> UCCA Phase 1 evidence appendix to `reviews/claude-ucca-01-requirements-matrix.md`. Line references are to the canonical race spec (or the named source) as of commit 89ca8f7. Extraction only: no canon is changed and nothing here is new biology. Tags: [ANAT] anatomical requirement · [DIR] direct control · [DER] derived/coupled · [SOFT] tendency · [VAL] validator · [LAT] latent/preset · [PRES] presentation · [DIAG] diagnostic · [OPEN] open/not authorized.

# UCCA extraction — Marchfolk (specs/marchfolk/MARCHFOLK_V1.md, 336 lines)

Source structure: universal-amendment banner (L5); v1.0 (L7–43); v1.1 (L45–96); v1.2 face (L98–147; skipped except whole-character touches); v1.3 (L149–193); v1.4 (L195–235); v1.5 (L237–273); Consistency Resolution Part 1 (L275–292, governs v1.1/v1.4 wording); Part 2 pre-inheritance (L294–336).
Governing order inside spec: Part 1 resolutions (L277–289) correct v1.1/v1.4 wording; universal amendment (L5) corrects Athletic-as-frame.

## A. Stature and proportions

**A1 Standing height**
- [ANAT] Min about 147 cm (4'10") / Reference about 173 cm (5'8") / Max about 203 cm (6'8"); "approved first-pass playable envelope" — v1.0 §4–5 L19–23.
- [ANAT] Duplicate table 147 / 173 / 203 cm under heading "Height (preliminary)" — v1.1 §3 L60–64. Column header now "Reference height" (renamed from "Baseline" per Part 1 §6 L286). v1.0 "approved first-pass" wording is later-recovered and controls (see notes).
- [ANAT] "about 173 cm (5'8") is the Marchfolk Reference Height. Minimum and maximum remain the approved playable envelope" — Part 1 §6 L286.
- [ANAT] "Anatomy doesn't change the 147–203 cm height range" — L5.
- [SOFT] Distribution: "population distributions may differ where appropriate, individual overlap stays broad, and a player character can sit anywhere in the supported range" (re sex) — L23. No numeric distribution/shape: SILENT.
- [DIR] Height is a quick control — v1.1 §1 L53.
- [VAL] Permanent height characters about 147, 173, 203 cm, each with several frame/composition combos, "never only the reference height" — v1.5 L249.

**A2 Torso length/depth/width**
- [DIR] Chest width and depth (Upper body); waist width, abdomen, torso length (Core and pelvis) — v1.1 §5 L74–75.
- [DER] "Chest depth: ribcage and upper-torso structure"; "Waist: smooth transitions through the abdomen and lower torso"; "Torso and leg length: plausible overall proportions" — v1.1 §6 L84–88.
- [ANAT] Frame includes "ribcage dimensions" — v1.0 §6–8 L27.
- [VAL] Relationship constraints across "shoulder width and ribcage, ribcage and waist" — L31; proportion stress covers torso — L251.

**A3 Limb length & segment proportions**
- [DIR] Leg length (Lower body) — L76. Arm length: SILENT as a listed control (only "arm thickness" L74).
- [VAL] Relationship constraints "upper arm and forearm", "femur and lower leg" — L31.
- [DER] "Limb thickness: believable joint transitions" — L87.
- [VAL] "Minimum and maximum limb relationships" in proportion stress — L251.
- [ANAT] Limb segment ratios / numbers: SILENT.
- Thickness terminology: "Neck, upper-arm, forearm, thigh and calf 'thickness' aren't automatically skeletal controls"; component contributions must be documented — Part 1 §3 L283 (governs v1.1 §5 L74–76 "thickness" controls).

**A4 Shoulder / pelvic relationships**
- [DIR] Shoulder width — L74; hip width, pelvis proportions — L75.
- [DER] "Shoulder width: clavicles, upper back and shoulder-joint position"; "Hip width: pelvis structure and upper-leg alignment" — L83, L86.
- [ANAT] Frame = shoulder breadth, ribcage dimensions, pelvic breadth, joint scale, skeletal visual mass — L27.
- [VAL] "pelvis and hips"; "neck and shoulders" relationship constraints — L31.

**A5 Neck**
- [DIR] Neck thickness (Upper body) — L74; not automatically skeletal — L283.
- [VAL] neck–shoulders relationship — L31; proportion stress includes neck — L251.
- [ANAT] Age affects neck structure — v1.2 §4 L128; aging may affect neck — v1.5 L257.

**A6 Hands / feet**
- [ANAT] Human hands and feet — L15.
- [DIR] Hand size — L74; foot size — L76 (v1.1 Pass-1 controls).
- [ANAT]/[OPEN] Must distinguish absolute vs proportional dimensions, skeletal vs soft tissue, length/breadth/depth; "One generic size scalar isn't a sufficient biological definition, and exact controls are future work" — Part 1 §4 L284.
- [VAL] hand–wrist, foot–ankle relationships — L31; hand and foot scale in proportion stress — L251.

**A7 Reach-related anatomy**
- [ANAT] SILENT on arm-span/reach anatomy.
- [OPEN] "a taller Marchfolk doesn't get more melee reach" (cosmetic neutrality) — L39; combat reach, interaction reach, hit detection OPEN, "none of these is set automatically by whole-character visual scale" — v1.5 L265.

**A8 Posture / Anatomical Resting Alignment**
- [ANAT] Age affects posture — v1.4 §2 L212. "Anatomical Resting Alignment" term: SILENT in spec.
- [ANAT] "Movement visually respects height, limb proportions, mass, frame and composition" — L265.

**A9 Population-specific axial structures** — SILENT (human; none).

**A10 Head-to-stature (whole-body)**
- [VAL] "head and body" listed among relationship constraints — L31.
- [ANAT] numeric head-to-stature: SILENT.

## B. Skeletal Frame
- [ANAT] "Frame describes skeletal structure (shoulder breadth, ribcage dimensions, pelvic breadth, joint scale, skeletal visual mass) and isn't muscularity, body fat, fitness or personality" — L27.
- [ANAT] "Skeletal Frame is the underlying continuous configuration of shoulder, ribcage, pelvis, joints and related structural dimensions" — Part 1 §5 L285.
- [LAT]/[DIR] Frame Presets Narrow, Balanced, Broad = "editable starting points, not immutable biological castes"; players may customize away within valid anatomy — L285; L58; L203 ("different starting anatomical proportions"); L206 ("A frame never restricts customization beyond the race's normal biological limits").
- [DIR] Starting body frame is a quick control — L53.
- Superseded: v1.1 §2 / v1.4 §1 "four frames" incl. Athletic — corrected by L5, L58, L201–204, L281.
- Robusticity, bone breadth/depth: SILENT beyond "joint scale", "skeletal visual mass" (L27). Frame-correlated tendencies: SILENT.
- [VAL] Frame test: each frame with lean/muscular/high body fat "to verify frame and composition stay independent" — L250.

## C. Physical Composition
- [ANAT] Muscularity, body-fat amount and distribution, regional muscle, physique vary independently of frame (examples Narrow+muscular … Broad+high body fat) — L27.
- [DIR] Overall muscularity, overall body-fat distribution (quick) — L53; regional muscle emphasis (detailed) — L77, §7 L90–92 ("starts cosmetic, with no automatic gameplay advantage").
- [DIR] Body-fat **amount** and **distribution** separate; quick controls "conceptually support both"; v1.1 wording "incomplete", "distribution never substitutes for amount" — Part 1 §2 L282 (supersedes literal L53/L68/L77/L231).
- [LAT] Composition presets Lean, Athletic, Muscular, Heavy, Custom — L5, L27. Athletic "may initialize muscularity, body-fat amount and distribution, regional muscle and other non-skeletal parameters. It never automatically changes skeletal shoulder breadth, ribcage or pelvic dimensions, limb-bone proportions, joint scale" — L281.
- [DER] "Visible mass comes from height, frame, muscle, fat and regional composition together, never one generic scale value, and exact mass calculation is a future problem" — L31.
- [DIR] No single thin-to-heavy slider — L68.
- Muscular Development Capacity: term SILENT in Marchfolk spec (Marchfolk is the comparator; see Skarn).
- Soft tissue: thickness = skeletal + muscle + adipose + total circumference — L283.
- [ANAT] Age affects body composition — L212, L257.

## D. Biological surface
- [ANAT] Human skin biology — L15.
- [DIR] Four Skin Appearance Layers, independently editable: Natural (base pigmentation, undertone, complexion, freckles, moles, birthmarks), Environmental (sun, tanning, weathering, dryness, roughness, calluses, minor discoloration, dirt), Applied (tattoos, makeup, paint, decorative markings), Acquired (scars) — v1.3 §1 L153–162; named Natural/Environmental/Applied/Acquired, "organize appearance state and aren't inheritance categories" — L287.
- [ANAT] Pigmentation envelope (AGREED): skin very light/fair → deep/dark brown; undertones cool, neutral, warm, golden, olive, reddish where appropriate; natural hair color families; iris families — Part 2 §1–2 L300–305.
- [SOFT]/[OPEN] "Exact Marchfolk frequencies are OPEN… Validity isn't frequency (locked)… no rigid phenotype packages" — L307.
- Patterning/scales/homologues: N/A (human); material/finish: SILENT.
- [VAL] Broad combinations tested keeping the four layers separate — L257.

## E. Hair / homologues
- [DIR] Planned hair controls: hairstyle, style-dependent length, texture, color, hairline, density, parting, accessories — v1.3 §2 L166–175.
- [ANAT] Natural hair color families; "Age-related depigmentation stays separate" — L304.
- [PRES] "Body frame doesn't needlessly restrict which hairstyles are available" — L177.
- [DIR] Facial hair: pointer — own style/length/density/color; color linked to hair by default, unlinkable — v1.3 §3 L181. Eyebrow hair: UFCA slot 11 pointer — L106.
- Body hair: SILENT.

## F. Age
- [ANAT] Adults only; continuous; reference points young adult, mature adult, middle-aged, older adult, elder — v1.4 §2 L210.
- [ANAT] Age affects "facial volume, skin elasticity, hair color and density, body composition, posture"; "Cosmetic age carries no automatic gameplay penalties" — L212.
- [ANAT] Chronological age / apparent biological age / age presentation distinct — Part 1 §8 L288 (refines L212 "actual vs apparent").
- [VAL] Adult aging "must do more than wrinkles and gray hair" incl. body composition — L257.
- [OPEN] Lifespan, maturation milestones, fertility span, senescence rate "E, OPEN" — Part 2 §5–6 L315.
- [DIR] Age is a creator variable (continuous adjustment) — L210; "preserving age" in selective randomization — L261.

## G. Sex-related anatomy
- [ANAT] Biological Anatomy layer includes "relevant sex-related characteristics" — L35.
- [ANAT] "no hard sex-specific height restriction from the selected sex-related anatomy or starting frame: population distributions may differ where appropriate, individual overlap stays broad" — L23; anatomy doesn't change height range — L5.
- Other sex-related body tendencies: SILENT. Reproductive biology: SILENT. R-SEX pointer: PROJECT_RULES L73–79 (not in spec).

## H. Asymmetry & acquired history (non-facial)
- Natural body asymmetry: SILENT (asymmetry only facial, v1.2 §3 L122–124).
- [DIR] Acquired layer = scars — L162; scars get different healed appearances — L185.
- [PRES] Weathering, scars, calluses, grooming show history; "player-controlled cosmetic options, never forced by class or occupation" — v1.3 §5 L189.
- Missing/damaged structures: SILENT.

## I. Presentation
- [PRES] Personal Presentation = hair, facial hair, clothing, makeup, scars, tattoos, accessories — L35.
- [PRES] Frontier reputation isn't anatomy: ruggedness, manual labor, toughness, frontier clothing, weathering, scars, muscularity come from culture/background/occupation/environment/history — L35.
- [DIR] Marking placement (future): position, scale, rotation, color, opacity, mirroring, layer order, independent removal; respects anatomical regions — v1.3 §4 L183–185.
- [PRES] Culture separation (ancestry ≠ culture) — Part 2 §14 L332.
- Body language vs resting alignment: SILENT. Clothing/gear preview: SILENT (lighting/expression previews are face-only L132–139).

## J. Creator system
- [DIR] Simple Mode Race → Preset → Confirm; Advanced Race → Preset → Customize → Confirm; preset = starting configuration — L39, v1.4 §4 L227 ("Both use identical character data").
- [DIR] Quick vs detailed body controls share character data; switching keeps appearance — v1.1 §1 L49.
- [LAT] Presets (themes, "not classes, occupations or required histories"): Frontier Settler, Traveling Scholar, Veteran Soldier, Rural Laborer, Merchant, Elder Wanderer — v1.4 §3 L216–223. "no hidden models and no preset-only features" — L216. Presets vary in height, frame, muscularity, fat distribution, age, face, skin, hair, markings, silhouette; fully reproducible — L231.
- [LAT] Randomization: full and selective, locks, race-aware validity, reproducible where needed, never converges on one default — L39. Target ops: randomize face, body, or hair and presentation only; preserve age, frame, selected facial traits, chosen body attributes; UI to be designed — L261.
- [VAL] Saved appearance: "One unified conceptual appearance record" for preset/advanced/random/NPC; schema + version tracking, migration, deterministic interpretation; "implementation OPEN" — L261.
- [DIR] NPC parity — L261 (NPC generation uses same record).
- [OPEN] First-person/third-person camera, height-dependent camera placement OPEN — L265.
- [VAL] Equipment accounts for height, frame, composition, hands, feet, head/face, hair, deformation "without scaling every piece with height"; "Canonical equipment dimensions stay independent of cosmetic whole-character scaling" — L265.
- [DIR] Gameplay neutrality of cosmetic variation — L39; L265 movement not automatically slower/faster.
- Technical compatibility (skin layering, hair/headwear, markings persist, save/load, LOD, body-morph compat, multiplayer sync) — L193.
- Prototype authority: "The existing UE5 character stays a prototype… Approved Design Specification > Open Decision Register > Prototype Implementation" — L269.

## K. Locked validation tests (body/whole-character)
No test IDs in Marchfolk spec. Unnamed tests:
- Permanent height characters 147/173/203 cm — L249.
- Frame independence test — L250.
- Proportion stress incl. combined extremes; "invalid overall are rejected even when each parameter is valid alone" — L251.
- Identity stress (no one body type/age/pigmentation family/hair type) — L253.
- Age, skin/hair/marking validation — L257.
- Preset round-trip Preset → Advanced → Edit → Save → Reload; no hidden geometry — L261.
- Randomization large-sample (validity, diversity, distributions, extremes, accidental correlations, convergence, selective, locks) — L261.
- World validation vs approved anatomy (doors…IK) — L265.
- Three-stage philosophy A/B/C — L243.

## L. Positive body identity
- "They represent the breadth of believable human physical diversity, not one idealized fantasy-human body" — L13.
- "Marchfolk keep recognizably human skeletal and cranial architecture, shoulders, ribcage, spine, pelvis, limbs, joints, hands, feet, face, skin and hair biology and human locomotor anatomy, with variation inside believable human boundaries" — L15.
- Primary Human Reference Population; "doesn't make Marchfolk the default anatomy for every humanoid race" — L15, L286, L273.

## M. Cross-population comparators (body)
- Marchfolk is the comparator for all races — L15. Ancestry families: Human = Marchfolk, Skarn, Sagekin; "Human never equals Marchfolk" — L321.
- No body boundary tests vs other populations defined in this spec: SILENT (tests live in Skarn/Sagekin).

## N. Forbidden controls / anti-patterns
- No uniform whole-character scaling for height — L23.
- No "one generic scale value" for mass — L31.
- No single thin-to-heavy slider — L68.
- Avoid disconnected morph targets, excessive mesh stretching, implausible combinations — L81.
- No generic hand/foot size scalar as biological definition — L284.
- Athletic must not set skeletal parameters (no frame+composition package) — L281.
- No hidden models / preset-only features / hidden geometry — L216, L261.
- No rigid phenotype packages — L307; ear not a pointiness slider — L311.
- No scaling every equipment piece with height — L265.
- No forced occupation/class appearance — L189.

## O. OPEN / DEFERRED
- Race-level biological gameplay differences — L39.
- Technical architecture (MetaHuman etc.) — L43, L269.
- Exact mass calculation — L31.
- Exact hand/foot controls — L284.
- Marking placement system "(future)" — L183.
- Appearance-record implementation, UI for selective ops — L261.
- Camera (FP/TP), collision, interaction/combat reach, hit detection, mounts — L265.
- Pigmentation frequencies — L307, L336; lifecycle numbers — L315; mixed-ancestry items — L336.
- RM-* refs: none in this spec.

## P. Pass 1 provisional creator-control lists (BODY)
Status: v1.1 sits under spec-wide "design update only, pending further refinement" (L3); body lists carry NO "PROVISIONAL CONTROL ORGANIZATION" label (that label is face-only, L102).
- Quick (v1.1 §1 L53): starting body frame, height, overall muscularity, overall body-fat distribution [read as amount + distribution per L282], general physique adjustments (undefined; audit 01 L10).
- Detailed (L54): all quick + individual body regions, detailed anatomical proportions, regional muscle development.
- Regions (v1.1 §5 L72–77): Upper body — shoulder width, chest width and depth, neck thickness, arm thickness, hand size; Core and pelvis — waist width, abdomen, torso length, hip width, pelvis proportions; Lower body — leg length, thigh thickness, calf thickness, foot size; Physical composition — overall muscularity, overall body-fat distribution, regional muscle emphasis. (Thickness/size controls qualified by L283–284.)
- Hair controls "Planned" (L166–175); facial hair (L181); marking placement "future" (L183–185).
- Frame presets N/B/B (L203); composition presets Lean/Athletic/Muscular/Heavy/Custom (L5).

## Extraction notes
- v1.1 §3 labels height "preliminary" (L60) while v1.0 (recovered later, L3) calls the same numbers the approved first pass (L23); Part 1 §6 L286 confirms the envelope. Numbers identical; register L446 marks AGREED.
- v1.1 §1/§4/§5 and v1.4 §5 "fat distribution" wording superseded by Part 1 §2 L282 (amount + distribution).
- v1.1 §2 and v1.4 §1 Athletic-as-frame superseded (L5, L58, L201–204, L281); v1.4 "proportions" re-read as composition relationships (L281).
- "General physique adjustments" (L53) undefined.
- Arm length not listed as a v1.1 control though "upper arm and forearm" relationships are validated (L31).
- Skin layers: v1.3 list four layers; register L21 historically said three (superseded).
