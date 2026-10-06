# ARM Candidate Record — GR: Grask central

**Order:** `reviews/chatgpt-rac-wave1-continuation-asset-build-order.md` (W1 continuation) **Date / pass:** October 5, 2026, W1c pass 1 **Builder/inspector:** Claude (D-5)
**Geometry:** `reviews/rac-w1c-evidence/geometry/GR_r6.npz` (R-6), SHA-256 `552128b370ef5b7fa4488ad5e23069b8682755741d9c860d1ef3e11173e9dc93`; rebuild: `tools/rac/w1/cfg/GR.json` + `tools/rac/w1/build_arm.py` (Blender 5.0.1 bpy + MPFB extension)
**Evidence sheet:** `reviews/rac-w1c-evidence/GR_evidence.jpg` (front, side, 3/4, head front, head side; 10 cm / 1 cm ticks; common scale)
**Measurements:** `reviews/rac-w1c-evidence/GR_meas.json`; invariance `GR_inv.json`

## Technical verdict: **CONSTRAIN** — **CONSTRAINED diagnostic candidate** (author ruling, W1c acceptance order §4): proportion evidence may remain; human-generator ears/pelvis and missing non-human structures do not satisfy canon

| Req. | Finding |
|---|---|
| R-1 age | Apparent age 35 y (D-4a): MPFB age macro 0.5769 (MakeHuman mapping 0.5 = 25 y, 1.0 = 90 y) |
| R-2 stature | Target 218 cm; measured 217.989 cm (R-6, vertex to sole); native (height macro solved, no scaling) |
| R-3/R-4 | Generator central values + listed targets; muscle/weight macros 0.5 (BUILDER-CHOSEN) |
| R-5 | Built mirrored (generator symmetric, no asymmetry targets) |
| R-6 | Rig re-pose only (D-4b): arms 8° abduction, elbows extended, palms to thighs; hip joint over ankle, feet parallel/flat; spine/head at generator rest. Invariance (rest vs R-6): rigid single-bone vertex sets max change 0.22 cm; joint-to-joint segment lengths unchanged; foot length +0.17 cm, foot breadth -0.17 cm; head HL +0.0000 cm; pelvic depth +1.10 cm, bitrochanteric -0.27 cm; volume -0.49 %; skinning deformation at the axilla changes max thorax breadth by -2.17 cm -> **anatomical dimensions are read on the generator-authored rest geometry; R-6 supplies stature and the stance evidence** |
| R-7…R-9, R-12 | No hair, clothing, material layers; single neutral surface |
| R-10 | Configuration 1 (MPFB gender macro 1.0), declared at build; paired with MF-M-R for like-for-like tests |
| R-11 | See notes |
| R-13 | cm, up = u, ground at the sole |
| R-14 | Builder-chosen values listed below |
| D-4c eyes | Landmark globes 2.77 cm (DER) at the generator's eye-helper centres. Fit on this candidate: skin vertices inside the globe 0 (clearance 0.045 cm); at +0.2 cm diameter 3 inside |
| Directional checks | 21 / 21 pass (`reviews/claude-rac-w1c-cross-race-audit.md`) |

**Notes:**
- R-11: folded late-taper ear NOT instantiated (human auricle).
- Pelvis and shoulder girdle: non-human morphology not authored; generator human structure carried.

**BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED:**
- MPFB/MakeHuman generator default proportions, 'race' mix asian 0.333 / caucasian 0.334 / african 0.333 (not Marchfolk biology, D-4d)
- muscle 0.50, weight 0.50, proportions 0.50 (provisional reference composition, D-4d)
- height macro 0.7881 (solved for native stature)
- R-6 arm abduction 8.0 deg (canon gives no angle)
- landmark globe diameter 2.77 cm = 2.4 cm x (generator orbit helper extent / MF-M-R helper extent) (D-4c: globe DER from orbit)
- generator targets (identity-relevant race proportion inputs): LR:hand-fingers-length-incr 0.40, LR:hand-scale-incr 0.15, head-scale-vert-incr 0.20, measure-knee-circ-incr 0.10, measure-lowerarm-length-incr 0.60, measure-lowerleg-height-incr 1.00, measure-napetowaist-dist-decr 0.30, measure-upperarm-length-incr 0.05, measure-upperleg-height-decr 0.30, measure-wrist-circ-incr 0.10, mouth-trans-down 0.20, nose-scale-vert-incr 0.50, torso-scale-horiz-decr 0.10
