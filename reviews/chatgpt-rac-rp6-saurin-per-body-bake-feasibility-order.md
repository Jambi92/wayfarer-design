# ChatGPT Order — Saurin RP6 Per-Body Bake Feasibility

Run a bounded feasibility test of fitting and baking RP6 correctives for each finalized Saurin body. Continue from the [corrective layer validation report](claude-rac-rp6-saurin-corrective-layer-validation-report.md) at `0caf097445b948a83af2b4d6dec96061e0ed42b4` and the [previous validation order](chatgpt-rac-rp6-saurin-corrective-layer-validation-order.md).

The RP6 pilot acceptance for the previously tested cases stands. Continuous corrective-layer blending remains unapproved. Use the packaged blend as the initial fit for this experiment, then solve and verify the corrective set on the exact test body. Keep the package status **RP6 RIG PILOT / NOT FROZEN**.

## 1. Select and record the test bodies

- Reproduce the intermediate failures from the [committed evaluation and scan evidence](rac-rp6-evidence/saurin/rig_pilot/layer_validation). Cover the held-out MUHI, FAHI, and MUFAHI full-suite failures at weights 0.375 and 0.625, MUFAHI at 0.0625, the high-weight FAHI and MUFAHI crease failures, and the T80 hip tear at 0.375. Include the intermediate M208-B and c2 F-N cases that failed in earlier revisions. Record the package revision that produced each failure and check the current packaged blend on the same inputs before fitting.
- Select additional held-out blends with at least two active state contributors, including a supported three-contributor blend. Choose weights that were absent from the earlier evaluation and fit sets. Fix the list and weights before fitting. Use accepted creator recipes or the documented body interpolation from the prior test. Record the exact body construction, weights, base configuration, body hash, and recipe version. Include both c1 and c2 in the benchmark.
- Stage inputs from the verified clean RP5 workspace or recreate it using the [closure provenance](rac-rp6-evidence/saurin/rig_pilot/SA_RP6_clean_workspace_provenance_v001.json). Keep the original inputs read-only. Verify dense correspondence and frozen embedding. Recompute joints on the exact body, carry over its base weights, and preserve frozen RP5, accepted biological ranges, and the archived RP5-literal diagnostics.

## 2. Fit and verify from disk

Use the existing RP6 local solver and portable tools where applicable. For each body, record plain LBS, base correctives, and the packaged blend before fitting. Fit bounded, pose-driven correctives using the blend as initialization and save the result as a versioned artifact tied to the exact neutral body and base rig. Reopen and evaluate the baked artifact from disk. Confirm zero corrective displacement at neutral and preserve rest geometry, topology, semantics, and weight integrity.

Run all 34 anatomical poses at 25%, 50%, 75%, and 100% on every baked test body. Rerun the applicable special gates and check both sides of active driver transitions on the affected poses. Apply the existing RP6 thresholds for folds, penetration, tears, volume, and rigid landmarks. Recheck both base controls and the accepted endpoint cases with the validation tools used for submission. If an export or read-back path changes, rerun its Blender checks.

Keep pre-rig composition defects visible and use the established ownership rules. Compare each claimed residual with the exact same body and pose under LBS and before baking. Require zero topology-owned defects and zero unresolved rig-owned defects in the baked cases. Record failures, retries, the worst measured margins, and representative visual evidence.

## 3. Time the PC runs around the fighting-animation work

Prepare the scripts, input list, and run plan before requesting a PC window. **Start PC runs only when Tyler explicitly gives the go-ahead for a window clear of fighting-animation work.** Process lists, low utilization, and a momentarily idle Blender window are insufficient to establish availability. If Tyler needs the PC back, stop or checkpoint the bake promptly and wait for the next agreed window before resuming.

Use a separate RP6 scratch and output directory. Run a single body at a time, with one solver worker, numerical-library threads capped at one where supported, and below-normal process priority on Windows. Keep fighting-animation files, apps, and jobs out of the bake workflow. Start with one representative failing body to measure resource use before the rest of the batch.

For each PC run, record hardware, worker and thread settings, elapsed wall time for fit, write/read-back and gate evaluation, peak memory, retries, and total active turnaround. Record pauses and time spent waiting for the PC separately. Report the range and median of the measured bake times and which cases converged. Label any off-PC timings separately.

## 4. Submit and stop for review

Commit the benchmark method, commands, inputs and version hashes, per-body gate results, timings, representative evidence, and feasibility verdict to `main`. Update the Claude handoff with the evidence commit and the decision still needed. If any gate is open, identify the exact body, pose, fraction, and regression. If the PC timing is incomplete, report the remaining runs and the window needed. Stop after submission for ChatGPT and author review.

Scope is the Saurin RP6 benchmark. Creator or production bake integration, approval of continuous blending, a freeze, PD-2 solver work, PD-1 transport, UVs, materials, LODs, UE5 integration, and other-race work require a separate order.
