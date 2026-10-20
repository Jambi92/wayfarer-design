# RAC RP1E — v014 M1 slit-band rebuild and continued manifold-contact closure order

**Date:** 2026-10-20  
**Authority:** Tyler-authorized autonomous continuation through ChatGPT.  
**Parent ruling:** `reviews/chatgpt-rac-rp1e-v014-manifold-contact-topology-ruling.md` (dc9d48f).  
**Returned gate:** `reviews/claude-rac-rp1e-v014-manifold-contact-gate.md` (500fcc3).  
**Preserved best M1 evidence:** `reviews/rac-rp1e-evidence/exp_v017_manifold/design_M1D04_cage.npz`.

## 1. Decision

Continue RP1E.

Choose M1 route **(a)** from the returned gate as the primary fix:

> Re-author the R-hand B/C facing walls from crotch to fusion as one continuous manifold slit band whose floor/shared crease follows the actual source slit-tip line.

The tube-to-side junction approach is retired for M1.

If the slit-band route is geometrically correct but the evaluated final surface still maps one wall onto the other, route **(b)** is authorized as the fallback:

> explicit per-wall source masks and final-resolution side-preserving remap.

Do not return for another author decision between (a) and (b); execute (a), then (b) if needed under the gates below.

## 2. Starting state

Authoritative production state remains v013:

- `GO_U_REF_RP1E_retopo_v013.blend`;
- `designs/design_v013.npz`.

No v014 has been promoted.

Preserve:
- v009–v013;
- all v016/v017 evidence;
- the best previous M1 cage `design_M1D04_cage.npz`.

The new M1 rebuild should be based on v013, using M1D04 only as diagnostic/reference evidence unless a component can be reused without preserving the bad seam placement.

## 3. M1 source truth

The source R-hand B–C anatomy is:

- one legitimate visible through-slit;
- source genus handle is real exterior anatomy;
- the slit narrows from a finite gap to a shared tip/crease;
- the fused block beyond the slit is one exterior volume;
- internal overlapping production sheets are forbidden.

The final production hand must preserve that visible handle and be manifold.

## 4. M1 slit-band topology

Rebuild the B/C facing-wall topology from a clean boundary before the crotch through the slit and into the fusion.

### 4.1 Continuous slit-band structure

Author one coherent patch containing:

1. B-side exterior wall;
2. C-side exterior wall;
3. the open slit between them where the source gap is finite;
4. a **shared floor/crease chain exactly on the source slit-tip line** where the gap reaches zero;
5. a continuous transition into the fused exterior block;
6. no capped hidden digit tube inside the fusion;
7. no tube-to-side disk junction.

The shared crease must occur at the actual source tip, not 3–7 mm displaced toward digit C.

### 4.2 Source tracing

Trace the slit floor/tip directly from the frozen source in sections along the B–C slit.

Freeze:
- the slit-mouth boundary;
- B wall path;
- C wall path;
- shared tip/crease polyline;
- fusion transition.

Use enough sections that the floor placement error is <= 0.25 mm before subdivision.

### 4.3 Density

Use compatible graded density across the entire facing-wall patch.

Do not create another narrow strip stitched into very large faces.

The attachment loops on B and C may be refined/rebuilt as far back as necessary to keep:
- aspect reasonable;
- Catmull-Clark support coherent;
- L1 surfaces on the intended side of the slit.

## 5. M1 explicit side ownership

Use **explicit frozen source face masks**, not normal-sign splitting.

Create:
- `Rhand_B_wall_source_faces`;
- `Rhand_C_wall_source_faces`;
- shared-crease/rim source set;
- fused-block exterior source set.

Requirements:
- B and C masks do not overlap except on the shared crease boundary;
- neither mask includes the facing wall of the opposite digit;
- the fused-block mask contains only the exterior envelope;
- no hidden/internal source sheet becomes a production target.

Save and visualize all mask boundaries.

## 6. M1 projection/evaluation

The low-resolution patch must first pass:

### Coarse
- 1 component globally;
- 0 boundary;
- 0 non-manifold;
- genus 1 globally;
- 0 coarse self-x.

### L1
- visible slit remains open;
- shared crease sits on the source slit tip;
- B and C walls stay on their own source sides;
- **regional self-x = 0**.

If L1 fails, revise the topology before L4.

### L4
Required in the M1 region:
- **regional self-x = 0**;
- hand T-2 max <= 1.5 mm;
- no product internal sheets;
- visible slit preserved;
- fused exterior silhouette preserved.

## 7. Attempt budget for M1

### Serious attempt A
Full continuous slit-band topology with explicit wall masks.

### Serious attempt B
A second full slit-band topology variation may alter:
- support-ring placement;
- number of columns;
- attachment-loop position;
- shared-crease support;
- fusion transition.

If one of these reaches L1 clean but final L4 mapping still crosses solely because projection loses wall identity, proceed to §8.

Do not return to the retired tube-to-side junction.

## 8. Authorized final-resolution per-wall fallback

If the low-resolution slit-band is topologically correct and L1-clean but L4 still crosses:

Use final-resolution replacement with **separate source-side masks**.

Unlike the failed disk-to-disk remap, do not map a patch containing both slit walls onto one topological source disk.

Instead:

1. split the final production patch along the shared crease and the mouth/fusion boundaries into topologically matching B-wall and C-wall patches;
2. remap B wall only to the frozen B-wall source mask;
3. remap C wall only to the frozen C-wall source mask;
4. keep the shared crease chain identical for both sides;
5. map the fused-block continuation to the exterior fused source mask;
6. weld all shared boundaries exactly.

Final requirements remain:
- one manifold genus-1 body;
- 0 boundary/non-manifold;
- 0 regional self-x;
- no duplicate shared vertices along the crease;
- T-2 pass.

This fallback may use direct final-resolution authoring/remapping only in the bounded M1 region.

## 9. M1 stop condition

If the continuous slit-band route **and** the explicit per-wall final-resolution fallback both fail to achieve regional self-x = 0 while preserving the visible slit and T-2:

Return:

**RP1E R-HAND VISIBLE HANDLE BLOCKED / AUTHOR DECISION REQUIRED**

Include:
- source slit sections;
- attempt A/B topology;
- explicit masks;
- L1 and L4 results;
- final-resolution fallback result.

Then STOP.

## 10. If M1 passes — continue M2–M6 automatically

Do not stop for another author gate after M1 passes.

Continue the existing manifold-contact program using the same principles:

### M2 — R thumb web
Entire local patch rebuild, explicit palm/thumb side masks, shared manifold rim at zero-thickness taper.

### M3 — L axilla visible knob/pinch/z153
Visible patch only; hidden D void excluded; finite-gap walls distinct, zero-gap contact terminates at shared crease.

### M4 — ears
Explicit source-side masks and shared rim edge; no normal-sign ownership.

### M5 — philtrum / lip / nose folds
Finite slots stay open; zero-width creases terminate manifoldly.

### M6 — remaining open Class-A defects
R axilla A tip, natal nub, palm crease, ulnar web, exposed toe/rim folds.

For M2–M6, the direct final-resolution local-patch fallback from the parent ruling remains authorized after a clean low-resolution topology attempt.

Do not use repeated global stack experiments.

## 11. D masks

After M1 passes and before the final gate, build the explicit topological D masks exactly as ruled:

- hidden L-hand tunnel interior only;
- hidden L-axilla void interior only.

Use seeded face-graph flood bounded by manually verified throat loops.

No visibility-beam threshold.

Freeze:
- face IDs;
- boundary loops;
- area/share;
- section proof.

## 12. Nails

After M1 passes, perform the already-authorized nail free-edge repair.

Use the recovered tool set that reproduces source tips to <=0.003 mm.

Required:
- 8/8 nails within ±0.15 mm;
- no new local self-x;
- no toe-length/global foot change;
- T-2 still passes.

## 13. T-6

The ruled T-6 implementation is closed and accepted:

- hip connected-curve selection;
- exact radius-circle segment clipping;
- unchanged tolerance.

v013 currently passes:
- max 1.122 mm;
- tail_00 and tail_05 >1.0 reported;
- none >1.5.

Re-run on the final candidate but do not reopen the measurement method.

## 14. v014 promotion

Promote only after M1–M6, D masks, and nails are integrated into one candidate.

Freeze:

- `design_v014.npz`;
- `design_v014_col.npy`;
- `design_v014_info.json`;
- source-side mask files;
- D masks;
- nail support metadata;
- any final-resolution patch provenance.

Import through Blender UI as:

`GO_U_REF_RP1E_retopo_v014.blend`

Do not overwrite v013.

## 15. Final v014 gate

### Topology
- 1 component;
- 0 boundary;
- 0 non-manifold;
- genus 1;
- 0 degenerates;
- **0 production self-intersections**;
- quad-dominant.

### Production-envelope surface
T-1:
- median <=0.5 mm;
- p95 <=1.5 mm;
- max <=3.0 mm.

T-2:
- median <=0.3 mm;
- p95 <=0.8 mm;
- max <=1.5 mm.

Also report raw full-source values.

### T-3
Unchanged.

### T-6
Ruled method; target <=1.0 mm; none >1.5 mm.

### T-7
>=0.995.

### Nails
8/8 within ±0.15 mm.

### Visual veto
Unchanged.

## 16. Final stop logic

### Full pass

**RP1E GORRUND PRODUCTION RETOPO PASS / READY FOR FAMILY-PILOT AUTHOR REVIEW**

STOP.

### Clean exterior production mesh, only D documentation disputed

**RP1E EXTERIOR PRODUCTION MESH PASS / D-MASK AUTHOR REVIEW REQUIRED**

STOP.

### Later M2–M6 bounded feature block

If M1 passes but a later feature still fails after the low-resolution manifold patch + authorized final-resolution local fallback:

**RP1E POST-M1 LOCAL FEATURE BLOCKED / AUTHOR DECISION REQUIRED**

Return only the failed feature evidence; do not undo passing regions.

STOP.

## 17. Scope

No RP2.
No rigging.
No creator implementation.
No UE5 production implementation.

## 18. Return

Return:

`reviews/claude-rac-rp1e-v014-manifold-closure-gate.md`

Evidence remains:

`reviews/rac-rp1e-evidence/`

Update:
- `reviews/rac-rp1e-evidence/RP1E_progress.md`
- `reviews/claude-session-handoff.md`
- `specs/STATUS.md` only with the substantive result.
