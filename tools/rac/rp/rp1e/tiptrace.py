import numpy as np, sys
sys.path.insert(0,'/home/claude/stc/rp1e')
from earsl import slice_loops
from scipy.spatial import cKDTree
# z-slices: in each z plane, B loop and C(+bar) loop; slit tip x = where the two loops' gap closes
res=[]
for zz in np.arange(91.8,94.6,0.1):
    L=[P for P,c in slice_loops(2,zz) if c]
    L=[P for P in L if np.linalg.norm(P.mean(0)[:2]-np.array([-33,-40.8]))<4]
    if len(L)==1:
        P=L[0]
        # merged: find the notch (slit tip) as the point of the loop nearest the slit line y=-40.85 with smallest x among points where the loop turns
        m=np.abs(P[:,1]+40.85)<0.15; 
        if m.any(): q=P[m][np.argmin(P[m][:,0])]; res.append((zz,'merged-notch',q.round(3).tolist()))
    elif len(L)>=2:
        A,B=sorted(L,key=lambda P:P[:,1].mean())[:2]
        d,i=cKDTree(B).query(A); k=np.argmin(d); res.append((zz,'gap %.2fmm'%(d[k]*10),((A[k]+B[i[k]])/2).round(3).tolist()))
for r in res: print(r)
