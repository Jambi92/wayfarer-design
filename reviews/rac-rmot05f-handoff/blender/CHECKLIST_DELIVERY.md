# Delivery checklist — Gorrund hand-sculpt (RM-OT-05G)

## Return package (one folder per version ID, e.g. `GO_sculpt_S1/`)

| File | Required | Notes |
|---|---|---|
| `GO_sculpt_S1_r6.obj` | **yes** | Written by `g_export.py` only. Never hand-edited, never written by Blender's own OBJ exporter |
| `GO_sculpt_S1_r6_export_report.json` | **yes** | Written by `g_export.py` next to the OBJ |
| `GO_sculpt_S1_preflight.txt` | **yes** | Output of `g_preflight.py`, ending `PREFLIGHT PASS` |
| `GO_sculpt_S1_manifest.json` | **yes** | From `MANIFEST_TEMPLATE.json` |
| `views/GO_SCULPT_BASE_{F,Q,P,RQ}_{grey,sil}.png` | **yes** | From `g_views.py` |
| `views/PREVIEW_{low,narrow,broad}_*` and the `g_preview.py` console line | recommended | Persistence evidence |
| `GO_sculpt_S1_work.blend` | if available | The working file |
| High-resolution detail (subdivided mesh, displacement / normal map) | optional | Separate files, clearly named. **Never a replacement for the base OBJ**; not validated in this gate |

## Receipt (repository side, unchanged)

1. Check `sha256(GO_sculpt_S1_r6.obj)` against the manifest and the export report.
2. Run `python3 tools/rac/w1/rmot05f_drivers/f_reentry.py GO_sculpt_S1_r6.obj S1`:
   - ingest I1–I6;
   - builds at reference, low, Narrow and Broad;
   - every 05D / 05E guard;
   - transport report.

   **Any failure:** return to the sculptor with the report. Thresholds are never relaxed.
3. Only after re-entry passes: run the replicated blind gate.
   - `f_blind.py S1 run1`, `run2` (and `run3` if needed);
   - 3 fresh uninformed scorers per run, with `f_scorer_prompt.md` verbatim;
   - `f_tally.py` (G1–G7, every run).

   A pass in one run and a fail in another is a fail.
4. Only after both gates pass may the authorized combined Stage C run (frozen Grask E3 + the validated Gorrund sculpt). Nothing is promoted automatically. Promotion needs the author gate.
