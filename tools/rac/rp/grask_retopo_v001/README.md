# RP2 Grask production retopology v001 — reproducibility tools

Cloud workspace scripts that produced `GR_U_REF_RP2_retopo_v001`. Analysis frame: cm, x = subject left, f = forward, u = up.
Blender frame = (x, −f, u)/100 m.

Inputs (cloud): `v005.npz` (frozen source geometry, verified equal to the frozen BLEND), `flab.npy` / `vlab.npy`
(31-part source labels from `mklabels.py`), `shoulder.json` (`shoulder.py`), `lm_src.json` (`lm.py` on v005),
the v004/v005 hand/foot construction models (`hand_model.py`, `hand_frame.py`, `foot_model.py` from the v005 source tools),
and the old GR5DE3 E3 joint seeds (diagnostic only).

Pipeline (`run21.sh`):

1. `build_cage.py cage21.npz` — authored quad cage (`cage.py`, `hands.py`, `feet.py`, `ears.py`) with tagged loops.
2. `pipe2.sh cage21.npz q21` — `subproj.py` (Catmull-Clark ×3, guarded per-part projection) → `polish.py` (+`rayproj.py`) →
   `crease.py` (bidirectional, part-aware crease capture) → `fixfold.py` → `crease.py` → `sxfix.py` / `crease.py` ×3.
3. `sxfinal.py`, `foldfix.py` — micro-fold and folded-face cleanup → `final.npz` (+ a 2-vertex collapsed-edge separation).
4. Gates: `sxq.py` (self-intersection), `dev.py` (T-1/T-2), `gate.py` (topology, density, T-3, T-4), `loopaudit.py`,
   `lm.py` + `lmdrift.py` (T-6), `iou.py` (T-7), `identity.py`, `folds.py`, `flipchk.py`; `tagloops.py`, `seams.py`.
5. Export: `export_retopo.py` (bpy) → `.blend`; `readback_rt.py`, `srccheck.py` (source hashes); `make_landmarks.py`,
   `make_sidecar.py`.
6. Evidence: `evidence.sh`, `wireh.py`, `diagF.py`, `tables.py`, `sheets.py`.

`sxq.py`, `sxfix.py`, `sxfinal.py`, `rayproj.py`, `export_retopo.py`, `readback_rt.py`, `srccheck.py` run in Blender's
Python (`bpy` 5.2.2); the rest run in CPython with numpy / scipy / libigl / trimesh.
