# RAC W1 Continuation — Author-Acceptance Gate

**Author:** Claude (builder/coordinator and auditor) **Date:** October 5, 2026
**Order:** `reviews/chatgpt-rac-wave1-continuation-asset-build-order.md` §10

**Review:** an independent audit agent checked this package against its evidence and canon. Its findings were verified, then fixed. Changes:
- FAL redefined per r3 L40;
- six missed canon directions added, and AE, FN, DU and VA rebuilt;
- Grask and other citations corrected;
- the eye fit checked on every candidate;
- the invariance and ordering deviations disclosed.

## Recommendation: **EXACT REMAINING ASSET / CANON BLOCKERS** (not "W1 candidates complete")

All 14 candidates were built, inspected and measured, and their evidence sheets were produced.
- **Five** are technically ready for author acceptance (§2): MF-M-R, MF-F-R, MF-FACE-PROJ-MAX, SK and SG.
- **Two** fail R-2 because the tool chain cannot reach their statures natively: PK and CG.
- **Seven** are CONSTRAIN: FN, AE, VA, HV, DU, GR and GO. Canon-required race anatomy (ear families, non-human pelves, ALPC) is either not producible by the generator or not authored in canon.

**Canon itself:** no internal contradiction was found, and no canon or envelope was changed.

**Candidates vs canon:** 132 of 133 tested canon directions hold. **FN's "slightly larger bony orbit" is not demonstrated**: the ORB breadth proxy reads lower than MF. The tested set is a minimum, not every direction in the specs.

## 1. Candidate table

| Candidate | Technical verdict | Target / measured stature (cm) | Native? | Directional checks | Geometry SHA-256 (prefix) | Evidence sheet |
|---|---|---|---|---|---|---|
| SA-M (Saurin male centre) | PASS — **author-accepted W1 ARM** | 188 / 187.88 | frozen closure | W1 pass 1 | a925e067… | `reviews/rac-w1-evidence/saurin_inspect.jpg` |
| SA-F (Saurin female centre) | PASS — **author-accepted W1 ARM** | 188 / 187.88 | derived (§263) | W1 pass 1 | derived | — |
| MF-M-R | PASS | 173 / 173.14 | yes | 0 / 0 | 5fce9e19098a0b87… | `reviews/rac-w1c-evidence/MF-M-R_evidence.jpg` |
| MF-F-R | PASS | 173 / 172.99 | yes | 0 / 0 | c448c4bd8a70c929… | `reviews/rac-w1c-evidence/MF-F-R_evidence.jpg` |
| MF-FACE-PROJ-MAX | PASS | 173 / 173.14 | yes | 2 / 2 | c6b428dc0571374e… | `reviews/rac-w1c-evidence/MF-FACE-PROJ-MAX_evidence.jpg` |
| SK | PASS | 208 / 208.01 | yes | 9 / 9 | a49d5572839a5ab1… | `reviews/rac-w1c-evidence/SK_evidence.jpg` |
| SG | PASS | 178 / 177.99 | yes | 7 / 7 | 47b62d2eb2a6a14d… | `reviews/rac-w1c-evidence/SG_evidence.jpg` |
| FN | CONSTRAIN | 181 / 181.14 | yes | 14 / 15 | 97f4246b43397209… | `reviews/rac-w1c-evidence/FN_evidence.jpg` |
| AE | CONSTRAIN | 190 / 190.01 | yes | 12 / 12 | efa08d2c6b43adcb… | `reviews/rac-w1c-evidence/AE_evidence.jpg` |
| VA | CONSTRAIN | 178 / 178.00 | yes | 13 / 13 | 33412e7ad2443b85… | `reviews/rac-w1c-evidence/VA_evidence.jpg` |
| HV | CONSTRAIN | 178 / 177.73 | yes | 8 / 8 | dbef6095f945ced1… | `reviews/rac-w1c-evidence/HV_evidence.jpg` |
| DU | CONSTRAIN | 137 / 136.99 | yes | 13 / 13 | 6570ff4d7ed2c0e3… | `reviews/rac-w1c-evidence/DU_evidence.jpg` |
| GR | CONSTRAIN | 218 / 217.99 | yes | 21 / 21 | 552128b370ef5b7f… | `reviews/rac-w1c-evidence/GR_evidence.jpg` |
| GO | CONSTRAIN | 229 / 228.99 | yes | 14 / 14 | 457830b21fea78bf… | `reviews/rac-w1c-evidence/GO_evidence.jpg` |
| PK | FAIL (R-2) | 107 / 107.00 | no — proxy ×0.7675 | 7 / 7 | 0a1132354cc1440d… | `reviews/rac-w1c-evidence/PK_evidence.jpg` |
| CG | FAIL (R-2) | 91 / 91.00 | no — proxy ×0.6373 | 12 / 12 | 3eab32485dea1c21… | `reviews/rac-w1c-evidence/CG_evidence.jpg` |

Records: `reviews/rac-w1c-arm/claude-rac-w1c-arm-<ID>.md`. Saurin: `reviews/rac-w1-arm/` and `reviews/claude-rac-w1c-saurin-d1-d2.md`.

## 2. Ready for author acceptance (technical PASS)

| Candidate | What the author is accepting |
|---|---|
| **MF-M-R** | Generator default adult male at 35 y, 173.14 cm native. Generator default proportions and ethnic mix as builder-chosen placeholders (never Marchfolk bounds, D-4d); muscle/weight 0.5; 8° R-6 abduction; 2.4 cm globes |
| **MF-F-R** | As MF-M-R, configuration 2, native 172.99 cm (height macro 0.606, **no scaling**; replaces the ×1.0877 candidate). The DER globe (2.44 cm) touches the skin at one vertex (0.044 cm); a fitting-size globe is an author option |
| **MF-FACE-PROJ-MAX** | **The Marchfolk maximum itself:** 1.2 cm bimaxillary lower-face advance → FPI 0.191 (MF central 0.143). Identity-relevant: it sets the human side of the Saurin boundary (RM-CF-05) |
| **SK**, **SG** | Their generator-target sets (identity-relevant proportions). All tested directions hold; SK elbow and knee are marginal |

## 3. Builder-chosen, identity-relevant values needing author acceptance

All are listed per candidate in the ARM records (R-14). The ones that most determine identity:
1. **Each race's generator-target set.** These are the numbers that make every race differ from MF-M-R. They were chosen to instantiate canon directions and **corrected until the tested directions held** (seven rounds). Their magnitudes are not canon, and some are large: CG upper arm ÷ arm 0.286 vs MF 0.353, and CG femur ÷ leg 0.342 vs 0.484.
2. **The MF-FACE-PROJ-MAX** advance (1.2 cm).
3. **The globe-diameter rule** (DER from the generator socket): 2.76–3.03 cm in SK, GR and GO. That is generator allometry; canon has no large-race orbit size.
4. **The generator joint system** as joint centres. The rig shoulder joint sits low (MF-M-R upper arm 24.9 < forearm 26.1 cm joint-to-joint), so absolute segment values follow the generator's convention.
5. **R-6 arm abduction** of 8°.
6. **Measurement rules:**
   - **D-W1c-1:** anatomy is read on the generator-authored rest geometry. This **deviates from D-4b** ("rebuild directly in R-6"), which this generator cannot do. The R-6 skinning moves the axilla (thorax breadth −0.84 to −3.22 cm) and the hip (pelvic depth up to +1.22 cm, bitrochanteric up to −1.40 cm).
   - The E-proxy landmarks: FAL per r3 L40, Pr at 75 %, Po\* at the concha, and low-confidence orbit proxies.
   - The ±0.010 "≈" tolerance and the 1 % marginal threshold.
7. **The HV no-lineage mix** as a whole. **Order deviation:** HV was built before its elven sources passed (§7 item 14). Its source-span checks must be re-run when FN, AE and VA are accepted.

## 4. Diagnostic results (`reviews/claude-rac-w1c-measurements.md`)

Measured:
- **RM-UB-07** (MF central, both configurations);
- **RM-OT-01** (SG vs MF);
- RM-LR-01 / 02 / 05 / 07 (MF, SK, GR, GO);
- **RM-CF-02**: MF central 0.143, configuration 2 0.169, maximum 0.191;
- RM-CF-03 / 04 central: GR 0.145, GO 0.149;
- RM-CF-06 (CBH): DU 1.116, GO 1.119, MF 1.077;
- RM-CF-07;
- RM-CF-10 / SR-04 (HSR);
- **RM-UF-01** (MF aperture 2.08 × 0.72 cm);
- RM-UB-01 for SK, SG, FN, AE, VA, HV and DU.

Not demonstrated:
- **RM-CF-08 (FN)**;
- **RM-LR-06 (GO ALPC)**.

**Saurin:**
- RM-CF-01 is done (W1 pass 1).
- The D-1 conversion is recorded: r3 FPI = Part 7 index + 1.194 cm ÷ HL.
- The limb items are blocked (D-2).

## 5. Cross-race results (`reviews/claude-rac-w1c-cross-race-audit.md`)

- **132 / 133 directional checks pass.** The one failure is FN ORB breadth.
- **10 passes are marginal** (under 1 %), so not demonstrated: SK elbow and knee; FN forearm share; AE leg share; VA vs AE leg share; DU arm share; GO > SK thoracic breadth; CG < PK wrist and knee; HV forearm span.
- These passes are **builder-forced (§7 circularity)**.
- The MF maximum face sits below the Saurin coupled corner in r3 (0.191 < 0.292). The required margin is RM-CF-05 (author).

## 6. Rebuilds and failures during the pass

- **MF-M / MF-F (Iteration 3):** replaced by MF-M-R and MF-F-R (age, stance, eyes; MF-F native).
- **MF-FACE-PROJ-MAX attempts 1–2:** generator mouth/chin targets rejected (snout-like lip mass, not a valid human face). Rebuilt with a bimaxillary displacement.
- **Race correction rounds 1–6:**
  - SK: torso, depth, clavicles, joints, arm length;
  - GR: lower leg, forearm, midface;
  - GO: arms, thorax, joints, palm;
  - FN: lower leg, aperture;
  - AE: arms, face;
  - PK: trunk;
  - CG: limb totals, redistribution, joints, head height;
  - HV: forearm.
- **Round 7, after the audit:**
  - AE: hands, feet, arm evenness;
  - FN: feet, orbit;
  - DU: arm contribution;
  - VA: leg share vs AE.
- **Construction trap:** arm "scale-horiz" targets lengthen A-posed arms.
- **Measurement fix:** FAL redefined per r3 L40. The earlier window-edge definition was withdrawn, and every FPI dropped by about 0.01.
- **Saurin D-2 copy, attempt 1:** failed invariance; not used.

## 7. Remaining blockers (exact)

| # | Blocker | Kind | Affects | What unblocks it |
|---|---|---|---|---|
| B-1 | The generator's adult range starts at about 137 cm (configuration 1) and 123 cm (configuration 2). **PK 107 cm and CG 91 cm cannot be built natively** | Tool chain (R-2) | PK, CG | A different short-adult base (sculpted or modelled), or an author ruling on per-stature targets + a units scale |
| B-2 | **Non-human ear families:** elven continuous taper (FN, AE, VA); mixed (HV); folded late-taper (GR); deep-bowl broad-rim (GO). The generator has only the human auricle, and its "pointed" morphs are the pointiness continuum that canon forbids | Asset (sculpt) | FN, AE, VA, HV, GR, GO head tests | Sculpted ears per family (builder-chosen shape, author acceptance) or supplied assets |
| B-3 | **Race pelvis morphology is OPEN in canon.** DU: "never a simply widened human pelvis". GO: "never a uniformly enlarged human pelvis". FN, AE, VA, GR and PK: distinct pelves. The candidates carry the generator's human pelvis with breadth targets | **Canon authorship** | DU, GO, FN, AE, VA, GR, PK pelvic items (RM-UB-06) | Pelvic morphology authored, then built |
| B-4 | **Gorrund ALPC / structural mass** not demonstrated; Grask and Gorrund shoulder girdles not authored | Asset + canon | GO (RM-LR-06), GR, GO | Sculpted trunk/girdle per canon, plus girdle authorship |
| B-5 | **FN bony orbit** ("slightly larger") not demonstrated; the soft-tissue ORB proxy disagrees | Asset / measurement | FN (RM-CF-08) | An author-accepted orbit landmark method (or skull geometry), then rebuild FN if it still fails |
| B-6 | **No Saurin joint-centre set,** so there is no verified D-2 copy | Asset / builder (identity-relevant) | SA RM-UB-01 limbs, RM-UB-04 | Author-accepted SA joint centres, or the closure rig |
| B-7 | **Author acceptance** of every builder-chosen value (§3), of D-W1c-1, and of the HV ordering deviation | Author | All | Author acceptance pass |

**Exact readiness:**
- B-7 alone lets MF-M-R, MF-F-R, MF-FACE-PROJ-MAX, SK and SG be formally accepted now.
- B-7 also lets the body-proportion items of AE, VA, DU, GR and GO be accepted as **partial** ARMs. That excludes pelvis, ears and ALPC.
- FN needs B-5 as well. HV needs its sources accepted.
- PK and CG need B-1. Saurin limb items need B-6.

STOP.

— Claude
