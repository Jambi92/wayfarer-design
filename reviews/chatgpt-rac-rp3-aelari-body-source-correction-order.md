# RAC RP3 — Aelari bounded body-source correction order

**Date:** 2026-10-27  
**Authority:** Tyler / ChatGPT review of Claude Aelari gate `a4f81979a75f61f8a355b2f2d6f74de118caebdb`.  
**Parent gate:** `reviews/claude-rac-rp3-aelari-body-face-ear-gate.md`.  
**Program references:**  
- `specs/aelari/AELARI_V1.md`;  
- `reviews/elf-comparative-review.md`;  
- `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md`;  
- frozen Fenn RP3 reference;  
- accepted Aelari ear prototype work from commit `a4f81979…`.

This order authorizes **one bounded Aelari body-source refinement** before final consolidation.

The Aelari face and ear work are not being reopened.

---

# 1. AUTHOR DECISIONS — ACCEPTED FROM THE PARENT GATE

The following are accepted and must be preserved:

## 1.1 Configuration-2 central route
`AELF190` is accepted as the correct **configuration-2 construction route**:
- ~190.00 cm;
- deterministic;
- same Aelari biological design logic as AEL1;
- no configuration-specific anatomy.

Its final geometry remains provisional only because the shared Aelari source design is being corrected below.

## 1.2 MPFB family propagation
Accepted:
- both Aelari body-family realizations use active v005 unchanged;
- both are 69 / 69 D1+D3+D4+D5+D6;
- integrity, density, face-readiness, contact and deformation gates pass.

## 1.3 Hidden-ear facial identity
Accepted:
- Aelari hidden-ear face PASS;
- 7 / 7 facial systems materially express the Aelari design;
- no craniofacial source-authoring pass is required.

**Do not alter the accepted Aelari craniofacial target set.**

## 1.4 Ear branch
Accepted:
- reuse of frozen Fenn ear-topology v002 is approved as an **engineering topology reuse only**;
- all Aelari vertex geometry is Aelari-specific;
- AE-E1/E2/E3 share one topology;
- **AE-E2 is selected as the central Aelari ear direction**.

**Do not alter AE-E2 geometry, ear topology, root architecture, or ear parameterization in this order.**

---

# 2. THE TWO BODY-SOURCE ISSUES TO FIX

The parent gate found two inherited AEL1 source ties.

They are not technical propagation failures.  
They are source-anatomy issues in the previously accepted W1m central body.

## 2.1 Thoracic vertical contribution tie

Current result at ~190 cm:

- Aelari thoracic/ribcage vertical interval ≈ Fenn;
- Aelari total torso/waist/neck/cranium vertical continuity still passes overall;
- however, the Elf Comparative Review explicitly gives Aelari the **greatest average vertical torso/ribcage/waist continuity** of the elves.

The current source therefore under-expresses the **ribcage/thoracic** part of that identity.

### Required correction
Increase Aelari **thoracic/ribcage vertical contribution** enough that, at matched stature:

> Aelari thoracic vertical > frozen Fenn

on both c1 and c2.

Do this without simply adding total height.

Preserve:
- overall stature;
- current Aelari torso share within a narrow tolerance;
- current neck identity;
- current waist-transition identity;
- current shallow thoracic depth;
- current moderate breadth;
- pelvis relationships.

The correction should redistribute the already-approved vertical architecture rather than turn Aelari into an exaggerated long-chest race.

---

## 2.2 Thigh / lower-leg distribution tie

Current AEL1 carries:
- thigh Y bone scale ~0.9875;
- calf Y bone scale ~1.0523.

This leaves config-1 shin/leg weighting effectively tied with Fenn.

Aelari canon requires:

> leg elongation distributed more evenly across thigh and lower leg than Fenn.

### Required correction
Rebalance the Aelari leg architecture so that:

- total Aelari leg share stays essentially unchanged;
- total stature stays unchanged;
- total Aelari-vs-human long-leg identity stays unchanged;
- **thigh/lower-leg distribution becomes measurably more even than frozen Fenn**;
- neither segment becomes extreme.

Do not solve this by making the leg shorter.

Do not alter hip-joint height or pelvic architecture merely to change the segment ratio.

---

# 3. SOURCE-SPACE AUTHORING RULE

The correction must be authored at the **Aelari source level** and then applied identically in biological logic to:

- AEL1 c1;
- AELF190 c2.

Preferred methods:

1. existing MPFB torso/ribcage targets and existing limb/bone-scale controls;
2. deterministic bounded source-space deformation only if existing controls cannot express the correction cleanly.

No production-mesh-only sculpt.

No family topology change.

No per-configuration race anatomy.

---

# 4. BOUNDED PROBE / SOLVE PHASE

Before committing the corrected source, probe only the controls relevant to these two issues.

## Thoracic probe set
Audit relevant existing controls such as:
- torso / ribcage vertical length;
- nape-to-waist;
- waist/lumbar length;
- spine segment scales;
- ribcage placement.

The objective is to find the **smallest coherent correction** that makes thoracic vertical > Fenn without inflating total torso share unnecessarily.

## Leg probe set
Audit:
- upper-leg length control;
- lower-leg length control;
- thigh Y scale;
- calf Y scale.

The objective is to move the segment ratio toward even Aelari elongation while keeping:
- total leg share stable;
- hip-joint height stable;
- knee position plausible;
- foot/ankle relationships stable.

Document the response matrix.

---

# 5. CHANGE BUDGET

This is a surgical correction.

Do not redesign the Aelari body.

Preferred normalized changes:
- small enough that the existing full-body silhouette remains recognizably the same central Aelari;
- large enough to make both canon directions unambiguous.

Avoid:
- >1% change to total stature;
- >0.5% unintended change to unrelated body-share metrics;
- any visible new exaggeration.

These are review constraints, not new biological canon.

---

# 6. LOCKED REGIONS / SYSTEMS

Do not intentionally change:

- cranium;
- face;
- orbit/eyes;
- jaw;
- neck length;
- shoulder width;
- clavicle length;
- arm proportions;
- hand proportions;
- foot proportions;
- pelvis breadth;
- pelvis vertical architecture;
- hip-joint placement;
- joint gracility;
- body composition;
- AE-E2 ear geometry/topology.

A small coupled torso-surface response to thoracic-length correction is allowed and must be reported.

---

# 7. REVISED SOURCE NAMING

Create versioned corrected sources rather than overwriting ancestry.

Suggested naming:

- `AEL1-R1` or `AEL1-BR1`;
- `AELF190-R1` or matching project convention.

Retain:
- original AEL1;
- original AELF190 candidate;
- full provenance.

The corrected c1/c2 pair becomes the candidate central Aelari body architecture pending author acceptance.

---

# 8. REQUIRED BODY METRICS AFTER CORRECTION

At matched ~190 cm, prove for both c1 and c2:

## Versus Fenn
- central vertical share > Fenn;
- extremity share < Fenn;
- torso share > Fenn;
- neck share > Fenn;
- waist interval / torso > Fenn;
- cranial vertical share > Fenn;
- **thoracic vertical > Fenn — NEW required correction**;
- **leg segment distribution more even than Fenn — NEW required correction**;
- Aelari remains long-legged overall;
- Fenn remains more extremity-emphasized.

## Versus Marchfolk / Sagekin
- Aelari remains non-human;
- leg share > human;
- arm share > human;
- hands/feet retain elven proportions;
- shallow thoracic depth remains;
- gracile joints remain.

---

# 9. PELVIS REGRESSION

Re-run the accepted Aelari pelvis rules.

Must remain:
- hip-joint height / stature > MF;
- bitrochanteric / crest not lower than MF;
- pelvic vertical / crest > MF and > Fenn;
- waist interval / torso > Fenn and >= MF;
- no breadth shortcut;
- no configuration-specific pelvic change.

Any pelvis regression is a FAIL.

---

# 10. HIDDEN-EAR BODY REGRESSION — HARD

Re-run the equal-height hidden-ear comparison:

- corrected Aelari c1 vs frozen Fenn;
- corrected Aelari c2 vs frozen Fenn;
- corrected Aelari vs Marchfolk/Sagekin.

Required:
- Aelari still reads vertically continuous;
- Fenn still reads compact-centered / extremity-emphasized;
- the corrected thorax should strengthen, not replace, the existing signal;
- the leg balance should improve without erasing the overall Aelari/Fenn family resemblance.

No exaggeration for instant silhouette classification.

---

# 11. HIDDEN-EAR FACE REGRESSION — HARD

Re-run the accepted hidden-ear face test.

Required:
- 7 / 7 Aelari facial systems remain materially expressed;
- the corrected body source does not alter accepted craniofacial geometry;
- face metrics must remain unchanged except for any mathematically unavoidable whole-body frame effect, which must be zero or negligible.

If face geometry changes materially, reject the correction.

---

# 12. FAMILY PROPAGATION REGRESSION

Propagate corrected c1/c2 sources onto frozen MPFB v005.

Required:
- exact v005 topology;
- V = M @ hm08;
- 100% quads;
- integrity pass;
- 69 / 69 D1–D6 on both;
- no new contact defect;
- density pass;
- face readiness unchanged;
- Standard v1 deformation no new topology-class failure.

No non-ear topology branch.

---

# 13. EAR REGRESSION

Reapply the already-selected AE-E2 branch to the corrected c1/c2 heads.

Do **not** change ear parameters.

Verify:
- root attachment remains clean;
- same Aelari ear topology;
- same AE-E2 geometry logic;
- T-4 remains within the accepted prototype quality class;
- aspect <= 10;
- no self-intersections;
- no seam / float / burial;
- head/neck readiness remains clean.

If head geometry at the root changes unintentionally, report it; do not silently refit the ear beyond the existing root-frame system.

---

# 14. VISUAL PACKAGE

Provide actual images.

Required:

1. original AEL1 vs corrected c1 front/profile/3-4;
2. original AELF190 vs corrected c2;
3. corrected Aelari vs frozen Fenn equal-height, ears hidden;
4. torso/ribcage close comparison:
   - Aelari before;
   - Aelari after;
   - Fenn;
5. leg-segment comparison:
   - thigh;
   - knee;
   - lower leg;
   - Aelari before/after vs Fenn;
6. pelvis regression;
7. hidden-ear face before/after;
8. full-body overlay before/after;
9. validator/margins;
10. deformation;
11. corrected c1/c2 with selected AE-E2 ear;
12. Fenn E2 vs corrected Aelari AE-E2.

Use identical cameras and true scale.

---

# 15. ACCEPTANCE LOGIC

Return exactly one:

## AELARI BODY SOURCE CORRECTION PASS — READY FOR FINAL CONSOLIDATION
Use if:
- thoracic vertical > Fenn on c1/c2;
- leg distribution is measurably more even than Fenn on c1/c2;
- all existing Aelari identity gates remain green;
- no face/ear/topology regression.

## AELARI BODY SOURCE CORRECTION PASS WITH ONE RESIDUAL
Use only if one canon direction improves materially but lands within method-resolution tie territory and further correction would visibly overstate the race.

## AELARI BODY SOURCE CORRECTION NEEDS LOCAL REVISION
Use if one of the two targeted issues remains unresolved.

## FAIL
Use only for a blocking regression.

Do not freeze Aelari.

---

# 16. REQUIRED RETURN

Commit:

1. `reviews/claude-rac-rp3-aelari-body-source-correction-gate.md`;
2. corrected c1/c2 source definitions/build records;
3. response/probe matrix;
4. corrected R-6 sources;
5. source regeneration proof;
6. matched-stature Aelari/Fenn/human metrics;
7. pelvis regression;
8. corrected family realizations;
9. D1–D6 validator outputs;
10. anatomy/density/contact/deformation audits;
11. hidden-ear body + face regression;
12. selected AE-E2 ear regression;
13. visual package;
14. immutable hashes;
15. narrow manifest/STATUS candidate update;
16. session handoff.

Explicitly answer:
- What exact source controls changed?
- Did thoracic vertical now exceed Fenn on c1 and c2?
- Did thigh/lower-leg distribution become more even than Fenn on c1 and c2?
- Did total leg share remain essentially unchanged?
- Did torso share remain essentially unchanged?
- Did pelvis architecture remain valid?
- Did hidden-ear body identity improve without exaggeration?
- Did hidden-ear facial identity remain unchanged?
- Did both family realizations remain 69/69?
- Did AE-E2 ear integration remain clean?
- Is Aelari ready for final consolidation?

---

# 17. STOP RULES

After committing the correction gate:

**STOP FOR CHATGPT REVIEW.**

Do not:
- freeze Aelari;
- redesign the face;
- redesign AE-E2;
- start Vael;
- start Halvren;
- alter frozen Fenn;
- alter active MPFB Family Base v005;
- declare universal elf anatomy/topology;
- implement creator morphs;
- finalize rigging;
- finalize UV/materials;
- generate LODs;
- integrate UE5.

---

## FINAL AUTHOR RULING

- AELF190 construction route is accepted.
- Aelari hidden-ear face is accepted.
- AE-E2 is selected as the central Aelari ear.
- Fenn v002 ear-topology reuse is accepted as engineering reuse only.
- Do not freeze Aelari with the two inherited AEL1 body ties.
- Correct only:
  1. thoracic/ribcage vertical contribution;
  2. thigh/lower-leg distribution.
- Preserve the already-good Aelari face, pelvis, overall silhouette and AE-E2 ear.
- If both corrections pass without regression, the next step is final Aelari consolidation/freeze.
