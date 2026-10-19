import numpy as np, sys
from earsl import slice_loops
from scipy.spatial import cKDTree
def curve(z, xr, yr):
    best=None
    for P,c in slice_loops(2,z):
        m=(P[:,0]>xr[0])&(P[:,0]<xr[1])&(P[:,1]>yr[0])&(P[:,1]<yr[1])
        if m.sum()>(best[0] if best else 0): best=(m.sum(),P,m)
    return best
def spike(z, xr, yr, sgn, W=1.0):
    """sgn=+1: spike toward +y (front crease, tip = max y); -1: back crease (tip = min y)"""
    b=curve(z,xr,yr)
    if b is None: return None
    _,P,m=b; n=len(P); idx=np.where(m)[0]; y=sgn*P[:,1]
    i=idx[np.argmax(y[idx])]
    a=[(i-k)%n for k in range(1,600)]; bb=[(i+k)%n for k in range(1,600)]
    A=P[a][:,:2]; B=P[bb][:,:2]; T=cKDTree(B); d,j=T.query(A)
    ka=int(np.argmax(d>W)) if (d>W).any() else len(a)-1
    return dict(tip=P[i],lA=P[a[ka]],lB=P[bb[j[ka]]],depth=float(sgn*(P[i,1]-0.5*(P[a[ka],1]+P[bb[j[ka]],1]))),P=P)
if __name__=='__main__':
    side=sys.argv[1]
    xr=(-26,-12) if side=='R' else (16,30)
    for z in np.arange(float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4])):
        f=spike(z,xr,(-48,-33),+1); b=spike(z,xr,(-34,-18),-1)
        fs='front tip %s lA %s lB %s d %.1f'%(f['tip'][:2].round(1),f['lA'][:2].round(1),f['lB'][:2].round(1),f['depth']) if f else 'front -'
        bs='back tip %s lA %s lB %s d %.1f'%(b['tip'][:2].round(1),b['lA'][:2].round(1),b['lB'][:2].round(1),b['depth']) if b else 'back -'
        print('z %.1f | %s | %s'%(z,fs,bs))
