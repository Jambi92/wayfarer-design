# RAC RP3 — Halvren central mixed-expression anchor + hidden-ear mixed-ancestry gate order

**Date:** 2026-10-29  
**Authority:** Tyler / ChatGPT after Vael final freeze commit `79505d81d9773c32a6815038d5abbfe140383f87`.  
**Program references:**  
- `specs/halvren/HALVREN_V1.md`;  
- `reviews/elf-comparative-review.md`;  
- frozen Marchfolk / Skarn / Sagekin references;  
- frozen Fenn / Aelari / Vael RP3 references;  
- `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md`;  
- `specs/RAC_PRODUCTION_MESH_CONTRACT.md`;  
- active frozen MPFB Family Base v005.

Halvren is the next RP3 race.

Halvren requires a different approval model from the previous races:

> **One central Halvren production reference does not define the entire Halvren population.**

Halvren are a coherent mixed-ancestry population with broad, developmentally constrained variation. They are not a midpoint race and are not reducible to one human/elf slider.

This order establishes and audits a **central balanced mixed-expression anchor only**.

Do not freeze Halvren in this order.

Do not author the full inheritance/randomization system in RP3.

---

# 1. HALVREN BIOLOGICAL FIREWALL

Halvren are not:

- humans with pointed ears;
- generic elves with human proportions;
- a 50/50 numerical average;
- a midpoint between Marchfolk and a generic elf;
- a patchwork of source-race body parts;
- a single mandatory body/face phenotype.

There is:
- no generic human parent;
- no generic elf parent;
- no global “Elf Percentage” slider;
- no requirement that every Halvren look visibly mixed at a glance.

The central RP3 anchor must instead prove:

> one developmentally coherent, biologically plausible mixed human/elven realization that can serve as a production reference without falsely defining the population envelope.

---

# 2. CURRENT CENTRAL ANCHOR

Use:

`HVC1`

as the existing accepted **diagnostic central anchor**, not yet as the final canonical production source.

Source:
- `reviews/reference-assets/r6/HVC1_r6.npz`
- SHA-256:  
  `eeda7b31e8390c9df77f708848ced19d55b484f6d10eba411fa0f4fdaa29c2c6`
- build: `reviews/reference-assets/builds/HVC1_build.json`
- accepted: W1s
- stature: ~177.726 cm.

Current design:
- modest nape-to-waist decrease;
- forearm length +0.12;
- lower-leg height +0.12;
- torso depth −0.05;
- finger length +0.12;
- wrist circumference −0.15;
- ankle circumference −0.10;
- no current explicit race-specific face target package;
- current MPFB human auricle is non-final for Halvren.

Accepted central-population stature envelope:
- ~152–213 cm;
- reference ~178 cm;
- ancestry-conditioned minority tails exist beyond the central envelope.

Do not use the tail bounds as the central c2 reference.

---

# PART A — CONFIGURATION-2 CENTRAL ANCHOR

# 3. Create missing c2 central anchor

No accepted Halvren configuration-2 central reference was found.

Create a ~178 cm c2 counterpart using the accepted shared MPFB c2 route.

Recommended ID:

`HVF178`

or project-consistent equivalent.

Rules:
- apply the same HVC1 mixed-expression body design logic;
- preserve the same biological intent rather than copying c1 coordinates;
- no c2-specific Halvren ancestry package;
- no sex-specific Halvren pelvis/ear/face rule;
- solve stature coherently to ~178 cm.

This c2 is a **central mixed-expression anchor**, not a separate ancestry phenotype.

---

# 4. c2 anchor validation

Required:

### Determinism
- rebuild from committed record;
- independent stature resolve;
- max |dV| = 0.

### Integrity
- one component;
- 0 boundary / non-manifold / degenerate / coincident defects;
- outward normals.

### Stature
- ~178 cm;
- inside central 152–213 envelope.

### Configuration consistency
c1/c2 must express the same central mixed biological design.

Do not normalize away legitimate shared MPFB configuration differences.

---

# PART B — CENTRAL BODY PROPAGATION

# 5. Active family base

Use frozen MPFB Family Base v005 only.

No family-base changes.

Authoritative validator:

**D1 + D3 + D4 + D5 + D6**

---

# 6. Create diagnostic Halvren family candidates

### c1
`HV_M_REF_RP3_bodyfam_v001.blend`
from HVC1.

### c2
`HV_F_REF_RP3_bodyfam_v001.blend`
from the accepted/pass c2 central anchor.

These are diagnostic body candidates.

The family human auricle is explicitly **non-final Halvren ear anatomy**.

---

# 7. Standard technical gates

For both:

- source regeneration identity;
- exact v005 topology;
- V = M @ hm08;
- 100 % quads;
- integrity;
- **69 / 69 D1–D6**;
- T-1 / T-2 / T-3 / T-7;
- density;
- contact;
- face/UFCA readiness;
- Standard v1 deformation;
- no new topology-class defect.

Technical propagation PASS does not approve Halvren biology.

---

# PART C — CENTRAL MIXED-ANCESTRY BODY GATE

# 8. The central-anchor test is NOT “unique race classification”

Do not require the central Halvren to be instantly classifiable as “Halvren” against all source populations.

Halvren canon explicitly allows:
- source-population resemblance;
- subtle mixed expression;
- broad overlap.

The hard failure is different:

> the central anchor must not be an unchanged source-race body with the Halvren label, nor a mechanical midpoint, nor disconnected patchwork.

---

# 9. Matched-height comparison set

At ~178 cm, matched:
- frame;
- muscle;
- fat;
- age;
- pose;
- ears hidden;
- pigmentation neutralized;
- hair/presentation removed.

Compare the Halvren central anchor against:

### Human family
- frozen Marchfolk;
- Sagekin;
- Skarn diagnostic at matched height where supported.

### Elven family
- frozen Fenn;
- frozen Aelari;
- frozen Vael.

Use source-compatible diagnostic builds where exact frozen reference stature differs.

Do not modify frozen races.

---

# 10. Central body coherence questions

The gate must answer:

### Axial skeleton
Does HVC1/HVF178 show a coherent mixed torso/ribcage/spine relationship rather than simply Marchfolk torso plus longer limbs?

### Appendicular skeleton
Do shoulders, pelvis, arms, legs and joint relationships transition coherently?

### Distal anatomy
Do hands/feet look like coherent mixed anatomy, not elven fingers grafted onto a human wrist/foot base?

### Structural presence
Does the anchor occupy a plausible mixed space between human-family structural distributions and elven-family gracility without being a scalar average?

### Source-population protection
Does the full configuration avoid exact duplication of:
- Marchfolk;
- Sagekin;
- Skarn;
- Fenn;
- Aelari;
- Vael?

A strong resemblance to one source is allowed.

Systematic whole-body duplication is not.

---

# 11. “Not an arithmetic average” audit

Quantitatively test whether HVC1 is suspiciously close to simple midpoints.

For each major metric group:
- torso;
- shoulder/clavicle;
- arm;
- leg;
- joint scale;
- hand;
- foot;
- head/face if available;

compare HVC1 against simple human/elf pair midpoints, including at minimum:
- Marchfolk ↔ Fenn;
- Marchfolk ↔ Aelari;
- Marchfolk ↔ Vael;
- Sagekin ↔ one elf where useful;
- Skarn ↔ one elf where useful.

Do **not** fail because one metric happens to sit near a midpoint.

Fail only if the **whole system** behaves like a mechanical average without coherent independent relationships.

---

# 12. Central-anchor status outcomes

Return one:

## HALVREN CENTRAL BODY PASS
Use if HVC1/HVF178 form one coherent mixed realization suitable as the central production anchor.

## HALVREN BODY SOURCE WORK REQUIRED
Use if HVC1 is effectively a generic human / generic elf / simple midpoint / incoherent patchwork.

## HALVREN BODY TOPOLOGY BRANCH REQUIRED
Use only if the source anatomy is valid but the family topology cannot carry it.

Do not proceed to ear work unless the central body passes.

---

# PART D — PELVIS: PROTOTYPE / REPORT, DO NOT INVENT CANON

# 13. Halvren pelvis is still biologically OPEN in detail

The Halvren spec explicitly states:

> detailed pelvic inheritance is OPEN and requires prototypes/further anatomical design.

Therefore do **not** invent final Halvren pelvis morphology or numeric inheritance rules in this order.

Instead:

1. measure HVC1/HVF178 pelvic relationships against:
   - Marchfolk;
   - Sagekin/Skarn where useful;
   - frozen Fenn;
   - frozen Aelari;
   - frozen Vael;
2. report:
   - hip-joint height/stature;
   - bitrochanteric/crest relationship;
   - pelvic vertical contribution;
   - AP depth;
   - waist/torso continuity;
   - hip-joint scale proxy;
3. assess whether the current HVC1 pelvis is:
   - coherent mixed anatomy;
   - suspiciously stock human;
   - suspiciously copied elf;
   - or unresolved.

Allowed result:

**HALVREN PELVIS NEEDS AUTHOR DESIGN PASS**

This is not automatically a failure of the rest of the central anchor.

Do not silently create final pelvis canon.

---

# PART E — HIDDEN-EAR / NEUTRAL-PIGMENT FACE GATE

# 14. Halvren face approval rule

Halvren have no single mandatory face.

The central anchor must prove only that one coherent mixed craniofacial realization exists.

Hard rule:

> With ears hidden, pigment neutralized, hair removed and neutral expression, the central Halvren face must plausibly contain both human-family and elven-family craniofacial ancestry without looking like a human face plus fantasy ears.

---

# 15. Current source-face audit

HVC1 currently has no explicit Halvren craniofacial target package comparable to frozen Fenn/Aelari/Vael.

Therefore audit before assuming the face is acceptable.

Compare c1/c2 against:
- Marchfolk;
- Sagekin;
- Skarn;
- frozen Fenn;
- frozen Aelari;
- frozen Vael.

Assess:
- cranium;
- forehead/brow;
- orbital system;
- cheeks/midface;
- nose;
- jaw/chin;
- lower-face mass.

Do not require one fixed mixed phenotype.

---

# 16. Face failure conditions

Return:

## HALVREN CENTRAL FACE PASS
if the current anchor is a coherent mixed realization.

Return:

## HALVREN CRANIOFACIAL SOURCE WORK REQUIRED
if it reads essentially as:
- Marchfolk/Sagekin/Skarn face;
- one frozen elf face;
- or generic human with only ear difference.

If source work is required:
- do not blame topology unless proven;
- do not build ears yet;
- recommend a bounded mixed craniofacial candidate pass.

---

# 17. Anti-beauty / anti-stereotype gate

The central Halvren anchor must not be “fixed” by:
- narrowing the jaw merely to look elven;
- enlarging eyes;
- shrinking/straightening the nose;
- increasing symmetry;
- feminizing facial structure;
- making the character young/slim/beautiful.

Mixed ancestry is not a beauty filter.

---

# PART F — CONDITIONAL EAR ARCHITECTURE STUDY

# 18. Ear work unlock condition

Proceed only if:

- central body PASS;
- central face PASS or a separately accepted face candidate exists;
- no unresolved blocker requires source redesign.

If those conditions are not met, STOP before ear geometry.

---

# 19. Halvren ear principle

Halvren ears are:

> **not human ears with a pointiness slider.**

They may combine:
- human auricular root/base;
- helix/antihelix/concha/tragus/lobe relationships;
- elven length/taper/orientation/projection/curvature;

through a coherent mixed developmental ear.

No one midpoint ear is canonical for the population.

---

# 20. Central mixed-ear reference

For the RP3 central anchor only, create a **balanced mixed-expression ear candidate family**.

Do not claim this is the whole Halvren ear envelope.

Use existing `HV-mixed` W1 evidence only as a starting reference, not final anatomy.

Current evidence from `ear_families.py`:
- length ~7.6 cm;
- half-width ~1.80 cm;
- continuous taper beginning later than the elf references;
- lobe fraction ~0.18;
- concha depth ~0.72;
- projection ~26°;
- tilt ~20°;
- sweep ~0.9 cm;
- thickness ~0.29–0.30 cm.

This evidence may be revised if it reads like a simple midpoint.

---

# 21. Ear topology architecture test

Test three possibilities:

### HT1 — family-human-root-biased mixed ear
Preserve more human root/base architecture while extending the upper ear coherently.

### HT2 — elf-engineering-derived mixed ear
Test whether the proven Fenn/Aelari/Vael elf-ear engineering topology can express the balanced Halvren central ear without forcing fully elven root anatomy.

### HT3 — dedicated mixed derivative
Build a bounded Halvren-specific local derivative if neither HT1 nor HT2 produces a coherent mixed ear.

Do not choose topology reuse for convenience.

---

# 22. Ear candidate geometry

On the best topology architecture, create three central-anchor geometry strengths:

## HV-E1 subtle mixed
- mostly human-scale length;
- subtle non-human taper;
- coherent mixed root.

## HV-E2 balanced mixed
- intended central anchor;
- moderate elongation;
- mixed projection/orientation;
- neither human ear with point nor small elf ear.

## HV-E3 stronger elven expression
- still valid central-anchor exploration;
- stronger taper/length/orientation;
- does not copy frozen Fenn/Aelari/Vael geometry.

These are **phenotypic-expression candidates**, not genealogy percentages.

---

# 23. Ear firewall

Compare HV-E candidates against:
- Marchfolk human ear;
- frozen Fenn E2;
- frozen Aelari AE-E2;
- frozen Vael VA-E2-RI3.

Required:
- coherent mixed read;
- no exact copy;
- no arithmetic visual midpoint requirement;
- no nested human-ear-plus-elf-shell construction;
- no simple pointiness morph.

---

# 24. Ear technical gates

Required:
- 100 % quads;
- one mesh;
- 0 boundary / non-manifold / degenerate;
- outward normals;
- no branch self-intersection;
- density <= 0.25 % stature;
- aspect < 10;
- root integration clean;
- c1/c2 identical topology for the selected architecture.

Run:
- head/neck readiness;
- projection;
- tilt;
- sweep;
- length;
- tip;
- base-width probes where appropriate.

No production ear rigging.

---

# 25. Visual package

## Body / face
1. HVC1 vs c2 central anchor;
2. source vs family realization;
3. matched-height Halvren vs Marchfolk/Sagekin/Skarn;
4. matched-height Halvren vs frozen Fenn/Aelari/Vael;
5. body region comparisons:
   - torso;
   - shoulders;
   - pelvis;
   - arms/legs;
   - joints;
   - hands/feet;
6. arithmetic-midpoint diagnostic sheet;
7. pelvis report;
8. hidden-ear neutral-pigment face comparison;
9. face regional residual/descriptor sheet;
10. validator/margins;
11. density;
12. deformation.

## Ear if unlocked
13. HT1/HT2/HT3 architecture comparison;
14. HV-E1/E2/E3 full head;
15. ear front/profile/rear/top;
16. root/concha closeups;
17. wire/poles;
18. T-4/aspect;
19. root integration;
20. source-family ear comparison;
21. human + three frozen elves + Halvren ear firewall;
22. c1 vs c2 selected candidate;
23. readiness/probes.

Use true scale and identical cameras.

---

# 26. Overall result logic

Return one:

## HALVREN CENTRAL BODY/FACE PASS + EAR ARCHITECTURE READY FOR AUTHOR SELECTION
Use if:
- c2 central anchor valid;
- propagation technical gates pass;
- central body is coherent mixed anatomy;
- central face is coherent mixed anatomy;
- ear prototypes are technically valid.

## HALVREN BODY SOURCE WORK REQUIRED

## HALVREN CRANIOFACIAL SOURCE WORK REQUIRED

## HALVREN PELVIS NEEDS AUTHOR DESIGN PASS
May coexist with a body/face pass; report separately rather than inventing canon.

## HALVREN EAR ARCHITECTURE REVISION REQUIRED

## FAIL
Use only for a true source/integrity blocker.

Do not freeze Halvren.

---

# 27. Required return

Commit:

1. `reviews/claude-rac-rp3-halvren-central-anchor-gate.md`;
2. c2 central source/build/sidecar;
3. HVC1/c2 regeneration proof;
4. v005 family candidates;
5. propagation manifest;
6. D1–D6 validator outputs;
7. anatomy/density/contact/deformation;
8. matched-height six-source comparison metrics;
9. arithmetic-average audit;
10. pelvis prototype/report;
11. hidden-ear neutral-pigment face audit;
12. if unlocked:
    - HT1/HT2/HT3 topology study;
    - HV-E1/E2/E3 geometry;
    - branch maps;
    - ear quality/readiness;
13. full visual package;
14. immutable hashes;
15. narrow manifest/STATUS update;
16. session handoff.

Explicitly answer:
- Was a valid ~178 cm c2 central anchor created?
- Do c1/c2 express one shared central mixed design?
- Are both family candidates 69/69 D1–D6?
- Is the central body a coherent mixed realization?
- Does it avoid mechanical arithmetic averaging?
- Does it avoid exact whole-body duplication of a source population?
- Is the current Halvren pelvis coherent, or does it require an author design pass?
- Does the hidden-ear/neutral-pigment central face pass?
- Is craniofacial source authoring required?
- Was ear work unlocked?
- Which ear topology architecture is best: HT1, HT2, or HT3?
- Which ear candidate is recommended?
- Does the ear read as coherent mixed anatomy rather than a pointiness morph?
- Is any race-specific non-ear topology branch required?
- What is the next author decision?

---

# 28. Stop rules

After committing the Halvren gate:

**STOP FOR CHATGPT REVIEW.**

Do not:
- freeze Halvren;
- start Durrim;
- start Pipkin;
- start Cogling;
- alter frozen Fenn/Aelari/Vael;
- alter frozen human references;
- alter active MPFB Family Base v005;
- define the full genealogy/randomization system;
- create an “Elf Percentage” slider;
- silently finalize Halvren pelvis inheritance;
- implement creator morphs;
- finalize rigging;
- finalize UV/materials;
- generate LODs;
- integrate UE5.

---

## FINAL AUTHOR RULING

- Halvren is the next RP3 race.
- HVC1 is a central diagnostic mixed-expression anchor, not a definition of the whole Halvren population.
- Create a proper ~178 cm c2 central counterpart.
- Prove the central body/face are coherent mixed anatomy before touching ears.
- Do not average human and elf source values mechanically.
- Do not invent detailed Halvren pelvis inheritance where canon still says OPEN.
- If body + face pass, test mixed-ear architecture rather than a pointiness slider.
- No Halvren freeze without ChatGPT review.
