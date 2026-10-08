# RAC W2D — Gorrund W2 Author-Acceptance Gate

**Author:** Claude (auditor) · **Date:** October 8, 2026 · **Order:** `reviews/chatgpt-rac-final-grask-w2-acceptance-gorrund-w2-order.md` §4–§5
**Author ruling (October 8, 2026; reviews/chatgpt-rac-w2d-gorrund-final-acceptance-w2e-sagekin-order.md):** ACCEPT — Gorrund W2 FINAL AUTHOR ACCEPTED / CLOSED. R1 accept current Broad (headroom diagnostic, not a maximum); R2 option (a) (GOR-BODY-14 bound by ALPC-5 depth vs Marchfolk; AD-G7 vs Skarn is a population direction); R3 joint presence = joint / adjacent bone, per-stature elbow report-only, no correction; R4 218 cm palm depth = generator-route dip, no correction. AD-3 CLOSED; Grask 198 vs Gorrund NOT APPLICABLE. Residual list (§9) is the closure record.
**Evidence:** `reviews/rac-w2d-go-evidence/` (`tables.md` is generated; every number below is from `w2d.json`, `probes.json`, `search_ad3.json`)
**Status:** DESIGN ONLY / NO UE5. NON-CANON diagnostics. No canon was rewritten, and no Skarn or Grask body was changed. Every comparator is the accepted body, with the W2C1 knee reverts applied (Skarn 229 configuration 1 = original W2B body; Marchfolk 203 configuration 1 = uncorrected body).

**Recommendation: CONSTRAIN.** The Gorrund family from 208 to 251 cm holds every stature-matched identity relation against Grask and Skarn, plus AD-1, ALPC-7, composition and AD-3. Four author rulings are needed, all Gorrund-only:
- **R1:** how wide Broad may go at the thorax;
- **R2:** which reading defines GOR-BODY-14;
- **R3:** elbow-per-stature against Broad Grask;
- **R4:** palm depth at 218 cm.

None of the four needs a Skarn or Grask workaround. **AD-3: recommend CLOSE.**

---

## 1. Body / construction manifest

**Route.** The accepted W1i/W1j Gorrund route (AD-G14), run at each height macro with no uniform scaling:
- Skeleton: minimum-composition build plus the accepted 16-parameter bone scales and trunk sculpt.
- Envelope: tissue donor at the same macro (`w2d_drivers/go_body.py`).

**Reference reproduction.** GOREF reproduces the accepted Gorrund exactly at 230.9 cm (macro 0.8369140625), on both skin and skeletal proxy, with 0 non-PASS skeletal rows.

| Body | Role | Height macro | Stature (cm) |
|---|---|---|---|
| GO208 | GOR-BODY-02, minimum | 0.685 | 208.3 |
| GO218 | overlap 218 | 0.7503 | 218.0 |
| GO229 | overlap 229 | 0.8241 | 229.0 |
| GOREF | GOR-BODY-01, accepted reference | 0.8369 | 230.9 |
| GO239 | overlap 239 | 0.8913 | 239.0 |
| GO251 | GOR-BODY-03, maximum | 0.9718 | 251.0 |
| GON5 / GON5_218 | GOR-BODY-04 Narrow (and GOR-BODY-12 magnitude) | ref / 0.7503 | 230.9 / 218.0 |
| GOB7 / GOB7_218 | GOR-BODY-05 Broad | ref / 0.7503 | 230.9 / 218.0 |
| GOD14_9 / GOD14_9_218 | GOR-BODY-14, lower thoracic depth | ref / 0.7503 | 230.9 / 218.0 |
| GOLP218 | AD-3 limb-present family | 0.7503 (3 limb/torso targets removed) | 217.1 |
| GOR-BODY-06…11, 16 | composition on the reference skeleton (plus 06/07/09/10/16 at 208 and 218 cm) | — | — |

**Frame writes** (cfg `tools/rac/w1/cfg/w2d/GO-boundary.json`):

- **Narrow:**
  - clavicle ×0.95;
  - rib-cage bone X ×0.95;
  - pelvis X ×0.98, with the femur cross-section following at ×0.98;
  - trunk-breadth sculpt ×0.95 upper / ×0.98 pelvic.
- **Broad:**
  - clavicle ×1.015;
  - pelvis X ×1.05, with the femur following at ×1.05;
  - pelvic-level sculpt ×1.05;
  - thorax unchanged.

Eleven other frame probes and thirteen named-extreme probes are listed with their failing rows in `probes.json`. Two of those probes were run on the wrong axis and are kept and labeled: GOX14 scales spine_03 Y, which is upper-thorax length, not depth.

**No 198 cm Gorrund was built.** The authored minimum is about 208 cm (GO L29).

## 2. Stature / allometry (208 → 251 cm)

| Reading | 208 | 218 | 229 | 230.9 | 239 | 251 |
|---|---|---|---|---|---|---|
| torso / stature | 0.3039 | 0.3024 | 0.3006 | 0.3004 | 0.2993 | 0.2979 |
| leg / stature | 0.5171 | 0.5207 | 0.5248 | 0.5254 | 0.5280 | 0.5314 |
| arm / stature | 0.3689 | 0.3707 | 0.3727 | 0.3730 | 0.3743 | 0.3759 |
| head / stature | 0.1189 | 0.1175 | 0.1160 | 0.1158 | 0.1148 | 0.1130 |
| skeletal thoracic breadth / stature (t=0) | 0.1840 | 0.1812 | 0.1778 | 0.1773 | 0.1754 | 0.1727 |
| skeletal thoracic depth / stature (t=0) | 0.1549 | 0.1505 | 0.1482 | 0.1477 | 0.1448 | 0.1426 |
| knee section / stature | 0.0780 | 0.0745 | 0.0718 | 0.0716 | 0.0728 | 0.0712 |

**What holds:**
- Head allometry holds: 208 > 229 > 251.
- 43 of 46 continuity rows are monotonic.
- Every body passes all 35 skeletal Gorrund rows except the fixed-reference items in §9.
- Proportions shift smoothly: legs and arms lengthen slightly with stature, and torso and breadth shares fall. That is the generator's allometry, not uniform scaling.
- The renders (`sheets/go_statures_208_to_251.jpg`) read adult at 208 cm and coherent at 251 cm. There is no tiny head and no giant-human scaling.

**Three reversals of at least 1 %**, all generator route effects. No body was redesigned for them.
- Shoulder-joint / thoracic breadth drops 2.3 % at the 218→229 step.
- Thoracic depth / breadth drops 1.3 % and then 1.0 %.
- Knee section rises 1.5 % at 239 cm.

**Fixed-reference W1 rows at the boundaries** are classified by the boundary-stature rule (§9).

## 3. Matched-height Grask and Skarn comparisons

### Gorrund vs Grask at 208 / 218 / 229 / 239 cm

**76 / 76 PASS.** Rows tested at each height:
- torso share greater;
- leg, arm and span shares lower;
- forearm and lower-leg emphasis lower;
- skeletal thoracic breadth, depth, girdle breadth and depth/breadth greater;
- pelvic vertical ≥ Grask;
- exact-plane joints, each per adjacent bone (RAC-05 metric) and per stature.

The thinnest margin is elbow / stature, at +1.3 % (239 cm) to +1.9 % (208 cm). Grask keeps its limb and reach contribution at every height:
- arm share −5 % to −13 % for Gorrund;
- span lower for Gorrund at every height.

### Gorrund vs Skarn at 208 / 218 / 229 cm

**12 / 12 PASS** on the authored architecture rows:
- skeletal thoracic depth / stature;
- thoracic breadth / stature;
- depth / breadth;
- skin thoracic breadth.

The thinnest margin is +2.6 %.

**Report only (AD-4: proportional separation undetermined):**
- torso share +2.7 % to +3.1 % for Gorrund;
- arm share −7.8 % to −8.3 %;
- girdle breadth +4 %;
- the ALPC ratios are all higher for Gorrund (+3 % to +19 %).

**Observation, not a canon item:** Skarn knees and ankles are larger than Gorrund's, both per stature (knee −1.8 % to −9.1 %, ankle −7.7 % to −8.0 %) and per adjacent bone (knee −4.8 % to −11.1 %). Canon leaves Skarn vs Gorrund joint scale n.d. (large-race review L61). Gorrund elbows and wrists per adjacent bone exceed Skarn's (+4 % to +6 %).

## 4. Broad Skarn vs Gorrund (AD-1, ALPC-7, RM-LR-03)

**45 / 45 PASS.** Rows tested:
- Gorrund 208 vs Broad Skarn at 208, 218 and 229 cm: thoracic depth / stature, depth / breadth, and all 7 ALPC-7 ratios. The thinnest is crest / thorax at +2.1 % against Broad Skarn 229.
- The equal-height ALPC-7 pairs at 218 and 229 cm.

**Breadth inflation was not needed.** Gorrund thoracic breadth exceeds Broad Skarn's (+9.9 % at 208, report only), but no row depends on it.

**RM-LR-03 / LR-04** (low-breadth GOR-BODY-12 and low-depth GOR-BODY-14 vs Broad Skarn 229): ALPC-7 and depth / stature all PASS. Thoracic breadth and joints are report-only, because breadth may invert under LR-04.

**Craniofacial and ear carriers of AD-1: NOT RUN** (body-only measurement scope).

## 5. Exact-plane joints (every newly scored joint row)

All new joint rows use exact-plane sections (`joint_sections.json`; REFERENCE_ANATOMY_V1 §10). Each joint is read both per adjacent bone (RAC-05 L32, the W1 metric) and per stature.

**Gorrund vs Grask, matched height:** 32 / 32 PASS, every row ≥ 1 %.

**Gorrund vs Broad Grask 218** (frames and AD-3 reciprocal):
- Per adjacent bone: all PASS.
- Per stature: knee, ankle and wrist PASS. **Elbow / stature FAILs** (0.0467 vs 0.0470, −0.68 %) for all three Gorrund 218 bodies, because they share one elbow. → **R3**.

**Within the Gorrund family:**
- Narrow keeps joint scale within 1 %: knee −0.8 %, the rest 0.0 %.
- Broad leaves the upper-limb joints unchanged; the femur follow raises the knee 2 %.

**Not built:** no Gorrund-wide joint allometry rule was derived. The knee trend is non-monotonic (§2).

## 6. Narrow / Balanced / Broad frames

### Narrow (GON5)

**Changes:**
- thorax −7.4 %;
- girdle −7.1 %;
- biacromial −5.6 %;
- crest −2.4 %;
- hip-joint spacing −2.0 %.

**Unchanged:**
- lengths and stature (0.00 %);
- depth (−0.03 %);
- joints.

All skeletal rows PASS at the reference, and Narrow beats Balanced Grask and Narrow Grask at 218 cm on every row.

**Pelvic limit:** Narrow pelvic narrowing is capped by GO-P2b, which keeps hip joints under the load path.
- Pelvis ×0.95 without femur follow FAILs.
- Pelvis ×0.98 without follow FAILs.
- Pelvis ×0.98 with femur follow ×0.98 PASSES.

**Breadth floor:** the upper-trunk breadth floor lies between ×0.95 (PASS) and ×0.935. At ×0.935, RM-LR-02a is NOT DEMONSTRATED and GO-P2b is T-SENSITIVE. GOR-BODY-12 is therefore the Narrow magnitude.

### Broad (GOB7)

**Changes:**
- girdle +1.4 %;
- biacromial +1.3 %;
- crest +5.0 %;
- hip-joint spacing +5.0 %;
- thorax +0.15 %.

**Unchanged:** lengths and depth. All skeletal rows PASS.

**Not a collapse into another body type:**
- vs Broad Skarn 229: ALPC-7 and depth all PASS.
- vs Broad (thick) Grask 218: all rows PASS except the R3 elbow / stature row.
- vs Marchfolk 203: depth, depth / breadth and ALPC-1 all PASS.

**Why Broad cannot widen the thorax more (→ R1).** The reference sits only 2.3 % above the AD-G7 bound (depth / breadth > Skarn). Any Broad thorax widening without depth therefore loses the bound quickly:

| Probe | Thorax change | Result |
|---|---|---|
| GOB5 | +1 % | AD-G7 NOT DEMONSTRATED |
| GOB4 | +1.5 % | AD-G7 FAIL, ALPC-1b T-SENSITIVE |
| GOB / GOBF | +5 % | ALPC-1b FAIL, AD-G7 FAIL |
| GOB3 / GOB6 | clavicle above ×1.025 | ALPC-4 FAIL / T-SENSITIVE |

Canon allows Broad to "increase thoracic, shoulder and pelvic breadth within valid relationships" and forbids hard-linking Broad to maximum depth (GO L245). Broad Gorrund therefore widens mainly through the pelvis.

### At 218 cm

The frames reproduce the same moves. Narrow 218 inherits the fixed-reference GO-P2b drift (§9).

## 7. Composition

- **Invariance:** 17 / 17 composition states keep torso, leg, arm, span, forearm and lower-leg shares within 1 % of their skeleton body (reference, 208 and 218 cm). The skeleton is shared by construction, so every skeletal row is unchanged.
- **Same composition at matched height:** 40 / 40 PASS. Thinnest margin +7.4 %. Pairings:
  - Gorrund 208 vs Skarn 208 in the low-muscle, high-muscle, higher-fat, high-both and 0.25 / 0.25 states: skin thoracic depth and breadth.
  - Gorrund 218 vs Grask 218 in the same states: depth, breadth, torso, leg, arm and span.
- **Low composition keeps the massiveness:** 0.25 / 0.25 Gorrund and low-muscle Gorrund keep every directional relation, so high composition is not the source of identity.
- **ALPC-6 skin half at matched low composition:**
  - reference: 5 FAIL, the same as the accepted W1 residual;
  - 218 cm: the same 5 FAIL;
  - 208 cm: 1 FAIL (pelvic AP / thoracic depth).
- **Not used as identity tests:** composition-state skin rows against neutral-composition comparators are report-only. Composition was not used to repair anything.

## 8. AD-3 resolution — recommend CLOSE

**AD-3 (a):** at matched height, the limb-present Gorrund family stays below the shortest-limbed valid Grask (GR-BODY-10, 218 cm) in relative limb contribution.

| Body vs GR-BODY-10 | leg | arm | span | torso |
|---|---|---|---|---|
| limb-present GOLP218 | −5.0 % | −7.0 % | −1.9 % | +8.2 % |
| central GO218 | −5.4 % | −13.0 % | −6.9 % | +9.1 % |

**The span margin is a real ceiling, not a search gap.** Proportion probes (`search_ad3.json`) bracket the family:
- Removing the finger target too (GOL000) gives span −0.6 % but fails both palm rows.
- Arm increases of +0.2 / +0.4 (GOLB, GOLC, GOLX) push span to between +0.5 % and +3.5 %. At those values the Gorrund's own canonical rows fail: "span < GR" (NOT DEMONSTRATED or FAIL), plus elbow joint scale > Grask.

So the AD-3 floor is enforced from the Gorrund side by the Gorrund rows themselves.

**Reciprocal test:** GOR-BODY-12 and GOR-BODY-14 at 218 cm vs Broad Grask 218. Limb, axial, depth and joint-per-bone rows all PASS. The only failures are the elbow / stature rows (R3).

**Grask 198 vs Gorrund:** outside the real overlap, because no Gorrund exists below 208 cm. This is classified as NOT APPLICABLE under the overlap rule. It is not a NOT DEMONSTRATED result.

## 9. Every non-PASS / NOT RUN / generator-limit item

| # | Item | Class | Notes |
|---|---|---|---|
| 1 | Broad thorax limited to about +1 % (AD-G7 / ALPC-4 / ALPC-1b) | Constraint → **R1** | probes GOB, GOBF, GOB3–6 |
| 2 | GOR-BODY-14 at depth sculpt ×0.90: AD-G7 depth / breadth > Skarn **FAIL** (0.7611 vs 0.8156 at t=0; −6.7 %) | → **R2** | ALPC-0…4 and every depth row vs Marchfolk, Grask and Skarn-depth / stature pass. If AD-G7 vs Skarn binds GOR-BODY-14, the valid lower-depth domain is under 2 % (×0.98 already FAILs). GO L759 asks only "depth criteria … at least against MF". |
| 3 | Elbow / stature vs Broad Grask 218: **FAIL** −0.68 % (3 rows) | → **R3** | per-bone metric passes |
| 4 | Palm depth / hand > Marchfolk at 218 cm: **FAIL** (0.1812 vs 0.1846, −1.8 %) on all 218 cm bodies; GOLP218 NOT DEMONSTRATED | → **R4** | passes at 208 (0.1865) and 229 (0.1876); a generator dip at macro 0.7503 |
| 5 | GO-P2b bitrochanteric / crest ≈ MF at 208 cm | Fixed-reference drift, REPORT | about +0.012 vs ±0.010 tolerance (t-sweep 1.2044 / 1.2110 / 1.2180 vs Marchfolk 173). The largest Marchfolk (203) reads lower, 1.1842, so no matched human closes it. |
| 6 | GO-P2b on Narrow 218 (and GON3_218 / GON4_218) | FAIL, fixed-reference drift | the Narrow reference body passes |
| 7 | ALPC-4 on Narrow 218 | T-SENSITIVE | 1.2501 vs 1.2493 at t=0.5 |
| 8 | GO-P3 pelvic vertical ≥ Grask at 251 cm, vs central Grask | MARGINAL (0.0505 vs 0.0508) | vs tallest Grask (239): +2.1 % PASS, report |
| 9 | Skin thoracic breadth > Skarn 208 (W1 fixed reference) | GO239 NOT DEMONSTRATED, GO251 FAIL (−1.7 %); also GON5 / GON3 / GON4 skin | vs Skarn 229: +7.2 % / +5.3 %; matched 208 / 218 / 229 PASS |
| 10 | Skin-layer ALPC rows on frames | GON5 / GOB7: ALPC-2b crest / lumbar ≤ MF FAIL; ALPC-4 skin MARGINAL | skeletal rows govern (AD-G14) |
| 11 | GO208 skin ALPC-7 pelvic AP / thoracic depth > Skarn central | FAIL | skeletal ALPC-7 vs Broad Skarn passes |
| 12 | Five skin pelvic rows shared with the accepted reference | as W1 | PV-D14 ×2, GO-P2b skin, ALPC-2a / 2b skin |
| 13 | ALPC-6 skin residuals | 5 / 5 / 1 FAIL | see §7 |
| 14 | GOLP218 ALPC-1b | T-SENSITIVE | 0.9855 vs 0.9867 at t=0.5 |
| 15 | Continuity reversals (S1 / S2, depth / breadth, knee) | NON-MONOTONIC | generator route, §2 |
| 16 | NOT RUN items | NOT RUN | craniofacial / ear carriers (AD-1); GO-P2a; ALPC-3 skin; ALPC-8 (Durrim); GOR-BODY-13 / 15 / 17 / 18; ALPC-5 as an automated row (its content is covered by the canonical rows on GON5 / GOD14_9). Gorrund has no 198 cm body by canon. |
| 17 | Generator limits | limit | pelvic narrowing moves the hip joints out unless the femur follows; the thorax depth / breadth headroom at the reference is 2.3 % |

## 10. Canon challenge statement

**No accepted canon must be challenged.** Everything above is a stature-matched pass, a generator limit, or a fixed-reference drift that the boundary rule already handles.

**Clarifications needed:**
- **R2:** whether GO-G7 / AD-G7 (depth / breadth > Skarn) binds the lower-depth named extreme.
- **R3:** whether "joint presence" vs Broad Grask is read per adjacent bone (RAC-05, the W1 metric) or per stature.

**Observation for the record, not a challenge:** Skarn knees and ankles exceed Gorrund's (§3). Canon leaves this n.d.

## 11. Recommendation — CONSTRAIN

Accept the Gorrund W2 family as built: 208 / 218 / 229 / 230.9 / 239 / 251 cm, Narrow GON5, Broad GOB7, composition, and AD-3 CLOSED. This is subject to four Gorrund-only rulings:

- **R1 — Broad thorax.** Accept Broad as pelvis- and girdle-led, with thorax ≤ about +1 % at the current depth.
  - Alternative: author a Broad that pairs thorax breadth with proportional depth. That is not a hard link to maximum depth, but it is new frame behavior.
  - Recommendation: accept as is.
- **R2 — GOR-BODY-14 definition.** Either:
  - (a) ALPC-0…4 plus depth vs Marchfolk, Grask and Skarn-depth / stature, per GO L759 — the extreme is ×0.90 and AD-G7 vs Skarn is waived; or
  - (b) AD-G7 vs Skarn binds — the lower-depth domain is under 2 %.

  Recommendation: (a).
- **R3 — elbow vs Broad Grask.** Treat joint presence as joint / adjacent bone; all PASS. If the per-stature reading must bind, the **minimum Gorrund-only correction** is elbow scale +1.7 % at 218 cm. It was not applied. Recommendation: per-bone.
- **R4 — palm depth at 218 cm.** Record it as a generator-route dip. The neighbors at 208 and 229 pass, so there is no correction. If it must pass, the minimum correction is a 218 cm-only palm-depth write (about +2 %), not tested. Recommendation: record.

**STOP.** Sagekin W2, elf W2, creator envelopes, facial extremes and UE5 work were not started.
