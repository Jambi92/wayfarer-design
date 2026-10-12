# WAYFARER RAC — RM-OT-05M GORRUND RODIN/HYPER3D SOURCE-BODY RECOVERY + SURGICAL REFERENCE-SCULPT ORDER

**Status:** AUTHOR DECISION ISSUED — END THE MANNEQUIN/SDF ROUTE AND MOVE TO A HIGH-QUALITY SOURCE BODY  
**Parent block:** RM-OT-05L true reference-first free-sculpt gate  
**Decision:** RS1/RS2 are rejected as final concepts because the headless SDF-clay/stroke workflow cannot supply the required biological surface quality. Preserve the body-first / skeleton-later construction order, but begin from a high-quality Rodin/Hyper3D source body exactly as the successful Saurin workflow did.  
**Primary route:** Recover the existing prior **male Gorrund Rodin/Hyper3D body** from the Wayfarer project / local asset stores and use it as raw sculpt clay.  
**Fallback route:** If no suitable prior source exists, prepare and, only if the already-available Rodin/Hyper3D tooling is actually accessible, create one fresh source body from the current Gorrund canon.  
**Scope:** SOURCE RECOVERY / DIRECT SURGICAL SCULPT / CONCEPT VALIDATION / MEASUREMENT SCAFFOLD ONLY — NO UE5  
**Stop condition:** Stop at the RM-OT-05M author gate before canon promotion, Stage C, production rigging, creator implementation, D4, animation or UE5.

---

# 1. AUTHOR DISPOSITION OF RM-OT-05L

Accept RM-OT-05L as a valid capability diagnosis.

Final rulings:

- **RS1 — REJECT**
- **RS2 — REJECT**
- **True body-first / skeleton-later construction order — KEEP**
- **Gorrund canon — KEEP**
- **Gorrund body-only readability bar — KEEP**
- **SDF / primitive-clay blockout workflow — INSUFFICIENT FOR FINAL SOURCE ANATOMY**
- **Measurement scaffold — CORRECTLY NOT DERIVED**
- **Grask E3 — KEEP FROZEN**
- **Stage C — REMAINS BLOCKED**
- **RM-OT-05 — REMAINS OPEN**

Do not make RS3.

Do not continue trying to hand-build a finished biological body from ellipsoids/capsules/stroke grooves.

The problem is now source-surface quality, not construction order.

---

# 2. IMPORTANT SAURIN LESSON

The successful Saurin workflow was not:

> empty primitive clay → finished biological organism.

It was:

> **high-quality source body first → surgical canon correction → validation → scaffold derived afterward.**

Apply that same order to Gorrund.

The high-quality source is raw clay, not canon.

The accepted Gorrund body must still be determined by:

- GORRUND_V1;
- accepted comparative canon;
- RM-OT-05 negative evidence;
- author review.

---

# 3. FIRST ACTION — RECOVER THE EXISTING PRIOR MALE GORRUND SOURCE BODY

Before generating anything new, search the local Wayfarer project / source-asset directories for the **male Gorrund body previously produced through the Rodin/Hyper3D pipeline**.

The project history records a completed male Gorrund GLB in the earlier race-reference pipeline.

Search non-destructively for plausible:

- `.glb`
- `.gltf`
- `.fbx`
- `.obj`
- `.blend`

under likely locations including:

- Wayfarer project asset folders;
- RaceBodies source/export folders;
- Rodin / Hyper3D export folders;
- Downloads / staging folders previously used for race bodies;
- any preserved reference-mesh archive on the author PC.

Do not move or overwrite anything during discovery.

---

# 4. SOURCE RECOVERY MANIFEST

For every plausible Gorrund source candidate, record:

- absolute path;
- filename;
- file type;
- file size;
- modified time;
- SHA-256;
- vertex / face counts where readable;
- whether rigged;
- whether materials/textures exist;
- whether clothing / gear obscures the body;
- whether the mesh is male;
- whether topology appears intact;
- whether the body can be isolated from accessories;
- whether it visually corresponds to the prior Gorrund race-reference generation.

If more than one candidate exists, create a comparison sheet and select the strongest recoverable source.

Do not infer provenance only from filename.

---

# 5. SOURCE SUITABILITY GATE

The recovered source does **not** need to already be canon-perfect.

It does need enough real biological surface organization to support surgical correction.

A source is suitable if:

- it reads as a coherent living humanoid rather than a primitive blockout;
- muscle-over-bone continuity exists;
- pelvis/thigh, shoulder/arm, knee/shank, elbow/forearm and back transitions are organically modeled;
- the body is sufficiently visible for sculpting;
- the topology / mesh can survive direct editing;
- gross noncanonical features are correctable without rebuilding the organism from zero.

Reject as source if:

- clothing/armor hides the anatomy;
- body geometry is missing;
- topology is catastrophically broken;
- it is a stylized mannequin/blockout comparable to RS1/RS2;
- it is clearly the wrong race asset;
- it is female-only;
- the body is so far from Gorrund canon that correction would amount to a new full sculpt.

If a suitable prior male source is found:

> **USE IT. DO NOT GENERATE A NEW SOURCE.**

---

# 6. FALLBACK IF NO SUITABLE PRIOR SOURCE EXISTS

Only if no suitable prior Gorrund male source exists, build a **new source-generation package** from current canon.

The package must include:

- concise Gorrund physical brief;
- front / front-3/4 / side / rear-3/4 / rear generation guidance;
- body-only priorities;
- anti-targets learned from S1–S4, EA, RF and RS failures;
- neutral adult male;
- minimal sculpt-safe garment only;
- no armor;
- no gear;
- no cultural costuming;
- neutral stance;
- fully visible limbs;
- no exaggerated monster anatomy.

If the existing local Rodin/Hyper3D tooling/account/API is actually accessible, use it to produce a fresh source.

If it is **not** accessible:

> STOP after producing the source-generation package and exact instructions needed for the author to run the external generation.

Do not substitute another primitive/mannequin generator.

Do not claim the source exists if it does not.

---

# 7. SOURCE BODY IS RAW CLAY — NO OLD SKELETON CAGE

Once a suitable high-quality source exists, create a separate working copy.

Name the lineage:

- **GO-RD1-SOURCE** — untouched recovered/generated source;
- **GO-RD1-REF** — Claude's surgically corrected reference candidate.

Do not constrain GO-RD1-REF to:

- the old Gorrund skeleton;
- old joint centres;
- old 05F route;
- S1–S4 proportions;
- Marchfolk anatomy;
- RF1/RF2 metrics;
- RS1/RS2 blockout geometry.

Use old results only as negative/comparative evidence.

---

# 8. DIRECT SURGICAL SCULPT — CLAUDE REMAINS THE SCULPTOR

Claude is responsible for the actual Gorrund correction.

Use genuine direct/manual sculpting in Blender.

The source body may be altered substantially where canon requires it.

Allowed:

- proportional sculpt;
- local grab;
- smooth;
- flatten;
- crease;
- inflate/deflate;
- local remesh or topology cleanup if genuinely required;
- local anatomy reconstruction;
- local retopology if needed to make a region editable.

Do not preserve bad source anatomy merely because it came from Rodin/Hyper3D.

The source is a starting anatomical surface, not authority.

---

# 9. DO NOT IMPORT THE OLD FAILURES INTO THE SOURCE

Explicitly prevent recurrence of:

- rectangular / parallel-column torso;
- box/slab chest;
- barrel cylinder;
- obese-human deep-chest/belly read;
- hourglass/female-human torso read;
- bodybuilder V;
- bulb/knob knees;
- armor-like joints;
- hip outriggers;
- mannequin sausage limbs;
- featureless back;
- carved-groove pseudo-anatomy;
- Grask calf/forearm/reach cues.

These are now a formal Gorrund negative-reference set.

---

# 10. GORRUND REFERENCE ANATOMY TARGET

GO-RD1-REF must visibly express:

> **massive load-bearing non-human architecture with broad/deep axial structure, substantial joints, strong girdle/thorax integration, strong pelvis/femur support and a coherent axial-to-limb load path.**

The read must come from the organism as a whole.

It must remain:

- upright;
- plantigrade;
- adult;
- humanoid;
- tool-capable;
- five-digit;
- structurally massive independent of fat/muscle.

---

# 11. AXIAL / THORACIC SURGERY

Correct the source toward:

- broad/deep three-dimensional rib cage;
- anatomical radiused thoracic section;
- strong but non-armor costal organization;
- clear lower axial continuation;
- no parallel-column trunk;
- no pinched human waist;
- no chest block sitting on the pelvis.

The torso may have a real lower-axial minimum if organically supported.

Do not force any old waist ratio.

---

# 12. GIRDLE / NECK SURGERY

Correct toward:

- broad skeletal neck root;
- shoulder girdle carried by thorax;
- clavicle/scapula/upper-arm relationship that reads structurally;
- large shoulder articulation;
- no bodybuilder deltoid caps;
- no trap-driven breadth;
- no shoulder overhang;
- no hunch.

---

# 13. POSTERIOR / SACRAL SURGERY

Correct toward:

- broad posterior thoracic organization;
- continuous axial load path;
- coherent interscapular plane;
- substantial sacral platform;
- sacrum→hamstring transition;
- no soft gluteal dominance;
- no bodybuilder erector ridges;
- no carved grooves pretending to be anatomy.

---

# 14. PELVIS / FEMUR SURGERY

Correct toward:

- substantial pelvic depth;
- large hip articulation;
- strong proximal-femur support;
- coherent trochanteric/lateral-thigh organization;
- no lateral hip outriggers;
- no tiny human pelvis under a giant trunk;
- no armor shelf.

---

# 15. KNEE / SHANK / ANKLE SURGERY

Correct toward:

- large integrated knee;
- patellar/condylar/tibial-plateau structure;
- supportive shank with real taper;
- substantial ankle;
- large plantigrade foot.

Avoid:

- knee bulbs;
- knobs;
- pillar legs;
- tiny ankles;
- digitigrade cues;
- Grask high-calf identity.

---

# 16. ELBOW / FOREARM / WRIST / HAND SURGERY

Correct toward:

- substantial elbow integrated into the long bones;
- structurally scaled forearm;
- broad functional wrist;
- large capable hand.

Avoid:

- elbow knobs;
- cuff wrist;
- shovel hands;
- reach-dominant Grask forearm.

---

# 17. REFERENCE FIRST — DO NOT CREATE LOW TOO EARLY

Before LOW exists, GO-RD1-REF must pass an author-facing internal gate.

Produce:

- full body neutral grey;
- silhouette;
- front;
- front 3/4;
- profile;
- rear 3/4;
- rear;
- close trunk;
- close back;
- close pelvis/thigh;
- close knee/ankle;
- close girdle;
- close elbow/wrist.

Comparison sheet:

- Marchfolk;
- Skarn;
- Skarn Broad;
- Grask E3;
- S4;
- RF1;
- RS2;
- GO-RD1-REF.

Controls are visual only.

---

# 18. INTERNAL REFERENCE GATE

GO-RD1-REF must pass:

- coherent biological organism;
- not mannequin;
- not enlarged human;
- not rectangular;
- not boxy;
- not slab-sided;
- not barrel/cylinder;
- not obese;
- not bodybuilder;
- not ogre/monster;
- not Grask-like;
- load-bearing axial identity visible;
- posterior load path visible;
- pelvis→femur support visible;
- substantial joint scale visible;
- whole-body structural coherence.

If RD1 is close but has one coherent source-artifact problem, authorize one surgical revision:

- **GO-RD2-REF**

If RD2 still fails internally, STOP.

Do not create RD3 without a new author order.

---

# 19. CREATE THE LOW / LEAN COMPANION MANUALLY

Only after REF passes, create:

- **GO-RD1-LOW** or **GO-RD2-LOW**

This is a direct/manual lower-muscle, lower-fat sculpt of the same organism.

Do not use:

- Marchfolk composition deltas;
- the old Gorrund low algorithm;
- automatic radial shrink;
- uniform scale.

Preserve structural anatomy:

- thorax;
- girdle;
- pelvis;
- joint scale;
- sacral path;
- limb lengths;
- Gorrund identity.

LOW must look leaner, not like a different race.

---

# 20. REF↔LOW STRUCTURAL CONSISTENCY

Audit REF and LOW through anatomical landmarks.

Confirm:

- stature stable;
- major joint locations stable;
- limb lengths stable;
- thoracic architecture stable;
- pelvis/femur load path stable;
- joint scale stable;
- posterior load path stable;
- differences are genuinely composition-level.

If the source topology allows exact vertex correspondence, use it.

If not, use reproducible landmark measurements.

---

# 21. CONCEPT BLIND GATE

After REF and LOW pass internal review, run a fresh replicated blind concept gate.

Neutralize:

- head;
- face;
- hair;
- pigmentation;
- culture;
- gear.

Use matched display stature.

Controls include at minimum:

- Marchfolk;
- Skarn;
- Skarn Broad;
- Grask E3.

Use fresh uninformed scorers.

Do not reveal the candidate identity or design goal.

A valid pass requires:

- REF consistently separates from human-family controls;
- LOW remains the same group;
- REF+LOW group stably;
- Gorrund remains distinct from Grask;
- reasons are canon-legal structural organization.

---

# 22. BLIND REASON AUDIT

Accept reasons such as:

- axial load-bearing architecture;
- joint structural scale;
- thorax/girdle integration;
- pelvis/femur support;
- posterior load path;
- complete structural organization.

Reject a nominal pass if it is driven primarily by:

- boxy;
- rectangular;
- slab;
- fat;
- obese;
- muscular;
- giant;
- monster;
- armor;
- posture.

---

# 23. ONLY AFTER BODY PASS — DERIVE THE MEASUREMENT SCAFFOLD

If REF/LOW pass the concept gate, derive the scaffold **from the accepted source-derived body**.

Derive, where defensible:

- stature landmarks;
- shoulder centres;
- elbow centres;
- wrist centres;
- hip centres;
- knee centres;
- ankle centres;
- long-bone axes;
- thoracic stations;
- lower-axial stations;
- pelvic stations;
- sacral reference;
- hand/foot attachment points.

This is measurement-only.

Do not rig yet.

Do not deform the accepted body to match old joint positions.

---

# 24. CANON RECONCILIATION AFTER SCAFFOLD

Compare the accepted RD body against current Gorrund canon and old route evidence.

Classify each relationship:

- **PRESERVED**
- **PRESERVED IN DIRECTION**
- **NUMERIC REFERENCE UPDATED**
- **OLD ROUTE ARTIFACT**
- **TRUE CANON CONFLICT**
- **NOT YET MEASURABLE**

Do not silently rewrite canon.

Do not force the body back into a failed numeric route merely to preserve history.

True conflicts return to the author.

---

# 25. OLD SKIN PELVIC-DEPTH DIAGNOSTIC

Carry the 05K disclosure forward:

Old-route skin pelvic-depth/thoracic-depth diagnostics regressed during S2–S4.

Do not use those old skin readings as a rejection gate on the RD body.

Once the RD scaffold exists, remeasure the relation directly on the new body and classify:

- biological relation preserved;
- old surface diagnostic artifact;
- or true conflict.

No ruling is made before the new body exists.

---

# 26. NO STAGE C YET

Even if RD REF/LOW and scaffold pass:

Do not begin Stage C automatically.

First return the author gate so the new body-first lineage can be reviewed before pairing it with Grask E3.

Grask E3 remains frozen.

---

# 27. PROVENANCE

Preserve:

- recovered raw source;
- source hash;
- source provenance;
- untouched source copy;
- RD working .blend;
- RD REF;
- RD LOW;
- visual sheets;
- blind evidence;
- scaffold;
- all 05A–05L negative evidence.

Do not overwrite the source GLB/OBJ.

Do not overwrite old Gorrund candidates.

---

# 28. REQUIRED AUTHOR GATE

Return:

**`reviews/claude-rac-rm-ot-05m-gorrund-rodin-source-surgical-gate.md`**

State:

- **Prior male Gorrund source found — YES / NO**
- **Source provenance verified — YES / PARTIAL / NO**
- **Fresh external source generated — YES / NO / NOT NEEDED / BLOCKED**
- **Final source used — exact path/hash**
- **Final surgical reference — RD1 / RD2 / NONE**
- **Reference internal gate — PASS / FAIL**
- **LOW companion — CREATED / NOT CREATED**
- **REF↔LOW consistency — PASS / FAIL / NOT RUN**
- **Concept blind gate — PASS / FAIL / NOT RUN**
- **Blind-reason canon audit — PASS / FAIL / NOT RUN**
- **Gorrund body-only readability — ACCEPT / CONSTRAIN / REJECT**
- **Measurement scaffold — DERIVED / PARTIAL / NOT DERIVED**
- **Canon reconciliation — CLEAN / CONFLICTS / NOT RUN**
- **RM-OT-05 — READY FOR AUTHOR CLOSURE / OPEN**
- **Stage C — READY / BLOCKED**
- **Canon promotion — NOT PERFORMED**
- **D4 — NOT STARTED**
- **UE5 — NOT STARTED**

Include:

1. source-recovery manifest;
2. source selection rationale;
3. source-generation package if fallback was needed;
4. untouched source hashes;
5. surgical edit summary;
6. REF/LOW sheets;
7. blind evidence;
8. scaffold data if derived;
9. canon reconciliation;
10. unresolved dependencies/conflicts.

---

# 29. STOP CONDITION

STOP at the RM-OT-05M author gate.

If no usable prior source exists and Rodin/Hyper3D generation is inaccessible, stop after delivering the source-generation package.

Do not fall back to:

- SDF primitives;
- Marchfolk donor morphing;
- old skeleton cage;
- another parametric Gorrund generator.

Do not begin:

- Stage C;
- canon promotion;
- production rigging;
- creator interpolation;
- D4;
- UE5;
- animation;
- equipment fitting;
- gameplay implementation;
- unrelated RAC work.
