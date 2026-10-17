# RAC RM-OT-05AK — Gorrund AC2 via UI Mesh Filter: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05ak-gorrund-ac2-mesh-filter-order.md` (90c6fc7)
**Source:** `GO-05AJ_preflight_baseline.blend` (sha256 `453ee2ba…d6d5`). After the masks were saved, the geometry read back with 0.000 mm deviation from this baseline.
**Executor:** Claude. All authoring was done in the Blender 5.2.2 UI on Tyler's PC (box masks, Mask menu, Mesh Filter tool). Cloud scripts were used only for read-back, gates and evidence.

## Verdict

**05AK AC2 FILTER ROUTE NOT CREDIBLE / STOP**

The first, conservative Mesh Filter application (AK1, Surface Smooth) produced **15 flipped faces**. Everything else in the geometry gate was clean:
- 0 seams, 0 SI, 0 degenerates;
- 1 / 0 / 0 topology;
- every protected region and the 05AI torso at 0.000 mm.

The surface moved very little (limb median 0.29 mm, p95 0.86 mm, max 3.1 mm).

Order §9 permits the one-time sliver reaction only for **≤ 6** isolated flips and says to STOP when there are more. So I used no repair, no rerun and no AK2/AK3. The active checkpoint stays the **passed 05AI AC1** (hashes re-verified this session). AC3 was not started.

## 1. Masks (UI only; order rule respected)

All mask work was done in `GO-05AK_working.blend`, saved before any filter. Front orthographic view:
1. Mask > Clear.
2. Box-mask both arms and both legs.
3. Mask > Invert.
4. **Joint-preservation boxes**, roughly ±4 cm about each joint centre taken from the rig weight boundaries:
   - elbows (z 137 / 134 cm);
   - wrists (117 / 113);
   - knees (55);
   - ankles (9).
5. Mask > Smooth Mask ×3. This feathers the limb/torso boundary and gives the joints their soft fall-off into the bellies.
6. **Final hard boxes, after all feathering:**
   - torso;
   - head;
   - both shoulder tops;
   - front hip / genital;
   - both hands;
   - feet;
   - both armpit strips;
   - right view: free tail;
   - right view: top of the feet.

No Smooth Mask was run after any hard box.

Read-back of the saved `.sculpt_mask` (`checks/ak_mask_readback.json`):

| Check | Result |
|---|---|
| 05AF protected sets (head, tail, tail junction, genital, perineal, hands, feet, all) | min 1.0, 0 vertices < 1 |
| 05AI torso / glute / pelvis_other | min 1.0, 0 vertices < 1 |
| Joint centres (mean mask within ±2.5 cm) | elbows 0.96 / 0.96, wrists 0.99 / 1.0, knees 0.96 / 0.98, ankles 0.995 / 0.92 |
| Mid-belly zones (mean mask) | biceps 0.31 / 0.22, forearms 0.01 / 0.01, thighs 0.08 / 0.05, calves 0.00 / 0.00 |
| Sculptable share (mask < 0.5) | upper arm 0.54, forearm 0.60, thigh 0.77, shin 0.78 |

The joint centres are clearly more protected than the mid-belly tissue, as required.

## 2. AK1 — the only filter application

The settings below are as shown in the UI.

| Setting | Value |
|---|---|
| Tool | Mesh Filter |
| Filter Type | **Surface Smooth** |
| Strength | 1.000 |
| Deform Axis | X Y Z |
| Orientation | Local |
| Shape Preservation | 0.500 |
| Per Vertex Displacement | 0.500 |
| Application | one horizontal drag of 200 px in the empty viewport |

Saved as `GO-05AK_AK1.blend` (sha256 `22aa6774…b2a5`). `GO-05AK_working.blend` stays as the clean pre-filter mask file.

### Displacement vs the 05AJ preflight baseline (`checks/ak1_displacement.json`)

| Zone | Median | p95 | Max |
|---|---|---|---|
| all limbs | 0.29 mm | 0.86 mm | 3.12 mm |
| upper arm | 0.25 | 0.67 | 1.89 |
| forearm | 0.23 | 0.66 | 1.70 |
| thigh | 0.37 | 1.07 | 3.12 |
| shin | 0.29 | 0.81 | 2.50 |

This is well inside the AK1 safety envelope (≤ 1.5 / 3.5 / 6.0 mm). Additional readings:
- trunk-to-limb transition band: max 0.92 mm;
- wrist/ankle buffers: max 1.12 mm (light transition, allowed);
- torso, glute and pelvis_other: 0.000 mm.

### Technical gate (`checks/ak1_gates.json`)

| Gate | Result |
|---|---|
| topology identical | yes |
| opened seams | 0 |
| self-intersections | 0 |
| **flipped faces** | **15 — FAIL** |
| degenerate faces | 0 |
| position-welded components / boundary / non-manifold | 1 / 0 / 0 |
| head, tail, tail junction, genital, perineal, hands, feet | 0.000 mm |
| stature / bbox | unchanged (204.5225 cm) |

### The 15 flips (`checks/ak1_flip_faces.json`)

- **Spread:** isolated, across all four limbs: left arm ×2, right arm ×5, left shin ×3, left knee/thigh ×2, right thigh ×1, right shin ×1, right knee ×1.
- **Size:** each face is sub-mm² to 1.4 mm², with vertices moving only 0.34–1.45 mm.
- **Quality:** they are not all slivers. Quality runs 0.03–0.36, and several are ordinary-looking triangles sitting in pre-existing micro-folds.
- **Predicted by the dry run:** 3 of them (344697, 344812, 406795) were already in the 05AJ dry-smoothing prediction list. The order did not authorise repairing those.

### Visual (for the record only)

At this displacement the change against 05AI AC1 is barely visible. The surface is clean: no shelves, ridges or lumps.

See `views/ak_cmp_*.jpg` for identical-camera comparisons against 05AI AC1:
- whole F / P / B / 3/4;
- body-only F / P / B / 3/4;
- arms front and 3/4;
- each arm in profile;
- thighs front and 3/4;
- calves profile and back.

## 3. Finding for the author

The blocker for AC2 is now clearly **source-mesh quality, not the authoring method**. Even a sub-millimetre, shape-preserving, uniform filter inverts about 15 faces scattered over the limbs. The preflight found 2 092 limb faces with quality < 0.15 and 35 micro-crimps. The 05AJ dry run predicted 9–24 flips under light smoothing; the order allowed repair only of crimp-classified faces.

Any route that moves the limb surface by the 3–6 mm needed to soften the heroic forms will flip far more faces than the 6-face authority covers.

Options for a follow-up order:
1. **Limb-zone quality pre-pass.** Run the dry-run Surface Smooth / Smooth simulation in the cloud on the masked limb zones and collect *every* predicted flip face, including the 15 observed here. Repair all of them with the proven 05AI local method (≤ 0.5 mm, near-coplanar rotations, 0.000 mm outside the 2-ring neighbourhoods), with an explicit budget (for example ≤ 60 neighbourhoods), then re-run the dry-run until it predicts 0 flips. Only then repeat AK1 from that frozen baseline.
2. **A UI-applied local retopology of the limb zones** (for example a masked QuadriFlow or Remesh of the limbs only, with the protected interfaces kept). The 05AK order forbids this, and it would change topology identity, so it needs explicit authority.
3. **Tyler hand-sculpting AC2** with a tablet. The masks in `GO-05AK_working.blend` are verified and reusable. It would still meet the same flip sensitivity.

My recommendation is (1). It keeps topology identity and the proven gates, and it turns the flip problem into a bounded, verifiable prep step.

## 4. Files

On the PC, in `RaceBodies/source/Gorrund-Neutral-C/05AK/`:

| File | Status |
|---|---|
| `GO-05AK_working.blend` | verified masks on the 05AJ preflight baseline; geometry unchanged |
| `GO-05AK_AK1.blend` (`22aa6774…b2a5`) | **REJECTED**, evidence only |
| `05AK_README.txt` | marks the folder |

No GO-05AK_AC2 was produced (no passing checkpoint).

Scripts are in `tools/rac/w1/rmot05ak_drivers/`:
- `maskcheck.py`: mask read-back;
- `akcheck.sh`: gates and the displacement envelope.

Blender was closed after the work; no windows from this order remain open.

## State

**Gorrund UNACCEPTED; Grask E3 FROZEN; RM-OT-05 OPEN; Stage C BLOCKED.** No LOW, no blind final acceptance, no scaffold, no D4/UE5/rigging/creator work. AC3 not started.
