# RAC RP2 — Grask 3D anatomical-source rebase — final gate

**Date:** 2026-10-23
**Order:** `reviews/chatgpt-rac-rp2-grask-3d-source-rebase-order.md` (commit 224e33b)
**Status:** **RP2 GRASK 3D ANATOMICAL SOURCE REBASE COMPLETE / READY FOR AUTHOR REVIEW**

This is an anatomical source only, not a production cage. v001–v006 are preserved unchanged. No v007, rig, creator morphs, UE5 or next race.

## 1. Deliverables

| Item | Location | SHA-256 |
|---|---|---|
| Source blend | `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Grask/RP2/SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v001.blend` | `2315d5c10b166a2af0345c7a69ab6202d4e70d2c492722c0a27041c2a4e3cf86` (PC readback matches) |
| GLB provenance copy | same folder, `GR_U_REF_RP2_SOURCE_3D_v001.glb` | `8db2970f61a980702d02dfb205324432639dd3c57dc81b9f19b1ca279777a94d` |
| Geometry hash (Blender co float32 + loop indices) | — | `2bd7712615a8984df1fc424eb9ba08776a3c9925e797ba4ef1a8601c2bf5ecb9` |
| Sidecar | `…SOURCE_3D_v001.json` (repo copy in `production/`) | `4a4df94f…5b07` |
| Reconstruction masks | `…SOURCE_3D_v001_reconstruction_masks.npz` (repo copy in `production/`) | `ec7434be…0525` |
| Repo GLB copy | `reviews/rac-rp2-evidence/grask_3d_source_rebase/source_copy/GR_U_REF_RP2_SOURCE_3D_v001.glb.gz` | `9434da0d…07d2` |
| Evidence | `reviews/rac-rp2-evidence/grask_3d_source_rebase/` | sheets A, B, C1–C3, D; silhouette; raw extraction; production records; tools |

The Blender object is `GR_U_REF_RP2_SOURCE_3D_v001`, in metres, Z-up, ground at z = 0, facing −Y. Blender readback deviates from the build array by at most 0.0001 mm.

## 2. Provenance

- **Uploaded GLB:** Tyler's `Downloads/base.glb`, sha256 `363b4566…93ce9`. It holds one mesh with three connected generated figures: 499,982 welded vertices and 1,000,000 triangles, untextured, y-up.
- **Extracted figure:** the left/front-derived figure, taken as the connected component with the most negative x.
  - 157,442 welded vertices (196,873 split) and 314,892 triangles.
  - These counts are identical to ChatGPT's dense `GRASK_front_reference_extracted_v3.glb` (196,873 V / 314,892 tris, `03aed1aa…`), so the full-detail source was used, not the proxy.
- **Repo proxy:** `assets/rac/rp2/grask/reference/GRASK_front_reference_proxy_v001.glb.gz` is **corrupt in the repo**.
  - gzip reports a CRC error.
  - The file hash is `c313a08f…`; the README states `b22eea7e…`.
  - It was not needed. Flagged for ChatGPT/Tyler to re-upload if the proxy matters for future work.
- **Turnaround:** `Troll Character Turnaround Sheet.png`, sha256 `3e061b0c…f4ef`. It is pixel-identical to the v004–v006 target image.

## 3. Scale (uniform only)

| Quantity | Value |
|---|---|
| Original generated height | 1.89825 m |
| Original bbox (m, glTF y-up) | [−0.787, 0.000, −0.198] – [−0.156, 1.898, 0.243] |
| Initial uniform scale | ×1.148428 → 218.000 cm |
| Re-normalisation after cleanup | ×0.998446 (cloth/tie removal and head yaw changed the top/bottom extremes), then ×1.000196 (after the scalp clean) |
| Net uniform factor | ≈ ×1.14687 |
| Final height | **218.000 cm** |
| Final bbox (cm; x = left, f = forward, u = up) | [−37.10, −20.50, 0.00] – [34.96, 27.29, 218.00] |

No non-uniform scaling was used anywhere.

## 4. Alignment and asymmetry

- **Global alignment:**
  - The generated figure stood yawed −8.25° and rolled −0.39° relative to its own bilateral plane, which was found by reflection-distance minimisation.
  - Both were removed with a rigid rotation.
  - The symmetry residual afterwards is 0.88 cm RMS, almost all in the legs/feet stance.
- **Head:** the head sat ~1.36° yawed against the torso, which is generation asymmetry. It was corrected by a rigid yaw about the neck, blended over the neck (≤ 5.7 mm move; recorded in `head_alignment_move_mm` and `headfix.json`).
- **Full mirror symmetrisation was tried and rejected.** It injected noise and created 44 self-intersection pairs.
- **Intentional asymmetry preserved:**
  - a residual natural stance difference of about 0.5–0.7 cm per region in the legs and feet (the weight distribution of the generated pose);
  - slight left/right differences in finger curl.

  These are small enough for a creator-morph baseline. A mirror pass can be applied at production retopology if Tyler wants exact bilateral symmetry.

## 5. Cloth and artifact removal (hidden-anatomy reconstruction)

The loincloth, its front and back flaps, the side ties and the knots were fused into the body volume by the generator. A thin-shell test could not separate them, so the band was replaced:

1. **Cut:** removed the trunk/leg band between z 87 and 135 cm from the source. This removed all cloth, flaps, ties and knots; genus went 3 → 0.
2. **Donor:** took the v006 production pelvis (neutral MPFB anatomy) for the same z range and coarse-fitted it per height to the source's section loops above and below the band (z 87 / 135).
3. **Fine fit:** a screened offset field matched the donor to cloth-free source skin (λ 400; valid-region weight 10, seam weight 100).
4. **Stitch:** zippered the donor to the source at its 3 boundary loops (waist and two legs), with donor loop vertices snapped to the source loops.
5. **Seam fair:** uniform-Laplacian region fair (λ 20, 3 iterations).
6. **Upper-anterior-thigh mound:** the donor carried this lump. It was flattened with paired negative normal masses at (±11.5, 13, 103) cm, amplitude −2.6 cm, followed by a light fair.

The result is a neutral, non-explicit pelvis that is continuous with the source's thighs, glutes and abdomen. No genital detail was invented.

- Masks: `pelvis_donor_reconstruction` (11,993 vertices), `seam_fair_weight`, `thigh_mound_flatten_weight`.
- v006 provided the **local pelvis geometry only**. It is not a shape authority: the donor was fitted to the source, not the reverse.

**Floating fragments, duplicate patches and holes:** none survive. The figure is a single component with 0 boundary edges, 0 duplicate faces and 0 coincident vertices (§8).

**Profile silhouette note:** in the profile overlay the target pelvis is deeper than the source (front 0.88, glute 0.62). That extra depth is the loincloth's front and back flaps in the turnaround, not body anatomy, so it is not a deficit.

## 6. Musculature neutralisation (race baseline, mass preserved)

Band-pass attenuation was used so that low-frequency mass is untouched:

- band = (X − cotsmooth(X, λ)) − lowpass(·, 100 cm²), with fine λ 0.4 cm² and medium λ 6 cm².

| Region | Fine band | Medium band |
|---|---|---|
| Body (abs, pec cuts, deltoid striation, arm grooves, tertiary ridges) | ×0.3 | ×0.3 |
| Face | ×0.6 (wrinkles softened; brow, orbit, nasal base and jaw block kept) | ×1 |
| Ears | ×1 | ×1 |
| Feet | ×1 | ×1 |
| Hands | ×0.35 (veins and surface noise) | ×0.9 |

- **Contact protection:** a contact-protection mask is grown automatically, iterating until 0 self-intersections. It protects the ear roots and the hand-to-thigh contacts (`neutralize_contact_protection`).
- **Move:** mean 2.15 mm, p95 5.38 mm, max 15.15 mm (`neutralize_move_mm`).
- **Scalp and ears:** the cranium and the area behind the ears were cleaned of generator pits (fine band ×0.85 on the scalp, ×0.4 on the ears; face untouched). Max move 5.9 mm; mask `scalp_ear_noise_clean_weight`.

Structural ribcage, shoulder, neck/trapezius, limb, hand, thigh and calf masses are retained (§9 silhouette).

## 7. Head, hands and feet

- **Head:**
  - compact, heavy troll head;
  - heavy brow and orbit, broad nasal base, substantial cheek and jaw block, grounded chin;
  - no tusks, no underbite.
- **Ears:** robust, lateral and modestly pointed, set at the head's sides. They are non-human but not elven. See sheet C1.
- **Hands:**
  - five fingers per hand, separated, with a continuous palm and an integrated thumb;
  - ordinary nails, no claws;
  - large and tool-compatible.

  Inspection found no fused digits or stray fragments, so no topology repair was needed; only surface noise and veins were reduced.
- **Feet:**
  - plantigrade, five separated toes, ordinary nails;
  - heel and forefoot continuous, with a planted broad forefoot.

  The sole view (sheet C2) shows no fused toes or fragments.

## 8. Technical evidence (from Blender readback)

| Check | Result |
|---|---|
| Vertices / triangles | 134,608 / 269,212 |
| Components | 1 (one body; no other generated figure) |
| Boundary edges / non-manifold edges | 0 / 0 (watertight) |
| Euler / genus | 2 / 0 |
| Degenerate faces / coincident vertices / duplicate faces | 0 / 0 / 0 |
| Normals | consistent; outward (signed volume +131.62 L in the Blender frame) |
| Self-intersections (triangle–triangle, non-adjacent) | **0 pairs** |
| Edge length (cm) | median 0.515, min 0.017, max 2.64 |
| Height | 218.000 cm |
| Bbox (cm) | [−37.10, −20.50, 0.00] – [34.96, 27.29, 218.00] |

**Reconstruction masks** (npz, per vertex):

- `pelvis_donor_reconstruction`
- `seam_fair_weight`
- `neutralize_contact_protection`
- `thigh_mound_flatten_weight`
- `head_alignment_move_mm`
- `neutralize_move_mm`
- `scalp_ear_noise_clean_weight`
- `scalp_clean_move_mm`

## 9. Silhouette against the target (normalised to height)

Source data: `silhouette/sil_src_table.json`; overlays in `sil_src_front.png` and `sil_src_profile.png`.

**Front, widest run (mesh ÷ target):**

| Station | Ratio |
|---|---|
| Head | 1.06 |
| Neck | 1.04 |
| Shoulders | 1.04 |
| Upper ribs | 1.04 |
| Lower ribs | 1.04 |
| Waist | 1.03 |
| Pelvis | 1.04 |
| Mid-thigh | 0.99 |
| Knee | 0.98 |
| Calf | 1.04 |
| Ankle | 0.92 |
| Forefoot | 0.99 |

- The proximal-thigh station is excluded because the target's loincloth bridges the legs at that height.

**Profile:**

| Station | Ratio |
|---|---|
| Head | 1.01 |
| Neck | 1.09 |
| Chest | 0.91 |
| Abdomen | 0.88 |
| Thigh | 0.96 |
| Calf | 0.96 |
| Foot | 1.08 |

- Glute (0.62) is loincloth-flap depth in the target.
- Chest and abdomen read slightly shallower than the painted turnaround. The generator itself produced this depth from the same image, and it was not altered: the order says to preserve the source's relationships rather than tune them toward a single painted view.

## 10. Self-audit (order §11)

**Source integrity — PASS**
- One body, with no geometry from the profile or three-quarter figures.
- No cloth or floating garbage.
- No duplicate shells.
- Watertight, genus 0, 0 self-intersections.
- 218.000 cm.

**Identity — PASS**
- In neutral clay it reads immediately as a troll: compact heavy head, brow and nasal block, lateral non-human ears, long heavy arms, big hands and feet.
- It is not human, not alien (no elongation) and not a generic bulky orc (no tusks, no underbite, no bodybuilder bulk).

**Body hierarchy — PASS**
- The head is heavy, and the neck and trapezius support it.
- Ribcage → waist → pelvis is coherent, with the reconstructed pelvis continuous.
- The arms stay long and substantial, and the hands large and functional.
- The thighs and calves stay strong (front 0.99–1.04 of target).
- The feet anchor the body (forefoot 0.99, foot depth 1.08).

**Surface — PASS**
- No scan or generator noise remains.
- The scalp pits, abdominal etching and the donor's thigh mound have been removed.
- No tertiary bodybuilder definition remains.
- It is not over-smoothed: knee, ankle, clavicle, ribcage and facial planes are all retained.

## 11. Evidence index (`reviews/rac-rp2-evidence/grask_3d_source_rebase/`)

**`sheets/`**
- `sheet_A_source_views.jpg`: front, left profile, back, three-quarter front L and R, three-quarter back.
- `sheet_B_target_vs_source.jpg`: target vs source at front, profile and three-quarter.
- `sheet_C1_face_ears.jpg`: face front, profile and 3/4; ears.
- `sheet_C2_hands_feet.jpg`: hands, feet and sole.
- `sheet_C3_body_details.jpg`: neck/shoulders, chest/ribcage, pelvis/thigh (reconstructed region), calf/ankle.
- `sheet_D_v006_vs_source.jpg`: optional historical comparison.

**Other folders**
- `silhouette/`: overlays and the width/depth table.
- `raw_extraction/`: the raw extracted figure before cleanup, including the cloth band and fused ties, for comparison.
- `production/`: sidecar, topology, PC hashes, masks, `scale.json`, `align.json`, `headfix.json`, `scalp_rescale.json`.
- `source_copy/`: gzipped GLB of the source.
- `tools/`: all build and audit scripts.

## 12. Preservation and stop

- The v001–v006 production blends and sidecars on the PC are unchanged; their hashes are listed in `production/pc_hashes.txt`.
- v001–v006 repo evidence is untouched.

Per order §14: **STOP.** The next step is Tyler's visual review of the source. Production retopology resumes only after author approval.

**RP2 GRASK 3D ANATOMICAL SOURCE REBASE COMPLETE / READY FOR AUTHOR REVIEW**
