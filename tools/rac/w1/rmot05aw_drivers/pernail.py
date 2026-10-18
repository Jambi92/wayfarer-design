import numpy as np, sys, json, pickle, glob, pymeshlab; sys.path.insert(0,'/home/claude/aw'); from nails2 import *
D=np.load('src_VF.npz'); V0=D['V']; F=D['F']; W=pickle.load(open(sorted(glob.glob('W3_*.pkl'))[-1],'rb'))
k0,iv=np.unique(np.round(V0,7),axis=0,return_inverse=True); iv=iv.ravel()
n_=lambda X: np.cross(X[F[:,1]]-X[F[:,0]],X[F[:,2]]-X[F[:,0]]); N0=n_(V0)
def si(V):
    k=np.zeros((iv.max()+1,3)); k[iv]=V; ms=pymeshlab.MeshSet(); ms.add_mesh(pymeshlab.Mesh(k,iv[F])); ms.compute_selection_by_self_intersections_per_face(); return int(ms.current_mesh().face_selection_array().sum())
def test(n,pr):
    w,fr=W[n]; sx,curl,te,tn=pr; loc0=np.round(fr['Pp'],5); M0=empty_mat(loc0,[0,0,YAW[n[0]]],[1,1,1])
    M1=empty_mat(np.round(loc0+fr['e']*te+fr['n']*tn,5),[curl,0,YAW[n[0]]],[sx,1,1]); V=apply_hook(V0,w,M0,M1)
    return si(V), int(((N0*n_(V)).sum(1)<0).sum()), V
if __name__=='__main__':
    pr=json.loads(sys.argv[1])
    for n in NAILS: s,f,_=test(n,pr); print(n,'SI',s,'flips',f)
