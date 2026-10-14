#!/usr/bin/env bash
# RM-OT-05U7: check for the minimal upper-crease facet extension (frozen baseline = U6A cp3). Run from the repository root:
#   bash tools/rac/w1/rmot05u7_drivers/check_return_u7.sh EDITED.blend OUTDIR      (or: --npz RETURN.npz OUTDIR for fixtures)
# Steps: export (t_export_blend) -> U7 protection adapter vs cp3 -> s_verify on the P05U7 layout -> FROZEN crease reference (u4) ->
# U6 guards (no-regression) -> U7 local guards + facet diagnostic -> cp3-vs-U7 identical-camera renders -> U7 aggregate.
# Exit 0 only if every U7 safety gate passes (aggregate_u7.json); 2 = export failed; 3 = NOT MET. Never implies author acceptance.
set -uo pipefail
if [ "$1" = "--npz" ]; then NPZ="$2"; OUT="$3"; BLEND=""; else BLEND="$1"; OUT="$2"; NPZ=""; fi; mkdir -p "$OUT"
Q=reviews/rac-rmot05q-evidence; S=reviews/rac-rmot05s-evidence; PR=reviews/rac-rmot05u2-proposal
CP3=reviews/rac-rmot05u6-evidence/return_u6a/checks; SETS=reviews/rac-rmot05u7-evidence/readiness; U6SETS=reviews/rac-rmot05u6-evidence/readiness/u6_sets_v1.json
REF=reviews/rac-rmot05u4-readiness/crease_reference_v1.json
T=tools/rac/w1/rmot05t_drivers; S5=tools/rac/w1/rmot05s_drivers; U4=tools/rac/w1/rmot05u4_drivers; U6=tools/rac/w1/rmot05u6_drivers; U7=tools/rac/w1/rmot05u7_drivers; R=tools/rac/w1/rmot05r_drivers
[ -f "$OUT/F1_working.obj" ] || gunzip -c $Q/source/F1_working.obj.gz > "$OUT/F1_working.obj"
[ -f "$OUT/GO-05S-S3.obj" ] || gunzip -c $S/repair/S3/GO-05S-S3.obj.gz > "$OUT/GO-05S-S3.obj"
[ -f "$OUT/cp3_result.obj" ] || gunzip -c $CP3/result.obj.gz > "$OUT/cp3_result.obj"
if [ -n "$BLEND" ]; then python3 $T/t_export_blend.py --blend "$BLEND" --out "$OUT/return" || { echo "EXPORT FAILED"; exit 2; }; else cp "$NPZ" "$OUT/return.npz"; fi
rm -f "$OUT"/result_u7_reintegrate.json "$OUT"/result_verify.json "$OUT"/crease_measure.json "$OUT"/guards_u6.json "$OUT"/guards_u7.json "$OUT"/aggregate_u7.json
python3 $U7/u7_reintegrate.py --ret "$OUT/return.npz" --s3 "$OUT/GO-05S-S3.obj" --f1 "$OUT/F1_working.obj" --cp3 $CP3/return.npz --sets $SETS --out "$OUT/result"
V=$(python3 -c "import json;print(json.load(open('$OUT/result_u7_reintegrate.json'))['verdict'])" 2>/dev/null || echo MISSING); echo "U7 protection (vs cp3): $V"
if [ "$V" = "ACCEPTED_FOR_VERIFICATION_U7" ]; then
  NP=$(python3 -c "import json;print(json.load(open('$SETS/u7_sets_v1.json'))['layout']['n_prot'])"); PS=$(python3 -c "import json;print(json.load(open('$SETS/u7_sets_v1.json'))['layout']['prot_sha'])")
  python3 $S5/s_verify.py --src "$OUT/F1_working.obj" --q05 $Q --plan $S/plan --res "$OUT/result.obj" --maps "$OUT/result_maps.npz" --labels "$OUT/result_face_labels.npy" \
    --nprot $NP --prot_sha $PS --prot_faces_file $SETS/P05U7_preview.npz:P05U7_src_ordered --src_exempt "$OUT/result_src_exempt_f1.npy" --out "$OUT/result" > /dev/null || echo "s_verify did not complete"
fi
python3 $U4/u4_crease_ref.py measure --s3 "$OUT/GO-05S-S3.obj" --proposal $PR --ret "$OUT/return.npz" --ref $REF --out "$OUT/crease_measure.json"
python3 $U6/u6_guards.py --s3 "$OUT/GO-05S-S3.obj" --ret "$OUT/return.npz" --sets $U6SETS --out "$OUT/guards_u6.json" > /dev/null || echo "u6 guards did not complete"
python3 $U7/u7_guards.py --s3 "$OUT/GO-05S-S3.obj" --ret "$OUT/return.npz" --cp3 $CP3/return.npz --sets $SETS --out "$OUT/guards_u7.json" || echo "u7 guards did not complete"
if [ "$V" = "ACCEPTED_FOR_VERIFICATION_U7" ] && python3 -c "import bpy" 2>/dev/null; then
  for side in posterior zoom upper; do
    case $side in posterior) CAM="--box 10 45 -28 5 148 180 --center 27.5 -10.5 162 --scale 18 --views 0:0,20:0,330:0,0:-45 --res 560";;
                  zoom) CAM="--box 10 45 -28 5 148 180 --center 28.9 -13.3 167.5 --scale 11 --views 0:0,20:0,330:0,0:-45 --res 560";;
                  upper) CAM="--box 10 45 -28 5 148 180 --center 28.9 -13.9 171.0 --scale 7 --views 0:0,20:0,330:0,0:-45 --res 560";; esac
    python3 $R/r_compare.py --out "$OUT/compare_${side}_shaded.png" --rows "U6A cp3 (before)|$OUT/cp3_result.obj|none" "U7 (after)|$OUT/result.obj|none" -- $CAM
    python3 $R/r_compare.py --out "$OUT/compare_${side}_wire.png" --rows "U6A cp3 (before)|$OUT/cp3_result.obj|none" "U7 (after)|$OUT/result.obj|none" -- $CAM --wire 1
  done
  python3 $R/r_compare.py --out "$OUT/compare_context_lateral_34_underside.png" --rows "U6A cp3 (before)|$OUT/cp3_result.obj|none" "U7 (after)|$OUT/result.obj|none" -- --box 10 45 -28 5 148 180 --center 28.9 -13.6 169.5 --scale 16 --views 90:0,45:10,315:10,0:-60 --res 520
fi
python3 $U7/u7_aggregate.py --reint "$OUT/result_u7_reintegrate.json" --verify "$OUT/result_verify.json" --crease "$OUT/crease_measure.json" --guards6 "$OUT/guards_u6.json" --guards7 "$OUT/guards_u7.json" --ref $REF --out "$OUT/aggregate_u7.json"; RC=$?
FILES=""; for f in return.npz result.obj result_verify.json result_u7_reintegrate.json crease_measure.json guards_u6.json guards_u7.json aggregate_u7.json; do [ -f "$OUT/$f" ] && FILES="$FILES $OUT/$f"; done
sha256sum ${BLEND:+"$BLEND"} $FILES > "$OUT/RETURN_HASHES.sha256"
echo "hashes: $OUT/RETURN_HASHES.sha256 | exit $RC"; exit $RC
