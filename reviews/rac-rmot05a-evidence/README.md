# RAC RM-OT-05A — Grask / Gorrund architecture-rebuild evidence

NON-CANON diagnostics for `reviews/claude-rac-rm-ot-05a-grask-gorrund-architecture-rebuild-gate.md`. Candidates are PENDING AUTHOR.

- `arch_final.json` — the final race-architecture sculpt recipe (GR, GO) applied by `tools/rac/w1/arch_sculpt.py` on the accepted W2C / W2D routes (`rmot05a_drivers/a_build.py`, `a_transport.py`). `narrow_knee_hold` = GO-G6 knee hold on the 230.9 Narrow frame.
- `sheets/a_<H>_<F|P|Q|RQ>_<grey|body|sil>.jpg` — matched lineups at 208 / 218 / 229 (MF 203 endpoint, Skarn, Grask W2 provenance, Grask 05A, Gorrund W2 provenance, Gorrund 05A, Gorrund 230.9 ARM). `sheets/c_<H>_<region>.jpg` — close architectural views (`a_package.py`).
- `blind/` — 16-body blind sets (N = RM-OT-05A, P = W2 provenance), grey + silhouette sheets, keys, and `blind_results.json` (three independent uninformed scorer agents per set; `a_blind.py`).
- `validators/` — W2C (`w2c.json`) and W2D (`w2d.json`) reruns with registries, joint inputs and logs (`a_eval.py`); `tables.json` (rebuild vs W2 deltas, matched-height orderings; `a_tables.py`); `contour.txt`; `arm_clearance.txt`.
- `construction/` — build records and measurements of every candidate (`construction.json`) and every transported `A_*` body (`transport.json`).
- `search/` — every recipe tried (`arch_v1`–`v13` preview, `arch_R1`–`R7` built), uninformed-reviewer probe sheets and keys, `search_history.json`.
