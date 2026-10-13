# RAC RM-OT-05U: real desktop direct sculpt, BLOCKED before Step 0 (desktop UI not controllable)

**Order:** `reviews/chatgpt-rac-rm-ot-05u-gorrund-real-desktop-direct-sculpt-order.md` (cbdb76c).
**Evidence:** `reviews/rac-rmot05u-evidence/`.

## State

| Item | State |
|---|---|
| Gorrund | **UNACCEPTED / DIRECT SCULPT REQUIRED** (unchanged; no return exists to review) |
| Grask E3 | FROZEN |
| RM-OT-05 | OPEN |
| Stage C | BLOCKED |
| D4 / UE5 / production rigging / creator implementation | NOT STARTED |
| Canon promotion | NOT PERFORMED |

The source master `base.glb` is unchanged (`78ecfa87…a7b`). No mesh was edited or generated. No credits were spent; nothing was installed.

## What happened

Order §6 says: *if the desktop UI cannot actually be controlled in the current session, report that limitation and stop without generating a substitute mesh.* That applies here.

1. **Prepared on Tyler's PC.** Desktop Blender **5.2.2** (portable) is at `E:\Tools\Blender\blender-5.2.2-windows-x64\`. I copied the verified 05T scene files to `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\sheets\gorrund_05U_direct_sculpt\scene\`:

   | File | sha256 |
   |---|---|
   | `GO-05T_sculpt_handoff.blend` | `c7e591fe…60cc` (= 05T release) |
   | `GO-05T_references.blend` | `50992e45…d2a5` (= 05T release) |
   | `fixture_test.blend` | `c7e591fe…60cc`, a disposable byte copy for Step 0 |

2. **Computer-use control.** Access to Blender (full) and the taskbar (click only) was granted.
   - Blender was launched twice. The taskbar then showed three Blender windows: an older `GO_sculpt_5t_work` session and two `Unsaved - Blender 5.2.2` windows.
   - **No Blender window ever appeared in a screenshot.** Clicking the taskbar button and the window thumbnails, Alt+Space, and releasing and re-acquiring the control lock all failed to bring one on screen (`U0_*.jpg`). The windows are most likely positioned off the only reported display; moving them needs a window-snap shortcut, and that permission request did not complete.
   - I stopped there rather than keep retrying (`U0_desktop_control_attempt.json`).
3. **Not done.** No Step 0 UI check, no brush stroke, no Save As, no return check. **Step 0 remains PENDING** and nothing is claimed for it. The pre-existing `GO_sculpt_5t_work` session was not touched.

## A note for when it resumes

The handoff scene was written by bpy 5.0.1, and the desktop app is 5.2.2. Opening it in 5.2.2 is a forward upgrade and is expected to work. Two things must be confirmed in Step 0 itself:
- the saved return reads back in the container's bpy 5.0.1, which `check_return.sh` uses;
- `rac_s3_vid1`, `.sculpt_mask` and the face sets survive the 5.2.2 save.

If the read-back fails, the supported exporter `t_export_blend.py` can instead be run inside the desktop Blender (Scripting tab → run the script with the output path). The reintegration and verify steps are unchanged.

## What unblocks this

Either of:
- **Tyler:** bring one Blender 5.2.2 window onto the main monitor and maximize it, ideally with `fixture_test.blend` open from the folder above, then say "continue 05U". Step 0 then runs as written, followed by the sculpt only if Step 0 passes.
- **Tyler or a sculptor:** do Step 0 and the sculpt by hand per `START_HERE.md`, then return the Step 3 files for verification.

**→ STOPPED: 05U BLOCKED ON DESKTOP UI CONTROL.** No substitute geometry.
