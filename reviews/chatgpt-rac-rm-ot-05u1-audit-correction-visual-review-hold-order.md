RAC RM-OT-05U1 — audit correction and author visual-review hold

**Authority:** Tyler requested the next instructions after the independent 05U return audit.
**Date:** October 13, 2026.
**Parent return:** `d6bdf9e9eb5150c832c22f97e38f56f81d1d82b6`.
**Parent Step 0:** `e378af140f40b718dc1142324445aa6989486d3b`.

## 1. Independent audit result

The uploaded `gorrund_05U_direct_sculpt_return.zip` is technically valid for the 05U author visual-review gate:

- 29,260,601 bytes; SHA-256 `aed5711fa00d193eccae9391f40de790d6e617333caa8add76554e81358a3159`, exactly matching the committed receipt.
- ZIP CRC integrity passes; all 27 manifest entries match, with no missing or unlisted payload files other than the manifest itself.
- All 25 files with 05U committed counterparts match the Git blobs byte-for-byte; the linked reference matches the verified 05T reference.
- All four RETURN_HASHES entries match, including the decompressed result OBJ.
- Independent array inspection confirms unchanged return topology and identity ordering, 101 moved editable vertices, no protected movement, and preservation of all 70,401 protected vertices including the 101 frozen-boundary vertices.
- V1 protected coordinate hash, source face correspondence and source coordinate preservation reproduce independently. Mesh boundary count is 320; non-manifold edge count is zero.
- The committed outputs report V2/V3 passing, reintegration ACCEPTED_FOR_VERIFICATION, V5 passing, and automated verdict UNRESOLVED. The independent audit did not rerun Blender or the full intersection verifier.

This finding establishes eligibility for visual review. It does not accept the Gorrund asset or certify that every geometric gate passes.

## 2. Correct the receipt additively

Correct the package receipt in `reviews/claude-rac-rm-ot-05u-gorrund-direct-sculpt-return-gate.md`:

- Change the own-manifest count from 26 to **27**.
- Change the clean-extraction count from 26/26 to **27/27**.
- Append a brief correction note identifying the counting error. The verified release bytes and ZIP hash stay as recorded.

Do not rebuild or replace the ZIP just to correct this receipt. Do not edit the packaged REPORT or manifest, which would change the verified release. The packaged REPORT predates the appended repository receipt.

Clarify that the V4 **failure and the eight bad-edge geometric measurements** are unchanged; the full V4 JSON is not identical because triangle-angle percentiles improved and result face indices were reordered. Do not change the verifier or thresholds.

If adding the audit limitation to the report, distinguish independently reproduced checks from the committed Blender/export/intersection evidence. Do not claim a new desktop test or a new full verification run.

## 3. Present the existing visual decision and stop

Use the existing identical-camera comparison images. Direct Tyler to:

- the posterior middle/lower strip, where the crinkled/notched surface has been substantially reduced;
- the remaining upper notches on the protected ring/source geometry;
- the softer fold edge in the front three-quarter view;
- the two new upper seam outliers (63.7 and 59.1 degrees), despite the overall V5 pass;
- the unresolved V6c-1 crease at theta -90 degrees, unchanged V4 bad edges and unchanged anterior V6c-2 failure.

Ask for Tyler's visual acceptance or specific revision direction. Do not infer approval from this instruction or the technical audit.

No additional brush stroke, boundary expansion, topology change, alternate candidate or scripted repair is authorized. Any request to remove the protected upper notches must first be returned to Tyler as a concrete boundary-extension proposal for approval; do not perform the extension.

## 4. Commit and hold

Commit the receipt correction and any concise clarification; report the commit and existing review images to Tyler. Keep the current asset and release unchanged.

Required state:

- Gorrund: **AUTHOR VISUAL REVIEW REQUIRED / UNACCEPTED**.
- Grask E3: **FROZEN**.
- RM-OT-05: **OPEN**.
- Stage C: **BLOCKED**.
- Canon promotion: **NOT PERFORMED**.
- D4 / UE5 / production rigging / creator implementation: **NOT STARTED**.
- Reconstructed skin: **INFERRED**.

**STOP FOR TYLER / AUTHOR VISUAL REVIEW.** Technical validation alone grants no permission to advance Stage C or canon.