# RAC W1m AS RUN: AEL1 (leg-rebalanced Aelari) reference, minimum-composition and composition-grid bodies for the CIB skeletal rows
# (same generator route as the W1g AE: build_variant on the candidate build record, height macro held). Files named AE* in their own folders.
cd /home/claude/wayfarer-design/tools/rac/w1
D=/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1m/ael1; mkdir -p $D/final $D/lean $D/comp
cp /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1m/legs/AEL1_build.json $D/final/AE_build.json
python3 - <<P
import json
b=json.load(open('$D/final/AE_build.json')); b['id']='AE'; b['cfg']['id']='AE'; json.dump(b,open('$D/final/AE_build.json','w'))
P
for st in rest r6; do cp /tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w1m/legs/AEL1_$st.npz $D/final/AE_$st.npz; done
echo '{"muscle": 0.0, "weight": 0.0}' > $D/lean/AE-LEAN.ov.json
python3 build_variant.py $D/final/AE_build.json $D/lean/AE-LEAN.ov.json $D/lean AE-LEAN
for mw in "0.0 0.25" "0.0 0.5" "0.25 0.0" "0.25 0.25" "0.25 0.5" "0.5 0.0" "0.5 0.25"; do set -- $mw
  t=$(python3 -c "print('C%03d%03d'%(round($1*100),round($2*100)))"); echo "{\"muscle\": $1, \"weight\": $2}" > $D/comp/AE-$t.ov.json
  python3 build_variant.py $D/final/AE_build.json $D/comp/AE-$t.ov.json $D/comp AE-$t; done
echo GRID_DONE
