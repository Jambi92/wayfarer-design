# Cloud (OFF_PC) runners — per-body bake order a13cae71

Anthropic cloud container: Linux x86_64, 2 vCPU, 7 GB; 1 numerical thread per process, `nice`; every job capped at 2 h, so every stage is resumable.

- `gates_lane.sh L WAITBODY` — special gates (`sa6_bake_gates.py`, 50 poses × 25/50/75/100 %) on each final artifact listed in `gates_lists.txt` (`G name artdir`), then control sweeps (`C name`). Per-pose checkpoint `GATES_CKPT`.
- `gate_refit.sh NAME INIT_ARTIFACT` — gate-driven refit: fit (`BAKE_INIT` + `BAKE_EXTRA` with `gate:<pose>` entries, `gate_refit_extra_<NAME>.json`) → reopen + evaluate 34 poses × 4 fractions → full between-sample sweep (`SWEEP_SET=all`) → all 50 special gates. Each stage skipped if its output exists.
- `gate_dense.sh NAME POSES` — dense check of the refit gate poses: every 0.025 from 0.025 to 0.975 (36 fractions; 0.25/0.5/0.75/1.0 already gated).
- `gate_refit_queue_example.sh` — the M208-B@0.75 queue: resumed sweep in 2 pose shards (`SWEEP_SHARD`, merged by `sa6_bake_sweep_merge.py`), then refit stages, then dense check.
- `fn_finish.sh` — relaunches the F-N pass-3 sweep chunks until the final sweep exists.
