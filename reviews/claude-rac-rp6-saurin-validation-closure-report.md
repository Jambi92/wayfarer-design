# Claude Report — Saurin RP6 Validation Closure (order 58aa486c)

Status: **RP6 RIG PILOT / NOT FROZEN**.

- **Order:** [ChatGPT Order — Saurin RP6 Validation Closure](chatgpt-rac-rp6-saurin-validation-closure-order.md).
- **Continues:** [the RP6 rig pilot report](claude-rac-rp6-saurin-rig-pilot-report.md), under the original order a407015.
- **Evidence:** `reviews/rac-rp6-evidence/saurin/rig_pilot/`; manifest `SA_RP6_rig_manifest_v001.json` (58 files).
- **Tools:** `tools/rac/rp/saurin_rp6_v001/`.

Both pending checks are closed: PD-2 (§18) and dense-source ownership (§11). Every RP6 gate passes on c1 and c2, and on all 19 accepted PD-2 creator states. One **design addition** is flagged for review: the creator-state corrective layer (§2.3).

## 1. Approved inputs

### Canonical sources

The five W2I6 files in `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/out/` were attached read-only and staged into scratch. Their SHA-256 values were re-hashed and match the RP5 source integrity record: **5/5**.

### Clean workspace

No verified copy existed, so the workspace was reproduced in scratch:

- `sa_consolidate.py` with `SA_RP5_full_cage_optionb_final.npz` from approved commit `2ee75ae`;
- the RP5 body and head builders `cr_build.py`, `cr_build2.py` and `cr_head.py`, on the approved W2/W3B inputs.

The result is `work/SA_RP5_WORK_v001.npz`, `src/saurin_w2_final_base.npz` and the 19 `cr_<STATE>.npy` arrays. All **28/28 files match `clean_workspace.files` in `consolidation_rebuild.json` byte for byte**, re-verified at the end of this work.

Consolidation checks all pass:

- dense c1/c2 correspondence;
- canonical face order;
- frozen embedding reproduction (c1 rebuilt equals the approved V at 0.0 cm);
- topology `255645a1…`.

Provenance is recorded in `SA_RP6_clean_workspace_provenance_v001.json`. Dense arrays stay out of Git.

### Frozen RP5 set

Hashed before and after against the freeze record and the pilot's start list. `sha256sum -c frozen_rp5_hashes_start.txt` gives 8/8 OK, and `sa6_common.check_frozen` passes. All rebuilds ran in scratch.

## 2. The two pending checks

### 2.1 Dense-source ownership (§11)

`sa6_eval.py` M and F were run with the clean workspace: `dense_source_staged: true` in both outputs.

| | c1 | c2 |
|---|---|---|
| Poses evaluated (suite + literal variants + special gates, at 25 / 50 / 75 / 100 %) | 102 | 102 |
| Topology-only flips | 0 | 0 |
| TOPOLOGY-classified poses | 0 | 0 |
| Gated poses | 98 | 98 |
| Gate failures (`experiments/gates.py`) | 0 | 0 |
| Max \|dV\| | 44.5 cm³ | 44.7 cm³ |
| Tear edges | 0 | 0 |

The four-step comparison (dense source → RP5 scaffold → RP6 weights → RP6 weights + correctives) is in `SA_RP6_deformation_audit_v001.json`, with step-1 source fold rates and smooth-map co-location counts. Every LBS-stage RIG-WEIGHTING fold is resolved by the correctives, leaving 0 rig- or weighting-owned folds after correctives.

### 2.2 PD-2 creator states (§18)

All 19 accepted states were run on the full anatomical 34-pose suite at full angle (`sa6_pd2.py`). Pre-rig source folds and neutral cage flips reconcile exactly with `SA_PD2_ownership.json` on all 19.

**Result:** 19/19 states clean.

- 0 rig-owned folds, 0 rig-owned interpenetration, 0 tears, 0 volume failures (|dV| > 100 cm³).
- 0 regressions against the base configuration.
- 0 cage- or topology-owned defects.

| State | Base | Source folds (flipped + collapsed) | Neutral cage flips | RP5 audit match | Rig-owned, base correctives only | Production: rig-owned folds / contact / tears / volume fails | Composition-owned | Regressions | Layer keys changed + new |
|---|---|---|---|---|---|---|---|---|---|
| B-T80 | c1 | 89 + 5 | 0 | yes | 106 | 0 / 0 / 0 / 0 | 0 | 0 | 25 + 0 |
| BRD | c1 | 39 + 5 | 0 | yes | 114 | 0 / 0 / 0 / 0 | 0 | 0 | 23 + 2 |
| DSP-HIGH | c1 | 18 + 3 | 0 | yes | 0 | 0 / 0 / 0 / 0 | 0 | 0 | 1 + 0 |
| DSP-LOW | c1 | 0 + 0 | 0 | yes | 0 | 0 / 0 / 0 / 0 | 0 | 0 | 1 + 0 |
| F-N | c2 | 0 + 0 | 0 | yes | 67 | 0 / 0 / 0 / 0 | 0 | 0 | 24 + 2 |
| FAHI | c1 | 6675 + 282 | 98 | yes | 114 | 0 / 0 / 0 / 0 | 70 | 0 | 24 + 5 |
| LT90 | c1 | 0 + 0 | 0 | yes | 20 | 0 / 0 / 0 / 0 | 0 | 0 | 18 + 0 |
| M168 | c1 | 0 + 0 | 0 | yes | 78 | 0 / 0 / 0 / 0 | 0 | 0 | 29 + 1 |
| M208-B | c1 | 39 + 4 | 0 | yes | 231 | 0 / 0 / 0 / 0 | 0 | 0 | 48 + 4 |
| MIN | c1 | 18 + 0 | 0 | yes | 40 | 0 / 0 / 0 / 0 | 0 | 0 | 14 + 1 |
| MUFAHI | c1 | 11201 + 629 | 169 | yes | 646 | 0 / 0 / 0 / 0 | 135 | 0 | 29 + 10 |
| MUHI | c1 | 1197 + 56 | 25 | yes | 440 | 0 / 0 / 0 / 0 | 3 | 0 | 21 + 5 |
| NAR | c1 | 0 + 0 | 0 | yes | 68 | 0 / 0 / 0 / 0 | 0 | 0 | 25 + 4 |
| ORB+3 | c1 | 0 + 0 | 0 | yes | 0 | 0 / 0 / 0 / 0 | 0 | 0 | 1 + 0 |
| ORB-8 | c1 | 0 + 0 | 0 | yes | 0 | 0 / 0 / 0 / 0 | 0 | 0 | 1 + 0 |
| RDG0.90 | c1 | 0 + 0 | 0 | yes | 0 | 0 / 0 / 0 / 0 | 0 | 0 | 1 + 0 |
| RDG1.30 | c1 | 6 + 1 | 0 | yes | 0 | 0 / 0 / 0 / 0 | 0 | 0 | 1 + 0 |
| T55 | c1 | 894 + 133 | 0 | yes | 1 | 0 / 0 / 0 / 0 | 0 | 0 | 8 + 0 |
| T80 | c1 | 45 + 0 | 0 | yes | 6 | 0 / 0 / 0 / 0 | 0 | 0 | 9 + 0 |

**Ownership rules.** These are the final rules, written in `sa6_pd2.py` and `SA_RP6_PD1_PD2_interfaces_v001.md`.

- **Composition / PD-2** covers three cases:
  - a fold or contact within 1 cm of a pre-rig source fold or neutral cage flip, **and** already present under plain LBS of that pose;
  - any posed state of a quad the composition inverts in the neutral (the RP5 neutral cage flips);
  - a contact vertex inside the composition-folded zone whose only intersected surface is that same folded flesh.
- A defect the correctives create or move is never composition-owned.
- Proximity was used only as a screening signal. Every candidate was checked against LBS and the base column before ownership was assigned.

**How the rules were tightened during the work:**

- **Correctives moving composition folds.** An earlier looser rule (proximity only) hid composition-zone folds that the correctives had created on FAHI (lower_axial_flex_25: LBS 9 → 31). The strict LBS rule now counts these as rig-owned. The layers were re-fitted until clean under it.
- **Inverted neutral quads.** These have no valid rest orientation. Straightening one in a pose measured as a "flip" against the folded rest. Re-measured against the canonical orientation, the 25 FAHI hip "new" flips were all repairs; none was a fold.
- **Contact inside a fold.** A test with the composition-zone quads removed from the winding test showed the remaining contact on FAHI and MUFAHI was the fold's own self-intersection, not a contact with any other part of the body.

**Counterfactual for volume.** Locally un-folding the FAHI neutral (9 smoothing passes, ≤ 2.4 cm) left the LBS volume loss of the hip and trunk poses unchanged: −2887 → −2857 cm³. The large heavy-state volume losses are therefore contact, not fold inversion. They are corrected by the rig (§2.3), not attributed to composition.

**Visual evidence.** `renders/pd2/SA_RP6_pd2_<STATE>.png` covers the 13 states with base rig-owned folds, including the extremes FAHI, MUHI, MUFAHI, NAR and BRD. Each image shows three panels:

- the neutral body, with the pre-rig composition folds in red;
- the worst pose with base correctives only (BEFORE);
- the same pose with production correctives.

For example:

| State | Pose | Folds before | Folds after (production) |
|---|---|---|---|
| FAHI | hip_flex70_xpos | 33 (21 rig-owned) | 8, all on the red composition zone |
| MUFAHI | elbow_90_xneg | 85 | 0 |
| M208-B | fist_xpos | 75 | 0 |

### 2.3 Design addition for review: creator-state corrective layer

**Why it was needed.** With the base correctives applied unscaled (the v001 interface), 13 of the 19 states had rig-owned folds at the same joints the base correctives fix: shoulder, elbow, hip, knee, fist, toe and tail root. The base weights are kept: one set per base configuration, carried by topology.

**What it is.**

- A per-state additive corrective layer, fitted by `sa6_pd2_fit.py` on the state's own rest body.
- It uses the same solver, gates and locality rules as the base fit.
- Packaged as base-referenced deltas in `SA_RP6_creator_layers_v001.json/.npz` (16.7 MB). Unchanged base keys are referenced, not copied; every state set is rebuilt from base plus layer and asserted exactly equal.

**Runtime interface:**

```
corrective(state, pose) = base(pose) + layer_state(pose)
```

Between accepted states, the creator blends the layer deltas with the creator weights.

**Solver extensions used only for the layers.** They are environment-gated (`COMP_MASK`, `SEGBULGE`); the base c1/c2 correctives are unchanged and were not refit.

- **Composition mask:** the fit ignores exactly the composition-owned defects above.
- **Segment flesh bulge:** the volume corrective for contact-limited poses on the heaviest states. Volume is carried by the driving segment and, if needed, by its parent, children and siblings, kept ≥ 6–8 cm clear of contact. Each step is followed by unfold, contact projection and tear fix.
  - MUHI elbow_130_xneg: −607 → 0 cm³, max displacement 1.1 cm.
  - MUFAHI hip_flex70_xpos: −3984 → 0 cm³, max displacement 2.1 cm.
  - Both end with 0 folds, 0 new contact and 0 tears.

**Compute.** The 18 non-NAR layers were fitted on Tyler's PC: 16 cores, a portable bundle with cage-level states only (no dense arrays), and a bit-identical portable mode checked against the workspace. MUFAHI was finished in the session. All layers were re-audited here on the clean workspace.

## 3. Historical RP5 poses (§3)

`SA_RP6_rp5_literal_diagnostics_v001.json` records both interpretations side by side for every retargeted pose: name, axis, sign, amplitude, pivot, reason and measured results for c1 and c2.

- **Sagittal sign.** RP5 assumed +Y posterior. Production uses the anatomical sign in the RP6 frame (+Y anterior), with the same axis and amplitude.
- **`jaw_open_20_rp5lit`.** Kept as the historical closure/contact diagnostic; classified CONTACT-SETUP. The literal sign closes the jaw into the upper mouth. The anatomical jaw opening and the jaw/head combinations are gated.
- **Tail-root literals.** `tail_root_lateral_30`, `tail_root_vertical_25` and `tail_twist_30` keep their historical off-joint pivot; classified NOT RIG-REALISABLE. The production variants are gated about `tail_01` at the same axes and angles.

| Tail-root literal | c1 | c2 |
|---|---|---|
| Pivot offset from `tail_01` | 10.20 cm | 10.40 cm |
| Induced translation, lateral_30 | 2.04 cm | 2.02 cm |
| Induced translation, vertical_25 | 4.39 cm | 4.48 cm |
| Induced translation, twist_30 | 3.09 cm | 3.14 cm |

No exception or ownership change beyond these four established diagnostics.

## 4. Rebuild and verification (§4)

**Package.** `sa6_package.py` was rebuilt with the fresh PD-2 and dense audits; the manifest now also covers `renders/`. All **58/58 files match their recorded SHA-256 and byte counts**. Both `.blend.xz` containers decompress to exactly the recorded blend SHA-256 and byte counts:

| | Blend SHA-256 | Bytes |
|---|---|---|
| M | `6639ea75…` | 407,279,433 |
| F | `cec2b375…` | 409,573,890 |

**Fresh-process Blender read-back.** Each packaged blend was decompressed from its container and reopened in a new bpy 5.2.2 process (`sa6_blend_readback.py`).

| Check | c1 | c2 |
|---|---|---|
| Neutral vs frozen RP5 blend | identical (max 0.0) | identical (max 0.0) |
| Neutral vs float64 embedding | 7.6e-6 cm | 7.6e-6 cm |
| Topology, face order, semantics | match | match |
| Bones (deform) | 108 (107) | 108 (107) |
| Weight groups = deform bones; max diff vs npz | yes; 0.0 | yes; 0.0 |
| Shape keys | 165/165 | 166/166 |
| Drivers valid (simple expressions) | 245/245 | 246/246 |
| Max shape-key value at rest | 0.0 | 0.0 |
| Images / libraries / materials / texts / UVs | 0 | 0 |
| Blender posed vs external evaluator | max 0.00039 cm, 0 flips | max 0.00016 cm, 0 flips |

**Audits re-run, all identical to the packaged audits:**

- **Weight audit:** leakage pass.
- **Corrective audit:** 80 families; 165 / 166 keys; 0 active at rest.
- **Reference → rig-prep → reference:**
  - (a) armature round trip: exact;
  - (c) exact inverse: 7e-14 cm;
  - (b) LBS re-bind residual: reported (0.34 / 0.14 cm max / p99), as before.
- **Special gates** (hand, shoulder, hip, tail, foot/toe, jaw/head) on c1 and c2: inside the 98 gated poses, FAILS 0.

**Frozen-source integrity:** 8/8 hashes and `check_frozen` pass.

### Submission checklist

| Requirement | Result |
|---|---|
| Topology-classified poses | 0 |
| Topology-only flips | 0 |
| Unresolved rig/weighting-owned folds or inversions after correctives | 0 |
| New rig-owned penetrations or tears in gated production poses | 0 |
| Special gates on c1 and c2 | pass |
| PD-2 check | closed: 19/19 clean |
| Dense-source check | closed |
| Fresh Blender read-back | pass |
| Frozen-source integrity | pass |
| PD-1 interface | unchanged |
| PD-2 interface | updated with the creator-state layer, ownership rules and retest requirements |

### For review

- **Creator-state corrective layer (§2.3).** Accept as the RP6 creator interface, or replace with a per-body-class re-solve.
- **Composition-owned residuals.** FAHI 70, MUHI 3 and MUFAHI 135 posed residuals remain owned by the folded creator inputs. They reach 0 only when the future composition solver delivers fold-free neutrals; the retest requirements are in the interface doc.

Scope stops at the RP6 review gate: no UV, materials, LOD, creator implementation, PD-2 solver, PD-1 transport, UE5 or other-race work.

**SAURIN RP6 PRODUCTION RIG / SKIN-WEIGHTING PILOT PASS — READY FOR CHATGPT / AUTHOR REVIEW**
