# RAC W3C (RM-CF-09) as run. S = session scratchpad; bpy-enabled python3; run from tools/rac/w1.
# override sets: reviews/rac-w3c-sk-evidence/overrides/*.ov.json (copied to $S/w3c/ov)
python3 build_variant.py $S/w1f/final/MF-M-R_build.json $S/w3c/ov/H183.ov.json $S/w3c/b MFM183
for p in "SKN_LOW SKM190-NLOW SK" "MFN_LOW MFM190-NLOW MF" "SKB SKM190-B SK" "MFB MFM190-B MF" "C1 SKM190-C1 SK" "C2 SKM190-C2 SK" "C3 SKM190-C3 SK" \
         "SKOV_BROW SKM190-SKOV_BROW SK" "SKOV_JAW SKM190-SKOV_JAW SK" "SKOV_MID SKM190-SKOV_MID SK" "MFOV_BROW MFM190-MFOV_BROW MF" "MFOV_JAW MFM190-MFOV_JAW MF" "MFOV_MID MFM190-MFOV_MID MF"; do
  set -- $p; base=$S/w2b/st/${3}M190_build.json; [ $3 = MF ] && base=$S/w2b/st/MFM190_build.json; [ $3 = SK ] && base=$S/w2b/st/SKM190_build.json
  python3 build_variant.py $base $S/w3c/ov/$1.ov.json $S/w3c/b $2; done
python3 build_variant.py $S/w2b/st/SKF190_build.json $S/w3c/ov/C1.ov.json $S/w3c/b SKF190-C1
cd w3c_drivers; python3 w3c_measure.py; python3 w3c_sheets.py; python3 w3c_tables.py
