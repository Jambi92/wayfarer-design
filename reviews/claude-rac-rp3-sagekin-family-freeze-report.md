# RAC RP3 — Sagekin family freeze report

**Date:** 2026-10-27
**Order:** `reviews/chatgpt-rac-rp3-sagekin-d6-acceptance-and-freeze-order.md` (d921903)
**Parent gate:** `reviews/claude-rac-rp3-sagekin-config2-reference-and-propagation-gate.md` (8ed659d)
**Freeze record:** `SAGEKIN_RP3_FREEZE.json` (sha `85147a24…`)
- on E: in `E:/…/RaceBodies/production/Sagekin/RP3/`, read back byte-identical;
- copy in `reviews/rac-rp3-evidence/sagekin_rp3_freeze/`.

**Evidence:** `reviews/rac-rp3-evidence/sagekin_rp3_freeze/`

## Result

**SAGEKIN RP3 — AUTHOR ACCEPTED / FROZEN — MPFB FAMILY PROPAGATION PASS.**

Frozen by record: neither production file was re-saved and no geometry or topology changed. The freeze record is authoritative over the sidecar and embedded `RAC_status` strings, which still read "CANDIDATE - NOT FROZEN".

| Question (§13) | Answer |
|---|---|
| Is SGF178 now formally accepted as the Sagekin c2 central reference? | **Yes.** `reviews/reference-assets/manifest.json` role is "reference, configuration 2 (central reference)", with build and geometry hashes added. `specs/sagekin/SAGEKIN_V1.md` has an acceptance block. Source hashes are unchanged. |
| Is D6 implemented as authoritative? | **Yes.** `val2lib.py` / `validator_v2.py --scale-ref 173.143 --d5 --d6-native NATIVE.npz`. Standard v1 §6 is updated. |
| Did D6 regress any existing family realization? | **No.** No verdict or loop count was lowered anywhere, and there were 0 false positives across 7 joints × 6 realizations (§2). |
| Are Marchfolk still 69 / 69? | **Yes.** MF-M 69, MF-F 69. |
| Are Skarn still 69 / 69? | **Yes.** SK-C1R 69, SK-F 69. |
| Is SG 69 / 69? | **Yes.** Hip 4 → 6 / 5. |
| Is SGF178 69 / 69? | **Yes.** |
| Did all Sagekin anatomy / identity / face / density / contact gates pass? | **Yes** (§3). |
| Did any new topology-class deformation failure appear? | **No** (§4). |
| Were both Sagekin production bodies frozen successfully? | **Yes.** |
| Any read-back / hash mismatch? | **None.** |
| Is Fenn still the recommended next race? | **Yes**, with the branch flags in §6. |

## 1. Frozen files

Read back from the PC copies with `tools/rac/rp/sagekin_rp3_v001/freeze_sg_verify.py`. It uses `freeze_check.py` in Blender and never saves. Results: `readback/`, `SAGEKIN_RP3_freeze_readback.json`; **ALL CHECKS PASS**.

| File | SHA-256 | Geometry hash | Face hash | V / Q |
|---|---|---|---|---|
| `SG_M_REF_RP3_retopo_v001.blend` (SG, configuration 1) | `bb156e9c4bc4…` (= manifest) | `56a73d8f…` (= manifest) | `ec768ae2…` (= family) | 57,842 / 57,840 |
| `SG_F_REF_RP3_retopo_v001.blend` (SGF178, configuration 2) | `0ef62ffc34aa…` (= manifest) | `9dcc5000…` (= manifest) | `ec768ae2…` (= family) | 57,842 / 57,840 |

Both files:
- 100 % quads; 1 mesh object; `UVMap`;
- 1 component; 0 boundary edges; 0 non-manifold edges or vertices; 0 degenerate faces; outward normals;
- geometry equals the candidate to ≤ 6e-8 m;
- sidecar and landmark hashes equal the manifest / repository.

**Map compatibility.**
- The PC hm08 map is byte-identical to the active family map `e690fbaf…`, and the arrays are equal.
- Candidate V = M @ Sagekin hm08 exactly (max error 0.0).

**Sources unchanged.** These hashes are recorded in the freeze record:
- SG R-6 `fe45866f…`, build `e39eff0d…`;
- SGF178 R-6 `52ff5e04…`, build `7f502543…`, geometry hash `7755a8f0…`;
- SGF152-NAT `9f096ff6…`, SGF208 `adb02cc6…`.

Both sources regenerate identically (max \|dV\| 0). The frozen Marchfolk v005 and Skarn files and records were not touched.

## 2. D6 — final implementation and blast-radius check (§2–§5)

**Rule.** For non-digit stations, a band side is undefined when either selected endpoint's dominant skin bone is not one of the station's own bones. The skin weights are the native hm08 source weights carried through the family map.
- Own bones are in `val2lib.D6_OWN`: neck, shoulder, elbow, wrist, hip, knee and ankle each have their own table (table in Standard v1 §6).
- Excluded sides are handled exactly as D1 undefined sides, including the closed-ring fallback when every side is excluded.
- Each side reports its `endpoint_dominant_bone` / `endpoint_dominant_weight`; each station lists `D6_undefined_sides`; fallback statuses carry `+D6_FOREIGN_SEGMENT_UNDEFINED`.

**Regression.** `tools/rac/rp/sagekin_rp3_v001/d6_regression.py` was run on all six realizations (`D6_regression/`). It audits **every non-digit band side**: endpoint bones and weights, and the audit-zone composition of the side path.

| Realization | D1–D5 | D1–D6 | Lowered | Sides excluded by D6 (path zone) | False positives |
|---|---|---|---|---|---|
| MF-M-R | 69 | **69** | none | hip ±p (forearm; arm zone), elbow ∓p (spine_02; trunk zone) | 0 |
| MF-F-R | 69 | **69** | none | hip (forearm / hand), elbow (trunk) | 0 |
| SK208-C1R | 69 | **69** | none | same | 0 |
| SKF208 | 69 | **69** | none | same | 0 |
| SG | 67 | **69** | none | same | 0 |
| SGF178 | 69 | **69** | none | same | 0 |

**By joint.** Every realization audited 4 neck sides and 8 sides each at shoulder, elbow, wrist, hip, knee and ankle. D6 excluded sides only at **hip (2)** and **elbow (2)**. Shoulder, knee, ankle, wrist and neck had 0 exclusions.

**Path zones.**
- Every side D6 kept has its whole path in the station's own body region (own-zone fraction 1.0).
- Every side D6 excluded has its whole path in the foreign region.
- Some kept sides have a dominant weight below 0.5, but always on an own bone (pelvis / thigh at the hip, upperarm at the shoulder). They are blended within the joint and correctly kept.

**Verdict changes.** Loop counts change only at the hip: SG 4 → 6, SGF178 12 → 15, SK-F 12 → 18. Elbow exclusions leave the loop counts unchanged.

**No false-positive ownership exclusion was found, so there is no stop condition.**

**Final margin table** (six realizations, D1–D6): `MPFB_family_margin_table_D1-D6.csv`, sheet `sheets/MPFB_family_margin_D1-D6.jpg`.

Sagekin margin-0 stations:
- SG: thumb_mcp, toe1_j1, toe2_j1, toe4_j1;
- SGF178: toe1_j1, toe4_j1.

The same stations are at margin 0 on the frozen v005 realizations (Standard v1 margin section).

## 3. Sagekin gates re-confirmed (§7)

Geometry is unchanged since the parent gate; results were re-read in the freeze verification.

| Gate | SG (c1) | SGF178 (c2) |
|---|---|---|
| Validator D1 + D3 + D4 + D5 + D6 | **69 / 69** | **69 / 69** |
| T-1 / T-2 / T-3 / T-7 | pass | pass |
| Family → source, body (median / p95 / max) | 0 / 0.20 / 1.79 mm | 0 / 0.17 / 2.02 mm |
| Silhouette IoU, minimum | 0.9976 | 0.9976 |
| Identity: fit ≪ signal in every zone (no regression toward Marchfolk, no exaggeration, no elfification) | holds | holds |
| Face: mouth / orbit rings; mouth-corner poles; mouth / orbit pass | 32 / 43 / 43; 0; pass | 34 / 43 / 43; 0; pass |
| Human auricle (ears deviation max) | 0.47 mm | 0.45 mm |
| Density, 9 zones | 9 / 9 pass | 9 / 9 pass |
| Contact: new propagation-induced rest defects | 0 (70 / 70 source-inherited) | 0 (122 / 122) |

SG and SGF178 remain valid central Sagekin references. Race-relevant proportions are carried exactly (production = M @ source): longer limbs, shorter torso, shallower ribcage, human hands, feet and auricle.

## 4. Deformation and carry-forward (§7, §9)

**No new topology-class failure.** Across the 18 Standard v1 poses, the worst Sagekin excess over the frozen Marchfolk v005 realization on the same topology is +2 flips (SG) and 0 (SGF178).

**Toe extension 30°** (`SAGEKIN_toe_flip_overlap_vs_marchfolk_v005.json`):
- **SGF178:** 58 flips, a strict subset of MF-F v005's 60, including the same MPFB-CF-1 toe-2 MTP crease faces. This is the CF-1 class, so no new ID.
- **SG:** 71 flips (MF-M 70); 69 are shared with MF-M. The other 2 (faces 54413 and 56501):
  - are on unchanged v003-class rows;
  - lie within 0.6 cm of flips in SG's own native hm08;
  - are adjacent to MF-M flips.

  This is the known single-ball-bone LBS crease region, so no new ID.

**Register.** `specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md` has a Sagekin section that records the applicability only, without duplicate IDs.

## 5. Records updated

- **`reviews/reference-assets/manifest.json`:** SGF178 is the accepted c2 central reference. SG (c1 central), SGF152-NAT (c2 minimum) and SGF208 (c2 maximum) are unchanged. No source hash is altered.
- **`specs/sagekin/SAGEKIN_V1.md`:** configuration-2 central-reference acceptance block.
- **`specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md`:**
  - D6 added: purpose, dominant-bone ownership method, station-owning-bone table, fallback, regression requirement and baseline, and the prohibition on changing topology for foreign-segment probes;
  - authoritative validator = **D1 + D3 + D4 + D5 + D6**;
  - Sagekin listed among the frozen realizations;
  - D1–D6 margin table referenced.

  The principle is retained: the technical process is standardised; race anatomy and identity are not.
- **`specs/STATUS.md`:** narrow update. **Handoff:** updated.

## 6. Next race — Fenn (recommendation only; not started)

**Fenn remains the recommended next RP3 race.** Its accepted source is `FNL4` (W1p, 181.16 cm, one configuration built). It is likely the **first true race-specific topology branch**:
- **Ears.** Fenn ears are their own external-ear anatomy, not human ears with stretched tips (`FENN_V1` §8 / §9). RP0 §6 planned an elf ear-density branch on the shared ear vertices. The family base's human-auricle density may not carry the tip, helix extension and projection.
- **Skeleton and identity.** Fenn are "the first playable race with a genuinely non-human skeleton" and must never read as thin humans with pointed ears. The hidden-ear validation (`FENN_V1` §13) is a hard identity gate. Elven long-bone relationships, joint scale, pelvis, ribcage and hands / feet are identity-bearing zones where propagation may hold geometrically but identity must be proven.
- **Configurations.** Only one Fenn configuration is built. A configuration-2 decision is likely needed, as for Sagekin.

A likely split:
- family propagation remains valid for most of the body;
- the ears (and possibly other identity zones) need a sanctioned branch.

The next order decides the strategy.

**STOP FOR CHATGPT REVIEW.** Fenn, Aelari, Vael, Halvren, Durrim, Pipkin, Cogling, rig finalisation, creator morphs, UV / materials, LOD and UE5 were not started.
