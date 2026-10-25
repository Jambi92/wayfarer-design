| | x1 (cage21 x1) | x2 raw (cage21 x2) | v002 selected (cage27 x2) | v001 reference (cage21 x3) |
|---|---|---|---|---|
| Vertices | 39,298 | 157,186 | 164,514 | 628,738 |
| Quads | 39,296 | 157,184 | 164,512 | 628,736 |
| Triangle equivalent | 78,592 | 314,368 | 329,024 | 1,257,472 |
| Mean edge head_face (mm) | 8.08 **over ceiling** | 3.87  | 3.87  | 1.93  |
| Mean edge ears (mm) | 4.96  | 2.49  | 2.49  | 1.27  |
| Mean edge hands (mm) | 5.16  | 2.52  | 2.44  | 1.26  |
| Mean edge feet (mm) | 5.96  | 2.83  | 2.72  | 1.42  |
| Mean edge trunk_limbs (mm) | 10.97  | 5.31  | 5.19  | 2.66  |
| T-1 body max (mm) | FAIL (8.52) | PASS (1.92) | PASS (1.56) | PASS (1.07) |
| T-2 identity zones | FAIL — fails head_face, ears, hand_l, hand_r, foot_r (max 8.52) | PASS (max 1.32) | PASS (max 1.40) | PASS (max 1.07) |
| T-3 stature / bbox (mm) | PASS (-0.30 / 0.22) | PASS (-0.08 / 0.11) | PASS (-0.09 / 0.11) | PASS (-0.04 / 0.05) |
| T-6 landmark max (mm) | FAIL (10.88) | PASS (0.84) | PASS (0.84) | PASS (0.64) |
| T-7 min IoU front/profile/rear | FAIL (0.9941) | PASS (0.9953) | PASS (0.9956) | PASS (0.9966) |
| Loop audit (69 joints) | FAIL — 24 fail | FAIL — 7 fail | PASS | PASS |
| Hard-limit quads | 2571 | 74 | 0 | 712 |
| Quads 45–135° / aspect ≤4 (%) | 79.3 / 99.5 | 95.2 / 99.1 | 94.7 / 98.7 | 95.1 / 98.2 |
| Worst angle min / max (°), max aspect | 0.1 / 179.6, 6.85 | 3.7 / 176.1, 9.96 | 20.2 / 160.0, 7.47 | 1.1 / 179.4, 30.75 |
| Self-intersection pairs | 0 | 0 | 0 | 0 |
| **Verdict** | **FAIL** | **FAIL** | **PASS** | **FAIL** |
