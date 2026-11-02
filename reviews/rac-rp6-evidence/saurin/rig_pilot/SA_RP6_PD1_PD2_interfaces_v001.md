# Saurin RP6 — PD-2 creator-state and PD-1 scale-detail interfaces

Status: **RP6 RIG PILOT / NOT FROZEN**. Order a407015 §18–§19. Numbers: `SA_RP6_deformation_audit_v001.json` → `pd2`.

## PD-2: creator-state interface

RP6 does not implement the creator. The rig was re-checked on all 19 accepted PD-2 states (NAR, BRD, T80, FAHI, MUHI, LT90, T55, MIN, MUFAHI, B-T80, M168, M208-B, F-N, ORB-8, ORB+3, RDG0.90, RDG1.30, DSP-LOW, DSP-HIGH) with `tools/rac/rp/saurin_rp6_v001/sa6_pd2.py`.

How each state was tested:

1. The frozen cage is realised on the state's dense body through the frozen barycentric embedding. No topology or geometry was changed.
2. Before rigging, the dense-source folds and the neutral cage flips of the state are recorded. This is the RP5 PD-2 measure.
3. The RP6 joint definitions are re-evaluated on the state, by the same method as for c2.
4. The c1 production weights and c1 correctives are applied through the shared topology. The full anatomical 34-pose suite is then run.
5. A posed fold within 1 cm of a pre-rig source fold, or of a neutral cage flip of the state, is **COMPOSITION/PD-2**. Any other fold is rig-owned on that state.
6. A rig-owned fold in a pose where c1 is clean counts as a **regression**.

### What the future composition solver must deliver before rig deformation

- A body on the frozen W2I6 face list, or the frozen cage realised from it through the frozen barycentric map. Same vertex order and same quad order (topology sha256 `255645a1…`).
- **No folded and no collapsed source triangles in the neutral state.** The deep crease folds of the high fat and high muscle states (FAHI, MUHI, MUFAHI) must be resolved by composition, not by the rig. Collapse means area below 5 % of rest.
- No neutral cage flips.
- Semantic regions unchanged: digits, webs, mouth slit, tail rings and claw caps.
- Landmarks and the semantic rings (digit base / r1 / r2, wrist, tail module rings) must stay inside their own body parts. Joints are re-derived from them.

### What the rig and weights assume from that clean input

- Joints are re-derived per state by the RP6 definitions: landmark joints by local affine transfer, ring joints by ring centroids.
- Weights are carried by topology. The capsule and diffusion method is region-masked, so a state that moves a region's vertices across another region's capsule does not change ownership.
- Correctives are rest-space deltas per corrective family. They are solved on c1 and c2. For other states they are applied unscaled. A production creator should either blend the c1 and c2 corrective sets by the state's position between them, or re-solve them per body class with `sa6_fit.py`.

### What to re-run once PD-2 is solved

- `sa6_pd2.py`: all 19 states; must show 0 rig-owned folds.
- `sa6_eval.py` on each new base configuration.
- `sa6_weight_audit.py` and the leakage tests.
- `sa6_fit.py` per base configuration, if new body classes are added.
- The Blender export and read-back.

## PD-1: scale-detail / relief interface

RP6 bakes no scales into the rig mesh. The rig deforms the frozen RP5 cage only.

- **What later relief transport must consume:**
  - the posed cage positions (LBS plus driven corrective shape keys);
  - the per-vertex blended rotation M_v = Σ w R, or its polar factor, as the local frame carrier;
  - the corrective activation values.

  All three come from the armature, weights and shape keys in the RP6 files.
- **Normals and tangent frames must be recomputed after deformation.** Static neutral normals are not valid under flexion. The corrective-free LBS surface folds in the priority poses (`step3_lbs_flips` in the audit), and correctives change the surface orientation in creases. Use per-frame normals and a tangent frame rebuilt from the deformed cage (e.g. MikkTSpace on the deformed mesh). Never use the neutral bake.
- **Deformation-aware detail transport is required wherever edge stretch or compression leaves the pilot thresholds or a corrective is active:**
  - knee and elbow creases (contact flattening);
  - axilla;
  - groin and hip;
  - the tail root;
  - finger, thumb and toe flexion creases;
  - the mouth slit under jaw opening.

  The per-pose stretch ranges are in the deformation audit (`joint_metrics.stretch_corrected`).
- **Does the rig make PD-1 worse by design?** No. The rig adds no topology, no subdivision and no geometry edit. The correctives are smooth and bounded: rest-space deltas derived from the frozen mesh by a Poisson rotation-field solve, local unfolding and contact projection, with no high-frequency content. The scale-placement problem of PD-1 is unchanged and remains owned by the later transport system.
