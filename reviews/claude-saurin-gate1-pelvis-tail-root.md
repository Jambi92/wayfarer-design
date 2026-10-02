# Saurin Gate 1: Pelvis / Sacrum / Tail-Root Integration (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/saurin-rodin-controlled-surgical-edit-directive.md` (ChatGPT, 2026-10-02). Gate 1 only.
**Status:** Stopped at the Gate 1 checkpoint. Gates 2–4 not started.

**Sources**
- Rodin **B1 = `c12`**: primary body, untouched except as listed below.
- Rodin **B2 = `c11`**: free-tail donor.
- **No rejected Phase A geometry, and no TS7–TS9 body geometry.**

**Images** are in `reviews/images/saurin-gate1/`:

| File | Contents |
|---|---|
| `g1_01_five_views.jpg` | Front, profile, rear, front 3/4, rear 3/4 |
| `g1_02_close_checks.jpg` | Close rear pelvis/tail root, close profile, low front-3/4 underside (crotch), close rear 3/4 |
| `g1_03_comparison.jpg` | Untouched B1 / Gate 1 / untouched B2, in profile, rear, rear 3/4 and front |
| `g1_04_accounting.jpg` | Provenance overlay: original vs relaxed seam band vs new vs donor |

**Scripts** (`tools/rodin/gate1/`):
- `g1.py`: the edit field.
- `stitch_mask.py`: the B1 edit mask.
- `assemble2.py`: cut and zip.
- `post.py`: seam fairing.
- `measure.py`: measurements.

**Mesh on Tyler's PC** (`RaceBodies/out/`):
- `SaurinGate1_RodinB1_B2tail.blend` / `.fbx`
- `saurin_gate1.npz`

The mesh is 125,944 vertices and 251,888 triangles. It is **watertight**: 0 boundary edges, 0 non-manifold edges, 0 orientation conflicts.

## 1. Method (preservation first)

1. **Edit zone only.** B1 and B2 were turned into signed-distance fields. The edit was written only where Gate 1 applies.
2. **Edit mask.** Every B1 vertex whose surface the edit changed by more than 0.8 mm was marked, then the mark was grown by 2 cm along the surface.
3. **Re-surface the mask only.** Only that masked patch of B1 was re-surfaced, at 3.5 mm.
4. **Keep everything else as original triangles.** The rest of B1 stays as its original Rodin triangles: **33,821 of the 37,627 B1 vertices are bit-for-bit original**.
5. **Join.** The original part and the re-surfaced patch were both cut along the same iso-line and zipped together.
6. **Fair the join.** The join was relaxed in a band at most 2.5 cm wide.
   - 1,435 original B1 vertices moved, by at most 2.25 cm.
   - All of these sit on the hip, lower trunk or thigh-top margin around the pelvis. None are on the chest, abdomen, neck, head, arms, hands, lower legs or feet.

## 2. What was deleted, retained and built

**B1 geometry deleted** (3,033 vertices, all between U 81–123 cm). Counts by adoption-map region:

| Region | Vertices |
|---|---|
| Posterior pelvis / glutes | 1,495 |
| Crotch | 599 |
| Dorsal strap (its lumbosacral end only) | 308 |
| Ventral abdomen (lowest edge above the crotch) | 259 |
| Lower-trunk flanks (lowest margin) | 180 |
| Hip/anterolateral pelvis | 123 |
| Thorax-shell label (dorsolateral margin at U 117–123; the 2 cm re-surfacing margin) | 69 |

**B2 geometry retained**
- B2's free tail beyond about F −47 cm, including its distal taper, curvature and fine tip.
- Only correction: the thick proximal part (F −33 to −72) was low-pass blurred at 2.5 cm to dissolve two transverse step-rings that B2 generated. These were a sudden 1.8 cm change in diameter around F −50, plus a ring at the cut. The distal tail and tip are untouched.
- B2's root, buttocks, legs and body are discarded.
- B2 was re-centered laterally (it sat 8 cm off-axis) and turned 1.3° so it runs straight back. **No rescale was needed**: it uses the same Rodin-unit-to-cm factor as B1.

**Newly built**
- **Gluteal hemispheres and cleft removed.** An elliptical carve cuts the posterior pelvis back to F −7 cm at its centre, receding smoothly outward. It has no rectangular edges.
- **Sacral/caudal platform and proximal tail root.**
  - One continuous sweep from inside the lumbosacral region into the caudal base.
  - At the B2 junction it morphs into the donor tail. It is a signed-distance interpolation over F −35 to −47, not a union, so there is no attachment crease.
  - The base is near pelvis-wide.
- **Restrained dorsal ridge.** It continues B1's dorsal midline strap over the platform onto the tail dorsum, fading toward the junction.
- **Neutral crotch.**
  - The sexed form was removed by replacing that region with a low-pass, 4 cm blurred version of **B1's own local surface**, set back 6 mm.
  - It is trimmed by a ventral fairing curve that runs from the lower abdomen to the perineum.
  - No reproductive anatomy was invented. The region is a smooth saddle between the thigh roots.

## 3. Measurements (H = 188 cm)

| Measure | Value | ÷ H |
|---|---|---|
| Standing height | 188.0 cm | 1.000 |
| **Tail length** (centreline from where it leaves the original B1 back line, F −11 / U 101, to the tip) | 128.0 cm (new root 34.6 + donor 93.4) | **0.681** (target 0.65–0.70) |
| **Proximal tail / caudal base section** (perpendicular to the axis, at F −23 / U 95) | 28.4 w × 21.1 h cm | **0.151 × 0.112** |
| Root–donor junction section (F −40 / U 86) | 18.8 w × 19.5 h cm | 0.100 × 0.104 |
| Section at F −14 (still inside the pelvic mass; not a free-tail section) | 39.1 × 40.2 cm | — |
| **Hip spacing** | unchanged | 0.152 → 0.152 |

- The caudal base is stronger than TS8 (0.10 × 0.11) and about pelvis-wide.
- The legs and femoral heads were not edited.

## 4. Confirmation: no non-Gate-1 regions altered

- **Original Rodin triangles, untouched:** chest, abdomen above the lowest abdominal edge, neck, **head** (still Rodin's), arms, hands, knees, lower legs and **feet** (still Rodin size).
- **Edits that reach into adjacent regions**, all limited to transition:
  - **Dorsal lumbosacral surface above U 110:** up to 4.3 cm, tapering to 1.1 cm at U 116–120 and 0.1 cm by U 122. This is where the dorsal line has to turn into the platform.
  - **Thigh tops below U 86:** up to 3.7 cm, where the gluteal carve meets the posterior thigh. This is the "very local hip-joint transition" the directive allows.
- The B1 leg artifacts (knee plate, calf fin) are **still present**. They are outside Gate 1.

## 5. Self-check against the Gate 1 "must not read as" list

| Must not read as | Assessment |
|---|---|
| Human buttocks with a tail inserted between them | **Pass.** No hemispheres or cleft; the posterior pelvis is one platform flowing into the caudal base (rear and rear-3/4 close views) |
| Tube attached to the sacrum | **Pass, mostly.** The base is pelvis-wide and the dorsal line is continuous in profile. From straight behind, the smooth base still reads somewhat as a separate rounded mass (see §6) |
| Two gluteal balls surrounding a tail | **Pass.** The lateral gluteal remnants were carved out to |x| ≈ 21 cm |
| Genital/crotch form | **Pass in close-up; watch item in the full front view** (see §6) |
| Decorative tail on a human pelvis | **Pass.** The tail is one system from the lumbar dorsum through the platform, with a dorsal ridge carried across |

## 6. Known issues (honest list for review)

1. **Front silhouette.** B2's tail drops steeply right behind the pelvis, so from the front the tail is visible hanging between the legs, from about knee to crotch height.
   - Combined with the neutral saddle above it, this could be misread in the full front view.
   - I tried pitching the donor tail up 15° (shape unchanged). It did not fix the front read, because the steep drop starts in the root, so it was not adopted.
   - **Decision needed:** either accept B2's carriage, or authorize a flatter root/tail carriage. That is a pose and proportion change, not a shape change.
2. **The new surfaces are smoother than B1's sculpt.** The platform/base and the crotch saddle are clean, low-detail surfaces next to B1's dense musculature.
   - This is deliberate for Gate 1: structure first, no invented anatomy.
   - Against the anti-regression rule it is a visible difference in sculptural density.
   - Restrained muscular/tendinous organization of the caudal base (e.g. caudofemoral load lines) would be a later, separately authorized step.
3. **Steep tail start.** In profile the tail leaves the platform heading downward at about 45°, inherited from B2's curvature.
4. **Fine sliver triangles along the zipped seam** were relaxed but not remeshed. The renders show no visible line; a topology pass would be needed before rigging.

**STOP: Gate 1 checkpoint.** Gate 2 (torso) is not started.

— Claude
