# Claude Report — RAC RP4 Cogling Final Author Acceptance / Freeze Closure

**Order:** `reviews/chatgpt-rac-rp4-cogling-final-author-acceptance-freeze-closure-order.md` (3007aba)
**Reviewed commit:** `c800205e4bd8df4b8a854f04d05fd31cebd9e7e2`
**Date:** 2026-10-30
**Mode:** freeze by record only. No geometry, topology, branch, validator or T-7 change, and no production file was rebuilt or resaved.

## Final state

**COGLING RP4 — AUTHOR ACCEPTED / FINAL PRODUCTION FROZEN**

## 1. Freeze record

`reviews/rac-rp4-evidence/cogling/final/COGLING_RP4_FREEZE.json`, promoted from `COGLING_RP4_FREEZE_CANDIDATE.json` (the candidate is retained and its sha256 is recorded in `promoted_from`).
- The record is authoritative over the "CANDIDATE / NOT FROZEN" text embedded in both production files.
- **Frozen:**
  - `CG_M_REF_RP4_v001` and `CG_F_REF_RP4_v001`;
  - `MPFB_COGLING_COMPACT_BRANCH_v001`;
  - c1 `CGJ7` and c2 technical anchor `CGF91-NAT`;
  - minimum `CG76H-NAT` and maximum `CG107-NAT`;
  - `CG76-NAT` as superseded provenance only.

## 2. Hashes (all equal the reviewed values; re-verified)

| | CG_M_REF_RP4_v001 | CG_F_REF_RP4_v001 |
|---|---|---|
| file sha256 | `d605422ebc3cb3f97e4914f35fbf955b7054c4439877b45ee7b42446e7fc62cb` | `9432594a376382c55115b90c98af37fd3a0497dae6f95687f2cd45271d74761b` |
| geometry hash | `7355ca55eb71e4ad2adbc16480fc613fe1be57fd6770cea1884aa910fb6208b1` | `be9396ec7f2707e1d4fadd3fa1457f611f94dc5067ab4141b76ac13c6a07fff3` |

Shared by both references:
- **Face topology:** `a11b8831506519db8ae17ba466540a0cd71faa5d82ca501f53c1fc1d5e3b76dc`. Both have 58,162 V / 58,160 Q (100 % quads), and the c1 / c2 topology is identical.
- **Branch definition:** `75ed801f698e78200c8ac3e2891b7f1d4c0459de4c4e6dc117b8629422965a5f`.
- **Branch map:** `600e30713dea72103d819dec23594625047734a7294ce3e50633d59c0733f9eb`.
- **Landmark files:** the hashes match the candidate record.

## 3. Read-back

I opened both committed `.blend` files fresh in Blender, without saving (`COGLING_RP4_freeze_closure_readback.json`):
- the file sha256 and geometry hash equal the reviewed values;
- faces equal the candidate; max |dV| 3e-8 m;
- 1 component;
- 0 boundary edges, 0 non-manifold edges / vertices, 0 degenerate faces;
- normals outward, 100 % quads, UVMap present.

## 4. Validator — permanent dual record

| Body | Raw authoritative | Author-adjusted |
|---|---|---|
| CG76H-NAT | 65 / 69 | **69 / 69** |
| CGJ7 | 65 / 69 | **69 / 69** |
| CGF91-NAT | 69 / 69 | **69 / 69** |
| CG107-NAT | 65 / 69 | **69 / 69** |

**Exception status:** `PASS_COGLING_TOE_PROBE_GEOMETRY_EXCEPTION`, preserved exactly.
- **Bodies:** CG76H / CGJ7 / CG107 only.
- **Stations:** `toe3_j1_l/r` and `toe4_j1_l/r` only.
- **Conditions:** the five stated ones, namely raw `FAIL_LOOPS`, closed-ring fallback, no crease poles, a size-consistent probe pass, and no foot topology added.

The exception does not reuse the Pipkin label, is not a universal compact-race exception, leaves global D4 unchanged and does not apply to Saurin or any later race. The raw outputs stay unchanged in `validator_raw/`.

## 5. 76 cm T-7 — permanent dual record

`PASS_COGLING_T7_SMALL_BODY_SAMPLING_EXCEPTION`, for CG76H-NAT only.
- **Raw fixed 3 px / cm:** minimum IoU 0.9931 against the 0.995 threshold. The raw failure is retained, and it is the same on v005 and on the branch.
- **Scale-consistent production verdict:** front / rear 0.99735, profiles 0.99804 / 0.99800, PASS.
- **T-1 / T-2:** pass.
- **Other bodies:** ordinary T-7 PASS.

Global T-7 is unchanged, and no geometry was changed to satisfy raster quantization.

## 6. c2 anchor residual

**ACCEPTED C2 TECHNICAL-ANCHOR NARROWER-CORE RATIO RESIDUAL** (`CGF91-NAT`):
- crest / thoracic breadth reads +1.05…+1.21 % against the diagnostic Pipkin c2;
- the crest itself is 5.7–6.1 % narrower and the thorax 6.6–7.2 % narrower than Pipkin c2;
- pelvic vertical / thoracic vertical is −9.8 % and pelvic AP / thoracic depth −4.6 %.

The c2 anatomy was not modified.

## 7. Immutable verification

`immutable_hashes_freeze_closure.txt`: **93 / 93 unchanged vs c800205e**. This covers:
- MPFB Family Base v005;
- frozen Durrim RP4 and frozen Pipkin RP4 (branches and production refs);
- every freeze record: Marchfolk, Sagekin, Fenn, Aelari, Vael, Halvren ×3, Grask, v005, Durrim and Pipkin, plus the Skarn family freeze report;
- the accepted Cogling sources and CG76-NAT provenance;
- the CGF91-NAT anchor;
- the reviewed Cogling final evidence: production files and sidecars, raw validators, the toe / T-7 records, gates, deformation and the candidate record.

No frozen race changed.

## 8. Production copy

Copied to `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Cogling/RP4/`, 13 files:
- both `.blend` files;
- the `.json` sidecars, branch maps, landmarks and read-backs;
- `COGLING_RP4_FREEZE.json` and the closure read-back;
- the branch definition.

**Byte identity was verified:** I staged every file back from the PC, and all 13 sha256 match (`COGLING_RP4_pc_copy_sha256.txt`).

## 9. Accepted notes (in the freeze record)

1. Cogling c1 toe3 / toe4 j1 raw failures are a documented D4 probe-geometry artifact, accepted under the Cogling-specific exception.
2. Cogling and Pipkin keep separate exception records; no universal compact-race exception exists.
3. Global D4 is unchanged.
4. The 76 cm raw T-7 failure is a fixed-raster sampling artifact; the scale-consistent reading is the accepted verdict for that boundary body.
5. Global T-7 is unchanged.
6. The CGF91-NAT crest / thorax ratio inversion is an accepted technical-anchor residual.
7. Cogling sex-related anatomy remains OPEN.
8. `MPFB_COGLING_COMPACT_BRANCH_v001` is Cogling-only and not universal. Its engineering face list matches Pipkin v001, but placement, S weights, branch-map geometry and the toe / T-7 exceptions are Cogling-specific and do not propagate without a later-race gate.

**Deformation and anatomy evidence (accepted):**
- c1 / c2: 18 poses each, no new topology class.
- CG76H / CG107 key poses: no new topology class.
- No grip / fist collapse, long-finger folding class, foot / toe defect or wrist / thumb-web failure.
- T-1 / T-2 / T-3 / T-6 pass.
- Branch T-4 > 4:1 = 0.
- 0 new contact pairs.
- Same-class strain differences are report-only.

## 10. Status / canon / handoff updates

- **`specs/STATUS.md`:** the top entry is now "COGLING RP4 — AUTHOR ACCEPTED / FINAL PRODUCTION FROZEN", and the READY FOR AUTHOR FREEZE entry is marked superseded.
- **`specs/cogling/COGLING_V1.md`:** new RP4 FINAL STATUS block covering the refs, branch, lineage, hashes, dual validator and T-7 records, the c2 residual, scope and the accepted anatomy (not reopened).
- **`specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md`:** a Cogling RP4 section with no carry-forward ID.
- **`reviews/reference-assets/manifest.json`:** a Cogling RP4 production entry.
- **`reviews/claude-session-handoff.md`:** a LATEST entry.

## 11. STOP

- Cogling is closed.
- **Saurin is next, but it is NOT started.**
- No geometry, feet, thumb branch, D4 or T-7 change.
- No rig, creator or UE5 work.

**STOP FOR CHATGPT REVIEW.**
