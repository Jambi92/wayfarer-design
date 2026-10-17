# RAC RM-OT-05AL — predictive limb-quality pre-pass and one AK1 rerun: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05al-predictive-limb-quality-prep-order.md` (46c0ec7)
**Source:** `GO-05AJ_preflight_baseline.blend`, sha256 `453ee2ba…d6d5`, verified before use.
**Executor:** Claude.
- **Cloud (bpy / numpy):** the diagnostic dry-runs and the bounded local repair.
- **Tyler's PC, Blender 5.2.2 UI only:** the mask rebuild and the single real Mesh Filter.

## Verdicts

1. **05AL PREDICTIVE LIMB PREP PASS / AK1 UI RERUN AUTHORIZED**
2. **05AL AK1 STABILITY PASS / READY FOR CONTROLLED AC2 FILTER BUILDUP**

I stopped there. I did not apply AK2 or AK3, and I did not start AC3.

## 1. Predictive dry-run (diagnostic only; never saved or promoted)

`tools/rac/w1/rmot05al_drivers/dryrun.py` is a numerical replica of Blender's Mesh Filter **Surface Smooth**. It implements the surface-smooth Laplacian step plus the displace step with α = Shape Preservation 0.5 and β = Per Vertex Displacement 0.5. It runs on the exact 05AK saved mask, with fade = f·(1 − mask).

**Calibration against the real 05AK AK1 result:**
- With **f = 0.78**, per-vertex displacement correlates **0.998** with the real filter.
- p99 residual is 0.09 mm; max residual is 0.47 mm.
- It predicts **exactly the same 15 flipped faces** (15/15 overlap, no extras).

**AK1-equivalent case:** one application at f = 0.78. Limb median 0.287 mm, p95 0.850 mm, max 3.05 mm.

**2× stress case:** eight sequential AK1-equivalent applications, which give a cumulative median of 0.577 mm (2.0× AK1), p95 1.66 mm and max 6.37 mm. Flips were collected at *every* step (union), not only at the end.

Why eight applications rather than one: a single application at f = 1.56 also gives about 2× the median, but its fade exceeds 1. That overshoots the Laplacian target and is numerically unstable (149 flips). It is not a mesh-quality signal and no UI step in the authorised range would do that, so I report it for information only. The sequential definition is the realistic "next safe step" (repeated conservative applications).

**Flag rule:** a face is flagged if it flips in either case, or if it is adjacent to a flipped face with a fold over 60° after the dry run.

## 2. Repair cycles (`al_repair.py`; `checks/al_repair_log.json`)

| Cycle | AK1 flips | AK1 adjacent >60° | 2× flips | 2× adjacent >60° | Neighbourhoods | Relaxed vertices | Edge rotations |
|---|---|---|---|---|---|---|---|
| 1 | 15 | 45 | 27 | 81 | 26 (merged two-ring) | 81 | 346 |
| 2 | 1 | 3 | 1 | 3 | 1 (inside / merged with the existing union) | 3 | 2 |
| 3 (analysis) | **0** | 0 | **0** | 0 | — | — | — |

- **Budget:** at most 27 neighbourhoods were used, well under the 60-neighbourhood limit. The repair took 2 cycles, with the 3rd used only for analysis (limit 3).
- **Relax:** 8 uniform-Laplacian half-step sweeps on the vertices of predicted-flip faces only, capped at **0.5 mm from the source position**.
- **Edge rotations:** the 05AI conditions throughout:
  - convex quad;
  - new diagonal absent;
  - dihedral < 15°;
  - new triangles within 0.97 of the local plane;
  - orientation preserved (dot > 0.95);
  - worse-triangle quality improved by > 0.02.
- **Protected vertices:** none of the 05AF protected sets or the 05AI torso/glute/pelvis_other were movable or touchable by a rotation.

## 3. Preservation gate (`checks/al_prep_gates.json`)

| Gate | Result |
|---|---|
| vertices / faces | 542 522 / 1 000 000 (unchanged) |
| vertices moved | 81, all inside the neighbourhood union (1 008 vertices) |
| movement outside the union | **0.000 mm** |
| max vertex movement | 0.500 mm (cap) |
| faces changed | 570, all inside the union |
| duplicate faces | 0 |
| patch surface deviation | new→old 0.342 mm, old→new 0.274 mm (≤ 0.5) |
| self-intersections / degenerates / patch faces inverted | 0 / 0 / 0 |
| position-welded components / boundary / non-manifold | 1 / 0 / 0 |
| protected regions (head, tail, tail junction, genital, perineal, hands, feet) | 0.000 mm |
| 05AI torso / glute / pelvis_other | 0.000 mm |
| patch minimum triangle quality | 0.0051 → 0.0288 |
| stature / bbox | unchanged (204.52246 cm) |

**Disclosure — static micro-folds:** the patch now has 7 dihedral edges over 60°, against 2 before.
- 2 of the 7 are pre-existing and untouched (right wrist area, z ≈ 121 cm).
- 5 are new, at the two crimp sites where the 0.5 mm relax cap was reached: the left knee (z ≈ 61.6 cm, the former flip face 406795) and the left upper arm (z ≈ 130.1 cm, the former flip face 218584).

They sit on faces of a few tenths of a mm². Both dry-runs predict them stable (0 flips, 0 adjacent >60° flags), and they are not visible in the renders.

**Frozen baseline:**
- `GO-05AL_predictive_limb_safe_baseline.blend`, sha256 `dcffb0dc5509f03faf6865b8818a88398225157a872702cfe3c8208d57907881`
- `GO-05AL_predictive_limb_safe_baseline.glb`, sha256 `d30daf24020be2e74f96f81429822ced3291ff17c2f34ad62c14607288dba8b6`

## 4. Mask rebuild (UI) and read-back (`checks/al_mask_readback.json`)

I opened the frozen baseline in the Blender UI and saved it as `GO-05AL_working.blend`, so the baseline file itself was never touched. I repeated the exact 05AK procedure at the same framing:
- front view: clear, limb boxes, invert, joint-preservation boxes (elbows, wrists, knees, ankles);
- Smooth Mask ×3, then the hard boxes (torso, head, shoulder tops, hip/genital, hands, feet, armpit strips);
- right view: tail and top of the feet.

No Smooth Mask was run after any hard box.

| Check | Result |
|---|---|
| geometry vs the frozen 05AL baseline | 0.000 mm |
| all 05AF protected sets | min 1.0, 0 vertices < 1 |
| 05AI torso / glute / pelvis_other | min 1.0, 0 vertices < 1 |
| joint centres (mean mask) | elbows 0.96 / 0.96, wrists 0.99 / 1.0, knees 0.96 / 0.98, ankles 0.995 / 0.92 |
| mid-belly zones (mean mask) | biceps 0.31 / 0.22, forearms 0.01, thighs 0.08 / 0.05, calves 0.00 |
| difference from the 05AK mask | 269 box-edge vertices |

I re-ran both dry-runs with the rebuilt mask. They still predict 0 / 0 flips.

## 5. Real UI AK1 (`GO-05AL_AK1.blend`)

**Settings, as shown in the UI:**

| Setting | Value |
|---|---|
| Tool | Mesh Filter |
| Filter Type | **Surface Smooth** |
| Strength | 1.000 |
| Deform Axis | X Y Z |
| Orientation | Local |
| Shape Preservation | 0.500 |
| Per Vertex Displacement | 0.500 |
| Application | one 200 px horizontal drag (identical to 05AK) |

No scripted invocation and no brush strokes were used.

**Files:**
- `GO-05AL_AK1.blend`, sha256 `a23364426da9866f315d132fe995b19a2ca274c6b45e8d9cf84b25f166eb37cc`
- `GO-05AL_AK1.glb` (review export of the same saved state), sha256 `23d5dec3c5d4a291b4e26b5aca2550ddf7a35dffc94b0806547b195d78879955`

### Gate (vs the frozen 05AL baseline; `checks/al_ak1_gates.json`)

| Gate | Result |
|---|---|
| topology identical | yes |
| opened seams | 0 |
| self-intersections | 0 |
| **flipped faces** | **0** (05AK: 15) |
| degenerate faces | 0 |
| position-welded components / boundary / non-manifold | 1 / 0 / 0 |
| head, tail, tail junction, genital, perineal, hands, feet | 0.000 mm |
| 05AI torso / glute / pelvis_other | 0.000 mm |
| trunk-to-limb transition band (disclosed) | max 0.92 mm |
| wrist/ankle buffers (light transition) | max 1.12 mm |
| stature / bbox | unchanged (204.5225 cm) |
| joint-centre drift (elbow, wrist, knee, ankle ring centroids) | ≤ 0.0013 mm (`checks/al_ak1_extra_checks.json`) |
| dihedral edges > 60° (whole mesh) | 505 → 487 (smoother, no new creases) |

**Displacement** (`checks/al_ak1_displacement.json`) is the same order of magnitude as 05AK AK1, as required:

| Zone | Median | p95 | Max |
|---|---|---|---|
| all limbs | 0.289 mm | 0.855 mm | 3.12 mm |
| upper arm | 0.245 | 0.669 | 1.89 |
| forearm | 0.232 | 0.660 | 1.70 |
| thigh | 0.366 | 1.067 | 3.12 |
| shin | 0.291 | 0.810 | 2.53 |

**Watch-list for the next order:**
- **No face inverted, but 5 face normals rotated more than 60°**: faces 262682 (80°, left shoulder/upper arm, z 156.8 cm), 431821 (75°, left upper arm, z 141.7), 549806, 962795 and 406794. They are the most likely first flips under heavier buildup.
- **A repeat of the predictive pass is advisable:** running the dry-run on each new checkpoint before each further filter step is cheap and has proven exact here.

### Visual

`views/al_cmp_*.jpg` shows three panels at identical cameras: 05AI AC1 | 05AL predictive-safe baseline | 05AL AK1. The views are:
- whole F / P / B / 3/4;
- body-only F / P / B / 3/4;
- arms front and 3/4;
- each arm in profile;
- thighs and knees front and 3/4;
- calves profile and back.

The predictive repair has no visible silhouette effect. AK1 is clean (no shelves, ridges, dents or filter artefacts), and limb relief is only very subtly softer. That is expected: this order was the stability proof, not the AC2 finish.

## 6. Files

On the PC, in `RaceBodies/source/Gorrund-Neutral-C/05AL/`:

| File | Status |
|---|---|
| `GO-05AL_predictive_limb_safe_baseline.blend` / `.glb` | frozen predictive-safe baseline |
| `GO-05AL_working.blend` | baseline + verified joint-banded masks (no geometry change) |
| `GO-05AL_AK1.blend` / `.glb` | stability-proof checkpoint |
| `05AL_README.txt` | marks the folder |

The 05AI AC1, 05AJ preflight and all rejected 05AJ/05AK files are untouched.

Scripts are in `tools/rac/w1/rmot05al_drivers/`: `dryrun.py`, `predict2.py`, `al_repair.py`, `maskcheck_al.py`, `alcheck.sh`.

Blender was closed after saving. Only the older frozen Blender window and a File Explorer window, both from an earlier session, remain open on the PC.

## State

**Gorrund UNACCEPTED; Grask E3 FROZEN; RM-OT-05 OPEN; Stage C BLOCKED.** No LOW, no blind final acceptance, no scaffold, no D4/UE5/rigging/creator work.

**Active checkpoints:**
- **Passed torso:** 05AI AC1, which is preserved inside all 05AL files.
- **AC2 working:** 05AL AK1, the stability-proof checkpoint. AC2 is not yet visually complete; it awaits the controlled filter-buildup order.
