<!-- RAC Phase 1 evidence extraction (agent-produced, line-checked at HEAD 218f64a). Not canon; supporting evidence for reviews/claude-rac-01…12. -->
# A1 — Pelvis and axial architecture: evidence extraction (13 races)

Extraction only. Nothing here is new canon. Every line number was confirmed against the current working-tree file with `awk`/`grep` (repo `/home/claude/wayfarer-design`, read-only). Quotes are verbatim substrings (≤25 words), bold markers stripped.

**Source abbreviations:** MF = `specs/marchfolk/MARCHFOLK_V1.md`; SK = SKARN; SG = SAGEKIN; FN = FENN; AE = AELARI; VL = VAEL; HV = HALVREN; DU = DURRIM; GR = GRASK; GO = GORRUND; PK = PIPKIN; CG = COGLING; SA = SAURIN (all `specs/<race>/<RACE>_V1.md`). PR = `decisions/PROJECT_RULES.md`; UCCA = `decisions/UCCA_V1.md`; LRR = `reviews/claude-pass2-r2-large-race-comparative-review.md`; SRR = `reviews/short-race-comparative-anatomy-v1.md`; ECR = `reviews/elf-comparative-review.md`; RMQ = `reviews/claude-pass2-r5-reference-mesh-queue.md`.

**Tags:** [POS] authored positive/directional anatomy · [OPEN] explicitly open/provisional · [TEST] named validation/boundary test · [BAN] explicit prohibition · [SILENT] not addressed · [REPRO] obstetric/reproductive/fertility content (must not be invented later).

**Line-offset warning:** the `reviews/ucca-evidence/*.md` digests and LRR cite older numbering in places. Example: the Gorrund ALPC transition table is at GO L717–723 in the current file (digest cites L715–718); LRR's "GO L703–715" corresponds to current GO L705–723. Use the spec lines below.

---

## Roster-wide rules that constrain this topic

- [POS] Skeletal Frame includes pelvic width, and pelvic depth only where canon names it — "pelvic width and depth where canon names it, joint scale, long-bone robusticity" (UCCA L119)
- [BAN] Composition never edits pelvic skeleton — "composition never edits the skeleton; thoracic depth is never faked by fat or muscle; pelvic breadth is never fat" (UCCA L156)
- [BAN] No torso-mass scalar or race-proportion master sliders — "no Torso Size / Body Thickness / Torso Mass" (UCCA L92); "no master race-proportion sliders (… ALPC, LSCTA, FSEA or equivalent)" (UCCA L92; quote spans an elision — exact text: "no master race-proportion sliders ("human → Pipkin", "Cogling Proportion", "Elf Percentage", "Elf Gracility", ALPC, LSCTA, FSEA or equivalent)")
- [POS] Torso/axial vertical contribution is a Slot 2 item; neck length only where canon binds it — "Stature; torso/axial vertical contribution; neck length where bound (AD-C10)" (UCCA L31); "DIR only where canon names it (AD-C10); otherwise hidden" (UCCA L78)
- [POS] Only one REDISTRIBUTE relationship tool exists, and it is Saurin's — "the only canon case is Saurin stature accounting: head, neck, thorax, lower trunk and legs sum coherently to stature" (UCCA L103)
- [OPEN] Roster-wide carried BIO OPEN — "pelvic morphology; segment ratios and numeric proportions" … "sex dimorphism magnitude (Durrim, Grask, Gorrund, Pipkin, Cogling); reproductive biology; lifecycle" (UCCA L355); also "Pipkin trunk-share numeric relation (T-2)" (UCCA L355)
- [OPEN] Segment-share bands are measurement-deferred — "Per-race segment-share and within-limb distribution bands (torso/axial, neck, arm …)" (RMQ L79, RM-UB-01); "Per-race allometric response of head, hands, feet, joints, bone breadth and torso breadth/depth to stature" (RMQ L80, RM-UB-02)
- [REPRO] R-SEX — "Reproductive biology is never inferred from creator architecture." (PR L95; repeated UCCA L177)
- [POS] R-SEX overlap/bounds — "Hard biological validity bounds remain available to either sex unless a race's canon explicitly establishes otherwise." (PR L91); "Adult phenotype overlap is mandatory." (PR L92); "Per-race sex-conditioned soft distributions are allowed; "no shift" is a valid complete state for a race." (PR L94)
- [BAN] Saurin sex canon is not to be generalized — "Existing deliberate Saurin sex-related canon (SAURIN_V1 §263) remains intact and is not generalized to other races." (PR L96)
- [POS] LSCTA is a preserved project term — "Race-specific anatomical terms (e.g. … Pipkin Low-Set Compact Trunk Architecture) are preserved." (PR L88)
- [POS] Frame boundary rules stay hard — "Broad Skarn ≠ Gorrund; Broad Grask ≠ Skarn/Gorrund; Narrow Gorrund keeps ALPC; Broad Pipkin/Cogling ≠ Durrim" (UCCA L131)
- **Measurement queue coverage note (RMQ):** pelvic quantities appear only in RM-SR-01 ("Pipkin central-trunk share (thorax + lumbar ÷ stature) and pelvic vertical contribution", RMQ L39) and RM-LR-06 ("girdle → thorax → pelvis breadth and depth continuity profile", RMQ L32). Torso share is queued for large races (RM-LR-01, RMQ L27: "Torso share (suprasternal → hip joint ÷ stature)"), Durrim (RM-SR-06, RMQ L44), Sagekin (RM-OT-01, RMQ L89 — ribcage depth/breadth, not torso share) and elves (RM-OT-02, RMQ L90 — "thoracic depth; neck relative length"). **No RM item measures pelvic breadth/depth/height morphology for any race other than via the Pipkin and ALPC proxies.**

---

## 1. Marchfolk (Human Reference Population)

- [POS] Human axial/pelvic skeleton is the reference — "Marchfolk keep recognizably human skeletal and cranial architecture, shoulders, ribcage, spine, pelvis, limbs, joints" (MF L15)
- [POS] Reference role but not a template — "This doesn't make Marchfolk the default anatomy for every humanoid race" (MF L15)
- [POS] Pelvic breadth is a frame (skeletal) variable — "Frame describes skeletal structure (shoulder breadth, ribcage dimensions, pelvic breadth, joint scale, skeletal visual mass)" (MF L27)
- [POS] Skeletal Frame definition includes pelvis — "the underlying continuous configuration of shoulder, ribcage, pelvis, joints and related structural dimensions" (MF L285)
- [BAN] Athletic preset never alters pelvis — "It never automatically changes skeletal shoulder breadth, ribcage or pelvic dimensions" (MF L281)
- [POS] Relationship-aware links named — "shoulder width and ribcage, ribcage and waist, pelvis and hips … neck and shoulders" (MF L31; exact text: "relationship-aware constraints or validation across shoulder width and ribcage, ribcage and waist, pelvis and hips")
- [POS] Detailed-region controls include torso length and pelvis proportions — "Waist width, abdomen, torso length, hip width, pelvis proportions" (MF L75)
- [POS] Neck appears only as thickness — "Shoulder width, chest width and depth, neck thickness, arm thickness, hand size" (MF L74)
- [POS] Waist is a transition — "smooth transitions through the abdomen and lower torso" (MF L85)
- [POS] Hip width tied to pelvis and leg alignment — "pelvis structure and upper-leg alignment" (MF L86)
- [POS] Torso/leg — "plausible overall proportions" (MF L88)
- [TEST] Proportion stress — "Minimum and maximum limb relationships, torso, shoulders, pelvis and hips, neck" (MF L251)
- [REPRO] Lifecycle/fertility OPEN — "Average and maximum lifespan, maturation milestones, fertility span and senescence rate are E, OPEN" (MF L315)
- [POS] Height not sex-restricted — "There's no hard sex-specific height restriction from the selected sex-related anatomy or starting frame" (MF L23)
- [SILENT] No numeric torso share, neck length, spinal curvature, pelvic tilt, sacrum, lumbar description or pelvic depth/height. No sex-related pelvic tendency is authored. The "human reference" pelvis is assumed, not described; every other race's "than Marchfolk" comparison therefore points at an unmeasured baseline (RM-LR-01 lists "Marchfolk reference", RMQ L27).

## 2. Skarn

- [POS] Skeletal foundation vs Marchfolk — "a deeper ribcage and more thoracic volume" (SK L22); "a more substantial neck base and pelvis" (SK L23)
- [POS] Torso share and depth — "a slightly larger torso share of total height and greater torso depth" (SK L75)
- [POS] Neck/pelvis restated — "a thicker neck base and a more substantial pelvis" (SK L77)
- [POS] Torso-dominance is a tendency with variety — "The Skarn central tendency is slightly more torso-dominant than Marchfolk, but Skarn aren't universally short-legged." (SK L86)
- [POS] Pelvis width varies — "Torso, leg and arm length, shoulder width, chest width and depth, and hip and pelvis width all vary." (SK L86)
- [POS] Height distribution through torso and pelvis — "Height changes keep believable relationships between the head, torso, pelvis, arms, legs, hands, feet and joint positions." (SK L40)
- [POS] Upper axial system — "Shoulders, clavicles, chest, upper back and neck act as one connected system" (SK L90)
- [POS] Lower body carries mass — "The pelvis, hips, thighs, knees, calves, ankles and feet plausibly carry the greater mass at every setting." (SK L94)
- [BAN] No top-heavy default — "There is no default "huge upper body, tiny legs" silhouette." (SK L94)
- [POS] Linkage — "Pelvis width sets upper-leg alignment." (SK L114); "Chest depth changes ribcage volume." (SK L113)
- [POS] Randomization respects pelvis link — "shoulders and ribcage, pelvis and upper-leg alignment, joint transitions" (SK L284)
- [POS] Mount data keeps pelvis — "race and skeleton, height, leg length, pelvis position, relevant proportions" (SK L362)
- [TEST] SK-04 "Narrow, lean, long-legged" (SK L330); SK-02 Marchfolk overlap (SK L328)
- [SILENT] "More substantial pelvis" is undifferentiated (breadth vs depth vs height not specified). No neck-length statement (only neck base/thickness). No spine/lumbar/curvature, sacrum, pelvic tilt or sex-related pelvic content. No Skarn-vs-Gorrund torso share (by design, see GO L675, AD-4).

## 3. Sagekin

- [POS] Shorter torso relative to stature — "a slightly shorter torso relative to stature" (SG L139)
- [POS] Less ribcage depth — "slightly less ribcage depth" (SG L140)
- [POS] Region table — "Slightly shorter, shallower torso relative to height. Broad Sagekin keep genuinely broad torsos" (SG L155)
- [POS] Clarification of the ribcage tendency — "the ribcage tendency is reduced depth, not an undefined global narrowing" (SG L89)
- [POS] Historical bullet (kept as history) — "a possibly somewhat narrower average ribcage" (SG L83)
- [POS] Controls named — "Torso length, ribcage width and depth, waist length and transition, shoulder width, pelvis width" (SG L155)
- [POS] Spine-pelvis link — "Torso changes keep the spine and pelvis relationship." (SG L179)
- [POS] Longer-torso Sagekin valid — "shorter-limbed and longer-torso Sagekin stay supported" (SG L97)
- [BAN] Elven boundary — "never reproduces Fenn or Aelari central-tendency anatomy" (SG L147)
- [TEST] SG-09 "Long torso" (SG L194, L426)
- [SILENT] No pelvic morphology statement beyond "pelvis width" as a control; no neck, lumbar, curvature, sacrum or sex-related pelvic content.
- **Cross-file tension (not resolved here):** Halvren's normalization reads Sagekin "narrower ribcage" as breadth — "Somewhat reduced average skeletal ribcage breadth relative to equivalent Marchfolk, not shallow thoracic depth unless separately established" (HV L460) — whereas SG L89 says the tendency "is reduced depth, not an undefined global narrowing" and SG L140 says "slightly less ribcage depth". RMQ RM-OT-01 queues "ribcage depth and breadth" for Sagekin vs Marchfolk with source "F-19 hand/ribcage wording" (RMQ L89).

## 4. Fenn

- [POS] Smaller torso share — "Slightly smaller torso share of height, somewhat less ribcage depth, more compact chest, longer waist transition" (FN L50)
- [POS] Ribcage/spine — "Somewhat shallower front to back, moderately narrow for height, somewhat vertically compact, with a relatively longer waist and lumbar transition" (FN L110)
- [POS] Pelvis — "A distinct elven pelvis, not a scaled human one, supporting longer femurs, stable hips, light visual build" (FN L111)
- [OPEN] Pelvis shape — "Exact shape awaits prototyping, and not every Fenn has narrow hips" (FN L111)
- [POS] Pelvis-to-leg differs from human — "different pelvis-to-leg relationships" (FN L38)
- [POS] Shallow upper torso and clean neck line — "a shallower upper torso than humans" … "a clean shoulder-to-neck line" (FN L109)
- [POS] Balance may differ — "may change balance, center of mass and locomotion" (FN L66)
- [TEST] Equal-height hidden-ears test includes "torso, shoulders, pelvis and legs" (FN L78); FN-08 "Long torso, against the population average" (FN L91)
- [POS] Randomization links — "shoulder and ribcage, pelvis and leg" (FN L341)
- [POS] ECR waist normalization — "This does not mean Fenn have a longer absolute or proportional waist transition than Aelari" (ECR L45)
- [SILENT] Neck length is not authored in FN (only "clean shoulder-to-neck line"); ECR assigns Fenn neck "Intermediate" (ECR L31). No curvature, sacrum, tilt or sex-related pelvic content.

## 5. Aelari

- [POS] Whole-body vertical elongation — "whole-body vertical elongation, distributed coherently through the cranium, neck, torso, arms and legs" (AE L33)
- [POS] Torso — "Longer than Fenn relative to height, longer waist transition, moderate chest breadth, relatively shallow depth" (AE L48)
- [BAN/guard] "Believable thoracic volume, never implausibly shallow" (AE L48)
- [POS] Neck — "Somewhat longer on average than humans and Fenn. The shoulder-to-neck-to-skull line adds subtly to verticality" (AE L50); guard "Believable range, never exaggerated" (AE L50)
- [POS] Ribcage — "Vertically longer than Fenn, moderate width, relatively shallow depth" (AE L123)
- [POS] Torso/spine controls — "Longer overall torso and waist transition than Fenn." and controls include "waist and lumbar length" (AE L124)
- [POS] Pelvis — "A distinct elven pelvis, not a stock human pelvis with longer legs attached." (AE L126); "Stable with long femurs, coherent with the spine" (AE L126)
- [OPEN] "Exact shape awaits prototyping." (AE L126)
- [BAN] "No mandatory hip width by race or sex-related anatomy" (AE L126)
- [POS] Link — "Pelvic width sets hip articulation and upper-leg alignment." (AE L143)
- [TEST] AE-11 "Long-torso stress test" (AE L95); risk case "Extreme neck, torso, arm, hand, leg and foot length together is the Aelari risk case." (AE L163); equal-height Fenn test at ~190 cm "Aelari more vertically continuous, with a longer torso and neck" (AE L169); human boundary checks "pelvis, limbs, hands, feet, and neck and torso" (AE L170)
- [POS] ECR neck — "Aelari trend toward greater average neck length, and greater neck contribution to total vertical body proportion, than Fenn and Vael populations" (ECR L320); absolute vs proportional "aren't interchangeable measurements" (ECR L320)
- [POS] ECR waist — "a longer average ribcage-to-pelvis (waist-transition) region than Fenn and Vael" (ECR L46)
- [SILENT] No curvature, sacrum, tilt, pelvic depth or sex-related pelvic tendency (beyond the hip-width ban).

## 6. Vael

- [POS] Torso — "Greater torso share than Fenn, deeper ribcage than Fenn or Aelari, moderate width, strong torso-to-pelvis continuity, less elongated than Aelari" (VL L35)
- [POS] Depth is skeletal — "Vael torso depth comes from ribcage depth and curvature, the spine-to-ribcage relationship, shoulder placement and the torso-to-pelvis transition." (VL L114)
- [BAN] "It's never faked with body fat, muscle, an oversized chest or uniform torso scaling." (VL L114)
- [POS] Spine and waist (only explicit lumbar curvature in the roster) — "Moderate torso length, less extended waist than Aelari, strong torso-to-pelvis continuity, natural lumbar curve." (VL L121)
- [POS] Frame scope — "shoulder and pelvic breadth are Skeletal Frame variables because frame changes them" (VL L121; also UCCA L133, T-10)
- [POS] Neck — "Somewhat shorter relative to the torso than Aelari (relative, not absolute), with broad variation" (VL L123); v1.0 "strong shoulder-to-neck integration" (VL L36)
- [BAN] "No short, thick-neck stereotype" (VL L123)
- [POS] Pelvis — "Their own elven pelvis (not human, Fenn or Aelari)" (VL L38); "A distinct elven pelvis: torso-to-pelvis continuity, stable with long legs" (VL L124)
- [OPEN/BAN] "No human pelvis plus a slider. Awaits prototype validation" (VL L124)
- [POS] Coupled relationships — "torso length and waist, waist and pelvis, and pelvis and hip" (VL L128)
- [POS] Center of mass — "lower center of mass than Aelari" (VL L165)
- [BAN] "Compact" — "never means short, dwarven, stocky or automatically muscular" (VL L29); "Durrim anatomy is never used to solve Vael compactness." (VL L179)
- [TEST] VL-16 Narrow/low muscle/low fat keeps "Vael ribcage, torso continuity" (VL L149); risk combos "short torso with long legs, long torso with shorter valid limbs" (VL L155)
- [POS] ECR — "The deeper ribcage must not be mistaken for a longer waist" (ECR L47)
- [SILENT] No pelvic depth/breadth direction, no sacrum, no tilt, no sex-related pelvic content.

## 7. Halvren

- [POS] Axial vs appendicular domains — "Spine, ribcage, torso relationships" (HV L35); "Shoulders, pelvis, arms, legs, joint relationships" (HV L36)
- [POS] Mosaic allowed only if coherent — "relatively human-like torso depth, moderately elven limbs" (HV L41)
- [POS] Torso inheritance — "covering ribcage width, depth and vertical length, waist-transition length, spine and torso proportions and torso-pelvis integration" (HV L120)
- [BAN] "It's never reduced to "human torso versus elf torso,"" (HV L120)
- [POS/OPEN] Pelvic principle locked, detail open — "the Halvren pelvis is a developmentally viable mixed structure, not a linear morph between stock human and stock elven pelvis geometry." (HV L122); "Detailed pelvic inheritance is OPEN, requiring prototypes and further anatomical design." (HV L122)
- [POS] Neck — "The neck keeps absolute length, length relative to torso, circumference, skeletal structure and muscular development separate." (HV L122); "Aelari ancestry may raise proportional neck contribution and Skarn ancestry structural neck presence" (HV L122)
- [POS] Source contributions — Skarn "more substantial neck and pelvis" (HV L111); Aelari "greater torso and waist vertical contribution" and "longer proportional neck contribution" (HV L113); Vael "more compact torso-pelvis continuity than Aelari ancestry" (HV L114)
- [POS] Elven family foundation — "elven pelvic foundation" (HV L48)
- [OPEN] Part 1 OPEN list — "torso, limb, pelvic, hand and foot, craniofacial" inheritance (HV L74); keep-open list includes "pelvic details" (HV L421)
- [OPEN] Blocked dependency — "(b) The shared elven pelvis, blocking pelvic inheritance." (HV L437); "Shared elven pelvic anatomy, the sex-related anatomy system" … "Never invented inside Halvren." (HV L497)
- [OPEN] Sex — "exact sex-related inheritance stays within the broader unresolved anatomical-system review" (HV L54)
- [TEST] Extreme combos — "Aelari verticality with human structure, Vael thoracic depth with gracile limbs" (HV L148); HV-13–17 include Aelari "verticality, neck and torso" (HV L371)
- [REPRO] "with no chromosome counts, molecular genetics, reproductive mechanisms or fertility probabilities" (HV L19); "Fertility biology is out of scope for this first pass" (HV L20); "not inherently sterile, with reproductive biology out of scope" (HV L319); "fertility where relevant" in future lifecycle design (HV L325); "Multigenerational viability provisionally approved" (HV L409)
- [SILENT] No Halvren-specific numeric torso/neck share; no curvature, sacrum or tilt.

## 8. Durrim

- [POS] Foundation tendencies — "strong shoulder and pelvic integration" … "a low center of mass" (DU L11)
- [BAN] Not scaled/compressed — "Compact doesn't mean compressed." (DU L21); "never look like a vertically squashed human skeleton" (DU L21)
- [POS] Torso identity — "a broad skeletal thorax relative to stature, substantial thoracic depth relative to stature, strong ribcage-spine integration, compact vertical torso relationships, and strong torso-pelvis continuity" (DU L25)
- [POS] Torso share — "Durrim have a greater torso contribution to height than equivalently tall Marchfolk, which doesn't mean an absolutely long torso" (DU L97)
- [BAN] Torso shape — "never an extremely long torso on short legs, a vertically compressed human torso or a near-square block" (DU L97)
- [POS] Transitions — "with recognizable thorax, abdomen, waist and pelvis transitions" (DU L97)
- [POS] Pelvis (Part 1) — "A distinct architecture for compact stature, broad foundation, shorter lower limbs, low center of mass and stable locomotion" (DU L32)
- [OPEN] "OPEN, requires detailed anatomical design." / "Never a simply widened human pelvis" (DU L32)
- [POS/OPEN] Pelvis (Part 2) — "Exact morphology stays OPEN. Only strong torso-pelvis integration, a compact-stature pelvis, stable hip placement, coherent support for shorter legs and broad variation are set" (DU L108)
- [BAN] "external hip width never stands in for skeletal width" (DU L109)
- [POS] Spine — "Supports compact stature, deep and broad thorax, substantial upper-body mass potential, functional flexibility and stable locomotion" (DU L33); "Never inherently stiff, since shorter doesn't mean less mobile" (DU L33)
- [POS] Center of mass — "Lower than equivalently proportioned taller humanoids, from stature, compact torso, shorter limbs, pelvis and mass distribution" (DU L34)
- [POS] Neck — "The neck trends toward a relatively short contribution to total height" (DU L21); "Relatively short proportional contribution, but always with a visible transition into the shoulder girdle" (DU L107)
- [BAN] Neck — "never the head attached straight to the torso" (DU L107)
- [BAN] Waist/abdomen — "No required large belly, fat-thick waist, straight waist or barrel silhouette." (DU L104)
- [POS] Pelvis independent of muscle — "a broad pelvis with low muscularity" (DU L52)
- [POS] Height distribution — "torso length, spinal and neck contribution, head-body relationships and limb segments" (DU L19)
- [POS] Pelvic orientation is individual variation — "individual variation in spinal posture, shoulder and head carriage, pelvic orientation, foot orientation and stance width never erases Durrim skeletal identity" (DU L430)
- [TEST] Combined-validity case "maximum torso breadth with minimum pelvis and shoulders" (DU L139); permanent ~152 cm Durrim/Marchfolk/Sagekin test (DU L145, L502); "Durrim near their upper boundary keep compact structural power" (DU L145)
- [OPEN] Final open list — "exact pelvic morphology, sex-related anatomy and facial-hair distributions" (DU L520)
- [REPRO] "lifecycle, lifespan, maturation, fertility and senescence" OPEN (DU L520)
- [OPEN] Sex — "Durrim sex-related anatomy isn't finalized" … "Durrim magnitudes stay OPEN" (DU L58)
- **Terminology note:** the label "compact structural concentration" does not appear in DU itself; it is defined in GO L731, PK L15, CG L21 and SRR L17. DU's own phrases are "compact skeletal architecture" (DU L430) and "compact structural power" (DU L145).
- **Wording flag:** DU L93 reads "Durrim trend toward greater torso and lower leg and overall limb contribution to total height", which on its face conflicts with DU L97/L119 (legs contribute less). Read in context it most likely means greater torso and lower (leg/overall limb) contribution; not resolved here.
- [SILENT] No sacrum, no lumbar curvature statement, no pelvic depth/height direction.

## 9. Grask

- [POS] Torso share lower — "Trends toward a lower contribution to standing height than Marchfolk and Skarn, producing the long-limbed silhouette" (GR L37); "never a tiny torso on giant limbs" (GR L37)
- [POS] Torso share is relative, not absolute — "proportionally reduced torso contribution never means small torso" (GR L198; exact: "so proportionally reduced torso contribution never means small torso")
- [POS] Signature — "coordinated elongation of multiple limb segments without equivalent elongation of every axial body region" (GR L192)
- [POS] Thorax — "Moderate skeletal breadth, meaningful thoracic depth, a relatively elongated but not oversized ribcage and strong spine-shoulder integration" (GR L38)
- [POS] Depth guard — "without converging on Durrim-like proportional depth or Skarn-like human power architecture" (GR L39)
- [POS] Ribcage — "never a human ribcage stretched vertically" (GR L202)
- [POS] Neck — "trending moderate-to-long relative to Durrim and Skarn; no swan-neck caricature, forward monster neck or permanent hunch" (GR L43)
- [BAN] Neck not identity — "Grask should not generally rely on extreme neck length for racial identity." (GR L172)
- [POS] Spine — "spinal curvature is never the source of troll identity, and a neutral Grask stands without hunch, stoop or crouch" (GR L44)
- [POS] Pelvis — "Distinct and suited to tall stature, long legs, bipedal locomotion and center-of-mass relationships" (GR L45)
- [POS/OPEN] Locked requirement — "Grask pelvis geometry must coordinate long lower limbs, upright bipedal locomotion and the Grask torso without being created by simply scaling or narrowing a human pelvis." (GR L208); "Exact morphology OPEN" (GR L208)
- [BAN] "never a narrowed or scaled human pelvis" (GR L45)
- [POS] Pelvic breadth vs soft tissue — "external hip width kept distinct from skeletal pelvic breadth, gluteal muscle and fat distribution" (GR L209)
- [BAN] Waist — "no required extremely narrow waist, V-shaped torso or gaunt abdomen" (GR L207); "neither a narrow "monster waist" nor a large belly is required" (GR L40)
- [TEST] Invalid combo "minimum torso contribution with maximum leg and neck length" (GR L255); Grask vs Aelari "Compare neck, torso and limb contribution" (GR L266); Aelari-lookalike failure "an Aelari with heavier joints and longer arms" (GR L174); shortest-limbed Grask vs Skarn uses "non-human girdle and pelvic organization, neck relationship" (GR L714); Grask vs Fenn "a different torso and pelvis system" (GR L267)
- [OPEN] Final list — "exact pelvic morphology; numerical body proportion ranges and ratios" … "sex-related anatomy and dimorphism" (GR L726)
- [REPRO] "Lifespan, maturation rate, fertility, senescence and developmental stages are OPEN" (GR L534)
- [SILENT] No sacrum, tilt, lumbar description or pelvic depth/height direction.

## 10. Gorrund (incl. Axial Load-Path Continuity)

- [POS] Massiveness defined skeletally — "skeletal breadth and depth, joint dimensions, axial scale, pelvic structure, limb-bone structural dimensions" (GO L19)
- [POS] Axial skeleton a major identifier — "broad skeletal thorax, substantial thoracic depth, strong vertebral and torso integration, substantial shoulder girdle and pelvis, strong neck-to-torso integration" (GO L39); "never a rectangular block" (GO L39)
- [POS] "Axial" defined — "means structural emphasis through spine, ribcage, shoulder girdle, pelvic integration and torso-to-limb transitions, never a torso that visually overwhelms the limbs" (GO L167)
- [POS] Torso share vs Grask — "Gorrund generally possess a greater proportional torso contribution to total standing height than Grask at matched height" (GO L169)
- [POS] Independence of axial dimensions — "Thoracic breadth, depth and vertical length, abdominal vertical contribution, waist skeletal relationships, and pelvic breadth and depth are independent, never one Torso Mass concept." (GO L175)
- [POS] Thoracic depth — "substantial thoracic skeletal depth relative to stature and breadth" (GO L42); "One of the strongest positive signals" (GO L180)
- [POS] Ribcage length — "Substantial enough to integrate the large torso, never just a widened and deepened short human ribcage" (GO L183)
- [POS] Waist — "narrower isn't human or bodybuilder, broader isn't obese or unfit" (GO L185); abdomen "no "ogre belly"" (GO L186)
- [POS] Shoulder-to-pelvis spectrum — "Continuous variation from more shoulder-dominant through balanced to more pelvis-present, not subtypes" (GO L188)
- [POS] Pelvis (P1) — "Distinct, suited to high structural scale, broad and deep torso, large lower limbs and upright locomotion" (GO L49); "never a uniformly enlarged human pelvis" (GO L49)
- [OPEN] "morphology OPEN for Part 2 and validation" (GO L49)
- [POS] Pelvic breadth — "May trend substantial, with external hip width kept separate from muscle, fat and sex-related anatomy" (GO L50)
- [POS/OPEN] Pelvis (P2) — "Gorrund pelvises possess substantial load-bearing skeletal dimensions and strong integration with both the deep axial torso and large lower limbs" (GO L189); "meaningful breadth, depth and hip-joint scale; exact morphology OPEN" (GO L189); "a narrower valid pelvis still supports large hip joints and femora" (GO L189)
- [BAN] "external hip circumference is never a proxy" (GO L190)
- [POS] Spine — "Upright bipedal neutral alignment, never a required hunch, kyphotic monster posture, forward head or bent knees" (GO L48); "Supports the torso without permanent forward lean, exaggerated lumbar arch or hunch" (GO L191)
- [POS] Neck — "moderate vertical neck contribution with high structural integration into the shoulder/torso complex" (GO L46); "no required missing neck, bull neck or extremely short neck" (GO L46); low-muscle "still has substantial skeletal neck integration, never dependent on trapezius" (GO L192)
- [BAN] "Gorrund are never enlarged Durrim" (GO L47)
- [POS] Height distribution — "extra stature distributes through spine, torso, pelvis, femur, lower leg, neck and head-body relationships" (GO L31)
- [POS] Linkage — "a large pelvic-breadth change needs validated hip-joint placement, femur alignment and gait" (GO L232); "pelvis, hip, femur and knee work as one biomechanical chain" (GO L232)
- [POS] ALPC (final clarification) — "the shoulder girdle, thoracic structure, lower axial trunk, pelvis and proximal lower limbs form a strongly integrated vertical load-bearing chain" (GO L711)
- [POS] ALPC is terminology, not a slider — "Axial Load-Path Continuity is project anatomical terminology, not a creator-facing slider." (GO L713)
- [BAN] ALPC misreadings — "never means uniform torso width, no waist, a rectangular or barrel body, a giant pelvis or shoulders, a thick abdomen" (GO L713)
- [POS] ALPC thorax→lower trunk — "transitions without abrupt skeletal collapse, while visible waist definition, narrower frames, low fat and athletic composition stay valid" (GO L718)
- [POS/OPEN] ALPC lower trunk→pelvis — "The pelvis reads as integrated with the axial body, not an independently widened hip structure; morphology stays OPEN but its relationship to the torso is now positively constrained" (GO L719 — 29 words; truncated quote: "The pelvis reads as integrated with the axial body, not an independently widened hip structure")
- [POS] ALPC pelvis→leg — "Hip-joint scale, proximal femur, pelvis and upper-leg dimensions suit receiving load from the pelvis and axial skeleton, never mandatory enormous thighs" (GO L720)
- [TEST] ALPC Narrow frame "(a critical identity test)" (GO L721); low muscle "it fails if it appears only once muscle is added" (GO L722); fat "Low fat reveals rather than creates the structure" (GO L723)
- [POS] Torso verticality vs Durrim — "substantial ribcage vertical length and large axial vertical contribution suited to a tall body, so a Gorrund is never a vertically scaled Durrim" (GO L733)
- [TEST] Matched-display silhouette test vs Durrim and "Equalized torso-breadth test" — "stay distinct through torso vertical relationships, limb contribution, pelvic relationships" (GO L735)
- [TEST] Equal-height Grask — "Gorrund: greater axial contribution, thoracic breadth and depth, joint presence, larger load-bearing relationships and pelvis-torso integration." (GO L238); Skarn — "distinct joint, torso and pelvis relationships. Fails as "extra-broad Skarn"" (GO L239); Aelari — "different torso, pelvis and limb organization" (GO L265); AD-3 low-breadth Gorrund vs Broad Grask "Numeric validator deferred to approved reference meshes (RM-LR-04)" (GO L244); AD-1 Skarn boundary "Axial Load-Path Continuity" as carrier (GO L271)
- [TEST] Stress GOR-STRESS-06 — "06 greater thoracic depth with lower breadth" (GO L249)
- [POS] AD-4 — "Skarn–Gorrund torso and limb proportional separation is undetermined by design (AD-4)" (GO L675); "no Gorrund torso-share or limb-share relationship to Skarn is defined" (GO L675)
- [POS] Separation from Durrim/Grask/Skarn — "This separates Gorrund from Durrim compact structural concentration as well as from Grask limb-dominant reach specialization" (GO L739)
- [BAN] ALPC and TSC never merged — "never collapse into one universal Gorrund slider" (GO L741)
- [OPEN] "torso-to-limb proportions; ribcage, shoulder and pelvic morphology" (GO L159); "body ratios; pelvic morphology" (GO L699); "sex-related anatomy and dimorphism" (GO L159, L699)
- [REPRO] "Lifespan, maturation, fertility, senescence and developmental timing are OPEN, with no numbers." (GO L531)
- [SILENT] No sacrum, no pelvic tilt, no numeric torso share; ALPC proxy measurement only queued (RM-LR-06, RMQ L32).

## 11. Pipkin (incl. Low-Set Compact Trunk Architecture)

- [POS] Part 1 torso — "Compact for the stature but less broad, deep and structurally massive than Durrim at matched height" (PK L41)
- [POS] Torso vertical contribution — "Moderate, never compressed to Durrim levels just because both are short" (PK L42)
- [POS] Thoracic depth — "deep load-bearing thorax isn't the specialization" (PK L44)
- [POS] Neck — "Adult, never a tiny child neck, a Durrim-like compact heavy neck or an Aelari-like elongated neck by default (relationships later)" (PK L48)
- [POS] Spine — "Upright adult humanoid spinal alignment, no mandatory hunch, crouch or lean" (PK L49)
- [POS/BAN] Pelvis (P1) — "never a scaled-down juvenile pelvis (mandatory) and never Durrim pelvic proportions reused because both are short" (PK L50); "morphology OPEN" (PK L50)
- [POS] LSCTA definition — "a mature, structurally broad pelvis contributes strongly to the central body silhouette while the thorax remains comparatively moderate in breadth and depth" (PK L133)
- [POS] Core chain — "moderate thorax → compact lower trunk → mature structurally broad pelvis → proportionally sustained limbs" (PK L135)
- [POS] "Low-set" defined — "means the relative structural importance of the lower trunk and pelvis within the adult body, never a sagging torso, low posture, short legs" (PK L135)
- [BAN] "Compact trunk never means Durrim-like vertical compression, no waist, a barrel or round body or high fat" (PK L135)
- [POS] Concrete tendency — "a modestly reduced vertical central-trunk contribution to total stature, a compact lumbar/waist transition" (PK L137)
- [POS] Pelvic participation — "a mature pelvis whose vertical height, depth and three-dimensional structural participation remain substantial relative to the thorax" (PK L137)
- [POS] Persists at human-like breadth — "This lower-trunk-centered organization persists even when pelvic breadth approaches Marchfolk-like values." (PK L137)
- [POS] Absorption — "absorbed primarily through sustained limb contribution and pelvic vertical contribution, not through enlargement of the head" (PK L137)
- [OPEN] T-2 — "The numeric split between limb and pelvic contribution stays deferred (UCCA RM-UB-01; short-race RM-SR items); no winner is invented." (PK L139)
- [POS] Thorax vs pelvis — "The pelvis carries greater structural importance relative to the thorax than in Marchfolk reference anatomy" (PK L150)
- [BAN] Pelvic breadth — "never extremely wide hips, feminized anatomy, high fat or one hourglass silhouette; this is skeletal anatomy" (PK L151)
- [OPEN] Pelvic depth — "Appropriate adult three-dimensional depth, never a widened scaled human pelvis (morphology OPEN)" (PK L152)
- [POS] Maturity — "Fully mature adult anatomy, especially important for the adult Pipkin and human child test" (PK L153)
- [POS] Like-for-like sex comparison — "racial identity is never defined by shoulder-to-hip ratio or external hip circumference" (PK L154)
- [BAN] Transition — "never an abrupt "small chest → huge hips"" (PK L156)
- [POS] Waist/abdomen — "a lean flat-bellied Pipkin is fully recognizable" (PK L157)
- [POS] vs Durrim pelvis — "the two never share one pelvis (morphology for later prototyping)" (PK L162)
- [POS] Frame — "Narrow never erases the Pipkin pelvic relationship and Broad never exaggerates it into caricature" (PK L168)
- [TEST] Durrim boundary ~122 cm — "Pelvic breadth is not the primary discriminator." (PK L194); human adult test "thorax-pelvis relationship, compact trunk organization, mature pelvic contribution" (PK L192); PIP-BODY-15 child test "thorax, shoulder girdle, mature pelvis, limb segmentation" (PK L193); PIP-BODY-16 (PK L196); "Lower valid pelvic breadth stays Pipkin, so pelvic width alone isn't the identifier" (PK L198); PIP-BODY-17/18/19 (PK L213–215); PIP-BODY-28/29 like-for-like male/female (PK L224–225); PIP-STRESS-06 "Greater pelvic contribution with lower thoracic breadth, coherent" (PK L234); PIP-STRESS-07 "(the race isn't one hip-width ratio)" (PK L235); PIP-INT-03 trunk readable with head/hands/feet hidden (PK L1597)
- [POS] Mandatory links — "thorax and pelvis, pelvis and proximal leg, torso vertical and limb contribution" (PK L207)
- [BAN] Posture — LSCTA "does not require" (PK L703) items including "exaggerated lumbar arch" (PK L709) and "or a childlike stance." (PK L712); "Standing posture must remain compatible with the mature pelvis, moderate thorax, compact lumbar/waist transition" (PK L714)
- [POS] Gait — "an adult narrow-base gait" (PK L746); "movement must not turn that into exaggerated side-to-side hip motion" (PK L750); "The compact lumbar/waist transition coordinates with the thorax rather than behaving as a rigid block." (PK L752)
- [POS] Equipment — "Waist placement cannot be inferred from total character height or copied from Marchfolk normalized percentages." (PK L1176)
- [BAN] Randomization package — "broad pelvis + exaggerated hip circumference" (PK L1419)
- [POS] Identity hierarchy — "1. Primary: Low-Set Compact Trunk Architecture." (PK L1502)
- [POS] Sex — "Sex-related physical anatomy may influence relevant pelvic, thoracic, facial, soft-tissue and other biological relationships" (PK L1491)
- [OPEN] "detailed torso ratios within Low-Set Compact Trunk Architecture" (PK L1535); "detailed pelvic morphology, including depth and implementation-ready dimensional relationships" (PK L1537); "magnitude and morphology of sex-related dimorphism" (PK L1545)
- [REPRO] "Exact maturation timing, lifespan, senescence curve, fertility timing and age-frequency distribution require later world/lifecycle design." (PK L1485)
- [SILENT] No sacrum, no explicit tilt (only "no permanently flexed hips"), neck length relationships deferred ("relationships later", PK L48).

## 12. Cogling

- [POS] Identity — "organized around a narrow stable central core and near-human total limb contribution" (CG L33)
- [POS] Central body — "total torso contribution remains broadly near the Marchfolk adult range rather than becoming strongly limb-dominant" (CG L100)
- [POS] Thorax/pelvis — "The pelvis is mature and integrated without becoming the dominant silhouette anchor." (CG L102)
- [OPEN] "Exact thorax-to-pelvis and torso-to-limb ratios remain OPEN pending validation." (CG L110)
- [POS/BAN] Pelvis (P1) — "Cogling possess a fully mature adult pelvis." (CG L256); must not become "childlike/narrow through immaturity" (CG L259), "Pipkin's primary lower-trunk identity mechanism" (CG L260), "Durrim-like structural mass" (CG L261), "or an external hip-width stereotype." (CG L262)
- [OPEN] "Pelvic breadth, depth, height and sex-related morphology remain OPEN for detailed Part 2 work." (CG L264)
- [POS] Neck (P1) — "disproportionately thick Durrim/Gorrund-like neck" banned (CG L270); "Neck length and circumference vary with frame, sex-related anatomy, muscularity and individual genetics." (CG L272)
- [POS] Core defined — "The central core consists of the thorax, spinal trunk and pelvis as an integrated adult structure." (CG L647); "a comparatively narrow transverse core while retaining sufficient depth and pelvic maturity" (CG L649); "Stable" "not superior gameplay balance" (CG L653)
- [BAN] Thorax — must not become "or an hourglass device." (CG L669) (also flattened/pinched/childlike/Durrim-deep/Gorrund-massive, CG L664–668)
- [POS] Waist/lumbar — "Cogling may show a readable waist/lumbar transition, but no narrow-waist stereotype is required." (CG L675); "The waist is an anatomical transition between thorax and pelvis, not a cosmetic cinch point." (CG L677)
- [POS] Pelvis (P2) — "Compared with Pipkin, the pelvis does not carry the same primary silhouette role relative to the thorax." (CG L685); "Compared with Durrim, it has lower structural mass and breadth/depth emphasis." (CG L687)
- [OPEN][REPRO] "Exact pelvic breadth, depth, height, inlet/outlet morphology and external soft-tissue expression remain OPEN." (CG L691); final list "pelvic morphology, including breadth, depth, height, inlet and outlet relationships" (CG L3163) — inlet/outlet is obstetric-adjacent; only named as OPEN.
- [POS] Axial length — "Cogling do not require a shortened spine, long waist or compressed vertebral column." (CG L705); "Total axial contribution remains adult and broadly balanced with the near-human total limb share." (CG L707); "Posture is not used to create apparent smallness." (CG L709)
- [BAN] Neck (P2) — "No mandatory thin neck, thick neck or forward-head posture is approved." (CG L723)
- [POS] Sex — "No single shoulder-to-hip ratio, chest form, waist shape or external hip width defines either Cogling sex-related anatomy or Cogling racial identity." (CG L877); "Magnitude and detailed morphology remain OPEN." (CG L879)
- [TEST] COG-BODY-09/09A vs Pipkin (CG L461–462); COG-BODY-10 vs Narrow Durrim "narrow central core" (CG L463); COG-BODY-11 toddler test "adult skeletal, pelvic, facial-development boundary" (CG L465); invalid combo "minimum shoulder/pelvic maturity producing a toddler read" (CG L1051); overlap carriers "adult axial/trunk contribution broadly near the Marchfolk adult range" (CG L901)
- [SILENT] No sacrum, curvature or tilt beyond "upright"; no neck-share direction (only variation and bans).

## 13. Saurin (incl. integrated pelvis / sacral / tail base)

- [POS] Body anchor — "deep mobile thorax → elongated lower axial trunk → strongly integrated pelvis/sacral base → substantial counterbalancing tail" (SA L56)
- [POS] Centerline continues — "a body whose centerline continues functionally through the pelvis into the tail rather than ending visually at a human-like sacrum" (SA L58)
- [POS] Tail is axial — "It is part of the approved axial architecture." (SA L60)
- [POS] Axial trunk — "lower axial trunk has greater longitudinal contribution than a typical Marchfolk relationship" (SA L96); "ribcage-to-pelvis transition remains visibly integrated rather than strongly pinched at a human waist" (SA L97); "lumbar/sacral organization must support the continuation into the tail" (SA L98); "the abdomen remains flexible and adult, not barrel-rigid" (SA L99)
- [OPEN] "Exact vertebral count and rib arrangement remain OPEN." (SA L103)
- [POS] Thorax — "moderate breadth" / "meaningful anteroposterior depth" / "long lower-rib/abdominal transition" (SA L110–112); "without copying Gorrund axial mass or Vael thoracic depth" (SA L107)
- [POS] Pelvis primary carrier — "The pelvis is a primary racial carrier." (SA L138); "comparatively strong posterior integration with the sacral/tail base" (SA L142); "no juvenile narrow pelvis" (SA L144); "no Gorrund-like massive load-bearing pelvis" (SA L145); "no Pipkin low-set compact-trunk specialization" (SA L146)
- [POS] "The posterior pelvis should read as designed around a real continuation of the vertebral axis." (SA L148)
- [POS] Pelvic-femoral — "longer front-to-back and more posteriorly organized in structural mass than the Marchfolk adult tendency" (SA L154); "This is not a crouched-lizard pelvis and does not force splayed legs." (SA L156)
- [POS] Tail origin — "emerges from integrated sacral/caudal anatomy" (SA L165)
- [POS] Center of mass — derived from "trunk proportions" / "pelvic architecture" / "tail mass/pose" (SA L241–244)
- [POS] Frame — "A Narrow Saurin remains Saurin through axial/pelvic/tail architecture." (SA L352); "A Broad Saurin cannot become Gorrund simply through breadth." (SA L354)
- [POS] Posture — "Neutral Saurin posture is upright and adult." (SA L411); not required to "hunch" / "crouch" / "thrust the head forward" (SA L414–416)
- [POS] Neck — "skull base accommodates an upright head over a non-human axial trunk" (SA L961); "neutral posture does not require forward-head carriage" (SA L964); "Exact occipital and cervical anatomy remains OPEN." (SA L966)
- [POS] Stature-share accounting — "neck-height share remains broadly near Marchfolk" (SA L970); "The elongated lower axial trunk is therefore paid for primarily through modestly reduced vertical head/thoracic contribution rather than by forcing shortened legs." (SA L970)
- [OPEN] "Exact proportional distributions remain OPEN and must still satisfy SAU-FACE-22." (SA L970); stature-accounting note "Part 2 must explicitly account for head, neck, thoracic-height, lower-trunk and leg shares" (SA L607)
- [POS] T-1 — "this stature-share statement is a reference / central-morphology description" (SA L972)
- [POS] Creator hard bounds (numeric, canon) — "neck length ±15 %; neck depth ±10 %; thoracic depth ±8 %; thoracic width ±7 %; axial trunk length ±10 %" … "pelvic width ±7 %" (SA L4166)
- [POS] Coupled — "thoracic depth/width ratio stays 0.80–1.00 (deep narrow-to-moderate shell)" (SA L4168)
- [POS] Frame scope — "Frame does not change stature, long-bone or axial lengths, the skull, or pelvic depth / sacral-caudal organization." (SA L4170)
- [POS] Tail coupling protects pelvis — "The frozen pelvis/sacral-caudal architecture is never altered to support tail extremes" (SA L4156)
- [POS] Balance — reference stance "would need ~8.8° of forward whole-body lean" … "Anatomy is not reopened for this." (SA L4162); "Living balance (axial inclination, pelvic organization, knees/ankles, tail carriage) is carried forward" (SA L4162)
- [POS] Sex (§263) — trunk-only dimorphism: "a longer lower axial trunk, a wider skeletal pelvic band, a fuller coelomic body wall and subtle ventral/ventrolateral fullness" (SA L407)
- [POS] Numeric sex centres — lower axial trunk "female distribution centre +7 %; male centre 0 %" inside "±10 % species bound" (SA L101; table SA L4227); pelvic band "female centre +5.5 %" inside "±7 % species bound" (SA L150; SA L4228)
- [BAN] "This is internal-capacity widening only: no human-style hip flare, paired buttocks or gluteal cleft" (SA L150)
- [BAN] "The female tendency is anti-hourglass: a fuller, continuous coelomic body wall and ventral organization, not a narrower waist." (SA L4221)
- [POS] Overlap — "Overlap is mandatory." (SA L4218); "sex never extends either bound" (SA L4250)
- [POS] Frozen under sex — "sacral platform; posterior pelvic mass; tail root" unchanged (SA L4255)
- [REPRO] Interpretation limited — "A and E: sex-correlated differences in coelomic/body-cavity capacity and body-wall organization." (SA L4239)
- [REPRO][BAN] "Excluded from Saurin baseline anatomy: mammary glands; lactation; nipples; human breasts; human external genital anatomy; human-style hip flare" (SA L4242); "No external primary-sex anatomy is modelled; the ventral pelvic field is identical in both sexes." (SA L4242)
- [REPRO][OPEN] "OPEN: internal gestation; egg vs live young; provisioning mechanism; reproductive organs and physiology" (SA L4244); also SA L4007, L4273
- [TEST] SAU-BODY-04 "Integrated-organism test" (SA L541); SAU-BODY-09 "Tail-base size and pelvic/sacral support remain coherent across tail extremes" (SA L546); SAU-BODY-10 "Neutral upright stance without hunch/crouch" (SA L547); SAU-BODY-12 "Vael-normalized torso comparison" (SA L549); SAU-BODY-14 Gorrund structural mass (SA L551); SAU-BODY-16 Durrim (SA L553); SAU-BODY-18 tail-integration stress (SA L555); SAU-BODY-19 sex configurations (SA L556); SAU-BODY-21/22 Skarn/Aelari (SA L558–559); SAU-SILHOUETTE "a substantial base anchored to the posterior pelvis" (SA L560); SAU-FACE-22 "head, neck, thorax, lower trunk and legs summing coherently" (SA L1263); SAU-MOVE-13 "pelvic → lower-axial → tail rotational flow" (SA L3432)
- [POS] Gait — "pelvic rotation → distributed lower-axial continuation → tail counter-response" (SA L2851)
- [OPEN] Part 1 — "pelvic morphology;" (SA L568), "sacral/caudal skeletal anatomy;" (SA L569), "exact vertebral/rib anatomy;" (SA L565); §265 "Numeric lower-trunk minimum relative to Marchfolk (§6) and a numeric Broad-vs-Gorrund boundary." (SA L4267); "Balanced neutral standing posture and living balance" (SA L4263)
- [SILENT] Pelvic tilt is not given as a number; "pelvic organization" in balance is deferred (SA L4162).

---

## Cross-race comparatives (explicit, with direction)

**Torso / axial share of stature**
- Skarn > Marchfolk — "a slightly larger torso share of total height" (SK L75)
- Sagekin < Marchfolk — "a slightly shorter torso relative to stature" (SG L139)
- Fenn < human (implicit Marchfolk) — "Slightly smaller torso share of height" (FN L50)
- Vael > Fenn — "Greater torso share than Fenn" (VL L35)
- Aelari > Fenn (torso relative to height) — "Longer than Fenn relative to height" (AE L48)
- Grask < Marchfolk, Skarn — "a lower contribution to standing height than Marchfolk and Skarn" (GR L37)
- Gorrund > Grask (matched height) — (GO L169)
- Gorrund vs Skarn/Marchfolk: undetermined by design (GO L675; LRR L53 "GO vs S n.d.; GO vs MF n.d.")
- Durrim > equal-height Marchfolk — (DU L97)
- Pipkin < Marchfolk (central trunk), "modestly reduced" — (PK L137; SRR L56)
- Cogling ≈ Marchfolk — "broadly near the Marchfolk adult range" (CG L100; SRR L59)
- Pipkin torso vertical contribution > Durrim compression — "never compressed to Durrim levels" (PK L42); Durrim "stronger torso vertical compactness" (PK L194)
- Saurin lower axial trunk > Marchfolk — (SA L96); head/thorax pays (SA L970)
- Elf ranking of waist/torso verticality: Aelari greatest — "The greatest average vertical torso continuity of the three" (ECR L46)

**Thoracic depth**
- Skarn > Marchfolk (SK L22, L75); Durrim > equal-height Marchfolk (DU L29); Sagekin < Marchfolk (SG L140); Fenn < Marchfolk and Vael (HV L456); Vael > Fenn, Aelari (VL L35, VL L120); Gorrund > Grask (GO L40); Gorrund "greater axial depth" than Skarn at equal height (GO L239); Grask never Durrim-like proportional depth (GR L39, L204); Pipkin "Durrim-deep" banned (PK L149); Cogling "Durrim-deep" banned (CG L667); Saurin "without copying … Vael thoracic depth" (SA L107)
- Undetermined: Skarn vs Grask depth (LRR L55 "S vs GR n.d."); Fenn vs Aelari ("no strict Fenn-Aelari thoracic ranking", HV L456)

**Neck**
- Aelari > humans and Fenn (AE L50); Aelari > Fenn and Vael (ECR L320, HV L458); Vael < Aelari, relative not absolute (VL L123)
- Grask "moderate-to-long relative to Durrim and Skarn" (GR L43; LRR L64 "GR > S (relative length)")
- Durrim "relatively short contribution to total height" (DU L21) — comparator unnamed in DU L21 (Marchfolk by context); DU L107 "Relatively short proportional contribution"
- Gorrund "moderate vertical neck contribution" (GO L46); Gorrund vs Skarn n.d. (LRR L64)
- Saurin neck share "broadly near Marchfolk" (SA L970)
- Pipkin: neither Durrim-compact nor Aelari-elongated by default (PK L48)
- Cogling: neither thin nor Durrim/Gorrund-thick (CG L270, L723)
- Skarn: substantial/thicker neck base vs Marchfolk (SK L23, L77) — base/structure, not length

**Pelvis (architecture, not numbers)**
- Skarn "more substantial pelvis" vs Marchfolk (SK L77); LRR L57 "Architectural difference only; morphology OPEN for Grask and Gorrund"
- Pipkin pelvis: greater structural importance relative to thorax than Marchfolk (PK L150); Durrim and Pipkin "never share one pelvis" (PK L162)
- Cogling pelvis: less silhouette role than Pipkin; lower mass than Durrim (CG L685, L687)
- Saurin pelvis: longer front-to-back and more posterior mass than Marchfolk (SA L154); not Gorrund-massive; not Pipkin LSCTA (SA L145–146)
- Elves: each distinct; "Pelvis is recorded as A plus E" — "shared non-human ancestry is locked, but the three pelvises aren't claimed to be identical" (ECR L37); Vael pelvis "not human, Fenn or Aelari" (VL L38)
- Gorrund pelvis integrated with axial body vs Durrim: "Equalized torso-breadth test … pelvic relationships" (GO L735)

**Torso–pelvis continuity**
- Durrim "strong torso-pelvis continuity" (DU L25); Vael "strong torso-to-pelvis continuity" (VL L35); Vael "more compact torso-to-pelvis continuity than Aelari" (ECR L257); Gorrund ALPC (GO L711); Saurin integrated ribcage-to-pelvis (SA L97)

**Center of mass**
- Durrim lower than "equivalently proportioned taller humanoids" (DU L34); Vael "lower center of mass than Aelari" (VL L165); Saurin COM includes tail (SA L238–246); no gameplay consequence anywhere (DU L34, GO L51, GR L46, SA L250, PK L68)

**Triangle summaries**
- Short: "Durrim concentrate structure. Pipkin organize a light adult body around a low-set compact trunk and mature pelvic foundation." (SRR L261)
- Large: Skarn human architecture vs Gorrund ALPC vs Grask reach (GO L675, L739); Saurin "Durrim — compact structural concentration;" listed as contrast (SA L3995); Saurin vs Aelari "lower-axial length is concentrated through the trunk-to-pelvis-to-tail system" (SA L514)

---

## Candidate classification (SUGGESTIONS ONLY — not canon)

Key: A = authorable qualitatively now from canon; B = direction now, number later; C = needs mesh measurement even for a useful answer; D = later biology; E = later system.

| # | Open pelvic / axial / neck question | Suggest | One-line justification |
|---|---|---|---|
| 1 | Marchfolk baseline pelvis, torso share, neck share | C | Every "than Marchfolk" comparison needs a measured reference; MF authors no shape or share (MF L15, L75; RMQ L27). |
| 2 | Skarn "more substantial pelvis" split into breadth/depth/height | B | Direction exists (SK L23, L77) but dimension is unspecified; numbers belong to RM-UB-01/02. |
| 3 | Skarn vs Gorrund torso/limb share | A (by design: no relation) | AD-4 states it is undetermined by design (GO L675); nothing further to author. |
| 4 | Gorrund pelvic morphology (GO L49, L189, L699) | B | Integration constraints and "meaningful breadth, depth and hip-joint scale" are authored (GO L189, L719); shape/numbers wait for RM-LR-06. |
| 5 | Gorrund ALPC quantitative proxy | C | Canon explicitly defers the numeric validator to reference meshes (GO L244; RMQ L32). |
| 6 | Grask pelvic morphology (GR L208) | B | Functional requirement locked (GR L208); no measured morphology; numeric bands via RM-UB-01. |
| 7 | Grask vs Skarn thoracic depth ordering | C | LRR marks it n.d. (LRR L55); no canon direction to extend. |
| 8 | Durrim pelvic morphology (DU L32, L108, L520) | B | Five qualitative constraints are set (DU L108); detail explicitly OPEN. |
| 9 | Durrim torso share number vs Marchfolk | C | Direction locked (DU L97); RM-SR-06 queues the measurement (RMQ L44). |
| 10 | Durrim L93 wording (torso/limb contribution) | A | Editorial clarification against DU L97/L119; no new biology. |
| 11 | Pipkin pelvic depth/height and trunk-share split (T-2) | B → C | Direction locked (PK L137, L150); split deferred to RM-UB-01/RM-SR-01 (PK L139; RMQ L39). |
| 12 | Pipkin neck relationships ("relationships later", PK L48) | A | Bans already bound the range (PK L48); a qualitative "adult, near-human" statement can be authored without numbers. |
| 13 | Cogling pelvic breadth/depth/height (CG L264, L691) | B | Relative rules vs Pipkin/Durrim exist (CG L685–687); numbers need meshes. |
| 14 | Cogling pelvic inlet/outlet relationships (CG L691, L3163) | D | Obstetric morphology; must not be invented (PR L95). |
| 15 | Saurin vertebral/rib count, sacral/caudal skeleton (SA L103, L565, L569) | D | Explicitly OPEN biology; frozen pelvis/sacral architecture must not change (SA L4156). |
| 16 | Saurin numeric lower-trunk minimum vs Marchfolk; Broad-vs-Gorrund boundary (SA L4267) | C | Requires Marchfolk and Gorrund measurement. |
| 17 | Saurin balanced standing posture / pelvic organization (SA L4162, L4263) | E | Carried to posture/locomotion/animation phase. |
| 18 | Saurin reproductive physiology (SA L4244) | D | Explicitly OPEN; R-SEX forbids inference. |
| 19 | Shared elven pelvic morphology (ECR L32, L37, L281; AE L126; FN L111; VL L124) | B → C | "A plus E": shared non-human foundation locked, shapes await prototype validation. |
| 20 | Halvren pelvic inheritance (HV L122, L437, L497) | D | Blocked on shared elven pelvis and sex-related system; "Never invented inside Halvren" (HV L497). |
| 21 | Elf neck relative length numbers (Aelari > Fenn, Vael) | B | Direction canon (ECR L320; VL L123); RM-OT-02 queues "neck relative length" (RMQ L90). |
| 22 | Fenn neck direction | A | ECR assigns "Intermediate" (ECR L31); can be restated in FN without numbers. |
| 23 | Sagekin ribcage: breadth vs depth | A | Editorial conflict between SG L89/L140 (depth) and HV L460 (breadth); resolution is wording, measurement in RM-OT-01. |
| 24 | Neck length as a creator control per race (AD-C10) | A | UCCA L78 binds neck length only where canon names it; listing which races name it is a reading task (bound: Saurin SA L4166; directional: AE, VL, GR, DU, GO). |
| 25 | Spinal/lumbar curvature per race | A (mostly SILENT) | Only bans (GO L191, PK L709, GR L44) and one positive (VL L121 "natural lumbar curve") exist; anything more would be new biology → D. |
| 26 | Pelvic tilt / orientation per race | E | No race authors tilt; DU treats pelvic orientation as individual posture (DU L430); Saurin defers pelvic organization to animation (SA L4162). |
| 27 | Sex-related pelvic dimorphism magnitude (Durrim, Grask, Gorrund, Pipkin, Cogling) | D | UCCA L355 carries it as BIO OPEN; R-SEX allows "no shift" as complete (PR L94). |
| 28 | Fertility/lifecycle tied to pelvis (MF L315, DU L520, GR L534, GO L531, PK L1485) | D | Lifecycle/fertility OPEN everywhere; not a pelvic-morphology input. |
| 29 | Torso share numeric bands (all races) | C | RM-UB-01 owns them (RMQ L79); canon supplies only directions. |
| 30 | Center-of-mass gameplay consequences | E | Every spec firewalls COM from gameplay (DU L34, GO L51, GR L46, SA L250). |
