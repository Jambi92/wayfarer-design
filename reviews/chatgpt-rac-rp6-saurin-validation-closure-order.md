# ChatGPT Order — Saurin RP6 Validation Closure

Continue the Saurin RP6 production rig and skin-weighting pilot under the [original order](chatgpt-rac-rp6-saurin-production-rig-skin-weighting-pilot-order.md) (`a40701536aeac85798f1a3d097a19eb54e35aaac`). Resume from the [Claude pilot report](claude-rac-rp6-saurin-rig-pilot-report.md) and evidence at `7242ed391104e95fd9fdd07a704fe79e3bb7eb11`. The formal submission is held on two required checks that share one external input dependency. Recover the clean RP5 workspace, close the PD-2 and dense-source checks, and rebuild and verify the RP6 submission package.

## 1. Recover the approved inputs

- Attach `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/` to the Claude session and stage approved inputs into scratch with read-only access to the originals. The five W2I6 files in `RaceBodies/out/` were checked against the [RP5 source integrity record](rac-rp5-evidence/saurin/SAURIN_RP5_source_integrity.json) when this order was written. Recheck their hashes after staging.
- Recover `work/SA_RP5_WORK_v001.npz`, `src/saurin_w2_final_base.npz`, and all 19 `cr_<STATE>.npy` arrays at the root of `SA_W`. Use the exact state names and SHA-256 values in `clean_workspace.files` in the [RP5 consolidation rebuild record](rac-rp5-evidence/saurin/full_cage/final_consolidation/consolidation_rebuild.json). Verify dense c1/c2 correspondence, canonical face ordering, and frozen embedding reproduction before running either check. Record the staged hashes and provenance in RP6 evidence. Keep the dense arrays and other workspace binaries out of Git.
- If a verified copy of the clean workspace is unavailable, reproduce it in scratch via `tools/rac/rp/saurin_rp5_v002/sa_consolidate.py APPROVED.npz CLEAN_WORKSPACE SCRATCH_OUTPUT` and the [RP5 final consolidation report](claude-rac-rp5-saurin-final-consolidation-report.md). Use `SA_RP5_full_cage_optionb_final.npz` from the `full_cage/optionb_final/` evidence tree at approved commit `2ee75ae1845a223f3c8b8b9a5abfa10608f06b27` as the recipe input. Stage the canonical sources and accepted creator arrays where the recipe expects them. When the arrays must be regenerated, use the existing RP5 body and head builders (`cr_build.py`, `cr_build2.py`, `cr_head.py`), the approved W2/W3B inputs and recipes, and the [session handoff](claude-session-handoff.md). Reproduce the accepted inputs and compare to the recorded hashes. Resolve any archive serialization difference by proving exact equality of the underlying arrays against verified reference data. Unresolved input differences block submission.
- Hash the complete frozen RP5 set before and after the work against the [freeze record](rac-rp5-evidence/saurin/full_cage/final_consolidation/SAURIN_RP5_FREEZE.json) and the pilot's starting hash list. Keep the RP5 production copy and canonical sources read-only. Preserve the frozen geometry, face and vertex order, semantics, barycentric data, accepted tail module, and accepted residuals. Run all rebuilds in scratch.

## 2. Close the two pending checks

Use the production weights and corrective data from `7242ed3` as the starting point. Point `SA_W` at the verified clean workspace. The commands below use the work-file names from the pilot handoff and run from the RP6 work directory with `RP6_TOOLS` pointing to `tools/rac/rp/saurin_rp6_v001/`.

```sh
unset POSES
python3 "$RP6_TOOLS/sa6_pd2.py" pd2.json W_M.npz CF_M.json
python3 "$RP6_TOOLS/sa6_eval.py" M W_M.npz CF_M.json ev_M.json
python3 "$RP6_TOOLS/sa6_eval.py" F W_F.npz CF_F.json ev_F.json
```

**PD-2 (§18).** Check that the output contains exactly the 19 accepted states and the full anatomical 34-pose suite for each state at full angle under the documented RP6 creator-state assumptions. Reconcile the pre-rig dense folds and neutral cage results with the [RP5 ownership audit](rac-rp5-evidence/saurin/full_cage/final_consolidation/validation/SA_PD2_ownership.json). Report pre-rig source and neutral cage results, posed residuals by owner, and regressions against c1. Inspect the known extremes, including high fat, high muscle, muscle plus fat, and the accepted narrow variants. Show which posed residuals are attributable to the pre-rig composition and support that attribution numerically and visually. Proximity to an existing fold is a screening signal. Investigate new or worsened defects before assigning ownership. Require zero cage/topology-owned defects and zero new rig-owned defects. Preserve the accepted ranges and document the clean input and retest requirements for the future composition solver.

**Dense-source ownership (§11).** Require `dense_source_staged: true` in both outputs and verify the actual source measurements and topology co-location results. Run the complete c1 and c2 suites at 25%, 50%, 75%, and 100% of the angles, including literal variants and special gates. Preserve the four-step comparison of dense source, RP5 scaffold, RP6 production weights, and RP6 weights with correctives. Use the historical scaffold baseline only where the configuration and definition match, and label the coverage explicitly. Record the source fold rates and smooth-map co-location counts where the test applies, and reconcile them with the ownership classifications. Cage-only results, missing dense measurements, and unexamined topology-only flips leave this check open.

## 3. Keep historical poses comparable

Preserve the archived RP5 definitions and evidence, including the original names, axes, signs, amplitudes, and pivots. Identify any retargeting in the RP6 audit. Record the RP5-literal diagnostic separately wherever it differs from the production motion. Use the anatomical sign convention in the RP6 frame (+Y anterior) and rotations centered on the applicable RP6 joints for the production gate. Document the two interpretations together in the pose definitions and audit, including the reason for each difference. Preserve the requested motion range.

- Keep `jaw_open_20_rp5lit` as the historical closure/contact diagnostic. In the RP6 frame the literal sign drives the lower jaw into the closed upper mouth. Gate the anatomical jaw opening and jaw/head combinations.
- Keep `tail_root_lateral_30_rp5lit`, `tail_root_vertical_25_rp5lit`, and `tail_twist_30_rp5lit` with their historical off-joint pivot. Report the measured offset and the translation it introduces. Gate the production variants about the `tail_01` joint at the same axes and angles.
- Retain measured results for these four diagnostics with their established contact/setup or non-realisable classification and corresponding evidence. Any additional exception or ownership change requires evidence and review before PASS.

## 4. Rebuild, verify, and submit

- Resolve ordinary RP6 rig, weighting, or bounded corrective regressions within the original authorization. Keep the existing gates and thresholds. If a rig artifact changes, regenerate the affected outputs, re-export both configuration builds as applicable, and rerun the full gate set against the resulting package.
- Rebuild the evidence package with `sa6_package.py WORKDIR` using fresh PD-2 and dense audit outputs. Refresh the summary, manifest, and provenance. Include both configurations' weights, correctives, pose definitions, ownership results, and Blender read-back. Record the tool versions, commands, input hashes, and evidence locations. Verify the manifest's hashes and byte counts, including the compressed Blender containers and the decompressed binaries.
- Reopen both packaged Blender files in fresh processes and verify neutral against the frozen RP5 references within the established float32 tolerance, rig and corrective data against the audited package, and posed evaluation against the external evaluator. Check that correctives are zero at rest and the files are self-contained. Rerun the weight and corrective audits, reference/rig-prep/reference round trip, and all special gates.
- Before submission confirm zero topology-classified poses, zero topology-only flips, zero unresolved rig/weighting-owned folds or inversions after correctives, and zero new rig-owned penetrations or tears in the gated production poses. Confirm the hand, shoulder, hip, tail, foot/toe, and jaw/head gates on c1 and c2, both pending checks, fresh Blender read-back, and frozen-source integrity. Preserve the documented PD-1 and PD-2 interfaces.
- Commit the verified RP6 evidence and closure report on `main` and update the Claude handoff with the evidence location, input provenance, counts, gate verdicts, and final evidence commit. Keep the package status **RP6 RIG PILOT / NOT FROZEN**. If a genuine external blocker or author decision remains, report the precise missing input, access, or failing gate and the evidence needed to resume. Withhold PASS until every gate is clean.

Submit the following line only after verification, then stop for review.

**SAURIN RP6 PRODUCTION RIG / SKIN-WEIGHTING PILOT PASS — READY FOR CHATGPT / AUTHOR REVIEW**

Scope ends at the Saurin RP6 review gate. No UVs, materials, LODs, creator implementation or PD-2 solver work, PD-1 transport implementation, UE5 integration, universal skeleton declaration, or other-race work.
