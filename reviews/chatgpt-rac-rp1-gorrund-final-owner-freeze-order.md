# RAC RP1 — Gorrund final owner acceptance, freeze, and production-pilot closure

**Date:** 2026-10-23
**Authority:** Tyler direct owner acceptance after reviewing rev110 hand/thumb/grip evidence.
**Accepted closure report:** `reviews/claude-rac-gorrund-hand-mesh-grip-closure.md` at commit `003477885a6f906c17e3afca1d336120463ebe43`.
**Accepted rev110 PC file:** `work/claude110/Gorrund_hand_production110.blend`
**Returned SHA-256:** `133edfde40532244332ac17ea6ad887713d5e700392c36365ef6c31ca20609e8`.

## 1. Owner ruling

Tyler has reviewed and **ACCEPTED** the rev110 Gorrund hand result.

This acceptance closes the remaining RP1 family-pilot visual/owner gate.

The final status is:

**RAC RP1 GORRUND FAMILY PILOT — FINAL OWNER ACCEPTED / FROZEN**

No additional Gorrund hand sculpting or retopology iteration is requested.

## 2. Accepted owner-review items

The following items from the rev110 closure are explicitly accepted for the Gorrund production pilot:

1. **Hand topology method substitution**
   - accepted rev107 hand surface refit into the v015 production body;
   - R middle/ring bridge cut/cap;
   - resulting hand/body topology at genus 0.

2. **Thumb-tip graft**
   - both thumb tips rebuilt from the accepted index-fingertip shape direction;
   - accepted as intentional owner-directed anatomy refinement;
   - the corresponding rev107 thumb-tip T-2 exclusion is accepted and is not a failure.

3. **R thumb-base crater exclusion**
   - accepted as exclusion of a known source sculpt artefact;
   - do not recreate the source crater in the production mesh.

4. **T-4 quality result**
   - 88.0% angle target / 95.4% aspect target is accepted for RP1;
   - T-4 is a quality target, not a hard failure gate;
   - the shortfall is localized primarily to rigid claw-tip fans;
   - retain as future LOD/topology-quality watch item.

5. **Diagnostic contact tolerances / correctives**
   - accepted as evidence that the hand shape can perform required motions;
   - skin-skin <=1.0 mm, claw contact <=0.5 mm, fixture penetration <=0.5 mm are accepted **for this diagnostic test only**;
   - corrective deformation up to ~10 mm is accepted as diagnostic proof, not as final production rig canon.

6. **Left-hand grip forms**
   - L clench thumb alongside index: accepted as a valid diagnostic closed grip;
   - L handle grip with thumb locked on index rather than handle: accepted as a valid diagnostic power grip;
   - these are **not mandatory runtime animation poses**.

## 3. Diagnostic rig is evidence only

Do **not** promote the rev110 diagnostic rig, human phalanx ratios, weights, actions, or corrective shape keys as the canonical production Gorrund rig.

Preserve them as deformation evidence only.

Carry forward to future rigging:
- claws require rigid distal ownership;
- soft-tissue palm/crease contacts will likely require proper corrective shapes or helper behavior;
- future production joint placement must derive from accepted Gorrund anatomy/landmarks, not simply reuse the diagnostic human-ratio estimates.

## 4. Final production freeze

Create a canonical frozen production copy from the accepted rev110 mesh **without changing geometry**.

Target canonical file:

`E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Gorrund/RP1/GO_U_REF_RP1_FINAL.blend`

Rules:
- copy/promote accepted rev110 production geometry only;
- no geometry edits;
- no re-sculpt;
- no retopo;
- no smoothing;
- no remesh;
- no rig promotion.

Open/re-save only if required for canonical naming/metadata and only if the production mesh geometry remains bit-identical.

Record:
- final file SHA-256;
- geometry hash;
- vertex/face counts;
- topology report;
- accepted parent file/hash;
- derivation chain v014 -> v015 -> rev107/refit -> rev110;
- owner acceptance provenance.

Create sidecar:

`GO_U_REF_RP1_FINAL.json`

## 5. Required final verification before freeze

Claude must independently re-run/verify before marking frozen:

- 1 component;
- 0 boundary edges;
- 0 non-manifold edges/vertices;
- genus 0;
- 0 degenerate faces;
- 0 self-intersections;
- 100% quads as returned;
- stature unchanged;
- bbox unchanged within returned evidence;
- T-2 hand result remains within accepted limits outside the two explicitly accepted exclusions;
- source/reference protected files re-hash unchanged;
- canonical frozen copy geometry matches accepted rev110 geometry.

If any of these fail, do **not** return to Tyler for visual review. Fix only bookkeeping/copy issues if possible; if geometry itself no longer matches accepted rev110, STOP with a technical failure report to ChatGPT.

## 6. Documentation closure

Create:

`reviews/claude-rac-rp1-gorrund-final-owner-freeze.md`

Update:
- `specs/STATUS.md`;
- `reviews/claude-session-handoff.md`;
- RAC RP1 queue/master status;
- source/production manifest pointers as needed.

Record exact status:

**RAC RP1 GORRUND FAMILY PILOT — FINAL OWNER ACCEPTED / FROZEN**

Also record:
- diagnostic rig is non-canonical evidence;
- T-4 claw-tip quality watch item;
- final rig needs anatomy-derived joints + soft-tissue correctives;
- no UE5/rigging/creator authorization follows automatically.

## 7. Stop

After the frozen copy and documentation verify successfully, RP1 is CLOSED.

Do not do more Gorrund work.

Proceed to RP2 only under the separate Grask order.

