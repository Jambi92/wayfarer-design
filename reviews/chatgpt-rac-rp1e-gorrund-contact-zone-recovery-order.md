# RAC RP1E — Gorrund contact-zone recovery after RP1 FAIL

**Date:** 2026-10-19
**Authority:** Tyler-authorized autonomous technical continuation after RP1 gate failure.
**Parent gate:** `reviews/claude-rac-rp1-gorrund-production-retopo-pilot-gate.md` (de1288c)
**Method:** remains M-B fully manual retopology.
**Production tolerances:** unchanged from `reviews/tyler-chatgpt-rac-rp1-gorrund-release-decisions.md`.

## 1. Ruling

The RP1 failure does **not** reopen the method or the tolerances.

Evidence shows the open/convex body, stature, bbox, tail root and silhouettes are already viable. The failure is localized to contact / concave zones where one coarse cage sheet is projected onto two nearby source sheets.

Proceed with a bounded local recovery.

Do not:
- relax T-1/T-2/T-3/T-6/T-7;
- accept contact topology as a permanent exception;
- use QuadriFlow or automatic remesh;
- rebuild the successful trunk/limbs from scratch unless a local repair proves impossible;
- start RP2.

## 2. Working source

Start from the latest manual-cage file that still contains the editable cage + modifier stack:

`E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Gorrund/RP1/GO_U_REF_RP1_retopo_v004.blend`

Recorded hash:
`212e7508ea3fe64ae227036a6780f874288c661cbc98bec230bf29c729505d57`

Candidate `GO_U_REF_RP1_production_v001.blend` is failed evidence only and must not be promoted.

Frozen anatomy source remains unchanged:
`GO-05AW4_nails_final.blend`
SHA-256 `5a4e45d40158e7dc92f6f8ba13d67ada2403e3e3dcda9048382323ee43a22d5e`.

## 3. Preserve successful cage regions

Keep the current manual cage topology where it already proves viable:
- open trunk surfaces;
- major limb shafts;
- tail body and accepted tail-root region;
- general stature / silhouette envelope.

Do not disturb those regions merely to make the topology more uniform.

## 4. Create derived local projection targets

The whole-body source is too ambiguous in close-contact regions.

From the **derived welded working copy only**, prepare temporary projection targets for:
- left hand;
- right hand;
- left axilla / upper-arm pocket;
- right axilla / upper-arm pocket if needed;
- head / jaw / ears;
- left foot / toes;
- right foot / toes;
- perineum / pouch.

These are diagnostic/authoring helpers only, not production outputs.

Each local target must contain only the intended source sheet plus enough overlap to support continuity.

No target may modify the frozen source.

## 5. Hands — rebuild as isolated manual sub-cages

Both hands are the main failure and must not be repaired by repeated whole-body shrinkwrap.

For each hand:

1. Detach or replace the current hand cage at a clean wrist ring.
2. Manually retopologize the hand against the **hand-only derived target**.
3. Explicitly author:
   - palm topology;
   - thumb web;
   - four finger clefts;
   - separate finger tubes;
   - knuckle loops;
   - nail-bearing distal surfaces.
4. The hand cage must have visible clearance between every digit pair **before subdivision**.
5. Join/weld the completed hand cage back to the wrist ring.
6. Preserve five-digit anatomy and source hand proportions.

Temporary separate hand objects are permitted during authoring; final production body remains one welded component.

## 6. Contact-zone loop repairs on the main cage

Author explicit separating loops for:

### Axillae
- deepen the axillary fold;
- keep arm tube clear of trunk;
- remove the cage's own contact/intersection before subdivision.

### Perineum / pouch
- create distinct left/right inner-thigh surfaces and central perineal/pouch flow;
- no single face may bridge opposing source sheets.

### Head / jaw / ears
- jaw-line loop separating underside of jaw from neck/chest;
- ear-cup inner-rim loops so the cup is represented as its own concavity;
- preserve muzzle/ear silhouette under T-2.

### Feet / toes
- one explicit cleft route between every adjacent toe;
- preserve the nail-bearing distal surface;
- no projection across neighboring toe sheets.

## 7. Mandatory coarse-cage gate before subdivision

Before applying any new subdivision/projection stack:

The manual cage itself must be:
- 1 intended connected body after joins;
- 0 boundary;
- 0 non-manifold;
- genus 0;
- **0 self-intersections**;
- visibly separated in every finger/toe cleft, axilla and perineal contact;
- no face bridging two opposing source sheets.

If the coarse cage fails this, keep editing it. Do not proceed to subdivision.

## 8. Progressive projection gate

Do not jump directly to the full 4-level applied stack.

Run the production stack one level at a time.

At each level:
1. subdivide once;
2. project only to the appropriate whole-body or local target;
3. evaluate self-intersections;
4. evaluate local T-2 deviation in the affected zones.

A level may advance only if:
- self-intersections = 0 in repaired contact zones;
- no new cross-sheet projection is visible;
- identity zones remain trending inside T-2.

If a projection step creates cross-sheet folding, revert that level and repair the lower-resolution cage.

## 9. Projection ownership

Use local projection targets where whole-body nearest-surface projection is ambiguous.

Recommended:
- trunk/open limbs/tail: whole welded source;
- hands: hand-only targets;
- ears/jaw: head-only target;
- feet/toes: foot-only targets;
- axilla/perineum: local body targets.

Projection is a fitting tool, not an anatomy author.

## 10. Nail preservation

Before final gate:
- explicitly restore/check each nail-bearing toe surface;
- all 8 tracked nail projections must remain within ±0.15 mm;
- nail taper/curl/silhouette remains visually unchanged.

No nail miss may be waived as micro-detail.

## 11. Landmark recovery

Re-run the length-weighted T-6 method only after contact-sheet folding is eliminated.

Required:
- target <= 1.0 mm;
- no landmark > 1.5 mm;
- any landmark > 1.0 mm individually explained.

Do not compensate landmark drift by moving accepted anatomy.

## 12. Final RP1E gate

The same accepted contract applies.

Required:
- 1 component / 0 boundary / 0 non-manifold;
- genus 0;
- 0 self-intersections;
- 0 degenerates;
- quad-dominant contract target;
- T-1 pass;
- T-2 pass in all identity zones;
- T-3 pass;
- T-6 pass;
- T-7 pass;
- all nails pass;
- visual veto clear.

Produce:
`reviews/claude-rac-rp1e-gorrund-contact-zone-recovery-gate.md`

Evidence:
`reviews/rac-rp1e-evidence/`

Include source vs RP1 failed vs RP1E final comparison sheets, especially hands, axillae, jaw/ears, perineum and toes.

## 13. Stop rule

If the manual contact-zone rebuild still cannot reach the accepted gates without changing anatomy, return:

**RP1E MANUAL CONTACT-ZONE RECOVERY FAILED / AUTHOR DECISION REQUIRED**

Do not relax the contract.

If it passes, return:

**RP1E GORRUND PRODUCTION RETOPO PASS / READY FOR FAMILY-PILOT AUTHOR REVIEW**

Then STOP.

Do not begin RP2, rigging, creator implementation or UE5.
