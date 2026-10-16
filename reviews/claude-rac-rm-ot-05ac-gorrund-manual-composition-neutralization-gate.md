# RAC RM-OT-05AC — manual composition neutralization: readiness gate (NOT STARTED)

**Order:** `reviews/chatgpt-rac-rm-ot-05ac-gorrund-manual-composition-neutralization-order.md` (7d96b7e).
**Date:** 2026-10-15.

## Outcome

**05AC NOT STARTED — NO INTERACTIVE BLENDER AVAILABLE TO THIS SESSION / TYLER ACTION REQUIRED**

No checkpoint was spent. The 05AB1 clean baseline and all earlier files are untouched:
- `GO-05AB1_macro_corrected_clean.blend` `79727daa…`;
- GLB `03693479…`;
- rig `a20d11fe…`.

Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**.

## Why

§5 requires **real Blender Sculpt / Edit work** on the applied mesh. Scripts may not author the sculpt shape.

| Route | Status |
|---|---|
| Cloud workspace | It has only the headless Blender 5.0.1 Python module. There is no viewport and no interactive brush input. Driving sculpt operators from scripted stroke paths would be scripts authoring the shape, which §5 forbids. |
| Tyler's linked PC (computer use) | The app resolver reports **Blender is not installed** (2026-10-15, about 19:55). This session may not install software. A portable copy might exist, for example under `E:\Tools`, but that folder is not connected to this session. |

## What unblocks it (author / Tyler choice)

1. **Tyler installs or points to Blender on the PC.** Blender 5.0 or later is needed to open the baseline `.blend`. Older versions can import `GO-05AB1_macro_corrected_clean.glb` instead. Claude would then sculpt through computer use (AC1–AC3, up to three checkpoints, every §8 gate run here on the saved GLB).
   - **Honest caveat:** whole-body soft-tissue neutralization on a 1-million-face mesh, done through screenshot-and-drag control, is slow. Achievable stroke precision is limited, so the §10 failure stop is a real possibility.
2. **A human sculptor** works from the frozen 05AB1 baseline. The macro contract and gate tooling are ready, and Claude re-runs the gates on the returned file.
3. **Order-level ruling** allowing Blender sculpt-brush operators with scripted stroke paths. This changes 05AC §5 and is not assumed here.

**STOP.**
