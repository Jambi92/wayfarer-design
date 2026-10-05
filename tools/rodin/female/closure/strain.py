# scale-surface verification: edge stretch of the scaled surface caused by the E+B tissue displacement alone (before global warps)
import numpy as np, pickle, sys, json; sys.path.insert(0,'/tmp/claude-0/rodin/v1'); sys.path.insert(0,'/tmp/claude-0/rodin/v5')
import vary, tissue, fsets3
L=pickle.load(open('/tmp/claude-0/rodin/v1/Lsurf.pkl','rb')); z=np.load(vary.REF_SURF); S=z['V'].astype(float); Fs=z['F'].astype(np.int64)
out={}
for nm,p in (('final_ref E2.0+B1.6',fsets3.REF),('C-level B3.0 + E2.0',dict(fsets3.REF,vfull=3.0)),('composition fat +1 (existing control, for scale)',{'fat':1.0})):
    if 'fat' in p: o=(L.fat*2.2)[:,None]*L.N
    else: o=tissue.offset(S,L,p)
    mv=np.linalg.norm(o,axis=1)>1e-4; fm=mv[Fs].any(1); F2=Fs[fm]
    S2=S+o; r=[]
    for a,b in ((0,1),(1,2),(2,0)):
        l0=np.linalg.norm(S[F2[:,a]]-S[F2[:,b]],axis=1); l1=np.linalg.norm(S2[F2[:,a]]-S2[F2[:,b]],axis=1); r.append(l1/np.maximum(l0,1e-9))
    r=np.concatenate(r); A0=np.linalg.norm(np.cross(S[F2[:,1]]-S[F2[:,0]],S[F2[:,2]]-S[F2[:,0]]),axis=1); A1=np.linalg.norm(np.cross(S2[F2[:,1]]-S2[F2[:,0]],S2[F2[:,2]]-S2[F2[:,0]]),axis=1)
    ar=A1/np.maximum(A0,1e-12)
    # flipped faces: normal reversal
    n0=np.cross(S[F2[:,1]]-S[F2[:,0]],S[F2[:,2]]-S[F2[:,0]]); n1=np.cross(S2[F2[:,1]]-S2[F2[:,0]],S2[F2[:,2]]-S2[F2[:,0]])
    flip=int(((n0*n1).sum(1)<0).sum())
    out[nm]=dict(faces=int(len(F2)),max_disp_cm=float(np.linalg.norm(o,axis=1).max()),edge_p01=float(np.percentile(r,1)),edge_p99=float(np.percentile(r,99)),edge_max=float(r.max()),area_p99=float(np.percentile(ar,99)),area_max=float(ar.max()),flipped=flip)
    print(nm,out[nm],flush=True)
json.dump(out,open('/tmp/claude-0/rodin/v5/strain.json','w'),indent=1)
