# Gorrund hand refinement — Codex progress

Date: October 20, 2026 (America/Phoenix).

Status: **ATTACHMENT REFINEMENT AVAILABLE LOCALLY FOR VISUAL REVIEW. NOT A PRODUCTION FREEZE.**

## Author direction

Tyler rejected the initial A/B/C directions because the human nail-bed anatomy remained too apparent and the claws were undersized relative to the fingers. He approved the direction of separate finger and thumb studies, requested that direction on the full model, and then authorized cleanup of the fingertip transitions and thumb attachments while keeping the overall claw size.

Reference: the Gorrund race specification, particularly its hand structure, articulation, dexterity and scale constraints. The older ordinary-nail wording is not silently rewritten; Tyler's current claw direction governs this visual experiment. The source model is not rescaled and the accepted stature envelope is not revised.

## Latest progress

- Completed separate finger/thumb anatomy studies and the initial ten-digit full-model visual candidate.
- Saved a new local review copy with smoother distal housing transitions and deeper root integration.
- Refined thumb attachment angles while retaining the approved claw-size direction.
- Generated relaxed views, thumb closeups and a controlled distal-flexion study.
- Checked local edit isolation, finite coordinates and basic face-area integrity. The protected production source remains unchanged.

The limited flexion screen is not a complete gripping pose or a production rig test. Some creasing/pinching remains visible, especially in the right-hand and bent-digit views. No deformation PASS is declared.

## Still pending

Author visual review; further local crease cleanup as needed; global self-intersection clearance; production rig/deformation acceptance; whole-hand grip/contact and collision validation. Separate keratin objects have not been accepted as a watertight production union.

v014, v015, v015b and the frozen source remain protected. No Unreal changes. Turnfall remains outside the task and untouched.

## Evidence location

Blender review copies, images, refinement scripts and detailed check reports remain in this Codex chat's local outputs/workspace. Automated approval review rejected exporting raw model coordinates and detailed derived geometry metadata to GitHub. This checkpoint therefore publishes only the plain-language progress summary; it does not upload those payloads or claim that they were published.

## Hand-quality audit in progress

The deeper intersection audit found additional defects in the candidate and also flagged portions of the protected source under the same method. Local hand repair is proceeding without changing the frozen production files or unrelated anatomy. Several distal patches have been rebuilt geometrically while preserving their topology and outer boundaries; the right-hand feature regions are treated separately.

A separate articulated hand test rig now exercises relaxed, fist, precision-pinch and handle-grip configurations. Initial trials exposed skin-weighting and thumb-opposition problems. Those trials are failures to be corrected, not production acceptance. Smooth connected-surface weights are replacing the initial weighting setup.

Current decision: HOLD. No global geometry, grip, rigging or production PASS, and no anatomical freeze. Detailed model evidence remains local in accordance with the earlier automatic approval restriction. An independent audit package will identify the unresolved checks explicitly.

## Quality-pass outcome: HOLD for independent audit

The quality pass is not complete or accepted. Local repairs improved the static mesh, but remaining intersection flags and the diagnostic rig's deformation/contact failures still block acceptance. The source control and actual Blender triangulation were cross-checked; fixed-diagonal triangle results are not interchangeable with the established quad-BVH gate.

The production component contract requires fused claws. The separate objects are visual-preview assets, and the fused-conversion preflight was not accepted. No production-ready fused character or passing hand rig is claimed.

A local, hand-only failure-analysis bundle has been prepared for Claude, with geometry crops, diagnostic bones/weights, checks and labelled failure sheets. It has not been transmitted. Raw model-data export still requires the explicit permission requested after the earlier automatic approval rejection. The repository receives this plain-language summary only.

Frozen sources, prior approved versions, Turnfall and Unreal remain untouched. No freeze or family propagation. The next audit must resolve the protected right-hand feature, component ownership, joint placement/weights and grip/contact gates before acceptance.

## Approved audit publication — 2026-10-21

Tyler explicitly approved sharing the prepared 22.7 MB hand-only audit bundle, including geometry, landmark coordinates, diagnostic rig bones/weights and failure reports, to this repository for Claude's independent review. This approval supersedes the pending-export status above.

- [Download the hand-only audit bundle](Wayfarer_Gorrund_Hand_Quality_HOLD_Audit.zip)
- [Read the independent audit instructions and limitations](AUDIT_REQUEST.md)
- Size: 22,672,065 bytes; SHA256: `d13d3b2890779d26e3e4d7e413b7b5fc7b4165ac742e3d6a6a3e1ea4f915bcaf`.

Status remains **HOLD**. Publication is a request for independent review, not evidence that Claude has reviewed or accepted it. The diagnostic rig and pose trials failed; no production freeze, fused-model acceptance or family propagation is authorized by this upload. Protected sources and Turnfall remain untouched.

## Repair progress — 2026-10-21

A separate fused diagnostic hand checkpoint now passes its local static intersection check: zero flagged triangles and zero verified crossings in the tested hand region. The full diagnostic body has one connected component, zero boundary edges, zero non-manifold edges/vertices, no unreferenced vertices, and the source's genus 1 under the triangle topology check. All 999,229 source vertices outside the connected source hand mask remain present at exactly their source coordinates. The protected v015 source SHA256 remains unchanged.

The checkpoint freezes its audited triangle tessellation to prevent curved-polygon retessellation from changing the surface during testing. It is a diagnostic target, **not the contract's manual quad production retopology**. No production freeze or global geometry PASS is declared. Unrelated source-control flags are not silently waived.

Hand rig repairs are continuing: source-fitted joint trials, continuous skin weights, rigid claw support, anatomically placed grip fixtures and finger-pad clearance. Relaxed, fist, precision-pinch and handle-grip trials are being inspected and corrected locally; they are not accepted deformation evidence yet. No rejected pose images or new raw geometry are uploaded at this checkpoint. Turnfall, Unreal and frozen production assets remain untouched.

## Functional hand repair checkpoint — 2026-10-21

Further pose inspection traced the stretched skin to inconsistent finger ownership in the diagnostic weights. The correction now follows connected finger surfaces and keeps each claw with its own fingertip, rather than assigning nearby skin across adjacent digits.

A distal tissue connection between two right-hand fingers is also present in the source control. The separate diagnostic candidate now opens that connection locally to permit independent articulation, consistent with the specification's fine-manipulation requirement. This is an explicit candidate change to the earlier preserved slit region; it does **not** inherit the v015 feature acceptance automatically. The protected source remains unchanged. The revised candidate has one closed manifold body and genus 0 after removing a tiny disconnected cut fragment; this topology change must be assessed during review rather than hidden behind the old genus-1 gate.

The repaired static hand region again has zero flagged triangles and zero verified crossings. The final local intersection correction was below one micron. Ten separate keratin surface regions are identified for rigid support. All 950,673 source vertices outside the complete source-hand mask remain at exactly their source coordinates, and the protected v015 file hash is unchanged.

Status remains **diagnostic work in progress**. Grip, pinch, clench, visual acceptance and manual production retopology are still being checked; no production or deformation PASS is declared. This update publishes only a progress summary. No new raw model bundle, rejected pose images, Unreal changes, family propagation or Turnfall changes are included.

## Manual hand rebuild started — 2026-10-21

The dense diagnostic mesh still develops skin folds during bending, so it has not passed deformation inspection. Further contact fitting alone will not resolve that. Work has moved to the contract's manual Blender UI retopology method, using a separate hand reference at native model scale and the race bible as constraints.

A new palm cage, four separately spaced finger roots, and the index finger's proximal and middle joint loops have been constructed manually and saved locally. This is an early construction checkpoint: the other digits, thumb, fingertip/claw shaping, surface fitting, body integration and deformation tests remain unfinished. The new cage is not a production-ready hand and has no visual or functional PASS.

Windows desktop Blender control is working. Only this isolated working copy is being edited. Frozen production files, Unreal and Turnfall remain untouched. This update contains prose only; no additional model geometry or rejected preview images are published.

## Visible hand sculpt cleanup completed — 2026-10-21

Tyler requested completion of the visible sculpt. Both hands now have smoother finger surfaces, cleaned claw-base transitions and material rims, and a rounded right-thumb claw root. The rough surface left by the diagnostic right interdigit separation was repaired locally. The substantial five-digit hand architecture and approved enlarged claw direction remain; the working model has not been uniformly scaled to the bible's nominal stature.

The finished sculpt review candidate passes the local static hand-region check with zero flagged triangles, zero verified non-adjacent crossings, zero near-zero-area triangles and finite coordinates. Its diagnostic body remains one connected closed surface, with no boundary or non-manifold edges, no unused vertices and Euler characteristic 2. All 950,673 reference vertices outside the complete hand mask are present at exactly their reference coordinates. The protected v015 source SHA256 is unchanged. Native height is unchanged from the input diagnostic candidate (204.51981985 cm); the bible's separately documented 204.5225 cm frozen-reference measurement and nominal race stature are not revised.

This completes the **visible sculpt cleanup only**. The saved local deliverable is `Gorrund_Hand_Sculpt_Complete_Review.blend`, accompanied by compact hand, thumb and full-model previews and a check report. This dense triangle surface is a sculpt review candidate, not the contract's manually built production quad mesh. The manual cage remains an unfinished separate construction; grip, pinch, clench, deformation acceptance, production freeze and family propagation remain **HOLD**. The local static result is not a global geometry or animation PASS, and no independent Claude acceptance is claimed.

Frozen production files, Unreal and Turnfall remain untouched. This repository update publishes prose only; no new geometry bundle or preview images are uploaded.

## Photo-reference claw revision — 2026-10-21

Tyler rejected the previous broad claw caps and supplied `1000007389.jpg` as the new visual target. That feedback supersedes any implied visual acceptance of the earlier claw shape. A new isolated review candidate now uses narrower claw roots and thickness, longer free edges, and more pronounced hooked points across all ten digits. Fingertip transitions were adjusted locally to support the slimmer profile; native body scale is unchanged. The approximate construction change was 45% greater axial claw span and an additional 10 mm of ventral curvature before local surface repairs. This is a visual interpretation of the photo, not an assertion of exact reference-image measurements.

The new local deliverable is `Gorrund_Photo_Reference_Claws.blend`, with compact both-hand, full-model and isolated hand-profile previews. The saved Blender file was reopened and its actual saved hand-region geometry checked: zero flagged triangles, zero verified non-adjacent crossings, zero near-zero-area triangles and finite coordinates. Its diagnostic surface remains one connected closed body, with zero boundary/non-manifold edges, no unused vertices and Euler characteristic 2. All 950,673 reference points outside the complete hand mask remain present at their exact reference positions; protected v015 SHA256 and the input candidate's native height are unchanged.

Status is **new visual review candidate; author acceptance pending**. Manual production quad construction, grip/deformation acceptance, global geometry acceptance, production freeze and independent Claude review remain open. This update publishes prose only. No new model or image bundle is uploaded, and frozen production files, Unreal and Turnfall remain untouched.

## Claw centering and root integration revision — 2026-10-21

Tyler identified poor blending and suspected off-center claws, particularly the pointer and pinky fingers. The new local review candidate fits each claw's root and lateral direction to the corresponding fingertip's surface cross-section centerline. Pointer/pinky root corrections were approximately 0.98 mm left pointer, -0.89 mm left pinky, 1.50 mm right pointer and 2.05 mm right pinky before final fairing; the points were also adjusted to follow each finger's direction. These are fitted sculpt references, not newly authoritative anatomical landmarks.

The raised collar-like junctions were rounded around the complete attachment, dorsal nail beds were extended back into the fingertips, and a small vertex-color transition softens the keratin/skin border. The geometry was corrected independently of that color transition. Direct isolated dorsal views of both pointers and pinkies and angled views of both complete hands were inspected; the longer hooked claw direction and native body scale remain.

Local deliverable: `Gorrund_Claws_Centered_Blended_Review.blend`, with both-hand and four-fingertip close-ups and a check report. The saved file was reopened and its vertices and triangle topology verified against the current inspected sculpt. Actual saved hand-region checks report zero flagged triangles, zero verified non-adjacent crossings, zero near-zero-area triangles and finite coordinates. The complete diagnostic surface is one closed connected body, with no boundary or non-manifold edges, no unused vertices and Euler characteristic 2. All 950,673 reference vertices outside the complete hand mask remain at exact reference positions; native input height and protected v015 file SHA256 are unchanged.

Status remains **visual review candidate; author acceptance pending**. The dense sculpt tessellation is not the contract's manual production quad mesh; production topology, deformation/grip checks, global geometry acceptance and independent review remain open. Only this prose progress record is published. No new geometry/images are uploaded, and frozen production files, Unreal and Turnfall remain untouched.

## Fingertip volume restoration — 2026-10-21

Tyler identified an abrupt reduction in finger thickness before the claw. The isolated sculpt now restores skin-pad and side-wall volume across all ten fingertips toward the earlier fuller sculpt, while retaining the substantial five-digit architecture and native scale required by the race bible. A smoothed displacement field gives the last-joint-to-pad transition a fuller profile. Every keratin vertex remains at its previous centered revision position; claw shape, centering and triangle topology are unchanged.

Local deliverable: `Gorrund_Full_Fingertips_Review.blend`, with compact both-hand, before/after pointer and side-profile previews. Front and side views were inspected. The saved file was reopened and verified against the inspected geometry. Its saved hand region has zero flagged triangles, zero verified non-adjacent crossings, zero near-zero-area triangles and finite coordinates. The complete diagnostic surface remains one closed connected body with 1,478,792 vertices, 2,957,580 triangles, zero boundary/non-manifold edges, no unused vertices and Euler characteristic 2. All 950,673 outside-hand reference vertices remain at exact reference positions. Native height (204.51981985 cm) and protected v015 SHA256 remain unchanged.

Status remains **visual review candidate; author acceptance pending**. Manual production quad construction, grip/deformation checks, global geometry acceptance and independent review remain open. This update publishes prose only, with no new geometry or images uploaded. Frozen production files, Unreal and Turnfall remain untouched.
