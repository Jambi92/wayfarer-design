# Claude Gate — RAC RP4 Pipkin Toe-Station Exception + Final Production Candidates

**Order:** `reviews/chatgpt-rac-rp4-pipkin-toe-exception-final-production-order.md` (68ba8e5; reviewed c3016d6)
**Date:** 2026-10-30
**Evidence:** `reviews/rac-rp4-evidence/pipkin/final/`
**Tools:** `tools/rac/rp/pipkin_rp4_v001/` (`run_pk_final.sh`, `pk_toe_exception.py`, `pk_make_prod.py`, `pk_final_sheets.py`)

## Result

**PIPKIN RP4 FINAL PRODUCTION PASS — READY FOR AUTHOR FREEZE**

Every §13 condition holds:
- **Validator:** adjusted 69 / 69 on PK91, PK107 c1, PK107 c2 and PK122. The raw history is preserved.
- **Toe exception scope:** applied only to the documented toe3 / toe4 j1 stations.
- **Candidates:** both c1 / c2 production candidates are clean.
- **Anatomy, firewalls and deformation:** pass.
- **Immutables:** unchanged.

**Nothing is frozen.** The record is `PIPKIN_RP4_FREEZE_CANDIDATE.json`, and the embedded status in both files reads "CANDIDATE / NOT FROZEN".

## 1. Validator — raw and author-adjusted (§2, §3)

**Raw record.** The raw authoritative D1 + D3 + D4 + D5 + D6 outputs are unchanged and committed in `validator_raw/`.

**Exception record.** `PIPKIN_toe_exception_validator_summary.json` holds the machine-readable exception. A station is relabelled `PASS_PIPKIN_TOE_PROBE_GEOMETRY_EXCEPTION` only if all of these hold:
1. The body is PK91 / PK-NAT / PK122.
2. The station is toe3_j1 / toe4_j1, left or right.
3. The raw status is `FAIL_LOOPS`, in `closed_ring_fallback` mode, with no crease pole (the documented case).
4. The size-consistent toe-probe diagnostic passes the station.

Any other failure would stay a failure. There were none.

| Body | Raw | Exception applied | Adjusted |
|---|---|---|---|
| PK91-NAT | 65 / 69 | toe3_j1_l / r, toe4_j1_l / r | **69 / 69** |
| PK-NAT (c1) | 65 / 69 | toe3_j1_l / r, toe4_j1_l / r | **69 / 69** |
| PKF107-NAT (c2) | 69 / 69 | — | **69 / 69** |
| PK122-NAT | 67 / 69 | toe3_j1_l / r | **69 / 69** |

Global D4, every other race's validator, the Pipkin feet and frozen Durrim are unchanged, and no foot topology was added.

## 2. Branch and production candidates (§4–§6)

**Branch.**
- `MPFB_PIPKIN_COMPACT_BRANCH_v001`, used exactly as reviewed (definition sha256 `ff16400f0ea1…`).
- Fresh realizations from that definition are bit-identical to the reviewed realizations on all four bodies, so branch placement was not revised.

| | PK_M_REF_RP4_v001 (c1, PK-NAT) | PK_F_REF_RP4_v001 (c2, PKF107-NAT) |
|---|---|---|
| vertices / quads | 58,162 / 58,160 (100 % quads) | 58,162 / 58,160 (100 % quads) |
| file sha256 | `554f1a743b6b1c51c70392ce699ac91d31163699a23ee8034fbd646a31ba6826` | `e64406bb1ca4ac677a86e98ac34b08ec24c334d7fcfc2e7961878f161b5969d3` |
| geometry hash | `1af7d3a818abd8d301234caad03d43c72fa014c50927b977aeb087ef7bd16a5c` | `fd208db6f6bfe98c0226b8d623fe681c5e7ff3a05f603d964a9a500bc65897e5` |
| face topology hash | `a11b8831506519db8ae17ba466540a0cd71faa5d82ca501f53c1fc1d5e3b76dc` | **identical** |
| branch definition hash | `ff16400f0ea131bc6709a88427e75c9c5b554545c8d3abe29b48ab93a9572e70` | identical |
| branch-map hash | `2e116576935275ce6ca41565b1cfb444899c63eb9cebdb429dd39c0686aaf7b0` | identical |
| landmark hash | `de99dddedb687ce5f2d146b2e68b5c4deb5f3696ee4bc506fd568e54c36b5108` | `d73d943eac78fa395bfcb798d183fd558575ab113354f32d8a7e23a05695d132` |

**Read-back** (Blender open, no save; both files):
- 1 component;
- 0 boundary edges, 0 non-manifold edges / vertices, 0 degenerate faces;
- normals outward, UVMap present;
- faces equal to the candidate;
- geometry hash equal; max |dV| 6e-8 m.

**Sidecars.** Each `_branch_map.npz` holds the exact M = S · M_v005, S itself, the v005 → production identity map and the part labels. The landmarks and the source lineage are in each `.json`.

## 3. Anatomy preservation (§7) — source vs production

| Body | T-1 / T-2 | T-3 (stature) | T-6 max drift | T-7 | body deviation p95 / max | contact new |
|---|---|---|---|---|---|---|
| PK91 | PASS | PASS (−0.23 mm) | 0.10 mm | PASS | 0.11 / 0.92 mm | 0 |
| PK107 c1 | PASS | PASS (−0.27 mm) | 0.12 mm | PASS | 0.13 / 1.08 mm | 0 |
| PKF107 c2 | PASS | PASS (0.00 mm) | 0.12 mm | PASS | 0.11 / 1.20 mm | 0 |
| PK122 | PASS | PASS (−0.30 mm) | 0.13 mm | PASS | 0.14 / 1.23 mm | 0 |

- **T-4:** 0 branch quads over 4:1 (max 3.84); branch angle flags 4, against 6 in the replaced v005 faces.
- **T-5:** adjusted 69 / 69, and density within the §8 ceilings.

The production branch only re-samples the v005 surface. So all of these are unchanged from the accepted sources:
- the low-set compact, pelvis-led trunk;
- preserved limb contribution;
- lighter joints than Durrim;
- adult hands / feet;
- mature face and ear tendency.

## 4. Firewalls on the final realizations (§8) — boards `sheets/PKF_C…G`

| Firewall | Result |
|---|---|
| 122 cm Pipkin vs frozen Durrim (W2H §4A carriers) | **16 / 16.** Durrim deeper / broader thorax, larger torso share, shorter limbs, thorax-led; Pipkin pelvis-led; Durrim heavier shafts / joints and broader palm / foot (board PKF_D) |
| Adult vs child (generator proxy, diagnostic only) | **17 / 19, 18 / 19, 19 / 19** (PK107, PKF107, PK91). Adult head share is below the child at every stature; no feature enlarged (board PKF_E) |
| Normalized Marchfolk | 7 / 7 on c1, c2 and 91; 6 / 7 at 122 (the accepted leg-share MARGINAL). Not a uniform scale; intentionally subtle (board PKF_F) |
| Cogling context | **11 / 11** at 91 and 107; comparison only (board PKF_G) |

## 5. Deformation (§9) — `PIPKIN_final_deformation_summary.json`, `deformation/`

| | Result |
|---|---|
| c1 PK_M (18-pose suite on the final realization) | 18 / 18 identical to v005 |
| c2 PK_F | 17 / 18 identical. thumb_opposition 54 vs 44 self-contact pairs: the known c2 class, all 54 matched to the existing v005 thumb–palm contact (0 unmatched) |
| PK91 / PK122 key poses (opposition, fist, wrist flex / ext, hip flex, knee 140, ankle, toe flex / ext, neck flex / rotation) | identical to v005 |

- The final c1 / c2 runs are identical to the reviewed runs.
- No new topology class.
- No grip / fist collapse.
- No new foot / toe defect: toe poses are identical to v005.

## 6. Immutables (§12) — `immutable_hashes_final.txt`

46 / 46 unchanged vs 68ba8e5. This covers:
- MPFB Family Base v005 map / core;
- the frozen Durrim RP4 branch and its production files;
- all 11 committed `*_FREEZE.json` records (Marchfolk v003, Sagekin, Fenn, Aelari, Vael, Halvren ×3, Grask, v005, Durrim);
- the Pipkin sources and the PKF107 anchor;
- the Cogling references used for comparison;
- the Pipkin branch definition (= reviewed value).

There is no Skarn RP3 freeze record in the repo, and no Skarn path was written. No frozen race changed.

## 7. Accepted notes carried into the candidate record (§11)

1. Pipkin c1 toe3 / toe4 j1 raw validator failures are a documented D4 probe-geometry artifact and are accepted under the Pipkin-specific toe-station exception.
2. The exception does not modify global D4 and does not apply automatically to Cogling.
3. Pipkin / Durrim, Pipkin / Marchfolk and Pipkin / Cogling visual separation is intentionally anatomical and may be subtle in neutral diagnostic clay.
4. PKF107-NAT is a technical c2 production anchor only; Pipkin sex-related anatomy remains OPEN.

## 8. Not done (STOP)

- No freeze.
- No global D4 change and no foot topology.
- Frozen Durrim untouched.
- No Cogling, Saurin, rig, creator or UE5.

**STOP FOR CHATGPT REVIEW.**
