# RAC RP2 — Grask production-mesh pilot: technical gate

**Date:** 2026-10-23
**Order:** `reviews/chatgpt-rac-rp2-grask-production-pilot-execute-order.md` (37d657a)
**Executor:** Claude. Autonomous execution; failed internal candidates were repaired before this report.

**Status: RP2 GRASK PRODUCTION PILOT TECHNICAL PASS / READY FOR OWNER VISUAL REVIEW**

## 1. Candidate

| Item | Value |
|---|---|
| File | `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Grask/RP2/GR_U_REF_RP2_production_v001.blend` |
| Companion files (same folder) | `GR_U_REF_RP2_production_v001.json` (sidecar); `…_landmarks.json`; `…_mpfb_mapping.npz` |
| File SHA-256 | `81f579f91b43667143840dbc5e6e41ce7c35c5e326c4669c8e14a896ac219c0a`. Matches the copy read back from the PC (`reviews/rac-rp2-evidence/production/pc_hashes.txt`). |
| Geometry hash | `5806a659ad88ee1082dd792ff5eddbebd0694fed8dc08f1f9bf7e982f0c295d8`: SHA-256 of the float32 vertex array followed by the int32 loop index array, in file order. |
| Object | `GR_U_REF_RP2_production_v001`, the only object. World matrix identity. Blender metres, frame (x, −f, u)/100. Smooth shading; normals outward (signed volume +107.98 L). |
| Counts | 214 146 vertices; 214 144 faces, 100 % quads |
| Source | `reviews/reference-assets/r6/GR5DE3_r6.npz`, sha256 `d859eb18…d778`. Re-hashed before and after; unchanged. |
| Production target | H: Class B regions symmetrized, Class C shoulder/neck base kept (`reviews/claude-rac-rp2-grask-asymmetry-adjudication.md`). |
| Not promoted | Owner visual review pending. No RP3, rig, creator, UE5 or clothing work. |

## 2. Construction (MPFB hm08 plus a Grask branch)

1. **Base.** The shared hm08 body topology (13 380 vertices / 13 378 quads), carrying S* (the bilateral average).
2. **Grask production branch.** It holds 13 386 vertices and 13 384 quads, and adds two things:
   - **Crotch slot.** E3's thigh sheets cross the midline and roof a pocket with the perineal strip. The sheets are labelled by the thigh_l − thigh_r weight and pulled off the midline to |x| ≥ δ. The walls are relaxed in (f, u) and the result untangled. The 16 perineal quads, which are asymmetric in topology, are freed from mirror pairing.
   - **Axilla seam patches, left and right.** The arm and trunk sheets cross at both axillae. They are cut on an envelope, re-joined along a projected crease polyline, then untangled.
3. **Subdivision.** Two levels (×16 quads) to production density.
   - Sub-vertices are snapped to the target outside the contact zones.
   - Patch descendants are projected only along their normals.
   - The clearance band (< 0.4 mm) and interior surfaces are frozen.
4. **Fairing.** Screened adaptive fairing (λ 400, IRLS), so the dense surface does not reproduce the 13k facets as striations. Then patch relax and a final untangle.
5. **Class C restore.** The shoulder, neck and head base is put back as β(z)·(E3 − S*), smoothstep over 167–173 cm. The displacement is low-pass filtered (λ 12) so no facet pattern returns.
6. **Silhouette rim lock.** Vertices whose normals are perpendicular to the front, rear or profile view directions are blended onto the target surface, with a weight that falls off smoothly up to |n·v| = 0.3. This restores the silhouette that fairing had eroded by tenths of a millimetre at the limb rims.
7. **Storage-safe pass.** Contacts are checked on both quad diagonals, in float64 and float32. A 204-vertex Laplacian relax at the two axilla apexes moves vertices by at most 3.75 mm, inside the resolution zone.

**Mapping back to MPFB.** These are mesh attributes, also stored in the mapping file:
- `mpfb_hm08_vertex`: the hm08 19 158-index of each base vertex; −1 for subdivision or branch vertices.
- `rp2_base_vertex`.
- `rp2_base_quad`: the parent branch quad of each production quad, = face index // 16.

Of the 13 386 branch vertices, 13 185 map to hm08 vertices exactly. The other 201 are crotch and axilla branch vertices.

## 3. Gate results (final candidate, re-run on the geometry read back from the saved .blend)

| Gate | Requirement | Result |
|---|---|---|
| Source integrity | Unchanged | sha `d859eb18…` before and after |
| Components / boundary / non-manifold edges and vertices | 1 / 0 / 0 | 1 / 0 / 0 / 0 |
| Genus / Euler | 0 | 0 / 2 |
| Degenerate faces / coincident vertices / unused vertices / directed-edge duplicates | 0 | 0 / 0 / 0 / 0 |
| Hidden shells or duplicates | 0 | 0 (single component, no coincident vertices) |
| **Self-intersections** | 0 | **0**: float64 design data, float32 stored file, and both quad diagonals |
| Outward normals | consistent | Yes; no directed-edge duplicates; volume +107.98 L in the Blender frame |
| Quads overall / in deformation zones | ≥ 98 % / 100 % | 100 % / 100 % |
| T-1 body, both directions | median ≤ 0.5, p95 ≤ 1.5, max ≤ 3.0 mm | prod → ref 0.074 / 0.493 / 1.837; ref → prod 0.084 / 0.608 / 2.287 — **PASS** |
| T-2 head / face | 0.3 / 0.8 / 1.5 | 0.011 / 0.254 / 0.789; 0.007 / 0.292 / 1.269 |
| T-2 hands | | 0.099 / 0.384 / 0.915; 0.114 / 0.494 / 1.368 |
| T-2 feet | | 0.082 / 0.411 / 0.983; 0.098 / 0.546 / 1.147 |
| T-2 girdle / shoulder | | 0.159 / 0.574 / 1.497; 0.178 / 0.667 / 1.182 |
| T-2 visible joints | | 0.133 / 0.510 / 0.952; 0.149 / 0.626 / 1.056 |
| T-2 pelvis | | 0.024 / 0.246 / 0.949; 0.038 / 0.241 / 1.016 |
| T-2 keel / chest | | 0.076 / 0.438 / 0.979; 0.087 / 0.482 / 1.007 — **all PASS** |
| T-3 stature | ± 1.0 mm | −0.43 mm (217.9458 cm vs 217.9887) — **PASS** |
| T-3 bbox | ± 2.0 mm per axis | max 0.61 mm — **PASS**. The lowest point is 0.35 mm above z = 0. |
| T-6 landmarks | ≤ 1.0 mm, none > 1.5 mm | The 104 rig joint heads and tails are carried unchanged: drift 0.000 mm. As a diagnostic, the change in joint-to-surface distance is at most 0.85 mm; none exceeds 1.0 mm. **PASS** |
| T-7 silhouette IoU vs source E3, 3 px/cm, body only | ≥ 0.995 | front 0.9959 / profile 0.9955 / rear 0.9959 — **PASS** |
| Deformation-zone topology audit | §7 loops; poles off crease planes | All 22 joint windows pass (for example shoulders 15/14 loops against 5 required, knees 5 against 3, PIP 9 against 2). No poles within 1.5 cm of the elbow, knee or wrist crease planes; 1 at each ankle. |
| Creator-density audit | §8 ceilings | Face / ears 0.068 % of stature (ceiling 0.25); hands 0.081 (0.30); feet 0.107 (0.30); trunk / pelvis 0.226 (0.60); limbs 0.300 (0.60). All pass. |
| T-4 / T-5 (quality targets) | — | Angles 45–135°: 98.05 %. Aspect ≤ 4: 94.50 %. Poles: 172 valence-3, 168 valence-5+. Loops and density pass. |

**Reference and resolution zones.** T-1 and T-2 are measured against H, the adjudicated target.
- On the reference side, the crotch slot quads and the two axilla patch regions are excluded: these are the source self-intersection geometry, which the order says must not be inherited.
- Production points whose nearest reference face lies in these zones are reported separately: n 7 919, prod → ref median 0.40 / p95 5.72 / max 15.25 mm.
- The deviation map puts everything above 3 mm at |x| ≤ 3 cm, z 110–116 cm, on the pubic-notch and perineal midline.

**Against raw E3, for reference only.** The result is the same except for the effect of the Class B symmetrization: body max 3.23 / 3.11 mm and pelvis max 1.41 / 1.67 mm (`gates/dev_vs_raw_E3_reference_only.json`).

## 4. Self-intersection resolution: what changed

- **Crotch.** E3's crossing thigh sheets become a midline slot.
  - The front-view crotch apex stays at 108.1–108.5 cm (E3 108.2–108.4) at x = ±0.3 cm.
  - Above it there is a closed midline cleft about 1 mm wide, from 108.8 cm up to the perineal roof at 114.1 cm. In E3 the lowest perineal-strip vertex is at 110.15 cm, with the thigh sheets crossing through that space.
  - The cleft shows as a slightly stronger groin and inguinal crease in front close-ups. It is within 3 mm except on the midline.
- **Axillae.** The arm–trunk crossing at both armpits is replaced by a seam patch that keeps the crease line (close-ups in `sheets/sheet_closeups.jpg`).

## 5. Diagnostic deformation (non-canonical)

48 poses were run with DQS on the MPFB joints, using smoothed source weights and per-finger split weights:
- shoulder abduction 45/90, flexion 60, extension 30; elbow 90/120; wrist ±45; fingers half and full curl;
- hip flexion 45/90, abduction 30, extension 15; knee 90/120; ankle dorsiflexion 20, plantarflexion 30; toes 20/30;
- each of the above both sides;
- neck flexion 30, extension 20, turn 45; spine flexion 20, extension 15, twist 25, lateral 20;
- the rig-prep A-pose at 45°.

Results:
- **30 clean, 18 local flexion-crease contact, 0 non-local.** Return to rest is exact (0.000 mm).
- The local contacts are the expected creases: elbow and knee at 120°, hip flexion and abduction, shoulder flexion, finger curls. The deepest is knee flexion 120 at 4.5 mm.
- No pose collapses.
- The diagnostic rig is not promoted.

## 6. Internal candidates rejected

| Candidate | Failure | Fix |
|---|---|---|
| cand_s3 (fully symmetric S*) | T-7 vs E3 front 0.9909 / profile 0.9935; one shoulder line lowered; both girdle slopes changed | The adjudication was refined to a Class C shoulder/neck base (asymmetry report §3). |
| Mean bias correction | No effect. The production was unbiased (median signed offset 0.02 mm). The silhouette loss was rim erosion from fairing. | Rim lock (§2 step 6) |
| Unfiltered hybrid (barycentric E3 − S* displacement) | Brought back facet lumps on the deltoid | Low-pass filter (λ 12) |
| Low-pass λ 30 | T-2 girdle failed (p95 0.93, max 1.72) | λ 12 |
| Hybrid ramp 162–170 cm | 2 self-intersections at the right axilla apex | Ramp moved to 167–173 cm |
| v001 before the storage-safe pass | 4 contacts at the axilla apexes on the other quad diagonal | f32safe relax (§2 step 7) |

## 7. Front-view and multi-view identity veto

Comparison is on identical cameras (`sheets/sheet_identity.jpg`, `sheets/sheet_closeups.jpg`, `sheets/T7_silhouette_diff_*.png`, `gates/stations.json`).

| Identity read | Result |
|---|---|
| Girdle slope | 30.54° / 25.17° against E3 30.96° / 25.17°. Shoulder tops are identical (181.4 / 183.4 cm at x = ±20). |
| Long arm and long shin | Rig joints and limb lengths unchanged. Stature −0.43 mm. Limb silhouettes match within one pixel at 3 px/cm. |
| Visible joint structure | Elbow, knee and ankle silhouettes unchanged. T-2 joints p95 ≤ 0.63 mm. |
| Pelvis organization | Trunk half-widths at z 110 / 120 within 0.1 cm. T-2 pelvis p95 0.25 mm. |
| Chest / abdomen / keel | Profile depths at 120–180 identical to E3. Keel T-2 p95 0.44 mm. The shading band is gone and the keel and flank masses are kept. |

The candidate reads as E3 in every view and does not drift toward a smoother, more human or Aelari-like body. **No veto.**

## 8. Shading-band cleanup audit

The band is the trunk ring at z 120–150, classified B. Shading normals were sampled at 1 899 fixed band points and their mirror images (`gates/shading_geo.json`).

| Measure | E3 | S* | Production v001 |
|---|---|---|---|
| Left/right normal asymmetry, p50 / p95 | 0.46° / 1.61° | 0.00° / 1.15° | **0.00° / 0.34°** |
| Roughness vs 3-cm low-pass normal, p50 | 1.16° | — | 1.38° |

The roughness change is anatomical relief, not added noise: the 13k facet striations are removed by fairing, and the close-ups show no band. **PASS.**

## 9. Bookkeeping

- **Stale GR5DE3 metadata corrected.** In `reviews/reference-assets/manifest.json`, the `accepted` field of GR5DE3, GR5DE3-LOW, GR5DE3N and GR5DE3B is now "STAGE C ACCEPTED / FROZEN DIRECTION", citing the Stage C ruling and closure. The superseded string is quoted for provenance.
- The RP0 inventory report `reviews/claude-rac-rp0-source-inventory-contract.md` §8 item 3 is historical evidence and was left unchanged.
- Evidence: `reviews/rac-rp2-evidence/`. It holds:
  - `tools/`: the full pipeline (`run_all.sh`), plus `hybrid.py`, `rimlock.py`, `f32safe.py`, `export_blend.py` and the gates;
  - `gates/`: JSON for every gate on the final candidate, plus the rejected cand_s3;
  - `sheets/`;
  - `production/`: sidecar, landmarks, PC hashes.

## 10. Owner visual review items

1. The Class C decision: E3's shoulder-line asymmetry is kept and the trunk band and crotch are symmetrized.
2. The crotch midline cleft (§4) and the slightly stronger groin crease.
3. The axilla seam patch.
4. The 0.35 mm ground offset of the lowest point. It is inside T-3; a translation can be applied in a later version if wanted.
