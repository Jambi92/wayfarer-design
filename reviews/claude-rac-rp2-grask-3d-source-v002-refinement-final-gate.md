# RAC RP2 — Grask 3D anatomical source v002 refinement — final gate

- **Date:** 2026-10-23
- **Order:** `reviews/chatgpt-rac-rp2-grask-3d-source-v002-refinement-order.md` (63d7dde)
- **Parent:** source v001, `reviews/claude-rac-rp2-grask-3d-source-rebase-final-gate.md` (c068533)
- **Status:** **RP2 GRASK 3D ANATOMICAL SOURCE V002 REFINEMENT PASS / READY FOR AUTHOR REVIEW**

v002 is an anatomical source, not a production cage. Source v001 and RP2 production v001–v006 are preserved unchanged. No v007, retopology, rig, creator morphs, UE5 or next race.

## 1. Deliverables

| Item | Location | SHA-256 |
|---|---|---|
| Source v002 | `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Grask/RP2/SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v002.blend` | `0651765f1edbaa70b843e21d702ef8255257fc8644c747b04557d0567119755a` (PC readback matches) |
| GLB copy | same folder, `…_v002.glb` | `4940665952ab427c67b221b696363aebbe77243495ec6f0dad170a75b65592ca` (PC readback matches) |
| Geometry hash | float32 co + loop indices | `01f09fc0e3deaea0bcc9f6ed6ace0b49b800f80e990675de76da4674e290c2ea` |
| Sidecar | `…_v002.json` (repo copy: `production/`) | `9ce1c871…1593` |
| Moved-region masks | `…_v002_refinement_masks.npz` (repo copy: `production/`) | `6e118dc6…8cc6` |
| Repo GLB copy | `reviews/rac-rp2-evidence/grask_3d_source_v002_refinement/source_copy/…_v002.glb.gz` | `888ec98d…0d20` |
| v001, unchanged | `…/SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v001.blend` | `2315d5c1…cf86` (re-verified) |

Blender readback deviates from the build array by at most 0.0001 mm.

## 2. What changed from v001

All steps are in `tools/refine2.py` (driven by `production/refine_params_v002.json`), plus `tools/ear_transplant.py`.

1. **Ears (D).**
   - v001's right ear has a full helix rim, antihelix, conchal bowl, lobe and posterior attachment. The left ear was an under-formed generator blob.
   - The left ear was replaced by a mirrored copy of the right ear's geometry, cut on the scalp ring around the ear root and zippered into the hole (58- and 60-vertex loops). The boundary offset was diffused inward and the seam faired.
   - The ears are now an intentional, symmetric pair: robust and modestly non-human, not elf-like.
   - Mask: `ear_transplant_mask` (837 vertices).
   - Shrink-wrapping the left ear onto the mirror (`ear_mirror.py`) was tried and rejected: it could not pull vertices into the conchal bowl.
2. **Symmetry of major masses (§13).**
   - Head, torso and pelvis were averaged with their own mirror image. The mirror displacement was smoothed (λ 25) so only primary masses move, not features.
   - Hands, legs, feet and ears are excluded.
   - Move: p95 0.9 mm, max 4.5 mm.
   - A full face mirror average (`head_sym.py`) was tried and rejected because it blurred the eyes and brow, which belong to the individual character of the face.
   - One local generator bulge on the left temple was mirrored from the right side (max 7.0 mm).
3. **Pelvis, glute and upper thigh (F).**
   - The reconstructed pelvis was flat behind: the glute line sat about 3 cm forward of both the hamstrings and the lumbar back.
   - Paired glute masses were added with a sharper lower edge to form the gluteal fold, and the cleft was kept.
   - Posterior surface at x = 8 cm:

     | Height | v001 | v002 |
     |---|---|---|
     | z 108 | −9.9 cm | −12.3 cm |
     | z 116 | −11.5 cm | −14.6 cm |
     | z 100 (fold) | −9.7 cm | −9.7 cm |

   - The glutes now sit flush with the lumbar back (−14.7 cm). They are not over-rounded, and there is no fashion-model hip.
   - Max move 4.3 cm (`glute_move_mm`).
4. **Neutral cleanup in three bands** (fine λ 0.4, medium λ 6, large λ 30 cm²). The large-scale mass is untouched (low-pass at 100 cm²). Fraction of each band kept:

   | Region | Fine | Medium | Large |
   |---|---|---|---|
   | General body / limbs | 0.30 | 0.80 | 1.0 |
   | Torso / back | 0.20 | 0.60 | 1.0 |
   | Pelvis | 0.20 | 0.45 | 1.0 |
   | Hands | 0.15 | 0.50 | 1.0 |
   | Fingers | 0.30 | 0.85 | 1.0 |
   | Foot dorsum | 0.20 | 0.25 | 1.0 |
   | Toe tips | 0.60 | 1.0 | 1.0 |
   | Face | 0.50 | 0.90 | 1.0 |
   | Ears | 0.60 | 1.0 | 1.0 |

   This removes rib cuts, sternal and serratus etching, scapular and spinal scan lumps, and dorsal hand and foot veins and tendons. Pectoral mass, clavicle plane, ribcage, scapular plane and knuckle rhythm stay as secondary forms.
   - Torso settings were tuned over three passes. The first (torso 0.1/0.15/0.65) over-smoothed the chest into a mannequin and was backed off.
5. **Cheek (C):** the generator crease under the left zygoma was faired into a clean cheek hollow (`cheek_fair_weight`).
6. **Fingers (A):** a radial +1.2 mm finger mass so the digits are not delicate (`finger_inflate_mm`).
7. **Scale:** ground at z = 0, then a uniform rescale ×1.001353 back to **218.000 cm**.
8. **Contact protection:** grown automatically until there are 0 self-intersections. It covers 1,717 vertices at the finger contacts (`contact_protection`).
   - A masking bug was found and fixed during the audit: the hand region had leaked into the outer toes, which were inflating and colliding.

## 3. Technical evidence (Blender readback)

| Check | v002 |
|---|---|
| Vertices / triangles | 134,753 / 269,502 |
| Components | 1 (one body) |
| Boundary / non-manifold edges | 0 / 0 (watertight) |
| Euler / genus | 2 / 0 |
| Degenerate / coincident / duplicate | 0 / 0 / 0 |
| Cloth, debris, duplicate shells, open holes | none |
| Normals | consistent, outward (+130.59 L; v001 131.62 L, −0.8 % from removing tertiary convexity) |
| Self-intersections (non-adjacent triangle pairs) | **0** |
| Edge (cm) | median 0.504, min 0.015, max 2.65 |
| Height | **218.000 cm** (no stature drift) |
| Bbox (cm) | [−36.78, −20.36, 0.00] – [34.75, 27.22, 218.00] |

**Moved-region masks** (npz, per vertex):

- `symmetry_move_mm`
- `mirror_spot0_move_mm`
- `glute_move_mm`
- `neutral_v2_move_mm`
- `cheek_fair_weight`
- `finger_inflate_mm`
- `ear_transplant_mask`
- `ear_seam_fair_weight`
- `contact_protection`

**Silhouette against the target** (`silhouette/sil_v002*`).

Front, widest-run ratio (v002 vs v001):

| Station | v002 | v001 |
|---|---|---|
| Head | 1.04 | 1.06 |
| Neck | 1.03 | 1.04 |
| Shoulders | 1.04 | 1.04 |
| Upper ribs | 1.04 | 1.04 |
| Waist | 1.02 | 1.03 |
| Pelvis | 1.04 | 1.04 |
| Mid-thigh | 0.98 | 0.99 |
| Knee | 0.98 | 0.98 |
| Calf | 1.03 | 1.04 |
| Ankle | 0.88 | 0.92 |
| Forefoot | 0.98 | 0.99 |

Profile ratio:

| Station | v002 | v001 |
|---|---|---|
| Chest | 0.90 | 0.91 |
| Abdomen | 0.88 | 0.88 |
| Glute | 0.73 | 0.62 |
| Thigh | 0.93 | 0.96 |
| Calf | 0.95 | 0.96 |
| Foot | 1.06 | 1.08 |

- The profile "thigh" station lies at hand height, so its run includes the hanging hand, whose palm and dorsum were cleaned. Measured directly, thigh depth is unchanged within 1 mm at z 80 / 86 / 92 / 98 on both legs. The thigh mass is preserved.
- The target glute still includes the loincloth flaps.

## 4. Symmetry and asymmetry record

- **Made symmetric:**
  - ears (mirrored pair);
  - head, torso and pelvis primary masses (half-way mirror averaging, smoothed);
  - left temple bulge.
- **Intentionally retained:**
  - the natural leg and foot stance difference (about 0.5–0.7 cm per region);
  - left/right finger curl (the hands are posed differently, and mirroring would break the contact-free rest pose);
  - small facial individuality: brow and eye fine form were not mirror-averaged, because doing so blurred the face.

## 5. Internal visual audit (order §15)

| # | Item | Result |
|---|---|---|
| 1 | Hands no longer look human or melted | **PASS.** Dorsal veins and tendons removed; large palm and metacarpal block; clean digits with no webbing (C2a, D2). |
| 2 | Thumbs integrate naturally | **PASS.** Thenar root continuous with the palm; the thumb sits forward and medial in an opposable rest pose (C2a thumb close-ups). |
| 3 | Fingers have coherent taper and spacing | **PASS.** Four fingers with even base spacing and tip taper; +1.2 mm mass so they are neither delicate nor sausage-like. |
| 4 | Feet are broad, planted and anatomically clean | **PASS.** Dorsal vein and tendon lumps gone; broad forefoot, arch, heel mass and sole continuous (C2b). |
| 5 | Toes are properly separated and hierarchical | **PASS.** Five separated toes, hallux dominant, ordinary nails, no fusion (C2b toe close-ups). |
| 6 | Face preserves troll identity | **PASS.** Same stern, heavy individual: brow block, broad nasal base, jaw block, grounded chin, no tusks (C1, D2). |
| 7 | Brow, nose, cheek and jaw transitions are coherent | **PASS.** Wrinkles softened; zygoma crease faired into a cheek hollow; nose bridge and nasal base kept. Remaining dark areas on one side of the head are the studio light, checked by rendering the mirrored mesh. |
| 8 | Ears are intentional and non-human without becoming elf-like | **PASS.** Helix, antihelix, concha, lobe and posterior attachment on both ears; robust and modestly pointed (C1). |
| 9 | Torso is structurally clear without bodybuilder definition | **PASS.** Rib and serratus cuts and sternal etching removed; pectoral mass, clavicle plane and ribcage retained (C3). |
| 10 | Pelvis, glute and thigh transitions are unified | **PASS.** Glute mass and fold added; lower abdomen to pelvis and adductor origin continuous; no segmented thigh (C3, D2, A back view). |
| 11 | Back planes are clean and free of scan lumps | **PASS.** Trapezius, scapular and lat planes read; spinal and scapular scan lumps removed; lower-back taper kept with no hump (C3). |
| 12 | No regression toward the rejected v001–v006 morphology | **PASS.** Every front silhouette ratio within 0.04 of v001; same mass hierarchy (D). |
| 13 | Neutral-clay silhouette still reads immediately as Grask | **PASS** (A, B). |
| 14 | Useful as a race baseline rather than one muscular individual | **PASS.** Tertiary definition removed; primary and secondary forms carry the species. |

## 6. Evidence (`reviews/rac-rp2-evidence/grask_3d_source_v002_refinement/`)

**`sheets/`**
- `sheet_A_v002_turnaround.jpg`: front, left profile, back, 3/4 front left and right, 3/4 back.
- `sheet_B_target_vs_v002.jpg`: target vs v002 at front, profile and 3/4, matched height.
- `sheet_C1_face_ears.jpg`: face front, profile and 3/4; ear profile, 3/4 and from behind.
- `sheet_C2a_hands.jpg`: palm, dorsal, outer, 3/4, thumb-root close-ups.
- `sheet_C2b_feet.jpg`: front, both sides, 3/4, heel, sole, toe close-ups.
- `sheet_C3_body_details.jpg`: neck/shoulders, chest/ribcage, torso profile, upper back, back 3/4, pelvis front and profile, glute 3/4, upper thigh, calf/ankle.
- `sheet_D_v001_vs_v002.jpg`: identical cameras at front, profile, back and 3/4.
- `sheet_D2_v001_vs_v002_details.jpg`: refinement close-ups with identical cameras.

**Other folders**
- `silhouette/`: overlays and the station table.
- `production/`: sidecar, topology, masks, parameters.
- `source_copy/`: gzipped GLB.
- `tools/`: everything used, including the rejected `ear_mirror.py` and `head_sym.py`.

## 7. Stop

Per order §17 and §19: **STOP.** v002 awaits Tyler's approval. Production retopology resumes only after the source is approved.

**RP2 GRASK 3D ANATOMICAL SOURCE V002 REFINEMENT PASS / READY FOR AUTHOR REVIEW**
