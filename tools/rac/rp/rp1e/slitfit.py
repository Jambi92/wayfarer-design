# slitfit.py IN.npz RINGS.json SIDE OUT.npz [cols|all] : per axilla crease column, trace the source slit (slice at J.z) from the lip mouth
# along its centreline to the top (air ends or width < WMIN), then put J = top + OVS along the slit axis (into the material),
# WA/WT on the arm/trunk walls at depth fraction WF of the traced slit.  env: OVS (0.3), WF (0.6), WMIN (0.03), STEP (0.02)
import numpy as np, sys, json, os
from matplotlib.path import Path
sys.path.insert(0,'/home/claude/stc/rp1e')
from earsl import slice_loops
inp,rp,side,out=sys.argv[1:5]; sel=sys.argv[5] if len(sys.argv)>5 else 'all'
z=np.load(inp); V=z['V'].astype(float).copy(); R=json.load(open(rp))[side]
OVS=float(os.environ.get('OVS','0.3')); WF=float(os.environ.get('WF','0.6')); WMIN=float(os.environ.get('WMIN','0.03')); ST=float(os.environ.get('STEP','0.02'))
cols=range(len(R['J'])) if sel=='all' else [int(c) for c in sel.split(',')]
def material(loops,p):
    return sum(Path(L).contains_point(p) for L in loops)%2==1
def ray(segs,o,d,maxd=2.0):
    # first boundary hit from o along d (2D)
    best=maxd
    for A,B in segs:
        e=B-A; den=d[0]*(-e[1])+d[1]*e[0]
        if abs(den)<1e-12: continue
        w=A-o; t=(w[0]*(-e[1])+w[1]*e[0])/den; s=(d[0]*w[1]-d[1]*w[0])/den
        if 0<t<best and 0<=s<=1: best=t
    return best
res={}
for i in cols:
    j=R["J"][i]; zz=V[j,2]+1.37e-4
    loops=[L[:,:2] for L,c in slice_loops(2,zz) if c and np.min(np.linalg.norm(L[:,:2]-V[j,:2],axis=1))<3]
    if not loops: res[i]='noloop'; continue
    segs=[(L[k],L[(k+1)%len(L)]) for L in loops for k in range(len(L))]
    segs=[s for s in segs if min(np.linalg.norm(s[0]-V[j,:2]),np.linalg.norm(s[1]-V[j,:2]))<3]
    A=V[R['JA'][i],:2]; T=V[R['JT'][i],:2]; L0=0.5*(A+T)
    ax_=V[j,:2]-L0; ax_/=np.linalg.norm(ax_)
    p=L0.copy(); path=[]
    # start: move to the mouth (first air point along axis from lip midpoint)
    k=0
    while material(loops,p) and k<200: p=p+ax_*ST; k+=1
    while k<400:
        if material(loops,p): break
        nrm=np.array([-ax_[1],ax_[0]]); l=ray(segs,p,nrm); r=ray(segs,p,-nrm)
        w=l+r
        if os.environ.get("DBG"): print("  ",np.round(p,3),round(l,3),round(r,3))
        if w<WMIN or w>1.5: break
        c=p+nrm*(l-r)/2; path.append((c.copy(),w,c+nrm*l,c-nrm*r))
        q=c+ax_*ST
        if len(path)>8:
            nd=path[-1][0]-path[-8][0]; nd/=np.linalg.norm(nd)+1e-12; ax_=0.85*ax_+0.15*nd; ax_/=np.linalg.norm(ax_)
        p=q; k+=1
    if len(path)<3: res[i]='closed'; continue
    top=path[-1][0]; tip=top+ax_*OVS
    w=path[min(int(WF*len(path)),len(path)-1)]
    # which wall is arm (nearer JA)
    w1,w2=w[2],w[3]
    wa,wt=(w1,w2) if np.linalg.norm(w1-A)+np.linalg.norm(w2-T)<np.linalg.norm(w2-A)+np.linalg.norm(w1-T) else (w2,w1)
    V[j,:2]=tip; V[R['WA0.5'][i],:2]=wa; V[R['WT0.5'][i],:2]=wt
    V[R['WA0.5'][i],2]=zz; V[R['WT0.5'][i],2]=zz
    res[i]='depth %.2f top %s width0 %.2f'%(np.linalg.norm(path[-1][0]-path[0][0]),np.round(top,2),path[0][1])
np.savez_compressed(out,V=V,F=z['F'])
for i in cols: print(i,R['J'][i],res[i])
