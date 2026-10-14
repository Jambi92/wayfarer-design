#!/usr/bin/env bash
# RM-OT-05U3: OPT-IN U2 return check (NON-PRODUCTION until Tyler approves the 05U2 boundary). Run from the repository root:
#   bash tools/rac/w1/rmot05u3_drivers/check_return_u2.sh EDITED.blend OUTDIR
# 1 supported export (t_export_blend.py), 2 U2 adapter (pinned proposal lists, frozen 05U baseline, no-topology-change,
# exact protection outside the 365 / 832, legacy V1 diagnostic), 3 s_verify in U2 mode (V1-U2 + unchanged V2-V6c),
# 4 identical-camera before (05U RETURN) / after renders with U2 labels (label 6 = edited source surface, cyan).
# The default 05T/05U path (tools/rac/w1/rmot05t_drivers/check_return.sh) is unchanged and remains the active rule.
# SUPERSEDED by tools/rac/w1/rmot05u4_drivers/check_return_u2.sh (RM-OT-05U4): this historical version re-derives the crease
# section planes from the RETURNED mesh (moving-plane limitation) and does not fail the command on a failed depth check.
set -euo pipefail
BLEND="$1"; OUT="$2"; mkdir -p "$OUT"
Q=reviews/rac-rmot05q-evidence; S=reviews/rac-rmot05s-evidence; U=reviews/rac-rmot05u-evidence/checks/return; PR=reviews/rac-rmot05u2-proposal
T=tools/rac/w1/rmot05t_drivers; S5=tools/rac/w1/rmot05s_drivers; U3=tools/rac/w1/rmot05u3_drivers; R=tools/rac/w1/rmot05r_drivers
[ -f "$OUT/F1_working.obj" ] || gunzip -c $Q/source/F1_working.obj.gz > "$OUT/F1_working.obj"
[ -f "$OUT/GO-05S-S3.obj" ] || gunzip -c $S/repair/S3/GO-05S-S3.obj.gz > "$OUT/GO-05S-S3.obj"
[ -f "$OUT/baseline_05U_result.obj" ] || gunzip -c $U/result.obj.gz > "$OUT/baseline_05U_result.obj"
python3 $T/t_export_blend.py --blend "$BLEND" --out "$OUT/return"
python3 $U3/u3_reintegrate.py --ret "$OUT/return.npz" --proposal $PR --s3 "$OUT/GO-05S-S3.obj" --baseline $U/return.npz --f1 "$OUT/F1_working.obj" --out "$OUT/result"
V=$(python3 -c "import json;print(json.load(open('$OUT/result_u2_reintegrate.json'))['verdict'])"); echo "U2 reintegration: $V"
if [ "$V" != "ACCEPTED_FOR_VERIFICATION_U2" ]; then echo "REJECTED - see $OUT/result_u2_reintegrate.json"; exit 2; fi
python3 $S5/s_verify.py --src "$OUT/F1_working.obj" --q05 $Q --plan $S/plan --res "$OUT/result.obj" --maps "$OUT/result_maps.npz" --labels "$OUT/result_face_labels.npy" \
  --nprot 139772 --prot_sha 25ffe5ac83d60e81b1026baf91bf3dbc07d7dc7136a8495f77f5581920328ffd --prot_faces_file $PR/P05U2_preview.npz:P05U2_src_ordered --src_exempt "$OUT/result_src_exempt_f1.npy" --out "$OUT/result" > /dev/null
python3 -c "import json;r=json.load(open('$OUT/result_verify.json'));print('s_verify (U2 mode) verdict:',r['verdict_automated']);[print(' ',k,v['pass_']) for k,v in r.items() if isinstance(v,dict) and 'pass_' in v]"
python3 $U3/u3_crease.py --s3 "$OUT/GO-05S-S3.obj" --baseline "$OUT/return.npz" --proposal $PR --out "$OUT/crease" > "$OUT/crease_stdout.json"
python3 -c "
import json;b=json.load(open('reviews/rac-rmot05u3-readiness/crease/crease_baseline.json'));r=json.load(open('$OUT/crease/crease_baseline.json'))
for x,y in zip(b['results'],r['results']): print(' crease',x['name'],'baseline',x['depth_cm'],'limit',x['limit_75pct_cm'],'now',y.get('depth_cm'),'PASS' if y.get('depth_cm',0)>=x['limit_75pct_cm'] else 'FAIL')"
python3 $U3/u3_guards.py --s3 "$OUT/GO-05S-S3.obj" --ret "$OUT/return.npz" --baseline $U/return.npz --proposal $PR --out "$OUT/guards.json"
if python3 -c "import bpy" 2>/dev/null; then
  for side in posterior zoom; do
    if [ $side = posterior ]; then CAM="--box 10 45 -28 5 148 180 --center 27.5 -10.5 162 --scale 18 --views 0:0,20:0,330:0,0:-45 --res 560"; else CAM="--box 10 45 -28 5 148 180 --center 28.9 -13.3 167.5 --scale 11 --views 0:0,20:0,330:0,0:-45 --res 560"; fi
    python3 $R/r_compare.py --out "$OUT/compare_${side}_shaded.png" --rows "05U RETURN (before)|$OUT/baseline_05U_result.obj|none" "U2 RETURN (after)|$OUT/result.obj|none" -- $CAM
    python3 $R/r_compare.py --out "$OUT/compare_${side}_wire.png" --rows "05U RETURN (before)|$OUT/baseline_05U_result.obj|none" "U2 RETURN (after; cyan = label 6)|$OUT/result.obj|$OUT/result_face_labels.npy" -- $CAM --wire 1
  done
  python3 $R/r_compare.py --out "$OUT/compare_arm_views.png" --rows "05U RETURN (before)|$OUT/baseline_05U_result.obj|none" "U2 RETURN (after)|$OUT/result.obj|none" -- --box 10 60 -30 30 140 190 --center 31 -1 164 --scale 30 --views 180:0,90:0,0:0,135:10,45:10,180:-55 --res 480
fi
sha256sum "$BLEND" "$OUT"/return.npz "$OUT"/result.obj "$OUT"/result_verify.json "$OUT"/result_u2_reintegrate.json "$OUT"/guards.json > "$OUT/RETURN_HASHES.sha256"; echo "hashes: $OUT/RETURN_HASHES.sha256"
