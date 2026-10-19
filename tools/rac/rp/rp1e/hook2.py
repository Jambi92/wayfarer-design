import numpy as np
from scipy.spatial import cKDTree
from earsl import slice_loops
def curve(y, win=(-10,12,93,110)):
    best=None
    for P,c in slice_loops(1,y):
        m=(P[:,0]>win[0])&(P[:,0]<win[1])&(P[:,2]>win[2])&(P[:,2]<win[3])
        if best is None or m.sum()>best[0]: best=(m.sum(),P)
    return best[1]
def roofC(P,cx=1.3):
    cm=(abs(P[:,0]-cx)<1.2)&(P[:,2]<103.5)&(P[:,2]>96); i=np.where(cm)[0][np.argmax(P[cm][:,2])]; return i
def hook(y,side,W=1.0,rmax=9):
    P=curve(y); n=len(P); ic=roofC(P); C=P[ic]; sg=-1 if side=='R' else 1
    reg=(sg*(P[:,0]-C[0])>0.4)&(P[:,2]>C[2]-0.6)&(np.linalg.norm(P[:,[0,2]]-C[[0,2]],axis=1)<rmax)
    # the tip = farthest point in the region that is connected to C along the curve through region points
    # walk from C toward the side
    for d in (1,-1):
        j=(ic+d*3)%n
        if sg*(P[j,0]-C[0])>0: dirn=d; break
    k=ic; path=[]
    for s in range(n):
        k=(k+dirn)%n
        if not reg[k] and sg*(P[k,0]-C[0])>0.4: break
        path.append(k)
    top=np.array(path)                      # C -> ... -> tip region boundary
    dd=np.linalg.norm(P[top][:,[0,2]]-C[[0,2]],axis=1); it=top[int(np.argmax(dd))]
    # lower branch from tip continuing in the same direction
    low=[]; k=it
    for s in range(n):
        k=(k+dirn)%n; low.append(k)
        if P[k,2]<C[2]-3: break
    low=np.array(low); topb=np.array([q for q in top if q!=it]); 
    T=cKDTree(P[topb][:,[0,2]]); dist,ii=T.query(P[low][:,[0,2]])
    km=int(np.argmax(dist>W)) if (dist>W).any() else len(low)-1
    m=P[low[km]]; i_=P[topb[ii[km]]]
    return dict(C=C,t=P[it],m=m,i=i_,width=float(np.median(dist[:max(km,1)])),depth=float(np.linalg.norm(P[it,[0,2]]-m[[0,2]])))
if __name__=='__main__':
    import sys
    for y in [float(t) for t in sys.argv[1].split(',')]:
        for s in 'RL':
            try:
                h=hook(y,s); print(y,s,'C',h['C'][[0,2]].round(2),'t',h['t'][[0,2]].round(2),'m',h['m'][[0,2]].round(2),'i',h['i'][[0,2]].round(2),'w %.2f d %.2f'%(h['width'],h['depth']))
            except Exception as e: print(y,s,'ERR',e)
