# RAC RP3 — Vael c2 central reference + three-elf hidden-ear identity + conditional ear-branch order

**Date:** 2026-10-28  
**Authority:** Tyler / ChatGPT after Aelari final freeze commit `40f5a8a03fc6f66a887e984ef2f035d19e0fe7fc`.  
**Program references:**  
- `specs/vael/VAEL_V1.md`;  
- `reviews/elf-comparative-review.md`;  
- `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md`;  
- `specs/RAC_PRODUCTION_MESH_CONTRACT.md`;  
- active frozen MPFB Family Base v005;  
- frozen Fenn RP3;  
- frozen Aelari RP3.

Vael is the next RP3 race.

This order has three conditional stages:

1. establish the missing Vael configuration-2 central reference at ~178 cm;
2. propagate the frozen MPFB family body to c1/c2 and prove Vael body + face identity with ears/pigmentation/presentation neutralized;
3. **only if body and face pass**, prototype the Vael external-ear branch and test reuse of the proven elf-ear engineering topology.

Do not freeze Vael in this order.

---

# 1. VAEL IDENTITY FIREWALL

Vael are **not**:
- dark-skinned Aelari;
- subterranean Fenn;
- humans with pointed ears;
- compact Skarn;
- dwarf-like elves;
- automatically muscular;
- biologically sinister, cruel, angry or predatory.

Vael population identity is:

- deeper skeletal torso / ribcage;
- stronger torso-to-pelvis continuity;
- more compact vertical distribution than Aelari;
- less extremity emphasis than Fenn;
- more joint and extremity-base presence than Fenn/Aelari;
- still gracile relative to humans;
- balanced arm/leg segmentation;
- moderately long elven hands/fingers with broader palm/base than Fenn/Aelari;
- moderately elongated, broader feet with stronger ankle-foot transition;
- Vael-specific craniofacial identity;
- Vael-specific external ears.

Identity must survive with:
- ears hidden;
- skin pigmentation neutralized;
- hair removed;
- presentation neutralized.

---

# PART A — CONFIGURATION-2 CENTRAL REFERENCE

## 2. Accepted configuration-1 Vael source

Use:

`VAL4`

- source: `reviews/reference-assets/r6/VAL4_r6.npz`
- SHA-256:  
  `ec73819d78226c4a4e992935cec2d7596ba2fa7228e1b392a5e9f340d3d1ed23`
- build: `reviews/reference-assets/builds/VAL4_build.json`
- accepted: W1n
- stature: ~178.0023 cm.

Accepted stature envelope:
- min `VA157-NAT` ~157 cm;
- central `VAL4` ~178 cm;
- max `VA203` ~203 cm.

Do not use the bounds as the c2 central reference.

---

# 3. VAL4 accepted body design to preserve

Current accepted VAL4 design includes:

- increased torso depth;
- moderate elven hand elongation;
- somewhat broader foot;
- broader finger spacing;
- modest orbital/eye enlargement;
- cheek-bone increase;
- more wrist/ankle/knee presence than Fenn/Aelari while still gracile;
- slightly reduced lower-leg height target;
- balanced arm segmentation;
- balanced leg segmentation;
- Vael pelvis architecture;
- stronger torso-pelvis continuity.

Current accepted bone-scale design includes:
- pelvis ~[1.02, 1.0, 1.03];
- thigh Y ~0.98849;
- calf Y ~1.02981;
- spine_03 Y ~0.9747;
- upperarm Y ~0.99414;
- lowerarm Y ~1.00565.

Do not simplify this into “Aelari made shorter” or “Fenn made deeper.”

---

# 4. Create configuration-2 central reference

No accepted Vael c2 central reference was found in the repository.

Create a central c2 reference at approximately:

**178 cm**

Recommended ID:

`VALF178`

or project-consistent equivalent.

Construction:
- use the accepted shared MPFB c2 route used for MF-F / SGF178 / FNF181 / AELF190-R1;
- apply the **same Vael race targets and bone-scale design logic** as VAL4;
- resolve stature coherently to ~178 cm;
- do not invent c2-specific Vael biology;
- no sex-specific pelvic, facial, or ear anatomy.

If a diagnostic local build exists, audit provenance first.

---

# 5. c2 central-reference validation

Required:

### Determinism
- rebuild from committed record;
- independent stature re-solve;
- max |dV| = 0;
- exact source identity.

### Integrity
- one component;
- zero boundary/non-manifold/degenerate defects;
- outward orientation;
- no coincident defects.

### Stature
- ~178 cm;
- within 157–203 cm envelope.

### Matched-stature identity
Compare c1/c2 against:
- frozen Fenn at 178;
- frozen Aelari at 178;
- Marchfolk;
- Sagekin.

Validate:
- deeper torso than Fenn/Aelari;
- less vertical torso/waist continuity than Aelari;
- less extremity share than Fenn;
- arm/leg elongation still > human in the intended combined system;
- more joint/base presence than Fenn/Aelari but less than humans where canon requires gracility;
- broader palm/base and foot transitions than Fenn/Aelari;
- no stocky/dwarf-like compactness.

---

# 6. Vael pelvis hard gate

Use the author-accepted Vael pelvis architecture.

At matched stature, skeletal proxy must establish:

### VA-P2a
hip-joint height / stature:
- > Marchfolk;
- < frozen Fenn;
- < frozen Aelari.

### VA-P2b
bitrochanteric / iliac-crest breadth:
- not lower than Marchfolk.

### VA-P2c
hip-joint scale:
- > Fenn;
- > Aelari;
- still gracile relative to Marchfolk.

### VA-P3
iliac structural presence:
- greatest of the three elves;
- still lighter than Marchfolk;
- no Aelari-style vertical iliac elongation.

### VA-P4
pelvic AP depth / stature:
- > Fenn;
- > Aelari;
- approximately Marchfolk is sufficient;
- Vael > Marchfolk is **not** required.

### VA-P6
costal-margin-to-crest interval / torso:
- < frozen Aelari;
- compact torso-pelvis continuity.

Also visually verify:
- natural human-homologous lumbar lordosis;
- no exaggerated curvature;
- no breadth shortcut;
- no configuration-specific pelvis.

Exact morphology/numeric envelopes remain OPEN.

If c2 cannot reproduce this without new sex-specific anatomy:
return **VAEL C2 NEEDS SOURCE DECISION** and STOP.

---

# PART B — MPFB BODY PROPAGATION + HIDDEN-EAR / NEUTRAL-COMPLEXION GATES

# 7. Active family base

Use only frozen MPFB Family Base v005.

No family-base changes.

Authoritative validator:

**D1 + D3 + D4 + D5 + D6**

---

# 8. Diagnostic Vael family candidates

Create:

### c1
`VA_M_REF_RP3_bodyfam_v001.blend`
from VAL4.

### c2
`VA_F_REF_RP3_bodyfam_v001.blend`
from accepted/pass VALF178.

These are diagnostic bodies and still carry the non-final family human auricle.

---

# 9. Standard technical gates

Both must pass:

- exact source regeneration;
- exact v005 topology;
- V = M @ hm08;
- 100% quads;
- integrity;
- **69/69 D1–D6**;
- T-1/T-2/T-3/T-7;
- 9-zone density;
- contact;
- face/UFCA readiness;
- Standard v1 deformation;
- no new topology-class defect.

Ear zone remains explicitly non-final.

---

# 10. THREE-ELF HIDDEN-EAR BODY GATE — HARD

At equal height, matched:
- frame;
- muscle;
- fat;
- age;
- pose;
- presentation;

hide/collapse ears and neutralize pigmentation.

Compare Vael to:
- frozen Fenn;
- frozen Aelari;
- Marchfolk;
- Sagekin.

### Vael must read as:
- deeper-bodied than Fenn/Aelari;
- more compact torso-to-pelvis continuity than Aelari;
- less extremity-emphasized than Fenn;
- more joint/base presence than both frozen elves;
- still distinctly elven vs humans;
- not stocky, dwarf-like, or Skarn-like.

### Required regional systems
- thoracic AP depth;
- torso/ribcage volume relationship;
- waist continuity;
- shoulder/neck integration;
- pelvis continuity;
- arm share/segment balance;
- leg share/segment balance;
- wrists/elbows/knees/ankles;
- palm/hand base;
- ankle/foot base.

Perfect classifier accuracy is not required.

If Vael becomes:
- dark Aelari with pigment removed,
- shortened Fenn,
- generic human,
return **VAEL BODY SOURCE/BRANCH WORK REQUIRED** and STOP before ears.

---

# 11. HIDDEN-EAR / NEUTRAL-COMPLEXION FACE GATE — HARD

Compare Vael against:
- frozen Fenn;
- frozen Aelari;
- Sagekin;
- Marchfolk.

Required Vael tendencies:

- less facial verticality than Aelari;
- more compact craniofacial vertical distribution;
- stronger cheek-to-midface integration;
- somewhat broader cheeks/orbits than Aelari;
- more mid-face structural depth than Aelari;
- stronger brow-orbit integration than Aelari without permanent scowl;
- somewhat more mandibular presence than Fenn/Aelari while remaining elven;
- moderate orbital size/definition;
- no dependence on complexion or glow.

### Nose
Do **not** require a single Vael nose.
“Stronger nasal/mid-face presence” may be population-level support, not a fixed nose type.

### Low-light adaptation
Do **not** invent:
- pupil shape;
- retinal mechanism;
- eye shine;
- glowing eyes;
- daylight weakness;
- gameplay bonus.

Those remain OPEN.

Only evaluate currently authored craniofacial/orbital anatomy.

If the source does not actually express the written Vael face canon:
return **VAEL CRANIOFACIAL SOURCE WORK REQUIRED** and STOP before ears.

---

# 12. Expression sanity

If hidden-ear face passes, run diagnostic expressions:
- neutral;
- speech if available;
- smile;
- anger;
- fear;
- surprise;
- sadness;
- blink;
- eye movement.

Guard:
- no permanent angry/sinister appearance;
- no orbit collapse;
- no new mouth-corner defect attributable to source anatomy.

Classify generic expression-unit issues as rig-stage items when appropriate.

Do not author production facial rigging.

---

# PART C — CONDITIONAL VAEL EAR BRANCH

# 13. Source limitation

VAL4 / VALF178 currently carry the MPFB human auricle unless a committed accepted Vael ear source is found.

Treat that auricle as non-final.

Vael external ears must be genuine non-human anatomy.

---

# 14. Vael ear canon

Compared with the frozen elf references:

### Vael
- somewhat broader base;
- more lateral/backward than Aelari;
- moderately shorter taper than Aelari;
- strong skull-attachment integration;
- not universally short/thick;
- not bat-like.

### Fenn
- greatest outward/backward projection on average.

### Aelari
- more upward/backward;
- closer-set;
- longer gradual taper.

Ear distributions overlap; one ear must not perfectly classify ancestry.

---

# 15. Vael evidence geometry

Use `tools/rac/w1/ear_families.py` / `ear_families_v2.py` VA-elven evidence as shape guidance only.

Current central evidence:

- length ~**8.4 cm**;
- max half-width ~**2.05 cm**;
- continuous taper start ~0.40, exponent ~1.25;
- lobe fraction ~0.16;
- bowl/concha depth ~0.68;
- projection ~**26°**;
- tilt ~**40°**;
- sweep ~**1.7 cm**;
- thickness ~0.29–0.30 cm;
- full helix/antihelix/concha/tragus/lobe structures.

Evidence geometry is not production topology and not pre-approved final geometry.

---

# 16. ELF-EAR TOPOLOGY REUSE TEST — ENGINEERING ONLY

Test whether the proven frozen Fenn-v002 connectivity—already reused successfully by Aelari—can carry Vael anatomy.

Allowed reuse:
- 52-vertex root interface;
- cuff engineering;
- tapered-leaf upper extension;
- block layout;
- deformation-aware guard;
- connectivity/parameterization.

Forbidden:
- Fenn vertex geometry;
- Aelari vertex geometry;
- automatic “universal elf ear” declaration.

Outcomes:

### REUSE PASS
Same engineering topology cleanly expresses wholly Vael geometry.

### REUSE FAIL
Create a bounded Vael-specific derivative topology.

Do not force reuse.

---

# 17. Vael ear candidates

If body + face pass, build one c1/c2 shared topology and three Vael geometry candidates:

## VA-E1 restrained
- somewhat shorter/subtler;
- broad base retained;
- moderate lateral/backward orientation.

## VA-E2 balanced central
Use VA-elven evidence as the starting center:
- ~8.4 cm;
- ~2.05 cm half-width evidence;
- ~26° projection;
- ~40° tilt;
- ~1.7 cm sweep;
- moderately shorter taper than Aelari.

## VA-E3 stronger
- somewhat longer/stronger;
- still not Fenn-level projection;
- not bat-like;
- not creator maximum.

All three:
- identical topology;
- same c1/c2 branch map;
- geometry only differs.

---

# 18. Ear anatomy / quality gates

Required anatomy:
- helix;
- antihelix stem + crura;
- triangular fossa;
- cymba/cavum;
- crus of helix;
- tragus;
- antitragus;
- intertragic notch;
- lobe;
- upper extension;
- natural Vael taper.

Technical:
- 100% quads;
- one mesh;
- no boundaries/non-manifold/degenerate faces;
- outward normals;
- no branch self-intersections;
- ear density mean <=0.25% stature;
- no aspect >10;
- T-4 reported;
- clean root;
- no seam/float/burial;
- identical topology c1/c2.

Use frozen Fenn/Aelari ear quality as benchmarks.

---

# 19. Vael visible-ear firewall

At matched presentation compare:
- Vael VA-E2 candidate;
- frozen Fenn E2;
- frozen Aelari AE-E2.

Vael must not read as:
- Fenn shortened;
- Aelari widened;
- either ear simply rotated.

Look for coordinated difference in:
- base width;
- root integration;
- taper onset/distribution;
- projection;
- tilt;
- upper-extension proportion;
- internal cartilage mass/read;
- lobe/root relationship.

Shared ancestry must remain plausible.

---

# 20. Ear deformation / probe readiness

Run:
- neck flex/ext;
- yaw ±45;
- pitch ±20;
- roll ±20.

Geometry-only probes:
- projection;
- tilt;
- sweep;
- length;
- tip blunt/sharp;
- base-width variation if supported without breaking root.

Required:
- no branch self-intersection;
- no root inversion;
- no broken seam;
- aspect <=10;
- no catastrophic T-4 spike.

No production ear rig.

---

# 21. Visual package

## Part A/B
1. VAL4 vs VALF178 c2 central;
2. source vs family realization;
3. equal-height three-elf body comparison, ears hidden:
   - Vael;
   - frozen Fenn;
   - frozen Aelari;
4. Vael vs Marchfolk/Sagekin;
5. torso depth/profile;
6. shoulder/neck;
7. pelvis/waist;
8. arm/hand base;
9. leg/ankle/foot base;
10. hidden-ear/neutral-complexion face comparison across all three elves + humans;
11. face regional residual/descriptor sheet;
12. validator/margins;
13. density;
14. deformation/expression sanity.

## Part C if unlocked
15. VA-E1/E2/E3 front/profile/3-4;
16. rear/top;
17. close ear anatomy;
18. wire/poles;
19. T-4/aspect;
20. root integration;
21. sections/thickness;
22. c1 vs c2 VA-E2;
23. Fenn E2 vs Aelari AE-E2 vs Vael VA-E2;
24. hidden-ear confirmation;
25. ear readiness/probes.

Use identical cameras and true scale.

No gate return without inspectable images.

---

# 22. Decision logic

Return one overall result:

## VAEL BODY/FACE PASS + EAR BRANCH READY FOR AUTHOR SELECTION
Use if:
- c2 central reference passes;
- family propagation passes;
- three-elf hidden-ear body gate passes;
- hidden-ear/neutral-complexion face passes;
- ear candidate set passes technically.

## VAEL BODY SOURCE/BRANCH WORK REQUIRED
Use if body identity does not meet the comparative canon.

## VAEL CRANIOFACIAL SOURCE WORK REQUIRED
Use if body passes but face source does not express canon.

## VAEL EAR TOPOLOGY REVISION REQUIRED
Use if body/head pass but shared ear engineering topology cannot express Vael anatomy.

## FAIL
Use only for a true source/integrity blocker.

Do not freeze Vael.

---

# 23. Required return

Commit:

1. `reviews/claude-rac-rp3-vael-body-face-ear-gate.md`;
2. c2 central source/build/sidecar;
3. central-reference validation;
4. Vael body-family candidates;
5. propagation manifest;
6. D1–D6 validator outputs;
7. anatomy/density/contact/deformation audits;
8. Vael pelvis validation;
9. three-elf equal-height hidden-ear body metrics;
10. hidden-ear/neutral-complexion face metrics;
11. expression sanity;
12. if Part C unlocks:
    - topology reuse/derivative record;
    - VA-E1/E2/E3 c1/c2 geometry;
    - branch maps;
    - ear quality/root/deformation audits;
13. full visual package;
14. immutable hashes;
15. narrow manifest/STATUS update;
16. session handoff.

Explicitly answer:
- Was a valid ~178 cm c2 central reference created?
- Does it reproduce the accepted Vael design without config-specific anatomy?
- Do all Vael pelvis rules hold?
- Are both family bodies 69/69 D1–D6?
- Does three-elf hidden-ear body identity pass?
- Does Vael remain elven against humans?
- Does hidden-ear neutral-complexion face identity pass?
- Is craniofacial source authoring required?
- Was any low-light physiology invented? (required answer: no unless separately authorized)
- Does the source lack final Vael ear anatomy?
- Can the proven elf-ear engineering topology express Vael anatomy?
- Were VA-E1/E2/E3 built on one topology?
- Which ear candidate is recommended?
- Does Vael remain related to but distinct from frozen Fenn and Aelari?
- Is any non-ear topology branch needed?
- What is the next author decision?

---

# 24. Stop rules

After committing the Vael gate:

**STOP FOR CHATGPT REVIEW.**

Do not:
- freeze Vael;
- start Halvren;
- alter frozen Fenn;
- alter frozen Aelari;
- alter active MPFB Family Base v005;
- declare universal elf anatomy/topology;
- decide low-light gameplay/physiology beyond existing canon;
- finalize ear rigging;
- implement creator morphs;
- finalize UV/materials;
- generate LODs;
- integrate UE5.

---

## FINAL AUTHOR RULING

- Vael is the next RP3 race.
- VAL4 is the accepted c1 reference.
- Create a proper ~178 cm c2 central reference with the same Vael biological design.
- Prove Vael body identity against **both frozen elves** with ears/pigmentation/presentation neutralized.
- Prove Vael facial identity without ears or complexion.
- Do not invent unresolved low-light physiology.
- If body/head pass, test reuse of the proven elf-ear **engineering topology only**.
- Vael ear geometry must independently express its broader base, stronger attachment, lateral/backward orientation, and shorter taper than Aelari.
- No Vael freeze without ChatGPT review.
