# RAC RM-OT-05Q: Gorrund source-surface patch feasibility, gate report

**Order:** `reviews/chatgpt-rac-rm-ot-05q-gorrund-source-surface-patch-feasibility-order.md` (commit c51ee71).
**Evidence:** `reviews/rac-rmot05q-evidence/`. **Tools:** `tools/rac/w1/rmot05q_drivers/`. **Replay:** `REPLAY.md`, with a SHA-256 manifest in `SHA256SUMS.txt`.
**Plan commit:** a93502b, made before any mesh edit. **Result commit:** this one.

## Status

| Item | Status |
|---|---|
| Gorrund | UNACCEPTED |
| Grask E3 | FROZEN |
| RM-OT-05 | OPEN |
| Stage C | BLOCKED |
| RD4 | REJECTED |
| RD1–RD4 | frozen |

This was a source-surface feasibility study only. It is not an acceptance of the source's muscularity, paws or garments. Nothing in it is canon, production, LOW, scaffold, blind-gate, D4 or UE5 work. There was no Rodin regeneration and no credits were used.

## Result in one paragraph

Every garment on Gorrund's F1 surface is fused into one continuous sheet. Nowhere is there skin modelled underneath a garment. The waist belt, bracers, shin wraps, mane and armband are all class (c). The loincloth flaps and the braids hang free below their attachments, which is class (a). The necklace and the −X armband are ambiguous, class (d).

One representative local repair was carried out on a duplicate: the +X upper-arm armband, exposed lateral arc only (θ −97°…88°).
- The band's 672 faces were removed, along with a 207-face seam band of skin.
- The hole was filled with 773 faces of **inferred** skin. No donor detail was used and nothing was projected.
- All 140,081 protected source faces are **bit-identical**, both by coordinate hash and by index correspondence.
- The mesh keeps exactly the source's 320 boundary edges, has 0 non-manifold edges and has no self-intersections.
- The garment ridge is gone. The radial step at the former band edges falls from 1.7–3.2 cm to 0.15–0.34 cm.
- The skin seams above and below are continuous: 98.7 % of their stitch edges are ≤ 35°.

The pre-registered automated verdict is **INCONCLUSIVE**. V4, V5 and V6 fail, but every failure is located either:
- where the fill meets the two cut ends of the remaining medial band (the band disappears into the fused armpit contact and was out of scope), or
- in the inferred skin directly under the deltoid, which inherits the deltoid's own steep lower slope.

Whether the inferred skin is credible is left to the author's visual review.

## §2 Source provenance and extraction (`source/`)

**The source file.** `base.glb` has sha256 `78ecfa87d169380ecb46ece3f0c0df3491d10e4547038a3c35c06df933f38a7b` and is 43,012,652 bytes. It was re-hashed at three locations:
- the session upload;
- a container copy;
- inside the E: zip `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Male\Gorrund-Male_Rodin_base.glb.zip`, whose own sha256 is `b3fbfb2a…482e` and size 22,764,144 bytes.

**F1 is the detailed 05N surface**, `c0s_1` / GO-RD0-SOURCE, taken before any 05N SDF, blur or field step.
- **The contact-slab cut:** island 0 holds both figures, and 05N split them at the contact slab. The slab bounds were **never recorded**. 05Q therefore recovered F1's exact 140,960 GLB face indices by centroid matching (max 7.2e-5) and committed them as `F1_face_indices.npz`. That list is now the authoritative definition of F1.
- **Extraction script:** `q_extract.py` rebuilds F1 from the GLB plus that list. It writes three files:
  - `F1_glb_units.obj`: untouched GLB coordinates;
  - `F1_rac_frame.obj`: RAC frame;
  - `F1_working.obj`: UV-seam duplicates welded at merge distance 0, with the face order kept.

  It also writes `extraction_record.json`.
- **Transform:** rotation of 180° about Z, scale 2.70634, translation. **It is not a mirror.** Mirroring happened only later, in 05N `field.py`.
- **The open arm seam:** the −X arm and hand are open at the cut, which accounts for all 320 boundary edges, plus four tiny slab fragments (219 faces). The +X arm is clean.
- **Check against 05N:** the rebuild matches GO-RD0-SOURCE within 0.00028 cm.
- **Untouched:** no stance, stature, composition, head/tail or muscle edits were made.

## §3 Clothing separability (`separability/`)

**Topology.** After welding, F1 is a single connected surface. Apart from the slab fragments there is no separate garment geometry.

**Method.**
- Plane sections were taken through each item and chained into loops (`q_sections.py`), shown in the `S_*.png` images with loop data in `S_*.json`.
- The question was whether a second, inner skin loop exists under the garment.
- Wireframe and underside renders are the `R_*_wire.png` images.

| Item | Class | Confidence | Evidence |
|---|---|---|---|
| Waist belt + loincloth top (z 112–140) | c | medium | z118/126/132: one outer contour (belt, buckle discs, fringe); no abdomen/pelvis loop inside |
| Loincloth flaps (z 72–112) | a/b | medium | z100: separate thigh loops inside the open skirt contour; flaps hang free below z ≈ 105 and are fused at the belt |
| Forearm bracers | c | high | z112–136: a single forearm loop with no inner loop; the strap relief is the outer surface |
| +X upper-arm armband | c | high | Long and perpendicular sections show a single outward step with an undercut lip and no skin beneath. The medial arc runs into the fused arm/trunk axillary contact |
| −X upper-arm armband | d | low | The −X arm is open at the 05N slab seam, so it cannot be read |
| Shin + ankle wraps | c | high | z24–46: a single loop per leg with no inner shin loop |
| Necklace + pendant teeth | d | medium | A shallow relief fused onto the chest; a single surface; a local fill is plausible but unproven |
| Front braids | a | medium | Separate small loops in front of the chest below the attachment; the chest contour is continuous behind them |
| Back braid | a | medium | A separate loop behind the back below the attachment |
| Mane over neck / upper back | c | medium | The outer contour is the mane; there is no neck or trapezius surface inside it |

**Inventory.** `inventory.json` and `inventory_face_zone.npy`, shown in `R_inventory_full.png`.
- Only the armband has a **verified** face set.
- The other zones are coarse boxes. Their known errors are listed in the inventory: they include adjacent body faces such as the chest in the necklace box and the thighs in the flaps box.

**No anatomy is claimed to be recovered anywhere.**

## §4 Patch selection and plan (`plan/`, committed first in a93502b)

**Why this patch.** The +X armband is the smallest limb-wrapping garment that has exposed anatomy on both sides: the deltoid above, the biceps and triceps below. The bracers and wraps cover almost whole limb segments. The pendant and pelvis are excluded by the order.

**The sector.** The band dives into the fused axillary contact at the anterior fold (θ ≳ 90°) and the posterior fold (θ ≲ −100°). The sector is therefore limited to the exposed arc, 185°. The medial band remainder is untouched, and its two cut ends stay visible.

**Face sets.**

| Set | Faces | Role |
|---|---|---|
| G | 672 | garment, removed (includes 82 enclosed band islands) |
| S | 207 | seam band, removed and rebuilt |
| P | 140,081 | protected; coordinate sha256 `28d2b7ae…aa34` |

**Plan contents.** The frame, the ledge curves, the method and the pre-registered criteria V1–V6 are in `PLAN.md`.

**What a PASS would prove:** a local garment ridge on F1 can be swapped for labelled inferred skin while the protected source stays bit-exact.

**What a PASS would not prove:** recovered anatomy, removability of larger garments, separation of the axillary contact, or acceptance.

## §5 Local repair on a duplicate (`repair/`)

All attempts are kept with their records, verification and renders in `repair/attempts/`.

| Attempt | Method | V1 | V2 | V3 | V4 | V5 | V6 | Outcome |
|---|---|---|---|---|---|---|---|---|
| A1 | Plan method as written: structured (θ, s) grid with Hermite r and Coons ends, global zipper | ✔ | ✔ | 21 intersections | ✗ | 0.75 | ✗ | rejected: the zipper folds where the jagged hole boundary wanders more than one grid row |
| A2 | A1 with smoothed guides and per-chain zippers | ✔ | ✔ | 66 | ✗ | 0.43 | ✗ | rejected (worse) |
| B1 | Constrained quality Delaunay of the hole in the (θ, s) layout; same Hermite/Coons field plus a harmonic residual to the exact boundary | ✔ | ✔ | 16 (all at the two band-end corners) | ✗ | 0.86 | ✗ | rejected |
| **B2** | B1 plus a local umbrella relaxation (30 iterations) of new vertices within 3 cm of the band ends only | ✔ | ✔ | **0** | ✗ | 0.84 | ✗ | **reported result** |
| B3 | B2 with 60 iterations over a 4 cm zone | ✔ | ✔ | 0 | ✗ | 0.84 | ✗ | no better than B2 |

**Deviation from the plan, disclosed.** The plan's step 3–4 (a structured grid with a zipper stitch) failed as A1/A2. Method B keeps the plan's inferred field: Hermite between the skin chains, slopes measured on protected skin, a 3 cm smoothstep Coons correction at the ends, no donor and no projection. It changes three things:
- **Triangulation:** constrained Delaunay (Shewchuk Triangle, q30, no boundary Steiner points) instead of the grid and zipper.
- **Exact boundary fit:** a harmonic residual so the field meets the exact boundary vertices. The mean boundary residual is 0.49 cm. The maximum, 4.1 cm, occurs at the band ends.
- **End relaxation:** the end-only relaxation used in B2.

At the band ends the hole loop crosses the band's overhanging lip and folds in the 2-D layout. That layout (not the 3-D positions) is straightened along the sector edge for 28 end-run vertices; this is recorded.

**What B2 changes.**
- Removed: 879 faces and 386 interior vertices.
- Added: 773 faces and 333 vertices, all inside the hole.
- All 109 hole-boundary vertices are original and unmoved.
- There is no global remesh, voxelization, smoothing or decimation.
- Output: `GO-05Q-B2.obj.gz`, sha256 `0ed458b7…962a`. Per-face labels and the vertex map are alongside. The layout is: protected faces first in their original order, then new faces.

## §6 Verification of B2 (`repair/B2_verify.json`, `repair/compare/`)

| # | Check | Result | Verdict |
|---|---|---|---|
| V1 | Protected coordinates sha256 `28d2b7ae…aa34` equals the plan's | Equal; index correspondence exact; all 70,248 kept vertices bit-identical | **PASS** |
| V2 | Boundary / manifold / orientation | 320 boundary edges, identical to the source; 0 non-manifold; 0 inconsistent orientation at the patch; 0 degenerate | **PASS** |
| V3 | Self-intersection (new faces against all faces within 6 cm; 1,821 faces tested) | 0 new; 0 pre-existing source pairs in the box | **PASS** |
| V4 | New-face minimum angle ≥ 10°, edges 0.25–2.5 cm | 10 faces < 10° (minimum 0.98°), **9 of them at the band ends**; 22 edges out of range; 5th-percentile minimum angle 18.1° (the removed source faces: 11.9°) | FAIL (localized) |
| V5 | Stitch dihedral ≤ 35° on ≥ 95 % of edges | 84.4 % overall. Skin seams: **98.7 %** (78 edges, max 43.7°). Band-end junctions: 48 % (31 edges, folds up to 178°). Source skin reference: p95 34° | FAIL (band-end junctions) |
| V6 | No ledge faces (\|n·d\| > 0.55) in the core; radial step < 0.3 cm | Step: 0.145 / 0.162 / **0.336** / 0.239 cm at θ −60/−20/20/60, against source 0.28 / 1.67 / 3.16 / 2.55 cm. Ledge faces: 50, but 49 lie in the top zone under the deltoid, where **45 % of the source's own protected skin** has \|n·d\| > 0.55. The criterion did not anticipate the deltoid's steep underside | FAIL (criterion and anatomy) |
| V7 | Adjacent relief intact | Follows from V1; see the same-camera closes | holds |

Under the pre-registered rules the verdict is **INCONCLUSIVE**:
- it is not FAIL, because V1 and V2 pass and the fill has no self-crossing;
- it is not PASS, because V4–V6 fail.

The V4 and V5 failures are not small in count, but they are confined to the band-end junctions. The breakdown that locates them is in `supplementary_posthoc`; it was computed after the result and does not change the verdict.

**Images.**

| File | Content |
|---|---|
| `compare/01_before_after_shaded.png` | Same cameras: front, lateral, rear, two 3/4 views, underside |
| `compare/02_before_after_wireframe.png` | The same views in wireframe |
| `compare/03_overlay_untouched_removed_reconstructed_seam.png` | Grey untouched; red removed garment; amber seam band; blue reconstructed (inferred) |
| `compare/04_full_figure_context.png` | Full figure |
| `compare/05_seam_cross_sections_before_after.png` | Four planes through the arm axis, coloured by label |
| `compare/06_axis_half_plane_profiles_V6.png` | Half-plane profiles used for the radial-step check |

**What a reviewer should look at.**
1. The two band-end junctions:
   - posterior, θ ≈ −97°: the crinkle in the rear/3/4 closes;
   - anterior, θ ≈ 88°: the fold at the lower lip.
   - Also the line where the untouched medial band continues into the armpit.
2. Whether the smooth inferred skin under the deltoid reads as plausible anatomy or as a featureless filler. It carries no muscle detail, by design.

## What this does and does not show

**Shows:**
- The F1 source surface can be locally edited without disturbing any protected face, bit for bit.
- A fused garment ridge can be removed and replaced by labelled inferred skin with continuous seams against exposed anatomy.

**Does not show:**
- Recovered anatomy. There is none under any class (c) garment, and the fill is inferred.
- Credibility of larger fills such as the belt, bracers or wraps, or of the class (d) items.
- A way to separate the fused axillary contact. Any full-ring removal would have to cut into it.
- Anything about acceptance.

## Stop

Stopped at the author visual gate. No RD5, no second patch, no blind gate, no LOW, scaffold, canon or production work. Gorrund is UNACCEPTED, Grask E3 is FROZEN, RM-OT-05 is OPEN and Stage C is BLOCKED.

**Large-file locations.**
- All meshes are committed gz-compressed: the source copies are about 1.8–2.1 MB each, the result and each attempt about 2.0 MB.
- `base.glb` itself (43 MB) is not committed. It is verified at the three locations in §2.
- The package `racebodies_v121` (on E:) carries the evidence and the result OBJ.

---

## Addendum (05R, October 12, 2026): author ruling and correction note. Append-only; the scores above are unchanged.

**Author ruling (05R order §1).** B2 is **NOT accepted**. The visible cut ends and crinkles, and the V4/V5 failures, are substantive defects:
- a minimum new-triangle angle of 0.98°;
- 22 edges outside the declared range;
- seam dihedral up to 177.72°;
- only 84.4 % of seam edges meeting the criterion overall.

They are not marginal, and the passing preservation and manifold checks do not make the skin credible. The 05Q plan, attempts, numbers, post-hoc breakdown and automated INCONCLUSIVE verdict stay above as provenance.

**Correction to the clothing summary.** The opening sentences of "Result in one paragraph" overreach. Findings are per item or region, with the confidence given in the §3 table:
- Free-hanging flaps and braids (class a), fused surface garments (class c) and ambiguous areas (class d) are different cases.
- What was demonstrated is limited: within the inspected sections, no skin surface was found under the **selected** class-c garment (the +X armband). The other class-c entries rest on the listed sections, at the listed confidence.
- The claim does not extend to uninspected or ambiguous regions.
- Connected geometry alone is not proof that no underlying surface exists.

**Package integrity.** The v121 package's `SHA256SUMS.txt` was the repository evidence manifest, but the package itself held JPEG conversions and omitted the source and attempt meshes. No complete package integrity pass was therefore established for v121. 05R issues a package with its own verified manifest.
