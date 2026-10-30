# Claude Gate — RAC RP4 Cogling Author Rulings + Final Production Candidates

**Order:** `reviews/chatgpt-rac-rp4-cogling-author-rulings-final-production-order.md` (f58dbd9; reviewed 6952ac1)
**Date:** 2026-10-30
**Evidence:** `reviews/rac-rp4-evidence/cogling/final/`
**Tools:** `tools/rac/rp/cogling_rp4_v001/`:
- `run_cg_final.sh`
- `cg_make_prod.py`
- `cg_toe_exception.py`
- `cg_t7_record.py`
- `cg_final_record.py`
- `cg_sheets.py` with `CBDIR=final`

## Result

**COGLING RP4 FINAL PRODUCTION PASS — READY FOR AUTHOR FREEZE**

| §16 condition | Result |
|---|---|
| Adjusted validator 69 / 69 on all four Cogling bodies | yes |
| Raw validator history preserved | yes |
| 76 cm T-7 dual record preserved | yes |
| c1 / c2 production candidates clean | yes |
| Anatomy / firewalls pass | yes |
| Deformation passes | yes |
| Immutable references unchanged | yes |

- **Freeze status:** nothing is frozen. The readiness record is `COGLING_RP4_FREEZE_CANDIDATE.json`, and the status embedded in both production files reads "CANDIDATE / NOT FROZEN".
- **Bit-identity with the reviewed run:** fresh realizations from the committed branch definition are bit-identical to the reviewed 6952ac1 realizations on all four bodies, and so are the final deformation runs.

## 1. Branch and production candidates (§5–§7)

**Branch.** `MPFB_COGLING_COMPACT_BRANCH_v001`, used exactly as reviewed (definition `75ed801f698e78200c8ac3e2891b7f1d4c0459de4c4e6dc117b8629422965a5f`).
- **Uniformity:** the face list and S are identical on all four bodies.
- **Determinism:** a definition rebuild and a re-application are bit-identical.

| | CG_M_REF_RP4_v001 (c1, CGJ7) | CG_F_REF_RP4_v001 (c2, CGF91-NAT) |
|---|---|---|
| vertices / quads | 58,162 / 58,160 (100 % quads) | 58,162 / 58,160 (100 % quads) |
| file sha256 | `d605422ebc3cb3f97e4914f35fbf955b7054c4439877b45ee7b42446e7fc62cb` | `9432594a376382c55115b90c98af37fd3a0497dae6f95687f2cd45271d74761b` |
| geometry hash | `7355ca55eb71e4ad2adbc16480fc613fe1be57fd6770cea1884aa910fb6208b1` | `be9396ec7f2707e1d4fadd3fa1457f611f94dc5067ab4141b76ac13c6a07fff3` |
| face topology hash | `a11b8831506519db8ae17ba466540a0cd71faa5d82ca501f53c1fc1d5e3b76dc` | **identical** |
| branch definition | `75ed801f…` | identical |
| branch-map hash | `600e30713dea72103d819dec23594625047734a7294ce3e50633d59c0733f9eb` | identical |
| landmark hash | `b66d78ef19c8fdfd5be185926e33ff7766acd61bdf500428c191673d55eaf888` | `49a2d8ff8f30f80b9ee0bfdef6e23ac521174d0721d2b10b3ac8895143c8f97f` |

**Face topology is shared with Pipkin.** The face-topology hash equals frozen Pipkin RP4's, because the engineering face list is the same. The vertex placement (geometry, S and branch map) is Cogling-only.

**Read-back** (Blender open, no save; both files):
- 1 component;
- 0 boundary edges, 0 non-manifold edges / vertices, 0 degenerate faces;
- normals outward, UVMap present;
- faces equal to the candidate, and the geometry hash equals the candidate;
- max |dV| 3e-8 m.

**Sidecars.** Each `_branch_map.npz` holds the exact M = S · M_v005, S itself, the identity v005 → production map and the part labels. The `.json` carries the hashes and lineage; `_landmarks.json` holds the landmarks. The thumb vertex group is the only branch group.

## 2. Validator — raw and author-adjusted (§2, §8) — `COGLING_toe_exception_validator_summary.json`

| Body | Raw authoritative (D1+D3+D4+D5+D6) | Exception applied | Adjusted |
|---|---|---|---|
| CG76H-NAT | 65 / 69 | toe3_j1_l / r, toe4_j1_l / r | **69 / 69** |
| CGJ7 (c1) | 65 / 69 | toe3_j1_l / r, toe4_j1_l / r | **69 / 69** |
| CGF91-NAT (c2) | 69 / 69 | — | **69 / 69** |
| CG107-NAT | 65 / 69 | toe3_j1_l / r, toe4_j1_l / r | **69 / 69** |

**Exception status:** `PASS_COGLING_TOE_PROBE_GEOMETRY_EXCEPTION`. This is a separate Cogling record; the Pipkin label was not reused. A station gets it only if all of these hold:
1. The body is CG76H / CGJ7 / CG107.
2. The station is one of the four listed.
3. Raw `FAIL_LOOPS`, closed-ring fallback, no crease poles.
4. The size-consistent probe passes.
5. No foot topology was added: every non-v005 vertex belongs to the thumb patch.

**Unchanged:** no other failure exists, raw outputs stay in `validator_raw/`, and global D4, Pipkin and Durrim are unchanged.

## 3. T-7 dual record (§3, §9) — `COGLING_T7_record.json`

| Body | Raw fixed 3 px / cm (min of front / rear / profiles) | Scale-consistent | Production verdict |
|---|---|---|---|
| CG76H-NAT | 0.9931 (profile), the same on v005 | front / rear 0.99735, profiles 0.99804 / 0.99800 | **PASS_COGLING_T7_SMALL_BODY_SAMPLING_EXCEPTION** |
| CGJ7 | 0.9963 | 0.9969–0.9978 | PASS (ordinary) |
| CGF91-NAT | 0.9960 | 0.9972–0.9975 | PASS (ordinary) |
| CG107-NAT | 0.9957 | 0.9974–0.9976 | PASS (ordinary) |

**The 76 cm exception and its §3 conditions:**
- it applies to the 76 cm body only;
- the raw reading is stored;
- the scaled reading passes;
- T-1 / T-2 pass (body p95 0.09 mm);
- the identical raw IoU on v005 and on the branch shows the failure is not branch-induced.

No other body has a raw T-7 failure, and global T-7 is unchanged.

## 4. Accepted c2 residual (§4)

`CGF91-NAT` crest / thoracic breadth reads +1.05…+1.21 % against the diagnostic Pipkin c2.
- **Recorded as:** ACCEPTED C2 TECHNICAL-ANCHOR NARROWER-CORE RATIO RESIDUAL.
- **Cause:** the thorax narrows more than the pelvis. Crest is −5.7…−6.1 % and thorax −6.6…−7.2 % against Pipkin c2.
- **Still holding:** pelvic vertical / thoracic vertical (−9.8 %) and pelvic AP / thoracic depth (−4.6 %).
- **Unchanged:** the anatomy was not modified, and Cogling sex-related anatomy remains OPEN.

## 5. Anatomy preservation (§10) — source vs production (`CG_final_gates.json`)

| Body | T-1 / T-2 | T-3 (stature) | T-6 max drift | T-7 | Body deviation p95 / max | T-4 branch: > 4:1 / max | Contact new |
|---|---|---|---|---|---|---|---|
| CG76H | PASS | PASS (−0.19 mm) | 0.0007 mm | exception (§3) | 0.09 / 0.81 mm | 0 / 3.82 | 0 |
| CGJ7 | PASS | PASS (−0.23 mm) | 0.0007 mm | PASS | 0.10 / 0.98 mm | 0 / 3.82 | 0 |
| CGF91 | PASS | PASS (0.00 mm) | 0.0006 mm | PASS | 0.09 / 1.00 mm | 0 / 3.82 | 0 |
| CG107 | PASS | PASS (−0.26 mm) | 0.0007 mm | PASS | 0.12 / 1.15 mm | 0 / 3.82 | 0 |

**Thumbs and body T-4.**
- The thumb MCP passes on every body: 3 / 3 on c1 bodies (one side by closed-ring fallback) and 4 / 4 on c2.
- Body T-4 angle flags are 3–4 below v005, and rest self-intersections are unchanged.

**Accepted anatomy unchanged.** The branch only re-samples the v005 surface (a sub-millimetre surface), so none of these change:
- Fine-Scale Elongated Articulation and the narrow stable core;
- near-human total limb contribution;
- distal arm / leg redistribution and the long-finger hand;
- fine shafts and small joints;
- the mature pelvis and adult head;
- the 76 cm adult firewall.

No source anatomy was corrected.

## 6. Firewalls (§11) — `../firewalls/CG_firewalls.json`

These are source readings: production equals source within T-1. Boards CGF_D–H were re-rendered on the final realizations.

| Firewall | Result |
|---|---|
| Cogling vs Pipkin, 91 cm equal height | **14 / 14** (narrower core, finer shaft, distal redistribution, longer fingers / hand share, less pelvis-led) |
| Cogling vs Pipkin, 107 cm equal height | **14 / 14** |
| Cogling vs Pipkin, c2 91 (diagnostic) | 13 / 14 (the §4 residual) |
| Cogling 107 vs Durrim 122, real-height context | **11 / 11** |
| Adult vs child, 76 cm critical (vs toddler ~1.5 y) | **17 / 19**; head share 0.145 vs 0.194 |
| Adult vs child, 91 cm support (vs child ~3 y) | **18 / 19** (c1 and c2) |
| Marchfolk normalized | **11 / 11** on 76 / 91 c1 / 91 c2 / 107; non-uniform scaling |
| Hidden identity, hands hidden | vs Pipkin 11 / 11 (c2 10 / 11, the §4 residual); vs Marchfolk 5 / 5 |
| Hidden identity, head + hands + feet hidden | same as hands hidden; identity does not collapse to long fingers |

## 7. Deformation (§12) — `COGLING_final_deformation_vs_v005.json`

| Body | Poses | Result |
|---|---|---|
| c1 CG_M (CGJ7) | 18 | 13 identical, 5 same class |
| c2 CG_F (CGF91) | 18 | 14 identical, 4 same class |
| CG76H | 15 key | 10 identical, 5 same class |
| CG107 | 15 key | 10 identical, 5 same class |

**No new topology class.** In every pose the self-intersection, fold and flip counts equal v005. The same-class differences are strain-only and report-only: thumb opposition p95 rises and its max falls, the same pattern as frozen Pipkin.

**Specific checks:**
- no grip / fist collapse (fist unchanged);
- no new long-finger folding class (finger topology is v005);
- no new foot / toe defect (toe, ankle and knee poses identical);
- no wrist / thumb-web failure.

## 8. Boards (`final/sheets/`)

| Board | Content |
|---|---|
| CGF_P | Production candidates: 8 views each |
| CGF_C | Bounds 76 / 91 c1 / 91 c2 / 107 |
| CGF_D | Equal-height vs frozen Pipkin, 91 / 107 |
| CGF_E | 107 vs Durrim 122, real height |
| CGF_F | Adult vs child, 76 / 91 |
| CGF_G | Normalized Marchfolk |
| CGF_H | Hidden identity |
| CGF_I | Deformation: fist, opposition, wrist flex, toe extension |

Ears on D–G are flattened by a harmonic fill (board only).

## 9. Immutables (§15) — `immutable_hashes_final.txt`

**74 / 74 unchanged vs f58dbd9.** This covers:
- MPFB Family Base v005;
- frozen Durrim RP4 (branch + production) and frozen Pipkin RP4 (branch + production + `PIPKIN_RP4_FREEZE.json`);
- all 13 freeze records: Marchfolk, Sagekin, Fenn, Aelari, Vael, Halvren ×3, Grask, v005, Durrim, Pipkin, plus the Skarn family freeze report;
- the accepted Cogling sources and CG76-NAT provenance;
- the CGF91-NAT anchor, the Cogling branch definition and the diagnosis toe package;
- COGLING_V1 and PIPKIN_V1.

## 10. Accepted notes (carried into `COGLING_RP4_FREEZE_CANDIDATE.json`)

1. Cogling c1 toe3 / toe4 j1 raw validator failures are a documented D4 probe-geometry artifact, accepted under the Cogling-specific exception.
2. Cogling and Pipkin keep separate exception records; no universal compact-race exception exists yet.
3. Global D4 is unchanged.
4. The 76 cm raw T-7 failure is a fixed-raster sampling artifact; the scale-consistent diagnostic passes and is the accepted production verdict for that boundary body.
5. Global T-7 is unchanged.
6. CGF91-NAT's crest / thorax ratio inversion is an accepted technical-anchor residual: the thorax narrows more than the pelvis, and the narrow-core and less-pelvis-led anatomy otherwise stays intact.
7. Cogling sex-related anatomy remains OPEN.
8. `MPFB_COGLING_COMPACT_BRANCH_v001` is Cogling-only and is not a universal compact-race branch.

## 11. Not done (STOP)

- No freeze.
- No global D4 / T-7 change and no Cogling foot topology.
- No anatomy revision.
- Frozen Pipkin / Durrim untouched.
- No Saurin, rig, creator or UE5.

The production files reach the E: drive only after freeze, matching Durrim and Pipkin.

**STOP FOR CHATGPT REVIEW.**
