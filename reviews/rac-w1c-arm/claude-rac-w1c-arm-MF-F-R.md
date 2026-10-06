# ARM Candidate Record — MF-F-R: Marchfolk configuration 2 (rebuilt)

**Order:** `reviews/chatgpt-rac-wave1-continuation-asset-build-order.md` (W1 continuation) **Date / pass:** October 5, 2026, W1c pass 1 **Builder/inspector:** Claude (D-5)
**Geometry:** `reviews/rac-w1c-evidence/geometry/MF-F-R_r6.npz` (R-6), SHA-256 `c448c4bd8a70c929da962dc8b2b1eded7fee900ebe865343a3fde7a9cefa9cc9`; rebuild: `tools/rac/w1/cfg/MF-F-R.json` + `tools/rac/w1/build_arm.py` (Blender 5.0.1 bpy + MPFB extension)
**Evidence sheet:** `reviews/rac-w1c-evidence/MF-F-R_evidence.jpg` (front, side, 3/4, head front, head side; 10 cm / 1 cm ticks; common scale)
**Measurements:** `reviews/rac-w1c-evidence/MF-F-R_meas.json`; invariance `MF-F-R_inv.json`

## Technical verdict: **PASS** — **AUTHOR-ACCEPTED W1 reference asset** (October 5, 2026; `reviews/chatgpt-rac-w1c-author-acceptance-blocker-resolution-order.md` §2). Generator-target magnitudes stay reference construction values, not population-envelope canon; diagnostics are not canon

| Req. | Finding |
|---|---|
| R-1 age | Apparent age 35 y (D-4a): MPFB age macro 0.5769 (MakeHuman mapping 0.5 = 25 y, 1.0 = 90 y) |
| R-2 stature | Target 173 cm; measured 172.991 cm (R-6, vertex to sole); native (height macro solved, no scaling) |
| R-3/R-4 | Generator central values + listed targets; muscle/weight macros 0.5 (BUILDER-CHOSEN) |
| R-5 | Built mirrored (generator symmetric, no asymmetry targets) |
| R-6 | Rig re-pose only (D-4b): arms 8° abduction, elbows extended, palms to thighs; hip joint over ankle, feet parallel/flat; spine/head at generator rest. Invariance (rest vs R-6): rigid single-bone vertex sets max change 0.18 cm; joint-to-joint segment lengths unchanged; foot length +0.20 cm, foot breadth -0.06 cm; head HL +0.0000 cm; pelvic depth +0.00 cm, bitrochanteric -0.17 cm; volume -0.40 %; skinning deformation at the axilla changes max thorax breadth by -0.84 cm -> **anatomical dimensions are read on the generator-authored rest geometry; R-6 supplies stature and the stance evidence** |
| R-7…R-9, R-12 | No hair, clothing, material layers; single neutral surface |
| R-10 | Configuration 2 (MPFB gender macro 0.0) |
| R-11 | See notes |
| R-13 | cm, up = u, ground at the sole |
| R-14 | Builder-chosen values listed below |
| D-4c eyes | Landmark globes 2.30 cm (fitting ordinary-human size, author ruling) at the generator's eye-helper centres. Fit on this candidate: skin vertices inside the globe 0 (clearance 0.026 cm); at +0.2 cm diameter 4 inside |
| Directional checks | 0 / 0 pass (`reviews/claude-rac-w1c-cross-race-audit.md`) |

**Notes:**
- D-4c (author ruling, W1c acceptance order §2): the generator-derived globe (2.44 cm) touched the socket skin at one vertex (0.044 cm), so it is replaced by a fitting ordinary-human landmark globe of 2.30 cm (BUILDER-CHOSEN size; 0.026 cm clearance; 2.35 cm leaves 0.001 cm, 2.40 cm intersects). Placement (generator eye centres) and face anatomy unchanged; FPI is unaffected (it uses the globe centre).

**BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED:**
- MPFB/MakeHuman generator default proportions, 'race' mix asian 0.333 / caucasian 0.334 / african 0.333 (not Marchfolk biology, D-4d)
- muscle 0.50, weight 0.50, proportions 0.50 (provisional reference composition, D-4d)
- height macro 0.6060 (solved for native stature)
- R-6 arm abduction 8.0 deg (canon gives no angle)
- landmark globe diameter 2.30 cm (fitting ordinary-human landmark globe; author ruling W1c acceptance §2)
