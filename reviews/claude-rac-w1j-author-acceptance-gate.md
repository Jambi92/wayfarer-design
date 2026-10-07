# RAC W1j — Gorrund Robustness Gate

**Author:** Claude **Date:** October 6–7, 2026
**Order:** `reviews/chatgpt-rac-w1i-author-decisions-w1j-robustness-order.md`
**Evidence:** `reviews/rac-w1j-evidence/` (`tables.md` holds every number quoted here; `README.md` maps the files).
The retained candidate is the W1i point. W1j rebuilt the reference and the four stature bodies, and they are identical to the W1i meshes (`geometry_identity.json`: max |ΔV| = 0 for each). Results W1j did **not** re-run (frames, ALPC-5 / 6 / 8, arm-tube test, ocular, ears, skin table) are carried from `reviews/rac-w1i-evidence/` on that basis (§7).

## Recommendation: CONSTRAIN — within the current search bounds the upper-thorax knife edge could not be materially reduced; the trade is presented (order §8, last paragraph)

1. **No more stable configuration was found.**
   - I tried a robust re-solve, a femur-ceiling trade study and a most-interior linear programme (candidate D). I also built the femur-1.294 trade point (candidate C).
   - Under the same ±2 % protocol on the W1j stature series, the retained W1i point is the most stable:

| Point | Perturbations keeping every relation | Reaching FAIL |
|---|---|---|
| **Retained W1i point** | **22 of 32** | **2** |
| D | 17 of 32 | 4 |
| C | 16 of 32 | 3 |

   - **Correction:** thoracic breadth falling *below* Skarn is a FAIL, which W1i did not count. The W1i point therefore has 2 FAIL, not 1, under both protocols (§2).
2. **The upper-thorax group cannot be made ±2 % robust inside the current search bounds** (first-order linear model, §3).
   - The group is rib-cage breadth, upper-thorax length, kb60 and kb80. The other 12 values can be made ±2 % robust together.
   - With those 12 held, rib-cage breadth tolerates about **±0.2 %**.
   - The binding relations:
     - rib-cage vertical ÷ breadth ≥ Marchfolk (ALPC-1b) at 208 cm, t = 1.0;
     - thoracic breadth > Skarn;
     - for the built +2 % step also AD-G7 thoracic depth ÷ breadth > SK and ALPC-7 crest ÷ thorax vs Broad Skarn;
     - at the femur-1.294 point also ALPC-4.
   - **Part of this limit is the non-canon search bounds.** Widening every bound by 0.5 raises the first-order tolerance to about ±1.2 %. That is still short of ±2 %, it needs large moves further *out* (kb44 / kb60 / kb80, posterior depth), and it was not built.
3. **Femur: a point at 1.294 passes every canonical relation; 1.274 fails one (§4).**
   - The femur floor is therefore **between about 1.27 and 1.29 in this construction**. This is a local estimate from one linearisation plus built checks, not a proven minimum.
   - The 1.294 and 1.306 points are less stable (16–17 / 32) and miss the W1j low-composition shelf guard by 0.0002–0.0004.
   - They also differ from the retained point in all 16 values, so the stability difference is not caused by the femur alone.
   - The visual difference from 1.386 is small (`sheets/femur_trade_hips.jpg`).
4. **Low composition (§5).**
   - Against MF and SK at the *same* low composition, Gorrund's waist ÷ hip-block is higher (0.821 reference, 0.827 at 208, vs 0.807 / 0.819): less shelf on that reading. Its waist ÷ thorax is higher (no pinch).
   - Its hip ÷ thorax is also higher (1.051 / 1.037 vs 0.996 / 0.984), as ALPC-7 requires. Its waist above the crest is slightly weaker (1.105 / 1.092 vs 1.111 / 1.110).
   - The W1i ALPC-6 skin half still applies: official slab reading 5 FAIL. Re-read on plane sections: 1 FAIL (pelvic AP ÷ thoracic depth) and 1 MARGINAL (hip-level ÷ lumbar).
   - These readings inform, but do not replace, the author's visual ruling on low-composition pelvic shelf.
5. **No accepted canon was challenged.** No other race was changed. Nothing is accepted.

**For the author:**
1. Accept the W1i point as the constrained central reference with the sensitivity stated here. Or rule on which side of the upper-thorax trade should give: one of the relations in item 2, or the search bounds.
2. Femur 1.386 (more stable here) or about 1.29 (lowest found that passes; less stable as built).

**Audit.** An independent auditor agent reviewed the first draft of this gate against the evidence. I checked each claim before changing anything. Corrections made:
- **FAIL counts.** Thoracic breadth falling below Skarn is now counted as a FAIL. This raises the retained point to 2 FAIL, and the W1i figure too (W1i reported 1).
- **Knife edge.** The draft called it intrinsic. It is now framed as limited partly by the search bounds: the widened-bound run is ≈ ±1.2 %, not built.
- **Femur floor.** Stated as a local, single-linearisation estimate.
- **Candidates C / D.** They pass every canonical relation but miss the W1j low-composition guard. C also has a small chest-lead shortfall (−0.0037, a W1h construction floor).
- **ALPC-6 skin residuals** added.
- **Frame results** marked as carried from W1i, with a not-re-run list.
- **ALPC-7 pair coverage** stated.
- **Competing relations.** AD-G7 and ALPC-7 added.
- **Margin.** The 208 cm ALPC-1b base margin disclosed.
- **Values table.** Full table with % of value.
- **d2b** added.
- **Labels** corrected:
  - 253.0 cm for the 251 donor;
  - candidate D, t1 = 0.5;
  - the robust-step shortfall quoted as built, not modelled.
- **Hip-crop command.** The femur hip-crop render command was added to `render_AS_RUN.sh`; re-running it reproduces the sheet pixel-for-pixel.

## 1. What W1j did (order §7)

**Robust re-solve** (`w1j_drivers/gn7.py`, run J1):
- **Method.** Ordinary thresholds, plus a first-order requirement that every single ±2 % step keeps every accepted relation. In the loop:
  - the true 208 cm body, with its equal-height Broad Skarn 208 pair;
  - the low-composition grid bodies of the reference and of the 208 cm body.
- **Result.** Built robust shortfall: 0.40 at the W1i point, 0.075 after one step, 0.052 at the best later step (model predictions 0.045–0.050).
- But the built steps broke ordinary relations; thoracic breadth > SK slack went negative, below the 1 % convention. The first-order picture does not hold over 2 % steps of these values. Not used.

**Interior analysis** (`interior_analysis.py`, `interior_bounds.py`, `maxmin.py`): §3.

**Femur trade** (`femur_trade2.py`): one linear model at the W1i point, with femur ≤ ceiling; each predicted point was built and checked. §4.

**Candidates D and C, and the retained point W**, through the full ±2 % protocol on the W1j series (`sens7.py`): §2.

**Renders** (`render_AS_RUN.sh`):
- retained candidate, four views: reference, true 208, 253 cm, Narrow, Broad, low composition, skeleton;
- Broad Skarn 208 / 229 comparison;
- trunk crop with same-composition MF / SK;
- femur hip crop.

**W1j stature series:**
- reference 230.9 cm;
- true 208.3 cm (height macro 0.685);
- 217.0 cm and 224.1 cm (215 / 222 donors);
- GOR-BODY-03 at 253.0 cm (251 donor).

**ALPC-7 in the W1j protocol** covers 8 pairs: 208 × {208, 215, 222, 229}, 215 × {222, 229}, 222 × 229, and 229 × 229.

For the retained point, all **10 W1i pairs** (W1i series) and all **4 true-208 pairs** pass (W1i `skeletal/alpc_w1i.json`, `skeletal/true208.json`).

## 2. Sensitivity before / after (tables §1)

| Point | Femur | Protocol | Keep every relation | FAIL |
|---|---|---|---|---|
| W1i point | 1.386 | W1i series (W1f 208 cm donor, 10 pairs) | 23 / 32 | 2 (kb18 −2 %, rib-cage breadth −2 %) — W1i reported 1 |
| **W1i point (retained)** | 1.386 | **W1j series** | **22 / 32** | **2** (same two) |
| D (linear programme, t1 = 0.5 ≈ ±1 % for 12 values) | 1.306 | W1j series | 17 / 32 | 4 (pelvis X −2 %, kb18 +2 %, rib-cage breadth ±2 %) |
| C (femur trade, ceiling 1.30) | 1.294 | W1j series | 16 / 32 | 3 (pelvis Y −2 %, rib-cage breadth ±2 %) |

**Retained point, losses under the W1j protocol** (tables §1):

| Perturbation | What fails |
|---|---|
| Rib-cage breadth −2 % | thoracic breadth vs SK −0.25 % (**FAIL**) |
| Rib-cage breadth +2 % | AD-G7 NOT DEMONSTRATED; ALPC-1b at 208 / 215 / 222 cm; ALPC-7 crest ÷ thorax at 4 cross pairs |
| Upper-thorax length −2 % | ALPC-1b at 208 / 215 / 222 cm |
| Upper-thorax length +2 % | thoracic breadth vs SK +0.94 % (NOT DEMONSTRATED) |
| kb44 / kb60 / kb80 +2 % | ALPC-1b at 208 cm |
| pelvis X +2 % | bitrochanteric ÷ crest ≈ MF, T-SENSITIVE |
| pelvis Y −2 % | pelvic vertical vs GR, MARGINAL |
| kb18 −2 % | **bitrochanteric ÷ crest ≈ MF FAIL** (a two-sided ±0.010 row) |

The 251-donor body (253.0 cm) appears in no loss list.

**Base margin to note:** at the retained point, ALPC-1b at 208 cm, t = 1.0, passes by only about 0.07 %.

## 3. The upper-thorax trade (tables §3)

**At the retained point:**
- **12 values can be ±2 % robust together:** pelvis X / Y / Z, femur, clavicle, ka, kp lower / upper, kb0, kb18, kb31, kb44.
- **The other four cannot**, holding those 12 (tolerance as a fraction of the ±2 % step):

| Value | Tolerance |
|---|---|
| Rib-cage breadth | 0.09 |
| Upper-thorax length | 0.11 |
| kb60 | 0.34 |
| kb80 | 0.45 |

Binding relations: ALPC-1b at 208 cm (t = 1.0), then thoracic breadth > SK.

**What limits it** (`interior_bounds.json`):

| Case | Joint tolerance | Comment |
|---|---|---|
| Current bounds, 2 % gap | 0.092 | Ten values sit on a search bound or the step limit at the optimum |
| Gap removed | 0.119 | |
| Every bound widened by 0.5, step limit 0.25 | 0.596 (≈ ±1.2 %) | Binding: thoracic breadth > SK, ALPC-1b at 208 cm, ALPC-2b crest ÷ lumbar. The step limit is then active for six values. Not built |

**At the femur-1.294 point:** the 12 cannot all be held at ±2 % within the current bounds. With widened bounds the joint tolerance is 0.586; the binding relations are ALPC-1b at 208, ALPC-7 vs Broad Skarn 229 and AD-G7.

**In plain terms:**
- Gorrund's skin thorax must be over 1 % wider than Skarn's.
- At the 208 cm end its rib cage must stay at least as tall, relative to its breadth, as Marchfolk's.
- Its thoracic depth ÷ breadth must stay above Skarn's, and its crest must stay broad relative to the thorax against Broad Skarn.
- The rib-cage breadth that meets all of these is narrow. Within the current search bounds that band is about ±0.2 %.
- **This is a first-order argument from two linearisation points, confirmed by the built protocol:** rib-cage breadth and upper-thorax length fail in both directions in every built candidate.
- It does not prove that no point beyond the current bounds is more robust.

## 4. Femur trade study (tables §2; `sheets/femur_trade_hips.jpg`)

| Femur ceiling | Femur | Built: canonical relations not passing | Thoracic breadth vs SK | W1j low-comp shelf guard (≥ 0.8191) | Protocol |
|---|---|---|---|---|---|
| — (retained) | 1.386 | 0 | +1.41 % | 0.8214 / 0.8273 | 22 / 32, 2 FAIL |
| 1.40 / 1.35 | 1.368 / 1.343 | 1 FAIL each (bitrochanteric ÷ crest ≈ MF) | +1.33 / +1.34 % | 0.8182 below | — |
| 1.33 (D, re-linearised at 1.294) | 1.306 | 0 | +1.35 % | 0.8189 below (by 0.0002) | 17 / 32, 4 FAIL |
| 1.30 (C) | **1.294** | **0** | +1.42 % | 0.8187 below (by 0.0004) | 16 / 32, 3 FAIL |
| 1.28 | 1.274 | 1 (proximal femur ÷ crest ≥ SK, T-SENSITIVE) | +1.15 % | 0.8182 below | — |
| ≤ 1.27 | — | linear model at the W1i point: no feasible point (trust 0.25) | — | — | — |

**Answer to order §3:**
- In this construction the lowest femur found that keeps every canonical relation at every stature and pair of the W1j series is **1.294**. 1.274 fails, so the floor lies between them.
- That point was **not** checked on frames, ALPC-5 / 6 / 8 or composition beyond the reference and 208 cm.
- The femur is held up by a chain:
  - proximal femur ÷ crest ≥ SK and bitrochanteric ÷ crest ≈ MF tie the femur to the crest;
  - ALPC-7 ties the crest to the thorax;
  - thoracic breadth > SK ties the thorax to Skarn.
- **1.386 tested more stable (22 vs 16–17 / 32).** The candidates differ in all 16 values, so this is not a femur-only effect.
- **Visually,** the thighs at 1.294 are slightly slimmer at the hip and upper thigh. The hip crop stops just above the waist, so it shows the pelvis-to-thigh transition only.

## 5. Low composition, skeleton and continuity (tables §5; `sheets/trunk_crop_w1j.jpg`)

| Body (muscle 0.25 / weight 0.25) | hip ÷ thorax | waist ÷ thorax | waist ÷ hip-block | waist rise |
|---|---|---|---|---|
| MF-M-R, same composition | 0.996 | 0.804 | 0.807 | 1.111 |
| SK, same composition | 0.984 | 0.806 | 0.819 | 1.110 |
| GO reference | 1.051 | 0.863 | 0.821 | 1.105 |
| GO true 208 cm | 1.037 | 0.858 | 0.827 | 1.092 |

**On the W1i comparator.** W1i compared GOR-BODY-16 with *reference-composition* skins (waist ÷ hip 0.839–0.868) and reported more hip shelf than any reference. At the same composition MF and SK read 0.807 / 0.819. On this reading Gorrund's low-composition shelf is not larger than the human references'. Its pelvis is broader relative to its thorax, and its waist-above-crest reading is slightly weaker. This is a measurement note for the author's visual judgement, not a reversal of it.

**ALPC-6 skin half (W1i, same geometry):**
- official slab reading 5 FAIL;
- plane-section re-read 1 FAIL (pelvic AP ÷ thoracic depth) and 1 MARGINAL (hip-level ÷ lumbar);
- the skeletal half passes.

**Skeleton (minimum composition):**

| Reading | GO reference | GO true 208 | Broad Skarn 208–229 |
|---|---|---|---|
| waist ÷ thorax | 0.799 | 0.785 | 0.732–0.748 |
| waist ÷ hip-block | 0.700 | 0.693 | 0.667–0.680 |
| hip ÷ thorax | 1.141 | 1.132 | 1.097–1.100 |
| breadth crease d2b | 0.0081 | 0.0108 | 0.0050–0.0066 |

- On d2b, Gorrund is 1.2–2.2× Broad Skarn. It is inside the MF / SG / DU reference range (≤ 0.0147).
- The lower-rib-margin edge the author noted is also visible on the Broad Skarn 229 and SK skeleton bodies (`trunk_crop_w1j.jpg`), so the generator's minimum-composition mesh contributes. Gorrund's edge is stronger by the d2b reading.

## 6. Final construction values and search bounds (tables §4; unchanged from W1i, `tools/rac/w1/cfg/w1i/GO.json`)

| Value | Final | Bound | Distance from bound, % of range | % of value |
|---|---|---|---|---|
| pelvis X | 1.2138 | [0.95, 1.25] | 12.1 % | 2.98 % |
| pelvis Y | 1.0450 | [0.97, 1.10] | 42.3 % | 5.26 % |
| pelvis Z | 1.2512 | [1.00, 1.35] | 28.2 % | 7.90 % |
| **femur robusticity** | 1.3863 | [1.00, 1.40] | **3.4 %** | **0.99 %** |
| clavicle length | 1.0069 | [0.85, 1.05] | 21.5 % | 4.28 % |
| **upper-thorax length** | 1.2404 | [1.00, 1.25] | **3.9 %** | **0.78 %** |
| ka amplitude | 1.0723 | [0.00, 1.10] | **2.5 %** | 2.58 % |
| kp lower (r 0.18 / 0.31) | 1.6225 | [0.90, 1.70] | 9.7 % | 4.78 % |
| kp upper (r 0.44 / 0.6) | 1.2782 | [0.85, 1.50] | 34.1 % | 17.35 % |
| kb r 0 | 1.0243 | [0.90, 1.30] | 31.1 % | 12.14 % |
| kb r 0.18 | 1.1599 | [0.90, 1.45] | 47.3 % | 22.41 % |
| kb r 0.31 | 1.3039 | [0.90, 1.40] | 19.2 % | 7.37 % |
| kb r 0.44 | 0.9116 | [0.90, 1.30] | **2.9 %** | 1.27 % |
| **kb r 0.6** | 0.9083 | [0.90, 1.20] | **2.8 %** | **0.91 %** |
| **kb r 0.8** | 1.1427 | [0.90, 1.15] | **2.9 %** | **0.64 %** |
| rib-cage breadth | 1.0460 | [0.95, 1.15] | 48.0 % | 9.18 % |

- **Within about 1 % of a bound, by value (order §4):** femur, upper-thorax length, kb60 and kb80. Six values are within 5 % of range.
- The femur bound of 1.40 is the author-accepted diagnostic bound.
- Upper-thorax length, kb60 and kb80 belong to the knife-edge group (§3). Moving them inward within the bounds costs one of the competing relations; moving them outward needs wider, non-canon bounds.

## 7. Residuals

| Item | Status |
|---|---|
| Rib-cage breadth −2 % | thoracic breadth below SK, **FAIL** |
| kb18 −2 % | bitrochanteric ÷ crest ≈ MF **FAIL** |
| Upper-thorax group | two-sided sensitive; first-order tolerance about ±0.2 % within bounds |
| ALPC-1b at 208 cm, t = 1.0 | base margin about +0.07 % |
| Femur 1.386 | not shown biologically necessary; lowest passing point found 1.294 |
| ALPC-6 skin half (W1i) | slab 5 FAIL; sections 1 FAIL + 1 MARGINAL |
| Skin pelvic AP ÷ thoracic depth | skin FAIL; skeletal relation passes |
| Armpit band | NOT DEMONSTRATED; visually accepted (order §6) |
| VA skin pelvic depth | FAIL (other race, unchanged) |
| SK elbow and knee | NOT DEMONSTRATED (unchanged) |

**NOT RUN in W1j (carried from W1i on identical geometry):**
- frame bodies (GOR-BODY-04 / -12 / -14 relations; -05 Broad is render-only and has never had relations run);
- ALPC-5 / 6 / 8;
- arm-tube test;
- directional and skin tables;
- ocular and ears;
- the 215v215 and 222v222 ALPC-7 pairs (W1i: pass).

**NOT RUN at all:**
- low composition at 215 / 222 / 253 cm and on the frames;
- frames, ALPC-5 / 6 / 8 and the full skin table for candidates C / D;
- a robust re-solve with the built (nonlinear) protocol as objective;
- built checks of the widened-bound interior point.

## 8. Canon statement

**No accepted canon was challenged.** The upper-thorax trade is between accepted relations, within construction search bounds that are not canon:
- Gorrund thoracic breadth > Skarn;
- ALPC-1b rib-cage proportion ≥ Marchfolk across the stature range;
- AD-G7 thoracic depth ÷ breadth > Skarn;
- ALPC-7 crest ÷ thorax > Broad Skarn;
- ALPC-4.

Loosening the trade would need either an author ruling on one of those relations, or authority to search beyond the current bounds (more extreme upper-thorax and posterior-depth sculpt values), which the order discourages. I have done neither.

No UE5, topology, rigging, animation, IK, equipment, gameplay or class work was done.

## 9. Recommendation

**CONSTRAIN.** Within the current search bounds, W1j could not materially reduce the remaining knife edge, and it presents the trade.

The retained W1i point is the most stable configuration found:
- every canonical relation passes on the reference, the W1j stature series (208.3–253.0 cm) and all ALPC-7 pairs, at the reference and 208 cm low composition, and (from W1i) on the three frame bodies;
- 22 / 32 ±2 % steps keep everything, and 2 reach FAIL;
- the sensitive group is the upper thorax, with its competing relations stated.

STOP.

— Claude


## Author ruling — October 7, 2026

**ACCEPTED / W1 CLOSED FOR GORRUND.** ChatGPT accepted the retained W1i/W1j point as the Gorrund W1 Anatomical Reference Mesh. The 22/32 perturbation result, two FAIL perturbations, upper-thorax sensitivity, ALPC-1b small margin, ALPC-6 skin residuals and armpit-band NOT DEMONSTRATED status remain recorded diagnostics. Femur 1.3863 is retained for the accepted reference construction, not promoted to a species-wide biological constant; ~1.294 remains a lower passing diagnostic trade point. See `reviews/chatgpt-rac-w1j-gorrund-final-author-acceptance.md`.
