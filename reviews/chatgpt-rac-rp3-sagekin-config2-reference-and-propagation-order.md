# RAC RP3 — Sagekin configuration-2 central reference + conditional MPFB family propagation order

**Date:** 2026-10-27  
**Authority:** Tyler / ChatGPT review following freeze commit `1e43fa5e5b478074eaa055412f02fc1baa1a32bc`.  
**Program references:**  
- `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md` — AUTHOR-ACCEPTED TECHNICAL STANDARD v1;  
- `specs/RAC_PRODUCTION_MESH_CONTRACT.md`;  
- `specs/sagekin/SAGEKIN_V1.md`;  
- RP0 source inventory;  
- active MPFB Family Base v005 freeze record.

This order has two sequential parts:

1. create and validate the missing Sagekin configuration-2 central reference at the canonical ~178 cm reference stature;
2. only if Part A passes the objective reference gates, propagate the active frozen MPFB family base to both Sagekin configurations and return the Sagekin RP3 gate.

Do not freeze Sagekin in this order.

---

# PART A — CREATE / VALIDATE SAGEKIN CONFIGURATION-2 CENTRAL REFERENCE

## 1. Canonical Sagekin source state

### Configuration 1 — accepted central reference

`SG`

- source: `reviews/reference-assets/r6/SG_r6.npz`
- SHA-256:  
  `fe45866ffad7d771aacfeea72cddad8aedc2f205dfb25178bd26aa3cf144adf3`
- build: `reviews/reference-assets/builds/SG_build.json`
- build SHA-256:  
  `e39eff0da68ec79226e7100c7750e694c91de7427b0feac363079693bd008ead`
- accepted: W1c
- stature: ~177.989 cm

### Configuration 2 — accepted stature bounds only

Minimum:
`SGF152-NAT`

- source: `reviews/reference-assets/r6/SGF152-NAT_r6.npz`
- SHA-256:  
  `9f096ff65f5be688d1bc9625b1d441d7d78954494cbf57191db24115c7e6c885`
- build: `reviews/reference-assets/builds/SGF152-NAT_build.json`
- build SHA-256:  
  `4dff21587dab7d98fd66806a0cc8c74b72dce6fb80843c2e61d186b37eca6b60`
- accepted role: c2 minimum bound
- stature: ~151.997 cm

Maximum:
`SGF208`

- source: `reviews/reference-assets/r6/SGF208_r6.npz`
- SHA-256:  
  `adb02cc63f3a4a55d74c28a0262c363f4b2238428b34f44b07e3f61e5f169fec`
- build: `reviews/reference-assets/builds/SGF208_build.json`
- build SHA-256:  
  `359ee2f5d6a2a5c0ccba23aebaf2166fb04ccbaac5abd3583a4036d423d4819f`
- accepted role: c2 maximum bound
- stature: ~208.006 cm

There is currently **no committed accepted configuration-2 central reference**.

Do not use either stature bound as the production central anchor.

---

# 2. Author direction for the missing central reference

Create a new Sagekin configuration-2 central-reference candidate at approximately **178 cm**.

Recommended ID:

`SGF178`

or project-consistent equivalent if an existing local diagnostic build already uses that ID.

The target is a **central anchor**, not a new biological extreme.

It must represent the accepted Sagekin configuration-2 anatomy at the canonical reference stature and must not simply interpolate appearance between SGF152-NAT and SGF208 unless the existing build system/canon explicitly defines that as the correct configuration-2 path.

---

# 3. Sagekin biology / identity constraints

Preserve the Sagekin canon from `specs/sagekin/SAGEKIN_V1.md`.

Sagekin are:

- fully human;
- not elf-like;
- not defined biologically by scholarship, intelligence, frailty, occupation, or personality;
- overlapping with Marchfolk by design;
- allowed Narrow / Balanced / Broad frames and full human composition range;
- slightly longer-limbed / more linear as a population tendency only;
- human hands and feet;
- human auricle family;
- distinct through overlapping craniofacial/proportional population tendencies, not caricature.

Do not exaggerate the config-2 reference merely to make it look more different from Marchfolk.

---

# 4. Central-reference stature / proportion target

Target stature:

**~178 cm**

Use the canonical Sagekin reference stature from the accepted spec.

Hard rule:

- do not use uniform whole-body scaling as the production solution;
- use the established MPFB / DIR architecture so joint relationships and anatomy remain coherent.

The new reference should sit naturally inside the accepted 152–208 cm envelope.

---

# 5. Build provenance

If an existing local `SGF178` diagnostic build exists:

1. locate it;
2. document exactly where it came from;
3. compare it to current accepted Sagekin config-2 bounds and current Sagekin spec;
4. do not assume it is accepted merely because it exists.

If no usable local diagnostic exists:

build the central reference from the accepted Sagekin config-2 architecture using the same MPFB version / build pipeline as the accepted sources.

Record:

- MPFB version;
- all sliders/macros / configuration values;
- height macro;
- pose / grounding sequence;
- source build record;
- generated R-6 source;
- geometry hash;
- SHA-256;
- rebuild identity.

---

# 6. Central-reference validation

Before family propagation, validate the new config-2 central reference itself.

Required:

### Geometry integrity
- one component;
- no boundary edges;
- no non-manifold edges;
- no degenerates;
- no duplicate/coincident defects;
- valid orientation / normals;
- rebuild geometry-identical.

### Stature
- target ~178 cm;
- report exact stature;
- must be a central reference, not boundary-like.

### Anatomical continuity
Compare against:
- SG configuration-1 reference;
- SGF152-NAT;
- SGF208.

Check:
- head / face;
- shoulder breadth;
- ribcage depth;
- torso length;
- pelvis;
- arm / forearm share;
- hand proportions;
- leg share;
- foot proportions;
- silhouette.

The central candidate should be biologically coherent with the accepted config-2 envelope.

### Race identity
Compare against Marchfolk at similar stature where useful.

The goal is:
- plausible Sagekin population identity;
- intentional human overlap;
- no caricature;
- no accidental elfification.

---

# 7. Central-reference result

Return one:

## SG CONFIG-2 CENTRAL REFERENCE PASS — READY FOR PROPAGATION

Use if:
- ~178 cm reference is coherent;
- build is deterministic;
- anatomy is valid;
- fits the accepted config-2 envelope;
- no source integrity problem.

### OR

## SG CONFIG-2 CENTRAL REFERENCE NEEDS AUTHOR DECISION

Use if:
- multiple plausible central builds remain materially different;
- current canon does not identify which one should be the permanent anchor.

### OR

## FAIL

Use only for a blocking source/build problem.

If PASS, proceed immediately to Part B.

If NEEDS AUTHOR DECISION or FAIL, STOP before propagation.

---

# PART B — CONDITIONAL SAGEKIN MPFB FAMILY PROPAGATION

Proceed only if Part A returns PASS.

---

# 8. Active family base

Use only the frozen active MPFB Family Base v005.

Active topology:

- 57,842 vertices;
- 57,840 quads;
- face topology hash:  
  `ec768ae210ea3ee1c053d0c4cd3256d57dad6db35d515502706b74f64281bee0`
- hm08 map: active v005 map from `MPFB_FAMILY_BASE_v005_FREEZE.json`.

Use the AUTHOR-ACCEPTED Standard v1 unchanged.

No family-base topology edits are authorized.

---

# 9. Sagekin production candidates

Create family-propagated candidates for:

### Configuration 1
Source:
`SG`

Suggested production name:
`SG_M_REF_RP3_retopo_v001.blend`

### Configuration 2
Source:
new accepted/pass central reference from Part A (`SGF178` or equivalent).

Suggested production name:
`SG_F_REF_RP3_retopo_v001.blend`

Use project-consistent naming if needed.

Both candidates must:

- use exact active family topology;
- use exact active family map architecture;
- share identical face list / UV topology;
- retain Sagekin source anatomy;
- contain no per-race topology change.

---

# 10. Source regeneration identity

Regenerate both accepted/reference sources from their build records.

Required:

- exact geometry identity;
- source hash match;
- rebuild max |dV| = 0.

Stop on mismatch.

---

# 11. Topology identity / integrity

For both Sagekin candidates:

- 57,842 V / 57,840 Q;
- 100% quads;
- one component;
- zero boundary edges;
- zero non-manifold edges / vertices;
- zero degenerate faces;
- outward normals;
- face topology hash equals active family base;
- hm08 map arrays identical to active map;
- production geometry = M @ Sagekin hm08.

No local fitting or relaxation.

---

# 12. D1 + D3 + D4 + D5 validator

Run authoritative validator:

`validator_v2.py --scale-ref 173.143 --d5`

Required:

- **69 / 69 firm PASS** on config 1;
- **69 / 69 firm PASS** on config 2.

Also report:

- loop count;
- minimum;
- margin;
- fallback mode;
- D5 undefined sides;
- same-digit pole ownership.

Create Sagekin margin table and note any margin-0 stations.

Do not modify topology to satisfy an invalid probe.

---

# 13. Anatomy gates

Run full:

- T-1;
- T-2;
- T-3;
- T-7;
- stature;
- bbox;
- silhouette IoU;
- head;
- ears;
- hands;
- feet.

Also compare race-relevant proportional identity:

- slightly longer-limbed tendency;
- slightly shorter torso relative to stature;
- reduced ribcage depth tendency;
- human hands/feet;
- human auricle foundation.

No anatomy is required to be exaggerated.

---

# 14. Sagekin identity gate

Because Sagekin intentionally overlap Marchfolk, the identity gate is not “must look unmistakably different.”

Required decision:

> Does each family realization remain on its accepted Sagekin source without regressing toward generic Marchfolk or another race?

Compare:

- source vs production;
- Sagekin reference vs Marchfolk reference at similar scale;
- config-1 vs config-2 Sagekin central references.

Record source-fit metrics and visual review.

No culture/clothing/hair presentation should be used to prove biological identity.

---

# 15. Face / UFCA readiness

Confirm:

- mouth rings;
- orbit rings;
- mouth-corner poles;
- eye-region poles;
- open lip/orbit pockets;
- face density;
- human auricle compatibility.

No face topology changes.

---

# 16. Creator density

Run all 9 zones.

All must pass.

Report:
- mean edge / stature;
- p95;
- any unusually tight or loose region relative to Marchfolk/Skarn.

Do not decimate or locally densify in this order.

---

# 17. Contact

Compare against source and family baseline.

Required:

- no new rest self-intersection defect;
- no new hand/foot contact defect;
- no new groin / toe / web defect attributable to propagation.

Existing source contact may remain if documented.

---

# 18. Limited deformation sanity

Run Standard v1 suite:

- shoulder abd45 / abd90 / flex90;
- elbow90 / elbow130;
- wrist flex/ext;
- fist;
- thumb opposition;
- hip flex90;
- knee90 / 140;
- ankle dorsiflexion;
- toe flex / ext;
- trunk twist;
- neck flex / rotation.

Classify:

- topology;
- weights;
- joint placement;
- contact/setup.

Acceptance question:

> Does the frozen family topology behave at least as well as Sagekin native hm08 under the same source rig/weights, with no new topology-class failure?

Do not start corrective weighting.

If toe-extension behavior resembles the already accepted MPFB female carry-forward, record it but do not automatically fail unless a new/worse topology-class issue appears.

---

# 19. Visual evidence

Provide inspectable sheets for both Sagekin configurations:

1. source vs family full-body clay;
2. wire;
3. front / rear / profile / 3/4 overlay;
4. face closeup;
5. shoulder;
6. elbow;
7. hand;
8. pelvis;
9. knee;
10. foot;
11. validator / margin sheet;
12. density heat;
13. deformation comparison;
14. config-1 vs config-2 Sagekin central-reference comparison;
15. Sagekin vs Marchfolk neutralized comparison at similar stature.

Do not return the gate without photos.

---

# 20. Sagekin propagation decision

Return exactly one:

## SAGEKIN FAMILY PROPAGATION PASS — READY FOR AUTHOR FREEZE

Use if:
- config-2 central reference passes;
- both configs use active family topology unchanged;
- 69/69 firm PASS;
- anatomy gates pass;
- Sagekin identity preserved;
- density / face readiness pass;
- no new topology-class deformation failure.

### OR

## SAGEKIN NEEDS RACE-SPECIFIC BRANCH

Use only if a true Sagekin anatomical requirement cannot be preserved by the active family topology.

Do not build the branch without a new order.

### OR

## FAIL

Use only for a blocking source or propagation problem.

---

# 21. Required return

Commit:

1. `reviews/claude-rac-rp3-sagekin-config2-reference-and-propagation-gate.md`;
2. new config-2 central-reference source + sidecar/build record;
3. source identity evidence;
4. config-2 central-reference validation;
5. Sagekin production candidates + sidecars;
6. Sagekin family propagation manifest;
7. topology identity proof;
8. full 69-station validator outputs;
9. anatomy audits;
10. Sagekin identity comparison;
11. face readiness;
12. density;
13. contact;
14. deformation sanity;
15. visual sheets;
16. hashes;
17. narrow `specs/STATUS.md` update;
18. session handoff.

The gate must explicitly answer:

- Was a proper ~178 cm config-2 central reference created?
- Is it deterministic and rebuild-identical?
- Does it sit coherently inside the 152–208 cm accepted envelope?
- Did both Sagekin configs propagate onto the active family topology unchanged?
- Are both 69/69 under D1+D3+D4+D5?
- Do anatomy gates pass?
- Does Sagekin identity remain intact without exaggeration?
- Does face/UFCA readiness pass?
- Does density pass?
- Did any new topology-class deformation failure appear?
- Is a Sagekin-specific topology branch needed?
- Is Sagekin ready for freeze?

---

# 22. Stop rules

After committing the Sagekin gate:

**STOP FOR CHATGPT REVIEW.**

Do not proceed to:
- Fenn;
- Aelari;
- Vael;
- Halvren;
- Durrim;
- Pipkin;
- Cogling;
- production rig finalization;
- creator morph implementation;
- final UV/materials;
- LOD generation;
- UE5.

---

## FINAL AUTHOR RULING

- Sagekin is the next MPFB-family race.
- Configuration 1 uses accepted `SG`.
- Configuration 2 requires a new proper ~178 cm central reference.
- SGF152-NAT and SGF208 remain accepted bounds, not central anchors.
- Build/validate the central reference first.
- If it objectively passes, continue directly into family propagation in the same run.
- Do not freeze Sagekin without ChatGPT review.
