# Direct-sculpt brief (05S §3–4 scope, unchanged by 05T)

**Fix:**
- **Posterior:** remove the crinkled / notched strip along the posterior axillary fold edge (θ −86…−106°, s 2–8 cm in the 05Q arm frame). Restore a credible arm-to-posterior-axillary-fold crease.
  - Keep the adjacent deltoid / triceps relief.
  - Keep a deliberate, tapered garment termination toward θ −136°: no lip, no cut end.
- **Anterior:** the arm-to-pectoral transition is plausible. Refine it only if necessary.

**Labelling:** all new skin is **INFERRED**. Do not invent recovered high-frequency anatomy, and do not project clothing detail.

**Out of scope (rejected by the check or by author review):**
- full-ring removal, arm–trunk separation, a shoulder or axilla rebuild;
- a second garment region;
- pose, scale or limb-length changes;
- global smoothing or remesh;
- any change outside the purple interface.

**Pre-registered gates** (`reviews/rac-rmot05s-evidence/plan/PLAN.md`), plus the 05T protection checks P1 / P2 run by `t_reintegrate`:

| Gate | Requirement |
|---|---|
| V1 | Outside anatomy unchanged |
| V2 | Boundary / manifold correct |
| V3 | No intersections |
| V4 | Minimum angle ≥ 10°, edges 0.25–2.5 cm |
| V5 | Seam ≤ 35° on ≥ 95 % of stitch edges |
| V6c | Ledge removed / taper / no folds |

**Context:** S3's own scores, the starting point, are in `reviews/rac-rmot05s-evidence/repair/S3/GO-05S-S3_verify.json`.
