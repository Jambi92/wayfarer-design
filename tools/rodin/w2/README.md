# Saurin W2 tool-chain records (canonical W2 reference, RAC W2I6)

Written by `tools/rac/w1/w2i6_drivers/sa_toolchain6.py` from the canonical W2 reference (the accepted W2I4 candidate; route `tools/rac/w1/w2i4_drivers/sa_finish.build_f`). These sit BESIDE the W1 files, which remain provenance and are unchanged.

| File | W1 counterpart | Content |
|---|---|---|
| `ref_metrics_w2.json` | `../creator-biology/ref_metrics.json` | Part 7 reference metrics measured on W2 SA-M188 |
| `axis_w2.npy` | `../gate8/axis.npy` | Gate 8 centreline of the W2 reference (same 477 samples; tail translated with the pelvis, trunk part follows the W2 stature budget) |
| `g7geo_w2_points.json` | `../gate1/g7geo.py` ARM / LEG | W2 construction points (S / E / W, H at the B1 axis and at the pelvic station, K / A) + the hand pad / claw anchor offset (+6.06 cm) used by `w2i4_drivers/g7surfc_moved.py` |
| `lbase_w2_stations.json` | `Lbase.pkl` stations | station vertex indices (unchanged, identical topology) with W1 and W2 heights |
| `s263_w2.json` | §263 accounting / `female/closure/torsosil.py` | §263 accounting re-verified on W2 (bands carried with the stations) |

W2 region fields: `saurin_w2_regfields.npz` (238 MB, SHA-256 in `reviews/rac-w2i6-sa-evidence/canon6.json`), reproducible with `w2i4_drivers/sa_surface.py` (carried `g15reg` labels + transported N / T). Regional stature route and isometric tail / caudal-base treatment: unchanged accepted W2I route (`w2i_drivers/sa_build.at_stature`).
