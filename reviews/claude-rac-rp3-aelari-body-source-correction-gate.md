# Claude gate — RAC RP3 Aelari body-source correction (order 0f6aba8)

**Order:** `reviews/chatgpt-rac-rp3-aelari-body-source-correction-order.md` (0f6aba8)
**Evidence:** `reviews/rac-rp3-evidence/aelari_rp3_correction/`
**Date:** 2026-10-27
**Tools:** `tools/rac/rp/aelari_rp3_v001/`:
- `probe_corr.sh`, `build_corr.sh`, `corr_matrix.py`;
- `run_aeeval.sh` (`AE_C1` / `AE_C2`), `run_ae_r1_prod.sh`, `ae_manifest.py` (`AE_C1` / `AE_C2` / `AE_PROD_VER`);
- `ae_partA.py` (`AE_ORDER`), `ae_hidden_ear.py` (`AE_HE_C1` / `AE_HE_C2`);
- `run_ae_ear.sh` (`AE_H1` / `AE_H2` / `AE_CF` / `AE_EAR_CANDS` / `AE_EAR_VER` / `SKIP_PROBES`);
- `ae_ear_regress.py`, `ae_corr_sheets.py`.

All defaults reproduce the fd71f15 behaviour. No Fenn tool was edited.

## Verdict

# AELARI BODY SOURCE CORRECTION PASS — READY FOR FINAL CONSOLIDATION

Both inherited AEL1 ties are corrected on c1 and c2 with one shared source-level change: three existing MPFB bone scales, then the stature re-solved to 190 cm.
- **Thoracic vertical:** now above frozen Fenn — c1 +1.00 % (was −0.62 %), c2 +1.32 % (was −0.33 %).
- **Leg segments:** thigh / lower leg is now distributed more evenly than Fenn. The gap of shin / leg to Marchfolk roughly halves:
  - c1 0.0096 (was 0.0198; Fenn 0.0192);
  - c2 0.0094 (was 0.0197; Fenn 0.0203).

Nothing else regressed:
- stature unchanged (189.98 / 190.00 cm);
- every share outside the two targets moved by ≤ 0.43 %;
- pelvis rules hold at t = 0 / 0.5 / 1.0;
- both family realizations stay 69 / 69 D1–D6;
- hidden-ear face is unchanged (head shape RMS 0.010 / 0.012 mm);
- AE-E2 regresses cleanly with identical parameters, topology and root.

The original AEL1 and AELF190 are retained unchanged as ancestry. Nothing is frozen.

Three things the reviewer should see plainly (none fails a gate; detail in §3–§4):
1. **Torso share rose** +0.68 % (c1) / +0.58 % (c2). This is the coupled response to the thoracic change, which the order allows. It was the smallest of the probed routes. Torso share stays between Fenn and Marchfolk.
2. **Leg share fell** −0.41 % / −0.36 %. This comes from the global stature re-solve, not from the leg controls; the leg probes alone moved leg share by 0.00 %. Leg share stays above Marchfolk, but the margin narrows from +0.75 % to +0.34 %.
3. **Waist interval / torso** still exceeds Fenn (c1 +1.29 %, c2 +0.60 %), with smaller margins than before.

## 1. Exact source-control change (Q1)

| Control (MPFB bone scale, Y) | AEL1 / AELF190 | AEL1-R1 / AELF190-R1 |
|---|---|---|
| `spine_03` | 0.9704 | **0.99** |
| `LR:thigh` | 0.9875 | **1.01** |
| `LR:calf` | 1.0523 | **1.03** |
| height macro (re-solved to 190 cm) | c1 0.5625; c2 0.66187 | c1 0.55762; c2 0.65649 |

- **No other control changed:** no target, no other bone scale, and no composition change.
- **c1:** `build_variant.py` on `AEL1_build.json` plus `sources/AEL1-R1_overrides.json`.
- **c2:** the accepted AELF190 route (MF-F-R base plus the full Aelari cfg), carrying the identical three values (`sources/AELF190-R1_overrides.json`). The same biological logic applies to both configurations.

Records in `reviews/reference-assets`. Both are CANDIDATE manifest entries; the originals are untouched.

| Source | r6 sha256 | build sha256 | stature |
|---|---|---|---|
| AEL1-R1 | `17ae6d13…` | `73ec892f…` | 189.985 cm |
| AELF190-R1 | `93a951d5…` | `73fab1c8…` | 189.995 cm |

**Determinism:**
- An independent second full re-solve (R1a) is byte-identical: dV 0.0, same height macro.
- `regen.py` from the committed record is geometry-identical (dV 0.0) on both.

### Probe matrix (§4; `probe/probe_matrix.json`, `probe/cand_matrix.json`)

Probes on AEL1 with the height macro held; % change vs AEL1.

| Probe | Change | Stature | Thoracic | Torso | Waist / torso | Leg | shin / leg | Thoracic vs Fenn |
|---|---|---|---|---|---|---|---|---|
| T1 | spine_03 → 1.00 | +0.54 | +2.35 | +0.97 | −1.49 | −0.53 | 0 | +1.72 |
| T2 | spine_03 → 1.03 | +1.08 | +4.72 | +1.95 | −2.96 | −1.07 | 0 | +4.07 |
| T3 | T2 + spine_02 0.97 | +0.98 | +4.82 | +1.68 | −3.94 | −0.97 | 0 | +4.17 |
| T4 | larger | +1.46 | +7.23 | +2.47 | −6.00 | −1.44 | 0 | +6.57 (exaggerated) |
| L1 | thigh 1.01 / calf 1.03 | 0 | 0 | 0 | 0 | **0** | −2.13 | — (gap to MF 0.0088) |
| L2 | 1.025 / 1.015 | 0 | 0 | 0 | 0 | 0 | −3.55 | gap 0.0014 (≈ human) |
| L3 | 1.035 / 1.005 | 0 | 0 | 0 | 0 | 0 | −4.50 | gap −0.0034 (overshoots MF) |

How the candidate was chosen:
- **Thoracic:** spine_03 is the only clean ribcage lever. spine_02 erodes the waist interval (T3).
- **Leg:** the leg controls redistribute without changing leg share or hip height. L1 is the smallest step that is clearly more even than Fenn. L2 / L3 push the ratio to or past human, which would be extreme.

Candidates at 190 cm (re-solved):
- **R1a** (spine_03 0.99 + L1) gives thoracic vs Fenn +1.00 / +1.32 %, with every unrelated share ≤ 0.43 %.
- **R1b** (spine_03 0.995) gives +1.40 / +1.75 %, but arm share moves −0.53 % on c2, over budget. Rejected; overrides kept as `sources/*R1b_overrides_rejected.json`.
- R1a became **R1**.

## 2. Thoracic vertical vs Fenn (Q2) — YES, both configurations

Skin rig measure: clavicle-head mid − spine_03 head, over stature, at 190 cm (`metrics/AELARI_R1_metrics_vs_FN_MF_SG.json`).

| | Original | R1 | Fenn | Marchfolk | R1 vs Fenn |
|---|---|---|---|---|---|
| c1 | 0.14313 | **0.14546** | 0.14402 | 0.15076 | **+1.00 %** (was −0.62 %) |
| c2 | 0.12978 | **0.13192** | 0.13021 | 0.13696 | **+1.32 %** (was −0.33 %) |

- The value stays below Marchfolk (−3.5 % / −3.7 %), so no long-chest exaggeration.
- Thoracic depth stays shallow: depth share < MF −6.3 % / −6.9 %, and < Fenn.
- Breadth is unchanged.

Sheets: AEC_04, AEC_00.

## 3. Leg segment distribution (Q3, Q4)

| | shin / leg: Original | R1 | Fenn | MF | Gap to MF: R1 | Fenn |
|---|---|---|---|---|---|---|
| c1 | 0.51633 | **0.50611** | 0.51572 | 0.49654 | **0.0096** | 0.0192 |
| c2 | 0.48833 | **0.47812** | 0.48897 | 0.46868 | **0.0094** | 0.0203 |

**Q3 — yes on c1 and c2.** The distribution is about twice as close to the human even split as Fenn's, and neither segment is extreme: still elven-leaning, not human. The knee joint moves down 1.2 cm.

**Q4 — essentially unchanged.**
- Leg share c1 0.54421 → 0.54198 (−0.41 %); c2 0.53635 → 0.53444 (−0.36 %). Within the 0.5 % budget.
- The leg controls themselves move leg share by 0.00 % (L1). The change is the global stature re-solve paying for the longer thorax.
- Leg share stays > MF (c1 +0.34 %, c2 +0.35 %; was +0.75 / +0.71 %) and < Fenn. Long-leg identity holds, with a narrower margin over humans.
- The hip joint is 0.44 / 0.37 cm lower in absolute terms.

## 4. Torso share and the rest of the §8 canon (Q5)

**Torso share** (suprasternal − hip centre) rose c1 0.27413 → 0.27599 (+0.68 %) and c2 0.27666 → 0.27827 (+0.58 %).
- The rise comes from the thoracic gain, partly offset by the waist interval (−1.12 / −0.97 %).
- It stays > Fenn (+2.4 %) and < MF.
- Reading: essentially unchanged, within the narrow coupled response the order allows (§6); every probe that raises the thorax raises torso share about 0.4 × as much.

Other shares, % change vs original:

| Share | c1 | c2 |
|---|---|---|
| stature | −0.02 | −0.00 |
| neck | −0.25 | −0.24 |
| arm | −0.36 | −0.43 |
| pelvic vertical | −0.24 | −0.30 |
| cranial vertical | −0.16 | −0.32 |
| thorax depth / breadth | ≈ 0 (scale only) | ≈ 0 (scale only) |

**§8 canon** (`metrics/AELARI_R1_canon_pelvis_validation.json`): c1 16 / 19 (was 14), c2 17 / 19 (was 16).
- The two new passes are exactly the two corrected rows.
- The remaining fails are the pre-existing skin gracility rows: c1 wrist, knee, ankle; c2 knee, ankle. These are diagnostic only, because knee / ankle skin breadth is unstable across the height macro (fd71f15 gate). Their values are unchanged within ±0.4 %.

All vs-Fenn rows hold on both configurations, as do all vs-human rows (leg, arm, hand, foot share; shallow ribcage):

| Row | c1 | c2 |
|---|---|---|
| central vertical vs Fenn | +2.67 % | +2.56 % |
| extremity vs Fenn | −2.73 % | −2.79 % |
| neck vs Fenn | +5.6 % | +4.2 % |
| cranial vs Fenn | +1.6 % | +1.8 % |

## 5. Pelvis (Q6) — valid

Skeletal proxy (lean build), t = 0 / 0.5 / 1.0. All six rules hold at all three t on both configurations (`pelvis/`, sheet AEC_06).

| Rule | c1 orig → R1 | c2 orig → R1 |
|---|---|---|
| AE-P2a hip-joint height / stature > MF | +0.75 → +0.34 % | +0.71 → +0.35 % |
| AE-P2b bitroch / crest ≥ MF | +0.80 → +0.85 % | +0.51 → +0.53 % |
| AE-P3 pelvic vertical / crest > MF | +10.6 → +10.7 % | +10.4 → +10.5 % |
| AE-P3 pelvic vertical / crest > Fenn | +10.4 → +10.4 % | +10.2 → +10.2 % |
| AE-P6 waist / torso > Fenn | +2.48 → +1.33 % | +1.61 → +0.62 % |
| AE-P6 waist / torso ≥ MF | +1.72 → +0.59 % | +1.80 → +0.81 % |

The pelvis bone scales are untouched. The AE-P2a and AE-P6 margins narrow, as described in §3 and §4.

## 6. Hidden-ear identity (Q7, Q8)

`hidden_ear/AE_hidden_ear_identity_R1.json`; sheets AEC_03, AEC_07, AEC_08.

**Body (Q7) — improved, not exaggerated.**
- Equal-height region RMS, original → R1:

  | Region | vs Fenn: c1 | vs Fenn: c2 | vs Marchfolk: c1 | vs Marchfolk: c2 |
  |---|---|---|---|---|
  | trunk | 10.0 → 13.6 mm | 10.4 → 13.2 mm | 11.0 → 9.6 mm | 10.9 → 9.6 mm |
  | leg | 15.7 → 23.3 mm | 16.1 → 23.6 mm | 14.0 → 9.3 mm | 13.4 → 9.1 mm |

- So Aelari separates further from Fenn, and does so by moving toward a human balance rather than past it.
- Central vertical vs Fenn is +2.67 / +2.56 % (was +2.26 / +2.23 %).
- Displacement original → R1:
  - max 12.8 / 12.3 mm, p95 6.9 / 6.6 mm;
  - concentrated in the thigh / knee (mean 7.8 mm) and lower trunk (3.7 mm);
  - head ≤ 1.3 mm (scale only).
- The silhouette is recognisably the same central Aelari (AEC_01 / AEC_02 overlays).

**Face (Q8) — unchanged.**
- Head shape after similarity alignment, original → R1: RMS 0.010 mm (c1) / 0.012 mm (c2), max 0.03 / 0.06 mm.
- The only change is the uniform scale from the stature re-solve: head height c1 24.97 → 24.91 cm, c2 24.13 → 24.06 cm.
- Face canon systems stay 7 / 7 directional and material on both configurations; all Fenn relations hold.
- Descriptors move ≤ 0.06 %, except:
  - `cranial_height_over_stature` −0.16 / −0.32 %: the same uniform rescale.
  - c2 eye-aperture elongation 2.762 → 2.900: a one-step quantisation of the 0.04 cm ray-grid aperture height (0.84 → 0.80 cm) in `arm_measure.py`. The geometry is identical; aperture area −0.75 %, matching the scale.
- No craniofacial target was touched.

## 7. Family realizations (Q9) — 69 / 69 both

Standard v1 pipeline on unchanged frozen MPFB v005 (`run_aeeval.sh`; `family/`, `validator/`, `audit/`, `anatomy/`, `contact/`, `deformation/`, `regen/`).

Topology:
- face-hash equal, faces / UV / map identical to v005;
- `V = M @ hm08` exact (0.0).

| Gate | AE_M_REF_RP3_bodyfam_v002 (AEL1-R1) | AE_F_REF_RP3_bodyfam_v002 (AELF190-R1) |
|---|---|---|
| D1–D6 firm (without D6) | 69 / 69 (69) | 69 / 69 (69) |
| Margin changes vs original | 3 stations, all +1 | 9 stations, all +1 |
| Margin-zero set | unchanged (thumb_mcp, toe1_j1) | unchanged (toe1_j1) |
| Anatomy T-1 / T-2, T-3, T-7; IoU min | pass; 0.9976 | pass; 0.9979 |
| Density (9 zones) | all pass | all pass |
| Mouth / orbit rings | pass | pass |
| Integrity | 1 component, 0 boundary / non-manifold / degenerate, outward | same |
| Self-intersection pairs (orig) | 62 (64) | 154 (158) |
| Contact source / family / new | 56 / 6 / 0 | 154 / 0 / 0 |
| Deformation worst flip excess vs MF v005 (orig) | 4 (4), no pose > 5 | 1 (1), no pose > 5 |
| Read-back (blend vs candidate) | 6.0e-8 m | 6.0e-8 m |

Native hm08 is clean: 13,380 V, 1 component, 0 defects.

## 8. AE-E2 regression (Q10) — clean

AE-E2 was rebuilt with **identical parameters** on the corrected heads, using Fenn v002 engineering topology unchanged (`ear/AELARI_AE-E2_regression.json`, sheets AEC_11 / AEC_12).

| | c1 AEL1 → AEL1-R1 | c2 AELF190 → AELF190-R1 |
|---|---|---|
| params identical | yes | yes |
| face list = frozen Fenn v002 | yes | yes |
| T-4 | 117 → 117 | 120 → 120 |
| aspect max (>10) | 8.29 → 8.28 (0) | 8.55 → 8.55 (0) |
| self-intersection (branch) | 0 → 0 | 0 → 0 |
| outside branch byte-identical | yes | yes |
| root valence / crease max | ok; 51.9° → 51.9° | ok; 51.6° → 51.5° |
| transition / clearance | 0.065; 0.73 cm | 0.070; 0.71 cm |
| guard iterations / 8-pose readiness | 1; 0 / 0 / 0 | 1; 0 / 0 / 0 |
| length (head scale) | 9.70 → 9.67 cm | 9.37 → 9.35 cm |

Integrity: 0 boundary, 0 non-manifold, 1 component.

Every ear measure normalised by head height is unchanged: 0.00 %, except c1 lateral extent −0.08 %. The Fenn E2 vs Aelari AE-E2 firewall is as before (AEC_12).

## 9. Ready for final consolidation? (Q11) — YES

All required gates pass on both configurations, and no new residual arises. The open items are the author's call at consolidation, not blockers:
- accept AEL1-R1 / AELF190-R1 as the central Aelari sources (originals retained);
- confirm the narrower margins (leg > MF +0.34 %, waist / torso > Fenn +0.60 % on c2) are acceptable;
- keep the skin gracility rows as diagnostics, as in fd71f15.

## 10. Answers

1. **Exact source controls changed:** spine_03 Y 0.9704 → 0.99; thigh Y 0.9875 → 1.01; calf Y 1.0523 → 1.03; height macro re-solved to 190 cm. Identical on c1 and c2.
2. **Thoracic vertical above Fenn:** yes — c1 +1.00 %, c2 +1.32 %.
3. **Leg distribution more even than Fenn:** yes — gap to human c1 0.0096 vs Fenn 0.0192; c2 0.0094 vs Fenn 0.0203.
4. **Leg share unchanged:** essentially yes — −0.41 / −0.36 %, still > MF and < Fenn.
5. **Torso share unchanged:** essentially yes — +0.68 / +0.58 %, the coupled response; still > Fenn, < MF.
6. **Pelvis valid:** yes — 6 / 6 rules at all t on both configurations.
7. **Hidden-ear body improved without exaggeration:** yes — further from Fenn, closer to the human balance; displacement ≤ 12.8 mm.
8. **Hidden-ear face unchanged:** yes — shape RMS ≤ 0.012 mm; 7 / 7 systems.
9. **Family realizations 69 / 69:** yes, both.
10. **AE-E2 integration clean:** yes — identical parameters / topology / root; gates unchanged.
11. **Ready for final consolidation:** yes.

## 11. Deliverables

Repository:
- **Sources:** `reviews/reference-assets/{r6,builds}/AEL1-R1*`, `AELF190-R1*` (r6, build, meas); manifest CANDIDATE entries (24 insertions, no other change).
- **Evidence** `reviews/rac-rp3-evidence/aelari_rp3_correction/`:
  - `sources/` (overrides, second re-solve builds, rejected R1b);
  - `probe/`, `metrics/`, `pelvis/`, `regen/`, `validator/`, `audit/`, `anatomy/`, `contact/`, `deformation/`;
  - `family/` (sidecars, landmarks, manifest v002, deformation comparison, AELF190-R1 sidecar);
  - `hidden_ear/`, `ear/`;
  - `sheets/` (AEC_00 metrics, then AEC_01–AEC_12 for the 12 §14 items);
  - `immutable_hashes.txt` — v005, freeze, AEL1, AELF190, Fenn freeze and v002 topology all re-verified unchanged;
  - `pc_readback_sha256.txt`.

PC: `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Aelari/RP3/`
- `AE_{M,F}_REF_RP3_bodyfam_v002.blend` with `_hm08_map.npz`, `.json`, `_landmarks.json`;
- `AELARI_RP3_bodyfam_propagation_manifest_v002.json`, `AELF190-R1_central_reference_sidecar.json`;
- `ear_branch/AE_{M,F}_REF_RP3_earE2_proto_v002.blend` (+ `.json`).
- Read back byte-identical. The v001 files are untouched.

Not done, per the stop rules:
- no freeze, and no face or AE-E2 redesign;
- no Vael / Halvren work;
- no change to frozen Fenn or v005;
- no rigging, UV, LOD or UE5 work.

**STOP FOR CHATGPT REVIEW.**
