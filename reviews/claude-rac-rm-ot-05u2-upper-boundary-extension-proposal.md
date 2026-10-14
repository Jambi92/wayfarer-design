# RAC RM-OT-05U2: minimal upper-boundary extension, PROPOSAL AWAITING AUTHOR APPROVAL

**Order:** `reviews/chatgpt-rac-rm-ot-05u2-upper-boundary-extension-proposal-order.md` (89d28f0).
**Supporting files:** `reviews/rac-rmot05u2-proposal/`. **Read-only tools:** `tools/rac/w1/rmot05u2_drivers/` (`u2_analyze.py`, `u2_views.py`).

**Nothing was changed.** This is a proposal only:
- no mesh, mask, face set, protection set, scene or release was altered;
- no sculpt was done and no candidate was produced;
- the 05U RETURN and its release (`aed5711f…3159`) are unchanged;
- the views are annotations of the unchanged 05U RETURN, not before/after views of a repair.

## State

| Item | State |
|---|---|
| Gorrund | **UNACCEPTED** (05U author visual review is still open) |
| Grask E3 | FROZEN |
| RM-OT-05 | OPEN |
| Stage C | BLOCKED |
| Reconstructed skin | INFERRED |
| Canon promotion | NOT PERFORMED |
| D4 / UE5 / production rigging / creator implementation | NOT STARTED |

## 1. Reference, indexing and confirmation

| Item | Value |
|---|---|
| Reference mesh | `GO-05S-S3.obj`, sha `1d50383376dc5dd2e249778c7b7d8330f4ec16daa21303656a146c0b4d81ac4c` (70,751 vertices, 141,194 faces) |
| Return measured | 05U `checks/return/return.npz`, sha `0989caf45cba8ddf0f44bdfba962671430c613bb752ac543d99d9b4b16420265` |
| Release | `gorrund_05U_direct_sculpt_return.zip`, sha `aed5711fa00d193eccae9391f40de790d6e617333caa8add76554e81358a3159` |

**How it was measured.** The RETURN was placed in S3 order through its identity attribute. Its topology was checked to be identical to S3. Protected positions equal S3, as already verified bit-exact.

**Indexing.** Every vertex and face index here is a **zero-based S3 index**. The scene attribute `rac_s3_vid1` is that index **+ 1** (one-based). F1 source indices (also zero-based) are given in `proposal_region.json`.

**Roughness** means the largest angle between a vertex's incident face normals and their mean normal. All six reported notch vertices are **confirmed**:

| S3 vertex | Category now | Source? | θ (deg) | s (cm) | Roughness (deg) |
|---|---|---|---|---|---|
| 61303 | frozen ring | yes (F1 61401) | −89.6 | 7.92 | 47.9 |
| 61559 | frozen ring | yes (F1 61666) | −87.2 | 8.08 | 35.1 |
| 62065 | frozen ring | yes (F1 62194) | −84.1 | 7.69 | 36.6 |
| 61581 | protected | yes (F1 61688) | −85.8 | 9.04 | 47.9 |
| 61580 | protected | yes (F1 61687) | −84.0 | 10.46 | 40.9 |
| 61562 | protected | yes (F1 61669) | −85.2 | 9.60 | 35.2 |

**What these notches are.** All six, and every face around the proposed extension, are **original F1 source surface** (face label 0). The notches were not caused by 05U; they are already present, unchanged, in F1, S3 and the 05U RETURN.

**How unusual they are.** On the source skin of the arm (1,438 sampled source vertices, r < 16 cm), roughness is p50 7.6°, p90 24.4°, p95 36.3° and p99 52.8°. The notch vertices (35–48°) are in roughly the top 5 %, and they are clustered along the posterior crease right above the interface.

**The cluster is local.** Above the proposed region, roughness returns to baseline:

| Band | Median roughness | Vertices ≥ 28° |
|---|---|---|
| s 10.5–13 cm | 6.9° | 1 (S3 61586, 31°) |
| s 13–16 cm | 7.8° | 1 (S3 61849, 28°) |
| s 16–20 cm | 6.9° | none |

Both of those single vertices are within the source p95 and stay protected.

## 2. The proposed region (smallest coherent extension)

**Rule** (explicit; in `u2_analyze.py`; no tuning loop):
1. **Seeds:** the six reported vertices.
2. **Growth:** add every edge-adjacent vertex that is inside θ −95…−75°, s 5–12 cm, r < 16 cm, is not already editable, and has roughness ≥ 28°, repeated to closure.
3. **Added faces:** every non-interface face touching a seed.
4. **Enclosed vertices:** any vertex whose every incident face is then inside the region becomes editable too, and is listed.

| | Current (05U) | Proposed | Change |
|---|---|---|---|
| Editable vertices | 350 (sha `ff059bb0…f8243`) | **365** (sha `0154b2be…5559`) | **+15** |
| Frozen ring vertices | 101 (sha `ff07157b…b3f0`) | **106** (sha `91725db2…0426`) | 97 kept, 4 released to editable, 9 new |
| Editable faces | 797 interface faces (sha `38b7ad3e…ff7a`) | 832 | **+35 added source faces** (sha `483ab7fe…7692`) |

**The 15 added vertices** (S3, zero-based), all original source vertices:
- **11 seeds:** 61219, 61303, 61405, 61559, 61562, 61580, 61581, 61652, 62061, 62065, 62086.
- **4 enclosed:** 61130, 61368, 61727, 61750.
- **By current category:**
  - 4 are **current frozen-ring** vertices: 61130, 61303, 61559, 62065.
  - 11 are **protected source** vertices.

  None is a B2-retained or 05Q-inferred vertex.

**The 35 added faces:**
- all **label 0, original F1 source surface**, currently inside the protected set P05S;
- 11.05 cm² in total;
- θ −90.8…−80.9°, s 7.69–10.46 cm, r 10.3–12.3 cm;
- one connected patch, attached to the top of the posterior interface. The posterior region stays one component.

**New frozen ring.**
- 9 new frozen vertices: 60886, 61355, 61522, 61771, 62027, 62052, 62382, 62713, 62890.
- Together with 97 retained current ring vertices, they make a 106-vertex ring.
- The roughest new ring vertex is 21.1° (61771), below the source p90, so the new seam starts from ordinary source surface rather than at a notch.

**Seam outliers.** Both 05U seam-outlier edges become interior to the extended region, so neither remains a seam:
- θ −88.4° / s 8.0, dihedral 63.7°: edge 61303–61559;
- θ −85.7° / s 7.89, dihedral 59.1°: edge 61559–62065.

**What stays frozen:**
- everything outside the 35 faces, including the crease line above s 10.5 cm;
- the deltoid, latissimus/trunk side, shoulder and axilla architecture;
- the whole anterior side;
- the untouched posterior taper (θ −116…−136°);
- all other garment regions.

**This changes the source surface, stated explicitly.** Approving this proposal means modifying **35 original F1 source faces and 15 source vertices** that are protected today. It is not an interface-only operation. Their reconstructed result would be labelled **INFERRED** under a new, explicitly named label (proposed label 6, "edited source surface, 05U2"). They would not be merged into the interface labels 4/5.

**Machine-readable files:**
- `proposal_region.json`: rule, confirmation, categories, lists, hashes, roughness baseline, seam outliers;
- `proposal_sets.npz`: current and proposed editable, ring and face index arrays;
- `P05U2_preview.json` and `P05U2_preview.npz`: the would-be protection set.

## 3. Annotated views (unchanged 05U RETURN; `views/`)

Each image has three rows:
1. **CURRENT:** purple = editable interface; amber = protected faces on the current frozen ring.
2. **PROPOSED (not performed):** red = the 35 added source faces; cyan = protected faces on the proposed new frozen ring; grey = stays protected.
3. **RESIDUAL DEFECTS:** pink = faces at the six notch vertices; orange = faces on the two seam-outlier edges.

| File | Camera |
|---|---|
| `P1_posterior_close_shaded.png` | The 05U posterior camera (centre 27.5, −10.5, 162; 18 cm; yaw 0 / 20 / 330, pitch −45) |
| `P2_posterior_close_wire.png` | Same, with wireframe |
| `P3_upper_notch_zoom_wire.png` | Zoom on the extension (centre 28.9, −13.3, 167.5; 11 cm), wireframe |
| `P4_arm_context_incl_yaw45.png` | The 05U arm cameras (rear, lateral, front, 3/4, **front 3/4 yaw 45**, underside), to judge scope |

The red patch is a small cap on the top of the posterior strip, along the crease. In the arm-context views it is a minor fraction of the visible arm.

## 4. Proposed method (not performed)

**Setup:**
- A new working copy `GO-05U2_sculpt_handoff.blend` made from the **05U RETURN**, which is preserved unchanged as the frozen baseline.
- The mask is opened on exactly the 365 proposed editable vertices.
- New face set 4 marks the 35 added faces; groups `EDIT_upper_ext_05U2` and `FROZEN_interface_boundary_05U2` are added.
- The identity attributes are kept.

**Brushes:**
- The **Smooth brush only**, at low strength (0.3–0.4) and a small radius, covering the cap and about 1 cm of the existing strip below it.
- Strokes run **along** the crease direction, not across it, so the fold line keeps its depth while the saw-tooth facets relax.
- No Draw, Clay, Grab, Dyntopo, remesh or topology change.

**Stop condition.** Stop as soon as all of these hold:
1. the notch facets no longer read at yaw 0, 20 and pitch −45;
2. no vertex in the extended region exceeds the source p95 roughness (36.3°);
3. crease depth across the cap stays at least 75 % of its pre-edit value. Depth is measured on the two sections through 61581 (s ≈ 9.0) and 61580 (s ≈ 10.5), as the deepest point's distance from the chord between the section's ring vertices.

At most three passes. If (3) would be violated, or the result reads flatter or more softened, stop, undo to the last good state and report it. Do not widen the region.

## 5. Changes that approval would require, and the verification contract

**Changed protection rules, explicit and versioned.** Each item is added alongside what exists; nothing existing is replaced.

| Item | Proposal |
|---|---|
| Protection set | **P05U2**: P05S minus the 35 faces = **139,772 faces** in P05S order. F1 face-index sha `02b608bc…9184`; precommitted coordinate sha on S3 / 05U `25ffe5ac83d60e81b1026baf91bf3dbc07d7dc7136a8495f77f5581920328ffd`. The removed F1 faces are listed in `P05U2_preview.json` |
| Reintegration | An **opt-in, versioned** edit-set argument for `t_reintegrate.py` that loads the approved lists (EDIT 365, RING 106, editable faces 832) and checks them against the hashes above. Default behaviour, and 05U results, unchanged |
| P1 / P2 | P1 = every vertex outside the 365 unchanged, bit-exact, **including the 106-vertex new ring**. P2 = every face outside the 832 present and unchanged |
| V1 | A new gate, **V1-U2**, runs with `--prot_faces P05U2 --nprot 139772 --prot_sha 25ffe5ac…` and checks source-vertex bit-identity on every source vertex outside the 15 approved ones. The original V1 (P05S) is **still reported**, as information: it must fail on exactly the 35 approved faces and 15 vertices and nowhere else, and that is shown |
| Labels | Added faces become label 6 ("edited source surface, 05U2", INFERRED). Existing labels are unchanged |

**Unchanged geometry-quality criteria.** V2–V6c keep the same code, thresholds and verdict rules. No validator is weakened and no threshold is moved.

**Tests required after approval, before any production stroke:**
1. **Real desktop fixture, on a disposable copy of the new handoff:**
   - mask display and a brush stroke crossing the new boundary: only the 365 move;
   - an edit **just outside** the new boundary, on protected source vertex 61586 or new-ring vertex 61771: must be **REJECTED**;
   - a moved **new frozen-ring** vertex (for example 61522): must be REJECTED;
   - a moved **old-ring vertex that stays frozen**: must be REJECTED;
   - an unchanged fixture: must reintegrate **bit-identical** to the 05U RETURN.
2. **Production:**
   - exact preservation of everything outside the 832 faces / 365 vertices;
   - supported reintegration ACCEPTED;
   - V1-U2 pass, plus the original V1 reported with its expected, localised failure;
   - V2–V6c all reported;
   - identical-camera before/after views (05U RETURN against the 05U2 result), using the 05U posterior, arm and zoom cameras above;
   - a new package with its own manifest and clean-extraction hash check.

## 6. Context, not in scope and not waived

| Item | Status |
|---|---|
| **V6c-1** θ −90° crease | 74.4° (limit 35°), unresolved. It is measured along the interface section, which ends at about s 7.8 cm, just where the cap begins; this proposal does not target it |
| **V4** | Eight bad edges in the untouched posterior taper (θ −122…−132°), unchanged |
| **V6c-2** | Anterior taper non-monotone, unchanged |

These are not repaired by this proposal, and they are not accepted or waived by it.

## 7. Decision requested

Tyler, please **approve**, **revise** or **decline**:
- the 35-face / 15-vertex boundary defined above, with the hashes in `proposal_region.json`;
- the method in §4;
- the verification contract in §5.

Approval would authorize only this stated revision. It would not accept Gorrund or open Stage C.

**→ STOP. PROPOSAL AWAITING AUTHOR APPROVAL. No geometry or protection-set change until approved.**
