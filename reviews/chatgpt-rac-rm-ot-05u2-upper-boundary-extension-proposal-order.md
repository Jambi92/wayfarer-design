# RAC RM-OT-05U2 — propose a minimal upper-boundary extension; no sculpt authorization

**Authority:** Tyler requested these instructions after the recommendation to review a concrete boundary-extension proposal before accepting Gorrund.
**Baseline:** verified 05U return, SHA-256 `aed5711fa00d193eccae9391f40de790d6e617333caa8add76554e81358a3159`.
**Context:** Synced repository history confirms the 05U1 correction/order in `81cbf62f5c4ef864ef57fbbb2bb0dd56ed7016bf`, followed by wording fix `d472156827cd7e162f6da51463ef74195a3ba0dc`. Continue from that corrected review hold.

## 1. Decision and scope

The posterior middle/lower strip is substantially improved, but the remaining upper notches warrant a bounded revision proposal before author acceptance. Gorrund remains UNACCEPTED.

Prepare a concrete, minimal proposal to extend the editable region around the remaining upper posterior notches. This authorizes read-only inspection, measurements, annotated views and proposal preparation only. Do not alter any mesh, mask, face set, protection set, scene or released package. Do not sculpt or produce an alternate candidate.

## 2. Establish the exact proposed region

Inspect the final 05U RETURN and its verified S3 correspondence. Confirm rather than assume the reported upper-notch vertices:

- S3 frozen-ring vertices 61303, 61559 and 62065;
- S3 source vertices 61581, 61580 and 61562;
- approximate region theta -84 to -90 degrees, s 8 to 10 cm.

State whether all indices are zero- or one-based and identify the exact reference mesh/hash used. Supply machine-readable vertex and face lists with hashes for both the current editable region and the proposed additions. Explain which current protection category each added vertex/face belongs to.

Propose the smallest coherent extension that could remove the upper notches and blend the two new seam outliers without shifting adjacent shoulder/axilla architecture or flattening the natural crease. Describe any vertices that must remain frozen and the proposed replacement frozen boundary. Identify source-surface changes explicitly; do not conceal them as an interface-only operation.

If the defect cannot be addressed by a small local extension, report that limitation and stop. Do not expand the scope to solve it.

## 3. Show the author exactly what would change

Provide clearly labelled views of the unchanged 05U return showing:

- current editable region and frozen boundary;
- proposed added vertices/faces, with the remaining protected anatomy distinct;
- proposed new frozen boundary;
- the residual notches and the seam locations at theta -88.4 degrees / s 8.0 cm and theta -85.7 degrees / s 7.89 cm;
- posterior close-up, wireframe and front three-quarter view (yaw 45), plus enough arm context to judge scope.

Use the existing comparison camera definitions where applicable. These are annotated proposal views, not before/after evidence of an unperformed repair.

## 4. Propose the method and verification contract

Describe the intended localized desktop brush work, how it would preserve a natural fold without over-softening, and a clear stop condition. Do not perform it.

Explain the exact additive changes approval would require to protection sets and the supported return pipeline. Preserve a frozen baseline and the existing checks. A revised boundary must be explicit, versioned and approved before use; never weaken a validator silently or modify thresholds to make a result pass.

List required post-approval tests: real desktop mask/protection fixture checks for the revised region; rejection of an edit just outside the new boundary and of a moved frozen-boundary vertex; exact preservation outside the approved extension; supported reintegration; V1-V6c reporting; identical-camera before/after views; package/hash verification. Separate changed protection rules from unchanged geometry quality criteria.

Report the current unresolved V6c-1 crease, V4 bad edges and anterior V6c-2 failure as context. Do not include repairs to the untouched taper or anterior in this proposal, and do not interpret them as waived or accepted.

## 5. Deliver and stop

Commit the proposal at `reviews/claude-rac-rm-ot-05u2-upper-boundary-extension-proposal.md`, with supporting lists/overlays under `reviews/rac-rmot05u2-proposal/`. Update status/queue pointers to PROPOSAL AWAITING AUTHOR APPROVAL without marking any repair or acceptance complete.

Return the commit, proposal, annotated views and exact scope for Tyler's approval. Ask Tyler to approve or revise that defined boundary and method. An approval of this proposal would authorize only its stated revision, not Gorrund acceptance or Stage C.

**STOP. No geometry or protection-set mutation until Tyler approves the concrete proposal.**

Required state: Gorrund UNACCEPTED; Grask E3 FROZEN; RM-OT-05 OPEN; Stage C BLOCKED; reconstructed skin INFERRED; no canon promotion, D4, UE5, production rigging or creator implementation.
