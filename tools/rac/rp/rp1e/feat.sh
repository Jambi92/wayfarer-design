#!/bin/bash
# feat.sh IN OUT "x,y,z" "r1 r2 .." EVALR [EXCLFACES] [LID] : final-res local fix = disk remap + collision-free local relax; first passing r wins
IN=$1; OUT=$2; C=$3; RS=$4; ER=$5; EX=${6:--}; LIDV=${7:-}
EXV=-; [ "$EX" != "-" ] && EXV=${EX%_faces.npy}_vertices.npy
for r in $RS; do
  T=/tmp/claude-0/ft_$$_$r
  if [ "$EX" != "-" ]; then LID=$LIDV timeout 900 python3 remap.py $IN $T.npz "($C)" $r $EX > $T.log 2>&1; else timeout 900 python3 remap.py $IN $T.npz "($C)" $r > $T.log 2>&1; fi
  [ -f $T.npz ] || { echo "r=$r remap failed: $(tail -1 $T.log)"; continue; }
  SRCV=; [ -f ${T}_src.npz ] && SRCV=${T}_src.npz
  SRC=${SRCV:-/home/claude/stc/rp1/weld_a.npz} REG=$C,$ER timeout 3000 /home/claude/stc/bin/python3 fixall.py -- $T.npz ${T}s.npz 40 0.0 0.7 > ${T}s.log 2>&1
  H=$(grep history ${T}s.log | cut -c1-80)
  P=$(timeout 900 /home/claude/stc/bin/python3 /tmp/claude-0/regsx.py -- ${T}s.npz "($C)" $ER 2>&1 | head -1)
  D=$(python3 /tmp/claude-0/regdev2.py ${T}s.npz "($C)" $ER $EXV)
  echo "r=$r $(grep patch $T.log | cut -c1-120) | fix $H | $P | $D"
  if [[ "$P" == "region pairs 0" && "$D" == *DEVPASS* ]]; then cp ${T}s.npz $OUT; echo "ACCEPT r=$r -> $OUT"; exit 0; fi
done
echo "NO PASS"; exit 1
