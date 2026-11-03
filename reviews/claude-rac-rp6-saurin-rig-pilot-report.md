# Claude Report — Saurin RP6 Production Rig / Skin-Weighting Pilot (order a407015)

**Status: all RP6 rig / weighting / corrective gates PASS on c1 (SA-M188) and c2 (SA-F188).
PASS submission held on one external input:** the PD-2 creator-state re-check (§18) and the dense-source
step of the four-step ownership audit (§11 step 1) need the rebuilt clean workspace
(`SA_RP5_WORK_v001.npz` + the 19 accepted `cr_<STATE>.npy` creator bodies), which lives on the operator E: drive
and was not available to this session. Everything else in §26 is complete and committed. When the folder is
attached, run `sa6_pd2.py` and re-run `sa6_eval.py` (dense mode switches on automatically), then the PASS line
can be issued if those two stay clean.

Tools: `tools/rac/rp/saurin_rp6_v001/` · Evidence: `reviews/rac-rp6-evidence/saurin/rig_pilot/`
(manifest `SA_RP6_rig_manifest_v001.json`, sha256 of every file).

---

## 1. Acceptance checklist (§26)

| Requirement | Result |
|---|---|
| Frozen RP5 package unchanged | 8/8 frozen hashes re-verified at end of run (`frozen_rp5_hashes_start.txt`, `sha256sum -c`) |
| RP6 neutral reproduces RP5 | max vertex error 7.96e-6 cm (c1), 7.92e-6 cm (c2) — float32 round-off |
| Saurin skeleton hierarchy documented | `SA_RP6_skeleton_v001.json` (108 bones) |
| c1 / c2 joint placements documented | `SA_RP6_joint_placement_{M,F}_v001.json` |
| Production weights documented | `SA_RP6_weights_{M,F}_v001.npz`, 107 deform groups |
| Full 34-pose suite on c1/c2 | 34 suite + 18 RP5-literal sign variants + 50 special-gate poses = 102 poses × 4 fractions per configuration |
| 0 TOPOLOGY-classified poses / 0 topology-only flips | 0 / 0 on the cage (dense-source confirmation pending — see top) |
| 0 RIG/WEIGHTING-owned folds after correctives | **0 on both configurations** (98 gated poses each) |
| Hand / shoulder / hip / tail-root classes closed | closed — 0 folds, 0 penetration, 0 tears |
| Tail / hand / foot / jaw-head gates | pass (§4) |
| PD-2 interface, no new rig regression | interface documented (`SA_RP6_PD1_PD2_interfaces_v001.md`); 19-state re-check **pending E: files** |
| Neutral identity unchanged | yes (above) |
| Blender read-back | pass both: Blender vs audit max 0.00039 cm (c1), 0.00016 cm (c2); 0 flips in Blender eval |
| Reproducible package committed | yes |

## 2. Deformation gate results (own audit, stricter than the order)

Gates per pose and fraction (0.25 / 0.5 / 0.75 / 1.0): 0 folded faces, 0 new interpenetrating vertices,
0 torn edges (stretch > 2.5× rest and > 0.75 cm), closed-body |ΔV| ≤ 100 cm³ (jaw poses exempt — the mouth opens),
rigid landmarks and head ≤ 0.05 cm.

| | c1 SA-M188 | c2 SA-F188 |
|---|---|---|
| Gated poses | 98 | 98 |
| Gate failures | **0** | **0** |
| Max closed-body \|ΔV\| | 44.5 cm³ | 44.7 cm³ |
| Torn edges | 0 | 0 |
| Max edge elongation | 1.93 cm | 1.69 cm |
| Rigid landmark max error | 0.000 cm | 0.000 cm |
| Weight audit leakage | pass | pass |
| Corrective families / keys | 80 / 165 | 80 / 166 |
| Keys active at rest | 0 | 0 |

Classification over the 102 poses (c1; c2 identical): 31 CLEAN, 67 RIG/WEIGHTING resolved by correctives,
1 CONTACT/SETUP, 3 NOT RIG-REALISABLE. The last two are diagnostics, not gated:

- `jaw_open_20_rp5lit` — the RP5 sign convention makes +20° *close* an already-closed mouth, driving the lower
  jaw into the upper. The anatomical `jaw_open_20` is clean.
- `tail_root_{lateral_30,vertical_25}_rp5lit`, `tail_twist_30_rp5lit` — the RP5 definitions pivot 9–10 cm off the
  tail_01 joint, which no bone rotation can reproduce (same driver angle as the realisable pose, different shape).
  The realisable versions pivot on the joint and pass every gate.

## 3. What changed in this round (beyond the RP6 v002 state)

1. **Locality.** Each pose's corrective may only move the blend zone of its driving joints (+8 rings), the flesh
   of the two segments the joint connects, and contact/tear sites (+10 rings). Hip correctives additionally reach
   tail_01 (caudofemoral coupling). Result: hip flexion moves hip, thigh, pelvis and tail root only — no longer
   the other leg or the distal tail.
2. **Partial self-masked bulge.** At deep flexion the outer elbow skin is already near the tear limit; a full
   volume-restoring bulge tore it, and the tear repair collapsed the volume. The polish now masks vertices a
   trial makes bad and takes the largest clean fraction of the bulge. This closed c2 `elbow_130_xneg`
   (−124 → −3 cm³), the last open defect.
3. Both configurations refit from scratch under these rules and converged (a full round with zero defects
   entering).

## 4. Special gates

- **Tail:** ring area ratio ≥ 0.94 on realisable poses, kink ratio ≤ 2.51, no folds — lateral 45/90/135, S-curve, combined, root poses.
- **Hand:** palm volume ratio 0.98–1.04 across fist, grasp, opposition, open, relaxed curl. Thumb tip reaches
  8.6–10.0 cm of the target fingertip in the opposition gates.
- **Foot / toe:** foot volume ratio 0.999–1.054; sole down-facing fraction unchanged from rest (0.82–0.84).
- **Jaw / head:** head and upper skull rigid error 0.000 cm; mouth-slit stretch is confined to the jaw.

Full tables: `SA_RP6_summary_tables_v001.md` and `SA_RP6_deformation_audit_v001.json`.

## 5. Visual evidence

21 matched c1/c2 sheets in `rig_pilot/renders/`. They cover:

- reference and rig-prep stance, and the skeleton overlay;
- shoulder 45/90, elbow 90/130, fist, grasp and opposition;
- hip, knee, ankle/toes, trunk and tail;
- jaw;
- worst residual before and after correctives;
- weight and corrective heat maps, the c1/c2 comparison, neutral overlay and contact ownership.

Checked by eye: the shoulder, hip, tail and elbow sheets show no folds or penetration. The deep elbow crease
is compressed on the inner side as expected.

## 6. Blender files

`SA_{M,F}_REF_RP6_rigpilot_v001.blend.xz`. Uncompressed they are 407 MB / 410 MB; xz brings each to 11.7 MB.
They hold the armature (108 bones), 107 vertex groups and LBS + baked pose-space corrective shape keys with
drivers (UE-native: no DQS at runtime).

Read back from disk in a fresh Blender process and compared with the audit evaluator. Object scale is 0.01
(cm → m).

## 7. Pending / next

1. Attach the E: drive folder that holds the clean workspace. Then run `sa6_pd2.py` for the 19 PD-2 states and
   re-run `sa6_eval.py` for dense-source ownership.
2. If both stay clean, issue the §26 PASS line and **stop for ChatGPT review**. No UV, material, LOD, creator,
   UE5 or other-race work was started.
