# RAC W2E — Sagekin W2 Author-Acceptance Gate

**Author:** Claude (auditor) · **Date:** October 8, 2026 · **Order:** `reviews/chatgpt-rac-w2d-gorrund-final-acceptance-w2e-sagekin-order.md` §5–§15
**Author ruling (October 8, 2026; reviews/chatgpt-rac-w2e-sagekin-final-acceptance-w2f-elf-family-order.md):** ACCEPT — Sagekin W2E FINAL AUTHOR ACCEPTED / CLOSED. SG-04 x1.5 accepted as the W2E long-limbed boundary diagnostic. Isolated scalar overlap with W1 Fenn / Aelari is not an elf failure and no Sagekin change is made; the overlap is carried to Elf W2F as a complete-anatomy dependency. Route seam, fixed-reference drift and composition-vs-neutral skin items retained as diagnostics. DU-P4 stays OPEN with Durrim W2.
**Evidence:** `reviews/rac-w2e-sg-evidence/` (`tables.md` is generated; every number below is from `w2e.json`)
**Status:** DESIGN ONLY / NO UE5. NON-CANON diagnostics. No Sagekin canon was rewritten, and no Marchfolk, Skarn, Fenn, Aelari or Durrim body was changed. Comparators are the accepted bodies, with the W2C1 knee reverts applied (Marchfolk 190 and 203 configuration 1 = uncorrected bodies).

**Recommendation: ACCEPT.** The Sagekin family from 152 to 208 cm keeps every authored RM-OT-01 tendency against Marchfolk at every matched height (48 / 48). It keeps them at every matched composition too (36 / 36). Frames and composition behave as human variation, and no Sagekin correction is needed.

What remains:
- route effects at the 152 / 163 cm seam;
- fixed-reference drift;
- **provisional** single-reading overlaps with the W1 Fenn / Aelari bodies. Sagekin canon allows single-reading overlap (SG L465). These are handed to elf W2.

---

## 1. Body / construction manifest

Configuration 1 only, because the accepted Sagekin W1 reference is configuration 1. Configuration 2 is NOT RUN.

**Route:** the accepted Marchfolk W2A boundary-route rule, applied to the accepted Sagekin build.
- Below 159 cm: the native short-adult route, from Sagekin's accepted base macro (0.537109375).
- At 159 cm and above: the generator height macro re-solved, with the same Sagekin targets.
- No uniform scaling anywhere.
- Record: `tools/rac/w1/cfg/w2e/SG-boundary.json`.

| Body | Role | Route / macro | Stature (cm) |
|---|---|---|---|
| SG152 | SG-02 minimum | native, base 0.537 | 152.0 |
| SG163 | continuity / Marchfolk overlap | macro 0.329 | 163.0 |
| SG173 | matched to the Marchfolk reference | macro 0.463 | 173.0 |
| SG178 | SG-01 reference (accepted W1, unchanged) | macro 0.537 | 178.0 |
| SG181 / SG190 | matched to Fenn W1 (181) / Aelari W1 and Marchfolk 190 | macro 0.554 / 0.617 | 181.0 / 190.0 |
| SG203 | matched to the tallest Marchfolk | macro 0.707 | 203.0 |
| SG208 | SG-03 maximum | macro 0.742 | 208.0 |

**Frames:** the accepted human W2A1 frame writes (set B Broad, set C Narrow), applied at 152, 178 and 208 cm.

**Composition:** six states on SG173, plus SG-06 / -07 / -08 on the 178 cm frames.

**Named validators:**
- SG-04: limb and hand targets ×1.5. Probes at ×1.75 and ×2.0 are kept.
- SG-09: torso-length direction reversed.
- SG-10: every Sagekin target at half strength.

**Matched Marchfolk comparators built here** (comparators only; Marchfolk unchanged):
- MF163, MF178, MF181 on the accepted macro route;
- MF163N and SG163N as native-route cross-checks.

**Skeletal proxies:** full CIB grids (exact-plane S7) for every Sagekin skeleton body.

## 2. Stature / allometry (152 → 208 cm)

| Reading | 152 | 163 | 173 | 178 | 190 | 203 | 208 |
|---|---|---|---|---|---|---|---|
| torso / stature | 0.2760 | 0.2796 | 0.2777 | 0.2769 | 0.2752 | 0.2736 | 0.2730 |
| leg / stature | 0.5392 | 0.5328 | 0.5392 | 0.5417 | 0.5469 | 0.5518 | 0.5535 |
| head / stature | 0.1350 | 0.1330 | 0.1294 | 0.1282 | 0.1257 | 0.1234 | 0.1226 |
| hand / stature | 0.1201 | 0.1223 | 0.1186 | 0.1177 | 0.1166 | 0.1155 | 0.1151 |
| finger / hand | 0.4590 | 0.4590 | 0.4591 | 0.4590 | 0.4586 | 0.4583 | 0.4581 |
| skeletal thoracic breadth / stature | 0.1665 | 0.1652 | 0.1605 | 0.1589 | 0.1559 | 0.1530 | 0.1519 |
| skeletal thoracic depth / stature | 0.1182 | 0.1161 | 0.1141 | 0.1129 | 0.1107 | 0.1087 | 0.1079 |
| knee section / stature | 0.0724 | 0.0726 | 0.0694 | 0.0688 | 0.0679 | 0.0664 | 0.0655 |
| femoral S7 breadth / stature | 0.0767 | 0.0762 | 0.0740 | 0.0730 | 0.0712 | 0.0696 | 0.0691 |

**Size readings change smoothly with stature.** Head, hands, joints, skeletal breadth and depth all fall smoothly relative to stature: the head is 5.3 % larger at 152 cm and 4.3 % smaller at 208 cm than at 178 cm. No single global factor produces this. Above 173 cm the family is monotonic on every reading.

**Route seam reversals are route effects, not Sagekin anatomy.** 22 of the 23 continuity reversals sit at the 152 → 163 → 173 cm seam. The generator macro's short-stature femur behaviour, which W2A excluded below 159 cm, still reaches 163 cm. At 163 cm the macro route reads femur / leg −6.4 % lower than the native route for Sagekin and −5.1 % lower for Marchfolk. Matched Sagekin-vs-Marchfolk rows are unaffected, because both populations share the route at every height. The native 163 cm cross-check passes the same RM-OT-01 directions.

**The one remaining reversal:** skeletal shoulder-joint breadth / stature, −1.8 % at 173 → 178 cm (it also reverses at the seam). The exact-plane knee does not reverse above the seam; slab joint ratios are historical and are not scored.

**The route base macro barely matters.** The SG152 route cross-check (base 0.537 vs the W1t proxy's 0.5) changes every share by ≤ 0.4 %.

**Renders** (`sg_statures_152_178_208.jpg`): 152 cm reads adult, and 208 cm reads human with no elongation.

## 3. RM-OT-01: Sagekin vs Marchfolk at matched height — 48 / 48 PASS

Matched heights: 152, 163, 173, 178, 190 and 203 cm.

| Tendency (canon) | Margin range across the six heights |
|---|---|
| torso share lower (SG L137–141) | −1.7 % to −2.3 % |
| leg share greater | +1.2 % to +1.7 % |
| forearm / arm greater (SG L138) | +1.1 % to +1.6 % |
| hand / stature greater (SG L155–157) | +4.4 % to +5.6 % |
| finger / hand greater | +4.7 % to +5.6 % |
| palm breadth / hand lower (slightly narrower hands) | −4.0 % to −4.7 % |
| skin ribcage depth / stature lower (SG L89, L141) | −2.6 % to −3.2 % |
| skeletal thoracic depth / stature lower (RAC-03) | −3.2 % to −4.4 % |

**The thinnest margin** is forearm / arm at 152 cm (+1.05 %). Every margin is a modest tendency, not a separation, which is what the canon intends.

**Report only:**
- Thoracic breadth is not reduced. Skeletal breadth is within about 1 % of Marchfolk, matching v1.1 §1: reduced depth, not an undefined breadth reduction.
- Arm share is +2.5 % to +3 %.
- Sagekin 208 vs the tallest Marchfolk (203) keeps the same directions.

**Fixed-reference rows.** The accepted W1 directional rows against fixed Marchfolk 173 drift at the boundaries:
- Forearm / arm falls with macro stature for both populations: Sagekin 0.3750 → 0.3665 and Marchfolk 0.3705 → 0.3624. The fixed-reference row therefore reads FAIL at 203 and 208 cm and NOT DEMONSTRATED at 152, 163, 181 and 190 cm.
- Ribcage depth reads FAIL at 152 cm. Ribcage depth / stature rises as stature falls (allometry).

The stature-matched rows govern under the boundary-stature rule.

## 4. Pelvis / axial (RM-UB-06; pelvic shape OPEN, report only)

At 178 cm against Marchfolk, all within 1 %:
- crest −0.7 %;
- AP pelvic depth −0.9 %;
- pelvic vertical −0.7 %;
- hip-joint spacing −0.8 %;
- bitrochanteric / crest −0.05 %;
- waist interval / torso −0.2 %.

**Above 1 %:**
- pelvic AP / thoracic depth +2.8 %, a consequence of the reduced ribcage depth;
- pelvic vertical / thoracic vertical +1.7 %, consistent with the slightly shorter torso.

The same pattern holds at 152, 173 and 203 cm. Spine–pelvis continuity is ordinary human anatomy. No Sagekin pelvic specialization is authored or proposed, and only external skeletal landmarks were used (obstetric firewall).

## 5. Skarn guard (report only; canon is silent on Sagekin-vs-Skarn directions)

**At 190, 203 and 208 cm, Sagekin stays well inside the ordinary human organization.** At 208 cm:

| Reading, Sagekin 208 vs Skarn 208 | Difference |
|---|---|
| skeletal thoracic depth | −18 % |
| shoulder-joint breadth | −10 % |
| thoracic breadth | −5 % |
| torso share | −8 % |
| knee per bone | −26 % |
| wrist per bone | −25 % |

**Broad Sagekin 208:**
- vs Broad Skarn: −18 % depth, −8 % girdle, −26 % knee.
- vs Balanced Skarn: breadth converges (thorax −0.7 %, crest −0.1 %), but depth (−16 %), girdle (−4 %), torso share (−8 %) and joints (−9 % to −24 %) stay far apart. Breadth alone does not make Broad Sagekin Skarn.

## 6. Provisional anti-elf sanity (W1 Fenn / Aelari only)

These rows are **PROVISIONAL**. A row is scored only where the W1 elf differs from matched Marchfolk (181 / 190 cm) by at least 1 %. Final elf boundaries belong to elf W2.

| Pair | Scored | PASS | Non-PASS |
|---|---|---|---|
| Sagekin 181 vs Fenn 181 (matched) | 14 | 13 | forearm / arm NOT DEMONSTRATED (−0.4 %) |
| Sagekin 178 vs Fenn 181 | 14 | 13 | forearm / arm NOT DEMONSTRATED (−0.1 %) |
| SG-04 (×1.5) vs Fenn 181 | 14 | 10 | forearm / arm **FAIL** (+0.8 %), finger / hand **FAIL** (+0.4 %), span NOT DEMONSTRATED (−0.9 %), hand share NOT DEMONSTRATED (−0.5 %) |
| Narrow Sagekin 178 vs Fenn 181 | 14 | 11 | skin thoracic breadth **FAIL** (−1.6 %), ribcage depth NOT DEMONSTRATED (+0.4 %), forearm NOT DEMONSTRATED |
| Sagekin 190 vs Aelari 190 (matched) | 11 | 7 | arm share **FAIL** (+0.7 %), hand share **FAIL** (+1.1 %), forearm / wrist NOT DEMONSTRATED |

**Every scored pair stays human on the complete anatomy.** These readings stay on the human side in every pair:
- leg share;
- lower-leg / leg (Fenn +3 %);
- foot;
- ribcage depth;
- elbow, knee and ankle per bone.

**The overlaps are single readings.** SG L465 allows single measurements to overlap, provided the complete anatomy never reproduces elven anatomy:
- **Forearm:** the accepted Sagekin forearm tendency already equals W1 Fenn's (0.3750 vs 0.3754).
- **Arm and hand share:** W1 Aelari's arm share is only 1.6 % above matched Marchfolk, and its hand share 3.5 % above. Both sit inside the authored Sagekin range.

**Flag for elf W2:** W1 Aelari's limb and hand readings and W1 Fenn's forearm do not exceed the authored Sagekin tendencies. This is not a Sagekin problem and no Sagekin change is proposed.

**SG-04 definition.** The ×2.0 probe crosses Fenn on forearm (+1.8 %), finger (+2.8 %) and hand (+1.1 %), so SG-04 was set at ×1.5, where only two single readings cross by less than 1 %. Cross-height rows (SG-04 and Narrow 208 vs Aelari 190) are report-only.

## 7. Narrow / Balanced / Broad

**Frame moves:** at 152, 178 and 208 cm, the accepted human frame writes move the following readings by 4.8–5.4 % each way. The one exception is Broad girdle breadth, which moves +2.5 % to +6.9 %.
- thoracic breadth;
- shoulder-joint breadth;
- biacromial;
- crest;
- hip-joint spacing.

**Lengths are unchanged:** stature, torso, leg, arm, forearm, lower leg, head, hand and finger are each within 0.5 % (0.00 %).

**Depth and joints follow the frame write, as authored for humans:**
- thoracic depth: Narrow −2.5 %, Broad +2.5 %;
- joints per bone: Narrow −1.4 % to −2.2 %, Broad +2.5 % to +6.7 %.

**Each frame stays a human frame:**
- **Broad Sagekin remains possible and human.** Against Broad Marchfolk it keeps the RM-OT-01 directions (report), and resemblance to Marchfolk is allowed.
- **Narrow Sagekin is not elf-like.** Against Fenn its limbs, legs and joints stay human (§6). The one single-reading overlap is skin thoracic breadth, which Narrow is meant to reduce.
- **Human alignment holds.** Crest / thoracic breadth and depth / breadth stay with the matching Marchfolk frame (report).
- **Frame does not set composition.**

## 8. Composition

- **Invariance:** 9 / 9 states keep torso, leg, arm, forearm, lower-leg, hand and finger within 1 % of their skeleton body, from minimum composition (0 / 0) up to high muscle plus fat.
- **Same composition, matched height (173 cm vs Marchfolk 173 in the same state):** 36 / 36 PASS, in the low-muscle, high-muscle, higher-fat, high-both, 0.25 / 0.25 and minimum states. Rows tested: torso, leg, forearm, hand, finger and skin ribcage depth. The thinnest margin is forearm at +1.27 %.
- **Identity does not come from body type.** Thinness, low muscle and low fat are not identity carriers, and composition was not used to repair anything.
- **Fixed-reference skin depth moves with composition.** The accepted W1 ribcage-depth row against neutral Marchfolk 173 reads FAIL on SG173-LOWMUS and SG173-HIBOTH, because skin depth changes with composition. The composition-matched rows pass.

## 9. SG-01…SG-10 dispositions

| Validator | Body | Disposition |
|---|---|---|
| SG-01 reference 178 | SG178 (accepted W1) | all accepted W1 rows PASS; RM-OT-01 vs MF178 8 / 8 |
| SG-02 minimum 152 | SG152 (native) | RM-OT-01 vs MF152 8 / 8; adult head 0.135; fixed-reference drift only |
| SG-03 maximum 208 | SG208 | directions hold vs the tallest Marchfolk (report); Skarn guard clear; no elongation |
| SG-04 long-limbed near the boundary | SG04 (×1.5) | RM-OT-01 stronger (hand +6.6 %, finger +7.9 %, forearm +2.6 %, leg +1.8 %); moves leg +0.4 % and forearm +0.9 % beyond the reference (NOT DEMONSTRATED, a generator response); provisional Fenn ceiling §6 |
| SG-05 short and Broad | SGB152 | frame moves 3.5–5.4 %, lengths kept; ribcage-depth fixed-reference FAIL (depth +2.5 % by frame) |
| SG-06 Broad + highly muscular | SG06 | proportions invariant; valid |
| SG-07 Broad + high fat | SG07 | proportions invariant; valid |
| SG-08 Narrow + muscular | SG08 | proportions invariant; valid |
| SG-09 long torso | SG09 | torso +2.3 % vs reference, reaching Marchfolk (+0.3 %); valid per RAC-03 (longer-torso Sagekin valid) |
| SG-10 Marchfolk-overlap edge | SG10 | torso, leg, arm, forearm and lower leg within 2 % of MF178 (torso −1.0 %, leg +0.7 %); hand +2.5 %, finger +2.7 %; ambiguity accepted (SG L195) |
| SG-11…14 | — | out of scope (order §12) |

## 10. Exact-plane joints and long bone (RM-UB-03; report only)

**At 178 cm vs Marchfolk** (no Sagekin direction is authored):

| Reading | Per stature | Per adjacent bone |
|---|---|---|
| elbow | −0.5 % | +0.6 % |
| wrist | +0.5 % | −3.5 % |
| knee | −0.7 % | −2.0 % |
| ankle | −1.0 % | −2.3 % |

The per-bone values sit lower because the limbs are longer, not because the joints are smaller.

**Long bone:** femoral shaft / femur −3.8 %, S7 breadth −2.1 %.

**Continuity:** joints are continuous above the seam. Knee per stature runs 0.0694 → 0.0655 from 173 to 208 cm.

No racial joint or robusticity difference is asserted.

## 11. The 152 cm Durrim–Marchfolk–Sagekin dependency (RAC-04)

**Run:** the Sagekin side and the Marchfolk side on accepted / current methods.

**Durrim compared without redesign** (W1t DU152 body, report only). Durrim stays clearly apart from both Sagekin and Marchfolk:

| Reading | Durrim vs Sagekin | Durrim vs Marchfolk |
|---|---|---|
| torso | +7.6 % | +5.1 % |
| skeletal thorax breadth | +8.6 % | +7.8 % |
| girdle | +11.3 % | +10.6 % |
| neck | −12.8 % | −14.0 % |
| knee per bone | +12.9 % | +9.2 % |
| wrist per bone | +34 % | +30 % |

**Durrim-specific matter stays with Durrim.** Skeletal AP pelvic depth / stature reads +1.0 % vs Sagekin and +0.8 % vs Marchfolk; this is DU-P4, which stays **OPEN / CARRIED to Durrim W2**. It was not pre-accepted or redesigned here.

**Classification:** the Sagekin side is complete. The three-way comparison is reported, and the Durrim side is owned by Durrim W2.

## 12. Every non-PASS / NOT RUN / generator-limit item

| # | Item | Class |
|---|---|---|
| 1 | 152 / 163 cm route seam: 22 of 23 continuity reversals; macro short-stature femur at 163 cm (−6.4 % Sagekin, −5.1 % Marchfolk vs native) | generator route; matched rows unaffected |
| 2 | Shoulder-joint breadth / stature −1.8 % at the 173 → 178 cm step | NON-MONOTONIC, generator route |
| 3 | Accepted W1 rows vs fixed Marchfolk 173 | drift, boundary-stature rule: forearm FAIL at 203 / 208; NOT DEMONSTRATED at 152 / 163 / 181 / 190; ribcage depth FAIL at 152 and on SGB152; leg and torso NOT DEMONSTRATED on SG09 (by design) |
| 4 | Composition skin depth vs neutral Marchfolk 173 | FAIL on SG173-LOWMUS / -HIBOTH; composition-matched rows pass |
| 5 | Provisional anti-elf | 5 FAIL and 8 NOT DEMONSTRATED (§6); single readings; elf W2 |
| 6 | SG-04 movement beyond the reference | leg +0.4 %, forearm +0.9 %: NOT DEMONSTRATED; generator target response |
| 7 | NOT RUN | configuration 2 (no accepted configuration-2 Sagekin reference); SG-11…14; craniofacial / ear / presentation |

## 13. Canon challenge statement

**No accepted canon must be challenged.** Every Sagekin tendency holds at matched height and at matched composition, without forcing separation. Broad, long-torso and Marchfolk-overlap Sagekin are all valid.

**Note for elf W2 (not a Sagekin issue):** W1 Aelari's arm and hand shares and W1 Fenn's forearm do not exceed the authored Sagekin tendencies. Elf W2 should establish elf limb and hand distinction on the complete anatomy, as SG L465 and FN L151 already state.

## 14. Recommendation — ACCEPT

Accept the Sagekin W2E family as built:
- 152 / 163 / 173 / 178 / 181 / 190 / 203 / 208 cm, configuration 1;
- frames;
- composition;
- SG-01…10 dispositions, with SG-04 at ×1.5;
- the 152 cm dependency classification.

The anti-elf rows stay provisional until elf W2.

No Sagekin-only correction is proposed.

**STOP.** Elf W2, Halvren W2, short-race W2, Saurin W2, creator envelopes, facial extremes and UE5 work were not started.
