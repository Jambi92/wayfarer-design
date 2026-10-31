# ChatGPT Order — RAC RP5 Saurin Full-Cage Refinement / Closure Order

**Repository:** `Jambi92/wayfarer-design`  
**Branch:** `main`  
**Reviewed WIP commit:** `f7bbe0bfa335d1abbdbbb711b11a9832161064d2`  
**Parent order:** `reviews/chatgpt-rac-rp5-saurin-full-authored-cage-order.md`  
**Scope:** refine the current full Saurin cage; close T-1 / T-2 / T-4; prove deformation ownership; complete missing semantic, identity, creator-support, detail-layer and PD evidence; return the actual full-body RP5 gate  
**Author ruling:** current cage architecture is APPROVED TO CONTINUE. Do not restart from scratch.  
**Stop condition:** complete the full authored-cage closure gate and **STOP FOR CHATGPT REVIEW**. Do not freeze.

---

# 1. Preserve the current architecture

Keep the existing full-body Saurin cage architecture from commit:

`f7bbe0bfa335d1abbdbbb711b11a9832161064d2`

Current WIP:
- 107,532 vertices
- 107,530 quads
- 100% quads
- one closed manifold body
- tail included
- identical c1 / c2 topology

Do **not**:
- restart from QuadriFlow;
- replace the full cage with a new automatic remesh;
- replace the accepted tail module;
- change the c1/c2 topology-sharing strategy;
- reopen Saurin biology;
- reopen the approved thigh art-pass.

This order is a **refinement / closure pass**, not an architecture reset.

---

# 2. Thigh art-pass — ACCEPTED / CLOSED

The derived thigh cleanup on `SA_RP5_WORK_v001` is accepted as production working-source preparation.

Preserve:
- the same changed vertex set on c1/c2;
- authorized 63–87 cm ramp / 66–84 cm full-strength band;
- canonical W2I6 source files untouched;
- W2 measurements and silhouette equivalence;
- pelvis/hip landmarks unchanged.

Do not further smooth or reshape the thigh unless a new cage-fit defect directly requires a bounded local change and is separately reported.

Treat this portion as **CLOSED**.

---

# 3. Current PASS gates to preserve

The following current results are good and must not regress:

## T-3
PASS on c1/c2.

## T-5
Regional mean density within production ceilings.

## T-6
PASS:
- c1 max landmark drift ~0.96 mm;
- c2 max landmark drift ~0.95 mm;
- no >1.0 mm current surface-landmark drift.

## T-7
PASS with tail included:
- all primary views ~0.9963–0.9970.

These are protection gates during refinement.

Any regression must be reported immediately.

---

# 4. T-1 / T-2 — localized precision closure

The architecture is retained; solve only the localized error clusters.

Current WIP:
- T-1 median ~0.067 mm, p95 ~0.50 mm — already good;
- T-1 max ~7.6 mm — FAIL;
- T-2 p95 generally good;
- T-2 max head / hands / feet / tail stations still ~2.1–2.9 mm — FAIL.

The problem is **maximum-error localization**, not broad cage fidelity.

## Required error-cluster analysis

Generate a machine-readable table of all vertices/faces exceeding:

- T-1 > 3.0 mm;
- T-2 identity-zone > 1.5 mm.

Cluster by anatomy.

At minimum isolate:

1. axilla vault / shoulder-neck slope;
2. snout / rostrum local max;
3. hand/finger/claw local maxima;
4. foot/toe/claw local maxima;
5. ventral pelvis / perineum;
6. body quads immediately cranial to the accepted tail-module root.

For every cluster report:
- count;
- max error;
- p95;
- anatomical cause;
- topology cause vs projection/relax cause;
- proposed bounded correction.

No global smoothing solution.

---

# 5. Axilla / shoulder-neck correction

This is currently the main T-1 blocker.

Current error:
- axilla vault around u ~150 cm;
- shoulder-neck slope around u ~160 cm;
- localized 4–7.6 mm miss.

Authorized approach:
- reshape the authored coarse shoulder / axilla hole rows;
- add or redistribute trunk/axilla support rows where needed;
- improve junction projection;
- use source-driven sliding / bounded local relaxation;
- keep shoulder/arm topology semantic structure intact.

Do not:
- widen/narrow the Saurin shoulder anatomy;
- alter thorax canon;
- use aggressive global Laplacian smoothing;
- reduce valid anatomy to make the cage easier.

Goal:
- T-1 max <= 3.0 mm;
- identity-zone max if applicable <=1.5 mm;
- no T-7 regression;
- no deformation-quality regression.

---

# 6. Head / rostrum local max

Current T-2 head p95 passes, but max is ~2.74 mm.

Diagnose the exact point/patch.

Likely candidates include:
- rostral cap;
- lip crease transition;
- canthal / orbit junction;
- jaw corner;
- display-root neighborhood.

Fix by:
- local authored row adjustment;
- local projection;
- local ring phase / relaxation correction.

Do not:
- alter rostral projection canon;
- soften structural ridges;
- change orbital spacing;
- humanize the mouth or jaw.

Goal:
- head T-2 max <=1.5 mm.

---

# 7. Hands / claws local max

Current hand T-2 max ~2.1 mm.

Localize whether the error is:
- claw tip;
- finger tip;
- web;
- palm transition;
- thumb;
- wrist-hand junction.

Authorized:
- local ring refinement;
- local claw-cap support;
- palm / knuckle transition correction;
- projection improvement.

Preserve:
- five digits;
- opposable thumb;
- accepted claw form;
- hand silhouette;
- shared c1/c2 topology.

Goal:
- hand T-2 max <=1.5 mm.

---

# 8. Feet / claws local max

Current foot T-2 max ~2.8 mm.

Localize:
- toe tip;
- claw cap;
- forefoot;
- heel;
- ankle-foot transition;
- web region.

Authorized:
- local ring / claw-cap support;
- local projection / phase correction;
- plantigrade-contact preservation.

Do not:
- alter foot length;
- alter toe count;
- alter plantigrade stance;
- digitigrade the foot.

Goal:
- foot T-2 max <=1.5 mm.

---

# 9. Tail-root cranial interface / pelvis ventral region

The accepted tail module itself remains approved.

Current issue:
- tail stations include a ~2.9 mm max on body quads just ahead of module root;
- perineum / ventral tail-root body region ~3.3 mm reported in handoff.

Fix the **body-side transition**, not the accepted tail module unless proven necessary.

Authorized:
- body-side ring redistribution;
- source-driven sliding;
- pelvis/sacral junction correction;
- ventral root integration correction.

Preserve:
- tail root area;
- tail length;
- tail RSI / coupling;
- tail carriage;
- module ring architecture;
- 16-chain landmarks.

Goal:
- tail-station T-2 max <=1.5 mm;
- T-1 max <=3 mm;
- no seam / “tube attached to torso” visual read.

---

# 10. T-4 — mandatory topology-quality cleanup

Current WIP is not acceptable yet:

- ~789 quads aspect > 4;
- ~3.1% quads outside 45–135°;
- collapsed fine edges create pathological aspect values.

This must be corrected before final gate.

## Required T-4 cluster map

List every T-4 failure cluster with:
- anatomy region;
- count;
- max aspect;
- min/max angle;
- whether it is in deformation-critical topology.

Expected hotspots include:
- 2:1 palm transition rows;
- 2:1 forefoot transition rows;
- local junction fans;
- collapsed projection edges;
- possibly tail/body fusion transitions.

## Authorized fixes
- local row redistribution;
- 2:1 transition redesign;
- edge sliding;
- corner-fan cleanup;
- local ring phase shift;
- local quad-centroid / angle-improving relaxation;
- remove accidental collapsed edges.

## Hard requirements
- no zero-area quads;
- no pathological near-zero edges;
- aspect <=4:1 outside accepted digit/tail-tip exemptions;
- deformation-critical zones must satisfy the production standard;
- angle outliers must be reduced to a bounded, explainable residual only if they cannot be eliminated.

Do not hide T-4 failures by deleting topology.

---

# 11. Explicit tail-tip / digit-tip exception accounting

Where the production contract permits tip exceptions:

- identify them explicitly;
- prove they are truly inside tail-tip or digit-tip zones;
- keep them out of deformation-critical creases;
- record exact counts and maximums.

No broad “tip exception” may cover palm, forefoot, wrist, ankle or root-transition defects.

---

# 12. Deformation — ownership proof required

The current temporary LBS scaffold produces many cage flips/folds in:
- shoulder;
- neck;
- trunk;
- pelvis;
- tail root.

The dense source shows substantially worse failures under the same crude scaffold.

This is **suggestive** of setup / weighting / source-deformation ownership, but not sufficient for final acceptance.

## Required ownership decomposition

For each problematic pose:

1. run current cage + current temporary weights;
2. run dense working source + same scaffold;
3. run cage with locally improved diagnostic weighting / influence localization;
4. run a topology-only fold test on the relevant cage patch;
5. compare rest-state quad quality and crease alignment.

Classify each failure as:
- TOPOLOGY;
- WEIGHTING / TEMPORARY SCAFFOLD;
- SOURCE-DEFORMATION / PD-2;
- SURFACE DETAIL / PD-1;
- MIXED.

No topology failure may be waved away because the dense source behaves worse.

---

# 13. Minimum deformation closure criteria

Before final gate, require:

## Must be clean or clearly non-topology
- jaw;
- wrist flex/ext;
- fist/grasp;
- thumb opposition;
- ankle;
- toe flex/ext;
- knee;
- mid-tail.

## High-attention zones
- neck flex / rotation;
- shoulder abd45 / abd90 / flex;
- hip flex;
- trunk twist;
- lower axial flex;
- tail-root lateral / vertical;
- tail twist.

For high-attention zones:
- if flips/folds remain, demonstrate with evidence that the owning defect is temporary weighting / source PD-2 and that the cage's topology remains deformation-suitable.

Any genuine cage-topology fold remains a blocker.

---

# 14. Semantic topology map — required now

Complete the semantic map required by the parent order.

At minimum label:

- orbit rings;
- mouth rings;
- jaw hinge;
- neck rings;
- shoulder/axilla;
- elbow;
- wrist;
- MCP/IP;
- trunk flex rings;
- lower axial rings;
- hip;
- knee;
- ankle;
- MTP/toe joints;
- tail root;
- tail chain bands;
- display root;
- claw-cap regions;
- 2:1 reduction rows.

The semantic map must be identical across c1/c2.

---

# 15. Identity metrics on the actual full cage

Run the accepted Saurin identity metrics against the refined cage.

Required source vs cage:

- stature;
- lower axial trunk length;
- thorax breadth/depth;
- pelvic band;
- tail length / stature;
- tail root area;
- tail 25/50/75% section areas;
- tail RSI / coupling;
- tail carriage;
- forearm/arm;
- femur/leg;
- rostral projection;
- orbit spacing;
- structural ridge readability;
- plantigrade foot read;
- claw presence;
- display-root integration.

No metric drift may be hidden by a good silhouette.

---

# 16. c1 / c2 shared-topology proof

Preserve:
- exact same face list;
- exact same semantic map;
- exact same vertex ordering.

Re-run:
- T-1/T-2 independently on SA-M188 and SA-F188;
- identity metrics independently;
- tail-root fusion independently;
- deformation ownership independently in at least the most sensitive c2 poses.

Any need for topology divergence is an author-review stop.

---

# 17. Creator-support diagnostics — complete the missing package

Do not build the full creator.

Test only topology support on bounded accepted states.

Required:
- Narrow frame;
- Broad frame;
- lower axial trunk low/high;
- pelvic-band low/high;
- short/long tail;
- small/large tail base;
- taper extremes;
- reachable tail-cap cases;
- orbit spacing −8/+3%;
- ridge lower/upper safe states;
- one low/high display-root structural state;
- hand/finger variation;
- foot/toe variation.

Return:
- PASS / CONSTRAIN / FAIL per state;
- where topology margin is thinnest;
- whether any accepted creator range would require a topology branch.

Do not change canon.

---

# 18. Layered scale-detail prototype — complete now

Implement the approved prototype after the refined base cage passes.

Required:
- regenerate canonical scale relief from saved seeds;
- transfer/reconstruct on the production-cage-derived surface;
- preserve Regional Scale Architecture field boundaries;
- compare against canonical surfaced W2.

Report:
- surface deviation;
- silhouette;
- field continuity;
- joint-region behavior;
- determinism;
- which detail stays geometric vs displacement/normal.

PD-1 must remain explicitly separated.

---

# 19. PD ownership final package

Return one concise ownership table for:

- PD-1 surface transport;
- PD-2 composition/base inversion;
- PD-3 seed validity/resampling;
- PD-4 auricular empty-field robustness.

For each:
- topology impact;
- current status;
- production owner;
- whether it blocks RP5 cage acceptance.

Do not claim resolution without evidence.

---

# 20. Final quality gates before return

The actual full-body gate may return PASS only if:

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
No unbounded quality failures.
- no collapsed edges;
- no pathological aspect;
- aspect <=4:1 outside explicit tip exemptions;
- angle residuals bounded and documented.

## T-5
PASS.

## T-6
PASS.

## T-7
PASS with tail included.

## Deformation
No unresolved topology-class defect.

---

# 21. Required final boards

Complete the parent order's A–P boards.

At minimum ensure final versions include:

- thigh before/after;
- full wire;
- pole/valence;
- head;
- neck;
- shoulders;
- hands;
- pelvis/tail root;
- feet;
- tail;
- c1/c2 overlays;
- source deviation heatmaps;
- density;
- layered detail;
- worst deformation poses;
- creator-support states.

WIP boards are not the final evidence package.

---

# 22. Pilot production files

If all closure gates pass, create:

- `SA_M_REF_RP5_pilot_v001`
- `SA_F_REF_RP5_pilot_v001`

Status:
**PILOT / NOT FROZEN**

Include:
- .blend;
- topology sidecar;
- source/barycentric mapping;
- semantic map;
- landmarks;
- read-back verification.

Do not create a freeze record.

---

# 23. Required decision

Return exactly one:

## SAURIN RP5 FULL AUTHORED CAGE PASS — READY FOR AUTHOR FINAL-CONSOLIDATION ORDER

or

## SAURIN RP5 FULL AUTHORED CAGE NEEDS REVISION — [exact remaining blocker]

or

## SAURIN RP5 REQUIRES AUTHOR DECISION — [exact unresolved issue]

---

# 24. Required return

Commit:

1. `reviews/claude-rac-rp5-saurin-full-authored-cage-gate.md`;
2. refined full cage;
3. T-1/T-2 cluster closure record;
4. T-4 cluster/cleanup record;
5. semantic topology map;
6. final c1/c2 proof;
7. identity metrics;
8. creator-support diagnostics;
9. layered detail prototype;
10. PD ownership table;
11. deformation ownership/classification;
12. final boards;
13. immutables;
14. pilot production files if PASS;
15. narrow STATUS/handoff update.

---

# 25. Immutable verification

Verify unchanged:

- canonical W2I6 Saurin files;
- canonical seed realization;
- W3B/W3B1/W3D evidence;
- accepted tail module;
- frozen RP3/RP4 production;
- Gorrund source/production;
- all freeze records.

No canonical or frozen asset may be overwritten.

---

# 26. STOP CONDITION

Do not:
- freeze Saurin;
- modify W2I6 canon;
- restart the full topology from an automatic remesh;
- overwrite the accepted tail module;
- begin final rigging;
- begin final UV/material work;
- begin LOD production;
- begin creator implementation;
- begin UE5 integration;
- begin another race.

Complete the refinement/closure pass and **STOP FOR CHATGPT REVIEW**.
