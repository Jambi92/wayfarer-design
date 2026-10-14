# RAC RM-OT-05U: real desktop direct sculpt, return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05u-gorrund-real-desktop-direct-sculpt-order.md` (cbdb76c).
**Evidence:** `reviews/rac-rmot05u-evidence/`, which holds `EDIT_LOG.md`, `step0/`, `scene/` and `checks/return/`.

**History of this report:**
- First attempt (d400b11): blocked because the desktop windows could not be controlled. The Blender windows were on other monitors.
- Tyler then brought a Blender 5.2.2 window up on the main display, and the order was carried out as written.

## State

| Item | State |
|---|---|
| Gorrund | **AUTHOR VISUAL REVIEW REQUIRED** |
| Grask E3 | FROZEN |
| RM-OT-05 | OPEN |
| Stage C | BLOCKED |
| D4 / UE5 / production rigging / creator implementation | NOT STARTED |
| Canon promotion | NOT PERFORMED |

The source master `base.glb` is unchanged (`78ecfa87…a7b`). All newly reconstructed skin remains **INFERRED**. Nothing was installed, nobody was contacted and no credits were spent. No RD5, LOW, scaffold, Rodin, D4 or UE5 work was done.

## 1. Step 0 (desktop Blender 5.2.2): PASS

All checks were performed in the UI on disposable fixtures. Details are in `EDIT_LOG.md`; the check outputs are in `step0/`.

| Check | Result |
|---|---|
| Units | Metric, 0.01, centimetres |
| Transform | Location 0, rotation 0, scale 1 |
| Linked F1 / B2 | Display when shown; Tab does not edit linked data |
| Sculpt mask | Shown with the mask overlay |
| Brush stroke from masked grey into editable blue | Only editable vertices moved; 70,401 / 70,401 protected vertices bit-identical |
| Edit-mode isolation | 797 / 141,194 faces and 451 vertices visible |
| `check_return.sh` on the stroked fixture | ACCEPTED, V1 True |
| A protected foot vertex moved 0.05 cm | **REJECTED** (P1: 1, S3 vertex 67315; P2: 4 faces) |

**Three findings on the way:**
1. **A single-jump synthetic drag does not sculpt** (0 vertices moved). Strokes have to be built from mouse-down, a series of moves, then mouse-up.
2. **The text-typing tool did not deliver a numeric transform value.** The first protected-move attempt recorded a zero-length Move. The value was then sent as individual key presses and verified in the header.
3. **Files saved by 5.2.2 read correctly in the container's bpy 5.0.1.** The identity attribute survived; all vertices were verified.

## 2. Production direct sculpt

**File:** `GO-05T_sculpt_RETURN.blend`, created by Save As of `GO-05T_sculpt_handoff.blend` before any edit. The linked reference file is beside it.

**Brushes and tools:**
- **Smooth brush only**, in five interactive passes (100–200 px, strength 0.4–0.7), along and across the posterior crinkled strip. Each pass is listed in `EDIT_LOG.md`.
- No Draw, Clay, Grab, Dyntopo, remesh, topology edit, modifier or script geometry operation.
- **The anterior was not touched.**

**Extent:**
- 101 of 350 editable vertices moved, all posterior, at θ −108…−81° and s −0.4…7.5 cm.
- Displacement: median 0.28 cm, maximum 1.72 cm, the maximum being the removal of the largest saw-tooth spike.
- No new vertices; topology unchanged.

**Hard rules, checked in the returned file:**
- object name `GO-05S-S3_working`;
- identity matrix, no parent and no modifiers;
- `rac_s3_vid1`, `rac_src_vid1` and `rac_label` present, with labels unchanged (`139807 / 417 / 173 / 421 / 376`);
- `.sculpt_mask` and `.sculpt_face_set` present;
- units unchanged;
- F1 / B2 still linked from the library.

## 3. Return verification (`check_return.sh scene/GO-05T_sculpt_RETURN.blend checks/return`)

| Item | Result |
|---|---|
| Export (`t_export_blend.py`) | 70,751 vertices / 141,194 faces, identity transform, 0 n-gons, 0 new vertices |
| **Reintegration** | **ACCEPTED_FOR_VERIFICATION** |
| P1 protected vertices | **70,401 / 70,401 unchanged** (frozen boundary 101 / 101) |
| P2 protected faces | **140,397 / 140,397 present** |
| Interface faces | 560 kept verbatim, 237 edited |
| `s_verify` verdict | **UNRESOLVED** (same automated verdict as S3) |

**Gate by gate, S3 (before) against the RETURN:**

| Gate | S3 | RETURN | Notes |
|---|---|---|---|
| V1 outside anatomy | pass | **pass** | |
| V2 boundary / manifold | pass | **pass** | |
| V3 intersections | pass | **pass** | |
| V4 triangle quality | fail | fail | **Unchanged.** Minimum angle 11.9° and the 8 out-of-range edges are all in the untouched posterior taper (θ −122…−132°). Sculpting does not change edge lengths there |
| V5 seam continuity | pass, 97.8 % ≤ 35° | **pass, 96.4 %** | Two new stitch outliers at the top end of the strip (θ −88.4° s 8.0: 63.7°; θ −85.7° s 7.9: 59.1°), where the smoothed interior meets the unsmoothable protected ring |
| V6c-1 ledge removed, worst direction change per 0.5 cm | −96°: 36.9; −90°: 95.1 | **−96°: 15.2; −90°: 74.4** | Better, but −90° still exceeds 35°. That is the axillary fold crease line itself; the other columns are unchanged |
| V6c-2 taper termination | fail | fail | **Unchanged.** Anterior non-monotone at θ 118–122°; anterior deliberately untouched |
| V6c-3 folds | pass; 2 dihedrals > 90° (θ −89.7°, −89.5°) | **pass; 0 > 90°** | The fold-edge kinks are gone |

A technical pass is not visual acceptance, and V6c-1 and V5 are reported as they came out.

## 4. Visual evidence (identical cameras; `checks/return/compare_*.png`)

| Required view | File |
|---|---|
| Posterior shaded close (yaw 0 / 20 / 330, pitch −45) | `compare_posterior_shaded.png` |
| Posterior wireframe with labels | `compare_posterior_wire.png` |
| Anterior shaded / wireframe (unchanged) | `compare_anterior_shaded.png`, `compare_anterior_wire.png` |
| Rear, lateral, front, rear 3/4, front 3/4, underside | `compare_arm_views.png` (yaw 180 / 90 / 0 / 135 / 45, pitch −55) |

**What I see** (for the author to confirm or reject):
- The crinkled, notched strip along the posterior axillary-fold edge is gone through the middle and lower strip. It now reads as a continuous arm-to-fold crease.
- The deltoid and triceps relief and the tapered termination of the remaining garment are unchanged; that area is outside the strokes or masked.
- **A few small notches remain at the very top end of the strip** (best seen at yaw 20). They are on **protected** vertices just outside the editable set:
  - S3 vertices 61303, 61559 and 62065 (frozen ring);
  - S3 vertices 61581, 61580 and 61562 (source), at θ −84…−90° and s 8–10 cm.

  The order forbids touching them. Removing them would need an authorised extension of the editable boundary.
- At the front 3/4 view (yaw 45), the smoothed fold edge now shows as a soft rounded edge where S3 had a sharp crinkled line. **The author should judge** whether that reads as natural or as slightly over-softened.

## 5. Package and delivery

`gorrund_05U_direct_sculpt_return.zip` has its own manifest and passed a clean-extraction and hash check. Its hashes and delivery locations are in the receipt below.

**→ STOP FOR TYLER / AUTHOR VISUAL REVIEW.** Gorrund is not promoted. Stage C is not begun, and the sculpt is not extended to any other region.

---

## Package receipt

**Release:** `gorrund_05U_direct_sculpt_return.zip`, a single ZIP.

| Property | Value |
|---|---|
| Size | 29,260,601 bytes |
| SHA-256 | `aed5711fa00d193eccae9391f40de790d6e617333caa8add76554e81358a3159` |
| Own manifest | `PACKAGE_MANIFEST.sha256`, 26 entries |

**Contents:**
- `scene/GO-05T_sculpt_RETURN.blend` (sha `9593d201…57a5`) with `GO-05T_references.blend`;
- `checks/return/`:
  - `return.npz` and `return.obj.gz`;
  - `result_reintegrate.json` and `result_verify.json`;
  - `RETURN_HASHES.sha256`;
  - `compare_*.png`;
  - `result.obj.gz` and the result maps / labels;
- `step0/`;
- `EDIT_LOG.md`;
- `REPORT.md`, a copy of this report.

**Clean extraction**, in an empty directory:
- `unzip -t` reported no errors.
- 26 of 26 manifest entries are present with equal hashes; nothing is unlisted.
- `check_return.sh` was re-run on the extracted `GO-05T_sculpt_RETURN.blend`:
  - **ACCEPTED**, with the same `s_verify` result;
  - `result.obj` (`6046f013…`) and `result_verify.json` (`e96e214a…`) are bit-identical;
  - the `return.npz` arrays are identical. Only its recorded source path string differs.
- **Result: PASS.**

**Delivered to:**
- the chat, as the attached file;
- `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\sheets\gorrund_05U_direct_sculpt\gorrund_05U_direct_sculpt_return.zip`, size confirmed on the device.

The working scene, the RETURN blend and the Step 0 fixtures remain in `…\gorrund_05U_direct_sculpt\scene\`. The fixtures and the `.blend1` backups there are disposable.

**→ STOP FOR TYLER / AUTHOR VISUAL REVIEW.**
