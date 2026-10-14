# RAC RM-OT-05U7 — minimal upper-crease facet extension from accepted U6A checkpoint 3

**Authority:** Tyler-authorized autonomous continuation after independent visual review of the U6A technically valid bounded return.
**Date:** October 14, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent order:** `reviews/chatgpt-rac-rm-ot-05u6a-resume-remaining-desktop-checkpoints-order.md` (b344af7).
**Parent return gate:** `reviews/claude-rac-rm-ot-05u6a-resumed-checkpoints-return-gate.md` (bb65683).

## 1. Author ruling on U6A

U6A checkpoint 3 is accepted as the **new safe technical baseline** for continued repair work.

It is not final author acceptance of Gorrund.

The following are accepted from U6A and must not be regressed:
- U2 protection, topology, V1-U2, V2, V3, V5 and V6c-3;
- R1 target roughness max 35.29 deg;
- R2 cap quality, minimum cap angle 13.63 deg;
- frozen crease A 0.7890 cm and crease B 0.3658 cm;
- the seven U6-changed vertices and their resolved lower-notch/sliver geometry.

The lower notch/sliver repair is visually acceptable as a continuation baseline.

The remaining blocker is visual: upper saw-tooth/faceted cuts remain visible along the posterior crease above the former cap. U6A identifies the principal geometry as:
- former frozen-ring vertices: **61522, 61771, 62027**;
- protected skin outside U2: **61586, 61183, 62063**.

Those vertices were outside U6 authorization and therefore were correctly left untouched.

## 2. U7 scope: minimal upper-crease extension only

Start from the exact U6A cp3 scene:

`GO-05U6_cp3.blend`
SHA-256 begins `22345d4d`.

Do not restart from 05U, 05U5, cp1 or cp2.

Build a **new U7 handoff copy** that preserves cp3 and creates the smallest contiguous editable target needed to correct the upper visible crease facets.

### Seed region

The target must be derived from the six identified seed vertices:
- 61522
- 61771
- 62027
- 61586
- 61183
- 62063

Use only the incident faces and, if required for a smooth local correction, the minimum one-ring support immediately adjacent to those incident faces.

### Hard size bounds

Without another author decision:
- U7 editable target: **no more than 24 vertices** total;
- U7 touched/authorized faces: **no more than 70 faces** total;
- create a frozen outer ring one topological ring beyond the editable target;
- the existing U6 16-vertex target is frozen at its cp3 coordinates for U7, except shared vertices if a seed/topological necessity proves unavoidable. If any such overlap exists, disclose it before editing and preserve the cp3 visual result.

If a contiguous safe target cannot be built within these bounds, STOP with a proposal rather than widening automatically.

The U7 working corridor must remain confined to the visible posterior upper-crease defect at approximately z 169.4–172.3 cm. Do not extend into unrelated back, shoulder, arm, anterior, far-posterior taper or garment regions.

## 3. Protection and readiness before production edits

Build an additive U7 verifier before desktop editing.

It must prove:
- cp3 geometry is the frozen baseline;
- every vertex outside the U7 target remains bit-exact to cp3;
- the U7 outer ring remains bit-exact;
- topology is unchanged;
- no new face labels or correspondence are lost;
- the U6A resolved lower region remains unchanged;
- crease A >= 0.6712880840904568 cm;
- crease B >= 0.27434876590971574 cm;
- no face in the U7 authorized faces falls below 10 deg minimum angle;
- no degenerate, inverted or intersecting face;
- no new edge outside 0.25–2.5 cm in the U7 local faces;
- V2, V3, V5 and V6c-3 remain PASS.

Keep the global V4 / V6 / V6c-1 / V6c-2 reporting intact and honest. Do not repair unrelated historical failures.

### Focused negative tests

Before desktop production editing, demonstrate that:
1. moving one vertex just outside the U7 target is rejected;
2. moving one U7 frozen-ring vertex is rejected;
3. changing one old U6 cp3 vertex outside any necessary U7 overlap is rejected;
4. a sub-10 deg U7 face fails;
5. a topology change fails.

## 4. Visual/facet diagnostic

The U6 roughness threshold is not the primary detector here; U6A showed the remaining cuts can be visually obvious while below 36.3 deg.

Create a **diagnostic-only** local facet report for the U7 corridor:
- adjacent-face normal/dihedral values around the six seed vertices;
- max and p95 local face-normal change;
- same values after each checkpoint.

Use this to confirm that the visible facets are being reduced, but do **not** invent an arbitrary new pass threshold after seeing the result.

The decisive U7 success test is:
- technical safety gates pass; and
- identical-camera shaded views show the upper saw-tooth/cut pattern materially removed without flattening the anatomical crease.

## 5. Desktop method

Use the real Blender desktop UI.

Permitted:
- precise Edit Mode vertex movement;
- small Grab adjustment;
- very light local Smooth/Relax if it is genuinely helpful.

Forbidden:
- Dyntopo;
- remesh / voxel remesh;
- topology change;
- global smoothing;
- scripted geometry movement;
- solver / coordinate sweep;
- generated candidate mesh;
- projection/shrinkwrap;
- widening the region during production.

Use anatomical judgement. The aim is a continuous posterior axillary-fold/upper crease, not a perfectly flat surface.

Preserve:
- the groove;
- deltoid/triceps relief;
- cp3 lower repair;
- no new dent, lip, ridge, spike or melted patch.

## 6. Pass budget

U7 has at most **two deliberate production checkpoints**.

This is a new scope block for a newly authorized region; it does not alter or reset the historical U6 budget.

After each checkpoint:
1. save a distinct scene;
2. run the U7 protection/safety verifier plus the existing U6 safety checks against cp3 as baseline where applicable;
3. render identical-camera posterior shaded/wire and upper zoom shaded/wire plus 3/4 and lateral context;
4. inspect before deciding whether checkpoint 2 is needed.

If checkpoint 1 is technically safe and the upper cuts are visually resolved, stop early.

If checkpoint 2 cannot resolve the defect without damaging the crease or cp3 repair, return the best safe checkpoint and STOP.

## 7. Success and deliverables

A successful U7 return must be a **TECHNICALLY SAFE U7 RETURN / AUTHOR VISUAL REVIEW REQUIRED**.

Deliver:
- U7 handoff/readiness definition and frozen sets;
- focused tests;
- exact editable vertex/face lists and hashes;
- edit log with exact desktop actions;
- checkpoint scenes;
- final return .blend and linked reference;
- supported return NPZ/OBJ/maps/labels;
- U7 protection/safety results;
- unchanged U6 crease measurements;
- local facet diagnostic;
- identical-camera cp3-vs-U7 views;
- hashes;
- distinctly named package with manifest, CRC/hash validation and clean-extraction rerun.

Commit:
- `reviews/claude-rac-rm-ot-05u7-upper-crease-facet-repair-gate.md`
- evidence under `reviews/rac-rmot05u7-evidence/`.

Then STOP for Tyler visual review.

Do not promote Gorrund, start Stage C, touch Grask E3, perform D4/UE5/rigging/creator implementation, or alter canon.

Expected state after a technically safe U7 return:
- Gorrund: AUTHOR VISUAL REVIEW REQUIRED
- Grask E3: FROZEN
- RM-OT-05: OPEN
- Stage C: BLOCKED
- canon promotion: NOT PERFORMED
