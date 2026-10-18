# RAC RM-OT-05AV — Gorrund foot-size and heel-stance correction: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05av-gorrund-foot-heel-correction-order.md` (c3227c9)
**Ruling:** `reviews/tyler-rac-rm-ot-05au-gorrund-deferred-item-author-ruling.md` (5cc8df6)
**Source:** `GO-05AT_AC3.blend` (sha `d462f36c…7ea618`, verified before the prep write).
**Executor:** Claude.
- Both shape changes were authored in the Blender 5.2.2 UI on Tyler's PC.
- Cloud scripts were used only for measurement, the transform plan, the four weight vertex groups (0.000 mm geometry change), prediction, read-back, gates, the GLB export and evidence.
- Blender is closed. Tyler's File Explorer window was left as it was.

## Verdict

**05AV FOOT/HEEL CORRECTION PASS / READY FOR FINAL GORRUND CLOSURE REVIEW**

Frozen:

| File | sha256 |
|---|---|
| `GO-05AV_feet_final.blend` | `45a04787c4760e95b9a9bef52837a516788670f1f1bade92c380ffcea74ab9a6` |
| `GO-05AV_feet_final.glb` | `b595f11e2cb4d6f69cdc38954fc9f422dadda9e8e46cee8aed57869face92b4b` |

Location: `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Neutral-C\05AV\`.

The final file is geometry-identical to the AV2 checkpoint (0.000 mm). It contains only the mesh object; the helper empties were deleted. The four `AV_*` weight groups remain in the file as a record.

## 1. Before / after (`checks/before_after_measurements.json`)

| Metric | L before | L after | R before | R after | Target |
|---|---|---|---|---|---|
| Foot length | 39.09 cm | **34.80** | 39.82 cm | **34.80** | 34.5–35.1 ✓ |
| Footprint width | 22.43 cm | **15.30** | 21.75 cm | **15.31** | 15.0–15.6 ✓ |
| Heel minimum (rear 15 %) | 0.88 cm | **0.35** | 1.60 cm | **0.35** | 0.3–0.5 ✓ |
| Ball minimum | 0.00 | 0.00 | 0.19 | 0.03 | — |
| Heel lift vs ball | 0.88 | **0.35** | 1.40 | **0.32** | 0.3–0.5 ✓ |
| Plantar contact span (< 3 mm, fraction of length) | 0.56–0.96 | **0.17–0.96** | 0.72–0.94 | **0.16–0.96** | heel + ball ✓ |

- Length is 17.0 % of stature on both sides, and width 7.5 %.
- The right foot no longer floats: its minimum toe height is now 0.00 cm.

**Symmetry:**

| Check | Result | Limit |
|---|---|---|
| Length difference | 0.002 cm | ≤ 0.3 ✓ |
| Width difference | 0.009 cm | ≤ 0.3 ✓ |
| Heel-lift difference | 0.027 cm | ≤ 0.15 ✓ |

**Plantar profiles:** `views/plantar_profiles_before_after.jpg`. Both heel pads now come down to about 0.2 cm at their lowest point, and the arch is kept.

## 2. Transform plan (pre-authoring; `tools/rac/w1/rmot05av_drivers/`, `checks/plan.json`)

**Per-foot frame:**
- The long axis is the horizontal PCA of the `foot_*` vertex-group set. Its yaw is 6.53° on the left and −31.22° on the right.
- The right foot is turned out about 31° in the source pose. That stance was kept, since the order preserves stance.
- The width axis is perpendicular to the long axis.
- The **ankle joint centre** is the shin/foot weight-blend ring centroid, the same definition as 05AU.

### AV1 — size

A non-uniform horizontal scale in the foot frame:

| Parameter | Value |
|---|---|
| Weight | 1 below z 4 cm, smoothstep to 0 at z 20 cm, that leg only |
| Pivot | the weight-averaged ankle-ring centroid, so the ring centroid cannot move |
| Left scale (width × length) | 0.6820 × 0.8885 |
| Right scale (width × length) | 0.7034 × 0.8696 |

The scale factors were solved to the targets. Nothing above z 20 cm can move, and the ankle's minimum circumference is at 22.5 cm.

### AV2 — heel and ground

A downward translation, applied separately from the scale:
- **Weight:** full at the heel (rear 18 % of length), smoothstep to 0 by 45 %. It fades in z from 1.8 cm to 0 at 6 cm, so it stays below the ankle ring.
- **Left:** 5.50 mm at the heel.
- **Right:** 12.60 mm at the heel. This includes 1.67 mm for the whole right sole, to remove the hover.

### Prediction

The prediction passed every gate below before anything was authored. Predicted renders are in `views/predicted_cmp_*.jpg`.

## 3. Exact UI operations (Blender 5.2.2)

Mechanism: the Hook modifier with a vertex-group weight. With falloff off, Blender moves each vertex by weight × (empty transform − rest), which is the same weighted local transform as the plan. This was verified in Blender before use (model error 7e-8 m).

1. Opened `GO-05AV_prep.blend` (sha `7c8a5410…7cd8`): AC3 plus the vertex groups `AV_scale_L/R` and `AV_heel_L/R`. Geometry change from AC3: 0.000 mm.
2. **AV1, left foot:**
   - Add > Empty > Plain Axes.
   - Typed location (0.25154, −0.43392, 0.08776) m and rotation Z 6.53°.
   - On the mesh, added a Hook modifier with Object = Empty and Vertex Group = `AV_scale_L`.
3. **AV1, right foot:** a second empty at (−0.21976, −0.34367, 0.08645) m with rotation Z −31.22°, and Hook.001 with `AV_scale_R`.
4. Typed the empty scales: left X 0.6820 / Y 0.8885; right X 0.7034 / Y 0.8696.
5. Applied both modifiers and saved **`GO-05AV_AV1.blend`** (sha `57c7584d…1034`).
   - Read-back against the model: max 0.0002 mm.
   - Gated (§4).
6. **AV2:**
   - Two new Hook modifiers on the same empties, with `AV_heel_L` and `AV_heel_R`.
   - Typed the empty location Z: 0.08226 on the left (−5.50 mm) and 0.07385 on the right (−12.60 mm).
   - Applied both, deleted the two empties, and saved **`GO-05AV_AV2.blend`** (sha `f0ecc1a5…43c6`).
   - Read-back against the model: max 0.0002 mm.
7. Saved as **`GO-05AV_feet_final.blend`**, then closed Blender (Ctrl+Q).
   - The GLB was exported in the cloud from that file, using the same exporter as earlier passes.

**AV3 (optional continuity pass):** not needed and not done. There was no Smooth, no brush work and no rerun.

## 4. Technical gates (`checks/AV1_gate.json`, `checks/final_gate.json`, vs AC3)

| Gate | AV1 | Final |
|---|---|---|
| Opened seams / welded vertex count | 0 / unchanged | 0 / unchanged |
| Self-intersections (AC3: 0) | 0 | 0 |
| Flips / degenerates | 0 / 0 | 0 / 0 |
| Components / boundary / non-manifold (welded) | 1 / 0 / 0 | 1 / 0 / 0 |
| Head, tail, tail junction, genital, perineal, hands | 0.000 mm | 0.000 mm |
| Everything outside the two legs below 20 cm (torso, pelvis, arms, thighs, knees, upper shins) | 0.000 mm | 0.000 mm |
| Everything at or above z 20 cm (ankle minimum circumference, calf) | — | 0.000 mm |
| Ankle joint centre drift L / R | 0.0007 / 0.0002 mm | 0.0007 / 0.0002 mm (≤ 0.2 ✓) |
| Stature | 204.5225 cm | 204.5225 cm (+0.00005 mm float) |
| Bounding box above 20 cm | unchanged | unchanged |
| Work-region dihedral increase | max 19.8°, none > 20° | max 19.8°, none > 20° |
| Work-region minimum triangle quality | 0.0125 → 0.0118 | 0.0125 → 0.0118 |

- **Moved:** 73 548 vertices, at most 45.4 mm (toe tips).
- **Toe contact:** there is no new toe contact or fusion. The full-weight region is an affine map, which cannot create self-intersections, and the SI count is 0.
- **Out of scope:** the three known connectivity handles (two hand loops and the left axilla) were not touched, per §9.

## 5. Visual gate

**Views:**
- `views/BA_feet_F34B.jpg` and `views/BA_feet_sides.jpg` (feet: front, 3/4, back, profile, lateral and medial);
- `views/BA_whole_FP.jpg` and `views/BA_whole_B34.jpg` (whole body F/P/B/3-4, before vs after).

| Requirement | Result |
|---|---|
| Feet still read large for a broad-frame beastfolk | ✓ (34.8 cm, about 13 % longer than W1 at equal stature) |
| No slab or monster-foot read | ✓ forefoot tapers, width harmonises with the ankle |
| Length no longer dominates the lower leg | ✓ length / tibia 0.85 → 0.76 |
| Heels plantigrade, not forefoot-only | ✓ contact runs from heel to toes |
| Toes believable, five, non-prehensile, ordinary nails | ✓ toes are narrower in proportion, with no fusion |
| Left/right match | ✓ in size and stance. The right foot keeps the source-pose 31° turn-out; it is preserved, not a mismatch in the feet themselves |
| Body above the ankles unchanged | ✓ (0.000 mm) |

## 6. Disclosures

- **Ankle transition buffer:** the buffer is z 4–20 cm. That is the region where the 30 cm-long foot section narrows to the leg, and the minimum ankle circumference is at 22.5 cm. Because of that, the lower ankle/heel mass between 9 and 20 cm narrows slightly. The ankle above 20 cm and the joint centre are exact.
- **Authoring mechanism:** the transforms were typed into the UI as Hook-modifier transforms driven by the prepared weight groups, then applied in the UI. No vertex positions were written by a script.
- **Right-foot yaw:** the about 31° turn-out of the right foot is unchanged, because the order preserves stance. It can be raised at the closure review if wanted.

## 7. State

STOP. No connectivity repair, retopology, rigging, creator work or Stage C.

| Item | Status |
|---|---|
| Gorrund BODY COMPOSITION | AUTHOR ACCEPTED / FROZEN |
| Head share | AUTHOR APPROVED / FROZEN |
| Tail root | AUTHOR APPROVED / FROZEN |
| Feet + heel stance | CORRECTED; pending final closure review |
| Connectivity cleanup | CARRIED TO RETOPOLOGY / RIG PREP |
| Overall Gorrund mesh | NOT YET FINAL |
| Grask E3 | FROZEN |
| RM-OT-05 | OPEN |
| Stage C | BLOCKED |
| D4, UE5, production rigging, creator implementation | none |
