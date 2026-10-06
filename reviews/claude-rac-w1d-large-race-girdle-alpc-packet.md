# RAC W1d — Skarn / Grask / Gorrund Shoulder-Girdle and Trunk Architecture Packet (incl. Gorrund ALPC)

**Author:** Claude (builder / auditor). **Order:** `reviews/chatgpt-rac-w1c-author-acceptance-blocker-resolution-order.md` §8 (work-order item 3, §11). **Status:** AUTHOR DECISION PACKET. Nothing here edits a race spec (order §7 last line applies by analogy; §12 canon firewall).
**Resolves (if accepted):** W1c gate blocker **B-4** ("Gorrund ALPC / structural mass not demonstrated; Grask and Gorrund shoulder girdles not authored", `reviews/claude-rac-w1c-author-acceptance-gate.md` L129).

**Citation keys (current HEAD line numbers):**
- **SK** `specs/skarn/SKARN_V1.md`; **GR** `specs/grask/GRASK_V1.md`; **GO** `specs/gorrund/GORRUND_V1.md`; **MF** `specs/marchfolk/MARCHFOLK_V1.md`
- **UCCA** `decisions/UCCA_V1.md`; **RA** `decisions/REFERENCE_ANATOMY_V1.md`
- **R2** `reviews/claude-pass2-r2-large-race-comparative-review.md` (the accepted Large-Race Comparative Review); **P2O** `reviews/chatgpt-pass2-author-closure-canonicalization-order.md` (its acceptance)
- **RAC-03/04/05** `reviews/claude-rac-0{3,4,5}-*.md`; **PH2** `reviews/chatgpt-reference-anatomy-closure-phase2-order.md`; **RMQ** `reviews/claude-pass2-r5-reference-mesh-queue.md`
- **W1c-M / W1c-A / W1c-G / W1c-B** `reviews/claude-rac-w1c-{measurements,cross-race-audit,author-acceptance-gate,build-method}.md`; evidence `reviews/rac-w1c-evidence/{SK,GR,GO,MF-M-R}_{meas,build}.json`

**Line-number note.** R2 was written at HEAD eb837b8 and cites the Gorrund Final Clarification as "GO L703–715" / "FC L701–731". At current HEAD the ALPC text is **GO L711–727** and the Durrim body distinction GO L729–739. This packet cites current lines; R2's content is unchanged.

**Labels used:**
- **CANON** — verbatim spec / accepted-decision text.
- **DERIVED** — a reading that follows from stated canon with no new biology (author confirmation recommended).
- **PROPOSAL — BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED** — new positive definition; not canon until accepted.
- **DIAGNOSTIC** — a value measured on a W1c generator candidate. Never canon (order §12; RA L88).

**Ground rules applied:** no invented numbers; no difference manufactured for silhouette (order §8, §12); Muscular Development Capacity (MDC), Current Muscularity and skeletal architecture kept separate (§5); AD-4 and AD-R15 undetermined pairs stay undetermined (§4).

---

## 1. Canon inventory

### 1.1 Accepted comparative orderings that this packet must preserve

| Source | Verbatim | Status |
|---|---|---|
| R2 L54 | "Thoracic / axial breadth (equal height or relative) \| S > MF (S L76) \| GR < S relative to stature (GR L203) \| GO > GR (GO L40, L236); GO > S "axial breadth" (GO L109, Part 1 only) \| **GO > S > GR**" | Canon ordering (accepted, R2 L153) |
| R2 L55 | "Thoracic depth \| S > MF (S L21, L75) \| "meaningful", non-directional vs Skarn (GR L38–39) \| GO > GR (GO L40); GO > S "greater axial depth" (GO L109, L237) \| GO > S; GO > GR; **S vs GR n.d.**" | Canon ordering |
| R2 L56 | "Shoulder architecture \| Broader clavicles and upper back (S L76) \| Less broad relative to height than Skarn; non-human scapula and clavicle (GR L41–42, L206) \| Substantial skeletal girdle, integrated into ALPC (GO L45, L709) \| S > GR (breadth); GO vs S **n.d.** (difference is architectural: human vs ALPC)" | Canon ordering; GO vs SK girdle **n.d.** |
| R2 L57 | "Pelvis \| "more substantial" (S L77) \| Distinct, non-human; morphology OPEN (GR L45, L208) \| Load-bearing, integrated with the axial body; OPEN (GO L49, L187, L711) \| Architectural difference only; morphology OPEN for Grask and Gorrund" | Pelvis handled by the separate §7 pelvic packet |
| R2 L63 | "Skeletal structural presence \| Robust (S L26) \| Leverage, not compact mass (GR L23, L31) \| "Massive" = skeletal structural scale (GO L19, L76) \| Qualitative: GO and S high, GR rangy. GO vs S is a difference of degree and architecture" | Canon |
| R2 L73–77 | "**Skarn–Gorrund:** **no proportional ordering exists** apart from axial depth and breadth at equal height. Canon separates them by **architecture**: human skeletal family vs non-human ALPC; …" | Canon framing |
| RAC-05 L32 | "**Cross-race orderings already canon** (no new direction): … large-race thoracic breadth GO > SK > GR (R2 L54); thoracic depth GO > SK, GO > GR (R2 L55); joint scale GO > GR (R2 L61)." | Accepted (PH2 §3 L71) |
| RAC-05 L34 | "**Left undetermined (C, not authored):** SK vs GR thoracic depth; SK vs GO and SK vs GR joint scale (R2 L55, L61)." | Undetermined |
| RAC-05 L63 | "AD-R15 \| Keep SK–GR and SK–GO joint/depth orderings **undetermined** until measured (no authored direction)" | Accepted; **see AD-G13 (wording ambiguity)** |
| PH2 L127–128 | "- Skarn–Gorrund torso/limb separation where intentionally undetermined; - SK–GR / SK–GO joint/depth orderings without measurement;" (under "OPEN items that must remain OPEN") | Must stay OPEN |
| P2O L44–49 | "### AD-4 — APPROVED / Skarn–Gorrund torso/limb proportional separation remains **undetermined by design** where canon does not order it. / Their distinction is allowed to remain architectural: human skeletal family versus Gorrund ALPC/load-bearing non-human architecture, plus established craniofacial/auricular differences. / Do not invent a new Gorrund torso-share or limb-share relationship to Skarn merely to create another axis." | Binding |
| P2O L24 (AD-1) | "The test must pass on proportional/architectural carriers — thoracic depth relative to stature/breadth, ALPC, craniofacial identity and ear architecture — never absolute size or Current Muscularity." | Binding |
| P2O L28 (AD-2) | "The shortest-limbed valid Grask must remain Grask through non-limb carriers including relative thoracic/shoulder organization, non-human girdle/pelvic organization, neck relationship, hand/digit relationships, craniofacial verticality and ear architecture." | Binding — makes the GR girdle an identity carrier that must exist positively |
| GO L679 | "**Skarn–Gorrund torso and limb proportional separation is undetermined by design (AD-4):** their distinction is architectural — the human skeletal family versus Gorrund Axial Load-Path Continuity and load-bearing non-human architecture, plus the established craniofacial and auricular differences — and no Gorrund torso-share or limb-share relationship to Skarn is defined." | Canon |
| RA L131 | "Grask span > Marchfolk and Skarn and > Gorrund (direction only)" | Canon (span is DER from shoulder + segments) |

### 1.2 Skarn (SK)

| Topic | Verbatim (SK) |
|---|---|
| Identity | L7 "Skarn are biologically human: a naturally larger, heavier, more powerfully built population than Marchfolk. They are not scaled-up Marchfolk and not automatically muscular." |
| Girdle / clavicle | L21 "broader clavicles"; L76 "broader clavicles, a wider and deeper ribcage, and a broader upper back" |
| Girdle as system; joint placement | L90 "Shoulders, clavicles, chest, upper back and neck act as one connected system, with no simple mesh stretching. Wider shoulders keep believable shoulder-joint placement. Deeper chests change ribcage volume, not just surface muscle." |
| Girdle links | L112 "Shoulder width moves the upper back and clavicles."; L113 "Chest depth changes ribcage volume."; L284 "Results respect the anatomical links: shoulders and ribcage, pelvis and upper-leg alignment, …" |
| Thorax | L22 "a deeper ribcage and more thoracic volume"; L75 "a slightly larger torso share of total height and greater torso depth" |
| Neck base / pelvis | L23 "a more substantial neck base and pelvis"; L77 "a thicker neck base and a more substantial pelvis" |
| Lower axial trunk / load | L94 "The pelvis, hips, thighs, knees, calves, ankles and feet plausibly carry the greater mass at every setting. There is no default "huge upper body, tiny legs" silhouette." |
| Pelvis link | L114 "Pelvis width sets upper-leg alignment." |
| Robusticity / MDC | L26 "greater skeletal robustness and a higher Muscular Development Capacity (biological range; Current Muscularity stays free, §5)"; L80 "a higher Muscular Development Capacity (not a default Current Muscularity)" |
| Composition | L36 "Composition is independent of frame … Muscle modifies Skarn anatomy rather than creating racial identity." |
| Frame | L32 "A Narrow Skarn is still structurally Skarn. A Broad Skarn can be extremely substantial but stays visibly distinct from Gorrund." |
| Prohibition (cross-race) | L300 "The three are never differently scaled versions of one anatomy. Skarn are large, robust humans. Gorrund are giant-kin on their own anatomical foundation. Even extreme Skarn settings must not recreate Gorrund anatomy." |
| Grask pointer | L302 "Skarn–Grask separation is carried by the Grask spec … This pointer adds no Skarn anatomy (Pass 2 AD-5)." |
| ALPC | none (Skarn spec does not use the term; correct — ALPC is Gorrund-specific) |
| Scapula | not named (human family implied by L7, L300) |

### 1.3 Grask (GR)

| Topic | Verbatim (GR) |
|---|---|
| Identity | L9 "…elongated, rangy skeletal architecture, substantial functional reach, a relatively slender skeletal silhouette for its stature (a skeletal proportion, not low body fat; §6–7)…"; L11 "…distinct shoulder and pelvic architecture…"; L23 "**Elongated skeletal leverage and reach rather than compact structural mass.**" |
| Absolute vs relative | L31 "…bones and joints may be substantial in absolute terms while looking relatively lean compared with total height, so **absolute structural size** and **structural size relative to stature** always stay distinct." |
| Thorax | L38 "Moderate skeletal breadth, meaningful thoracic depth, a relatively elongated but not oversized ribcage and strong spine-shoulder integration; not a barrel, extremely narrow, flat or giant muscular chest, with breadth and depth independently variable" |
| Thoracic depth | L39 "Enough thoracic depth to be credible at Grask stature, without converging on Durrim-like proportional depth or Skarn-like human power architecture (comparative distributions need validation)"; L204 "Meaningful: never paper-thin for a rangy look, and never approaching Durrim proportional depth" |
| Shoulders (girdle) | **L41** "A race-specific relationship: moderate absolute-to-substantial breadth, long upper-limb integration, structure supporting extended reach and scapular and clavicular relationships distinct from humans, never simply widened human shoulders (exact morphology to develop)" |
| Shoulder breadth vs stature | **L42** "Can be large in absolute terms while looking less broad relative to height than Skarn; never classified "small" just because the silhouette is rangier" |
| Neck / transition | L43 "Supports tall stature, head stabilization, shoulder transition and broad variation, trending **moderate-to-long relative to Durrim and Skarn**; no swan-neck caricature, forward monster neck or permanent hunch" |
| Spine | L44 "…spinal curvature is never the source of troll identity, and a neutral Grask stands without hunch, stoop or crouch" |
| Pelvis | L45 "…exact morphology **OPEN**, never a narrowed or scaled human pelvis"; L208 "**Grask pelvis geometry must coordinate long lower limbs, upright bipedal locomotion and the Grask torso without being created by simply scaling or narrowing a human pelvis.**" |
| Torso share | L37 "…lower contribution to standing height than Marchfolk and Skarn … never a tiny torso on giant limbs"; L198 "…**proportionally reduced torso contribution** never means **small torso**." |
| Ribcage | L202 "Functional at large body size, with independent skeletal breadth, depth, vertical length, lower-rib relationship and taper; never a human ribcage stretched vertically" |
| Thoracic breadth | L203 "May be substantial in absolute terms at reference height, but generally reads less broad relative to stature than Skarn, surviving composition neutralization" |
| Shoulders (Part 2) | **L205** "Evaluated as absolute skeletal breadth, breadth relative to torso, breadth relative to stature and relationship to arm origin, never one Shoulder Width concept" |
| Scapulae and clavicles | **L206** "Support long functional arms while preserving upright posture, large movement ranges and arms that don't look dislocated, visibly distinct from widened human clavicles; no ape-like shoulder invented to justify reach (exact morphology for later prototyping)" |
| Span | L225 "Arm span emerges from shoulder architecture, upper-arm, forearm and hand length, never one Arm Span slider." |
| Coordination | L174 "Grask identity emerges from coordinated relationships among torso, pelvis, femur, lower leg, shoulder, upper arm, forearm, hands and feet, never by maximizing every limb segment at once…" |
| Frame | L70 "**Broad** may increase thoracic, shoulder and pelvic skeletal breadth and joint and base dimensions, but isn't Skarn, muscular, fat or maximum everything."; L249 "A **Broad** Grask stays rangy, avoiding Skarn convergence, Gorrund assumptions, a blocky torso and visually shortened limbs." |
| Muscle vs skeleton | L72 "Muscle and fat wrap the approved skeleton without redefining it (pectorals don't change thoracic breadth, abdominal fat doesn't change the pelvis, shoulder muscle doesn't move the shoulder joint)" |
| MDC | L72 "**Muscular Development Capacity** (the biological range) stays separate from **Current Muscularity**, and whether Grask capacity differs from humans is **OPEN**, never inferred from silhouette."; L251 "Whether Grask muscular-development capacity differs from humans stays **OPEN**, and long visible muscles never imply greater strength or capacity." |
| AD-2 test | L716 "The Grask stays Grask through non-limb carriers: thoracic and shoulder breadth relative to stature, non-human girdle and pelvic organization, neck relationship, hand and digit relationships, craniofacial verticality and ear architecture" |
| Prohibitions | L11 "…avoids gorilla caricature, ape posture, a hunched monster silhouette, a giant human silhouette, an extremely narrow stick figure and a bodybuilder troll."; L100 "High muscle \| Fails if it becomes Skarn with longer arms"; L318 "**Do not allow Grask variation to pre-design or presume the anatomy of an unfinished population.**" |
| ALPC | none (correct — Gorrund-specific) |

### 1.4 Gorrund (GO)

| Topic | Verbatim (GO) |
|---|---|
| Identity | L9 "…massive load-bearing skeletal architecture, high absolute structural scale, broad/deep body organization, substantial joints and strong axial-to-limb integration. Their identity comes from skeletal construction, not from mandatory muscularity, obesity, ugliness or exaggerated monster anatomy." |
| "Massive" | L19 ""Massive" means biological structural scale first (skeletal breadth and depth, joint dimensions, axial scale, pelvic structure, limb-bone structural dimensions), never automatically muscular, fat or heavy-looking from clothing." |
| Axial skeleton | L39 "A major identifier: broad skeletal thorax, substantial thoracic depth, strong vertebral and torso integration, substantial shoulder girdle and pelvis, strong neck-to-torso integration; never a rectangular block" |
| vs Grask | L40 "…against Grask at equal height, greater skeletal breadth and depth, more axial presence and less dependence on limb elongation for stature…" |
| Thoracic breadth | L41 "Trends high: greater than Grask at matched height and, at equal height, greater axial breadth than Skarn … but never maximum width on everyone, a square torso or a bodybuilder V; Narrow-frame Gorrund stay valid"; L179 "…**the lower valid end of Gorrund thoracic breadth must still preserve Gorrund identity through depth, joints, axial integration and overall skeletal scale**" |
| Thoracic depth | L42 "**Gorrund trend toward substantial thoracic skeletal depth relative to stature and breadth, producing a genuinely three-dimensional load-bearing torso rather than a wide but shallow body**"; L180 "One of the strongest positive signals: meaningful front-to-back ribcage depth relative to stature, never a cylindrical barrel chest"; L181 "**Thoracic skeletal depth** (ribcage) stays separate from **abdominal soft-tissue projection**…" |
| Independence | L43 "Never one Torso Size or Body Thickness; breadth, depth, vertical contribution, muscle and adipose contribution stay separate"; L175 "Thoracic breadth, depth and vertical length, abdominal vertical contribution, waist skeletal relationships, and pelvic breadth and depth are independent, never one Torso Mass concept." |
| Ribcage | L44 "Coherent, never a barrel-chest caricature, a perfect cylinder or uniformly enlarged human ribs (morphology for prototyping)"; L182 "Anatomically shaped, never circular, rectangular or boxy"; L183 "Substantial enough to integrate the large torso, never just a widened and deepened short human ribcage"; L184 "Upper and lower breadth, taper and flare vary, with no universal V or barrel" |
| Shoulders (girdle) | **L45** "Substantial skeletal architecture from clavicular, scapular, thoracic and upper-arm relationships, never width alone; **skeletal shoulder breadth** stays separate from **deltoid and trapezius development**, so low-muscle Gorrund can have very broad skeletal shoulders"; **L187** "Skeletal breadth, clavicular contribution, scapular relationship, joint placement and thorax-to-arm transition are separate, never external circumference as the measure" |
| Shoulder-to-pelvis | **L188** "Continuous variation from more shoulder-dominant through balanced to more pelvis-present, not subtypes" |
| Neck | L46 "…**moderate vertical neck contribution with high structural integration into the shoulder/torso complex**…"; L192 "…a low-muscle Gorrund still has substantial skeletal neck integration, never dependent on trapezius" |
| Spine | L48 "Upright bipedal neutral alignment, never a required hunch…"; L191 "…without permanent forward lean, exaggerated lumbar arch or hunch" |
| Pelvis | L49 "…never a uniformly enlarged human pelvis"; L189 "**Gorrund pelvises possess substantial load-bearing skeletal dimensions and strong integration with both the deep axial torso and large lower limbs**, with meaningful breadth, depth and hip-joint scale; exact morphology **OPEN**. Not every pelvis is extremely broad, and a narrower valid pelvis still supports large hip joints and femora, upright gait and axial integration"; L190 "Skeletal pelvic breadth, gluteal muscle and regional fat stay separate; external hip circumference is never a proxy" |
| Waist / abdomen | L185 "Varies within valid anatomy; narrower isn't human or bodybuilder, broader isn't obese or unfit"; L186 "External shape comes from skeleton, muscle, fat amount and distribution and posture; no "ogre belly"" |
| Combined validity | L119 "…(maximum height, torso breadth and depth with the smallest joints; narrowest frame and minimum joints at maximum height; **broadest shoulders on the narrowest pelvis without transition**; maximum skeletal breadth, muscle and fat without spatial validation)." |
| Axial definition | L167 "…"Axial" means structural emphasis through spine, ribcage, shoulder girdle, pelvic integration and torso-to-limb transitions, never a torso that visually overwhelms the limbs." |
| Core principle | L165 "**Gorrund anatomy must read as a coordinated massive load-bearing skeletal system, not as a human body enlarged uniformly or as independent width/depth sliders applied to a generic humanoid.**" |
| Chains | L232 "…Shoulder-joint scale, upper-arm structure and thorax stay compatible, and pelvis, hip, femur and knee work as one biomechanical chain, especially at maximum height and Broad frame." |
| Joints | L74 "**Substantial joint structural presence appropriate to large load-bearing bones, without exaggerating the joints into monstrous anatomy.**"; L76 "This is one of the strongest body signals across shoulders, elbows, wrists, hips, knees and ankles. Long bones have greater absolute cross-sectional structural scale than smaller humanoids, with no numbers yet…" |
| Frame | L80 "**Narrow** Gorrund keep axial depth, load-bearing scale, substantial joints and Gorrund integration, never becoming Grask, Skarn or a giant human. **Broad** Gorrund stay plausible, avoiding maximum width everywhere, a rectangular torso and automatic muscle or obesity."; L220 "**Narrow** Gorrund may reduce relative thoracic, shoulder and pelvic breadth within valid limits but keep meaningful thoracic depth, substantial joints, large long-bone scale and strong axial integration."; L222 "**Narrow skeletal breadth does not automatically mean low skeletal depth.**"; L224 "…**broad frame never hard-links to maximum thoracic depth**… about 208 cm with a Broad frame stays Gorrund without becoming Skarn…" |
| Muscle / MDC | L21 "**Gorrund skeletal massiveness exists independently from Current Muscularity and Body-Fat Amount.**"; L82 "Whether their muscular-development capacity differs from humans or other races is **OPEN**, never inferred from skeletal scale. High-muscle Gorrund stay Gorrund, but muscle is never the only reason they look massive, and neutralizing muscle preserves identity."; L228 "Whether Gorrund have a different muscular-development ceiling or distribution is **OPEN**, never settled from appearance."; L703 OPEN list includes "muscular-development capacity" |
| Equal-height Skarn | L239 "Skarn: human skeletal family, powerful large-human relationships, the already-approved higher Muscular Development Capacity (not a default Current Muscularity), human cranial and body foundation. Gorrund: a distinct non-human load-bearing system with greater axial depth and structural scale beyond "big human" and distinct joint, torso and pelvis relationships. Fails as "extra-broad Skarn"" |
| AD-1 test | L271 "Passes only on proportional and architectural carriers: thoracic depth relative to stature and breadth, Axial Load-Path Continuity, craniofacial identity (Transverse Structural Continuity) and ear architecture. Fails if it relies on absolute size or Current Muscularity" |
| AD-3 reciprocal | L244 "The Gorrund stays Gorrund through body architecture: lower relative limb contribution than the Grask distribution, greater axial contribution, joint presence and Axial Load-Path Continuity. Ears, face, surface phenotype, muscle and absolute height never rescue an otherwise collapsed body architecture." |
| Composition tests | L243 "Composition-neutral recognition (GOR-BODY-16, neutral pose and presentation) \| Fails if it needs muscle bulk or fat volume to read Gorrund"; L683 "…fails if Gorrund need more muscle to be distinguished" |
| Durrim distinction | L737 "Not compact: substantial ribcage vertical length and large axial vertical contribution suited to a tall body, so a Gorrund is never a vertically scaled Durrim" |

**ALL ALPC text (GO L711–727, L735, L739, L743, L745; plus UCCA):**

> GO L713 "Massive load-bearing architecture, broad and deep axial construction, substantial shoulders and pelvis, large joints and long bones can overlap Durrim conceptually, and absolute size isn't a sufficient positive distinction, so a Gorrund-specific body relationship is added:"

> GO L715 "**Gorrund possess pronounced axial load-path continuity: the shoulder girdle, thoracic structure, lower axial trunk, pelvis and proximal lower limbs form a strongly integrated vertical load-bearing chain, with skeletal transitions that preserve substantial structural continuity from the upper torso through the pelvis into the legs.**"

> GO L717 "**Axial Load-Path Continuity** is project anatomical terminology, not a creator-facing slider. The body reads as one load-bearing system, **shoulder girdle → thorax → lower axial trunk → pelvis → hip and proximal femur**, visually and biomechanically communicating continuous support rather than individually enlarged regions attached together. It never means uniform torso width, no waist, a rectangular or barrel body, a giant pelvis or shoulders, a thick abdomen, high fat or muscle, column-shaped legs or one "massiveness" slider."

| GO line | Transition | Requirement (verbatim) |
|---|---|---|
| L721 | Shoulder to torso | "The substantial shoulder girdle integrates with the thorax, never huge shoulders on a comparatively ordinary torso as the racial recipe" |
| L722 | Thorax to lower trunk | "The broad, deep thorax transitions without abrupt skeletal collapse, while visible waist definition, narrower frames, low fat and athletic composition stay valid; the relationship is skeletal load paths, not circumference" |
| L723 | Lower trunk to pelvis | "The pelvis reads as integrated with the axial body, not an independently widened hip structure; morphology stays **OPEN** but its relationship to the torso is now positively constrained" |
| L724 | Pelvis to leg | "Hip-joint scale, proximal femur, pelvis and upper-leg dimensions suit receiving load from the pelvis and axial skeleton, never mandatory enormous thighs" |
| L725 | Narrow frame | "Keeps the continuity: reduced breadth never removes thoracic depth, joint scale, pelvic and proximal-limb integration or structural continuity (a critical identity test)" |
| L726 | Low muscle | "The continuity is especially readable through skeleton; it fails if it appears only once muscle is added" |
| L727 | Fat | "Low fat reveals rather than creates the structure; high fat may soften the silhouette without eliminating the skeletal relationships" |

> GO L735 (Durrim vs Gorrund) "**Axial load-path continuity** across shoulder girdle, thorax, lower trunk, pelvis and proximal lower limbs within a massive tall-body architecture"
> GO L739 "…Gorrund axial load-path continuity, greater vertical axial development, fully substantial tall-body limb contribution and distinct shoulder-thorax-pelvis-proximal-leg integration; identical silhouettes after normalization fail. **Equalized torso-breadth test:** … never breadth alone."
> GO L743 "**Their massive body architecture is further distinguished by axial load-path continuity: coordinated structural integration from the shoulder girdle through the thorax and lower axial trunk into the pelvis and proximal lower limbs. This separates Gorrund from Durrim compact structural concentration as well as from Grask limb-dominant reach specialization and Skarn large-scale human anatomy.**"
> GO L745 "**Axial Load-Path Continuity** (body) and **Transverse Structural Continuity** (face) describe different anatomical systems and never collapse into one universal Gorrund slider…"
> UCCA L92 "…no master race-proportion sliders (… ALPC, LSCTA, FSEA or equivalent)."; UCCA L131 "…(… Narrow Gorrund keeps ALPC; …) stay hard."
> RMQ L32 "RM-LR-06 \| P2 \| Axial Load-Path Continuity proxies: girdle → thorax → pelvis breadth and depth continuity profile (cross-section series along the trunk) \| Gorrund reference and Narrow; Skarn Broad \| LR-01–04; GO FC"
> RMQ L28 "RM-LR-02 \| P1 \| Thoracic depth ÷ stature; thoracic depth ÷ thoracic breadth; shoulder breadth ÷ stature \| Same, plus Narrow and Broad presets \| LR-01, LR-04"

### 1.5 Universal rules that bind this packet

| Source | Verbatim |
|---|---|
| UCCA L119 | "Skeletal Frame is the continuous configuration of a character's skeletal breadth, depth, joint and robusticity variables (shoulder/clavicular breadth, thoracic width, thoracic depth where bound, pelvic width and depth where canon names it, joint scale, long-bone robusticity, plus race-specific extras)…" |
| UCCA L154 | "**Five-way separation:** Muscular Development Capacity ≠ Current Muscularity ≠ Body-Fat Amount ≠ Body-Fat Distribution ≠ Skeletal Frame. Soft-tissue fullness, circumference and visible mass are DER." |
| UCCA L156 | "**Hard rules:** composition never edits the skeleton; thoracic depth is never faked by fat or muscle; pelvic breadth is never fat; frame never edits composition." |
| UCCA L161–164 | "- Capacity is Biological Anatomy and sets the valid ceiling of Current Muscularity (CLAMP). … - Where the population distribution is OPEN (Grask, Gorrund, Pipkin, Cogling), **no population shift is invented.**" |
| RA L35 (R-4) | "**Current Muscularity and Body-Fat Amount at the population centre, neutral (untilted) fat distribution, no regional muscle offsets.** … **Reference composition is a measurement state, never a body preset…**" |
| RA L84–88 | "A mesh built from **numeric targets chosen by a builder** … returns those targets when measured. Measuring it **cannot discover** canon … **No measured value becomes canon merely because a candidate mesh embodies it.**" |
| RA L106 | "Directional canon … is a **constraint the measurement must satisfy**, never permission to invent a magnitude." |
| RA L127–128 | "J-4 \| Bone robusticity never follows muscularity"; "J-5 \| Thoracic depth and breadth are independent; narrow never implies shallow" |
| RA L124 | "Curvature is never a racial identity carrier, except Vael's "natural lumbar curve". ARMs use neutral adult curvature" |
| MF L15 | "…Marchfolk keep recognizably human skeletal and cranial architecture, shoulders, ribcage, spine, pelvis…" |
| MF L83–86 | "**Shoulder width:** clavicles, upper back and shoulder-joint position." / "**Chest depth:** ribcage and upper-torso structure." / "**Waist:** smooth transitions through the abdomen and lower torso." / "**Hip width:** pelvis structure and upper-leg alignment." |
| Order §3 | "Accept the current FAL/Pr/Po* proxy definitions, +/-0.010 approximate-comparison tolerance, and 1% marginal threshold for this pass." |

### 1.6 Current diagnostic state (W1c; DIAGNOSTIC — not canon)

- GO candidate = MakeHuman generic human mesh at 229 cm with trunk targets `torso-scale-depth-incr 0.8`, `torso-scale-horiz-incr 0.7`, `measure-shoulder-dist-incr 0.45`, `hip-scale-horiz-incr 0.3`, `hip-scale-depth-incr 0.3` (`GO_build.json`). That is, a **human trunk with independent width/depth multipliers per region** — exactly the construction GO L165 excludes ("independent width/depth sliders applied to a generic humanoid"). GR candidate = human trunk with `torso-scale-horiz-decr 0.1` and human scapula/clavicle (`GR_build.json`).
- W1c-M L144 "RM-LR-06 (ALPC) \| GO \| **Not demonstrated** (qualitative; the evidence sheet reads lean)". W1c-G L129 B-4.
- W1c-A L148 row 94 "thoracic breadth GO > SK \| RAC-05 L32 \| 0.197 \| > \| SK 0.197 \| PASS" — marginal (0.09 %, W1c-G L96): **not demonstrated**.
- Trunk profile shape computed from the W1c rest-geometry values already in `*_meas.json` (skin surface, soft tissue included, generator joints; ratios to each body's own maximum thoracic breadth TB / depth TD):

| Ratio (DIAGNOSTIC) | MF-M-R | SK | GR | GO |
|---|---|---|---|---|
| shoulder-joint breadth ÷ TB | 1.123 | 1.137 | 1.124 | **1.147** |
| waist breadth ÷ TB | 0.847 | 0.815 | 0.854 | **0.802** |
| iliac-crest-proxy breadth ÷ TB | 0.869 | 0.836 | 0.882 | **0.822** |
| bitrochanteric ÷ TB | 1.010 | 0.971 | 1.032 | **0.946** |
| hip-joint spacing ÷ TB | 0.667 | 0.636 | 0.681 | **0.622** |
| waist depth ÷ TD | 0.843 | 0.786 | 0.845 | **0.782** |
| pelvic AP depth ÷ TD | 0.971 | 0.870 | 0.953 | **0.864** |

  **Reading (diagnostic, flagged):** relative to its own thorax, the GO candidate has the *widest girdle overhang* and the *largest drop* from thorax to lower trunk and pelvis of the four bodies — i.e. a large thorax on a proportionally ordinary-to-small lower trunk and pelvis. Its normalized lower-trunk profile is *less* continuous than the human reference. This is the GO L721 anti-pattern ("huge shoulders on a comparatively ordinary torso") extended downward, and is the measurable form of "not demonstrated". **Caveats:** skin-surface values include soft tissue at R-4 composition; hip-joint spacing is the generator rig (W1c-B L78), not femoral-head scale; mesh edge ~0.7 cm (W1c-B L98). None of these numbers is proposed as a target.

---

## 2. What canon defines vs what is missing (girdle and trunk)

| Race | Canon already defines (positive) | Missing / OPEN | Class |
|---|---|---|---|
| **SK** | Human skeletal family (L7, L300). Broader clavicles and upper back than MF (L21, L76). Girdle–chest–upper back–neck as one system; shoulder width moves clavicles/upper back; wider shoulders keep believable joint placement (L90, L112). Deeper/wider ribcage, greater torso depth (L22, L75, L76). Lower body carries the mass, no top-heavy default (L94). | Scapular morphology not named — **human by family** (DERIVED; no gap). Which pelvic dimension "more substantial" means (RAC-03 L26; pelvic packet scope). | **Sufficient** for the girdle (§3d) |
| **GR** | Girdle is race-specific and non-human (L11, L41, L206, L716). Breadth: absolute moderate-to-substantial, relative-to-stature < SK, never "small" (L41–42, L203). Four separate shoulder readings (L205). Functional constraints: long functional arms, upright posture, large movement ranges, arms not dislocated, strong spine-shoulder integration (L38, L206). Two bans: "never simply widened human shoulders" (L41) / "visibly distinct from widened human clavicles" (L206); "no ape-like shoulder invented to justify reach" (L206). Span DER from shoulder architecture (L225). Elongated, not oversized, ribcage (L38, L202). | **The positive morphology itself:** L41 "exact morphology to develop"; L206 "exact morphology for later prototyping". Canon says what the girdle must *do* and what it must *not be*, but nowhere *what it is*. No direction for "breadth relative to torso" or "relationship to arm origin" (L205 names the readings, no directions). GR vs MF shoulder breadth relative to stature: **silent**. | **Canon authorship needed** (§3a) |
| **GO** | Substantial skeletal girdle; clavicular, scapular, thoracic and upper-arm relationships; skeletal breadth ≠ deltoid/trapezius (L39, L45, L187). Girdle is the first link of ALPC; must integrate with thorax, never "huge shoulders on a comparatively ordinary torso" (L715–721). Shoulder-joint scale ↔ upper-arm ↔ thorax compatible (L232). Neck highly integrated into shoulder/torso complex, skeletally (L46, L192). Shoulder-to-pelvis continuous variation (L188). Broadest shoulders on narrowest pelvis without transition invalid (L119). Narrow keeps continuity (L725). | Girdle morphology: L159 OPEN list "ribcage, shoulder and pelvic morphology". No operational definition of ALPC: L715–727 give qualitative transitions; RMQ L32 names a proxy profile but no pass condition. "Abrupt skeletal collapse", "integrated", "independently widened" have no testable form. GO vs GR *girdle* breadth: implied by L40 "greater skeletal breadth" but not stated for the girdle. | **Canon authorship (girdle) + operational definition (ALPC)** (§3b, §3c) |

---

## 3. PROPOSALS

Every item in §3 is **PROPOSAL — BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED** unless labelled DERIVED. All are directional or relational. No magnitude is proposed; magnitudes come from builds declared under R-14 (RA L45) and accepted under RA §7.

### 3a. Grask shoulder-girdle relationships

**Design intent derived from canon:** a girdle *organized for reach on an elongated, moderately broad, meaningfully deep thorax*, distinct from a human girdle by **organization**, not by width — because canon both bans "simply widened human shoulders" (GR L41) and sets breadth relative to stature below Skarn (GR L42, L203). Breadth therefore cannot be the carrier of Grask girdle distinctness; the carrier must be arrangement.

| ID | PROPOSAL — BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED | Derives from | Rejected alternatives (and why) |
|---|---|---|---|
| **GR-G1** Breadth mechanism | Grask girdle breadth **follows the Grask thorax** (moderate breadth): shoulder breadth relative to thoracic breadth is **not raised above the human (MF) relationship as the means of obtaining shoulder breadth**. The girdle is not a human girdle with lengthened clavicles. | GR L41 "never simply widened human shoulders"; L206 "visibly distinct from widened human clavicles"; L42/L203 relative breadth < SK; L38 moderate breadth | Wider-than-human clavicular overhang: is the banned "widened human" recipe and pushes toward Skarn (L249 "avoiding Skarn convergence"). |
| **GR-G2** Vertical scapular organization | The scapular blade is **vertically extended along the relatively elongated ribcage** (superior-to-inferior extent relative to its own breadth greater than in the human reference), seated close to the thoracic wall with strong spine–scapula coupling (no winging), giving long muscle-attachment levers for the long upper limb. This is the primary positive "scapular relationship distinct from humans". | GR L38 "relatively elongated but not oversized ribcage and strong spine-shoulder integration"; L41 "long upper-limb integration, structure supporting extended reach and scapular and clavicular relationships distinct from humans"; L202 ribcage vertical length independent; L206 large movement ranges, upright posture | (i) Laterally/anteriorly rotated glenoid for reach: approaches "ape-like shoulder invented to justify reach" (L206). (ii) Elevated/shrugged girdle: conflicts with "no … permanent hunch" posture reads (L43–44) and would carry identity through posture (RA L124 spirit). Both listed for completeness; **not recommended**. |
| **GR-G3** Arm origin | The glenohumeral arm origin sits so that the long, hanging arm in R-6 clears the thoracic wall **without increasing the 8° measurement abduction** and without a visible step at the shoulder ("arms that don't look dislocated"). Arm origin is lateral enough for clearance, never by an overhanging acromial shelf. | GR L205 "relationship to arm origin"; L206; order §3 (8° is the W1c stance convention) | Clearance by widening the girdle: violates GR-G1. |
| **GR-G4** Clavicle | Clavicle **length and orientation are a consequence of GR-G1/G3**, not an independent widener: a long, slender-relative-to-length but absolutely substantial clavicle (absolute vs relative per GR L31; J-3, RA L126), with the sternoclavicular end integrated into an upright neck base (moderate-to-long neck, L43). | GR L31, L43, L206; RA L126 (J-3) | Short, robust human-power clavicle: Skarn architecture (L39 "without converging on … Skarn-like human power architecture"). |
| **GR-G5** Girdle–neck transition | The girdle–neck transition is **upright and open** (the neck rises from the girdle, not from between elevated shoulders), consistent with moderate-to-long neck relative to SK and DU. Neck length is not raised to carry identity (L172). | GR L43, L172 | — |
| **GR-G6** Never Gorrund-like / never scaled human | (a) No ALPC-type continuity is required or implied for Grask (ALPC is Gorrund-specific, GO L743); (b) Grask girdle breadth relative to stature stays **below SK** (canon) and therefore below GO (DERIVED, §4); (c) a uniformly scaled human girdle (MF shape ratios at 218 cm) **fails** GR-G2 by construction. | GR L41, L42, L316–318; GO L40, L743 | — |
| **GR-G7** GR vs MF breadth relative to stature | **No direction authored.** Canon is silent; "never classified "small"" (L42) is a read requirement, not an MF ordering. Measured value is reported only. Author may decide (AD-G4). | GR L42 | Authoring GR ≥ MF or GR ≤ MF would manufacture an axis. |
| **GR-G8** Frame behaviour | Narrow/Broad write girdle and thoracic breadth **together** (GR-G1 preserved across frames); Broad never produces Skarn-like girdle overhang or a "blocky torso" (L249). GR-G2 scapular organization is not a frame variable (morphology, not breadth). | GR L70, L249; UCCA L119, L129 | — |

**Uncertainty flag:** GR-G2 is the one proposal that commits to a *shape*. It is the minimum positive morphology that satisfies L41/L206 without breadth and without ape-likeness. If the author prefers to keep scapular shape OPEN, the minimum alternative is GR-G1 + GR-G3 + GR-G4 only, with GR-G2 replaced by "scapular relationship distinct from humans, morphology at builder's choice, declared under R-14". That leaves the AD-2 "non-human girdle organization" carrier untestable (AD-G2).

### 3b. Gorrund shoulder-girdle relationships (consistent with ALPC)

| ID | PROPOSAL — BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED | Derives from |
|---|---|---|
| **GO-G1** Girdle carried by the thorax | Gorrund girdle breadth is **carried by thoracic breadth and depth, not by girdle overhang**: shoulder-joint breadth ÷ thoracic breadth is **not greater than the human (MF) relationship**. Large absolute shoulder breadth comes from the large thorax. | GO L721 "never huge shoulders on a comparatively ordinary torso as the racial recipe"; L45 "never width alone"; L41 "never … a bodybuilder V"; L717 "never … a giant pelvis or shoulders" |
| **GO-G2** Girdle wraps a deep thorax | The scapulae are seated on a **deep, posterolaterally broad ribcage**; the glenoid / arm origin sits within the thoracic depth envelope (the arm hangs at mid-thoracic depth, not behind or in front of the chest wall). The girdle's anteroposterior placement follows thoracic depth. | GO L42, L45 "clavicular, scapular, thoracic and upper-arm relationships", L187 "joint placement and thorax-to-arm transition are separate" |
| **GO-G3** Clavicle and girdle joints | Clavicle with **substantial cross-section** for its length; sternoclavicular and acromioclavicular joints and the glenohumeral joint share GO joint presence (no tiny shoulder articulation under a large thorax). Shoulder-joint scale ↔ upper-arm structure ↔ thorax compatible. | GO L74, L76 (joint presence incl. "shoulders"), L232 |
| **GO-G4** Neck–girdle integration | Broad skeletal **neck base integrated into the girdle and upper thorax** (cervicothoracic junction substantial), readable at low muscle; never produced by trapezius. | GO L46, L192; L726 |
| **GO-G5** Shoulder-to-pelvis variation | The girdle–pelvis breadth relation varies continuously (shoulder-dominant ↔ pelvis-present) **within** ALPC-2/ALPC-4 (§3c). Extremes that break continuity (L119 "broadest shoulders on the narrowest pelvis without transition") are invalid. | GO L188, L119 |
| **GO-G6** Frame | Narrow reduces girdle, thoracic and pelvic breadth **coherently**; depth, joint scale and continuity stay (ALPC holds on resolved values). | GO L220, L222, L725; UCCA L131 |
| **GO-G7** GO vs GR girdle | **DERIVED:** GO girdle (skeletal shoulder) breadth relative to stature > GR at matched height, from GO L40 "greater skeletal breadth" + R2 L54 thoracic GO > GR + GO-G1. Author confirmation requested (AD-G6). | GO L40; R2 L54 |
| **GO-G8** GO vs SK girdle | **Stays n.d. (R2 L56).** No breadth ordering between GO and SK girdles is authored. The SK/GO girdle difference is **architectural**: SK = human girdle at robust scale; GO = girdle as first link of ALPC (GO-G1/G2 + ALPC-4). | R2 L56; AD-4 (P2O L44–49) |

### 3c. Gorrund ALPC — operational definition

**Proposed definition (PROPOSAL — BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED):**
ALPC is demonstrated when the **normalized skeletal breadth and depth profile** of the axial chain — girdle → thorax → lower axial trunk → pelvis → hip / proximal femur — (i) has a valid humanoid shape (ALPC-0), (ii) carries proportionally **more** of the thoracic dimension down into the lower trunk, pelvis and proximal femur **than the human reference does** (ALPC-1…3), (iii) does not get its upper end from girdle overhang (ALPC-4), and (iv) keeps (i)–(iii) under Narrow frame and low composition (ALPC-5, ALPC-6). Every criterion is a **ratio to the body's own thorax**, compared **only in direction** with the MF reference profile shape. No number is set.

**Why "relative to the MF profile shape":** MF is the Human Reference Population (MF L15). A uniformly scaled human trunk has, by construction, **exactly the MF normalized profile**. GO L165 ("not as a human body enlarged uniformly") and GO L715 ("**pronounced** axial load-path continuity") together require the Gorrund normalized profile to differ from the human one *in the direction of continuity*. Comparing shape ratios — not sizes — means height, frame breadth and composition cannot satisfy the test by themselves.

**Stations (skeletal, measured on R-6 / rest geometry per D-W1c-1; external skeletal landmarks only per RA L122):**

| Station | Level | Breadth | Depth |
|---|---|---|---|
| S1 Girdle | glenohumeral / acromial level | biacromial (skeletal) and shoulder-joint breadth | thoracic AP at the same level |
| S2 Thorax max | maximum ribcage breadth | TB | TD (max ribcage AP) |
| S3 Lower thorax | inferior costal margin | lower-ribcage breadth | lower-ribcage AP |
| S4 Lower axial trunk | narrowest skeletal level between S3 and S5 (lumbar) | lumbar skeletal breadth proxy | lumbar AP (vertebral body + posterior elements proxy) |
| S5 Pelvis upper | iliac crest | bi-iliac breadth | pelvic AP at crest |
| S6 Pelvis–hip | hip-joint centres | inter-acetabular and bitrochanteric breadth | pelvic AP at hip-joint level |
| S7 Proximal femur | subtrochanteric | femoral shaft breadth; femoral head/neck scale | femoral shaft AP |

| Criterion | PROPOSAL (pass condition, relational) | Canon basis |
|---|---|---|
| **ALPC-0** Valid shape (necessary, not sufficient) | Breadth non-increasing S2→S4 and non-decreasing S4→S6; **at most one local minimum (at S4)** between S2 and S6; no local minimum at S5 (no pinch between waist and hips); no step at S1→S2. **At reference, S4 < S2** (some taper exists: ALPC is never "uniform torso width, no waist"). MF passes ALPC-0 too — it is a validity screen. | GO L717 (never uniform width / no waist / rectangular / barrel); L722 waist definition valid; L182 never rectangular or boxy |
| **ALPC-1** No abrupt skeletal collapse (thorax → lower trunk) | S3 ÷ S2 and S4 ÷ S2, **breadth and depth**, are **greater than MF's** corresponding ratios. | GO L715 "pronounced"; L722 "transitions without abrupt skeletal collapse … skeletal load paths, not circumference"; L183 ribcage "never just a widened and deepened short human ribcage" |
| **ALPC-2** Pelvis integrated, not independently widened (lower trunk → pelvis) | Two-sided: **(a) no collapse** — S5 ÷ S2 and S6 ÷ S2 (breadth) and pelvic AP ÷ TD are **not less than MF's**; **(b) no independent widening** — S5 ÷ S4 and S6 ÷ S4 (breadth) are **not greater than MF's**. Together: the pelvis is as large relative to the thorax as continuity carries it, and no larger relative to the lower trunk than in a human. | GO L723 "integrated with the axial body, not an independently widened hip structure"; L189 "strong integration with both the deep axial torso and large lower limbs"; L717 "never … a giant pelvis"; L49 "never a uniformly enlarged human pelvis" |
| **ALPC-3** Pelvis → proximal femur | Femoral head/neck scale ÷ S6 pelvic breadth and subtrochanteric shaft breadth ÷ femur length are **not less than MF's**. Thigh soft tissue excluded. | GO L724 "Hip-joint scale, proximal femur … suit receiving load … never mandatory enormous thighs"; L189 "hip-joint scale"; L76 cross-sectional scale; L232 chain |
| **ALPC-4** Girdle → thorax (= GO-G1) | S1 shoulder-joint breadth ÷ S2 TB **not greater than MF's**. | GO L721 |
| **ALPC-5** Frame invariance | ALPC-0…4 pass on **GOR-BODY-04 (Narrow) and GOR-BODY-12 (lower axial-breadth extreme)**, and depth criteria pass on **GOR-BODY-14** (lower thoracic-depth extreme) at least against MF. | GO L725 "a critical identity test"; L179; L222; UCCA L131 "Narrow Gorrund keeps ALPC" |
| **ALPC-6** Composition invariance | ALPC-0…4 pass on the **skeleton / skeletal proxy**, and the skin-surface profile of **GOR-BODY-16 (low muscle, low fat)** shows the same directions. A body that passes only at high muscle **fails**. Soft-tissue (bideltoid, waist circumference, gluteal) measures are never used. | GO L726, L727, L243; UCCA L156; GO L45, L190 |
| **ALPC-7** Separation from Skarn (AD-1 carrier) | On the equal-height Broad Skarn (RMQ L32 lists "Skarn Broad"; AD-1 heights), the GO ALPC-1 and ALPC-2(a) ratios are **greater than SK's**, beyond the 1 % marginal threshold (order §3). This is an **architecture** comparison, not torso or limb share, so it does not touch AD-4. | P2O L24 (ALPC as AD-1 carrier); GO L271; GO L743 "separates Gorrund from … Skarn large-scale human anatomy"; AD-4 allows architectural separation |
| **ALPC-8** Separation from Durrim (existing canon test, reused) | Matched-display silhouette test GO L739 applies; ALPC adds nothing new here beyond using the same stations. | GO L735–739 |

**Optional (lower confidence; AD-G9):**
- **ALPC-1b** Ribcage vertical length ÷ S2 breadth **not less than MF's** (ribcage not widened without lengthening). Basis: GO L183, L737 "substantial ribcage vertical length". Risk: none found against AD-4 (internal trunk organization, not torso share), but flag for author.
- **ALPC-1c** Costal-margin-to-iliac-crest skeletal gap ÷ torso length **not greater than MF's** (the "unsupported" lumbar span is not proportionally longer). Basis: L715 "strongly integrated vertical load-bearing chain". Risk: could press toward "no waist" (L717); recommended only as a report-only diagnostic.

**How this differs from a scaled human trunk (and from the current GO candidate):**
1. **Scaled human trunk:** every normalized ratio equals MF's → ALPC-1, -2(a), -3, -7 fail (equality is not "greater"). The criteria are immune to height.
2. **Independently enlarged regions** (the W1c construction: thorax depth/breadth targets + separate hip targets + shoulder target): passes or fails region by region with no continuity requirement. ALPC-2's two-sided form makes "enlarge the pelvis separately" fail (b) and "enlarge the thorax separately" fail (a). On the current W1c GO candidate, **ALPC-1 and ALPC-2(a) fail** on the diagnostic skin values in §1.6 in both rest and R-6 geometry; **ALPC-4 fails only on rest geometry** (shoulder-joint ÷ TB 1.147 vs MF 1.123) and passes on R-6 (1.190 vs 1.193), so it is not demonstrated either way (S4 ÷ TB 0.802 vs MF 0.847; pelvic AP ÷ TD 0.864 vs 0.971; shoulder ÷ TB 1.147 vs 1.123). This is consistent with W1c-M L144 "not demonstrated" and is a reason to rebuild, not a target.
3. **Not over-correction:** ALPC-0 and ALPC-2(b) exclude the opposite failures named in GO L717 (uniform width, no waist, barrel, giant pelvis). Waist definition remains valid (L722).
4. **Not a slider:** ALPC is a validator over resolved skeletal values, never a creator control (GO L717; UCCA L92).

**Measurement caveats (flag):** (a) W1c measures skin surface on a generator mesh with no skeleton; ALPC is "skeletal load paths, not circumference" (GO L722). A valid ALPC run needs either a modelled skeletal proxy (ribcage, lumbar column, pelvis, proximal femur) or, at minimum, the GOR-BODY-16 low/low skin profile alongside the reference. (b) The generator hip "joint" is a rig bone head (W1c-B L78); ALPC-3 needs femoral-head geometry. (c) The MF comparator must be the **accepted** MF-M-R (order §2) at R-4; its profile is the reference shape, not a target to exceed by a chosen amount.

### 3d. Skarn — sufficiency check

**Finding (DERIVED): canon is sufficient for the Skarn girdle and trunk.** Skarn are "biologically human" (SK L7) and "large, robust humans" (SK L300); the girdle is a **human girdle** at robust scale with broader clavicles and upper back (L21, L76), connected-system behaviour and believable joint placement (L90, L112), and a deeper/wider ribcage (L22, L76). No new Skarn authorship is proposed. Skarn is a formally accepted W1 asset (order §2); nothing here reopens it.

Notes (no proposal):
- **No ALPC for Skarn.** SK must not acquire Gorrund ALPC (SK L300 "Even extreme Skarn settings must not recreate Gorrund anatomy"); ALPC-7 tests this from the Gorrund side.
- **Informational (DIAGNOSTIC):** the accepted SK candidate also shows lower-trunk/pelvic ratios below MF (§1.6: waist ÷ TB 0.815, pelvic AP ÷ TD 0.870). SK L94 ("no default "huge upper body, tiny legs" silhouette") is about lower-body load-carrying, not trunk ratios, and has no numeric test; this packet does **not** propose one. It is recorded so that ALPC-7 is read against the SK values actually measured, and so the author can decide whether SK L94 needs a check (AD-G12).
- Remaining Skarn gap is pelvic only ("more substantial" dimension, RAC-03 L26) — pelvic packet scope.

---

## 4. SK / GR / GO comparisons at normalized height

### 4.1 Status of each pair and dimension

| Dimension | Canon ordering | Must stay undetermined | This packet |
|---|---|---|---|
| Thoracic breadth ÷ stature | **GO > SK > GR** (R2 L54; RAC-05 L32) | — | Test (RM-LR-02) |
| Thoracic depth ÷ stature | **GO > SK; GO > GR** (R2 L55; RAC-05 L32; GO L42, L239) | **SK vs GR** (R2 L55; RAC-05 L34) | Test GO pairs; SK–GR report only |
| Thoracic depth ÷ breadth | GO "relative to stature **and breadth**" (GO L42); used as AD-1 carrier vs SK (P2O L24) | SK vs GR (no canon) | **DERIVED** GO > SK, GO > GR (AD-G7); SK–GR report only |
| Shoulder (girdle) breadth ÷ stature | **SK > GR** (GR L42; R2 L56) | **GO vs SK** (R2 L56, architectural) | Test SK > GR; GO > GR DERIVED (GO-G7, AD-G6); GO–SK report only |
| Girdle overhang (shoulder ÷ thoracic breadth) | none | — | **PROPOSAL** GR ≤ MF (GR-G1), GO ≤ MF (GO-G1 / ALPC-4); SK no condition |
| Torso share; limb / arm / span share | GR < SK, MF; GO > GR; GR span > SK, GO (R2 L53, L58; RA L131) | **GO vs SK torso and limb share — by design** (AD-4; GO L679) | Not touched; RM-LR-01 rerun only |
| Joint scale | GO > GR (R2 L61; RAC-05 L32) | **SK vs GO; SK vs GR** (RAC-05 L34; AD-R15; PH2 L128) | Not touched (girdle joints: GO-G3 is within-GO) |
| ALPC profile | GO-specific (GO L715–743) | — | **PROPOSAL** ALPC-0…8; GO > SK on continuity ratios (ALPC-7) |

**Undetermined-by-design list (must stay without pass conditions; may be reported as diagnostics only):** GO vs SK torso share and limb/arm/span share (AD-4); SK vs GR thoracic depth (R2 L55); SK vs GO and SK vs GR joint scale (RAC-05 L34); GO vs SK girdle breadth (R2 L56). **AD-R15 ambiguity:** RAC-05 L63 reads "SK–GR and SK–GO joint/depth orderings", which can be read as making GO vs SK *depth* undetermined, contradicting the canon GO > SK depth (R2 L55, RAC-05 L32, GO L239). W1c applied both readings (W1c-A L29 "SK vs GO … depth/joints: no pass condition" vs row 96 GO > SK depth PASS). Recommended reading: AD-R15 covers exactly the RAC-05 L34 list (SK–GR depth; SK–GO, SK–GR joints). → **AD-G13**.

### 4.2 Proposed tests and pass conditions

All pass conditions: direction must hold **beyond the 1 % marginal threshold** accepted for this pass (order §3); a pass under 1 % is "not demonstrated" (W1c-G L96 convention). Bodies: accepted MF-M-R and SK; **rebuilt** GR and GO references; frame variants per RA L63.

**RM-LR-02 (extended)**

| # | Check | Pass condition | Basis |
|---|---|---|---|
| 02-a | TB ÷ H | GO > SK > GR | R2 L54 |
| 02-b | TD ÷ H | GO > SK; GO > GR | R2 L55 |
| 02-c | TD ÷ TB | GO > SK; GO > GR (if AD-G7 accepted) | GO L42; P2O L24 |
| 02-d | Skeletal shoulder breadth ÷ H (acromial or anatomical glenohumeral centres, not bideltoid) | SK > GR; GO > GR (if AD-G6) | GR L42; GO L40 |
| 02-e | Shoulder breadth ÷ TB | GR ≤ MF; GO ≤ MF (proposals GR-G1, GO-G1) | GR L41; GO L721 |
| 02-f | Narrow GO (GOR-BODY-04) TD ÷ H | > GR (reference and Broad) | GO L224 |
| 02-g | Report only | SK vs GR TD; GO vs SK shoulder ÷ H; GR vs MF shoulder ÷ H | §4.1 |
| 02-h | GR girdle organization (if GR-G2 accepted) | scapular superior–inferior extent ÷ scapular breadth > MF; arm clearance at 8° abduction without step (GR-G3) — qualitative, on orthographic renders | GR L41, L206 |

**RM-LR-06 (ALPC)** — run ALPC-0…8 (§3c; ALPC-8 reuses the existing GO L739 test) on GO reference, GOR-BODY-04, -12, -14, -16; MF-M-R as the shape comparator; Broad SK at 208 and 229 cm for ALPC-7 (AD-1 heights). Pass = all GO bodies pass ALPC-0…6 (ALPC-7/-8 are the separation tests listed with them) and the reference and GOR-BODY-02-height body pass ALPC-7.

**Method prerequisite (flag):** the generator shoulder joint "sits low" (W1c-B L78) and bideltoid breadth is soft tissue that moves with arm pose (W1c-B L65). Girdle checks need an anatomical acromial / glenohumeral landmark on rest geometry (D-W1c-1 scope). Proposed as a measurer method choice for acceptance (AD-G10).

---

## 5. Separation: skeletal architecture vs muscle amount vs Muscular Development Capacity

| Layer | Canon | Consequence for this packet |
|---|---|---|
| **Skeletal architecture** (Biological Anatomy + Skeletal Frame) | UCCA L119 frame = "skeletal breadth, depth, joint and robusticity variables"; GO L19 "Massive" = skeletal; GO L21 "**Gorrund skeletal massiveness exists independently from Current Muscularity and Body-Fat Amount.**"; GR L23 "leverage and reach rather than compact structural mass" | All girdle and ALPC proposals are skeletal. All tests measure skeletal landmarks or skeletal proxies. |
| **Current Muscularity / muscle amount** (Physical Composition) | UCCA L156 "composition never edits the skeleton; thoracic depth is never faked by fat or muscle; pelvic breadth is never fat"; GO L45 "**skeletal shoulder breadth** stays separate from **deltoid and trapezius development**, so low-muscle Gorrund can have very broad skeletal shoulders"; GR L72 "shoulder muscle doesn't move the shoulder joint"; GO L192 neck "never dependent on trapezius"; GO L726 "fails if it appears only once muscle is added"; SK L36 "Muscle modifies Skarn anatomy rather than creating racial identity"; RA L127 J-4 | Bideltoid breadth, trapezius slope, waist and hip circumference are **excluded** from every pass condition. ALPC-6 requires the low-muscle/low-fat body (GOR-BODY-16) to show the same continuity. ARMs at R-4 (RA L35). |
| **Muscular Development Capacity** (Biological Anatomy, ceiling) | UCCA L154 "Muscular Development Capacity ≠ Current Muscularity ≠ …"; UCCA L161 "Capacity … sets the valid ceiling of Current Muscularity (CLAMP)"; UCCA L164 "Where the population distribution is OPEN (Grask, Gorrund, …), **no population shift is invented.**"; SK L26/L80 Skarn higher MDC "(not a default Current Muscularity)"; GR L72, L251 OPEN; GO L82 "**OPEN**, never inferred from skeletal scale", L228, L703 | **MDC plays no role in any girdle/ALPC criterion.** Skarn's higher MDC is not a skeletal difference and is not used to separate SK from GO (GO L239 lists it as a Skarn property, but the AD-1 test passes on architecture only, P2O L24). GR/GO MDC remain OPEN; nothing in this packet infers them from girdle size or trunk mass. |

Explicit firewall statement (PROPOSAL for the packet's own acceptance record): *a larger skeletal girdle or a more continuous axial profile neither implies nor requires higher Current Muscularity or higher Muscular Development Capacity; and neither muscle amount nor capacity may be used to satisfy, rescue or fail any §3–§4 check.*

---

## 6. Build implications after acceptance

**Dependencies.**
1. This packet + the **pelvic morphology packet** (order §7) must be accepted together or in that order: ALPC-2/ALPC-3 constrain pelvis-to-trunk and pelvis-to-femur *relationships*, while pelvic *morphology* (GR, GO) is the §7 packet. Any conflict between the two packets is resolved before building (AD-G11).
2. Ear families (order §6) are independent of this packet.

**Rebuild (GR, GO).** The MakeHuman generator cannot produce a non-human scapula (GR-G2), a girdle carried by the thorax with a continuous lower axial chain (ALPC), or measurable skeletal stations (W1c-G L129 "Sculpted trunk/girdle per canon"). Proposed approach, for method acceptance:
- Build a **skeletal trunk proxy** per race (ribcage, girdle — clavicles, scapulae, glenoid —, lumbar column envelope, pelvis per §7 packet, proximal femur) at reference stature by proportion (R-2), then fit / sculpt the R-4 soft-tissue envelope over it. Keep the accepted W1c limb, hand and head proportions where they still pass (GR rows 69–89, GO rows 90–104 in W1c-A) to avoid re-opening accepted directions.
- Declare every builder-chosen magnitude (girdle overhang, scapular extent, station ratios) under R-14; their acceptance is an authorship decision about those values (RA L86).
- Variants needed in W2: GOR-BODY-04, -12, -14, -16, GOR-BODY-02 (208 cm), Broad SK at 208 / 229 cm (accepted SK base, frame write only), GR-BODY-10 for RM-LR-04.

**RM-LR and other checks to rerun.**

| Item | Why it reruns |
|---|---|
| RM-LR-01 | Trunk rebuild moves suprasternal and hip-joint landmarks: GR < MF, SK torso share; GO > GR torso share; GR span > SK, GO must still hold. GO vs SK stays report-only (AD-4) |
| RM-LR-02 | All of §4.2 (02-a…h); first run with skeletal girdle landmarks |
| RM-LR-03 | GOR-BODY-12 / -14 vs Broad SK (LR-04; GO L179) — uses ALPC and depth ratios |
| RM-LR-04 | GR-BODY-10 vs GO limb-present family (AD-3) — limb shares are measured from the girdle (arm origin), so GR-G3/GO-G2 change the arm-origin landmark |
| RM-LR-05 | Shoulder and hip joint scale change with GO-G3 / ALPC-3 (GO > GR must hold; SK pairs stay n.d.) |
| RM-LR-06 | First real run (§3c) |
| RM-LR-07 | Only if hands are rebuilt (not expected) |
| RM-UB-06 | Pelvic external skeletal dimensions for GR, GO (with §7 packet) |
| W1c-A rows | 69–104 for GR and GO, especially 87 (GR breadth < SK), 94 (GO > SK breadth, currently marginal), 95–98 (depth) |
| Boundary tests | AD-1 (GO L271), AD-2 (GR L716), AD-3 (GR L717, GO L244), GO L150 Narrow, GO L148 low muscle, GR L100 high muscle, GR L104 equal-height Skarn |

---

## 7. Author decisions needed

1. **AD-G1 — Grask girdle breadth mechanism (GR-G1).** Accept that Grask shoulder breadth follows the Grask thorax and is not obtained by human-girdle widening (shoulder ÷ thoracic breadth ≤ MF).
2. **AD-G2 — Grask scapular organization (GR-G2).** Accept the vertically extended, close-seated, spine-coupled scapula as the positive "scapular relationship distinct from humans"; **or** keep morphology OPEN at builder's choice (then the AD-2 girdle carrier stays qualitative).
3. **AD-G3 — Grask arm origin and clavicle (GR-G3, GR-G4, GR-G5).** Accept clearance-without-overhang, the clavicle as a consequence of girdle placement, and the upright open girdle–neck transition.
4. **AD-G4 — Grask vs Marchfolk shoulder breadth relative to stature (GR-G7).** Confirm it stays undetermined (recommended), or author a direction. (Diagnostic: the W1c GR candidate sits below MF; canon only requires "never classified small".)
5. **AD-G5 — Gorrund girdle (GO-G1…G6).** Accept girdle carried by the thorax (≤ MF overhang), girdle wrapping a deep thorax, substantial clavicle and girdle joints, skeletal neck–girdle integration, and continuous shoulder–pelvis variation within ALPC.
6. **AD-G6 — GO > GR girdle breadth relative to stature (GO-G7).** Confirm as DERIVED from GO L40 / R2 L54.
7. **AD-G7 — GO thoracic depth ÷ breadth > SK and > GR.** Confirm as DERIVED from GO L42 and AD-1 (P2O L24), making RM-LR-02-c a pass condition.
8. **AD-G8 — ALPC operational definition (ALPC-0…8).** Accept the station set, the "normalized profile, compared in direction with the MF shape" principle, the two-sided pelvis criterion (ALPC-2), and ALPC-7 (GO > Broad SK on continuity ratios as the AD-1 ALPC carrier). Confirm that ALPC-7 is architectural and does not touch AD-4.
9. **AD-G9 — Optional ALPC criteria.** ALPC-1b (ribcage vertical length ÷ breadth ≥ MF): adopt or not. ALPC-1c (costal–iliac gap): report-only (recommended) or drop.
10. **AD-G10 — Measurement method.** Accept skeletal-proxy measurement (or, at minimum, GOR-BODY-16 skin profile plus reference) for ALPC; accept anatomical acromial / glenohumeral landmarks for girdle checks instead of the generator shoulder joint; keep the 1 % marginal threshold for these checks.
11. **AD-G11 — Sequencing with the pelvic packet.** Confirm that ALPC-2/-3 constrain pelvic relationships only and that pelvic morphology is decided in the §7 packet; resolve any conflict before rebuild.
12. **AD-G12 — Skarn.** Confirm canon is sufficient for the Skarn girdle (no new authorship). Decide whether SK L94 ("no top-heavy default") needs any check, given the diagnostic lower-trunk ratios of the accepted SK (recommended: no new canon; informational only).
13. **AD-G13 — AD-R15 wording.** Confirm AD-R15 covers exactly RAC-05 L34 (SK–GR depth; SK–GO and SK–GR joints), so GO > SK thoracic depth (R2 L55) stays a canon pass condition.
14. **AD-G14 — Rebuild method.** Accept a skeletal-trunk-proxy + sculpted envelope build for GR and GO (generator cannot satisfy GR-G2 or ALPC), with all magnitudes declared under R-14, and the RM-LR rerun list in §6.
15. **AD-G15 — Firewall statement (§5).** Accept that girdle size and ALPC neither imply nor require higher Current Muscularity or MDC, and that neither may satisfy, rescue or fail any check.

**Not proposed (stays as is):** any GO vs SK torso/limb share (AD-4); SK–GR depth; SK–GO / SK–GR joints; any numeric envelope; any MDC distribution for GR or GO; any spec edit before acceptance.

— Claude (draft; STOP at author-acceptance gate)
