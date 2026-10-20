# runc.sh TAG CAGE.npz BASEFSM [addnew=0] : sim with r3 targets; fsm = remapped base (+ new verts if addnew)
T=$1; C=$2; B=$3; A=${4:-0}
python3 - $C $B $T $A <<'PY'
import numpy as np, sys
C,B,T,A=sys.argv[1:5]; rm=np.load(C.replace('.npz','_remap.npy')); n=len(np.load(C)['V'])
old=[int(t) for t in open(B).read().split()]; ids=set(int(rm[i]) for i in old if i<len(rm) and rm[i]>=0)
if A=='1':
    img=set(int(x) for x in rm if x>=0); ids|=set(i for i in range(n) if i not in img)
open('fsm_%s.txt'%T,'w').write(' '.join(map(str,sorted(ids))))
PY
cp $C cage_$T.npz; cp ${C%.npz}_col.npy cage_${T}_col.npy
TPRE=tg_r3m5 FINALSM=3 FSMF=0.5 FSMV=$PWD/fsm_$T.txt ./runv.sh $T cage_$T.npz cage_${T}_col.npy PN 1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24 > /dev/null 2>&1
grep -E "L4_sx" $T.log | cut -c1-160
