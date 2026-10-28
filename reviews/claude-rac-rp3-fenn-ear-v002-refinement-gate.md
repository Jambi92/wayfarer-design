# RAC RP3 — Fenn ear topology v002 refinement gate (order 0d9c70b)

**Verdict: FENN EAR v002 PASS WITH DOCUMENTED T-4 RESIDUAL — AUTHOR DECISION**

E2 was refined once, within the bounded budget R1 → R2 → R3, on one shared c1 / c2 topology.

- Branch-wide T-4 is 4.4 % on c1 and 3.9 % on c2 (v001: 15.8 % / 16.3 %), below the preferred 10 %.
- Every hard gate passes on both configurations and on all ten probes.
- E2 shape, the root loop, the junction and the hidden-ear CF2 identity are unchanged.

The verdict is not "READY" because of three small, documented residuals:

1. **Root-band cells:** one cell per configuration is sharper than v001. The min corner is c1 7.9° and c2 12.7° (v001 19.5° / 18.2°). These are near-triangular root-band quads in the locked root-band topology. The c1 cell is held by a head contact.
2. **Aspect:** more branch quads sit between aspect 6 and 10 (17 / 19 vs 1 / 2), all ≤ 9.3.
3. **Bridge corner:** a cluster of obtuse cells remains at the bridge / concha-floor corner.

None of these can be removed without changing the locked root band, the anatomy, or contact clearance. Whether they are acceptable at consolidation is the author's call.

Fenn is **not frozen**. Nothing outside the ear branch changed.

Evidence: `reviews/rac-rp3-evidence/fenn_ear_v002/`. Tools: `tools/rac/rp/fenn_rp3_v001/` (`run_earbranch_v002.sh`). Production review files: `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Fenn/RP3/ear_branch_v002/` (read-back sha256 equal).

## 1. What changed (v001 → v002)

| Target | v001 | v002 |
|---|---|---|
| **A** — upper extension / tip | 12 × 12 kite block F2 (corners Y, c1f, tip, P_up) | <ul><li>Crescent F1' (28 rows × 12) over the whole notch U, to a new cut c1f → P_up, held as a feature line.</li><li>Tapered leaf above the cut: 23 rows across the ear, marched at square cells.</li><li>Columns 12 → 2 by staggered 3 → 1 reductions (bands 2 / 5 / 9 / 13 / 15).</li><li>One diamond cap.</li><li>Rim strip on the new path.</li></ul> |
| **B** — cuff count transitions | DP 52 / 56 / 60 / 64 / 68, placed by relax | <ul><li>Same DP rule; every alternative tried was worse (provenance).</li><li>Placement changed to tangential pre-smoothing plus a 3-D corner-angle quality pass (sizing, normal, transition, log-aspect, contact and root-crease terms).</li><li>Deformation-aware guard.</li></ul> |
| **C** — attachment corners | sheet relax | <ul><li>Line-A end exponent 1.5.</li><li>Local corner-angle optimisation of the sheet.</li><li>The 3-D quality pass on the cuff side.</li></ul> |
| **D** — lobe-cusp knob | cuff shoulder raised at the lobe front | Lobe lift ends at the lobe front with an attachment exemption; the lobe thins (0.6). |
| Unchanged | | <ul><li>E2 parameters.</li><li>52-vertex root loop.</li><li>Junction ring J (70).</li><li>Root band.</li><li>Transition ring.</li><li>v005 outside the branch (byte-identical).</li></ul> |

Topology v002 per side: 1,732 V / 1,757 Q (v001 1,300 / 1,325). Whole mesh: 58,944 V / 58,942 Q, 100 % quads. The topology is identical for c1, c2 and the probes (`topology/FENN_EAR_BRANCH_TOPOLOGY_v002.*`, cuff canon v002).

## 2. Hard gates (final R3 configuration)

| Gate | c1 FNL4-CF2 | c2 FNF181-CF2 |
|---|---|---|
| Quads / components / boundary / non-manifold / degenerate branch faces | 100 % / 1 / 0 / 0 / 0 | 100 % / 1 / 0 / 0 / 0 |
| Normals outward, winding consistent | yes | yes |
| Self-intersection pairs touching the branch | 0 (whole mesh 60 = CF2 v005 baseline 60) | 0 (166 = baseline 166) |
| Root valence 4 (52 / 52 per side) | yes | yes |
| Outside branch byte-identical (max Δ 0.0) | yes | yes |
| Seam / float / burial (ear-to-head clearance min) | none (0.38 cm) | none (0.45 cm) |
| Branch quad aspect > 10 | 0 (max 9.29) | 0 (max 8.71) |

## 3. T-4 (corner outside 45–135°) — v001 E2 → v002 E2, identical zone definitions (`ear_zones.py`)

| Zone | c1 v001 | c1 v002 | c2 v001 | c2 v002 |
|---|---|---|---|---|
| **Branch-wide** | 450 / 2854 (15.8 %) | **165 / 3718 (4.4 %)** | 465 / 2854 (16.3 %) | **145 / 3718 (3.9 %)** |
| Upper extension (F2 / leaf + rim_up) | 222 / 768 (28.9 %) | **30 / 960 (3.1 %)** | 222 / 768 | **30 / 960 (3.1 %)** |
| Upper extension by s ≥ 0.52 (geometric) | 232 / 632 (36.7 %), min 7.1° | 36 / 1088 (3.3 %), min 35.1° | same as c1 | same as c1 |
| Cuff count-transition quads | 31 / 74 (41.9 %), min 5.8° | **10 / 70 (14.3 %)**, min 10.7° | 31 / 74, min 9.1° | **7 / 70 (10.0 %)**, min 12.9° |
| Attachment corners (≤ 0.5 cm of c0 / c1) | 66 / 141 (46.8 %), min 5.8° | **34 / 136 (25.0 %)**, min 19.7° | 67 / 144, min 6.7° | **24 / 138 (17.4 %)**, min 22.2° |
| Lobe cusp (≤ 0.8 cm of c0f) | 20 / 158 (12.7 %) | 18 / 175 (10.3 %) | 20 / 154 | 18 / 173 (10.4 %) |
| Front / back / rim | 150 / 132 / 10 | 60 / 22 / 8 | 150 / 132 / 10 | 60 / 22 / 8 |
| Cuff (incl. root band) | 142 / 722 | 57 / 722 | 157 / 722 | 39 / 722 |
| Root band | 16 / 104, min 19.5° | 8 / 104, min **7.9°** | 20 / 104, min 18.2° | 7 / 104, min **12.7°** |
| Transition (v005 faces) | 16 / 204 | 18 / 204 | 16 / 204 | 16 / 204 |
| Branch min corner | 5.8° | 7.9° | 6.7° | 12.7° |
| Aspect > 4 / > 6 / max | 98 / 1 / 6.01 | 129 / 17 / 9.29 | 96 / 2 / 6.27 | 121 / 19 / 8.71 |

The v005 ear-zone baseline is 3.4 %, so v002 is close to the surrounding body standard. Records: `FENN_EAR_v001_v002_zone_report.json`, `FENN_EAR_v001_v002_comparison.json`.

### Documented residual

- **Root-band cells.** Positions 28 / 31 / 72 / 75 / 76 / 78 of the 104 root-band quads have a 165–177° corner in both versions; they are triangle-like quads where the band meets the root loop.
  - v002 leaves 1–2 of them sharper than v001:
    - c1: position 75 at 7.9°, position 28 at 10.0°;
    - c2: position 78 at 12.7°.
  - On c1, position 75's vertices are contact-held: they are frozen in the quality pass because moving them makes the cuff touch the head.
  - R3 recovered the crease-driven cell on c2 (position 75: 7.1° → above 25°).
  - The remaining cells would need a root-band topology change, which this order locks.
- **Aspect.** 17 / 19 quads now fall between aspect 6 and 10. They are the denser leaf / crescent rows near the cut and rim, and the log-aspect barrier keeps all of them below 10.
- **Bridge corner.** The reflex corner of the 28 × 3 bridge block at the concha floor (bottom of the front view in sheet 12) keeps a cluster of obtuse cells.

## 4. Density (≤ 0.25 % of stature)

| | c1 v001 | c1 v002 | c2 v001 | c2 v002 |
|---|---|---|---|---|
| Vertices / quads per side | 1,300 / 1,325 | 1,732 / 1,757 (+432) | 1,300 / 1,325 | 1,732 / 1,757 |
| Branch mean edge | 0.210 cm (0.116 %) | 0.178 cm (0.098 %) | 0.205 cm (0.113 %) | 0.173 cm (0.095 %) |
| p95 edge | 0.199 % | 0.170 % | 0.192 % | 0.167 % |
| Faces / v005 ear-zone faces | 1.18 | 1.54 | 1.18 | 1.54 |

The added rows are the crescent (28 rows × 12 across the whole notch) and the 23-row tapered leaf with its 184-face rim strip, replacing the 144-face kite. Density stays valid.

## 5. Root integration (no worse than v001)

| | c1 v001 | c1 v002 | c2 v001 | c2 v002 | v005 baseline |
|---|---|---|---|---|---|
| Root-loop crease max (l / r) | 73.0° / 71.5° | **64.0° / 64.0°** | 64.6° / 66.5° | **64.0° / 64.0°** | 71.1° (c1) / 67.1° (c2) |
| Root-loop crease mean | 29.1° / 30.2° | 28.9° / 28.7° | 27.8° / 28.4° | 27.4° / 27.6° | 29.2° / 26.9° |
| Transition ring displacement max | 0.054 cm | 0.057 cm | 0.056 cm | 0.059 cm | — |
| Cuff skin vs hidden-ear skull, mean / p95 / max | 0.205 / 0.482 / 0.602 cm | 0.199 / 0.471 / 0.597 cm | 0.222 / 0.548 / 0.666 cm | 0.223 / 0.528 / 0.664 cm | — |

- Root vertices are fixed (root deviation 0).
- No new posterior-lip crease: the lobe-region sharpest fold drops from 156.5° / 154.7° to 80.6° / 73.8° (`FENN_EAR_v002_lobe_cusp_metrics.json`).
- Root integration does not regress. The root-band cell residual (§3) is the one local quality item.

## 6. Static deformation readiness (same 8 poses: neck flex / ext 30, head yaw ±45, pitch ±20, roll ±20)

| | c1 v001 | c1 v002 | c2 v001 | c2 v002 |
|---|---|---|---|---|
| New self-intersections touching the branch / flipped branch faces / root-band inversions | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| Ear to non-head clearance, min over poses | 3.59 cm | 3.56 cm | 3.24 cm | 3.21 cm |
| Root-loop edge strain (yaw 45, worst) | −15.8 / +17.4 % | identical | −16.9 / +20.0 % | identical |

Root strain is identical because the root loop is fixed. The deformation guard converged in one iteration on both configurations (3 faces held at the untangled state). Records: `deform/`, `build/*_deform_guard*.json`.

## 7. Shape probes (10; geometry only, shared topology, c1 E2 base)

| Probe | T-4 | Aspect max | Min ∠ | Self-intersection / boundary | Measure moves as intended |
|---|---|---|---|---|---|
| len −10 % / +10 % | 151 / 159 | 9.06 / 8.39 | 9.8 / 11.4 | 0 / 0 | chord 7.22 / 8.99 cm (base 8.10) ✓ |
| proj 40 / 60 | 131 / 139 | 8.65 / 9.33 | 7.9 / 12.3 | 0 / 0 | body angle 42.8 / 62.6° (base 52.7) ✓ |
| sweep 1.0 / 2.2 | 159 / 128 | 8.91 / 8.50 | 8.8 / 16.6 | 0 / 0 | sweep 0.59 / 0.96 cm (base 0.77) ✓ |
| tilt 24 / 40 | 140 / 140 | 8.71 / 8.71 | 17.7 / 14.4 | 0 / 0 | upper axis 25.9 / 39.6° (base 32.3) ✓ |
| tip blunt / sharp | 143 / 211 | 8.71 / 8.71 | 8.9 / 7.9 | 0 / 0 | tip angle 52.5 / 17.9° (base 32.9) ✓ |

- No probe has a self-intersection, a broken root, aspect > 10, or catastrophic T-4: the worst is tip_sharp at 5.7 %, against v001's 15.8 % on the base.
- v002 is not over-specialised to E2. The R1 tip_sharp failure (aspect 16.4) was corrected in R2, and the R3 `sweep_m06` aspect 10.1 was corrected in R3 itself (provenance).
- Record: `probes/FENN_EAR_shape_probes.json`, sheet 18.

## 8. CF2 / hidden-ear regression

- Outside-branch vertices are byte-identical to the CF2 family realization on both configurations.
- All 19 hidden-ear landmark family vertices lie outside the branch and are byte-identical.
- Source descriptors are unchanged (`FENN_EAR_hidden_ear_CF2_regression.json`, sheet 20).
- Immutable hashes are re-verified and equal to the v001 gate record (`immutable_family_and_source_hashes.txt`): v005 blend + hm08 map, v005 freeze record, FNL4 / FNF181 / CF2 R-6, CF2 builds, CF2 family realizations.
- FENN-CF-1 (c2 mouth corner) is unchanged: no face vertex moved.

## 9. E2 identity (v002 − v001, c1; c2 within 0.01 of these)

| Measure | Δ |
|---|---|
| lobe-to-tip length | −0.06 cm (8.10 cm) |
| auricle height | +0.11 cm |
| max width | +0.02 cm |
| auricle–body angle | +0.6° |
| lateral extent | 0.00 cm |
| side-view upper extension | 0.0° |
| sweep max axis deviation | +0.06 cm |
| tip in-plane angle | −0.04° |
| thickness median | −0.005 cm |

The minimum thickness falls from 0.28 to 0.15 cm at the thinned lobe edge (target D, lobe_thin). Sections (sheet 21) and the identical-camera views (sheets 01–06) show the same silhouette.

## 10. Refinement budget

| Round | What | Why |
|---|---|---|
| R1 | Leaf layout, crescent cut, cuff quality pass, knob removal, guard | primary |
| R2 | Near-tip row tightening, adaptive aspect repair, stronger guard | R1 probe tip_sharp aspect 16.4 |
| R3 | Root-crease cap 60 → 64°; aspect-repair fallback | R2 root-band cells at 7–10° (crease-driven); one probe face at 10.1 |

Details, sweeps and rejected variants: `FENN_EAR_v002_refinement_provenance.md`.

## 11. Answers (§21)

| Question | Answer |
|---|---|
| Is E2 preserved as the selected Fenn central ear? | **Yes.** Same parameters; silhouette and measures within 0.11 cm / 0.6°. |
| Did upper-extension T-4 improve? | **Yes**, 222 → 30 faces (28.9 % → 3.1 %), both configurations. |
| Did cuff-transition T-4 improve? | **Yes**: 31 → 10 (c1) and 31 → 7 (c2); min corner 5.8 → 10.7° / 9.1 → 12.9°. |
| Did attachment-corner quality improve? | **Yes**: 46.8 → 25.0 % (c1), 46.5 → 17.4 % (c2); min corner 5.8 → 19.7° / 6.7 → 22.2°; no aspect > 10. |
| Was the lobe-cusp knob removed? | **Yes.** Lobe-front cuff shoulder lowered 0.19 / 0.18 cm at J; sharpest lobe fold 155° → 74–81°; no new crease or dent. |
| What is the final branch-wide T-4 rate? | **4.4 % (c1, 165 / 3718), 3.9 % (c2, 145 / 3718)**. |
| Did any aspect > 10 appear? | **No.** Configurations max 9.29 / 8.71; probes max 9.33. |
| Did density remain valid? | **Yes**: 0.098 % / 0.095 % mean, p95 0.170 % / 0.167 % (limit 0.25 %). |
| Did root integration regress? | **No.** Crease max 64.0° (v001 73.0 / 66.5°), transition ≤ 0.059 cm, root fixed. Documented residual: 1–2 root-band cells sharper than v001 (§3). |
| Did static deformation readiness regress? | **No**: 0 / 0 / 0 on all 8 poses, both configurations. |
| Did shape-probe readiness regress? | **No**: 10 / 10 clean, measures move as intended, T-4 3.4–5.7 %. |
| Did CF2 / hidden-ear identity remain unchanged? | **Yes.** Byte-identical outside the branch; hashes equal. |
| Is the ear branch ready for final Fenn consolidation? | **Yes, subject to the author accepting the documented residual** (root-band cells, aspect 6–10 band, bridge-corner obtuse cells). The consolidation package is prepared and not executed: `FENN_FINAL_CONSOLIDATION_PACKAGE.md`. |

## 12. Visual package (`sheets/`, identical cameras per sheet, v001 | v002)

Each sheet exists for c1 and c2 unless noted:

| Sheets | Content |
|---|---|
| 01–06 | front / profile / ¾ front / ¾ rear / rear / top |
| 07 | wireframe |
| 08 | upper extension |
| 09 | cuff transitions |
| 10 | attachment corners |
| 11 | lobe cusp |
| 12 | T-4 heat |
| 13 | aspect heat |
| 14 | poles |
| 15 | root integration |
| 16 | thickness |
| 17 | deformation |
| 18 | probes (c1 only) |
| 19 | c1 vs c2 (single sheet) |
| 20 | hidden-ear CF2 |
| 21 | sections |

Key sheets: 08 (upper extension), 12 (T-4), 11 (lobe cusp), 19 (c1 vs c2).

## 13. Production review files (E:, not frozen)

`E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Fenn/RP3/ear_branch_v002/`:

- `FN_M_REF_RP3_cf2_earE2_v002.blend` (`fc13da73…`)
- `FN_F_REF_RP3_cf2_earE2_v002.blend` (`d9d26f37…`)
- sidecar JSONs
- `FENN_EAR_BRANCH_MAP_v005_v002.npz / .json`

Read-back hashes: `production/pc_readback_sha256.txt`.

## 14. Stop

STOP FOR CHATGPT REVIEW.

- No freeze.
- No Aelari / Vael / Halvren.
- No universal elf-ear claim.
- v005 unmodified.
- No ear rig, morphs, UV / materials, LODs or UE5.
