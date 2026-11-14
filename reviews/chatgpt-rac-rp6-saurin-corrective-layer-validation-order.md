# ChatGPT Order — Saurin RP6 Corrective Layer Validation

## RP6 pilot decision

The Saurin RP6 pilot **PASS is accepted for the cases tested** in the [validation closure report](claude-rac-rp6-saurin-validation-closure-report.md) at `c7e3151bb1973b14175ca4a9f3d875b6f3c461a3`. This includes both base configurations and the 19 accepted PD-2 states at the 34 tested full-angle poses with their fitted state correctives. Keep the package status **RP6 RIG PILOT / NOT FROZEN**. Approval of the proposed creator-state corrective layer for use between states is pending this review.

Continue on `main` from the accepted evidence. Use the [closure order](chatgpt-rac-rp6-saurin-validation-closure-order.md), the [PD-2 interface](rac-rp6-evidence/saurin/rig_pilot/SA_RP6_PD1_PD2_interfaces_v001.md), and the [committed deformation audit](rac-rp6-evidence/saurin/rig_pilot/SA_RP6_deformation_audit_v001.json) as the baseline.

## Validate the packaged layer

1. Load the committed `SA_RP6_creator_layers_v001.json/.npz` and the matching c1 and c2 base corrective data. Verify the inputs against the manifest. Recover the verified clean RP5 workspace using the closure provenance if needed. Reconstruct and evaluate the layers from the package on disk. Compare the reconstructed full-angle endpoint results with the closure audit and prove that neutral produces exactly zero corrective displacement. Verify the base-only case at zero state influence and the fitted state at unit influence. Use each state's documented base configuration, including c2 for F-N.
2. Implement the proposed blend in the validation harness. Evaluate each contributing layer at the actual pose on the blended body's joint frames, then use the same convex weights that produce the test body. Blend offsets relative to the matching base corrective and apply the resulting rest-space correction before LBS. The package stores changed keys as full replacement arrays. Account for the base contribution exactly once, including where sparse vertex supports differ, where keys are inherited, and where a state adds its own keys or driver samples. Document how the harness handles these cases and show the endpoint and neutral identities numerically.
3. Keep the accepted RP5 geometry, topology, source hashes, biological ranges, and historical RP5-literal diagnostics intact. Use the joint-centered anatomical suite for the production checks.

## Sample the pose and blend ranges together

| Coverage | Required run |
|---|---|
| Accepted states | Run all 34 anatomical poses on each of the 19 states at 25%, 50%, 75%, and 100% of the defined angles. Check neutral independently on every state. |
| Intermediate creator blends | For each selected blend path, test creator weights at 25%, 50%, and 75%, with the endpoints as controls. Run the same 34 poses at 25%, 50%, 75%, and 100% on those bodies. Include a valid mixed case with more than two contributors if supported by the proposed interface. |
| Driver transitions | On the most demanding cases, sample either side of active corrective key and pose-driver transitions and inspect a forward and return sweep through the pose range. Include any discontinuity the regular samples miss. |

Choose and document blend paths from the accepted creator ranges. Cover c1 and c2 within their respective bases. Include heavy muscle, heavy fat, combined muscle and fat, narrow and broad builds, and representative proportions that change joint or tail placement. Include base-to-extreme paths and valid between-state paths with two active corrective layers. Exercise the c2 F-N path within the available c2 evidence. Choose the exact supported paths from the approved recipes, and record the creator parameters, contributing states, weights, and any coverage limits. Build each intermediate neutral using the approved creator diagnostics or the documented body interpolation for the proposed interface. State which geometry method was used. Derive joints on that body, and compare plain LBS, base correctives alone, and base plus blended layers on the same body and pose.

## Gate and return for review

- Apply the existing RP6 fold, new penetration, tear, volume, and applicable special-pose gates without relaxing thresholds. Check for jumps or spikes in deformation as either angle or creator weight crosses a driver boundary. Include close-up evidence for the worst cases, with attention to the hand, shoulder, elbow, hip, knee, foot, jaw, and tail root where the tests exercise them.
- Measure pre-rig folds and neutral cage condition for every intermediate body. Use the closure ownership rules and compare against the same pose under plain LBS and with the base correctives. Show the evidence for any residual attributed to PD-2 composition. The gate requires zero topology-owned defects and zero unresolved rig-owned defects with the layer applied throughout the sampled cases. Record existing composition-owned residuals and coverage limits explicitly.
- Resolve ordinary evaluator, packaging, and bounded RP6 corrective-layer issues within this order. For any layer revision, version the evidence, record the changes, and repeat the coverage above, including the accepted endpoint and base controls. Recheck package hashes and prove repeatability from the submitted files. Escalate an unresolved defect, unsupported blend rule, or tradeoff that needs an author decision.
- Commit the validation method, sampled weights and pose fractions, per-case results, worst-case evidence, reproduction commands, and report on `main`. Update the Claude handoff with the evidence commit and verdict. If the checks pass, submit **SAURIN RP6 CORRECTIVE LAYER VALIDATION PASS — READY FOR CHATGPT / AUTHOR REVIEW** and stop. If any gate remains open, report the affected states, weights, angles, and evidence for review.

This order authorizes Saurin RP6 validation and bounded corrective-layer work through the review gate. Corrective layer approval remains with ChatGPT and the author. No freeze, UVs, materials, LODs, creator implementation, PD-2 solver work, PD-1 transport, UE5 integration, or other-race work.
