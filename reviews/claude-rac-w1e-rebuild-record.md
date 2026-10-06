# RAC W1e — Rebuild record (FN, AE, VA, DU, GR, GO, PK) and diagnostic reruns

**Author:** Claude **Date:** October 5, 2026
**Order:** `reviews/chatgpt-rac-w1d-author-decisions-continuation-order.md` §9 items 4, 6, 7
**Evidence:** `reviews/rac-w1e-evidence/`. Every number quoted here is in `tables.md`. **ARM records:** `reviews/rac-w1e-arm/`

## 1. Method

**Regional non-uniform deformation (PV-D21 (c)).** A new tool step, `arm_lib.apply_bone_scales`, does the following:
- It scales selected deform bones in bone space (X lateral, Y along the bone, Z depth).
- Their children do not inherit the scale.
- The result is baked into the mesh before the R-6 pose.

What each bone controls:
- **Pelvis bone:** X spreads the hip joints, Y raises the iliac (vertical) region, Z deepens AP.
- **spine_01…03:** shape the lumbar and lower thorax.
- **Clavicle:** sets girdle breadth.

This moves joint positions and skin together. It is a **reference-construction** route, not a production algorithm. Configs are in `tools/rac/w1/cfg/w1e/`.

**All bone-scale magnitudes are BUILDER-CHOSEN (R-14).** They were found by trial against the accepted relations; they are **not** proven minima.
- After the W1e audit, two scales were tested for need. The VA pelvic depth increase was **removed** (see §2). The PK pelvic vertical scale was **kept**: without it PK leg share exceeds MF, which fails a directional check.
- A trial that raised the AE/VA leg targets was **rejected**. It demonstrated AE hip height > MF, but it broke the AE forearm and foot directions and VA depth.

**Routes:**
- **DU and PK** use the native short-adult route (`native_short.py`). For DU this is a builder choice needing acceptance (§5, BM-2). PV-D21 (c) names regional deformation for DU, and native short-adult only for PK. DU-NAT combines the native source (W1d finding: the minimum-height generator model is implausible) with a regional pelvic bone scale.
- **FN, AE, VA, GR and GO** use the native height solve, as in W1c.

**Validation limit (PV-D16, AD-G10).** All pelvic, girdle and ALPC checks here read **skin** stations or **generator joints**. These are composition-inclusive diagnostics, not the skeletal / bony-landmark validation that canon requires. In detail:
- The girdle readings use the generator shoulder joint, not anatomical acromial / glenohumeral landmarks.
- The waist interval (spine_01 → spine_03 joints) and thoracic vertical (suprasternal → spine_03) are joint-based. They therefore move **directly** with the spine Y scales: AE spine_01 +8 %, PK spine_01 −10 %, GO spine_03 +14 %. Those passes show the construction produced the relation; they are not independent evidence.
- S7 is a thigh skin section, but ALPC-3 excludes soft tissue, so S7 is not used for ALPC-3.

**The ordered AD-G14 rebuild (skeletal-trunk proxy + sculpted envelope for GR and GO) was not executed in this pass.** GR and GO were rebuilt on the skin / bone-scale route only.

## 2. What was changed and why

| Body | Change (exact values in `tables.md` §1) | Accepted relation it serves |
|---|---|---|
| FN | Pelvis X and Z +4 %; spine_01 X +3 % | E-A2 (bitrochanteric ÷ crest ≥ MF); PV-D3 (a) / PV-D4 (a) (depth and breadth ≈ MF) |
| AE | Pelvis Y +7 %, Z +6 %; spine_01 Y +8 %. Upper/lower-leg targets 0.15 → 0.25; forearm target 0.35 → 0.32 | PV-D5 (vertical elongation); E-A2; AE-P6 (longest waist interval) |
| VA | Pelvis X +2 % (**no depth increase**: PV-D6 (a) says not to author VA > MF without need). Lower-leg decrement 0.15 → 0.10 | PV-D6 (a) (VA depth > FN and AE, ≈ MF minimum); VA-P2a |
| GR | spine_01 X −4 %; clavicle length −2 % | GR-P6 (pelvis ÷ thorax breadth ≈ MF); GR-G1 / AD-G1 (girdle follows the thorax) |
| GO | Pelvis X +14 %, Z +15 %; spine_01…03 broadened and deepened; spine_03 length +14 %; clavicle −4 %. Torso-depth target 0.8 → 1.0 | PV-D14, ALPC-1/1b/2/4/7, AD-G6, AD-G7 (see §4) |
| DU | Native short-adult route; pelvis Y −10 % | PV-D8, PV-D9, DU-P3 (squat pelvis) |
| PK | Native short-adult route; pelvis Y +6 %; spine_01 Y −10 % | PV-D10, PK-P2a (leg share ≤ MF), PK-P3…P6 |

**Not rebuilt:** HV and CG-NAT. Their geometry hashes match W1c / W1d. They were re-measured with the new W1e readings, and every earlier value is unchanged.

## 3. Results

### Accepted pelvic / girdle / ALPC relations (`w1e_checks.json`)

**75 rows:**

| Result | Count | What it covers |
|---|---|---|
| PASS | 57 | — |
| NOT DEMONSTRATED | 3 | AE hip-joint height > MF; VA hip-joint height > MF; VA hip-joint height < AE |
| MARGINAL | 1 | VA AP depth ≥ MF minimum, −0.6 % |
| FAIL | 8 | All GO (§4) |
| NOT RUN | 5 | GO-P2a hip-joint scale; ALPC-3, ALPC-5, ALPC-6, ALPC-8 |
| REPORT | 1 | ALPC-1c |

The rule is AD-G10 / PV-D10:
- a strict direction must hold by ≥ 1 %;
- a non-strict direction that misses by < 1 % is MARGINAL, not a failure.

The '~' checks use the W1c absolute ±0.010 tolerance. On these shares that is a ±6–8 % band. That is wide, and it is disclosed in `tables.md` §3.

**The elven hip-height ordering is the open issue.** MF < VA < AE on hip-joint height ÷ stature currently sits inside two 1 % margins (MF 0.5321, VA 0.5334, AE 0.5343). Demonstrating it needs a longer-legged AE centre, which in turn moves the other AE limb directions. That is an author-level magnitude question (§5, BM-3).

### Cross-race directional checks (`directional_checks.json`)

**134 checks:** 126 PASS, **7 NOT DEMONSTRATED** (strict direction holding by < 1 %), 1 FAIL.
- **NOT DEMONSTRATED:** SK elbow and knee joint > MF, FN forearm share > MF, AE leg share > MF, AE foot share > MF, VA leg share < AE, GO thoracic breadth > SK.
- **FAIL:** the FN bony-orbit E-proxy. It remains a diagnostic (O-D4) until the O-1 rings are accepted.
- **HV source span:** 8 / 8, re-run against the rebuilt FN, AE and VA.

### Notable movements against W1c (`tables.md` §2)

**GO:**
- Leg share 0.5521 → 0.5363 and torso share 0.2773 → 0.2908. This is consistent with the lengthened spine_03 lowering the hip joint relative to stature.
- Thoracic depth ÷ breadth 0.7292 → 0.7940.

**DU** (native route):

| Reading | W1c | W1e |
|---|---|---|
| Leg share | 0.4866 | 0.5168 |
| Torso share | 0.3147 | 0.2965 |
| Shoulder-joint share | 0.2705 | 0.2393 |
| Thoracic breadth share | 0.2354 | 0.2215 |

These are identity-relevant and need author review (BM-1, BM-2).

### Visual check (PV-D17)

`side_lineup.jpg` and the per-candidate evidence sheets read as plausible adult bodies with no soft-tissue artefacts, except as noted for GO.

## 4. Gorrund — FAIL

Eight skin diagnostics fail:
- pelvic AP depth ÷ crest > MF;
- pelvic AP depth ÷ crest > SK (PV-D14);
- bitrochanteric ÷ crest ≈ MF (GO-P2b, |Δ| 0.023 > 0.010);
- pelvic vertical ÷ stature ≥ GR (GO-P3, −1.2 %);
- ALPC-1 lumbar depth;
- ALPC-2a pelvic AP ÷ thoracic depth;
- ALPC-7 S4 depth > SK;
- ALPC-7 pelvic depth ÷ thoracic depth > SK.

GO-P2a (hip-joint scale ÷ crest) and ALPC-3/5/6/8 are NOT RUN (no skeletal femur, frame bodies or silhouette test). ALPC-7 is compared with **central** Skarn, not the equal-height Broad Skarn the criterion names. AD-G6 (GO > GR shoulder-joint breadth ÷ stature) and AD-G7 pass.

**Skin-only trial.** Pelvis Z +65 % and thigh Z +14 % (`go_skin_trial_*`). It clears six of the eight failures, but ALPC-2a and GO-P2b still fail, and it produces a buttock/abdomen bulge (comparison sheet). The likely cause: the generator carries AP pelvic depth as soft tissue around a human pelvis, while the deeper thorax raises the comparison denominator. This is the case AD-G14 addresses, and AD-G14 was ordered but **not executed** here.

**Visual:** the trunk still reads as a large lean human rather than a structurally massive axial trunk.

## 5. Undetermined relationships and OPEN envelopes kept

- **GR vs MF shoulder breadth ÷ stature:** undetermined (AD-G4), not checked.
- **ALPC-1c:** report-only (AD-G9).
- **AD-R15:** covers only the SK–GR depth and SK–GO / SK–GR joint pairs (AD-G13).
- **All bone scales, ear centres and the ring increment:** W1 reference values, not envelopes (PV-D22, E-D2, O-D2).

— Claude
