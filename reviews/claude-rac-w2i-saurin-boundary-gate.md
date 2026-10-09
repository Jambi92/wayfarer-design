# RAC W2I — Saurin Boundary Gate

**Author:** Claude (auditor) · **Date:** October 8, 2026 · **Order:** `reviews/chatgpt-rac-w2h-final-acceptance-w2i-saurin-order.md` §2–§25
**Author ruling (October 8, 2026; `reviews/chatgpt-rac-w2i1-saurin-closure-order.md`):** axial / pelvic, frames, composition firewall and RM-OT-04 ACCEPTED IN PRINCIPLE; RM-UB-08 body NAMED DEPENDENCY; stature family accepted in principle with **D1 APPROVED** (regional route = accepted W2 measurement / reference construction route, not the production creator implementation; uniform route historical cross-check only); tail coupling / RM-UB-04 accepted in principle with **D2 (a) + (b) APPROVED** and **D2 (c) CLARIFIED** (+3° interim guard judged primarily against the same-stature, same-state reference; SA-M188 secondary); **D3**: bounded J-2 measurement-only landmark pass authorized; **D4**: SAU-SILHOUETTE CONSTRAIN pending a neutral-carriage closure test (0 / +4 / +8 / +12°). Closure: `reviews/claude-rac-w2i-saurin-final-closure-report.md`.
**Evidence:** `reviews/rac-w2i-sa-evidence/`. `tables.md` is generated, and every number below comes from its JSON files.
**Status:** DESIGN ONLY / NO UE5. NON-CANON diagnostics.
- The frozen SA-M (aff1b52) and the §263 SA-F are **never written back**.
- No Saurin, Marchfolk, Skarn, Sagekin, elf, Halvren or Gorrund canon or body was changed.

## Verdicts

| Item | Verdict | Reason in one line |
|---|---|---|
| **Saurin stature family** | **CONSTRAIN** | 168 / 188 / 203 / 208 cm build as coherent adults, with matched points at 173 / 178 / 181 / 190. Every family check passes: stature, head bound, d/w, isometric tail guards and continuity. The route is new because Saurin has no generator or skeleton, so the author needs to accept it (**D1**). |
| **Saurin axial / pelvic body system** | **ACCEPT** | The −10 % lower-trunk Saurin stays far longer than matched Marchfolk at both 168 and 203 cm: +19 / +22 % (costal → hip joint) and +50 / +48 % (costal → crest). Frames and composition never change axial lengths. |
| **Saurin frame system** | **ACCEPT** | 104 / 104 frame checks pass. Breadth moves, while lengths, skull, tail and thoracic depth (±2 %) hold, and d/w ≤ 1.00 in every frame. Broad stays distinct from Gorrund 208 on the canon interim guard plus the complete package (11–12 of 12 readings separate). |
| **Saurin composition firewall** | **ACCEPT** | 96 / 96 checks pass. Composition never changes lengths or the tail percentage. d/w ≤ 1.00. The tail guards hold in every state; the highest muscle + fat case gives RSI 0.76 against a floor of 0.75. |
| **Saurin tail coupling / RM-UB-04** | **CONSTRAIN** | The anchors reproduce: Balanced 78 % and Broad 80 % are the reachable caps, and Narrow + high fat 72 % is reachable. But 72 % is not that state's cap; Narrow alone is the tightest state. The cap also moves about 2.5 points with the base convention, and the binding guard is always the +3° relative lean (**D2**). |
| **RM-OT-04** | **ACCEPT** | Against Sagekin and Halvren at every matched height, 10–12 of 12 body readings separate (9–11 with the tail hidden). The lower axial trunk is +32 to +41 % longer. Face rows use existing accepted values only. |
| **RM-UB-08 body portion** | **NAMED DEPENDENCY** | The as-built per-field spacing and relief are measured. There is no evidence for ranges: one realization only, and fields were never varied in Part 7 or §263. |
| **Saurin W2I overall** | **CONSTRAIN** | No anatomical contradiction was found. D1–D2 are construction / reading rulings. Limb, joint and S7 readings stay blocked by the absent measurement-only copy (**D3**). The front tail silhouette needs an author visual ruling (**D4**). |

---

## 1. Reference reproduction (§2, §23.1)

**The working copies.** The original creator-biology working copies in `/tmp` no longer existed, so I rebuilt them in the scratchpad:
- from the repo sources (`tools/rodin/creator-biology`, `female/closure`, `gate1`);
- plus the PC-staged frozen mesh `saurin_final_base.npz` (SHA-256 `a925e067…`, identical to the W1 record).

The Gate-8 centreline could not use its source mesh (the Gate 6/7 `g7up.npz` is gone), so it was re-derived on the frozen base with the accepted script.

| Item | Result |
|---|---|
| SA-M: all 22 Part 7 body / head / stature / mass / CoM / lean readings | **exact** (0.000 %) |
| SA-M tail length, tail % H | +0.002 % |
| SA-M tail section readings | root area +0.34 %, volume +0.23 %, RSI_raw −0.28 %, A50 +0.56 %, **taper_raw +2.30 %** (re-derived centreline) |
| SA-F (§263 centre) vs W1 ARM | height 187.881, lower trunk 33.640, pelvis 43.055, d/w 0.9217, tail 64.66 % H: **exact** |
| +10 % reference female | lower trunk 34.33 cm (§263 accounting 34.3) |
| Claw diagnostic (`claws.py`, field labels regenerated with the accepted `g7regs.py`) | **exact** Part 7 values (×1.15 → 0.008 cm, ×1.3 → −0.11 cm, ×1.5 → −0.29 cm; forefoot +0.35 / +0.70 cm) |

**Normalization.** All W2I tail ratios are normalized to the reproduced SA-M. That cancels the 2.3 % taper difference, which comes from the centreline source, not the anatomy.

## 2. Stature family and construction route (§4, §22)

**Why a new route.** Saurin has no generator and no skeleton. Part 7 and §263 validated 168 / 208 cm with the global height factor, which is a **uniform scale** that the W2 order forbids. W2I therefore uses a **regional route**, in the same sense as the accepted human native short-adult route:
- one length factor *k* for the vertical body;
- girth k^0.654;
- head k^0.688, about the neck / head junction;
- hands k^0.842 and feet k^0.942, about wrist and ankle.

These are the accepted W2 generator-allometry betas. The **tail is isometric** (k about the caudal-base landmark), because SAURIN §256.9 says "stature is isometric for every tail relationship". *k* is solved so standing height (tail excluded) hits the target.

| Body | Height | k | Lower trunk / H | Head length / H (bound 0.156–0.184) | d/w | Tail % H | Size-normalized RSI | Lean vs SA-M |
|---|---|---|---|---|---|---|---|---|
| SA-M168 | 168.00 | 0.890 | 0.1696 | 0.1751 | 0.880 | 64.34 | 0.996 | −0.32° |
| SA-M188 (frozen) | 187.88 | 1 | 0.1703 | 0.1696 | 0.880 | 64.61 | 1.000 | 0 |
| SA-M203 | 203.00 | 1.084 | 0.1708 | 0.1659 | 0.880 | 64.80 | 1.003 | +0.24° |
| SA-M208 | 208.00 | 1.111 | 0.1710 | 0.1648 | 0.880 | 64.86 | 1.004 | +0.32° |

- **64 / 64 family checks PASS** (male and female centre at all 8 statures):
  - height on target;
  - head length / H inside the §258 bound;
  - d/w ≤ 1.00;
  - isometric tail guards (RSI, taper, A50, A25).
- **Continuity:** 26 / 26 series readings are monotonic or flat. Breadths fall about 0.5–2 % per step with girth allometry; head share falls by allometry; tail % H rises 0.06–0.24 % per step, because the head is part of standing height.
- **Regional vs uniform cross-check (U, report):** at 168 / 208 cm the regional route moves head length / H by +3.3 / −2.9 % and lower trunk / H by −0.4 / +0.4 % relative to the Part 7 uniform convention.
- **Intermediate statures:** 173 / 178 / 181 / 190 were built **only** for real matched-height comparisons (§14). 203 is required by AD-R36.
- The 168–208 cm family stays a W2 diagnostic family, not a creator distribution.
- → **D1.**

## 3. Lower-trunk floor (§6; AD-R36)

The order's permanent test: the **−10 % lower-trunk Saurin** (creator `trunk_len` 0.90, the validated species bound) at 168 and 203 cm, against **real matched-height Marchfolk** (MF168, MF203).

| Body vs Marchfolk | LT1 costal margin → hip joint / H | LT2 costal margin → crest / H |
|---|---|---|
| SA-M168-LT90 vs MF168 | 0.1565 vs 0.1313: **+19.2 % PASS** | 0.1126 vs 0.0750: **+50.2 % PASS** |
| SA-F168-LT90 vs MF168 | 0.1563: **+19.1 % PASS** | **+50.0 % PASS** |
| SA-M203-LT90 vs MF203 | 0.1576 vs 0.1295: **+21.7 % PASS** | 0.1134 vs 0.0768: **+47.6 % PASS** |
| SA-F203-LT90 vs MF203 | **+21.6 % PASS** | **+47.4 % PASS** |

**Landmarks.**
- Saurin uses the authored axial stations that define the canon lower trunk (§263 accounting 32.0 cm = costal margin u 123 − hip-joint level u 91; pelvic platform u 100; thoracic inlet u 152). They move with every warp.
- Marchfolk uses the rig proxies used throughout RAC: costal margin = spine_03 joint; crest = spine_01 joint; hip joint.
- These definitions are not identical. **The margins (19–50 %) are far larger than any plausible landmark offset.** LT2, which uses crest-level landmarks on both sides, carries +47 % on its own.
- **Cause isolation:** none needed, because both boundaries pass.
- **Sex never extends the bound:** the female-shifted body requesting −10 % sits at the male bound (−0.12 %).

## 4. Thorax / lower trunk / pelvis / sacral continuity (§7)

- **Thorax deep, never past the guard:** d/w 0.880 (male) / 0.922 (female) at every stature; 0.82–0.96 across frames, composition and sex. The only values above 1.00 are the two §263 over-requests, which canon already clamps (§7 below).
- **Long, integrated lower trunk:**
  - lower trunk / H 0.170 (male), +5.1 % in the female centre, matching canon accounting 32.0 → 33.6;
  - thoracic vertical / H 0.154;
  - both flat across stature (+0.1 % per step).
- **Pelvis / sacral / caudal base:**
  - the caudal base stays the same mesh continuation (AD-R35 landmark, axis at the posterior pelvic plane);
  - tail root, platform and sacral organization move only through the tail-base frame component (§256.10);
  - frames never change pelvic depth or sacral organization (§258 frame scope; verified on axial lengths and thoracic depth ±2 %).
  - **Skeletal pelvic depth itself is not measurable on the rig-less mesh.** It is reported, not scored.
- **No obstetric anatomy** was introduced, and no reproductive anatomy was invented.

## 5. Frames (§8)

| Check (168 / 188 / 203 / 208, Narrow and Broad) | Result |
|---|---|
| Stature, both lower-trunk intervals, thoracic vertical, head length, hip station and tail % H unchanged (≤ 0.5 %) | **56 / 56 PASS** |
| Thoracic depth within ±2 % (§258) | **8 / 8 PASS** (−1.97 / +1.97 %) |
| Shoulder, thoracic breadth and pelvis move in the frame direction (≥ 1 %) | **24 / 24 PASS**. At 188: Narrow −6.2 / −8.4 / −5.6 %; Broad +9.2 / +9.3 / +6.5 % |
| d/w ≤ 1.00 | **8 / 8 PASS** (Narrow 0.941, Broad 0.821) |
| Tail guards with the reference tail | **8 / 8 PASS** |

**Never-Gorrund at 208 cm (§8).** The canon interim guard (AD-R36: frame never changes axial lengths or pelvic depth, plus d/w ≤ 1.00) **holds** for Broad, Broad + high muscle and Broad + muscle + fat: d/w 0.82 / 0.84 / 0.86. The complete package separates from GO208 on 11–12 of 12 common readings.

**Context, report only.** On the cross-pipeline readings:
- Saurin shoulder breadth / H is −4.7 to −5.8 % below Gorrund;
- Saurin thoracic depth / H and breadth / H read +10…13 % and +15…17 % above GO208.

Those two thoracic readings use different definitions on the two meshes: Saurin uses band maxima, MPFB uses level readings. Saurin's deep thorax is its own canon carrier, so they are not scored. Gorrund's structural-mass carriers (joint scale, limb robusticity) cannot be measured on Saurin (§9). **The existing guard and complete anatomy are sufficient; no new Broad-vs-Gorrund number is proposed.**

## 6. Composition firewall (§9)

Male and female centre, six states (low / high muscle, low / high fat, both high, minimum):

| Check | Result |
|---|---|
| Lengths and tail % H unchanged (≤ 1 %) | **72 / 72 PASS** |
| d/w ≤ 1.00 | **12 / 12 PASS** (0.861–0.960) |
| Tail guards (no fake tail base) | **12 / 12 PASS** |

**Tail root under composition.** Root area moves −9.8 % (minimum) to +39.5 % (high muscle + fat), because muscle follows composition into the proximal tail and caudal adipose is graded (§256.6–7). The root-sufficiency index stays inside the band: **0.76 at muscle + fat high, 0.05 above the 0.75 floor**.

**Identity under composition.** A low-muscle Saurin keeps every axial and tail relation. High muscle at 208 Broad stays distinct from Gorrund (§5). Sex-related E / B stay separate tissue and are not part of the fat control (tool-chain construction, as §263).

## 7. Sex-related configurations and stress cases (§5, §19)

**Female centre vs male centre, at every stature:**
- lower trunk +5.1 % (canon accounting +5.0 %);
- pelvis +3.2 % (+3.4 %);
- d/w 0.922 (0.922);
- height, tail % H and head length unchanged (≤ 0.09 %).

**Stress cases:**

| Case | d/w | Result |
|---|---|---|
| Narrow female | 0.985 | PASS |
| Broad female | 0.860 | PASS |
| +10 % reference female | 0.922 | PASS |
| Female high fat / low fat | 0.947 / 0.917 | PASS |
| Female at 168 / 208 cm | 0.922 | PASS |

**Clamps reproduced exactly as canon states:**

| Case | d/w | Canon outcome |
|---|---|---|
| Narrow + B 3.0 | **1.025** | exceeds → **CONSTRAIN** |
| … clamped to 2.1 | **0.999** | valid |
| Narrow + high fat + B 1.6 | **1.002** | exceeds → **CONSTRAIN** |
| … clamped to 1.5 | **1.000** | valid |

Sex never extends the ±10 % trunk bound (§3).

## 8. Tail (§10–§12; RM-UB-04)

**Landmark (§10):** the accepted AD-R35 caudal-base point (axis crosses the posterior pelvic plane, f = −14.8 on the frozen reference). Length is measured along the relaxed centreline to the tip and is never mixed with standing height.

**Coupling bodies (TL).**

| Body | Guards |
|---|---|
| 55 % with coupled base (0.83–0.85) | PASS; A50 0.44–0.45 (a complete tail, not a stump) |
| **Balanced 78 % (base 1.15)** | PASS; Δlean **+3.00°** |
| **Broad 80 % (base 1.16)** | PASS; +2.57° |
| **Narrow + high fat 72 % (base 1.10)** | PASS; +2.81° |
| 168 cm + 55 % | PASS |
| Balanced 80 % | **FAIL**: +3.78° |
| Narrow + high fat 78 % | **FAIL**: +4.19° |
| 208 cm Broad 80 % | **FAIL**: +3.03° vs SA-M; +2.71° vs its own stature reference |

**Reachable-cap sweep (RM-UB-04 body portion).** At each length the dependent base is solved by the §256.1 power law. Every §256 guard and d/w is then checked, and the longest passing length is the cap. Two base conventions inside the canon band were used:

| State | Cap, constant sufficiency (RSI 1.00) | Cap, most permissive base (RSI 1.19) | Canon anchor |
|---|---|---|---|
| Balanced, reference composition | 75.8 % | **78.4 %** | ~78 % |
| Broad | 77.3 % | **79.8 %** | 80 % |
| Narrow | **71.9 %** | **74.4 %** | — |
| Narrow + high fat | 73.0 % | 75.5 % | ~72 % |
| Balanced + high fat | 77.0 % | 79.6 % | — |
| Female centre | 76.4 % | 79.0 % | — |

- **The binding guard is always the +3° relative lean**, under the uniform-density static model.
- **The low end is coupled:** 55 % passes with the constant-sufficiency base, but **fails the cylindrical guard** (A50 0.50–0.51 > 0.48) with the smallest admissible base. A short tail must keep a substantial base.
- **Reading.** The Balanced and Broad anchors are reachable caps. The **72 % Narrow + high-fat anchor is reachable but is not that state's cap** (73.0–75.5 %). Narrow alone is the tightest state (71.9–74.4 %).
- No continuous production function is asserted. The anchors and the two cap sets are returned with the dependency.
- → **D2.**

**Balance firewall (§13).** The +3° relative guard is used only as the creator / reference diagnostic, scaled to stature. The uniform-density CoM is not biology. Final density, absolute limits and the neutral idle remain later work. No hunch, crouch or tail drag was introduced.

## 9. Limbs, hands, feet, joints, claws (§16, §17)

**Not run: limb segment lengths, within-limb distribution, exact-plane joints, femoral S7 and long-bone presence.**
- These need joint centres. The verified measurement-only re-posed copy does **not exist**: the W1c attempt failed its invariance check, and the W1d author ruling is **J-3**, "keep blocked; do not author joint centres merely to complete a table".
- I did not author joints. → **D3.**
- Affected validators: SAU-BODY-13, 15, 16, and the joint / limb portions of SAU-BODY-11 and 14.

**Feet.** Whole-foot sole length / H is 0.181 against matched Marchfolk 0.149–0.151, i.e. **+20 to +22 %**, consistent with broad, plantigrade feet with increased forefoot / toe contribution. The forefoot / toe split is not separable on the mesh (report). Plantigrade contact holds (claw tips above the ground at reference).

**Claw / digit coupling (§17).** The Part 7 diagnostic reproduces exactly: foot-claw tips reach the ground at about +15 % length. Under the stature route the foot scales uniformly about the ankle on the ground plane, so the threshold is size-invariant. Hand / foot claw numeric ranges stay **OPEN** (grip pose, footwear, gloves).

**Watch item.** The hip-joint station sits at 0.484 H, against 0.51–0.55 H for MPFB rig hip joints. Canon asks for "moderate-to-long legs". Leg length needs joint centres (D3), so this is reported, not scored.

## 10. Matched-height race comparisons (§14) and RM-OT-04 (§15)

**Common readings (12).** These are defined per mesh:
- hip height, lower trunk (costal → hip joint), costal → crest, thoracic vertical;
- thoracic d/w, depth and breadth;
- shoulder, pelvis, head height, foot;
- tail % H.

**Results.**
- **138 / 138 canon-direction rows PASS** at 168 / 173 / 178 / 181 / 190 / 203 / 208:

| Comparator | Rows (Saurin over comparator) |
|---|---|
| vs Marchfolk | lower trunk +29 to +39 %; d/w +20 to +27 %; thoracic depth / H +56 to +63 % |
| vs Skarn | shoulder −11 to −16 % (pelvic-axial, not clavicular); lower trunk +25 to +32 % |
| vs Sagekin | lower trunk +32 to +41 % |
| vs Fenn | thoracic depth / H +65 to +72 %; lower trunk +34 to +43 % |
| vs Aelari | lower trunk +29 to +37 %; d/w +20 to +28 % |
| vs Vael | lower trunk +30 to +38 % |
| vs Halvren | lower trunk +32 to +40 %; d/w +20 to +27 % |

- **Body-only passing:** 76 / 76 PASS. 10–12 of 12 readings separate with the tail; **9–11 of 11 with the tail hidden (P0).** The tail is never the sole carrier.
- **RM-OT-04 face (existing accepted values only):** Saurin male-centre r3 FPI 0.325 (W1 RM-CF-01) against Sagekin 0.143–0.145 and Halvren 0.143–0.145. No new facial geometry. Rows on OPEN facial landmarks (orbit placement, cross-race rostral floor) stay **named dependencies**.

## 11. RM-UB-08 body scale fields (§18)

Field labels were regenerated with the accepted `g7regs.py`; the claw reproduction confirms them. As-built, area-weighted p5 / p50 / p95 for the body (head fields excluded):

| Field | Spacing (cm) | Relief (cm) |
|---|---|---|
| structural | 0.53 / 1.23 / 3.20 | 0.05 / 0.11 / 0.22 |
| transitional / articulation | 0.53 / 0.62 / 1.06 | 0.05 / 0.06 / 0.09 |
| ventral | 1.20 / 1.60 / 1.75 | 0.06 / 0.07 / 0.09 |
| contact (palm / sole) | 0.28 / 0.30 / 0.39 | 0.025 / 0.025 / 0.035 |
| claw keratin | 0.31 / 0.42 / 0.54 | 0.03 / 0.04 / 0.05 |

- Articulation fields stay finer than structural fields: p50 0.62 vs 1.23 cm.
- Under the stature route, absolute spacing follows the local linear factor (girth 0.927 / 1.071 at 168 / 208 cm). Field topology is unchanged, and there is no global scale-size slider.
- **No numeric per-field range is supported**: there is only one realization, and fields were never varied in Part 7 or §263. → **NAMED DEPENDENCY / INSUFFICIENT EVIDENCE.**
- RM-UF-04 (facial fields) was not begun.

## 12. Named validators (§20)

| Validator | Disposition |
|---|---|
| SAU-BODY-01 min / ref / max | PASS (§2; sheets) |
| SAU-BODY-02 | PASS (neutral material; identity carried by axial / tail system and 9–11 non-tail readings) |
| SAU-BODY-03 vs Marchfolk at equal height | PASS (§10; tail present) |
| SAU-BODY-04 integrated organism | PASS (one continuous mesh; tail rows continuous) |
| SAU-BODY-05 / 06 / 07 frames / muscle / fat | PASS (§5, §6) |
| SAU-BODY-08 / 09 / 18 tail extremes and support | PASS within the §256 guards (§8). 80 % only on Broad; Balanced 80 % and Narrow + fat 78 % correctly CONSTRAIN |
| SAU-BODY-10 neutral upright stance | PASS as the reference stance. Living balance is later work (§257) |
| SAU-BODY-11 Marchfolk-normalized skeleton | PASS (axial); **limb portion NOT RUN** (D3) |
| SAU-BODY-12 vs Vael torso | PASS (lower trunk +30 to +38 %; d/w higher) |
| SAU-BODY-13 vs Grask limb / reach | **NOT RUN** (D3) |
| SAU-BODY-14 vs Gorrund structural mass | interim guard PASS (§5); **joint portion NOT RUN** (D3) |
| SAU-BODY-15 / 16 Cogling forearm / Durrim joints | **NOT RUN** (D3) |
| SAU-BODY-17 plantigrade foot | PASS (feet +20 %; plantigrade contact; claw coupling) |
| SAU-BODY-19 sex configurations | PASS (§7) |
| SAU-BODY-20 world-space | REPORT / later implementation; no proxy run |
| SAU-BODY-21 vs Skarn | PASS (§10) |
| SAU-BODY-22 vs Aelari | PASS (§10) |
| **SAU-SILHOUETTE** | **AUTHOR VISUAL CHECK** (D4) |

Culture, equipment, animation, gameplay and collision portions are **OUT OF CURRENT SCOPE**.

**SAU-SILHOUETTE measurement.** In the neutral straight-front orthographic view, the descending free tail shows through the thigh gap below the crotch:
- **12.7 cm** of visible extent, 6.3 % of the gap area, on the frozen reference;
- 11.1 cm at 168 and 20.6 cm at 208;
- 9.7 cm with a 55 % tail and 17.7 cm with a 78 % tail;
- 10.7 cm with the validated +8° lift and 15.7 cm with +10° droop.

In the workbench render it reads as a dark rounded mass between the thighs (`sheets/sa_lower_trunk_floor.jpg`, front column). This is the accepted frozen anatomy and carriage: Gate 1 recorded the front tail read as an open item, and the free-tail carriage stays locked. W2I changes nothing.

## 13. Complete non-pass list (§23.18)

**Scored:**
- TL Balanced 80 % FAIL (+3.78°) — correct CONSTRAIN.
- TL Narrow + high fat 78 % FAIL (+4.19°) — correct CONSTRAIN.
- TL 208 cm Broad 80 % FAIL (+3.03° vs SA-M; +2.71° vs its own stature reference).

**MARGINAL / near-edge (PASS):**
- Balanced 78 % at +3.00°;
- muscle + fat RSI 0.763;
- §263 clamps at d/w 0.999 / 1.000.

**Expected guard excess (canon CONSTRAIN):** Narrow + B 3.0 (d/w 1.025) and Narrow + high fat + B 1.6 (1.002).

**NOT RUN:** limb segments, within-limb distribution, exact-plane joints, femoral S7, long-bone presence; SAU-BODY-13 / 15 / 16; limb / joint portions of SAU-BODY-11 / 14 (D3).

**NAMED DEPENDENCY:**
- RM-UB-08 numeric field ranges;
- RM-OT-04 OPEN facial rows;
- claw numeric ranges;
- final density / balance;
- world-space (SAU-BODY-20).

**REPORT only:** Gorrund thoracic context (different definitions); regional vs uniform cross-check (U); sex deltas; balance list; foot proxy; face FPI.

**Generator / measurement limits:**
- rig-less mesh, so station landmarks instead of skeletal proxies;
- centreline re-derived (tail taper +2.3 % absolute, normalized out);
- pelvic depth not measurable;
- forefoot / toe split not separable.

## 14. Author decisions requested (narrow)

- **D1 — Saurin W2 stature construction.**
  - Accept the regional route as the W2 Saurin stature construction: vertical k, accepted W2 girth / head / hand / foot betas, **isometric tail** per §256.9.
  - It replaces the Part 7 uniform height factor for W2, which stays as a cross-check.
  - **Recommended:** it is the only non-uniform route available for a generator-less mesh, and every family relation holds.
- **D2 — RM-UB-04 reading.**
  - **(a)** Define the reachable cap on the most permissive admissible base (RSI band edge). Then Balanced ≈ 78 % and Broad ≈ 80 % are caps.
  - **(b)** Read the 72 % Narrow + high-fat anchor as a validated reachable point, not that state's cap.
  - **(c)** Carry the uniform-density +3° lean as the binding guard until the density / posture model exists.
  - **Recommended (a) + (b) + (c).** No production interpolation function is proposed.
- **D3 — Saurin limb / joint measurement.**
  - The order asks to "use or produce" the measurement-only copy. Producing one requires joint centres, which W1d J-3 still blocks.
  - **Options:**
    - **J-1:** author-placed joints.
    - **J-2:** builder-placed joints. The accepted construction gates already define shoulder / elbow / wrist construction points (`gate1/g7geo.py`) that could serve as a J-2 basis.
    - **J-3:** keep blocked.
  - **Recommended J-2 with author review of the points.** Nothing is applied until the author rules.
- **D4 — SAU-SILHOUETTE front read.**
  - The author should judge the straight-front tail read (§12 measurement; render provided) against "not readily mistaken for external genital anatomy".
  - **No anatomy change is proposed.** If it is judged a problem, the lever is resting carriage, which is later posture / animation work (§256.8). The validated +8° lift reduces the visible extent by 2 cm.

## 15. Canon and endpoint statements (§24)

- **Canon challenge: none genuinely challenged.**
- **Watch items:**
  - Hip-station height vs "moderate-to-long legs" can only be decided with joint centres (D3).
  - The Narrow + high-fat anchor ordering (D2).
- **Stature endpoints 168 / 208:** supported (coherent adults, all guards).
- **Tail endpoints:**
  - **55 % is supported only with a coupled base.**
  - **80 % is reachable only on Broad** (79.8 % at the band edge). Balanced tops out at about 78 %, matching "the 80 % endpoint is not an entitlement for every body".
  - **Narrow** is the tightest frame: 72–74 %.
- **Remaining for later work:**
  - world-space tail consequences (SAU-BODY-20);
  - facial rows (RM-OT-04, RM-UF-04);
  - creator-envelope interpolation for tail caps and stature;
  - final density / posture / balance;
  - claw ranges;
  - scale-field numeric ranges;
  - implementation.

---

**STOP.** Wave 3, Halvren genealogy references, final roster world-scale review, creator envelopes, tail world-space implementation, UE5, rigging, animation, equipment and gameplay were not begun. This gate goes to the author for review.
