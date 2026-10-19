# crestpts.py x [arc] : front-most point of the ear blade in the x-slice (z 199-206, y<-48) and points at +-arc along the section
import numpy as np, sys
from earsl import slice_loops
def crest(x,arc=0.8,zr=(199.0,206.0)):
    best=None
    for P,c in slice_loops(0,x):
        m=(P[:,2]>zr[0])&(P[:,2]<zr[1])&(P[:,1]<-48)
        if not m.any(): continue
        i=np.where(m)[0][np.argmin(P[m,1])]
        if best is None or P[i,1]<best[0][best[1],1]: best=(P,i)
    P,i=best; n=len(P)
    def walk(d):
        s=0;k=i
        while s<arc: k2=(k+d)%n; s+=np.linalg.norm(P[k2]-P[k]); k=k2
        return P[k]
    a,b=walk(1),walk(-1)
    up,lo=(a,b) if a[2]>b[2] else (b,a)
    return P[i],up,lo
if __name__=='__main__':
    for x in map(float,sys.argv[1].split(',')):
        c,u,l=crest(x,float(sys.argv[2]) if len(sys.argv)>2 else 0.8)
        print('x %.2f crest %s up %s lo %s'%(x,c.round(2).tolist(),u.round(2).tolist(),l.round(2).tolist()))
