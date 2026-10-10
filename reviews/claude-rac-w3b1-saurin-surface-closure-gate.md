# RAC W3B1 — Saurin surfaced-envelope closure gate

**Order:** `reviews/chatgpt-rac-w3b-author-review-w3b1-saurin-surface-closure-order.md`
**Predecessor:** `reviews/claude-rac-w3b-saurin-orbit-ridge-scale-gate.md` (W3B, CONSTRAIN)
**Evidence:** `reviews/rac-w3b1-sa-evidence/` (JSON, logs, 3 sheets, `canon_hash_check.json`)
**Scope:** diagnostic creator-biology / reference measurement only. No UE5. Nothing written to SAURIN_V1 (§11 firewall).

---

## 0. Verdicts

| Item | Verdict |
|---|---|
| **RM-UF-03 horizontal spacing** | **FINAL ACCEPT** — common creator-safe interval **IOD −8 % … +3 %** of the W2 reference. The +14.x % result on reference-width / wider crania is kept as conditional diagnostic headroom only. No interpolation between cranial width 0.92 and 1.0. No orbit rerun (§2 of the order); no contradiction appeared. |
| **Vertical / AP placement** | **REMAINS LOCKED** |
| **Surfaced ridge lower bound** | **CONSTRAIN** — at canonical relief the lowest valid surfaced m is **0.90** (first fail 0.85). With reduced facial relief it is **0.60** (first fail 0.55). The floor is relief-dependent and is set by the temporal line only (§1). m = 0.40 is **not** promoted. |
| **Ridge upper bound** | **CONSTRAIN** — **m = 1.30** is confirmed with scales on at canonical, minimum and C-R1-capped high relief (min legibility 1.43–4.06, 0–2 excess folds). It stays under C-R1, which blocks the high-ridge × high-relief armor corner. |
| **Ridge × scale clamp** | **CONSTRAIN** — **C-R1 is verified and kept**: legibility scales exactly as S_F(m) ÷ r_local in all three relief configurations, with prediction error ≤ 0.01. **C-R2 is rejected and replaced.** Its temporal clause would admit m = 0.40 at minimum relief, which fails at 0.30. Its canthal clause never binds. The replacement is one global rule (§1.4). |
| **Facial scale-field creator ranges** | **CONSTRAIN** — seed-robust ends: auricular size max ×1.3; cranial structural size max ×2.0 by metric, capped at ×1.5 visually; eyelid size max not seed-robust above ×1.0 (§3). |
| **Body scale-field creator ranges** | **CONSTRAIN** — region-specific. The articulation size maxima are measured biological bounds and are seed-stable. The large structural / ventral fields carry creator caps, not species maxima (§3–§4). |
| **Seed reproducibility** | **CONSTRAIN** — 16 boundaries closed on 2–4 extra seeds. Two fine ends (eyelid max, shin min) carry single-realization S4 failures at tolerance level (3–4 flips against a tolerance of 2). Those failures are seed-specific, not size-driven (§3). |
| **Extreme-body folding classification** | **PRODUCTION DEPENDENCY** — two mechanisms, neither biological (§2). (a) Surface transport: folds on dorsal tail, shin, dorsal trunk and the low-m surfaced head vanish when the same relief is carried along smoothed-base normals. (b) The composition deformation inverts the *unsurfaced base* in creases (24–1,997 faces per field). Every remaining surfaced fold sits on or next to those inversions (median 0.02–0.03 cm away; 93–99 % within 2 cm). No fold remains in clean skin under the corrected route. |
| **Large-unit visual caps** | **CONSTRAIN** — ×1.5 holds as the creator cap for cranial structural, dorsal / lateral trunk, dorsal tail and ventral fields, because the plate / tile read begins at ×1.75. Foot, knee and wrist show no visible failure through ×2.0, so ×2.0 there is a tested maximum with no failure, capped at ×1.5. The dorsal-hand visual is NOT DEMONSTRATED: the camera did not resolve the field. Its metric is seed-stable to ×1.75. |
| **W3B Saurin overall** | **CONSTRAIN** — every W3B1 item is closed to a bracketed number, a cap or a named production dependency. Final acceptance waits on the author's decision on the two tolerance-level seed ends and on owner assignment for the two production dependencies. |

### Required reports (§10)

1. **Numbers proposed for promotion:** §5.1.
2. **Creator-safe caps that are not species maxima:** §5.2.
3. **Construction-only values:** §5.3.
4. **NOT DEMONSTRATED items:** §6.
5. **Production dependencies:** §5.4.
6. **Persistent files changed:** §8.
7. **Accepted Saurin biology reopened:** **none.**
8. **Canonical W2 reference asset modified:** **NO.** All 8 canonical files have SHA-256 identical to the pre-W3B record (`canon_hash_check.json`, `identical: true`).

---

## 1. Surfaced ridge lower bound (primary task)

### 1.1 Method

- **Head:** canonical surfaced W2 head with canonical seeds. Ridges are changed by level-set transfer of the hidden strength m, then the canonical relief is applied, scaled per configuration.
- **Configurations:**
  - **canonical:** facial size ×1, relief ×1;
  - **minimum:** every facial field at its own minimum valid relief (cranial ×0.40, so the local temporal relief is about ×0.42);
  - **high:** every facial field at its maximum valid relief, limited by C-R1 at m = 1 (cranial ×1.18, others ≤ ×2.5).
- **Legibility:** ridge strength ÷ scale relief amplitude within 1 cm of the core. Each required family must be ≥ 1.0.
- **Eye visibility** measures scowl. **Excess folds** are counted against the canonical surfaced head; the tolerance is 2.
- **Matched-camera visual check:** front, three-quarter and profile (`sheets/w3b1_surfaced_ridge_minimum.jpg`).

### 1.2 Sweep (minimum legibility, binding family is temporal in every row; excess folds with raw normals)

| m | canonical relief | minimum relief | high relief (C-R1) |
|---|---|---|---|
| 1.30 | **1.69** / 0 | 4.06 / 2 | **1.43** / 0 |
| 1.00 | 1.18 / 0 | 2.83 / 2 | **1.00** / 0 — *lowest valid* |
| 0.95 | 1.09 / 2 | — | — |
| 0.90 | **1.00** / 3* — *lowest valid* | 2.39 / 5* | 0.85 / 2 — **first fail** |
| 0.85 | 0.91 / 3* — **first fail** | — | — |
| 0.80 | 0.82 / 2 | 1.96 / 4* | 0.69 / 0 |
| 0.70 | 0.64 / 11* | 1.53 / 15* | 0.54 / 2 |
| 0.65 | — | 1.32 / 19* | — |
| 0.60 | 0.46 / 23* | **1.11** / 26* — *lowest valid* | 0.39 / 15* |
| 0.55 | — | 0.91 / 26 — **first fail** | — |
| 0.50 | 0.29 / 23 | 0.70 / 27 | 0.25 / 17 |
| 0.40 | 0.13 / 21 | 0.30 / 25 | 0.11 / 16 |

\* Folds above tolerance at m ≥ 0.60 are **surface transport**, not skull geometry (§1.3).

Other guards, all rows:
- **Eye visibility** at 0° stays 0.64–0.71 against 0.66 at reference. There is no scowl, and the brow never closes onto the eye.
- **Supraorbital legibility** stays ≥ 8.0 and the canthal plane break ≥ 1.0 wherever the temporal line passes. Canthal first drops below 1.0 only at m 0.40 with canonical relief (0.53).

**Visual check** (sheet):
- **Lowest valid rows:** the skull architecture (temporal line, canthal break, platform) still reads through the scales.
- **First-fail rows:** the temporal line dissolves into the scale field. The skull edge is then carried by scale borders, which is the order's "scales become the structure" failure.
- **m 0.40 surfaced:** visibly a smoother, more generic head.
- **m 1.30:** the ridges are stronger but there is no armor read and no fold.

### 1.3 Fold firewall for the ridge sweep

The same canonical relief was carried onto each ridge-modified skin along raw normals (the W2 convention) and along normals of the 20-iteration smoothed base (`w3b1_ridge_transport.json`, whole head, z > 165).

| m | 1.0 | 0.95 | 0.9 | 0.85 | 0.8 | 0.75 | 0.7 | 0.65 | **0.6** | **0.55** | 0.5 | 0.45 | 0.4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| excess, raw normals | 0 | 2 | 3 | 3 | 5 | 8 | 17 | 21 | 34 | 48 | 55 | 70 | 92 |
| excess, smoothed normals | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **1** | **8** | 12 | 16 | 24 |

- **m ≥ 0.60:** the folds are pure transport, located at the canthal / orbital-margin crease (head-local about (±3.9, 9.35, 5.0)). They fold into **PD-1**.
- **Below 0.60:** folds persist with the corrected transport. The softened skull compresses the orbital-margin crease below what canonical relief can sit on.
- That geometric limit agrees with the legibility floor at minimum relief (first fail 0.55). **0.60 is therefore a two-sided-evidence absolute surfaced floor.**

### 1.4 Returned values and the relationship rule

| Return item | Value |
|---|---|
| Lowest valid surfaced m, canonical relief | **0.90** (first demonstrated invalid **0.85**: temporal 0.91) |
| Lowest valid m with reduced relief | **0.60** (first demonstrated invalid **0.55**: temporal 0.91 plus 8 geometric folds) |
| Lowest valid m, high relief at the C-R1 cap | **1.00** (first demonstrated invalid **0.90**: temporal 0.85) |
| Naked-skull diagnostic minimum (W3B) | 0.40 — not a creator bound |

**Relationship-aware rule (replaces C-R2; C-R1 retained):**

> **m ≥ max(0.60, m_T(r_T))**, where m_T is the lowest m at which the temporal line keeps legibility ≥ 1.0 for the local temporal-region relief multiplier r_T. Equivalently, C-R1 for the temporal family: r_T ≤ 1.18 × S_T(m) ÷ S_T(1).

- **W2 calibration (construction-only):**
  - S_T is linear in m over 0.40–1.30: legibility at r = 1 is 1.75 m − 0.57 (residual ≤ 0.02);
  - so m_T(r) = 0.33 + 0.57 r_T;
  - this gives 0.90 at r 1, 1.00 at r 1.18 and 0.56 at r 0.42, where the floor of 0.60 governs.
- **Prediction check against the sweep:**
  - minimum relief: m 0.60 predicts 1.10 (measured 1.11); m 1.30 predicts 4.05 (measured 4.06);
  - high relief: m 0.90 predicts 0.85 (measured 0.85).
- **Upper side:** m ≤ 1.30. C-R1 also caps relief at high m, so high ridge × high relief cannot become armor. The W3B I4 corner at legibility 0.57 is rejected by the same rule.

**Global vs regional control.** One global ridge control **remains defensible**. The temporal line is the only family that binds in any tested configuration. The canthal plane break passes wherever the temporal line passes, so a separate canthal floor is not needed. The floor must be **relief-dependent** (the rule above), not a constant. A fixed global 0.40 is wrong with scales on. A fixed global 0.90 would wrongly forbid low-relief / low-ridge heads, which are valid down to 0.60.

---

## 2. Extreme-body folds — biology vs transport firewall

### 2.1 Routes

All routes use the same field identity, size / relief multipliers and seed indices (`w3b1_transport.json`):
- **R0 carried:** the W2 convention (canonical relief along the body's raw normals);
- **R1 re-evaluated:** the W2 generator core re-run on the deformed base, with the same seeds, R scaled by stature and the flow projected to the new tangent planes;
- **R2:** R1 along smoothed-base normals;
- **R3:** R0 along smoothed-base normals.

**Bodies:** SA-M188 (reference), high muscle (MUHI), high fat (FAHI), Narrow + high fat (N-FAHI). 10 fields.

**Base inversion:** a base face whose orientation opposes the canonical base face, i.e. the unsurfaced skin itself folded by the composition deformation. These inversions are reported apart from the surface layer (`w3b1_transport_split.json`, `w3b1_transport_dist.json`).

### 2.2 Results (excess surfaced folds over the canonical count; tolerance max(2, 10 %))

| Body / field | Base inverted | R0 | R1 | R2 | R3 | Class |
|---|---|---|---|---|---|---|
| SA-M188, all 10 fields | 0 | 0 | 0 | ≤ 1 | ≤ 1 | clean |
| MUHI dorsal tail | 0 | 22 | 18 | −151 | −150 | **transport** |
| MUHI dorsal trunk | 0 | 4 | 7 | −3 | −3 | **transport** |
| FAHI / N-FAHI shin | 0 | 19 / 24 | 19 / 27 | −1 / −1 | −1 / −1 | **transport** |
| FAHI / N-FAHI dorsal tail | 3 | 231 / 247 | 226 / 227 | −76 / −74 | −52 / −39 | **transport** |
| FAHI / N-FAHI dorsal trunk | 12 / 8 | 22 / 18 | 28 / 26 | 16 / 16 | 13 / 9 | transport + base |
| MUHI axilla | 1,997 | 436 | 458 | 414 | 405 | **base inversion** |
| MUHI neck flexion | 1,142 | 319 | 346 | 303 | 293 | **base inversion** |
| FAHI / N-FAHI lateral trunk | 1,802 / 1,822 | 451 / 455 | 406 / 403 | 348 / 344 | 482 / 486 | **base inversion** |
| FAHI / N-FAHI dorsal hand | 636 / 640 | 447 / 449 | 437 / 442 | 292 / 290 | 392 / 391 | **base inversion** |
| FAHI / N-FAHI lower-trunk flexion | 1,218 | 103 / 108 | 117 / 119 | 104 / 107 | 90 / 98 | **base inversion** |
| FAHI / N-FAHI tail articulation | 168 / 164 | 85 / 87 | 79 / 76 | 71 / 72 | 80 / 85 | **base inversion** |
| FAHI / N-FAHI axilla | 44 / 24 | 3 / 3 | 8 / 9 | 12 / 9 | 27 / 12 | base inversion (small) |

**Where the residual folds sit.** Folds that survive R3 on faces whose own base is not inverted lie a median of 0.020–0.027 cm from the nearest inverted base face. 93–99 % lie within 2 cm (MUHI axilla, FAHI lateral trunk, FAHI lower-trunk flexion, N-FAHI dorsal hand). They are the fringe of the base fold, not independent surface failures.

**Visual check** (`sheets/w3b1_extreme_transport.jpg`):
- **Unsurfaced base column:**
  - MUHI axilla shows a self-crossing sheet;
  - FAHI shin shows a deep base groove;
  - FAHI lateral trunk and lower-trunk flexion show compressed crease shelves.
- **R0:** crease lines appear on the MUHI dorsal tail and the groove edges are jagged.
- **R3 / R2:** the tail and shin surfaces are clean. The crease regions remain broken because the base under them is broken.

### 2.3 Classification

- **No genuine biological conflict was found.** Wherever the body base is clean, canonical scale biology (×1 size and relief, canonical seeds) sits on every accepted extreme without folding once it is transported correctly. Scale biology can therefore exist on the accepted bodies.
- **PD-1 surface transport:** carrying relief along raw per-vertex normals folds in compressed or high-curvature skin. The diagnostic fix (smoothed-base normals, 20 iterations) removes it.
- **PD-2 composition-deformation base inversion:** the composition deformation folds the unsurfaced base in deep creases (axilla, neck flexion, lateral trunk, lower-trunk flexion, dorsal hand, tail articulation) on MUHI / FAHI / N-FAHI. That is a body-deformation production defect upstream of any scale system. It is reported, not fixed. No frame or composition limit was changed.
- **C-B1 is withdrawn as biology.** At most it is a temporary production exposure guard until PD-1 / PD-2 are resolved. It is not a Saurin scale rule.

---

## 3. Seed-stability closure

The canonical 130,949-seed realization is untouched. Extra realizations: rng 1007 / 2007 / 3007 / 4007 (`w3b1_seeds.json`, `w3b1_seeds2.json`, `w3b1_seeds3_raw.json`).

### 3.1 Six W3B unstable ends

| Boundary | W3B canonical-seed end → seed-robust step | W3B1 result on extra seeds | Stable end (creator-safe candidate) |
|---|---|---|---|
| Cranial structural size max | 2.5 → 2.0 | 2.0 valid 4 / 4; 2.5 fails S5 crowding 2 / 2 | **×2.0** by metric (visual cap ×1.5, §4) |
| Axilla size max | 1.3 → 1.2 | 1.2 valid 4 / 4; 1.3 valid 2 / 2, but failed one W3B seed | **×1.2** |
| Palmar size max | 1.3 → 1.2 | 1.2 valid 4 / 4; 1.3 fails S2 hierarchy 2 / 2 (true boundary) | **×1.2** |
| Auricular size max | 1.75 → 1.5 | 1.5 fails on rng 1007: S0, the generator produced no units. 1.75 fails on rng 3007 (S0). Inward step 1.3 valid 4 / 4 | **×1.3** (the 1.5 failure is a generator dependency, PD-4) |
| Eyelid size max | 1.5 → 1.3 | rng 1007 fails S4 at both 1.2 and 1.3 (3 flips, tolerance 2) but passes at 0.9 and 1.0 (1 flip). The other three seeds pass at 1.2 / 1.3, and 1.5 passes on 3007 / 4007 | **×1.0 strictly seed-robust.** ×1.2–1.3 is MARGINAL: one realization exceeds the fold tolerance by one face |
| Shin size min | 0.5 → 0.6 | rng 4007 fails S4 at 0.5, 0.6 and 0.7 (3–4 flips) and passes at 0.8 and 1.0. The other seeds pass down to 0.6 | **×0.8 strictly seed-robust.** ×0.6–0.7 is MARGINAL on one realization |

The W3B seed-robust step held for cranial, axilla and palmar. It did **not** hold for eyelid and shin. Their failures depend on the seed, not on size: the same realization fails across a run of sizes at 3–4 sliver-level flips while every other realization passes, including at more extreme sizes. They are reported as tolerance-level realization noise (PD-3). The author must choose between two options:
- adopt the strict ends (eyelid ≤ ×1.0, shin ≥ ×0.8);
- or accept a 4-face fold tolerance for fine fields and keep ×1.3 / ×0.6.

### 3.2 Ten large fields (W3B NOT RUN), rng 1007 / 2007

| Field | Size cap → result | Stress point → result | Relief end → result |
|---|---|---|---|
| Dorsal trunk | 1.5: 2 / 2 | 1.75: 2 / 2 (metric) | 1.0: 1 / 2 (rng 1007 fails S4 at the *canonical* point, 5 flips — PD-3) |
| Lateral trunk | 1.5: 2 / 2 | 1.75: 2 / 2 | 1.0: 2 / 2 |
| Dorsal tail | 1.5: 2 / 2 | 1.75: 2 / 2 | 1.0: 2 / 2 |
| Neck flexion | 1.5: 2 / 2 | 1.75: 2 / 2 | **1.25: 0 / 2** (aspect 0.300–0.301 against the 0.30 limit) → seed-robust relief max **×1.0** |
| Lower-trunk flexion | 1.3: 2 / 2 | 1.5: fails S2 2 / 2 (measured bound confirmed) | 1.5: 2 / 2 |
| Hip crease | 1.5: 2 / 2 | 1.75: fails S2 2 / 2 (confirmed) | 1.5: 2 / 2 |
| Tail articulation | 1.5: 2 / 2 | 1.75: fails S2 2 / 2 (confirmed) | 1.5: 2 / 2 |
| Chest / abdomen | 1.5: 2 / 2 | 1.75: 2 / 2 | 1.5: 2 / 2 |
| Tail underside | 1.5: 2 / 2 | 1.75: 2 / 2 | 1.5: 2 / 2 |
| Dorsal hand | 1.5: 2 / 2 | 1.75: 2 / 2 | 1.0: 2 / 2 |

No conclusion changed except neck-flexion relief max, which moves from ×1.25 to ×1.0 because ×1.25 sits on the C-B2 aspect threshold. No full re-sweep was needed.

---

## 4. Large-unit "not reached" ends — visual brackets

`sheets/w3b1_large_unit_caps.jpg`: size ×1.0 / 1.25 / 1.5 / 1.75 / 2.0, reseeded field (rng 7), relief ×1, matched close camera per row.

| Field (class) | ×1.5 read | ×1.75 read | Category |
|---|---|---|---|
| Cranial structural | Plates still follow the plane breaks | Plates bridge the cranial edge; mosaic read turns to plating | creator cap **×1.5** (metric bound ×2.0; 2.5 fails S5) |
| Dorsal trunk | Large but graded, with fine margins kept | Tile / armor read; the size gradient toward the flank is lost | creator cap **×1.5** (tested ×2.5 / ×1.75 seeds, no metric failure) |
| Dorsal tail | Acceptable | Flat tiles, facet stretching | creator cap **×1.5** |
| Chest / abdomen (ventral) | Wide transverse plates still read as ventral | Plates merge into broad shields at ×2.0 | creator cap **×1.5** |
| Tail underside (ventral) | Acceptable | Coarse but not failed | creator cap **×1.5**; tested maximum ×2.0 with no failure |
| Knee, wrist (articulation) | No change of read | No visible failure through ×2.0 (fine units, low exposure) | tested maximum ×2.0, no failure; creator cap **×1.5** |
| Dorsal foot | No change of read | No visible failure through ×2.0 | tested maximum ×2.0, no failure; creator cap **×1.5** |
| Dorsal hand | Not resolved by the camera | — | visual NOT DEMONSTRATED; metric seed-stable to ×1.75; creator cap **×1.5** |

The three categories are kept apart:
- **Measured biological failure bounds:** demonstrated first-invalid and seed-stable (§5.1).
- **Creator-safe exposure caps:** visual ×1.5 where no failure was reached (§5.2).
- **Tested maxima with no failure:** ×2.5 W3B metric, ×1.75 seed metric, ×2.0 visual (§6).

---

## 5. Classification

### 5.1 Safe to promote if the author accepts

- **Orbit:** horizontal IOD **−8 % … +3 %** of the W2 reference.
- **Ridge:** hidden strength **0.60 … 1.30** with scales on, under the rule **m ≥ max(0.60, temporal-legibility floor)**. Equivalently: C-R1 (r_local ≤ L_F(1) × S_F(m) ÷ S_F(1)), with the temporal family binding. At canonical relief this means m ≥ 0.90.
- **Measured, seed-stable size bounds:**
  - palmar max ×1.2;
  - axilla max ×1.2;
  - auricular max ×1.3;
  - cranial structural metric max ×2.0;
  - lower-trunk flexion max ×1.3 (fail 1.5);
  - hip crease max ×1.5 (fail 1.75);
  - tail articulation max ×1.5 (fail 1.75);
  - neck flexion max ×2.0 (W3B; fail 2.5 S1).
- **Seed-robust fine ends (strict):** eyelid size max ×1.0; shin size min ×0.8. The alternatives ×1.3 / ×0.6 apply only if the author accepts the fine-field tolerance in §3.1.
- **Relief maxima with a measured first-invalid:**
  - dorsal / lateral trunk, dorsal tail, dorsal hand ×1.0 (fail 1.25, S3 aspect);
  - neck flexion ×1.0 (revised);
  - knee, wrist, lower-trunk flexion, hip crease ×1.5;
  - tail articulation ×1.75 (seeds verified ×1.5);
  - dorsal foot ×1.75;
  - axilla ×1.5;
  - palmar ×1.75.
- **Facial and body minima:** as in W3B §6–§7, all with demonstrated first-invalid points. The two fine-end minima above are the exceptions.
- **Clamp C-B2** (relief ≤ 0.30 × unit size; hand 0.40) as a biological relationship: it is the binding relief guard on every structural field, and it was re-confirmed on extra seeds (neck flexion).

### 5.2 Creator-safe exposure caps, not species maxima

- **Size ×1.5:**
  - cranial structural;
  - dorsal trunk, lateral trunk, dorsal tail;
  - chest / abdomen, tail underside;
  - dorsal hand, dorsal foot, knee, wrist;
  - neck flexion (its measured bound is ×2.0).
- **Relief ×1.5** where W3B reached ×3.0 without failure: chest / abdomen, tail underside. On the face, relief above the C-R1 limit is capped by legibility (cranial ×1.18 at m 1.0, rising with m).
- **Tail stretch C-T1:** tail-field size multiplier × stretch ≤ field cap.

### 5.3 Construction-only

- **Orbit:**
  - absolute W2 cm values (IOD 8.883 cm, all ridge strengths in cm, unit sizes and reliefs in cm);
  - orbit warp radii (2.4 / 5.2 / 2.0).
- **Ridge construction:** level-set transfer and Newton / fairing settings (FAIR 4).
- **Transport diagnostics:** 20-iteration smoothed-normal diagnostic transport; re-evaluation route.
- **Seeds and sampling:** reseed rule (Poisson, c = 0.5, rng 7 / 1007–4007).
- **Generator:** smooth field weights; the 1.7-edge resolution limit.
- **Guard thresholds:** S1–S7, G1–G6, fold tolerance max(2, 10 %), sliver rule.
- **W2 calibration of the temporal rule:** legibility = 1.75 m − 0.57; m_T = 0.33 + 0.57 r_T.
- **Legibility constants:** the L_F(1) values (1.18, 1.94, 2.57 …).

### 5.4 Open production dependencies

| ID | Dependency | Evidence | Status |
|---|---|---|---|
| **PD-1** | Relief carried along raw per-vertex normals folds in compressed or curved skin (extreme bodies; surfaced head at m 0.60–0.95) | Removed by smoothed-base-normal transport (§1.3, §2.2) | OPEN; diagnostic fix identified, not implemented |
| **PD-2** | The composition deformation inverts the unsurfaced base in deep creases on MUHI / FAHI / N-FAHI | 24–1,997 inverted base faces per field; residual surfaced folds are colocated (§2.2) | OPEN; upstream body-deformation issue; not a scale or biology matter |
| **PD-3** | Single-realization S4 sliver flips at tolerance level (eyelid rng 1007, shin rng 4007, dorsal trunk rng 1007 at the canonical point) | §3 | OPEN; fold-tolerance / sliver rule for reseeded fine fields |
| **PD-4** | Auricular reseed produces no units at ×1.5 (rng 1007) and ×1.75 (rng 3007) | §3.1 (S0) | OPEN; generator robustness |

---

## 6. NOT DEMONSTRATED / NOT RUN

- **Dorsal-hand large-unit visual:** the camera did not resolve the field.
- **Orbit outward tolerance between cranial width 0.92 and 1.0** (by order, not interpolated).
- **Surface on inverted base regions (PD-2):** whether canonical relief is valid there cannot be judged until the base is fixed.
- **Single-family ridge maxima above 2.5** (unchanged from W3B).
- **Fine-field size below the generator resolution** (unchanged).
- **Relief below ×0.5 on the composition extremes:** unchanged, and now moot because C-B1 is withdrawn as biology.
- **NOT RUN:**
  - vertical / AP orbit (locked);
  - SA-F188 surfaced-ridge sweep (species-level; §263 is soft tissue only);
  - smoothed-normal transport as a production route (diagnostic only).

## 7. Cross-canon audit (§12)

| Reference | Result |
|---|---|
| SAURIN_V1 (§36a, 42–45 cranial identity and orbit / eye coupling; §79–85, 94–99 ridge-and-plane and Regional Scale Architecture; §100–102 display; §259–265) | **Kept:** <br>• The surfaced floor *strengthens* §79–85: ridges must stay legible through the scales, so scales never carry skull identity. <br>• The hierarchy is preserved: the articulation S2 bounds are confirmed on seeds. <br>• Display untouched (naked state). <br>• No frame or composition limit changed (§2.3). <br>• No numbers written into SAURIN_V1. |
| UFCA_V1 / UCCA_V1 | No sex-, frame- or composition-specific scale bound created. C-B1 is withdrawn as biology. |
| REFERENCE_ANATOMY_V1 | No new landmark or reference mesh. Legibility remains a measurement proxy. |
| W2I6 canonicalization | Canonical asset unchanged (hash check identical). |
| W2I4 scale-field realization | 130,949 seeds remain canonical. Extra realizations are diagnostic only. PD-1 and PD-2 are documented as properties of the W2 carried-relief convention and the composition deformation, not of the realization. |
| TS6 ridge architecture | Amplitude-only changes on the BROW_INT 5 skull, as in W3B. The temporal line is confirmed as the binding family. |
| Creator register (A12 ≤ ±3 %, A32 ±20 / ±25 %, fine ±10 %) | History only. A12 is superseded by the −8 / +3 % candidate. A32 structural ranges are region-specific with ×1.5 creator caps. Fine-field size spans ×0.8–1.0 strict and ×0.6–1.3 if the tolerance is accepted. |
| W3B gate / tables | **Changed by W3B1:** <br>• surfaced ridge minimum 0.40 → 0.60 absolute / 0.90 at canonical relief; <br>• C-R2 rejected and replaced; <br>• neck-flexion relief max 1.25 → 1.0; <br>• eyelid / shin seed-robust ends tightened; <br>• auricular 1.5 → 1.3; <br>• C-B1 reclassified as a production guard. <br>**Unchanged:** all other W3B values. |

**Contradictions with accepted canon:** none. Two production dependencies (PD-1, PD-2) are surfaced, not fixed.

## 8. Persistent files changed

- `reviews/claude-rac-w3b1-saurin-surface-closure-gate.md` (this gate)
- `reviews/rac-w3b1-sa-evidence/`:
  - `surfaced_ridge_sweep.json`, `surfridge*.out`;
  - `w3b1_ridge_transport.json`;
  - `w3b1_transport.json`, `w3b1_transport_split.json`, `w3b1_transport_dist.json`;
  - `w3b1_seeds.json`, `w3b1_seeds2.json`, `w3b1_seeds3_raw.json`;
  - `canon_hash_check.json`;
  - `sheets/`: surfaced ridge minimum, large-unit caps, extreme transport.
- `tools/rac/w1/w3b_drivers/`:
  - new: `w3b1_transport.py`, `w3b1_transport_split.py`, `w3b1_transport_sheet.py`, `w3b1_ridge_transport.py`, `w3b1_ridge_sheet.py`, `w3b1_seeds.py`, `w3b1_seeds2.py`, `w3b1_caps.py`;
  - modified: `w3b_interact.py` (rC1 configuration, excess-fold metric, results file via `W3B_IX`), `AS_RUN.sh`.
- `tools/rac/w1/cfg/w3b/SA-surface.json`: W3B1 block added.
- `specs/STATUS.md`, `reviews/claude-pass2-r5-reference-mesh-queue.md`: status lines.
- **Not changed:** SAURIN_V1, the canonical W2 asset, the creator register.

## 9. Stop

W3B1 stops here for author review. Nothing else was started: no W3C, RM-CF-09, RM-CF-05, RM-UF-05, RM-UF-01 / 02 closure, claw ranges, density model, posture, world-space tail review, roster review, creator, UE5, rigging, animation, equipment or gameplay work.
