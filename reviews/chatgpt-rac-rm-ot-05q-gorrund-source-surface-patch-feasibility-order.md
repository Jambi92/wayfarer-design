# RAC RM-OT-05Q — Gorrund source-surface clothing removal: one-patch feasibility

**Authority:** Tyler-approved next order after author review of racebodies_v120 and the 05P gate.
**Date:** October 12, 2026 (America/Phoenix).
**Parent:** 05P order bcab9bc2b080f5f14215564e15a36809a653fb48; reviews/claude-rac-rm-ot-05p-gorrund-anatomical-repair-gate.md.
**Status:** Execute source inspection and one representative local patch study. Commit evidence and STOP for author visual review, even if successful. No whole-body restart in this block.

## 1. Author ruling

Reject RD4 as the accepted Gorrund reference. Accept the useful 05P diagnostic evidence and proper stop: the images show only marginal improvement, with soft/erased anatomy, columnar trunk/pelvis and unresolved knobby joints/tubular shanks. The LOW mask-preservation result is useful tooling evidence, not anatomical or species acceptance; mask placement still uses proxy landmarks.

The author verified all 48 files in v120's evidence checksum manifest, but did not independently rerun sculpting or geometry checks.

Freeze RD1–RD4 and all earlier results as provenance. Do not continue patching RD4. Authorize a new source-surface feasibility study only: determine whether local clothing removal/reconstruction can preserve F1's exposed anatomical surface. This is not acceptance of source muscularity, proportions, paws or garments as canon.

## 2. Recover the actual source surface with provenance

Use the historical source master base.glb, SHA-256 78ecfa87d169380ecb46ece3f0c0df3491d10e4547038a3c35c06df933f38a7b, unchanged. Re-hash accessible master/copy and record location, size and hash. If unavailable, report the blocker; do not substitute an RD remesh.

Use F1's detailed extracted surface before 05N occupancy, signed-distance field, large-radius opening, blur or z-relaxation. Trace it to the original component/figure and reproduce its extraction. Document the F1/F2 contact-slab cut, open arm seam and any other extraction changes. Distinguish original extraction from later half-mirroring; do not describe a mirrored/repaired surface as untouched. Preserve both original and working copies and an explicit transform record.

Keep the existing documented reference coordinate/display frame for comparison. No stance correction, limb lengthening, stature normalization of actual geometry, body-composition edit, head/tail change or broad muscle reduction in this block. Any display scaling must be labeled separately from source coordinates.

## 3. Verify clothing separability before claiming it

Inspect the source mesh, not just its rendered appearance. For belt/loincloth, bracers/armbands, shin/ankle wraps, necklace/ornaments, and hair/mane over the body, classify:
- separate disconnected geometry with intact underlying body;
- attached/fused ornament with a local removable boundary and recoverable underlying surface;
- garment replacing the body surface, with hidden anatomy absent;
- ambiguous or inseparable with current tools.

Provide local wireframe/cross-section/underside views, component or face-set identifiers, boundary loops and evidence of whether body exists underneath. Appearance as a layer is not proof of topological separability. Do not assume the 11 global source islands map to separable garment layers within F1.

Include a garment/body face-label inventory with confidence and known errors. Where anatomy is absent, say it requires reconstruction; do not infer its true volume from the outer garment silhouette or claim it was recovered.

## 4. Select one representative patch and commit the plan

Select ONE local garment/body interface that tests genuine surgery and continuity, such as a bounded bracer or shin-wrap segment adjacent to exposed anatomy. Avoid selecting a floating pendant whose deletion proves nothing about reconstructing a body patch. Do not attempt the whole pelvis or an entire limb.

Explain why this patch is representative, what it can prove and what remains untested elsewhere. If no reasonable patch can be isolated, deliver the inspection and stop with a feasibility limitation.

Before the edit, commit a short plan containing source/baseline hashes, exact patch bounds, garment face sets, preserved anatomy sets, seam/blend band, proposed local method and verification criteria. Keep that plan commit distinct from the result commit so sequence is reviewable. No parameter sweep or trial selection based on scoring.

## 5. Perform one local source-preserving repair

Work on a duplicate. Remove only verified garment/ornament faces in the declared patch. Preserve exposed anatomical vertices/faces outside the patch and seam band exactly. Do not remesh, voxelize, smooth, decimate or diffuse the entire figure. Local topology changes are permitted inside the declared repair area; document any seam-band edits and correspondence to the original source.

If intact anatomy is present underneath, preserve it. If absent, reconstruct only the missing local patch with anatomical continuity guided by adjacent visible forms and documented reference evidence. Label reconstructed geometry explicitly. Do not invent high-frequency detail under clothing as recovered anatomy.

Any surface projection must use a vetted anatomical donor mask: no garment/wrap/strap edges, necklace, braids or unrelated nearby body surface. Show donor selection, excluded garment faces, projection direction/distance constraints and correspondence. Do not project the clothed source indiscriminately or recreate clothing as skin. If valid anatomical donor detail does not exist for the hidden region, leave the reconstruction honestly inferred; do not fake source recovery.

Preserve the source's visible form quality without making its exaggerated muscularity a new requirement. Do not add broad monster bulk or reshape the race to make this patch succeed. Use local mesh surgery/direct sculpt tools; if current tooling cannot do it credibly, disclose that and stop instead of returning to whole-body fields.

Retain the original patch, edited patch, intermediate results and any rejected attempt produced during this bounded operation. State failures plainly. No automatic second patch or full-body extension.

## 6. Verify geometry and visual continuity

Provide:
1. Same-camera, same-material before/after close views from multiple angles; wireframe and cross-sections at the seam.
2. A full-figure contextual view so the local scope is visible, without claiming a new full-body reference.
3. Color overlay distinguishing untouched source anatomy, removed garment, reconstructed patch and edited seam band.
4. Source-to-result vertex/face correspondence outside the patch; count/hash proof that protected anatomy coordinates and faces are unchanged. Report seam-band displacement separately.
5. Boundary, manifold, normal/winding and self-intersection checks scoped to the patch; pre-existing source defects listed separately. A whole source need not be declared watertight when it is not.
6. Evidence that garment ridges/edges are absent from the repaired skin, and adjacent anatomical relief remains intact without pinching, inflated smoothing, discontinuities or a blank-clay patch.

Do not apply a global repair to obtain a clean validator result. Geometric validity and surface continuity are separate findings. A correct seam or zero outside displacement is not enough if the patch looks anatomically poor.

Report PASS / FAIL / INCONCLUSIVE for this local feasibility experiment only. A local pass does not prove belt/pelvis removal, shoulder separation, pose correction or whole-body suitability.

## 7. Deliver, report and stop

Commit reviews/claude-rac-rm-ot-05q-gorrund-source-surface-patch-feasibility-gate.md and evidence under reviews/rac-rmot05q-evidence/. Supply the separate plan commit, result commit, source provenance, extraction details, clothing classification, selected patch rationale, actual method, untouched-region checks, local geometry checks, image comparisons, limitations, replay commands and SHA-256 manifest. Use repo-relative commands/configured source inputs, not scratch-only paths. Preserve source master hashes and all earlier evidence.

If a source-derived file is too large for normal Git, use existing repository asset conventions and provide a verified accessible location/hash; do not claim a download exists when it does not. Deliver review images and a reproducible patch recipe regardless.

Then STOP for author visual review. Do not create a complete RD5 body, repair a second garment area, run a replicated blind gate, build LOW, derive scaffold, reconcile/freeze canon or start production transfer. The next whole-body route requires a separate author order after this local feasibility result.

Grask E3 FROZEN. Gorrund UNACCEPTED. RM-OT-05 OPEN. Stage C BLOCKED. D4, UE5, production rigging, creator implementation and canon promotion NOT STARTED/NOT PERFORMED. Retain approved leonine head/tail identity, existing plantigrade/body guardrails and the later 13,380-vertex production-contract validation requirement. No Rodin regeneration/credits, replacement source or unrelated RAC work.
