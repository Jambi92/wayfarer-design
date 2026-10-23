# RAC RP1 — Gorrund final owner acceptance and freeze

**Date:** 2026-10-23
**Order:** `reviews/chatgpt-rac-rp1-gorrund-final-owner-freeze-order.md` (6aed2e6)
**Executor:** Claude

**Status: RAC RP1 GORRUND FAMILY PILOT — FINAL OWNER ACCEPTED / FROZEN**

## 1. Frozen canonical file

| Item | Value |
|---|---|
| File | `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Gorrund/RP1/GO_U_REF_RP1_FINAL.blend` |
| Sidecar | `GO_U_REF_RP1_FINAL.json` (same folder; repo copy in `reviews/rac-rp1-final-evidence/`) |
| How it was made | Byte-for-byte copy of the accepted rev110 file (`copy /b` on Tyler's PC). Not opened or re-saved. No geometry, rig or metadata change. |
| File SHA-256 | `133edfde40532244332ac17ea6ad887713d5e700392c36365ef6c31ca20609e8`: identical to the accepted rev110 hash. Confirmed by certutil on the PC and by sha256sum on the copy read back to the cloud. |
| Geometry hash | `e98cdc60a1c49da72c422c323bfff27b80c16c69f4629f8077d6f4a0b8c773f1`: SHA-256 of the float32 vertex array followed by the int32 polygon index array, both in file order. |
| Object | `GO_hand_production110`, the single mesh object. It keeps its accepted name; the canonical name is carried by the file name. World matrix is identity. |
| Counts | 1 443 272 vertices; 1 443 270 faces, 100 % quads |
| Parent | `work/claude110/Gorrund_hand_production110.blend` (same hash), report `reviews/claude-rac-gorrund-hand-mesh-grip-closure.md` @ `0034778` |
| Owner acceptance | Tyler, via the order above (2026-10-23) |

## 2. Derivation chain

| Step | File | SHA-256 |
|---|---|---|
| v014 | `GO_U_REF_RP1E_retopo_v014.blend` | `18df4197…850b` |
| v015 | `GO_U_REF_RP1F_refine_v015.blend` | `dfba363e…5e75` |
| rev107 refit | v015 topology refitted to the accepted rev107 hands (`outputs/Gorrund_Rounded_Fingertips_Review.blend`) → rev109 | `cdc9e3a9…9179` (reference) |
| rev110 | thumb-tip graft → `Gorrund_hand_production110.blend` | `133edfde…09e8` |
| FINAL | byte copy of rev110 | `133edfde…09e8` |

## 3. Verification before freeze (re-run independently on the geometry read out of the frozen file)

| Check | Result |
|---|---|
| Components | 1 |
| Boundary edges / non-manifold edges | 0 / 0 |
| Directed-edge duplicates (orientation consistency) | 0 |
| Euler characteristic / genus | 2 / 0 |
| Degenerate faces / coincident vertices / unused vertices | 0 / 0 / 0 |
| Quads | 100 % |
| Stature | 204.519820 cm. Identical to rev110; native 204.51982 cm. |
| Bbox | 84.40883 × 134.1764 × 204.51982 cm. Difference vs rev110 is at most 0.00001 mm. |
| Match to accepted rev110 | Vertex order identical. Faces identical; the winding differs only because of the analysis frame's y-flip. Max vertex difference 0.00012 mm (float32 storage). |
| T-2 hands vs rev107, outside the two accepted exclusions | L: prod → ref max 0.44 mm, ref → prod max 0.61 mm. R: prod → ref max 1.21 mm, ref → prod max 1.11 mm. Identical to the accepted closure. |
| T-4 (quality target) | 88.0 % / 95.4 %. Accepted; kept as a watch item. |
| Protected files re-hashed | v015 `dfba363e…5e75` unchanged; rev107 `cdc9e3a9…9179` unchanged; v014 `18df4197…850b`. |
| Self-intersections | **0** in the accepted design geometry (float64). The check on the vertices as stored in the `.blend` (float32) flags **6 face pairs** at three spots: R hand at (−28.3, −41.0, 92.7) cm, and both feet at z ≈ 2.5–2.9 cm. In the design geometry these faces are separated by 0.000013–0.00024 mm, and storing the file rounds vertices by up to 0.00012 mm. They are rounding tangencies, not modelled overlaps. The already-frozen v015 file shows 33 pairs of the same kind under the same float32 check. The geometry itself is unchanged and matches the accepted rev110 exactly, so this is recorded here, not waived and not edited. A future production gate should state whether self-intersection is measured on the design data or on the stored float32 file. |

## 4. Accepted owner-review items (per the order)

1. The method substitution: rev107 hand refit into v015, the R middle/ring bridge cut and cap, genus 0.
2. The thumb-tip graft and its T-2 exclusion.
3. The R thumb-base crater exclusion. The crater is not recreated.
4. T-4 at 88.0 / 95.4 %. It is a quality target, not a failure gate; it is kept as a claw-tip LOD/topology watch item.
5. The contact tolerances (1.0 / 0.5 / 0.5 mm) and correctives up to about 10 mm, accepted **for the diagnostic test only**.
6. The left-hand grip forms (thumb alongside the index; thumb locked on the index). These are valid diagnostic grips, **not mandatory runtime poses**.

## 5. Non-canonical evidence and carry-forward

- The rev110 diagnostic rig is **non-canonical deformation evidence only**. This covers its human-ratio joint estimates, weights, actions and corrective shape keys (`Gorrund_hand_grip_tests110_L_DIAG.blend`, `…_R_DIAG.blend`). It is not promoted.
- Carry-forward to future rigging:
  - claws need rigid distal ownership;
  - palm and crease soft-tissue contacts need proper corrective shapes or helper behaviour;
  - joint placement must come from accepted Gorrund anatomy and landmarks, not from the diagnostic human ratios.
- No UE5, rigging or creator authorization follows from this freeze.

## 6. Closure

RP1 is **CLOSED**. No further Gorrund work. RP2 proceeds only under the separate Grask order (`reviews/chatgpt-rac-rp2-grask-production-pilot-execute-order.md`).

Evidence: `reviews/rac-rp1-final-evidence/`. It holds:
- the sidecar;
- the extraction and hash (`freezeextract.py`, `extract.json`);
- the topology gate (`topo.json`);
- self-intersection pairs (`sx.json`);
- T-2 (`dev2.json`, `gate_dev2m.py`, using the accepted rev110 exclusion mask);
- the PC certutil output.
