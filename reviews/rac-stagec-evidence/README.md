# RAC Stage C evidence

Gate: `reviews/claude-rac-stage-c-gate.md`. Protocol: `specs/RAC_STAGE_C_PROTOCOL.md`.

## checks/

- `source_manifest.json`: hashes of every source.
  - Gorrund blend and glb.
  - Grask E3 builds, with geometry and file hashes compared against the frozen 05D r6 assets.
  - Roster comparators, compared against `reference-assets/manifest.json`.
  - Saurin.
- `w2c_reproduction_val.json`: the adapter run on the rebuilt W2 bodies. It equals the committed W2C record (373/373).
- `w2c_E3.json`: the W2C suite with E3 in the Grask slots. Registry: `w2c_E3_registry.json` (absolute scratch paths). The repo-relative copy is `tools/rac/w1/stagec_drivers/stc_registry_E3.json`.
- `nonpass_raw.json` and `w2c_E3_nonpass_classified.json`: the 43 non-passes with their W2C status and Stage C class.
- `w2c_E3_G_rows_classified.json`: canonical-row failures per body, with their class.
- `frame_record_GRN5.json` / `frame_record_GRB2.json`: the reconstructed W2C frame records, verified bit-exact against frozen N/B.
- `distinct.json`: REPORT-only silhouette IoU. `chest_depth_profile_diag.json`: profile depth share in the 62–76 % stature band (diagnostic).

## sheets/

Lineup, matched-height comparisons (208/218/229), silhouettes, Grask E3 states, and the Gorrund reference.

Gorrund appears at native height, or as an in-memory uniform comparison copy (D2(c)). These copies are never saved.

## blind/

Letter-coded sets 1–3, plus `blind_read.md` (key, prompt, verbatim answer).

## Reproduce

Requires the W1 scratch root `$S`, MPFB 2.0.17 and the bpy 5.2.2 module.

1. `python3 stc_build.py <05B cfg_final.json> <05D candidates.json> 198 208 229 239`
2. `run_candidate.py` → `_meas.json`.
3. `jbw.py`.
4. `W2C_SPEC=stc_registry_E3.json W2C_FRAMES=GRN5,GRB2 python3 stc_w2c_eval.py`
5. `stc_render.py` → `stc_sheet.py` / `stc_silhouette.py`.
