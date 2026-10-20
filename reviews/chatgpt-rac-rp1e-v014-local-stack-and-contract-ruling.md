# RAC RP1E — v014 production-surface interpretation, local projection-stack recovery, and validation-tooling ruling

**Date:** 2026-10-20  
**Authority:** Tyler-authorized autonomous technical ruling through ChatGPT.  
**Parent:** `reviews/chatgpt-rac-rp1e-v013-class-a-closure-order.md` (5693b3b).  
**Returned gate:** `reviews/claude-rac-rp1e-v013-class-a-closure-gate.md` (aa5b4c0).

## 1. Ruling

Continue RP1E.

Do **not** relax the accepted surface tolerances, visual veto, nail tolerance, or zero-self-intersection requirement for the **production mesh**.

The v013 evidence establishes that three separate issues were being conflated:

1. the frozen Gorrund source is genus 3 while the production contract intentionally requires a genus-0 production body;
2. some thin visible features fail because the repeated global projection stack makes neighboring sheets cross after local refinement;
3. T-6 hip_R and nail validation currently contain measurement/tooling problems unrelated to accepted anatomy.

Resolve those separately.

## 2. Production-surface interpretation for the genus-3 source

### 2.1 Product topology remains genus 0

The production mesh must remain:
- one component;
- closed;
- genus 0;
- 0 boundary;
- 0 non-manifold;
- **0 self-intersections**.

Do not copy the source's genus-3 internal handles into the production body.

### 2.2 Exterior-envelope rule

For retopology acceptance, the production target is the **visible/deformable exterior envelope** of the frozen source.

Sealed source surfaces that exist only as the interior wall of a genus handle are not required to be duplicated as internal production sheets when doing so would violate the genus-0 and zero-self-intersection contract.

This is a topology interpretation, not permission to alter the frozen source.

Specifically:

- the sealed L-hand web tunnel;
- the enclosed zero-gap L-axilla void;
- inaccessible internal sheets inside the intentionally fused R-digit block;

may be omitted from the production topology **if and only if** the visible exterior source envelope is preserved.

### 2.3 Fused right digits — mandatory single-envelope production topology

The current v013 solution leaves internal digit sheets crossing inside the fused block. That is not acceptable because Claude identified high deformation/skinning risk.

Do **not** accept those 818+ hidden intersections as Class B.

Instead, rebuild the fused region as a **single exterior production envelope**:
- preserve the visible fused source silhouette and volume;
- preserve the externally visible digit identities up to the actual fusion;
- terminate/merge the internal digit tubes before they become hidden sheets inside the fused block;
- no duplicate/internal opposing production sheets inside the fusion;
- no artificial separation of the fused source anatomy.

This should also remove the false hand contribution to hip_R section measurements.

### 2.4 D-zone deviation accounting

For the two sealed handle interiors and the removed internal fused-block sheets:

- keep a frozen source-face/vertex mask identifying the excluded **non-production interior surfaces**;
- report their area/share explicitly;
- exclude only those masked interior surfaces from T-1/T-2 maximum-deviation pass/fail calculations;
- do not exclude their visible rim, mouth, silhouette, or exterior continuation;
- do not create any new D zone without explicit evidence and author ruling.

Produce both:
1. raw full-source deviation metrics; and
2. production-envelope deviation metrics.

The accepted T-1/T-2 numerical thresholds themselves remain unchanged.

## 3. Local projection-stack change is authorized

The parent stack is no longer immutable in the blocked thin-feature regions.

Do **not** change the global stack for the already-passing open body.

For the blocked visible features, Claude may use **region-specific projection ownership and a region-specific modifier order** so adjacent sheets cannot snap across each other.

Target regions:
- R thumb-web fin;
- philtrum / upper-lip overhang;
- ear rims / knobs;
- L axilla knob and pinch-mouth visible surface;
- L axilla z153 visible pocket;
- R axilla A tip;
- natal-cleft nub;
- L palm crease;
- R hand ulnar web;
- small remaining toe/web/rim folds.

## 4. Preferred local-stack method

Use the following hierarchy.

### P1 — per-sheet ownership targets first

For a thin flap, fin, slit, web or overhang with two nearby source sheets:

1. identify each intended production side;
2. build separate derived projection targets for each source side;
3. assign the production vertices/faces on each side to only their own target;
4. keep the crease/rim ownership explicit;
5. do not allow a whole-body Nearest pass to override the local ownership afterward.

This is the preferred fix because v013 proves the refined topology can reach the target before the global projection makes it cross.

### P2 — local modifier-order change

If P1 alone is insufficient, the affected vertex group may use a local sequence different from the global body, such as:

- Subdivision;
- ownership-specific Nearest/Project;
- restrained local relax/smooth;
- ownership-specific final Nearest;

with **no subsequent whole-body projection on that local group**.

The exact sequence may be chosen from measured tests.

### P3 — final collision-safe/local relaxation

A bounded local relaxation is allowed after projection only if:
- it runs solely on the affected region;
- it preserves the exterior target within T-1/T-2;
- it does not change silhouette;
- it reduces, rather than hides, intersections.

Do not use broad global smoothing.

## 5. Local-stack feasibility matrix

Do not blindly rebuild every remaining feature first.

Use three representative pilot regions:

1. **R thumb-web fin** — thin positive membrane;
2. **L axilla knob/pocket** — contact/crease feature;
3. **philtrum or ear rim** — facial identity overhang.

For each pilot, compare at minimum:

- current v013 stack;
- P1 per-sheet ownership with current local stack;
- P1 + P2 localized modifier-order variant.

Record:
- L1 survival;
- L4 deviation;
- self-x count in the region;
- new self-x elsewhere;
- silhouette/identity effect.

A method is viable only if:
- coarse cage remains 0 self-x;
- the visible feature survives L1;
- no new positive-normal fold appears;
- regional L4 self-x = 0 for true Class-A defects;
- exterior deviation is within the existing T-1/T-2 limit.

If one method works on all three pilot types, use that method for the analogous remaining blocked regions.

If different feature types require different local sequences, that is acceptable if documented.

## 6. v014 geometry scope

Start from v013.

### 6.1 First geometry task
Rebuild the R fused-digit block to the single-envelope production topology in §2.3.

Freeze and gate this before other local-stack work.

### 6.2 Then
Apply only the topology/support changes needed for the visible Class-A regions whose support geometry is already shown to improve deviation.

Do not add a third support-topology attempt merely for density if the prior support topology was already adequate and the failure was projection crossing.

Use the local-stack fix instead.

### 6.3 Preserve
Do not disturb:
- accepted torso/limb macro;
- passed feet except a specific remaining exposed toe point;
- muzzle/nose identity already cleared;
- tail-root geometry;
- already-passing silhouettes.

## 7. T-6 measurement correction

The T-6 tolerance remains:

- target <= 1.0 mm;
- none > 1.5 mm;
- every value > 1.0 mm individually reported.

### 7.1 hip_R

The v013 diagnosis proves the current hip_R section includes the hanging R hand.

Correct the **measurement**, not the anatomy.

Use a deterministic anatomical-component filter:
- intersect the landmark plane as before;
- separate section segments into spatial/connected clusters;
- select the cluster containing the source hip/pelvis landmark region;
- apply the same selection rule to source and production.

Document the rule and prove that it excludes the hand consistently.

Do not simply shrink the radius until the answer passes unless the radius has an anatomical basis.

### 7.2 Tail stations

Re-run tail stations with the existing length-weighted method after v014.

Do not waive them.

If any tail station remains >1.0 mm, report it.
If any remains >1.5 mm, it is still a T-6 failure and must be corrected or returned for decision.

## 8. Nail tooling recovery

The nail tolerance remains **±0.15 mm per tracked nail**.

This is a tooling recovery task.

Claude is authorized to:
1. search the repo and Tyler's E: project/source/evidence folders read-only for the prior AW4 nail-plate masks and foot-frame definitions;
2. stage/copy the required helper files into the cloud workspace;
3. if those helper files are genuinely unavailable, regenerate them deterministically from the frozen `GO-05AW4_nails_final` source using the same prior nail definitions/landmarks and prove equivalence against the prior 05AW4 nail measurements before using them.

Do not change geometry merely because the checker is missing inputs.

Run the per-nail ±0.15 mm gate on the promoted v014 candidate.

## 9. v014 promotion requirements

Freeze one consolidated design:

- `design_v014.npz`
- `design_v014_col.npy`
- `design_v014_info.json`
- all local ownership/stack group definitions.

Import through the normal Blender UI as:

`GO_U_REF_RP1E_retopo_v014.blend`

Do not overwrite v013.

Provenance gate:
- import-vs-design <= 0.10 mm;
- 1 component;
- 0 boundary;
- 0 non-manifold;
- genus 0;
- 0 coarse self-x;
- consistent normals.

## 10. Final progressive gate

Run L1 -> L4 on the promoted v014.

Required reporting:

### Production topology
- 1 component;
- 0 boundary;
- 0 non-manifold;
- genus 0;
- 0 degenerates;
- **0 production self-intersections**.

### Deviation
Report:
- raw full-source T-1/T-2;
- exterior-envelope T-1/T-2 after only the approved D masks;
- exact excluded D area/share.

Exterior-envelope thresholds stay:
- T-1: median <=0.5 / p95 <=1.5 / max <=3.0 mm;
- T-2: median <=0.3 / p95 <=0.8 / max <=1.5 mm.

### T-3
Unchanged.

### T-6
Use corrected hip component method; unchanged tolerance.

### T-7
Unchanged >=0.995.

### Nails
All tracked nails ±0.15 mm.

### Visual veto
Unchanged.

## 11. Decision logic

### PASS
If the production mesh reaches the unchanged exterior-envelope contract, including zero production self-intersections:

**RP1E GORRUND PRODUCTION RETOPO PASS / READY FOR FAMILY-PILOT AUTHOR REVIEW**

STOP.

### Local stack succeeds, but a true contract issue remains
Return:

**RP1E GEOMETRY RECOVERED / FINAL CONTRACT RULING REQUIRED**

Only use this if geometry/self-x is solved and the remaining blocker is specifically a documented measurement/contract interpretation.

### Projection-stack route fails
If per-sheet ownership + localized stack variants fail on the three representative pilots without source-anatomy change:

**RP1E LOCAL PROJECTION-STACK RECOVERY FAILED / AUTHOR DECISION REQUIRED**

Include the three pilot comparison tables and STOP.

Do not resume blind topology refinement.

## 12. No authorization beyond RP1E

No RP2.
No rigging.
No creator implementation.
No UE5 production implementation.

## 13. Return

Return:
`reviews/claude-rac-rp1e-v014-local-stack-recovery-gate.md`

Evidence:
`reviews/rac-rp1e-evidence/`

Update handoff and STATUS only with the substantive result.
