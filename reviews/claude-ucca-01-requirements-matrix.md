# UCCA-01: Whole-Roster Requirements Extraction Matrix

**Author:** Claude (auditor / architecture analyst)
**Order:** `reviews/chatgpt-ucca-phase1-order.md` (89ca8f7), §5
**Phase:** UCCA Phase 1, design only. No race spec, PROJECT_RULES, UFCA_V1, STATUS or other canon is changed.
**Evidence:**
- `reviews/ucca-evidence/<race>.md`: one full extraction per race, sections A–P, every item tagged and cited by line.
- `reviews/ucca-evidence/prototype-gaps.md`: PROJECT_RULES creator rules, plus the prototype, plan, audit and register material on frame, height, scaling and saved appearance.

This matrix condenses the evidence. Where a cell and an evidence file differ, the evidence file and the spec govern.
**Scope:** the face is governed by the closed `decisions/UFCA_V1.md`. It appears here only where it touches whole-character systems (head-to-stature, age, sex, saved appearance).

## 0. How to read this matrix

**Race codes:**

| Code | Race | Code | Race | Code | Race |
|---|---|---|---|---|---|
| MF | Marchfolk | AE | Aelari | GR | Grask |
| SK | Skarn | VA | Vael | GO | Gorrund |
| SG | Sagekin | HV | Halvren | PK | Pipkin |
| FN | Fenn | DU | Durrim | CG | Cogling |
| SA | Saurin | | | | |

**Class tags** (order §5):

| Tag | Meaning |
|---|---|
| **A** | anatomical requirement |
| **DIR** | creator-facing direct control |
| **DER** | derived / coupled |
| **SOFT** | tendency / correlation |
| **VAL** | validator-only |
| **LAT** | latent preset / randomization variable |
| **PRES** | Presentation |
| **DIAG** | diagnostic / measurement |
| **O** | OPEN / not authorized |

**References:**
- `L###` is a line in that race's spec.
- `ECR` is `reviews/elf-comparative-review.md`.
- `SRR` is `reviews/short-race-comparative-anatomy-v1.md`.
- `LRR` is `reviews/claude-pass2-r2-large-race-comparative-review.md`.
- `PR` is PROJECT_RULES.

**SILENT** means the spec says nothing on the point. No biology has been inferred to fill a SILENT cell.

**Status of body creator controls.** No race spec labels a *body* control list as "APPROVED FIRST-PASS FUNCTIONAL REQUIREMENTS / PROVISIONAL CONTROL ORGANIZATION". That label covered facial organization only, now closed by UFCA. Body control lists appear as "controls to explore", "(provisional)", "(proposed universal)" or capability lists. The forms differ by race:

| Race(s) | Form |
|---|---|
| MF | v1.1 regions (L72–77) |
| SK | L86, L98, L102 |
| SG | L153–157 |
| FN, AE, VA | Torso, arm, hand, leg and foot lists |
| CG | §69 capability list |
| SA | Part 4 §145–§153 controls and §258 first-pass creator hard bounds ("may be revised by the universal creator-control review", §255) |
| HV, DU, GR, GO, PK | No body control list. Body variables appear as anatomy that varies, plus validation casts |

UCCA-11 Appendix A gives every listed item a disposition.

---

## 1. Positive body identity (what must survive neutralization)

| Race | Canonical body carrier | Ref |
|---|---|---|
| MF | Breadth of believable human variation; the **Human Reference Population**, "not the default anatomy for every humanoid race" | L13–15, L286 |
| SK | Biologically human, larger, heavier and more powerfully built; "not scaled-up Marchfolk and not automatically muscular". A lean, elderly, narrow or high-fat Skarn still reads Skarn | L7, L137 |
| SG | Fully human; population-level shift (leg share, slightly shorter torso, reduced ribcage depth, longer forearms, hands and fingers). Recognizable across a sample, **not every individual** | L21, L34, L58, L89, L250 |
| FN | Extremity-emphasized: limb-to-torso, forearm and lower-leg share, gracile skeleton, small joints, elven pelvis; "never thin humans with pointed ears" | L3, L7–18, L357; ECR L59 |
| AE | Whole-body vertical elongation through cranium, neck, torso, arms and legs; "never a uniformly scaled human or Fenn with stretched legs" | L33, L115; ECR L59 |
| VA | Greater thoracic depth than FN/AE (skeletal), compact torso-pelvis continuity, more joint and extremity-base presence | L110, L114, L165; ECR L59, L145 |
| HV | Coherent mixed human/elven organism. "Neither an averaged human and elf body nor a collection of independently inherited race parts"; own validity envelope | L9, L11, L80, L82 |
| DU | Compact Structural Concentration (SRR term): short adult stature, high skeletal presence, broad/deep compact torso, coordinated shorter limbs, substantial joints and extremities; "not humans scaled down" | L9, L66, L512; SRR L17 |
| GR | Elongated skeletal leverage and reach: greater limb, arm-span, forearm and lower-leg contribution; lower torso share; "not a human skeleton with individually stretched limbs" | L9, L23, L188, L192, L722 |
| GO | Massive load-bearing architecture, **Axial Load-Path Continuity** (validator term, not a slider), broad/deep torso, substantial joints | L9, L35, L165, L709–711 |
| PK | **Low-Set Compact Trunk Architecture** (primary; not a slider): moderate thorax → compact lower trunk → mature broad pelvis → sustained limbs; light skeleton; adult, never childlike | L19, L133–141, L1498–1506 |
| CG | **Fine-Scale Elongated Articulation** (not a slider): narrow stable core, near-human total limb share, distal redistribution to forearm, lower leg, hands and fingers, fine shafts | L31–41, L545–547, L3155 |
| SA | **Counterbalanced Pelvic-Axial Architecture**: deep mobile thorax → elongated lower axial trunk → integrated pelvis/sacral base → mandatory counterbalancing tail. The tail must look "anatomically inevitable", not attached | L12, L56, L614, L3523, L3547–3553 |

## 2. Stature

| Race | Min / Reference / Max | Status and notes | Ref |
|---|---|---|---|
| MF | 147 / 173 / 203 cm | Approved first-pass envelope; 173 = Reference Height | L19–23, L286 |
| SK | 183 / 208 / 229 cm | Provisional; overlaps MF intentionally | L11–15 |
| SG | 152 / 178 / 208 cm | Provisional; never the main marker | L70–74 |
| FN | 157 / 181 / 211 cm | Provisional | L22–26; ECR L28 |
| AE | 168 / 190 / 221 cm | Provisional; the 221 cm technical stress character is permanent; maximum never cut for the prototype | L25–27, L594; ECR L336 |
| VA | 157 / 178 / 203 cm | Provisional; "compact never means short" | L15–19, L29 |
| HV | ~152–213 cm **central population envelope**, ref ~178 | **Not an absolute wall**; ancestry-dependent tails allowed below and above; tail limits and frequencies **OPEN**; never clipped, compressed, uniformly scaled or parent-averaged | L86–90, L481, L490 |
| DU | 122 / 137 / 152 cm | Provisional; distribution "left for later" | L15–19 |
| GR | 198 / 218 / 239 cm | First-pass range, cross-race validation pending; no longer tallest | L15–19, L178 |
| GO | 208 / 229 / 251 cm | First-pass; 251 = "current world-validation upper stature, never a permanent maximum" | L27–31 |
| PK | 91 / 107 / 122 cm | Provisional; no longer the lower roster boundary | L25–29, L119, L1531 |
| CG | 76 / 91 / 107 cm | Provisional; the smallest population; "no whole-body scale multiplier is authoritative" | L53–67 |
| SA | 168 / 188 / 208 cm (tail excluded) | **Racial hard bound**; frozen reference 187.9 cm | L64–68, L4164, L4234 |

**Roster span:** about 76–251 cm (PK L119).

**Distribution shapes** are SILENT or OPEN for every race.

**Height is never uniform scaling** (MF L23; SK L40; DU L19; GR L19; GO L31; CG L2685; HV L481; PR L29).

## 3. Torso and axial

| Race | Requirement | Kind | Ref |
|---|---|---|---|
| MF | Chest width/depth, waist, abdomen, torso length controls; ribcage–waist and shoulder–ribcage relationships validated | DIR, VAL | L74–75, L31 |
| SK | Slightly larger torso share; wider, deeper ribcage; broader upper back; "deeper chests change ribcage volume" | SOFT, DER | L75–76, L86, L90 |
| SG | Slightly shorter torso relative to stature; **reduced ribcage depth (AC-6)**; linear silhouette | SOFT, DIR | L139–141, L89, L155 |
| FN | Smaller torso share, shallower ribcage, compact chest. "Longer waist transition" is read through ECR L45: never longer than Aelari | SOFT | L50, L110; ECR L45 |
| AE | Longer torso and waist than FN/VA; relatively shallow thoracic depth | SOFT, DIR | L48, L123–124; ECR L46 |
| VA | **Torso depth is skeletal**, never fat, muscle or uniform scaling; deeper than FN/AE; strong torso-pelvis continuity | A, SOFT | L114, L120–121; ECR L29, L47 |
| HV | Torso inheritance (width, depth, length, waist, spine, torso-pelvis) "never human torso versus elf torso" | A | L120 |
| DU | Broad/deep skeletal thorax relative to stature; greater torso contribution, vertically compact; thoracic depth ≠ fat | A, VAL | L25–30, L97–104 |
| GR | Lower torso contribution than MF/SK, never a small torso; breadth less than SK relative to stature; depth never Durrim-like | A | L37–40, L198–207 |
| GO | Greater torso share than GR at matched height; high breadth and depth; **never one Torso Size / Body Thickness**; ALPC chain | A, DER | L39–43, L169–186, L709–721 |
| PK | LSCTA: modestly reduced central-trunk share; pelvis structurally important relative to the thorax; thorax moderate; "not a slider" | A, SOFT | L133–155 |
| CG | Narrow stable core; torso contribution near MF; adult thorax "not an hourglass device" | A | L98–102, L647–669 |
| SA | Deep, mobile, moderate-breadth thorax; elongated lower axial trunk. Bounds: thoracic depth ±8 %, width ±7 %, axial trunk length ±10 %. Coupled depth/width ratio 0.80–1.00 | A, DIR, VAL | L94–113, L4164–4166 |

## 4. Limbs and segments

| Race | Requirement | Kind | Ref |
|---|---|---|---|
| MF | Leg length control; upper-arm/forearm and femur/lower-leg relationships validated; arm length not listed as a control | DIR, VAL | L76, L31 |
| SK | Arm and leg length vary; "more substantial limbs and larger joints"; no huge-upper-body/tiny-legs default | DIR, SOFT | L78, L86, L94 |
| SG | Greater leg share; longer forearms, hands and fingers (AC-6); never elven limb proportion | SOFT, DIR | L137–138, L156–157, L435 |
| FN | Longer limbs relative to torso; greater forearm and lower-leg share | SOFT, DIR | L35, L51–52, L121–123; ECR L33 |
| AE | Even elongation across segments, "not one extremely long segment" | SOFT, VAL | L56–58, L152–154 |
| VA | Moderate elongation; **somewhat smaller leg share than FN/AE**; compactness "never just from shortening legs" | SOFT, VAL | L44–46, L138–140 |
| HV | Segments needn't share one ancestry strength; coupling keeps transitions coherent | A, DER | L126–131 |
| DU | Lower limb contribution than MF at equal height; femur and lower leg needn't shorten by identical percentages; "no fixed arm ratio" | A, DER | L38, L113, L119 |
| GR | Greater leg, arm and span contribution; forearm and lower-leg emphasis; **"never one Arm Span slider"**; arm-span ratios OPEN | A, O | L52, L213–229, L310–314 |
| GO | Lower limb share than GR; "long-armed" shorthand forbidden; large absolute arms | A | L57, L196–202, L277–283 |
| PK | Limb contribution preserved relative to Durrim; legs never automatically exceed ordinary human adult proportions; no forearm emphasis | A, O | L54–56, L164 |
| CG | Total limb share near MF; within-limb distal redistribution | A | L136–147, L558–584, L619–626 |
| SA | Moderate-to-long legs; forearm may carry somewhat more contribution than MF. Bounds: arm ±6 %, leg ±6 %; frame never changes lengths | A, DIR | L256–261, L294–300, L4164–4168 |

## 5. Shoulders and pelvis

| Race | Requirement | Ref |
|---|---|---|
| MF | Shoulder width, hip width and pelvis-proportion controls; frame = shoulder, ribcage, pelvis, joints | L27, L74–75, L83–86 |
| SK | Broader clavicles and upper back, more substantial pelvis; "shoulders act as one connected system" | L76–77, L90 |
| SG | Shoulder and pelvis width controls | L155 |
| FN / AE / VA | Distinct elven pelvis, **exact shape OPEN**; gracile shoulders; Broad gains real skeletal breadth (AE) | FN L107–111; AE L49, L125–126; VA L36–38, L122–124; ECR L32, L281 |
| HV | Pelvis "a developmentally viable mixed structure, not a linear morph"; pelvic inheritance **OPEN** (Class B dependency) | L122, L497 |
| DU | Substantial clavicles; pelvis morphology OPEN, never a widened human pelvis | L31–32, L105–109 |
| GR | Shoulders race-specific, "never one Shoulder Width concept"; pelvis functional requirement locked, morphology OPEN | L41, L45, L205–209 |
| GO | Skeletal shoulder ≠ deltoid; shoulder-to-pelvis continuum, not subtypes; pelvis load-bearing, integrated in ALPC | L45, L187–189, L715–718 |
| PK | Mature broad pelvis is skeletal ("not wide hips caused by body fat"); **never a scaled-down juvenile pelvis**; never one hourglass silhouette | L50, L149–153, L182 |
| CG | Mature adult pelvis, not the dominant anchor; "no single shoulder-to-hip ratio defines identity" | L252–262, L683–689 |
| SA | Pelvis a primary carrier, posteriorly organized, integrated with the tail base. Bounds: shoulder ±8 %, pelvic width ±7 %. Frame changes shoulder and pelvic width, never pelvic depth or sacral-caudal organization | L121–156, L4164–4168 |

## 6. Neck

| Race | Requirement | Ref |
|---|---|---|
| MF | "Neck thickness" control, "not automatically skeletal" | L74, L283 |
| SK | More substantial neck base; neck in the regional-muscle list | L77, L102 |
| SG | SILENT | — |
| FN | SILENT in spec; ECR "intermediate" | ECR L31 |
| AE | Longer than humans and FN on average (ECR: and VA); **absolute ≠ proportional neck length**; no neck control listed | L50; ECR L320 |
| VA | Somewhat shorter relative to torso than AE | L123 |
| HV | Absolute length, relative length, circumference, skeleton, muscle kept separate; "never one 'neck size' control" | L122 |
| DU | Short contribution; skeletal integration, not neck muscle | L21, L107, L249 |
| GR | Moderate-to-long; never relied on for identity | L43, L172 |
| GO | Moderate, highly integrated | L46–47, L192 |
| PK | Adult; relationships later | L48 |
| CG | Varies; no mandatory thin or thick neck | L268–272, L715–723 |
| SA | **Neck length ±15 %, neck depth ±10 %** | L4164 |

## 7. Hands and feet

| Race | Requirement | Ref |
|---|---|---|
| MF | Hand and foot size controls; but "one generic size scalar isn't a sufficient biological definition; exact controls future" | L74–76, L284 |
| SK | Larger hands and feet; hand size/breadth, finger proportions, foot length/breadth "to explore" | L79, L98 |
| SG | Hand length/breadth, finger proportion; foot length/breadth; hands "human anatomy" | L89, L156–157 |
| FN / AE / VA | Overall scale, palm length/breadth, finger length/thickness; **no per-finger controls yet**; foot length/breadth; no prehensile feet | FN L122–124; AE L153–155; VA L139–141 |
| HV | "Never one hand size / foot size scalar"; humanoid, no claws | L133 |
| DU | Relatively large hands and feet; "never one Hand Size / Foot Size" | L44–46, L115, L121 |
| GR | Large hands, finger:palm tendency; 5 digits; plantigrade; frame does not set foot breadth | L233–245, L322–326 |
| GO | **5 digits locked**; large dexterous hands; plantigrade | L71, L206–216 |
| PK | Moderate hands; 5 digits locked; feet somewhat larger tendency; "never one big-feet control"; hand dimensions independent | L58–64, L170–176 |
| CG | Hands a supporting identifier; long fingers; **palm and finger dimensions must not collapse into one control**; feet: seven foot dimensions | L163–181, L588–643 |
| SA | 5-digit hands, opposable thumb; claw-like nails; plantigrade (not digitigrade). Bounds: hand ±8 %, foot ±8 %. Claw controls (length, curvature, width, thickness, tip, pigment) with no numeric canon | L306–312, L1739–1770, L4164, L4203 |

## 8. Reach

| Race | Requirement | Ref |
|---|---|---|
| All | **Anatomical, interaction, combat and camera-targeting reach are separate systems**; none is set by visual scale; gameplay reach is OPEN everywhere | MF L265; SK L350; DU L455; GR L61, L646; GO L98, L623; PK L898; CG L2846–2855; SA L3284–3300; PR L27 |
| GR | Genuinely greater anatomical reach tendency (arm length, span, forearm, hand) | L646 |
| GO | Large absolute reach ≠ Grask relative reach | L65 |
| CG / PK | Short absolute reach; anatomy never distorted to normalize it; no hidden arm extension | CG L2402–2408; PK L896–898 |
| SA | **The tail never extends hand-interaction or combat reach** | L3284–3300 |

## 9. Posture / Anatomical Resting Alignment

**The universal rule.** Anatomical Resting Alignment is distinct from Cultural/Personal Body Language (PR L21; AE L66–69 defines it).

| Race | Requirement | Ref |
|---|---|---|
| DU | Ordinary relaxed stance, never a crouch or hunch | L428 |
| GR | Upright; no hunch or ape arm-hang | L90, L622 |
| GO | Upright plantigrade | L601 |
| PK | Upright adult alignment; LSCTA needs no crouch | L699–714 |
| CG | Upright; posture never creates smallness | L709–711, L2486–2496 |
| SA | Upright; counterbalance guard **≤ +3° extra forward lean** beyond the frozen reference; balanced neutral posture and density model OPEN | L411–421, L4148, L4160 |
| MF, SK, SG, FN, VA, HV | SILENT on the term | — |

## 10. Population-specific axial structures (the Saurin tail)

**Only Saurin have one.** All other specs are SILENT or say "no tail" (GR L88 "not approved").

**Saurin tail (mandatory, never a toggle):**

| Item | Canon | Ref |
|---|---|---|
| Length | 55–80 % of standing height; the 80 % endpoint is "not an entitlement for every body" | L174, L3606 |
| Frozen reference | 121.4 cm = 64.6 % H | L4143 |
| Length → base | **Length is the driver**: base ≈ length^1.18 | §256 L4145 |
| Root-sufficiency band | 0.75–1.20 | L4145 |
| Taper | Loss rate ≤ 1.25× reference | L4146 |
| Mid-tail area | 0.27–0.48 of root | L4147 |
| Distal area | ≥ 0.065 of root | L4147 |
| Reachable length by frame/composition | ~78 % H Balanced; 80 % H Broad; ~72 % H Narrow high-fat | L4149 |
| Tail muscularity and caudal fat | **Follow Physical Composition**; no independent tail-muscle slider; root-concentrated fat invalid | L4150–4151 |
| Carriage | +8° lift … +10° droop | L4152 |
| Tail-base breadth | Frame component follows pelvic width | L4154 |
| Validator outcomes | FAIL and CONSTRAIN cases listed | L4156 |
| World-space reach | ~170 cm behind the heel at the extremes | L4272 |
| Coupling | Tail variation always coupled to pelvis and sacral base | L182–207 |
| Tail loss / injury | **OPEN**; never a creator substitute; excluded from randomization | L209, L2324 |
| Partial garment coverage | Allowed if the tail persists; construction extent OPEN | L3122–3140, L4067 |

## 11. Head-to-stature (whole body)

| Race | Requirement | Ref |
|---|---|---|
| SA | **DIR: head length 0.156–0.184 H (±8 %; "the +8 % head-scale decision is the centre")**; head-height share near to modestly below MF (§55). Tension noted | L970, L4164 |
| DU, PK, CG | Somewhat greater head contribution than MF allowed, **never oversized and never a maturity or racial carrier**; ratio OPEN | DU L21; PK L33, L199; CG L274–284 |
| GR, GO | Ratio OPEN; avoid tiny-head giant and uniformly scaled human head | GR L433; GO L299, L407 |
| MF, SK, others | Head–body relationship validated; no ratio | MF L31; SK L40 |

UFCA AD-U4 already holds non-Saurin head scale at VAL / DIAG.

## 12. Skeletal Frame

**Universal rules:**
- Skeletal Frame = continuous skeletal configuration.
- Narrow / Balanced / Broad = **editable starting presets, not castes** (PR L13, L66).
- Frame ≠ muscularity, fat, fitness, personality or sex (MF L27, L285).

| Race | What frame changes / never changes | Ref |
|---|---|---|
| MF | Shoulder breadth, ribcage, pelvic breadth, joint scale, skeletal visual mass. **Athletic is not a frame** | L5, L27, L281, L285 |
| SK | All three frames inside Skarn; Broad never Gorrund | L32 |
| SG | All three; "Sagekin ancestry never means narrow or thin" | L93 |
| FN | Gracile skeleton, smaller joints with **hard minimum boundaries**; Broad stays light-boned | L32–44, L107, L115 |
| AE | **"Frame changes the real skeleton: clavicle, ribcage and pelvic breadth, joints"**, separate from muscle, fat, sex, height | L130–134 |
| VA | Frame changes clavicles, ribcage, pelvis, joints; "a Narrow Vael is never a scaled-down Broad Vael" | L122, L128–132 |
| HV | **Frame Presets are not ancestry categories**; valid ranges may depend partly on ancestry; no "Elf Gracility" slider | L54, L105, L137 |
| DU | Breadth and joints, "never every dimension equally"; never muscle alone; Balanced is not the canonical body; no height-frame packages | L50–52, L127–131 |
| GR | **Breadth relationships only; never height, limb or hand/foot length, muscle or fat**; frame never fixes foot breadth | L70, L249, L326 |
| GO | Breadth only; never height, muscle, fat, hand/foot size or face; Broad never hard-links to maximum depth; bones and joints never scale linearly with stature | L80, L220–224 |
| PK | Shoulder, thoracic and pelvic breadth, joints; never height, muscle, fat, face or hair | L68, L166 |
| CG | Clavicle, thorax and pelvic breadth; robusticity and joints as **starting tendencies only (AC-9)**; robusticity is a distinct parameter | L755–783 |
| SA | **Changes:** shoulder breadth, thoracic width (depth ±2 % only), pelvic width, limb/joint girth, hand/foot breadth, tail-base frame component, reachable tail length. **Never:** stature, long-bone/axial lengths, skull, pelvic depth / sacral-caudal | L4168, L4149 |

**Prototype placeholder.** The prototype's "Frame" swaps the Manny and Quinn mannequins. This mixes sex-related anatomy and body type with frame. It is a current placeholder, incompatible with the target (prototype-gaps §3 #1; audits 01 L24, 05 L13).

## 13. Physical Composition

**Universal rule:** Current Muscularity, Body-Fat Amount and Body-Fat Distribution are separate (PR L14). Muscular Development Capacity ≠ Current Muscularity (PR L67).

| Race | Requirement | Ref |
|---|---|---|
| MF | Overall muscularity, fat amount + distribution (Part 1 §2), regional muscle; **no thin-to-heavy slider**; composition presets Lean / Athletic / Muscular / Heavy / Custom; Athletic never sets skeleton | L27, L53, L68, L281–282 |
| SK | Higher **Muscular Development Capacity** (not a default Current Muscularity); 10 regional muscle groups; **mass derived, body weight not a slider** | L26, L80, L102, L106 |
| SG | Full range; derived mass, no weight slider | L101, L161–169 |
| FN / AE / VA | Full range; identity never depends on thinness | FN L58; AE L62; VA L51, L145 |
| HV | Composition not ancestry; Skarn ancestry shifts capacity, never current build | L54, L137, L447 |
| DU | Full range; low-muscle Durrim is a permanent test; the legacy mass multiplier is superseded | L54, L135 |
| GR | Capacity vs current; **whether Grask capacity differs is OPEN** | L72, L251 |
| GO | Capacity OPEN, never inferred from skeleton; ALPC readable at low muscle | L82, L228, L720 |
| PK | Capacity OPEN, "never lowered because Pipkin are small"; no "round halfling"; no hidden physique packages | L72, L180–184 |
| CG | Capacity vs current explicit; "fine bones don't require low capacity"; fat amount and distribution distinct controls | L314–331, L818–869 |
| SA | Capacity, current, fat amount, fat distribution all independent. Muscle and fat regions are listed. **Prohibited:** human pectoral blocks, six-pack, buttocks, bodybuilder width, uniform inflation | L358–381, L4170 |

## 14. Saurin E/B tissue and anti-hourglass canon

- **E** = coelomic body-wall fullness. **B** = ventral fullness.
- Both are Biological Anatomy tissue tendencies, **never folded into the fat control**.
- Male centre 0. Female centre: E 2.0 cm; B 1.6 cm, with a **B ceiling of 3.0 cm**.
- Constrain cases: Narrow + B 3.0 → ~2.1 cm.
- **Anti-hourglass:** "a fuller, continuous coelomic body wall … not a narrower waist". Human breasts were evaluated and rejected; no hip flare and no buttocks.

(SA L4211–4253)

**Related bans in other races:** Cogling thorax "not an hourglass device" (L669); Pipkin pelvis "never one hourglass silhouette" (L149).

## 15. Biological surface

**Universal rules:**
- Four Skin Appearance Layers: Natural / Environmental / Applied / Acquired. Dirt is Environmental (PR L68).
- Lighting invariance (ECR L165).
- **Pigmentation is multidimensional, never one Skin Color slider** (DU L354; GR L506; GO L508; CG L1728; HV L245).

| Race | Integument family and key requirement | Ref |
|---|---|---|
| MF, SK, SG | Human skin; four layers; regional environmental appearance (face, hands, forearms, feet) "proposed universal" | MF L153–162; SK L207–220; SG L269–273 |
| FN, AE | Human-like skin; elven ranges (ECR-corrected); no green or forest default; Aelari not pale-mandatory | FN L240–260; AE L292–303; ECR L157–158, L223 |
| VA | Charcoal/slate/gray/blue-gray/violet/ash-brown families; "living tissue, not painted stone"; sun response OPEN | L363–379 |
| HV | Never RGB averaging; ancestry can be visually latent | L243–262 |
| DU | Broad human-like envelope; ruddiness never required; soot and grime never racial | L353–362, L389 |
| GR | Earth-toned, low-to-moderate chroma envelope; never required green or gray; warts not racial | L493–516, L578–586 |
| GO | Earth-toned ≠ dark; green not established | L506–509, L572–591 |
| PK | Broad range; no "freckled halfling"; nails ordinary | L474–506, L571–575 |
| CG | Broad range; no "cute" bundle; texture not exaggerated | L1706–1766, L2008–2015 |
| SA | **Scaled integument, Regional Scale Architecture**: structural, articulation, fine and ventral fields. **No global scale-size control**. Pigment and pattern families; pattern controls (family, contrast, density, scale, edges, weighting, continuity, tail, facial); claw keratin colour; matte–satin material; no RGB picker; thermoregulation OPEN | L1323–1506, L4207, L2048 |

## 16. Hair and homologues

| Race | Scalp hair | Body hair | Ref |
|---|---|---|---|
| MF, SK, SG | Full human range; biology ≠ style | **SILENT** | MF L166–175; SK L224; SG L277 |
| FN, AE, VA | Biology ≠ presentation; natural silver/white ≠ aging | **SILENT** | ECR L171–174; AE L324–336; VA L389–395 |
| HV | Biology ≠ presentation; no averaging | **SILENT** | L266 |
| DU | Biology ≠ presentation | **OPEN** | L199, L207 |
| GR | Bald valid; distributions OPEN | **OPEN** | L402 |
| GO | Never skin-locked | **OPEN, "never inferred heavy from size"** | L365, L519 |
| PK | Broad; no hairstyle biological | **States variation**; locked: hairy feet not required; sex distributions OPEN | L359–361, L561–567 |
| CG | Broad | **States variation**, "not determined by" scalp hair, sex, etc.; sex distributions OPEN, soft only | L1772–1823 |
| SA | **No mammalian hair** | Absent; filamentous integument OPEN | L1907–1913 |

**Interfaces:**
- Facial hair and eyebrows → UFCA slot 11.
- Saurin keratin display → UFCA slot 10, with an optional restrained body continuation (SA §101a L1686–1694).

## 17. Age

**Universal rules:**
- Adult creator scope; triad distinct (PR L16).
- Cosmetic age carries no gameplay penalty (MF L212).

| Race | Requirement | Ref |
|---|---|---|
| MF | Age affects composition and posture; aging "more than wrinkles and gray hair" | L210–212, L257 |
| SK | "Old age is not frailty" | L183 |
| FN / AE / VA | Visibly age, including body composition and posture where individually appropriate | ECR L245 |
| HV | No lifespan-percentage slider | L325 |
| DU | Aging never "just wrinkles plus gray hair"; never all frail | L374, L383 |
| GR | Older not automatically hunched or frail | L534 |
| GO | Aging never an ogre caricature | L527–529 |
| PK | Adult at the youngest age without age cues; elder without mandatory frailty | L385–389, L971–975, L1476–1481 |
| CG | Age cannot change stature dramatically; no stoop required | L1943–1947, L2524–2530 |
| SA | Systemic aging list; firewall (no frailty, stoop, reduced tail control); age presets young / established / mature / late adult | L2113–2152 |

**Lifecycle is OPEN everywhere.**

## 18. Sex-related anatomy

| Race | Canon | Ref |
|---|---|---|
| MF | "No hard sex-specific height restriction … overlap stays broad" | L23 |
| SK, SG, FN | SILENT ("no shift" valid under R-SEX) | — |
| AE, VA | Frame, hair and hip width never locked to sex-related anatomy | AE L126, L134, L344; VA L128, L407 |
| HV | Separate; **Class B source dependency** | L54, L497 |
| DU, GR, GO | **OPEN**; never assume human dimorphism | DU L58; GR L76; GO L82 |
| PK | May influence pelvic, thoracic, facial and soft-tissue relationships; magnitude OPEN; like-for-like comparisons | L72, L1487–1494 |
| CG | May affect pelvis, thorax, soft tissue; not a binary set; magnitude OPEN | L337–352, L875–877 |
| SA | **CLOSED (§263)**: shifts only lower trunk +7 %, pelvic band +5.5 %, E 2.0 cm, B 1.6 cm (ceiling 3.0); identical hard bounds; overlap mandatory; **no control named "female body"**; reproductive biology OPEN | L4211–4253 |

## 19. Asymmetry and acquired history (non-facial)

- **Natural body asymmetry:** stated **only by SA** (claw shape, tail resting curvature, pattern, ridge and display; L2156–2166). It is SILENT in all other specs.
- **Acquired history:** a layer in every race; scars never forced by class or occupation (MF L189); never toughness shorthand (GO L535).
- **Saurin acquired:** scale damage, chipped claws, damaged ridges (L1863–1872).
- **Major tail / rostral / jaw loss:** OPEN and excluded from randomization (SA L2324).
- **Missing or damaged body structures:** SILENT elsewhere.

## 20. Presentation

| Item | Canon |
|---|---|
| Separation | Culture, occupation, class, personality, reputation are never biology (PR L15; MF L35; SG L11–17; GR L80; PK L1456–1470; CG L389–406; SA L456–470) |
| Presentation presets ("proposed universal") | Never replace anatomy (SK L247; SG L301; FN L333; AE L380/L431, two differing lists; VA L443) |
| Identity layers (proposed universal) | Ancestry / Birthplace / Culture / Background (SG L305–312) |
| Body language | Never biological: no graceful-elf, sinister, waddle, bounce or fidget defaults (FN L447; VA L580; PK L963–967; CG L2470–2496) |
| Clothing / equipment | Fits anatomy; canonical equipment never scales with the holder (PR L26) |
| Saurin tail presentation | Wraps, bands, jewellery, partial coverage allowed, "cannot cosmetically erase its presence" (L211) |

## 21. Creator-system requirements

| Requirement | Canon |
|---|---|
| Modes | Simple Race → Preset → Confirm; Advanced Race → Preset → Customize → Confirm; one data model (PR L8–9; MF L227; PK L1398–1403; CG L2915; SA L2246–2260) |
| Presets | Legitimate outputs of the same system; no preset-only anatomy (PR L10; MF L216; AE L435; VA L478; GR L687; GO L693; PK L1364; CG L2919; SA L2264). Race libraries: MF 6 themes; SK 8; SG 8; FN 8; AE 8; VA 8; HV codes A–M (I–M internal labels only); DU directions; GR tendencies; GO families; PK 8 coverage concepts; CG neutral set; SA presets + surface + age + tail presets |
| Preset tiers in canon | Character vs Presentation presets (SG L324–327); frame and composition presets (MF L5); PK frame presets vs coverage presets (two tiers, relationship unstated, PK notes) |
| Randomization | Race-aware, relationship-aware, never independent rolls then repair; biological vs presentation separate; Saurin adds Acquired-History randomization (PR L11; SK L284; SA L2298–2326, L4257) |
| Selective randomization and locks | Every race that states it; locks absolute; locked child never forces invalid parent (PR L38; CG L2983–2989; SA L2346–2364) |
| Saved appearance | One unified record with schema/version and migration (MF L261; register L456). Halvren: genealogy inputs / phenotype / final anatomical state; "final slider values alone may not suffice" (L70, L394). Cogling: semantic reconstruction; cross-race reuse via semantic mapping (L2993–3013). Saurin: stored by layer (L2537–2552). PK: stable conceptual traits ≠ mesh values (L1438–1444) |
| Saved-appearance gap | **Prototype record holds only frame, height step, two colours, finish** (plan L83; audits 06 L20, 07 L7) |
| NPC parity | Same system (DU L508; GR L687; GO L693; PK L1405; CG L3017; SA L2556) |
| First-person | OPEN everywhere. If supported: actual eye height, own arms and hands, never generic human arms (FN L487; AE L574; PK L1312–1316; CG L2462; SA L2662–2671, L3396–3402) |
| Gameplay firewall | Appearance never changes stats (MF L39; SA L2631–2645; PK L1018–1039) |

## 22. Locked body / whole-character validation inventory (carried forward)

| Race | Tests |
|---|---|
| MF | Unnamed: height characters 147/173/203; frame independence; proportion stress; identity stress; preset round-trip; randomization sample; world (L249–265) |
| SK | SK-01…12; v1.1 validation characters 1–8; silhouette; equal-height 190 cm; anti-stereotype; animation (L126–133, L288–342) |
| SG | SG-01…14; large-sample; clone/stereotype; cultural neutralization (L360–431) |
| FN | FN-01…17, FN-28…38; final gate (L84–152, L397–407, L521–540) |
| AE | AE-01…24, AE-37…50 (L85–190, L496–509) |
| VA | VL-01…24, VL-43…60; three-elf silhouette (L80–195, L531–548) |
| HV | Source-passing, mixed silhouette, equal height, extreme combinations; HV-01…50; HV-FAMILY-01/02 (L145–148, L357–488) |
| DU | Part 1 tests, cross-population 152 cm, Part 5 movement tests, failure list (L72–154, L496–508) |
| GR | GR-BODY-01…18, GR-MOVE/INT/EQUIP, AD-2, AD-3 (L96–132, L288–296, L693–718) |
| GO | GOR-BODY-01…18, GOR-STRESS-01…09, GOR-MOVE/INT/EQUIP, AD-1, AD-3, ALPC tests (L129–271, L667–733) |
| PK | PIP-BODY-01…29, PIP-STRESS-01…10, PIP-MOVE-01…24, PIP-INT-01…21 (L100–236, L1045–1081, L1593–1613) |
| CG | COG-BODY-01…31 (25/26 retired), COG-MOVE, COG-WORLD, COG-CC-01…15 (L451–471, L1061–1076, L2585–3098) |
| SA | SAU-BODY-01…22 + SILHOUETTE, SAU-SURF, SAU-CC-01…29, SAU-MOVE, SAU-EQP, SAU-WORLD, SAU-CAM, SAU-GAME; §246–§247 populations (L538–560, L2000–2026, L2687–2715, L3420–3455, L3950–3981) |
| Comparative reviews | SR-COMP-01…12 (SRR); LR-01…12 and AD-1…AD-5 (LRR) |

## 23. Explicitly OPEN / deferred (body; not resolved by UCCA)

| Topic | Races / where |
|---|---|
| Pelvic morphology | FN, AE, VA, HV (Class B), DU, GR, GO, PK, CG; SA sacral |
| Segment ratios and numeric proportions | All |
| Arm span | GR, PK |
| Joint / robusticity distributions | All |
| Head-to-stature | All except SA |
| Muscular Development Capacity distributions | GR, GO, PK, CG |
| Fat-distribution tendencies | All |
| Sex dimorphism magnitude | DU, GR, GO, PK, CG |
| Reproductive biology | SA, explicitly |
| Lifecycle | All |
| Body hair | DU, GR, GO OPEN; others SILENT |
| Halvren height tails | HV (L481, L490) |
| Saurin balanced posture and density model; caudal-base landmark; numeric lower-trunk minimum vs MF; numeric Broad-vs-Gorrund boundary; claw and digit numeric ranges; per-field scale ranges; tail world-space validation; tail loss | SA §265 |
| Thermoregulation | SA |
| Skin thickness / durability | DU, GR, GO |
| Legacy gameplay traits | SK breath, FN sneak/swim, DU breath/swim, GR, GO, PK sneak, SA breath/swim |
| Collision, reach, camera, first-person, mounts, equipment fitting, animation / IK / retargeting, technical body architecture, save schema implementation | All |

## 24. Measurement-deferred items already queued

| Item | Covers |
|---|---|
| RM-LR-01…07 | Large races, including the GR-BODY-10 floor and ALPC proxies |
| RM-SR-01…06 | Short races |
| RM-OT-01…05 | Sagekin, elves, Halvren source-passing, Saurin vs SG/HV, world scale |
| RM-CF-10 | HSR |

No race spec carries an RM-* reference.

## 25. Cross-cutting findings (inputs to UCCA-02…11)

| # | Finding |
|---|---|
| B-1 | **Multidimensionality bans recur:** no Hand Size, Foot Size or big-feet scalar (MF, HV, DU, GR, GO, PK, CG); Arm Span (GR, GO); Shoulder Width concept (GR); Torso Size / Body Thickness / Torso Mass (GO); neck size (HV); Skin Color (DU, GR, GO, CG); weight slider (SK, SG); thin-to-heavy (MF); global scale size (SA); master race proportion sliders (PK "human → Pipkin", CG "Cogling Proportion", HV "Elf Percentage"/"Elf Gracility", GO ALPC, PK LSCTA, CG FSEA) |
| B-2 | **Frame scope differs by race but always skeletal.** Saurin and Grask/Gorrund state explicitly what frame never changes. Cogling makes robusticity/joints starting tendencies only (AC-9) |
| B-3 | **Stature-change behaviour is stated only as prohibitions** (no uniform scaling) plus allometry statements (GO L224; CG L883–893). No race gives segment or allometry numbers |
| B-4 | **Composition canon is consistent roster-wide.** Only Saurin adds a sex-related tissue system (E/B) that must stay outside fat |
| B-5 | **Coverage silences:** body hair (MF, SK, SG, FN, AE, VA, HV); natural body asymmetry (all but SA); neck controls (SG, FN, PK detail); Vael shoulder/pelvic width controls (omitted from VA L121 though frame changes them, VA L128) |
| B-6 | **Saved appearance is the largest canon/prototype gap** (prototype: frame, height step, two colours, finish) |
| B-7 | **The Manny/Quinn frame swap is a prototype placeholder** that conflates frame, body type and sex (level 6). Canon already rejects it (PR L29) |
| B-8 | **Tensions to carry, not resolve:** SA head share (§55) vs the +8 % centre (§258); PK trunk-share absorption (L137 vs L164); AE presentation-preset lists (L380 vs L431); SA §145 tail muscularity, superseded by §256.6 but unmarked; HV L156/L410 old height wording; DU 150/152 cm (UFCA-07 N-2); GR stale "tallest"; register "three skin layers" (L21) stale; plan age→movement-speed and "race plus slider values" record (level 6) conflict with canon |

— Claude
