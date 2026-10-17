# Claude session handoff — Wayfarer RM-OT-05 (Gorrund)

Purpose: if a conversation runs out of room, a new Claude conversation reads this file first and continues.
Updated: 2026-10-17 (after RM-OT-05AT).

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
- Latest pass: 05AT AC3 = GO-05AT_AC3 (see above). Previous: 05AO AC2 — `GO-05AO_AC2.blend` sha `ba129999cfe71c1ab7afc2f11c1b911bd1e85fc06f301e1bad9a483fcba4f6f3`,
  GLB `1f60fb33fa0c75c9d0f9aa0c1315143005473fd5c72ada67ad922782240de434` (commit f7fc142).
- 05AP (10dc9a5): Smooth-only AC3 not credible; nothing authored.

## Last order: RM-OT-05AT — AC3 PASS / READY FOR FINAL Q1-Q2 + TYLER VISUAL REVIEW (2026-10-17)
- FROZEN: `GO-05AT_AC3.blend` sha d462f36c08a3b528aff5b4408539f7dfe704b513585da6f2923136c60b7ea618; `.glb` 8ae6ccedffa5098ceb1fad18583edb18d2243060faf942bec933e79899c9fc0d (PC folder ...\Gorrund-Neutral-C\05AT\). This is now the active composition (AC1 torso + AC2 limbs + AC3 posterior).
- Next: Tyler's visual review / ChatGPT's Q1-Q2 order. Pre-review sheet: reviews/rac-rmot05at-evidence/views/Q1Q2_prereview_GO-05AT_AC3.jpg.
- Key technique: log-map masks through the Smooth event count, M = 1 + ln(1 - 0.95 w)/N; a linear ramp near 1.0 acts as a hard edge under long smoothing. Tools: tools/rac/w1/rmot05at_drivers/.

## Calibrations (Blender UI)
- Mesh Filter Smooth: each mouse-move event = 1 Laplacian iteration with mask.
- Surface Smooth one 200 px drag ≈ replica f=0.78.
- Mesh Filter Inflate: strength 0.020 with a −100 px drag = −7.92 mm x (1-mask), non-cumulative. Type numbers into Blender fields with single key presses (the type action doesn't land). Real Smooth runs ~1.16x the model.
- Duplicate-position seam vertices (tail root) behave as open boundaries under Smooth: keep a 30 mm mask ramp around them.
- Split duplicate-position seam vertices must carry IDENTICAL mask values (pin to 1.0), or Blender opens the seam.
- Blender is a portable install: it can only be resolved for computer use while running. Launch it from the Explorer window on E:\Tools\Blender (click tier) if closed; computer_open_application starts a NEW instance even when one is running, so avoid it.
- In Blender text fields the computer `type` action sometimes types directly and fails (and can leave the field empty); type file names with single key presses (shift+letter, minus, period) and zoom to verify before saving.
- Computer-use access expires after 30 min idle; re-grant blender.exe + textinputhost.exe.
