# Saurin Gate 2: Torso Anatomical Translation (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/saurin-gate2-torso-translation-order.md` (ChatGPT, 2026-10-02)
**Base:** accepted Gate 1 refinement (`e751973`). Torso only. **Stopped at the Gate 2 checkpoint**; Gate 3 not started.

**Images** are in `reviews/images/saurin-gate2/`:

| Required item | File |
|---|---|
| 1–5. Front, profile, rear, front 3/4, rear 3/4 | `t2_01_five_views.jpg` |
| 6–8. Close front torso, close front 3/4 (both sides), close profile | `t2_02_close_torso.jpg` |
| 9. Before/after with identical cameras | `t2_03_before_after.jpg` (rows: untouched Rodin B1 / accepted Gate 1 / Gate 2), `t2_04_before_after_full.jpg` |
| 10. Geometry-accounting overlay | `t2_05_accounting.jpg`, `t2_accounting.json` |

**Mesh on Tyler's PC** (`RaceBodies/out/`):
- `SaurinGate2_Torso.blend` / `.fbx`
- `saurin_gate2.npz`

The mesh has 179,780 vertices and 359,512 triangles. It is watertight: 0 boundary edges, 0 non-manifold edges, 0 orientation conflicts.

**Scripts:**
- `tools/rodin/gate1/g3.py`: the torso field.
- `blur_torso.py`: the B1 torso low-pass.
- `assemble4.py`: in-place surgery with locks.
- `compose_t.py`: the sheets.

## 1. Method: translate, don't erase

1. **Low-pass of B1's own torso.** B1's ventral/lateral torso surface was low-passed: a 3.5 cm blurred signed-distance field, read back with C2 cubic interpolation, receded 1.5 mm.
   - This keeps B1's **volume, silhouette and thoracic depth**.
   - It removes the human organization that lives at that scale: the pectoral plates and under-pec shelf, the rectus blocks, the linea alba groove, and the navel.
2. **New organization on top.** A Saurin organization was laid on that base as smooth surface-normal offsets: designed load paths, bevels and grooves.
3. **Kept unchanged:** B1's own sternal keel strap (above U 138), the clavicular strap, the shoulders and the lateral rib/serratus relief beyond the edit fade.
4. **In-place surgery.** The edit was applied to the accepted Gate 1 mesh: re-surface only the changed patch, zip it in, and relax a seam band of at most 0.9 cm. Locked regions were excluded from the patch before re-surfacing.

## 2. The new ventral/lateral load paths (anatomical explanation)

The paths read thorax → lower axial trunk → accepted pelvis:

1. **Keeled chest shield**
   - **Replaces:** the human pectoral plate.
   - **What it is:** B1's sternal keel strap is kept as the midline keel. Each side of it, the old rounded pectoral plate is turned into a **planar facet sloping back from the keel**. The facet window is elliptical, so there are no box edges.
   - **Result:** the deep thoracic shell reads as a keeled shield rather than two plates on a flat chest. The under-pec shelf is gone; the facet runs into the ribcage.
2. **Pectoral fan**
   - **What it is:** three broad, flat fascicles run from the keel to a common humeral insertion. They converge toward the shoulder, separated by shallow grooves.
   - **Function:** it carries arm load into the keel and shield, which is the shoulder/chest relationship, without a human plate silhouette.
   - **Arms:** not edited.
3. **Costal arches**
   - **What they are:** B1's inverted-V costal margin, made continuous and load-bearing. They run from the sternal apex down and out along the costal margin, fading into the lateral rib relief.
   - **Function:** they bound the thoracic shell and give the strongest diagonal of the torso.
4. **Ventral shield**
   - **Replaces:** the six-pack.
   - **What it is:** **one continuous, unsegmented** central plate from the costal apex down to the Gate 1 pelvic platform, narrowing from about 13 to 7.5 cm wide.
     - It has a faint longitudinal crown, not a linea-alba groove.
     - Its margins are bevelled and set off by a shallow groove.
   - **Function:** this is the "restrained central ventral organization" the order allows, with no transverse segmentation.
5. **Long oblique load paths**
   - **What they are:** one broad strap each side, from the lateral thorax (below the fan, behind the costal arch) diagonally down and in to the pelvic platform at the inguinal level.
   - **Function:** with the costal arches they form a **diagonal chain from the deep thorax across the elongated lower trunk into the caudal pelvis**. This is the visible counterbalance link of the Counterbalanced Pelvic-Axial Architecture.
   - **Removed after review:** a counter-diagonal cross-brace was tried and taken out, because it made the abdomen busy and streaky.

## 3. Lock confirmation (vertex-level, against the accepted Gate 1 mesh)

| Locked region | Vertices | Changed |
|---|---|---|
| B2 free tail (F < −45) | 34,263 | **0** |
| Gate 1 pelvis, thighs and everything below U 100 | 100,985 | **0** |
| Lower legs and feet | 30,925 | **0** |
| Arms and hands (\|x\| > 19.5) | 16,241 | **0** |
| Head and neck (U > 153) | 5,087 | 77, all on the **lower edge of the clavicular strap** (U 153.0–154.6, front, \|x\| 1.6–18.5). This is the authorized "very local upper shoulder/chest junction", not the neck column |

**Totals**
- **Vertices changed:** 5,830 Gate 1 vertices, all inside \|x\| ≤ 19.4, U 101.2–154.6, F −6.9 to +17.6. That covers the anterior/lateral thorax, abdomen, flanks and lower trunk.
- **Seam band:** 1,155 vertices were copied and relaxed at the seam (≤ 0.9 cm).
- **Gate 1 seam:** the Gate 1 pelvis seam was not crossed. Edits fade out by U 103–109.

**No change to:** hip locations, stance, tail, head, arms, feet.

## 4. Anti-regression self-assessment (compared with untouched B1)

**Passes**
- The silhouette and thoracic depth are unchanged in profile; the torso is not tubular.
- The human organization is gone.
- The new organization is coherent and directional: keel, shield, fan, costal arches and obliques all read as continuous load paths.

**Honest shortfall**
- **The abdomen is quieter and smoother than B1's rectus sculpt.** The shield and obliques are clean, broad forms. B1's abs had more high-frequency tension and shadow.
- **The fan fascicles are somewhat regular.**
- These are the main risk under the "do not replace anatomy with absence of anatomy" rule.
- A later surface-integration pass could add restrained intramuscular tension within the shield and obliques (no segmentation) and vary the fan fascicles.
- I stopped here rather than add invented detail without review.

**Other notes**
- **Edge transition.** At the edit's lateral edge, B1's original rib/serratus relief meets the smoother re-organized surface. From some front-3/4 angles the original flank relief reads slightly stronger than the new interior.
- **Front tail silhouette.** Still as accepted in Gate 1, with the tail visible between the legs from the front.

**STOP: Gate 2 checkpoint.** Gate 3 (head/neck) not started.

— Claude
