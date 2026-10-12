# RAC RM-OT-05F — Gorrund hand-sculpt escalation / re-entry order

**Authority:** author decision following RM-OT-05E  
**Predecessor:** `reviews/claude-rac-rm-ot-05e-gorrund-structural-readability-closure-gate.md`  
**Status:** EXECUTE. Stop at the next author-acceptance gate.

## 1. Author ruling

Accept the RM-OT-05E result exactly as reported.

1. **Grask E3 is accepted as the developmental race-anatomy direction pending Stage C.**
   - Freeze the demonstrated E3 body organization.
   - Do not reopen the Grask procedural search.
   - Do not promote Grask beyond the already stated developmental status until Stage C is completed.

2. **Gorrund RM-OT-05E fails.**
   - Do **not** promote P1, P2, P3, E1, E2, or any other failed 05C–05E candidate.
   - Do **not** continue tuning the exhausted procedural generator in an attempt to force a pass.
   - Do **not** solve the failure by changing canon, changing posture, adding fat/muscle bulk, or hiding the problem in surface detail.

3. **Authorize the 05E recommended escalation: a dedicated hand-sculpted Gorrund base mesh.**
   - The purpose is to introduce hard-form anatomical organization that cannot be explained as ordinary heavy-human variation.
   - The sculpt must remain fully inside the existing Gorrund canon and technical constraints.

RM-OT-05 remains OPEN until the sculpt passes re-entry validation and Stage C.

## 2. RM-OT-05F objective

Prepare the exact production and validation package needed to obtain and accept a hand-sculpted Gorrund base mesh without losing the already-validated race-system constraints.

This is **not** a new anatomy ideation pass. The 05E report already defines the allowed hard-form direction.

Create an implementation-ready package that a sculptor or direct mesh-edit workflow can execute without reinterpretation, then make the existing pipeline ready to ingest and validate that mesh.

If the repository already contains a genuinely direct mesh-sculpt/edit route that is independent of the exhausted procedural generator, it may be used. If no such route exists, do **not** fake a sculpt procedurally; produce the handoff package and stop at the handoff gate.

## 3. Locked Gorrund constraints

The hand-sculpt must preserve all of the following:

- accepted Gorrund skeleton;
- joint centres;
- long-bone axes and bone scales;
- accepted stature route, with 230.9 cm as the reference body and the already accepted range;
- R-6 neutral stance;
- plantigrade feet;
- five digits;
- human-compatible hands and feet;
- protected deep-pelvis / load-path relations at skeleton-anchored stations;
- MPFB / R-6 rig compatibility;
- 05D true-floor semantics;
- 05D/05E volume semantics;
- existing Frame and body-composition system;
- no uniform whole-body scale as the race solution;
- no posture trick;
- no identity by fat or muscle amount;
- no canon rewrite.

Do not alter race canon files in RM-OT-05F.

## 4. Required hard-form anatomy

Translate §10 of the 05E report into explicit sculpt targets, measurements/landmarks where the current data supports them, and matched-view references.

The hand-sculpt brief must require all six families below.

### A. Trunk section, S2–S5
- planar/faceted slab rather than a smooth human torso;
- defined lateral edges between anterior and lateral planes;
- broad flat sternal–abdominal plate;
- crisp lower structural border rather than a soft belly transition;
- no human pectoral shelf as the defining torso read;
- no waist hollow;
- thoracolumbar depth carried as structure, not fat mass.

### B. Posterior axial load path
- paired broad paraspinal load columns;
- flat interscapular plane;
- defined sacral plate with a hard transverse upper border;
- continuous sacral-to-hamstring structural path;
- no round human gluteal apex as the dominant form;
- no ordinary buttock fold;
- profile must sustain a straight/inclined structural line from upper back into proximal thigh.

### C. Pelvis → thigh
- structural hip plate;
- clear trochanteric shelf;
- planar lateral thigh;
- defined step/transition rather than a smooth human taper.

### D. Knee / shank / ankle
- broad, flat patellar plate;
- legible femoral/tibial condyle blocks;
- squarish shank section;
- flat anteromedial tibial plane;
- defined posterior tendon column;
- broad malleolar ankle blocks;
- must read as a jointed structural column, not as a uniform pillar and not as thick-thigh/thin-shin human taper.

### E. Elbow / forearm / wrist
- defined olecranon/epicondyle block;
- flattened/squarish forearm section;
- clear tendon border;
- broad wrist plate;
- hands unchanged in digit count and basic compatibility.

### F. Shoulder girdle / neck root
- low, broad girdle integrated with the slab trunk;
- trapezius plane continuous with the trunk planes;
- planar shoulder block over the accepted joint;
- no ordinary human deltoid cap as the primary read.

The sculpt must preserve these cues at both reference and low-composition states.

## 5. Deliverables

Create all of the following.

### 5.1 Production brief
Create:

`reviews/gorrund-rm-ot-05f-hand-sculpt-production-brief.md`

It must contain:
- the six hard-form families above;
- locked skeleton/stature/rig constraints;
- protected measurements and station definitions already supported by 05D/05E;
- explicit “must not” examples from the failed 05C–05E routes;
- front, front 3/4, profile, rear 3/4 and body-only silhouette targets;
- low-composition and Narrow/Broad persistence requirements;
- import/export expectations for the reference mesh;
- a sculptor checklist and a validator checklist.

Do not invent new canon measurements merely to fill a table. Where no numeric canon exists, mark the target as relational/visual and point to the accepted evidence.

### 5.2 Evidence/reference index
Create:

`reviews/rac-rmot05f-handoff/README.md`

Index the strongest existing 05D/05E evidence that defines:
- accepted Gorrund skeletal floor/protected relations;
- failed human-reading examples;
- successful Grask E3 non-human organization as a contrast case only;
- matched camera and silhouette standards;
- low-composition persistence requirement.

Copy or regenerate only what is needed for a clean handoff package. Do not relabel failed candidates as accepted references.

### 5.3 Re-entry validator
Add or prepare a dedicated 05F validator/driver layer that can ingest the future sculpt without rewriting the existing 05D/05E guards.

It must check:
- exact stature / ground contact;
- skeleton, joint, long-bone axis and bone-scale preservation;
- no uniform scaling;
- R-6 posture equality;
- plantigrade contact;
- hand/foot topology and digit count;
- true-floor compliance;
- gross self-intersection;
- arm/trunk clearance;
- protected Gorrund relations;
- whole-body volume semantics;
- Frame ordering;
- body-composition ordering;
- reference and low-composition transport.

Do not weaken any existing threshold to accommodate the sculpt.

### 5.4 Blind-gate package
Prepare the replicated blind-gate runner for the sculpt.

Required protocol remains:
- body only;
- head/neck removed;
- height-normalized;
- matched front + profile;
- neutral grey + black silhouette;
- fresh shuffle each run;
- 3 uninformed scorers per run;
- Grask E3 included in every run as the accepted non-human contrast;
- human-family controls included;
- Gorrund reference and low-composition states both tested.

Pass condition remains:
- Gorrund receives **C = distinct humanoid race/species from at least 2/3 scorers at reference and low composition in every replicated run**;
- stable grouping;
- distinguishable from Grask;
- majority explanation must cite structural organization, not bulk;
- both axial and limb cues must be named;
- no human-control collapse.

## 6. Stage C rule

Do **not** run combined Stage C yet.

Stage C may begin only after a hand-sculpted Gorrund body:
1. passes every technical re-entry guard; and
2. passes the replicated blind structural-readability gate.

Once that happens, run Stage C using:
- **Grask E3** as the frozen accepted developmental Grask direction;
- the newly accepted Gorrund sculpt;
- the existing matched-stature and roster-wide comparative framework.

Stage C must then verify that the two races remain distinct across:
- shared statures;
- Frame states;
- composition extremes;
- front / 3/4 / profile / rear;
- body-only silhouettes;
- final head/body integration later in the race pipeline.

## 7. Canon and scope guard

Do not:
- revise Gorrund canon to make the sculpt easier;
- add digitigrade anatomy;
- change joint order;
- change posture;
- use clothing, hair, texture, pigmentation, scars, or face traits to pass this body-only gate;
- use extra fat or muscle as the identity;
- replace Grask E3 with a new procedural search;
- promote any failed 05C–05E Gorrund candidate;
- start UE5 implementation or D4 work from an unaccepted body.

## 8. Stop condition

This order ends at the next author gate.

### If a genuine direct sculpt route is available now
Produce the sculpt candidate, run all re-entry guards and the replicated blind gate, package the evidence, and stop for author review.

### If no genuine direct sculpt route is available
Complete the production brief, evidence index, validator, and blind-gate package; record the exact external asset required and its expected file/topology format; then stop for author review.

Do not report RM-OT-05 closed until the accepted Gorrund sculpt has passed the gate and Stage C is subsequently completed.
