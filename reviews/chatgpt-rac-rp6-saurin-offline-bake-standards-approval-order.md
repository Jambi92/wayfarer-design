# ChatGPT Order — Saurin RP6 Offline Bake Standards Approval

Record the author's decisions below and close the standards review against the [offline bake validation report](claude-rac-rp6-saurin-offline-bake-validation-report.md) and evidence at `c74bbe5cb8c0767776f994e5668010622a844b0e`. Continue from the handoff at `bdde9d4434dfac3a81a1ce39c58d61dfbc621b42`. Offline per-body baking is the adopted Saurin RP6 workflow.

## 1. Approve the dense audit and standard recipe

Use the following standard for future bakes.

- Set `BAKE_PK_MINW=0.25`. In the existing solver this is the minimum half-width of a pose-key tent as a fraction of the pose's full angle. Record that convention explicitly in the recipe.
- Enable `BAKE_DENSE=1` with `DENSE_STEP=0.0025`. Audit every bake-affected anatomical pose and the heavy-joint risk set, retaining samples 0.25 degrees to either side of active baked and initialization-layer transitions within the supported range.
- Run all 34 anatomical poses and all 50 special-gate poses at 25%, 50%, 75%, and 100%, plus neutral, from the initial validation pass. Run the full anatomical sweep at 0.025 steps on the heavy-joint and bake-affected poses and 0.125 elsewhere. Sweep refitted special poses densely at 0.025, including their transitions.
- Feed failures from the gates, sweeps, dense audit, and provisional motion rule into the adaptive fit. Allow up to three adaptive refits per body, then report any remaining failure for review. Keep the existing fold, penetration, tear, volume, rigid-landmark, and integrity requirements and the established composition ownership evidence.
- Reopen the artifact from disk and rerun the complete applicable validation after a refit. Acceptance records must state the sampled motions and fractions, recipe and tool versions, exact body and rig inputs, and artifact hashes.

Put these settings in the normal entry point or a documented standard runner so ordinary callers use the approved recipe. Preserve an explicit way to reproduce the archived runs with their recorded settings. Verify the runner settings and affected behavior with checks appropriate to the change.

## 2. Provisionally approve the tail criterion

For the frozen Saurin tail topology, use the criterion implemented by `sa6_tail_criterion.py`. With the existing 181 rings and 11-junction window, measure the maximum deformation-added turning concentration relative to the same body's neutral tail.

| Result | Criterion |
|---|---|
| PASS | Concentration at most 2.0 degrees and ring-area retention at least 0.95 |
| REVIEW | Concentration above 2.0 and at most 2.5 degrees, with area retention at least 0.95. Require visual review of the centerline and shaded mesh in motion at the flagged frame. |
| FAIL | Concentration above 2.5 degrees or ring-area retention below 0.95 |

The raw 2.51 kink ratio remains a recorded diagnostic. A visible hard kink, root collapse, tearing, or inversion remains an open defect even when the concentration score passes. Review the worst baked tail cases and the calibration anchors, including the root crease near 2.12 degrees and the smooth distributed bend near 2.45 degrees. Record the visual conclusion. This provisional approval is scoped to the calibrated frozen Saurin tail and sampled motions.

## 3. Provisionally approve the local motion rule

Use the final local rule from `sa6_bake_motion.py`, comparing the same vertex and frame pair in the baked body and initialization layer. Each excursion is measured on the corrected surface relative to plain LBS.

```text
e_bake(f, g, v) <= max(0.50 cm, e_initialization(f, g, v) + 0.05 cm)
```

Keep the documented test speed of the full pose range in one second at 30 fps, with the 1/240 pose grid and driver-transition samples. Retain the original verdict and bake-only excursion as diagnostics.

Use this as a regression check together with visual playback of the worst cases before accepting a new body's bake. Record playback speed and the visual conclusion. The numerical rule inherits motion already present in the initialization layer and measures frame excursion. Claims about smooth acceleration or behavior at other speeds require corresponding evidence. Review the existing elbow slope break in playback and flag any visible problem for the author.

## 4. Retain the passing bakes

Retain the current BASE_c1 and BASE_c2 artifacts exactly as identified by hash in `offline_bake/SA_RP6_offline_bake_results_v001.json` at `c74bbe5`. Both already pass the final dense audit, local motion rule, full suites, and integrity checks. Their recorded one-eighth pose-key floor is an accepted existing-artifact exception to the future one-quarter recipe. Record that exception and reuse the passing evidence.

Keep END_FAHI and END_MUFAHI as the tested regression controls with their recorded recipes and results. The shipping-preset roster remains an author decision. This order designates no additional shipping bodies.

## 5. Record the decisions and stop

Update the RP6 interface and bake instructions, the applicable Saurin status or carry-forward records, and the Claude handoff to reflect these decisions and their scope. Preserve the original reports and measured verdicts as historical evidence. Record the retained base artifact hashes and the evidence supporting their acceptance.

Use existing evidence for closure. Complete the visual reviews above and perform any small reproduction or playback check needed to substantiate the record. Tyler's PC authorization continues for those checks. A new defect should be reported with its exact body, pose, angle, evidence, and proposed correction for review.

Commit the standards updates and a concise closure report to `main`, cite the final evidence commit in the handoff, and **stop for ChatGPT and author review**. Keep the package status **RP6 RIG PILOT / NOT FROZEN**. Further bake batches, elbow-family changes, shipping-preset designation, production freeze, creator or runtime integration, UVs, materials, LODs, PD-1/PD-2 implementation, UE5 integration, and other-race work require a separate order.
