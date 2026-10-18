# RAC RM-OT-05AW4 — final micro-finish: nail-edge bevel + lesser-toe projection

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05AW3.
**Date:** 2026-10-18.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05aw3-gorrund-final-nail-finish-gate.md` (3b73e46).
**Purpose:** Resolve the only two remaining AW3 visual misses without redesigning the nails.

## 1. Ruling

05AW3 is technically clean and has the desired:
- visible profile projection;
- mild downward curl;
- tapered feline free edge;
- clean continuous nail surfaces;
- preserved foot/heel/body geometry.

The remaining issues are:
1. side-wall / inlay read from the plate step wall;
2. lesser-toe projection 1.25–1.42 mm versus the 1.5 mm floor.

This order authorizes **one final micro-finish only**.

Do not rebuild the nail plates.

## 2. Source

Start only from:

`GO-05AW3_C.blend`
SHA-256:
`1d68c9f5e496ce0076318a96220667040b5a4b467dc380d8c49a8e354823cc78`

Treat this as the exact technical baseline.

## 3. Frozen scope

Do not alter:
- nail root position;
- nail overall planform;
- big-toe projection/curl except tiny continuity smoothing;
- toe shape;
- toe spacing;
- foot dimensions;
- heel stance;
- ankle;
- lower leg;
- body;
- head;
- tail.

Only:
- the nail plate’s own outer side edge;
- the distal lesser-toe nail tips;
may be modified.

## 4. Stage A — bevel / soften the plate side wall itself

The AW3 skin-ring Inflate did not solve the incised-outline read.

Work on the **plate edge itself**, not the surrounding toe skin.

Target:
- reduce the abrupt ~1–1.7 mm step-wall appearance;
- preserve a readable nail boundary;
- convert the edge from a trench-like outline to a softer convex keratin-to-skin transition.

Preferred UI operations:
- restrained Smooth / Surface Smooth on the outer ~0.5–0.8 mm nail plate edge;
- tiny local bevel-like vertex relaxation;
- tiny local edge slide / edge rotation if required for continuity.

Do not flatten the whole plate.

### Stage A gate
PASS only if:
- boundary remains visible;
- dark incised/trench read is materially reduced in 3/4;
- nail still sits slightly proud of toe;
- no new dent, shelf, or blur;
- technical gate remains clean.

## 5. Stage B — lesser-toe projection correction

Increase only L2–L4 and R2–R4 distal projection.

Target additional forward displacement:
- approximately **+0.15 to +0.25 mm** per lesser nail.

Goal final projection:
- >= **1.50 mm**
- <= **1.70 mm**

Keep their current downward curl essentially unchanged.

Do not alter big toes unless needed for symmetry read.

Preferred:
- reuse the same Hook / weighted distal groups;
- increase only lesser-toe forward amount;
- no global nail scaling.

## 6. Cleanup budget

One tiny cleanup pass is allowed after Stage B if needed:
- side-edge smooth;
- symmetry touch;
- removal of the soft crease above R3.

No fourth redesign cycle.

## 7. Technical gate

Required:
- 0 opened seams;
- 0 self-intersections;
- 0 folded/flipped faces against local surface;
- 0 degenerates;
- 1 welded component;
- 0 boundary;
- 0 non-manifold;
- genus unchanged;
- no new toe contact;
- no nail/ground intersection;
- no nail/adjacent-toe intersection;
- no movement outside nail + immediate nail-bed support;
- ankle drift 0.0 mm target;
- accepted foot width unchanged;
- total foot length remains within **3.5 mm** of 05AV;
- heel stance unchanged.

## 8. Visual gate

PASS only if:
- crack/chip/split read remains gone;
- side-wall groove/inlay read is materially reduced;
- nail still has a clear readable outline;
- plate sits slightly proud of toe;
- all nails show profile projection;
- lesser-toe projection is at least 1.5 mm;
- mild curl remains;
- taper remains feline;
- no exaggerated hook/talon;
- both feet are coherent.

## 9. Output

If PASS, freeze:

`GO-05AW4_nails_final.blend`
`GO-05AW4_nails_final.glb`

Record hashes.

## 10. Evidence

Return:

`reviews/claude-rac-rm-ot-05aw4-gorrund-final-microfinish-gate.md`

Evidence:

`reviews/rac-rmot05aw4-evidence/`

Include:
- AW3 vs AW4 front / top / 3-4 / profile;
- close side-wall comparisons;
- per-nail final projection table;
- technical gate;
- protected displacement;
- final foot/heel metrics;
- whole-body confirmation.

## 11. Decision

### PASS

Return:

**05AW4 FINAL NAIL MICRO-FINISH PASS / READY FOR FINAL GORRUND CLOSURE REVIEW**

Then STOP 05AW4.

### FAIL

Return:

**05AW4 FINAL MICRO-FINISH FAILED / AUTHOR REVIEW REQUIRED**

Do not continue to closure.

## 12. State

- Gorrund BODY COMPOSITION: AUTHOR ACCEPTED / FROZEN
- Head share: AUTHOR APPROVED / FROZEN
- Tail root: AUTHOR APPROVED / FROZEN
- Foot size + heel stance: AUTHOR APPROVED / FROZEN
- Toenail morphology: FINAL MICRO-FINISH IN PROGRESS
- RM-OT-05: OPEN
- Stage C Gorrund blocker: BLOCKED
- Grask E3: FROZEN
