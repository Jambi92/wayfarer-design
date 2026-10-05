<!-- RAC Phase 1 evidence extraction (agent-produced, line-checked at HEAD 218f64a). Not canon; supporting evidence for reviews/claude-rac-01…12. -->
# C — Sex-related body biology, hair, skin / external tissue: evidence extraction

Repo: `/home/claude/wayfarer-design` (read-only). Date of extraction: 2026-10-05.

## 0. Method, abbreviations, authority

**Spec abbreviations** (all `specs/<race>/<RACE>_V1.md`): MF Marchfolk, SK Skarn, SG Sagekin, FN Fenn, AE Aelari, VA Vael, HV Halvren, DU Durrim, GR Grask, GO Gorrund, PI Pipkin, CO Cogling, SA Saurin.
**Other sources:** PR = `decisions/PROJECT_RULES.md`; UCCA = `decisions/UCCA_V1.md`; UFCA = `decisions/UFCA_V1.md`; SRR = `reviews/short-race-comparative-anatomy-v1.md`; LRR = `reviews/claude-pass2-r2-large-race-comparative-review.md`; REG = `register/decision-register.md`; ECR = `reviews/elf-comparative-review.md` (accepted comparative review, cited only where it fills a spec silence); IT3 = `reviews/iteration-3-visual-body-validation-closed.md`; IT3M = `reviews/iteration-3-normalized-masculine-decision.md`.

**Authority (PR L67–75):** race specs (1) > PROJECT_RULES + UFCA/UCCA (2) > accepted comparative reviews / author resolutions (3) > decision register (4, "supporting decision history only; historical until reconciled", PR L71) > other reviews (5). REG L3 says entries stop at September 30, 2026 and do not reflect later canon. IT3/IT3M are level-5 visual-reference decisions ("Canonical specs remain authoritative", IT3M L5).

**Tags:** [POS] positive canon; [OPEN] explicitly open; [TEST] validation/test requirement; [BAN] prohibition / firewall; [SILENT] nothing found (grep terms stated); [REPRO] reproductive biology. Every quote below was re-checked as an exact substring of the cited line (verbatim, ≤25 words; "…" marks an elision inside a quote only where shown).

**Silence-check grep terms used (case-insensitive) on every spec:**
- Sex: `\bsex|female|\bmale\b|feminine|masculine|dimorph|reproducti|R-SEX`
- Body hair: `body hair|body-hair|chest hair|arm hair|hairy|leg hair|hirsut|pubic|axillary` (note: `axillary` only hit "maxillary" — false positives discarded)
- Facial hair: `facial hair|facial-hair|beard|stubble|mustache|moustache`
- Skin tissue: `skin thick|thick skin|durab|pore|leather|roughness|skin texture|texture|toughness|armou?r`

---

## 1. Universal rules that frame all three parts

### 1.1 R-SEX (PR L90–96)
- [POS] Hard bounds shared by default — "Hard biological validity bounds remain available to either sex unless a race's canon explicitly establishes otherwise." (PR L91)
- [POS] Overlap mandatory — "Adult phenotype overlap is mandatory." (PR L92)
- [BAN] Sex is never a package — "Sex is never a body preset or package and never forces frame, stature, muscularity, body-fat amount or distribution, face" (PR L93); the same line ends "unless explicit race canon defines a tendency." (PR L93)
- [POS] "no shift" is complete — "Per-race sex-conditioned soft distributions are allowed; "no shift" is a valid complete state for a race." (PR L94)
- [REPRO][BAN] — "Reproductive biology is never inferred from creator architecture." (PR L95)
- [POS] Saurin is the closed exception, not a template — "Existing deliberate Saurin sex-related canon (SAURIN_V1 §263) remains intact and is not generalized to other races." (PR L96)
- [POS] Terminology — "**Sex-related anatomy** = the biological category; **sex-related tendency** = a distribution shift." (PR L86) (quoted with markdown bold as in source)
- [POS] UCCA summary — "Sex-related anatomy selection is a SOFT input under R-SEX; it never moves stored values or invents dimorphism." (PR L51)

### 1.2 UCCA §11 (Sex-Related Anatomy and R-SEX, AD-C6)
- [POS] Selection is SOFT — "The body-level sex-related anatomy selection is a **SOFT biological input under R-SEX** (PROJECT_RULES)." (UCCA L173)
- [BAN] — "It **never moves already stored values**, never becomes a body package and **never invents dimorphism**." (UCCA L174)
- [POS] Only Saurin has authored centres — "Saurin's authored §263 sex-shift centres are the only authored soft centres" (UCCA L113); and "Population stature and proportion distributions are OPEN or SILENT for every race" (UCCA L113).
- [POS] Slot 7 "Sex-Related Anatomy" holds the selection plus "race-canon sex-related tissue controls (**Saurin E/B** only)" (UCCA L36); E/B are Absent for "all but Saurin" (UCCA L65).
- [REPRO][BAN] — "Reproductive biology is never inferred from creator architecture." (UCCA L177)
- [OPEN] BIO OPEN list includes "sex dimorphism magnitude (Durrim, Grask, Gorrund, Pipkin, Cogling); reproductive biology" (UCCA L355).
- [TEST] Reference-body / validation need — "**Frame × sex-related anatomy × composition factorial** at reference stature per race." (UCCA L333); validation group "F | Age / sex / asymmetry" (UCCA L324).
- [POS] Implementation must carry sex-related configurations — "Any future implementation must represent every **frame × sex-related anatomy × composition** combination independently inside each race envelope." (UCCA L135) (the "Manny/Quinn" prototype swap is "superseded at design level", same line).
- [POS] Randomization — "**Sex:** shifts only race-canon soft centres (§11)." (UCCA L268)
- [POS] Saved appearance has a domain "4 sex-related anatomy" (UCCA L276).
- [BAN] Frame and composition never write sex — frame "never writes stature, segment lengths, composition, face, hair, sex-related anatomy or presentation" (UCCA L129); composition operations "never skeletal frame, stature, sex-related anatomy or capacity" (UCCA L167).

### 1.3 UFCA sex row
- [POS] Face — "Sex-related facial tendency is **SOFT only**, never a control or preset (R-SEX). The default is "no shift"; Saurin has none (§263)." (UFCA L95)
- [OPEN] "Sex-related facial magnitude (Durrim, Grask, Gorrund, Pipkin, Cogling) | OPEN" (UFCA L379)
- [TEST] Validation tier "**F** | Age and asymmetry (with the R-SEX sex sub-tier)" (UFCA L339).

### 1.4 Hair (UCCA §13, UFCA Q-2)
- [POS] Body hair binding table — "**Bound only where canon supports it** (Pipkin, Cogling). **Hidden** for Marchfolk, Skarn, Sagekin, Fenn, Aelari, Vael and Halvren pending biological authorship." (UCCA L195)
- [OPEN] same row — "**Durrim, Grask, Gorrund: BIO OPEN.** Body hair is never inferred from scalp or facial hair" (UCCA L195)
- [POS] PR summary — "Body hair is bound only where race canon supports it; silent races keep it hidden pending biological authorship." (PR L52)
- [POS] Every spec's closing UCCA status line ends "body hair follows UCCA §13" (e.g. MF L338; identical pointer verified in all 13 specs' final status line).
- [POS] Hair colour relationship / locks — "Hair colour is related across scalp, brows, face and body without identical values. Hair is never locked to frame, sex, physique or occupation." (UCCA L198)
- [POS] Facial hair & eyebrows routed to UFCA slot 11 "(closed)" (UCCA L194); UFCA slot 11 "Facial-hair and eyebrow-hair biology. Saurin: Absent" (UFCA L52).
- [POS] UFCA Q-2 (eyebrow biology for 7 races) — "Eyebrow-hair biology for Marchfolk, Skarn, Sagekin, Fenn, Aelari, Vael and Halvren | Final closure Q-2." (UFCA L206); content: "ordinary variation in density/fullness, distribution/coverage, strand/coarseness character where the population's ordinary hair biology supports it" (UFCA L206).
- [BAN] Q-2 — "No culture, personality, class, attractiveness or sex encoding; no race-specific eyebrow morphology" (UFCA L206).
- [POS] Scope of Q-rows — "explicit author authorizations for the named coverage only. They do not change the rule that a shared slot never authorizes anatomy by itself." (UFCA L208)
- [POS] — "Durrim, Grask, Gorrund, Pipkin and Cogling keep their already-authored eyebrow biology and routing; Saurin eyebrows stay Absent." (UFCA L208)
- [TEST] N-levels — "N2 adds neutral body hair, no clothing (or a neutral fitted proxy) and neutral body language" (UCCA L339); face N2: "facial hair removed, eyebrows neutralized where practical" (UFCA L319).

### 1.5 Skin (UCCA §14, PR terminology)
- [POS] Four layers — "**Four layers govern: Natural / Environmental / Applied / Acquired.**" (UCCA L202)
- [POS] Calluses — "ordinary environmental callusing = Environmental-persistent; permanent, history-like tissue alteration = Acquired." (UCCA L212) and "no population's biology is exceptional." (UCCA L212)
- [BAN] — "surface never compensates for structure (identity survives neutral grey / uniform pigment)" (UCCA L214); "**Environmental and Acquired state are never forced by race, class, culture or occupation**" (UCCA L214).
- [OPEN] BIO OPEN — "skin thickness/durability (Durrim, Grask, Gorrund)" (UCCA L355).
- [BAN] Gameplay firewall — "No creator value feeds a gameplay stat." (UCCA L357)
- [POS] PR — "Ordinary dirt and other transient accumulation are **Environmental**" (PR L85).
- [POS] Term guard on "thickness" — ""Thickness" isn't used alone where several tissues could produce the visible dimension." (MF L283) — this is a body-dimension term rule, not about skin, but it is the only canonical "thickness" disambiguation.

---

## PART 1 — SEX-RELATED BODY BIOLOGY

### MF — Marchfolk (Human Reference Population)
- [POS] Sex-related characteristics live in Biological Anatomy — "**biological anatomy** (including relevant sex-related characteristics)" (MF L35)
- [POS] Height: distributions may differ, overlap broad — "There's no hard sex-specific height restriction from the selected sex-related anatomy or starting frame" (MF L23); "population distributions may differ where appropriate, individual overlap stays broad" (MF L23).
- [POS] Layers independent — "The four layers stay distinct, and choosing one never determines another" (MF L35)
- [POS] Human anatomy baseline (supports "human" pelvis/skin/hair biology generally, not a sex magnitude) — "Marchfolk keep recognizably human skeletal and cranial architecture, shoulders, ribcage, spine, pelvis" (MF L15)
- [BAN] Forehead: "no sex, personality, attractiveness, culture, age or ancestry stereotype" (MF L106)
- [SILENT] No pelvis/thorax/shoulder/soft-tissue/composition sex tendency, no magnitude, no like-for-like rule, no R-SEX pointer, no reproductive statement in MF (sex grep returned only L23, L35, L106 eyebrow/forehead text). UCCA treats MF as having no authored centres (UCCA L113).
- [TEST] (indirect) MF validation asks presets and stress for proportion extremes (MF L251) but names no sex-matched case.
- Register: "Marchfolk height envelope 147 / 173 / 203 cm … with no hard sex-specific height limit | AGREED" (REG L446).

### SK — Skarn
- [SILENT] Sex grep: only the eyebrow Q-2 sentence "Eyebrows encode no culture, personality, class, attractiveness or sex stereotype" (SK L166). No sex-related body text.
- [POS] Possibly relevant — "Biological anatomy sets no separate height limits." (SK L15) (the line does not name sex; it is the only "biological anatomy vs height" statement).
- [TEST] Equal-height Marchfolk comparison matched on "apparent age, muscle, body fat, pose and presentation" (SK L292) — sex is not among matched variables ([SILENT] on like-for-like).
- Note: IT3M adopted "Skarn_S2 as the neutral Skarn visual reference" (IT3M L13) in the masculine set — level-5 visual reference, "No canonical spec changes from this decision." (IT3M L36).

### SG — Sagekin
- [SILENT] Sex grep: only Q-2 eyebrow line (SG L209); "reproducible" hits are generation-reproducibility, not biology (SG L457). Population is "fully human" (SG L3) — "Sagekin are a fully human population with a distinct ancestral homeland." (SG L3).

### FN — Fenn
- [SILENT] Sex grep: only Q-2 line (FN L162) whose brow rule bans "feminine, masculine or other personality or presentation read" (FN L162).
- [POS] Partial hint on pelvis — "Exact shape awaits prototyping, and not every Fenn has narrow hips" (FN L111).
- [TEST] Equal-height test "matched on frame, muscle, body fat, age, clothing and pose, with Fenn ears hidden" (FN L78) — sex not a matched variable.

### AE — Aelari
- [POS] Pelvis — "No mandatory hip width by race or sex-related anatomy" (AE L126)
- [POS] Frame independent — "Frame stays separate from muscle, fat, sex-related anatomy, height and presentation." (AE L134)
- [BAN] Hair — "Hairstyle, length and grooming are never locked to sex-related anatomy, frame, physique or occupation." (AE L344)
- [SILENT] No tendency, no magnitude, no reproductive statement.

### VA — Vael
- [POS] Frame — "stays independent of muscle, fat, height, sex-related anatomy and presentation." (VA L128)
- [BAN] — "Hair and grooming are never locked to sex-related anatomy, frame, muscle, fat, class or occupation." (VA L407)
- [SILENT] No tendency/magnitude/reproductive statement.

### HV — Halvren
- [POS] Separation — "Sex-related anatomy stays separate from frame, height, muscle, fat, face, hair and presentation, mixed ancestry doesn't change that" (HV L54)
- [OPEN] — "exact sex-related inheritance stays within the broader unresolved anatomical-system review." (HV L54)
- [POS/OPEN] Height may later include "sex-related population distributions where later appropriate" (HV L101).
- [OPEN] Dependency — "(i) The sex-related anatomy system (Part 1 §22)." (HV L437) listed among missing source information; class B blocker: "Shared elven pelvic anatomy, the sex-related anatomy system" (HV L497), "Never invented inside Halvren." (HV L497).
- [REPRO] — "with no chromosome counts, molecular genetics, reproductive mechanisms or fertility probabilities unless later design benefits from them" (HV L19); "not inherently sterile, with reproductive biology out of scope and no chromosome or genetic pseudo-detail." (HV L319).
- Register: "Missing pelvis or sex-related anatomy stops only the dependent section | AGREED" (REG L551).

### DU — Durrim (magnitude OPEN)
- [OPEN] Core status — "Durrim sex-related anatomy isn't finalized and stays separate from height, frame, muscle, fat, face, hair, culture and occupation" (DU L58)
- [BAN] — "with no sex automatically broad, narrow, tall, short, muscular or bearded, pending the universal system" (DU L58)
- [OPEN] R-SEX pointer — "the universal rule is now R-SEX in `decisions/PROJECT_RULES.md` — Durrim magnitudes stay OPEN" (DU L58)
- [BAN] Frame — "Broad never automatically means muscular, fat, male or every skeletal dimension at maximum." (DU L52)
- [BAN] Population tendencies "never require high muscularity or body fat, beards, a masculine look" (DU L11)
- [OPEN] Fat distribution — "Fat distribution isn't forced toward belly, waist or face, and sex-related differences depend on the unresolved universal system." (DU L54); "Fat distribution (face and neck, upper torso, abdomen, waist, hips, glutes, upper arms, thighs) is separate from amount, with sex-related patterns OPEN." (DU L135)
- [POS] Pelvis (sex-neutral population tendency) — "strong shoulder and pelvic integration" (DU L11); [OPEN] "exact pelvic morphology, sex-related anatomy and facial-hair distributions" (DU L520).
- [TEST] Like-for-like (future) — equal-height comparison "matched in age, composition, sex-related state once defined, expression and presentation" (DU L304)
- [BAN/TEST] — "Never "male means giant beard and broad square face, female means a scaled-down human woman with no beard."" (DU L219); "with sex-related variation future work" (DU L219).
- [TEST] Population sampling fails on "giant beard, broad male-coded face or old-looking face" (DU L222)
- [BAN] Identity — Durrim aren't "universally muscular, broad-framed, fat, male-coded, pale or ruddy" (DU L516)
- [BAN] Cosmetics "never sex-locked by default" (DU L393)
- [REPRO/OPEN] lifecycle list includes "lifecycle, lifespan, maturation, fertility and senescence" (DU L520).
- [SILENT] No direction (which sex trends broader/deeper etc.), no thorax-specific sex rule, no hard-bound exception.
- SRR applies (level 3): "Where comparative cases include sex-related anatomical variation, compare like-for-like configurations and presentation states first." (SRR L169); "Race identity must survive without relying on a sex-linked stereotype or mismatched anatomy to create separation." (SRR L169)

### GR — Grask (magnitude OPEN)
- [OPEN] — "Exact sex-related anatomy is **OPEN**, never assumed identical to humans or exaggerated for readability" (GR L76)
- [OPEN] magnitude class itself open — "whether average skeletal dimorphism is minimal, moderate or strong is **OPEN**." (GR L76)
- [POS] — "every configuration preserves Grask anatomy" (GR L76)
- [OPEN] approved-decision list: "muscular-development capacity, the exact pelvis and sex-related anatomy and dimorphism are OPEN" (GR L138); OPEN list "sex-related anatomy and dimorphism" (GR L726).
- [OPEN/BAN] Face — "Sex-related facial anatomy is **OPEN**, never assuming human dimorphism transfers, and any differences keep the same Grask foundation." (GR L433)
- [OPEN] Surface — "Sex-related pigmentation tendencies and sex-related facial hair, body hair and pattern hair loss are **OPEN**." (GR L564)
- [SILENT] No like-for-like sex rule in GR; LRR is silent on sex (grep `sex|female|male|dimorph|like-for-like` on LRR returned nothing). LRR tests match height/composition only (e.g. LR-10 composition inversion, LRR L100).
- [REPRO/OPEN] "lifespan, maturation, fertility and senescence" (GR L726).

### GO — Gorrund (magnitude OPEN)
- [OPEN/BAN] — "Sex-related anatomy and dimorphism are **OPEN**, never assuming human-identical dimorphism, huge males and small females" (GO L82)
- [BAN] — "or one sex broad or muscular and the other narrow or soft; all share one Gorrund foundation." (GO L82)
- [POS] Pelvis — "Pelvic breadth | May trend substantial, with external hip width kept separate from muscle, fat and sex-related anatomy" (GO L50)
- [OPEN] Part 1 OPEN list "ribcage, shoulder and pelvic morphology … sex-related anatomy and dimorphism" (GO L159); major OPEN "sex-related anatomy and dimorphism" (GO L699).
- [OPEN] Face — "Sex-related facial anatomy is **OPEN**, never assuming human dimorphism transfers, and future differences stay within one Gorrund foundation." (GO L413)
- [OPEN] Surface — "Sex-related pigmentation, facial and body hair, pattern loss and age interactions are **OPEN**, never assuming human patterns" (GO L564)
- [REPRO/OPEN] "Lifespan, maturation, fertility, senescence and developmental timing are **OPEN**, with no numbers." (GO L531)
- [SILENT] No like-for-like sex rule; LRR silent.

### PI — Pipkin (magnitude OPEN; most developed non-Saurin text)
- [OPEN/BAN] — "Sex-related anatomy and dimorphism are **OPEN**, never assuming human proportions transfer or encoding exaggerated dimorphism." (PI L72)
- [POS] Scope of influence — "Sex-related physical anatomy may influence relevant pelvic, thoracic, facial, soft-tissue and other biological relationships, but:" (PI L1491)
- [BAN] — "it does not determine height, frame, muscularity, fat amount, hair, clothing, class, personality or culture;" (PI L1492)
- [POS/TEST] — "like-for-like comparisons are used where sex-related anatomy materially affects a race comparison;" (PI L1493)
- [BAN] — "racial identity is not defined by external shoulder-to-hip ratio or sex-coded presentation." (PI L1494)
- [OPEN] — "Exact creator-facing control organization remains subject to the universal architecture review." (PI L1496); OPEN list "magnitude and morphology of sex-related dimorphism;" (PI L1545)
- [POS] Pelvis vs thorax tendency is a race trait measured within sex — "Where sex-related anatomy materially affects pelvis or thorax, compare like-for-like anatomical configurations" (PI L154); "(for example male Pipkin with male Marchfolk and female Pipkin with female Marchfolk)" (PI L154)
- [BAN] Pelvic breadth "never extremely wide hips, feminized anatomy, high fat or one hourglass silhouette; this is skeletal anatomy" (PI L151); greater valid breadth "avoids caricature, sex stereotyping and body-fat confusion" (PI L198)
- [POS] "External hip width | Skeletal breadth, gluteal muscle, fat distribution and external circumference stay separate" (PI L155)
- [TEST] PIP-BODY-28 — "Adult male Pipkin vs adult male Marchfolk at normalized displayed height, frame and composition" (PI L224); PIP-BODY-29 the female equivalent (PI L225); both require "without cross-sex coding" (PI L224, L225).
- [TEST] PIP-FACE-22/23 male/female vs Marchfolk "without exaggerated dimorphism" (PI L445) and "without juvenile or cross-sex coding" (PI L446).
- [TEST] PIP-INT-21 — "Like-for-like sex-related movement comparison: adult male Pipkin vs adult male Marchfolk walk" (PI L1615)
- [BAN] Lips "not sex-locked or race-defining" (PI L319); lashes "never used as sex or youth shorthand" (PI L381).
- [REPRO/OPEN] "Exact maturation timing, lifespan, senescence curve, fertility timing and age-frequency distribution require later world/lifecycle design." (PI L1485)
- Register: within-sex measurement "AGREED (resolved by the Part 2 patch below)" (REG L934); "dimorphism magnitude stays OPEN" (REG L942).
- Implication for reference bodies: PI requires a male and a female Pipkin and Marchfolk pair for validation (PI L224–225) → sex-related reference morphology is needed for both PI and MF, even though PI magnitude is OPEN and MF is SILENT.

### CO — Cogling (magnitude OPEN)
- [POS] Pelvis must carry sex-related anatomy — "The pelvis must provide adult locomotor and sex-related anatomy without becoming:" (CO L258); [OPEN] "Pelvic breadth, depth, height and sex-related morphology remain OPEN for detailed Part 2 work." (CO L264)
- [POS] — "The pelvis must remain capable of broad valid sex-related and individual variation." (CO L689); [OPEN] "Exact pelvic breadth, depth, height, inlet/outlet morphology and external soft-tissue expression remain OPEN." (CO L691)
- [POS] Neck varies "with frame, sex-related anatomy, muscularity and individual genetics." (CO L272)
- [OPEN] Fat — "Sex-related and individual distribution patterns remain subject to the universal anatomy model and later detailed review." (CO L333)
- [POS] §23 — "Sex-related physical anatomy may affect pelvis, thorax, soft tissue and other biological structures where appropriate, but does not automatically determine:" (CO L339) (list: height, frame, muscularity, fat amount, facial identity, hairstyle, clothing, class, culture, occupation, personality).
- [OPEN] — "Magnitude and morphology of Cogling sex-related dimorphism remain OPEN." (CO L352)
- [POS/TEST] §61 — "The race must remain recognizable in like-for-like comparisons and across valid anatomical configurations." (CO L875)
- [BAN] — "No single shoulder-to-hip ratio, chest form, waist shape or external hip width defines either Cogling sex-related anatomy or Cogling racial identity." (CO L877); [OPEN] "Magnitude and detailed morphology remain OPEN." (CO L879)
- [BAN] Height changes must not automatically change "- sex-related anatomy." (CO L893; §62 list).
- [POS] Face §93 — "It does not define a binary set of faces and does not determine:" (CO L1492); "Exact magnitude remains OPEN." (CO L1505)
- [POS] UFCA routing — "there is no face-level sex slider and the magnitude stays OPEN (UFCA AC-U2)." (CO L1566)
- [BAN] Movement firewall §164 — "Movement differences should arise from anatomy only where physically necessary and must not encode gender stereotypes." (CO L2520)
- [TEST] COG-BODY-14 "Like-for-like sex-related adult comparisons; race identity does not depend on sex coding" (CO L468); COG-BODY-28 "Like-for-like sex-related normalized comparison against Marchfolk" (CO L1073); COG-FACE-21/21A (CO L1658–1659); COG-MOVE-20 (CO L2604).
- [TEST] Reference preset set — "At minimum, first-pass validation should support neutral biological presets approximately covering:" (CO L2941) including "- multiple sex-related anatomical configurations;" (CO L2949). → Explicit canon need for multiple sex-related reference bodies.
- [BAN] Muscularity "cannot serve as a proxy for age, sex, occupation or racial authenticity." (CO L838)

### SA — Saurin (CLOSED reference; brief)
- [POS] §263 closed — "Saurin sexual dimorphism is low-to-moderate and regionally limited to the trunk" (SA L407)
- [POS] Four authored centres: lower axial trunk "female distribution centre **+7 %**" within "±10 %" (SA L101); pelvic band "female centre **+5.5 %**" inside "±7 %" (SA L150); E 2.0 cm, B 1.6 cm, ceiling 3.0 cm (SA L4227–4230 table).
- [POS] Distribution model — "Sex influences **soft population distributions**, not body presets or separate anatomical envelopes." (SA L4216); "Male and female hard bounds are identical; sex never extends a species bound." (SA L4217)
- [POS] "**Overlap is mandatory.**" (SA L4218); "No control is named or implemented as "female body"." (SA L4219, typographic quotes in source)
- [POS] No shift elsewhere — "Stature, skeletal frame, muscle, generic fat, tail, skull/face and the cranial-display family receive **no sex shift" (SA L4220)
- [POS] "The female tendency is **anti-hourglass**" (SA L4221); [POS] "Sex is not reliably readable at gameplay distance; anatomy is not exaggerated to force it." (SA L4236)
- [REPRO] Excluded: "mammary glands; lactation; nipples; human breasts; human external genital anatomy" (SA L4242); "No external primary-sex anatomy is modelled; the ventral pelvic field is identical in both sexes." (SA L4242)
- [REPRO][OPEN] "internal gestation; egg vs live young; provisioning mechanism; reproductive organs and physiology" (SA L4244)
- [POS] E/B not fat — "Sex-correlated body-wall and ventral fullness (§263) belong to Biological Anatomy, not Physical Composition" (SA L2237)
- [POS] Face — "no craniofacial sex shift is canon." (SA L1059)
- [TEST] SAU-BODY-19 "Same body with multiple neutral sex-related anatomical configurations; race identity unchanged" (SA L556); "Validated on the reference female: Narrow/Balanced/Broad, low/high muscle, low/high fat, 168/208 cm" (SA L4252).
- Relevance: §263 shows the canonical closure *pattern* (named regions, centres as % or cm, identical hard bounds, overlap, exclusions, CONSTRAIN examples, reference accounting at equal stature, mesh validation) but PR L96 forbids generalizing its content.

### Part 1 — cross-race observations (evidence, not recommendations)
1. Only SA authors direction + magnitude. PI and CO author the *scope* (pelvis, thorax, soft tissue, face may be affected) but no direction; DU, GR, GO author OPEN plus bans only; HV defers to sources; AE/VA author independence statements only; MF authors "population distributions may differ" for height only; SK/SG/FN are SILENT.
2. Like-for-like sex comparison rules exist in PI (L154, L1493, tests L224–225, L445–446, L1615), CO (L875, tests L468, L1073, L1658–1659, L2604), DU (L304 "once defined"), SRR L168–169. They are absent from MF, SK, SG, FN, AE, VA, HV, GR, GO and LRR.
3. Sex-related reference sets are required by: UCCA factorial (L333) and implementation rule (L135) for every race; CO L2949; PI L224–225 (which also forces male + female MF reference bodies); SA L556/L4252. Level-5 reviews already used masculine and feminine normalized sheets: "The neutral reference bodies preserve racial architecture across masculine and feminine examples without using masculine=broad or feminine=gracile as substitutes for race." (IT3 L21).
4. No spec establishes a sex-specific hard bound (PR L91 default stands everywhere; SA L4217 confirms identical bounds).

### Part 1 — Candidate classification (labelled suggestions)
- **Q1.1 DU sex-related body magnitude/morphology (pelvis, thorax, soft tissue, fat distribution).** Suggestion: **D** (later biology), secondary **C**. Canon has no direction at all (DU L58 "isn't finalized"; L135 "sex-related patterns OPEN"); bans are already authorable (A-type content exists). A direction cannot be set without authoring biology; SA's closure needed mesh accounting (SA L4236), so numbers will be C after D.
- **Q1.2 GR sex-related magnitude.** Suggestion: **D**. Even the magnitude *class* ("minimal, moderate or strong", GR L76) is OPEN; nothing to calibrate yet.
- **Q1.3 GO sex-related magnitude.** Suggestion: **D**. Same structure as GR (GO L82, L413); only bans present.
- **Q1.4 PI sex-related magnitude.** Suggestion: **B** (direction could be authored now: canon already names regions "pelvic, thoracic, facial, soft-tissue", PI L1491, and the within-sex measurement rule is closed, REG L942); numbers **C** (PIP-BODY-28/29 need male and female meshes at normalized height). Note that direction itself is still unauthored — B requires an author decision.
- **Q1.5 CO sex-related magnitude.** Suggestion: **B → C**, same logic as PI: regions named (CO L339, L873), pelvis must "provide … sex-related anatomy" (CO L258), presets need "multiple sex-related anatomical configurations" (CO L2949).
- **Q1.6 MF/SK/SG sex-related tendencies (silent human-family).** Suggestion: **A or B** by author choice: R-SEX permits declaring "no shift" as a complete state now (PR L94) — **A**; alternatively MF L23 ("population distributions may differ where appropriate") supports a human-reference direction now with numbers later — **B**. Note PI L224–225 already requires male and female MF reference bodies, so MF sex-related reference morphology is needed regardless (C for the meshes).
- **Q1.7 FN/AE/VA sex-related tendencies.** Suggestion: **A** ("no shift" valid now) or **D** if elven dimorphism is to be designed; canon has only independence statements (AE L126, L134; VA L128) and FN is silent.
- **Q1.8 HV.** Suggestion: **D**, dependent on sources (HV L437(i), L497; REG L551 source-first rule).
- **Q1.9 Reproductive biology (all non-Saurin; SA open items).** Suggestion: **D**, and outside creator scope (PR L95, UCCA L177; HV L319 "out of scope").
- **Q1.10 Sex-related reference bodies for validation (all races).** Suggestion: **C**. Required by UCCA L333/L135; content depends on Q1.1–1.8 (with "no shift" a race's two reference bodies may legitimately share body-proportion values but still exist as configurations).

---

## PART 2 — HAIR

### MF — Marchfolk
- Body hair: [SILENT] (grep terms above: no hit except the UCCA pointer "body hair follows UCCA §13", MF L338). Binding: Hidden pending biological authorship (UCCA L195).
- [POS] Possibly supporting human hair biology generally — Marchfolk keep "face, skin and hair biology and human locomotor anatomy" (MF L15) (in the sentence "Marchfolk keep recognizably human … skin and hair biology"). This is general, not body-hair-specific.
- Facial hair: [POS] "Facial hair has its own style, length, density and color controls." (MF L181); "Its color is linked to hair color by default, with an option to unlink them." (MF L181); presentation includes "hair, facial hair, clothing, makeup" (MF L35). No sex distribution stated ([SILENT] on sex link).
- Eyebrows: [POS] UFCA Q-2 bound (MF L106; UFCA L206).
- Scalp hair: [POS] planned controls "texture", "color", "hairline", "density" (MF L164–175); natural colours "Black, dark brown, brown, light brown, blond, auburn and red" (MF L304). [OPEN] texture distribution absent (HV L437 (g) "The Marchfolk hair-texture list" missing).
- [TEST] aging affects "hair density and pigmentation" (MF L257).

### SK — Skarn
- Body hair: [SILENT] (only UCCA pointer SK L382). Hidden (UCCA L195).
- Facial hair: [POS] "Facial hair is presentation, not racial identity. Clean-shaven Skarn are fully recognizable as Skarn." (SK L195); "Facial hair is independent presentation: clean-shaven, stubble, or short, full, long or styled and braided beards." (SK L228); [BAN] "Skarn are not all square-jawed, heavy-browed, bearded or angry-looking." (SK L154). Note: SK frames facial hair as *presentation* only; biological facial-hair growth capability is not separately stated ([SILENT] on facial-hair biology).
- Eyebrows: Q-2 bound (SK L166).
- Scalp: [POS] "texture, hairline, density, color, graying" (SK L224); "Hair isn't locked to anatomy, frame or physique." (SK L224)
- [POS] Skarn ears follow "the Marchfolk human-family auricular anatomical foundation" (SK L160) — precedent of human-family inheritance by explicit AC, *not* extended to hair.

### SG — Sagekin
- Body hair: [SILENT] (only pointer SG L477). Hidden.
- Facial hair: [POS] "Facial hair stays independent, from clean-shaven to substantial where biologically appropriate, and never determines ancestry." (SG L281); [TEST] checklist fail item "Mandatory facial hair." (SG L379)
- Scalp: [POS] "Sagekin have the full human range: straight, wavy, curly, and tightly curled or coiled." (SG L46); "Biological hair (texture, density, natural color) is separate from hairstyle." (SG L277)
- Eyebrows: Q-2 bound (SG L209).
- [POS] "fully human population" (SG L3) — general support for human-family biology, not a body-hair authorization.

### FN — Fenn
- Body hair: [SILENT] (only pointer FN L550). Hidden.
- Facial hair: [SILENT] in FN (facial-hair grep returned nothing). ECR (level 3) fills: "Not biologically prohibited for any elf without a later reason." (ECR L175); "Clean-shaven isn't universally elven" (ECR L175). REG: "Facial hair isn't biologically prohibited for elves, and clean-shaven isn't universally elven | AGREED" (REG L411).
- Eyebrows: Q-2 eyebrow-hair biology bound (FN L162) plus anatomical brow controls (UFCA L204).
- Scalp: [POS] "Texture covers straight, wavy, curly, and tightly curled or coiled." (FN L264); "Frequencies wait for the comparative elf review." (FN L264)

### AE — Aelari
- Body hair: [SILENT] (only pointer AE L616). Hidden.
- Facial hair: [POS] "Aelari are neither required to be clean-shaven nor required to have facial hair. Frequency is provisional." (AE L340); [OPEN] REG "Aelari hair, eye and facial-hair frequencies | OPEN" (REG L280).
- Scalp: [POS] "Elves aren't universally straight-haired." (AE L332); silver/white "if it's later validated as Aelari biology" (AE L332).
- [BAN] "Hairstyle, length and grooming are never locked to sex-related anatomy, frame, physique or occupation." (AE L344)
- Eyebrows: Q-2 bound (AE L204).

### VA — Vael
- Body hair: [SILENT] (only pointer VA L622). Hidden.
- Facial hair: [POS] "Facial hair is neither required nor prohibited by Vael ancestry." (VA L399); "Presence, density, texture, length, style, color and graying are all biologically appropriate variation." (VA L399)
- Scalp: [POS] "Biology: texture, density, natural color, hairline, age changes." (VA L389); "Not universally straight. Frequencies provisional" (VA L390)
- [BAN] (VA L407) hair never locked to sex-related anatomy.
- Eyebrows: Q-2 bound (VA L225).

### HV — Halvren
- Body hair: [SILENT] (only pointer HV L507). Hidden.
- Facial hair: [POS/OPEN] "Facial-hair biology will follow ancestry distributions, without assuming elves can't grow facial hair" (HV L210); "Facial hair depends on population inheritance, with no assumptions that Halvren can't grow it, elven ancestry always reduces it" (HV L266); [OPEN] "(f) Facial-hair distributions for humans and elves." (HV L437)
- Scalp: [POS] "Human-family ancestry supports black, dark brown, brown, light brown, blond, auburn and red" (HV L266); "inherited natural silver or white hair stays separate from age-related depigmentation" (HV L266)
- Eyebrows: Q-2 bound (HV L233).
- [BAN] Source-first: HV may not invent source biology (REG L551; HV L497 "Never invented inside Halvren").

### DU — Durrim (body hair BIO OPEN)
- Body hair: [OPEN] "Body-hair biology is OPEN, identity never comes from universal hairiness" (DU L207); [POS] future structure: "any later body hair separates biology, grooming, age, sex-related distribution and individual variation." (DU L207)
- Facial hair: [POS] "Facial-hair biology (follicle distribution, density, texture, coverage, growth rate where relevant, age change) is designed separately from beard culture" (DU L203); [OPEN] "with Durrim distributions provisional until sex-related anatomy is resolved." (DU L203); [OPEN] "**Durrim facial-hair sex-related distributions are OPEN.**" (DU L207); [BAN] "real-world human distributions aren't assumed to apply to Durrim" (DU L207)
- [POS] Locked — "A clean-shaven Durrim must look completely biologically valid and unmistakably adult" (DU L205)
- [POS/BAN] "not every Durrim grows a beard, facial hair isn't only male, beard density doesn't define adulthood, beard length isn't biological, and beardless Durrim aren't unusual." (DU L58)
- Eyebrows: [POS] "Eyebrows vary in density, width, shape, texture, pigmentation and asymmetry, never necessarily bushy" (DU L207)
- Scalp: [POS] "Texture isn't restricted: straight, wavy, curly, and tightly curled or coiled where appropriate to final population design, with frequencies OPEN." (DU L199); "Scalp-hair density varies, never universally thick-haired, bald-resistant or hairy" (DU L199)
- [POS] "scalp hair, eyebrows and facial hair related but not identical" (DU L422)
- [TEST] "Hair neutralization | Different hair colors, textures, densities and hairlines are equally Durrim" (DU L406); beard physics validation with armour, "clipping is never accepted as an unavoidable racial feature" (DU L207).
- REG: "Durrim facial-hair sex-related distributions, body-hair biology … | OPEN" (REG L587).

### GR — Grask (body hair BIO OPEN)
- Body hair: [OPEN] "Body-hair distribution is **OPEN**, without universal hairiness." (GR L402); early part: "Scalp, facial and body hair biology come in later parts, never assuming trolls are hairless, very hairy, bald or bearded." (GR L76); [OPEN] sex-related body hair (GR L564); "sex relationships of body and facial hair" (GR L726).
- Facial hair: [POS] "not all or no Grask grow beards, and troll facial hair isn't required to be sparse or coarse." (GR L402); [OPEN] "Sex-related and individual facial-hair distributions are **OPEN** pending universal sex-related anatomy work, with no male-coded troll face." (GR L402); [POS] "facial hair contributes **zero required racial recognition**" (GR L402)
- Eyebrows: [POS] "skeletal brow, eyebrow hair, expression, age and lighting stay separate" (GR L354) (Grask eyebrow-hair biology otherwise thin; UFCA L208 says GR keeps "already-authored eyebrow biology").
- Scalp: [POS] "Bald Grask are fully valid, and any population-specific pattern hair loss is **OPEN**." (GR L402); "Hair biology (what can grow) stays separate from personal presentation" (GR L402)
- REG L721: "body hair" OPEN.

### GO — Gorrund (body hair BIO OPEN)
- Body hair: [OPEN] "body hair is **OPEN**, never inferred from size." (GO L521); approved list "body hair OPEN" (GO L415); [OPEN] sex-related body hair (GO L564).
- [POS] Colour relation — "Scalp, eyebrow, facial and body hair relate in color without exact matching." (GO L521) (presupposes body hair can exist; no distribution).
- Facial hair: [POS] "never assuming a mandatory beard, mandatory clean-shaven state or coarse ogre beard (sex and age distributions **OPEN**)" (GO L521); "A clean-shaven Gorrund is fully recognizable, and facial hair contributes **zero required racial recognition**." (GO L365); [OPEN] "Relationships among sex-related anatomy, age and facial-hair density, distribution and pattern are **OPEN**" (GO L365)
- Eyebrows: [POS] "brow skeleton, eyebrow hair, expression, age and lighting stay separate" (GO L308)
- Scalp: [POS] "Bald and haired Gorrund are valid, and pattern hair loss may exist with prevalence **OPEN**." (GO L365); "patterned loss may exist with distribution, age and sex relationships and frequency **OPEN**" (GO L521)
- [TEST] Helmets/facial hair strategy OPEN (GO L645).

### PI — Pipkin (body hair BOUND)
- Body hair: [POS] "Pipkin support broad individual variation in body-hair density and distribution across limbs, torso and other ordinary humanoid regions." (PI L563); [OPEN] "Exact sex-related and hormonal population distributions remain **OPEN**." (PI L563)
- [BAN] "- hairy feet are not required," (PI L566); "- unusually hairy bodies are not required," (PI L567); "- body hair does not encode rusticity or masculinity," (PI L568); "- lack of body hair does not encode youth or femininity." (PI L569)
- Note internal staleness: Part 3 still says "Body-hair biology belongs to the later universal/race surface review." (PI L383); Part 4 §11 (L561–569) supersedes in practice and UCCA binds PI (UCCA L195).
- [TEST] PIP-SURF-07/08/12/13 (PI L655–661), e.g. "Low body hair, no youth/sex coding" (PI L660), "Higher body hair, no rusticity/masculinity coding" (PI L661); combined test "High body hair + substantial feet: must not create a hairy-foot fantasy stereotype." (PI L675)
- Facial hair: [POS] "Facial-hair capability is biologically variable and must not be required for adult male recognition or adult recognition generally." (PI L369); "Where anatomy/hormonal configuration supports facial-hair growth, density, coverage, strand character and pattern vary." (PI L371); [OPEN] "Sex-related facial-hair distributions and hormonal relationships remain **OPEN** pending universal review and must use soft biological correlations rather than hard presentation locks." (PI L375)
- Eyebrows/lashes: [POS] "Eyebrow density, thickness, shape and growth direction vary; brow grooming is presentation." (PI L381)
- Scalp: [POS] "Pipkin scalp hair follows a broad adult humanoid biological range." (PI L361)

### CO — Cogling (body hair BOUND)
- Body hair: [POS] "Body-hair amount and distribution vary individually." (CO L1817); [BAN/POS] "Body hair is **not determined by** scalp hair, facial hair, sex-related anatomy, muscularity, age presentation or culture." (CO L1819); [OPEN] "Any sex-related or hormonal distributions in scalp, facial or body hair remain OPEN" (CO L1821) "and, if later approved, must use **soft correlations rather than hard creator dependencies**." (CO L1821); [BAN] "No unusually hairy or hairless Cogling racial stereotype is approved." (CO L1823)
- Register flags a tension: "Body hair "independent from sex-related anatomy" pre-decides an OPEN distribution question" (REG L1057, OPEN, Cogling Part 4 audit). The current spec wording ("not determined by" + soft correlations OPEN) appears to be the reconciled form; REG is level 4 and pre-dates later canon (REG L3).
- Facial hair: [POS] "Where supported by individual biology, Cogling may grow facial hair." (CO L1802); list: "is not mandatory", "does not define sex" (CO L1805, L1807).
- Eyebrows: [POS] "Eyebrow and eyelash biology remains independently variable." (CO L1827); "No permanently raised, bushy inventor brow or childlike fine brow is racial." (CO L1836)
- Scalp: [POS] hair architecture may vary in "- strand thickness;" (CO L1773), "- density;" (CO L1774), "- straight/wavy/curly/coily pattern;" (CO L1775); [POS/TEST] "biological hair diameter is not assumed to scale linearly with total body height." (CO L2035); [OPEN] "Exact strand diameter, density and grooming representation require later art/technical validation." (CO L2037)

### SA — Saurin (brief)
- [POS] "Baseline Saurin do **not** possess mammalian scalp hair." (SA L1909); "Saurin do not possess human-style facial hair by default." (SA L1919); "generic creator categories for mammalian **Hair** and **Facial Hair** are biologically empty under the current baseline and must not expose human assets." (SA L604); UCCA: "**No mammalian hair (Absent).**" (UCCA L196).

### Part 2 — statements that could support or forbid body-hair authoring for silent races
- Support (general human-family biology): MF L15 ("skin and hair biology" kept human); SG L3 ("fully human population"); SK "Skarn faces are fully human and diverse." (SK L48); precedent of explicit human-family inheritance for ears (SK L160, Pass 2 AC-4); PI L563 phrase "ordinary humanoid regions" (Pipkin-only).
- Support (elves): ECR L175 shared validity principle for *facial* hair only.
- Forbid inference: UCCA L195 "Hidden … pending biological authorship" and "Body hair is never inferred from scalp or facial hair"; UFCA L208 "a shared slot never authorizes anatomy by itself"; PR L52; GO L521 "never inferred from size"; HV L497 / REG L551 source-first (HV cannot invent).
- Consequence: no current text authorizes body hair for MF/SK/SG/FN/AE/VA/HV; the human-family statements are general and would need an explicit author binding (as Q-2 did for eyebrows, UFCA L206–208).

### Part 2 — Candidate classification (labelled suggestions)
- **Q2.1 Body hair MF/SK/SG (silent, human-family).** Suggestion: **A** — authorable qualitatively now by explicit author decision modelled on Q-2 ("ordinary human hair biology", with PI-style bans), because MF L15/SG L3/SK L48 establish human-family biology; frequencies later. Without that decision it stays Hidden (UCCA L195).
- **Q2.2 Body hair FN/AE/VA (silent, elven).** Suggestion: **A or D**. A if the author extends the ECR shared-validity principle (ECR L175) to body hair; D if elven body-hair biology is to be designed. No elven text on body hair exists.
- **Q2.3 Body hair HV.** Suggestion: **D** (blocked on sources by source-first rule, REG L551).
- **Q2.4 Body hair DU/GR/GO (BIO OPEN).** Suggestion: **A** for the qualitative baseline (broad individual variation + existing bans: DU L207 "never … universal hairiness", GR L402, GO L521 "never inferred from size"); **D** for sex-related distribution (DU L207, GR L564, GO L564).
- **Q2.5 Sex-related facial-hair distributions DU/GR/GO/PI/CO.** Suggestion: **D** — every spec ties it to the unresolved sex-related system (DU L203, GR L402, GO L365, PI L375, CO L1821); PI/CO already fix the form (soft correlations, no hard locks).
- **Q2.6 Facial-hair biology MF/SK (presentation-only wording).** Suggestion: **A** — growth capability is implicit (MF L181 density control; SK L228) but not stated as biology; a clarifying binding is qualitative.
- **Q2.7 Eyebrow biology.** Closed for 7 races (UFCA Q-2); DU/GR/GO/PI/CO authored; SA Absent. No open question.
- **Q2.8 Cogling hair-strand scale.** Suggestion: **C** (CO L2037 requires art/technical validation).

---

## PART 3 — SKIN / EXTERNAL TISSUE

### MF — Marchfolk
- [POS] Layers — "Environmental | Sun exposure, tanning, weathering, dryness, roughness, calluses, minor discoloration, dirt" (MF L160); "Acquired | Scars" (MF L162).
- [POS] Surface vs structure in markings — "Placement respects anatomical regions and avoids heavy texture distortion." (MF L185)
- [SILENT] Skin thickness/durability: no hit for `skin thick|durab|pore|toughness` in MF. Human baseline via MF L15 "skin and hair biology".
- [BAN] Rugged reputation not anatomy — "ruggedness, manual labor, survival skill, toughness, frontier clothing, weathering, scars and muscularity come from culture, background, occupation, environment or history." (MF L35)

### SK — Skarn
- [POS] Layers — "Environmental | Sun exposure, wind and weather, dryness, roughness, calluses, localized wear, dirt" (SK L212)
- [SILENT] thickness/durability/pores (grep). 

### SG — Sagekin
- [POS] "The universal four layers stay: natural, environmental, applied and acquired." (SG L269)
- [SILENT] thickness/durability/pores.

### FN — Fenn
- [POS] Environmental layer includes "roughness, dryness, calluses, localized wear, dirt" (FN L256)
- [SILENT] thickness/durability.

### AE — Aelari
- [POS] Environmental "(tanning, sun, weathering, dryness, roughness, calluses, dirt)" (AE L303)
- [SILENT] thickness. REG (level 4): "gracile never means fragile, weaker, less durable or thin | AGREED" (REG L377) (Elf Review).

### VA — Vael
- [POS] "Vael skin shows blood-flow influence, localized redness or equivalent perfusion, subsurface variation, regional differences (lips, eyes, ears, palms)" (VA L371); "It's never flat or monochrome." (VA L371)
- [SILENT] thickness/durability.

### HV — Halvren
- [POS] "Natural, Environmental, Applied and Acquired layers stay separate" (HV L311)
- [SILENT] thickness/durability.

### DU — Durrim (thickness/durability OPEN)
- [OPEN][BAN] "Durrim skin thickness or tissue durability relative to other humanoids isn't assumed from the substantial skeleton, and has no gameplay effect" (DU L359)
- [POS] Surface detail — "Realistic pores, fine lines, texture, local pigment, age changes and individual variation, never exaggerated roughness to look "rugged"" (DU L358)
- [POS] Classification of skin as surface appearance — "Skin thickness, texture, wrinkles, pores, scarring and weathering are surface appearance" (DU L278)
- [BAN] Structure vs material — "Racial structure is never faked mainly through normal maps, displacement, roughness, ambient occlusion, baked shadow or skin materials" (DU L280); "large-scale depth lives in geometry or deformation, fine detail may use materials later" (DU L280)
- [BAN] Ruddiness "Never biologically required." (DU L356); "Regional variation … never painted-on gradients" (DU L357)
- [POS] Approved list: "skin toughness or thickness differences OPEN" (DU L422); OPEN list "skin thickness and tissue durability" (DU L520).
- [BAN] "Scars are acquired unless a specific biological mechanism says otherwise" (DU L393); "Durrim aren't universally weathered." (DU L393)
- REG L614 OPEN (skin thickness or toughness).

### GR — Grask (thickness/durability OPEN)
- [OPEN][BAN] "Whether Grask skin thickness or tissue durability differs from humans is **OPEN**, never inferred from stature, mythology, coloration or combat role." (GR L512)
- [BAN] "Default skin is recognizably biological, never warty, scaly, rocky, cracked, slimy, leathery or bark-like" (GR L512)
- [POS] "pore visibility, fine texture, oiliness, dryness, local roughness and fine lines vary by individual, age, environment and exposure, without racializing grime or neglect." (GR L512)
- [POS] Visible tissue effect stated as observation — "ear pigmentation may vary with thickness (translucency in thinner areas, vascular influence, regional pigment) as observational surface phenomena" (GR L512)
- [POS] Palms/soles "aren't assumed bright pale, dark pads or animal-like foot pads" (GR L512)
- [TEST] "A Grask stays recognizable under a neutral diagnostic material" (GR L491)
- [POS] Approved: "skin thickness and durability are OPEN; warts and growths aren't racial anatomy" (GR L568); "gray never implies stone biology, death or age" (GR L568)
- [POS] Skin materials "must eventually represent pigmentation, undertone, regional variation, age, texture and environmental overlays" (GR L564)
- LRR: LR-05 fails "if skin or ears alone separate them" (LRR L95).

### GO — Gorrund (thickness/durability OPEN)
- [OPEN][BAN] "Skin thickness and soft-tissue durability are **OPEN**, never inferred from size or turning large anatomy into armor." (GO L515)
- [BAN] "Default skin is biological humanoid skin, never inherently warty, rocky, leathery, cracked, scaly, bark-like, slimy or callused everywhere." (GO L515)
- [POS] "Pore visibility, fine texture, oiliness, dryness, local roughness, fine lines and exposure changes vary with biology, age, environment and activity." (GO L515)
- [BAN] "Warts, lesions, cysts and growths aren't racial identifiers, and "ogre skin" is never made through pathology." (GO L515)
- [POS] Calluses — "acquired rather than racial, and smooth, well-cared-for Gorrund skin is fully valid." (GO L515); layer clarification "ordinary environmental callusing is **Environmental-persistent**" (GO L517)
- [BAN/TEST] lighting/material: colours "never turn bright green, dead gray or stone-textured through lighting or material response." (GO L541); clean, dry, neutral-lighting recognition test (GO L537).
- [OPEN] major list "skin thickness and durability" (GO L699).

### PI — Pipkin
- [SILENT] thickness/durability (grep `skin thick|durab|tough` returned no skin hit).
- [POS] "Visible vascularity and flushing depend on pigmentation, skin properties, temperature, exertion, emotion and physiology." (PI L506)
- [POS] Specialized regions "should be modeled as biological surface systems rather than painted racial masks." (PI L508)
- [POS] Aging "changes in texture, elasticity, wrinkling, localized pigmentation" (PI L607)
- [TEST] PIP-SURF-17 "Same anatomy rendered under substantially different valid lighting; biological identity unchanged" (PI L665)
- [OPEN] "detailed skin/weathering distributions;" (PI L1550)

### CO — Cogling
- [SILENT] thickness/durability.
- [POS] "Healthy Cogling skin may show broad individual texture variation." (CO L1754); texture may reflect "pores" (CO L1759)
- [BAN] "Small body scale does not imply doll-like, poreless or permanently smooth skin." (CO L1764); "Texture also cannot be exaggerated merely to prove adulthood." (CO L1766)

### SA — Saurin (brief)
- [POS] "Saurin possess a **scaled integument** as baseline biological anatomy." (SA L1325); "“Scales” are not one uniform tile texture." (SA L1327); "scales conform to anatomy rather than replacing it." (SA L1335)
- [BAN] Ventral field "is not automatically a snake belly, armor plate or aquatic adaptation." (SA L1405); musculature "is not armour plating" (SA L711)
- [BAN] Gameplay: tail "carries no automatic gameplay effect: no damage vulnerability" (SA L215); "They do not automatically grant climbing, unarmed-damage or weapon bonuses." (SA L1751)
- [OPEN] UCCA "per-field numeric ranges OPEN" (UCCA L214).

### Part 3 — visible structural skin vs material behaviour (evidence summary)
- Canon draws the line in DU: thickness/texture/pores/scarring/weathering are "surface appearance" (DU L278); racial structure never mainly in normal maps/roughness/skin materials (DU L280). GO L541 and GR L491 add neutral-material / lighting identity tests; UCCA L214 "surface never compensates for structure".
- The only canonical *visible* consequence of tissue thickness is Grask ear translucency, framed as "observational surface phenomena" (GR L512).
- Bans on armor-skin and durability inference: GO L515 ("turning large anatomy into armor"), GR L512 ("combat role"), DU L359 ("has no gameplay effect"), SA L1405/L711, UCCA L357 ("No creator value feeds a gameplay stat"), REG L377 (elves not "less durable").

### Part 3 — Candidate classification (labelled suggestions)
- **Q3.1 DU/GR/GO skin thickness (biological).** Suggestion: **D** — explicitly OPEN biology (DU L359, GR L512, GO L515), with inference sources banned (skeleton, size, stature, mythology, coloration, combat role).
- **Q3.2 DU/GR/GO tissue durability (any effect).** Suggestion: **E** if ever pursued (gameplay/system), but current canon bans any effect (DU L359; UCCA L357) — so for the creator it is effectively a firewall, not a work item.
- **Q3.3 Visible surface texture (pores, fine lines, roughness, oiliness) DU/GR/GO/PI/CO.** Suggestion: **A** — already authored qualitatively (DU L358, GR L512, GO L515, CO L1754–1766); numeric/material realisation later (materials, DU L280).
- **Q3.4 Visible structural skin features from thickness (e.g. Grask ear translucency).** Suggestion: **C** (material/mesh validation; GR L512 frames it as observation).
- **Q3.5 Skin thickness for silent races (MF/SK/SG/FN/AE/VA/HV/PI/CO).** Suggestion: no question raised by canon; treat as **A** ("ordinary" — no differential claim) only if the author states it; otherwise leave SILENT. No spec claims a difference.

---

## 4. Register / review cross-checks (supporting history only)
- REG L29 "Sex-related anatomy for each non-human race | OPEN | Amendment v0.1 §4".
- REG L663 (GR), L800 (GO), L920 (PI) "sex-related anatomy and dimorphism | OPEN".
- REG L746 "Sex-related pigmentation and hair biology; normal scleral tint range | OPEN" (GR); REG L870 "Lifecycle; genetics; sex-related surface biology; technical surface architecture | OPEN" (GO). Note: sex-related *pigmentation* is also OPEN for GR (GR L564) and GO (GO L564) — outside this brief but adjacent.
- REG L954 PI "facial hair never required for adult or male recognition; sex-related facial-hair distributions OPEN" AGREED; REG L965 PI body hair AGREED; REG L972 PI "sex-related body and facial hair distributions" OPEN.
- REG L1051 CO hair/facial hair "PRELIMINARY"; REG L1057 CO body-hair/sex audit item OPEN; REG L1058 CO "body-hair frequencies" OPEN.
- REG L274 universal hair-not-locked-to-sex AGREED.
- SRR L110: "facial hair, scars, tattoos and age presentation cannot be assigned as mandatory racial separators."
- LRR: silent on sex, body hair, facial hair, skin thickness (grep `sex|female|male|dimorph|body hair|facial hair|skin thick|durab|like-for-like|reproduc` → 0 hits).
- IT3 L10: "The feminine normalized sheet confirms that the approved racial body relationships survive sex-related reference variation rather than depending on the masculine bodies." (level 5).

## 5. Gaps / inconsistencies noticed (factual)
1. PI Part 3 L383 ("Body-hair biology belongs to the later universal/race surface review") is stale relative to PI Part 4 L563 and UCCA L195 (PI bound).
2. CO L1819 "not determined by … sex-related anatomy" vs REG L1057 audit concern; spec L1821 already reserves soft sex correlations as OPEN.
3. MF and SK facial hair is written as presentation/controls (MF L181; SK L195, L228) with no explicit facial-hair *biology* statement, while UFCA slot 11 is "Facial-hair and eyebrow-hair biology" (UFCA L52). FN has no facial-hair statement at all (ECR L175 fills).
4. Like-for-like sex comparison is required for PI/CO/DU (and SRR) but no large-race, elven or human-family test matches on sex (SK L292, FN L78, GO L439/L735 list matched variables without sex).
5. UCCA L333/L135 require sex-related configurations per race even where race canon is SILENT; with R-SEX "no shift" (PR L94) those configurations may share body values, but the reference set still has to exist.
