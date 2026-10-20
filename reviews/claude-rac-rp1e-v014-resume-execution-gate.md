# RAC RP1E — v014 resume-execution gate (order `chatgpt-rac-rp1e-v014-resume-execution-order.md`, 647fa4e)

**Date:** 2026-10-20
**Governing orders:** 647fa4e on top of 913d0e4 (M1 slit band) and dc9d48f (manifold-contact ruling)
**Result line:** **RP1E EXTERIOR PRODUCTION MESH PASS / D-MASK AUTHOR REVIEW REQUIRED**

## Summary

- **The mesh.** v014 is a single closed manifold genus-1 quad mesh with 0 production self-intersections. Every gate item passes on it:
  - production-envelope T-1/T-2;
  - T-3;
  - T-6;
  - T-7;
  - nails 8/8.
- **The handle.** The R-hand B–C visible handle (M1) is kept open.
- **The two D masks** are built, frozen and documented. They are the only surfaces excluded from the envelope metrics: 0.017 % of the source area together.
- **Why the result is "D-mask review" and not a full PASS.** Two decisions about where the D boundary sits are judgement calls (§4.3). I think the author should confirm them before the family pilot.
- **Import.** v014 was imported through the Blender UI as `GO_U_REF_RP1E_retopo_v014.blend` and verified. v009–v013 are unchanged.

## 1. M1 — R-hand B–C visible handle: PASS

| Item | Result |
|---|---|
| Topology | Attempt B pants slit band. Shared 5-vertex crease chain (cage 5384–5388, Blender edge crease 1.0), placed at the traced ~0.7 mm-gap section, mouthward of the zero-gap tip. Explicit wall masks `m1_masks/`. Crease colour 46 / target `tgx_m1p`. |
| Coarse / L1 regional self-x | 0 / 0 |
| L4 (PB_1) regional self-x | 19 |
| Fallback (§3) | Per-wall side-restricted final-resolution reprojection (`crfix.py`). B-side vertices are projected only onto the B-wall mask and C-side vertices only onto the C-wall mask; the crease chain stays one shared chain. 275 vertices moved, max 0.50 mm. |
| Result | Regional self-x 0; hand T-2 max 1.19 mm; slit visibly open; genus 1; no boundary or non-manifold edges. |

## 2. M2–M6 and the remaining Class-A list

### 2.1 Method

All remaining defects were closed at final resolution. This is the direct final-resolution local-patch fallback (913d0e4 §10; dc9d48f §10). Vertex positions only; the topology is the L4 of the v014 cage, unchanged. Every step is bounded to a ball, and its rim welds exactly to the untouched mesh. Three tools were used:

- **`remap.py` — disk remap.** A disk patch of production quads is mapped onto the source region enclosed by its projected boundary, using mean-value Tutte maps.
  - Explicit D faces can be excluded.
  - With `LID`, each hole left by an excluded D face set is capped by a fan lid. The production then closes across the throat as one surface instead of entering the hidden interior.
- **`fixall.py` — collision-free local relaxation.** The vertices of crossing quads are smoothed until the region has no crossings, with no projection (dc9d48f P3).
- **Fit tools.**
  - `fit2.py`: a bounded two-way fit, used on head features.
  - `fit3.py`: a bounded chord-error fit, so that triangle-centroid and edge-midpoint samples lie on the source.
  - `nailsnap.py`: the nails (§3).

Each step was accepted only when its region had 0 self-intersections and no deviation sample above the zone limit in either direction. The step list is in `v014_final/feats*.txt`, `feats1.out`, `feats2.out` and `steps_h.log`.

### 2.2 Starting state and totals

- **Start.** The M1-passing L4 product, after a global side-restricted crossing pass (`fx1`), had 289 pairs in 4 clusters and 32 over-limit source clusters.
- **Final.** 36 247 of 1 427 072 vertices (2.5 %) differ from the stack L4. Median move is small; p99 is 4.3 mm; the maximum is 13.1 mm, at the L axilla slot entry.

### 2.3 Results per feature

| Feature | Fix | Result |
|---|---|---|
| M2 R thumb web/fin (−32.5, −47.0, 104.7) | Remap r 1.1 + relax | Region pairs 0; src→prod 1.16 mm |
| M3 L axilla knob (24.2, −38.7, 143.1) | Remap r 1.4 + relax | Max 4.39 → 0.82 mm |
| M3 L axilla pinch mouth | The visible slot is open (gap 1–3 mm, z 144–145.8 and 147.5–148.6). The production follows it to the void throats, then closes with lids. A 0.5 mm-gap neck at (23.5, −41.5, 145.8) is fused by local relaxation. | Region misses 0 (general zone); pairs 0 |
| M3 z153 surface | Not reopened (already passing) | — |
| M4 ear rims (4 sites) | Remap or two-way fit | Max ≤ 1.47 mm |
| M5 philtrum, upper lip (3 sites), nose fold | Fit / remap | Philtrum 2.57 → 1.36 mm; lip sites ≤ 1.42 mm |
| M6 R axilla A tip (−18.7, −31.3, 141.9) | Remap r 1.5 + relax (194 crossing pairs at the apex also cleared) | Max 4.39 → 2.57 mm (general limit 3.0) |
| M6 natal nub | Remap | 3.55 → 1.52 mm |
| M6 low back (−6.6, −53.1, 105.6) | Remap | 3.05 → 2.12 mm |
| M6 L palm crease | Remap | 2.33 → 1.08 mm |
| M6 R ulnar web | Remap | 3.08 → 1.06 mm |
| M6 L web lobe (39.0, −46.3, 100.6), a 2–3 mm fin | Remap | 3.59 → 0.79 mm; 72 pairs cleared |
| M6 L index web, L webs (tunnel D faces excluded) | Remap | Pairs 18 → 0 |
| M6 toes / feet (7 sites), R toe web | Remap | ≤ 1.49 mm |
| M6 R eye fold and two chord-error spots (prod→src) | Fit | Max ≤ 1.36 mm |

## 3. Nails: 8/8 within ±0.15 mm

- **Tool.** The recovered nail tooling (masks and fitted axes; it reproduces the source tips within 0.003 mm).
- **Before.** v013 nails were −0.12 to −0.71 mm.
- **After the toe remaps** they were −0.006 to −0.32 mm.
- **Free-edge support** (`nailsnap.py`): per nail, the production vertex nearest the frozen source tip is put on the tip and its 1-ring is relaxed onto the source.
  - Moves per nail were 0.07–1.15 mm.
  - No toe or foot length change: T-3 bbox and stature are unchanged.
  - Each tip region has 0 pairs, and its deviation within 0.6 mm is ≤ 0.63 mm.
- **Final:** L1–L4 and R1–R4 all **0.000 mm** (`v014_final/gate/nails.json`). Metadata is in `v014_final/nail_support.json`.

## 4. D masks: exactly two, frozen (`v014_final/D_masks/`)

### 4.1 The masks

| Mask | Seed face | Throat loops | Faces / vertices | Area | Share |
|---|---|---|---|---|---|
| `D_Lhand_tunnel` | 166074 | 2 (13 and 8 vertices) | 229 / 125 | 3.41 cm² | 0.0091 % |
| `D_Laxilla_void` | 263664 | 2 (bands of 41 and 24 faces, at z 145.80 and 147.55) | 144 / 87 | 3.00 cm² | 0.0080 % |

Face ids, vertex ids, boundary loops and info are in `*_info.json`. Section evidence is in `*_sections.png`, with mask faces in magenta and the production in red. Neither mask uses a beam threshold. Both are seeded face-graph floods bounded by explicit throat loops. They do not include the visible mouth, rim, slit walls or silhouette.

**Tunnel.** The tube is about 5 mm across, with a sealed pocket on each side.

- Throat loops: where the source passes through the production envelope at the zero-gap necks of the pocket.
- Flood set: faces enclosed by the envelope and more than 0.2 mm inside it.
- Check: rebuilt identically on the final mesh.
- Every point outside the mask is ≤ 1.58 mm and within the hand_L envelope; all 100 deep misses are inside the mask.

**Void.** This is the axilla contact cavity between arm and torso.

- Throat loops: the outermost planar z-sections in which the cavity is still a separate closed loop.
- Below the lower throat and above the upper throat the cavity is a visible open slot, which the production now follows (M3).

### 4.2 Accounting

- **Raw full-source** src→prod maxima: general 6.71 mm and hand_L 9.81 mm, caused by the D interiors only.
- **Production envelope:** general 2.909 mm and hand_L 1.444 mm.

### 4.3 Points for author review (the reason for this result line)

1. **Two different throat definitions.**
   - Tunnel: throat loops are where the source passes through the production envelope at the zero-gap neck.
   - Void: throat loops are the last closed planar section.
   - Both are explicit, frozen and shown in sections. But the tunnel's boundary is defined relative to the production envelope, not the source alone.
2. **Void throats are capped by lids.**
   - The production closes across each void throat with a lid: one surface spanning the 1–3 mm cavity cross-section, at most about 1.5 mm off the source.
   - This is not a zero-gap shared crease. The finite-gap slot below it is kept open as the order requires.
   - One alternative would be to move the void throats deeper, which needs the production to enter the 1–2 mm cavity.

## 5. Final v014 gate (`v014_final/gate/`)

### 5.1 Topology

| Item | Result |
|---|---|
| Vertices / faces | 1 427 072 V / 1 427 072 faces, 100 % quads |
| Components | 1 |
| Boundary / non-manifold edges | 0 / 0 |
| Euler / genus | 0 / **genus 1** |
| Degenerate faces / loose vertices | 0 / 0 |
| Directed-edge duplicates | 0 (consistent winding; outward in the Blender frame) |
| Production self-intersections (global quad-BVH, all faces) | **0** |

### 5.2 Deviation (mm; median / p95 / max)

| Zone | prod → src | src → prod, production envelope | src → prod, raw full source | Limit |
|---|---|---|---|---|
| general | 0.009 / 0.084 / 2.816 | 0.023 / 0.240 / 2.909 | 0.023 / 0.241 / 6.71 | 0.5 / 1.5 / 3.0 |
| head_muzzle_ears | 0.002 / 0.051 / 1.496 | 0.024 / 0.246 / 1.467 | same | 0.3 / 0.8 / 1.5 |
| hand_L | 0.007 / 0.045 / 1.459 | 0.030 / 0.182 / 1.444 | 0.030 / 0.192 / 9.81 | 0.3 / 0.8 / 1.5 |
| hand_R | 0.005 / 0.050 / 1.376 | 0.032 / 0.161 / 1.335 | same | 0.3 / 0.8 / 1.5 |
| foot_L | 0.007 / 0.053 / 1.218 | 0.014 / 0.114 / 1.381 | same | 0.3 / 0.8 / 1.5 |
| foot_R | 0.006 / 0.058 / 1.220 | 0.018 / 0.147 / 1.494 | same | 0.3 / 0.8 / 1.5 |
| tail_root | 0.006 / 0.033 / 0.281 | 0.017 / 0.061 / 0.239 | same | 0.3 / 0.8 / 1.5 |

**All production-envelope T-1/T-2 pass.** The head prod→src max (1.496) and the general envelope max (2.909) are close to their limits.

### 5.3 Other gate items

| Item | Result |
|---|---|
| T-3 | Stature −0.027 mm; bbox within 0.47 mm (unchanged) |
| T-4 | 91.8 % of quads have all angles 45–135°; 96.5 % have aspect ≤ 4 |
| T-6 (ruled method) | Max 1.122 mm. tail_00 1.122 and tail_05 1.119 are above 1.0 and reported; none above 1.5. All others ≤ 0.79. **PASS** (identical to v013; `neck_min` not computed, as before) |
| T-7 IoU | Front 0.99857, profile 0.99786, rear 0.99859 (≥ 0.995) |
| Nails | 8/8 at 0.000 mm |
| Visual | Source vs v014 renders in `v014_final/visual/v014_vs_source.png` (full body, R hand slit, L axilla, R axilla, head, L hand web). No silhouette change seen; the visual veto is for the author. |

## 6. Freeze and import

### 6.1 Design files (`reviews/rac-rp1e-evidence/designs/`)

| File | Contents | sha256 |
|---|---|---|
| `design_v014.npz` | Cage, 5475 V / 5674 F, genus 1 | a6feb1d6… |
| `design_v014_col.npy` | Cage colours, incl. crease colour 46 | 161dd4ef… |
| `design_v014_crease_edges.json` | Crease edges, weight 1.0 | 53e62d2d… |
| `design_v014_production_L4.npz` | Authoritative final production mesh: the stack L4 of the cage with the final-resolution vertex overrides of §1–§3 | 6db61448… |

**Provenance.** Stack L4 (`sim.py`, `tgx_m1p` targets, XFN 46, CREASE) → crfix → fixall → the local steps listed in `v014_final/`.

### 6.2 Blender UI import (Tyler's PC, Blender 5.2.2, no Python console)

1. Opened `v013.blend` and deleted the cage "Cylinder".
2. File > Import > Wavefront `RP1E_cage_v014_design.obj`; Apply > Rotation. The object is named "Cylinder".
3. File > Import > Stanford PLY with `RP1E_production_v014_part1.ply` and `part2.ply` (defaults).
4. Ctrl+J; Edit Mode; select all; Merge by Distance at **0.000001 m**. This welds only the bit-identical seam duplicates; the minimum vertex separation is 0.0023 mm.
5. Renamed the object to `RP1E_production_v014`.
6. Save As `GO_U_REF_RP1E_retopo_v014.blend` (sha 18df4197…850b).
7. Closed Blender, then closed the Explorer window that was opened to launch it.

**v013.blend was not written** (mtime unchanged).

### 6.3 Verification (`import_v014/verify_v014.json`)

- Cage: index-identical, max 0.00024 mm, faces identical, identity matrix.
- Production: 1 427 072 V, bijective vertex match, faces identical, max 0.00012 mm, identity matrix, no modifiers.
- weldsrc: unchanged (562 265 V).

## 7. Scope

No RP2, no rigging, no creator implementation, no UE5 work.

## 8. Tools (`tools/rac/rp/rp1e/`)

- New: `fit2.py`, `fit3.py`, `feat.sh`, `featfit.sh`, `featfit3.sh`, `runfeats.sh`, `nailsnap.py`, `dflood.py`, `dmask2.py`, `ploops.py`, `mslice.py`, `misses.py`, `p2s.py`, `envstats.py`, `srcgapf.py`, `srcgapr.py`, `pcl2.py`, `l4map2.py`, `regdev2.py`, `regsx.py`.
- Updated: `remap.py` (D exclusion + `LID`), `fixall.py` (`REG` / `EXCL` / `SRC` / plane rules).
