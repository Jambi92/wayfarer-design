# RAC RP3 — Sagekin SGF178 acceptance + D6 validator adoption + Sagekin freeze order

**Date:** 2026-10-27  
**Authority:** Tyler / ChatGPT review of Claude return `8ed659dc47fc41f43c0a70f82e50058a8cc933c4`.  
**Parent gate:** `reviews/claude-rac-rp3-sagekin-config2-reference-and-propagation-gate.md`.  
**Program references:**  
- `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md`;  
- `specs/RAC_PRODUCTION_MESH_CONTRACT.md`;  
- `specs/sagekin/SAGEKIN_V1.md`;  
- active MPFB Family Base v005 freeze record.

This order formally accepts the Sagekin configuration-2 central reference, adopts D6 as an authoritative family validator rule, revalidates Sagekin under the expanded validator, freezes Sagekin if all read-back checks pass, and updates the family propagation standard.

Do not begin Fenn in this order.

---

# 1. SGF178 — AUTHOR ACCEPTED CONFIGURATION-2 CENTRAL REFERENCE

Promote:

`SGF178`

from:

> configuration-2 construction base for SGF152-NAT / SGF208

to:

> **SAGEKIN CONFIGURATION-2 CENTRAL REFERENCE — AUTHOR ACCEPTED**

Accepted source:

- R-6: `reviews/reference-assets/r6/SGF178_r6.npz`
- SHA-256:  
  `52ff5e04331561a4b6f19cb88d8987b6b8e240199e7eec76246cc86202f059e1`
- build: `reviews/reference-assets/builds/SGF178_build.json`
- build SHA-256:  
  `7f50254337ab0d26a2eada3d9e860edcb7c2f113893b67dff0cb0dd038019620`
- geometry hash:  
  `7755a8f00de921dd8651a899c96e1050ff65b481a0ebf08025b0c82875359a25`
- stature: ~178.0013 cm

Accepted basis:

- deterministic rebuild, max |dV| = 0;
- full height re-solve reproduces the same build;
- canonical ~178 cm Sagekin reference stature;
- coherent with accepted SGF152-NAT / SGF208 configuration-2 bounds;
- same accepted Sagekin proportional targets as configuration-1 SG;
- human anatomy preserved;
- no elf-like exaggeration;
- matched-stature comparison preserves subtle Sagekin-vs-Marchfolk population tendencies.

Update the relevant source inventory / manifest role without modifying the source geometry.

Keep:

- `SGF152-NAT` = accepted c2 minimum bound;
- `SGF208` = accepted c2 maximum bound;
- `SGF178` = accepted c2 central reference.

---

# 2. D6 — AUTHOR ACCEPTED VALIDATOR RULE

Accept the proposed **D6 foreign-segment probe rule**.

## Rule

For **non-digit stations**, a band side is undefined when either selected endpoint's dominant native/source skin bone does not belong to the anatomical segment/joint being audited.

Examples:

- hip station:
  - valid ownership includes pelvis / spine_01 / thigh;
  - forearm / hand endpoints are foreign and must not count.
- elbow station:
  - valid ownership includes upperarm / lowerarm;
  - trunk/spine endpoints are foreign and must not count.

Use the native hm08 source weights carried through the family map to determine endpoint ownership.

Excluded D6 sides are handled like D1 undefined sides.

Report:

`+D6_FOREIGN_SEGMENT_UNDEFINED`

or equivalent.

---

# 3. Why D6 is accepted

The current Sagekin SG hip failure is not a topology failure.

The diagnostic proves:

- the failing hip side samples the hanging forearm;
- the selected path is entirely in the arm zone;
- dominant skin ownership is lowerarm;
- the actual hip sides carry sufficient support.

The same foreign-segment artifact exists across all six tested family realizations:

- MF-M;
- MF-F;
- SK-C1R;
- SK-F;
- SG;
- SGF178.

The prior races passed only because the sampled foreign segment happened to contain enough loops.

D6 therefore corrects measurement ownership rather than weakening the topology standard.

---

# 4. Authoritative validator hierarchy

The MPFB-family authoritative validator is now:

1. ordinary band method;
2. **D1** — undefined side handling;
3. **D3** — same-digit pole ownership;
4. **D4** — stature-normalized station geometry;
5. **D5** — interdigital endpoint validity;
6. **D6** — non-digit foreign-segment ownership validity.

Authoritative form:

**D1 + D3 + D4 + D5 + D6**

Legacy / prior validator outputs remain historical evidence only.

Do not alter geometry to satisfy a side that D6 proves belongs to another anatomical segment.

---

# 5. D6 regression / blast-radius verification

Before freezing Sagekin, rerun D6 on all currently validated family realizations:

- MF-M;
- MF-F;
- SK-C1R;
- SK-F;
- SG;
- SGF178.

Required:

- no existing PASS becomes FAIL;
- no station verdict is lowered;
- no valid same-segment side is incorrectly excluded;
- Marchfolk remains 69 / 69;
- Skarn remains 69 / 69;
- SG becomes 69 / 69;
- SGF178 remains 69 / 69.

Also explicitly audit any D6 exclusions at:

- hip;
- elbow;
- shoulder;
- knee;
- ankle;
- wrist;
- neck.

Do not assume D6 is safe solely from hip/elbow examples.

If another joint exposes a false-positive ownership exclusion, STOP and return the rule for refinement before freeze.

---

# 6. Sagekin production candidates accepted for freeze if D6 passes

### Configuration 1

`SG_M_REF_RP3_retopo_v001.blend`

Current candidate:
- SHA-256 prefix `bb156e9c…`
- geometry hash prefix `56a73d8f…`

### Configuration 2

`SG_F_REF_RP3_retopo_v001.blend`

Current candidate:
- SHA-256 prefix `0ef62ffc…`
- geometry hash prefix `9dcc5000…`

Both must remain:

- 57,842 V / 57,840 Q;
- 100% quads;
- one component;
- active family face topology hash `ec768ae2…`;
- identical active family map;
- V = M @ Sagekin hm08 exactly;
- no per-race topology change.

Do not resave unless necessary. Prefer freeze-by-record.

---

# 7. Sagekin final gate requirements

Re-run / confirm on both configurations:

## Validator
- 69 / 69 under D1+D3+D4+D5+D6.

## Anatomy
- T-1 PASS;
- T-2 PASS;
- T-3 PASS;
- T-7 PASS;
- silhouette preserved;
- race-relevant proportions preserved.

## Identity
- no regression toward Marchfolk;
- no exaggeration;
- no elfification;
- SG and SGF178 remain valid central Sagekin references.

## Face / UFCA
- mouth/orbit readiness pass;
- no mouth-corner pole regression;
- human auricle compatibility.

## Density
- 9 / 9 zones PASS.

## Contact
- 0 new propagation-induced rest contact defects.

## Deformation
- no new topology-class failure;
- accepted family toe-extension rig-class behavior may carry forward.

---

# 8. Sagekin freeze

If all §7 checks pass:

Freeze by record:

- `SG_M_REF_RP3_retopo_v001.blend`
- `SG_F_REF_RP3_retopo_v001.blend`

Create:

`reviews/claude-rac-rp3-sagekin-family-freeze-report.md`

and a Sagekin freeze record / manifest.

Status:

> **SAGEKIN RP3 — AUTHOR ACCEPTED / FROZEN — MPFB FAMILY PROPAGATION PASS**

The freeze record must carry:

- exact file hashes;
- geometry hashes;
- family face hash;
- source hashes;
- SGF178 accepted-reference status;
- validator version/rules;
- anatomy/density/face results;
- carry-forward items;
- exact PC read-back results.

Do not change the production mesh merely to embed status.

---

# 9. Carry-forward register

If Sagekin deformation reproduces the accepted family toe-extension behavior without a new topology-class issue, record only what materially belongs to later rigging/weighting.

Do not duplicate already-known family-wide entries unnecessarily.

If SG or SGF178 has a distinct additional rig/joint issue, assign a new carry-forward ID with evidence.

No topology reopen.

---

# 10. Update MPFB Family Propagation Standard v1

Update:

`specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md`

to include D6 as an accepted authoritative validator rule.

The standard should now state:

**Authoritative validator = D1 + D3 + D4 + D5 + D6**

Document:

- D6 purpose;
- dominant-bone ownership method;
- station-owning-bone table;
- fallback behavior;
- regression requirement;
- prohibition on modifying topology to satisfy foreign-segment probes.

Retain the principle:

> Standardize the technical process, not race anatomy or identity.

---

# 11. Update Sagekin source/reference records

Update the appropriate source/reference manifest(s) so that:

- SG = accepted c1 central reference;
- SGF178 = accepted c2 central reference;
- SGF152-NAT = accepted c2 min bound;
- SGF208 = accepted c2 max bound.

Do not alter any source hashes.

Update `specs/STATUS.md` narrowly.

---

# 12. Next-race recommendation — Fenn

After Sagekin freeze succeeds:

recommend **Fenn** as the next RP3 race.

But do not begin it in this order.

The handoff/recommendation should flag that Fenn is the first likely true race-specific topology branch because of:

- pointed/non-human ear anatomy;
- elven skeletal/proportional identity;
- explicit rule that Fenn must not simply inherit a generic human/MetaHuman shape;
- family propagation may remain valid for most of the body while ears and possibly other identity-bearing zones require a sanctioned branch.

The next order will decide the exact Fenn strategy after reviewing Sagekin freeze.

---

# 13. Required return

Commit:

1. `reviews/claude-rac-rp3-sagekin-family-freeze-report.md`;
2. SGF178 author-acceptance/reference update;
3. Sagekin freeze record;
4. D6 final implementation;
5. six-realization D6 regression evidence;
6. final Sagekin validator outputs;
7. final read-back verification;
8. updated `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md`;
9. updated reference/source manifest(s);
10. carry-forward register update if needed;
11. narrow `specs/STATUS.md` update;
12. session handoff.

The return must explicitly answer:

- Is SGF178 now formally accepted as Sagekin c2 central reference?
- Is D6 implemented as authoritative?
- Did D6 regress any existing family realization?
- Are Marchfolk still 69/69?
- Are Skarn still 69/69?
- Is SG 69/69?
- Is SGF178 69/69?
- Did all Sagekin anatomy/identity/face/density/contact gates pass?
- Did any new topology-class deformation failure appear?
- Were both Sagekin production bodies frozen successfully?
- Any read-back/hash mismatch?
- Is Fenn still the recommended next race?

---

# 14. Stop rules

After committing the Sagekin freeze package:

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
- UE5 integration.

---

## FINAL AUTHOR RULING

- `SGF178` is **AUTHOR ACCEPTED** as Sagekin configuration-2 central reference.
- D6 foreign-segment ownership is **AUTHOR ACCEPTED**.
- The authoritative family validator becomes **D1 + D3 + D4 + D5 + D6**.
- No Sagekin-specific topology branch is authorized or required.
- Revalidate and freeze Sagekin if all gates remain green.
- Update Standard v1.
- Stop before Fenn.
