# RAC RM-OT-05G — Blender sculpt production handoff report

**Order:** `reviews/chatgpt-rac-rm-ot-05g-blender-sculpt-production-handoff-order.md` (commit `136321c`)

**Result:** Blender support package prepared and tooling verified headless in Blender 4.2.0 LTS and 5.0.1. **STOP: EXTERNAL SCULPT REQUIRED — AWAITING ASSET.**

The missing deliverable is the sculptor-produced `GO_sculpt_<ID>_r6.obj` derived from `reviews/rac-rmot05f-handoff/template/GO_ref_route_r6.obj`.

## 1. State (unchanged)

| Item | State |
|---|---|
| RM-OT-05 | **OPEN** |
| Grask E3 | Frozen as the accepted developmental direction pending Stage C; not reopened, not promoted |
| Gorrund | Unaccepted; **EXTERNAL SCULPT REQUIRED — AWAITING ASSET**. Every 05C–05E body stays unpromoted |
| Stage C | **Blocked** |
| Other | No D4, no UE5, no canon promotion |

**No new procedural Gorrund body was made.** `arch_sculpt.py` and `race_base.py` were not run or changed, and there was no parameter search.

Two pre-existing 05F tooling fixtures were reused, read-only:
- the T1 fixture (the failed 05D E1 surface as a displacement signal), used to verify the preview against the 05F builds;
- the round-trip OBJ, which went through the authoritative `f_ingest` under the tooling ID `ZZ`.

Neither is a candidate. No frozen anatomy, canon text, validator threshold, scorer prompt or tally rule was changed.

## 2. Correction to the 05F record

The 05F gate said "no Blender … is installed" in this environment. That was wrong.
- The `bpy` module (Blender 5.0.1 as a Python module) was installed. The 05D / 05E sheet renderer has always used it.
- It does not change the 05F conclusion: there is still no human sculptor and no interactive sculpting session here, and a procedural substitute stays forbidden.
- It does mean the Blender tooling below could be executed and verified for real.

For the 4.2 LTS tests, `bpy` 4.2.0 was installed temporarily. Blender 5.0.1 was restored afterwards.

## 3. Package

### Package files — `reviews/rac-rmot05f-handoff/blender/`

| Entry point | File |
|---|---|
| Overview: versions, axes / units / mirror note, scene contents, commands, exporter contract | `README.md` |
| Scene setup (Blender) | `scripts/g_setup.py` |
| Controlled exporter (Blender) | `scripts/g_export.py` |
| Persistence preview, low / Narrow / Broad (Blender) | `scripts/g_preview.py` |
| Matched view captures (Blender) | `scripts/g_views.py` |
| Standalone preflight (Python + numpy) | `scripts/g_preflight.py` |
| Script hashes | `scripts/SHA256SUMS.txt` |
| Sculptor step-by-step | `CHECKLIST_SCULPTOR.md` |
| Return / receipt | `CHECKLIST_DELIVERY.md` |
| Delivery manifest | `MANIFEST_TEMPLATE.json` |
| Preview data (route, true floor, T / s per state; not sculpt targets) | `transport/` + `transport_report.json` |
| Tooling evidence | `tooling_evidence/blender_4.2.0/`, `tooling_evidence/blender_5.0.1/` (incl. 8 tooling view captures), `f_ingest_roundtrip_5.0.1.*` |

### Repository tools — `tools/rac/w1/rmot05g_blender/`

- The same five scripts. The package copies are byte-identical (SHA-256 below).
- `g_make_transport.py`: generates `transport/` from the accepted route and verifies it.
- `g_tests.py`: the headless tooling verification.

### How the contract is met

**Source-order parse.** The OBJ importer in Blender 4.2 / 5.0 has no "Keep Vert Order" / "Split" option. Its actual operator options are recorded in `tooling_results.json`, `R0_operator_options`. So `g_setup.py` parses the template itself in file order and builds the mesh with `from_pydata`:
- no split, merge or sort;
- faces and winding exactly as listed.

**Immutable reference, one editable object.**
- `GO_SOURCE_REFERENCE` is hidden, unselectable and locked.
- `GO_SCULPT_BASE` is the only selectable object; its transforms are locked at identity.
- Guides and overlays sit in separate `*_NO_EXPORT` collections and are unselectable.

**Identity correspondence.** Each vertex stores:
- `rac_src_index`, its template index;
- `rac_src_co`, its template position.

The exporter requires `rac_src_index` to be exactly 0..13379, in order. It never matches by nearest neighbour.

**Protection.**
- Vertex groups and the sculpt mask come from the exact `regions.json` indices: the no-touch sets and `NO_TOUCH_all`, plus `FAM_A`–`FAM_F` as jurisdiction groups.
- A colour attribute shows the regions.
- A verified `REMASK_ONLY` helper restores the mask without touching coordinates.

**Units and axes.**
- Scene units None, scale 1.0: 1 BU = 1 cm.
- Source coordinates are kept as-is: Z up, +Y anterior, +X body left.
- The data is mirror-handed, so a linked display duplicate with scale y = −1 gives the anatomically correct sheet convention for viewing and captures.

**Exporter.**
- It writes template-order positions plus the template's own face records verbatim.
- Unmoved vertices keep their template text.
- It refuses (writes nothing) on: transform, parent or constraint; counts; identity; faces; shape keys / Multires; non-finite values; template hash; stature / ground (0.05 cm); no-touch (0.5 cm).

**Brief §1 "Apply Transform".** This is replaced by the identity requirement. The exporter reads base mesh data in source coordinates and refuses any non-identity object transform. It was proven numerically (§4).

**Persistence preview.**
- Formula: `preview = route_state + s · T · (base − template)`. These are the 05F `sculpt_layer` quantities before the floor clamp and volume layer.
- It reports where a form would be clamped at each state.
- There is no whole-body scaling and no invented shape.

## 4. Verification

Command: `python3 tools/rac/w1/rmot05g_blender/g_tests.py reviews/rac-rmot05f-handoff <out>`, with `RAC_T1_FIXTURE` / `RAC_T1_BUILT` pointing at the 05F tooling fixture and its built states. Run headless through `bpy` 4.2.0 and 5.0.1. **Both: ALL AS EXPECTED.**

| Test | 4.2.0 | 5.0.1 |
|---|---|---|
| R0 native importer (information only): default axes add a +90° X object rotation; *Forward Y / Up Z* keeps order, faces and coordinates (7.6 × 10⁻⁶ cm) | same | same |
| R1 setup → save → reopen → Edit / Sculpt / Object mode → export, unedited: **every `v` and `f` record bit-identical** to the template; max coordinate difference 0; stature Δ 0; ground 0; anchor fit scale 1.000000, rotation 0°, shift 0 | ✔ | ✔ |
| R1 standalone preflight on the round trip: P1–P7 PASS | ✔ | ✔ |
| R1 authoritative 05F `f_ingest` on the round trip (tooling ID ZZ): I1–I6 PASS | — | ✔ |
| R2 every vertex group equals its `regions.json` source index set; `NO_TOUCH_all` equals the union; sculpt mask = `.sculpt_mask` attribute equal to the no-touch set | ✔ | ✔ |
| R2b re-mask restores the mask exactly; coordinates bit-unchanged | ✔ | ✔ |
| **Exporter negative fixtures** (each refused, no file written, expected check failed): N1 delete vertex (X2); N2 random vertex reorder, same count (X3); N3 one face winding flipped (X4); N4 `rac_src_index` removed, i.e. ambiguous identity (X3); N5 object rotation 5° (X1); N6 object scale 1.01 (X1); N7 object translation (X1); N7b delta rotation (X1); N7c quaternion rotation (X1); N8 hand moved 1 cm (X9); N9 shape keys (X5); N10 Multires (X5); N11 mesh lifted 2 cm (X8, X9); N12 voxel remesh (X2); N13 applied subdivision (X2); N14 NaN coordinate (X6); N15 merge by distance 0.5 cm (X2) | 17 / 17 | 17 / 17 |
| **Preflight negative OBJ fixtures** (each FAIL): missing vertex; reordered with remapped faces; reordered with faces unchanged; face winding; uniform scale 1.02 | 5 / 5 | 5 / 5 |
| Preview, unedited base: each preview equals its route (max 7.6 × 10⁻⁶ cm, float32); 0 new floor penetrations | ✔ | ✔ |
| Preview with the T1 tooling fixture vs the built 05F states (pipeline incl. guard and volume): p90 0.007 / 0.011 / 0.018 cm (low / Narrow / Broad); max 1.24 cm at low where the pipeline's floor clamp acts | ✔ | ✔ |
| View captures: 8 PNGs (F / Q / P / RQ × grey / silhouette), head and neck hidden by a Mask modifier (no vertex deleted) | ✔ | ✔ |

`g_make_transport.py --verify` reports the same agreement repository-side: preview vs built p90 ≤ 0.018 cm, transport rotation 0°, s 0.976–1.007.

**Round-trip OBJ SHA-256:**
- 4.2.0: `cc501204…`
- 5.0.1: `fba33b1a…`

They differ only in the provenance header (Blender version and time). The `v` and `f` records are identical to the template.

## 5. Unverified items

Not run here:
- the Blender desktop UI;
- the `blender` command-line binary;
- real brush strokes.

The scripts were executed through the official `bpy` module of the same versions, and Edit / Sculpt mode enter and exit were exercised. The first genuine session should confirm the UI steps in `CHECKLIST_SCULPTOR.md`. Any deviation (transform, topology, identity, protected zones) is caught by the exporter, the preflight and `f_ingest`. Blender 3.x is unsupported.

No production `.blend` is shipped: the setup script generates the scene reproducibly in the sculptor's own version.

## 6. Source hashes (SHA-256)

| File | SHA-256 |
|---|---|
| `template/GO_ref_route_r6.obj` | `d0eb0d1643d135f3d5bd0920a9d6007f6dec8d1238530b30b298f3a1b2034eee` |
| `template/GO_true_floor_r6.obj` | `c6edbb98a8c4a93dd4c4cb0c615a29c5ba9133b4ce05aa7feef58d9190b288c2` |
| `template/GO_old_lean_r6.obj` | `e1c56b06cfa6a7298b77a63f4737fb3b27baa3d8928510f4b123a69e87e5aeee` |
| `template/GO_low_route_r6.obj` | `ed518d494d6412700db19946625bee97ed8ff35ff6eaed4cc85609c24ad8e618` |
| `data/regions.json` | `62833d43f79e7e1efeb9a64f4c8452a182db39b548392dfcc01da285be5b3ae2` |
| `data/joints_r6.json` | `f23a676c13b4b60da02e5a2f4ce6f543a9f4212def579494fc8f0faf524e0d1c` |
| `data/stations.json` | `3d20ac4867529724cab062174ee66c5b1dc4cbbf616aa0d3ab470391c3d28691` |
| `g_setup.py` | `b03261922fe1701b0fced21a067d34f746eb53e8f8fe1c9378710dbbbeb2b7e7` |
| `g_export.py` | `0dec4256095364269b1106170de25299d271b26d41a4458ccff575f23c0953e2` |
| `g_preview.py` | `5921117223ebe43ce7588e8c191a683057750beae0969032f64f45c537649925` |
| `g_views.py` | `f43526492218ec0c44594a8c1384f64a1b68b9431bb843d6617bb21f4e2371da` |
| `g_preflight.py` | `5add362c01d46cde35adbee35846b1b614b2d9420937304f13071ae035abd15f` |

## 7. Exact sculptor next action

1. Copy `reviews/rac-rmot05f-handoff/`.
2. In Blender 4.2 LTS or 5.0, run `blender/scripts/g_setup.py` and *Save As* `GO_sculpt_S1_work.blend` outside the package.
3. Sculpt `GO_SCULPT_BASE` (move existing vertices only) to brief §4, within §3.
4. Run `g_preview.py`, then `g_views.py`.
5. Run `g_export.py` with `SCULPT_ID = 'S1'` → `GO_sculpt_S1_r6.obj`.
6. Run `python3 g_preflight.py GO_sculpt_S1_r6.obj`.
7. Return the files in `CHECKLIST_DELIVERY.md`.

**On receipt:**
- `python3 tools/rac/w1/rmot05f_drivers/f_reentry.py GO_sculpt_S1_r6.obj S1`;
- then the replicated blind gate (`f_blind.py`, `f_scorer_prompt.md`, `f_tally.py`; G1–G7 in every run);
- only then the authorized combined Stage C.

## 8. Files changed

### Added

- `reviews/rac-rmot05f-handoff/blender/`: README, both checklists, manifest template, `scripts/` (5 scripts + `SHA256SUMS.txt`), `transport/` (6 OBJ, 3 npz, report), `tooling_evidence/`.
- `tools/rac/w1/rmot05g_blender/`: `g_setup.py`, `g_export.py`, `g_preview.py`, `g_views.py`, `g_preflight.py`, `g_make_transport.py`, `g_tests.py`.
- `reviews/claude-rac-rm-ot-05g-blender-sculpt-production-handoff-report.md` (this file).

### Changed (navigation pointers / status only)

- `reviews/rac-rmot05f-handoff/README.md`: pointer to `blender/`.
- `reviews/gorrund-rm-ot-05f-hand-sculpt-production-brief.md`: one pointer line. Its §1 exporter note is superseded for Blender 4.2 / 5.0 by the controlled exporter. Anatomy is untouched.
- `specs/STATUS.md`, `reviews/claude-pass2-r5-reference-mesh-queue.md`: status / tracking.
