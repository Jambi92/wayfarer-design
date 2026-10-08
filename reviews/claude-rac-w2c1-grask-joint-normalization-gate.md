# RAC W2C1 — Grask Joint-Measurement Normalization Author-Acceptance Gate

**Author:** Claude **Date:** October 7, 2026
**Order:** `reviews/chatgpt-rac-w2c1-grask-joint-normalization-order.md` (commit c70b79b)
**Evidence:** `reviews/rac-w2c1-joint-evidence/` (`tables.md` holds every number; `joint_sections.json`, `knee_normalization.json`, `elbow_wrist_ankle_check.json`)

Measurement normalization only. **No body was rebuilt.** Every reverted value is a knee-only generator target. The bodies it points back to already existed and were measured in W2A / W2B.

## Recommendation: ACCEPT final Grask W2 closure

Under the exact-plane knee section, the slab-derived 0.575 slope is not reused. Using the section readings alone:

**Knee corrections:**

| Correction | Exact-plane verdict | Action |
|---|---|---|
| MF 190, configuration 1 | Unnecessary | **Reverted** |
| MF 203, configuration 1 (accepted W2A) | Unnecessary | **Reverted** |
| MF 203, configuration 2 (accepted W2A) | Unnecessary | **Reverted** |
| SK 229, configuration 1 (accepted W2B1) | Unnecessary; it moved the knee farther from the trend | **Reverted** |
| MF 190, configuration 2 | Supported (marginally) | **Kept** |

**After the reverts:**
- Every accepted knee decision still holds under the section reading. Skarn > Marchfolk overlap knees are +21 to +26 %.
- Elbow, wrist and ankle show slab / section offsets, but no accepted decision changes.
- **The accepted Grask W2C bodies are unchanged and show no contradiction.** Their knee series is smooth, and the W2C knee flags were the slab artifact.

## 1. Exact-plane knee measurements

`joint_sections.json`; tables, "Joint breadths". Values are knee breadth ÷ R-6 stature, section (slab).

| Population | Bodies |
|---|---|
| Marchfolk configuration 1 | 147: 0.0734 (0.0744) · 173: 0.0696 (0.0688) · 190 uncorrected: 0.0684 (0.0557) · 190 K8: 0.0756 (0.0644) · 203 macro: 0.0666 (0.0580) · 203 K6: 0.0705 (0.0640) |
| Marchfolk configuration 2 | 147: 0.0697 · 173: 0.0661 · 190 uncorrected: 0.0614 · 190 K3: 0.0639 · 203 macro: 0.0607 · 203 K3: 0.0629 |
| Skarn configuration 1 | 183: 0.0857 · 190: 0.0844 · 198: 0.0822 · 203: 0.0807 · 208 ARM: 0.0794 (slab 0.0711) · 218: 0.0785 · 229 original: 0.0789 (0.0784) · 229 W2B1: 0.0694 (0.0689) |
| Skarn configuration 2 | 183: 0.0789 · 190: 0.0781 · 203: 0.0766 · 208: 0.0763 · 229: 0.0757 |
| Grask (W2C control) | 198: 0.0726 · 208: 0.0706 · 218: 0.0686 · 229: 0.0674 · 239: 0.0668 |
| Gorrund (diagnostic) | GO-H208: 0.0780 · 217 donor: 0.0749 · 224 donor: 0.0729 · W1 central (231 cm): 0.0716 |

**Slab ÷ section ranges 0.81–1.02, and it depends on the body.** The slab under-reads exactly the bodies the corrections were measured against: SK 208 at 0.896, MF 190 / 203 macro at 0.81 / 0.87, Grask 198 at 0.845.

## 2. Normalized knee allometry

Each fit is a log-log fit over the **uncorrected** bodies only. Tables, "Normalized knee trends".

| Population | Bodies | Slope (share) | Max residual | Adequacy |
|---|---|---|---|---|
| Marchfolk configuration 1 | 147, 173, 190, 203 | −0.290 | 0.5 % | Adequate but small. Two routes (147 native, 190 / 203 macro) on one curve |
| Marchfolk configuration 2 | 147, 173, 190, 203 | −0.456 | 1.7 % | Small. Its scatter is comparable to the 190 cm verdict margin |
| Skarn configuration 1 | 183–229 (7) | −0.413 | 1.9 % | Good. The top end flattens (218 / 229) |
| Skarn configuration 2 | 183–229 (5) | −0.190 | 0.5 % | Adequate. The 229 cm body is the native-extension route |
| Grask | 198–239 (5) | −0.451 | 0.8 % | Good |
| Gorrund | 3 donors + W1 central | −0.834 | — | **Insufficient** for a rule: mixed constructions; diagnostic only |

The slopes differ by population and configuration. No single cross-race knee slope is supported. Each correction is judged against its own population's trend, **leave-one-out**: the fit excludes every body at the judged stature.

## 3. Ruling recommendations on the questioned knee corrections

| Correction | Expected (LOO trend) | Uncorrected | Corrected | Recommendation |
|---|---|---|---|---|
| **MF 190, config 1** (knee target 0.8) | 0.0679 | 0.0684 (+0.7 %) | 0.0756 (+11.4 %) | **Unnecessary → revert** to the height-macro body |
| **MF 203, config 1** (accepted W2A K6, knee 0.6) | 0.0669 | 0.0666 (−0.4 %) | 0.0705 (+5.3 %; above the 173 cm anchor, a reversal) | **Unnecessary → revert** |
| MF 190, config 2 (knee 0.3) | 0.0628 | 0.0614 (−2.2 %) | 0.0639 (+1.8 %) | **Supported (marginal)** → kept. Both readings are within the 1.7 % fit scatter; the rule reverts only when the uncorrected body is the more coherent one |
| **MF 203, config 2** (accepted W2A K3, knee 0.3) | 0.0602 | 0.0607 (+0.8 %) | 0.0629 (+4.5 %) | **Unnecessary → revert** |
| **SK 229, config 1** (accepted W2B1: knee incr 1.0 → decr 0.5) | 0.0759 | 0.0789 (+4.0 %) | 0.0694 (−8.6 %) | **Unnecessary; moved the knee farther → revert** to the original W2B body (ARM knee incr 1.0) |

**Residual.** The original SK 229 sits +4.0 % over the LOO trend, beyond a 3 % builder tolerance, because Skarn's knee flattens at the macro top (SK 218 is +1.7 % over the same fit). No new correction is proposed, per the order.

## 4. Elbow / wrist / ankle method check

`elbow_wrist_ankle_check.json`; tables, "Elbow / wrist / ankle".

| Joint | Slab ÷ section | Character |
|---|---|---|
| Elbow | 1.008–1.026 | Near-uniform |
| Wrist | 1.017–1.104 | Population / configuration-linked (MF configuration 2 ≈ 1.10, Skarn ≈ 1.03–1.06) |
| Ankle | 1.039–1.174 | Population-linked (Marchfolk / Grask / elves ≈ 1.13–1.17, Skarn ≈ 1.09) |
| (Knee | 0.81–1.02 | The only joint whose offset swings within one population across stature) |

**Accepted comparisons re-read** (16 pairs × 4 joints):
- Skarn > Marchfolk at 190 / 203, both configurations;
- the canonical pair;
- Gorrund > Grask at 208 / 218;
- Skarn vs Grask (report);
- Broad Skarn vs GO-H208 (report);
- Narrow Skarn vs MF 203.

**No ordering and no 1 % class changes on any scored decision.** Section margins are close to slab margins: ankle margins widen by 2–4 points, wrist margins move by ≤ 9 points, in the decided direction. One improvement:
- **Gorrund > Grask knee at 217–218 cm** goes from +0.2 % (slab) to +9.1 % (section). The W1 row used the skin knee ÷ femur reading and already passed.

**Class changes appear only on the unadjusted elf pairs:** MF vs Aelari / Fenn wrist and ankle, and Vael vs Aelari / Fenn ankle. These are diagnostic, stature-mismatched pairs.
- The accepted **W2A1 "wrist vs Aelari: no verdict"** row stays no verdict. The central Marchfolk carried to 190 cm on the normalized Marchfolk trend sits at ≈ 0.0 % against Aelari.
- The thin accepted **W1 elf joint rows** were not re-scored, because elves are outside this order's set:
  - Fenn ankle gracility vs Aelari −1.47 %;
  - Vael ankle > Aelari +1.3 %;
  - Vael wrist > Aelari +1.8 %.

  On the unadjusted pairs the section shifts every one of them by about 1–2 points **in its accepted direction**: Fenn lighter, Vael heavier. No reversal is indicated. **Identified for a bounded re-check before elf W2 relies on joint scale.** I did not propagate the method silently.

## 5. Accepted comparator bodies that changed (knee-only writes)

| Record | Write changed | Body now |
|---|---|---|
| W2A Marchfolk 203, configuration 1 | `measure-knee-circ-incr` 0.6 → removed | height-macro body (MFM203) |
| W2A Marchfolk 203, configuration 2 | `measure-knee-circ-incr` 0.3 → removed | height-macro body (MFF203) |
| W2B Marchfolk 190, configuration 1 (comparator) | `measure-knee-circ-incr` 0.8 → removed | height-macro body (MFM190) |
| W2B1 Skarn 229, configuration 1 | `measure-knee-circ-decr` 0.5 → removed; `measure-knee-circ-incr` 1.0 restored (ARM value) | original W2B body (SKM229) |

**Only the knee readings change.** Every skin ratio other than knee ÷ femur is identical, and the skeletal grids are untouched. Recorded in `cfg/w2a/MF-boundary.json` and `cfg/w2b/SK-boundary.json`. **Unchanged:** Marchfolk 190 configuration 2 (knee 0.3), and every other accepted construction value.

**Knee rows re-checked on the resolved bodies** (section) — tables, "Accepted knee decisions re-checked". All PASS:
- Skarn > Marchfolk 190 / 203: +23.4 / +21.1 % (configuration 1), +22.1 / +26.3 % (configuration 2);
- canonical pair: +24.8 / +24.1 %;
- Gorrund > Grask: +10.5 / +9.1 %;
- W2A1 Narrow Marchfolk > Aelari (matched): +4.2 %;
- Skarn > Grask at 218 / 229: +14.4 / +17.2 %.

Under the section reading the Marchfolk and Skarn knee series are monotonic after the reverts:
- MF configuration 1: 0.0734 → 0.0696 → 0.0666;
- MF configuration 2: 0.0697 → 0.0661 → 0.0607;
- SK configuration 1: 0.0857 → 0.0794 → 0.0789.

## 6. Grask W2C bodies

**Unchanged; no contradiction.** All 21 Grask W2C bodies keep their construction:
- the stature series;
- final frames GRN5 / GRB2 and the frame probes;
- GR-BODY-10…18;
- composition.

The Grask exact-plane knee runs smoothly from 198 to 239 cm (slope −0.451, residuals ≤ 0.8 %). Narrow / Broad move the knee −2.6 / +3.6 % by section.

The W2C knee flags were slab artifacts:
- the knee continuity reversal;
- the 198 / 208 knee "−10 to −13 % off slope";
- the skin knee ÷ femur reversal, which also comes from a ±1 cm slab.

Grask comparisons that used the reverted Marchfolk 203 / Skarn 229 bodies change only in report-only knee rows. The proportion rows are identical.

## 7. Final residual list for Grask W2C

| Status | Item |
|---|---|
| PROVISIONAL (author) | AD-3 floor, Gorrund side, pending Gorrund W2. Grask 198 GO-P3 pending a matched-height Gorrund |
| Accepted boundary outcome (author ruling) | Fixed-reference W1 rows at 229 / 239 cm: GR-P6 drift, GR-G1, lower-leg, forearm. Reference-state relations; validated at the central construction |
| Carried diagnostic | Narrow arm-tube contact (1 vertex / side, non-penetrating) |
| NOT DEMONSTRATED | Narrow Grask derived span vs Broad Skarn (+0.5 %) |
| MARGINAL (PV-D10) | GR-G1 within +1 % of MF at some t on GR-BODY-10 / 11 / 12 / 17 / 18 |
| Station effect | 239 cm thorax-maximum level jump (level 7 reading continuous) |
| CONSTRAINED | GR-G2 scapula (no landmark) |
| Method limit | Generator fat macro weak; lower-leg target at the generator maximum |
| NOT RUN | GR-FACE-14 |
| Cross-project (identified, not Grask) | Elf W1 wrist / ankle thin rows to re-check before elf W2 (§4). The remaining SK 229 knee residual +4.0 % (§3) |

## 8. Recommendation

**ACCEPT** final Grask W2 closure. The AD-3 Gorrund side stays provisional by the author's ruling.

**For the author:**
1. Confirm the four knee-only reverts (§5) and the kept Marchfolk 190 configuration-2 knee.
2. Confirm exact-plane knee as the knee-breadth standard going forward. Elbow, wrist and ankle stay on the slab, with the documented offsets.
3. Accept Grask W2.

Gorrund W2, Sagekin W2, GR-FACE-14 and creator-envelope work are not started.

STOP.

— Claude
