# RAC RM-OT-05AC1 — recover existing desktop Blender path/session before changing sculpt method

**Authority:** Tyler-authorized autonomous continuation after 05AC readiness stop.
**Date:** October 15, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05ac-gorrund-manual-composition-neutralization-gate.md` (48f28bb).

## 1. Purpose

Do not change the 05AC sculpt method yet.

The current readiness report says the linked PC reports Blender not installed, but this conflicts with the project's own prior evidence:

- `reviews/claude-rac-rm-ot-05u-gorrund-direct-sculpt-return-gate.md` records **Blender 5.2.2 on Tyler's computer**, with Tyler bringing its window to the main display and the order being executed there.
- `reviews/claude-rac-rm-ot-05u5-bounded-desktop-sculpt-return-gate.md` records real desktop fixtures in Blender 5.2.2.
- `reviews/claude-rac-rm-ot-05u6a-resumed-checkpoints-return-gate.md` records real desktop Blender 5.2.2 checkpoints.

Therefore first reconcile whether the current session has merely lost discovery/control of the existing Blender installation.

## 2. Safety / access rule

Do **not**:
- install Blender;
- download software;
- alter OS permissions;
- bypass app-resolution or computer-use restrictions;
- use scripted sculpt strokes as a substitute.

This is discovery/readiness only.

## 3. Recovery sequence

Use only normal, permitted desktop/app/file discovery that is already available to this session.

Try, in order:

1. Re-read the 05U/05U5/05U6A evidence for any recoverable application/session details.
2. Ask the PC app resolver / normal application discovery for Blender again, including the explicit name **Blender 5.2.2**.
3. Check normal accessible Start-menu/application shortcuts if computer use exposes them.
4. Check only filesystem locations already exposed/connected to this session for an existing `blender.exe` or Blender folder.
5. If a Blender executable or shortcut is found, launch it normally through the allowed desktop path.
6. Confirm:
   - a visible Blender window exists;
   - it is on the controllable/main display;
   - mouse/keyboard computer-use input can interact with the viewport;
   - version is sufficient to open `GO-05AB1_macro_corrected_clean.blend`, or else import the GLB;
   - no geometry is modified during this readiness check.

Do not search or mount unconnected private folders by workaround.

## 4. If Blender is recovered

Return:

**05AC1 DESKTOP BLENDER RECOVERED / 05AC READY TO RESUME**

Record:
- version;
- how it was found/launched;
- whether the viewport is controllable;
- whether the 05AB1 clean baseline opens successfully;
- one screenshot showing the baseline in the viewport;
- hashes proving the baseline remained unchanged.

Then STOP. Do not begin AC1 sculpt strokes in this recovery block.

## 5. If Blender cannot be recovered

Return:

**05AC1 DESKTOP BLENDER NOT RECOVERABLE IN CURRENT SESSION / TYLER MUST OPEN OR POINT TO BLENDER**

In that case give Tyler the shortest manual action:
- open the existing Blender installation on the main display, or
- provide the exact installed executable path/shortcut if known.

Do not recommend reinstalling unless Tyler confirms Blender truly is absent.

## 6. State

No 05AC checkpoint is spent in this block.
All 05AB1 files remain immutable.
Gorrund remains UNACCEPTED; Grask E3 FROZEN; RM-OT-05 OPEN; Stage C BLOCKED.

## 7. Return

Commit:
`reviews/claude-rac-rm-ot-05ac1-desktop-blender-recovery-gate.md`

No geometry package is required unless a screenshot/readiness artifact is produced.
