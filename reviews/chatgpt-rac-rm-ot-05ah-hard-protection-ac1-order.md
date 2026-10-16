# RAC RM-OT-05AH — hard-protection AC1 retry from 05AF; isolate head edge and recurring flip sites

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05AG stop.
**Date:** October 16, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05ag-gorrund-composition-sculpt-gate.md` (a94bcc6).

## 1. Ruling

05AF remains the valid sculpt-safe baseline.

05AG AC1 failed for two known, bounded reasons:
1. global Smooth Mask softened the protected head edge and trap strokes reached protected head-side seams;
2. the same three lower-pec / armpit faces flipped under smoothing.

Do not alter 05AF topology again in this order.

Retry AC1 once using **hard protection**, not broader geometry changes.

## 2. Baseline

Start only from:

`GO-05AF_full_sculpt_safe_baseline.blend`
SHA-256:
`6ef02c298db3cd89d93d8aafc6f2a3580f568945c869cbf7af445b51ff93edb8`

Do not use the rejected 05AG AC1 as a starting point.

## 3. Hard head protection

The head / upper-neck protection must remain hard for the entire sculpt.

Required sequence:

1. If any torso/hip mask softening is desired, do it **before** placing the final head mask.
2. Apply the final hard head/upper-neck box mask afterward.
3. Do **not** run global `Mask > Smooth Mask` after the head mask exists.
4. Do not sculpt the trapezius within **3 cm** of the protected head boundary.
5. For this AC1 retry, it is acceptable to leave the upper trap slope essentially unchanged.

The AC1 objective is torso/chest/shoulder soft-tissue neutralization; the trap can be revisited later only if a safe local method is available.

Required head displacement after sculpt: **0.000 mm**.

## 4. Recurring flip-site protection

The three recurring face sites are:

- approximately `(15.9, -54.1, 146.1) cm`
- approximately `(13.0, -56.2, 146.3) cm`
- approximately `(-19.3, -40.9, 153.2) cm`

These are measured in the established 05AF/05AG evidence frame.

Before sculpting:
- locate these three faces / their immediate one-ring neighborhoods;
- apply a small hard sculpt mask around each site through normal Blender UI;
- protect enough of the local one-ring that Smooth/Flatten falloff cannot rotate those faces through inversion.

Do **not** move or repair these faces in this order. This is protection, not geometry authoring.

Record the exact masked face/vertex IDs in the return report.

## 5. AC1 sculpt scope

UI-only Blender sculpt.

Allowed targets:
- abs;
- serratus;
- central pec split;
- lower-pec shelf;
- pec projection;
- deltoid cap away from the protected flip neighborhoods;
- love-handle / flank bodybuilder bulk.

Do not sculpt:
- upper traps within 3 cm of head boundary;
- protected head/upper neck;
- the three flip-site masks;
- arms below shoulder transition;
- legs;
- glutes;
- tail;
- genital / perineal protected interfaces.

## 6. Method

Allowed:
- Smooth / Surface Smooth;
- restrained Flatten / Scrape;
- restrained Grab only for soft-tissue volume;
- normal UI masks / face sets.

Forbidden:
- global Smooth Mask after final hard protection is applied;
- Python console;
- scripting workspace;
- shell;
- scripted strokes;
- topology change;
- Dyntopo/remesh;
- scripted vertex movement.

## 7. AC1 pass gate

Required:

- topology identical to 05AF;
- 0 opened seams;
- 0 self-intersections;
- 0 flipped faces;
- 0 degenerate faces;
- 1 position-welded component;
- 0 boundary / 0 non-manifold;
- head displacement exactly 0.000 mm;
- tail / tail junction / genital / hands / feet / perineal fold 0.000 mm;
- stature and bbox unchanged;
- macro proportions unchanged;
- clear visible improvement versus 05AF:
  - abs/serratus reduced;
  - pec split softer;
  - pec projection reduced;
  - deltoid cap moderately reduced;
  - no new crease / shelf / dent / melted region.

### PASS

Return:

**05AH AC1 PASS / READY FOR AC2**

Then STOP. Do not begin AC2 in this order.

### FAIL

If a new unrelated technical failure appears despite the hard-protection method:

**05AH AC1 HARD-PROTECTION RETRY FAILED / HUMAN SCULPTOR REQUIRED**

Then STOP. No further autonomous AC1 loop.

## 8. Evidence

Return:
- checkpoint .blend + GLB hashes;
- exact masked IDs for the 3 flip neighborhoods;
- full geometry gate JSON;
- protected-region displacement report;
- whole/body-only F/P/B/3/4;
- torso front/profile/3/4 comparison against 05AF and rejected 05AG AC1;
- defect overlay proving zero opened seams/flips if PASS.

## 9. State

Until AC1 PASS:
- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED.

## 10. Return

Commit:
`reviews/claude-rac-rm-ot-05ah-hard-protection-ac1-gate.md`

Evidence:
`reviews/rac-rmot05ah-evidence/`
