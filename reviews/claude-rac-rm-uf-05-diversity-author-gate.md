# RAC RM-UF-05 — batch diversity / anti-convergence author gate

**Order:** `reviews/chatgpt-rac-w3d-final-ruling-rm-uf-05-order.md`
**Evidence:** `reviews/rac-rmuf05-evidence/`:
- `coverage.json`
- `manifest.json` (68 batches; `batches/*.npz`)
- `eval.json`, `options.json`, `profile.json`, `slotbalance.json`, `halvren_demo.json`
- 6 sheets

**Drivers:** `tools/rac/w1/rmuf05_drivers/` — `uf05_spaces.py`, `uf05_metrics.py`, `uf05_batches.py`, `uf05_eval.py`, `uf05_slotbalance.py`, `uf05_coverage.py`, `uf05_build_faces.py`, `uf05_face_sheets.py`, `uf05_charts.py`.
**Scope:** RM-CF-05 writeback and W3 closure, plus RM-UF-05 diagnostics. No distance formula or threshold is canonized. All sampling is labelled **DIAGNOSTIC COVERAGE SAMPLING — NOT POPULATION FREQUENCY**.

---

## 0. Verdicts

| Item | Verdict |
|---|---|
| **RM-CF-05 writeback** | **COMPLETE** (commit 029f090; §1) |
| **RM-CF-05 = 0.05 r3 recorded** | **YES** |
| **Saurin Part 7 floor changed** | **NO** (0.255) |
| **W3** | **FINAL CLOSED** |
| **C1R pointer preserved** | **YES** (`reviews/rac-w3d-evidence/geometry/SK208-C1R_r6.npz`; neck-to-jaw clarification recorded) |
| **RM-UF-05 evidence coverage by population** | §2. Only **Saurin** supports a numeric batch (10 of its axes have author-accepted numeric ranges). **Skarn and Marchfolk** support a constrained batch on a diagnostic anchor scale built from the W3C / W3D anchors. **The other 10 populations are NOT FULLY CALIBRATABLE**: every facial DIR range is qualitative, and every frequency is OPEN. |
| **D1 result** | Stable in absolute value across slot profiles: the coefficient of variation (CV) of the broad-batch median nearest-neighbour (NN) distance is 0.046. But it is **dominated by large slots**: collapsing a 1-control slot lowers it only 1–5 %, while collapsing the ear slot (8–15 controls) lowers it 12–32 %. |
| **D2 result** | Similar stability (CV 0.057) and **far better slot balance**: a 1-control slot collapse lowers it 3–10 %, and the largest-slot collapse 10–17 %. D1's large-slot bias is 8–20×; D2's is 2–3×. The median-slot variant was the least stable (CV 0.107) and is not recommended. |
| **Recommended metric** | **D2** (UFCA-slot-balanced), always reported **with** a per-slot coverage check and a separate canon-bundle diagnostic. Neither pairwise metric alone detects a single-slot collapse or a cliché bundle (§4). |
| **Option A threshold** | near-clone fraction (D2 NN < 0.015) ≤ 5 % |
| **Option B threshold** | A **plus**: D2 NN 5th percentile ≥ 0.010; every slot's coverage ≥ 0.05; multi-slot tercile-tuple lift ≤ 4; canon-bundle share ≤ max(3 × its broad-coverage expectation, 2 %) |
| **Option C threshold** | B **plus**: D2 NN median ≥ 0.09 and every slot's coverage ≥ 0.5 |
| **Claude recommendation** | **B — advisory only** (§6). |
| **Race-specific Tier-G regressions** | **None.** Every race-specific test stays authoritative and unchanged. Five stale UFCA-06 §2.G line citations and a missing Skarn Tier-G row are reported (§5). |
| **Cliché-bundle regressions** | **None** in the accepted central states: Skarn C1R central batch Viking-bundle share 0 %; Saurin central batch dragon-wedge share 0 %. The forced-bundle stress batches are caught by B and C, and not by A (§4). |
| **Frequency assumptions introduced** | **NONE** |
| **Invented creator bounds introduced** | **NONE.** The human anchor scale is labelled a diagnostic anchor scale, not a creator interval. Saurin uses only §258 / §259 / §267 bounds. |
| **Author decision required** | **YES** |

---

## 1. RM-CF-05 writeback and W3 closure

**RM-CF-05 FINAL CLOSED** — 0.05 r3 FPI, VAL / DIAG only. The canonical record (new SAURIN_V1 §268) states:
- the Saurin Part 7 floor 0.255 is unchanged;
- the coupled minimum corner is 0.29196;
- the current operational non-Saurin comparison limit is **0.24196**, conditional on the current Saurin minimum;
- a future collision is **AUTHOR REVIEW REQUIRED — RM-CF-05 COLLISION**, never automatic clipping, invalidation, floor raise or margin change;
- FPI is never a membership test;
- precision is meaningful to hundredths only.

Pointers were updated in:
- SAURIN_V1 §259 (cross-race check closed) and §265 (OPEN item resolved for the current comparator state);
- UFCA_V1 §12;
- REFERENCE_ANATOMY_V1 §9 (W3 row) and §10 (new relational-margin rule);
- UFCA-06 rows 284 / 304 and the r3 framework RM-CF-05 row (closure-status notes; history not overwritten);
- the RMQ RM-CF-05 row, STATUS and RMQ.

**C1R neck-to-jaw clarification** recorded in SKARN_V1, the REFERENCE_ANATOMY §7 C1R row and the W3D gate closure note:
- NJT is a central tendency, not a clamp;
- parity on configuration 2 and the Narrow / low-muscle body is not a failure;
- no 0.50 widening, no NJT minimum, no neck membership test.

**RAC W3 FINAL CLOSED.** Preserved:
- W3A / W3A1, W3B / W3B1, W3C and W3D evidence;
- the generator capability gaps;
- Saurin PD-1 … PD-4;
- GR-FACE-14, GOR-FACE-05 and the other maximum-valid faces, as NOT DEMONSTRATED.

No UE5 authorization.

## 2. Evidence coverage by population (structural facial DIR, slots 2–9)

Source classes come from the UFCA_V1 / UFCA-04 / UFCA-08 routing and every race spec. **No structural facial frequency is authored anywhere (FREQUENCY OPEN for all).**

| Population | DIR (≈) | Numeric (author-accepted) | Anchor-scaled | Remainder | Batch status |
|---|---|---|---|---|---|
| Marchfolk | 22 | 0 | 9 (shared human anchor scale) | QUALITATIVE regions; projection anchored by MF-FACE-PROJ-MAX; granular control list not enumerated | anchor-scale batch — **CONSTRAINED** |
| Skarn | 44 | 0 | 9 (C1R / C2 / six overlap anchors) | QUALITATIVE; mandibular-body and anterior maxillary depth NOT DEMONSTRATED | anchor-scale batch — **CONSTRAINED** |
| Sagekin | 53 | 0 | 0 | QUALITATIVE ("detailed ranges come later") | **NOT FULLY CALIBRATABLE** (profile diagnostic only) |
| Fenn | 46 | 0 | 0 | QUALITATIVE; ORB δ and ear centres are central values | **NOT FULLY CALIBRATABLE** |
| Aelari | 45 | 0 | 0 | QUALITATIVE; ear centres are central values | **NOT FULLY CALIBRATABLE** |
| Vael | 41 | 0 | 0 | QUALITATIVE; VL-35 / 36 NOT DEMONSTRATED | **NOT FULLY CALIBRATABLE** |
| Halvren | 50 | 0 | 0 | QUALITATIVE inside ancestry envelope B; no face anchor | **NOT FULLY CALIBRATABLE** (synthetic-source diagnostic only) |
| Durrim | 50 | 0 | 0 | QUALITATIVE; DU-FACE / DU-DEPTH NOT DEMONSTRATED | **NOT FULLY CALIBRATABLE** |
| Grask | 37 | 0 | 0 | QUALITATIVE; projection central only; GR-FACE-14 NOT DEMONSTRATED | **NOT FULLY CALIBRATABLE** |
| Gorrund | 41 | 0 | 0 | QUALITATIVE; projection central only; GOR-FACE-05 NOT DEMONSTRATED | **NOT FULLY CALIBRATABLE** |
| Pipkin | 49 | 0 | 0 | QUALITATIVE; relational aperture / orbit CLAMP | **NOT FULLY CALIBRATABLE** |
| Cogling | 39 | 0 | 0 | QUALITATIVE | **NOT FULLY CALIBRATABLE** |
| Saurin | ≈30 | **11** (head scale; cranial L / W / D; ridge m 0.90–1.30 at canonical relief; orbit; IOD*; rostrum L / base W / anterior W / depth; posterior jaw depth) | 0 | ≈19 QUALITATIVE | **numeric batch (10 axes) — SUPPORTED** |

\* **IOD binding conflict:** UFCA §4 / §12 / §19 still call Saurin spacing Bound-locked, while SAURIN §267.2 now gives a creator-safe interval. IOD was **excluded** from the batch vector pending an author ruling.

**Space definitions.**
- **Saurin:** the multiplier spans of §258 / §259 / §267, normalized 0–1. Validators: the rostrum minimum rises with cranial length (index floor via the W1 coupled corner); rostrum > +10 % → rostral and jaw depth ≥ reference; anterior / base ratio 0.60–0.73.
- **Human anchor scale (Skarn / Marchfolk):** the MPFB target span between the accepted W3C / W3D anchors:
  - brow −0.30 (light-brow Skarn) … +0.60 (strong-brow Marchfolk);
  - cheek −0.30 … +0.60;
  - jaw breadth −0.30 … +0.60;
  - jaw drop 0 … 0.30;
  - nose −0.15 … +0.30;
  - head breadth / depth 0 … C2.
  - **This is a diagnostic anchor scale, not a creator interval.** It covers 9 of Skarn's ≈44 DIR and 9 of Marchfolk's ≈22. Ears, mouth, lids, forehead and chin are UNSCALED and excluded; that coverage loss is reported.

**Excluded from every vector:** DER (globe), SOFT, LAT, PRES, hair / pigmentation, the VAL / DIAG indices (FPI etc.) and bound-locked anatomy.

## 3. Batches (N = 256, seeds 101 / 202 / 303 / 404, exact manifests)

**Conditions:**
- **central:** reference ± 10 % of span (Subtle-like concentration);
- **broad:** scrambled Sobol over the demonstrated valid space, with reject / resample through the validators;
- **converge:** 3 templates + 1 % jitter;
- **mixed:** 50 % converge + 50 % broad;
- **slotcollapse:** broad, but one slot collapsed to a single value (Skarn / Marchfolk brow, Saurin rostrum);
- **cliché:** canon bundle forced.
  - Skarn "mandatory Viking face": brow, jaw breadth, gonial drop and head breadth all in the top 15 % (SKARN L48 / L154; W3C order).
  - Saurin "dragon-like wedge head": long rostrum, narrow anterior rostrum, strong ridges (SAURIN L752, §29).
  - Marchfolk has no structural cliché bundle beyond "one face with minor tweaks", so converge stands in for it (MF L253).

**Results** (mean over 4 seeds; ranges in `eval.json`):

| Population / condition | D1 NN median | D2 NN median | D2 NN p5 | near-clone < 0.015 | effective rank ÷ d | minimum slot coverage | tuple lift | canon-bundle share |
|---|---|---|---|---|---|---|---|---|
| SA central | 0.040 | 0.036 | 0.026 | 0 % | 0.98 | 0.20 | 1.0 | 0 % |
| SA broad | 0.192 | 0.173 | 0.137 | 0 % | 0.94 | 0.90 | 1.8 | 0.4 % |
| SA converge | 0.008 | 0.007 | 0.005 | 100 % | 0.16 | 0.60 | 8.8 | 0 % |
| SA mixed | 0.077 | 0.073 | 0.006 | 50 % | 0.64 | 0.84 | 14.6 | — |
| SA slotcollapse | 0.122 | 0.121 | 0.086 | 0 % | 0.64 | **0.03** | 1.8 | — |
| SA cliché | 0.123 | 0.114 | 0.089 | 0 % | 0.68 | 0.35 | 1.3 | **100 %** |
| SK central (C1R) | 0.035 | 0.034 | 0.024 | 0 % | 0.98 | 0.20 | 1.1 | **0 %** |
| SK broad | 0.190 | 0.181 | 0.134 | 0 % | 1.00 | 1.00 | 1.6 | 0 % |
| SK converge | 0.007 | 0.007 | 0.005 | 100 % | 0.20 | 0.79 | 10.3 | 0 % |
| SK mixed | 0.077 | 0.073 | 0.005 | 50 % | 0.68 | 0.93 | 10.5 | — |
| SK slotcollapse | 0.169 | 0.154 | 0.111 | 0 % | 0.89 | **0.04** | 1.2 | — |
| SK cliché | 0.091 | 0.084 | 0.063 | 0 % | 0.60 | 0.15 | 1.2 | **100 %** |
| MF central | 0.027 | 0.026 | 0.018 | 0 % | 0.86 | 0.11 | 1.0 | n/a |

MF broad, converge and mixed equal SK on the shared anchor scale.

**Profile study** (`profile.json`): unit-span diagnostic sampling on each population's slot-count profile (8 slots, 22–53 DIR).
- Broad median NN: D1 0.27–0.33, D2 0.25–0.32.
- Central: D1 0.053–0.063, D2 0.048–0.063.
- Converge: ≈ 0.010 for both.
- **Absolute NN distance grows with dimension.** A fixed threshold therefore transfers across populations only within this 22–53 DIR band, and only at N = 256. NN distance scales roughly as N^(−1/d_eff), so thresholds must be re-derived for other batch sizes.

## 4. Anti-clone and bundle findings

1. **Near-clones and duplicate templates** (converge, mixed) are caught by **every** option, on every population and seed: near-clone fraction 50–100 % against 0 % for every valid batch.
2. **Central concentration is not cloning.**
   - Subtle-like central batches keep a D2 NN p5 of 0.018–0.026 (Marchfolk 0.018 at the edge of its span), against ≈ 0.005 for clones. A near-clone distance of 0.015 separates them on every population tested.
   - A median floor (Option C) **rejects every central batch**, including the accepted Skarn C1R central concentration and the Sagekin-profile central batch (sheet 4). That would make a statistically central identity look like a failure.
3. **Single-slot collapse is invisible to pairwise distance.** D2 NN stays at 0.12–0.15, so it passes A. It is caught only by the **per-slot coverage** check (0.03–0.04 on the collapsed slot, against ≥ 0.11 on every valid batch).
4. **Cliché bundles are invisible to pairwise distance and to the generic tercile-tuple metric:**
   - D2 NN 0.08–0.11; tuple lift 1.2–1.3.
   - Correlation inside the bundle is low (|r| ≈ 0.02–0.07): the failure is **concentration**, not correlation.
   - Only the canon-bundle share catches it: 100 % against 0–0.4 % on the broad batches.
   - This confirms the order's requirement for a **separate bundle-convergence diagnostic**.
   - Legitimate FOLLOW / CLAMP couplings were left in place, through the Saurin validators, and were not scored as bundles.
5. **Halvren** (sheet 5; synthetic source centres, since no Halvren face anchor exists):
   - an exact-50/50 midpoint collapse keeps D2 NN 0.031, so it **passes A**;
   - its 50/50 midpoint share is 96 % against 0 % for a valid mixed batch;
   - near-duplicate source passing has a source-passing share of 100 %.
   - The anti-50/50 and source-passing tests must therefore remain separate Halvren bundle diagnostics, exactly as in HALVREN L60 / L381 / L504.
6. **Most converged UFCA slot:** central batches are concentrated in every slot by construction; the minimum is the slot whose reference sits at the span edge. The collapsed slot is identified correctly in every slot-collapse batch (`eval.json` `most_converged_slot`).

## 5. Tier-G carried tests (mapped; none replaced)

| Population | Tier-G test (current line) | RM-UF-05 mapping / status |
|---|---|---|
| Marchfolk | identity stress (MF L253); randomization sample (MF L261) | "one face with minor tweaks" = the converge condition → caught by A / B / C. Anchor-scale coverage only. **CONSTRAINED** |
| Skarn | anti-stereotype (SK L294–296); relationship-aware randomization (SK L282–284); SK-12; W3C six overlap validators (permanent) | Viking bundle caught by B / C; C1R central share 0 %. Overlap cases remain manually creatable. The ±10 % central batch does not reach the light-brow side (brow below the Marchfolk value: 0 %), as expected for Subtle; Diverse / broad reaches it. **No UFCA-06 Tier-G row for Skarn — add one.** |
| Sagekin | clone / stereotype (SG L370–383); SG-14; population-sample | Clone side = converge (caught). Stereotype items (identical noses, one template) need nose / mouth axes that are UNSCALED. Central-identity sensitivity is shown in sheet 4. **NOT FULLY CALIBRATABLE** |
| Fenn / Aelari / Vael | FN-34, FN L553; AE L479–481, AE-48…50; VA L505–507, VL-55…57 | Generic-elf / cliché convergence needs elf structural axes (all QUALITATIVE). The generic metric is not run numerically; the tests stay authoritative. **NOT FULLY CALIBRATABLE** |
| Halvren | anti-generic-half-elf L223; anti-beauty L222; anti-50/50 L60 / L361 / L381; HV-FAMILY-01 / 02; source L145 / L383 / L504 | Method demonstrated on synthetic sources (sheet 5). Real calibration needs Halvren face anchors. **NOT FULLY CALIBRATABLE** |
| Durrim | population sampling DU L233; Part 5 L521 | **NOT FULLY CALIBRATABLE** |
| Grask | anti-caricature GR L739; biological diversity GR L740 | Projection is held at central values (UFCA §13), so it is not a diversity axis. **NOT FULLY CALIBRATABLE** |
| Gorrund | minimum-stereotype GO L713; biological diversity GO L716 | Same as Grask. **NOT FULLY CALIBRATABLE** |
| Pipkin | PIP-INT-15 (L1622); PIP-INT-14 | Juvenile large-eye bundle (PK L469) definable, but its axes are unscaled. **NOT FULLY CALIBRATABLE** |
| Cogling | COG-SURF-14; COG-CC-04 / 06 (13 / 14 relevant) | Structural score never rescued by surface: surface is excluded from the vector by design. **NOT FULLY CALIBRATABLE** |
| Saurin | SAU-CC-01 / 03 / 05 / 17 / 18 / 24 / 25 / 26; §74; §264 | Numeric batch: clones, slot collapse and dragon-wedge bundle are caught by B; central and broad pass. SAU-CC-24 ("extremes not uniformly common") is a frequency question, left OPEN. **SUPPORTED** |

**Stale UFCA-06 §2.G citations.** Current lines are MF L253 / L261, SG L370, AE L479, VA L505, HV L381, DU L233, GR L739 / L740 and GO L713 / L716. These are reported for a later documentation pass and were not edited here.

## 6. Threshold options (N = 256; D2 = UFCA-slot-balanced RMS over normalized DIR; author decision)

| | **A — permissive anti-clone** | **B — robust anti-convergence** | **C — aggressive diversity** |
|---|---|---|---|
| **Formula / thresholds** | near-clone fraction = share of faces with D2 NN < **0.015**; must be ≤ **5 %** | A **and**:<br>• D2 NN p5 ≥ **0.010**;<br>• every slot's coverage (mean axis SD ÷ uniform SD) ≥ **0.05**;<br>• largest multi-slot tercile-tuple share ≤ **4 ×** its independence expectation;<br>• canon-bundle share ≤ **max(3 × broad-coverage expectation, 2 %)** for each canon-prohibited bundle | B **and**:<br>• D2 NN median ≥ **0.09**;<br>• every slot's coverage ≥ **0.5** |
| **Batch size** | 256 (re-derive for other N) | 256 | 256 |
| **Coverage prerequisites** | normalized spans for the participating DIR | same, plus a canon bundle defined in DIR terms | a demonstrated broad valid space for every slot |
| **Passes (of 4 seeds)** | central, broad, slotcollapse, cliché: 4 / 4 on SA / SK / MF. converge / mixed: 0 | central and broad 4 / 4; converge, mixed, slotcollapse, cliché 0 | broad 4 / 4 only; **central 0 / 4** |
| **Constrained populations** | the 10 NOT FULLY CALIBRATABLE populations, plus the scaled subsets of SK / MF | same; bundles exist only where canon names them and the axes are scaled | same, and C needs broad coverage that does not exist |
| **False-positive risk** | very low | low. Slot coverage 0.05 sits well below the central batches' 0.11–0.20 | **high**: rejects legitimate central concentration (Subtle, C1R central, Sagekin statistical identity) |
| **False-negative risk** | **high**: passes single-slot collapse, cliché bundles and the Halvren 50/50 collapse | moderate. Only canon bundles expressible on scaled axes are checked; race Tier-G tests still carry the rest | lowest |
| **Distorts statistical identities?** | no | no — it never asks for spread beyond a clone / collapse floor | **yes**: forces spread on Sagekin / elf population identities and on central reference states |
| **Converts OPEN frequency into canon?** | no | no — thresholds are anti-collapse floors, not distribution targets | **effectively yes**: a spread floor implies a minimum distribution width that canon has not authored |

**Claude recommendation (advisory): Option B.**
- It catches every failure mode tested: clones, partial duplication, single-slot collapse and canon cliché bundles.
- It passes every valid concentration and broad batch, on all populations and seeds.
- It makes no frequency claim.

It should be paired with:
- the race-specific Tier-G tests, which stay authoritative;
- the Halvren 50/50 and source-passing shares as separate bundle diagnostics.

The numbers (0.015 / 0.010 / 0.05 / 4× / 3×) are W3-era diagnostic calibrations at N = 256 on 9–10 scaled axes. They should be re-validated when the qualitative populations gain numeric spans. **Not canonized.**

## 7. Visual evidence

- `uf05_1_healthy_diverse.jpg` — Skarn broad batch (8 of 256, front and profile).
- `uf05_2_near_clone.jpg` — Skarn converge batch (three templates).
- `uf05_3_cliche_bundle.jpg` — Skarn forced Viking bundle: pairwise distance healthy, bundle share 100 %.
- `uf05_4_sagekin_statistical.png` — statistically sensitive case on the Sagekin profile: central passes A / B and is rejected by C.
- `uf05_5_halvren_50_50.png` — Halvren 50/50 collapse passes pairwise A; the midpoint share catches it; source-passing share 100 %.
- `uf05_6_skarn_c1r_central.jpg` — Skarn C1R central batch: central tendency, Viking-bundle share 0 %.

The faces are N4-style neutralized: one grey material, no hair, brows, beard or texture, neutral expression, standardized camera. Ears are visible because they are not varied. On the narrow W3C anchor scale the differences between faces are deliberately subtle. That reflects how little numeric facial span is currently authored, not a weakness of the method.

## 8. NOT DEMONSTRATED / limits

- **Numeric facial spans:** none for 10 populations. Skarn / Marchfolk cover only 9 anchor axes, so ears, mouth, lids, forehead and chin are unscaled.
- **Halvren and elf face anchors:** not built.
- **Saurin IOD:** binding conflict (UFCA vs §267.2).
- **Generic Tier-G calibration:** not possible beyond SA / SK / MF.
- **Image-embedding similarity:** not used.
- **Cluster counts:** reported only as effective rank. No biological cluster model was invented.
- **Frequency:** OPEN everywhere.

## 9. Persistent files changed

**RM-CF-05 writeback / W3 closure (commit 029f090):**
- `specs/saurin/SAURIN_V1.md` (§268, plus §259 / §265 pointers)
- `decisions/UFCA_V1.md` (§12)
- `decisions/REFERENCE_ANATOMY_V1.md` (§7 C1R row note, §9, §10)
- `reviews/claude-ufca-06-validation-framework.md` and `reviews/claude-pass2-r3-craniofacial-framework.md` (status notes)
- `reviews/claude-rac-w3d-fpi-margin-author-gate.md` (closure status)
- `specs/skarn/SKARN_V1.md` (neck clarification)
- `specs/STATUS.md`, `reviews/claude-pass2-r5-reference-mesh-queue.md`

**RM-UF-05:**
- `reviews/claude-rac-rm-uf-05-diversity-author-gate.md` (this gate)
- `reviews/rac-rmuf05-evidence/`
- `tools/rac/w1/rmuf05_drivers/`
- `specs/STATUS.md`, `reviews/claude-pass2-r5-reference-mesh-queue.md` (status lines)

## 10. Stop

Stopped after the RM-UF-05 author gate. Not begun: RM-UF-05 canonization, RM-OT-05, posture, equipment, UE5, MetaHuman, rigging, animation and gameplay.
