# GO-05U2_sculpt_handoff.blend (RM-OT-05U5)

**Built by:** `tools/rac/w1/rmot05u5_drivers/u5_build_handoff.py`, run headless with bpy 5.0.1.

**Built from:** an unchanged copy of the verified 05U RETURN.

| Input | sha256 |
|---|---|
| `GO-05T_sculpt_RETURN.blend` | `9593d201…57a5` |
| 05U `return.npz` | `0989caf4…0265` |
| Output handoff | `30a3dfb102ea29d92c769cad46acffbd37814e6e14180a5502762d2a08aa374e` |
| Linked reference `GO-05T_references.blend` (unchanged, must sit beside the handoff) | `50992e45…d2a5` |

## Checks (all pass)

- **Vertex and face order** equal S3.
- **Positions** equal the 05U return at float32.
- **Object:** identity transform, no modifiers, name `GO-05S-S3_working`.
- **Attributes:** `rac_s3_vid1`, `rac_src_vid1` and `rac_label` are present and unchanged.
- **Units:** metric, scale 0.01, centimetres.
- **References:** linked from `//GO-05T_references.blend`.

## Support data set in this copy

| Item | Value |
|---|---|
| `.sculpt_mask` | 0.0 on exactly the 365 approved editable vertices (list-equal); 1.0 elsewhere |
| `.sculpt_face_set` | 1 protected (140,362), 2 posterior interface (408), 3 anterior interface (389), **4 the 35 approved added source faces** |
| `rac_u2_added` (face attribute) | 1 on the 35 added faces |
| Vertex groups | `EDIT_upper_ext_05U2` (15) and `FROZEN_interface_boundary_05U2` (106). The 05T group is renamed `FROZEN_interface_boundary_05T_historical` |
| Edit-mode visibility | only the 832 approved faces are visible |
| Text block | `RAC_U2_README` |

## Notes

**Brush-asset library link.** The saved file lists bpy's essentials brush-asset library under its container path. bpy re-adds this on save because of the active brush in tool settings; a stale link carried over from the 05U desktop session was removed first. It has no effect on geometry, and desktop Blender uses its own installed brushes.

**Precheck.** The untouched handoff was run through the corrected 05U4 path, `check_return_u2.sh` (`precheck_untouched_handoff/`):
- **Result:** ACCEPTED_FOR_VERIFICATION_U2. Crease A and B pass at baseline, and the roughness guard fails (the unrepaired notches, as expected), so the numerical stop conditions are **NOT MET** and the command exits 3.
- **Geometry:** `result.obj` is identical to the verified 05U baseline in the U2 layout.
