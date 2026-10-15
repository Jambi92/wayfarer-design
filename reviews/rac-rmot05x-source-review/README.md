# RM-OT-05X evidence: new male Gorrund GLB source review (no repair)

The report is `reviews/claude-rac-rm-ot-05x-new-male-gorrund-source-review.md`. Recommendation: **REVISE AT SOURCE**.

## The source file

- **Name:** `Gorrund.glb`
- **SHA-256:** `1c23b92b7d2faa88ce629d6ccb6d795502d4b704c52af2fcf10b2b34bdd83170`
- **Size:** 30,470,312 bytes
- **Master location:** `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Male-05X\Gorrund.glb`

The master is not copied into this folder or into canon.

## Contents

- `views/`
  - `01`, `03`–`09`: renders of the untouched source;
  - `02`: body-only views from a disposable diagnostic copy (not a repair);
  - `10`: matched displayed-height exhibit next to the frozen controls (display normalization only).
- `geometry/`
  - `inspection.json`: read-only container, topology, quality, self-intersection and approximate level data;
  - `bodyonly_diagnostic_cut.json`: the face-deletion rules used for the diagnostic copy;
  - `tile_check_bodyonly.json`: fragment check, 6/6 clean.

Tools are in `tools/rac/w1/rmot05x_drivers/`: `x_inspect.py`, `x_render.py`, `x_sheet.py` and `x_bodyonly.py`. All are read-only with respect to the source.
