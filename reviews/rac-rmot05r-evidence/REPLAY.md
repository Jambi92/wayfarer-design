# RM-OT-05R replay (run from the repository root, or from the package root with the paths in `README.md`)

Requirements: Python 3.11, numpy, scipy, trimesh, matplotlib, Pillow, libigl (python `igl`), `triangle`, and bpy 5.0 (renders only). Versions are listed in the package's `REQUIREMENTS.txt`.

```bash
Q=reviews/rac-rmot05q-evidence; R=reviews/rac-rmot05r-evidence; T=tools/rac/w1/rmot05r_drivers; OUT=/tmp/r05
mkdir -p $OUT
gunzip -c $Q/source/F1_working.obj.gz > $OUT/F1_working.obj   # sha256 17591025…53b0
gunzip -c $Q/repair/GO-05Q-B2.obj.gz  > $OUT/B2.obj            # sha256 0ed458b7…962a
```

## Plan (committed f1e0cb7, before any edit)

```bash
python3 $T/r_select.py --src $OUT/F1_working.obj --b2 $OUT/B2.obj --q05 $Q --out $OUT/plan   # reproduces $R/plan/junction_sets.npz
```

## The planned operation and the bounded correction (every produced mesh is kept)

```bash
python3 $T/r_repair.py --b2 $OUT/B2.obj --q05 $Q --plan $R/plan --out $OUT --tag R1                         # planned operation
python3 $T/r_repair.py --b2 $OUT/B2.obj --q05 $Q --plan $R/plan --out $OUT --tag R2 --orient boundary --flip_guard global
python3 $T/r_repair.py --b2 $OUT/B2.obj --q05 $Q --plan $R/plan --out $OUT --tag R3 --orient boundary --flip_guard global --flip_winding topo
```

| Run | Expected decoded sha256 |
|---|---|
| R1 | `66123d9b…3295` |
| R2 | `f33a039c…fd75` |
| R3 | `f68fe318…4844` |

R2 and R3 are the bounded correction of one discrete issue: inconsistent orientation and non-manifold edges at the patch, caused by the flip implementation.

## Verification

```bash
python3 $T/r_verify.py --src $OUT/F1_working.obj --q05 $Q --plan $R/plan --res $OUT/GO-05R-R3.obj --maps $OUT/GO-05R-R3_maps.npz \
        --labels $OUT/GO-05R-R3_face_labels.npy --out $OUT/R3
```

To score the baseline B2 with the same code, use 05Q's protected set:

```bash
python3 $T/r_verify.py --src $OUT/F1_working.obj --q05 $Q --plan $R/plan --res $OUT/B2.obj --maps $R/baseline/GO-05Q-B2_maps_for_r_verify.npz \
        --labels $Q/repair/GO-05Q-B2_face_labels.npy --nprot 140081 --prot_sha 28d2b7aed535275fe9a176b977fc0199f79c5a19af7c5a88f99062c59edfaa34 --prot_faces P05Q --out $OUT/B2
```

## Images

Images use identical cameras and material:

```bash
python3 $T/r_compare.py --out X.png --rows "SOURCE|F1_working.obj|none" "B2|B2.obj|none" "R3|GO-05R-R3.obj|none" -- <camera>
```

- Posterior camera: `--box 15 45 -25 5 150 178 --center 28.7 -10.4 162.5 --scale 14 --views 0:0,20:0,330:0,0:-45 --res 560`
- Anterior camera: `--box 15 45 -5 25 150 178 --center 30.1 9.6 163 --scale 14 --views 180:0,160:0,200:0,180:-45 --res 560`
- Arm camera: `--box 10 60 -30 30 140 190 --center 31 -1 164 --scale 30 --views 180:0,90:0,0:0,135:10,45:10,180:-55 --res 520`

Sections:

```bash
python3 $T/r_profiles.py --frame $Q/plan/patch_selection.json --meshes "source=…:0.65" "B2=…:#ff7f0e" "R3=…:#1f77b4" --thetas …
```
