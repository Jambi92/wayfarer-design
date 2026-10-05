# ARM Acceptance Record — SA-M: Saurin male centre (manifest #15)

**Order:** RAC W1, W1-01 **Date / pass:** October 5, 2026, W1 pass 1 **Inspector:** Claude
**Asset:** `RaceBodies/out/saurin_final_base.npz`, SHA-256 `a925e067…8b8c9c`; closure reference aff1b52
**Evidence:** `reviews/rac-w1-evidence/saurin_w1.json`, `saurin_symmetry_regions.json`, `saurin_inspect.jpg`; tools `tools/rac/w1/saurin_w1.py`, `saurin_sym_regions.py`

## Technical verdict: **PASS (CONSTRAIN note on R-5/R-6)** — pending author acceptance

| Req. | Check | Finding | Result |
|---|---|---|---|
| R-1 | Central adult | Closure reference body; adult proportions | PASS |
| R-2 | Reference stature by proportion | 187.880 cm vertex (reference 188 cm; tail excluded). Built, not scaled | PASS (−0.12 cm) |
| R-3 | Central skeletal values | Part 7 metrics reproduce the closure reference exactly (head length 31.871 cm, rostral index 0.2879, pelvis 41.73 cm, thorax d/w 0.880) | PASS |
| R-4 | Reference composition | Canonical fat-depot ordering of the closure base | PASS |
| R-5 | Zero natural asymmetry | Head median mirror distance 0.06 cm (p99 0.42); tail 0.20; torso 0.47; arms 1.35; **legs 1.97 (p99 6.91, max 7.73 cm near the left knee, x −30.5, u 38.8)** | **CONSTRAIN**: the residual is stance asymmetry from the frozen pose, not anatomical asymmetry |
| R-6 | Measurement stance | Saurin stance is the frozen closure stance (required tail-balance lean 8.82°). Re-posing would alter the frozen geometry, so it was not done | PASS as frozen; see author decision D-2 |
| R-7 | N3 | Neutral base, no presentation layers | PASS |
| R-8 | No hair | None | PASS |
| R-9 | Neutral surface | Base = no scale relief (scales are a separate surface file) | PASS |
| R-10 | Configuration declared | Male centre (§263) | PASS |
| R-11 | Mandatory anatomy | Tail present (tail lowest point u 67.58 cm; length 121.40 cm = 64.61 % of stature), rostrum | PASS |
| R-12 | No contamination | No equipment/hair/props | PASS |
| R-13 | Units | cm, feet at u = 0.001 | PASS |
| R-14 | Provenance | Hash recorded; no new builder-chosen value | PASS |

**§6 acceptance:** the body meets SAU-BODY-01/02, SAU-FACE-22 stature accounting and the SAU-SILHOUETTE tail requirement as already validated at closure. Measurements taken on it are DIAGNOSTIC (see `reviews/claude-rac-w1-measurements.md`). Left/right readings are kept for limb items because of the R-5 note.
