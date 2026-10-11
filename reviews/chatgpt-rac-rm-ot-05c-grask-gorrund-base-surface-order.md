# RAC RM-OT-05C — Grask / Gorrund dedicated base-surface authoring order

**Author decision:** RM-OT-05B does **not** pass. Keep RM-OT-05 **OPEN**. Do not promote 05B bodies, do not close the gate, and do not write back D4.

The 05B work is retained as diagnostic/provenance and as useful infrastructure, especially the race-surface stage and the improved skeletal relations. However, the current MPFB-derived whole-body surface still reads as human-family anatomy under body-only blind review. The next block is therefore an **art/base-surface escalation**, not another attempt to force the existing human-derived surface farther with procedural fields.

## 1. Objective

Create genuinely race-specific whole-body base surfaces / tissue donors for **Grask** and **Gorrund** that:

1. preserve the accepted race skeletons, stature system, ground contact, bony relations, and composition firewall;
2. preserve the useful 05A/05B architectural findings;
3. replace the remaining human whole-body soft-tissue organization with race-specific anatomy;
4. read as Grask or Gorrund in a neutral body-only presentation **without relying on head, ears, pigmentation, hair, clothing, texture, equipment, or extreme composition**;
5. do not achieve distinctness merely by becoming "thin/lanky human" or "stocky/heavy human."

This is a **visual-first authoring gate**. Do **not** spend another large validator cycle before the body biology is visually approved.

## 2. Locked constraints

These remain binding unless a later author order explicitly changes them:

- No canon rewrite.
- No stature-range rewrite.
- No uniform scaling.
- No class-locking or anatomy that would make normal playable movement/equipment fundamentally impossible.
- Do not alter Skarn, Marchfolk, elves, Durrim, Pipkin, Cogling, Sagekin, Saurin, or Halvren in this block.
- Face, ear, pigmentation, hair, texture, locomotion, rigging, animation, collision, camera, UE5 creator, and equipment-fit work remain out of scope.
- Keep the accepted skeletons / bony guard relationships intact.
- Composition remains a separate amount layer; do not bake "muscular," "fat," "thin," or any other composition state into racial anatomy.
- Preserve adult read. Do not create juvenile, sex-coded, or caricature anatomy to gain silhouette separation.
- Do not fake race readability with posture.
- RM-OT-05 remains OPEN throughout this order.

## 3. Construction route

Use the accepted architecture as the starting support, but the new race identity must come from a **dedicated base surface / tissue donor**, not from increasingly aggressive perturbation of the MPFB human surface.

Preferred route:

```
accepted race skeleton
  -> accepted 05A architecture
  -> dedicated race-specific base surface / tissue donor
  -> retopology / transport to the validator-compatible vertex order
  -> composition amount layer
  -> final surface
```

The 05B procedural surface code may be reused where helpful, but it is **not** the identity-defining solution.

The base surface may be hand-authored or procedurally assisted during sculpt construction, but the result must represent a coherent race anatomy rather than a stack of localized deformations on human anatomy.

## 4. Grask design target

The Grask body must stop reading as "lanky human."

Required whole-body cues:

- **Long-tendon limb organization** that is apparent at body scale, not only in close-up:
  - visibly shorter / higher muscle bellies where canon permits;
  - longer distal tendon runs;
  - clear transition into wrist / ankle rather than ordinary human taper.
- **Integrated shoulder girdle**:
  - avoid the ordinary human deltoid cap;
  - shoulder, upper arm, scapular and latissimal masses should read as one race-specific mechanical system.
- **Pelvis-to-thigh organization**:
  - invent a non-human but plausible muscle/fascial arrangement while preserving the locked GR-P2b / GR-P6 bony relations;
  - do not simply narrow the pelvis or erase the buttocks if that violates canon.
- **Distal architecture**:
  - hands, wrists, ankles, feet, elbows, and knees should contribute to the racial read;
  - do not depend only on long limbs.
- Preserve a capable adult physiology. It must not read emaciated, sickly, adolescent, or feminized simply to differentiate it.

The visual target is: **a naturally evolved Grask anatomy whose long-lever body is structurally coherent**, not a stretched human.

## 5. Gorrund design target

The Gorrund body must stop reading as "stocky/heavy/boxy human."

Required whole-body cues:

- **Axial load-bearing anatomy**:
  - trunk musculature should read as a continuous structural chain from upper back through lumbar region into sacrum/pelvis;
  - avoid the ordinary human sequence of ribcage -> waist hollow -> gluteal shelf.
- **Depth-led pelvis and abdominal wall**:
  - retain the canonically deep pelvis;
  - redesign abdominal / pelvic soft tissue so it belongs to that architecture rather than reading as a human paunch or obesity.
- **Columnar limb musculature**:
  - thigh, shank, forearm, and upper arm should carry load-bearing mass differently from human muscle bellies;
  - knee / ankle / elbow / wrist transitions should look structural rather than merely thick.
- **Joint relief** must remain present and useful at reference composition and low composition.
- The silhouette should communicate "Gorrund" through body mechanics, not just width.

The visual target is: **a structurally powerful Gorrund adapted around a deep axial frame**, not a large human bodybuilder or obese human.

## 6. Candidate exploration — do not jump directly to one final mesh

Produce a small deliberate candidate family before committing.

For each race, make **3 distinct candidate base-surface directions**:

- **Candidate A — restrained:** closest to current canon-safe anatomy while replacing the most human muscle-group reads.
- **Candidate B — balanced:** stronger race-specific tissue organization while still conservative enough for production.
- **Candidate C — assertive:** pushes the race biology as far as the locked skeleton and relations honestly allow without caricature.

Do not create candidates that differ only by muscle/fat amount, stature, or simple global width.

For each candidate, provide:
- reference composition;
- one low-muscle / low-composition diagnostic;
- one Broad or Narrow frame diagnostic only if needed to prove the racial anatomy survives frame variation.

## 7. Visual-first evidence gate

Before exhaustive W2C/W2D revalidation, produce matched evidence specifically for **author visual selection**.

### 7.1 Required comparison sheets

For **Grask** use the accepted central/reference stature around **218 cm** plus one matched-height comparison where useful.

For **Gorrund** use the accepted central/reference build around **229–230.9 cm**.

For each race/candidate provide:

1. full body, head/neck removed, neutral grey:
   - front
   - front 3/4
   - profile
   - rear 3/4
2. pure black silhouette:
   - front
   - profile
3. matched comparison with:
   - current accepted/provisional race body;
   - Skarn at matched height where possible;
   - Marchfolk control where useful.
4. one close architecture strip showing the anatomy that actually changed:
   - shoulder / thorax
   - pelvis / hip
   - knee / ankle
   - elbow / wrist / hand
   as appropriate to the race.

Use one ground plane, matched orthographic camera, matched reference distance, neutral material, and no visual tricks.

### 7.2 Required body-only reading question

Run a **lightweight blind read**, not the full validator suite yet.

At minimum:
- three independent uninformed scorers;
- labels hidden;
- body-only, height-normalized grey + silhouette;
- include human-family controls and the new candidates;
- require written descriptions of *why* the scorer grouped a body.

The key question is not merely assignment count. It is:

> Would an uninformed viewer describe this as a distinct non-human body organization, or still as a lanky / stocky / unusual human?

A candidate that wins by "thinness," "bulk," "height," "big hands," or a single local feature is not sufficient.

## 8. Minimal guards before author review

Do **not** run the entire W2C/W2D validator chains yet, but reject a candidate immediately if any of these fail:

- stature;
- ground contact;
- no uniform scaling;
- no gross self-intersection;
- arm / trunk clearance;
- accepted skeleton unchanged;
- locked bony relations obviously violated;
- composition firewall broken;
- candidate collapses back to human read in low composition;
- candidate requires forbidden posture or presentation tricks.

For Grask, specifically verify GR-P2b and GR-P6 are not being violated by the surface construction.

For Gorrund, specifically verify the new surface has not trivially destroyed the accepted deep-pelvis architecture. Do not attempt to satisfy old skin-depth rows by simply restoring the exact human glute / belly morphology that 05B was trying to escape.

## 9. What not to optimize yet

Do not spend time in this block on:
- full exhaustive W2C/W2D validator reruns;
- final retopology cleanup beyond what is needed for trustworthy candidate renders;
- equipment;
- rigging;
- animation;
- skinning;
- facial identity;
- ears;
- pigmentation;
- textures;
- hair;
- clothing;
- locomotion;
- gameplay;
- UE5 integration.

Those come **after** author selection of the base biology.

## 10. Acceptance standard for this gate

This order is successful when there is at least **one credible Grask candidate and one credible Gorrund candidate** for which:

- the body-only silhouette and grey read are clearly distinguishable from human-family controls;
- scorer explanations no longer reduce the body to "lanky human" or "stocky/heavy human";
- the distinction survives low composition;
- the design reads as coherent anatomy rather than ornamental exaggeration;
- the minimal guards above pass.

This is **not** final promotion. It is an **author candidate gate**.

## 11. Deliverables

Create:

- `reviews/claude-rac-rm-ot-05c-grask-gorrund-base-surface-candidate-gate.md`
- `reviews/rac-rmot05c-evidence/`
  - `README.md`
  - candidate sheets
  - blind-read results
  - minimal-guard results
  - candidate construction notes
- persistent candidate assets / manifests under the existing race reference-asset conventions, clearly marked **PENDING AUTHOR / NOT ACCEPTED**.

The gate report must include:
- concise summary of each candidate direction;
- which candidates were rejected and why;
- which Grask candidate Claude recommends;
- which Gorrund candidate Claude recommends;
- explicit statement of whether either race still reads human and why;
- list of any canon guard that prevented a stronger solution;
- exact files changed / added.

## 12. Stop condition

**STOP after the RM-OT-05C candidate gate.**

Do not promote a candidate.
Do not close RM-OT-05.
Do not run the exhaustive final validator suite.
Do not write D4.

Wait for author review of the candidate biology. After a candidate is selected, the next order will authorize production retopology/transport and the full numerical closure gate.

