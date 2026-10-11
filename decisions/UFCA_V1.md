# Universal Facial Customization Architecture (UFCA) v1

**Status:** **CLOSED / FINAL-AUTHOR ACCEPTED** (October 5, 2026; `reviews/chatgpt-ufca-final-closure-order.md`). Canonicalized in UFCA Phase 2 (`reviews/chatgpt-ufca-phase2-canonicalization-order.md`). See §21 for what closure freezes.
**Phase:** DESIGN ONLY. This document defines creator **design behaviour**. It does not define UE5 mesh, topology, morph, bone, rig, camera or UI implementation (§20).
**Sources:**
- Phase 1 package: `reviews/claude-ufca-01…08`
- Per-race evidence: `reviews/ufca-evidence/`
- Author decisions: AD-U1…AD-U12 and AC-U1…AC-U4

## 1. Purpose and authority

UFCA is the single creator-facing facial architecture for all 13 playable populations. It gives every population one shared navigation and validation language. It does **not** give them shared anatomy, topology, morphs or ranges.

**Authority:**
- UFCA is a roster-wide rule document at PROJECT_RULES level (authority level 2).
- It governs facial **creator organization**: navigation, control classes, dependencies, presets, randomization and validation structure.
- Each race spec (level 1) keeps governing that population's **anatomy**, tendencies, bounds, identity statements, locked tests and OPEN items.
- If a race spec's provisional facial control organization differs from UFCA, UFCA governs the organization. The race requirement underneath is preserved and routed to its UFCA home (§10).
- Nothing in UFCA authorizes anatomy that a race spec does not state.

## 2. Slot / binding model

A **slot** is a navigation place. It is not an anatomical structure. Shared navigation never implies anatomical equivalence.

Each population supplies a **binding** for each slot:

| Binding field | Content |
|---|---|
| Label | The name the player sees (it may differ by population) |
| Anatomy family | The population's own anatomical system behind the slot |
| Control set | Its direct controls in that slot |
| Validators | Its validity rules for that slot |
| State | Bound, Bound-locked or Absent (§4) |

**A shared slot never by itself authorizes a control** (AD-U12).

## 3. The 16-slot navigation hierarchy

| # | Slot | Scope |
|---|---|---|
| 0 | Starting Face | Presets, whole or regional randomization, locks. Halvren: ancestry-informed starting faces |
| 1 | Head & Proportions | Head scale (Saurin only, §5); facial soft-tissue composition (SOFT + offset) |
| 2 | Cranium & Forehead | Vault, temporal region, forehead. Saurin: frontal/cranial transition and **structural ridges** |
| 3 | Brow & Orbit | Skeletal brow, bony orbit, interorbital spacing. Saurin: orbital-temporal platform and rim |
| 4 | Eyes | 4a External Eye (aperture, lids, angle, canthal relationships); 4b Ocular (iris, permitted ocular tissue, Saurin pupil shape and dilation range) |
| 5 | Cheeks & Midface | Zygoma, cheek soft tissue, midface, maxillary projection. Saurin: **Rostrum & Lateral Face** (rostral projection lives here, not under Nose) |
| 6 | Nose | Nasal pyramid. Saurin: **Nasal Openings** |
| 7 | Mouth | Lips and oral region. Saurin: **Mouth Line** |
| 8 | Jaw & Chin | Mandible and chin. Saurin: **Jaw** (chin Absent) |
| 9 | Ears | Routed to the population's ear-architecture family (§10.2). Saurin: **Auricular Openings** |
| 10 | Hair / Cranial Display | Scalp-hair biology. Saurin: **Cranial Display** (keratin display system) |
| 11 | Facial Hair & Brows | Facial-hair and eyebrow-hair biology. Saurin: Absent |
| 12 | Skin & Surface | Natural facial pigmentation; Saurin facial scale fields. Sub-domain **Acquired** (scars, ear damage, keratin breakage, dental wear or loss), kept distinct from asymmetry |
| 13 | Asymmetry | Per-region left/right offsets; Restore Symmetry; Naturalize Face (provisional, §19) |
| 14 | Age | Apparent Biological Age driver with coupled regional effects |
| 15 | Presentation | Cosmetics, grooming and styling, hairstyle, applied markings, applied display decoration, preview tools (expression, lighting, pupil dilation), creator camera |

**Outside the face tree:**

| Item | Where it goes |
|---|---|
| Halvren genealogy | A Lineage step (§11) |
| Chronological Age | Character data |
| Magical eye effects | Effects systems |
| Expression and lighting | Preview only |
| Ear mobility, low-light physiology, tusk-like canines | OPEN |

## 4. Bound / Bound-locked / Absent

| State | Meaning |
|---|---|
| **Bound** | The population has this anatomy, and the bound controls are authorized |
| **Bound-locked** | The anatomy exists, but no editable control is authorized (for example Saurin orbital spacing, §259; the Saurin nictitating membrane). The anatomy is still validated |
| **Absent** | The population lacks the anatomy. The slot or sub-panel is **hidden, never shown as a dead or empty control** |

## 5. Universal control taxonomy

| Code | Class | Rule |
|---|---|---|
| DIR | Direct anatomical control | Player-edited anatomical dimension named by population canon |
| DER | Derived / coupled | Recomputed from connected anatomy; never hand-stored |
| SOFT | Soft-correlated | Population or body-to-face tendency setting defaults and weights; the player may override within valid anatomy |
| VAL | Validator-only | Never exposed except through its outcome messages |
| LAT | Preset latent variable | Generation only; never a slider |
| PRES | Presentation | Non-biological styling and acquired history |
| DIAG | Diagnostic | Comparison and QA only |

**Canonical class decisions:**

| Decision | Rule |
|---|---|
| **AC-U1: "eye size"** | Bony orbit size = **DIR**; visible eye aperture = **DIR**; eyeball (globe) size = **DER from the orbit**, never an independent slider. Population orbit and aperture constraints are preserved (for example the Pipkin and Cogling anti-enlargement rules; the Saurin orbit coupling) |
| **AD-U4: head scale** | Non-Saurin head scale is **VAL / DIAG only** until measurement work (RM-CF-10, RM-SR-04) shows a direct control is appropriate. No qualitative player range is invented. Saurin keeps its canonical ±8 % head-scale control (SAURIN §258) |
| **AD-U5: dentition** | **No detailed dentition creator controls in v1.** Population-valid dentition is anatomy. Acquired dental wear or loss lives in Acquired history where already supported. Tusk and canine questions stay OPEN |
| **Sex** | Sex-related facial tendency is **SOFT only**, never a control or preset (R-SEX). The default is "no shift"; Saurin has none (§263). **AC-U2:** Cogling's sex-related facial capability is met by the body-level sex-related anatomy selection plus any canonically permitted SOFT facial distribution. No face-level sex slider; magnitude OPEN |
| **Pupil** | Pupil dilation **state** is preview only, never saved |

**Ocular scale clarification (RAC W1e author decision, October 6, 2026; `reviews/chatgpt-rac-w1e-author-decisions-w1f-continuation-order.md` §5):** this replaces the W1d S-D3 reading that "Marchfolk-compatible adult range" meant an absolute 2.2–2.4 cm globe for every population.

> **Species-Scaled Adult Ocular Anatomy Rule:** "Adult humanoid in scale" means mature, non-juvenile ocular/orbital anatomy appropriate to that biological population. It does not require Marchfolk absolute globe diameter. Globe size, socket size and inter-orbital spacing may scale allometrically with species cranial architecture, provided the result preserves adult facial presentation, fits physically, and does not create a "huge-eyed child" phenotype unless independently authored.

It applies with AC-U1 (globe DER from the orbit) and with each population's anti-enlargement rule (PIPKIN Part 3 §4 Forehead, brow and orbital anatomy; COGLING §79). Ocular anatomy implies no visual acuity, magical property or gameplay effect. Landmark globe values in reference meshes are W1 construction geometry, never population canon.

## 6. Dependency relations and resolution order (AD-U2)

**Relations:**

| Relation | Behaviour |
|---|---|
| **FOLLOW** | The child is a function of the parent (for example Saurin orbit → lids, aperture frame, eyeball; the eyeball follows the orbit roster-wide) |
| **OFFSET** | The child keeps an individual offset while a systemic parent moves the base: age effects, soft tissue vs body composition, asymmetry |
| **CLAMP** | The parent sets the child's valid interval. The child is clamped and the player's intent value is retained |
| **NEIGHBOR-ADJUST** | A canon-named consequence moves connected **unlocked** neighbours (for example Saurin rostrum > +10 % → rostral and posterior jaw depth ≥ reference) |
| **ENVELOPE** | A soft relationship shifts the child's distribution; its value moves only if it leaves validity |
| **REDISTRIBUTE** | Only inside an approved relationship tool. None exist in v1 (§7, AD-U3) |
| **INVALID** | The combination cannot be repaired without moving a locked or player-held value |

**Resolution order:**
1. FOLLOW / DER recomputation.
2. CLAMP, retaining intent.
3. NEIGHBOR-ADJUST on unlocked neighbours only.
4. Re-validate the region and its neighbours.

**Outcomes (roster-wide):**
- **PASS**: valid.
- **CONSTRAIN**: valid after an adjustment. It **must be reported** and **biologically deterministic**. It is never silent or arbitrary repair.
- **FAIL**: rejected, with explanation and resolution options.

**Locks are absolute.** A locked child can never force an invalid parent. **No silent reset.**

## 7. Firewall F-1 and Rules G-1…G-5 (AD-U6, AD-U3)

| Rule | Content |
|---|---|
| **F-1** | A quantity becomes DIR only if population canon names it as a variable or control dimension **and** it is not a ratio or index whose only purpose is comparison. Measurability never makes a slider. All Pass 2 craniofacial indices (FPI, MPI, MdPI, CI, CBH, FVB, MVI, FDH, FVI, ORB, IOD, TBP, JDI, HSR), the Facial Diagnostic Domains (FD-*), the Durrim depth domains A–E and all race variation diagnostics are DIAG and/or VAL |
| **G-1** | No hidden global state drives several regions. The only stored systemic facial values are Apparent Biological Age, the facial soft-tissue offset, Saurin head scale and per-region asymmetry offsets |
| **G-2** | Any broad relationship tool would be an *operation* that writes ordinary regional values and leaves no residual state |
| **G-3** | **No broad relationship tools in v1** (AD-U3 option a). No master face-shape, face-width, face-length, face-depth, verticality, elfness, humanity, masculinity, femininity, beauty, age-face, race-face, ancestry-percentage or equivalent whole-face slider. Future coherent tools only after testing and separate author approval. Presets, regional randomization, Quick controls and Detailed controls are the broad editing entry points |
| **G-4** | Halvren phenotype is reached through ordinary controls inside ancestry-derived constraints. Genealogy is never an appearance control (§11) |
| **G-5** | Latent generation variables are never player-facing sliders. Generated and preset faces resolve to ordinary DIR values |

## 8. Quick vs Detailed controls (Advanced Mode)

Advanced Mode uses one tree with two depths:

| Depth | Content |
|---|---|
| **Quick controls** | One curated DIR control per major dimension of each Bound slot. Never a hidden macro |
| **Detailed controls** | The full control set, plus Asymmetry |

Marchfolk's v1.2 "face presets / quick controls / detailed controls" levels map onto Starting Face / Quick / Detailed.

## 9. Simple Mode

- Simple Mode is Race → (Halvren: optional genealogy) → Preset → Confirm.
- It uses the Starting Face slot only. Any whole-face shuffle is the same generator (§13).
- Simple and Advanced Mode share one appearance record. Simple Mode never uses a simplified substitute model.
- Halvren Simple Mode never requires genetics.

## 10. Population binding and exception principles

### 10.1 General principles

1. An exception is solved in the **binding** (label, control set, validators, state), never by hiding anatomy in presets.
2. Population identity carriers stay **population validators**. They are never universal axes. Examples:
   - Durrim craniofacial depth relative to facial height;
   - Grask multiregional verticality and folded late-taper ears;
   - Gorrund Transverse Structural Continuity and deep-bowl ears;
   - Pipkin Integrated Mature Facial Architecture and anti-juvenile limits;
   - Cogling Fine-Scale Planar Integration, camera-not-enlargement and close-view ear folds;
   - elven ECR tendencies;
   - Sagekin statistical identity (population-sample validation only);
   - Skarn robust tendencies (SOFT, never mandatory);
   - Marchfolk as Human Reference Population, not a mandatory face template.
3. Population tendencies are SOFT distributions and envelopes. Control sets stay shared where anatomy is shared.
4. **Coverage-completion rule (AD-U12):**
   - Where canonical anatomy explicitly states that a dimension varies, the matching universal control is bound within that population's validators.
   - Where canon is silent on whether it varies, the control stays **hidden pending author confirmation**.
   - The current per-item disposition is in §19.2.

### 10.2 Ear-architecture families (slot 9)

The families are distinct architectures. **Never a pointiness continuum or interpolation.**

| Family | Populations |
|---|---|
| Human auricle | Marchfolk, Skarn, Sagekin (AC-4). Durrim uses its own broadly humanoid compact range (DURRIM §29–34), routed to the human-auricle variable set; it is not Marchfolk ear anatomy |
| Elven continuous taper | Fenn, Aelari, Vael |
| Mixed coupled human + elven | Halvren |
| Folded late-taper | Grask |
| Deep-bowl broad-rim | Gorrund |
| Compact rounded | Pipkin |
| Fine folded | Cogling |
| Recessed auricular opening | Saurin |

The family-specific parameter sets are those in each race spec, summarized in `reviews/claude-ufca-04-exception-map.md` §3.

### 10.3 Coverage-completion bindings (AD-U12)

| Bound now | Basis |
|---|---|
| Skarn mouth and lips | Normal human-family coverage under the Marchfolk facial-coverage requirement (SKARN v1.2 §2). A coverage clarification, not new Skarn anatomy |
| Skarn and Sagekin ear controls | Human-auricle family under the Marchfolk human-family auricular foundation (Pass 2 AC-4) |
| Marchfolk orbit and midface controls | Required by the Marchfolk v1.5 face validation (§2–6) |
| Durrim regional controls | Where Durrim anatomy explicitly states the dimension varies (Part 3) |
| Grask and Gorrund regional controls | Their canonical required-coverage lists and anatomy |
| Fenn brow structure and brow-to-eye distance | Stated as supported variation (FENN §2–7) |
| Pipkin natural asymmetry | AC-U3 (§10.4) |
| Fenn forehead-to-cranium transition contour | Final closure Q-1. The Fenn "smoother forehead-to-cranium line" relationship (FENN §2–7) inside the Fenn craniofacial envelope, preserving existing broad individual variation where canon supports it. **Not** a generic forehead-height/slope package and no Marchfolk forehead architecture |
| Fenn brow prominence, brow contour/shape, brow vertical position relative to the orbit, medial/lateral brow relationship where needed for coherent regional editing | Final closure Q-4. Anatomical brow/orbital controls (slot 3) inside the Fenn craniofacial envelope, not eyebrow grooming. They preserve the Fenn compact face and approved visible-eye/orbital relationships; no Marchfolk default range; no permanent surprised, delicate, severe, youthful, feminine, masculine or other personality/presentation read |
| Marchfolk forehead height, slope/contour, forehead-to-brow relationship, forehead-to-cranium transition | Final closure Q-3. Regional DIR controls (slot 2), not global face-shape controls; no numeric bounds; inside believable Marchfolk adult human anatomy. Relationship validity keeps brow, orbit, cranium and hairline-region coherence. No preferred or ideal forehead; no sex, personality, attractiveness, culture, age or ancestry stereotype; not a template for other populations |
| Eyebrow-hair biology for Marchfolk, Skarn, Sagekin, Fenn, Aelari, Vael and Halvren | Final closure Q-2. Slot 11: ordinary variation in density/fullness, distribution/coverage, strand/coarseness character where the population's ordinary hair biology supports it, and natural colour relationship to the individual's hair/pigmentation. Grooming, trimming, shaping, cosmetics, dye, styling and deliberate removal stay Presentation. No culture, personality, class, attractiveness or sex encoding; no race-specific eyebrow morphology |

The final-closure rows (Q-1…Q-4) are explicit author authorizations for the named coverage only. They do not change the rule that a shared slot never authorizes anatomy by itself. Durrim, Grask, Gorrund, Pipkin and Cogling keep their already-authored eyebrow biology and routing; Saurin eyebrows stay Absent.

Items held hidden are in §19.2.

### 10.4 Pipkin natural asymmetry (AC-U3)

- Ordinary biological left/right facial variation is available to Pipkin.
- It creates no deformity, pathology, juvenile cue, racial identifier or acquired-injury system.
- Natural asymmetry stays distinct from Acquired history.

## 11. Halvren: genealogy → constraints → phenotype

| Layer | Architecture |
|---|---|
| **A. Genealogy** | An optional Lineage step outside the face tree. Never an appearance slider |
| **B. Ancestry-derived constraints** | Validator envelopes per slot, computed from A and the source specs. With no genealogy set, the general Halvren mixed-population envelope applies. The inheritance clusters (craniofacial; external ear) are LAT, never sliders |
| **C. Phenotype** | Ordinary DIR controls, valid inside B |

**Rules:**
- Editing phenotype never rewrites genealogy.
- No Elf Percentage, lifespan percentage, skull interpolation, pointiness or single "eye" control.
- No 50/50 default.
- Mixed ears are a coupled union of human-foundation and elven variables.
- Whole-face **source-race protection** rejects exact recreation of a source population's complete craniofacial distribution.
- Source-influenced preset codes (I–M) stay internal labels; presets never assert genealogy.

## 12. Saurin homologous routing

**Bindings:**

| Slot | Saurin binding |
|---|---|
| 2 | Cranium with **structural ridges** (skull anatomy; vary in strength, never toggled off) |
| 3 | Orbital-temporal platform; orbit size drives the **FOLLOW** coupling; spacing Bound-locked |
| 4a | Aperture inside the orbit coupling |
| 4b | Vertical-elliptical pupil (species anatomy; shape and dilation range only); nictitating membrane Bound-locked |
| 5 | Rostrum & Lateral Face |
| 6 | Nasal Openings |
| 7 | Mouth Line |
| 8 | Jaw |
| 9 | Auricular Openings |
| 10 | Cranial Display (keratin display; §260 validators) |
| 12 | Field-aware facial scales (no global scale size) |

**AC-U4.** No human forehead or cheek controls exist for Saurin. Homologous controls are:
- frontal/cranium transition and structural ridge;
- temporal/orbital platform;
- rostral and lateral-face relationships;
- mandibular relationships.

**Absent:** chin, lips, zygoma, vertical forehead, nasal pyramid, pinnae, facial hair, eyebrows. **No human facial topology is introduced through slot names.**

**Further rules:**
- The rostral index floor (0.255, provisional, SAURIN §259) remains protective canon.
- Cross-race closure is deferred to RM-CF-01…05. No margin is set. **Update — **RM-CF-05 FINAL CLOSED (author ruling, October 10, 2026; `reviews/chatgpt-rac-w3d-final-ruling-rm-uf-05-order.md` §3-§5; evidence `reviews/claude-rac-w3d-fpi-margin-author-gate.md`):** required Saurin-to-non-Saurin rostral-projection separation **0.05 r3 FPI** (VAL / DIAG cross-architecture safety margin; not a player control, race classifier or frequency statement). Saurin Part 7 floor **0.255 unchanged**; Saurin coupled minimum corner r3 FPI 0.29196; current operational non-Saurin comparison limit **0.24196**, conditional on the current Saurin minimum (not a universal ceiling). A future accepted non-Saurin maximum-valid face that exceeds that limit or reduces the margin below 0.05 is **AUTHOR REVIEW REQUIRED — RM-CF-05 COLLISION** (no automatic invalidation, clipping, floor raise or margin change). FPI is one diagnostic dimension, never a membership test; precision is meaningful to hundredths, not thousandths. (SAURIN_V1 §268).**
- No craniofacial sex shift (§263).

## 13. Presets and randomization

**Presets:**
- A face preset is an ordinary appearance record: valid under the same controls and validators, reproducible in Advanced Mode, round-trip stable.
- **No preset-only anatomy, morphs or geometry.**
- Coverage tags are metadata, never subraces, castes, classes, cultures or genealogy.
- No stereotype bundles.

**Generation pipeline:**
1. Population envelope (Halvren: B).
2. Drivers from weighted SOFT distributions (LAT).
3. Dependents inside coupled bands.
4. Validators: FAIL shapes are rejected and resampled. **Never "roll everything and repair".**
5. Batch diversity check.
6. Biological, Presentation and Acquired-History passes kept separate.

**Selective randomization:** whole face, one slot or slot sets, with locks. Out-of-scope values win over in-scope samples.

**Seeds:** a seed + generator version + distribution version reproduces a generation event. The appearance record resolves to DIR values (saved-appearance schema implementation stays OPEN).

**NPCs** use the same system. Narrative exceptions are flagged as outside canonical species anatomy and excluded from generation baselines.

**Population notes:**
- Saurin follow §264.
- Grask and Gorrund tusk-like canines are excluded until reviewed.
- Grask and Gorrund maxillary/mandibular projection are drawn only from authored central values until the distributions are authored.
- Sagekin identity is reproduced across a batch, not forced on each individual.

## 14. Randomization strength (AD-U7)

These are player-facing:

| Strength | Behaviour |
|---|---|
| **Subtle** | Samples nearer the population's central, high-frequency space |
| **Diverse** | Samples broadly across the normal valid distribution |
| **Extreme** | Deliberately samples toward valid tails and unusual combinations. It stays **biologically valid**: it never unlocks invalid anatomy, caricature, another population's anatomy or hidden developer-only ranges |

The full manually creatable valid range is available regardless of strength.

## 15. Frequency vocabulary (AD-U8)

**Internal (non-player-facing) vocabulary: Very Common / Common / Uncommon / Rare.**

- These describe generation, preset and NPC weighting only, never biological validity.
- A Rare valid phenotype is always manually creatable.
- Interim weights are never population canon.

## 16. N0–N4 neutralization (AD-U10)

| Level | Removes |
|---|---|
| N0 | Nothing (as authored) |
| N1 | Presentation removed |
| N2 | N1 + hair controlled, facial hair removed, eyebrows neutralized where practical; Saurin display minimal (structural ridges remain) |
| N3 | N2 + pigmentation, pattern and acquired features neutralized |
| N4 | N3 + ears hidden or partly obscured per population test |

**Every level uses:** neutral expression, neutral reference lighting and a standardized camera.

**Comparison conditions:**
- **Equal-height:** stature valid for both populations.
- **Matched-scale:** normalized head size; diagnostic only, never resizing characters.
- **Population-sample:** for statistically defined identities.

## 17. Validation tiers and generic pairwise harness (AD-U10)

| Tier | Question |
|---|---|
| **A** | Intra-population validity |
| **B** | Cross-population boundary validity |
| **C** | Relationship validity |
| **D** | Extreme-combination stress |
| **E** | Neutralization |
| **F** | Age and asymmetry (with the R-SEX sex sub-tier) |
| **G** | Preset / randomization diversity and anti-stereotype |

**Rules:**
- Every population's existing facial tests remain **authoritative** and are assigned to tiers in `reviews/claude-ufca-06-validation-framework.md` §2.
- No surface, hair, presentation or observation domain compensates for a failed structural read.
- **Generic pairwise harness:** every population pair is run at N4 matched-scale. It **fills coverage gaps** (pairs without an explicit test; matrix in UFCA-06 §3). It never overwrites an accepted population test.
- Population-sample tests apply where identity is statistical (Sagekin; elf populations at population level).

## 18. Measurement-deferred policy and RM-UF links (AD-U11)

- Where a control or validator needs a number, UFCA defines the semantic variable, its landmarks or index, and its exposure.
- The number is deferred to the Reference-Mesh Measurement Queue (`reviews/claude-pass2-r5-reference-mesh-queue.md`).
- **No numeric facial envelope is set by UFCA.**

**Added to the queue:**

| Item | Measures |
|---|---|
| RM-UF-01 | Visible-aperture distributions relative to orbit, per population |
| RM-UF-02 | Ear-family parameter envelopes. **Depends on authored Grask ear-length and Gorrund projection ranges, which do not yet exist** |
| RM-UF-03 | Saurin orbital spacing tolerance |
| RM-UF-04 | Saurin structural-ridge strength and facial scale-field ranges |
| RM-UF-05 | Batch diversity / anti-convergence threshold |

**Existing links:** RM-CF-01…10, RM-SR-04, RM-SR-05, RM-OT-03, RM-OT-04.

## 19. OPEN and provisional items

### 19.1 Provisional and OPEN carried

| Item | Status |
|---|---|
| **Naturalize Face** | Provisional operation pending testing (AD-U9). The requirement is preserved; its final behaviour is not canonized |
| Low-light / visual adaptation and non-Saurin pupil morphology | OPEN |
| Grask/Gorrund prognathism distributions | OPEN |
| Grask/Gorrund tusk-like canines (separately) | OPEN |
| Dentition counts | OPEN |
| Ear mobility | OPEN |
| Grask/Gorrund ear length and projection ranges | OPEN |
| Sex-related facial magnitude (Durrim, Grask, Gorrund, Pipkin, Cogling) | OPEN |
| Non-Saurin head-to-stature | OPEN |
| Scleral tint (Gorrund OPEN; Grask "comes later") | OPEN |
| Saurin membrane, iris, pupil-dynamics, spacing, ridge, scale-field and display-beyond-family numerics | OPEN |
| Frequencies | OPEN |
| Lifecycle | OPEN |
| Halvren genetic-simulation depth and ancestry UI | OPEN |
| Statistical calibration of soft distributions | OPEN |
| Technical architecture | OPEN |

Full register: `reviews/claude-ufca-07-open-deferred-decision-register.md` §4.

### 19.2 Coverage items held hidden (AD-U12)

| Population | Hidden item | Note |
|---|---|---|
| Fenn | Forehead height and any other forehead dimension beyond the bound forehead-to-cranium transition contour | Hidden unless later canon independently authorizes it (final closure Q-1) |
| Durrim | Sclera / ocular-tissue visibility as a player control | DURRIM §21–28 describes sclera responding to biology, age, vascularity and lighting: a derived appearance, kept as DER in slot 4b, not a player dimension |

## 20. Implementation firewall

UFCA defines **design behaviour only**. It does not decide or imply:
- mesh, topology, head-mesh count, morph targets, blendshapes, bones, rig or deformation method;
- MetaHuman or other asset base;
- LOD;
- UI layout;
- camera implementation;
- animation, speech or lip-sync solutions.

A shared slot does not imply a shared mesh. The Elf Comparative Review guard against a single superficial "Elf Head" (unless prototyping proves it reproduces approved diversity) is carried to implementation.

## 21. Closure

UFCA is **CLOSED / FINAL-AUTHOR ACCEPTED** (October 5, 2026; `reviews/chatgpt-ufca-final-closure-order.md`). Final author decisions Q-1…Q-4 are recorded in §10.3 and §19.2.

Closure freezes the universal facial creator architecture **at the design level**. It does not freeze later legitimate resolution of:
- named OPEN biology (§19.1);
- measurement work (§18);
- implementation choices (§20).

Every named OPEN, DEFERRED and PROVISIONAL item stays as listed. That includes Naturalize Face, which stays provisional.

**Closure is not permission to begin UE5 implementation.**
