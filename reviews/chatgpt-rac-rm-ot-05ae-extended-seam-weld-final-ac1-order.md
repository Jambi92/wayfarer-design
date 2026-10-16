# RAC RM-OT-05AE — extend sculpt-safe weld through neck base and make final AC1 retry

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05AD.
**Date:** October 16, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05ad-sculpt-safe-seam-weld-and-ac1-retry-gate.md` (82c3508).

## 1. Ruling

05AD seam-weld preparation is accepted as technically valid.

The AC1 retry failed only on a narrow residual boundary problem:
- 11 opened seam pairs at z 168.5–170.1 cm;
- 27 self-intersecting faces caused by those neck-base seam openings;
- 5 isolated flipped faces at mask/crease edges.

The sculpt direction itself is improving and the original massive seam failure has been eliminated.

Authorize one final bounded AC1 preparation/retry.

## 2. Immutable history

Preserve unchanged:
- 05AB1 clean baseline;
- 05AD sculpt-safe baseline;
- rejected 05AC AC1;
- rejected 05AD AC1 retry.

Do not promote either rejected sculpt.

## 3. 05AE sculpt-safe baseline extension

Start from the frozen 05AD sculpt-safe baseline:

`GO-05AD_sculpt_safe_baseline.blend`
SHA-256:
`74de02e61dff24751a5e16b41b3b6d8d5f9a1ecc800f86ec944fd9dcb8c4a7bc`

Extend the exact/coincident seam weld only through the remaining upper AC1 transition band:

- current upper weld bound: 168.3 cm;
- new upper weld bound: **172.0 cm** from the floor;
- keep lower bound at 117.0 cm;
- exact/coincident duplicates only;
- maximum merge distance remains **0.01 mm**;
- do not merge visibly distinct surfaces.

### Protected anatomy

The following remain protected from any positional change:
- face / muzzle / ears;
- skull;
- hands / wrists;
- feet / ankles;
- legs below AC1;
- free tail;
- tail root / gluteal region.

A neck-base duplicate may be welded if:
- it is an exact/coincident duplicate;
- it lies at or below 172.0 cm;
- the merge produces 0.000 mm surface displacement.

This does **not** authorize reshaping or shortening the neck.

## 4. 05AE weld gate

The new baseline must satisfy:

- surface Hausdorff / vertex deviation: 0.000 mm where exact duplicates are collapsed;
- stature and bbox unchanged;
- macro targets unchanged;
- one position-welded component;
- 0 position-welded boundary edges;
- 0 non-manifold edges;
- 0 self-intersections;
- 0 flipped faces;
- 0 degenerate faces;
- protected anatomy unmoved.

Record:
- duplicate groups newly merged versus 05AD;
- vertex count before/after;
- z range;
- exact hashes.

Freeze as:

`GO-05AE_sculpt_safe_baseline.blend`
`GO-05AE_sculpt_safe_baseline.glb`

Status:

**05AE EXTENDED SEAM-WELD PASS / FINAL AC1 BASELINE FROZEN**

If this cannot be achieved exactly, STOP:
**05AE EXTENDED SEAM-WELD FAIL / HUMAN RETOPOLOGY REQUIRED**

## 5. Final AC1 retry

If the 05AE baseline passes, perform one final UI-only AC1 sculpt.

### Mask placement change

The head/neck protection mask edge must be placed **at or below the welded upper boundary**, not above it.

Target approximately:
- mask/protection transition at **171.0–171.5 cm**;
- no brush falloff may reach unwelded seam territory above 172.0 cm.

The lower torso/hip mask should use a broader/softer transition rather than a hard edge exactly at z 117 if normal UI permits.

## 6. Sculpt direction

Keep the successful direction from the rejected retries:

- flatten pectoral projection;
- soften/remove central pec split and hard lower-pec shelf;
- further reduce deltoid cap;
- soften abs and serratus;
- reduce love-handle/bodybuilder flank read;
- preserve the broad/deep Gorrund thorax;
- preserve neck length and macro skeleton.

The retry should be at least as visually neutralized as the 05AD retry.

## 7. Local flip-site cleanup authority

Within the same final AC1 checkpoint, after the main sculpt:

If isolated face flips or near-flips remain at the previously known sites, Claude may perform **tiny UI-only local corrective strokes** using:
- light Smooth / Surface Smooth;
- very restrained Flatten;
- Edit-mode local vertex movement only if necessary.

This cleanup must be:
- localized to the actual defect;
- visually imperceptible outside the local surface;
- not a new broad sculpt pass.

No more than **two micro-cleanup cycles** may be used before final validation.

Do not use scripts to author the correction.

## 8. Final AC1 gates

Required for PASS:

- topology coherent relative to the 05AE baseline;
- 0 opened welded seams;
- 0 self-intersections;
- 0 flipped faces;
- 0 degenerate faces;
- one position-welded component;
- 0 boundary;
- 0 non-manifold;
- stature/bbox unchanged;
- macro targets preserved;
- head/hands/feet/free-tail unmoved;
- no meaningful movement outside AC1 region;
- no new crease/ridge/dent/shelf artifacts;
- clear visual reduction of pec/deltoid/abs/serratus heroic anatomy.

### PASS

Return:

**05AC AC1 SAFE IMPROVEMENT / READY FOR AC2**

Then STOP. Do not start AC2 in this order.

### FAIL

If this final retry still cannot meet the zero-defect technical gates:

**05AC AC1 FINAL RETRY FAILED / HUMAN SCULPTOR OR RETOPOLOGY REQUIRED**

Then STOP. No further autonomous AC1 retry loop.

## 9. State

Until AC1 PASS:
- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED;
- no LOW / blind final acceptance / scaffold / D4 / UE5 / production rigging / creator implementation.

## 10. Return

Commit:
`reviews/claude-rac-rm-ot-05ae-extended-seam-weld-final-ac1-gate.md`

Evidence:
`reviews/rac-rmot05ae-evidence/`
