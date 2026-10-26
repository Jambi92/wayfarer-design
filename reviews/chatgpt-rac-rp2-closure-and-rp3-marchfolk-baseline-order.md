# RAC RP2 closure + RP3 Marchfolk production-mesh baseline order

**Date:** 2026-10-26  
**Authority:** Tyler / ChatGPT after review of Grask RP2 final diagnostic return `02468aaf7353008e7d207564ba4d5fba68e76952`.  
**Program references:** `reviews/chatgpt-rac-retopology-rigprep-master-plan.md`, `specs/RAC_PRODUCTION_MESH_CONTRACT.md`, RP0 source inventory, frozen Gorrund RP1, frozen Grask RP2.

This order has two sequential purposes:

1. formally close Grask RP2 deformation-validation work and preserve its production-rig carry-forward items;
2. begin **RP3 Marchfolk**, the first MPFB-derived human-family production-mesh baseline.

Do not begin final production rigging for Grask in this order.

---

# PART A — GRASK RP2 FORMAL CLOSURE

## 1. Final RP2 disposition

Record Grask RP2 as:

**RETOPOLOGY / PRODUCTION-MESH PILOT: AUTHOR ACCEPTED / FROZEN / VALIDATED FOR PROGRAM CONTINUATION**

The accepted production mesh remains:

`GR_U_REF_RP2_retopo_v003.blend`

- SHA-256: `03bfe7d924ff5b8b61a4c10095af5d16ca29d41667d7f61d0abeca14e1f07ce0`
- geometry hash: `f9c4a7ac98e86d98017376b9d67c85428503d2d6385258471d99bc766bfe702f`

No topology failure was demonstrated by the deformation studies.

Do not modify this asset.

---

## 2. Grask carry-forward items

Preserve the following explicitly for later production rigging:

### Elbow
- H2 = preferred diagnostic direction through 60–120°.
- 130° deep flexion remains an open production-rig/contact-corrective item.
- VC3 = best numeric 130° reference.
- overlap-aware physical volume relative to the straight elbow + local ring girth are the authoritative engineering volume measures for later work.
- RP2 elbow experimentation is closed.

### Shoulder
- SW3 = accepted Grask shoulder production direction.
- left flex90 anterior axillary-fold residual remains a named production-rig corrective item.
- LF2 = best diagnostic reference for that residual:
  - 0 non-contact pairs;
  - 1.3 mm crease depth;
  - orientation 111;
  - 2 local inversions;
  - 4 folds outside;
  - loop 0.525;
  - p95 / max strain 49.7 / 103%;
  - zone proxy −31.7%.
- RP2 shoulder experimentation is closed.

### Other retained decisions
- v002 knees remain diagnostic baseline.
- Nail Plate Rigidity v2 remains the correct nail diagnostic criterion.
- GH remains at the accepted diagnostic location.
- no source anatomy or retopology reopening is implied by any carry-forward item.

Create a concise closure record and update `specs/STATUS.md`.

---

## 3. Program transition ruling

Gorrund RP1 is already owner-frozen and closed.

Grask RP2 is now closed.

Therefore the two difficult pilots have validated the production-mesh program sufficiently to proceed to **RP3 — human / elf-derived families**, beginning with **Marchfolk** as specified by the master plan.

Do not start final production rigging before the race-production program reaches its later handoff stages.

---

# PART B — RP3 MARCHFOLK BASELINE

## 4. Authoritative Marchfolk sources

Use the accepted RP0 sources only.

### Configuration 1
`MF-M-R`

- source: `reviews/reference-assets/r6/MF-M-R_r6.npz`
- SHA-256: `2caaf056fff559c8c2c8b92dd5e2bc751be0c3efd9a98d0f8d4a7052f65be4d7`
- build: `reviews/reference-assets/builds/MF-M-R_build.json`
- build SHA-256: `c5be9ca0805f8ac298181cb0da42070bc4a4843fc0aa15129d4d8ba5f686c9ee`
- accepted provenance: W1c
- stature: 173.143 cm

### Configuration 2
`MF-F-R`

- source: `reviews/reference-assets/r6/MF-F-R_r6.npz`
- SHA-256: `c254fb4bc47225d90fcf7950514240cd74baace0ee3b48cd4d78fa38d9381761`
- build: `reviews/reference-assets/builds/MF-F-R_build.json`
- build SHA-256: `252907fda37c791dd3f5d5b547dc28886a8feeb14c7b1a79719667d49089de6d`
- accepted provenance: W1c
- stature: 172.9913 cm

Regenerate both sources with the recorded MPFB build path and prove geometry identity before deriving production assets.

The old PC `Marchfolk_Masc.blend` and other pre-RAC generator files are provenance only and must not be used as accepted source truth.

---

## 5. RP3 strategy — native topology first

Marchfolk is the baseline MPFB-family pilot.

The contract already establishes that the accepted MPFB family shares the hm08 topology:
- 13,380 body vertices;
- 13,378 quads;
- identical face index list;
- existing UVs;
- source rig / weights / shape keys available in the regenerated source.

Do **not** immediately rebuild the Marchfolk topology from scratch.

First determine whether the native hm08 quad body can serve as the **shared production base topology** after:
- helper removal;
- production cleanup;
- required face/orbit preparation;
- deformation-zone audit;
- creator-density audit;
- LOD-readiness tagging.

Only add or alter topology where the production contract actually requires it.

The goal is to establish the reusable MPFB-family base, not to create unnecessary topology divergence.

---

## 6. Source-helper removal

Derived Marchfolk production bodies must contain only the intended body skin.

Remove from production copies:
- MPFB helper eyes;
- teeth/tongue helper geometry;
- clothes/tights/skirt helpers;
- hair helpers;
- joint cubes;
- any other generator-only helper objects.

Do not delete them from regenerated source files.

The body must remain one closed manifold production mesh.

---

## 7. Configuration policy

Treat configuration 1 and configuration 2 as two accepted source realizations of the same Marchfolk race.

Do not collapse them into one averaged body.

Do not redefine sex-related biology.

If they can use the same production topology and vertex order, preserve that shared topology explicitly.

Produce independent fitted production realizations for both configurations, with a recorded common-topology mapping.

Suggested naming:

- `MF_M_REF_RP3_retopo_v001.blend`
- `MF_F_REF_RP3_retopo_v001.blend`

Use the repository's actual established naming convention if a more precise existing convention applies.

---

## 8. Phase 1 — native hm08 production audit

Before editing topology, audit the regenerated native body against the accepted contract.

Report separately for both configurations:

### Geometry integrity
- component count;
- boundaries;
- non-manifold edges/vertices;
- duplicates;
- degenerates;
- normals;
- self-intersections;
- quad percentage;
- pole locations;
- angle/aspect quality.

### Deformation-zone loop coverage
Audit contract §7:
- shoulder / axilla;
- clavicle/girdle;
- elbow;
- wrist;
- fingers;
- hip/groin/gluteal fold;
- knee;
- ankle;
- ball/toes;
- neck;
- spine/abdomen;
- mouth/jaw;
- eye/orbit.

Do not simply count rings globally; show actual closed-loop evidence at representative joints.

### Creator density
Audit §8 as mean edge length / stature:
- face;
- ears;
- hands/feet/digits;
- trunk/pelvis/gluteal;
- limbs.

Pay special attention to:
- face/orbit support for UFCA;
- hands/fingers;
- feet/toes;
- shoulders/axilla;
- pelvis/groin;
- abdomen/frame/composition zones.

### LOD readiness
Identify:
- continuous removable loop bands;
- silhouette-critical loops;
- regions that would collapse poorly;
- topology features that would prevent sane later LOD generation.

---

## 9. Face / eye / mouth production readiness

RP3 is the first phase where MPFB-derived face topology must be prepared for later real components.

The production body must support:
- separate eyeballs later;
- open/usable orbit topology;
- mouth-corner deformation;
- jaw-hinge deformation support;
- later separate teeth/tongue/mouth interior.

Do **not** create final eyeballs, teeth, tongue or oral interior in this order.

Do **not** invent new facial biology.

Cross-check with the accepted UFCA design.

If the existing native topology cannot support later facial customization cleanly, document the exact deficiency and make only the minimum justified topology change.

---

## 10. Production candidate policy

### If native hm08 passes
Create a production candidate largely preserving native topology, with only required cleanup/metadata/tagging and explicitly justified local changes.

### If native hm08 fails
Create one bounded `v002` topology candidate addressing only the documented failures.

Do not create an open-ended retopology cycle.

Do not propagate a changed family topology to other races until Marchfolk is explicitly accepted by ChatGPT.

---

## 11. Anatomy preservation

For every Marchfolk production candidate, validate against its own accepted source.

Use:
- stature / bbox;
- surface deviation;
- silhouette IoU;
- independently remeasured landmarks where applicable;
- identical-camera front/rear/profile/3-4;
- head;
- hands;
- feet;
- pelvis/groin;
- shoulder/axilla.

Do not morph configuration 1 toward configuration 2 or vice versa.

Preserve legitimate source asymmetry.

---

## 12. Rig-facing landmarks

Because Marchfolk is MPFB-derived, use the accepted source rig joint centres as the primary rig-facing landmark provenance where the contract permits.

Create versioned production landmark packages for both configurations.

Do not finalize the future game skeleton.

This stage should record:
- root/pelvis;
- hips;
- knees;
- ankles;
- balls/toes;
- SC/acromion/GH;
- elbows;
- wrists;
- MCP/IP/tips;
- spine_01–03;
- neck/head;
- jaw/eyes/mouth corners;
- ear root/tip.

Flag any source-rig landmark that is mechanically implausible rather than silently replacing it.

---

## 13. Diagnostic deformation — limited Marchfolk family gate

After a reference-stance production candidate passes geometry/anatomy checks, run a **small bounded diagnostic deformation set**, not the full Grask research cycle.

The purpose is to verify the baseline family topology can deform adequately before it is offered for propagation.

At minimum test:
- shoulder abduction 45° / 90°;
- shoulder flexion 90°;
- elbow 90° / 130°;
- wrist flex/ext;
- fist;
- thumb opposition;
- hip flexion 90°;
- knee 90° / deep flexion;
- ankle dorsiflexion;
- trunk twist;
- neck flex/rotation.

Use source-rig/diagnostic weights as a baseline.

Do not optimize production weights in RP3.

Classify failures as:
- topology;
- weights;
- joint placement;
- contact/test setup.

If a failure resembles a known Grask production-rig issue but the Marchfolk topology itself is adequate, do not launch another multi-cycle corrective program here.

---

## 14. Shared-topology family decision

Return a clear recommendation:

### FAMILY BASE PASS
The Marchfolk topology is suitable as the MPFB-family production base, subject to race-specific branches.

or

### FAMILY BASE NEEDS CORRECTION
The Marchfolk topology needs specific changes before reuse.

If PASS, identify which features are safe to propagate unchanged to:
- Skarn;
- Sagekin;
- Fenn;
- Aelari;
- Vael;
- Halvren;
- Durrim;
- Pipkin;
- Cogling.

Also identify which zones must branch per race, consistent with the contract.

Do **not** actually begin Skarn or another race in this order.

---

## 15. Required evidence

Provide actual inspectable sheets for both configurations:

- full-body front/rear/profile/3-4;
- topology/wire;
- face/orbit/mouth;
- shoulder/axilla;
- elbow;
- hand/fingers;
- pelvis/groin;
- knee;
- foot/toes;
- loop evidence;
- density heat/edge-length evidence;
- source-vs-production overlays;
- diagnostic deformation key poses.

Include common-topology mapping evidence between the two Marchfolk configurations.

---

## 16. Required return

Commit:

1. `reviews/claude-rac-rp2-grask-final-closure.md`;
2. `reviews/claude-rac-rp3-marchfolk-production-baseline-gate.md`;
3. Marchfolk production candidates / manifests / sidecars;
4. Marchfolk production landmark packages;
5. source-regeneration identity evidence;
6. topology / loop / density / quality audits;
7. anatomy-preservation measurements;
8. limited diagnostic deformation results;
9. visual evidence;
10. common-topology mapping evidence;
11. before/after source hashes;
12. reproducible tools;
13. narrow `specs/STATUS.md` and session-handoff update.

The Marchfolk gate must explicitly answer:

- Does native hm08 pass as the shared production base?
- What local topology changes, if any, were required?
- Are configuration 1 and 2 on the same final vertex/face topology?
- Do both preserve their accepted anatomy?
- Do both satisfy deformation-loop requirements?
- Do both satisfy creator-density requirements?
- Is face/orbit/mouth topology adequate for later UFCA/facial production?
- What diagnostic deformation failures remain, and what class are they?
- Is the MPFB-family base ready for explicit author acceptance and later propagation?

---

## 17. Stop rules

After committing the Marchfolk gate:

**STOP FOR CHATGPT REVIEW.**

Do not proceed to:
- Skarn;
- Sagekin;
- any other race;
- family-wide topology propagation;
- production rig finalization;
- production skin freeze;
- creator morph implementation;
- UV/material finalization;
- LOD generation;
- UE5.

---

## FINAL AUTHOR RULING

- Grask RP2 is formally closed as a successful production-mesh pilot.
- Its remaining elbow/shoulder edge cases are production-rig carry-forward items, not topology failures.
- Final Grask production rigging is deferred until the broader production-mesh program reaches its appropriate handoff stage.
- RP3 begins with Marchfolk.
- Marchfolk will establish the shared MPFB-family production base before any family propagation.
