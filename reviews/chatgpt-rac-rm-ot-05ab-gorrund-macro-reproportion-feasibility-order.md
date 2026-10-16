# RAC RM-OT-05AB — rig-assisted macro-reproportion feasibility from donor C

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05AA AA0.
**Date:** October 15, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05aa-gorrund-manual-composition-neutralization-gate.md` (404d2c8).

## 1. Route decision

AA0 correctly proved that donor C cannot proceed through a soft-tissue-only sculpt because its segment proportions conflict with the accepted Gorrund W1 ARM.

This order authorizes a **new derivative route**:

**Use donor C as a high-resolution sculptural donor, but first correct its macro segment/joint proportions with a controlled temporary armature / rigid-segment deformation driven by the already accepted W1 Gorrund ARM.**

This is an order-level supersession of AA0's "do not warp C" rule for one separate feasibility derivative only.

The immutable C donor and AA baseline remain unchanged.

This is **not** authorization to accept C as-is, and it is not a creator/production rig.

## 2. Pinned inputs

### Donor
`Gorrund_Neutral.glb`
SHA-256:
`513bc9e2c5c4ba1da0a5a33661f230181bf18a24c50e0af0d49acdf5521dccf6`

### AA baseline
`GO-05AA_C_baseline.blend`
SHA-256:
`c17ac3c2b213cf877e952fe2089eb0545d661b4ffa14ca197fa42ea954df7bac`

### Accepted macro guide
Retained W1i/W1j Gorrund ARM:
`reviews/rac-w1i-evidence/geometry/GO_r6.npz`

Author acceptance:
`reviews/chatgpt-rac-w1j-gorrund-final-author-acceptance.md`

The accepted ARM is a **guide to anatomical relationships and the accepted reference outcome**, not a surface donor.

## 3. Feasibility goal

Create a separate working derivative:

`GO-05AB_macro_corrected.blend`

whose macro segment proportions are brought into compatibility with the accepted W1 ARM **without**:
- changing C's immutable source;
- replacing topology;
- remeshing;
- procedurally generating a new body;
- shrinking/wrapping C onto the W1 surface;
- copying another race.

The question for this block is:

> Can C's real sculptural surface be re-proportioned to the accepted Gorrund macro skeleton cleanly enough that a later manual soft-tissue sculpt is credible?

Do not perform the later composition sculpt in 05AB.

## 4. Method

### Allowed

A temporary Blender armature, lattice, or equivalent macro-deformation scaffold may be used, provided the deformation is driven by explicit anatomical segments and joint centres.

Preferred:
- pelvis/root;
- spine/trunk;
- clavicle/shoulder anchors;
- upper arm;
- forearm;
- hand as rigid terminal;
- thigh;
- lower leg;
- foot as rigid terminal.

Hands, feet and head should be treated as rigid or near-rigid shape blocks wherever possible.

You may use scripts to:
- create the temporary rig/scaffold;
- identify / assign vertex groups;
- read W1 joint/landmark measurements;
- calculate bone transforms;
- verify metrics.

Do **not** use scripts to directly invent per-vertex final shapes.

The actual surface must be driven through the Blender deformation stack (armature/lattice/proportional segment transform), with smooth anatomical transition zones around joints.

### Forbidden

- Dyntopo;
- voxel remesh;
- topology replacement;
- SDF or primitive body generation;
- shrinkwrap to the W1 mesh as final geometry;
- direct scripted coordinate fitting to W1 vertices;
- nonuniform whole-body warp with no anatomical segmentation;
- copying the W1 surface;
- changing Grask or any other race.

## 5. Macro targets

The reference-body derivative should reproduce the accepted W1 ARM's macro relationships closely.

Use the existing AA0 method and any stronger accepted W1 skeletal landmarks available in the tooling.

At minimum:

### Limb / pelvis shares
- lowest fingertip: target **44.3 % of height**;
- crotch height: target **48.5 % of height**.

For this feasibility derivative, treat **±0.5 percentage points** as a diagnostic reproduction tolerance, not new biological canon.

The corrected Gorrund must not have greater relative reach than Grask E3.

### Segment logic
Do not achieve the numbers by moving the hands/feet alone.

The correction must come from credible changes to:
- humerus / forearm segment lengths and elbow/wrist positions;
- pelvis / hip placement;
- femur / tibia segment lengths and knee position.

Preserve terminal hand and foot scale unless the accepted W1 relationship clearly requires a later separate decision.

### Trunk
Do not force C's heroic soft-tissue depth to W1 in this block. Torso depth/breadth excess caused by muscle/fat is intentionally deferred to the later sculpt.

Only correct trunk length / pelvic seating needed for the macro skeleton.

## 6. Preservation checks

Before and after the macro deformation, report:

- topology identity;
- connected components;
- manifold/boundary/nonmanifold state;
- self-intersections;
- head dimensions / silhouette;
- hand dimensions;
- foot dimensions;
- digit counts;
- tail free portion;
- pelvis landmark continuity;
- elbow/knee/wrist/ankle continuity.

No head, hand or foot deformation beyond minor joint-transition effects is acceptable.

The tail root/gluteal fusion is deferred; do not fix it here.

## 7. Visual quality / deformation-artifact gate

Produce identical-camera:
- whole F / P / B / 3/4;
- headless/body-only F / P / B / 3/4;
- close shoulder/elbow/wrist;
- close pelvis/hip/knee;
- close ankle/foot;
- overlay or side-by-side with AA0 C and accepted W1 ARM at matched displayed height.

Reject the route if macro correction creates:
- rubber-hose limbs;
- collapsed joints;
- stretched/compressed hands or feet;
- pinched pelvis;
- obvious texture/surface shearing;
- stair-step joint transitions;
- major skin fold artifacts that cannot plausibly be cleaned by normal sculpting;
- new intersections.

## 8. Feasibility decision

### PASS

Return:

**05AB MACRO REPROPORTION FEASIBLE / READY FOR MANUAL COMPOSITION SCULPT**

only if:
- fingertip and crotch targets reproduce within the diagnostic tolerance;
- joint positions/segment relationships are credible;
- topology remains valid;
- terminal anatomy remains intact;
- deformation artifacts are bounded and sculpt-cleanable;
- the headless body now respects the accepted Gorrund-vs-Grask reach relationship.

If PASS, do **not** start the composition sculpt in the same block. Return the exact corrected scene/hash and a frozen macro-corrected baseline for the next order.

### FAIL

Return:

**05AB MACRO REPROPORTION NOT CREDIBLE / HUMAN SCULPTOR OR NEW NON-RODIN SOURCE REQUIRED**

if the above cannot be achieved without wholesale distortion.

Do not iterate indefinitely. Maximum:
- 2 deliberate macro-deformation checkpoints.

## 9. State

Until a 05AB PASS and later manual composition sculpt:
- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED;
- no LOW / blind final scoring / scaffold;
- no D4 / UE5 / production rigging / creator implementation.

## 10. Return

Commit:
`reviews/claude-rac-rm-ot-05ab-gorrund-macro-reproportion-feasibility-gate.md`

Evidence:
`reviews/rac-rmot05ab-evidence/`

Preserve all donor/AA0 history unchanged.
