# RAC RM-OT-05AS — Gorrund AC3 final short-cleanup rerun: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05as-gorrund-ac3-short-cleanup-order.md` (10f6030)
**Source:** `GO-05AO_AC2` (AO2 vertex data, sha-verified blend from 05AO).
**Executor:** Claude. All work was cloud prediction. **No AS1 was authored**: under §6 and §8, the predictor showed that no short-cleanup plan can meet the visual gate (§12).

## Verdict

**05AS AC3 FINAL CLEANUP NOT CREDIBLE / STOP** (stopped before authoring)

- The active composition stays **`GO-05AO_AC2`** (unchanged).
- Nothing was written to the PC and Blender was not opened.

The short-cleanup plan **does pass** the new strict gates:
- 0 SI, 0 flips, 0 collapse;
- no new edge-dihedral increase over 20°;
- no new edge over 35°;
- no crease chains;
- tail core 0.000 mm;
- continuity ring ≤ 2.0 mm;
- pelvis 0.0%, hip core 0.000 mm, thigh ≥ −1.9%.

It **fails** the visual requirement to "keep the improved, natural posterior volume" (§12). Predicted with the calibrated models, the buttocks stay round and heroic with a defined lower-glute undercut, much closer to AO2 than to AR1r. See `views/evs_body_B.jpg`, `evs_body_P.jpg` and `plan_B.jpg`.

**Why:** most of AQ1r and AR1r's visible softening came from the long (~150-event) Laplacian Smooth, not from the ~8 mm deflate. That same long smoothing is what creates the lateral folds. A short cleanup removes the folds and the softening together.

## 1. Refined mask (§3–§4) — `asmask.py`, `refine_as.py`

**Reused unchanged from 05AR:**
- the immutable tail core (free tail + junction ≤ 8 mm from the interface);
- the continuity ring and its distance ramp (1.0 to 22 mm, then smoothstep over 60 mm);
- duplicate-position seams pinned to 1.0.

**Field:** the 05AR field, with the lateral hip and front-lateral thigh transitions widened:
- variable graph-Lipschitz feather: **80 mm** on every edge touching the thigh or lateral-hip zone (|x| > 14 cm), 50 mm elsewhere;
- a C1 relaxation of the mask, so the ramp meets 1.0 without a slope kink (hard vertices held at 1.0);
- mask-only protective bumps at predicted dihedral spikes (3 refinement cycles).

**First widening attempt (trunk cut moved forward to y > −52 cm, thigh cut to the front):** it shrank pelvis width by **2.5–2.8%** (limit 0.5%) because the lateral-most hip deflated (`checks/cleanup_table_first_widened_mask_pelvis_fail.json`). The final field therefore keeps the lateral-most hip line hard and runs the 80 mm feather inward from it.

**Design check (`checks/mask_design_check.json`; mask is design-only, not written to a .blend):**

| Set | Min mask |
|---|---|
| Core | 1.0 |
| Seams | 1.0 |
| Ring | ≥ 0.99 |
| Head, tail, genital, perineal, hands, feet, torso | 1.0 |

Visualisation: `views/as_mask.jpg`.

## 2. Cleanup table (§6–§7) — `checks/cleanup_table_10_to_40.json`

**Model:**
- the exact UI Inflate (strength 0.020, −100 px = −7.92 mm × (1 − M));
- then N masked Laplacian iterations, the calibrated Smooth Mesh Filter model.

**Dihedral gate (`dihed.py`):**
- shared edges are compared with AO2;
- the transition field is every edge touching a vertex with 0.05 < M < 1;
- a chain is any connected set of edges with an increase over 10° that spans more than 40 mm.

| Smooth events | New SI | Flips | Collapse | Max new dihedral increase | Edges > 20° | New edges > 35° | Chains | Ring max | Pelvis | Hip core | Thigh L/R | Buttock depth L/R |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 (deflate only) | 0 | 8 | 0 | 145° | 178 | 112 | 0 | 0.54 mm | 0.0% | 0 | −1.66/−1.37% | −1.8/−1.6 mm |
| 3 | 0 | 0 | 0 | 53° | 7 | 6 | 0 | 0.62 | 0.0% | 0 | −1.67/−1.37 | −1.8/−1.7 |
| 5 | 0 | 0 | 0 | 28° | 5 | 3 | 0 | 0.72 | 0.0% | 0 | −1.67/−1.38 | −1.8/−1.7 |
| **8** | 0 | 0 | 0 | **18.6°** | **0** | **0** | 0 | 0.97 | 0.0% | 0 | −1.68/−1.39 | −1.9/−1.7 |
| 10 | 0 | 0 | 0 | 17.4° | 0 | 0 | 0 | 1.11 | 0.0% | 0 | −1.69/−1.40 | −1.9/−1.7 |
| 15 | 0 | 0 | 0 | 16.4° | 0 | 0 | 0 | 1.42 | 0.0% | 0 | −1.71/−1.41 | −1.9/−1.8 |
| 20 | 0 | 0 | 0 | 17.0° | 0 | 0 | 0 | 1.66 | 0.0% | 0 | −1.73/−1.43 | −2.0/−1.8 |
| 25 | 0 | 0 | 0 | 17.9° | 0 | 0 | 0 | 1.84 | 0.0% | 0 | −1.74/−1.45 | −2.0/−1.9 |
| 30 | 0 | 0 | 0 | 19.0° | 0 | 0 | 0 | 1.97 | 0.0% | 0 | −1.76/−1.47 | −2.1/−1.9 |
| 40 | 0 | 0 | 0 | 21.1° | 3 | 1 | 0 | 2.15 | 0.0% | 0 | −1.80/−1.51 | −2.1/−2.1 |

**Technical selection:** the lowest passing count is **8 events**. The whole 8–30 range passes, which allows for the observed real/model factor of about 1.2–1.4×.

**Long-cleanup diagnostic (`checks/cleanup_table_long_diagnostic.json`):** with this mask, 60, 100 and 150 events fail again.

| Events | Max increase | Edges > 20° | Ring |
|---|---|---|---|
| 60 | 26.6° | 10 | 2.39 mm |
| 100 | 38° | 30 | 3.29 mm |
| 150 | 55° | 65 | 3.99 mm |

**Surface Smooth alternative (`checks/surface_smooth_test.txt`; 05AL replica, f = 0.78, 1–10 steps):**
- it does not remove the deflate-stage folds: max increase 97–120°, 18–50 edges over 20°, 1 flip;
- buttock depth is unchanged.

It fails the gate.

## 3. Why the plan cannot meet §12

**Contribution to mean posterior buttock movement (z 92–108):**

| Mask | Deflate only | + 150 Smooth |
|---|---|---|
| AQ1r (v4) | 4.6 mm | 7.3 mm |
| AR1r (ar5) | 4.5 mm | 7.3 mm |
| AS (this order) | 2.8 mm | 5.1 mm |

- About 40% of the AQ1r/AR1r posterior change came from the long Laplacian shrink.
- The wider 80 mm transitions and fold protection also leave fewer fully sculptable belly vertices: 2 775 with M < 0.1, against about 10 000 in 05AR.
- With 8–30 events, the predicted renders (`views/evs_body_B.jpg`, `evs_body_P.jpg`, `plan_B.jpg`, `plan_P.jpg`) show:
  - buttocks still round and projecting, close to AO2;
  - a crisper lower-glute undercut (the deflate deepens the fold, and a short cleanup cannot soften it);
  - **but:** the front and 3/4 stripe is gone (`plan_34.jpg`) and the tail root blends cleanly.

That fails §12: "keep the improved, natural posterior volume", "no bodybuilder projection" and "lower glute fold soft and continuous". Authoring AS1 would spend the final attempt on a result the calibrated predictor already shows as visually failing.

## 4. What this establishes for the author

On this mesh, with these rules, the AC3 target sets up a direct conflict:

| Approach | Visual softening (volume, soft fold) | Lateral creases |
|---|---|---|
| Long Laplacian Smooth (~150 events) | yes | yes (>50°) |
| Short cleanup (≤ 30 events) | no | none |
| Deflate strength | capped at ~8 mm by the orders | — |

Options that would break the conflict (author's call):
1. **Two-mask authoring.** Deflate plus a long Smooth with a *belly-only* mask (the transition band hard), then a separate short Smooth with the wide-feather mask for the boundary. This needs a mask swap between UI steps. A cloud-written second mask attribute is not usable from the UI, so it would need either a UI mask rebuild or authority to load a second prepared file state.
2. **Allow a somewhat stronger deflate** (for example about 10–11 mm, under the earlier 12 mm ceiling) with the short cleanup. At 8 mm the deflate is technically clean after 8+ cleanup events; a stronger deflate has not been predicted yet and would need its own table.
3. **Accept GO-05AO_AC2 posterior as-is** for Tyler's Q1/Q2 visual review, treating AC3 as optional.

## 5. Files

No PC files were written. Scripts are in `tools/rac/w1/rmot05as_drivers/` (`asmask.py`, `dihed.py`, `table.py`, `refine_as.py`). The 05AR tail-core/ring and seam tools were reused.

## 6. State

Gorrund UNACCEPTED; Grask E3 FROZEN; RM-OT-05 OPEN; Stage C BLOCKED. No LOW, blind final acceptance or scaffold. No D4, UE5, production rigging or creator implementation.
