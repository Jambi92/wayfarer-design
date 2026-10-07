# RAC W1n — Vael W1 acceptance gate evidence

Order: GitHub Issue #1, final Aelari ruling comment (Vael next; recorded in `reviews/chatgpt-rac-w1l-grask-order-issue1-record.md`). Gate: `reviews/claude-rac-w1n-vael-acceptance-gate.md`. Nothing here is canon or accepted.

| Path | Contents | Produced by |
|---|---|---|
| `tables.md` | All tables (generated) | `tools/rac/w1/gen_w1n_docs.py` |
| `central_<tag>.json` | Directional and skin rows (accepted Aelari AEL1, Gorrund, Grask in their slots), the added canon-derived rows, distribution; tags W1g, VAL1…VAL5, frames (NARROWB, BROADB, NARROW, BROAD), composition (LOWMUS, HIMUS, HIFAT, HIBOTH, LOW) | `w1n_drivers/va_eval.py` |
| `skeletal_<tag>.json` | CIB skeletal rows on the W1i base with accepted AE and GR: W1g (control reproduces W1i to 5e-13), VAL4, NARROW, BROAD, NARROWB, BROADB | `w1n_drivers/va_skel.py`, grids `va_grid.py` |
| `composition.json`, `separation.json` | Continuity readings, same-composition low check; % difference of VAL4 from each population | `w1n_drivers/va_comp.py` |
| `sheets/*.jpg` | Separation lineup; trunk / lumbar side crop; VAL4 frames and minimum composition; composition variants | `w1n_drivers/render_AS_RUN.sh` |

Construction record: `tools/rac/w1/cfg/w1n/VA.json`. VA as-built geometry = W1g (vertices identical to `reviews/rac-w1g-evidence/geometry/VA_r6.npz`; build record matches `cfg/w1g/VA.json`).
