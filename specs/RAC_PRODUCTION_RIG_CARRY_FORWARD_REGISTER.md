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

## Grask RP2 (frozen v003)

Kept separately. See `reviews/claude-rac-rp2-grask-final-closure.md` §2:
- elbow 60–120° H2 direction;
- 130° deep-flexion contact corrective;
- engineering volume measures;
- the remaining items listed there.
