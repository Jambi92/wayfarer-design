# RAC W1h — Author-Acceptance Gate

**Author:** Claude **Date:** October 6, 2026
**Order:** `reviews/chatgpt-rac-w1g-author-decisions-w1h-continuation-order.md`
**Evidence:** `reviews/rac-w1h-evidence/` (`tables.md` holds every number quoted here; `README.md` maps the files)
**ARM records:** `reviews/rac-w1h-arm/` (GO, GR). AE, VA, FN geometry is unchanged from W1g (`reviews/rac-w1g-arm/`).

## Recommendation: CONSTRAIN — no candidate is ready for final ARM acceptance

What W1h closed:
- **GOR-BODY-03 (251 cm) passes 15 / 15** skeletal rows (W1g: 3 FAIL). The full stature series was run: 208, 215, 222, 229 and 251 cm.
- **Frame bodies pass.** GOR-BODY-04 15 / 15, GOR-BODY-12 15 / 15, GOR-BODY-14 3 / 3 (W1g: 1 FAIL, 2 T-SENSITIVE).
- **Gorrund thoracic breadth > Skarn is restored on skin: +1.19 %**, beyond the 1 % convention (W1g −1.5 %).
- **No arm interpenetration where it can be tested,** on two independent tests, for every Gorrund body.
- **Less isolated crest flare.** On skin the crest now sits inside the straight waist-to-hip line (flank flare −0.0077; W1g +0.0003). The accepted references read −0.0038 to −0.0095 (MF, SK, SG, DU; tables §7).
- **Reference skeletal table:** 83 rows. 79 PASS, 1 REPORT, 3 placeholders (run separately). No FAIL, MARGINAL or NOT DEMONSTRATED in this table. The stress-body residuals are listed below and in §10.
- **Directional table:** 138 rows. 0 FAIL. 2 NOT DEMONSTRATED: Skarn elbow and knee on skin (direction only, AD-W1H-8; unchanged). 2 superseded Fenn rows are kept as historical, non-vetoing.
- **Grask:** skin pelvis ÷ thorax ≈ MF passes again (GR-P6). All 8 skeletal rows pass.

Why Gorrund is still CONSTRAIN:
- **Thin and bound-dependent.** Two Gorrund values sit outside the W1h solver's own bounds and one sits at a bound (§3). Under ±2 % perturbation, 15 of 34 single-value changes lose an accepted relation: 11 a skeletal row (2 to FAIL), 4 the 1 % thoracic-breadth margin over SK (§7).
- **Shorter statures.** Ribcage vertical ÷ breadth ≥ MF:
  - **208 cm (GOR-BODY-02, minimum stature):** T-SENSITIVE, missing by 1.4 % at t = 1.0. W1g PASS. It was a solver target and was never fully satisfied.
  - **215 cm:** MARGINAL (H8 candidate PASS; the T9 step lowered it).
  - **222 cm:** T-SENSITIVE.
- **ALPC-7:** crest ÷ thorax vs Broad Skarn is NOT DEMONSTRATED at 5 of the 6 cross-height pairs (W1g: all PASS). All 4 equal-height pairs pass (§4).
- **ALPC-6 skin** (composition diagnostic, AD-W1H-4): 5 of 12 FAIL (W1g 1). Cause: in the low-composition body the narrowest trunk level now sits at the crest, so no waist is read above the crest (§4).
- **Armpit band:** still NOT DEMONSTRATED. Render inspection is required (§4).
- **Render review** of the reworked lower trunk is the author's (§4; `sheets/go_render_review.jpg`).
- **Circularity:** the reference body, GOR-BODY-02 and GOR-BODY-03 were solver targets. 215 / 222 cm, the frame bodies, GOR-BODY-05 and GOR-BODY-16 were not.

**No canon conflict was found (§9).** The Aelari budget is compatible at the 1 % convention but has no room for healthier margins unless the head / neck-base share shrinks. That is an author decision, not a conflict packet (§6).

No UE5, topology, rig, animation, equipment, gameplay, class, camera or first-person work was done.

**Independent audit.** An independent audit of this pass was run. Its 17 verified findings are corrected or disclosed in this gate and in tables.md:
- pair counts and the reference flare range;
- the sensitivity loss count (now including the thoracic-breadth margin);
- which values lose rows;
- the femur interval;
- probe results under the ordinary rule (now logged in `solver/probe_ordinary.log`);
- T9 checked on the reference only, and its remaining solver-margin shortfalls;
- the 208 cm regression;
- the VA leg in the Aelari budget;
- the dropped W1g residuals;
- several wording and table fixes.

## 1. Candidate status

| Candidate | Status | Basis |
|---|---|---|
| GO | **CONSTRAIN** | Re-solved. 35 / 35 reference skeletal rows; frames and 251 cm pass. Skin thoracic breadth > SK +1.19 %. Open: intermediate-stature rows, ALPC-7 cross pairs, ALPC-6 skin, armpit band, render review, bound reliance and sensitivity (§2–§4, §7) |
| GR | **CONSTRAIN** | Pelvis X re-tuned to 0.985 for the W1h station method (W1g 1.12). 8 / 8 skeletal and 7 / 7 skin rows pass. GR-G1 demonstrated (accepted, AD-W1H-11). GR-G2 CONSTRAINED (no scapular bone). The pelvis value is method-sensitive (§8) |
| AE | **CONSTRAIN** | Geometry unchanged from W1g. All rows pass under the W1h method. Directional margins 0.11–0.19 % over the 1 % threshold. Budget result in §6 |
| VA | **CONSTRAIN** | Unchanged. All skeletal and directional rows pass. Skin pelvic depth ≥ MF misses by 1.4 % (diagnostic only; unchanged) |
| FN | **CONSTRAIN** | Unchanged. O-1 δ = 0.03 and v2 ears retained (AD-W1H-10). All rows pass; ring fits (§8) |
| PK-NAT / CG-NAT | **CONSTRAIN** | Current globes retained (AD-W1H-9). All ocular fits pass on the W1h set |
| HV, DU-NAT | **CONSTRAIN** | Unchanged; all rows pass |
| SK (reference) | unchanged | Joint rows direction only (AD-W1H-8) |

## 2. Method changes (AD-W1H-1) and what they did

The composition-infimum bony envelope (CIB) is kept as the **validation upper-bound proxy**. Its parameters are refined, not canonized. Details: tables §1.

1. **Exact plane sections.** Trunk stations are read on plane sections of the trunk faces, not ±1 cm vertex slabs. Slabs missed whole vertex rings on stretched meshes, so one grid body could set the minimum alone.
2. **Fixed levels.** The thorax-maximum and waist stations are read at the reference body's levels in every grid body. A per-body re-search jumped to different anatomy in some grid bodies (the W1g GOR-BODY-03 crest and shaft cause).
3. **`confine_legs`.** The trunk sculpt no longer moves the free thigh.
4. **Two new readings:** skin flank flare, and an arm-tube interpenetration test.

**These changes are not anatomy, but they move results.**
- Read with the W1h method, the W1g Gorrund parameters fail several rows (`solver/p0.log`), e.g. bitrochanteric ÷ crest and crest-to-thorax at 251 cm. So the W1h passes come from **both** the method and the re-solve; they cannot be separated by one switch.
- Grask's pelvis value had to move from 1.12 to 0.985 to keep GR-P6 under the new method. That is how method-sensitive that row is.
- **Solver reading error, found and fixed in this pass.** Solver runs H1–H8 read skin thoracic breadth on the plane-section reading. It reads about 0.5–0.65 points wider than the directional check (H8 +1.11 % vs +0.47 %; final +1.71 % vs +1.19 %). The H8 result therefore showed only +0.47 % over SK on the directional reading (NOT DEMONSTRATED). The solver now uses the directional reading (`gn5.py`). The final step T9 (§3) was chosen on that reading.

## 3. Gorrund re-solve (AD-W1H-2, -3, -6, -7, -12)

**How it was solved:**
- **gn5**, Gauss–Newton with 17 parameters. Constraints:
  - every GO skeletal row with margin;
  - shares vs GR; chest-lead and buttock-lead;
  - stature 229 ± 2;
  - arm clearance ≥ 0.25 cm in the testable band;
  - skin thoracic breadth > SK;
  - skin flank flare ≤ 0;
  - a real waist level;
  - no folded skeleton slab;
  - GOR-BODY-03 rows (lower-thorax depth excluded) and GOR-BODY-02 rows.
- Runs H1–H8 (`solver/gn5_H*.log`). H8 ended with small residual solver-margin shortfalls (summed 0.014). Under the ordinary rule its reference rows all passed.
- **Post-solve step T9** (`solver/probeTB*.{py,log}`):
  - every breadth sculpt node ×1.017;
  - every posterior-depth node ×1.03;
  - femur robusticity 1.28.
- **Why T9:**
  - Widening the upper thorax alone (T1–T4) pulled thoracic depth ÷ breadth > SK (AD-G7) and ALPC-7 below the solver margins. Under the ordinary rule, T4 had ALPC-7 crest ÷ thorax FAIL and AD-G7 T-SENSITIVE.
  - Widening the whole trunk (T6, T7, T10) made bitrochanteric ÷ crest ≈ MF FAIL and the proximal-femur ÷ crest rows T-SENSITIVE.
  - Whole-trunk widening plus a more robust femur (T9) kept every reference row under the ordinary rule.
  - Ordinary-rule results for T0–T4, T6 and T7 are in `solver/probe_ordinary.log`; for T9 and T10, in `solver/probeTB3.log`.
  - **T9 was chosen on the reference body only** (no GOR-BODY-02 / -03 in the probe), then the full set was rebuilt and every check re-run.
  - T9 still sits slightly short of two solver margins: bitrochanteric ÷ crest at t = 1.0 (−0.0004) and skin thoracic breadth (+1.19 % against the solver's 1.3 % target). Both pass under the ordinary rule.
  - No full re-solve was run at T9. The only other femur value in 1.25–1.28 that was looked at is the sensitivity point 1.254 (§7).
- The full set was rebuilt and every check re-run on T9. The H8 candidate's results are kept in `solver/h8_candidate/`.

**Final values** (full table with bounds: tables §2):

| Value | W1g | W1h |
|---|---|---|
| Pelvis [X, Y, Z] | [1.0315, 1.045, 1.2644] | [1.1906, 1.0361, 1.2736] |
| Femur robusticity (breadth / depth; length unchanged) | 1.1941 | **1.28 (outside the solver bound 1.25)** |
| Clavicle length | 0.9368 | 1.0117 |
| Upper-thorax length | 1.186 | 1.21 |
| ka amplitude | 0.9608 | **1.0979 (bound 1.10)** |
| kp at r 0.18 / 0.31 / 0.44 / 0.6 | 1.11 / 1.60 / 1.65 / 0.92 | 1.23 / 1.26 / 1.38 / 1.29 |
| kb at r 0 / 0.18 / 0.31 / 0.44 / 0.6 / 0.8 | 1.16 / 1.40 / 1.27 / 0.95 / 1.05 / 1.02 | 1.00 / 1.18 / 1.22 / 0.94 / 1.04 / **1.17 (outside the solver bound 1.15)** |

ka is anterior depth, kp posterior depth and kb breadth.

**What changed in the body:**
- The pelvis bone is wider (X 1.03 → 1.19).
- The soft-tissue crest breadth is much lower (kb 1.40 → 1.18).
- The waist posterior depth is lower (kp 1.60 / 1.65 → 1.26 / 1.38).
- The femur is more robust.

On skin the result is less crest flare and a more continuous thorax → lumbar → pelvis line:

| Reading | W1g | W1h |
|---|---|---|
| Skin crest breadth | 43.9 cm | 41.8 cm |
| Skin waist depth | 33.0 cm | 30.0 cm |
| Flank flare | +0.0003 | −0.0077 |

Skin crest breadth is from `candidates/GO_meas.json`; flank flare is tables §7.

The skeleton body's flank flare (+0.022) is inside the accepted minimum-composition references: MF +0.030, SK +0.023, GR +0.022 (`skeletal/skeleton_flank_flare.json`).

**AD-W1H-12:** these remain CONSTRAINED construction values.
- Biological rationale: a broader bony pelvis and more robust femora carry the load path under a massive trunk (the order's "massive load-bearing architecture", AD-W1H-2). The crest soft tissue was reduced so the width is skeletal, not a flank pad.
- The femur 1.28 and upper-thorax breadth 1.17 are the price of thoracic breadth > SK at the 1 % convention in this construction path. No re-solve with a smaller femur was run.
- Sensitivity: §7.

## 4. Gorrund results

### Reference, frames, stature (AD-W1H-3, -7; tables §5–§6)

| Body | Stature (cm) | Result | Solver target? |
|---|---|---|---|
| GO reference | 229.62 | 35 / 35 reference rows; ALPC-0…4 15 / 15 | yes |
| GOR-BODY-02 | 209.60 | 14 PASS, 1 T-SENSITIVE (ribcage vertical ÷ breadth ≥ MF: −0.5 / −1.0 / −1.4 % at t = 0 / 0.5 / 1.0; W1g PASS) | yes in H8, not in T9 |
| GO 215 | 215.81 | 14 PASS, 1 MARGINAL (same row, −0.04 / −0.4 / −0.9 %) | no |
| GO 222 | 222.83 | 14 PASS, 1 T-SENSITIVE (same row, +0.5 / +0.1 / −0.3 %) | no |
| GOR-BODY-03 | 251.59 | **15 / 15** | yes in H1–H8 (lower-thorax depth excluded), not in T9 |
| GOR-BODY-04 / -12 / -14 | 229.6 | 15 / 15, 15 / 15, 3 / 3 | no |
| GOR-BODY-05 (Broad write) | 229.71 | render only | no |

**GOR-BODY-03 trace (AD-W1H-3):**
- The W1g crest and shaft rows came from the station method. In the minimum-composition and grid bodies at the 251 cm macro, the per-body level search jumped levels and vertex slabs missed rings (fixed by §2.1–2.2).
- The lower-thorax depth row was isolated as a generator corner at the maximum height macro (`skeletal/gor03_generator_diagnostic_W1g.json`). It was excluded from the solver.
- It now **passes without being targeted**: 0.874 vs MF 0.822 at t = 0.5 (W1g 0.720 FAIL).

**Frame regressions (AD-W1H-7):**
- **Shaft rows: proxy artifact, reclassified.** The frame's pelvis-breadth write lowers the 20 %-femur shaft section through the pelvis skin weights, with no femur change (GOR-BODY-04: 18.65 cm with the write, 18.91 cm without; `skeletal/frame_shaft_diagnostic_W1g.log`). The frame anatomy was not tuned to it.
- The rows now pass, but partly on the more robust femur (§3). The artifact itself remains in the proxy.
- **GOR-BODY-12 lower-thorax breadth:** a genuine frame reading, not the pelvis artifact: without the pelvis write it still only reached NOT DEMONSTRATED at t = 0 / 0.5 (0.8185 vs 0.8182 at 0.5) and FAIL at t = 1.0 (0.8114 vs 0.8115). It now passes (0.859 vs 0.832 at t = 0.5) with the wider W1h lower thorax. Not targeted.

### ALPC (tables §5)

| Test | W1g | W1h |
|---|---|---|
| ALPC-0…4, reference | PASS | 15 / 15 |
| ALPC-5 frames | 1 FAIL, 2 T-SENSITIVE | all PASS |
| ALPC-6 skeletal half | 15 / 15 | 15 / 15 |
| ALPC-6 skin half (diagnostic) | 11 / 12 | **7 / 12** |
| ALPC-7, 10 height pairs (4 equal-height, 6 cross-height) | 10 / 10 PASS | 5 pairs 7 / 7; **5 of the 6 cross-height pairs** crest ÷ thorax > Broad Skarn NOT DEMONSTRATED (+0.3 to +0.9 %) |
| ALPC-8 vs Durrim | shape rows yes | all 5 readings GO > DU; torso vertical only +0.4 % (not a failure under AD-W1G-2); silhouette IoU front 0.850 / side 0.790 |

**ALPC-7 cross pairs:** NOT DEMONSTRATED where GO 208 or 215 cm is compared with a taller Broad Skarn (215–229 cm). The equal-height pairs and every pair with GO ≥ 222 cm pass. These pairs were not solver targets.

**ALPC-6 skin (AD-W1H-4, kept diagnostic):**
- In GOR-BODY-16 (composition 0.25 / 0.25) the waist search finds its minimum on the crest level itself (S4 = S5 = 36.6 cm breadth). So no waist is read above the crest.
- The ALPC-0 shape row and the lumbar-depth, crest ÷ thorax and hip ÷ lumbar rows follow from that.
- It is the low-composition skin consequence of removing the crest flare. The skeleton passes all 15.
- No source line requiring these relations to survive composition unchanged was found, so no ruling is requested beyond the render review.
- **Author question (render):** should a skin waist still read at low composition?

### Arm clearance (AD-W1H-6; tables §7)

| Test | Covers | Gorrund result (all 10 bodies) |
|---|---|---|
| (a) Trunk section | Upper-arm vertices vs the trunk's closed section. GO reference: 157.1–162.3 cm, i.e. 24–29 cm below the 186.6 cm shoulder joint | 0 vertices inside; clearance 2.08–3.07 cm |
| (b) Arm tube (new) | Trunk vertices inside the closed upper-arm tube, from 8.0 to 26.5 cm below the shoulder joint (GO reference) | 0 inside, both sides |

- The new test reads MF, SK, GR, DU and AE / VA / FN as 0. It catches the known W1f Gorrund (4 inside), so it classifies the accepted bodies correctly.
- **Limitation:** neither test reaches the top ~8 cm below the shoulder joint (the axilla junction). There the arm and trunk sections are not closed.
- **Armpit band: NOT DEMONSTRATED.** Render inspection is required (`sheets/go_render_review.jpg`, front and 3/4 back).

### Render review (AD-W1H-2, required work 11)

`sheets/go_render_review.jpg` shows, side / front / 3/4 back on one scale:
- GO W1h 229 cm;
- GO W1g (not accepted);
- GOR-BODY-05 broad-frame stress;
- GOR-BODY-03 251 cm;
- SK 208, GR 218, MF 173;
- the GO W1h skeleton body.

Also delivered: `go_stature_series.jpg` (208 → 251 cm), `go_frame_bodies.jpg`, `side_lineup.jpg` and `skeletal_proxy_sheet.jpg`.

Limits of the sheet: the 3/4 view is from the back only. At full-body scale, with the arms hanging close, the armpit band cannot be judged reliably. A close axilla render is still needed for that band.

My read, for the author to confirm or reject:
- The front lower trunk is straighter than W1g, with no independent flank bulge.
- The side view keeps a strong posterior pelvis / buttock read (buttock-lead within the solver limit).
- The skeleton body shows a visible step from rib cage to abdomen.
- Whether this is "structural continuity, not a giant pelvis" is the author's call.

## 5. Directional and skin results (tables §10–§11)

- **Directional:** 0 FAIL. NOT DEMONSTRATED: SK elbow and knee only (direction only, unchanged).
- **Gorrund thoracic breadth > SK:** 0.1991 vs 0.1967 (+1.19 %; W1g −1.5 % FAIL; H8 +0.47 %).
- **Skin diagnostics, Gorrund** (never a pass condition):

| Row | W1g | W1h |
|---|---|---|
| Pelvic depth ÷ crest > MF and SK | FAIL | still FAIL vs MF and SK (0.750; MF 0.778, SK 0.752) |
| Bitrochanteric ÷ crest ≈ MF | FAIL 1.098 | FAIL 1.183 vs 1.163 (now on the other side) |
| Pelvic AP ÷ thoracic depth ≥ MF | FAIL | FAIL |
| Hip-level ÷ lumbar ≤ MF | PASS | FAIL (1.282 vs 1.255) |
| Crest ÷ lumbar ≤ MF | FAIL 1.110 | MARGINAL 1.083 |
| Lumbar depth ÷ thorax > MF | PASS 0.931 | NOT DEMONSTRATED 0.830 |
| ALPC-7 skin: pelvic depth ÷ thoracic depth > Skarn central | NOT DEMONSTRATED 0.877 | FAIL 0.868 vs 0.870 |
| ALPC-7 skin: lumbar depth ÷ thoracic depth > Skarn central | PASS 0.931 | NOT DEMONSTRATED 0.830 vs 0.826 |

- **VA** skin pelvic depth: −1.4 %, unchanged.
- **GR** skin: all PASS (AD-W1H-11 re-check done; GR was not tuned to skin; the pelvis value was set by the skeletal GR-P6 row).

## 6. Aelari vertical budget (AD-W1H-5; tables §8)

- **Relations:** with stature fixed, AE leg ≥ 1.01 × VA leg ≥ 1.01² × MF leg; AE torso ≥ 1.01 × FN; AE neck ≥ 1.01 × MF. Leg + torso + neck + remaining share (head plus neck base) = 1.
- **Current margins over the thresholds:** leg / VA +0.15 %, VA / MF +0.11 %, torso +0.17 %, neck +0.19 %.
- **Most even distribution** at the current remaining share: **+0.14 %** on every relation. Redistributing gains 0.03 points, so the current W1g values were kept (AD-W1H-5: no artificial compensation).
- **Healthier margins need a smaller head / neck-base share:**

| Uniform margin | Change to the remaining share |
|---|---|
| +0.25 % | −1.2 % |
| +0.5 % | −4.0 % |
| +1 % | −9.7 % |

- **Margins above zero also need a longer VA leg.** The VA leg minimum is 0.5387 at +0.25 % (current 0.5380), 0.5401 at +0.5 % and 0.5428 at +1 %. So healthier AE margins touch VA as well (order item 8).
- **Not a conflict.** The set is geometrically compatible at the 1 % convention (at zero margin the remaining share could even grow 1.6 %). So no conflict packet is returned.
- **Author decision:** accept thin margins, or authorize a smaller Aelari head / neck-base share. That is an identity choice not settled by canon.

## 7. R-14 sensitivity (AD-W1H-12; tables §9)

**Method:** each of the 17 Gorrund values perturbed alone by ±2 % (ka amplitude ±0.05). The reference and the 251 cm body were rebuilt and every Gorrund skeletal row re-checked with the ordinary rule (`solver/sensitivity.json`; full table: tables §9).

**Results (34 perturbations):**
- **23 keep every skeletal row; 11 lose at least one.** Results among the losses: 9 T-SENSITIVE, 2 NOT DEMONSTRATED, 1 MARGINAL, 2 FAIL (some perturbations lose more than one row).
- **The 2 FAILs:** bitrochanteric ÷ crest ≈ MF (hip joints under the load path), at pelvis X −2 % and crest breadth kb18 +2 %.
- **Thoracic breadth > SK** stays positive in all 34 (lowest +0.72 %). It falls under the 1 % convention (NOT DEMONSTRATED) in 4 more: clavicle −2 %, upper-thorax length +2 %, upper-thorax breadth kb60 −2 % and kb80 −2 %.
- **Total: 15 of 34 lose an accepted relation.**
- **The 251 cm body keeps every row under all 34.**
- **Arm clearance** stays ≥ 1.84 cm; **flank flare** stays ≤ −0.0072.
- **Anterior / posterior depth values (ka, kp) change no row** at ±2 %. They are not tightly determined by the checks.
- **Femur:** at −2 % (1.254) two rows become T-SENSITIVE. This is one single-value perturbation with no re-solve, so it does not show that a smaller femur is impossible.

**Answer to AD-W1H-12:**
- A modest perturbation preserves the accepted relations for the depth values (ka, kp, pelvis Z).
- It does **not** for:
  - pelvis breadth and pelvis length;
  - hip-level, crest and waist breadth (kb0, kb18, kb31);
  - femur;
  - clavicle;
  - upper-thorax length and breadth (kb60, kb80).
- These sit on the relations, not inside them.
- The earlier H8 candidate (`solver/h8_candidate/sensitivity_H8.json`) lost a skeletal row in 15 of 34 with no FAIL, but held thoracic breadth > SK at only +0.47 %. T9 trades that for 2 FAIL-level perturbations.

## 8. Other races (AD-W1H-8 … -11)

- **VA / FN margins (order item 8)**, from `directional_checks.json` (geometry unchanged, re-run on the W1h set):
  - VA: leg share < AE +1.15 %; broader palms than AE +1.33 %.
  - FN: forearm share > MF +1.31 %; lower-leg share > MF +1.89 %.
  - All neighbouring rows pass. Margins are as in W1g.
- **SK:** joint rows direction only; Skarn unchanged.
- **PK / CG:** current globes retained. All rings fit on the W1h set.
- **FN:** O-1 δ = 0.03 retained; ring fits (clearance 0.75 cm). v2 ears: 22 PASS + 10 REPORT of 32 rows (unchanged).
- **GR:**
  - GR-G1 demonstrated.
  - GR-G2 CONSTRAINED; no scapula was invented. Render support: GR 218 cm is on `go_render_review.jpg` (side / front / 3/4 back) for inspection. No scapular landmark can be measured on it.
  - Pelvis X 0.985 (W1g 1.12; W1e base 1.0): the W1g value was a correction for the W1g method's crest reading, and the W1h fixed-level sections remove that need.
  - `gr_before_after.jpg` shows the change.

## 9. Canon conflict statement

**No accepted canon was changed, overridden or found contradictory.**
- No canonical stature or range was narrowed: GOR-BODY-03 at 251.6 cm passes.
- The trade found in §3 (thoracic breadth > SK against the crest / femur rows) has a solution under this construction, so it is not a contradiction. It costs a more robust femur, which is an author-visible magnitude.

**Rulings / acceptances requested:**
1. Gorrund lower-trunk render review (§4), including the ALPC-6 low-composition waist question.
2. Femur robusticity 1.28 and upper-thorax breadth 1.17 as the cost of thoracic breadth > SK (§3), given the sensitivity (§7).
3. ALPC-7 cross-height pairs at 208 / 215 cm and the intermediate-stature ribcage row: accept as the 1 % convention's limit, or require further work.
4. Aelari head / neck-base share (§6).
5. Armpit band: render inspection only (§4).

## 10. Residual FAIL / MARGINAL / NOT DEMONSTRATED (exact values in tables §4, §5, §10, §11)

**Skeletal:**
- ribcage vertical ÷ breadth ≥ MF: GOR-BODY-02 T-SENSITIVE (FAIL-size −1.4 % at t = 1.0; W1g PASS), GO 215 MARGINAL, GO 222 T-SENSITIVE;
- ALPC-7 crest ÷ thorax > Broad Skarn: NOT DEMONSTRATED at 5 of 6 cross-height pairs.

**Composition / skin diagnostics:**
- ALPC-6 skin 5 FAIL;
- GO skin: 6 FAIL, 1 MARGINAL, 2 NOT DEMONSTRATED (§5; tables §11);
- VA skin pelvic depth FAIL.

**Directional:** SK elbow and knee NOT DEMONSTRATED (direction only).

**Not demonstrated by measurement:**
- armpit band;
- GR-G2;
- the GO lower-trunk read (render review);
- biological defensibility of the femur and upper-thorax magnitudes beyond "required by the accepted relations under this construction".

**W1g residuals now closed:**
- GOR-BODY-03 (3 FAIL);
- GOR-BODY-12 lower-thorax breadth;
- the frame shaft rows;
- GO thoracic breadth > SK;
- GR skin GR-P6.

**Carried from W1g, not reworked in W1h (not ordered):**
- the FN ring increment (not demonstrated by measurement);
- PV-D17 crest thickness (not demonstrated by measurement).

**NOT RUN:**
- a re-solve at other femur values (only the sensitivity point 1.254 was evaluated);
- Skarn heights other than 208 / 215 / 222 / 229 cm;
- frame bodies for other races (not ordered);
- a finer composition grid.

## 11. Acceptance-readiness recommendation

**No candidate is ready for final ARM acceptance.**

Gorrund is the closest it has been:
- every reference, frame and maximum-stature skeletal row passes;
- thoracic breadth > SK holds;
- no testable arm interpenetration.

But it depends on two values outside the solver's own bounds and on rows that move under small perturbations (§7). It needs the render ruling (§9.1–9.2).

Other candidates:
- Grask passes every skeletal and skin row, but GR-G2 remains CONSTRAINED by order and its pelvis value is method-sensitive.
- AE / VA / FN pass, but their magnitudes are CONSTRAINED and the AE margins are thin pending §9.4.

STOP.

— Claude
