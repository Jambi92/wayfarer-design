# ChatGPT Order — Saurin RP6 Production Rig / Skin-Weighting Pilot

**Repository:** `Jambi92/wayfarer-design`  
**Branch:** `main`  
**Frozen RP5 closure:** `fc1d99025a4f861a65119a52a76471b4f1e28960`  
**Freeze-record follow-up / PC verification:** `d35d0720be14c8cb1c37dde3885ffe646f46df5f`  
**Frozen record:** `reviews/rac-rp5-evidence/saurin/full_cage/final_consolidation/SAURIN_RP5_FREEZE.json`  
**Frozen topology:** `255645a12a8dc59ae8dace55dcf2af2b196a4f5a799fdf425b394b831ffb2d49`  
**Carry-forward register:** `specs/RAC_PRODUCTION_RIG_CARRY_FORWARD_REGISTER.md`  
**Production contract:** `specs/RAC_PRODUCTION_MESH_CONTRACT.md`  
**Saurin canon:** `specs/saurin/SAURIN_V1.md`

## Immediate instruction

Begin **Saurin RP6 — production rig / skin-weighting pilot** on the frozen RP5 topology.

This order authorizes rigging, production skin weights, bounded rig-driven corrective deformation, and deformation validation for Saurin only.

This order does **not** authorize any change to frozen RP5 geometry/topology, any UV/material work, LOD work, creator implementation, UE5 integration, or work on another race.

Work internally through ordinary rigging/weighting problems. Do not stop for routine technical choices. Submit only when your own audit reaches the RP6 pilot gate described below, unless a genuinely new author decision or external blocker is encountered.

---

# 1. Frozen RP5 is immutable input

Use exactly the frozen RP5 production references:

- `SA_M_REF_RP5_freeze_candidate_v001.blend`
  - SHA-256 `a37cc37723f1a25fed3320c972341883c05e7df30c4f6f44d112746c86880a07`
- `SA_F_REF_RP5_freeze_candidate_v001.blend`
  - SHA-256 `fd5dad4f3cc5ba598ba0f2198f062c8845f17f1317e948399398bc8e5c6403d7`
- cage NPZ SHA-256:
  `ca1c635c1c3c234cc675c2471a31cf9646f95b597c0896b93486cd2b57f99839`
- topology SHA-256:
  `255645a12a8dc59ae8dace55dcf2af2b196a4f5a799fdf425b394b831ffb2d49`
- accepted tail module:
  `559565cc28a89db67c559c6db899cee51af0e349614fcb466255a6b35156baab`

Before work begins, re-hash the frozen package.

At the end, re-hash it again.

Required result:

**frozen RP5 files unchanged.**

Do not:
- move frozen vertices;
- alter face order;
- add/remove topology;
- change semantic data;
- resave the frozen RP5 Blender files;
- overwrite the frozen production directory.

All RP6 files are new derived files with new names and hashes.

---

# 2. RP6 goal

The purpose of RP6 is to prove that the frozen Saurin topology can support a production-quality deformation system without reopening geometry.

The RP5 deformation work established:

- 34 diagnostic poses;
- 0 TOPOLOGY-classified poses;
- 0 topology-only flips;
- remaining problem classes belong to temporary weighting/scaffold behavior;
- PD-2 extreme-body failures are source/composition-owned, not cage-owned.

RP6 must replace the temporary diagnostic scaffold with a deliberate Saurin production-rig pilot and show that the major weighting/scaffold classes are either:

1. **CLEAN**, or
2. explicitly owned by a later non-RP6 system such as PD-2 composition, with no frozen-topology defect and no hidden rig regression.

The target is not merely “better than the temporary scaffold.” It is a credible production rig/weighting baseline.

---

# 3. Do not declare a universal skeleton

The global game skeleton hierarchy is not yet canonically frozen by the production mesh contract.

Therefore:

- build a **Saurin-specific RP6 production-rig pilot**;
- do not declare its hierarchy universal for all races;
- do not retrofit Saurin into the MPFB humanoid skeleton where anatomy requires otherwise;
- do not change other races to match Saurin;
- do not call the pilot a final engine skeleton.

However, the rig should be authored with later UE5 compatibility in mind:
- deterministic hierarchy;
- clean parentage;
- stable bone names;
- no circular constraints;
- no scale-dependent deformation tricks that cannot later be baked/exported;
- explicit distinction between deform bones, controls, helpers and diagnostic objects.

---

# 4. Reference stance and rig-prep stance

The frozen RP5 reference stance remains anatomy truth.

Create derived RP6 rigged copies only.

Do not freely reshape vertices into a rig pose.

If a rig-prep pose is used, generate it only through the armature from the frozen reference stance, consistent with `RAC_PRODUCTION_MESH_CONTRACT.md` §4.

Record:

- exact reference stance;
- exact rig-prep stance;
- shoulder abduction;
- elbow flexion;
- hand orientation;
- tail neutral state;
- any head/neck offset.

Required round trip:

reference → rig-prep → reference must reproduce the frozen reference body within numerical skinning tolerance and without a geometry edit.

---

# 5. Skeleton architecture pilot

Author a Saurin-appropriate hierarchy from frozen landmarks and semantic loops.

At minimum include production deformation coverage for:

## Root / axial
- world/root control structure as needed;
- pelvis/root deform hierarchy;
- lumbar / abdominal / thoracic spine chain;
- neck chain;
- head;
- clean root-motion separation from deform hierarchy.

## Shoulder / arms
Per side:
- clavicle / shoulder-girdle support as required;
- upper arm;
- forearm;
- hand;
- twist/distribution support only where justified by deformation evidence.

## Hands
Per hand:
- thumb chain;
- four finger chains;
- joints aligned to frozen semantic/landmark structure;
- enough articulation to validate fist, grasp and thumb opposition.

Do not add topology to accommodate the rig.

## Legs
Per side:
- thigh;
- shin;
- foot/ankle;
- ball/toe articulation appropriate to the accepted Saurin foot;
- twist/distribution support only where justified.

## Tail
Create a dedicated production tail chain.

Use the mesh-contract Saurin proposal of approximately **16 deform segments** as the starting hypothesis, not an immutable count.

Validate the count against:
- frozen tail ring spacing;
- curvature distribution;
- tail-root coupling;
- required bend/twist smoothness;
- weight stability.

A nearby count is allowed if the evidence demonstrates it is materially better.

Do not alter the frozen tail mesh to fit the chosen chain.

## Jaw / head
Provide:
- jaw hinge/deform articulation;
- mouth-corner / lower-face support as needed;
- rostrum and cranial-display geometry must remain structurally Saurin.

Do not create an independent “moving rostrum” unless the accepted Saurin anatomy explicitly requires one. Jaw motion must not make the rostrum read as mammalian muzzle deformation.

## Eyes / display
Use non-deforming anchors/helpers where useful.

Do not invent biological mobility for the cranial display merely because a rig can support it.

---

# 6. Joint placement

Derive joint centres/axes from the frozen RP5 landmark package, semantic loops and accepted Saurin source anatomy.

For each deform joint record:

- name;
- parent;
- head/tail position;
- local axes;
- source landmark(s);
- method:
  - source-derived;
  - loop/section fit;
  - centreline fit;
  - manually resolved from accepted geometry;
- configuration c1/c2 placement relationship;
- reason for any offset from a surface-derived centre.

Do not use visual convenience to shift joints outside anatomically defensible regions.

The c1 and c2 bodies may have different joint coordinates while sharing one hierarchy/naming architecture.

---

# 7. Bind / weighting method

Use a production-oriented deformation solution compatible with later engine export.

Primary baseline:

**Linear blend skinning with deliberate weights and bounded corrective support.**

Diagnostic DQS or other methods may be used to understand a failure, but do not make a non-exportable diagnostic deformation method the hidden production dependency.

For every zone:
- weights normalized;
- no unintended deform-bone influence;
- no disconnected weight islands;
- no unexplained left/right asymmetry on symmetric anatomy;
- no single-vertex spikes;
- no influence leaking across narrow web slots or opposite surfaces;
- preserve frozen semantic structures.

Document maximum influences per vertex and pruning policy.

Do not optimize weights by reducing accepted anatomy.

---

# 8. Corrective-deformation policy

Correctives are authorized when the frozen topology is sound and production weighting alone cannot preserve the accepted form through required motion.

Allowed:
- pose-driven corrective shapes;
- twist/distribution bones;
- helper deform bones;
- bounded volume-preservation correctives;
- contact/crease correctives;
- tail-root coupling correctives;
- jaw/mouth correctives.

Requirements:
- every corrective has an owning pose or continuous driver;
- every corrective is derived from the frozen RP5 mesh;
- neutral/reference value = exactly zero;
- disabling all correctives returns the unchanged bound frozen mesh;
- no corrective silently changes the reference anatomy;
- no corrective serves as a disguised topology repair.

Do not bake correctives into the frozen RP5 asset.

---

# 9. Priority carry-forward failure classes

The following RP5 weighting/scaffold classes are priority RP6 targets.

## Hands
- fist;
- grasp;
- thumb opposition.

The temporary LBS scaffold produced large flip counts in some of these poses.

RP6 must demonstrate that production weights/correctives remove the weight-owned failure class without creating:
- web-slot penetration;
- palm collapse;
- thumb-base inversion;
- finger interpenetration beyond deliberate contact;
- claw distortion.

## Shoulder
- abduction 90°;
- flexion.

Preserve:
- axillary vault;
- shoulder volume;
- neck/shoulder transition;
- no pinched inverted fold;
- no topology-class regression.

## Hip
- hip flexion;
- lower-trunk / pelvis interaction.

Avoid groin collapse, thigh/pelvis inversion and excessive volume loss.

## Tail root
- lateral bend;
- vertical bend;
- twist.

Preserve the frozen tail-root structure while producing a smooth pelvis-to-tail deformation field.

The tail must not behave like a rope merely because it has many bones.

---

# 10. Full 34-pose validation suite

Re-run the established RP5 34-pose suite on the RP6 production rig.

Include at least the already-established classes:

- jaw;
- neck flexion / extension;
- neck/head rotation;
- shoulder abduction 45°;
- shoulder abduction 90°;
- shoulder flexion;
- elbow 90°;
- elbow 130°;
- wrist motion as already represented;
- fist;
- grasp;
- thumb opposition;
- hip flexion;
- knee motion;
- ankle motion;
- toe flexion;
- toe extension;
- trunk twist;
- lower axial flexion;
- tail-root lateral bend;
- tail-root vertical bend;
- tail twist;
- all other established RP5 diagnostic poses needed to total the accepted 34-pose set.

Use the exact RP5 pose definitions where they already exist so before/after comparison is meaningful.

Do not quietly reduce pose severity to obtain a pass.

---

# 11. Four-step ownership audit remains mandatory

For every pose, preserve the existing ownership logic.

Compare at minimum:

1. frozen reference topology / source condition;
2. diagnostic/simple weighting baseline;
3. RP6 production weights;
4. RP6 production weights + authorized correctives.

Classify every residual as:

- CLEAN;
- RIG/WEIGHTING;
- SOURCE/POSE;
- CONTACT/SETUP;
- COMPOSITION/PD-2;
- TOPOLOGY.

Required topology result:

- **0 TOPOLOGY-classified poses**
- **0 topology-only flips**

RP6 target for the production rig:

- **0 RIG/WEIGHTING-owned inverted/folded faces in the required 34-pose suite after authorized correctives**
- no new self-intersection class caused by rigging
- no unexplained regression versus RP5

If a residual is intentionally accepted under SOURCE/POSE, CONTACT/SETUP or COMPOSITION/PD-2, prove ownership numerically and visually.

Do not relabel a rig failure to pass the gate.

---

# 12. Deformation-quality measurements

Flips alone are not sufficient.

For every major joint/pose report:

- signed / relative face orientation;
- self-intersections;
- local edge stretch/compression;
- local area change;
- joint-volume change;
- crease quality;
- landmark displacement;
- silhouette stability where relevant.

Create specific metrics for:

- axillary volume;
- elbow volume;
- wrist/palm volume;
- thumb-base volume;
- hip/groin volume;
- knee volume;
- ankle/foot contact;
- tail-root cross-section and curvature continuity;
- jaw/rostrum silhouette.

Use the frozen neutral body as the baseline.

Do not invent universal numerical limits without evidence. Establish pilot thresholds from:
- neutral-to-pose behavior;
- source/diagnostic comparison;
- visible failure onset;
- consistency across c1 and c2.

Report the chosen thresholds and why they are appropriate.

---

# 13. Tail-specific gate

The tail is mandatory Saurin anatomy and requires its own rig gate.

Validate:

- neutral;
- lateral bends at multiple amplitudes;
- vertical up/down bends;
- S-curve;
- distributed twist;
- combined bend + twist;
- root-biased motion;
- mid-tail-biased motion;
- distal-tail motion.

Required:
- no root collapse;
- no pelvis tearing;
- no hard kink at bone boundaries;
- no corkscrew volume failure;
- no tail inversion;
- no topology-class failure;
- smooth centreline curvature;
- acceptable cross-section retention;
- accepted tail module geometry unchanged in neutral.

Record the selected tail-segment count and why.

---

# 14. Hand-specific gate

For each configuration and each hand:

Validate:
- open hand;
- relaxed curl;
- full fist;
- cylindrical grasp;
- broad grasp;
- thumb opposition to each relevant digit reach;
- finger splay;
- combined opposition + curl.

Required:
- web spaces remain correctly owned;
- no opposite-wall weight leakage;
- no palm collapse;
- no thumb-base inversion;
- no claw inversion;
- contact may occur, but penetrations must be distinguished from intentional contact;
- no new fold class.

Produce close-up wire/weight/pose evidence.

---

# 15. Foot / toe gate

Validate:
- neutral plantigrade support;
- toe flexion;
- toe extension;
- foot roll / ball articulation if within the pilot;
- ankle flexion/extension;
- combined ankle + toe movement.

Preserve:
- accepted plantigrade contact logic;
- claws;
- forefoot topology;
- ankle transition;
- no sole collapse or unintended loss of ground-contact capability.

---

# 16. Jaw / mouth / head gate

Validate:
- jaw open at small / medium / large diagnostic angles;
- jaw lateral/forward motion only if anatomically supported;
- head yaw/pitch/roll;
- jaw + head combinations.

Required:
- jaw hinge anatomically plausible;
- no rostrum collapse;
- no orbit distortion from jaw weighting;
- no mouth-corner tearing;
- no throat inversion;
- cranial display remains structurally stable unless intentionally given approved mobility.

This is rig readiness, not facial-animation finalization.

Do not build the complete facial-animation system in RP6.

---

# 17. c1 / c2 rig relationship

Use one shared Saurin hierarchy/naming architecture where anatomy permits.

Validate both:
- SA-M188;
- SA-F188.

Do not assume c1 weights can simply be copied to c2 without audit.

Allowed:
- transferred initial weights using shared topology;
- c2-specific weight refinement;
- c2-specific joint coordinates;
- c2-specific corrective amplitudes where justified.

Required:
- same semantic bone roles;
- same core hierarchy;
- explicit record of every c1/c2 difference.

Avoid configuration-specific topology or neutral geometry.

---

# 18. PD-2 creator-state interface

RP6 does not implement the character creator.

However, the rig must be tested against the existing accepted PD-2 creator-state evidence.

At minimum re-check the 19 accepted states using the RP6 rig assumptions where technically meaningful.

The key extreme states include:
- high fat;
- high muscle;
- muscle + fat;
- Narrow + high fat and other previously problematic accepted states.

Do not reduce accepted creator ranges.

Classification rule:

If the unsurfaced creator body itself folds before rig deformation, that remains **COMPOSITION/PD-2**, not a rig defect.

But RP6 must not add additional rig-owned failure on top of it.

Produce a clear interface requirement for the future composition solver:
- what geometry/state it must deliver before rig deformation;
- what rig/weight assumptions depend on that clean input;
- what tests must be rerun once PD-2 is solved.

---

# 19. PD-1 / scale-detail interface

Do not implement final scale-field transport in RP6.

But verify that rig deformation does not make the existing PD-1 problem worse by design.

Record:
- which rig deformation outputs the later relief transport must consume;
- whether normals/tangent frames must be recomputed after deformation;
- where deformation-aware detail transport will be required;
- no assumption that static neutral normals are valid under extreme flexion.

Do not bake scales into the RP6 rig mesh.

---

# 20. Rig data outputs

Create a new RP6 evidence tree, recommended:

`reviews/rac-rp6-evidence/saurin/rig_pilot/`

Create new production-derived files, recommended:

- `SA_M_REF_RP6_rigpilot_v001.blend`
- `SA_F_REF_RP6_rigpilot_v001.blend`
- `SA_RP6_skeleton_v001.json`
- `SA_RP6_joint_placement_M_v001.json`
- `SA_RP6_joint_placement_F_v001.json`
- `SA_RP6_weights_M_v001.npz` or equivalent explicit portable representation
- `SA_RP6_weights_F_v001.npz`
- `SA_RP6_correctives_v001.json`
- `SA_RP6_pose_suite_v001.json`
- `SA_RP6_deformation_audit_v001.json`
- `SA_RP6_rig_manifest_v001.json`

The exact internal format may vary if Blender data require a better representation, but the package must be reproducible and auditable outside an in-memory Blender session.

Status for this pass:

**RP6 RIG PILOT / NOT FROZEN**

Do not call it final until we review the gate.

---

# 21. Blender file hygiene

Each RP6 Blender file must have a clearly documented object structure.

Record:
- mesh object;
- armature object;
- deform vs control bones;
- constraints;
- drivers;
- corrective shape keys;
- helper objects;
- modifiers;
- unit/scale state;
- external dependencies.

No hidden dependency on an uncommitted local file.

The frozen RP5 body geometry in neutral must be reconstructably identical inside the RP6 file before deformation.

If the rigged file stores float32 Blender coordinates, quantify read-back error exactly as RP5 did.

---

# 22. Weight audit

For both c1/c2 record:

- vertex group list;
- deform groups only;
- influence count histogram;
- max influences per vertex;
- weight-sum error;
- zero-weight vertices;
- orphan groups;
- symmetric-difference diagnostics;
- cross-surface leakage tests at:
  - finger webs;
  - toe webs;
  - axilla;
  - groin;
  - tail root;
  - mouth/throat.

Require:
- all body vertices intentionally weighted;
- normalized sums;
- no accidental influence islands;
- no opposite-wall leakage in narrow structures.

---

# 23. Corrective audit

For each corrective record:

- name;
- owning pose/driver;
- affected semantic regions;
- maximum neutral-space displacement;
- activation interval;
- c1/c2 behavior;
- reason;
- visual evidence;
- whether later UE export should use morph target, helper bone, or another equivalent implementation.

Require:
- neutral displacement exactly zero;
- no corrective active in reference stance;
- no global anatomy drift;
- no dependency loop.

---

# 24. Visual evidence package

Produce matched c1/c2 evidence for:

1. reference stance;
2. rig-prep stance;
3. skeleton overlay front/profile/3/4;
4. shoulder 45° / 90°;
5. elbow 90° / 130°;
6. fist;
7. grasp;
8. thumb opposition;
9. hip flexion;
10. knee;
11. ankle/toes;
12. trunk flex/twist;
13. tail lateral/vertical/twist;
14. jaw open;
15. worst residual pose before corrective;
16. same pose after corrective;
17. weight heatmaps for the priority failure regions;
18. corrective heatmaps where used;
19. c1/c2 comparison;
20. neutral overlay proving no RP5 geometry drift.

Where a residual is classified non-rig-owned, show the evidence that proves ownership.

---

# 25. Neutral identity preservation

Rigging must not change the frozen neutral model.

For neutral/read-back require:

- same topology hash as RP5;
- same vertex count;
- same face count;
- same face ordering;
- same semantic ownership;
- neutral mesh positions equal to frozen RP5 within Blender storage roundoff only;
- tail unchanged;
- accepted T-4/T-6 residuals unchanged.

Any unexplained neutral change is a FAIL.

---

# 26. Production-rig pilot acceptance gate

Claude should internally iterate until one of the states below is reached.

## PASS submission

Use exactly:

# **SAURIN RP6 PRODUCTION RIG / SKIN-WEIGHTING PILOT PASS — READY FOR CHATGPT / AUTHOR REVIEW**

Required for PASS:

- frozen RP5 package unchanged;
- RP6 neutral reproduces RP5;
- deliberate Saurin skeleton hierarchy documented;
- c1/c2 joint placements documented;
- production weights documented;
- full 34-pose audit completed on c1/c2;
- 0 TOPOLOGY-classified poses;
- 0 topology-only flips;
- 0 remaining **RIG/WEIGHTING-owned** fold/inversion class after authorized correctives in the required suite;
- priority hand/shoulder/hip/tail-root classes closed;
- tail-specific gate passed;
- hand-specific gate passed;
- foot/toe gate passed;
- jaw/head gate passed;
- PD-2 interface documented with no new rig-owned regression;
- neutral identity unchanged;
- Blender read-back passes;
- reproducible rig/weights/corrective package committed.

## Genuine author decision

Stop only if proceeding would require a new author decision about:
- Saurin anatomy/canon;
- frozen RP5 geometry/topology;
- biological mobility not previously defined;
- an unavoidable tradeoff that materially changes intended motion;
- a proposed skeleton structure that commits the entire game to a universal hierarchy;
- acceptance of a persistent rig-owned deformation defect.

## External blocker

Stop only for an unavailable required source/tool/permission that cannot be worked around without changing the authorized scope.

Do not submit ordinary “needs revision” checkpoints for fixable weighting work.

---

# 27. Internal audit before submission

Before returning PASS:

1. close and reopen both RP6 Blender files;
2. verify all rig objects and data from disk;
3. re-run neutral hash/geometry comparison;
4. re-run the full 34-pose suite;
5. re-run weight audit;
6. re-run corrective audit;
7. re-run tail/hand/foot/head special gates;
8. re-run c1/c2 comparison;
9. verify the frozen RP5 source hashes again;
10. verify no RP5 or previous frozen-race file changed;
11. verify no UV/material/LOD/creator/UE5 work was started;
12. update the Claude handoff with the exact RP6 state.

Do not rely only on in-memory Blender state.

---

# 28. Stop boundaries

Do **not**:

- alter or resave frozen RP5 production files;
- change RP5 topology;
- change RP5 neutral geometry;
- modify the accepted tail module;
- modify canonical W2I6 sources;
- reduce accepted Saurin creator ranges;
- solve PD-2 by narrowing biology;
- implement final scale-field transport;
- implement the full character creator;
- create final UVs/materials;
- generate LODs;
- perform UE5 integration;
- declare a universal game skeleton;
- rig another race;
- start another race-production phase.

After the RP6 pilot PASS submission:

**STOP FOR CHATGPT REVIEW.**

---

# FINAL AUTHORIZATION

Proceed with the **Saurin RP6 production rig / skin-weighting pilot** using the frozen RP5 topology as immutable input.

The pilot must replace the temporary deformation scaffold with a documented, production-oriented Saurin skeleton, weights and bounded correctives; close the known rig/weighting failure classes across the established 34-pose suite; preserve the frozen neutral model exactly; document the PD-1 / PD-2 interfaces; and stop at:

**SAURIN RP6 PRODUCTION RIG / SKIN-WEIGHTING PILOT PASS — READY FOR CHATGPT / AUTHOR REVIEW**
