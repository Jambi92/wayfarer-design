# Claude session handoff — Wayfarer RM-OT-05 (Gorrund)

Purpose: if a conversation runs out of room, a new Claude conversation reads this file first and continues.
Updated: 2026-10-17 (during RM-OT-05AQ).

## Roles and loop
- ChatGPT writes orders: `reviews/chatgpt-rac-rm-ot-05XX-*.md`. Tyler authorized them as if from him.
- Claude executes, gates, commits `reviews/claude-rac-rm-ot-05XX-*-gate.md` + `reviews/rac-rmot05XX-evidence/`,
  inserts a paragraph in `specs/STATUS.md` (before the previous order's), adds a line to
  `reviews/claude-pass2-r5-reference-mesh-queue.md` (after the previous order's), pushes, reports plainly to Tyler.
- Tyler's rules: close every Blender window when done (never leave extra instances); final shape authoring is
  Blender UI only on Tyler's PC (no Blender Python console there); cloud scripts only for prep/diagnostics/masks/repair/evidence.
  Downloads go to the E: drive. Leave the old frozen Blender window and the File Explorer window alone.

## PC paths
- Blender: `E:\Tools\Blender\blender-5.2.2-windows-x64\blender.exe`
- Gorrund work: `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Neutral-C\05AO\` (and sibling 05AQ folder)

## Frozen state
- Latest pass: 05AO AC2 — `GO-05AO_AC2.blend` sha `ba129999cfe71c1ab7afc2f11c1b911bd1e85fc06f301e1bad9a483fcba4f6f3`,
  GLB `1f60fb33fa0c75c9d0f9aa0c1315143005473fd5c72ada67ad922782240de434` (commit f7fc142).
- 05AP (10dc9a5): Smooth-only AC3 not credible; nothing authored.

## In progress: RM-OT-05AQ (AC3 broad feather + restrained deflate)
- Driver tools to be committed under `tools/rac/w1/rmot05aq_drivers/` (postmask.py, aqmetrics.py, hip landmark).
- Broad posterior mask built (diffusion feather k=250); protected sets min 1.0.
- Sim: deflate 8 mm along normals x (1-mask) then Smooth 150 → profile depth −4.2/−6.2 mm, pelvis width 0, thigh radius −2.0/−1.7 %, 3 predicted flips (need repair).
- Open issue: skeletal hip landmark. No armature in the blend. Weight-blend-ring centroid sits at the glute fold (z≈77 cm), not the joint, and moves 0.6–0.8 mm.
  Rig hip pivots exist only in `reviews/rac-rmot05ab-evidence/joints_C.json` (05AB frame, H 189.79).
- Remaining steps: landmark → predictor+repair (≤50 nbhds) → calibrate UI Inflate-negative on scratch copy → AQ1 in UI → gates → visuals → freeze GO-05AQ_AC3 or STOP.

## Calibrations (Blender UI)
- Mesh Filter Smooth: each mouse-move event = 1 Laplacian iteration with mask.
- Surface Smooth one 200 px drag ≈ replica f=0.78.
- Computer-use access expires after 30 min idle; re-grant blender.exe + textinputhost.exe.
