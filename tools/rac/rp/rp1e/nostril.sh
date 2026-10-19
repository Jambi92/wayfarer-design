# nostril.sh IN OUT "top,c,bot" "tx,ty,tz" [fu] [fd] [lipoff] : refine the two spoke edges of c and crease top'-c-bot' with the tip at the nostril floor
IN=$1; OUT=$2; IFS=, read t c b <<< "$3"; T=$4; FU=${5:-0.25}; FD=${6:-0.45}; LO=${7:-0.5}
W=/tmp/claude-0/ns; mkdir -p $W
n1=$(python3 -c "import numpy as np;print(len(np.load('$IN.npz')['V']))")
p=$(python3 -c "import numpy as np;V=np.load('$IN.npz')['V'];print(','.join(map(str,(V[$c]+$FU*(V[$t]-V[$c])).tolist())))")
python3 slotN.py $IN.npz ${IN}_col.npy $W/a.npz $c $t $p >/dev/null || exit 1
n2=$((n1+1))
p=$(python3 -c "import numpy as np;V=np.load('$W/a.npz')['V'];print(','.join(map(str,(V[$c]+$FD*(V[$b]-V[$c])).tolist())))")
python3 slotN.py $W/a.npz $W/a_col.npy $W/b.npz $c $b $p >/dev/null || exit 1
python3 - <<PY
import json; json.dump({"path":[$n1,$c,$n2],"tip":[None,[$T],None],"A":["auto"],"B":["auto"],"lipoff":$LO,"lipsnap":False},open('$W/spec.json','w'))
PY
python3 pathbevel.py $W/b.npz $W/b_col.npy $OUT.npz $W/spec.json || exit 1
/home/claude/stc/bin/python3 selfx_npz.py -- $OUT.npz 2>&1 | grep SELFX
