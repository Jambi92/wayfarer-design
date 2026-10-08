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
| RM-LR-02 | P1 | Thoracic depth ÷ stature; thoracic depth ÷ thoracic breadth; shoulder breadth ÷ stature. **Pass conditions (RAC W1d, AD-G1/AD-G5…AD-G7/AD-G10/AD-G13, October 5, 2026):** (a) TB ÷ H GO > SK > GR (R2 L54); (b) TD ÷ H GO > SK, GO > GR (R2 L55; AD-R15 does not cover GO–SK depth, AD-G13); (c) **TD ÷ TB GO > SK and GO > GR** (AD-G7); (d) skeletal shoulder breadth ÷ H SK > GR (GR L42), GO > GR (AD-G6); (e) shoulder-joint breadth ÷ TB GR ≤ MF (GR-G1, AD-G1), GO ≤ MF (GO-G1, AD-G5); (g) **report only:** SK vs GR TD; GO vs SK shoulder ÷ H; GR vs MF shoulder ÷ H (AD-G4 undetermined); (h) GR scapular organization (GR-G2, AD-G2) and arm clearance without step (GR-G3, AD-G3): qualitative, orthographic renders. Girdle readings use anatomical acromial / glenohumeral landmarks on skeletal geometry, never bideltoid breadth or the generator shoulder joint (AD-G10). A direction holding by less than the **1 % marginal threshold** is "not demonstrated" (AD-G10). Muscle and MDC never satisfy, rescue or fail a check (AD-G15) | Same, plus Narrow and Broad presets; rebuilt GR and GO (AD-G14) | LR-01, LR-04; GR/GO girdle canon (RAC W1d) |
| RM-LR-03 | P1 | Low-breadth Gorrund (GRR-BODY-12) vs Broad Skarn at equal height: depth ratios and joint-to-long-bone ratios | GRR-BODY-12, GRR-BODY-14, Broad Skarn at 208–229 cm | LR-04 |
| RM-LR-04 | P1 | Limb contribution of GR-BODY-10 (short-limbed Grask) vs Gorrund's "slightly more limb-present" family at matched height | GR-BODY-10; GO L232 family | **AD-3** floor |
| RM-LR-05 | P2 | Joint scale (knee, elbow and wrist breadth ÷ adjacent long-bone length) | All three, plus Marchfolk | Large-race joint n.d. |
| RM-LR-06 | P2 | Axial Load-Path Continuity proxies: girdle → thorax → pelvis breadth and depth continuity profile (cross-section series along the trunk). **Criteria (RAC W1d, AD-G8/AD-G9, October 5, 2026):** stations S1–S7 and ALPC-0…8 as defined in GORRUND (ALPC operational definition after the ALPC transition table); normalized profile compared in direction with the accepted MF-M-R profile shape; ALPC-2 two-sided; ALPC-1b adopted; **ALPC-1c report-only**; ALPC-7 is architectural (does not touch AD-4). **Method (AD-G10):** skeletal-proxy measurement (ribcage, girdle, lumbar column envelope, pelvis, proximal femur), anatomical acromial / glenohumeral landmarks, femoral-head geometry for ALPC-3; ALPC-7 beyond the **1 % marginal threshold**. Pass = all Gorrund bodies pass ALPC-0…6, and the reference and the 208 cm body pass ALPC-7. Muscle and MDC never satisfy, rescue or fail a criterion (AD-G15) | Gorrund reference, GOR-BODY-04, -12, -14, -16, 208 cm Gorrund; Broad Skarn at 208 and 229 cm (accepted SK base, frame write only); MF-M-R as shape comparator | LR-01–04; GO FC; AD-1 |
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
| RM-UB-06 | — | Per-race pelvic breadth, depth and vertical contribution, **external skeletal landmarks only** (obstetric firewall). **RAC W1d additions (October 5, 2026):** (1) **new external skeletal readings (PV-D15):** costal margin (lowest rib) → iliac-crest interval ("waist interval"), lower-trunk skeletal breadth at the costal margin, and thoracic vertical length; (2) **validation layer (PV-D16):** pelvic canon is validated on skeletal / bony-landmark geometry; W1c skin-surface readings stay composition-inclusive diagnostics; (3) **construction (PV-D17):** pelvic robusticity / gracility is a visual orthographic review for W1 (numeric crest-thickness proxy deferred unless later validation requires it); (4) **sacral relationships (PV-D19)** may remain frame-level statements not measured here; (5) Pipkin pelvic vertical contribution ÷ stature is a **≥ MF** direction (PV-D10), magnitude with RM-SR-01 / T-2. Directions per race: each race spec's "Pelvic architecture (RAC W1d)" note | ARMs per race; frame variants | Pelvic-axial constraints (RAC-03 §2); RAC W1d pelvic architecture (race specs); Pipkin T-2 (with RM-SR-01); ALPC-2/-3 (RM-LR-06) |
| RM-UB-07 | — | **Marchfolk baseline set:** segments, torso, neck, pelvis, head share and joints at 147 / 173 / 203 cm, both sex-related configurations | Marchfolk ARMs and stature variants | Every "than Marchfolk" constraint; Saurin lower-trunk floor; **run first in W1** **W1 status (October 5, 2026):** MF-M-R and MF-F-R accepted W1 reference assets (`reviews/chatgpt-rac-w1c-author-acceptance-blocker-resolution-order.md` §2); central diagnostic readings in `reviews/claude-rac-w1c-measurements.md` (diagnostic, not canon); 147/203 cm variants W2. |
| RM-UB-08 | — | Saurin **body** scale-field size and relief ranges (body analogue of RM-UF-04) | Saurin ARM and creator extremes | SAURIN §262 numeric per-field ranges |

**Method:** all items use approved reference meshes as defined in `decisions/REFERENCE_ANATOMY_V1.md` (added RAC Phase 2). Waves W1–W3 are in its §9.

**Build routes (RAC W1d, author-accepted October 5, 2026; `reviews/chatgpt-rac-w1d-author-decisions-continuation-order.md` PV-D21, AD-G14):** pelves are rebuilt by regional non-uniform sculpt/deformation for Durrim, Grask, Gorrund and the elves, and as purpose-built geometry inside the native short-adult base for Pipkin. Grask and Gorrund trunks are rebuilt as a skeletal trunk proxy plus sculpted R-4 envelope. Every builder-chosen magnitude is declared under R-14 and accepted under REFERENCE_ANATOMY §7; affected RM-LR, RM-UB-06 and W1c audit rows are rerun. These are reference-construction routes, not canon or production methods.

**W1e status (October 5, 2026; `reviews/claude-rac-w1e-author-acceptance-gate.md`):** RM-CF-08 FN ORB — O-1 landmark orbital-margin rings built for MF-M-R / MF-F-R / FN, FN increment δ proposed; stays NOT DEMONSTRATED until the author confirms δ (O-D4). RM-SR-04 — PK/CG adult globes do not fit the authored sockets (S-D3 contradiction flagged; PK/CG eye/orbit readings blocked). RM-UF-02 — ear-family v2 reference centres built and attached for FN, AE, VA, HV, GR, GO, PK, CG; envelopes stay OPEN. RM-UB-06 / RM-LR-02 / RM-LR-06 — re-run on skin diagnostics only (PV-D16); skeletal validation and the AD-G14 GR/GO skeletal-trunk proxy are not built.

**W1f status (October 6, 2026; `reviews/claude-rac-w1f-author-acceptance-gate.md`):** RM-CF-08 FN ORB — the O-1 ring at δ = 0.03 (accepted O-D2a) fits and is the bony-orbit surrogate; the old E-proxy is historical, non-vetoing evidence. RM-SR-04 — PK/CG species-scaled adult ocular geometry built under the Species-Scaled Adult Ocular Anatomy Rule (UFCA). RM-UB-06 / RM-LR-02 / RM-LR-06 — run on the W1f skeletal proxy (PV-D16, AD-G10) for every affected race, with the AD-G14 Gorrund and Grask skeleton + envelope rebuilds, GOR-BODY-02/04/12/14/16 and equal-height Broad Skarn (208, 229 cm); ALPC-6 (GOR-BODY-16 skin profile) does not hold — see the gate.

**W1g status (October 6, 2026; `reviews/claude-rac-w1g-author-acceptance-gate.md`):** RM-UB-06 / RM-LR-02 / RM-LR-06 re-run with composition-infimum bony stations (M-1(a)); after the GO re-solve, GR pelvis and AE / VA / FN bone-length corrections the skeletal table has 79 PASS, 1 REPORT, 3 placeholders run separately; ALPC-7 passes at 10 Gorrund / Broad Skarn height pairs (208–229 cm); ALPC-6 on a GOR-BODY-16 valid by construction (skin 11 / 12); GOR-BODY-12 and GOR-BODY-03 (251 cm) have FAIL rows (see gate); RM-SR-04 G-S1 globes PK 1.716 / CG 1.222 cm returned for acceptance. Nothing accepted.

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

**W1h status (October 6, 2026; `reviews/claude-rac-w1h-author-acceptance-gate.md`):** CIB kept as validation upper-bound proxy with refined stations (fixed reference levels, plane sections). GO re-solved for lower-trunk continuity and thoracic breadth > SK (+1.19 %): skeletal table 79 PASS, 1 REPORT, 3 placeholders run separately; GOR-BODY-03 (251 cm) 15 / 15; frames GOR-BODY-04 / -12 / -14 all PASS; residuals: ribcage row at 208 / 215 / 222 cm, ALPC-7 at 5 cross-height pairs (NOT DEMONSTRATED), ALPC-6 skin 7 / 12 (diagnostic), armpit band NOT DEMONSTRATED. GR pelvis re-tuned to 0.985 for the new method. AE budget: compatible, margins limited by head / neck-base share (author decision). Nothing accepted.

**W1i status (October 6, 2026; `reviews/claude-rac-w1i-author-acceptance-gate.md`):** Gorrund re-solved with the full stature series (208.3 true minimum, 210.8, 217.0, 224.1, 230.9, 253.0 cm) and every ALPC-7 cross-height pair in the loop, plus reference-derived continuity guards: every Gorrund skeletal row passes at every stature, frame and height pair; thoracic breadth > SK +1.41 %; ALPC-6 skin official reading 7 / 12, 10 PASS / 1 MARGINAL / 1 FAIL on plane sections (vertex-slab artifact documented); 23 of 32 ±2 % perturbations keep every relation (1 FAIL; corrected in W1j to 2 — thoracic breadth below SK counts as FAIL). Femur robusticity 1.386 (bound raised to 1.40) awaits author ruling. Nothing accepted.

**W1j status (October 7, 2026; `reviews/claude-rac-w1j-author-acceptance-gate.md`):** CONSTRAIN, trade presented. The W1i point is retained (geometry identical); it is the most stable configuration built (22 / 32 ±2 % steps keep every relation on the W1j series with the true 208 cm body, 2 FAIL). Candidates at femur 1.306 / 1.294 pass every canonical relation but are less stable (17 and 16 / 32). Femur floor in this construction lies between about 1.27 and 1.29. The upper-thorax group (rib-cage breadth, upper-thorax length, kb60, kb80) cannot be made ±2 % robust within the current search bounds (first-order tolerance about ±0.2 %; about ±1.2 % with bounds widened by 0.5, not built). Competing relations: TB > SK, ALPC-1b at 208 cm, AD-G7, ALPC-7 vs Broad Skarn, ALPC-4. Low composition is measured against same-composition MF / SK. Nothing accepted; awaiting author ruling.


## RAC W1 measurement-status update — Gorrund (October 7, 2026)

The retained Gorrund W1i/W1j reference is **AUTHOR ACCEPTED as the W1 ARM** (`reviews/chatgpt-rac-w1j-gorrund-final-author-acceptance.md`). Measurements and residuals produced by W1i/W1j may now be treated as evidence from an accepted reference body. Construction/search values and perturbation bounds remain diagnostic/reproducibility data unless a separate canonical rule explicitly adopts them. Creator-validator envelopes remain later measurement/parameterization work.

**W1k status — Grask (October 7, 2026; `reviews/claude-rac-w1k-grask-acceptance-gate.md`):** CONSTRAIN. Central GR (W1h geometry, 218.0 cm) passes 15 / 15 skeletal, 30 / 30 directional and 12 / 12 skin rows against MF, SK and the accepted Gorrund point, and separates from Gorrund (217 cm) and Broad Skarn (215 / 222 cm) on proportions at overlapping stature (span vs Broad Skarn NOT DEMONSTRATED). Record error found: the W1h build kept the base lumbar narrowing (spine_01 X 0.96) that the W1g/W1h records call removed; without it GR-P2b and GR-P6 cannot both pass by pelvis width alone. Author decision requested. GR-G2 CONSTRAINED, armpit band NOT DEMONSTRATED; RM-LR-04 and GR-BODY-02/03/10-18 NOT RUN (W2). Nothing accepted.

**W1l status — Grask (October 7, 2026; `reviews/claude-rac-w1l-grask-acceptance-gate.md`; order GitHub Issue #1, option b):** PASS, awaiting author ruling. Lumbar narrowing removed; GR-P2b recovered through proximal-femur robusticity (femur cross-section 1.20, whole femur) with pelvis X 0.925. Central body passes 15 / 15 skeletal, 30 / 30 directional and 12 / 12 skin rows (GR-P2b +0.60 %, GR-P6 0.9658). Regressions: Broad frame GR-P2b MARGINAL (−0.08 %), Narrow frame arm-tube 1 vertex per side (diagnostic frames). Span vs Broad Skarn NOT DEMONSTRATED (non-blocking). Nothing accepted.

**Grask W1 closure (October 7, 2026; GitHub Issue #1 final author ruling):** GR is an **AUTHOR-ACCEPTED W1 ARM** — the W1l corrected central body (pelvis X 0.925, femur cross-section 1.20, no lumbar narrowing; `tools/rac/w1/cfg/w1l/GR.json`; gate `reviews/claude-rac-w1l-grask-acceptance-gate.md`). Construction values are reference-construction values, not species constants. Disclosed residuals (Broad frame GR-P2b MARGINAL, Narrow arm-tube, GR-G2 CONSTRAINED, armpit band and span vs Broad Skarn NOT DEMONSTRATED, W2 items NOT RUN) are non-blocking for W1. Next W1 body: Aelari.

**W1m status — Aelari (October 7, 2026; `reviews/claude-rac-w1m-aelari-acceptance-gate.md`; order GitHub Issue #1 final ruling):** CONSTRAIN. As-built AE (W1g geometry, record verified) passes all existing rows against the accepted comparators, but fails canon even leg elongation (AE L58 / L167) measured as lower leg / thigh ~ MF (1.002 vs 1.067; new row, arm-row convention). Candidate AEL1 (thigh 0.9875 / calf 1.0523; leg length and all vertical shares unchanged) passes every row, both diagnostic frames and the same-composition low check. Author points: torso share below MF (budget-bound), leg-evenness row and tolerance, Sagekin limb overlap, high muscle + fat visual. Nothing accepted.

**Aelari W1 closure (October 7, 2026; GitHub Issue #1 final Aelari ruling):** AE is an **AUTHOR-ACCEPTED W1 ARM** — candidate AEL1 (thigh 0.9875 / calf 1.0523, all other W1g scales; `tools/rac/w1/cfg/w1m/AE.json`; gate `reviews/claude-rac-w1m-aelari-acceptance-gate.md`). Leg-evenness row accepted for W1. Thin vertical-budget margins (1.1–1.3 %) recorded. **Dependency:** AE rows against Fenn and Vael (torso > FN, neck > FN, AE-P6, PV-D5 / D6, VA rows) to be re-checked once those bodies are accepted. Next W1 body: Vael.

**W1n status — Vael (October 7, 2026; `reviews/claude-rac-w1n-vael-acceptance-gate.md`; order GitHub Issue #1 Aelari ruling):** CONSTRAIN. As-built VA (W1g geometry, record verified) passes all previously run rows but fails four canon-derived rows: limb balance (lower leg / thigh, forearm / upper arm ~ MF ±0.010) and wrist / ankle gracility vs MF. Candidate VAL4 (limb segments rebalanced, wrist / ankle / knee lightened; lengths, shares, trunk, head unchanged; accepted Aelari budget intact) passes them; arm < AE NOT DEMONSTRATED under BM-3. Frame finding: borrowed Broad Skarn write conflicts with VAEL L114; breadth-only Narrow passes, breadth-only Broad fails E-A2 (hip apparatus must follow crest). Author points: VAL4, added rows, frame convention, separation from MF / SG (face and ears carry it). Fenn dependency recorded. Nothing accepted.

**W1o status — Vael Broad frame (October 7, 2026; `reviews/claude-rac-w1o-vael-acceptance-gate.md`; order `reviews/chatgpt-vael-w1n-author-ruling-w1o-order.md`):** PASS, awaiting final Vael acceptance. VAL4 central accepted (W1n ruling). Broad breadth-only frame with pelvis (hip-joint spacing) x1.12 instead of x1.08 restores E-A2 (1.2010 vs 1.1992, +0.15 %) with all other rows unchanged; compact continuity within the Vael frame range (hip / thorax 0.978 vs Narrow 0.976, Fenn 0.985). Skin AP-depth diagnostic and Fenn dependency carried. Nothing else accepted.

**Vael W1 closure (October 7, 2026; GitHub Issue #1 final Vael ruling; `reviews/chatgpt-vael-final-acceptance-fenn-w1-order.md`):** VA is an **AUTHOR-ACCEPTED W1 ARM** — VAL4 (`tools/rac/w1/cfg/w1n/VA.json`; gates `reviews/claude-rac-w1n-vael-acceptance-gate.md`, `reviews/claude-rac-w1o-vael-acceptance-gate.md`). Frame principle breadth-only; Broad diagnostic frame pelvis x1.12 (hip-joint spacing, not joint size). Residuals carried: skin AP-depth diagnostic, arm vs Aelari BM-3, thin margins, Fenn-dependent rows (re-check in the Fenn pass). Next W1 body: Fenn.

**W1p status — Fenn (October 7, 2026; `reviews/claude-rac-w1p-fenn-acceptance-gate.md`; order `reviews/chatgpt-vael-final-acceptance-fenn-w1-order.md`):** CONSTRAIN. As-built FN (W1g geometry, record verified) passes all rows against the accepted elves and the newly run canon rows except the E-A1 gracility order at elbow and knee vs accepted Aelari. Candidate FNL4 (arm-bone cross-section 0.95, leg-bone 0.96, knee target 0.6; lengths and shares unchanged) passes everything; elf-family chain intact; all Aelari / Vael rows that depended on Fenn pass. Broad frame with the Vael principle (pelvis x1.12) passes E-A2. Author points: FNL4, neck reading (neck / torso vs neck / stature), frame breadth rows. Nothing accepted.

**Fenn W1 closure (October 7, 2026; GitHub Issue #1 final Fenn ruling; `reviews/chatgpt-fenn-final-acceptance-pipkin-w1-order.md`):** FN is an **AUTHOR-ACCEPTED W1 ARM** — FNL4 (`tools/rac/w1/cfg/w1p/FN.json`; gate `reviews/claude-rac-w1p-fenn-acceptance-gate.md`). Elf neck rule read as neck / torso. Frame breadth rows vs unmatched central MF are non-vetoing. **Elf dependency closure:** all Aelari and Vael rows that depended on Fenn were re-run against FNL4 and pass. Next W1 body: Pipkin.

**W1q status — Pipkin (October 7, 2026; `reviews/claude-rac-w1q-pipkin-acceptance-gate.md`; order `reviews/chatgpt-fenn-final-acceptance-pipkin-w1-order.md`):** PASS, awaiting author ruling. PK-NAT as built (record verified) passes every measurable row: 7 / 7 skeletal incl. the five pelvis-led rows, 9 / 9 directional, 7 / 7 skin, 16 / 16 added (Durrim / Cogling rows as unaccepted dependencies). No correction proposed. PK-P2b convergent femora NOT DEMONSTRATED (R-6 stance places hip above ankle by definition). Child proxy (generator, 107 cm) separates on head share, waist, pelvis, face, extremities. Breadth-only frames and Broad PK vs Narrow DU hold. Nothing accepted.

**Pipkin W1 closure (October 7, 2026; GitHub Issue #1 final Pipkin ruling; `reviews/chatgpt-pipkin-final-acceptance-cogling-w1-order.md`):** PK is an **AUTHOR-ACCEPTED W1 ARM** — PK-NAT as built, 107 cm (`tools/rac/w1/cfg/w1q/PK-NAT.json`; gate `reviews/claude-rac-w1q-pipkin-acceptance-gate.md`). PK-P2b convergent femora NOT DEMONSTRATED (R-6 stance; re-test with a natural stance). PK-P2a thin margin into W2. Durrim and Cogling rows provisional. Next W1 body: Cogling.

**W1r Cogling gate returned (October 7, 2026).** Per `reviews/chatgpt-pipkin-final-acceptance-cogling-w1-order.md` (Issue #1 2026-10-07T18:10Z). As-built CG-NAT carries the identity but fails fine construction (elbow ÷ stature vs MF and PK; ankle ND; femoral-shaft depth vs MF). Bounded CG-only candidate CGJ7 (ankle-circ-decr 1.0; upper arm / forearm / thigh radial ×0.95) passes every scored row. Author rulings requested: CGJ7 vs as built; height-normalized scaled-slab joint reading; breadth-only frames. Gate: `reviews/claude-rac-w1r-cogling-acceptance-gate.md`. Halvren not started.

**Cogling W1 closed (October 7, 2026).** Author ruling (Issue #1 2026-10-07T18:57Z; `reviews/chatgpt-cogling-final-acceptance-halvren-w1-order.md`): COGLING W1 ACCEPTED — CGJ7 central at ~91 cm; stature-scaled slab adopted for height-normalized joint comparisons across strongly different statures; breadth-only frames with Broad pelvis x1.12. Durrim-dependent rows provisional. Record: `tools/rac/w1/cfg/w1r/CG-NAT.json`. Next: Halvren W1, then Durrim.

**W1s Halvren gate returned (October 7, 2026).** Per `reviews/chatgpt-cogling-final-acceptance-halvren-w1-order.md` (Issue #1 2026-10-07T18:57Z). HV as built (177.7 cm) measured directly against MF-M-R, SK, SG, FNL4, AEL1, VAL4: inside the source span, no domain-wide duplication, 13/13 human/elven nearest split on body readings, not an arithmetic midpoint, pelvis not a linear morph, mixed ear architecture. No correction proposed; orbit-breadth row unstable under eye-target probes (HVC1 offered). Hidden-ear craniofacial NOT DEMONSTRATED (accepted elven heads except Aelari not separated from MF). Diagnostic expression panel HVH3 / HVE3. Gate: `reviews/claude-rac-w1s-halvren-acceptance-gate.md`. Durrim not started.

**Halvren W1 closed (October 7, 2026).** Author ruling (Issue #1 2026-10-07T19:28Z; `reviews/chatgpt-halvren-final-acceptance-durrim-w1-order.md`): HALVREN W1 ACCEPTED — diagnostic anchor HVC1 at ~178 cm (HV with eye-scale target removed). Orbit-breadth no verdict; hidden-ear craniofacial NOT DEMONSTRATED (source-method limit); pelvic inheritance OPEN. Record: `tools/rac/w1/cfg/w1s/HV.json`. Next: Durrim W1 (last W1 body).

**W1t Durrim gate returned (October 7, 2026).** Per `reviews/chatgpt-halvren-final-acceptance-durrim-w1-order.md` (Issue #1 2026-10-07T19:28Z). DU-NAT as built passes every authored Durrim relation (skin, directional, skeletal DU-P2b…P6); structural-mass axis CG < PK < DU closes at all four joints and femoral S7. Short-race cases (Broad PK vs Narrow DU, COG-BODY-10/10A, SR-COMP-03 at 122 cm) pass except breadth convergence. 152 cm boundary: DU-P4 skeletal NOT DEMONSTRATED (+0.8 %). Durrim-specific Broad frame pelvis ×1.08. No correction proposed. Gate: `reviews/claude-rac-w1t-durrim-acceptance-gate.md`. Last W1 body; W2 gated.

**Durrim W1 closed; RAC Wave 1 CLOSED (October 7, 2026).** Author ruling (Issue #1 2026-10-07T21:18Z; `reviews/chatgpt-durrim-final-acceptance-rac-w2-kickoff-order.md`): DURRIM W1 ACCEPTED — DU-NAT as built; Durrim Broad pelvis x1.08; DU-P4 at 152 cm OPEN/CARRIED to W2. All W1 bodies accepted; Wave 2 UNGATED. Next: W2A Marchfolk boundary foundation (RM-UB-07, 147 / 203 cm, both configurations), then STOP.

**W2A Marchfolk boundary gate returned (October 7, 2026).** Per `reviews/chatgpt-durrim-final-acceptance-rac-w2-kickoff-order.md` §W2A. RM-UB-07 at 147 / 203 cm, both configurations: no uniform scaling, adult at 147, not Skarn-like or elf-like at 203 (matched-stature allometry-adjusted), continuity with reported route kinks. Route rule proposed: native regional route at 147 cm; generator macro + knee restored to the generator allometric slope at 203 cm (knee-circ-incr 0.6 / 0.3). Frames and composition at 173 cm pass. All values NON-CANON. Gate: `reviews/claude-rac-w2a-marchfolk-boundary-gate.md`. Next W2 block not started.

**W2A partially accepted (October 7, 2026).** Author ruling (Issue #1 2026-10-07T21:46Z; `reviews/chatgpt-rac-w2a1-marchfolk-frame-closure-order.md`): 147 / 203 cm boundary bodies, both configurations, accepted (knee 0.6 / 0.3); routes are construction methods only; composition accepted; envelopes NON-CANON. Frames reopened as W2A1 (multi-domain Marchfolk frame at 173 cm, both configurations).

**W2A1 Marchfolk frame gate returned (October 7, 2026).** Per `reviews/chatgpt-rac-w2a1-marchfolk-frame-closure-order.md`. Multi-domain skeletal frames at 173 cm, both configurations: breadth ±5 % (clavicle, spine, pelvis with hip joints), ribcage / pelvic depth ±2.5 %, long bones +3.5 / −1.5 %, joint circumference +0.15 / −0.10. Lengths, head, composition unchanged; Broad below Skarn; Narrow above Fenn / Aelari (Narrow joint reduction capped by the Aelari knee bound). Gate: `reviews/claude-rac-w2a1-marchfolk-frame-gate.md`. Next W2 block not started.

**W2A Marchfolk FULLY ACCEPTED (October 7, 2026).** Ruling (Issue #1 2026-10-07T22:24Z; `reviews/chatgpt-rac-w2a-final-acceptance-w2b-skarn-order.md`): stature foundation, composition and W2A1 multi-domain frames accepted; envelopes NON-CANON. Next: W2B Skarn boundary foundation (183 / 208 / 229 cm, both configurations; MF overlap at 190 / 203; frames; composition; SK-02/03/04/05/07/08).

**W2B Skarn boundary gate returned (October 7, 2026).** Per `reviews/chatgpt-rac-w2a-final-acceptance-w2b-skarn-order.md`. 183 / 208 / 229 cm, both configurations (config 2 229 cm by macro 1.0 + native extension); MF overlap at 190 / 203 (MF 190 config 1 knee rule 0.8) and canonical pair all PASS; frames = W2A1 human magnitudes on the SK ARM, Narrow stays Skarn, Broad below GO-H208 on authored carriers, ALPC-7 21 / 21; composition 8 / 8; SK-02/03/04/05/07/08. 368 scored PASS, 0 FAIL, 58 report, 6 continuity reversals (route characteristics). No canon challenge. Gate: `reviews/claude-rac-w2b-skarn-boundary-gate.md`. Grask / Gorrund W2 not started.

**W2B Skarn CONSTRAIN (October 7, 2026).** Ruling `reviews/chatgpt-rac-w2b-skarn-constrain-w2b1-order.md`: 183 / 208 cm bodies, MF overlap 190 / 203, canonical pair, frames and Narrow / Broad boundaries, ALPC-7, composition, SK-02/03/04/05/07/08 provisionally accepted; envelopes NON-CANON. W2B1 ordered: bounded 229 cm continuity cleanup (configuration 2 S7 depth; configuration 1 knee).

**W2B1 Skarn 229 cm gate returned (October 7, 2026).** Per `reviews/chatgpt-rac-w2b-skarn-constrain-w2b1-order.md`. Configuration 1 · 229 cm knee corrected (knee incr 1.0 → decr 0.5 at 229 cm only; +14.9 % → +0.9 % vs slope; nothing else moves). Configuration 2 · 229 cm body unchanged: the S7-depth drop is a ±0.8 cm vertex-slab sampling artifact (skin continuous; ±1.5 cm slab or exact section restores continuity; thicker-thigh target lowers the slab reading); plane-section S7 offered as a CANDIDATE measurement ruling. No W2B row regressed (370 PASS, 57 REPORT, 5 configuration-2 S7 reversals). Gate: `reviews/claude-rac-w2b1-skarn-229-correction-gate.md`.

**W2B1 ACCEPTED; S7 method normalized (October 7, 2026).** Ruling `reviews/chatgpt-rac-w2b1-skarn-author-ruling-s7-normalization-order.md`: 229 cm configuration 1 knee correction (knee decr 0.5) accepted; 229 cm configuration 2 accepted unchanged; S7 read on exact plane sections from now on. Next: bounded S7 normalization of every S7-dependent row in W1, W2A, W2B / W2B1, then the Skarn W2 final gate.

**S7 normalization / Skarn W2 final gate returned (October 7, 2026).** Per `reviews/chatgpt-rac-w2b1-skarn-author-ruling-s7-normalization-order.md`. S7 now read on exact plane sections (`tools/rac/w1/s7_station.py`). 73 skeletal-proxy bodies re-read without rebuilding (vertex control reproduces every recorded S7); 20 S7-dependent evidence files across W1i, W1r, W1s, W1t, W2A, W2A1, W2B / W2B1 re-run (baseline reproduction exact): 1,662 rows, 211 value changes, 15 status changes, all improvements (W1i Cogling shaft rows, CGJ7 Broad S7 breadth, 5 Skarn 229 cm continuity rows); no regression, no contradiction. W2B1 Skarn 375 PASS / 57 REPORT / 0 reversals. Proposed: Skarn W2 FULLY ACCEPTED. Gate: `reviews/claude-rac-s7-normalization-skarn-w2-final-gate.md`.

**Skarn W2 FULLY ACCEPTED; S7 normalization accepted (October 7, 2026).** Ruling `reviews/chatgpt-rac-s7-skarn-final-acceptance-w2c-grask-order.md`: exact-plane S7 is the measurement standard; Skarn 183 / 208 / 229 cm (both configurations, W2B1 knee correction), overlap, frames, boundaries, composition and named extremes locked as W2 diagnostic evidence (record `tools/rac/w1/cfg/w2b/SK-boundary.json`). Next: W2C Grask boundary foundation.
