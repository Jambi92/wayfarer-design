# Saurin Gate 3: Head / Neck / Thorax Integration (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/saurin-gate3-head-neck-thorax-integration-order.md`
**Base:** locked Gate 2A, `3467b75`. **Stopped at the Gate 3 checkpoint.**

**Images** are in `reviews/images/saurin-gate3/`:

| Required item | File |
|---|---|
| 1–5. Full body: front, profile, rear, front 3/4, rear 3/4 | `h3_01_five_views.jpg` |
| 6–10. Close head/neck: front, profile, rear, front 3/4, rear 3/4 | `h3_02_close_head_neck.jpg` |
| 11. Pre-Gate-3 vs Gate 3, identical cameras | `h3_03_before_after.jpg` (close), `h3_04_before_after_full.jpg` (full body) |
| 12. Provenance accounting | `h3_05_accounting.jpg`, `h3_accounting.json` |

**Mesh on Tyler's PC** (`RaceBodies/out/`):
- `SaurinGate3_HeadNeck.blend` / `.fbx`
- `saurin_gate3.npz`

The mesh has 294,964 vertices and 589,844 triangles. It is watertight: 0 boundary, 0 non-manifold, 0 orientation conflicts.

**Script:** `tools/rodin/gate1/g5.py`, surgery via `assemble6.py`.

## 0. Interpretation decision (please confirm)

Through Gate 2A the body still carried **B1's own Rodin head**. That head is on the mandatory rejection list ("Rodin's oversized/alternate head in place of the accepted Saurin cranial direction"). Every adoption directive names the **accepted TS6.1 cranium** as the cranial authority.

Gate 3 therefore:
- **removes the Rodin head and neck column**: 2,852 vertices above U 165;
- **installs the accepted TS6.1 head**: the same signed-distance construction, at its canonical scale and the same head-frame origin used since TS6.1;
- **does not redesign the head**: no facial detail, scale, crest, horn or eye work.

Standing height stays 188 cm: the head top is at 188.0, as before.

## 1. Anatomical explanation

**Cervical volume.** A new cervical loft carries the skull base (about 11 × 13 cm) down into the B1 cervicothoracic base (about 28 × 27 cm).
- It is a planar-chamfered section, not a cylinder.
- Its dorsal extent is greater than its ventral, so it is deep behind and slimmer at the throat.
- It leans slightly forward under the skull for an upright obligate biped.
- B1's human-looking neck cords and trapezius slope at the cervicothoracic base were replaced by a 3 cm low-pass of **B1's own surface**, so the shoulder silhouette is kept.

Four layers of tissue planes are built on that volume. They are broad, partly sunk forms, not cords.

1. **Dorsal cranial-to-thoracic load path**
   - Paired **broad nuchal planes** run from the occipital region down and out to the upper scapular region and medial dorsal thorax.
   - Between them, the **axial midline line** runs continuously from the occipital crest into B1's dorsal axial strap, which already continues to the sacral ridge and tail dorsum.
   - This visibly ties the skull to the same axial system as the pelvis and tail.
   - It is not a trapezius cape: no sheet spreads to the acromion. The planes converge on the medial scapula.
2. **Lateral cervical organization.** Two separate layers keep jaw, neck and shoulder from fusing into one wedge.
   - **Layer 1:** posterior/temporal cranial base, then the cervical column, then the lateral shoulder (acromial) foundation. This stabilizes head turning and carries head mass into the girdle.
   - **Layer 2:** a flatter plane in front of layer 1, from the mandibular base to the **lateral** clavicular strap.
   - Layer 2 deliberately does **not** run to the sternum, so there is no sternocleidomastoid pattern.
   - The groove between the two layers marks where articulation and motion happen.
3. **Ventral jaw/throat-to-thorax transition**
   - **One broad, low ventral sheet** runs from the deep posterior mandibular base and spreads onto the top of the chest shield beside B1's sternal keel.
   - The throat contour is modest.
   - No dewlap, gular organ, gill, venom, display or respiratory structure; nothing inflatable.
4. **Termination into the Gate 2A shoulder/chest system.** All cervical layers end at or interleave with structures that already exist:
   - **nuchal planes:** medial scapular region;
   - **lateral layer 1:** acromial shoulder;
   - **lateral layer 2:** lateral clavicular strap;
   - **ventral sheet:** chest-shield crown beside the keel.

   Every Gate 3 change fades to zero between U 151.8 and 148.6, so the chest shield, pectoral fan and Gate 2A load paths are untouched.

## 2. Lock and provenance accounting

Vertex-identity check against **Gate 2A**:

| Locked region | Vertices | Identical |
|---|---|---|
| Free tail (F < −45) | 34,263 | **34,263** |
| Pelvis/sacrum/tail root + thighs (everything below U 100) | 100,985 | **100,985** |
| Lower legs + feet | 30,925 | **30,925** |
| Gate 2A torso below the cervicothoracic seam (everything below U 148) | 179,697 | **179,697** |
| Arms/hands (\|x\| > 19.5) | 16,241 | **16,241** |

- **Changed relative to Gate 2A:** 7,553 vertices, all within U 148.0–188.0 and |x| ≤ 17.4. That is the head, neck and upper shoulder boundary.
- **Unchanged:** hip positions, stance, height, tail, feet, pelvis and abdomen.

## 3. Self-audit against the anti-regression tests

| # | Test | Result |
|---|---|---|
| 1 | Head more human | **Pass.** TS6.1 unchanged: no chin, nose, lips or pinnae |
| 2 | Generic dragon/lizard head | **Pass.** It is the accepted head, and the Rodin generic long head is removed |
| 3 | Cylindrical / featureless neck | **Pass.** Planar chamfered section with four distinct tissue layers. See the stalk note below |
| 4 | Human neck muscles dominate | **Pass.** The SCM-like cords and trapezius slope of B1 are gone. The lateral layers attach to the shoulder and lateral clavicle, not the sternum |
| 5 | Head looks attached | **Mostly pass.** Dorsal, lateral and ventral layers all start on the skull and the axial line is continuous. From straight in front, the jaw base still shows as a distinct ledge, which is TS6.1's own gular plane |
| 6 | Neck so massive it destroys the shoulder silhouette | **Pass.** The neck tapers; the shoulder silhouette is B1's |
| 7 | Gate 2A overwritten | **Pass.** Vertex-identical below U 148 |
| 8 | Pelvis/tail changed | **Pass.** Vertex-identical |
| 9 | Unapproved biology | **Pass.** None |
| 10 | Sophistication decreases | **Watch.** The new neck is cleaner and quieter than B1's sculpt and needs the Gate 2A-style organic pass if accepted |

**Main proportion issue for review.**
- At canonical scale the TS6.1 head is much smaller than the Rodin head it replaces, and B1's frame is massive.
- In the full-body views (`h3_04`) the head reads small and the neck reads relatively long, close to the "bird-like stalk" risk.
- Options:
  - **(a)** accept as is (canon head proportion);
  - **(b)** a small uniform head scale-up (about +10–15%) with a shorter cervical span;
  - **(c)** lower the head frame by 2–3 cm and thicken the upper neck.
- Each changes head proportion or height, so I have not done any of them without approval.

**STOP: Gate 3 checkpoint.** No hands, feet, scales, display structures or materials.

— Claude
