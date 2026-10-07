# RAC W1o — Vael Broad-frame correction evidence

Order: `reviews/chatgpt-vael-w1n-author-ruling-w1o-order.md` (= GitHub Issue #1 comment 2026-10-07T15:53Z). Gate: `reviews/claude-rac-w1o-vael-acceptance-gate.md`. Nothing here is canon or accepted.

| Path | Contents | Produced by |
|---|---|---|
| `tables.md` | All tables (generated) | `tools/rac/w1/gen_w1o_docs.py` |
| `skeletal_<tag>.json` | CIB skeletal rows (W1i base, accepted AE AEL1 and GR W1l): VAL4, BROADB (W1n), BROADB_P112 / P114 / P116 | `w1n_drivers/va_skel.py` (`EVDIR`), grids `va_grid.py` (frames `BROADB_P<nnn>`) |
| `central_<tag>.json` | Added, skin and directional rows for the same bodies | `w1n_drivers/va_eval.py` (`EVDIR`) |
| `continuity.json` | Trunk continuity readings: central, Narrow, the Broad candidates, MF, AE, FN | `gn6.cont`, `waist_rise` |
| `sheets/*.jpg` | Broad four-view (central, W1n Broad, W1o Broad, Narrow); trunk crop (central, W1o Broad, W1n Broad, x1.16 probe) | `w1n_drivers/render_w1o_AS_RUN.sh` |
