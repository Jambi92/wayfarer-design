# RM-OT-05S direct band-to-axilla interface repair plan (committed BEFORE any edit)

This is one declared direct study of the **same** +X armband interface: both junctions plus the band lip and fold edge immediately next to them. It is not full-body clothing removal and not RD4. B2 and R1–R3 stay rejected and frozen.

## Capability statement (05S §2)

| Requirement | Available here | How |
|---|---|---|
| Explicit vertex / edge / face selection | **yes** | Index sets on the baseline mesh, chosen by explicit profile position (below) |
| Controlled local topology reconstruction | **yes** | Explicit deletion; constrained quality triangulation (Shewchuk Triangle) of an explicit chart; 3-D Lawson edge flips with topological winding; explicit stitching to the exact boundary vertices |
| Anatomical surface shaping | **scripted only** | Every new vertex is placed on an explicitly **designed cross-section profile** per 0.25° column (below). There is **no interactive brush or sculpt**. Blender 5.0.1 is present only as a Python module (bpy / bmesh, headless), with no UI. **No interactive brush work is claimed.** |

**This is not a harmonic / biharmonic fill.** No Laplacian or bi-Laplacian solve is used, there is no relaxation or smoothing pass, and there is no parameter sweep.

**Fallback.** If the study fails verification, geometry work stops, and the release carries a direct-edit handoff for an interactive sculptor: a native `.blend` scene with masks (vertex groups), a brief and the verification setup.

## Inputs and baseline rationale

| Item | Value |
|---|---|
| base.glb (external, unchanged) | sha256 `78ecfa87d169380ecb46ece3f0c0df3491d10e4547038a3c35c06df933f38a7b` |
| F1 working | `reviews/rac-rmot05q-evidence/source/F1_working.obj.gz`, decoded `17591025…53b0` |
| Baseline B2 | decoded `0ed458b7…962a` |

**Why B2.** B2 *is* the fresh F1 duplicate with the verified 05Q removal recipe (`q_patch_b.py … --tag B2 --relax 30`, reproducible bit-identically). Its central inferred patch, θ −80…74°, is kept: it was credible and V1–V3-clean.

Its defective ends, and all of R3, are **not** inherited. The R3 junction mesh is not used at all; it appears only in the comparison images.

## Interface regions I (`interface_sets.npz`, `interface_selection.json`; `s_design.py`, `s_select.py`)

All positions use the 05Q arm-local frame (θ = 0 lateral, +90° anterior; s along the arm). The baseline is cut into half-plane **profile columns every 0.25°**. Each column carries explicit anchors:

- **Ledge level `s_led(θ)`:** the band's lower ledge, from faces facing down the axis (2° medians, smoothed).
- **A:** the profile point at `s_led − 1.8` cm on exposed arm skin.
- **B:** the first profile point after the ledge with `s ≥ s_B`. In the sector, `s_B = s_hi + 1.8`. Anterior beyond the sector it is `s_hi(88) + 1.8`. If the profile turns down first (the posterior lip / fold-edge peak), B is placed **2.5 cm of arclength beyond the peak on the fold / trunk side**, so the curled fold edge sits inside the region.
- A and B are smoothed along θ (σ 3°) and re-projected onto their columns.

**Zones and weight w(θ).** `w` is 0 at both region ends, so the result equals the baseline there and meets unchanged geometry. It rises by smoothstep to 1, which means full reconstruction.

| Side | Region θ | w ramps up | w = 1 (garment fully removed) | w tapers down (deliberate termination) |
|---|---|---|---|---|
| **Posterior** | −80 … −136° | 0 → 1 over −80 … −88 | −88 … −116 | 1 → 0 over −116 … −136: the band's ledge and lip shrink to the untouched remainder |
| **Anterior** | 74 … 122° | 0 → 1 over 74 … 82 | 82 … 104 | 1 → 0 over 104 … 122 |

**Region I.** Baseline faces whose centroid chart position satisfies `t = (l − l_A)/(l_B − l_A) ∈ [0, 1]` inside the zone. Each side is one connected disk.

| Side | Faces | Source faces (area) | Boundary loop | Chart crossings | Bounds (cm) |
|---|---|---|---|---|---|
| Posterior | 238 = 110 B2-new + 128 source | 128 (51.2 cm²) | 50 vertices | 0 | x 23.25–32.62, y −15.39 to −4.33, z 157.82–168.39 |
| Anterior | 219 = 73 B2-new + 146 source | 146 (63.3 cm²) | 51 vertices | 0 | x 22.60–33.05, y 4.06–11.17, z 159.18–168.57 |

**Garment / anatomy classification** of the source faces, by profile position:

| Class | Posterior | Anterior |
|---|---|---|
| Arm skin seam, below the ledge | 30 | 22 |
| Garment band (ledge to lip / top) | 67 | 106 |
| Fold edge or trunk (beyond the lip peak) | 31 | — |
| Fused fold, ambiguous (slope above `s_led + 4`) | — | 18 |

All fold-edge, trunk and ambiguous faces inside I are rebuilt as **INFERRED** surface. No skin is claimed as recovered.

**Original protected faces now inside the authorized boundary.** 274 faces of the 05Q protected set P fall inside I:
- 74 of them were the 05R extension;
- 200 are new in 05S: the band remnant, the lip curl / fold edge and the trunk strip beyond the peak, and the remainders of the 05Q seam band;
- 3 faces of the 05R extension lie outside I and stay protected.

By group and reason:
- posterior: 30 arm-skin seam faces (skin between anchor A and the ledge; wording corrected after the plan commit, no content change), 67 garment, 31 fold edge (the curled lip that caused the 05R intersections);
- anterior: 22 arm-skin seam, 106 garment, 18 fused-ambiguous.

The index lists, with classes, are in `interface_sets.npz` (`src_post`, `class_post`, `src_ant`, `class_ant`).

**Protection outside I (P05S).** The 05Q P minus those 274 faces: 139,807 faces in the original order, face-index sha `00ec4337…aa4d`, **coordinate sha `4468dd862307b8393dfcc8dab58d5cab6033558a87ba523b220e379b7df57c55`**. The 05Q and 05R protection sets stay in their evidence as committed.

**Not in scope:** the full ring, arm–trunk separation, the whole axilla or shoulder, pose, a second garment, and any torso or limb redesign.

## Designed surface (explicit; `design_*_columns.png` shows 12 columns per side)

At each column:
- **The existing profile segment, S_AB(u).** It runs A → B, with u as normalized arclength.
- **The designed no-garment profile, D(u).** A cubic Hermite curve A → B whose end tangents are the profile tangents at A and B, with magnitude equal to the chord. It resamples to arclength.
- **The target, P(u) = (1 − w)·S_AB(u) + w·D(u).**

What this does:
- **Where w = 1:** the ledge, the band face and the curled lip / fold edge are replaced by a direct arm-to-fold crease that is tangent-continuous with exposed arm skin at A and with the fold / trunk surface at B.
- **In the taper zones:** the band's step shrinks progressively. It meets the untouched remainder as a **tapered termination, not a cut end or a lip**.

There is no donor, no projection and no invented detail.

## Method: the one declared study, `s_repair.py`, written after this commit

1. **Baseline duplicate.** Decode B2, then apply the documented C1 flip (B2 faces 140820 / 140812, as in 05R).
2. **Per side, delete the I faces.** Get the boundary loop; its 3-D positions stay exact.
3. **Chart.** For each vertex, x = θ_rad · 9 cm and y = l − l_A, giving unfolded arclength along its column. The boundary loop is checked for simplicity (0 crossings in the dry run). If a crossing appears, the offending boundary vertices are clamped onto the zone-end column; this changes the layout only.
4. **Triangulate.** Run a constrained quality triangulation (q30, area for a 0.7 cm edge, no boundary Steiner points). Orientation comes from the removed faces' boundary half-edges.
5. **Place new vertices.** Each new interior vertex is placed exactly on the designed target P(θ, u), interpolated bilinearly between neighbouring 0.25° columns and the 64 u-samples. There is no solve and no relaxation.
6. **Flip edges.** 3-D Lawson flips among the new faces only: topological winding, minimum-angle gain ≥ 0.5°, resulting dihedral ≤ 40°, and never creating an edge that already exists anywhere.
7. **Assemble.** P05S faces come first (in the 05Q order), then the retained B2 faces (B2 order, with C1), then the new faces. Maps go to F1 and to B2.
   - Label 5 is reconstructed skin (centroid w ≥ 0.99).
   - Label 4 is the termination / transition (w < 0.99).
   - Both are INFERRED.
8. **Checkpoints.** The selection, the chart and triangulation, the pre-flip mesh and the final mesh are all saved.
9. **No retries.** If verification exposes a discrete implementation fault, one bounded correction is allowed and documented. Otherwise the result is reported as FAIL or UNRESOLVED and the handoff is supplied.

## Verification (pre-registered)

| # | Check | PASS criterion |
|---|---|---|
| V1 | Protected coordinates | `sha256(V'[F'[:139807]])` equals `4468dd86…7c55`, with index correspondence to `P05S_src_ordered`; kept source vertices bit-identical |
| V2 | Boundary / manifold | Mapped boundary edges equal the source's 320. 0 non-manifold edges, 0 inconsistent orientation, 0 degenerate faces |
| V3 | Intersections | 0 new-face intersections against all faces within 6 cm. Pre-existing source pairs listed separately |
| V4 | Triangle quality (unchanged) | All new faces (retained B2 + C1 + interface): minimum angle ≥ 10°, edges 0.25–2.5 cm. Full distribution and every outlier with its location |
| V5 | Seam continuity (unchanged) | Every new↔source stitch edge: dihedral ≤ 35° on ≥ 95 %. Full histogram and outlier locations. No junction is excluded |
| V6 | Historical (05Q) | Reported separately |
| V6c-1 | Garment ledge removed (anatomy-aware) | At θ = −112, −104, −96, −90, 84, 90, 96, 102 (w = 1 columns): along the rebuilt section from A to B, the largest direction change within any 0.5 cm arclength window is ≤ 35°. The source band edges at the same angles are reported for contrast. The deltoid / fold slope itself is not penalised (a direction change, not \|n·d\|) |
| V6c-2 | Taper is a termination, not a lip | In each taper zone, the section's ledge step (largest radial jump within s_led ± 1.5) decreases monotonically from the untouched end toward the w = 1 zone (tolerance 0.1 cm), and the section is free of undercut (s non-decreasing from A to the ledge top) |
| V6c-3 | No folds | 0 dihedrals > 120° between new/new or new/source faces. Counts > 90° are reported |

**Verdict rules:**
- **PASS** requires V1–V5 and V6c-1..3.
- **FAIL** if V1, V2 or V3 fails, or there is any dihedral > 120°, or any minimum angle < 5°.
- **UNRESOLVED** otherwise. Remaining slivers and folds are never called marginal.

Anatomical visual credibility is judged separately, and the author decides.

**Images:** source / B2 / R3 / new result, all with the same camera and material:
- both junctions at readable size;
- front, lateral, rear, 3/4 and underside closes;
- wireframe and labels;
- sections at both junctions;
- full figure.

Plan images in this folder: `P1_arm_views_interface.png`, `P2_posterior_interface.png`, `P3_anterior_interface.png` (source / B2 / R3 with I marked), `P4/P5_*_profiles_src_B2_R3.png`, `I_*_chart_topology.png` and `design_*_columns.png`.

## Package

The release `racebodies_v123` follows the v122 conventions: its own manifest, split volumes of ≤ 25 MB, clean-extraction verification and a scripted replay.
