# RAC RP2 — Grask retopology v002 production optimization — gate

**Date:** 2026-10-25  
**Order:** `reviews/chatgpt-rac-rp2-grask-retopo-v002-production-optimization-order.md` (d683312)  
**Result:** `GR_U_REF_RP2_retopo_v002` complete — **READY FOR AUTHOR REVIEW** (not accepted, not frozen).  
**Evidence:** `reviews/rac-rp2-evidence/grask_retopo_v002_optimization/` · **Tools:** `tools/rac/rp/grask_retopo_v002/` (exact sequence in `run_v002.sh`)

## 1. Summary

| | v001 (×3) | **v002 (×2, selected)** |
|---|---|---|
| Vertices | 628,738 | **164,514** |
| Quads | 628,736 | **164,512** (−73.8 %) |
| Triangle equivalent | 1,257,472 | **329,024** |
| Hard-limit quads (angle <20° / >160° or aspect >8) | 712 | **0** |
| Worst angle min / max, max aspect | 1.1° / 179.4°, 30.75 | **20.2° / 160.0°, 7.47** |
| Loop audit | 69/69 | **69/69** |
| Origin | v005 frame (pelvis at 0.11, −5.72 cm) | **pelvis_root projected to ground** |

v002 keeps the v001 architecture. It is a Catmull-Clark ×2 of the same authored cage, with support loops added where ×2 fell below
the joint minimums (§4). It passes every gate in §8 and has no sliver exceptions left to justify.

## 2. Deliverables

All files are in `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Grask/RP2/`, with copies in `evidence/production/`. After the copy, each PC file was re-staged and re-hashed. Every PC copy matches its cloud original.

| File | SHA-256 |
|---|---|
| `GR_U_REF_RP2_retopo_v002.blend` | `49ae8a6e2f2c66e94182a49f6e95103a72730a29120cc541fde74abc5355f55e` (geometry hash `1c2297e4…ba72b14`) |
| `GR_U_REF_RP2_retopo_v002.json` (sidecar) | `2dbd722163c028467f46813946aa84777c03092ec8ab664717bc074479d7684a` |
| `GR_U_REF_RP2_retopo_v002_landmarks.json` | `48887566ce04e8ff9970076aaeb207ba31aec9d8d41f2a17465bd3dfa88a968c` |

Contents of the blend:

- one mesh object `GR_U_REF_RP2_retopo_v002`; location, rotation and scale are identity, and the origin is the production origin;
- all quads, no UVs, no materials;
- face attributes `rac_part` / `rac_zone`;
- edge attributes `identity_loop` (34,688 edges) and `seam_proposal` (3,174 edges);
- 437 vertex groups `LOOP_*`.

Readback: positions agree with the fitted mesh to 2e-5 cm, and the geometry hash is identical.

## 3. Source integrity and ancestry

- **Frozen v005:** `…/RP2/SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v005.blend`.
  - **Before** work, both the PC copy and the cloud copy gave file SHA-256 `7bba8d2d…52ab14` and geometry hash `2697929d…c1d7bc`. **Match.**
  - **After** work, both copies gave the same two hashes. **Unchanged.**
  - The file was only opened read-only and was never saved.
- **v001 preserved:** after the v002 work, the v001 blend, sidecar and landmarks on the PC were re-staged and hashed:
  - blend `82c10a64…`, sidecar `ed579e0b…`, landmarks `a22c3959…`;
  - all three are identical to the v001 deliverables.
  - Nothing named v001 was overwritten. The earlier `production_v001–v006` files were not touched.
- **Ancestry:** v002 uses the v001 cage builder (`build_cage.py` + `cage/hands/feet/ears.py`). The rings, ports, split chains, fan hinge and caps are the same, with extra loops only (§4). v005 is the only fitting target.
- **Common frame:** all shape validation (T-1/T-2/T-3/T-6/T-7, identity, asymmetry) is computed in the v005 frame, with the production-origin translation undone.

## 4. Density study

The full table is in `density_study/density_table.md` and `.json`. Per-candidate reports are in `density_study/L1`, `L2v` and `final`. Visual and wire comparison sheets: `S1_density_visual_1..3.png` (v005 / v001 / ×1 / ×2 / v002; front, profile, rear, 3/4, head, shoulder, hand, foot) and `S2_density_wire.png` (cage / ×1 / ×2 / v002; face, shoulder, hand, groin, knee, foot).

| | ×1 (cage x1) | ×2 raw (v001 cage x2) | **v002 (revised cage x2)** | v001 (x3) |
|---|---|---|---|---|
| Vertices / quads | 39,298 / 39,296 | 157,186 / 157,184 | **164,514 / 164,512** | 628,738 / 628,736 |
| Triangle equivalent | 78,592 | 314,368 | **329,024** | 1,257,472 |
| Mean edge head / ears / hands / feet / trunk (mm) | **8.08** / 4.96 / 5.16 / 5.96 / 10.97 | 3.87 / 2.49 / 2.52 / 2.83 / 5.31 | 3.87 / 2.49 / 2.44 / 2.72 / 5.19 | 1.93 / 1.27 / 1.26 / 1.42 / 2.66 |
| Ceiling (mean) head / ears / hands / feet / trunk | 5.45 / 5.45 / 6.54 / 6.54 / 13.08 | ← | ← | ← |
| T-1 (body max) | FAIL 8.52 | PASS 1.92 | **PASS 1.56** | PASS 1.07 |
| T-2 (identity zones) | FAIL head, ears, hands, foot_r | PASS (max 1.32) | **PASS (max 1.40)** | PASS (max 1.07) |
| T-3 stature / bbox (mm) | PASS −0.30 / 0.22 | PASS −0.08 / 0.11 | **PASS −0.09 / 0.11** | PASS −0.04 / 0.05 |
| T-6 landmark max (mm) | FAIL 10.88 | PASS 0.84 | **PASS 0.84** | PASS 0.64 |
| T-7 min IoU front/profile/rear | FAIL 0.9941 | PASS 0.9953 | **PASS 0.9956** | PASS 0.9966 |
| Loop audit (69 joints) | FAIL (24) | FAIL (7) | **PASS** | PASS |
| Hard-limit quads | 2,571 | 74 | **0** | 712 |
| Quads in 45–135° / aspect ≤4 | 79.3 / 99.5 % | 95.2 / 99.1 % | 94.7 / 98.7 % | 95.1 / 98.2 % |
| Self-intersection pairs | 0 | 0 | **0** | 0 |
| **Verdict** | **FAIL** | **FAIL** | **PASS** | FAIL on the v002 quality rule |

**×1.** It fails the head density ceiling (mean 8.08 mm against 5.45 mm). It also fails T-1, T-2, T-6, T-7 and 24 joint minimums. The face rings, ears, webs and nail rims cannot be held at that density.

**×2 on the unchanged v001 cage.** It passes deviation, but 7 joints fall below their minimums:

- the toe MTP joints;
- the index MCP;
- one side of the shoulder fan.

At ×3, the v001 cage got these minimums only from subdivision density. It also had 74 hard-limit quads.

**Selected: ×2 of the revised cage.** The cage has 10,282 quads (v001 9,824). Loops were added inside the existing architecture:

- 2 palm rings at the MCP row (`UPOST`, 4 → 6);
- a third proximal-phalanx station on each toe (`TOEP1`);
- 2 forefoot planes at the toe-MTP row (`FFW`, 6 → 8);
- 4 shoulder-fan rings (`NFAN` 14 → 18);
- finger proximal stations `FINP1` (stations proximal of the port are dropped, as in v001).

This costs 7,328 quads (+4.7 % over ×2 raw). It is the smallest change that made all 69 joints pass. It adds no poles: 166, the same as v001.

**Mixed / selective density was evaluated and rejected** (`density_study/mixed_estimate.json`). The best case would put the trunk and limb shafts outside every joint band at ×1 and keep the rest at ×2. That gives 109,804 quads (−33 %). But:

1. ×1 already fails T-1 inside those shafts: 3.64 mm at the anterior axillary fold (`L1` deviation). The ×1 portion would have to shrink further.
2. Every ×1/×2 boundary needs a 2:1 transition band. That means about 16 bands across creator-active torso and limb regions, each one a ring of v3/v5 pole pairs. The order excludes density cliffs and uncontrolled poles there.
3. It would put the coarsest mesh exactly where the muscularity, composition and frame morphs act.

Since ×2 passes with uniform density, the mixed variant was not built.

**Justification of the count.**

- **Floor:** 164,512 quads sits one subdivision level above a candidate that fails on anatomy (×1).
- **Over ×2 raw:** it adds only the loops the joint audit requires.
- **Against v001:** the reduction is 73.8 %.
- **Density margins:** mean edge is 29–62 % under every creator ceiling (head 3.87 against 5.45 mm; trunk 5.19 against 13.08 mm).
- **Creator readiness:** that margin leaves room for the creator range and for LODs to be generated downward.

## 5. Quad-quality repair (T-4)

| Zone | v001: in 45–135 % / min° / max° / max aspect | **v002** |
|---|---|---|
| Head / face | 96.4 / 21.3 / 159.3 / 3.49 | 95.9 / 20.2 / 159.8 / 3.26 |
| Ears | 82.4 / 12.2 / 166.7 / 5.80 | **84.3 / 23.2 / 159.6 / 4.35** |
| Hands | 98.8 / 3.7 / 173.3 / 30.75 | **98.9 / 20.2 / 159.8 / 6.34** |
| Feet | 98.7 / 1.1 / 179.4 / 15.58 | **99.0 / 21.8 / 159.9 / 4.18** |
| Trunk / limbs | 93.3 / 2.9 / 174.6 / 7.45 | 92.4 / 20.2 / 160.0 / 7.47 |

Aspect ≤4, v001 → v002:

| Zone | v001 | v002 |
|---|---|---|
| Ears | 99.07 % | 99.90 % |
| Hands | 97.35 % | 99.44 % |
| Feet | 99.58 % | 99.99 % |
| Trunk | 97.94 % | 97.89 % |
| Head | 100 % | 100 % |

**How the slivers were removed.** Most of them were rows of quads that crease capture had pulled into a narrow cleft (web floors, the hallux–toe-2 crease, the ring/pinky web), or valence-6 web saddles squeezed into a slot. The repair sequence:

1. **`CLPUSH`:** the cage pulls the dorsal and plantar web caps toward the cleft floor, so fewer rows enter the slot.
2. **`centfix`:** quads whose centre floats off v005 across a crease are pulled onto the surface.
3. **`qopt` recipe, then `revsx`:** quads are optimised, and any move that created a self-intersection is undone.
4. **`lrepair`:** patch smoothing, with at most 0.15 cm off the surface and a deviation guard.
5. **`optfix`:** the last four web-root clusters are optimised directly, staying within 0.30 mm of the surface.

These are:
- the toe-4/5 web on the right (a valence-6 saddle, 4.1° → 25°);
- the hallux–toe-2 crease on the left (10.4° → 25.7°);
- the index–middle web on both sides (12.9° and 14.8° → 25°).

`Q1_quad_quality_repairs.png` shows v001 against v002 for the ear, axillary fan, shoulder, index–middle web, thumb web, toe web, hallux–toe-2 crease and groin.

**Exceptions — none against the hard limits.**
- 0 quads below 20° or above 160°.
- 0 quads with aspect >8.
- No 10:1 aspect quad anywhere.

**Remaining soft-target extremes.** These are within the hard limits, are listed in `quad_quality/worst_remaining_quads.json`, and are shown in `Q2_worst_remaining_quads.png`.

| Quad | Where | Value |
|---|---|---|
| 87307 | right lateral heel edge (−10.7, −10.5, 3.2) | 22.0° / 160.0° |
| 20 | sacral midline (0.2, −11.6, 115.8) | 21.6° / 159.9° |
| 118592 | right hallux–toe-2 crease | 24.8° / 159.9° |
| 98430 | left posterior axillary fan (19.5, −11.3, 153.4) | aspect 7.47 |
| 47411 | left posterior axillary fan | aspect 6.99 |
| 27926 | right posterior axillary fan | aspect 6.69 |
| 30562 | right ring–pinky web, palmar | aspect 6.34 |

The axillary fan strips are the fan-hinge columns of the approved shoulder architecture. They run along the axillary fold, not across a joint crease, and the shoulder loop count is 9–10 against a required 5. Shortening them would mean moving the hinge or adding a second fan, which changes the approved v001 shoulder flow.

The ears sit at 84.3 % inside 45–135°, up from 82.4 %. The rest are the helix and antihelix crescent sections, which bend sharply. Their worst quad is now 23.2° / 159.6°.

## 6. Production origin correction

Record: `reports/origin_correction.json`.

| | Analysis cm (x, f, u) | Blender m |
|---|---|---|
| Old origin | (0, 0, 0) of the v005 frame | (0, 0, 0) |
| Pelvis root, measured on v002 | (0.11180, −5.72272, 123.928) | (0.001118, 0.057227, 1.23928) |
| Pelvis root, v005 | (0.11168, −5.72153, 123.928) | — |
| **Translation** | **(−0.11180, +5.72272, 0)** | **(−0.001118, −0.057227, 0)** |
| New origin, in the old frame | (0.11180, −5.72272, 0) — the pelvis root on the ground | — |
| Pelvis root after | (0, 0, 123.928) | (0, 0, 1.23928) |
| Bbox after | x −36.053…34.995, f −14.622…31.856, u 0.0014…217.993 | x −0.3605…0.3499, y −0.3186…0.1462, z 0.0000…2.1799 |

The correction is one rigid translation: no rotation, no scale, and no change to any individual vertex (every vertex moved by exactly the same vector, to within 1.8e-14 mm).

- **Ground and stature:** the ground is still u = 0, because there is no vertical component. Stature is unchanged at 217.991 cm.
- **Inter-landmark distances:** all 2,701 pairs across the 74 landmarks keep their distances (max change 2.8e-13 mm).
- **Source untouched:** v005 was not moved.
- **Landmark package:** it carries the production frame, the Blender frame and the source frame for each landmark.

## 7. Topology

Gate: `reports/topology_gate.json`.

**Counts and integrity.**
- 164,514 verts, 164,512 faces; **100 % quads**; 0 triangles; 0 n-gons.
- 0 boundary edges, 0 non-manifold edges, 0 winding-inconsistent edges; 1 component.
- 0 unused vertices, 0 duplicate faces, 0 coincident vertices, 0 degenerate faces.
- Outward normals, volume 129,026 cm³.

**Surface health.**
- Self-intersection: **0 pairs**.
- Folded edges (>120° dihedral): **0**.
- Flipped faces: **0**.

**Deformation loops.** Audit `reports/loop_audit.json`: **69/69 pass** and no pole lies within 2 loops of an audited crease.

| Joint | Loops in band (required) |
|---|---|
| Neck | 8 (≥4) |
| Shoulder L / R | 10 / 9 (≥5) |
| Elbow | 6 / 6 (≥4) |
| Wrist | 3 / 3 (≥3) |
| Hip | 8 / 8 (≥5) |
| Knee | 5 / 6 (≥4) |
| Ankle | 7 / 6 (≥3) |
| Finger MCP | ≥3 (≥3) |
| Finger IP | ≥2 (≥2) |
| Toe joints | ≥2 (≥2) |

The tagged face rings (orbits, mouth) and the jaw support are carried over from v001.

**Poles.** Inventory `reports/pole_inventory.json`; labelled wires in `pole_audit/` and `P_pole_audit.png`.
- 166 poles: v3 104, v5 28, v6 34 — the same set as v001.
- **Where they come from:** all are authored-cage construction poles: tip and nail caps (v3), web-saddle forks (one v6 per web), fan and port corners.
- **Web spaces:** no high-valence cluster.
- **Density transitions:** none exist, because the subdivision is uniform.
- **Inside a joint band, but more than 2 loops from the crease:** 2 poles, at thumb_mcp_r and toe5_j1_r.

## 8. Validation

All measurements below are in the v005 frame, in mm; tables in `reports/deviation.json`.

**T-1 / T-2 deviation.** Limits: T-2 0.3 / 0.8 / 1.5 for head, ears, hands and feet; T-1 0.5 / 1.5 / 3.0 for the body.

| Zone | source → v002 (median / p95 / max) | v002 → source (median / p95 / max) |
|---|---|---|
| Head / face | 0.061 / 0.267 / 0.740 | 0.000 / 0.126 / 0.604 |
| Ears | 0.087 / 0.316 / 0.792 | 0.000 / 0.184 / 0.687 |
| Hand L | 0.027 / 0.161 / 1.405 | 0.000 / 0.095 / 0.823 |
| Hand R | 0.028 / 0.155 / 1.192 | 0.000 / 0.095 / 0.979 |
| Foot L | 0.035 / 0.163 / 1.099 | 0.001 / 0.114 / 0.695 |
| Foot R | 0.035 / 0.159 / 1.282 | 0.001 / 0.112 / 0.559 |
| Whole body | 0.032 / 0.168 / 1.561 | 0.000 / 0.096 / 0.979 |

- Hands, feet, toes and nails all sit inside T-2. No micro-detail exemption was used.
- Where the whole-body max occurs:
  - 1.56 mm at the left posterior axillary fold (19.6, −5.0, 167.2), in a T-1 zone;
  - the girdle and chest identity stations agree within 0.3 mm (see Identity below);
  - p95 there is 0.17 mm.

**T-3.** Stature −0.087 mm; bbox max per-axis 0.112 mm; both with the production translation undone. **PASS.**

**T-6.** 74 landmarks; median 0.00 mm, **max 0.84 mm** (mouth_corner_l); **none >1.0 mm.** **PASS.**

- **Method change (v002):** surface-fit features are now measured on dense area samples, about 1.2 mm apart, instead of raw triangle centroids. The new method was applied equally to v005, v001 and v002, and the v005 values were re-measured (`reports/v005_source_landmarks_dense.json`).
- **Why it was needed:** with centroids, the flat back-summit `scapular_inferior_proxy_l` jumped 3.2 mm on the coarser ×2 facets, although the surface there is within 0.28 mm.
- **v001 under the new method:** max 0.64 mm, so the change does not favour v002.

**T-7.** Silhouette IoU at 3 px/cm:

| View | IoU |
|---|---|
| Front | 0.9961 |
| Rear | 0.9961 |
| Profile L | 0.9956 |
| Profile R | 0.9956 |
| 3/4 views | 0.9966–0.9968 |

**PASS** (≥0.995).

**Identity.** `reports/identity_stations.json`, 20 stations.
- Chest at the axilla and at the nipple, waist, iliac pelvis, hip/glute, limbs, shoulder extents: all within 0.67 mm.
- Neck width: −0.31 mm.
- Head brow: perimeter −2.37 mm on a 79.8 cm section (−0.3 %), width −0.27 mm. This is the chord effect of a half-density mesh over the brow rugosity; the brow, orbit and nose read the same in `B_head_face.png`.
- Head extent: within 0.8 mm.

**Asymmetry.** `reports/left_right_asymmetry.json`. Mirrored source points measured against v005 and against v002 give the same statistics: median 2.43 / 2.44 mm, p95 9.48 / 9.49 mm, max 41.36 / 41.41 mm. The accepted source asymmetry is preserved, with no symmetrisation.

**Visual veto.** Sheets A–G (whole body, head/face, girdle/torso/pelvis, hands, feet, topology, deviation) and S1: v002 is indistinguishable from v005 at every camera.

- **Head and face:** brow, narrow eye opening, nose, jaw and ears hold.
- **Hands and feet:** digit hierarchy, webs and nails hold.
- **Girdle:** the slope and the chest keel hold. **PASS.**

## 9. Tool and method changes since v001

Each change is applied identically to every candidate and re-scored on v001.

- `gate.py` — the density pass now applies the contract ceiling as a maximum **mean** edge length (the order's rule); p99 is still reported. v001 passes under both.
- `loopaudit.py` — loop count = max(closed-ring trace, min-over-sides surface-path count). The path-only count of v001 under-counted oblique loops at ×2, for example at the index MCP where palm rings meet the finger axis at an angle. v001 passes 69/69 under the new count (`density_study/final/final_loops_audit_v2method.json`).
- `lm.py` — dense area sampling (see T-6).
- New tools:
  - `symm.py`, `origin.py`, `poleaudit.py`, `density_table.py`;
  - `centfix.py`, `lrepair.py`, `revsx.py`, `optfix.py`;
  - `crease.py` options `CGUARD` and box-restricted relax.

## 10. Evidence index

Everything below is under `reviews/rac-rp2-evidence/grask_retopo_v002_optimization/`.

**Sheets (`sheets/`)**
- `A_whole_body`, `B_head_face`, `C_girdle_torso_pelvis`, `D_hands`, `E_feet`, `F_topology_diagnostics`, `G_deviation`
- `S1_density_visual_1..3`, `S2_density_wire`
- `Q1_quad_quality_repairs`, `Q2_worst_remaining_quads`
- `P_pole_audit`

**Reports (`reports/`)**
- `topology_gate`, `deviation`, `loop_audit`, `landmark_drift`, `identity_stations`
- `silhouette_iou`, `left_right_asymmetry`, `origin_correction`, `pole_inventory`
- `seam_plan_proposal`, `tagged_identity_loops`, `v005_source_landmarks_dense`
- `blend_readback.txt`, `source_integrity.txt`, `folds.txt`, `self_intersections.txt`

**Density study (`density_study/`)**
- `density_table.md` / `.json`, `mixed_estimate.json`
- per-candidate reports for ×1 (`L1`), ×2 raw (`L2v`) and v001 (`final`)
- wire crops

**Quad quality and poles**
- `quad_quality/`: hard-limit list (empty), worst remaining quads, repair crops
- `pole_audit/`: labelled crops

**Silhouettes and wireframes**
- `silhouettes/`
- `wireframes/`

**Production (`production/`)**
- the sidecar and the landmarks file

## 11. Acceptance checklist (§22)

| # | Item | Result |
|---|---|---|
| 1 | Frozen v005 hash verified before | **PASS** (PC + cloud `7bba8d2d…` / `2697929d…`) |
| 2 | Frozen v005 unchanged after | **PASS** |
| 3 | v001 preserved | **PASS** (PC hashes identical) |
| 4 | v002 derived from v001 architecture + frozen v005 shape | **PASS** |
| 5 | ×1 tested | **PASS** (fails anatomy → rejected) |
| 6 | ×2 tested | **PASS** |
| 7 | Mixed / selective density evaluated | **PASS** (estimated −33 %; rejected, §4) |
| 8 | Lowest practical passing density | **PASS** (×2 + required support loops) |
| 9 | Final count materially justified | **PASS** (§4) |
| 10 | Triangle-equivalent reported | **PASS** (329,024) |
| 11 | Stature preserved | **PASS** (−0.087 mm) |
| 12 | Silhouette preserved | **PASS** (IoU ≥0.9956) |
| 13 | Head / face preserved | **PASS** (T-2 max 0.74 mm) |
| 14 | Grask front-view identity | **PASS** (sheet A, S1) |
| 15 | Girdle slope | **PASS** (shoulder extents ≤0.26 mm, sheet C) |
| 16 | Torso / pelvis organization | **PASS** (stations ≤0.67 mm) |
| 17 | Hand anatomy | **PASS** (T-2 max 1.41 mm) |
| 18 | Foot anatomy | **PASS** (T-2 max 1.28 mm) |
| 19 | Nails | **PASS** (inside T-2, no exemption) |
| 20 | Accepted asymmetry | **PASS** (§8) |
| 21 | ≥98 % quads | **PASS** (100 %) |
| 22 | 100 % quads in deformation zones | **PASS** |
| 23 | 0 n-gons | **PASS** |
| 24 | Manifold / watertight | **PASS** |
| 25 | Loop minimums | **PASS** (69/69) |
| 26 | Creator density | **PASS** (all zones under mean ceilings) |
| 27 | No destructive density transitions | **PASS** (uniform ×2) |
| 28 | Pole placement | **PASS** (0 on creases, 0 web clusters) |
| 29 | Extreme slivers corrected or justified | **PASS** (0 hard-limit quads) |
| 30 | T-4 materially improved from v001 | **PASS** (712 → 0 hard; worst 1.1° → 20.2°; aspect 30.8 → 7.5) |
| 31 | Pelvis-root origin by rigid translation only | **PASS** |
| 32 | Ground / stature / inter-landmark distances preserved | **PASS** |
| 33 | T-1 | **PASS** |
| 34 | T-2 | **PASS** |
| 35 | T-3 | **PASS** |
| 36 | T-6 | **PASS** (max 0.84 mm) |
| 37 | T-7 | **PASS** |
| 38 | Zero catastrophic self-intersections | **PASS** (0 pairs) |
| 39 | Visual veto | **PASS** |
| 40 | All evidence / sidecars complete | **PASS** |

## 12. Not done (per order)

- No freeze, rig, skin weights or creator morphs.
- No UVs or materials: there is a seam proposal attribute only.
- No LODs.
- No UE5 export.
- No other race.

**STOP FOR TYLER / CHATGPT REVIEW.**
