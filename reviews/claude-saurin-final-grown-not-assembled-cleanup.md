# Saurin Final "Grown, Not Assembled" Cleanup (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/chatgpt-saurin-final-grown-not-assembled-cleanup-order.md` (ec5370c)
**Base:** the accepted post-Gate-8 polish (36cc531): tail taper and brow integration accepted.
**Scope:** meso/anatomical continuity only. No base-mesh densification, no UE5.

**Images** are in `reviews/images/saurin-final-cleanup/`. All are neutral material with identical cameras unless the sheet says otherwise.

| # | Required item | File |
|---|---|---|
| 1 | Whole organism: front, profile, rear, front 3/4, rear 3/4 | `c14_01_whole_organism.jpg` |
| 2 | Chest/sternum before/after | `c14_02_chest.jpg` |
| 3 | Dorsal neck/upper thorax before/after | `c14_03_dorsal.jpg` |
| 4 | Shoulder and upper arm before/after | `c14_04_shoulder.jpg` |
| 5 | Inguinal/hip before/after | `c14_05_inguinal.jpg` |
| 6 | Ankle/heel plus defect repair before/after | `c14_06_ankle.jpg` |
| 7 | Head–neck splice close-up before/after | `c14_07_head-neck.jpg` |
| 8 | Postorbital/brow/jugal: front 3/4, pure profile, close-up | `c14_08_postorbital.jpg` |
| 9 | Tail confirmation: profile, top, rear 3/4 | `c14_09_tail.jpg` |
| 10 | All six cranial display variants on the polished skull, including an attachment close-up | `c14_10_display_family.jpg` |
| 11 | Pigmented whole body, head and tail after cleanup (P1, P2, P7, P9) | `c14_11_gate8_after.jpg` |
| 12 | Regional Scale Architecture preservation | `c14_12_rsa.jpg` |
| 13 | Geometry-change heat map and accounting | `c14_13_accounting.jpg`, `c14_accounting.json` |

**Mesh on Tyler's PC** (`RaceBodies/out/`):
- `saurin_cleanup_base.npz`: the anatomical base mesh.
- `saurin_cleanup_surface_delta.npz` with `rebuild_cleanup.py`: rebuilds the exact 4.48 M-vertex scaled surface (error under 0.001 mm).
- `SaurinCleanup.blend` / `.fbx`: a preview decimated to 1.12 M triangles.

**Tools** are in `tools/rodin/cleanup/`:

| Tool | What it does |
|---|---|
| `zones.py` | Defines the authorized zones |
| `cleanup_ops.py` | The zone operators |
| `fixslivers.py` | Ankle seam-ring repair |
| `seamdist13.py` | Locates the head–neck splice seam |
| `seedmap13.py` | Carries the scale seeds onto the new mesh |
| `acct13.py` | Change accounting |
| `compose14.py` | Sheet layout |
| `build13.sh`, `r13.sh`, `g7var13.sh` | Build, render and display-variant scripts |

`tools/rodin/gate1/` holds `wf_saurin_head63.py` (`BROW_INT=3` adds the postorbital sweep; `BROW_INT=2` reproduces the accepted polish skull exactly), `assemble15.py` and `efield15.py`.

## Method

**1. Postorbital bar (skull SDF, field-difference surgery as in the polish).**
- The bar is now a sharp descending ridge (radius 0.46–0.50 cm). Its lower limb sweeps back and down along the jugal toward the quadrate line, tapering 0.36 → 0.22 cm.
- It used to stop in a rounded 0.78 cm foot, which read as a peg.
- The brow integration from the polish is unchanged.
- Only the 1,516 vertices whose field changed were re-surfaced. The patch was zipped with a 4.6 mm largest gap.

**2. Local meso-scale operators on the anatomical base, one per authorized zone.**
- Each zone gets a band filter along smoothed normals: the low-frequency body shape is kept, and only the feature band is broadened and/or lowered.
- Convex and concave relief have separate gains, so a crease can be filleted while a ridge is kept.
- Zone edges are feathered. Outside the feathered zones the base mesh is bit-identical.

| Zone | Operation |
|---|---|
| Sternum | Strips and bar lowered to ~35 %, broadened ~1.5 cm, grooves half-filled |
| Dorsal rod | Lowered progressively: ~35 % at the nape down to 10 % at its lower end, broadened ~2.5 cm, flanking grooves filled. It now fades into the spinal line. |
| Shoulder | Acromial crease filleted (concave gain 0.4) and broadened; convex shoulder structure kept (0.9) |
| Upper arm | Grooves softened (0.5) and lengthened; arm mass kept (0.65 on ridges) |
| Inguinal/hip | Thigh–pelvis creases filleted (0.4); convex form kept (0.95); residual hip fold included |
| Ankle front | The lump-with-step reduced to 20 % and blended into the tendon line |
| Heel | Achilles transition graded |

**Correction to my polish report:** the "heel lump" I flagged sits on the **front** of the ankle, as an anterior tendon bulge with a step under it, not behind the heel. I corrected it there under the same authorization, and also graded the heel/Achilles transition.

**3. Head–neck splice.** The visible stipple and facet band follows the Gate 6 head-patch seam on the neck. I traced it through the vertex provenance chain and de-noised that band in place with shape-preserving Taubin smoothing: median 0.04 mm, max 1.3 mm. Scales are carried across it, so there is no ring, density jump or field boundary.

**4. Ankle mesh defect.** The dark speck came from sliver and folded triangles in an old zip-seam ring at the ankle (u ≈ 16).
- I removed them with link-condition-safe edge collapses, which keep the mesh watertight and manifold, then smoothed that narrow band.
- The speck and most of the seam line are gone.
- Near-zero-area slivers still remain in that ring; they don't show in renders.
- A second, similar ring on the forearms (u ≈ 110) was **not** touched, because it is outside the authorized zones. It is listed as a finding below.

**5. Surface.**
- **Scale seeds** are carried from the polish surface: 137,494 kept, with 1,696 re-filled only where a base triangle was re-meshed.
- **Regenerated with the Gate 7 closure code:** the region map, then the surface relief from the carried seeds.
- **Gate 8:** fields rebuilt, then the same phenotype code re-run.

## Required reporting

**Vertex movement by authorized zone** (base mesh, against the accepted polish):

| Zone | Vertices | Median mm | p95 mm | p99 mm | Max mm |
|---|---|---|---|---|---|
| Postorbital/brow patch | 20,748 | 0.31 | 3.12 | 4.75 | 6.98 |
| Sternum | 58,997 | 0.42 | 2.05 | 3.81 | 7.01 |
| Dorsal rod | 43,489 | 0.88 | 5.59 | 8.03 | 9.40 |
| Shoulder | 47,260 | 0.25 | 2.23 | 3.92 | 7.05 |
| Upper arm | 60,966 | 0.23 | 1.37 | 2.07 | 3.48 |
| Inguinal/hip | 120,501 | 0.22 | 2.73 | 4.47 | 7.92 |
| Ankle front (lump) | 17,013 | 0.65 | 4.11 | 7.13 | 11.27 |
| Heel/Achilles | 38,652 | 0.53 | 3.29 | 4.46 | 5.84 |
| Head–neck splice band | 22,218 | 0.04 | 0.26 | 0.44 | 1.34 |
| Ankle seam repair | 49 | 0.61 | 3.53 | 4.84 | 4.84 |
| **Outside all zones** | **691,514** | **0** | **0** | **0** | **0.00** |

Zone counts include their feathered blend margins.

**Other checks:**

| Check | Result |
|---|---|
| Movement outside authorized zones | **None** (0.00 mm max over 691,514 vertices) |
| Watertight / manifold | 0 boundary edges, 0 non-manifold edges, 1 component (1,121,407 vertices / 2,242,810 faces) |
| Dimensions (height / width / depth) | 187.88 / 90.56 / 161.48 cm, unchanged |
| Tail taper | Section areas identical to the accepted polish (max difference 0.00 %); volume s12–98 = 17,696 cm³, unchanged; peak taper rate 11.7 cm²/cm (polish 11.2, measurement noise); tip and path untouched |
| Scale-family agreement | 99.455 % overall; 99.999 % on unmoved surface; 98.49 % on corrected surface (normals changed slightly where creases were filleted) |
| Display attachments | **No change beyond re-seating.** The six variants were rebuilt on the final skull with unchanged parameters (crest still 2.43 cm). Each is SDF-anchored on the new skull surface and blended into it; nothing floats, and no collar or socket forms (`c14_10`, attachment column). |

## Closure test

| Test | Result |
|---|---|
| No reviewed feature reads as a separate attached piece | **Mostly yes.** Sternum, shoulder, arm, hip, ankle and splice read as grown. The dorsal rod now tapers into the spine; its upper part between the scapulae is still a distinct, softened ridge (see findings). |
| Sharp structures stay sharp | **Yes.** Brow crest, postorbital ridge, jugal line and shoulder structure are kept; operators reduce feature bands, not plane breaks. |
| No correction makes the Saurin more human | **Yes.** No pectoral blocks, no groin or gluteal anatomy, no mammalian pads. |
| Tail taper intact | **Yes.** Identical to the polish. |
| Brow stays integrated and reptilian | **Yes.** |
| Postorbital bar reads as part of the cranial load path | **Yes.** Brow → postorbital → jugal → quadrate is now one continuous ridge in profile (`c14_08`). |
| No visible head–neck splice | **Yes** at neutral close-up (`c14_07`). |
| Pelvis/thigh/tail root one system | **Yes.** |
| Displays grow from the skull | **Yes** for all six. The swept-back pair shows a slightly thick base in close-up, still blended rather than socketed. |
| Regional Scale Architecture survives | **Yes.** |
| Gate 8 survives | **Yes** (`c14_11`): P1/P2/P7/P9, with tail pattern flow continuous. |
| Proportions and silhouette unchanged | **Yes.** |

## Findings for the author (documented, not changed)

1. **Dorsal rod, upper part:** between the scapulae it is still a distinct ridge with shallow flanking grooves. It is softened and continuous with the spine, but more lowering would start to erase the nuchal/spinal definition. Author's call.
2. **Front-of-ankle hairline:** a faint vertical line remains where the tendon groove was (`c14_06`, front view). It is a fine surface feature and could be finished in normal maps.
3. **Forearm zip-seam ring (u ≈ 110):** sliver triangles of the same kind as the ankle defect, outside the authorized zones. It shows as a faint line in close-up; the same repair applies if authorized.
4. **Swept-back display base:** slightly bulbous at the attachment in close-up; a narrower base radius would read more grown.

**STOP: final cleanup package. Awaiting author review.** No sex anatomy, age system, sliders, clothing/equipment, rigging, animation, gameplay, hero microdetail or UE5.

— Claude
