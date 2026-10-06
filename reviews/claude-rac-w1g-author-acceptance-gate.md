# RAC W1g — Author-Acceptance Gate

**Author:** Claude **Date:** October 6, 2026
**Order:** `reviews/chatgpt-rac-w1f-author-decisions-w1g-continuation-order.md`
**Evidence:** `reviews/rac-w1g-evidence/` (`tables.md` holds every number quoted here; `README.md` maps the files)
**ARM records:** `reviews/rac-w1g-arm/` (GO, GR, AE, VA, FN)

## Recommendation: CONSTRAIN — no candidate is ready for final ARM acceptance

- **An explicit bony-station model was built (M-1(a)).** Each station is the narrowest the same skeleton gets across the generator's composition grid (the composition infimum). Every grid body, including the low-composition Gorrund, therefore lies outside the bone *by construction*.
- **It showed that the W1f crest passes came from the method.** Read with the new model, the unchanged W1f Gorrund fails 3 crest rows and the W1f Grask fails 1 (§2).
- **Both skeletons were corrected (Gorrund re-solved; Grask pelvis).**
  - Skeletal table: 83 rows. 79 PASS, 1 REPORT, and 3 placeholders that are run separately. No FAIL, MARGINAL or NOT DEMONSTRATED.
  - Directional checks: 138 rows. 1 FAIL (Gorrund thoracic breadth > Skarn, on skin) and 2 Skarn skin rows NOT DEMONSTRATED (shown on bony readings).
  - The W1f AE, VA and FN gaps are closed, with margins as small as 0.1 % over the 1 % threshold (§4).
- **Gorrund is still CONSTRAIN.**
  - **ALPC-6:** the test body is now valid (by construction); the skin half fails 1 of 12 rows.
  - **ALPC-5:** GOR-BODY-12 fails 1 row (−0.1 %, regressed from W1f PASS). GOR-BODY-12's shaft row never passes; GOR-BODY-04's shaft row fails at t = 0 (regressed from PASS).
  - **251 cm body (GOR-BODY-03):** 3 FAIL. Only 1 of the 3 is traced to the generator.
  - **Skin thoracic breadth > Skarn:** fails by 1.5 % (W1f −0.65 %).
  - **Render review:** the new lower-trunk breadth needs it (§3).
- **No accepted canon was changed (§9).** The Aelari vertical budget is close to a conflict and is flagged (§4).
- No UE5, topology, rig, animation, equipment, gameplay, class, camera or first-person work was done.

An independent audit of this pass was run. Its verified findings are corrected or disclosed below:
- the Fenn ocular pipeline regression;
- the arm test coverage;
- the hand-set solver step;
- overstated counts;
- the GOR-BODY-03 attribution;
- frame regressions;
- the R-14 list;
- by-construction wording;
- the Skarn joint magnitudes;
- exact margins;
- the method description.

## 1. Candidate status

| Candidate | Status | Basis |
|---|---|---|
| FN | **CONSTRAIN** | Forearm length +0.5 % → forearm share > MF **PASS** (+1.31 %; W1f +0.99 %). All skeletal rows pass. All directional rows pass, including the accepted O-1 bony-orbit rows (the superseded E-proxy rows are kept as historical, non-vetoing). Magnitudes CONSTRAINED |
| AE | **CONSTRAIN** | Hip height = leg share +2.28 % over MF, foot +1.25 % → **PASS**. The new budget rows are near the threshold: torso > FN +1.17 %; neck > MF +1.20 % (§4) |
| VA | **CONSTRAIN** | Hip height +1.11 % over MF and −1.14 % under AE → **PASS**. Skin pelvic depth ≥ MF still misses by 1.4 %, unchanged (diagnostic only, AD-W1G-12) |
| HV | **CONSTRAIN** | Unchanged. Source span 8 / 8 with the corrected FN, AE and VA |
| DU-NAT | **CONSTRAIN** | Unchanged. All rows pass under the bony model |
| GR | **CONSTRAIN** | Pelvis width ×1.12; W1e lumbar narrowing removed. All skeletal rows pass. Arm: no interpenetration where testable (§3). GR-G2 stays CONSTRAINED (§6). Skin pelvis ÷ thorax ≈ MF now fails (§8) |
| GO | **CONSTRAIN** | Re-solved. All 35 reference skeletal rows pass, and ALPC-7 passes at all 10 tested height pairs. Open items: ALPC-6 skin 1 FAIL; frame rows; GOR-BODY-03; skin thoracic breadth vs Skarn; render review; R-14 magnitudes (§3, §10) |
| PK-NAT | **CONSTRAIN** | G-S1: viable 1.716–1.745 cm, solution 1.716; current 1.719 is inside the interval and within method uncertainty (§5) |
| CG-NAT | **CONSTRAIN** | G-S1: viable 1.222–1.258 cm, solution 1.222; current 1.231 is inside the interval and within method uncertainty (§5) |
| SK (reference) | unchanged | Elbow and knee rows shown on the composition-infimum joint reading, direction only (§4) |

## 2. Bony-station method (AD-W1G-1) and its limits

**Model (CIB):**
- The same skeleton is built at muscle and weight ∈ {0, 0.25, 0.5}: 9 bodies, with AD-G14 bodies through their own route.
- Each body is aligned to the reference rig joints.
- Each station S2–S7 takes the minimum over the 9 bodies (breadth and depth separately), then the W1f soft-tissue sweep t = 0 / 0.5 / 1.0 cm.
- The proximal-femur scale is reduced by half the S6 change.
- The glenohumeral and acromion landmarks, joints and vertical intervals are as in W1f.

**What changed:**
- **The crest (S5) moves for every body.** The generator's minimum-composition body flares there:
  - MF 29.12 → 26.38 cm;
  - W1f GO 41.98 → 34.32 cm.
- **Other stations move for a few bodies:** for example Broad Skarn 229 S4 −12 % (an ALPC-7 comparator) and GOR-BODY-03 S4 −11 %. The per-station minimum body is listed in each `cib/<ID>_cib.json`.

**Attribution: the unchanged W1f bodies read with the bony model** (`method_attribution_checks.json`; inputs `cib/GO-W1f_cib.json` and `cib/GR-W1f_cib.json`; procedure `tools/rac/w1/w1g_drivers/attribution.md`):

| Body | Row | Value | Requirement |
|---|---|---|---|
| GO | Crest ÷ thorax | 0.815 | ≥ MF 0.899 |
| GO | Trochanteric ÷ crest | 1.360 | ≈ 1.227 |
| GO | ALPC-7 vs Broad Skarn | 0.815 | > 0.838 |
| GR | GR-P6 pelvis ÷ thorax | 0.839 | ≈ 0.899 |

**Limits (R-14):**
- **An upper bound on bone, not a measurement.** The t sweep is the only allowance below it.
- **Grid resolution.** The grid is 3 × 3.
- **Crest level.** The crest is still read at the spine_01 joint height, where the profile is steep.
- **Validity is circular.** Physical validity of any grid body (GOR-BODY-16 included) holds by construction.
- **The crest hoop in `skeletal_proxy_sheet.jpg` still uses the minimum-composition surface.**
- **Skin rows are kept separate** (§8).

## 3. Gorrund (AD-W1G-1, -2, -3, -4, -5)

### Re-solve (AD-W1G-3), with exact provenance (`solver/`)

**Solver runs:**
- Four solver runs (`gn4_S1`–`S4`) had the bony model in the loop. None reached feasibility: the last, `S4`, ended with lower-thorax depth (ALPC-1) still failing.
- An earlier run (`S2`) pushed the femur to 1.30 before caps were added.

**Hand-set step (not solver output):**
- Single-parameter probes (`probe3`) showed that raising posterior depth at r 0.31 to 1.60–1.65, or lowering it at r 0.6, rescues ALPC-1.
- So the start point for the least-extreme pass was **set by hand** at kp 0.31 = 1.60 and kp 0.6 = 0.92. 0.92 is below the solver's own lower bound for that node (1.0).

**Least-extreme pass (`shrink.log`):**
- Each parameter was moved a third of the way toward the generator default, twice, and kept only if the accepted relations held. The tolerance was 0.0006 summed residual, from the ALPC-3 shaft row, not exactly zero.
- **Only 1 of 15 parameters moved:** kp 0.18, 1.25 → 1.11. The other 14 were rejected.

**After the pass:**
- Upper-thorax breadth at r 0.6 / 0.8 was lowered from 1.11 / 1.06 to 1.05 / 1.02 for arm clearance (`probe4`, `probe5`). The pass itself ran with the old values.
- The final set was then rebuilt and every check re-run on it; all reference skeletal rows pass.

**Final values vs W1f** (bounds hit are marked):

| Value | W1f | W1g |
|---|---|---|
| Pelvis | [1.10, 1.045, 1.28] | [1.03, 1.045, 1.26] |
| Femur | 1.20 | 1.19 |
| Clavicle | 0.90 | 0.94 |
| Upper-thorax length | 1.186 | 1.186 |
| ka amplitude | 1.0 | 0.96 |
| kp (r 0.18 / 0.31 / 0.44 / 0.6) | 1.25 / 1.50 / 1.65 / 1.35 | 1.11 / 1.60 / 1.65 / 0.92 |
| kb (r 0 / 0.18 / 0.31 / 0.44) | 1.0 / 1.16 / 1.19 / 1.16 | 1.16 / **1.40 (upper bound)** / 1.27 / **0.95 (lower bound)** |
| kb (r 0.6 / 0.8) | 1.11 / 1.06 | 1.05 / 1.02 |

ka is anterior depth, kp posterior depth and kb breadth.

**AD-W1G-3 answer (partial):**
- The femoral ×1.19 and posterior depth ×1.65 are the least values *found*: a one-third move breaks ALPC-3 and ALPC-1. Only one alternative femur value (1.13) was tested.
- Their biological defensibility is **not demonstrated** beyond "required by the accepted relations under this construction."

**Still circular.** The skeleton is fitted to its own rows. The frame, height and composition bodies were not targets.

### Render review needed (M-5)

- The lower-trunk breadth (×1.16 at the hip, ×1.40 at the crest) puts a visible flank flare on the skeleton render. It is milder on the skin (`go_before_after.jpg`).
- On skin, crest ÷ lumbar breadth is 1.110 vs MF 1.079. That is the "no independent widening" direction (ALPC-2b) reversed on skin; the skeleton passes.
- The fail mode to check is the "independently widened hip structure" (GORRUND L744; "giant pelvis" L740).

### Arm clearance (AD-W1G-4, -11): what can be shown

- Each upper-arm vertex is tested against the trunk's own cross-section at its height. This is decidable **only where the section is closed**.
- At the armpit the trunk-only section is open. So only the lower 19–50 % of upper-arm vertices are tested (counts and height bands in tables §7).
- Above that band only the W1f vertex-to-vertex gap exists.

| Body | Interpenetration (testable band) | Vertex gap |
|---|---|---|
| GO W1f | 4 vertices inside the trunk (−0.68 cm) | 0.57 cm |
| GO W1g | 0 inside; 1.09 cm in the band | 0.67 cm |
| GO stress bodies | 0 inside | 0.57–1.67 cm |
| GR | 0 inside (W1f "1 marginal vertex" was the crude test's false positive) | 0.72 cm |

- **Not shown:** clean clearance in the armpit band.
- A nearest-surface sign test was tried there and rejected: it calls the accepted MF and SK "inside".
- The solver's clearance constraint used an earlier version of this test that treated open sections as outside. It was corrected afterwards; the delivered values above are from the corrected test.
- **Cost of the fix:** lowering upper-thorax breadth made Gorrund thoracic breadth ÷ stature fall 1.5 % below Skarn on skin (directional FAIL; W1f −0.65 %). It still passes on the skeleton.
- AD-W1G-4 asks that thorax relations be preserved. **This is a trade-off for the author.**

### ALPC-6

- **GOR-BODY-16** = the reference skeleton at muscle 0.25 / weight 0.25, through the same route. It is one of the 9 grid bodies, so its skin lies outside the bone **by construction**. The minimum is 0.09 cm per side at the crest; W1f was 3.1 cm *inside*.
- **Skeletal half:** 15 / 15. Same skeleton, so this holds by construction.
- **Skin half (vs MF at the same composition): 11 / 12.**
  - **FAIL:** pelvic depth ÷ thoracic depth, 0.915 vs 0.983 (−6.9 %).
  - The W1f lumbar-depth and ALPC-0 failures now pass.
  - Not tuned; no tissue authored.

### Frames and stature (AD-W1G-5)

The frame writes were not re-tuned. W1f → W1g changes per row are in tables §4.

| Test | Result |
|---|---|
| GOR-BODY-04 | 14 PASS. Shaft ÷ femur FAIL at t = 0, MARGINAL at 0.5, PASS at 1.0 (W1f PASS) |
| GOR-BODY-12 | **Lower-thorax breadth ÷ thorax FAIL**: 0.8171 vs 0.8182, all t (W1f PASS). Shaft ÷ femur FAIL / FAIL / MARGINAL, **never passes** (W1f T-SENSITIVE). Hip-level breadth ÷ thorax PASS (W1f MARGINAL) |
| GOR-BODY-14 | 3 / 3 |
| GOR-BODY-02 (208.8 cm) | 15 / 15 |
| GOR-BODY-03 (250.7 cm) | 3 FAIL (below) |
| ALPC-7 | 10 / 10 tested pairs × 7 / 7: Gorrund 208 / 215 / 222 / 229 cm vs equal or taller Broad Skarn. Tested points only |

**GOR-BODY-03, 3 FAIL: lower-thorax depth, crest ÷ thorax, shaft ÷ femur.**
- **Only the lower-thorax depth row is traced to the generator.** The plain generator body with Gorrund inputs, at minimum composition, falls 0.813 → 0.728 at the 251 cm height setting, while its skin stays at 0.906 / 0.905 (`gor03_generator_diagnostic.json`).
- **The crest row is not explained.** The generator ratio rises with height, while the GOR-BODY-03 bony crest drops to 36.56 cm. Its minimum is at the 0.25 / 0.25 grid body.
- **The shaft row was not analysed.**
- Returned as **M-6**.

### ALPC-8 (AD-W1G-2): shape reading

Gorrund > Durrim on every shape reading:

| Reading | Gorrund | Durrim |
|---|---|---|
| Ribcage vertical ÷ stature | 0.1680 | 0.1662 (+1.1 %) |
| Torso vertical ÷ breadth | 1.707 | 1.555 |
| Ribcage vertical ÷ breadth | 0.969 | 0.872 |
| Leg contribution | 0.530 | 0.517 |

- Silhouettes are not identical (IoU 0.734 front / 0.797 side).
- Torso share is not a criterion under AD-W1G-2.

## 4. AE / VA / FN / SK (AD-W1G-6, -7, -8, -12)

**Method:**
- Bone lengths only; evenly across thigh and lower leg; pelvis not truncated; canonical statures held with no height re-solve.
- A height re-solve was tried and rejected because it changed the forearm proportion and arm share.

| Body | Change |
|---|---|
| AE | Legs +1.99 %; upper thorax −2.96 %; neck −7.5 % (a canon-emphasized trait, kept > MF and > FN); foot +0.5 %. Stature 190.01 cm |
| VA | Legs +0.94 %; upper thorax −2.53 %. Stature 178.00 cm |
| FN | Forearm +0.5 %. Canon requires the direction (FN L51, L134) |

**Exact margins:**

| Relation | Margin |
|---|---|
| AE hip height / leg share vs MF | +2.28 % (one quantity, used in two rows) |
| VA vs MF | +1.11 % |
| VA vs AE | −1.14 % |
| VA vs FN | −2.25 % |
| AE foot vs MF | +1.25 % |
| AE torso vs FN | +1.17 % |
| AE neck vs MF | +1.20 % |
| AE neck vs FN | +3.65 % |

The torso and neck rows were added because the correction could break them (AE L40, L48, L50, L58).

**Aelari vertical budget (M-8).** Together, these accepted rules leave about 0.1 % of stature unless the Aelari head share falls (the head was not changed):
- AE leg ≥ 1.01 × VA ≥ 1.01² × MF;
- AE torso ≥ 1.01 × FN;
- AE neck ≥ 1.01 × MF.

**Skarn (AD-W1G-8):**
- **Source and measure:** SKARN L24 "heavier joints" and L78 "larger joints". The W1c measure is skin joint breadth ÷ bone length: +0.9 % elbow, +0.8 % knee.
- **Composition-infimum joint reading:** SK ÷ MF elbow ×1.047, knee ×1.256, wrist ×1.235.
- **The magnitudes are not robust.** MF's minimum-composition knee is an outlier. Without the minimum-composition bodies the readings are elbow ×1.054, knee ×1.063, wrist ×1.239.
- **Conclusion:** the direction is shown on bony upper bounds, not landmarks, and the magnitudes are uncertain. Skarn was not changed. Returned for the author to accept the reading.

**Vael skin depth (AD-W1G-12):** −1.4 %, unchanged; the skeleton passes.

## 5. Ocular

### PK / CG, G-S1 (AD-W1G-10)

**Search:** globe diameter at the existing eye centre.
- **Lower bound:** the lids rest on the globe as in MF-M-R, scaled by head height (per azimuth).
- **Upper bound:** no skin intersection.
- **Cap:** globe ÷ head height no more than 1 % over MF.

| Body | Viable (cm) | Solution (cm) | Current (cm) | Globe ÷ HH vs MF | Clearance at solution (cm) |
|---|---|---|---|---|---|
| PK | 1.716–1.745 | 1.716 | 1.719 | 0.994 | 0.020 |
| CG | 1.222–1.258 | 1.222 | 1.231 | 0.970 | 0.018 |

**The lower bound has about 1 % uncertainty:**
- Accepted males sit 0.9 % (SK) and 0.1 % (SG) below their own computed minimum.
- The method gives empty intervals for MF-F-R and DU (their aperture shape differs from MF-M-R; not measured further).
- So the solution and the current globes are not distinguishable. Either value is a valid adult, non-enlarged geometry. Returned for acceptance; meshes unchanged.

### FN (AD-W1G-9)

- The δ = 0.03 ring is kept as the constrained construction.
- The directional checks now run the accepted O-1 rows. A W1g pipeline regression had fallen back to the old E-proxy rows; it was found by the audit and fixed. The E-proxy rows are kept only as historical.

## 6. GR-G2 (AD-W1G-11)

- **Not feasible as bony validation.** The generator rig has no scapula bone (trunk bones: pelvis, spine_01–03, clavicles, upper arms) and the mesh has no scapular landmarks.
- GR-G2 stays **CONSTRAINED**: by construction, plus render review.
- GR-G1 (biacromial ÷ thorax ≤ MF, acromial landmarks) passes.
- Arm: §3.

## 7. Ears (AD-W1G-13)

22 / 22 direction rows pass, plus 10 report rows. Not reopened.

## 8. Skin diagnostics (composition-inclusive; never a pass condition)

| Row | W1g | W1f |
|---|---|---|
| GO crest ÷ lumbar ≤ MF | **FAIL** 1.110 vs 1.079 | PASS |
| GO pelvic depth ÷ crest > MF / > SK | **FAIL** 0.708 | FAIL / PASS |
| GO trochanteric ÷ crest ≈ MF | **FAIL** 1.098 vs 1.163 | PASS |
| GO pelvic depth ÷ thoracic depth ≥ MF | **FAIL** 0.877 vs 0.971 | FAIL |
| GR pelvis ÷ thorax ≈ MF | **FAIL** 0.923 vs 0.869 | PASS |
| VA pelvic depth ≥ MF | **FAIL** −1.4 % | FAIL |
| GO lumbar-depth rows | **PASS** | FAIL |

The bony and skin layers now disagree at the crest for GO and GR.

## 9. Was any accepted canon challenged?

**No accepted canon was changed or overridden.** Two canon-sourced Aelari directional rows were added. The W1e Grask lumbar narrowing (a construction value) was removed.

**Rulings / acceptances needed:**
- **M-4:** accept the bony model with its limits (§2).
- **M-5:** Gorrund lower-trunk render review (§3).
- **M-6:** maximum-height route. GOR-BODY-03 fails 3 rows; only 1 is traced to the generator.
- **M-7:** ALPC-6 skin, 1 of 12: pelvic depth ÷ thoracic depth. Accept as soft tissue, or reopen M-1(b).
- **M-8:** the Aelari vertical budget (§4).
- **M-9:** arm clearance vs skin thoracic breadth > Skarn (§3). Also: the armpit band is untestable with the current method.
- **M-10:** accept the Skarn joint reading (direction only) and the G-S1 values (§4, §5).

## 10. Identity-relevant R-14 magnitudes awaiting author acceptance

| Item | Values |
|---|---|
| **Bony model** | 3 × 3 composition grid, per-station minimum, t sweep, proximal-femur correction |
| **GO skeleton** | Pelvis [1.0315, 1.045, 1.2644]; femora [1.1941, 1, 1.1941]; clavicle 0.9368; upper thorax 1.186; height macro 0.8369 |
| **GO trunk sculpt** | ka amplitude 0.9608 on the W1f ka profile; kp 1.1122 / 1.60 / 1.65 / 0.92 / 1.0 / 0.97 at r 0.18–1.0; kb 1.1619 / 1.40 / 1.2688 / 0.95 / 1.05 / 1.02 / 1.03 at r 0–1.0 |
| **GO solver and pass** | Constraints, the hand-set start and tolerances (§3) |
| **GO stress bodies** | Frame writes (W1f); donor height settings 0.7019 / 0.7438 / 0.7911 / 0.985; GOR-BODY-16 0.25 / 0.25 |
| **Broad Skarn** | W1f write at 208 / 215 / 222 / 229 cm |
| **GR** | Pelvis ×1.12, lumbar narrowing removed, clavicle length 0.98 (carried from W1e), scapula proxy INF 0.62 / MED 0.28 |
| **AE** | Carried from W1e: pelvis [1.0, 1.07, 1.06], spine_01 length 1.08. New: legs 1.0199, upper thorax 0.9704, neck 0.925, foot 1.005 |
| **VA** | Carried: pelvis [1.02, 1, 1.03]. New: legs 1.0094, upper thorax 0.9747 |
| **FN** | Carried: pelvis [1.04, 1, 1.04], spine_01 width 1.03. New: forearm 1.005. Ring δ 0.03 |
| **PK / CG** | G-S1 globes 1.716 / 1.222 cm (or the current values; §5) |
| **Joint reading** | Composition-infimum joint reading for the Skarn rows |
| **Diagnostic thresholds** | Arm clearance 0.25 cm in the solver; contour floors (no accepted thresholds) |

## 11. Remaining items

**FAIL:**
- GO ALPC-6 skin, 1 row;
- GOR-BODY-12 lower-thorax breadth;
- GOR-BODY-03, 3 rows;
- GO thoracic breadth > SK on skin (directional).

**Fails at some t / never passes:**
- GOR-BODY-12 shaft ÷ femur (never passes);
- GOR-BODY-04 shaft ÷ femur (FAIL at t = 0).

**NOT DEMONSTRATED:** SK skin elbow and knee; direction shown on the composition-infimum reading.

**Not demonstrated by measurement:**
- arm clearance in the armpit band;
- GR-G2;
- the FN ring increment;
- PV-D17 crest thickness;
- the GO lower-trunk read (M-5);
- biological defensibility of the femoral and posterior-depth magnitudes.

**NOT RUN:**
- frame bodies for other races (not ordered);
- Skarn heights other than 208 / 215 / 222 / 229 cm;
- a finer composition grid;
- other femur values.

STOP.

— Claude
