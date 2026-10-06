# RAC W1 Continuation — ARM Build and Measurement Method

**Author:** Claude (W1 builder/coordinator, D-5) **Date:** October 5, 2026
**Order:** `reviews/chatgpt-rac-wave1-continuation-asset-build-order.md`
**Status:** Method record. Every choice below that is not canon is a **BUILDER-CHOSEN** or **MEASURER METHOD CHOICE** value and needs author acceptance (§7 circularity rule). None of it is canon.

## 1. Tool chain

| Step | Tool | File |
|---|---|---|
| Build | Blender 5.0.1 (bpy) + MPFB extension (MakeHuman base mesh, `game_engine` rig), headless | `tools/rac/w1/arm_lib.py`, `build_arm.py`, `cfg/<ID>.json` |
| Measure | numpy (surface E-layer landmarks, r3 indices) | `tools/rac/w1/arm_measure.py`, `run_candidate.py` |
| Pose invariance (D-4b) | rest vs R-6 comparison | `tools/rac/w1/invariance.py` |
| Eye fit (D-4c) | globe vs socket | `tools/rac/w1/eyefit.py` |
| Evidence sheets (§8) | orthographic z-buffer renderer | `tools/rac/w1/evidence.py` |
| Directional checks | canon directions vs measured candidates | `tools/rac/w1/directional_checks.py` |
| Docs | tables and ARM records generated from the JSON evidence | `tools/rac/w1/gen_w1c_docs.py` |

The build is deterministic: 4 repeated builds of the same config gave identical stature and landmark vertices. This was observed in the build session; that check is not saved as an evidence file. The R-6 geometry of every candidate is committed with its SHA-256 in `reviews/rac-w1c-evidence/geometry/`.

## 2. Build conventions

1. **Age (D-4a):** 35 years apparent biological age. The MPFB age macro is 0.5769, from MakeHuman's mapping (0.5 = 25 y, 1.0 = 90 y, linear between).
2. **Composition (D-4d):** muscle 0.5, weight 0.5, proportions 0.5, used as provisional builder-chosen reference composition.
3. **Generator defaults (D-4d):** default human proportions, with the generator's default ethnic mix asian 0.333 / caucasian 0.334 / african 0.333. This mix is **not** Marchfolk biology and is never used to derive Marchfolk bounds.
4. **Native stature (R-2):** the MPFB height macro is solved by bisection on the **R-6 stature**, with no uniform scaling.
   - The macro has a step near its default: 0.4845 → 0.485 jumps about 0.37 cm. Where the target falls inside the step, the closest reachable stature is used and the deviation is recorded: MF-M-R +0.14 cm, FN +0.14 cm, HV −0.27 cm.
   - **Range limit:** the generator's adult range is about 137–243 cm at configuration 1 and 123–229 cm at configuration 2.
   - The step and the range limits come from session probes of the macro at 0, 0.5 and 1 and a fine sweep of 0.478–0.492. They are not saved as evidence files and can be reproduced with `arm_lib.build`. **PK (107 cm) and CG (91 cm) cannot be reached natively.** They were built as uniform-scale **proxies**, which are **not R-2 compliant** (see the ARM records).
5. **Configuration (R-10):** Marchfolk is built in both configurations (MPFB gender 1.0 / 0.0). Every one-configuration race is declared configuration 1 (gender 1.0) and paired with MF-M-R for like-for-like tests.
   - Elves: no human soft tissue is imported. Gender 1.0 has no breast tissue, and the generator body carries no genital geometry.
6. **Race proportions:** each race is the MF-M-R build plus **generator targets**, chosen to instantiate the canon directions, then corrected until the directional checks pass (§7: a failed candidate is rebuilt, canon is not changed). Every target and value is listed in the race's ARM record as identity-relevant and builder-chosen.
   - Six correction rounds were needed, plus a seventh after the independent audit added missed directions: AE hands, feet and arm evenness; FN feet; DU arm contribution; VA leg share.
   - The main cause was the generator's tall-stature allometry: the height macro lengthens the long bones faster than the joints and lengthens the arms strongly.
   - One construction trap was found: arm "scale-horiz" targets lengthen the A-posed arm. Arms use depth targets only.
7. **MF-FACE-PROJ-MAX:** the MF-M-R build plus a smooth bimaxillary forward displacement of the lower face (`arm_lib.face_forward`).
   - The displacement is **1.2 cm**, BUILDER-CHOSEN.
   - Full displacement from 5 cm below the eye centres to the chin, fading out at the infraorbital level, under the chin, posteriorly and laterally.
   - The nose, orbits and cranium are untouched. There is no muzzle and no non-human maxilla.
   - The generator's own mouth/chin "forward" targets were tried first and **rejected**: at strength they produce a snout-like lip mass, which is not a valid human face.
8. **Eyeballs (D-4c):** the source generator's eye system supplies the placement (eye-helper centres).
   - **Globe diameter is DER from the orbit:** 2.4 cm (documented adult-human globe size, about 24 mm) × this candidate's helper-socket extent ÷ MF-M-R's.
   - **Fit is checked on every candidate** (`<ID>_meas.json` → `eyefit`; ARM record D-4c row).
   - On MF-M-R, a 2.4 cm globe has 0.03 cm clearance with no skin intersection, and +0.2 cm would intersect. The globe is visible through the lids (aperture area 1.16 cm²).
   - **On MF-F-R the DER globe (2.44 cm) touches the skin at one vertex (0.044 cm).** This is flagged in its record.
   - All the others fit with 0.013–0.055 cm clearance.
   - The globes are landmark geometry, not a racial trait, and placement was never tuned to an FPI.
9. **R-6 stance (D-4b):** rotations of rig bones only:
   - upper arm, forearm and hand aimed down at **8° abduction** (canon gives no angle; BUILDER-CHOSEN);
   - elbows extended;
   - palms toward the thighs (twist split one-third humerus, two-thirds forearm; residual 0.000°);
   - thighs and shanks set to zero frontal-plane angle, so the hip joint sits over the ankle and the feet are at hip width;
   - feet parallel and flat;
   - spine, neck and head left at the generator's upright rest.

## 3. D-4b invariance finding and the rule adopted

Result on every candidate (`*_inv.json`):
- Joint-to-joint segment lengths are unchanged (≤ 2e-5 cm).
- Foot length changes +0.08 to +0.20 cm and foot breadth −0.05 to −0.21 cm (re-aimed foot and toe soft tissue).
- Head dimensions and indices are unchanged, except a 0.001 cm HL change in the CG proxy.
- **Pelvic depth changes 0.00 to +1.22 cm and bitrochanteric breadth −0.17 to −1.40 cm** (gluteal and hip soft tissue when the thighs are re-aimed).
- Rigid single-bone vertex sets move by ≤ 0.27 cm. This is from the residual ≤ 2 % weights.
- Volume changes −0.39 % to −1.06 %.
- **The axilla does not hold.** Linear-blend skinning moves the lateral chest wall, changing the maximum thorax breadth by −0.84 to −3.22 cm (largest in SK), and bideltoid breadth changes with the arm position.

**Rule adopted (a deviation from D-4b as written; author decision D-W1c-1):** the rig cannot demonstrate anatomical invariance at the shoulder girdle and the hip. D-4b says to rebuild directly in R-6 in that case. Rebuilding directly in R-6 is impossible with this generator, whose authored rest pose is the A-pose. So:
- **anatomical dimensions are read on the generator-authored rest geometry**, which has zero skinning deformation;
- **stance-dependent values** (stature, hip-joint height / leg share) and the visual evidence come from the R-6 geometry;
- every share uses the R-6 stature.

This is a method choice for author acceptance (gate D-W1c-1).

## 4. Landmark methods (E layer; MEASURER METHOD CHOICES)

| Item | Method |
|---|---|
| Joint centres | Generator joint system: MakeHuman joint helpers, which are the rig bone heads. Check on MF-M-R (rest geometry): the acromion surface point is 5.6 cm above the rig shoulder joint, and acromion → elbow joint is 29.9 cm. The joint-to-joint upper arm (24.9 cm) reads shorter than the forearm (26.1 cm), which is the reverse of the usual human relation. **The rig's humeral-head joint sits low**, so these joint-to-joint segments are not anatomical joint centres. This is identical for every candidate, so directional comparisons are like-for-like. Absolute segment values are generator-convention, not anthropometric |
| Torso length | Suprasternal proxy (midpoint of the sternoclavicular joints) to the hip-joint midpoint |
| Leg share | Hip-joint height ÷ stature (R-6) |
| Arm, span | Shoulder joint → middle-finger tip; span DER = 2 × arm + shoulder-joint breadth |
| Hand / palm / finger | Wrist joint → fingertip along the hand axis; palm = wrist → middle MCP; palm breadth and depth = PCA extents at 85 % palm length |
| Joint breadths | Maximum PCA extent perpendicular to the limb axis within ±1 cm of the joint centre (skin; soft tissue included) |
| Thorax | Trunk vertices (arm weight < 0.2), slabs ±1 cm; maximum breadth and depth over the spine_02 → shoulder-joint − 2 cm span |
| Pelvis (external only) | Iliac-crest proxy level = generator lumbar joint (spine_01 head). Breadth there; bitrochanteric = maximum width within ±3 cm of the hip joints; AP depth at hip-joint level; vertical contribution = crest proxy − hip joint |
| Profile | Skin section by the plane x = +0.013 cm, keeping the anterior-most crossing per 0.05 cm level |
| Profile points | Pronasale = maximum in the nasal band. Then walking down: subnasale (min), labrale superius (max), stomion (min), labrale inferius (max), labiomental (min), pogonion (max), with 0.03 cm hysteresis and a 3 cm span |
| FAL, Pr | **FAL** (r3 L40, literal) = the more anterior of subnasale (first profile minimum below pronasale) and A' (deepest point of the upper-lip concavity before labrale superius). Nose and vermilion are excluded. On every candidate it is subnasale. **Pr** = cutaneous upper lip at 75 % of the way from subnasale to labrale superius (method choice; MPI depends on it). An earlier window-maximum definition was withdrawn after the audit: FAL always fell on the window edge |
| N\*, G\* | N\* = deepest point between the glabella-equivalent and pronasale |
| Me, Gn | Me = lowest midline chin point within 2.5 cm behind and 3 cm below pogonion; Gn = extreme of (f − u) on that contour |
| Op, V | Most posterior and highest head-surface points, ears excluded |
| Po\* | **Proxy: deepest concha point** (the generator has no ear canal). The implied FH\* tilt is reported. FH\* itself is not used for orientation: as for Saurin, the body frame at neutral carriage is the FH\*-equivalent frame, with ±3° pitch sensitivity reported |
| OC | Landmark globe centres |
| Aperture | Frontal orthographic visibility of the globe through the lids (0.04 cm ray grid) |
| Orbit (E proxy) | Or\* / Os\* = most posterior anterior-surface points 0.4–3 cm below / above the aperture on the vertical through OC; Mf\* = deepest point medial to the aperture; Ec\* = first point lateral to the aperture where the surface turns > 45°. **Low confidence** (soft-tissue proxy for a bony rim) |

**Uncertainty:**
- Mesh edge length is about 0.7 cm on the body and finer on the face, which is coarser than the 0.3 cm in the packets.
- Left and right readings are identical, because the builds are mirrored.
- Directional checks whose relative margin is **under 1 %** are flagged "marginal (inside landmark uncertainty)" in the cross-race audit. That threshold is a method choice.

— Claude

## 5. Author rulings on this method (October 5, 2026; `reviews/chatgpt-rac-w1c-author-acceptance-blocker-resolution-order.md` §3)

| Item | Ruling |
|---|---|
| D-W1c-1 (rest-geometry anatomy, R-6 stance values, R-6 stature for shares) | **Accepted, scope-limited** to this generator-specific W1c diagnostic pass; **not a universal anatomy rule** |
| Generator joint system | Accepted **only for like-for-like W1c directional diagnostics**; absolute segment values are not anthropometric canon |
| 8° arm abduction | Accepted only as the W1c evidence/measurement stance convention |
| FAL / Pr / Po\* proxies, ±0.010 "≈" tolerance, 1 % marginal threshold | Accepted for this pass |
| Soft-tissue orbit proxies | Low confidence; **cannot overrule authored bony-orbit canon** (FN orbit: `reviews/claude-rac-w1d-fenn-orbit-packet.md`) |
| Generator-derived large-race globe allometry | **Not canonized** |
| MF-F-R globe | Fitting ordinary-human landmark globe (2.30 cm) instead of the generator-derived 2.44 cm; face anatomy unchanged |
