# RAC RM-OT-05AW3 — final Gorrund feline nail projection / side-wall finish

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05AW2.
**Date:** 2026-10-18.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05aw2-gorrund-local-subdivision-nail-gate.md` (b050768).
**Supersedes as final candidate:** 05AW2 visual candidate only.

## 1. Ruling

05AW2 is technically clean and solves the cracked / chipped / split nail problem.

Its remaining visual issues are narrow and well-defined:

1. the nails do not visibly project beyond the toe enough in profile;
2. there is essentially no downward feline curvature;
3. the side walls can read as carved grooves / inlaid shields rather than a nail sitting slightly proud of the toe;
4. minor Stage-A residue remains on a few toes.

Do not rebuild the nails again.

Perform one final local finish pass on the clean 05AW2 candidate.

## 2. Source

Start only from:

`GO-05AW2_nails_final.blend`
SHA-256:
`75734a39b922f656ecc767b65c0263fa85cfde0e2e35600831b4f9830b1b9206`

Review GLB:
`GO-05AW2_nails_final.glb`
SHA-256:
`2c7c560cf2f7d84f191309806cdbc17b5e8ea0431f9f3264a3cbc399172d1a09`

The 05AW2 technical state is the advancement baseline.

## 3. Frozen anatomy

Do not alter:
- toe count;
- toe spacing;
- toe length;
- toe base silhouette;
- foot length/width beyond the limits below;
- heel stance;
- plantar contact;
- ankle;
- lower leg;
- body;
- head;
- tail.

Only the existing high-resolution nail plates and their immediate nail-bed transition may move.

## 4. Visual target

Final nails should read as **natural large-feline nail forms in a relaxed standing state**.

Required:
- clearly visible nail plate;
- sits slightly proud of the toe rather than looking engraved into it;
- clean tapered free edge;
- modest distal projection;
- subtle downward curve at the distal end;
- smooth continuous surface;
- no crack / chip / split;
- no carved-outline-groove appearance;
- no human-flat-nail appearance;
- no exaggerated fantasy talon.

## 5. Stage A — side-wall relief correction

First correct the inlaid/groove read.

Target:
- preserve the current plate outline;
- reduce the depth contrast of the surrounding side groove;
- create a slight raised side-wall relationship between nail and toe.

Allowed UI operations:
- very restrained Inflate / Clay / Fill on the nail side wall;
- very restrained Smooth / Surface Smooth on the adjacent groove transition;
- local Grab only if needed to restore a convex transition.

Do not erase the nail boundary.

### Stage A gate
Pass only if:
- nail still has a clear outline;
- side boundary reads as nail-to-skin transition, not an incised trench;
- no new ridge, dent or plateau;
- 0 technical defects.

## 6. Stage B — distal projection and curl

From a passing Stage A:

Move only the distal approximately **25–35%** of each nail.

Target envelope:
- distal forward projection: **1.5–2.5 mm** relative to 05AW2;
- distal downward drop / curl: approximately **0.5–1.2 mm**;
- smooth taper through the final third of the plate;
- root and proximal two-thirds remain essentially fixed.

The big toe may use the upper end of the projection envelope.
Lesser toes should generally use the lower/middle end.

Preferred UI operations:
- masked Grab / Elastic Deform;
- local Edit Mode proportional translation/rotation;
- tiny Smooth afterward for continuity.

Do not use global Inflate to create the projection.

## 7. Profile-read requirement

The final nail must be visibly present in the lateral/medial profile renders.

Required:
- free edge visibly clears the soft toe-tip silhouette;
- curve is readable without becoming hooked;
- nail does not point straight upward;
- nail does not intersect the floor.

If a nail disappears in profile, the projection/curl gate fails.

## 8. Cleanup authority

One small cleanup checkpoint is authorized after Stage B.

Allowed:
- remove the lower L1 shelf line;
- remove isolated specks/creases on L4, R2, R3;
- left/right symmetry adjustment;
- tiny free-edge smooth.

No second redesign cycle.

## 9. Dimensional limits versus accepted 05AV

Hard limits:
- total foot length change from 05AV <= **3.5 mm** per foot;
- footprint width change <= **1.0 mm**;
- heel-lift change <= **0.1 cm**;
- ankle-centre drift <= **0.2 mm**;
- no nail/ground intersection;
- no nail/adjacent-toe intersection.

Everything outside nail + immediate nail-bed support remains 0.000 mm.

## 10. Technical gate

Required:
- 0 opened seams;
- 0 self-intersections;
- 0 folded/flipped faces against local surface;
- 0 degenerates;
- 1 welded component;
- 0 boundary;
- 0 non-manifold;
- genus unchanged;
- no new toe fusion/contact;
- no ground intersection;
- protected anatomy unchanged.

Preserve the 05AW2 local-subdivision topology unless one tiny local edge rotation/dissolve is required to eliminate a new fold.

No remesh / Dyntopo / voxel remesh.

## 11. Visual gate

PASS only if:
- crack/chip/split read remains gone;
- nail surfaces remain smooth;
- side-wall groove/inlay read is materially reduced;
- nail sits slightly proud of toe;
- profile projection is visible;
- mild downward curve is visible;
- taper reads feline;
- no exaggerated hook/talon;
- both feet share coherent species language.

The final target is:
**05AW2 front-view clarity + actual feline projection/curvature in profile.**

## 12. Checkpoint budget

Authorize up to 3 checkpoints:
- AW3-A side-wall transition;
- AW3-B projection/curl;
- AW3-C cleanup/symmetry.

If AW3-B is visually credible and technically clean, do not overwork it.

## 13. Output

If PASS, freeze:

`GO-05AW3_nails_final.blend`
`GO-05AW3_nails_final.glb`

Record exact hashes.

## 14. Evidence

Return:

`reviews/claude-rac-rm-ot-05aw3-gorrund-final-nail-finish-gate.md`

Evidence:

`reviews/rac-rmot05aw3-evidence/`

Include:
- AW2 vs AW3 front/top/3-4/profile;
- profile projection measurements per nail;
- side-wall transition closeups;
- full technical gate;
- protected displacement;
- foot/heel metrics;
- whole-body confirmation.

## 15. Decision

### PASS

Return:

**05AW3 FINAL FELINE NAIL FINISH PASS / READY FOR FINAL GORRUND CLOSURE REVIEW**

Then STOP 05AW3.

### FAIL

Return:

**05AW3 FINAL NAIL FINISH FAILED / AUTHOR REVIEW REQUIRED**

Do not run closure.

## 16. State

- Gorrund BODY COMPOSITION: AUTHOR ACCEPTED / FROZEN
- Head share: AUTHOR APPROVED / FROZEN
- Tail root: AUTHOR APPROVED / FROZEN
- Foot size + heel stance: AUTHOR APPROVED / FROZEN
- Toenail morphology: FINAL LOCAL FINISH IN PROGRESS
- RM-OT-05: OPEN
- Stage C Gorrund blocker: BLOCKED
- Grask E3: FROZEN
- connectivity cleanup: CARRIED TO RETOPOLOGY / RIG PREP
