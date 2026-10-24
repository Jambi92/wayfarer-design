# RAC RP2 — Grask 3D anatomical-source rebase order

**Date:** 2026-10-24  
**Authority:** Tyler direct author ruling through ChatGPT after rejection of the v001-v006 morphology branch.  
**Latest rejected production-shape candidate:** `GR_U_REF_RP2_production_v006.blend` / Claude commit `4c3166239bc38c9581d70c21277e0cf049e72d19`.  
**New 3D handoff:** `assets/rac/rp2/grask/reference/GRASK_front_reference_proxy_v001.glb.gz`.  
**Visual authority:** Tyler's approved grounded-troll turnaround image already used in v004-v006.

## 1. Author ruling

STOP trying to morph v006 toward the target.

v001-v006 remain preserved as development evidence and as potential topology/deformation references, but **none of them remains the Grask morphology authority**.

Tyler supplied a new GLB generated from the approved Grask turnaround. That GLB contained three separate generated full-body figures corresponding to the front, profile and three-quarter source views. ChatGPT isolated the **left/front-derived full figure** as the primary 3D anatomical source candidate.

This changes the workflow:

> Build and approve a new clean Grask anatomical source first. Only after author approval may RP2 production retopology resume against that source.

Do not begin v007 production morphology.

## 2. Source files and limitations

Repository handoff:
- `assets/rac/rp2/grask/reference/GRASK_front_reference_proxy_v001.glb.gz`
- accompanying README in the same folder.

The repo GLB is deliberately a **coarse macro-shape proxy** because the connector could not stream the full dense 6.1 MB extraction into GitHub.

Proxy:
- ~649 V / 1,424 tris;
- ~1.898 m generated height;
- one isolated full figure;
- no profile/three-quarter character mixed in.

Dense extraction retained by ChatGPT:
- `GRASK_front_reference_extracted_v3.glb`
- ~196,873 V / 314,892 tris;
- SHA-256 `03aed1aad8f134720e448feab54301d99dbc6bf8fa61583f671a2906878bceb2`.

**Do not use the proxy topology as production topology.**
**Do not infer fine anatomy from proxy faceting.**

The proxy is a 3D macro-massing guide. Tyler's approved turnaround remains the detailed visual authority until the dense source is available in Claude's environment.

## 3. Why this source supersedes v006 morphology

The isolated source simultaneously carries the body relationships that v001-v006 repeatedly failed to reproduce:

- grounded broad ribcage;
- substantial but non-bodybuilder shoulder structure;
- strong neck/trapezius integration;
- long but substantial arms;
- large functional hands;
- coherent pelvis and upper-thigh mass;
- strong thighs and calves;
- large planted feet;
- compact/heavy troll-like head;
- robust non-human ear direction;
- one coherent whole-body mass rhythm rather than independently tuned body regions.

Preserve those relationships.

## 4. New task — anatomical source construction, NOT production retopology

Create a new clean high-density Grask anatomical-source candidate.

Suggested file:
`GR_U_REF_RP2_SOURCE_3D_v001.blend`

The job is to reconstruct/clean the anatomy represented by the new 3D source and Tyler's target image.

Do **not** turn the coarse proxy directly into the production cage.

Do **not** reuse v006 as the shape authority.

Existing v006 production topology may later be salvaged only if it can conform to the approved new source without compromising that source.

## 5. Canonical scale

The generated extracted source is ~1.898 m tall.

Rescale the anatomical source uniformly to the established Grask reference target of approximately **218 cm** while preserving proportions.

Record:
- original source height;
- scale factor;
- resulting height;
- bbox before/after.

Do not use nonuniform scaling to force body ratios.

## 6. Remove generated presentation artifacts

The target/source includes a minimal loincloth/modesty covering.

For the anatomical source:
- remove cloth geometry and cloth-derived surface contamination;
- reconstruct hidden body anatomy conservatively;
- use bilateral continuity, target-image silhouette, existing Grask canon and neighboring body planes;
- do not invent exaggerated genital or pelvic detail;
- keep the neutral anatomy suitable for later creator/rigging work.

Also remove or repair:
- floating scan fragments;
- duplicate patches;
- accidental holes;
- disconnected garbage;
- cloth intersections;
- obvious generator artifacts.

## 7. Neutralize over-specific musculature

The generated figure is a useful structural source but represents a fairly fit specimen.

The Grask racial anatomical baseline must preserve:
- broad structural ribcage;
- strong neck/shoulders;
- substantial limbs;
- large hands/feet;
- thigh/calf mass;

while reducing overly individual/bodybuilder-specific definition:
- etched abdominal separation;
- sharp pec cuts;
- excessive deltoid striation;
- over-defined arm muscle grooves;
- tertiary muscle ridges.

Do **not** reduce structural mass to achieve neutrality.

The goal is a **race baseline**, not a smooth human mannequin and not a bodybuilder.

## 8. Head / face / ears

Use the source/target direction:
- compact heavy troll head;
- strong brow/orbit;
- broad nasal base;
- substantial cheek/jaw block;
- grounded chin;
- robust, modestly non-human ears.

Avoid:
- v001 human face;
- v002 alien elongation;
- giant orc jaw/underbite;
- mandatory tusks;
- elf ears;
- monster caricature.

If the coarse proxy lacks sufficient facial detail, follow the approved turnaround image rather than inventing from proxy polygons.

## 9. Hands and feet

The source gets the **scale and weight** of hands/feet much closer to target, but generator defects are expected.

Repair:
- finger separation;
- digit lengths/taper;
- thumb integration;
- palm continuity;
- toe separation;
- forefoot/heel continuity;
- stray fragments or fused artifacts.

Keep:
- five fingers;
- five toes;
- ordinary nails;
- no claws;
- plantigrade feet;
- tool/weapon-compatible hands;
- large but biologically grounded troll proportions.

## 10. Symmetry / natural asymmetry

Use a clean neutral reference stance.

Correct obvious generation asymmetry and artifacts.

Do not erase all natural anatomical variation if the source supports it, but the frozen anatomical authority must be suitable for a race baseline and creator morph system.

Record any intentional asymmetry preserved.

## 11. Self-audit before author turn-in

Claude must complete and internally pass the source before returning it.

Required checks:

### Source integrity
- one intended body;
- no geometry from the other generated figures;
- no cloth/floating garbage;
- no accidental duplicate shells;
- coherent surface;
- correct ~218 cm scale.

### Identity
- neutral material reads immediately as Grask/troll-like;
- not human;
- not alien;
- not generic bulky orc;
- target-like head/neck/torso/limb mass hierarchy survives cleanup.

### Body hierarchy
- head feels heavy enough;
- neck supports head;
- ribcage/waist/pelvis hierarchy is coherent;
- arms remain long and substantial;
- hands remain large and functional;
- thighs/calves remain strong;
- feet visibly anchor the body.

### Surface
- no scan noise that would mislead later retopology;
- no arbitrary lumps;
- no bodybuilder-specific tertiary definition;
- no oversmoothing that destroys species form.

If any of these fail, continue internally. Do not send a partial source.

## 12. Required visual evidence

Produce neutral-clay comparison renders:

### A. New source
- front;
- left profile;
- back;
- three-quarter front;
- three-quarter back.

### B. Target comparison
Show Tyler's target image beside:
- front;
- profile;
- three-quarter.

### C. Detail checks
- face front/profile/three-quarter;
- ears;
- hands;
- feet;
- neck/shoulders;
- chest/ribcage;
- pelvis/thigh;
- calf/ankle.

### D. Optional historical comparison
A single v006 vs new-source sheet is useful only to demonstrate why the rebase is superior. Do not tune the new source toward v006.

## 13. Technical evidence for source

This is not yet the final production cage, so production quad-density rules do not apply to the source itself.

Still report:
- component count;
- boundary/non-manifold status;
- duplicate/floating geometry status;
- normals;
- self-intersection diagnostics where meaningful;
- vertex/face counts;
- exact height/bbox;
- source/proxy hashes;
- any reconstruction masks/regions.

A high-density clean sculpt/source mesh is acceptable at this stage.

## 14. Freeze boundary

Do **not** restart production retopology in this order.

Do not:
- create RP2 production v007;
- rig;
- create creator morphs;
- integrate UE5;
- begin another race.

First return the cleaned anatomical source for Tyler's visual approval.

Required status:

**RP2 GRASK 3D ANATOMICAL SOURCE REBASE COMPLETE / READY FOR AUTHOR REVIEW**

Then STOP.

## 15. Deliverables

Create:
- `GR_U_REF_RP2_SOURCE_3D_v001.blend`
- export GLB/OBJ source copy if useful for provenance.

Report:
`reviews/claude-rac-rp2-grask-3d-source-rebase-final-gate.md`

Evidence:
`reviews/rac-rp2-evidence/grask_3d_source_rebase/`

Update:
- `reviews/claude-session-handoff.md`
- `specs/STATUS.md`

Preserve all v001-v006 production artifacts and evidence unchanged.
