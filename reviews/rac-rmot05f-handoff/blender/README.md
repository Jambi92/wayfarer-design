# Gorrund hand-sculpt — Blender production companion (RM-OT-05G)

**Order:** `reviews/chatgpt-rac-rm-ot-05g-blender-sculpt-production-handoff-order.md`
**Governs anatomy:** the frozen brief `reviews/gorrund-rm-ot-05f-hand-sculpt-production-brief.md` (canon governs any conflict). This companion is **tooling only**: it adds no anatomy, no target shape and no Gorrund body.
**Status:** Gorrund **EXTERNAL SCULPT REQUIRED — AWAITING ASSET**. RM-OT-05 OPEN; Stage C blocked; Grask E3 frozen.

The route is:
1. the supplied start mesh;
2. sculptor edits that **move existing vertices only**;
3. the **controlled exporter** writes `GO_sculpt_<ID>_r6.obj`;
4. the unchanged 05F re-entry validation;
5. the replicated blind gate.

## 1. Versions and what was actually tested

| | Blender 4.2.0 LTS | Blender 5.0.1 |
|---|---|---|
| Scene setup, save, reopen, Edit / Sculpt mode enter + exit, controlled export: **unedited round trip bit-exact** (every `v` and `f` record identical to the template) | ✔ | ✔ |
| Exporter refuses all 17 negative fixtures and writes nothing | ✔ | ✔ |
| Standalone preflight fails all 5 negative OBJ fixtures | ✔ | ✔ |
| Persistence preview: unedited base equals the route meshes; the 05F T1 tooling fixture agrees with the built 05F states (p90 ≤ 0.018 cm) | ✔ | ✔ |
| Matched view captures render (8 PNGs, body only) | ✔ | ✔ |

Results are in `tooling_evidence/blender_4.2.0/` and `tooling_evidence/blender_5.0.1/`.

**How these were run.** Headless, through the official `bpy` Python module of each version (the same Blender build, without the UI), by `tools/rac/w1/rmot05g_blender/g_tests.py`.

**Not tested here:**
- the desktop UI;
- the `blender` command-line binary;
- real brush strokes.

The UI steps in §4 are the documented route. The first genuine sculptor session should confirm them, and the exporter's checks catch any deviation regardless. Blender 3.x is not supported: its sculpt mask is stored differently.

## 2. Coordinates, units and the mirror note (read once)

- **1 Blender unit = 1 cm.** The setup sets Scene > Units to *None* with unit scale 1.0. Nothing converts units.
- **Z up, ground z = 0, +Y anterior (the body faces +Y), +X = the body's left.** These are the package's source coordinates. They are kept exactly: no axis conversion on import, none on export.
- **The data is a mirror image** (+Y front with +X left is left-handed). In the viewport you therefore see a mirrored body. That is harmless for sculpting, but the brief's "left" is always the **+X** side.

**Viewport navigation:**

| To see the body's… | Use |
|---|---|
| Front | **Ctrl + Numpad 1** (Blender's *Back* view: it looks from +Y) |
| Back | Numpad 1 |
| Left side (+X) | Numpad 3 |
| Right side | Ctrl + Numpad 3 |

`GO_VIEW_ANATOMICAL` is a display-only linked duplicate with object scale y = −1. It shows the body anatomically correct, exactly like the 05D / 05E sheets, and the view captures render it.

**Blender's own OBJ importer and exporter are not used.** Blender 4.2 and 5.0 have no "Keep Vert Order" / "Split" option. The brief's §1 exporter note was written for the legacy importer and is **superseded here** by the controlled exporter. Measured, for information (`tooling_results.json`, `R0_*`):
- the native importer with default axes keeps vertex order and faces, but adds a +90° X object rotation (world coordinates off by up to 240 cm);
- with *Forward Y / Up Z* it reproduces the template to float precision (7.6 × 10⁻⁶ cm).

Neither is needed. The setup parses the OBJ itself in file order, and the exporter writes the template's own face records.

## 3. Files

| Path | What |
|---|---|
| `scripts/g_setup.py` | **Scene setup** (run in Blender) |
| `scripts/g_export.py` | **Controlled exporter** (run in Blender): writes `GO_sculpt_<ID>_r6.obj` plus `GO_sculpt_<ID>_r6_export_report.json`, or refuses |
| `scripts/g_preview.py` | **Persistence preview** (run in Blender): low composition, Narrow, Broad |
| `scripts/g_views.py` | **Matched view captures** (run in Blender): F / ¾ / P / rear ¾, grey and silhouette, body only |
| `scripts/g_preflight.py` | **Standalone preflight** (Python 3 + numpy, no Blender): same thresholds as the 05F ingest |
| `scripts/SHA256SUMS.txt` | Hashes. The scripts are byte-identical copies of `tools/rac/w1/rmot05g_blender/` |
| `transport/` | Persistence-preview data generated from the accepted route by `g_make_transport.py`: low / Narrow / Broad route meshes, their true floors, and the transport fields T, s. **Not sculpt targets** |
| `CHECKLIST_SCULPTOR.md` | Step-by-step for the sculptor |
| `CHECKLIST_DELIVERY.md` | What to return and how it is received |
| `MANIFEST_TEMPLATE.json` | Delivery manifest to fill in |
| `tooling_evidence/` | Round-trip and rejection-test results for both versions, plus tooling view captures (unedited start mesh). **Not a sculpt, not a candidate** |

## 4. The scene that setup builds

| Object / collection | Purpose | Exported? |
|---|---|---|
| `GO_SCULPT_BASE` (collection `SCULPT_EXPORT`) | **The only object you sculpt.** Transforms locked at identity | **Yes, the only one** |
| `GO_SOURCE_REFERENCE` (`REF_LOCKED_NO_EXPORT`) | Immutable copy of the start mesh; hidden, unselectable | No |
| `GO_true_floor`, `GO_old_lean`, `GO_low_route` (`GUIDES_NO_EXPORT`) | Guides, wireframe, unselectable, hidden at start (eye icon to show). True floor = **hard inner limit** | No |
| `JOINT_*`, `GROUND_z0`, `STATURE_230.90` (`OVERLAYS_NO_EXPORT`) | Accepted R-6 joint heads, ground, stature marker | No |
| `GO_VIEW_ANATOMICAL`, `CAM_F` / `CAM_Q` / `CAM_P` / `CAM_RQ` (`VIEW_NO_EXPORT`) | Sheet-convention display duplicate and cameras | No |
| `PREVIEW_low` / `PREVIEW_narrow` / `PREVIEW_broad` (`PREVIEW_NO_EXPORT`, made by `g_preview.py`) | Transport previews beside the base at x = +110 / +220 / +330 cm | No |

On `GO_SCULPT_BASE`:

**Vertex groups:**
- `NO_TOUCH_head_neck`, `NO_TOUCH_hands_digits`, `NO_TOUCH_toes_forefoot`, `NO_TOUCH_all`;
- `FAM_A` … `FAM_F` (editing jurisdiction only; the brief text governs anatomy).

These come from the exact source indices in `data/regions.json` (verified).

**Sculpt mask** = `NO_TOUCH_all`: masked areas are protected. Masks are **editing aids**. The exporter's numeric checks enforce the contract: no-touch zones within 0.5 cm, stature and ground within 0.05 cm.
- If the mask is cleared or edited, restore it exactly: open `g_setup.py`, set `REMASK_ONLY = True`, and *Run Script*. This rewrites the mask from `NO_TOUCH_all` and changes no coordinate (verified). CLI: `--remask`.

**Colour attribute** `rac_regions`: families A–F in colour, no-touch zones dark. To see it: *Viewport Shading > Solid > Color: Attribute*.

**Hidden bookkeeping attributes** — never edit or delete them:
- `rac_src_index`: each vertex's template index. **This is how the exporter proves correspondence.**
- `rac_src_co`: template position.

The base shares its mesh with `GO_VIEW_ANATOMICAL`. As a result, Blender refuses to *apply* modifiers to it. That is intended: never apply a modifier, remesh or subdivision to the base.

## 5. Commands

**GUI** (the normal route):
1. Open Blender.
2. Go to *Scripting > Open* and choose `blender/scripts/g_setup.py`, then *Run Script*.
3. *File > Save As* your working file, e.g. `GO_sculpt_S1_work.blend`, in a folder **outside** the frozen package.
4. If the scripts cannot find the package, set `PACKAGE_ROOT = r"…\rac-rmot05f-handoff"` at the top of each script.

**CLI** (documented; verified through the `bpy` module, not with the binary):

```
blender --background --python <pkg>/blender/scripts/g_setup.py -- --package <pkg> --out GO_sculpt_S1_work.blend
blender --background GO_sculpt_S1_work.blend --python <pkg>/blender/scripts/g_preview.py -- --package <pkg> --save
blender --background GO_sculpt_S1_work.blend --python <pkg>/blender/scripts/g_views.py -- --outdir views --previews
blender --background GO_sculpt_S1_work.blend --python <pkg>/blender/scripts/g_export.py -- --package <pkg> --id S1 --sculptor "Name" --outdir .
python3 <pkg>/blender/scripts/g_preflight.py GO_sculpt_S1_r6.obj --package <pkg>
```

**On receipt** (repository side, unchanged 05F):

```
python3 tools/rac/w1/rmot05f_drivers/f_reentry.py GO_sculpt_S1_r6.obj S1
```

Then the replicated blind gate: `f_blind.py S1 run1|run2[|run3]`, `f_scorer_prompt.md` verbatim, `f_tally.py`.

## 6. Exporter contract

`g_export.py` writes **nothing** unless all of these hold:

| Check | Requirement |
|---|---|
| X1 object | No parent or constraints; location, rotation (Euler / quaternion / axis-angle), scale and every delta are identity, and the evaluated world matrix is identity |
| X2 counts | 13 380 vertices and the template face count |
| X3 identity | `rac_src_index` exactly 0..13379 in order. A count check alone would miss a reorder; this does not |
| X4 faces | Every polygon equals its template face record: same vertices, start and winding |
| X5 state | No shape keys and no Multires |
| X6 values | All coordinates finite |
| X7 template | Template SHA-256 equals the one stored at setup |
| X8 stature / ground | Within 0.05 cm |
| X9 no-touch | Every NO_TOUCH vertex within 0.5 cm |

**Output:**
- template-order positions;
- the template's own face records, verbatim;
- unmoved vertices keep their template text, so an unedited export is bit-identical;
- a JSON export report.

The exporter never uses nearest-neighbour matching, never repairs and never reorders.
