# RAC RP2 — Grask retopology v002 production-optimization order

**Date:** 2026-10-24  
**Authority:** Tyler direct author ruling through ChatGPT after review of `GR_U_REF_RP2_retopo_v001.blend`.  
**Parent candidate:** `GR_U_REF_RP2_retopo_v001.blend`.  
**Parent gate:** `reviews/claude-rac-rp2-grask-retopo-v001-gate.md` (9be2e94).  
**Frozen anatomical source:** `GR_U_REF_RP2_SOURCE_3D_v005.blend`.  
**Frozen source authority:** `reviews/chatgpt-rac-rp2-grask-3d-source-v005-final-author-acceptance-freeze-order.md` (33e4aaf).  
**Production contract:** `specs/RAC_PRODUCTION_MESH_CONTRACT.md`.

## 1. Author ruling

`GR_U_REF_RP2_retopo_v001` is **not approved for production freeze**.

The v001 topology architecture is accepted as the correct direction.

The following v001 accomplishments are specifically approved and must be preserved:

- frozen v005 source integrity;
- v005 as sole geometry/anatomy authority;
- explicitly authored quad cage architecture;
- Grask-specific topology ownership;
- all-quad construction;
- deformation-loop architecture;
- hand/finger topology;
- foot/toe topology;
- facial/orbit/mouth topology direction;
- shoulder/axilla/girdle topology direction;
- pelvis/groin/glute topology direction;
- landmark framework;
- source asymmetry preservation;
- T-1/T-2/T-3/T-6/T-7 validation framework;
- seam-plan and tagged-loop framework.

The v001 problem is **not anatomy preservation**.

The problem is that the final production candidate was globally subdivided too far and therefore remains unnecessarily dense, while some local quads still have extreme aspect ratios / angles.

This order is a **production optimization and topology-quality pass**, not a retopology restart.

## 2. Mission

Create:

`GR_U_REF_RP2_retopo_v002.blend`

using the successful v001 authored cage/topology system as the parent architecture.

Goal:

> Produce the lowest practical deformation-ready Grask production mesh that preserves frozen v005 within all accepted tolerances, while improving local quad quality and correcting the production origin.

Do **not** rebuild the Grask from scratch.

Do **not** change frozen v005 anatomy.

Do **not** change topology architecture merely to chase a lower polygon count.

Do **not** invent a final game-wide vertex budget.

## 3. Why v001 is constrained

v001 final mesh:

- 628,738 vertices;
- 628,736 quads;
- ~1,257,472 triangle-equivalent faces.

Frozen v005 source:

- 590,764 vertices;
- 1,181,524 triangles.

Therefore v001 is a clean production-flow mesh, but it is not yet a meaningful production-density reduction.

The authored base cage is only about 9.8k quads, then globally Catmull-Clark subdivided ×3.

Approximate hierarchy:

- base cage: ~9.8k quads;
- ×1: ~39k quads;
- ×2: ~157k quads;
- ×3: ~629k quads.

v002 must determine the **lowest practical level / mixed-density solution** that still passes the production contract.

## 4. Density strategy — mandatory comparative test

Before choosing the v002 final density, generate and evaluate at minimum:

1. **Level A — ×1 candidate**
2. **Level B — ×2 candidate**
3. **Level C — mixed/selective-density candidate**, if needed

Do not automatically assume ×2 is correct.

### 4.1 Level A — ×1

Evaluate whether the ×1 topology can satisfy:

- T-1;
- T-2;
- T-3;
- T-6;
- T-7;
- deformation-loop minimums;
- creator-density ceilings;
- nail visibility;
- finger/toe/web preservation;
- face/orbit/mouth preservation;
- Grask girdle/chest/pelvis identity.

If ×1 passes all required gates and visual evidence, prefer it.

### 4.2 Level B — ×2

If ×1 cannot preserve identity/detail within contract, evaluate ×2.

Do not use ×2 merely because it is easier.

### 4.3 Mixed/selective density

If broad-body regions pass at ×1 but identity/deformation zones need more support, create a controlled mixed-density production mesh.

Allowed higher-density zones:

- face/orbits/mouth;
- ears;
- shoulder/axilla if required;
- hands/fingers/thumb;
- feet/toes/nails;
- other explicitly demonstrated Grask identity regions.

Preferred lower-density zones:

- broad trunk expanses;
- upper/lower limb shafts away from joints;
- large cranial expanses away from expression topology;
- broad back areas where silhouette and creator support remain safe.

Density transitions must be explicitly authored.

Do not create:
- random triangle fans;
- unstructured pole clusters;
- abrupt density cliffs;
- visible shading artifacts;
- loop dead-ends on deformation creases.

## 5. Selection rule

Choose the lowest-density candidate that satisfies **all** of the following:

1. frozen v005 visual identity;
2. T-1;
3. T-2;
4. T-3;
5. T-6;
6. T-7;
7. all required deformation loops;
8. creator-density requirements;
9. acceptable local quad quality;
10. zero catastrophic self-intersections;
11. production usability.

If a lower-density candidate fails, document exactly why and move upward only as needed.

The final report must show the comparison, not merely the selected result.

## 6. Frozen anatomy — no change

Preserve exactly the accepted v005 anatomy already carried successfully by v001:

### Whole body
- 218 cm stature;
- long-limb / short-torso organization;
- front-view Grask identity;
- girdle slope;
- shoulder width;
- neck/trapezius relationship;
- chest / sternum / keel organization;
- abdomen transition;
- waist / pelvis hierarchy;
- glutes;
- thigh/calf mass;
- limb proportions;
- accepted asymmetry.

### Head
- cranium;
- heavy brow;
- narrow eye opening;
- eyelid/orbit relationship;
- nose;
- cheeks;
- jaw;
- ears;
- head/neck relationship.

### Hands
- scale;
- palm mass;
- five digits;
- finger hierarchy;
- MCP/PIP/DIP placement;
- thick naturalized digit mass;
- web spaces;
- nails;
- thumb opposition;
- thumb/thenar integration.

### Feet
- scale;
- broad forefoot;
- heel/arch;
- plantigrade stance;
- hallux dominance;
- lesser-toe hierarchy;
- toe roots;
- toe joints;
- plantar contact;
- toenails.

No anatomy redesign is authorized.

## 7. Preserve v001 topology architecture

Keep the successful v001 edge-flow intent unless a local quality repair requires redirection.

Preserve:

- face/orbit/mouth ring topology;
- shoulder/axilla flow;
- Grask girdle support;
- elbow and wrist loops;
- palm / metacarpal flow;
- finger root and IP architecture;
- thumb branch;
- pelvis/groin split;
- gluteal flow;
- hip/knee/ankle loops;
- forefoot/toe architecture;
- landmark-support topology.

Do not revert to MPFB hm08.

Do not force a universal humanoid topology.

## 8. Quad-quality correction — mandatory

v001 technically passed manifold and deformation gates, but some local quads are too distorted.

v001 reported:

### Ears
- only ~82.4% of quads inside 45–135°;
- min angle ~12.2°;
- max angle ~166.7°;
- max aspect ~5.8:1.

### Hands
- min angle ~3.7°;
- max angle ~173.3°;
- max aspect ~30.75:1.

### Feet
- min angle ~1.1°;
- max angle ~179.4°;
- max aspect ~15.58:1.

### Trunk / limbs
- max aspect ~7.45:1.

These are **not acceptable as the preferred final production topology merely because T-4 is labeled a quality target**.

### Required repair priority

Focus on:

- finger web roots;
- toe web roots;
- nail-support transitions;
- thumb web;
- ear helix/rim;
- axillary fan;
- shoulder transition;
- groin / crotch split;
- density-transition regions.

### Target

Move materially closer to the contract T-4 targets:

- quad angles 45–135°;
- aspect <= 4:1 outside digit tips.

Do not damage anatomy to force every single quad inside the target.

If a small number of exceptions remain:
- list them individually or by bounded cluster;
- show them in wireframe;
- justify why they are preferable to an anatomy/deformation regression.

Do not hide extreme outliers inside aggregate percentages.

## 9. No sliver-quad loophole

The following fail v002 unless specifically justified by unavoidable tip geometry:

- near-zero-angle quads;
- near-180° quads;
- 10+:1 aspect quads in deformation/web regions;
- stretched strips crossing joint creases;
- pinched ear or web topology;
- projection-created foldbacks.

A clean manifold mesh with poor local deformation topology does not pass.

## 10. Production origin correction

v001 retained the frozen source coordinate frame and reported the pelvis root at approximately:

- X = +0.11 cm;
- plan Y/F offset approximately 5.72 cm from the contract root projection.

v002 must conform to the production mesh contract:

> origin = pelvis-root landmark projected onto the ground plane.

Apply a **single rigid translation only**.

Requirements:

- no rotation;
- no scale;
- no vertex-relative deformation;
- ground remains correct;
- stature unchanged;
- anatomy unchanged;
- source remains untouched.

Record:

- old origin;
- pelvis-root landmark;
- translation vector;
- new origin;
- post-translation bbox;
- verification that all inter-landmark distances are unchanged.

Because validation compares shapes, perform comparisons in a common frame / after undoing the rigid production-origin translation as appropriate.

Do not alter the frozen v005 source to match the production origin.

## 11. Vertex-count discipline

There is still **no final game-wide vertex budget**.

However:

> The final v002 must represent a meaningful production simplification relative to v001 unless Claude demonstrates with evidence that a lower-density solution cannot satisfy the accepted contract.

Do not keep ~629k vertices simply because it passes.

Do not chase an arbitrary low number.

The correct count is the lowest practical count that preserves:

- anatomy;
- deformation;
- creator flexibility;
- face topology;
- hand/foot detail;
- future LOD generation.

Report triangle-equivalent count as well as quad/vertex count.

## 12. Deformation zones

The v001 loop audit passed 69/69.

v002 must preserve or exceed the required minimums while removing redundant support loops where safe.

Required:

- neck >= 4;
- shoulder >= 5 + axillary fold;
- elbow >= 3 + crease;
- wrist >= 3;
- finger MCP support;
- finger IP >= 2;
- hip/groin/glute >= 5 + fold;
- knee >= 3 + crease;
- ankle >= 3;
- toe joints >= 2;
- face ring topology;
- jaw support.

Do not preserve excessive loops solely because ×3 subdivision created them.

The purpose is **necessary support**, not maximal loop count.

## 13. Creator-readiness

The v002 mesh must remain suitable for later:

- stature morphing;
- Narrow / Balanced / Broad frame;
- muscularity;
- composition/fat distribution;
- regional development;
- hand/foot size controls;
- sex-related soft-distribution controls;
- race-specific Grask morphs;
- facial customization.

Do not simplify the mesh into a single static-body shell that cannot support accepted creator ranges.

Use the contract density ceilings as **maximum mean edge lengths**, not instructions to subdivide to the smallest possible edges.

## 14. Projection / fitting

Projection remains allowed.

At the selected lower density:

- project to frozen v005;
- preserve region ownership;
- protect web spaces;
- protect nail planes;
- protect eyelids/lips;
- protect girdle/chest/pelvis;
- avoid shrinkwrap flattening;
- avoid ripples.

After each major topology change, rerun the relevant local deviation check.

## 15. Mandatory comparison evidence

Create a density-study package before finalizing v002.

### A. Density comparison table

For ×1, ×2, and mixed/selective candidate if created, record:

- vertices;
- quads;
- triangle equivalent;
- mean edge length by zone;
- T-1 results;
- T-2 results;
- T-3;
- T-6;
- T-7;
- loop audit;
- quad-quality statistics;
- self-intersections;
- PASS / FAIL with reason.

### B. Visual comparison

At minimum compare:

- v005 source;
- v001 final;
- ×1 candidate;
- ×2 candidate;
- selected v002.

Views:
- front;
- profile;
- rear;
- 3/4;
- head;
- shoulder/girdle;
- hand;
- foot.

Do not rely only on numerical tables.

### C. Wireframe comparison

Show:
- base authored cage;
- ×1;
- ×2;
- selected v002.

Focus on:
- face;
- shoulder;
- hand;
- groin;
- knee;
- foot.

## 16. Mandatory v002 evidence

For selected v002:

### Whole body
- source vs v002;
- identical-camera front/profile/rear/3/4;
- overlay;
- silhouette IoU.

### Head/face
- clay and wire;
- brow/orbit;
- mouth/jaw;
- ears.

### Girdle/torso/pelvis
- shoulder/axilla;
- chest;
- abdomen;
- pelvis/groin;
- glute.

### Hands
- palm;
- dorsal;
- thumb;
- web spaces;
- finger side;
- MCP/PIP/DIP;
- nails;
- wireframe close-ups.

### Feet
- top;
- sole;
- hallux;
- lesser toes;
- toe webs;
- nails;
- ground contact;
- wireframes.

### Quad quality
Provide a dedicated sheet showing:
- worst remaining angle quads;
- worst remaining aspect quads;
- ear repair;
- axilla repair;
- finger/toe web repair.

## 17. Validation gates

The selected v002 must pass all accepted production tolerances.

### T-1 general body
- median <= 0.5 mm;
- p95 <= 1.5 mm;
- max <= 3.0 mm.

### T-2 identity zones
- median <= 0.3 mm;
- p95 <= 0.8 mm;
- max <= 1.5 mm.

Identity zones include:
- head/face;
- ears;
- hands;
- feet;
- toes;
- nails;
- Grask-defining torso/girdle regions where appropriate.

### T-3
- stature +/-1.0 mm;
- bbox +/-2.0 mm per axis, evaluated with production-origin translation accounted for.

### T-6
- landmark target <=1.0 mm;
- none >1.5 mm;
- list every >1.0 mm.

### T-7
- front/profile/rear silhouette IoU >=0.995.

### Visual veto
Still active.

## 18. Technical gate

Final selected v002 must have:

- 1 intended body;
- 0 boundary edges;
- 0 non-manifold edges/vertices;
- 0 duplicate faces;
- 0 coincident duplicates;
- 0 degenerates;
- 0 n-gons;
- >=98% quads overall;
- 100% quads in deformation zones;
- consistent outward normals;
- 0 catastrophic self-intersections;
- no hidden shells;
- no accidental contact handles;
- no projection folds;
- production origin compliant with contract.

Triangles are allowed only outside deformation zones if a controlled density transition truly benefits the final mesh.

Do **not** maintain 100% quads at the cost of extreme sliver quads.

## 19. Pole and transition audit

Re-run pole inventory.

Required:
- no poles directly on joint crease lines;
- avoid poles within 2 loops of creases where practical;
- no high-valence cluster in web spaces;
- no uncontrolled pole chains through axilla/groin;
- density-transition poles must be clearly documented.

Provide wireframes with pole labels.

## 20. Source integrity

Frozen source must remain:

`GR_U_REF_RP2_SOURCE_3D_v005.blend`

with SHA-256:

`7bba8d2d5f081c077351b2e79e7e5fcce91b4f376cd6b2cfc76f1c2eb052ab14`

Verify before and after.

Any mismatch = STOP.

v001 remains preserved unchanged as provenance.

## 21. Deliverables

Create:

`GR_U_REF_RP2_retopo_v002.blend`

`GR_U_REF_RP2_retopo_v002.json`

`GR_U_REF_RP2_retopo_v002_landmarks.json`

Final gate:

`reviews/claude-rac-rp2-grask-retopo-v002-optimization-gate.md`

Evidence:

`reviews/rac-rp2-evidence/grask_retopo_v002_optimization/`

Include:

- density study;
- source-integrity record;
- topology report;
- quad-quality report;
- deviation report;
- silhouette report;
- landmark report;
- origin-correction record;
- loop audit;
- pole audit;
- visual sheets;
- wireframes;
- reproducibility tools.

Update:

- `reviews/claude-session-handoff.md`
- `specs/STATUS.md`

## 22. Acceptance checklist

Claude must explicitly PASS/FAIL:

### Source / ancestry
1. frozen v005 hash verified before;
2. frozen v005 unchanged after;
3. v001 preserved;
4. v002 derived from accepted v001 topology architecture + frozen v005 shape authority.

### Density
5. ×1 tested;
6. ×2 tested;
7. mixed/selective density evaluated if useful;
8. final selection is lowest practical passing density;
9. final count materially justified;
10. triangle-equivalent count reported.

### Anatomy
11. stature preserved;
12. silhouette preserved;
13. head/face preserved;
14. Grask front-view identity preserved;
15. girdle slope preserved;
16. torso/pelvis organization preserved;
17. hand anatomy preserved;
18. foot anatomy preserved;
19. nails preserved;
20. accepted asymmetry preserved.

### Topology
21. >=98% quads;
22. 100% quads in deformation zones;
23. 0 n-gons;
24. manifold/watertight;
25. loop minimums pass;
26. creator density passes;
27. no destructive density transitions;
28. pole placement passes;
29. extreme sliver quads corrected or individually justified;
30. T-4 quality materially improved from v001.

### Origin
31. pelvis-root production origin corrected by rigid translation only;
32. ground/stature/inter-landmark distances preserved.

### Validation
33. T-1 pass;
34. T-2 pass;
35. T-3 pass;
36. T-6 pass;
37. T-7 pass;
38. zero catastrophic self-intersections;
39. visual veto pass;
40. all evidence / sidecars complete.

## 23. Stop rule

After v002 and its full evidence package are complete:

**STOP FOR TYLER / CHATGPT REVIEW.**

Do not:
- freeze v002 automatically;
- rig;
- skin;
- build creator morphs;
- create final UVs/materials;
- build final LODs;
- export to UE5;
- begin another race.

Return exactly:

**RP2 GRASK RETOPO V002 OPTIMIZATION COMPLETE / READY FOR AUTHOR REVIEW**

Then STOP.
