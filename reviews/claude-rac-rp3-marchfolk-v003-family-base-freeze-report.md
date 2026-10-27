# RAC RP3 — Marchfolk v003 family-base freeze report

**Date:** 2026-10-26
**Order:** `reviews/chatgpt-rac-rp3-marchfolk-freeze-and-skarn-propagation-order.md` (85b7c1c), Part A
**Status:** **MARCHFOLK RP3 v003 — AUTHOR ACCEPTED / FROZEN — MPFB FAMILY BASE**

## Freeze method

The freeze is recorded, not written into the files.
- The accepted `.blend` files were **not re-saved**, so they stay byte-identical.
- The authoritative record is `MF_RP3_v003_FREEZE.json`, sha256 `4af62f81ff4ba55e0396f70397e1e4945739353bc7247bc2ded00b6c12d35ba9`. It sits next to the blends in `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Marchfolk/RP3/`; a copy is in `reviews/rac-rp3-evidence/marchfolk_v003_freeze/`.
- The PC read-back of the record is identical.
- The status field in the older sidecar JSONs predates acceptance. The freeze record supersedes it.

## Read-back verification

Both files were re-staged from the PC and opened read-only in Blender (`freeze_check.py`). Reports: `MF_{M,F}_v003_readback.json`.

| Check | `MF_M_REF_RP3_retopo_v003.blend` | `MF_F_REF_RP3_retopo_v003.blend` |
|---|---|---|
| sha256 | `5b793eda…7276` ✔ | `a5d8adfe…c188` ✔ |
| Geometry hash | `64ecbff0…41da` ✔ | `ebf5829d…99d4` ✔ |
| Face topology hash | `68f7b6a9…8262` ✔ | `68f7b6a9…8262` ✔ |
| Verts / quads / quad % | 57,674 / 57,672 / 100 % | 57,674 / 57,672 / 100 % |
| Components / boundary / non-manifold edges / non-manifold verts | 1 / 0 / 0 / 0 | 1 / 0 / 0 / 0 |
| Degenerate faces / normals outward | 0 / yes | 0 / yes |
| UV layer | UVMap | UVMap |
| Blend vs map output | max 6.0e-8 m, faces equal | max 6.0e-8 m, faces equal |
| D1 + D3 validator | **69 / 69 firm PASS** | **69 / 69 firm PASS** |
| Anatomy T-1 / T-2 / T-3 / T-7 | pass | pass |
| Density (9 zones) | pass | pass |
| Face (mouth / orbit rings, corner poles) | 35 / 43 + 43, 0 | 35 / 43 + 43, 0 |

**Maps.**
- hm08 → v003: `bc3b7c54…a17`, identical for both configurations.
- v002 → v003: `0829d1dc…475`.
- Both read back identical.
- The weight, UV and morph transfer paths are carried by these maps.

**Source hashes are unchanged:**
- MF-M-R R-6 `2caaf056…`, build `c5be9ca0…`;
- MF-F-R R-6 `c254fb4b…`, build `252907fd…`.

**Fallback and strict notes, recorded as quality notes and not blocking:**
- thumb_mcp_l (both configurations): `PASS_FALLBACK_CLOSED_RING`.
- shoulder_l / r (configuration 2): `PASS_FALLBACK_DEFINED_SIDES`.
- toe3_j3 l/r (both) and toe4_j2 l/r (configuration 2): `PASS_FALLBACK_DEFINED_SIDES+SCOPED_ADJACENT_DIGIT_POLE`.
- Strict-only:
  - configuration 1: middle and ring MCP l/r;
  - configuration 2: ring MCP l/r.
- Configuration-1 sole lowest point +0.41 mm: accepted.

## What the freeze covers

**Frozen:**
- the common topology;
- the hm08 → family-base map architecture;
- the D1 and D3 validator rules;
- the frame and origin convention;
- the weight, UV and morph transfer methods;
- the loop, density and face base organisation.

**Not frozen:**
- the skeleton and skin weights;
- race branches;
- race anatomy;
- final UV layout and materials;
- creator morphs;
- LODs.

The validator rules are documented in `tools/rac/rp/marchfolk_rp3_v001/validator_v2.py` and in `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md` §6.
