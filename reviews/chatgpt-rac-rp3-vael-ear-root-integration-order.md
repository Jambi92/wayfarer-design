# RAC RP3 — Vael VA-E2 root/concha integration revision order

**Date:** 2026-10-28  
**Authority:** Tyler / ChatGPT visual review after Claude Vael ear prototype return `ccdaffd030439f7ffa38371573110803cb1099c9`.  
**Parent gate:** `reviews/claude-rac-rp3-vael-ear-prototype-gate.md`.  
**Program references:**  
- `specs/vael/VAEL_V1.md`;  
- frozen Fenn RP3 ear branch;  
- frozen Aelari RP3 ear branch;  
- accepted Vael R1 + VD2 + VF2 body;  
- accepted Vael VC2 face;  
- current Vael VA-E2 prototype.

This order revises one problem only:

> The current Vael prototype reads visually like a conventional inner ear layered inside a larger pointed outer ear.

That nested / doubled-ear read is not acceptable for final production anatomy.

Do not reopen the Vael body, face, shoulder frame, pelvis, or broad VA-E2 silhouette.

---

# 1. AUTHOR RULING

## 1.1 VA-E2 remains the selected overall Vael ear direction

Keep as the target:

- broadest-base elf ear;
- intermediate lateral projection;
- more backward orientation than Fenn / Aelari;
- shorter / blunter taper;
- moderate relative length;
- non-bat-like silhouette;
- current three-elf family differentiation.

Do not restart VA-E1 / VA-E2 / VA-E3 selection.

VA-E1 and VA-E3 remain evidence only.

---

## 1.2 Final freeze is blocked

Current VA-E2 is **not freeze-ready**.

Reason:

> root / cuff / concha integration creates a visible “ear inside an ear” or “ear layered on another ear” read.

This is a visual-anatomical integration failure, not an overall silhouette failure.

---

# 2. Diagnosis to address

The current construction preserves enough of an inner human-like/cuff silhouette that it reads as a second ear nested inside the larger Vael outer leaf.

Most likely contributing regions:

- cuff perimeter;
- concha bowl boundary;
- tragus / antitragus placement;
- root-to-concha spacing;
- helix-to-cuff relationship;
- broad-base transition.

The current concha-clearance solution (~0.15 cm) solved contact and T-4 issues, but appears to have separated the internal ear anatomy from the outer auricle too strongly.

Do not assume that exact 0.15 cm spacing must survive.

---

# 3. Primary objective

The revised Vael ear must read as:

> **one continuous biological auricle**

not:

> a normal inner ear plus a second fantasy outer shell.

The skull root, concha, tragus complex, helix, antihelix, lobe and upper extension must visually belong to the same continuous volume.

---

# 4. What must remain locked

Do not change:

- Vael VF2 body;
- Vael VC2 face;
- accepted hidden-ear firewalls;
- pelvis ordering;
- shoulder carry-forward;
- current VA-E2 overall outer silhouette except local root/base integration;
- VA-E2 general:
  - length;
  - base breadth;
  - projection;
  - backward tilt;
  - sweep;
  - taper character;
- three-elf visible-ear ordering;
- 52-vertex v005 skull root interface unless a local derivative absolutely requires otherwise.

Fenn and Aelari frozen ears remain read-only references.

---

# 5. What may change

Authorize a **Vael-specific local cuff / concha / root derivative** if needed.

Allowed local changes:

- cuff topology;
- cuff geometry;
- concha floor depth / placement;
- tragus / antitragus integration;
- root-to-concha transition;
- helix root path;
- lobe/root blending;
- one bounded transition ring around the existing root;
- local face count;
- local pole layout.

The engineering topology may remain reused where it still works.

Do **not** preserve Fenn-v002 local cuff geometry merely because the connectivity is already proven.

If Vael’s broader base requires its own local derivative, build it.

---

# 6. Specific visual problems to eliminate

The revision must eliminate all of the following:

## 6.1 Second-ear silhouette
There must not be a smaller ear-shaped outline visible inside the larger ear.

## 6.2 Detached concha bowl
The concha should not look like a separate insert sitting on the skull.

## 6.3 Independent cuff rim
The cuff must not trace a second auricle perimeter.

## 6.4 Tragus as a pasted-on human ear remnant
The tragus / antitragus complex must emerge from the Vael ear root architecture.

## 6.5 Outer shell effect
The broad pointed portion must not look like a fantasy fin surrounding a normal ear.

---

# 7. Revised anatomical integration target

The revised VA-E2 must read as one continuous structure from:

1. skull attachment;
2. root;
3. concha floor;
4. tragus / antitragus;
5. antihelix;
6. helix root;
7. helix rim;
8. broad upper auricle;
9. tapered upper extension;
10. tip.

The upper extension should feel like a continuation of the auricle, not a second layer.

---

# 8. Concha / root strategy

Test at least three bounded root-integration solutions on the same selected VA-E2 outer silhouette.

## RI1 — reduced stand-off
- reduce concha/cuff clearance from the current value;
- keep current topology where possible;
- improve visual continuity.

## RI2 — blended cuff / concha
- redistribute cuff and concha rows so the root volume flows directly into the concha;
- remove the inner ear-shaped perimeter;
- likely preferred approach.

## RI3 — local Vael derivative
- bounded local topology derivative around cuff/concha/root;
- preserve 52-vertex skull root interface;
- use only if RI1/RI2 cannot eliminate the nested-ear read cleanly.

These are not new ear silhouettes.

They are root-integration alternatives for VA-E2 only.

---

# 9. Selection rule

Choose the **least invasive** solution that:

- removes the nested-ear read;
- preserves anatomy;
- preserves deformation readiness;
- preserves topology quality;
- preserves VA-E2 silhouette.

Do not choose by T-4 alone.

Visual biological coherence is the primary gate.

---

# 10. Anatomy requirements after revision

All required structures must still be identifiable:

- helix;
- antihelix;
- superior / inferior crura;
- triangular fossa;
- cymba;
- cavum;
- crus of helix;
- tragus;
- antitragus;
- intertragic notch;
- lobe;
- upper extension.

But they must no longer read like separate labeled pieces placed inside a larger shell.

---

# 11. Root / topology quality gates

Required:

- one connected body mesh;
- all quads;
- 0 boundary edges;
- 0 non-manifold edges;
- 0 degenerate faces;
- outward normals;
- 0 branch self-intersections;
- no root seam;
- no floating / buried root;
- aspect < 10;
- density < 0.25 % stature;
- root deformation readiness preserved.

Preferred:
- T-4 no worse than current VA-E2;
- cuff/root min angles not worse than current accepted class.

If a local Vael derivative slightly increases face count but produces a substantially better biological read, prefer the better anatomy.

---

# 12. Projection / stand-off rule during this pass

Do not yet optimize the global Fenn-vs-Vael projection metric unless necessary for root integration.

However, report:

- auricle-body angle;
- mean free-ear lateral stand-off;
- median free-ear lateral stand-off;
- tip stand-off.

Compare:
- frozen Fenn E2;
- revised Vael E2;
- frozen Aelari AE-E2.

The expected population ordering for **average lateral projection** remains:

> **Fenn > Vael > Aelari**

If the revised integration naturally restores that ordering, record it.

If not, report it for the next/final consolidation decision.

Do not distort the ear solely to chase tip stand-off.

---

# 13. Visual package — critical

Provide close visual sheets specifically designed to reveal the nested-ear problem.

Required for c1 and c2:

1. current VA-E2 vs RI1 vs RI2 vs RI3, 3/4 front;
2. close profile;
3. close 3/4 rear;
4. front;
5. rear;
6. root closeup;
7. concha closeup;
8. tragus / antitragus closeup;
9. wireframe;
10. section through root/concha;
11. section through helix/concha;
12. silhouette-only render;
13. neutral clay render without annotation;
14. current vs revised overlay;
15. revised Vael vs frozen Fenn vs frozen Aelari;
16. deformation readiness;
17. T-4/aspect;
18. projection/stand-off metric visualization.

No annotation-only sheet may substitute for neutral clay visual review.

---

# 14. Human-read test

Ask explicitly:

> If this were not pointed, would the root/concha still look like a coherent single ear?

And:

> Does the viewer perceive one auricle or two layered auricles?

The revised result must unambiguously read as **one**.

---

# 15. Shape-probe regression

Re-run VA-E2 probes on the selected root revision:

- projection ±10°;
- tilt ±8°;
- sweep ±0.6;
- length ±10%;
- tip blunt/sharp;
- base width ±8%.

Ensure the revised concha/root does not split visually under variation.

No “inner ear remains fixed while outer shell moves” behavior.

---

# 16. Deformation readiness

Re-run:

- neck flex / extension;
- yaw ±45;
- pitch ±20;
- roll ±20.

Require:

- 0 root inversions;
- 0 branch flips;
- 0 new branch contact;
- no concha collapse;
- no cuff separation.

---

# 17. Result logic

Return exactly one:

## VAEL EAR ROOT-INTEGRATION PASS — VA-E2 READY FOR FINAL CONSOLIDATION

Use if one continuous biological ear read is achieved.

## VAEL EAR ROOT-INTEGRATION PASS — AUTHOR SELECTION REQUIRED

Use if multiple RI options are technically clean but visually meaningfully different.

## VAEL EAR ROOT-INTEGRATION NEEDS LOCAL REVISION

Use if the doubled-ear read remains.

## FAIL

Use only for a true technical blocker.

Do not freeze Vael.

---

# 18. Final-consolidation preparation

If root integration passes, update the prepared final-consolidation plan to use:

- R1 + VD2 + VF2 body;
- VC2 face;
- selected revised VA-E2 ear;
- final local Vael cuff/concha topology version;
- shoulder rig carry-forward;
- projection verification;
- final freeze checklist.

Do not execute freeze in this order.

---

# 19. Required return

Commit:

1. `reviews/claude-rac-rp3-vael-ear-root-integration-gate.md`;
2. RI1/RI2/RI3 definitions;
3. selected revised VA-E2 c1/c2 geometry;
4. topology/map if locally revised;
5. anatomy audit;
6. root/concha audit;
7. integrity/T-4/aspect/density;
8. projection/stand-off metrics;
9. deformation readiness;
10. shape-probe regression;
11. visual package;
12. updated final-consolidation plan;
13. immutable hash proof;
14. narrow STATUS update;
15. session handoff.

The gate must explicitly answer:

- Does the revised ear read as one auricle rather than an ear layered on another ear?
- Which RI solution is recommended?
- Was a Vael-specific local cuff/concha topology derivative required?
- Is VA-E2’s overall silhouette preserved?
- Are all required ear anatomical systems still present?
- Did root integration improve visually?
- Did any new topology/deformation issue appear?
- What is the final average lateral projection ordering?
- Does the revised ear remain distinct from frozen Fenn and Aelari?
- Is Vael ready for final consolidation/freeze review?

---

# 20. Stop rules

After committing the gate:

**STOP FOR CHATGPT REVIEW.**

Do not:
- freeze Vael;
- start Halvren;
- modify VF2;
- modify VC2;
- modify frozen Fenn;
- modify frozen Aelari;
- invent low-light physiology;
- implement creator morphs;
- finalize ear rigging;
- finalize UV/materials;
- generate LODs;
- integrate UE5.

---

## FINAL AUTHOR RULING

- VA-E2 remains the selected Vael ear direction.
- Current VA-E2 root/concha integration is not accepted.
- Fix the “ear layered on another ear” read before freeze.
- Preserve the broad-base, backward, intermediate-projection Vael silhouette.
- Prefer one continuous biological auricle over forced reuse of Fenn local cuff geometry.
- Final Vael freeze remains blocked until this visual-anatomical issue is resolved.
