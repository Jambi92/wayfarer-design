# UFCA-03: Control Taxonomy & Dependency Model

**Author:** Claude (auditor / architecture analyst)
**Order:** `reviews/chatgpt-ufca-phase1-order.md` §6, §7, §11
**Status:** PROPOSAL for author review.
**Input:** UFCA-01, UFCA-02, `reviews/claude-pass2-r3-craniofacial-framework.md` (landmarks and indices), `reviews/claude-pass2-r5-reference-mesh-queue.md` (RM items)

## 1. The seven control classes

Every UFCA variable carries exactly one class per race binding.

| Code | Class | Definition | Player sees it? | Stored in the appearance record? |
|---|---|---|---|---|
| **DIR** | Direct anatomical control | The player edits a meaningful anatomical dimension | Yes | Yes |
| **DER** | Derived / coupled | The value follows from connected anatomy | Shown read-only, or not at all | Recomputed (never hand-stored) |
| **SOFT** | Soft-correlated | Population tendency or body-to-face correlation; sets defaults and generation weights. The player may override within valid anatomy | As a default, not a separate slider | The player's override is stored |
| **VAL** | Validator-only | Enforces coherence; never exposed | No; only its PASS / CONSTRAIN / FAIL messages | No |
| **LAT** | Preset latent variable | Used by generation and presets; never a literal slider | No | Optional (seed + generator version) |
| **PRES** | Presentation | Non-biological styling | Yes (slot 15 and Acquired) | Yes, in the presentation or acquired layers |
| **DIAG** | Diagnostic measurement | Comparison and QA only | No (QA tools only) | No |

**Firewall F-1 (proposed universal rule).** A quantity becomes DIR only if (a) race canon names it as a variable or control dimension, and (b) it is not a ratio or index whose only purpose is comparison.

Being measurable is never enough. All r3 indices (FPI, MPI, MdPI, CI, CBH, FVB, MVI, FDH, FVI, ORB, IOD, TBP, JDI, HSR), the Facial Diagnostic Domains (FD-*), the Durrim depth domains A–E and every GR-FACE / GOR-FACE / DU-FACE variation diagnostic are DIAG, VAL, or both. **None is a slider.**

## 2. Variable registry (by slot)

Columns:
- **Class** gives the default class; race exceptions are in brackets.
- **Measured by** gives the r3 landmark or index, where one exists.
- **Numbers** gives the RM item that must supply bounds. "—" means no number is needed for Phase 1 (bounds come from validators or the race's qualitative envelope).

### Slot 1: Head & Proportions

| Variable | Class | Measured by | Numbers |
|---|---|---|---|
| Head scale relative to stature | SA: **DIR** (±8 %, L4162). Others: **VAL/DIAG** (OPEN for GR, GO, PK, CG); exposure is author decision AD-U4 | HSR | RM-CF-10; RM-SR-04 |
| Facial soft-tissue composition (cheek, buccal, submental, periorbital fat) | **SOFT** from body composition, plus a DIR individual offset | — | — |

Basis for the soft-tissue row: never a deterministic facial-fat value (GO L338; SK L175 "pending validation"; CG L1458–1470; PK L410).

### Slot 2: Cranium & Forehead

| Variable | Class | Measured by | Numbers |
|---|---|---|---|
| Cranial length, breadth, vault height | **DIR** | CI, CBH | DU/GO tendency: RM-CF-06 |
| Posterior cranial depth/contour | DIR (SA, CG, PK) | — | — |
| Temporal breadth | DIR | — | — |
| Forehead height, slope, contour | DIR. SA: **Absent as a forehead**; the frontal slope is part of cranium/rostrum transition | — | — |
| SA structural-ridge prominence, transition strength, temporal definition, posterior contour | **DIR with a non-zero floor** (never toggled off, L692) | — | Structural-ridge numerics OPEN (L671) |

### Slot 3: Brow & Orbit

| Variable | Class | Measured by | Numbers |
|---|---|---|---|
| Skeletal brow projection/shape | **DIR** | G\* region; DU domain A (DIAG) | RM-SR-05 (DU) |
| Bony orbit size (breadth/height) | **DIR**. SA: DIR **driver** of the orbit-coupled set | ORB | RM-CF-08 |
| Orbital depth / orientation | DIR | — | — |
| Interorbital spacing | **DIR**. SA: **VAL (Bound-locked)**, tolerance OPEN (L4183) | IOD | RM-CF-08 |
| SA orbital-platform breadth, orbital rim | DIR | — | — |

### Slot 4: Eyes

| Variable | Class | Numbers / notes |
|---|---|---|
| Visible aperture width/height | **DIR**. PK/CG: DIR with an anti-enlargement ceiling (PK L297; CG L1199). SA: DIR **inside** the orbit coupling (L826) | RM-SR-04 (PK, CG) |
| Eye angle; lid shape/structure; canthal/corner relationships | DIR | — |
| **Eyeball (globe) size** | **DER from orbit, everywhere.** Never DIR | See §5.1 |
| Iris pigmentation / detail | **DIR** (Natural layer). Validity ≠ frequency | Frequencies OPEN |
| Sclera / ocular-tissue visibility | DIR for SA only (L2427 lists it). DU (L368 describes variation but names no control dimension): hidden pending AD-U12 §3.2. GO tint range OPEN; GR "comes later" | — |
| Pupil shape | SA: **species anatomy**; shape variation + dilation range DIR within vertical-elliptical. Others: **not exposed** (round, or OPEN for VA/HV) | — |
| Pupil dilation **state** | **PRES/preview only.** Never saved (SA L2437) | — |
| SA nictitating membrane | **VAL (Bound-locked)** species anatomy; direction/opacity OPEN | — |

### Slot 5: Cheeks & Midface / Rostrum & Lateral Face

| Variable | Class | Measured by | Numbers |
|---|---|---|---|
| Zygomatic breadth, projection, height | **DIR**. SA: **Absent** (no human zygoma; lateral face is DER from platform/rostrum/jaw) | Zy–Zy, TBP | RM-CF-06 (GO TSC) |
| Cheek soft-tissue fullness | **SOFT + DIR offset** | — | — |
| Midface height / vertical contribution | DIR | MVI | RM-CF-07 (GR) |
| Midface depth / maxillary projection | DIR. GR/GO: **range held to authored central values until the prognathism distribution is authored (OPEN)** | MPI, FDH | RM-CF-02…04 |
| SA rostral length, base width, anterior width, depth, dorsal contour, rostrum-to-orbit transition | **DIR** with coupled VAL | FPI | RM-CF-01…05 |
| **SA rostral index (FPI)** | **VAL + DIAG only. Never a slider.** Provisional floor 0.255 is protective canon | FPI | RM-CF-01…05 |

### Slot 6: Nose / Nasal Openings

| Variable | Class | Notes |
|---|---|---|
| Nasal root height/depth, bridge length/breadth/contour, projection, tip shape/rotation, alar breadth, nostril form | **DIR**, multidimensional. **Never one Nose Size** (DU L184; GR L366) | — |
| SA opening size, spacing, orientation, local contour | DIR | Must never form a nasal pyramid |

### Slot 7: Mouth / Mouth Line

| Variable | Class | Notes |
|---|---|---|
| Mouth width; upper/lower lip volume and balance; Cupid's bow; philtrum length/depth; corner position; oral projection | **DIR** | SA: lips **Absent** |
| SA mouth-line length; corner position; oral-margin expression | DIR | — |

### Slot 8: Jaw & Chin / Jaw

| Variable | Class | Measured by | Numbers |
|---|---|---|---|
| Mandibular breadth; ramus height; body depth; gonial angle/contour; lower-face height | **DIR** | JDI, MdPI | RM-CF-02…04 (projection) |
| Chin width, height, projection, shape | DIR. SA: **Absent** | Gn/Me | — |
| SA posterior jaw depth; anterior taper; mandibular angle | DIR, coupled to the rostrum | JDI | — |

### Slot 9: Ears

| Variable | Class | Notes |
|---|---|---|
| Family-specific parameter set (UFCA-04 §3) | **DIR** | Each family keeps its own variables |
| Family identity | **VAL (Bound-locked by race)** | Never a slider; never interpolated (MF L307) |
| HV mixed-ear parameter union (human foundation variables + elven variables) | DIR with **coupled VAL** (HV L198) | — |
| Ear mobility | **Not exposed (OPEN)** | — |

### Slots 10–12: Hair / Display, Facial Hair & Brows, Skin & Surface

| Variable | Class | Notes |
|---|---|---|
| Scalp-hair biology (hairline, density, texture, natural colour) | **DIR** (Natural) | Facial scope only |
| SA display family, count, attachment, spacing, base, length, thickness, taper, sweep, curvature, orientation, symmetry, crest, plates, surface, keratin colour, inherited arrangement | **DIR** with §260 VAL limits | Minimal is always selectable |
| Facial-hair capability, density, distribution pattern, natural colour; eyebrow density, thickness, shape, growth direction | **DIR** (Natural). Sex-related distributions: **SOFT, OPEN** | SA: Absent |
| Grooming, beard/brow styling, dye | **PRES** | — |
| Natural facial pigmentation, living-skin regional variation | DIR (Natural) | Lighting-invariant |
| SA facial scale fields (per field) and facial pattern | **DIR per field. No global scale size** (L4205) | Numerics OPEN |
| Acquired: scars, ear damage, keratin breakage, dental wear/loss | **PRES-layer (Acquired)** | Never randomized as Biological |

### Slots 13–14: Asymmetry and Age

| Variable | Class | Notes |
|---|---|---|
| Per-region left/right offsets | **DIR**, as signed offsets on the symmetric value | — |
| Restore Symmetry | Operation (zeros the offsets) | — |
| Naturalize Face | Operation, **proposed** (SK L183; VA L294) | Pending test |
| Apparent Biological Age | **DIR** systemic driver | — |
| Regional age effects (soft-tissue volume, elasticity, periorbital, jawline, neck, scale-edge wear, keratin wear, dental wear) | **DER** from Apparent Biological Age, applied as offsets | Never alter skeletal racial identity (DU L377; GO L527) |
| Age Presentation | **PRES** | — |

### Systemic soft inputs

| Variable | Class | Notes |
|---|---|---|
| Sex-related facial tendency | **SOFT only, never a control** (R-SEX). Default "no shift". DU/GR/GO/PK/CG magnitude OPEN. **SA: zero (closed)** | See §5.3 |
| Body composition, frame | Body-level SOFT inputs to slot 1 | Frame never changes the SA skull (L4166) |

### Latent variables (LAT, never sliders)

- Population correlated factors: SG soft correlations (L348); DU "different subsets strongly" (L252).
- HV inheritance clusters: craniofacial, ear (L33–41).
- SA driver set: §264.
- Randomization strength.
- Coverage tags on presets.

## 3. Global versus regional controls (order §7)

**Rule G-1 (proposed).** No global control is stored as hidden state that drives several regions. The only stored systemic values are:
- **Apparent Biological Age**: canon systemic driver (age triad).
- **Facial soft-tissue offset**: individual deviation from the body-composition expectation.
- **Head scale**: Saurin only, unless AD-U4 extends it.
- **Asymmetry offsets**: per region, not global.

**Rule G-2 (proposed): relationship tools are operations, not state.** A broad edit, such as "more rostrally expressed" or "broader face", may exist only as a **tool**:
- It writes ordinary values into the regional DIR controls, in proportions fixed by the race's own canon relationship.
- It then disappears. Afterwards the player sees and owns every regional value it changed.
- Nothing remains that later re-drives the face silently.

**Rule G-3 (proposed): eligibility for a relationship tool.** A tool may exist only if race canon names the relationship as one coherent system. Tools are **refused** for:
- face width (DU L170)
- face depth (DU L265; GO L304)
- verticality (GR L473)
- TSC (GO L425)
- "elfness", "humanity", ancestry percentage (HV L58)
- masculinity / femininity (R-SEX)
- beauty, age face, race face (PK L412; CG L1568; GR L406; GO L371)

The **only candidate** found in canon is Saurin compact ↔ rostrally expressed "within one system" (SA L738). Even that is listed as author decision AD-U3, not adopted.

**Rule G-4: Halvren.** Phenotype expression is reached through the ordinary DIR controls plus ancestry-informed presets. The valid envelope of those controls is set by **ancestry-derived constraints (B)** from genealogy (A). There is no expression slider or percentage (HV L58, L227, L463). This meets order §7 bullet 5: phenotype expression is exposed; genealogy is not an appearance percentage.

**Rule G-5: randomization and presets** may use LAT variables (UFCA-05). Their output is ordinary DIR values. A preset is therefore editable like any other face.

## 4. Diagnostic measurements: explicit non-slider list

These stay DIAG or VAL even though each could be measured and exposed:

| Measurement | Source |
|---|---|
| FPI (Saurin rostral index) | §259 |
| FVB, MVI (Grask verticality); "not solely height-to-width" | GR L473 |
| FDH and Durrim depth domains A–E; "never five fully independent sliders" | DU L300 |
| TBP (Gorrund TSC) | — |
| CBH (Durrim / Gorrund cranial breadth) | — |
| FVI (Cogling / Pipkin face-to-vault) | — |
| HSR (non-Saurin) | — |
| ORB-vs-aperture ratios | — |
| FD-STRUCT / SOFT / SURF / HAIR / PRES / OBS | DU L280, L330; CG §101A |
| GR-FACE-02…13, GOR-FACE-02…15, DU-FACE-02…11, DU-DEPTH-01…03 | Variation diagnostics, "never phenotype packages" (GR L410) |
| Matched-scale and cross-section tests | GO L437; DU L315 (never player-facing) |

## 5. Dispositions needing author confirmation

### 5.1 "Eye size" (SK L169, SG L216, VA L252)

**Proposal:** split "eye size" into:
- orbit size (slot 3, DIR);
- visible aperture (slot 4a, DIR);
- eyeball (DER from orbit).

The roster-wide rule supports this: DU L179, GR L356, GO L308, PK L289, CG L1195, the ECR terminology rule (ECR L51, L145), and the Saurin coupling. **No race loses capability.** Flagged as AC-U1.

### 5.2 Saurin "orbital spacing" (§73 L1190)

**Disposition:** not exposed. §259 L4183 locks it and later canon governs (SA L4034–4038). Recorded for completeness; no decision needed.

### 5.3 Cogling "sex-related anatomy" capability (L1560)

**Proposal:**
- The capability is met by the body-level sex-related anatomy selection plus Cogling's SOFT facial distribution (magnitude OPEN).
- No face-level sex control exists, because R-SEX forbids sex forcing the face.
- COG-FACE-21 and 21A carry forward.

Flagged as AC-U2.

## 6. Dependency model (order §7)

### 6.1 Relation types

| Type | Behaviour | When to use (decision rule) | Canon examples |
|---|---|---|---|
| **FOLLOW** | The child equals a function of the parent; it has no independent value | Canon says structures scale **together** as one unit | SA orbit size → lids, aperture frame, eyeball (L4181); eyeball follows orbit roster-wide (§5.1) |
| **OFFSET** | The child stores an individual offset; the parent moves the base, and the offset is kept | A systemic driver modifies individual anatomy, and canon requires the individual to stay recognizable | Age effects on top of the young-adult face ("same person", MF L124); soft tissue vs body composition (GO L338); asymmetry on the symmetric value |
| **CLAMP** | The parent sets the child's valid interval; the child is clamped and the player's **intended** value is retained for restoration | Canon gives a floor or ceiling that depends on another value | SA rostral minimum rises with cranial length (L4178); SA anterior width ≤ base width (L4180); PK/CG aperture ceiling relative to face (PK L297) |
| **REDISTRIBUTE** | One edit is spread across several unlocked DIR controls by fixed proportions | **Only** inside an approved relationship tool (G-2), never automatically | (None adopted; candidate AD-U3) |
| **NEIGHBOR-ADJUST** | An edit raises or lowers connected **unlocked** neighbours to keep a named relation, then reports it | Canon names an explicit consequence in connected anatomy | SA rostrum > +10 % → rostral depth and posterior jaw depth ≥ reference (L4179); GO cranial breadth shifts the envelopes of orbit spacing, zygoma and jaw (L371); the envelope shifts, values move only if out of envelope |
| **ENVELOPE** | A soft relationship; the child's *distribution* shifts but its value is untouched unless it leaves the valid envelope | Population tendencies (PR "weighted distributions or validity envelopes rather than hard creator dependencies", per SG extraction PR L18) | DU frame ↔ face, never Broad Frame → Broad Face (L189); CG frame → robusticity starting values (AC-9); GO "valid envelopes rather than hard-locking every correlation" (L371) |
| **INVALID** | A combination that no unlocked adjustment can repair. Outcome: **FAIL**; the system explains and offers choices, and never silently resets | Named invalid combinations, or a locked value that would force an invalid parent | GR L406 (strongest brow + deepest orbit + smallest opening; maximum ear length/sweep + smallest base); CG §101 toddler, mini-elf, comic-nose and oversized-ear combinations; HV L198 (narrow human base + extreme elven length/projection/sweep); SA locked child forcing invalid parent (L2362) |

### 6.2 Resolution order

The proposed universal order adopts Saurin §159 and Cogling §196 as the roster rule (author decision AD-U2):

1. Apply FOLLOW and DER recomputation.
2. Test the edited value against CLAMP intervals. If outside, clamp and keep the intent value.
3. Apply NEIGHBOR-ADJUST to **unlocked** neighbours only.
4. Re-test every validator in the region and its neighbours:
   - **PASS:** done.
   - **CONSTRAIN:** done, with a message naming what moved and why.
   - **FAIL:** reject the edit and offer resolutions (unlock a neighbour, accept a clamp, or revert).
5. **Locks are absolute.** A locked attribute is never moved by the system. A locked child can never force an invalid parent (SA L2362; CG §196).
6. **No silent reset** (SA L2584–2588).

### 6.3 Cross-region seams

Connected-anatomy continuity between slots is preserved by validators, not by merging slots. Examples:
- nose–philtrum–lip–jaw (SG L220);
- orbit–zygoma–maxilla–mandible junctions (CG L1128);
- brow → temporal/postorbital (SA L4172).

Mesh-level continuity is technical architecture: OPEN and out of Phase 1.

— Claude
