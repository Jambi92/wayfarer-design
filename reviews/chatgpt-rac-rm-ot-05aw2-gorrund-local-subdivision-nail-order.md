# RAC RM-OT-05AW2 — local high-resolution feline toenail rebuild

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05AW1.
**Date:** 2026-10-18.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05aw1-gorrund-toenail-rework-gate.md` (bcb8779).
**Supersedes:** 05AW and 05AW1 nail-shaping attempts as final candidates.

## 1. Ruling

05AW1 established that the cracked/split source plates can be removed, but the remaining toe-tip mesh is too coarse to hold a defined feline nail outline.

Claude is now authorized to add **strictly local resolution inside the nail supports only**.

Use two local subdivision cuts, then rebuild the nail surfaces and shape them as clean naturalistic feline nails.

This is the preferred route over:
- accepting nail-less toes;
- keeping bump-like Stage B;
- deferring the species-defining nail morphology to a later stage.

## 2. Lineage and source

Authoritative accepted parent remains:

`GO-05AV_feet_final.blend`
SHA-256:
`45a04787c4760e95b9a9bef52837a516788670f1f1bade92c380ffcea74ab9a6`

The allowed operational topology-prep checkpoint is:

`GO-05AW1_T.blend`
SHA-256:
`63aa8e74ad77390a1146900b5ebbb49576562ee98bf243b047c90d70cae37f1b`

This checkpoint contains only the AW1 local toe-region topology preparation:
- merge exact duplicate-position seam copies;
- dissolve the specified valence-3 nail-support vertices.

Before use, independently revalidate GO-05AW1_T against 05AV.

If revalidation finds an unresolved local orientation defect, repair only that defect before subdivision.

Do not use GO-05AW1_A or GO-05AW1_B as the advancement source.

## 3. Revalidation gate for GO-05AW1_T

Required before subdivision:

- 0 self-intersections;
- 0 opened seams;
- 0 degenerates;
- 1 welded component;
- 0 boundary;
- 0 non-manifold;
- genus unchanged;
- no visible change outside toe/nail support;
- foot length/width/heel stance unchanged within diagnostic tolerance;
- body above feet unchanged.

If a few source crack-wall faces have local reversed orientation, classify them against the outward surface reference and repair only true orientation errors.

Freeze validated prep as:

`GO-05AW2_base.blend`

## 4. Local subdivision authority

Subdivide only the union of the eight visible nail supports and the minimum immediate nail-bed transition.

Authorized:
- **2 subdivision cuts**;
- local only;
- no smoothing during the subdivision operator unless explicitly measured and proven position-neutral outside the support;
- no toe-wide or foot-wide subdivision.

Expected scale from 05AW1 simulation:
- about 8,850 support vertices before subdivision;
- about +45,244 vertices across both feet;
- local effective spacing roughly 0.4 mm.

### Hard protection
No topology change outside:
- nail plate support;
- immediate nail-bed transition.

No changes to:
- toe base;
- toe spacing;
- toe length;
- foot dimensions;
- heel;
- ankle;
- lower leg.

### Subdivision gate
After subdivision:
- 0 SI;
- 0 opened seams;
- 0 degenerates;
- 1 / 0 / 0 welded topology;
- genus unchanged;
- no movement outside support;
- no visible toe silhouette change;
- foot dimensions unchanged.

Freeze:

`GO-05AW2_subdiv_base.blend`

## 5. Stage A — high-resolution nail-surface restoration

On the subdivided nail supports:

Rebuild each visible nail into one continuous clean keratin surface.

Required:
- remove the inherited split/crack;
- remove the chipped rim;
- remove recessed broken-plate appearance;
- smooth the nail-bed transition;
- retain a distinct nail boundary rather than erasing the nail completely.

Unlike AW1-A, the higher-resolution Stage A should preserve enough controlled relief to define:
- proximal nail root/cuticle;
- side walls;
- distal free edge.

### Preferred UI tools
- Smooth / Surface Smooth;
- local Fill / Clay / Inflate where needed;
- local Flatten only for a true surface break;
- masked Grab for boundary placement.

Do not over-smooth the entire nail into the toe pad.

### Stage A PASS
Every nail must have:
- continuous surface;
- visible clean outline;
- no crack/split;
- no chipped edge;
- no recessed plate;
- no technical defects.

Save:

`GO-05AW2_A.blend`

## 6. Stage B — feline morphology

From a passing Stage A:

Shape each nail as a restrained large-feline nail in neutral presentation.

Required anatomy:
- clean proximal root;
- distinct but integrated side walls;
- tapered distal end;
- smooth free edge;
- modest projection beyond the soft toe;
- mild downward curvature;
- continuous convex keratin surface.

The nail must read as a separate anatomical structure, not:
- a bump;
- ridge;
- groove;
- crack;
- human flat nail;
- exaggerated fantasy form.

### Big toe
May remain broader and heavier than the lesser toes while sharing the same species language.

### Lesser toes
Should be narrower and more tapered.

## 7. Local topology/shaping authority

Within the subdivided nail supports only, Claude may use:
- local edge slide;
- local edge rotation;
- tiny local dissolve/retriangulate;
- tiny local extrude/inset if needed to establish a readable free edge;
- local sculpt;
- local masked transforms.

This is **not** permission for broad toe retopology.

Do not:
- remesh the foot;
- use Dyntopo;
- use voxel remesh;
- alter toe count or toe silhouette.

## 8. Autonomous checkpoint budget

Claude may use up to **4 deliberate checkpoints**:

- AW2-S: subdivision/base;
- AW2-A: surface restoration;
- AW2-B: feline morphology;
- AW2-C: one final refinement/symmetry cleanup if needed.

Do not stop at the first technically clean result if the nails still read as bumps, grooves, cracked plates, or human toenails.

Self-review close renders after every checkpoint.

## 9. Dimensional limits

Versus accepted 05AV:

- foot-length change <= **3 mm** per foot;
- footprint-width change <= **1 mm**;
- heel-lift change <= **0.1 cm**;
- ankle-centre drift <= **0.2 mm**;
- no nail/ground intersection;
- no nail/adjacent-toe intersection.

Everything outside the nail-support union must remain 0.000 mm except the immediate nail-bed transition explicitly included in support.

## 10. Technical gate

Final candidate requires:

- 0 opened seams;
- 0 self-intersections;
- 0 flipped faces;
- 0 degenerates;
- 1 welded component;
- 0 boundary;
- 0 non-manifold;
- genus unchanged;
- no new toe fusion/contact;
- no ground intersection;
- no change outside allowed nail support;
- accepted foot/heel/ankle metrics preserved.

Known hand/axilla downstream topology debt remains out of scope.

## 11. Visual gate

PASS only if all are true:

- nail forms are visibly present;
- crack/split/chipped read is gone;
- nail surfaces are smooth and continuous;
- nail outline is readable;
- distal taper is clearly feline;
- free edge is clean;
- mild projection/curve is natural;
- no bump/ridge/groove read;
- no human-flat-nail read;
- no exaggerated fantasy appearance;
- left/right species language is coherent.

## 12. Output

If PASS, freeze:

`GO-05AW2_nails_final.blend`
`GO-05AW2_nails_final.glb`

Record exact hashes.

## 13. Evidence

Return:

`reviews/claude-rac-rm-ot-05aw2-gorrund-local-subdivision-nail-gate.md`

Evidence:

`reviews/rac-rmot05aw2-evidence/`

Include:
- revalidation of GO-05AW1_T;
- exact subdivision region and counts;
- subdivision gate;
- Stage A closeups;
- Stage B closeups;
- any local topology-edit log;
- per-nail front/top/profile/3-4;
- 05AV vs rejected 05AW vs AW1-A/B vs AW2 comparison;
- technical gate JSON;
- protected-region displacement report;
- foot/heel measurements;
- whole-body confirmation.

## 14. Decision

### PASS

Return:

**05AW2 HIGH-RES TOENAIL REBUILD PASS / READY FOR FINAL GORRUND CLOSURE REVIEW**

Then STOP 05AW2.

### FAIL

Return:

**05AW2 HIGH-RES TOENAIL REBUILD FAILED / AUTHOR REVIEW REQUIRED**

Do not run final closure.

## 15. State

- Gorrund BODY COMPOSITION: AUTHOR ACCEPTED / FROZEN
- Head share: AUTHOR APPROVED / FROZEN
- Tail root: AUTHOR APPROVED / FROZEN
- Foot size + heel stance: AUTHOR APPROVED / FROZEN
- Toenail morphology: IN HIGH-RES REBUILD
- RM-OT-05: OPEN
- Stage C Gorrund blocker: BLOCKED
- Grask E3: FROZEN
- connectivity cleanup: CARRIED TO RETOPOLOGY / RIG PREP
