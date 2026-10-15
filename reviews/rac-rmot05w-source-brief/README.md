# RM-OT-05W — Gorrund neutral source brief package

This package covers source selection and readiness only. It is not canon and not an ARM. The report is `reviews/claude-rac-rm-ot-05w-gorrund-source-sculpt-reset-readiness.md`.

## Contents

Start with these:

1. `SOURCE_BRIEF.md`: what the new source must be, with canon citations.
2. `NEGATIVE_CHECKLIST.md`: what rejects a source.
3. `NEGATIVE_REFERENCES_avoid_only.jpg`: labelled images of failed bodies, to avoid only.
4. `SUBMISSION_PACKAGE.md`: the concept-image prompt, Rodin dry-run and submit commands (the submit needs approval), and the sculptor alternative.

Then these:

5. `REVIEW_SPEC.md`: the whole-body and body-only source gate, and the conditions for a later blind gate.
6. `LOW_PREREGISTRATION.md`: draft method for the validation-only LOW derivative.
7. `blind-protocol/`:
   - `control_set_labelled.jpg`: the clean frozen control set;
   - `control_tiles/`: the 20 control tiles;
   - `tile_check_controls.json`: 20/20 clean;
   - `tile_check_05V_candidate.json`: the 05V fragment detected.

## Tools

The tools are in `tools/rac/w1/rmot05w_drivers/`:

- `w_tile_check.py`: single-silhouette contamination gate for blind tiles;
- `w_control_sheet.py`: builds the labelled control exhibit, and refuses to if any tile is contaminated;
- `w_negative_sheet.py`: builds the avoid-only exhibit.
