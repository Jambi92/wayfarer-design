# UCCA-02: Proposed Universal Creator Navigation

**Author:** Claude (auditor / architecture analyst)
**Order:** `reviews/chatgpt-ucca-phase1-order.md` §6
**Status:** PROPOSAL for author review.
**Inputs:** UCCA-01, closed `decisions/UFCA_V1.md`

## 1. Model

UCCA reuses the closed UFCA **slot / binding model** (UFCA_V1 §2, §4) for the whole character:

- A **slot** is navigation, never anatomy.
- Each population binds each slot as **Bound**, **Bound-locked** or **Absent** (hidden, never a dead control).
- Each binding carries its own label, anatomy family, control set and validators.
- **A shared slot never by itself authorizes a control** (UFCA AD-U12 rule, extended to the body as AD-C17).

## 2. Proposed hierarchy (15 slots)

| # | Slot | Contents | Universal / conditional |
|---|---|---|---|
| 0 | **Race & Lineage** | Race selection. **Halvren only:** optional genealogy entry (UFCA §11 layer A), which sets ancestry-derived constraints (layer B). **Never a body or face slider** | Universal; Lineage panel Halvren-only |
| 1 | **Starting Character** | Whole-character presets (race libraries); whole and selective randomization; strength (Subtle / Diverse / Extreme); lock overview. **Simple Mode ends here** | Universal |
| 2 | **Stature & Proportions** | Stature; torso and axial vertical contribution; neck length; arm length and segment distribution; leg length and segment distribution. **Saurin:** head-to-body (±8 %). Head-to-stature is VAL / DIAG elsewhere | Universal; contents race-bound |
| 3 | **Skeletal Frame** | Frame starting point (Narrow / Balanced / Broad) plus the continuous skeletal breadth/depth variables: shoulder/clavicular breadth, thoracic width, thoracic depth, pelvic width (depth where canon names it), joint scale, long-bone robusticity, neck skeletal depth (Saurin) | Universal; contents race-bound |
| 4 | **Hands & Feet** | Multidimensional hand and foot variables (never one size scalar). **Saurin:** claws. **Cogling:** finger internal distribution | Universal; contents race-bound |
| 5 | **Tail** | Saurin tail: length (driver), base, taper, cross-section, segment/curvature, resting carriage, proximal/distal mass character, restrained dorsal keratin, tail pattern view. **No on/off** | **Conditional: Saurin only; Absent for the other 12** |
| 6 | **Physical Composition** | Current Muscularity (overall + regional); Body-Fat Amount; Body-Fat Distribution (regional); Muscular Development Capacity where exposed (AD-C4). Composition starting points (AD-C5) | Universal |
| 7 | **Sex-Related Anatomy** | Body-level sex-related anatomy selection (a soft-distribution input under R-SEX, never a package) and race-canon sex-related tissue controls (**Saurin E / B**) | Universal selection; tissue controls Saurin-only |
| 8 | **Face** | Routes into the closed UFCA 16-slot hierarchy. UCCA adds nothing inside it | Universal (UFCA) |
| 9 | **Hair & Display** | Scalp-hair biology (shared with UFCA slot 10); **body-hair biology** where bound (AD-C7); Saurin cranial display (UFCA slot 10) and optional restrained body continuation (SA §101a). Facial hair and brows stay in UFCA slot 11 | Universal; body hair conditional; Saurin: hair Absent, display Bound |
| 10 | **Skin & Integument** | Natural layer: pigmentation (multidimensional), undertone, regional variation, natural marks. **Saurin:** Regional Scale Architecture fields, pattern, claw keratin colour. Environmental layer sub-panel (tanning, weathering, dirt, wetness) | Universal; Saurin scale/pattern conditional |
| 11 | **Age** | **One Apparent Biological Age driver for the whole character.** This is the same variable as UFCA slot 14, shown in both places. Body and surface age effects are coupled underneath. Chronological Age is character data; Age Presentation sits in slot 14 | Universal |
| 12 | **Asymmetry & Acquired History** | Natural body asymmetry where bound (Saurin canon; others per AD-C8). **Acquired** layer: scars, burns, damaged scales, chipped claws, acquired marks. Facial asymmetry stays in UFCA slot 13 | Universal Acquired; natural body asymmetry conditional |
| 13 | **Body Language** | Idle / stance / gesture presentation presets. They never alter Anatomical Resting Alignment | Universal |
| 14 | **Presentation** | Hair styling and grooming; cosmetics, paint, Applied markings; jewellery; clothing/gear preview; Age Presentation; culture / birthplace / background presentation presets; creator camera and preview lighting | Universal |

## 3. Evaluation of the order's candidate structure (§6)

| Candidate category | Disposition | Reason |
|---|---|---|
| 0 Starting Character / Presets | **Kept as slot 1, with Race & Lineage before it** | Race must precede presets. Halvren genealogy must precede generation, because it sets envelope B (UFCA §11) |
| 1 Stature & Global Proportions | **Renamed: Stature & Proportions** | "Global" must not imply a global scale (B-1; UFCA G-1). Stature is a real stored variable; proportions are regional shares |
| 2 Skeletal Frame | **Kept, broadened** to hold every skeletal breadth/depth/joint/robusticity variable | Frame *is* the continuous skeletal configuration (MF L285; AE L134). Splitting breadths across body-region slots would scatter one system |
| 3 Torso & Axial / 4 Shoulders / 5 Pelvis / 6 Arms & Hands / 7 Legs & Feet | **Not top-level.** Lengths and segment shares are nested in slot 2; breadths/depths in slot 3; hands and feet in slot 4 | Region-based top-level slots would duplicate each region across lengths, breadths and composition. Canon organizes by system: frame vs proportion vs composition (PR L12). Regions survive as **sub-panels** inside slots 2, 3 and 6 |
| 8 Physical Composition | **Kept** (slot 6) | PR L12, L14 |
| 9 Population-Specific Anatomy | **Rejected as a generic slot.** Replaced by a **conditional Tail slot** (5) and race-bound contents elsewhere | Only Saurin has body structures with no homologue. The ALPC, LSCTA, FSEA and Compact Structural Concentration anchors are **validators, not controls** (GO L711; PK L135; CG L37). A generic slot would be empty for 12 races, and hide the tail, a primary carrier, behind a vague name |
| 10 Skin / Integument | **Kept** (slot 10) | — |
| 11 Hair / Biological Display | **Kept** (slot 9) | Mirrors the UFCA Hair / Cranial Display routing |
| 12 Face → UFCA | **Kept** (slot 8) | UFCA closed and authoritative (order §3.23) |
| 13 Age | **Kept** (slot 11), with **one** driver shared with UFCA | Two age drivers would let face and body age diverge silently |
| 14 Asymmetry & Acquired History | **Kept** (slot 12) | Natural asymmetry and Acquired stay distinct, as in UFCA |
| 15 Presentation | **Kept** (slot 14); **Body Language split out** (slot 13) | PR L21: body language must never write anatomy. A separate slot makes the boundary visible |
| — | **Added: Sex-Related Anatomy** (slot 7) | Needed as a body-level soft input (R-SEX) and as the home of Saurin E/B, which must never sit under fat (SA L4232) |

## 4. The order's specific questions

| Question | Answer |
|---|---|
| **Truly universal slots** | 0 (race), 1, 2, 3, 4, 6, 7 (selection), 8, 10, 11, 12 (Acquired), 13, 14 |
| **Conditional slots** | 5 Tail (Saurin only); the Lineage panel (Halvren only); body hair in slot 9 (AD-C7); natural body asymmetry in slot 12 (AD-C8); Saurin E/B in slot 7; scale/pattern/claw contents in slots 4 and 10 |
| **Population-specific labels and bindings** | Slot 4 "Hands, Feet & Claws" (Saurin). Slot 9 "Cranial Display" (Saurin; hair Absent). Slot 10 "Scales & Pattern" (Saurin). Slot 3 contents differ by race (UCCA-05 §3). Slot 2 contents differ by race (UCCA-04) |
| **Nested rather than top-level** | Torso/axial, neck, arms and legs (inside 2 and 3); regional muscle and regional fat (inside 6); Environmental layer (inside 10); Lineage (inside 0) |
| **Absent for some populations** | Tail (12 races). Scalp and body hair (Saurin). Facial hair and brows (Saurin, inside UFCA). Saurin-specific contents (all others). E/B (all but Saurin) |
| **Does the Saurin tail need its own top-level category?** | **Yes, proposed.** It is mandatory biology with its own large control set (§145), its own lock group (§144), its own coupled validators (§256) and its own selective randomization (§11a L220). It is a primary identity carrier (L3547–3553). Folding it into a generic slot would hide it; folding it into Stature & Proportions would bury a ten-variable system. Tail muscularity and fat stay in **Composition** (§256.6–7); only the panel *displays* them read-only |
| **Body hair: Hair, Surface or a conditional slot?** | **Hair & Display (slot 9).** Hair biology (texture, colour relationship, density) is one system across scalp, body and face (DU L366; GR L518; GO L517). Body hair stays **conditional**: bound for PK and CG (canon states variation); hidden for DU, GR, GO (OPEN) and for MF, SK, SG, FN, AE, VA, HV (SILENT) pending AD-C7; Absent for Saurin |
| **How does Halvren genealogy enter without becoming a body slider?** | Through **slot 0, Lineage panel only** (optional). Genealogy (A) computes ancestry-derived constraint envelopes (B) for every body and face slot. The player then edits phenotype (C) with the ordinary controls. No percentage, cluster or "human ↔ elf" control appears anywhere (HV L58, L105, L137, L467; UFCA §11). Changing genealogy never silently rewrites existing appearance (HV L394) |

## 5. Simple Mode, Advanced Mode, Quick / Detailed

| Mode | Flow / content |
|---|---|
| **Simple Mode** | Race → (Halvren: optional lineage) → Starting Character preset → Confirm. Slot 1 shuffle uses the same generator. **No simplified fake body** (SA L2250) |
| **Advanced Mode** | Same tree, all slots |
| **Quick controls** | One curated DIR control per major dimension in each Bound slot. Example for MF canon (L53): starting frame, height, overall muscularity, overall fat amount and distribution |
| **Detailed controls** | Full regional sets |

**Quick controls are never hidden macros** (UFCA §8 discipline).

## 6. Binding summary

| Slot | MF SK SG | FN AE VA | HV | DU | GR | GO | PK | CG | SA |
|---|---|---|---|---|---|---|---|---|---|
| 0 Race & Lineage | B | B | B + Lineage | B | B | B | B | B | B |
| 2 Stature & Proportions | B | B | B (central envelope; tails held) | B | B | B | B | B | B (+ head-to-body) |
| 3 Skeletal Frame | B | B | B (ancestry-dependent ranges) | B | B (breadth only) | B (breadth only) | B | B (AC-9) | B (§258 scope) |
| 4 Hands & Feet | B | B | B | B | B | B | B | B (+ fingers) | B (+ claws) |
| 5 Tail | A | A | A | A | A | A | A | A | **B** |
| 6 Composition | B | B | B | B | B | B | B | B | B |
| 7 Sex-Related Anatomy | B (selection) | B | B (selection; system is a Class B dependency) | B | B | B | B | B | B (+ E/B) |
| 9 Body hair | hidden (AD-C7) | hidden | hidden | hidden (OPEN) | hidden (OPEN) | hidden (OPEN) | **B** | **B** | A |
| 10 Skin & Integument | Skin | Skin | Skin | Skin | Skin | Skin | Skin | Skin | **Scales & Pattern** |
| 12 Natural body asymmetry | hidden (AD-C8) | hidden | hidden | hidden | hidden | hidden | hidden | hidden | **B** |

B = Bound; A = Absent (hidden); "hidden" = held pending author decision or OPEN. All other slots are Bound for every race.

— Claude
