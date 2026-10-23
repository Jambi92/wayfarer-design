# RAC RP2 — Grask production-mesh pilot with internal asymmetry adjudication and self-test-first execution

**Date:** 2026-10-23
**Authority:** Tyler authorizes autonomous technical execution through ChatGPT.
**Parent program:** `reviews/chatgpt-rac-retopology-rigprep-master-plan.md`.
**Prerequisite:** RP1 Gorrund final freeze order in this same release.

## 1. Execution policy

Claude is authorized to execute RP2 autonomously.

**Do not turn routine intermediate work over to Tyler for review.**

Tyler should see a result only after Claude has:
- completed its own technical gates;
- corrected all fixable failures;
- rerun the full gate;
- produced a candidate that is technically PASS, or
- proven a true canon/anatomy contradiction that cannot be resolved from existing authority.

Ordinary topology, shading-band, symmetry, deformation, or cleanup failures are Claude's responsibility to diagnose and repair before escalation.

No "looks good, owner review?" checkpoints before the technical gate passes.

## 2. Authoritative Grask source

Use:

`reviews/reference-assets/r6/GR5DE3_r6.npz`

SHA-256:

`d859eb189ef11881cae2f92ac77414ee630a899d4c1dcf95c0ac78e5a558d778`

Role:
**Stage C accepted E3 reference, approximately 218 cm.**

Authority:
- `reviews/tyler-chatgpt-rac-stage-c-final-author-ruling.md`
- `reviews/claude-rac-stage-c-final-closure.md`

The older RP0 inventory string saying "PENDING AUTHOR / NOT ACCEPTED" is stale metadata and is superseded by Stage C final acceptance.

Correct that metadata during RP2 bookkeeping; do not treat it as an acceptance conflict.

Source remains immutable.

## 3. Accepted Grask identity constraints

Production must preserve the accepted E3 direction:

- long-limb / short-torso organization;
- accepted girdle slope;
- visible joint structure;
- pelvis organization;
- scapular mass / keel / flank relationships;
- moderate but adequate front-view Grask identity;
- multi-view species identity;
- chest/abdomen organization;
- distinction from stretched-human / Aelari-like anatomy;
- distinction from Durrim compact structural-power architecture.

Carry Stage C implementation rulings:

1. E3 scapular mass / keel / flank scale relationship-aware across stature.
2. Narrow-frame joint breadth belongs to skeleton/frame, not fake tendon-cord bulk.
3. Chest/abdomen shading band is a retopology/surface/normal issue, **not morphology canon**.
4. Front-view identity must survive topology, rigging, creator, clothing and animation.

## 4. Internal asymmetry adjudication — no owner gate first

RP0 found E3 bilateral asymmetry:
- overall mirror RMS about 0.18 cm;
- p99 about 0.99 cm;
- shoulder/neck local max about 1.86 cm;
- prior W2 GR218R is near-symmetric.

This must be resolved **internally before production authoring**, using evidence rather than asking Tyler to judge raw numbers.

### 4.1 Build diagnostic evidence

Generate:
- E3 original;
- E3 mirrored comparison;
- bilateral-average diagnostic surface;
- W2 GR218R comparison;
- front/back/profile/3-quarter overlays;
- asymmetry heat map;
- landmark-side difference table;
- silhouette-side difference table;
- trunk/shading-band localization;
- shoulder/neck/scapular localization.

Do not modify source.

### 4.2 Classify every significant asymmetry region

Classify into exactly one:

**A — accepted structural asymmetry**
- tied to skeletal landmark or accepted silhouette relationship;
- persistent across views;
- contributes meaningfully to accepted E3 identity;
- not explained by one-sided construction/shading artefact.

**B — construction/surface artefact**
- localized to one-sided E3 organization or shading-band construction;
- skeletal/joint landmarks remain effectively bilateral;
- removal improves surface continuity without changing accepted multi-view identity.

**C — mixed**
- structural base should remain asymmetric, but a superimposed surface/shading artefact should be symmetrized/cleaned.

### 4.3 Automatic decision rule

Claude should choose the production interpretation itself:

- preserve Class A;
- symmetrize/clean Class B;
- use a hybrid for Class C.

Do **not** globally mirror E3.

The default is conservative: accepted source shape is preserved unless the evidence clearly identifies construction artefact under the Stage C ruling.

A local surface asymmetry may be removed when:
- it is not supported by landmark/skeletal asymmetry;
- it is linked to the known shading-band/organization artefact;
- its removal does not weaken front-view or multi-view identity;
- the chosen production surface still passes the contract.

### 4.4 Only true unresolved contradiction escalates

If, after the full diagnostic package, a region is equally supported as intentional accepted anatomy and construction artefact, Claude must create **both technically viable local alternatives**, run the same gates on both, and recommend one.

Only after both alternatives are fully tested may Claude return:

**RP2 GRASK ASYMMETRY CANON CONTRADICTION / CHATGPT DECISION REQUIRED**

Do not send an untested visual question to Tyler.

## 5. Production topology strategy

Grask uses the MPFB hm08 topology family as the starting production base, because E3 already uses the shared 13,380-vertex/13,378-quad topology.

Do not retopologize Grask from scratch unless the shared base demonstrably cannot satisfy the RP2 contract.

Use the MPFB topology plus a **Grask-specific production branch**.

Required local additions/cleanup where necessary:
- shoulder/girdle support;
- scapular mass;
- keel/chest organization;
- abdomen/flank organization;
- elbows/wrists/hands;
- hips/knees/ankles;
- visible joint support;
- creator-density support;
- any topology needed to eliminate E3's current reference-pose self-intersections.

Preserve a mapping back to the shared MPFB base.

## 6. Source self-intersections are not inherited

RP0 records approximately 124 piercing edges on E3 in R-6 stance.

The production mesh must not simply inherit them.

Required final production reference stance:
- 1 component;
- 0 boundary;
- 0 non-manifold;
- genus 0;
- 0 degenerate faces;
- 0 hidden shells/duplicates;
- **0 self-intersections** unless a later explicit contact exception is proven and authorized;
- consistent outward normals;
- >=98% quads overall;
- 100% quads in deformation zones.

## 7. Chest/abdomen shading-band cleanup

Treat the one-sided chest/abdomen band as a production-surface problem unless the asymmetry evidence proves a structural anatomical component.

Correct using:
- topology flow;
- surface continuity;
- normals/shading readiness;
- local bilateral cleanup where classified B/C.

Do not flatten the accepted keel, scapular mass, or abdominal organization.

Do not turn Grask into a smooth generic humanoid.

## 8. Deformation and creator readiness

RP2 must prove the Grask branch is production-usable.

Required support:
- shoulders / axilla;
- elbows;
- wrists;
- fingers;
- hips;
- knees;
- ankles;
- toes;
- neck;
- spine/abdomen;
- pelvis;
- scapular/girdle region.

Use diagnostic deformation tests where useful.

Do not promote a final game rig.

For every diagnostic deformation:
- test the topology yourself;
- correct avoidable collapse/intersection;
- do not ask Tyler to review a failing deformation pose.

## 9. Production tolerances

Use `specs/RAC_PRODUCTION_MESH_CONTRACT.md` §16.

Required hard gates:

### T-1 body, both directions
- median <=0.5 mm;
- p95 <=1.5 mm;
- max <=3.0 mm.

### T-2 identity zones
- median <=0.3 mm;
- p95 <=0.8 mm;
- max <=1.5 mm.

For Grask, identity zones include at minimum:
- head/face;
- hands/feet;
- girdle/shoulder organization;
- visible joint landmarks;
- pelvis organization;
- keel/chest organization where it defines Grask read.

### T-3
- stature ±1.0 mm;
- bbox ±2.0 mm per axis.

### T-6
- target <=1.0 mm;
- none >1.5 mm;
- individually report any >1.0 mm.

### T-7
- front/profile/rear silhouette IoU >=0.995.

T-4 and T-5 remain quality targets; improve failures when practical and report concentrated exceptions.

## 10. Front-view identity veto

A numeric pass is insufficient if the production result weakens Grask's accepted front-view read.

Claude must run identical-camera comparisons showing:
- girdle slope;
- long-arm and long-shin contribution;
- visible joint structure;
- pelvis organization;
- chest/abdomen/keel read.

If a candidate becomes visually more human/Aelari-like, reject it internally and continue.

Do not send that rejected candidate to Tyler.

## 11. Candidate workflow

Use versioned production candidates under:

`E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Grask/RP2/`

Suggested naming:

`GR_U_REF_RP2_production_v001.blend`
`GR_U_REF_RP2_production_v002.blend`
etc.

Evidence:

`reviews/rac-rp2-evidence/`

Never overwrite a promoted candidate.

Keep source read-only and re-hash before/after.

## 12. Internal retry policy

Claude is explicitly expected to self-correct.

For a failed candidate:
1. identify the failing region/mechanism;
2. modify only the needed production branch;
3. rerun local gates;
4. rerun global gates;
5. continue until PASS or a genuine contract/canon contradiction is proven.

Do not stop because:
- one topology attempt failed;
- one asymmetry cleanup failed;
- one projection/shrinkwrap method failed;
- one diagnostic deformation failed;
- one shading approach failed.

Choose another technically legitimate method within the production contract.

## 13. Required pre-owner PASS package

Before Tyler sees RP2, Claude must have one candidate that passes:

- source integrity;
- topology integrity;
- 0 self-intersections;
- T-1;
- T-2;
- T-3;
- T-6;
- T-7;
- front-view identity veto;
- multi-view identity veto;
- deformation-zone topology audit;
- creator-density audit;
- asymmetry adjudication report;
- shading-band cleanup audit.

Then return:

**RP2 GRASK PRODUCTION PILOT TECHNICAL PASS / READY FOR OWNER VISUAL REVIEW**

Only at that point is an owner visual review appropriate.

## 14. Hard stop

If a genuine unresolved biology/canon contradiction remains **after both alternatives have been built and technically tested**, return:

**RP2 GRASK CANON CONTRADICTION / CHATGPT DECISION REQUIRED**

Provide both tested alternatives and a recommendation.

Do not ask Tyler to decide before technical testing is complete.

## 15. No downstream authorization

No RP3.
No final production rigging.
No creator implementation.
No UE5 integration.
No clothing/equipment production.

RP2 must pass and be accepted first.

## 16. Return files

Create:
- `reviews/claude-rac-rp2-grask-production-pilot-gate.md`;
- `reviews/claude-rac-rp2-grask-asymmetry-adjudication.md`;
- production sidecar(s);
- full evidence under `reviews/rac-rp2-evidence/`.

Update:
- `specs/STATUS.md`;
- `reviews/claude-session-handoff.md`;
- stale GR5DE3 acceptance metadata in the appropriate manifest/inventory bookkeeping without altering historical evidence files that should remain immutable.

