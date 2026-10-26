# RP2 Grask production retopology v003 — reproducibility tools

Order: `reviews/chatgpt-rac-rp2-grask-thumb-web-visual-review-and-audit-closure-order.md`. `run_v003.sh` is the exact sequence.

What changed from v002 (`../grask_retopo_v002/`):

- **Cage** (`cage29`): ankle fan 7 → 10 rings (`ANKPHI`), elbow 4 → 6 rings (`ELBR`), one more palm ring at the MCP row
  (`UPOST` 14.18). Same architecture, same poles (166), ×2 density.
- **Short-edge quads**: `optfix.py` now also targets the longest/shortest edge ratio (`OPT_RSEL`, `OPT_RMAX`, `OPT_RING`, `OPT_OFF`)
  and refuses any patch that adds a fold or a self-intersection (Blender BVH test on a crop).
- **Thumb web**: `relaxg.py` — guarded tangential relaxation on the source surface (removes uneven quad spacing that shaded as rumples).
- **Audit on the exact deliverable**: `rbnpz.py` reads the exported blend back into the v005 frame; `finalaudit.sh` runs every gate on
  it. New `techx.py` (manifold vertices, Euler/genus, components, BOTH aspect statistics), `ringshow.py` (closed-ring evidence pictures),
  `lmdrift.py` splits independently measured landmarks from copied construction coordinates.
- **Inspection pictures**: `handview.py` (isolated hand/foot renders, `REGION=foot`, `ZMAX` crop, exported blend read back with the
  translation undone), `pick.py`, `twsec.py`, `twsheet.py`, `tw5.py`, `facesheet.py`, `sheets3.py` (strict: refuses missing panels).
