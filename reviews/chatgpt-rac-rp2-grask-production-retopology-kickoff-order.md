# RAC RP2 — Grask production retopology kickoff / execution order

**Date:** 2026-10-24  
**Authority:** Tyler direct author authorization through ChatGPT.  
**Program:** RAC Retopology / Rig-Prep — RP2 Grask production-mesh pilot.  
**Frozen anatomical authority:** `GR_U_REF_RP2_SOURCE_3D_v005.blend`.  
**Freeze authority:** `reviews/chatgpt-rac-rp2-grask-3d-source-v005-final-author-acceptance-freeze-order.md` (33e4aaf).  
**Freeze source SHA-256:** `7bba8d2d5f081c077351b2e79e7e5fcce91b4f376cd6b2cfc76f1c2eb052ab14`.  
**Freeze GLB SHA-256:** `81f872e7dd2c3d8e92623273bc50d8abbcc24acd251948421c2f2916bc0cc548`.  
**Frozen geometry hash:** `2697929d90c9ed708997a594502a4d5edeaebb8f4ae39deefcc0802dc7c1d7bc`.  
**Production contract:** `specs/RAC_PRODUCTION_MESH_CONTRACT.md`.  
**Master plan:** `reviews/chatgpt-rac-retopology-rigprep-master-plan.md`.

## 1. Author authorization

Tyler authorizes the next Grask stage:

> **BEGIN RP2 GRASK PRODUCTION RETOPOLOGY.**

The anatomical source is finished.

Do not reopen, resculpt, or reinterpret the frozen v005 anatomy.

The job now is to create a clean, quad-dominant, deformation-ready, creator-ready production topology that reproduces the frozen v005 source within the accepted production tolerances.

This order supersedes all earlier RP2 stop rules that blocked production retopology.

It does **not** authorize:
- final rigging;
- final skin weighting;
- creator morph production;
- UE5 implementation;
- final UV/material production;
- final LOD policy;
- another race.

## 2. Source authority — critical supersession

For RP2 Grask, the old RP0 inventory entry `GR5DE3` / MPFB E3 is now **historical provenance and constraint evidence only**.

It is **not** the retopology shape source.

The authoritative Grask production parent is now:

`GR_U_REF_RP2_SOURCE_3D_v005.blend`

The v005 author freeze supersedes the earlier RP0 Grask source recommendation wherever the two conflict.

Do not fit the production mesh back toward GR5DE3 merely to regain MPFB-family topology.

Do not force v005 onto the old hm08 topology if that changes the accepted anatomy.

The old Grask Stage C / W2 / E3 records remain useful for:
- provenance;
- race-specific identity checks;
- prior joint/landmark context;
- front-view constraints.

But **v005 wins on geometry and anatomy**.

Do not rewrite historical RP0 reports. Record the supersession in the new RP2 sidecar, gate, handoff, and status.

## 3. Output lineage

Start a clean retopology lineage:

`GR_U_REF_RP2_retopo_v001.blend`

Sidecars:

`GR_U_REF_RP2_retopo_v001.json`

`GR_U_REF_RP2_retopo_v001_landmarks.json`

Do not reuse or overwrite the earlier rejected/superseded RP2 production v001-v006 files.

Those remain provenance only.

Store the working production file under the contract-compliant Grask RP2 production folder.

The frozen source remains read-only.

## 4. Source immutability gate

Before any geometry work:

1. locate the exact frozen v005 source;
2. verify the BLEND SHA-256 equals:
   `7bba8d2d5f081c077351b2e79e7e5fcce91b4f376cd6b2cfc76f1c2eb052ab14`;
3. verify source geometry hash where practical:
   `2697929d90c9ed708997a594502a4d5edeaebb8f4ae39deefcc0802dc7c1d7bc`;
4. record file path, Blender version, transforms, dimensions, topology statistics and source hash;
5. never save over the source.

At the end:
- hash the source again;
- prove it is unchanged.

Mismatch = STOP.

## 5. Retopology method — HYBRID, anatomy-first

Use a **hybrid production-retopology method**.

### 5.1 Automated topology is allowed only as a broad-body seed

Claude may use an automatic quad-remesh / field-aligned remesh as a starting point for broad, low-risk regions such as:
- large trunk expanses;
- broad limb shafts;
- non-critical cranial expanses away from face/orbits/ears.

It is a **seed**, not an accepted final topology.

Do not accept automatic flow merely because it is clean.

### 5.2 Manual / explicitly authored topology is mandatory in critical zones

Manually construct, redirect, or repair edge flow for:

- face;
- orbit / eyelids;
- mouth / jaw;
- ears;
- neck base;
- clavicle / scapular / shoulder girdle;
- shoulder / axilla;
- chest keel / front-view Grask identity flow;
- abdomen transition / accepted shading-band ownership;
- elbows;
- wrists;
- palm / metacarpal block;
- thumb root / thenar;
- all finger roots and finger joints;
- pelvis / groin;
- gluteal fold;
- hips;
- knees;
- ankles;
- forefoot;
- hallux;
- lesser-toe roots and joints;
- all nail-bearing digit tips.

If an automatic seed fights the v005 anatomy, discard or rebuild that local topology.

### 5.3 No source-shape compromise for topology convenience

Do not:
- narrow the shoulders;
- normalize the torso toward a human base;
- straighten the girdle slope;
- reduce joint visibility;
- simplify the pelvis organization;
- thin or humanize the hands;
- simplify the large feet;
- remove toe or finger mass;
- alter face/head identity;
- symmetrize away accepted source shape;
- reopen the old MPFB appearance.

Topology serves anatomy, not the reverse.

## 6. Frozen anatomical identity

The following v005 traits are immutable during retopology:

### Whole body
- 218.000 cm stature;
- accepted long-limb / short-torso organization;
- accepted whole-body silhouette;
- shoulder width;
- girdle slope;
- neck/trapezius relationship;
- ribcage / waist / pelvis hierarchy;
- glute and thigh mass;
- calf mass;
- arm and leg proportions;
- front-view Grask identity.

### Head
- cranium;
- heavy brow;
- accepted eye opening / eyelid relationship;
- nose;
- cheeks;
- jaw;
- ears;
- head-to-neck transition.

### Hands
- overall scale;
- five digits;
- palm mass;
- finger hierarchy;
- MCP/PIP/DIP locations;
- naturalized thick Grask digit mass;
- non-cylindrical digit planes;
- web architecture;
- ordinary nails;
- thumb opposition;
- thumb/thenar integration.

### Feet
- plantigrade stance;
- overall scale;
- broad forefoot;
- heel / arch;
- five toes;
- hallux dominance;
- lesser-toe hierarchy;
- toe roots / joint architecture;
- plantar contact;
- ordinary toenails.

The production mesh may simplify topology, not anatomy.

## 7. Symmetry policy

Topology may be bilaterally symmetric where doing so improves production consistency.

**Shape must still match frozen v005.**

Do not force the projected result into geometric mirror symmetry if v005 contains accepted asymmetry.

If symmetric topology is used:
- project each side independently to v005;
- report left/right shape deviation;
- preserve source asymmetry where measurable/visible.

No anatomy-changing symmetrization is authorized.

## 8. Topology contract

Final v001 candidate must satisfy `specs/RAC_PRODUCTION_MESH_CONTRACT.md`.

At minimum:

- 1 intended connected body;
- 0 boundary edges;
- 0 non-manifold edges or vertices;
- 0 hidden shells;
- 0 duplicate/coincident vertices;
- 0 degenerate faces;
- consistent outward normals;
- 0 n-gons;
- quad-dominant overall: **>= 98% quads**;
- **100% quads inside deformation zones**;
- triangles only outside deformation zones and only for justified density transitions;
- valence-3 and valence-5+ poles kept off joint crease lines and preferably >= 2 loops away;
- no folded faces;
- quad interior angles targeted to 45-135 degrees;
- aspect ratio targeted <= 4:1 outside digit tips;
- no unwelded positional seams.

Do not keep sculpt/source density just because it exists.

Do not decimate critical anatomy blindly.

## 9. Deformation-loop requirements

Meet or exceed the contract minimums.

### Upper body
- neck: >= 4 supporting loops;
- shoulder / glenohumeral region: >= 5 loops plus clean axillary fold;
- clavicle / scapular flow follows Grask girdle;
- elbow: >= 3 loops + crease support;
- wrist: >= 3 loops.

### Hands
- finger MCP / major knuckle support: >= 3 loops where contract requires;
- IP joints: >= 2 support loops per joint;
- distinct thumb CMC/MCP/IP flow;
- web spaces must deform without collapsing;
- palm/metacarpal flow must support grip and spread;
- nail-bearing distal topology must retain visible nail form.

### Lower body
- hip / groin / gluteal fold: >= 5 loops plus gluteal-fold support;
- knee: >= 3 loops + crease support;
- ankle: >= 3 loops;
- ball / toe joints: >= 2 loops per toe joint;
- sole must remain compatible with plantigrade contact.

### Face
Provide production-quality edge flow for:
- orbit / eyelids;
- brow;
- mouth rings;
- jaw hinge;
- nasolabial / cheek transition where needed for later facial creator and animation.

Do not change the accepted neutral expression to create topology.

## 10. Grask-specific topology ownership

The retopo must deliberately support the anatomy that previously had no dedicated topology.

### Required Grask flow
- girdle slope;
- clavicle/scapular mass;
- upper-back transition;
- chest / sternum / keel organization;
- abdomen transition;
- pelvis organization;
- visible large-race joint structure;
- thick hand anatomy;
- broad foot anatomy.

The chest/abdomen shading-band history is **not** permission to flatten the body.

Build topology so surface shading can remain smooth while the accepted primary form remains intact.

The production mesh must not read as:
- stretched Marchfolk;
- stretched Aelari;
- generic human;
- old MPFB Grask with enlarged limbs.

## 11. Density / creator-readiness

There is **no final game vertex budget yet**.

Do not invent one.

Use the production contract density requirements as the governing rule:

- face / ears: mean edge length <= 0.25% stature;
- hands / feet / digits: <= 0.30% stature;
- trunk / pelvis / gluteal: <= 0.60% stature;
- limbs: <= 0.60% stature.

For 218 cm stature, these are ceilings, not targets to maximize.

Use the lowest practical density that:
- preserves v005 within tolerance;
- meets deformation-loop needs;
- leaves room for creator morphs;
- gives clean edge flow;
- remains LOD-friendly.

Report:
- total vertices;
- quads / triangles;
- density by zone;
- why the count is justified.

Do not artificially chase a lower polygon count at the expense of anatomy or deformation.

## 12. Face / eyes / mouth policy

Do not create final eyeball, teeth, tongue, or mouth-interior assets in this order.

However, the body topology must be ready for later production.

Required:
- clean orbit / eyelid ring flow;
- preserve the accepted narrow Grask eye opening;
- clean mouth rings;
- jaw-hinge support;
- no destructive eye opening;
- no change to facial proportions.

If an internal closed surface from the source cannot map directly into production face topology without changing visible anatomy, document the issue and preserve the visible neutral surface. Do not invent new biology.

## 13. Nails

Grask uses ordinary nails, not claws.

Keep the v005 nail read.

Nails remain part of the body mesh unless a later contract explicitly changes ownership.

Required:
- fingernail and toenail silhouette/read preserved;
- local support topology sufficient for future creator/deformation work;
- no talon conversion;
- no flattening the nail into invisibility.

Fine nail micro-edge detail may use the accepted micro-detail exemption only if:
- projection;
- taper;
- curl;
- silhouette;
- overall nail read
remain unchanged.

List every exemption.

## 14. Landmark package

Because v005 supersedes the old MPFB Grask source, do **not** blindly copy the old MPFB rig joints and call them exact v005 landmarks.

Use the older Grask/W2/Stage C joint data as **diagnostic seeds only**.

For v005:
- fit or transfer landmarks to the frozen v005 anatomy;
- validate each result against visible joint organization;
- record method for each landmark as `prior-seed+surface-fit`, `surface-fit`, or `manual`;
- report any meaningful departure from old Grask joint coordinates.

Required landmark groups:
- pelvis root;
- hips;
- knees + flexion axes;
- ankles + axes;
- MTP/ball lines;
- five toe tips per foot;
- sternoclavicular joints;
- clavicle ends/acromia;
- scapular proxies;
- glenohumeral centres;
- elbows + axes;
- wrists + axes;
- MCP roots and finger tips;
- thumb CMC;
- spine stations;
- neck base;
- atlanto-occipital/head pivot;
- crown;
- jaw hinges;
- chin;
- eye centres;
- mouth corners;
- ear roots/tips.

Production-vs-source landmark drift:
- target <= 1.0 mm;
- none > 1.5 mm;
- every value > 1.0 mm reported individually.

## 15. Anatomy-preservation tolerances

Use the accepted contract tolerances.

### T-1 — general body, both directions
- median <= 0.5 mm;
- p95 <= 1.5 mm;
- max <= 3.0 mm.

### T-2 — identity zones
For:
- head/face;
- ears;
- hands;
- feet;
- toes;
- nails;
- other Grask-defining regions.

Required:
- median <= 0.3 mm;
- p95 <= 0.8 mm;
- max <= 1.5 mm.

### T-3 — stature / bbox
- stature within +/-1.0 mm;
- bbox within +/-2.0 mm per axis.

### T-6 — landmarks
- target <= 1.0 mm;
- none above 1.5 mm;
- report every value above 1.0 mm.

### T-7 — silhouette
Body-only source vs production:
- front >= 0.995 IoU;
- profile >= 0.995;
- rear >= 0.995.

Also render 3/4 comparisons.

**Visual veto remains active.**

A numeric pass does not override a visible Grask identity change.

## 16. Projection discipline

Shrinkwrap / projection is allowed, but it must not:
- collapse joint loops;
- flatten knuckles;
- erase web spaces;
- destroy nail planes;
- shrink the girdle;
- flatten chest/pelvis organization;
- introduce surface ripples;
- make face flow lumpy.

Use controlled projection with:
- region masks;
- source normals where useful;
- post-projection topology cleanup;
- repeated bidirectional deviation checks.

Identity zones must be checked at higher precision than broad trunk regions.

## 17. UV / material / LOD scope

### UV
Do not perform final UV production.

Create only:
- a proposed seam edge set / seam plan;
- notes on likely islands;
- preservation of material-neutral topology.

If any old MPFB UV cannot meaningfully transfer, do not force it.

### LOD
Do not build final LODs.

Make LOD0 topology generation-friendly:
- continuous loops;
- removable supporting loops where sensible;
- tagged silhouette-critical loops;
- tagged head/girdle/hand/foot identity loops.

No LOD count or ratio is authorized.

## 18. Mandatory visual evidence

Create an RP2 evidence package.

### A. Source v005 vs retopo v001 whole body
Identical cameras:
- front;
- profile;
- rear;
- 3/4 front;
- 3/4 rear.

Provide:
- source;
- retopo;
- overlay;
- silhouette comparison.

### B. Head / face
Close:
- front;
- profile;
- 3/4;
- brow/orbit;
- nose/cheek;
- mouth/jaw;
- ear.

Show:
- source clay;
- retopo clay;
- wireframe overlay.

### C. Girdle / torso / pelvis
Close:
- shoulders/clavicle;
- upper back/scapular;
- chest/front-view identity;
- abdomen transition;
- pelvis/groin;
- gluteal fold.

### D. Hands
For each critical view:
- palm;
- dorsal;
- 3/4;
- thumb root;
- finger side;
- MCP row;
- PIP/DIP;
- fingertip/nail;
- web spaces.

Show both:
- clay comparison;
- wireframe.

### E. Feet
- top/front;
- outer;
- inner;
- sole;
- hallux;
- lesser toes;
- MTP/toe roots;
- toenails;
- ground-contact side.

Show both:
- clay comparison;
- wireframe.

### F. Topology diagnostics
Provide clear wireframe sheets for:
- face;
- shoulder/axilla;
- elbow;
- wrist;
- hand/fingers;
- hip/groin/glute;
- knee;
- ankle;
- foot/toes.

Label:
- poles;
- density transitions;
- loops;
- triangle locations, if any.

### G. Deviation
Provide:
- bidirectional deviation heat maps;
- per-zone median/p95/max table;
- identity-zone table;
- silhouette IoU table;
- landmark drift table.

## 19. Technical evidence

Final report must include:

- source path/hash before;
- source path/hash after;
- Blender version;
- retopo method used by region;
- automatic seed tool/settings, if used;
- manual-rebuild regions;
- vertex count;
- edge count;
- quad count;
- triangle count;
- quad percentage;
- n-gon count;
- components;
- boundary/non-manifold counts;
- duplicate/coincident/degenerate counts;
- self-intersection result;
- normals result;
- bbox;
- stature;
- density per zone;
- pole counts / notable pole locations;
- loop-count audit by deformation zone;
- landmark package;
- bidirectional deviation;
- silhouette IoU;
- race-specific identity audit.

## 20. Self-intersection

The final production retopo candidate must have:

- **0 catastrophic self-intersections**;
- no hidden penetrations caused by retopology;
- no accidental contact loops;
- no finger/body or toe/body intersections introduced by projection.

If the frozen v005 reference stance contains an intentional or unavoidable surface contact, document it distinctly rather than creating a topology handle around it.

## 21. Required deliverables

Create:

`GR_U_REF_RP2_retopo_v001.blend`

`GR_U_REF_RP2_retopo_v001.json`

`GR_U_REF_RP2_retopo_v001_landmarks.json`

Final gate:

`reviews/claude-rac-rp2-grask-retopo-v001-gate.md`

Evidence:

`reviews/rac-rp2-evidence/grask_retopo_v001/`

Include:
- source-integrity record;
- topology report;
- deviation report;
- silhouette report;
- landmark report;
- visual sheets;
- wireframes;
- seam-plan proposal;
- reproducibility tools/scripts.

Update:
- `reviews/claude-session-handoff.md`
- `specs/STATUS.md`

Do not modify the frozen v005 source.

## 22. Acceptance checklist

Claude must explicitly PASS/FAIL each item.

### Source
1. correct frozen v005 hash verified before work;
2. v005 unchanged after work;
3. retopo derives only from v005 anatomy.

### Anatomy
4. 218 cm stature preserved;
5. silhouette preserved;
6. head/face preserved;
7. Grask front-view identity preserved;
8. girdle slope preserved;
9. chest/abdomen organization preserved;
10. pelvis organization preserved;
11. joint visibility preserved;
12. hand scale and anatomy preserved;
13. foot scale and anatomy preserved;
14. ordinary nails preserved.

### Topology
15. >=98% quads overall;
16. 100% quads in deformation zones;
17. 0 n-gons;
18. manifold / watertight / one body;
19. loop minimums satisfied;
20. creator-density ceilings satisfied;
21. pole placement acceptable;
22. no destructive density transitions.

### Validation
23. T-1 pass;
24. T-2 pass;
25. T-3 pass;
26. T-6 pass;
27. T-7 pass;
28. visual author sheet shows no identity drift;
29. no catastrophic self-intersections;
30. source provenance / sidecars complete.

A technical pass does not override a visual failure.

## 23. Stop rule

After producing the first complete retopology candidate and its gate:

**STOP FOR TYLER / CHATGPT AUTHOR REVIEW.**

Do not:
- rig;
- skin;
- build creator morphs;
- begin final UV/material work;
- build LODs;
- export to UE5;
- start Marchfolk or another race;
- propagate this topology to other races.

Return exactly:

**RP2 GRASK RETOPO V001 COMPLETE / READY FOR AUTHOR REVIEW**

Then STOP.
