# 05AS dihedral gate. Shared-edge dihedrals vs GO-05AO_AC2. Transition field = edges whose faces touch a vertex with 0.05 < M < 1
# (the feather band incl. its outer boundary). Reports max new increase, max absolute dihedral among edges that were < 35 deg in AO2,
# and coherent chains: connected sets of edges (through shared faces) with increase > 10 deg; a chain is flagged when it spans > 40 mm.
import sys; sys.path[:0]=['/home/claude/al','/home/claude/aq']; import numpy as np, scipy.sparse as sp
from predict2 import face_adj, nrm
from scipy.sparse.csgraph import connected_components
class Gate:
    def __init__(s,V0,F,M):
        s.F=F; s.fa,s.fb=face_adj(F); s.V0=V0; n0=nrm(V0,F); s.a0=np.degrees(np.arccos(np.clip((n0[s.fa]*n0[s.fb]).sum(1),-1,1)))
        band=(M>0.05)&(M<1); fb=band[F].any(1); s.trans=fb[s.fa]|fb[s.fb]; s.field=((M<1)[F].any(1))[s.fa]|((M<1)[F].any(1))[s.fb]
        s.c=(V0[F[s.fa]].mean(1)+V0[F[s.fb]].mean(1))/2
    def eval(s,X,mask_edges=None):
        n1=nrm(X,s.F); a1=np.degrees(np.arccos(np.clip((n1[s.fa]*n1[s.fb]).sum(1),-1,1))); d=a1-s.a0
        T=s.trans; out=dict(max_inc_transition=round(float(d[T].max()),2),max_inc_field=round(float(d[s.field].max()),2),
            n_inc20_transition=int((d[T]>20).sum()),max_abs_new35_transition=round(float(a1[T&(s.a0<35)].max()),2),n_abs_over35_new=int((T&(s.a0<35)&(a1>35)).sum()))
        e=np.flatnonzero(T&(d>10)); chains=[]
        if len(e):
            nf=len(s.F); A=sp.coo_matrix((np.ones(len(e)),(s.fa[e],s.fb[e])),shape=(nf,nf)); k,lab=connected_components(A,directed=False)
            fl=np.unique(np.r_[s.fa[e],s.fb[e]]); 
            for comp in np.unique(lab[fl]):
                fs=fl[lab[fl]==comp]; p=s.V0[s.F[fs]].reshape(-1,3); span=float(np.linalg.norm(p.max(0)-p.min(0))*1000)
                if span>40: chains.append(dict(span_mm=round(span,1),faces=int(len(fs)),centre_cm=[round(float(x)*100,1) for x in p.mean(0)]))
        out['chains_over_40mm']=chains; return out,d
