# Saurin Female Pass 3: Closure Package

**CLOSURE PACKAGE: for author review. `specs/saurin/SAURIN_V1.md` not edited.**

- **Author:** Claude
- **Responds to:** `reviews/chatgpt-saurin-female-pass3-closure-order.md` (c79174d)
- **Direction executed:** A-structure + E coelomic body wall + B subtle ventral fullness. D (paired breasts) is rejected and does not appear anywhere in this package.

## Method

All bodies are derived from the frozen reference (`c12/g15_body` base, `c12/g15_surf` scaled surface). Two layers were applied:
- the existing creator warp (`vary.warp`);
- the Pass-2 tissue fields (`tissue.py`, unchanged from Pass 2 except where noted).

The tissue fields are smooth, shell-following displacements: radial from a heavily smoothed torso-section centre. Head and tail compensation is K(trunk) = 1 + 0.19 · (trunk − 1), so the head and tail keep the reference absolute size and % H at every trunk value.

**No corrections were needed.** No female-distribution or tissue parameter was changed from the author's package.

## 1. Values ready for author reconciliation

| Tendency | Male centre | Female centre | Reference female (individual) | Hard bound / ceiling | Class |
|---|---|---|---|---|---|
| Lower axial trunk length | 0 % | **+7 %** | +10 % | ±10 % species bound (unchanged) | Biological anatomy: sex-shifted soft distribution |
| Pelvic band (skeletal) | 0 % | **+5.5 %** | +5.5 % | ±7 % species bound (unchanged) | Biological anatomy: sex-shifted soft distribution |
| Coelomic body-wall fullness (E) | 0 cm | **2.0 cm** | 2.0 cm | No new ceiling needed; it never approached the thoracic guard | Biological tissue tendency (not Presentation, not fat) |
| Ventral / ventrolateral fullness (B) | 0 cm | **1.6 cm** | 1.6 cm | **3.0 cm** ceiling (C-level), plus the shared thoracic depth/width ≤ 1.00 guard | Biological tissue tendency (not Presentation, not fat) |

- Every other control has **no sex shift**: stature, frame, muscle, fat, tail, cranial displays, skull and face.
- Male and female hard bounds are identical. Sex moves distribution centres only.

**Creator classification** (for the later universal review; no UI is finalized here):
- Sex is a distribution influence, not a preset.
- E and B are biological anatomy/tissue tendencies. They are not Presentation, and they are not folded into the generic fat control.
- Overlap is mandatory.
- No control is named "female body".

## 2. Quantitative change accounting

All bodies at equal stature (187.9 cm), Balanced frame, reference composition.

| Quantity | Male mean | Pass-1 female | **Female centre** | **Reference female** |
|---|---|---|---|---|
| Lower trunk, hip → costal margin (cm) | 32.0 | 33.4 | 33.6 (+5.0 %) | 34.3 (+7.3 %) ¹ |
| Pelvic width, external (cm) | 41.73 | 42.27 | 43.05 (+3.2 %) | 42.83 (+2.6 %) ² |
| Upper-abdomen width (cm) | 36.93 | 37.24 | 37.97 | 37.78 |
| Chest width (cm) | 38.57 | 38.16 | 38.09 | 37.89 |
| Midline thoracic depth (cm) | 33.41 | 33.06 | 34.58 | 34.40 |
| Thoracic depth/width (guard ≤ 1.00) | 0.880 | 0.880 | 0.922 | 0.922 |
| Ventral projection (cm) | 18.36 | 18.17 | 19.72 | 19.61 |
| **Front waist / shoulder** (silhouette) | 0.468 | 0.465 | **0.539** | **0.539** |
| Front waist / hip | 0.613 | 0.605 | 0.692 | 0.697 |
| Head length / H | 0.1696 | 0.1698 | 0.1698 | 0.1698 |
| Tail length (% H) | 64.6 | 64.7 | 64.7 | 64.7 |
| Tail root area (cm²) ³ | 527 | 516 | 515 | 509 |
| Tail RSI (normalized) | 1.00 | 1.01 | 1.01 | 1.02 |
| Extra lean vs reference (guard +3°) | 0 | −0.01° | −0.40° | −0.40° |

1. Measured lengths are smaller than the parameter percentages for two reasons: the stretch band ramps in smoothly, and stature normalization rescales the whole body to equal height.
2. The reference female's external pelvic width is slightly *less* than the centre's for the same pelvic parameter. This is stature normalization: the longer trunk scales the body by about 0.98.
3. Root anatomy is identical. The area differences are the same isometric normalization; RSI stays at 1.01–1.02.

**Distinguishability vs Pass 1.** Pass 1 left the frontal torso silhouette unchanged (waist/shoulder 0.465 vs 0.468). The final reference and the centre fill the sub-costal waist by **+15 %** (0.539) and add 1.3 cm of ventral projection.
- At creator and conversation distance, this is clearly more distinguishable (`v21_01`, `v21_02`).
- The change goes in the **anti-hourglass** direction: waist/hip rises from 0.61 to 0.69–0.70.

## 3. Scale-surface verification (`v21_06`)

Edge-length ratios on the 4.5 M-vertex scaled surface under the E+B displacement alone:

| Field | 1st–99th percentile | Max | Flipped faces |
|---|---|---|---|
| E+B (final) | 0.922–1.199 | 1.398 | **0** |
| C-level B 3.0 cm + E | 99th: 1.264 | 1.451 | **0** |

The peak combined displacement is 3.0 cm, where E and B overlap.

Scales keep their size class and field layout. No field boundary moves, and no new seams appear.

**Speckle in the fat-high rows comes from the existing fat tool, not E+B.** The fat-high rows show speckle and dark pits. These come from the *existing diagnostic fat-composition tool*, which offsets along raw vertex normals:
- 37,826 flipped faces on the surface;
- 99th-percentile edge stretch 1.72.

It appears identically on a male with fat high (control row in the sheet). It is a limitation of the diagnostic tool, not of E+B, and not a female finding. Production morphs will need a smoothed-normal fat displacement. Recorded as OPEN; it is not a female-anatomy blocker.

## 4. Validation results

| # | Required item | Sheet | Result |
|---|---|---|---|
| 1 | Male vs final reference female (front, profile, rear 3/4, torso 3/4, torso front; Pass 1 for comparison) | `v21_01` | PASS |
| 2 | Male mean vs female sampling centre | `v21_02` | PASS |
| 3 | Reference female and centre in isolation (they differ only in trunk +10 % vs +7 %) | `v21_03` | PASS |
| 4 | Torso close: E+B continuous across the midline, follows the thoracic shell; no paired forms, mammary read or hourglass | `v21_04` | PASS |
| 5 | Pelvis/sacrum/tail root: +1.1 cm external pelvis; no flare, buttocks or cleft; sacral platform, posterior mass and root unchanged; no external sex anatomy | `v21_05` | PASS |
| 6 | Scale surface (§3) | `v21_06` | PASS |
| 7 | Frame/composition on the reference female. Thoracic d/w: Narrow 0.985, Balanced 0.922, Broad 0.860, muscle low 0.907, muscle high 0.945, fat low 0.917, fat high 0.947 | `v21_07` | PASS |
| 8 | Stature 168 / 208 cm (isometric, d/w 0.922 at both) | `v21_08` | PASS |
| 9 | Tail extremes: see the tail table below | `v21_08` | PASS |
| 10 | Overlap: see the overlap table below | `v21_09` | PASS |
| 11 | Anti-stereotype: see the anti-stereotype table below | `v21_10` | PASS |
| 12 | Gameplay distance, accounting only (no anatomy exaggerated). Frontal waist change is visible as a slightly fuller mid-body; sex is not reliably readable at ~64 px, as accepted | `v21_11` | Recorded |
| 13 | Accounting and clamps | §2, §5 | — |

**Tail extremes (item 9)**

| Case | RSI | Extra lean |
|---|---|---|
| 55 % tail | 1.01 | −2.4° |
| 78 % tail | 1.18 | +2.5° |
| Broad + 80 % tail | 1.12 | +2.2° |

The 78 % tail sits near the RSI (≤ 1.20) and lean (≤ 3°) limits, the same as on the male. Coupling is unchanged.

**Overlap (item 10)**

- A **male at the female sampling centre is geometrically identical to the female centre**.
- An ordinary male inside the female range (trunk +5 %, pelvis +3 %, E 1.0 cm, B 0.8 cm) is valid.
- A female at the male mean is identical to the male reference.
- A female near the mean (+2 / +1 / 0.5 / 0.4) is valid. Her waist/shoulder is 0.487, between the sexes.

**Anti-stereotype (item 11)**

| Case | Result |
|---|---|
| Broad + high-muscle female | d/w 0.882, RSI 0.83 |
| Narrow + low-muscle female | d/w 0.969 |
| High-fat female | d/w 0.947, no hourglass |
| Low-fat female | E+B persist; she does not read as a "reduced male" |
| Narrow male with female-shifted values | Valid (d/w 0.985) and identical to the Narrow reference female |

## 5. Every clamp and coupling invoked

| Case | Requested | Result | Mechanism |
|---|---|---|---|
| Narrow + C-level ventral | B 3.0 cm, d/w **1.025** | **CONSTRAIN → B 2.1 cm** (d/w 0.999) | Shared thoracic depth/width ≤ 1.00 guard |
| Narrow + fat high + **centre** B | B 1.6 cm, d/w **1.002** | **CONSTRAIN → B 1.5 cm** (d/w 1.000) | Same guard. **New finding:** on Narrow + high fat, the female centre value clamps by 0.1 cm |
| Balanced + fat high + C-level | B 3.0 cm, d/w 0.984 | PASS: valid individual | — |
| Trunk +16 % (sex shift stacked on an individual) | — | **CONSTRAIN → +10 %** | Species hard bound; sex never extends the envelope |
| Pelvis | Never exceeded ±7 % in this package | — | — |
| E (body wall) | No clamp invoked | — | It adds width as well as depth, so it does not drive d/w up |

Couplings exercised and unchanged:
- tail length → base → RSI / taper / A50;
- balance guard;
- head and tail stature compensation;
- frame/composition independence.

Assessment of the Narrow + high-fat clamp: it is small (0.1 cm) and arises from the already-accepted d/w guard. It is the creator working as designed, not a contradiction. No parameter was changed.

## 6. Biological interpretation canonized by this closure (only what the anatomy requires)

**To canonize:**
- A and E: sex-correlated differences in coelomic (body-cavity) capacity and body-wall organization.
- B: a sex-correlated ventral soft-tissue tendency.

**Remains OPEN, not canon:**
- internal gestation;
- egg vs live young;
- the provisioning mechanism;
- reproductive organs and physiology;
- B as a reproductive fat body. This is kept as a plausible future explanation only.

**Excluded:**
- mammary glands;
- lactation;
- nipples, human breasts and human external genital anatomy;
- hip flare, paired buttocks, cleft and hourglass construction.

## 7. Frozen anatomy check

Untouched in every body:
- skull, rostrum, orbits, jaw, naked-head identity and neck;
- limb ratios, hands, feet and claws;
- tail envelope, path and coupling;
- sacral platform, posterior mass and tail root;
- scale-field topology.

Head length/H is 0.1698 in every female. The cranial-display family remains sex-neutral and fully available (validated in Pass 1; head construction is unchanged).

## 8. Closure criteria (order §8)

| Criterion | Result |
|---|---|
| More distinguishable than Pass 1 at creator/conversation distance | **Yes.** Waist/shoulder 0.465 → 0.539, ventral projection +1.3 cm, longer lower trunk |
| Biologically Saurin, not human-female-coded | **Yes.** Continuous, shell-following, anti-hourglass; nothing paired or mammary |
| Male/female distributions visibly overlap | **Yes.** Identical bodies across sexes demonstrated (`v21_09`, `v21_10`) |
| E+B survives frame/composition extremes without hourglass or mammary reads | **Yes**, with the d/w clamps listed in §5 |
| Gate 6/7 anatomy and surface identity intact | **Yes.** 0 flipped faces from E+B |
| No new reproductive canon | **Yes** |
| No sex-exclusive display, tail, stature, frame, muscle or fat rule | **Yes** |

## **SAURIN FEMALE ANATOMY CLOSED**

The values in §1 and the clamp list in §5 are ready for author reconciliation into `specs/saurin/SAURIN_V1.md`. The spec has not been edited.

## 9. OPEN (carried forward, non-blocking)

1. Reproductive life history: internal gestation, egg vs young, provisioning, organs.
2. B as a reproductive fat body (plausible, not canon).
3. Smoothed-normal fat displacement for production morphs (§3).
4. Statistical spreads of the female and male distributions around their centres (only centres and bounds are set here).
5. Female GLB comparison (file never accessible).

## 10. Files

**Images:** `reviews/images/saurin-female-closure/`
- `v21_01`…`v21_11`;
- `v21_metrics.json` (sweep, clamps, strain, silhouettes).

**Tools:** `tools/rodin/female/closure/`
- `fsets3.py`, `tissue.py`, `sweep3.py`, `render3.py`;
- `clamp.py`, `strain.py`, `torsosil.py`, `compose30.py`.

STOP. No spec edit. No facial-control architecture, pigmentation, clothing, rigging, animation, UE5 work or next race. Awaiting ChatGPT author review.

— Claude
