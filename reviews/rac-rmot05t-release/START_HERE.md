# START HERE: Gorrund +X armband interface direct sculpt (RM-OT-05T)

**State:** Gorrund UNACCEPTED / DIRECT SCULPT REQUIRED. The scripted repair S3 is UNRESOLVED. It is the starting point, not a candidate.

**Your task:** sculpt by hand, in Blender, the one committed 05S interface on the +X upper arm. The brief is in [BRIEF.md](BRIEF.md).

**What has been verified:** headless checks of the scene, the masks, the export and the protection tests (below). Nobody has yet opened this scene in the desktop Blender UI. Step 0 is that first check.

## Files

| File | Use |
|---|---|
| [scene/GO-05T_sculpt_handoff.blend](scene/GO-05T_sculpt_handoff.blend) | Working scene (Blender 5.0.1, units cm). It holds the object `GO-05S-S3_working` |
| [scene/GO-05T_references.blend](scene/GO-05T_references.blend) | F1 source and B2, **linked** into the working scene. Keep both files together in the same folder |
| [views/](views/) | Defect and overlay images. **Red** = the crinkled strip to fix; **purple** = editable; **amber** = protected faces on the frozen boundary; **grey** = protected |

**Every check below runs from the release root folder.** In the extracted package (`gorrund_05T_sculpt_handoff/`), that root holds this START_HERE.md, `scene/`, `views/`, `reviews/` and `tools/`. All `reviews/…` and `tools/…` paths below are relative to that root.

In the repository, run from the repository root instead, and prefix `scene/` with `reviews/rac-rmot05t-release/`.

The exporter, checks and tools are at:
- `tools/rac/w1/rmot05t_drivers/check_return.sh`
- `tools/rac/w1/rmot05t_drivers/t_export_blend.py`

## Step 0: first-session desktop check, on a disposable fixture (PENDING until a person does it)

1. Copy `scene/GO-05T_sculpt_handoff.blend` to `fixture_test.blend`, in the same `scene/` folder so the linked references still resolve. **Never** run this test on the production file.
2. Open `fixture_test.blend`. Confirm:
   - **Scene Properties → Units:** Metric, Unit Scale 0.01, Length Centimeters.
   - **Object Properties:** `GO-05S-S3_working` has location and rotation 0 and scale 1.
3. In the Outliner, `REFERENCES_linked_readonly` holds `F1_source_reference` and `B2_reference`. Show them (eye icon) to inspect. They are linked library data and cannot be edited.
4. **Sculpt Mode check.**
   - The mask should already cover everything except the interface. Turn on mask display: **Viewport Overlays → Sculpt Mask**.
   - Stroke with a Draw brush across a grey (masked) area and across a purple area.
   - **Expected:** only the purple area deforms.
5. **Edit Mode check.** Only the 797 interface faces should be visible (the rest is hidden). Do **not** use Alt+H (reveal all).
6. Run `bash tools/rac/w1/rmot05t_drivers/check_return.sh scene/fixture_test.blend checks/fixture`.
   - **Expected:** `reintegration: ACCEPTED_FOR_VERIFICATION` and `V1_outside_anatomy True`.
7. Undo the test stroke (or delete the fixture), move one grey vertex, save, and re-run the check.
   - **Expected:** `REJECTED`.
8. Write the outcome of steps 2–7 into `EDIT_LOG.md`. Until a person completes this, Step 0 is **PENDING**.

## Step 1: sculpt (production working copy)

- Open `scene/GO-05T_sculpt_handoff.blend` and **Save As** `GO-05T_sculpt_RETURN.blend` in the same folder.
- **Sculpt Mode:**
  - keep the provided mask: never Clear Mask or Invert Mask without restoring it;
  - work inside face sets 2 (posterior) and 3 (anterior);
  - **Face Sets → Show only face set 2** isolates the posterior side.
- **Fix:** the red strip (vertex group `FOCUS_posterior_crinkle`, inside `EDIT_posterior`).
- **Never move:** `FROZEN_interface_boundary` or any masked vertex. The export check rejects any change there, even 0.001 cm.
- **Local retopology** (Dyntopo, remesh of a selection, subdivide) is allowed **only** on purple faces. Do not run a whole-object remesh, smooth or decimate.
- **Do not touch:**
  - the object transform;
  - the object name `GO-05S-S3_working`;
  - the attributes `rac_s3_vid1`, `rac_src_vid1` and `rac_label`.
- **Do not add modifiers.** If you do, remove them before export; do not apply them to protected geometry.

## Step 2: export and check (the ONLY supported export path)

```bash
bash tools/rac/w1/rmot05t_drivers/check_return.sh scene/GO-05T_sculpt_RETURN.blend checks/return
```

**What the check does:**
- exports through `t_export_blend.py`;
- verifies the protected region exactly through `t_reintegrate.py`, rejecting any change to protected or frozen vertices or faces;
- runs the pre-registered `s_verify.py` gates;
- renders identical-camera S3-before / return-after views of the posterior, the anterior, the arm (front, lateral, rear, 3/4, underside) and the wireframe.

**Do NOT use File → Export → Wavefront OBJ for the return.** That exporter prints 6 decimals and converts axes, which destroys the exact identity check. Tested: 0 of 139,807 protected faces recovered.

## Step 3: return these files

| File | Notes |
|---|---|
| `GO-05T_sculpt_RETURN.blend` | The edited native scene, keeping `GO-05T_references.blend` beside it |
| `checks/return/return.npz` and `return.obj` | The whole working mesh as exported. Edit and label maps are implicit: `result_maps.npz` and `result_face_labels.npy` are created by the check, and topology changes are handled by the identity attribute |
| `checks/return/result_reintegrate.json`, `result_verify.json`, `RETURN_HASHES.sha256` | Protection result, gate scores and hashes |
| `checks/return/compare_*.png` | Before / after views |
| `EDIT_LOG.md` | Your actual edit log: tools, brushes, what changed, Step 0 outcome |

The S3 and source snapshots are in this release, and their hashes are in `PACKAGE_MANIFEST.sha256`.

**A clean technical result still needs the author's visual acceptance.** It does not accept Gorrund, the species body or any other garment region.
