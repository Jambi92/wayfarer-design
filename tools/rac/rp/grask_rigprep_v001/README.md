# Grask RP2 rig-prep readiness — proposal v001 tools

These tools are read-only on every parent. They never build an armature, write weights, pose, or save a mesh. The gate is `reviews/claude-rac-rp2-grask-rigprep-readiness-gate.md`.

| File | Purpose |
|---|---|
| `run_rigprep.sh WORKDIR` | Runs the whole pipeline: before-hashes → npz equality → fits → proposal → tables → crops → renders → sheets → after-hashes |
| `hash_parents.sh`, `geomhash.py` | SHA-256 and geometry hash of every immutable parent (staged PC copies) |
| `npzcheck.py` | Proves that the analysis npz copies equal the v005 / v003 blends |
| `fitlib.py` | Section, axis and sphere fitting helpers, plus frame conversion (production = source + T, Blender = (x, −f, u)/100) |
| `rigprep_fit.py MESH.npz OUT.json` | Measurements on one mesh: limb axes, knee/ankle/hip/elbow/wrist/GH/SC definitions A/B, construction-joint validation, axial sections, eyes, mouth check |
| `compose.py` | Builds the proposal `GR_U_REF_RP2_rigprep_landmarks_v001.json`: provenance audit, consensus rule, uncertainty, depth, v003 Δ, hierarchy, segment lengths, right-handed Blender frames, flexion signs, asymmetry |
| `tables.py` | Readable markdown and csv tables |
| `crops.py` | Isolated hand and foot crops (connected piece containing the construction wrist) and the arm-free trunk used for the hip side views |
| `render.py`, `render_all.sh`, `views.sh` | Identical-camera orthographic clay renders (v005) and clay + wire renders (v003) in a derived, never-saved scene |
| `overlay.py` | 2-D overlay of proposals, alternatives, frozen values, construction and measured markers, axes and legend; sheet assembly |

**Measurement inputs:**
- v005 source: `/tmp/claude-0/src3d/v5/v005.npz`;
- v003 production freeze read-back: `/tmp/claude-0/rt/frz/v003_frz.npz` (source frame);
- frozen v005 extremity construction model: `/tmp/claude-0/src3d/v5/tools`.

The superseded MPFB/E3 skeleton is never read. Its only trace is the frozen package value, carried as alternative C.

## Diagnostic stage (order bf7d664): adjudicated landmarks v002, diagnostic rig v001, D1–D10

The pipeline is `run_diagstage.sh WORKDIR`.

| File | Purpose |
|---|---|
| `adjudicate.py`, `package.py` | Apply AD-R1…R12 and write `GR_U_REF_RP2_rigprep_landmarks_v002.json` with tables and the 27-check validation |
| `overlay2.py` | Landmark sheets drawn with the actual rig bones, with the rejected alternatives shown in grey |
| `rig_build.py` | Builds the derived `GR_U_REF_RP2_rigdiag_v001.blend` from a work copy of v003 (save-as to a new path only): 86 bones, bone-heat weights |
| `rig_clean.py` | The single logged weight cleanup: side bones zeroed more than 3 cm across the midline |
| `rig_check.py` | Checks Blender deformation against the numpy LBS, rest-return (T-1) and bone lengths (T-6) |
| `diag_lib.py`, `diag_run.py` | D1–D10 poses and measurements |
| `dqs_eval.py` | Preserve-volume (dual-quaternion) comparison |
| `run_diag.sh` | Runs the LBS suite, the DQS comparison and the pivot-placement comparisons |
| `judge.py` | Pass/fail against the AD-R12 criteria, with failure causes |
| `evidence.py`, `cmp_sheet.py` | Identical-camera clay + wire sheets |
