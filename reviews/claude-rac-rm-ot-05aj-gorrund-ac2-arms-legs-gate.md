# RAC RM-OT-05AJ — Gorrund AC2 arms and legs: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05aj-gorrund-ac2-arms-legs-order.md` (676da93)
**Parent:** passed 05AI AC1 (`GO-05AI_AC1.blend` sha256 `89a19ba2…0dae`, `.glb` `68d876df…5e36`, both re-verified unchanged on the PC after this order)
**Executor:** Claude (UI-only sculpt in Blender 5.2.2 on Tyler's PC; cloud scripts only for preflight, gates and evidence)

## Verdict

**05AJ AC2 NOT CREDIBLE / STOP**

The AC2 attempt is rejected. The active checkpoint stays the **passed 05AI AC1**; nothing was written over it. AC3 was not started.

Why it fails:
- **Technical:** the final AC2 state has **4 flipped faces**: right upper arm ×3 at about 124–146 cm, and the left knee at about 55 cm. The earlier, lighter passes had 0. Every other technical gate passes.
- **Visual:** the heroic forms are only marginally softened:
  - the teardrop above the knee, the calf bellies and the biceps/triceps separation still read heroic;
  - the forearm cords are only moderately softer;
  - repeated Smooth strokes left **visible stroke-boundary shelves and lumps** on the left shin, the right calf and the front of the left thigh.

  This fails "teardrop materially softened", "calf bulges less heroic" and "no new dents / ridges / shelves".
- **Method limit:** on this 1 M-face mesh, each remote mouse-drag Smooth pass moves the surface by only about 0.8 mm median (p95 about 2.3 mm). The heroic relief is centimetre-scale, so reaching the visual target would need many more passes. Each pass so far has added stroke artefacts and flips faster than it removed relief. A Flatten/Contrast pass at 0.35 moved the surface by at most 1.2 mm. I did not use Mesh Filter or any whole-limb automated smoothing (the order forbids broad limb optimisation and slimming).

## 1. Masks (verified before any stroke)

The masks were built UI-only in `GO-05AJ_working.blend`:
1. clear;
2. limb boxes;
3. invert;
4. Smooth Mask (feathering), done **before** any hard mask;
5. hard boxes for the head, torso, shoulder tops, front hip/genital, hands, feet, glute/tail-root, tail, tail gap and armpit strips.

No Smooth Mask was run after the hard masks. The `.sculpt_mask` attribute was read back in the cloud:

| Set | Min mask | Vertices < 1 |
|---|---|---|
| head, tail, tail junction, genital, perineal, hands, feet (05AF protected sets) | 1.0 | 0 |
| 05AI torso / glute / pelvis_other | 1.0 | 0 |

Sculptable share (mask < 0.5): upper arm 0.72, forearm 0.67, thigh 0.86, shin 1.00.

## 2. Mesh-quality preflight (passed, then repaired)

- **Scan:** 392 524 arm/leg zone faces; 2 092 faces with quality < 0.15; 35 crimp-like faces (folded > 60° against all neighbours).
- **Dry run** (simulated uniform Laplacian smoothing, in memory only): only **2** of the 35 crimps actually flip:
  - face 599288 at the right knee;
  - face 744896 at the right thigh.

  The other simulated flips are ordinary slivers, which this order does not authorise repairing. That count is well within the 8-neighbourhood budget.
- **Repair:** the proven 05AI method (`ai_local_flip_fix.py`, `AI_FACES=599288,744896`):
  - 6 vertices moved, ≤ 0.5 mm;
  - 21 near-coplanar edge rotations;
  - 35 faces changed, all inside the two 2-ring neighbourhoods;
  - 0.000 mm outside them;
  - patch deviation ≤ 0.12 mm;
  - 0 SI / flips / degenerates;
  - 1 / 0 / 0 topology;
  - folds over 60° reduced from 6 to 0;
  - protected regions 0.000 mm.
- **Output:** `GO-05AJ_preflight_baseline.blend` (sha256 `453ee2ba…d6d5`) / `.glb` (`6a6eb730…46a1`).

Evidence: `checks/preflight.json`, `checks/preflight_dry_smooth.json`, `checks/aj_prep_report.json`, `checks/aj_prep_gates.json`.

## 3. AC2 sculpt log (UI only, front and right orthographic views)

| Pass | Brush | What | Flips | Gates otherwise |
|---|---|---|---|---|
| s1 | Smooth 0.5, 30 px | single strokes on arms, thighs, knees, shins | 0 | all pass |
| p1 | + Smooth, side view | triceps, biceps, forearm, calf, front knee, hamstring | 0 | all pass |
| p2 | Smooth 0.7, 40 px | zigzags on calves, knee, thigh, triceps, forearm (side); teardrops, quads, calves, arms (front) | 0 | all pass |
| p3 | Flatten/Contrast 0.35, 40 px | teardrops, outer quads, calves, biceps, forearms | 0 | all pass (max 1.2 mm move) |
| p4 | Smooth 1.0, 40 px | dense zigzags: teardrops, quads, calves, arms | 1 | all else pass |
| p5 | Smooth 1.0 ×2 | same | 2 | all else pass; stroke shelves appear |
| p6 (final) | Smooth 0.5 | long vertical blending strokes on both legs and arms | **4** | all else pass; shelves remain |

p1–p3 were technically clean, but visually they are nearly identical to AC1. They do not meet the visual gate either.

Per-pass gate JSONs are in `checks/aj_pass_*_gates.json`.

## 4. Final AC2 attempt — technical gate (vs 05AJ preflight baseline)

| Gate | Result |
|---|---|
| topology identical | yes |
| opened seams | 0 |
| self-intersections | 0 |
| flipped faces | **4 — FAIL** (−35.0, −42.7, 124.5), (−24.8, −36.7, 124.3), (−31.7, −34.2, 145.5), (12.5, −44.4, 54.6) cm |
| degenerate faces | 0 |
| position-welded components / boundary / non-manifold | 1 / 0 / 0 |
| head, tail, tail junction, genital, perineal, hands, feet | 0.000 mm |
| 05AI torso, glute, pelvis_other | 0.000 mm |
| wrist/ankle buffers | 0.000 mm |
| trunk-to-limb transition band (disclosed) | max 4.66 mm (shoulder and upper-thigh continuity only; torso proper 0.000 mm) |
| limb displacement | max 11.0 mm; p95 of moved vertices: upper arm 4.5, forearm 4.7, thigh 5.5, shin 4.1 mm |
| stature / bbox | unchanged (204.5225 cm; 84.744 × 136.339 × 204.522 cm) |

Hands and feet were at 0.000 mm and the masks pinned the joints, so the crotch, fingertip and ankle relationships did not move. Knee-region displacement stays ≤ 11 mm and is surface smoothing only. The visual failure above stands regardless.

Files: `checks/aj_ac2_final_gates.json`, `checks/aj_ac2_final_region_disp.json`.

## 5. Visual evidence (identical cameras; Workbench studio, orthographic)

`views/aj_cmp_*.jpg` shows 05AI AC1 (left) against the rejected 05AJ AC2 attempt (right) in:
- whole F / P / B / 3/4;
- body-only F / P / B / 3/4;
- both arms front and 3/4;
- each arm in profile (right and left);
- both thighs/knees front and 3/4;
- both calves in profile and back.

`views/aj_defect_map.jpg` shows the displacement heat map with the 4 flip sites.

Renderer: `tools/rac/w1/rmot05aj_drivers/aj_render_views.py`. The gate runner and check scripts are alongside it.

## 6. Files

On the PC, in `RaceBodies/source/Gorrund-Neutral-C/05AJ/`:

| File | Status |
|---|---|
| `GO-05AJ_preflight_baseline.blend` / `.glb` | passed prep |
| `GO-05AJ_working.blend` | masks only |
| `GO-05AJ_AC2.blend` (sha256 `6a3b64bb…92af`) | **REJECTED**, evidence only |
| `GO-05AJ_AC2_REJECTED.glb` (sha256 `f8b48ccb…f285`; cloud export of the same state) | **REJECTED**, evidence only |
| `05AJ_README_REJECTED.txt` | marks the folder |

Blender was closed after the work. One older frozen Blender window from a previous session and one File Explorer window are still open on the PC; they were left for Tyler.

## 7. Recommendation to the author (for ChatGPT / Tyler)

AC2 by remote single-pass mouse-drag Smooth/Flatten is not converging on this dense mesh. Options for a follow-up order:

- **(a)** Author an explicit, bounded, UI-applied **Mesh Filter (Surface Smooth / Relax)** pass inside the existing verified limb masks, with stated iteration and strength limits. This keeps the work UI-only, but it is a deliberate whole-zone operation and needs order authority.
- **(b)** Allow Tyler-performed hand sculpting with a tablet for AC2. The masks in `GO-05AJ_working.blend` are already verified and reusable.
- **(c)** Accept a lighter AC2 target. The technically clean p2 state was barely different from AC1, so it is not a real alternative under the current visual gate.

## State

**Gorrund UNACCEPTED; Grask E3 FROZEN; RM-OT-05 OPEN; Stage C BLOCKED.** No LOW, no blind final acceptance, no scaffold, no D4/UE5/rigging/creator work. AC3 not started.
