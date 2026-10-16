# RAC RM-OT-05AC2 — UI-only AC1: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05ac2-ui-only-ac1-order.md` (6de9218).
**Date:** 2026-10-16.

## Outcome

**05AC2 UI-ONLY DESKTOP CONTROL REFUSED / TYLER MANUAL ACTION REQUIRED**

## Sequence

All steps used normal UI input only. No console, scripting workspace, shell or scripted input was used.

1. The app resolver found the running `blender.exe` (portable 5.2.2) and File Explorer.
2. Tyler approved the computer-use grant: Blender at full tier, File Explorer at click tier.
3. Blender was brought forward and showed a fresh splash screen.
4. A Windows text-input overlay (`textinputhost.exe`) was in front and blocked the click. It was granted through the normal access prompt.
5. The next action, **a single left-click on "Open…" in Blender's splash screen**, was **refused by this session's safety check** ("Auto-Mode Bypass").

Per order §2, I stopped immediately. No workaround was attempted, and the computer-use lock was released.

## State

- No file opened.
- No working copy saved.
- No mask painted.
- No sculpt stroke.
- **No AC1 checkpoint spent.**
- 05AB1 baseline (`79727daa…`) and the joined 05AC copy are untouched.

Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**.

## Tyler manual action required

The safety check on this session now refuses ordinary Blender UI clicks, whatever the method. Desktop sculpting by Claude is therefore not available in this session.

Realistic routes:
1. **Tyler or a human sculptor performs AC1 in Blender.** Open `…\Gorrund-Neutral-C\05AC\GO-05AB1_macro_corrected_clean.blend`, Save As `GO-05AC_working_AC1.blend`, sculpt the torso per §5, then save `GO-05AC_AC1.blend` and export `GO-05AC_AC1.glb`. Claude then runs every 05AC §8 gate on the returned file: topology, single-body, intersections, flips, macro targets, protected regions, renders.
2. **A fresh session**, in which the safety check may re-evaluate. There is no guarantee.

---

# Retry in a fresh session (2026-10-16, ~09:20–09:55 PT): AC1 performed UI-only, result below

## Outcome

**05AC AC1 UI SCULPT NOT CREDIBLE / STOP**

The torso read improved, but the sculpt broke the surface: it opened seams. Per §8 the checkpoint is rejected and **not promoted**. The 05AB1 baseline stays the reference, untouched (`05AC\GO-05AB1_macro_corrected_clean.blend`, modified time unchanged since 05:21; GLB used for comparison: `05AB1\GO-05AB1_macro_corrected_clean.glb`, sha256 `03693479…`).

## What was done (normal Blender UI only)

No console, scripting workspace, shell or scripted strokes were used. The Windows text-input overlay was granted through the normal access prompt, and ordinary clicks were then accepted.

1. Used File > Open on the joined baseline. The splash screen's "Open…" was used first; the bridge then dropped and reconnected, and the file was opened.
2. Saved As `GO-05AC_working_AC1.blend`. The baseline was not overwritten: the dialog was checked to show "Save As", not "Overwrite".
3. Sculpting workspace. Front orthographic view.
4. **Protection** with four Box Mask passes:
   - head and neck above the neck base;
   - each arm below the shoulder cap;
   - everything below the hips (pelvis, legs, feet, tail).
   Torso and shoulder caps were left sculptable. The .npy masks were not applied, as required by §4.
5. **Strokes (hand-driven mouse):**
   - Smooth (strength 0.5) over:
     - abdominal blocks;
     - pec split and lower-pec shelf;
     - serratus;
     - love handles;
     - pec–deltoid groove.
   - Flatten (strength 0.25) over:
     - both pecs (front view);
     - the chest profile and deltoid cap (right view).
   - In the three-quarter view, further Smooth passes on the serratus, flank crease, lateral abdominals and lower-pec edge.
   - No Dyntopo, remesh or Grab.
6. Saved `GO-05AC_AC1.blend`. Exported `GO-05AC_AC1.glb` via File > Export > glTF 2.0. Blender vertex count unchanged (554,591).

## §8 gates (`checks/ac1_checks.json`, `checks/ac1_seam_opening.json`)

| Gate | Result |
|---|---|
| Single body (1 node, 1 mesh, 1 primitive) | PASS |
| Face count / Blender vertex count | unchanged (1,000,000 tris; 554,591 verts) |
| Stature / bounding box | unchanged (204.52 cm; extents identical to 0.001 cm) |
| Moved region | only z 117.0–169.9 cm, the trunk band; max displacement 14.6 mm, p99 3.9 mm |
| Protected regions (head, hands, feet, tail, legs) | not moved: no vertex outside the trunk band moved |
| **Seam integrity** | **FAIL: 1,480 positions that coincided in the baseline were pulled apart (798 by more than 1 mm, max 8.7 mm).** These are duplicate (unwelded) vertices on existing seams; Smooth moves each copy separately. Cracks follow the lower-pec line, the navel/linea alba, the axillae and the flank/hip lines (red in `views/ac1_baseline_vs_ac1_torso.jpg`). |
| Flipped faces | **FAIL: 316 new, 294 of them on the opened seams** |
| Degenerate faces | **FAIL: 310 new (baseline 0), 216 on the opened seams** |
| Self-intersections | **FAIL: 0 in the baseline → 3,024 after, all new** (`checks/ac1_self_intersections.json`; pymeshlab, faces welded by position, so opened seam edges count too) |

`topology_identical: false`, `components: 1778` and `nonmanifold_edges: 169` in `ac1_checks.json` come from welding by position *after* the seams opened. They are symptoms of the same seam opening, not a separate topology change.

## Visual read

In `views/ac1_baseline_vs_ac1_torso.jpg`:
- the abdominal block segmentation is largely gone;
- the serratus grooves and pec split are softer.

The pec mass and deltoid cap are only slightly reduced. A visible crease now runs along the opened lower-pec seam. On visuals alone this is a partial improvement; the seam damage decides the verdict.

## Root cause and options (author / Tyler ruling)

The 05AB1 clean baseline carries unwelded duplicate vertices along internal seams across the torso. No smoothing or flattening brush can work across those seams without opening them, whoever sculpts — Claude or a human. Options:

1. Authorize a **Merge by Distance (seams only, ~0.01 mm)** on a working copy before AC1. This is a topology change, which 05AC currently forbids, so it needs an explicit ruling. Then re-run AC1 the same way.
2. Sculpt only with brushes that respect seams. Blender has no reliable option for this on unwelded duplicates, so it is not recommended.
3. Human sculptor, under the same seam constraint as 1.

## Files on Tyler's PC (`…\Gorrund-Neutral-C\05AC\`)

- `GO-05AC_working_AC1.blend`, `GO-05AC_AC1.blend`, `GO-05AC_AC1.glb` (sha256 `886053f0…`): **rejected, kept as evidence only**.
- Baseline `.blend` / GLB: untouched.

## State

- One AC1 checkpoint spent (rejected).
- No AC2 / AC3.
- Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**.
