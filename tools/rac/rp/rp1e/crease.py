import numpy as np, sys
from earsl import slice_loops
from scipy.spatial import cKDTree
def front_curve(z, xr=(-14,16), ymax=-44):
    best=None
    for P,c in slice_loops(2,z):
        m=(P[:,0]>xr[0])&(P[:,0]<xr[1])&(P[:,1]<ymax)
        if m.sum()>(best[0] if best else 0): best=(m.sum(),P,m)
    return best[1],best[2]
def spikes(z, W=1.0, prom=0.8):
    P,m=front_curve(z); n=len(P); out=[]
    idx=np.where(m)[0]
    # local maxima of y along the closed curve (backward = +y), restricted to front window
    y=P[:,1]
    for i in idx:
        win=[(i+k)%n for k in range(-40,41)]
        if y[i]<y[win].max(): continue
        # walk both directions until walls are W apart: left branch / right branch
        a=[(i-k)%n for k in range(1,400)]; b=[(i+k)%n for k in range(1,400)]
        A=P[a][:,:2]; Bc=P[b][:,:2]; T=cKDTree(Bc)
        d,j=T.query(A)
        ka=np.argmax(d>W) if (d>W).any() else None
        if ka is None or ka<2: continue
        mouthA=P[a[ka]]; mouthB=P[b[j[ka]]]
        depth=P[i,1]-0.5*(mouthA[1]+mouthB[1])
        if depth<prom: continue
        out.append(dict(tip=P[i],mA=mouthA,mB=mouthB,depth=float(depth),width=float(np.median(d[:ka]))))
    return out
if __name__=='__main__':
    for z in np.arange(float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3])):
        S=spikes(z)
        print('z %.1f'%z,' | '.join('tip %s mA %s mB %s d %.1f w %.2f'%(s['tip'][:2].round(1),s['mA'][:2].round(1),s['mB'][:2].round(1),s['depth'],s['width']) for s in S))
