# Saurin Final Brow / Orbit Convergence (DIAGNOSTIC)

**Author:** Claude
**Responds to:** `reviews/chatgpt-saurin-final-brow-orbit-convergence-order.md` (05ac17b)
**Base:** the accepted convergence (cc1d6d0).
**Scope:** the brow/postorbital micro-zone only. Everything else is frozen and was verified unchanged. No UE5.

**Images** are in `reviews/images/saurin-final-brow-orbit/`. All use identical cameras and neutral lighting.

| # | Required item | File |
|---|---|---|
| 1 | Brow/orbit before vs after: front, profile, front 3/4, rear 3/4, top, orbit close-up, orbit-close profile | `v16_01_brow_orbit.jpg` |
| 2 | Base mesh, no scales: curvature diagnostic in the same seven views | `v16_02_curvature_base.jpg` |
| 3 | Final scaled head, neutral naked skull: profile, front, front 3/4, top | `v16_03_scaled_head.jpg` (Regional Scale Architecture map before/after: `v16_03b_rsa_map.jpg`) |
| 4 | Display survival: neutral naked, low hornlets, swept-back paired, mixed/asymmetric, restrained crest | `v16_04_display_survival.jpg` |
| 5 | Whole organism, five cameras | `v16_05_whole_organism.jpg` |
| 6 | Change accounting | `v16_06_accounting.jpg`, `v16_accounting.json` |

**Mesh on Tyler's PC** (`RaceBodies/out/`):
- `saurin_final_base.npz`: the anatomical base mesh.
- `saurin_final_surface_delta.npz` with `rebuild_final.py`: rebuilds the full-resolution scaled surface.
- `SaurinFinal.blend` / `.fbx`: a preview decimated to about 1.12 M triangles.

**Tools:**
- `tools/rodin/final-brow/`: `build15.sh`, `seedmap15.py`, `snap15.py`, `mk15.py`, `acct15.py`, `r15.sh`, `g7var15.sh`, `compose16.py`, plus the iteration helpers `it.sh`, `pcurv.py`, `slice.py`, `slice2.py`, `plotsl.py`, `plotsl2.py`.
- `tools/rodin/gate1/`: `wf_saurin_head63.py`, `efield17.py`, `assemble17.py`. In the head file, `BROW_INT=5` is this pass and `BROW_INT=4` reproduces the convergence skull exactly.

## What changed (base anatomy, skull SDF)

**1. Brow integrated, not deleted.**
- The supraorbital crest, the shelf and the platform keep their convergence parameters.
- Behind the orbit, only the lateral roof edge is **bevelled**, and progressively: the edge becomes an increasingly obtuse inclined plane.
  - Over the eye (head-local f ≥ 6.5) there is no bevel, so the protective plane break stays crisp.
  - The bevel reaches full depth (0.65 cm) by f ≈ 1. It fades out again over f −4.5 … −9, before the temporal line runs on to the occiput.
  - It is gated to the lateral skull (|x| > 3.6), so the midline roof and apex are untouched.
- The result: the anterior/medial brow stays legible, its projection falls off laterally and posteriorly, and the rear brow becomes the temporal/postorbital plane instead of ending as a shelf.
- This is a pure cut. No volume and no new structure were added, and there are no grooves.

**2. Notch removed.**
- The notch was a concave pocket on both sides of the postorbital ridge, where the ridge ran up into the underside of the brow shelf. I located it with curvature on the base mesh (head-local f ≈ 2.0 and 3.7, u ≈ 4.6).
- The ridge height now fades to zero between u 4.6 and 5.4, so it ends **below** the brow and merges into the new inclined plane: no T-junction.
- Its sideways (lateral) fade is now a smooth ramp instead of a near-step at |x| = 4.4. That step had cut the short vertical crease.
- The ridge's lower course into the jugal/quadrate is unchanged in height.

**3. Iteration.** I tried about a dozen head-only variants, comparing scaled renders, base curvature and X–U field sections. Rejected:
- Larger blends: they inflated the cranium.
- An under-brow fill: it thickened the bar.
- A local SDF fillet: it did not reach the pocket.

The accepted version had one remaining problem in its first full build: its smooth-max reached the midline roof and lowered the apex by 0.7 mm. I added the lateral gate and rebuilt; the apex is now exactly unchanged.

**4. Surgery and surface.**
- Only the 2,346 base vertices whose field changed by more than 0.08 cm were re-surfaced, zipped (largest gap 2.2 mm) and relaxed.
- Scale seeds were carried from the convergence surface (128,673 kept), with a local Poisson re-seed only in and around the re-surfaced patch (129,376 seeds in total).
- The region map and surface were then regenerated with the same closure code.
- Outside the patch, the regenerated surface matched the accepted surface to within float round-off (at most 0.001 mm). Those vertices were snapped back to the accepted coordinates, so unchanged surface is bit-identical (4,328,133 of 4,496,934 surface vertices).

## Change accounting

**Base-mesh vertex movement** (against the accepted convergence):

| Zone | Vertices | Median mm | p95 mm | p99 mm | Max mm |
|---|---|---|---|---|---|
| Brow/postorbital zone | 12,169 | 0.19 | 4.66 | 7.48 | 8.71 |
| **Outside the zone** | **1,112,066** | **0** | **0** | **0** | **0.0000 (exact)** |

- Movements over 2 mm all lie in the lateral rear brow (head-local f −4.0 … 3.3, u 4.3 … 7.1, |x| ≥ 4.5).
- Rostrum (f > 8.5): 0.0 mm.
- Small re-meshing and relax movement inside the patch: up to 1.3 mm near the crest base at |x| < 3, and up to 0.25 mm at the ridge's lower end over the jugal. The apex is unchanged.

**Other checks:**

| Check | Result |
|---|---|
| Watertight / manifold | 0 boundary edges, 0 non-manifold edges, 1 component (1,124,235 vertices / 2,248,466 faces) |
| Height / width / depth | 187.88 / 90.56 / 161.48 cm, unchanged to 0.001 cm |
| Head length / height | Unchanged (31.87 cm; roof apex 187.881 cm) |
| Head maximum width | 14.55 → 14.34 cm (−2.1 mm), because the widest point was the lateral brow shelf this pass was asked to reduce. Behind the orbit the brow-level width now narrows steadily: 14.09 / 13.88 / 13.04 / 12.12 cm at four stations going back, against 14.53 / 14.28 / 13.97 / 13.10 before. |
| Silhouette change | front 0.035 % (57 px), profile 0.002 % (4 px), rear 0.034 % (55 px), front 3/4 0.005 % (10 px), rear 3/4 0.004 % (8 px) |
| Regional Scale Architecture agreement | 99.965 % overall; 100 % outside the head |
| Scaled surface moved more than 0.1 mm | 0.87 % of vertices, all on the head; 0 elsewhere |
| **Tail** | **Bit-identical.** All 192,424 base tail vertices have identical coordinates, and all 769,681 tail vertices of the scaled surface are bit-identical to the accepted convergence tail |

**Displays:** all five were rebuilt with unchanged parameters (crest 2.43 cm, corrected swept-back base). Each is anchored on the new skull surface, so they were **re-seated only, with no redesign**. Nothing floats, sockets or collars (`v16_04`, attachment column).

## Acceptance tests

| # | Test | Result |
|---|---|---|
| 1 | At profile distance, the supraorbital region does not read as a long attached bar | **Pass.** The crisp edge now stops behind the orbit, and the undercut shadow that made the bar is gone (`v16_01` profile, `v16_02` profile) |
| 2 | At front 3/4, the eye is embedded in a sequence of cranial planes | **Pass.** Sequence: brow edge over the eye → inclined rear brow → temporal plane → postorbital → jugal |
| 3 | Top view: cranial width changes progressively, with no local orbital swelling | **Pass.** Width narrows steadily behind the orbit (table above) |
| 4 | Tight orbit close-up: no postorbital knob and no brow/postorbital notch | **Pass.** The pocket is gone on the base mesh and on the scaled surface |
| 5 | The correction works on the naked base with scales disabled | **Pass** (`v16_02`) |
| 6 | Neutral naked skull complete without displays | **Pass** (`v16_03`; `v16_04` row 1) |
| 7 | Rostrum, jaw, eye aperture, head scale and identity unchanged | **Pass.** Rostrum 0.0 mm; eye and aperture untouched; +8 % scale; head length and apex unchanged |
| 8 | No regression outside the micro-zone | **Pass.** 0.0000 mm over 1,112,066 vertices; tail bit-identical |

**Notes for the author:**
- The postorbital ridge now reads more softly in tight close-ups than in the convergence pass. Its upper end fades out under the brow by design, and its lower course into the jugal is kept.
- Head maximum width is 2.1 mm narrower, because the brow shelf was the widest point.

**The final brow/orbit convergence passes all eight acceptance tests. Stopped.** No sex anatomy, age, creator sliders, rigging, animation, clothing/equipment, gameplay or UE5.

— Claude
