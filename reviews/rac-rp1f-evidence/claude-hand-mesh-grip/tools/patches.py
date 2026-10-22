import sys; sys.path.insert(0,'/tmp/claude-0/hand/tools'); from hm import *
def comp_faces(faces, seedv, nv):
    # connected component of face set (via shared vertices) containing seed vertex
    k=faces.shape[1]; E=np.vstack([faces[:,[i,(i+1)%k]] for i in range(k)])
    A=sp.coo_matrix((np.ones(len(E)),(E[:,0],E[:,1])),shape=(nv,nv))
    _,lab=connected_components(A,directed=False); keep=lab[faces[:,0]]==lab[seedv]; return faces[keep]
def boundary_loops(faces):
    k=faces.shape[1]; E=np.vstack([faces[:,[i,(i+1)%k]] for i in range(k)])
    key=np.sort(E,1); u,inv,c=np.unique(key,axis=0,return_inverse=True,return_counts=True)
    b=E[c[inv]==1]; nxt={a:bb for a,bb in b}; loops=[]; seen=set()
    if len(nxt)!=len(b): raise ValueError('non-manifold boundary vertex (%d dup)'%(len(b)-len(nxt)))
    for s in nxt:
        if s in seen: continue
        L=[s]; seen.add(s); x=nxt[s]
        while x!=s:
            L.append(x); seen.add(x); x=nxt[x]
            if len(L)>len(b): raise ValueError('open boundary chain')
        loops.append(L)
    return loops, (c>2).sum()
if __name__=='__main__':
    V,Q=load15(); R,F,mat=load107(); D=json.load(open('/tmp/claude-0/hand/digits.json'))
    for k,d in D.items():
        ax=np.array(d['axis']); c1=np.array(d['c1']); p0=c1+(d['claw_s'][0]-1.0)*ax
        T=np.array(d['T']); sv=np.argmin(np.linalg.norm(V-T,axis=1)); sr=np.argmin(np.linalg.norm(R-np.array(d['claw_tip']),axis=1))
        inv=(V-p0)@ax>0; fq=comp_faces(Q[inv[Q].all(1)],sv,len(V))
        inr=(R-p0)@ax>0; ft=comp_faces(F[inr[F].all(1)],sr,len(R))
        lq,nmq=boundary_loops(fq); lt,nmt=boundary_loops(ft)
        print(k,'v015 faces',len(fq),'chi',euler_sub(fq),'loops',[len(l) for l in lq],'| r107 tris',len(ft),'chi',euler_sub(ft),'loops',[len(l) for l in lt])
