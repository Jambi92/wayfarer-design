# RAC RP3 — Marchfolk v003 family-base freeze + conditional Skarn propagation order

**Date:** 2026-10-26  
**Authority:** Tyler / ChatGPT review of Claude Marchfolk final family-core return `22966487dd84d8af264ad7fec46d04d8ef0a2d9f`.  
**Parent gates:**  
- `reviews/claude-rac-rp3-marchfolk-family-core-v003-gate.md`  
- `reviews/claude-rac-rp3-marchfolk-v004-final-family-core-gate.md`  

**Program references:**  
- `specs/RAC_PRODUCTION_MESH_CONTRACT.md`  
- `reviews/chatgpt-rac-retopology-rigprep-master-plan.md`  
- RP0 source inventory / family policy.

This order has two sequential parts:

1. **formally accept and freeze Marchfolk v003 as the shared MPFB-family production base**;  
2. **only after the freeze read-back passes, propagate that frozen family base to Skarn as the first family-sharing validation race.**

Do not start Sagekin or any other race in this order.

---

# PART A — MARCHFOLK v003 FORMAL AUTHOR ACCEPTANCE / FAMILY-BASE FREEZE

## 1. Final author decisions

### D1 — accepted
Keep the standardized validator behavior already implemented:

- use the ordinary band method when a valid outward-facing endpoint exists;
- when the band ray is geometrically undefined, do not use tie order as a geometry verdict;
- use the documented anatomical closed-ring / defined-side fallback;
- report the fallback mode explicitly.

Accepted fallback stations:

- `thumb_mcp_l`, configuration 1: `PASS_FALLBACK_CLOSED_RING`;
- `thumb_mcp_l`, configuration 2: `PASS_FALLBACK_CLOSED_RING`;
- configuration-2 `shoulder_l`: `PASS_FALLBACK_DEFINED_SIDES`;
- configuration-2 `shoulder_r`: `PASS_FALLBACK_DEFINED_SIDES`.

No geometry change is authorized for these stations.

---

## 2. D3 — digit pole ownership ACCEPTED

Adopt the proposed digit-ownership rule as the standard production validator rule:

> For finger, thumb and toe joint stations, a pole counts against the audited joint only if the pole belongs to the **same digit** being audited, determined by the nearest valid digit axis / chain on that hand or foot.

A neighboring digit's legitimate tip-cap pole must not be counted as a crease pole for the audited digit merely because the station search radius overlaps the adjacent digit.

Therefore the following former toe-IP failures are accepted as **validator-attribution false positives**, not topology defects:

- config 1: `toe3_j3_l/r`;
- config 2: `toe3_j3_l/r`;
- config 2: `toe4_j2_l/r`.

Under D1 + D3:

**Both Marchfolk configurations have 69 / 69 firm station PASS.**

Preserve the remaining strict-only observations as quality notes; they are not blocking firm failures.

Update the reusable validator implementation and documentation so future MPFB-family races use these rules consistently.

---

## 3. Configuration-1 sole note ACCEPTED

Accept the configuration-1 v003 sole's lowest point at approximately **+0.41 mm** relative to ground.

Reason:

- within T-3;
- multiple sole vertices remain within 1 mm of ground;
- sole remains flat-capable;
- no visible or gameplay-relevant anatomy issue;
- another geometry edit is not justified.

Do **not** re-pin the sole.

Record the +0.41 mm value as a freeze note only.

---

## 4. Marchfolk family-base artifacts accepted

### Configuration 1

`MF_M_REF_RP3_retopo_v003.blend`

- SHA-256:  
  `5b793eda8d4513a31fa018ef095d2eff25821618b297014a243ec472f6e17276`
- geometry hash:  
  `64ecbff04faf3615e45ee452bc117fc6a49195d9611edb2f1abce64c2f3041da`
- face topology hash:  
  `68f7b6a90a40917e40f2ab191218ab7ae2245d0cb1b1b20ede2fe5b56e5e8262`

### Configuration 2

`MF_F_REF_RP3_retopo_v003.blend`

- SHA-256:  
  `a5d8adfe979e0c6314ddc825062f6f953a24a1288f79c987dff5232ef45dc188`
- geometry hash:  
  `ebf5829d9e6d98192a1fb2771b48feb8983027b22f8c0875bfe1d9c14b6599d4`
- face topology hash:  
  `68f7b6a90a40917e40f2ab191218ab7ae2245d0cb1b1b20ede2fe5b56e5e8262`

Shared topology:

- **57,674 vertices**
- **57,672 quads**
- 100% quads
- identical face list
- identical topology hash
- identical hm08 mapping structure
- identical common topology architecture

Accepted mapping:

- hm08 → v003 map SHA-256:  
  `bc3b7c548293a2a653e89c13e37c7088b5f12fdb42968fdb6bd9147cfd248a17`
- v002 → v003 map SHA-256:  
  `0829d1dc596299bb36a2737ae113400fa88e027fd126a8effb216b6f2b3ae475`

---

## 5. Freeze meaning

The Marchfolk v003 topology is hereby accepted as:

> **THE SHARED MPFB-FAMILY PRODUCTION BASE TOPOLOGY**

subject to race-specific branches required by the contract.

This freezes:

- common vertex / face topology;
- hm08 → family-base mapping architecture;
- D1 validator fallback rules;
- D3 digit pole ownership rule;
- shared production frame/origin convention;
- source weight-transfer method;
- UV-transfer method;
- MPFB target/morph-transfer method;
- base deformation-loop organization;
- base creator-density architecture;
- base face/orbit/mouth production-readiness topology.

This does **not** freeze:

- final production skeleton;
- production skin weights;
- race-specific ear branches;
- compact-race density branches;
- race-specific anatomy;
- final UV layout/materials;
- creator morph implementation;
- LOD policy.

---

## 6. Freeze-by-record / read-back verification

Preserve the accepted v003 `.blend` files byte-identically where practical.

Do not resave the accepted files merely to change an embedded status string if that changes their SHA-256.

Use a separate authoritative freeze record if needed, as done for Grask.

After creating the freeze record, re-stage/read back both accepted Marchfolk files and verify:

- exact accepted file SHA-256;
- exact geometry hash;
- exact face topology hash;
- 57,674 vertices;
- 57,672 quads;
- 100% quads;
- one component;
- zero boundary edges;
- zero non-manifold edges / vertices;
- no new degenerates;
- outward normals;
- mappings preserved;
- UV transfer path preserved;
- source/morph/weight transfer paths preserved;
- D1 + D3 validator = 69 / 69 firm PASS on both configs;
- anatomy T-1 / T-2 / T-3 / T-7 preserved;
- all creator-density zones preserved;
- face/UFCA readiness preserved;
- source hashes unchanged.

Create:

`reviews/claude-rac-rp3-marchfolk-v003-family-base-freeze-report.md`

and a versioned freeze manifest / record under the Marchfolk RP3 evidence or production directory.

Update `specs/STATUS.md` unambiguously to:

**MARCHFOLK RP3 v003 — AUTHOR ACCEPTED / FROZEN — MPFB FAMILY BASE**

---

# PART B — CONDITIONAL SKARN PROPAGATION / SHARING TEST

Proceed only after Part A passes exact freeze verification.

If any Marchfolk freeze hash or read-back check fails, STOP before Skarn.

---

## 7. Skarn authoritative sources

Use only the accepted RP0 sources.

### Configuration 1

`SK208-C1R`

- role: c1 reference body + accepted C1R central face
- source:  
  `reviews/rac-w3d-evidence/geometry/SK208-C1R_r6.npz`
- SHA-256:  
  `fd8a43d2e6dc6e63f21306755baedd70cfef9151ff2b4fd442ad1a78ed4448d0`
- build:  
  `reviews/rac-w3d-evidence/builds/SK208-C1R_build.json`
- build SHA-256:  
  `c1c54d286b23e1b3e2f7ad30ba36462fc0b2aaf560364f40fe0f34a4675f5231`
- accepted provenance: W3D C1R
- stature: ~208.006 cm

### Configuration 2

`SKF208`

- source:  
  `reviews/reference-assets/r6/SKF208_r6.npz`
- SHA-256:  
  `0245683ec889d36e4d284ad0fe4ae533a3c7ab8ce17c28e46cda92a99769ab4f`
- build:  
  `reviews/reference-assets/builds/SKF208_build.json`
- build SHA-256:  
  `ddf77a849902c1843b825396a4f21272ea66d4d80e1bd78acdecab609d4c377a`
- accepted provenance: W2B
- stature: ~208.009 cm

Regenerate both accepted Skarn sources and prove geometry identity before fitting the family base.

Do not use older prototype Skarn files as production truth.

---

## 8. Propagation principle

Skarn is the **first validation that the frozen Marchfolk family base can actually be reused on another race without cheapening race identity**.

Start from the frozen Marchfolk family topology and hm08 mapping architecture.

Do not independently retopologize Skarn.

The task is:

> Fit the frozen MPFB-family topology to each accepted Skarn source through the shared hm08 map, then test whether the result preserves Skarn anatomy within the production contract.

The topology must stay identical to the frozen family base unless a true Skarn-specific branch is justified.

The contract currently names **no pre-authorized Skarn topology branch**.

Therefore:

- no topology changes by default;
- if Skarn anatomy cannot be preserved with the frozen family base, STOP and document the exact reason before branching.

---

## 9. Skarn candidate files

Suggested names:

- `SK_M_REF_RP3_retopo_v001.blend`
- `SK_F_REF_RP3_retopo_v001.blend`

Use the project's established configuration codes if a more precise naming rule already exists.

Both candidates must use:

- exactly **57,674 vertices**;
- exactly **57,672 quads**;
- frozen family face topology hash;
- frozen family mapping architecture;
- same D1/D3 validator rules.

The M/F Skarn candidates must have identical topology to one another and to the frozen Marchfolk family base.

---

## 10. Skarn source-fit / anatomy gates

For each configuration independently rerun:

- T-1 surface deviation;
- T-2 identity-zone preservation;
- T-3 stature / bbox;
- T-7 silhouette IoU;
- head / face;
- ears;
- hands;
- feet;
- shoulder/girdle;
- pelvis/groin;
- knee/ankle;
- Skarn-specific body proportions and accepted face identity.

Configuration 1 must preserve the accepted **C1R central face**.

Do not regress the C1R face toward generic MPFB/Marchfolk facial structure.

This is a hard race-identity gate.

Return identical-camera:

- front;
- rear;
- profile;
- 3/4;
- head/face closeup;
- hands;
- feet;
- shoulder;
- pelvis.

---

## 11. Loop / validator audit

Run the standardized family validator on all 69 stations for both Skarn configs using:

- D1 undefined-band fallback;
- D3 same-digit pole ownership.

Required:

- 69 / 69 firm PASS in both configurations;
- fallback modes explicitly identified;
- strict-only observations listed separately.

Do not modify geometry to satisfy a measurement method that is undefined.

---

## 12. Creator density

Re-run all family density zones using Skarn stature.

All contract ceilings must pass.

Because Skarn is significantly taller than Marchfolk, explicitly report:

- mean edge / stature;
- p95 edge / stature;
- whether any zone is now over-dense or unnecessarily heavy relative to the production target.

Do **not** decimate merely because Skarn is taller.

The family topology consistency is more important than shaving vertices unless a later performance contract says otherwise.

---

## 13. Face / UFCA readiness

Confirm:

- mouth rings preserved;
- orbit rings preserved;
- open orbit / lip pockets valid;
- C1R face remains preserved;
- no mouth-corner pole regression;
- face density adequate.

Do not create final facial components.

Do not redesign Skarn face anatomy.

---

## 14. Mapping / transfer proof

For both Skarn configurations prove:

- accepted source hm08 → frozen family base mapping;
- weights transfer;
- UV transfer;
- MPFB target/morph transfer compatibility;
- identical topology hash to frozen family base.

Create a family propagation manifest recording:

- frozen Marchfolk family-base commit/hash;
- Skarn source hashes;
- generated Skarn production hashes;
- mapping hashes;
- topology identity proof.

This should become the reusable propagation workflow for later MPFB-family races if accepted.

---

## 15. Limited Skarn diagnostic deformation

Run a compact validation, not another Grask-style research program.

At minimum:

- shoulder abd45;
- shoulder abd90;
- shoulder flex90;
- elbow 90;
- elbow 130;
- wrist flex/ext;
- fist;
- thumb opposition;
- hip flex90;
- knee 90 / deep flex;
- ankle dorsi;
- trunk twist;
- neck flex/rotation.

Use source rig / source weights transferred through the frozen family map.

Classify failures:

- topology;
- weights;
- joint placement;
- contact/setup.

The acceptance question is:

> Does the frozen family topology behave at least as well as the accepted Skarn source topology under equivalent rig/weights, without introducing a topology-class failure?

Do not launch corrective-weight development.

---

## 16. Family-standardization capture

Because the user has directed us to standardize repeatable work without cheapening the game, this Skarn run must explicitly identify what is now reusable.

If Skarn passes, package/document the following as the **MPFB Family Propagation Standard v1**:

1. source regeneration identity check;
2. hm08 → frozen family-base mapping;
3. helper removal;
4. production frame/origin;
5. topology identity check;
6. D1/D3 joint validator;
7. density audit;
8. anatomy T-1/T-2/T-3/T-7;
9. face readiness audit;
10. limited deformation sanity;
11. visual evidence set;
12. freeze/acceptance gate template.

Do not standardize race-specific anatomy judgments.

The reusable pipeline is technical; the anatomy/identity gate remains race-specific.

---

## 17. Skarn gate decision

Return exactly one:

### SKARN FAMILY PROPAGATION PASS — READY FOR AUTHOR FREEZE

Use if:

- both Skarn configs preserve accepted anatomy;
- C1R face passes;
- frozen family topology remains unchanged;
- 69/69 firm stations pass;
- density passes;
- face readiness passes;
- no topology-class deformation failure appears;
- mappings/transfer paths pass.

### SKARN FAMILY PROPAGATION NEEDS RACE-SPECIFIC BRANCH

Use only if a real Skarn anatomy requirement cannot be preserved by the frozen family base.

Specify exact zone and why.

Do not build the branch in this order unless it is a trivial mapped correction already permitted by existing canon; otherwise stop.

### SKARN PROPAGATION FAIL

Use if a blocking issue invalidates the frozen family topology for Skarn.

---

## 18. Required visual evidence

Provide actual inspectable sheets for both Skarn configurations:

- full body clay / wire;
- source vs production overlay;
- C1R face closeup;
- face/orbit/mouth topology;
- shoulder;
- elbow;
- hand;
- pelvis;
- knee;
- foot;
- density heat;
- counted joint loops / fallback labels;
- limited deformation comparison.

Do not return the gate without photos.

---

## 19. Required return

Commit:

### Marchfolk
1. `reviews/claude-rac-rp3-marchfolk-v003-family-base-freeze-report.md`;
2. freeze manifest/record;
3. D1/D3 validator documentation;
4. exact freeze/read-back hashes;
5. STATUS update.

### Skarn
6. `reviews/claude-rac-rp3-skarn-family-propagation-gate.md`;
7. Skarn production candidates / sidecars;
8. propagation manifest;
9. source regeneration identity evidence;
10. anatomy-preservation audit;
11. loop/validator audit;
12. density audit;
13. face/C1R audit;
14. limited deformation results;
15. visual sheets;
16. before/after hashes;
17. reusable **MPFB Family Propagation Standard v1** draft;
18. session handoff.

The Skarn gate must explicitly answer:

- Did Marchfolk freeze verify exactly?
- Are both Skarn configs using the frozen family topology unchanged?
- Does C1R identity pass?
- Do all anatomy tolerances pass?
- Are all 69 firm stations passing?
- Do all density zones pass?
- Is face/UFCA readiness intact?
- Did any topology-class deformation failure appear?
- Is a Skarn-specific topology branch needed?
- Is the propagation process ready to standardize for subsequent MPFB-family races?

---

## 20. Stop rules

After committing the Skarn gate:

**STOP FOR CHATGPT REVIEW.**

Do not proceed to:

- Sagekin;
- Fenn;
- Aelari;
- Vael;
- Halvren;
- Durrim;
- Pipkin;
- Cogling;
- family-wide batch propagation;
- production rig finalization;
- creator morph implementation;
- final UV/materials;
- LODs;
- UE5 integration.

---

## FINAL AUTHOR RULING

- Marchfolk v003 is **AUTHOR ACCEPTED** as the shared MPFB-family production base.
- D1 fallback logic is accepted.
- D3 same-digit pole ownership is accepted.
- The +0.41 mm configuration-1 sole note is accepted.
- Freeze Marchfolk v003 exactly.
- After freeze verification, propagate the frozen family base to Skarn as the first reuse validation race.
- Standardize the technical propagation process if Skarn passes, but preserve race-specific anatomy review as an explicit human/author gate.
