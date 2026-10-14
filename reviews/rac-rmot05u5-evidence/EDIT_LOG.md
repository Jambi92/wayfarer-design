# RM-OT-05U5 EDIT_LOG (desktop Blender 5.2.2 LTS, Tyler's computer, real UI)

**Working file:** `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/sheets/gorrund_05U5_bounded_sculpt/scene/GO-05U5_sculpt_RETURN.blend`.
- Created by Save As from the clean handoff `GO-05U2_sculpt_handoff.blend` (sha `30a3dfb1…`), with no edits, after fixtures F1–F5.
- Sits beside `GO-05T_references.blend`.

**State for every pass:**
- Sculpt Mode, Front Orthographic (looking at −Y, the posterior), all faces revealed.
- Box-zoomed onto the cap.
- Mask: 0 on the 365 approved vertices and 1 elsewhere, from the handoff, never edited.

**Tools used:** the Smooth brush only. No Draw, Clay, Grab, Dyntopo, remesh, topology edit, global smoothing or script.

Each checkpoint was verified with the one approved command, `bash tools/rac/w1/rmot05u4_drivers/check_return_u2.sh <file>.blend <out>`:
- the frozen `crease_reference_v1.json` (`c1efefde…`);
- no `--ref_sha` or pin overrides;
- fixed limits.

| # | Settings | Strokes (screen, Front Ortho) | Checkpoint sha | Result |
|---|---|---|---|---|
| 0 | none | none (Save As from the handoff) | (bit-identical in geometry to the handoff) | Precheck: protection PASS, A 0.8951, B 0.3658, sliver (e) PASS, roughness (b) FAIL with 7 over the limit. Exit 3 |
| **1** | Smooth, radius 100 px, strength 0.350 | 2 vertical strokes along the crease line (x 552 and x 562, y 238→334) over the cap and about 1 cm of strip, 9 steps each | `81dba949…` | Protection PASS: 12 added source vertices moved, 0 outside, 0 ring, legacy 12/15 and 32/35 within limits. **A PASS 0.7007. B FAIL 0.2397 < 0.2743.** **Roughness (b) worse:** max 62.6° (baseline 47.9°), 7 over the limit, including in-cap 61581 62.6, 61303 47.2, 61219 47.1 and 61405 44.6. **Sliver (e) FAIL:** 13 cap faces lost angle, although the global minimum rose 6.24 → 11.19. Exit 3. Visually the notches softened, not removed |
| — | Ctrl+Z ×2 (undo, not a pass) | back to checkpoint 0 | — | Notches visibly restored |
| **2** | Smooth, radius 60 px, strength 0.350 | 2 vertical strokes along the crease on the cap interior (x 566 and x 578, y 240→324) | `00ceddd2…` | Protection PASS: 2 vertices moved (62061, 62086). A PASS 0.8951. **B PASS 0.2893.** **Roughness (b) unchanged at max 47.9**, still 7 over the limit (61581 and 61303 untouched). **Sliver (e) FAIL:** 4 faces. Exit 3. Visually no meaningful change |
| — | Ctrl+Z ×2, Ctrl+S | back to checkpoint 0, saved as the return | **`b45f42ae…`** | **The returned file:** 0 editable vertices moved; V1 hash matches; result.obj `edd7fbd0…`, verify, crease, guards and aggregate are byte-identical to the untouched-handoff precheck. Exit 3 on roughness (b) only |

**Pass 3 was not used, deliberately.**

The diagnostic `tools/rac/w1/rmot05u5_drivers/u5_feasibility.py` (output in `feasibility/`) ran on copies of the baseline only, never on a production file. It tested Laplacian smoothing of the 4 notch vertices or of all 15 cap vertices:
- **every** setting tested (λ 0.1–0.5, 1–4 iterations) made 5–12 cap faces lose min angle, so guard (e) fails;
- in-scope roughness clears only with whole-cap smoothing of λ ≥ 0.2 for 4 iterations, or λ ≥ 0.35 for 2, which moves vertices 0.2–0.6 cm;
- that same smoothing is the kind of edit that took crease B below its threshold in pass 1.

So no Smooth edit can satisfy (e), (b, in scope) and crease B together. Guard (b) is also NOT MET by construction, because of the out-of-scope vertices 70735, 70592 and 70408. Pass 3 could not produce a valid return and would only have spent the last of the budget on a guaranteed failure.

The budget was not reset: 2 of 3 passes were used, and the undo steps are disclosed above.
