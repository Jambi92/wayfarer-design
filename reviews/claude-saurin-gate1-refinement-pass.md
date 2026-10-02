# Saurin Gate 1: Refinement Pass (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/saurin-gate1-refinement-order.md` (ChatGPT, 2026-10-02).
**Status:** One constrained refinement pass on the current Gate 1 mesh (commit `b2164a1`). Stopped for review. Gate 2 not started.

**Images** are in `reviews/images/saurin-gate1-refinement/`:

| Required item | File |
|---|---|
| 1. Same five full-body views | `r1_01_five_views.jpg` |
| 2–5. Close rear pelvis/tail root, close profile, low front-3/4 underside, close rear 3/4 | `r1_02_close_checks.jpg` |
| 6. Direct before/after against current Gate 1, same cameras | `r1_03_before_after.jpg` (close views), `r1_04_before_after_full.jpg` (full rear and profile) |
| 7. Accounting overlay of what changed in this pass | `r1_05_accounting.jpg` |
| 8. Lock confirmation | §3 below, and `r1_accounting.json` |

**Mesh on Tyler's PC** (`RaceBodies/out/`):
- `SaurinGate1R1_RodinB1_B2tail.blend` / `.fbx`
- `saurin_gate1_r1.npz`

The mesh has 137,574 vertices and 275,096 triangles, and is watertight: 0 boundary, 0 non-manifold, 0 orientation conflicts.

**Scripts:** `tools/rodin/gate1/g2.py` (refined field) and `assemble3.py` (in-place surgery on the Gate 1 mesh).

## 1. Method

The Gate 1 mesh is the base. It was not reverted or rebuilt.

1. The refined field was compared with the Gate 1 field at every Gate 1 vertex.
2. Only the vertices it changes were marked, then grown 1.5 cm along the surface.
3. **Locked free-tail vertices (F < −45 cm) were excluded from the mark before anything else.**
4. That patch alone was re-surfaced at 3.5 mm.
5. It was cut and zipped to the untouched remainder along a shared iso-line. The new seam was relaxed in a band at most 1.8 cm wide, with locked vertices pinned.

## 2. What was changed

### Refinement 1: posterior pelvic/sacral platform

**Planar definition**
- On the platform portion of the root only (axis F > −34), the cross-sections were sharpened:
  - crisper plane transitions;
  - stronger dorsolateral bevels;
  - a 1 cm flatter sacral crown.
- This gives a sacral plate bounded by bevel planes instead of a dome.
- These changes taper out before the root→donor morph zone, so the free tail is unaffected.

**Directional transition from the lower axial trunk into the tail**
- Paired low epaxial bands start on the lumbar dorsum about 8.5 cm either side of the midline. They converge to about 5 cm as they run onto the tail dorsum, either side of the existing restrained dorsal ridge.
- They are broad and low, about 0.5 cm proud, and blended over 2.6 cm.
- They are load-path organization, not muscle-belly separations.

**Platform vs free tail**
- The planar, bevelled platform section changes to B2's round free-tail section through the existing morph zone.
- The chevron where the bevels end marks the end of the platform.

### Refinement 2: pelvis-to-femur integration

**Caudofemoral load bands** (left and right). This is the reptilian caudofemoralis analogue:
- Each tapered band runs from the ventrolateral caudal base (|x| 6.5, F −27, U 89) forward and down into the posterior proximal thigh (|x| 11, F −2.5, U 81.5).
- It is blended into the preserved thigh over 5 cm.
- This is what ties the femora to the tail-base mass.

**Pocket fix.** A concave pocket formed between band, thigh and platform, and read as a pit or opening. It was found with a morphological closing test and closed with a local fill (|x| 8.6, F −10, U 89.5). The re-test shows no remaining pocket in the new geometry.

**Hips and stance.** Hip joint locations and stance are **unchanged**. No femoral or leg relocation; hip spacing stays 0.152H.

### Refinement 3: ventral/underside neutrality

- **The fault.** In Gate 1, the neutral saddle and the tail underside left a slot between them, about 7 cm deep at the midline (between F −4 and +3 at U 92–95). That slot was the fold or opening-like form.
- **The fix.** A low, wide perineal transition closes it. The underside now runs continuously from the lower abdomen, across the saddle, into the tail underside.
- There is no slit, cavity, aperture, cloaca, bulge or organ. The saddle itself is unchanged from Gate 1, so it is still B1's own low-passed surface.

## 3. Lock confirmation (exact, vertex-level)

| Locked item | Result |
|---|---|
| **B2 free tail** (all 34,263 Gate 1 vertices with F < −45) | **34,263 / 34,263 identical**: same positions and same triangles. Tail length is unchanged at 0.681H; taper and curvature are untouched |
| Original B1 geometry in Gate 1 (35,256 vertices) | **34,133 identical**. 1,123 affected, all at the pelvic margin (details below) |
| Chest, abdomen, head, neck, shoulders, arms/hands, lower legs, feet | **Untouched.** None of the affected vertices are in these regions |

**Where the 1,123 affected B1 vertices are.** All lie within |x| ≤ 19.6, U 71.5–119.5, F −11.5 to +4.9.

| Region (adoption-map label) | Vertices | Notes |
|---|---|---|
| Remaining posterior-pelvis margin | 793 | |
| Hip / anterolateral pelvis | 157 | |
| Thigh tops | 77 | The caudofemoral insertion junction (Refinement 2), nothing below U 71.5 |
| Lumbar dorsolateral margin | 95 | U ≤ 119.5. Where the epaxial bands start. These carry the "thorax shell" and "lower-trunk flanks" labels in the planning map, but sit at the old Gate 1 zone border, not on the chest |
| Crotch | 1 | |

Of these vertices, 383 were only relaxed at the new seam, by at most 1.46 cm.

## 4. Measurements

| Measure | Gate 1 | Refined |
|---|---|---|
| Standing height | 188.0 | 188.0 |
| Tail length | 0.681H | 0.681H (locked) |
| Proximal tail section at F −23 (w × h) | 28.4 × 21.1 cm | 28.1 × 23.5 cm (height includes the caudofemoral band origins) |
| Root–donor junction section | 18.8 × 19.5 cm | 18.8 × 19.5 cm |
| Hip spacing / hip-joint positions | 0.152H | **unchanged** |

## 5. Self-check against the success test

**Does the pelvis now read as a structurally organized Saurin sacral/caudal system?**
- **Better than Gate 1.** The platform now has a sacral plate, bevel planes, converging dorsal load bands, and visible tail-to-femur bands.
- **No human buttocks:** no hemispheres and no midline cleft. The only midline element is the restrained dorsal ridge, which sits proud of the surface rather than recessed.
- **No reproductive design:** the slot is closed and nothing is an aperture.
- **Rodin sculpt:** the sculpt outside the pelvis is unchanged.

**Open points for review**
1. **Bands are the one subjective call.** The epaxial bands and ridge give three longitudinal elements over the platform. In the close rear view they read as clear structure, but they could be judged slightly too graphic. Tell me if you want them halved.
2. **Small round form at the right hip** (close rear view). This is B1's original "bolt knob" generation artifact, which sits outside the zone and was left alone. It was in the untouched source.
3. **New-surface density.** The new surfaces are more organized but still smoother than B1's dense sculpt. That is intentional, to avoid inventing musculature.
4. **Still open from Gate 1:**
   - The tail carriage seen from the front: the free tail is locked.
   - B1's knee-plate and calf-fin leg artifacts.

**STOP: Gate 1 refinement checkpoint.** Gate 2 not started.

— Claude
