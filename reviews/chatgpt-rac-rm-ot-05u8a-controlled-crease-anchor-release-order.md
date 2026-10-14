# RAC RM-OT-05U8A — controlled crease-anchor release to finish the residual lower wedge

**Authority:** Tyler-authorized autonomous continuation after review of U8 checkpoint 1.
**Date:** October 14, 2026.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent order:** `reviews/chatgpt-rac-rm-ot-05u8-final-lower-cut-facet-cleanup-order.md` (8e105da).
**Parent gate:** `reviews/claude-rac-rm-ot-05u8-final-lower-cut-facet-cleanup-gate.md` (8a47583).

## 1. Author ruling

U8 checkpoint 1 is accepted as the new safe baseline.

The remaining wedge is confirmed to be carried primarily by the two crease anchors:
- **61581** — crease A anchor, approximately 0.121 cm inside its neighbour centroid;
- **61580** — crease B anchor, approximately 0.117 cm inside its neighbour centroid.

The previous prohibition on moving these two anchors is lifted **only for this controlled U8A block**.

The frozen crease reference file and thresholds do **not** change:
- crease A must remain >= **0.6712880840904568 cm**;
- crease B must remain >= **0.27434876590971574 cm**.

Do not rebuild, refit, move or weaken the crease reference after editing.

## 2. Start state

Start only from the exact U8 safe checkpoint:

`GO-05U8_cp1.blend`
SHA-256 `2341d55445a448e24852f98fd9df3984ab12d706ef0b455cb4a2cdb0782860d6`.

Everything already repaired in U6/U7/U8 is frozen unless explicitly named below.

## 3. U8A editable set

Initial editable vertices:
- **61581**
- **61580**

No other new editable vertices are authorized initially.

The existing U8 cp1 edited vertices 61562 / 61727 / 61735 / 61940 are now frozen at their cp1 coordinates.

Create a new frozen one-ring around 61580 / 61581. Every vertex outside the two-anchor target must be bit-exact to U8 cp1.

No topology change.

## 4. Readiness before any desktop edit

Build an additive U8A verifier against U8 cp1 that proves:

- exact cp1 baseline identity;
- topology unchanged;
- every vertex outside {61580,61581} bit-exact to cp1;
- U8 cp1 edited vertices unchanged;
- U7/U6 edited vertices unchanged except 61581, which is now explicitly released;
- local affected faces remain manifold and intersection-free;
- local minimum triangle angle >= 10 deg;
- no new local edge outside 0.25-2.5 cm;
- V2, V3, V5 and V6c-3 remain PASS;
- U6 target roughness remains <= 36.3 deg;
- U6/U7/U8 local quality does not regress below 10 deg;
- crease A/B are measured with the unchanged frozen reference and original thresholds.

Focused negative tests:
1. moving a vertex other than 61580/61581 -> reject;
2. topology change -> reject;
3. sub-10-deg affected face -> fail;
4. a legal tiny 61581 move -> protection accepts and crease measurement updates;
5. a legal tiny 61580 move -> protection accepts and crease measurement updates;
6. a move that pushes crease A or B below threshold -> aggregate fails.

Do not modify historical U2/U4/U6/U7/U8 tools.

## 5. Desktop checkpoint sequence

Use real Blender desktop UI only.

### Checkpoint 1 — crease A anchor first

Because the U8 diagnostic places the residual wedge apex closer to 61581, address **61581 first**.

Use a small hand-judged lift along its local normal, with a maximum displacement of **0.06 cm** for this checkpoint.

Do not move 61580 in checkpoint 1.

Then:
- save a distinct cp1 scene;
- run full U8A verification;
- record crease A/B;
- inspect identical-camera lower-close, zoom, posterior and 3/4 views;
- report local dihedrals around 61581, face 130139 and edge 61562-61580.

If the wedge is no longer conspicuous and all safety gates pass, STOP and return checkpoint 1.

### Checkpoint 2 — crease B anchor only if still necessary

Use checkpoint 2 only if checkpoint 1 is safe and materially improves the wedge but a residual remains attributable to 61580.

Allow a **very small** 61580 lift, maximum **0.04 cm** along its local normal or an equivalently small hand-judged adjustment.

Crease B currently has limited margin. Do not chase the visual at the expense of the protected groove.

After the move, run full verification immediately.

If crease B falls below threshold, or if the wedge improvement is marginal while B loses substantial margin, revert to checkpoint 1 and return the safer result.

No third checkpoint is authorized.

## 6. Visual success test

The result is acceptable for author review only if:
- the residual dark lower wedge is no longer conspicuous in yaw 0, yaw 20 and pitch -45 views;
- the posterior axillary/crease groove remains anatomically readable;
- no flat spot, bulge, dent, lip, spike, ridge or melted patch appears;
- U6/U7/U8 improvements remain visually intact.

Numerical safety is mandatory but not sufficient.

## 7. Deliverables and stop

If successful, return:

**TECHNICALLY SAFE U8A RETURN / AUTHOR VISUAL REVIEW REQUIRED**

with:
- readiness / focused tests;
- exact anchor movements;
- checkpoint scenes;
- unchanged frozen crease reference plus measured A/B results;
- all protection and geometry checks;
- local dihedral diagnostic;
- identical-camera U8-cp1 versus U8A views;
- final .blend and linked reference;
- supported NPZ/OBJ/maps/labels;
- hashes;
- distinct package with manifest, CRC/hash validation and clean-extraction rerun.

Commit:
- `reviews/claude-rac-rm-ot-05u8a-controlled-crease-anchor-release-gate.md`
- evidence under `reviews/rac-rmot05u8a-evidence/`.

If the visual wedge cannot be removed while keeping both crease thresholds, STOP and state:

**U8A LIMIT REACHED / PRESERVE CREASE OVER FURTHER FACET REDUCTION**

Do not widen the region, create another automatic U-block, promote Gorrund, start Stage C, alter Grask E3, or begin D4/UE5/rigging/creator implementation.
