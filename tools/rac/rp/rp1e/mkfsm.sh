# mkfsm.sh NEW.npz REMAP.npy BASEFSM OUTFSM : remap a smoothing-group id list and add all new verts
python3 - "$@" <<'PY'
import numpy as np, sys
new,rmp,base,out=sys.argv[1:5]
rm=np.load(rmp); n=len(np.load(new)['V'])
old=[int(t) for t in open(base).read().split()]
ids=set(int(rm[i]) for i in old if i<len(rm) and rm[i]>=0); img=set(int(x) for x in rm if x>=0); ids|=set(i for i in range(n) if i not in img)
open(out,'w').write(' '.join(map(str,sorted(ids))))
PY
