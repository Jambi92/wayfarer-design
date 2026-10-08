# RAC W2H — Short-Race Family Final Closure Report (W2H1)

**Author:** Claude (auditor) · **Date:** October 8, 2026 · **Order:** `reviews/chatgpt-rac-w2h1-durrim-pelvic-closure-order.md`
**Gate closed by this report:** `reviews/claude-rac-w2h-short-race-family-gate.md`
**Evidence:** `reviews/rac-w2h-sr-evidence/closure/`
- `w2h_closure.json` — every number below comes from it.
- `tables_closure.md` — generated.
- `registry_closure.json`, `spec_closure.json`, `construction_closure.json`, `joint_sections_closure.json`, `sheets/`.

The W2H gate-time evidence in `rac-w2h-sr-evidence/` is unchanged.

**Status:** DESIGN ONLY / NO UE5. NON-CANON diagnostics. **The only anatomical change is the author-approved bounded Durrim D1 write: pelvis bone Z ×1.04.** Pipkin, Cogling, Marchfolk, Sagekin, Fenn, Grask and the child proxies are untouched: **0 of the non-Durrim checks changed by any amount**.

## Recommendation

| Item | Recommendation |
|---|---|
| **Durrim W2H** | **ACCEPT.** D1 at ×1.04 turns DU-P4 into a clear PASS (+3.68 % at every t). It moves nothing else beyond 0.75 %, keeps the family coherent, and every Durrim-dependent row still passes. |
| **Pipkin W2H** | **ACCEPT** (accepted in principle; disposition unchanged) |
| **Cogling W2H** | **ACCEPT** (accepted in principle; D2 / D3 recorded) |
| **Short-Race Structural-Mass Axis** | **ACCEPT** (accepted in principle; D4 recorded) |
| **Short-Race Family W2H overall** | **ACCEPT — formal W2H closure recommended.** D1 resolves without a new contradiction. |

---

## 1. D1 construction (order §2, §3)

**The write.** DU-NAT has pelvis bone scale [1, 0.9, 1.0]; D1 makes it **[1, 0.9, 1.04]**. Everything else is unchanged: targets, native short-adult route, frame rule (Broad pelvis X ×1.08), composition states.

**Identical to the probe.** The corrected DU152 reproduces the W2H probe DU152P4 exactly: 0.00000 % maximum ratio difference, same stature.

**Rebuilt bodies.**
- The family: DU122C, DU137C (reference realization), DU152C.
- Narrow / Broad frames at all three statures.
- Six composition states at 137 cm.
- Narrow-low DU (named).
- DU-P4 composition bodies at 152 cm (LOW / MIN / HIBOTH).
- Nine new skeletal grids, plus exact-plane joints for every rebuilt body.

×1.06 was not used.

**Bounded-correction guard (order §2):** 19 / 19 PASS. Every Durrim body was compared with its uncorrected W2H twin on 26 readings, covering everything the order says must not move. All stay within 1 %.

| Reading (DU122 / DU137 / DU152) | Before → after |
|---|---|
| skeletal thoracic depth / stature | 0.1488 / 0.1434 / 0.1387 — unchanged (−0.01 %) |
| skeletal thoracic breadth / stature | unchanged (−0.01 %) |
| skeletal crest breadth / stature | +0.08 % |
| skeletal pelvic vertical / stature | +0.20…0.22 % |
| skeletal pelvic vertical / crest | +0.12…0.14 % |
| skeletal hip-joint spacing / stature | unchanged (−0.01 %) |
| hip-joint height / stature | unchanged (−0.01 %) |
| skeletal crest / thoracic breadth | +0.09 % |
| torso / arm / leg / neck / head / hand share, palm and foot breadth | unchanged (≤ 0.03 %) |
| femoral shaft breadth / femur, S7 breadth | unchanged (−0.01 / −0.02 %) |
| **femoral S7 depth / stature** | **+0.75 %** (the S7 station sits under the pelvis's skin influence; within the guard) |
| exact-plane elbow / wrist / knee / ankle per stature | unchanged (−0.01 %) |

Nothing moved materially beyond the probe behaviour, so no compensation was needed anywhere.

## 2. D1-touched rows, before → after (order §4)

| Body | skeletal AP pelvic depth / stature (t = 0 / 0.5 / 1) | skeletal pelvic AP / thoracic depth | skin AP / stature (diagnostic) |
|---|---|---|---|
| DU122 | 0.1058 / 0.1000 / 0.0943 → **0.1086 / 0.1029 / 0.0971 (+2.82 %)** | 0.7110 → 0.7300 (+2.83 %) | 0.1405 → 0.1477 (+5.1 %) |
| DU137 | 0.1023 / 0.0965 / 0.0907 → **0.1050 / 0.0993 / 0.0935 (+2.84 %)** | 0.7132 → 0.7324 (+2.85 %) | 0.1357 → 0.1388 (+2.4 %) |
| DU152 | 0.0992 / 0.0934 / 0.0876 → **0.1019 / 0.0961 / 0.0903 (+2.85 %)** | 0.7152 → 0.7345 (+2.86 %) | 0.1315 → 0.1292 (**−1.7 %**) |
| Narrow / Broad, 122–152 | same +2.82…+2.86 % at every stature and frame | +2.83…+2.86 % | as the Balanced body |

**Continuity (order §11).** The skeletal gain is uniform: +2.82 % / +2.84 % / +2.85 % across 122 / 137 / 152. There is no single-height spike, no new reversal on any skeletal or skin body reading, and no route seam; the route is native throughout, and DU137R still reproduces the uncorrected DU-NAT exactly.

The Durrim skeletal AP series stays a smooth allometric decline (0.1029 → 0.0993 → 0.0961 at t = 0.5).

The two new continuity flags (ORB height / HH and aperture / orbit height, DU122 → DU152) are ocular-landmark instability, not D1. DU152 before and after have an identical head, yet ORB height / HH reads 0.1048 before and 0.2054 after (§7).

**Skin is a diagnostic only (PV-D16 / PV-D20).** At reference composition the skin pelvic AP reading of DU152 *falls* 1.7 % while the skeleton deepens 2.85 %. This is the same non-monotonic skin landmark response W1t recorded for pelvis Z probes. At low, minimum and high composition the skin reading rises +2.4…+2.6 %.

## 3. DU-P4 final test (order §5)

**DU-P4 — PASS.**

| Item | Before (W2H) | After (W2H1) |
|---|---|---|
| 1. skeletal AP pelvic depth / stature, DU152 vs MF152 | +0.81 % (NOT DEMONSTRATED) | **+3.68 %** |
| 2. by t (DU152 vs MF152) | 0.0992 / 0.0934 / 0.0876 vs 0.0984 / 0.0927 / 0.0869 | **0.1019 / 0.0961 / 0.0903** vs 0.0984 / 0.0927 / 0.0869: **PASS at t = 0, 0.5 and 1** |
| method cross-check (W1t S7-normalized Marchfolk grid) | +0.81 % | +3.68 % (identical Marchfolk values) |
| context vs SG152 | +1.01 % | +3.89 % |
| 3. skeletal pelvic AP / thoracic depth vs MF152 | −11.2 % | **−8.7 %** (step reduced) |
| 4. composition-independent skeletal result | skeleton shared by all composition states → +0.81 % | **+3.68 % in every composition state** (skeletal proxy is composition-free) |
| frame | Narrow / Broad +0.81 % | Narrow / Broad **+3.68 %** (frame is breadth-only; no pelvic-depth change) |
| 5. skin, diagnostic only: reference / LOW / MIN / HIBOTH | −1.65 / +0.80 / +0.38 / +4.18 % | −3.35 / **+3.38 / +3.00** / +6.69 % |

**6. The deep thorax → pelvis transition now reads as coherent.**
- The Durrim lower trunk is now distinctly deeper than both equal-height comparators, in every t-plane, frame and composition: +3.7 % vs Marchfolk and +3.9 % vs Sagekin.
- The thorax is still much deeper (+13.5 %), so pelvic AP / thoracic depth remains below Marchfolk (−8.7 %). As the order states, the rule is a distinctly deep Durrim lower trunk, not thorax–pelvis identity.
- The pelvis is no longer an ordinary-depth human pelvis under a deep thorax.
- The low-muscle, low-fat requirement (DU L52: "must show DU-P4") now holds even on skin: +3.4 % at LOW and +3.0 % at MIN, against +0.8 / +0.4 % before.

**Reasoning.**
- The canon direction (DU-P4, PV-D8) is now demonstrated above the AD-G10 1 % threshold by 3.7×, at the permanent equal-height comparison (DURRIM L156).
- The method cross-check is identical, so no measurement-normalization effect is involved.
- The result does not depend on composition, frame or t.

## 4. Durrim-dependent rerun (order §9, §10)

**667 checks** with a Durrim body on either side were re-evaluated. **No Durrim-dependent result changed class** other than DU-P4 (ND → PASS) and the two ocular continuity flags (§2).

| Group | Result after D1 | Margins that moved (> 0.05 pt) |
|---|---|---|
| **§4A PK122 vs DU122** (18 rows) | **18 / 18 PASS** | crest / thorax −7.33 → −7.24 % |
| **PIP-BODY-14 PKB122 vs DUN122** (16 + 2 report) | **16 / 16 PASS** | crest / thorax −8.96 → −8.87 % |
| **COG-BODY-10A CG107 vs DU122** (15) | **15 / 15 PASS** | none |
| **COG-BODY-10 normalized COG05 vs DUN137** (15) | **15 / 15 PASS** | none |
| body-only collision with a Durrim side (9 pairs) | **9 / 9 PASS** (26–31 of 31 readings separate) | — |
| **152 cm boundary** DU152 vs MF152 and SG152 (44) | **44 / 44 PASS** | crest / stature +5.21 → +5.30 % (MF); pelvic vertical / crest −12.15 → −12.05 %; crest / thorax −2.40 → −2.31 % (DU-P6 still ≤ MF) |
| **Structural-mass rows with Durrim** (femoral shaft, S7 breadth / depth, 4 joints) | all PASS as before | **S7 depth**: PK122 < DU122 −5.01 → −5.77 %; PK107 < DU137 −1.50 → −2.29 %; PK91 < DU122 −6.07 → −6.82 %; COG05 < DUN137 −16.2 → −16.9 % |
| **D4 normalized item** PK122 vs DU152, S7 depth | FAIL (report under D4) | +2.74 → **+1.91 %** (gap narrowed by D1) |
| **Durrim frames** (§10) | all PASS | Narrow keeps crest > MF (+1.13…+9.0 %), DU-P5 vs Narrow Marchfolk (+6.6…+14.9 %); Broad stays thorax-led (crest / thorax ≤ MF, −0.88…−1.81 %); Broad pelvis ×1.08 coherent; frame does not change pelvic depth (+2.82…2.86 % at every frame) |
| **Durrim composition** (§10; 67 rows) | all PASS | the low-muscle / minimum Durrim keeps the corrected skeletal depth (composition-free proxy) and deep thorax, joints, torso > MF in the same state; composition neither creates nor erases DU-P4 (skeletal +3.68 % in every state) |

**Pipkin and Cogling frame and composition dispositions:** unchanged. Their bodies, grids and joint sections are byte-for-byte the W2H ones, and **0 non-Durrim checks changed**.

## 5. Author rulings recorded (D2, D3, D4)

The rulings are recorded in:
- `tools/rac/w1/cfg/w2h/SR-family-boundary.json`;
- the W2H gate author-ruling line;
- D4 as a W2 measurement standard in `decisions/REFERENCE_ANATOMY_V1.md`.

**D2 — Broad Cogling thorax.** "Narrow-to-moderate thorax" is read at Balanced. Broad Cogling reaching about Broad-Marchfolk thoracic breadth (CGB91 −0.7 %, CGB107 +0.2 %) is valid, because the complete package survives:
- crest / thorax < Pipkin;
- fine joints and shafts;
- distal redistribution;
- no Durrim concentration;
- no Pipkin trunk collapse.

The CGB76 thoracic-depth +1.05 % stays a measurement / coupling item; nothing in the rerun touched Cogling.

**D3 — Cogling distal extremes.**

COG-BODY-12 is read at arm-to-wrist:
- COG-BODY-12 arm-to-wrist = **0.2817, identical to the accepted CGJ7**, so the long-finger end adds only finger length and the upper limb is not globally overlong.
- **Precision note for the record:** the ±0.010 "near-human" band was authored on arm-to-fingertip share. At arm-to-wrist, the accepted Cogling reference itself sits 0.013 below Marchfolk (0.2817 vs 0.2947), by its authored short-upper-arm redistribution. So "within the band" at arm-to-wrist means "at the accepted Cogling reference value", which COG-BODY-12 meets exactly.

COG-BODY-13 gets the directional reading:
- forearm / arm +0.9 %, femur / leg −0.7 %, both in direction;
- hand / arm +12 % and finger / hand +4 % carry the identity;
- arm share +0.0101; arm-to-wrist 0.2882, within 0.0065 of Marchfolk.

**D4 — Robusticity.**
- Girth β 1.0 is kept for Pipkin and Cogling.
- Real-height comparisons govern.
- PK122 vs DU152 S7 depth stays a normalized cross-stature report item; D1 narrowed it to +1.91 %.
- **Named dependency carried:** relative robusticity behaviour across each short-race creator envelope is resolved in creator-envelope work, so no interpolation path creates a structural inversion.

## 6. RM-SR dispositions (final)

| Item | Disposition |
|---|---|
| RM-SR-01 Pipkin trunk / pelvis | **RESOLVED** (W2H; unchanged) |
| RM-SR-02 Cogling segment distribution | **RESOLVED** (W2H; D3 recorded) |
| RM-SR-03 structural-mass axis | **RESOLVED**, D4 recorded. After D1 every real-height and matched-composition Durrim row still passes, with S7-depth margins larger. |
| RM-SR-04 adult read | **body RESOLVED; ocular NAMED DEPENDENCY / OUT OF CURRENT SCOPE** (unchanged; no head or eye enlarged) |
| RM-SR-05 Durrim depth | **body proxies REPORTED; facial domains A–E NAMED DEPENDENCY** (unchanged; proxies moved ≤ 0.3 pt) |
| RM-SR-06 Durrim torso / thoracic depth vs MF152 | **RESOLVED** (torso +5.1 %, thoracic depth +11.4 % skin / +13.5 % skeletal; unchanged by D1) |
| **DU-P4** | **PASS** (+3.68 % at every t; §3) |

Adult-read watch items are preserved as ordered:
- Cogling 76 body PASS, head 10.91 cm MARGINAL;
- Pipkin 91 has the highest allometric head share, with no juvenile anatomy;
- ocular instability is a named dependency.

## 7. Complete non-pass accounting (order §14)

Every W2H non-pass row is listed with its final class; nothing was removed.

| # | W2H item | W2H result | Final class | Note |
|---|---|---|---|---|
| 1 | DU-P4 skeletal AP vs MF152 | NOT DEMONSTRATED (+0.81 %) | **RESOLVED BY D1** | PASS +3.68 % |
| 2 | PK122 / PKN122 / PKB122 leg share ≤ MF | MARGINAL (+0.2 %) | **ACCEPTED MARGINAL** | carried PK-P2a "thin" (AD-G10) |
| 3 | COG-BODY-12 arm share ≈ MF | FAIL (+0.0119) | **ACCEPTED BY D3** | arm-to-wrist = CGJ7 (precision note §5) |
| 4 | COG-BODY-13 arm share ≈ MF | FAIL (+0.0101) | **ACCEPTED BY D3** | arm-to-wrist within 0.0065 |
| 5 | COG-BODY-13 forearm / arm > MF | NOT DEMONSTRATED (+0.9 %) | **ACCEPTED BY D3** | direction kept |
| 6 | COG-BODY-13 femur / leg < MF | NOT DEMONSTRATED (−0.7 %) | **ACCEPTED BY D3** | direction kept |
| 7 | axis PK122 < DU152 S7 depth | FAIL (normalized) | **ACCEPTED BY D4 / NORMALIZED DIAGNOSTIC ONLY** | +1.91 % after D1; real height PASS |
| 8 | CGB91 thoracic breadth < Broad MF | NOT DEMONSTRATED | **ACCEPTED BY D2** | |
| 9 | CGB107 thoracic breadth < Broad MF | FAIL (+0.2 %) | **ACCEPTED BY D2** | |
| 10 | CGB76 thoracic depth invariance | FAIL (+1.05 %) | **MEASUREMENT LIMIT** | section coupling; no depth written |
| 11 | CG76 head height 11–13 cm | MARGINAL (10.91 cm) | **ACCEPTED MARGINAL** | builder 11.0 cm vs measured landmark |
| 12 | continuity: ORB / HH, aperture / orbit (PK, CG; and DU after the rebuild) | NON-MONOTONIC | **MEASUREMENT LIMIT → FACIAL NAMED DEPENDENCY** | identical DU152 head reads 0.1048 vs 0.2054 |
| 13 | continuity: MPI / MdPI (DU, PK, CG) | NON-MONOTONIC | **FACIAL NAMED DEPENDENCY** | |
| 14 | continuity: Cogling skin crest / stature, crest / thorax at 107 | NON-MONOTONIC | **MEASUREMENT LIMIT** | skin landmark; skeletal crest series monotonic |
| 15 | continuity: Durrim skeletal bitrochanteric / crest 137→152 (−1.3 %) | NON-MONOTONIC | **VALID REPORT-ONLY** | generator allometry; unchanged by D1 |
| 16 | continuity: Cogling skeletal pelvic AP / thoracic depth 76→91 (−1.0 %) | NON-MONOTONIC | **VALID REPORT-ONLY** | at threshold |
| 17 | G: CG76 / CGN76 / CGB76 head 10.91 cm | NOT ALL PASS | **ACCEPTED MARGINAL** | |
| 18 | G: W1 slab-ratio joint rows CG < PK (CG76 family, CG91 / PK107 composition states, COG13) | NOT ALL PASS | **MEASUREMENT LIMIT** | historical slab per-segment ratios; exact-plane real-height and same-composition rows all PASS |
| 19 | G: Broad / high-fat / high-both Cogling thorax vs MF Balanced (CGB76 / 91 / 107, COG05, CG91-HIFAT, -HIBOTH) | NOT ALL PASS | **ACCEPTED BY D2** (frames) / **NORMALIZED DIAGNOSTIC ONLY** (composition vs reference-composition MF; same-composition rows PASS) | |
| 20 | G: PK122 / PKN122 / PKB122 leg share and hip-joint height | NOT ALL PASS | **ACCEPTED MARGINAL** | |
| 21 | G: DU137-MIN / DU152-MIN elbow / knee per segment vs reference-composition MF; PK107-HIBOTH wrist vs DU; PK107-LOW knee vs CG | NOT ALL PASS | **NORMALIZED DIAGNOSTIC ONLY** | composition-mismatched fixed references; matched-composition rows PASS |
| 22 | G: COG12 / COG13 arm share, forearm, femur | NOT ALL PASS | **ACCEPTED BY D3** | |
| 23 | G: DUN152 hip-joint spacing vs MF173 Balanced (+0.2 %) | NOT ALL PASS | **NORMALIZED DIAGNOSTIC ONLY** | PASS vs Narrow Marchfolk (frame-matched) |
| 24 | G: CG91-MIN face-to-vault (FVI) | NOT ALL PASS | **FACIAL NAMED DEPENDENCY / OUT OF CURRENT SCOPE** | |
| 25 | DU-P4 skin at reference composition (−1.65 % → −3.35 %) | REPORT | **VALID REPORT-ONLY** | skin is diagnostic (PV-D16 / D20); low-composition skin PASS-direction |
| 26 | opposed-composition structural-axis rows (soft tissue can invert skin joints) | REPORT | **VALID REPORT-ONLY** | skeletal axis never inverts |
| 27 | HIBOTH elbow sections (~0.08 / stature, all races and MF) | report note | **MEASUREMENT LIMIT** | arm–torso contact |
| 28 | femoral shaft / S7 breadth under frames | REPORT | **MEASUREMENT LIMIT** | horizontal section follows femoral obliquity; S7 depth unchanged |
| 29 | RM-SR-04 ocular subtests | — | **FACIAL NAMED DEPENDENCY** | |
| 30 | RM-SR-05 domains A–C (and A–E as authored) | — | **FACIAL NAMED DEPENDENCY** | |
| 31 | K child-proxy rows (90), S5 proxies (12), A per-segment joints, Q / R / U / P4 / F / O / D report rows | REPORT | **VALID REPORT-ONLY** | |
| 32 | short-race robusticity across creator envelopes | — | **OUT OF CURRENT SCOPE** (named creator-envelope dependency, D4) | |

**UNRESOLVED: none. NOT RUN: none.**

## 8. Confirmations

- **No other race body changed.** All Pipkin, Cogling, Marchfolk, Sagekin, Fenn, Grask and child-proxy bodies, grids and joint sections are the W2H originals, and 0 non-Durrim checks moved.
- **The D1 correction is Durrim-specific**, applied through the DU-NAT construction only. It is not a generator-wide rule.
- **Durrim envelope and identity preserved:**
  - 122–152 cm envelope; native short-adult route; Broad pelvis ×1.08;
  - Compact Structural Concentration;
  - thorax-led architecture (DU-P6 −2.3 %);
  - substantial joints and long bones; reduced limbs; substantial hands and feet; low centre;
  - adult read (17 / 19 readings separate from the 137 cm child proxy);
  - no uniform scale.
- **On acceptance of this report, DU137C becomes the Durrim reference realization** for W2H closure, with identity DU-NAT plus D1 and every other anatomy unchanged. I have not changed the W1 record `tools/rac/w1/cfg/w1t/DU-NAT.json`; that bookkeeping waits for the author ruling.

**Recommendation: formal W2H closure.**

---

**STOP.** Saurin W2, Wave 3, Halvren genealogy references, creator envelopes, UE5, rigging, animation, equipment and gameplay were not begun. This closure package goes to the author for review.
