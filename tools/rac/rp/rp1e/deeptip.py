# deeptip.py SIDE z0 z1 dz : front-crease deepest air point per z, including enclosed void loops near the main tip
import numpy as np, sys
from earsl import slice_loops
from axcrease import spike
side=sys.argv[1]; xr=(-26,-12) if side=='R' else (16,30)
for z in np.arange(float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4])):
    f=spike(z,xr,(-48,-33),+1)
    if not f: print('z %.1f -'%z); continue
    t=f['tip']; best=t; nv=0
    for P,c in slice_loops(2,z):
        m=(np.linalg.norm(P[:,:2]-t[:2],axis=1)<2.0)
        if m.any() and len(P)<len(f['P']):
            nv+=1; i=np.argmax(P[:,1]*m - 1e9*(~m))
            if P[i,1]>best[1]: best=P[i]
    print('z %.1f spike %s deep %s voids %d depth %.1f'%(z,t[:2].round(2),best[:2].round(2),nv,f['depth']))
