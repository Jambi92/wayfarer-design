# RAC W2F — Elf Family (Fenn / Aelari / Vael) Author-Acceptance Gate

**Author:** Claude (auditor) · **Date:** October 8, 2026 · **Order:** `reviews/chatgpt-rac-w2e-sagekin-final-acceptance-w2f-elf-family-order.md` §4–§17
**Evidence:** `reviews/rac-w2f-elf-evidence/` (`tables.md` is generated; every number below is from `w2f.json`)
**Status:** DESIGN ONLY / NO UE5. NON-CANON diagnostics. No elf, Marchfolk, Sagekin or Skarn canon or body was changed. The leg probes in §12 are diagnostics only and were **not applied**.

## Recommendation

| Population | Recommendation | Reason in one line |
|---|---|---|
| **Fenn** | **ACCEPT** | Every authored direction holds at every matched height, against Marchfolk and against Sagekin. |
| **Aelari** | **CONSTRAIN** | Aelari stays distinct from Sagekin through its whole anatomy. But its "longer legs than humans" relation is NOT DEMONSTRATED at matched height (+0.6–0.8 %). The probes show it cannot be raised past 1 % without breaking "longer arms" and "longer torso than Fenn". |
| **Vael** | **CONSTRAIN** | E-A2 (hip-joint height above humans) and VA-P2a (legs shorter than Aelari) are both NOT DEMONSTRATED at matched height. Strictly read, the two cannot both hold together with the Aelari rows (§12). |
| **Family** | **CONSTRAIN** | One author ruling (R1) is needed on how the coupled vertical-share relations are read at matched height. The rest of the family holds as a complete-anatomy package. |

---

## 1. Construction manifest

**Starting points:** the accepted W1 references, all unchanged:
- FNL4 (Fenn, 181 cm, macro 0.5435);
- AEL1 (Aelari, 190 cm, macro 0.5625);
- VAL4 (Vael, 178 cm, macro 0.5479).

**Configuration:** configuration 1 only; configuration 2 was NOT RUN.

**Route:** the accepted W2A rule, the same one Sagekin W2E used.
- Below 159 cm: the native short-adult route, from each population's accepted base macro, with bone scales and targets carried.
- At 159 cm and above: the generator height macro re-solved.
- No uniform scaling.

**Statures (cm):**

| Population | Statures |
|---|---|
| Fenn | **157** (native) / 163 / 173 / 178 / **181** / 190 / 203 / **211** |
| Aelari | **168** / 173 / 178 / 181 / **190** / 203 / 211 / **221** |
| Vael | **157** (native) / 163 / 173 / **178** / 181 / 190 / **203** |

**Matched points:**
- 173, 178, 181, 190 and 203 cm hold all three elves, Marchfolk and Sagekin.
- Marchfolk 157 (native) and 168 (macro) were built as comparators only.
- 211 and 221 cm sit above Marchfolk (tallest is 203) and are report-only.

**Frames:** the accepted elf breadth-only rule from W1n/W1o/W1p:
- ±8 % on clavicle and rib-cage spine X;
- Broad pelvis ×1.12, Narrow ×0.92;
- depth, lengths and joints unchanged.

Applied at each population's minimum, reference and maximum. I did not use the Skarn or Marchfolk frame write (order §11).

**Composition:**
- six states at 173 cm per population (low muscle, high muscle, higher fat, high both, 0.25 / 0.25, minimum), matched to the Marchfolk 173 and Sagekin 173 states;
- five frame × composition validators per reference.

**Skeletal proxies:** CIB grids (exact-plane S7) for every stature, frame and named body.

**Record:** `tools/rac/w1/cfg/w2f/ELF-family-boundary.json`.

## 2. Stature and allometry

| Reading | FN 157 | FN 181 | FN 211 | AE 168 (macro) | AE 173 native | AE 190 | AE 221 | VA 157 | VA 178 | VA 203 |
|---|---|---|---|---|---|---|---|---|---|---|
| head / stature | 0.1329 | 0.1267 | 0.1214 | 0.1384 | 0.1350 | 0.1314 | 0.1255 | 0.1339 | 0.1292 | 0.1244 |
| neck / stature | 0.0531 | 0.0534 | 0.0519 | 0.0577 | 0.0552 | 0.0554 | 0.0531 | 0.0543 | 0.0545 | 0.0530 |
| torso / stature | 0.2702 | 0.2710 | 0.2680 | 0.2775 | 0.2736 | 0.2741 | 0.2709 | 0.2790 | 0.2797 | 0.2757 |
| leg / stature | 0.5481 | 0.5504 | 0.5606 | 0.5317 | 0.5427 | 0.5442 | 0.5557 | 0.5360 | 0.5380 | 0.5488 |
| ribcage depth / stature | 0.1299 | 0.1237 | 0.1181 | 0.1258 | 0.1242 | 0.1202 | 0.1149 | 0.1418 | 0.1356 | 0.1298 |
| knee / femur (exact plane) | 0.2499 | 0.2377 | 0.2113 | 0.2917 | 0.2516 | 0.2435 | 0.2164 | 0.2773 | 0.2653 | 0.2378 |

**Allometry is coherent.** Head, hands, ribcage and joints fall smoothly relative to stature in all three populations. Head share is greater at the minimum and smaller at the maximum (6 / 6 PASS). The minimum bodies read adult, and the maximum bodies read elongated without uniform scaling (`sheets/*_statures_*.jpg`).

**All 53 continuity reversals are route effects.** Each one sits at a step out of a body whose re-solved macro is below about 0.40: FN163 (0.306), VA163 (0.357), AE168 (0.290) and AE173 (0.359). There the generator's short-stature femur behaviour — which W2A excluded below 159 cm — is still active. Femur / leg, measured on native cross-checks against the macro route:

| Body | Native route vs macro route |
|---|---|
| AE168 | +9.5 % |
| AE173 | +6.5 % |
| FN163 | +9.0 % |
| VA163 | +6.6 % |

The native cross-checks behave coherently. For example, AE173N leg is +2.0 % vs Marchfolk 173, and its knee / bone is −7.0 %.

**Route refinement candidate (construction rule, not biology):** use the native route wherever the re-solved macro falls below about 0.40, not only below 159 cm. → **R2**

## 3. RM-OT-02 family matrix (matched 173 / 178 / 181 / 190 / 203 cm)

**108 PASS, 9 NOT DEMONSTRATED, 3 FAIL.** All three FAILs are at 173 cm and come from AE173's short-femur macro route (§2).

**What holds at every matched height (178–203 cm), with the 190 cm values:**
- Aelari neck > Fenn: +4.7 %.
- Aelari torso > Fenn: +1.5 %.
- Aelari neck / torso > Vael: +4.3 %.
- Vael torso > Fenn: +2.9 %.
- Vael ribcage depth > Fenn and > Aelari: skin +8.6 % / +10.1 %; skeletal +10.0 % / +12.0 %.
- Vael AP pelvic depth > Fenn and > Aelari (VA-P4).
- Vael palm breadth > both.
- Vael elbow and knee per bone > both.
- Gracility order (E-A1): Fenn elbow and knee per bone < Aelari.
- Fenn waist interval < Aelari (FN-P6).

**NOT DEMONSTRATED:**
- **Vael leg < Aelari (VA-P2a), at 178–203 cm: −0.1 % to +0.1 %.** Vael and Aelari leg shares are equal at matched height. → R1
- Aelari waist interval > Vael (AE-P6): +0.3 % to +0.4 % at 181–203 cm.
- Vael wrist per bone > Aelari at 178 cm: +0.35 %. It passes at 181–203 cm (+1.3 % to +1.7 %).
- Vael palm breadth > Aelari at 203 cm.

**Each population's identity in the complete body** (`sheets/elf_family_matched_181.jpg`, `_190.jpg`):
- **Fenn:** long limbs (arm +5.1 %, leg +2.5 % vs Marchfolk 190), long lower leg, long hands, fingers and feet, compact torso (−3.7 %), shallow and narrow ribcage, and the most gracile joints.
- **Aelari:** vertical elongation through the cranium (head +3.9 %), neck (+3.4 %), lower leg (lower leg / leg +4.0 %) and pelvis (pelvic vertical / thoracic vertical +8.9 %), with a shallow ribcage (−6.2 %) and gracile joints. It is not "only long arms or legs".
- **Vael:** deep ribcage (+3.3 % vs Marchfolk), the most torso among the elves, deep pelvis, more joint presence and broad palms. It is not "ocean Aelari": Vael and Aelari differ in depth by 10–12 %.

## 4. Matched-height Marchfolk and Sagekin checks

### Against Marchfolk (each population's own authored directions)

**Fenn: 91 / 91 PASS from 157 to 203 cm.**

**Aelari: 61 PASS, 9 NOT DEMONSTRATED, 2 FAIL.**
- **Leg share > Marchfolk is NOT DEMONSTRATED at every matched height (+0.5 % to +0.8 %).** → R1
- Foot share is NOT DEMONSTRATED at 203 cm.
- At 168 / 173 cm, knee per bone FAILs and wrist per bone is NOT DEMONSTRATED. These come from the route (§2): the native AE168N / AE173N read knee −10.1 % / −7.0 %.
- Neck, arms, hands, ribcage depth and the other joints pass.

**Vael: 15 PASS, 6 NOT DEMONSTRATED.**
- **E-A2 hip-joint height (leg share) > Marchfolk is NOT DEMONSTRATED at every height (+0.6 % to +0.7 %).** → R1
- Bitrochanteric / crest and AP pelvic depth pass.

The fixed-reference W1 rows pass at all three references (§10). The matched-height rows govern under the boundary-stature rule.

### Against Sagekin W2E (the required dependency, order §9)

**Fenn: 55 PASS, 5 NOT DEMONSTRATED.** The five are forearm / arm, which is effectively equal to Sagekin (e.g. 0.3754 vs 0.3740 at 181). Every other exposed reading separates:

| Reading | Fenn vs Sagekin 181 |
|---|---|
| arm | +2.8 % |
| hand | +2.3 % |
| finger / hand | +2.0 % |
| span | yes |
| leg | +1.3 % |
| lower leg / leg | +3.8 % |
| foot | +4.9 % |
| ribcage depth | −2.2 % |
| ribcage breadth | −2.8 % |
| wrist per bone | −10.6 % |
| knee per bone | −7.1 % |

**Fenn's complete anatomy is distinct.**

**Aelari: 26 PASS, 18 FAIL, 6 NOT DEMONSTRATED.**
- **Sagekin exceeds Aelari** on arm, hand and leg share at every height (at 190: arm −0.7 %, hand −1.1 %, leg −0.5 %).
- **Aelari and Sagekin are about equal** on wrist and knee per bone.
- **Aelari is distinct through its axial and vertical package** (at 190):

| Reading | Aelari vs Sagekin 190 |
|---|---|
| head | +4.5 % |
| neck | +3.9 % |
| neck / torso | +4.3 % |
| ribcage depth (skin) | −3.4 % |
| ribcage depth (skeletal) | −4.2 % |
| ribcage breadth | −4.4 % |
| iliac-crest breadth | −7.0 % |
| waist interval | +2.0 % |
| pelvic vertical / thoracic vertical | +7.1 % |
| lower leg / leg | +4.0 % |
| foot | +1.9 % |
| ankle per bone | −4.8 % |
| elbow per bone | −2.5 % |

Under the W2E ruling (isolated scalar overlap is not an elf failure), Aelari's **complete anatomy remains distinct**. The limb-share overlap with Sagekin is real: Aelari limbs are not longer than the long-limbed human end. AE L183 lists limbs among the carriers, so this sits under R1.

**Vael: leg share vs Sagekin FAILs at every height.** The comparison runs in the E-A2 direction, and Sagekin legs are +0.6 % to +1.3 % longer. Vael is distinct from Sagekin through ribcage depth (+6.4 % at 190), torso (+0.9 %), pelvic depth and broader palms. Hips relative to Sagekin are the same E-A2 item. → R1

## 5. Exact-plane joint re-measurement (W1 measurement normalization)

The exact-plane anatomical section was used for every newly scored joint row, both per adjacent bone and per stature (`joint_sections.json`).

**The W1 conclusions hold at the references with exact-plane sections:**
- **Fenn:** wrist per bone −13.6 % and knee per bone −9.0 % vs Marchfolk 181.
- **Aelari:** elbow −1.9 %, wrist −3.6 % and knee −3.2 % per bone vs Marchfolk 190.
- **Vael:** elbow, wrist and knee per bone > Fenn and > Aelari at 181–203 cm.
- **Gracility order** Fenn > Aelari > Vael holds at every matched height (E-A1).

**One normalization consequence:** Vael wrist per bone > Aelari is +0.35 % at 178 cm, which is NOT DEMONSTRATED. The W1 slab row passed. This is classed as **measurement normalization**, not redesign, and the row passes at 181 cm and above.

**Unchanged rules:** J-1 / J-3 / J-4 are preserved, and gracility does not follow muscularity. Composition states change skin joint breadths, but the skeletal proxies are shared.

## 6. Pelvic / axial diagnostics (RM-UB-06; report only)

**At the references, the accepted skeletal rows pass** (§10):
- E-A2 bitrochanteric / crest ≥ Marchfolk;
- FN-P5 / FN-P6;
- AE-P3 / AE-P6;
- VA-P4.

**Matched-height cross-elf pelvic rows (§3) hold, except** AE-P6 vs Vael, which is NOT DEMONSTRATED.

**At the boundaries (157 / 168 / 203 / 211 / 221 cm)** the pelvic readings keep their population pattern (report):
- Aelari has the tallest pelvic vertical and the narrowest crest.
- Vael has the deepest pelvis.

**Rules kept:** obstetric firewall maintained, external landmarks only, and no new pelvic specialization.

## 7. Narrow / Balanced / Broad (all three populations)

**410 PASS, 4 NOT DEMONSTRATED, 2 REPORT.** Frames were applied at min / reference / max for each population.

**What the frames move, and what they leave alone:**
- Breadth readings move at least 1 % each way: thorax, girdle, biacromial, crest, and hip spacing (carried with the crest).
- Unchanged within 0.5 %: lengths, head, neck and hands.
- Unchanged within 1 %: thoracic depth and every joint per bone. Frame does not set gracility, and Narrow is not "more elven".

**The 4 NOT DEMONSTRATED** are the Aelari and Vael frame bodies' leg share vs Marchfolk, the same R1 item.

**The 2 REPORT** are Fenn Narrow / Broad thoracic breadth vs unmatched Marchfolk, which W1 ruled a non-veto.

**Broad Aelari stays Aelari:** depth, joints and torso stay far from Skarn (§9).

## 8. Composition (all three)

- **Invariance: 33 / 33.** No composition state moves torso, leg, arm, forearm, lower leg, hand or neck by 1 % or more, from minimum up to high muscle plus fat, including the frame × composition validators.
- **Same composition and matched height (173 cm vs Marchfolk 173 and Sagekin 173 in the same state):**
  - **Fenn:** every row passes vs Marchfolk. Forearm vs Sagekin is NOT DEMONSTRATED, as in §4.
  - **Aelari and Vael:** the leg rows repeat the §4 picture — NOT DEMONSTRATED vs Marchfolk, FAIL vs Sagekin. AE173 also carries the route effect.
  - Every other row passes in every state.
- **Identity is skeletal, not thinness.** The minimum-composition and high-composition bodies keep the same patterns (`sheets/elf_composition_173.jpg`). Low muscle or low fat was not used to rescue anything.

## 9. Named body-validator dispositions

| Validator | Disposition |
|---|---|
| FN-01 / AE-01 / VL-01 (references) | accepted W1 rows all PASS (§10) |
| FN-02 157, FN-03 211 | coherent; directions hold vs Marchfolk 157 and vs Marchfolk 203 (report) |
| AE-02 168, AE-09 short Aelari | macro route in the short-femur zone (§2); the native AE168N holds the Aelari pattern (leg +2.6 %, knee −10.1 % vs Marchfolk 168) |
| AE-03 221, AE-24 combined stress | coherent; Skarn guard clear (vs Skarn 229: depth −19.7 %, girdle −12 %, knee per bone −25 %); Broad 221 matches Skarn crest (−1.1 %) but not depth, joints or torso |
| VL-02 157, VL-03 203, VL-24 | coherent; Vael directions hold except the R1 leg item |
| FN-04/14, AE-13, VL-16 (Narrow low / low) | proportions invariant; joint stress readings in tables |
| FN-05/AE-05/VL-05, Broad + high muscle, high fat, Broad + high fat, Narrow + high muscle | proportions invariant (33 / 33) |
| FN-15 maximum arm + hand | arm +3.3 %, hand +4.2 % vs reference; Fenn directions hold |
| FN-16 maximum leg + foot | leg +0.9 % (NOT DEMONSTRATED as a move; generator response); directions hold |
| FN-09 short-limbed near the boundary | at ×0.5 the forearm direction **FAILs** vs Marchfolk 181 and Sagekin 181; at ×0.75 all Fenn directions hold (forearm +0.98 %, NOT DEMONSTRATED). **Propose FN-09 = ×0.75** |
| FN-08 long torso | valid; directions hold |
| AE-19 / AE-20 / AE-11 | valid; the R1 leg item persists (AE-20 leg +1.6 % vs Marchfolk 190, but arm and torso drop to NOT DEMONSTRATED, §12) |
| VL-09 long-limbed | leg rises above Aelari (FAIL VA-P2a), part of R1; VL-10 compact and VL-23 deep ribcage + Narrow valid |
| Hidden-ear / face / ear validators | out of body scope (§11) |

## 10. Cross-elf dependency re-checks

**At the references, all accepted W1 rows pass with the other elves at their W1 references** (the W1 Fenn-dependent Aelari / Vael rows included):

| Reference | Directional | Skeletal |
|---|---|---|
| FN181 | 24 / 24 | 10 / 10 |
| AE190 | 20 / 20 | 11 / 11 |
| VA178 | 14 / 14 | 8 / 8 |

**At matched height (§3), every Fenn-dependent Aelari and Vael row holds** (Aelari neck and torso > Fenn, Vael torso and depth > Fenn, FN-P6). The exceptions are the Vael-vs-Aelari leg and waist items.

## 11. Body vs craniofacial / ear scope

This gate is a **body** gate. Carried forward and not re-measured:
- RM-CF-08 orbit relationships (accepted W1 O-1 rings);
- RM-UF-02 ear families;
- the Aelari face-length row.

No body conclusion here depends on them. Fenn, Aelari and Vael ears stay separate families. The face / ear envelopes remain OPEN.

## 12. The R1 contradiction, measured (probes NOT applied)

At fixed stature, leg + torso + neck + head ≈ 1 (sum 1.000–1.005 for every body). Aelari's authored cranial elongation makes its head share +3.9 % above Marchfolk. Read strictly (≥ 1 % each), the matched-height rows require at 190 cm:

| Row | Required at 190 cm |
|---|---|
| Aelari leg > Marchfolk (AE L33–58) | ≥ 0.5455 |
| Aelari torso > Fenn (AE L40 / L48 / L58) | ≥ 0.2727 |
| Aelari neck > Marchfolk and Fenn | ≥ 0.0541 |
| Vael leg > Marchfolk (E-A2) | ≥ 0.5455 |
| Vael leg < Aelari (VA-P2a) | so Aelari ≥ 0.5510 |

- **Aelari rows alone:** leg 0.5455 + torso 0.2727 + neck 0.0541 + head 0.1314 = 1.0037. That fits inside Aelari's 1.0051 with about 0.13 % of stature to spare.
- **With the Vael rows:** leg 0.5510 + 0.2727 + 0.0541 + 0.1314 = 1.0092. That **exceeds** 1.0051, so it is infeasible unless Aelari loses cranial elongation (AE L40, AE head).

**Probes** (Aelari's own leg targets scaled, stature re-solved to 190):

| Probe | Leg vs Marchfolk | Arm vs Marchfolk | Torso vs Fenn | Neck vs Fenn |
|---|---|---|---|---|
| ×1.75 | +2.05 % PASS | −0.29 % **FAIL** | −0.21 % **FAIL** | +3.3 % |
| ×2.0 | +2.48 % | −0.94 % **FAIL** | −0.79 % **FAIL** | +2.8 % |
| ×2.5 | +3.37 % | −2.22 % **FAIL** | −1.96 % **FAIL** | +1.8 % |

Vael with its lower-leg decrease removed: leg +0.85 % vs Marchfolk (NOT DEMONSTRATED), and the Vael leg < Aelari row FAILs (+0.09 %).

**The smallest genuine contradiction:** the strict matched-height reading of E-A2 (Vael and Aelari) together with VA-P2a and the Aelari "even elongation plus longer torso than Fenn" rows. No elf-only target or bone change satisfies all of them at once. The W1 passes came from comparing each elf at its own reference stature against Marchfolk 173, where generator allometry adds about 2 % leg share by 190 cm.

## 13. Every non-PASS / NOT RUN / generator-limit item

| # | Item | Class |
|---|---|---|
| 1 | Aelari leg > Marchfolk, all matched heights (+0.5 % to +0.8 %) | NOT DEMONSTRATED → R1 |
| 2 | Vael E-A2 leg > Marchfolk, all heights (+0.6 % to +0.7 %) | NOT DEMONSTRATED → R1 |
| 3 | VA-P2a Vael leg < Aelari (−0.1 % to +0.1 %) | NOT DEMONSTRATED; FAIL at 173 (route) → R1 |
| 4 | Aelari / Vael leg, arm and hand vs Sagekin | FAIL / NOT DEMONSTRATED single readings; complete anatomy distinct (W2E ruling) → R1 for limbs |
| 5 | AE-P6 waist interval Aelari > Vael (+0.3 % to +0.4 %) | NOT DEMONSTRATED |
| 6 | Vael wrist per bone > Aelari at 178 cm (+0.35 %) | measurement normalization (exact plane) |
| 7 | AE168 / AE173 / FN163 / VA163 short-femur macro route; all 53 continuity reversals; AE knee / wrist FAIL at 168 / 173 | generator route → R2 |
| 8 | Fenn forearm / arm vs Sagekin (≈ equal) | single-reading overlap, allowed |
| 9 | FN-09 at ×0.5 forearm FAIL | validator definition → R3 (×0.75) |
| 10 | AE foot > Marchfolk at 203 cm | NOT DEMONSTRATED |
| 11 | Named-validator moves under 1 % (FN-16 leg, AE-20 leg, VL-09 / -10 leg) | generator target response |
| 12 | NOT RUN | configuration 2; face / ear / orbit (§11); SG-like elder and cultural validators; ALPC-type stress beyond the named set |

## 14. Canon challenge statement

**The matched-height reading of the coupled elf vertical-share relations needs an author ruling (R1).**

The rows involved:
- E-A2 hip-joint height > Marchfolk, for Aelari and Vael;
- VA-P2a Vael leg < Aelari;
- AE L33–58 "longer legs (even elongation)";
- AE "longer torso than Fenn";
- AE "neck longer".

The canon is not wrong. As written and verified in W1 these were reference-state relations. Read strictly at matched height they cannot all hold together given Aelari's authored cranial elongation.

**Options for R1:**
- **(a) Reference-state reading.** Treat E-A2, VA-P2a and the Aelari leg relation as reference-state population relations. They hold at the W1 references, and at matched height the direction holds with margins under 1 % (classed as ND, accepted). This needs no body change. Recommended.
- **(b) Matched-height correction.** Require matched-height ≥ 1 % on the Aelari leg only, and relax VA-P2a and the Vael E-A2 row to direction-only. The bounded Aelari correction would move about 0.2–0.3 % of stature from torso into lower leg, with arm targets compensating. It is not built, because the window is about 0.13 % of stature and not robust.
- **(c) Accept the Sagekin overlap.** Accept that Aelari limbs do not exceed the long-limbed human (Sagekin) end, and that Aelari's distinction from humans is carried by the cranium, neck, ribcage, pelvis, lower-leg distribution and gracility (§4).

**Other rulings:**
- **R2 (construction only):** native route wherever the re-solved macro is below about 0.40.
- **R3:** FN-09 defined at ×0.75.

## 15. Recommendations

- **Fenn: ACCEPT** the W2F family (157–211 cm), frames, composition and named validators, with FN-09 at ×0.75 (R3).
- **Aelari: CONSTRAIN**, pending R1 (and R2 for AE-02 / 168–173 cm). No correction is applied.
- **Vael: CONSTRAIN**, pending R1. No correction is applied.
- **Family: CONSTRAIN.** One ruling, R1, decides the Aelari and Vael leg relations. The family otherwise holds as three distinct complete anatomies, and against Marchfolk, Sagekin and Skarn.

**STOP.** Halvren W2, the short-race W2s, Saurin W2, Wave 3 work, creator envelopes, facial extremes and UE5 work were not started.
