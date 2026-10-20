# dtarget.py DMASK.npz KEYS PREFIX_IN PREFIX_OUT cols : copy targets PREFIX_IN_c<col>.npz -> PREFIX_OUT_c<col>.npz without faces touching D-mask vertices
import sys, os, numpy as np
from scipy.spatial import cKDTree
m=np.load(sys.argv[1]); keys=sys.argv[2].split(','); pin,pout=sys.argv[3],sys.argv[4]; cols=[int(c) for c in sys.argv[5].split(',')]
S=np.load('/home/claude/stc/rp1/weld.npz')['V'].astype(float)
D=np.concatenate([m[k+'_idx'][m[k+'_esc']==0] for k in keys]); Dm=np.zeros(len(S),bool); Dm[D]=True
for c in cols:
    src=pin+'_c%d.npz'%c; t=np.load(src); TV=t['V'].astype(float); TF=t['F'].astype(np.int64)
    d,i=cKDTree(S).query(TV); assert d.max()<1e-4
    bad=Dm[i][TF].any(1); Fc=TF[~bad]; used=np.unique(Fc); mp=-np.ones(len(TV),int); mp[used]=np.arange(len(used))
    dst=pout+'_c%d.npz'%c
    if os.path.islink(dst): os.remove(dst)
    np.savez_compressed(dst,V=TV[used],F=mp[Fc]); print(c,'removed faces',int(bad.sum()))
