# RAC RM-OT-05U5 — approved bounded upper-notch revision; real desktop sculpt

**Authority:** On October 14, 2026, Tyler explicitly delegated the limited-revision approval decision to ChatGPT: "Do what you think is best and send the next instructions." Following the independent 05U2–05U4 review, ChatGPT approves the boundary, method and verification contract specified below. Do not ask Tyler to reapprove this same scope.
**Readiness closure:** `421bf752e306072a3c3fd5626c2d0e0dbebcc55d`.
**Approved proposal:** `reviews/claude-rac-rm-ot-05u2-upper-boundary-extension-proposal.md`, as clarified by 05U3 and corrected by 05U4.

## 1. Authorization is limited to this revision

Build the bounded U2 handoff, complete the real desktop fixtures, and only if those pass perform the localized posterior upper-notch revision through the actual Blender desktop UI. Then verify, package and return the result for visual review.

This authorizes changes to the exact 35 original source faces / 15 additional source vertices in the committed proposal. It does not accept Gorrund, authorize a wider repair, advance Stage C or promote canon.

## 2. Pin the approved region and baseline

Use the verified 05U RETURN as the frozen starting point. Preserve its `.blend`, linked reference, return arrays and released ZIP unchanged (release SHA-256 `aed5711fa00d193eccae9391f40de790d6e617333caa8add76554e81358a3159`). Preserve `base.glb` and the previous default protection path.

Approved lists are those in `reviews/rac-rmot05u2-proposal/`:

- 35 added faces: hash `483ab7feac190c76679eadc3ce677cd8e538349e2dc4842c6db0dfd441797692`.
- 15 added source vertices: hash `5be5a27f133f9e936f6d4164340eb7561de8af0bc9016f17a97aa5fdc6cd0aa1`.
- 365 total editable vertices: hash `0154b2be773056f049e7a729f15d97e8844fb3862c77b58a760f7c2666e95559`.
- 106 frozen-boundary vertices: hash `91725db2ca491529305c0a77e14f89db5578628bba7500d9495536f724340426`.
- 832 total editable-region faces; P05U2 protects the other original source faces as defined in the committed preview.

The lists define a maximum authorized region, not a requirement to move every listed element. Actual production brush work is restricted to the upper cap and roughly 1 cm of the existing posterior strip immediately below it. Leave the anterior and the remaining existing interface alone. Do not widen or regenerate the approved lists.

## 3. Build and test the handoff before production

On a new copy of the unchanged 05U RETURN, build `GO-05U2_sculpt_handoff.blend` with exactly the approved editable set, the 106-vertex frozen ring, clear face sets/groups and the linked references preserved. Verify units, identity transform, object name, attributes, correspondence, masks and absence of modifiers. All added reconstructed/edited source surface remains INFERRED, separately labelled 6 in return provenance.

Use clearly separate disposable `.blend` fixtures to perform the real desktop checks:

1. Show the new mask and face sets; inspect the cap and new ring.
2. Perform a real brush stroke crossing from protected grey into the newly editable cap. Prove that editable geometry actually moved and all geometry outside the approved set stayed exact.
3. Deliberately move a protected vertex just outside the boundary: the supported U2 protection check must reject it.
4. Move a new frozen-ring vertex and a retained old frozen-ring vertex in separate fixtures: both must be rejected.
5. Export an unchanged fixture through the supported path: reconstructed geometry must be identical to the verified 05U baseline, apart from the approved face ordering/labels.

Record the exact desktop actions and results. Synthetic array tests from 05U3/05U4 do not replace these. For fixtures, distinguish protection acceptance from the expected roughness failure of the unrepaired baseline.

If any fixture fails or the desktop UI cannot be controlled, STOP before production. Report the precise blocker; do not create a scripted substitute.

## 4. Execute the approved desktop revision

After every fixture passes, open the clean handoff and Save As a new return file before editing. Do not continue from a stroked or deliberately damaged fixture.

- Smooth brush only, low strength approximately 0.3–0.4, small localized radius, strokes along the crease.
- Remove the residual upper saw-tooth/notched read while preserving the natural groove, adjacent relief and established middle/lower strip.
- At most **three deliberate production passes total**, with checkpoint saves and inspection. Do not reset the pass budget by reopening, renaming, undoing or relabelling a pass.
- No Draw, Clay, Grab, Dyntopo, remesh, topology editing, global smoothing, coordinate sweep, scripted relaxation or generated substitute mesh.

Stop as soon as the intended visual correction and all numerical stop conditions are met. If three passes are insufficient, or the crease flattens / the surface becomes over-softened, return the best clearly identified safe checkpoint and report the limitation. A checkpoint that fails the conditions is a failed attempt, not an accepted repair. Do not widen the boundary or silently relax any guard.

## 5. Verify with the corrected 05U4 path

Use `tools/rac/w1/rmot05u4_drivers/check_return_u2.sh`, the supported exporter and the approved pinned inputs. Do not use the historical moving-plane 05U3 command, the ordinary OBJ exporter as authority, `--ref_sha` overrides or custom pin overrides.

The immutable reference is `reviews/rac-rmot05u4-readiness/crease_reference_v1.json`, SHA-256 `c1efefde5b50316b1ff4b2edaeae3fe702dc94b9722f52ba8da7f6d490772d51`. Do not rebuild it from a sculpted mesh.

Required numerical stop conditions:

- supported U2 reintegration accepted; exact protection outside the 365 vertices / 832 faces, including all 106 frozen-boundary vertices;
- no topology change; full source correspondence retained; label 6 explicitly accounts for the 35 added source faces;
- V1-U2 passes; no hard FAIL verdict from the unchanged geometry criteria;
- fixed section A depth at least **0.6712880840904568 cm**; fixed section B depth at least **0.27434876590971574 cm**, using the frozen planes/chords;
- roughness guard (b) passes: none of the 365 editable vertices above the committed 36.3-degree limit;
- sliver guard (e) passes for all 35 added faces, using the committed baseline-relative guard and its documented numerical tolerance; none below 5 degrees;
- `aggregate.json` reports numerical stop conditions PASS and the supported command exits 0. Missing, ambiguous or non-finite measurements are failures.

Numerical PASS is not visual acceptance. Inspect identical-camera evidence for a natural crease with no persistent notch facets, cut lip, extra fold or over-softening.

Report the original P05S/legacy diagnostic and enumerate actual source vertices and faces affected; they must remain within the authorized 15 / 35. Report V2–V6c honestly, including the unresolved theta -90 crease, the eight untouched taper edges and the anterior taper failure. These remain unwaived; this order does not authorize their repair or require their scores to pass. The source sliver at S3 face 130139 remains under guard (e).

## 6. Return evidence, package and stop

Return:

- real desktop fixture evidence and an edit log of the actual production brush passes;
- the new sculpt return `.blend` and linked reference;
- supported return NPZ/OBJ (lossless gzip acceptable), reintegration/maps/labels, full geometry verification, fixed-reference crease measurements, guards, aggregate result and hashes;
- identical-camera **05U baseline versus revised return** posterior shaded/wire, upper zoom shaded/wire and arm context including yaw 45 and underside;
- exact protected geometry counts, actual changed vertices/faces and preservation checks;
- a new, distinctly named ZIP with its own complete manifest, CRC/clean-extraction and hash verification, and a rerun of the corrected return path on the extracted scene. Preserve the old release.

Commit `reviews/claude-rac-rm-ot-05u5-bounded-desktop-sculpt-return-gate.md` and evidence under `reviews/rac-rmot05u5-evidence/`; update status and queue. Deliver the new package to the established project location and attach it if supported.

If successful, state **TECHNICALLY VALID RETURN / AUTHOR VISUAL REVIEW REQUIRED**. Otherwise report the failed attempt or blocker without claiming completion. Do not present missing evidence, partial movement or protection-only acceptance as a successful repair.

**STOP after the return.** Gorrund remains UNACCEPTED pending visual review; Grask E3 FROZEN; RM-OT-05 OPEN; Stage C BLOCKED. No canon promotion, D4, UE5, production rigging or creator implementation. This delegated approval covers only the bounded revision above.
