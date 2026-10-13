# RM-OT-05Q replay (run from the repository root)

Requirements: Python 3 with trimesh, numpy, scipy, matplotlib, PIL, igl, `triangle` (`pip install triangle`), and bpy (renders only).

```bash
T=tools/rac/w1/rmot05q_drivers; S=reviews/rac-rmot05q-evidence
GLB=path/to/base.glb        # sha256 78ecfa87…a7b; see source/PROVENANCE.md for verified locations
```

## §2 Extraction

The script checks the GLB hash. It writes the original and working copies plus `extraction_record.json`.

```bash
python3 $T/q_extract.py --glb $GLB --faces $S/source/F1_face_indices.npz --out OUT
# OUT/F1_working.obj must have sha256 17591025c24fd080e7fd45e3dc88dccc4707a0bee9efcb3fd70ef5ab6da453b0
# (the committed copy is source/F1_working.obj.gz)
gunzip -k $S/source/F1_working.obj.gz; M=$S/source/F1_working.obj
```

## §3 Separability

Sections: the plane lists for each item are in `separability/S_*.json`, as label:origin:normal:R.

```bash
python3 $T/q_sections.py --mesh $M --out $S/separability/S_belt --planes z100:0,4,100:0,0,1:32 z110:0,4,110:0,0,1:32 ...
```

Renders: `q_render.py` (the titles name the view, box and centre).

Inventory:

```bash
python3 $T/q_inventory.py --mesh $M --sel $S/plan/patch_face_sets.npz --out $S/separability
```

## §4 Plan

Committed in a93502b before any edit. See `plan/PLAN.md`.

```bash
python3 $T/q_select.py --mesh $M --out $S/plan                        # defaults ta=-97 tb=88 dg=0.45 ds=1.8 rmax=13
python3 $T/q_mapplot.py $M $S/plan/patch_selection.json $S/plan/patch_face_labels.npy $S/plan/P_theta_s_map.png
```

## §5 Repair: every attempt, in order

```bash
python3 $T/q_patch.py   --mesh $M --sel $S/plan --out OUT --tag A1                              # rejected
python3 $T/q_patch.py   --mesh $M --sel $S/plan --out OUT --tag A2 --smooth 2.0 --zip chain     # rejected
python3 $T/q_patch_b.py --mesh $M --sel $S/plan --out OUT --tag B1                              # rejected (V3 intersections)
python3 $T/q_patch_b.py --mesh $M --sel $S/plan --out OUT --tag B2 --relax 30                   # RESULT (reported)
python3 $T/q_patch_b.py --mesh $M --sel $S/plan --out OUT --tag B3 --relax 60 --relax_zone 4    # not better than B2
```

## §6 Verification

```bash
python3 $T/q_verify.py --src $M --sel $S/plan --res OUT/GO-05Q-B2.obj --out OUT/B2
```

The verifier writes `B2_verify.json` and `B2_V6_sections.png`. `GO-05Q-B2.obj` must have sha256 `0ed458b72e6481377aa829d70f8f7896381634e9fc7cca09bc325a91b420962a`; the committed copy is `repair/GO-05Q-B2.obj.gz`.

The compare images are `q_render.py` with identical `--box/--center/--scale/--views` for before and after:

```
--box 10 60 -30 30 140 190 --center 31 -1 164 --scale 30 --views 180:0,90:0,0:0,135:10,45:10,180:-55
```

Rows are stacked with PIL.
