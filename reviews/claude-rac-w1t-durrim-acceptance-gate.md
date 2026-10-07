# RAC W1t — Durrim W1 Author-Acceptance Gate

**Author:** Claude **Date:** October 7, 2026
**Author ruling (October 7, 2026; GitHub Issue #1 final Durrim ruling (2026-10-07T21:18Z); reviews/chatgpt-durrim-final-acceptance-rac-w2-kickoff-order.md):** DURRIM W1 ACCEPTED — DU-NAT as built; Durrim frame rule breadth-only with Broad pelvis x1.08; structural-mass axis closed; palm depth vs CG is report context; palm share MARGINAL; 122/107 cm proxies diagnostic only; DU-P4 at 152 cm OPEN/CARRIED to W2. RAC W1 CLOSED. The analysis below is unchanged.
**Order:** `reviews/chatgpt-halvren-final-acceptance-durrim-w1-order.md`, the same text as GitHub Issue #1 comment 2026-10-07T19:28Z.
**Evidence:** `reviews/rac-w1t-du-evidence/` (`tables.md` holds every number quoted)
**Construction record:** `tools/rac/w1/cfg/w1t/DU-NAT.json`

Nothing here is accepted. Specs and `STATUS.md` are untouched.

## Recommendation: accept DU-NAT as built (137 cm) — no central correction; Durrim-specific Broad frame

DU-NAT carries Compact Structural Concentration on every authored Durrim relation against MF, and the short-race dependencies now close against the accepted Pipkin (PK-NAT) and Cogling (CGJ7).

| Group | Result (DU vs MF unless stated) |
|---|---|
| Torso / limbs | torso +4.6 %, leg −2.9 %, arm −2.4 % (−22.7 % absolute), hip-joint height −2.9 % |
| Thorax / shoulders | thoracic breadth +16.4 %, depth +20.9 %; shoulder-joint breadth +12.0 %; skeletal thorax breadth / depth +15 % / +22 % (t = 0) |
| Pelvis (skeletal, all t) | DU-P2b hip spacing +12.7 %, DU-P3 pelvic vertical ÷ crest −18.9 %, DU-P4 AP depth +8.1 %, DU-P5 crest +13.5 %, DU-P6 crest ÷ thorax −1.5 % (thorax-led) — all PASS |
| Long bones / joints | S7 femoral section breadth / depth +12.8 % / +14.5 %; elbow / wrist / knee / ankle ÷ stature (scaled slab) +8.1 / +23.7 / +13.5 / +6.3 % |
| Hands / feet | hand +13.9 %, palm breadth +13.3 %, palm depth +13.6 %, foot breadth +16.5 %, foot length +3.5 % (moderate) |
| Neck / head | neck −14.7 %; head share +9.3 % over MF but −6.2 % under Pipkin (no fantasy-dwarf head) |
| Structural-mass axis | **CG < PK < DU at all four joints** (scaled slab) and on femoral S7 breadth and depth, every t |
| Rows | skin 6 / 6, directional 16 / 16, added 41 / 43 scored |

**The two non-PASS rows:**
- **Palm share of hand length ≥ MF: MARGINAL (−0.03 %).** This is a provisional tendency (DURRIM L126).
- **Durrim vs Cogling palm depth ÷ stature: −2 % (FAIL as measured; −0.4 % with a stature-scaled palm slice).** Cogling's hands are canonically emphasized, so this is a hand-size question, not a structure one. The structural hand distinction holds on wrist (+32 %), palm breadth ÷ hand (+4.7 %) and foot breadth (+13 %). Hand-bone probes (×1.06 in either cross axis) do not move palm depth (0.0236 → 0.0238 / 0.0233), so no bounded skeletal write fixes it. I recommend no correction; author call.

**No accepted canon is challenged.**

## 1. Short-race dependencies closed (order items 3, 5–7; tables §2)

| Case | Result |
|---|---|
| Pipkin vs Durrim (central) | thorax depth +20.5 %, breadth +17.8 %, leg −2.7 %, arm −4.1 %, hands +5.9 %, palm +4.2 %, foot breadth +10.4 %, neck −14.4 %; thorax-led DU vs pelvis-led PK (crest ÷ thorax −11.1 %) |
| Cogling vs Durrim (central) | thorax +22.7 % / +21.0 %, leg −3.7 %, arm −4.2 %, palm breadth ÷ hand +4.7 %, foot breadth +13 %, neck −14.1 % |
| **Broad Pipkin vs Narrow Durrim** (item 6) | 12 / 13: depth +19 %, crest ÷ thorax −12 %, leg −2.7 %, arm −4.1 %, joints +1–21 %, hands, feet, neck all separate. **Thoracic breadth converges (−0.1 %)** — breadth convergence alone, which the order accepts |
| **COG-BODY-10** Broad high-muscle Cogling vs Narrow Durrim | 14 / 14 (thorax depth +22 %, upper arm ÷ arm +14 %, forearm ÷ arm −11 %, finger ÷ palm −13 %, joints +12–39 %) |
| **COG-BODY-10A** Cogling 107 cm beside Durrim 122 cm | 14 / 14 |
| **SR-COMP-03** Pipkin / Durrim at 122 cm | 13 / 13 |

**Method note (items 7, 9):** the 122 cm Pipkin and 107 cm Cogling are built on their accepted native routes. Those use girth β = 1.0, so trunk and limbs scale together and only hands, feet and head follow allometry. They are diagnostic proxies, not authored maximum-height bodies. The Durrim side uses its own allometric route. I recommend carrying authored maximum-height Pipkin / Cogling bodies to W2.

## 2. 152 cm equal-height boundary (item 8; permanent test)

DU, MF and SG were built at 152 cm on the native short-adult route. The generator's own height macro is excluded below ~159 cm because of its implausible femur (`native_short_allometry.json`). No body uses uniform scale.

| DU152 vs | Passing | Non-PASS |
|---|---|---|
| MF152 | 17 / 18 | **AP pelvic depth ÷ stature −1.6 % (skin)** |
| SG152 | 17 / 18 | **AP pelvic depth ÷ stature −1.0 % (skin)** |

All other separations hold at 152 cm: neck −14 %, torso +5 %, leg −2.2 %, thorax +10 % / +11 %, shoulders +12 %, crest +4.7 %, hip spacing +4.5 %, thorax-led, hands +11 %, palm +10 %, feet +16 %, joints +2–18 %.

**Skeletal DU-P4 at 152 cm (canon reading, PV-D16): NOT DEMONSTRATED (+0.8 %, all t).** Every other skeletal Durrim row passes against the matched MF152 grid.

I did not propose a correction. Pelvis depth probes (pelvis Z ×1.04 / ×1.06) move the skin pelvic-depth reading non-monotonically at both 137 and 152 cm (`probes.json`), so no clean bounded lever exists.

Sagekin at 152 keeps its longer legs (+1.5 % vs MF152). Its narrower ribcage is NOT DEMONSTRATED (−0.7 %); that is a Sagekin row, reported.

## 3. Frames (item 11)

| Frame | Rows | DU-P6 thorax-led (skeletal, t = 0) |
|---|---|---|
| Narrow (−8 % breadth) | all Durrim minimums kept: thorax, crest, hip spacing, depth, joints (skin and skeletal) | PASS |
| **Broad, pelvis ×1.08 (Durrim rule, recommended)** | all pass | 0.951 vs MF 0.965 — PASS |
| Broad, pelvis ×1.12 (elf / short-race rule) | all pass except | **MARGINAL** (0.966 vs 0.965) |

**Durrim-specific frame rule:** breadth only (clavicle Y, spine_01–03 X, pelvis X at the same ±8 %); depth, joints and long bones untouched. The ×1.12 hip-apparatus rule came from the elves' E-A2 relation, which Durrim do not have, and it weakens thorax-led DU-P6. Hip spacing still rises on Broad (+22 % over MF).

## 4. Composition (item 10)

- **Same-composition low (DU-LOW vs MF-LOW, SK-LOW, PK-LOW, CG-LOW):** every row passes except the same two hand rows as the central body. Low composition remains Durrim.
- **Composition bodies:** low muscle, high muscle, higher fat, high muscle + fat. Scored against reference-composition comparators, the skin pelvic rows wobble (high muscle: AP depth and crest ÷ thorax), which is composition mismatch; the skeleton is identical. See `sheets/du_composition_4view.jpg` for the "no comic dwarf" visual call.

## 5. Adult read and head (items 13, 14)

| Reading | DU vs 137 cm child proxy (age ~9 y) |
|---|---|
| Face ÷ bizygomatic (FVB) | +13.6 % (adult face) |
| Thoracic depth | +19 % |
| Hands | +21 % |
| Crest ÷ thorax | −12 % |
| Head share | −1.7 % |

Head share is close to the 9-year-old's. It is allometric (the native head factor plus the authored head-breadth target) and stays below Pipkin's. **Flag for the visual call** (`sheets/du_adult_read.jpg`).

## 6. Residuals

| Item | Status |
|---|---|
| DU vs CG palm depth | −2 % as measured; structural hand distinction carried by wrist, palm breadth ÷ hand and feet; no skeletal lever |
| Palm share of hand | MARGINAL (provisional tendency) |
| DU-P4 at 152 cm | skeletal NOT DEMONSTRATED (+0.8 %); skin −1.6 %; no clean lever |
| Pelvic depth ÷ thoracic depth | 0.71 vs MF 0.80 (skeletal, report): the deep thorax outruns the pelvis; DU-P4 itself passes centrally |
| Head share vs child proxy | close (−1.7 %); adult read carried by face, thorax, hands, pelvis |
| 122 / 107 cm proxies | Pipkin / Cogling proxies on girth β = 1.0 routes; authored maximum-height bodies are W2 |
| NOT RUN (W2) | named frame / composition stress, SR-COMP-04…12 beyond the cases above, movement |

## 7. Canon statement

**No accepted canon was challenged.** No correction was made; DU-NAT is unchanged. No accepted comparator was touched. No UE5, topology, rigging, animation, equipment, gameplay or class work was done.

## 8. For the author

1. **Central:** accept DU-NAT as built (recommended).
2. **Frames:** accept the Durrim breadth-only rule with Broad pelvis ×1.08 (not ×1.12).
3. **152 cm DU-P4:** accept NOT DEMONSTRATED (skeletal +0.8 %) as a carried residual, or order further pelvic work.
4. **DU vs CG palm depth:** accept as a hand-size, not structure, difference (no correction).
5. **122 / 107 cm proxies:** accept as diagnostic, with authored maximum-height Pipkin / Cogling bodies in W2.

This is the last W1 body. Wave 2 remains gated.

STOP.

— Claude
