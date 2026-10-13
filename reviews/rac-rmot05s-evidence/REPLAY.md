# RM-OT-05S replay (run from the repository root, or from the package root)

Requirements: as for 05R (`REQUIREMENTS.txt`). The `.blend` handoff needs bpy 5.0.1.

```bash
Q=reviews/rac-rmot05q-evidence; S=reviews/rac-rmot05s-evidence; T=tools/rac/w1/rmot05s_drivers; OUT=/tmp/r05s; mkdir -p $OUT
gunzip -c $Q/source/F1_working.obj.gz > $OUT/F1_working.obj        # 17591025…53b0
gunzip -c $Q/repair/GO-05Q-B2.obj.gz  > $OUT/B2.obj                # 0ed458b7…962a (baseline = F1 + verified 05Q recipe)
```

## Plan (35479a0, before any edit)

```bash
python3 $T/s_design.py --mesh $OUT/B2.obj --frame $Q/plan/patch_selection.json --out $OUT/plan    # design columns
python3 $T/s_select.py --b2 $OUT/B2.obj --src $OUT/F1_working.obj --q05 $Q --design $OUT/plan --out $OUT/plan
python3 $T/s_planviz.py --src $OUT/F1_working.obj --b2 $OUT/B2.obj --r3 <05R R3 decoded> --q05 $Q --plan $OUT/plan
```

## The declared study: S1, then the documented correction passes S2 and S3

```bash
python3 $T/s_repair.py --b2 $OUT/B2.obj --q05 $Q --plan $S/plan --out $OUT --tag S1
python3 $T/s_repair.py --b2 $OUT/B2.obj --q05 $Q --plan $S/plan --out $OUT --tag S2 --chart target --flip_cap 5000
python3 $T/s_repair.py --b2 $OUT/B2.obj --q05 $Q --plan $S/plan --out $OUT --tag S3 --chart target --flip_cap 5000 --extend 1
```

| Run | Expected decoded sha256 |
|---|---|
| S1 | `058360ca…39e3` |
| S2 | `f7160a0e…0589` |
| S3 | `1d503833…ac4c` |

## Verification

```bash
python3 $T/s_verify.py --src $OUT/F1_working.obj --q05 $Q --plan $S/plan --res $OUT/GO-05S-S3.obj --maps $OUT/GO-05S-S3_maps.npz \
        --labels $OUT/GO-05S-S3_face_labels.npy --out $OUT/S3
```

## Handoff

```bash
python3 $T/s_handoff_blend.py --res $OUT/GO-05S-S3.obj --labels $OUT/GO-05S-S3_face_labels.npy --src $OUT/F1_working.obj --b2 $OUT/B2.obj \
        --frame $Q/plan/patch_selection.json --out handoff.blend
python3 $T/s_rematch.py --edited EDITED.obj --src $OUT/F1_working.obj --plan $S/plan --out EDITED_rm      # then s_verify on EDITED_rm
```

## Images

Images come from `tools/rac/w1/rmot05r_drivers/r_compare.py` and `r_profiles.py`. The camera arguments are in `reviews/claude-rac-rm-ot-05s-gorrund-direct-band-axilla-interface-gate.md`.
