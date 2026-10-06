# Reference-Mesh Measurement Queue (Pass 2)

**Author:** Claude (auditor). **Order:** `reviews/chatgpt-pass2-resolution-sequence-order.md` §8.

**Purpose:** list the numeric validators to be **derived** once approved race reference meshes exist. Nothing here supplies a number.

**Model:** Saurin Part 7.
1. Measure the accepted reference.
2. Measure creator extremes.
3. Set diagnostic envelopes from accepted anatomy.
4. Validate creator bounds with PASS / CONSTRAIN / FAIL.

**Common conventions:**
- Normalized height means each body is measured at its own stature, and ratios are taken to standing height.
- Craniofacial indices use `claude-pass2-r3-craniofacial-framework.md`.
- **Prerequisites for every race:** an approved reference mesh (central tendency), plus Narrow / Broad frame-preset meshes and the creator-extreme variants the race's validation set already names.

**Priority:**
- **P1** — needed for Pass-2 author decisions or UFCA floors.
- **P2** — needed for creator-validator implementation.
- **P3** — refinement.

## 1. Large races (Skarn, Grask, Gorrund)

| ID | Pri | Measure | Populations / cases | Feeds |
|---|---|---|---|---|
| RM-LR-01 | P1 | Torso share (suprasternal → hip joint ÷ stature); leg share; arm length and arm span ÷ stature; forearm ÷ arm; lower leg ÷ leg | Skarn, Grask and Gorrund references; Marchfolk reference | Large-race §3 n.d. cells; AD-4 |
| RM-LR-02 | P1 | Thoracic depth ÷ stature; thoracic depth ÷ thoracic breadth; shoulder breadth ÷ stature | Same, plus Narrow and Broad presets | LR-01, LR-04 |
| RM-LR-03 | P1 | Low-breadth Gorrund (GRR-BODY-12) vs Broad Skarn at equal height: depth ratios and joint-to-long-bone ratios | GRR-BODY-12, GRR-BODY-14, Broad Skarn at 208–229 cm | LR-04 |
| RM-LR-04 | P1 | Limb contribution of GR-BODY-10 (short-limbed Grask) vs Gorrund's "slightly more limb-present" family at matched height | GR-BODY-10; GO L232 family | **AD-3** floor |
| RM-LR-05 | P2 | Joint scale (knee, elbow and wrist breadth ÷ adjacent long-bone length) | All three, plus Marchfolk | Large-race joint n.d. |
| RM-LR-06 | P2 | Axial Load-Path Continuity proxies: girdle → thorax → pelvis breadth and depth continuity profile (cross-section series along the trunk) | Gorrund reference and Narrow; Skarn Broad | LR-01–04; GO FC |
| RM-LR-07 | P2 | Hand: finger ÷ palm length; palm breadth and depth ÷ hand length | All three | Finger:palm and palm-structure n.d. |

## 2. Short races (Durrim, Pipkin, Cogling)

| ID | Pri | Measure | Cases | Feeds |
|---|---|---|---|---|
| RM-SR-01 | P2 | Pipkin central-trunk share (thorax + lumbar ÷ stature) and pelvic vertical contribution, vs Marchfolk at normalized height | Pipkin reference, Narrow, Broad | Pipkin primary identifier; SR-COMP-01/02 |
| RM-SR-02 | P2 | Cogling segment ratios: upper arm ÷ arm, forearm ÷ arm, hand ÷ arm, finger ÷ hand; femur ÷ leg; total arm and leg ÷ stature | Cogling reference and extremes | Cogling §8, §38–§42; SR-COMP-01/02 |
| RM-SR-03 | P2 | Long-bone shaft breadth ÷ length; joint breadth ÷ adjacent length | Cogling, Pipkin, Durrim | Structural-mass axis (short-race review §4) |
| RM-SR-04 | P1 | Head ÷ stature; FVI; ORB vs aperture (anti-juvenile) | Pipkin and Cogling references, plus their minimum-height cases; Durrim reference (head-share scope, RAC Phase 2). Cogling's canon head size "roughly 11–13 cm" is **head height** (menton–vertex; W1-A1), tested here | UFCA anti-juvenile constraints; SR-COMP-11 |
| RM-SR-05 | P2 | Durrim depth domains A–E; FDH; CBH | Durrim reference; Marchfolk at 152 cm (corrected comparison point, UCCA T-6) | Durrim C3 (numeric thresholds deferred) |
| RM-SR-06 | P3 | Durrim torso contribution and thoracic depth vs equal-height Marchfolk | 152 cm three-population test | Durrim P2 §54–63 |

## 3. Craniofacial (UFCA floors)

| ID | Pri | Measure | Cases | Feeds |
|---|---|---|---|---|
| RM-CF-01 | P1 | FPI conformance re-measure; also FPI at the minimum-rostrum and cranial-length coupling corners | Saurin frozen reference aff1b52 and creator extremes | Saurin floor **W1 status (October 5, 2026):** SA-M and SA-F **author-accepted as W1 ARMs** (continuation order D-3; bilateral limb readings only from a verified D-2 measurement copy). Diagnostic RM-CF-01 done (`reviews/claude-rac-w1-measurements.md`). **D-1:** the Saurin floor stays in the Part 7 convention; r3 FPI is reported alongside; measured conversion on the accepted anatomy: r3 FPI = Part 7 index + 1.194 cm ÷ HL (`reviews/claude-rac-w1c-saurin-d1-d2.md`); RM-CF-05 compares populations in r3 |
| RM-CF-02 | P1 | FPI, MPI, MdPI distributions including the most prognathic valid face | Marchfolk, including the diagnostic head **MF-FACE-PROJ-MAX** (authored RAC Phase 2) | Saurin floor audit **W1 status:** MF-FACE-PROJ-MAX accepted as the W1 diagnostic Marchfolk maximum reference (1.2 cm, r3 FPI 0.191); central MF-M-R 0.143, MF-F-R 0.169 (diagnostic). |
| RM-CF-03 | P1 | Same | Grask; central projection and max-valid rule **authored RAC Phase 2** (GR L362); max-valid case **GR-FACE-14** | Saurin floor audit |
| RM-CF-04 | P1 | Same | Gorrund; comparator **authored RAC Phase 2** (GO L312 and the note after it); max-valid case **GOR-FACE-05** | Saurin floor audit |
| RM-CF-05 | P1 | *Decision:* the required FPI margin | — | Author |
| RM-CF-06 | P2 | CBH and TBP | Durrim, Gorrund, Marchfolk | Durrim / Gorrund cranial-breadth tendency; Gorrund TSC |
| RM-CF-07 | P2 | FVB with MVI | Grask, Aelari, Marchfolk, Skarn | Grask facial verticality (multiregional) |
| RM-CF-08 | P2 | ORB, IOD and aperture | Fenn, Aelari, Vael (orbit terminology, F-20); Saurin | Elf orbit and presentation distinction |
| RM-CF-09 | P3 | Skarn craniofacial tendencies (skull size, brow, jaw mass, midface) vs Marchfolk | Skarn | Skarn v1.0 §8 promise (S L48) |
| RM-CF-10 | P2 | HSR | Grask, Gorrund, Pipkin, Cogling, **Durrim** (all OPEN; Durrim added RAC Phase 2) | Head-to-height OPEN items; world scale |

## 3A. Universal facial architecture (RM-UF; added October 5, 2026 by UFCA Phase 2, author decision AD-U11)

Semantics only; no numbers are set here. Priority is assigned at measurement planning.

| ID | Pri | Measure | Cases | Feeds |
|---|---|---|---|---|
| RM-UF-01 | — | Visible-aperture distribution relative to bony orbit (ORB vs aperture) | Every population with a bound External Eye slot; first non-elf races (elves and Saurin are covered by RM-CF-08) | UFCA aperture validators; Pipkin/Cogling anti-enlargement (with RM-SR-04) |
| RM-UF-02 | — | Ear-family parameter envelopes (family-specific variables; ear landmarks are not in r3 and must be defined) | All eight ear-architecture families. **Dependency status (RAC Phase 2):** Grask ear length is read relative to head height (longest valid = GR-EAR-02 class); Gorrund projection-from-skull and outward extent are separate variables; ear landmarks are defined in `decisions/REFERENCE_ANATOMY_V1.md` §11. Ranges themselves stay OPEN and are measured here | UFCA slot 9 family validators |
| RM-UF-03 | — | Saurin orbital placement/spacing tolerance (IOD) | Saurin frozen reference and creator extremes | SAURIN §259 lock (tolerance OPEN, §265) |
| RM-UF-04 | — | Saurin structural-ridge strength and facial scale-field ranges | Saurin reference and extremes | SAURIN §36a (numerics OPEN), §262 |
| RM-UF-05 | — | Batch diversity / anti-convergence threshold (distance over DIR vectors; convergence toward named cliché bundles) | Generated batches per population | UFCA validation tier G |

## 3B. Universal body architecture (RM-UB; added October 5, 2026 by UCCA Phase 2, `decisions/UCCA_V1.md` §25; RM-UB-06…08 added by RAC Phase 2)

Semantics only; no numbers are set here. Measurement-deferred values are not creator controls unless canon separately authorizes them.

| ID | Pri | Measure | Cases | Feeds |
|---|---|---|---|---|
| RM-UB-01 | — | Per-race segment-share and within-limb distribution bands (torso/axial, neck, arm, upper-arm/forearm, leg, femur/lower-leg, hand, palm/finger, foot), absolute and proportional | Approved reference meshes per race and frame; extends RM-LR / RM-SR / RM-OT | UCCA Slot 2 CLAMP bands; Pipkin trunk-share split (T-2) |
| RM-UB-02 | — | Per-race allometric response of head, hands, feet, joints, bone breadth and torso breadth/depth to stature | Min / ref / max reference meshes per race | DER absolute dimensions at any stature; no-uniform-scale validator |
| RM-UB-03 | — | Joint-scale and long-bone robusticity envelopes, including race hard minimums | Reference meshes per race and frame | UCCA Slot 3 bounds |
| RM-UB-04 | — | Saurin reachable tail-length cap as a continuous function of resolved frame and composition, through the canon points (~78 % H Balanced reference composition; 80 % H Broad; ~72 % H Narrow high-fat) | Saurin reference variants | Slot 5 CLAMP (SAURIN §256.5) |
| RM-UB-05 | — | Halvren inherited stature-tail limits and frequencies outside the 152–213 cm central envelope. **Authorship done (RAC Phase 2):** H-1…H-6 and the H-5 outer bound (inside 147–229 cm, never automatically a source extreme) in HALVREN; this item measures the actual limits and frequencies; never hard clipping | Halvren genealogy cases with strong short-human, Skarn or Aelari ancestry; HV-49 / HV-50 | UCCA §22 envelope B (AD-C3b) |
| RM-UB-06 | — | Per-race pelvic breadth, depth and vertical contribution, **external skeletal landmarks only** (obstetric firewall) | ARMs per race; frame variants | Pelvic-axial constraints (RAC-03 §2); Pipkin T-2 (with RM-SR-01) |
| RM-UB-07 | — | **Marchfolk baseline set:** segments, torso, neck, pelvis, head share and joints at 147 / 173 / 203 cm, both sex-related configurations | Marchfolk ARMs and stature variants | Every "than Marchfolk" constraint; Saurin lower-trunk floor; **run first in W1** **W1 status (October 5, 2026):** MF-M-R and MF-F-R accepted W1 reference assets (`reviews/chatgpt-rac-w1c-author-acceptance-blocker-resolution-order.md` §2); central diagnostic readings in `reviews/claude-rac-w1c-measurements.md` (diagnostic, not canon); 147/203 cm variants W2. |
| RM-UB-08 | — | Saurin **body** scale-field size and relief ranges (body analogue of RM-UF-04) | Saurin ARM and creator extremes | SAURIN §262 numeric per-field ranges |

**Method:** all items use approved reference meshes as defined in `decisions/REFERENCE_ANATOMY_V1.md` (added RAC Phase 2). Waves W1–W3 are in its §9.

## 4. Other populations

| ID | Pri | Measure | Populations | Feeds |
|---|---|---|---|---|
| RM-OT-01 | P2 | Leg share; forearm, hand and finger ratios; ribcage depth and breadth | Sagekin vs Marchfolk | Sagekin v1.1 §1 tendencies; F-19 hand/ribcage wording **W1 status:** SG accepted W1 reference asset; diagnostic readings and directions in `reviews/claude-rac-w1c-cross-race-audit.md`. |
| RM-OT-02 | P2 | Elf limb share; segment emphasis; thoracic depth; neck relative length; joint ratios | Fenn, Aelari, Vael | Elf review matrix |
| RM-OT-03 | P3 | Halvren source-passing statistics over a generated sample | Halvren vs its six sources | Halvren P2 §32–36 phenotypic boundary protection |
| RM-OT-04 | P2 | Saurin vs Sagekin and Halvren matched-height checks (body and face) | Saurin | F-25 |
| RM-OT-05 | P3 | Stature distributions and world-scale extremes (76–251 cm) | All | Roster world-scale review |

## 5. Rules for deriving the numbers

1. Derive envelopes from **accepted reference anatomy and validated extremes only**. Never back-fit them to a prototype.
2. A validator compares **valid maxima and minima** across populations on the same layer (S or E). Central values alone never establish a boundary.
3. A clamp that a measurement exposes is creator behaviour (CONSTRAIN), not a reason to weaken a population's distribution. This is the same rule as Saurin §263.
4. Record every derived value as a **diagnostic envelope** first. Canonize it only by author acceptance, as Saurin Part 7 did.

— Claude
