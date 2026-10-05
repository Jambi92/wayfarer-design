> UCCA Phase 1 evidence appendix to `reviews/claude-ucca-01-requirements-matrix.md`. Line references are to the canonical race spec (or the named source) as of commit 89ca8f7. Extraction only: no canon is changed and nothing here is new biology. Tags: [ANAT] anatomical requirement · [DIR] direct control · [DER] derived/coupled · [SOFT] tendency · [VAL] validator · [LAT] latent/preset · [PRES] presentation · [DIAG] diagnostic · [OPEN] open/not authorized.

# UCCA extraction: Vael (specs/vael/VAEL_V1.md, v1.5 first pass complete)

Source: `specs/vael/VAEL_V1.md` (620 lines), cited as `Lnnn`. Comparative authority: `reviews/elf-comparative-review.md` (accepted, authority level 3), cited as `ECR Lnnn`. Per ECR L3/L302, the race spec stays authoritative wherever the ECR does not explicitly clarify or supersede it. Face anatomy is out of scope (UFCA_V1). Eye/low-light items appear only as whole-character pointers.

## 0. What the Elf Comparative Review settles for the Vael BODY

| Topic | ECR settlement (Vael) | Class | Effect on Vael spec |
| --- | --- | --- | --- |
| Limb share / segments | "Moderate elongation, balanced segments, more substantial wrist, hand, ankle and foot transitions" (ECR L33); final: "Moderate elongation, stronger wrist-hand and ankle-foot transitions" (ECR L279); hands "Moderate finger elongation, broader palm, stronger wrist and hand base" (ECR L34); feet "Moderate elongation, broader, stronger ankle transition" (ECR L35); hands and feet "more breadth and base presence than Fenn and Aelari" (ECR L280) | [SOFT] | Confirms L44–47, L138–141. ECR does not restate the spec's "somewhat smaller leg share of height than Fenn or Aelari" (L46, L140), which stays as Vael-spec canon |
| Neck | "Somewhat shorter neck-to-torso than Aelari" (ECR L31); Aelari have greater average neck length and proportional contribution than Fenn **and Vael**, with overlap; absolute vs proportional distinct (ECR L320) | [SOFT] / [DIAG] | Confirms L123 ("relative, not absolute"). No Vael-vs-Fenn neck ranking is given |
| Thoracic depth / torso | "Greater front-to-back thoracic depth (skeletal, never muscle or fat), moderate ribcage width, compact torso and limb continuity, strong torso-pelvis integration" (ECR L29); final: "Greater thoracic depth than Fenn and Aelari, less vertical waist elongation than Aelari, stronger compact torso-pelvis continuity" (ECR L278). Waist clarification: "Less vertical waist elongation than Aelari … The deeper ribcage must not be mistaken for a longer waist" (ECR L47). Terminology example: "greater average thoracic depth than Fenn and Aelari" rather than "deeper torso" (ECR L145) | [SOFT] / [VAL] | Confirms L35, L114, L120–121; **the terminology rule supersedes the bare wording** "deeper torso"/"deep-bodied" (L3, L27, L165, L506) for comparative use |
| Frame / gracility | "Gracile, with somewhat more joint and skeletal presence" (ECR L27); final: "Still gracile relative to robust humans, with the greatest average joint, base and skeletal structural presence of the three" (ECR L276, L314); ordering Fenn → Aelari → Vael with overlap ("an individual Vael more gracile than an individual Aelari"), never fixed bone-thickness presets (ECR L316). "Broad frames are valid for all elves … never a human skeleton, Skarn or Durrim anatomy" (ECR L55) | [SOFT] / [VAL] | Confirms L36–37, L132; ordering now explicit |
| Composition | No elven population defined by low fat/low muscle; full ranges, all frames, age-related composition (ECR L55) | [ANAT] | Confirms L51, L145 |
| Pigmentation | Vael: "Charcoal, slate, cool, neutral and warmer gray, blue-gray, muted or desaturated violet, ash-brown, desaturated brown, and grounded variants found in prototyping. Living tissue, not painted stone"; E: light-to-dark distribution, undertone distribution, colour-family frequency (ECR L159). "Vael overlap is also possible … No artificial color boundaries are forced" (ECR L227); final: "More divergent provisional distribution, overlap still possible" (ECR L284). Pigmentation isn't identity; must survive neutralization (ECR L161). Lighting invariance promoted to universal principle (ECR L165) | [SOFT] / [VAL] / [OPEN] | Confirms L363–367; **promotes** L375 "Proposed universal" lighting invariance to locked universal (A) |
| Hair | Biology/presentation split (ECR L171); texture: no "Vael-straight-white" assumption (ECR L172); colour distributions unresolved (ECR L173); natural silver/white ≠ aging (ECR L174, L290); facial hair not prohibited (ECR L175); "Frequencies unresolved" (ECR L285); rigid "gray skin, white hair and violet eyes" package rejected (ECR L195) | [ANAT] / [OPEN] | Confirms L389–399, L490 |
| Age | Shared visible aging incl. body composition and posture where individually appropriate; lifecycle E (ECR L245, L298) | [ANAT] / [OPEN] | Confirms L294; adds body-level aging |

Also settled, body-relevant: shoulders/clavicles "Moderate clavicles, stronger neck and shoulder integration, more shoulder-joint presence" (ECR L30); pelvis "Supports deeper torso continuity and Vael legs (E in detail)" (ECR L32, L281); movement "Greater average thoracic depth than Fenn and Aelari, more compact torso-to-pelvis continuity than Aelari, somewhat greater joint and base presence than Fenn and Aelari, moderate limb elongation"; "Not automatically: Predatory, sinister, crouched, aggressive, cave-adapted posture" (ECR L257); height 157–203 cm ref about 178 (ECR L28, L277); Vael low-light adaptation D+E, mechanism unresolved, gameplay OPEN (ECR L100, L189); adaptation isn't culture: "A surface-raised Vael may keep inherited Vael ocular biology" (ECR L191).

## A. Stature and proportions

**A1 Height**
- [ANAT] Minimum 157 cm (about 5'2"), Reference 178 cm (about 5'10"), Maximum 203 cm (about 6'8") — v1.0 §3 L15–17; ECR L28.
- [SOFT] "Height never defines Vael, and minimum, reference and maximum-height Vael share one population identity." — L19.
- Labelled "(provisional)" — L13. Distribution shape: SILENT.
- [OPEN] Prototype: "uniform scaling (0.95)" — v1.5 L566 (CURRENT IMPLEMENTATION, not final).
- [VAL] "'Compact' never means short, dwarven, stocky or automatically muscular." — L29.

**A2 Torso length/depth/width**
- [SOFT] "Greater torso share than Fenn, deeper ribcage than Fenn or Aelari, moderate width, strong torso-to-pelvis continuity, less elongated than Aelari" — v1.0 §5–8 L35. [VAL] "Believable thoracic volume, broad variation" — L35.
- [ANAT] "Torso depth is skeletal": "comes from ribcage depth and curvature, the spine-to-ribcage relationship, shoulder placement and the torso-to-pelvis transition. It's never faked with body fat, muscle, an oversized chest or uniform torso scaling. A Narrow, lean Vael keeps it." — v1.1 §2 L114.
- [SOFT] Ribcage "Deeper front to back than Fenn or Aelari, moderate width, slightly shorter vertically than Aelari, strong 3D volume, smooth into shoulders and waist" — L120. [VAL] "No barrel-chest caricature, flat human scaling or Skarn-like mass" — L120.
- [SOFT] Spine/waist "Moderate torso length, less extended waist than Aelari, strong torso-to-pelvis continuity, natural lumbar curve" — L121.
- [DIR] "torso length, ribcage length, width and depth, waist and lumbar length" — "All relationship-aware" — L121.
- [DER] Coupled: ribcage width and depth, ribcage and spine, torso length and waist, waist and pelvis — §8–9 L128.

**A3 Limbs & segment proportions**
- [SOFT] Arms "Long relative to humans, less extreme elongation than Fenn or Aelari, balanced upper arm and forearm, a somewhat sturdier wrist transition" — L44; "Somewhat less relative elongation than Fenn or Aelari, still elven" — L138.
- [VAL] "Never made by shortening Fenn arms with a slider" — L44.
- [SOFT] Legs "Long relative to humans, somewhat smaller leg share of height than Fenn or Aelari, balanced femur and lower leg, more knee and ankle presence" — L46; L140.
- [VAL] "Compactness never comes from just shortening legs" — L140.
- [DIR] Arms: total length, upper-arm and forearm proportion, thickness, regional muscle — L138. Legs: total length, femur and lower-leg proportion, thigh and calf thickness, regional muscle — L140.
- [DER] "The chain from shoulder to hand stays coherent" — L138; "Hip, knee, ankle and foot stay coherent" — L46.
- [SOFT] "lower center of mass than Aelari" — silhouette matrix L165.

**A4 Shoulder/pelvic relationships**
- [SOFT] "Moderate clavicles, strong shoulder-to-neck integration, broad width variation, slightly more shoulder-joint presence than Fenn or Aelari" — L36. [VAL] "Never automatically broad. Narrow, Balanced and Broad all supported" — L36.
- [SOFT] "Moderate clavicles and breadth, strong neck and shoulder integration, more shoulder-joint presence than Fenn or Aelari, broad variation" — L122. [VAL] "Frame changes the skeleton, and a Narrow Vael is never a scaled-down Broad Vael" — L122.
- [ANAT] Pelvis "Their own elven pelvis (not human, Fenn or Aelari): stable leg articulation, torso-to-pelvis continuity, Narrow to Broad support, plausible muscle attachment, natural locomotion" — L38; L124.
- [OPEN] "Exact shape awaits prototyping" — L38; "No human pelvis plus a slider. Awaits prototype validation" — L124; ECR L281.

**A5 Neck**
- [SOFT] "Somewhat shorter relative to the torso than Aelari (relative, not absolute), with broad variation" — L123.
- [VAL] "Keeps head support, shoulder integration, cervical anatomy and full movement. No short, thick-neck stereotype" — L123.
- [DER] Coupled: neck and shoulders — L128. [LAT] Randomization: neck to shoulders — L486.
- Neck-length control: SILENT.

**A6 Hands/feet**
- [SOFT] Hands "Elven proportions, moderately long fingers, somewhat broader palms than Fenn or Aelari, a sturdier wrist and hand base" — L45; "Elven fingers, moderate elongation, broader palm than Fenn or Aelari, stronger wrist-to-hand transition. Never shortened human hands" — L139.
- [DIR] "overall scale, palm length and breadth, finger-length proportion, finger thickness. No per-finger controls yet" — L45, L139.
- [SOFT] Feet "Humanoid, moderately elongated, somewhat broader than Fenn or Aelari, stronger ankle-to-foot transition" — L47; L141.
- [DIR] "Length and breadth" — L141. [VAL] "Ankle, heel, arch, forefoot and toes stay believable. No prehensile or gripping adaptations" — L141; "No prehensile feet, clawed feet or cave-gripping toes. Underground competence needs no gimmicks" — L47.

**A7 Reach-related anatomy**
- [OPEN] "collision, melee reach, interaction reach, step height, climbing reach and other size effects" — v1.5 §21–23 L600; ECR L269.
- [VAL] "Vael don't automatically reach tiny spaces others can't, and underground doesn't grant automatic movement advantages." — L596.

**A8 Posture / Anatomical Resting Alignment**
- SILENT as a named concept (defined in Aelari L66). [DIAG]/[OPEN] Center of mass: "Whether torso depth, compact continuity and joint presence meaningfully change balance, turning, acceleration, stride or weight transfer. No bonuses or penalties are invented" — L576.
- [VAL] "Sneaking, sinister or predatory movement, grace, aggression and underground expertise are never biological" — L580; ECR L257 (no cave-adapted posture).
- [SOFT] "natural lumbar curve" — L121.

**A9 Population-specific axial structures**
- SILENT.

**A10 Head-to-stature**
- SILENT on ratio. [SOFT] Cranium "Moderate cranial height, less vertical elongation than Aelari" — L243 (face; UFCA). [VAL] Landmarks include head and neck across height, frame, muscle, fat, extreme proportions — L574.

## B. Skeletal Frame
- [SOFT] "Gracile next to humans (especially Skarn), but more joint presence than Fenn or Aelari at wrists, elbows, knees, ankles, shoulders and hand and foot bases" — L37. [VAL] "Never compact Skarn" — L37.
- [ANAT] "Frame changes the clavicles, ribcage, pelvis, joints and skeletal presence, and stays independent of muscle, fat, height, sex-related anatomy and presentation." — v1.1 §8–9 L128.
- [ANAT] "Narrow/Balanced/Broad are Skeletal Frame presets combined with composition" — L51.
- [SOFT] Joint scale: "gracile compared with humans, with somewhat more presence than Fenn or Aelari, always in proportion." [VAL] "Joints are never oversized, and hard bounds prevent thin limbs on implausibly tiny or oversized joints." — v1.1 §10 L132.
- [SOFT] Structural direction: "somewhat more structural presence through torso, joints and extremity bases" — L27.
- [SOFT] Ordering (greatest structural presence of three) — ECR L314.

## C. Physical Composition
- [ANAT] "Vael support the full range of muscle, fat, regional development and conditioning … Identity never depends on thinness, muscle or fat." — v1.0 §13 L51.
- [ANAT] "Muscle, fat, regional development and conditioning stay fully independent. The Vael skeleton survives very low or high muscle, low or high fat, mixed regional development and aging." — v1.1 §15 L145.
- [VAL] Torso depth never faked with fat or muscle — L114; failure "'Deep-bodied' becomes high body fat" and "They require muscle" — L206–207.
- [VAL] VL-16/17/18 stress table — L149–151 ("Skeleton is judged before soft tissue", L150).
- [VAL] Composition stress: Narrow lean or muscular, Balanced high fat, Broad lean/muscular/high-fat, Elder lean/muscular/high-fat — L521.
- Muscular Development Capacity vs Current Muscularity: SILENT. Fat distribution pattern: SILENT. Population-specific tissue systems: SILENT.

## D. Biological surface
- [SOFT] Colour families: "Charcoal, slate, cool gray, neutral gray, warmer gray, blue-gray, muted or desaturated violet, ash-brown, desaturated brown, and other grounded tones found in prototyping" — v1.3 §1–3 L363.
- [SOFT] Light to dark: "Meaningful variation from lighter to deeper values. Not every Vael is extremely dark or gray" — L364.
- [SOFT] Undertones: "Cool, neutral, warm, blue, violet, reddish, and brown or earth where appropriate. No highly saturated fantasy colors unless testing justifies them" — L365.
- [ANAT] "The target is living tissue, not painted stone." — L367.
- [ANAT] Living skin: "blood-flow influence, localized redness or equivalent perfusion, subsurface variation, regional differences (lips, eyes, ears, palms), freckles, moles, birthmarks or Vael equivalents, aging and environmental effects. It's never flat or monochrome. The universal Natural, Environmental, Applied and Acquired layers stay." — v1.3 §4–5 L371.
- [VAL] Lighting invariance and cave-lighting trap: "Stored pigmentation never changes under daylight, moonlight, firelight, magical light, blue cave light or warm interiors … The creator needs neutral lighting … Every approved family gets a neutral-light reference first" — §6–7 L375 (now universal per ECR L165).
- [OPEN] Sun response "(tanning, burning, pigment change, other reactions) is OPEN, resolved only if useful" — §8–9 L379.
- [SOFT] Environmental appearance varies; "Not every Vael is personally a cave-dweller" — L379.
- [VAL] Pigmentation distribution test: span lighter/mid/deeper across gray, blue-gray, violet-influenced and brown/desaturated-brown families — §14–15 L494.
- [OPEN] Frequencies — L383; ECR L159.

## E. Hair / homologues
- [ANAT] Biology (texture, density, natural color, hairline, age changes) vs presentation (length, cut, styling, shaving, braiding, tying, accessories, cultural grooming) — v1.3 §11–13 L389.
- [SOFT] Texture "Straight, wavy, curly, and coiled where valid. Not universally straight. Frequencies provisional" — L390.
- [SOFT] Colours "Black, very dark brown, brown, ash-brown, muted reddish or auburn where valid, inherited gray or silver-like, white or very light where valid. Frequencies OPEN, and white or silver is never required" — L391.
- [ANAT] Inherited silver vs aging: "A young, naturally white-haired Vael and an elderly gray-haired Vael are different states. The same rule applies to Aelari and any other applicable population." — §14 L395.
- [ANAT] Facial hair (pointer): "neither required nor prohibited by Vael ancestry" — §15 L399. Eyebrow-hair → UFCA slot 11 — L225.
- [VAL] "Hair and grooming are never locked to sex-related anatomy, frame, muscle, fat, class or occupation." — L407.
- Body hair: SILENT.

## F. Age
- [ANAT] "Vael visibly age: facial volume, skin elasticity, eye area, cheeks, jawline, neck, wrinkles, hair density and color, and ear tissue where appropriate." — v1.2 §25–26 L294.
- [OPEN] "Lifespan and aging rate are an OPEN DECISION." — L294; L616.
- [OPEN] "If Vael have specialized eye anatomy, aging must be tested against it. Elderly Vael aren't assumed to lose or keep the same vision, and the gameplay effects are unresolved." — L294.
- [ANAT] Skeleton survives aging — L145. Skin shows aging — L371.
- [VAL] VL-08 Elder (L87), VL-31 Elder face (L321), VL-50 Elder culturally neutral (L537); Deep-City Elder preset (L467); failure "Aging destroys Vael identity" (L345).

## G. Sex-related anatomy
- [ANAT] Frame "independent of muscle, fat, height, sex-related anatomy and presentation" — L128.
- [VAL] Hair and grooming never locked to sex-related anatomy — L407.
- Canonical sex tendencies: SILENT. R-SEX pointers: none. Reproductive biology: SILENT (ECR L245 fertility span E).

## H. Asymmetry & acquired history (non-facial)
- Natural body asymmetry: SILENT (face/ears only: L290, L298).
- [ANAT] Acquired layer retained — L371; ear damage "stay acquired" — L290.
- [PRES] "weathered, scarred, tattooed" as personal appearance — L407.
- Missing/damaged structures: SILENT.

## I. Presentation
- [PRES] Personal appearance never determines authenticity — §19–20 L407.
- [VAL] Biology vs culture: "Underground history never implies evil, cruelty, secrecy, treachery, religious fanaticism, social hierarchy, magical affinity or personality." — §21 L411. Four-layer model (ancestral biology / environmental adaptation / individual exposure / culture) — v1.0 §16 L63–70; ECR L183.
- [PRES] Clothing "Black armor and dark robes are never universal"; markings "never universally required" — §27–29 L435.
- [PRES] Presentation presets: Deep-City Practical, Surface Traveler, Artisan/Industrial, Merchant, Formal Urban, Military, Ceremonial, Foreign-Raised — "never alter anatomy" — L443, L478.
- [VAL] Cross-cultural pairs — L443, L523. Cultural neutralization — L522. No monolithic Vael culture — §30 L439.
- [VAL] Movement traits not biological — L580; expression never permanently sinister — L306.

## J. Creator system
- [LAT] Preset architecture: "complete, editable starting people built with the same system as custom characters and NPCs" — v1.4 §1 L455.
- [LAT] Character presets (provisional): Deep-City Engineer, Surface Merchant, Broad Craftworker, Lean Wayfinder, Heavyset Trader, Surface-Raised Vael, Deep-City Elder, Cross-Cultural Traveler — §2–3 L461–468; never assign class/stats etc.; library varies height, frame, muscularity, body fat, age, face, ears, skin, undertone, hair, eye color, grooming, presentation — L470.
- [VAL] Surface-Raised validation preset: "reference height, a Balanced or Narrow frame, moderate composition, brownish or desaturated natural pigmentation, dark natural hair, non-glowing eyes, subtle ears, ordinary above-ground clothing and no subterranean decoration. It must still read as Vael" — §4 L474.
- [VAL] "Every character preset must be reproducible with the player's own tools, with no preset-exclusive anatomy, and Simple and Advanced Mode keep the same underlying data." — §5–6 L478.
- [LAT] Population-aware randomization (height, frame, proportions, craniofacial, ears, pigmentation, undertones, hair, eyes); strengths Subtle / Diverse / Extreme "(proposed universal)" — §7–9 L482.
- [LAT]/[DER] Preserved relationships: neck to shoulders, shoulders to clavicles, ribcage to spine, torso to pelvis, pelvis to legs, limb thickness to joints, arms to hands, legs to feet, cranial to facial, ear base to skull, eye to orbit — §10–11 L486.
- [DIR] Groups: entire character, body, face, ears, natural pigmentation, hair, eyes, skin details, markings, presentation; "any parameter or group can be locked" — L486.
- [SOFT] Soft correlations allowed; rigid packages ("charcoal skin, white hair, violet eyes; or brownish skin, dark hair, brown eyes") not — §12–13 L490.
- [LAT] Deterministic generation: future requirement (NPC persistence, save/load, testing, bug reproduction, presets, multiplayer) — §16 L498.
- [ANAT] Unified record; "Shared ancestry does not automatically require one shared skeleton"; appearance-data requirements (schema/version tracking, migration, preset reproducibility, deterministic generation, save/load, Simple/Advanced continuity, randomization locks) unresolved — §24–26 L604.
- [VAL] Cameras incl. "optional first-person"; future creator lighting options without changing stored appearance — §15–17 L592. First-person arm proportions: SILENT (Fenn/Aelari have explicit rule; Vael only "first-person support" OPEN, L616).
- [VAL] Equipment across frame, height, muscle, fat, elder, extreme proportions; "watched especially around the deeper Vael ribcage for chest flattening …"; gloves/boots fit palm breadth, wrists, ankles — §11–14 L588. "Canonical equipment dimensions don't scale with the holder" — L600.
- [VAL] World compatibility full range; shared settlements work both ways — §18–20 L596.

## K. Locked validation tests (body / whole-character)
- VL-01 Reference 178 cm Balanced; VL-02 157 cm; VL-03 203 cm; VL-04 Narrow lean; VL-05 Broad; VL-06 Broad high muscle; VL-07 High body fat; VL-08 Elder; VL-09 Long-limbed near racial boundary; VL-10 Compact-proportioned; VL-11 Equal-height Fenn; VL-12 Equal-height Aelari; VL-13 Equal-height Sagekin; VL-14 Hidden-ear elven comparison; VL-15 Valid extreme proportional — L80–94.
- VL-16 Narrow low muscle low fat; VL-17 Broad high muscle; VL-18 High body fat; VL-19 Equal-height Fenn body; VL-20 Equal-height Aelari body; VL-21 Equal-height Sagekin; VL-22 Broad muscular Skarn boundary; VL-23 Deep ribcage with Narrow frame stress; VL-24 Max-height combined-proportion stress — L187–195.
- (Face/eye set VL-25–VL-42, L314–331; whole-character relevant: VL-30 high-body-fat facial, VL-31 Elder face.)
- VL-43 Surface-raised subtle ears neutral clothing; VL-44 Brown/desaturated-brown with dark hair; VL-45 Lighter valid pigmentation; VL-46 Deep valid pigmentation; VL-47 Broad low muscle; VL-48 Broad high fat; VL-49 Narrow high muscularity; VL-50 Elder culturally neutral; VL-51 Fenn boundary; VL-52 Aelari boundary; VL-53 Sagekin boundary; VL-54 Skarn boundary; VL-55 Cliché-convergence counterexample; VL-56 Diverse randomized; VL-57 Extreme valid randomized; VL-58 Full-neutralization; VL-59 Neutral daylight; VL-60 Very low light — L531–548.
- Permanent technical stress set: VL-03, VL-16, VL-17, VL-18, VL-48, VL-32, VL-33, VL-43, VL-58, VL-59, VL-60 — L608.
- Three-elf silhouette matrix (permanent) — §20–23 L159–167. Shared-ancestry test — L171. Full neutralization test — L502. Cliché-convergence and pigmentation distribution tests — L494. Daylight/low-light tests — L513. Composition stress — L521. Combined-proportion risk list — L155.

## L. Positive body identity statement
- "Vael have more compact structural continuity, a deeper torso and somewhat more skeletal presence, still recognizably elven." — v1.1 §1 L110.
- "Vael | More compact, deeper-bodied, with somewhat more structural presence through torso, joints and extremity bases" — L27.
- Silhouette: "Deeper torso, more compact torso-to-limb continuity, more joint presence, sturdier wrist, hand, ankle and foot transitions, moderate elongation, lower center of mass than Aelari" — L165.
- ECR: "Vael are deeper with compact continuity" (ECR L59); "Deeper, compact-continuity specialization" (ECR L275). Comparative wording per ECR L145: "greater average thoracic depth than Fenn and Aelari".

## M. Cross-population boundary tests (body)
- Fenn/Aelari/Vael "at about equal height" (v1.0) — L74; same height (v1.1) — L159; three-elf body test — L506. Stature: unspecified number.
- Marchfolk/Sagekin "similarly sized" — L74, L177, L519.
- Skarn: "tall, Broad, muscular Vael against a matched Skarn" — L178, L520.
- Durrim warning: "Durrim anatomy is never used to solve Vael compactness … Durrim v1.0 is now FIRST-PASS COMPLETE and the comparison uses it" — L179.
- VL-11/12/13, VL-19–22, VL-51–54 — K above.

## N. Forbidden controls / anti-patterns (body)
- "Never made by shortening Fenn arms with a slider" — L44; "Compactness never comes from just shortening legs" — L140.
- Torso depth never from "body fat, muscle, an oversized chest or uniform torso scaling" — L114.
- "a Narrow Vael is never a scaled-down Broad Vael" — L122; "No human pelvis plus a slider" — L124.
- No per-finger controls — L45, L139. "Sliders aren't rolled independently" — L486.
- No barrel-chest caricature; no short, thick-neck stereotype; joints never oversized — L120, L123, L132.
- Body failure conditions: identity depends on skin colour or ears; recolored Aelari; shortened Fenn; "Compact" becomes dwarf-like; "Deep-bodied" becomes high body fat; require muscle; Narrow lean become generic elves; Broad muscular become Skarn; valid controls produce incoherent anatomy; technical convenience overrides biology — L201–211; v1.4 L552.
- Prototype must not flatten torso or reduce joint differences — L568.

## O. OPEN / DEFERRED (body / whole-character)
- Technical foundation / MetaHuman — v1.0 §20 L98; v1.5 L564; architecture L604; ECR L265.
- Pelvis exact shape — L38, L124.
- Combined-proportion implementation "isn't chosen" — L155.
- Center-of-mass consequences — L576.
- Low-light mechanism, pupil, daylight, gameplay — L59, L264, L272, L584; ECR L100, L189.
- Sun response — L379.
- Lifespan/aging rate; elderly vision — L294.
- Collision/reach/step height; mounts — L600. First-person support — L616.
- Full open list (§30): lifespan and aging rate; elven lifespan relationships; ear mobility; ocular mechanism and low-light gameplay; daylight sensitivity; skin, hair colour, hair texture, eye colour frequencies; shared elven ancestry definition; skeleton architecture; MetaHuman suitability; morph/deformation; animation/retargeting; equipment fitting; headgear/ear; first-person; collision/reach; mounts; race/class restrictions; culture/background architecture; mixed ancestry; gameplay attributes; networked appearance sync — L616.
- Prototype protection list (incl. "lighting systems and eye materials") — L612.
- No RM-* references.

## P. Pass 1 provisional creator-control lists (BODY)
No list labelled "Pass 1". Body control lists as written:
- Spine/waist: torso length, ribcage length, width and depth, waist and lumbar length ("All relationship-aware") — L121. (Shoulder width and pelvic width are not listed as Vael controls, unlike Aelari L124. Shoulder/clavicle breadth appears only as a tendency in L122.)
- Arms: total length, upper-arm and forearm proportion, thickness, regional muscle — L138.
- Hands: overall scale, palm length and breadth, finger-length proportion, finger thickness, no per-finger — L45, L139.
- Legs: total length, femur and lower-leg proportion, thigh and calf thickness, regional muscle — L140.
- Feet: length and breadth — L141.
- Frame: Narrow / Balanced / Broad = Skeletal Frame presets combined with composition — L51, L128.
- Randomization groups, locks — L486. Strengths Subtle / Diverse / Extreme — L482.
- Status labels: body controls carry no explicit status label. "APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION" (L221) applies to facial/ear control organization only. Other labels: height "(provisional)" L13; three-branch table "(provisional)" L21; silhouette signal "(provisional)" L161; presets "(provisional)" L457; strengths "(proposed universal)" L482; lighting invariance "Proposed universal" L375 (now A via ECR L165); CURRENT IMPLEMENTATION / TARGET DESIGN L566–568.

## Extraction notes
- **Terminology:** "deeper torso" and "deep-bodied" (L3, L27, L110, L165, L506) are read per ECR L145 as "greater average thoracic depth than Fenn and Aelari", which is skeletal (L114, ECR L29). The ECR also forbids reading the deeper ribcage as a longer waist (ECR L47).
- **Torso share:** the Vael spec says "Greater torso share than Fenn" (L35) and "Moderate torso length" (L121). The ECR does not restate a torso-share ranking for Vael; it speaks of depth and compact continuity. No conflict.
- **Leg share:** "somewhat smaller leg share of height than Fenn or Aelari" (L46, L140) is not contradicted by the ECR, which says only "moderate elongation" (ECR L279). Spec canon stands.
- **Shoulder-joint presence:** L36 says "slightly more" and L122 says "more", relative to Fenn/Aelari. ECR L314 says "greatest average joint, base and skeletal structural presence of the three".
- **Lighting invariance:** L375 marks it "Proposed universal". ECR L165 locks it as a universal character principle (A).
- **Control-list gap:** the Vael torso control list (L121) omits shoulder width and pelvic width, which Fenn (L50) and Aelari (L124) list. Possibly unintended. Frame still changes clavicles and pelvis (L128).
- **First-person arms:** no Vael-specific rule like Fenn L487 or Aelari L574. Only cameras "optional first-person" (L592) and "first-person support" OPEN (L616).
- **Durrim reference** (L179): the comparison now uses Durrim v1.0 (first-pass complete), which is outside this extraction.
- Silent: sex-related tendencies, body hair, natural body asymmetry, Anatomical Resting Alignment term, Muscular Development Capacity/Current Muscularity split.
