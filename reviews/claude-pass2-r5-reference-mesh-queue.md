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
| RM-LR-04 | P1 | Limb contribution of GR-BODY-10 (short-limbed Grask) vs Gorrund's "slightly more limb-present" family at matched height | GR-BODY-10; GO L230 family | **AD-3** floor |
| RM-LR-05 | P2 | Joint scale (knee, elbow and wrist breadth ÷ adjacent long-bone length) | All three, plus Marchfolk | Large-race joint n.d. |
| RM-LR-06 | P2 | Axial Load-Path Continuity proxies: girdle → thorax → pelvis breadth and depth continuity profile (cross-section series along the trunk) | Gorrund reference and Narrow; Skarn Broad | LR-01–04; GO FC |
| RM-LR-07 | P2 | Hand: finger ÷ palm length; palm breadth and depth ÷ hand length | All three | Finger:palm and palm-structure n.d. |

## 2. Short races (Durrim, Pipkin, Cogling)

| ID | Pri | Measure | Cases | Feeds |
|---|---|---|---|---|
| RM-SR-01 | P2 | Pipkin central-trunk share (thorax + lumbar ÷ stature) and pelvic vertical contribution, vs Marchfolk at normalized height | Pipkin reference, Narrow, Broad | Pipkin primary identifier; SR-COMP-01/02 |
| RM-SR-02 | P2 | Cogling segment ratios: upper arm ÷ arm, forearm ÷ arm, hand ÷ arm, finger ÷ hand; femur ÷ leg; total arm and leg ÷ stature | Cogling reference and extremes | Cogling §8, §38–§42; SR-COMP-01/02 |
| RM-SR-03 | P2 | Long-bone shaft breadth ÷ length; joint breadth ÷ adjacent length | Cogling, Pipkin, Durrim | Structural-mass axis (short-race review §4) |
| RM-SR-04 | P1 | Head ÷ stature; FVI; ORB vs aperture (anti-juvenile) | Pipkin and Cogling references, plus their minimum-height cases | UFCA anti-juvenile constraints; SR-COMP-11 |
| RM-SR-05 | P2 | Durrim depth domains A–E; FDH; CBH | Durrim reference; Marchfolk at ~150–152 cm | Durrim C3 (numeric thresholds deferred) |
| RM-SR-06 | P3 | Durrim torso contribution and thoracic depth vs equal-height Marchfolk | 152 cm three-population test | Durrim P2 §54–63 |

## 3. Craniofacial (UFCA floors)

| ID | Pri | Measure | Cases | Feeds |
|---|---|---|---|---|
| RM-CF-01 | P1 | FPI conformance re-measure; also FPI at the minimum-rostrum and cranial-length coupling corners | Saurin frozen reference aff1b52 and creator extremes | Saurin floor |
| RM-CF-02 | P1 | FPI, MPI, MdPI distributions including the most prognathic valid face | Marchfolk | Saurin floor audit |
| RM-CF-03 | P1 | Same | Grask, **after** its projection distribution is authored (GR L360) | Saurin floor audit |
| RM-CF-04 | P1 | Same | Gorrund, **after** its prognathism distribution is authored (GO L308) | Saurin floor audit |
| RM-CF-05 | P1 | *Decision:* the required FPI margin | — | Author |
| RM-CF-06 | P2 | CBH and TBP | Durrim, Gorrund, Marchfolk | Durrim / Gorrund cranial-breadth tendency; Gorrund TSC |
| RM-CF-07 | P2 | FVB with MVI | Grask, Aelari, Marchfolk, Skarn | Grask facial verticality (multiregional) |
| RM-CF-08 | P2 | ORB, IOD and aperture | Fenn, Aelari, Vael (orbit terminology, F-20); Saurin | Elf orbit and presentation distinction |
| RM-CF-09 | P3 | Skarn craniofacial tendencies (skull size, brow, jaw mass, midface) vs Marchfolk | Skarn | Skarn v1.0 §8 promise (S L48) |
| RM-CF-10 | P2 | HSR | Grask, Gorrund, Pipkin, Cogling (all OPEN) | Head-to-height OPEN items; world scale |

## 3A. Universal facial architecture (RM-UF; added October 5, 2026 by UFCA Phase 2, author decision AD-U11)

Semantics only; no numbers are set here. Priority is assigned at measurement planning.

| ID | Pri | Measure | Cases | Feeds |
|---|---|---|---|---|
| RM-UF-01 | — | Visible-aperture distribution relative to bony orbit (ORB vs aperture) | Every population with a bound External Eye slot; first non-elf races (elves and Saurin are covered by RM-CF-08) | UFCA aperture validators; Pipkin/Cogling anti-enlargement (with RM-SR-04) |
| RM-UF-02 | — | Ear-family parameter envelopes (family-specific variables; ear landmarks are not in r3 and must be defined) | All eight ear-architecture families. **Dependency:** Grask ear-length ranges and Gorrund projection ranges are OPEN and must be authored first; no numbers are derived before then | UFCA slot 9 family validators |
| RM-UF-03 | — | Saurin orbital placement/spacing tolerance (IOD) | Saurin frozen reference and creator extremes | SAURIN §259 lock (tolerance OPEN, §265) |
| RM-UF-04 | — | Saurin structural-ridge strength and facial scale-field ranges | Saurin reference and extremes | SAURIN §36a (numerics OPEN), §262 |
| RM-UF-05 | — | Batch diversity / anti-convergence threshold (distance over DIR vectors; convergence toward named cliché bundles) | Generated batches per population | UFCA validation tier G |

## 4. Other populations

| ID | Pri | Measure | Populations | Feeds |
|---|---|---|---|---|
| RM-OT-01 | P2 | Leg share; forearm, hand and finger ratios; ribcage depth and breadth | Sagekin vs Marchfolk | Sagekin v1.1 §1 tendencies; F-19 hand/ribcage wording |
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
