# RAC W1m — Aelari W1 Author-Acceptance Gate

**Author:** Claude **Date:** October 7, 2026
**Author ruling (October 7, 2026; GitHub Issue #1, final Aelari author ruling comment (2026-10-07T15:23Z)):** ACCEPTED — AEL1 is the Aelari W1 central reference (thigh 0.9875 / calf 1.0523). Torso share below MF accepted (no rebudget); leg-evenness row and ±0.010 tolerance accepted for W1; Sagekin overlap and high muscle + fat accepted. Thin margins and Fenn / Vael dependencies recorded; dependent rows to be re-checked after those bodies are accepted. Aelari W1 is closed. The analysis below is unchanged.
**Order:** GitHub Issue #1, final author ruling comment (2026-10-07T14:57Z): "Proceed to the next locked Wave 1 body: AELARI." Recorded in `reviews/chatgpt-rac-w1l-grask-order-issue1-record.md`.
**Evidence:** `reviews/rac-w1m-ae-evidence/` (`tables.md` holds every number quoted; `README.md` maps the files)
**Construction record:** `tools/rac/w1/cfg/w1m/AE.json`

**Comparators:**
- accepted MF-M-R, SK, SG, Gorrund (W1i/W1j) and Grask (W1l);
- Fenn and Vael as built in W1g. They are not yet accepted, so the rows comparing against them depend on bodies still under review.

Nothing here is accepted. Specs and `STATUS.md` are untouched.

## Recommendation: CONSTRAIN — one canon relation fails on the current Aelari; a bounded correction (AEL1) passes everything

**First checks:**
- The as-built Aelari geometry matches its construction record: build scales equal `cfg/w1g/AE.json`, sha256 880b4f0b…
- Re-checked against the current, accepted comparators, the as-built body passes every existing row: 11 / 11 skeletal (CIB), 20 / 20 directional, 11 / 11 skin.

**The finding: one canon relation had no row.** The canon says legs elongate evenly ("even elongation through thigh and lower leg", "Elongation spread evenly, not one extremely long segment"; AELARI L58, L167).
- The arm has a matching row (forearm ÷ upper arm ≈ MF ± 0.010). The leg never had one.
- Measured the same way, the as-built Aelari **fails**: lower leg ÷ thigh is 1.002 vs MF 1.067.

| Segment | Aelari vs MF | Stature for reference |
|---|---|---|
| Thigh | +15.9 % | +9.7 % |
| Lower leg | +8.8 % | +9.7 % |

All of the extra leg is in the thigh; the shin grows less than stature (tables §1–§2).

**Bounded correction: candidate AEL1** (thigh 0.9875, calf 1.0523; knee lowered):
- moves femur length into the lower leg;
- leaves total leg length, hip height, stature (190.01 cm) and every vertical share unchanged, so the tight Aelari vertical budget is untouched.

**AEL1 result:**
- **Leg evenness:** lower leg ÷ thigh 1.0675 vs MF 1.0673, PASS.
- **Every other row:** 11 / 11 skeletal, 20 / 20 directional, 11 / 11 skin, with the same margins as before (§2).
- **Frames:** its Narrow and Broad bodies pass everything, including their own skeletal rows.
- **Low composition** passes all 5 same-composition rows.
- **A milder split, AEL2,** misses the band (1.0558).

**I recommend AEL1** as the Aelari central reference. Choosing between AEL1 and the as-built body is the author's call; I have not replaced the body.

**No accepted canon needs to be challenged.** Two interpretation points and one visual point are for the author (§4).

## 1. Central body: canonical relations (tables §3.1–3.2)

| Group | Rows | As built | AEL1 | Thinnest margin (AEL1) |
|---|---|---|---|---|
| Pelvis E-A2, PV-D3/D5/D6, AE-P6 (FN, VA and MF comparisons), VA-P2a (skeletal CIB) | 11 | PASS | PASS | — |
| Elongation and limb rows: neck > FN and > MF, neck ÷ torso > VA, torso > FN, arms and legs > MF, forearm ÷ upper arm ≈ MF | 8 | PASS | PASS | VA leg < AE +1.14 %; torso > FN +1.17 %; neck > MF +1.19 % |
| **Leg evenness: lower leg ÷ thigh ≈ MF (± 0.010), new row** | 1 | **FAIL (1.002 vs 1.067)** | **PASS (1.0675)** | — |
| Gracility: shallow ribcage, elbow, wrist and knee < MF; VA deeper ribcage, joints and palms | 9 | PASS | PASS | VA palms +1.33 % |
| Hands, feet, face: hand > MF, foot > MF, FVB > MF | 3 | PASS | PASS | foot +1.25 % |
| Skin diagnostics | 11 | PASS | PASS | — |
| Ears (W1i; head unchanged): tip more upward and backward than FN, taper earlier than VA | — | PASS | PASS (same head) | — |
| Ocular (W1h): globe fits the orbit (2.42 cm) | — | PASS | same head | — |

**The thin margins (1.1–1.3 %) are the known Aelari vertical budget** (W1h §6). They are unchanged, and the author ruled them acceptable without shrinking the head (W1i order §10).

## 2. Vertical elongation: how it is distributed (tables §2)

Shares of stature, with Aelari's difference from MF:

| Segment | Aelari | MF | Aelari vs MF | Fenn vs MF |
|---|---|---|---|---|
| Head | 0.1314 | 0.1300 | **+1.1 %** | −2.5 % |
| Neck | 0.0554 | 0.0547 | **+1.3 %** | −2.4 % |
| Torso | 0.2741 | 0.2834 | **−3.3 %** | −4.4 % |
| Leg | 0.5442 | 0.5321 | **+2.3 %** | +3.4 % |
| Arm | 0.4155 | 0.4072 | **+2.1 %** | +5.5 % |

- **Not uniform scaling.** A scaled MF would match MF on every share. Aelari differs in every segment, and the head, neck and limbs all gain share.
- **More distributed than Fenn.** Fenn concentrates on the limbs and loses head and neck share; Aelari gains head and neck share.
- **The face is longer:** FVB +5.9 % over MF.
- **The torso is longer in absolute terms but loses share** (§4.1):
  - +6.1 % in cm over MF, against stature +9.7 %;
  - longer than Fenn relative to height (canon AE > FN: +1.17 %);
  - the longest waist transition (waist interval ÷ torso 0.275, above MF, Fenn and Vael).
- **The neck is construction-shortened** (neck bone ×0.925, W1g budget) yet stays above MF and Fenn.

## 3. Separation and variants

**Separation** (`separation.json`; tables §6; `sheets/ae_separation_lineup.jpg`). Aelari's difference from each body:

| Reading | MF | SG | Fenn | Vael | SK | Grask |
|---|---|---|---|---|---|---|
| Head share | +1.1 % | +2.5 % | +3.7 % | +1.7 % | +5.0 % | +6.2 % |
| Neck share | +1.2 % | +2.5 % | +3.6 % | +1.6 % | +3.4 % | +10.1 % |
| Torso share | −3.3 % | −1.0 % | +1.2 % | −2.0 % | −7.3 % | +3.2 % |
| Leg share | +2.3 % | +0.5 % | −1.1 % | +1.2 % | +3.8 % | −3.4 % |
| Arm share | +2.1 % | −0.5 % | −3.3 % | +0.8 % | +3.3 % | −3.6 % |
| Thoracic depth | −9.3 % | −5.5 % | −2.9 % | −11.4 % | −15.5 % | −0.7 % |
| Thoracic breadth | −7.9 % | −6.5 % | −2.8 % | −7.2 % | −10.9 % | +2.8 % |
| Knee ÷ femur | −9.0 % | −5.7 % | −4.2 % | −6.4 % | −9.7 % | +14.0 % |
| Face FVB | +5.9 % | +5.8 % | +6.1 % | +6.1 % | +5.7 % | +2.2 % |

- **Marchfolk and Skarn:** separated on every axis.
- **Fenn:** Aelari has the longer torso and neck, Fenn the longer limbs and hands, as canon requires (AE L114–115).
- **Vael:** Aelari is shallower and more gracile, with longer legs and neck, as required.
- **Grask (accepted):** Grask is limb-dominant (+3–4 % limbs) with a shorter torso and neck and heavier joints. Aelari is vertically distributed. This is not "thicker Aelari" (GRASK L105).
- **Sagekin:** limb shares overlap (leg +0.5 %, arm −0.5 %). Separation is carried by:
  - thorax: shallower −5.5 %, narrower −6.5 %;
  - joints: gracile −1.5 to −6.6 %;
  - face (+5.8 %), head and neck share (+2.5 %), and ears.

  Canon AE L183 ("never read as the tallest end of human customization") is a visual test with no numeric row (§4.3).
- **Ears:** the renders show bodies without attached ears. Ear-family rows are W1i (PASS).

**Frames** (`sheets/ae_frames_4view.jpg`; tables §3.3–3.4). These use the same diagnostic convention as Grask: the Broad Skarn write (+8 % breadth, +4 % depth, +5 % robusticity) and its mirror. Aelari has no authored frame magnitudes.
- Narrow and Broad each pass 11 / 11 skeletal (own CIB), 20 / 20 directional, 11 / 11 skin and leg evenness.
- Visually both stay vertically elongated. Broad gains real skeletal breadth (AE L49, L125).

**Composition** (`sheets/ae_composition_4view.jpg`; tables §3.5–3.9, §4–§5):
- **Same composition** (low 0.25 / 0.25 vs MF / SK low): 5 / 5 pelvic rows pass. Whole-trunk readings sit with the references: hip ÷ thorax 1.008 vs MF 0.996 / SK 0.984; waist rise 1.11 vs 1.11 / 1.11.
- **The other composition bodies** were scored against *reference-composition* comparators, not like for like. Their skin FAILs are listed in the tables and are diagnostic.
- **Minimum composition** (generator muscle 0 / weight 0): waist ÷ thorax 0.673 and waist rise 1.51 sit at the MF / SG minimum-composition readings (0.681–0.686 / 1.50).
- **Visual:** the high muscle + fat body (1 / 1) is heavily muscled with broad deltoids. Canon: "Broad muscular Aelari never become narrow/lean Skarn" (AE L184, L497). The low-muscle body shows the generator's soft low-muscle belly. See §4.4.

## 4. For the author

1. **Torso share below MF.** Aelari's torso is longer than MF in cm (+6.1 %), longer than Fenn relative to height and has the longest waist transition, all as canon states. Its share of stature is 3.3 % *below* MF.
   - Canon states no AE-vs-MF torso relation; RAC-04 has AE > FN only.
   - If "elongation distributed through the … torso" is meant to require torso share ≥ MF, the budget cannot supply it. The extra 0.009 of stature would push the leg share (0.535) below Vael's (0.538), breaking the accepted chain AE leg > VA leg > MF leg. Shrinking the head / neck share is the option the author already deferred.
   - Reported as an interpretation point, not a failure.
2. **The leg-evenness row.**
   - The row is new.
   - It is derived from canon and uses the arm row's ± 0.010 convention, but the tolerance is a method choice.
   - The author may confirm it, or rule that "even" means something else.
3. **Sagekin overlap.** Limb shares overlap Sagekin. Separation rests on thorax, joints, face, head and neck, and ears. The lineup sheet is the evidence for the visual call.
4. **High muscle + fat visual.** The same generator behaviour was accepted for Grask; Aelari needs its own ruling.

## 5. Construction values

The values below are in `cfg/w1m/AE.json`. They are construction values, not anatomy.

**Hand-set bone scales:**
- pelvis Y / Z 1.07 / 1.06;
- spine_01 length 1.08;
- upper thorax 0.9704;
- neck 0.925;
- foot 1.005;
- legs: thigh / calf 1.0199 / 1.0199 as built, 0.9875 / 1.0523 in AEL1.

**Generator targets:** all within 0.1–0.6 of range; none at a bound. Height macro 0.5625.

There are no solver search bounds.

## 6. Residuals

| Status | Items |
|---|---|
| **FAIL** | As-built only: leg evenness (§1). None on AEL1 |
| **Thin (1.1–1.3 %, accepted budget)** | VA leg < AE, torso > FN, neck > MF, foot > MF, VA palms |
| **Diagnostic** | Composition-variant skin rows (not like for like). AE low-composition forearm ÷ upper arm ≈ MF reads FAIL on skin. The skeleton is AEL1's, so this is a measurement-layer effect of tissue on joint detection |
| **Dependency** | Fenn and Vael are not yet accepted. Rows comparing against them (torso > FN, neck > FN, AE-P6, PV-D5 / D6, VA rows) would need re-checking if those bodies change |
| **NOT RUN** | AE-02 / AE-03 statures (168 / 221 cm), AE-24 combined-proportion stress, AE-39…44 neutralization tests with ears hidden as a formal row, and named frame / composition bodies as authored. All are W2. Also the arm-clearance run on Aelari and an ocular re-check (head unchanged) |

## 7. Canon statement

**No accepted canon needs to be challenged.**
- The leg-evenness failure belongs to the as-built construction, and AEL1 fixes it inside the canon.
- The torso-share point is an interpretation question. If the author wants torso share ≥ MF, that would conflict with the accepted leg chain within the current head share.

No comparator body was changed. No other race was touched. No UE5, topology, rigging, animation, equipment, gameplay or class work was done.

## 8. Recommendation

**CONSTRAIN.** The as-built Aelari fails the canon's even-leg elongation once it is measured.

AEL1 is the bounded correction: femur length moved to the lower leg, with leg length and every vertical share unchanged. It passes every row on the central body, both frames and the same-composition low body.

**For the author:**
1. Accept AEL1 as the Aelari W1 central reference (recommended), or keep the as-built body.
2. Rule on the torso-share interpretation (§4.1).
3. Rule on the leg-evenness row and its tolerance (§4.2).
4. Visual rulings on the Sagekin overlap and the high muscle + fat body (§4.3–4.4).

Vael is not started.

STOP.

— Claude
