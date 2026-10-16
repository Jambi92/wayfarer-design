# RAC RM-OT-05AC2 — fresh UI-only desktop sculpt attempt; no console, no scripted strokes

**Authority:** Tyler-authorized autonomous continuation after 05AC1.
**Date:** October 16, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05ac1-desktop-blender-recovery-gate.md` (63667ef).

## 1. Ruling

Blender is present and usable on Tyler's PC:

`E:\Tools\Blender\blender-5.2.2-windows-x64\blender.exe`

The 05AB1 clean baseline has already been joined into:

`E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Neutral-C\05AC\GO-05AB1_macro_corrected_clean.blend`

and verified SHA-256:

`79727daa2552842ddb0ec80505334a4c091ccc026c469e35de7c6c1b7d098a61`

The previous session's safety refusal followed use of Blender's Python console. Do not use the console again.

This order authorizes one **fresh, UI-only** attempt to resume 05AC.

## 2. Hard safety boundary

Allowed:
- File Explorer / normal app launch;
- Blender menus, workspaces, viewport, keyboard shortcuts and mouse;
- Sculpt Mode / Edit Mode;
- hand-painted masks / face sets through normal Blender UI;
- ordinary save-as / export through Blender UI.

Forbidden:
- Blender Python console;
- scripting workspace;
- command prompt / PowerShell / shell;
- scripted brush strokes;
- automation that moves vertices or simulates sculpt strokes;
- any workaround around a computer-use or safety refusal.

If normal UI input is refused again, STOP immediately with:
**05AC2 UI-ONLY DESKTOP CONTROL REFUSED / TYLER MANUAL ACTION REQUIRED**

Do not attempt a workaround.

## 3. Open the baseline

Launch Blender 5.2.2 normally from File Explorer.

Use Blender's ordinary **File > Open** UI to open the already-joined 05AC baseline above.

Verify visually that object `GO-05AB1_macro_corrected_clean` is present and unchanged.

Do not save over the frozen baseline.

Immediately Save As a new working copy:

`GO-05AC_working_AC1.blend`

## 4. Masks

The prepared .npy masks are evidence/helpers only in this UI-only route. Do not apply them via Python.

Instead, create only the protection needed for AC1 using Blender's normal UI:
- head / face / ears: protected;
- hands: protected;
- feet: protected;
- free tail: protected;
- neck length / terminal anatomy: protected;
- leave torso, chest, abdomen, waist and shoulder-cap soft tissue sculptable.

Use normal Sculpt Mask / Face Set UI or direct careful brush avoidance.

Do not spend excessive time recreating exact scripted masks; this is a sculpt-protection aid, not a measurement target.

## 5. AC1 scope only

This order resumes **only AC1** from the parent 05AC order.

Target:
- flatten pectoral projection;
- remove hard central pec split / lower-pec shelf;
- reduce deltoid cap;
- soften bodybuilder trapezius/shoulder read without changing neck length;
- remove abdominal block segmentation;
- soften serratus grooves;
- reduce love-handle bulges;
- preserve the broad/deep Gorrund thorax and integrated trunk.

Do not intentionally reshape:
- arms below the shoulder-cap transition;
- legs;
- glutes/posterior;
- head;
- hands;
- feet;
- tail;
- pelvis/joint positions.

## 6. Method

Real interactive Blender sculpt only.

Permitted brushes:
- Smooth / Surface Smooth;
- restrained Flatten / Scrape;
- restrained Grab / Elastic only for soft-tissue volume;
- ordinary mask/face-set operations.

No Dyntopo, remesh, topology change, procedural deformation, or scripted shape authoring.

Maximum **one AC1 checkpoint** in this order.

## 7. Save and handoff

If normal UI sculpt succeeds:

Save the working checkpoint as:
`GO-05AC_AC1.blend`

Export a GLB through normal Blender UI:
`GO-05AC_AC1.glb`

Then return control to the cloud/repo validation side for the existing 05AC §8 gates.

Do not perform AC2 or AC3 in this order.

## 8. Validation

Run the parent 05AC AC1 checks after the file is returned:
- topology identity;
- single-body;
- boundary/non-manifold;
- self-intersections;
- flips;
- macro target preservation;
- protected-region comparison;
- identical-camera whole/body-only/chest/shoulder/abdomen views.

### If AC1 is technically safe and visibly improves the heroic torso read

Return:
**05AC AC1 SAFE IMPROVEMENT / READY FOR AC2**

### If AC1 causes damage or fails to improve the target

Revert to the frozen 05AB1 baseline and return:
**05AC AC1 UI SCULPT NOT CREDIBLE / STOP**

## 9. State

No change to canon or acceptance:
- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED.

## 10. Return

Commit:
`reviews/claude-rac-rm-ot-05ac2-ui-only-ac1-return-gate.md`

Evidence:
`reviews/rac-rmot05ac2-evidence/`
