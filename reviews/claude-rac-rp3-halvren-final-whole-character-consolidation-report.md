# Claude Report — RAC RP3 Halvren Final Whole-Character Consolidation / Freeze Readiness

**Order:** `reviews/chatgpt-rac-rp3-halvren-final-whole-character-consolidation-freeze-readiness-order.md` (fd22665; reviewed commit 0aeaf0e)
**Date:** 2026-10-30
**Evidence:** `reviews/rac-rp3-evidence/halvren_rp3_final_whole/`
**Tools:** `tools/rac/rp/halvren_rp3_v001/`
- `run_hvfinal.sh`
- `run_hvfinal_eval.sh`
- `run_hvfinal_prod.sh`
- `hv_make_prod.py`
- `hv_tri_readback.py`
- `hv_final_gates.py`
- `hv_final_sheets.py`

## Recommendation

**HALVREN RP3 WHOLE-CHARACTER FINAL FREEZE RECOMMENDED**

All 12 freeze-readiness criteria in §11 are met on the measured record. Two items go to the author, and neither is a consolidation defect:

- **Blind identity review: overall FAIL.** The independent reviewer's FAIL is driven by Q6, the surface quality of the frozen HE2 auricle:
  - concha / scapha relief;
  - rear rim crumple;
  - lower-rear flap.

  These are the author-accepted residuals of the ear-family freeze. In a regression comparison against the frozen-ear boards, the same reviewer found them **identical, not new or worse**. The order forbids reopening HE2 / HR2.
- **Hidden-ear read is subtle.** It is the nearest figure to Marchfolk, with body slenderness carrying the signal. This is exactly the accepted HB2 + HF2 + HP-B source read; the sources match it at dV 0. Order §7 says not to reopen it for subtlety.

Candidate record: `halvren_rp3_final_whole/HALVREN_RP3_FREEZE_CANDIDATE.json` (contains the hashes and the proposed freeze-by-record action, §12 below).

## 1. Source lineage

| Reference | Config | Source | Build record sha256 | r6 sha256 | Family realization sha256 | Ear |
|---|---|---|---|---|---|---|
| `HV_M_REF_RP3_v001` | c1 | HVC1-HB2HF2-HPB | `ea4be405…` | `3ae231a8…` | `1af30766…` | HE2 HVEAR3 + HR2, V `b88da857…`, Q `9629e171…`, TRI-HV1 `9e18beb9…` |
| `HV_F_REF_RP3_v001` | c2 | HVF178-HB2HF2-HPB | `827b6568…` | `fc47ba4b…` | `562c13bf…` | HE2 HVEAR3 + HR2, V `eb18b3c7…`, Q `9629e171…`, TRI-HV1 `db0bbcdc…` |

**Composition:**
- Body: HB2
- Face: HF2
- Pelvis: HP-B
- Base: MPFB Family Base v005, outside the ear branch
- Topology: VAEL_EAR_BRANCH_TOPOLOGY_v002 sheet + RI3 cuff canon (`1a0b070b…`)
- Face topology: `f8367ab0…`

The HE1 / HE3 bounds are not used. There is no third anchor.

## 2. Final candidate assets

Location: `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Halvren/RP3/`. Naming follows the Fenn / Aelari / Vael convention: blend, sidecar json, branch map, landmarks, TRI-HV1 sidecar and manifest.

| File | sha256 |
|---|---|
| HV_M_REF_RP3_v001.blend | `4a360bc83f9cd09ce859cd2ae2ff448e81b5f2a0545a60e2b458c2073b7342f8` |
| HV_M_REF_RP3_v001.json | `589c2d9edfa086a2c7d090acf1b101649be4479760be4263ed1276ac11aacd82` |
| HV_M_REF_RP3_v001_TRI-HV1.npz | `92c81c4f44cbb7216f51a4ad4864f9859b5bc3a4db901238951a10df467d0c3f` |
| HV_M_REF_RP3_v001_branch_map.npz | `d0785b4a38438970b8349282094a317dc72143b58a87d4e6439bb55c2d616179` |
| HV_M_REF_RP3_v001_landmarks.json | `bc03ef766594464d2a180adb0a5a5c5ac74ba4dea8c9f7e0100eaa980de84890` |
| HV_F_REF_RP3_v001.blend | `0e830248dffbabfa803839c8d3dc9567d349a1d1f588813c93c49ce60d62b9fa` |
| HV_F_REF_RP3_v001.json | `7b22e2f8fcad40fe2b913508eeebf18b981df85f143d9ec5818e04cc3c0b86cc` |
| HV_F_REF_RP3_v001_TRI-HV1.npz | `f01d2d9494717780ea271c993d48c88ca185d2282b326f2fc784a5e3e4a6812c` |
| HV_F_REF_RP3_v001_branch_map.npz | `1e8e82e004fdebd5960ed3f39d3935c2d47918e65cb8800cf91714044499ade6` |
| HV_F_REF_RP3_v001_landmarks.json | `e4ead6736cda9fbdd9b9715df2493c519632aaa7815558b74bb3479466c4029b` |
| HALVREN_RP3_final_reference_manifest.json | `1dbe037c4be7f4b4b86caec0bb7673f2a89bebdddce14ccb18d0634dc5f40001` |

**Geometry hashes:**
- M: `133f22ee4a15eb949881755a0a62b84f938fef032aca5b461ba2034320a39d66`
- F: `ca90812f80e6d40fd0ca02f587e68921cd4f6d5e7900b4538c8cefc4e56e1a20`

**Mesh:** 59,076 vertices / 59,074 quads each.

**TRI-HV1** is carried in two places:
- the face attribute `TRI_HV1_diagonal` in the blend;
- the `NAME_TRI-HV1.npz` sidecar. The triangles' sha256 is asserted equal to the frozen hash at write time.

**Status:** the embedded status reads "CANDIDATE … NOT frozen".

## 3. Clean rebuild / determinism

The rebuild ran in a fresh folder (`run_hvfinal.sh`) from committed inputs only.

| Check | c1 | c2 |
|---|---|---|
| R-6 regeneration geometry = committed (max dV) | identical (0.0) | identical (0.0) |
| Full record rebuild = committed r6 (max dV, faces) | 0.0, faces identical | 0.0, faces identical |
| Measurements = committed `_meas.json` | yes | yes |
| Fresh family realization = accepted (byte) | yes | yes |
| HE2 / HR2 V float32 = ear-family freeze | `b88da857…` yes | `eb18b3c7…` yes |
| HE2 Q = freeze | `9629e171…` yes | `9629e171…` yes |
| HE2 guard iterations | 1 | 1 |
| TRI-HV1 recomputed = frozen | `9e18beb9…` yes, step-5 flips [58824, 58827, 58867], 0 crossings | `db0bbcdc…` yes, flips [57083], 0 crossings |
| Cuff canon / face topology = accepted | yes / yes | yes / yes |
| Second independent production write | geometry / face / branch map / TRI / landmarks identical (the blend file sha differs only by the save timestamp) | same |

## 4. Technical validation (both references)

| Gate | c1 | c2 |
|---|---|---|
| Validator D1 + D3 + D4 + D5 + D6 | **69 / 69**; 69 stations identical to the family; family = accepted | **69 / 69**; same |
| Integrity | 1 component; 0 boundary / non-manifold / degenerate; winding and normals OK | same |
| Density (all zones) | PASS; ear branch mean 0.101 % of stature | PASS |
| Face rings | mouth 36, orbits 43 / 43, 0 poles at mouth corners; = family | same |
| Anatomy (ear + HR2 zone excluded) | T1 / T2 / T3 / T7 PASS; IoU ≥ 0.9977; stature −0.43 mm | PASS |
| Ear root | valence 4 × 52 per side; root seam boundary 0; clearance min 0.165 cm; branch self-intersections 0 | same |
| Contact | pair set = family; classes 54 source / 4 family / 0 new; 0 on branch faces | 114 / 0 / 0 new |
| Ear (HE2) | T4 231 / 245; audit and measures = approved build; on TRI-HV1: 0 contacts / inversions / root inversions | same |
| Left / right | mirror max 0.503 cm = family; p99 0.058 | 0.376 cm = family; p99 0.053 |
| Stature / bbox | 178.008 / 177.965 cm | 177.988 / 177.988 cm |
| Export / reload | see §8 | see §8 |

**Unmasked `anatomy.py` T1 / T2 flag.** This flag also appears on the ear-excluded run. The cause is the frozen HR2 root zone: 214 (c1) / 220 (c2) head-skin vertices, all ≤ 0.47 cm from the branch, moved ≤ 0.80 / 0.85 cm. These vertices are part of the frozen HE2 V hash. With that zone excluded:
- every other vertex has dV = 0 against the family;
- T1 / T2 / T3 / T7 PASS.

Record: `HALVREN_FINAL_hr2_zone_localisation.json`. This is the same class as the frozen Vael unmasked-anatomy localisation.

**Expressions.** These are MPFB expression units, run with `cf_expr`. They show the same pattern as the frozen Vael final:
- blink lid-closure self-intersections: 126 / 148;
- surprise flips: 92.

This is a rig / expression-stage class, not a source defect. There is no HP-B accepted expression entry to diff against.

## 5. Approved-morphology regression

| Subsystem | Check | Result |
|---|---|---|
| Body (HB2) | `hv_eval` body rows = accepted `HPB_eval`. Material vs MF / SG / SK / FN / AE / VA: c1 10 / 13 / 22 / 17 / 13 / 13; c2 11 / 13 / 20 / 12 / 12 / 8. 7 groups with signal vs MF. Scalar-blend firewall best: c1 MF-AE R² 0.694; c2 SG-AE R² 0.733 (pass). Stature equal. | **no regression** |
| Face (HF2) | face rows = accepted. 3 regions depart from MF. Distinct from FN 6 / AE 5 / VA 3. Anti-beauty: jaw / bizyg −1.17 / −1.28 %, lower-face height +1.97 / +2.04 %. | **no regression** |
| Pelvis (HP-B) | skeletal proxy = accepted HP-B; lean r6 equal. Pelvic vertical / crest +3.29 / +3.21 % vs MF; crest share −2.54 / −2.43 %; AP depth share −1.53 / −1.61 %; leg share vs MF +0.34 %. | **no regression** |
| Ear (HE2 / HR2 / TRI-HV1) | V / Q / TRI hashes = freeze; firewall R² 0.51 / 0.44 / 0.23 unchanged (arrays identical); root seam and clearance as frozen; one-auricle read: the blind regression comparison found no new or worse item | **no regression** |
| Everything else | outside the frozen branch + HR2 zone, dV = 0 to the accepted family realization | exact |

Board C (`HVFINAL_C_regression_c1/c2.jpg`) shows accepted R-6 | accepted family | final, with a |final − family| heat map. Only the ring of the HR2 zone shows.

## 6. Whole-character identity (visible and hidden ears)

Reviewer: an independent blind agent that saw only the boards and the questions. Record: `halvren_rp3_final_whole/blind_identity_review.md`.

| # | Question | Verdict |
|---|---|---|
| 1 | One biologically coherent organism | **PASS** — smooth proportional transitions in all views; no patchwork |
| 2 | Not Marchfolk with pointed ears | **BORDERLINE** — with ears hidden it is the nearest figure to MF; narrower shoulders / waist and slimmer, longer-looking limbs; face almost the same |
| 3 | Not a reduced Fenn / Aelari / Vael | **PASS** — human-framed torso / chest / pelvis; MF-like brow and jaw mass; smaller, less flared ear |
| 4 | Not an arithmetic blend | **PASS (weak)** — a lopsided mosaic (limbs / waist ~20–30 % toward the elves; face / torso near-human), not halfway everywhere |
| 5 | Hidden ears keep the mixed anatomy | **BORDERLINE** — limb slenderness and narrower trunk visible side by side; craniofacial difference barely perceptible |
| 6 | Visible ear integrates, does not dominate | scale / position **good, does not dominate**; surface **FAIL** (concha / scapha relief, tragus / lobe nub, rear rim crumple / dark gap, lower-rear flap) |

**Follow-up regression check** (same reviewer, final ear vs the frozen-HE2 boards PT_B / HE2RV_D): every ear item was "PRESENT IN EARLIER BOARD (same)". Silhouette, size and position match.

**Measured hidden-ear record** (`hidden_ear/HV_hidden_ear_identity_final.json`). Ears are excluded at w_ears > 0.05 and all bodies are matched at 178 cm. The values equal the accepted source pass, because the inputs are dV 0. For example, c1 trunk:
- HV-MF 4.31 mm, against the human SG-MF baseline of 8.75;
- the arm is nearest AE;
- the hand is nearest AE / SG.

This is the accepted "mixed body + subtle face" result.

**Disposition:**
- Questions 1, 3 and 4 pass.
- Questions 2 and 5 are the accepted subtle source read (§7 of the order: not reopened).
- Q6's surface items are the frozen HE2's accepted residuals:
  - "cuff band crumple / back-sheet Z-kink, stamped interior relief, HR2 lobe-base crease";
  - the HE2 root-visual review notes.

Q6 is raised for **author attention**: the blind eye still calls the auricle surface unclean at head scale. Changing it would mean reopening the frozen ear, which is outside this order.

## 7. Deformation / contact

Standard v1, 18 poses, final / accepted family / MF v005 flipped faces, with the frozen Vael final shown for comparison.

| Pose | c1 | c2 |
|---|---|---|
| fist_l | 265 / 265 / 281 (VA 268) | 260 / 260 / 278 (VA 263) |
| knee_140_l | 76 / 76 / 76 (VA 77) | 84 / 84 / 90 (VA 84) |
| toe_ext30_l | 71 / 71 / 70 (VA 72) | 54 / 54 / 60 (VA 61) |
| hip_flex90_l | 57 / 57 / 56 (VA 56) | 40 / 40 / 40 (VA 40) |
| elbow_130_l | 53 / 53 / 54 (VA 54) | 43 / 43 / 45 (VA 45) |
| knee_90_l | 11 / 11 / 15 (VA 12) | 32 / 32 / 36 (VA 32) |
| neck_rot45 / neck_flex30 | 0 / 0 / 0 | 0 / 0 / 0 |

- **Flips and self-intersections:** final − family new flips and new self-intersections are 0 on every pose. New self-intersections vs R-6 are 1,406 / 1,410, equal to the family (MF 1,464 / 1,557). New folds equal the family.
- **Ear readiness:** the 8 head poses (neck flex / ext, yaw ±45, pitch, roll) are all zero.
- **Ear on TRI-HV1:** 0 contacts, inversions and root inversions.
- **Ear skinning:** the ear stays rigid to the head at final skinning, per the existing carry-forward. There is no new rig-stage issue.
- **Contact:** the set is identical to the family's, with no new pairs.

## 8. Export / read-back

| Check | Result |
|---|---|
| Local read-back of the blend | faces equal; V ≤ 6e-8 m; TRI attribute → triangles = frozen hash |
| Second independent write | geometry / face / branch map / TRI / landmarks identical |
| E: production copies (11 files) | byte-identical to the reviewed candidates (`readback/pc_readback.json`, `pc_readback_sha256.txt`) |
| Read-back integrity | OK |
| Validator from read-back geometry | 69 / 69 both. Loops, margins, sides and D5 / D6 identical. One fallback status label differs per configuration from float32 noise (c1 `toe3_j3_l`, c2 `shoulder_r`), the same kind recorded in the Aelari / Vael freezes |
| TRI-HV1 read-back from the E: blends | triangles = frozen hash (`readback/*_tri_readback.json`) |

## 9. Immutable references

- **Repository:** `immutable_hashes.txt`. The 14-file ear-family closure list, the HE2 V hashes, the ear-family freeze record and its baked TRI-HV1 data are all **UNCHANGED**.
- **Production folder read-back:** `HALVREN_FINAL_frozen_reference_readback.json`. These files match their freeze records, **29 / 29 UNCHANGED**:
  - Fenn / Aelari / Vael production blends, sidecars, branch maps and landmarks;
  - the Fenn / Aelari freeze copies;
  - the Marchfolk v005 M / F blends;
  - the v005 freeze record.

## 10. Carry-forwards

There are no new carry-forwards. These are unchanged:
- **HALVREN-CF-EAR-TRI-LOD-1:** baked TRI-HV1, imported normals / tangents, LOD-HV1, and a UE5 smoke test at first integration.
- **Ear rigid to the head at final skinning.**
- **MPFB expression-unit lid-closure intersections:** same class as the frozen races; expression / rig stage.

## 11. Boards (`halvren_rp3_final_whole/sheets/`)

- **A** `HVFINAL_A_whole_character.jpg` — c1 / c2: front, front 3/4, side, rear 3/4, rear.
- **B** lineups and heads:
  - `HVFINAL_B_lineup_c{1,2}_vis.jpg` — ears visible: production references uniformly scaled to 178 cm, each figure rotated in place for front / front 3/4 / side.
  - `HVFINAL_B_lineup_c{1,2}_hid.jpg` — ears hidden: R-6 at 178 cm, ear collapsed.
  - `HVFINAL_B_heads_c{1,2}.jpg` — heads.
  - Lineup order: Marchfolk | Halvren final | Fenn | Aelari | Vael.
- **C** `HVFINAL_C_regression_c{1,2}.jpg` — body / face / pelvis / ear root: accepted R-6 | accepted family | final + heat.
- **D** `HVFINAL_D_ear_integration.jpg` — HE2 c1 / c2: front 3/4, side, true rear 3/4, lower-rear 3/4 (grazing light).
- **E** `HVFINAL_E_deformation_c{1,2}.jpg` — the five worst poses + neck rot / flex, full body + joint / ear close-ups, captions final / family / MF.
- **Review crops:** `HVFINAL_review_ear_vs_frozen_PTB.png`, `HVFINAL_review_front_vs_HE2RV.png`.

## 12. Proposed freeze-by-record action (on author approval only)

1. Write `halvren_rp3_final_whole/HALVREN_RP3_FREEZE.json` from `HALVREN_RP3_FREEZE_CANDIDATE.json`, with the status "HALVREN RP3 WHOLE CHARACTER — AUTHOR ACCEPTED / FINAL PRODUCTION FROZEN" and the candidate hashes above. Copy it to `E:/…/production/Halvren/RP3/`.
2. Re-hash the 11 production files on E: against the record. Do not re-save any blend and make no geometry change. The record is authoritative over the embedded "CANDIDATE … NOT frozen" strings.
3. Update STATUS / handoff. Halvren joins the frozen RP3 races; HALVREN-CF-EAR-TRI-LOD-1 is unchanged in the register.

## 13. Not done

- No freeze.
- No UE5 work, creator work, clothing, hair or materials.
- No other race.
- No change to HB2 / HF2 / HP-B / HE2 / HR2.

**STOP FOR CHATGPT REVIEW.**
