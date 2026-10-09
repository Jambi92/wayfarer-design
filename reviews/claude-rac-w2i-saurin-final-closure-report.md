# RAC W2I — Saurin Final Closure Report (W2I1)

**Author:** Claude (auditor) · **Date:** October 8, 2026 · **Order:** `reviews/chatgpt-rac-w2i1-saurin-closure-order.md` §1–§15
**Parent gate:** `reviews/claude-rac-w2i-saurin-boundary-gate.md` · **Evidence:** `reviews/rac-w2i-sa-evidence/closure/` (`tables.md` is generated; every number below comes from its JSON files)
**Status:** DESIGN ONLY / NO UE5. NON-CANON diagnostics.
- **No accepted Saurin anatomy changed.** The frozen SA-M (aff1b52) and the §263 SA-F are never written back. J-2 landmarks deform nothing (§3 audit). The carriage test is posture-only and moves no non-tail vertex.
- No other race's body or canon was changed.

## Verdicts

| Item | Verdict | Reason in one line |
|---|---|---|
| **Saurin stature family** | **ACCEPT** | D1 is recorded: the regional route is the accepted W2 measurement / reference construction route. 168 / 188 / 203 / 208 plus the 173 / 178 / 181 / 190 matched bodies are preserved. Nothing new failed. |
| **Saurin axial / pelvic body system** | **ACCEPT** | Unchanged from W2I (lower-trunk floor PASS at 168 / 203). The J-2 pass reads limbs only. |
| **Saurin frame system** | **ACCEPT** | Unchanged (104 / 104). |
| **Saurin composition firewall** | **ACCEPT** | Unchanged (96 / 96). |
| **Saurin tail coupling / RM-UB-04** | **ACCEPT** (one marginal for author confirmation) | Under the same-state rule, the caps on the most permissive base are Balanced 78.4 %, Broad 79.75 %, Narrow 77.1 % and Narrow + high fat 79.1 % H. The ~72 % Narrow + fat anchor passes (+1.78°). Every earlier tail failure is still a failure, now with its cause stated. **Broad 80 % now sits 0.25 points above the reachable Broad cap** (§2). |
| **Saurin limb / joint body validation** | **CONSTRAIN** | J-2 passes the invariance audit and resolves every blocked limb row. **Two canon wordings are contradicted by the as-built limbs:** "moderate-to-long legs" (§4.3) and "modest forearm emphasis" (§4.2). Skeletal-mass rows are a **MEASUREMENT LIMIT** (§4.4). |
| **RM-OT-04** | **ACCEPT** | Unchanged. |
| **RM-UB-08 body portion** | **NAMED DEPENDENCY** | As-built values only; there is no evidence for ranges. RM-UF-04 was not begun. |
| **SAU-SILHOUETTE** | **CONSTRAIN** (not resolved by the permitted lever) | No carriage from 0 to +12° removes the rounded mass seen between the thighs from the front. The best lift (+12°) shrinks the visible extent only from 12.7 to 9.7 cm (§5). |
| **Saurin W2I overall** | **CONSTRAIN** | Everything except limbs and silhouette is accepted. The remaining items are two canon-wording conflicts and one silhouette lever problem. They need author rulings, not builder fixes (§8). |

---

## 1. D1 — recorded (order §2)

The regional stature route is recorded as the **accepted W2 Saurin measurement / reference construction route** (`tools/rac/w1/cfg/w2i/SA-boundary.json` `rulings.D1`):
- vertical *k*;
- girth k^0.654, head k^0.688, hands k^0.842, feet k^0.942;
- isometric tail from the caudal-base landmark (§256.9).

It is **not** the production creator implementation. The Part 7 uniform route remains a historical / diagnostic cross-check. Standing height excludes the tail. 168–208 cm stays the W2 diagnostic biological family, not a production distribution. The future creator must not introduce a visible discontinuity.

The J-2 pass uses this route unchanged: its 26 bodies are the same regional-route builds.

## 2. D2 — same-state tail-cap accounting (order §3)

**Rule (D2(c)).** Δlean = tested body − the **same-stature, same-frame / composition reference**, meaning the same state carrying the reference tail (64.613 % H, base 1.0).
- The frozen SA-M188 comparison is reported second and no longer gates.
- The cap is read on the most permissive admissible base (D2(a): RSI solved to 1.19).
- Constant sufficiency (RSI 1.00) is a report column.
- Driver: `w2i_drivers/sa_tailcap2.py`.

**Reference leans (same state):**

| State | Lean |
|---|---|
| Balanced 188 | 8.82° |
| Broad 188 | 8.00° |
| Narrow 188 | 9.59° |
| Narrow + high fat 188 | 9.84° |
| Balanced + fat 188 | 9.07° |
| Female centre | 8.29° |
| 168 | 8.50° |
| 208 | 9.13° |
| 208 Broad | 8.33° |

**Reachable caps (% H; binding guard always the +3° same-state lean):**

| State | D2(a) cap, RSI 1.19 | Report: RSI 1.00 | W2I value (RSI 1.19, old rule) |
|---|---|---|---|
| Balanced 188 | **78.4** | 75.75 | 78.4 |
| Broad 188 | **79.75** | 77.25 | 79.8 |
| Narrow 188 | **77.1** | 74.5 | 74.4 |
| Narrow + high fat 188 | **79.1** | 76.5 | 75.5 |
| Balanced + high fat 188 | 80.5 | 77.9 | 79.6 |
| Female centre 188 | 79.0 | 76.4 | 79.0 |
| Balanced 168 | 78.9 | 76.4 | — |
| Balanced 208 | 77.9 | 75.4 | — |
| Broad 208 | 79.4 | 76.75 | — |

The bisection resolves caps to 0.125 point.

**What changed under the clarified rule.**
- Narrow and Narrow + high fat caps rise by about 3 points. Those states lean further forward with their own reference tail, so measuring against SA-M188 had penalized them.
- Balanced is unchanged, because its reference *is* SA-M188.
- Broad falls slightly, because Broad stands more upright (8.00° vs 8.82°).
- **Narrow is still the tightest frame** (77.1 %).
- Composition now changes the cap: high fat raises it.
- No production cap function is authored.

**Named / earlier non-pass cases at their recorded bases:**

| Case | Δlean same-state | Δlean vs SA-M188 (secondary) | Result |
|---|---|---|---|
| Balanced 78 % (anchor, base 1.15) | +3.00° | +3.00° | PASS (at the guard) |
| **Balanced 80 %** (rule base 1.22) | +3.78° | +3.78° | **FAIL**, as in W2I. Balanced cap 78.4 % |
| **Broad 80 %** (anchor, base 1.16) | **+3.39°** | +2.57° | **FAIL under the same-state rule** (passed under the old rule) |
| Narrow + high fat 72 % (anchor, base 1.10) | +1.78° | +2.81° | PASS. A reachable point, not the cap (D2(b)) |
| **Narrow + high fat 78 %** (base 1.15) | +3.16° | +4.19° | **FAIL at this base**. At the permissive base the state reaches 79.1 %, so 78 % is reachable with a heavier base |
| **208 cm Broad 80 %** (base 1.16) | **+3.51°** | +3.03° | **FAIL**. Its 208 Broad baseline stands more upright, so the same-state rule is stricter here. The 208 Broad cap is 79.4 % |
| 55 % (base 0.85 / 0.83) | −1.97° / −2.05° | same | PASS |
| 168 cm + 55 % | −1.88° | −2.20° | PASS |

- The low end stays coupled: 55 % **fails A50** (0.50–0.51 > 0.48) on the smallest admissible base in every state. A short tail needs a substantial base (D2(a) wording preserved).
- **Interaction, reported rather than compensated:** under the same-state rule, Broad reaches 79.75 % at 188 and 79.4 % at 208, not a full 80 %. The canon anchor "Broad 80 %" is therefore 0.25 point (188) / 0.6 point (208) above the reachable cap on the uniform-density interim guard.
  - No base or lean value was tuned.
  - Proposed classification: **MARGINAL**, for author confirmation as ACCEPTED MARGINAL (the anchors are "~" values and the guard is interim).

## 3. D3 — J-2 derivation and invariance audit (order §4)

**Sources.** The derivation uses the accepted Saurin construction skeleton:
- the per-side **B1 limb axes** that the accepted Gate 4 and Gate 5 reconstructions were built about and kept;
  - Gate 4 §1: "each leg keeps its own B1 hip–knee–ankle axis";
  - Gate 5 §1: "each arm keeps its B1 shoulder–elbow–wrist axis";
- carried verbatim in `gate1/g7geo.py` `ARM` / `LEG` (the Gate 7 "skeleton references") and `g7.py` `SK`;
- the hand builder's digit-III metacarpal head (`hand.py` `FING[1]`, in the `hand.frame(W, E)` frame) as the MCP point.

The hand and foot claws were built on these same points, and the W2I claw diagnostic reproduces them **exactly**, which confirms the points still sit in the final mesh frame.

**What was not done.** No point was fitted, eyeballed or moved, and no humanoid default skeleton was authored. Driver: `w2i_drivers/sa_joints.py`. Review sheet: `sheets/sa_j2_joints.jpg`.

**Defensibility checks on the frozen SA-M:**
- All 14 points lie inside the closed surface (winding number 0.998–1.002).
- For elbow, wrist, knee and ankle, the exact-plane section through the point **encloses it**. In-plane offset from the section centroid:

| Joint | Offset | Equivalent radius |
|---|---|---|
| Wrist | 0.06 / 0.40 cm | 3.1 / 3.2 cm |
| Ankle | 0.27 / 0.23 cm | 5.2 / 5.3 cm |
| Knee | 0.50 / 0.88 cm | 6.6 / 5.9 cm |
| Elbow | 1.59 / 2.04 cm | 5.0 / 5.3 cm (the posterior olecranon mass shifts the centroid) |

- The construction knee (u 62) sits at the narrow level above the calf (calf maximum u 43–46). The knee fields (condylar flats, extensor sheet) were built there in Gate 4.
- **No joint is UNRESOLVED.**

**Transport.** Each joint is an affine-exact, least-norm combination of an anchor ring of 1,502–3,595 surface vertices (within 1 cm of the joint plane and 12 cm of the point). It reads vertex positions only, in the MakeHuman sense.

**Invariance audit (order §4C):**

| # | Check | Result |
|---|---|---|
| 1 | Source mesh hash / geometry unchanged | V / F SHA-256 identical before and after. Base file SHA-256 identical. The working base equals the frozen `saurin_final_base.npz` (SHA-256 `a925e067…`, arrays identical) |
| 2 | Stature unchanged | 187.881 before = after |
| 3 | Thorax / lower trunk / pelvis / tail unchanged | All 61 `measure()` readings identical (max abs diff **0.0**), including d/w, lower trunk, pelvis, tail %, RSI and A50 |
| 4 | Head / hand / foot unchanged | Head length / depth and foot length identical (same 61 readings). Hand geometry is read, not moved |
| 5 | No transform or pose edit | Every one of the 26 warped bodies hashes identically before and after landmarking |
| 6 | Deterministic and reproducible | Points and weights bit-identical on re-derivation. Affine constraint residual 6e-12 cm. An arbitrary affine map is reproduced to 7e-12 cm |
| — | Transport control | The ring-centroid alternative differs by ≤ 0.41 cm (max over bodies; 0.07–0.33 cm on the family). This is the transport uncertainty |

**The audit passes.** D3 proceeds.

## 4. D3 — limb, joint and S7 readings and validators (order §5–§6)

Definitions are the MPFB `arm_measure.py` ones applied to the J-2 joints:
- segment = joint-to-joint;
- hand = wrist → farthest hand vertex along the wrist → MCP-III axis (claw included, as MPFB includes the nail; claw-excluded value also reported);
- exact-plane joint sections follow the W2C1 `joint_section.py` rule;
- S7 is the exact plane at 20 % of the femur, on the body and on its composition floor (muscle −1 / fat −1), inset 2t for t = 0 / 0.5 / 1.

The comparator sections were recomputed with the same rule. **Control:** Cogling CG91 reproduces the committed W2H `joint_sections.json` values exactly.

### 4.1 Newly resolved rows

**Limb segments and distribution (SA-M188; per-body rows in `tables.md` §2–§3):**

| Reading | SA-M188 | MF190 | Note |
|---|---|---|---|
| Upper arm | 30.7 cm (0.164 H) | 0.148 H | |
| Forearm | 23.5 cm (0.125 H) | 0.150 H | |
| Arm to wrist | 54.2 cm | | |
| Hand | 21.1 cm (0.112 H; 21.0 without claw) | 0.111 H | |
| Total arm | 0.401 H | 0.409 H | |
| Forearm / arm | **0.312** | **0.366** | |
| Hand / arm | 0.280 | | |
| Thigh (femur) | 24.3 cm (0.129 H) | 0.251 H | |
| Shin | 53.0 cm (0.282 H) | 0.248 H | |
| Leg to ankle | 77.3 cm (0.411 H) | 0.499 H | |
| Hip height | 0.458 H (J-2) / 0.484 H (axial station u 91) | 0.537 H | |
| Lower leg / leg | 0.69 | 0.50 | |
| Foot / leg | foot +20–22 % vs matched Marchfolk | | W2I |

**Exact-plane joints (breadth / depth, SA-M188):**

| Joint | Breadth / depth (cm) | Breadth / H | MF190 breadth / H |
|---|---|---|---|
| Elbow | 11.0 / 10.2 | 0.058 | 0.049 |
| Wrist | 8.0 / 4.9 | 0.043 | 0.030 |
| Knee | 16.9 / 10.0 | 0.090 | 0.068 |
| Ankle | 11.5 / 9.6 | 0.061 | 0.077 |

**Long-bone presence and S7:**
- **Long-bone presence (surface sections):** mid-humerus 15.6 cm, mid-forearm 7.4 cm, mid-shin 15.2 cm breadth.
- **Femoral S7 (composition floor, t = 0.5):**
  - breadth 0.078 H, against Marchfolk 0.067, Gorrund 0.092 and Durrim 0.079;
  - **depth 0.135 H, against Marchfolk 0.062 and Gorrund 0.094.**

**Stature behaviour.** Across 168–208, the limb ratios are flat to within about 1 %. Joint and segment-section shares fall slightly with the girth allometry. Female centre:
- legs 1.2 % shorter in share, because §263 lengthens the lower trunk;
- forearm / arm unchanged.

### 4.2 SAU-BODY-11 limb portion — Marchfolk-normalized (real matched height, 168–203, M and F)

**Total arm** is close to Marchfolk (0.394–0.403 H vs 0.407–0.410). This fits "moderate total arm contribution".

**Forearm.** Forearm / arm is **0.311–0.312 against 0.362–0.371**, i.e. **15 % below** Marchfolk at every matched height. The Saurin arm is upper-arm-dominant (forearm / upper arm 0.76).
- §17's "forearms *may* carry somewhat greater proportional contribution than Marchfolk" is permissive and not breached.
- But the identity statement (SAURIN L3602, "moderate arm length with modest forearm emphasis") is **contradicted** by the as-built arm.
- Exact humerus / forearm ratios remain OPEN in canon (L302). This is surfaced for the author; nothing was retuned.

**Hand.** Hand / H 0.110–0.114 ≈ Marchfolk (0.111–0.114). Non-human hand identity is carried by digit, claw and pad architecture, not length (report).

**Skeletal presence.** Joint and shaft surface sections are larger than Marchfolk's (elbow / H +20 %, wrist +42 %, knee +32 %). (SA-M188 vs MF190.) This fits "moderate-to-substantial skeletal presence" directionally. It is a **REPORT** only, because skin sections are not bone (§4.4).

### 4.3 Hip station vs "moderate-to-long legs" (order §6 watch item) — **CONTRADICTED**

Every available leg reading puts the Saurin legs **shorter** than Marchfolk at real matched height, and shorter than Durrim in share:

| Reading (share of H) | Saurin (168–208) | Marchfolk (matched) | Durrim DU137C |
|---|---|---|---|
| Hip height, J-2 construction hip | **0.450–0.459** | 0.529–0.546 | 0.517 |
| Hip height, authored axial station u 91 (the most favourable Saurin definition) | **0.477–0.486** | (same) | (same) |
| Hip-to-ankle leg length | **0.405–0.413** | 0.487–0.504 | 0.474 |

**Vertical budget at matched height** (SA-M188 vs MF190):

| Segment | Saurin | Marchfolk |
|---|---|---|
| Ground → hip | 0.484 (station) | 0.537 |
| Hip → costal (LT1) | 0.170 | 0.130 |
| Costal → vertex | 0.345 | 0.334 |

**Reading.**
- The elongated lower axial trunk is paid for almost entirely by the legs.
- That contradicts SAURIN L970: "paid for primarily through modestly reduced vertical head/thoracic contribution rather than by forcing shortened legs".
- It also contradicts "moderate-to-long legs / leg contribution" (L258, L526, L3599) if read against the Marchfolk tendency.
- Within the leg, the construction knee is high: the femur is 0.129 H and the shin 0.282 H.
- The two hip definitions differ by 5 cm, but **even the most favourable gives −8 to −12 %** versus matched Marchfolk. The result does not depend on the landmark choice.
- **Disposition: CONTRADICTED.** As ordered, no anatomy was retuned. It is surfaced as **D-A** (§8).

### 4.4 Structural-mass rows — **MEASUREMENT LIMIT** (order §5 "classify correctly")

**Why.**
- The MPFB skeletal proxies are generator skeletal envelopes: minimum composition, muscle 0 / weight 0.
- The rig-less Saurin mesh has no skeletal envelope. Its composition floor removes at most 0.45 + 0.35 cm and keeps the canonical **caudofemoral system** on the posterior thigh (Gate 1 / Gate 4).
- So the Saurin S7 depth (0.135 H) and the joint sections measure musculature plus bone.
- These surface sections are reported, **not scored as skeletal mass**.

**Raw directions, surfaced rather than hidden.** At 208, Saurin limb surface sections exceed Gorrund's: elbow / H +20 to +37 %, wrist +15 to +25 %, knee +12 to +32 %, S7 depth +32 to +40 %.
- S7 breadth (9 / 9 rows) and ankle section (3 / 3) stay below Gorrund.
- Saurin joint surface sections also exceed Durrim's.
- On the visual sheet (`sheets/sa_vs_gorrund_208.jpg`, W2I) the Saurin limbs are sinewy and muscular, not bone-massive.
- This becomes a **named dependency**: a Saurin internal skeletal model is needed before "substantially lower skeletal mass" (L529) can be scored.

### 4.5 Validator closure

| Validator | Disposition |
|---|---|
| **SAU-BODY-11** limb portion | Axial PASS (W2I). Limb: total arm moderate; **forearm emphasis CONTRADICTED** (§4.2); **legs CONTRADICTED** (§4.3); skeletal presence REPORT / MEASUREMENT LIMIT |
| **SAU-BODY-13** vs Grask (matched 208 + GR218 normalized) | **PASS** on global limb readings: arm / H 0.399–0.404 vs 0.432, leg 0.41 vs 0.52, hip height 0.46 vs 0.56. One marginal: Broad 208 span (2 × arm + shoulder joints) / H 1.061 vs 1.055 (+0.6 %), caused by the Broad frame's lateral shoulder offset; Saurin arm length stays below Grask. **MARGINAL** (sub-1 %). Upper-arm share exceeds Grask (+9–10 %) but is a segment reading (REPORT) |
| **SAU-BODY-14** vs Gorrund (joint portion) | **MEASUREMENT LIMIT** (§4.4); the interim never-Gorrund guard PASS stands (W2I) |
| **SAU-BODY-15** vs Cogling | **PASS** (28 / 28). Forearm / arm 0.31 vs 0.39 and (forearm + hand) / arm 0.59 vs 0.71: no Cogling distal redistribution. Joint and S7 surface sections exceed Cogling's (not fine), but that part is surface-based (report) |
| **SAU-BODY-16** vs Durrim | Length rows **FAIL**: hip height / H −11 to −13 % and leg length / H −13 to −14 % below Durrim, i.e. the same leg contradiction (§4.3, D-A). Arm / H ≈ Durrim (−0.4 to +0.8 %, NOT DEMONSTRATED / one sub-1 % FAIL). Joint-mass rows MEASUREMENT LIMIT (§4.4) |

## 5. D4 — neutral-carriage test (order §7–§9)

**Lever.** The accepted carriage parameter only (`tail_curv`). It rotates the free-tail centreline distal to the caudal base, with the angle growing toward the tip. Driver: `w2i_drivers/sa_carriage.py`; sheets `sheets/sa_carriage_M188.jpg`, `_F188.jpg`, `_M208.jpg`, each with full front / profile / rear 3/4 plus a close straight-front pelvis view and the same view from 12° below.
- **+12° lies outside the validated §256.8 range** (+8° lift … +10° droop). It was tested once, as ordered, and not extended.

**Invariance, verified in every state.**
- Caudal-base point unchanged (shift 0.0).
- No non-tail vertex moves (≤ 1e-7 cm), so stance, pelvis and legs are unchanged.
- Tail length, root area, volume, RSI, taper, A50 / A25 / A75 and mass share change ≤ 0.018 %.
- No tail drag: lowest tail point 60–79 cm above the ground.
- Δlean ≤ +0.03°: "carriage changes clearance and reach, not balance" holds.

**Measurements (front thigh gap, SA-M188):**

| Lift | Visible extent below crotch | Gap share covered | Max visible width | Lowest tail point | Tip height | Distal elevation |
|---|---|---|---|---|---|---|
| 0° | 12.7 cm | 6.3 % | 14.8 cm | u 67.6 | u 80.2 | 12.5° |
| +4° | 11.7 | 5.7 % | 14.6 | 68.6 | 84.2 | 16.2° |
| +8° | 10.7 | 5.0 % | 14.2 | 69.7 | 88.1 | 19.8° |
| +12° | 9.7 | 4.4 % | 13.6 | 70.7 | 92.1 | 23.5° |

The same pattern holds for 168 cm (11.1 → 8.1 cm), 208 cm (20.6 → 16.6), the 78 % tail (17.7 → 13.7), the 55 % tail (9.7 → 7.7) and SA-F (18.0 → 15.0).
- The female and 208 extents are larger partly because the crotch rule lands on the perineal surface rather than the inner thigh on those bodies.
- Width and lowest point are the robust readings.

**Qualitative findings (renders).**
- In all four states the straight-front view still shows **a dark, rounded, centrally suspended mass between the thighs**. It shrinks only marginally. The view from 12° below makes it more pendulous.
- **Root continuity:**
  - no kink (root tangent change ≤ 1.4°);
  - the root path still reads sacral origin → posterior projection → caudal sweep in profile;
  - no new "raised flag" look up to +8°;
  - at +12° the distal tail starts to tilt up (23.5° distal elevation) without becoming a flag.

**Cause (measured, `sa_carriage.py` source trace).**
- The tail leaves the pelvis almost horizontally at crotch height and runs straight back.
- In the straight-front orthographic view it is seen **end-on**: the visible patch is made of tail vertices from the whole free tail (median 45 cm from the tip at 0°), not a local bulge.
- Its tapered cross-section (~14 cm wide) projects as a disc whose lower edge lies 10–13 cm below the crotch.
- `tail_curv` lifts mostly the distal tail (the rotation grows toward the tip). The mid-tail underside that forms the disc rises only 1 cm per 4°.

**Disposition: SAU-SILHOUETTE CONSTRAIN — not resolved by the permitted lever.**
- No natural carriage in the tested range removes the ambiguity, so **no carriage candidate is recommended** (+8° is not proposed as canon).
- No arbitrary larger lift was tested.
- Root anatomy, pelvis, tail length / thickness and the caudal base were not touched. → **D-C** (§8).

## 6. Tail-cap regression (order §10)

The order makes this conditional on a recommended carriage. None is recommended, so for information only the D2 run was repeated at **+8°** (`tailcap2_lift8.json`; states Balanced, Broad, Narrow + fat 188 and Broad 208):

| Case | Δlean same-state at 0° | Δlean same-state at +8° | Result |
|---|---|---|---|
| Balanced 78 % | +3.00° | +3.00° | PASS |
| Balanced 80 % | +3.78° | +3.78° | FAIL |
| Broad 80 % | +3.39° | +3.39° | FAIL |
| Narrow + fat 72 % | +1.78° | +1.78° | PASS |
| Narrow + fat 78 % | +3.16° | +3.16° | FAIL |
| 208 Broad 80 % | +3.51° | +3.51° | FAIL |
| 55 % | −1.97° | −1.97° | PASS |

**Caps at +8° (RSI 1.19 base):** Balanced 78.5 %, Broad 79.75 %, Narrow + fat 79.1 %, Broad 208 79.4 %. These are identical to 0° within the 0.125-point bisection step.

**Carriage does not interact with RM-UB-04 inside ±8°.** The coupling system is unaffected.

## 7. Complete non-pass accounting (order §13)

| Item | Classification |
|---|---|
| TL Balanced 80 % FAIL (+3.78°; same under both references) | **REPORT-ONLY** (correct CONSTRAIN: Balanced cap 78.4 %); stands as the canon "80 % not an entitlement" result |
| TL Narrow + high fat 78 % FAIL at base 1.15 (+3.16° same-state; +4.19° old reference) | **RESOLVED BY D2** (cap read on the permissive base, 79.1 %; 78 % reachable with a heavier base) |
| TL 208 Broad 80 % (+3.03° old reference; **+3.51° same-state**) | **MARGINAL** (208 Broad cap 79.4 %), with Broad 188 80 % (cap 79.75 %; +3.39° at base 1.16). Proposed ACCEPTED MARGINAL — **D-B** |
| Balanced 78 % at +3.00° | REPORT (at the guard) |
| Low end 55 % fails A50 on the smallest admissible base | **RESOLVED BY D2** (D2(a) wording: valid only with a substantial base) |
| Muscle + fat RSI 0.763; §263 clamps d/w 0.999 / 1.000; Narrow + B 3.0 / Narrow + fat + B 1.6 guard excess | REPORT-ONLY (W2I accepted in principle) |
| Absent joint measurements (limb segments, distribution, exact-plane joints, S7, long-bone presence; SAU-BODY-13 / 15 / 16; limb / joint portions of 11 / 14) | **RESOLVED BY D3** (J-2, audit passed; every row now measured) |
| Moderate-to-long legs (hip height / leg length below Marchfolk and Durrim) | **UNRESOLVED — canon wording conflict** (CONTRADICTED; D-A) |
| SAU-BODY-16 leg / hip share rows FAIL vs Durrim | **UNRESOLVED** (same conflict, D-A) |
| Modest forearm emphasis (forearm / arm −15 % vs Marchfolk) | **UNRESOLVED — canon wording conflict** (D-A) |
| SAU-BODY-16 arm share vs Durrim (−0.4 … +0.8 %) | REPORT-ONLY (near equal; canon names shortened limbs, which the legs carry) |
| SAU-BODY-13 Broad 208 span +0.6 % vs Grask | **MARGINAL** (sub-1 %; frame shoulder offset), proposed ACCEPTED MARGINAL — D-B |
| SAU-BODY-14 / 16 joint-mass and S7 rows; S7 depth | **MEASUREMENT LIMIT** (no skeletal envelope; caudofemoral tissue) + **NAMED DEPENDENCY** (Saurin internal skeletal model) |
| Upper-arm share > Grask; knee / femur and other per-segment joint ratios | REPORT-ONLY |
| SAU-SILHOUETTE | **UNRESOLVED** (carriage lever insufficient; D-C) |
| RM-UB-08 numeric field ranges | **NAMED DEPENDENCY / INSUFFICIENT EVIDENCE** |
| RM-OT-04 OPEN facial rows; RM-UF-04 | **NAMED DEPENDENCY** |
| Claw numeric ranges (hand / foot) | **NAMED DEPENDENCY** (grip, footwear, gloves) |
| Final density / absolute balance / neutral idle / dynamic posture (+3° guard interim) | **NAMED DEPENDENCY** (later posture work, §257) |
| SAU-BODY-20 world-space | **OUT OF CURRENT SCOPE** (later implementation) |
| Gorrund thoracic context (different definitions); regional vs uniform cross-check; face FPI; foot proxy; forefoot / toe split | REPORT-ONLY / MEASUREMENT LIMIT (W2I) |
| Surface crotch reading (tried for the leg item) | **MEASUREMENT LIMIT**: on a tailed body the rule lands on the inner thigh or the perineal / tail-root surface depending on body, so it was not used (`crotch.json` kept for the record) |

## 8. Author decisions requested (narrow)

- **D-A — Saurin limb canon wording vs as-built anatomy.** The accepted Saurin limbs (Rodin B1 lineage, kept through Gates 4 / 5) have:
  - legs **shorter** than Marchfolk and Durrim in share (hip height 0.45–0.49 H vs Marchfolk 0.53–0.55 and Durrim 0.52);
  - a high knee;
  - an upper-arm-dominant arm (forearm / arm 0.31 vs Marchfolk 0.37).

  This contradicts "moderate-to-long legs" (L258, L526, L3599), L970's "rather than by forcing shortened legs", and "modest forearm emphasis" (L3602). The options are the author's:
  - **(a)** amend the canon wording to describe the as-built body (e.g. "legs share the stature budget with the elongated lower trunk");
  - **(b)** keep the canon and open a future anatomy pass on the limbs (not authorized here);
  - **(c)** record it as a known divergence for the final roster review.

  The builder makes no recommendation between (a) and (b). Both are identity decisions. The J-2 segment values are reference construction values, not population canon (W1d J-D2).
- **D-B — marginal acceptance.** Confirm as ACCEPTED MARGINAL, or not:
  - Broad 80 % (cap 79.75 % at 188 / 79.4 % at 208 under the same-state rule; anchor "~80 %"; interim guard);
  - the Broad 208 span +0.6 % vs Grask.
- **D-C — SAU-SILHOUETTE.** Carriage within 0 … +12° does not remove the front ambiguity, because the tail is seen end-on at crotch height. The levers left are all outside this pass:
  - **(a)** extend the carriage system with a root-level elevation (a new carriage family; needs §256.8 validation and a balance / cap rerun);
  - **(b)** judge SAU-SILHOUETTE in perspective or 3/4 views rather than strict orthographic front;
  - **(c)** carry it to the posture / animation phase (§257 living balance includes tail carriage) as a named dependency.

  No anatomy change is proposed.
- **D-D — structural-mass scoring.** Accept the MEASUREMENT LIMIT for SAU-BODY-14 / 16 joint-mass rows until a Saurin internal skeletal model exists (named dependency). Raw surface sections are on record.

## 9. Statement on anatomy

**No accepted Saurin anatomy changed.** The mesh, the stature route, stature endpoints, axial / pelvic identity, frames, composition, §263 clamps, plantigrade foot, claw coupling, RM-OT-04, RM-UB-08, matched-height separation and the never-Gorrund guard are all as accepted. J-2 is measurement-only, and carriage was tested on copies. No canon text was edited; the conflicts are surfaced in D-A and D-C.

---

**STOP.** Wave 3, Halvren genealogy references, final roster world-scale review, creator envelopes, tail world-space implementation, UE5, rigging, animation, equipment and gameplay were not begun. This closure package goes to the author for review.
