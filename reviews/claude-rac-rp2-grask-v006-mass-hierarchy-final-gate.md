# RAC RP2 — Grask v006 mass-hierarchy correction: final gate

**Status: RP2 GRASK V006 MASS-HIERARCHY CORRECTION PASS / READY FOR AUTHOR REVIEW**

**Order and inputs**
- Order: `reviews/chatgpt-rac-rp2-grask-v006-mass-hierarchy-correction-order.md` (e0da541).
- Parent: v005 (`958af4fd…9a52`).
- Visual authority: Tyler's grounded-troll turnaround.

**Candidate:** `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Grask/RP2/GR_U_REF_RP2_production_v006.blend`
- File hash: `9f4275cc4e3477ab9f0b2786c9ece37b54098392591b3805bceaf4aec9e34f13`.
- Geometry hash: `df4fc55b…bc88`.
- Read back from the PC and matched.
- The sidecar, landmarks, edit masks and MPFB mapping sit next to it.

**Preserved versions** (hashes re-checked on the PC): v001 `81f579f9…9c0a`, v002 `9622a062…23ee`, v003 `46697d1b…5b52`, v004 `cd8f1cdb…b2f3`, v005 `958af4fd…9a52`.

**Evidence:** `reviews/rac-rp2-evidence/grask_v006_mass_hierarchy/`
- `gates/`
- `sheets/`
- `silhouette/`
- `target/`
- `production/`
- `tools/` (includes `params_v006.json`)

## 1. Why v005 was not accepted

v005 removed v004's local lumps, but it spread the mass evenly over a smooth capsule. The overlay study (§4) located the misses:

- **Head:** too short (0.108 H against 0.122).
- **Neck:** read as a column instead of a trapezius-supported unit.
- **Torso:** about 12 % too wide at the lower ribs against an untapered waist, so it had no V hierarchy.
- **Pelvis:** narrow (0.95 of target width).
- **Calves, ankles and forefoot:** light at 0.88, 0.92 and 0.79 of target.
- **Arms:** emphasis sat on the forearm rather than on the shoulder.

There was one technical cause that a ratio table hides. Limb breadth was applied before the macro low-pass, and on a thin limb the radial displacement averages out around the circumference. So the limb factors delivered only a quarter to a third of their nominal effect. v006 adds an unfiltered limb increment for that reason (§3).

## 2. Changes in v006

| Area | Change |
|---|---|
| **Head (A)** | <ul><li>Whole head-and-face block scaled down from the crown: ×1.06 in breadth and depth, ×1.10 in height. Ears and face scale with it, so there is no face-only stretch.</li><li>Head height / stature 0.108 → **0.114** (target 0.122).</li><li>Head bone and neck tail joints moved with the scale (z 200.1 → 198.2).</li><li>Ear wing 0.9 → 0.7, so the ears stay in proportion to the larger head.</li><li>Face design unchanged.</li></ul> |
| **Neck / traps (B)** | <ul><li>Neck breadth ×1.24–1.32 in width, ×1.04–1.08 in depth, so the neck is wide but not a deep column.</li><li>The neck mask now ends below the jaw (z 189). Reaching higher had pushed the throat into the chin; that version was rejected for 194 self-intersection pairs.</li><li>The mask starts lower and falls off more widely (z 168 / 10 cm ramp, 8.5 / 5 cm radius), so it blends into the shoulders. The old radius had left a "turtleneck" ledge.</li><li>Broad trapezius slopes added, plus a side-neck mass, a reduced nuchal mass and a soft submandibular hollow.</li><li>Clavicle relief halved.</li><li>Local cotangent fairing on the neck-base ring.</li></ul> |
| **Pelvis (C)** | <ul><li>Trunk breadth ×1.18 / 1.16 at z 100 / 112.</li><li>Proximal-thigh lateral increment (×1.22) on the iliac / trochanter line.</li><li>Pelvis width is now **0.99 of target** (v005 0.95).</li><li>The glutes were not re-inflated.</li></ul> |
| **Thighs (D)** | <ul><li>Unfiltered increment, smoothed-surface basis: lateral ×1.22 → 1.06 from hip to knee; depth peaks at mid-thigh (×1.30 at t 0.6–0.8).</li><li>The first depth peak sat at t 0.2–0.45 and recreated a groin mound in profile, so it was moved down. The profile now rises in one convex curve from knee to hip.</li><li>Inner thigh damped (0.5) to keep the crotch clear.</li></ul> |
| **Calves (E)** | Unfiltered increment ×1.10 → 1.30 → 1.08 in width, ×1.22 at peak in depth. Calf width 0.88 → **0.97**, ankle 0.92 → **1.04** of target. |
| **Arm chain (F)** | <ul><li>Arm chain shifted 3.1 cm (v005 2.4), so the shoulders are wider and the axilla has more clearance.</li><li>Broad deltoid cap mass added.</li><li>Upper arm 1.16 → 1.40 toward the elbow (proximal inner end kept at 1.0 for clearance in flexion).</li><li>Forearm peak moved distally (1.42 / 1.50 / 1.52 / 1.40), so the chain reads shoulder → elbow → wrist rather than a forearm ball.</li></ul> |
| **Torso (G)** | <ul><li>Ribcage-to-waist V: trunk breadth lowered at z 138–150 (×0.98) and kept under the armpit (×1.06 at z 162); side-line retarget 0.85.</li><li>Lower ribs 1.12 → **1.06** of target; waist 1.00.</li><li>Broad pectoral plate (+0.8 cm, σ 7 × 5 × 4.5) and a soft costal / epigastric transition (−0.35 cm band at z 141).</li><li>Abdomen front depth 1.18 → 1.26 at z 125, so the flat belly keeps natural mass.</li><li>No triangle, no cut abdomen.</li></ul> |
| **Feet (H)** | <ul><li>Forefoot broadened over a longer, smoother band (σ 6.5 instead of a 3.5 cm ring, which had made a bunion bump), toes elongated ×0.36, heel ×3.6.</li><li>Forefoot width 0.79 → **0.86** of target, foot length 0.169 → 0.190 H (target 0.198).</li><li>Plantigrade, five toes, no claws.</li></ul> |
| **Deformation support** | Axilla relief mass on the trunk side of the armpit (−1.1 cm, σ 2.5 × 4 × 3.5). See §8. |

## 3. Operators added

All are in `ident_body.py` and `ident_make2.py`:

- `profile_extra`: an unfiltered PCHIP limb increment on the smoothed-surface basis.
- Neck mask parameters `_neck_z0`, `_neck_ramp`, `_neck_r`, `_neck_rr`.
- `fore_sig` and `fore_shift` for the forefoot.
- `lower_face_scale`: implemented, but not used in v006 (it would stretch the face).
- Joint update for `head_scale` in `v6build.sh`.

## 4. Normalized silhouette study (order §16)

Target and mesh are normalized to equal displayed height. The front views are aligned at the midline; the mesh profile is mirrored to face left and aligned at the calf. Overlays are in `silhouette/` and sheet D: red = target only, blue = mesh only, grey = both.

"Widest run" is the trunk or limb on its own. It is the reliable measure wherever the target's arms or loincloth touch the outline.

### Front (widest run, fraction of displayed height)

| Station | Target | v005 | v006 | v006 / target |
|---|---|---|---|---|
| Head (cranium, t 0.06) | 0.102 | 0.122 (ears) | 0.101 | 0.99 |
| Neck | 0.107 | 0.096 | 0.099 | 0.92 |
| Shoulders | 0.236 | 0.238 | 0.248 | 1.05 |
| Lower ribcage | 0.154 | 0.172 | 0.163 | 1.06 |
| Waist | 0.162 | 0.166 | 0.161 | 1.00 |
| Pelvis | 0.193 | 0.183 | 0.190 | 0.99 |
| Mid-thigh | 0.067 | 0.065 | 0.069 | 1.02 |
| Knee | 0.062 | 0.063 | 0.065 | 1.06 |
| Calf maximum | 0.072 | 0.064 | 0.070 | 0.97 |
| Ankle | 0.037 | 0.034 | 0.039 | 1.04 |
| Forefoot | 0.092 | 0.073 | 0.079 | 0.86 |

- **Upper ribcage (t 0.25):** the target's arms touch the trunk there, so it is compared by full silhouette: 0.252 against 0.270.
- **Proximal thigh:** the target is hidden by the loincloth.

### Profile (depth, fraction of displayed height)

| Station | Target | v006 | Ratio |
|---|---|---|---|
| Head | 0.106 | 0.114 | 1.07 |
| Neck | 0.082 | 0.100 | 1.21 |
| Chest | 0.158 | 0.161 | 1.01 |
| Abdomen | 0.126 | 0.117 | 0.93 |
| Thigh | 0.109 | 0.098 | 0.90 |
| Calf | 0.092 | 0.092 | 1.00 |
| Foot length | 0.188 | 0.181 | 0.96 |

The glute and lumbar rows are covered by the target's loincloth back flap and are not compared.

The neck is still deeper than the target's (1.21). The target's neck is unusually slender front-to-back under a forward-set jaw. Bringing v006's neck depth further down would undo the neck–trapezius support the order asks for, so it is left wide and only moderately deep.

## 5. Target ratio table (same method as v004 / v005)

| Ratio | Target | v005 | **v006** |
|---|---|---|---|
| Shoulder width / H | 0.252 | 0.258 | 0.267 |
| Ribcage width / H | 0.149 | 0.168 | **0.158** |
| Waist / shoulder | 0.616 | 0.632 | 0.582 |
| Pelvis / shoulder | 0.807 | 0.739 | 0.748 |
| Head height / H | 0.122 | 0.108 | **0.114** |
| Neck / head width | 1.172 | 0.970 | 0.901 |
| Upper-arm thickness / arm length | 0.096 | 0.108 | 0.108 |
| Forearm thickness / forearm length | 0.324 | 0.319 | 0.319 |
| Thigh thickness / leg length | 0.131 | 0.119 | **0.126** |
| Calf thickness / lower leg | 0.267 | 0.237 | **0.250** |
| Foot length / H | 0.198 | 0.184 | **0.190** |
| Hand / forearm | 0.733 | 0.755 | 0.755 |

- **Pelvis / shoulder** fell because the shoulders widened to 1.05 of target. Absolute pelvis width is 0.99 of the target.
- **Neck / head width** fell because the head is larger. Absolute neck width rose (0.096 → 0.099), and the neck now flows into broad trapezius slopes.

These are calibration ratios. As the order requires, the build was judged on the whole silhouette, not on the table.

## 6. Self-review against the target image (order §17)

| # | Question | Answer |
|---|---|---|
| 1 | Head heavy enough? | **Yes**: larger block (0.114 H), cranium width at target, heavy brow and jaw kept |
| 2 | Neck and traps support the head? | **Yes**: wide neck with trapezius slopes into the shoulders; no collar ledge, no hunch |
| 3 | Pelvis has structural width? | **Yes**: 0.99 of target width; firm, not flared |
| 4 | Thighs closer without lumps? | **Yes**: one convex mass in front, three-quarter and profile; no groin mound |
| 5 | Calves closer without peaks? | **Yes**: 0.97 of target width, smooth taper into a sturdy ankle |
| 6 | Arm mass flows from shoulder to hand? | **Yes**: deltoid cap → upper arm → elbow → forearm, forearm peak spread distally |
| 7 | Torso has clear rib / chest / lat / abdomen hierarchy? | **Yes**: V from armpit to waist, broad pectoral plate, costal transition, flat solid abdomen |
| 8 | Feet anchor the body? | **Yes**: broader forefoot and heel, longer planted footprint |
| 9 | Front reads more like the target than v005? | **Yes** (sheets A and D) |
| 10 | Profile reads more like the target than v005? | **Yes**: deeper thigh and calf, head forward mass, flat abdomen kept |
| 11 | Three-quarter reads more like the target than v005? | **Yes** |
| 12 | v005's clean surfaces preserved? | **Yes** (sheet C) |
| 13 | v004 lumps still absent? | **Yes**: rejected along the way were a groin mound, a bunion ring and a neck-collar ledge |
| 14 | No v002 alien cues? | **Yes**: no facial stretch; head scaled as a block |
| 15 | Not a human mannequin? | **Yes** |
| 16 | Reads immediately as grounded troll Grask? | **Yes** |

## 7. Topology and self-intersection

| Check | Result |
|---|---|
| Components / boundary edges / non-manifold | 1 / 0 / 0 |
| Genus | 0 |
| Degenerates, duplicates, coincident or unused vertices | 0 |
| Hidden shells | 0 |
| **Rest-pose self-intersections** | **0** (float64 data and the stored float32 file, both quad diagonals) |
| Normals | Outward; +129.77 L |
| Quads | 100 % overall and in deformation zones |
| Zone audit | Edge loops and creator density pass |
| T-4 (quality target) | 97.18 % angles / 95.08 % aspect (v005: 97.25 / 94.92) |
| T-1, unchanged region against H | PASS: median 0.32, p95 0.59, max 0.83 mm |
| Stature | 217.947 cm (−0.42 mm against E3; −0.006 mm against v005); ground z = 0 |
| Stored-file readback | 1 object, identity transform, all quads, MPFB attributes present; 0.0001 mm deviation |

## 8. Shoulder flexion (order §19)

| | Shoulder flexion 60°: contact depth | Folded faces | Class |
|---|---|---|---|
| v004 | 2.0 mm | — | local |
| v005 | 4.72 mm | 22 | local |
| **v006** | **1.84 mm** (left) / 1.83 mm (right) | 23 | local, 14.4 cm from the joint |

- **Where the contact is:** inside the armpit, where the chest wall meets the inner arm (x 19, z 164).
- **How it was fixed:** an axilla relief mass on the trunk side, plus the wider arm chain (3.1 cm).
- **Tradeoff checked:**

  | Arm-chain shift | Contact depth | Shoulders |
  |---|---|---|
  | 3.4 cm | 0.87 mm | 1.07 of target |
  | 2.8 cm | 2.1 mm | — |
  | **3.1 cm (chosen)** | **1.84 mm** | 1.05 of target |

  The 3.1 cm setting keeps the contact below v004 and the shoulders at 1.05.
- **Folded faces:** 23 against v005's 22. Practically the same; these are the axilla seam-patch faces.

## 9. Full deformation (54 poses, DQS on the v006 joints, weight smoothing 60)

- **Result:** 35 clean, 19 local flexion-crease contacts, **0 non-local**. Return to rest is 0.000 mm. No collapse.
- **Clean:** shoulder abduction 45° and 90°, shoulder extension, clavicle elevation and protraction (0.0 mm), neck, spine, wrists, ankles, pelvis tilt and the A-pose.

Local contacts:

| Pose | Depth | Distance from joint |
|---|---|---|
| Shoulder flexion 60° | 1.8 mm | 14.4 cm |
| Elbow flexion 120° | 3.7 mm | 11.6 cm |
| Hip flexion 45° / 90° | 1.6–1.9 / 3.0–3.1 mm | 22.9 cm |
| Knee flexion 120° (deepest) | 5.4 mm | 22.7 cm |
| Pelvis lateral 10° | 1.3 mm | 22.5 cm |
| Finger curls | 1.9 mm | — |
| Toe extension | 0.17 mm | — |

## 10. Delta from v005 to v006 (order §21)

Masks are assigned by dominant skin weight, so every vertex falls in exactly one region. They are saved in `GR_U_REF_RP2_production_v006_edit_masks.npz` with per-vertex displacement.

| Mask | Vertices | Moved > 0.5 mm | Mean mm | Max mm |
|---|---|---|---|---|
| Head | 65 253 | 65 220 | 10.3 | 21.6 |
| Neck / traps | 8 359 | 8 299 | 8.1 | 17.9 |
| Shoulders | 291 | 291 | 7.0 | 8.5 |
| Torso | 15 604 | 14 942 | 4.7 | 10.9 |
| Pelvis | 3 685 | 3 602 | 3.1 | 7.8 |
| Upper arms | 9 826 | 9 807 | 7.1 | 12.5 |
| Forearms | 7 909 | 7 909 | 7.0 | 7.8 |
| Hands (rigid arm-chain shift) | 51 059 | 51 059 | 5.9 | 7.1 |
| Thighs | 10 653 | 10 547 | 6.6 | 22.8 |
| Calves | 7 448 | 7 448 | 5.2 | 10.6 |
| Feet | 34 059 | 33 400 | 5.2 | 13.6 |
| Deformation support (axilla; overlaps torso and upper arms) | 2 639 | 2 618 | 4.6 | 8.1 |
| **Outside all masks** | 0 | 0 | — | — |

- Bounding-box change: ±6.7 mm laterally (arm-chain shift), +8.2 mm forward (feet).
- Stature change: −0.006 mm.

## 11. Comparison sheets

All in `reviews/rac-rp2-evidence/grask_v006_mass_hierarchy/sheets/`:

- `sheet_A_target_vs_v006.jpg`: target against v006 at matched height (front, profile, three-quarter).
- `sheet_B_v005_vs_v006_body.jpg`: front, profile, back and three-quarter with identical cameras.
- `sheet_C_mass_hierarchy_closeups.jpg`: 15 close-ups:
  - head / neck front and profile;
  - shoulder / chest front and three-quarter;
  - torso profile;
  - pelvis front and profile;
  - thigh front and three-quarter;
  - calf front and profile;
  - arm front and three-quarter;
  - foot top and profile.
- `sheet_D_silhouette_study.jpg`: normalized front and profile overlays, v005 and v006 against the target. The tables are in `silhouette/`.

## 12. Rebuild

1. Run `tools/v6build.sh params_v006.json TAG`. This runs `ident_full`, ground, f32safe, the head-joint update and the self-intersection check on both diagonals.
2. Export with `export_blend_v006.py`, then read back with `readback_v006.py`.
3. Run the gates as in §7–10: `gate_topo`, `zone_audit` with JOINTS, `gate_ident`, `gate_v006_deltas`, `deform … 60`, `v6sil.py`.

## 13. Scope stop

v006 is not promoted. There is no canon freeze, next race, rig promotion, creator or UE5 work. Work stops here for Tyler's author review.
