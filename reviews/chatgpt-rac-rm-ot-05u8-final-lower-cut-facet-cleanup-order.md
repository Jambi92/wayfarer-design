# RAC RM-OT-05U8 — final micro-scope lower-cut facet cleanup from U7 cp2

**Authority:** Tyler-authorized autonomous continuation after independent visual review of the U7 technically safe return.
**Date:** October 14, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent order:** `reviews/chatgpt-rac-rm-ot-05u7-minimal-upper-crease-facet-extension-order.md` (d22466e).
**Parent return gate:** `reviews/claude-rac-rm-ot-05u7-upper-crease-facet-repair-gate.md` (bd4a7e8).

## 1. Author ruling on U7

U7 checkpoint 2 is accepted as the new safe technical baseline for one final localized visual cleanup.

It is not yet final Gorrund acceptance.

Accepted and frozen from U7:
- all U7 safety gates;
- all U6 no-regression gates;
- crease A 0.7890 cm and crease B 0.3503 cm;
- U7 local quality min angle 12.68 deg;
- U6 cap quality min angle 13.41 deg;
- U7 cp2's four edited vertices and improved upper-corridor result.

The remaining visual defect is the lower persistent crease cut identified by U7:
- sharpest lower edge: **61562-61580**, about 41.8 deg at the prior cp3 reference and visually still conspicuous;
- adjacent sharp U7-ring-related edges involving **61735** and **61940**.

## 2. Start state

Start only from:

`GO-05U7_cp2.blend`
SHA-256 `1de9d0ac88f0011062a37f75eed6b6811a5288ae1ef80cc632bfc18c38bfb667`.

Do not restart from any earlier scene.

## 3. U8 editable micro-region

Build readiness first from U7 cp2.

### Seed editable vertices

Primary seeds:
- **61562**
- **61735**
- **61940**

Allow only the minimum one-ring support necessary to make a visually continuous correction.

### Hard bounds

- maximum U8 editable vertices: **8**
- maximum U8 authorized/touched faces: **28**
- create a frozen outer ring around the U8 target
- everything outside the U8 target must be bit-exact to U7 cp2

### Special protection: 61580

Vertex **61580 remains frozen initially** because it is the crease-B anchor.

Do not include 61580 in the U8 editable set during readiness or checkpoint 1.

If checkpoint 1 demonstrates that the 61562-61580 cut cannot be corrected sufficiently without moving 61580, STOP and return that exact finding. Do not silently unfreeze it.

No automatic U8A/U9 expansion is authorized by this order.

## 4. Mandatory readiness and protection checks

Before any desktop production edit, build an additive U8 protection path that proves:

- U7 cp2 is the pinned baseline;
- topology unchanged;
- all vertices outside U8 target bit-exact to U7 cp2;
- U8 frozen ring bit-exact;
- vertex 61580 bit-exact;
- all U7-edited vertices not in U8 target bit-exact;
- all U6 lower-repair vertices not in U8 target bit-exact;
- crease A >= 0.6712880840904568 cm;
- crease B >= 0.27434876590971574 cm;
- U6 target roughness remains <= 36.3 deg;
- U6 cap quality remains >= 10 deg;
- U7 local quality remains >= 10 deg;
- U8 local faces: no degenerate/inverted face, min angle >= 10 deg, no edge outside 0.25-2.5 cm;
- V2, V3, V5 and V6c-3 remain PASS.

Focused negative tests must include:
1. moving 61580 -> reject;
2. moving one U8 frozen-ring vertex -> reject;
3. moving one U7 cp2 vertex outside U8 -> reject;
4. topology change -> reject;
5. sub-10-deg U8 face -> fail.

Do not alter historical U2/U4/U6/U7 verifiers.

## 5. Diagnostic

Report the cp2 and checkpoint dihedral values for:
- 61562-61580;
- edges incident to 61735;
- edges incident to 61940;
- all edges in the U8 local corridor.

Diagnostic values guide judgment but do not replace the visual decision.

## 6. Desktop repair

Use real Blender desktop UI only.

Preferred method:
- precise Edit Mode movement of 61562 and/or the two adjacent support seeds;
- small Grab or very light Relax only if truly useful.

No scripted geometry movement, solver, candidate generation, Dyntopo, remesh, projection, global smoothing or topology change.

Goal:
- remove the remaining visibly sharp lower crease cut;
- preserve a natural anatomical groove;
- preserve U6/U7 improvements;
- no new dent, spike, ridge, lip, stair-step or melted patch.

## 7. Pass budget

U8 has at most **two checkpoints**.

Checkpoint 1 should attempt the correction with 61580 frozen.

After checkpoint 1:
- save separately;
- run full U8 verification;
- render identical-camera U7-cp2 vs U8 posterior shaded/wire, zoom shaded/wire, lower-close shaded/wire, and 3/4/lateral context.

If visually resolved and safe, stop early.

If still visually conspicuous and the exact reason is the frozen 61580 endpoint, return that finding and STOP. Do not spend checkpoint 2 merely to move unrelated vertices.

Checkpoint 2 is permitted only for a further small correction inside the already-authorized U8 editable set, with 61580 still frozen.

## 8. Success / stop

If the lower cut is materially removed and all gates pass, return:

**TECHNICALLY SAFE U8 RETURN / AUTHOR VISUAL REVIEW REQUIRED**

with:
- readiness/sets/hashes;
- focused tests;
- exact edit list;
- checkpoint scenes;
- return scene and linked reference;
- verification outputs;
- crease measurements;
- U6/U7 no-regression checks;
- dihedral diagnostic;
- identical-camera evidence;
- distinct ZIP package with manifest, CRC/hash validation and clean-extraction rerun.

Commit:
- `reviews/claude-rac-rm-ot-05u8-final-lower-cut-facet-cleanup-gate.md`
- evidence under `reviews/rac-rmot05u8-evidence/`.

Then STOP.

If the defect cannot be resolved safely without moving 61580, state:
**U8 BLOCKED ON CREASE-B ANCHOR 61580 / AUTHOR RULING REQUIRED**
and return the best safe checkpoint.

Do not promote Gorrund, begin Stage C, alter Grask E3, or start D4/UE5/rigging/creator implementation.
