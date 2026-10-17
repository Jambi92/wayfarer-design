# RAC RM-OT-05AQ — AC3 posterior via broad feather + restrained deflate

**Authority:** Tyler-authorized autonomous continuation after RM-OT-05AP.
**Date:** 2026-10-17.
**Repository:** `Jambi92/wayfarer-design`, `main`.
**Parent gate:** `reviews/claude-rac-rm-ot-05ap-gorrund-ac3-posterior-gate.md` (10dc9a5).

## 1. Author ruling

05AP correctly stopped before authoring because Smooth / Surface Smooth alone cannot reduce the posterior projection within the prior mask and metric contract.

The 05AP feasibility renders show:

- **8 mm masked deflate + Smooth 150** gives the preferred direction;
- **15 mm deflate + Smooth 150** is visibly flatter and is not the starting target;
- the 8 mm version reduces heroic buttock projection while retaining substantial natural volume.

Therefore authorize a new AC3 route with:
1. a broader posterior soft-tissue region;
2. a rig/skeletal hip landmark instead of the moving surface seam proxy;
3. one restrained masked negative Inflate / deflate step;
4. Smooth cleanup afterward;
5. the same predictive and zero-defect gates used throughout 05AL–05AO.

## 2. Advancement source

Advance only from the frozen AC2 checkpoint:

`GO-05AO_AC2.blend`
SHA-256:
`ba129999cfe71c1ab7afc2f11c1b911bd1e85fc06f301e1bad9a483fcba4f6f3`

Review GLB:
`GO-05AO_AC2.glb`
SHA-256:
`1f60fb33fa0c75c9d0f9aa0c1315143005473fd5c72ada67ad922782240de434`

No 05AP geometry was authored, so there is no 05AP checkpoint to advance.

## 3. AC3 target

Reduce the remaining heroic posterior read while preserving a broad, substantial Gorrund pelvis.

Required final read:

**large-frame Gorrund + ordinary untrained posterior soft tissue**

Reduce:
- round bodybuilder buttock projection;
- high rounded glute shelf;
- lower-glute undercut;
- hard glute/posterior-thigh separation.

Preserve:
- natural buttock volume;
- broad pelvis;
- upper posterior-thigh mass;
- sacral structure;
- tail-root identity;
- stance and leg lengths.

Do not produce:
- flat buttocks;
- deflated/sagging appearance;
- narrow pelvis;
- tucked pelvis;
- pinched tail root;
- obvious mask outline.

## 4. Broader posterior region

The 05AP glute-only region was too small and created boundary shelves.

Build a broader vertex-ID posterior region including:
- glute soft tissue;
- lateral hip soft tissue outside the protected pelvis core;
- upper posterior thigh down to approximately mid-thigh, enough to place the lower feather boundary on low-curvature tissue;
- a generous lateral feather zone.

### Hard-protected cores
Remain exactly 1.0:
- tail root;
- tail junction;
- free tail;
- genital;
- perineal protected fold;
- pelvis/sacral skeletal core;
- hip joint core;
- passed torso;
- arms;
- knees and lower legs;
- hands/feet.

### Tail protection feather
The tail root/junction itself stays hard 1.0.
Create a broad feather ring **outside** the protected tail set so the active posterior region approaches it gradually rather than ending on a hard vertical edge.

### Lower boundary
Place the posterior-thigh mask transition far enough down the thigh that it does not coincide with the glute fold.

No hard mask edge through:
- buttock belly;
- glute fold;
- tail-side soft tissue;
- upper hamstring belly.

## 5. Hip-centre metric ruling

The 05AP posterior thigh/trunk surface seam proxy is retired as the hard hip-centre gate for AC3.

Reason:
the glute fold and posterior seam surface must move slightly to soften the fold; measuring that surface ring as a skeletal hip centre falsely treats valid soft-tissue motion as joint drift.

Use instead:
- the rig thigh-bone head / hip pivot if available; or
- a stable rig-weight-derived skeletal hip landmark centered on the actual joint.

Required skeletal hip drift:
- target < 0.25 mm;
- hard ceiling **0.5 mm**.

Also continue to report the old surface-seam proxy as a diagnostic only, not a pass/fail joint gate.

## 6. Predictive gate

Before every real authored step:
1. simulate the proposed deflate / Smooth sequence as closely as possible;
2. flag:
   - flips;
   - >60° cumulative normal rotation;
   - new local inversions;
   - adjacent >60° folds;
   - new self-intersections;
3. repair only discrete predicted neighborhoods using the proven bounded local method.

Repair authority:
- maximum 50 neighborhoods total;
- max 3 repair-analysis cycles per proposed authored stage;
- <= 0.5 mm vertex movement;
- <= 0.5 mm patch surface deviation;
- near-coplanar edge rotations only;
- 0.000 mm outside repair union.

No generalized remeshing.

## 7. Deflate authority

Authorize Blender Mesh Filter **Inflate with negative drag / deflate** through the normal UI.

### AQ1 target
Calibrate for approximately **8 mm deflation at the glute-belly centre**.

The exact UI drag is to be chosen from simulation/calibration.

Do not treat 8 mm as a requirement at every vertex.

The effect should be strongest at the buttock belly and fall off through the broad feathered mask.

### Hard ceiling for AQ1
No posterior soft-tissue vertex may move more than:
**12 mm** from GO-05AO_AC2
during the deflate stage before smoothing.

### Not authorized initially
Do not jump to 15 mm.

If 8 mm is visually insufficient but technically clean, see §11.

## 8. Smooth cleanup after deflate

After the real AQ1 deflate:
- apply one restrained Smooth or Surface Smooth pass, approximately equivalent to the successful **Smooth 150** feasibility direction;
- exact count calibrated by predictor/simulation;
- goal is to remove lower-fold hardness and boundary transitions, not further flatten the buttocks dramatically.

No broad brush sculpting.

## 9. Shape preservation metrics

Track against GO-05AO_AC2:

### Pelvis core
- bony/core pelvis width change <= **0.5%**
- skeletal hip drift <= **0.5 mm**

### Upper posterior thigh
- mean-radius loss <= **3.0%**

### Glute projection
Report:
- left/right posterior-most buttock point, lateral to tail root;
- reduction in mm.

No fixed minimum reduction is required; visual gate governs.

### Tail / genital / perineal
- tail root = 0.000 mm
- tail junction = 0.000 mm
- free tail = 0.000 mm
- genital = 0.000 mm
- perineal protected fold = 0.000 mm

### Torso / finished limbs
- torso = 0.000 mm
- arms = 0.000 mm
- lower legs outside posterior continuity band = 0.000 mm

## 10. Technical gate

After AQ1 deflate + cleanup:

- 0 opened seams;
- 0 self-intersections;
- 0 flipped faces;
- 0 degenerates;
- 1 position-welded component;
- 0 boundary / 0 non-manifold;
- protected regions 0.000 mm;
- stature / bbox unchanged;
- pelvis width within 0.5%;
- skeletal hip drift <= 0.5 mm;
- posterior thigh radius loss <= 3%;
- no visible mask shelf;
- no tail-root pinching;
- no buttock dent or melted patch.

If the real step fails:
- revert;
- one predictive-repair-and-rerun of that exact stage is allowed.
If it fails again, STOP.

## 11. Optional AQ2 only if 8 mm is insufficient

If AQ1 is technically clean and clearly improved but still visibly too heroic:

Authorize **one** additional restrained deflate stage.

Cumulative target:
- do not exceed approximately **12 mm belly-centre deflation** without stopping for Tyler review;
- cumulative max posterior soft-tissue displacement <= **18 mm**.

Then one restrained smoothing cleanup may be used.

Do not approach the 15 mm feasibility state automatically.

If the visual target still is not met within AQ2:
**05AQ AC3 DEFLATE ROUTE NOT CREDIBLE / STOP**

## 12. Visual gate

Compare:
- GO-05AO_AC2;
- 05AP Smooth-only simulations;
- 05AP 8 mm and 15 mm feasibility renders;
- real 05AQ result.

Required:
- profile projection materially reduced from AO2;
- back view no longer reads as two highly rounded bodybuilder glutes;
- buttocks remain substantial and natural;
- lower glute fold softer;
- lateral hip transition continuous;
- no patch outline;
- no tail-side vertical shelf;
- pelvis remains broad;
- posterior thigh remains robust;
- no flat / deflated appearance.

The preferred target should visually stay closer to the **05AP 8 mm feasibility** than the 15 mm version.

## 13. Output

If PASS, freeze:

`GO-05AQ_AC3.blend`
`GO-05AQ_AC3.glb`

Record exact hashes.

## 14. Decision

### PASS
Return:

**05AQ AC3 PASS / READY FOR FINAL Q1-Q2 + TYLER VISUAL REVIEW**

Then STOP.

Do not alter:
- head share;
- tail root;
- heel lift;
- final foot size;
- genus handles.

### FAIL
Return:

**05AQ AC3 DEFLATE ROUTE NOT CREDIBLE / STOP**

Revert active composition state to `GO-05AO_AC2`.

## 15. Evidence

Return:
- posterior mask visualization/readback;
- skeletal hip landmark definition;
- old seam proxy diagnostic;
- predictor/repair logs;
- exact Inflate-negative UI settings / drag calibration;
- exact smoothing settings / event count;
- projection change L/R;
- pelvis width;
- skeletal hip drift;
- posterior-thigh radius;
- geometry gates;
- identical-camera:
  - whole F/P/B/3/4;
  - body-only F/P/B/3/4;
  - close posterior B/P/3/4;
  - AO2 vs AQ1/AQ2 comparison;
  - comparison to 05AP 8 mm feasibility target.

## 16. State

Until Tyler visually accepts final composition:
- Gorrund UNACCEPTED;
- Grask E3 FROZEN;
- RM-OT-05 OPEN;
- Stage C BLOCKED;
- no LOW / blind final acceptance / scaffold;
- no D4 / UE5 / production rigging / creator implementation.

## 17. Return

Commit:

`reviews/claude-rac-rm-ot-05aq-gorrund-ac3-deflate-gate.md`

Evidence:

`reviews/rac-rmot05aq-evidence/`
