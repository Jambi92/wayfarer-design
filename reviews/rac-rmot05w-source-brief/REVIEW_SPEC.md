# Gorrund source — whole-body and body-only review specification (RM-OT-05W §5, §6)

This is the gate a new source must pass **before** any cleanup, metric validation or scaffold work.

Passing it makes the mesh an **accepted source for bounded corrections only**. It does not make it an ARM or biological canon (order §5).

## 1. What is submitted for review (no edits yet)

Everything is rendered from an **untouched working copy** of the immutable source master. Workbench, neutral grey, orthographic, common ground line and grid (RA L74).

1. **Whole organism:** front, left profile, back and front 3/4, with the leonine head and tail.
2. **Body only:** the same views with the head removed at the neck root and the tail hidden.
   - The tail is separated as a **clean connected component or cut at the tail root**, never masked by distance.
   - Every body-only tile must pass `tools/rac/w1/rmot05w_drivers/w_tile_check.py`: one connected silhouette, no fragment of 12 px or more. A contaminated tile blocks the sheet. This is the 05V tail-fragment fix.
3. **Matched-height exhibit:** the candidate beside the frozen controls (`blind-protocol/control_set_labelled.jpg`: MF and SK ref / nar / brd / low, Grask E3 ref / low), normalized to the same displayed height.
4. **Provenance:**
   - source-master path and SHA-256;
   - job record and tier;
   - the input image(s) and the prompt;
   - every deviation from `SOURCE_BRIEF.md`.

## 2. The four questions (order §5)

Each is answered **yes / no / unclear** with the views that show it.

| Q | Question | Main evidence | Checklist items |
|---|---|---|---|
| Q1 | Coherent adult organism with Gorrund structural identity **at neutral composition**? | Body-only F / P / B / 3/4 | B1–B4, E1 |
| Q2 | Distinct from enlarged human or Skarn, rangy Grask, bodybuilder and ogre caricature once head, tail, equipment and presentation are neutralized? | Matched-height exhibit | B1–B5, E2 |
| Q3 | Source pose, feet, visible landmarks and continuous transitions suitable from the start? R-6 within a rigid or semi-rigid repose; five toes; landmarks visible. | Profile + feet close-ups | A1–A2, C5–C8, B6 |
| Q4 | Surface good enough that later work can stay local? No repair needed on more than a few small, named regions. | Close-ups of neck / girdle, thorax / back, pelvis / hip, knee / ankle, hands, feet | D1–D5 |

**Decision:**
- **ACCEPT AS SOURCE:** all four are yes.
- **REVISE AT SOURCE:** a new image or generation, or a sculptor revision.
- **REJECT.**

Beauty, technical cleanliness and numeric protection never count as a pass on their own (order §5).

## 3. Blind readability (after source acceptance only)

This replaces running the known-invalid 05V protocol again (order §6). Before any fresh scoring:

1. **Clean sheets.** Every candidate and control tile passes `w_tile_check.py`. The complete control set is shown clean (`blind-protocol/control_set_labelled.jpg`, `tile_check_controls.json`: 20 / 20 single-island). The 05V candidate profile tile is shown failing the same check (`tile_check_05V_candidate.json`: islands of 56,241 and 1,701 px). This proves the check catches the defect the 05V scorers saw.
2. **Surface-style confound (new, flagged for pre-registration).**
   - The frozen controls are smooth MPFB-derived bodies.
   - A Rodin or sculpted source carries real surface detail, so the candidate could be picked out by rendering style alone.
   - The pre-registration for the new gate must state how this is handled, for example:
     - the same workbench shading and resolution for all tiles;
     - silhouette-only criteria counted separately;
     - an explicit scorer question on "surface style vs body structure".
   - It must not "fix" this by smoothing the candidate's structural anatomy.
3. **LOW companion.** A validation-only LOW derivative per `LOW_PREREGISTRATION.md`. Without it, C1 and C5-LOW cannot be evaluated. If no credible LOW can be made, report that as a capability dependency rather than running a gate that cannot pass.
4. **Criteria.** The C1–C5 criteria and the mechanical evaluator (`v_gate_eval.py`, extended for LOW) are frozen **before** scoring. They are not weakened afterwards.
