# RAC RP2 — Grask elbow helper-volume study + shoulder failure-isolation order

**Date:** 2026-10-26  
**Authority:** Tyler / ChatGPT review of Claude return `95cf74745f3783f7eeb6ad39f23e26e29f651f33`.  
**Parent gate:** `reviews/claude-rac-rp2-grask-nail-criterion-elbow-corrective-gate.md`.  
**Status entering this order:** Grask RP2 retopology remains AUTHOR ACCEPTED / FROZEN / CLOSED. Production deformation is **not accepted**.

This order records the author rulings on C-1…C-5 and K-1, then authorizes one bounded elbow helper-joint / volume-preservation study. If and only if the elbow study reaches the acceptance conditions below without regressions, proceed directly to a bounded shoulder failure-isolation study. Otherwise stop after the elbow study for ChatGPT review.

---

## 1. Immutable parents / firewall

Do not edit, resave over, reproject, smooth, retopologize, symmetrise, or otherwise change:

- `GR_U_REF_RP2_retopo_v003.blend`
- `GR_U_REF_RP2_SOURCE_3D_v005.blend`
- frozen v003 sidecars / landmarks / freeze record
- v001 / v002 retopo provenance
- previously returned diagnostic rigs and evidence packages

The accepted rest mesh remains exactly the frozen v003 geometry.

No v004 retopology is authorized.

No production rig, final weights, creator morphs, facial/oral work, UVs, materials, LODs, UE5 integration, animation, or another race is authorized.

---

## 2. Author rulings on the latest gate

### C-1 — elbow volume

The C2 elbow corrective is accepted as **diagnostic proof that the existing topology can deform materially better**, but its volume loss is **not accepted as production deformation quality**.

Do not promote C2 unchanged as a final production solution.

Do not continue the rejected C3-style simple side bulge.

Authorize one bounded study using a small helper-joint / helper-bone volume mechanism combined with a lighter pose-space corrective.

The goal is not to force exact rest volume at all costs. The goal is to preserve believable elbow / upper-forearm / distal-biceps mass while retaining the C2 gains in intersection removal, loop spacing and crease behavior.

### C-2 — DQS

Do **not** author DQS-specific elbow keys in this order.

Keep LBS as the diagnostic skinning baseline for the elbow study.

DQS remains comparison evidence only. Do not select the final Wayfarer skinning policy here.

### C-3 — right-side support extent

The asymmetric right support extent is accepted.

The right contact region reaches farther than the left; therefore a right support of approximately 21 cm is allowed where the left remains approximately 18 cm.

Do not force mirrored support extents.

The exact-zero boundary guard remains mandatory.

### C-4 — strain / crease folds

The current C2 strain and in-crease folds are acceptable **for diagnostic comparison only**.

They are not a production-quality approval.

The helper-volume study should attempt to improve volume behavior without materially worsening:
- p95 strain;
- maximum strain;
- crease depth;
- loop spacing;
- orientation disagreement;
- local fold / inversion indicators;
- non-contact intersections.

### C-5 — next target

Primary target: elbow helper-volume preservation.

If the elbow helper study meets the acceptance conditions in §7, proceed to shoulder failure isolation.

If it does not, stop after the elbow study.

### K-1 — knee

Keep the **v002 knee placement** as the diagnostic baseline.

Do not promote the bounded v003 knee placement.

No further knee work in this order.

---

## 3. Nail state

Nail Plate Rigidity v2 is accepted as the current gating definition.

Nail Cap Historical v1 remains report-only.

Do not modify nail weights or geometry in this order unless the helper/shoulder work unexpectedly regresses Nail Plate v2. If that happens, report the regression and stop rather than compensating elsewhere.

---

# STAGE A — ELBOW HELPER-VOLUME STUDY

## 4. Baseline

Use:

- v002 diagnostic landmarks;
- W0 baseline weights;
- LBS;
- left C2 and right C2rx as the corrective comparison baseline;
- identical elbow pivots and test poses;
- the frozen v003 rest mesh.

Build a new derived diagnostic branch/file only.

Recommended name:

`GR_U_REF_RP2_rigdiag_v005.blend`

The Basis/rest geometry must remain byte/geometry-equivalent to frozen v003.

---

## 5. Helper mechanism to test

Test one small helper-joint / helper-bone class per elbow side.

The helper is a diagnostic deformation aid, not final production skeleton canon.

### Required behavior

Use one helper transform for the distal upper-arm / proximal forearm contact-mass region per side, driven by elbow flexion.

The helper may:
- rotate partially with the forearm or upper arm;
- translate a small amount along the local bisector / outward mass-preservation direction;
- influence only the local elbow-volume support region;
- blend smoothly to zero outside its support;
- differ left vs right where the accepted source asymmetry requires it.

The helper must not:
- move the pivot;
- alter segment lengths;
- affect wrist/hand or shoulder/trunk regions outside the declared support;
- create rest-pose change;
- act when the elbow is below the activation threshold;
- conceal penetration by moving unrelated body areas.

### Activation

Use a smooth flexion-driven curve.

Suggested diagnostic activation:
- 0 at <=45°;
- progressive activation through 60 / 75 / 90°;
- stronger activation through 110 / 120 / 130°.

Do not introduce discontinuous keys or steps.

---

## 6. Candidate limit

At most **three** helper/corrective candidates are allowed:

- **H1:** helper only, no new pose-space corrective beyond the current baseline comparison.
- **H2:** helper + reduced-strength C2-style corrective.
- **H3:** one bounded refinement of H2, only if H2 exposes a specific localized failure.

Do not create a broad search tree.

Do not alter W0 baseline weights except for the helper's own declared local influence.

Every candidate must be reproducible from a committed config and tool path.

---

## 7. Elbow acceptance conditions

Compare W0, C2/C2rx, and H1/H2/H3 at:

- 45°
- 60°
- 75°
- 90°
- 110°
- 120°
- 130°

for both left and right where applicable.

A helper candidate may be selected only if:

1. **Rest / low-angle integrity**
   - 45° is bit-identical or numerically negligible to the accepted diagnostic baseline where activation is zero.
   - rest-return T-1 remains effectively zero.

2. **Intersections**
   - 0 non-contact intersections at 90°;
   - 0 non-contact intersections at 130°;
   - no new unrelated intersections at intermediate angles.

3. **Loop spacing**
   - >=0.50 of rest at 90–120°;
   - target >=0.50 at 130° on both sides;
   - if right 130° remains slightly below, it must materially improve over C2rx without worsening other criteria.

4. **Crease**
   - 90° crease depth <=2.0 mm;
   - 110–130° should be no worse than the currently selected C2/C2rx unless compensated by a major volume gain and visually better contact.

5. **Orientation / inversions**
   - no new local inversion faces relative to C2/C2rx;
   - orientation disagreement must not regress materially.

6. **Volume**
   - demonstrate a clear improvement over C2/C2rx closed-volume loss at 110–130°;
   - target at least **50% reduction in the corrective-caused closed-volume loss** at 130° relative to C2/C2rx;
   - the local cone/zone proxy should move toward the W0/DQS physical-volume behavior rather than farther away.

7. **Strain**
   - p95 strain should not increase by more than 5 percentage points over C2/C2rx at any tested angle;
   - max strain must be reported and visually localized.

8. **Boundary field**
   - helper influence and corrective deltas taper continuously to zero;
   - exact-zero support-boundary guard remains enforced;
   - no visible support seam.

9. **Visual read**
   - no ballooning, pipe-like elbow, biceps lump, flattened outer elbow, or artificial muscle bulge;
   - preserve the Grask's accepted long-limbed anatomy;
   - the inner contact at deep flexion should read as soft-tissue compression/contact, not interpenetration.

If no candidate meets these conditions, **do not invent more helpers or edit topology**. Stop and report the best candidate and the limiting failure.

---

## 8. Required elbow evidence

Provide:

- identical-camera clay and wire sheets at 90° and 130°;
- left and right;
- W0 vs C2/C2rx vs selected helper candidate;
- flexion-plane cross-sections;
- helper influence/weight field sheet;
- activation curve;
- closed-volume comparison;
- zone/cone-volume comparison;
- loop-spacing plots;
- non-contact / crease intersection overlays;
- orientation / local-inversion overlays;
- p95/max strain tables;
- rest-return check.

Explicitly state whether the helper reduced volume loss by >=50% at 130°.

---

# STAGE B — SHOULDER FAILURE ISOLATION
## Execute only if Stage A passes §7

## 9. Scope

Do not solve the entire shoulder in this order.

Perform a **failure-isolation study** on the existing W0 baseline to identify whether the remaining D1 shoulder/girdle failures are primarily caused by:

- GH placement;
- clavicle / scapular proxy mechanics;
- missing scapular rotation;
- diagnostic weighting;
- axillary contact handling;
- topology / loop compression;
- test criterion classification.

Use the already accepted v002 diagnostic landmarks unless a direct contradiction is proven.

No new source anatomy.

---

## 10. Shoulder tests

Focus on:

- abduction 45°;
- abduction 90°;
- flexion 90°;
- extension 30°;
- girdle-enabled 90° abduction/flexion variants already present in the suite.

Run left and right separately.

At minimum compare:

1. current W0 shoulder behavior;
2. one **scapular/clavicular motion-enabled diagnostic variant** using the existing manual scapular proxies;
3. one bounded weight-only comparison only if needed to separate mechanics from weighting.

No more than two new shoulder candidates.

Do not build production-quality shoulder weights.

---

## 11. Shoulder measurements

For each tested pose report:

- non-contact intersections;
- axillary contact/intersection depth;
- orientation disagreements;
- local inversions;
- folds outside intended crease/contact zones;
- loop-spacing collapse;
- p95/max strain;
- local volume proxy;
- acromion/GH relationship;
- scapular-proxy displacement and rotation;
- clavicle motion;
- visible deltoid/axillary contour continuity.

Include identical-camera:
- front;
- rear;
- three-quarter;
- axillary closeup;
- wireframe;
- shoulder cross-section or contour plot where useful.

---

## 12. Shoulder classification

Return one of:

- **MECHANICS-DOMINANT** — scapular/clavicular motion substantially fixes the failure with existing topology;
- **WEIGHTING-DOMINANT** — local weighting change fixes it without new topology;
- **JOINT-PLACEMENT-DOMINANT** — accepted diagnostic landmark placement is mechanically implausible;
- **TOPOLOGY-CONTRIBUTING** — persistent collapse remains after plausible mechanics/weights;
- **MIXED / INCONCLUSIVE**.

Do not reopen retopology merely because the classification is TOPOLOGY-CONTRIBUTING. Stop for ChatGPT review.

---

## 13. Full-suite regression check

If an elbow helper candidate is selected:

- run the unchanged full 43-pose suite;
- confirm all inactive poses remain bit-identical or numerically negligible to the baseline;
- report pass count;
- report every fixed, regressed and unchanged criterion;
- retain Nail Plate v2 gating;
- retain v002 knees.

If Stage B is reached, shoulder candidates may be evaluated on their targeted D1 poses only unless their mechanism has non-zero influence elsewhere; if influence is non-zero elsewhere, run the relevant regression subset.

---

## 14. Required return

Commit:

1. `reviews/claude-rac-rp2-grask-elbow-helper-volume-shoulder-isolation-gate.md`;
2. elbow helper configs/tools and reproducible build;
3. `GR_U_REF_RP2_rigdiag_v005.blend` manifest/hash if built;
4. elbow Stage A tables and visual sheets;
5. full-suite regression result if a helper is selected;
6. shoulder Stage B isolation report/evidence only if Stage A passes;
7. immutable-parent before/after hashes;
8. narrowly scoped `specs/STATUS.md` and session handoff update.

The gate must explicitly state:

- whether any helper candidate met §7;
- whether the 130° closed-volume loss improved by >=50%;
- whether left/right helper extents differ;
- whether any new regression occurred;
- whether Stage B was executed;
- shoulder failure classification if Stage B was executed;
- the exact next decision required from ChatGPT.

---

## 15. Stop rules

STOP FOR CHATGPT REVIEW after this order.

Do not proceed to:

- final production rig;
- production skinning;
- further elbow helper proliferation;
- topology edits;
- facial/oral/eye component work;
- creator morphs;
- UV/materials;
- LODs;
- UE5;
- another race.

---

## FINAL AUTHOR RULING

- Grask RP2 retopology remains **ACCEPTED / FROZEN / CLOSED**.
- Nail Plate Rigidity v2 remains the gating nail criterion.
- C2/C2rx are retained as the elbow corrective comparison baseline, not final production deformation.
- v002 knee placement remains the diagnostic baseline.
- One bounded elbow helper-volume study is authorized.
- If that study passes, one bounded shoulder failure-isolation study is authorized.
- No source anatomy or topology reopening is authorized.
