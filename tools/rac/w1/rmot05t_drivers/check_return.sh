#!/usr/bin/env bash
# RM-OT-05T return check (run from the release or repository root):
#   bash tools/rac/w1/rmot05t_drivers/check_return.sh EDITED.blend OUTDIR
# 1 export with the supported exporter, 2 exact identity / protection reintegration (REJECTS on any protected change),
# 3 pre-registered s_verify (05S gates, unchanged), 4 identical-camera before/after renders (needs bpy).
set -euo pipefail
BLEND="$1"; OUT="$2"; mkdir -p "$OUT"
Q=reviews/rac-rmot05q-evidence; S=reviews/rac-rmot05s-evidence; T=tools/rac/w1/rmot05t_drivers; S5=tools/rac/w1/rmot05s_drivers; IN=reviews/rac-rmot05t-release/inputs
[ -f "$OUT/F1_working.obj" ] || gunzip -c $Q/source/F1_working.obj.gz > "$OUT/F1_working.obj"
[ -f "$OUT/GO-05S-S3.obj" ] || gunzip -c $S/repair/S3/GO-05S-S3.obj.gz > "$OUT/GO-05S-S3.obj"
echo "17591025c24fd080e7fd45e3dc88dccc4707a0bee9efcb3fd70ef5ab6da453b0  $OUT/F1_working.obj" | sha256sum -c -
echo "1d50383376dc5dd2e249778c7b7d8330f4ec16daa21303656a146c0b4d81ac4c  $OUT/GO-05S-S3.obj" | sha256sum -c -
python3 $T/t_export_blend.py --blend "$BLEND" --out "$OUT/return"
python3 $T/t_reintegrate.py --ret "$OUT/return.npz" --s3 "$OUT/GO-05S-S3.obj" --s3maps $S/repair/S3/GO-05S-S3_maps.npz --s3labels $S/repair/S3/GO-05S-S3_face_labels.npy --out "$OUT/result" > "$OUT/reintegrate_stdout.json"
V=$(python3 -c "import json;print(json.load(open('$OUT/result_reintegrate.json'))['verdict'])"); echo "reintegration: $V"
if [ "$V" != "ACCEPTED_FOR_VERIFICATION" ]; then echo "REJECTED: protected geometry changed - see $OUT/result_reintegrate.json"; exit 2; fi
python3 $S5/s_verify.py --src "$OUT/F1_working.obj" --q05 $Q --plan $S/plan --res "$OUT/result.obj" --maps "$OUT/result_maps.npz" --labels "$OUT/result_face_labels.npy" --out "$OUT/result" > /dev/null
python3 -c "import json;r=json.load(open('$OUT/result_verify.json'));print('s_verify verdict:',r['verdict_automated']);[print(' ',k,v['pass_']) for k,v in r.items() if isinstance(v,dict)]"
if python3 -c "import bpy" 2>/dev/null; then
  R=tools/rac/w1/rmot05r_drivers
  for side in posterior anterior; do
    if [ $side = posterior ]; then CAM="--box 10 45 -28 5 148 180 --center 27.5 -10.5 162 --scale 18 --views 0:0,20:0,330:0,0:-45 --res 560"; else CAM="--box 10 45 -5 28 148 180 --center 29 9.5 163 --scale 18 --views 180:0,160:0,200:0,180:-45 --res 560"; fi
    python3 $R/r_compare.py --out "$OUT/compare_${side}_shaded.png" --rows "S3 (before)|$OUT/GO-05S-S3.obj|none" "RETURN (after)|$OUT/result.obj|none" -- $CAM
    python3 $R/r_compare.py --out "$OUT/compare_${side}_wire.png" --rows "S3 (before)|$OUT/GO-05S-S3.obj|none" "RETURN (after)|$OUT/result.obj|$OUT/result_face_labels.npy" -- $CAM --wire 1
  done
  python3 $R/r_compare.py --out "$OUT/compare_arm_views.png" --rows "S3 (before)|$OUT/GO-05S-S3.obj|none" "RETURN (after)|$OUT/result.obj|none" -- --box 10 60 -30 30 140 190 --center 31 -1 164 --scale 30 --views 180:0,90:0,0:0,135:10,45:10,180:-55 --res 480
else echo "bpy not available: renders skipped (do them in Blender with the same cameras, see START_HERE.md)"; fi
sha256sum "$BLEND" "$OUT"/return.npz "$OUT"/result.obj "$OUT"/result_verify.json > "$OUT/RETURN_HASHES.sha256"; echo "hashes: $OUT/RETURN_HASHES.sha256"
