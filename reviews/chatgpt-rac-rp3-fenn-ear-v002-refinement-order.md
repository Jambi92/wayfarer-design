# RAC RP3 — Fenn E2 ear-branch topology v002 refinement + final-consolidation candidate order

**Date:** 2026-10-27  
**Authority:** Tyler / ChatGPT review of Claude return `59d233177ec3911663d5c1bc68d39d1496af0b93`.  
**Parent gate:** `reviews/claude-rac-rp3-fenn-ear-branch-gate.md`.  
**Program references:**  
- `specs/fenn/FENN_V1.md`;  
- `specs/RAC_PRODUCTION_MESH_CONTRACT.md`;  
- `specs/RAC_MPFB_FAMILY_PROPAGATION_STANDARD_v1.md`;  
- accepted Fenn CF2 craniofacial sources;  
- Fenn ear branch v001 evidence in `reviews/rac-rp3-evidence/fenn_ear_branch_v001/`.

This order formally selects **E2** as the central Fenn ear geometry direction and authorizes exactly one bounded **ear-topology v002 quality refinement** before final Fenn consolidation/freeze.

No new aesthetic-selection cycle is authorized.

---

# 1. AUTHOR DECISION — E2 SELECTED

Select **E2** as the canonical central Fenn ear geometry direction.

Preserve the E2 visual/anatomical target:

### Configuration 1 reference
Approximate measured state:
- lobe→tip chord ~8.17 cm;
- auricle height ~7.83 cm;
- max width ~3.05 cm;
- auricle-body angle ~52.1°;
- lateral extent ~2.63 cm;
- upper-extension axis ~32.3°;
- sweep ~0.72 cm;
- median thickness ~0.30 cm.

### Configuration 2
Same normalized construction / same topology / same parameterization, head-scaled through the accepted root-frame system.

E1 and E3 remain:
- evidence of valid directional variation;
- not selected central references;
- not creator extrema;
- not to be carried forward into another selection round.

---

# 2. What is LOCKED

Do not change the selected Fenn identity.

Locked:

- accepted Fenn body architecture;
- accepted FNF181 c2 body reference;
- accepted E-A2 pelvis tie;
- accepted CF2 craniofacial direction;
- hidden-ear body PASS;
- hidden-ear facial PASS;
- CF2 source topology;
- active MPFB body topology outside the Fenn ear branch;
- 52-vertex root loop;
- branch root location;
- E2 central:
  - length;
  - projection;
  - tilt;
  - sweep;
  - general width;
  - lobe scale;
  - thickness;
  - overall silhouette;
- required ear anatomy:
  - helix;
  - antihelix;
  - superior/inferior crura;
  - triangular fossa;
  - cymba;
  - cavum;
  - crus of helix;
  - tragus;
  - antitragus;
  - intertragic notch;
  - lobe;
  - upper extension;
  - natural taper.

Do not make the ear smaller, less projected, more human, or more exaggerated while cleaning topology.

---

# 3. v001 problems to fix

The v001 ear branch is accepted in concept and anatomy but not yet freeze-quality because of concentrated T-4 cell distortion.

Current E2 branch:
- integrity PASS;
- density PASS;
- no branch self-intersections;
- aspect max ~6;
- static deformation PASS;
- but T-4 angle violations ~15.8–16.3% versus ~3.4% in the replaced family ear zone.

The problem is concentrated in four known local structures.

Only these structures may be modified.

---

# 4. Refinement target A — upper-extension / tip block

This is the highest priority.

Current issue:
- rhombic / kite-shaped quads shear as the ear tapers toward the tip;
- angle violations increase strongly from E1→E3;
- this region drives the majority of E2's avoidable T-4 cost.

Required v002 approach:

- replace the current kite-style upper-extension flow with rows that follow the ear taper;
- orient edge flow along:
  - the helix/upper-extension direction;
  - the cross-ear narrowing direction;
- let loop spacing compress gradually rather than abruptly;
- distribute the taper over more rows if needed;
- maintain a clean continuous helix path into the tip;
- preserve the antihelix/scapha relationship;
- keep the point broad enough to avoid knife geometry.

Allowed:
- modest local face-count increase;
- adding a small number of rows in the upper extension;
- local pole relocation outside active crease/anatomy structures;
- reparameterizing the tip block.

Not allowed:
- changing the E2 silhouette materially;
- extending the tip;
- sharpening the tip aesthetically;
- changing projection/tilt/sweep.

---

# 5. Refinement target B — cuff count transitions

Current issue:
- the ±2 ring-count transitions create concentrated shear;
- many cuff T-4 violations cluster around those transitions.

Required:

- spread count transitions over a wider axial span;
- avoid consecutive transition events;
- avoid concentrating multiple valence changes in one local cell cluster;
- preserve the 52-vertex root interface;
- preserve root valence 4;
- keep the junction-ring architecture coherent;
- no valence-2 vertices;
- minimize valence-6+ use.

Preferred:
- distribute each ±2 change through staged quad-compatible transitions;
- move poles away from the root and away from the highest-curvature attachment corners where possible.

Do not globally densify the cuff.

---

# 6. Refinement target C — attachment corners

Current issue:
- the bridge-to-cuff ends near line A contain the smallest angles (~5.6–7°).

Required:

- improve those corner cells;
- remove acute corner collapse;
- preserve tragus/concha/root anatomy;
- preserve root loop positions;
- preserve adjacent skull/temple geometry outside the permitted transition region.

Target:
- materially raise local minimum corner angle;
- no new aspect > 10;
- no new seam or root crease.

---

# 7. Refinement target D — lobe-cusp cuff knob

Remove the small cuff knob behind the lobe cusp identified in the v001 rear/root sheets.

Requirements:
- keep lobe volume;
- keep antitragus/intertragic relationship;
- preserve root attachment;
- no flattening of the lower ear into a generic oval;
- no visible crease or dent created in exchange.

This is a local surface/topology cleanup only.

---

# 8. Topology-sharing requirement

v002 must remain ONE shared Fenn ear topology for:

- configuration 1;
- configuration 2.

The selected production direction is now E2 only for consolidation, but also prove that the topology remains capable of the previously tested bounded creator-style probes.

Required:
- identical vertex count c1/c2;
- identical face list;
- identical branch map;
- identical cuff/root architecture;
- identical UV topology plan.

No config-specific topology.

---

# 9. Mapping / provenance

Create:

- v005 family base → Fenn ear branch v002 map;
- v001 ear branch → v002 map;
- updated root-frame geometry record.

Preserve:
- all non-branch active-family rows unchanged;
- root rows unchanged unless a transition-ring position adjustment is required and explicitly reported;
- CF2 face/head rows unchanged outside branch.

Every new/replaced vertex must have deterministic provenance.

---

# 10. T-4 acceptance goal

Do not chase theoretical perfection.

The goal is **material improvement to production quality**.

For E2 c1/c2, report:

- angle violations;
- aspect violations;
- union;
- max aspect;
- min angle;
- per-zone:
  - front sheet;
  - back sheet;
  - rim;
  - cuff;
  - transition;
  - upper extension.

### Required
- no aspect > 10;
- no new severe slivers;
- v002 T-4 angle violation count must be **materially lower** than v001 E2;
- upper-extension violations should drop substantially;
- attachment-corner minimum angle should improve;
- cuff violations should decrease.

### Preferred target
Aim for branch-wide angle violations **well below 10%** if achievable without anatomy or deformation regression.

This is a preferred target, not an automatic fail threshold.

If getting below 10% requires visible anatomy damage or excessive density, stop at the best clean result and document the tradeoff.

---

# 11. Integrity hard gates

v002 must maintain:

- 100% quads;
- one connected body mesh;
- 0 boundary edges;
- 0 non-manifold edges/vertices;
- 0 degenerate faces;
- outward normals;
- 0 new branch self-intersections;
- 0 new whole-mesh rest contact attributable to the branch;
- no seam at root;
- no floating/buried root;
- root valence 4 retained.

---

# 12. Density

Recompute ear density.

Requirements:
- mean edge/stature <= 0.25%;
- do not over-densify merely to solve angles;
- report v001→v002:
  - vertices;
  - quads;
  - mean edge/stature;
  - p95;
  - local rows added.

If extra upper-extension rows are added, justify them anatomically/topologically.

---

# 13. Root / transition regression

Re-run:

- root-loop dihedral;
- transition-ring displacement;
- cuff-to-skull deviation by ring;
- ear-to-head clearance;
- seam check.

Requirements:
- root integration no worse than v001;
- no new posterior-lip crease;
- c1 and c2 both clean;
- transition displacement remains bounded.

If a topology change requires moving a root vertex:
**reject that candidate** unless the move is absolutely necessary and separately authorized. Root positions are intended to stay fixed.

---

# 14. Static deformation-readiness regression

Re-run the same v001 diagnostics:

- neck flex 30;
- neck extension 30;
- head yaw ±45;
- head pitch ±20;
- head roll ±20.

Required:
- 0 new branch self-intersections;
- 0 flipped branch faces;
- 0 root inversions;
- root strain no worse than v001;
- neck/shoulder clearance preserved.

---

# 15. Shape-probe regression

Re-run the same bounded E2 topology-readiness probes:

- projection ±10°;
- tilt ±8°;
- sweep ±0.6;
- length ±10%;
- tip blunt/sharp.

The v002 topology must remain capable of these directions.

Required:
- no self-intersection;
- no broken root;
- no catastrophic T-4 spike;
- measure moves in intended direction.

If a probe fails because the topology was over-specialized to central E2, reject/refine.

---

# 16. CF2 / hidden-ear regression

Prove:

- CF2 c1/c2 source hashes unchanged;
- CF2 head/face outside branch unchanged;
- hidden-ear body identity still PASS;
- hidden-ear face identity still PASS;
- FENN-CF-1 rig carry-forward unchanged.

Do not alter CF2 to improve ear topology.

---

# 17. Visual acceptance package

Provide side-by-side **v001 E2 vs v002 E2** sheets for c1 and c2.

Required:

1. full head front;
2. profile;
3. 3/4 front;
4. 3/4 rear;
5. rear;
6. top;
7. wireframe;
8. upper-extension closeup;
9. cuff transitions closeup;
10. attachment corners;
11. lobe-cusp region;
12. T-4 heat before/after;
13. aspect heat before/after;
14. pole/valence before/after;
15. root integration before/after;
16. thickness/section;
17. deformation readiness;
18. shape probes;
19. c1 vs c2 final E2;
20. hidden-ear CF2 confirmation.

True scale and identical cameras.

---

# 18. Candidate budget

This is a bounded cleanup cycle.

At most:

- **R1** — primary v002 refinement;
- **R2** — one correction if R1 has a specific localized regression;
- **R3** — final bounded correction only if one small issue remains.

No broad redesign.

Do not restart ear anatomy from scratch.

---

# 19. Final recommendation logic

Return exactly one:

## FENN EAR v002 PASS — READY FOR FINAL CONSOLIDATION
Use if:
- E2 visual identity preserved;
- T-4 materially improved;
- integrity/density/root/deformation all pass;
- no topology-readiness regression.

### OR

## FENN EAR v002 PASS WITH DOCUMENTED T-4 RESIDUAL — AUTHOR DECISION
Use if remaining T-4 cells are unavoidable without harming anatomy or deformation.

### OR

## FENN EAR v002 NEEDS LOCAL REVISION
Use only if one bounded local defect remains.

### OR

## FAIL
Use only for a blocking regression.

Do not freeze Fenn in this order.

---

# 20. Final-consolidation preparation

If v002 passes, prepare the exact final consolidation package but do not execute freeze.

It should combine:

- accepted Fenn body:
  - FNL4 / FNF181 architecture;
- accepted CF2 craniofacial source:
  - FNL4-CF2;
  - FNF181-CF2;
- selected E2 ear geometry;
- refined v002 ear topology;
- final branch mapping;
- body-family topology elsewhere;
- validator D1+D3+D4+D5+D6;
- accepted rig carry-forward items.

Propose final production names and freeze records.

---

# 21. Required return

Commit:

1. `reviews/claude-rac-rp3-fenn-ear-v002-refinement-gate.md`;
2. v002 topology definition;
3. v005→v002 branch map;
4. v001→v002 map;
5. final E2 c1/c2 geometry;
6. integrity audit;
7. T-4/aspect audit;
8. density audit;
9. root integration audit;
10. static deformation regression;
11. shape-probe regression;
12. CF2/hidden-ear regression proof;
13. visual before/after sheets;
14. refinement provenance (R1/R2/R3);
15. final-consolidation preparation note;
16. immutable hashes;
17. narrow STATUS update;
18. session handoff.

The gate must explicitly answer:

- Is E2 preserved as the selected Fenn central ear?
- Did upper-extension T-4 improve?
- Did cuff-transition T-4 improve?
- Did attachment-corner quality improve?
- Was the lobe-cusp knob removed?
- What is the final branch-wide T-4 rate?
- Did any aspect >10 appear?
- Did density remain valid?
- Did root integration regress?
- Did static deformation-readiness regress?
- Did shape-probe readiness regress?
- Did CF2/hidden-ear identity remain unchanged?
- Is the ear branch ready for final Fenn consolidation?

---

# 22. Stop rules

After committing the v002 refinement gate:

**STOP FOR CHATGPT REVIEW.**

Do not:
- freeze Fenn;
- start Aelari;
- start Vael;
- start Halvren;
- declare universal elf-ear topology;
- modify active MPFB Family Base v005;
- implement final ear rigging;
- implement creator morphs;
- finalize UV/materials;
- generate LODs;
- integrate UE5.

---

## FINAL AUTHOR RULING

- E2 is selected as the central Fenn ear direction.
- v001 ear anatomy/branch architecture is accepted in concept.
- v001 is not freeze-quality due to concentrated T-4 angle distortion.
- Run one bounded v002 topology-quality refinement.
- Preserve E2 visual identity, CF2 head, root interface and shared c1/c2 construction.
- If v002 materially improves T-4 without regression, the next step is final Fenn consolidation/freeze.
