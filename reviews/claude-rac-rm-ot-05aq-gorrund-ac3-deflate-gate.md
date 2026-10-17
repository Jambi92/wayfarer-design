# RAC RM-OT-05AQ — Gorrund AC3 via broad feather + restrained deflate: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05aq-gorrund-ac3-deflate-order.md` (0847cdb)
**Source:** `GO-05AO_AC2.blend` (sha `ba129999…f6f3`, verified before every step).
**Executor:** Claude. The deflate and Smooth filters were authored in the Blender 5.2.2 UI on Tyler's PC. Cloud scripts were used only for the mask attribute, simulation, calibration read-back, gates and evidence.

## Verdict

**05AQ AC3 DEFLATE ROUTE NOT CREDIBLE / STOP**

- The active composition reverts to **`GO-05AO_AC2`** (unchanged). Nothing from 05AQ is frozen.
- The deflate direction is right. The buttocks lose the round bodybuilder read and keep substantial volume. Pelvis width, the skeletal hip, thigh radius and all protected anatomy pass.
- Two real attempts were made: AQ1 and the single permitted rerun, AQ1r.
  - **AQ1 failed technically:** a vertex collapsed onto a protected seam vertex beside the tail root, giving 6 self-intersecting faces, 2 degenerate faces and 2 non-manifold edges.
  - **AQ1r passed every numeric gate but failed §10/§12 visually:**
    - a raised, jagged plateau around the tail root, on both sides;
    - a vertical crease along the lateral hip and thigh mask boundary.
- Under §10, a second failure means STOP.
- **Root cause.** The hard 0.000 mm tail-junction set has an irregular outline that sits on the upper-medial buttock. Any deflation strong enough to matter leaves that outline standing proud. This is a constraint-design problem, not a filter-strength problem (§7 below).

## 1. Broad posterior mask (§4)

The mask was built by vertex ID: `postmask.py`, then `ramp.py`, then predictor refinement in `refine3.py`. Only `.sculpt_mask` was written; the geometry change is 0.000 mm (read-back).

**Sculptable region:**
- the 05AI glute region;
- trunk-dominant lateral and posterior hip soft tissue, z 88–118 cm, outside a sacral midline strip (|x| ≤ 4 cm);
- the posterior upper thigh, behind the thigh axis, above z 70 cm. That is about mid-thigh, so the lower transition is well below the glute fold.

**Feathering:**
- A 250-iteration diffusion ramp (gain 2) runs inside the region.
- v3/v4 add a guaranteed minimum-width ramp: 25 mm from any hard vertex, and 40 mm from the tail, tail junction, genital, perineal and sacral sets.
- Duplicate-position seam vertices get a 30 mm ramp (see AQ1).
- Predicted fold sites get small feathered bumps: 114 vertices.

**Hard 1.0:** all 05AF protected sets, the 05AI torso, arms, knees and lower legs, and thigh below 62 cm. Read-back is in `checks/mask_v4_readback.json`:

| Region | Mask min |
|---|---|
| Protected (all) | 1.0 |
| Torso | 1.0 |
| Elbows, knees, ankles, wrists | 1.0 |

The final region has 21 307 sculptable vertices, 14 412 of them below 0.5. Visualisation: `views/aq_mask_v4.jpg`.

## 2. Skeletal hip landmark (§5)

The blend has no armature, so no rig hip pivot exists in the file. The rig weights were used instead.

**Hip-joint core, L/R:** the thigh/trunk weight-blend ring (0.25 < w_thigh < 0.75) minus the authorised soft-tissue region (final mask < 1). That leaves 2 046 vertices on the left and 2 105 on the right.

**Landmark:** the centroid of the hip-joint core. These vertices are hard-masked, so the landmark tracks the skeletal blend and ignores the intended glute-fold motion. Drift is 0 whenever the hip-joint core is genuinely protected; the landmark's job is to verify that protection.

**Diagnostics only (not pass/fail):**

| Proxy | Left | Right |
|---|---|---|
| Angle-binned full ring (includes the glute fold) | 0.40 mm | 0.77 mm |
| Plain ring centroid | 0.63 mm | 0.87 mm |
| Retired surface-seam proxy | 1.29 mm | 1.35 mm |

All are measured on AQ1r. Code is in `aqmetrics.py` (`hip_core`, `hip_ring_binned`, `hip_seam_proxy`). Candidate comparison is in `hipcand.py`.

## 3. Inflate-negative calibration (§7)

Calibration was done on the scratch copy `GO-05AQ_calib_scratch.blend` (`checks/inflate_calibration.json`). Settings: Mesh Filter, Inflate, XYZ, Local.

| Drag | Strength | Result |
|---|---|---|
| A: −100 px, 10 events | 1.000 | −396 mm × (1 − mask); far too strong; undone |
| B: −100 px, 10 events | **0.020** | −7.92 mm × (1 − mask); corr 0.99999, residual 0.008 mm rms; max move 7.88 mm |

- The filter is non-cumulative: it uses original normals and coordinates.
- Leftward drag deflates.
- Masked vertices moved 0.000 mm.

**AQ1 deflate setting:** strength 0.020, −100 px. Result: 7.88 mm at the belly centre (≤ 12 mm ceiling ✓).

## 4. Predictor and repair (§6)

**Model:** the exact Inflate model above, followed by masked Laplacian Smooth iterations (05AN calibration). The predictor was bracketed at 150, 175 and 200 events because the real UI ran about 16% heavier than modelled.

**Flags checked:**
- flips;
- faces over 60° from their 1-ring;
- new local inversions;
- new self-intersections (pymeshlab);
- edge collapse (new edge under 0.3 mm or under 15% of its start length).

**Cycles:** v3/v4 needed 2 cycles to reach 0 at all three counts (`checks/mask_v4_predictor_log.json`).

**Repair:** no geometry repair was used, so 0 of the 50 neighbourhoods were spent. All instability was resolved with mask protection only, as in 05AO.

**Deflate-only intermediate:** it carries transient folds and self-intersections at the lateral and sacral-adjacent buttock (21 SI on AQ1). The Smooth cleanup removes them, as predicted. It is not a checkpoint.

## 5. Real attempts

### AQ1 (mask v2) — technical FAIL

Steps: deflate (0.020, −100 px), then Smooth (strength 1.000, 150 events).

**Result:**

| Check | Value |
|---|---|
| Self-intersecting faces | 6 |
| Degenerate faces | 2 |
| Non-manifold edges after weld | 2 |
| Flips | 0 |
| Protected regions | 0.000 mm |

All defects are at one site: x 6.3, z 95.6 cm, at the tail-root edge.

**Cause:**
- v2 had a hard mask step there: protected vertex at 1.0, neighbours at 0.41.
- The site sits on a duplicate-position seam: vertices 185348 and 185349 are split but position-welded.
- Blender smooths split vertices as open-boundary vertices, so the neighbour was pulled onto the protected seam vertex.
- The uniform-Laplacian model cannot see this, so the prediction was clean.

AQ1 was reverted. Files: `GO-05AQ_AQ1*.blend`; gates in `checks/aq1_first_attempt_*.json`.

### AQ1r (mask v4, the one allowed rerun) — numeric PASS, visual FAIL

**Steps:**
- Deflate: strength 0.020, −100 px, 10 events → `GO-05AQ_AQ1r_deflate.blend`.
- Smooth: strength 1.000, 144 mouse-move events → `GO-05AQ_AQ1r.blend` (sha `2d43a2d6…36b6`).

The real smoothing tracks the model at about 1.16× (the 150–200 bracket).

**Geometry gate vs AO2:**

| Check | Result |
|---|---|
| Topology | identical |
| Seams opened | 0 |
| Self-intersections | 0 |
| Flips | 0 |
| Degenerates | 0 |
| Topology (components / boundary / non-manifold) | 1 / 0 / 0 |
| Protected (all 05AF sets) | 0.000 mm |
| Torso | 0.000 mm |
| Arms | 0.000 mm |
| Lower legs | 0.000 mm |
| Thigh below 62 cm | 0.000 mm |
| Height | 204.5225 → 204.5225 cm |
| Bounding box | unchanged |

**Shape metrics (`checks/aq1r_metrics.json`):**

| Metric | Result | Limit |
|---|---|---|
| Deflate-stage max move | 7.88 mm | ≤ 12 ✓ |
| Final max move (after Smooth) | 18.5 mm | — |
| Pelvis core width | 518.72 → 518.72 mm (0.00%) | ≤ 0.5% ✓ |
| Skeletal hip (hip-joint core) | 0.000 / 0.000 mm | ≤ 0.5 ✓ |
| Upper posterior thigh radius | −2.12% / −1.80% | ≥ −3% ✓ |
| Buttock profile depth (mean of the 200 most-posterior points per side, z 92–108) | −3.6 mm L / −7.0 mm R | report |
| Single most-posterior point | −0.18 / −0.82 mm (it sits on the hard tail-side margin) | report |

**Visual gate (§10 and §12): FAIL.** Views: `views/pair_body_B.jpg`, `pair_body_P.jpg`, `zoom_AQ1r.jpg`, `zoom_AQ1r_P.jpg`, `aq1r_cmp_*.jpg`.

Passed:
- Back view: no longer two highly rounded bodybuilder glutes; the volume is still substantial and the fold is softer.
- The pelvis is still broad.

Failed:
- **Tail-side shelf:** a raised, jagged plateau around the tail root on both buttocks. Its outline is the irregular border of the hard tail-junction set. Displacement rises from about 0.5 mm at 0–3 mm from the set to a 90th percentile of 4–7 mm at 10–20 mm.
- **Mask outline:** vertical crease marks on the lateral hip and thigh at the lateral feather, plus small dents. They are visible in profile.

## 6. Decision

Per §10: AQ1 failed, the single predictive-repair rerun (AQ1r) also failed, so **STOP**. AQ2 (§11) is only for a clean but still-heroic result, so it does not apply. The active state is **GO-05AO_AC2**.

## 7. Recommendation for the author

The volume change itself works: about 4–7 mm of posterior depth reduction with no pelvis, hip or thigh cost. What blocks it is the hard boundaries.

1. **Tail junction.** Let the outer ring of the tail-junction set move as continuity tissue. For example, its outer 2–3 cm could move up to about 3 mm with a smooth falloff, while the tail root core, emergence height, angle and cross-section stay at 0.000 mm. Without this, every useful deflation exposes the set's jagged border. The alternative is a 70–80 mm tail ramp, which gives up most of the upper-medial reduction.
2. **Lateral boundary.** Widen the lateral hip and thigh feather to at least 50 mm, ending on the front and side thigh, or allow a tiny UI Smooth touch along that line.
3. **Seams.** Keep the 30 mm ramp from duplicate-position seam vertices. Blender's open-boundary smoothing at those vertices caused the AQ1 collapse.

## 8. Files (PC: `…\Gorrund-Neutral-C\05AQ\`)

| File | sha256 | Status |
|---|---|---|
| GO-05AQ_AQ1_prep.blend | 8ef4d7ce…a3c1 | AO2 + mask v2 |
| GO-05AQ_calib_scratch.blend | — | calibration scratch |
| GO-05AQ_AQ1_start / _deflate / GO-05AQ_AQ1.blend | 6af4d905… / 81251fce… / 81691e51… | rejected (technical) |
| GO-05AQ_AQ1r_prep.blend | 2dfa045e…5348 | AO2 + mask v4 |
| GO-05AQ_AQ1r_deflate.blend | 664da28c…0eaf | intermediate |
| GO-05AQ_AQ1r.blend | 2d43a2d6…36b6 | rejected (visual), evidence only |

Full hashes are in `checks/file_hashes.txt`. Scripts are in `tools/rac/w1/rmot05aq_drivers/`. The 05AN predictor, gate and renderer were reused. Blender was closed at the end.

## 9. State

Gorrund UNACCEPTED; Grask E3 FROZEN; RM-OT-05 OPEN; Stage C BLOCKED. No LOW, blind final acceptance or scaffold. No D4, UE5, production rigging or creator implementation.
