# RAC RM-OT-05AW — bounded Gorrund feline toenail refinement

**Authority:** Tyler-approved follow-up after successful 05AV foot/heel correction.
**Date:** 2026-10-17.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Author acceptance:** `reviews/tyler-rac-rm-ot-05av-gorrund-foot-author-acceptance-with-claw-exception.md`
**Parent gate:** `reviews/claude-rac-rm-ot-05av-gorrund-foot-heel-correction-gate.md`

## 1. Purpose

Perform one strictly bounded local refinement of the Gorrund toenails so they read like the tapered keratin nail forms of a large wild cat rather than blunt human toenails.

This is a cosmetic morphology pass only.

The accepted body composition, head share, tail root, foot dimensions, heel stance, plantigrade support and ankle relationship must remain unchanged.

## 2. Frozen source

Start only from:

`GO-05AV_feet_final.blend`
SHA-256:
`45a04787c4760e95b9a9bef52837a516788670f1f1bade92c380ffcea74ab9a6`

Review GLB:
`GO-05AV_feet_final.glb`
SHA-256:
`b595f11e2cb4d6f69cdc38954fc9f422dadda9e8e46cee8aed57869face92b4b`

Do not use any pre-05AV foot state.

## 3. Scope

Allowed:
- visible toenail geometry on all toes of both feet;
- the minimum immediate nail-bed transition needed for continuity.

Do not change:
- foot length or width;
- heel position or heel lift;
- plantar contact;
- toe count, spacing, base size or length;
- ankle shape or position;
- lower-leg proportions;
- stance;
- body composition;
- head;
- tail;
- hands.

## 4. Visual target

The toenails should read as naturalistic big-cat nail forms in a neutral/resting presentation.

Required qualities:
- more tapered;
- narrower toward the distal end;
- modestly more projecting beyond the soft toe tip;
- subtly curved;
- less flat/blunt than the current human-like nail;
- naturally integrated into each toe.

Use lion/tiger/large-wild-cat anatomy as the visual family, while keeping the result restrained and believable.

## 5. Guardrails

Do not create:
- oversized fantasy nail forms;
- extremely long or thin tips;
- exaggerated hooks;
- disconnected nail pieces;
- broad toe reshaping.

The nail forms must remain proportionate to the accepted 05AV feet.

## 6. Toe hierarchy and symmetry

Preserve the existing toe-size hierarchy.

The largest toe may carry the most substantial nail, but all toes should share a coherent species language:
- similar taper family;
- similar curvature family;
- consistent nail-bed integration.

Left and right feet should match closely in:
- projection;
- taper;
- curvature;
- nail-bed placement.

Organic micro-variation is acceptable.

## 7. Preferred authoring method

Final morphology authoring must occur in Blender UI.

Allowed:
- tiny local Edit Mode transforms;
- tiny local sculpt/Grab;
- restrained Smooth;
- restrained local shaping of the nail tip;
- local vertex groups/masks for protection.

Diagnostic scripts may:
- identify nail vertices;
- measure nail projection;
- compare symmetry;
- validate technical gates;
- produce evidence.

Forbidden:
- scripted final vertex placement;
- remesh;
- Dyntopo;
- voxel remesh;
- whole-toe scaling;
- broad foot sculpting.

## 8. Projection envelope

Use the current nail bed as the anatomical root.

Target only a modest increase in visible distal nail projection.

Hard rule:
- total foot length must remain within the accepted 05AV tolerance;
- target total-length change from 05AV: <= 2 mm per foot;
- accepted footprint width remains effectively unchanged.

## 9. Technical gate

Required after the nail pass:

- 0 opened seams;
- 0 self-intersections;
- 0 flipped faces;
- 0 degenerates;
- 1 component / 0 boundary / 0 non-manifold;
- no new toe contact or fusion;
- no overlap between adjacent nail/toe surfaces;
- no ground-plane intersection from the refined nails;
- no visible deformation outside nail + immediate nail-bed transition;
- foot length change <= 2 mm;
- accepted foot width effectively unchanged;
- heel lift and plantar contact unchanged;
- ankle joint centre unchanged;
- body above the foot region unchanged.

The three known connectivity defects from 05AU remain out of scope.

## 10. Visual gate

PASS only if:
- the previous human-toenail read is clearly reduced;
- the nails read feline/naturalistic;
- taper is clearly improved;
- projection and curvature are restrained;
- current 05AV foot proportions remain intact;
- feet still look large, load-bearing and plantigrade;
- the nail treatment does not become exaggerated.

## 11. Output

If PASS, freeze:

`GO-05AW_nails_final.blend`
`GO-05AW_nails_final.glb`

Record exact hashes.

## 12. Evidence

Return:

`reviews/claude-rac-rm-ot-05aw-gorrund-toenail-refinement-gate.md`

Evidence:

`reviews/rac-rmot05aw-evidence/`

Include:
- close before/after views of both feet;
- front/profile/3-4 nail closeups;
- whole-body before/after confirmation;
- exact local work region;
- technical gate summary;
- protected-region displacement report;
- final foot measurements.

## 13. Decision

### PASS

Return:

**05AW TOENAIL REFINEMENT PASS / READY FOR FINAL GORRUND CLOSURE REVIEW**

Then STOP.

### FAIL

If a credible feline nail read cannot be achieved without changing accepted toe/foot proportions:

**05AW TOENAIL REFINEMENT NOT CREDIBLE / STOP**

Revert active geometry to `GO-05AV_feet_final`.

## 14. State

- Gorrund BODY COMPOSITION: AUTHOR ACCEPTED / FROZEN
- Head share: AUTHOR APPROVED / FROZEN
- Tail root: AUTHOR APPROVED / FROZEN
- Foot size + heel stance: AUTHOR APPROVED / FROZEN
- Toenail morphology: IN REFINEMENT
- Connectivity cleanup: CARRIED TO RETOPOLOGY / RIG PREP
- Gorrund overall mesh: NOT YET FINAL
- Grask E3: FROZEN
- RM-OT-05: OPEN
- Stage C: BLOCKED
- no D4 / UE5 / production rigging / creator implementation
