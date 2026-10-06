# ARM Candidate Record — HV: Halvren central (no-lineage general envelope)

**Order:** `reviews/chatgpt-rac-wave1-continuation-asset-build-order.md` (W1 continuation) **Date / pass:** October 5, 2026, W1c pass 1 **Builder/inspector:** Claude (D-5)
**Geometry:** `reviews/rac-w1c-evidence/geometry/HV_r6.npz` (R-6), SHA-256 `dbef6095f945ced1be5bf0638e1bc82dc308ee3896b9ffd0caa4edb9f3290b1d`; rebuild: `tools/rac/w1/cfg/HV.json` + `tools/rac/w1/build_arm.py` (Blender 5.0.1 bpy + MPFB extension)
**Evidence sheet:** `reviews/rac-w1c-evidence/HV_evidence.jpg` (front, side, 3/4, head front, head side; 10 cm / 1 cm ticks; common scale)
**Measurements:** `reviews/rac-w1c-evidence/HV_meas.json`; invariance `HV_inv.json`

## Technical verdict: **CONSTRAIN** — **CONSTRAINED diagnostic candidate** (author ruling, W1c acceptance order §4): proportion evidence may remain; human-generator ears/pelvis and missing non-human structures do not satisfy canon; early build accepted only as a diagnostic ordering deviation; source-span checks re-run after FN/AE/VA are accepted

| Req. | Finding |
|---|---|
| R-1 age | Apparent age 35 y (D-4a): MPFB age macro 0.5769 (MakeHuman mapping 0.5 = 25 y, 1.0 = 90 y) |
| R-2 stature | Target 178 cm; measured 177.726 cm (R-6, vertex to sole); native (height macro solved, no scaling); closest reachable native stature (macro step); no scaling applied |
| R-3/R-4 | Generator central values + listed targets; muscle/weight macros 0.5 (BUILDER-CHOSEN) |
| R-5 | Built mirrored (generator symmetric, no asymmetry targets) |
| R-6 | Rig re-pose only (D-4b): arms 8° abduction, elbows extended, palms to thighs; hip joint over ankle, feet parallel/flat; spine/head at generator rest. Invariance (rest vs R-6): rigid single-bone vertex sets max change 0.19 cm; joint-to-joint segment lengths unchanged; foot length +0.14 cm, foot breadth -0.14 cm; head HL -0.0000 cm; pelvic depth +0.43 cm, bitrochanteric -0.35 cm; volume -0.61 %; skinning deformation at the axilla changes max thorax breadth by -1.96 cm -> **anatomical dimensions are read on the generator-authored rest geometry; R-6 supplies stature and the stance evidence** |
| R-7…R-9, R-12 | No hair, clothing, material layers; single neutral surface |
| R-10 | Configuration 1 (MPFB gender macro 1.0), declared at build; paired with MF-M-R for like-for-like tests |
| R-11 | See notes |
| R-13 | cm, up = u, ground at the sole |
| R-14 | Builder-chosen values listed below |
| D-4c eyes | Landmark globes 2.44 cm (DER) at the generator's eye-helper centres. Fit on this candidate: skin vertices inside the globe 0 (clearance 0.028 cm); at +0.2 cm diameter 4 inside |
| Directional checks | 8 / 8 pass (`reviews/claude-rac-w1c-cross-race-audit.md`) |

**Notes:**
- R-11: mixed coupled human + elven ear NOT instantiated.
- The no-lineage general envelope is BUILDER-CHOSEN as a whole (canon: not 50/50, not a linear morph, but no central values); identity-relevant, needs author acceptance.
- Native stature 177.73 cm (generator height-macro step; -0.27 cm).
- Order deviation: HV was built in this pass although its elven sources (FN, AE, VA) are CONSTRAIN, not PASS (order §7 item 14). Its source-span checks use those candidates; they must be re-run when the sources are accepted.

**BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED:**
- MPFB/MakeHuman generator default proportions, 'race' mix asian 0.333 / caucasian 0.334 / african 0.333 (not Marchfolk biology, D-4d)
- muscle 0.50, weight 0.50, proportions 0.50 (provisional reference composition, D-4d)
- height macro 0.5435 (solved for native stature)
- R-6 arm abduction 8.0 deg (canon gives no angle)
- landmark globe diameter 2.44 cm = 2.4 cm x (generator orbit helper extent / MF-M-R helper extent) (D-4c: globe DER from orbit)
- generator targets (identity-relevant race proportion inputs): LR:eye-scale-incr 0.10, LR:hand-fingers-length-incr 0.12, measure-ankle-circ-decr 0.10, measure-lowerarm-length-incr 0.12, measure-lowerleg-height-incr 0.12, measure-napetowaist-dist-decr 0.10, measure-wrist-circ-decr 0.15, torso-scale-depth-decr 0.05
