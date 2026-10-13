# RM-OT-05Q patch plan (committed BEFORE any mesh edit)

This plan is for a source-surface feasibility study only. It covers one local patch on a duplicate of the source surface.

It does not accept Gorrund, source muscularity, the paws or the garments. RD1–RD4 stay frozen, and RD4 is rejected.

## Inputs (hashes)

| Item | Value |
|---|---|
| Source GLB | `base.glb`, sha256 `78ecfa87d169380ecb46ece3f0c0df3491d10e4547038a3c35c06df933f38a7b`, 43,012,652 bytes |
| F1 face-index list | `source/F1_face_indices.npz`: 140,960 GLB faces, index sha256 `f1b46e6b…9f72` |
| Working copy | `source/F1_working.obj` (gz in repo), sha256 `17591025c24fd080e7fd45e3dc88dccc4707a0bee9efcb3fd70ef5ab6da453b0` |

The working copy:
- is in the RAC frame, with the 05N GO-RD0 transform and no mirroring;
- has UV-seam duplicates welded, with merge distance 0;
- has 70,634 vertices, 140,960 faces, 320 boundary edges and 0 non-manifold edges.

## Choice of patch: the +X upper-arm armband, exposed lateral arc only

**Why this patch.** The +X armband is the smallest garment that wraps a limb. It has exposed source anatomy on both sides: the deltoid above and the biceps/triceps below. The +X arm is the clean arm; the −X arm is open at the F1/F2 seam.

**Not chosen:**
- *Bracers and shin wraps.* They cover almost the whole forearm or shin, so there is little exposed anatomy next to them.
- *Pendant.* Excluded by the order.
- *Pelvis.* Excluded by the order.

**Medial limit.** The patch does not cover the whole ring. The band disappears into the fused arm/trunk contact in two places:
- the anterior axillary fold at θ ≳ 90°, where the band's upper ledge vanishes and the surface slopes smoothly into the pectoral fold;
- the posterior fold at θ ≲ −100°.

Perpendicular sections show this: for s ≥ 0 the arm loop opens into the trunk (`separability/S_armband_perp.png`). The sector is therefore θ ∈ [−97°, 88°], which is 185° of exposed band. The medial remainder of the band stays untouched, and its cut ends will show.

**What a PASS would prove:** a local garment ridge on F1 can be removed and the gap closed with labelled inferred skin, while every protected source face stays bit-identical.

**What a PASS would not prove:**
- that the anatomy under the band was recovered (it was never modelled; this is class c);
- that larger garments (belt, wraps, bracers) are removable;
- that the medial axillary contact can be separated;
- anything about acceptance.

## Arm-local frame

| Quantity | Value |
|---|---|
| Origin O | (30.5, −1.3, 160.4): centroid of the arm cross-section just below the band |
| Axis d | (−0.29408, −0.05401, 0.95425): normal of the plane fitted to the band's lower ledge |
| θ = 0 | lateral (+X), e1 = (0.95565, 0, 0.29451) |
| θ = +90° | anterior, e2 = (−0.01591, 0.99854, 0.05162) |

The ledge curves s_lo(θ) and s_hi(θ) are area-weighted medians of the faces whose normal faces down or up the axis (|n·d| > 0.55). They are listed in `patch_selection.json`.

## Face sets (`patch_face_sets.npz`, `patch_face_labels.npy`: 1 = G, 3 = S)

**G (garment, removed).** 672 faces, 279.8 cm², sha256 `9cef0fc3…6b1`, bounds x 27.56–39.39, y −13.87–10.55, z 159.92–168.82.
- G is the set of faces connected to the seed (face 131757, on the band's outer face) within θ ∈ sector and s ∈ [s_lo − 0.45, s_hi + 0.45], with r < 13.
- It also includes 82 faces of protected islands that the removed region fully encloses. These lie on the band's surface at the sector ends.

**S (seam band, removed and rebuilt).** 207 faces, 101.6 cm², sha256 `33f44c90…8233`.
- S is skin within s ∈ [s_lo − 1.8, s_hi + 1.8] in the same sector, minus G.
- Known label error: at the sector ends (θ > 75°, θ < −80°) the upper ledge is weak, so some band-top faces are labelled S instead of G. Both sets are removed, so this affects only the reporting split.

**Removed region R = G ∪ S.** 879 faces in one component, a disk:
- 1 boundary loop of 109 edges, Euler characteristic 1;
- 386 interior vertices are deleted;
- the 109 boundary vertices are kept exactly.

**P (protected).** 140,081 faces, index sha256 `f4fe4516…a64f`. The sha256 of the float64 coordinates V[F[P]] is `28d2b7aed535275fe9a176b977fc0199f79c5a19af7c5a88f99062c59edfaa34`.

## Method (`q_patch.py`, to be written after this commit)

1. **Duplicate.** Load the working copy, delete the R faces, and drop the 386 orphaned interior vertices. The output vertex array is the kept original vertices in their original order, followed by the new vertices. The map is recorded.
2. **Boundary.** The hole boundary is one loop, which is split into four chains at the sector corners:
   - the lower skin chain;
   - the upper skin chain;
   - two end chains, which cross the remaining band.
3. **Fill.** A structured interior grid in (θ, s) with about 1.0 cm spacing, which matches the local source mean edge length of 1.19 cm.
   - **Lower and upper rows:** the radius r(θ, s) is a cubic Hermite interpolation between the lower and upper skin chains. The slopes ∂r/∂s are measured on the protected skin within 2.5 cm outside each chain, so the fill is tangent-continuous with the exposed anatomy.
   - **End chains:** the end chains enter through a localized Coons correction that decays with smoothstep over 3 cm from each end. The result is a short labelled ramp up to the remaining band's cut end; there is no global tilt.
   - **What the fill does not contain:** no donor detail, no projection and no sculpted muscle. The fill is honestly inferred, smooth skin, labelled reconstructed. No vetted donor mask exists, so none is used.
4. **Stitch.** The grid's outer ring is zipper-stitched to the hole boundary loop. Each triangle advances on whichever loop gives the shorter diagonal. The boundary vertices are shared, so the result is watertight to P.
5. **No global operations.** There is no whole-figure remesh, voxelization, smoothing or decimation. Only R is touched.
6. **Keep every attempt.** Rejected attempts are kept in `repair/attempts/` with their records.

## Verification (pre-registered)

| # | Check | PASS criterion |
|---|---|---|
| V1 | Protected faces | `sha256(V'[F'[P']])` equals `28d2b7ae…aa34`. The P faces are the first 140,081 faces in their original order, and their vertex coordinates are bit-identical through the recorded map. |
| V2 | Boundary / manifold | The whole mesh still has exactly the same 320 boundary edges as the source (none introduced) and 0 non-manifold edges. Patch faces have consistent orientation with their neighbours, and there are no degenerate faces. |
| V3 | Self-intersection | No new face intersects any face within 6 cm (triangle–triangle test). Pre-existing source intersections in the same box are listed separately and are not counted. |
| V4 | Triangle quality | The minimum angle of new faces is ≥ 10°, and the edge length is between 0.25 and 2.5 cm. |
| V5 | Seam continuity | The dihedral angle across the stitch edges (new face to P face) is ≤ 35° on ≥ 95 % of those edges, compared with the same statistic for source skin in the band neighbourhood. |
| V6 | Ridge removed | In the sector, away from the 3 cm end ramps, no reconstructed face has \|n·d\| > 0.55 (no ledge). The radial step across the former band edges is below 0.3 cm, measured on perpendicular sections at θ = −60, −20, 20, 60. |
| V7 | Adjacent relief intact | This follows from V1. The deltoid, biceps and triceps relief outside R is shown in same-camera before/after views. |

**Outcomes:**
- PASS if V1–V7 all pass.
- FAIL if V1 or V2 fails, or if the fill crosses itself.
- INCONCLUSIVE if V3–V6 fail only marginally.

The visual credibility of the inferred skin is reserved for author review.

**Images:**
- same-camera before/after closes (front, lateral, rear, 3/4, underside), shaded and wireframe;
- seam cross-sections;
- full-figure context;
- a colour overlay: untouched grey, removed red (before), reconstructed blue, seam amber.

## Stop

After the result there is no RD5, no second patch, no blind gate, LOW, scaffold, canon or production work.
