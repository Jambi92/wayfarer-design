# RAC RP3 — Vael final consolidation / validation / freeze report

Order: `reviews/chatgpt-rac-rp3-vael-final-consolidation-freeze-order.md` (db01617).
Evidence: `reviews/rac-rp3-evidence/vael_rp3_final/`. Visual package: `vael_rp3_final/sheets/VA_FINAL_01..20` plus `18b`.
Records:
- `VAEL_FINAL_gates.json`
- `VAEL_FINAL_deformation_summary.json`
- `VAEL_RP3_freeze_readback.json`
- `VAEL_RP3_FREEZE_CANDIDATE.json`

## RESULT

## VAEL FINAL CONSOLIDATION NEEDS AUTHOR DECISION

Every gate passes except one Standard v1 deformation row. Configuration 1 `neck_rot45` adds **one fold** that the VF2 family realization does not have. It is a dihedral that crosses 120° on two sub-millimetre left cuff quads at the lobe junction. There is no flip, no contact and no root inversion. This item is new and outside the registered class (§18: "any new deformation excess outside that registered class requires review").

The order forbids fixing it here:
- The RI3 arrays must equal the reviewed candidate.
- Ear rigging is out of scope.

Everything else is ready to freeze by record:
- The production files are written to E:.
- The files were read back byte-identical.
- The validator was recomputed from the read-back: 69 / 69 on both configurations.

`VAEL_RP3_FREEZE.json` is therefore **not** written. The complete record is held as `VAEL_RP3_FREEZE_CANDIDATE.json`. On acceptance it becomes the freeze record unchanged, with no rebuild and no resave.

## Open item — c1 neck_rot45 cuff fold (sheet 18b)

**Where:**
- Faces 57125 / 57126, left side, part `cuff`.
- Position in the root frame: b −0.4, u −2.4, n +0.7 cm. This is the lobe-to-cheek junction.
- Edge lengths are 0.14–1.56 mm.

**Rest vs pose:** the dihedral is 112° at rest and 155° in the pose. This crosses the 120° fold threshold.

**Scope:**
- Configuration 1 only. Configuration 2 and the right ear are clean.
- No other pose is worse than the family.
- The eight ear-readiness poses are 0 / 0 / 0, including head yaw ±45.

**Cause:**
- The vertices carry 98.4–99.0 % head weight with a 1.0–1.6 % neck_01 tail. These weights are carried from the v005 skin by the branch map.
- Under plain LBS that tail shears these sub-millimetre quads by tenths of a millimetre, which is enough to crease them.

**Diagnostic** (`vael_rp3_final/diagnostics/`, not production): with the ear branch bound 100 % to the head bone, all 18 Standard v1 poses equal the family realization (folds / flips / contacts).

**Classification proposed:** rig / weight carry-forward at the production-rig stage. The ear branch should skin rigidly to the head. Geometry and topology are not implicated.

**Options for the author:**
1. **Recommended.** Accept it as a registered carry-forward, proposed `VAEL-CF-EARROOT-1`: "bind the Vael ear branch rigidly to head at rig stage". Then freeze by record. `VAEL_RP3_FREEZE_CANDIDATE.json` is renamed to `VAEL_RP3_FREEZE.json` with its status changed. The blends are already final.
2. Require a geometry fix: a local relax of the lobe-junction cuff quads. This reopens the accepted RI3 and produces `_v002` production files.

## 4. Clean rebuild / provenance — PASS (both)

| Check | c1 | c2 |
|---|---|---|
| R-6 regen (regen.py) | identical, max dV 0, geometry hash = accepted | identical, max dV 0 |
| Full record rebuild vs committed r6 | max dV 0, faces identical, measures equal | max dV 0, faces identical, measures equal |
| Family realization | byte-identical to reviewed `bodyfam_v004` | byte-identical |
| VA-E2-RI3 branch arrays vs reviewed RI3 | all arrays identical, max dV 0 | all arrays identical, max dV 0 |
| Twelve RI3 probes | V / measures identical to reviewed | — |
| Topology / cuff canon / face hash | `VAEL_EAR_BRANCH_TOPOLOGY_v002`, canon = accepted, face hash = accepted | same face hash as c1 |

Outside the ear branch, the production mesh equals the family realization byte for byte.

## 5 / 22. Production files and PC read-back — PASS

Files in `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Vael/RP3/`:
- `VA_M_REF_RP3_v001.blend`: sha `42f0cebb…`
- `VA_F_REF_RP3_v001.blend`: sha `516b18e8…`
- For each, `.json`, `_landmarks.json` and `_branch_map.npz`.

The frame is the standard one: metres, Z up, faces −Y, subject left +X, origin at pelvis root on ground.

Read-back of the E: copies:
- byte-identical to the written files (`production/pc_readback_sha256.txt`);
- geometry hash = sidecar;
- 59,076 V / 59,074 Q, 100 % quads, 1 mesh, `UVMap`, 1 component;
- 0 boundary, 0 non-manifold, 0 degenerate;
- normals outward;
- faces equal to the candidate, geometry within 6e-6 cm (float32 metres);
- branch map arrays equal to the candidate; landmarks and sidecars equal to written;
- face topology hash identical c1 / c2;
- **validator recomputed from the read-back geometry: 69 / 69 and 69 / 69.**

## 6. Integrity — PASS (both)

- 59,076 / 59,074, 1 component.
- 0 boundary / non-manifold edges / non-manifold vertices / degenerate faces.
- Winding consistent, normals outward, 0 coincident pairs.
- Rest contact set equal to the family's (c1 60 / 60; c2 110 / 110). Contact classes: c1 source 58 + family 2 + **new 0**; c2 source 110 + **new 0**.
- 0 branch self-intersections; root valence 4 (52 per side).

## 7. Validator — PASS

D1 + D3 + D4 + D5 + D6 = **69 / 69** on both configurations. All 69 stations are identical to the family realization (loops / margins / sides / D5 / D6). The family realization equals the reviewed v004. Fallback-label differences are the same kind as in the Aelari freeze. Table: `sheets/VA_FINAL_validator_margin_table.csv`.

## 8. Anatomy — PASS

- **Ear-excluded:** T-1 / T-2 / T-3 / T-7 pass on both. Stature difference: c1 −0.42 mm, c2 +0.00 mm. Minimum IoU 0.998 / 0.997.
- **Unmasked anatomy.py:** T-1 / T-2 and T-7 flag the new ear. The R-6 source carries the MPFB human auricle.
- **Localisation:** at more than 1.5 cm from every ear-branch vertex, the deviation is within the T-1 body limits on both:
  - c1: prod→source max 1.73 mm, source→prod max 0.86 mm;
  - c2: 1.95 / 0.81 mm.
  - File: `anatomy/VAEL_unmasked_anatomy_localisation.json`.

## 9 / 10. Human and three-elf body firewalls — PASS, equal to VF2

| Measure | c1 | c2 | Equals accepted VF2 |
|---|---|---|---|
| Canon (including every vs-Fenn / vs-Aelari row) | 20 / 20 | 20 / 20 | yes |
| Body systems material vs Marchfolk / Sagekin | 5 / 8 | 5 / 8 | yes |
| Face systems | 6 / 6 | 6 / 6 | yes |
| Elf face rows | 9 / 9 | 9 / 9 | yes |

Sheets 03 and 04 show silhouette overlays at 178 cm with ears hidden.

## 11. Pelvis — PASS

Gating rules hold **9 / 9 on both configurations** at t = 0 / 0.5 / 1.0:
- VA-P2a: > MF, < Fenn, < Aelari;
- VA-P2b;
- VA-P3;
- VA-P4 (×3);
- VA-P6.

The rows are identical to VF2.

## 12. Hidden-ear face — PASS

The face gate is 6 / 6 systems and 9 / 9 elf rows on both configurations, via va2_eval.

The seven-system hidden-ear read is identical to the accepted VF2:
- c1 material 5 / 7, direction 7 / 7;
- c2 material 6 / 7, direction 7 / 7.

## 13. UFCA / expressions — PASS

- 37 / 33 mouth rings.
- 43 / 43 orbit rings.
- 0 poles at mouth corners.
- 0 poles within 2 cm of the mouth.
- 4 / 4 poles within 2 cm of the eyes, as in the family.
- Face density mean 0.141 / 0.138 %.
- Equal to the family realization.
- Expression sanity identical to VF2.

## 14. Ear final gate — PASS

| Measure | c1 | c2 |
|---|---|---|
| T-4 (of 3,850 branch faces) | 123 | 144 |
| Min corner | 25.9° | 14.9° |
| Aspect max | 9.26 (0 > 10) | 9.26 (0 > 10) |
| Branch density mean (% stature) | 0.102 | 0.099 |
| Root crease max | 51° | 51° |
| Transition displacement | 0.06 cm | 0.06 cm |
| Clearance | 0.53 cm | 0.45 cm |

Audit and measures are identical to the reviewed RI3. Self-intersections 0; root valence 4 (52 per side).

## 15. Root / concha read — PASS

The final arrays are identical to the reviewed RI3.

| Read | c1 | c2 |
|---|---|---|
| Cuff skin vs hidden-ear skull, mean | 0.28 cm | 0.22 cm |
| Anterior cuff mound p90 | 0.17 cm | 0.08 cm |

Sheets 09, 11, 12 and 15 show:
- neutral clay at 3/4 front, profile and 3/4 rear;
- root, concha and tragus closeups;
- horizontal and vertical sections;
- the prototype→final overlay.

**If the point were removed, does it read as one coherent ear?** Yes.
**One auricle or a nested ear?** One auricle. The raised human-root cuff perimeter does not reappear.

## 16. Visible-ear firewall — PASS

Both configurations meet all five ordering checks:

| Check | Values (c1) |
|---|---|
| Angle: Fenn > Vael > Aelari | 52.7° > 37.4° > 27.2° |
| Vael broadest base, w/L | 0.448 vs Fenn 0.378, Aelari 0.335 |
| Vael broadest base, w/HH | also broadest |
| Vael most backward, chord | 26.0° vs 19.5 / 22.9° |
| Vael most backward, upper axis | 45.7° vs 32.3 / 38.0° |
| Vael shorter and blunter than Aelari | L / HH 0.327 vs 0.388; tip 34.5° vs 31.4° |
| Aelari most upward | yes |

Fenn is still visually most outward (sheet 16).

**Accepted residual (§2), recorded and not chased:**
- c1 stand-off over Fenn: mean +0.0047 HH, median +0.0041 HH, tip +0.0037 HH.
- c2 keeps Fenn > Vael > Aelari.

## 17. Density — PASS

All 9 zones pass on both configurations. The ear branch is ≤ 0.25 %. Only the face, ears and head zone means move from the family, all because of the new ear (head c1 0.239 → 0.293). Export does not change density: the read-back is identical.

## 18. Body deformation — one open item (above)

- Final equals the family realization pose by pose on 17 / 18 poses in c1 and 18 / 18 in c2 (flips, contacts, folds).
- The family equals the reviewed v004 on every pose.
- 0 new rest-contact class.
- **VAEL-CF-SHOULDER-1 reproduced unchanged:**
  - c1 shoulder flex 90° = 19 flips vs Marchfolk v005 13 (+6);
  - c2 16 vs 14 (+2).
- No other excess over Marchfolk exceeds +5.
- The only new item is the c1 `neck_rot45` cuff fold.

## 19. Ear / head readiness — PASS

All eight poses are 0 branch contacts / 0 flips / 0 root inversions on both configurations: neck flex and extension, yaw ±45, pitch ±20, roll ±20. There is no concha collapse and no cuff separation, and clearance is preserved.

## 20. Shape probes — PASS

12 / 12 intended measures move. The probes are identical to the reviewed RI3 probes:
- same topology;
- 0 branch self-intersections, 0 boundary / non-manifold;
- root valence 4;
- aspect max 9.74;
- T-4 111–178.

## 21. Visual package

`VA_FINAL_01`–`20`:
1. full body c1
2. full body c2
3. three-elf hidden-ear bodies
4. human firewall
5. pelvis
6. hidden-ear face
7. head c1
8. head c2
9. neutral clay
10. ear views
11. root / concha closeups
12. sections
13. wire / poles
14. T-4 / aspect
15. root integration and overlay
16. three-elf ears
17. projection / stand-off
18. body deformation
19. readiness / probes
20. source→production overlay

`18b` covers the open fold.

## Lineage (for the freeze record)

- c1: VAL4 ancestry → R1 (VB2g + VC2) → VD2 (VDF1.2) → VF2 (VEF1) → `VA_M_REF_RP3_v001`
- c2: VALF178 route → R1 → VD2 → VF2 → `VA_F_REF_RP3_v001`
- Ear: VA-E2 → RI3 → `VAEL_EAR_BRANCH_TOPOLOGY_v002`. This is a Vael-specific engineering topology. It is not a universal elf topology.

## Not done (stop rules)

None of the following were started:
- Halvren;
- any change to frozen Fenn, frozen Aelari or v005;
- low-light physiology;
- universal elf topology;
- creator morphs;
- ear rigging;
- UV / materials;
- LODs;
- UE5 integration.

`manifest.json` and `VAEL_V1.md` are not updated to frozen because the freeze is pending.

## Next race (after the Vael decision)

Recommend **Halvren**. Do not start it.
- Fenn, Aelari and Vael are separate elf population references. Two are frozen now; Vael will be the third once accepted.
- Halvren is mixed ancestry and must not be a simple average.
- Shared ear engineering may inform Halvren, but Halvren needs its own biological gate.

**STOP FOR CHATGPT REVIEW.**
