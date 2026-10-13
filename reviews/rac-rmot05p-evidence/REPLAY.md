# RM-OT-05P replay (run from the repository root)

```bash
T=tools/rac/w1/rmot05p_drivers; O=reviews/rac-rmot05o-evidence; N=reviews/rac-rmot05n-evidence; S=reviews/rac-rmot05p-evidence
BASE=$O/surface/GO-RD3b-REF_surface.obj        # declared baseline (sha256 79c513bd…a3100c)
```

## Baseline axes (proxy landmarks; declared joint heights)

```bash
python3 $T/p_legaxes.py $BASE $S/baseline/RD3b_leg_axes --hip_z 109.55 --knee_z 58.34 --ankle_z 10.84 --zmax 108 --thigh 70 95 --shank 22 48
```

## Stage A: coronal stance

```bash
python3 $T/p_coronal.py --in $BASE --axes $S/baseline/RD3b_leg_axes.json --out $S/A_coronal/GO-RD4A-REF_coronal.obj
```

## Stage B: trunk / pelvis

```bash
python3 $T/p_trunkprofile.py $S/A_coronal/GO-RD4A-REF_coronal.obj $S/B_trunk/RD4A_trunk_profile.json 104 176 2
python3 $T/p_displace.py --in $S/A_coronal/GO-RD4A-REF_coronal.obj --zones $S/B_trunk/B_zones.json --profile $S/B_trunk/RD4A_trunk_profile.json --out $S/B_trunk/GO-RD4B1-REF_displace.obj
python3 $T/p_brush.py --in $S/B_trunk/GO-RD4B1-REF_displace.obj --strokes $S/B_trunk/B5_strokes.json --out $S/B_trunk/GO-RD4B-REF_trunk.obj
```

## Stage C: joints and surface

C1, the arm pose clearance, was attempted and rejected; see `C_limbs/C1_rejected/`. It used `p_armclear.py` and is not part of the chain.

```bash
python3 $T/p_regiondisp.py --in $S/B_trunk/GO-RD4B-REF_trunk.obj --zones $S/C_limbs/C2_zones.json --out $S/C_limbs/GO-RD4C2-REF_joints.obj
python3 $T/p_brush.py --in $S/C_limbs/GO-RD4C2-REF_joints.obj --strokes $S/C_limbs/C3_strokes.json --out $S/C_limbs/GO-RD4-REF.obj
```

## LOW, rebuilt from the repaired REF with protection

```bash
python3 $T/p_low.py --ref $S/C_limbs/GO-RD4-REF.obj --regions $S/LOW/low_regions.json --out $S/LOW/GO-RD4-LOW.obj
python3 $T/p_maskplot.py $S/C_limbs/GO-RD4-REF.obj $S/LOW/GO-RD4-LOW_masks.npz $S/LOW/RD4_LOW_masks.png
```

Independent surface check: `tools/rac/w1/rmot05o_drivers/o_preserve.py`, with the `low_regions` converted to its format (`protect` = [name, c, r]; `tissue` = [name, c, r, amount, true]).

Sections: `tools/rac/w1/rmot05o_drivers/o_sections.py --station_z` with `LOW/station_z.json` (minus `_note`).

## Organism review overlay

```bash
python3 $T/p_org.py --org $N/ORG/GO-RD2-ORG-REF.obj --ref $N/RD2/GO-RD2-REF.obj --body $S/C_limbs/GO-RD4-REF.obj --dz 3.55 --out $S/organism/GO-RD4-ORG-REF.obj
```

## Renders

All renders use `$T/p_render.py` (see the `--items` lines in each image title).

The untouched source GO-RD0-SOURCE is rebuilt from `base.glb` by `tools/rac/w1/rmot05n_drivers/xf.py` (05N split of F1). It is not committed: it is derived and 10 MB.
