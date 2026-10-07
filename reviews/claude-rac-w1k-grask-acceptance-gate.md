# RAC W1k — Grask W1 Author-Acceptance Gate

**Author:** Claude **Date:** October 7, 2026
**Order:** `reviews/chatgpt-rac-w1-remaining-bodies-continuation-order.md` §2–§4
**Evidence:** `reviews/rac-w1k-gr-evidence/` (`tables.md` holds every number quoted here; `README.md` maps the files)
**Comparators:**
- accepted MF-M-R and SK;
- the accepted Gorrund point (W1i/W1j) in the GO slot;
- Broad Skarn, a frame write on the accepted SK.

Nothing here is accepted. Specs and `STATUS.md` are untouched.

## Recommendation: CONSTRAIN — one construction question for the author; everything else passes or is a disclosed limit

**What passes.** The central Grask (GR-BODY-01, 218.0 cm, W1h geometry unchanged) passes every canonical row on the central reference against the accepted comparators:
- **Skeletal (CIB):** 15 / 15.
- **Directional:** 30 / 30, each beyond 1 %.
- **Skin diagnostics:** 12 / 12.

**Distinct from Skarn and Gorrund without stature.** Against Gorrund at 217.0 cm and Broad Skarn at 215.1 cm (§3), Grask has:
- a shorter torso share (−9 to −12 %);
- longer legs (+6 to +8 %);
- longer arms (+7 % vs Broad Skarn, +16 % vs Gorrund);
- a narrower thorax (−14 to −19 %);
- forearm and finger emphasis (+7 %, +13 %);
- lighter joints than Gorrund (−14 to −21 %).

**The problem is a record error I found in the construction.**
- The W1g and W1h records state that Grask's −4 % lumbar narrowing (spine_01 X 0.96) was removed. The delivered W1h geometry still carries it. It is the body every W1h–W1j sheet showed.
- I rebuilt the documented construction, without that narrowing. It **fails two accepted pelvic rows**: bitrochanteric ÷ crest ≥ MF (GR-P2b, −1.15 %) and pelvis ÷ thorax ≈ MF (GR-P6).
- Pelvis width alone cannot recover both. Across pelvis X 0.92–1.05, GR-P6 passes only at ≤ ~0.96, while GR-P2b needs ≥ ~1.02 (§2).
- So the central body's pelvic passes depend on that narrowing. It acts directly on the bony crest reading: crest ÷ stature is 0.1357 with it and 0.1383 without.
- GR-P5 says crest breadth must come from torso proportioning, "never of a narrowing operation on a human pelvis". GR-P5 itself passes either way; the crest stays 7.8–9.6 % under MF. But how the pelvic rows are being satisfied is an author question.

**Smallest bounded corrective pass I recommend** (the order's §4 asks for one on CONSTRAIN). Not started:
- Remove the lumbar narrowing, as the records say.
- Restore GR-P2b through the hip apparatus, not the pelvis. That is hip-joint spacing or proximal-femur construction, which GR-P2b itself names ("hip apparatus proportioned to the long femora").
- Re-run the pelvic, girdle and directional rows, the frames, composition and renders.
- Do not touch any other value.

**The alternative** is to accept the as-built body, recording spine_01 X 0.96 as a CONSTRAINED construction value.

**No accepted canon needs to be challenged** under either option.

## 1. Canonical relations tested (central GR-BODY-01; tables §2.1)

| Group | Rows | Result | Thinnest margin |
|---|---|---|---|
| Pelvis GR-P2a / P2b / P4 / P5 / P6 (skeletal) | 6 | PASS | GR-P2b +0.65 %; GR-P6 0.969 vs MF 0.964 (±0.010) |
| Girdle GR-G1 (glenohumeral and acromial, skeletal) | 2 | PASS | +0.46 % (shoulder-joint ÷ TB ≤ MF) |
| Large-race rows with GR as comparator (RM-LR-02 a / b / d, AD-G6, AD-G7, GO-P2b, GO-P3; skeletal) | 7 | PASS | GO-P3 +1.62 % |
| Proportions: torso, leg, arm, span, forearm ÷ arm, lower leg ÷ leg, vs MF and SK | 12 | PASS | lower leg ÷ leg vs MF +1.39 % |
| Hands: finger ÷ palm vs MF and SK | 2 | PASS | +12.7 % |
| Thorax: TB ÷ H < SK; TD never Durrim-like; SK > GR; GO > GR depth | 4 | PASS | — |
| Joints GO > GR (elbow, wrist, knee) | 3 | PASS | — |
| Face: FVB and MVI vs MF and SK; FPI ≈ MF | 5 | PASS | FPI 0.1437 vs 0.1435 |
| Gorrund-vs-Grask proportion rows | 4 | PASS | — |
| Ears (W1i): late taper, folded cartilage, Gorrund tip < Grask | 3 | PASS | — |

Skin diagnostics: 12 / 12 PASS. The thinnest is GR-G1 skin at +1.03 %.

The two non-strict pelvic and girdle rows (≥ / ≤) sit within 1 % of the reference. They pass under the AD-G10 rule.

## 2. Construction finding (tables §2.2; `probe/pelvis_probe.json`; `cfg/w1h/GR.json` correction note)

| Build | spine_01 X | pelvis X | GR-P2b (≥ MF 1.1992) | GR-P5 (≤ MF 0.1500) | GR-P6 (≈ MF 0.9640 ± 0.010) |
|---|---|---|---|---|---|
| **As built (W1h geometry)** | 0.96 | 0.985 | 1.2069 PASS | 0.1357 PASS | 0.9691 PASS |
| Documented construction | 1.00 | 0.92 | 1.1586 FAIL | 0.1342 PASS | 0.9585 PASS |
| ″ | 1.00 | 0.95 | 1.1712 FAIL | 0.1361 PASS | 0.9720 PASS |
| ″ | 1.00 | 0.985 | 1.1854 FAIL | 0.1383 PASS | 0.9877 FAIL |
| ″ | 1.00 | 1.02 | 1.1992 T-SENSITIVE | 0.1405 PASS | 1.0034 FAIL |
| ″ | 1.00 | 1.05 | 1.2107 PASS | 0.1424 PASS | 1.0169 FAIL |

**Cause.** The W1h build script applied only the pelvis override on a base that still carried spine_01 0.96 (`w1h_drivers/grfin.sh`). So the W1h pelvis re-tune to 0.985 was made with the narrowing present. The tooling record now carries a correction note; the earlier gate text is unchanged.

**What it looks like.** The trunk crop (`sheets/gr_trunk_crop.jpg`) shows the as-built and documented bodies almost identical. The narrowing matters to the bony crest reading, not to the silhouette.

**Other construction values at a bound:**
- **Generator lower-leg length target `measure-lowerleg-height-incr` 1.0 is at the generator's maximum.** It carries the lower-leg emphasis, the thinnest proportion margin at +1.39 % vs MF. The other generator targets are at 0.05–0.6 of range.
- Pelvis X 0.985, spine_01 0.96 and clavicle Y 0.98 are hand-set; there is no search bound. These remain construction values, not anatomy.

## 3. Variants (order §2)

### Frames

**Construction.** GR-BODY-04 Narrow and -05 Broad; `sheets/gr_frames_4view.jpg`, tables §2.8–2.9.
- Broad uses the accepted Broad Skarn frame write: +8 % skeletal breadth, +4 % thoracic depth, +5 % long-bone robusticity.
- Narrow uses its mirror image.
- This is diagnostic construction. Grask has no authored frame magnitudes.
- Stature does not change (217.9 / 218.1 cm), and limb lengths do not change.

| Body | Not PASS |
|---|---|
| Narrow | GR-G1 shoulder-joint ÷ TB ≤ MF **T-SENSITIVE** (−0.54 % at one t); span ÷ stature vs MF and vs SK **NOT DEMONSTRATED** (+0.88 / +0.89 %; span includes shoulder breadth, which the Narrow write lowers) |
| Broad | GR-G1 shoulder-joint ÷ TB **MARGINAL** (skin; skeletal rows pass) |

**Visually,** both frames stay long-limbed and short-torsoed. Broad does not read as Skarn or Gorrund. Narrow is slender but not fragile.

### Composition

**Construction.** GR-BODY-06 low muscle, -07 high muscle, -08 higher fat, -09 high muscle + fat, plus low composition at 0.25 / 0.25; `sheets/gr_composition_4view.jpg`, tables §2.3–2.7, §4–§5.
- These are the central skeleton with generator tissue at that composition. The skeleton is unchanged, so every skeletal row is the central body's.
- Their skin rows are scored against MF, SK and GO at *reference* composition. That is not like for like and is diagnostic only. Those rows show GR-P6 skin FAIL on all five bodies, plus:
  - GR-BODY-06: AP pelvic depth;
  - GR-BODY-07: GR-P2b;
  - GR-BODY-09: AD-G7 (−0.29 %) and elbow;
  - low composition: GR-G1 MARGINAL.

**Like-for-like check at the same composition** (Grask low vs MF and SK low, §5):
- 6 / 7 skin rows pass.
- GR-P6 skin fails (0.768 vs 0.864).
- The whole-trunk readings sit with the references: hip ÷ thorax 1.018 vs MF / SK 0.996 / 0.984, waist ÷ thorax 0.814 vs 0.804 / 0.806.
- The single GR-P6 reading therefore looks like a skin-station effect. It is a diagnostic either way.

**Minimum-composition skeleton** (the sheet shows a pinched waist):

| Reading | Grask | Accepted MF / SG / SK skeletons |
|---|---|---|
| waist ÷ thorax | 0.707 | 0.681–0.731 |
| waist rise | 1.45 | 1.40–1.50 |

It lies inside the accepted range, so it is the generator's minimum-composition shape, not a Grask defect. GR-P6 gives Grask no waist direction.

**Visual review for the author** (canon fail conditions, GRASK L99–L101, L271):
- **Low muscle (-06) and low composition** read as a lean, long-limbed tall figure. Whether they read as "a tall thin human" is the main visual call. The proportion rows that separate Grask from humans are skeletal and unchanged.
- **High muscle + fat (-09)** reads as heavily muscled with broad deltoids. It is the variant closest to "Skarn with longer arms"; check it against the canon.
- **The generator's fat macro is weak:** weight 1.0 moves the surface at most about 2.2 cm from reference. So -08 "higher fat" barely tests the "fat giant / troll belly" rule.
- **Statures shift with composition** (216.4–218.0 cm). That is the generator's macro behaviour, not a skeleton change.

## 4. Girdle, scapula, arm and other named constraints

| Item | Status |
|---|---|
| **GR-G2 scapula** | **CONSTRAINED / NOT DEMONSTRATED.** The rig has no scapula bone and no scapular landmarks; none was invented (AD-W1H-11) |
| **GR-G3 hanging-arm clearance** | 0 upper-arm vertices inside a closed trunk section and 0 trunk vertices inside the arm tube. Smallest gap 0.72 cm (MF 1.15, SK 2.50). Armpit band **NOT DEMONSTRATED** (method cannot test it). Frames not tested |
| GR-G4 clavicle, GR-G5 neck | Visual only (sheets). No row exists |
| Hands and feet | Finger ÷ palm passes. Five digits, plantigrade, as generated. Foot rows are not authored (RM-LR-07 P2 hand ratios reported above) |
| Craniofacial | FVB, MVI and FPI pass. GR-FACE-14 (projection extreme) is W2, **NOT RUN** |
| Ears | Family rows pass (W1i). Envelope (RM-UF-02) is later work |
| Surface | Neutral matte. No hair or skin-colour dependence. No row |

## 5. Queue items naming Grask (RMQ)

| Item | What this evidence supports |
|---|---|
| **RM-LR-01** | Central shares reported (tables §2.1, §3). Envelopes need W2 bodies |
| **RM-LR-02** | Rows (a) and (b) with SK and GO, (d) and (e) GR-G1, AD-G6, AD-G7: all PASS. SK-vs-GR thoracic depth is report-only (undetermined by canon) |
| **RM-LR-04** (AD-3 floor) | **NOT RUN.** Needs GR-BODY-10 (short-limbed Grask, W2). The central body exceeds Gorrund limb contribution by 8 % (legs) and 16 % (arms) |
| **RM-LR-05** joints | GO > GR passes (skin measurement layer). SK-vs-GR is undetermined by canon |
| **RM-LR-07, RM-CF-07, RM-CF-10** | Central readings in tables. No envelopes |
| **RM-CF-03, RM-UF-02, RM-UB-01/02/03/06** | Later work (W2 extremes, envelopes) |

## 6. Residuals

| Status | Items |
|---|---|
| **FAIL** | None on the central body. GR-P2b and GR-P6 fail only on the documented construction (§2). The composition-variant skin FAILs are not like-for-like (§3) |
| **MARGINAL** | Broad GR-G1 (skin). Low-composition GR-G1 (skin) |
| **T-SENSITIVE** | Narrow GR-G1 skeletal shoulder-joint ÷ TB |
| **NOT DEMONSTRATED** | GR-G2 scapula. Armpit band. Narrow span vs MF / SK. **Span vs Broad Skarn at matched height (+0.76 / +0.88 %):** Broad Skarn's wider shoulders offset Grask's longer arms in the derived span; arm ÷ stature still separates them by +7 % |
| **NOT RUN** | GR-BODY-02 / -03 statures; GR-BODY-10…18 extremes and combinations, including RM-LR-04; GR-FACE-14; frame arm clearance; ocular re-check |
| **Construction** | Lumbar narrowing record error (§2). Lower-leg target at generator maximum. Frame writes borrowed (Broad Skarn) and mirrored |

## 7. Comparator dependencies

- **MF-M-R and SK:** all pelvis and girdle rows, proportions, face and hands.
- **Accepted Gorrund point:** AD-G6, AD-G7, RM-LR-02 (a) and (b), and the joint and proportion orderings.
- **Broad Skarn:** used only in §3 and the frame write.
- **SG and DU:** the DU thoracic-depth row and the skeleton range.

No comparator body was changed.

## 8. Canon statement

**No accepted canon needs to be challenged.** The open question is construction, not canon: how Grask's crest-level breadth is built. Either way the body stays inside GR-P1…P6 as written.

No other race was changed. No UE5, topology, rigging, animation, equipment, gameplay or class work was done.

## 9. Recommendation

**CONSTRAIN.** The central Grask meets every canonical relation tested, and it is distinct from Skarn and Gorrund on proportions at matched height.

**For the author:**
1. Choose one:
   - (a) accept the as-built body with spine_01 X 0.96 recorded as a CONSTRAINED construction value; or
   - (b) authorize the bounded corrective pass in the recommendation (lumbar narrowing removed, GR-P2b restored through the hip apparatus).

   I recommend (b), because GR-P5 forbids a narrowing operation.
2. Visual rulings on the low-muscle and high-muscle-plus-fat bodies (§3).
3. Whether the span-vs-Broad-Skarn NOT DEMONSTRATED is acceptable given the +7 % arm separation, since span includes frame-driven shoulder breadth.

STOP. Aelari is not started.

— Claude
