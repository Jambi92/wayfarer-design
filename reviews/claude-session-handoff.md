# Claude session handoff — Wayfarer RM-OT-05 (Gorrund)

Purpose: if a conversation runs out of room, a new Claude conversation reads this file first and continues.
Updated: 2026-10-17 (after RM-OT-05AV).

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
- Gorrund work: `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Neutral-C\05AV\` (latest; earlier passes in sibling 05AO/05AT folders)

## Frozen state
- Latest pass: 05AV feet = GO-05AV_feet_final (see below); before that 05AT AC3 = GO-05AT_AC3. Previous: 05AO AC2 — `GO-05AO_AC2.blend` sha `ba129999cfe71c1ab7afc2f11c1b911bd1e85fc06f301e1bad9a483fcba4f6f3`,
  GLB `1f60fb33fa0c75c9d0f9aa0c1315143005473fd5c72ada67ad922782240de434` (commit f7fc142).
- 05AP (10dc9a5): Smooth-only AC3 not credible; nothing authored.

## Last order: RM-OT-05AV — FOOT/HEEL CORRECTION PASS / READY FOR FINAL GORRUND CLOSURE REVIEW (2026-10-17)
- Active frozen source now: `GO-05AV_feet_final.blend` sha 45a04787c4760e95b9a9bef52837a516788670f1f1bade92c380ffcea74ab9a6; `.glb` b595f11e2cb4d6f69cdc38954fc9f422dadda9e8e46cee8aed57869face92b4b (PC ...\Gorrund-Neutral-C\05AV\). = AC3 + feet only.
- Feet 34.8 cm / 15.3 cm (17.0 / 7.5 % H), heel lift 0.35 cm L / 0.32 cm R. Head share + tail root approved/frozen (05AU ruling 5cc8df6). Connectivity handles (2 hand loops, L axilla) carried to retopology.
- UI technique that worked: Hook modifier + prepared vertex-group weights (falloff off = exact weighted local transform); add Empty, type loc/rot in Object tab, add Hook (vertex group first, then object; no reset needed), type empty scale/location, Apply in modifier menu. Type numbers with single key presses (ctrl+a, digits, 'period', 'minus').
- Next: ChatGPT/Tyler final Gorrund closure review. Tools: tools/rac/w1/rmot05av_drivers/.

## Previous: RM-OT-05AU — DEFERRED-ITEM AUDIT (2026-10-17)
- Tyler ACCEPTED the 05AT body composition (457c202): BODY COMPOSITION AUTHOR ACCEPTED / FROZEN; overall mesh NOT YET FINAL.
- Frozen active source: `GO-05AT_AC3.blend` sha d462f36c08a3b528aff5b4408539f7dfe704b513585da6f2923136c60b7ea618; `.glb` 8ae6ccedffa5098ceb1fad18583edb18d2243060faf942bec933e79899c9fc0d (PC ...\Gorrund-Neutral-C\05AT\).
- 05AU audit (reviews/claude-rac-rm-ot-05au-gorrund-deferred-item-audit.md): KEEP head share (HH 13.96 % vs W1 11.58 %), KEEP tail root;
  LOCAL heel/foot + foot-size correction recommended (feet 19.1-19.5 % length / 10.6-11.0 % width of H vs W1 15.1 / 5.5 %; heel lift L 0.88, R 1.4-1.6 cm;
  suggested target 16.5-17.5 % / 7-8 % H, pivot at ankle/heel, feet below ~25 cm only); genus 3 = two finger loops + left-axilla tunnel -> topology repair at retopology.
- Next: Tyler/ChatGPT review of 05AU recommendations; expect a bounded feet/heel order. Nothing authored in 05AU; Blender closed.
- W1 reference: GO_r6.npz uses `keep` mask (helper geometry below sole); sole z = 0, vertex stature 230.897 cm. Tools: tools/rac/w1/rmot05au_drivers/ (cloud bpy at /home/claude/bpyenv for renders).
- Key technique (05AT): log-map masks through the Smooth event count, M = 1 + ln(1 - 0.95 w)/N. Tools: tools/rac/w1/rmot05at_drivers/.

## Calibrations (Blender UI)
- Mesh Filter Smooth: each mouse-move event = 1 Laplacian iteration with mask.
- Surface Smooth one 200 px drag ≈ replica f=0.78.
- Mesh Filter Inflate: strength 0.020 with a −100 px drag = −7.92 mm x (1-mask), non-cumulative. Type numbers into Blender fields with single key presses (the type action doesn't land). Real Smooth runs ~1.16x the model.
- Duplicate-position seam vertices (tail root) behave as open boundaries under Smooth: keep a 30 mm mask ramp around them.
- Split duplicate-position seam vertices must carry IDENTICAL mask values (pin to 1.0), or Blender opens the seam.
- Blender is a portable install: it can only be resolved for computer use while running. Launch it from the Explorer window on E:\Tools\Blender (click tier) if closed; computer_open_application starts a NEW instance even when one is running, so avoid it.
- In Blender text fields the computer `type` action sometimes types directly and fails (and can leave the field empty); type file names with single key presses (shift+letter, minus, period) and zoom to verify before saving.
- Computer-use access expires after 30 min idle; re-grant blender.exe + textinputhost.exe.
