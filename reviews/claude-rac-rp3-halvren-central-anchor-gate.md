# RAC RP3 — Halvren central mixed-expression anchor + hidden-ear mixed-ancestry gate

Order: `reviews/chatgpt-rac-rp3-halvren-central-anchor-order.md` (91a1e33, 2026-10-29).
Evidence: `reviews/rac-rp3-evidence/halvren_rp3_central_anchor/` (15 sheets `HV_01..12`).
Tools: `tools/rac/rp/halvren_rp3_v001/`. Workspace: `/tmp/claude-0/rt/hv`.

## RESULT

## HALVREN BODY SOURCE WORK REQUIRED
## HALVREN CRANIOFACIAL SOURCE WORK REQUIRED
## HALVREN PELVIS NEEDS AUTHOR DESIGN PASS

The technical side passes:
- the new c2 central anchor `HVF178` is valid;
- both v005 family candidates are 69 / 69 D1–D6 and technically clean.

The biology does not pass. At 178 cm, with ears hidden and pigment neutralized, the current central anchor (HVC1 and its c2 counterpart) is **effectively a Marchfolk body with slightly longer forearm / lower leg / fingers and slimmer wrist / ankle, and an unchanged Marchfolk face and pelvis**.
- It is not an arithmetic average.
- It is not a patchwork.
- It sits at the human end of every human / elf pair: the order's "unchanged source-race body with the Halvren label" failure.

**Ear work was not unlocked (§18). No ear geometry was built.** Nothing is frozen.

## Answers (§27)

| Question | Answer |
|---|---|
| Valid ~178 cm c2 central anchor created? | **Yes.** `HVF178` (178.01 cm): MF-F-R route + exactly the HVC1 body targets, stature re-solved. |
| c1 / c2 express one shared central design? | **Yes.** The cfg is identical to HVC1 except gender. 31 / 31 metrics follow the human-family c1→c2 pattern (same sign, inside the MF / SG spread). The Halvren−Marchfolk offset is near-identical in both configurations. |
| Both family candidates 69 / 69 D1–D6? | **Yes**, 69 / 69 and 69 / 69. |
| Central body a coherent mixed realization? | **No.** It is coherent, but it is human-family anatomy. Its departures from Marchfolk are inside human variation in every body region except the c1 neck. |
| Avoids mechanical arithmetic averaging? | **Yes.** It is not a scalar blend (blend fit R² ≤ 0.52, midpoint-zone metrics 0–2 per pair). It sits at the human end, not the middle. |
| Avoids exact whole-body duplication of a source? | **No, effectively.** Against Marchfolk only 2 of 31 metrics differ materially (both lower-leg share), and region RMS is below the Sagekin–Marchfolk baseline. |
| Pelvis coherent or author design pass? | **Author design pass.** The pelvis is stock Marchfolk: every pelvic relation is within ±0.7 % of MF, and HVC1 carries no pelvis term. |
| Hidden-ear / neutral-pigment central face passes? | **No.** The face *is* the Marchfolk face (aligned RMS ≤ 0.01 mm in all 7 regions). |
| Craniofacial source authoring required? | **Yes.** A bounded mixed craniofacial candidate pass is recommended. |
| Ear work unlocked? | **No.** |
| Best ear topology architecture (HT1 / HT2 / HT3)? | Not tested (locked). |
| Recommended ear candidate? | None (locked). |
| Ear reads as coherent mixed anatomy? | Not built. |
| Race-specific non-ear topology branch required? | **No.** v005 carries the anchor cleanly (exact topology, V = M @ hm08, 0 new contact class). The failure is in the source, not the topology. |
| Next author decision? | See §8. |

## 1. Part A — c2 central anchor `HVF178`

**Construction** (`build_hv_partA.sh`):
- `build_variant.py` with base `MF-F-R_build.json` (the accepted shared human-family c2 route, as SGF178 / VALF178).
- Overrides are **exactly the HVC1 body targets**:
  - nape-to-waist −0.10;
  - lower-arm length +0.12;
  - lower-leg height +0.12;
  - torso depth −0.05;
  - finger length +0.12;
  - wrist −0.15;
  - ankle −0.10.
- Stature 178 with `resolve_stature`.
- There is no c2-specific package and no sex-specific Halvren rule. The cfg differs from HVC1 only in `gender` and `id`.
- No earlier Halvren c2 record existed.

| Check | Result |
|---|---|
| Height | macro 0.6375, solve reachable in 12 iterations, stature 178.011 cm (inside 152–213; HV152N-NAT 152.0 / HV213M 213.0) |
| Determinism | independent second full re-solve: same macro, max \|dV\| 0, faces identical |
| HVC1 record rebuild | max \|dV\| 0, faces identical |
| Regeneration | regen.py geometry identical (dV 0) for HVC1 and HVF178 |
| Native hm08 integrity | 13,380 V / 13,378 Q, 1 component; 0 boundary / non-manifold / orientation / degenerate / coincident |
| Configuration consistency | 31 / 31 metrics carry the human-family c1→c2 difference (same sign as MF and inside the MF / SG spread); shared MPFB configuration differences are kept |

Committed:
- `reviews/reference-assets/r6/HVF178_r6.npz` (`c0e57bae…`), `builds/HVF178_build.json` (`bc61f4e7…`), `HVF178_meas.json`;
- sidecar `HVF178_central_anchor_sidecar.json`.

## 2. Part B — v005 family candidates — technical PASS

`HV_M_REF_RP3_bodyfam_v001` (HVC1) and `HV_F_REF_RP3_bodyfam_v001` (HVF178). The Standard v1 pipeline is `run_aeeval.sh` with `AE_WORK=…/hv`.

| Gate | c1 | c2 |
|---|---|---|
| Topology | exact v005 (57,842 V / 57,840 Q, 100 % quads); face hash, faces, UV and map identical; V = M @ hm08 max 0 | same |
| Integrity | 1 component; 0 boundary / non-manifold edges / non-manifold vertices / degenerate / coincident; winding consistent; normals outward | same |
| Validator D1–D6 | **69 / 69** | **69 / 69** |
| Anatomy T-1 / T-2 / T-3 / T-7 | pass; IoU min 0.9975; stature −0.42 mm | pass; 0.9977; 0.00 mm |
| Density | 9 / 9 zones pass | 9 / 9 zones pass |
| Contact | source 70, family 0, **new 0** | source 118, family 0, **new 0** |
| Face / UFCA | 32 mouth rings, 43 / 43 orbit rings, 0 poles at mouth corners, 0 within 2 cm of the mouth | 33 mouth rings, otherwise the same |

**Standard v1 deformation, flips:** the worst excess over Marchfolk v005 is +2 (c1) and 0 (c2). No pose is more than +5.

**Standard v1 deformation, contacts:**
- c1 thumb opposition: 42 vs Marchfolk 24.
- c2 knee 90°: 108 vs 87.
- Both are already on the native source (19 vs Marchfolk native 12; 28 vs 22). This is source anatomy (finger / lower-leg length), not topology.

PC copies are in `E:/…/production/Halvren/RP3/` (blends, hm08 maps, sidecars, landmarks, manifest, HVF178 sidecar). They read back byte-identical (`pc_readback_sha256.txt`).

The family human auricle is non-final Halvren ear anatomy. A technical PASS does not approve Halvren biology.

## 3. Part C — matched-height body gate (178 cm, ears hidden, geometry only)

**Comparators (`HV_partA.json`, `HV_hidden_ear_identity.json`):**
- Marchfolk, Sagekin;
- frozen Fenn (FNL4-CF2 / FNF181-CF2 records), frozen Aelari (AEL1-R1 / AELF190-R1), frozen Vael (VAL4-R1-VD2-VF2 / VALF178-R1-VD2-VF2);
- Skarn: SK / SKF208 re-solved to 178 cm. This is **diagnostic only**, below the 183–229 cm Skarn envelope.

The metric groups are:
- torso;
- shoulder / clavicle;
- arm;
- leg;
- joint scale;
- hand;
- foot;
- head / neck;
- pelvis (skin).

That is 31 metrics. "Material" means |diff| ≥ 1 % and more than 2× the human baseline |SG − MF|.

**Source-population protection** (metrics that differ materially from each source):

| | MF | SG | SK | FN | AE | VA |
|---|---|---|---|---|---|---|
| c1 | **2** | 3 | 26 | 14 | 18 | 10 |
| c2 | **2** | 2 | 24 | 11 | 12 | 8 |

**Nearest source per metric:**
- c1: MF 12, SG 7, VA 7, AE 4, FN 1.
- c2: MF 14, VA 6, AE 5, SG 3, SK 2, FN 1.

The only material Marchfolk difference is lower-leg share (shin / thigh +2.6 %, shin / leg +1.3 %). Halvren − Marchfolk:
- **Torso:** torso share −1.0 %, thorax depth −0.7 / −0.8 %, thoracic vertical −1.3 / −1.4 %.
- **Shoulders:** shoulder-joint −0.1 / −0.2 %.
- **Arms:** forearm / upper arm +3.1 / +3.3 %.
- **Joints:** wrist / forearm −4.2 / −4.5 %, ankle / shin −3.0 / −3.8 %.
- **Hands:** finger / hand +2.7 / +2.9 %.

All of these sit inside the human baseline.

**Hidden-ear region RMS, Halvren vs Marchfolk (with the Sagekin–Marchfolk human baseline):**

| Region | c1 | c2 |
|---|---|---|
| Trunk | 3.0 (8.8) mm | 4.6 (8.9) mm |
| Arm | 3.3 (4.3) | 2.5 (4.4) |
| Hand | 8.4 (11.2) | 6.8 (10.9) |
| Leg | 5.6 (7.6) | 6.7 (7.7) |
| Foot | 0.7 (1.4) | 0.5 (1.3) |
| Neck | 2.2 (1.5), the only region above the baseline | 0.7 (1.8) |

By comparison, against the elves the trunk is 6.6–14.0 mm and the leg 4.0–19.7 mm.

**Coherence questions (§10):**
- **Axial skeleton:** no mixed torso / ribcage relationship. It is the Marchfolk torso (thorax breadth −0.1 %, depth −0.7 %) with a slightly shorter nape-to-waist.
- **Appendicular skeleton:** the Marchfolk shoulder and pelvis frame. Only the forearm and lower-leg shares move (Fenn-type tendencies: lower-leg, arm share and wrist sit about 0.26–0.38 of the way from Marchfolk toward Fenn).
- **Distal anatomy:** the hands and feet are not grafted. The wrist and ankle slimming follows the longer forearm and lower leg, so they are coherent. But the foot base is the Marchfolk foot: breadth / length +0.2 %, against Fenn +13 % and Vael −7 %.
- **Structural presence:** it is human-family structural presence with slight distal gracility. It is not a mixed space.
- **Source protection:** it is not an exact copy, but it is systematically Marchfolk at whole-body scale.

## 4. "Not an arithmetic average" audit — PASS (not an average)

`HV_06`: for each pair, take the metrics with a material gap and compute t = (HV − human) / (elf − human).

| Pair | c1: t median / scalar blend α / R² / metrics in 0.35–0.65 | c2 |
|---|---|---|
| MF ↔ FN | 0.06 / 0.14 / 0.28 / 2 | 0.17 / 0.17 / 0.52 / 1 |
| MF ↔ AE | 0.02 / 0.08 / 0.21 / 2 | 0.03 / 0.07 / 0.12 / 2 |
| MF ↔ VA | 0.03 / 0.02 / 0.01 / 0 | 0.05 / 0.08 / 0.09 / 0 |
| SG ↔ FN | −0.02 / 0.02 / 0.01 / 0 | 0.07 / 0.08 / 0.32 / 1 |

The SK ↔ VA pair gives t ≈ 1 (α 0.97–1.00). That only says Halvren is far from the 178 cm Skarn diagnostic, which sits outside its envelope.

The whole system is **not** a mechanical average. The problem is the opposite: almost every relationship sits at the human end.

## 5. Part D — pelvis report (REPORT ONLY; no canon applied)

Skeletal proxy at t = 0 / 0.5 / 1.0 (`HV_07`, `HV_07b`, `HV_partA.json → pelvis_report`). Halvren vs Marchfolk at t = 0.5:

| Measure | c1 | c2 |
|---|---|---|
| Hip-joint height / stature | +0.66 % | +0.70 % |
| Bitrochanteric / crest | +0.00 % | −0.01 % |
| Pelvic vertical / stature | −0.30 % | −0.21 % |
| AP depth / stature | −0.32 % | −0.30 % |
| Waist / torso | −0.07 % | +0.10 % |
| Hip-joint scale proxy | −0.33 % | (c2: +0.5 % vs SG; the MFF178 proxy reading is an outlier, +24.7 %) |

Against the elves, pelvic vertical / crest is −9.8 % vs Aelari and the crest is −1.1 to +7.5 %.

**Classification: suspiciously stock human.** The pelvis is the Marchfolk construction (HVC1 has no pelvic term) with the leg-length change only. Halvren pelvic inheritance is OPEN in canon (HALVREN_V1 Part 2 §15–19), so no numeric rule is proposed.

**HALVREN PELVIS NEEDS AUTHOR DESIGN PASS.**

## 6. Part E — hidden-ear neutral-pigment face — SOURCE WORK REQUIRED

Ears collapsed, geometry only, similarity alignment onto the Halvren head (`HV_08`, `HV_09a`, `HV_09b`). Aligned RMS (mm), Halvren vs each source:

| Region | MF | SG | SK | FN | AE | VA | SG–MF baseline |
|---|---|---|---|---|---|---|---|
| Cranium | 0.01 | 0.01 | 0.12 | 4.36 | 4.06 | 1.67 | 0.03 |
| Forehead | 0.01 | 0.01 | 0.06 | 2.79 | 2.66 | 0.57 | 0.01 |
| Orbit | 0.00 | 0.00 | 0.04 | 1.70 | 1.68 | 0.50 | 0.01 |
| Nose | 0.01 | 0.01 | 0.04 | 0.75 | 1.13 | 0.26 | 0.01 |
| Cheeks / midface | 0.01 | 0.01 | 0.07 | 2.21 | 1.54 | 2.72 | 0.02 |
| Mouth | 0.01 | 0.01 | 0.09 | 1.30 | 0.99 | 0.26 | 0.01 |
| Jaw / chin | 0.01 | 0.01 | 0.50 | 2.20 | 4.23 | 1.40 | 0.02 |

(c1 shown; c2 is the same within 0.1 mm.)

- 0 / 7 regions and 0 / 15 descriptors depart from Marchfolk.
- The HVC1 record removes the only face target the HV design had (`eye-scale`), so the face is the MPFB human base face shared by Marchfolk and Sagekin.
- It reads as "a human face, ear difference only", which is the order §16 failure.

No anti-beauty fix was attempted (§17).

## 7. Ears — locked

The §18 unlock condition is not met (body and face both fail). HT1 / HT2 / HT3 and HV-E1 / E2 / E3 were **not** built. The HV-mixed W1 ear evidence stays a starting reference for later.

## 8. Next author decisions

1. **Accept `HVF178`** as the Halvren c2 central-anchor foundation (same design as HVC1 on the shared c2 route).
2. **Authorize a bounded mixed body source pass:** three candidates of increasing strength, built on both configurations.
   - **It sets coordinated relationships, not one slider:**
     - an axial term (thoracic depth / vertical relationship moving off Marchfolk without copying any elf);
     - shoulder / clavicle;
     - segment shares, with joints coupled to their long bones;
     - hand and foot base.
   - **Guards:**
     - not a scalar blend toward any elf;
     - not duplicating any frozen elf;
     - the composition stays independent.
   - **Gate:** the same matched-height metrics and midpoint audit (§3–4).
3. **Pelvis design pass:** the author states the intended central Halvren pelvic relationship. It could stay human-family-default, take a mild elven vertical / crest relationship, or a third option. No numeric pelvic rule should be authored before that.
4. **Bounded mixed craniofacial candidate pass:**
   - regional and coupled: cranium, brow / orbit, midface / cheek, nose, jaw / chin, lower face;
   - within the human ↔ elven family gap measured in §6;
   - no beauty filter;
   - the same hidden-ear gate.
5. **Ears stay locked** until body and face pass.

## Not done (stop rules)

None of the following were done:
- no Halvren freeze;
- no change to frozen Fenn / Aelari / Vael, the human references or v005;
- no genealogy / randomization system and no "Elf Percentage" control;
- no pelvis canon;
- no creator morphs, rigging, UV, LODs or UE5.

**STOP FOR CHATGPT REVIEW.**
