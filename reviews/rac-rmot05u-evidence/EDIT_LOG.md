# EDIT_LOG: RM-OT-05U direct sculpt (Gorrund +X armband interface)

**Operator:** Claude, driving the desktop Blender UI on Tyler's PC through computer use (screenshots plus mouse and keyboard). No Python was run inside Blender for any geometry change.
**Desktop app:** Blender 5.2.2 LTS (portable), `E:\Tools\Blender\blender-5.2.2-windows-x64\`.
**Work folder:** `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\sheets\gorrund_05U_direct_sculpt\scene\`.
**Return check:** the supported `check_return.sh`, run in the container with bpy 5.0.1 on files copied back from the PC.

## Step 0: desktop check on disposable fixtures. Result: **PASS**

**Fixtures:**
- `fixture_test.blend` and `fixture_test2.blend`, both byte copies of `GO-05T_sculpt_handoff.blend` (`c7e591fe…60cc`);
- `GO-05T_references.blend` sits beside them.

**Hashes of the returned fixtures:** `step0/FIXTURE_HASHES.sha256`. **Check outputs:** `step0/checks_*`.

| # | Requirement | What was done in the UI | Result |
|---|---|---|---|
| 2a | Units | Scene Properties → Units | Metric, Unit Scale 0.010000, Length Centimeters: **PASS** |
| 2b | Identity transform | Object Properties of `GO-05S-S3_working` | Location 0 cm, Rotation 0°, Scale 1.000: **PASS** |
| 3 | Linked references | Outliner: `REFERENCES_linked_readonly` holds `B2_reference` and `F1_source_reference` (link icons, hidden). F1 shown with the eye icon, then Tab pressed with F1 selected | F1 displays. Tab did **not** enter Edit Mode (linked data cannot be edited). Hidden again: **PASS** |
| 4a | Show the sculpt mask | Sculpt Mode → Sculpt Mode Overlays | Mask overlay on (0.75) and Face Sets overlay on. Mesh revealed with Alt+H (fixture only) so the masked grey shows around the blue (face set 2) and yellow (face set 3) patches: **PASS** |
| 4b | Test brush stroke, grey and editable | Draw brush, size 100 px, strength 0.5 | See the three attempts below: **PASS** |
| 5 | Edit-mode isolation | `fixture_test2.blend`, Tab into Edit Mode, Statistics overlay | Visible 797 / 141,194 faces and 451 / 70,751 vertices (350 editable + 101 frozen ring). Nothing else visible: **PASS** |
| 6 | Supported check on an allowed edit | `check_return.sh` on `fixture_test.blend` after the strokes | `ACCEPTED_FOR_VERIFICATION`, `V1_outside_anatomy True`: **PASS** |
| 7 | Deliberate protected move | `fixture_test2.blend`, Edit Mode, Alt+H (fixture only), one foot vertex selected (1 / 70,751), G Z 0.05 (header: "D: 0.05 = 0.5 mm (0.0500 cm) along global Z"), Tab, Ctrl+S | `REJECTED`. P1: 1 vertex moved (S3 index 67315); P2: 4 faces missing: **PASS** |

**Test strokes (4b), measured by the return check against S3:**
1. **One synthetic drag** (press, jump, release). Recorded in the undo history as a Draw Brush step, but **0 vertices moved** anywhere. A single-jump drag gives Blender no intermediate motion events, so this attempt proves nothing.
2. **Stroke built from small mouse moves, mostly inside the blue patch.** 21 of 350 editable vertices moved (up to 0.53 cm). 0 of 70,401 protected vertices changed. Accepted.
3. **Stroke starting on masked grey and crossing into blue.** 6 more editable vertices moved (up to 0.17 cm). Grey stayed **bit-identical**: P1 70,401 / 70,401 unchanged; P2 140,397 / 140,397 present. **Only the editable area deformed.**

**Other observations:**
- **First protected-move attempt.** The value "0.01" was sent with the text-typing tool. Blender recorded a Move of zero length, and the export showed 0 vertices changed. The digits were then sent as individual key presses, the header confirmed 0.05 cm, and the move was applied. That second attempt is the one reported in row 7.
- **Version.** Files saved by Blender 5.2.2 read correctly in the container's bpy 5.0.1, with the warning "File written by newer Blender binary". The identity attribute survived the save: all 70,751 vertices were verified by `rac_s3_vid1` plus bit-exact position.
- **Backups.** Blender 5.2.2 writes `.blend1` backups next to saved files (a desktop preference). They are not part of the return.

## Production sculpt (only after Step 0 passed)

**Scene setup:**
1. Opened `scene/GO-05T_sculpt_handoff.blend` (sha `c7e591fe…60cc`).
2. **File → Save As** `GO-05T_sculpt_RETURN.blend` in the same folder, before any edit. `GO-05T_references.blend` stays beside it, and the handoff file was not modified.
3. Entered Sculpt Mode and revealed the full mesh (Alt+H in Sculpt Mode) so the surrounding anatomy was visible for judgement. This changes hide flags only; the mask still protected everything outside the interface. Mask overlay 0.75; face-set overlay lowered to 0.2 so the shading reads.
4. View → Viewpoint → Front (this looks at Gorrund's back from −Y), then Shift+B zoom-border onto the posterior interface.

**Tool:** the **Smooth** brush (Blender 5.2.2 essentials asset), with ordinary interactive strokes from mouse-down, mouse moves and mouse-up. Nothing else was used: no Draw, Clay, Dyntopo, remesh, Grab, topology change or modifier, and no script or coordinate operation.

| Pass | Brush settings | Stroke | Purpose |
|---|---|---|---|
| 1 | Smooth, 100 px, strength 0.7 | Down the centre of the crinkled strip, top to bottom | First test of the strip |
| 2 | Smooth, 200 px, strength 0.7 | Down the medial (trunk-side) edge of the strip | Remove the saw-tooth facets along the fold edge |
| 3 | Smooth, 200 px, strength 0.7 | Down the lateral (arm-side) edge, curving at the lower end | Blend the strip into the arm side |
| 4 | Smooth, 200 px, strength 0.7 | Zig-zag across the upper third | Remove the notches in the upper strip |
| 5 | Smooth, 140 px, strength 0.4 | Short local stroke at the top-medial corner | Light touch on the remaining top notches |

Checkpoints were saved after passes 3, 4 and 5 and checked with `check_return.sh`; all were ACCEPTED. **Pass 5 changed almost nothing.** The notches still visible at the top of the strip lie on **protected** vertices (source and frozen-ring vertices at θ −84…−90°, s 8–10 cm, outside the editable set; listed in the report). They cannot be sculpted under the order, so I stopped.

**Anterior:** not touched; no stroke was made there. **No Dyntopo, remesh or local topology edit** was needed or used.

**Result:**
- 101 of the 350 editable vertices moved. No vertices were added; topology is unchanged (141,194 faces).
- Protected vertices: 70,401 / 70,401 bit-identical, including all 101 frozen-boundary vertices.
- Object, transforms, units, `rac_s3_vid1`, `rac_src_vid1`, `rac_label`, mask and face sets are all retained. There are no modifiers, and the linked references are unchanged.
