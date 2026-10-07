# RAC W1p — Fenn W1 Author-Acceptance Gate

**Author:** Claude **Date:** October 7, 2026
**Author ruling (October 7, 2026; GitHub Issue #1 final Fenn ruling (2026-10-07T17:19Z); reviews/chatgpt-fenn-final-acceptance-pipkin-w1-order.md):** FENN W1 ACCEPTED — FNL4 central; neck rule = neck / torso (neck / stature secondary); frame breadth rows do not veto Narrow / Broad against unmatched central MF; breadth-only frames, Broad x1.12 acceptable; high muscle + fat acceptable. Aelari / Vael dependency rows pass; accepted elves not reopened. The analysis below is unchanged.
**Order:** `reviews/chatgpt-vael-final-acceptance-fenn-w1-order.md`, the same text as GitHub Issue #1 comment 2026-10-07T16:06Z.
**Evidence:** `reviews/rac-w1p-fn-evidence/` (`tables.md` holds every number quoted; `README.md` maps the files)
**Construction record:** `tools/rac/w1/cfg/w1p/FN.json`
**Comparators:** accepted MF-M-R, SK, SG, Aelari (AEL1), Vael (VAL4), Gorrund and Grask.

Nothing here is accepted. Specs and `STATUS.md` are untouched.

## Recommendation: CONSTRAIN — one canon relation fails on the current Fenn; a bounded Fenn-only correction (FNL4) passes everything

**First checks:**
- The as-built Fenn geometry matches its record: sha256 1495f5a0…, build scales equal to `cfg/w1g/FN.json`.
- Re-checked against the now-accepted elves, plus every canon row not run before, it passes:

| Layer | Rows | Note |
|---|---|---|
| Skeletal (CIB) | 10 / 10 | Includes every accepted-Aelari and accepted-Vael pelvic row against Fenn |
| Directional | 25 / 26 | The 26th is a superseded historical ORB diagnostic, labelled non-vetoing |
| Skin diagnostics | 10 / 10 | — |
| Added canon-derived rows | 20 / 22 | Proportions, hands, feet, thorax, joints vs MF, and more |

**The failure: the elf gracility order** (E-A1, FENN L115; ECR L312–316: "Fenn, then Aelari, then Vael"). Against the accepted Aelari, Fenn's joints read:

| Joint | Fenn vs Aelari | Result |
|---|---|---|
| Wrist | −7.5 % | lighter |
| Ankle | −1.1 % | lighter |
| **Elbow** | 0.332 vs 0.324 (+2.4 %) | **FAIL** |
| **Knee** | 0.275 vs 0.264 (+4.4 %) | **FAIL** |

This is a population-average ordering with overlap (ECR L316), but at the two central references it should hold.

**Bounded Fenn-only correction, FNL4:**
- arm-bone cross-section ×0.95;
- leg-bone cross-section ×0.96;
- generator knee target 0.3 → 0.6.

Bone lengths, stature (181.16 cm), every share, trunk, pelvis, head and tissue are unchanged. No accepted body was touched.

**FNL4 result:** the elbow is 2.0 % lighter than Aelari's and the knee 2.1 % lighter, so the order holds at all four joints. Every other row still passes: skeletal 10 / 10, directional 25 / 26 (the historical diagnostic), skin 10 / 10, added 22 / 22. Two lighter-touch probes did not clear both joints:
- FNL1: arms only;
- FNL3: arms plus a stronger knee target only.

**I recommend FNL4** as the Fenn W1 central reference. Choosing between FNL4 and the as-built body is the author's call; I have not replaced the body.

**No accepted canon needs to be challenged.**

## 1. The elf-family chain (order item 3; `separation.json`, tables §6)

Fenn (FNL4)'s difference from each accepted elf:

| Reading | vs Aelari | vs Vael | Canon |
|---|---|---|---|
| Leg share | **+1.1 %** | **+2.3 %** | Fenn more limb-focused than Aelari; Vael shorter-legged than Fenn ✓ |
| Arm share | **+3.4 %** | **+4.2 %** | ✓ |
| Hand share / finger ÷ hand | +4.2 % / +7.3 % | +3.9 % / +7.4 % | extremity emphasis ✓ |
| Forearm ÷ arm; lower leg ÷ leg | +1.1 %; +1.9 % | +1.9 %; +1.9 % | "slightly longer forearms / lower legs" ✓ |
| Head share / neck share | **−3.6 % / −3.5 %** | −2.0 % / −2.0 % | Aelari more distributed head and neck ✓ |
| Torso share | **−1.2 %** | **−3.1 %** | Aelari and Vael torso > Fenn ✓ |
| Thoracic depth | +2.9 % | **−8.8 %** | Vael deeper ✓; Fenn vs Aelari not ranked |
| Palm breadth ÷ hand | −5.3 % | **−6.5 %** | Vael broader-palmed ✓ |
| Joints (elbow / wrist / knee / ankle) | −2.0 / −9.7 / −2.1 / −1.5 % | −8.1 / −11.3 / −9.9 / −2.8 % | Fenn most gracile ✓ (FNL4) |

The chain is intact:
- Fenn carries the limb and extremity elongation;
- Aelari carries the distributed head, neck and torso elongation;
- Vael stays deeper, more jointed, broader-palmed and shorter-legged.

**Neck: one reading point.** Canon "Aelari > Fenn ≥ Vael in relative contribution" (RAC-03 E-4; ECR L320).
- **neck ÷ torso,** the reading used in every accepted gate: Fenn 0.197 ≥ Vael 0.195, PASS.
- **neck ÷ stature:** Fenn 0.0534 < Vael 0.0545 (−2.0 %).
- "Relative contribution" fits either reading. ECR L320 itself keeps absolute and proportional neck separate. See §6.1.

## 2. Central body: canon rows (tables §1, §3.1, §3.5)

| Group | As built | FNL4 | Thinnest margin (FNL4) |
|---|---|---|---|
| Pelvis: E-A2, FN-P4 AP depth ≈ MF, FN-P5 crest ≈ MF, FN-P6 waist ≥ MF and < AE; accepted AE / VA rows against FN (skeletal CIB) | PASS 10 / 10 | PASS 10 / 10 | FN-P6 ≥ MF +0.57 % (non-strict, known) |
| Proportions: torso < MF; leg > MF and > AE; arm > MF and > AE; lower leg ÷ leg > MF; forearm ÷ arm > MF | PASS | PASS | leg > AE +1.13 %; forearm +1.31 % |
| Hands and feet: hand and finger longer, palm narrower, feet longer and narrower than MF | PASS | PASS | — |
| Thorax shallower and narrower for height than MF | PASS | PASS | — |
| Joints smaller than MF (elbow, wrist, knee, ankle) | PASS | PASS | — |
| **Gracility order vs Aelari (4 joints)** | **2 FAIL** | **PASS** | ankle −1.47 %; elbow −2.0 %; knee −2.1 % |
| Fenn ≥ Vael neck ÷ torso | PASS | PASS | +1.13 % |
| Accepted-elf directional rows (torso, neck, ribcage, palms, joints, leg) | PASS | PASS | Aelari torso > FN +1.17 % (known) |
| Skin diagnostics | PASS 10 / 10 | PASS 10 / 10 | — |

**Head, face, eyes, ears and complexion** are unchanged; FNL4 changes no head geometry.
- Orbit O-1 δ = 0.03 and the ring fit (W1h, clearance 0.75 cm) stand.
- The v2 ears pass 22 / 22 directional rows, including Fenn's greatest lateral projection: +8.7 % over Vael (E-D3).
- "Backward" is not a Fenn > Aelari ranking; Aelari's tip reads more backward (accepted row).
- Complexion stays Fenn-specific; the ARM uses a neutral matte surface.

## 3. Separation (tables §6; `sheets/fn_elf_family_lineup.jpg`)

Fenn's difference from each human comparator:

| Reading | MF | SG | SK |
|---|---|---|---|
| Leg / arm share | +3.4 / +5.5 % | +1.6 / +2.8 % | +5.0 / +6.8 % |
| Hand / finger | +6.8 / +7.5 % | +2.1 / +2.0 % | +2.0 / +6.9 % |
| Torso share | −4.4 % | −2.2 % | −8.4 % |
| Thoracic depth / breadth | −6.6 / −4.8 % | −2.8 / −3.4 % | −13.0 / −8.0 % |
| Joints | −4 to −14 % | −2.6 to −11.1 % | −11 to −31 % |

- **Not a "generic slender human".** Fenn is distinct from MF and SK on every limb, extremity, thorax and joint reading. Against Sagekin the margins are smaller but in the same direction.
- **Grask** (accepted) shares limb and finger emphasis (arm −0.4 %, finger +0.1 %). Canon notes this as valid overlap (GRASK L287, L729): "the distinction survives through overall skeletal scale, joint architecture, torso and pelvis … craniofacial anatomy and ear architecture".
  - Measured: Fenn's thorax is wider (+6.2 %) and deeper (+2.2 %) for height, and its wrist lighter (−6.1 %).
  - Grask's knee is leaner than Fenn's (Fenn +11.6 %).
  - The Grask range (198–239 cm) overlaps Fenn only at the top.

## 4. Variants

**Frames** (tables §3.6–3.8; `sheets/fn_frames_4view.jpg`). These follow the accepted Vael principle: breadth only, no borrowed depth or robusticity write, and the Broad hip joints follow the crest.

| Body | Skeletal | Other rows | Result |
|---|---|---|---|
| Narrow (breadth only) | 8 / 10 | FN-P5 crest ≈ MF fails (skin and skeletal); Aelari pelvic vertical ÷ crest > FN drops to NOT DEMONSTRATED | See below |
| Broad, pelvis ×1.08 | 9 / 10 | E-A2 MARGINAL | — |
| **Broad, pelvis ×1.12** | **10 / 10** | Directional "ribcage narrower than MF" fails (skin) | See below |

The Vael principle carries over to Fenn: pelvis ×1.12 keeps E-A2.

The Narrow crest row and the Broad ribcage row are **central-value breadth relations**: crest ≈ MF, ribcage narrower than MF.
- A Narrow or Broad body differs in breadth by definition, and canon gives Fenn all three frames with no breadth identity (E-A3, FENN L115).
- So these rows aren't like for like against the central MF; a frame-matched MF would be the comparator.
- Reported, not treated as Fenn defects (§6.2).

**Composition** (tables §3.9–3.13, §4–§5; `sheets/fn_composition_4view.jpg`):
- **Same composition** (low 0.25 / 0.25 vs MF / SK low): 5 / 5 pelvic rows pass, including FN-P4 AP depth ≈ MF and FN-P5 crest ≈ MF.
- **Other composition bodies** are scored against reference-composition comparators, not like for like. Their skin FAILs are diagnostic.
- **Minimum composition** waist rise is 1.58, against MF / SG 1.50. Hip ÷ thorax is 1.13, against 1.09.

## 5. Construction values

Recorded in `cfg/w1p/FN.json`. They are construction values, not anatomy.

| Value | Status |
|---|---|
| Pelvis [1.04, 1, 1.04] | As built |
| spine_01 X 1.03 | As built |
| Forearm length 1.005 | As built |
| Arm-bone cross-section 0.95 | **FNL4** |
| Leg-bone cross-section 0.96 | **FNL4** |
| Knee target 0.6 | **FNL4** |

**Generator targets:** all within 0.05–0.7 of range; none at a bound (eye-scale-incr 0.7 is the highest). Height macro 0.5435.

## 6. For the author

1. **Neck reading.** Should "Fenn ≥ Vael in relative contribution" be read as neck ÷ torso (passes; used so far) or neck ÷ stature (Fenn 2.0 % below Vael)? If neck ÷ stature is required, the fix would lengthen the Fenn neck slightly with stature held, a separate bounded pass. I have not done it.
2. **Frame breadth rows.** Confirm that central-value breadth relations (crest ≈ MF, ribcage narrower than MF) are not required of Narrow or Broad frame bodies against the central MF.
3. **FNL4,** and the slightly slimmer limb-bone cross-sections it implies (`sheets/fn_joints_before_after.jpg`).

## 7. Residuals

| Status | Items |
|---|---|
| **FAIL** | As built: gracility order at elbow and knee. FNL4: none. Historical ORB-breadth diagnostic (superseded, non-vetoing) |
| **Interpretation** | Neck ÷ stature vs Vael (§6.1). Frame breadth rows (§6.2) |
| **Thin (1.1–1.9 %)** | Leg > AE +1.13 %, Aelari torso > Fenn +1.17 %, forearm +1.31 %, ankle gracility vs AE −1.47 %, lower leg +1.89 %. FN-P6 ≥ MF +0.57 % (non-strict) |
| **Dependency closure** | All Aelari and Vael rows that waited on Fenn were re-run against the as-built body and FNL4, and all pass. Nothing changes for the accepted Aelari or Vael |
| **NOT RUN (W2)** | FN-02 / FN-03 statures; named frame, composition and combined bodies; ears-hidden body row as a formal test; face extremes; arm clearance |

## 8. Canon statement

**No accepted canon needs to be challenged.** The gracility-order failure belongs to the as-built construction, and FNL4 fixes it inside the canon with a Fenn-only change.

No accepted comparator was changed. No other race was touched. No UE5, topology, rigging, animation, equipment, gameplay or class work was done.

## 9. Recommendation

**CONSTRAIN.** The as-built Fenn fails the elf gracility order at the elbow and knee once it is measured against the accepted Aelari.

FNL4 is the bounded Fenn-only correction: slightly slimmer limb-bone cross-sections and a lighter knee, with all lengths and shares unchanged. It passes every row on the central body, the Broad frame (×1.12) and the same-composition low body. The elf-family chain reads as authored.

**For the author:**
1. Accept FNL4 (recommended), or keep the as-built body.
2. Rulings on the neck reading (§6.1) and frame breadth rows (§6.2).

Pipkin is not started.

STOP.

— Claude
