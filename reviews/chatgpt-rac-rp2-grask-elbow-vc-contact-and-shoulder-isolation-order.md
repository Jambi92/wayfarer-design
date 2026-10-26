# RAC RP2 — Grask 130° elbow volume-conserving contact + independent shoulder isolation order

**Date:** 2026-10-26  
**Authority:** Tyler / ChatGPT review of Claude Stage A helper-volume return `fe125b1beba8b29d7fb3b777cf09c1a83acd2cf6`.  
**Parent gate:** `reviews/claude-rac-rp2-grask-elbow-helper-volume-shoulder-isolation-gate.md`.  
**Status entering this order:** Grask RP2 retopology remains AUTHOR ACCEPTED / FROZEN / CLOSED. Production deformation remains **not accepted**.

This order resolves D-1…D-4 from the Stage A return and authorizes two bounded diagnostic tracks:

- **Track E:** one final 130° elbow contact-redistribution study;
- **Track S:** shoulder failure isolation, now authorized independently of the elbow outcome.

Neither track authorizes production rigging or topology edits.

---

## 1. Immutable parents / hard firewall

Do not edit, resave over, reproject, smooth, retopologize, symmetrise, or otherwise modify:

- `GR_U_REF_RP2_retopo_v003.blend`
- `GR_U_REF_RP2_SOURCE_3D_v005.blend`
- frozen v003 sidecars / landmark package / freeze record
- v001 / v002 retopo provenance
- prior diagnostic rigs, configs, weights, helper records, corrective records, or evidence packages

The accepted rest mesh remains exactly the frozen v003 geometry.

No v004 retopology is authorized.

No production rig, production skinning, facial/oral component work, creator morphs, UVs, materials, LODs, UE5 integration, animation, or another race is authorized.

Parent hashes must be captured before and after all work. Stop on any mismatch.

---

# AUTHOR RULINGS

## 2. D-1 — elbow configuration by flexion range

### 60–120°
H2 is accepted as the **best diagnostic configuration below 130°**.

That means:
- retain H2 as the preferred diagnostic reference through 60°, 75°, 90°, 110° and 120°;
- do not call H2 production-ready;
- do not erase C2/C2rx provenance.

### 130°
H2 is **not accepted** at 130° because of the demonstrated crease, orientation and strain regressions.

For 130°:
- C2/C2rx remain the clean comparison baseline;
- the new Track E experiment will attempt one volume-conserving contact-redistribution solution.

Do not force one single corrective architecture to cover all angles if the evidence supports angle-specific behavior.

---

## 3. D-2 — helper local scale

The local-scale helper behavior used in H2/H3 is accepted as a **diagnostic helper mechanism**.

It is not final production-skeleton canon.

Record scale values explicitly and keep the mechanism isolated to diagnostic rigs.

Do not infer race biology or final muscle architecture from helper scale.

---

## 4. D-3 — 130° elbow decision

Do **not** declare 130° a hard Grask anatomical limit yet.

Authorize exactly one bounded attempt at **volume-conserving contact redistribution**, not another generic helper-proliferation cycle.

Preferred method: corrective/contact solve that redistributes displaced volume instead of simply flattening both surfaces or bulging laterally.

A second biceps-side helper is **not authorized in this order**.

If the volume-conserving contact approach fails, stop and return the evidence. Do not create more helper chains.

---

## 5. D-4 — shoulder

Authorize shoulder failure isolation **independently now**.

Track S does not wait for Track E to pass.

The goal is classification, not production-quality shoulder deformation.

---

# TRACK E — FINAL 130° ELBOW CONTACT-REDISTRIBUTION STUDY

## 6. Scope

Focus only on deep elbow flexion behavior, centered on **130°**.

Use:
- v002 diagnostic landmarks;
- W0 baseline weights;
- LBS;
- H2 as the accepted 60–120° diagnostic reference;
- C2/C2rx as the 130° comparison baseline;
- frozen v003 rest geometry.

No pivot changes.

No topology changes.

No global weight redesign.

---

## 7. Contact-redistribution concept

The problem to solve is:

> At 130°, C2/C2rx eliminate non-contact penetration but lose substantial closed volume by flattening the forearm–biceps contact interface; H2 restores only part of that volume and then produces deeper crease failure and strain.

The new method must conserve or redistribute soft-tissue mass **within the local elbow-contact region**.

Allowed mechanisms:
- local contact-aware displacement solve;
- local volume-preserving corrective field;
- constrained Laplacian / ARAP-style redistribution;
- divergence/volume constrained displacement;
- bounded outward redistribution distributed over upper-arm and forearm support rather than a single side bulge.

The method may use separate upper-arm and forearm support masks, but they are corrective support regions, **not new helper bones**.

Do not:
- push volume into the wrist, hand, shoulder, torso or unrelated anatomy;
- create a visible isolated biceps lump;
- create a pipe-like forearm;
- hide contact by translating the entire limb;
- edit the frozen rest mesh.

---

## 8. Candidate limit

At most **three** Track E candidates:

- **VC1:** base volume-conserving contact redistribution;
- **VC2:** one bounded refinement if VC1 exposes a specific localized failure;
- **VC3:** one final bounded refinement only if VC2 is close but fails one clearly isolated criterion.

No broader search tree.

Each candidate must be reproducible from committed configs/tools.

---

## 9. Required elbow test angles

Primary:
- 120°
- 130°

Regression/sanity:
- 90°
- 110°

Both left and right.

Below 120°, do not displace H2 unless the new method has a non-zero activation there. If it does, prove there is no regression.

---

## 10. Track E acceptance criteria

A Track E candidate is acceptable for further production-rig planning only if all of the following are satisfied:

### Integrity
- 0 non-contact intersections at 130° both sides;
- no new local inversions;
- no folds outside declared crease/contact zones;
- rest return effectively zero.

### Crease/contact
- 130° crease depth no worse than C2/C2rx by more than 0.5 mm;
- preferred target:
  - left <= 3.5 mm;
  - right <= 3.5 mm.

### Orientation
- no material regression over C2/C2rx;
- preferred:
  - left <= 100 disagreement faces;
  - right <= 90 disagreement faces.

### Loop spacing
- >= 0.50 of rest at 130° both sides;
- do not sacrifice loop spacing to restore volume.

### Closed volume
This is the main target.

Relative to C2/C2rx:
- reduce corrective-caused 130° closed-volume loss by **at least 50%**;
- preferred stronger target: <= 120 cm³ absolute loss per side if achievable without regressions.

Report both:
- closed-mesh dV vs W0;
- percentage improvement vs C2/C2rx.

### Zone/cone proxy
Must move materially toward the physical-volume behavior of W0 / DQS rather than farther away.

Do not accept a solution that improves only global closed volume while worsening local zone collapse.

### Strain
- p95 strain no more than +5 percentage points over C2/C2rx;
- max strain must not show a new concentrated spike comparable to H2's failed 130° case;
- show strain maps.

### Visual
At 130°:
- contact should read as flesh compression;
- no upper-crease spike;
- no shelf, ridge, balloon, pipe or isolated muscle bulge;
- outer elbow contour remains believable;
- preserve accepted Grask long-limb read.

---

## 11. Required Track E evidence

Provide for both sides:

- W0 vs C2/C2rx vs H2 vs selected VC candidate;
- 120° and 130° identical-camera clay;
- wire closeups;
- flexion-plane sections;
- closed-volume plots;
- zone/cone proxy plots;
- loop-spacing plots;
- p95/max strain plots and maps;
- contact/intersection overlays;
- orientation/inversion overlays;
- displacement field visualization;
- support-mask visualization;
- rest-return check.

Explicitly answer:

1. Did 130° volume loss improve by >=50%?
2. Did crease depth stay within +0.5 mm of C2/C2rx?
3. Did loop spacing remain >=0.50?
4. Was any new orientation/local-inversion regression introduced?
5. Does the visual read improve without a compensating bulge artifact?

If no candidate passes, **stop Track E**. Do not declare 130° an anatomical limit yet; simply return it as an unresolved production-deformation problem for author ruling.

---

# TRACK S — SHOULDER FAILURE ISOLATION

## 12. Purpose

Determine whether the current D1 shoulder/girdle failures are primarily:

- mechanics;
- weighting;
- joint placement;
- topology contribution;
- contact classification;
- or mixed.

Do not attempt final shoulder deformation.

Use the existing accepted diagnostic landmark architecture unless a direct mechanical contradiction is demonstrated.

---

## 13. Shoulder baseline

Use:
- v002 diagnostic landmarks;
- W0 baseline;
- frozen v003 rest mesh;
- LBS;
- existing SC / acromion / scapular proxy / GH structure.

No source anatomy edits.

No GH relocation unless a dedicated comparison proves current placement is mechanically impossible.

---

## 14. Shoulder candidates

At most **two** new shoulder candidates:

### S1 — mechanics variant
Introduce a diagnostic shoulder-girdle motion model using existing proxies:
- clavicular elevation/rotation;
- scapular upward rotation;
- scapular posterior/lateral translation if needed;
- GH motion remains tied to the accepted diagnostic centre.

Use a simple, reproducible shoulder-elevation rule.

Do not claim production anatomy.

### S2 — bounded weighting comparison
Only if S1 shows that mechanics help but local deformation remains limited.

S2 may adjust local diagnostic shoulder/axillary weights in a bounded region to separate mechanics from weighting.

No production-quality weight sculpting.

---

## 15. Shoulder tests

Both left and right:

- abduction 45°;
- abduction 90°;
- flexion 90°;
- extension 30°;
- existing girdle-enabled abduction/flexion variants.

Also include rest/low-angle sanity.

---

## 16. Shoulder measurements

For every candidate/pose report:

- non-contact intersections;
- axillary contact depth;
- orientation disagreement;
- local inversions;
- folds outside intended crease/contact zones;
- loop-spacing collapse;
- p95/max strain;
- local volume proxy;
- GH-to-acromion relationship;
- clavicle motion;
- scapular-proxy motion;
- visible deltoid continuity;
- axillary contour continuity;
- rest-return integrity.

---

## 17. Shoulder visual package

Identical cameras:

- front;
- rear;
- 3/4 front;
- 3/4 rear;
- axillary closeup;
- wireframe closeup;
- shoulder contour/cross-section where useful.

Overlay:
- SC;
- acromion;
- scapular inferior proxy;
- scapular medial proxy;
- GH;
- support/weight boundaries;
- contact/intersection regions.

---

## 18. Shoulder classification

Return exactly one primary classification, plus secondary contributors if needed:

- **MECHANICS-DOMINANT**
- **WEIGHTING-DOMINANT**
- **JOINT-PLACEMENT-DOMINANT**
- **TOPOLOGY-CONTRIBUTING**
- **CONTACT-CRITERION-DOMINANT**
- **MIXED / INCONCLUSIVE**

Support the classification with measurements and visuals.

If topology is contributing, do **not** edit retopology. Stop for review.

---

# CROSS-TRACK CONTROLS

## 19. Nail and knee state

- Nail Plate Rigidity v2 remains gating.
- Nail Cap Historical v1 remains report-only.
- v002 knee placement remains the diagnostic baseline.
- No knee revision in this order.

---

## 20. Diagnostic-rig files

Derived diagnostic files may be created.

Suggested:
- `GR_U_REF_RP2_rigdiag_v006_elbow.blend`
- `GR_U_REF_RP2_rigdiag_v006_shoulder.blend`

or one clearly separated v006 diagnostic file if both tracks can coexist without interaction.

Every diagnostic file must:
- preserve frozen v003 Basis/rest geometry;
- be tagged DIAGNOSTIC / NON-PRODUCTION;
- log active helpers/correctives/weights;
- include exact file and geometry hashes.

Do not overwrite v001–v005 diagnostic files.

---

## 21. Regression policy

If Track E selects a candidate:
- run the relevant elbow arc;
- run the unchanged 43-pose full suite if the selected corrective has any nonzero influence outside D2;
- otherwise document zero influence and prove unrelated poses bit-identical.

If Track S changes only D1 shoulder mechanics:
- run all D1 poses plus any pose where the new bones/weights have non-zero influence;
- prove unrelated regions remain unchanged.

Any unexpected cross-region regression is a stop condition.

---

## 22. Required return

Commit:

1. `reviews/claude-rac-rp2-grask-elbow-vc-contact-and-shoulder-isolation-gate.md`;
2. Track E configs/tools;
3. Track E evidence package;
4. Track S configs/tools;
5. Track S evidence package;
6. diagnostic file manifests/hashes;
7. parent before/after hashes;
8. narrow `specs/STATUS.md` update;
9. session handoff.

The gate must state:

### Track E
- selected candidate or none;
- 130° closed-volume improvement percentage left/right;
- crease depth;
- orientation disagreements;
- loop ratio;
- p95/max strain;
- whether all §10 criteria passed;
- whether 130° remains unresolved.

### Track S
- S1/S2 results;
- primary shoulder classification;
- whether mechanics materially improve the shoulder;
- whether weighting materially improves the shoulder;
- whether joint placement appears implausible;
- whether topology contribution remains.

### Global
- parent integrity;
- any regression;
- whether production deformation is accepted (**it is not automatically accepted by this order**);
- exact next author decision required.

---

## 23. Stop rules

STOP FOR CHATGPT REVIEW after both tracks are complete.

Do not proceed to:

- production rig finalization;
- production skinning;
- new helper chains;
- topology edits;
- facial/oral/eye work;
- creator morphs;
- UV/materials;
- LODs;
- UE5;
- another race.

---

## FINAL AUTHOR RULING

- Grask RP2 retopology remains **ACCEPTED / FROZEN / CLOSED**.
- H2 is the preferred diagnostic elbow configuration through 60–120°.
- C2/C2rx remain the 130° comparison baseline.
- One final 130° volume-conserving contact-redistribution study is authorized.
- Shoulder failure isolation is independently authorized now.
- No topology or source-anatomy reopening is authorized.
