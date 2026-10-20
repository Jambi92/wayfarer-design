#!/bin/bash
# featfit3.sh IN OUT "x,y,z" "R.." EVALR : chord-error fit (fit3.py, LAP) + collision-free local relax
IN=$1; OUT=$2; C=$3; RS=$4; ER=$5
for r in $RS; do
  T=/tmp/claude-0/f3_$$_$r
  LAP=${LAP:-0.15} python3 fit3.py $IN $T.npz $C $r ${NIT:-150} > $T.log 2>&1
  REG=$C,$ER timeout 3000 /home/claude/stc/bin/python3 fixall.py -- $T.npz ${T}s.npz 40 0.0 0.7 > ${T}s.log 2>&1
  H=$(grep history ${T}s.log | cut -c1-60)
  P=$(timeout 900 /home/claude/stc/bin/python3 /tmp/claude-0/regsx.py -- ${T}s.npz "($C)" $ER 2>&1 | head -1)
  D=$(python3 /tmp/claude-0/regdev2.py ${T}s.npz "($C)" $ER -)
  echo "R=$r $(tail -1 $T.log) | fix $H | $P | $D"
  if [[ "$P" == "region pairs 0" && "$D" == *DEVPASS* ]]; then cp ${T}s.npz $OUT; echo "ACCEPT R=$r -> $OUT"; exit 0; fi
done
echo "NO PASS"; exit 1
