# RAC RM-OT-05AW — Gorrund feline toenail refinement: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05aw-gorrund-toenail-refinement-order.md` (31a2aa1)
**Author acceptance:** `reviews/tyler-rac-rm-ot-05av-gorrund-foot-author-acceptance-with-claw-exception.md` (d8d119f)
**Source:** `GO-05AV_feet_final.blend` (sha `45a04787…b9a6`, verified before the prep write).
**Executor:** Claude.
- All shape changes were authored in the Blender 5.2.2 UI on Tyler's PC.
- Cloud scripts were used only for nail location, the eight weight groups (0.000 mm geometry change), prediction, read-back, gates, the GLB export and evidence.
- Blender is closed.

## Verdict

**05AW TOENAIL REFINEMENT PASS / READY FOR FINAL GORRUND CLOSURE REVIEW**

The technical gate passes in full.

The visual result reads clearly more tapered, pointed and down-curved than 05AV, so I am returning PASS. One caveat for the closure review: the source nail plates are **sunken, cracked Rodin-era plates**, and a bounded deformation cannot rebuild them. Their recessed rim and their central split survive, and the split is now pinched into a fine central line. The human-nail read is reduced but not fully eliminated. A full feline claw form would need new nail geometry, which belongs to retopology or a dedicated sculpt pass, not this bounded order. **Tyler's visual confirmation is the deciding check.**

Frozen:

| File | sha256 |
|---|---|
| `GO-05AW_nails_final.blend` | `bb815843b432042c31eef5424ec55379f8c4bfdf084b5074fed9ab647608784a` |
| `GO-05AW_nails_final.glb` | `082de3c9b51576a89ac3a3a943e49b76637a7ddd8399f7b3bb15caf2ac55dae1` |

Location: `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Neutral-C\05AW\`.

The final file holds the mesh only (empties deleted). It is geometry-identical to checkpoint `GO-05AW_A.blend` (sha `6d5bf876…84a`).

## 1. Nail location and work region

The nail plates were located from orthographic grid renders of the frozen 05AV feet:
- big toes from the top view;
- the other toes from the front view, where their plates face forward over the toe tip.

Evidence: `views/top_*_grid.jpg`, `views/front_*_grid.jpg`.

**Nails worked:** L1–L4 and R1–R4, the eight visible nails. The fifth toes show no separate visible nail plate from the front or top, so they were left unchanged.

**Per-nail frame:**

| Element | Definition |
|---|---|
| Root (pivot) | proximal edge of the plate |
| Distal axis | proximal → distal edge |
| Lateral axis | foot lateral |
| Outward normal | lateral × distal |

**Weight:** the plate plus a short distal and immediate nail-bed band (`views/mask2_front_*.jpg`). It is built from:
- a lateral falloff (full to 0.30 × nail width, zero at 0.80 ×);
- a distal ramp (0 at the root, full by 70 % of the plate length, ends 45 % past the plate);
- an outward-side term (6 mm depth band);
- connectivity to the nail's own toe only;
- 40 smoothing iterations confined to within 4.5 mm of the support;
- normalising to a peak weight of 1;
- duplicate-position seam copies forced equal.

**Local protection (mask-only):** weights were flattened around the predicted flip sites. The log is in `checks/refine_log.json`. All eight nails then predict 0 SI and 0 flips.

**Region size:**

| Measure | Value |
|---|---|
| Vertices moved | 5 687, all inside the eight nail supports (0 outside) |
| Per nail | 449–979 vertices |
| Largest move | 6.26 mm at a nail tip |
| Mean move per nail | 2.0–2.9 mm |

## 2. Shaping (`checks/ui_values.json`)

One weighted local transform per nail, with the same parameters for all eight so the species language is consistent:

| Effect | Setting |
|---|---|
| Taper | lateral scale **0.32** about the nail centre line; acts with the distal weight, so the tip narrows to a point and the root is unchanged |
| Curvature | **14°** rotation about the lateral axis at the nail root, so the tip curls toward the toe |
| Projection | **+4 mm** along the nail's distal axis |
| Raise | **+3 mm** outward, so the tip stands proud of the toe surface like a sheath |

## 3. Exact UI operations (Blender 5.2.2; same Hook mechanism as 05AV)

1. Opened `GO-05AW_prep.blend` (sha `a314933b…bb24`): 05AV final plus the vertex groups `AW_L1…AW_R4`. Geometry change: 0.000 mm.
2. Added eight Plain Axes empties. For each one I typed:
   - the location at the nail root;
   - rotation Z: 6.53° on the left foot, −31.22° on the right (the 05AV foot frames).
3. For each nail in turn:
   - added a Hook modifier with Vertex Group = `AW_<nail>` and Object = its empty, which caused no deformation;
   - typed the empty's new location (root + 4 mm distal + 3 mm outward), rotation X 14° and scale X 0.32;
   - applied the modifier.
4. Saved `GO-05AW_A.blend`.
   - Read-back against the prediction: max **0.00015 mm**.
   - Empty transforms were verified from the file.
5. Deleted the eight empties and saved **`GO-05AW_nails_final.blend`**.
6. Exported the GLB in the cloud with the same exporter as earlier passes.

There was no brush work, no Smooth, no remesh and no rerun.

## 4. Technical gate (`checks/final_gate.json`, `checks/extra_checks.json`; vs 05AV final)

| Gate | Result |
|---|---|
| Opened seams | 0 |
| Self-intersections | **0** (so no toe contact or fusion, and no nail/toe overlap) |
| Flipped faces | 0 |
| Degenerates | 0 |
| Components / boundary / non-manifold (welded) | 1 / 0 / 0 |
| Movement outside the nail supports | 0 vertices |
| Head, tail, tail junction, genital, perineal, hands | 0.000 mm |
| Everything above z 20 cm; ankle-ring centroid | 0.000 mm |
| Heel regions L / R | 0.000 mm |
| Ground | lowest moved vertex 2.0 mm above the floor (was 2.2 mm); no ground intersection |
| Stature | 204.5225 cm, unchanged |
| Minimum triangle quality in the foot region | unchanged |

Of the rapid curvature changes, 486 edges rise by more than 20°. All sit inside the nail plates, where the taper deliberately sharpens the form.

**Foot measurements (`checks/foot_measurements.json`):**

| Measure | L before → after | R before → after | Limit |
|---|---|---|---|
| Foot length | 34.80 → **34.98 cm** (+1.8 mm) | 34.80 → 34.80 cm | ≤ +2 mm ✓ |
| Footprint width | 15.30 → 15.30 cm | 15.31 → 15.31 cm | unchanged ✓ |
| Ball contact | unchanged | unchanged | — |
| Heel | 0.000 mm movement | 0.000 mm movement | — |

- **Left heel-lift number:** it reads 0.341 cm instead of 0.350 only because the +1.8 mm length shifts the rear-15 % measuring window. No heel vertex moved.
- **Right "contact" count:** it rises from 1 290 to 1 296 vertices below 3 mm. These are six nail-tip front vertices now 2–3 mm above the floor; nothing touches the ground.

## 5. Visual gate

**Views:**
- `views/BA_nails_front_ortho.jpg` (front orthographic, both feet);
- `views/BA_nails_L.jpg`, `views/BA_nails_R.jpg` (front, profile and 3/4 nail close-ups);
- `views/BA_feet.jpg` (foot front, 3/4, back);
- `views/BA_whole.jpg` (whole body F/P/3-4/B).

| Requirement | Result |
|---|---|
| Taper clearly improved | ✓ every nail narrows to a point; nail tips narrow to about a third of their former width |
| Modest projection and curvature | ✓ tips project 4–6 mm and curl toward the toe; restrained, no hooks or talons |
| Feline/naturalistic read; human-nail read reduced | **partly**: reduced, but the inherited recessed rim and central split remain (see Verdict) |
| Toe hierarchy and left/right match | ✓ same parameters on all eight nails; big-toe nails stay the largest |
| 05AV foot proportions intact; feet large, plantigrade | ✓ length +1.8 mm (left only), width and heel unchanged |
| No exaggeration | ✓ |

## 6. State

STOP.

- No connectivity repair, retopology, rigging, creator work or Stage C.
- `RM-OT-05AX` (final closure review) is unblocked by this PASS and is the next queued order.

| Item | Status |
|---|---|
| Gorrund BODY COMPOSITION | AUTHOR ACCEPTED / FROZEN |
| Head share; tail root; foot size and heel stance | AUTHOR APPROVED / FROZEN |
| Toenail morphology | REFINED; pending Tyler visual confirmation in 05AX |
| Connectivity cleanup | CARRIED TO RETOPOLOGY / RIG PREP |
| Overall Gorrund mesh | NOT YET FINAL |
| Grask E3 | FROZEN |
| RM-OT-05 | OPEN |
| Stage C | BLOCKED |
| D4, UE5, production rigging, creator implementation | none |

Scripts are in `tools/rac/w1/rmot05aw_drivers/`.
