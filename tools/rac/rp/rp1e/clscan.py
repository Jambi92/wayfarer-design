# clscan.py SPEC.json : sweep levels for each oblique cleft, print floor 3D, width, 2D depth
import sys, json, numpy as np
sys.path.insert(0,'/home/claude/stc/rp1e')
from planeslice import plane_loops
from cleftfloor import trace
S=json.load(open(sys.argv[1]))
for ci,c in enumerate(S['clefts']):
    n=np.array(c['nrm'],float); n/=np.linalg.norm(n); e2=np.array(c['e2'],float); e2-=(e2@n)*n; e2/=np.linalg.norm(e2); e1=np.cross(e2,n); o=np.array(c['org'])
    for lv in np.arange(-1.8,2.31,0.3):
        p0=o+n*lv; L=[P for P,cl in plane_loops(p0,n) if cl and np.linalg.norm(P-p0,axis=1).min()<10]; L2=[np.c_[(P-p0)@e1,(P-p0)@e2] for P in L]
        res=None
        for st in c['starts']:
            p=trace(lv,tuple(st),(0,1),loops2d=L2)
            if p and len(p)>=3: res=p; break
        if res: f=res[-1][0]; q=p0+e1*f[0]+e2*f[1]; print(ci,'lv %.1f floor %s 2d %s w %.2f'%(lv,q.round(2),f.round(2),res[-2][1]))
        else: print(ci,'lv %.1f none'%lv)
