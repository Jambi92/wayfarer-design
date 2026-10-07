# RAC W1n — Vael W1 Author-Acceptance Gate

**Author:** Claude **Date:** October 7, 2026
**Order:** GitHub Issue #1, final Aelari ruling comment (2026-10-07T15:23Z), "NEXT: proceed to VAEL". Recorded in `reviews/chatgpt-rac-w1l-grask-order-issue1-record.md`.
**Evidence:** `reviews/rac-w1n-va-evidence/` (`tables.md` holds every number quoted; `README.md` maps the files)
**Construction record:** `tools/rac/w1/cfg/w1n/VA.json`

**Comparators:**
- accepted MF-M-R, SK and SG;
- accepted Aelari (AEL1), Gorrund and Grask;
- Fenn as built (W1g), an unaccepted dependency, as ordered.

Nothing here is accepted. Specs and `STATUS.md` are untouched.

## Recommendation: CONSTRAIN — four canon-derived rows fail on the current Vael; a bounded correction (VAL4) passes them

**First checks:**
- The as-built Vael geometry matches its record: vertices identical to the W1g evidence file, build scales equal to `cfg/w1g/VA.json`.
- Against the accepted comparators it passes every row run before: 8 / 8 skeletal (CIB) and 14 / 14 directional.
- Of 8 skin rows, 7 pass. The eighth is the long-known skin pelvic-depth diagnostic (−1.4 %, AD-W1G-12).

**Rows the canon states but no pass had run.** I tested them with the conventions the author accepted for Aelari (VAEL L37, L44–47, L145; tables §1):

| Canon | Reading | As built | MF | Result |
|---|---|---|---|---|
| "balanced femur and lower leg" (L46) | lower leg ÷ thigh | 1.0248 | 1.0673 | **FAIL** (thigh-heavy, as Aelari was) |
| "balanced upper arm and forearm" (L44) | forearm ÷ upper arm | 1.0371 | 1.0491 | **FAIL** (just outside ± 0.010) |
| Joints "gracile compared with humans" (L37, L145) | wrist ÷ forearm | 0.2182 | 0.2116 | **FAIL** (+3.1 %) |
| ″ | ankle ÷ lower leg | 0.3501 | 0.3454 | **FAIL** (+1.4 %) |
| Arms "less extreme elongation than … Aelari" (L44) | arm ÷ stature vs AE | −0.75 % | — | NOT DEMONSTRATED; accepted under BM-3 (MF < VA < AE within 1 %) |

The arm case has almost no room to satisfy both sides beyond 1 %. Aelari's arm share is only 2.0 % above MF, so "Vael arm > MF and < AE, each beyond 1 %" leaves a window of about 0.0001.

**Bounded correction, candidate VAL4.** Four changes:
1. Femur length moved into the lower leg (thigh 0.98849, calf 1.02981).
2. Upper-arm length moved into the forearm (0.99414 / 1.00565).
3. Wrist, ankle and knee circumference lightened, using the generator's own joint targets (wrist 0.35, ankle 0.10, knee 0.05).

These leave unchanged:
- leg and arm length, hip height and stature (178.00 cm);
- every vertical share, so the **accepted Aelari leg budget is untouched** (VA leg 0.5380);
- the trunk, pelvis, head and tissue.

**VAL4 result:**
- **Both balance rows pass:** lower leg ÷ thigh 1.0676, forearm ÷ upper arm 1.0491.
- **Joints are gracile against Marchfolk:**

| Joint | VAL4 vs MF |
|---|---|
| Wrist | −3.3 % |
| Knee | −1.1 % |
| Ankle | −1.4 % |
| Elbow | −2.6 % |

- **They keep more presence than Aelari and Fenn**, as canon requires: wrist +1.8 % over AE, ankle +1.3 %, knee and elbow larger.
- **Other rows:** skeletal 8 / 8, directional 14 / 14, added rows 15 / 15 (arm < AE NOT DEMONSTRATED under BM-3).
- **Every Aelari row that compares against Vael still passes,** so the accepted Aelari is not disturbed.

**I recommend VAL4** as the Vael central reference. Choosing between VAL4 and the as-built body is the author's call; I have not replaced the body.

**Main visual question: Vael vs humans.** Body-wise, Vael sits close to Marchfolk on most readings (§3). The order's "deeper, more compact-continuity" organization is real but mainly *relative to the other elves*. That is how the canon writes it: VA-P4 sets "≈ MF" as the minimum, and "Vael > MF is not authored".

**No accepted canon needs to be challenged.**

## 1. Central body (tables §3.1, §3.5)

| Group | Rows | As built | VAL4 | Thinnest margin (VAL4) |
|---|---|---|---|---|
| Pelvis E-A2, PV-D6, VA-P2a, AE-P6 mirror (skeletal CIB) | 8 | PASS | PASS | AP depth > FN +1.46 % |
| Directional rows involving VA, incl. accepted-AE rows (leg < AE and < FN, torso > FN, deeper ribcage, broader palms, joint presence > AE / FN, neck ÷ torso < AE) | 14 | PASS | PASS | leg < AE +1.14 %; palms > AE +1.33 %; wrist > AE +1.78 % |
| **Added: limb balance (2), joints gracile vs MF (4), ankle > AE / FN, feet broader than AE / FN, arm > MF, arm < FN, Fenn ≥ Vael neck ÷ torso, AE leg budget, arm < AE (BM-3)** | 15 | **4 FAIL**, 1 ND | **PASS**, 1 ND (BM-3) | knee gracile +1.06 % |
| Skin diagnostics | 8 | 7 PASS, AP depth ≥ MF −1.4 % | same | — |
| Report only: hip- and shoulder-joint *spacing* | 5 | — | — | These readings are spacing, not joint size, so they cannot test "joint presence" or VA-P2c |

**VA-P1, natural lumbar curve** (`sheets/va_trunk_lumbar_crop.jpg`, side panel). The lordosis is present, not neutralized, and reads like MF's, not exaggerated. This satisfies the author's PV-D7 (a) on a visual check; there is no numeric row.

**Head, face, eyes and ears** are unchanged from W1g / W1i:
- ear rows (broader base, more lateral and backward) PASS in earlier passes;
- landmark globe 2.45 cm fits.

## 2. Distribution and compact continuity (tables §2, §5)

**Vael against the other elves** (shares of stature):

| Reading | Vael | Aelari | Fenn |
|---|---|---|---|
| Leg | 0.5380 | 0.5442 | 0.5504 |
| Torso | 0.2797 | 0.2741 | 0.2710 |
| Neck ÷ torso | 0.195 | 0.202 | 0.197 |
| Thoracic depth | 0.1356 | 0.1202 | 0.1237 |
| Waist interval ÷ torso | 0.268 | 0.275 | — |

Every canon direction holds:
- shorter legs than Fenn and Aelari;
- a longer torso share than Fenn (+3.2 %);
- a shorter neck relative to the torso than Aelari;
- a deeper thorax than Aelari (+12.9 %) and Fenn (+9.6 %), which "compact continuity" requires;
- a shorter waist interval than Aelari.

**Trunk profile (skin):** hip ÷ thorax 0.964 and waist rise 1.094, between MF (0.946 / 1.083) and Fenn (0.985 / 1.112). It is continuous with no step-in. The minimum-composition skeleton (waist rise 1.50) sits with MF / SG.

## 3. Separation (`separation.json`; tables §6; `sheets/va_separation_lineup.jpg`)

Vael's difference from each body:

| Reading | MF | SG | Aelari | Fenn | SK | Grask |
|---|---|---|---|---|---|---|
| Leg share | +1.1 % | −0.7 % | −1.1 % | −2.2 % | +2.6 % | −4.5 % |
| Arm share | +1.3 % | −1.3 % | −0.8 % | −4.0 % | +2.5 % | −4.4 % |
| Torso share | −1.3 % | +1.0 % | +2.0 % | +3.2 % | −5.4 % | +5.3 % |
| Thoracic depth | +2.4 % | +6.6 % | +12.9 % | +9.6 % | −4.6 % | +12.1 % |
| Thoracic breadth | −0.8 % | +0.7 % | +7.7 % | +4.7 % | −4.0 % | +10.7 % |
| Elbow / wrist / knee / ankle | −2.6 / −3.3 / −1.1 / −1.4 % | ±0–2.5 % | +1.3 to +8.7 % | +2.5 to +9.9 % | −2 to −22 % | +6 to +24 % |
| Face FVB | −0.2 % | −0.3 % | −5.8 % | 0.0 % | −0.3 % | −3.7 % |

- **Aelari and Fenn:** separated as canon requires. Vael is deeper, more jointed, broader-palmed and shorter-legged. It is not "recolored Aelari" or "shortened Fenn".
- **Skarn and Grask:** separated on every axis. Vael is not compact Skarn. Grask is limb-dominant, Vael compact and deep.
- **Marchfolk and Sagekin:** the body differences are small, mostly within ±3 %:
  - against MF: slightly longer limbs, slightly deeper thorax, slightly lighter joints;
  - against SG: deeper thorax (+6.6 %) and broader palms (+5.4 %), with limbs overlapping.

  Canon "Vael never become human" (L190, L532) therefore rests on the face (stronger midface, broader cheeks and orbits), the ears and the jointed-but-gracile elven limbs. The renders show bodies without ears.

## 4. Variants

**Frames** (tables §3.7–3.10; `sheets/va_frames_4view.jpg`).

*Borrowed Broad Skarn write* (as used for Grask and Aelari): ±8 % breadth, ±4 % thoracic depth, ±5 % limb robusticity.
- **It misreads Vael.** The −4 % depth on Narrow contradicts VAEL L114 ("A Narrow, lean Vael keeps it"). The ±5 % robusticity pushes Vael's joints out of their narrow canon window.
- **Narrow:** skeletal AP depth > FN NOT DEMONSTRATED; joints fall below Fenn and Aelari.
- **Broad:** joints exceed MF; E-A2 MARGINAL.

*Breadth-only write* (±8 % skeletal breadth; depth and robusticity unchanged; diagnostic):
- **Narrow passes everything:** 8 / 8 skeletal, 14 / 14 directional, 15 / 15 added. As on the central body, arm < AE stays NOT DEMONSTRATED (BM-3) and the skin AP-depth diagnostic remains.
- **Broad fails E-A2** bitrochanteric ÷ crest ≥ MF on the skeleton (1.1855 vs 1.1992, −1.1 %). Same mechanism as Grask: the breadth write widens the lumbar / crest level without widening the hip apparatus.
- **This is a frame-construction finding, not a central-body defect.** A Broad Vael must carry the hip apparatus with the crest so that E-A2 holds across frames (E-A3).

**Composition** (tables §3.11–3.15, §4; `sheets/va_composition_4view.jpg`):
- **Same composition** (low 0.25 / 0.25 vs MF / SK low): 3 / 3 pelvic rows pass. AP depth ≥ MF *passes* here (0.1292 vs 0.1273): Vael's depth survives low composition, as canon requires.
- **Trunk:** hip ÷ thorax 1.018 vs MF / SK low 0.996 / 0.984.
- **Other composition bodies** are scored against reference-composition comparators, not like for like. Their joint and pelvic skin rows move with tissue, so those results are diagnostic.

## 5. Construction values

Recorded in `cfg/w1n/VA.json`. They are construction values, not anatomy.

**Hand-set bone scales:**
- pelvis [1.02, 1, 1.03];
- upper thorax 0.9747;
- VAL4 limbs: thigh 0.98849, calf 1.02981, upper arm 0.99414, forearm 1.00565.

**Generator targets:** wrist-circ-decr 0.35, ankle 0.10, knee 0.05. All targets are within 0.05–0.35 of range; none at a bound. Height macro 0.5479.

## 6. Residuals

| Status | Items |
|---|---|
| **FAIL** | As built: limb balance (2), wrist and ankle gracility. VAL4: none. Diagnostic: skin AP depth ≥ MF −1.4 % (known AD-W1G-12; skeleton and same-composition pass). Breadth-only Broad frame E-A2 (frame-construction finding) |
| **NOT DEMONSTRATED** | Arm < AE (BM-3). Borrowed-write Narrow skeletal AP depth > FN |
| **Thin (1.06–1.46 %)** | Leg < AE, palms > AE, knee gracile, AP depth > FN, Fenn ≥ Vael neck ÷ torso, Aelari leg budget |
| **Dependency** | Fenn is not yet accepted. Rows comparing against Fenn (leg < FN, torso > FN, AP depth > FN, joints and palms and feet > FN, arm < FN, neck ÷ torso) to be re-checked after Fenn's pass |
| **Visual / no row** | VA-P1 lumbar curve (render). Separation from MF / SG (mainly face and ears) |
| **NOT RUN (W2)** | VL-02 / VL-03 statures (157 / 203 cm); VL-24 stress; named frame, composition and combined bodies; ears-hidden neutralization as a formal row; arm-clearance run |

## 7. Canon statement

**No accepted canon needs to be challenged.**
- The four failures belong to the as-built construction, and VAL4 fixes them inside the canon and the accepted Aelari budget.
- The arm-vs-Aelari window is narrow by construction of the accepted bodies, and BM-3 already covers it.

No accepted comparator was changed. No other race was touched. No UE5, topology, rigging, animation, equipment, gameplay or class work was done.

## 8. Recommendation

**CONSTRAIN.** The as-built Vael fails four canon-derived rows: leg balance, arm balance, wrist gracility and ankle gracility. VAL4 is the bounded correction. It rebalances limb segments and lightens joints, with lengths, shares, trunk and head unchanged. It passes every row on the central body, the breadth-only Narrow frame and the same-composition low body.

**For the author:**
1. Accept VAL4 as the Vael W1 central reference (recommended), or keep the as-built body.
2. Confirm the added rows (limb balance ± 0.010; joints gracile vs MF beyond 1 %), or rule otherwise.
3. Frame convention: rule whether Vael frames use the breadth-only write. Note that a Broad frame must carry the hip apparatus with the crest (E-A2).
4. Visual ruling on Vael vs Marchfolk / Sagekin, where body separation is small and face and ears carry it.

Fenn is not started.

STOP.

— Claude
