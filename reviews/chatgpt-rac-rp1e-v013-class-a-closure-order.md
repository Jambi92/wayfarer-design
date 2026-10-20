# RAC RP1E — v013 representable Class-A closure and decision-gate order

**Date:** 2026-10-20  
**Authority:** Tyler-authorized autonomous continuation through ChatGPT.  
**Parent order:** `reviews/chatgpt-rac-rp1e-nonlocal-subcage-rebuild-order.md` (a2f5ee5).  
**Latest checkpoint:** `reviews/claude-rac-rp1e-nonlocal-subcage-rebuild-gate.md` (34eeaa7 / status d4ff3a4).

## 1. Purpose

Continue the existing RP1E non-local rebuild.

This order does **not** replace the parent contract. It narrows the next session to one objective:

> **Clear every remaining representable/open Class-A defect that can be repaired without changing the frozen source anatomy, integrate the best repairs into one v013 production-cage candidate, import/verify it in Blender, run the full L1→L4 gate, and return an actual decision line.**

Do not return another open-ended "checkpoint / work continues" report unless an external tool/safety interruption makes completion impossible.

## 2. Authoritative starting point

Start from the promoted v012 state:

### PC
`GO_U_REF_RP1E_retopo_v012.blend`

Recorded SHA:
`25e9b53c…7f9c`

### Cloud design
`reviews/rac-rp1e-evidence/designs/design_v012.npz`

Recorded state:
- 5043 V;
- 5170 F;
- 4912 quads;
- 258 tris;
- genus 0;
- 1 component;
- 0 boundary;
- 0 non-manifold;
- consistent orientation;
- 0 coarse self-intersections.

Preserve v009–v012 unchanged.

## 3. Already-successful regions are frozen unless continuity requires a tiny boundary adjustment

Do not reopen successful rebuilds merely for cosmetic uniformity:

- left foot major rebuild: keep the L4 self-x = 0 result;
- right foot major rebuild: keep its large improvement;
- cleared R-hand web 3/4 pocket;
- cleared L thumb-web main pocket;
- both nostril cavities;
- cleared mouth-corner pockets;
- successful L axilla z~153 depth recovery;
- tail-root accepted region;
- successful ear/jaw/mouth topology already present.

Any modification to one of these must be justified by a remaining Class-A defect in that exact region.

## 4. Deferred source micro-cavities remain deferred

Do not spend this session trying to force topology into:

1. the proven sealed L-hand web tunnels;
2. the enclosed zero-gap L-axilla void behind the pinch.

Keep them measured and report them later.

They are **not yet waived**.

Do not distort visible anatomy to eliminate them.

## 5. Remaining Class-A closure sequence

Proceed in this order.

### C1 — Right thumb-web fin

The v012 evidence shows this is a thin positive web membrane, not a slit.

Do **not** repeat the rejected direct fin-band insertion into 2–5 cm surrounding faces.

Instead:

1. Refine the surrounding thumb-base / palm faces into a graded support ring or nested support loops.
2. The refined attachment topology must reduce the scale jump before the fin is inserted.
3. Insert the fin/web band only after the surrounding support mesh passes:
   - coarse self-x = 0;
   - L1 no fold at the stitch;
   - preserved thumb/palm proportions.
4. The final fin must represent the visible source membrane without thickening it into a block.

Reject any attempt that clears deviation but creates large L1 fold counts.

### C2 — Philtrum bottom, upper lip, chin lobe

Repair the remaining T-2 facial misses using support topology, not a single deep tip.

Required:
- extend/deepen the philtrum slot to the actual lower floor;
- add a support loop/ring where the upper lip overhang requires it;
- add support topology under the chin lobe if needed.

Preserve the accepted muzzle profile, lip silhouette, nose width and chin shape.

### C3 — Mouth-line contact cluster

The new mouth band created a positive-normal fold/contact left of the corner.

Before editing:
- measure source opposed-sheet gap at the exact cluster;
- determine whether the source itself is a zero-width lip contact.

If source gap is effectively zero and the product follows the visible lip crease without bridging an open cavity:
- classify it as a **provisional B lip-contact candidate**;
- do not distort the lips to create artificial separation.

If source gap is nonzero:
- terminate/refine the mouth band with a proper crease row and clear the Class-A fold.

### C4 — Ear-rim and nose-ridge residual folds

Add only the support loops needed to clear the remaining exposed/positive-normal folds and T-2 misses.

Do not redesign the ear identity.

Target the specific remaining rim/knob clusters.

### C5 — Left axilla residual visible folds

Repair:
- the z153 pocket contact/fold;
- pinch-mouth fold;
- open/exposed points around approximately (24.2, -39.0, 143.6) and (23.3, -40.3, 149.6) that are **not** inside the deferred zero-gap void.

Do not chase the sealed void.

Use local support rings/column refinement rather than deep tip overshoot.

### C6 — Right axilla slit tips

Add or refine support columns/slit-band topology so the open tips survive L1.

Do not change shoulder/arm macro anatomy.

### C7 — Right groin ridge end

Use a bounded ridge-support loop or termination topology so the sharp source ridge end is represented without creating a crease fold.

Preserve genital/perineal anatomy.

### C8 — Natal-cleft nub classification and action

First determine from slices whether the nub is:
- externally visible connected anatomy;
- a tiny source micro-artifact / nearly sealed loop.

If exterior anatomy:
- represent it with support topology.

If it is demonstrably non-visible micro-artifact:
- do not mutate the source;
- classify it for the later author ruling with screenshots and measurements.

### C9 — Remaining open hand/foot shape misses

After C1–C8, repair only residual **open/exposed** shape misses that are still above the applicable tolerance.

Examples:
- L-hand palm/crease/wrist/open thumb-tip misses;
- exposed toe tips;
- small open R-toe residuals.

Do not disturb the now-clean L-foot cleft topology.

## 6. Attempt budget

Avoid another indefinite topology loop.

For each C1–C9 feature group:

- maximum **2 serious support-topology redesign attempts** after diagnosis;
- diagnostic parameter sweeps that do not create promoted geometry do not count as a serious attempt;
- if two genuine rebuilds fail for the same physical reason, stop treating it as "more iteration needed" and classify it as blocked with evidence.

A "serious rebuild" means the support topology itself was changed in the manner authorized by the parent order and tested at least through L1.

## 7. L1 survival is mandatory before promotion

For every rebuilt open pocket/fin/ridge:

Before full L4 simulation, demonstrate at L1 that:
- the feature still exists;
- the limit surface enters/follows the intended source shape;
- there is no new fold at the attachment;
- there is no cross-sheet ownership error.

If it disappears or folds at L1, reject it before UI import.

## 8. Build one consolidated v013 candidate

Do not promote a succession of partial PC cages.

Cloud experimentation may use as many temporary design tags as needed within §6.

Once the best C1–C9 repairs are selected:

Freeze one consolidated design:

`design_v013.npz`
`design_v013_col.npy`
`design_v013_info.json`
`fsm_v013.txt`

Record:
- V/F counts;
- quad/tri counts;
- topology;
- hashes;
- parent;
- exact repair list.

Required cloud pre-import gate:
- 1 component;
- 0 boundary;
- 0 non-manifold;
- genus 0;
- 0 coarse self-intersections;
- consistent normals;
- no unintended face bridge across an exterior opening.

## 9. UI import and provenance

Import v013 through the normal Blender UI under the existing transcription ruling.

Create:

`GO_U_REF_RP1E_retopo_v013.blend`

Do not overwrite v012.

Verify:
- design/import positional deviation <= 0.10 mm;
- topology/faces identical by intended mapping;
- 0 coarse self-x;
- 0 boundary;
- 0 non-manifold;
- 1 component;
- genus 0;
- normals consistent.

If UI import fails provenance, fix the import itself; do not silently edit geometry away from the frozen design.

## 10. Full progressive gate

After v013 is verified on the PC, run:

**L1 → L2 → L3 → L4**

Record for each level:
- total self-x pairs;
- self-x by zone;
- positive-normal folds vs opposed-sheet contacts;
- source→product deviations by contract zone;
- product→source maxima;
- source gap;
- face size;
- amplitude;
- openness;
- cross-sheet ownership errors.

Also rerun:
- T-1;
- T-2 identity zones;
- T-3;
- nail preservation checks where affected;
- any T-6/T-7 checks needed to prove these local rebuilds did not disturb global anatomy.

## 11. Residual classification at v013

Every remaining L4 self-intersection/deviation cluster must be assigned exactly one of:

### A — representable/open production defect
A visible/open feature is still missed, bridged, folded, or incorrectly projected.

### B — provisional source-consistent micro-contact
Allowed classification only when:
- exterior visible shape is correct;
- no cross-sheet ownership mistake;
- no visible fold/inversion;
- contact is inside a source web/slit/fused-contact region;
- source gap is at/below relevant final face scale or the source is intentionally fused/contacting;
- removing the contact would require anatomy distortion.

### D — deferred sealed source micro-cavity
For the already-approved deferred cases and any newly proven truly sealed non-visible cavity.

Provide exact evidence; do not expand this category casually.

## 12. Required return — no ordinary checkpoint

Return exactly one of these substantive outcomes.

### Outcome 1 — desired

If no representable/open Class-A defect remains:

**RP1E OPEN CLASS-A CLEAR / MICRO-CONTACT FINAL RULING REQUIRED**

Then provide:
- exact B pair count by cluster;
- exact D/deferred list;
- which B contacts are deformation-zone contacts;
- source gap vs face scale;
- amplitude/openness;
- exterior visibility;
- whether a B contact could affect skinning;
- recommended final acceptance rule.

STOP.

### Outcome 2 — full pass

If zero self-intersections and all parent gates pass without any waiver:

**RP1E GORRUND PRODUCTION RETOPO PASS / READY FOR FAMILY-PILOT AUTHOR REVIEW**

STOP.

### Outcome 3 — proven block

If one or more open Class-A features remain after the authorized genuine support-topology attempts:

**RP1E NON-LOCAL SUB-CAGE REBUILD BLOCKED / AUTHOR DECISION REQUIRED**

For every blocked feature show:
- source dimensions;
- v012 baseline;
- attempt 1 topology and L0/L1/L4 result;
- attempt 2 topology and L0/L1/L4 result;
- why further topology would require source-anatomy change or a projection-stack contract change.

STOP.

Do not return "checkpoint, work continues" after completing this order.

## 13. Contract / project state

No relaxation is authorized here.

Until a later explicit ruling:
- 1 component;
- 0 boundary;
- 0 non-manifold;
- genus 0;
- 0 self-intersections;
- 0 degenerates;
- quad-dominant;
- T-1 PASS;
- T-2 PASS;
- T-3 PASS;
- T-6 PASS;
- T-7 PASS;
- nails PASS;
- visual veto clear.

No RP2.
No rigging.
No creator implementation.
No UE5 production implementation.

## 14. Return files

Update:
- `reviews/rac-rp1e-evidence/RP1E_progress.md`
- `reviews/claude-session-handoff.md`
- `specs/STATUS.md` only when the substantive gate is known.

Return:

`reviews/claude-rac-rp1e-v013-class-a-closure-gate.md`

Evidence:

`reviews/rac-rp1e-evidence/`
