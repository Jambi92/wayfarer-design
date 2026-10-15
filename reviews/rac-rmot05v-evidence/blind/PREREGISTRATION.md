# RM-OT-05V neutralized structural-readability gate: pre-registration (written before any scoring)

**Candidate:** the neutral ARM candidate GO-ARM-N1 (final chain state), under the fixed key name `GO-S-ref`.

## Protocol

The 05O protocol (`reviews/rac-rmot05o-evidence/blind/PREREGISTRATION.md`) is carried unchanged except where stated.

**Controls.** The same 10 frozen controls are used: Marchfolk and Skarn × ref / Narrow / Broad / low, plus Grask E3 ref and low. Their cached headless front and profile tiles come from the 05O run-1 cache (tag `K05a_GO-RD3`); they are byte-identical inputs to 05O.

**Candidate rendering:**
- Body only. Head and neck are removed at the source-lineage neck root, z 191 (the 05N cut).
- The tail is not shown.
- Height-normalized, front + profile, neutral grey and black silhouette.
- The original control renderer (a scratch tool) no longer exists, so the candidate tiles are rendered with Blender Workbench, studio light, single grey, orthographic, at the same 750 px tile size. The shading may differ slightly from the control tiles; this is disclosed.

**Runs.** Two independent runs with new seeds (sets V and W). Each run uses 3 fresh, uninformed scorers who see only the two sheet images. The keys are kept and never shown.

**Prompt.** `tools/rac/w1/rmot05o_drivers/o_scorer_prompt_05O.md`, unchanged except that the code range reads {P}01–{P}11.

## Rules (fixed now; not changed after results)

These are evaluated per run over the 3 scorers for `GO-S-ref`.

| # | Rule |
|---|---|
| C2 | ≥ 2/3 scorers neither group a Marchfolk code with GO-S-ref nor give it class A |
| C3 | ≥ 2/3 scorers do not group SK-brd with GO-S-ref |
| C4 | ≥ 2/3 scorers place both Grask E3 codes outside the GO-S-ref group |
| C5-REF | ≥ 2/3 scorers give **all** of: `primary_driver` ∈ {axial_section_shape, joint_integration, segment_relations, load_path}; `posture_pose`, `fat`, `muscularity` and `boxiness` each none or minor; `posture_read` false |

**Not evaluable: C1 and C5-LOW.** Both require a Gorrund LOW composition body. Under order §9 that body may be derived only after ARM acceptance, so it does not exist.

**Consequence, stated before scoring.** The pre-registered gate requires C1–C5 in both runs. It therefore **cannot PASS** in this block whatever the scores are.
- If C2–C5-REF pass in both runs, the outcome is recorded as "REF criteria pass; gate incomplete (C1 / C5-LOW not evaluable)".
- If any of them fails, the outcome is a mandatory failure with that evidence.

No failed output will be replaced or re-run.
