# ARM Candidate Record — PK: Pipkin central

**Order:** `reviews/chatgpt-rac-wave1-continuation-asset-build-order.md` (W1 continuation) **Date / pass:** October 5, 2026, W1c pass 1 **Builder/inspector:** Claude (D-5)
**Geometry:** `reviews/rac-w1c-evidence/geometry/PK_r6.npz` (R-6), SHA-256 `0a1132354cc1440d6902495eb6318998eb5a5cb967878a9aac924b21026ccf62`; rebuild: `tools/rac/w1/cfg/PK.json` + `tools/rac/w1/build_arm.py` (Blender 5.0.1 bpy + MPFB extension)
**Evidence sheet:** `reviews/rac-w1c-evidence/PK_evidence.jpg` (front, side, 3/4, head front, head side; 10 cm / 1 cm ticks; common scale)
**Measurements:** `reviews/rac-w1c-evidence/PK_meas.json`; invariance `PK_inv.json`

## Technical verdict: **FAIL (R-2)** — not an ARM candidate in this form

| Req. | Finding |
|---|---|
| R-1 age | Apparent age 35 y (D-4a): MPFB age macro 0.5769 (MakeHuman mapping 0.5 = 25 y, 1.0 = 90 y) |
| R-2 stature | Target 107 cm; measured 107.000 cm (R-6, vertex to sole); **uniform-scale proxy - FAILS R-2**; below generator adult range; uniform-scale proxy (R-2 non-compliant) |
| R-3/R-4 | Generator central values + listed targets; muscle/weight macros 0.5 (BUILDER-CHOSEN) |
| R-5 | Built mirrored (generator symmetric, no asymmetry targets) |
| R-6 | Rig re-pose only (D-4b): arms 8° abduction, elbows extended, palms to thighs; hip joint over ankle, feet parallel/flat; spine/head at generator rest. Invariance (rest vs R-6): rigid single-bone vertex sets max change 0.13 cm; joint-to-joint segment lengths unchanged; foot length +0.10 cm, foot breadth -0.07 cm; head HL +0.0000 cm; pelvic depth +0.59 cm, bitrochanteric -0.65 cm; volume -0.87 %; skinning deformation at the axilla changes max thorax breadth by -1.23 cm -> **anatomical dimensions are read on the generator-authored rest geometry; R-6 supplies stature and the stance evidence** |
| R-7…R-9, R-12 | No hair, clothing, material layers; single neutral surface |
| R-10 | Configuration 1 (MPFB gender macro 1.0), declared at build; paired with MF-M-R for like-for-like tests |
| R-11 | See notes |
| R-13 | cm, up = u, ground at the sole |
| R-14 | Builder-chosen values listed below |
| D-4c eyes | Landmark globes 1.62 cm (DER) at the generator's eye-helper centres. Fit on this candidate: skin vertices inside the globe 0 (clearance 0.017 cm); at +0.2 cm diameter 13 inside |
| Directional checks | 7 / 7 pass (`reviews/claude-rac-w1c-cross-race-audit.md`) |

**Notes:**
- The candidate is a uniform-scale PROXY (factor in the builder-chosen list); measurements are diagnostic of the proportion targets only.
- Pelvis: Pipkin LSCTA pelvis not authored in detail; generator human pelvis with targets.

**BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED:**
- MPFB/MakeHuman generator default proportions, 'race' mix asian 0.333 / caucasian 0.334 / african 0.333 (not Marchfolk biology, D-4d)
- muscle 0.50, weight 0.50, proportions 0.50 (provisional reference composition, D-4d)
- height macro 0.0000 (generator adult minimum; NOT solved - proxy)
- R-6 arm abduction 8.0 deg (canon gives no angle)
- landmark globe diameter 1.62 cm = 2.4 cm x (generator orbit helper extent / MF-M-R helper extent) (D-4c: globe DER from orbit)
- generator targets (identity-relevant race proportion inputs): LR:foot-scale-incr 0.10, hip-scale-depth-incr 0.15, hip-scale-horiz-incr 0.25, hip-scale-vert-incr 0.30, measure-lowerleg-height-incr 0.20, measure-napetowaist-dist-decr 0.40, measure-upperleg-height-incr 0.20, measure-wrist-circ-decr 0.15, torso-scale-horiz-decr 0.05
- NON-COMPLIANT uniform scale 0.7675 (proxy only)
