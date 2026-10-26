# GR_U_REF_RP2_rigprep_landmarks_v001 — readable tables

Generated from `GR_U_REF_RP2_rigprep_landmarks_v001.json` by `tools/rac/rp/grask_rigprep_v001/tables.py`. **Proposal only.** It does not replace the frozen landmark package.

Frames:

- **production cm**: x = subject left, f = forward, u = up; origin = frozen pelvis_root projected to the ground.
- **Blender m**: (x, −f, u)/100.
- **source** = production − (−0.11180, 5.72272, 0).

## 1. Frozen landmark package: provenance audit (74 records)

| provenance class | records |
|---|---|
| fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids) | 18 |
| independently measured surface landmark | 12 |
| copied construction coordinate | 42 |
| rule-based estimate (heuristic offset from the ear root; mislabelled "construction coordinate (copied)" in the frozen package) | 2 |

| id | frozen method | frozen "evidence" field | audited provenance | counts as independent measurement | T-6 drift mm |
|---|---|---|---|---|---|
| spine_01 | prior-seed+surface-fit | independently measured on v003 | fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids) | yes | 0.008 |
| spine_02 | prior-seed+surface-fit | independently measured on v003 | fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids) | yes | 0.013 |
| spine_03 | prior-seed+surface-fit | independently measured on v003 | fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids) | yes | 0.004 |
| pelvis_root | prior-seed+surface-fit | independently measured on v003 | fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids) | yes | 0.012 |
| neck_base | prior-seed+surface-fit | independently measured on v003 | fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids) | yes | 0.014 |
| head_pivot | prior-seed+surface-fit | independently measured on v003 | fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids) | yes | 0.057 |
| crown | surface-fit | independently measured on v003 | independently measured surface landmark | yes | 0.294 |
| hip_l | prior-seed+surface-fit | independently measured on v003 | fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids) | yes | 0.045 |
| knee_l | prior-seed+surface-fit | independently measured on v003 | fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids) | yes | 0.009 |
| ankle_l | prior-seed+surface-fit | independently measured on v003 | fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids) | yes | 0.025 |
| sternoclavicular_l | prior-seed+surface-fit | independently measured on v003 | fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids) | yes | 0.033 |
| glenohumeral_l | prior-seed+surface-fit | independently measured on v003 | fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids) | yes | 0.003 |
| acromion_l | surface-fit | independently measured on v003 | independently measured surface landmark | yes | 0.07 |
| elbow_l | prior-seed+surface-fit | independently measured on v003 | fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids) | yes | 0.005 |
| wrist_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| index_mcp_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| index_tip_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| middle_mcp_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| middle_tip_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| ring_mcp_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| ring_tip_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| pinky_mcp_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| pinky_tip_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| thumb_cmc_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| scapular_inferior_proxy_l | surface-fit | independently measured on v003 | independently measured surface landmark | yes | 0.209 |
| hallux_mtp_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| hallux_tip_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| toe2_mtp_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| toe2_tip_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| toe3_mtp_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| toe3_tip_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| toe4_mtp_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| toe4_tip_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| toe5_mtp_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| toe5_tip_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| eye_l | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| hip_r | prior-seed+surface-fit | independently measured on v003 | fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids) | yes | 0.044 |
| knee_r | prior-seed+surface-fit | independently measured on v003 | fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids) | yes | 0.01 |
| ankle_r | prior-seed+surface-fit | independently measured on v003 | fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids) | yes | 0.034 |
| sternoclavicular_r | prior-seed+surface-fit | independently measured on v003 | fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids) | yes | 0.033 |
| glenohumeral_r | prior-seed+surface-fit | independently measured on v003 | fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids) | yes | 0.008 |
| acromion_r | surface-fit | independently measured on v003 | independently measured surface landmark | yes | 0.042 |
| elbow_r | prior-seed+surface-fit | independently measured on v003 | fitted joint-centre estimate (superseded MPFB/E3 seed shifted by section centroids) | yes | 0.005 |
| wrist_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| index_mcp_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| index_tip_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| middle_mcp_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| middle_tip_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| ring_mcp_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| ring_tip_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| pinky_mcp_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| pinky_tip_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| thumb_cmc_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| scapular_inferior_proxy_r | surface-fit | independently measured on v003 | independently measured surface landmark | yes | 0.209 |
| hallux_mtp_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| hallux_tip_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| toe2_mtp_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| toe2_tip_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| toe3_mtp_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| toe3_tip_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| toe4_mtp_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| toe4_tip_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| toe5_mtp_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| toe5_tip_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| eye_r | manual | construction coordinate (copied) | copied construction coordinate | no | 0.0 |
| chin | surface-fit | independently measured on v003 | independently measured surface landmark | yes | 0.339 |
| ear_tip_l | surface-fit | independently measured on v003 | independently measured surface landmark | yes | 0.364 |
| ear_root_l | surface-fit | independently measured on v003 | independently measured surface landmark | yes | 0.139 |
| jaw_hinge_l | manual | construction coordinate (copied) | rule-based estimate (heuristic offset from the ear root; mislabelled "construction coordinate (copied)" in the frozen package) | no | 0.139 |
| mouth_corner_l | surface-fit | independently measured on v003 | independently measured surface landmark | yes | 0.84 |
| ear_tip_r | surface-fit | independently measured on v003 | independently measured surface landmark | yes | 0.279 |
| ear_root_r | surface-fit | independently measured on v003 | independently measured surface landmark | yes | 0.071 |
| jaw_hinge_r | manual | construction coordinate (copied) | rule-based estimate (heuristic offset from the ear root; mislabelled "construction coordinate (copied)" in the frozen package) | no | 0.071 |
| mouth_corner_r | surface-fit | independently measured on v003 | independently measured surface landmark | yes | 0.79 |

## 2. Proposed joint centres and markers (body, girdle, axial, face)

| id | status | provenance | production cm | Blender m | uncertainty cm | depth in v005 cm | v003 Δ cm | parent | length cm |
|---|---|---|---|---|---|---|---|---|---|
| hip_l | provisional | fitted joint-centre estimate | (12.11, 2.85, 119.03) | (0.1211, -0.0285, 1.1903) | 5.87 | 6.66 | 0.002 | pelvis_root | 13.06 |
| knee_l | provisional | fitted joint-centre estimate | (13.66, 1.01, 71.17) | (0.1366, -0.0101, 0.7117) | 4.64 | 5.85 | 0.002 | hip_l | 47.92 |
| ankle_l | provisional | fitted joint-centre estimate | (15.53, 0.23, 13.50) | (0.1553, -0.0023, 0.1350) | 6.05 | 4.37 | 0.000 | knee_l | 57.70 |
| glenohumeral_l | provisional | fitted joint-centre estimate | (17.85, -1.36, 173.71) | (0.1785, 0.0136, 1.7371) | 5.97 | 6.74 | 0.369 | sternoclavicular_l | 17.47 |
| elbow_l | provisional | fitted joint-centre estimate | (26.06, -2.62, 142.77) | (0.2606, 0.0262, 1.4277) | 5.09 | 3.49 | 0.002 | glenohumeral_l | 32.03 |
| wrist_l | usable (construction) | copied construction coordinate | (30.79, 6.92, 105.00) | (0.3079, -0.0692, 1.0500) | — | 2.82 | 0.000 | elbow_l | 39.24 |
| sternoclavicular_l | provisional | fitted joint-centre estimate | (3.30, 6.41, 179.48) | (0.0330, -0.0641, 1.7948) | 5.10 | 3.68 | 0.445 | spine_03 | 30.32 |
| acromion_l | usable (surface marker) | independently measured surface landmark | (23.84, -4.37, 179.72) | (0.2384, 0.0437, 1.7972) | — | 0.00 | 0.007 | — | — |
| scapular_inferior_proxy_l | provisional (surface proxy only) | independently measured surface landmark | (10.87, -14.52, 166.52) | (0.1087, 0.1452, 1.6652) | — | 0.03 | 0.021 | — | — |
| ear_root_l | usable (surface marker) | independently measured surface landmark | (7.39, 6.30, 200.24) | (0.0739, -0.0630, 2.0024) | — | 0.47 | 0.014 | — | — |
| mouth_corner_l | usable (surface marker) | independently measured surface landmark | (2.63, 19.11, 194.53) | (0.0263, -0.1911, 1.9453) | — | 0.01 | 0.084 | — | — |
| jaw_hinge_l | provisional (no jaw anatomy) | rule-based estimate | (5.89, 8.50, 198.24) | (0.0589, -0.0850, 1.9824) | — | 1.28 | — | head_pivot | 6.28 |
| eye_l | usable (construction) | copied construction coordinate | (3.54, 16.12, 203.85) | (0.0354, -0.1612, 2.0385) | 0.10 | 1.17 | 0.198 | head_pivot | 9.21 |
| hip_r | provisional | fitted joint-centre estimate | (-12.11, 2.76, 119.16) | (-0.1211, -0.0276, 1.1916) | 5.61 | 6.61 | 0.002 | pelvis_root | 13.02 |
| knee_r | provisional | fitted joint-centre estimate | (-13.16, 1.25, 71.20) | (-0.1316, -0.0125, 0.7120) | 6.26 | 5.71 | 0.001 | hip_r | 47.99 |
| ankle_r | provisional | fitted joint-centre estimate | (-15.50, -1.11, 13.75) | (-0.1550, 0.0111, 0.1375) | 6.54 | 4.21 | 0.001 | knee_r | 57.54 |
| glenohumeral_r | provisional | fitted joint-centre estimate | (-19.23, 1.63, 170.82) | (-0.1923, -0.0163, 1.7082) | 9.28 | 5.73 | 0.279 | sternoclavicular_r | 19.61 |
| elbow_r | provisional | fitted joint-centre estimate | (-26.82, -2.88, 142.99) | (-0.2682, 0.0288, 1.4299) | 4.82 | 3.82 | 0.003 | glenohumeral_r | 29.20 |
| wrist_r | usable (construction) | copied construction coordinate | (-31.31, 6.72, 105.00) | (-0.3131, -0.0672, 1.0500) | — | 2.82 | 0.000 | elbow_r | 39.44 |
| sternoclavicular_r | provisional | fitted joint-centre estimate | (-2.32, 6.40, 179.53) | (-0.0232, -0.0640, 1.7953) | 5.08 | 3.86 | 0.195 | spine_03 | 30.19 |
| acromion_r | usable (surface marker) | independently measured surface landmark | (-24.77, -3.93, 178.04) | (-0.2477, 0.0393, 1.7804) | — | 0.00 | 0.004 | — | — |
| scapular_inferior_proxy_r | provisional (surface proxy only) | independently measured surface landmark | (-10.87, -14.25, 166.33) | (-0.1087, 0.1425, 1.6633) | — | 0.04 | 0.021 | — | — |
| ear_root_r | usable (surface marker) | independently measured surface landmark | (-7.57, 6.22, 200.32) | (-0.0757, -0.0622, 2.0032) | — | 0.27 | 0.007 | — | — |
| mouth_corner_r | usable (surface marker) | independently measured surface landmark | (-2.88, 19.18, 194.53) | (-0.0288, -0.1918, 1.9453) | — | 0.01 | 0.079 | — | — |
| jaw_hinge_r | provisional (no jaw anatomy) | rule-based estimate | (-6.07, 8.42, 198.32) | (-0.0607, -0.0842, 1.9832) | — | 1.18 | — | head_pivot | 6.28 |
| eye_r | usable (construction) | copied construction coordinate | (-3.76, 16.12, 203.85) | (-0.0376, -0.1612, 2.0385) | 0.15 | 1.33 | 0.075 | head_pivot | 9.24 |
| pelvis_root | provisional | fitted joint-centre estimate | (0.00, 2.80, 123.93) | (0.0000, -0.0280, 1.2393) | 4.84 | 11.31 | 0.002 | — | — |
| spine_01 | provisional | fitted joint-centre estimate | (-0.00, -0.02, 133.88) | (-0.0000, 0.0002, 1.3388) | 2.74 | 8.30 | 0.000 | pelvis_root | 10.35 |
| spine_02 | provisional | fitted joint-centre estimate | (-0.21, 0.62, 142.42) | (-0.0021, -0.0062, 1.4242) | 1.42 | 7.95 | 0.001 | spine_01 | 8.57 |
| spine_03 | provisional | fitted joint-centre estimate | (-0.47, 0.19, 150.04) | (-0.0047, -0.0019, 1.5004) | 1.52 | 8.35 | 0.000 | spine_02 | 7.64 |
| neck_base | usable (diagnostic) | fitted joint-centre estimate | (0.28, 2.06, 189.14) | (0.0028, -0.0206, 1.8914) | 0.69 | 5.42 | 0.001 | spine_03 | 39.15 |
| head_pivot | provisional | fitted joint-centre estimate | (-0.08, 8.49, 200.18) | (-0.0008, -0.0849, 2.0018) | 1.28 | 7.37 | 0.002 | neck_base | 12.77 |
| crown | usable (surface marker) | independently measured surface landmark | (-0.16, 7.21, 217.97) | (-0.0016, -0.0721, 2.1797) | — | 0.02 | 0.029 | head_pivot | 17.84 |
| chin | usable (surface marker) | independently measured surface landmark | (0.02, 17.70, 189.63) | (0.0002, -0.1770, 1.8963) | — | 0.03 | 0.034 | head_pivot | 14.00 |
| ball_l | usable (construction) | derived from copied construction coordinates | (19.69, 19.52, 1.93) | (0.1969, -0.1952, 0.0192) | — | 1.54 | 0.000 | ankle_l | 22.88 |
| ball_r | usable (construction) | derived from copied construction coordinates | (-19.91, 19.52, 1.93) | (-0.1991, -0.1952, 0.0192) | — | 1.64 | 0.000 | ankle_r | 24.18 |

## 3. Alternatives behind each fitted centre (production cm; distance to the proposal)

| id | alternative | position | distance cm |
|---|---|---|---|
| hip_l | A: thigh axis extended to the level of the inguinal fold (first local minimum of the anterior contour above the crotch) | (11.38, 7.66, 115.75) | 5.87 |
| hip_l | C: frozen v003 package value (MPFB/E3-seeded) | (12.84, -1.96, 122.31) | 5.87 |
| knee_l | A: centroid of the minimum-area section across the knee (perpendicular to the mean thigh/shank axis) | (14.41, -1.12, 67.11) | 4.64 |
| knee_l | B: centroid of the section at the patellar flattening (minimum slope of the anterior contour) | (13.66, 1.00, 75.56) | 4.39 |
| knee_l | C: frozen v003 package value (MPFB/E3-seeded) | (13.23, 1.86, 71.17) | 0.95 |
| ankle_l | A: distal-shank axis at the anterior ankle crease (maximum curvature of the anterior contour) | (15.53, 0.23, 13.50) | 0.00 |
| ankle_l | B: distal-shank axis at the Achilles concavity (most anterior point of the posterior contour above the heel) | (15.58, -0.57, 19.50) | 6.05 |
| ankle_l | C: frozen v003 package value (MPFB/E3-seeded) | (14.87, 1.54, 9.23) | 4.51 |
| glenohumeral_l | A: least-squares sphere on the lateral/superior shoulder cap (faces within 9 cm of the measured acromion, normals lateral or up) | (17.47, -1.36, 173.71) | 0.38 |
| glenohumeral_l | B: least-squares sphere on the lateral deltoid only (faces within 11 cm of the acromion, 1..12 cm below it, normal lateral > 0.7) | (17.85, -0.81, 172.09) | 1.71 |
| glenohumeral_l | C: frozen v003 package value (MPFB/E3-seeded) | (21.34, -4.37, 177.51) | 5.97 |
| elbow_l | A: centroid of the minimum-area section across the elbow | (26.06, -2.62, 142.77) | 0.00 |
| elbow_l | B: centroid of the section at the cubital fossa (most posterior point of the anterior contour) | (26.35, -2.49, 141.30) | 1.51 |
| elbow_l | C: frozen v003 package value (MPFB/E3-seeded) | (25.46, -4.43, 147.50) | 5.09 |
| wrist_l | B (reference only, not an alternative): forearm waist 7.0 cm proximal | (30.75, 4.92, 111.79) | 7.08 |
| sternoclavicular_l | A: anterior surface summit beside the jugular notch (skin point) | (3.58, 11.35, 178.27) | 5.10 |
| sternoclavicular_l | C: frozen v003 package value (MPFB/E3-seeded) | (3.02, 1.46, 180.69) | 5.10 |
| eye_l | A: v003 eyeball-volume centre (construction) | (3.54, 16.12, 203.85) | 0.00 |
| eye_l | B: sphere on the anterior eye surface (r=1.51 cm, rms 1.00 mm) | (3.54, 16.03, 203.80) | 0.10 |
| hip_r | A: thigh axis extended to the level of the inguinal fold (first local minimum of the anterior contour above the crotch) | (-11.49, 7.36, 116.00) | 5.61 |
| hip_r | C: frozen v003 package value (MPFB/E3-seeded) | (-12.73, -1.84, 122.31) | 5.61 |
| knee_r | A: centroid of the minimum-area section across the knee (perpendicular to the mean thigh/shank axis) | (-14.21, -1.51, 65.67) | 6.26 |
| knee_r | B: centroid of the section at the patellar flattening (minimum slope of the anterior contour) | (-13.16, 1.25, 73.63) | 2.44 |
| knee_r | C: frozen v003 package value (MPFB/E3-seeded) | (-12.74, 2.30, 71.20) | 1.12 |
| ankle_r | A: distal-shank axis at the anterior ankle crease (maximum curvature of the anterior contour) | (-15.50, -1.11, 13.75) | 0.00 |
| ankle_r | B: distal-shank axis at the Achilles concavity (most anterior point of the posterior contour above the heel) | (-15.63, -1.81, 20.25) | 6.54 |
| ankle_r | C: frozen v003 package value (MPFB/E3-seeded) | (-14.94, 0.16, 9.29) | 4.67 |
| glenohumeral_r | A: least-squares sphere on the lateral/superior shoulder cap (faces within 9 cm of the measured acromion, normals lateral or up) | (-16.05, 2.10, 170.82) | 3.22 |
| glenohumeral_r | B: least-squares sphere on the lateral deltoid only (faces within 11 cm of the acromion, 1..12 cm below it, normal lateral > 0.7) | (-19.23, 1.63, 170.72) | 0.11 |
| glenohumeral_r | C: frozen v003 package value (MPFB/E3-seeded) | (-22.27, -3.93, 177.60) | 9.28 |
| elbow_r | A: centroid of the minimum-area section across the elbow | (-26.82, -2.88, 142.99) | 0.00 |
| elbow_r | B: centroid of the section at the cubital fossa (most posterior point of the anterior contour) | (-27.11, -2.83, 141.51) | 1.51 |
| elbow_r | C: frozen v003 package value (MPFB/E3-seeded) | (-26.33, -4.24, 147.59) | 4.82 |
| wrist_r | B (reference only, not an alternative): forearm waist 7.0 cm proximal | (-31.31, 5.01, 111.86) | 7.07 |
| sternoclavicular_r | A: anterior surface summit beside the jugular notch (skin point) | (-2.43, 11.35, 178.37) | 5.08 |
| sternoclavicular_r | C: frozen v003 package value (MPFB/E3-seeded) | (-2.21, 1.46, 180.69) | 5.08 |
| eye_r | A: v003 eyeball-volume centre (construction) | (-3.76, 16.12, 203.85) | 0.00 |
| eye_r | B: sphere on the anterior eye surface (r=1.38 cm, rms 0.79 mm) | (-3.78, 16.22, 203.74) | 0.15 |
| pelvis_root | A: midpoint of the proposed hip centres | (-0.00, 2.80, 119.09) | 4.84 |
| pelvis_root | B: torso section centroid at the frozen pelvis-root height | (0.01, 3.57, 123.93) | 0.76 |
| pelvis_root | C: frozen v003 package value (defines the production origin) | (0.00, 0.00, 123.93) | 2.80 |
| spine_01 | A: torso section centroid at the station height | (-0.03, 2.71, 133.88) | 2.74 |
| spine_01 | C: frozen v003 package value (MPFB/E3-seeded) | (0.02, -2.76, 133.88) | 2.74 |
| spine_02 | A: torso section centroid at the station height | (-0.20, 2.04, 142.42) | 1.42 |
| spine_02 | C: frozen v003 package value (MPFB/E3-seeded) | (-0.22, -0.80, 142.42) | 1.42 |
| spine_03 | A: torso section centroid at the station height | (-0.47, 1.71, 150.04) | 1.52 |
| spine_03 | C: frozen v003 package value (MPFB/E3-seeded) | (-0.47, -1.33, 150.04) | 1.52 |
| neck_base | A: torso section centroid at the station height | (0.24, 2.75, 189.14) | 0.69 |
| neck_base | C: frozen v003 package value (MPFB/E3-seeded) | (0.31, 1.37, 189.14) | 0.69 |
| head_pivot | A: neck/head section centroid at the mean ear-root height | (-0.07, 9.77, 200.25) | 1.28 |
| head_pivot | C: frozen v003 package value (MPFB/E3-seeded) | (-0.08, 7.21, 200.10) | 1.28 |

## 4. Local axes (right-handed in Blender; X = flexion axis toward subject-left, Y = toward child, Z = X × Y)

| id | X (Blender) | Y (Blender) | Z (Blender) | det Blender / analysis | flexion sign |
|---|---|---|---|---|---|
| hip_l | (0.999, -0.001, 0.032) | (0.032, 0.038, -0.999) | (-0.000, 0.999, 0.038) | +1 / -1 | negative rotation about local +X (right-hand rule, Blender frame) — hip flexion: knee moves anterior |
| knee_l | (0.999, -0.000, 0.032) | (0.032, 0.013, -0.999) | (0.000, 1.000, 0.013) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — knee flexion: ankle moves posterior |
| ankle_l | (0.983, 0.156, 0.094) | (0.182, -0.843, -0.506) | (-0.000, 0.515, -0.857) | +1 / -1 | negative rotation about local +X (right-hand rule, Blender frame) — ankle dorsiflexion: ball moves up |
| glenohumeral_l | (0.967, -0.010, 0.256) | (0.256, 0.039, -0.966) | (0.000, 0.999, 0.041) | +1 / -1 | negative rotation about local +X (right-hand rule, Blender frame) — shoulder flexion: elbow moves anterior |
| elbow_l | (0.967, -0.191, 0.169) | (0.121, -0.243, -0.962) | (0.225, 0.951, -0.212) | +1 / -1 | negative rotation about local +X (right-hand rule, Blender frame) — elbow flexion: wrist moves anterior |
| wrist_l | (0.308, 0.950, -0.047) | (0.112, -0.086, -0.990) | (-0.945, 0.299, -0.133) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — wrist flexion: hand moves palmar |
| sternoclavicular_l | (0.554, -0.668, 0.497) | (0.833, 0.444, -0.330) | (0.000, 0.597, 0.802) | +1 / -1 | not defined in this proposal (girdle/jaw/eye axes deferred) |
| jaw_hinge_l | (0.906, -0.308, -0.289) | (-0.423, -0.662, -0.619) | (0.000, 0.684, -0.730) | +1 / -1 | not defined in this proposal (girdle/jaw/eye axes deferred) |
| index_mcp_l | (0.318, 0.936, -0.151) | (-0.217, -0.083, -0.973) | (-0.923, 0.342, 0.177) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| index_pip_l | (0.318, 0.936, -0.151) | (-0.600, 0.075, -0.797) | (-0.735, 0.343, 0.585) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| index_dip_l | (0.318, 0.936, -0.151) | (-0.759, 0.156, -0.632) | (-0.568, 0.315, 0.761) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| middle_mcp_l | (0.310, 0.949, -0.065) | (-0.223, 0.006, -0.975) | (-0.924, 0.316, 0.214) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| middle_pip_l | (0.310, 0.949, -0.065) | (-0.655, 0.164, -0.737) | (-0.689, 0.271, 0.672) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| middle_dip_l | (0.310, 0.949, -0.065) | (-0.820, 0.232, -0.523) | (-0.482, 0.215, 0.850) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| ring_mcp_l | (0.299, 0.954, 0.022) | (-0.263, 0.104, -0.959) | (-0.917, 0.281, 0.282) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| ring_pip_l | (0.299, 0.954, 0.022) | (-0.731, 0.244, -0.638) | (-0.614, 0.175, 0.770) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| ring_dip_l | (0.299, 0.954, 0.022) | (-0.885, 0.286, -0.368) | (-0.358, 0.091, 0.929) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| pinky_mcp_l | (0.284, 0.951, 0.125) | (-0.299, 0.212, -0.930) | (-0.911, 0.226, 0.345) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| pinky_pip_l | (0.284, 0.951, 0.125) | (-0.797, 0.306, -0.521) | (-0.534, 0.048, 0.844) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| pinky_dip_l | (0.284, 0.951, 0.125) | (-0.931, 0.304, -0.201) | (-0.229, -0.060, 0.972) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| thumb_cmc_l | (0.831, 0.339, -0.441) | (-0.394, -0.202, -0.897) | (-0.393, 0.919, -0.034) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| thumb_mcp_l | (0.831, 0.339, -0.441) | (-0.505, 0.125, -0.854) | (-0.235, 0.932, 0.275) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| thumb_ip_l | (0.831, 0.339, -0.441) | (-0.556, 0.521, -0.647) | (0.010, 0.783, 0.621) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| hallux_mtp_l | (1.000, -0.017, -0.000) | (-0.017, -0.997, 0.070) | (-0.001, -0.070, -0.998) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| hallux_ip_l | (1.000, -0.017, 0.000) | (-0.017, -0.999, -0.035) | (0.001, 0.035, -0.999) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe2_mtp_l | (0.999, 0.035, -0.000) | (0.034, -0.984, 0.174) | (0.006, -0.174, -0.985) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe2_pip_l | (0.999, 0.035, -0.000) | (0.033, -0.939, -0.342) | (-0.012, 0.342, -0.940) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe2_dip_l | (0.999, 0.035, 0.000) | (0.035, -0.994, -0.105) | (-0.004, 0.104, -0.995) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe3_mtp_l | (0.998, 0.070, -0.000) | (0.069, -0.982, 0.174) | (0.012, -0.173, -0.985) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe3_pip_l | (0.998, 0.070, -0.000) | (0.065, -0.925, -0.375) | (-0.026, 0.374, -0.927) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe3_dip_l | (0.998, 0.070, -0.000) | (0.069, -0.988, -0.139) | (-0.010, 0.139, -0.990) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe4_mtp_l | (0.993, 0.122, -0.000) | (0.120, -0.980, 0.156) | (0.019, -0.155, -0.988) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe4_pip_l | (0.993, 0.122, -0.000) | (0.110, -0.900, -0.423) | (-0.052, 0.419, -0.906) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe4_dip_l | (0.993, 0.122, -0.000) | (0.120, -0.974, -0.191) | (-0.023, 0.189, -0.982) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe5_mtp_l | (0.982, 0.191, 0.000) | (0.189, -0.972, 0.139) | (0.027, -0.137, -0.990) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe5_pip_l | (0.982, 0.191, 0.000) | (0.168, -0.867, -0.469) | (-0.090, 0.461, -0.883) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe5_dip_l | (0.982, 0.191, 0.000) | (0.185, -0.952, -0.242) | (-0.046, 0.237, -0.970) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| hip_r | (1.000, 0.001, -0.022) | (-0.022, 0.031, -0.999) | (0.000, 1.000, 0.031) | +1 / -1 | negative rotation about local +X (right-hand rule, Blender frame) — hip flexion: knee moves anterior |
| knee_r | (0.999, 0.002, -0.041) | (-0.041, 0.041, -0.998) | (0.000, 0.999, 0.041) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — knee flexion: ankle moves posterior |
| ankle_r | (0.983, -0.158, -0.091) | (-0.183, -0.853, -0.489) | (0.000, 0.497, -0.868) | +1 / -1 | negative rotation about local +X (right-hand rule, Blender frame) — ankle dorsiflexion: ball moves up |
| glenohumeral_r | (0.966, 0.041, -0.256) | (-0.260, 0.154, -0.953) | (0.000, 0.987, 0.160) | +1 / -1 | negative rotation about local +X (right-hand rule, Blender frame) — shoulder flexion: elbow moves anterior |
| elbow_r | (0.989, 0.069, -0.134) | (-0.114, -0.243, -0.963) | (-0.099, 0.968, -0.233) | +1 / -1 | negative rotation about local +X (right-hand rule, Blender frame) — elbow flexion: wrist moves anterior |
| wrist_r | (0.388, -0.921, 0.025) | (-0.122, -0.078, -0.989) | (0.914, 0.381, -0.143) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — wrist flexion: hand moves palmar |
| sternoclavicular_r | (0.506, 0.415, -0.756) | (-0.862, 0.243, -0.444) | (0.000, 0.877, 0.481) | +1 / -1 | not defined in this proposal (girdle/jaw/eye axes deferred) |
| jaw_hinge_r | (0.902, 0.315, 0.295) | (0.432, -0.658, -0.616) | (0.000, 0.683, -0.730) | +1 / -1 | not defined in this proposal (girdle/jaw/eye axes deferred) |
| index_mcp_r | (0.399, -0.908, 0.128) | (0.206, -0.048, -0.977) | (0.894, 0.416, 0.168) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| index_pip_r | (0.399, -0.908, 0.128) | (0.577, 0.139, -0.805) | (0.713, 0.395, 0.579) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| index_dip_r | (0.399, -0.908, 0.128) | (0.732, 0.231, -0.641) | (0.552, 0.350, 0.757) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| middle_mcp_r | (0.390, -0.920, 0.042) | (0.204, 0.042, -0.978) | (0.898, 0.390, 0.204) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| middle_pip_r | (0.390, -0.920, 0.042) | (0.626, 0.231, -0.745) | (0.675, 0.317, 0.666) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| middle_dip_r | (0.390, -0.920, 0.042) | (0.788, 0.310, -0.533) | (0.477, 0.241, 0.845) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| ring_mcp_r | (0.379, -0.924, -0.044) | (0.236, 0.142, -0.961) | (0.895, 0.354, 0.272) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| ring_pip_r | (0.379, -0.924, -0.044) | (0.696, 0.316, -0.645) | (0.610, 0.214, 0.763) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| ring_dip_r | (0.379, -0.924, -0.044) | (0.850, 0.366, -0.378) | (0.365, 0.106, 0.925) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| pinky_mcp_r | (0.361, -0.921, -0.147) | (0.263, 0.252, -0.931) | (0.895, 0.297, 0.334) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| pinky_pip_r | (0.361, -0.921, -0.147) | (0.758, 0.382, -0.528) | (0.543, 0.079, 0.836) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| pinky_dip_r | (0.361, -0.921, -0.147) | (0.898, 0.386, -0.211) | (0.251, -0.056, 0.966) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| thumb_cmc_r | (0.864, -0.275, 0.421) | (0.393, -0.152, -0.907) | (0.313, 0.949, -0.024) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| thumb_mcp_r | (0.864, -0.275, 0.421) | (0.477, 0.181, -0.860) | (0.160, 0.944, 0.288) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| thumb_ip_r | (0.864, -0.275, 0.421) | (0.498, 0.577, -0.647) | (-0.065, 0.769, 0.636) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| hallux_mtp_r | (1.000, 0.017, 0.000) | (0.017, -0.997, 0.070) | (0.001, -0.070, -0.998) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| hallux_ip_r | (1.000, 0.017, -0.000) | (0.017, -0.999, -0.035) | (-0.001, 0.035, -0.999) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe2_mtp_r | (0.999, -0.035, 0.000) | (-0.034, -0.984, 0.174) | (-0.006, -0.174, -0.985) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe2_pip_r | (0.999, -0.035, 0.000) | (-0.033, -0.939, -0.342) | (0.012, 0.342, -0.940) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe2_dip_r | (0.999, -0.035, -0.000) | (-0.035, -0.994, -0.105) | (0.004, 0.104, -0.995) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe3_mtp_r | (0.998, -0.070, 0.000) | (-0.069, -0.982, 0.174) | (-0.012, -0.173, -0.985) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe3_pip_r | (0.998, -0.070, 0.000) | (-0.065, -0.925, -0.375) | (0.026, 0.374, -0.927) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe3_dip_r | (0.998, -0.070, 0.000) | (-0.069, -0.988, -0.139) | (0.010, 0.139, -0.990) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe4_mtp_r | (0.993, -0.122, 0.000) | (-0.120, -0.980, 0.156) | (-0.019, -0.155, -0.988) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe4_pip_r | (0.993, -0.122, 0.000) | (-0.110, -0.900, -0.423) | (0.052, 0.419, -0.906) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe4_dip_r | (0.993, -0.122, 0.000) | (-0.120, -0.974, -0.191) | (0.023, 0.189, -0.982) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe5_mtp_r | (0.982, -0.191, -0.000) | (-0.189, -0.972, 0.139) | (-0.027, -0.137, -0.990) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe5_pip_r | (0.982, -0.191, -0.000) | (-0.168, -0.867, -0.469) | (0.090, 0.461, -0.883) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| toe5_dip_r | (0.982, -0.191, -0.000) | (-0.185, -0.952, -0.242) | (0.046, 0.237, -0.970) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — digit flexion: child moves palmar/plantar |
| pelvis_root | (1.000, 0.000, 0.000) | (-0.000, 0.273, 0.962) | (-0.000, -0.962, 0.273) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — trunk/neck flexion: child moves anterior |
| spine_01 | (1.000, -0.002, 0.024) | (-0.024, -0.075, 0.997) | (0.000, -0.997, -0.075) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — trunk/neck flexion: child moves anterior |
| spine_02 | (0.999, 0.002, 0.033) | (-0.034, 0.057, 0.998) | (0.000, -0.998, 0.057) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — trunk/neck flexion: child moves anterior |
| spine_03 | (1.000, 0.001, -0.019) | (0.019, -0.048, 0.999) | (0.000, -0.999, -0.048) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — trunk/neck flexion: child moves anterior |
| neck_base | (1.000, -0.014, 0.024) | (-0.028, -0.503, 0.864) | (0.000, -0.864, -0.503) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — trunk/neck flexion: child moves anterior |
| head_pivot | (1.000, 0.000, 0.005) | (-0.005, 0.072, 0.997) | (0.000, -0.997, 0.072) | +1 / -1 | positive rotation about local +X (right-hand rule, Blender frame) — trunk/neck flexion: child moves anterior |

## 5. Hand / foot construction joints: surface validation on v005

| id | production cm | inside v005 | depth cm | digit-section offset / note | v003 Δ |
|---|---|---|---|---|---|
| ear_tip_l | (11.32, 4.34, 206.74) | yes | 0.03 | None | 0 (construction; not evidence) |
| index_mcp_l | (31.09, 12.70, 90.20) | yes | 1.52 | inside the palm/forefoot mass; 1.52 cm deep | 0 (construction; not evidence) |
| index_pip_l | (29.75, 13.21, 84.21) | yes | 1.08 | digit-section centroid offset 0.03 cm | 0 (construction; not evidence) |
| index_dip_l | (27.48, 12.93, 81.19) | yes | 0.96 | digit-section centroid offset 0.01 cm | 0 (construction; not evidence) |
| index_tip_l | (25.14, 12.45, 79.24) | yes | 0.48 | inside the palm/forefoot mass; 0.48 cm deep; surface tip 0.48 cm beyond | 0 (construction; not evidence) |
| middle_mcp_l | (32.30, 9.82, 89.59) | yes | 1.78 | inside the palm/forefoot mass; 1.78 cm deep | 0 (construction; not evidence) |
| middle_pip_l | (30.81, 9.78, 83.10) | yes | 1.11 | digit-section centroid offset 0.06 cm | 0 (construction; not evidence) |
| middle_dip_l | (28.00, 9.08, 79.94) | yes | 0.99 | digit-section centroid offset 0.01 cm | 0 (construction; not evidence) |
| middle_tip_l | (25.29, 8.31, 78.21) | yes | 0.49 | inside the palm/forefoot mass; 0.49 cm deep; surface tip 0.50 cm beyond | 0 (construction; not evidence) |
| ring_mcp_l | (33.07, 6.66, 89.96) | yes | 1.75 | inside the palm/forefoot mass; 1.75 cm deep | 0 (construction; not evidence) |
| ring_pip_l | (31.39, 6.00, 83.84) | yes | 1.03 | digit-section centroid offset 0.08 cm | 0 (construction; not evidence) |
| ring_dip_l | (28.41, 5.01, 81.24) | yes | 0.94 | digit-section centroid offset 0.01 cm | 0 (construction; not evidence) |
| ring_tip_l | (25.59, 4.10, 80.07) | yes | 0.47 | inside the palm/forefoot mass; 0.47 cm deep; surface tip 0.48 cm beyond | 0 (construction; not evidence) |
| pinky_mcp_l | (33.52, 3.50, 90.96) | yes | 1.46 | inside the palm/forefoot mass; 1.46 cm deep | 0 (construction; not evidence) |
| pinky_pip_l | (31.96, 2.40, 86.10) | yes | 0.88 | digit-section centroid offset 0.10 cm | 0 (construction; not evidence) |
| pinky_dip_l | (29.38, 1.40, 84.41) | yes | 0.81 | digit-section centroid offset 0.01 cm | 0 (construction; not evidence) |
| pinky_tip_l | (26.87, 0.58, 83.86) | yes | 0.42 | inside the palm/forefoot mass; 0.42 cm deep; surface tip 0.42 cm beyond | 0 (construction; not evidence) |
| thumb_cmc_l | (28.71, 10.14, 101.71) | yes | 2.15 | inside the palm/forefoot mass; 2.15 cm deep | 0 (construction; not evidence) |
| thumb_mcp_l | (26.02, 11.51, 95.59) | yes | 1.65 | inside the palm/forefoot mass; 1.65 cm deep | 0 (construction; not evidence) |
| thumb_ip_l | (23.53, 10.90, 91.36) | yes | 1.11 | digit-section centroid offset 0.03 cm | 0 (construction; not evidence) |
| thumb_tip_l | (21.32, 8.83, 88.80) | yes | 0.50 | inside the palm/forefoot mass; 0.50 cm deep; surface tip 0.50 cm beyond | 0 (construction; not evidence) |
| hallux_mtp_l | (13.49, 21.72, 2.30) | yes | 2.10 | inside the palm/forefoot mass; 2.09 cm deep | 0 (construction; not evidence) |
| hallux_ip_l | (13.40, 26.61, 2.64) | yes | 1.68 | digit-section centroid offset 0.00 cm | 0 (construction; not evidence) |
| hallux_tip_l | (13.33, 30.91, 2.49) | yes | 0.95 | inside the palm/forefoot mass; 0.95 cm deep; surface tip 0.95 cm beyond | 0 (construction; not evidence) |
| toe2_mtp_l | (17.64, 21.32, 1.85) | yes | 1.54 | inside the palm/forefoot mass; 1.54 cm deep | 0 (construction; not evidence) |
| toe2_pip_l | (17.80, 25.85, 2.65) | yes | 1.10 | digit-section centroid offset 0.03 cm | 0 (construction; not evidence) |
| toe2_dip_l | (17.88, 28.29, 1.76) | yes | 0.91 | digit-section centroid offset 0.00 cm | 0 (construction; not evidence) |
| toe2_tip_l | (17.95, 30.38, 1.54) | yes | 0.56 | inside the palm/forefoot mass; 0.56 cm deep; surface tip 0.56 cm beyond | 0 (construction; not evidence) |
| toe3_mtp_l | (20.69, 20.32, 1.72) | yes | 1.47 | inside the palm/forefoot mass; 1.47 cm deep | 0 (construction; not evidence) |
| toe3_pip_l | (20.96, 24.25, 2.41) | yes | 1.04 | digit-section centroid offset 0.04 cm | 0 (construction; not evidence) |
| toe3_dip_l | (21.11, 26.38, 1.55) | yes | 0.84 | digit-section centroid offset 0.01 cm | 0 (construction; not evidence) |
| toe3_tip_l | (21.24, 28.26, 1.29) | yes | 0.53 | inside the palm/forefoot mass; 0.53 cm deep; surface tip 0.53 cm beyond | 0 (construction; not evidence) |
| toe4_mtp_l | (23.44, 18.92, 1.62) | yes | 1.53 | inside the palm/forefoot mass; 1.53 cm deep | 0 (construction; not evidence) |
| toe4_pip_l | (23.86, 22.35, 2.17) | yes | 0.99 | digit-section centroid offset 0.09 cm | 0 (construction; not evidence) |
| toe4_dip_l | (24.08, 24.15, 1.32) | yes | 0.78 | digit-section centroid offset 0.02 cm | 0 (construction; not evidence) |
| toe4_tip_l | (24.28, 25.81, 1.00) | yes | 0.50 | inside the palm/forefoot mass; 0.50 cm deep; surface tip 0.50 cm beyond | 0 (construction; not evidence) |
| toe5_mtp_l | (25.89, 17.32, 1.55) | yes | 1.00 | inside the palm/forefoot mass; 1.00 cm deep | 0 (construction; not evidence) |
| toe5_pip_l | (26.44, 20.14, 1.95) | yes | 1.16 | inside the palm/forefoot mass; 1.16 cm deep | 0 (construction; not evidence) |
| toe5_dip_l | (26.72, 21.62, 1.16) | yes | 0.71 | digit-section centroid offset 0.04 cm | 0 (construction; not evidence) |
| toe5_tip_l | (26.99, 23.00, 0.80) | yes | 0.41 | inside the palm/forefoot mass; 0.41 cm deep; surface tip 0.47 cm beyond | 0 (construction; not evidence) |
| ear_tip_r | (-11.54, 4.33, 206.73) | yes | 0.03 | None | 0 (construction; not evidence) |
| index_mcp_r | (-31.38, 12.26, 90.11) | yes | 1.52 | inside the palm/forefoot mass; 1.52 cm deep | 0 (construction; not evidence) |
| index_pip_r | (-30.12, 12.55, 84.08) | yes | 1.08 | digit-section centroid offset 0.03 cm | 0 (construction; not evidence) |
| index_dip_r | (-27.93, 12.02, 81.03) | yes | 0.96 | digit-section centroid offset 0.01 cm | 0 (construction; not evidence) |
| index_tip_r | (-25.67, 11.31, 79.05) | yes | 0.48 | inside the palm/forefoot mass; 0.48 cm deep; surface tip 0.48 cm beyond | 0 (construction; not evidence) |
| middle_mcp_r | (-32.84, 9.48, 89.57) | yes | 1.78 | inside the palm/forefoot mass; 1.78 cm deep | 0 (construction; not evidence) |
| middle_pip_r | (-31.48, 9.21, 83.06) | yes | 1.11 | digit-section centroid offset 0.06 cm | 0 (construction; not evidence) |
| middle_dip_r | (-28.80, 8.21, 79.86) | yes | 0.99 | digit-section centroid offset 0.01 cm | 0 (construction; not evidence) |
| middle_tip_r | (-26.20, 7.19, 78.10) | yes | 0.49 | inside the palm/forefoot mass; 0.49 cm deep; surface tip 0.50 cm beyond | 0 (construction; not evidence) |
| ring_mcp_r | (-33.87, 6.41, 90.00) | yes | 1.75 | inside the palm/forefoot mass; 1.75 cm deep | 0 (construction; not evidence) |
| ring_pip_r | (-32.37, 5.50, 83.87) | yes | 1.03 | digit-section centroid offset 0.08 cm | 0 (construction; not evidence) |
| ring_dip_r | (-29.53, 4.22, 81.25) | yes | 0.94 | digit-section centroid offset 0.01 cm | 0 (construction; not evidence) |
| ring_tip_r | (-26.82, 3.05, 80.04) | yes | 0.47 | inside the palm/forefoot mass; 0.47 cm deep; surface tip 0.48 cm beyond | 0 (construction; not evidence) |
| pinky_mcp_r | (-34.58, 3.31, 91.07) | yes | 1.46 | inside the palm/forefoot mass; 1.46 cm deep | 0 (construction; not evidence) |
| pinky_pip_r | (-33.20, 2.00, 86.20) | yes | 0.88 | digit-section centroid offset 0.10 cm | 0 (construction; not evidence) |
| pinky_dip_r | (-30.74, 0.76, 84.49) | yes | 0.81 | digit-section centroid offset 0.01 cm | 0 (construction; not evidence) |
| pinky_tip_r | (-28.32, -0.28, 83.92) | yes | 0.42 | inside the palm/forefoot mass; 0.42 cm deep; surface tip 0.42 cm beyond | 0 (construction; not evidence) |
| thumb_cmc_r | (-29.03, 9.69, 101.62) | yes | 2.15 | inside the palm/forefoot mass; 2.15 cm deep | 0 (construction; not evidence) |
| thumb_mcp_r | (-26.34, 10.73, 95.43) | yes | 1.65 | inside the palm/forefoot mass; 1.65 cm deep | 0 (construction; not evidence) |
| thumb_ip_r | (-23.98, 9.83, 91.18) | yes | 1.11 | digit-section centroid offset 0.03 cm | 0 (construction; not evidence) |
| thumb_tip_r | (-22.01, 7.55, 88.62) | yes | 0.50 | inside the palm/forefoot mass; 0.50 cm deep; surface tip 0.50 cm beyond | 0 (construction; not evidence) |
| hallux_mtp_r | (-13.71, 21.72, 2.30) | yes | 2.04 | inside the palm/forefoot mass; 2.04 cm deep | 0 (construction; not evidence) |
| hallux_ip_r | (-13.63, 26.61, 2.64) | yes | 1.68 | digit-section centroid offset 0.05 cm | 0 (construction; not evidence) |
| hallux_tip_r | (-13.55, 30.91, 2.49) | yes | 0.95 | inside the palm/forefoot mass; 0.95 cm deep; surface tip 0.95 cm beyond | 0 (construction; not evidence) |
| toe2_mtp_r | (-17.86, 21.32, 1.85) | yes | 1.50 | inside the palm/forefoot mass; 1.50 cm deep | 0 (construction; not evidence) |
| toe2_pip_r | (-18.02, 25.85, 2.65) | yes | 1.09 | digit-section centroid offset 0.08 cm | 0 (construction; not evidence) |
| toe2_dip_r | (-18.11, 28.29, 1.76) | yes | 0.87 | digit-section centroid offset 0.06 cm | 0 (construction; not evidence) |
| toe2_tip_r | (-18.18, 30.38, 1.54) | yes | 0.55 | inside the palm/forefoot mass; 0.55 cm deep; surface tip 0.57 cm beyond | 0 (construction; not evidence) |
| toe3_mtp_r | (-20.91, 20.32, 1.72) | yes | 1.44 | inside the palm/forefoot mass; 1.44 cm deep | 0 (construction; not evidence) |
| toe3_pip_r | (-21.19, 24.25, 2.41) | yes | 1.02 | digit-section centroid offset 0.10 cm | 0 (construction; not evidence) |
| toe3_dip_r | (-21.34, 26.38, 1.55) | yes | 0.80 | digit-section centroid offset 0.07 cm | 0 (construction; not evidence) |
| toe3_tip_r | (-21.47, 28.26, 1.29) | yes | 0.52 | inside the palm/forefoot mass; 0.52 cm deep; surface tip 0.54 cm beyond | 0 (construction; not evidence) |
| toe4_mtp_r | (-23.66, 18.92, 1.62) | yes | 1.42 | inside the palm/forefoot mass; 1.42 cm deep | 0 (construction; not evidence) |
| toe4_pip_r | (-24.08, 22.35, 2.17) | yes | 0.97 | digit-section centroid offset 0.14 cm | 0 (construction; not evidence) |
| toe4_dip_r | (-24.30, 24.15, 1.32) | yes | 0.73 | digit-section centroid offset 0.07 cm | 0 (construction; not evidence) |
| toe4_tip_r | (-24.51, 25.81, 1.00) | yes | 0.49 | inside the palm/forefoot mass; 0.49 cm deep; surface tip 0.52 cm beyond | 0 (construction; not evidence) |
| toe5_mtp_r | (-26.11, 17.32, 1.55) | yes | 1.14 | inside the palm/forefoot mass; 1.14 cm deep | 0 (construction; not evidence) |
| toe5_pip_r | (-26.66, 20.14, 1.95) | yes | 1.15 | inside the palm/forefoot mass; 1.15 cm deep | 0 (construction; not evidence) |
| toe5_dip_r | (-26.95, 21.62, 1.16) | yes | 0.68 | digit-section centroid offset 0.04 cm | 0 (construction; not evidence) |
| toe5_tip_r | (-27.21, 23.00, 0.80) | yes | 0.46 | inside the palm/forefoot mass; 0.46 cm deep; surface tip 0.49 cm beyond | 0 (construction; not evidence) |

## 6. Segment lengths (parent → child, cm)

| parent | child | length | mirrored partner | L − R |
|---|---|---|---|---|
| pelvis_root | hip_l | 13.06 | 13.02 | +0.04 |
| hip_l | knee_l | 47.92 | 47.99 | -0.07 |
| knee_l | ankle_l | 57.70 | 57.54 | +0.16 |
| sternoclavicular_l | glenohumeral_l | 17.47 | 19.61 | -2.14 |
| glenohumeral_l | elbow_l | 32.03 | 29.20 | +2.83 |
| elbow_l | wrist_l | 39.24 | 39.44 | -0.19 |
| spine_03 | sternoclavicular_l | 30.32 | 30.19 | +0.13 |
| head_pivot | jaw_hinge_l | 6.28 | 6.28 | +0.00 |
| head_pivot | eye_l | 9.21 | 9.24 | -0.03 |
| wrist_l | index_mcp_l | 15.89 | 15.89 | +0.00 |
| index_mcp_l | index_pip_l | 6.16 | 6.16 | +0.00 |
| index_pip_l | index_dip_l | 3.79 | 3.79 | +0.00 |
| index_dip_l | index_tip_l | 3.08 | 3.08 | +0.00 |
| wrist_l | middle_mcp_l | 15.76 | 15.76 | +0.00 |
| middle_mcp_l | middle_pip_l | 6.66 | 6.66 | +0.00 |
| middle_pip_l | middle_dip_l | 4.29 | 4.29 | +0.00 |
| middle_dip_l | middle_tip_l | 3.30 | 3.30 | +0.00 |
| wrist_l | ring_mcp_l | 15.22 | 15.22 | +0.00 |
| ring_mcp_l | ring_pip_l | 6.38 | 6.38 | +0.00 |
| ring_pip_l | ring_dip_l | 4.07 | 4.07 | +0.00 |
| ring_dip_l | ring_tip_l | 3.19 | 3.19 | +0.00 |
| wrist_l | pinky_mcp_l | 14.71 | 14.71 | +0.00 |
| pinky_mcp_l | pinky_pip_l | 5.22 | 5.22 | +0.00 |
| pinky_pip_l | pinky_dip_l | 3.25 | 3.25 | +0.00 |
| pinky_dip_l | pinky_tip_l | 2.69 | 2.69 | +0.00 |
| wrist_l | thumb_cmc_l | 5.05 | 5.05 | +0.00 |
| thumb_cmc_l | thumb_mcp_l | 6.82 | 6.82 | +0.00 |
| thumb_mcp_l | thumb_ip_l | 4.95 | 4.95 | +0.00 |
| thumb_ip_l | thumb_tip_l | 3.96 | 3.96 | +0.00 |
| ankle_l | hallux_mtp_l | 24.32 | 25.60 | -1.28 |
| hallux_mtp_l | hallux_ip_l | 4.90 | 4.90 | +0.00 |
| hallux_ip_l | hallux_tip_l | 4.30 | 4.30 | +0.00 |
| ankle_l | toe2_mtp_l | 24.19 | 25.50 | -1.31 |
| toe2_mtp_l | toe2_pip_l | 4.60 | 4.60 | +0.00 |
| toe2_pip_l | toe2_dip_l | 2.60 | 2.60 | +0.00 |
| toe2_dip_l | toe2_tip_l | 2.10 | 2.10 | +0.00 |
| ankle_l | toe3_mtp_l | 23.86 | 25.16 | -1.31 |
| toe3_mtp_l | toe3_pip_l | 4.00 | 4.00 | +0.00 |
| toe3_pip_l | toe3_dip_l | 2.30 | 2.30 | +0.00 |
| toe3_dip_l | toe3_tip_l | 1.90 | 1.90 | +0.00 |
| ankle_l | toe4_mtp_l | 23.52 | 24.80 | -1.28 |
| toe4_mtp_l | toe4_pip_l | 3.50 | 3.50 | +0.00 |
| toe4_pip_l | toe4_dip_l | 2.00 | 2.00 | +0.00 |
| toe4_dip_l | toe4_tip_l | 1.70 | 1.70 | +0.00 |
| ankle_l | toe5_mtp_l | 23.29 | 24.52 | -1.23 |
| toe5_mtp_l | toe5_pip_l | 2.90 | 2.90 | +0.00 |
| toe5_pip_l | toe5_dip_l | 1.70 | 1.70 | +0.00 |
| toe5_dip_l | toe5_tip_l | 1.45 | 1.45 | +0.00 |
| pelvis_root | spine_01 | 10.35 | — | — |
| spine_01 | spine_02 | 8.57 | — | — |
| spine_02 | spine_03 | 7.64 | — | — |
| spine_03 | neck_base | 39.15 | — | — |
| neck_base | head_pivot | 12.77 | — | — |
| head_pivot | crown | 17.84 | — | — |
| head_pivot | chin | 14.00 | — | — |
| ankle_l | ball_l | 22.88 | 24.18 | -1.30 |

## 7. Left / mirrored-right asymmetry of proposals (cm; x_sum = x_l + x_r, 0 = symmetric)

| joint | x_sum | Δf | Δu |
|---|---|---|---|
| hip | +0.22 | +0.09 | -0.13 |
| knee | +0.72 | -0.25 | -0.03 |
| ankle | +0.26 | +1.34 | -0.25 |
| glenohumeral | -1.16 | -2.98 | +2.88 |
| elbow | -0.54 | +0.25 | -0.21 |
| wrist | -0.30 | +0.20 | +0.00 |
| sternoclavicular | +1.21 | +0.00 | -0.05 |
| acromion | -0.71 | -0.44 | +1.68 |
| scapular_inferior_proxy | +0.22 | -0.26 | +0.19 |
| ear_root | +0.05 | +0.09 | -0.08 |
| mouth_corner | -0.03 | -0.06 | +0.00 |
| jaw_hinge | +0.05 | +0.09 | -0.08 |
| eye | +0.00 | +0.00 | +0.00 |
| ball | +0.00 | +0.00 | +0.00 |
