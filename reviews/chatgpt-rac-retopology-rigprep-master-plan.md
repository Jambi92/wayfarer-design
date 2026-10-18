# RAC Production Mesh Program — Retopology / Rig-Prep Master Plan

**Status:** AUTHOR-DIRECTED PROGRAM PLAN
**Date:** 2026-10-18
**Repository:** `Jambi92/wayfarer-design`, `main`
**Authority:** Tyler approved moving from the closed Reference Anatomy / D4 program into retopology / rig preparation.

## 1. Program purpose

Convert the 13 author-accepted race reference bodies into **production-mesh candidates** that are suitable for:

- deformation and skinning;
- future race-aware character-creator morphs;
- stature / frame / composition variation;
- facial customization where applicable;
- equipment fitting;
- LOD generation;
- later UE5 import and production rigging.

This program must preserve accepted anatomy.

Reference meshes / frozen sculpts are **immutable source truth**. Production meshes are derived assets. Nothing in this program reopens race biology unless a true anatomy contradiction is discovered and returned for author review.

## 2. Program firewall

This program does **not** itself authorize:

- UE5 integration;
- final production rigging / skin weighting;
- animation;
- gameplay;
- creator UI implementation;
- final UV/texturing/material production;
- equipment production;
- final LOD policy.

It prepares meshes and rig-facing data so those stages can begin safely.

## 3. Core production principles

### P-1 — anatomy wins over shared topology
Do not force all 13 races onto one universal topology if doing so changes accepted anatomy.

Topology reuse is allowed only where it preserves race identity and required anatomy.

### P-2 — topology families, not one body
Use topology families where practical, subject to RP0 evidence.

Candidate families:
- human-derived / near-human: Marchfolk, Skarn, Sagekin;
- elf-derived / mixed: Fenn, Aelari, Vael, Halvren;
- compact humanoid: Durrim, Pipkin, Cogling;
- long-limbed Grask;
- leonine Gorrund;
- reptilian Saurin.

These are planning families, not canon categories and not mandatory sharing groups.

### P-3 — reference source is never overwritten
Every production mesh must point to:
- exact frozen source file;
- exact hash;
- exact author-acceptance / Stage C provenance.

No accepted source mesh is edited in place.

### P-4 — creator support is a topology requirement
Production topology must leave room for later:
- stature DIR deformation;
- Narrow / Balanced / Broad frame;
- muscularity;
- fat amount/distribution;
- regional development;
- hands / feet;
- sex-related soft-distribution changes;
- race-specific anatomy.

Do not collapse topology around one frozen body in a way that makes the accepted creator ranges impossible.

### P-5 — skeletal relationships are protected
Rig prep must preserve accepted:
- joint centres;
- limb axes;
- girdle relationships;
- pelvis organization;
- head/neck relationship;
- hands/feet proportions;
- race-specific tail roots / tail bases;
- race-specific ears, rostra, claws, cranial displays and other mandatory anatomy.

### P-6 — no hidden anatomy change through cleanup
Retopology, smoothing, normal cleanup, shrinkwrap and projection may not silently alter silhouette or body organization.

Every race requires before/after comparison and measured deviation evidence.

### P-7 — neutral production state
Derived production bodies remain neutral reference assets:
- no clothing;
- no culture/class coding;
- no animation pose personality;
- no material trick used to fake race structure.

## 4. Program phases

### RP0 — Source Inventory + Production Mesh Contract
**Read-only. No geometry authoring.**

Goals:
- find the actual accepted source file for every race;
- hash and classify each source;
- inspect topology / components / UVs / normals / transforms / symmetry / scale / pose;
- list known debt;
- determine which sources are usable directly as retopo references;
- define the production-mesh contract and topology-family recommendation;
- define pilot-race order.

Output:
- `specs/RAC_PRODUCTION_MESH_CONTRACT.md`
- `reviews/claude-rac-rp0-source-inventory-contract.md`
- `reviews/rac-rp0-evidence/`

RP0 ends at an author/ChatGPT review gate if any production-standard choice cannot be resolved from existing canon.

### RP1 — Gorrund production-mesh pilot
Use Gorrund as the first difficult pilot because:
- its final sculpt is frozen and well documented;
- known topology debt exists;
- it has a tail, feline feet/nails and unusual head anatomy;
- it tests whether the contract can preserve non-human anatomy.

Required cleanup targets already carried:
- hand contact loops;
- left-axilla micro-tunnel;
- perineal seam handling;
- slivers / low-quality local topology;
- nail-support local topology;
- clean deformation topology around shoulders, hips, knees, elbows, wrists, ankles and tail root.

No anatomy redesign.

RP1 must prove:
- reference preservation;
- deformation-ready edge flow;
- clean manifold production body;
- creator-safe regional density;
- a repeatable source→production process.

### RP2 — Grask production-mesh pilot
Second pilot for a structurally different non-human body.

Carry:
- E3 accepted direction;
- long-limb / short-torso organization;
- girdle slope;
- joint visibility;
- pelvis organization;
- front-view identity;
- chest/abdomen shading-band ownership.

The production mesh must not collapse Grask into a stretched human or Aelari-like front read.

### RP3 — Human / elf-derived families
Proceed only after RP1/RP2 validate the contract.

Suggested order:
1. Marchfolk — baseline human topology;
2. Skarn;
3. Sagekin;
4. Fenn;
5. Aelari;
6. Vael;
7. Halvren.

Topology sharing may be proposed where supported, but race-specific ear, head, frame and proportion topology is preserved.

### RP4 — Compact humanoid family
Suggested order:
1. Durrim;
2. Pipkin;
3. Cogling.

Special attention:
- adult read at small stature;
- hands / feet;
- face/orbit/jaw support;
- compact joint topology;
- Cogling 76 cm support.

### RP5 — Saurin
Saurin remains a special production family.

Required support includes:
- mandatory tail;
- tail-base deformation;
- rostrum;
- scale-field topology;
- cranial display support;
- claw anatomy;
- non-human head/neck transition.

Do not force Saurin into a mammalian head topology standard.

### RP6 — Cross-race deformation / creator-readiness validation
After all reference production meshes exist:

Validate:
- joint-region deformation topology;
- topology-family compatibility;
- stature deformation support;
- frame support;
- composition support;
- hand/foot controls;
- tail / ear / display special anatomy;
- symmetry and asymmetry pathways;
- creator-safe support for accepted extremes.

This phase may use diagnostic rigs/deformations, but does not create the final production rig unless separately authorized.

### RP7 — Production handoff
Produce the package required to start:
- production rigging;
- creator implementation;
- UE5 integration.

RP7 is a gate, not automatic authorization of those workstreams.

## 5. Production-mesh contract topics RP0 must settle

RP0 must recommend and document:

1. **Authoritative source per race**
   - file path;
   - hash;
   - acceptance provenance;
   - whether it is sculpt, procedural ARM, GLB, NPZ or other.

2. **Units / axes / origin**
   - real-world scale;
   - ground reference;
   - transform policy.

3. **Pose policy**
   - source measurement stance;
   - proposed retopo/rig-prep pose;
   - whether a non-destructive pose copy is required.

4. **Mesh ownership**
   - body;
   - eyes;
   - teeth/tongue if present;
   - nails/claws;
   - ears;
   - tails;
   - Saurin display;
   - any separate anatomy.

5. **Topology quality**
   - manifold requirements;
   - boundary policy;
   - allowed triangles/poles/ngons;
   - minimum local quality;
   - seam policy.

6. **Deformation zones**
   - shoulders;
   - elbows;
   - wrists;
   - fingers;
   - hips;
   - knees;
   - ankles;
   - toes;
   - neck;
   - jaw/face;
   - tail roots / tail joints.

7. **Creator-density zones**
   - face;
   - ears;
   - hands/feet;
   - torso composition;
   - pelvis;
   - tails / displays;
   - race-specific regions.

8. **Topology-family policy**
   - what may share topology;
   - what may only share standards;
   - what must remain unique.

9. **UV/material readiness**
   - whether UVs are required in this phase;
   - whether only seam planning is required;
   - preserve neutral anatomy/material separation.

10. **LOD readiness**
    - whether LOD0 topology should be LOD-generation-friendly;
    - no final LOD counts without a later performance contract.

11. **Rig-facing landmarks**
    - joint centres;
    - axes;
    - root/pelvis;
    - jaw/eyes;
    - tail chain;
    - ear/display support where applicable.

12. **Anatomy-preservation validation**
    - silhouette comparison;
    - landmark comparison;
    - surface deviation;
    - stature/bbox;
    - race-specific metrics;
    - visual author sheet.

RP0 may recommend numeric technical tolerances, but must label them **production tolerances**, not biology canon. Any tolerance that could visibly change accepted anatomy requires author/ChatGPT acceptance before RP1.

## 6. Per-race production acceptance gate

A production mesh does not pass merely because it is clean.

Every race must satisfy:

### Source integrity
- exact frozen source identified and unchanged;
- derivation history recorded.

### Geometry integrity
- intended components only;
- no accidental open seams;
- no self-intersections that affect deformation;
- no non-manifold defects unless explicitly justified;
- no hidden duplicate surface shells;
- normals coherent.

### Anatomy preservation
- stature preserved;
- accepted silhouette preserved;
- race-defining landmarks preserved;
- no creator-valid region silently narrowed;
- race-specific anatomy preserved.

### Deformation topology
- clean edge flow / support around primary joints;
- sufficient density where creator deformation will operate;
- no unnecessary source-sculpt density retained merely because it exists;
- no destructive decimation of identity-critical regions.

### Visual comparison
- identical-camera front / profile / back / 3/4;
- closeups of head, hands, feet and race-specific regions;
- overlay / deviation evidence.

### Author gate
The first production mesh in each topology family requires explicit author/ChatGPT acceptance before family propagation.

## 7. Source priority

Use this priority when several assets exist:

1. newest author-approved frozen sculpt/reference;
2. accepted Stage C source;
3. accepted W2/W1 ARM/reference;
4. accepted high-resolution GLB submitted by Tyler if canonically matched;
5. older candidates only as comparison/provenance.

Never advance from a rejected candidate because it has easier topology.

## 8. Known special cases

### Gorrund
- final frozen source = `GO-05AW4_nails_final`;
- topology debt belongs here;
- native sculpt height is not a canon envelope revision;
- creator variants deferred.

### Grask
- Stage C accepted direction = E3;
- W2 GR218R is provenance/constraint, not the final E3 realization;
- preserve front-view identity constraints.

### Halvren
- central reference and ancestry-conditional stature reaches are distinct;
- topology must not become an "elf percentage" interpolation system.

### Saurin
- special topology family;
- mandatory tail and reptilian cranial anatomy.

## 9. Stop rules

Stop and ask for author/ChatGPT decision if:
- accepted source for a race cannot be identified;
- two accepted assets conflict;
- topology sharing would alter anatomy;
- a retopo/rig-prep pose would require anatomy-changing reproportion;
- a creator requirement forces a new biological decision;
- production tolerance would permit visible identity change.

Do not silently solve those by changing canon.

## 10. Immediate next action

Execute RP0.

No geometry editing is authorized until RP0 returns the source inventory and production-mesh contract.
