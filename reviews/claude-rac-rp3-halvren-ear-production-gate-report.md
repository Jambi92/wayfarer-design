# RAC RP3 — Halvren ear family final production triangulation / shading gate

**Order:** `reviews/chatgpt-rac-rp3-halvren-ear-final-production-triangulation-gate-order.md` (a656750; reviewed commit 9c08cb2).
**Evidence:** `reviews/rac-rp3-evidence/halvren_rp3_ear_production_gate/`

| File | Contents |
|---|---|
| `pre_audit_hashes.json` / `post_audit_hashes.json` | snapshot hashes before / after every test (+ baked triangle hashes) |
| `HV_ear_production_gate_summary.json` | per-mesh summary (HE1 / HE2 / HE3 × c1 / c2 + frozen Fenn / Aelari / Vael c1 baseline) |
| `records/<mesh>_prodtri.json` | full per-mesh audit: rule, every flagged quad (chosen vs alternate), normals / tangents, poses, LOD, FBX, mirroring |
| `baked/<mesh>_TRI-HV1.npz` | the baked diagonal per quad (+ triangle hash): reproduces the exact production surface downstream |
| `boards/PT_A..D` | A triangulation closeups, B / B2 / B3 shading, C pose stress, D LOD |
| `board_pixel_diffs.json` | quads vs triangles vs rebuild pixel differences |
| `production_shading_review.md` | independent blind technical-art review of the boards |

**Tools** (`tools/rac/rp/halvren_rp3_v001/`):
- `hv_ear_prodtri.py` (bpy) — per-mesh audit;
- `hv_ear_prodtri_boards.py` — boards;
- `hv_ear_prodtri_collect.py` — evidence, summary and post-audit hashes.
- `grask_rigprep_v001/render_attr.py` gained opt-in inspection lighting (`RENDER_LIGHTING`, `RENDER_SPEC`; inert by default).

## FINAL DISPOSITION

__DISPOSITION__

## 1. Approved shapes untouched (§1, §3)

- **Snapshot.** The six approved 9c08cb2 realizations (HE1 / HE2 / HE3 on c1 / c2) were copied and hashed before any test (`pre_audit_hashes.json`).
  - HE2 c1 / c2 V hashes `b88da857…` / `eb18b3c7…` equal the HE2 + HR2 freeze record.
- **Validation only.** No vertex position and no quad connectivity was changed: every snapshot re-hashes identical after all tests (`post_audit_hashes.json`: 6 / 6 unchanged).
- Silhouette, length, width, tip, projection, backward angle, helix, concha, lobe, root placement and family ordering are therefore unchanged by construction.
- **Posed positions** for the pose audit were regenerated from the snapshot with the existing `ear_deform.py`. Each `deform.json` is identical to the approved record (8 poses clean, all six).
- **No local geometry correction was needed.** Every fix in this gate is a triangulation or LOD rule (§2, §6), not a vertex edit.

## 2. Production triangulation rule — TRI-HV1 (§4)

Evaluated **once** on the approved rest pose at authoring time, then **baked** into the asset as triangles. It is never re-evaluated per pose or at import.

For each quad (a, b, c, d), split A = (a,b,c)+(a,c,d) [diagonal a–c] and split B = (a,b,d)+(b,c,d) [diagonal b–d]:
1. Take the split with the smaller fold between its two triangle normals, if the folds differ by > 0.5°.
2. Else take the split with the larger minimum triangle angle, if they differ by > 0.5°.
3. Else take the shorter diagonal.
4. Else take the diagonal holding the smallest vertex index.
5. **Intersection validation.** In the ear neighbourhood (14 cm), triangle pairs touching the branch must not cross at rest or in any of the 8 head / neck poses.
   - A quad taking part in a crossing is flipped to its other diagonal, greedily, in frozen quad order.
   - A flip is kept only if the total crossing count over all 9 states drops.
   - Repeat until stable.

Triangles keep the quad winding.

**Why step 5 exists.** The quad audit ignores triangles of vertex-adjacent quads, so a twisted cuff quad can cross its neighbour without being counted. On the baked triangles this is a real crossing.

| Rest-pose crossings | HE1 c1 | HE1 c2 | HE2 c1 | HE2 c2 | HE3 c1 | HE3 c2 | Fenn | Aelari | Vael |
|---|---|---|---|---|---|---|---|---|---|
| fixed a–c split (what a naïve exporter does) | 1 | 0 | **5** | 2 | 0 | 0 | 0 | 1 | 2 |
| TRI-HV1 steps 1–4 | 0 | 1 | 5 | 1 | 0 | 0 | 0 | 0 | 0 |
| **TRI-HV1 (step 5)** | **0** | **0** | **0** | **0** | **0** | **0** | 0 | 0 | 0 |
| step-5 flips | 0 | 1 (cuff) | 3 (cuff) | 1 (cuff) | 0 | 0 | 0 | 0 | 0 |

**Determinism:**
- Steps 1–4 are geometry-only: every quad's choice is identical under all 4 cyclic vertex shifts and under reversed winding (0 mismatches on all 9 meshes).
- Step 5 visits quads in the frozen index order.
- Independent rebuilds produce byte-identical triangles for HE1 / HE3 (closure determinism builds) and HE2 (the ee0e98c freeze build): dV 0.
- Rendered pixels are identical (board B3, max pixel difference 0).

**Flagged quads** (folded = the two splits disagree in orientation, the closure audit metric; or warped = fold across the chosen diagonal > 20°):

| | HE1 c1 | HE1 c2 | HE2 c1 | HE2 c2 | HE3 c1 | HE3 c2 | Fenn | Aelari | Vael |
|---|---|---|---|---|---|---|---|---|---|
| branch quads | 3850 | 3850 | 3850 | 3850 | 3850 | 3850 | 3718 | 3718 | 3850 |
| flagged (folded) | 493 (30) | 485 (27) | 422 (21) | 409 (12) | 407 (28) | 412 (20) | 218 (16) | 208 (12) | 267 (10) |
| max fold across chosen diagonal | 174° | 171° | 154° | 134° | 152° | 158° | **176°** | 160° | 107° |
| max surface deviation chosen ↔ alternate | 0.11 cm | 0.09 | 0.18 | 0.17 | 0.13 | 0.12 | 0.10 | 0.12 | 0.10 |
| min triangle angle (branch) | 4.6° | 4.7° | 5.1° | 5.2° | 3.2° | 4.2° | 5.6° | 7.4° | 6.7° |
| max triangle aspect (branch) | 9.4 | 9.4 | 9.7 | 9.3 | 9.9 | 8.4 | 9.5 | 7.3 | 8.5 |

- Every flagged quad's chosen / alternate diagonal, both fold angles, deviation, min angle / aspect, normal break and vertex-normal imprint are listed in `records/<mesh>_prodtri.json` (`flagged.quads`).
- **Twisted cuff quads.** The quads with a fold > 90° across both diagonals (HE1 16, HE2 5–14, HE3 13, Fenn 9, Aelari 5, Vael 4) are folded in the frozen geometry itself. No diagonal makes them flat.
  - They sit in the cuff band (folded-quad audit of the closure).
  - TRI-HV1 takes the lesser fold.
  - They are the same class as the frozen elf ears (Fenn's worst is 176°).
- **Slivers.** The smallest triangle angles (3.2–5°) are halves of the long, thin cuff / anterior-cavum quads that stay under aspect 10. They are not degenerate: 0 zero-area triangles; for example the HE3 c2 cuff slivers are 0.0014–0.0025 cm² at 4.2–4.4°.
- **Board A** shows the cuff / root, lobe junction and upper helix / tip of each ear as quads, chosen triangles and the alternate diagonal, tinted by fold.

## 3. Normals / tangents / shading (§5)

- **Normals:**
  - smooth angle-weighted vertex normals on the baked triangles (one smoothing group, no split normals);
  - Blender corner normals equal the reference computation within 0.03–0.09° on the branch.
- **Tangents:**
  - MikkTSpace (Blender `calc_tangents`, the Unreal-compatible basis) on a production-like Smart UV Project unwrap. The final production UV is outside this gate.
  - 0 degenerate / NaN tangents on every mesh.
  - 0 vertices with a mixed bitangent sign inside one UV island.
  - Within-island tangent spread per vertex: 12–37° (HE) vs 22–30° (Fenn / Aelari / Vael).
- **Quads vs baked triangles.** Vertex-normal differences between quad-based and triangle-based normals reach 44–88° on single twisted cuff vertices: HE 44–88°, Fenn 78°, Aelari 70°, Vael 25°. Rendered at production scale (board B3), quads and triangles cannot be told apart.
- **Boards:**
  - B: grazing rim light + specular;
  - B2: reflection-stripe matcap;
  - each with seven views per ear and configuration (front 3/4, strict side, true rear 3/4, direct rear, lower-rear 3/4, lower-root closeup, upper helix / tip), plus the frozen Fenn / Aelari / Vael rows under the same rule and light.
- **Visual verdict:** __SHADING__

## 4. Pose stability on the baked triangles (§6)

Posed positions: the 8 head / neck poses, regenerated from the snapshot (identical to the approved deformation records).

| | contacts | triangle inversions | vertex-normal flips | root inversions | baked diagonal changes | flagged-quad max local normal change |
|---|---|---|---|---|---|---|
| HE1 c1 / c2 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 3.8° / 1.8° |
| HE2 c1 / c2 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 9.5° / 9.0° |
| HE3 c1 / c2 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 13.7° / 24.3° |
| Fenn / Aelari / Vael c1 | 0 | 0 | 0 | 0 | 0 | 14.3° / 13.8° / 14.0° |

- The fold count across the baked diagonals is unchanged in every pose (e.g. HE2 c1 14 → 14).
- **"Pose-dependent change of diagonal interpretation"** is excluded by baking. As evidence of why baking is required: re-evaluating any quad rule per pose would change 115–129 HE branch diagonals (67–109 on the frozen elves).
- **HE3 c2, 24.3° (head yaw left).** This is the face-normal swing of two 3–5° sliver triangles of ≈ 0.002 cm² in the cuff band. The smooth vertex normals around them move ≤ a few degrees.
  - No inversion, contact or visible change (board C, worst two poses per ear).
- Worst two poses are head yaw left / right for every ear, including the frozen references.

## 5. LOD (§7)

**LOD-HV1 (production LOD constraint; the source mesh is untouched):** Decimate collapse of the baked triangles with vertex-group weights:
- 0 on the cuff + transition band and its one-ring (root junction protected);
- 0.35 on the lobe zone (auricle sheet below 30 % of the ear height);
- 1 elsewhere (the rest of the sheet and the head decimate normally).

| | 50 %: self-x / drift / root drift | 25 %: self-x / drift / root drift | unconstrained 25 %: self-x / drift |
|---|---|---|---|
| HE1 c1 | 0 / 0.011 / 0 cm | 0 / 0.038 / 0 cm | **10** / 0.072 |
| HE1 c2 | 0 / 0.009 / 0 | 0 / 0.037 / 0 | 0 / 0.039 |
| HE2 c1 | 0 / 0.010 / 0 | 0 / 0.039 / 0 | **4** / 0.058 |
| HE2 c2 | 0 / 0.007 / 0 | 0 / 0.027 / 0 | **2** / 0.032 |
| HE3 c1 | 0 / 0.008 / 0 | 0 / 0.039 / 0 | 0 / 0.039 |
| HE3 c2 | 0 / 0.008 / 0 | 0 / 0.037 / 0 | **2** / 0.039 |
| Fenn / Aelari / Vael c1 | 0 / 0.009–0.012 / 0 | 0 / 0.029–0.032 / 0 | 0 / 0 / **4** (Vael) |

- Every row: 0 non-manifold edges and 0 zero-area triangles in the ear region.
- **Drift:** the max distance from source branch vertices to the LOD surface (silhouette / Hausdorff).
- **Folded-quad regions:** max drift ≤ 0.056 cm. A few LOD faces at twisted cuff quads deviate > 60° from the source's ill-defined normal there (HE 1–11, elves 2–5); no visible change on board D.
- **Why the constraint.** The unconstrained (closure prodcheck) decimation lets the narrow gap between the back of the auricle and the cuff collapse at 25 %, giving back / rim ↔ cuff crossings. This also happens on the frozen Vael ear, so it is a property of the shared cuff, not of HE1–3. LOD-HV1 removes it on every ear and also reduces drift.
- **Why the lobe weight.** Blind shading review round 1 found a V-notch pinch at the top of the HE1 c1 lobe at 25 % (root-only protection). The lobe-zone weight removes it: the lobe matches the source, with no other change (`production_shading_review.md`).

## 6. Export / reload and Unreal-style import sanity (§8)

FBX (Blender exporter, baked triangles, normals, tangent space) → reimport, on all 9 meshes:
- **Triangles:** identical (same vertex order, same loop order).
- **Positions:** |dV| ≤ 8.4e-6 cm (float export precision).
- **Normals:** within 0.03°.
- **Tangents:** recomputed within 0.0002°; bitangent signs identical.
- **Root seam:** 0 boundary / non-manifold edges in the ear region (no seam opens); the ear branch stays one surface with the head.
- **No re-triangulation:** the asset is already triangles, so the importer has nothing to re-triangulate. The surface is the baked one.
- **Mirroring:** on the auricle sheet, 1396 / 1396 left / right quad pairs take the mirrored diagonal (0 mismatches). The cuff transitions are canonical per side, as in the frozen ears, so they are not a mirror pair.

**If the asset were exported as quads**, an importer would triangulate it itself:

| Importer rule | HE branch quads that differ from TRI-HV1 | flagged quads that differ | of which into the folded split | max surface change |
|---|---|---|---|---|
| fixed 0–2 split (FBX-SDK-style) | 1881–1918 | 196–242 | 6–14 | 0.09–0.18 cm |
| BEAUTY | 32–63 | 10–16 | 2–6 | 0.08–0.18 cm |
| SHORT_EDGE | 61–86 | 19–38 | 1–6 | 0.04–0.08 cm |

So the production asset **must be exported as baked triangles** (TRI-HV1, `baked/*.npz`). This also keeps the step-5 crossing fixes.

**Limitation:** Unreal Engine itself is not available in this environment. The Unreal path is emulated by:
- the FBX round trip;
- MikkTSpace tangents;
- smooth normals;
- importer re-triangulation tests.

A UE import of `baked/` triangles with "import normals and tangents" should reproduce this surface. That check is recommended at engine integration.

## 7. Residual acceptance (§9)

| Condition | Result |
|---|---|
| triangulation deterministic | **PASS** — TRI-HV1, order-invariant, rebuild byte-identical |
| chosen diagonal stable | **PASS** — baked; 0 diagonal changes in 8 poses × 6 meshes |
| shading clean | __SHADING_GATE__ |
| deformation clean | **PASS** — 0 contacts / inversions / flips / root inversions on the triangles |
| LODs clean | **PASS** with LOD-HV1 — 0 non-manifold / zero-area / self-intersection at 50 / 25 %, drift ≤ 0.04 cm |
| export / reload stable | **PASS** — FBX exact; tangents deterministic; mirrored diagonals |
| no visible artifact at gameplay / close distance | __VISIBLE__ |

**Local corrections made:** none to the mesh. Rule-level fixes only:
- TRI-HV1 step 5 (5 cuff diagonals flipped across HE1 c2 / HE2 c1 / HE2 c2);
- LOD-HV1 protection.

**Folded quads accepted, not chased to zero.** The residual folded / warped quads (HE 12–30 folded per mesh) are the same class as the frozen Fenn / Aelari / Vael ears (10–16 folded). They triangulate deterministically, stay intersection-free, deform cleanly, LOD cleanly with LOD-HV1, and round-trip exactly.

## 8. Final family hashes and the production triangulation

| Mesh | approved V float32 sha256 (pre = post) | baked TRI-HV1 triangles sha256 |
|---|---|---|
| HE1 c1 | `295e0536e41a…` | `e5e0b66917b0…` |
| HE1 c2 | `fd2a787f5463…` | `e317e3be2c35…` |
| HE2 c1 (frozen) | `b88da8570535…` | `9e18beb9e91b…` |
| HE2 c2 (frozen) | `eb18b3c7feaa…` | `db0bbcdc4e71…` |
| HE3 c1 | `e78ac3f26162…` | `2b767fc4cafc…` |
| HE3 c2 | `19f73c71c9ae…` | `027cea817d1e…` |

Full hashes are in `post_audit_hashes.json`, and the per-quad diagonal choice is in `baked/<mesh>_TRI-HV1.npz`. Downstream must:
- use the baked triangles, or re-run TRI-HV1 including step 5 with the same 8 poses;
- export triangles, with normals and MikkTSpace tangents;
- build LODs with LOD-HV1.

## STOP

STOP FOR CHATGPT REVIEW.
- Validation only: no shape, HR2, firewall or size-floor change.
- No other race or character work was started.
