# RAC RP3 — Fenn configuration-2 central reference + hidden-ear body propagation + ear branch — gate

**Date:** 2026-10-27
**Order:** `reviews/chatgpt-rac-rp3-fenn-body-and-ear-branch-order.md` (57dc328)
**Evidence:** `reviews/rac-rp3-evidence/fenn_rp3_v001/`
**Tools:** `tools/rac/rp/fenn_rp3_v001/`, plus the Standard v1 pipeline.

## Results

| Part | Result |
|---|---|
| Part A | **FENN C2 CENTRAL REFERENCE PASS — READY FOR BODY PROPAGATION.** FNF181, 180.99 cm. One flag for the author: the skeletal-proxy E-A2 pelvis ratio is a tie below method resolution (§A4). |
| Part B, technical | Both body-family candidates pass Standard v1 on the unchanged v005 topology: **69 / 69 (D1–D6)**, anatomy, density, face rings, contact (documented source contact only) and deformation. |
| Part B, hidden-ear **body** identity | **PASS.** |
| Part B, hidden-ear **facial** identity | **NOT MET** beyond the orbit / eye region. |

**Overall result (§16): FENN BODY NEEDS RACE-SPECIFIC BRANCH.** It applies to the **head / face only** (zones: cranium vault, forehead-to-cranium transition, cheeks / mid-face, jaw / chin).

**What kind of branch is needed.**
- The evidence points to **craniofacial source authoring** (geometry), not a topology change.
- The active family topology reproduces the accepted Fenn head to p95 0.08–0.09 mm. It already carries a race identity face (Skarn C1R).
- What is missing is Fenn craniofacial anatomy in the **source itself**. The accepted FNL4 head is the MPFB human head scaled −1.2 %, plus the eye-scale / eye-height targets.

**Part C was not started**, per the §8 stop rule: "If this gate fails: STOP before Part C … Do not use ear exaggeration to hide a failed body foundation."

Nothing was frozen. The active MPFB family base is untouched.

---

# PART A — FNF181 configuration-2 central reference

## A1. Construction and provenance

There was no existing Fenn configuration-2 build: every Fenn build is gender 1.0 (FNL4, FN157-NAT, FN211).

FNF181 was built on the accepted human-family configuration-2 route, the same route as SGF178 / SKF208:
- **Builder:** `tools/rac/w1/build_variant.py`.
- **Base:** `MF-F-R_build.json`.
- **Overrides:** exactly the FNL4 targets (17) and bone scales (pelvis 1.04, spine_01 1.03, upper / lower arm 0.95 radial, thigh / calf 0.96 radial), plus stature 181 with `resolve_stature`.

**The resulting cfg equals FNL4's in every key except `gender` (0.0) and `id`.**
- No target was diluted.
- No sex-specific Fenn target or bone scale was authored, so there is no pelvic-width shift of Fenn's own. The configuration-2 difference comes only from the shared MPFB configuration architecture (the same gender macro as accepted MF-F-R).

| | |
|---|---|
| MPFB / Blender | 2.0.17 / 5.2.2 LTS |
| Height macro | **0.63916015625** (re-solved, 11 iterations) |
| R-6 stature | **180.9921 cm** |
| Pose | `pose_r6`, arm abduction 8°, then ground |

Files:
- `reviews/reference-assets/r6/FNF181_r6.npz`, sha `05c41aa0…`;
- `builds/FNF181_build.json`, sha `80948a51…`;
- `builds/FNF181_meas.json`;
- manifest entry "configuration-2 central reference CANDIDATE (pending author acceptance)";
- sidecar `FNF181_central_reference_sidecar.json`.

## A2. Determinism and integrity

**Rebuild identity.**
- `regen.py` from the record: geometry-identical, max \|dV\| 0.
- A second full height re-solve: identical, max \|dV\| 0, same macro.
- The FNL4 source also regenerates identically (`9c37d16a…`).

**Native hm08 body integrity:**

| | FNF181 | FNL4 |
|---|---|---|
| V / Q | 13,380 / 13,378 | 13,380 / 13,378 |
| Components | 1 | 1 |
| Boundary / non-manifold edges | 0 / 0 | 0 / 0 |
| Orientation-inconsistent edges | 0 | 0 |
| Degenerate faces / coincident vertices | 0 / 0 | 0 / 0 |
| Volume | outward (−57.9 L) | outward (−62.5 L) |

## A3. Fenn body identity at matched stature (both configurations)

**Diagnostic comparators** (not reference assets) are the accepted MF-M-R / MF-F-R / SG / SGF178 builds with stature re-solved to 181 cm: MFM181, MFF181, SGM181, SGF181.

**Measurement.** `run_candidate.py` with the common MF-M-R eye reference. It reproduces the committed `FNL4_meas.json` exactly (2e-16).

**Canon directions** (`FENN_V1` v1.0–v1.1, order §1 / §4): 16 directional measures, each must hold against both Marchfolk and Sagekin (`partA/FNF181_reference_validation.json`; sheet `Fenn_central_references`).

| Measure | c1 FNL4 vs MF / SG | c2 FNF181 vs MF / SG |
|---|---|---|
| leg share | +2.68 / +1.34 % | +2.69 / +1.35 % |
| lower leg / leg | +3.84 / +3.84 | +4.39 / +4.28 |
| arm share; forearm / arm | +5.32 / +2.82; +1.97 / +0.38 | +5.55 / +2.92; +2.50 / +0.57 |
| hand; finger / hand | +7.30 / +2.32; +7.36 / +2.03 | +8.03 / +2.53; +7.91 / +2.16 |
| foot share; foot breadth / length | +3.94 / +4.85; −11.3 / −11.3 | +4.90 / +5.93; −11.5 / −11.7 |
| knee / ankle / wrist / elbow joint scale | −8.1 / −5.3 / −14.1 / −6.8 vs MF | −9.3 / −7.8 / −17.4 / −7.0 vs MF |
| torso; ribcage depth; thorax breadth | −3.9; −5.1; −3.4 vs MF | −3.8; −6.4; −1.6 vs MF |

**Results:**
- **c1: 16 / 16. c2: 15 / 16.** The one c2 exception is pelvis E-A2 (§A4).
- c2 replicates the c1 sign on 21 of 22 rows.
- The Fenn c2 − c1 differences track the human-family architecture (Marchfolk c2 − c1): same sign on 22 / 22, largest gap 4.2 %.
- FNF181 is therefore not a thin Marchfolk and not an extreme Sagekin. It carries the whole accepted Fenn skeletal-proportion system.

## A4. Pelvis (canon validation layer)

Canon validates the pelvis on **skeletal / bony geometry** (PV-D16); skin readings are diagnostics. I ran `skeletal_proxy.py` (lean skeletal-envelope builds, t = 0 / 0.5 / 1.0 cm) on FNL4, FNF181, MFM181 and MFF181.

| E-A2 rule | c1 | c2 |
|---|---|---|
| Hip-joint height / stature > MF | **yes** (0.5504 vs 0.5360) | **yes** (0.5421 vs 0.5278) |
| Bitrochanteric / crest not lower than MF | **yes**, +0.18 / +0.19 / +0.20 % | **−0.09 / −0.09 / −0.09 %** (1.0800 vs 1.0810) |

**Why the c2 result counts as a tie:**
- The difference is −0.001 in the ratio.
- The proxy's own alignment residual is 0.35 cm, which is 1.15 % of the bitrochanteric breadth.
- So −0.09 % is a **tie below method resolution**, not a measurable narrowing.

Fixing it would need a configuration-specific Fenn pelvic target, which the order forbids ("do not invent sex-specific Fenn anatomy"). It is flagged here as an author note, not changed.

The skin-surface diagnostic for the same ratio is −0.53 %.

**Part A verdict: PASS — READY FOR BODY PROPAGATION**, with the E-A2 tie recorded.

---

# PART B — body-family propagation and hidden-ear gate

## B1. Body-family candidates (diagnostic; carry the family human ear)

| | `FN_M_REF_RP3_bodyfam_v001.blend` (FNL4) | `FN_F_REF_RP3_bodyfam_v001.blend` (FNF181) |
|---|---|---|
| sha / geometry hash | `cbcc4d00…` / `fe4ff746…` | `e30215fc…` / `b44f13c8…` |
| Face topology hash | **`ec768ae2…` = family** | **`ec768ae2…` = family** |
| V / Q, quads | 57,842 / 57,840, 100 % | 57,842 / 57,840, 100 % |
| Integrity | 1 component; 0 boundary / non-manifold / degenerate; outward | same |
| Map / UVs / faces | byte-identical map `e690fbaf…`; UVs and faces = family | same |
| V = M @ hm08 | 0.0 | 0.0 |
| Read-back | ≤ 6e-8 m | ≤ 6e-8 m |

- No fitting or relaxation; frozen base and map hashes are unchanged (`frozen_base_hashes.txt`).
- The PC copies (`E:/…/Fenn/RP3/`) were read back byte-identical.
- Manifest: `FENN_RP3_bodyfam_propagation_manifest.json`.

## B2. Standard v1 gates

| Gate | FNL4 (c1) | FNF181 (c2) |
|---|---|---|
| Validator D1 + D3 + D4 + D5 + D6 | **69 / 69** | **69 / 69** |
| Validator without D6 (D4 + D5) | 67 / 69 (hip ±p) | 69 |
| T-1 / T-2 / T-3 / T-7 | pass | pass |
| Family → source, body (median / p95 / max) | 0 / 0.196 / 1.81 mm | 0 / 0.164 / 1.93 mm |
| Head | p95 0.09 / max 0.90 mm | p95 0.08 / max 0.92 mm |
| **Ear zone** (**non-final source anatomy**: MPFB human auricle) | max 0.47 mm | max 0.45 mm |
| Silhouette IoU, minimum | 0.9974 | 0.9971 |
| Density, 9 zones (face 0.134 / ears 0.100 % of stature) | pass | pass (face 0.131 / ears 0.100) |
| Face rings: mouth / orbit; mouth-corner poles | 32 / 43 / 43; 0 | 33 / 43 / 43; 0 |
| Contact | 60 / 60 source-inherited | 166 / 166 source (8 toe-2/3 cleft pairs, below) |
| Deformation vs Marchfolk v005, worst flip excess | +2 | 0 |

**Validator.**
- FNL4 without D6 shows the same hip forearm-probe artefact D6 was accepted for: the longer Fenn forearm.
- Margin-0 stations:
  - FNL4: thumb_mcp, toe1_j1, toe2_j2, toe3_j1;
  - FNF181: toe1_j1.
- Margin table: `validator/FENN_margin_table_D1-D6.csv`; sheet `Fenn_margin_D1-D6`.

**Contact detail (FNF181).** 8 foot pairs did not match a native pair within 1 cm. All of them:
- lie exactly on the native surface (0.0 mm), on unchanged v003-class rows;
- sit on native quads 5592 / 5992, whose triangles intersect each other in the source. These are opposite-facing surfaces in the toe-2/3 cleft, pressed together by Fenn's narrow foot.

The native audit misses this because those quads share a vertex. **This is documented source contact, not attributable to propagation** (`contact/FNF181_contact.json`).

**Deformation.** No new topology-class failure; all residuals are the known LBS rig-class regions.

## B3. Hidden-ear identity — HARD GATE (§8)

`fenn_rp3_v001/fenn_hidden_ear.py`; `anatomy/FN_hidden_ear_identity.json`; sheets `Fenn_hidden_ear_body`, `Fenn_hidden_ear_face`, `Fenn_shoulder_joint_scale`, `Fenn_pelvis_leg`, `Fenn_hand`, `Fenn_foot`.

**Setup.**
- Matched stature (~181 cm), frame, composition and age; R-6; no clothing or hair.
- The external ear (hm08 `w_ears` > 0.05) is excluded from every metric and harmonically collapsed onto the skull in the renders.

### Body — PASS

Region correspondence RMS, Fenn vs Marchfolk, against the human-human baseline (Sagekin vs Marchfolk):

| Region | c1 | c2 |
|---|---|---|
| trunk | 19.4 vs 8.9 mm | 18.2 vs 8.9 mm |
| arm | 11.1 vs 4.4 | 11.1 vs 4.4 |
| hand | 26.6 vs 11.1 | 26.9 vs 11.0 |
| leg | 26.8 vs 7.7 | 26.1 vs 7.6 |
| foot | 8.4 vs 1.3 | 8.4 vs 1.3 |
| neck | 4.9 vs 1.7 | 3.5 vs 1.7 |

- The Fenn departure is 2–6× the human-human difference in every region.
- Canon directions hold: 16 / 16 (c1) and 15 / 16 (c2, the E-A2 tie).
- The combined system — limb share, long-bone relationships, joint scale (−5 to −17 %), hands, feet, torso / ribcage, shoulders, pelvis-to-leg — is materially non-human.

### Face — NOT MET beyond the orbit / eye region

**Method.** Each comparator head is similarity-aligned onto the Fenn head (head size removed) on all non-ear head vertices. The table gives RMS residual by region.

| Region | c1 FN vs MF | c2 FN vs MF | Material departure? |
|---|---|---|---|
| orbit / eye region | **1.17 mm** (0.5 % HH) | **1.17 mm** | **yes** (eye-scale / eye-height targets) |
| forehead | 0.26 | 0.60 | no (spill-over from the orbit) |
| nose | 0.39 | 0.44 | no |
| cheeks / mid-face | 0.31 | 0.41 | no |
| cranium vault | 0.14 | 0.13 | no |
| mouth | 0.03 | 0.04 | no |
| jaw / chin | 0.08 | 0.11 | no |

**Canon descriptors** (`FENN_V1` §2–7 tendencies, Fenn vs Marchfolk):

| Descriptor | c1 | c2 |
|---|---|---|
| Cranial height / face | −0.06 % | +0.05 % |
| Skull breadth / HH | 0.00 % | +0.04 % |
| Lower-face width / bizygomatic | +0.01 % | −0.01 % |
| Jaw width / bizygomatic | +1.98 % (opposite to canon) | −0.07 % |
| Cheekbone height / HH | +0.05 % | +0.13 % |
| Forehead profile turn | +0.08 % | −0.12 % |

Only head size relative to stature differs (−1.2 %).

The `meas.json` craniofacial indices agree. FPI, CBH, FVI, FDH, FVB and MVI are within ±0.5 % of Marchfolk, and Eu–Eu, Zy–Zy and HL are all −1.1 to −1.2 %, i.e. uniform scale.

**Finding.**
- The accepted FNL4 head is the MPFB human head uniformly scaled about −1.2 %, plus the eye-region targets. FNF181 inherits it.
- With ears hidden, the Fenn face reduces to a human face with a larger, more open eye region.
- The canon's cranial height, narrower skull, lighter lower face, higher cheekbones, lighter jaw and smoother forehead-to-cranium line are **not expressed by the source**.

**Why this is a source gap, not a topology limit.**
- The family realization preserves the source face exactly (fit p95 0.07–0.08 mm), so propagation has lost nothing.
- The face topology (32–35 mouth / 43 orbit rings, no mouth-corner poles) can carry any craniofacial reshaping. The same topology already carries Skarn C1R's identity face.

**Gate result.** Hidden-ear body PASS; hidden-ear facial identity NOT MET → **STOP before Part C**.

---

## Required answers (§18)

| Question | Answer |
|---|---|
| Was a valid ~181 cm Fenn configuration-2 central reference created? | **Yes.** FNF181, 180.99 cm (candidate, pending author acceptance). |
| Is it deterministic and canon-coherent? | **Deterministic:** yes, \|dV\| 0 three ways. **Canon:** 15 / 16 body directions; the pelvis E-A2 bitrochanteric / crest ratio is a −0.09 % tie below method resolution (author note). |
| Do both Fenn body realizations preserve active family topology unchanged? | **Yes.** |
| Are both 69 / 69 under D1 + D3 + D4 + D5 + D6? | **Yes.** |
| Does hidden-ear **body** identity pass? | **Yes.** |
| Does hidden-ear **facial** identity pass? | **No.** Only the orbit / eye region departs. Cranium, forehead, cheeks / mid-face and jaw / chin carry no Fenn tendency in the accepted source. |
| Is a non-ear Fenn topology branch required? | **No topology branch is indicated.** The required work is a **Fenn craniofacial source branch**: author-directed geometry for cranium, forehead-to-cranium, cheeks / mid-face and jaw / chin, inside the existing face topology. Canon gives directions only; magnitudes need author decisions ("exact morphology and numeric envelopes remain OPEN"). |
| Does the current source lack final Fenn external-ear anatomy? | **Yes.** FNL4 / FNF181 carry the MPFB human auricle (ear zone reported as non-final). |
| Was one shared local Fenn ear-branch topology created? | **No.** Withheld by the §8 stop rule. |
| Do E1 / E2 / E3 share that topology? | **Not built.** |
| Which ear candidate is recommended and why? | **None this run.** For the next order: the W1e `FN-elven` v2 ear-family reference (procedural evidence geometry: L 8.6 cm, projection 50°, Y-shaped antihelix, cymba / cavum, tragus, lobe, continuous taper) is the obvious canon-derived basis for E2. |
| Did any new contact or topology-class deformation failure appear? | **No.** The FNF181 toe-2/3 cleft contact is documented source contact. |
| Is Fenn ready for author selection of the central ear geometry? | **No.** The facial hidden-ear gate must be resolved first. |

## For the author / next order

1. **Craniofacial source.** Decide the Fenn craniofacial departures to author on FNL4 / FNF181: cranial height / face, skull breadth, lower-face mass, cheekbone height, jaw, forehead line. Use either MPFB head targets or a sculpt branch on the existing topology.
2. **Re-run the hidden-ear facial gate.** Then the ear branch (Part C) can follow.
3. **FNF181 acceptance**, including the E-A2 tie ruling.
4. **Ear basis.** Optionally, adopt the W1e FN-elven ear-family reference as the E2 basis.

**STOP FOR CHATGPT REVIEW.** No freeze. Aelari, Vael and Halvren were not started. The family base was not modified, and no ear branch, rig, morphs, UV / materials, LOD or UE5 work was done.
