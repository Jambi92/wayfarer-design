# RAC RM-OT-05G — support handoff acceptance, bounded corrections and sculptor release

**Authority:** Tyler-approved next author order after review of the 05G report and sculptor checklist.
**Date:** October 12, 2026 (America/Phoenix).
**Status:** EXECUTE the bounded handoff corrections below, commit the final release package and report, then STOP awaiting an external/direct sculpt.

## 1. Author ruling

Accept the 05G support preparation in its limited scope. The report documents headless verification through Blender bpy 4.2.0 and 5.0.1; this is useful tooling evidence, not proof of desktop brush operation or Gorrund readability. The author review inspected the report, checklist and committed exporter but did not independently rerun the Blender tests. Preserve the disclosed unverified desktop UI, command-line binary and brush-stroke items.

Blender remains the preferred direct sculpt workflow. The actual missing asset remains `GO_sculpt_<ID>_r6.obj`, a sculptor-edited copy of `reviews/rac-rmot05f-handoff/template/GO_ref_route_r6.obj`. No unchanged round trip, failed-route fixture, setup scene or preview is an accepted sculpt.

## 2. Correct the protection claim

Patch `reviews/rac-rmot05f-handoff/blender/CHECKLIST_SCULPTOR.md`, step 10, and any equivalent claims in the README or report. Replace “The exporter refuses every one of these” with this controlling wording:

> These operations are forbidden by the sculpt contract. The exporter rejects detectable topology, identity, transform and protected-region violations; it cannot determine every editing action used to produce a mesh. A manually re-posed limb or another forbidden coordinate edit may preserve topology and object transforms. The sculptor must follow this checklist, and the returned asset must pass the complete 05F re-entry and replicated blind gates.

Keep all prohibited operations prohibited. Do not weaken checks or add claims of universal detection. Explain that the exporter writes base mesh data and ignores non-Multires modifiers: an unapplied modifier visible in the viewport does not become the delivered sculpt. The exported base itself must express the intended forms. No automatic repair, guessed vertex correspondence or procedural morphology correction.

## 3. Make preview and UI limits clear

In the inspection checklist and preview documentation, explicitly state that `g_preview.py` shows transported forms before the authoritative floor clamp and volume restoration. Its views and penetration counts are advisory; it does not prove final persistence or replace `f_reentry.py`. Preserve the report’s observed difference at clamped low-composition vertices. Do not change the transport or validator to make a preview appear to pass.

Add a short first-session desktop verification checklist: confirm the editable base, identity transforms, protected masks and anatomical display orientation; make a small reversible brush edit in an allowed region on a disposable working copy; export and preflight that copy; verify the intended indexed vertex displacement and unchanged protected regions; undo/discard the fixture. Label this as a tooling fixture, never a sculpt candidate. Perform it only if a real interactive Blender session is available; otherwise leave it explicitly pending for the sculptor and record that limitation. Do not invent completed UI tests.

## 4. Release a self-contained sculptor handoff

Verify that copying only `rac-rmot05f-handoff/` leaves every required instruction available. The present checklist refers to a production brief outside that directory. Supply a release bundle or staging folder that includes an exact frozen copy of `reviews/gorrund-rm-ot-05f-hand-sculpt-production-brief.md` and all necessary handoff assets, scripts, checklists, reference/evidence files and transport data, with working relative links. Keep repository originals unchanged apart from necessary pointers and the corrections above.

Use a repeatable packaging command and a release manifest containing source commit, full SHA-256 values and required file paths. Verify completeness and links from a clean extraction or copy, without access to the rest of the repository. If the archive is too large to commit, commit the packaging script, manifest and exact build/download instructions; report the actual output location and hash without claiming an unavailable download. Regenerate script hash lists only if scripts change. Preserve template and frozen-brief hashes.

Add one concise `START_HERE.md` for the sculptor: open the frozen brief, use the supported Blender setup, follow the corrected checklist, complete pending desktop verification, directly sculpt the six hard-form families, inspect/export/preflight, and return the OBJ, working file if available, views, manifest and logs. No new anatomical targets or altered canon.

## 5. Asset and state protections

- Exactly 13,380 source-order vertices and identical faces/winding; existing vertices moved only.
- Supplied R-6 pose and scale; numeric units cm, Z up, +Y anterior, +X body left, ground z = 0. No re-pose, re-scale, re-centre or re-ground.
- Exact source-index no-touch sets; unchanged positions are the editing goal, with existing 0.5 cm ingest tolerance preserved.
- True-floor, skeleton, joints, long bones, stature route, rig, plantigrade contact, digit count, protected structural relations, Frame/composition and volume semantics unchanged.
- Preserve Q1 and the corrected reference-only waist interpretation, all six hard-form families and their canon guardrails. No borrowed Grask identity cues.
- Grask E3 remains frozen as the accepted developmental direction pending Stage C.
- RM-OT-05 remains OPEN. Gorrund remains unaccepted: **EXTERNAL SCULPT REQUIRED — AWAITING ASSET**.
- Stage C remains blocked until a genuine sculpt passes technical re-entry and every replicated blind-gate condition. No D4, UE5 or canon promotion.

## 6. Verification, report and stop

For documentation/packaging-only changes, verify corrected wording, valid relative links, manifest hashes and clean-copy completeness. Do not rerun broad morphology studies. If code changes are necessary, run targeted tests appropriate to those changes and report actual results. Preserve prior test evidence and its scope.

Commit the bounded changes and write `reviews/claude-rac-rm-ot-05g-sculptor-release-closure.md`. List exact files changed, release entry point, source commit, full hashes, packaging command/result, clean-copy check, desktop verification status and the exact sculptor next action. Confirm no new procedural Gorrund body, no canon/threshold change, Grask E3 frozen, RM-OT-05 open and Stage C blocked.

Then **STOP**. Do not contact or hire a sculptor, incur costs, or claim an external asset has been produced. The next production action belongs to a real direct sculpt session using this package. No `arch_sculpt.py`, `race_base.py` or derivative search to manufacture a substitute; no AI-generated replacement topology.

When a genuine asset is supplied, run the unchanged `python3 tools/rac/w1/rmot05f_drivers/f_reentry.py GO_sculpt_<ID>_r6.obj <ID>`. Only after all guards pass run the replicated blind gate with the existing scorer prompt and mechanical tally. Only after both gates pass may the previously authorized combined Stage C use frozen Grask E3 and the validated sculpt. A handoff release does not close RM-OT-05.
