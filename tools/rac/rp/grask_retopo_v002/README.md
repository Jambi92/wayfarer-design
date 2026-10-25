# RP2 Grask production retopology v002 — reproducibility tools

Cloud workspace scripts that produced `GR_U_REF_RP2_retopo_v002` (order `reviews/chatgpt-rac-rp2-grask-retopo-v002-production-optimization-order.md`).
`run_v002.sh` is the exact sequence. Analysis frame: cm, x = subject left, f = forward, u = up; Blender = (x, −f, u)/100 m, shifted by the
production-origin translation recorded in `v002_origin.json` / the sidecar.

What changed from v001 (`tools/rac/rp/grask_retopo_v001/`):

- **Density** — Catmull-Clark ×2 instead of ×3 (`pipeL.sh CAGE OUT 2`). The authored cage keeps the v001 architecture and gains support
  loops where ×2 fell short of the joint-loop minimums: palm MCP row (`UPOST`), finger/toe proximal phalanges (`FINP1`, `TOEP1`),
  forefoot planes at the toe-MTP row (`FFW`), shoulder fan (`NFAN=18`). `CLPUSH` (web-cap pull toward the cleft floor) is on by default.
- **Quad quality** — `centfix.py` (quads whose centroid floats off v005 across a narrow crease), `qopt.py` recipe (`recipe.sh`), `revsx.py`
  (undo any move that creates a self-intersection), `lrepair.py` (patch smoothing / bounded off-surface relaxation with a deviation guard),
  `optfix.py` (direct local optimisation of the last web-root slivers). `crease.py` gained `CGUARD` and a box-restricted relax.
- **Gates** — `gate.py` density rule = contract ceiling as maximum MEAN edge (p99 still reported); `loopaudit.py` loop count =
  max(closed-ring trace, min-over-sides surface path) — v001 still passes 69/69 under it; `lm.py` measures surface-fit features on dense
  (~1.2 mm) area samples (applied to v005, v001 and v002 alike); new `symm.py`, `origin.py`, `poleaudit.py`, `density_table.py`.
- **Export** — `export_retopo.py` takes `ORIGIN_T` (one rigid translation) and `RETOPO_NAME`.

`sxq.py`, `sxfix.py`, `sxfinal.py`, `rayproj.py`, `export_retopo.py`, `readback_rt.py`, `srccheck.py` run in Blender's Python (`bpy` 5.2.2);
the rest run in CPython with numpy / scipy / libigl / trimesh.
