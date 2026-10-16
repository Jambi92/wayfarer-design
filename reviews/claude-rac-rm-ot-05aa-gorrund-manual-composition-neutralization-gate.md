# RAC RM-OT-05AA — Gorrund manual composition-neutralization: AA0 readiness gate

**Order:** `reviews/chatgpt-rac-rm-ot-05aa-gorrund-manual-composition-neutralization-order.md` (fbc8cd2).
**Date:** 2026-10-15.
**Evidence:** `reviews/rac-rmot05aa-evidence/aa0/`.

## Outcome

**05AA BLOCKED — DONOR MACRO FRAME INCOMPATIBLE / HUMAN SCULPT OR NEW NON-RODIN SOURCE REQUIRED**

Donor C's soft tissue is the visible Q1/Q2 failure, but its **segment proportions also differ from the accepted W1 ARM by amounts only bone-length / joint-position reconstruction could close**:

- **Relative arm reach.** C's lowest fingertip is at **36.5 %** of height. The W1 ARM's is at **44.3 %**, a difference of 7.8 points (≈ 15 cm at C's 190 raw cm; ≈ 18 cm at the ARM's 229 cm stature). C reaches lower even than **Grask E3 (37.0 %)**. Gorrund V1 §222 and §299 say Grask have the greater relative arm length and that increased relative reach is not a Gorrund trait. C's arms would need shortening at the humerus and forearm, which means moving the elbow and wrist.
- **Leg length / crotch height.** C's crotch is at **44.5 %** of height, against 48.5 % for the ARM, 48.3 % for Skarn and 48.8 % for Marchfolk. Closing this means lengthening the femur and tibia, or moving the hip joint.
- **Lower-leg envelope.** Knee width is 9.2 % and calf width 11.1 % of height in C, against 6.8 % and 6.2 % in the ARM. This is partly soft tissue. The calf ratio, however, is close to double, and the knee and ankle envelopes are also larger.

Per §4, **AA1 was not started.** C was not warped into place. Nothing was sculpted, and no checkpoint was spent. The baseline working scene exists, unmodified, for whoever takes the next route.

Gorrund **UNACCEPTED**; Grask E3 **FROZEN**; RM-OT-05 **OPEN**; Stage C **BLOCKED**.

## 1. AA0 steps 1–3: pinned baseline

| Item | Value |
|---|---|
| Donor | `Gorrund_Neutral.glb`, SHA-256 `513bc9e2c5c4ba1da0a5a33661f230181bf18a24c50e0af0d49acdf5521dccf6`. Identical before and after; it is never written. |
| Baseline scene | `GO-05AA_C_baseline.blend`, SHA-256 `c17ac3c2b213cf877e952fe2089eb0545d661b4ffa14ca197fa42ea954df7bac`, 35,479,548 bytes, compressed. Object `GO-05AA_C_working`: 556,391 vertices, 1,000,000 faces, with the donor hash stored as a custom property (`aa0/baseline_blend.json`). |
| How it was made | Headless import, then save, using the Blender 5.0.1 Python module (`tools/rac/w1/rmot05aa_drivers/aa_baseline_blend.py`). This is an import only; no geometry operation was applied. **A Blender older than 5.0 may not open this file.** In that case, re-import the GLB on the desktop. |
| Stored at | `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Neutral-C\05AA\`, in 2 parts plus `REJOIN.txt` |

## 2. AA0 step 4: accepted W1 reference

The accepted W1 ARM is **`reviews/rac-w1i-evidence/geometry/GO_r6.npz`**: the retained W1i point, whose geometry `rac-w1j-evidence/geometry_identity.json` shows is identical to W1j. Its stature input is 229 cm and its surface height is 230.9 raw. It was used read-only as the macro guide, never as a surface target.

Controls, all frozen:
- Marchfolk male ref `rac-w1c-evidence/geometry/MF-M-R_r6.npz`;
- Skarn ref `SK_r6.npz`;
- Grask E3 `reference-assets/r6/GR5DE3_r6.npz`.

## 3. AA0 steps 5–6: macro comparison (`aa0/macro_frame.json`)

Method:
- read-only horizontal sections, centred on each body's trunk midline;
- values are % of each mesh's own top-to-sole height, so the comparison does not depend on stature;
- for C, trunk loops behind the body (the tail) and hand loops are excluded;
- `aa_macro.py` is additive tooling.

| % of height | W1 ARM | **C** | Skarn ref | Marchfolk M ref | Grask E3 |
|---|---|---|---|---|---|
| Crotch height | 48.5 | **44.5** | 48.3 | 48.8 | 52.3 |
| Lowest fingertip | 44.3 | **36.5** | 41.0 | 39.5 | 37.0 |
| Max breadth, 74–86 % (shoulders and arms) | 28.2 | **35.2** | 28.7 | 27.8 | 24.0 |
| Trunk depth, 72 / 66 / 60 / 53 % | 16.0 / 15.4 / 13.4 / 15.1 | **20.3 / 19.3 / 17.1 / 18.8** | 14.2 / 12.8 / 11.3 / 12.9 | 13.0 / 11.6 / 11.4 / 13.1 | 16.0 / 11.5 / 10.9 / 9.2 |
| Trunk width, 66 / 60 / 53 % | 17.5 / 18.0 / 21.2 | **22.9 / 20.3 / 22.1** | 15.7 / 16.0 / 18.4 | 15.8 / 16.2 / 18.8 | 15.5 / 15.7 / 17.4 |
| Knee width × depth, 28 % | 6.8 × 7.8 | **9.2 × 9.8** | 7.2 × 8.2 | 5.9 × 6.9 | 6.1 × 8.5 |
| Calf width × depth, 20 % | 6.2 × 6.2 | **11.1 × 10.3** | 7.6 × 7.9 | 6.8 × 6.6 | 4.5 × 5.9 |

C's chest width at 72 % is not comparable: C's arms touch the trunk there, so the section merges them.

### Reading by the order's macro items

| Item | Finding | Sculptable as soft tissue? |
|---|---|---|
| Thoracic breadth and depth | C is deeper (20 % against 16 %), mostly from pectoral and abdominal projection | **Yes.** This is the intended AA1 work. |
| Lumbar transition and pelvis | Wider and deeper than the ARM, with love handles and large gluteals | Mostly yes |
| Shoulder-girdle placement | Shoulder-to-arm breadth is 35 % against 28 %: deltoid mass plus arms held close | Partly. The deltoid is soft tissue; the girdle width is uncertain. |
| Major joint scale | Knees are larger. That is acceptable for Gorrund in principle, but sits with the calf excess. | Partly |
| **Limb shares and reach** | **Arm reach is 7.8 points of stature longer than the ARM and longer than Grask. Crotch is 4.0 points lower.** | **No.** This is bone length and joint position. |
| Thigh and calf envelope | Calf width is about 1.8 × the ARM's | Partly soft tissue |
| Stance | Upright, plantigrade, comparable | Yes |

Exhibits:
- `aa0_macro_frame_equal_height.jpg`: whole bodies uniformly scaled to a common displayed height of 1.90 m, for display only. Crotch and fingertip lines are drawn for each body, with the ARM's levels dashed.
- `aa0_headless_matched_height.jpg`: controls, ARM and C body-only.

## 4. AA0 decision

The Q1/Q2 failure is **not primarily superficial**. A soft-tissue-only AA1 would leave a Gorrund whose arms reach farther, relative to stature, than Grask E3, and whose legs are proportionally the shortest of any compared body. That contradicts the accepted ARM's limb relationships and Gorrund V1's reach rule.

Fixing it requires shortening both arms and re-seating the hip and knee. That is the "wholesale bone-length/joint-position reconstruction" that §4 says to stop on. Doing it by hand with Grab or Elastic on a 1-million-face surface would be the warping §4 forbids.

**05AA BLOCKED — DONOR MACRO FRAME INCOMPATIBLE / HUMAN SCULPT OR NEW NON-RODIN SOURCE REQUIRED.**

### Possible next routes (order-level; not started)

1. **Human sculptor.** C's head, hands and feet stay usable as references. A sculptor rebuilds the limb proportions to the W1 ARM.
2. **New non-Rodin source.** An image-to-3D or sculpt route that accepts proportion guidance, for example the W1 ARM silhouette or skeleton as input.
3. **Author ruling** that C's reach and leg ratios are acceptable variation. This is not recommended: it would contradict Gorrund V1 §222 / §299 on the Grask distinction.

### Caveats

- Fingertip height also depends on shoulder height and arm hang. C's arms hang close to vertical, and the ARM's are abducted 8° (cos 8° ≈ 0.99), so the reach gap is not a pose artefact.
- Measurements are section-based, using each mesh's own top-to-sole height, and C's head proportion differs from the ARM's. C's skull share is 11.3 % against 12.6 % for the ARM, which would *reduce* C's reach gap only slightly.

**STOP.** No AA1 checkpoint, no sculpt, no repair, LOW, blind, scaffold, D4, UE5, rigging, creator work or Stage C.
