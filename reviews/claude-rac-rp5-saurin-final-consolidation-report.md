# RAC RP5 — Saurin final consolidation / freeze-readiness report

Order: `reviews/chatgpt-rac-rp5-saurin-final-consolidation-freeze-readiness-order.md` (cd87d9c).
Approved source: commit `2ee75ae1845a223f3c8b8b9a5abfa10608f06b27`, gate `reviews/claude-rac-rp5-saurin-full-authored-cage-gate.md`.
Package and evidence: `reviews/rac-rp5-evidence/saurin/full_cage/final_consolidation/`.
The approved `optionb_final/` evidence is unchanged, including the pilot files (`git diff 2ee75ae -- optionb_final` is empty).

## SAURIN RP5 FINAL CONSOLIDATION PASS — READY FOR FINAL FREEZE REVIEW

Status of every candidate file: **FREEZE CANDIDATE / NOT FROZEN**. No geometry was changed, and nothing was frozen.

## 1. Clean rebuild (`sa_consolidate.py` → `consolidation_rebuild.json`)

**What "rebuild" means here.** The approved authored cage is fully defined by four things:
- its face list;
- its barycentric embedding on the canonical W2I6 face list (base triangle + barycentrics per vertex);
- the derived working source `SA_RP5_WORK_v001` (canonical arrays + the committed thigh art-pass delta);
- the accepted tail-module block.

The iterative optimisation history that produced the embedding is in the 2ee75ae gate, the tool chain and the session handoff. It was not replayed: the order forbids another geometry-development cycle, and the locked state is reproduced exactly without it.

**Clean workspace** `/tmp/claude-0/rp5clean`. It was built from empty, using only hash-verified inputs:
- **Canonical inputs:** `saurin_w2_final_base.npz` and `saurin_w2_SA-F188_realization.npz` match the recorded sha256 (`f86ae800…`, `8019420a…`). Their arrays match the recorded array hashes.
- **Working source:** `SA_RP5_WORK_v001` was **rebuilt** from the canonical arrays + `thigh/SA_RP5_WORK_v001_delta.npz`. The array hashes equal the recorded `working_array_sha256`: v_M `27e5ed28…`, v_F `4c5bc624…`, f `ae4fb0a9…`.
- **Landmarks, regions and accepted tail module:** copied from the repository. Tail module sha `559565cc…`.
- **Creator-state realisations:** used only as validation inputs. Their hashes are recorded.

**Rebuild vs approved**, using the approved npz read from the git object of 2ee75ae (sha `5a1f7a01…`):

| Check | Result |
|---|---|
| c1 geometry re-derived from the embedding vs the approved V | max \|Δ\| **0.0** (exact) |
| Tail block vs accepted module | 1.7e-13 cm (float noise); faces identical (15,626) |
| Counts | 190,948 V / 190,946 Q, 100 % quads |
| Mesh | closed 2-manifold, consistently oriented, chi 2, no degenerate quad |
| Topology sha256 | `255645a12a8dc59ae8dace55dcf2af2b196a4f5a799fdf425b394b831ffb2d49` (unchanged) |
| c1 / c2 | one face list, one vertex order, one embedding |
| Candidate npz re-read from disk | all 10 approved arrays **bit-identical** (+ a `provenance` field) |

Environment: Python 3.13.18, numpy 2.5.3, scipy 1.18.1, libigl (pip), torch 2.15.0, Blender bpy 5.2.2 LTS (numpy 2.5.4). The rebuild step is fully deterministic: it involves no seeds or optimisation.

## 2. Freeze-readiness validation (`validation/`, rerun on the candidate in the clean workspace)

| Check | Result | vs approved 2ee75ae |
|---|---|---|
| T-1 max c1 / c2 | 2.44 / 2.40 mm PASS | identical |
| T-2 all zones (max 1.32 mm) | PASS | identical |
| T-3, T-5, T-7 | PASS | identical |
| T-6 | 1.03 / 1.02 mm, PASS (tool rule) — accepted residual | identical |
| Host-aware census: inverted / bow-tie / concave / concave deformation-critical | 0 / 0 / 0 / 0 | identical |
| Aspect > 4 outside tip / tail exemptions (c1 and c2) | 0 (max 3.58 / 3.62); min edge 0.15 mm, no collapsed edge | — |
| T-4 angle register | 231 rows (c1 65, c2 166) | **identical file** |
| Deformation, 34 poses | 0 TOPOLOGY poses, 0 topology-only flips | identical JSON |
| PD-2, 19 creator states (incl. 6 head states) | 0 cage-owned flips | identical JSON |
| Direct identity metrics | — | identical JSON |
| Semantic map | 210 loops, face-semantic sha `f750f30e…` | identical (loops, labels, hashes) |
| Accepted tail module | sha `559565cc…`, geometry and faces | unchanged |
| Canonical / accepted immutables | 229 / 229 unchanged | — |

The accepted residuals are carried forward unchanged:
- **T-4 angle register:** `SA_RP5_freeze_candidate_v001_T4_angle_residuals_ACCEPTED.csv` / `.json`. It includes the strong c1 quads 2049, 54957, 83708 and 85405.
- **T-6:** about 1.03 / 1.02 mm.

## 3. Freeze-candidate files and Blender read-back

**Export** (`sa_freeze_candidate_export.py`):
- one mesh object per file, nothing else in the scene;
- mesh data in cm, exactly the approved cage;
- object transform: identity location / rotation, plus the established pilot unit convention, scale 0.01 (cm → m);
- face attribute `semantic`, plus a custom-property table;
- provenance properties and the status `FREEZE CANDIDATE / NOT FROZEN`.

**Read-back** (`sa_freeze_candidate_readback.py`): each file is opened in a fresh bpy process. The read-back was repeated independently by the package verifier. Both files give the same result:

| Item | M (`readback_M.json`) | F (`readback_F.json`) |
|---|---|---|
| Objects | `SA_M_REF_RP5_freeze_candidate_v001` only (MESH, visible, no parent) | `SA_F_REF_RP5_freeze_candidate_v001` only |
| V / Q | 190,948 / 190,946, all quads | same |
| Face list / vertex order / semantic | identical / identical / identical | identical / identical / identical |
| Topology sha | `255645a1…` | `255645a1…` |
| Max vertex read-back error | 7.6e-6 cm (Blender float32 storage) | 7.6e-6 cm |
| Transform | loc 0, rot 0, scale 0.01 (float32 0.0099999998) | same |
| Units | METRIC, scale_length 1.0 | same |
| Modifiers / constraints / shape keys / node groups | none | none |
| Materials / images / libraries / external paths | none (self-contained) | none |
| Mesh attributes | position, semantic, sharp_face (Blender default flat-shading flag; does not change geometry) | same |
| Verdict | **PASS** | **PASS** |

## 4. Package manifest (`SA_RP5_freeze_candidate_v001_MANIFEST.json`)

| File | sha256 |
|---|---|
| `SA_RP5_full_cage_freeze_candidate_v001.npz` | `ca1c635c1c3c234cc675c2471a31cf9646f95b597c0896b93486cd2b57f99839` |
| `SA_M_REF_RP5_freeze_candidate_v001.blend` | `a37cc37723f1a25fed3320c972341883c05e7df30c4f6f44d112746c86880a07` |
| `SA_F_REF_RP5_freeze_candidate_v001.blend` | `fd5dad4f3cc5ba598ba0f2198f062c8845f17f1317e948399398bc8e5c6403d7` |
| `SA_RP5_freeze_candidate_v001_barycentric_map.npz` | `d845c5b1b98989c5896ee666156535000a72c6c29bd13df9fa0a302ea7ec1b8e` |
| `SA_RP5_freeze_candidate_v001_semantic_map.json` | `6a4b462df03a62d1038d2ff219c5a4692975df3f80cf4faa6913767fc1ac32df` |
| `SA_RP5_freeze_candidate_v001_face_semantic.npy` | `ad4570cc3e94240ef54e5508c340b02cc76973465ff8e24c8287b198b2ca9dd9` |
| `SA_RP5_freeze_candidate_v001_T4_angle_residuals_ACCEPTED.csv` / `.json` | `b30e391b…` / `e8ed6193…` |
| `SA_RP5_freeze_candidate_v001_landmarks_SA-M188.json` | `29a21120…` |
| `SA_RP5_freeze_candidate_v001_sidecar.json` | `cbf1b9cb…` |
| `SA_RP5_freeze_candidate_v001_freeze_candidate_record.json` | `7f8dece3…` |

**Freeze-candidate record** (`…_freeze_candidate_record.json`). It holds:
- race Saurin, stage RP5, architecture Option B;
- source approval `2ee75ae…`;
- the cage, topology, M, F, semantic-map, barycentric-map and tail-module hashes;
- immutables 229 / 229;
- the accepted residual references;
- the full gate block;
- generation time and commit;
- status **FREEZE CANDIDATE / NOT FROZEN**.

## 5. Production copy

**PRODUCTION COPY DEFERRED — NO UNAMBIGUOUS APPROVED DESTINATION.**

The repository has no established Saurin / RP5 production-candidate directory. Earlier races keep freeze material under their own review-evidence trees. The canonical PC tree (`E:/UnrealProjects/Wayfarer 5.8/RaceBodies/out`) holds canonical sources, not candidates. No frozen or canonical asset was touched.

## 6. Internal audit (`sa_verify_package.py` → `package_verification.json`: PASS, 29 / 29)

The audit ran as a fresh process, using only the files on disk and the git object of 2ee75ae. It confirmed:
- manifest, sidecar and record hashes match the files;
- candidate arrays are bit-identical to the approved commit, and the topology hash and counts are unchanged;
- the barycentric map equals the embedding;
- semantic labels and loops are identical;
- every validation JSON is identical to the approved evidence (run metadata aside), and the angle-register CSV is byte-identical;
- T-1 to T-7 pass, the census is 0 / 0 / 0 / 0, aspect is 0 with no collapsed edge, deformation shows no topology regression, and PD-2 has 0 cage-owned flips;
- both fresh Blender read-backs pass;
- no file is named or labelled frozen;
- `optionb_final` and the pilot files are unchanged;
- immutables re-hashed 229 / 229, and the tail module is unchanged.

**Tools added:** `sa_consolidate.py`, `sa_freeze_candidate_export.py`, `sa_freeze_candidate_readback.py`, `sa_package.py`, `sa_verify_package.py`.

**Tools changed:** `sa_identity2.py` and `sa_detail2.py` now honour the `SA_W` workspace variable (path only).

**Not done, as instructed:** no freeze or freeze authorisation, no geometry / canon / biology / tail / architecture change, and no rig, UV, LOD, creator, UE5 or other-race work.

The commit that contains the freeze candidates is recorded in the submission commit message and the handoff.

STOP FOR CHATGPT / AUTHOR REVIEW AND EXPLICIT FREEZE AUTHORIZATION.
