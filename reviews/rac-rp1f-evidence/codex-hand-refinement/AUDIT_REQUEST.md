# Wayfarer Gorrund hand-quality audit — HOLD

This package is a failure-analysis handoff, not a frozen or production-ready character.

## What Tyler approved

Keep the substantially larger claw direction shown in the separate finger/thumb studies and full-model review. Improve integration, retain the race bible's hand structure/dexterity and accepted scale, preserve the protected source and approved non-hand anatomy, and check relaxed hand, fist, precision pinch and weapon grip before freezing.

## What was completed

- Body and claw mesh audits, including a control run on the unchanged source.
- Several local geometric repairs, retaining the body vertex/quad counts and existing outer patch boundaries.
- A separate diagnostic armature and skinning trials for all four configurations.
- Full-precision connected-surface weights and an initial source-section joint fit.
- A fused-claw preflight against the production contract.

## Why this is a HOLD

The body still has added intersection flags relative to the source control. The right-hand slit/web region is especially sensitive. The best static trial improved the flags substantially, but no zero-crossing gate was achieved. A later source-web restoration trial made the count worse and was rejected. Do not treat the latest generated file as automatically better than the best static trial.

The diagnostic rig has visible deformation failures in the fist, pinch and handle-grip images. Its automatically fitted joint positions/weights are not production acceptance. A pinch IK target can remain out of reach; a reached handle target still does not establish collision-free contact.

The preview's separate claw objects also fail the component-ownership requirement in `specs/RAC_PRODUCTION_MESH_CONTRACT.md` §5. Fused conversion was only preflighted; two cap regions were too small to carry the broad roots without unsafe stretching. No fused production mesh was delivered.

## Audit requests for Claude

1. Reconcile the actual Blender triangle audit with the established quad-BVH intersection gate. Initial fixed-diagonal triangle counts overstate the actual-tessellation counts and are not directly interchangeable with prior gates. Reproduce the source control before classifying any source flag as a defect or accepted contact.
2. Locate the remaining right-hand slit/web crossings and propose a repair preserving the approved feature. Do not close or redesign that feature to make a count pass.
3. Review the cap mappings and root attachment. Preserve the approved claw silhouette while satisfying the fused-component rule; do not silently choose a separate-claw production architecture.
4. Replace/validate the diagnostic hand joints and weights against anatomical landmarks. Prove the four poses with mesh and contact checks, not only IK target errors.
5. Re-run T-6/T-7 and required production gates after a valid repair. No freeze or family propagation without author visual review.

## Files and limitations

`hand_geometry_review.npz` contains source-index-aligned, hand-only crops for the source control, best static trial and current failed-rig input. Crop boundaries are deliberate and are not production boundary defects. It is not the full character. `diagnostic_weights_NOT_ACCEPTED.npz` contains the test weights; `test_bones.json` records test bone heads/tails. The `.jpg` sheets show failures and are labelled accordingly. Detailed counts and the source hash are in `GATE_DECISION.json`.

The scripts are working diagnostics and expect the original local workspace layout and full-model inputs. They are not a portable production pipeline. The original visual candidate and protected source remain separate. The crop, scripts and weights contain raw model data: do not upload or transmit them without explicit permission for that destination.
