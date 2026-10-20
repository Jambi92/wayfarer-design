# cleftfloor.py: trace an inter-digit cleft in horizontal (axis AX) slices: start in the open gap at (x0,y0), step along +DIR,
# re-centring between the walls (rays along the perpendicular), until the gap closes. Returns per-level floor points.
import sys, numpy as np
sys.path.insert(0,'/home/claude/stc/rp1e')
from earsl import slice_loops
from matplotlib.path import Path
def ray(segs,o,d,maxd=3.0):
    best=maxd
    for A,B in segs:
        e=B-A; den=d[0]*(-e[1])+d[1]*e[0]
        if abs(den)<1e-12: continue
        w=A-o; t=(w[0]*(-e[1])+w[1]*e[0])/den; s=(d[0]*w[1]-d[1]*w[0])/den
        if 0<t<best and 0<=s<=1: best=t
    return best
def trace(level,start,direc,axis=2,step=0.04,wmin=0.03,maxsteps=600,ij=(0,1)):
    i,j=ij
    L=[P[:,[i,j]] for P,c in slice_loops(axis,level+1.3e-4) if c]
    L=[l for l in L if np.min(np.linalg.norm(l-np.array(start),axis=1))<6]
    segs=[(l[k],l[(k+1)%len(l)]) for l in L for k in range(len(l))]
    mat=lambda p: sum(Path(l).contains_point(p) for l in L)%2==1
    p=np.array(start,float); d=np.array(direc,float); d/=np.linalg.norm(d); path=[]
    if mat(p): return None
    for k in range(maxsteps):
        n=np.array([-d[1],d[0]]); l=ray(segs,p,n); r=ray(segs,p,-n)
        if l>=3.0 or r>=3.0:   # still outside (open air on a side): just step
            q=p+d*step
        else:
            if l+r<wmin: break
            c=p+n*(l-r)/2; path.append((c.copy(),l+r))
            if len(path)>8:
                nd=path[-1][0]-path[-8][0]; nn=np.linalg.norm(nd)
                if nn>1e-6: d=0.85*d+0.15*nd/nn; d/=np.linalg.norm(d)
            q=c+d*step
        if mat(q): break
        p=q
    if path:
        # refine the floor: fan search from the last centre for the deepest reachable air point along the initial direction
        d0=np.array(direc,float); d0/=np.linalg.norm(d0); best=(path[-1][0]@d0,path[-1][0])
        for c0 in [path[k][0] for k in range(max(0,len(path)-12),len(path),3)]:
          for a in np.radians(np.arange(-80,81,10)):
            R=np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]]); dd=R@d0; q=c0.copy()
            for _ in range(120):
                q2=q+dd*0.02
                if mat(q2): break
                q=q2
            if q@d0>best[0]: best=(q@d0,q)
        path.append((best[1],path[-1][1]))
    return path
if __name__=='__main__':
    x0,y0=map(float,sys.argv[1].split(',')); zs=np.arange(float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]))
    for zz in zs:
        pth=trace(zz,(x0,y0),(0,1))
        if not pth: print('z %.2f none'%zz); continue
        c,w=pth[-1]; print('z %.2f floor (%.2f, %.2f) width_at_floor %.2f  mouth width %.2f n %d'%(zz,c[0],c[1],w,pth[0][1],len(pth)))
