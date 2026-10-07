# RAC W1q — Pipkin W1 Author-Acceptance Gate

**Author:** Claude **Date:** October 7, 2026
**Order:** `reviews/chatgpt-fenn-final-acceptance-pipkin-w1-order.md`, the same text as GitHub Issue #1 comment 2026-10-07T17:19Z.
**Evidence:** `reviews/rac-w1q-pk-evidence/` (`tables.md` holds every number quoted; `README.md` maps the files)
**Construction record:** `tools/rac/w1/cfg/w1q/PK-NAT.json`

**Comparators:**
- accepted MF-M-R, SK, SG, Aelari, Vael, Fenn, Gorrund and Grask;
- **Durrim (DU-NAT) and Cogling (CG-NAT) as built, both unaccepted dependencies;**
- two diagnostic bodies built for this gate: a generator human-child proxy (107 cm) and a breadth-only Narrow Durrim.

Nothing here is accepted. Specs and `STATUS.md` are untouched.

## Recommendation: PASS — central Pipkin sound as built; one canon relation not measurable in the current method

**First checks:**
- The as-built Pipkin (PK-NAT, native short-adult route, 107.0 cm) matches its record: vertices identical to the W1e evidence file, build scales equal to `cfg/w1e/PK-NAT.json`.
- The directional rows read this body: the "PK" and "PK-NAT" measurement files are identical. They do not read the rejected uniform-scale proxy.

**Result on the central body** (accepted comparators, plus Durrim and Cogling as dependencies):

| Layer | Rows | Result |
|---|---|---|
| Skeletal (CIB) | 7 / 7 | PASS |
| Directional | 9 / 9 | PASS |
| Skin diagnostics | 7 / 7 | PASS |
| Added canon-derived rows | 16 / 16 tested | PASS (plus 16 report-only readings) |

**The order's five pelvis-led rows** (skeletal, against MF):

| Row | Margin |
|---|---|
| Pelvic vertical ÷ thoracic vertical > MF | +10.5 % |
| Pelvic vertical ÷ stature ≥ MF | +5.3 % |
| AP pelvic depth ÷ thoracic depth > MF | +6.9 % |
| Crest ÷ thoracic breadth > MF | +7.3 % |
| Waist interval ÷ torso < MF | +5.5 % |

**No correction is needed or proposed.**

**One canon relation cannot be measured: PK-P2b, convergent femora on an adult narrow base.**
- The R-6 measurement stance places each hip joint straight above its knee and ankle by definition (`arm_lib.pose_r6`: "hip joint above ankle (feet at hip width)"). So femoral convergence cannot appear in any R-6 joint reading.
- A mesh reading of leg-section spacing shows Pipkin's knees at 1.084 × hip-joint spacing (MF 1.027, DU 1.086). That reading mixes in thigh soft tissue, so it is report-only.
- A leg-valgus probe (generator knock-knee target, three strengths) did not converge the knees under R-6, and it broke the ankle-vs-Durrim row. It was rejected.
- **PK-P2b is NOT DEMONSTRATED (method).** It needs a render ruling, or a later stance method that keeps natural femoral obliquity (§6.1).

**No accepted canon needs to be challenged.**

## 1. Central body (tables §1, §3.1)

| Group | Rows | Result | Thinnest margin |
|---|---|---|---|
| PK-P2a hip height > DU and ≤ MF; PK-P3, P4, P5, P6; PV-D10 (skeletal CIB) | 7 | PASS | leg share ≤ MF +0.17 % (non-strict); > DU +2.8 % |
| Trunk share < MF (modest); pelvis > thorax vs MF; legs ≤ MF; head share > MF only as allometry; structural-mass axis CG < PK < DU (wrist, knee) | 9 | PASS | — |
| **Pipkin vs Durrim** (dependency): leg share +2.8 %, arm share +4.3 %; thoracic depth −17.0 % and breadth −15.1 %; pelvic vertical ÷ thoracic vertical +29.9 %; crest ÷ thoracic breadth +12.5 %; elbow / wrist / knee / ankle lighter (−12.8 / −19.9 / −19.6 / −3.8 %); palm breadth and depth lighter at matched stature (−4.1 / −1.7 %) | 12 | PASS | palm depth −1.7 % |
| **Pipkin vs Cogling** (dependency): trunk share < CG (−3.2 %); crest ÷ thoracic breadth > CG (+3.7 %); waist interval ÷ torso < CG (−5.5 %); pelvic vertical ÷ thoracic vertical > CG (+10.5 %) | 4 | PASS | — |
| Skin diagnostics | 7 | PASS | — |

**Correction to one of my own rows.** My first palm row tested palm *shape* (palm breadth ÷ hand length) and failed (0.443 vs DU 0.436). But canon PIPKIN L183 reads "**at matched stature**, Durrim hands … stronger palm and wrist presence, while Pipkin hands are more moderate with lighter wrist and palm dimensions". The rows were rewritten to palm breadth ÷ stature and palm depth ÷ stature (both PASS). The shape reading is kept as report-only.

**Head, face, eyes and ears** are unchanged from W1e–W1h:
- head share +16.5 % over MF, accepted as allometry for this W1 candidate (W1d order L88);
- globe kept as constrained adult geometry (AD-W1H-9);
- compact rounded ear family (EA-W2);
- facial vertical ÷ breadth (FVB) +0.7 % over MF, a mature midface.

## 2. Adult, not juvenile (order item 4; child proxy; `sheets/pk_short_race_lineup.jpg`)

The **human-child proxy** is a diagnostic body, not canon: the accepted MF generator with the age macro set to about 6 years and stature re-solved to 107 cm. Pipkin against it:

| Reading | Pipkin vs child proxy | Reads as |
|---|---|---|
| Head height ÷ stature | **−8.3 %** (0.151 vs 0.165) | smaller head share than the child |
| Waist interval ÷ torso | **−22.8 %** | compact adult trunk vs the child's long soft waist |
| Pelvic vertical ÷ stature | **+16.1 %** | mature, vertically substantial pelvis |
| Pelvic vertical ÷ thoracic vertical | **+14.1 %** | pelvis-led |
| Facial vertical ÷ breadth | **+13.0 %** | mature, vertical face |
| Hand / foot share | +11.3 % / +8.0 % | not "childishly small" |
| Leg / arm share | +5.4 % / +5.1 % | adult limb contribution |
| Crest ÷ thoracic breadth | −5.3 % | the generator child's soft hip is wide; Pipkin's pelvis leads through height and depth, not breadth (PK L209) |

At the fixed sheet scale, the two silhouettes are close. The separation rests on the readings above, not on overall outline, so **adult identity at a glance is a visual call** (§6.2).

## 3. Separation (`separation.json`, tables §6)

Pipkin's difference from each body:

| Reading | MF | Durrim | Narrow Durrim (diag.) | Cogling | Fenn |
|---|---|---|---|---|---|
| Torso share | −3.9 % | −8.1 % | −8.1 % | −3.2 % | +0.5 % |
| Leg share | −0.2 % | +2.8 % | +2.8 % | −1.1 % | −3.5 % |
| Thoracic depth | +0.3 % | −17.0 % | −16.6 % | +1.8 % | +7.4 % |
| Thoracic breadth | −1.2 % | −15.1 % | **−7.5 %** | +3.1 % | +3.8 % |
| Pelvic vertical ÷ thoracic vertical | +10.5 % | +29.9 % | +29.9 % | +10.5 % | +7.2 % |
| Crest ÷ thoracic breadth | +9.2 % | +12.5 % | +12.0 % | +3.7 % | +8.1 % |
| Waist interval ÷ torso | −5.5 % | −7.2 % | −7.2 % | −5.5 % | −6.2 % |
| Head share | +16.5 % | +6.6 % | +6.6 % | +16.7 % | +19.6 % |

- **Not a scaled Marchfolk.** The trunk is low-set and compact (torso −3.9 %, waist −5.5 %) and pelvis-led (+9 to +10 %).
- **Not a slender Durrim.** The thorax is far less deep (−17 %), the pelvis leads, joints are lighter, and limbs contribute more.
- **Not a small Cogling.** The trunk share is reduced, the pelvis leads (+3.7 to +10.5 %) and the waist is compact (−5.5 %). Leg segmentation is not used as a separator (COGLING L913).

**Broad Pipkin vs Narrow Durrim** (tables §3.4; `sheets/pk_broad_vs_narrow_du.jpg`):
- Thoracic breadth converges, 0.2033 vs 0.2032, which is what the pairing is designed to produce.
- Every identity row still holds: thoracic depth −16 %, pelvis-led ratios +12 to +30 %, joints −4 to −20 %, limbs +3 to +4 %, palm lighter.
- Skeletal rows pass 7 / 7. Frame breadth does not collapse identity.

## 4. Variants

**Frames** use the accepted breadth-only principle (Vael and Fenn); Broad pelvis ×1.12 so the hip joints follow the crest (`sheets/pk_frames_4view.jpg`).
- Narrow and Broad each pass 7 / 7 skeletal, 9 / 9 directional, 7 / 7 skin and all added rows.
- Continuity:

| Body | hip ÷ thorax |
|---|---|
| Central | 1.021 |
| Narrow | 1.034 |
| Broad | 1.037 |
| MF | 0.946 |

  Both frames stay pelvis-led. Broad does not approach Durrim (0.922).

**Composition** (`sheets/pk_composition_4view.jpg`; tables §3.5–3.9, §4):
- **Same composition** (low 0.25 / 0.25 vs MF / SK low): 6 / 6 pelvic rows pass.
- **Other bodies, scored against reference-composition comparators** (not like for like, diagnostic):
  - low muscle and higher fat pass everything;
  - high muscle and high muscle + fat fail PK-P4 AP-depth ÷ thoracic-depth on skin, because muscle thickens the thorax;
  - one structural-mass axis row moves.
- **Visual:** check the high-muscle bodies against "muscular Pipkin must not become Durrim / Skarn" and the higher-fat body against "never a round-halfling stereotype". On the sheet, high muscle + fat is heavily muscled; higher fat stays slight.

## 5. Construction values

As built since W1e, recorded in `cfg/w1q/PK-NAT.json`. They are construction values, not anatomy:
- native short-adult regional factors;
- pelvis vertical 1.06, spine_01 length 0.9;
- generator hip, torso, wrist and foot targets, all within 0.05–0.4 of range; none at a bound;
- G-S1 globe.

No change was made in W1q.

## 6. For the author

1. **PK-P2b convergent femora (see the Recommendation).** The method cannot measure it, so it is NOT DEMONSTRATED. Accept on render review for W1, or call for a later stance method.
2. **Adult-not-juvenile visual (§2).** The readings separate Pipkin from the child proxy on head share, waist, pelvis, face and extremities. The silhouette call is yours.
3. **Composition visuals:** high muscle + fat (not Durrim or Skarn) and higher fat (not round-halfling) (§4).
4. **Dependencies:** Durrim and Cogling are not accepted. Every Pipkin-vs-Durrim and Pipkin-vs-Cogling row, and the axis rows, must be re-checked after their W1 passes.

## 7. Residuals

| Status | Items |
|---|---|
| **FAIL** | None on the central body or frames. Composition skin rows against reference-composition comparators (diagnostic) |
| **NOT DEMONSTRATED** | PK-P2b femoral convergence (method) |
| **Thin** | PK-P2a leg share ≤ MF +0.17 % (non-strict); palm depth vs DU −1.7 % |
| **Dependency** | Durrim (DU-NAT) and Cogling (CG-NAT) unaccepted: 21 rows involve them (16 added, 4 directional, 1 skeletal) |
| **Diagnostic bodies** | Child proxy (generator age macro); Narrow Durrim (breadth-only write on unaccepted DU) |
| **NOT RUN (W2)** | PIP-BODY-02 / -03 statures; PIP-BODY-14 at about 122 cm (the canon's Broad-PK vs Narrow-DU test height); PIP-BODY-15 / -16 / -28 / -29 as authored; stress bodies; face extremes; arm clearance |

## 8. Canon statement

**No accepted canon needs to be challenged.** The as-built Pipkin meets every measurable canon relation tested. PK-P2b is a measurement-method limit, not a construction failure.

No comparator body was changed. No other race was touched. No UE5, topology, rigging, animation, equipment, gameplay or class work was done.

## 9. Recommendation

**PASS.** The central Pipkin reads as light, compact, adult and pelvis-led against Marchfolk, Durrim, Cogling and a human-child proxy. It needs no correction, and its frames and same-composition low body hold.

**For the author:**
1. Final W1 acceptance of PK-NAT.
2. The PK-P2b ruling (§6.1).
3. Visual rulings (§6.2–6.3).

Cogling is not started.

STOP.

— Claude
