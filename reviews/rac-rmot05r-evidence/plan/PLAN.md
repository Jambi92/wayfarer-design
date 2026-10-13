# RM-OT-05R junction repair plan (committed BEFORE any edit)

**Scope.** This plan covers the same +X upper-arm patch from 05Q. Its two junctions with the remaining band are repaired locally. Nothing else changes.

**Baseline.** B2 is the repair baseline only; it is not accepted anatomy (author ruling, 05R §1).

## Frozen inputs (hashes)

| Item | Value |
|---|---|
| base.glb (external source master) | sha256 `78ecfa87d169380ecb46ece3f0c0df3491d10e4547038a3c35c06df933f38a7b` |
| F1 working copy | `reviews/rac-rmot05q-evidence/source/F1_working.obj.gz`, decoded sha256 `17591025c24fd080e7fd45e3dc88dccc4707a0bee9efcb3fd70ef5ab6da453b0` |
| B2 baseline | `reviews/rac-rmot05q-evidence/repair/GO-05Q-B2.obj.gz`, decoded sha256 `0ed458b72e6481377aa829d70f8f7896381634e9fc7cca09bc325a91b420962a` |

B2 is laid out as 140,081 protected source faces (in the 05Q P order) followed by 773 new faces. Its vertex map and labels are in the 05Q `repair/` folder.

The following stay frozen and are not edited:
- the 05Q plan (a93502b), all 05Q attempts, numbers, post-hoc breakdown and INCONCLUSIVE verdict;
- earlier RD evidence.

## The two junctions: current defects in B2

Every B2 V4 outlier but one, and every V5 stitch outlier, lies at the two band ends.

**Posterior, θ ≈ −97°**
- **What is there:** the remaining band is a short stub. Its bottom lip sits at s ≈ 0.8–1.3, and its top merges into the posterior axillary fold edge. The fold edge is a diagonal running from s ≈ 3 at θ −118° to s ≈ 6.2 at θ −98°.
- **B2 defects:**
  - slivers at s 5.8–6.3 (B2 faces 140099, 140134, 140135, 140158, 140163, 140168, 140171, 140173, 140177, 140181, 140190, 140191, 140192, 140242, among others);
  - stitch folds up to 177.7°;
  - a crinkle where the fill climbs to the top-lip curl.

**Anterior, θ ≈ 88°**
- **What is there:** the remaining band is a bottom lip at s ≈ 1.3–1.7, with a raised surface above it that slopes up into the anterior axillary/pectoral fold. There is no top ledge.
- **B2 defects:**
  - slivers at s 1.1–1.4 (140185, 140227, 140238 at 1.0°, 140290, 140291);
  - stitch folds where the fill meets the lip's cut end.

**The one outlier outside the ends:** B2 face 140820 at θ 5.2°, s −0.11, with a minimum angle of 9.975°.

The evidence for all of this is in `J_*_profiles_src_vs_B2.png`, which shows half-plane sections through the arm axis (grey = source, blue = B2), and in `J_*_selection_on_B2.png`.

## Junction regions J (`junction_sets.npz`, `junction_selection.json`; `r_select.py`)

All geometry uses the 05Q arm-local frame: origin (30.5, −1.3, 160.4), axis (−0.29408, −0.05401, 0.95425), θ = 0 lateral, +90° anterior.

**Posterior J: 134 B2 faces.**
- **104 B2 new faces:** θ ∈ [−110°, −82°], which covers B2's whole posterior end zone.
- **30 source faces:** the extension into the remaining band stub, θ ∈ [−110°, −97°].
  - Bounds: s ≥ s_lo − 1.8 and s ≤ fold-edge line − 0.25 cm, r < 11 cm.
  - Of these, 23 are garment remnant (band lip and face) and 7 are skin seam.
  - Area 11.06 cm². Index sha256 `6ab7e0f3…6388`.
- The fold edge itself and the fold surface stay outside J.

**Anterior J: 121 B2 faces.**
- **74 B2 new faces:** θ ∈ [74°, 102°].
- **47 source faces:** the extension, θ ∈ [88°, 102°].
  - Bounds: s ≥ s_lo − 1.8, s ≤ 4.5, r < 13.
  - Of these, 39 are garment remnant (lip and the raised band surface) and 8 are skin seam.
  - Area 21.93 cm². Index sha256 `a44fa6e9…447e`.
- The pectoral-fold contact beyond θ 102° stays outside J.

**Topology of each J:** one connected component, a disk (Euler characteristic 1), with one boundary loop.
- Posterior loop: 40 boundary edges, lengths 0.372–2.083 cm.
- Anterior loop: 39 boundary edges, lengths 0.302–2.262 cm.
- All boundary edges therefore sit within the V4 edge bounds.

In the (θ·8 cm, s) layout the posterior loop has four crossings, at the fold-edge spur near s ≈ 6. That is why the layout below uses an embedding, not (θ, s): `J_*_layout_topology.png`.

**Extension relative to 05Q.** The 05Q removed region R had 879 faces. The extension adds **77 source faces (33.0 cm²)** that were in the 05Q protected set P. They are listed by F1_working index in `ext_post_src` and `ext_ant_src`.

**Protected set for 05R (P05R).** This is the 05Q P minus those 77 faces:
- 140,004 faces, kept in the 05Q P order (`P05R_src_ordered`);
- face-index sha256 `753f17f5…e395`;
- float64 coordinate sha256 **`15819a655804550df67022a111d82a28deb22e62eb1c8e5abaf6183babfa3bf0`**.

The 05Q P (coordinate sha256 `28d2b7ae…aa34`) stays in the 05Q evidence unchanged.

**Not touched:**
- the fold edges;
- the axillary contacts;
- the remaining medial band beyond θ −110° and 102°;
- the shoulder, and every other region.

## Method (one planned operation; `r_repair.py` will be written after this commit)

For each J:

1. **Delete** the J faces from B2. Keep all other B2 faces and vertices bit-identical, with B2's retained new faces kept as they are.
2. **Boundary loop.** The loop's 3-D positions are never moved.
3. **Layout.** Use a fold-free Tutte (uniform-weight) embedding of the J submesh, with the boundary placed by arc length on an ellipse whose aspect is the J's (θ·8 cm) : s extent and whose area equals the J's 3-D area. Being convex, the layout is valid by construction.
4. **Triangulate.** Run a constrained quality Delaunay triangulation of that layout (Triangle, q30, no Steiner points on the boundary). The target area corresponds to a 0.8 cm mean edge.
5. **Solve 3-D positions.** Positions of new interior vertices come from a **uniform bi-Laplacian** solve: minimise Σ|L x|² over the interior vertices and the boundary vertices on the skin / B2-fill side, with the boundary and the outside 1-ring fixed, which gives tangent continuity to skin.
   - Boundary vertices that touch garment-remnant faces outside J are left out of the energy. This gives the remaining band a natural, tapered termination rather than a forced continuation of its lip tangent.
   - This is not projection and uses no donor. The result is labelled INFERRED.
6. **Improve triangles in 3-D.** Run Lawson edge flips on edges between new faces: flip when the minimum angle improves and the resulting dihedral is ≤ 40°. Then re-solve step 5. Two rounds.
7. **Seam correction C1** (documented, outside J). Flip the shared edge of B2 faces 140820 and 140812, both inferred.
   - Dry-run check: the minimum angles go from 9.98° / 27.1° to 16.8° / 15.1°, with a pre-flip dihedral of 8.3°.
   - No vertex moves.

**Bounded correction.** One bounded local correction is allowed if verification exposes a discrete fixable issue. There is no parameter sweep. If the junctions cannot be made credible within J, the outcome is FAIL or INCOMPLETE and work stops.

**Output layout:**
- **Faces:** P05R faces in order, then the retained B2 new faces (in B2 order, with C1 applied), then the J new faces (posterior, then anterior).
- **Vertices:** kept vertices, with a map to F1_working (or to B2 for retained new vertices), then new vertices.
- **Labels:**

  | Label | Meaning |
  |---|---|
  | 0 | untouched source |
  | 2 | B2 reconstructed |
  | 3 | B2 seam |
  | 5 | 05R junction reconstruction (INFERRED) |

## Verification (pre-registered)

The original 05Q checks are re-run on the whole repaired patch, extension included, against the F1 source.

| # | Check | PASS criterion |
|---|---|---|
| V1 | Outside anatomy | `sha256(V'[F'[:140004]])` equals `15819a65…bfa3bf0`; the vertex map gives exact index correspondence to `P05R_src_ordered`; kept source vertices are bit-identical |
| V2 | Boundary / manifold | The mesh boundary, mapped to F1_working indices, equals the source's 320 boundary edges exactly. 0 non-manifold edges; consistent orientation at the patch; 0 degenerate faces |
| V3 | Intersections | 0 intersections between new faces and any face within 6 cm. Pre-existing source pairs are listed separately |
| V4 | Triangle quality (unchanged bounds) | Every new face (retained B2 plus J plus C1) has minimum angle ≥ 10° and edges in 0.25–2.5 cm. The full distribution is reported, with the location of every outlier |
| V5 | Seam continuity (unchanged) | Every stitch edge (new face to source face): dihedral ≤ 35° on ≥ 95 %. The distribution is reported, with outlier locations |
| V6 | Historical (05Q definition) | Reported only |
| V6b-1 | Supplemental: garment step | Radial step < 0.3 cm (largest change of the outermost radius between neighbouring 0.25 cm s-bins, s ∈ (s_lo − 2, s_hi + 2)) at θ = −80, −60, −40, −20, 0, 20, 40, 60, 74 |
| V6b-2 | Supplemental: anatomy versus garment slope | Among reconstructed faces in the top zone (s > s_hi − 1, θ in the 05Q core), the fraction with \|n·d\| > 0.55 is ≤ the adjacent source skin's fraction (0.452) + 0.10 |
| V6b-3 | Supplemental: no lip or fold | Inside J, max dihedral between adjacent new faces ≤ 45°. Anywhere on the patch, no new/new or new/source dihedral > 90° |

**Verdict rules:**
- **PASS** requires V1–V5, V6b-1, V6b-2 and V6b-3 all to pass.
- **FAIL** if V1, V2 or V3 fails, or if any new face has a minimum angle < 5°, or if any dihedral > 90° remains (a fold).
- **UNRESOLVED** otherwise. Remaining slivers or folds are not called marginal.

Anatomical visual credibility is reported separately and is reserved for the author.

**Images**, all with identical camera and material, comparing source-before, B2 and the 05R result:
- front, lateral, rear, 3/4 and underside closes;
- both junctions at readable size;
- wireframe and colour labels;
- half-plane cross-sections at the junction angles;
- full-figure context.

## Package (independent of sculpt success)

The package `racebodies_v122` gets its own manifest of the packaged bytes, built by `r_package.py`, and is verified by a clean extraction in an isolated directory with a replay check.
