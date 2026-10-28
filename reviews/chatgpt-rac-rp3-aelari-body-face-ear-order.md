# RAC RP3 — Aelari c2 central reference + hidden-ear identity + conditional ear-branch architecture order

**Date:** 2026-10-27  
**Authority:** Tyler / ChatGPT after Fenn final freeze commit `78e4b4a1e0093017862d5171921e468a9a806f6a`.  
**Program references:**  
- `specs/aelari/AELARI_V1.md`;  
- `reviews/elf-comparative-review.md`;  
- `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md`;  
- `specs/RAC_PRODUCTION_MESH_CONTRACT.md`;  
- active MPFB Family Base v005;  
- frozen Fenn RP3 package, including Fenn ear topology v002, as **engineering precedent only**.

Aelari is the next RP3 race.

This order has three conditional stages:

1. establish a proper Aelari configuration-2 central reference at ~190 cm;
2. propagate the frozen MPFB family body to both configurations and run the Aelari-specific hidden-ear body + face identity gates;
3. **only if the hidden-ear gates pass**, prototype Aelari external ears and test whether the Fenn v002 ear topology architecture is reusable with Aelari geometry.

Do not freeze Aelari in this order.

---

# 1. AELARI IDENTITY FIREWALL

Aelari are **not**:
- taller Fenn;
- thin humans with pointed ears;
- universally pale;
- universally beautiful;
- biologically aristocratic, proud, wise or magical.

Aelari identity is whole-body **vertical continuity**:
- greater cranial vertical contribution;
- longer neck;
- longer torso / ribcage / waist transition;
- long arms and legs with elongation distributed more evenly than Fenn;
- long hands/fingers;
- gracile joints;
- elven shoulders/clavicles;
- distinct elven pelvis-to-leg architecture.

At equal height:
- **Fenn** = compact-centered, stronger extremity emphasis;
- **Aelari** = vertical elongation distributed continuously through neck, torso, arms and legs.

Every stage below must preserve that distinction.

---

# PART A — CONFIGURATION-2 CENTRAL REFERENCE

## 2. Accepted configuration-1 Aelari source

Use:

`AEL1`

- source: `reviews/reference-assets/r6/AEL1_r6.npz`
- SHA-256:  
  `7bc1021a6a68feea08d835c95d29e01e08ec3177f346bff62397964d300386fb`
- build: `reviews/reference-assets/builds/AEL1_build.json`
- build SHA-256:  
  `bf7ac6d63b508d9c4e0a5cae7b41acf5ec1cb6d0b2845557483c1dd279e52912`
- accepted: W1m
- stature: ~190.0136 cm.

Accepted stature envelope:
- min `AE168N-NAT` ~168 cm;
- central `AEL1` ~190 cm;
- max `AE221` ~221 cm.

Do not use a stature bound as the c2 central anchor.

---

## 3. Current AEL1 body architecture

Preserve the accepted AEL1 architecture, including:

- head vertical increase;
- neck-height increase;
- longer torso / nape-to-waist interval;
- longer upper and lower arms;
- longer upper and lower legs;
- shallow torso depth;
- lighter wrist/knee/ankle scale;
- long/narrow elven hands and feet;
- accepted pelvis/spine/leg bone-scale relationships;
- existing Aelari craniofacial targets.

Do not simplify the source to “Fenn + height.”

---

## 4. Create Aelari configuration-2 central reference

Create a central c2 reference at approximately:

**190 cm**

Recommended ID:

`AELF190`

or project-consistent equivalent.

Construction:
- use the accepted shared MPFB c2 route used for MF-F / SGF178 / FNF181;
- apply the **same Aelari race targets and bone-scale design logic** as AEL1;
- resolve stature coherently to ~190 cm;
- do not invent configuration-specific Aelari anatomy;
- no mandatory sex-related pelvic-width or ear difference.

If an existing diagnostic c2 build exists locally, audit provenance first rather than assuming acceptance.

---

## 5. c2 central-reference validation

Required:

### Determinism
- rebuild from record;
- full stature re-solve;
- max |dV| = 0;
- exact geometry identity.

### Integrity
- one component;
- zero boundary/non-manifold/degenerate defects;
- outward orientation;
- no coincident defects.

### Stature / envelope
- ~190 cm;
- coherent inside 168–221 cm accepted envelope.

### Aelari body identity
Compare c1/c2 at matched stature against:
- Marchfolk;
- Sagekin;
- frozen Fenn.

Validate:
- Aelari torso share > Fenn at equal height;
- Aelari neck contribution > Fenn;
- Aelari ribcage/waist vertical continuity > Fenn;
- arm elongation distributed more evenly than Fenn;
- leg elongation distributed more evenly than Fenn;
- long hands/fingers retained;
- joint gracility retained;
- Aelari is not merely the tallest human range.

### Pelvis
Audit author-accepted relational Aelari pelvis rules:
- hip-joint height/stature > Marchfolk;
- bitrochanteric/crest not measurably lower than Marchfolk;
- pelvic vertical contribution / iliac breadth > Marchfolk and > Fenn;
- longest average elven waist interval;
- no narrowing used as a shortcut.

Exact morphology/numeric envelopes remain OPEN; report ties below method resolution rather than inventing configuration-specific anatomy.

Return:
- **AELARI C2 CENTRAL REFERENCE PASS**
- **NEEDS AUTHOR DECISION**
- or **FAIL**.

If not PASS, STOP before Part B.

---

# PART B — FAMILY BODY PROPAGATION + HIDDEN-EAR IDENTITY

## 6. Active family base

Use only frozen MPFB Family Base v005:

- 57,842 V / 57,840 Q;
- face topology hash  
  `ec768ae210ea3ee1c053d0c4cd3256d57dad6db35d515502706b74f64281bee0`;
- active v005 hm08 map.

Authoritative validator:

**D1 + D3 + D4 + D5 + D6**

No family-base topology change.

---

## 7. Aelari body-family candidates

Create diagnostic unbranched body candidates:

### c1
source: `AEL1`

Suggested:
`AE_M_REF_RP3_bodyfam_v001.blend`

### c2
source: accepted/pass `AELF190`

Suggested:
`AE_F_REF_RP3_bodyfam_v001.blend`

These still carry the source/family human-type auricle and are **not final Aelari bodies**.

---

## 8. Standard technical gates

For both:
- exact source regeneration;
- exact v005 topology;
- V = M @ hm08;
- 100% quads;
- integrity pass;
- **69/69 D1–D6**;
- T-1/T-2/T-3/T-7;
- 9-zone density;
- contact audit;
- face/UFCA readiness;
- Standard v1 deformation suite;
- no new topology-class failure.

Ear zone is non-final source anatomy and must not be called a final Aelari-ear PASS.

---

# 9. HIDDEN-EAR BODY IDENTITY — HARD GATE

Compare at matched stature and matched frame/composition/age/pose:

- Aelari vs Fenn;
- Aelari vs Sagekin;
- Aelari vs Marchfolk.

External ears hidden/collapsed and excluded.

Aelari must retain identity through:

- neck length;
- vertical torso/ribcage continuity;
- waist transition;
- shoulders/clavicles;
- pelvis vertical contribution;
- evenly distributed arm elongation;
- evenly distributed leg elongation;
- joint scale;
- hands/fingers;
- feet.

### Equal-height Fenn/Aelari test
Hard question:

> With ears hidden and height equalized, does Aelari read as vertically continuous while Fenn remains compact-centered / extremity-emphasized?

Perfect instant classification is not required, but “same elf body at different height” is a FAIL.

If this body gate fails:
return **AELARI BODY NEEDS SOURCE/BRANCH WORK** and STOP before ears.

---

# 10. HIDDEN-EAR FACIAL IDENTITY — HARD GATE

Aelari facial canon must survive without ears.

Compare against:
- frozen Fenn CF2;
- matched Sagekin;
- matched Marchfolk.

Required Aelari tendencies:
- greater facial verticality;
- slightly greater cranial-height contribution;
- longer forehead-to-chin relationship;
- somewhat narrower lower face;
- lighter mandible on average;
- vertically oriented cheek/mid-face relationships;
- somewhat longer/narrower visible eye presentation than Fenn;
- lighter brow tendency, without mandatory delicacy.

Not required:
- small/narrow nose;
- one eye angle;
- V-shaped jaw;
- conventional beauty.

### Shared ancestry test
Aelari should look related to Fenn, but not like:
- CF2 Fenn stretched vertically;
- Fenn with narrower eyes;
- human face with pointed ears.

If the accepted AEL1/AELF190 sources do not actually express the written face canon:
- identify it as a **source geometry gap**;
- do not blame family topology;
- STOP before ear geometry;
- recommend bounded craniofacial source authoring, as was done for Fenn.

If hidden-ear body + face both PASS, continue to Part C.

---

# PART C — CONDITIONAL AELARI EAR BRANCH PROTOTYPE

## 11. Ear source limitation

Unless a committed accepted Aelari external-ear production source is found, treat the current MPFB auricle as **non-final**.

Aelari ears are genuinely non-human:
- not stretched human ears;
- related to Fenn by deeper ancestry;
- distinct Aelari population geometry.

---

# 12. Aelari ear canon

Compared with Fenn:

### Aelari tendency
- more upward orientation;
- cleaner gradual taper;
- somewhat closer to skull;
- moderate-to-long length.

### Fenn tendency
- more outward/backward projection;
- greatest average lateral projection among Fenn/Aelari/Vael.

Overlap is required:
- short-eared Aelari valid;
- long-eared Fenn valid.

Do not turn these into rigid species markers.

---

# 13. Canon-derived Aelari ear evidence

Use `tools/rac/w1/ear_families.py` / `ear_families_v2.py` Aelari evidence as shape guidance, not production topology.

Current AE-elven central evidence parameters:

- length ~**9.4 cm**;
- max half-width ~**1.70 cm**;
- continuous taper from ~0.25;
- lobe fraction ~0.14;
- bowl/concha depth ~0.62;
- projection ~**24°**;
- tilt ~**30°**;
- sweep ~**1.7 cm**;
- cartilage thickness ~0.25–0.27 cm;
- full helix/antihelix/crura/concha/tragus/lobe structures.

This is evidence geometry, not an automatic final answer.

---

# 14. Fenn topology reuse test — ENGINEERING ONLY

The frozen Fenn ear topology v002 may be tested as an engineering template because it has:

- proven 52-vertex root interface;
- proven cuff method;
- tapered-leaf upper extension;
- deformation-aware guard;
- creator-direction shape readiness.

But:

> **Fenn ear geometry must not be reused as Aelari anatomy.**

Test whether Fenn v002 **topology architecture** can express Aelari AE-elven geometry cleanly.

Two outcomes are allowed:

### REUSE PASS
One Aelari branch uses the Fenn-v002 engineering topology with wholly Aelari vertex geometry/parameters.

### REUSE FAIL
Aelari anatomy requires a locally revised topology; create a versioned Aelari-specific derivative.

Do not force reuse to save time.

Do not declare a universal elf ear topology.

---

# 15. Aelari ear candidate set

If the reuse test is viable, build one shared c1/c2 Aelari topology and three geometry candidates:

## AE-E1 restrained
- shorter / subtler;
- closer to skull;
- still clearly non-human.

## AE-E2 balanced central
- based around AE-elven evidence;
- ~9.4 cm central length;
- upward/clean taper;
- ~24° projection;
- ~30° long-axis orientation;
- recommended starting central candidate.

## AE-E3 stronger
- longer / stronger upward presence;
- still closer-set than Fenn central;
- not creator maximum;
- not “bigger Fenn.”

All three:
- same topology;
- same branch map;
- c1/c2 same topology;
- geometry only differs.

---

# 16. Ear anatomy / technical gates

Required anatomy:
- helix;
- antihelix stem + crura;
- triangular fossa;
- cymba/cavum;
- crus of helix;
- tragus/antitragus;
- intertragic notch;
- lobe;
- upper extension/tip;
- natural continuous taper.

Technical:
- 100% quads;
- one mesh;
- no boundary/non-manifold/degenerate faces;
- outward normals;
- no branch self-intersections;
- density <= 0.25% stature mean;
- no aspect > 10;
- T-4 reported;
- clean root;
- no burial/floating/seam;
- same topology c1/c2.

Use Fenn v002 quality as a benchmark, not a geometry target.

---

# 17. Static ear readiness

Run:
- neck flex/ext;
- head yaw ±45;
- pitch ±20;
- roll ±20.

Also bounded shape probes:
- projection;
- vertical orientation;
- sweep;
- length;
- tip sharp/blunt.

Required:
- no branch self-intersection;
- no root inversion;
- no broken seam;
- no catastrophic T-4/aspect spike.

No production ear rig.

---

# 18. Fenn-vs-Aelari visible-ear firewall

At matched height and same neutralized presentation compare frozen Fenn E2 against Aelari candidates.

Aelari must not read as:
- Fenn ear scaled longer;
- Fenn ear rotated upward;
- same elf preset with lower projection.

Look for a coordinated difference in:
- root-to-tip trajectory;
- taper distribution;
- projection;
- upper-extension proportion;
- internal cartilage layout/read;
- head/ear integration.

Shared ancestry should remain visible.

---

# 19. Visual package

## Part A/B
1. AEL1 vs c2 central reference;
2. Aelari c1/c2 body-family source vs production;
3. equal-height Aelari vs frozen Fenn, ears hidden;
4. Aelari vs Marchfolk/Sagekin, ears hidden;
5. body region comparisons:
   - neck/torso;
   - shoulder/clavicle;
   - pelvis/leg;
   - hands;
   - feet;
6. hidden-ear facial comparison vs Fenn/humans;
7. validator/margins;
8. density;
9. deformation.

## Part C if unlocked
10. AE-E1/E2/E3 full-head front/profile/3-4;
11. rear/top;
12. close ear anatomy;
13. wire/poles;
14. T-4/aspect;
15. root integration;
16. sections/thickness;
17. c1 vs c2 AE-E2;
18. Fenn E2 vs Aelari AE-E2 matched-height comparison;
19. hidden-ear confirmation;
20. static deformation/probes.

Do not return without actual inspectable images.

---

# 20. Decision logic

Return one overall result:

## AELARI BODY/FACE PASS + EAR BRANCH READY FOR AUTHOR SELECTION
Use if:
- c2 central reference passes;
- body propagation passes;
- hidden-ear body passes;
- hidden-ear face passes;
- ear prototype set is technically valid;
- only ear candidate selection/refinement remains.

## AELARI CRANIOFACIAL SOURCE WORK REQUIRED
Use if body passes but hidden-ear face does not express canon.

## AELARI BODY SOURCE/BRANCH WORK REQUIRED
Use if equal-height Aelari/Fenn body identity fails.

## AELARI EAR TOPOLOGY REVISION REQUIRED
Use if body/head pass but Fenn-topology reuse cannot cleanly express Aelari ear anatomy.

## FAIL
Use only for a true source/integrity blocker.

Do not freeze Aelari.

---

# 21. Required return

Commit:

1. `reviews/claude-rac-rp3-aelari-body-face-ear-gate.md`;
2. c2 central-reference source/build/sidecar;
3. central-reference validation;
4. Aelari body-family candidates;
5. propagation manifest;
6. D1–D6 validator outputs;
7. anatomy/density/contact/deformation audits;
8. equal-height hidden-ear Fenn/Aelari metrics;
9. hidden-ear facial metrics;
10. if unlocked:
    - ear topology/reuse record;
    - AE-E1/E2/E3 c1/c2 geometry;
    - branch maps;
    - T-4/density/root/deformation audits;
11. full visual package;
12. immutable hashes;
13. narrow STATUS update;
14. session handoff.

Explicitly answer:
- Was a valid ~190 cm c2 central reference created?
- Does it preserve Aelari vertical-continuity anatomy?
- Are both body realizations 69/69 D1–D6?
- Does equal-height hidden-ear Aelari vs Fenn body identity pass?
- Does hidden-ear Aelari facial identity pass?
- Is craniofacial source authoring required?
- Does current source lack final Aelari ear anatomy?
- Could Fenn v002 topology engineering be reused without reusing Fenn geometry?
- Were AE-E1/E2/E3 built on one topology?
- Which ear candidate is recommended?
- Does Aelari remain clearly related to but distinct from Fenn?
- Is any non-ear topology branch required?
- What should the next author decision be?

---

# 22. Stop rules

After committing the Aelari gate:

**STOP FOR CHATGPT REVIEW.**

Do not:
- freeze Aelari;
- start Vael;
- start Halvren;
- alter frozen Fenn;
- alter active MPFB Family Base v005;
- declare universal elf topology;
- finalize ear rigging;
- implement creator morphs;
- finalize UV/materials;
- generate LODs;
- integrate UE5.

---

## FINAL AUTHOR RULING

- Aelari is the next RP3 race.
- AEL1 is the accepted c1 reference.
- Create a proper ~190 cm c2 central reference with the same Aelari biological design.
- Prove Aelari body identity at equal height against frozen Fenn with ears hidden.
- Prove Aelari facial identity without ears.
- Aelari must never become taller Fenn.
- If body/head pass, test reuse of Fenn ear **engineering topology only**.
- Aelari ear geometry must be independently Aelari: more upward, cleaner taper, closer-set, moderate-to-long.
- No Aelari freeze without ChatGPT review.
