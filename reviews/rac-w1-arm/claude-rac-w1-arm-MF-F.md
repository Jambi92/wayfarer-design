# ARM Acceptance Record — MF-F: Marchfolk configuration 2, Iteration 3 candidate (manifest #2)

**Order:** RAC W1, W1-02 **Date / pass:** October 5, 2026, W1 pass 1 **Inspector:** Claude
**Asset:** `RaceBodies/out/Marchfolk_Fem.blend`, SHA-256 `4592b725…2663`
**Evidence:** `reviews/rac-w1-evidence/mf_checks.json`, `mf_Fem_inspect.jpg`

**Superseded (W1 continuation, October 5, 2026):** the corrected/rebuilt candidate is **MF-F-R** (`reviews/rac-w1c-arm/claude-rac-w1c-arm-MF-F-R.md`). This record stays as history.

## Technical verdict: **FAIL (R-2)** — rebuild required. Not measured.

| Req. | Finding | Result |
|---|---|---|
| R-2 Stature by proportion, never uniform scaling | MPFB default female ≈ 159.05 cm, **uniformly scaled ×1.0877** to 173.000 cm | **FAIL** |
| R-1 | Age macro "young" | CONSTRAIN |
| R-6 | A-pose: upper arm 42.5°, elbow flexion 38.8°; thigh 7.7°, shin 5.3° | CONSTRAIN |
| R-11 | No eyeballs | CONSTRAIN |
| Joint centres | Rig upper arm 25.27 cm, forearm 22.92 cm (rig not anatomical) | noted |
| R-5 | mirror p99 5.1e-8 cm | PASS |
| R-14 | Same builder-chosen list as MF-M plus breast macros and the ×1.0877 scale | listed |

Uniform scaling enlarges head, hands, joints and every proportion together, which is exactly what R-2 forbids. Rebuild spec: `reviews/rac-w1-packets/claude-rac-w1-packet-MF-F-R.md`.
