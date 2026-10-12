# Sculptor checklist — Gorrund hand-sculpt in Blender (RM-OT-05G)

Read first:
- `../../gorrund-rm-ot-05f-hand-sculpt-production-brief.md` (anatomy: governs);
- `README.md` (tooling).

Blender 4.2 LTS or 5.0. `<pkg>` = the `rac-rmot05f-handoff` folder.

## A. Open and set up

1. [ ] Copy the whole `rac-rmot05f-handoff` folder to your machine. Keep it unchanged; it is frozen.
2. [ ] Verify the script hashes. In a terminal in `blender/scripts`, run `sha256sum -c SHA256SUMS.txt`. On Windows: `certutil -hashfile g_setup.py SHA256` per file, compared by eye.
3. [ ] Open Blender. In *Scripting*, open `blender/scripts/g_setup.py` and choose *Run Script*. The console prints `RAC_SETUP {...}` with 13380 vertices and 26756 faces.
4. [ ] *File > Save As* a working copy **outside** the package: `GO_sculpt_S1_work.blend`. Save incremental copies as you go.
5. [ ] Confirm the start state:
   - only `GO_SCULPT_BASE` is selectable;
   - its N-panel transform is Location 0 0 0, Rotation 0 0 0, Scale 1 1 1, all locked;
   - Scene > Units = None.

## B. Protect

6. [ ] Enter Sculpt mode on `GO_SCULPT_BASE`. Head / neck, hands / digits and toes / forefoot appear masked (dark).
   - If the mask is ever lost, run `g_setup.py` with `REMASK_ONLY = True`.
7. [ ] To see the families: *Viewport Shading > Solid > Color: Attribute* (`rac_regions`). The colours show editing jurisdiction only; **the brief text governs anatomy**.
8. [ ] Show the guides when needed (eye icons in `GUIDES_NO_EXPORT`):
   - `GO_true_floor` is the **hard inner limit**;
   - `GO_old_lean` is context only (you may go inside it);
   - `GO_low_route` is the low-composition body.

## C. Sculpt (move existing vertices only)

9. [ ] Use only brushes that move vertices: Grab, Draw, Clay Strips, Flatten / Fill / Scrape, Pinch, Crease, Smooth, Layer, Inflate, Elastic Deform, Snake Hook (with care).
10. [ ] **Never** use any of these on `GO_SCULPT_BASE`:
    - Dyntopo;
    - Voxel / Quadriflow Remesh;
    - Multires;
    - an applied Subdivision;
    - Decimate, Weld / Merge, Merge by Distance, Dissolve, Triangulate, Sort Elements, Separate / Join;
    - shape keys;
    - re-posing (armatures, proportional transforms of whole limbs), re-scaling, re-centring, re-grounding.

    The exporter refuses every one of these.
11. [ ] Work Symmetry X on: the body is bilaterally symmetric about x = 0.
12. [ ] Build the six hard-form families of brief §4, within the canon guardrails of brief §3:
    - **A — trunk S2–S5:**
      - sternal / anterior plate;
      - lateral thoracic planes with **strong but radiused** plane breaks;
      - costal lower border;
      - an anatomically shaped, radiused section, **never** rectangular, boxy, mechanically slab-sided or cylindrical (Q1);
      - the read must not rely on a human pinched waist. That is a reference-direction goal, not a race rule.
    - **B — posterior axial load path:** paired broad paraspinal columns, interscapular plane, sacral plate into the hamstring; straight / inclined line; no hump, no buttock, no lumbar hollow.
    - **C — pelvis → thigh:** hip plate, trochanteric shelf, planar lateral thigh; step at pelvis → thigh only; no lateral outrigging.
    - **D — knee / shank / ankle:**
      - flush patellar plate and condyle blocks (never bulbous, spiked or armor-like);
      - squarish shank with tibial plane and tendon column;
      - ankle **narrower than the calf**;
      - not a pillar, not a human thick-thigh / thin-shin taper.
    - **E — elbow / forearm / wrist:** integrated elbow block (not a knob); flattened forearm with tendon border; broad flattened wrist (not a column); hands unchanged.
    - **F — shoulder girdle / neck root:** low broad girdle, trapezius plane, shoulder block; no deltoid cap, no overhang, no hump.
13. [ ] Limbs (D, E) have about 1.5 cm of inward room (`figures/floor_margin.png`). Build those forms mainly by reshaping and outward planes.
14. [ ] **Not as identity:**
    - bulk, obesity, muscle amount;
    - posture, crouch, hunch or digitigrade illusion;
    - oversized hands or feet;
    - face, hair, texture, clothing;
    - any Grask cue (scapular hump, high calf with long cord).

## D. Inspect

15. [ ] Check every family against brief §4 and §5 in front (Ctrl + Numpad 1), ¾, profile (Numpad 3) and rear ¾. The data is mirrored; `GO_VIEW_ANATOMICAL` (eye icon) shows the anatomically correct body.
16. [ ] Run `g_preview.py`. It builds `PREVIEW_low` / `narrow` / `broad` beside the base and prints how many vertices of each state fall inside that state's true floor because of the sculpt (`new_inside_caused_by_sculpt`; aim for 0).
    - **Every family must still read on `PREVIEW_low`.**
    - Never judge persistence by scaling the body.
17. [ ] Run `g_views.py` (and `--previews` from the CLI if wanted). It writes F / ¾ / P / rear ¾ grey and silhouette PNGs, body only, to `views/` next to your `.blend`. Compare them with `../evidence/05e/*` (failed examples) and `../evidence/05d/d_GR_*` (Grask contrast only).

## E. Export and preflight

18. [ ] Save the `.blend`.
19. [ ] In `g_export.py` set `SCULPT_ID = 'S1'` (next delivery `S2`, …) and `SCULPTOR = 'your name / studio'`, then *Run Script*.
    - It prints `RAC_EXPORT PASS` and writes `GO_sculpt_S1_r6.obj` + `GO_sculpt_S1_r6_export_report.json` next to the `.blend`.
    - Or it prints `RAC_EXPORT REFUSED` with the failing check. Fix the cause. Never edit the OBJ by hand.
20. [ ] Run `python3 <pkg>/blender/scripts/g_preflight.py GO_sculpt_S1_r6.obj --package <pkg>`. It must print `PREFLIGHT PASS`.

## F. Submit

21. [ ] Fill in `MANIFEST_TEMPLATE.json` as `GO_sculpt_S1_manifest.json` and deliver per `CHECKLIST_DELIVERY.md`.
