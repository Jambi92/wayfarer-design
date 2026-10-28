# RAC RP3 — Vael final elf-frame correction + human-firewall gate

**Date:** 2026-10-28
**Order:** `reviews/chatgpt-rac-rp3-vael-elf-frame-human-firewall-order.md`
**Parent gate:** `reviews/claude-rac-rp3-vael-custom-body-deformation-gate.md` (842f33a)
**Evidence:** `reviews/rac-rp3-evidence/vael_rp3_elf_frame/` (22 sheets in `sheets/`)
**Ear proposal:** `reviews/claude-rac-rp3-vael-ear-branch-proposal.md`
**Tools:**
- `tools/rac/w1/vael_body_field.py`, which gains VEF1;
- `tools/rac/w1/arm_lib.py` (clavicle-span hook, inert without `vef`);
- `tools/rac/rp/vael_rp3_v001/`: `build_vf.sh`, `vf_eval.py`, `vf_comp.py`, `vf_ear_root.py`, `vf_sheets.py`, plus `va_manifest.py` (v004).

## RESULT — VAEL HUMAN FIREWALL PASS — VF2 RECOMMENDED — EAR PROTOTYPING UNLOCKED

One deformation note is disclosed in §7.

At equal height with ears hidden, VF2 no longer reads as a normal human-family body beside Marchfolk and Sagekin (sheets 04, 05, 21). The read comes from the combined system:
- a moderately narrower shoulder foundation;
- gracile limb shafts;
- the Vael deep torso (+5.5 / +6.6 % thorax depth);
- compact torso-to-pelvis continuity;
- stronger joint and extremity bases (palm root +10 / +9 %, heel +15 / +14 % vs MF);
- the VC2 face.

The distinction is modest, not dramatic. VF2 groups with the elf family and stays distinct from Fenn and Aelari (sheets 06, 21).

## 1. VEF1 — the elf-frame term

VEF1 is shared by c1 and c2, deterministic and versioned:

| Item | Value |
|---|---|
| Definition sha | b0bf94cf… |
| Module sha | 36b8e171… |
| Definition file | `VF_definitions.json` |
| Built on | VD2, with the VD field held at 1.0 |
| Height macro | held |

The term has three components, all scaled by `vef_magnitude` (VF1 0.6, VF2 1.0, VF3 1.4).

| Component | Mechanism | VF2 (c1 / c2) |
|---|---|---|
| **A — clavicle span** | Clavicle bone length (bone-space Y) × (1 − 0.04 × m), applied with the bone scales in `arm_lib.build`. Skeletal: the shoulder joint moves medially along the clavicle. | Clavicle factor 0.96; shoulder joint −0.66 cm per side |
| **A2 — axillary continuity** | The upper-thorax side wall below the axilla follows the shoulder joint's own medial shift (1.4 × shift). Gaussian in height at 0.55 of spine_03 → clavicle (σ 0.15), lateral / posterior azimuth only (> 75°). Keeps arm-to-trunk clearance. | max 0.73 / 0.67 cm |
| **B — shaft gracility** | Radial reduction toward each bone axis, strongest mid-shaft, smoothstep fades before each joint. Windows: upper arm 0.18–0.78, forearm 0.15–0.65, thigh 0.22–0.78, calf 0.15–0.70. Relative factors 1.0 / 0.8 / 1.0 / 0.8. | k = 4 %; realised sections in §3 |

- **Normalisation:** everything is a fraction of the body's own bone lengths and section radii, so c1 and c2 share one rule.
- **Determinism:** independent rebuild drift is 0 for VF1–VF3, rest and R-6. Regen is geometry-identical for the winner.

**Design iterations (disclosed):**

| Version | What happened | Change |
|---|---|---|
| v1 (A + B only) | New arm–trunk contact in R-6: c1 70 vs 56 pairs | Added A2 |
| A2 at azimuth > 55° | Moved the front shoulder | Restricted to > 75° |

## 2. Shoulder span (§11) — / stature, vs Marchfolk (c1 / c2)

| Population | Clavicle span | Shoulder-joint span | Bideltoid |
|---|---|---|---|
| VD2 | +0.04 / +0.10 % | +0.04 / +0.10 % | −0.05 / 0.00 % |
| **VF2** | **−3.47 / −3.32 %** | **−3.47 / −3.32 %** | **−2.78 / −2.59 %** |
| VF1 | −2.06 / −1.95 % | same | −1.69 / −1.56 % |
| VF3 | −4.87 / −4.68 % | same | −3.86 / −3.63 % |
| Sagekin | −0.57 / −0.63 % | same | −0.60 / −0.60 % |
| Frozen Fenn | −4.00 / −4.49 % | same | −6.12 / −4.04 % |
| Frozen Aelari | −4.99 / −6.00 % | same | −4.49 / −5.02 % |

- **VF2 ordering** on every span, both configurations: **MF > SG > Vael VF2 > Fenn / Aelari**.
- **VF3** is narrower than Fenn on clavicle and joint span in c1 (−4.87 vs −4.00 %). It breaks the ordering and drifts Fenn-like, which confirms VF2 is not under-powered.

## 3. Limb envelope and bases (§12)

**Mid-shaft section** (geometric mean of the principal extents, ±2.5 cm slab; c1 / c2):

| Shaft | VF2 vs VD2 | VF2 vs MF | Fenn vs MF | Aelari vs MF |
|---|---|---|---|---|
| Upper arm | −3.3 / −3.4 % | −2.8 / −3.0 % | −6.5 / −7.1 % | −3.5 / −4.3 % |
| Forearm | −2.3 / −2.2 % | −0.7 / −2.1 % | −5.2 / −7.0 % | −3.0 / −5.3 % |
| Thigh | −3.4 / −3.4 % | −3.4 / −3.3 % | −7.8 / −5.6 % | −4.4 / −4.1 % |
| Calf | −2.5 / −2.5 % | −2.4 / −2.4 % | −5.2 / −4.9 % | −3.5 / −3.0 % |

**Bases, VF2 vs MF.** Bases are kept: the shaft fields end before the joint stations.

| Base | VF2 | Fenn | Aelari |
|---|---|---|---|
| Elbow / stature | −0.3 / −0.1 % | −5.3 / −5.7 % | −2.0 / −4.0 % |
| Knee / stature | −0.5 / −0.4 % | −7.9 / −12.1 % | −4.9 / −8.3 % |
| Ankle / stature | +0.5 / +0.3 % | | |
| Wrist / forearm | −2.9 / −2.0 % (still > Fenn and Aelari) | | |
| Palm / hand | +1.8 / +1.9 % | | |
| Palm root / wrist | +10.2 / +8.7 % | | |
| Heel / foot length | +15.0 / +13.5 % | | |
| Foot breadth / length | +7.9 / +6.9 % | | |

- Canon holds 20 / 20 on both configurations: elbow, wrist, knee and ankle presence > Fenn and Aelari; joint mean gracile vs MF.
- **Read:** slimmer shafts with comparatively stronger joint, hand and foot bases (sheets 09–12).

## 4. Human firewall (§9) and three-elf firewall (§10)

**Human firewall: PASS (visual).**
- Front and three-quarter: narrower shoulder foundation, slimmer arms and legs, and an upper-thorax side wall that reads continuous (sheets 04, 05, 15 overlays). With the deep profile torso (sheet 03) and the VC2 face, VF2 is clearly not another Marchfolk / Sagekin variant at whole-character scale.
- The read is not dramatic. VF2 is still the most structurally present of the three elves.
- Body systems material vs humans rise to 5 / 8 on both configurations (from 4 / 8).

**Three-elf firewall: PASS (sheets 06, 21).**
- **Fenn:** narrower and lighter joints, more extremity-led, shallower torso (Vael thorax depth +11 / +13 % vs Fenn).
- **Aelari:** more vertical, more gracile joints, longer vertical continuity.
- **Vael:**
  - moderately gracile shafts (between MF and Aelari);
  - deeper torso;
  - compact continuity;
  - stronger bases;
  - shoulder foundation between humans and the other elves;
  - VC2 face.
- Not too narrow, frail, or Fenn / Aelari-like. Shaft reduction stays below Aelari's on every segment. Only VF3 crosses Fenn on joint span.

## 5. Torso, pelvis and integrity

**Torso** (§15, sheet 13; VF2 vs MF):

| Measure | c1 | c2 |
|---|---|---|
| Thorax max breadth | −3.2 % | −3.25 % (axillary continuity) |
| Waist | −1.8 % | −2.4 % (unchanged from VD2) |
| Crest | −0.5 % | −1.1 % (unchanged) |
| Thorax depth | +5.5 % | +6.6 % |

No waist pinch (the GX c2 outcome does not recur), no barrel chest, no lost depth or continuity, and no shoulder / trunk discontinuity.

**Pelvis** (§14, skeletal proxy, all t): **9 / 9 for VF1, VF2 and VF3, both configurations.**

| Rule | c1 | c2 |
|---|---|---|
| MF < Vael < Aelari < Fenn | +0.10 / −0.11 / −2.37 % | +0.055 / −0.29 / −2.44 % (identical to VD2) |
| VA-P6 | −1.56 % | −0.29 % |
| VA-P2b | +0.95 % | +1.49 % |
| VA-P3 vertical | −6.5 % | −5.9 % |
| VA-P4 | holds | holds |

**Source integrity** (§16): 1 component, no boundary, non-manifold or degenerate faces, normals outward.

| | c1 | c2 |
|---|---|---|
| Self-intersection pairs, R-6 source (VD2 → VF2) | 56 → 50 | 86 → 82 |

New pairs are churn within the existing arm–trunk contact patch. Totals fall for every candidate.

**VF2 displacement vs VD2** (c1 / c2; per-region max in cm):

| | c1 | c2 |
|---|---|---|
| Vertices moved | 7,116 | 7,111 |
| Max displacement | 0.76 cm | 0.67 cm |
| RMS displacement | 0.58 cm | 0.50 cm |
| Clavicle / shoulder | 0.69 | 0.61 |
| Upper arm | 0.76 | 0.67 |
| Forearm | 0.74 | 0.64 |
| Thigh | 0.39 | 0.39 |
| Calf | 0.20 | 0.21 |
| Trunk | 0.73 | 0.67 |
| Hand / foot | 0.67 | 0.58 (the whole arm translates medially with the shoulder joint) |
| Head / neck | 0.24 | 0.20 (neck-base seam only) |
| Ears | 0 | 0 |

## 6. Composition firewall (§13)

**Why VEF1 is skeletal / structural by construction:**
- Component A is a bone length.
- A2 and B are fractions of the body's own section radii about its own bone axes.
- None reads or writes the muscle, weight or frame macros.
- The skeletal-envelope (lean) builds receive the same term, so the pelvis proxy sees it.

**Diagnostic** (`VF_composition_diagnostic.json`, sheet 22): VD2 and VF2 rebuilt with the skeleton held at three compositions. VF2 vs VD2 changes:

| Configuration | Composition | Clavicle span | Upper arm | Forearm | Thigh | Calf |
|---|---|---|---|---|---|---|
| c1 | narrow / low muscle (0 / 0) | −3.51 % | −3.36 % | −2.30 % | −3.41 % | −2.49 % |
| c1 | balanced | −3.51 % | −3.30 % | −2.30 % | −3.43 % | −2.47 % |
| c1 | broad / high muscle (1.0 / 0.5) | −3.51 % | −3.43 % | −2.36 % | −3.43 % | −2.31 % |
| c2 | all three | −3.41 to −3.42 % | −3.25 to −3.36 % | −2.20 to −2.34 % | −3.42 to −3.49 % | −2.54 to −2.67 % |

The relative change is the same across compositions (within 0.2 points), while the absolute composition differences are preserved. The upper-arm section in c1 is 6.4 / 9.5 / 9.8 cm across the three states. This is not a thinness preset.

## 7. Family propagation, deformation, VC2, expressions

**Propagation:** `VA_{M,F}_REF_RP3_bodyfam_v004` (sha 3cf114dd… / f650ca75…), sources `VAL4-R1-VD2-VF2` / `VALF178-R1-VD2-VF2` (CANDIDATE).
- 57,842 V / 57,840 Q.
- Face hash, map and UV identical; |V − M·hm08| = 0.
- 69 / 69 D1–D6 on both.
- T-1 / T-2 / T-3 / T-7 pass.
- Density 9 / 9.
- Face rings: mouth 37 / 33, orbit 43 / 43, unchanged.
- Contact: 0 new (c1: 58 source + 2 family, vs VD2 68 + 2; c2: 110, vs VD2 114).
- E: read-back is byte-identical.

**Deformation** (sheet 19):

| Pose | c1 flipped faces (MF v005) | c2 flipped faces (MF v005) |
|---|---|---|
| Shoulder abduction 90° | 25 (25) | 19 (19) |
| Shoulder abduction 45° | 10 (7) | 17 (16) |
| Elbow, wrist, hip, knee, ankle | ≤ MF + 3 | ≤ MF + 3 |

No arm-raise collapse, no shoulder inversion, no arm / trunk collision, no unstable joints.

**DEFORMATION NOTE:** c1 `shoulder_flex90` has 19 flipped faces vs MF 13. That is +6, one face over the family "+5" flag; VD2 was 16.
- The 3 extra faces sit on the front of the shoulder.
- Ablation (`deform_ablation/VF_shoulder_flex_ablation.json`) leaves the count at 19 with:
  - A2 off;
  - shaft gracility off;
  - a 12 % smaller clavicle term;
  - a later upper-arm window.
- So the faces come from the clavicle-length scale route itself (carried MPFB weights / plain LBS), not from source geometry. Native source flips are 5 vs 4.
- c2 is fine (+2).
- **Classification:** rig / weight level, for the rigging stage (shoulder corrective). Not a reason to reopen the anatomy.

**VC2:**
- Non-ear head max |dV| is 0.0009 cm (geometry unchanged).
- Face systems 6 / 6; elf rows 9 / 9.
- Whole-face departure 1.138 / 1.128 mm (= VD2).
- Brow −1.30 / −2.66 % (= VD2).
- Jaw +0.42 / +0.71 % (VD2 +0.43 / +0.72; no jaw inflation).
- Hidden-ear identity unchanged.

**Expressions:** identical to VD2 for every unit.

## 8. Answers

1. **Is VC2 unchanged?** Yes.
2. **Is VD2 retained?** Yes. The VD field stays at 1.0; VEF1 is added on top.
3. **Which VF candidate is recommended?** **VF2.** VF1 sits only about 1.6 % below MF on bideltoid; VF3 crosses Fenn on joint span.
4. **What is the final shoulder-span ordering?** MF > SG > Vael VF2 > Fenn / Aelari, on clavicle, joint and bideltoid span, both configurations.
5. **How much did the upper-arm / forearm / thigh / calf envelopes change?** Mid-shaft sections vs VD2: −3.3 / −2.3 / −3.4 / −2.5 % (c1), −3.4 / −2.2 / −3.4 / −2.5 % (c2).
6. **Did Vael's stronger joint and extremity bases remain?** Yes: canon 20 / 20, palm root +10 / +9 %, heel +15 / +14 % vs MF.
7. **Does the full-body front / 3-4 human firewall finally pass?** **Yes**, modestly and clearly.
8. **Does the three-elf firewall remain pass?** Yes.
9. **Did any candidate become too narrow, frail or Fenn / Aelari-like?** VF3 only, on joint span. VF2 does not.
10. **Is waist / ribcage integrity preserved?** Yes: no pinch, depth unchanged.
11. **Does pelvis remain 9 / 9?** Yes, for all candidates.
12. **Did family topology remain unchanged?** Yes.
13. **Are both propagated bodies 69 / 69 D1–D6?** Yes.
14. **Did deformation remain acceptable?** Yes, with the one disclosed note: c1 `shoulder_flex90` is +6 vs MF, from the rig / weight route, for the rigging stage.
15. **Is Vael ready for ear prototyping?** **Yes.** The proposal is ready (`claude-rac-rp3-vael-ear-branch-proposal.md`):
    - reuse the Fenn-v002 engineering topology;
    - the root interface fits;
    - VA-E1 / E2 / E3 parameters are set out.

    No ear geometry was built.

## 9. Delivered / unchanged

- **Repository:**
  - `reviews/reference-assets/{r6,builds}/VAL4-R1-VD2-VF2*`, `VALF178-R1-VD2-VF2*` (CANDIDATE);
  - evidence: definitions, overrides, determinism, eval, pelvis, self-intersection, composition, hidden-ear, face regression, expressions, deformation ablation, ear root interface, family audit / validator / contact / deformation / regen, build records, 22 sheets.
- **E:** `production/Vael/RP3/`:
  - `VA_{M,F}_REF_RP3_bodyfam_v004.{blend,json}`, `_landmarks`, `_hm08_map`;
  - `VAEL_RP3_bodyfam_v004_propagation_manifest.json`;
  - source sidecars and `VAEL_VEF1_definitions_v004.json`.
  - Read-back is byte-identical (`pc_readback_sha256.txt`).
- **Unchanged** (`immutable_hashes.txt`, 24 / 24 equal to the previous gate): v005, Fenn, Aelari, VAL4 / VALF178, R1, VD2 sources, Fenn ear topology.
- **Not done, per the stop rules:** no freeze, no final ears, no Halvren, no creator morphs, no rig / UV / LOD / UE5 work. VC2 untouched.

**STOP FOR CHATGPT REVIEW.**
