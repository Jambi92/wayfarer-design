import numpy as np,sys
from scipy.spatial import cKDTree
tag=sys.argv[1]; R=float(sys.argv[2]); th=float(sys.argv[3])
S=np.load('/home/claude/stc/rp1/weld.npz')['V'].astype(float)
d=np.load('sim_%s_L4_dsp.npy'%tag); P=np.load('sim_%s_L4.npz'%tag)['V']*np.array([1,-1,1])
kp=cKDTree(P); C=np.load(sys.argv[4])['V'] if len(sys.argv)>4 else None
for c in eval(sys.argv[5] if len(sys.argv)>5 else '[]'):
    m=(np.linalg.norm(S-np.array(c),axis=1)<R)&(d>th)
    if not m.any(): print(c,'none'); continue
    i=np.where(m)[0]; j=kp.query(S[i])[1]; dv=(P[j]-S[i]); k=i[np.argmax(d[i])]
    near=np.argsort(np.linalg.norm(C-S[k],axis=1))[:5] if C is not None else []
    print(c,'n',m.sum(),'max',d[i].max().round(2),'at',S[k].round(2),'box',S[i].min(0).round(2),S[i].max(0).round(2),'dir',dv.mean(0).round(2),'cage',list(map(int,near)))
