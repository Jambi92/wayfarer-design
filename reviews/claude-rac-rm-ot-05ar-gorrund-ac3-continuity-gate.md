# RAC RM-OT-05AR — Gorrund AC3 continuity-ring correction: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05ar-gorrund-ac3-continuity-order.md` (87c074f)
**Source:** `GO-05AO_AC2.blend` (sha `ba129999…f6f3`, verified before each prep write).
**Executor:** Claude. The deflate and Smooth filters were authored in the Blender 5.2.2 UI on Tyler's PC. Cloud scripts were used only for masks, simulation, read-back, gates and evidence.

## Verdict

**05AR AC3 CONTINUITY CORRECTION NOT CREDIBLE / STOP**

- The active composition reverts to **`GO-05AO_AC2`**. Nothing from 05AR is frozen.
- **What the core/ring split fixed:**
  - The jagged tail-root plateau is gone. The root now blends through a soft, round transition.
  - The immutable tail core is exactly 0.000 mm, including centroid, emergence height, axis and cross-section.
  - The continuity ring moved at most 2.07 mm (limit 3.0).
  - AR1r passes every numeric and topology gate.
- **What is still wrong:** AR1r (the final permitted attempt) still shows **vertical creases on the lateral hip and front-lateral thigh, on both sides**. These are real folds, not shading: new edge dihedrals reach up to 59°. They sit in the high-mask transition band where the field ends at the front of the hip and thigh. That fails §11 and §12 ("no vertical lateral crease"), so the order requires STOP.
- **Why the §7 touch was not used:**
  - It is for *one isolated* residual crease. Here there are lines on both sides.
  - The creases sit where the mask is 0.95–1.0, so a masked Smooth brush cannot reach them.
- **Root cause (§7 below).** The creases grow with the number of Smooth events. The predictor's ">60° fold" threshold was too loose to catch them.

## 1. Immutable tail core vs continuity ring (§4)

Definitions are in `checks/tail_core_ring_definition.json`.

- **Interface:** the 207 free-tail vertices that touch the 05AF tail-junction set.
- **Immutable core (67 006 vertices):**
  - all 66 589 free-tail vertices;
  - the 417 tail-junction vertices within 8 mm of the interface.
  - These are hard-masked at 1.0.
- **Continuity ring:** the other 1 478 tail-junction vertices, 8–30 mm from the interface.
- **Core validation on AR1r:**

| Metric | Result |
|---|---|
| Root centroid | 0.000 mm |
| Emergence height | 0.000 mm |
| Root axis (PCA of proximal 12 cm of tail) | 1.5e-6° (float noise) |
| Root width (x) | 0.000 mm |
| Root depth (y) | 0.000 mm |
| Free tail | 0.000 mm |

## 2. Masks

**AR1 mask:**
- **Region:** the field (`armask.py`) is the 05AI glute region, plus the trunk lateral and posterior hip (z 88–118 cm, y > −46 cm, |x| > 4 cm), plus the thigh above 70 cm on its posterior and lateral side, plus the continuity ring.
- **Feather:** a diffusion ramp, then a graph Lipschitz limit: no edge changes mask faster than 1 per 50 mm. That satisfies both the 50 mm lateral and posterior-thigh rule and the 30 mm seam rule.
- **Refinement:** predictor-driven, `refine_ar.py`.

**AR1r mask (`tailramp.py`; read-back `checks/mask_ar5_readback_AR1r.json`):**
- The ring is driven by distance to the root core instead of the irregular 05AF set: the mask stays 1.0 out to 22 mm, then falls by smoothstep over 60 mm.
- All 220 duplicate-position seam vertices in the field are pinned to 1.0.
- The Lipschitz limit is re-applied.

**Read-back:** geometry changed 0.000 mm and the read-back matches the design. Mask minimums:

| Set | Min mask |
|---|---|
| Core | 1.0 |
| Ring | 0.994 |
| Genital, perineal, head, hands, feet, torso, joints | 1.0 |
| Duplicate seam vertices | 1.0 |

The maximum mask slope is 1.0 per 50 mm. Visualisation: `views/ar_mask_AR1r.jpg`.

## 3. UI settings (§9)

| Step | Settings |
|---|---|
| Deflate | Mesh Filter Inflate, strength **0.020**, −100 px drag in 10 events (same as the AQ calibration: −7.92 mm × (1 − mask)) |
| Cleanup | Mesh Filter Smooth, strength 1.000: 148 mouse-move events (AR1), 144 (AR1r) |

AR1r used the same deflate strength as AR1, so there was no increase.

## 4. Predictor (§8)

**Model:** the exact Inflate model, then masked Laplacian iterations bracketed at 150, 175 and 200 events.

**Checks:**
- flips;
- faces over 60° from their 1-ring;
- new local inversions;
- new self-intersections;
- new edge collapse (under 0.3 mm or under 15% of start length);
- ring and core displacement;
- seam vertices.

**AR1 mask:** reached 0 on all flags in 7–9 cycles (mask-only refinement; 0 geometry-repair neighbourhoods spent). The ring was predicted at ≤ 2.59 mm.

**AR1r mask:** 0 on all flags. The ring was predicted at 1.71 mm and the core at 0.000. Logs are `checks/predictor_*.json`.

## 5. Real attempts

### AR1 — technical FAIL

Sha `6979eed3…f6ab`; gates in `checks/ar1_*.json`. Failures:
- 3 duplicate-seam pairs opened (up to 2.58 mm), giving 8 boundary edges after the weld.
- The continuity ring moved 3.42 mm (limit 3.0).

**Cause:**
- The seam pairs sit at the sacral margin (x ≈ −0.4, z ≈ 102 cm). The two copies of each split pair had different mask values (1.0 vs 0.93), so Blender moved one and not the other.
- The real smoothing also ran about 1.4× the model in the high-mask ring band.

**Fix for the rerun (mask only):**
- seam copies forced equal and pinned at 1.0;
- the ring driven by a smooth distance ramp;
- the ring target lowered to ≤ 1.9 mm in the model.

Visually, the plateau was already smaller but still had a ragged edge (`views/ar1_body_B.jpg`).

### AR1r (the one bounded rerun) — numeric PASS, visual FAIL

**Files:**

| File | sha256 |
|---|---|
| GO-05AR_AR1r.blend | `bba06880…9d4b` |
| GO-05AR_AR1r_deflate.blend | `fec9c973…6d03` |

**Geometry gate vs AO2 (`checks/ar1r_gates.json`):**

| Check | Result |
|---|---|
| Topology | identical |
| Seams opened | 0 |
| Self-intersections | 0 |
| Flips | 0 |
| Degenerates | 0 |
| Components / boundary / non-manifold | 1 / 0 / 0 |
| Height | 204.5225 → 204.5225 cm |
| Bounding box | unchanged |

**Shape metrics (`checks/ar1r_metrics.json`):**

| Metric | Result | Limit |
|---|---|---|
| Immutable tail core, free tail, genital, perineal, head, hands, feet | 0.000 mm | 0.000 ✓ |
| Arms, torso (05AI), lower legs, thigh < 62 cm | 0.000 mm | 0.000 ✓ |
| Continuity ring | 2.07 mm | ≤ 3.0 ✓ |
| Duplicate seam vertices | 0.000 mm | — |
| Deflate-stage max move | 7.92 mm | — |
| Pelvis core width | 518.72 → 518.26 mm (−0.09%) | ≤ 0.5% ✓ |
| Skeletal hip (hip-joint core, 1 946 / 2 027 vertices) | 0.000 / 0.000 mm | ≤ 0.5 ✓ |
| Upper posterior thigh radius | −2.67% / −2.46% | ≥ −3% ✓ |
| Buttock depth (mean of 200 most-posterior points, z 92–108) | −3.4 mm L / −5.4 mm R | report |

**Visual gate:**

| Check | Result |
|---|---|
| Jagged tail-root plateau | **eliminated** (`views/ar_tailroot_B.jpg`, `ar_close_B.jpg`) |
| Buttocks substantial and natural, no bodybuilder projection | ✓ |
| Lower fold soft | ✓ |
| Profile (no lateral crease in true profile) | clean ✓ |
| Lateral hip / front-lateral thigh, both sides | **FAIL** |

The failing lines show as vertical stripes in front and three-quarter views (`views/hip_body_34.jpg`, `hip_body_F.jpg`, `crease34.jpg`). New edge dihedrals:

| Increase | Edges |
|---|---|
| > 8° | 992 |
| > 20° | 155 |
| Maximum | 59° |

They run along the lateral hip at about x ±26 cm, y −46 cm, z 94–111 cm, and down the front-lateral thigh.

## 6. Decision

AR1 failed technically and AR1r failed visually, so §9 requires **STOP**. The §7 touch does not apply (see the verdict). The active state is **GO-05AO_AC2**.

## 7. Diagnosis and recommendation

**The cleanup is what creates the creases.** On the real AR1r deflate-only state, the model shows the largest new dihedral at the transition band rising with Smooth events:

| Smooth events | Largest new dihedral | New SI / flips |
|---|---|---|
| 25 | 36° | 0 |
| 50 | 38° | 0 |
| 100 | 51° | 0 |
| 150 | 55° | 0 |
| 175 | 56° (real ≈ 59°) | 0 |

- The transient self-intersections in the deflate-only state are already gone after 10 events.
- Buttock depth barely depends on the count. Model at 25 events vs 175 events: −2.0/−2.6 mm vs −3.0/−4.7 mm.
- So about 150 Laplacian events mostly shrink the 0.95–1.0 transition band against fixed neighbours, which is what folds it.

**Recommended next route (needs author authority):**
1. Keep the 05AR core/ring split, the distance-driven ring ramp, pinned seams and the 50 mm Lipschitz feather. These solved the tail-root plateau and the seam failures.
2. Run the cleanup at **about 25–40 Smooth events**, or one Surface Smooth pass (shape-preserving), instead of about 150.
3. Add a predictor gate on **new edge-dihedral increase**, for example nothing above about 20°, since the 60° fold test missed these visible creases.
4. Optionally end the front edge of the field on the front thigh with a wider (≥ 80 mm) ramp.

## 8. Files (PC: `…\Gorrund-Neutral-C\05AR\`)

| File | sha256 | Status |
|---|---|---|
| GO-05AR_AR1_prep.blend | cbc45c8a…4c63 | AO2 + AR1 mask |
| GO-05AR_AR1_deflate / GO-05AR_AR1.blend | d17621bd… / 6979eed3… | rejected (seams) |
| GO-05AR_AR1r_prep.blend | 77144b99…6b1e | AO2 + AR1r mask |
| GO-05AR_AR1r_deflate / GO-05AR_AR1r.blend | fec9c973… / bba06880… | rejected (creases), evidence only |

Full hashes are in `checks/file_hashes.txt`. Scripts are in `tools/rac/w1/rmot05ar_drivers/`.

**Blender housekeeping:**
- Blender was closed at the end.
- After a computer-use permission timeout, one stray empty Blender instance was briefly launched. It was closed straight away, unchanged.
- Tyler's File Explorer window was left as it was.

## 9. State

Gorrund UNACCEPTED; Grask E3 FROZEN; RM-OT-05 OPEN; Stage C BLOCKED. No LOW, blind final acceptance or scaffold. No D4, UE5, production rigging or creator implementation.
