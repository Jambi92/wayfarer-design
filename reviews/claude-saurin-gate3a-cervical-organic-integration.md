# Saurin Gate 3A: Cervical Organic Integration (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/saurin-gate3a-cervical-organic-integration-order.md`
**Base:** Gate 3, `82e30d0`. Head/neck/thorax transition only. **Stopped for review**; Gate 4 not started.

**Images** are in `reviews/images/saurin-gate3a/`:

| Required item | File |
|---|---|
| 1. Full-body five-view | `ha_01_five_views.jpg` |
| 2. Close head/neck five-view | `ha_02_close_head_neck.jpg` |
| 3. Gate 3 vs Gate 3A, identical cameras (7 views including close rear and underside) | `ha_04_gate3_vs_3a.jpg` |
| 4–5. Close rear cervical; underside / front-3/4 jaw-throat | `ha_03_rear_and_underside.jpg` |
| 6. Geometry accounting: edit zone vs locked | `ha_05_accounting.jpg`, `ha_accounting.json` |

**Mesh on Tyler's PC** (`RaceBodies/out/`):
- `SaurinGate3A_HeadNeck.blend` / `.fbx`
- `saurin_gate3a.npz`

The mesh has 302,569 vertices and 605,050 triangles. It is watertight: 0 boundary, 0 non-manifold, 0 orientation conflicts.

**Script:** `tools/rodin/gate1/g6.py`, surgery via `assemble7.py`.

## 1. What changed and how

**Unchanged from Gate 3:**
- the TS6.1 head construction;
- the cervical loft, so neck height, gross width and depth stay the same;
- head placement;
- the cut and the low-pass of the B1 base;
- the fade-out above the locked Gate 2A torso.

**Replaced:** the Gate 3 tissue system. Gate 3 used partly-buried tubes, which made long, nearly parallel strips. Each cervical structure is now a **surface-conforming tissue path**:
- a spline projected onto the neck surface;
- evenly resampled and smoothed so there is no scalloping;
- expressed as a smooth outward offset of the surface rather than an added volume.

Along its length, each path varies its **width and height** with organic modulation and **left/right** variation, and it **emerges from and disappears into** neighbouring tissue (height fades to zero at both ends). Where paths overlap they combine smoothly (root-sum-square). One structure can pass under or into another without a crease.

| Requirement | Construction |
|---|---|
| Break the fluted column | Staggered origins and insertions. A **broad deep nuchal mass** is crossed obliquely by a **narrower superficial slip** that starts lower and diverges more. Lateral layers differ in width and depth. **Interdigitating slips** cross between the two lateral layers. No strips run in parallel over the full neck length |
| Cranial-base seating | A **short three-ray occipital/posterior-temporal fan** per side diverges from the posterior skull into the nuchal mass. The temporal/postorbital region feeds lateral layer 1. The skull-to-neck blend is widened (3.0 to 3.6) so the cranial base sits in the cervical mass. The axial midline line now runs **from the occipital crest continuously into B1's dorsal strap** instead of ending in a knob |
| Mandibular/throat integration | A **mandibular-base sling** runs from each jaw angle toward the throat midline. This gives the jaw underside depth, removes the horizontal ledge, and keeps the jaw edge readable. The **broad throat sheet** is slightly asymmetric and flows down to the chest shield. No sternocleidomastoid analogy, and no pouch, dewlap or other organ (an intermediate trial produced a throat bulge and was discarded) |
| Lower neck into shoulder/thorax | Terminations **fan out and submerge**. The nuchal system ends in a **three-ray scapular fan** into the medial dorsal thorax. Lateral layer 1 spreads onto the acromial shoulder; layer 2 onto the lateral clavicle. The throat sheet splits into **two short fingers** onto the chest-shield crown. All heights fade to zero before the locked boundary, so no vertical ribbon ends |
| Visual hierarchy | Relief is low, 0.3–1.5 cm. The neck reads as the connecting bridge, not a feature: silhouette unchanged, no new mass |

## 2. Vertex-identity accounting

**Locked, identical to Gate 2A (so also to Gates 1 and 2A):**

| Region | Vertices | Identical |
|---|---|---|
| Free tail | 34,263 | **34,263** |
| Pelvis/sacrum/tail root + thighs (below U 100) | 100,985 | **100,985** |
| Lower legs + feet | 30,925 | **30,925** |
| Gate 2A torso (below U 148) | 179,697 | **179,697** |
| Arms/hands (\|x\| > 19.5) | 16,241 | **16,241** |

**Modified relative to Gate 3:**
- 84,084 vertices, all within U 148.0–187.5 and |x| ≤ 19.3: the head/neck/upper-shoulder edit zone.
- **Skull:** the TS6.1 head construction is identical. 20,957 of 25,281 front-skull vertices (U > 176) are bit-identical to Gate 3. The rest were re-surfaced only because the posterior skull-base blend was widened; their shape comes from the same head construction.
- **Height:** standing height is 188.0 cm (187.96, meshing). Hips, stance and proportions are unchanged.

## 3. Self-check against the order's test

> Does the head appear to have grown from a specialized cervical structure that itself grows naturally into this thorax?

**Improved, not perfect.**
- **Rear and rear-3/4:** the nuchal system now reads as layered, crossing tissue that seats the skull and spreads into the shoulders. No curtain of strips.
- **Profile:** layered lateral planes with interruptions.
- **Underside:** the jaw base flows into the throat without a ledge.

**Watch items**
1. **Fine scratch texture.** A faint fine texture is visible on the neck in some close views. It comes from re-surfacing a faceted B1-derived field at 2 mm; it is not design intent and would vanish in a remesh/surface pass.
2. **Head scale.** The head-scale vs neck-length question raised in Gate 3 is unchanged by design; this order preserved dimensions.
3. **Relief strength.** Relief is deliberately restrained. If reviewers want the layers stronger, the heights can be scaled without changing the layout.

**No** scales, colour, horns, crests, eye detail, claws, limb, pelvis or tail changes. No human neck muscles. No new biology.

**STOP: Gate 3A checkpoint.**

— Claude
