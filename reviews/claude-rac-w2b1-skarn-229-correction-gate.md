# RAC W2B1 — Skarn 229 cm Bounded Correction Author-Acceptance Gate

**Author:** Claude **Date:** October 7, 2026
**Author ruling (October 7, 2026; reviews/chatgpt-rac-w2b1-skarn-author-ruling-s7-normalization-order.md):** configuration 1 · 229 cm knee correction ACCEPTED; configuration 2 · 229 cm body ACCEPTED UNCHANGED; exact plane-section S7 ADOPTED; bounded S7 normalization across W1 / W2A / W2B ordered. The analysis below is unchanged.
**Order:** `reviews/chatgpt-rac-w2b-skarn-constrain-w2b1-order.md` (commit 4e93836)
**Evidence:** `reviews/rac-w2b1-sk-evidence/` (`tables.md` holds every number quoted; `probes.json`, `construction.json`, `s7_section.json`, `s7_band_probe.json`)

Every value here is a NON-CANON diagnostic. The accepted SK ARM, every other W2B body, the Marchfolk W2A bodies, Grask, Gorrund and the frame solution are untouched.

## Recommendation

The two 229 cm problems had different causes, so they get different fixes.

1. **Configuration 1 · 229 cm knee: corrected.** I made one local change, to the knee target on the 229 cm body only. The knee falls from +14.9 % to **+0.9 %** against the allometric slope. Stature, lengths, head, trunk, the other joints and the 208 cm ARM are unchanged.
2. **Configuration 2 · 229 cm S7 depth: no body correction, because the body is not collapsed.** The drop comes from how the generator samples the thigh mesh when the ±0.8 cm slab is read. It is not anatomy:
   - the skin thigh depth is continuous;
   - widening the slab or reading an exact plane section restores continuity (−1.3 % vs 208);
   - raising the thigh depth with the generator's own target makes the slab reading *fall*.

   Every body change I tried to "fix" it either alters limb lengths (which the order forbids) or leaves the reading erratic. I kept the accepted body and report a **CANDIDATE measurement ruling** for you to decide (§2).

**No previously accepted W2B row regressed.** Only the 229 cm continuity and knee rows changed (§3). No accepted Skarn, Marchfolk, Grask or Gorrund canon or reference needs challenge.

## 1. Configuration 1 · 229 cm knee

**Exact change** (229 cm body only): `measure-knee-circ-incr` 1.0 → removed; `measure-knee-circ-decr` 0 → 0.5. Height macro 0.929443 unchanged; stature 229.0 cm.

**Rule:** the W2A knee rule. I took the smallest probed 0.1 step that puts the knee back on the generator allometric slope from the 208 cm anchor, within the 1 % AD-G10 resolution.

| Knee write at 229 cm | knee / stature | vs slope (0.0683) |
|---|---|---|
| incr 1.0 (W2B, accepted ARM value) | 0.0784 | +14.9 % |
| incr 0.7 / 0.6 / 0.5 / 0.4 | 0.0764 / 0.0757 / 0.0750 / 0.0743 | +11.9 / +10.9 / +9.9 / +8.9 % |
| target removed | 0.0715 | +4.8 % |
| decr 0.3 | 0.0703 | +3.0 % |
| **decr 0.5 (W2B1)** | **0.0689** | **+0.9 %** |
| decr 0.6 / 0.7 | 0.0685 / 0.0681 | +0.3 / −0.3 % |

**Results after the change:**
- **Continuity:** 183 → 208 → 229 now runs 0.0758 → 0.0711 → 0.0689, a steady decline. The C row and K row both PASS.
- **Unchanged:** elbow, wrist and ankle; every segment share; the trunk grid readings. Nothing else on the body moves more than 0.05 % (`sheets/sk_229_w2b1.jpg`).

**Residual generator limit.** Even with the ARM's knee target removed, the 229 cm knee sits +4.8 % over the slope. The height macro at 0.93 widens the knee on the SK ARM by itself, so the correction has to cross zero into the decrease target. The 208 cm ARM (knee target 1.0, the generator maximum) is unchanged.

## 2. Configuration 2 · 229 cm S7 depth

**What the accepted reading does.** S7 is the femur section 20 % down the hip-to-knee axis. It is read on a ±0.8 cm slab of thigh vertices on each composition body, and the minimum across compositions is kept. At 229 cm the minimum-composition body is the one that sets it.

**Evidence that the drop is a sampling artifact, not anatomy:**

| Test | 208 cm | 229 cm (accepted body) |
|---|---|---|
| Accepted S7 depth / stature | 0.0725 | 0.0613 (−15.4 %) |
| Skin S7 depth / stature, reference composition | 0.1067 | 0.1032 (−3.3 %, continuous like the other trunk readings) |
| Minimum-composition depth: ±0.8 cm slab → ±1.5 cm slab | 15.07 → 15.07 cm | 14.02 → **16.48 cm** (0.0720) |
| CANDIDATE exact plane section (infimum) | 14.92 cm (0.0717) | **16.22 cm (0.0708, −1.3 %)** |

Only the 229 cm body is sensitive to the slab width. Its mesh is stretched, so the thin slab misses a vertex ring. This is the same failure W1h fixed for the trunk stations ("vertex slabs miss whole vertex rings where the mesh is stretched"), but S7 was never moved onto plane sections.

**Body probes, all rejected** (`probes.json`):

| Probe | Accepted S7 depth / stature | Side effect |
|---|---|---|
| Accepted route + `upperleg-scale-depth-incr` 0.5 / 1.0 | 0.0626 / 0.0638 | Skin depth +1 / +2 %. Collapse remains |
| Macro hand-off at 0.881 (= accepted 208 body) + extension | 0.0702 | femur / leg 0.5326 → 0.5174, leg −1.4 %, torso +1.5 %: the limb-length growth with height is lost (lengths scale nearly uniformly) |
| Hand-off at 0.90 / 0.92 / 0.94 | 0.0680 / 0.0683 / 0.0687 | femur / leg −2.3 % to −1.4 %, torso +1.2 % to +0.7 % |
| Hand-off 0.94 + depth target 0.5 / 1.0 | 0.0697 / **0.0631** | A *thicker* thigh reads *thinner*: the reading is not anatomical |
| Hand-off 0.96 / 0.97 + depth target 1.0 | 0.0634 / 0.0635 | Same |

A thigh bone-depth write would raise the skin depth by the same factor. That would create a new skin step. At most ×1.024 fits inside the skin continuity. Even combined with the depth target at 1.0, that reaches only 0.0653.

**Decision:** the configuration-2 229 cm body stays exactly as accepted in W2B. **No anatomical change is warranted.**

**CANDIDATE for author ruling (not applied):** read S7 as the composition infimum on an exact plane section of the thigh faces. This is the W1h trunk rule extended to S7 (`w2b1_drivers/s7_section.py`). It reproduces the accepted vertex readings exactly when run in slab mode (control).

Applied to every W2B check:
- 57 rows change value; **none changes result**. One more continuity row passes (configuration 2 S7 breadth at t = 0).
- Skarn > Marchfolk S7 margins stay ≥ +9.0 %.
- Configuration 2 S7 depth runs 0.0727 → 0.0717 → 0.0708.

**Cost if adopted:** it would also move accepted S7 values elsewhere. Examples:
- MF 203 configuration 1 depth: 11.95 → 13.81 cm (+15.6 %; the same artifact);
- SK-04: 12.73 → 14.86 cm;
- W1 SK / SG / MF-M-R / GO-H208: +1.4 / +2.0 / +3.9 / +2.3 %.

The W1 and W2A S7 rows have **not been re-run** under it. The t = 0.5 / 1.0 S7 readings are built on the same vertex infimum, so their reversals remain until a ruling.

## 3. Regression

Re-ran the full W2B evaluation with only the 229 cm bodies substituted (`w2b1.json`). A control run with the W2B bodies reproduces W2B exactly (432 checks, identical values and results).

| Required re-check | Result |
|---|---|
| 229 cm continuity, configuration 1 | Knee reversal resolved (PASS) |
| 229 cm continuity, configuration 2 | Accepted reading unchanged; S7 breadth / depth t = 0.5 / 1.0 and S7 breadth t = 0 still flagged. Resolved only under the §2 candidate |
| Skarn > Marchfolk overlap directions (190 / 203) | 60 / 60 identical |
| Canonical pair MF 203 vs SK 183 | 30 / 30 identical |
| Frame lengths / stature invariance | 20 / 20 identical; frame domains 36 / 36 identical |
| Broad Skarn below GO-H208 on authored carriers | 2 / 2 identical |
| ALPC-7 | 21 / 21 identical |
| Composition shares | 8 / 8 identical |
| SK-04 | Unchanged |

**Totals:** 432 checks; 370 PASS, 57 REPORT, 5 continuity reversals. All five are configuration 2 S7 rows (W2B had 368 / 58 / 6).

**Envelope change:** the knee minimum is now SK-M229 (0.0689); the knee maximum is SK-F183 (0.0782).

## 4. Residuals

| Item | Status |
|---|---|
| Configuration 1 · 229 cm knee | Corrected; the height macro alone adds +4.8 % at 229 cm on the SK ARM (generator characteristic) |
| Configuration 2 · 229 cm S7 | Body unchanged; slab-sampling artifact; candidate measurement ruling pending |
| Configuration 2 · 229 cm height | Generator macro maximum (1.0) + native extension, unchanged from W2B |
| Configuration 2 · 183 cm knee −5.2 % vs slope | Unchanged report (outside this order) |
| Knee decr 0.4 | Not built (interpolates to about +2 %) |

## 5. For the author

1. Accept the configuration 1 · 229 cm knee correction (`measure-knee-circ-decr` 0.5 in place of incr 1.0, 229 cm only).
2. Accept that configuration 2 · 229 cm keeps its W2B body, with the S7 depth drop classed as a measurement artifact rather than a body defect.
3. Rule on the candidate: S7 on exact plane sections. If adopted, I re-run the S7 rows of W1, W2A and W2B as a separate bookkeeping block.

The next W2 population is not started.

STOP.

— Claude
