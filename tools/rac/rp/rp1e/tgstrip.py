# tgstrip.py PREFIX_OUT "centre" R a,b [a,b ...] : write PREFIX_OUT_c<a>.npz = tg_r3m5_c<a> minus faces whose source colour is b within R of centre (and the reverse pair given)
import sys, os, numpy as np
from scipy.spatial import cKDTree
pout=sys.argv[1]; c=np.array(eval(sys.argv[2])); R=float(sys.argv[3]); pairs=[tuple(float(x) for x in p.split(',')) for p in sys.argv[4:]]
S=np.load('/home/claude/stc/rp1/weld.npz')['V'].astype(float); sc=np.load('col_r3.npy'); kS=cKDTree(S)
os.makedirs(os.path.dirname(pout),exist_ok=True)
for fn in os.listdir('.'):
    if fn.startswith('tg_r3m5_c') and fn.endswith('.npz'):
        dst=pout+'_'+fn[len('tg_r3m5_'):]
        if not os.path.exists(dst): os.symlink(os.path.abspath(fn),dst)
for pr in pairs:
    a,b=int(pr[0]),int(pr[1]); nd=np.array(pr[2:5]) if len(pr)>2 else None
    t=np.load('tg_r3m5_c%d.npz'%a); TV=t['V'].astype(float); TF=t['F'].astype(np.int64)
    d,i=kS.query(TV); vc=sc[i]; C=TV[TF].mean(1)
    bad=(np.linalg.norm(C-c,axis=1)<R)&(vc[TF]==b).any(1)
    if nd is not None:
        n=np.cross(TV[TF[:,1]]-TV[TF[:,0]],TV[TF[:,2]]-TV[TF[:,0]]); n/=np.linalg.norm(n,axis=1)[:,None]+1e-12; bad&=(n@nd>0.3)
    Fc=TF[~bad]; used=np.unique(Fc); mp=-np.ones(len(TV),int); mp[used]=np.arange(len(used))
    dst=pout+'_c%d.npz'%a
    if os.path.lexists(dst): os.remove(dst)
    np.savez_compressed(dst,V=TV[used],F=mp[Fc]); print(a,'minus',b,'removed',int(bad.sum()))
