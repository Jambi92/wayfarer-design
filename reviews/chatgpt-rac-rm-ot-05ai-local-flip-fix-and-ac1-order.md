# RAC RM-OT-05AI — author-authorized local flip/sliver fix and AC1 rerun

**Authority:** Tyler authorizes Claude to perform the local fix instead of requiring a human sculptor.
**Date:** 2026-10-16.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05ah-hard-protection-ac1-gate.md` (88e54b4).

## 1. Author ruling

The 05AH result is close enough that a human sculptor is not required yet.

Claude is hereby authorized to perform a **strictly bounded local mesh-quality / flip-prevention fix** in the identified problem neighborhoods, then rerun AC1 once.

This is a narrow exception to the prior stop condition.

## 2. Source baseline

Start only from the frozen 05AF baseline:

`GO-05AF_full_sculpt_safe_baseline.blend`
SHA-256:
`6ef02c298db3cd89d93d8aafc6f2a3580f568945c869cbf7af445b51ff93edb8`

Do **not** start from the rejected 05AH sculpt result.

## 3. Known problem neighborhoods

### 3A. Recurring protected flip sites from earlier passes
- face `643992`
- face `686657`
- face `907533`

### 3B. New 05AH hard-mask-edge flips
- face `441095`
- face `448814`
- face `468838`
- face `919029`

Work only in these faces and their immediate one-ring / two-ring neighborhoods as needed.

## 4. Authorized local quality-fix pass

Before sculpting, create one local working derivative.

Allowed only inside the seven listed neighborhoods:

- tiny Edit Mode vertex slide / relax / reposition;
- local edge rotate / edge flip;
- local retriangulation if needed;
- tiny local cleanup to improve triangle quality and prevent inversion under nearby sculpt strokes or mask transitions.

Forbidden:
- broad sculpting during this prep pass;
- remesh / Dyntopo / voxel / decimate / shrinkwrap;
- moving vertices outside the local repair neighborhoods;
- changing silhouette or macro form;
- touching protected regions.

### Shape-preservation rule
- Outside repair neighborhoods: **0.000 mm** movement required.
- Inside repair neighborhoods: keep the surface visually identical, with no visible silhouette change in normal review views.
- Target local nearest-surface deviation: **<= 0.5 mm**, preferably lower.

### Prep gate
The repaired pre-sculpt baseline must have:
- 0 opened seams;
- 0 self-intersections;
- 0 flipped faces;
- 0 degenerate faces;
- 1 component / 0 boundary / 0 non-manifold;
- head / hands / feet / tail / tail junction / genital / perineal fold unchanged;
- stature and bbox unchanged.

If prep passes, freeze as:

`GO-05AI_local_quality_baseline.blend`
`GO-05AI_local_quality_baseline.glb`

Status:
**05AI LOCAL QUALITY PREP PASS / AC1 RETRY AUTHORIZED**

If prep itself cannot pass cleanly:
**05AI LOCAL QUALITY PREP FAILED / HUMAN SCULPTOR REQUIRED**
STOP.

## 5. AC1 rerun from 05AI baseline

If and only if the 05AI prep passes, rerun AC1 once.

Use the same successful hard-protection strategy as 05AH, with these requirements:

### Protection rules
- If any torso/hip mask smoothing is needed, do it **before** the final head mask.
- Final head / upper-neck mask must stay hard.
- No global Smooth Mask after the head mask exists.
- No trap strokes within 3 cm of the head boundary.
- The three old recurring flip neighborhoods and the four repaired neighborhoods may be lightly feather-protected if needed, but do not let mask-edge pinning recreate flips.

### AC1 sculpt targets
- flatten pec projection;
- soften/remove central pec split;
- reduce lower-pec shelf;
- soften abs and serratus;
- reduce deltoid cap where safe;
- reduce flank / love-handle bodybuilder bulk;
- preserve broad/deep Gorrund frame.

Do not sculpt:
- head / upper neck;
- arms below the shoulder transition;
- legs;
- glutes;
- tail;
- genital / perineal protected interfaces.

## 6. AC1 pass gate

Required for PASS:
- 0 opened seams;
- 0 self-intersections;
- 0 flipped faces;
- 0 degenerate faces;
- 1 component / 0 boundary / 0 non-manifold;
- head displacement 0.000 mm;
- tail / tail junction / genital / hands / feet / perineal fold 0.000 mm;
- stature and bbox unchanged;
- macro proportions unchanged;
- visible improvement versus 05AF:
  - abs/serratus reduced,
  - pec split softer,
  - pec projection reduced,
  - deltoid cap reduced,
  - no new dents / shelves / melt.

### PASS
Return:
**05AI AC1 PASS / READY FOR AC2**

Then STOP. Do not begin AC2 in this order.

### FAIL
If AC1 still fails technically after the local quality pass:
**05AI LOCAL FIX + AC1 FAILED / HUMAN SCULPTOR REQUIRED**

Then STOP. No further autonomous AC1 loop.

## 7. Evidence required

Return:
- prep baseline .blend + GLB hashes;
- exact list of vertices/faces changed in the prep pass;
- local deviation report for the repair neighborhoods;
- AC1 geometry gate JSON;
- protected-region displacement report;
- whole/body-only F/P/B/3/4;
- torso front/profile/3/4 comparison against 05AF and 05AH;
- overlay proving 0 seams / 0 flips if PASS.

## 8. Return

Commit:
`reviews/claude-rac-rm-ot-05ai-local-flip-fix-and-ac1-gate.md`

Evidence:
`reviews/rac-rmot05ai-evidence/`
