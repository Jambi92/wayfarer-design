# Stage A (per-nail-class params): masked Laplacian smooth + inflate over geodesic ellipse regions
import numpy as np, sys, json, pickle, os; sys.path.insert(0,'/home/claude/aw1'); import aw1lib as L
def W_of(n,c):
    big=n[1]=='1'; g=lambda k,d: c.get(k+('_big' if big else ''),c.get(k,d))
    key=f"{os.environ.get('AW1_PFX','')}e_{g('margin',0.012)}_{g('ramp',0.006)}_{g('scap',1.35)}_{n}.npy"
    if os.path.exists(key): w=np.load(key)
    else: w=L.ellipse_weight(n,margin=g('margin',0.012),ramp=g('ramp',0.006),scap=g('scap',1.35))[0]; np.save(key,w)
    return w*g('wmul',1.0)
if __name__=='__main__':
    cfg=json.loads(sys.argv[1]); tag=sys.argv[2]; sup=np.load(cfg.get('support','support_c.npy'))
    w=np.zeros(len(L.V0))
    for n in L.FR: w=np.maximum(w,W_of(n,cfg))
    w[~sup]=0; M=1-w; M[L.dup_left]=1; X=L.V0.copy()
    for st in cfg['steps']:
        if st[0]=='S': X=L.smooth(X,M,int(st[1]))
        elif st[0]=='I': X=L.inflate(X,M,float(st[1]))
        elif st[0]=='R': X=L.relax(X,M,int(st[1]))
        elif st[0]=='H': X=L.hc_smooth(X,M,int(st[1]),st[2],st[3])
    np.save(f'M_{tag}.npy',M); np.savez(f'{tag}_VF.npz',V=X,F=L.F)
    d=np.linalg.norm(X-L.V0,axis=1)*1000; print(tag,'moved',int((d>1e-3).sum()),'max %.2f'%d.max())
