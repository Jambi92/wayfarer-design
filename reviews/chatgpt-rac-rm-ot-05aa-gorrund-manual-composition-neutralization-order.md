# RAC RM-OT-05AA — alternate-source decision: manual composition-neutralization from Gorrund-Neutral-C

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05Z3 route retirement.
**Date:** October 15, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05z3-gorrund-neutral-c-calibration-review.md` (4b4723c).

## 1. Order-level route decision

The Rodin Gorrund ARM source route is retired for reference composition.

Do not purchase or run another Gorrund Rodin composition generation.

Adopt a new route:

**Gorrund-Neutral-C is an immutable high-resolution sculpt donor, not an accepted ARM. A separate Blender working derivative may now be manually sculpted to neutral reference composition, using the already author-accepted W1i/W1j Gorrund ARM as the structural guide.**

This order supersedes the 05Z3 "do not sculpt C" prohibition only for a new derived working copy under the safeguards below. The original C master remains untouched forever.

## 2. Pinned sources and roles

### Immutable donor C
`Gorrund_Neutral.glb`
- size: 29,805,740 bytes
- SHA-256: `513bc9e2c5c4ba1da0a5a33661f230181bf18a24c50e0af0d49acdf5521dccf6`

Role:
- high-resolution sculptural surface donor;
- clean leonine head;
- five-fingered hands;
- five-toed plantigrade feet;
- neutral unclothed pelvis;
- single connected body;
- usable pose;
- tail whose root is closer to the midline than A/B.

It is **not** a reference-composition body and is not canon.

### Accepted structural guide
The retained W1i/W1j Gorrund point is already **AUTHOR ACCEPTED as the W1 ARM** by:

`reviews/chatgpt-rac-w1j-gorrund-final-author-acceptance.md`

Use its accepted anatomical relationships and reference outcome as the macro-structure guide.

Important:
- raw W1 solver values remain construction/reproducibility values, not species constants;
- do not force C to arbitrary numeric solver coordinates merely because they exist;
- do use the accepted W1 body to protect the integrated thorax-lumbar-pelvis load-bearing identity, joint scale, frame relationships and distinction from Broad Skarn / enlarged human.

### 2D soft-tissue reference
Candidate 09 may be used only as visual reference for neutral surface composition:
- flat chest;
- sloping shoulders;
- low muscle definition;
- slim-to-average limb soft tissue;
- no belly compensation.

Do not project the 2D silhouette blindly onto the mesh.

## 3. Why this route is allowed

05W established:
- procedural/SDF anatomy is not acceptable as the final sculptural source;
- a **real sculpt in Blender is acceptable**;
- Blender itself was not the failure;
- Claude's earlier desktop work demonstrated credible local hand-sculpting, though not a whole-organism procedural rebuild.

This order therefore does **not** authorize a procedural body generator, SDF rebuild, solver-generated surface, or scripted geometry replacement.

It authorizes **manual sculpting of the real C donor surface**, with the accepted W1 ARM used as an anatomical reference.

## 4. Phase AA0 — readiness / structural comparison before sculpt

Before changing C:

1. import C into Blender as a working copy;
2. save a pinned baseline scene, e.g. `GO-05AA_C_baseline.blend`;
3. record the exact donor hash and prove the source file remains unchanged;
4. locate/reconstruct the accepted W1i/W1j reference body through the existing reproducible W1 tooling;
5. create same-height / normalized comparison views between:
   - C body-only diagnostic;
   - accepted W1 Gorrund ARM;
   - frozen Marchfolk / Skarn / Grask controls already used by the RAC method;
6. compare macro structure only:
   - thoracic breadth/depth;
   - integrated lumbar transition;
   - pelvis breadth/depth;
   - shoulder girdle placement;
   - major joint scale;
   - limb shares / reach;
   - thigh and calf envelope;
   - stance.

### AA0 decision

If C's **macro skeletal/frame envelope is materially incompatible** with the accepted W1 ARM such that manual surface sculpting would require wholesale bone-length/joint-position reconstruction, STOP:

**05AA BLOCKED — DONOR MACRO FRAME INCOMPATIBLE / HUMAN SCULPT OR NEW NON-RODIN SOURCE REQUIRED**

Do not warp it into place.

If the macro frame is compatible enough that the remaining Q1/Q2 failure is primarily superficial/soft-tissue form, continue to AA1.

## 5. Phase AA1 — manual composition-neutralization sculpt

Work only in real Blender desktop Sculpt/Edit interaction.

### Preserve
Unless a local continuity touch is unavoidable, preserve:
- skull/head identity;
- muzzle, ears and facial proportions;
- hands and digit count;
- feet and toe count;
- major joint centres;
- accepted rib-cage / pelvis frame;
- limb lengths;
- overall stature relationship;
- neutral groin/pelvic landmarks;
- tail free-length geometry;
- all topology.

### Modify
Neutralize the heroic **soft-tissue surface**, not the skeleton:

**Torso**
- remove abdominal block segmentation;
- soften / remove serratus grooves;
- flatten pectoral projection toward natural untrained tissue;
- remove central chest split / hard lower-pec shelf;
- remove love-handle bulges without pinching the waist;
- preserve a broad/deep thorax and integrated trunk.

**Shoulder / arms**
- reduce deltoid cap;
- soften biceps/triceps separation;
- remove corded forearm / vein-like definition;
- preserve joint size and ordinary arm mass.

**Legs**
- soften quadriceps separation and teardrop;
- reduce calf belly definition;
- preserve large knees/ankles and load-bearing leg identity.

**Gluteal / posterior**
- reduce the large round projected gluteal mass to natural untrained volume;
- preserve robust pelvis and gluteal crease landmarks;
- do not create flat or atrophied anatomy.

The desired read is:
**large structural frame + ordinary untrained soft tissue**, not bodybuilder, strongman, obese, chubby, melted mannequin or smooth primitive.

## 6. Method limits

Allowed:
- Sculpt Mode Smooth;
- Surface Smooth / Relax where available;
- Flatten / Scrape in restrained local passes;
- Grab / Elastic Deform for small soft-tissue volume correction;
- Edit Mode vertex movement for specific continuity issues;
- masking / face sets.

Forbidden:
- Dyntopo;
- voxel remesh;
- global remesh;
- decimation;
- topology replacement;
- scripted vertex movement;
- solver-generated candidate shapes;
- SDF / primitive reconstruction;
- shrinkwrap-as-final-shape;
- uniform scaling;
- automated "make less muscular" deformation;
- copying another race's surface.

The W1 ARM may be shown as a **reference/guide**, not used as an automated surface target.

## 7. Checkpoint budget and region order

Maximum **three deliberate production checkpoints**:

1. **Torso + shoulder girdle** — chest, deltoids, abs/serratus, waist.
2. **Arms + legs** — upper/forearms, quads, calves.
3. **Posterior** — gluteal projection / posterior thigh continuity, only if needed.

After each checkpoint:
- save a distinct scene;
- render identical-camera whole and body-only F / P / B / 3/4 views;
- compare to donor C, accepted W1 ARM and controls;
- run topology / self-intersection / manifold checks;
- confirm preserved regions and major landmarks have not drifted.

Do not spend a later checkpoint if Q1/Q2 are already satisfied.

## 8. Acceptance gate for the sculpted derivative

After the best safe checkpoint, rerun the existing whole-source Q1-Q4 gate.

Required for success:

- **Q1 YES:** Gorrund structural identity at reference composition;
- **Q2 YES:** with head and tail hidden, does **not** read as enlarged human/bodybuilder/ogre and remains distinct from Grask;
- **Q3:** pose, feet, landmarks and continuity are at least as good as C, aside from the already known tail/heel items;
- **Q4 YES for remaining work:** any remaining defects are local/bounded.

Also compare directly to A/B/C:
- materially less heroic muscle definition;
- no obesity compensation;
- no melted/mannequin loss of anatomy;
- no collapse of the W1 accepted load-bearing frame.

### Success phrase

**05AA COMPOSITION NEUTRALIZATION PASS / AUTHOR VISUAL REVIEW REQUIRED**

Then STOP for Tyler's visual ruling before tail-root or heel correction.

### Failure phrase

If three manual checkpoints cannot achieve Q1/Q2 without damaging the accepted structural read:

**05AA MANUAL SCULPT LIMIT REACHED / HUMAN SCULPTOR OR NEW NON-RODIN SOURCE REQUIRED**

Then STOP. Do not create another generator loop.

## 9. Deferred local issues

Do not repair these during AA1 unless they physically block the composition sculpt:
- tail fused down the gluteal cleft / buttock;
- heel lift ~1–1.6 raw cm;
- final foot-size judgement;
- genus handles.

If AA1 passes, those become the next bounded local-repair block.

## 10. State

Until AA1 passes and Tyler visually accepts it:
- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED;
- no LOW / blind final acceptance / scaffold;
- no D4 / UE5 / production rigging / creator implementation.

## 11. Return

Commit:
`reviews/claude-rac-rm-ot-05aa-gorrund-manual-composition-neutralization-gate.md`

Evidence:
`reviews/rac-rmot05aa-evidence/`

First return should include AA0 readiness and, if compatible, the checkpointed AA1 result.
