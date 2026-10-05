# Universal Character Creation Architecture (UCCA) v1

**Status:** **CANONICAL: UCCA Phase 2** (October 5, 2026; `reviews/chatgpt-ucca-phase2-canonicalization-order.md`). Closure pending author review of the Phase 2 report (`reviews/claude-ucca-phase2-canonicalization-report.md`).
**Phase:** DESIGN ONLY. This document defines whole-character creator **design behaviour**. It does not define UE5 mesh, skeleton, morph, rig, animation, camera, UI or save-file implementation (§26).
**Sources:**
- Phase 1 package: `reviews/claude-ucca-01…11` (line citations there refer to commit 571b71f)
- Per-race evidence: `reviews/ucca-evidence/`
- Author rulings: AD-C1…AD-C17, AD-C3b and T-1…T-12 (`reviews/chatgpt-ucca-phase2-canonicalization-order.md` §2–§3)
- Closed facial companion: `decisions/UFCA_V1.md`

## 1. Purpose and authority

UCCA is the single creator-facing **whole-character** architecture for all 13 playable populations. It gives every population one shared navigation, control and validation language for the body. It does **not** give them shared anatomy, proportions, ranges or distributions.

**Authority:**
- UCCA is a roster-wide rule document at PROJECT_RULES level (authority level 2), alongside UFCA.
- UCCA governs whole-character creator **organization**: navigation, control classes, dependencies, presets, randomization, locks, saved-appearance requirements and validation structure.
- **UFCA governs the face** (§12). UCCA routes into it and changes nothing in it.
- Each race spec (level 1) keeps governing that population's **anatomy**, tendencies, bounds, identity statements, locked tests and OPEN items.
- Where a race spec's provisional body-control organization differs from UCCA, UCCA governs the organization; the race requirement underneath is preserved and routed to its UCCA home (`reviews/claude-ucca-11-phase1-architecture-audit.md` Appendix A).
- **Nothing in UCCA authorizes anatomy, numbers, distributions or allometric functions that a race spec does not state.**

## 2. The 15-slot navigation (AD-C1)

A **slot is navigation, never anatomy.** Shared navigation never implies anatomical equivalence.

| # | Slot | Contents |
|---|---|---|
| 0 | **Race & Lineage** | Race selection. **Halvren only:** optional genealogy entry (§22). Never a body or face slider |
| 1 | **Starting Character** | Whole-character presets; whole and selective randomization; strength; lock overview. **Simple Mode ends here** |
| 2 | **Stature & Proportions** | Stature; torso/axial vertical contribution; neck length where bound (AD-C10); arm and leg length and segment distribution. **Saurin:** head-to-body (±8 %) |
| 3 | **Skeletal Frame** | Frame starting operation (Narrow / Balanced / Broad) and the continuous skeletal breadth, depth, joint and robusticity variables (§7) |
| 4 | **Hands & Feet** | Multidimensional hand and foot variables (§8). **Saurin:** claws. **Cogling:** finger internal distribution |
| 5 | **Tail** | **Saurin only; Absent for all others** (§9) |
| 6 | **Physical Composition** | Current Muscularity (overall + regional); Body-Fat Amount; Body-Fat Distribution; Muscular Development Capacity where exposed (§10) |
| 7 | **Sex-Related Anatomy** | Body-level sex-related anatomy selection (SOFT input, §11); race-canon sex-related tissue controls (**Saurin E/B** only) |
| 8 | **Face** | Routes into the closed UFCA 16-slot hierarchy |
| 9 | **Hair & Display** | Scalp-hair biology (shared with UFCA slot 10); body-hair biology where bound (§13); Saurin cranial display (UFCA slot 10) and restrained body continuation |
| 10 | **Skin & Integument** | Natural layer; Environmental sub-panel (§14). **Saurin:** scale fields, pattern, claw keratin colour |
| 11 | **Age** | **One Apparent Biological Age driver** for face and body (= UFCA slot 14; one variable shown in both places) (§15) |
| 12 | **Asymmetry & Acquired History** | Natural subtle body asymmetry (§16); Acquired layer. Facial asymmetry stays in UFCA slot 13 |
| 13 | **Body Language** | Idle / stance / gesture presentation (§17) |
| 14 | **Presentation** | Styling, grooming, Applied markings, cosmetics, clothing/gear preview, Age Presentation, culture / birthplace / background presentation presets, creator camera and preview lighting (§18) |

**Nested, not top-level:** torso/axial, neck, arms and legs (inside 2 and 3); regional muscle and fat (inside 6); Environmental layer (inside 10); Lineage (inside 0).

**Modes:**
- **Simple Mode:** Race → (Halvren: optional Lineage) → Starting Character preset → Confirm. Simple Mode never requires genetics. No simplified fake body.
- **Advanced Mode:** Race → Starting Character → Customize (all slots, plus UFCA) → Confirm.
- **Quick controls:** one curated DIR control per major dimension in each Bound slot. **Detailed controls:** the full regional sets. Quick controls are never hidden macros.
- Both modes write **one appearance record**; switching modes keeps the appearance.

## 3. Bound / Bound-locked / Absent

Each population supplies a **binding** for each slot (label, anatomy family, control set, validators, state), exactly as UFCA_V1 §2 and §4:

| State | Meaning |
|---|---|
| **Bound** | The population has this anatomy and the bound controls are authorized |
| **Bound-locked** | The anatomy exists and is validated, but no editable control is authorized |
| **Absent** | The population lacks the anatomy. The slot or sub-panel is **hidden, never a dead control** |

**A shared slot never by itself authorizes a control** (AD-C17; UFCA AD-U12 and F-1 discipline extended to the whole body). A body control exists only where race canon names the quantity as a variable or control dimension.

**Population-specific labels:** Slot 4 "Hands, Feet & Claws" (Saurin); Slot 9 "Cranial Display" (Saurin; hair Absent); Slot 10 "Scales & Pattern" (Saurin). Absent for some: Tail (12 races); scalp and body hair (Saurin); E/B (all but Saurin); Saurin-specific contents (all others).

## 4. Control taxonomy

The UFCA classes apply unchanged (UFCA_V1 §5): **DIR** (direct anatomical control), **DER** (derived/coupled, recomputed, never hand-stored), **SOFT** (soft-correlated tendency), **VAL** (validator-only), **LAT** (preset latent / write operation), **PRES** (presentation), **DIAG** (diagnostic).

**Body class decisions:**

| Quantity | Class |
|---|---|
| Stature | DIR (the only absolute size control, §6) |
| Segment shares and within-limb distributions | DIR where canon names them; bands from RM-UB-01 |
| Head-to-stature | **VAL / DIAG** for every race except Saurin, whose ±8 % head-to-body control is DIR (SAURIN §258) |
| Neck length | DIR only where canon names it (AD-C10); otherwise hidden |
| Absolute dimensions (cm of head, hands, feet, joints, breadths) | **DER** via per-race allometry (RM-UB-02) |
| Arm span; visible mass; limb circumference ("thickness") | **DER**, never sliders |
| Frame starting operation | **LAT** write operation (§7) |
| Composition starting operation | **LAT** write operation (§10) |
| Muscular Development Capacity | DIR only where canon requires it; otherwise VAL ceiling (§10) |
| Sex-related anatomy selection | **SOFT** (§11) |
| Apparent Biological Age | DIR, one driver (§15) |
| Natural body asymmetry offsets | DIR, near-zero default (§16) |
| Body Language, Presentation | PRES |
| Matched-scale and equal-height comparisons; all Pass 2 indices | DIAG |

**Firewall (F-1 applied to the body):** measurability never makes a slider. A diagnostic or measurement-deferred quantity is never a creator control unless canon separately authorizes it.

**Multidimensionality bans (roster-wide validators):** no Hand Size or Foot Size scalar; no Arm Span slider; no Torso Size / Body Thickness / Torso Mass; no weight or thin-to-heavy slider; no single Skin Colour slider; no global scale-size control (Saurin); no master race-proportion sliders ("human → Pipkin", "Cogling Proportion", "Elf Percentage", "Elf Gracility", ALPC, LSCTA, FSEA or equivalent).

## 5. Dependency relations and resolution order

The UFCA relations, resolution order and outcomes apply unchanged (UFCA_V1 §6): **FOLLOW, OFFSET, CLAMP, NEIGHBOR-ADJUST, ENVELOPE, REDISTRIBUTE, INVALID**; order FOLLOW/DER → CLAMP (intent retained) → NEIGHBOR-ADJUST (unlocked only) → re-validate; outcomes **PASS / CONSTRAIN / FAIL**. CONSTRAIN is reported and biologically deterministic. **Locks are absolute; a locked child never forces an invalid parent; no silent reset.**

**Body applications:**
- **CLAMP:** race segment bands (RM-UB-01); capacity ceiling on Current Muscularity; Saurin reachable tail cap (§9); Saurin B ceiling.
- **FOLLOW / DER:** absolute dimensions from stature and race-relative values; Saurin tail base from tail length.
- **OFFSET:** regional muscle on overall muscularity; age effects; natural asymmetry.
- **ENVELOPE:** frame starting operation writes; sex-related SOFT centres; Halvren envelope B.
- **REDISTRIBUTE:** the **only** canon case is **Saurin stature accounting**: head, neck, thorax, lower trunk and legs sum coherently to stature rather than inflating independently (SAURIN §55 stature-share accounting; SAU-FACE-22). The tail is not part of stature (§256.9). No other body relationship tool exists in v1.
- **No broad body relationship tools in v1** (UFCA G-3 extended): no master body-shape, body-type, masculinity, femininity, race-body or ancestry-percentage slider.

## 6. Stature and proportions; no uniform scaling (AD-C3)

1. **Stature is the only absolute size control.** It is DIR within the race's canonical envelope.
2. **Other dimensions are stored semantically and race-relatively** (shares, ratios to neighbouring anatomy, positions within the race envelope).
3. **Absolute dimensions are DER** through race-specific allometry (RM-UB-02). Head, hands, feet, joints and bone breadth never follow stature by one shared scale factor.
4. **No uniform whole-body scaling** as the design model, ever. The prototype's uniform height step and race scale are non-authoritative (PROJECT_RULES, Technical authority).
5. **Height is relationship-aware:** stature changes distribute through segment shares inside race CLAMP bands. No race gains or loses identity by stretching one segment.
6. **Ranges are exactly the canon envelopes.** Population stature and proportion distributions are OPEN or SILENT for every race (Saurin's authored §263 sex-shift centres are the only authored soft centres); generation uses interim weights that are never canon (§20).
7. **Equal-height tests** use a stature valid for every participant (GRASK_V1 equal-height rule). Where no stature is shared, **matched-scale** comparison is diagnostic only. The **Durrim–Marchfolk equal-height comparison point is 152 cm** (T-6).
8. **Halvren:** §22.

## 7. Skeletal Frame (AD-C2)

**Definition:** Skeletal Frame is the continuous configuration of a character's skeletal breadth, depth, joint and robusticity variables (shoulder/clavicular breadth, thoracic width, thoracic depth where bound, pelvic width and depth where canon names it, joint scale, long-bone robusticity, plus race-specific extras), each inside that population's envelope.

**Frame is not** sex, body type, muscularity, fatness or stature. **Balanced is not the canonical or default body.**

**No persistent driving frame state:**
1. Narrow / Balanced / Broad are **write-and-vanish starting operations** that write race-specific starting values.
2. Regional edits act on values directly; nothing pulls back toward the preset.
3. **The resolved skeletal values are the frame.** Canon effects tied to a frame category are computed from resolved values (the one case: Saurin reachable tail cap, §9).
4. "Started from: Broad" may be kept as **non-driving provenance**; nothing depends on it.

**Write scope:** frame writes **only skeletal values**: Slot 3, and for Saurin also hand/foot breadth (Slot 4) and the tail-base frame component (Slot 5) (SAURIN §258). It never writes stature, segment lengths, composition, face, hair, sex-related anatomy or presentation.

**Correlated dimensions** may be influenced when frame is applied but remain independently editable where canon allows (Cogling AC-9 robusticity/joints as tendencies; Grask foot breadth; Gorrund thoracic depth; Durrim unequal breadths; "population-level correlation does not create a hard creator dependency"). Joint hard minimums and each race's frame boundary rule (Broad Skarn ≠ Gorrund; Broad Grask ≠ Skarn/Gorrund; Narrow Gorrund keeps ALPC; Broad Pipkin/Cogling ≠ Durrim; Narrow Pipkin/Cogling ≠ child or Fenn; Broad Saurin ≠ Gorrund; Narrow Vael ≠ scaled-down Broad) stay hard.

**Vael:** shoulder and pelvic breadth are Skeletal Frame variables because Vael canon says frame changes them (T-10).

**Manny/Quinn:** the prototype mannequin swap is superseded **at design level**. Any future implementation must represent every **frame × sex-related anatomy × composition** combination independently inside each race envelope. Whether those assets are kept, replaced or used as technical bases is not decided (§26).

## 8. Hands & Feet

Hands and feet are **multidimensional**: absolute vs proportional dimensions; length, breadth, depth; palm vs finger; heel, midfoot, forefoot, toes; skeletal vs soft-tissue contribution (Marchfolk universal amendment §4). **No single size scalar.** Where a race spec names an overall hand or foot scale (Fenn, Aelari, Vael; Saurin hand/foot size ±8 %), it is one control inside the multidimensional set, bounded by canon. Hands preserve grasp; feet preserve plantigrade contact and footwear compatibility. Saurin claws are Slot 4 (claw keratin colour in Slot 10).

## 9. Saurin Tail binding

- The tail is **mandatory biology. No on/off control.** No garment, preset, randomization or Acquired state makes a Saurin functionally tailless.
- Slot 5 holds: length (driver), base, taper, cross-section, segment/curvature, resting carriage, proximal/distal mass character, restrained dorsal keratin, tail pattern view.
- **Tail coupling (SAURIN §256) is authoritative:** length drives the base (base ≈ length^1.18); root-sufficiency 0.75–1.20 of reference; abrupt-taper guard ≤ 1.25×; mid-tail area 0.27–0.48 of root; distal ≥ 0.065; balance guard ≤ +3°; carriage +8° lift … +10° droop.
- **Tail muscularity follows Physical Composition; there is no independent tail-muscle slider** (§256.6 supersedes the older §145 wording, T-4). Caudal fat is graded through the proximal half.
- **Reachable length cap** is a function of resolved frame and composition through the canon points (~78 % H Balanced at reference composition; 80 % H Broad; ~72 % H Narrow high-fat). Between the points it is RM-UB-04.
- The tail has its own lock group and selective randomization scope.
- Garments may partially cover, drape or sheath the tail (permission resolved, SAURIN §195/§225); tail-equipment construction and coverage extent remain OPEN.
- Acquired tail loss/injury remains OPEN and is never generated.

## 10. Physical Composition and capacity

**Five-way separation:** Muscular Development Capacity ≠ Current Muscularity ≠ Body-Fat Amount ≠ Body-Fat Distribution ≠ Skeletal Frame. Soft-tissue fullness, circumference and visible mass are DER.

**Hard rules:** composition never edits the skeleton; thoracic depth is never faked by fat or muscle; pelvic breadth is never fat; frame never edits composition. Regional muscle values are OFFSETS on overall muscularity. Distribution never substitutes for amount. No uniform inflation.

**Regional groups:** a superset navigation list (neck, shoulders, upper arm, forearm, chest, upper back, core, glutes/hips, thigh, calf/shank; Saurin: tail). Each race binds **only the groups its canon names.** Saurin excludes human pectoral blocks, six-pack segmentation and gluteal/buttock mass.

**Muscular Development Capacity (AD-C4, option a, conservative):**
- Capacity is Biological Anatomy and sets the valid ceiling of Current Muscularity (CLAMP).
- It is a **Detailed control only where canon explicitly requires it as a representable or variable axis** (Saurin variation axis; Cogling §69 representable variable).
- Elsewhere it is a **VAL ceiling / distribution property.**
- Where the population distribution is OPEN (Grask, Gorrund, Pipkin, Cogling), **no population shift is invented.**
- Capacity and visual muscularity **never imply gameplay strength.**

**Composition starting operations (AD-C5):** **Lean / Athletic / Muscular / Heavy** are universal write-and-vanish operations with race-specific values supplied by each race. They write **Physical Composition only** (muscularity, regional offsets, fat amount, fat distribution) and never skeletal frame, stature, sex-related anatomy or capacity. After writing there is no "Athletic" state. **"Custom" is a UI state/description, not an anatomical preset.**

**Prohibited packages:** no stereotype physique bundle (never Broad → muscular → high fat); no "round halfling"; no "bodybuilder troll"; no "ogre belly".

## 11. Sex-Related Anatomy and R-SEX (AD-C6)

- The body-level sex-related anatomy selection is a **SOFT biological input under R-SEX** (PROJECT_RULES).
- It may shift **only race-canon soft distributions/centres** used by generation. It **never moves already stored values**, never becomes a body package and **never invents dimorphism**. "No shift" is a valid complete state.
- **Saurin** keeps exactly its four authored centres (SAURIN §263) and no other sex shift. E/B live in Slot 7, never under fat: E coelomic body-wall fullness (female centre 2.0 cm); B ventral fullness, one continuous midline field (female centre 1.6 cm, ceiling 3.0 cm); identical bounds for both sexes; overlap mandatory; B counts against the thoracic depth/width guard.
- **Saurin anti-hourglass validators:** no waist narrowing as a sex signal; no paired ventral masses; no hip flare; no buttocks.
- Reproductive biology is never inferred from creator architecture.

## 12. UFCA integration

- Slot 8 routes into closed UFCA **unchanged in substance.**
- **One Apparent Biological Age driver** (UFCA slot 14 = UCCA slot 11).
- **Scalp hair** is one variable shown in UFCA slot 10 and UCCA slot 9.
- **Saurin head scale** is one variable: the SAURIN §258 ±8 % head-to-body control is shown in UFCA slot 1 (AD-U4) and UCCA Slot 2. There is no second head control.
- **One randomization strength** for face and body; face-only and body-only selective randomization each preserve the other side.
- Head-to-stature and head-neck balance validators run with face extremes.
- UFCA machinery (classes, relations, outcomes, N-levels, frequency vocabulary, strengths, AD-U12) is reused, never redefined.

## 13. Hair & Display (AD-C7)

| System | Biology (Slot 9) | Styling (Slot 14) |
|---|---|---|
| Scalp hair | Texture, density, hairline, growth, natural colour, inherited silver/white (≠ age graying) | Length, cut, braids, shaving, dye, accessories |
| Facial hair, eyebrows | UFCA slot 11 (closed) | Grooming |
| **Body hair** | **Bound only where canon supports it** (Pipkin, Cogling). **Hidden** for Marchfolk, Skarn, Sagekin, Fenn, Aelari, Vael and Halvren pending biological authorship. **Durrim, Grask, Gorrund: BIO OPEN.** Body hair is never inferred from scalp or facial hair | Shaving, grooming |
| Saurin | **No mammalian hair (Absent).** Cranial display in UFCA slot 10; optional restrained body continuation, never a mandatory spinal crest | Display polish, paint, wraps |

Hair colour is related across scalp, brows, face and body without identical values. Hair is never locked to frame, sex, physique or occupation.

## 14. Skin Appearance Layers (AD-C9)

**Four layers govern: Natural / Environmental / Applied / Acquired.**

| Layer | Contents | Slot |
|---|---|---|
| **Natural** | Multidimensional pigmentation, undertone, perfusion, regional variation, freckles, moles, birthmarks. Saurin: scale fields, inherited pattern, claw keratin colour, integumentary ridges | 10 |
| **Environmental-persistent** | Tanning / sun response, weathering, dryness, **ordinary reversible or accumulated callusing** | 10 (sub-panel) |
| **Environmental-transient** | Dirt, dust, soot, mud, wetness and comparable temporary contamination or state | 10 (sub-panel) |
| **Applied** | Tattoos and equivalents, body paint, cosmetics, dye, decorative claw treatment, display paint | 14 |
| **Acquired** | Scars, burns, healed injuries, permanent or localized damage, damaged scale fields, chipped claws, localized pigment change, and callus-like tissue change **only when it has become a persistent individual-history alteration** | 12 |

**Calluses (T-9):** ordinary environmental callusing = Environmental-persistent; permanent, history-like tissue alteration = Acquired. This reconciles race wording by state and degree; no population's biology is exceptional.

**Rules:** never one Skin Colour slider; stored values are lighting-invariant; surface never compensates for structure (identity survives neutral grey / uniform pigment); validity ≠ frequency; **Environmental and Acquired state are never forced by race, class, culture or occupation**; soot and grime are never racial. Saurin: field boundaries locked, no global scale-size control, no unrestricted RGB picker; per-field numeric ranges OPEN.

## 15. Age

| Element | Architecture |
|---|---|
| **Chronological Age** | Character data, never inferred from appearance |
| **Apparent Biological Age** | **One systemic DIR driver for face and body.** Adult creator scope only. Body effects are DER OFFSETS (composition redistribution, skin, hair density and colour, Saurin scale-edge and claw wear, posture-range tendencies only where canon allows) |
| **Age Presentation** | Presentation (Slot 14) |

**Firewalls:** no frailty, stoop or slowness package; aging is never "wrinkles + gray hair" only; aging never changes racial skeletal identity or stature dramatically; adults read adult at the youngest valid age; no lifespan-percentage slider. **Apparent Biological Age is appearance biology and never automatically imposes movement-speed or other gameplay penalties** (T-11). Age starting points are write operations on Apparent Biological Age. Lifecycle is OPEN everywhere.

## 16. Natural body asymmetry and Acquired (AD-C8)

**Natural subtle body asymmetry is a universal representable capability for all 13 populations**, as ordinary individual biological variation.

- It is **not** a racial identity trait, deformity, injury, culture or Presentation.
- **Neutral default = zero / near-zero asymmetry.**
- Ordinary subtle offsets only, unless a race spec explicitly authorizes more.
- It must preserve joints, gait-support geometry, paired-limb functional coherence and population identity.
- It may not simulate acquired injury, missing anatomy, pathological deformation or major length discrepancy.
- **Acquired asymmetry stays Acquired History** (Slot 12, separate panel).
- **No race-specific asymmetry distributions or numeric ranges exist**; none are invented here.
- Saurin canon remains authoritative where more specific. Facial asymmetry stays in UFCA.

## 17. Body Language vs Anatomical Resting Alignment (AD-C11)

Body Language (Slot 13) is a universal Presentation slot for idle, stance and gesture presentation. It **never rewrites anatomy or Anatomical Resting Alignment.** No race defaults: no graceful-elf, sinister, waddle, bounce, fidget or tinker poses. Saurin tail poses carry no fixed emotional meaning.

## 18. Presentation

- Culture / birthplace / background are Presentation presets and identity layers that **never write anatomy.** Choosing a race never applies cultural markings automatically.
- Markings are placed in the Applied layer (position, scale, rotation, colour, opacity, mirroring, layering, independent removal); Saurin patterns are Natural, not markings.
- Clothing and gear are creator preview only. Equipment fits anatomy; canonical equipment never scales with the holder.
- Creator camera and lighting: neutral reference lighting first; purpose views (whole body, face, hands, feet, tail, surface).

## 19. Presets: write-and-vanish

| Rule | Content |
|---|---|
| P-1 | Every preset is a **write operation** that produces an ordinary valid appearance record |
| P-2 | No preset-only anatomy, morphs or geometry |
| P-3 | After writing, no preset state remains; editing any value leaves an ordinary character |
| P-4 | Provenance (starting preset id) is optional and **non-driving** |
| P-5 | Effects canon ties to a frame or composition **category** are computed from resolved values, never from the label |

**Tiers:** whole-character presets (race libraries); frame starting operations (Slot 3); composition starting operations (Slot 6); presentation presets (Slot 14 only); Saurin surface presets (Natural only); age starting points; Saurin tail neutral presets. **Presets are never castes, subraces, classes, cultures or genealogy.** No stereotype bundles. Every library includes neutral and minimum-stereotype individuals.

## 20. Randomization, strength, frequency, scopes and locks (AD-C12)

- **Domains:** Biological, Presentation and Acquired-History are separate passes; Presentation and Acquired never rewrite anatomy; Acquired never creates major tail, rostral or jaw loss.
- **Pipeline:** race envelope (Halvren B) → drivers from weighted SOFT distributions → dependents in coupled bands → validators: **reject FAIL and resample; never roll everything and repair** → batch diversity → presentation pass.
- **Strength:** Subtle / Diverse / Extreme exactly as UFCA_V1 §14; one setting for face and body.
- **Frequency:** internal Very Common / Common / Uncommon / Rare describes weighting only (UFCA_V1 §15). **Interim weights are never canon.** Rare phenotypes are always manually creatable.
- **Sex:** shifts only race-canon soft centres (§11).
- **Selective scopes (universal union):** whole character; body only; face only; surface only; hair only; eyes only; composition only (preserving frame and height); presentation only; acquired only; age presentation only; **tail only and pattern only (Saurin)**. Population-bound scopes appear only where anatomically bound.
- **Locks:** any attribute, region or slot can be locked. **Locks are absolute and never silently broken.** If no valid solution exists, the lock is kept and the conflict is reported.
- **Seeds:** seed + generator version + distribution version + scope + locks reproduce a generation event; **saved characters store resolved values, not seeds.**
- Anti-juvenile packages (Pipkin, Cogling) are banned.

## 21. Saved / reusable appearance (AD-C13)

**Conceptual domains** (not a format): 1 schema/version; 2 race; 3 Halvren lineage record (constraints B recomputed, not stored); 4 sex-related anatomy; 5 Biological Anatomy (stature, shares, hands/feet, Saurin tail and E/B, head-to-body where bound, capacity, Natural surface, hair biology, ocular per UFCA, display); 6 Skeletal Frame (resolved values); 7 Physical Composition; 8 Face (UFCA values); 9 Age (Chronological, Apparent Biological, Age Presentation); 10 natural body asymmetry; 11 Environmental (persistent and transient subtypes); 12 Acquired history; 13 Presentation; 14 optional non-driving provenance.

| # | Rule |
|---|---|
| S-1 | Resolved values, not preset references |
| S-2 | Semantic traits, not mesh or morph weights, and not prototype slider values |
| S-3 | Derived values are recomputed on load from stored values and current race rules |
| S-4 | Migration, not reinterpretation; a rule change that invalidates a stored value → CONSTRAIN on load, reported |
| S-5 | Cross-race reuse only by semantic re-mapping and race-valid reinterpretation; not required in v1 |
| S-6 | NPC parity: NPCs, presets, randomized and player characters share one record and one set of validators; narrative exceptions are flagged non-baseline |
| S-7 | Lighting-invariant storage; responsive states (pupil dilation) are never stored |

The prototype's "race + slider values" record is non-authoritative and superseded at design level (T-11). **No serialization format, save schema, mesh representation or UE5 implementation is chosen.**

## 22. Halvren lineage and body architecture (AD-C3b)

- **Genealogy (A) → ancestry-derived constraints (B, recomputed, never stored) → phenotype (C)** (UFCA_V1 §11). Lineage is optional and lives only in Slot 0.
- **No Elf Percentage, Elf Gracility or ancestry-percentage body slider.** No 50/50 default. Frame never encodes ancestry. Source protection applies to body and face.
- **Stature:** 152–213 cm is the established **central population envelope**, not the complete biological hard bound. The architecture **supports ancestry-dependent stature tails outside it** through envelope B. Inherited stature is **never hard-clipped** to 152–213 cm.
- **Tail limits and frequencies are BIO/MEAS deferred** (RM-UB-05). They are derived later from approved source-population biology, Halvren inheritance/development rules and reference-mesh measurement. **No tail number is invented.**
- Any temporary central-only testing scope must be **explicitly labelled non-canonical interim test scope** (T-12).
- HV-49 / HV-50 stay validation targets. Tails never make a source-race height automatically valid.

## 23. Saurin body exceptions

Saurin canon (SAURIN_V1, especially §140–§154, §256–§258, §263, §265) governs wherever it is more specific than UCCA:
- mandatory tail and Slot 5 (§9);
- head-to-body ±8 % DIR; the ±8 % creator bound governs creator variation, and the older stature-share wording is a reference/central morphology statement (T-1);
- §258 creator hard bounds; stature 168–208 cm independent;
- frame scope per §258 (no stature, long-bone/axial length, skull or sacral-caudal change; no sex shift);
- Saurin-specific muscle and fat regions; E/B and anti-hourglass (§11);
- no mammalian hair; scale fields, pattern and claws;
- stature accounting is the only canon REDISTRIBUTE (§5);
- lock groups per §144.

UCCA never humanizes Saurin architecture.

## 24. Validation framework (AD-C14, AD-C15)

**Every existing permanent body and race test is carried forward unchanged and stays authoritative.** Tiers organize them (`reviews/claude-ucca-09-validation-framework.md`):

| Tier | Scope |
|---|---|
| A | Intra-population validity |
| B | Cross-population boundary validity |
| C | Relationship validity |
| D | Extreme-combination stress |
| E | Neutralization / identity persistence |
| F | Age / sex / asymmetry |
| G | Preset / randomization diversity |
| H | Stature / proportion validity |
| I | Frame / composition independence |
| J | Surface / presentation separation |
| K | Whole-character integration with UFCA |

**Universal validators adopted (AD-C15):**
- **No-uniform-scale test:** two statures of one character are never related by a single scale factor across head, hands, feet and joints.
- **Frame × sex-related anatomy × composition factorial** at reference stature per race.
- **Athletic write test:** applying any composition starting operation changes no Slot 3 value.
- **Body Language separation test:** no body-language preset changes Anatomical Resting Alignment.
- **Simple → Advanced equivalence:** a Simple Mode character opened in Advanced Mode is the same record.
- **Natural asymmetry test:** offsets stay subtle, preserve function and never read as injury, deformity or race identity.

**N-level body extension** (UFCA_V1 §16): N2 adds neutral body hair, no clothing (or a neutral fitted proxy) and neutral body language; N3 adds uniform pigment and pattern (Saurin: tail present); **N-Head** neutralizes the head for body tests.

**Generic pairwise body harness (AD-C14):** each population pair at a stature valid for both where one exists, matched-scale otherwise. **Diagnostic; supplements, never replaces, race tests.** No visual stereotype may substitute for anatomical validity.

## 25. Measurement-deferred and BIO OPEN

**Measurement-deferred (not creator controls unless canon separately authorizes them):** RM-UB-01…05, listed in `reviews/claude-pass2-r5-reference-mesh-queue.md` §3B, plus the existing RM-LR, RM-SR, RM-OT, RM-CF and RM-UF items, carried unchanged.

| ID | Item |
|---|---|
| RM-UB-01 | Per-race segment-share and within-limb distribution bands |
| RM-UB-02 | Per-race allometric response to stature |
| RM-UB-03 | Joint-scale and long-bone robusticity envelopes |
| RM-UB-04 | Saurin reachable tail-length cap function |
| RM-UB-05 | Halvren inherited stature-tail limits and frequencies (authorship + measurement) |

**BIO OPEN (carried, not resolved):** pelvic morphology; segment ratios and numeric proportions; arm span (Grask, Pipkin); joint/robusticity distributions; head-to-stature (all but Saurin); capacity distributions (Grask, Gorrund, Pipkin, Cogling); fat-distribution tendencies; sex dimorphism magnitude (Durrim, Grask, Gorrund, Pipkin, Cogling); reproductive biology; lifecycle; body hair (Durrim, Grask, Gorrund; hidden elsewhere where silent); Halvren stature-tail limits; Saurin balanced posture and density model, caudal-base landmark, numeric lower-trunk minimum, numeric Broad-vs-Gorrund boundary, claw/digit and per-field scale ranges, tail world-space validation, acquired tail/rostral/jaw loss, thermoregulation, tail-equipment construction and coverage extent; skin thickness/durability (Durrim, Grask, Gorrund); Pipkin trunk-share numeric relation (T-2).

**Later gameplay review:** legacy racial traits (breath, swim, sneak and similar) stay outside creator biology. No creator value feeds a gameplay stat.

## 26. Implementation firewall

UCCA is **DESIGN ONLY**. It does not decide or authorize: UE5 implementation; mesh, skeleton or morph construction; Manny/Quinn asset fate; animation, locomotion, IK or retargeting; camera or first-person geometry; collision or reach; equipment fitting; save serialization; gameplay balancing. The prototype (level 6) stays non-authoritative where it conflicts. **Canonical status is not permission to begin UE5 implementation.**

— Claude, canonicalized under `reviews/chatgpt-ucca-phase2-canonicalization-order.md`
