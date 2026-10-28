# RAC RP3 — Aelari final consolidation / validation / freeze order

**Date:** 2026-10-28  
**Authority:** Tyler / ChatGPT review of Claude correction return `7d2f73485234837356b3c2c815304444d7800e03`.  
**Parent gates:**  
- `reviews/claude-rac-rp3-aelari-body-face-ear-gate.md` (`a4f81979…`);  
- `reviews/claude-rac-rp3-aelari-body-source-correction-gate.md` (`7d2f734…`).  
**Program references:**  
- `specs/aelari/AELARI_V1.md`;  
- `reviews/elf-comparative-review.md`;  
- `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md`;  
- `specs/RAC_PRODUCTION_MESH_CONTRACT.md`;  
- active frozen MPFB Family Base v005;  
- frozen Fenn RP3, used only as comparative/engineering precedent.

This order formally accepts the corrected Aelari R1 body sources, the selected AE-E2 ear geometry, and the reuse of Fenn ear-topology v002 as **engineering topology only**, and authorizes **final Aelari consolidation, full validation, PC read-back, and freeze-by-record**.

If every final gate remains green, Aelari RP3 should be closed.

Do not start Vael in this order.

---

# 1. FINAL AUTHOR DECISIONS — ACCEPTED

## 1.1 Corrected Aelari central body sources

Accept:

### Configuration 1
`AEL1-R1`

- R-6: `reviews/reference-assets/r6/AEL1-R1_r6.npz`
- full SHA-256:  
  `17ae6d138809d3b3936c0631a6bbe30f2a891c16782052c3bc0ccc156f0c0faf`
- build SHA-256:  
  `73ec892fc04a840fe704d6fde5925c741bd3aa72cc4051bfcdfc3e62531dfcff`
- stature: ~189.985 cm.

### Configuration 2
`AELF190-R1`

- R-6: `reviews/reference-assets/r6/AELF190-R1_r6.npz`
- full SHA-256:  
  `93a951d585a7c9d8fcba7a7a77795686eea1ac57326ad3107f1b7a6636a59239`
- build SHA-256:  
  `73fab1c8777c1b45e0c8652cd1626f5bb30311094a94da8c81e4b25471917238`
- stature: ~189.995 cm.

Retain original `AEL1` and `AELF190` as immutable ancestry/provenance.

---

## 1.2 Accepted R1 body correction

The shared Aelari source correction is accepted:

| Control | Original | Accepted R1 |
|---|---:|---:|
| `spine_03` Y | 0.9704 | **0.99** |
| `LR:thigh` Y | 0.9875 | **1.01** |
| `LR:calf` Y | 1.0523 | **1.03** |

Height macro was re-solved to preserve ~190 cm.

This correction is now canonical for the central Aelari reference pair.

Accepted effects:
- thoracic vertical > frozen Fenn:
  - c1 +1.00 %;
  - c2 +1.32 %;
- thigh/lower-leg distribution more even than Fenn on both;
- total leg share remains essentially unchanged within the bounded correction;
- torso share increase is accepted as the coupled thoracic response;
- hidden-ear body identity strengthened;
- hidden-ear face unchanged.

Do not reopen the body correction unless the final consolidation itself introduces a regression.

---

## 1.3 Pelvis

Accept the post-R1 pelvis result:

- all six Aelari pelvis rules pass at t = 0 / 0.5 / 1.0;
- pelvis bone scales themselves were not altered;
- narrower margins remain valid;
- no configuration-specific pelvic anatomy.

The following are accepted final central-reference margins, not blockers:
- leg share > Marchfolk by ~+0.34 / +0.35 %;
- waist interval / torso > Fenn by ~+1.33 % c1 / +0.62 % c2.

Do not enlarge these merely to create bigger visual separation.

---

## 1.4 Craniofacial identity

Accept the existing Aelari craniofacial source architecture unchanged.

Final hidden-ear face requirement:
- 7 / 7 Aelari systems remain directional/material;
- Aelari remains distinct from frozen Fenn;
- no craniofacial source branch is required.

Do not alter the face in consolidation.

---

## 1.5 Aelari ear

Accept:

**AE-E2 = canonical central Aelari ear direction.**

AE-E2 parameters remain the accepted evidence-based central design:

- nominal source length ~9.4 cm;
- max half-width ~1.70 cm;
- projection ~24° input / reviewed realized body angle ~27°;
- tilt ~30° input;
- sweep ~1.7 cm;
- clean gradual taper;
- closer-set to skull than Fenn;
- more upward trajectory than Fenn;
- full non-human helix / antihelix / concha / tragus / lobe anatomy.

Do not reopen AE-E1/E2/E3 selection.

---

## 1.6 Ear topology reuse

Accept:

> frozen Fenn ear topology v002 may be reused for Aelari as **engineering topology only**.

This acceptance means:
- same connectivity / face list;
- same 52-vertex root-interface architecture;
- same cuff method;
- same tapered-leaf upper-extension engineering;
- same deformation-aware guard concept.

It does **not** mean:
- same ear geometry;
- same race anatomy;
- universal elf ear topology.

Every Aelari ear vertex geometry remains Aelari-specific.

---

# 2. FINAL PRODUCTION COMPOSITION

Produce final Aelari production bodies:

## Configuration 1
`AE_M_REF_RP3_v001.blend`

Composition:
- AEL1-R1 body source;
- frozen MPFB Family Base v005 outside the ear branch;
- accepted Aelari face from AEL1-R1;
- selected AE-E2 Aelari ear geometry;
- accepted reused Fenn-v002 engineering ear topology.

## Configuration 2
`AE_F_REF_RP3_v001.blend`

Composition:
- AELF190-R1 body source;
- same family base outside branch;
- accepted Aelari face from AELF190-R1;
- selected AE-E2 geometry;
- same ear topology.

No configuration-specific topology.

---

# 3. EXPECTED FINAL TOPOLOGY

Because AE-E2 uses the accepted Fenn-v002 engineering connectivity, expected whole-body topology is:

- **58,944 vertices**
- **58,942 quads**
- 100 % quads

unless the committed Aelari prototype record proves an exact equivalent count under the same topology.

Required:
- c1/c2 identical face list;
- branch connectivity identical to frozen Fenn v002;
- Aelari geometry distinct from Fenn;
- active MPFB topology unchanged outside branch;
- 52-root-vertex interface per side retained;
- root valence 4.

Record the final face-topology hash.

---

# 4. CLEAN REBUILD / PROVENANCE

Rebuild from committed immutable inputs only.

Required chain:

1. regenerate AEL1-R1 / AELF190-R1 from committed build records;
2. prove max |dV| = 0;
3. export native hm08;
4. propagate onto frozen MPFB v005;
5. prove the resulting family realization equals the reviewed v002 corrected body-family candidate;
6. construct AE-E2 from the committed Aelari parameters on the accepted ear topology;
7. prove ear geometry equals the reviewed corrected AE-E2 prototype within numerical roundoff;
8. write production-frame blends.

Stop on any source/hash mismatch.

---

# 5. FINAL SIDECARS / MAPS

Create per-body final records, project-consistent with Fenn:

- `AE_M_REF_RP3_v001.json`
- `AE_F_REF_RP3_v001.json`
- `AE_M_REF_RP3_v001_landmarks.json`
- `AE_F_REF_RP3_v001_landmarks.json`
- `AE_M_REF_RP3_v001_branch_map.npz`
- `AE_F_REF_RP3_v001_branch_map.npz`

The branch-map sidecar must capture:
- v005 → final index mapping;
- removed v005 ear rows/faces;
- branch part / side;
- hm08 proxy / weights needed for deformation validation;
- root interface;
- provenance to the reused engineering topology.

---

# 6. FULL INTEGRITY GATE

For both final bodies require:

- 100 % quads;
- 1 connected component;
- 0 boundary edges;
- 0 non-manifold edges;
- 0 non-manifold vertices;
- 0 degenerate faces;
- winding consistent;
- outward normals;
- no new coincident defects;
- 0 branch self-intersections;
- no branch-attributable whole-body rest contact;
- no root seam;
- no root float;
- no root burial.

Whole-body self-intersection/contact may equal only the already accepted body-family baseline.

---

# 7. AUTHORITATIVE JOINT VALIDATOR

Run final:

**D1 + D3 + D4 + D5 + D6**

on both final production bodies.

Required:
- **69 / 69 firm PASS** c1;
- **69 / 69 firm PASS** c2.

Report:
- fallback statuses;
- D5 exclusions;
- D6 exclusions;
- margin-zero stations;
- differences vs corrected body-family candidate.

The ear branch must not alter any body-joint verdict.

Vertex-order-only fallback-label differences may be documented exactly as in Fenn, but loops/margins/valid sides must remain equivalent.

---

# 8. FINAL BODY ANATOMY / SOURCE FIT

Because the R-6 sources still carry the non-final MPFB human auricle while production carries the accepted Aelari ear branch:

### Primary body/source anatomy gate
Run T-1 / T-2 / T-3 / T-7 with the external-ear branch excluded from source-fit judgment.

Required:
- body PASS;
- head excluding external ear PASS;
- hands PASS;
- feet PASS;
- stature/bbox PASS;
- silhouette excluding ear pixels PASS.

### Unmasked run
Also record the ordinary unmasked anatomy run for transparency.

It may fail T-1/T-2/T-7 solely because the human source auricle differs from the accepted AE-E2 ear.

If so:
- explicitly classify it as **expected source-vs-new-ear anatomy divergence**;
- do not treat it as a body failure.

No other unmasked failure is acceptable.

---

# 9. FINAL AELARI BODY IDENTITY

Re-run equal-height hidden-ear body comparison against:

- frozen Fenn;
- Marchfolk;
- Sagekin.

Required:

### Aelari vs Fenn
- central vertical share > Fenn;
- torso share > Fenn;
- neck contribution > Fenn;
- thoracic vertical > Fenn;
- waist interval / torso > Fenn;
- cranial vertical contribution > Fenn;
- extremity share < Fenn;
- leg segment distribution more even than Fenn.

### Aelari vs humans
- long-leg identity remains;
- long-arm identity remains;
- hands/feet remain elven;
- joint gracility remains;
- shallow thoracic depth remains;
- Aelari is not merely a tall human.

Do not require exaggerated perfect classification.

---

# 10. PELVIS FINAL GATE

Re-run the skeletal-proxy Aelari pelvis suite at:

- t = 0;
- 0.5 cm;
- 1.0 cm.

Required on c1/c2:

- hip-joint height / stature > MF;
- bitrochanteric / crest not lower than MF;
- pelvic vertical / crest > MF;
- pelvic vertical / crest > frozen Fenn;
- waist interval / torso > Fenn;
- waist interval / torso >= MF;
- no breadth shortcut.

The accepted narrower R1 margins may remain.

---

# 11. HIDDEN-EAR FACE FINAL GATE

Re-run the accepted hidden-ear Aelari face test against:

- frozen Fenn;
- Marchfolk;
- Sagekin.

Required:
- 7 / 7 systems material/directional on both configurations;
- facial verticality;
- cranial-height contribution;
- longer forehead-to-chin relationship;
- lower-face relationship;
- lighter mandible tendency;
- vertical cheek/mid-face orientation;
- lighter-brow relationship;
- longer/narrower eye presentation relative to Fenn.

No face geometry may change in final consolidation beyond numerical export noise.

---

# 12. UFCA / FACE READINESS

Reconfirm:

- mouth rings;
- orbit rings;
- mouth-corner pole count;
- poles near eyes;
- open lip/orbit pockets;
- face density;
- no topology change outside ear branch.

No Aelari craniofacial topology branch.

---

# 13. EAR FINAL GATE — AE-E2

Rebuild AE-E2 with the exact accepted parameters.

For both final bodies require:

- same topology as accepted reused engineering topology;
- same Aelari geometry logic;
- root valence 4;
- clean root transition;
- no self-intersection;
- no seam / float / burial;
- no aspect > 10;
- T-4 at or below the reviewed Aelari AE-E2 quality class.

Reviewed corrected prototype expectations:
- c1 T-4 = 117 / 3,718;
- c2 T-4 = 120 / 3,718;
- aspect max ~8.28 / 8.55;
- branch self-intersections = 0.

Do not worsen these materially.

---

# 14. AELARI-vs-FENN VISIBLE-EAR FIREWALL

Final matched-presentation comparison against frozen Fenn E2.

Required Aelari direction:
- less lateral projection;
- closer to skull;
- more upward trajectory;
- longer/narrower gradual taper;
- distinct root-to-tip trajectory;
- no “Fenn ear rotated upward” read.

Shared ancestry may remain visible in engineering structure/internal cartilage family resemblance.

Do not change frozen Fenn.

---

# 15. DENSITY

Run all 9 family density zones plus ear branch.

Required:
- all family zones PASS;
- ear branch mean edge / stature <= 0.25 %;
- no accidental density change during final production export.

---

# 16. BODY DEFORMATION FINAL GATE

Run Standard v1 18-pose deformation suite on:

- native corrected source;
- corrected family realization;
- final Aelari production body;
- Marchfolk reference where appropriate.

Required:
- final production body adds no new topology-class defect over the corrected family realization;
- no new contact class;
- no unexplained flip/fold increase.

Classify all remaining behavior:
- topology;
- weights;
- joint placement;
- contact/setup;
- known family rig class.

Do not author production corrective weights in RP3.

---

# 17. EAR / HEAD DEFORMATION READINESS

Run accepted Aelari ear readiness:

- neck flex/ext;
- head yaw ±45;
- head pitch ±20;
- head roll ±20.

Required:
- 0 new branch self-intersections;
- 0 flipped branch faces;
- 0 root inversions;
- root strain acceptable;
- head/neck clearance preserved.

No production ear movement/rig is authored.

---

# 18. EAR SHAPE-PROBE RETENTION

Re-run AE-E2 topology-readiness probes:

- projection ±10°;
- tilt ±8°;
- sweep ±0.6;
- length ±10 %;
- tip blunt/sharp.

Required:
- same topology;
- no branch self-intersection;
- no broken root;
- aspect <= 10;
- no catastrophic T-4 spike;
- intended measure moves in intended direction.

These remain diagnostics, not creator morphs.

---

# 19. SKIN-GRACILITY DIAGNOSTIC NOTE

The remaining skin-surface gracility rows for wrist/knee/ankle are accepted as **diagnostic only**, as already established in the parent gates, because those skin breadth readings are unstable across the stature macro.

Do not modify source anatomy to chase those skin measurements.

Final biological gracility is judged by the accepted whole-system skeletal/body relationships and the authoritative validator, not those unstable skin-width diagnostics.

---

# 20. FINAL VISUAL FREEZE PACKAGE

Provide actual final sheets:

1. c1 full body;
2. c2 full body;
3. c1 head front/profile/3-4;
4. c2 head front/profile/3-4;
5. corrected Aelari vs frozen Fenn equal-height hidden-ear body;
6. thorax / torso comparison;
7. leg-segment comparison;
8. pelvis validation;
9. hidden-ear face comparison;
10. final AE-E2 ear front/profile/rear/top;
11. final ear wire/poles;
12. final T-4/aspect;
13. root integration;
14. Aelari AE-E2 vs frozen Fenn E2;
15. c1 vs c2 AE-E2;
16. validator/margin table;
17. density summary;
18. body deformation summary;
19. ear readiness/probes;
20. source→production overlay.

No freeze without the visual package.

---

# 21. FINAL PRODUCTION FRAME / READ-BACK

Write final blends in the standard production frame:

- meters;
- Z up;
- faces −Y;
- subject left +X;
- origin at pelvis root projected to ground.

After writing:

- copy to the production Aelari RP3 directory;
- read back without saving;
- confirm file SHA;
- confirm geometry hash;
- confirm face hash;
- confirm faces equal candidate;
- confirm max geometry deviation only Blender roundoff;
- confirm sidecar/branch-map hashes;
- recompute validator from read-back.

PC copies must be byte-identical to the freeze records.

---

# 22. FREEZE BY RECORD

If all gates pass, create:

`AELARI_RP3_FREEZE.json`

and:

`reviews/claude-rac-rp3-aelari-final-freeze-report.md`

Freeze by record; do **not** resave production blends merely to change status.

Freeze record must contain:

- final filenames;
- full file SHA-256;
- geometry hashes;
- face topology hash;
- ear-topology hash;
- branch-map hashes;
- corrected source hashes;
- original ancestry hashes;
- active v005 hashes;
- frozen Fenn comparison reference hashes where used;
- validator results;
- anatomy/identity results;
- pelvis results;
- hidden-ear body/face results;
- density;
- ear T-4/aspect;
- deformation;
- shape-probe result;
- read-back results;
- accepted diagnostic notes.

The freeze record is authoritative over embedded candidate status strings.

---

# 23. REFERENCE / SPEC / STATUS UPDATE

On successful freeze update:

- `reviews/reference-assets/manifest.json`;
- `specs/aelari/AELARI_V1.md`;
- `specs/STATUS.md`;
- session handoff.

Final source lineage must be explicit:

### c1
AEL1 ancestry → AEL1-R1 accepted central body → final Aelari production body.

### c2
AELF190 route → AELF190-R1 accepted central body → final Aelari production body.

Ear:
AE-E2 geometry + reused Fenn-v002 engineering topology = accepted **Aelari-specific external-ear branch**.

Do not describe the topology as universal elf topology.

---

# 24. FINAL RESULT

Return exactly one:

## AELARI RP3 FINAL PASS — AUTHOR ACCEPTED / FROZEN

Use only if every gate and read-back passes.

### OR

## AELARI FINAL CONSOLIDATION NEEDS AUTHOR DECISION

Use only for a new, non-blocking residual not already accepted.

### OR

## FAIL

Use for a genuine blocker.

---

# 25. NEXT RACE RECOMMENDATION

After successful Aelari freeze:

recommend the next RP3 race.

Expected master-plan next candidate:

**Vael**

Do not start it.

The handoff must note:
- Fenn and Aelari are now separate frozen elven population references;
- Vael must not become “dark Aelari” or “subterranean Fenn”;
- shared engineering may be tested, but Vael body/head/ear biology requires its own gate;
- no universal elf topology has yet been declared.

---

# 26. STOP RULES

After committing the Aelari final freeze package:

**STOP FOR CHATGPT REVIEW.**

Do not:
- start Vael;
- start Halvren;
- alter frozen Fenn;
- alter active MPFB Family Base v005;
- declare universal elf anatomy/topology;
- finalize ear rigging;
- implement creator morphs;
- finalize UV/materials;
- generate LODs;
- integrate UE5.

---

## FINAL AUTHOR RULING

- Accept AEL1-R1 as the corrected canonical c1 Aelari central body source.
- Accept AELF190-R1 as the corrected canonical c2 Aelari central body source.
- Accept the bounded thoracic + leg-distribution correction.
- Accept the narrower but still valid final body margins.
- Keep the already-accepted Aelari face unchanged.
- Accept AE-E2 as the canonical central Aelari ear.
- Accept Fenn-v002 ear topology reuse as engineering topology only.
- Consolidate final Aelari c1/c2 production bodies.
- Run full validation and PC read-back.
- If all gates remain green, freeze Aelari RP3 by record.
- Stop before Vael.
