# RM-OT-05X R1 evidence: revised Gorrund GLB `base_1.glb` (no repair)

**Report:** `reviews/claude-rac-rm-ot-05x-r1-revised-gorrund-source-review.md`. Recommendation: **REVISE AT SOURCE** (the direction is improving).

**Source file:** `base_1.glb`, SHA-256 `b0214fcfcf157da9b8e457a110fcb78ea5ae88ec14f8a53aea159efabb5d5973`, 31,543,564 bytes. The master is stored at `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Male-05X-R1\` (stored as `base_1.glb.part000` + `.part001` with `REJOIN.txt`, because the file is over the 30 MB transfer limit; the rejoined file must hash to `b0214fcf…`).

## views/

- `00_file_overview_three_figures.jpg`: the untouched file, seen from the front and the back.
- `00b_each_figure_canonical.jpg`: all three figures, each shown with a rigid display rotation only.
- `01`, `03`–`09`: whole-body views and close-ups of fig2.
- `02`: fig2 body-only views from a disposable diagnostic copy (head and tail hidden).
- `10`: matched displayed-height exhibit comparing fig2 with the previous candidate and the frozen controls.

## geometry/

- `inspection.json`: read-only facts for the whole file.
- `figures_split.json`: per-figure topology and the display transforms.
- `bodyonly_diagnostic_fig2.json`: the diagnostic cut record.
- `tile_check_bodyonly.json`: 6 of 6 tiles clean.

## Tools

The new tools in `tools/rac/w1/rmot05x_drivers/` are `x_split.py`, `x_tailtrack.py` and `x_tailcut.py`.

- `x_tailcut.py` is an earlier attempt kept for the record. Its seed selection picked a hand on fig0 and fig1, so it is **not used** for any evidence.
- `x_inspect.py` was revised so that it computes generic levels only.
- Region-specific findings for 05X are in `reviews/rac-rmot05x-source-review/geometry/scan_findings.json`.
