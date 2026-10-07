# RAC W1l — Grask Final W1 Author-Acceptance Gate

**Author:** Claude **Date:** October 7, 2026
**Author ruling (October 7, 2026; GitHub Issue #1, final author ruling comment (2026-10-07T14:57Z)):** ACCEPTED as presented; construction point locked at pelvis X 0.925, femur cross-section 1.20, no lumbar narrowing; fuller thighs accepted; residuals non-blocking for W1. Grask W1 is closed. The analysis below is unchanged.
**Order:** GitHub Issue #1, "AUTHOR ORDER — Grask W1l bounded corrective pass", with the author confirmation comment: option (b).
**Basis:** `reviews/claude-rac-w1k-grask-acceptance-gate.md`
**Evidence:** `reviews/rac-w1l-gr-evidence/` (`tables.md` holds every number quoted; `README.md` maps the files)
**Construction record:** `tools/rac/w1/cfg/w1l/GR.json`

Nothing here is accepted. Specs and `STATUS.md` are untouched.

## Recommendation: PASS — ready for author ruling

**The correction (bounded as ordered):**
- Removed the residual lumbar narrowing (spine_01 X 0.96 → none).
- Recovered GR-P2b through the femur instead: proximal-femur robusticity, as femur cross-section ×1.20 (length unchanged).
- Lowered pelvis X from 0.985 to 0.925 to keep GR-P6.
- **Nothing else changed:**
  - clavicle, every generator target, tissue, height macro and stature (217.99 cm);
  - the generator lower-leg target, still at its maximum, as ordered;
  - the comparators.

**Result on the central body** (accepted MF-M-R, SK and Gorrund):
- **Every canonical row passes:** 15 / 15 skeletal, 30 / 30 directional, 12 / 12 skin.
- **The pelvic pass no longer depends on a narrowing operation:** GR-P5 crest ÷ stature is 0.1353 vs MF 0.1500, from torso proportioning.
- **Margins are where W1h had them:**

| Row | W1h | W1l |
|---|---|---|
| GR-P2b bitrochanteric ÷ crest ≥ MF | +0.65 % | **+0.60 %** |
| GR-P6 pelvis ÷ thorax ≈ MF 0.9640 | 0.9691 | **0.9658** |

**Regression checks, all as ordered:**
- Frames, low composition and matched height: nothing new fails.
- Two small changes, both on the diagnostic frame bodies:
  - Broad frame GR-P2b moves from +0.08 % to **−0.08 % (MARGINAL)**;
  - Narrow frame shows 1 trunk vertex inside the arm tube per side.
- Neither frame write is authored Grask anatomy.

**One visual point for the author.** The rig has no separate proximal-femur bone, so the ×1.20 cross-section applies along the **whole femur**. The thighs read visibly fuller, skin and skeleton (`sheets/gr_w1l_hips_before_after.jpg`). The joint relations still hold:
- knee ÷ femur is 0.231 (W1h 0.211);
- Gorrund 0.284, SK 0.292, MF 0.290;
- "relatively lean joints" and Gorrund > Grask are preserved (knee margin vs Gorrund at matched height +11 to +14 %, was +19 to +21 %).

If the thighs read too heavy, the minimum passing alternative is pelvis 0.93 / femur 1.17. It passes every row, but GR-P2b is only +0.20 %.

**No accepted canon was challenged.**

## 1. Correction search (`probe/probe_summary.json`; skeletal CIB rows; lumbar narrowing removed)

| Pelvis X | Femur cross-section | GR-P2b (≥ 1.1992) | GR-P6 (≈ 0.9640 ± 0.010) | Other rows |
|---|---|---|---|---|
| 0.950 | 1.05 | 1.1825 FAIL | 0.9733 PASS | pass |
| 0.950 | 1.10 | 1.1937 MARGINAL | 0.9745 FAIL | pass |
| 0.935 | 1.15 | 1.1990 T-SENSITIVE | 0.9690 PASS | pass |
| 0.930 | 1.17 | 1.2015 PASS (+0.20 %) | 0.9673 PASS | all pass (minimum alternative) |
| **0.925** | **1.20** | **1.2063 PASS (+0.60 %)** | **0.9658 PASS** | **all pass (chosen)** |

W1k probes with pelvis width alone (femur 1.0): no value passes both rows. Those probes are in `reviews/rac-w1k-gr-evidence/probe/`.

**Why 1.20 over 1.17:** it restores the W1h GR-P2b margin. The 1.17 point sits 0.2 % from the threshold, and the Gorrund pass showed how thin margins behave under perturbation.

## 2. Central body, canonical relations (tables §2.2)

| Group | Rows | Result | Thinnest margin |
|---|---|---|---|
| Pelvis GR-P2a / P2b / P4 / P5 / P6 (skeletal) | 6 | PASS | GR-P2b +0.60 %; GR-P4 +1.32 % |
| Girdle GR-G1 (glenohumeral and acromial) | 2 | PASS | +0.49 % |
| Large-race rows with Grask as comparator (RM-LR-02 a / b / d, AD-G6, AD-G7, GO-P2b, GO-P3) | 7 | PASS | — |
| Proportions, hands, thorax, joints, face vs MF / SK / Gorrund | 30 directional | PASS (all beyond 1 %) | lower leg ÷ leg vs MF +1.39 % |
| Skin diagnostics | 12 | PASS | GR-G1 +1.03 % |
| Ears (W1i, head unchanged) | 3 | PASS | — |

## 3. Regression checks

**Matched height** (`matched_height.json`; tables §3). Torso, leg and arm share, span and thorax are identical to W1k, because the correction touches no length. Only knee ÷ femur moved, and it still passes.
- Against Gorrund at 217.0 / 224.1 cm and Broad Skarn at 215.1 / 222.1 cm: 28 / 30 PASS.
- Span vs Broad Skarn stays NOT DEMONSTRATED (+0.76 / +0.88 %). That is non-blocking per the author.

**Frames** (diagnostic writes as in W1k; tables §2.3–2.4; `sheets/gr_w1l_frames_4view.jpg`):

| Body | W1k (as built) | W1l |
|---|---|---|
| Narrow | GR-G1 T-SENSITIVE; span vs MF / SK NOT DEMONSTRATED | same |
| Broad | GR-G1 MARGINAL (skin) | GR-G1 MARGINAL (skin); **GR-P2b skeletal MARGINAL (1.1983 vs 1.1992, −0.08 %)** |

The Broad write widens the pelvis 8 % but the femur only 5 %, so it lowers bitrochanteric ÷ crest. This is the borrowed Broad Skarn write, not Grask anatomy. Under PV-D10, MARGINAL is not a failure.

**Low composition** (tables §2.5, §4–§5). Same as W1k:
- 6 / 7 same-composition skin rows pass.
- GR-P6 skin reads 0.768 vs 0.864, the skin-station effect noted in W1k.
- Whole-trunk readings sit with MF / SK low: hip ÷ thorax 1.007 vs 0.996 / 0.984.

**Composition visuals** are author-accepted. `sheets/gr_w1l_composition_4view.jpg` re-renders them on the corrected skeleton for the record.

**Trunk continuity** (`composition.json`):

| Reading | W1h | W1l | MF / SK |
|---|---|---|---|
| hip ÷ thorax | 0.971 | 0.961 | 0.946 / 0.939 |
| waist rise | 1.087 | 1.077 | 1.083 / 1.085 |

W1l is closer to the references. The minimum-composition skeleton stays inside the accepted MF / SG / SK skeleton range (waist ÷ thorax 0.713, waist rise 1.43).

**Arm clearance, GR-G3** (`arm_clearance.json`):

| Body | Smallest gap | Inside a closed trunk section | Trunk vertices inside the arm tube |
|---|---|---|---|
| Central | 0.72 cm | 0 (unchanged) | 0 |
| Broad | 0.48 cm | 0 | 0 |
| Narrow | 0.68 cm | 0 | **1 per side** (new reading; frames were not tested in W1k) |

The armpit band remains NOT DEMONSTRATED; the method cannot test it.

## 4. Construction values

Recorded in `cfg/w1l/GR.json` as CONSTRAINED construction values, not anatomy:

| Value | Note |
|---|---|
| Pelvis X 0.925 | Hand-set |
| Femur cross-section 1.20 | Hand-set; whole femur |
| Clavicle Y 0.98 | Hand-set |
| Lumbar narrowing | Removed |
| `measure-lowerleg-height-incr` 1.0 | **At the generator maximum** (unchanged, per order) |

There are no solver search bounds.

## 5. Residuals

| Status | Items |
|---|---|
| **FAIL** | None on the central body |
| **MARGINAL** | Broad frame GR-P2b skeletal (−0.08 %) and GR-G1 skin. Low-composition GR-G1 skin |
| **T-SENSITIVE** | Narrow frame GR-G1 skeletal |
| **NOT DEMONSTRATED** | GR-G2 scapula (CONSTRAINED; no scapula bone). Armpit band. Narrow span vs MF / SK. Span vs Broad Skarn (non-blocking, author) |
| **Diagnostic** | Low-composition GR-P6 skin. Narrow frame arm-tube 1 vertex per side. Composition-variant skin rows scored against reference composition (not like for like) |
| **NOT RUN (W2)** | GR-BODY-02 / -03 statures; GR-BODY-10…18 (incl. RM-LR-04, the AD-3 floor); GR-FACE-14 |

## 6. Comparator dependencies and canon

**Comparators:**
- MF-M-R and SK: pelvis, girdle, proportions, face and hands.
- Accepted Gorrund point: large-race rows and matched height.
- Broad Skarn: matched height and the frame write.
- SG: the skeleton range.

None was changed. No other race was touched.

**Canon:** no accepted canon was challenged.
- GR-P2b now holds through the hip apparatus it names.
- GR-P5 holds through torso proportioning, with no narrowing operation.
- GR-P6 holds with no authored departure.

No UE5, topology, rigging, animation, equipment, gameplay or class work was done.

## 7. Recommendation

**PASS.** The corrected central Grask meets every canonical relation tested, with margins equal to the pre-correction body and no narrowing operation. Its Narrow, Broad and low-composition variants and matched-height comparisons show no new failure.

**For the author:**
1. Final W1 acceptance of this Grask (pelvis 0.925, femur 1.20, no lumbar narrowing).
2. Confirm the fuller-thigh read is acceptable; if not, choose the 1.17 alternative.

Aelari is not started.

STOP.

— Claude
