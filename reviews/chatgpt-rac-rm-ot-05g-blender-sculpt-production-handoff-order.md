# RAC RM-OT-05G — Blender sculpt production handoff order

**Authority:** Tyler-approved author workflow selection following RM-OT-05F and its completed author-ruling closure.
**Date:** October 11, 2026 (America/Phoenix).
**Status:** EXECUTE — production support only; then STOP awaiting the external sculpt.

## 1. Workflow decision and scope

Select **Blender as the preferred external/direct sculpt workflow** for the Gorrund hand-sculpt dependency. The route is the supplied accepted-route base mesh → deliberate sculptor edits of existing vertices → controlled base-level OBJ export → unchanged 05F re-entry validation → replicated blind structural-readability gate.

Claude must prepare a practical Blender-safe production handoff, including the scripts, reference scene setup, checklists and validation instructions a sculptor needs. This order authorizes support tooling and packaging. It does not authorize Claude to generate another procedural Gorrund body or claim that setup work satisfies the external sculpt dependency.

Read and preserve:

- `reviews/chatgpt-rac-rm-ot-05f-gorrund-hand-sculpt-handoff-stage-c-order.md`
- `reviews/chatgpt-rac-rm-ot-05f-handoff-author-ruling-freeze-order.md`
- `reviews/claude-rac-rm-ot-05f-handoff-author-ruling-closure.md`
- `reviews/gorrund-rm-ot-05f-hand-sculpt-production-brief.md`
- `reviews/rac-rmot05f-handoff/README.md` and its template/data/evidence assets
- `tools/rac/w1/rmot05f_drivers/`

The frozen brief governs anatomical intent; canon governs any conflict. Preserve Q1: strong planar anatomical organization on an anatomically shaped, radiused trunk, never rectangular, boxy, mechanically slab-sided or cylindrical. The reference sculpt must not depend on a human pinched waist as its readability cue; canon-valid Frame/composition waist variation remains available. Region masks define editing jurisdiction only. Preserve all six hard-form families and their guardrails.

## 2. State remains locked

- **RM-OT-05 remains OPEN.**
- **Grask E3 stays frozen** as the accepted developmental race-anatomy direction pending Stage C. No new Grask search or promotion.
- **Gorrund remains unaccepted: EXTERNAL SCULPT REQUIRED — AWAITING ASSET.** Every failed/provisional 05C–05E candidate remains unpromoted.
- **Stage C remains blocked** until a genuine sculpt passes all technical re-entry guards and the replicated blind gate.
- No D4, UE5 implementation or canon promotion. Handoff readiness, an unchanged round-trip OBJ or a preview render is not acceptance.

## 3. Exact asset contract

Start exclusively from `reviews/rac-rmot05f-handoff/template/GO_ref_route_r6.obj`. Return `GO_sculpt_<ID>_r6.obj`, with a two-character version ID (first genuine delivery may be `S1`).

| Property | Required protection |
|---|---|
| Topology | Exactly **13,380 vertices**, each retaining its original template index; identical ordered faces and winding. Move existing vertices only. |
| Coordinates | **1 numeric unit = 1 cm; Z up; +Y anterior; +X body left; ground z = 0.** Preserve source coordinates through import/export. |
| Pose/scale | Supplied R-6 neutral stance, reference stature 230.90 cm. No re-pose, re-scale, re-centre or re-ground. Lock object transforms. |
| No-touch zones | Use every `NO_TOUCH_*` set in `data/regions.json`: head/neck, hands/digits, toes/forefoot. Aim for unchanged positions; existing ingest tolerance remains ≤ 0.5 cm. |
| True floor | `template/GO_true_floor_r6.obj` is the hard inner limit. Existing ingest condition: zero organized vertices penetrating by more than 0.2 cm. |
| Locked route | Skeleton, joints, long-bone axes/scales, stature route, protected structural relations, plantigrade contact, five digits, rig compatibility, Frame/composition and volume semantics remain unchanged. |

No remesh, voxel remesh, DynTopo, weld/merge, split, dissolve, added/deleted geometry, retopology, triangulation or vertex reordering on the deliverable. No applied subdivision or topology-changing modifier on the exported base. Temporary subdivision may support visualization only; the returned base must retain every index and face. Any projection from a working high-resolution level must preserve that base and pass the same checks.

## 4. Required Blender support package

Add a companion under `reviews/rac-rmot05f-handoff/blender/` and support scripts under an appropriately named tools directory. Preserve the frozen source package; only add navigation pointers where necessary.

Deliver:

1. **Setup script and reproducible scene instructions.** Parse the source OBJ without splitting, merging or sorting vertices. Use Keep Vert Order / Split off where supported; otherwise construct the mesh directly in source order. Record the Blender version and actual supported options. Create an immutable source reference and one editable base object. Keep true-floor, old-lean, low-route and other guide meshes in separately named, non-exported collections. Derive joint/station overlays and protected groups from existing data. Lock reference/guide objects against editing; isolate sculpt/export selection.
2. **Protection setup.** Create named vertex groups and sculpt masks from the exact no-touch index sets, plus family A–F jurisdiction groups. Make protected regions clearly visible. Explain that masks are editing aids; numerical checks enforce the contract. Do not silently alter coordinates when installing masks or scene units.
3. **Controlled exporter.** Export only base-level vertex coordinates in original template order, using the original template face list and winding. Preserve non-position source records as needed; `vt`/`vn` remain irrelevant to current validation. Reject altered topology, transforms, invalid coordinates, missing indices or ambiguous correspondence. Never infer correspondence by nearest-neighbour matching or quietly repair/reorder a changed mesh. A template-based exporter may retain original `f` records and replace only `v` positions after verifying index correspondence.
4. **Reference/view setup.** Provide front, front ¾, profile, rear ¾ and silhouette views matching the 05D/05E sheet standard, neutral grey, matched ground/stature/cameras and body-only views. Hide head/neck for viewing without deleting mesh vertices. Label failed Gorrund examples as failure evidence and Grask E3 as contrast only. No bulk, posture, face, clothing or surface decoration as identity shortcuts; no borrowed Grask hump/high-calf/long-cord cues.
5. **Sculptor checklist.** Step-by-step open/setup, save a working copy, mask protected zones, directly sculpt existing vertices, inspect all six families and canon guardrails, save, export, run preflight and submit. Include low-composition and Narrow/Broad persistence previews using the existing transport semantics; never approximate them with whole-body scaling or invent morphology. Provide exact commands and expected files.
6. **Delivery checklist and manifest.** Record source commit and asset hashes, Blender version, scripts/settings, sculptor provenance, version ID, returned OBJ hash, working `.blend` if available, matched view captures and validation logs. Optional high-resolution references are separate, never replacements for the base OBJ.

Document version-specific import/export axes and unit handling. Do not assume an exporter checkbox guarantees safety. The brief’s Apply Transform instruction must produce identity in source coordinates: no net axis rotation or scale conversion. Prove the result numerically. If a Blender operator cannot meet the contract, use the explicit source-order parser/exporter and document it.

## 5. Tooling verification before handoff

Run an **unedited round-trip test** through setup and export. Compare every indexed vertex position and every face against the template; demonstrate no net rotation, translation, scale, stature or ground change. Confirm all no-touch groups use the source indices. Keep test outputs clearly labelled as tooling evidence, outside the genuine-sculpt candidate namespace.

Use disposable negative fixtures to verify rejection of changed vertex count/order or face indices, changed object transforms and protected-zone displacement beyond the existing tolerance. Prove identity correspondence with stored original-index data and topology checks; a count check alone is insufficient. Support tools must fail closed on ambiguous identity.

Do not change existing validator thresholds, scorer prompt or tally rules. Report actual test commands/results. If Blender cannot be run in Claude’s environment, deliver the scripts and manual verification steps, explicitly mark the round trip **UNVERIFIED**, and stop at that blocker; do not claim a tested or production-ready `.blend`. Never substitute a procedural sculpt to fill the gap.

## 6. Re-entry and Stage C gate

When a genuine externally/directly sculpted asset arrives, preserve the existing sequence:

```text
python3 tools/rac/w1/rmot05f_drivers/f_reentry.py GO_sculpt_<ID>_r6.obj <ID>
```

Every ingest and downstream guard must pass on reference, low, Narrow and Broad, with the transport report. Only then run `f_blind.py`, use `f_scorer_prompt.md` verbatim and tally with `f_tally.py`: at least two fresh shuffled runs, three fresh uninformed scorers per run, eight human-family controls plus frozen Grask E3 reference/low and Gorrund reference/low. Preserve all G1–G7 conditions: ≥ 2/3 C at reference and low in every run; stable exclusion of controls and Grask; structural organization with both axial and limb cues; no human-control collapse. A pass in one run and fail in another is a fail.

Only after both gates pass may the previously authorized combined Stage C use frozen Grask E3 and the validated Gorrund sculpt. This support order neither starts Stage C nor closes RM-OT-05. No D4/UE5/canon promotion follows automatically.

## 7. Claude response and stop condition

Commit the support package and write `reviews/claude-rac-rm-ot-05g-blender-sculpt-production-handoff-report.md`. List files changed, source hashes, setup/export/checklist entry points, reproducible commands, actual round-trip and rejection-test results, unverified items and exact sculptor next action. Confirm no new procedural Gorrund body was made, no frozen anatomy/canon/validator threshold was changed, Grask E3 remains frozen, RM-OT-05 remains OPEN and Stage C remains blocked. Add only necessary status/tracking pointers.

Do not use `arch_sculpt.py`, `race_base.py` or derivative parameter searches to manufacture another Gorrund candidate. Existing transport/validation machinery may process an authentic sculpt or clearly labelled tooling fixtures without changing anatomy rules. No AI-generated replacement mesh, placeholder accepted body or reopened 05C–05E search.

After support preparation and its report, **STOP: EXTERNAL SCULPT REQUIRED — AWAITING ASSET.** The missing deliverable is the actual sculptor-produced `GO_sculpt_<ID>_r6.obj` derived from the frozen template.
