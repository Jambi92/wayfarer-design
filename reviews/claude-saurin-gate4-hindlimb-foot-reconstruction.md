# Saurin Gate 4: Hindlimb / Foot Load-Path Reconstruction (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/saurin-gate4-limb-system-reconstruction-order.md`
**Base:** accepted Gate 3A, `147c650`. **Stopped for review**; Gate 5 not started.

**Images** are in `reviews/images/saurin-gate4/`:

| Required item | File |
|---|---|
| 1. Five full-body views | `l4_01_five_views.jpg` |
| 2. Close hindlimb: front, profile, rear | `l4_02_hindlimb.jpg` |
| 3. Close knee: front, lateral, rear 3/4 | `l4_03_knee.jpg` |
| 4. Close foot: dorsal, lateral, medial, front 3/4, plantar | `l4_04_foot.jpg` (right foot isolated so the medial and plantar views aren't blocked) |
| 5. Before/after vs the pre-Gate-4 mesh, identical cameras | `l4_05_before_after.jpg` |
| 6. Accounting overlay | `l4_06_accounting.jpg`, `l4_accounting.json` |

**Mesh on Tyler's PC** (`RaceBodies/out/`):
- `SaurinGate4_Legs.blend` / `.fbx`
- `saurin_gate4.npz`

The mesh has 530,044 vertices and 1,060,000 triangles. It is watertight: 0 boundary, 0 non-manifold, 0 orientation conflicts.

**Scripts:** `tools/rodin/gate1/`
- `foot.py`: the new foot.
- `g7.py`: the leg field.
- `blur_legs.py`, `seg_arm.py`.
- `assemble8.py`: surgery.

## 1. Method

**Skeleton kept.** Each leg keeps **its own B1 hip–knee–ankle axis**, so stance, hip positions and height are unchanged.

- **Hip:** (±13, 3.5, 86).
- **Knee:** left (−17.4, 2.8, 62); right (15.2, 3.0, 62).
- **Ankle:** left (−26.4, 0.2, 9.6); right (21.6, 1.6, 9.6).
- B1's two legs are not symmetric (the left splays wider), and that was preserved.

**Surface, in three layers:**

1. **Base.** A 3.2 cm low-pass of **B1's own leg surface**, built from B1 *without* the arms, because the hands hang beside the thighs. It keeps limb mass, silhouette and taper while removing:
   - the human quad, hamstring and adductor surface map;
   - the patellar knee cap;
   - the knee-plate and calf-fin generation artifacts.

   On top of that, a stronger local low-pass removes the patellar lump at the knee. The lower leg tapers by 1.5 cm into a narrower ankle, and B1's bulbous calf ball is reduced.
2. **Load paths.** Surface-conforming load paths, built the same way as the accepted Gate 3A neck work: projected curves with organically varying width and height that fade in and out, combined smoothly where they overlap.
3. **Feet.** The B1 feet are **replaced** by a new plantigrade foot (§3).

## 2. Load-path organization (pelvis → claws)

**Thigh.** Long directional planes rather than isolated bellies, one per function:

| Function | Structure |
|---|---|
| Extension | Femorotibial extensor plane on the anterior thigh |
| Hip stabilization / abduction | Iliotibial plane from the lateral hip to the anterolateral knee, overlapping the extensor |
| Rotation / flexion | Iliofibular band from the posterolateral hip to the lateral knee |
| **Caudofemoral interaction** | The Gate 1 caudofemoral bands insert on the posterior proximal thigh. A **caudofemoral continuation** carries that tail-generated load down the back of the thigh to the knee |
| Flexion | Medial flexor from the ischial region to the medial knee |
| Adduction | Broad medial adductor plane |

**Knee**
- Femoral termination as medial and lateral **condylar masses**.
- A **lateral collateral ridge** (stabilization).
- A **low extensor sheet** passing over the front: no patellar cap, since none is mechanically required here.
- A **posterior flexion volume**.
- A tibial transition below.

**Lower leg**

| Role | Structure |
|---|---|
| Load-bearing | A **tibial crest** line (anteromedial) |
| Front | An **anterior extensor** that narrows into a dorsal ankle tendon |
| Propulsion | An **asymmetric posterior propulsion mass**: the lateral head is longer and runs into the **calcaneal tendon**; the medial head is shorter and ends higher |
| Lateral | A **peroneal band** to the lateral ankle |

This gives clear front/back and medial/lateral organization and a taper into the ankle.

## 3. Foot: full reconstruction

The foot is plantigrade, about **34.1 cm long (0.181H)**, against B1's 45–50 cm (0.26H). It is broad and stable, with toe-out of 6°.

Chain:
1. **Calcaneal column → heel pad**, in stance contact.
2. **Talar/ankle block**.
3. **Tarsal block**: a structured midfoot with the **medial arch held off the ground**, so it is not a slab.
4. **Five-ray metatarsal fan**.
5. **Forefoot contact pad** under the metatarsal heads.
6. **Five long digits** with joint logic: phalanges **2-3-4-4-3** (I–V), joint swellings, and a resting arc.
7. **Claws** that **grow from the terminal phalanx**: a keratin sheath continuous with the last segment, curving down to the ground.

The contact surfaces are flat and left for later scale/thickening work. There are no pads or paws, and it is not digitigrade.

## 4. Lock accounting (vertex identity against Gate 3A)

| Locked region | Vertices | Identical |
|---|---|---|
| Free tail (F < −45) | 34,263 | **34,263** |
| Everything above U 80: Gate 1 pelvis/sacrum/tail root, Gate 2A torso, Gate 3A head/neck | 251,025 | **251,025** |
| Arms/hands | 8,998 | **8,998** |
| Tail between the legs (F < −18, \|x\| < 12) | 68,767 | **68,767** |

- **Changed:** 16,226 Gate 3A vertices, all at U 0–80: the legs and feet only.
- **Height:** standing height 188.0 cm (187.96, meshing).
- **Hips and stance:** unchanged.

## 5. Self-assessment and open issues

**Delivered**
- Human leg map, patella cap and the two B1 leg artifacts removed.
- Continuous pelvis → caudofemoral → knee → calcaneal path.
- A new plantigrade foot at about 0.18H with structured midfoot, metatarsal fan, articulated digits and claws.
- Stance and height unchanged.

**Honest gaps**
1. **Calf mass.** B1's calf is still the dominant lower-leg volume. It is reduced, but from the rear it still reads as a strong rounded mass rather than a fully elongated propulsion form.
2. **Thigh volume.** The thigh volume is B1's, low-passed. The new planes organize it, but the thigh still carries B1's overall human-athletic proportion. A stronger rebuild would re-shape the volume itself, which was not done to avoid changing silhouette or stance without review.
3. **Foot and proportions.** The foot is a clean structural build and smoother than the body's sculpt. Its proportions are the main thing to judge.
4. **Mesh density.** The legs were re-surfaced at 2.2 mm, so the mesh is heavier (about 1.06 M triangles). A decimate/remesh pass will be needed before any rigging.

**STOP: Gate 4 checkpoint.**

— Claude
