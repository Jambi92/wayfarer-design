import numpy as np,sys;sys.path.insert(0,'/home/claude/aw1');import aw1lib as L
def folds(X,thr=60):
    F=L.F;fn=np.cross(X[F[:,1]]-X[F[:,0]],X[F[:,2]]-X[F[:,0]]);A=np.linalg.norm(fn,axis=1);fn=fn/np.maximum(A,1e-30)[:,None]
    vn=L.vnormals(X);dev=np.degrees(np.arccos(np.clip((fn*vn[F]).sum(2).min(1) if False else np.einsum('ij,ikj->ik',fn,vn[F]).min(1),-1,1)))
    return dev>thr, A
if __name__=='__main__':
    for t in sys.argv[1:]:
        X=np.load(t)['V'];f,A=folds(X);f0,_=folds(L.V0)
        mv=np.linalg.norm(X-L.V0,axis=1)>1e-6;fm=mv[L.F].any(1)
        print(t,'folded faces in moved region',(f&fm).sum(),'were folded in src',(f0&fm).sum())
