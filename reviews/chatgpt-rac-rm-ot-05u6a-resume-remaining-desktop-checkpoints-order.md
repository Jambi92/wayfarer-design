# RAC RM-OT-05U6A — resume U6 from checkpoint 1; execute remaining bounded checkpoints if desktop control is available

**Authority:** Tyler-authorized autonomous continuation after review of the 05U6 checkpoint-1 return.
**Date:** October 14, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent order:** `reviews/chatgpt-rac-rm-ot-05u6-corrected-guards-targeted-desktop-repair-order.md` (a5279b1).
**Parent gate:** `reviews/claude-rac-rm-ot-05u6-targeted-desktop-notch-repair-gate.md` (c4b2634).

## Author ruling

Checkpoint 1 is accepted as a legitimate partial improvement and safe continuation point, but it is **not** accepted as the final bounded repair.

Independent review agrees with the 05U6 report:
- the lower notch/sliver cluster is improved;
- R2 cap quality is now healthy (face 130139 improved from 6.24° to 13.61°);
- both frozen crease-depth guards remain intact;
- protection, locus, topology, V1-U2, V2, V3, V5 and V6c-3 all hold;
- the visible higher saw-tooth marks remain;
- the only U6 mandatory numerical blocker is R1 target roughness at vertices 61559, 61581 and 61580.

The U6 verification contract, target set, exception set, frozen ring and scope remain unchanged. Do not reopen or redesign the guards.

## Resume point and budget

Resume from the exact saved checkpoint-1 scene:

`GO-05U6_cp1.blend`
SHA-256 `6262620e18732d1672ea4b62d53581eda2a34e4329144a91936cc51f42ddf2dd`.

The historical budget remains:
- checkpoint 1: spent;
- checkpoint 2: available;
- checkpoint 3: available.

Do not reset or reinterpret the budget.

## Checkpoint 2

If real desktop Blender control is available and permitted, execute the already documented checkpoint-2 plan from the 05U6 edit log:

- vertex **61559**: lift approximately **0.30 cm along its current vertex normal**;
- vertex **61581**: lift approximately **0.10 cm along its current vertex normal**;
- vertex **61750**: lift approximately **0.10 cm along its current vertex normal**, intended to improve the 61580 / face-130133 local roughness without directly moving crease-B anchor 61580.

These are intended local actions, not mandatory blind coordinates. Before committing each typed position, visually inspect the local surface and preserve anatomical judgement. If the current normal or scene state makes one move visibly wrong, use a smaller bounded Edit Mode correction instead; disclose the exact value.

Do not move 61580 unless checkpoint-2 verification demonstrates that the indirect 61750 correction cannot bring the local target into range and a direct movement can still preserve frozen crease B. Any direct movement of 61580 belongs, at earliest, to checkpoint 3.

After checkpoint 2:
1. save as a distinct `GO-05U6_cp2.blend`;
2. run the unchanged `check_return_u6.sh`;
3. record all exact changed vertices/faces;
4. inspect identical-camera posterior and zoom views;
5. report target roughness values for all 16 target vertices and frozen A/B crease depths.

If all U6 mandatory gates pass and the visible upper saw-tooth is resolved without a dent, lip, spike or melted patch, package checkpoint 2 as the return and STOP for Tyler's visual review.

## Checkpoint 3, only if needed

Use checkpoint 3 only if checkpoint 2 is safe and materially closer but still misses one localized U6 target.

Checkpoint 3 may make one final small desktop Edit Mode / Grab / Smooth / Relax correction inside the existing 16-vertex target, under the exact 05U6 authorization.

Do not widen the target, editable set, boundary, frozen ring or method scope. Do not repair the anterior taper, far posterior taper or unrelated global V4/V6 items.

If diagnostics show checkpoint 3 cannot satisfy the remaining blocker without damaging crease A/B or visual anatomy, return the best safe checkpoint instead of forcing a numerical pass.

## Desktop-control limitation

This order provides project/author approval to continue the authorized U6 edits. It does **not** authorize bypassing or defeating any system safety or access control.

If the desktop-control system again refuses the Blender interaction, STOP and report the exact blocker. Do not use a scripted substitute, coordinate generator, headless geometry edit, or fabricated desktop action.

## Success condition

A successful return must satisfy the existing U6 mandatory gates exactly. No thresholds or sets change under this continuation.

If successful, state:

**TECHNICALLY VALID BOUNDED RETURN / AUTHOR VISUAL REVIEW REQUIRED**

and deliver the corrected scene, checks, exact change log, identical-camera evidence, hashes and a new package/manifest or an explicitly versioned continuation package.

Then STOP.

Gorrund remains UNACCEPTED pending Tyler's visual ruling; Grask E3 FROZEN; RM-OT-05 OPEN; Stage C BLOCKED; no canon promotion, D4, UE5, production rigging or creator implementation.
