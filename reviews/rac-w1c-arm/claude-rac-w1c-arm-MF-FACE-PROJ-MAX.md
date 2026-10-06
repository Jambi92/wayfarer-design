# ARM Candidate Record — MF-FACE-PROJ-MAX: Marchfolk most-projecting valid adult face (diagnostic head on MF-M-R)

**Order:** `reviews/chatgpt-rac-wave1-continuation-asset-build-order.md` (W1 continuation) **Date / pass:** October 5, 2026, W1c pass 1 **Builder/inspector:** Claude (D-5)
**Geometry:** `reviews/rac-w1c-evidence/geometry/MF-FACE-PROJ-MAX_r6.npz` (R-6), SHA-256 `c6b428dc0571374e35fafb9a240b0bc4c9d25e242cbe245bb116979787431c25`; rebuild: `tools/rac/w1/cfg/MF-FACE-PROJ-MAX.json` + `tools/rac/w1/build_arm.py` (Blender 5.0.1 bpy + MPFB extension)
**Evidence sheet:** `reviews/rac-w1c-evidence/MF-FACE-PROJ-MAX_evidence.jpg` (front, side, 3/4, head front, head side; 10 cm / 1 cm ticks; common scale)
**Measurements:** `reviews/rac-w1c-evidence/MF-FACE-PROJ-MAX_meas.json`; invariance `MF-FACE-PROJ-MAX_inv.json`

## Technical verdict: **PASS** — author acceptance pending

| Req. | Finding |
|---|---|
| R-1 age | Apparent age 35 y (D-4a): MPFB age macro 0.5769 (MakeHuman mapping 0.5 = 25 y, 1.0 = 90 y) |
| R-2 stature | Target 173 cm; measured 173.143 cm (R-6, vertex to sole); native (height macro solved, no scaling); closest reachable native stature (macro step); no scaling applied |
| R-3/R-4 | Generator central values + listed targets; muscle/weight macros 0.5 (BUILDER-CHOSEN) |
| R-5 | Built mirrored (generator symmetric, no asymmetry targets) |
| R-6 | Rig re-pose only (D-4b): arms 8° abduction, elbows extended, palms to thighs; hip joint over ankle, feet parallel/flat; spine/head at generator rest. Invariance (rest vs R-6): rigid single-bone vertex sets max change 0.19 cm; joint-to-joint segment lengths unchanged; foot length +0.14 cm, foot breadth -0.14 cm; head HL +0.0000 cm; pelvic depth +0.43 cm, bitrochanteric -0.35 cm; volume -0.65 %; skinning deformation at the axilla changes max thorax breadth by -1.94 cm -> **anatomical dimensions are read on the generator-authored rest geometry; R-6 supplies stature and the stance evidence** |
| R-7…R-9, R-12 | No hair, clothing, material layers; single neutral surface |
| R-10 | Configuration 1 (MPFB gender macro 1.0), declared at build; paired with MF-M-R for like-for-like tests |
| R-11 | See notes |
| R-13 | cm, up = u, ground at the sole |
| R-14 | Builder-chosen values listed below |
| D-4c eyes | Landmark globes 2.40 cm (DER) at the generator's eye-helper centres. Fit on this candidate: skin vertices inside the globe 0 (clearance 0.027 cm); at +0.2 cm diameter 7 inside |
| Directional checks | 2 / 2 pass (`reviews/claude-rac-w1c-cross-race-audit.md`) |

**Notes:**
- The forward displacement (1.2 cm, bimaxillary, nose and orbits untouched) is BUILDER-CHOSEN; canon gives only the rule (MF L340). Reads as an adult human face with bimaxillary protrusion, no muzzle (evidence sheet, head side).

**BUILDER-CHOSEN / AUTHOR ACCEPTANCE REQUIRED:**
- MPFB/MakeHuman generator default proportions, 'race' mix asian 0.333 / caucasian 0.334 / african 0.333 (not Marchfolk biology, D-4d)
- muscle 0.50, weight 0.50, proportions 0.50 (provisional reference composition, D-4d)
- height macro 0.5000 (solved for native stature)
- R-6 arm abduction 8.0 deg (canon gives no angle)
- landmark globe diameter 2.40 cm = 2.4 cm x (generator orbit helper extent / MF-M-R helper extent) (D-4c: globe DER from orbit)
- lower-face bimaxillary forward displacement 1.2 cm (identity-relevant for the MF maximum)
