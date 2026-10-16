# RAC RM-OT-05AD — prepare sculpt-safe torso seams, then retry AC1

**Authority:** Tyler-authorized autonomous continuation after 05AC2 rejected AC1.
**Date:** October 16, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05ac2-ui-only-ac1-return-gate.md` (102d7f7 / 1e15759).

## 1. Ruling

The rejected AC1 proves two things:

1. the manual sculpt direction is visually valid (abs/serratus softened; torso moved toward reference composition);
2. the 05AB1 working mesh contains coincident duplicate seam vertices that Blender's sculpt brushes move independently, creating cracks, flips, degenerates and self-intersections.

Therefore the next step is **not** another sculpt attempt on the unwelded mesh.

Authorize one bounded topology-preparation derivative:

**Merge coincident seam duplicates only where required for AC1 sculpting, verify the surface remains geometrically identical and clean, freeze that sculpt-safe baseline, then retry AC1 once.**

This is an explicit exception to the previous "topology identical" rule for the sculpt-working derivative only.

The immutable 05AB1 baseline remains untouched.

## 2. Inputs

Frozen 05AB1 baseline:

`GO-05AB1_macro_corrected_clean.blend`
SHA-256:
`79727daa2552842ddb0ec80505334a4c091ccc026c469e35de7c6c1b7d098a61`

Review GLB:
`GO-05AB1_macro_corrected_clean.glb`
SHA-256:
`03693479be311e72fd608728e6d978ee24169f7fefd679bbc872990061b35e0b`

Rejected AC1 GLB:
`GO-05AC_AC1.glb`
SHA-256:
`886053f023293848daf998dd778adb7130645bc54c4f46c6cc073d085d6fd929`

Rejected AC1 is evidence only; do not advance from it.

## 3. Weld scope

Do **not** globally merge the entire organism by distance.

Build the weld set from the frozen 05AB1 baseline using exact/coincident-position duplicate groups.

Restrict candidate seam groups to the AC1 sculptable torso/shoulder band:

- approximate z = 117–170 cm on the 05AB1 body;
- trunk/chest/abdomen/flanks/axillae;
- shoulder-cap transition needed for AC1.

Exclude and preserve:
- head / face / ears;
- neck above the AC1 transition;
- hands / wrists;
- feet / ankles;
- legs below the AC1 band;
- free tail;
- tail-root/gluteal region;
- genital/pelvic landmarks not in the AC1 torso band.

### Distance threshold

Use **0.01 mm maximum** for Merge by Distance / exact duplicate collapse.

Do not merge distinct surfaces merely because they are close.

Before applying, report:
- candidate duplicate groups;
- vertex count before/after;
- exact positions involved;
- regions touched.

## 4. Weld safety requirements

After the seam weld, the **surface geometry must remain visually and spatially unchanged**.

Required:
- same whole-body dimensions within numeric noise;
- same stature;
- same macro target percentages;
- same triangle surface shape to within <= 0.01 mm Hausdorff / nearest-surface deviation where measurable;
- one connected organism;
- 0 boundary edges;
- 0 non-manifold edges;
- 0 self-intersecting faces;
- 0 inverted/flipped faces;
- 0 degenerate faces;
- protected head/hands/feet/tail unchanged.

UVs/material seams may be lost in the welded AC1 region. That is acceptable for this **reference-anatomy sculpt working derivative**. This is not a production topology asset.

Do not alter the immutable 05AB1 files.

## 5. Frozen sculpt-safe baseline

If the weld passes all gates, save:

`GO-05AD_sculpt_safe_baseline.blend`

and export:

`GO-05AD_sculpt_safe_baseline.glb`

Record exact hashes.

Status phrase:

**05AD SEAM-WELD PREP PASS / SCULPT-SAFE BASELINE FROZEN**

If the weld cannot be made without changing visible geometry or damaging topology, STOP:

**05AD SEAM-WELD PREP FAIL / HUMAN RETOPOLOGY REQUIRED**

Do not retry AC1.

## 6. AC1 retry

If and only if 05AD passes, use the new sculpt-safe baseline for **one** fresh AC1 checkpoint.

Use the same UI-only sculpt direction proven in the rejected AC1:

- flatten pec projection;
- remove central pec split and lower-pec shelf;
- soften serratus;
- remove abdominal block segmentation;
- reduce deltoid cap;
- soften bodybuilder trap/shoulder read;
- reduce love handles;
- preserve broad/deep Gorrund thorax and macro proportions.

Normal Blender UI only:
- Smooth / Surface Smooth;
- restrained Flatten / Scrape;
- restrained Grab only if needed for soft-tissue volume;
- masks / face sets through normal UI.

No console, scripting workspace, shell, scripted strokes, Dyntopo, remesh, procedural deformation, or solver-shaped geometry.

## 7. Retry gate

After the AC1 retry, require:

- 0 opened welded seams;
- 0 self-intersections;
- 0 flips;
- 0 degenerates;
- one component / 0 boundary / 0 non-manifold;
- macro targets preserved;
- head/hands/feet/free-tail unchanged;
- no moved geometry outside the AC1 torso/shoulder region;
- visually clearer reduction in pec/deltoid/abs/serratus than the rejected AC1.

Return:

**05AC AC1 SAFE IMPROVEMENT / READY FOR AC2**

only if all technical gates pass and the visual torso read is clearly improved.

Otherwise:

**05AC AC1 RETRY NOT CREDIBLE / STOP**

## 8. Budget

- 1 topology-prep derivative (05AD).
- 1 AC1 retry from the passed 05AD baseline.

No AC2 or AC3 in this order.

## 9. State

Until AC1 passes:
- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED;
- no LOW / blind final acceptance / scaffold / D4 / UE5 / production rigging / creator implementation.

## 10. Return

Commit:
`reviews/claude-rac-rm-ot-05ad-sculpt-safe-seam-weld-and-ac1-retry-gate.md`

Evidence:
`reviews/rac-rmot05ad-evidence/`

Preserve all prior baselines and rejected AC1 evidence unchanged.
