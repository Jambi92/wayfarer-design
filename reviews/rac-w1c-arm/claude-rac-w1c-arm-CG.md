# ARM Candidate Record — CG: Cogling central

**Order:** `reviews/chatgpt-rac-wave1-continuation-asset-build-order.md` (W1 continuation) **Date / pass:** October 5, 2026, W1c pass 1 **Builder/inspector:** Claude (D-5)
**Geometry:** `reviews/rac-w1c-evidence/geometry/CG_r6.npz` (R-6), SHA-256 `3eab32485dea1c213b82fa4af62f68731804fccc97bfc5263e62b16cfae6d8d2`; rebuild: `tools/rac/w1/cfg/CG.json` + `tools/rac/w1/build_arm.py` (Blender 5.0.1 bpy + MPFB extension)
**Evidence sheet:** `reviews/rac-w1c-evidence/CG_evidence.jpg` (front, side, 3/4, head front, head side; 10 cm / 1 cm ticks; common scale)
**Measurements:** `reviews/rac-w1c-evidence/CG_meas.json`; invariance `CG_inv.json`

## Technical verdict: **FAIL (R-2)** — **diagnostic proxy only** (author ruling, W1c acceptance order §5); replaced by a native short-adult build once that method is accepted

| Req. | Finding |
|---|---|
| R-1 age | Apparent age 35 y (D-4a): MPFB age macro 0.5769 (MakeHuman mapping 0.5 = 25 y, 1.0 = 90 y) |
| R-2 stature | Target 91 cm; measured 91.000 cm (R-6, vertex to sole); **uniform-scale proxy - FAILS R-2**; below generator adult range; uniform-scale proxy (R-2 non-compliant) |
| R-3/R-4 | Generator central values + listed targets; muscle/weight macros 0.5 (BUILDER-CHOSEN) |
| R-5 | Built mirrored (generator symmetric, no asymmetry targets) |
| R-6 | Rig re-pose only (D-4b): arms 8° abduction, elbows extended, palms to thighs; hip joint over ankle, feet parallel/flat; spine/head at generator rest. Invariance (rest vs R-6): rigid single-bone vertex sets max change 0.10 cm; joint-to-joint segment lengths unchanged; foot length +0.08 cm, foot breadth -0.05 cm; head HL -0.0009 cm; pelvic depth +0.01 cm, bitrochanteric -1.11 cm; volume -1.04 %; skinning deformation at the axilla changes max thorax breadth by -1.00 cm -> **anatomical dimensions are read on the generator-authored rest geometry; R-6 supplies stature and the stance evidence** |
| R-7…R-9, R-12 | No hair, clothing, material layers; single neutral surface |
| R-10 | Configuration 1 (MPFB gender macro 1.0), declared at build; paired with MF-M-R for like-for-like tests |
| R-11 | See notes |
| R-13 | cm, up = u, ground at the sole |
| R-14 | Builder-chosen values listed below |
| D-4c eyes | Landmark globes 1.30 cm (DER) at the generator's eye-helper centres. Fit on this candidate: skin vertices inside the globe 0 (clearance 0.013 cm); at +0.2 cm diameter 27 inside |
| Directional checks | 12 / 12 pass (`reviews/claude-rac-w1c-cross-race-audit.md`) |

**Notes:**
- Uniform-scale PROXY, not an ARM (as PK). Globe diameter DER from the scaled socket (1.30 cm) is far below an adult human globe - a proxy artefact.

**BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED:**
- MPFB/MakeHuman generator default proportions, 'race' mix asian 0.333 / caucasian 0.334 / african 0.333 (not Marchfolk biology, D-4d)
- muscle 0.50, weight 0.50, proportions 0.50 (provisional reference composition, D-4d)
- height macro 0.0000 (generator adult minimum; NOT solved - proxy)
- R-6 arm abduction 8.0 deg (canon gives no angle)
- landmark globe diameter 1.30 cm = 2.4 cm x (generator orbit helper extent / MF-M-R helper extent) (D-4c: globe DER from orbit)
- generator targets (identity-relevant race proportion inputs): LR:hand-fingers-length-incr 0.35, LR:hand-scale-incr 0.05, head-scale-depth-decr 0.15, head-scale-horiz-decr 0.15, head-scale-vert-decr 0.25, measure-ankle-circ-decr 0.45, measure-calf-circ-decr 0.50, measure-knee-circ-decr 1.00, measure-lowerarm-length-incr 0.30, measure-lowerleg-height-incr 0.80, measure-napetowaist-dist-decr 0.15, measure-thigh-circ-decr 0.40, measure-upperarm-length-decr 0.80, measure-wrist-circ-decr 0.70, torso-scale-depth-decr 0.15, torso-scale-horiz-decr 0.20
- NON-COMPLIANT uniform scale 0.6373 (proxy only)
