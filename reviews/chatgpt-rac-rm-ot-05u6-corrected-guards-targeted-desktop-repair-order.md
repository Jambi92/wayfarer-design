# RAC RM-OT-05U6 — correct over-constrained local guards and perform targeted desktop notch repair

**Authority:** Tyler-authorized autonomous continuation; ChatGPT author ruling after independent review of the 05U5 return, package and failed-pass evidence.
**Date:** October 14, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent:** `reviews/claude-rac-rm-ot-05u5-bounded-desktop-sculpt-return-gate.md` (17aa792).

## 1. Author ruling on 05U5

05U5 is accepted as an honest failed attempt and safe stop. The returned checkpoint 0 is correctly NOT a technically valid repair and remains the baseline.

The desktop fixture results F1-F5 are accepted. The current 365-vertex / 832-face U2 protection boundary and 106-vertex frozen ring are also accepted and remain unchanged.

No wider boundary is authorized.

Two verification rules are corrected because 05U5 demonstrated that they are over-constrained relative to the actual authorized task:

### R1 — roughness guard (b): target versus baseline exceptions

The 36.3-degree roughness threshold is a **repair-target criterion**, not a requirement to repair untouched geometry outside the approved working locus.

The three demonstrated baseline offenders outside the brushed cap/strip:
- S3 vertex 70735;
- S3 vertex 70592;
- S3 vertex 70408;

are **baseline exceptions** for this local repair. They must remain bit-exact to the 05U baseline and must not be used as a reason to fail the notch repair.

For the actual local repair target (upper cap and approximately 1 cm of the posterior strip), the 36.3-degree threshold remains binding. Existing in-target offenders must be corrected rather than grandfathered.

All other vertices outside the actual local repair target must remain unchanged. Do not broaden the brush area merely to improve a diagnostic.

Update the aggregate/reporting logic additively so it reports:
- target roughness PASS/FAIL;
- baseline-exception identity PASS/FAIL;
- the historical 365-wide value as a diagnostic only.

Do not rewrite historical results.

### R2 — sliver guard (e): use meaningful cap quality, not per-face monotonicity

The 05U5 rule that every one of the 35 cap faces must retain or improve its own previous minimum angle is retired for this repair. It incorrectly rejects a result that can substantially improve the worst triangle while some already-safe neighboring triangles change modestly.

The replacement local cap-quality guard is:
- no degenerate or inverted cap face;
- no cap face below **10 degrees** minimum angle after the repair;
- no **new** cap edge outside the existing V4 edge band of **0.25–2.5 cm**;
- any cap edge already outside that band at the frozen baseline may remain only if bit-exact / unchanged and must be reported;
- V2 and V3 remain mandatory.

Report the old per-face-relative guard as historical diagnostic only. Do not silently alter old 05U5 evidence.

The known source face 130139 at 6.24 degrees is inside this cap and therefore must be improved to at least 10 degrees for a U6 technical pass.

## 2. Crease guards remain frozen

Do not change the 05U4 frozen crease reference.

Required:
- section A depth >= 0.6712880840904568 cm;
- section B depth >= 0.27434876590971574 cm.

The result must preserve a readable natural groove; passing these numbers alone is not visual acceptance.

## 3. Authorized desktop method

The Smooth-only restriction from 05U5 is lifted because the evidence demonstrates that Smooth alone couples notch reduction to crease loss / local quality failure.

Use the **real Blender desktop UI** only. No scripted geometry generation.

Permitted tools, locally and sparingly:
- Grab;
- Smooth;
- Slide Relax / Relax if available as an interactive sculpt/edit operation;
- direct Edit Mode movement of the specific local notch vertices when needed for precise cleanup.

Use the existing topology. No Dyntopo, remesh, voxel remesh, global smoothing, shrinkwrap/projection, solver, coordinate sweep, scripted relaxation, or automatic candidate generation.

Primary target remains the visible posterior upper saw-tooth / notched strip, especially the two persistent notch locations represented by vertices 61581 and 61303. Correct the surface by anatomical judgement, preserving the groove rather than flattening it.

Do not edit the anterior, the far posterior taper, pose, proportions, shoulder architecture, other garments or any geometry outside the current U2 authorization.

All reconstructed/edited skin remains INFERRED.

## 4. Pass budget

This is a **new author-authorized method/gate block**, so U6 has a fresh budget of at most **three deliberate production checkpoints**. This is not a reset of the historical 05U5 budget; preserve 05U5 as completed evidence.

After each checkpoint:
1. save a distinct checkpoint;
2. run the corrected U6 verification;
3. inspect identical-camera zoom and posterior views;
4. stop early if all U6 numerical gates pass and the notch is visibly resolved.

Do not spend another pass when diagnostics show the remaining approach cannot succeed.

## 5. Mandatory U6 technical gates

A TECHNICALLY VALID U6 return requires all of:

- U2 protection accepted exactly;
- 0 moved vertices outside the existing 365;
- 0 moved vertices on the 106 frozen ring;
- the three R1 baseline exceptions bit-exact to the frozen baseline;
- target roughness <= 36.3 degrees;
- local cap-quality R2 PASS;
- crease A PASS;
- crease B PASS;
- V1-U2 PASS;
- V2 boundary/manifold PASS;
- V3 intersections PASS;
- V5 seam continuity PASS;
- V6c-3 no folds PASS;
- no topology change unless separately stopped and returned for author approval (none is authorized here).

Continue to report V4, V6 historical, V6c-1 and V6c-2 globally and honestly. The untouched far taper/anterior failures are not silently waived or repaired by this order; the U6 decision is for the bounded posterior upper-notch task only.

The aggregate command must return success only when the U6 mandatory gates above all pass. Add focused tests for the revised R1/R2 logic before production, including negative fixtures that prove:
- moving any baseline-exception vertex fails identity;
- an in-target roughness offender still fails above 36.3;
- a cap face below 10 degrees fails;
- a safe cap face may lose some minimum angle while remaining >=10 degrees without failing solely for that reason.

## 6. Visual gate

Even after numerical PASS, inspect the result against the 05U baseline and the 05U5 failed attempts.

Required visual outcome:
- the posterior upper saw-tooth/notched strip is no longer conspicuous;
- no new spike, dent, cut lip or faceted ridge;
- the arm-to-posterior-axillary-fold groove remains anatomically readable;
- adjacent deltoid/triceps relief is preserved;
- no over-softened or melted patch.

If technically valid but visually questionable, stop for Tyler review rather than iterating automatically.

## 7. Deliverables and stop

Commit:
- `reviews/claude-rac-rm-ot-05u6-targeted-desktop-notch-repair-gate.md`
- evidence under `reviews/rac-rmot05u6-evidence/`.

Include:
- revised verifier/aggregate and focused tests;
- real desktop edit log;
- every U6 checkpoint;
- exact changed vertices/faces;
- return .blend and linked reference;
- supported NPZ/OBJ, reintegration, verify, crease, local guards, aggregate and hashes;
- identical-camera baseline-versus-return posterior shaded/wire, zoom shaded/wire, lateral/3-4/underside context;
- a distinctly named package with its own manifest, CRC/hash validation and clean-extraction rerun.

If all U6 gates pass, state:
**TECHNICALLY VALID BOUNDED RETURN / AUTHOR VISUAL REVIEW REQUIRED.**

If they do not, return the best safe checkpoint and state the exact remaining blocker without widening scope or creating substitute geometry.

Then STOP.

Gorrund remains UNACCEPTED until Tyler's visual ruling; Grask E3 remains FROZEN; RM-OT-05 OPEN; Stage C BLOCKED; no canon promotion, D4, UE5, production rigging or creator implementation.
