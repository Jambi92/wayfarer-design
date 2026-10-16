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
