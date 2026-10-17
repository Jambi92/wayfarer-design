# Claude session handoff — Wayfarer RM-OT-05 (Gorrund)

Purpose: if a conversation runs out of room, a new Claude conversation reads this file first and continues.
Updated: 2026-10-17 (after RM-OT-05AR).

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

## Last order: RM-OT-05AR — CONTINUITY CORRECTION NOT CREDIBLE / STOP (gate committed 2026-10-17)
- AR1r is numerically clean (tail core 0, ring 2.07 mm) and the tail plateau is fixed, but ~150 Smooth events fold the lateral hip/front thigh transition band (up to 59° dihedral). Active state = GO-05AO_AC2.
- Proven pieces to reuse: `tools/rac/w1/rmot05ar_drivers/` (armask.py field + Lipschitz feather, tailramp.py distance ramp from root core, pinned duplicate seams). Model says ~25 Smooth events clears SI with far smaller kinks.
- Next: wait for ChatGPT's ruling. Cloud work dirs /home/claude/aq and /home/claude/ar are lost if the container is reclaimed; rebuild from repo tools.

## Calibrations (Blender UI)
- Mesh Filter Smooth: each mouse-move event = 1 Laplacian iteration with mask.
- Surface Smooth one 200 px drag ≈ replica f=0.78.
- Mesh Filter Inflate: strength 0.020 with a −100 px drag = −7.92 mm x (1-mask), non-cumulative. Type numbers into Blender fields with single key presses (the type action doesn't land). Real Smooth runs ~1.16x the model.
- Duplicate-position seam vertices (tail root) behave as open boundaries under Smooth: keep a 30 mm mask ramp around them.
- Split duplicate-position seam vertices must carry IDENTICAL mask values (pin to 1.0), or Blender opens the seam.
- Blender is a portable install: it can only be resolved for computer use while running. Launch it from the Explorer window on E:\Tools\Blender (click tier) if closed; computer_open_application starts a NEW instance even when one is running, so avoid it.
- Computer-use access expires after 30 min idle; re-grant blender.exe + textinputhost.exe.
