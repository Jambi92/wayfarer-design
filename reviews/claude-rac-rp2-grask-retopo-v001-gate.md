# RAC RP2 — Grask production retopology v001 — gate

**Date:** 2026-10-24  
**Order:** `reviews/chatgpt-rac-rp2-grask-production-retopology-kickoff-order.md` (61ff0e7)  
**Result:** `GR_U_REF_RP2_retopo_v001` candidate complete — **READY FOR AUTHOR REVIEW** (not accepted, not frozen).  
**Evidence:** `reviews/rac-rp2-evidence/grask_retopo_v001/` · **Tools:** `tools/rac/rp/grask_retopo_v001/`

## 1. Deliverables

| File | Location | SHA-256 |
|---|---|---|
| `GR_U_REF_RP2_retopo_v001.blend` | `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Grask/RP2/` | `82c10a64517860d5fcf835e753cfbdb7f762ab20d23b9bf68a660eb04776ded0` (geometry hash `5ebc7813…6dec`) |
| `GR_U_REF_RP2_retopo_v001.json` (sidecar) | same folder + `evidence/production/` | — |
| `GR_U_REF_RP2_retopo_v001_landmarks.json` | same folder + `evidence/production/` | `a22c3959e544e215d315f3de95288e9b7261272876a907e79e9e8b783ff226d1` |

PC copies were re-read and re-hashed after the copy; they match the cloud originals. One mesh object, transforms identity,
no UVs, no materials. Face attributes `rac_part` / `rac_zone`; edge attributes `identity_loop` and `seam_proposal`;
422 vertex groups `LOOP_*` (tagged identity / deformation loops).

## 2. Source integrity and supersession

- Frozen source: `…/RP2/SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v005.blend`. Opened read-only in Blender 5.2.2 LTS and never saved.
  Before work, on both the PC and the cloud copy: file SHA-256 `7bba8d2d…52ab14` and geometry hash `2697929d…c1d7bc`. **Match.**
  After work: the same hashes on both copies. **Unchanged.**
- Source: 590,764 verts / 1,181,524 tris, transforms identity, stature 218.000 cm, ground z = 0. The fit target `v005.npz` equals the BLEND geometry (max |Δ| 1.2e-5 cm, same triangles).
- **Supersession recorded:** GR5DE3 / MPFB E3 is historical provenance only. Its joints were used as diagnostic landmark seeds, nothing more. **v005 wins on geometry and anatomy.** No RP0 report was rewritten. The earlier RP2 production v001–v006 files are provenance only; none was reused or overwritten.
- Frame note: the production mesh keeps the frozen v005 frame. The v005 pelvis root sits at (0.11, −5.72) cm in plan, not at the contract origin. Re-origining is a fixed translation, so it is deferred to rig prep and left for the author to decide. No anatomy was moved.

## 3. Method (hybrid, anatomy-first)

**No automatic remesher or seed was used.** Every region is an explicitly authored procedural quad cage of about 9.8k quads. The cage is built from labelled v005 sections, then:

1. Catmull-Clark subdivision ×3 (pure quads);
2. guarded projection per part (adjacent parts only where they are closer and the normals agree);
3. normal-ray polish;
4. bidirectional, part-aware crease capture (source points the mesh misses pull in their own-part vertices);
5. local untangling of folds and self-intersections.

| Region | Authored construction |
|---|---|
| Torso / neck / head | 40-column ring tube on horizontal v005 sections from 117 to 216 cm. Under-jaw columns re-spaced by surface arclength. Crown closed with a grid cap |
| Face | 2 inset rings per orbit. 2 inset rings around the lip line (stomion 194.6 cm) |
| Ears | Rectangular head-grid port → 5 crescent x-sections → rim cap aligned along the crescent |
| Shoulder / axilla / girdle | Planar arm-root port loop (6/9/6/9). 14 fan rings hinged on a line through the open arm/torso gap, 7 cm below the armpit apex (no converging slivers). Columns carried forward from ring to ring |
| Elbow / arm | 4 elbow rings (+2.4 / +0.9 / −0.6 / −2.1 cm) and 19 forearm rings. Column continuation with phase-optimal arclength spacing |
| Hands | Palm tube of 13 rings and a thumb split branch. Finger ports share their cleft edges (index 4 wide, others 3). Digit tubes have 3 loops per IP joint and grid tips |
| Pelvis / groin / legs | Crotch split (half ring plus an 11-vertex chain). 34 leg rings, with the knee at 76 / 73 / 71 / 69 / 66 cm |
| Feet | Ankle fan hinged on the ankle-front crease. 6 forefoot planes advance to a toe-web line fitted to the most proximal interdigital slot points. 5 toe ports share cleft edges. Toe tubes have 3 loops per IP joint |

## 4. Topology report

| Item | Value |
|---|---|
| Vertices / edges / faces | 628,738 / 1,257,472 / 628,736 |
| Quads / triangles / n-gons | 628,736 (**100 %**) / **0** / **0** |
| Components / boundary / non-manifold | **1 / 0 / 0** |
| Duplicate faces / coincident verts / degenerate faces | **0 / 0 / 0** |
| Winding / normals | consistent, outward (+129.08 L) |
| Self-intersections (BVH overlap, all face pairs) | **0**; source v005 also has 0 |
| Folded faces (dihedral > 120°, or facing against the source normal) | **0** |
| Stature / bbox | 217.996 cm (Δ −0.04 mm); bbox max Δ 0.05 mm |
| Poles | 166: 104 v3, 28 v5, 34 v6. All are tube-cap, port-corner, inset-corner or web-corner poles (inventory in `reports/pole_inventory.json`, shown in sheet F) |
| T-4 targets: angles 45–135° / aspect ≤ 4:1 | 95.1 % / 98.2 % of quads overall |

Density and quality by zone:

| Zone | Mean edge (mm) | Ceiling (mm) | Angles in 45–135° | Aspect ≤ 4 |
|---|---|---|---|---|
| Head / face | 1.93 | 5.45 | 96.4 % | 100 % |
| Ears | 1.27 | 5.45 | 82.4 % | 99.1 % |
| Hands | 1.26 | 6.54 | 98.8 % | 97.4 % |
| Feet | 1.42 | 6.54 | 98.7 % | 99.6 % |
| Trunk / limbs | 2.66 | 13.08 | 93.3 % | 97.9 % |

T-4 is a target. The quads outside it sit in three places: the ear helix curl, the axillary fan, and the finger and toe web
roots. They are listed in `reports/topology_gate.json` and are not hidden.

**Vertex count justification.** About 629k all-quad vertices is the density at which the large, deeply creased Grask hands and
feet hold T-2. That includes nail rims, web slots of about 1 mm and the hallux–toe-2 cleft. A pure-quad mesh cannot refine
locally, so the body carries the same ×3 level. Every zone stays well under its ceiling. The authored ×1 / ×2 levels are
continuous loop systems (LOD-friendly); no LOD count was set.

## 5. Loop audit (69 joints)

Loops were counted as edges crossed along surface paths on four sides of each joint band. Poles count as "on the crease" when they lie within 2 local loops of the joint plane on the joint's own surface.

| Joint | Required | Minimum found |
|---|---|---|
| Neck | 4 | 13 |
| Shoulder | 5 + axillary fold | 19 (the axilla crease is captured; see C / F2) |
| Elbow | 3 + crease | 7–10 |
| Wrist | 3 | 6 |
| Finger MCP | 3 | ≥ 4 |
| Finger IP | 2 | ≥ 5 |
| Thumb MCP / IP | 3 / 2 | 9 / ≥ 2 |
| Hip / groin / glute | 5 + fold | 15 |
| Knee | 3 + crease | 10 |
| Ankle | 3 | 3–4 on the tightest (anterior) side; 20+ elsewhere |
| Toe joints | 2 | ≥ 2 |

No pole sits within 2 loops of a crease. **All 69 joints pass** (`reports/loop_audit.json`).

Sides merged into a web are reported, not counted: one side of each thumb MCP, the shoulder and the hip. Web-corner poles
next to the short toe-5 IP and the toe-2 MTP sit about 4–5 mm outside those toes' surfaces, on the web.

## 6. Anatomy preservation

**Bidirectional surface deviation** (mm, median / p95 / max):

| Zone | Source → retopo | Retopo → source | Limit |
|---|---|---|---|
| Head / face | 0.027 / 0.128 / 0.42 | 0.000 / 0.040 / 0.31 | T-2 0.3 / 0.8 / 1.5 |
| Ears | 0.043 / 0.227 / 0.49 | 0.000 / 0.059 / 0.51 | T-2 |
| Hand L | 0.010 / 0.064 / 0.47 | 0.000 / 0.026 / 0.55 | T-2 |
| Hand R | 0.010 / 0.064 / 0.38 | 0.000 / 0.026 / 0.67 | T-2 |
| Foot L | 0.013 / 0.070 / 1.07 | 0.000 / 0.035 / 0.64 | T-2 |
| Foot R | 0.013 / 0.070 / 0.67 | 0.000 / 0.034 / 0.49 | T-2 |
| Whole body | 0.012 / 0.074 / 1.07 | 0.000 / 0.031 / 0.80 | T-1 0.5 / 1.5 / 3.0 |

Hands and feet include the digits and nails. No micro-detail exemption was used, so the nails meet T-2 as part of the digits.

**Left / right.** Each side was projected independently and there is no symmetrization. Source → retopo max is 1.07 mm on the left and 0.99 mm on the right, so the source asymmetry is carried within tolerance.

**Silhouette IoU at 3 px/cm, body only (limit 0.995):**

| View | IoU |
|---|---|
| Front | 0.99726 |
| Rear | 0.99726 |
| Profile L / R | 0.99657 / 0.99657 |
| 3/4 views | 0.99799–0.99806 |

**Identity stations** (20 sections and extents: chest, waist, pelvis, glutes, limbs, neck, head, hands, feet, shoulders) differ from v005 by at most 1.13 mm (`reports/identity_stations.json`).

**Landmarks (T-6).** 74 landmarks re-measured on the production mesh with the same methods used on v005.

- Median drift 0.000 mm, max 0.80 mm (crown). **None exceeds 1.0 mm.**
- Methods: `prior-seed+surface-fit` (spine, neck base, head pivot, hips, knees, ankles, sternoclavicular, glenohumeral, elbows), `surface-fit` (crown, acromia, scapular proxies, chin, ears, mouth corners), `manual` (v004/v005 construction joints for wrists, MCPs, tips, thumb CMC, toes; v003 eye centres; estimated jaw hinges).
- Surface-fit features are now measured on area-weighted surface samples and ray / section constructions, so they no longer depend on vertex sampling. The v005 values were regenerated with the same definitions.

**Departure from the old E3 seeds is meaningful and expected,** because v005 changed the anatomy. Departures (cm):

| Landmark | Departure from E3 seed (cm) |
|---|---|
| Glenohumeral | 11.6–12.0 |
| Elbow | 11.9–12.1 |
| Sternoclavicular | 7.5 |
| Hips | 6.9–7.1 |
| Knees | 6.4–7.0 |
| Ankles | 5.6–6.7 |
| Pelvis root | 6.2 |
| Neck base | 5.6 |
| Spine stations | 3.8–5.3 |
| Head pivot | 3.2 |

The v005 elbow sits at z 147.5, where the arm section is narrowest above the forearm mass. The E3 seed is about 12 cm away.

## 7. Scope items

- **UV:** none. Seam plan proposal only (37 seams, `reports/seam_plan_proposal.json`, edge attribute `seam_proposal`):
  - 11 closed seams at segment boundaries: neck, shoulder ports, groin splits, wrists, ankles, ear roots;
  - geodesic seams along the occipital midline, back midline, inner arms, inner legs and medial foot borders;
  - side lines on the digits.
  Likely islands: head, torso, 2 arms, 2 hands, 2 legs, 2 feet, 2 ears.
- **LOD:** none. 422 identity and deformation loops are tagged: orbits, mouth, ear roots, neck, shoulder ports and fans, elbows, wrists, palm and MCP rows, every digit station, groin, hips, knees, ankles, forefoot.
- **Not done, per the stop rule:** rig, skin, creator morphs, UVs and materials, LODs, UE5, other races.

## 8. Visual evidence

| Sheet | Contents |
|---|---|
| `sheets/A_whole_body.png` | Source vs retopo, identical cameras: front, profile, rear, 3/4 front, 3/4 rear, plus silhouette overlays (all 8 views in `silhouettes/`) |
| `sheets/B_head_face.png` | Clay comparison and wireframe for the head and face |
| `sheets/C_girdle_torso_pelvis.png` | Girdle, torso and pelvis comparison |
| `sheets/D_hands.png` | Both hands, clay and wire |
| `sheets/E_feet.png` | Both feet, clay and wire |
| `sheets/F_topology_diagnostics.png` | Tagged loops by family and pole map |
| `sheets/F2_edge_flow_cage.png` | Readable edge flow (×1) for face, shoulder/axilla, elbow, wrist, hand, hip/groin, glute, knee, ankle, foot |
| `sheets/G_deviation.png` + `G2_tables.png` | Heat maps (0–1.5 mm) and tables |

**Visual read.** Side by side, no identity drift is visible, including:

- the heavy brow, narrow eye opening, nose, jaw and ears;
- the girdle slope and shoulder width;
- the chest and abdomen organization;
- the pelvis and glutes;
- joint visibility;
- the thick hands, webs and nails;
- the broad plantigrade feet, toes and nails.

## 9. Acceptance checklist (§22)

| # | Item | Result |
|---|---|---|
| 1 | Correct frozen v005 hash verified before work | **PASS** |
| 2 | v005 unchanged after work | **PASS** |
| 3 | Retopo derives only from v005 anatomy | **PASS** (E3 used only as landmark seeds) |
| 4 | 218 cm stature preserved | **PASS** (Δ −0.04 mm) |
| 5 | Silhouette preserved | **PASS** (IoU ≥ 0.9966) |
| 6 | Head / face preserved | **PASS** (T-2 max 0.42 mm) |
| 7 | Grask front-view identity preserved | **PASS** (sheets A / C) |
| 8 | Girdle slope preserved | **PASS** (shoulder stations ≤ 0.1 mm) |
| 9 | Chest / abdomen organization preserved | **PASS** (stations ≤ 0.15 mm) |
| 10 | Pelvis organization preserved | **PASS** (stations ≤ 0.33 mm) |
| 11 | Joint visibility preserved | **PASS** |
| 12 | Hand scale and anatomy preserved | **PASS** (T-2 max 0.67 mm) |
| 13 | Foot scale and anatomy preserved | **PASS** (T-2 max 1.07 mm) |
| 14 | Ordinary nails preserved | **PASS** (inside T-2, no exemption) |
| 15 | ≥ 98 % quads overall | **PASS** (100 %) |
| 16 | 100 % quads in deformation zones | **PASS** |
| 17 | 0 n-gons | **PASS** |
| 18 | Manifold / watertight / one body | **PASS** |
| 19 | Loop minimums satisfied | **PASS** (69 / 69) |
| 20 | Creator-density ceilings satisfied | **PASS** (all zone means under ceiling) |
| 21 | Pole placement acceptable | **PASS** (none within 2 loops of a crease) |
| 22 | No destructive density transitions | **PASS** (single uniform level; no triangles) |
| 23 | T-1 | **PASS** |
| 24 | T-2 | **PASS** |
| 25 | T-3 | **PASS** |
| 26 | T-6 | **PASS** (max 0.80 mm) |
| 27 | T-7 | **PASS** |
| 28 | Visual author sheet shows no identity drift | **PASS** (pending the author's visual veto) |
| 29 | No catastrophic self-intersections | **PASS** (0 intersections, 0 folds) |
| 30 | Source provenance / sidecars complete | **PASS** |

**RP2 GRASK RETOPO V001 COMPLETE / READY FOR AUTHOR REVIEW**
