# RAC RP3 — MPFB Family Base v005 final acceptance/freeze + Skarn freeze + Standard v1 promotion order

**Date:** 2026-10-27  
**Authority:** Tyler / ChatGPT review of Claude return `a4ad723ae56736cfac5814c3d26e66d7dab574e0`.  
**Parent gate:** `reviews/claude-rac-rp3-mpfb-family-base-final-toe2-web-gate.md`.  
**Program references:**  
- `specs/RAC_PRODUCTION_MESH_CONTRACT.md`;  
- `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md`;  
- frozen Marchfolk v003 family base and v004/v005 successor evidence.

This order formally accepts the v005 successor as the **active MPFB family production base**, freezes Marchfolk and Skarn on that topology, records the toe-extension exception as a production-rig carry-forward item, and promotes the technical family propagation standard to author-accepted status.

No further Marchfolk/Skarn family-base topology work is authorized in RP3.

---

# 1. Immutable historical provenance

Preserve unchanged:

- frozen Marchfolk v003 family base and freeze record;
- all v004 margin-hardening candidates/evidence;
- all v005 candidate/evidence files;
- accepted Marchfolk sources;
- accepted Skarn sources;
- all mapping/provenance files.

Do not overwrite or delete v003/v004 history.

Record:

- **v003 = historical accepted MPFB Family Base v1**
- **v004 = margin-hardening provenance**
- **v005 = active MPFB Family Base v2 / final margin-hardened base**

---

# 2. Final validator standards — ACCEPTED

The authoritative MPFB-family validator rules are:

- **D1** — undefined band-side fallback;
- **D3** — same-digit pole ownership;
- **D4** — stature-normalized station geometry;
- **D5** — interdigital endpoint-validity rule.

D4 and D5 are now formally accepted and no longer provisional.

The standard validator must use:

`D1 + D3 + D4 + D5`

for future MPFB-family race propagation.

Do not use legacy fixed-cm station verdicts as authoritative on differently sized races.

---

# 3. Toe-extension exception — ACCEPTED

Accept the documented v005 toe-extension exception:

### Marchfolk configuration 2
- 3 topology-attributable flipped faces at toe extension 30°.

### Skarn configuration 2
- 2 topology-attributable flipped faces at toe extension 30°.

Conditions:

- toe flexion = 0 topology-attributable flips;
- male configurations = 0;
- exception is localized to the known MTP/toe-extension crease;
- no new rest contact/self-intersection defects;
- no anatomy regression;
- local topology quality is otherwise substantially improved;
- the rejected TW3 alternative reduces flip count only marginally while worsening T-4.

Classify these flips as:

**PRODUCTION-RIG / TOE-WEIGHTING CARRY-FORWARD ITEM**

They are not a reason to reopen the family topology.

Do not create another toe topology cycle.

---

# 4. Active family-base artifacts — ACCEPTED

Accept the v005 successor topology:

- **57,842 vertices**
- **57,840 quads**
- common shared topology across Marchfolk M/F and Skarn M/F;
- authoritative face topology / mapping from `MPFB_FAMILY_BASE_v005.json`;
- hm08 → v005 map SHA prefix `e690fbaf…`;
- v003 → v005 map SHA prefix `928bec17…`;
- v004 → v005 map SHA prefix `cdb401a1…`.

Use the exact full hashes from the committed manifest in the freeze record.

The family topology includes:

- v004 posterior-heel barycentric correction;
- v004 hip support hardening;
- v004 toe-3 root support / crease-pole correction;
- v005 toe-2 dorsal racetrack architecture;
- D1/D3/D4/D5 validator semantics;
- current production frame/origin;
- current source weight / UV / morph transfer paths.

---

# 5. Marchfolk v005 formal freeze

Freeze by record:

- `MF_M_REF_RP3_retopo_v005.blend`
- `MF_F_REF_RP3_retopo_v005.blend`

Do not re-save merely to change embedded status if that changes file hashes.

Create:

`reviews/claude-rac-rp3-marchfolk-v005-active-family-base-freeze-report.md`

and an authoritative freeze record/manifest.

Read back both files and verify:

- exact file SHA-256;
- exact geometry hash;
- exact face topology hash;
- 57,842 V / 57,840 Q;
- 100% quads;
- one component;
- 0 boundary;
- 0 non-manifold;
- 0 degenerates;
- outward normals;
- exact map compatibility;
- 69/69 firm PASS under D1+D3+D4+D5;
- T-1/T-2/T-3/T-7 pass;
- all density zones pass;
- face/UFCA readiness unchanged;
- source hashes unchanged.

Update `specs/STATUS.md` to:

**MARCHFOLK RP3 v005 — AUTHOR ACCEPTED / FROZEN — ACTIVE MPFB FAMILY BASE**

---

# 6. Skarn formal freeze

Freeze the Skarn production realizations using the exact same active family topology:

- `SK_M_REF_RP3_retopo_v003.blend`
- `SK_F_REF_RP3_retopo_v003.blend`

Create:

`reviews/claude-rac-rp3-skarn-family-freeze-report.md`

Read back and verify:

- exact file/geometry hashes;
- same active family topology hash;
- C1R face identity preserved;
- T-1/T-2/T-3/T-7 pass;
- 69/69 firm PASS under D1+D3+D4+D5;
- density pass;
- face readiness pass;
- no new topology-class deformation failure beyond the accepted toe-extension carry-forward item;
- source hashes unchanged.

Update status:

**SKARN RP3 — AUTHOR ACCEPTED / FROZEN — MPFB FAMILY PROPAGATION PASS**

Do not alter Skarn anatomy or topology during freeze.

---

# 7. Promote MPFB Family Propagation Standard v1

Update:

`specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md`

Status:

**AUTHOR-ACCEPTED TECHNICAL STANDARD v1**

The standard must include:

1. source regeneration identity check;
2. hm08 → active family-base mapping;
3. helper removal;
4. production frame/origin;
5. topology identity verification;
6. D1/D3/D4/D5 validator rules;
7. creator-density audit;
8. anatomy T-1/T-2/T-3/T-7;
9. face/UFCA readiness audit;
10. limited deformation sanity;
11. race-specific identity gate;
12. visual evidence package;
13. manifest/freeze template;
14. carry-forward issue recording;
15. stop rules.

Explicitly state:

> The technical propagation process is standardized. Race anatomy, identity, cultural appearance, and race-specific branches remain explicit author-review gates and are never auto-approved merely because the technical pipeline passes.

---

# 8. Freeze the family-base manifest

Create an authoritative active family-base freeze manifest:

`MPFB_FAMILY_BASE_v005_FREEZE.json`

It must record:

- all active base hashes;
- map hashes;
- topology counts;
- validator version / rules;
- standard version;
- accepted exceptions;
- provenance chain:
  - hm08 → v002 → v003 → v004 → v005;
- frozen Marchfolk realization hashes;
- frozen Skarn realization hashes;
- current active status.

The freeze manifest is authoritative over older candidate sidecar status strings.

---

# 9. Standardized carry-forward register

Create or update a concise family production-rig carry-forward register.

At minimum record:

### Marchfolk F
- toe extension 30°: 3 topology-attributable faces in the MTP crease.

### Skarn F
- toe extension 30°: 2 topology-attributable faces in the MTP crease.

Class:
- rig/weighting / toe-articulation stage.

Do not classify as topology-blocking.

Preserve prior Grask carry-forward items separately.

---

# 10. Next-race recommendation

After all freezes and standard promotion verify successfully:

**STOP FOR CHATGPT REVIEW before starting the next race.**

Do not automatically start Sagekin or another race in this order.

In the freeze report, recommend the next MPFB-family race based on the accepted master-plan sequence and current family risks.

Preferred sequence remains:

1. Sagekin;
2. Fenn;
3. Aelari;
4. Vael;
5. Halvren;
6. Durrim;
7. Pipkin;
8. Cogling;

unless the source inventory / accepted canon indicates a safer ordering.

Do not begin propagation until ChatGPT sends the next explicit order.

---

# 11. Required return

Commit:

1. `reviews/claude-rac-rp3-marchfolk-v005-active-family-base-freeze-report.md`;
2. `reviews/claude-rac-rp3-skarn-family-freeze-report.md`;
3. `MPFB_FAMILY_BASE_v005_FREEZE.json`;
4. updated `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md`;
5. carry-forward register;
6. read-back verification evidence;
7. source/frozen hash checks;
8. narrow `specs/STATUS.md` update;
9. session handoff.

The return must explicitly state:

- Marchfolk v005 frozen successfully?
- Skarn frozen successfully?
- active family topology/hash?
- D1/D3/D4/D5 authoritative?
- accepted toe-extension exception recorded?
- standard promoted?
- next recommended race?
- any freeze/read-back mismatch?
- any new blocker?

---

# 12. Stop rules

After committing the freeze package:

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
- production rig finalization;
- creator morph implementation;
- final UV/materials;
- LOD generation;
- UE5 integration.

---

## FINAL AUTHOR RULING

- v005 is **AUTHOR ACCEPTED** as the active MPFB family base.
- The 3/2 female toe-extension flips are accepted as production-rig carry-forward items.
- Marchfolk v005 is to be frozen.
- Skarn on the same family topology is to be frozen.
- D4 and D5 are permanently accepted validator standards.
- MPFB Family Propagation Standard v1 is to be promoted to AUTHOR-ACCEPTED.
- No more family-base topology work is authorized in RP3.
