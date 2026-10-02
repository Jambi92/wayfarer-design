# Saurin Gate 2A: Organic Torso Integration (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/saurin-gate2a-organic-integration-refinement-order.md`
**Base:** Gate 2, `ea53933`. Torso refinement only. **Stopped at the checkpoint**; Gate 3 not started.

**Images** are in `reviews/images/saurin-gate2a/`:

| Deliverable | File |
|---|---|
| 1. Full body: front, profile, rear, front 3/4, rear 3/4 | `a2_01_five_views.jpg` |
| 2. Close torso: front, both front 3/4 views, profile | `a2_02_close_torso.jpg` |
| 3. Gate 2 vs Gate 2A, identical cameras | `a2_03_gate2_vs_2a.jpg` |
| 4. Untouched Rodin B1 vs Gate 2A, identical cameras | `a2_04_B1_vs_2a.jpg` |
| 5. Provenance accounting | `a2_05_accounting.jpg`, `a2_accounting.json` |

**Mesh on Tyler's PC** (`RaceBodies/out/`):
- `SaurinGate2A_Torso.blend` / `.fbx`
- `saurin_gate2a.npz`

The mesh has 191,116 vertices and 382,156 triangles. It is watertight: 0 boundary, 0 non-manifold, 0 orientation conflicts.

**Script:** `tools/rodin/gate1/g4.py`, surgery via `assemble5.py`.

## 1. How organic variation was introduced (same map, living tissue)

The Gate 2 map is unchanged: keel, chest shield, pectoral fan, costal arches, continuous ventral shield, long obliques. What changed is how each element is built. Every load path is now a **curved band** (quadratic Bézier on the surface chart) instead of a straight segment, and each band carries its own:
- **Width and prominence that breathe along its length.** Two incommensurate low-frequency modulations, so nothing repeats evenly.
- **Edge tension that differs between its two edges.** One edge firmer, one softer, which is the soft-to-firm transition.
- **Restrained fibre striation along its length.** About 0.3 mm amplitude, roughly 1.7 cm spacing, with drifting phase. It reads as fibre direction, not grooves.
- **Its own termination fade**, so bands end by blending rather than stopping.

Seeds differ left and right, so control points, phases and lengths vary slightly by side. That gives natural variation without changing pose or construction.

**Ventral shield**
- Still one continuous, unsegmented plate.
- **Its half-width breathes along its length,** about ±7% from two drifting frequencies.
- **Its crown line drifts slightly off the midline** and varies in intensity.
- **Margin tension differs by side.**
- **Four shallow compression/extension zones** were added. They are oblique, elliptical, irregularly placed, **not aligned across the midline** and only 0.8–1.4 mm deep, so they cannot read as rectus segmentation.
- **The transition into the lower trunk** keeps Gate 2's soft fade into the accepted pelvic platform.

**Shield → oblique integration**
- Three soft, tapering **interdigitating wedges** per side carry load from the shield margin down and out into the oblique chain.
- Their spacing, length and width are irregular.
- **The shield's margin groove is suppressed wherever a wedge crosses it**, so the "central panel + side straps" boundary dissolves into one system.

**Obliques.** Gentle S-curves rather than straight diagonals, with varying width and height and asymmetric edge tension.

**Costal arches**
- **Now one continuous band** from the sternal apex to the lateral costal margin.
- **Thinner toward the lateral end**, where it fades into B1's own rib relief.
- **Softened.** In Gate 2 the arch's lower edge stacked on B1's original undercut and produced a crack-like crease. That is now fixed.

**Pectoral fan**
- Three fascicles, each with a different start height, width, prominence, curvature and termination length.
- All three still converge on the humeral insertion, so the fan remains one functional system.

**Restored B1 tension**
- On the lateral thorax and flank (beyond |x| ≈ 14 cm, U 113–146), **45% of B1's own high-frequency relief is blended back in**: rib, serratus and tension breaks.
- These regions carry the new load paths and have no human organization to bring back.
- B1's ventral relief, where the pecs and abs were, was **not** restored.

**Global tissue undulation.** A very low-amplitude (about 1 mm), anisotropic, side-specific undulation across the region breaks up mathematically clean surfaces.

## 2. Lock and provenance accounting

Vertex-identity check against the **accepted Gate 1 mesh**:

| Locked region | Vertices | Identical |
|---|---|---|
| Free tail (F < −45) | 34,263 | **34,263** |
| Pelvis/sacrum/tail root + thighs (everything below U 100) | 100,985 | **100,985** |
| Lower legs + feet | 30,925 | **30,925** |
| Arms/hands (\|x\| > 19.5) | 16,241 | **16,241** |
| Head + neck column (U > 155) | 4,578 | **4,578** |

- **Everything changed since Gate 1** (Gate 2 + 2A together) lies in |x| ≤ 19.4, U 101.2–154.6: the torso zone.
- The only part above U 153 is 87 vertices along the lower edge of the clavicular strap. This is the authorized upper chest/shoulder transition. The neck column and shoulder architecture are untouched.
- **Hip locations, stance and proportions are unchanged**: every vertex below U 100 is identical.
- **Relative to Gate 2**, the accounting overlay shows the changes confined to the Gate 2 torso patch, with a seam relaxation of at most 0.7 cm.

## 3. Self-audit against the anti-regression requirements

| # | Requirement | Result |
|---|---|---|
| 1 | No recognizable human pecs | **Pass.** Keeled planar shield and asymmetric three-fascicle fan; no plate silhouette, no under-pec shelf (`a2_04` front and profile) |
| 2 | No six-pack / rectus ladder | **Pass.** No transverse segmentation. The shallow compression zones are oblique, irregular, staggered across the midline and ≤1.4 mm |
| 3 | No linea alba / navel | **Pass.** The midline carries a faint, drifting raised crown, not a groove; no navel |
| 4 | Shield not armor plating | **Pass, watch item.** No hard panel edge: the margin groove dissolves under the interdigitations and the width breathes. In strong raking light the shield's lateral bevel can still read slightly "designed" |
| 5 | No repetitive decorative grooves | **Pass, watch item.** Striation is at about 0.3 mm with drifting phase and irregular spacing. At close range on the obliques it can still read as faint parallel fibre lines; it can be lowered further if needed |
| 6 | Not a generic smooth tube | **Pass.** Thoracic depth and profile are unchanged from Gate 2/B1, and the surface carries variable tension. **Still below B1's density** of tension breaks on the ventral trunk (`a2_04`). This is the remaining gap |
| 7 | Pelvis/tail-root architecture unchanged | **Pass.** Vertex-identical |
| 8 | Proportions and stance unchanged | **Pass.** All limbs, pelvis and tail are vertex-identical; the torso silhouette is preserved |

**First impression at normal distance:** deep keeled thoracic shell, then a ventral system fanning into long oblique chains, then a narrow lower trunk running into the caudal pelvis. The front 3/4 reads as one system rather than "plate + panel + straps", although the shield is still the calmest area of the torso.

**STOP: Gate 2A checkpoint.** Gate 3 not started.

— Claude
