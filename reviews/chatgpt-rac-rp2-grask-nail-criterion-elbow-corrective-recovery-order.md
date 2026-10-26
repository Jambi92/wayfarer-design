# RAC RP2 — Grask nail-criterion ruling and elbow corrective-recovery order

**Date:** 2026-10-26  
**Authority:** Tyler-authorized autonomous continuation through ChatGPT.  
**Parent diagnostic return:** `reviews/claude-rac-rp2-grask-nail-binding-elbow-weight-isolation-gate.md` (44e1ec6).  
**Parent order:** `reviews/chatgpt-rac-rp2-grask-baseline-nail-binding-and-elbow-weight-isolation-order.md` (b303b9e).  
**Frozen retopology:** `GR_U_REF_RP2_retopo_v003.blend`, SHA-256 `03bfe7d924ff5b8b61a4c10095af5d16ca29d41667d7f61d0abeca14e1f07ce0`, geometry `f9c4a7ac98e86d98017376b9d67c85428503d2d6385258471d99bc766bfe702f`.  
**Diagnostic baseline:** W0 `weights_v001c.npz` SHA prefix `74cbfb95…`; v002 landmarks; rigdiag v003 is the current derived diagnostic file.

## 1. Rulings on the returned decisions

### N-1 — nail criterion mask: REVISE PROSPECTIVELY

Adopt the **groove-bounded nail-plate mask** as the correct nail-rigidity criterion for all new diagnostic runs.

Reason:
- the actual sculpted nail plate is already rigid under W0 to approximately 0.000–0.012 mm;
- the former distal-cap mask crosses the U-shaped nail groove and includes periungual fold skin;
- that fold skin is anatomically supposed to deform;
- forcing the full cap rigid only moves deformation into surrounding skin and creates a new thumb fold.

Therefore:

- New criterion name: **Nail Plate Rigidity v2**.
- Mask: connected groove-bounded plate region, stopping at the proximal/lateral groove.
- Pass threshold remains **<= 0.3 mm Kabsch rigid-fit residual**.
- Keep the old cap-mask metric in reports as **Nail Cap Historical v1** for continuity only.
- Do not retroactively relabel past runs.
- Do not claim the old cap criterion was “passed”; state that it was superseded because it measured deformable periungual skin in addition to the nail plate.

### N-2 — WN / WNcap

- **W0 remains the diagnostic weight baseline.**
- WN is **not adopted**; retain it as a no-op evidence record only.
- WNcap remains **REJECTED**.
- Do not bind periungual fold skin rigidly.

### E-1 — weights-only elbow work

**ACCEPT: the left-elbow weights-only experiment is exhausted within the authorized candidate family.**

E1 and E2 are not selected.

Do not spend another cycle inventing more upperarm/forearm weight re-splits of the same class.

### E-2 — 130° forearm–biceps overlap

Do **not** reclassify the 130° overlap as expected contact at this time.

It is demonstrated same-part penetration with approximately 4.5 mm maximum depth and remains a failure unless:
- a later predeclared contact model demonstrates that this exact overlap is acceptable soft-tissue compression without surface penetration, or
- the deformation is corrected.

Proximity/contact is expected at deep flexion; mesh penetration is not automatically exempt.

### E-3 — E2's 90° gain

E2 is **not adopted** as a weight parent.

Its 90° orientation improvement may be used as diagnostic evidence when designing the corrective, but W0 remains the parent weight array.

## 2. Next phase — pose-space elbow corrective feasibility and recovery

The next authorized work is a **bounded pose-space corrective study** for the elbow.

This is not permission to reopen retopology.

This is not production-rig freeze authority.

The purpose is to determine whether the frozen retopology + W0 + accepted landmarks can achieve acceptable elbow deformation using localized pose-dependent correction.

## 3. Immutable parents

Verify before and after:

- frozen retopo v003 hash and geometry above;
- frozen SOURCE_3D v005 and all source sidecars;
- v001/v002/v003 retopo provenance;
- current diagnostic rigs v001/v002/v003;
- W0/W1/W2/WN/WNcap/E1/E2 records;
- accepted thumb-web anatomy and narrow-web quad exception.

No rest-mesh edit.

No topology edit.

No vertex-count or face-count change.

No UV/material/LOD/UE5 work.

If any frozen parent hash differs, STOP and report.

## 4. Diagnostic file/versioning

Create a new derived diagnostic file:

`GR_U_REF_RP2_rigdiag_v004.blend`

Required:
- rest geometry bit-identical to frozen retopo v003;
- skeleton/rest matrices unchanged from the current diagnostic parent;
- W0 weights bit-identical;
- v002 landmarks unless a separately approved knee comparison explicitly uses v003 as a comparison;
- corrective data clearly tagged as diagnostic and non-production.

Record:
- full file hash;
- rest geometry hash;
- skeleton matrix hash;
- W0 weight hash;
- corrective support vertex IDs and delta hashes.

## 5. Corrective method

Use a **pose-space corrective delta field**, not a new weight re-split.

The initial feasibility study may evaluate the corrective as a post-skin diagnostic delta so that the geometry question is isolated cleanly.

If a candidate passes, also show that the same correction can be represented by a practical production mechanism (for example pose-driven shape/corrective deformation) without changing the frozen rest mesh.

Do not use:
- remesh;
- rest-shape sculpt;
- topology revision;
- helper bones in the first corrective family;
- broad whole-arm displacement;
- corrective deltas outside the declared support.

Helper-bone work is deferred unless this corrective family proves insufficient.

## 6. Corrective support

Primary support is the left elbow/adjacent soft tissue.

The support must include only what is necessary to address:
- inner elbow crease;
- compressed loops `elbow_l_21|22`;
- forearm flesh near deep flexion;
- distal upper-arm/biceps flesh implicated in the 130° penetration;
- outer elbow contour if needed for volume preservation.

Use one connected support region.

Suggested maximum support extent:
- approximately 18 cm from the accepted elbow pivot;
- full corrective strength only in the necessary inner core;
- smooth C1/C2 taper to exactly zero at the support boundary.

Document:
- support IDs;
- core IDs;
- taper band;
- max delta;
- per-edge delta gradient;
- whether the support crosses any anatomical seam/part boundary.

No shoulder, wrist, hand, torso or unrelated upper-arm correction.

## 7. Pose keys / interpolation

Build corrective targets around the actual failing flexion arc.

At minimum evaluate:
- 45°;
- 90°;
- 130°.

Recommended driver behavior:
- 0 corrective at rest;
- near-zero / minimal corrective at 45° unless evidence requires otherwise;
- dedicated correction at 90°;
- dedicated correction at 130°;
- smooth interpolation through the range;
- smooth return to zero as flexion returns to rest.

Do not create a discontinuous “snap” between keys.

Log the driver curve and exact activation weights at all tested poses.

## 8. Corrective objectives

The corrective must solve geometry, not merely improve one proxy.

Use all existing retained elbow metrics unchanged.

Primary objectives:

1. eliminate non-contact self-intersections at 90° and 130° where technically achievable;
2. materially reduce inner-crease penetration/depth;
3. improve `elbow_l_21|22` loop compression;
4. preserve outer elbow contour and volume;
5. avoid new folds/local inversions;
6. avoid new orientation-disagreement clusters;
7. avoid excessive strain;
8. preserve rest-return exactly.

Do not select a candidate that improves 90° while worsening 130°.

Do not select a candidate that hides penetration by creating a fold.

## 9. Candidate budget

Authorize up to **three internal corrective candidates** in this family.

Claude may iterate internally among C1/C2/C3.

Do not turn in the first attempt.

Selection must be based on the combined 45° / 90° / 130° result under the same metric set.

If none of the three candidates produces a clear net improvement without new failures, stop with the blocker status in §18 rather than starting an unbounded campaign.

## 10. LBS / DQS evaluation

Evaluate the selected corrective under both:
- LBS;
- DQS / preserve-volume diagnostic mode.

Keep:
- identical rest geometry;
- identical pivots;
- identical W0 weights;
- identical poses;
- identical corrective activation.

Do not select a skinning policy for UE5 here.

The purpose is to ensure the corrective is not merely compensating for one evaluation method while catastrophically failing under the other.

Report both methods separately.

## 11. Right-elbow propagation after left success

Do not mirror anything until the left-side corrective family clearly passes the local selection gate.

If the left side passes:

1. create a geometry-aware right-side counterpart using symmetry/mapping from the frozen mesh;
2. preserve real left/right asymmetry where present;
3. test the same flexion arc on the right;
4. adjust only within the same bounded corrective class if the right side needs a small asymmetric correction.

Do not assume index mirroring alone is valid.

If the right side fails for a materially different anatomical reason, report that difference and keep the left result.

## 12. Nail criterion implementation

Update the diagnostic evaluator so every new run reports both:

### Gating
**Nail Plate Rigidity v2**
- groove-bounded plate mask;
- <=0.3 mm.

### Historical / non-gating
**Nail Cap Historical v1**
- old distal-cap set;
- report residual;
- explicitly label periungual-skin inclusion.

Run a mask sanity sheet showing:
- plate mask;
- groove;
- excluded periungual fold skin;
- original historical cap mask.

No geometry or weights change is needed for this ruling.

## 13. Topology-density audit — analysis only

Because `elbow_l_21|22` remains strongly compressed, perform a **non-destructive topology-density audit** around the elbow.

Measure:
- loop spacing at rest;
- edge lengths;
- quad aspect;
- valence;
- loop count across the flexion zone;
- density gradient relative to adjacent upper-arm and forearm regions.

Compare the implicated loops with neighboring passing regions.

This audit is evidence only.

**Do not edit the frozen retopology.**

If the corrective cannot pass because the existing loop distribution cannot support the required shape, identify that precisely for later author ruling.

Do not infer “topology limitation” merely from failure; demonstrate the mechanism.

## 14. Knee verification

The previous cycle did not trigger the v003-knee verification because no elbow weight candidate was selected.

After a corrective candidate is selected and before the final full-suite run:

- run the previously defined bounded-v003-knee versus unrestricted-v002 comparison;
- keep W0 weights;
- keep elbow corrective inactive for knee-only poses unless the pose includes elbow flexion;
- report the exact displacement compliance and deformation result;
- do not silently promote the knee landmark if it still conflicts with the 5 mm bound.

This remains diagnostic, not production landmark freeze authority.

## 15. Full-suite regression gate

If and only if a left corrective is selected:

1. propagate/test the right side as above;
2. enable **Nail Plate Rigidity v2** as the new gating nail metric;
3. retain Nail Cap Historical v1 as report-only;
4. run the complete original 43-pose suite;
5. add any necessary elbow 45° poses as supplemental diagnostics, not replacements;
6. compare against W0 baseline;
7. highlight every changed metric, every fixed criterion and every regression.

Unrelated poses with corrective activation = 0 should remain bit-identical or numerically equivalent to the baseline.

Any unexpected unrelated change is a failure and must be investigated before return.

## 16. Visual evidence

Required identical-camera sheets:

### Elbow
- W0 vs selected corrective;
- 45°, 90°, 130°;
- LBS and DQS;
- inner crease;
- lateral/outer contour;
- front/three-quarter;
- wireframe close-up;
- intersection/fold IDs.

### Cross-section
- flexion-plane contour overlays at 90° and 130°;
- W0 vs selected corrective;
- inner crease and outer contour marked;
- penetration pairs marked.

### Corrective field
- support/core/taper visualization;
- delta magnitude;
- delta direction;
- boundary continuity.

### Nail criterion
- old cap vs new plate mask;
- groove and fold skin visible.

### Topology audit
- rest wire/loop map around `elbow_l_21|22`;
- spacing/density measurements.

Do not rely on metric tables alone.

## 17. Acceptance logic

A corrective candidate may be selected only if:

- no new non-local failure is created;
- 45° remains clean;
- 90° improves on geometric integrity;
- 130° improves rather than regresses;
- no new local fold/inversion is introduced;
- rest-return remains exact;
- outer contour stays anatomically plausible;
- the correction is localized and smoothly tapered;
- full-suite regression check is clean outside intended elbow changes.

Do not require every historical proxy to improve if it has already been shown to be reference-sensitive; retain and report it, but select by demonstrated geometry and the retained meaningful metrics.

## 18. Return statuses

### Desired success

If the corrective family succeeds locally and the full suite has no unintended regression, return:

**RP2 GRASK ELBOW CORRECTIVE RECOVERY PASS / NEXT DEFORMATION FAILURES READY FOR TRIAGE**

This does **not** mean the whole Grask production deformation suite is accepted unless all remaining retained failures are also gone.

### Corrective-family blocker

If all three bounded corrective candidates fail to improve both 90° and 130° without new problems, return:

**RP2 GRASK ELBOW CORRECTIVE FAMILY EXHAUSTED / AUTHOR DECISION REQUIRED**

Report whether the evidence most strongly points toward:
- helper-bone study;
- topology-density limitation;
- skinning-method limitation;
- or unresolved combination.

Do not reopen retopology or add helper bones without a new order.

### Frozen-parent mismatch

If a parent hash/rest-geometry mismatch is found:

**RP2 GRASK DIAGNOSTIC PARENT MISMATCH / STOP**

## 19. Required report

Create:

`reviews/claude-rac-rp2-grask-nail-criterion-elbow-corrective-gate.md`

Evidence:

`reviews/rac-rp2-evidence/grask_rig_diagnostic_v004/`

Update narrowly:
- `reviews/claude-session-handoff.md`;
- `specs/STATUS.md`.

Record:
- N-1 through E-3 rulings from this order;
- new nail criterion version;
- corrective candidate definitions;
- selection/rejection;
- topology-density audit;
- knee verification;
- full-suite result if triggered;
- exact unresolved failures.

## 20. Scope

No retopology edit.
No rest-shape edit.
No production-rig freeze.
No production-weight freeze.
No facial/oral component work.
No morphs.
No UV/material/LOD work.
No UE5 integration.
No next race.

After the required return, **STOP FOR CHATGPT REVIEW**.
