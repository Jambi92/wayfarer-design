# RAC RP3 — Halvren ear family closure after HR2

**Order:** `reviews/chatgpt-rac-rp3-halvren-ear-family-closure-after-hr2-order.md` (94eabf1; reviewed commit ee0e98c).
**Evidence:** `reviews/rac-rp3-evidence/halvren_rp3_ear_family_closure/`

| File | Contents |
|---|---|
| `HALVREN_HE2_HR2_FREEZE.json` | HE2 + HR2 freeze record |
| `HV_ear_family_closure_record.json` | consolidated record: technical, silhouette / root sectors, domains, firewall, decomposition, family, trials (HE3 56, HE1 size 12, HE1 identity 30), determinism, frozen-ear rebuild |
| `HV_ear_family_prodcheck.json` | mirroring / export / LOD |
| `boards/HVF_A..F` | A HE3 firewall, B HE3 HR2 root gate, C HE3 body context, D HE1 size floor, E family lineup, F HE3 decomposition |
| `records/` | per-build build / audit / deform / guard / repair / measure: final HE1 / HE2 / HE3 c1 / c2, and the HE1 L 5.3 edge test (`L53_*`) |
| `HV_ear_definitions_HVEAR4.json` | ear definitions (final, before-states, test bodies) |
| `folded_cuff_quads_audit.json` | folded-quad audit, all ears incl. frozen references |
| `immutable_hashes.txt` | 16 / 16 unchanged |
| `blind_family_review.md` | five independent blind reviews and the action taken after each |

**Tools** (`tools/rac/rp/halvren_rp3_v001/`):
- `hv_ear_family_closure.py EVIDIR` — record;
- `hv_ear_family_boards.py EVIDIR OUT` — boards;
- `hv_cuff_repair.py` — Halvren realization-path repair, new stages:
  - 3: symmetric sheet stretch repair (aspect > 9.8; junction fixed);
  - 4: symmetric relaxation of folded auricle-sheet quads;
  - 5: cuff-crease relaxation (edges > 120°) with corner / aspect / no-new-crossing / no-new-fold guards.
  - Stages 4 / 5 run only when the ear's geo sets `sheet_fold_fix` (HE1, HE3). HE2 is unflagged and untouched.

**Library** (`fenn_rp3_v001`; Fenn / Aelari / Vael rebuilt dV 0):
- `ear_branch_lib.py`:
  - HE1 and HE3 are HVEAR4;
  - before-states kept: `HE1-HVEAR3`, `HE3-HVEAR3`, `HE1-R3` (the round-3 HE1);
  - `HE1-HS` is the layout-metric test body.
- `ear_build.py`: probe keys `clear`, `helix_h`, `helix_w` (inert unless set).

## FINAL DISPOSITION

**HALVREN EAR FAMILY FREEZE RECOMMENDED**

- **HE2 + HR2:** freeze recorded (`HALVREN_HE2_HR2_FREEZE.json`); HE2 rebuilt with the final code reads back dV 0.
- **HE3 (HVEAR4):** firewall R² **0.64 / 0.61 / 0.27** (MF ↔ Fenn / Aelari / Vael; c2 0.59 / 0.58 / 0.31), down from 0.88. Still the elf-forward extreme (composite 0.85). Clean on c1 / c2, 8 poses clean, one auricle on HR2.
- **HE1:** **HE1 SIZE FLOOR ACCEPTED AS CANONICAL FAMILY BOUND** at the revised floor **L 5.6 ≈ Marchfolk +10–13 %** (was +27 %), on the shared production path. No dedicated human-scale scaffold is required: Path B was tested and is worse.
  - HE1 now has a human-family outline: upright, rounded, soft apex, rolled helix.
  - Firewall R² 0.22 / 0.17 / 0.12.
- **Family:** HE1 0.46 < HE2 0.65 < HE3 0.85, non-lockstep (outline and rim type change; projection / backward angle non-monotone).
- **Frozen references:** 16 / 16 hashes unchanged; Fenn / Aelari / Vael rebuild dV 0.
- **Author-facing visual review:** two consecutive independent blind reviews return **FINAL FAMILY LINEUP: PASS** (rounds 4 and 5, after three failing rounds that drove the HE3 rim / interior, the sheet-fold / cuff-crease repairs and the HE1 outline).
- **Residual author-taste item (not a gate):** HE3 separates from HE2 mainly by height and tip (round 5: BORDERLINE). Further separation was tested and is limited by the shared sheet, the HR2 head clearance and the firewall (§3, review log).

## 1. HE2 + HR2 freeze recorded (§1)

- **Record.** `HALVREN_HE2_HR2_FREEZE.json` freezes the ee0e98c state by record. It holds:
  - authority 94eabf1 §1;
  - the HE2 definition, `HV_ROOT2` and `HV_SKIN`;
  - topology and build path;
  - per-configuration realization hashes (branch npz sha256, V float32 sha256, face sha256 `f8367ab0…`);
  - the closed gates, and the polish items marked non-blocking;
  - the firewall (0.51 / 0.44 / 0.23);
  - tool hashes at ee0e98c.
- **Read-back.** HE2 rebuilt on c1 and c2 with this pass's final code (library, probe keys, repair stages 3–5): dV 0, faces identical. The V float32 hashes equal the freeze record (`immutable_hashes.txt`).
- **Canon pointers:**
  - `specs/halvren/HALVREN_V1.md` (RP3 ear status);
  - `specs/STATUS.md`;
  - `reviews/claude-session-handoff.md`.
- **Not reopened:** the HE2 root, HE2 morphology and HR2.
  - No correction to HE1 / HE3 exposed a shared-root defect.
  - The shared polish items are listed in §10.

## 2. HE3 root-cause diagnosis (§4)

**One-alpha fit of HVEAR3 HE3 on HR2 (the "before"),** in source-SD units on the common c1 head:

| Pair | R² | α | n | Domains carrying the fit |
|---|---|---|---|---|
| MF ↔ Fenn | **0.883** | 0.897 | 11 | width / L, tragus height, upward extension, tip angle |
| MF ↔ Aelari | 0.782 | 0.791 | 10 | upward extension, width / L, length, tip angle |
| MF ↔ Vael | 0.473 | 0.753 | 11 | tip angle, backward angle, length, upward extension |

Residuals by domain for every pair, before and after, are in `decomposition` in the record and on board F.

**Why HE3 moved from Aelari-like to Fenn-like after HR2.** The root line changed.
- Under HR1, HE3's anterior attachment line leaned backward (y = −1.95 SD). That is opposite to Fenn (dx +0.54). It was the largest Fenn residual (−2.40), and it held MF ↔ Fenn at R² 0.76.
- HR2 seats the auricle on the head, so the line became near-vertical / forward (y = +1.21). That removed the residual, and MF ↔ Fenn rose to 0.88.
- At the same time, HR2's lobe-edge lift (0.30) opened a lobe residual against Aelari (dx +2.73), so MF ↔ Aelari fell 0.87 → 0.78.

**Why it collapses onto an elf line at all.** HVEAR3 HE3 moved elf-ward in every domain that defines an elf ear, at roughly one common scale:
- long (t 1.06);
- narrow (t 1.75);
- elevated (t 1.45);
- sharp (t 0.96);
- projecting (t 0.69);
- backward (t 0.69);
- helix fullness elf-ward (t 0.49).

The root line was the only domain breaking that pattern, and HR2 removed it.

## 3. HE3 correction — HVEAR4 (§5)

**Strategy: cross-domain recombination, not scalar interpolation.**
- **Kept elf-forward:** the extreme length (L 8.2), the most elevated upper extension of the family (t 1.52, beyond the elf mean), and a sharp point (tip 64°).
- **Placed on a Halvren human-family body:**
  - broad base (wb 1.95 → 2.10);
  - full-shouldered helix (taper 0.42 / 1.05 / 0.10 → 0.50 / 1.25 / 0.15): helix fullness 0.737, *fuller than the Marchfolk auricle*, while the tip stays sharp;
  - low projection (26 → 20°);
  - moderate tilt / sweep (14 / 1.5 → 12 / 1.0).
- **Its own surface (round-1 blind review):** an elven-derived crisp blade rim (0.22 × 0.20) and stronger antihelix / crura / crus (0.40 / 1.5 / 0.22).
- **Root:** the upper attachment is lifted 0.55 cm (`lift_top`), so the fuller upper helix clears the HR2-seated head on c2; without it there were 15–37 self-intersections. HR2 otherwise as before (sulcus off for HE3).

**Calibration:** 56 rest-state trials (`HE3_trials`).
- Taper-only changes self-intersected at the upper attachment.
- Sweep / projection / base width alone stalled at R² 0.66–0.70.
- 18 outline trials that tried to separate HE3 further from HE2 either self-intersected, re-aligned with an elf line (R² 0.73–0.88), or stayed at normalized-silhouette IoU ≥ 0.83 with HE2.

**Domains (HE3 before → corrected; t = 0 Marchfolk, 1 = elf mean):**

| Domain | MF | Fenn | Aelari | Vael | HE2 | HE3 before (t) | **HE3 corrected (t)** |
|---|---|---|---|---|---|---|---|
| length / HH | 0.240 | 0.363 | 0.406 | 0.344 | 0.328 | 0.378 (1.06) | **0.381 (1.07)** |
| width / length | 0.541 | 0.372 | 0.410 | 0.480 | 0.388 | 0.330 (1.75) | **0.345 (1.62)** |
| projection | 6.5° | 52.5° | 30.5° | 38.7° | 18.6° | 30.0° (0.69) | **19.7° (0.39)** |
| upward extension / HH | 0.015 | 0.089 | 0.108 | 0.056 | 0.090 | 0.116 (1.45) | **0.121 (1.52)** |
| backward angle | 4.8° | 21.1° | 24.7° | 28.0° | 14.6° | 18.5° (0.69) | **14.2° (0.48)** |
| tip angle | 123.5° | 52.9° | 54.4° | 64.2° | 82.6° | 59.5° (0.96) | **64.0° (0.90)** |
| lobe fraction | 0.046 | 0.103 | 0.136 | 0.112 | 0.051 | 0.069 (0.33) | **0.072 (0.36)** |
| root line | −1.5° | 2.9° | 1.5° | −17.7° | 0.1° | 8.5° | **8.3°** |
| concha depth / L | 0.268 | 0.236 | 0.168 | 0.218 | 0.195 | 0.220 (0.80) | **0.197 (1.17)** |
| tragus height | 0.404 | 0.274 | 0.350 | 0.355 | 0.289 | 0.291 (1.46) | **0.291 (1.46)** |
| helix fullness | 0.697 | 0.621 | 0.610 | 0.607 | 0.758 | 0.655 (0.49) | **0.737 (−0.47)** |

## 4. HE3 firewall (§6)

| Pair | Before: R² / α / n | **Corrected c1: R² / α / n** | Corrected c2: R² / α / n | Limit |
|---|---|---|---|---|
| MF ↔ Fenn | 0.883 / 0.897 / 11 | **0.643 / 0.750 / 11** | 0.593 / 0.751 / 11 | < 0.80 |
| MF ↔ Aelari | 0.782 / 0.791 / 10 | **0.612 / 0.685 / 10** | 0.580 / 0.707 / 10 | < 0.80 |
| MF ↔ Vael | 0.473 / 0.753 / 11 | **0.272 / 0.559 / 11** | 0.314 / 0.627 / 11 | < 0.80 |

- **Margin:** at least 0.16 below 0.80 on every pair, on both heads.
- **What breaks the fit now:**
  - helix fullness (+2.6 / +2.7 SD residual against Fenn / Aelari);
  - upward extension (+1.2 to +1.4);
  - width / L, projection and concha vs Fenn;
  - tragus and lobe vs Aelari.
- **Distinct domains (> 0.5 SD):** 7 vs Fenn, 8 vs Aelari, 10 vs Vael, 7 vs HE2, 11 vs Marchfolk.
- **Still the elf-forward extreme:** composite elf-ward position HE1 0.46 < HE2 0.65 < **HE3 0.85**.

## 5. HE3 technical / deformation / root (§6, §10)

| | HE3 c1 | HE3 c2 |
|---|---|---|
| components / boundary / non-manifold / degenerate / outward | 1 / 0 / 0 / 0 / yes | 1 / 0 / 0 / 0 / yes |
| branch self-intersections | 0 | 0 |
| min corner / max aspect | 13.8° / 9.92 | 12.8° / 9.01 |
| root valence 4 × 52 both sides | yes | yes |
| 8 deformation poses (contacts / flips / root inversions) | 0 | 0 |
| deformation guard iterations | **2** (3 → 10 guarded faces; logged) | 0 |
| repair | stage 1; stage 4 folds 18 → 6 (≤ 0.11 cm); stage 5 creases 9 → 0 (worst 157 → 120°, ≤ 0.11 cm) | stage 4 18 → 6; stage 5 10 → 0 (161 → 103°) |
| clearance min | 0.20 cm | 0.19 cm |
| HR2 pedestal p90 posterior / inferior; loop crease | 0.38 / 0.41 cm; 10 / 6° | 0.30 / 0.27 cm; 11 / 8° |
| mirroring (sheet max / mean; connectivity) | 0.058 / 0.0001 cm; identical | 0.059 / 0.0001 cm; identical |
| export / reload | dV 6e-6 cm, faces equal | same |
| LOD 50 / 25 % | 0 non-manifold, 0 zero-area | same |
| determinism | dV 0, faces identical | dV 0, faces identical |

**Visual (boards B, C).**
- Strict side, true rear 3/4, direct rear, lower-rear 3/4, the Board-E 3/4 camera and the lower anterior root all show one auricle on c1 and c2: no flange, no lower fork, no notch.
- In body context it stands as the elf-forward Halvren ear: longer and more elevated than HE2, upright and broad, never the swept horizontal blade of the elf families.

## 6. HE1 size-floor investigation (§7–§8)

**Cause, tested cleanly.** The HVEAR3 "floor" (L 6.3, +23–27 %) is not a structural limit of the shared sheet.
- With HR2, shorter HE1s are clean in every gate except one: 2–20 **anterior-cavum front-sheet quads** cross aspect 10 (10.04 at L 5.9, 10.25 at 5.6, 10.52 at 5.3, 11.24 at 5.0).
- There are no self-intersections, and min corners stay ≥ 12.5°.

Rest-state sweep on c1 (`HE1_size_trials`):

| HE1 length | Measured length vs Marchfolk | Shared layout: max aspect / T4 | Human-scale layout metric (Path B scaffold test): max aspect / T4 | + stage-3 sheet stretch repair (shared layout) |
|---|---|---|---|---|
| 6.3 (HVEAR3) | +23 % | 9.78 / 344 (clean) | 14.09 / 171 | — |
| 5.9 | +16 % | 10.04 / 393 | — | — |
| 5.6 | +10 % | 10.25 / 458 | 12.70 / 191 | **9.94 (c1 + c2 guarded: clean)** |
| 5.3 | +5 % | 10.52 / 498 | 11.94 / 192 | 9.973 / 9.999 (c1 / c2: at the gate) |
| 5.0 | 0 % | 11.24 / 551 | 12.55 / 213 | 9.99 (rest) |

**Path B (dedicated human-scale scaffold), tested at minimum viable scope.** The same connectivity, with vertex positions optimised in a human-scale metric (`EAR_LAYOUT_METRIC=HE1-HS`).
- It halves the T4 angle violations.
- But it makes the worst aspect worse (11.9–14.1), even at L 6.3.
- Scaling the concha seat with length does not help (`C*` trials).
- So a separate scaffold is not the fix.

**What works** is a bounded sheet stretch repair inside the existing Halvren realization path (`hv_cuff_repair.py` stage 3):
- a symmetric per-vertex tangential search on the offending front-sheet quads, with junction vertices fixed;
- ≤ 0.09 cm moves;
- same connectivity, same family authoring controls;
- inert on HE2 (freeze read-back dV 0).

**Path A judged visually (board D).**
- At L 6.3 (the old floor), HE1 reads as a slightly scaled HE2, not as a human-forward member (blind review round 1: "plainly a shrunken HE2").
- Accepting +23–27 % as the canonical human-forward minimum would make the human-forward bound an elf-sized ear.

**Identity (blind reviews 1–4, `HE1_identity_trials`).** Size alone did not separate HE1 from HE2: the L 5.6 size-only column still reads as a shrunken HE2. Final HE1 HVEAR4 is L 5.6 with a human-family outline:
- upright: tilt 12 → 9, sweep 0.65 → 0.45;
- a rounded, egg-shaped upper ear with only a soft Halvren apex: taper 0.54 / 0.85 / 0.12 → 0.52 / 0.70 / 0.06;
- a fully rolled human helix: 0.30 × 0.30 → 0.38 × 0.40;
- a longer lobe gate (0.19 → 0.24) for a smooth rim-to-lobe line;
- base wb 2.15, concha 1.00.

| | HE1 c1 | HE1 c2 |
|---|---|---|
| measured length vs Marchfolk | **+13 %** | — |
| firewall R² MF ↔ Fenn / Aelari / Vael | 0.22 / 0.17 / 0.12 | 0.28 / 0.22 / 0.16 |
| integrity (1 / 0 / 0 / 0 / outward) | yes | yes |
| branch self-intersections | 0 | 0 |
| min corner / aspect | 12.4° / 9.79 | 12.7° / 9.55 |
| root valence | 4 × 52 | 4 × 52 |
| 8 poses | clean | clean |
| guard iterations | 0 | 0 |
| repair | stage 1 (1 sliver); stage 3 (21 sheet quads → aspect < 10); stage 4 folds 28 → 7; stage 5 creases 7 → 1 (150 → 140°) | stage 3; stage 4 24 → 8; stage 5 13 → 0 (151 → 116°) |
| clearance | 0.23 cm | 0.18 cm |
| mirroring | 0.036 cm max, mean 0.0001, identical | 0.035 cm max, mean 0.0001, identical |
| export / LOD | pass | pass |
| determinism | dV 0, faces identical | dV 0, faces identical |

**HE1 SIZE FLOOR ACCEPTED AS CANONICAL FAMILY BOUND** — at the revised floor:
- The shared production path reaches **L 5.6 ≈ Marchfolk +10–13 %**, not the old +27 %.
- No dedicated human-scale scaffold is required: Path B was tested and is worse; the shared path with the stage-3 repair is clean on c1 / c2.
- The remaining +10–13 % is a modest, deliberate Halvren trait. Even the most human-forward Halvren ear is slightly larger than Marchfolk, with a soft point.
- L 5.3 (+5 %) is the edge (aspect 9.999 on c2); Marchfolk size (L 5.0) is reachable at rest but not robustly.

## 7. Final HE1 / HE2 / HE3 lineup (board E)

| | HE1 (HVEAR4) | HE2 (frozen) | HE3 (HVEAR4) |
|---|---|---|---|
| length vs Marchfolk | +13 % | +37 % | +59 % |
| composite elf-ward | 0.46 | 0.65 | 0.85 |
| best firewall R² (c1) | 0.22 (MF ↔ Fenn) | 0.51 (MF ↔ Fenn) | 0.64 (MF ↔ Fenn) |
| outline | upright, rounded egg-shaped upper ear, soft apex | leaning leaf, controlled shouldered point | tall upright lancet, sharp point on a full-shouldered broad helix |
| rim | fully rolled human helix | balanced roll | crisp elven blade rim |

- **Ordering:** HE1 < HE2 < HE3 holds.
- **Not lockstep:**
  - the outline type changes (rounded → leaf → lancet);
  - so does the rim (rolled → balanced → blade);
  - projection and backward angle are non-monotone: HE3's 19.7° / 14.2° sit at or below HE2's;
  - helix fullness: HE3 is fuller than any elf, close to HE2.
- **Shared:** one topology, one HR2 root path, one base / lobe language.

**Author-facing visual review (`blind_family_review.md`).** Five fresh independent reviewers each saw only the boards and the order's role definitions, never this report.

| Round | Verdict | Drove |
|---|---|---|
| 1 | FAIL — "one ear at three sizes" | HE1 human upper ear / rim; HE3 blade rim + stronger interior; symmetric stage 3 |
| 2 | BORDERLINE → FAIL — crinkles / crease lines | stage 4 (folded sheet quads: HE1 34 → 5–8, HE3 18 → 6) |
| — (own audit) | dark speck before the HE1 c2 tragus (cuff edge creased 162°) | stage 5 (cuff creases > 120°, crossing- and fold-safe) |
| 3 | FAIL — HE1 "shrunken, tip-cut HE2"; rough upper rim | HE1 human-family outline (upright, rounded, soft apex, rolled helix) |
| 4 | **PASS** | HE1 rim-to-lobe polish (lobe gate 0.24) |
| 5 | **PASS** | HE2 reference rows added to board B |

## 8. Immutable references

`immutable_hashes.txt` (re-verified after the final build):
- the 14 frozen reference files are unchanged (v005 blend and map, MPFB / Fenn / Aelari / Vael freeze records, Fenn / Vael topology and cuff canon, r6 heads);
- the HE2 + HR2 realization hashes (c1 / c2) match the freeze record;
- frozen Fenn E2, Aelari AE-E2 and Vael VA-E2-RI3 rebuild with dV 0 and identical faces;
- HB2 + HF2 + HP-B is unchanged.

## 9. Character-creator implications

- **One ear system.** HE1 / HE2 / HE3 are presets of one Halvren ear model, not three meshes:
  - one engineering topology (VAEL_EAR_BRANCH_TOPOLOGY_v002 sheet + RI3 cuff canon);
  - one HR2 root;
  - one realization path (ear_build + Halvren repair stages 1–5 + deformation guard).
- **Controls are domains, not a slider.** Separate controls:
  - length and base width;
  - outline: taper start / extension / shoulder, from a rounded human top to a lancet;
  - rim roll height / width (rolled vs blade);
  - projection, tilt / sweep;
  - concha, lobe gate, and upper-attachment lift.

  HE1 (rounded + rolled + upright) and HE3 (long + elevated + full helix + low projection) show that the creator must not tie these to one "elf amount" axis (Halvren canon: no elf-percentage slider).
- **Supported range:**
  - **minimum** L 5.6 (≈ Marchfolk +10–13 %), robust on both configurations;
  - **maximum** demonstrated at HE3 (L 8.2, +59 %).
  - Below L 5.6 the sheet-stretch gate tightens (L 5.3 at aspect 10.0). Clamp at 5.6, or treat 5.3–5.6 as unsupported until a quality pass exists.
- **Couplings the realization path applies automatically** (not player controls):
  - fuller upper helices need `lift_top` (≈ 0.55) on narrow heads (c2);
  - HE3-type long ears keep the HR2 sulcus off;
  - ears below L 6.3 rely on stage 3;
  - generated ears other than the frozen HE2 run stages 4 / 5 (`sheet_fold_fix`).
- **Firewall as validation.** The measured-domain arithmetic firewall (one-alpha R² < 0.80 against MF ↔ each elf) is the validation check for creator-generated Halvren ears (RM-UF-05 Tier-G style). Randomized or edited ears that fall onto a Marchfolk → elf line should be flagged.
- **Rigging carry-forward (as Vael):** bind the ear branch rigidly to the head at final skinning.

## 10. Family-level closure rule (§11)

| # | Condition | Result |
|---|---|---|
| 1 | HE2 + HR2 freeze recorded and unchanged | **PASS** — record + read-back dV 0, V hashes equal |
| 2 | HE3 firewall < 0.80 on all three pairs | **PASS** — 0.64 / 0.61 / 0.27 (c2 0.59 / 0.58 / 0.31) |
| 3 | HE3 remains the elf-forward extreme | **PASS** — composite 0.85 (top), longest / most elevated / sharpest; reviewers 4 / 5 PASS |
| 4 | HE3 c1 / c2 deformation and HR2 visual gates | **PASS** — 8 poses clean both, one auricle (board B) |
| 5 | HE1 size-floor disposition explicitly resolved | **PASS** — HE1 SIZE FLOOR ACCEPTED AS CANONICAL FAMILY BOUND at L 5.6 (≈ +10–13 %) |
| 6 | HE1 a valid human-forward member | **PASS** — firewall 0.22, composite 0.46, clean c1 / c2, reviewers 4 / 5 PASS |
| 7 | Coherent but non-lockstep family | **PASS** — ordered composite; outline / rim type change; non-monotone domains |
| 8 | Frozen non-Halvren references untouched | **PASS** — 16 / 16 hashes; Fenn / Aelari / Vael dV 0 |
| 9 | Character-creator implications documented | **PASS** — §9 |
| 10 | Final family lineup passes author-facing visual review | **PASS** — blind rounds 4 and 5 (residual taste note on HE3 vs HE2 recorded) |

**Shared polish carry-forwards (non-blocking; present on the frozen HE2 too, so not HE1 / HE3 defects):**
- **Crumpled cuff band / back-sheet Z-kink.** On the skull-facing back (lower-rear 3/4, direct rear), the RI3 cuff band plus the HR2 back-sheet Z-kink recorded in the HR2 report. Identical on HE2 (rear comparison in the review log). Folded cuff / transition quads: Fenn 14, Aelari 10, Vael 8, HE2 8–17, HE1 19–23, HE3 14–22 (`folded_cuff_quads_audit.json`).
- **Synthetic stamped interior relief** of the shared sheet. It is denser on the small HE1.
- **HR2 lobe-base crease.**

If wanted, a shared cuff / sheet polish pass would also have to touch HE2's frozen surface, so it is outside this order.

## STOP

STOP FOR CHATGPT REVIEW.
- Recorded: the HE2 + HR2 freeze.
- Recommended, not frozen: HE3 / HE1 HVEAR4 and the family freeze.
- No other race, Halvren system or retopology was started.
