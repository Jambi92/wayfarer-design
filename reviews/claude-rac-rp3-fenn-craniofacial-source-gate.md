# RAC RP3 — Fenn craniofacial source authoring + hidden-ear revalidation — gate

**Date:** 2026-10-27
**Order:** `reviews/chatgpt-rac-rp3-fenn-craniofacial-source-order.md` (2de0e28)
**Evidence:** `reviews/rac-rp3-evidence/fenn_craniofacial_v001/`
**Tools:** `tools/rac/rp/fenn_rp3_v001/`
- `fn_face_metrics.py`, `cf_probe_eval.py`, `cf_eval.py`, `cf_expr.py`, `cf_sheets.py`;
- `build_cf.sh`, `run_cfeval.sh`.

## Result

**FENN CRANIOFACIAL PASS — CF2 RECOMMENDED.**

- Hidden-ear facial identity now passes on **6 / 6** canon systems for both configurations, with one shared craniofacial design.
- The orbit stays Fenn without dominating: its share of the face residual drops from 0.80 to 0.07.
- Face topology and the family base are unchanged.

**Not frozen.** The ear branch was only *prepared* (§8), not built.

## 1. Author decisions recorded (§1, §16)

- **FNF181** is the accepted **configuration-2 central body reference**.
- The **E-A2 pelvis tie** is accepted and left **unchanged**; no configuration-specific pelvis was introduced.
- **Body-family propagation** is accepted.
- `reviews/reference-assets/manifest.json`:
  - FNF181 is "central BODY reference; craniofacial source geometry PROVISIONAL until a CF revision is accepted; external ear not final".
  - FNL4 carries the same craniofacial-provisional note.
  - No source hash changed (`frozen_base_and_source_hashes.txt`).

## 2. Source-authoring architecture (§3, §5, §6)

**Method:** existing **MPFB 2.0.17 head / cheek / chin targets** (preferred method 1). Every source vertex is reproducible by `build_variant.py` from a build record.
- No sculpting.
- No production-mesh-only edits.
- No face-topology change.

**Design, in four steps:**
1. **Target probe.** 24 MPFB head-region targets were each applied at 0.5 on FNL4 (`definitions/probe_response.json`). Each probe records:
   - descriptor deltas;
   - region RMS;
   - non-head displacement.
2. **Solve.** Bounded ridge least squares (weights 0–0.6, λ 1) toward canon-direction departures. It includes:
   - a cranium-vault RMS penalty;
   - a **crown-roundness guard**;
   - a no-head-size-change constraint.

   Nose and mouth targets were excluded by rule (§4.5), and so was the neck (it moves the body).
3. **Rejected first iteration** (`definitions/CF_definitions_iteration1_rejected.json`). It used `head-diamond` 0.48, which numerically passed but gave a **peaked crown** on visual review. It was replaced, and the guard was added.
4. **Final CF2 target set**, the same keys and signs for both configurations; the accepted eye-scale / eye-height targets are kept:

   | Target | Value |
   |---|---|
   | head-oval | 0.12 |
   | head-scale-horiz-decr | 0.145 |
   | head-scale-vert-incr | 0.07 |
   | head-scale-depth-decr | 0.60 |
   | LR:cheek-trans-up | 0.60 |
   | LR:cheek-inner-decr | 0.25 |
   | LR:cheek-volume-decr | 0.32 |
   | chin-bones-decr | 0.60 |
   | chin-height-decr | 0.14 |

   **CF1 = 0.55 × CF2; CF3 = 1.6 × CF2** (`definitions/CF_definitions.json`). Only magnitude differs between candidates.

**Configuration sharing.** The same target dictionary is applied to FNL4 (configuration 1) and FNF181 (configuration 2); only the shared MPFB configuration architecture differs.
- Same region set, operation, signs: yes.
- c2 / c1 normalized magnitudes 0.99–1.13 per descriptor.
- Identity strength c1 / c2: CF1 4.4 / 4.6, CF2 7.8 / 8.2, CF3 12.4 / 12.9.

**Body preserved (§7).**
- The height macro is held, so the body skeleton is unchanged.
- Largest non-head change: CF1 0.06 / CF2 0.11 / CF3 0.17 mm, only at the head-neck boundary.
- Disclosed: CF2 raises the head top by 2.8 mm. Head height goes up 1.2 %, which cancels the source's −1.2 % head-size deficit versus Marchfolk.

**Determinism.** All six candidates regenerate identically (`regen.py`, max \|dV\| 0). R-6 sources and build records are in `sources/`.

## 3. Hidden-ear facial gate (§8, §9) — PASS

**Method.** Same as the parent gate:
- matched-stature MFM181 / MFF181 / SGM181 / SGF181;
- ears excluded / collapsed;
- head size removed by similarity alignment.

**Landmarks.** The craniofacial descriptors now use **fixed hm08 landmark vertices** chosen once on the FNL4 template (vertex, nasion, glabella, menton, euryon, zygion, cheek apex, gonion, lower-face, crown). Every body is read at the same anatomical vertices.
- **Disclosure:** with this robust method the current source's configuration-1 jaw-width reading is **−0.29 %** (essentially equal to Marchfolk). The parent gate's +1.98 % came from a noisy band measurement.

**Material** (selection constraint only, not canon): at least 1.0 % against **both** Marchfolk and Sagekin in the canon direction, **and** more than 2× the human-human baseline (Sagekin vs Marchfolk, ≤ 0.06 % on every descriptor).

**Descriptor departures vs matched Marchfolk** (c1 / c2):

| Descriptor (canon direction) | Source | CF1 | **CF2** | CF3 |
|---|---|---|---|---|
| cranial height / face (+) | −0.01 / +0.02 % | +1.21 / +1.28 | **+2.21 / +2.30** | +3.54 / +3.67 |
| skull breadth / HH (−) | 0.00 / +0.05 | −1.38 / −1.36 | **−2.49 / −2.49** | −3.95 / −3.98 |
| forehead-to-cranium turn (−, smoother) | +0.20 / +0.12 | −1.17 / −1.22 | **−2.28 / −2.29** | −3.71 / −3.68 |
| cheekbone height / HH (+) | +0.03 / −0.04 | +0.69 / +0.72 | **+1.22 / +1.33** | +1.91 / +2.14 |
| mid-face projection / HH (−, lighter) | −0.06 / −0.06 | −1.78 / −1.84 | **−3.17 / −3.29** | −4.99 / −5.18 |
| lower-face width / bizygomatic (−) | +0.01 / +0.01 | −1.65 / −1.67 | **−3.03 / −3.05** | −4.89 / −4.93 |
| lower-face height / HH (−) | +0.01 / +0.01 | −1.22 / −1.27 | **−2.22 / −2.31** | −3.54 / −3.67 |
| jaw width / bizygomatic (−) | −0.29 / −0.42 | −1.37 / −1.65 | **−2.26 / −2.67** | −3.48 / −4.05 |
| **Systems material (of 6)** | **0** | 6* | **6** | 6 |
| Orbit share of face residual | 0.80 | 0.14 | **0.07** | 0.05 |

\* CF1 is borderline: cheekbone height is +0.7 %, so the system passes only through mid-face projection, and the forehead turn sits at the 1 % line.

All directions also hold against Sagekin. Full table: `CF_hidden_ear_eval.json`; sheets `CF_3_vs_matched_humans_c1/c2`.

**Region RMS vs Marchfolk, CF2 c1** (head size removed; sheet `CF_4_residual_heat`):

| Region | RMS |
|---|---|
| cranium vault | 4.22 mm |
| forehead | 2.76 |
| cheeks / mid-face | 2.13 |
| jaw / chin | 2.19 |
| orbit | 1.65 |
| mouth | 1.31 |
| nose | 0.72 |

Against Sagekin the values are within 0.02 mm of these. The vault is the largest region but holds only 45 % of the residual, so no single region dominates.

- CF3 shows cheek hot-spots and a 6.8 mm vault.
- **Orbit:** it stays materially Fenn (1.65 mm, above the source's 1.17 mm) and is no longer the identity carrier.

**Visual read** (sheets 1–3, 5–8):
- CF2 reads as a slightly taller, narrower, rounded cranium with a smoother brow-to-crown line, slightly higher and lighter cheeks, and a lighter lower face and jaw.
- It is natural and non-caricatured, with clear human overlap, and not a "pretty-elf" jaw.
- CF1 is subtle.
- CF3 tends toward an elongated, stylized head and pronounced cheek planes.

## 4. Recommendation (§14)

**CF2**, because:
- every canon system departs clearly (≥ 1.2 %) but subtly;
- the orbit share is 0.07;
- c1 and c2 are consistent;
- no single-region outlier;
- the smallest expression amplification that still passes cleanly.

**CF1** is too borderline (cheekbone below 1 %). **CF3** is stronger than necessary but still valid (it is not a creator maximum).

## 5. Topology / UFCA regression (§10, §11)

All 6 candidates:
- family realization 57,842 V / 57,840 Q;
- face hash **`ec768ae2…`**; map byte-identical (`e690fbaf…`);
- V = M @ hm08;
- **no face-topology change**.

| Check | Result |
|---|---|
| T-1 / T-2 / T-3 / T-7 | pass on every candidate |
| Head family → source | p95 0.08–0.09 mm, max ≤ 0.95 mm; the family topology carries the authored geometry without loss |
| Orbit rings | 43 / 43 on all |
| Mouth rings | 31–34 (source 32–33). Same loops (identical topology); the count is a geometric radius criterion. Mouth and orbit pass flags: true. |
| Poles at mouth corners / within 2 cm of mouth | 0 / 0 |
| Poles near the eyes | 4 / 4, = source |
| Lip / orbit pockets | open, preserved |
| Face density | 0.127–0.132 % of stature (source 0.131–0.134; ceiling 0.25) |
| Validator D1–D6 | 69 / 69 on all 6 |
| Rest contact | unchanged (60 / 166 source pairs) |
| Blender read-back | ≤ 6e-8 m |

- PC copies are in `E:/…/Fenn/RP3/craniofacial/` (sha equal).
- **No craniofacial topology branch is needed.**

## 6. Expression sanity (§12; diagnostic)

**Setup.**
- MPFB 2.0.17 expression units (blink, lid-follow for look up / down, smile, anger, surprise, sadness) are added to each source.
- They are carried through the family map and checked on the head faces.
- Look left / right is **not supported**: eyeball rotation only, no skin unit.

**Findings** (`CF_expression_sanity.json`; sheet `CF_12_expression_sanity`):

| Area | Result |
|---|---|
| Eyelids | The generic blink unit already overlaps the lids on the current sources (c1 64, c2 59 pairs). Every CF is **equal or lower** (50–63). No orbit collapse. |
| Configuration 1 | No candidate exceeds its source materially in any expression. |
| Jaw / chin, anger, surprise | No new defect. |
| **Configuration-2 mouth corner** | See below. |

**Configuration-2 mouth corner.** CF2 adds:
- smile +6 self-intersection pairs;
- sadness +10 pairs and +12 flipped faces.

CF1 adds less and CF3 more. All of it is at the mouth corners, exactly where the **source already folds** (smile 4 pairs, sadness 2 flips). The lighter, raised mid-face amplifies the generic unit's existing corner fold.

**Class:** facial-rig corrective (mouth corner), not a source or topology defect. Recorded for the rig stage; no production weights or correctives were authored.

## 7. Visual sheets (§13)

`sheets/`:

| # | Sheet |
|---|---|
| 1 | `CF_1_source_vs_candidates` |
| 2 | `CF_2_…_ears_hidden` |
| 3 | `CF_3_vs_matched_humans_c1 / c2` |
| 4 | `CF_4_residual_heat` |
| 5 | `CF_5_cranium_forehead` |
| 6 | `CF_6_orbit_eye` |
| 7 | `CF_7_cheeks_midface` |
| 8 | `CF_8_jaw_chin` |
| 9 | `CF_9_wire_topology` |
| 10 | `CF_10_config1_vs_config2` |
| 11 | `CF_11_full_body_hidden_ear` |
| 12 | `CF_12_expression_sanity` |

Cameras are identical and at true scale.

## 8. Ear branch — preparation only (§15)

`ear_branch_prep/FENN_EAR_BRANCH_PREP.md`.

**Region:**
- per side, 1,206 faces / 1,233 vertices;
- root = **one closed 52-vertex loop**;
- branch = ear zone + one transition ring.

**Mapping plan:**
- all non-ear v005 rows are unchanged;
- 52 root rows are kept;
- interior ear vertices are replaced by one all-quad patch, with per-candidate root-frame offsets;
- shared by c1 and c2.

**Reference:** W1e `FN-elven` (L 8.6 cm, 50° projection, tilt 32° / sweep 1.6 cm, Y-antihelix, cymba / cavum, tragus, lobe; parameters in `W1e_FN-elven_params.json`).

**Proposal:**
- E1: 7.6 cm / 42°;
- **E2: the W1e reference**;
- E3: 9.4 cm / 55°.

All share one topology. No ear geometry was built.

## Required answers (§17)

| Question | Answer |
|---|---|
| Is FNF181 body architecture formally accepted? | **Yes** (recorded in the manifest). |
| Was the E-A2 pelvis tie left unchanged? | **Yes.** |
| Did CF1 / CF2 / CF3 share one craniofacial design architecture? | **Yes.** One target set, scaled 0.55 / 1.0 / 1.6, identical for c1 and c2. |
| Which regions now materially express Fenn identity? | Cranium height, skull breadth, forehead-to-cranium transition, cheekbone / mid-face, lower-face mass and jaw / chin (6 / 6), plus the orbit. |
| Does hidden-ear facial identity pass? | **Yes** (CF2 and CF3 clearly; CF1 borderline). |
| Does the orbit remain Fenn without dominating the whole identity? | **Yes.** 1.65 mm RMS; residual share 0.07 (was 0.80). |
| Which CF candidate is recommended? | **CF2.** |
| Did family topology remain unchanged? | **Yes** (`ec768ae2…`, map identical). |
| Did UFCA readiness remain intact? | **Yes.** |
| Did any new facial deformation / contact defect appear? | **No** new rest contact. Configuration 2's existing mouth-corner smile / sadness fold grows modestly with strength (CF2 +6 / +10 pairs, +12 flips). Facial-rig item. |
| Is a craniofacial topology branch actually needed? | **No.** |
| Is the project ready to proceed to the Fenn ear branch? | **Yes** after ChatGPT review; preparation note committed. |

**STOP FOR CHATGPT REVIEW.** No freeze. Fenn ears were not finalized. Aelari, Vael and Halvren were not started. The family base, creator morphs, rig, UV, LOD and UE5 were not touched.
