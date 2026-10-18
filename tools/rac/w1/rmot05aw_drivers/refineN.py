# Mask-only local protection: flatten weight around flip/SI sites (cloud prep; weights only).
import numpy as np, sys, json, pickle; sys.path.insert(0,'/home/claude/aw')
exec(open('pnN.py').read().split("if __name__")[0])
from scipy.spatial import cKDTree
PR={n:json.loads(sys.argv[1]) for n in NAILS}
tree=cKDTree(V0); log=[]
for n in NAILS:
    for it in range(6):
        s,f,V=test(n,PR[n])
        fl=np.flatnonzero((N0*n_(V)).sum(1)<0)
        if s==0 and len(fl)==0: break
        # SI faces for this nail: approximate via faces with high dihedral? use flips + (if SI) the moved faces nearest to flips
        sites=V0[F[fl]].mean(1) if len(fl) else np.empty((0,3))
        if s and not len(fl):
            k=np.zeros((iv.max()+1,3)); k[iv]=V; ms=pymeshlab.MeshSet(); ms.add_mesh(pymeshlab.Mesh(k,iv[F])); ms.compute_selection_by_self_intersections_per_face(); sf=np.flatnonzero(ms.current_mesh().face_selection_array()); sites=V0[F[sf]].mean(1)
        w=W[n][0].copy()
        for c in sites:
            idx=tree.query_ball_point(c,0.003); idx2=tree.query_ball_point(c,0.005)
            m=w[idx].mean(); w[idx]=m
            ring=np.setdiff1d(idx2,idx); d=np.linalg.norm(V0[ring]-c,axis=1); t=np.clip((d-0.003)/0.002,0,1); w[ring]=m*(1-t)+w[ring]*t
        gm=np.zeros(iv.max()+1); np.maximum.at(gm,iv,w); W[n]=(gm[iv],W[n][1])
        log.append(dict(nail=n,iter=it,SI=s,flips=len(fl),sites=len(sites)))
    s,f,_=test(n,PR[n]); log.append(dict(nail=n,final_SI=s,final_flips=f)); print(n,'final SI',s,'flips',f)
pickle.dump(W,open(sys.argv[2],'wb')); json.dump(log,open('refine_log.json','w'),indent=1)
