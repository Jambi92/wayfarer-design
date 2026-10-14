#!/usr/bin/env bash
# RM-OT-05U4: OPT-IN U2 return check with FIXED crease references and an aggregate exit status (supersedes
# tools/rac/w1/rmot05u3_drivers/check_return_u2.sh, whose crease step re-derived the section planes from the returned mesh).
# NON-PRODUCTION until Tyler approves the 05U2 boundary. Run from the repository root:
#   bash tools/rac/w1/rmot05u4_drivers/check_return_u2.sh EDITED.blend OUTDIR      (or: --npz RETURN.npz OUTDIR for fixtures)
# Exit 0 only if the numerical stop conditions pass (aggregate.json); 2 = export failed; 3 = stop conditions NOT MET.
# Diagnostics, renders and hashes are kept wherever possible even on failure. Never implies author acceptance.
set -uo pipefail
if [ "$1" = "--npz" ]; then NPZ="$2"; OUT="$3"; BLEND=""; else BLEND="$1"; OUT="$2"; NPZ=""; fi; mkdir -p "$OUT"
Q=reviews/rac-rmot05q-evidence; S=reviews/rac-rmot05s-evidence; U=reviews/rac-rmot05u-evidence/checks/return; PR=reviews/rac-rmot05u2-proposal
REF=reviews/rac-rmot05u4-readiness/crease_reference_v1.json
T=tools/rac/w1/rmot05t_drivers; S5=tools/rac/w1/rmot05s_drivers; U3=tools/rac/w1/rmot05u3_drivers; U4=tools/rac/w1/rmot05u4_drivers; R=tools/rac/w1/rmot05r_drivers
[ -f "$OUT/F1_working.obj" ] || gunzip -c $Q/source/F1_working.obj.gz > "$OUT/F1_working.obj"
[ -f "$OUT/GO-05S-S3.obj" ] || gunzip -c $S/repair/S3/GO-05S-S3.obj.gz > "$OUT/GO-05S-S3.obj"
[ -f "$OUT/baseline_05U_result.obj" ] || gunzip -c $U/result.obj.gz > "$OUT/baseline_05U_result.obj"
if [ -n "$BLEND" ]; then python3 $T/t_export_blend.py --blend "$BLEND" --out "$OUT/return" || { echo "EXPORT FAILED"; exit 2; }; else cp "$NPZ" "$OUT/return.npz"; fi
rm -f "$OUT/result_u2_reintegrate.json" "$OUT/result_verify.json" "$OUT/crease_measure.json" "$OUT/guards.json" "$OUT/aggregate.json"
python3 $U3/u3_reintegrate.py --ret "$OUT/return.npz" --proposal $PR --s3 "$OUT/GO-05S-S3.obj" --baseline $U/return.npz --f1 "$OUT/F1_working.obj" --out "$OUT/result"
V=$(python3 -c "import json;print(json.load(open('$OUT/result_u2_reintegrate.json'))['verdict'])" 2>/dev/null || echo MISSING); echo "U2 reintegration (protection only): $V"
if [ "$V" = "ACCEPTED_FOR_VERIFICATION_U2" ]; then
  python3 $S5/s_verify.py --src "$OUT/F1_working.obj" --q05 $Q --plan $S/plan --res "$OUT/result.obj" --maps "$OUT/result_maps.npz" --labels "$OUT/result_face_labels.npy" \
    --nprot 139772 --prot_sha 25ffe5ac83d60e81b1026baf91bf3dbc07d7dc7136a8495f77f5581920328ffd --prot_faces_file $PR/P05U2_preview.npz:P05U2_src_ordered --src_exempt "$OUT/result_src_exempt_f1.npy" --out "$OUT/result" > /dev/null \
    || echo "s_verify did not complete"
fi
python3 $U4/u4_crease_ref.py measure --s3 "$OUT/GO-05S-S3.obj" --proposal $PR --ret "$OUT/return.npz" --ref $REF --out "$OUT/crease_measure.json"
python3 $U3/u3_guards.py --s3 "$OUT/GO-05S-S3.obj" --ret "$OUT/return.npz" --baseline $U/return.npz --proposal $PR --out "$OUT/guards.json" || echo "guards did not complete"
if [ "$V" = "ACCEPTED_FOR_VERIFICATION_U2" ] && python3 -c "import bpy" 2>/dev/null; then
  for side in posterior zoom; do
    if [ $side = posterior ]; then CAM="--box 10 45 -28 5 148 180 --center 27.5 -10.5 162 --scale 18 --views 0:0,20:0,330:0,0:-45 --res 560"; else CAM="--box 10 45 -28 5 148 180 --center 28.9 -13.3 167.5 --scale 11 --views 0:0,20:0,330:0,0:-45 --res 560"; fi
    python3 $R/r_compare.py --out "$OUT/compare_${side}_shaded.png" --rows "05U RETURN (before)|$OUT/baseline_05U_result.obj|none" "U2 RETURN (after)|$OUT/result.obj|none" -- $CAM
    python3 $R/r_compare.py --out "$OUT/compare_${side}_wire.png" --rows "05U RETURN (before)|$OUT/baseline_05U_result.obj|none" "U2 RETURN (after; cyan = label 6)|$OUT/result.obj|$OUT/result_face_labels.npy" -- $CAM --wire 1
  done
  python3 $R/r_compare.py --out "$OUT/compare_arm_views.png" --rows "05U RETURN (before)|$OUT/baseline_05U_result.obj|none" "U2 RETURN (after)|$OUT/result.obj|none" -- --box 10 60 -30 30 140 190 --center 31 -1 164 --scale 30 --views 180:0,90:0,0:0,135:10,45:10,180:-55 --res 480
fi
python3 $U4/u4_aggregate.py --reint "$OUT/result_u2_reintegrate.json" --verify "$OUT/result_verify.json" --crease "$OUT/crease_measure.json" --guards "$OUT/guards.json" --ref $REF --out "$OUT/aggregate.json"; RC=$?
FILES=""; for f in return.npz result.obj result_verify.json result_u2_reintegrate.json crease_measure.json guards.json aggregate.json; do [ -f "$OUT/$f" ] && FILES="$FILES $OUT/$f"; done
sha256sum ${BLEND:+"$BLEND"} $FILES > "$OUT/RETURN_HASHES.sha256"
echo "hashes: $OUT/RETURN_HASHES.sha256 | exit $RC"; exit $RC
