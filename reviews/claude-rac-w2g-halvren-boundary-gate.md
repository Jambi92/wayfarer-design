# RAC W2G — Halvren Central-Envelope Boundary Gate

**Author:** Claude (auditor) · **Date:** October 8, 2026 · **Order:** `reviews/chatgpt-rac-w2f-final-acceptance-w2g-halvren-order.md` §2–§17
**Author ruling (October 8, 2026; `reviews/chatgpt-rac-w2g-final-acceptance-w2h-short-race-order.md`):** W2G FINAL AUTHOR ACCEPTED / CLOSED — central stature envelope, frame system, composition firewall, mixed-development body system and overall accepted; no redesign. D1 approved (endpoint source-family diagnostic, labeled, not matched height). D2 approved (reading-space expression; HVXAEc diagnostic only). D3 approved with precedence clarification (D3 governs where matched-height allometry contradicts the accepted tendency). HV-49 / HV-50, RM-UB-05, RM-OT-03 remain Wave 3.
**Evidence:** `reviews/rac-w2g-hv-evidence/`. `tables.md` is generated, and every number below comes from `w2g.json`.
**Status:** DESIGN ONLY / NO UE5. NON-CANON diagnostics.
- No Halvren, Marchfolk, Sagekin, Skarn, Fenn, Aelari or Vael canon, body or accepted comparator was changed.
- HVC1 is unchanged and is used only as the diagnostic anchor.
- Probe HVXAEc (§7) is a diagnostic and was **not applied**.

## Verdicts

| Item | Verdict | Reason in one line |
|---|---|---|
| **Halvren central stature envelope** | **CONSTRAIN** | 152–213 cm holds as one coherent family: 54 of 56 source-span rows pass at matched height, with no uniform scaling. The 152 cm exact-plane wrist sits 1.29 % below the human-only span (MF152 / SG152), because no accepted elf body exists at 152 cm. It is inside once the nearest accepted elf bodies (FN157 / VA157) are read (decision **D1**). |
| **Halvren frame system** | **ACCEPT** | 142 / 142 frame checks pass. Breadth moves 7.0–12.0 % while lengths, neck, depth and joints stay within tolerance. Broad is not Skarn (20–23 of 24 readings separate). Narrow is not elf (14–20 / 24). Broad pelvis ×1.12 shows no contradiction. |
| **Halvren composition firewall** | **ACCEPT** | 48 / 48 matched-composition span rows and 16 / 16 invariance rows (6 composition states + HV-36…43, HV-08, HV-09) pass. No body share moves by 1 % under any composition. |
| **Halvren mixed-development body system** | **CONSTRAIN** | The population tests hold: the central family sits as a mosaic inside the source spans, with no exact duplicate of any source (33 / 33). 24 of 30 scored expression tendencies move toward their source. Three items need an author reading: Aelari-influenced neck overshoot, Aelari wrist direction, and three sub-1 % tendencies (decisions **D2**, **D3**). |
| **Halvren W2G overall** | **CONSTRAIN** | No anatomical blocker and no canon challenge. D1–D3 are narrow reading / specification rulings. The route junction is carried as a creator dependency, as in W2F 1C. |

**HV-49 / HV-50 NOT RESOLVED.** No tail limits were set. Ancestry-conditioned tail frequencies, RM-UB-05, RM-OT-03 and genealogy-conditioned reference generation were **not** resolved, estimated or weighted in W2G (§4). The authored tail rules (strictly inside the source outer union; Marchfolk lower-tail, Skarn / Aelari upper-tail contributors; Fenn, Vael and Sagekin do not extend the tails) were not touched.

---

## 1. Construction (§3, §14)

| Stature | Body | Route | Re-solved macro |
|---|---|---|---|
| 152 (HV-11) | HV152 = HV152N-NAT | native short-adult from HVC1 base macro | 0.192 (< 0.40) |
| 163 | HV163 = HV163N-NAT | native | 0.343 (< 0.40) |
| 173 | HV173M | macro re-solved | 0.479 |
| 178 | **HVC1** (W1 anchor, unchanged) | — | 0.543 |
| 181 / 190 / 203 | HV181M / HV190M / HV203M | macro | 0.561 / 0.624 / 0.714 |
| 213 (HV-12) | HV213M | macro | 0.784 |

**Why these statures.** 163, 173, 181, 190 and 203 are the heights where accepted W2 source bodies exist at matched height (§3: no smoothing points). 152 and 213 are the order's boundaries.

**Route check (D, REPORT).** Macro builds at 152 / 163 were kept as checks only. On the macro route, HV152 would have:
- femur / leg 0.4209 against 0.4835 native;
- knee / adjacent segment 0.3424 against 0.2806 native.

That is the generator's short-femur zone, so W2F R2 applies.

**Frames.** Narrow / Broad at 152, 178 and 213, using the accepted W1 Halvren breadth-only rule.

**Composition.** Six states at 173 cm, matched to the Marchfolk / Sagekin / Fenn / Aelari / Vael 173 states.

**Stress.**

| Validator | Body |
|---|---|
| HV-36 | Narrow + muscle |
| HV-37 | Narrow + fat |
| HV-38 | Broad low |
| HV-39 | Broad + muscle |
| HV-40 | Broad + fat |
| HV-41 | 213 + fat |
| HV-42 | 152 + muscle |
| HV-43 | Fenn-influenced + muscle |
| HV-08 | fat |
| HV-09 | muscle |

**Expressions (§7).** Expressions sit at 178 cm, with no uniform scaling anywhere. The `construction.json` manifest records every body. It also keeps the two superseded expression builds:
- **Summed targets:** overshot the source span on forearm.
- **max(HVC1, ½ source):** under-expressed.

## 2. Central stature family and continuity (§3, §14)

**Allometry (U).**
- Head share: 152 > 178 > 213 (0.1356 / 0.1287 / 0.1223), PASS.
- Hand, foot, neck, knee and femoral-breadth trends are reported (RM-UB-02 diagnostic). For example, knee breadth / stature is 0.0727 / 0.0691 / 0.0650.

**Continuity (C).** 39 of 45 series readings are monotonic. The 6 reversals of ≥ 1 % are all classified below. None is unexplained biology.

| Reading | Steps 152→163→173→178→181→190→203→213 | Class |
|---|---|---|
| femur / leg | −0.0 / **−1.4** / +1.4 / +0.8 / +2.1 / +2.6 / +1.7 % | **route junction** (native → macro) |
| shin / leg | +0.0 / **+1.3** / −1.3 / … | route junction (mirror of femur / leg) |
| skeletal pelvic vertical / stature | +0.1 / **+1.1** / −0.9 / … | route junction |
| ankle / adjacent segment | −0.7 / **−1.8** / +0.9 / … | route junction |
| femoral S7 depth / stature | −2.3 / −2.8 / −0.1 / +0.0 / +0.0 / +0.2 / +0.2 % | Monotonic non-increasing to within 0.2 %. The flag comes from the counting rule (most steps are sub-1 % +). The decline at 152–173 cm is native-route robusticity at short stature (relative to the macro range) together with the junction. |
| skeletal shoulder-joint breadth / stature | +0.7 / +1.8 / +0.6 / +0.8 / −1.3 / −2.1 / −2.9 % | **Shared generator macro allometry.** At 181 / 190 / 203 cm, HV reads 0.1974 / 0.1948 / 0.1908 and accepted Marchfolk reads 0.1974 / 0.1948 / 0.1908 — identical. Fenn, Aelari and Sagekin show the same rise-then-fall. The Halvren targets do not touch the shoulder. Not Halvren-specific. |

**Route junction.**
- It lies between HV163 (native, macro 0.34) and HV173 (macro 0.48), with magnitude 1.1–1.8 % on four readings.
- It is the same class W2F 1C accepted.
- **Carried dependency:** a future continuous creator must interpolate across the native ↔ macro junction (no visible pop). The junction is construction, not Halvren biology.
- Nothing here is dismissed as "generator" without the matching family comparison (§14).

## 3. Matched-height source comparisons (§5)

O rows are the accepted W1 Halvren "within source span (MF, SG, FN, AE, VA)" rows: torso, leg, arm, forearm / arm, shin / leg, thorax depth, finger / hand, and wrist (exact plane). They are read against the **accepted W2 families at matched height**:
- 152 cm: MF152 / SG152 (no elf reaches 152);
- 163 cm: MF163 / SG163 / FN163 / VA163;
- 173–203 cm: all five.

| Height | Scored rows | Result | Positions in the span (0 = min, 1 = max) |
|---|---|---|---|
| 152 | 8 | 6 PASS, **1 MARGINAL**, **1 FAIL** | torso 0.40, leg 0.61, arm 0.57, forearm 0.72, shin **1.03**, thorax depth 0.70, finger 0.52, wrist **−0.43** |
| 163 | 8 | 8 PASS | 0.01–0.81 |
| 173 | 8 | 8 PASS | 0.25–0.91 |
| 178 (HVC1) | 8 | 8 PASS | torso 0.74, leg 0.24, arm 0.25, forearm 0.67, shin 0.26, thorax depth 0.56, finger 0.37, wrist 0.66 |
| 181 / 190 / 203 | 24 | 24 PASS | the 178 pattern ± 0.06 |

**Not an average (§2, §5).** Halvren sits on the human side for limb shares (0.24–0.25) and on the elf side for torso (0.73–0.74), forearm (0.61–0.91) and wrist (0.64–0.67). It is a mosaic, not a 50 / 50 midpoint and not one copied source.

**152 cm items.**

| Reading | HV152 | MF152 | SG152 | Result |
|---|---|---|---|---|
| shin / leg | 0.5165 | 0.5163 | 0.5101 | MARGINAL: 0.04 % above MF152, i.e. equal to Marchfolk |
| exact-plane wrist / forearm | 0.2004 | 0.2091 | 0.2030 | **FAIL: −1.29 %** |

- The Halvren wrist is an inherited elf gracility: HVC1 carries the W1 wrist-circumference decrease. At 178 cm, HVC1 (0.1919) is already below both humans (MF178 0.2014, SG178 0.1943) and is inside only because FN178 / AE178 are in the span.
- At 152 cm no accepted elf body exists, because the elf floor is 157 cm.
- Read against MF152 / SG152 plus the nearest accepted elf bodies FN157 / VA157 (report span), **all 24 body readings at 152 are inside**. The wrist sits at position 0.69.
- → **D1.**

**Other report rows.**
- Non-canon body readings at matched height: 10 lie outside a matched span, all by < 1.3 %. These are 152 cm elbow, ankle and pelvic readings (inside with FN157 / VA157), 163 foot −0.37 %, and 173 / 178 knee −0.12 to −0.29 %.
- **213 cm** has no matched source above 211. Read against MF203 / SG208 / FN211 / AE211 (report), all 8 W1 rows are inside (positions 0.04–0.67).

**G rows (REPORT).** These are the accepted W1 rows at the **fixed W1 reference statures**. 21 bodies show at least one row outside: HV152 / 203 / 213, their frames, composition states, and the stress and expression bodies. Under the accepted boundary-stature rule, matched-height comparisons govern. The central-body G misses read at matched height as follows:
- HV152 thorax depth, HV203 shin: inside the matched span (O).
- HV152 wrist: D1.
- HV213 leg / forearm: inside the 203–211 cm report span.

Composition G misses are inside the matched-composition span (M).

## 4. Source-passing / neutralization (§6)

The test reads the 24 body readings only:
- skin shares: torso, leg, arm, span, forearm, shin, neck, hand, finger, palm, foot, thorax breadth and depth;
- exact-plane joints (four);
- skeletal readings: thoracic breadth and depth, shoulder joint, crest, AP pelvic depth, pelvic vertical, waist interval.

It uses neutral composition and excludes face, ears, pigmentation, hair, clothing and equipment. **Failure = systematic exact duplication** (fewer than 2 readings separating by ≥ 1 %).

| vs | 152 | 163 | 173 | 178 | 181 | 190 | 203 |
|---|---|---|---|---|---|---|---|
| Marchfolk | 10 | 9 | 10 | 11 | 10 | 8 | 8 |
| Sagekin | 10 | 17 | 10 | 11 | 10 | 10 | 10 |
| Fenn | — | 21 | 20 | 20 | 20 | 20 | 20 |
| Aelari | — | — | 21 | 19 | 19 | 18 | 18 |
| Vael | — | 10 | 10 | 11 | 11 | 10 | 10 |
| Skarn | — | — | — | — | — | 22 | 22 |

- **33 / 33 PASS.** 213 vs SK208 separates on 22 readings (report).
- Halvren is closest to Marchfolk at the top of the envelope: 8 / 24 readings at 190–203 cm. That is a resemblance the canon allows (HV-04), not a duplication.

## 5. Limbs and exact-plane joints (§8)

**Joint breadth relative to the adjacent segment (exact plane).** All values are inside the 178 cm source span of MF / SG / FN / AE / VA / SK183, which runs elbow 0.3185–0.3909, wrist 0.1736–0.2686, knee 0.2419–0.3655, ankle 0.2580–0.3197:

| Body | elbow | wrist | knee | ankle |
|---|---|---|---|---|
| HVC1 | 0.3435 | 0.1919 | 0.2657 | 0.2706 |
| Fenn-influenced | 0.3452 | 0.1857 | 0.2600 | 0.2651 |
| Aelari-influenced | 0.3383 | 0.1861 | 0.2591 | 0.2632 |
| Vael-influenced | 0.3421 | 0.1949 | 0.2640 | 0.2767 |
| Skarn-influenced | 0.3547 | 0.2177 | 0.2940 | 0.2899 |
| Sagekin-influenced | 0.3438 | 0.1912 | 0.2622 | 0.2706 |
| Marchfolk-influenced | 0.3425 | 0.1965 | 0.2646 | 0.2757 |
| HV-43 gracile + muscle | 0.3289 | 0.1820 | 0.2613 | 0.2644 |

- No gracile segment connects through a massive joint, and no joint is driven by one global "robustness" control.
- The Skarn-influenced joints rise 7–13 % while staying 18–40 % below Skarn.
- The Fenn-influenced joints fall 2–3 % with their segments.
- Absolute joint scale (breadth / stature) and long-bone S7 breadth are in `w2g.json`.

## 6. Thorax, pelvis and axial body (§9)

- **Axial / pelvic readings (A, REPORT): 80 of 91 sit inside the matched source span.**
  - Four at 152 cm are outside by ≤ 0.31 %, and all are inside with FN157 / VA157.
  - Two at 163 cm are outside by ≤ 0.28 %.
  - Five at 173–203 cm sit on the span edge by ≤ 0.02 %. Bitrochanteric / crest is the narrowest-in-family value, equal to a source.
- The pelvic readings sit at different span positions: crest 0.92, AP depth 0.23, vertical 0.53 at 152 cm with elves. The pelvis behaves as its own mixed structure, not as a linear human-to-elf morph.
- No obstetric anatomy was modelled. No sex-related pelvic biology was invented. **Surfaced dependency:** detailed mixed pelvic inheritance needs sex-specific source pelvic biology, which still does not exist. That belongs to the genealogy / sex-variation work, not W2G.

## 7. Frames (§10)

| Check | Result |
|---|---|
| Narrow / Broad moves thoracic breadth, shoulder-joint, biacromial, crest and hip-joint spacing at 152 / 178 / 213 | 30 / 30 PASS; magnitude 6.98–12.0 % |
| Lengths, neck, HH, hand, thoracic depth and four joints kept | PASS (≤ 0.5 % / 1 %) |
| Broad pelvis ×1.12 carries the hip joints with the crest | bitrochanteric / crest −0.17 to −0.23 % (Broad), +1.67 to +1.69 % (Narrow): PASS (2 %) |
| Broad is not Skarn | HVB178 vs SK183: 23 / 24; HVB213 vs SK208: 23; vs SKB208: 20 |
| Narrow is not elf | HVN178 vs FN178: 20; AE178: 19; VA178: 14 |
| Narrow / Broad 178 inside the source span | 16 / 16 PASS (positions identical to HVC1 except Broad thorax depth 0.60) |

- Broad Halvren thoracic breadth equals Broad Skarn: HVB213 0.1696 against SKB208 0.1681. Thoracic depth (0.1095 against 0.1340) and joints (knee 0.2264 against 0.3090) stay Halvren. Breadth carries frame; depth and joints carry ancestry. That is the canon rule.
- No contradiction to ×1.12 was found.

## 8. Composition (§11)

- **Firewall: 48 / 48** matched-composition span rows pass. These are the HV173 states against the same-composition MF / SG173 / FN173 / AE173 / VA173 states.
- **Invariance:** 6 composition states and 10 stress bodies change no share by ≥ 1 %.
- Render: `sheets/hv_composition_173.jpg`, `hv_stress_36_43.jpg`.

## 9. Named body validators (§12)

| Validator | Body evidence | Result | Out of scope |
|---|---|---|---|
| HV-01 strong human | HVXMF (HVC1 targets ×0.5) inside the span; not a Marchfolk duplicate (4 / 24: wrist −2.4 %, ankle …) | PASS (body), **close by design** | face, ears |
| HV-02 strong elven | HVXFN / HVXAE / HVXVA not duplicates of FN178 / AE178 / VA178 (19 / 18 / 11) | PASS (body) | face, ears |
| HV-03 broad mixed | HVC1 mosaic positions 0.24–0.91 (§3) | PASS | face, ears |
| HV-04 subtle | HVC1 vs MF178 11 / 24, vs SG178 11 / 24 | PASS (allowed resemblance) | face, ears |
| HV-07 Broad | breadth +7–12 %, not Skarn | PASS | — |
| HV-08 higher fat | invariance | PASS | — |
| HV-09 high muscle | invariance; the skeleton keeps its Skarn separation (22 / 24 at 190 / 203) | PASS | — |
| HV-11 152 cm | §3 | MARGINAL + FAIL → **D1** | face, hands / feet equipment, world |
| HV-12 213 cm | §3 (report against 203–211 sources) | PASS (report) | same |
| HV-13…17 body portions | §10 | see §10 | face, ears, pigmentation, culture |
| HV-36…43 | invariance 10 / 10; HV-43 joints coherent (§5) | PASS | — |

Face, ear, pigmentation, lifecycle, cultural, equipment and genealogy portions are **OUT OF CURRENT SCOPE**. No new validators were created.

## 10. Source-influenced expression (§7; HV-13…17 body portions)

**Construction.** On the systems the Halvren canon names for each influence, HVC1's targets move halfway toward the source population's own targets. This is builder-chosen and diagnostic, not ancestry percentages or subtypes. No source body was copied, and no other slider was weakened.

**Tendency test.** Does the expression move from HVC1 *toward the matched source* on each named reading, by ≥ 1 %?
- PASS if it does, short of passing the source;
- OVERSHOOT if it passes the source;
- NOT DEMONSTRATED if the move is < 1 %;
- FAIL if it moves away by ≥ 1 %;
- REPORT if the source is within 1 % of HVC1 (nothing to express).

| Influence | Scored | PASS | Other | Inside 178 span (8 W1 rows) | vs source duplicate |
|---|---|---|---|---|---|
| Fenn (HV-13) | 8 | **8**: shin, hand, finger, foot, wrist, knee, ankle, thorax depth (0.24–0.63 of the gap) | forearm REPORT (gap 0.7 %) | 7 PASS, forearm **MARGINAL** (−0.20 %, at FN178 edge) | 19 / 24 |
| Aelari (HV-14) | 7 | 3: thorax depth, knee, ankle | neck share **OVERSHOOT** (+6.6 % vs gap +4.2 %); neck / torso **OVERSHOOT**; shin NOT DEMONSTRATED; wrist **FAIL** (−3.0 %, source +2.4 %); arm / leg / forearm REPORT (gaps < 1 %) | 7 PASS, forearm **MARGINAL** (−0.10 %) | 18 / 24 |
| Vael (HV-15) | 4 | 3: thorax depth, skeletal thoracic depth, hand | palm breadth NOT DEMONSTRATED (+0.4 % of +2.8 %) | 8 PASS | 11 / 24 |
| Skarn (HV-16) | 8 | **8**: thorax depth (both), shoulder joint, torso, knee, wrist, ankle, hand (0.24–0.64 of the gap) | — | 8 PASS (span incl. SK183) | 24 / 24 |
| Sagekin (HV-17) | 3 | 2: finger, thorax depth | shin NOT DEMONSTRATED (−0.65 % of −1.23 %); leg / torso / forearm REPORT | 8 PASS | 8 / 24 |
| Marchfolk | — | — | broad distribution, no named direction | 8 PASS | 4 / 24 |

**Totals.** 30 scored tendencies:
- **24 PASS**, 2 OVERSHOOT, 3 NOT DEMONSTRATED, 1 FAIL;
- 8 REPORT;
- spans 46 PASS / 2 MARGINAL;
- duplicates 6 / 6 PASS.

**The non-pass items.**

1. **Aelari neck overshoot.**
   - Half of the Aelari neck-height target (0.30) moves neck share +6.6 %, past matched AE178. AE178 is a re-solved 190 cm reference whose neck share falls with stature.
   - **Probe HVXAEc (not applied):** neck 0.10, wrist kept, upper leg 0.06.
     - Neck / torso +1.29 % (PASS, 0.23 of the gap).
     - Neck share +0.99 % (just under 1 %).
     - Knee and ankle 0.82 / 0.95 of the gap.
     - All W1 rows inside the span; 19 / 24 separate from AE178.
   - The overshoot is a target-space specification artifact. The direction is correct. → **D2.**
2. **Aelari wrist FAIL.**
   - HVXAE becomes *more* gracile at the wrist (−3.0 %). This is the canon-named Aelari "gracility" direction.
   - Matched AE178's exact-plane wrist / forearm is *larger* than HVC1's (0.1964 against 0.1919), because AE178 is re-solved from the 190 cm reference.
   - So the canon tendency and the matched-height reading disagree. That is a reference-state relation of the W2F R1 kind, not a Halvren defect. → **D3.**
3. **Three sub-1 % tendencies.**
   - Aelari shin / leg: the canon says "even limb elongation", which leaves shin / leg flat, so this is consistent.
   - Vael palm breadth: weak generator finger-distance response.
   - Sagekin shin: a half-gap of a 1.23 % gap is < 1 % by construction.
   - All three move in the right direction, or are canon-consistent. → **D3.**
4. **Forearm MARGINAL.**
   - HVC1 already sits at forearm position 0.67, and FN178 is the span maximum.
   - Fenn and Aelari influence push it 0.10–0.20 % past FN178. That is AD-G10 MARGINAL, accepted class.

## 11. Route and generator limitations (§14)

- **Native ↔ macro junction** between 163 and 173 cm (1.1–1.8 %, four readings). Carried: creator interpolation, no visible pop (W2F 1C class).
- **Shared macro shoulder allometry** above 181 cm. This is identical in Marchfolk, so it is not Halvren biology.
- **Generator target-to-reading non-linearity** in expressions (neck height, palm breadth). → D2.
- **Wrist / forearm ratio and absolute wrist** do not move together under forearm-length targets (Aelari). → D3.
- Hidden-ear craniofacial separation: **NOT DEMONSTRATED** (W1, source-method limitation), preserved. Orbit-breadth: no verdict. Accepted ankle MARGINAL: preserved. Eye-scale target: removed. Nothing craniofacial was exaggerated (§13).

## 12. Complete non-pass list (§15.13)

**Scored:**
- O 152 shin MARGINAL;
- O 152 wrist **FAIL**;
- X HVXFN forearm MARGINAL;
- X HVXAE forearm MARGINAL;
- X HVXAE neck share OVERSHOOT;
- X HVXAE neck / torso OVERSHOOT;
- X HVXAE shin NOT DEMONSTRATED;
- X HVXAE wrist **FAIL**;
- X HVXVA palm NOT DEMONSTRATED;
- X HVXSG shin NOT DEMONSTRATED;
- C 6 NON-MONOTONIC (all classified, §2).

**NOT RUN:** X W1 panel HVH3 / HVE3 exact-plane wrist (W1 panel bodies have no joint sections; report).

**REPORT only:**
- O 144;
- A 91;
- K 24 (Halvren below Skarn on every guard reading except Broad thoracic breadth, §7);
- U 12;
- D 12;
- G 21 bodies NOT ALL PASS at fixed W1 references;
- X 42 + probe;
- P 1.

## 13. Author decisions requested (narrow)

- **D1 — HV-11 reading at 152 cm.** Read the 152 cm Halvren source-plausible rows against MF152 / SG152 **plus the nearest accepted elf bodies FN157 / VA157** (the elf floor), since no elf exists at 152 cm. Recommended. Halvren's elf-derived wrist gracility otherwise cannot fit a human-only span. All 24 body readings are inside on this reading.
- **D2 — Expression specification space.** Source-influenced Halvren tendencies are specified and validated **in reading space, bounded by the matched source** (move toward, not past), not as generator-target fractions. Recommended. Evidence: the Aelari neck overshoot and the bounded probe HVXAEc. Specification only; HVXAEc is not applied.
- **D3 — Reference-state tendencies.** Where the canon-named tendency and the matched-source reading disagree (Aelari wrist gracility), or the gap is < 2 % so a half move is < 1 % (Sagekin shin, Vael palm, Aelari shin under "even elongation"), read them under the W2F R1 reference-state rule. Recommended. They are not mandatory ≥ 1 % separations.

## 14. Canon challenge

**No accepted Halvren or source-population canon is genuinely challenged.**
- The 152 cm wrist item is a matched-height availability gap (no elf at 152), not a contradiction of the W1 source-plausible row.
- The expression items concern how tendencies are specified and read, not the tendencies themselves.
- The route junction and shoulder allometry are construction / shared-generator effects, demonstrated by comparison.

## 15. Wave 3 information identified (not resolved)

These facts are for Wave 3. No limit, weight or frequency was set.
- At 213 cm the central body sits inside MF203 / SG208 / FN211 / AE211 on all 8 W1 rows, and separates from SK208 on 22 / 24 readings.
- At 152 cm it sits on Marchfolk for shin / leg (0.04 %).

Both are starting facts for HV-49 / HV-50 tests (H-3: tails vs matched-stature Marchfolk / Skarn / Aelari).

---

**STOP.** Short-race W2, Saurin W2, Wave 3 genealogy references, HV-49 / HV-50 limits, RM-UB-05 / RM-OT-03, creator envelopes and UE5 were not begun. This gate goes to the author for review.
