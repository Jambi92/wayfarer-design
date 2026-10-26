# RAC RP2 — Grask rig-preparation readiness and landmark review order

**Date:** 2026-10-25  
**Authority:** Tyler requested the next instructions through ChatGPT after review of the committed v003 freeze.  
**Parent:** freeze commit `59aacfe`; closure hash-record commit `59ffd1c`.  
**References:** `specs/RAC_PRODUCTION_MESH_CONTRACT.md`, especially §§4, 12, 16; `reviews/chatgpt-rac-retopology-rigprep-master-plan.md`; the v003 acceptance order and freeze report.

## 1. Author review and next authorized scope

The committed freeze report, manifest, read-back evidence and status update have been reviewed. Grask RP2 retopology remains **AUTHOR ACCEPTED / FROZEN / CLOSED**. This is not another retopology correction cycle.

Begin a **Grask-only rig-facing readiness review and landmark/axis proposal**. This is a preparation gate within the existing program, not commencement of RP6 or final rig production. Deliver evidence and a concrete diagnostic test proposal for ChatGPT review before any skeleton construction, weighting or posing.

The master plan still requires the remaining production-mesh phases before roster-wide RP6 validation. This order does not skip those phases or start another race.

## 2. Immutable parents

Accepted production file: `GR_U_REF_RP2_retopo_v003.blend`.

- SHA-256: `03bfe7d924ff5b8b61a4c10095af5d16ca29d41667d7f61d0abeca14e1f07ce0`.
- Geometry hash: `f9c4a7ac98e86d98017376b9d67c85428503d2d6385258471d99bc766bfe702f`.
- Frozen anatomical source: `GR_U_REF_RP2_SOURCE_3D_v005.blend`, SHA-256 `7bba8d2d5f081c077351b2e79e7e5fcce91b4f376cd6b2cfc76f1c2eb052ab14`.
- Source geometry: `2697929d90c9ed708997a594502a4d5edeaebb8f4ae39deefcc0802dc7c1d7bc`.

Verify these before and after inspection. Stop on a mismatch. Never save over either parent, its sidecars, landmarks or freeze manifest. Keep v001/v002 unchanged. The separate freeze record is authoritative over the historical candidate property inside the byte-identical blend.

Preserve accepted thumb-web anatomy, asymmetry, production origin, identity/deformation groups, seam proposal and the accepted ring–pinky quad exception. No geometry cleanup, re-projection, symmetry enforcement or v004 is authorized.

## 3. Audit the actual landmark package

Read the current frozen landmark package and classify every record by provenance: copied construction coordinate, independently measured surface landmark, fitted joint-centre estimate, or author-placed proposal. Do not count copied construction coordinates as independent measurements or assume surface markers are internal joint centres.

Review contract §12 coverage for root/pelvis, hips, knees, ankles, balls/toes, girdle, shoulders, elbows, wrists, MCP/IP joints, thumb CMC, spine, neck/head, jaw, eyes and ear roots. Mark each as usable, provisional, missing or not applicable, with a reason. A closed sculpted mouth or absent eyeballs must be reported, not repaired or populated with new anatomy.

For proposed joint centres and axes record:

- stable ID and left/right identity;
- position in both analysis centimetres and Blender metres, with the exact frame conversion and production translation;
- estimation method and the source geometry used;
- uncertainty and limitations; numerical fitting precision is not anatomical certainty;
- parent/child segment relationship and resulting length;
- orthonormal local axes, handedness and proposed flexion direction where supportable.

Fit proposals to accepted v005 anatomy and cross-check against v003. Do not blindly reuse the superseded MPFB Grask skeleton. Preserve documented asymmetry; assess sides separately. If an internal centre cannot be justified from available anatomy, label it provisional and show the alternatives rather than declaring it exact.

New data must be a separate versioned proposal, e.g. `GR_U_REF_RP2_rigprep_landmarks_v001.json`, never a replacement for frozen landmarks. Existing T-6 remains a surface-preservation check; it does not establish accuracy of newly inferred internal joint centres.

## 4. Visual review package

Provide actual inspectable images, not just paths or numerical claims:

- whole-body front, side, rear and three-quarter views with clearly labelled proposed centres and axes;
- unobstructed shoulder/girdle, pelvis/hip, elbow/knee and wrist/ankle closeups;
- both hands, thumb CMC and finger-joint proposals; both feet, MTP line and toe joints;
- head/neck/jaw views showing uncertainty and any missing internal anatomy.

Use neutral clay and a legible wireframe option. Distinguish existing measured markers from new estimates by a visible legend. Use identical cameras for source/production comparisons and disclose any display offset. Overlay geometry must live in a separate derived inspection scene if needed; no armature, weights, posing or mesh edits.

## 5. Diagnostic deformation proposal — plan only

Propose the smallest useful later diagnostic rig/test suite for Grask: shoulder elevation and axillary clearance, elbow flexion, wrist and finger bends, thumb opposition, hip/knee flexion, ankle/toe articulation, trunk twist and neck motion.

For each test specify proposed angles/poses, purpose, observed risk zones, evidence views and pass/fail measurements. These are technical test proposals, not canon range-of-motion limits. Distinguish deformation defects from intentional source hollows and contact anatomy. Do not invent creator ranges or biological constraints.

Describe how a later authorized diagnostic copy would preserve segment lengths and return to the reference stance within contract §4, using T-1 and T-6 as applicable. Do not run deformation tests in this order. Do not use this review to select a final game skeleton, UE5 compatibility policy or performance budget.

## 6. Required return and stop

Commit:

1. `reviews/claude-rac-rp2-grask-rigprep-readiness-gate.md` with coverage, methods, uncertainty, blockers and precise author decisions needed;
2. the separate proposed landmark/axis JSON and readable tables;
3. images and before/after parent hashes under `reviews/rac-rp2-evidence/grask_rigprep_readiness_v001/`;
4. reproducible inspection tools under `tools/rac/rp/` if new tools were needed;
5. a narrowly scoped status/handoff update: **retopology frozen; rigprep readiness proposal awaiting ChatGPT review**.

Report missing inputs candidly. Do not call this stage passed merely because files were created. Do not claim production rig readiness where internal landmarks or component requirements remain unresolved.

No final or diagnostic armature construction, skin weighting, posing, corrective deformation, creator morphs, UVs, materials, LODs, UE5 work or another race is authorized by this order.

After committing the readiness report and evidence, **STOP FOR CHATGPT REVIEW**. Return the commit hash and display the key visual sheets. A later execution order is required before building or testing any rig.
