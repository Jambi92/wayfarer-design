# RAC RP2 — Grask diagnostic deformation failure isolation order

**Date:** 2026-10-26  
**Authority:** Tyler requested these follow-up orders through ChatGPT after review of Claude's diagnostic return.  
**Return reviewed:** `2a0df3c`, `reviews/claude-rac-rp2-grask-rig-landmark-adjudication-diagnostic-gate.md`.  
**Prior execution authority:** `bf7d664`, rig-landmark adjudication and diagnostic-rig order.

## 1. Author ruling

The diagnostic cycle is received as useful evidence, not a production deformation acceptance. The retained criteria passed in 20/43 poses. Failures remain failures; do not relabel them as passing because they occur near a crease or because DQS preserves volume.

The evidence supports a substantial contribution from diagnostic weights and skinning method. It does **not** establish that topology can be excluded as a contributor. Replace categorical claims that the failures are not topology with this qualified conclusion in the new report. Preserve the original report as history.

Grask retopology remains **AUTHOR ACCEPTED / FROZEN / CLOSED**. This order authorizes one bounded follow-up cycle on new diagnostic copies: resolve knee-placement compliance, improve diagnostic weights locally, compare joint placements under controlled conditions, and map remaining failures. It does not authorize a retopology revision or production rigging.

## 2. Immutable parents and versioning

Verify before and after:

- `GR_U_REF_RP2_retopo_v003.blend`: SHA-256 `03bfe7d924ff5b8b61a4c10095af5d16ca29d41667d7f61d0abeca14e1f07ce0`; geometry `f9c4a7ac98e86d98017376b9d67c85428503d2d6385258471d99bc766bfe702f`.
- `GR_U_REF_RP2_SOURCE_3D_v005.blend`: SHA-256 `7bba8d2d5f081c077351b2e79e7e5fcce91b4f376cd6b2cfc76f1c2eb052ab14`; geometry `2697929d90c9ed708997a594502a4d5edeaebb8f4ae39deefcc0802dc7c1d7bc`.

Stop on mismatch. Preserve v001/v002 provenance, all frozen sidecars/landmarks, the freeze record, loop tags, seam proposal, accepted thumb-web anatomy and accepted quad exception. Do not resave or overwrite any frozen parent or diagnostic v001 evidence.

New outputs: `GR_U_REF_RP2_rigdiag_v002.blend`, separate versioned landmark/weight records and manifests. Any rest mesh in a new diagnostic file must match frozen v003 geometry exactly. No geometry edits, rest-shape adjustments, corrective shapes or helper deformation bones in this cycle; those would confound the isolation experiment.

## 3. Resolve AD-R2 explicitly

The previous order's maximum 5 mm knee fitting adjustment applies to the complete displacement from the v001 consensus target, not only vertical level. The reported 5.8/7.8 mm AP/ML displacement is not approved as compliant.

Create `GR_U_REF_RP2_rigprep_landmarks_v003.json` as a diagnostic revision. For each knee, preserve the specified level and place AP/ML as close as possible to the local section centre within a total 5 mm displacement from the exact v001 consensus coordinate. Report the original coordinate, unrestricted section centroid, chosen coordinate, displacement vector/norm and residual distance to the section centre.

Keep the former unrestricted v002 knee as a labelled comparison only. Do not silently change its provenance or call it approved. If the two requirements cannot both be met, state that conflict; the bounded point is an experimental candidate pending review, not a claim that the section-centre requirement has been fully met. Apply the same displacement audit to all explicitly bounded placements, reporting any other exceedance rather than hiding it.

This is the one authorized landmark revision for this order. Do not iterate through further landmark versions without returning for review.

## 4. Controlled comparisons

Retain the v001 rig/weights as the reproducible baseline. Separate variables:

1. baseline pivots and baseline weights;
2. same pivots with locally improved diagnostic weights;
3. alternate pivots with the identical improved weight array;
4. LBS versus DQS with identical pivots, weights and poses.

Log precise pose transforms, affected vertex IDs, weight-array hashes and bone matrices. Compare changed centres using the same local angle definitions and also disclose resulting world-space limb orientation/endpoints; equivalent named angles must not hide different motion.

For shoulders retain v002 GH as the baseline, with the old E3 alternative as a comparison, not an adopted replacement. Include pure-GH and girdle-assisted elevation as separately labelled tests. Girdle participation is appropriate to test, but a fixed 20-degree split is not accepted as final scapulohumeral mechanics or biology canon. Document what actually moves, including scapular-proxy participation.

For hips retain v002 as baseline. The previously reported inguinal-axis alternative may be evaluated at its existing coordinates as a sensitivity comparison only; it is not approved as the new centre. Include flexion and abduction on both sides so an improvement in one pose cannot conceal regression in another. Do not search indefinitely for a pivot that minimizes one metric.

For knees compare bounded v003 and unrestricted v002 using the same weights and poses. Surface appearance alone does not establish internal anatomical joint-centre accuracy.

## 5. Local diagnostic weight work

Authorize a limited, logged weight cleanup in derived files for shoulders/axilla, elbows, hips/groin, knees, wrists and hands/thumb. Normalize weights, remove unintended cross-region leakage and use smooth joint transitions while preserving intended segment influence. Bind nail-region vertices to the appropriate distal digit segment for the rigidity test; document the selection and transition boundary.

This is diagnostic weight authoring, not a production skin-weight deliverable. Do not alter geometry to make weights work. Do not change skeleton architecture while comparing weights. Explain the method, regions changed and expected effect, and retain before/after maps.

Use at most two logged weight candidates beyond the baseline. Select and justify the best-supported candidate, then rerun the complete original 43-pose suite with it to detect regressions. Include representative DQS comparisons for the difficult poses; do not claim the full suite passes in DQS unless it was actually evaluated. No UE5 skinning policy is selected here.

## 6. Validate measurements and localize failures

Retain the previous diagnostic thresholds. Report all original metrics and pass/fail results, including intersections, crease depth, folds, orientation failures, zone volume, p95 strain, loop spacing and nail rigidity.

Add diagnostic overlays with exact face/vertex IDs for intersections, folds, orientation failures and compressed loops. Show neutral clay and wireframe for shoulders, elbow, hip/groin, knee and thumb/fist, including both sides where tested. Compare baseline and improved candidates with identical cameras and disclosed display offsets.

Audit the meaning of the metrics:

- Distinguish a face normal opposed to a skinned reference normal from a demonstrated local surface inversion. If the existing flip test measures the former, label it accurately, retain its results and supplement it with geometric evidence before drawing conclusions.
- Explain how intersection depth and contact labels are calculated; show representative pairs rather than relying on aggregate counts.
- Explain the zone-volume estimator, how its patch boundary/cap is handled and how it behaves under rigid motion. If it is an open-patch cone-volume proxy, call it that; do not equate it to anatomical tissue volume. Include a rigid-transform sanity check and retain historical numbers for comparison.
- Validate crease/contact masks against actual geometry. Declare forearm–upper-arm proximity at deep flexion as a candidate expected contact region, not an exemption for penetration or inversions. Preserve original classifications alongside any justified reclassification; no threshold relaxation or enlarged masks just to obtain a pass.

Do not infer that improved volume alone resolves deformation. In particular, the previous DQS hip result introduced folds outside the crease and remains a failure.

## 7. Decision logic

Classify each remaining failure with evidence and confidence: measurement/test setup, placement sensitivity, weights, skinning method, expected contact, possible topology limitation, or unresolved combination.

An improvement after changing weights or skinning demonstrates contribution, not exclusive causation. If reasonable diagnostic weights and plausible pivots still leave a localized problem, identify the implicated loops and mechanism and stop for review. Do not reopen the frozen mesh or assert that corrective shapes are necessarily sufficient without testing.

Facial/oral component work remains deferred and separate. Do not combine jaw/eye geometry authoring with this body diagnostic investigation.

## 8. Required return and stop

Commit `reviews/claude-rac-rp2-grask-diagnostic-deformation-failure-isolation-gate.md` and evidence under `reviews/rac-rp2-evidence/grask_rig_diagnostic_v002/`, including:

- parent hashes before/after, new file hashes and read-back rest-geometry verification;
- v003 landmark proposal and full displacement compliance table;
- reproducible baseline/candidate definitions, weight edit logs/maps and comparison matrices;
- full-suite before/after results with regressions highlighted;
- metric validation, failure overlays and actual inspectable visual sheets;
- qualified conclusions and precise unresolved author decisions;
- narrowly scoped STATUS/handoff update: **retopology frozen; diagnostic deformation follow-up awaiting review**.

Execute one bounded follow-up cycle and return even if failures remain. Do not perform an open-ended correction campaign.

No production skeleton, production weights, corrective-shape authoring, creator morphs, facial/oral geometry, UV/material/LOD work, UE5 integration or another race is authorized.

After committing the report and evidence, **STOP FOR CHATGPT REVIEW**. Return the commit hash and display the key before/after images. Do not mark production deformation accepted or freeze a diagnostic candidate as final.
