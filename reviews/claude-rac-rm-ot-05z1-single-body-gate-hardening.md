# RAC RM-OT-05Z1 — single-body intake gate hardened for scene-graph instancing

- **Order:** `reviews/chatgpt-rac-rm-ot-05z1-scene-graph-single-body-gate-hardening-order.md`
- **Date:** 2026-10-15
- **Tool:** `tools/rac/w1/rmot05z_drivers/z_single_body_gate.py`, revised
- **Self-test:** `tools/rac/w1/rmot05z_drivers/z_gate_fixtures.py`, new
- **Evidence:** `reviews/rac-rmot05z-input/gate_selftest/`

## Outcome

**Gate hardened. All 11 self-tests match their expectations.**

**Still STOPPED AT IMAGE GATE / AWAITING SINGLE-FIGURE INPUT IMAGE.**

Nothing else happened in this order:
- no image was generated;
- nothing was submitted to Rodin and no credits were spent;
- no canon change;
- no 05Y figure was extracted;
- no anatomy, ARM, LOW, blind, scaffold, Stage C, D4, UE5, rigging or creator work.

**No GLB was modified.**

## 1. What changed in the gate (order items 1–9)

| # | Requirement | Implementation |
|---|---|---|
| 1 | Active scene, recursive traversal | Uses `scene` (default 0). Walks `scenes[scene].nodes` and all `children` recursively. Node cycles return REVIEW. |
| 2 | Transform composition | Each node's local matrix comes from `matrix` (glTF column-major, transposed on read) or from TRS (normalized quaternion xyzw, then scale, then translation). World matrix = parent × local. |
| 3 | One instance per scene node | Every node with `mesh` adds one mesh instance. Each primitive of that mesh is instantiated once per instance. |
| 4 | World coordinates | POSITION is transformed by the instance's world matrix **before** welding, component analysis and body sizing. |
| 5 | Several primitives per body | All instanced primitives are welded together by exact world position. A body split across primitives or meshes is therefore one component. |
| 6 | Unused meshes ignored | Only meshes referenced by active-scene nodes are counted. `unused_mesh_definitions` is reported. Nodes outside the active scene are ignored. |
| 7 | Counts reported | `scene_nodes_traversed`, `mesh_definitions`, `mesh_instances`, `primitive_instances`, `components`, `body_sized_components`, `world_bounds`. |
| 8 | Multi-body FAIL | FAIL when there is more than one body-sized component (height at least 50 % of the tallest). **Also FAIL** when two instances of the same mesh have identical world bounds. Those instances would weld into one component and hide the duplicate. |
| 9 | Small pieces listed | Each piece under 50 % of the tallest height is listed with its faces, height and bounds. Nothing is dropped silently. |

**Fail-safe REVIEW (exit 4; never PASS)** covers:
- a non-GLB container, wrong version or length mismatch, or missing JSON;
- external or data-URI buffers, or a missing BIN chunk;
- sparse accessors;
- POSITION that is not float32 VEC3, or is normalized;
- non-TRIANGLES primitive modes;
- non-integer or out-of-range indices, or an index count not divisible by 3;
- reads past the end of a buffer view;
- a missing active scene, or a scene with no mesh;
- missing nodes or meshes, node cycles;
- an invalid quaternion, or non-finite matrices or positions.

Interleaved (strided) buffer views are read correctly.

Flags reported for the later anatomy review do not change the verdict: nested components, open boundaries and non-manifold edges.

## 2. Tests

The fixtures are built from code by `z_gate_fixtures.py`. They are byte-identical on every run: a rebuild was compared with `cmp`.

- The **body** is a closed 0.4 × 1.8 × 0.3 box.
- The **accessory** is a closed 0.05 cube.
- The fixtures are committed (`gate_selftest/fixtures/`, 17.9 kB).
- The expectations, worked out analytically and then checked against the run, are in `gate_selftest/expected_fixtures.json`.
- The run log is `gate_selftest/selftest_run.txt`.

| Test | Expected | Result |
|---|---|---|
| f1 one mesh, one node | PASS, 1 body | ok |
| f2 one mesh instanced by three translated nodes | FAIL, 3 body-sized | ok |
| f3 body plus a small accessory (two primitives) | PASS, accessory listed as 1 small piece | ok |
| f4 parent (T 10,0,0; S 2) → child (T 1,0,0; R 90° about Y) | PASS; world bounds x 11.7–12.3, y 0–3.6, z −0.4–0.4 (analytic) | ok |
| f5 unused mesh definition | PASS; `unused_mesh_definitions` = [1] | ok |
| f6 two nodes using `matrix` (one translated by 3 in x) | FAIL, 2 body-sized | ok |
| f7 two coincident instances of one mesh | FAIL (coincident duplicate [0, 1]) | ok |
| f8 TRIANGLE_STRIP primitive | REVIEW (fail-safe) | ok |
| f9 extra bodies only in an inactive scene | PASS (active scene has one body) | ok |
| real 05X `Gorrund.glb` (`1c23b92b…`) | PASS: 1 scene node, 1 instance, 1 component | ok |
| real 05Y `base_1.glb` (`b0214fcf…`) | FAIL: 1 instance, 3 body-sized components | ok |

**To rerun:**

```
python3 tools/rac/w1/rmot05z_drivers/z_gate_fixtures.py OUTDIR reviews/rac-rmot05z-input/gate_selftest/expected_fixtures.json [--real Gorrund.glb base_1.glb]
```

Exit 0 means every test matched. The two real masters are not stored in the repo; they live on E: under `RaceBodies/source/`, as recorded in 05X / 05Y.

## 3. State

**STOP AT IMAGE GATE / AWAITING SINGLE-FIGURE INPUT IMAGE.**

The prompt is `reviews/rac-rmot05z-input/IMAGE_INPUT_05Z.md`. The gate form is `IMAGE_GATE_05Z.md`.

Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**; canon advancement **NOT PERFORMED**; D4 / UE5 / production rigging / creator **NOT STARTED**.
