# RAC RP2 — Grask v005 body-form cleanup: final gate

**Status: RP2 GRASK V005 BODY-FORM CLEANUP PASS / READY FOR AUTHOR REVIEW**

- **Order:** `reviews/chatgpt-rac-rp2-grask-v005-body-form-cleanup-order.md` (83886d9).
- **Parent:** v004 (`cd8f1cdb…b2f3`).
- **Visual authority:** Tyler's grounded-troll turnaround.
- **Candidate:** `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Grask/RP2/GR_U_REF_RP2_production_v005.blend`
  - file `958af4fd35740cdd35ad8fa5b08e25fd67edf753b9f3b0ac24bdd43eebfb9a52`
  - geometry `bb8b43fd…77cb`
  - Read back from the PC: matches. The sidecar, landmarks, edit masks and MPFB mapping sit beside it.
- **Preserved** (hashes re-checked on the PC):

  | Version | SHA-256 |
  |---|---|
  | v001 | `81f579f9…9c0a` |
  | v002 | `9622a062…23ee` |
  | v003 | `46697d1b…5b52` |
  | v004 | `cd8f1cdb…b2f3` |

- **Evidence:** `reviews/rac-rp2-evidence/grask_v005_body_form_cleanup/`, with these folders:
  - `gates/`
  - `sheets/`
  - `target/`
  - `production/`
  - `tools/` (includes `params_v005.json`)

## 1. What caused the four defects

All four came from how v004's mass was applied, not from the shapes v004 was aiming for:

- **Multiplicative scaling amplified existing bumps.** v004's breadth and depth changes multiplied each vertex's own offset. Every small bump in the base surface was enlarged along with the volume: the forearm swell below the elbow, the pectoral apex, the scapular and lat mass.
- **Overlapping trunk bands created a ridge.** The four trunk bands summed to front depth ×1.48 at z 124–138. They also gave the back ×1.08 under a band of ×0.97, which made a ridge on the back.
- **The trunk bands reached into the thighs.** They also acted on 60 % of the thigh weight above z 92, which put a horizontal band across the upper thigh.
- **Point-like bumps in the relief.** The relief included three midline sternal bumps (the "keel") and a small pectoral bump. Together these made the triangular chest point.

## 2. Exact fixes to the four owner-observed defects

| Defect | Fix |
|---|---|
| **A. Upper-thigh lumpiness** | <ul><li>Removed the trunk-band thigh weight entirely.</li><li>Thigh breadth is now a PCHIP-smooth profile, measured from a low-passed copy of the surface, so base bumps are not amplified.</li><li>Breadth: 1.16 at the hip → 1.31 mid-thigh → 1.14 at the knee.</li><li>Front-to-back depth: 1.02 → 1.14, peaking at mid-thigh instead of under the groin.</li><li>The medial side is damped smoothly (0.55, a cosine blend rather than a step), so the adductor mass is continuous.</li><li>Local geometric fairing (cotangent weights) of the upper anterior thigh at the inguinal crease: the profile mound drops from 18.9 to 17.4 cm forward and joins the hip and knee cleanly.</li><li>Trochanter relief softened to 0.10 cm.</li></ul> |
| **B. Mid-back mound** | <ul><li>The trunk is now one continuous PCHIP field over z 88–182 (breadth, front depth, back depth), scaled from the low-passed primary form.</li><li>Above z 138, the back profile is retargeted 55 % toward a straight line from the mid-back to the upper back.</li><li>The lumbar is filled (back factor 1.12 at z 125), so the back flows into the pelvis.</li><li>Cotangent fairing on the scapular / lat region (both sides) and the mid-back midline.</li><li>Result: the posterolateral swell and the barrel outline in the back and rear-three-quarter views are gone; the back reads as broad planes.</li></ul> |
| **C. Triangular chest bump** | <ul><li>Removed the three sternal keel bumps and the small pectoral bump.</li><li>Added a negative midline mass at the manubrium (−2.4 cm, σ 4 × 6 × 5) and a broad flat pectoral mass on each side (+0.45 cm, σ 7 × 5 × 5.5).</li><li>Light cotangent fairing (1.2) over the pectoral field. Uniform-Laplacian fairing was tried and rejected because it left nipple cones.</li><li>The chest now reads as one broad plate with a sternal plane and a soft lower pectoral border. The midline upper chest now sits 20.7 cm forward (v004: 22.1).</li></ul> |
| **D. Arm bumps** | <ul><li>Arm breadth is now measured from a smoothed limb surface (λ 120), which removed the forearm "ball" and the outer-elbow lump.</li><li>Upper-arm profile: 1.06 at the shoulder → 1.18 / 1.16 through the humerus → 1.36 at the elbow.</li><li>The forearm starts at 1.42, so the elbow transition matches. It runs 1.58 / 1.54 through the flexor and extensor mass and tapers to 1.36 at the wrist.</li><li>Olecranon and epicondyle relief halved, so the elbow is structural rather than a knob.</li><li>Hands were not changed and stay connected to the forearm.</li></ul> |

## 3. Secondary balance changes

- **E. Abdomen.**
  - The front profile is flattened 40 % toward the line from the pubis to the chest (z 112–150).
  - The front of the abdomen sits 2.6–2.9 cm further back than in v004, and the lumbar is filled.
  - Waist depth is 25.2 cm, against the target's 27.6 and v004's 27.6. The waist is not pinched: the mass moved from a round belly into a straighter back line.
- **F. Posterior and glutes.**
  - The glute back factor was lowered to 0.97, and cotangent fairing was applied to the gluteal mass.
  - Rear projection at z 100–108 is 1.3–1.5 cm less.
  - With the lumbar filled, the pelvis-to-thigh transition reads firm rather than bulbous.
- **G. Head and neck.**
  - Head mass +5 % in breadth and depth and +4 % in height, scaled downward from the crown, so stature is unchanged. The head–neck blend is by head weight.
  - Head height / stature is now 0.108 (v004 0.104; target 0.122). This is a small step that keeps the compact head.
  - The neck-to-trapezius integration was kept; neck width / head width is 0.97.

## 4. Target-image comparison

Sheet B shows the target against v005. Ratio table (same method as v004; full table in `target/ratios.md`):

| Ratio | Target | v004 | v005 |
|---|---|---|---|
| Shoulder width / H | 0.252 | 0.258 | 0.258 |
| Waist / shoulder | 0.616 | 0.632 | 0.632 |
| Pelvis / shoulder | 0.807 | 0.780 | 0.739 |
| Hand / forearm | 0.733 | 0.755 | 0.755 |
| Head height / H | 0.122 | 0.104 | **0.108** |
| Neck / head width | 1.172 | 0.979 | 0.970 |
| Upper-arm thickness / arm length | 0.096 | 0.118 | **0.108** |
| Forearm thickness / forearm length | 0.324 | 0.376 | **0.319** |
| Thigh thickness / leg length | 0.131 | 0.122 | 0.119 |
| Calf thickness / lower leg | 0.267 | 0.245 | 0.237 |

- **Arms:** both arm ratios moved closer to the target (1.23 → 1.12 and 1.16 → 0.98). The arms are still heavy, but the mass is spread out.
- **Legs:** thigh and calf stay near v004 (0.91 and 0.89 of the target), not back toward v003's 0.84 and 0.86.
- **Pelvis:** the pelvis reads 4 % narrower because the trunk band no longer widens the hip, and it no longer bulges.
- **Torso profile:** `target/profile_vs_target.txt` compares the target's per-height torso depth and back line with v004 and v005. v005's upper-chest depth is 35.1 cm at z 164, closer to the target's 34.4 than v004's 36.1.

## 5. Defect audit (order §16)

| # | Item | Result |
|---|---|---|
| 1 | Upper-thigh lumpiness | **PASS**: one coherent mass in front and three-quarter views; clean profile (sheet C, columns 1–3) |
| 2 | Mid-back lumpiness | **PASS**: no posterolateral mound; broad planes (sheet C, columns 6–7; sheet A, back) |
| 3 | Triangular chest bump | **PASS**: no apex; broad pectoral plate (sheet C, columns 4–5) |
| 4 | Upper-arm bumpiness | **PASS**: continuous cylinder from deltoid to elbow (sheet C, columns 8–9) |
| 5 | Forearm bumps / concentrated mass | **PASS**: no ball below the elbow; mass spread from elbow to wrist (sheet C, column 10; sheet A, front) |
| 6 | Abdomen too round | **PASS**: flat, solid, not cut or pinched (sheet C, column 11) |
| 7 | Posterior / glutes too projected | **PASS**: rear projection reduced; firm pelvis-to-thigh transition (sheet C, column 12) |
| 8 | Head-to-body scale | **PASS**: small increase, compact (sheet D) |
| 9 | Neck-to-shoulder integration | **PASS**: unchanged thick neck and trapezius flow (sheet D) |
| 10 | New lumps elsewhere | **PASS**. Problems found while iterating and removed before v005: nipple cones from uniform fairing; an over-thinned waist from the first back-line retarget, which pulled the lumbar forward; thinner forearms and legs from scaling the smoothed surface, which was compensated. The final whole-body and close-up sheets show no new lump. |

## 6. Self-review (order §18)

All twelve answers are **YES**:

1. Upper thighs are free of lumpiness.
2. No mid-back mound.
3. The chest point is gone.
4. The arms are continuous and heavy.
5. Forearm mass is distributed naturally.
6. The abdomen is closer to the target without being muscular or pinched.
7. The posterior is closer to the target.
8. It reads immediately as grounded troll Grask.
9. The v004 silhouette is kept: shoulders 0.258, waist taper 0.632, long limbs, large hands and feet, ears and face.
10. No region was smoothed into generic human anatomy. Fairing is local only, and mass was redistributed rather than removed.
11. No v002 alien cues.
12. Tyler's four defects are visibly resolved in sheets A and C.

## 7. Topology and self-intersection

| Check | Result |
|---|---|
| Components / boundary / non-manifold | 1 / 0 / 0 |
| Genus | 0 |
| Degenerates / duplicates / coincident / unused vertices | 0 |
| Hidden shells | 0 |
| **Rest-pose self-intersections** | **0**: float64 data and the stored float32 file, both quad diagonals |
| Normals | Outward; +123.66 L |
| Quads | 100 % overall, 100 % in deformation zones |
| Zone audit | Loops and creator density pass |
| T-4 quality target | 97.25 % / 94.92 % (v004: 97.42 / 95.38) |
| T-1, unchanged region vs H | PASS (median 0.20, p95 0.61, max 0.91 mm) |
| Stature | 217.947 cm: −0.42 mm vs E3, 0.001 mm vs v004; ground z = 0 |
| Stored-file readback | 1 object, identity transform, all quads, MPFB attributes; 0.0001 mm deviation |

T-4 is a quality target, not a §19 requirement. Its change is −0.2 points on angles and −0.5 on aspect.

## 8. Deformation (order §20)

- **Setup:** 54 poses, DQS on the v005 joints (unchanged from v004), weight smoothing 60.
- **Result:** 31 clean, 23 local flexion-crease, **0 non-local**. Return to rest 0.000 mm. No collapse.
- **Clean poses:** shoulder abduction 45° and 90°, clavicle elevation, pelvis tilt, neck, spine, wrist, ankle and the A-pose.

Local contacts:

| Region | Pose | Depth |
|---|---|---|
| Shoulder / pec | Flexion 60° | 4.7 mm, local (v004: 2.0) |
| Clavicle | Protraction | 0.19 mm |
| Elbow | Flexion 120° | 3.1 mm |
| Hip | Flexion 90° | 3.0 mm, 21.8 cm from the joint (v004: 3.3 mm, 24.7 cm) |
| Hip | Abduction 30° | 2.1 mm |
| Pelvis | Lateral 10° | 0.9 mm |
| Knee | Flexion 120° | 4.8 mm (deepest) |
| Fingers | Curls | 2.1 mm |
| Toes | Extension | 0.2 mm |

## 9. Delta from v004 to v005 (order §21)

Edit masks are in `GR_U_REF_RP2_production_v005_edit_masks.npz`, with per-vertex displacement from v004.

| Mask | Vertices | Moved > 0.5 mm | Mean mm | Max mm |
|---|---|---|---|---|
| Thighs | 10 512 | 10 512 | 7.4 | 26.6 |
| Back | 10 132 | 9 662 | 3.7 | 14.0 |
| Chest | 10 565 | 9 806 | 5.2 | 18.4 |
| Upper arms | 9 518 | 9 443 | 2.4 | 13.0 |
| Forearms | 7 905 | 7 905 | 4.5 | 11.1 |
| Abdomen | 3 206 | 3 206 | 16.5 | 27.5 |
| Pelvis / glutes | 714 | 714 | 7.3 | 12.0 |
| Head / neck (changed) | 68 762 | 68 660 | 7.5 | 12.0 |
| Calves (leg-mass balance) | 7 448 | 7 418 | 3.2 | 7.1 |
| Hands (transition only) | 51 043 | 1 727 | 0.04 | 1.5 |
| Feet (transition only) | 34 059 | 2 698 | 0.14 | 4.3 |
| **Outside all masks** | 282 | 259 | — | **1.6** |

- Movement outside the masks is at most 1.6 mm, from smooth low-pass falloff.
- Bbox delta is at most 0.47 mm. Stature delta is 0.001 mm.

## 10. Comparison sheets

All in `reviews/rac-rp2-evidence/grask_v005_body_form_cleanup/sheets/`:

- `sheet_A_v004_vs_v005_body.jpg`: front, profile, back and three-quarter, identical cameras.
- `sheet_B_target_vs_v005.jpg`: front, profile and three-quarter at matched height.
- `sheet_C_closeups.jpg`: 12 views
  - upper thighs front and three-quarter;
  - thigh profile;
  - chest front and three-quarter;
  - mid-back and back three-quarter;
  - upper arm front and three-quarter;
  - forearm profile;
  - abdomen profile;
  - pelvis / glute profile.
- `sheet_D_head_neck.jpg`: head front, profile and three-quarter, plus neck and shoulder front and profile.

## 11. Rebuild

1. Run `tools/ident_full.sh params_v005.json TAG`, then `ground.py`, then `f32safe.py` (or `tools/v5build.sh params TAG`).
2. Export with `export_blend_v005.py` and verify with `readback_v005.py`.
3. Run the gates as in §7–9: `gate_topo`, `sxq` on both diagonals, `zone_audit` with JOINTS, `gate_ident`, `gate_v005_deltas`, and `deform … 60`.

New operators in `ident_body.py` / `ident_make2.py`:
- `trunk_field`, with back / front / side line retargets;
- `masses`;
- PCHIP limb profiles measured from a smoothed surface;
- `head_scale`;
- `local_fair` with cotangent weights (`local_fair_cot`).

## 12. Scope stop

Not promoted. No next race, canon freeze, rig promotion, creator or UE5 work. Stopping for Tyler's review.
