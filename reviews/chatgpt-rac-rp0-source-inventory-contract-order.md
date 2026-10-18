# RAC RP0 — source inventory and production-mesh contract audit

**Authority:** Tyler approved the Retopology / Rig-Prep program.
**Date:** 2026-10-18.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Master plan:** `reviews/chatgpt-rac-retopology-rigprep-master-plan.md`

## 1. Purpose

Perform the read-only bootstrap audit for production retopology / rig preparation.

Do not edit geometry.

Deliver:
1. exact accepted source inventory for all 13 races;
2. topology / rig-prep characterization;
3. a proposed production-mesh contract;
4. topology-family recommendation;
5. exact RP1 Gorrund pilot entry plan.

## 2. Source search scope

Inspect:
- `reviews/reference-assets/manifest.json`;
- Stage C / D4 status records;
- race specs;
- accepted author gates;
- current local race-body workspace under the Wayfarer project on E:;
- uploaded/final GLB/BLEND assets available in the local Wayfarer race-body source tree.

Do not assume the NPZ reference asset is the best production-retopo source if a newer accepted sculpt/GLB exists.

For each race identify:
- canonical accepted anatomy source;
- best high-resolution retopo reference;
- best editable source if different;
- any accepted min/max/configuration variants relevant to future creator work.

If a file cannot be found locally, state that explicitly.

## 3. Required 13-race inventory

For each:
- Marchfolk
- Skarn
- Sagekin
- Fenn
- Aelari
- Vael
- Halvren
- Durrim
- Grask
- Gorrund
- Pipkin
- Cogling
- Saurin

Record:

### Identity
- source path;
- file type;
- SHA-256;
- provenance / acceptance commit;
- stature;
- sex-related configuration;
- whether source is reference-only, sculpt, production candidate or generator artifact.

### Mesh statistics
Where accessible:
- object count;
- vertex count;
- edge count;
- triangle/face count;
- components;
- boundaries;
- non-manifold edges;
- self-intersection summary;
- duplicate/coincident vertices/shells;
- degenerate faces;
- normals;
- symmetry;
- transform/scale;
- ground/origin;
- current pose.

### Production readiness
- UV presence;
- material slots;
- vertex groups;
- armature / skin weights;
- shape keys;
- named landmarks;
- separate eyes/teeth/tongue/nails/tail/etc.;
- obvious deformation risks;
- obvious creator-density risks.

### Known debt
Reconcile against repo notes.

Especially:
- Gorrund hand-contact loops;
- left-axilla micro-tunnel;
- perineal/seam handling;
- slivers;
- local nail-support subdivision;
- Grask chest/abdomen shading band;
- Grask front-view preservation constraint.

## 4. Source confidence classification

Assign each race:

- **A — production-retopo source confirmed**
- **B — accepted anatomy confirmed, but best editable/high-res source ambiguous**
- **C — accepted reference exists, but production-retopo source missing**
- **D — source conflict / author decision required**

Do not resolve B/C/D by choosing an older candidate silently.

## 5. Topology-family analysis

Recommend whether production topology should be:

- shared;
- family-shared with race-specific branches;
- unique.

Evaluate at least:
- human-derived group;
- elf/mixed group;
- compact humanoids;
- Grask;
- Gorrund;
- Saurin.

Consider:
- limb proportions;
- torso/pelvis;
- hands/feet;
- craniofacial topology;
- ears;
- tails;
- creator ranges;
- sex-related configurations.

Do not force shared topology for convenience.

## 6. Production-mesh contract draft

Create:

`specs/RAC_PRODUCTION_MESH_CONTRACT.md`

It must define, at minimum:

- source immutability;
- naming/versioning;
- units/axes/origin;
- pose strategy;
- component ownership;
- topology-quality rules;
- joint/deformation zones;
- creator-density zones;
- topology-family policy;
- UV readiness scope;
- LOD readiness scope;
- rig-facing landmark package;
- anatomy-preservation validation;
- evidence package;
- family-pilot acceptance rule.

### Technical thresholds
You may propose:
- surface-deviation tolerances;
- landmark drift tolerances;
- topology quality thresholds;
- density/budget ranges.

But:
- label them **PROPOSED PRODUCTION TOLERANCES**;
- do not turn them into biology canon;
- explain why each is appropriate;
- flag any threshold whose acceptance needs Tyler/ChatGPT before geometry work.

Do not invent a final game-performance vertex budget without UE5/performance evidence.

## 7. Pose recommendation

Recommend a retopo/rig-prep pose policy.

Must distinguish:
- accepted reference measurement stance;
- derived production rig-prep pose;
- runtime idle.

If recommending A-pose/T-pose or another pose:
- use a derived copy;
- never overwrite the accepted reference;
- explain how anatomical landmarks remain invariant.

No posing is authorized in RP0.

## 8. Rig-facing landmark proposal

Define a race-aware landmark package for later rigging:
- root / pelvis;
- hip;
- knee;
- ankle;
- ball / toe;
- clavicle / scapular proxy where relevant;
- shoulder;
- elbow;
- wrist;
- finger roots;
- neck;
- head;
- jaw;
- eyes;
- tail root/chain for Gorrund/Saurin and any other accepted tail;
- ear/display support where appropriate.

This is landmark prep, not skeleton-family finalization.

## 9. RP1 Gorrund pilot plan

Prepare but do not execute:

`reviews/chatgpt-rac-rp1-gorrund-production-retopo-pilot-HOLD.md`

It must include:
- exact final Gorrund source path/hash;
- known topology debt;
- immutable anatomy zones;
- allowed topology operations;
- proposed output path;
- deviation/landmark gates;
- joint-loop expectations;
- tail/nail/head/hand/foot protections;
- evidence requirements;
- stop conditions.

Do not start RP1 in RP0.

## 10. Deliverables

Return:

`reviews/claude-rac-rp0-source-inventory-contract.md`

Evidence:

`reviews/rac-rp0-evidence/`

Also create:
- `specs/RAC_PRODUCTION_MESH_CONTRACT.md`
- `reviews/chatgpt-rac-rp1-gorrund-production-retopo-pilot-HOLD.md`

Update:
- `specs/STATUS.md`
- `reviews/claude-session-handoff.md`

with RP0 status only.

## 11. Decision gate

Return one of:

**RP0 PASS / PRODUCTION MESH CONTRACT READY / RP1 GORRUND PILOT READY FOR RELEASE**

or

**RP0 CONSTRAINED / AUTHOR DECISIONS REQUIRED**

or

**RP0 BLOCKED / SOURCE INVENTORY INCOMPLETE**

Then STOP.

No geometry changes in RP0.
