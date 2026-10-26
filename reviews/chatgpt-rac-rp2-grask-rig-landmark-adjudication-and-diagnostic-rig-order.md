# RAC RP2 — Grask rig-landmark adjudication + diagnostic-rig execution order

**Date:** 2026-10-25  
**Authority:** Tyler / ChatGPT author review after Claude rig-preparation readiness proposal v001.  
**Parent:** `reviews/claude-rac-rp2-grask-rigprep-readiness-gate.md` (commit `2558dc0f1216246524f3359d367b39c72ebe7c8b`).  
**Frozen retopo:** `GR_U_REF_RP2_retopo_v003.blend` — AUTHOR ACCEPTED / FROZEN / CLOSED.  
**Purpose:** adjudicate AD-R1…AD-R12, produce a versioned author-approved diagnostic landmark package, then build and execute a **derived diagnostic rig only** to validate deformation topology. This is **not final production rigging** and does not reopen anatomy.

---

## 1. Immutable parents and hard firewall

The following remain immutable:

- `GR_U_REF_RP2_retopo_v003.blend`
  - SHA-256 `03bfe7d924ff5b8b61a4c10095af5d16ca29d41667d7f61d0abeca14e1f07ce0`
  - geometry hash `f9c4a7ac98e86d98017376b9d67c85428503d2d6385258471d99bc766bfe702f`
- `GR_U_REF_RP2_SOURCE_3D_v005.blend`
  - SHA-256 `7bba8d2d5f081c077351b2e79e7e5fcce91b4f376cd6b2cfc76f1c2eb052ab14`
  - geometry hash `2697929d90c9ed708997a594502a4d5edeaebb8f4ae39deefcc0802dc7c1d7bc`
- v001/v002 provenance, v003 sidecar, v003 landmark package, freeze record, seam proposal, identity/deformation-loop data.

Before and after all work, verify parent hashes. Stop immediately on mismatch.

**Do not:**
- edit, resave, reproject, smooth, symmetrise or otherwise alter the frozen v003 or v005 parents;
- create v004 retopology;
- reopen the accepted thumb-web anatomy or ring–pinky quad exception;
- reinterpret this order as final skeleton-family selection, production skinning, animation, creator morphs, UV/material/LOD work or UE5 integration.

All armature, weight and pose work must occur only in a new derived diagnostic file.

---

## 2. Author ruling on the readiness gate

Claude's finding is accepted:

> The frozen surface is sufficient for retopology validation but does not uniquely determine every internal joint centre.

That is **not** a defect in the accepted Grask mesh. Do not modify source anatomy merely to expose or manufacture bony landmarks.

For the diagnostic skeleton, internal centres may therefore be **author-placed rigging landmarks** when the source surface cannot determine a biological centre. They must be labelled `manual-author-rig` (or an equivalently unambiguous provenance class), with the construction rule recorded. Do not call such points measured anatomy.

The v001 readiness proposal remains evidence/provenance, not the final diagnostic landmark definition.

---

## 3. AD-R1 — hip centres: AUTHOR DECISION

Use a manual diagnostic centre based on the **v001 consensus region**, not the old frozen E3 value alone and not the inguinal-axis alternative alone.

Target the v001 consensus:
- L approximately `(12.11, 2.85, 119.03) cm`
- R approximately `(-12.11, 2.76, 119.16) cm`

Claude may make only a small fitting adjustment (maximum 5 mm) if required to place the centre on the proximal thigh load axis while preserving the separately measured left/right anatomy.

Record the exact final coordinates and the adjustment reason.

Do not mirror the two sides into a synthetic symmetric pair.

---

## 4. AD-R2 — knee and ankle centres / axes: AUTHOR DECISION

### Knee
Use the v001 consensus level:
- L approximately z `71.17 cm`
- R approximately z `71.20 cm`

Place AP/ML at the local limb-section centreline at that level. A maximum 5 mm adjustment is allowed for section-centre consistency.

Use a mediolateral flexion axis for the diagnostic test.

### Ankle
Use the v001 consensus / anterior-crease level rather than the old low frozen value:
- L approximately z `13.50 cm`
- R approximately z `13.75 cm`

Place the centre on the distal-shin/ankle section centreline.

For this diagnostic stage, **accept a mediolateral ankle axis with no invented talocrural obliquity**. The source provides no reliable malleolar evidence for an oblique anatomical axis.

Label the ankle axis as a diagnostic engineering axis, not a biological canon statement.

---

## 5. AD-R3 — glenohumeral centres: AUTHOR DECISION

Reject the large sphere fits as direct humeral-head centres; Claude already showed that those fits are dominated by the broad deltoid/trapezius mass.

Do not simply reuse the old frozen E3 point either.

Create a reproducible **manual author rig centre** per side using this rule:

1. anchor from the accepted acromion surface marker;
2. establish the proximal upper-arm shaft centreline from free upper-arm sections below the axillary contact;
3. extrapolate that shaft centreline superiorly;
4. choose the diagnostic GH centre on that extrapolated line approximately **3.5–4.5 cm inferior to the acromion**, with AP position following the proximal arm section centroid rather than the deltoid sphere centre;
5. ensure the point remains internal and gives a plausible shoulder lever arm without pulling the centre into the torso.

Preserve the documented left/right shoulder-line asymmetry. **No symmetry enforcement.**

Return exact coordinates, acromion-to-GH distance, surface depth and L/R comparison.

If the rule cannot be satisfied because the extrapolated shaft misses the shoulder mass, STOP and report the contradiction rather than inventing a different rule.

---

## 6. AD-R4 — elbow centres: AUTHOR DECISION

Use the cubital/waist region, not the old high frozen value.

Target:
- L approximately z `142.77 cm`
- R approximately z `142.99 cm`

Place the centre on the local upper-arm/forearm hinge intersection derived from the reference stance.

Retain the proposed mediolateral bend-axis logic from v001.

Maximum local fitting adjustment: 5 mm.

---

## 7. AD-R5 — sternoclavicular centres: AUTHOR DECISION

Do not use the old point approximately 10 cm behind the anterior skin summit.

Use the jugular-notch / clavicular surface summit as the anchor and place the diagnostic SC centre **3.0 cm inward/posterior from that local anterior surface anchor**, following the local AP direction.

This is a manual rigging landmark, not a surface-measured anatomical joint.

Record:
- surface anchor;
- inward direction;
- exact 3.0 cm placement;
- resulting distance to GH and acromion;
- L/R asymmetry.

If 3.0 cm would place the point outside the torso on either side, use the deepest valid point up to 3.0 cm and report it.

---

## 8. AD-R6 — spine architecture: AUTHOR DECISION

Keep the frozen `spine_01`, `spine_02`, `spine_03` records unchanged as provenance/reference markers.

For the diagnostic rig, add **three new thoracic stations** between `spine_03` and `neck_base`:

- `thoracic_01`: approximately 25% of the vertical interval;
- `thoracic_02`: approximately 50%;
- `thoracic_03`: approximately 75%.

At each station:
- use the torso cross-section centroid for AP/ML placement;
- preserve source asymmetry rather than forcing x = 0 if the section centroid is measurably offset;
- record exact source-frame and Blender-frame coordinates.

The purpose is to eliminate the approximately 39 cm single thoracic span while leaving the frozen landmark file untouched.

The diagnostic axial chain is therefore:
`pelvis -> spine_01 -> spine_02 -> spine_03 -> thoracic_01 -> thoracic_02 -> thoracic_03 -> neck_base -> head_pivot`.

These added stations are rig-prep controls, not newly declared biological vertebrae.

---

## 9. AD-R7 — root / pelvis architecture: AUTHOR DECISION

Preserve the existing production origin exactly.

Define two separate rig concepts:

1. **root_motion / world root:** at the production origin on the ground plane, `(0,0,0)` in the production analysis frame.
2. **pelvis:** use the v001 internal pelvis proposal approximately `(0.00, 2.80, 123.93) cm`, with maximum 5 mm section-centroid fitting adjustment.

The offset between world root and pelvis is intentional.

Do not move the mesh, origin or frozen pelvis-root reference to make these coincide.

---

## 10. AD-R8 — jaw and eyes: AUTHOR DECISION

### Eyes
Keep the validated eye centres as rig-facing reference points. They may be included as **non-deforming diagnostic eye joints / aim centres** only.

Do not create eyeball geometry in this order. Do not weight the body mesh to eye joints.

### Jaw
Do **not** build or weight a jaw joint in the diagnostic rig.

The current closed sculpt has no oral cavity or mandible support. The existing jaw-hinge entries are placeholders only.

Mark functional jaw deformation as **DEFERRED — REQUIRES FACIAL/ORAL COMPONENT STAGE**.

This does not block body deformation diagnostics.

The eventual Wayfarer production character is expected to support facial animation, so jaw/eye component work remains required before final character production handoff; it is simply outside this order.

---

## 11. AD-R9 — scapular medial-border proxy: AUTHOR DECISION

Do not pretend the source exposes a measurable scapular medial border.

Create an explicitly manual **rigging proxy**, not an anatomical landmark:

`scapula_medial_proxy_l/r`

Construction rule per side:
1. use the accepted acromion and existing scapular inferior proxy;
2. on the posterior body surface, locate the vertical level 60% of the way from the inferior proxy toward the acromion;
3. at that level, take a transverse target 45% of the distance from posterior midline toward the acromion's x position;
4. project that target to the posterior source surface;
5. store the result as `manual-author-rig-proxy`.

This point exists only to support shoulder-girdle diagnostic mechanics. It is not canon bony anatomy.

Return a visual sheet showing the acromion, inferior proxy, medial proxy and GH centre together.

---

## 12. AD-R10 — local-axis convention: AUTHOR DECISION

For this **diagnostic rig**, approve the v001 convention:

- right-handed local frames in Blender;
- local X = flexion axis;
- X oriented toward subject-left (+X analysis) on both sides;
- Y = toward child joint;
- Z = X × Y;
- retain the v001 flexion-sign definitions.

This convention is approved only for diagnostic consistency.

Do not claim it is the final UE5 production-skeleton orientation policy. That remains a later rig-contract decision.

---

## 13. AD-R11 — jaw-hinge provenance correction: AUTHOR DECISION

Do not edit the frozen v003 landmark package.

In the new versioned diagnostic package, correct the provenance of `jaw_hinge_l/r` from copied construction to a clearly labelled rule-based placeholder / deferred facial landmark.

Retain the old frozen entry exactly as historical provenance.

---

## 14. AD-R12 — diagnostic deformation thresholds: AUTHOR DECISION

Approve the v001 D1–D10 diagnostic suite and its proposed thresholds as **engineering diagnostics**, with these clarifications:

- a failed pose does not automatically invalidate the retopology; first classify the cause as topology, joint placement, diagnostic weights, source-contact anatomy or test setup;
- accepted source hollows and documented contact regions remain exclusions;
- automatic/diagnostic weights are not production weights;
- no range-of-motion angle in the test suite becomes biology canon;
- do not "repair" a failed diagnostic by editing the frozen retopo.

Retain:
- 0 non-contact intersections;
- no new flipped faces;
- no new pathological folds outside declared crease/contact zones;
- per-zone volume targets from v001;
- wrist/ankle/joint-loop spacing checks;
- nail rigidity check;
- rest-return T-1/T-6 verification.

---

## 15. Required versioned landmark deliverable

Create a new package, never replacing frozen data:

`GR_U_REF_RP2_rigprep_landmarks_v002.json`

and readable `.md` / `.csv` tables.

Every record must contain:
- stable ID;
- provenance class;
- source-frame cm coordinate;
- production-frame cm coordinate;
- Blender metres;
- local frame where applicable;
- parent/child;
- segment length;
- construction rule;
- uncertainty / limitation;
- whether it is suitable for diagnostic rigging, final production carry-forward, or deferred.

The v002 package must clearly distinguish:
- frozen surface markers;
- copied construction joints;
- manual author rig centres;
- manual rigging proxies;
- deferred facial placeholders.

No record may gain false anatomical certainty merely because it has an exact coordinate.

---

## 16. Diagnostic rig execution — AUTHORIZED AFTER v002 LANDMARK VALIDATION

After the v002 landmark package is generated and internally validated against this order, create a derived file:

`GR_U_REF_RP2_rigdiag_v001.blend`

Do not overwrite or save over v003.

The diagnostic rig may include:
- world/root bone;
- pelvis;
- hip/knee/ankle/ball/toe chains;
- SC / clavicle / scapular-proxy / GH / elbow / wrist / hand/finger chains;
- spine_01–03 + thoracic_01–03 + neck/head;
- non-deforming eye aim/reference joints.

Do not include functional jaw deformation.

Use diagnostic automatic/envelope/heat weights as a starting point. Minimal normalization or cleanup needed to make the test executable is allowed **only in the diagnostic copy** and must be logged. Do not spend this stage hand-authoring production-quality weights.

---

## 17. Execute D1–D10

Run the v001 proposed diagnostic suite:

- D1 shoulder elevation / axillary clearance;
- D2 elbow flexion;
- D3 wrist;
- D4 finger curl / spread;
- D5 thumb opposition;
- D6 hip flexion / abduction;
- D7 knee flexion;
- D8 ankle / toes;
- D9 trunk twist / flexion;
- D10 neck.

For every pose:
- capture identical-camera clay + wire evidence;
- measure non-contact intersections;
- folds / flips;
- volume change;
- p95 edge strain;
- loop-spacing collapse;
- rest-return T-1 / T-6;
- classify every failure by likely cause.

Also capture explicit shoulder and pelvis closeups showing whether the new manual joint placements produce a better mechanical read than the rejected/old alternatives.

Do not tune the frozen mesh to pass.

If joint placement is clearly wrong, adjust **only the v002/v003 diagnostic landmark proposal and derived rig**, record the revision, and keep all frozen parents untouched.

Limit this order to at most **one bounded diagnostic landmark revision** (`rigprep_landmarks_v003`) if a placement is mechanically untenable. If a second revision would be needed, STOP for ChatGPT review.

---

## 18. Acceptance logic

This order is successful if:

1. all immutable parent hashes remain unchanged;
2. the v002 adjudicated landmark package follows every author ruling above;
3. diagnostic rig construction is reproducible and isolated from frozen assets;
4. D1–D10 evidence is complete;
5. failures are honestly classified rather than hidden through mesh edits;
6. no final-rig or UE5 claims are made.

A diagnostic failure is **not** permission to reopen v003.

If a failure appears to prove that accepted topology itself cannot deform adequately even with a plausible joint and reasonable diagnostic weights, document it and STOP for author review.

---

## 19. Required return

Commit:

1. `reviews/claude-rac-rp2-grask-rig-landmark-adjudication-diagnostic-gate.md`;
2. `GR_U_REF_RP2_rigprep_landmarks_v002.json` plus readable tables;
3. visual landmark sheets, including the new shoulder/scapular and thoracic-chain sheets;
4. diagnostic-rig manifest and exact file/hash record for `GR_U_REF_RP2_rigdiag_v001.blend`;
5. D1–D10 measurement outputs and visual evidence;
6. parent before/after hashes;
7. reproducible tools/scripts;
8. narrowly scoped STATUS/handoff update.

The return report must state:
- which author rulings were implemented;
- exact final joint coordinates;
- whether a bounded landmark revision was needed;
- pass/fail per diagnostic pose;
- failure classification;
- whether any result suggests a true topology problem versus diagnostic rig/weights/placement;
- the next decision needed from ChatGPT.

After committing the package, **STOP FOR CHATGPT REVIEW**.

Do not proceed to:
- final production skeleton;
- production skin weights;
- facial/oral mesh changes;
- creator morphs;
- UV/material work;
- LODs;
- UE5 integration;
- another race.

---

## FINAL AUTHOR RULING

**Grask RP2 retopology remains accepted, frozen and closed.**

Proceed with the author-adjudicated diagnostic landmark package and one isolated diagnostic-rig/deformation validation cycle only.

No source-anatomy reopening is authorized.
