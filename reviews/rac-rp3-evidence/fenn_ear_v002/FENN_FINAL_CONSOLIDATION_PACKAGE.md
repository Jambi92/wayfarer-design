# Fenn final consolidation package (order 0d9c70b §20; prepared, NOT executed)

Nothing here has been run. It lists exactly what the consolidation / freeze order would do if ChatGPT accepts ear topology v002. Fenn is not frozen.

## 1. Inputs

| Item | Record | Status |
|---|---|---|
| Fenn body architecture | FNL4 (configuration 1), FNF181 (configuration 2) | accepted (orders 57dc328 / 2de0e28) |
| E-A2 pelvis tie | FNF181 skeletal-proxy note | accepted |
| Craniofacial source | `FNL4-CF2`, `FNF181-CF2` (`reviews/reference-assets/manifest.json`, R-6 `b10fb791…` / `3674b724…`) | accepted (order bdcd6a6) |
| Hidden-ear identity | body PASS, face PASS | accepted hard condition |
| Ear geometry | E2 (W1e FN-elven central) | selected (order 0d9c70b §1) |
| Ear topology | `topology/FENN_EAR_BRANCH_TOPOLOGY_v002` + cuff canon v002 | this gate; awaiting ChatGPT |
| Branch map | `mapping/FENN_EAR_BRANCH_MAP_v005_v002` (+ v001 → v002 provenance map) | this gate |
| Body family elsewhere | MPFB Family Base v005 (frozen; unchanged; hashes re-verified) | accepted |
| Validator | D1 + D3 + D4 + D5 + D6 (Sagekin freeze precedent) | to run at consolidation |
| Rig carry-forwards | FENN-CF-1 (configuration-2 mouth corner) | registered, unchanged |

## 2. Proposed final production names

| Configuration | File | Sidecars |
|---|---|---|
| 1 | `FN_M_REF_RP3_v001.blend` | `FN_M_REF_RP3_v001_branch_map.npz` (v005 → branch map, weight / zone proxy rows, provenance), `FN_M_REF_RP3_v001.json` (hashes) |
| 2 | `FN_F_REF_RP3_v001.blend` | `FN_F_REF_RP3_v001_branch_map.npz`, `FN_F_REF_RP3_v001.json` |

Location: `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Fenn/RP3/`. Contents: the CF2 family realization (M_v005 @ CF2 hm08) outside the branch plus the v002 E2 ear branch, both produced by `run_earbranch_v002.sh`. Both configurations come from the same code and parameters; no configuration-specific edits.

## 3. Consolidation steps

1. Re-run `run_earbranch_v002.sh` from clean inputs (canonical cuff band list read-only from `topology/FENN_EAR_BRANCH_CUFF_CANON_v002.json`). Check geometry-hash equality with this gate's records (`geometry/FENN_EAR_BRANCH_GEOMETRY_v002.json`).
2. Write the production blends (`ear_blend.py` frame contract: m, Z up, faces −Y, subject left +X, origin pelvis root on ground). Write the `ear_branch` vertex group, UV placeholder on branch faces (UV out of scope), and the map sidecars.
3. Full validation on both files:
   - integrity / topology (`audit.py` + `ear_audit.py`);
   - validator v2 D1 + D3 + D4 + D5 + D6 (`--d5 --d6-native`);
   - landmarks / face rings / anatomy;
   - RP3 deformation set (`mf_deform.py`) + ear head / neck readiness (`ear_deform.py`);
   - hidden-ear body + face rerun (failure reopens the source, not the ear).
4. Freeze record `FENN_RP3_FREEZE.json` (Sagekin `freeze_check.py` pattern):
   - file and geometry hashes, PC read-back hashes;
   - immutable v005 / CF2 source hashes;
   - topology v002 + map hashes;
   - carry-forward register entries (FENN-CF-1 + anything the final deformation set finds);
   - manifest roles → "frozen reference";
   - `specs/fenn/FENN_V1.md` RP3 status → frozen.
5. Out of scope at consolidation unless ordered: production ear rig / ear movement (FENN_V1 §15), creator morphs, final UV / materials, LODs, UE5.

## 4. Freeze acceptance conditions

- 100 % quads; one component; no boundary; no non-manifold; outward normals; branch adds 0 self-intersections (whole mesh = CF2 v005 baseline).
- Outside-branch vertices byte-identical to the CF2 family realization. Transition-ring displacement bounded (≤ 0.06 cm in this gate).
- Ear mean edge ≤ 0.25 % of stature; no branch quad aspect > 10.
- Root valence 4 on all 52 root vertices.
- Root crease no worse than v001 (this gate: max 64.0° on both configurations; v001 64.6–73.0°, v005 baseline 67.1–71.1°).
- Static head / neck readiness: 0 new self-intersections, 0 flipped branch faces, 0 root inversions.
- Hidden-ear CF2 identity PASS.
- T-4 at or below this gate's v002 level (documented residual).
