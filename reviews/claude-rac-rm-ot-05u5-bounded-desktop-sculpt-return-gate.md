# RAC RM-OT-05U5: bounded desktop sculpt return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05u5-approved-bounded-desktop-sculpt-order.md` (324dc71). Bounded revision approved by ChatGPT under Tyler's delegated authority.
**Evidence:** `reviews/rac-rmot05u5-evidence/`. **Tools:**
- `tools/rac/w1/rmot05u5_drivers/u5_build_handoff.py`;
- `u5_feasibility.py` (diagnostic only).

**Result: STOP CONDITIONS NOT MET. The bounded Smooth revision did not produce a valid return. The returned file is the best safe checkpoint (checkpoint 0, geometry identical to the 05U baseline).**

This is **not** a "TECHNICALLY VALID RETURN". Author visual review of the two failed attempts is offered for information only.

| Item | State |
|---|---|
| Gorrund | **UNACCEPTED** |
| Grask E3 | FROZEN |
| RM-OT-05 | **OPEN** |
| Stage C | BLOCKED |
| Reconstructed skin | INFERRED |
| Canon promotion | NOT PERFORMED |
| D4 / UE5 / production rigging / creator implementation | NOT STARTED |
| `base.glb` | unchanged |
| Rodin | not run |

## 1. Handoff and desktop fixtures (done before any production stroke)

**Handoff:** `GO-05U2_sculpt_handoff.blend` (sha `30a3dfb1…`), built from the pinned 05U RETURN (`9593d201…` / `0989caf4…`). See `handoff/HANDOFF_BUILD.md`.
- Mask 0 on the 365 approved vertices.
- Face set 4 on the 35 cap faces.
- Vertex groups `EDIT_upper_ext_05U2` (15) and `FROZEN_interface_boundary_05U2` (106).
- Untouched precheck: identical to the 05U baseline; exit 3 on roughness only.

**Real desktop fixtures** (Blender 5.2.2 on Tyler's computer; `fixtures/`, with screenshots):

| Fixture | Edit | Result |
|---|---|---|
| F1 | Draw stroke from protected skin into the cap | ACCEPTED_U2. Only 5 cap vertices moved; the mask held: 0 of 70,386 outside and 0 ring vertices moved |
| F2 | Protected vertex 62958 moved | REJECTED |
| F3 | New-ring vertex 62890 moved | REJECTED |
| F4 | Retained old-ring vertex 70234 moved | REJECTED |
| F5 | Unchanged re-save | ACCEPTED; bit-identical to the baseline |

## 2. Production passes (2 of 3 used; `EDIT_LOG.md`)

Smooth brush only, strength 0.350, strokes along the crease, cap plus about 1 cm of strip. Mask unchanged. No other tool and no script.

All results come from `tools/rac/w1/rmot05u4_drivers/check_return_u2.sh`:
- the frozen `crease_reference_v1.json` (`c1efefde…`);
- no overrides;
- fixed limits.

| | Checkpoint 0 (returned) | Pass 1 (r 100 px, on the crease line) | Pass 2 (r 60 px, cap interior) |
|---|---|---|---|
| Blend sha | `b45f42ae…` | `81dba949…` | `00ceddd2…` |
| Protection U2 | PASS (0 moved) | PASS: 12 moved, all cap; 0 outside; 0 ring | PASS: 2 moved; 0 outside; 0 ring |
| Legacy diagnostic (within 15 / 35) | 0 / 0 | 12 vertices / 32 faces, within | 2 vertices / 12 faces, within |
| V1-U2 | PASS | PASS | PASS |
| Crease A ≥ 0.6713 | 0.8951 PASS | 0.7007 PASS | 0.8951 PASS |
| Crease B ≥ 0.2743 | 0.3658 PASS | **0.2397 FAIL** | 0.2893 PASS |
| Roughness (b), official, 365 vertices | FAIL: max 47.9, 7 over | **FAIL: max 62.6, 7 over** | FAIL: max 47.9, 7 over |
| Roughness, in-scope diagnostic (cap / strip) | 4 over: 61581 47.9, 61303 47.9, 61580 40.9, 62065 36.6 | 4 over: 61581 62.6, 61303 47.2, 61219 47.1, 61405 44.6 | 4 over: 61581 47.9, 61303 47.9, 61562 39.9, 62065 36.6 |
| Sliver (e) | PASS | **FAIL: 13 faces lost angle** (global min rose 6.24 → 11.19) | **FAIL: 4 faces** |
| Aggregate | NOT MET, exit 3 | NOT MET, exit 3 | NOT MET, exit 3 |
| Visual | notches present | notches softened, not removed | essentially unchanged |

**Guard (b) out-of-scope vertices.** 70735 (anterior, θ117.7), 70592 (anterior, θ116.2) and 70408 (far posterior taper, θ−133.3) are in the guarded 365 but outside the brushed area. They stay over the limit in every state, so **official (b) is NOT MET by construction**. This was reported to Tyler before sculpting; he chose to sculpt and report both.

**Why pass 3 was not spent.** `u5_feasibility.py` smoothed **copies** of the baseline numerically: either the 4 notch vertices or all 15 cap vertices, λ 0.1–0.5, 1–4 iterations (`feasibility/feasibility_output.txt`).
- **Every** variant makes 5–12 cap faces lose min angle, so (e) fails.
- In-scope roughness clears only with whole-cap smoothing that moves vertices 0.2–0.6 cm, the same kind of edit that dropped crease B in pass 1.

Under the fixed guards, Smooth-only edits cannot meet (e), in-scope (b) and crease B together. A third pass could not yield a valid return. The budget was not reset; both undo steps are disclosed.

## 3. Returned file and verification

**Return:** `return/scene/GO-05U5_sculpt_RETURN.blend` (sha `b45f42ae…`) beside `GO-05T_references.blend`. It is checkpoint 0, restored by Ctrl+Z after pass 2 and saved:
- 0 editable vertices moved;
- **legacy V1 hash matches**;
- `result.obj` `edd7fbd0…`, verify, crease, guards and aggregate are **byte-identical** to the untouched-handoff precheck;
- `return.npz` and the reintegration JSON differ only in the recorded source path.

**Checks** (`return/checks/`):
- `return.npz`, `return.obj.gz`, `result.obj.gz`, maps and labels;
- verify, crease, guards, aggregate, `RETURN_HASHES.sha256`;
- identical-camera 05U-baseline vs return views: posterior shaded / wire, upper zoom shaded / wire, and arm context including yaw 45 and the underside.

The same views for each attempt are in `attempts/pass{1,2}/checks/`.

**Disclosed geometry gates (unchanged, not waived):**
- V2, V3, V5 and V6c-3 hold.
- **V4 fails** (8 taper edges).
- **V6c-1 fails** (θ −90 crease).
- **V6c-2 fails** (anterior taper, unresolved).
- V6 historical fails.
- The source sliver, face 130139 (6.24°), stays under guard (e) and is unchanged in the return.

## 4. Package

`gorrund_05U5_bounded_sculpt_return.zip`, sha `595dca5f8826b34e506f7e51121f4b3afee8e8a0b8525f9f961031ae3bc6b98d`, 61,903,434 bytes. Contents:
- the return scene and its reference;
- checks, attempts, fixtures and feasibility;
- `EDIT_LOG`, `HANDOFF_BUILD`, the crease reference and `README`;
- `MANIFEST.sha256` (83 files).

Clean extraction: manifest 83/83 OK. The corrected path was rerun on the extracted scene: exit 3 on `roughness_guard_b` only, with result, aggregate, guards, crease and verify byte-identical (`package/`).

Delivered to `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/sheets/gorrund_05U5_bounded_sculpt/`.

## 5. What would be needed (for the author; nothing done)

Any one of these is an author decision:
- **Boundary:** extend the guard (b) scope rule, or the editable boundary, to 70735, 70592 and 70408, or rule them out of (b).
- **Guard (e):** restate (e) as a global minimum (≥ baseline min, ≥ 5°) instead of per face. Every smoothing lowers some face angles even while the global minimum improves (pass 1: 6.24 → 11.19).
- **Method:** allow a method other than Smooth for the two notch vertices (61581 / 61303), such as a vertex-local relax that keeps the crease section points.

**→ STOP. Stop conditions NOT MET; best safe checkpoint returned. Awaiting author ruling.**
