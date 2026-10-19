# RAC RP1E — authorize non-local sub-cage rebuild for remaining open Class-A pockets

**Date:** 2026-10-19  
**Authority:** Tyler-authorized autonomous continuation through ChatGPT.  
**Parent order:** `reviews/chatgpt-rac-rp1e-class-a-residual-recovery-order.md` (4e2b1a9).  
**Returned gate:** `reviews/claude-rac-rp1e-class-a-recovery-gate.md` (06a9162).  

## 1. Author ruling

Continue RP1E.

The previous order's "bounded local repair" scope is now explicitly widened.

Claude is authorized to perform **non-local rebuilds of the affected hand, foot, muzzle and axilla sub-cages** where the evidence shows that local crease insertion cannot survive the Catmull-Clark limit surface and projection stack.

This does **not** reopen the successful trunk, limb shafts, tail body, accepted head silhouette, or other already-passing cage regions.

Do not change the frozen anatomy source.

Do not start RP2.

## 2. Authoritative starting cage

The authoritative PC cage is:

`GO_U_REF_RP1E_retopo_v011.blend`

Recorded SHA-256:
`5792e5d9…1857`

Design source:

`reviews/rac-rp1e-evidence/designs/design_v011.npz`

Recorded design state:
- 3475 vertices;
- 3605 faces;
- 3341 quads;
- 264 tris;
- closed;
- manifold;
- genus 0;
- one component;
- consistent normals;
- 0 coarse self-intersections.

Preserve v009, v010 and v011 unchanged.

Every rebuilt candidate must become a new design/version and a new PC .blend after normal UI import/provenance verification.

## 3. Source-anatomy ruling

The frozen source remains authoritative and unchanged.

### 3A. Do not fill or edit the source

Do not "solve" a retopo problem by:
- filling a source cavity;
- separating a fused source contact;
- deleting a source fold;
- flattening a source feature;
- changing the accepted anatomy.

### 3B. Deferred sealed-source micro-cavities

The following are recognized as **deferred source-micro-cavity cases** for this rebuild order:

1. sealed L-hand web tunnels demonstrated as closed source slice loops;
2. the enclosed L-axilla zero-gap void behind the pinch.

Do not spend additional topology cycles trying to force production faces into a cavity that has no usable exterior opening at production scale.

These are **not yet accepted as final Class-B exceptions**. They are simply removed from the active Class-A rebuild workload until the open, representable defects are cleared.

They must remain measured and reported at the next gate.

### 3C. Nostrils are not deferred

The nostril slits are facial identity geometry and open to the exterior.

They remain Class A.

The fact that the slits are approximately 1 mm wide does not authorize their removal.

The muzzle/nose sub-cage may be rebuilt at a locally finer coarse resolution so that the production limit surface can represent the nostril openings without collapsing them.

### 3D. Natal-cleft nub

Do not delete or fill the natal-cleft nub.

Attempt to preserve it if it can be represented as part of the posterior/pelvis sub-cage without destabilizing the tail-root/natal-cleft region.

If evidence shows it is a sealed/non-visible source micro-artifact rather than exterior anatomy, classify it separately at the next author gate instead of changing it silently.

## 4. Why broader rebuild is authorized

The evidence from 06a9162 establishes a repeatable mechanism:

- at L1, Catmull-Clark limit-surface evaluation retracts a pocket tip toward its neighbours;
- the first projection then snaps to the mouth/wall instead of the intended pocket floor;
- later levels cannot recover the cavity;
- local overshoot large enough to compensate causes coarse self-intersection.

Therefore the remedy must change the **coarse support topology**, not merely push the same local tip deeper.

For the remaining open pockets Claude may rebuild the entire local sub-cage back to a clean attachment ring so that:
- pocket depth is represented by multiple support rings;
- the limit surface naturally enters the pocket;
- no extreme tip overshoot is required;
- ownership remains unambiguous.

## 5. Rebuild scope and priority

Proceed in this order.

### R1. Left foot — toe cleft 3

Mandatory first target:
- open L toe cleft 3 around approximately (31.3, -54.8, 3.6) cm;
- current max deviation approximately 11.4 mm;
- current A self-x cluster approximately 97 pairs.

Replace as much of the local toe-3/toe-4 base topology as necessary.

Requirements:
- explicit saddle/web floor;
- multiple support loops before the digit tubes;
- preserve toe lengths, width, nail-bearing distal surfaces, and the four-free-toe source anatomy;
- do not disturb the fused fifth-toe source condition.

Do not accept the v12b local-crease result that increased self-x.

### R2. Right hand — web 3/4 and remaining open web pockets

Rebuild the relevant palm/digit-base sub-cage from a clean palm ring if needed.

Required:
- represent the open web 3/4 pocket;
- preserve five-digit anatomy and digit proportions;
- preserve nail-bearing distal surfaces;
- do not force separation of the known fused-source contact;
- use support topology that survives the L1 limit surface.

### R3. Thumb webs / remaining open hand clefts

Repair open, representable thumb-web and inter-digit pockets on both hands.

The sealed L-hand tunnels from §3B are deferred and must not drive the rebuild deeper than the actual exterior source opening.

### R4. Muzzle / nose

Rebuild the necessary local muzzle/nose sub-cage to represent:
- both nostril slits;
- philtrum slot;
- any remaining mouth-line pocket residual still over T-2.

A locally denser **coarse** cage is allowed in this identity region.

Preserve:
- muzzle silhouette;
- nose width/projection;
- lip shape;
- accepted facial identity.

Do not use a one-tip pocket topology if the limit-surface evidence shows it will retract out of the slit.

Use mouth/nostril-specific support loops or slit-wall rings that remain inside the openings at L1.

### R5. Left axilla z~153 open crevice and residual pinch-mouth fold

Rebuild the local axilla slit band/columns where needed.

Target:
- open z ~153 wedge crevice;
- residual pinch-mouth fold.

The sealed zero-gap void behind the pinch is deferred under §3B and must not be chased by distorting the visible axilla surfaces.

### R6. Remaining representable open residuals

After R1-R5:
- R axilla tips;
- narrow R toe clefts;
- R groin crease end;
- exposed chin/ear-rim/toe-tip shape misses;
- natal-cleft nub if technically representable under §3D;
- isolated positive-normal folds that are actual product folds.

## 6. Topology budget / method

There is no arbitrary vertex-count ceiling for these local rebuilds.

The cage must remain production-reasonable and quad-dominant, but **correct support topology takes precedence over preserving the previous local vertex count**.

Allowed:
- cloud-authored sub-cage redesign;
- additional coarse support rings;
- local 6- or 8-vertex cross-sections;
- dedicated saddle/web topology;
- local ring-count increase;
- locally denser facial identity topology;
- File > Import through Blender UI under the existing provenance ruling;
- UI join/stitch/merge at clean attachment boundaries.

Forbidden:
- automatic remeshing;
- voxel remesh;
- QuadriFlow;
- broad source shrinkwrap as topology author;
- scripted final shape authoring inside Blender;
- changing accepted source anatomy;
- replacing successful unrelated cage regions.

## 7. Design requirement before UI import

For each rebuilt region, the cloud design must first demonstrate:

- 0 coarse self-intersections;
- 0 boundary after intended body integration;
- 0 non-manifold;
- genus remains 0 globally;
- consistent orientation;
- no face bridging an exterior opening;
- source feature represented in diagnostic slices at cage/limit-surface level;
- L1 test shows the pocket/slit survives the limit surface before doing a full L4 run.

A local design that already loses the cavity at L1 is rejected before UI import.

## 8. UI import / provenance

Continue using the authorized File > Import workflow.

For each promoted design:
- new artifact name;
- frozen design hash;
- new versioned .blend;
- import-vs-design max positional deviation <= 0.10 mm;
- faces/topology identical by intended index mapping;
- 0 coarse self-x;
- 0 boundary / 0 non-manifold;
- one component;
- genus 0;
- normals consistent.

Never overwrite v011.

## 9. Progressive gate

For each serious candidate, test L1 before full progression.

Once all R1-R6 open Class-A rebuilds are in one credible cage, run the complete:

L1 -> L2 -> L3 -> L4

Record at each level:
- total self-x;
- self-x by zone;
- cross-sheet ownership;
- source->product deviation;
- exposed/open residuals;
- source gap;
- final face size;
- amplitude;
- T-1/T-2 status.

## 10. Success criterion for this order

The target is to clear **all representable/open Class-A defects**.

Do not require the deferred sealed micro-cavities from §3B to be represented in this order.

At the next checkpoint classify all residuals into:

### Class A
A representable/open production defect remains.

### Provisional Class B
A hidden source-consistent contact inside a slit/web/fused-contact region where the production cage follows the visible anatomy and removing the contact would require anatomy distortion.

### Deferred source micro-cavity
Specifically the §3B cases, plus any newly proven truly sealed source cavity supported by slice evidence.

## 11. Stop logic

### If representable Class-A defects are cleared

Return:

**RP1E OPEN CLASS-A CLEAR / MICRO-CONTACT FINAL RULING REQUIRED**

Include exact residual counts and the complete proposed B/deferred list.

STOP. Do not make the final waiver yourself.

### If the entire unchanged parent contract reaches 0 self-intersections and all other gates pass

Return:

**RP1E GORRUND PRODUCTION RETOPO PASS / READY FOR FAMILY-PILOT AUTHOR REVIEW**

STOP.

### If a remaining open Class-A feature still cannot be represented after a genuine support-topology rebuild

Return:

**RP1E NON-LOCAL SUB-CAGE REBUILD BLOCKED / AUTHOR DECISION REQUIRED**

Show:
- the rebuilt topology;
- L0/L1/L4 slices;
- source opening dimensions;
- cage face scale;
- why further topology cannot solve it without source-anatomy change.

## 12. Final contract is otherwise unchanged

Until a later explicit author ruling:
- 1 component;
- 0 boundary;
- 0 non-manifold;
- genus 0;
- 0 self-intersections;
- 0 degenerates;
- quad-dominant contract;
- T-1 PASS;
- T-2 PASS in all identity zones;
- T-3 PASS;
- T-6 PASS;
- T-7 PASS;
- all nails PASS;
- visual veto clear.

No RP2, rigging, creator implementation, or UE5.

## 13. Return

Update:
- `reviews/rac-rp1e-evidence/RP1E_progress.md`
- `reviews/claude-session-handoff.md`

Return the next decision report as:

`reviews/claude-rac-rp1e-nonlocal-subcage-rebuild-gate.md`

Evidence remains under:

`reviews/rac-rp1e-evidence/`
