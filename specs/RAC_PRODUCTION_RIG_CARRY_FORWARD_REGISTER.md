# RAC — Production-rig carry-forward register

Items accepted at a topology / base freeze that belong to a **later** stage: production rigging, weighting, correctives or toe / finger articulation.
- They are **not topology-blocking**.
- They do not reopen any frozen base.
- Each item names its owning stage and where its evidence lives.

## MPFB family base (active base v005, `MPFB_FAMILY_BASE_v005_FREEZE.json`)

| ID | Configuration | Item | Class / owning stage | Evidence |
|---|---|---|---|---|
| MPFB-CF-1 | Marchfolk F (MF-F-R, configuration 2) | Toe extension 30°: **3** topology-attributable flipped faces in the toe-2 MTP crease (dorsal racetrack return strip / turn). Toe flexion 0. | Rig / weighting — toe-articulation stage | `reviews/rac-rp3-evidence/mpfb_family_base_final_toe2/deformation/MPFB_v005_flip_parentage.json` |
| MPFB-CF-2 | Skarn F (SKF208, configuration 2) | Toe extension 30°: **2** topology-attributable flipped faces in the toe-2 MTP crease. Toe flexion 0. | Rig / weighting — toe-articulation stage | same |

Context: male configurations (MF-M, SK-C1R) have 0. Accepted by order 78a109f §3.

**Known rig-class regions.** These are recorded for the rig stage; they are not exceptions.
- **Toe-extension MTP crease, single ball bone (LBS).** Frozen v003 already has 50–71 flipped faces against 12–20 native. 6 of the new v005 flips on MF-F and 6 on SK-F are parent-quad folds.
- **Hip-flex 90° groin crease.** LBS collapse; flips are concentrated in faces that already flipped on the parent.
- **Knee 140°, fist and shoulder flex 90°.** Inherited source-rig behaviour, identical across v003 / v004 / v005.

## Sagekin RP3 (frozen `SAGEKIN_RP3_FREEZE.json`, order d921903)

**No new ID.** Sagekin reproduces the family behaviour already registered above; it is recorded here only so the rig stage knows it applies.
- **SGF178 (configuration 2): MPFB-CF-1 class.** Toe extension 30°: 58 flips, a strict subset of MF-F v005's 60, including the same CF-1 toe-2 MTP crease faces (57776–57798). Toe flexion: 42, all shared with MF-F.
- **SG (configuration 1): known rig-class region.** Toe extension 30°: 71 flips (MF-M v005 70). 69 are shared with MF-M. The other 2 (faces 54413, 56501) are on unchanged v003-class rows, within 0.6 cm of flips in SG's own native hm08, and adjacent to MF-M flips: the single-ball-bone LBS crease, not topology.
- **Other poses:** at or below Marchfolk v005 (worst +2 flips).
- **Evidence:**
  - `reviews/rac-rp3-evidence/sagekin_rp3_freeze/SAGEKIN_toe_flip_overlap_vs_marchfolk_v005.json`;
  - `reviews/rac-rp3-evidence/sagekin_rp3_v001/SAGEKIN_RP3_deformation_comparison.json`.

## Fenn RP3 (FROZEN by record, order 6d2eadc; register opened bdcd6a6)

| ID | Configuration | Item | Class / owning stage | Evidence |
|---|---|---|---|---|
| FENN-CF-1 | Fenn configuration 2 (FNF181-CF2) | Generic diagnostic MPFB expression units, existing mouth-corner fold region. **Smile:** +6 self-intersection pairs against the pre-CF source, while flipped faces improve. **Sadness:** +10 self-intersection pairs and +12 flipped faces. Neutral / rest geometry is clean; topology and UFCA readiness pass; other expression metrics are equal or better. The source already folds there; CF strength scales the generic unit. | **FACIAL RIG / MOUTH-CORNER CORRECTIVE CARRY-FORWARD** — facial-rig stage. Not a source or topology blocker; CF2 geometry is not reopened for it. No production facial weights or correctives in RP3. | `reviews/rac-rp3-evidence/fenn_craniofacial_v001/CF_expression_sanity.json`; `reviews/claude-rac-rp3-fenn-craniofacial-source-gate.md` |

Final consolidation (order 6d2eadc, `reviews/claude-rac-rp3-fenn-final-freeze-report.md`):
- FENN-CF-1 is carried unchanged into the frozen bodies `FN_F_REF_RP3_v001` (and does not apply to `FN_M_REF_RP3_v001`).
- No new Fenn ID: the final Standard v1 deformation set adds 0 flips / 0 self-intersections / 0 folds over the CF2 family realization on every pose, and the ear head / neck readiness poses are 0 / 0 / 0.
- The accepted ear topology v002 T-4 residuals (root-band cells, aspect 6-10 quads, bridge-corner cells) are **topology-quality residuals accepted in 6d2eadc §2, not carry-forward items**.

## Vael RP3 (FROZEN by record 2026-10-29, `VAEL_RP3_FREEZE.json`; register opened by order `chatgpt-rac-rp3-vael-ear-prototype-order.md` §2)

Both items are carried into the final freeze (`reviews/chatgpt-rac-rp3-vael-final-author-acceptance-freeze-closure-order.md`) and are owned by production rigging. Neither reopens VF2, RI3 or `VAEL_EAR_BRANCH_TOPOLOGY_v002`.

| ID | Configuration | Item | Class / owning stage | Evidence |
|---|---|---|---|---|
| VAEL-CF-SHOULDER-1 | Vael configuration 1 (`VAL4-R1-VD2-VF2` → `VA_M_REF_RP3_bodyfam_v004` → final `VA_M_REF_RP3_v001`) | Shoulder flex 90° (left): **19** flipped faces vs Marchfolk v005 **13** (+6, one over the family +5 flag; VD2 was 16). The 3 faces above VD2 sit on the front of the shoulder. Native source flips are 5 vs 4. Ablation leaves the count at 19 with axilla A2 off, shaft gracility off, a smaller clavicle term (0.035) or a later upper-arm window, so the faces come from the clavicle-length route carried by the current MPFB weights / plain LBS, not from source anatomy. Configuration 2 is +2. Shoulder abduction 90° equals Marchfolk (25 / 25). **Carried into the final freeze unchanged** (final production body: 19 vs 13, c2 16 vs 14). | **RIG / WEIGHT / SHOULDER-CORRECTIVE CARRY-FORWARD**, production-rig stage (shoulder corrective / clavicle weighting). Not a source or topology blocker; VF2 anatomy is not reopened for it (author ruling). | `reviews/rac-rp3-evidence/vael_rp3_elf_frame/deform_ablation/VF_shoulder_flex_ablation.json`; `reviews/rac-rp3-evidence/vael_rp3_elf_frame/VAEL_deformation_comparison.json`; `reviews/claude-rac-rp3-vael-elf-frame-human-firewall-gate.md` §7 |
| VAEL-CF-EARROOT-1 | Vael configuration 1, final `VA_M_REF_RP3_v001` | Standard v1 `neck_rot45`: one new fold pair on two very small left ear-cuff quads at the lobe / root junction (faces 57125 / 57126; edges ~0.14–1.56 mm; dihedral ~112° at rest → ~155° posed, crossing the 120° fold diagnostic). 0 flips, 0 self-intersections / contacts, 0 root inversions; configuration 2 and the right ear clean; all 8 dedicated ear-readiness poses 0 / 0 / 0. Cause: the vertices inherit a ~1.0–1.6 % `neck_01` weight tail from the carried MPFB weights instead of moving rigidly with the skull. Diagnostic: with the ear branch bound 100 % to `head`, all 18 Standard v1 poses equal the family realization. | **RIG / WEIGHT / EAR-ROOT CORRECTIVE CARRY-FORWARD**, production-rig / skin-weighting stage. Required at final skinning: bind the Vael external-ear branch effectively rigidly to the head / skull, remove the inherited neck-weight tail from the external ear / root cuff, revalidate neck rotation, preserve the accepted RI3 root / concha geometry. Not a source or topology blocker (author ruling 2026-10-29). | `reviews/rac-rp3-evidence/vael_rp3_final/sheets/VA_FINAL_18b_c1_neck_rot45_fold.jpg`; `reviews/rac-rp3-evidence/vael_rp3_final/diagnostics/deform_VAL4-R1-VD2-VF2_rigid_head_ear_weights.json`; `reviews/claude-rac-rp3-vael-final-freeze-report.md` |

## Halvren RP3 ear family (frozen, `HALVREN_EAR_FAMILY_RP3_FREEZE.json`)

| ID | Configuration | Item | Class / owning stage | Evidence |
|---|---|---|---|---|
| HALVREN-CF-EAR-TRI-LOD-1 | HE1 HVEAR4 / HE2 HVEAR3 / HE3 HVEAR4, c1 (`HVC1-HB2HF2-HPB`) and c2 (`HVF178-HB2HF2-HPB`) | Production surface = baked TRI-HV1 triangles (per-quad diagonals incl. the step-5 crossing-resolution flips). Import normals / MikkTSpace tangents instead of letting the importer re-triangulate (a quad export would re-choose 10–242 flagged diagonals, up to 0.18 cm surface change). LODs with LOD-HV1 (root band protected, lobe zone weighted). One engine-side UE5 smoke test at first integration: exact imported triangle count / topology, no importer re-triangulation, normals / tangents intact, root seam intact, source / LOD silhouettes matching the approved evidence. | **ENGINE-INTEGRATION CARRY-FORWARD**, UE5 / rig integration stage. Not a geometry blocker; does not keep the family unfrozen (author ruling 2026-10-30). | `reviews/rac-rp3-evidence/halvren_rp3_final/HALVREN_EAR_FAMILY_RP3_FREEZE.json`; `reviews/claude-rac-rp3-halvren-ear-production-gate-report.md`; `reviews/rac-rp3-evidence/halvren_rp3_ear_production_gate/` |

## Grask RP2 (frozen v003)

Kept separately. See `reviews/claude-rac-rp2-grask-final-closure.md` §2:
- elbow 60–120° H2 direction;
- 130° deep-flexion contact corrective;
- engineering volume measures;
- the remaining items listed there.
