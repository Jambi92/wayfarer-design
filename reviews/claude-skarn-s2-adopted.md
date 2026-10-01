# Skarn S2 Adopted — Iteration 3 Reference Update

**Author:** Claude
**Responds to:** `reviews/claude-adopt-skarn-s2-action.md` and `reviews/iteration-3-normalized-masculine-decision.md`
**Status:** DONE. The feminine normalized review is still open before Iteration 3 closes.

## What changed

- **Skarn_S2 is now the neutral Skarn reference** in every Iteration 3 sheet, for both sexes, and in the build script and model files.
  - It changes only the skeletal frame: girdles, ribcage, joints, and the hand/foot skeleton.
  - Muscle and fat stay at the shared neutral setting, so no muscularity was added.
  - S2 marks the population center. It is not a minimum and does not narrow valid Skarn variation.
- **The original Skarn is kept as `Skarn_v1`** for historical comparison. It is in `skarn_*_normalized.jpg` next to Marchfolk and the current Skarn, and in `RaceBodies/out/Skarn_v1_*.blend/.fbx` on Tyler's PC.
- **Regenerated sheets** in `reviews/images/race-references-iteration-3/`:
  - `setA_*` (true scale and normalized)
  - `stress_*`
  - `skarn_*`

  The `setB_*` sheets have no Skarn column and are unchanged.

## Carried work (unchanged)

1. **Gorrund:** direct sculpt of the shoulder girdle → thorax → lower axial trunk → pelvis → proximal lower limbs load path. This is a tooling limit, not a spec change.
2. **Saurin:** dedicated sculpt of the head, extremities, scale architecture and tail-base integration. The body and the complete tail stay as they are.
3. **Feminine review:** `stress_Fem_normalized.jpg` is ready for the Author/Tyler review that closes Iteration 3.

No canonical spec was edited. No Pass 2 or UE5 work was done.
