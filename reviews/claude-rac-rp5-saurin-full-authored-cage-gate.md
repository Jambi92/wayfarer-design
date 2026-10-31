# RAC RP5 — Saurin full authored cage: refinement / closure gate

Orders: `reviews/chatgpt-rac-rp5-saurin-full-authored-cage-order.md` (ad9cb85) and `reviews/chatgpt-rac-rp5-saurin-full-cage-refinement-closure-order.md` (f0a2b96).
Evidence: `reviews/rac-rp5-evidence/saurin/full_cage/` (thigh/, closure/). Tools: `tools/rac/rp/saurin_rp5_v002/`.

Nothing is frozen. The canonical W2I6 files are untouched and the accepted tail module is unchanged. No rig, UV, LOD, creator or UE5 work was done, and no other race was started.

## Decision

## SAURIN RP5 FULL AUTHORED CAGE NEEDS REVISION — T-1 maximum (axillary vault 5.1 mm, shoulder–neck slope 3.6 mm vs 3.0), T-2 maxima (head 2.65, hands 2.07, feet 1.92, tail stations 1.77 / 1.86 mm vs 1.5), T-4 residual (641 quads with aspect > 4 outside tip zones; 2.7 % angle outliers), and deformation-ownership steps 3–4 (improved diagnostic weights, topology-only fold test) not yet run

The architecture is retained as ordered: the cage was refined, not restarted. Every median and p95 passes everywhere. The remaining failures are local maxima and quad-shape residuals in named clusters (§2, §3). Each has a bounded correction proposed. No pilot `.blend` files were created, because §22 allows them only after every gate passes.

## 1. Refined cage (`closure/SA_RP5_full_cage_cc4.npz`, sha256 `dc267415…`)

**Mesh**
- 107,532 vertices / 107,530 quads, 100 % quads.
- One closed manifold that includes the tail.
- One face list and one vertex order for c1 and c2, realized by the same barycentric embedding on the shared canonical base face list.

**Route, reproducible with `sa_ccage.py`**
1. Authored coarse cage `sa_design.py`: 1,445 corners / 1,436 quads.
2. Three Catmull-Clark levels.
3. Restricted projection onto `SA_RP5_WORK_v001`, using the nearest-coarse-quad partition and the 2-ring coarse neighbourhood.
4. Relaxation with a coverage pull. Pulled vertices smooth less, and the smoothing rule is shape-improving (quad centroid).
5. The accepted tail module is attached on its 128-vertex root ring.

**Changes against the WIP (f7bbe0b)**
- All near-zero edges are removed (max aspect 1.2e9 → 61).
- Aspect > 4 drops from 789 to 643.
- T-1 max drops from 7.6 to 5.1 mm.
- Feet T-2 max drops from 2.8 to 1.9 mm, and tail stations from 2.9 to 1.8 mm.

**Two trials are recorded and NOT adopted**
- **cc5** (`trial_cc5_axilla_rows_T1-T7.json`): hole rows moved to the vault apex by sections. T-1 max regressed to 6.8 mm, T-7 to 0.9948 and T-4 to 1,505.
- **cc6** (`trial_cc6_quality_phase_T1-T7.json`): final shape phase. T-4 improves to 575 / 2.5 % and head / hands to 1.99 / 1.88 mm, but the axilla regressed to 8.9 mm.

## 2. Gates (`closure/SA_full_cage_T1-T7.json`)

| Gate | SA-M188 | SA-F188 | Result |
|---|---|---|---|
| T-1 median / p95 / max (mm) | 0.067 / 0.454 / **5.08** | 0.067 / 0.453 / **5.01** | max FAIL |
| T-2 head (median / p95 / max) | 0.041 / 0.310 / **2.65** | 0.041 / 0.310 / **2.65** | max FAIL |
| T-2 hands | 0.087 / 0.448 / **2.07** | 0.086 / 0.443 / **2.05** | max FAIL |
| T-2 feet | 0.083 / 0.641 / **1.92** | 0.082 / 0.633 / **1.90** | max FAIL |
| T-2 tail root | 0.080 / 0.359 / 0.96 | 0.084 / 0.367 / 0.94 | PASS |
| T-2 tail stations | 0.056 / 0.311 / **1.77** | 0.056 / 0.310 / **1.86** | max FAIL |
| T-3 stature / bbox | −0.03 mm / ≤ 1 mm | −0.03 mm / ≤ 1 mm | PASS |
| T-5 density | every region below its ceiling (head 0.15 % of stature, hands 0.15 %, feet 0.20 %, trunk 0.48 %) | same | PASS |
| T-6 max | 0.99 mm | 0.98 mm | PASS (none > 1.0) |
| T-7 (tail included) | min 0.9960 | min 0.9964 | PASS |

**T-1 / T-2 clusters** (`SA_full_cage_T1T2_T4_clusters.json`). Every cluster records count, max, p95, anatomy, topology-vs-projection cause and proposed correction.
- **T-1 > 3 mm (7 clusters):**
  - axillary vault, both sides, max 5.1 / 4.8 / 3.8 / 3.2 / 3.1 mm. TOPOLOGY + PROJECTION: the pocket rises 6–10 cm above the hole bottom row inside a fused section, and the cage spans its mouth. Correction: an authored vault patch (an apex corner with its own support ring) plus local sliding. Moving rows by height (cc5) failed.
  - shoulder–neck slope, 3.6 / 3.1 mm. PROJECTION: one support row at u ≈ 160.
- **T-2 > 1.5 mm (40 small clusters):**
  - snout lip crease / nostril pits (15): projection; crease-snapped slit row plus nostril pit rings.
  - toe webs / pads (14): projection; web-corner sliding.
  - thumb base / palm 2:1 row (7): local topology; thumb-base support ring and 2:1 re-phase.
  - body quads at the module root (3): P-row redistribution and sliding.
  - perineum (1): an extra perineal row.

**T-4** (same file, `T4_by_region`)
- 643 quads with aspect > 4, of which 641 lie outside tip zones.
- 2,952 angle outliers (2.7 %); 0 near-zero edges; max aspect 61.
- Concentration by region (aspect > 4 / angle outliers):

| Region | Aspect > 4 | Angle outliers |
|---|---|---|
| palm (2:1 row) | 138 | 533 |
| thumb | 107 | 271 |
| toe web | 90 | 267 |
| orbit | 72 | 544 |
| shoulder | 64 | 140 |
| finger web | 54 | 220 |
| forefoot (2:1 row) | 42 | 285 |
| head | 28 | 72 |
| finger | 24 | 34 |
| toe | 13 | 53 |

- Deformation-critical regions affected: shoulder, thumb, finger, toe. The tip-zone exemption covers only 2 quads, and no tip exemption is claimed for any palm, forefoot or root defect.
- Corrections:
  - redesign the 2:1 rows (re-phase the group corners; move the reduction one ring proximal);
  - make the web quads 2 coarse rows deep;
  - give the orbit fans 8 + 8 rings with a radius-matched phase;
  - apply the cc6 shape phase after the axilla patch.

## 3. Deformation ownership (`SA_full_cage_deformation.json`)

**Scaffold.** Temporary 25-bone LBS with gaussian distance weights (2.5 cm), run on the cage and on the dense working source with the same weights.

**Clean poses (0 cage folds):**
- wrist flex / ext, knee 90 / deep, ankle dorsiflexion, mid-tail bend;
- jaw open: 1 fold on the cage and 1 on the source.

**High-attention poses**
- These still fold on the cage: neck flex 145, shoulder abd90 232–250, shoulder flex 343, elbow 83–142, hip flex 75, trunk twist 68, tail-root vertical 169.
- The dense source folds 15–20× more per pose (sampled at 25 % of its faces).
- Several folds sit far from the moving joint; for example, elbow poses fold in "hip / pelvis". That is a weight-leak signature of the temporary scaffold.

**Classification so far:** WEIGHTING / TEMPORARY SCAFFOLD for the far-field folds, with source / PD-2 involvement at the shoulder, neck and tail root. This is suggestive only. The order's steps 3 (locally improved diagnostic weights) and 4 (topology-only fold test per patch) are not done, so no pose is yet cleared as non-topology. That is part of the blocker.

**Not tested** (no scaffold built): fist / grasp, thumb opposition, toe flex / ext.

## 4. Semantic topology map (`SA_full_cage_semantic_map.json`, `SA_full_cage_face_semantic.npy`)

- 210 traced loops. Each loop is the authored coarse ring carried through Catmull-Clark: each coarse edge becomes an 8-hop fine chain. Loops cut by a hole are recorded as open chains.
- Loops covered:
  - orbit rings and orbit rim;
  - mouth slit plus mouth-support rings, and the jaw-hinge / mouth-corner ring;
  - neck rings;
  - shoulder / axilla hole ring and rows;
  - elbow, forearm and wrist rings;
  - finger MCP base rings, knuckle ring with webs, PIP and DIP / claw-base rings, thumb rings;
  - trunk flex rings and lower-axial rings (tail-hole rows);
  - hip root ring and P4;
  - knee rings, ankle / heel rings;
  - toe MTP base rings, MTP ring with webs, toe IP rings;
  - tail root ring = module ring 0, plus module rings 0–10 and every 10th tail-chain band.
- Face labels include claw cap (1,280 faces), 2:1 reduction row (4,608) and display root (896).
- Topology hash and face-semantic hash are recorded. The map is the same object for c1 and c2.

## 5. Identity metrics (`SA_full_cage_identity_metrics.json`, c1 and c2, source vs cage)

**Cage minus source**

| Metric | SA-M188 | SA-F188 |
|---|---|---|
| Stature | −0.03 mm | −0.03 mm |
| Thorax breadth / depth | −0.6 / −3.1 mm | −0.6 / −0.6 mm |
| Pelvic band | −1.8 mm | −0.1 mm |
| Tail section areas 25 / 50 / 75 % | −0.18 / −0.13 / −0.13 cm² | −0.19 / −0.16 / −0.13 cm² |

**Unchanged by construction:** tail length and ratio, carriage, lower axial trunk, forearm / arm, femur / leg, rostral projection, orbit spacing, ball-line height and claw counts. These metrics are read from the same landmarks, and the cage T-6 fit is within 1 mm.

**Not measured as separate metrics:** structural-ridge readability, plantigrade read and display-root integration. Boards D and I and the semantic labels show them.

## 6. Creator-support diagnostics (`SA_full_cage_creator_support.json`)

**Bodies.** The accepted W2 creator route (`w2i4_drivers/sa_finish.build_f`) was rebuilt in the workspace. It needed the label pickles, the centreline and the PC sculpt modules `wf_saurin_body*.py` (staged read-only). 13 states were built on the shared base face list, and the cage was realized on each by barycentric transfer with no re-fit.

**Results**
- **CONSTRAIN (no flips, fit p95 0.42–0.52 mm, max 4.2–6.6 mm, mostly the same axillary cluster):**
  - Narrow, Broad, Narrow female;
  - lower-trunk −10 %;
  - tails 55 % / 0.83 base, 80 % / 1.22 base, Broad 80 %;
  - minimum composition;
  - statures 168 and Broad 208.
- **FAIL (flipped quads):** high fat (92 flips), high muscle (20), high muscle + fat (150), with edge strain up to 166–202 %. These are the composition offsets, PD-2 territory. Ownership is not yet proven: a source-side fold count per state is still needed.
- **Thinnest margin:** hip / pelvis / shoulder for frame and composition, tail / pelvis for the tail states, ankle / foot for stature.
- **Not run:** orbit spacing −8 / +3 %, ridge lower / upper, display root low / high (W3B head level-set chain), and hand / foot variation (no accepted digit creator control exists to drive).
- **Topology branch:** none indicated by the run states. The composition FAIL must be resolved by the PD-2 ownership check.

## 7. Layered scale-detail prototype (`SA_full_cage_detail_layer.json`)

- **Layer source:** the canonical seed realization (seeds sha `a1d07b8d…`, surfaced float32 sha `7a1b3daa…`, deterministic) transported per point onto a cage-derived surface. The surface is the cage plus 2 Catmull-Clark levels, projected onto the base, with the delta interpolated on the upsampled children.
- **Deviation from the canonical surfaced organism:**
  - median 0.068 mm, p95 0.45 mm, p99 0.76 mm;
  - max 8.4 mm, at the cage's own axillary miss;
  - per-region p95 0.18 mm (hands / head) to 0.55 mm (arms).
- **Field continuity:** field boundaries stay continuous because the delta is interpolated, never re-seeded.
- **Geometric vs displacement / normal:**
  - geometric: macro anatomy and silhouette;
  - displacement / normal: the scale relief (≤ 1.7 mm).
- **PD-1:** cross-state re-realization remains separate.

## 8. PD ownership

| | Topology impact | Status | Owner | Blocks RP5 cage? |
|---|---|---|---|---|
| PD-1 surface transport | none: the layer is transported on top of the cage (§7) | prototype works on c1; cross-state transport not shown | detail-layer pipeline | no |
| PD-2 composition / base inversion | possible: the FAIL creator states fold under fat / muscle offsets | source-side check outstanding | source deformation / creator route | not by itself, but the open check is part of the blocker |
| PD-3 seed validity / resampling | none | unchanged | detail generator | no |
| PD-4 auricular empty-field robustness | none | unchanged | detail generator | no |

## 9. Thigh, boards, immutables

- **Thigh art-pass:** CLOSED and unchanged (`full_cage/thigh/`).
- **Boards** (`closure/sheets/`): B wire, C poles / valence, D head, F shoulders, G hands, H pelvis / tail root, I feet, K c1 / c2, M density.
  - Still missing: A thigh, E neck, J tail, L deviation heatmaps, N layered detail, O worst deformation, P creator states.
- **Immutables** (`closure/immutable_hashes_closure.txt`): 228 / 228 UNCHANGED against the pilot record. The accepted tail module is UNCHANGED (`559565cc…`).

## 10. Next bounded pass

1. Authored axillary-vault patch and shoulder–neck support row.
2. Crease-snapped mouth slit and nostril pit rings.
3. 2:1 palm / forefoot redesign, deeper webs, orbit fans.
4. Rerun the cc6 shape phase, then re-gate.
5. Deformation steps 3–4.
6. PD-2 source-side counts for the composition states.
7. Head creator states.
8. Remaining boards.

STOP FOR CHATGPT REVIEW.
