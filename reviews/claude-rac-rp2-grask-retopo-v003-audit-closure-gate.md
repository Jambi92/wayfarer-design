# RAC RP2 — Grask retopology v003 — thumb-web review and audit closure — gate

**Date:** 2026-10-25  
**Order:** `reviews/chatgpt-rac-rp2-grask-thumb-web-visual-review-and-audit-closure-order.md` (4d4f6e0). Parent: retopo v002 (7835e22, blend `49ae8a6e…f55e`).  
**Result:** `GR_U_REF_RP2_retopo_v003` — every required technical gate and evidence check passes on the **exported blend**.  
**Author visual approval is still pending:** this is not acceptance and not a freeze.

**Evidence:** `reviews/rac-rp2-evidence/grask_retopo_v003_audit_closure/`  
**Tools:** `tools/rac/rp/grask_retopo_v003/` (the exact sequence is in `run_v003.sh`)

## 1. Thumb–index hollow (§1) — the open author decision

Sheets in `thumb_web/`:

| Sheet | Content |
|---|---|
| TW1, TW2 | Right and left hand, isolated. Matched v005 / v002 cameras, a red arrow on the hollow, dorsal / palmar / 3/4 / thumb-side context, four close-ups, clay and wireframe (the source with its own triangle wire). |
| TW3 | Zoom on the saddle, with a retopology-only fix preview. |
| TW4, TW6 | Transverse sections through the hollow (v002 and v003). |
| TW5 | Saddle zoom: v005 / v002 / v003. |

These were displayed to Tyler first, in the conversation.

**The hollow is v005 anatomy.** It is the soft dip of the first dorsal web space, between the thumb and index metacarpals.

- It sits at (−27.2, 6.9, 94.9) cm on the right hand and (27.4, 7.4, 94.8) cm on the left.
- It is visible in the frozen source surface and in the source's own triangle wireframe (TW1/TW2 rows 1, 4 and 5).
- The sections show the source outline dipping there, with the retopology lying on top of it.

**v002 also had a retopology defect at the same place.** Its quads were unevenly spaced around the saddle pole, which shaded as faint rumples (TW3, middle column). The defect sits on top of the anatomy and does not change it.

**v003 fixes the defect, not the anatomy.**
- The fix is `relaxg.py`: a guarded tangential relaxation that keeps every vertex on the source surface.
- Within 2.5 cm of the hollow, v003 stays within 0.11 / 0.35 / 0.80 mm of the source (median / p95 / max), inside T-2.
- The rumples are gone. A faint shading variation remains at the web-floor pole on the right hand (TW5).

**v005 is unchanged.** Making the hollow shallower would be a source-anatomy change and needs Tyler's explicit approval of an illustrated proposal. **That is the remaining author decision.**

## 2. Deliverables

All files are in `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Grask/RP2/`, with copies in `evidence/production/`. After the copy, every PC file was re-staged and re-hashed and matches the cloud original.

| File | SHA-256 |
|---|---|
| `GR_U_REF_RP2_retopo_v003.blend` | `03bfe7d924ff5b8b61a4c10095af5d16ca29d41667d7f61d0abeca14e1f07ce0` (geometry `f9c4a7ac98e8…fe702f`) |
| `GR_U_REF_RP2_retopo_v003.json` (sidecar) | `808cf772dd01f13e6358fcd8bacd5f7229be66edb832025a745a64b10ba8ed5b` |
| `GR_U_REF_RP2_retopo_v003_landmarks.json` | `aafbe617260dfa67632f7fe9abe495fcbf5cacd39584ab31ae8a1ead6ec8ff09` |

- The PC copy was also re-opened in Blender. Its geometry hash is identical, and positions match the fitted mesh to 2e-5 cm.
- One mesh object `GR_U_REF_RP2_retopo_v003`, transforms identity, origin at the production origin.
- No UVs or materials. Attributes `rac_part` / `rac_zone` / `identity_loop` / `seam_proposal`, and 449 `LOOP_*` vertex groups.

**Source and provenance.**
- Frozen v005, before and after the v003 copy, on both the PC and the cloud copy: SHA-256 `7bba8d2d…52ab14`, geometry `2697929d…c1d7bc`. **Unchanged.**
- v001 and v002 on the PC were re-hashed before and after and are unchanged (v002 blend `49ae8a6e…`, sidecar `2dbd7221…`, landmarks `48887566…`; v001 blend `82c10a64…`).
- v003 is a new version; nothing was overwritten.

## 3. What changed v002 → v003

All of v002's architecture and its ×2 density are kept.

| Change | Why |
|---|---|
| Ankle fan 7 → 10 rings (`ANKPHI`) | Behind the ankle only 2 path loops crossed the ±15 mm band (§5) |
| Elbow 4 → 6 rings (`ELBR`) | One side of the right elbow had a path count of 3, against 4 required |
| One extra palm ring at the MCP row (`UPOST` 14.18) | The index MCP sat right at the band edge, at exactly 3 loops |
| Short-edge quad repair (`optfix.py`, edge-ratio objective, fold and self-intersection guards) | §4 |
| Thumb-web relaxation (`relaxg.py`) | §1 |

**Counts.** 170,466 vertices / 170,464 quads / **340,928 triangle-equivalent**.

- That is +3.6 % over v002 and −72.9 % against v001.
- Mean edges: head 3.87 / ears 2.49 / hands 2.41 / feet 2.71 / trunk 5.02 mm. Every zone is under its mean ceiling.
- Poles: 166, the same as v002.

The density study now includes v003 (`density_study/density_table.md`). The selection reasoning is the same as v002's (×1 fails; mixed was rejected), plus the support loops listed above.

## 4. Quad quality — both aspect statistics (§2)

v003 was measured on the exported blend (`reports/techx.json`, `reports/gate.json`). The two aspect statistics are separate measures and are reported separately.

| | v002 | **v003** |
|---|---|---|
| Hard-limit angle quads (<20° / >160°) | 0 | **0** (20.1° … 160.0°) |
| Aspect A = ratio of the sums of opposite edges (max) | 7.47 | **7.07** (0 quads >8) |
| Aspect B = longest edge / shortest edge (max) | 11.86 | **8.07** |
| B: quads >10 / >8 / >6 | 2 / 8 / 266 | **0 / 1 / 279** |
| Quads in 45–135° / aspect A ≤4 | 94.7 / 98.7 % | 94.5 / 99.0 % |

The audit's 8 named v002 faces are in `quad_quality/Q3_named_short_edge_faces.png` and `.json`. Each is shown in context, with the face filled and its shortest edge highlighted, beside the same place in v003.

| v002 face | Tag | Actual location | v002 ratio B | v003 worst within 6 mm |
|---|---|---|---|---|
| 14853 | toe2_l | hallux–toe-2 web floor, left (15.9, 17.4, 1.3) | 8.44 | 3.80 |
| 19204 | pinky_l | ring–pinky web floor, left, palmar (32.9, −1.0, 89.0) | 8.50 | **8.07** |
| 30301 | middle_r | index–middle web floor, right (−32.7, 5.6, 88.3) | 11.86 | 3.97 |
| 30562 | pinky_r | ring–pinky web floor, right (−33.7, −1.3, 89.0) | 8.13 | 4.75 |
| 60332 | pinky_l | ring–pinky web floor, left (32.9, −1.3, 88.9) | 11.52 | **8.07** |
| 110879 | hand_l | dorsal wrist / thumb-base strip (28.3, 4.1, 106.4) | 8.25 | 4.07 |
| 141725 | hand_l | dorsal wrist / thumb-base strip (28.5, 3.8, 107.5) | 8.26 | 3.52 |
| 153946 | pinky_r | ring–pinky web floor, right (−33.6, −1.6, 89.0) | 9.94 | 4.75 |

The region tags were checked against the actual positions. Six of the eight faces are on web floors; the two `hand_l` faces are on the dorsal wrist strip above the thumb base.

**Bounded soft exception:** one face, v003 face 62534, on the left ring–pinky web floor.
- Values: ratio B 8.07, ratio A 3.87, angles 36°–148°.
- Why it stays: the interdigital slot there is about 0.4 mm wide at the floor. Every repair that brought this face below 8 either moved one web wall through the other (rejected by the self-intersection guard) or added a fold. Attempts were made with targets 5.0, 7.0, 7.5 and 9.0; the 9.0 attempt took the second face of the pair from 10.78 to 8.07.
- The face is under the 10:1 limit, is not a hard-limit quad, and lies along the web floor, not across a joint crease.

**Other soft-target extremes** (`Q2_worst_remaining_quads.png`, `worst_quads_v003.json`):
- worst angle 21.6° / 160.0° (sacral midline);
- aspect A 7.07 (left posterior axillary fan);
- ratio B 7.91 (left ear root).

The axillary-fan strips are the approved v001/v002 shoulder fan hinge.

Repair-region crops comparing v001 and v003 are in `Q1_quad_quality_repairs.png`.

## 5. Joint loops and poles (§3)

**Loop audit on the exported blend: 69/69 pass** (`reports/loop_audit.json`; the joint passes if the closed-ring count or the minimum surface-path count meets the requirement). The path-only count, on its own, now passes at 68 joints. It still fails at `toe5_j0_l` (sides 3 / 1 / 3), where three complete rings around the toe sit inside the ±4 mm band.

Closed-ring evidence, as labelled pictures and a table, is in `ring_evidence/` and `sheets/R_ring_evidence.png`. Each joint shows every distinct closed ring in the band, its offset from the joint plane, how oblique it is, its authored tag, and the poles nearby.

| Joint | Distinct closed rings in band (required) | Path count by side | Note |
|---|---|---|---|
| Ankle L | 7 (3) | 11 / 13 / **3** / 32 | The fan rings are hinged on the front ankle crease and sweep diagonally over the heel. The heel side (posterior) was 2 in v002; with 10 fan rings it is now 3. Ring-trace failures from three start sides come from poles on the starting loop, not from missing loops. The same 7 rings are reached from the remaining side. |
| Ankle R | 7 (3) | 11 / 11 / 30 | One side is web-merged. |
| Elbow R | 7 (4) | 18 / 5 / 8 / 8 | 6 authored elbow rings plus subdivision loops. Rings are traced from all 4 sides. They are tilted relative to the forearm axis (they are perpendicular to the upper arm), which is why their extent reads ±4–5 cm along the forearm axis. |
| Toe-5 MTP L | 3 (2) | 3 / **1** / 3 | Three complete rings at −2.8 / +0.3 / +3.2 mm (forefoot_l_14 plus two subdivision loops), traced from all four sides. The single low path side is a staircase path counting only along-edges. |

**Poles:** 166 (v3 104, v5 28, v6 34), all from the authored cage.
- 0 within 2 loops of any audited crease.
- 3 inside a band but further away: thumb_mcp_l, thumb_mcp_r, toe5_j1_r.
- 0 high-valence clusters in web spaces.
- There are no density-transition poles, because the subdivision is uniform.

Labelled crops: `sheets/P_pole_audit.png`, `pole_audit/`.

## 6. Validation of the exported blend (§4)

The blend was read back into the v005 frame by `rbnpz.py`, which undoes the production translation, and audited by `finalaudit.sh`.

**Topology** (`reports/gate.json`, `reports/techx.json`, `reports/folds_flips.txt`, `reports/self_intersections.txt`)
- 170,466 V / 170,464 faces, **100 % quads**, 0 triangles, 0 n-gons.
- 0 boundary edges, 0 non-manifold edges, **0 non-manifold vertices**.
- **1 component, Euler characteristic 2, genus 0** (no hidden shells, no handles).
- 0 winding-inconsistent edges, outward normals.
- 0 duplicate faces, 0 coincident vertices, 0 degenerate faces.
- **0 self-intersection pairs, 0 folded edges (>120°), 0 flipped faces.**

**T-1 / T-2 deviation** (mm). Each row gives source → v003 and v003 → source as median / p95 / max; the v003 side samples vertices **and quad centres**.

| Zone | source → v003 | v003 → source | Limit |
|---|---|---|---|
| Head / face | 0.061 / 0.262 / 0.719 | 0.000 / 0.126 / 0.608 | T-2 0.3 / 0.8 / 1.5 |
| Ears | 0.088 / 0.312 / 0.792 | 0.000 / 0.183 / 0.577 | T-2 |
| Hand L | 0.027 / 0.161 / 1.194 | 0.000 / 0.095 / 1.062 | T-2 |
| Hand R | 0.027 / 0.157 / 1.020 | 0.000 / 0.093 / 1.253 | T-2 |
| Foot L | 0.035 / 0.163 / 1.068 | 0.001 / 0.114 / 0.576 | T-2 |
| Foot R | 0.035 / 0.159 / 1.283 | 0.001 / 0.111 / 0.560 | T-2 |
| Whole body | 0.032 / 0.167 / 1.798 | 0.000 / 0.094 / 1.253 | T-1 0.5 / 1.5 / 3.0 |

The whole-body maximum of 1.80 mm is at the left posterior axillary fold, (19.6, −5.0, 167.2), which is a T-1 zone (it was 1.56 mm in v002). The shoulder and chest identity stations agree within 0.3 mm. Local recapture attempts at the fold brought it to 1.55 mm but created hard-limit quads, so they were not used.

**T-3:** stature −0.087 mm; bbox max per axis 0.112 mm (production translation accounted for). **PASS.**

**T-6.** **30 independently measured surface landmarks: max 0.84 mm, median 0.04 mm, none >1.0 mm.** **PASS.**
- **Measured landmarks** are re-measured on the v003 surface with dense area sampling, the same method on v005.
- **Copied construction coordinates** are 44 other landmarks: exact v005 hand/foot joints and eye parameters, carried as data.
  - Their drift is 0 by construction.
  - They are **not** presented as evidence that the surface was preserved.
  - Each entry in the landmark file is marked `evidence: construction coordinate (copied)` or `independently measured on v003`.

**T-7:** IoU front 0.9962, rear 0.9962, profile 0.9955 / 0.9955, 3/4 views 0.9966–0.9967. **PASS.**

**Identity:** 20 stations, all within 0.7 mm except two.
- head_brow perimeter −2.38 mm on a 79.8 cm section (−0.3 %; the chord effect over the brow rugosity);
- head extent 0.79 mm.

**Asymmetry:** mirrored-source statistics are the same for v005 and v003 (p95 9.48 / 9.49 mm). There is no symmetrisation.

**Origin.** Pelvis root projected to the ground, applied as one rigid translation:
- translation (−0.11180, +5.72272, 0) cm in the analysis frame, (−0.001118, −0.057227, 0) m in Blender;
- re-measuring the pelvis root on the exported blend reproduces the translation to 1e-7 cm;
- stature 217.991 cm, ground u = 0 (min 0.0014 cm);
- inter-landmark distances unchanged to 2.8e-13 mm;
- bbox after: x −36.05…35.00, f −14.62…31.86, u 0.00…217.99 cm.

**Visual evidence**, with no blank panels and no occlusion (`sheets3.py` refuses any missing panel):
- `A_whole_body` with the rear-3/4 panels filled; B, C, D, F, G;
- `S1_density_visual_1..3` (v005 / v001 / v002 / v003);
- `S2_density_wire` (cage / ×1 / ×2 / v002 / v003);
- `feet/E_feet_left|right_unobstructed.png`: isolated feet, top / front / sole / lateral / medial / toe webs / nails, clay and wire;
- `webs/W_webs_left|right_hand.png`: every finger web dorsal and palmar plus the thumb web, v005 / v002 / v003.

**Visual veto: PASS.** Webs and toes read as the source. The toe-web clefts show faint streaks in the narrowest slots, as in v002.

## 7. Checklist (order §4)

| Item | Result |
|---|---|
| Frozen v005 file and geometry hashes before and after | **PASS** (PC + cloud) |
| File hashes + Blender readback of blend, sidecar, landmarks (PC copies) | **PASS** |
| Density / counts / selection rationale | **PASS** (§3, density table) |
| One component, manifold edges AND vertices, outward winding, no duplicates / degenerates / hidden shells / handles | **PASS** (genus 0) |
| Intersection / fold / flip | **PASS** (0 / 0 / 0) |
| Quad angles and both aspect statistics, bounded exceptions | **PASS** (0 hard; 1 bounded soft exception, §4) |
| 69 joint requirements and pole placement | **PASS** (69/69; ring evidence §5) |
| Bidirectional T-1 / T-2 including face interiors | **PASS** |
| T-3, T-6, T-7, identity, asymmetry in the common frame | **PASS** |
| Pelvis-root ground origin, rigid-translation consistency | **PASS** |
| Complete visual evidence, no occlusion or blank panels | **PASS** |
| v001 / v002 preserved as provenance, new version | **PASS** |
| Thumb-web images displayed first; v005 unchanged; no unapproved anatomy edit | **PASS** |

**Open author decisions:**
1. Whether the source thumb–index hollow should be softened. That would be an illustrated source proposal; no change is made without approval.
2. Visual acceptance of v003.

Not done: freeze, rig, skin, morphs, UVs / materials, LODs, UE5, any other race. Turnfall is untouched.

**STOP FOR TYLER / CHATGPT REVIEW.**
