# RAC W2I5 — Saurin Medial / Posterior Thigh Finish / Conditional Canonicalization: Failure Package

**Author:** Claude (auditor) · **Date:** October 9, 2026 · **Order:** `reviews/chatgpt-rac-w2i5-saurin-final-thigh-canonicalization-order.md` §1–§16

**Evidence:** `reviews/rac-w2i5-sa-evidence/` (README lists every file and driver).
**Status:** REFERENCE-ASSET FINISH — NO UE5. **Canonicalization NOT performed.**
- Of the §12 conditions, 1 (reference-quality relief) and 3 (relief diagnostic toward native) failed, and condition 2 (sector-boundary marks) is not met. Per §12 this report is the failure package.
- Nothing canonical or accepted changed: W1 aff1b52 / §263 SA-F, the accepted W2I4 candidate files, the tool chain, `specs/saurin/SAURIN_V1.md` and the PC `RaceBodies/out/` set are untouched.
- The canonicalization scripts are prepared but were not run (§9).

## Verdicts

| Item | Verdict | One line |
|---|---|---|
| **Medial / posterior thigh relief** | **REJECT (W2I5 procedural candidate)** | Visually only marginally different from W2I4. The relief diagnostic got worse, not closer to native (§3). |
| **Scale-field continuity** | **ACCEPT** | The saved W2I4 seed set was reused exactly (130,949 seeds), and every region matches W2I4 (§5). |
| **Topology / fold / strain** | **ACCEPT** | 0 new flips and 0 new folds vs W2I4 on all 62 bodies; closed manifold; no band-wide strain (§4). |
| **Measurement invariance** | **ACCEPT** | 0 verdict changes vs W2I4 (493 internal checks, all limb / cross-race rows); largest drift 0.034 % (§6). |
| **Tail coupling** | **ACCEPT** | Every cap is identical to W2I4; dlean changes by at most 0.0004° (§7). |
| **SAU-SILHOUETTE** | **ACCEPT WITH PRESENTATION CONTEXT** | Unchanged; the caudal system was not touched. |
| **Saurin W2 reference asset** | **CONSTRAIN** | It stays the accepted W2I4 candidate. Only the medial / posterior thigh relief is still open. |
| **Canonicalization** | **NOT COMPLETED** | §12 conditions 1–3 not met. |
| **Saurin W2I overall** | **CONSTRAIN** | Biology, scale field, coupling and silhouette are all accepted. One asset item is open (§10). |

**No accepted Saurin biology changed in W2I5.** The W2I5 delta moves only thigh surface vertices (frozen frame u 58.4–86.6 cm, leg label ≥ 0.30, tail label ≤ 0.03), by at most 0.40 cm. Every measurement-bearing vertex is held.

---

## 1. W2I4 rulings recorded

- `cfg/w2i/SA-boundary.json` `rulings_w2i4`;
- the author ruling line in the W2I4 gate;
- the issue record;
- the queue;
- `specs/STATUS.md`;
- one general rule in `decisions/REFERENCE_ANATOMY_V1.md` §10: reference-asset surface finish is not biology, and an accepted regenerated seed realization replaces a lost layout.

## 2. What was built (`tools/rac/w1/w2i5_drivers/sa_sculpt.py`)

The W2I5 delta is added after the W2I4 route and before the stature route (`build_s`). It is computed once on the male centre at 188 and carried to every state, like W2I4.

**1. Sector.**
- Covers the medial / posterior thigh plus the whole W2I4 sector transition, fading out into the accepted anterior / lateral thigh.
- The true crotch / pouch wall (upper inner thigh above 84 cm, more than 3 cm medial) is untouched.
- All masks are diffused over the mesh, so no weight step or held vertex can print into the surface.

**2. Native relief source — surface walk.**
- W2I4 sampled the frozen point vertically offset in 3-D. On faces that turn toward the other leg, that point is off-surface, which caused the W2I4 pits and tears.
- W2I5 instead walks on the frozen surface: from each vertex's own frozen position it steps along the local vertical tangent, re-projecting each step, until it reaches the source height.
- The source heights use the W2I4 anchors (knee transition 63 cm, hip crease 86 + 9.2 cm), with an amplitude-normalized cross-fade.

**3. Band-limited re-form.**
- Inside the sector, sharp sub-0.45 cm content is removed, which erases speckle and tear micro-detail.
- The 0.45–1.5 cm band is replaced by the walked native band.
- Source samples that land in the frozen thigh's own defect patches (local roughness above its 95th percentile) are faded, not copied.
- Inside the blend zone, torn patches of the current surface are smoothed.

**4. Fold guard over all 62 bodies.**
- A face may not flip against its W2I4 build unless it turns toward the locally smoothed W2I4 surface and ends up unfolded. That case is a repair of an inherited W2I4 fold.
- A face may not newly fold against the smoothed surface.
- 12 rounds left 3,325 → 2 offending faces; a closure pass (`sa_guardfix5.py`) brought it to 0 on all 62 bodies.

**Variants tested and rejected** (the evidence is in the session renders; the drivers keep each variant behind a switch):

| Variant | Result |
|---|---|
| Unguarded first pass (no band limit) | Copied the frozen medial tear twice (9.2 cm apart) and printed dark speckle dots |
| 3 cm "shelf" flattening of the tear | New knee / crotch artifacts and 156 flips |
| Re-measurement iteration (`ITERS` 3 / 8) | Pushes the metric toward native (4 cm lag 0.50), but diverges into spikes at the posterior / medial edges (323 flips before the guard) |
| Narrow vs wide cross-fade | No effect on the metric |

## 3. Medial / posterior relief — why it fails (§4, §12 conditions 1–3)

**Diagnostic.** Vertical correlation length of the 1.5 cm relief, by sector (`thigh_relief5.json`; native = frozen):

| | whole mid-thigh | anterior / lateral | medial / posterior |
|---|---|---|---|
| frozen (native) | 3.31 | 2.63 | **3.94** |
| W2I3 | 5.47 | 4.17 | 6.67 |
| W2I4 | 5.06 | 2.92 | 6.75 |
| **W2I5** | 5.89 | 2.95 | **> 9 (correlation never drops below 0.5)** |

The vertical autocorrelation of the medial / posterior relief (`relief_curve5.json`):

| lag (cm) | 1 | 2 | 3 | 4 | 6 | 9 |
|---|---|---|---|---|---|---|
| frozen | 0.90 | 0.76 | 0.61 | 0.49 | 0.33 | 0.22 |
| W2I4 | 0.93 | 0.84 | 0.75 | 0.67 | 0.54 | 0.40 |
| W2I5 | 0.92 | 0.84 | 0.76 | 0.72 | 0.62 | **0.51** |

**Diagnosis.**
- **The target itself is roughly native at short lags.** The walked target field has a 4 cm lag of 0.45 and a 6 cm lag of 0.37.
- **Inserting 9.2 cm duplicates a band.** The frozen 70–79 cm band is read from both anchors, which raises the 9 cm lag (0.60). This is the same duplication W2I4 had, and it is stronger on the medial thigh, whose forms are long and vertical (hamstring / adductor lines).
- **The direct re-form does not fully take.** Without iteration, the re-measured relief keeps the stretched 1.5–3 cm W2I3 form leaking through the Gaussian split. Iteration fixes the metric but diverges into spikes.

**Visual** (`sheets/w2i5_thigh_base_SA-M188.jpg`, `..._SA-F188.jpg`, surfaced versions too; matched camera, W2I3 / W2I4 / W2I5):
- The rear and hip-to-thigh views are cleaner than W2I4.
- In the medial / adductor view, the W2I4 sector-boundary marks and the inherited Rodin tear on the right medial thigh are reduced but **still visible**. That tear is present in the frozen W1 asset too.
- The guard blocks their full removal, because erasing them would flip or fold faces in the high-fat / high-muscle bodies that share the same delta.

**Conclusion.** Within the hard holds (one delta for all 62 bodies, 0 new flips, every measurement held), a procedural re-sample cannot invent the missing 9.2 cm of native hamstring / adductor relief without duplicating it. The W2I4 finding stands, now confirmed with a stronger method.

**The remaining item needs a hand sculpt on the medial / posterior thigh by an artist in a sculpting tool**, followed by the same regression. This session cannot do that.

## 4. Topology / fold / strain (§7) — PASS

| Check | Result |
|---|---|
| Flips vs W2I4, 62 bodies | **0 new flips**; 11 faces flipped as repairs of inherited W2I4 folds (they now agree with the smoothed surface) |
| New folds vs the smoothed W2I4 surface | **0** (W2I4 folds 42,574 → W2I5 42,543) |
| SA-M188 / SA-F188 | 0 flips vs W2I4, 0 vs frozen |
| Faces newly past 90° against frozen | 115, all in composition / LT90 bodies where W2I4 already turned them close to 90°; 0 in the core states. W2I4 had the same class (139). |
| Surfaced SA-M188 | Closed (0 boundary), manifold (0 non-manifold), 0 degenerate faces, Euler 2. Faces flipped against their own base: 2,338 (W2I4: 2,320). |

Sculpted-edge strain vs W2I4 (SA-M188), 563,720 edges:

| p1 | p50 | p99 | min | max | Outside 0.8–1.25 |
|---|---|---|---|---|---|
| 0.93 | 1.00 | 1.03 | 0.46 | 1.33 | 410 edges (0.07 %), all isolated |

There is no band-wide stretch or compression.

## 5. Scale field (§6) — PASS

| Check | Result |
|---|---|
| Seed set | Identical to the saved W2I4 set (130,949 seeds) |
| Generator | Unchanged (`g7surfc.py` via `g7surfc_moved.py`) |
| Region labels | Unchanged; N / T recomputed |
| Hand-pad anchors | Carried (+6.06 cm) |
| Relief at the 4.12 M unmoved upsampled vertices | Matches W2I4 within 0.1 mm (normal recomputation only) |

Continuity ratio, frozen / W2I4 / W2I5:

| Region | frozen | W2I4 | W2I5 |
|---|---|---|---|
| thigh | 1.107 | 1.176 | 1.173 |
| knee | 1.153 | 1.182 | 1.184 |
| neck, shoulder, forearm | — | unchanged | unchanged |

Seed spacing / R: p10 / p50 / p90 0.50 / 0.53 / 0.62. No third layout was created.

## 6. 62-body regression (§8) — PASS

**0 result changes vs W2I4.** The largest scalar change is 0.034 % (SA-M188-MUFAHI tail mass share). SA-M188 measurements change by at most 0.02 % (body volume, centre of mass); `d_com_f` is a difference of two near-equal numbers.

| Suite | Result |
|---|---|
| Stature, continuity | ST 64, C 26 |
| Frames, composition | FR 104, CO 96 |
| §263 | SX 17 PASS + the 2 canon CONSTRAIN cases |
| Report-only beyond-anchor tail cases | TL FAIL ×2, unchanged |
| LTF, M, P, P0, G | 8, 138, 76, 76, 6 |
| Durrim leg separation | 24 / 24 |
| Cogling forearm separation | 8 / 8 |
| Grask reach | 14 PASS + D-B Broad 208 span (accepted marginal) |

Hip / H 0.5333, femur / leg 0.420, forearm / arm 0.366, total arm 0.400 H, lower trunk 32.0 cm, thoracic d/w 0.880, tail 64.6 %, root area 529.21, lean 8.42°: all unchanged.

## 7. Tail coupling (§10) — PASS

| State | W2I4 cap | W2I5 cap |
|---|---|---|
| Balanced 188 | 78.875 % | 78.875 % |
| Broad 188 | 80.25 % | 80.25 % |
| Narrow + high fat 188 | 79.625 % | 79.625 % |
| Broad 208 | 79.75 % | 79.75 % |

The other five states are also identical. The 55 % substantial-base low end is unchanged (A50 binds). Across the named cases, dlean changes by at most 0.0004° and every pass / fail is identical.

## 8. §12 conditions

| # | Condition | Result |
|---|---|---|
| 1 | Medial / posterior relief visually reference-quality | **FAIL** — boundary marks and the inherited tear are reduced, not removed |
| 2 | Sector-boundary artifacts removed | **FAIL** — still visible in the medial view |
| 3 | Relief diagnostic clearly toward native | **FAIL** — medial / posterior > 9 cm vs W2I4 6.75 cm and native 3.94 cm |
| 4 | Topology / fold / strain guards | PASS |
| 5 | W2I4 measurements / verdicts unchanged | PASS |
| 6 | Scale-field reuse with the saved W2I4 seeds | PASS |
| 7 | Tail coupling unchanged | PASS |
| 8 | No new canon contradiction | PASS (no canon edited) |

## 9. Canonicalization — NOT COMPLETED (prepared only)

**Prepared, not run:**
- `sa_canon5.py` — the W2 canonical file set in the accepted `RaceBodies/out` formats under new names, so the W1 `final` set stays untouched as provenance:
  - `saurin_w2_final_base.npz`;
  - `saurin_w2_final_surface_delta.npz` (float16, the same format as W1);
  - `rebuild_w2_final.py`;
  - `saurin_w2_seeds.npy`;
  - `saurin_w2_SA-F188_realization.npz`;
  - region fields;
  - `SaurinW2Final.blend` / `.fbx` through the accepted fast-simplification export.
- `sa_toolchain5.py` — the W2 tool-chain counterparts beside the W1 files (`tools/rodin/w2/`):
  - `ref_metrics_w2.json`;
  - `axis_w2.npy`;
  - `g7geo_w2_points.json` (ARM / LEG points and the hand-anchor offset);
  - `lbase_w2_stations.json`;
  - `s263_w2.json` (§263 accounting plus the waist / shoulder and waist / hip silhouette check with station-carried bands).

The W2I4 gate §9c canon text edits remain the prepared wording.

**Provenance unchanged:**
- W1 `saurin_final_base.npz` `a925e067…`, `saurin_final_surface_delta.npz` `b72691ab…`, `rebuild_final.py` `722b0420…`;
- the W2I4 candidate `saurin_w2i4_base.npz` `f86ae800…`.

**W2I5 candidate delta (scratch only):** `sculpt_delta.npz` `568074c9…`.

## 10. Remaining named dependencies

| Item | Classification |
|---|---|
| Medial / posterior thigh relief (hamstring / adductor) at native scale; W2I4 sector-boundary marks; inherited Rodin medial-thigh tear | **OPEN ASSET ITEM** — needs a hand sculpt in a sculpting tool (procedural route exhausted in W2I4 + W2I5); blocks canonicalization |
| Canonicalization package (`sa_canon5.py`, `sa_toolchain5.py`, W2I4 §9c text) | **READY TO RUN** once the thigh closes |
| SAU-SILHOUETTE | ACCEPT WITH PRESENTATION CONTEXT |
| Broad ~80 % / Broad 208 span | ACCEPTED MARGINAL D-B |
| Skeletal-mass rows | ACCEPTED DEPENDENCY D-D |
| Beyond-anchor TL cases | REPORT-ONLY (unchanged) |
| RM-UB-08, RM-UF-04, facial rows, claw numeric ranges, final density, neutral idle / dynamic posture, SAU-BODY-20 world-space, creator-envelope interpolation, UE5 / rig / animation / equipment / gameplay | NAMED DEPENDENCY / LATER WORK (untouched) |

## 11. Author decision requested

The procedural route is now exhausted for the medial / posterior thigh. The options:
- **(a)** Hand off the thigh to an artist. Tyler or an artist sculpts the medial / posterior thigh relief, plus the two marks and the tear, on the W2I4 base, in Blender sculpt mode or ZBrush, with the measurement vertices locked. The result is brought back for the same regression, then canonicalized with the prepared package.
- **(b)** Accept the W2I4 candidate (or this W2I5 candidate, which is equal on every measure and slightly cleaner in the rear views) as the W2 reference with the medial thigh noted as a later art-pass item, and run the prepared canonicalization.
- **(c)** Keep W1 aff1b52 canonical, with W2 as the accepted biological target, until the art pass.

**STOP.** W2I not closed; Wave 3 not begun.
