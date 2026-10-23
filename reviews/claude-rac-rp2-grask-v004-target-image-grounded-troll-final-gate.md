# RAC RP2 — Grask v004 target-image grounded-troll build: final gate

**Status: RP2 GRASK TARGET-IMAGE GROUNDED-TROLL BUILD PASS / READY FOR AUTHOR REVIEW**

- **Order:** `reviews/chatgpt-rac-rp2-grask-v004-target-image-grounded-troll-build-order.md` (fe03f91)
- **Visual authority:** Tyler's attached target turnaround (front / profile / three-quarter)
- **Candidate:** `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Grask/RP2/GR_U_REF_RP2_production_v004.blend`
  - file SHA-256 `cd8f1cdb9eaf8f3b815a104bc71ddfd0807e4ea45a3c578ccedb282fb763b2f3`
  - geometry SHA-256 `de46b5d8…9cd5`
  - The PC copy was read back and matches.
  - The sidecar, landmarks, edit masks and MPFB mapping are next to the .blend.
- **Preserved, hashes re-checked on the PC:**
  - v001 `81f579f9…9c0a`
  - v002 `9622a062…23ee`
  - v003 `46697d1b…5b52`
- **Evidence:** `reviews/rac-rp2-evidence/grask_v004_target_image/`, with these folders:
  - `gates/`
  - `ratio_study/`
  - `sheets/`
  - `production/`
  - `tools/`, which includes the build parameters `params_v004.json`

## 1. Why v003 failed visually

v003 fixed v002's alien face but kept a body of human width:

- **Shoulders:** 0.235 H, against the target's 0.252.
- **Neck:** thin, 0.83 of head width against the target's 1.17.
- **Limbs:** slender forearms, thighs and calves.
- **Feet:** short, 0.169 H against the target's 0.198.

At game distance it read as a tall, thin human with troll ears. The target reads as a troll because of its massing: a wide, load-bearing girdle, a thick neck flowing into the trapezius, and heavy forearms, calves and feet on long limbs.

## 2. Target-image ratio study (order §12)

The target was gridded and stations were read by hand in pixel rows:

| Station | Pixel row |
|---|---|
| Crown | 68 |
| Chin | 228 |
| Acromion | 275 |
| Elbow | 510 |
| Wrist | 735 |
| Fingertip | 900 |
| Hip | 640 |
| Knee | 940 |
| Ankle | 1300 |
| Sole | 1380 |

The mesh stations come from the mesh joints. The same silhouette measurements were then taken on all three. These are visual calibration ratios only, not canon numbers. Script and data: `ratio_study/ratios.py` and `ratios.json`; gridded target: `target_grid_*.jpg`.

| Ratio | Target | v003 | **v004** | v004 / target |
|---|---|---|---|---|
| Shoulder width / height | 0.252 | 0.235 | **0.258** | 1.02 |
| Ribcage width / height (t 0.34) | 0.149 | 0.152 | **0.164** | 1.10 |
| Waist / shoulder | 0.616 | 0.635 | **0.632** | 1.03 |
| Pelvis / shoulder | 0.807 | 0.792 | **0.780** | 0.97 |
| Hand length / forearm length | 0.733 | 0.742 | **0.755** | 1.03 |
| Foot length / height | 0.198 | 0.169 | **0.184** | 0.93 |
| Head height / height | 0.122 | 0.105 | **0.104** | 0.85 |
| Neck width / head width | 1.172 | 0.832 | **0.979** | 0.84 |
| Upper-arm thickness / arm length | 0.096 | 0.108 | **0.118** | 1.23 |
| Forearm thickness / forearm length | 0.324 | 0.305 | **0.376** | 1.16 |
| Thigh thickness / leg length | 0.131 | 0.110 | **0.122** | 0.93 |
| Calf thickness / lower-leg length | 0.267 | 0.229 | **0.245** | 0.92 |

Every carrier moved from v003 toward the target or past it. Three ratios are left short of the target on purpose:

- **Head size (0.85).** The order asks for a compact head with no alien elongation, so the target's larger head was not copied.
- **Foot length (0.93).** The foot is +3.3 cm over v003. Going further caused toe contact in toe extension.
- **Calf thickness (0.92).** It is limited by knee-flexion contact.

The target's pelvis and lower abdomen are partly covered by the loincloth, so those two rows are approximate.

## 3. Macro-body changes (v003 → v004)

Topology is unchanged: 214 146 vertices and 214 144 quads, same order. Body deltas are low-passed (macro_lowpass 60) so the mass changes stay smooth.

- **Shoulder girdle.**
  - The arm chain was shifted 2.4 cm laterally (clavicle lengthening).
  - Shoulder span is 63.2 cm, up from 57.8.
  - The trapezius, nuchal mass and pectorals were raised.
- **Neck.**
  - Neck breadth was raised to 1.26–1.32 laterally and 1.28–1.45 front-to-back.
  - The neck mask was extended up to the jaw, so the neck now flows from the jaw into the trapezius.
- **Trunk.** Four zones run from 92 to 178 cm, with separate front and back factors.
  - The ribcage has more breadth and depth: trunk depth at 130 cm is 27.95 cm, up from 24.35.
  - Back mass is real.
  - The glutes were moderated (back factor 1.18), so the profile stays grounded rather than soft.
- **Arms.**
  - The deltoid cap is 1.22.
  - The forearm is heavy: 1.8 lateral and 1.45 front-to-back at its widest.
- **Legs.**
  - Thighs are 1.26 lateral and 1.12–1.16 front-to-back, with the medial side damped to 0.55 to keep the crotch clear.
  - The upper-thigh front was kept at 1.0 for clearance in hip flexion.
  - Calves are 1.5–1.62 laterally.

## 4. Head, face and ears

- **Head order.** The head was faired before the warps, so the brow survives smoothing.
- **Brow and orbits.**
  - Three-lobe brow arcs per side (amplitude 1.35) with a glabella mass.
  - Orbit depth 0.35, limited by eyelid clearance.
  - Mirrored bumps are summed, which removes the seam at the midline.
- **Nose and mouth.**
  - Broad nose: flaring 0.6, point width 0.6, hump 0.5, volume 0.4.
  - Wider mouth (0.6).
  - Shallow nasolabial groove only (0.15).
  - The mouth-corner target was dropped because it caused slits.
- **Cheeks, jaw and chin.**
  - Zygoma 2.0, cheekbones 0.6.
  - Gonion 1.5, jaw width 0.2, chin 0.7, prominent chin 0.3.
  - The MH targets are low-passed (8), which removes facets at the mouth corners.
- **Ears.** Lateral wing 0.9, slightly pointed (0.15), with a broad lobe.
  - Lateral extent is 12.65 cm, up from 10.7.
  - Length is 8.2 cm.
  - They sit compact against the skull and do not reach elf length.
- **Unchanged:** no tusks, no claws, no texture.

## 5. Hands and feet

- **Hands.**
  - Scale 1.06, broader palm (0.4), thicker fingers (0.32).
  - Knuckle relief was reduced to 0.04 and the finger-segment blend softened (0.9 cm), which removed the ring steps at the finger joints.
  - Hand length is 32.7 cm, 0.86 of the forearm.
  - The hand stays heavy and broad without reading as alien.
- **Feet.**
  - Length 40.4 cm, up from 37.1; breadth 17.3 cm, up from 15.6.
  - Toe length 0.3, splay 0.18, broader forefoot, heel extended 3 cm back, instep 0.7.
  - Plantigrade, five toes.
- **Ground.** Ground is restored to z = 0 at the soles. Stature is 217.95 cm, −0.42 mm against E3.

## 6. Joints and landmarks

- **Arm chain** (clavicle tail, upper arm, lower arm, hand, fingers): shifted +2.4 cm laterally along with the girdle.
- **Finger and toe-tip joints:** re-swept with the extremity changes. 76 joint ends moved, by at most 29.3 mm; that maximum is at the toe tips from the longer foot.
- **Trunk, pelvis, hip, knee and ankle joints:** carried unchanged.
- **Landmarks file:** `GR_U_REF_RP2_production_v004_landmarks.json`.

## 7. Topology gate (order §14)

| Check | Result |
|---|---|
| Components / boundary / non-manifold edges and vertices | 1 / 0 / 0 / 0 |
| Genus / Euler | 0 / 2 |
| Degenerate faces, duplicate faces, coincident vertices, unused vertices | 0 |
| Hidden shells | 0 (single component) |
| **Rest-pose self-intersections** | **0**: float64 design data and the stored float32 file, both quad diagonals |
| Normals | Outward; Blender volume +131.90 L |
| Quads | 100 % overall, 100 % in deformation zones |
| Zone audit with the v004 joints | Edge loops pass; creator density passes |
| T-4 quality target | Angles 45–135° 97.4 %; aspect ≤ 4 95.4 % (v003: 98.2 / 95.6). This is the cost of the larger mass change; no face is degenerate. |
| T-1, unchanged region vs H | PASS: prod→ref median / p95 / max 0.12 / 0.54 / 0.78 mm |
| Stored-file readback | 1 object, world identity, all quads, MPFB attributes present; maximum deviation 0.0001 mm from the design data |

Region deltas against v003 (mean / max, mm), from `gates/deltas_vs_v001_v002_v003.json`:

| Region | Mean | Max |
|---|---|---|
| Head and face | 3.0 | 17.4 |
| Ears | 7.2 | 22.9 |
| Neck and girdle | 11.2 | 20.4 |
| Torso | 15.0 | 35.7 |
| Hands | 21.6 | 34.9 |
| Feet | 13.0 | 26.1 |
| Limbs | 15.7 | 40.3 |

Silhouette area against v003 is +11.7 % front and +9.4 % in profile.

## 8. Deformation gate (order §15)

- **Setup:** DQS on the v004 joints, with source weights smoothed over 60 iterations and split per finger.
  - The smoothing count was re-calibrated by rerunning v003, which reproduces v003's recorded hip-flexion result: 57 pairs against 56 recorded.
  - The v003 rerun is in `gates/deform_v003_rerun.json`.
- **Suite:** 54 poses. Six were added to cover the order's girdle and pelvis items: clavicle elevation 15° (left and right), clavicle protraction 15° (left and right), pelvis tilt 10° and pelvis lateral tilt 10°.
- **Classification for the new poses:**
  - Girdle poses are measured from the shoulder end of the clavicle.
  - Pelvis poses use the 25 cm hip-region radius.

**Results:**

- 32 clean, 22 local flexion-crease contacts, **0 non-local**.
- Return to rest is exact (0.000 mm). No pose collapses.
- The v003 rerun on the same 54-pose suite: 35 clean, 19 local, 0 non-local.

| Local contact | Detail |
|---|---|
| Knee flexion 120° | Deepest contact in the suite, 5.5 mm (v003: 4.5–5.0) |
| Elbow flexion 120° | 4.3 mm |
| Hip flexion 90° | 3.3 mm, 24.7 cm from the joint |
| Shoulder flexion 60° | Local crease |
| Hip abduction 30° | Local crease |
| Hip flexion 45° | Local crease |
| Pelvis lateral tilt 10° | Local crease |
| Finger curls | Local crease |
| Toe extension 20 / 30° | 0.06 / 0.22 mm |
| Clavicle protraction (left) | 4 pairs, 0.00 mm |

- Clavicle elevation, the right protraction, pelvis tilt, every shoulder-abduction pose, wrist, ankle, neck, spine and the A-pose are clean.
- **Fixed during the build:** hip flexion at 90° was non-local (25.5–25.6 cm) in candidate v004t. The upper-thigh front depth and the lower-belly front factor were reduced until it fell inside the hip radius.

## 9. Self-review against the target image (order §16)

| # | Question | Answer |
|---|---|---|
| 1 | Front silhouette resembles the target's grounded troll rather than v003? | **Yes.** Sheet A matches the target's shoulder width (1.02), waist taper, heavy forearms and calves, and the wide girdle over long limbs. Sheet B shows the change from v003. |
| 2 | Profile has the target's torso depth and grounded abdomen-hip balance? | **Yes.** Trunk depth +15 % with real back mass; the glutes were moderated so the profile is grounded rather than soft. The target's abdomen is partly hidden by the loincloth. |
| 3 | Shoulders and neck substantial enough? | **Yes.** Shoulder span 63 cm; the neck reaches 0.98 of head width and flows from the jaw into the trapezius. |
| 4 | Arms long **and** thick? | **Yes.** Arm length is unchanged; upper arm 1.23 and forearm 1.16 of the target's thickness ratios. |
| 5 | Hands large and heavy without becoming alien? | **Yes.** 0.86 of forearm length, broad palm, thick smooth fingers, no claws; the joint ring steps are removed. |
| 6 | Thighs and calves substantial enough to support the stature? | **Yes.** 0.93 / 0.92 of the target's thickness ratios (v003: 0.84 / 0.86). |
| 7 | Feet visibly anchor the body? | **Yes.** 40 × 17 cm, broad forefoot, heel and instep. |
| 8 | Head compact and heavy, no alien elongation? | **Yes.** Head is 0.104 H, smaller than the target's 0.122. Broad jaw and cheeks, heavy brow, no vertical stretch. |
| 9 | Face reads troll-like without tusks, texture, scars or skin color? | **Yes.** Heavy brow arcs and glabella, deep-set orbits, a broad flared nose, wide cheekbones and mouth, a broad jaw. It reads somewhat milder than the textured target, because gray clay carries no skin folds or wrinkles. |
| 10 | Ears support rather than dominate? | **Yes.** Lateral, slightly pointed, compact against the skull, like the target's. |
| 11 | Still rangy and distinct from Skarn? | **Yes.** Long arms (fingertip at 0.63 H), long legs and a narrow waist are kept at 218 cm stature. Mass sits in the girdle and extremities, not in bulk. |
| 12 | Would a neutral viewer call the base body a troll-like fantasy humanoid without textures? | **Yes.** The silhouette alone carries it: wide girdle, thick neck, heavy forearms, calves, hands and feet on long limbs, big lateral ears and a heavy-browed broad face. |

Known differences that are not misses:

- The clay is smooth, without the target's muscle striation. The order allows this (§10, no bodybuilder read).
- The hands are shown open in the rest pose, while the target's are relaxed and curled.
- The cameras differ, so sheet A compares silhouette and massing, not pixels.

## 10. Comparison sheets

All sheets are in `reviews/rac-rp2-evidence/grask_v004_target_image/sheets/`:

- `sheet_A_target_vs_v004.jpg`: target vs v004, front, profile and three-quarter, matched height.
- `sheet_B_v003_vs_v004_body.jpg`: front, profile, back and three-quarter, identical cameras.
- `sheet_C_body_carriers.jpg`: neck and shoulder, chest and ribcage, torso profile, pelvis and upper thigh, arm and forearm, hand back and palm, thigh–knee–calf front and profile, foot side and top.
- `sheet_D_head.jpg`: front, profile, three-quarter, brow and orbit, nose and midface, jaw and chin, ear.
- `sheet_E_presentation.jpg`: nude neutral production presentation. Nothing is obscured.

## 11. Rebuild

1. Run `tools/ident_full.sh params_v004.json TAG`.
2. Run `ground.py`.
3. Run `f32safe.py`.
4. Export with `export_blend_v004.py` and verify with `readback_v004.py`.
5. Run the gates: `gate_topo.py`, `sxq.py` (both quad diagonals), `zone_audit.py` with `JOINTS`, `gate_ident.py`, `gate_v004_deltas.py`, and `deform.py -- … 60` with `JOINTS`.

## 12. Scope stop

v004 is not promoted. There is no canon freeze, no next race, no rig promotion, no creator implementation and no UE5 integration. Work stops here, waiting for Tyler's review.
