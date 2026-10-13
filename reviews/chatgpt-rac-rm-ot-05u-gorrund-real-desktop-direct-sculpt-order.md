# RAC RM-OT-05U — perform the real desktop direct sculpt from the verified 05T handoff

**Authority:** Tyler-authorized continuation after review of the completed 05T/05T1 release.  
**Date:** October 13, 2026.  
**Repository:** `Jambi92/wayfarer-design`, `main`.  
**Parent closure:** `reviews/claude-rac-rm-ot-05t-gorrund-direct-sculpt-handoff-validation-closure.md`.  
**Verified release:** `gorrund_05T_sculpt_handoff.zip`, SHA-256 `8bb33bf0a106cfd54b75a7085c443f8e03e19e4e71f69ce80535482495e37d9e`.

## Author ruling

The 05T package is accepted as the correct technical handoff. Its package hash, ZIP integrity and 69-file manifest have been independently checked, and the supplied views correctly isolate the posterior crinkled/notched strip inside the editable interface.

Proceed to the **actual direct sculpt**. This is not another procedural repair study.

## 1. Mandatory desktop Step 0

Use the desktop Blender application and follow `START_HERE.md` Step 0 on a disposable `fixture_test.blend`.

You must actually perform the UI checks:
- confirm units and identity transforms;
- inspect the linked F1/B2 references;
- show the sculpt mask;
- make a real test brush stroke across masked grey and editable purple;
- verify only purple deforms;
- verify edit-mode isolation;
- run the supported `check_return.sh` fixture path;
- deliberately move one protected grey vertex and prove the return check rejects it.

Record the exact result in `EDIT_LOG.md`.

**If any Step 0 requirement fails, STOP.** Do not touch the production scene. Commit a short failure report describing exactly what failed and what must be corrected.

## 2. Production direct sculpt

Only after Step 0 passes:

1. Open `scene/GO-05T_sculpt_handoff.blend`.
2. Save As `GO-05T_sculpt_RETURN.blend`, preserving the linked reference file beside it.
3. Work interactively in Blender Sculpt Mode on the authorized interface only.

### Primary target

Fix the **posterior crinkled/notched strip** along the posterior axillary-fold edge:
- remove the saw-tooth / crumpled surface read;
- restore a natural arm-to-posterior-axillary-fold crease;
- preserve the adjacent deltoid and triceps relief;
- preserve a deliberate tapered termination of the remaining garment region;
- do not create a cut lip, ledge or second fold.

The anterior transition is already plausible. Leave it alone unless a very small local adjustment is necessary for continuity.

### Sculpt method

Use real interactive sculpt judgement. Prefer ordinary localized brush work and the existing topology.

Do **not** recreate the prior scripted-profile method. Do not write a coordinate sweep, solver, interpolation pass, relaxation process or automatic candidate generator and call it a sculpt.

Local topology editing is allowed only if genuinely needed and only inside the purple editable faces. Avoid Dyntopo/remesh unless ordinary sculpting cannot solve the defect. Never remesh or smooth the whole object.

## 3. Hard protection rules

Do not alter:
- any grey/masked geometry;
- `FROZEN_interface_boundary`;
- object transforms, scale, pose or limb proportions;
- object name `GO-05S-S3_working`;
- `rac_s3_vid1`, `rac_src_vid1`, or `rac_label`;
- the source master `base.glb`;
- any other garment region;
- shoulder/axilla architecture outside the committed interface.

No full-ring removal, arm-trunk separation, global smoothing/remesh, RD5, LOW, blind study, scaffold, Rodin generation, canon rewrite, D4, UE5, rigging or creator implementation.

All newly exposed/reconstructed skin remains **INFERRED**.

## 4. Return verification

Run only the supported return path:

`bash tools/rac/w1/rmot05t_drivers/check_return.sh scene/GO-05T_sculpt_RETURN.blend checks/return`

Do not use Blender's ordinary Wavefront OBJ exporter as the authoritative return.

Required technical outcome:
- reintegration accepted;
- P1/P2 protection passes exactly;
- V1 outside anatomy passes;
- no protected or frozen-boundary changes;
- no new non-manifold geometry or intersections;
- V4/V5/V6c results reported honestly.

A technical pass is **not** visual acceptance.

## 5. Required visual evidence

Produce identical-camera before/after views:
- posterior shaded close;
- posterior wireframe;
- anterior shaded;
- anterior wireframe;
- underside;
- lateral;
- rear 3/4;
- arm overview.

The result must visibly remove the crinkled/notched strip and read as continuous anatomy, not merely improve numeric scores.

## 6. Deliverables

Return:
- `GO-05T_sculpt_RETURN.blend`;
- `return.npz` and `return.obj`;
- `result_reintegrate.json`;
- `result_verify.json`;
- `RETURN_HASHES.sha256`;
- all `compare_*.png`;
- `EDIT_LOG.md` including the real Step 0 desktop results and the actual brushes/tools used.

Create a compact return package with its own manifest and clean-extraction/hash verification. Put the usable package on the established E: drive project location and attach it to the chat if supported.

Commit:
- `reviews/claude-rac-rm-ot-05u-gorrund-direct-sculpt-return-gate.md`
- supporting evidence under `reviews/rac-rmot05u-evidence/`

Do not commit a fabricated desktop result. If the desktop UI cannot actually be controlled in the current session, report that limitation and stop without generating a substitute mesh.

## 7. Stop gate

After the verified direct-sculpt return is produced, **STOP FOR TYLER / AUTHOR VISUAL REVIEW**.

Do not promote Gorrund, do not begin Stage C and do not expand the sculpt to other regions until author acceptance.

Expected state after a technically valid return:
- **Gorrund: AUTHOR VISUAL REVIEW REQUIRED**
- **Grask E3: FROZEN**
- **RM-OT-05: OPEN**
- **Stage C: BLOCKED**
- **Canon promotion: NOT PERFORMED**
- **D4 / UE5 / production rigging / creator implementation: NOT STARTED**
