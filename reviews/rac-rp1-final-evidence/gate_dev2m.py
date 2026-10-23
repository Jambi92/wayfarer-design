# gate_dev2.py PROD.npz BASE.npz OUT.json : T-2 hand deviation vs rev107 excluding (a) the Tyler-directed thumb-tip rebuild
# (production vertices that moved vs BASE, with a 3 mm margin) and (b) the recorded R thumb-base crater exclusion
import sys,numpy as np,igl,json; sys.path.insert(0,'/tmp/claude-0/hand/tools'); from hm import *
from scipy.spatial import cKDTree
z=np.load(sys.argv[1]); P=z['V']*np.array([1,-1,1]); Q=z['Q']; T=np.vstack([Q[:,[0,1,2]],Q[:,[0,2,3]]])
b=np.load(sys.argv[2]); P0=b['V']*np.array([1,-1,1])
MV=np.load(sys.argv[4]) if len(sys.argv)>4 else None
mv=np.linalg.norm(P-P0,axis=1)>1e-6 if MV is None else MV
R,F,mat=load107(); V15,_=load15()
d15=cKDTree(V15).query(R)[0]; hand_r=d15>1e-4
prot=z['prot']; o2n=z['old2new']; hand_p=np.ones(len(P),bool); hand_p[o2n[prot]]=False
cr=json.load(open('/tmp/claude-0/hand/c3/crater_exclusion.json'))
zone=np.vstack([P[mv],P0[mv]]); kz=cKDTree(zone)
exr=kz.query(R)[0]<0.3
exr|=np.linalg.norm(R-np.array(cr['centre_cm']),axis=1)<cr['radius_cm']
exq=(kz.query(P[Q].mean(1))[0]<0.3)
out={'excluded_ref_vertices':int(exr.sum()),'moved_prod_vertices':int(mv.sum())}
for side,sg in (('L',1),('R',-1)):
    rv=np.where(hand_r&(np.sign(R[:,0])==sg)&~exr)[0]
    pq=np.where(((hand_p[Q]).any(1))&(np.sign(P[Q].mean(1)[:,0])==sg)&~exq)[0]
    samp=np.vstack([P[np.unique(Q[pq])],P[Q[pq]].mean(1)])
    d1=np.sqrt(igl.point_mesh_squared_distance(samp,R,F)[0])*10
    d2=np.sqrt(igl.point_mesh_squared_distance(R[rv],P,T)[0])*10
    out['hand_'+side]=dict(prod_to_ref=dict(median=float(np.median(d1)),p95=float(np.percentile(d1,95)),max=float(d1.max())),ref_to_prod=dict(median=float(np.median(d2)),p95=float(np.percentile(d2,95)),max=float(d2.max())))
print(json.dumps(out,indent=1)); json.dump(out,open(sys.argv[3],'w'),indent=1)
