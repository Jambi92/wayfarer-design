# ChatGPT Order — RAC RP5 Saurin Targeted Revision Until Internal PASS

**Repository:** `Jambi92/wayfarer-design`  
**Branch:** `main`  
**Reviewed Claude gate:** `a6fc99250f1dc7156557c70217165cb689e40fba`  
**Parent order:** `reviews/chatgpt-rac-rp5-saurin-full-cage-refinement-closure-order.md`  
**Standing submission rule:** `reviews/chatgpt-claude-internal-audit-pass-before-submission-directive.md`  
**Scope:** close all remaining Saurin RP5 full-cage blockers and do not return until Claude's own full audit passes, unless a genuine author decision or external blocker is reached  
**Stop condition:** only submit when internal gate = PASS / READY FOR CHATGPT REVIEW, or a genuine AUTHOR DECISION / EXTERNAL BLOCKER exists. Do not submit another NEEDS REVISION gate.

---

# 1. Preserve approved architecture

Retain the current Saurin full-cage architecture.

Current accepted architecture:
- 107,532 V / 107,530 Q;
- 100% quads;
- one closed manifold;
- same c1/c2 face list and vertex order;
- canonical W2I6 source unchanged;
- accepted tail module unchanged;
- thigh art-pass CLOSED;
- layered surface strategy retained.

Do not restart the cage or use an automatic full-body remesh.

---

# 2. Internal iteration rule for this order

Claude must iterate internally:

**refine -> audit -> diagnose -> refine -> rerun**

until the full ordered gate passes.

Do not return to ChatGPT with:
- T-1 still failing;
- T-2 still failing;
- T-4 still failing;
- unresolved topology-class deformation;
- missing required creator/head diagnostics;
- missing required final boards;
- incomplete PD-2 ownership proof.

A NEEDS REVISION result remains internal unless the next correction requires a new author ruling.

---

# 3. Axillary vault — authored patch required

Current blocker:
- T-1 max ~5.1 mm;
- dominant cluster = axillary vault;
- prior row-height experiment cc5 failed.

Do not repeat cc5.

Create a true authored axillary-vault patch:

- explicit vault apex corner / local control point;
- dedicated support ring following the actual source pocket;
- local shoulder-hole integration;
- local source-driven sliding;
- preserve shoulder/arm semantic flow;
- preserve c1/c2 shared topology.

Targets:
- T-1 max <= 3.0 mm;
- no T-7 regression;
- no T-4 regression;
- no shoulder deformation-topology regression.

Audit both sides and both configurations.

---

# 4. Shoulder-neck slope

Current localized max ~3.6 mm.

Add/reposition a bounded support row at the actual source slope.

Do not alter:
- thorax width/depth canon;
- neck identity;
- shoulder breadth canon.

Target:
- local T-1 <= 3.0 mm;
- preferably <= 2.0 mm for margin.

---

# 5. Head T-2 closure

Current head max ~2.65 mm.

Implement the bounded corrections already diagnosed:

## Mouth / lip crease
- crease-snapped mouth-slit support row;
- preserve jaw/mouth semantics;
- preserve neutral expression.

## Nostril pits
- local nostril pit rings / support;
- no external human-style nose construction.

## Orbit / head quality
- redesign orbit fan layout;
- radius-matched ring phase;
- preserve accepted IOD and ridge architecture.

Target:
- head T-2 max <=1.5 mm;
- orbit/mouth T-4 clean enough for production target.

---

# 6. Hand / thumb / palm closure

Current hand max ~2.07 mm.
T-4 hotspots:
- palm 2:1 rows;
- thumb;
- finger webs.

Required:
- move/rephase palm 2:1 reduction one ring proximal if needed;
- add thumb-base support ring;
- deepen finger web topology to two coarse rows where required;
- remove aspect >4 in non-tip hand regions;
- preserve five digits, thumb opposition, claw form.

Target:
- hand T-2 max <=1.5 mm;
- palm/thumb/finger-web T-4 pass;
- fist / grasp / opposition topology-safe.

---

# 7. Foot / toe / forefoot closure

Current foot max ~1.92 mm.
T-4 hotspots:
- toe webs;
- forefoot 2:1 row;
- toe transitions.

Required:
- redesign forefoot 2:1 transition;
- deepen toe web topology;
- source-drive local web/pad sliding;
- preserve plantigrade sole and claw silhouette.

Target:
- foot T-2 max <=1.5 mm;
- no non-tip aspect >4 in forefoot/web regions;
- toe flex topology-safe.

---

# 8. Tail-root cranial body-side closure

Current tail-station max ~1.77–1.86 mm.

Accepted tail module remains unchanged.

Fix only:
- body-side P-row distribution;
- pelvis/sacral transition;
- perineal support;
- module-root cranial-adjacent quads.

Add an extra perineal row if needed.

Targets:
- tail-station T-2 max <=1.5 mm;
- root integration remains visually continuous;
- no tail metric regression.

---

# 9. T-4 must reach production-pass state

Current:
- ~641 non-tip quads aspect >4;
- ~2.7% angle outliers.

This is still a blocker.

Required internal loop:
1. cluster T-4 failures;
2. correct each named region;
3. rerun full T-4;
4. repeat until passable.

Priority regions:
- palm;
- thumb;
- toe web;
- orbit;
- shoulder;
- finger web;
- forefoot;
- head;
- finger;
- toe.

Use:
- 2:1 row redesign;
- local phase changes;
- ring redistribution;
- quad-centroid shape improvement;
- local edge sliding;
- web depth;
- fan redesign.

Hard stop rules:
- no collapsed edges;
- no pathological aspects;
- aspect <=4 outside explicit tip exceptions;
- no deformation-zone T-4 violation.

Only bounded, anatomically harmless angle residuals may remain, and they must be documented individually.

---

# 10. Deformation ownership — complete before submission

The prior gate did not complete the required proof.

Run all four steps for every high-attention pose:

1. current cage + baseline temporary weights;
2. dense working source + same scaffold;
3. cage + improved local diagnostic weights;
4. topology-only fold test on the relevant patch.

High-attention poses:
- neck flex / rotation;
- shoulder abd45 / abd90 / flex;
- elbow 90 / 130;
- hip flex;
- trunk twist;
- lower axial flex;
- tail-root lateral / vertical;
- tail twist.

Also run previously missing:
- fist;
- grasp;
- thumb opposition;
- toe flex / ext.

Required classification:
- TOPOLOGY;
- WEIGHTING / SCAFFOLD;
- SOURCE / PD-2;
- DETAIL / PD-1;
- MIXED.

No unresolved topology-class failure may remain at submission.

---

# 11. PD-2 creator-state ownership proof

Prior creator FAIL states:
- high fat;
- high muscle;
- high muscle + fat.

Run source-side fold/inversion counts for the same accepted creator states.

Compare:
- source/base;
- cage;
- diagnostic weighting route.

Determine whether the failures are:
- inherited PD-2 source/composition inversion;
- cage topology;
- mixed.

Do not shrink creator biology to eliminate PD-2.

If the cage adds a new topology failure, fix it before submission.

---

# 12. Complete missing creator/head support diagnostics

Run the still-missing accepted states:

- orbit spacing −8%;
- orbit spacing +3%;
- ridge lower safe state;
- ridge upper safe state;
- display-root low state;
- display-root high structural state.

For hand/foot:
- if no accepted creator control exists, document NOT RUN because no canonical driver exists;
- do not invent one.

All tested states must preserve shared topology.

---

# 13. Layered detail closure

The detail-layer prototype is promising but must be rerun after cage refinement.

Required:
- regenerate from canonical saved seeds;
- same field boundaries;
- deterministic result;
- report c1 and c2;
- report representative creator state if cleanly supported;
- isolate PD-1 from cage topology.

Targets:
- no cage-induced detail discontinuity;
- no new silhouette failure;
- no re-seeding.

---

# 14. Identity metrics — final rerun

After final cage refinement, rerun:

- stature;
- thorax breadth/depth;
- lower axial trunk;
- pelvic band;
- tail length / stature;
- tail root area;
- tail 25/50/75 section areas;
- tail RSI/coupling;
- carriage;
- forearm/arm;
- femur/leg;
- rostral projection;
- orbit spacing;
- plantigrade foot;
- claw presence;
- display-root integration;
- structural-ridge readability.

Do not infer unchanged metrics only from landmarks if a direct cage measurement is possible.

---

# 15. Final visual evidence — complete A–P

The previous closure package was incomplete.

Return final boards including:

A. thigh before/after  
B. full wire  
C. pole/valence  
D. head/rostrum  
E. neck/throat  
F. shoulders/arms  
G. hands/claws  
H. pelvis/sacrum/tail root  
I. legs/feet  
J. tail  
K. c1/c2 overlay  
L. deviation heat maps  
M. density  
N. layered detail  
O. worst deformation poses + ownership labels  
P. creator-support states

No WIP board labels in the final package.

---

# 16. Pilot production files only after internal PASS

Only after Claude's own audit passes every gate, create:

- `SA_M_REF_RP5_pilot_v001`
- `SA_F_REF_RP5_pilot_v001`

Status:
**PILOT / NOT FROZEN**

Include:
- .blend;
- sidecar;
- source/barycentric map;
- semantic map;
- landmarks;
- read-back verification.

If internal audit still fails, keep iterating and do not create final pilot deliverables yet.

---

# 17. Required internal PASS criteria

Claude's own final gate may say PASS only when:

## T-1
- median <=0.5 mm;
- p95 <=1.5 mm;
- max <=3.0 mm.

## T-2
Every identity zone:
- median <=0.3 mm;
- p95 <=0.8 mm;
- max <=1.5 mm.

## T-3
PASS.

## T-4
- no collapsed edges;
- no pathological aspect;
- aspect <=4 outside explicit tip exceptions;
- no unresolved deformation-critical angle/shape defect.

## T-5
PASS.

## T-6
PASS.

## T-7
PASS with tail included.

## Deformation
No unresolved topology-class failure.

## Creator support
No unclassified cage-specific blocker.

## Detail layer
No cage-induced field discontinuity.

## Evidence
All mandatory records and boards complete.

---

# 18. Submission rule

Do **not** submit another:

**SAURIN RP5 ... NEEDS REVISION**

if the remaining corrections are already authorized by this order.

Continue working until one of these is true:

### PASS
**SAURIN RP5 FULL AUTHORED CAGE PASS — READY FOR CHATGPT / AUTHOR REVIEW**

### Genuine author decision
**SAURIN RP5 REQUIRES AUTHOR DECISION — [decision that cannot be made under existing canon/order]**

### External blocker
**SAURIN RP5 BLOCKED — [external resource/tool/permission blocker]**

Only then return to ChatGPT.

---

# 19. Immutable verification

Verify unchanged:

- canonical W2I6 files;
- canonical seed realization;
- W3B/W3B1/W3D evidence;
- accepted tail module;
- frozen RP3/RP4 production;
- Gorrund source/production;
- all freeze records.

No canonical/frozen asset may be overwritten.

---

# 20. STOP CONDITION

After internal PASS / genuine AUTHOR DECISION / external BLOCKER:
- commit the final evidence;
- stop for ChatGPT review.

Do not:
- freeze Saurin;
- begin final rigging;
- begin final UV/materials;
- begin LOD production;
- begin creator implementation;
- begin UE5;
- begin another race.
