> UCCA Phase 1 evidence appendix to `reviews/claude-ucca-01-requirements-matrix.md`. Line references are to the canonical race spec (or the named source) as of commit 89ca8f7. Extraction only: no canon is changed and nothing here is new biology. Tags: [ANAT] anatomical requirement · [DIR] direct control · [DER] derived/coupled · [SOFT] tendency · [VAL] validator · [LAT] latent/preset · [PRES] presentation · [DIAG] diagnostic · [OPEN] open/not authorized.

# UCCA extraction: Fenn (specs/fenn/FENN_V1.md, v1.5 first-pass complete)

Source: `specs/fenn/FENN_V1.md` (548 lines), cited as `Lnnn`. Comparative authority: `reviews/elf-comparative-review.md` (accepted, authority level 3), cited as `ECR Lnnn`. Per ECR L3/L302, the race spec stays authoritative wherever the ECR does not explicitly clarify or supersede it. Face anatomy is out of scope (UFCA_V1); face items appear only where they touch whole-character systems.

## 0. What the Elf Comparative Review settles for the Fenn BODY

| Topic | ECR settlement (Fenn) | Class | Effect on Fenn spec |
| --- | --- | --- | --- |
| Limb share / extremity contribution | "Strongest extremity contribution: long arms, strong forearm and lower-leg contribution, long hands, long narrow feet" (ECR L33); final matrix: "Greater extremity contribution relative to torso, stronger forearm and lower-leg proportional contribution" (ECR L279); hands/feet "Greater average elongation and narrowness" (ECR L280); movement: "relatively long forearms, relatively strong lower-leg contribution" (ECR L255). Shorthand "extremity-emphasized" (ECR L59, L275) | [SOFT] | Confirms L50–52, L121–124. Proportional wording governs (ECR L145: "longer forearm relative to total arm length" rather than "longer forearms") |
| Neck | "Intermediate" (ECR L31). Aelari have greater average neck length and proportional neck contribution than Fenn and Vael, with substantial overlap; absolute vs proportional neck length are distinct measurements (ECR L320). "Long necks aren't universally elven" (ECR L31, L129) | [SOFT] | Fills a Fenn-spec gap (spec only states "clean shoulder-to-neck line", L107) |
| Thoracic depth / torso | "Compact-centered torso, relatively shallow ribcage, strong extremity contribution" (ECR L29); final: "Compact-centered, relatively shallow ribcage, gradual waist transition within the compact Fenn system" (ECR L278). Waist-transition clarification: Fenn transition "may be relatively gradual or extended within the Fenn proportional system. This does not mean Fenn have a longer absolute or proportional waist transition than Aelari" (ECR L45); Aelari have a longer average waist region than Fenn and Vael (ECR L46) | [SOFT] | **Clarifies/supersedes reading of** L50 "longer waist transition" and L110 "relatively longer waist and lumbar transition" (see Extraction notes) |
| Frame / gracility | Fenn have the "Greatest average skeletal gracility of the three" (ECR L276, L312); ordering Fenn → Aelari → Vael is a population distribution "with substantial overlap, not a rigid rule" and "never becomes three fixed bone-thickness presets" (ECR L316). Gracility never means weakness, low muscularity, low body weight, frailty, small frame or low capability (ECR L316, L21). "Broad frames are valid for all elves"; Broad = broader skeletal relationships within the population range, never human/Skarn/Durrim skeleton, automatic muscularity or obesity (ECR L55) | [SOFT] / [VAL] | Confirms L4 (L44), L30–40, L115 |
| Composition | "No elven population is defined by low fat or low muscle. All three support low and high muscle, low and high fat, regional development, Narrow, Balanced and Broad frames, and age-related composition" (ECR L55) | [ANAT] | Confirms L58, L130 |
| Pigmentation | Corrected Fenn range (Part 3 clarification, ECR L223; matrix ECR L157): fair and light, intermediate beige and tan where appropriate, olive, copper and bronze, brown, rich deeper brown, other compatible variants; undertones cool, neutral, warm, olive, golden, reddish/copper-influenced where appropriate. Not universally warm/tan/brown/olive/bronze/green/"forest colored". Frequencies E. Fenn–Aelari overlap locked (ECR L225); validity ≠ frequency (ECR L229); pigmentation isn't identity, must survive neutralization (ECR L161); no universal elven complexion (ECR L213); lighting invariance (ECR L165) | [SOFT] / [VAL] / [OPEN] | **Supersedes/extends** L244 (adds "cool" undertones as full member and "reddish or copper-influenced"; spec said "some cooler ones") |
| Hair | Biology vs presentation split (ECR L171); texture straight/wavy/curly/tightly curled or coiled, no "Fenn-wavy" assumption, frequencies E (ECR L172); natural colour distributions population-specific, frequencies unresolved (ECR L173); natural silver/white ≠ age depigmentation (ECR L174, L290); facial hair not prohibited, clean-shaven not universally elven (ECR L175); Fenn hair "Frequencies unresolved" (ECR L285) | [ANAT] / [OPEN] | Consistent with L262–268; frequencies still open despite L264 "wait for the comparative elf review" |
| Age | All three visibly age; may affect skin elasticity, facial volume, eye region, cheeks, jawline, neck, wrinkling, hair density/pigmentation, body composition, posture where individually appropriate, ear tissue (ECR L245). Lifespan, maturation, adult aging rate, fertility span, same-rate question = E (ECR L245, L116, L298). Biological age vs age presentation separate (ECR L245). "Old elves are never just young elves with white hair" (ECR L245) | [ANAT] / [OPEN] | Confirms L199; lifespan stays open |

Also settled, body-relevant: shoulders/clavicles "Gracile, tied to extremity-emphasized anatomy" (ECR L30); pelvis "Supports compact center and long extremities (E in detail)" (ECR L32), final "Prototype validation" (ECR L281); hands "Strong elongation, narrow and gracile" (ECR L34); feet "Longer and narrower" (ECR L35); height 157–211 cm ref ~181 (ECR L28, L277); movement biomechanics, "Not automatically: Sneaky, crouched, acrobatic, animal-like, permanently graceful" (ECR L255); sneak/swim traits kept as prototype gameplay facts, biology status OPEN (ECR L187, L236); Fenn low-light vs Marchfolk OPEN (ECR L298).

## A. Stature and proportions

**A1 Height**
- [ANAT] Minimum 157 cm (about 5'2"), Reference 181 cm (about 5'11"), Maximum 211 cm (about 6'11") — §2 L22–24; ECR L28, L277.
- [SOFT] "substantial overlap with Marchfolk and Sagekin, and height never defines Fenn" — §2 L26.
- [OPEN] "These values await visual and technical validation." — §2 L26 ("provisional", L20).
- Distribution shape: SILENT. ECR: "Height … Not an elven trait: elves aren't universally tall" (ECR L28).

**A2 Torso length/depth/width**
- [SOFT] "Slightly smaller torso share of height, somewhat less ribcage depth, more compact chest, longer waist transition" — §5–7 L50 (waist wording clarified by ECR L45; see §0).
- [SOFT] Ribcage "Somewhat shallower front to back, moderately narrow for height, somewhat vertically compact, with a relatively longer waist and lumbar transition" — v1.1 §2–4 L110 (waist clarified by ECR L45).
- [VAL] "Enough thoracic volume, never an implausibly tiny chest" — L110.
- [SOFT] "a shallower upper torso than humans" — L107.
- [DIR] Torso length, ribcage width and depth, shoulder width, waist, pelvis width — L50.

**A3 Limbs & segment proportions**
- [SOFT] "longer limbs relative to the torso" — §3 L35.
- [SOFT] Arms: "Longer arms relative to torso, slightly longer forearms, longer hands and fingers, narrower wrists" — L51; "Longer arms, somewhat greater forearm share" — L121.
- [SOFT] Legs: "Greater leg share of height, slightly longer lower legs, narrower ankles, somewhat longer feet than same-height humans" — L52; "Greater leg share, slightly greater lower-leg share" — L123.
- [DIR] Arm length, upper-arm and forearm proportion, (thickness, regional muscle) — L51, L121. Leg length, thigh and lower-leg proportion, thigh and calf development/thickness, regional muscle — L52, L123.
- [DER] "Shoulder, elbow and wrist alignment is kept"; "Hip, knee and ankle relationships are kept" — L121, L123.
- [DER] Structural proportion rule: "Changing one region may bring bounded supporting changes in related anatomy. The player sets the intended proportion, and the system keeps it coherent." — v1.1 §1 L103.

**A4 Shoulder/pelvic relationships**
- [SOFT] "Moderately long clavicles, a shallower upper torso than humans, less massive shoulder joints, a clean shoulder-to-neck line, broad individual width variation" — L107.
- [VAL] "Broad Fenn shoulders stay light-boned, never Skarn-like" — L107.
- [ANAT] Pelvis: "A distinct elven pelvis, not a scaled human one, supporting longer femurs, stable hips, light visual build, Narrow to Broad frames, plausible muscle attachment and natural locomotion" — L111.
- [OPEN] "Exact shape awaits prototyping, and not every Fenn has narrow hips" — L111; ECR L32, L281 (shared pelvic morphology E).
- [ANAT] "different shoulder and clavicle relationships"; "different pelvis-to-leg relationships" — §3 L37–38.

**A5 Neck**
- [SOFT] "a clean shoulder-to-neck line" — L107. No Fenn neck-length tendency stated: SILENT in spec; ECR: "Intermediate" (ECR L31); Aelari > Fenn on average (ECR L320).
- [ANAT] Neck keeps coherent placement and articulation across full range — v1.5 §2 L439.
- [ANAT] neck tissue aging — L199 (see F).

**A6 Hands/feet**
- [SOFT] Hands: "Longer palms and fingers, somewhat narrower hands and wrists" — L122.
- [DIR] "Overall hand scale, palm length and breadth, finger length and thickness. No per-finger length controls yet" — L122.
- [SOFT] Feet: "Somewhat longer and narrower, with normal humanoid toes" — L124; §3 L36.
- [DIR] "Foot length and breadth" — L124.
- [VAL] "No prehensile, gripping or animal-like feet" — L124.
- [VAL] "Hands stay compatible with weapon grips, shields, tools, environment interactions, animation and IK. Forest and canopy skill doesn't need biological gimmicks." — L126.

**A7 Reach-related anatomy**
- [OPEN] "The capsule, height, width, melee reach, interaction reach, step height and climbing reach are still to decide. Cosmetic differences never automatically become gameplay effects." — v1.5 §18 L499; ECR L269.
- [VAL] Climbing: "Reach, hand and foot placement, body clearance, mantling and ledge transitions get validated. Cosmetic proportions never give climbing advantages without a dedicated gameplay review." — L459.

**A8 Posture / Anatomical Resting Alignment**
- SILENT as a named concept in the Fenn spec (the term is defined in Aelari §13 L68). [OPEN] Balance/center of mass "to investigate" — v1.0 §10 L66. Aging may affect "body composition and posture" — L199.

**A9 Population-specific axial structures**
- SILENT (no tail or other axial structure).

**A10 Head-to-stature**
- SILENT on head-to-stature ratio. [SOFT] Cranium "Slightly greater cranial height relative to face, somewhat narrower skull" — L172 (face-level; UFCA governs). [VAL] Landmarks "neck and head keep coherent placement and articulation across the full valid range" — L439.

## B. Skeletal Frame
- [SOFT] "a more gracile skeleton, with lower skeletal mass for their height"; "narrower joints and slenderer long bones" — §3 L32–33.
- [ANAT] "Gracile never means fragile. The anatomy looks naturally adapted, not like weakened human anatomy." — L40; ECR L21.
- [DIR]/[ANAT] "Narrow, Balanced and Broad all apply inside Fenn anatomy. A Broad Fenn is still biologically Fenn, and Narrow isn't the only authentic look." — §4 L44.
- [SOFT] Joint scale: "Wrists, elbows, knees and ankles look smaller relative to limb length than on same-height humans, with minimum anatomical boundaries." — v1.1 §5 L115.
- [VAL] "A Narrow, low-muscle, low-fat Fenn never gets implausibly tiny or fragile joints." — L115.
- [SOFT] Gracility ordering: Fenn greatest of three, overlap, not presets — ECR L312, L316.
- Frame semantics (what Narrow/Broad changes in the skeleton): SILENT in Fenn spec beyond L44/L107; ECR universal: Broad = "broader skeletal relationships within that population's range" (ECR L55).

## C. Physical Composition
- [ANAT] "Muscle, fat, regional development and conditioning all vary. Very lean, average, Broad-framed, highly muscular, high-body-fat and elder Fenn are all explicitly allowed. Fenn identity never depends on thinness, and muscle and fat modify the Fenn foundation rather than replace it." — §8 L58.
- [VAL] "The same composition settings act on each race's own foundation." Highly muscular Marchfolk/Skarn/Sagekin/Fenn comparison; "soft tissue never erases the Fenn skeleton" — v1.1 §10 L130.
- [VAL] Composition stress set: Narrow+lean, Narrow+muscular, Balanced+high fat, Broad+lean, Broad+muscular, Broad+high fat, Elder+muscular, Elder+high fat — v1.4 §6 L349.
- Muscular Development Capacity vs Current Muscularity split: SILENT. Fat distribution pattern: SILENT. Population-specific tissue systems: SILENT.
- [DIR] thigh and calf development/thickness, regional muscle — L52, L121, L123.

## D. Biological surface
- [SOFT] Natural pigmentation range — v1.3 §2 L244 (superseded/extended by ECR L223, see §0). [VAL] "There's no naturally green skin as a default Fenn trait." — L244. [OPEN] "Frequencies are unresolved." — L244; ECR L157, L223.
- [ANAT] "Shared elven ancestry doesn't mean one elven complexion … racial identity never rests on one skin value." — v1.3 §1 L240.
- [ANAT] Four layers: natural (pigmentation, undertone, complexion, freckles, moles, birthmarks), environmental (sun and tanning, weathering, roughness, dryness, calluses, localized wear, dirt), applied (tattoos, body paint, makeup, ceremonial markings), acquired (scars). "Natural pigmentation and tanning stay separate." — v1.3 §5 L256.
- [DIR] "The face, hands, forearms, feet and general exposed skin keep regional controls where feasible." — v1.3 §6 L260. [VAL] "Fenn aren't automatically weathered for living in or coming from forests. Individual history decides." — L260.
- Material/finish, perfusion: SILENT in spec; ECR: living biological skin with perfusion where appropriate; no universal "elven skin material"; physiology/material differences E (ECR L151).
- [VAL] Lighting invariance (universal) — ECR L165.

## E. Hair / homologues
- [SOFT] Texture "straight, wavy, curly, and tightly curled or coiled"; colors "black, dark brown, brown, lighter brown, auburn, red, and blond or light shades where valid" — v1.3 §7 L264. [OPEN] Frequencies — L264; ECR L172–173, L285.
- [PRES] "Long hair, braids, and leaves, flowers, feathers, twigs or other forest decoration are never biologically required … go bald or closely shaved where appropriate. A Fenn without Fenn-style hair still looks Fenn." — v1.3 §8 L268.
- Body hair: SILENT. Facial hair: SILENT in spec (pointer: ECR L175, not prohibited; eyebrow hair → UFCA slot 11, L162).
- Natural silver/white: SILENT in Fenn spec colour list; ECR L174 rule applies "where valid".

## F. Age
- [ANAT] "Fenn visibly age. Age can affect facial volume, skin elasticity, the eye area, cheeks, jawline, neck tissue, wrinkles, hair density and color, ear tissue (subtly), and body composition and posture." — v1.2 §12 L199.
- [OPEN] "Lifespan and aging rate aren't set yet and are logged for lore review." — L199; ECR L245, L298.
- [VAL] Elder validation: FN-23 (L228), FN-30, FN-31 (L400–401), Elder test (L529). Failure: "Mandatory youthful appearances" (L416).
- Adult scope / maturation: SILENT (ECR L245 maturation E).

## G. Sex-related anatomy
- SILENT. The Fenn spec contains no sex-related anatomy statement and no R-SEX pointer. Partial hint: "not every Fenn has narrow hips" (L111). Reproductive biology: SILENT (ECR L245: fertility span E).

## H. Asymmetry & acquired history (non-facial)
- Natural body asymmetry: SILENT (ear asymmetry only, L191; face asymmetry L177).
- [ANAT] Acquired layer = scars — L256. Acquired ear damage "belong to scars and acquired appearance, never to racial anatomy" — L195; ECR L112 (shared principle).
- Missing/damaged body structures: SILENT. Tail: N/A.

## I. Presentation
- [PRES] Hair presentation not biological — L268.
- [PRES] Tattoos, paint and markings: "cultural and acquired, never required for Fenn ancestry" — v1.3 §14 L300.
- [PRES] Clothing/materials, no universal "leaf" clothing — L292; motifs — L296.
- [PRES] Presentation presets "never overwrite race, skeleton, face, ears, height, composition or natural pigmentation" — v1.4 §2 L333.
- [VAL] Culture separation: "Culture never changes biology. A Marchfolk raised among Fenn stays anatomically Marchfolk, and a Fenn raised abroad stays Fenn." — L312; table L304–310; ECR L191.
- [VAL] Movement: "no exaggerated 'graceful elf' animation just because they're elves. Movement comes from anatomy, physical state, equipment, training and gameplay needs." — v1.5 §4 L447. Five movement layers (anatomy / learned / cultural body language / personal / emotional) — ECR L249.
- Body language vs resting alignment: SILENT in spec (see ECR L249).

## J. Creator system
- [LAT] Character presets (provisional): Canopy Pathfinder, Forest Artisan, Broad Warden, River Traveler, Heavyset Trader, Elder Storykeeper, Foreign-Raised Fenn, Young Wanderer — v1.4 §1 L320–327. "visual starting characters only … never assign class, stats, personality, permanent occupation, background or abilities, and all are reproducible and fully editable" — L329.
- [PRES] Presentation presets: Canopy Practical, Forest Formal, Trail-Worn, Ceremonial, Artisan, Foreign/Urban — L333.
- [LAT] Generation sequence (conceptual): foundation → skeletal and frame variation → body proportions → physical composition → facial anatomy → ear anatomy → pigmentation and hair → individual details → cultural and personal presentation — v1.4 §3 L337.
- [LAT]/[VAL] "Sliders are never randomized independently." Preserved relationships: limb-to-torso, upper and lower limb, joint-scale, hand and wrist, foot and ankle, shoulder and ribcage, pelvis and leg, craniofacial, ear-to-skull — §4 L341.
- [VAL] "Randomization never produces a human body plus a human face plus pointed ears." — §5 L345.
- [LAT] Biology vs presentation randomization (proposed universal) — §12 L380–385.
- [LAT] Deterministic generation from stored data or seeds (NPC persistence, save/load, testing, bug reproduction, presets, networking) — v1.5 §22 L515.
- [ANAT] Unified record: "ancestry, skeleton and body, composition, face, age and identity, skin, hair, markings and presentation" — not requiring same skeleton/mesh/morph — §20 L503; shared vs race-owned table L507–509.
- Simple/Advanced: SILENT. Locks: SILENT. NPC parity: only via L515.
- [VAL] First-person arms: "Fenn keep their own arm, forearm and hand proportions, skin and equipment. They're never silently swapped for generic human arms. The architecture is unresolved." — §15 L487.
- [VAL] Cameras: "There's no single camera height for every race and body." — §14 L483.
- [VAL] Equipment: clothing/armor must fit every valid height, frame, limb proportion, muscle, fat and age — §10 L467; ears/headgear — §11 L471; footwear vs longer, narrower feet — §13 L479; "Canonical weapon dimensions never scale with hand size" — §6 L455.
- [VAL] World compatibility list — §16 L491. [OPEN] Mounts — §17 L495.
- [OPEN] Skeleton architecture: none chosen; scaled human skeleton/stretched bones/MetaHuman not assumed — §1 L435; ECR L265.

## K. Locked validation tests (body / whole-character)
- FN-01 Reference 181 cm Balanced; FN-02 157 cm; FN-03 211 cm; FN-04 Narrow very lean; FN-05 Broad; FN-06 Broad highly muscular; FN-07 High body fat; FN-08 Long torso against population average; FN-09 Short-limbed near racial boundary; FN-10 Hidden-ear human-overlap stress — L84–93.
- FN-11 Broad high muscle; FN-12 Narrow high muscle; FN-13 Broad high fat; FN-14 Narrow low muscle low fat joint stress; FN-15 Max arm+hand combination; FN-16 Max leg+foot combination; FN-17 Sagekin/Fenn proportional boundary — L146–152.
- (Face-set FN-18–FN-27, L223–232; whole-character relevant: FN-22 high-body-fat facial, FN-23 Elder.)
- FN-28 Broad high-muscle silhouette; FN-29 Broad high-fat silhouette; FN-30 Elder muscular; FN-31 Elder high fat; FN-32 Minimum-ear full-body; FN-33 Maximum-ear full-body; FN-34 Neutral-presentation randomized; FN-35 Marchfolk-culture Fenn; FN-36 Sagekin-culture Fenn; FN-37 Hidden-ear randomized boundary; FN-38 Valid extreme randomization — L397–407.
- Hidden-ear validation (body) — §13 L78. Hidden-ear population test (100 Marchfolk / 100 Sagekin / 100 Fenn) — v1.4 §7 L353. Silhouette validation — §8 L357. Subtle-ear validation — §10 L365.
- Final gate (20 checks: hidden-ear body/face, min/max ear, Narrow, Broad, high-muscle, high-fat, elder, extreme-valid-proportion, animation, facial-expression, IK/contact, weapon-grip, equipment-fit, headgear/ear, world-compat, cross-cultural, save/load reproduction, population-randomization) — v1.5 §23 L521–540.
- Animation/IK tests — §3 L443, §5 L451. ECR shared tests: neutralization and equal-height (ECR L63), equal-body-condition movement (ECR L261), neutral material/grayscale/hair neutralization/random population (ECR L201–205).

## L. Positive body identity statement
- "Fenn identity comes from the whole anatomical system: limb-to-torso relationships, long-bone proportions, skeletal robustness and joint scale, ribcage, shoulder and clavicle relationships, pelvis and leg relationships, hands, fingers and feet, craniofacial anatomy, external ears. Pointed ears are only one part." — §1 L7–18.
- "Fenn are the first playable race with a genuinely non-human skeleton, and they are never thin humans with pointed ears." — L3.
- Silhouette: "Fenn read through limb length, forearm and lower-leg proportions, torso share, ribcage, shoulders, joint scale, hands and feet combined." — L357.
- ECR: "Fenn are extremity-emphasized" (ECR L59); "Extremity-emphasized specialization" (ECR L275).

## M. Cross-population boundary tests (body)
- Marchfolk/Sagekin/Fenn "of about equal height", matched, ears hidden — L78 (stature: unspecified "about equal").
- Sagekin boundary: "Sagekin are the long-limbed end of fully human variation, and Fenn have a genuinely different elven skeleton … never just from longer human sliders." — L138; L74; L544; FN-17 L152.
- Highly muscular Marchfolk, Skarn, Sagekin, Fenn comparison — L130 (stature: SILENT).
- Fenn compared against Marchfolk, Sagekin, Skarn, later Aelari and Vael — L544.
- ECR equal-height three-elf test "at identical height" (no number) — ECR L63; Aelari spec uses about 190 cm for Fenn/Aelari (AELARI L169).

## N. Forbidden controls / anti-patterns (body)
- "never longer human sliders" — L138. Not "a scaled human skeleton … human bones can simply be stretched" — L435.
- "nothing is exaggerated into animal-like anatomy" — L54.
- "Sliders are never randomized independently" — L341.
- No per-finger length controls yet — L122.
- Failure conditions: human bodies with pointed ears; mandatory thin physiques; mandatory youthful appearances; mandatory conventional attractiveness; excessively similar pigmentation; mandatory long hair or braids; mandatory forest decoration; implausible extreme proportion combinations; Broad/muscular Fenn losing elven skeleton — L413–423.
- Cosmetic body settings never give automatic gameplay advantages — L66, L499.
- Ears never "clipping … hidden or deleted for every helmet … flattened … all headgear made Fenn-only" — L471.
- Exaggeration not the fix — ECR L294.

## O. OPEN / DEFERRED (body / whole-character)
- Height values await validation — L26.
- Combined-proportion validation method "isn't chosen yet" — v1.1 §11 L134.
- Exact pelvis shape — L111; ECR L32, L298.
- Balance/movement implications — L66; exact biomechanical consequences — ECR L298.
- Sneak/swim traits: unquantified — L70, L463; biology status OPEN — ECR L236.
- Lifespan/aging rate — L199; ECR L298.
- Low-light vision vs humans — L272; ECR L298.
- Pigmentation/hair frequencies — L244, L264, L389; ECR L157, L213.
- Skeleton architecture, MetaHuman — L435; ECR L265.
- Headgear/ear architecture — L471; first-person arms architecture — L487; mounts — L495; collision/reach — L499.
- No RM-* references in the Fenn spec.

## P. Pass 1 provisional creator-control lists (BODY)
The Fenn spec contains no list labelled "Pass 1". Body control lists as written:
- Torso: torso length, ribcage width and depth, shoulder width, waist, pelvis width — L50.
- Arms/hands: arm length, upper-arm and forearm proportion, hand length and breadth, finger proportion — L51; v1.1 refinement: total length, upper-arm and forearm proportion, thickness, regional muscle; hand: overall hand scale, palm length and breadth, finger length and thickness, no per-finger — L121–122.
- Legs/feet: leg length, thigh and lower-leg proportion, thigh and calf development, foot length and breadth — L52; v1.1: total length, thigh and lower-leg proportion, thigh and calf thickness, regional muscle; foot length and breadth — L123–124.
- Frame: Narrow / Balanced / Broad — L44.
- Regional environmental skin controls: face, hands, forearms, feet, general exposed skin "where feasible" — L260.
- Status labels: none on body controls. The only explicit status label ("APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION", L158) applies to facial and ear control organization only. Height labelled "(provisional)" L20; presets "(provisional)" L318, L331; cultural foundation "(provisional)" L274; combined-proportion "(proposed universal)" L132; biology-vs-presentation randomization "(proposed universal)" L378; reproducibility "proposed" L515.

## Extraction notes
- **Waist transition (supersession by clarification):** L50 "longer waist transition" and L110 "relatively longer waist and lumbar transition" are read through ECR L41–49: Fenn transition is gradual/extended only within the compact Fenn system, never longer absolutely or proportionally than Aelari (ECR L45).
- **Pigmentation:** L244 ("broad warm and neutral undertones and some cooler ones") is corrected by ECR L223 (cool listed fully; reddish/copper-influenced added; "intermediate beige and tan families"). L248 Vael direction is superseded by the Vael spec and ECR L159.
- **Comparative-review promises:** L252, L389, L548 say frequencies wait for the review. The review is complete but left frequencies E (ECR L213, L298), so they stay open.
- **Ear projection** already updated in-spec (L183) per ECR L328.
- **Neck** is silent in the Fenn spec. ECR "Intermediate" (L31) is the only Fenn neck statement.
- **Tension:** L50 "Slightly smaller torso share of height" plus L110 "somewhat vertically compact" ribcage vs FN-08 "Long torso, against the population average" (L91). Not a conflict, since this is a deliberate counter-tendency test.
- **"Thigh and calf development" (L52) vs "thickness" (L123):** possibly a composition control vs a skeletal/soft-tissue mix. The spec does not split skeletal and muscular limb thickness.
- Sex-related anatomy, body hair, natural body asymmetry, Simple/Advanced mode, locks: entirely SILENT in Fenn (present in Aelari/Vael).
