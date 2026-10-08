# RAC W2F — Elf Family Final Closure Report

**Author:** Claude (auditor) · **Date:** October 8, 2026
**Order:** `reviews/chatgpt-rac-w2f-elf-family-closure-order.md` (author rulings R1–R3)
**Basis:** `reviews/claude-rac-w2f-elf-family-gate.md`
**Evidence:** `reviews/rac-w2f-elf-evidence/closure/` (`w2f_closure.json`, `tables_closure.md`, `r2_cutoff_sensitivity.json`). The gate-time evidence at the top level is unchanged.
**Status:** DESIGN ONLY / NO UE5. No elf, Marchfolk, Sagekin or Skarn body or canon was changed. The reference bodies FNL4, AEL1 and VAL4 are unchanged. Face, ear and orbit envelopes are untouched. No uniform scaling.

## Recommendations

| | Recommendation |
|---|---|
| **Fenn** | **ACCEPT** |
| **Aelari** | **ACCEPT** |
| **Vael** | **ACCEPT** |
| **Elf Family W2F** | **ACCEPT — recommend formal W2F closure** |

Every prior non-pass is resolved or classified under R1–R3 or the existing rules (§6). One small item surfaced in the re-run, Aelari neck at 168–173 cm on the new native route. It is classified under R1's general matched-height clause and listed separately for the author to see (§5).

---

## 1. R1 incorporated: the matched-height interpretation

**The rule is recorded where later work will find it:** `decisions/REFERENCE_ANATOMY_V1.md`, under "Measurement standards adopted during RAC Wave 2". E-A2, VA-P2a and the Aelari longer-leg relation are population / reference-state directional relations. They are not mandatory ≥ 1 % separations at every matched stature. Later audits, creator-envelope work and UE5 must not re-read them that way.

**How the evaluator now applies it** (`w2f_eval.py`; the raw class is kept in `raw_result`):
- **Rows covered:** E-A2 / Aelari-leg / VA-P2a rows that miss by under 1 % in, or effectively equal to, the intended direction.
- **New class:** **PASS (R1 reference-state)**.
- **Count:** 37 rows:
  - Aelari: 8;
  - Vael: 21;
  - Fenn: none needed.

**Sagekin scalar overlaps** in the S rows (elf vs Sagekin at matched height) and the M rows (vs Sagekin at matched composition) are classed **OVERLAP (R1 complete anatomy)**. That is 63 rows:
- Fenn 11 (forearm only);
- Aelari 41 (arm, hand, leg, wrist, knee);
- Vael 11 (leg).

The complete-anatomy evidence that carries each population against Sagekin is unchanged from the gate (§4 there). For Aelari at 190 cm:
- head +4.5 %;
- neck +3.9 %;
- ribcage depth −3.4 % (skin) / −4.2 % (skeletal);
- crest −7.0 %;
- pelvic vertical / thoracic vertical +7.1 %;
- lower leg / leg +4.0 %;
- ankle per bone −4.8 %.

**No leg was forced upward and no Vael was shortened.** The gate's leg probes stay unapplied diagnostics.

**The reference bodies still pass every accepted W1 row:**

| Reference | Directional | Skeletal |
|---|---|---|
| FN181 | 24 / 24 | 10 / 10 |
| AE190 | 20 / 20 | 11 / 11 |
| VA178 | 14 / 14 | 8 / 8 |

## 2. R2 incorporated: native route below re-solved macro ~0.40

**Rebuilt on the native short-adult route,** from each population's accepted base macro with targets and bone scales unchanged (`w2f_drivers/leg_probe.py route`, `r2_rebuild.py`):
- FN163 (macro 0.306);
- VA163 (0.357);
- AE168 (0.290);
- AE173 (0.359).

**Dependants rebuilt:** the six Aelari 173 composition states, the Aelari 168 Narrow / Broad frames, the CIB grids and the exact-plane joints.

**Matched Marchfolk 163:** the native MF163N, a comparator only. Marchfolk 168 (macro 0.419) stays on the macro route under the rule.

**The macro builds are kept with suffix M as "before".**

### Before (macro) / after (native)

| Body | femur / leg | leg / stature | torso / stature | neck / stature | head / stature | knee / femur | wrist / forearm |
|---|---|---|---|---|---|---|---|
| FN163 before | 0.4349 | 0.5406 | 0.2735 | 0.0549 | 0.1323 | 0.2821 | 0.1811 |
| **FN163 after** | **0.4740** | **0.5487** | **0.2704** | **0.0532** | **0.1306** | **0.2467** | **0.1790** |
| VA163 before | 0.4539 | 0.5287 | 0.2828 | 0.0558 | 0.1339 | 0.2968 | 0.2045 |
| **VA163 after** | **0.4837** | **0.5366** | **0.2792** | **0.0543** | **0.1325** | **0.2737** | **0.2021** |
| AE168 before | 0.4419 | 0.5317 | 0.2775 | 0.0577 | 0.1384 | 0.2917 | 0.2035 |
| **AE168 after** | **0.4837** | **0.5422** | **0.2734** | **0.0551** | **0.1361** | **0.2542** | **0.2003** |
| AE173 before | 0.4541 | 0.5350 | 0.2766 | 0.0571 | 0.1365 | 0.2725 | 0.1999 |
| **AE173 after** | **0.4837** | **0.5427** | **0.2736** | **0.0552** | **0.1350** | **0.2516** | **0.1986** |
| Marchfolk 163 before | 0.4593 | 0.5251 | 0.2856 | 0.0557 | 0.1337 | 0.2984 | 0.2096 |
| **Marchfolk 163 after** | **0.4837** | **0.5311** | **0.2830** | **0.0546** | **0.1323** | **0.2763** | **0.2050** |

**The generator's short-femur distortion is gone.** Femur / leg returns to each population's reference value (+6.5 % to +9.5 %). The leg, knee and torso readings follow.

**Population directions vs Marchfolk, before and after:**

| Body | Before (macro) | After (native) |
|---|---|---|
| Fenn 163 | 13 / 13 | 13 / 13 |
| Vael 163 | leg +0.7 % ND | leg +1.0 % PASS; 3 / 3 |
| Aelari 168 | knee per bone FAIL, wrist ND, leg ND | knee −10.1 %, wrist −2.5 %, leg +2.6 % PASS |
| Aelari 173 | knee FAIL, wrist ND, leg ND | knee −7.0 %, wrist −1.5 %, leg +2.0 % PASS |

The route rebuild does not touch any reference body, and no racial target changed.

## 3. The 53 continuity reversals

**53 → 38 after R2.** All 38 surviving reversals of 1 % or more are explained individually in `closure/tables_closure.md` (code C). They fall into five groups:

| Group | Count | Explanation |
|---|---|---|
| Native → macro junction | 34 | Every one sits at the first step from a native-route body to a macro-route body: FN163 → FN173 (13), AE173 → AE178 (16), VA163 → VA173 (5). See below. |
| Fenn ankle breadth / stature, FN173 → FN178 | 1 | −1.1 % on an almost flat reading (total range under 2 %); a section-level wobble on a macro step, not a trend. VALID REPORT-ONLY. |
| Fenn wrist per bone, 157 → 163 → 173 | 1 | Falls −1.0 / −2.1 % on the native side, then flat (+0.1 to +0.3 %) on the macro side. The native route carries the generator's adult girth allometry (girth ∝ length^0.654), so short native bodies have relatively thicker wrists, while the macro side is flat. This is legitimate allometry on the native side; it is flagged only because the majority of steps rise. |
| Aelari skeletal girdle breadth / stature | 1 | Flagged at 181 → 190 → 203 (−1.5 / −1.8 %). The real trend above the junction is a decline, which is ordinary allometry (Fenn −1.6 / −0.9 %, Marchfolk similar). The flag comes from the step-count rule: one +1.4 % junction step plus small +0.1 % steps outnumber the declines. Legitimate allometry. |
| Vael skeletal girdle breadth / stature | 1 | −0.8 % then +1.0 % around VA178, then −2.0 % at 190 → 203. The accepted VAL4 reference (W1 held-macro build with its W1 bone-scale overrides) sits about 1 % low on girdle breadth relative to its re-solved neighbours; the top step is ordinary allometry. Reference bodies are not altered (order §11). VALID REPORT-ONLY. |

**Why the native → macro junction produces reversals.** The native route (the accepted W2A construction) holds the base-macro segment proportions and applies one length factor. It carries no segment-length allometry by design. The macro route does carry it, and just above macro 0.40 it still shows a fading part of the short-stature femur and shoulder behaviour; for example, FN173 at macro 0.444 has femur / leg 3 % below the reference. Where the two routes meet, readings that carry segment allometry step.

**Sensitivity test** (`r2_cutoff_sensitivity.json`; diagnostic only, the ruled cutoff is not changed): with FN173, AE178 and VA173 also on the native route, the reversals become 19. The Fenn junction reversals disappear, the Aelari ones move up to the new AE178 → AE181 junction, and two Vael ones appear higher up. The kink moves with the junction, so it belongs to the route, not to the anatomy.

**Classification: GENERATOR LIMIT** (route junction). It is not smooth allometry, and it is not a biological discontinuity. There is no residual ≥ 1 % reversal that cannot be explained.

## 4. FN-09 at ×0.75 (R3)

FN-09 is now the ×0.75 build (Fenn's own arm and leg length targets at 0.75 strength, 181 cm). The rejected ×0.50 build is kept as FN09x50 for the record.

**Against Marchfolk 181:** every Fenn direction holds.

| Reading | FN-09 vs Marchfolk 181 |
|---|---|
| torso | −3.3 % |
| ribcage depth | −4.6 % |
| ribcage breadth | −2.9 % |
| arm | +4.9 % |
| leg | +2.2 % |
| lower leg / leg | +2.7 % |
| hand | +7.9 % |
| foot | +4.6 % |
| wrist per bone | −11.9 % |
| knee per bone | −9.3 % |
| skeletal ribcage depth | −5.7 % |
| bitrochanteric / crest | +1.4 % |
| forearm / arm | +0.98 % (NOT DEMONSTRATED; direction present) |

The ×0.50 build failed this forearm row. ×0.75 keeps it, just under the 1 % threshold, so it is the right stress extreme.

**Against Sagekin 181:**
- Fenn stays distinct on 13 of 15 readings.
- Forearm / arm is −0.6 %. That is the known Fenn ≈ Sagekin forearm overlap (Fenn reference vs Sagekin is +0.4 %) → ACCEPTED COMPLETE-ANATOMY OVERLAP.
- Leg is +0.9 % (direction present).

**Movement vs the Fenn reference** is −0.4 % arm and −0.5 % leg (NOT DEMONSTRATED). This is a generator target response: halving or quartering length targets moves shares little once stature is re-solved.

**FN-09 remains recognizably Fenn.**

## 5. Surfaced in the re-run: Aelari neck at the native short end

| Comparison | Aelari neck vs Marchfolk |
|---|---|
| 168 cm vs macro Marchfolk 168 | −0.1 % (raw FAIL) |
| 173 cm vs Marchfolk 173 | +0.87 % (NOT DEMONSTRATED) |
| 173 cm, five same-composition states | +0.9 % (NOT DEMONSTRATED) |
| 168 cm vs a route-parity native Marchfolk MF168N (comparator only) | +0.9 %, direction present |
| Reference (190) | +3.4 % |

**Cause:** the native route keeps the reference neck share (0.0551–0.0552), while the macro Marchfolk's neck share rises at short stature.

**AE L50** says Aelari necks are "somewhat longer on average than humans", which is a population statement. It is not one of the three relations R1 names. R1's general matched-height clause applies: "differences below the 1 % demonstration threshold are acceptable where the intended direction remains present or effectively equal and the complete anatomical package remains distinct". The Aelari package at 168–173 cm stays distinct:
- head +3.7 % (route parity);
- leg +2.0–2.6 %;
- ribcage depth −6.2 % to −6.7 %;
- knee per bone −7 % to −10 %.

**Classified RESOLVED BY R1 (general clause).** It is surfaced here so the author can confirm. No Aelari neck change is proposed.

**Aelari foot at 168 cm** reads +0.01 % vs macro Marchfolk 168 and +1.5 % at route parity → RESOLVED BY R2 (route parity).

## 6. Complete accounting of prior non-pass items

The W2F gate §13 items, and every non-pass code in the closure run, with classifications as order §9 defines them.

| # | Prior item | Closure result | Classification |
|---|---|---|---|
| 1 | Aelari leg > Marchfolk, matched heights (+0.5 % to +0.8 %) | PASS (R1 reference-state); at 168 / 173 cm after R2 +2.6 % / +2.0 % PASS | **RESOLVED BY R1** (+ R2 at the short end) |
| 2 | Vael E-A2 leg > Marchfolk (+0.6 % to +0.7 %) | PASS (R1 reference-state); Vael 163 after R2 +1.0 % PASS | **RESOLVED BY R1** |
| 3 | VA-P2a Vael leg < Aelari (−0.1 % to +0.1 %; FAIL at 173) | PASS (R1 reference-state) at 178–203; at 173 the native Aelari leg is +1.3 % above Vael | **RESOLVED BY R1 / R2** |
| 4 | Aelari / Vael arm, hand, leg, joints vs Sagekin; Fenn forearm vs Sagekin | OVERLAP (R1 complete anatomy), 63 rows | **ACCEPTED COMPLETE-ANATOMY OVERLAP** |
| 5 | AE-P6 waist interval Aelari > Vael (+0.35 % to +0.64 % at 181–203) | direction present, under 1 % | **RESOLVED BY R1** (general clause; Aelari waist interval > Fenn and Marchfolk holds) |
| 6 | Vael wrist per bone > Aelari at 178 cm (+0.35 %) | unchanged; PASS at 181–203 (+1.3 % to +1.7 %) | **MEASUREMENT NORMALIZATION** (exact plane vs W1 slab) |
| 7 | AE168 / AE173 / FN163 / VA163 short-femur macro route; AE knee / wrist FAIL at 168 / 173 | rebuilt natively; knee / wrist pass | **RESOLVED BY R2** |
| 8 | 53 continuity reversals | 38 left, all explained (§3) | **RESOLVED BY R2** (15) / **GENERATOR LIMIT** (34 junction) / **VALID REPORT-ONLY** (2) / legitimate allometry (2) |
| 9 | FN-09 ×0.5 forearm FAIL | ×0.75: direction present (+0.98 %) | **RESOLVED BY R3** |
| 10 | Aelari foot > Marchfolk at 203 cm (+0.95 %) | direction present | **RESOLVED BY R1** (general clause) |
| 11 | Named-validator moves under 1 % (FN-15 forearm, FN-16 leg, FN-09, AE-20 leg, VL-09 / VL-10 leg) | unchanged | **GENERATOR LIMIT** (target response under re-solved stature) |
| 12 | NOT RUN: configuration 2; face / ear / orbit; elder and cultural validators | unchanged | **OUT OF CURRENT SCOPE** |
| 13 | 173 cm matched point after R2 (the native Aelari 173 meets macro Fenn 173 and Vael 173): Aelari torso > Fenn +0.57 % ND; Vael wrist > Aelari −0.67 % FAIL; VA-P4 +0.52 % ND; Fenn knee < Aelari −0.45 % ND | with all three native at 173 (sensitivity bodies): +1.05 % / +0.04 % / +1.11 % / −3.99 % — torso, VA-P4 and the Fenn knee pass; Vael wrist ≈ Aelari (as item 6) | **GENERATOR LIMIT** (mixed-route matched point) / **MEASUREMENT NORMALIZATION** (wrist) |
| 14 | Vael palm breadth > Aelari at 203 cm (+1.00 %, ND by rounding) | direction present | **RESOLVED BY R1** (general clause) |
| 15 | Aelari neck at 168 / 173 cm (new, §5); Aelari 173 composition neck rows (5 × +0.9 %) | direction present at route parity | **RESOLVED BY R1** (general clause), **surfaced for confirmation** |
| 16 | Accepted W1 rows on non-reference bodies against fixed W1 references (98 "not all pass" body groups) | boundary-stature rule; references 6 / 6 groups PASS | **VALID REPORT-ONLY** (fixed-reference drift) |
| 17 | Frame breadth rows vs unmatched Marchfolk (Fenn Narrow / Broad), REPORT | unchanged | **VALID REPORT-ONLY** (W1-ruled non-veto) |
| 18 | Leg probes (Q) | diagnostics, not applied | **VALID REPORT-ONLY** |

**UNRESOLVED: none.**

## 7. Re-run results by area

| Area | Result |
|---|---|
| Stature / allometry | coherent in all three; head share min > ref > max (6 / 6); continuity per §3 |
| RM-OT-02 matrix (173–203) | Fenn 14 PASS + 1 ND (173 mixed route); Aelari 16 PASS + 4 ND (AE-P6 ×3 under R1; 173 torso is the mixed route); Vael 77 PASS + 4 R1 + 3 ND (VA-P4 173, wrist 178, palm 203) + 1 FAIL (173 wrist, mixed route; parity +0.04 %) |
| vs Marchfolk | Fenn 91 / 91; Aelari 64 PASS + 4 R1 + 3 ND + 1 FAIL (neck 168, §5; foot 168 / 203); Vael 16 PASS + 5 R1 |
| vs Sagekin | Fenn 55 PASS + 5 overlap; Aelari 27 PASS + 23 overlap; Vael 5 overlap |
| Frames | 410 PASS + 4 R1 + 2 report. Breadth system only: lengths, head, neck and hands ±0.5 %; depth and joint per bone ±1 %; Aelari 168 frames rebuilt on the native body |
| Composition | invariance 33 / 33; matched-composition rows pass except the R1 / overlap classes and the Aelari 173 neck rows (§5) |
| Named validators | FN-09 = ×0.75 (§4); all others as in the gate |
| Cross-elf dependencies | reference W1 rows 6 / 6 groups PASS; Fenn-dependent Aelari / Vael rows hold at matched height |

## 8. Preserved, as ordered

- **Fenn:** long limbs, compact torso, shallow and narrow ribcage, the most gracile joints.
- **Aelari:** cranial and neck elongation, longer torso than Fenn, shallow ribcage, pelvic verticality, lower-leg distribution, gracility.
- **Vael:** deeper ribcage and pelvis, more torso, broader palms, more joint presence.
- **Frames** stay a breadth system.
- **Composition** stays firewalled from skeletal proportion.
- **Ears** stay as three families. Face and ear envelopes are carried forward unchanged and remain OPEN for their own gate.

## 9. Records updated

- `decisions/REFERENCE_ANATOMY_V1.md`: R1 and R2 measurement standards.
- `tools/rac/w1/cfg/w2f/ELF-family-boundary.json`: rulings and closure bodies.
- The W2F gate's author-ruling line.
- The order log and the queue note.
- The W2F closure itself is not marked accepted in STATUS until the author reviews it.

**STOP.** Halvren W2 and later race work wait for acceptance of this closure.
