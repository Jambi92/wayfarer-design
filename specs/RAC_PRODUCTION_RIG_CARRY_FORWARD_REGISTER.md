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

## Vael RP3 (NOT frozen; register opened by order `chatgpt-rac-rp3-vael-ear-prototype-order.md` §2)

| ID | Configuration | Item | Class / owning stage | Evidence |
|---|---|---|---|---|
| VAEL-CF-SHOULDER-1 | Vael configuration 1 (`VAL4-R1-VD2-VF2` → `VA_M_REF_RP3_bodyfam_v004`) | Shoulder flex 90° (left): **19** flipped faces vs Marchfolk v005 **13** (+6, one over the family +5 flag; VD2 was 16). The 3 faces above VD2 sit on the front of the shoulder. Native source flips are 5 vs 4. Ablation leaves the count at 19 with axilla A2 off, shaft gracility off, a smaller clavicle term (0.035) or a later upper-arm window, so the faces come from the clavicle-length route carried by the current MPFB weights / plain LBS, not from source anatomy. Configuration 2 is +2. Shoulder abduction 90° equals Marchfolk (25 / 25). | **RIG / WEIGHT / SHOULDER-CORRECTIVE CARRY-FORWARD**, production-rig stage (shoulder corrective / clavicle weighting). Not a source or topology blocker; VF2 anatomy is not reopened for it (author ruling). | `reviews/rac-rp3-evidence/vael_rp3_elf_frame/deform_ablation/VF_shoulder_flex_ablation.json`; `reviews/rac-rp3-evidence/vael_rp3_elf_frame/VAEL_deformation_comparison.json`; `reviews/claude-rac-rp3-vael-elf-frame-human-firewall-gate.md` §7 |

## Grask RP2 (frozen v003)

Kept separately. See `reviews/claude-rac-rp2-grask-final-closure.md` §2:
- elbow 60–120° H2 direction;
- 130° deep-flexion contact corrective;
- engineering volume measures;
- the remaining items listed there.
