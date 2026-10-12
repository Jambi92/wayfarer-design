# START HERE — Gorrund hand-sculpt (Blender)

This folder is the complete sculptor package. Nothing outside it is needed.

**Status:** Gorrund is **EXTERNAL SCULPT REQUIRED — AWAITING ASSET**. You are producing that asset. Nothing in this folder is an accepted Gorrund body.

**About paths in the brief:** the brief names files as `reviews/rac-rmot05f-handoff/…`. That prefix means *this folder*: for example, `reviews/rac-rmot05f-handoff/template/GO_ref_route_r6.obj` is [`template/GO_ref_route_r6.obj`](template/GO_ref_route_r6.obj). Files under `tools/…` are used by the receiving side, not by you.

1. **Read the brief.** [`brief/gorrund-rm-ot-05f-hand-sculpt-production-brief.md`](brief/gorrund-rm-ot-05f-hand-sculpt-production-brief.md) is an exact, frozen copy. It governs the anatomy; canon governs any conflict. It covers:
   - the six hard-form families (§4) and their canon guardrails (§3);
   - Q1: planar anatomical zones on a radiused, anatomically shaped trunk, never rectangular, boxy, mechanically slab-sided or cylindrical;
   - the waist ruling: the read must not rely on a human pinched waist, but this is a reference-sculpt goal, not a race rule.
2. **Use a supported Blender:** 4.2 LTS or 5.0. See [`blender/README.md`](blender/README.md) for:
   - the units (1 unit = 1 cm);
   - the axes (Z up, +Y anterior, +X body left);
   - the mirror note;
   - what the scripts do.
3. **Do the first-session desktop verification:** [`blender/CHECKLIST_SCULPTOR.md`](blender/CHECKLIST_SCULPTOR.md) §0. It is still pending (never done in a desktop session) and is a disposable tooling check, not a sculpt.
4. **Set up and sculpt.** Follow [`blender/CHECKLIST_SCULPTOR.md`](blender/CHECKLIST_SCULPTOR.md) §A–§C:
   - run `blender/scripts/g_setup.py` and save a working copy outside this folder;
   - sculpt only `GO_SCULPT_BASE`, by moving existing vertices;
   - build the six hard-form families directly in the base mesh.

   Forbidden operations stay forbidden even where the exporter cannot detect them (checklist step 10).
5. **Inspect.** Checklist §D:
   - the views;
   - `g_preview.py` for low composition, Narrow and Broad. The preview is advisory: it shows the forms before the pipeline's floor clamp and volume restoration;
   - `g_views.py`.
6. **Export and preflight.** Checklist §E:
   - `g_export.py` with `SCULPT_ID = 'S1'` writes `GO_sculpt_S1_r6.obj` plus its export report, or refuses with the reason;
   - `python3 blender/scripts/g_preflight.py GO_sculpt_S1_r6.obj` must print `PREFLIGHT PASS`.
7. **Return** (see [`blender/CHECKLIST_DELIVERY.md`](blender/CHECKLIST_DELIVERY.md)):
   - `GO_sculpt_S1_r6.obj` and `GO_sculpt_S1_r6_export_report.json`;
   - the preflight output;
   - `views/` (and preview views if made);
   - the working `.blend` if available;
   - `GO_sculpt_S1_manifest.json` (from [`blender/MANIFEST_TEMPLATE.json`](blender/MANIFEST_TEMPLATE.json), including the desktop-verification result).

After delivery, the receiver runs the unchanged re-entry validation and the replicated blind test. Acceptance is decided there, not by the preflight.
