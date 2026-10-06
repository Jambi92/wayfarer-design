# RAC W1f — Author-Acceptance Gate

**Author:** Claude **Date:** October 6, 2026
**Order:** `reviews/chatgpt-rac-w1e-author-decisions-w1f-continuation-order.md`
**Evidence:** `reviews/rac-w1f-evidence/`. `tables.md` holds every number quoted here.
**ARM records:** `reviews/rac-w1f-arm/` (GO, GR, VA)

## Recommendation: CONSTRAIN — no candidate is ready for final ARM acceptance

**What was done:**
- The AD-G14 route (skeleton plus sculpted envelope) was built for Gorrund (new skeleton) and Grask (W1e skeleton carried onto the route; body unchanged to 4 decimals).
- A skeletal proxy now validates every affected race.

**Gorrund:**
- Every validly measurable accepted relation holds on its skeleton:
  - ALPC-3;
  - ALPC-5: GOR-BODY-04 and -14 pass; GOR-BODY-12 passes with 1 MARGINAL and 1 T-SENSITIVE row;
  - ALPC-7 at 229 and 208 cm, against equal-height and greater-height Broad Skarn;
  - ALPC-8, on the shape reading.
- The skeleton was solved to these relations (§2). The passes show that a consistent skeleton exists. They are not independent evidence.
- **ALPC-6 is NOT DEMONSTRATED.** The low-composition test body is physically invalid at the iliac crest: its skin lies inside the skeletal proxy.

**Overall:**
- No accepted canon was changed (§6).
- No final ARM acceptance is granted.
- No UE5, topology, rig, animation, equipment, gameplay or class work was done.

**Audit:** an independent audit reviewed this pass. Its verified findings are corrected or disclosed below. They cover the crest bias, solver circularity, statuses, the ALPC-0 rule change, ALPC-7 coverage and arm clearance.

## 1. Candidate status

| Candidate | Status | Basis |
|---|---|---|
| FN | **CONSTRAIN** | Skeletal pelvic relations pass. The bony orbit is shown through the accepted O-1 ring at δ = 0.03: it fits, and the increment holds by construction (§4). Forearm share > MF is NOT DEMONSTRATED (+0.99 %). Magnitudes are CONSTRAINED construction values (BM-1) |
| AE | **CONSTRAIN** | Hip height > MF NOT DEMONSTRATED (BM-3). Leg share and foot share > MF NOT DEMONSTRATED |
| VA | **CONSTRAIN** | Pelvic depth +3 %, so PV-D6 (VA > FN and > AE) holds on the skeleton. Hip-height ordering NOT DEMONSTRATED (BM-3). Skin diagnostic: depth ≥ MF misses by 1.4 % (skin only) |
| HV | **CONSTRAIN** | Geometry unchanged. Source span 8 / 8. The envelope is still builder-chosen and its sources are CONSTRAINED |
| DU-NAT | **CONSTRAIN** | Route accepted (BM-2). All skeletal and directional checks pass. The pelvic bone-scale magnitudes are not separately accepted. Globe ÷ HH is 1.023 × MF; the globe fits |
| GR | **CONSTRAIN** | The AD-G14 route reproduces the W1e body: the skeleton is identical and the skin differs only in the 4th decimal. All skeletal girdle and pelvic relations pass on acromial and glenohumeral landmarks. GR-G2 is shown by a scapula-proxy render construction, so it holds by construction and needs the author's render review. GR-G3: the arm clears the thoracic wall at R-6 by 0.72 cm (1 of 240 upper-arm vertices marginal). Magnitudes CONSTRAINED (BM-1) |
| GO | **CONSTRAIN** | All 35 skeletal rows pass, but the skeleton was solved to them (§2). ALPC-6 NOT DEMONSTRATED (invalid test body, §3). ALPC-2a crest row lies within the crest bias (§3). GOR-BODY-12 has 1 MARGINAL and 1 T-SENSITIVE row. Arm clearance 0.57 cm, with 5 of 243 upper-arm vertices medial of the trunk wall. All R-14 magnitudes are open (§5) |
| PK-NAT | **CONSTRAIN** | Species-scaled ocular geometry fits (globe-to-skin clearance 0.019 cm). Skeletal pelvic relations pass. Magnitudes CONSTRAINED (BM-1); ocular magnitudes need acceptance (G-S1) |
| CG-NAT | **CONSTRAIN** | As PK; globe-to-skin clearance 0.014 cm |

MF-M-R, MF-F-R, SK and SG remain the accepted references and are used here only as comparators.

## 2. Method, and what the passes do and do not show

### Skeletal proxy (PV-D16, AD-G10)

**Construction:**
- Each body is rebuilt with the same skeleton at the generator's minimum composition (muscle 0, weight 0).
- The result is aligned to the body's rig joints (residual ≤ 0.32 cm).
- It is then inset by an unmeasured soft-tissue allowance, t = 0, 0.5 or 1.0 cm × stature / 173. A direction counts only if it holds at all three values of t.

**Landmarks:**
- Glenohumeral centre: sphere fit to the shoulder cap.
- Acromion: the highest point over the shoulder.
- Hip joints: the rig joints.
- Proximal-femur scale: hip-to-trochanter.
- Femoral shaft: thigh section at 20 % of femur length.

All of this is builder method (R-14).

**Known defect (M-3): crest bias.** At the iliac crest (S5), the minimum-composition body is wider than the skin for every body:

| Body | Tissue per side at S5 breadth (% of stature) |
|---|---|
| MF | −0.14 % |
| GO | −0.25 % |
| GOR-BODY-16 | −1.37 % (skin about 3 cm per side inside the skeleton) |

So crest-breadth readings carry a relative bias of about 1 % between bodies. The t sweep does not cover this bias.

### Gorrund AD-G14 construction

**Skeleton:** the W1c GO inputs at minimum composition, plus:
- bone scales on the pelvis, femora, clavicles and upper-thorax length;
- a smoothed trunk sculpt (anterior depth, posterior depth and breadth by height), building a deep, posterolaterally broad lower ribcage (GO-G2).

**Envelope:** the skeleton plus GO's own reference-composition tissue field, carried vertex-wise and unscaled.

**Height:** re-solved to 228.77 cm.

**How the magnitudes were set (disclosed; circular):**
- A Gauss-Newton solver (`tools/rac/w1/w1f_drivers/gn2.py`) set the bone scales and sculpt nodes.
- It targeted:
  - the GO skeletal check rows, with margin 1.3 % for > and 0.3 % for ≥;
  - torso share, leg share and arm share vs GR;
  - the contour diagnostics;
  - stature.

**What this shows and does not show:**
- A skeletal solution exists that meets all measurable accepted relations at once, fits inside a plausible envelope, and survives frame changes (ALPC-5) and height change (ALPC-7 at 208 cm). Those last two were not solver targets.
- The passes are not independent evidence of the relations.

**Two items need author review:**
- ALPC-3 passes mainly through the solver-chosen femoral scale (×1.20). That scale acts on a minimum-composition surface that still includes some thigh tissue.
- Posterior lower-trunk depth goes up to ×1.65. It is applied to a back surface that includes the erector region. This is the structural reading GO-G2 allows, but it sits at the boundary between skeleton and tissue.

**Contour (the W1e rejection mode):**

| Body | Chest-lead (chest ahead of abdomen) | Buttock projection |
|---|---|---|
| GO W1f | +0.0032 | 0.0156 |
| GO W1e | +0.0020 | — |
| Rejected skin trial | +0.0001 | 0.0377 |
| References | +0.0046…+0.0071 | 0.0175…0.0230 |

All values are fractions of stature.
- GO chest-lead is still below every reference.
- The threshold used was a solver target, not an accepted rule.
- The buttock projection is also below every reference, partly because of the posterior sculpt.

Evidence: `go_before_after.jpg`, `go_frame_bodies.jpg`, `skeletal_proxy_sheet.jpg`, tables §4.

### Grask

- The W1e GR skeleton (BM-1 values) with unscaled GR tissue. The result equals the W1e body.
- The **scapula proxy** is a render construction for the qualitative GR-G2 review (RM-LR-02 (h)):
  - inferior angle at 0.62 vs MF 0.50 of thoracic vertical;
  - medial border at 0.28 vs MF 0.35 of half thoracic breadth;
  - laid on the posterior skeletal surface.
- The proxy's directions hold by construction.
- Evidence: `gr_before_after.jpg`, tables §5.

### Variant bodies

| Body | Change |
|---|---|
| GOR-BODY-04 | −8 % breadth |
| GOR-BODY-12 | −12 % breadth |
| GOR-BODY-14 | −12 % thoracic depth |
| GOR-BODY-16 | Muscle 0.25, weight 0.25. Same skeleton as GO, so its skeletal readings equal GO's by construction |
| GOR-BODY-02 | 208 cm |
| Broad Skarn | 229 and 208 cm; accepted SK base, frame write only |
| MF and SK | Rebuilt at the same low composition |

## 3. Results

### Skeletal validation (tables §2)

**83 rows:**
- 76 PASS;
- 3 NOT DEMONSTRATED (AE and VA hip height; BM-3);
- 1 REPORT;
- 3 placeholders (run in the ALPC rows);
- no FAIL.

The GO ALPC-2a crest ÷ thorax PASS (1.0041 vs MF 0.9962, +0.8 %) lies within the crest bias, so it is not robust.

### ALPC

| Criterion | Result |
|---|---|
| ALPC-0…4, GO skeleton | 15 / 15 PASS (solver targets) |
| ALPC-5, GOR-BODY-04 | 15 / 15 PASS |
| ALPC-5, GOR-BODY-12 | 13 PASS; hip-level breadth ÷ thorax MARGINAL (−0.1 %); shaft ÷ femur T-SENSITIVE (MARGINAL at t = 0, PASS at t ≥ 0.5) |
| ALPC-5, GOR-BODY-14 | 3 / 3 PASS |
| ALPC-7, GO 229 vs Broad Skarn 229 | 7 / 7 PASS |
| ALPC-7, GO 208 vs Broad Skarn 208 | 7 / 7 PASS |
| ALPC-7, GO 208 vs Broad Skarn 229 (greater valid Skarn height, GO L292) | 7 / 7 PASS. Intermediate heights not built |
| ALPC-8 vs Durrim | Silhouettes not identical (IoU front 0.760, side 0.796). GO > DU in ribcage vertical ÷ stature, torso vertical ÷ thoracic breadth, ribcage vertical ÷ thoracic breadth, and leg contribution. **Torso share GO 0.2960 vs DU 0.2965: not greater** (M-2) |
| **ALPC-6** | **NOT DEMONSTRATED** (details below) |

**Why ALPC-6 is NOT DEMONSTRATED:**
- **Skeletal half:** holds, but by construction, because GOR-BODY-16 has the same skeleton as GO.
- **Skin half:** the GOR-BODY-16 skin profile reads 5 / 12 FAIL against composition-matched MF. The failing rows are:
  - lumbar depth ÷ thorax;
  - crest ÷ thorax;
  - pelvic AP ÷ thoracic depth;
  - hip-level ÷ lumbar;
  - ALPC-0.

  But that body's skin lies about 3 cm per side inside the skeletal proxy at the crest, so the test body is physically invalid, and the skin result cannot be attributed to tissue.
- **Rule change:** W1f tightened ALPC-0 to a strict S4 < S5 ("no local minimum at S5", GORRUND L752). Under the W1e rule (S4 ≤ S5) the count would be 4 / 12. The tool still omits the spec clauses "no step S1→S2" and "at most one local minimum".
- **Sensitivity run (not adopted):** carrying human MF tissue onto the GO skeleton leaves 3 / 12 failures.

### Directional checks (tables §7)

**136 rows:**
- **127 PASS.**
- **6 NOT DEMONSTRATED:**
  - SK elbow and knee (accepted reference; marginal since W1c);
  - FN forearm;
  - AE leg and foot;
  - VA leg < AE.
- **2 HISTORICAL:** the FN E-proxy rows (non-vetoing, O-D2a).
- **1 FAIL:** GO thoracic breadth > SK on skin, −0.65 %. It passes on the skeleton.

HV source span: 8 / 8.

### Skin diagnostics (tables §8)

- GO depth items fail on skin.
- VA depth ≥ MF misses by 1.4 %.

These diagnostics include composition. They are not PV-D16 validation.

### Ears (tables §9)

v2 families re-attached. 22 / 22 direction checks pass.

## 4. Ocular (tables §6; `ocular_rings.jpg`)

**Fenn, δ = 0.03 ring:**
- 4.42 × 3.74 cm, 100 % inside skin, 0.75 cm clear of the globe.
- 1.030 × MF-M-R, and 1.016 / 1.015 × the MF-F-R ring.
- The 1.030 holds **by construction** (ring = MF ring × head ratio × 1.03); only the fit is measured.
- It supersedes the E-proxy for RM-CF-08.
- **Placement deviation:** the accepted O-1 forward offset of 0.8 cm is now carried with head height (FN 0.815 cm) so that small heads keep the ring inside the face. At a fixed 0.8 cm the FN ring also fits (W1e).

**PK and CG (Species-Scaled Adult Ocular Anatomy Rule, now in UFCA):**
- The ring is the MF ring carried with the head, so it is at MF proportion by construction.
- The globes are the existing socket-derived landmark globes, at MF globe ÷ socket proportion: PK 1.719 cm, CG 1.231 cm (globe ÷ HH 0.995 and 0.977 × MF).
- Fit: rings fully inside skin; ring-to-globe clearance 0.49 / 0.37 cm; globe-to-skin clearance 0.019 / 0.014 cm. That is tight, but there is no intersection.
- The "smallest physically sound" geometry (G-S1) was **not searched**. These are the existing values, now shown to fit at adult proportion.

**DU, GR, GO (G-S2):**
- All globes fit.
- Globe ÷ HH vs MF: DU 1.023, GR 0.959, GO 1.036. DU and GO follow their larger sockets (AC-U1).
- Not altered.

## 5. Identity-relevant R-14 magnitudes needing acceptance

| Item | Values (tables §1) |
|---|---|
| **GO skeleton** | Pelvis [1.10, 1.045, 1.28]; femora [1.20, 1, 1.20]; clavicle length 0.90; upper-thorax length 1.186; trunk sculpt ka / kp / kb (posterior lower-trunk depth up to ×1.65); height macro 0.8369 |
| **GO solver** | Gauss-Newton; targets and margins as in §2 |
| **GO side effects** | Girdle ÷ stature below MF (0.1855 vs 0.1944); GO > GR holds; no GO-vs-MF direction is authored. Skin thoracic breadth < SK (−0.65 %). Chest-lead and buttock projection below every reference. Arm clearance 0.57 cm |
| **GO variants** | GOR-BODY-04 (−8 %); -12 (−12 %); -14 (−12 % thoracic depth); -16 (0.25 / 0.25); -02 (208 cm, height macro 0.7019) |
| **Broad Skarn write** | +8 % breadth, +4 % thoracic depth, +5 % long-bone robusticity |
| **VA** | Pelvic bone scale [1.02, 1, 1.03] |
| **GR scapula proxy** | INF 0.62, MED 0.28 (MF 0.50, 0.35) |
| **Skeletal-proxy method** | Minimum-composition envelope; t sweep; landmark rules; S5 crest bias (M-3) |
| **Tissue transfer** | Vertex-wise donor tissue, unscaled; this decides the ALPC-6 test body |
| **ALPC-0 reading** | Strict S4 < S5 (changed from W1e's S4 ≤ S5) |
| **Contour diagnostics** | Chest-lead and buttock projection; no accepted thresholds |
| **Ocular** | O-1 placement carried with head height; PK/CG globes 1.719 / 1.231 cm |

## 6. Was any accepted canon challenged?

**No accepted canon was changed or overridden.** The Species-Scaled Adult Ocular Anatomy Rule (UFCA, plus PIPKIN and COGLING notes) and the Cogling ear-scale clarification (EA-W2) were recorded as issued. One COGLING note was reworded so that it restates the existing anti-enlargement rule rather than strengthening it.

Rulings needed:

- **M-1 — ALPC-6.** A valid low-composition test needs one of:
  - **(a)** a skeletal method that stays inside every composition, such as an explicit bony crest model; or
  - **(b)** an authored Gorrund reference tissue distribution (composition, firewalled under AD-G15).

  Until then, ALPC-6 stays NOT DEMONSTRATED.
- **M-2 — ALPC-8.** Is "greater vertical axial development" a stature share (GO = DU) or a shape (GO > DU)?
- **M-3 — Skeletal-proxy method.** Accept it with the disclosed crest bias, or require the bony-landmark model in M-1 (a).

## 7. Remaining NOT RUN / NOT DEMONSTRATED

**NOT DEMONSTRATED:**
- AE and VA hip-height ordering (BM-3);
- directional checks: AE leg and foot share, VA leg < AE, FN forearm, SK elbow and knee;
- GO ALPC-6.

**MARGINAL, T-SENSITIVE or not robust:**
- GOR-BODY-12 hip-level breadth ÷ thorax;
- GOR-BODY-12 shaft ÷ femur;
- GO ALPC-2a crest ÷ thorax (crest bias).

**By construction or render review only:**
- GR-G2;
- the FN orbit increment;
- PK/CG ocular proportions;
- PV-D17 crest thickness.

**NOT RUN:**
- ALPC-7 at Skarn heights between 208 and 229 cm;
- GOR-BODY-03 (maximum height);
- frame bodies for other races (not ordered);
- PK/CG minimal-globe search (G-S1).

STOP.

— Claude
