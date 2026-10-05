# UCCA-03: Control Taxonomy & Dependency Model (Whole Character)

**Author:** Claude (auditor / architecture analyst)
**Order:** `reviews/chatgpt-ucca-phase1-order.md` §7
**Status:** PROPOSAL for author review.

## 1. Classes and rules carried over from closed UFCA

- **Classes:** UCCA uses the UFCA classes unchanged (UFCA_V1 §5): **DIR, DER, SOFT, VAL, LAT, PRES, DIAG**.
- **Firewall F-1 and Rules G-1…G-5** (UFCA_V1 §7) are extended to the body. They are not redefined.
- **Relation types:** UCCA uses the UFCA relations: **FOLLOW, OFFSET, CLAMP, NEIGHBOR-ADJUST, ENVELOPE, REDISTRIBUTE, INVALID**.
- **Resolution order and outcomes** are as in UFCA_V1 §6: FOLLOW/DER → CLAMP retaining intent → NEIGHBOR-ADJUST (unlocked only) → re-validate. The outcomes are PASS / CONSTRAIN (reported, biologically deterministic) / FAIL. Locks are absolute, and there is no silent reset.
- **REDISTRIBUTE** is authorized only where canon names a redistribution. UCCA found one: the Saurin stature-accounting rule (UCCA-04 §4). No broad relationship tools are added (UFCA AD-U3 = none in v1).

## 2. Body variable registry

Columns:
- **Class** gives the default, with race exceptions.
- **Stored as** gives the proposed representation (AD-C3).
- **Numbers** gives the RM item, where one exists, or "—" if no number is needed for Phase 1.

### Slot 0: Race & Lineage

| Variable | Class | Stored as | Numbers |
|---|---|---|---|
| Race | DIR (categorical) | id | — |
| Halvren genealogy (A) | **Non-appearance input**; never an appearance control | genealogy record (schema OPEN, HV L70, L394) | — |
| Ancestry-derived constraints (B) | **VAL envelopes, recomputed** (proposed: not stored) | — | RM-OT-03 |

### Slot 2: Stature & Proportions

| Variable | Class | Stored as | Numbers |
|---|---|---|---|
| Stature | **DIR** within race bounds. Halvren: ancestry-dependent envelope B; tail limits OPEN (AD-C3b) | absolute cm | — |
| Torso / axial vertical contribution | DIR (SA axial trunk ±10 %); elsewhere DIR as share | share relative to race reference | RM-LR / SR / OT |
| Neck length | DIR (SA ±15 %); MF "neck thickness" is not skeletal (L283); others per AD-C10 | share | RM-UB-01 |
| Arm length; upper-arm / forearm distribution | DIR; distribution is a separate DIR (FN, AE, VA, SG, GR, CG) | share + distribution | RM-UB-01; RM-LR-04 (GR floor) |
| Leg length; femur / lower-leg distribution | DIR | share + distribution | RM-UB-01 |
| Arm span | **DER** from shoulder breadth + arm segments + hand. **Never a slider** (GR L225; GO L202) | — | RM-UB-01 |
| Head-to-stature | **SA: DIR (±8 %).** Others: VAL / DIAG (UFCA AD-U4) | SA: ratio | RM-CF-10 |
| Absolute segment and extremity dimensions | **DER**: stature × share × race allometry | — | RM-UB-02 |

### Slot 3: Skeletal Frame

| Variable | Class | Numbers |
|---|---|---|
| Frame starting point (N / B / B) | **LAT operation** that writes breadth/depth/joint/robusticity values. **No persistent frame state** (AD-C2) | — |
| Shoulder / clavicular breadth | DIR | — |
| Thoracic width | DIR | — |
| Thoracic depth | DIR. **Skeletal only, never fat or muscle** (VA L114; DU L103; GO L181). SA: frame moves it ±2 % only; the separate DIR bound is ±8 % | — |
| Pelvic width; pelvic depth | DIR where canon names it (SA ±7 % width; frame never changes SA depth) | morphology OPEN |
| Joint scale | DIR, with race hard minimums (FN L115; AE L130; VA L132) | RM-UB-03 |
| Long-bone robusticity | DIR where canon names it as a distinct parameter (CG L755); elsewhere DER from frame values | RM-UB-03 |
| Skeletal visual mass | DER (MF L27) | — |
| Visible body mass / weight | **DER only. Never a slider; shown only when credible** (SK L106; SG L169) | — |

### Slot 4: Hands & Feet

| Variable | Class | Numbers |
|---|---|---|
| Hand: overall scale, palm length, palm breadth, (depth), finger length/proportion, finger thickness, thumb, wrist | DIR set. **Never one Hand Size** | RM-UB-01 |
| Per-finger lengths | **Not exposed** ("no per-finger controls yet", FN/AE/VA) | — |
| Cogling finger internal distribution | DIR (CG L605–611) | — |
| Foot: length, breadth, forefoot, midfoot, heel, depth, arch, toe length, ankle | DIR set per race canon. **Never one Foot Size** | arch OPEN |
| Saurin claws: length, curvature, width, thickness, tip, pigment | DIR, coupled to grasp and plantigrade contact | no numeric canon (SA L4203) |
| Digit count | **VAL (locked)**: 5 (GR, GO, PK, CG, SA) | — |

### Slot 5: Tail (Saurin)

| Variable | Class | Numbers |
|---|---|---|
| Tail length (% H) | **DIR driver** | 55–80 % H; reachable cap by frame/composition |
| Tail base breadth/depth | **DER / CLAMP** (base ≈ length^1.18; root sufficiency 0.75–1.20) + frame component | §256 |
| Taper; mid and distal fullness | DIR inside VAL bands (taper ≤ 1.25×; mid 0.27–0.48; distal ≥ 0.065) | §256 |
| Cross-section tendency; segment/curvature character | DIR | — |
| Resting carriage | DIR (+8° lift … +10° droop) | §256.8 |
| Tail muscularity; caudal fat | **DER from Composition** (no tail-muscle slider, §256.6–7) | — |
| Dorsal keratin (restrained) | DIR (display continuation) | — |
| Tail on/off | **Does not exist** (§145) | — |
| Tail loss / injury | **Not exposed (OPEN)** | — |

### Slot 6: Physical Composition

| Variable | Class |
|---|---|
| Muscular Development Capacity | AD-C4: **Biological Anatomy value**; DIR in Detailed only where canon names it as a creator variation axis or representable variable (SA L358; CG §69, which does not finalize sliders); elsewhere a VAL ceiling from the race distribution. GR, GO, PK distributions OPEN |
| Current Muscularity (overall) | DIR, bounded by capacity |
| Regional muscle (race group list) | DIR as OFFSETS on overall ("regional values stay tied to overall", SK L102) |
| Body-Fat Amount | DIR |
| Body-Fat Distribution (regional) | DIR, separate from amount (MF L282) |
| Soft-tissue fullness, limb circumference | DER (bone + muscle + fat; GR L251) |
| Facial soft tissue | DER / SOFT into UFCA slot 1 (closed) |

### Slot 7: Sex-Related Anatomy

| Variable | Class |
|---|---|
| Sex-related anatomy selection | **SOFT input.** Shifts only race-canon soft-distribution centres used by generation. **Never moves existing values; never a preset or package** (AD-C6; R-SEX) |
| Saurin E (body-wall fullness), B (ventral fullness) | DIR Biological Anatomy, available to both sexes (overlap mandatory). Centres by sex; B ceiling 3.0 cm; CLAMP vs thoracic guard. **Never in fat** |
| Other races' sex magnitudes | Not exposed (OPEN / "no shift") |

### Slots 9–14

| Variable | Class |
|---|---|
| Scalp-hair biology | DIR (Natural); UFCA slot 10 |
| Body-hair biology | DIR where bound (PK, CG); hidden otherwise (AD-C7) |
| Skin pigmentation | **DIR multidimensional set** (base amount, balance/undertone, vascular contribution, regional variation, natural marks). **Never one Skin Color** |
| Saurin scale fields | DIR per field: relief, unit size within bounds, ventral expression, transitions. **No global scale size** |
| Saurin pattern | DIR set (family, contrast, density, element scale, edges, weighting, continuity, tail expression) |
| Environmental layer | DIR (Environmental): tanning, weathering, dirt, wetness |
| Apparent Biological Age | **DIR, one driver for face + body** |
| Body age effects | **DER OFFSETS** (composition redistribution, skin, hair, posture-range only where canon allows) |
| Chronological Age | character data |
| Age Presentation | PRES |
| Natural body asymmetry | DIR offsets where bound (SA; others per AD-C8) |
| Acquired history | PRES-layer (Acquired) |
| Body language, idle, stance presentation | PRES. **Never writes Anatomical Resting Alignment** |
| Anatomical Resting Alignment | **DER** from anatomy (SA counterbalance guard VAL ≤ +3°) |

### Diagnostic and validator-only (never sliders, under F-1)

| Item | Source |
|---|---|
| ALPC | GO |
| LSCTA | PK |
| FSEA | CG |
| Compact Structural Concentration | DU / SRR |
| Grask leverage/reach floor | GR-BODY-10, RM-LR-04 |
| Torso / limb share comparisons | LRR orderings |
| Normalized displayed-height comparisons | SR-COMP-04: "not a valid in-world body state" |
| Center of mass | — |
| Saurin balance lean and reference stance | §257 |
| Root-sufficiency index | SA |
| Waist/hip and frontal waist/shoulder ratios | SA §263 accounting |
| Matched-scale silhouettes | — |
| SK/MF equal-height comparisons | — |

## 3. Prevention matrix (order §7 "specifically prevent")

| Must not happen | Mechanism |
|---|---|
| One body-size slider scaling the whole character | Stature is DIR; every other absolute is DER through race allometry (UCCA-04). There is no global scale variable (G-1). Uniform scaling is FAIL by validator (PR L29) |
| Height silently scaling head, hands, feet, width or depth | Breadths, depths, head, hands and feet are stored as **race-relative values** and recomputed by **allometry, not identity scaling** (AD-C3). Allometry never multiplies by one factor (GO L224; CG L888) |
| Frame silently changing muscle or fat | The frame starting point writes only skeletal values: Slot 3, plus for Saurin hand/foot breadth (Slot 4) and the tail-base frame component (Slot 5) (MF L281; GR L249; GO L220; SA L4168). Slot 6 is outside its write set |
| Muscle or fat silently changing the skeleton | Composition writes only Slot 6. Thoracic depth, pelvic breadth and joint values are never DER from composition (VA L114; PK L182) |
| Sex becoming a body package | The sex selection only shifts generation centres and never moves stored values (AD-C6). Saurin's four shifts are centres inside identical bounds (§263) |
| Age becoming a frailty package | Age effects are canon-listed OFFSETS. Posture changes only "where individually appropriate" (ECR L245; CG L1937). Firewall validators (SA §130; GO L527; GR L534; PK L1481) |
| Ancestry becoming a Halvren body-percentage slider | Genealogy sets B envelopes only. No cluster or percentage control (UFCA G-4; HV L58, L105, L137) |
| Race becoming a hidden global morph axis | Race selects envelopes, distributions and bindings, never a blend weight. Changing race on an existing character requires **semantic re-mapping** (CG §198), never value carry-over |
| "Athletic", "slim", "heavy" becoming persistent hidden macro states | Starting presets are **write-and-vanish operations** (UFCA G-2 discipline). After writing, only ordinary DIR values exist. A provenance label may be kept as metadata with no driving effect (AD-C2, AD-C5) |

## 4. How presets write values without leaving hidden state

| # | Rule |
|---|---|
| P-1 | A preset (whole-character, frame, composition, presentation, surface, age or tail) is a **set of target DIR values**. Some are absolute (stature); most are race-relative |
| P-2 | Applying a preset runs the normal resolution order. Locks win; CONSTRAIN is reported |
| P-3 | After application **no reference to the preset drives anything**. Editing a region does not "pull back" toward the preset |
| P-4 | Optional provenance ("started from: Broad / Athletic / Coastal Soldier") may be stored as **non-driving metadata**. A reusable appearance never depends on it (order §12) |
| P-5 | Effects canon ties to a frame or composition **category** are computed from the **resolved values**, never from the label. The case: SA reachable tail length "~78 % Balanced / 80 % Broad / ~72 % Narrow high-fat", §256.5. The canonical category points stay authoritative; the curve between them is measurement-deferred (RM-UB-04; AD-C2) |

## 5. Dependency relations: body examples

| Relation | Canon example |
|---|---|
| FOLLOW | Tail muscularity and caudal fat follow Composition (SA §256.6–7). Limb circumference follows bone + muscle + fat (GR L251) |
| OFFSET | Regional muscle on overall muscularity (SK L102). Age effects on the individual body. Natural asymmetry on symmetric values. Facial soft tissue on body composition (UFCA) |
| CLAMP | Tail base from tail length (root sufficiency). Tail length capped by frame/composition. Saurin B ceiling vs thoracic depth/width guard (§263). Joint hard minimums (FN L115; VA L132). Saurin lower-trunk / pelvic requests beyond bounds → CONSTRAIN (L4248) |
| NEIGHBOR-ADJUST | Saurin: tail extremes keep pelvic support (SAU-CC-29). Grask: midface/lower-face (face, closed). Cogling: proximal segments accommodate distal redistribution (CG L145) |
| ENVELOPE | Frame → robusticity/joint starting tendencies (CG AC-9). Broad frame ↔ craniofacial presence, soft (DU L189). Foot breadth vs frame is a tendency only (GR L322–326). Halvren genealogy → B envelopes |
| REDISTRIBUTE | Saurin stature accounting (UCCA-04 §4), the only canon-named case |
| INVALID (FAIL) | Named combinations: DU L139; GR L255; GO L119–123, GOR-STRESS; PK L98, L205; CG L1050–1055; SA §158 and §256 FAIL list; HV joint-bridging L133 |

— Claude
