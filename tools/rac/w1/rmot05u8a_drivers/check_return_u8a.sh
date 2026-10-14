#!/usr/bin/env bash
# RM-OT-05U8A: check for the controlled crease-anchor release (frozen baseline = U8 cp1; additive copy of check_return_u8.sh).
#   bash tools/rac/w1/rmot05u8a_drivers/check_return_u8a.sh EDITED.blend OUTDIR      (or: --npz RETURN.npz OUTDIR for fixtures)
# Steps: export -> U8A protection adapter vs U8 cp1 -> s_verify on the P05U8A layout -> FROZEN crease reference (u4, unchanged file and
# thresholds) -> U6 / U7 / U8 guards (no-regression) -> U8A local guards, anchor step limits + dihedral diagnostic -> U8cp1-vs-U8A renders -> U8A aggregate.
# Exit 0 only if every U8A safety gate passes (aggregate_u8a.json); 2 = export failed; 3 = NOT MET. Never implies author acceptance.
set -uo pipefail
if [ "$1" = "--npz" ]; then NPZ="$2"; OUT="$3"; BLEND=""; else BLEND="$1"; OUT="$2"; NPZ=""; fi; mkdir -p "$OUT"
Q=reviews/rac-rmot05q-evidence; S=reviews/rac-rmot05s-evidence; PR=reviews/rac-rmot05u2-proposal
CP1=reviews/rac-rmot05u8-evidence/return/checks; CP2=reviews/rac-rmot05u7-evidence/return/checks; CP3=reviews/rac-rmot05u6-evidence/return_u6a/checks
SETSA=reviews/rac-rmot05u8a-evidence/readiness; SETS=reviews/rac-rmot05u8-evidence/readiness; SETS7=reviews/rac-rmot05u7-evidence/readiness; U6SETS=reviews/rac-rmot05u6-evidence/readiness/u6_sets_v1.json
REF=reviews/rac-rmot05u4-readiness/crease_reference_v1.json
T=tools/rac/w1/rmot05t_drivers; S5=tools/rac/w1/rmot05s_drivers; U4=tools/rac/w1/rmot05u4_drivers; U6=tools/rac/w1/rmot05u6_drivers; U7=tools/rac/w1/rmot05u7_drivers; U8=tools/rac/w1/rmot05u8_drivers; U8A=tools/rac/w1/rmot05u8a_drivers; R=tools/rac/w1/rmot05r_drivers
[ -f "$OUT/F1_working.obj" ] || gunzip -c $Q/source/F1_working.obj.gz > "$OUT/F1_working.obj"
[ -f "$OUT/GO-05S-S3.obj" ] || gunzip -c $S/repair/S3/GO-05S-S3.obj.gz > "$OUT/GO-05S-S3.obj"
[ -f "$OUT/u8cp1_result.obj" ] || gunzip -c $CP1/result.obj.gz > "$OUT/u8cp1_result.obj"
if [ -n "$BLEND" ]; then python3 $T/t_export_blend.py --blend "$BLEND" --out "$OUT/return" || { echo "EXPORT FAILED"; exit 2; }; else cp "$NPZ" "$OUT/return.npz"; fi
rm -f "$OUT"/result_u8a_reintegrate.json "$OUT"/result_verify.json "$OUT"/crease_measure.json "$OUT"/guards_u6.json "$OUT"/guards_u7.json "$OUT"/guards_u8.json "$OUT"/guards_u8a.json "$OUT"/aggregate_u8a.json
python3 $U8A/u8a_reintegrate.py --ret "$OUT/return.npz" --s3 "$OUT/GO-05S-S3.obj" --f1 "$OUT/F1_working.obj" --cp3 $CP1/return.npz --sets $SETSA --out "$OUT/result"
V=$(python3 -c "import json;print(json.load(open('$OUT/result_u8a_reintegrate.json'))['verdict'])" 2>/dev/null || echo MISSING); echo "U8A protection (vs U8 cp1): $V"
if [ "$V" = "ACCEPTED_FOR_VERIFICATION_U8A" ]; then
  NP=$(python3 -c "import json;print(json.load(open('$SETSA/u8a_sets_v1.json'))['layout']['n_prot'])"); PS=$(python3 -c "import json;print(json.load(open('$SETSA/u8a_sets_v1.json'))['layout']['prot_sha'])")
  python3 $S5/s_verify.py --src "$OUT/F1_working.obj" --q05 $Q --plan $S/plan --res "$OUT/result.obj" --maps "$OUT/result_maps.npz" --labels "$OUT/result_face_labels.npy" \
    --nprot $NP --prot_sha $PS --prot_faces_file $SETSA/P05U8A_preview.npz:P05U8A_src_ordered --src_exempt "$OUT/result_src_exempt_f1.npy" --out "$OUT/result" > /dev/null || echo "s_verify did not complete"
fi
python3 $U4/u4_crease_ref.py measure --s3 "$OUT/GO-05S-S3.obj" --proposal $PR --ret "$OUT/return.npz" --ref $REF --out "$OUT/crease_measure.json"
python3 $U6/u6_guards.py --s3 "$OUT/GO-05S-S3.obj" --ret "$OUT/return.npz" --sets $U6SETS --out "$OUT/guards_u6.json" > /dev/null || echo "u6 guards did not complete"
python3 $U7/u7_guards.py --s3 "$OUT/GO-05S-S3.obj" --ret "$OUT/return.npz" --cp3 $CP3/return.npz --sets $SETS7 --out "$OUT/guards_u7.json" > /dev/null || echo "u7 guards did not complete"
python3 $U8/u8_guards.py --s3 "$OUT/GO-05S-S3.obj" --ret "$OUT/return.npz" --cp2 $CP2/return.npz --sets $SETS --out "$OUT/guards_u8.json" > /dev/null || echo "u8 guards did not complete"
python3 $U8A/u8a_guards.py --s3 "$OUT/GO-05S-S3.obj" --ret "$OUT/return.npz" --cp2 $CP1/return.npz --sets $SETSA --out "$OUT/guards_u8a.json" || echo "u8a guards did not complete"
if [ "$V" = "ACCEPTED_FOR_VERIFICATION_U8A" ] && python3 -c "import bpy" 2>/dev/null; then
  for side in posterior zoom lower upper; do
    case $side in posterior) CAM="--box 10 45 -28 5 148 180 --center 27.5 -10.5 162 --scale 18 --views 0:0,20:0,330:0,0:-45 --res 560";;
                  zoom) CAM="--box 10 45 -28 5 148 180 --center 28.9 -13.3 167.5 --scale 11 --views 0:0,20:0,330:0,0:-45 --res 560";;
                  lower) CAM="--box 10 45 -28 5 148 180 --center 28.8 -13.3 169.3 --scale 6 --views 0:0,20:0,330:0,0:-45 --res 560";;
                  upper) CAM="--box 10 45 -28 5 148 180 --center 29.0 -14.2 172.3 --scale 6 --views 0:0,20:0,330:0,0:-45 --res 560";; esac
    python3 $R/r_compare.py --out "$OUT/compare_${side}_shaded.png" --rows "U8 cp1 (before)|$OUT/u8cp1_result.obj|none" "U8A (after)|$OUT/result.obj|none" -- $CAM
    python3 $R/r_compare.py --out "$OUT/compare_${side}_wire.png" --rows "U8 cp1 (before)|$OUT/u8cp1_result.obj|none" "U8A (after)|$OUT/result.obj|none" -- $CAM --wire 1
  done
  python3 $R/r_compare.py --out "$OUT/compare_context_lateral_34_underside.png" --rows "U8 cp1 (before)|$OUT/u8cp1_result.obj|none" "U8A (after)|$OUT/result.obj|none" -- --box 10 45 -28 5 148 180 --center 28.9 -13.6 169.5 --scale 16 --views 90:0,45:10,315:10,0:-60 --res 520
fi
python3 $U8A/u8a_aggregate.py --reint "$OUT/result_u8a_reintegrate.json" --verify "$OUT/result_verify.json" --crease "$OUT/crease_measure.json" --guards6 "$OUT/guards_u6.json" --guards7 "$OUT/guards_u7.json" --guards8 "$OUT/guards_u8.json" --guards8a "$OUT/guards_u8a.json" --ref $REF --out "$OUT/aggregate_u8a.json"; RC=$?
FILES=""; for f in return.npz result.obj result_verify.json result_u8a_reintegrate.json crease_measure.json guards_u6.json guards_u7.json guards_u8.json guards_u8a.json aggregate_u8a.json; do [ -f "$OUT/$f" ] && FILES="$FILES $OUT/$f"; done
sha256sum ${BLEND:+"$BLEND"} $FILES > "$OUT/RETURN_HASHES.sha256"
echo "hashes: $OUT/RETURN_HASHES.sha256 | exit $RC"; exit $RC
