# RAC RM-OT-05D — true skeletal-envelope separation + race anatomy evidence

Non-canon diagnostics for `reviews/claude-rac-rm-ot-05d-true-skeletal-envelope-race-anatomy-gate.md`. Every candidate is **PENDING AUTHOR / NOT ACCEPTED**.

## Route

The skeleton route is unchanged from RM-OT-05C: the accepted 05B skeleton route, which is the 05A architecture plus the 05B knee / residual corrections and Narrow holds. The 05B surface stage is not used. On top of it, the steps are:

1. The race base-surface organization (`tools/rac/w1/race_base.py`).
2. **Guarding against the true skeletal floor** (`tools/rac/w1/true_envelope.py`; spec `"floor": "true"`) instead of the MPFB minimum-body `-LEAN` surface.
3. Restoring the composition amount: the volume moved out of donor relief is returned as an even layer (`"keep_volume": true`).

The spec rides in the skeleton meta, so every grid and composition body gets the same organization. The `-LEAN` is never rewritten.

## Contents

| Path | What |
|---|---|
| `candidates.json` | the five specs: Grask E1 / E2 / E3 and Gorrund E1 / E2 |
| `stageA/stageA_{GR,GO}_{shoulder,pelvis}.png` | Stage A section strips: old `-LEAN` guard, new true floor, 05C baseline and 05D surface, in matched frames |
| `stageA/stageA_{GR,GO}_allowed.json` | allowed-movement table: per region, floor depth below the old guard, and how far 05D actually moved inside it |
| `stageA/floorview_*.jpg` | rendered `-LEAN` vs true floor vs body |
| `sheets/d_{GR,GO}_{F,Q,P,RQ}_grey.jpg` | reference candidates beside Skarn at matched height, the Marchfolk reference control and the 05C developmental baseline |
| `sheets/d_*_{F,P}_sil.jpg` | silhouettes |
| `sheets/d_*_low_*` | low composition (muscle 0 / weight 0.5) |
| `sheets/d_*_frames_*` | Narrow / reference / Broad |
| `sheets/c_218_*` (Grask), `sheets/c_229_*` (Gorrund) | close strips: shoulder, thorax, pelvis (incl. rear 3/4 = sacrum), knee, shank, elbow, wrist, hand, foot, ankle |
| `blind/` | the three blind runs (see below) |
| `guards/guard_all.json` | §9 minimal technical guards for all 20 bodies, including the skeleton-anchored station readings |
| `construction/` | build records, skin measurements and CIB files |
| `search/` | spec history (`d1`–`e3`, `t*` isolation tests, `mk*` generators), preview sheets and uninformed probes |

### Blind runs

| Run | Files | Bodies |
|---|---|---|
| 1 | `blind_D_*`, `key_D05.json`, `blind_results_run1.json` | 16: Grask E1 / E2, Gorrund E1 / E2, 8 controls |
| 2 | `blind_F_*`, `key_D05b.json`, `blind_results_run2.json` | 18: Grask E3 added |
| 3 | `blind_H_*`, `key_D05c.json`, `blind_results_run3.json` | 18: replication of run 2 with a new seed |

`blind_summary.json` holds the C counts per candidate per run.

## Drivers

All in `tools/rac/w1/rmot05d_drivers/`:

| Driver | Purpose |
|---|---|
| `d_build.py` | builds |
| `d_guard.py` | guards |
| `d_stageA.py` | Stage A |
| `d_package.py` | sheets |
| `d_blind.py` | blind runs (`run2`, `run3` options) |
| `d_floorview.py` | floor view |
| `d_evidence.py` | builds this directory |

Measurement: `tools/rac/w1/skeletal_stations.py`.
