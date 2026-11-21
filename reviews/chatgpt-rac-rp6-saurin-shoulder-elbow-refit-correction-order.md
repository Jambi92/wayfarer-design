# ChatGPT Order — Saurin RP6 Shoulder, Elbow, and Refit Corrections

Fix the shoulder deformation, add elbow muscle response, and resolve the refit convergence issue recorded in the [standards closure](claude-rac-rp6-saurin-offline-bake-standards-closure.md) at `a993a7857537783ec82c20cf688bf31ae740a4fd`. Run the revised RP6 validation on Tyler's PC, commit the evidence, and stop for review.

This authorizes revisions to the Saurin RP6 joint placement, girdle motion, weights, affected pose definitions, and bounded correctives needed for these corrections. Create versioned replacements for affected rig and bake artifacts. Keep the accepted artifacts and reports as comparison baselines. Use frozen RP5 geometry, topology, semantic order, embedding, and accepted biology as immutable inputs.

## 1. Correct shoulder abduction

Close `SAURIN-RP6-DEF-SHOULDER-1` on both sides and both base configurations.

- Reproduce the reported low upper-arm/armpit bend in whole-body playback. Check the humeral pivot against the accepted landmarks and source geometry, including its relationship to the shoulder cap. Correct joint placement where the evidence supports it and record the coordinates and reason.
- Add anatomically defensible shoulder-girdle participation through the existing clavicle/shoulder architecture. The closure's approximate 2:1 glenohumeral-to-girdle proposal is a starting hypothesis to test against Saurin anatomy and playback. Document the resulting coupling and ensure it evaluates consistently in the rig, external evaluator, and packaged file.
- Reweight the deltoid, shoulder cap, and axillary transition, then refit the affected correctives. The cap must rise and rotate with the arm, with the bend centered at the shoulder joint and the axillary vault preserved. Verify abduction, flexion, return to rest, and the existing combined or special poses that exercise the revised shoulder.
- Preserve the intended total arm motion and established endpoint severity. Record total arm angle relative to the trunk as well as the humeral and girdle contributions so adding girdle motion does not accidentally change the target angle. Keep the historical RP5-literal definitions and the previous production definitions as explicit comparison records.

## 2. Add elbow muscle response

Close `SAURIN-RP6-DEF-ELBOW-MUSCLE-1` with elbow-angle-driven shapes for both arms, c1 and c2.

- Add a visible, anatomically supported shortening and bulging response of the biceps/brachialis region during flexion, with corresponding triceps lengthening and flattening and a smooth return during extension. Use the accepted Saurin anatomy and local tissue geometry to establish shape and amplitude.
- Keep the shapes local, bounded, volume-aware, and exactly zero at the frozen neutral reference. Record each driver, activation range, displacement, and affected region. Preserve rigid landmarks and the existing hand, shoulder, and elbow crease behavior through the supported range.
- Validate the response at partial angles as well as 90 and 130 degrees. Show it on both base configurations and the heavy-body regression controls, where visibility may differ with the accepted tissue composition. Include motion with the corrected shoulder so the two systems work together.

## 3. Resolve convergence through the normal bake entry point

Fix the unresolved motion-feedback case recorded under `standards_review/motion_feedback_test/`, where widening the shoulder pose keys cleared the motion failure but left 1–3 tears. Reproduce the failure from its recorded input and settings. Diagnose the coarse widening step and the interaction between motion smoothness, contact, folds, and tears. Include the recorded neighbouring-contact-sample oscillation in the regression checks.

Use the existing solver and failure feedback where possible. A controlled widening schedule or a pose refit from the initialization layer with a wider floor is authorized if it solves the problem. Record the chosen behavior, convergence, and iteration history. Exercise the full automatic loop through `sa6_bake_full.py` and the standard runner, including save, reopen, evaluation, motion, dense audit, and refit. The evidence must demonstrate closure of all applicable gates together.

Keep the approved limit of three adaptive refits per body and all numerical thresholds. Report any remaining failure with its body, pose, fraction, iteration, and solver diagnosis after that limit. Record restarted fits and their reasons so the convergence claim is reproducible.

## 4. Rebuild and rerun RP6 validation on the PC

Tyler authorizes using his PC for this work. Use independent body workers or pose shards within its capacity, checkpoint each stage, and record tool hashes, worker settings, wall time, peak memory, and interruptions. Verify the deployed PC tools against the committed versions before running. Identify and report any stage performed off-PC separately.

- Rebuild both base configurations and rebake BASE_c1, BASE_c2, END_FAHI, and END_MUFAHI against the revised rig and corrective data. These are the current base and regression roster. Record the dependency versions so each bake matches the exact skeleton, weights, driver definitions, and initialization layer it uses.
- Apply the approved [standard recipe](../tools/rac/rp/saurin_rp6_v001/BAKE_STANDARD.md), including `BAKE_PK_MINW=0.25` as the pose-key minimum half-width fraction, `BAKE_DENSE=1`, and `DENSE_STEP=0.0025`. Run all 34 anatomical poses and all 50 special gates at 25%, 50%, 75%, and 100%, plus neutral; the full sweep; dense audits of affected and heavy-joint poses; transition samples; and dense sweeps of refitted special poses.
- Apply the provisional local motion rule at the documented playback speed and the provisional tail criterion with required visual review. Retain the ownership comparisons and existing fold, penetration, tear, volume, rigid-landmark, weight-leakage, and neutral-integrity requirements. Check the accepted hip behavior and other unaffected systems for regressions.
- Rerun the established 19-state PD-2 check with the revised rig assumptions and report ownership for every state. Recheck affected held-out intermediate and mixed-body cases from the earlier bake benchmark. Any newly fitted per-body artifact submitted as passing must complete the same standard validation. Record the evaluated body set and limits.
- Rebuild the portable rig/weights/correctives and Blender packages as needed for the revised data. Reopen both base Blender builds in fresh processes, compare neutral to frozen RP5, and verify joint transforms, weights, drivers, corrective values at rest, and posed geometry against the external evaluator. Rehash frozen sources before and after. Verify the new manifest and artifact dependencies.

## 5. Submit visual evidence and stop for review

Produce matched before/after whole-body front, side, and useful rear views for shoulder abduction and flexion, and clear elbow muscle close-ups. Include real-time forward/reverse playback at the documented speed, slower copies, and stills at key angles for both configurations. Provide the combined shoulder/elbow examples and the worst heavy-body cases. Record whether the arm now rotates at the correct joint and whether the muscle response reads naturally, alongside the numerical verdicts.

Commit the revised artifacts, reproducible commands, gate results, convergence regression evidence, timings, manifest, and correction report to `main`. Update the RP6 interface, bake instructions, carry-forward register, and Claude handoff with the exact evidence commit and the status of both visual defects and solver follow-ups.

Work through ordinary in-scope corrections internally. At completion, report each requested correction as closed or identify the exact unresolved issue. **Stop for ChatGPT and author review.** Keep **RP6 RIG PILOT / NOT FROZEN** through review. Shipping-preset designation, a production freeze, creator/runtime integration, muscle systems at other joints, UVs, materials, LODs, PD-1/PD-2 implementation, UE5 integration, and other-race work require a separate order.
