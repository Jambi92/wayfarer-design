> UCCA Phase 1 evidence appendix to `reviews/claude-ucca-01-requirements-matrix.md`. Line references are to the canonical race spec (or the named source) as of commit 89ca8f7. Extraction only: no canon is changed and nothing here is new biology. Tags: [ANAT] anatomical requirement · [DIR] direct control · [DER] derived/coupled · [SOFT] tendency · [VAL] validator · [LAT] latent/preset · [PRES] presentation · [DIAG] diagnostic · [OPEN] open/not authorized.

# UCCA extraction: Aelari (specs/aelari/AELARI_V1.md, v1.5 first-pass complete)

Source: `specs/aelari/AELARI_V1.md` (614 lines), cited as `Lnnn`. Comparative authority: `reviews/elf-comparative-review.md` (accepted, authority level 3), cited as `ECR Lnnn`. Per ECR L3/L302, the race spec stays authoritative wherever the ECR does not explicitly clarify or supersede it. Face anatomy is out of scope (UFCA_V1).

## 0. What the Elf Comparative Review settles for the Aelari BODY

| Topic | ECR settlement (Aelari) | Class | Effect on Aelari spec |
| --- | --- | --- | --- |
| Limb share / segments | "Long limbs with even elongation, upper arm to forearm and femur to lower leg" (ECR L33); final: "Long limbs, elongation evenly distributed across segments" (ECR L279); hands "Long hands and fingers integrated with vertical anatomy" (ECR L34); feet "Elongated, supporting vertical anatomy" (ECR L35); hands/feet "Elongation integrated with vertical anatomy" (ECR L280). Fenn = stronger forearm/lower-leg proportional contribution (ECR L279) | [SOFT] | **Resolves** the "Not final until comparative validation" / "Exact differences provisional" Fenn-contrast hedges at L56–58, L155 |
| Neck | "Strongest average elongation" (ECR L31). Final clarification §2: "greater average neck length, and greater neck contribution to total vertical body proportion, than Fenn and Vael populations, with substantial overlap. Not every Aelari has a longer neck than every Fenn or Vael. Absolute neck length … and proportional neck contribution … aren't interchangeable measurements" (ECR L320). Movement: "longer average neck" (ECR L256) | [SOFT] / [DIAG] | Extends L50 ("longer on average than humans and Fenn") to "than Fenn **and Vael**", and requires two distinct measures |
| Thoracic depth / torso | "Longer vertical ribcage and torso, longer waist, shallow thoracic depth, whole-body continuity" (ECR L29); final: "Greatest average vertical torso and waist continuity of the three, relatively shallow thoracic depth" (ECR L278). Waist clarification: "a longer average ribcage-to-pelvis (waist-transition) region than Fenn and Vael" (ECR L46) | [SOFT] | Confirms L48, L123–124; makes the Aelari waist comparison explicit vs both elves |
| Frame / gracility | "Strong average gracility with vertical elongation, and somewhat more skeletal structural presence than Fenn" (ECR L276); "somewhat greater average skeletal structural presence than Fenn when comparing otherwise equivalent individuals" (ECR L313); ordering Fenn → Aelari → Vael, with overlap, never three bone-thickness presets (ECR L316). "Broad frames are valid for all elves" (ECR L55) | [SOFT] / [VAL] | **New**: places Aelari between Fenn and Vael; the spec itself never ranks Aelari vs Fenn gracility |
| Composition | No elven population defined by low fat/low muscle; full low–high muscle/fat, regional development, all frames, age-related composition (ECR L55) | [ANAT] | Confirms L62, L159 |
| Pigmentation | Aelari skin: very light/fair, light, warm/neutral beige, golden, olive, bronze, medium brown, deeper brown; undertones cool, neutral, warm, golden, olive, reddish where appropriate; "Aelari ancestry equals pale skin" rejected; frequencies E (ECR L158). Fenn–Aelari substantial overlap locked (ECR L225, L284); validity ≠ frequency (ECR L229); pigmentation must not carry identity (ECR L161); lighting invariance (ECR L165) | [SOFT] / [VAL] / [OPEN] | Confirms L292–293 verbatim; frequencies remain E despite L299 |
| Hair | Biology/presentation split (ECR L171); texture: no "Aelari-straight" assumption, frequencies E (ECR L172); colours population-specific distributions, unresolved (ECR L173); natural silver/white ≠ aging (ECR L174, L290); facial hair not prohibited (ECR L175); Aelari "Frequencies unresolved" (ECR L285) | [ANAT] / [OPEN] | Confirms L326–340; whether natural silver/white is valid Aelari biology (L332 "if it's later validated") is **not** settled by ECR |
| Age | Shared visible aging including body composition and posture where individually appropriate; lifespan, maturation, adult aging rate, fertility span E (ECR L245, L298) | [ANAT] / [OPEN] | Confirms L239 (OPEN DECISION stays) |
| Height | 168–221 cm, reference about 190 (ECR L28, L277). **KNOWN CURRENT-IMPLEMENTATION / TARGET-DESIGN GAP**: prototype "1.02 race scale with about ±7.5% generic height variation" doesn't reproduce the range; approved range authoritative; maximum not reduced (ECR L336). 221 cm (7'3") Aelari permanent world validation; minimum and reference also tested (ECR L338); world validated against approved anatomy, not prototype-reachable anatomy (ECR L342) | [ANAT] / [VAL] | Adds precise prototype numbers to L549/L594/L610 |

Also settled, body-relevant: shoulders/clavicles "Relatively long clavicles, strong vertical neck and shoulder continuity" (ECR L30); pelvis "Supports vertical elongation and long femurs (E in detail)" (ECR L32, L281); movement "Not automatically: Regal, elegant, aloof, slow, delicate (presentation or personality, not anatomy)" (ECR L256); Aelari Wisdom value kept as prototype only, not biological (ECR L237); no major Aelari environmental adaptation locked (ECR L188); "Aelari maximum height needs particular attention" for world compatibility (ECR L269).

## A. Stature and proportions

**A1 Height**
- [ANAT] Minimum 168 cm (about 5'6"), Reference 190 cm (about 6'3"), Maximum 221 cm (about 7'3") — v1.0 §3 L25–27; ECR L28.
- [SOFT] "Height supports Aelari identity but doesn't create it. A minimum-height Aelari is still anatomically Aelari." — L29.
- Labelled "(provisional)" — L23. Distribution shape: SILENT.
- [OPEN]/[VAL] Prototype gap — L549 ("uniform scaling"), L594 ("The approved maximum height is never cut to suit the prototype's human scale"), ECR L336 (1.02 scale, ±7.5%).

**A2 Torso length/depth/width**
- [SOFT] "Longer than Fenn relative to height, longer waist transition, moderate chest breadth, relatively shallow depth, elven ribcage relationships" — v1.0 §6–8 L48. [VAL] "Believable thoracic volume, never implausibly shallow" — L48.
- [SOFT] Ribcage "Vertically longer than Fenn, moderate width, relatively shallow depth" — v1.1 §2–5 L123. [VAL] "A functional 3D structure with enough thoracic volume, never an extremely flat or narrow chest" — L123.
- [SOFT] Torso/spine "Longer overall torso and waist transition than Fenn" — L124.
- [DIR] "torso length, ribcage length, width and depth, waist and lumbar length, shoulder width, pelvic width" — L124.
- [DER] "Ribcage width and depth set torso volume." "Torso length moves the spine, ribcage and waist transition." — v1.1 §8 L141–142.

**A3 Limbs & segment proportions**
- [SOFT] Arms "Longer than humans, with elongation spread evenly across upper arm and forearm, and broad variation" — L56; "Fairly even elongation across upper arm and forearm" — L152.
- [SOFT] Legs "Distinctly long-legged while keeping the longer torso, with even elongation through thigh and lower leg (not lower leg alone)" — L58; "Elongation spread evenly, not one extremely long segment" — L154.
- [DIR] Arms: total length, upper-arm and forearm proportion, thickness, regional muscle — L152. Legs: total length, thigh and lower-leg proportion, thigh and calf thickness, regional muscle — L154.
- [VAL] "no independent segment stretching"; "Hip, knee, ankle and foot stay coherent" — L152, L154.
- [DER] "Limb thickness keeps the joint transitions." — L144.
- [SOFT] Overall: "whole-body vertical elongation, distributed coherently through the cranium, neck, torso, arms and legs" — v1.0 §4 L33; core rule table L112–115.

**A4 Shoulder/pelvic relationships**
- [SOFT] "Relatively long clavicles, broad shoulder variation, all three frames, lighter shoulder joints than humans or Skarn" — L49; v1.1 L125 adds "coherent shoulder-to-neck transition".
- [VAL] "Broad Aelari stay Aelari. Gracile never means narrow shoulders" — L49; "Broad Aelari gain real skeletal breadth, not just muscle or fat" — L125.
- [ANAT] Pelvis: "A distinct elven pelvis, not a stock human pelvis with longer legs attached. Stable with long femurs, coherent with the spine, Narrow to Broad variation, plausible muscle attachment, natural locomotion" — L126.
- [OPEN] "Exact shape awaits prototyping." — L126; ECR L32, L281.
- [DER] "Shoulder width moves the clavicles, upper back and shoulder joints." "Pelvic width sets hip articulation and upper-leg alignment." — L140, L143.

**A5 Neck**
- [SOFT] "Somewhat longer on average than humans and Fenn. The shoulder-to-neck-to-skull line adds subtly to verticality" — L50. [VAL] "Believable range, never exaggerated" — L50.
- [SOFT] Extended by ECR L320 (longer than Fenn and Vael on average; overlap; absolute vs proportional are distinct) — see §0.
- [LAT] Randomization link "neck, shoulders and skull" — L445.
- Neck-length control: SILENT (no explicit neck control listed in body control lists).

**A6 Hands/feet**
- [SOFT] Hands "Long hands and fingers, relatively narrow breadth, gracile wrists" — L57; "Elven hands, not stretched human ones: longer hands, palms and fingers, relatively narrow breadth, gracile wrists" — L153.
- [DIR] "Overall scale, palm length and breadth, finger-length proportion, finger thickness. No per-finger controls yet." — L153.
- [VAL] "Knuckles, finger bases, palm and wrist stay believable." — L153.
- [SOFT] Feet "Humanoid, somewhat longer, moderate to narrow breadth, gracile ankle" — L155. [DIR] "Foot length and breadth" — L155.
- [VAL] "No prehensile or animal-like feet or exaggerated toes." — L155.

**A7 Reach-related anatomy**
- [OPEN] "Collision, melee and interaction reach, step height, climbing reach and other size effects stay OPEN … racial size is a dedicated balance decision." — v1.5 §17–19 L582; ECR L269.
- [VAL] "A 168 cm and a 221 cm Aelari can't share unadjusted contact positions." — L562.

**A8 Posture / Anatomical Resting Alignment**
- [ANAT] "Anatomical resting alignment | Skeletal and body relationships" vs "Cultural and personal body language | Culture, personality, training, occupation, emotion and circumstance" — v1.0 §13 L66–69 (labelled universal).
- [SOFT] "Aelari anatomy may give an upright neutral silhouette. Pride, nobility, refinement, arrogance and aristocratic posture are never biological." — L71.
- [SOFT] Movement: "Anatomy may shape stride length, step relationships, center of mass, turning, acceleration and deceleration, arm swing and foot placement." — v1.5 §6 L558.

**A9 Population-specific axial structures**
- SILENT.

**A10 Head-to-stature**
- SILENT on ratio. [SOFT] Vertical elongation "distributed coherently through the cranium, neck, torso…" — L33. [LAT] Randomization link "neck, shoulders and skull" — L445. Landmarks include neck and head at min/ref/max height and all frames — L554.

## B. Skeletal Frame
- [SOFT] Provisional shared themes: "a more gracile skeleton than humans … less apparent joint mass" — L13–15.
- [ANAT] Frame interaction: "Narrow, Balanced and Broad change the real skeleton: clavicle, ribcage and pelvic breadth, joint relationships and overall skeletal presence. Frame stays separate from muscle, fat, sex-related anatomy, height and presentation." — v1.1 §7 L134.
- [ANAT] "Narrow/Balanced/Broad are Skeletal Frame presets" — L62.
- [SOFT] Joint scale: "Shoulders, elbows, wrists, hips, knees and ankles are gracile compared with humans but structurally sufficient. Gracile never means fragile, and hard minimum boundaries prevent implausibly tiny joints." — v1.1 §6 L130 ([VAL] for the bound).
- [SOFT] Gracility rank vs Fenn/Vael: SILENT in spec; ECR L313.

## C. Physical Composition
- [ANAT] "The full system applies: overall muscle, fat distribution, regional development and conditioning." Supported combinations: Narrow and lean, Narrow and muscular, Balanced, Broad, Broad and highly muscular, high body fat, elder composition. "Aelari identity never depends on thinness." — v1.0 §12 L62.
- [VAL] Composition stress test set — v1.1 §13 L159; v1.4 §15–16 L472. "Soft tissue never erases the Aelari skeleton, and muscle never turns Aelari into Skarn." — L159.
- Muscular Development Capacity vs Current Muscularity: SILENT. Fat distribution pattern: SILENT (only "fat distribution" as a system component, L62). Population-specific tissue systems: SILENT.

## D. Biological surface
- [SOFT] Skin valid range: "Very light or fair, light, warm or neutral beige, golden, olive, bronze, medium brown, deeper brown"; undertones "Cool, neutral, warm, golden, olive, and reddish where appropriate" — v1.3 §2 L292–293. "These are not frequencies." — L295.
- [VAL] "High Elf = pale skin" rejected; "white-tower architecture, magic, prestige, clothing and institutions never set biological pigmentation" — L75, L286.
- [ANAT] Four layers: natural, environmental, applied, acquired; "Natural pigmentation stays separate from tanning." — v1.3 §4–5 L303.
- [DIR]/[VAL] "Face, hands, forearms, exposed feet and general exposed skin each show their own history, with no automatic occupation or culture." — L303.
- [ANAT] Validity vs frequency: Common/Uncommon/Rare; "Rarity never blocks a player's manual choice." — §8 L320.
- Material/finish: SILENT (ECR L151: physiology/material differences E).

## E. Hair / homologues
- [ANAT] Biological (texture, density, natural color, hairline) vs presentation (length, cut, styling, parting, braiding, tying, shaving, accessories, grooming) — v1.3 §9 L324–326. "Long hair is never biologically required." — L328.
- [SOFT] Texture "straight, wavy, curly, and coiled where valid. Elves aren't universally straight-haired." Colours "black, dark brown, brown, lighter brown, auburn, red, blond and light, plus naturally silver-like or white hair if it's later validated as Aelari biology. Frequencies are OPEN." — §10–11 L332.
- [ANAT] Natural light hair vs aging: "If natural silver or white hair becomes a valid inherited trait, it stays distinct from age-related graying … recorded for the future material and data architecture." — §12 L336.
- [ANAT] Facial hair (pointer): "independent of hairstyle and frame, covering presence, density, style, length, color and graying … neither required to be clean-shaven nor required to have facial hair. Frequency is provisional." — §13 L340. Eyebrow-hair → UFCA slot 11 — L204.
- [VAL] "Hairstyle, length and grooming are never locked to sex-related anatomy, frame, physique or occupation." (universal) — §14 L344.
- Body hair: SILENT.

## F. Age
- [ANAT] "Aelari visibly age: facial volume, skin elasticity, eye area, cheeks, jawline, neck, wrinkles, hair density and color, and ear tissue where appropriate. High Elves are never assumed to stay permanently youthful." — v1.2 §13 L239.
- [OPEN] "Lifespan and aging rate are an OPEN DECISION." — L239; ECR L245.
- Body-level aging (composition, posture): SILENT in Aelari spec (only "elder composition", L62); ECR L245 adds body composition and posture.
- [VAL] AE-08 Elder (L92), AE-30 (L268), AE-43 Elder culturally neutral (L503); failure "Elder Aelari stop reading as Aelari" (L520); Elder Waykeeper preset (L421).

## G. Sex-related anatomy
- [ANAT] Pelvis: "No mandatory hip width by race or sex-related anatomy" — L126.
- [ANAT] "Frame stays separate from muscle, fat, sex-related anatomy, height and presentation." — L134.
- [VAL] Hair never locked to sex-related anatomy — L344.
- Canonical sex tendencies: SILENT. R-SEX pointers: none. Reproductive biology: SILENT (ECR L245 fertility span E).

## H. Asymmetry & acquired history (non-facial)
- Natural body asymmetry: SILENT (ears L235; face L220).
- [ANAT] Acquired layer = scars — L303. Ear damage "stay acquired appearance" — L235.
- Individuality: "scarred, asymmetrical, elderly or high body fat" Aelari valid — §14 L243.
- Missing/damaged structures: SILENT.

## I. Presentation
- [PRES] Personal appearance (meticulous … tattooed … highly decorated) never sets authenticity; cultural hair is options only — L348.
- [PRES] Biology vs civilization: "Pride, wisdom, education, status and magical scholarship are never biological." — §17 L352. Cultural pillars (provisional) — L356–362. White towers not biology — L368.
- [PRES] Clothing, jewelry, markings "never universally required" — §21–23 L376.
- [PRES] Presentation presets (v1.3): White-Tower Formal, Artisan Practical, Arcane Institutional, Military Formal, Traveler, Rural/Provincial, Foreign/Urban, Ceremonial — "never overwrite ancestry, skeleton, height, frame, muscle, fat, face, ears or natural pigmentation" — §24 L380.
- [VAL] Cross-cultural matrix — §25 L384–392; v1.4 §21–22 L488.
- [ANAT]/[PRES] Resting alignment vs body language — L66–71; movement grace never biological — L558; ECR L249.

## J. Creator system
- [LAT] Preset architecture: "complete, editable starting people using the same system as custom characters and NPCs" — v1.4 §1 L408.
- [LAT] Character presets (provisional): White-Tower Archivist, Provincial Artisan, Tower Guard, Heavyset Merchant, Broad Craftworker, Traveling Aelari, Foreign-Raised Aelari, Elder Waykeeper — L412–421; never assign class/stats/etc. — L423. Library must vary height, frame, muscle, fat, age, face, ears, pigmentation, hair, eyes, grooming, presentation — §3 L427.
- [PRES] Presentation presets (v1.4): White-Tower Formal, Institutional Practical, Artisan, Military, Traveler, Provincial, Ceremonial, Foreign/Urban — §4 L431 (list differs from v1.3 L380; see notes).
- [VAL] "Every preset is a reproducible configuration of the player's system, with no preset-only anatomy. Simple and Advanced modes share the same appearance data." — §5 L435.
- [LAT] Population-aware distributions for height, frame, proportions, craniofacial, ears, pigmentation, hair, eyes; strengths Subtle / Diverse / Extreme ("Extreme never means invalid") — §6–8 L439.
- [LAT]/[DER] Relationship-aware randomization links: neck–shoulders–skull; shoulder width–clavicles–upper back; ribcage–torso; spine–pelvis; pelvis–upper-leg alignment; arm length–upper arm–forearm–hand; leg length–femur–lower leg–foot; limb thickness–joint scale; cranial–facial; ear base–skull attachment — §9 L445–454.
- [DIR] Selective randomization groups (entire character, body, face, ears, hair, natural appearance, skin details, markings, presentation) and locks on parameters or groups — §10–11 L460.
- [SOFT] Soft probabilistic correlations, never rigid packages — §12 L464.
- [LAT] Reproducible from stored data or seeds (NPC persistence, save/load, testing, bug reproduction, presets, multiplayer) — L464.
- [VAL] Appearance schema: versioning and migration, reproducible generation, preset reproducibility, save/load continuity, Simple/Advanced continuity, selective randomization locks; implementation unresolved — v1.5 §22 L590.
- [ANAT] Unified record — §20–21 L586.
- [VAL] First-person: "If visible first-person arms exist, they keep Aelari arm, forearm and hand proportions, skin and equipment, and are never generic human arms. First-person support stays in the Decision Register." — §13–14 L574.
- [VAL] Cameras: no universal camera height; maximum-height Aelari special attention — L574.
- [VAL] Equipment tested at min/ref/max height, all frames, low/high muscle and fat, ages, extreme proportions — §9 L566; headgear/ears, gloves, boots — §10–12 L570; "Canonical equipment never scales" — L582.
- [VAL] World compatibility, 221 cm mandatory stress case — §15–16 L578.

## K. Locked validation tests (body / whole-character)
- AE-01 Reference 190 cm Balanced; AE-02 168 cm; AE-03 221 cm; AE-04 Narrow lean; AE-05 Broad; AE-06 Broad high muscle; AE-07 High body fat; AE-08 Elder; AE-09 Short Aelari human-overlap; AE-10 Equal-height Fenn; AE-11 Long-torso stress; AE-12 Valid extreme proportional — L85–96.
- AE-13 Narrow low muscle low fat; AE-14 Narrow high muscle; AE-15 Balanced high fat; AE-16 Broad low muscle; AE-17 Broad high muscle; AE-18 Broad high fat; AE-19 Max hand proportions; AE-20 Max leg+foot; AE-21 Equal-height Sagekin; AE-22 Equal-height Fenn; AE-23 Broad muscular Skarn boundary; AE-24 Max-height combined-proportion stress — L179–190.
- (Face set AE-25–AE-36, L263–274; whole-character relevant: AE-29 high-body-fat facial, AE-30 Elder.)
- AE-37 Short and Broad; AE-38 Short high muscle; AE-39 Min ears neutral; AE-40 Max ears neutral; AE-41 Dark hair dark eyes neutral; AE-42 High body fat short hair; AE-43 Elder culturally neutral; AE-44 Foreign-raised; AE-45 Sagekin boundary; AE-46 Fenn boundary; AE-47 Skarn boundary; AE-48 Generic-elf convergence counterexample; AE-49 Diverse randomized; AE-50 Extreme valid randomized — L496–509.
- AE-03 = permanent technical stress character — L594.
- Generic-elf convergence test — §14 L468. Hidden-ear population test — §17 L476. Cultural neutralization — L488. Composition stress — L159, L472.
- Equal-height Fenn/Aelari test (v1.0) — §15 L79. Landmarks/locomotion — L554; IK/grips — L562.

## L. Positive body identity statement
- "Aelari are built around whole-body vertical elongation, distributed coherently through the cranium, neck, torso, arms and legs. They're never a uniformly scaled human or Fenn with stretched legs." — v1.0 §4 L33.
- "Aelari | Distributed continuously through the neck, torso, arms and legs" — L115.
- ECR: "Aelari are vertically distributed" (ECR L59); "Vertically distributed specialization" (ECR L275).

## M. Cross-population boundary tests (body)
- Equal-height Fenn/Aelari, "permanent, about 190 cm, ears hidden, matched frame, muscle, fat, age, pose and clothing" — L169 (stature 190 cm); v1.0 version "about equal height" — L79; v1.4 L483.
- Human boundary "Similarly tall Marchfolk and Sagekin" — L170; Sagekin "especially important" — L482.
- Skarn boundary "using tall, Broad, muscular Aelari" — L171, L484.
- AE-09 Short Aelari human-overlap; AE-21/45 Sagekin; AE-10/22/46 Fenn; AE-23/47 Skarn — K above.
- Cross-race technical comparison table (Marchfolk, Sagekin, Skarn, Fenn, Aelari) — L598–604.

## N. Forbidden controls / anti-patterns (body)
- "never a uniformly scaled human or Fenn with stretched legs" — L33; "never taller Fenn" — L7.
- "no independent segment stretching" — L152. "Sliders are never rolled independently." — L443.
- No per-finger controls yet — L153.
- No mandatory hip width by race or sex — L126.
- Longer legs "never mean simply faster playback or uniform stride scaling" — L554.
- Failure conditions: pointed ears needed; simply taller Fenn; stretched humans; Broad/muscular lose identity; high-fat lose identity; elders stop reading; one "pretty High Elf" template; pale skin mandatory; light hair mandatory; cultural presentation needed; valid sliders combine into invalid anatomy; prototype limits redefine anatomy — L515–527.
- Rigid phenotype packages — L464.

## O. OPEN / DEFERRED (body / whole-character)
- Technical foundation / MetaHuman — v1.0 §17 L100; v1.5 §1 L543; ECR L265.
- Combined-proportion implementation — L163.
- Pelvis exact shape — L126.
- Lifespan/aging rate — L239.
- Hair/pigmentation/iris frequencies — L299, L332, L439; natural silver/white validity — L332.
- Collision, reach, step height, mounts — L582. First-person support — L574.
- Reproducibility/schema implementation — L464, L590.
- Prototype protection list (uniform race scaling, human animation placeholder, Manny and Quinn, serialization, collision, camera, reach, weapons, stats, class restrictions, race models) — L610.
- Height prototype gap — ECR L336.
- No RM-* references.

## P. Pass 1 provisional creator-control lists (BODY)
No list labelled "Pass 1". Body control lists as written:
- Torso/spine: torso length, ribcage length, width and depth, waist and lumbar length, shoulder width, pelvic width — L124.
- Arms: total length, upper-arm and forearm proportion, thickness, regional muscle — L152.
- Hands: overall scale, palm length and breadth, finger-length proportion, finger thickness (no per-finger) — L153.
- Legs: total length, thigh and lower-leg proportion, thigh and calf thickness, regional muscle — L154.
- Feet: foot length and breadth — L155.
- Frame: Narrow / Balanced / Broad = Skeletal Frame presets — L62, L134.
- Randomization groups and locks — L460. Strengths Subtle / Diverse / Extreme — L439.
- Status labels: body controls carry no explicit status label. "APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION" (L200) covers facial/ear control organization only. Other labels: height "(provisional)" L23; presets "(provisional)" L410, L431; "(proposed universal)" L309; "OPEN DECISION" L100, L239, L541.

## Extraction notes
- **Shared-foundation hedge superseded:** L21 ("Shared elven anatomy isn't finalized until Vael have a biological design pass") is superseded by ECR Part 1 (L19–37, L57–59).
- **Fenn-contrast hedges resolved:** L56, L58 ("Not final until comparative validation", "Exact differences provisional") and L155 are settled at population-tendency level by ECR L33–35, L279–280. Exact numbers are still absent.
- **Neck:** L50 compares only against humans and Fenn. ECR L320 adds Vael and the absolute vs proportional distinction. There is no neck control in the body control lists. The neck appears only as a randomization link (L445) and a landmark (L554).
- **Gracility vs Fenn:** the spec says Fenn and Aelari share themes (L13) without ranking them. ECR L313 ranks Aelari as having somewhat more structural presence than Fenn.
- **Presentation preset lists differ** between v1.3 §24 (L380: "Artisan Practical", "Arcane Institutional", "Military Formal", "Rural/Provincial") and v1.4 §4 (L431: "Institutional Practical", "Artisan", "Military", "Provincial"). The spec has no supersession note. The later v1.4 list presumably governs, but this is unstated.
- **Height implementation:** the spec says "uniform scaling" (L549). ECR L336 gives 1.02 race scale, ±7.5%.
- ECR L46 and L320 sharpen "longer" into comparisons named against both Fenn and Vael (terminology rule, ECR L51, L145).
- Silent: body hair, natural body asymmetry, Muscular Development Capacity/Current Muscularity split, body-level aging beyond "elder composition" (ECR L245 fills this).
