# RAC RP1F — Gorrund family-pilot localized aesthetic refinement order

**Date:** 2026-10-20  
**Authority:** Tyler direct author feedback following the v014 family-pilot visual review.  
**Parent technical pass:** RP1E v014.  
**Frozen baseline:** `GO_U_REF_RP1E_retopo_v014.blend`.  
**Visual evidence:** `reviews/rac-rp1e-evidence/v014_final/visual_review/`.

## 1. Author review result

Tyler's family-pilot review is:

**RP1E TECHNICAL RETOPO ACCEPTED / FAMILY-PILOT PASS WITH LOCALIZED AESTHETIC REFINEMENT**

Do not reopen the successful RP1E retopology globally.

The v014 body proportions, stature, tail, limbs, torso, ears, hands/web topology, axilla solutions, pouch/perineum topology, and overall Gorrund identity are accepted as the production baseline.

The only approved author changes are:

1. more feline **hand claw** anatomy;
2. better **toe-to-claw/nail proportion and shape**;
3. slightly reduced / better blended **whisker-pad prominence**;
4. a diagnostic shading/fur test for visible repair-region rippling, followed by geometry polish **only if the artifact survives intended shading**.

## 2. Versioning and preservation

Freeze v014 unchanged.

Create a new family-pilot refinement candidate:

- design / cage: **v015**
- PC file: `GO_U_REF_RP1F_refine_v015.blend`

Do not overwrite:
- `GO_U_REF_RP1E_retopo_v014.blend`;
- `design_v014*`;
- v014 D masks;
- v014 gate evidence.

The v015 candidate is not final canon until Tyler reviews the new comparison renders.

## 3. Global no-change rule

Outside the explicit refinement masks in this order, v015 must remain effectively identical to v014.

Do not alter:
- stature;
- shoulder width;
- torso/chest/abdomen;
- pelvis/hips;
- arm or leg proportions;
- hand length/width;
- finger count or general finger proportions;
- existing R-hand visible through-slit;
- L-hand web/tunnel exterior solution;
- axilla topology;
- foot length/width;
- toe count;
- tail root/length/curve;
- ear silhouette;
- nose projection;
- muzzle length;
- jaw/chin;
- pouch/perineum;
- any D-mask definition unless a local approved aesthetic edit geometrically requires a boundary re-audit.

No broad smoothing or resculpting.

## 4. Refinement A — hands: feline claw treatment

### 4.1 Art direction

The current hands are technically excellent but read too human because the distal digits and nail plates look human.

The goal is:

> **fully functional humanoid hands with unmistakably feline distal anatomy.**

Do **not** turn the hands into paws.

Preserve:
- five-digit dexterity;
- thumb opposition;
- weapon/tool grip;
- existing finger lengths;
- existing web/through-slit anatomy.

### 4.2 Claw design

Each hand digit should receive a subtle **retractable or semi-retractable feline claw/sheath treatment**.

Default relaxed pose:
- claw mostly retracted;
- a small pointed keratin tip may remain visible;
- nail bed transitions into a feline claw sheath rather than a flat human fingernail;
- distal fingertip remains usable for manipulation.

Avoid:
- long permanent talons;
- exaggerated raptor claws;
- fantasy stiletto fingernails;
- changing finger length to create the claw;
- oversized claw volume that interferes with gripping.

### 4.3 Geometry guidance

Prefer:
- narrower keratin base than the current human-like nail plate;
- stronger dorsal taper;
- mild downward curvature;
- a defined sheath/lip around the claw root;
- tip centered along the distal phalanx rather than sitting like a flat plate.

The visible relaxed tip should be modest. Treat potential full extension as a future rig/shape-key/animation concern, not as the default sculpt.

### 4.4 Symmetry / identity

Keep the handed asymmetries and special R-hand topology already proven in RP1E.

Do not rebuild web topology merely to add claws.

## 5. Refinement B — feet: toe/claw proportion

Tyler's note: the current toe/nail ratio feels off.

The issue is not the accepted foot size or toe layout. It is the broad plate-like keratin coverage.

### 5.1 Target

Keep:
- plantigrade foot;
- current toe count and fused-fifth anatomy;
- current foot/toe lengths;
- current gait-capable silhouette.

Change only the keratin/claw read.

### 5.2 Toe claw design

Revise each visible toe nail toward a feline claw:

- slightly narrower base;
- less lateral plate coverage;
- stronger taper toward the free edge;
- mild dorsal-to-downward curvature;
- more pointed but **not needle-like**;
- claw/sheath transition integrated into the toe;
- preserve the small overall claw scale appropriate to normal locomotion and footwear.

Do not make the toes longer.

Do not create oversized exposed talons.

### 5.3 Ratio target

Use the current nail length as a starting point, but reduce the visual impression of “nail plate covering the toe” by narrowing and tapering before adding any net length.

Any increase in exposed tip length should be small and subordinate to the taper/sheath correction.

## 6. Refinement C — whisker pads

Tyler's note: the whisker pads are too pronounced.

The current muzzle length, nose, jaw and chin are accepted.

Do **not** shrink or shorten the muzzle.

### 6.1 Target

Reduce the prominence of the individual whisker-pad lobes by approximately **10–15% as a starting range**, then judge visually.

The goal is:
- one broad leonine whisker-pad mass;
- individual follicle/lobe forms still readable;
- less “cluster of swollen bumps” appearance;
- smoother transition into the muzzle/cheek.

### 6.2 Preserve

Preserve:
- muzzle width;
- muzzle length;
- nose width/projection;
- lip line;
- philtrum;
- jaw/chin;
- left/right identity.

Blend the lobes together more smoothly rather than simply flattening the entire muzzle.

The eventual fur/follicle/whisker system should provide much of the micro-definition.

## 7. Refinement D — rippling diagnostic before geometry change

Some close v014 renders show directional rippling/creasing in heavily repaired regions, especially:
- muzzle/eyelid/cheek;
- hand webs;
- L axilla;
- R axilla.

Do **not** automatically smooth these areas.

### 7.1 First: shading/material diagnostic

Create a diagnostic comparison using v014 unchanged:

1. smooth normals / intended production smooth shading;
2. neutral skin-like rough material without cavity exaggeration;
3. a **temporary short-fur preview** or procedural short-fur stand-in sufficient to show whether the fine rippling survives the intended surface treatment.

This is diagnostic only; do not build a final fur system.

Render:
- face front / three-quarter / profile;
- muzzle close;
- R hand;
- L hand/web;
- both axilla close views.

### 7.2 Decision

If the apparent rippling disappears under proper smooth shading / short-fur preview:
- make **no geometry change** for that region.

If a ripple remains clearly visible as a real surface wave:
- perform the minimum bounded polish needed;
- no silhouette change;
- no loss of anatomical crease;
- no reopening of D cavities;
- no topology change unless strictly required.

Document exactly which regions were polished and why.

## 8. Construction method

The preferred method is to refine the **v014 cage/design where practical**, then regenerate the production surface so the family-pilot changes are reproducible.

For claw/sheath geometry that cannot be represented faithfully by the existing cage:
- a localized cage topology addition is allowed;
- preserve genus 1;
- preserve all RP1E successful contact topology.

For very fine claw free-edge support or tiny surface polish:
- bounded final-resolution overrides are allowed using the established v014 provenance method.

Every final-resolution override must be recorded.

Do not use automatic remesh / voxel remesh / QuadriFlow.

## 9. Refinement masks and delta control

Create explicit v015 author-change masks for:

- `A_HAND_CLAWS_L`
- `A_HAND_CLAWS_R`
- `B_FOOT_CLAWS_L`
- `B_FOOT_CLAWS_R`
- `C_WHISKER_PADS`
- optional `D_POLISH_<region>` only where §7 proves necessary.

All production-vertex movement outside those masks should be zero except for the smallest unavoidable support-ring continuity zone.

Report:
- moved vertex count per mask;
- max displacement;
- bbox delta;
- stature delta;
- any movement outside masks.

## 10. Technical gate after refinement

Because this is an author-approved anatomy change, do **not** compare the edited regions against the old GO-05AW4 source as though the old shape remained mandatory.

Instead use a two-part gate:

### 10.1 Unchanged regions
Against v014:
- silhouette/landmarks unchanged;
- no unintended drift;
- no new self-x;
- no topology damage.

### 10.2 Edited regions
Against the explicit author-refinement intent in this order:
- claw/sheath geometry coherent;
- whisker-pad reduction within the intended range unless documented visual reason requires less/more;
- no collision or self-x;
- no dexterity/locomotion obstruction;
- left/right consistency.

### 10.3 Whole mesh
Required:
- 1 component;
- 0 boundary;
- 0 non-manifold;
- genus 1;
- 0 degenerate faces;
- 0 production self-intersections;
- quad-dominant / preserve 100% quads where reasonably possible;
- T-3 unchanged outside local author edits;
- T-6 remains passing;
- T-7 remains passing at >=0.995;
- visual silhouette preserved.

The old ±0.15 mm nail-to-GO-05AW4 gate is **superseded for the edited claw regions**, because Tyler is intentionally changing their anatomy.

Instead record the new claw dimensions explicitly so they can become the next frozen reference if approved.

## 11. Required visual return

Create side-by-side comparison renders:

### Whole body
- front;
- left profile;
- rear.

### Face
- front;
- three-quarter;
- profile;
- muzzle close.

### Hands
- R front;
- R outside;
- R claw close;
- R slit close;
- L front;
- L outside;
- L claw close;
- L web close.

### Feet
- top both feet;
- L toe/claw close;
- R toe/claw close;
- side/oblique claw profile.

### Diagnostic polish
- before/after material/shading comparison for each region that was actually polished.

Each comparison must show:
- **v014 PASSED BASELINE**
- **v015 FAMILY-PILOT REFINEMENT**

Do not compare v015 only against GO-05AW4 for the intentionally changed claw/pad regions; show v014→v015 so Tyler can judge the author-directed delta.

## 12. Stop / return logic

### Desired result

When the candidate is technically clean and renders are ready, return:

**RP1F GORRUND LOCALIZED REFINEMENT COMPLETE / READY FOR AUTHOR VISUAL REVIEW**

STOP.

Do not freeze v015 as final Gorrund anatomy until Tyler approves the visual result.

### If a localized change threatens accepted topology

If any requested claw/pad refinement cannot be completed without damaging:
- the R-hand handle;
- L-hand web/tunnel solution;
- axilla topology;
- genus;
- zero-self-x;
- or major silhouette,

return:

**RP1F LOCALIZED REFINEMENT BLOCKED / AUTHOR DECISION REQUIRED**

Show the exact conflict and STOP.

## 13. No downstream work

No RP2.
No rigging.
No character-creator implementation.
No UE5 production integration.
No propagation to other Gorrund bodies until Tyler approves v015.

## 14. Return files

Create:

`reviews/claude-rac-rp1f-gorrund-v015-localized-refinement-gate.md`

Evidence:

`reviews/rac-rp1f-evidence/gorrund_v015/`

Update:
- `reviews/claude-session-handoff.md`
- `specs/STATUS.md`

Keep RP1E v014 recorded as the frozen technical-pass baseline.
