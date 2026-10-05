# UFCA-02: Proposed Universal Navigation & Control Hierarchy

**Author:** Claude (auditor / architecture analyst)
**Order:** `reviews/chatgpt-ufca-phase1-order.md` §5
**Status:** PROPOSAL for author review. Nothing here is canon until ChatGPT accepts it.
**Input:** UFCA-01 and `reviews/ufca-evidence/`

## 1. Design approach: slots and bindings

The hierarchy is a set of **navigation slots**. A slot is a place a player goes. It is not an anatomical structure. Each race supplies a **binding** for each slot:

| Binding field | Content |
|---|---|
| Label | The name the player sees for this race (it may differ by race) |
| Anatomy family | The race's own anatomical system behind the slot (for example, human auricle versus recessed auricular opening) |
| Control set | The race's direct controls in that slot (UFCA-03) |
| Validators | The race's validity rules for that slot (UFCA-06) |
| State | **Bound**, **Bound-locked** (anatomy exists but no editable control is authorized) or **Absent** (no such anatomy; the slot is hidden, never shown as a dead control) |

This applies order §2.2 ("shared navigation does not require shared anatomy") directly. It also meets Pass 2 creator requirement 1: race-conditional region sets, with biologically absent regions hidden (`claude-pass2-03` §7.1).

**What the hierarchy is not:**
- It is **not** the r3 landmark framework. Landmarks and indices stay diagnostic (UFCA-03 §4).
- It is **not** a mesh, morph or bone layout. Technical architecture is OPEN in every spec.

## 2. The proposed hierarchy

Sixteen slots (0–15) in four groups. Smallest-hierarchy test: every slot holds requirements from at least two races, or holds a routing that race canon explicitly permits (Hair → Cranial Display, SA L604, L2445). Every UFCA-01 requirement lands in exactly one slot, or is explicitly outside the face (§5).

### Group 0: Start

| # | Slot | Scope | Universal / conditional |
|---|---|---|---|
| 0 | **Starting Face** | Face presets (valid system outputs, UFCA-05), whole-face or regional randomization, locks overview. Halvren: ancestry-informed starting faces, filtered by genealogy when genealogy is set | Universal |

### Group 1: Structure (skeletal and soft-tissue anatomy)

| # | Slot | Scope | Universal / conditional |
|---|---|---|---|
| 1 | **Head & Proportions** | Head scale relative to stature where a race authorizes it; facial soft-tissue composition (follows body composition with an individual offset); race-named relationship tools, if the author approves any (UFCA-03 §3) | Universal slot; contents conditional |
| 2 | **Cranium & Forehead** | Vault length, breadth and height; posterior contour; temporal breadth; forehead height, slope and contour. Saurin: frontal slope, plus **structural-ridge prominence** (skull anatomy, never zero) | Universal |
| 3 | **Brow & Orbit** | Skeletal brow; bony orbit size, depth and orientation; interorbital spacing. Saurin: orbital platform and rim; spacing is Bound-locked (§259) | Universal |
| 4 | **Eyes** | Two nested panels. **4a External Eye:** aperture width and height, angle, lids, corner/canthal relationships. **4b Ocular:** iris pigmentation and detail; sclera/ocular tissue where canon allows; pupil (Saurin shape and dilation range only); dilation preview. Saurin nictitating membrane: Bound-locked. Magic eye effects are excluded (§5) | Universal; 4b contents conditional |
| 5 | **Cheeks & Midface** | Zygomatic breadth, projection and height; cheek soft tissue; midface height and depth; maxillary projection. Saurin label: **Rostrum & Lateral Face** (rostral length, base width, anterior width, depth, dorsal contour, rostrum-to-orbit transition) | Universal, renamed for Saurin |
| 6 | **Nose** | Nasal root, bridge, length, projection, tip, alar region, nostrils. Saurin label: **Nasal Openings** (size, spacing, orientation, local contour on the rostral terminal plane) | Universal, renamed for Saurin |
| 7 | **Mouth** | Width, lip volumes and relationships, Cupid's bow, philtrum, corners, projection. Saurin label: **Mouth Line** (mouth-line length, corner position, oral-margin expression); no lips | Universal, renamed for Saurin |
| 8 | **Jaw & Chin** | Mandibular breadth, ramus, body depth, gonial angle, lower-face height; chin width, height and projection. Saurin label: **Jaw** (posterior jaw depth, mandibular-body depth, width, anterior taper, mandibular angle); the chin sub-panel is Absent | Universal; chin conditional |
| 9 | **Ears** | Routed to the race's **ear-architecture family** (UFCA-04 §3). Each family has its own parameter set. Saurin label: **Auricular Openings** | Universal slot; family-specific contents |

### Group 2: Surface and hair biology

| # | Slot | Scope | Universal / conditional |
|---|---|---|---|
| 10 | **Hair / Cranial Display** | Haired races: scalp-hair biology (hairline, density, texture, natural colour). Saurin: **Cranial Display** (family, count, attachment, length, sweep, crest, plates, keratin colour). Saurin canon permits this routing (§150 L2445 "may present"; L604). Adopting it as the universal structure is part of AD-U1. Hair *styling* belongs to Presentation | Universal slot; Saurin routing permitted by canon |
| 11 | **Facial Hair & Brows** | Facial-hair biology (capability, density, distribution pattern, natural colour); eyebrow-hair biology (density, thickness, shape, growth direction). Saurin: **Absent** (biologically empty; §117, L2445) | Conditional (Absent for Saurin) |
| 12 | **Skin & Surface** | Facial natural pigmentation and living-skin regional variation; Saurin **facial scale fields** and facial pattern (field-aware; no global scale size). Sub-panel **Acquired:** scars, ear notches, keratin breakage, dental wear or loss. These are kept apart from Asymmetry (order §2.8) | Universal; scale fields conditional |

### Group 3: Systemic edits and presentation

| # | Slot | Scope | Universal / conditional |
|---|---|---|---|
| 13 | **Asymmetry** | Per-region left/right offsets for every Bound region that has stated asymmetry. **Restore Symmetry** is an operation; **Naturalize Face** is a proposed operation (SK L183, VA L294), pending test | Universal slot. Pipkin binding needs author confirmation (UFCA-07 AC-U3) |
| 14 | **Age** | **Apparent Biological Age** as a systemic anatomical driver, with regional age effects coupled underneath. Chronological Age is character data, not appearance. Age Presentation belongs to Presentation | Universal |
| 15 | **Presentation** | Cosmetics; brow and beard grooming and styling; hairstyle; Applied markings; jewellery; Saurin applied display decoration (polish, paint, wraps); preview-only tools (expression, lighting, dilation); creator camera | Universal |

The Hair / Cranial Display, Facial Hair & Brows and Skin & Surface slots overlap with whole-body systems. UFCA defines only their **facial** scope and their **navigation routing**. Scalp-hair styling and whole-body skin systems are outside UFCA.

## 3. Disposition of the order's starting hypothesis (§5)

| Hypothesis category | Disposition | Reason |
|---|---|---|
| Face Preset / Starting Face | **Kept** (slot 0) | Universal entry point; Simple Mode ends here |
| Global Craniofacial Relationships | **Renamed and narrowed** to *Head & Proportions* (slot 1) | Canon bans whole-face scalars: Face Width (DU L170), Face Depth (DU L265, GO L304), verticality ratio (GR L473), TSC slider (GO L425), master race faces (PK L412, CG L1568). Only true stored relationships stay: race-authorized head scale, soft-tissue offset and approved relationship tools |
| Cranium & Forehead | **Kept** (slot 2) | Universal |
| Brow & Orbit | **Kept** (slot 3) | Bony brow and bony orbit sit together in every spec. Separating orbit from the external eye is mandatory (X-1) |
| Eyes / External Eye | **Kept and nested** (slot 4: 4a External, 4b Ocular) | The ECR five-system rule (ECR L94) and HV L181 require orbit ≠ external eye ≠ ocular ≠ pigmentation ≠ magic. Orbit lives in slot 3; magic is excluded |
| Cheeks & Midface | **Kept**; Saurin renamed *Rostrum & Lateral Face* | For Saurin the midface *is* the rostrum (SA L663). The human zygoma is not copied (SA L946) |
| Nose / Rostrum / Homologous Midface Projection | **Split.** The nose stays slot 6 (Saurin: *Nasal Openings*); rostral projection moves to slot 5 | Durrim: "midface identity is never nasal size" (L245). Grask and Gorrund also separate midface from nose. Saurin nostrils sit on the rostrum's terminal plane (L690); rostral projection is midface anatomy |
| Mouth / Oral Region | **Kept** (slot 7); Saurin renamed *Mouth Line* | SA L871–889 |
| Jaw & Chin / Mandibular Region | **Kept** (slot 8); chin sub-panel Absent for Saurin | SA L4172 |
| Ears / Auricular Region | **Kept** (slot 9), family-routed | Eight families (UFCA-04 §3) |
| Race-Specific Cranial Structures | **Not a separate universal slot. Proposed dissolution (AD-U1), consistent with Saurin canon:** Saurin structural ridges go to slot 2 (skull, §36a, L692) and keratin displays to slot 10 (§150, L2445) | No other race has such structures. A separate slot would duplicate Saurin's canon routing and show a dead slot to 12 races |
| Asymmetry | **Kept** (slot 13), separate from Acquired | Order §2.8; SA L2164 |
| Age-related Anatomy | **Kept** (slot 14) as the Apparent Biological Age driver | Age triad (PR L16 and specs) |
| Surface / Facial Biology | **Split** into slots 10, 11 and 12 | Hair, facial hair and skin have different races Absent or Bound (Saurin) and different layer homes |
| Presentation | **Kept** (slot 15) | Order §2.10 |

**Added (not in the hypothesis):**
- **Facial Hair & Brows** as its own slot, because it is Absent for exactly one race and canon-routed.
- **Acquired** as a sub-panel of Skin & Surface, because acquired damage must stay separate from biological asymmetry.

## 4. Simple Mode, Advanced Mode, and Quick / Detailed controls

| Mode | Flow | Face scope |
|---|---|---|
| **Simple Mode** | Race → (Halvren: optional genealogy) → Preset → Confirm | Slot 0 only. Includes regional randomization, if offered (UFCA-05) |
| **Advanced Mode, Quick controls** | Same tree | One curated control per major dimension in each Bound slot |
| **Advanced Mode, Detailed controls** | Same tree | The full control set, plus slot 13 (Asymmetry) |

Both modes use one appearance record (PR; SA §138–139; PK §22; CG §191; AE L431; VA L474). Marchfolk's v1.2 tiers (face presets / quick / detailed, L106–112) map onto this one-to-one. The Pass 2 rename to "Quick / Detailed controls" is preserved.

**Quick-control curation rule (proposed):** a quick control is always one of the race's own direct controls. It is never a hidden macro. A quick control may *be* an approved relationship tool (UFCA-03 §3) only if the author approves that tool.

## 5. Kept out of the face hierarchy

| Item | Where it goes | Basis |
|---|---|---|
| Halvren **genealogy** (A) | A non-appearance **Lineage** step before Starting Face; it is never a slot control | HV L463 |
| Chronological Age | Character data | Age triad |
| Magical eye effects, glow, emissive marks | Effects systems outside biology; never stored as iris or ocular data | AE L305–312; VA L264; SA L1588; GR L562; GO L537 |
| Expression | Animation and presentation; preview only, never stored as anatomy | CG L1295; SA L714 |
| Lighting | Preview only; stored biology is lighting-invariant | ECR L165; SA SAU-CC-20 |
| Ear mobility, low-light physiology, tusk-like canines | Not exposed: OPEN | UFCA-01 §24 |
| Dentition controls | Not exposed; species default plus Acquired history | No race defines one. Author decision AD-U5 |
| Body composition, frame, sex-related anatomy selection | Body-level systems that feed slots 1 and 14 only as soft inputs | R-SEX; GO L338 |

## 6. Race binding summary

| Slot | MF SK SG | FN AE VA | HV | DU | GR | GO | PK | CG | SA |
|---|---|---|---|---|---|---|---|---|---|
| 0 Starting Face | B | B | B (ancestry-informed) | B | B | B | B | B | B |
| 1 Head & Proportions | B (soft tissue) | B | B | B | B | B | B (anti-juvenile) | B (anti-juvenile) | B (head scale ±8 %) |
| 2 Cranium & Forehead | B | B | B | B | B | B | B | B | B (+ structural ridge) |
| 3 Brow & Orbit | B | B | B | B | B | B | B | B | B; spacing **L** |
| 4a External Eye | B | B | B | B | B | B | B | B | B (inside orbit coupling) |
| 4b Ocular | B (iris) | B (iris) | B (iris, never averaged) | B | B | B | B | B | B (iris, pupil shape and dilation; membrane **L**) |
| 5 Cheeks & Midface | B | B | B | B | B | B | B | B | B as *Rostrum & Lateral Face* |
| 6 Nose | B | B | B | B | B | B | B | B | B as *Nasal Openings* |
| 7 Mouth | B | B | B | B | B | B | B | B | B as *Mouth Line* |
| 8 Jaw & Chin | B | B | B | B | B | B | B | B | B as *Jaw*; chin **A** |
| 9 Ears | Human auricle | Elven taper | Mixed coupled | Human-like | Folded late-taper | Deep-bowl | Compact rounded | Fine folded | Recessed opening |
| 10 Hair / Display | Hair | Hair | Hair | Hair | Hair | Hair | Hair | Hair | **Cranial Display** |
| 11 Facial Hair & Brows | B | B | B | B | B | B | B | B | **A** |
| 12 Skin & Surface | B | B | B | B | B | B | B | B | B (+ scale fields) |
| 13 Asymmetry | B | B | B | B | B | B | B? (AC-U3) | B | B |
| 14 Age | B | B | B | B | B | B | B | B | B |
| 15 Presentation | B | B | B | B | B | B | B | B | B (no human hair or beard assets) |

B = Bound; L = Bound-locked; A = Absent (hidden).

— Claude
