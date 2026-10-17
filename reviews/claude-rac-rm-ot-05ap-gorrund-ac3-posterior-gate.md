# RAC RM-OT-05AP — Gorrund AC3 posterior: return gate

**Order:** `reviews/chatgpt-rac-rm-ot-05ap-gorrund-ac3-posterior-order.md` (4acb85a)
**Source:** `GO-05AO_AC2.blend` (sha `ba129999…f6f3`, verified).
**Executor:** Claude. All work was cloud diagnostics. **No real AC3 checkpoint was authored**, because the predict-before-author rule (§6) and the simulations showed that no authorised step can pass the gate.

## Verdict

**05AP AC3 NOT CREDIBLE / STOP — author ruling required**

- The active composition stays **`GO-05AO_AC2`** (unchanged).
- Nothing was written to the PC this order, and Blender was not opened.
- No AC3 files exist.

## 1. What was tried (simulation only, using the calibrated Smooth model)

The model is the 05AN UI calibration: 1 mouse event = 1 Laplacian iteration, per-vertex correlation 0.991 against the real filter.

**Posterior masks by vertex ID** (`tools/rac/w1/rmot05ap_drivers/glutemask.py`; `views/ap_masks.jpg`):
- **Sculptable:** the 05AI glute region, optionally plus a posterior upper-thigh continuity band (thigh-dominant vertices behind the thigh axis, z > 80–85 cm).
- **Excluded:** every 05AF protected set (tail, tail junction, genital, perineal, …), which stays hard at 1.0.
- **Feather:** a diffusion ramp from the region boundary inward, k = 60 / 150.

**Metrics** (`apmetrics.py`) were tracked against GO-05AO_AC2:
- buttock posterior-most point, lateral to the tail root;
- pelvis width at z 98–112 cm;
- hip-centre proxy (centroid of the thigh/trunk seam ring);
- upper posterior thigh mean radius;
- flips.

| Variant | Events | Hip-centre proxy drift (L / R) | Upper-thigh radius | Pelvis width | Flips |
|---|---|---|---|---|---|
| glute + thigh band, k = 60 | 100 | **0.57 / 0.57 mm** | −0.24 / +0.06 % | 0.00 % | 5 |
| same | 200 | **0.69 / 0.63** | −0.38 / +0.11 % | 0.00 % | 7 |
| same | 350 | **0.72 / 0.58** | −0.48 / +0.16 % | 0.00 % | 9 |
| same | 1 000 | **0.71 / 0.45** | −0.57 / +0.24 % | 0.00 % | 12 |
| glute + band z > 80, k = 150 | 350 | **0.75 / 0.53** | −0.94 / −0.19 % | 0.00 % | 3 |
| glute only, k = 150 | 350 | 0.00 / 0.00 | 0 / 0 | 0.00 % | 4 |
| glute only, k = 150 | 700 | 0.00 / 0.00 | 0 / 0 | 0.00 % | 7 |

The flips would be repairable within the 40-neighbourhood budget. They were not repaired, because the blockers below come first.

## 2. Why AC3 cannot pass within this order

1. **Hip-centre limit vs the glute fold.** The lower glute fold *is* the posterior thigh/trunk seam. Any variant that softens the fold (the posterior thigh band) moves the posterior half of that seam ring and pushes the hip-centre proxy to **0.45–0.75 mm**, over the 0.5 mm hard limit. The glute-only variants keep the hip at 0.000 mm but leave the fold untouched.
2. **Hard boundary shelves.** In every glute-only and band variant, back and 3/4 views (`views/apv3_body_B.jpg`, `views/applan_body_B.jpg`) show a **visible patch outline**:
   - a horizontal shelf under the buttocks;
   - vertical edges beside the tail root and at the lateral hip.

   This happens because the region borders are fixed protected anatomy (pelvis core, tail junction, thigh). Smoothing pulls the interior away from those fixed borders and creates a ridge. §10 forbids "new ridge, dent, hard mask line". Wider feathering inside the small glute region cannot remove it without also cancelling the effect.
3. **Projection is barely reduced.** Smooth / Surface Smooth relax relief but cannot remove a convex volume bounded by fixed tissue. Even 1 000 iterations change the buttock's posterior-most point by only about 1 mm, and the profile (`views/applan_body_P.jpg`) still reads round and projected. Only the lower undercut softens.
4. **What would work needs authority.** A masked **deflate** (Mesh Filter Inflate with negative drag) of 8–15 mm plus Smooth 150 visibly flattens the profile toward the target (`views/apfeas_body_*.jpg`). It keeps the hip proxy at 0.16–0.52 mm, pelvis width at 0.00 % and upper-thigh radius above −0.35 %. Inflate/deflate is **not in the §7 allowed list**, and the boundary-shelf issue would remain without a broader feathered region.

## 3. Recommendation for the next order

- **A. Broader posterior region.** Define the AC3 region as glute + lateral hip soft tissue + upper posterior thigh (to roughly mid-thigh), with a **wide** feather. That lets the boundary sit on low-curvature tissue instead of at the fold and tail root. Keep the tail root/junction, genital and perineal sets at exactly 1.0, with their own feather ring outside the protected set.
- **B. Hip-centre measurement.** Redefine the hip-centre check as a skeletal/rig landmark (for example the thigh bone head or the rig's hip pivot) rather than the surface seam ring, or set a separate surface-seam tolerance (about 1.0 mm). Softening the glute fold necessarily moves the posterior seam surface.
- **C. Deflate authority.** Authorise one restrained masked **Inflate-negative (deflate)** step, about 8–12 mm at belly centre, followed by Smooth, with predictor and gates as in 05AO. This is the only filter route that reduces projection.
- **D. Fallback.** Alternatively, accept AC2 and treat the posterior as out of scope for this pass. Tyler can judge the AC2 glutes in the final Q1/Q2 review.

## 4. Evidence

| File | Contents |
|---|---|
| `views/ap_masks.jpg` | the three posterior mask variants (back view) |
| `views/applan_body_{B,P,34}.jpg` | AO2 vs glute + thigh band Smooth 100 / 200 / 350 |
| `views/apv3_body_{B,P,34}.jpg` | AO2 vs band-350 vs glute-only 350 / 700 (boundary shelves visible) |
| `views/apfeas_body_{B,P,34}.jpg` | AO2 vs Smooth 350 (authorised) vs deflate 8 / 15 mm + Smooth 150 (needs authority) |
| scripts | `tools/rac/w1/rmot05ap_drivers/glutemask.py`, `apmetrics.py` (05AN predictor/model reused) |

## State

**Gorrund UNACCEPTED; Grask E3 FROZEN; RM-OT-05 OPEN; Stage C BLOCKED.**
- **Active:** GO-05AO_AC2 (AC2 PASS).
- **AC3:** not authored.

No LOW, no blind final acceptance, no scaffold, no D4/UE5/rigging/creator work.
