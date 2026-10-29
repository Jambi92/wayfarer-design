# RAC RP3 — Vael final consolidation / validation / freeze order

**Date:** 2026-10-28  
**Authority:** Tyler / ChatGPT review of Claude root-integration return `f25b3457b714a99fa17531297e5e0b32022a0f97`.  
**Parent gates:**  
- `reviews/claude-rac-rp3-vael-body-face-source-gate.md`;  
- `reviews/claude-rac-rp3-vael-custom-body-deformation-gate.md`;  
- `reviews/claude-rac-rp3-vael-elf-frame-human-firewall-gate.md`;  
- `reviews/claude-rac-rp3-vael-ear-prototype-gate.md`;  
- `reviews/claude-rac-rp3-vael-ear-root-integration-gate.md`.  
**Prepared plan:** `reviews/claude-rac-rp3-vael-final-consolidation-plan.md`.

This order formally accepts the final Vael body, face, and ear architecture and authorizes **final Vael consolidation, complete RP3 validation, PC read-back, and freeze-by-record**.

If every final gate stays green, Vael RP3 should be closed.

Do not start Halvren in this order.

---

# 1. FINAL AUTHOR DECISIONS — ACCEPTED

## 1.1 Final Vael c1 body source

Accept:

`VAL4-R1-VD2-VF2`

as the canonical central configuration-1 Vael body source.

Source:
- `reviews/reference-assets/r6/VAL4-R1-VD2-VF2_r6.npz`
- R-6 SHA-256:  
  `fec300953b2306c326e738c0606a9d7218668592d12d616324a7b78c8a0f8fd0`
- build SHA-256:  
  `32fd7ffa80519380caf94b94eca91174be97476f585ee3c9a654242047f6d470`
- geometry hash:  
  `a800b533b3f847af599a99a358cf1339968eec4d21af2497b4fa02bfe5a6be77`
- stature: ~177.993 cm.

Lineage:
VAL4 → R1 source correction → VD2 Vael body field → VF2 elf-frame correction.

---

## 1.2 Final Vael c2 body source

Accept:

`VALF178-R1-VD2-VF2`

as the canonical central configuration-2 Vael body source.

Source:
- `reviews/reference-assets/r6/VALF178-R1-VD2-VF2_r6.npz`
- R-6 SHA-256:  
  `c338d97240c29129fef85578818eba84f632f99918fc9ed6861325937444e1e8`
- build SHA-256:  
  `0e32948a4c9fc3f648602a07f28983456b462669693c5fbe08740bf69ebd6aa1`
- geometry hash:  
  `1db646d28f0eb625e2dd501b58374edb9a3adbfdbbbd3816b27ae52a29ff75ad`
- stature: ~178.001 cm.

No configuration-specific Vael biology is authorized.

---

## 1.3 Vael body architecture

Accept the complete R1 + VD2 + VF2 architecture.

This includes:

- deeper skeletal torso/ribcage;
- compact torso-to-pelvis continuity;
- less vertical elongation than frozen Aelari;
- less extremity emphasis than frozen Fenn;
- more structural/joint/base presence than frozen Fenn/Aelari while remaining elven;
- balanced arm/leg segmentation;
- broader palm/hand-base and ankle/foot-base relationships;
- Vael pelvis ordering;
- VDF1.2 body field;
- VEF1 elf-frame term;
- clavicle/axillary/shaft-gracility adjustments.

Final body canon at the source gate:
- 20 / 20 body canon rows;
- human firewall PASS;
- three-elf firewall PASS.

Do not reopen source anatomy during consolidation.

---

## 1.4 Vael craniofacial source

Accept:

**VC2**

as the final central Vael craniofacial direction.

Keep:
- stronger mid-face integration;
- somewhat broader cheek/orbit system than Aelari;
- more compact facial vertical distribution than Aelari;
- stronger brow-orbit integration without permanent scowl;
- more mandibular presence than Fenn/Aelari while remaining elven;
- neutral-complexion hidden-ear identity.

Final requirements remain:
- Vael face systems 6 / 6;
- elf-comparative face rows 9 / 9.

Do not change VC2.

No low-light physiology is authored by this freeze.

---

## 1.5 VA-E2 selected ear direction

Accept:

**VA-E2**

as the canonical central Vael external-ear direction.

Keep the reviewed Vael visual identity:
- broadest-base elf ear of the three central references;
- intermediate projection;
- strong backward trajectory;
- moderately shorter/blunter taper than Aelari;
- stronger skull attachment integration;
- clearly distinct from frozen Fenn E2 and frozen Aelari AE-E2;
- not bat-like;
- not a shortened Fenn ear;
- not a widened Aelari ear.

Do not reopen VA-E1/E2/E3 selection.

---

## 1.6 RI3 root / concha integration

Accept:

**RI3**

as the final VA-E2 root/concha solution.

RI3 is the accepted fix for the layered-ear / nested-ear problem.

Required final interpretation:

> one continuous biological auricle from skull attachment through concha / tragus / antihelix / helix into the Vael outer leaf.

The old raised cuff perimeter is rejected and must not return.

Accepted RI3 engineering:
- concha clearance setting ~−0.30 cm relative to the prototype scheme;
- skin-hugging cuff;
- bounded Vael-specific local cuff derivative;
- six cuff rings:
  - 52 / 56 / 60 / 64 / 66 / 68;
- one extra cuff ring relative to Fenn/Aelari;
- root interface unchanged;
- root band unchanged;
- junction ring unchanged;
- outer sheet silhouette preserved.

---

## 1.7 Vael ear topology v002

Accept:

`VAEL_EAR_BRANCH_TOPOLOGY_v002`

as the Vael-specific final ear topology.

Record:
- 59,076 vertices;
- 59,074 quads;
- face-topology SHA-256:  
  `f8367ab09385d218559b6d3cac52ed159a9249cf12d91807e93e3b095d9ac297`
- map SHA-256:  
  `ad312c8028642f6a0f4df4d6b307ec5db23c589b19a6f9b88503832d79e3bdbb`
- cuff canon:  
  `VAEL_EAR_CUFF_CANON_v001.json`
- cuff canon SHA-256:  
  `1a0b070b42e84846d1b7beebfd153fec8d1ddf4e5a1d2ecc54a0d4351549a779`.

This topology is:

> a Vael-specific local derivative of the proven Fenn/Aelari engineering architecture.

It is **not** universal elf topology.

---

# 2. ACCEPTED PROJECTION RESIDUAL

The primary population-level outward projection order is accepted through the auricle-body angle:

- Fenn E2 ~52.7°;
- Vael RI3 ~37.4°;
- Aelari AE-E2 ~27.2°.

This correctly reads:

**Fenn > Vael > Aelari**

on both configurations.

RI3 also restores the mean / median / tip stand-off ordering on c2.

On c1, normalized Vael stand-off remains approximately:

- mean free-ear stand-off ~0.005 head-height above frozen Fenn;
- tip stand-off ~0.004 head-height above frozen Fenn.

This is an **accepted secondary measurement residual**.

Reason:
- the primary angular/visual projection hierarchy is correct;
- Vael visually remains intermediate;
- ear length, base geometry and head scale influence stand-off;
- correcting the tiny c1 reversal would require distorting the accepted Vael ear solely to chase a secondary scalar.

Do **not** deform RI3 during consolidation to force c1 mean/tip stand-off ordering.

Record the residual in the freeze record.

---

# 3. FINAL PRODUCTION FILES

Produce:

## Configuration 1
`VA_M_REF_RP3_v001.blend`

Composition:
- VAL4-R1-VD2-VF2 source;
- accepted VC2 face;
- frozen MPFB Family Base v005 everywhere outside the ear branch;
- VA-E2 outer ear geometry;
- RI3 root/concha integration;
- VAEL_EAR_BRANCH_TOPOLOGY_v002.

## Configuration 2
`VA_F_REF_RP3_v001.blend`

Composition:
- VALF178-R1-VD2-VF2 source;
- same accepted Vael biological architecture;
- same VC2 face logic;
- same VA-E2 / RI3 ear construction;
- same Vael ear topology v002.

No config-specific topology.

---

# 4. CLEAN REBUILD / PROVENANCE

Rebuild from committed immutable inputs only.

Required:

1. regenerate VF2 R-6 sources from build records;
2. prove max |dV| = 0;
3. independently rebuild full source record;
4. prove exact source geometry identity;
5. export native hm08;
6. propagate onto frozen MPFB v005;
7. prove family realization equals the reviewed `VA_{M,F}_REF_RP3_bodyfam_v004`;
8. rebuild VA-E2-RI3 from:
   - committed Vael parameters;
   - VAEL_EAR_CUFF_CANON_v001;
   - topology v002;
   - recorded guard settings;
9. prove RI3 geometry arrays equal the reviewed candidate:
   - max |dV| = 0;
   - faces identical;
10. write final production blends.

Stop on any mismatch.

---

# 5. FINAL SIDECARS / MAPS

Create:

- `VA_M_REF_RP3_v001.json`
- `VA_F_REF_RP3_v001.json`
- `VA_M_REF_RP3_v001_landmarks.json`
- `VA_F_REF_RP3_v001_landmarks.json`
- `VA_M_REF_RP3_v001_branch_map.npz`
- `VA_F_REF_RP3_v001_branch_map.npz`

Branch-map records must preserve:
- v005→final index map;
- removed v005 ear zone;
- root interface;
- weight/proxy rows;
- part/side;
- topology/cuff provenance;
- source/branch hashes.

---

# 6. FULL INTEGRITY GATE

Both final production bodies require:

- 100 % quads;
- one connected component;
- 0 boundary edges;
- 0 non-manifold edges;
- 0 non-manifold vertices;
- 0 degenerate faces;
- winding consistent;
- outward normals;
- no coincident defects;
- 0 branch self-intersections;
- no new branch-attributable whole-body rest contact;
- no root seam;
- no floating root;
- no buried root.

Expected topology:
- **59,076 V / 59,074 Q**.

Face-topology hash must be identical c1/c2.

---

# 7. AUTHORITATIVE VALIDATOR

Run:

**D1 + D3 + D4 + D5 + D6**

Required:
- **69 / 69** c1;
- **69 / 69** c2.

Compare against reviewed VF2 family realization:
- loops;
- margins;
- valid sides;
- D5 exclusions;
- D6 exclusions.

No body-joint verdict may change due to the ear branch.

Vertex-order fallback-label differences may be documented if underlying station data is equivalent.

---

# 8. PRIMARY ANATOMY / SOURCE-FIT GATE

The Vael R-6 sources still contain the obsolete MPFB human auricle.

Therefore run:

### Ear-excluded primary anatomy
T-1 / T-2 / T-3 / T-7 with the final external-ear branch excluded from source-fit judgment.

Required:
- body PASS;
- head excluding ear PASS;
- hands PASS;
- feet PASS;
- stature/bbox PASS;
- silhouette outside ear pixels PASS.

### Unmasked transparency run
Also report normal anatomy.py unmasked.

It may fail only because:
- source = human MPFB auricle;
- production = accepted VA-E2-RI3 ear.

Localize the divergence to the ear branch.

Any non-ear source-fit failure blocks freeze.

---

# 9. VAEL HUMAN FIREWALL — FINAL

Re-run neutralized Vael vs Marchfolk / Sagekin.

Ears and pigmentation neutralized.

Required Vael signal:
- deeper skeletal torso/ribcage;
- compact torso-pelvis continuity;
- elven limb relationships;
- more structural presence without becoming human;
- Vael hand/foot-base identity;
- elf-frame shoulder/clavicle signal;
- limb shaft gracility.

Vael must not collapse back to Marchfolk at full-body scale.

Final firewall must equal the accepted VF2 result.

---

# 10. THREE-ELF BODY FIREWALL — FINAL

At equal height, ears/pigmentation/presentation neutralized:

### Fenn
- strongest extremity emphasis;
- lowest joint/base presence;
- shallower torso;
- most outward ear population tendency.

### Aelari
- strongest vertical continuity;
- longest neck/torso/waist distribution;
- most upward/close-set central ear.

### Vael
- deeper torso;
- more compact torso-pelvis continuity;
- more joint/base presence;
- moderate limb elongation;
- lower center of mass than Aelari;
- structurally distinct from Fenn and Aelari.

No exaggerated separation is required.

All accepted three-elf rows must remain green.

---

# 11. VAEL PELVIS FINAL GATE

Re-run the accepted pelvis suite.

Required:
- **9 / 9**;
- all required comparisons at t = 0 / 0.5 / 1.0.

Keep:

### VA-P2a
hip ordering:

> Marchfolk < Vael < Aelari < Fenn

where the accepted comparative metric applies.

### VA-P2b
bitrochanteric / crest not lower than MF.

### VA-P2c
Vael hip-joint scale greater than Fenn/Aelari while still gracile to humans.

### VA-P3
greatest structural presence among the three elf pelves, but lighter than MF.

### VA-P4
AP depth > Fenn/Aelari; approximately MF is sufficient.

### VA-P6
waist / torso continuity more compact than Aelari.

Natural lumbar lordosis remains plausible and not exaggerated.

No pelvis change during consolidation.

---

# 12. HIDDEN-EAR FACE FINAL GATE

Re-run VC2 hidden-ear / neutral-complexion comparisons.

Required:

- Vael face systems **6 / 6**;
- comparative elf rows **9 / 9**;
- distinct from frozen Fenn;
- distinct from frozen Aelari;
- distinct from humans without complexion.

Preserve:
- compact vertical distribution;
- stronger mid-face;
- broader cheek/orbit tendency than Aelari;
- stronger brow-orbit integration;
- more mandible presence.

No permanent angry/sinister read.

Do not invent low-light eye physiology.

---

# 13. UFCA / EXPRESSION READINESS

Reconfirm:
- mouth rings;
- orbit rings;
- mouth-corner poles;
- poles near eyes;
- open mouth/orbit pockets;
- face density.

Run the same diagnostic expression sanity as previously accepted.

No source-level facial regression.

Any generic expression-unit issue remains rig-stage only if already classified as such.

---

# 14. EAR FINAL GATE — VA-E2-RI3

Rebuild the exact selected candidate.

For both configurations require:

- topology = VAEL_EAR_BRANCH_TOPOLOGY_v002;
- VA-E2 outer silhouette preserved;
- RI3 skin-hugging root/concha integration preserved;
- one continuous auricle read;
- root valence 4, 52 per side;
- 0 branch self-intersections;
- no seam / float / burial;
- density <= 0.25 % stature mean;
- aspect < 10.

Reviewed RI3 quality class:

### c1
- T-4 ~123 branch faces;
- min corner ~25.9°;
- aspect max ~9.26.

### c2
- T-4 ~144 branch faces;
- min corner ~14.9°;
- aspect max ~9.26.

Do not worsen these materially.

---

# 15. ROOT / CONCHA BIOLOGICAL READ — HARD VISUAL GATE

Final production ear must still answer:

> If the point were removed, would this read as one coherent ear?

Required answer: **yes**.

Also:

> Does the viewer perceive one auricle, not a smaller ear nested inside a fantasy outer ear?

Required answer: **one auricle**.

Check final:
- neutral clay;
- 3/4 front;
- profile;
- 3/4 rear;
- horizontal root/concha sections;
- current-vs-final overlay.

The raised human-root cuff perimeter must not reappear.

---

# 16. THREE-ELF VISIBLE-EAR FIREWALL

Compare final Vael RI3 to:
- frozen Fenn E2;
- frozen Aelari AE-E2.

Required:
- Vael broadest base;
- Vael intermediate angular projection;
- Vael stronger backward trajectory;
- Vael shorter/blunter taper than Aelari;
- Fenn still visually most outward;
- Aelari still visually most upward/close-set.

Accept the c1 secondary normalized stand-off residual from §2.

Do not fail the freeze solely because c1 mean/tip normalized stand-off is a few thousandths HH above Fenn if the visual and auricle-angle hierarchy remains correct.

---

# 17. DENSITY

Run all 9 standard density zones plus Vael ear branch.

Required:
- all family zones PASS;
- ear branch mean <= 0.25 % stature;
- no accidental density change during export.

---

# 18. BODY DEFORMATION FINAL GATE

Run Standard v1 18-pose deformation suite.

Final body must add:
- 0 new rest-contact class;
- no new topology-class failure vs VF2 family realization.

### Registered carry-forward
Preserve:

**VAEL-CF-SHOULDER-1**

Configuration 1:
- shoulder flex 90° = 19 flips;
- Marchfolk v005 = 13;
- +6;
- configuration 2 = +2.

Class:
**RIG / WEIGHT / SHOULDER-CORRECTIVE CARRY-FORWARD**

This is accepted and must not reopen VF2 anatomy or topology.

If final consolidation reproduces the same behavior, record it unchanged.

Any new deformation excess outside that registered class requires review.

---

# 19. EAR / HEAD DEFORMATION READINESS

Run:
- neck flex/ext 30°;
- yaw ±45°;
- pitch ±20°;
- roll ±20°.

Required:
- 0 branch contacts attributable to ear;
- 0 flipped branch faces;
- 0 root inversions;
- no concha collapse;
- no cuff separation;
- clearance preserved.

---

# 20. SHAPE-PROBE RETENTION

Re-run RI3 c1 probes:

- projection ±10°;
- tilt ±8°;
- sweep ±0.6;
- length ±10 %;
- tip blunt/sharp;
- base width ±8 %.

Required:
- 12 / 12 intended measures move correctly;
- topology unchanged;
- no branch self-intersection;
- no boundary/non-manifold;
- root valence 4;
- aspect < 10;
- no split between “fixed inner ear” and “moving outer shell.”

No creator morphs are implemented.

---

# 21. FINAL VISUAL FREEZE PACKAGE

Provide final inspectable sheets:

1. c1 full body;
2. c2 full body;
3. three-elf hidden-ear body comparison;
4. Vael vs human firewall;
5. pelvis validation;
6. hidden-ear neutral-complexion face;
7. c1 head front/profile/3-4;
8. c2 head front/profile/3-4;
9. final VA-E2-RI3 neutral clay;
10. ear front/profile/rear/top;
11. root/concha closeups;
12. root/concha sections;
13. ear wire/poles;
14. T-4/aspect;
15. root integration;
16. Vael vs frozen Fenn vs frozen Aelari ears;
17. projection/stand-off metrics;
18. body deformation;
19. ear readiness / probes;
20. source→production overlay.

No freeze without the final visual package.

---

# 22. PRODUCTION FRAME / PC READ-BACK

Write final production blends in standard frame:

- meters;
- Z up;
- faces −Y;
- subject left +X;
- origin pelvis root on ground.

Production directory:
`E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Vael/RP3/`

After writing:
- copy final files;
- read back without saving;
- verify file SHA;
- geometry hash;
- face-topology hash;
- candidate equality;
- branch-map equality;
- landmark/sidecar hashes;
- validator recomputed from read-back = 69 / 69 both.

PC copies must be byte-identical to the freeze record.

---

# 23. FREEZE BY RECORD

If every gate passes, create:

`VAEL_RP3_FREEZE.json`

and:

`reviews/claude-rac-rp3-vael-final-freeze-report.md`

Freeze by record; do not resave production blends only to change status.

Freeze record must contain:

- final filenames;
- full file SHA-256;
- geometry hashes;
- face-topology hash;
- VAEL_EAR_BRANCH_TOPOLOGY_v002 hashes;
- branch-map hashes;
- cuff canon hash;
- VF2 source hashes;
- VC2 provenance;
- VDF1.2 / VEF1 definition hashes;
- active v005 hashes;
- frozen Fenn/Aelari comparison hashes;
- validator results;
- body/human/three-elf firewall results;
- pelvis 9/9;
- hidden-ear face result;
- ear root-integration result;
- T-4/aspect/density;
- deformation;
- VAEL-CF-SHOULDER-1;
- shape probes;
- accepted c1 stand-off residual;
- exact PC read-back.

Freeze record is authoritative over embedded status strings.

---

# 24. REFERENCE / SPEC / STATUS UPDATES

On successful freeze update:

- `reviews/reference-assets/manifest.json`;
- `specs/vael/VAEL_V1.md`;
- `specs/STATUS.md`;
- `specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md` only as needed to mark VAEL-CF-SHOULDER-1 carried into final freeze;
- session handoff.

Final lineage must be explicit:

### c1
VAL4 ancestry → R1 → VD2 → VF2 → `VA_M_REF_RP3_v001`

### c2
VALF178 route → R1 → VD2 → VF2 → `VA_F_REF_RP3_v001`

### ear
VA-E2 → RI3 → VAEL_EAR_BRANCH_TOPOLOGY_v002.

No universal elf topology declaration.

---

# 25. FINAL RESULT

Return exactly one:

## VAEL RP3 FINAL PASS — AUTHOR ACCEPTED / FROZEN

Use only if every gate and read-back passes.

### OR

## VAEL FINAL CONSOLIDATION NEEDS AUTHOR DECISION

Use only for a new, non-blocking residual not already accepted.

### OR

## FAIL

Use for a genuine blocker.

---

# 26. NEXT RACE RECOMMENDATION

After successful Vael freeze:

recommend the next RP3 race.

Expected master-plan next candidate:

**Halvren**

Do not start it.

Handoff must note:
- Fenn, Aelari, Vael are now separate frozen elf population references;
- Halvren mixed ancestry must not be implemented as a simple average;
- shared ear engineering may inform Halvren, but Halvren needs its own biological gate.

---

# 27. STOP RULES

After committing the Vael final freeze package:

**STOP FOR CHATGPT REVIEW.**

Do not:
- start Halvren;
- modify frozen Fenn;
- modify frozen Aelari;
- modify active MPFB Family Base v005;
- decide low-light physiology;
- declare universal elf topology;
- implement creator morphs;
- finalize production ear rigging;
- finalize UV/materials;
- generate LODs;
- integrate UE5.

---

## FINAL AUTHOR RULING

- Accept VF2 body and VC2 face.
- Accept VA-E2 as the central Vael ear.
- Accept RI3 as the final root/concha integration.
- Accept VAEL_EAR_BRANCH_TOPOLOGY_v002 as the Vael-specific local ear topology.
- Accept the small c1 normalized stand-off reversal as a secondary measurement residual.
- Preserve VAEL-CF-SHOULDER-1 for production rigging.
- Do not run another Vael ear iteration.
- Consolidate final c1/c2 production bodies.
- Run the complete validation and PC read-back.
- If every gate remains green, freeze Vael RP3 by record.
- Stop before Halvren.
