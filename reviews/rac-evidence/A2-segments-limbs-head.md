<!-- RAC Phase 1 evidence extraction (agent-produced, line-checked at HEAD 218f64a). Not canon; supporting evidence for reviews/claude-rac-01…12. -->
# A2 — Segment & stature evidence: limbs, hands/feet, head-to-stature

Evidence extraction for the design audit. Read-only on the repo at HEAD `218f64a`. Every spec line number below was checked with `sed -n <n>p` / `grep -n` against the current file. Quotes are verbatim contiguous excerpts (at most 25 words; long lines are excerpted, never re-worded inside quote marks). Paraphrase sits outside the quotes.

Tag key: **[POS]** positive canon statement · **[OPEN]** canon marks it open · **[TEST]** a named validation case that constrains segments · **[BAN]** explicit prohibition · **[NUM]** a number canon already states · **[SILENT]** not addressed in the spec.

Abbreviations: MF Marchfolk, SK Skarn, SG Sagekin, FN Fenn, AE Aelari, VL Vael, HV Halvren, DU Durrim, GR Grask, GO Gorrund, PI Pipkin, CO Cogling, SA Saurin. HSR = head-to-stature ratio (r3 framework: "HH ÷ standing height; HL ÷ standing height").

---

## 0. Cross-cutting canon (UCCA and reviews)

- [POS] Stature is the only absolute size control — "**Stature is the only absolute size control.** It is DIR within the race's canonical envelope." (UCCA L108)
- [POS] Absolute head/hand/foot sizes are derived per race — "Head, hands, feet, joints and bone breadth never follow stature by one shared scale factor." (UCCA L110)
- [POS] Segment shares are DIR where canon names them; bands come later — "Segment shares and within-limb distributions | DIR where canon names them; bands from RM-UB-01" (UCCA L76)
- [POS] Head-to-stature is a validator, not a control, except Saurin — "Head-to-stature | **VAL / DIAG** for every race except Saurin, whose ±8 % head-to-body control is DIR (SAURIN §258)" (UCCA L77)
- [POS] Arm span is derived — "Arm span; visible mass; limb circumference ("thickness") | **DER**, never sliders" (UCCA L80)
- [BAN] "no Hand Size or Foot Size scalar; no Arm Span slider" (UCCA L92). Same line also bans master proportion sliders: "ALPC, LSCTA, FSEA or equivalent" (UCCA L92)
- [POS] REDISTRIBUTE has exactly one canon case — "the **only** canon case is **Saurin stature accounting**: head, neck, thorax, lower trunk and legs sum coherently to stature" (UCCA L103)
- [POS] Height distributes through shares inside bands — "stature changes distribute through segment shares inside race CLAMP bands. No race gains or loses identity by stretching one segment." (UCCA L112)
- [POS] Ranges are exactly the canon envelopes; distributions OPEN — "Population stature and proportion distributions are OPEN or SILENT for every race" (UCCA L113)
- [POS] Equal-height rule; DU–MF point 152 cm — "The **Durrim–Marchfolk equal-height comparison point is 152 cm** (T-6)." (UCCA L114)
- [BAN] "Anti-juvenile packages (Pipkin, Cogling) are banned." (UCCA L272)
- [TEST] "**No-uniform-scale test:** two statures of one character are never related by a single scale factor across head, hands, feet and joints." (UCCA L332)
- [OPEN] BIO OPEN list — "segment ratios and numeric proportions; arm span (Grask, Pipkin); joint/robusticity distributions; head-to-stature (all but Saurin)" (UCCA L355)
- [OPEN] RM-UB-01 "Per-race segment-share and within-limb distribution bands" (UCCA L349); RM-UB-02 "Per-race allometric response to stature" (UCCA L350)
- [NUM] Roster span: "first-pass playable stature spans approximately **76 cm (2'6") to 251 cm (8'3")**" (PIPKIN L119)
- Reference-mesh queue (r5): RM-LR-01 measures "Torso share (suprasternal → hip joint ÷ stature); leg share; arm length and arm span ÷ stature; forearm ÷ arm; lower leg ÷ leg" (r5 L27); RM-LR-04 = GR-BODY-10 vs Gorrund limb-present family (r5 L30); RM-SR-01 Pipkin trunk share (r5 L39); RM-SR-02 Cogling segment ratios (r5 L40); RM-SR-04 "Head ÷ stature; FVI; ORB vs aperture (anti-juvenile)" (r5 L42); RM-CF-10 "HSR | Grask, Gorrund, Pipkin, Cogling (all OPEN)" (r5 L59); RM-UB-01 bands list "(torso/axial, neck, arm, upper-arm/forearm, leg, femur/lower-leg, hand, palm/finger, foot)" and dependency "Pipkin trunk-share split (T-2)" (r5 L79); RM-OT-01 Sagekin vs Marchfolk (r5 L89); RM-OT-02 elf limb share (r5 L90); RM-OT-05 "Stature distributions and world-scale extremes (76–251 cm)" (r5 L93).
- HSR framework (r3): "HSR — head to stature | HH ÷ standing height; HL ÷ standing height | E | Saurin head length/H 0.156–0.184 (§258); OPEN for Grask, Gorrund, Pipkin and Cogling" (r3 L78). Note: r3 lists only four OPEN races; Durrim also has a stated head-contribution tendency (DURRIM L21) that is not listed there.

---

## 1. Marchfolk (Human Reference Population)

- [NUM] Height envelope: "About 147 cm (4'10") | About 173 cm (5'8") | About 203 cm (6'8")" (MARCHFOLK L21); repeated "147 cm | 173 cm | 203 cm" (L64); reference-height term: "about 173 cm (5'8") is the Marchfolk **Reference Height**" (L286)
- [POS] Height is not uniform scale — "It isn't produced by uniformly scaling the whole character, and height should come from anatomically appropriate proportional relationships." (L23)
- [POS] Marchfolk are the comparison anchor for limbs, hands and feet — "the grounded reference for judging how another race differs in skeletal proportions, craniofacial anatomy, joints, limbs, hands and feet" (L15)
- [POS] Relationship-aware constraints name the segment pairs — "upper arm and forearm, femur and lower leg, hand and wrist, foot and ankle, neck and shoulders, and head and body" (L31)
- [POS] Control list names leg length, torso length, hand size, foot size — "Leg length, thigh thickness, calf thickness, foot size" (L76); "arm thickness, hand size" (L74); "Torso and leg length:** plausible overall proportions." (L88)
- [POS] Hand/foot multidimensionality (universal amendment §4) — "These distinguish absolute dimensions (measured size) from proportional dimensions (relative to height, limb length or neighboring anatomy)" (L284); "One generic size scalar isn't a sufficient biological definition, and exact controls are future work" (L284)
- [TEST] Permanent height characters — "About 147, 173 and 203 cm, each tested with several frame and composition combinations, never only the reference height" (L249)
- [TEST] Proportion stress — "Minimum and maximum limb relationships, torso, shoulders, pelvis and hips, neck, hand and foot scale and proportion" (L251)
- [BAN] No privileged ideal body — "not one idealized fantasy-human body" (L13)
- [SILENT] No arm-length control is listed (controls name "arm thickness, hand size", L74, but no arm length). No upper-arm/forearm or femur/lower-leg tendency, no leg-share value, no arm span, no head-to-stature statement, no anti-juvenile body rule (adult read is implicit). As the reference population, every relative comparison elsewhere depends on Marchfolk numbers that do not exist yet (no RM item measures a Marchfolk segment baseline on its own; it rides along in RM-LR-01/05 and RM-OT-01).

## 2. Skarn

- [NUM] "183 cm (6'0") | 208 cm (about 6'10") | 229 cm (7'6")" (SKARN L13); overlap with Marchfolk "(up to 203 cm) is intentional" (L15)
- [POS] Slightly larger torso share than MF — "a slightly larger torso share of total height and greater torso depth" (L75)
- [POS] Torso-dominant tendency but long legs possible — "The Skarn central tendency is slightly more torso-dominant than Marchfolk, but Skarn aren't universally short-legged. Long-legged and long-torso Skarn are both possible." (L86)
- [POS] Larger hands and feet — "larger hands and feet" (L25, L79); scale carriers — "Hands, feet, joints and torso carry much of the Skarn sense of scale." (L40)
- [POS] Height distributes across head/torso/limbs — "Height changes keep believable relationships between the head, torso, pelvis, arms, legs, hands, feet and joint positions." (L40)
- [POS] Head-to-body set by body scale (pending) — "body scale sets head-to-body proportion. Players keep independent facial control. This is pending validation." (L179); skull "slightly larger, more robust skull suited to body size" (L147)
- [POS] Hand/foot detail controls — "hand size and breadth, finger proportions, foot length and breadth. All stay anatomically constrained" (L98)
- [BAN] "There is no default "huge upper body, tiny legs" silhouette." (L94)
- [TEST] Equal-height MF test — "Compare a 190 cm Marchfolk with a 190 cm Skarn" (L292); SK-03 "Maximum height, 229 cm" (L329); SK-04 "Narrow, lean, long-legged" (L330); validation character "**Short Skarn:** 183 cm, Narrow, low muscle." (L126); "**Maximum Skarn:** 229 cm at the supported extremes." (L133)
- [OPEN] Reach — "Collision, reach and gameplay size (unresolved)" (L348)
- Clarification elsewhere: Halvren reconciles "larger hands/feet" as "Greater average absolute skeletal hand and foot dimensions, with proportional relationships also following Skarn anatomy" (HALVREN L454)
- [SILENT] Arm length relative to height, arm span, upper-arm/forearm, femur/lower-leg, finger:palm, numeric head-to-stature. r2 marks Skarn arm/span, leg and forearm emphasis "n.s." (r2 L58–60).

## 3. Sagekin

- [NUM] "152 cm (5'0") | 178 cm (5'10") | 208 cm (about 6'10")" (SAGEKIN L72); tests "SG-02 | Minimum height, 152 cm" / "SG-03 | Maximum height, 208 cm" (L187–188, L419–420)
- [POS] v1.1 tendencies vs MF (current authority) — "a slightly greater leg share of height" (L137); "slightly longer forearms, hands and fingers" (L138); "a slightly shorter torso relative to stature" (L139)
- [POS] v1.0 wording kept as history, clarified by AC-6 — "hands and feet remain human anatomy while the population may trend toward longer forearms, hands and fingers" (L89); v1.0 bullets: "slightly longer limbs relative to torso" (L81), "normal human hands and feet" (L84)
- [POS] Arms/hands region — "Somewhat longer fingers and slightly narrower hands, subtle and human" (L156); legs — "Somewhat greater leg share of height. Feet stay structurally believable" (L157)
- [POS] Segment variables named — "arm length, forearm proportion, leg length, thigh-to-lower-leg relationship, torso length, and hand and foot size" (L97)
- [POS] Shorter-limbed Sagekin valid — "shorter-limbed and longer-torso Sagekin stay supported" (L97)
- [BAN] Elven boundary — "never reproduces Fenn or Aelari central-tendency anatomy" (L147); "Pointed ears, exaggerated limbs, very light bones and other elven traits are never used to set Sagekin apart." (L147); "never elven in limb proportion" (L435)
- [BAN] No "soft hands" biology — "Intelligence, education, weakness, frailty, "soft hands" and scholarly occupation are never encoded in anatomy." (L17)
- [TEST] SG-04 "Long-limbed, near the proportional boundary" (L189; L421 "near the boundary"); cross-race "Sagekin stay human in skeletal organization and proportional limits." (L199)
- [SILENT] Upper-arm vs forearm direction beyond "longer forearms"; femur/lower-leg direction (variable named at L97/L157 but no tendency); arm span; head-to-stature; numeric magnitudes of "slightly".

## 4. Fenn

- [NUM] "157 cm (about 5'2") | 181 cm (about 5'11") | 211 cm (about 6'11")" (FENN L24); FN-01 "Reference: 181 cm, Balanced" (L84)
- [POS] Skeleton — "longer limbs relative to the torso" (L34); "longer hands and fingers" (L35); "longer, somewhat narrower feet" (L36)
- [POS] Torso share smaller — "Slightly smaller torso share of height, somewhat less ribcage depth, more compact chest, longer waist transition" (L50)
- [POS] Arms v1.0 — "Longer arms relative to torso, slightly longer forearms, longer hands and fingers, narrower wrists" (L51); v1.1 — "Longer arms, somewhat greater forearm share" (L121)
- [POS] Legs v1.0 — "Greater leg share of height, slightly longer lower legs, narrower ankles, somewhat longer feet than same-height humans" (L52); v1.1 — "Greater leg share, slightly greater lower-leg share" (L123)
- [POS] Hands — "Longer palms and fingers, somewhat narrower hands and wrists" (L122); "No per-finger length controls yet" (L122)
- [POS] Feet — "Somewhat longer and narrower, with normal humanoid toes" (L124)
- [POS] Pelvis supports long femurs — "A distinct elven pelvis, not a scaled human one, supporting longer femurs" (L111)
- [POS] Joints small relative to limb length — "Wrists, elbows, knees and ankles look smaller relative to limb length than on same-height humans, with minimum anatomical boundaries." (L115)
- [POS] Combined extreme — "maximum arm length, forearm proportion, hand length and finger length together may exceed the supported range" (L134)
- [POS] Sagekin boundary — "Sagekin are the long-limbed end of fully human variation, and Fenn have a genuinely different elven skeleton." (L138)
- [TEST] FN-09 "Short-limbed, near the racial boundary" (L92); FN-15 "Maximum supported arm and hand combination" (L150); FN-16 "Maximum supported leg and foot combination" (L151); FN-17 Sagekin/Fenn proportional boundary (L152); equal-height test "Fenn must still stand out through limb proportions, joint scale, hands, feet" (L78)
- [BAN] "No prehensile, gripping or animal-like feet" (L124); "never just from longer human sliders" (L138)
- [OPEN] "Collision and reach (unresolved)" (L497)
- [SILENT] Arm span; numeric leg share; head-to-stature (only forehead-cranium contour, L162).

## 5. Aelari

- [NUM] "168 cm (about 5'6") | 190 cm (about 6'3") | 221 cm (about 7'3")" (AELARI L27); AE-03 "Maximum height, 221 cm" (L87)
- [POS] Whole-body elongation incl. cranium — "whole-body vertical elongation, distributed coherently through the cranium, neck, torso, arms and legs" (L33)
- [POS] Arms: even split — "Longer than humans, with elongation spread evenly across upper arm and forearm" (L56); "Fairly even elongation across upper arm and forearm" (L152)
- [POS] Fenn contrast on forearm, provisional — "Fenn may lean more on forearm length. Not final until comparative validation" (L56)
- [POS] Legs: even thigh/lower leg — "Distinctly long-legged while keeping the longer torso, with even elongation through thigh and lower leg (not lower leg alone)" (L58); "Elongation spread evenly, not one extremely long segment" (L154)
- [POS] Hands — "longer hands, palms and fingers, relatively narrow breadth, gracile wrists" (L153); feet — "Humanoid, somewhat longer, moderate to narrow breadth, gracile ankle" (L155)
- [POS] Longer torso than Fenn — "Longer overall torso and waist transition than Fenn." (L124)
- [POS] Risk case — "Extreme neck, torso, arm, hand, leg and foot length together is the Aelari risk case." (L163)
- [TEST] Equal-height Fenn at ~190 cm — "Aelari more vertically continuous, with a longer torso and neck and evenly spread limb elongation" (L169); AE-19 "Maximum supported hand proportions" (L185); AE-20 "Maximum supported leg and foot combination" (L186); AE-11 "Long-torso stress test" (L95); AE-12 "Valid extreme proportional test" (L96)
- [BAN] "never a uniformly scaled human or Fenn with stretched legs" (L33); "Aelari never read as the tallest end of human customization" (L170); "with no independent segment stretching" (L152)
- [OPEN] "Exact Fenn and Aelari differences provisional" (L155); reach OPEN (L582)
- [SILENT] Arm span; head-to-stature (cranium elongation is named, L33, but no head-share direction); numeric leg share.

## 6. Vael

- [NUM] "157 cm (about 5'2") | 178 cm (about 5'10") | 203 cm (about 6'8")" (VAEL L17)
- [POS] Torso share greater than Fenn — "Greater torso share than Fenn, deeper ribcage than Fenn or Aelari" (L35)
- [POS] Arms — "Long relative to humans, less extreme elongation than Fenn or Aelari, balanced upper arm and forearm, a somewhat sturdier wrist transition" (L44); v1.1 "Somewhat less relative elongation than Fenn or Aelari, still elven" (L138)
- [POS] Legs — "somewhat smaller leg share of height than Fenn or Aelari, balanced femur and lower leg, more knee and ankle presence" (L46); v1.1 "Long next to humans, somewhat smaller leg share than Fenn or Aelari" (L140)
- [POS] Hands — "moderately long fingers, somewhat broader palms than Fenn or Aelari, a sturdier wrist and hand base" (L45); "broader palm than Fenn or Aelari, stronger wrist-to-hand transition. Never shortened human hands" (L139)
- [POS] Feet — "Moderate elongation, broader than Fenn or Aelari, stronger ankle-to-foot transition" (L141)
- [BAN] "Never made by shortening Fenn arms with a slider" (L44); "Compactness never comes from just shortening legs" (L140); "No prehensile or gripping adaptations" (L141)
- [POS] Combined risks — "short torso with long legs, long torso with shorter valid limbs, large hands with narrow wrists" (L155)
- [TEST] VL-10 "Compact-proportioned" (L89); VL-15 "Valid extreme proportional test" (L94); three-elf matrix "Vael | Deeper torso, more compact torso-to-limb continuity, more joint presence ... moderate elongation, lower center of mass than Aelari" (L165, excerpted); VL-16 must show "limb segmentation, hands and feet" (L149)
- [SILENT] Arm span; head-to-stature; numbers.

## 7. Halvren

- [NUM] "About 152 cm (5'0") | About 178 cm (5'10") | About 213 cm (7'0")" (HALVREN L88); central envelope, not hard bound — "provisional height range is **152–213 cm (5'0"–7'0")** with reference **about 178 cm (5'10")**" (L156); "ancestry-dependent tails outside it, limits OPEN" (L410)
- [NUM] Source table — "Marchfolk | 147–203 cm | About 173 cm" (L94) … "Vael | 157–203 cm | About 178 cm" (L99)
- [POS] Height not a midpoint — "Height is never an average of parental or reference heights." (L101)
- [POS] Limb inheritance per segment — "Arms and legs may express ancestry through total limb contribution to height, upper-arm, forearm, femur and lower-leg contribution" (L126); "Segments needn't share one ancestry strength, but coupling keeps transitions coherent." (L126)
- [POS] Arm examples — "Human-like total arm length with a greater Fenn-like forearm share" (L130); leg examples — "Human-like femur relationship with a greater Fenn-like lower-leg share" (L131)
- [POS] Source-trait summaries: Fenn "greater forearm share of arm length, greater lower-leg share of leg length, longer and narrower hands and feet" (L112); Aelari "evenly elongated limb segments, long hands and fingers, elongated feet" (L113); Vael "moderate limb elongation, stronger wrist-hand and ankle-foot transitions, somewhat broader hands and feet" (L114); Sagekin "somewhat longer-limbed human proportions" (L116)
- [POS] Hands/feet multidimensional — "Hands vary in absolute length, length relative to forearm and body, palm breadth and length" (L133); "never one "foot size" scalar" (L133)
- [TEST] HV-11 "About 152 cm, validating proportions, face, hands and feet, equipment and world, never uniform scaling" (L369); HV-12 "About 213 cm" (L370); HV-49/HV-50 tail cases (L487–488)
- [OPEN] "torso, limb, pelvic, hand and foot, craniofacial ... inheritance" (L74, excerpted list); edge-effect issue: "The spec doesn't say whether ancestry-shifted distributions are truncated at the envelope edge or compressed within it" (L436)
- [BAN] "It fails if a highly gracile long bone connects through an implausibly massive joint" (L133)
- [SILENT] Head-to-stature; arm span; numeric inheritance.

## 8. Durrim

- [NUM] "About 122 cm (4'0") | About 137 cm (4'6") | About 152 cm (5'0")" (DURRIM L17); summary "provisional height **122–152 cm (4'0"–5'0")** with reference **about 137 cm (4'6")**" (L85)
- [NUM] Equal-height MF point — "A Durrim and a Marchfolk at **152 cm** (the corrected comparison point, T-6, UCCA Phase 2" (L72); tests "About 122, 137 and 152 cm, never by uniform scale" (L75)
- [POS] Lower limb contribution — "**lower average limb contribution to total height than equivalently tall Marchfolk**, especially the legs" (L38)
- [POS] Arms — "Arms trend shorter in absolute length and in contribution to height than Marchfolk, while possibly staying substantial relative to the compact torso" (L38); "Upper-arm and forearm lengths vary independently within relationship-aware limits, with no fixed arm ratio." (L113)
- [POS] Legs — "Legs are proportionally shorter relative to stature than equivalent-height Marchfolk, through coordinated pelvis, femur, knee, lower leg, ankle and foot relationships" (L119); "femur and lower leg needn't shorten by identical percentages" (L119)
- [POS] Greater torso contribution — "Durrim have a greater torso contribution to height than equivalently tall Marchfolk, which doesn't mean an absolutely long torso" (L97)
- [POS] Hands — "trending toward a greater hand size relative to stature than Marchfolk" (L115); "A greater palm share of total hand length is a **provisional population tendency**, but fingers aren't universally short" (L115)
- [POS] Feet — "relatively large dimensions for stature, substantial skeletal breadth" (L121); "moderate relative length with high breadth ... are all valid" (L121, excerpted)
- [POS] Three-level measurement rule — "**absolute dimension**, **dimension relative to total height** and **dimension relative to adjacent anatomy**" (L93)
- [POS] Head — "Durrim may have a somewhat greater head-to-total-height contribution than the Marchfolk Human Reference Population ... but never an oversized fantasy-dwarf head" (L21, excerpted across the dash — see full line)
- [BAN] Anti-juvenile — "**Adults read unmistakably as adults**, with no childlike head-body or facial proportions" (L21); "never made by uniformly scaling a Marchfolk down, shortening only the legs, enlarging only the torso or head" (L11)
- [BAN] Combined invalid — "a very short femur with maximum lower-leg length" (L139)
- [TEST] "Limb proportions | Shorter-limbed, central and longer-limbed Durrim, with the longer-limbed one still Durrim rather than a short Marchfolk" (L501); Cross-Population Equal-Height test at ~152 cm (L145, L502); "Adult read" test (L76)
- [OPEN] Gameplay reach — "never solved by stretching arms. Gameplay reach is OPEN" (L150)
- **Wording hazard (audit note):** L93 reads "Durrim trend toward greater torso and lower leg and overall limb contribution to total height". Read with "lower" as an adjective it matches L38/L119 (lower leg and limb contribution). Read with "lower leg" as the anatomical segment it would say the lower leg contributes *more*, which contradicts L119 ("The lower leg trends the same way"). Suggest disambiguation; no anatomy change implied.
- [SILENT] Numeric head-to-stature (not listed in r3 HSR OPEN row); arm span (only implied by shorter arms); numeric ratios.

## 9. Grask

- [NUM] "about 198 cm (6'6") | about 218 cm (7'2") | about 239 cm (7'10")" (GRASK L17); GR-BODY-01 "Reference: about 218 cm" (L122); Gorrund now exceeds: "Gorrund, provisional maximum about 251 cm, exceeds them; T-7, UCCA Phase 2" (L178)
- [POS] Lower torso, greater leg, arm and span vs MF and SK — "Grask trend toward lower torso contribution to standing height, greater lower-limb contribution, greater upper-limb length relative to height and greater arm span relative to height" (L198)
- [POS] Legs — "trending toward greater leg length relative to height than Marchfolk and Skarn, never defined by one Leg Length slider" (L213)
- [POS] Lower leg (approved first-pass tendency) — "**Grask lower-leg length is an important contributor to their rangy silhouette and may be proportionally emphasized relative to human reference anatomy.**" (L215)
- [POS] Femur/lower-leg distribution — "valid individuals may lean femur-dominant, balanced or lower-leg-dominant around a coherent distribution" (L217)
- [POS] **Arm span (OPEN number, locked direction)** — "**Grask trend toward greater arm span relative to standing height than Marchfolk and Skarn reference anatomy.** Exact ratios stay OPEN pending prototype measurement and comparative validation." (L223); Part 1: "Generally substantial relative to stature, with no fixed arm-span-to-height ratio yet" (L60); strengthened: "exact ratios **OPEN pending prototype validation** and no invented numbers" (L166)
- [POS] Arm span is emergent — "Arm span emerges from shoulder architecture, upper-arm, forearm and hand length, never one Arm Span slider." (L225)
- [POS] Reach not by torso shortening — "reach identity can't be produced just by shortening the torso" (L166)
- [POS] Upper arm — "**Grask upper arms trend toward greater absolute length and greater length relative to total standing height than Marchfolk and Skarn reference anatomy.**" (L310)
- [POS] Forearm — "**Forearm length is a meaningful contributor to Grask racial anatomy and trends toward increased proportional contribution compared with Marchfolk and Skarn reference anatomy**" (L227); "never requires every Grask to have forearms longer than upper arms" (L314)
- [POS] Hands — "Grask trend toward somewhat greater finger length relative to palm dimensions than Marchfolk and Skarn reference anatomy" (L235); "Grask reach never depends mainly on enormous hands" (L229)
- [POS] Feet — "Foot length suffices for support and locomotion but never scales linearly with height" (L245)
- [POS] Head — "No head-to-height ratio is locked, but a comically small, oversized or uniformly scaled human head is avoided" (L433)
- [BAN] "hands hanging near the knees is **not** a mandatory population trait" (L57); "Leg elongation fails if it creates stilt-like anatomy, an extremely high crotch, a tiny-looking torso" (L217); "never reaching ape caricature" (L229)
- [BAN] Adult read — "no default adolescent gangliness, childlike head-body relationships or infantilized soft-feature variants" (L716)
- [BAN] Combined — "maximum arm length, forearm emphasis and finger length" (L255)
- [TEST] GR-BODY-10 "Shorter-limbed valid extreme" (L131); GR-BODY-11 "Longer-limbed valid extreme" (L132); GR-BODY-12 "Forearm-emphasis valid extreme" (L290); GR-BODY-13 "Upper-arm-emphasis valid extreme" (L291); GR-BODY-14 "Long-hand valid extreme" (L292)
- [TEST] **GR-BODY-10 floor (AD-3)** — "GR-BODY-10 (shorter-limbed extreme) keeps enough limb contribution to read Grask — at matched height it must still trend above the Gorrund limb-present proportion family" (L259, excerpted); test row: "GR-BODY-10 still trends above the Gorrund limb-present family in relative limb contribution." (L715); "Numeric validator deferred (RM-LR-04)" (L715)
- [TEST] GR-BODY-10 vs Skarn (AD-2) carriers — "thoracic and shoulder breadth relative to stature, non-human girdle and pelvic organization, neck relationship, hand and digit relationships" (L714)
- [OPEN] "numerical body proportion ranges and ratios; arm-span distribution" (L726)
- [SILENT] Numeric HSR (r3/r5 RM-CF-10 OPEN).

## 10. Gorrund

- [NUM] "about 208 cm (6'10") | about 229 cm (7'6") | about 251 cm (8'3")" (GORRUND L29); "superseding Grask's 239 cm only as the **current world-validation upper stature**, never a permanent maximum" (L31)
- [POS] Greater torso share than Grask — "**Gorrund generally possess a greater proportional torso contribution to total standing height than Grask at matched height, while retaining fully adult, functional limb lengths.**" (L169)
- [POS] Legs — "**Gorrund lower limbs generally contribute less proportionally to standing height than Grask lower limbs at equal height**, never meaning short-legged" (L196)
- [POS] Femur/lower-leg — "The femur-to-lower-leg relationship varies (slight femur emphasis, balanced, slight lower-leg emphasis) without extreme mismatches for variety, with ratios **OPEN**." (L196)
- [POS] Arms/span vs Grask — "**Grask should generally exhibit greater arm length and arm-span contribution relative to total stature than Gorrund.**" (L200); "Arm span stays appropriate to the anatomy, neither extremely short nor Grask-extended (distribution **OPEN**)" (L202)
- [POS] Absolute vs proportional arms — "increased arm length or reach relative to total standing height is NOT currently a defining Gorrund trait." (L277); "Gorrund aren't currently defined by unusually increased arm length relative to height." (L279)
- [BAN] "**Do NOT use "long-armed" as shorthand for Gorrund racial anatomy.**" (L281)
- [POS] Forearm — "never one of the strongest identifiers, with moderate upper-arm-to-forearm variation and no extremely short or Grask-like forearms (ratios **OPEN**)" (L202)
- [POS] **"Slightly more limb-present" family (AD-3)** — "Presets may use internal proportion families (more axial, more balanced, slightly more limb-present; at matched height the limb-present family stays below the shortest-limbed valid Grask" (L232, excerpted)
- [TEST] **AD-3 reciprocal** — "Lower-breadth / lower-depth Gorrund (GOR-BODY-12, GOR-BODY-14) vs Broad Grask at matched height" must hold through "lower relative limb contribution than the Grask distribution, greater axial contribution, joint presence and Axial Load-Path Continuity" (L244); "Numeric validator deferred to approved reference meshes (RM-LR-04)" (L244)
- [POS] **ALPC** — "the shoulder girdle, thoracic structure, lower axial trunk, pelvis and proximal lower limbs form a strongly integrated vertical load-bearing chain" (L711); "project anatomical terminology, not a creator-facing slider" (L713); Narrow keeps it — "reduced breadth never removes thoracic depth, joint scale, pelvic and proximal-limb integration or structural continuity" (L721)
- [POS] Durrim contrast on limbs — "Not shorter: limbs stay fully substantial contributors to a tall adult body, while less reach-dominant than Grask" (L732)
- [POS] Hands — "**Gorrund palms possess substantial breadth and depth relative to their overall hand length**" (L210); feet — "foot length is never exaggerated to signal size" (L216)
- [POS] Head — "Suited to the very large body, avoiding the tiny-head giant, the oversized fantasy-ogre head and a uniformly scaled human head; head-to-height ratio **OPEN**" (L299)
- [TEST] Head failure at max/min — "The head stops being adult, credible and clearly Gorrund (tiny-head giant syndrome)" (L408); max-height failure "It needs uniform scaling, extreme limb elongation, a tiny head or monster posture" (L151)
- [BAN] Adult read — "narrower, softer or lower-height Gorrund are never infantilized" (L690)
- [OPEN] "torso-to-limb proportions; ... femur-to-lower-leg and upper-arm-to-forearm relationships; hand and foot architecture" (L159)
- [SILENT] Gorrund vs Skarn (and vs MF) leg/arm/span direction — r2 records "**GO vs S n.d.**" for arm/span, leg, forearm/lower-leg (r2 L58–60).
- Line drift note: r2 and r5 cite the family as "GO L230" (r2 L97, r5 L30); it is now GORRUND L232.

## 11. Pipkin

- [NUM] "about 91 cm (3'0") | about 107 cm (3'6") | about 122 cm (4'0")" (PIPKIN L27); Durrim boundary "near **122 cm (4'0")**" (L29); Cogling overlap "approximately **91–107 cm**" (L94)
- [NUM] Prototype (non-authoritative) — "approximately 0.7× Marchfolk scale (~121 cm)" (L1621)
- [POS] Preserved limbs — "**Limb contribution remains comparatively preserved despite short stature.**" (L54); "Preserved doesn't mean unusually long limbs; arms and legs just aren't reduced as far as Durrim's compact system." (L56)
- [POS] **Trunk-share absorption (~L137)** — "Pipkin trend toward a **modestly reduced vertical central-trunk contribution to total stature**" (L137); "The reduced trunk share is absorbed primarily through **sustained limb contribution and pelvic vertical contribution, not through enlargement of the head**." (L137); "This never requires unusually long legs and never creates Durrim-like compression." (L137)
- [POS] **T-2 reconciliation (L139)** — "the absorption of the reduced trunk share is relationship-aware stature/proportion behaviour, never permission for global scaling or juvenile proportions." (L139); "The numeric split between limb and pelvic contribution stays deferred (UCCA RM-UB-01; short-race RM-SR items); no winner is invented." (L139). Ruling source: "If the two passages prescribe genuinely incompatible numeric behavior, keep the numeric relation deferred rather than inventing a winner." (chatgpt-ucca-phase2-canonicalization-order L99)
- [POS] **Leg rule (~L164 section, text L166)** — "Legs contribute more to standing height than Durrim legs at matched height but never automatically exceed ordinary human adult proportions (Marchfolk relationship subject to validation)" (L166); "Pipkin aren't defined by unusually long legs" (L166)
- [POS] Femur/lower leg — "femur-to-lower-leg balance **OPEN**), with slight femur emphasis, balanced segmentation or slight lower-leg emphasis valid" (L166)
- [POS] **Arm span (OPEN distribution, negative tendency stated)** — "moderate upper-arm and forearm variation and no Grask-like forearm emphasis; unusual arm span isn't a Pipkin trait (distribution **OPEN**)" (L166)
- [POS] Arms vs Durrim — "possibly with greater proportional contribution than Durrim at matched height (ratio **OPEN**)" (L56)
- [POS] Hands — "**Pipkin hands are relatively moderate in size for their stature**" (L58); "moderate structural scale relative to stature, neither Durrim-substantial nor childishly small" (L172)
- [POS] Feet — "Modestly increased foot contribution relative to stature is a population tendency" (L64); "Feet may trend somewhat larger relative to height than Marchfolk as a **population tendency**, not a requirement" (L178); "**feet aren't the primary identifier**" (L178)
- [POS] Head — "Pipkin may have somewhat greater head contribution to standing height than the Marchfolk Human Reference Population as a natural consequence of short adult architecture" (L33); "but never an oversized "cute halfling head" (ratio **OPEN**)" (L33); "**Pipkin may possess somewhat greater head contribution relative to total stature within an adult proportional system, but an oversized head is NOT a defining racial trait.**" (L205)
- [BAN] "**Greater relative head contribution is NOT a Pipkin maturity signal and must never be used to distinguish an adult Pipkin from a human child.**" (L201); "Short stature never justifies juvenile proportions: no oversized cranium, huge eyes, tiny jaw, extremely short face, childlike shoulders or pelvis, infant-like limbs" (L33)
- [TEST] PIP-BODY-02 "Minimum height, about 91 cm; stays adult (critical anti-child test)" (L103); PIP-BODY-10 "Greater valid limb contribution, never miniature Grask or Fenn" (L111); PIP-BODY-11 "Lower valid limb contribution, never Durrim" (L112); PIP-BODY-12/13 larger/smaller feet (L113–114); PIP-BODY-15 "Adult Pipkin vs human child at matched height" (L116); PIP-BODY-17 "Reference with head, hands and feet obscured; body still reads Pipkin through trunk, pelvis and limbs" (L213); PIP-BODY-24/25 limb contribution extremes (L220–221); PIP-BODY-26/27 foot–hand decoupling (L222–223); PIP-STRESS-08 "Greater foot contribution with lower valid ankles" (L236); anti-child test "Greater head contribution to stature + youngest adult apparent age" (L457); PIP-FACE-17 "Adult Pipkin vs human child at similar head size" (L440)
- [OPEN] Consolidated §32 — "final head-to-body ratio envelope" (L1534); "femur-to-lower-leg balance" (L1538); "upper-arm-to-forearm balance and total arm-span distribution" (L1539); "detailed hand proportions" (L1540); also "final Pipkin height range; the current ~91–122 cm range remains provisional" (L1533)
- **Audit note on absorption:** L137 (trunk share reduced; absorbed by limbs + pelvic vertical, "not through enlargement of the head") and L166 (legs never automatically exceed ordinary human adult proportions) jointly leave the pelvic vertical contribution and arms-free-of-stature as the main sink, while L33/L205 still allow "somewhat greater head contribution". These are compatible only as "allometric head share is allowed; deliberate head enlargement may not pay for the trunk deficit". T-2 parks the numeric split at RM-UB-01 / RM-SR-01. Also note UCCA L103 says Saurin stature accounting is the **only** canon REDISTRIBUTE; Pipkin absorption is therefore handled as a CLAMP-band relationship (T-2 wording "relationship-aware stature/proportion behaviour"), not as a REDISTRIBUTE tool.

## 12. Cogling

- [NUM] "**Minimum:** ~76 cm / 2'6"" (COGLING L53); "**Reference:** ~91 cm / 3'0"" (L54); "**Maximum:** ~107 cm / 3'6"" (L55); overlap "approximately 91–107 cm with Pipkin" (L63)
- [NUM] Head size — "face and expression readability at an adult-valid head size of roughly 11–13 cm" (L522; repeated L1583, L3172 "approximately 11–13 cm"). The dimension (height vs length) is not specified.
- [NUM] Prototype (non-authoritative) — "approximately **0.72× Marchfolk scale (~125 cm)**" (L445)
- [POS] Near-human total limbs — "At normalized displayed height, Cogling total arm and leg contribution remains broadly within the Marchfolk adult envelope." (L558); "Cogling are not defined by greater total limb share." (L560)
- [POS] Torso near MF — "total torso contribution remains broadly near the Marchfolk adult range rather than becoming strongly limb-dominant" (L100)
- [POS] **Distal redistribution** — "relatively greater forearm contribution within total arm length" (L139); "relatively greater lower-leg contribution within total leg length" (L140); "hands that occupy a larger proportional share of arm length than in normalized Marchfolk" (L141); "fingers that are proportionally long relative to palm length" (L142); "The corresponding proximal segments accommodate that redistribution so the race does not become globally limb-dominant." (L145)
- [POS] **Arm-segment (§39)** — "somewhat reduced proximal upper-arm share" (L572); "somewhat increased forearm share" (L573); "increased hand share" (L574); "increased finger contribution within the hand" (L575)
- [POS] **Finger/hand internal distribution (§40–41)** — "proportionally increased finger length relative to palm" (L593); "Palm width, palm length, finger length and finger segment proportions must not collapse into one control." (L599); variation list "proximal/middle/distal phalanx contribution" (L607); UCCA places it in Slot 4: "**Cogling:** finger internal distribution" (UCCA L33)
- [POS] **Leg-segment (§42)** — "somewhat reduced femoral share" (L620); "somewhat increased lower-leg share" (L621); "This is within-limb redistribution, not longer legs overall." (L624); "total leg contribution to stature remains broadly near the Marchfolk adult range" (L203)
- [POS] Feet — "Cogling feet remain moderate adult humanoid feet." (L630); "They are not required to be unusually small or large relative to stature." (L632)
- [POS] Head — "A Cogling head may occupy a somewhat greater fraction of total stature than the Marchfolk Human Reference Population ... simply because of allometric scaling" (L280, excerpted); "**racial identity cannot depend on deliberate head enlargement**" (L280); "Head-to-body ratio must remain within an adult-valid Cogling envelope and survive direct comparison with a human child." (L282)
- [POS] Allometry, not uniform — "Height changes must not automatically change: - head size by identical percentage; - hand/finger emphasis by identical percentage" (L887–889)
- [BAN] Juvenile — "infant/toddler head share;" "bobble-head silhouette;" "oversized cranium as racial shorthand." (L732–734); "Very small stature is not juvenile anatomy." (L94); "Head size cannot be used as the main mechanism that makes Cogling look small." (L274)
- [BAN] Arm system — "extremely short humeri;" "ape-like reach;" "dangling hands;" "spider fingers;" (L580–583); "**not** permission for extreme spider-like limbs, giant hands, giant feet or implausibly thin bones" (L147)
- [BAN] Combined invalid — "minimum height + maximum head share + minimum shoulder/pelvic maturity producing a toddler read;" (L1051); "maximum forearm + maximum hand + maximum finger contribution without compensating proximal segments;" (L1052)
- [TEST] COG-BODY-11 "Minimum-height Cogling (~76 cm) beside a roughly 1–2-year-old similar-height human toddler" (L465); COG-BODY-12 long-finger high end (L466); COG-BODY-16 vs Fenn "near-human total limb share with within-limb distal redistribution rather than Fenn greater limb share" (L470); COG-BODY-19 "Maximum forearm redistribution with total arm share held near-human; no Grask reach read" (L1064); COG-BODY-20 "Maximum lower-leg redistribution with total leg share held near-human; no Fenn/global limb dominance" (L1065); COG-BODY-21 max finger emphasis (L1066); COG-BODY-09A/27 Pipkin overlap at ~107 / ~91 cm (L462, L1072)
- [OPEN] Historical Part 1 list includes "arm span/reach distribution;" (L514) and "head-to-body ratio;" (L512). Consolidated §207 governs: "exact body segment ratios;" (L3161), "hand, palm and finger proportions;" (L3165), "foot proportions and arch distribution;" (L3166), "exact head allometry;" (L3170). §51: "Exact head-to-body ratios remain OPEN pending facial design and camera validation." (L736). Part 2 list: "exact upper-arm/forearm and femur/lower-leg distributions;" (L1089)
- Audit note: arm span appears only in the historical Part 1 OPEN list (L514), not in §207, and UCCA L355 lists arm span OPEN for "(Grask, Pipkin)" only. For Cogling it is implicitly covered by "exact body segment ratios" and by UCCA DER (L80); total arm length is directionally near-Marchfolk (L558), but shoulder breadth is a narrow core (L100), so span direction is not derivable from canon text alone.

## 13. Saurin

- [NUM] "~168 cm / 5'6" | ~188 cm / 6'2" | ~208 cm / 6'10"" measured "**excluding tail length**" (SAURIN L64–68); restated L3584–3586; "Stature 168–208 cm remains the racial hard bound (§4) and is **independent**." (L4166)
- [NUM] **§258 creator bounds** — "head-to-body proportion ±8 % (head length 0.156–0.184 of standing height; the +8 % head-scale decision is the centre)" (L4166); same line: "arm length ±6 %; leg length ±6 %; hand size ±8 %; foot size ±8 %" and "axial trunk length ±10 %" and "neck length ±15 %"
- [NUM] Reference accounting — "equal stature 187.9 cm" … "Head length/H (0.170) and tail length (frozen reference, §256) unchanged" (L4236, excerpted). Arithmetic check (not new canon): 0.170 × 0.92 = 0.1564 and 0.170 × 1.08 = 0.1836, consistent with 0.156–0.184.
- [NUM] Tail (not part of stature) — "approximately **55–80% of standing height**" (L174); frozen reference "tail 121.4 cm along the relaxed centreline, 64.6 % of standing height" (L4145)
- [POS] **Part 1 stature-accounting note** — "The elongated lower axial trunk and moderate-to-long leg contribution cannot both expand without compensating elsewhere in total standing height." (L607)
- [POS] **§55 stature-share accounting (L956 section; text L970)** — "Saurin head-height share trends **near to modestly below the Marchfolk adult range**, while neck-height share remains broadly near Marchfolk." (L970); "paid for primarily through modestly reduced vertical head/thoracic contribution rather than by forcing shortened legs" (L970); "Exact proportional distributions remain OPEN and must still satisfy SAU-FACE-22." (L970)
- [POS] **T-1** — "this stature-share statement is a reference / central-morphology description." (L972); "The two describe different things and are not competing hard controls. No new number is introduced." (L972)
- [TEST] **SAU-FACE-22** — "Stature-accounting cast: minimum/reference/maximum bodies with head, neck, thorax, lower trunk and legs summing coherently rather than independently inflating" (L1263)
- [POS] Combined validity — "stature × head share × thoracic share × lower-trunk share × leg share;" (L2573)
- [POS] UCCA: one head-scale variable — "the SAURIN §258 ±8 % head-to-body control is exposed in two navigation contexts ... One stored semantic value, one canonical bound" (UCCA L184, excerpted)
- [POS] Legs — "moderate-to-long leg contribution;" (L258); arms — "moderate total arm contribution;" (L297, within §17); "forearms may carry somewhat greater proportional contribution than Marchfolk without approaching Cogling's defining distal redistribution or Grask reach specialization" (L298); summary "moderate arm length with modest forearm emphasis;" (L3600)
- [POS] Hands — "moderately elongated fingers;" (L310); feet — "longer forefoot/toe contribution than Marchfolk tendency;" (L284)
- [POS] Frame does not touch lengths — "Frame does **not** change stature, long-bone or axial lengths, the skull" (L4170)
- [BAN] "Saurin are not rangy reach specialists. Moderate-to-long legs and modest forearm emphasis cannot become Grask global limb dominance." (L526); "Adult creator controls cannot be pushed far enough to manufacture juvenile anatomy through:" … "childlike body ratios." (L2092, L2098)
- [TEST] SAU-BODY-13 "Grask-normalized limb/reach comparison" (L550); SAU-BODY-15 "Cogling-normalized forearm/distal comparison" (L552); SAU-FACE-21 head/neck balance (L1262); SAU-CC-13 "Adult age extremes do not create juvenile anatomy" (L2701)
- [OPEN] "Exact humerus/forearm ratios remain OPEN." (L302); Part 1 list "limb segment ratios;" "hand/finger proportions;" "foot/toe proportions;" (L575–577); "final stature distribution;" (L564)
- Audit notes: (1) §55 speaks of **head-height share** (HH-type) while §258 binds **head length** ÷ standing height (HL-type, includes rostrum) — r3 defines HSR both ways (r3 L78). T-1 resolves the authority question but the metric mismatch is the reason the two "describe different things". (2) The "+8 % head-scale decision" is referenced as the centre (L972, L4166) but its origin is not stated inside the spec. (3) Arms/legs are only ±6 % creator bands with no stated central value relative to Marchfolk beyond "moderate" / "moderate-to-long".
- [SILENT] Arm span; Saurin vs Marchfolk numeric leg share; HH-based head share number.

---

## Cross-race comparatives (explicit directional statements in canon)

Torso / leg / arm share
- SK > MF torso share: "a slightly larger torso share of total height" (SKARN L75); "slightly more torso-dominant than Marchfolk" (L86)
- SG < MF torso, SG > MF leg share: "a slightly greater leg share of height" / "a slightly shorter torso relative to stature" (SAGEKIN L137, L139)
- FN < humans torso share; FN > humans leg share: (FENN L50, L52)
- VL > FN torso share; VL < FN, AE leg share: "Greater torso share than Fenn" (VAEL L35); "somewhat smaller leg share of height than Fenn or Aelari" (VAEL L46)
- AE torso longer than FN: "Longer overall torso and waist transition than Fenn." (AELARI L124)
- GR < MF, SK torso; GR > MF, SK leg, arm and span: (GRASK L198)
- GO > GR torso share; GO < GR leg, arm, span: (GORRUND L169, L196, L200)
- GR-BODY-10 > GO limb-present family in relative limb contribution (AD-3): (GRASK L715; GORRUND L232)
- GO vs SK and GO vs MF on leg/arm/span: not determined ("GO vs S n.d.", r2 L58–60)
- DU < MF limb contribution, DU > MF torso contribution at equal height: (DURRIM L38, L97)
- PI > DU leg contribution at matched height; PI legs ≤ ordinary human adult proportions: (PIPKIN L56, L166)
- PI < MF central-trunk share: (PIPKIN L137)
- CO ≈ MF total limb share and torso share; CO ≠ FN (FN greater limb share): (COGLING L100, L558; COG-BODY-16 L470)
- SA: legs "moderate-to-long", arms "moderate"; not GR global limb dominance (SAURIN L258, L297, L526)

Within-limb segmentation
- Forearm emphasis: FN "somewhat greater forearm share" (FENN L121); AE even split, "Fenn may lean more on forearm length" (AELARI L56); VL "balanced upper arm and forearm" (VAEL L44); GR forearm "increased proportional contribution compared with Marchfolk and Skarn" (GRASK L227); GO "never copying Grask forearm emphasis" (GORRUND L67); PI "no Grask-like forearm emphasis" (PIPKIN L166); CO forearm share up, upper-arm share down (COGLING L572–573); SA modest, not CO, not GR (SAURIN L298); DU "no fixed arm ratio" (DURRIM L113); SG "slightly longer forearms" vs MF (SAGEKIN L138).
- Lower-leg emphasis: FN "slightly greater lower-leg share" (FENN L123); AE "even elongation through thigh and lower leg (not lower leg alone)" (AELARI L58); VL "balanced femur and lower leg" (VAEL L46); GR "may be proportionally emphasized relative to human reference anatomy" (GRASK L215); GO "without reproducing Grask's lower-leg emphasis" (GORRUND L196); PI slight emphasis valid, not anchor (PIPKIN L166; short-race L69); CO lower-leg share up within near-human leg (COGLING L620–624). Boundary: "**Leg segmentation alone cannot separate Cogling from Pipkin**" (COGLING L914).

Fenn vs Aelari vs Vael (limb distinctions)
- Where elongation sits: "Fenn | Concentrated in the extremities, around a compact-centered torso" vs "Aelari | Distributed continuously through the neck, torso, arms and legs" (AELARI L114–115)
- Three-branch: "Vael | More compact, deeper-bodied, with somewhat more structural presence through torso, joints and extremity bases" (VAEL L27)
- Elf review matrix: FN "Strongest extremity contribution: long arms, strong forearm and lower-leg contribution, long hands, long narrow feet"; AE "Long limbs with even elongation, upper arm to forearm and femur to lower leg"; VL "Moderate elongation, balanced segments, more substantial wrist, hand, ankle and foot transitions" (elf-comparative-review L33)
- Hands: VL "broader palm than Fenn or Aelari" (VAEL L139); FN "somewhat narrower hands and wrists" (FENN L122); AE "relatively narrow breadth, gracile wrists" (AELARI L153)
- Feet: VL "broader than Fenn or Aelari" (VAEL L141); FN "Somewhat longer and narrower" (FENN L124); AE "moderate to narrow breadth, gracile ankle" (AELARI L155)

Sagekin vs Marchfolk; Sagekin vs elves
- SG > MF leg share, forearm/hand/finger length; SG < MF torso share and ribcage depth (SAGEKIN L137–140). "Sagekin are the long-limbed end of fully human variation" (FENN L138). GR comparison: "Sagekin's mild longer-limbed tendency is never confused with Grask non-human limb architecture" (GRASK L710). Cogling comparison: Sagekin "may show somewhat greater leg contribution to height" (COGLING L992).

Skarn vs Marchfolk
- SK > MF torso share (L75/L86); SK > MF hands and feet (L79), clarified as absolute skeletal dimensions (HALVREN L454); equal-height test at 190 cm (SKARN L292). No limb-share or span direction stated.

Hands relative to stature
- DU > MF hand size relative to stature (DURRIM L115); PI "relatively moderate in size for their stature" (PIPKIN L58), lighter than DU (PIPKIN L174); CO hands larger share of arm length (COGLING L141); GR finger:palm > MF, SK (GRASK L235); GO palm breadth/depth relative to hand length (GORRUND L210); across neutral hands: "Skarn a large human hand; Durrim a relatively substantial hand for short stature; Grask a large hand integrated with long forearm and reach architecture; Gorrund a very large absolute hand" (GORRUND L210, excerpted).

Head-to-stature (direction only)
- DU, PI, CO: "somewhat greater" than MF, never oversized (DURRIM L21; PIPKIN L33, L205; COGLING L280, L727)
- SA: head-height share "near to modestly below the Marchfolk adult range" (SAURIN L970)
- GR, GO: no ratio locked, avoid tiny/oversized (GRASK L433; GORRUND L299)
- SK: "body scale sets head-to-body proportion" (SKARN L179)
- MF, SG, FN, AE, VL, HV: silent.

---

## Candidate classification of open questions (suggestions only)

Legend: **A** authorable qualitatively now · **B** direction now, number later · **C** needs mesh even for a useful answer · **D** later biology · **E** later system.

| # | Open question | Suggested | One-line justification |
|---|---|---|---|
| 1 | Grask arm span ÷ stature (GRASK L60, L166, L223, L726) | **B** | Direction is locked twice (> MF, SK: L223; > GO: GORRUND L200); only the ratio waits on RM-LR-01. |
| 2 | Pipkin arm span (PIPKIN L166, L1539; UCCA L355) | **A** (number **B/C**) | Canon already says "unusual arm span isn't a Pipkin trait"; a qualitative "no racial span tendency, DER from segments" statement can be written now; any numeric band rides RM-UB-01. |
| 3 | Pipkin trunk-share absorption split, limbs vs pelvic vertical (PIPKIN L137, L139, L166) | **C** | T-2 explicitly defers the split to RM-UB-01 / RM-SR-01 and forbids inventing a winner; direction is partially given but the two sinks are only separable by measurement. |
| 4 | Pipkin head-to-stature (L33, L205, L1534) | **B** | Direction (somewhat > MF, never oversized, never a maturity signal) is authored; number via RM-SR-04 / RM-CF-10. |
| 5 | Cogling head-to-stature (L282, L736, L3170) | **B** | Direction and an 11–13 cm head-size figure exist; ratio needs RM-SR-04 and camera validation. Clarify whether 11–13 cm is head height or length (A). |
| 6 | Cogling within-limb and finger/palm distributions (L572–575, L593, L620–621, L1089) | **B** | Every direction is stated; magnitudes are RM-SR-02. |
| 7 | Cogling arm span (L514 historical only) | **A/B** | Can be written as "DER; total arm near-MF; no span tendency stated"; whether the narrow core lowers span needs a mesh (B). |
| 8 | Grask head-to-stature (L433) | **C** | Only negative guards exist; no direction relative to MF is stated, so a useful answer needs RM-CF-10. |
| 9 | Gorrund head-to-stature (L299, L408) | **C** | Same as Grask; failure modes at max/min height are only checkable on meshes. |
| 10 | Durrim head-to-stature number (L21) | **B** | Direction stated; not listed in r3 HSR OPEN row, so add it to RM-CF-10 / RM-SR-04 scope. |
| 11 | GR-BODY-10 vs Gorrund limb-present floor (GRASK L715; GORRUND L232, L244) | **C** | AD-3 locked the direction; the numeric validator is explicitly RM-LR-04. |
| 12 | Gorrund vs Skarn (and vs MF) leg/arm/span direction (r2 L58–60 n.d.) | **A** then **C** | An author can state the intended direction qualitatively; canon is currently silent, so without an author ruling only meshes can describe it. |
| 13 | Femur:lower-leg and upper-arm:forearm bands — Grask, Gorrund, Pipkin, Durrim | **B** | Each spec gives a qualitative range (e.g. "slight femur emphasis, balanced, slight lower-leg emphasis"); numbers RM-LR-01 / RM-UB-01. |
| 14 | Saurin humerus/forearm and leg share (L302, L258, L297) | **B** | Direction ("moderate", "modest forearm emphasis") exists; ±6 % creator bands already set; central values need measurement on the frozen reference. |
| 15 | Saurin §55 head-height share vs §258 head-length bound | **A** | Authority resolved by T-1; a one-line metric clarification (HH vs HL) can be written now with no new number. |
| 16 | Elf segment magnitudes (FN/AE/VL) | **B** | Directions are explicit and mutually ordered; numbers RM-OT-02; AE "Fenn may lean more on forearm length" is provisional and needs validation. |
| 17 | Sagekin vs Marchfolk magnitudes | **B** | "Slightly" directions exist; RM-OT-01. |
| 18 | Skarn vs Marchfolk torso/leg share magnitude; Skarn arm span | **B** (span **A**) | Torso direction stated; arm span is silent and could be authored as "no racial span tendency" or left. |
| 19 | Marchfolk baseline segment bands, arm length control, head share | **C** | MF is the reference; no relative direction is possible, so values must come from the reference mesh. |
| 20 | Hand and foot proportion bands per race | **B** (GO/GR palm, finger **B**) | Directions are stated for nearly every race; numbers RM-LR-07 / RM-UB-01. |
| 21 | Halvren limb/hand/foot inheritance values | **D** | Depends on inheritance and development rules not yet authored (HALVREN L74). |
| 22 | Halvren stature tails outside 152–213 cm | **D** then **C** | UCCA/RM-UB-05: "biological authorship first ... then reference-mesh measurement". |
| 23 | Population stature distributions, all races | **D** | UCCA L113: distributions OPEN or SILENT; generation weights are non-canon. |
| 24 | Final stature envelopes and world-scale extremes 76–251 cm | **E** | World/camera/collision validation (RM-OT-05; Gorrund max "not a permanent project maximum", GORRUND L653). |
| 25 | Interaction, combat and gameplay reach | **E** | Every spec separates anatomical reach from gameplay reach (e.g. GRASK L646, DURRIM L150). |
| 26 | Durrim L93 "lower leg" wording | **A** | Editorial disambiguation only; L38 and L119 already fix the meaning. |
| 27 | Per-race allometry of head/hands/feet with stature | **C** | RM-UB-02 needs min/ref/max meshes per race. |
