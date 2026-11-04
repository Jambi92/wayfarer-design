# Saurin RP6 — PD-2 creator-state and PD-1 scale-detail interfaces

Status: **RP6 RIG PILOT / NOT FROZEN**. Order a407015 §18–§19. Numbers: `SA_RP6_deformation_audit_v001.json` → `pd2`.

## PD-2: creator-state interface

RP6 does not implement the creator. The rig was re-checked on all 19 accepted PD-2 states (NAR, BRD, T80, FAHI, MUHI, LT90, T55, MIN, MUFAHI, B-T80, M168, M208-B, F-N, ORB-8, ORB+3, RDG0.90, RDG1.30, DSP-LOW, DSP-HIGH) with `tools/rac/rp/saurin_rp6_v001/sa6_pd2.py` on the verified clean RP5 workspace (`SA_RP6_clean_workspace_provenance_v001.json`). Results: `SA_RP6_deformation_audit_v001.json` → `pd2`; renders: `renders/pd2/`.

### How each state is evaluated

1. The frozen cage is realised on the state's dense body through the frozen barycentric embedding. No topology or geometry change.
2. Pre-rig, the dense-source folds (flipped or collapsed below 5 % of rest) and the neutral cage flips are recorded. They are reconciled against the RP5 ownership audit (`SA_PD2_ownership.json`); all 19 match exactly.
3. The RP6 joint definitions are re-evaluated on the state, by the same landmark transfer as c2.
4. **Weights: one set per base configuration.** These are carried by topology: c1 for the SA-M states, c2 for F-N.
5. **Correctives: the base configuration's set plus the state's creator-state corrective layer.** The layer is in `SA_RP6_creator_layers_v001.json/.npz`.
6. The full anatomical 34-pose suite is run at full angle. Each pose is evaluated three ways: LBS only, base correctives, and production (base + layer).

### Ownership rules

- **Composition-owned (COMPOSITION/PD-2), fold or contact:** the defect lies within 1 cm of a pre-rig source fold or neutral cage flip, and plain LBS of the same pose already shows it there. A defect the correctives create or move is never composition-owned.
- **Composition-owned, inverted quads:** quads the composition inverts in the neutral are composition-owned in every pose. These are the RP5 neutral cage flips: 98 on FAHI, 25 on MUHI and 169 on MUFAHI.
- **Composition-owned, fold self-intersection:** a contact vertex inside the composition-folded zone, whose only intersected surface is that same folded flesh, is composition-owned. The test is that there is no penetration once the zone's quads are excluded from the winding-number test.
- **Rig-owned:** every other fold, new interpenetration, tear edge (> 2.5× and > 0.75 cm) or closed-body volume change above 100 cm³ (jaw poses exempt). The thresholds are the same as for c1 and c2.
- **Regression:** a rig-owned defect in a pose where the base configuration is clean.

**Result:** 19 of 19 states have 0 rig-owned folds, 0 rig-owned interpenetration, 0 tears, 0 volume failures and 0 regressions. There are 0 cage- or topology-owned defects. The composition-owned residuals are listed per pose in the audit:

| State | Composition-owned residuals | Rig-owned with base correctives only |
|---|---|---|
| FAHI | 70 | 114 |
| MUHI | 3 | 440 |
| MUFAHI | 135 | 646 |

### Creator-state corrective layer (design addition — for ChatGPT / author review)

Base correctives applied unscaled leave rig-owned folds on 13 of the 19 states. They sit at the same joints the base correctives fix: shoulder, elbow, hip, knee, fist, toe and tail root. The layer fixes them with the base solver, gates and locality rules, fitted on the state's own rest body (`sa6_pd2_fit.py`). Each layer is an additive delta over the base set; base keys are reused unchanged wherever the state needs no change.

**Runtime interface:**

```
corrective(state, pose) = base corrective of the state's base configuration (pose) + layer_state(pose)
```

Between accepted states, the creator blends the layer deltas with the same convex creator weights it uses for the morphs.

**Solver extensions used only for the layers:**

- **Composition mask:** the fit ignores exactly the composition-owned defects defined above, so it neither chases composition folds nor trades volume against them.
- **Segment flesh bulge:** a contact-limited volume corrective spread over the driving segment and its neighbours, kept clear of contact.

The base c1 and c2 correctives are unchanged; they were not refit.

### What the future composition solver must deliver before rig deformation

- A body on the frozen W2I6 face list, or the frozen cage realised from it through the frozen barycentric map. Same vertex order and quad order (topology sha256 `255645a1…`).
- No folded and no collapsed source triangles in the neutral state. Collapse means area below 5 % of rest. The deep crease folds of FAHI, MUHI and MUFAHI are composition defects; they must be resolved by composition, not by the rig.
- No neutral cage flips.
- Semantic regions unchanged: digits, webs, mouth slit, tail rings and claw caps.
- Landmarks and semantic rings must stay inside their own body parts. Joints are re-derived from them.

### Retest requirements once PD-2 is solved

- Re-fit the creator-state layer per state with `sa6_pd2_fit.py`. On a clean composition the composition mask is empty.
- Re-run `sa6_pd2.py` on all states. It must show 0 rig-owned defects, 0 volume failures and 0 regressions. The composition-owned residuals of FAHI, MUHI and MUFAHI must reach 0, because they exist only because the input is folded.
- Run `sa6_eval.py` on each new base configuration, `sa6_weight_audit.py` and the leakage tests, and the Blender export and read-back.

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
