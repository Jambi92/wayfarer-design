# RAC RP3 — Fenn final consolidation / validation / freeze report

**Date:** 2026-10-27
**Order:** `reviews/chatgpt-rac-rp3-fenn-final-consolidation-freeze-order.md` (6d2eadc)
**Parent gate:** `reviews/claude-rac-rp3-fenn-ear-v002-refinement-gate.md` (96c41d0)
**Freeze record:** `FENN_RP3_FREEZE.json` (sha `0bafdfb4…`)
- on E: in `E:/…/RaceBodies/production/Fenn/RP3/`, read back byte-identical;
- copy in `reviews/rac-rp3-evidence/fenn_rp3_freeze/`.

**Evidence:** `reviews/rac-rp3-evidence/fenn_rp3_freeze/`
**Tools:** `tools/rac/rp/fenn_rp3_v001/`:
- `run_fnfinal.sh`, `run_fnfinal_eval.sh`;
- `fn_make_prod.py`, `fn_final_anatomy.py`, `fn_final_gates.py`, `fn_final_sheets.py`, `fn_freeze_verify.py`, `fn_freeze_record.py`.

## Result

**FENN RP3 FINAL PASS — AUTHOR ACCEPTED / FROZEN**

- Both final production bodies were rebuilt from the committed immutable inputs.
- Every gate in §5–§13 is green on both configurations.
- PC read-back is byte-exact.
- Fenn RP3 is frozen by record. Neither production file was re-saved after it was written and read back.

| File | Configuration | SHA-256 | Geometry hash | Face-topology hash | V / Q |
|---|---|---|---|---|---|
| `FN_M_REF_RP3_v001.blend` | 1 — FNL4 body + FNL4-CF2 + E2 / v002 | `3f7f1778…` | `36aedf19…` | `4615d6bc…` | 58,944 / 58,942 |
| `FN_F_REF_RP3_v001.blend` | 2 — FNF181 body + FNF181-CF2 + E2 / v002 | `14c1cf81…` | `bff70eb0…` | `4615d6bc…` (identical) | 58,944 / 58,942 |

Sidecars per body: `_branch_map.npz`, `.json` and `_landmarks.json`.
- The branch map holds hm08 weight / zone proxy rows, the v005 → production index map, the removed v005 vertices / faces, and part / side.
- The geometry hashes equal the reviewed v002 candidate blends exactly.

## 1. Composition and topology (§3, §4)

- **Outside the ear branch:** MPFB Family Base v005 topology, carrying the CF2 family realization.
- **Ear:** the accepted Fenn ear branch topology v002 with E2 geometry.
- **Shared topology:** one face list for both configurations (face-topology hash identical).
- **Counts:** 58,944 V / 58,942 Q, 100 % quads.
  - Ear branch: 1,732 V / 1,757 Q per side.
  - Root loop: 52 vertices per side, valence 4.
  - Transition ring: 102 v005 vertices.
- **UV:** `UVMap` keeps the family UV on all 55,428 v005 faces. The 3,514 branch faces carry a zero placeholder; final UV is out of scope. The plan is identical on c1 and c2.
- **Vertex group:** `ear_branch`.
- **Family topology unchanged:** the active family topology is unchanged outside the branch. The CF2 family geometry outside the branch is byte-identical (transition ring excluded; its accepted displacement is ≤ 0.059 cm).

## 2. Clean rebuild / provenance (§5)

| Step | c1 FNL4-CF2 | c2 FNF181-CF2 |
|---|---|---|
| Regenerate R-6 from `reviews/reference-assets/builds` (`regen.py`) | geometry identical, max \|dV\| 0 | geometry identical, max \|dV\| 0 |
| Native hm08 export | byte-equal arrays to the reviewed native | same |
| Propagate onto v005 (frozen blend + hm08 map) | family npz **byte-identical** (`2331cebf…`) | **byte-identical** (`5727201a…`) |
| Ear branch v002 E2 from the committed cuff canon | all 14 arrays equal the reviewed v002 candidate; committed geometry record within 2e-15 cm | same |
| 10 shape probes | geometry identical to the reviewed probes | — |
| Production blend | geometry hash = reviewed v002 blend | same |

**Immutable hashes are re-verified and unchanged** (`immutable_and_source_hashes.txt`):
- v005 blend `e560386c…`, hm08 map `e690fbaf…`, v005 freeze record `2d555a5e…`;
- FNL4 / FNF181 R-6;
- CF2 R-6 `b10fb791…` / `3674b724…`, CF2 builds `b5b2117c…` / `4c1718e7…`;
- ear topology v002, cuff canon, v005→v002 map and geometry record.

No hidden local edits: the rebuild reads only committed records and the frozen family base.

## 3. Integrity (§6)

| | c1 | c2 |
|---|---|---|
| Quads / components / boundary / non-manifold edges and vertices / degenerate faces | 100 % / 1 / 0 / 0 / 0 / 0 | same |
| Winding consistent; outward normals | yes; yes | yes; yes |
| Self-intersection pairs (whole mesh) | 60 = CF2 family set exactly | 166 = CF2 family set exactly |
| Pairs on ear-branch faces | 0 | 0 |
| Contact class (family record) | 60 / 60 source-inherited | 166 / 166 source (documented toe-2/3 cleft) |
| Root valence 4 (per side) | 52 / 52 | 52 / 52 |
| Seam / float / burial (ear–head clearance min) | none (0.38 cm) | none (0.45 cm) |
| Transition displacement max | 0.057 cm | 0.059 cm |
| Blender read-back of the PC copy vs candidate | ≤ 6e-8 m, faces equal | same |

## 4. Validator D1 + D3 + D4 + D5 + D6 (§7)

| | c1 `FN_M_REF_RP3_v001` | c2 `FN_F_REF_RP3_v001` |
|---|---|---|
| Firm PASS | **69 / 69** | **69 / 69** |
| Margin-0 stations | thumb_mcp l/r, toe1_j1 l/r, toe2_j2 l/r, toe3_j1 l/r | toe1_j1 l/r |
| D5 exclusions | pinky_ip1 l/r, toe1_j1 l/r, toe5_j1 l/r (one side each) | toe1_j1 l/r, toe2_j1 l/r (both q sides), toe5_j3 l/r |
| D6 exclusions | elbow l/r, hip l/r (one side each) | same |

**Fallback statuses:**
- **c1:**
  - thumb_mcp_l closed-ring;
  - hip l/r defined-sides + D6;
  - toe3_j3 l/r defined-sides + scoped adjacent-digit pole;
  - pinky_mcp_r and toe1_j2_r defined-sides.
- **c2:**
  - thumb_mcp_l closed-ring;
  - hip_l defined-sides + D6;
  - toe3_j3 l/r and toe4_j2 l/r scoped adjacent-digit pole (with defined-sides except toe3_j3_r);
  - shoulder_r defined-sides.

**No regression from consolidation.** Loops, margins, valid sides and D5 / D6 exclusions are identical to the CF2 family realization at **all 69 stations** on both configurations.

Six station *labels* differ only in a fallback annotation:
- c1: index_mcp_l, pinky_mcp_l, shoulder_r, toe1_j2_r;
- c2: shoulder_l, hip_l.

The annotation depends on the raw loop count of an already-undefined side, and that count depends on vertex order; the branch re-indexes the mesh. The ear branch is not near any body station.

Records: `validator/`, margin table `sheets/FENN_FINAL_validator_margin_table.csv`, sheet 13.

## 5. Anatomy / identity (§8)

**Body anatomy** (`fn_final_anatomy.py` = `anatomy.py` with the ear branch excluded):
- The R-6 source still carries the MPFB human auricle, and the production body carries the accepted E2 ear, so the external ear is gated in §7 instead.
- Excluded points: production branch vertices, and source vertices with `w_ears` > 0.05 or within 1 cm of the branch.
- Distances are taken to the full other surface. Silhouettes are compared outside the ear pixels.

| | c1 | c2 |
|---|---|---|
| T-1 body (prod→src median / p95 / max) | 0 / 0.20 / 1.81 mm — pass | 0 / 0.17 / 1.93 mm — pass |
| T-2 head (no ear) / hands / feet | max 0.88 / 0.84 / 0.88 mm — pass | 0.86 / 0.75 / 0.85 mm — pass |
| T-3 stature / bbox | −0.45 mm / ≤ 0.45 mm — pass | −0.00 mm — pass |
| T-7 silhouette IoU (front / rear / profiles) | 0.9982 / 0.9982 / 0.9974 / 0.9973 — pass | 0.9972 / 0.9972 / 0.9978 / 0.9977 — pass |

These equal the unbranched CF2 family realization (`anatomy.py`: T-1 / T-2 / T-3 / T-7 pass, body max 1.81 / 1.93 mm).

Unmasked, `anatomy.py` on the production body reports T-1 / T-2 and T-7 FAIL because of the ear alone: ear zone median 6.4 mm vs the human auricle, front IoU 0.994. Both runs are recorded.

**Fenn identity:**
- `sg_identity.py`: identity holds in **all zones** on both configurations.
- Fit ≪ signal vs matched Marchfolk / Sagekin / the other configuration.
- The ratio of signal median to fit p95 is 13–220 (head 18 / 15, hand 196 / 221).
- The listed systems are all carried exactly through the family map: long limbs, joint gracility, hands, feet, torso / ribcage, pelvis-leg and shoulder.

**Hidden-ear body — PASS.** Rerun on the CF2 sources (`fenn_hidden_ear.py`). Fenn departure is 2.1–6.5× the human–human baseline in every region:
- c1: trunk 2.2, arm 2.5, hand 2.4, leg 3.5, foot 6.4, neck 2.9;
- c2: 2.1 / 2.6 / 2.5 / 3.4 / 6.5 / 2.3.

**Hidden-ear face — PASS.**
- `cf_eval.py` on the rebuilt CF2: **6 / 6 canon systems material, 6 / 6 direction**. Descriptors and region RMS are identical to the accepted CF2 evaluation.
- Facial regions with a material departure: cranium vault, forehead, orbit, cheeks, mouth and jaw (6 / 7; the nose does not depart).

## 6. Craniofacial / UFCA (§9)

| | c1 | c2 |
|---|---|---|
| CF2 source hashes | unchanged | unchanged |
| Mouth rings / orbit rings | 31 / 43 / 43 | 34 / 43 / 43 |
| Mouth-corner poles; poles within 2 cm of mouth; poles within 2 cm of each eye | 0; 0; 4 / 4 | 0; 0; 4 / 4 |
| Lip / orbit pockets open (mouth / orbit pass) | yes / yes | yes / yes |
| Face density (mean % stature) | 0.136 (limit 0.25) | 0.133 |
| Equal to the CF2 family realization | yes | yes |

The ear branch does not alter the accepted CF2 face.

## 7. Ear final gate (§10)

| | c1 | c2 |
|---|---|---|
| E2 measures (chord / height / width / body angle / extent / upper axis) | 8.10 / 7.94 / 3.06 cm / 52.7° / 2.63 cm / 32.3° | 7.80 / 7.63 / 2.95 / 52.7° / 2.63 / 32.3° |
| Measures vs reviewed v002 | identical | identical |
| T-4 | 165 / 3,718 (4.4 %) — accepted v002 level | 145 / 3,718 (3.9 %) |
| Aspect max; > 10 | 9.29; 0 | 8.71; 0 |
| Branch self-intersections | 0 | 0 |
| Root crease max; transition | 64.0°; 0.057 cm | 64.0°; 0.059 cm |
| Thickness | median 0.29 cm, minimum 0.15 cm at the thinned lobe edge | 0.28 / 0.14 |

- External-ear anatomy is present on both configurations: helix, antihelix stem and crura, triangular fossa, cymba / cavum, crus of helix, tragus, antitragus, intertragic notch, lobe, upper extension and natural taper (sheet 09).
- There is no stretched-human-ear read: sheets 05 and 10, and the overlay in sheet 15.
- There is no new concentrated distortion cluster. The accepted residuals are unchanged: root-band cells, aspect 6–10 quads, bridge-corner cells.

## 8. Density (§11)

All 9 family density zones pass on both configurations (mean % of stature, c1 / c2):

| Zone | c1 | c2 |
|---|---|---|
| face | 0.136 | 0.133 |
| ears | 0.096 | 0.093 |
| hand | 0.144 | 0.133 |
| foot | 0.200 | 0.190 |
| trunk | 0.484 | 0.485 |
| arm | 0.481 | 0.444 |
| leg | 0.496 | 0.483 |
| neck | 0.309 | 0.280 |
| head | 0.299 | 0.302 |

- Ear branch mean edge: 0.098 / 0.095 % (limit 0.25 %); p95 0.170 / 0.167 %.
- Only the face / ears / head zone figures differ from the family realization, because the branch replaces the human-ear rows.
- No accidental over-densification.

## 9. Deformation (§12)

**Standard v1, 18 poses.** Source rig plus the MPFB weights carried through the branch map, plain LBS:
- The production body adds **0 flips, 0 new self-intersections and 0 new folds** over its CF2 family realization on **every** pose, both configurations.
- Worst excess over the frozen Marchfolk v005 realization on the same topology class: c1 +2 (shoulder_flex90 15 vs 13; toe_flex30 1 vs 0), c2 0. These are the same family-class LBS regions as the accepted Fenn body gate.
- No new topology-class failure (`FENN_FINAL_deformation_summary.json`, sheet 14).

**Ear readiness** (neck flex / ext 30, head yaw ±45, pitch ±20, roll ±20): 0 new branch self-intersections, 0 flipped branch faces, 0 root inversions on both configurations.

No ear rigging was authored.

## 10. Shape probes (§13)

The 10 probes (projection ±10°, tilt ±8°, sweep ±0.6, length ±10 %, tip blunt / sharp) were rebuilt in the clean run and are geometry-identical to the reviewed probes:
- same topology;
- 0 self-intersections; 0 boundary edges;
- aspect max 9.33;
- no broken root;
- every measure moves in the intended direction (chord 7.22 / 8.99 cm, body angle 42.8 / 62.6°, sweep 0.59 / 0.96 cm, upper axis 25.9 / 39.6°, tip angle 52.5 / 17.9°).

These remain topology-readiness diagnostics, not creator morphs.

## 11. Carry-forward (§14)

- **FENN-CF-1** (configuration-2 CF2 mouth-corner expression units; facial rig / corrective stage) is preserved unchanged.
- No new Fenn ID.
- The accepted v002 T-4 residual is recorded as a topology-quality residual, not a carry-forward item (`specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md`).

## 12. Visual freeze package (§15, `sheets/`)

All sheets use identical cameras per sheet.

| No. | Content |
|---|---|
| 01, 02 | full body c1 / c2 |
| 03, 04 | head front / profile / ¾, c1 / c2 |
| 05 | E2 ear: lateral / front / rear / top |
| 06 | ear wire |
| 07 | T-4 / aspect |
| 08 | root integration |
| 09 | ear anatomy annotation |
| 10 | c1 vs c2 E2 |
| 11 | hidden-ear body, c1 / c2 |
| 12 | hidden-ear face, c1 / c2 |
| 13 | validator / margin table |
| 14 | deformation summary |
| 15 | source → production overlay |

## 13. Freeze by record (§16) and PC read-back

- **`FENN_RP3_FREEZE.json`** records:
  - filenames, SHA-256, geometry / face / branch-topology / branch-map hashes;
  - accepted source, CF2 and v005 hashes;
  - validator, anatomy / identity, density and T-4 results;
  - accepted residuals, carry-forward references and read-back results.
- **PC read-back** (`FENN_RP3_freeze_readback.json`, `production/pc_readback_sha256.txt`):
  - all 8 production files plus the freeze record are byte-equal to the written files;
  - the Blender read-back (`freeze_check.py`, no save) passes every integrity check;
  - the branch-map arrays equal the candidate;
  - the validator recomputed on the read-back gives 69 / 69 on both.
- The freeze record is authoritative over the embedded `RAC_status` string ("… freeze status is held by record: FENN_RP3_FREEZE.json").

## 14. Records updated (§17)

- **`reviews/reference-assets/manifest.json`:**
  - FNL4-CF2 / FNF181-CF2 are the accepted c1 / c2 craniofacial references, frozen in `FN_M/F_REF_RP3_v001`;
  - FNL4 / FNF181 body ancestry is retained;
  - no source hash or provenance was overwritten.
- **`specs/fenn/FENN_V1.md`:** RP3 final status block (frozen; E2 + ear topology v002 = the accepted Fenn external-ear branch; Fenn only).
- **`specs/STATUS.md`**, the session handoff and the carry-forward register.

## 15. Next race (§19 — recommendation only; not started)

**Aelari** is the recommended next RP3 race.

- Fenn is the **first accepted elf-specific ear branch**.
- Aelari must not inherit Fenn geometry or become a "taller Fenn".
- The ear-branch concepts may be proposed for reuse, but Aelari ear / head / body identity needs its own author gate. Reusable concepts:
  - root-loop interface on v005;
  - shared cuff canon method;
  - tapered-leaf upper extension;
  - deformation-aware guard.

**STOP FOR CHATGPT REVIEW.** The following were not started or changed: Aelari, Vael, Halvren, any universal elf ear topology, active MPFB Family Base v005, production ear rigging, creator morphs, UV / materials, LODs, UE5.
