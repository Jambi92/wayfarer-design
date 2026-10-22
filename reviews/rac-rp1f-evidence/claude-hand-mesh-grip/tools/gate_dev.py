# gate_dev.py PROD.npz OUT.json : T-2 hand surface deviation, production <-> accepted rev107 sculpt (both directions), per hand
import sys,numpy as np,igl,json; sys.path.insert(0,'/tmp/claude-0/hand/tools'); from hm import *
from scipy.spatial import cKDTree
z=np.load(sys.argv[1]); P=z['V']*np.array([1,-1,1]); Q=z['Q']; T=np.vstack([Q[:,[0,1,2]],Q[:,[0,2,3]]])
R,F,mat=load107(); V15,_=load15()
d15=cKDTree(V15).query(R)[0]; hand_r=d15>1e-4            # rev107 vertices that differ from v015 = the edited hand region
prot=z['prot']; o2n=z['old2new']; hand_p=np.ones(len(P),bool); hand_p[o2n[prot]]=False
out={}
for side,sg in (('L',1),('R',-1)):
    rv=np.where(hand_r&(np.sign(R[:,0])==sg))[0]; rf=F[(hand_r[F].any(1))&(np.sign(R[F].mean(1)[:,0])==sg)]
    pq=np.where(((hand_p[Q]).any(1))&(np.sign(P[Q].mean(1)[:,0])==sg))[0]
    samp=np.vstack([P[np.unique(Q[pq])],P[Q[pq]].mean(1),0.5*(P[Q[pq,0]]+P[Q[pq,1]]),0.5*(P[Q[pq,1]]+P[Q[pq,2]])])
    d1=np.sqrt(igl.point_mesh_squared_distance(samp,R,F)[0])*10
    tq=np.vstack([Q[pq][:,[0,1,2]],Q[pq][:,[0,2,3]]])
    d2=np.sqrt(igl.point_mesh_squared_distance(R[rv],P,T)[0])*10
    out['hand_'+side]=dict(prod_to_ref=dict(median=float(np.median(d1)),p95=float(np.percentile(d1,95)),max=float(d1.max()),n=int(len(d1))),
                         ref_to_prod=dict(median=float(np.median(d2)),p95=float(np.percentile(d2,95)),max=float(d2.max()),n=int(len(d2))))
    if d2.max()>1.5:
        w=rv[d2>1.5]; out['hand_'+side]['ref_to_prod_over_1.5mm_points']=R[w][:20].round(3).tolist(); out['hand_'+side]['ref_to_prod_over_1.5mm_count']=int(len(w))
    if d1.max()>1.5: out['hand_'+side]['prod_to_ref_over_1.5mm_count']=int((d1>1.5).sum())
print(json.dumps(out,indent=1)); json.dump(out,open(sys.argv[2],'w'),indent=1)
