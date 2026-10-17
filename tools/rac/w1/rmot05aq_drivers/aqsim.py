# 05AQ proposal model: UI Mesh Filter Inflate (negative) = displacement along vertex normals x c x (1-mask), then
# UI Mesh Filter Smooth N events = N masked Laplacian iterations (05AN calibration). Predicts flags + self-intersections.
import sys; sys.path.insert(0,'/home/claude/an'); sys.path.insert(0,'/home/claude/al'); sys.path.insert(0,'/home/claude/aq')
import numpy as np, scipy.sparse as sp, dryrun as D, predict_an as PA
def vnormals(X,F):
    fn=np.cross(X[F[:,1]]-X[F[:,0]],X[F[:,2]]-X[F[:,0]]); v=np.zeros_like(X)
    for i in range(3): np.add.at(v,F[:,i],fn)
    return v/np.maximum(np.linalg.norm(v,axis=1),1e-30)[:,None]
def proposal(F,M,c,n,Avg):
    def f(X):
        Y=X+vnormals(X,F)*(c*(1-M))[:,None]; return PA.laplace_iter(Y,Avg,M,n) if n else Y
    return f
def si(V,F):
    import pymeshlab
    k,iv=np.unique(np.round(V,7),axis=0,return_inverse=True); ms=pymeshlab.MeshSet(); ms.add_mesh(pymeshlab.Mesh(k,iv.ravel()[F])); ms.compute_selection_by_self_intersections_per_face()
    return np.flatnonzero(ms.current_mesh().face_selection_array())
def flags(V,F,M,c,n,Vstart=None):
    Avg=D.adjacency(F,len(V)); ref,_=PA.reference(F,V if Vstart is None else Vstart); r=PA.predict(V,F,M,proposal(F,M,c,n,Avg),ref=ref); S=r.pop('S')
    vf=sp.csr_matrix((np.ones(F.size),(F.ravel(),np.repeat(np.arange(len(F)),3))),shape=(len(V),len(F))); rv=PA.ringang(V,F,vf); rs=PA.ringang(S,F,vf)
    out=dict(flips=[f for f in r['flips'] if rs[f]>45], near60=[int(f) for f in np.flatnonzero((rs>60)&(rv<=60))], local_new_inversions=r['local_new_inversions'],
             raw_flips=len(r['flips']), raw_near60=len(r['near60']))
    s0=set(si(V,F).tolist()); s1=set(si(S,F).tolist()); out['new_si']=sorted(s1-s0); out['si_before']=len(s0)
    return out,S
if __name__=='__main__':
    V=np.load('/home/claude/ao/ao2/ao2_VF.npz')['V']; F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']; M=np.load(sys.argv[1])
    for c,n in [(-0.008,0),(-0.008,150),(-0.008,120)]:
        r,S=flags(V,F,M,c,n); print(c,n,{k:(len(v) if isinstance(v,list) else v) for k,v in r.items()}, 'maxmove mm',round(float(np.linalg.norm(S-V,axis=1).max()*1000),2),flush=True)
        for k in ('flips','near60','local_new_inversions','new_si'):
            if r[k]: z0=V[:,2].min(); print('  ',k,[[round(float(x)*100,1) for x in (p[0],p[1],p[2]-z0)] for p in S[F[r[k][:6]]].mean(1)])
def collapse(V0,S,F,ratio=0.15,abs_mm=0.3):
    # faces with an edge shrunk below ratio x its start length or below abs_mm (vertex-collapse / degeneracy precursor)
    out=[]
    for i in range(3):
        a,b=F[:,i],F[:,(i+1)%3]; l0=np.linalg.norm(V0[a]-V0[b],axis=1); l1=np.linalg.norm(S[a]-S[b],axis=1)
        out.append(((l1<ratio*l0)|(l1<abs_mm/1000))&(l0>=abs_mm/1000))
    return np.flatnonzero(np.any(out,0)).tolist()
def flags2(V,F,M,c,ns,Vstart=None):
    # deflate (exact UI model) then several Smooth event counts bracketing the UI event-count uncertainty
    Avg=D.adjacency(F,len(V)); Y=V+vnormals(V,F)*(c*(1-M))[:,None]; ref,_=PA.reference(F,V if Vstart is None else Vstart)
    vf=sp.csr_matrix((np.ones(F.size),(F.ravel(),np.repeat(np.arange(len(F)),3))),shape=(len(V),len(F))); rv=PA.ringang(V,F,vf); s0=set(si(V,F).tolist())
    res={}; S=Y; done=0
    for n in sorted(ns):
        S=PA.laplace_iter(S,Avg,M,n-done); done=n
        r=PA.predict(V,F,M,lambda X:S,ref=ref); r.pop('S'); rs=PA.ringang(S,F,vf)
        res[n]=dict(flips=[f for f in r['flips'] if rs[f]>45],near60=[int(f) for f in np.flatnonzero((rs>60)&(rv<=60))],local_new_inversions=r['local_new_inversions'],
                    new_si=sorted(set(si(S,F).tolist())-s0),collapse=collapse(V,S,F))
    return res,S
