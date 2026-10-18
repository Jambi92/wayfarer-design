# RAC Stage C C4.1 evidence

Report: `reviews/claude-rac-stage-c-c4-1-grask-resolution.md`. Everything here is read-only: no mesh was edited or saved. Normalized copies were made in memory only.

## checks/

- `gr_g1_canonical.json`: GR-G1 in three readings, for E3 ref / N / B, with the MF-M-R comparator and PASS / MARGINAL / FAIL by t.
  - W1/W2 route (canonical).
  - 05D skeleton-station level (disclosed).
  - Organized (Stage C control).
- `g1_GR5DE3*.json`: raw readings from `tools/rac/w1/stagec_drivers/c41_gr_g1.py`.
- `grask_vs_durrim_architecture.json`: 21 existing directional readings, Grask E3 vs Durrim, with roster ranks.
- `sil_c41.json`: REPORT-only silhouette IoU, covering Grask vs Durrim (normalized to 218) and the front-only set.

## sheets/

- `grask_vs_durrim_native.jpg`: native world scale, with Skarn and Marchfolk for reference.
- `grask_vs_durrim_norm218.jpg`: DIAGNOSTIC; Durrim uniformly ×1.591. Not a body.

## blind/

- `front_only.jpg`: the sheet the reader saw.
- `front_only_read.md`: key, prompt and verbatim answer.
