# variable-radius Poisson-disk seeding (dart throwing in batches): seed spacing follows the graded size field with no seams
import numpy as np
from scipy.spatial import cKDTree
def poisson_seeds(V,R,mask,rng,c=0.80,ncand=None,batch=25000):
    idx=np.where(mask)[0]; ncand=ncand or min(len(idx),2_500_000)
    cand=rng.choice(idx,ncand,replace=False); acc=np.zeros(0,np.int64); Rmax=float(R[idx].max())
    for b0 in range(0,ncand,batch):
        cb=cand[b0:b0+batch]; rc=c*R[cb]
        if len(acc):
            tr=cKDTree(V[acc]); d,j=tr.query(V[cb],k=1,distance_upper_bound=c*Rmax)
            ok=np.ones(len(cb),bool); hit=np.isfinite(d); ok[hit]=d[hit]>=np.minimum(rc[hit],c*R[acc[j[hit]]])
            cb=cb[ok]; rc=rc[ok]
        if len(cb)==0: continue
        tb=cKDTree(V[cb]); pairs=tb.query_pairs(c*Rmax,output_type='ndarray'); keep=np.ones(len(cb),bool)
        if len(pairs):
            dd=np.linalg.norm(V[cb[pairs[:,0]]]-V[cb[pairs[:,1]]],axis=1); cf=pairs[dd<np.minimum(rc[pairs[:,0]],rc[pairs[:,1]])]
            for a,bq in cf:
                if keep[a] and keep[bq]: keep[max(a,bq)]=False
        acc=np.concatenate([acc,cb[keep]])
    return acc
if __name__=='__main__':
    import time; z=np.load('g7up.npz'); V=z['V'].astype(np.float64); r=np.load('g7reg.npz'); R=r['R'].astype(np.float64); FAM=r['FAM']
    t=time.time(); S=poisson_seeds(V,R,(FAM!=6)&(FAM!=7),np.random.default_rng(7)); print(len(S),time.time()-t)
