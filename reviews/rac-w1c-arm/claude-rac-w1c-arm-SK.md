# ARM Candidate Record — SK: Skarn central

**Order:** `reviews/chatgpt-rac-wave1-continuation-asset-build-order.md` (W1 continuation) **Date / pass:** October 5, 2026, W1c pass 1 **Builder/inspector:** Claude (D-5)
**Geometry:** `reviews/rac-w1c-evidence/geometry/SK_r6.npz` (R-6), SHA-256 `a49d5572839a5ab114fce212c79054b6390fef0d34683b20a439c8acabfb0da7`; rebuild: `tools/rac/w1/cfg/SK.json` + `tools/rac/w1/build_arm.py` (Blender 5.0.1 bpy + MPFB extension)
**Evidence sheet:** `reviews/rac-w1c-evidence/SK_evidence.jpg` (front, side, 3/4, head front, head side; 10 cm / 1 cm ticks; common scale)
**Measurements:** `reviews/rac-w1c-evidence/SK_meas.json`; invariance `SK_inv.json`

## Technical verdict: **PASS** — **AUTHOR-ACCEPTED W1 reference asset** (October 5, 2026; `reviews/chatgpt-rac-w1c-author-acceptance-blocker-resolution-order.md` §2). Generator-target magnitudes stay reference construction values, not population-envelope canon; diagnostics are not canon

| Req. | Finding |
|---|---|
| R-1 age | Apparent age 35 y (D-4a): MPFB age macro 0.5769 (MakeHuman mapping 0.5 = 25 y, 1.0 = 90 y) |
| R-2 stature | Target 208 cm; measured 208.005 cm (R-6, vertex to sole); native (height macro solved, no scaling) |
| R-3/R-4 | Generator central values + listed targets; muscle/weight macros 0.5 (BUILDER-CHOSEN) |
| R-5 | Built mirrored (generator symmetric, no asymmetry targets) |
| R-6 | Rig re-pose only (D-4b): arms 8° abduction, elbows extended, palms to thighs; hip joint over ankle, feet parallel/flat; spine/head at generator rest. Invariance (rest vs R-6): rigid single-bone vertex sets max change 0.24 cm; joint-to-joint segment lengths unchanged; foot length +0.17 cm, foot breadth -0.19 cm; head HL -0.0000 cm; pelvic depth +1.13 cm, bitrochanteric -0.28 cm; volume -0.60 %; skinning deformation at the axilla changes max thorax breadth by -3.22 cm -> **anatomical dimensions are read on the generator-authored rest geometry; R-6 supplies stature and the stance evidence** |
| R-7…R-9, R-12 | No hair, clothing, material layers; single neutral surface |
| R-10 | Configuration 1 (MPFB gender macro 1.0), declared at build; paired with MF-M-R for like-for-like tests |
| R-11 | See notes |
| R-13 | cm, up = u, ground at the sole |
| R-14 | Builder-chosen values listed below |
| D-4c eyes | Landmark globes 2.76 cm (DER) at the generator's eye-helper centres. Fit on this candidate: skin vertices inside the globe 0 (clearance 0.045 cm); at +0.2 cm diameter 3 inside |
| Directional checks | 9 / 9 pass (`reviews/claude-rac-w1c-cross-race-audit.md`) |

**Notes:**
- None beyond the builder-chosen list.

**BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED:**
- MPFB/MakeHuman generator default proportions, 'race' mix asian 0.333 / caucasian 0.334 / african 0.333 (not Marchfolk biology, D-4d)
- muscle 0.50, weight 0.50, proportions 0.50 (provisional reference composition, D-4d)
- height macro 0.7832 (solved for native stature)
- R-6 arm abduction 8.0 deg (canon gives no angle)
- landmark globe diameter 2.76 cm = 2.4 cm x (generator orbit helper extent / MF-M-R helper extent) (D-4c: globe DER from orbit)
- generator targets (identity-relevant race proportion inputs): LR:foot-scale-incr 0.15, LR:hand-scale-incr 0.20, LR:lowerarm-scale-depth-incr 1.00, LR:lowerleg-scale-depth-incr 0.30, LR:lowerleg-scale-horiz-incr 0.30, LR:upperarm-scale-depth-incr 0.60, LR:upperleg-scale-horiz-incr 0.20, hip-scale-depth-incr 0.10, hip-scale-horiz-incr 0.15, measure-ankle-circ-incr 0.60, measure-calf-circ-incr 0.60, measure-knee-circ-incr 1.00, measure-lowerarm-length-decr 0.40, measure-napetowaist-dist-incr 0.40, measure-neck-circ-incr 0.25, measure-shoulder-dist-incr 0.80, measure-thigh-circ-incr 0.60, measure-underbust-circ-incr 0.20, measure-upperarm-length-decr 0.60, measure-upperleg-height-decr 1.00, measure-wrist-circ-incr 0.60, torso-scale-depth-incr 0.60
