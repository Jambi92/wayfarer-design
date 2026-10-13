# RAC RM-OT-05T — validate and release the direct-sculpt handoff; stop scripted morphology

**Authority:** Tyler-approved next order after review of racebodies_v123 / 05S.
**Date:** October 13, 2026 (America/Phoenix).
**Parent:** 05S order 27730589280494d8dee239a584a924f67a1b96e2 and reviews/claude-rac-rm-ot-05s-gorrund-direct-band-axilla-interface-gate.md.

## Author ruling

S3 remains UNRESOLVED and unaccepted. Its technical improvements do not overcome the visibly crinkled posterior fold. The author verified archive CRCs and all 211 packaged file hashes, with no missing/unlisted payloads; the author did not independently test the Blender scene or rerun geometry validation.

The useful next deliverable is the existing native Blender direct-edit handoff. Stop all new scripted morphology, designed-profile sweeps, interpolation/relaxation retries and automatic candidate generation. No S4 or complete RD5 body. This block validates the handoff and releases it for a real direct sculpt session; it does not manufacture a substitute sculpt.

## Validate the existing handoff

Inspect GO-05S_interface_handoff.blend using available Blender tooling. Verify working S3 geometry against its frozen OBJ, identity object transforms, numeric coordinates/units, face labels, edit groups, frozen boundary and source/B2 reference objects. Check that editable and frozen groups do not overlap ambiguously and that the posterior focus lies inside the authorized editable interface. Preserve original handoff and input hashes; record any necessary support-only fixes in a new release copy.

Vertex groups are selection aids, not automatic sculpt protection. Supply an explicit mask/isolation workflow that protects every outside vertex and the boundary. Verify mask generation numerically if using headless Blender; do not claim brushes or desktop UI were tested. Reference objects must remain selectable for inspection without becoming accidental edit targets.

Audit OBJ export settings and the exact-coordinate rematch method. Test an unchanged Blender import/export round trip through the actual recommended exporter, not just rematching the original S3 OBJ. Blender coordinate precision or triangulation may affect exact equality. Diagnose any failure and provide a controlled export/identity scheme rather than weakening protected-region checks or guessing correspondence. Retain the unchanged test as a TOOLING FIXTURE, never a sculpt candidate.

Run meaningful targeted protection tests on disposable copies: an allowed small interface displacement must be recognized; a moved protected vertex and a moved frozen-boundary vertex must be rejected; authorized local topology edits must preserve correspondence outside the interface. Confirm that boundary enforcement is checked independently if the existing V1 only checks original-source faces. Keep original validators and scores; any verification fixes must be additive, documented and tested. No tolerance relaxation or silent rounding/repair to conceal changes.

If a requirement cannot be verified, mark it pending or failed and explain the exact limitation. Do not call the release fully ready merely because a .blend file exists.

## Sculptor entry point and exact return contract

Create START_HERE.md with a short sequence: open scene; inspect source and S3; enable verified masks/isolation; confirm transforms/units; directly sculpt only the committed 05S interface; export with the verified procedure; run checks; return artifacts. Include clear posterior defect views and fixed-boundary overlays.

The direct sculpt task is unchanged: remove the posterior crinkled/notched strip and restore a credible arm-to-posterior-axillary-fold crease while retaining adjacent deltoid/triceps relief and a deliberate garment termination. Preserve the plausible anterior transition; refine only if necessary. All new skin stays INFERRED. No full ring, arm–trunk separation, shoulder/axilla rebuild, second garment region, pose/scale/limb change, global smoothing/remesh or projection of clothing detail.

Specify return files: edited native scene, whole working mesh OBJ, explicit edit/label maps if topology changed, identical-camera before/after anterior/posterior/underside/3/4/wireframe views, verification output and hashes. Keep source/S3 snapshots and actual edit log. A geometrically clean result still requires author visual acceptance.

Add a first-session desktop check: verify masks and export on a disposable fixture before touching the production working copy. Leave it PENDING unless a real interactive session completes it. Do not imply this order creates an interactive capability that is absent.

## Self-contained delivery and closure

Release a compact self-contained sculptor package with scene, F1/S3 references or embedded verified equivalents, frozen interface definition, masks/maps, START_HERE, brief, export/rematch/verification tools, targeted test evidence and dependency/version instructions. Do not duplicate all historical race evidence into another large archive; cite frozen provenance while including everything needed for this local edit and validation.

Use a package-specific manifest covering actual bytes/paths, keep repository manifests separate, verify CRCs/hashes and clean-extraction completeness/links, and test the release commands where supported. Record package location/size/hash and an actual usable download location or explicitly disclose its absence. No fabricated links or completed tests.

Commit reviews/claude-rac-rm-ot-05t-gorrund-direct-sculpt-handoff-validation-closure.md and evidence under reviews/rac-rmot05t-release/. Report exact changes, scene and export checks, protection tests, pending desktop checks, entry point, package hashes and the next direct sculpt action. Do not hire/contact anyone, install software or spend credits/costs.

Then STOP AWAITING DIRECT-SCULPT RETURN. Do not continue generating instructions or meshes as a substitute for that asset. When an actual edited asset arrives, verify it under the preserved technical/visual gates and return it for author review; no automatic expansion or promotion.

Gorrund UNACCEPTED; Grask E3 FROZEN; RM-OT-05 OPEN; Stage C BLOCKED; D4/UE5/production rigging/creator implementation NOT STARTED; canon promotion NOT PERFORMED. Source master base.glb remains unchanged, SHA-256 78ecfa87d169380ecb46ece3f0c0df3491d10e4547038a3c35c06df933f38a7b. Preserve beastfolk identity, existing plantigrade/body guardrails and later 13,380-vertex rig-contract validation. No new LOW, blind study, scaffold, canon rewrite, Rodin generation or unrelated RAC work.
