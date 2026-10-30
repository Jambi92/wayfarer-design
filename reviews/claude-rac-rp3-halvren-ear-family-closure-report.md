# RAC RP3 — Halvren ear family closure after HR2

**Order:** `reviews/chatgpt-rac-rp3-halvren-ear-family-closure-after-hr2-order.md` (94eabf1; reviewed commit ee0e98c).
**Evidence:** `reviews/rac-rp3-evidence/halvren_rp3_ear_family_closure/`

| File | Contents |
|---|---|
| `HALVREN_HE2_HR2_FREEZE.json` | HE2 + HR2 freeze record |
| `HV_ear_family_closure_record.json` | consolidated record |
| `HV_ear_family_prodcheck.json` | mirroring / export / LOD |
| `boards/HVF_A..F` | A HE3 firewall, B HE3 HR2 root gate, C HE3 body context, D HE1 size floor, E family lineup, F HE3 decomposition |
| `records/` | per-build build / audit / deform / guard / repair / measure: final HE1 / HE2 / HE3 c1 / c2, and the HE1 L 5.3 edge test (`L53_*`) |
| `HV_ear_definitions_HVEAR4.json` | ear definitions |
| `immutable_hashes.txt` | 16 / 16 unchanged |
| `blind_family_review.md` | independent blind review |

**Tools** (`tools/rac/rp/halvren_rp3_v001/`):
- `hv_ear_family_closure.py` — record;
- `hv_ear_family_boards.py` — boards;
- `hv_cuff_repair.py` — new stage 3: sheet stretch repair.

**Library** (`fenn_rp3_v001`; Fenn / Aelari / Vael rebuilt dV 0):
- `ear_branch_lib.py`:
  - HE1 and HE3 are now HVEAR4;
  - the old definitions are kept as `HE1-HVEAR3` / `HE3-HVEAR3`;
  - `HE1-HS` is the layout-metric test body.
- `ear_build.py`: probe key `clear` (inert unless set).

## FINAL DISPOSITION

__DISPOSITION__

## 1. HE2 + HR2 freeze recorded (§1)

- **Record.** `HALVREN_HE2_HR2_FREEZE.json` freezes the ee0e98c state by record. It holds:
  - authority 94eabf1 §1;
  - the HE2 definition, `HV_ROOT2` and `HV_SKIN`;
  - topology and build path;
  - per-configuration realization hashes (branch npz sha256, V float32 sha256, face sha256 c1 `f8367ab0…`);
  - the closed gates, and the polish items marked non-blocking;
  - the firewall (0.51 / 0.44 / 0.23);
  - tool hashes at ee0e98c.
- **Read-back.** HE2 rebuilt on c1 and c2 with this pass's final code (HE3 / HE1 library changes, the `clear` probe key, repair stage 3): dV 0, faces identical. The V float32 hashes equal the freeze record (`immutable_hashes.txt`).
- **Canon pointers.** Status blocks added to:
  - `specs/halvren/HALVREN_V1.md` (RP3 ear status);
  - `specs/STATUS.md`;
  - `reviews/claude-session-handoff.md`.
- **Not reopened in this pass:** the HE2 root, HE2 morphology and HR2.

## 2. HE3 root-cause diagnosis (§4)

**One-alpha fit of HVEAR3 HE3 on HR2 (the "before"),** in source-SD units on the common c1 head:

| Pair | R² | α | n | Domains carrying the fit |
|---|---|---|---|---|
| MF ↔ Fenn | **0.883** | 0.897 | 11 | width / L, tragus height, upward extension, tip angle |
| MF ↔ Aelari | 0.782 | 0.791 | 10 | upward extension, width / L, length, tip angle |
| MF ↔ Vael | 0.473 | 0.753 | 11 | tip angle, backward angle, length, upward extension |

Residuals by domain for every pair, before and after, are in `decomposition` in the record and on board F.

**Why HE3 moved from Aelari-like to Fenn-like after HR2.** One domain changed: the root line.
- Under HR1, HE3's anterior skin-attachment line leaned backward (y = −1.95 SD). That is opposite to Fenn (dx +0.54). It was the largest Fenn residual (−2.40), and it held MF ↔ Fenn at R² 0.76.
- HR2 seats the auricle on the head, so the attachment line became near-vertical / forward (y = +1.21). That removed the residual, and MF ↔ Fenn rose to 0.88.
- At the same time, HR2's lobe-edge lift 0.30 (lobe fraction t 0.33 instead of the HR1 free lobe) opened a lobe residual against Aelari (dx +2.73), so MF ↔ Aelari fell 0.87 → 0.78.

**Why it collapses onto Fenn at all.** HVEAR3 HE3 lined up with the elf direction in every domain an elf ear is defined by, at roughly one common scale:
- long (t 1.06);
- narrow (t 1.75);
- elevated (t 1.45);
- sharp (t 0.96);
- projecting (t 0.69);
- backward (t 0.69);
- helix fullness elf-ward (t 0.49).

With every domain moving the same way, a one-alpha fit explains it. The root line was the only domain breaking the pattern, and HR2 removed it.

## 3. HE3 correction — HVEAR4 (§5)

**Strategy: cross-domain recombination, not scalar interpolation.**
- **Kept elf-forward:** the extreme length (8.2), the most elevated upper extension of the family (t 1.51, beyond the elf mean), and the sharp point (tip 70°).
- **Placed on a Halvren human-family body:**
  - broad base (wb 1.95 → 2.10);
  - full-shouldered helix (taper start 0.42 → 0.50, shoulder 0.10 → 0.15): helix fullness 0.740, *fuller than the Marchfolk auricle*, while the tip stays sharp;
  - low projection (26 → 20°);
  - moderate tilt / sweep (14 → 12 / 1.5 → 1.0);
  - the upper attachment lifted 0.55 cm (`lift_top`), so the fuller upper helix clears the HR2-seated head on c2. Without it: 15–37 self-intersections.
- **Root:** HR2 as before (sulcus off for HE3).

**Calibration.** 32 rest-state trials (`HE3_trials` in the record).
- Taper-only changes self-intersected at the upper attachment (20–43 pairs).
- Sweep / projection / base width alone stalled at R² 0.66–0.70.
- `lift_top` made the fuller shoulder clean on c2.

**Domains (HE3 before → corrected, t = 0 Marchfolk, 1 elf mean):**

| Domain | MF | Fenn | Aelari | Vael | HE2 | HE3 before (t) | **HE3 corrected (t)** |
|---|---|---|---|---|---|---|---|
| length / HH | 0.240 | 0.363 | 0.406 | 0.344 | 0.328 | 0.378 (1.06) | **0.382 (1.08)** |
| width / length | 0.541 | 0.372 | 0.410 | 0.480 | 0.388 | 0.330 (1.75) | **0.344 (1.63)** |
| projection | 6.5° | 52.5° | 30.5° | 38.7° | 18.6° | 30.0° (0.69) | **21.2° (0.43)** |
| upward extension / HH | 0.015 | 0.089 | 0.108 | 0.056 | 0.090 | 0.116 (1.45) | **0.120 (1.51)** |
| backward angle | 4.8° | 21.1° | 24.7° | 28.0° | 14.6° | 18.5° (0.69) | **14.1° (0.47)** |
| tip angle | 123.5° | 52.9° | 54.4° | 64.2° | 82.6° | 59.5° (0.96) | **70.5° (0.80)** |
| lobe fraction | 0.046 | 0.103 | 0.136 | 0.112 | 0.051 | 0.069 (0.33) | **0.073 (0.38)** |
| root line | −1.5° | 2.9° | 1.5° | −17.7° | 0.1° | 8.5° | **9.3°** |
| concha depth / L | 0.268 | 0.235 | 0.168 | 0.218 | 0.195 | 0.220 (0.80) | **0.180 (1.45)** |
| tragus height | 0.404 | 0.274 | 0.350 | 0.355 | 0.289 | 0.291 (1.46) | **0.288 (1.50)** |
| helix fullness | 0.697 | 0.621 | 0.610 | 0.607 | 0.758 | 0.655 (0.49) | **0.740 (−0.51)** |

## 4. HE3 firewall (§6)

| Pair | Before: R² / α / n | **Corrected c1: R² / α / n** | Corrected c2 R² | Limit |
|---|---|---|---|---|
| MF ↔ Fenn | 0.883 / 0.897 / 11 | **0.621 / 0.756 / 11** | 0.600 | < 0.80 |
| MF ↔ Aelari | 0.782 / 0.791 / 10 | **0.612 / 0.701 / 10** | 0.552 | < 0.80 |
| MF ↔ Vael | 0.473 / 0.753 / 11 | **0.260 / 0.561 / 11** | 0.291 | < 0.80 |

- **Margin:** at least 0.18 below 0.80 on every pair.
- **What breaks the fit now:** the largest residuals are helix fullness (+2.5 to +2.8 SD in every pair), concha (−1.8 Fenn), upward extension, width and tragus.
- **Distinct domains (> 0.5 SD):** 8 vs Fenn, 8 vs Aelari, 10 vs Vael, 5 vs HE2 (11 vs Marchfolk).
- **Still the elf-forward extreme:** composite elf-ward position HE1 0.39 < HE2 0.65 < **HE3 0.88**.

## 5. HE3 technical / deformation / root (§6, §10)

| | HE3 c1 | HE3 c2 |
|---|---|---|
| components / boundary / non-manifold / degenerate / outward | 1 / 0 / 0 / 0 / yes | 1 / 0 / 0 / 0 / yes |
| branch self-intersections | 0 | 0 |
| min corner / max aspect | 13.2° / 9.01 | 13.3° / 9.01 |
| root valence 4 × 52 both sides | yes | yes |
| 8 deformation poses (contacts / flips / root inversions) | 0 | 0 |
| deformation guard iterations | **4** (13 guarded faces; logged) | 0 |
| cuff repair | stage 1 only | stage 1 only |
| clearance min | 0.23 cm | 0.20 cm |
| HR2 pedestal p90 posterior / inferior | 0.37 / 0.47 cm | 0.29 / 0.33 cm |
| loop crease posterior / inferior | 5 / 5° | 9 / 6° |
| mirroring (sheet max / mean; connectivity) | 0.078 / 0.0001 cm; identical | 0.059 / 0.0001 cm; identical |
| export / reload | dV 6e-6 cm, faces equal | same |
| LOD 50 / 25 % | 0 non-manifold, 0 zero-area | same |
| determinism | dV 0, faces identical | dV 0, faces identical |

**Mirroring.** The sheet is mirrored to 0.0001 cm mean. The 0.06–0.08 cm maxima are 2 rim vertices moved by the per-side untangle / guard, not a systematic asymmetry.

**Visual (boards B, C).**
- One auricle from strict side, true rear 3/4, direct rear, lower-rear 3/4 and the Board-E 3/4 camera on c1 and c2: no flange, no lower fork.
- In body context the ear stands as the elf-forward Halvren ear: longer and more elevated than HE2, with a fuller, rounder upper body than any elf ear.

## 6. HE1 size-floor investigation (§7–§8)

**Cause, tested cleanly.** The HVEAR3 "floor" (L 6.3, +23–27 %) was not a structural limit of the shared sheet. With HR2, shorter HE1s are clean in every gate except one:
- 2–20 **anterior-cavum front-sheet quads** cross aspect 10 (10.04 at L 5.9, 10.25 at 5.6, 10.52 at 5.3, 11.24 at 5.0);
- there are no self-intersections, and min corners stay ≥ 12.5°.

Rest-state sweep on c1 (`HE1_size_trials`):

| HE1 length | Measured length vs Marchfolk | Shared layout: max aspect / T4 | Human-scale layout metric (Path B scaffold test): max aspect / T4 | + stage-3 sheet stretch repair (shared layout) |
|---|---|---|---|---|
| 6.3 (HVEAR3) | +23 % | 9.78 / 344 (clean) | 14.09 / 171 | — |
| 5.9 | +16 % | 10.04 / 393 | — | — |
| 5.6 | +10 % | 10.25 / 458 | 12.70 / 191 | **9.94 (c1 + c2 guarded: clean)** |
| 5.3 | +5 % | 10.52 / 498 | 11.94 / 192 | 9.973 / 9.999 (c1 / c2: at the gate) |
| 5.0 | 0 % | 11.24 / 551 | 12.55 / 213 | 9.99 (rest) |

**Path B tested.** A dedicated human-scale scaffold was tried: the same connectivity, with vertex positions optimised in a human-scale metric (`EAR_LAYOUT_METRIC=HE1-HS`).
- It halves the T4 angle violations.
- But it makes the worst aspect worse (11.9–14.1), even at L 6.3.
- Scaling the concha seat with length does not help (`C*` trials).

**What works** is a bounded sheet stretch repair inside the existing Halvren realization path, `hv_cuff_repair.py` stage 3:
- a per-vertex tangential search on the 2–20 offending front-sheet quads, with junction vertices fixed;
- ≤ 0.04 cm moves at L 5.6 (≤ 0.10 at L 5.0);
- same connectivity, same family authoring controls;
- inert on HE2 / HE3 (HE2 freeze read-back dV 0).

**Measured size range on the production path:**
- L 5.6 (+10 %) is clean with margin on c1 and c2: aspect 9.94, 8 poses clean, guard 0.
- L 5.3 (+5 %) is exactly at the gate (aspect 9.999 on c2).
- Marchfolk size (L 5.0) is reachable at rest but not robustly.

**Path A judged visually (board D).** At L 6.3, HE1 reads as a slightly scaled HE2, not as a human-forward member:
- +23 % Marchfolk length against HE2's +37 %;
- its outline and body nearly overlap HE2's.

Accepting +23–27 % as the canonical human-forward minimum would make the human-forward bound an elf-sized ear.

**Recommendation.** HE1 HVEAR4 = the same human-forward body at **L 5.6**:
- +10 % measured length vs Marchfolk;
- firewall R² 0.34 / 0.27 / 0.21;
- composite 0.39.

The Halvren family bound for human-forward ear size is **L 5.6 ≈ Marchfolk +10 %**, on the shared production path. It is a modest, deliberate Halvren trait: even the most human-forward Halvren ear is slightly longer and pointed. No separate scaffold or topology is needed.

| | HE1 c1 | HE1 c2 |
|---|---|---|
| integrity (1 / 0 / 0 / 0 / outward) | yes | yes |
| branch self-intersections | 0 | 0 |
| min corner / aspect | 16.3° / 9.94 | 16.1° / 9.94 |
| root valence | 4 × 52 | 4 × 52 |
| 8 poses | clean | clean |
| guard | 0 | 0 |
| repair | stage 1: 1 sliver; stage 3: 2 sheet quads → 9.94 | stage 3: 2 quads |
| clearance | 0.28 cm | 0.24 cm |
| mirroring | 0.085 cm max (one stage-3-repaired vertex), mean 0.0001, connectivity identical | 0.082 cm max, mean 0.0001, identical |
| export / LOD | pass | pass |
| determinism | dV 0, faces identical | dV 0, faces identical |
| HR2 pedestal p90 posterior / inferior; crease | 0.19 / 0.30 cm; 7 / 6° | — |

## 7. Final HE1 / HE2 / HE3 lineup (board E)

| | HE1 (HVEAR4) | HE2 (frozen) | HE3 (HVEAR4) |
|---|---|---|---|
| length vs Marchfolk | +10 % | +37 % | +59 % |
| composite elf-ward | 0.39 | 0.65 | 0.88 |
| best firewall R² | 0.34 (MF ↔ Fenn) | 0.51 (MF ↔ Fenn) | 0.62 (MF ↔ Fenn) |
| character | short, blunt-shouldered late point, broad human-family body | balanced: broad full body, controlled shouldered point | long, most elevated, sharp point on a full-shouldered broad helix, low projection |

- **Ordering:** HE1 < HE2 < HE3 holds.
- **Not lockstep:**
  - helix fullness is non-monotone (HE2 fullest);
  - HE3's projection (21°) and backward angle (14°) sit at or below HE2's, not above;
  - HE1's apex shape differs (late / blunt);
  - HE3 differs from HE2 in 5 domains.
- **Shared:** all three use one topology and one HR2 root path.

__VISUAL__

## 8. Immutable references

`immutable_hashes.txt`:
- the 14 frozen reference files are unchanged (v005 blend and map, MPFB / Fenn / Aelari / Vael freeze records, Fenn / Vael topology and cuff canon, r6 heads);
- the HE2 + HR2 realization hashes (c1 / c2) match the freeze record;
- frozen Fenn E2, Aelari AE-E2 and Vael VA-E2-RI3 rebuild with dV 0 and identical faces;
- HB2 + HF2 + HP-B is unchanged.

## 9. Character-creator implications

- **One ear system.** HE1 / HE2 / HE3 are presets of one Halvren ear model, not three meshes:
  - one engineering topology (VAEL_EAR_BRANCH_TOPOLOGY_v002 sheet + RI3 cuff canon);
  - one HR2 root;
  - one realization path (ear_build + Halvren repair + deformation guard).
- **Controls are domains, not a slider.** Length, base width, taper start / shoulder (helix fullness vs point), projection, tilt / sweep, concha, lobe and upper-attachment lift are separate. HE3 shows that elf-forward length and elevation combine with a human-family full helix and low projection, so the creator must not tie these to one "elf amount" axis (Halvren canon: no elf-percentage slider).
- **Supported range:**
  - **minimum** ≈ Marchfolk +10 % length (L 5.6), robust;
  - **maximum** demonstrated at HE3 (L 8.2, +59 %).
  - Below L 5.6 the sheet-stretch gate tightens (L 5.3 at aspect 10.0). The creator should clamp HE1-type length at 5.6, or treat 5.3–5.6 as unsupported until a quality pass exists.
- **Couplings the creator must respect:**
  - fuller upper helices need `lift_top` (≈ 0.55) to clear the head on narrow-headed configurations (c2);
  - the HE3-type long ears keep the HR2 sulcus off;
  - ears below L 6.3 rely on the stage-3 sheet stretch repair.

  These are realization-path rules, applied automatically by the path, not player controls.
- **Firewall as validation.** The measured-domain arithmetic firewall (one-alpha R² < 0.80 against MF ↔ each elf) is the validation check for creator-generated Halvren ears (RM-UF-05 Tier-G style): randomized or edited ears that fall onto a Marchfolk → elf line should be flagged.
- **Rigging carry-forward (as Vael):** bind the ear branch rigidly to the head at final skinning.

## 10. Family-level closure rule (§11)

__GATES__

## STOP

STOP FOR CHATGPT REVIEW. Recorded: HE2 + HR2 freeze. Recommended, not frozen: HE3 / HE1 HVEAR4 and the family freeze. No other race, Halvren system or retopology was started.
