import numpy as np, json, sys
from earsl import slice_loops
cg,ring,out=sys.argv[1:4]; FR=float(sys.argv[4]); keys=sys.argv[5].split(';')
z=np.load(cg);V=z['V'];R=json.load(open(ring))['rungs']; J={}
for a,b in R[:-1]:
    k='%d,%d'%(a,b)
    if k not in keys: continue
    pa,pb=V[a],V[b]; x=(pa[0]+pb[0])/2; best=None
    for P,c in slice_loops(0,x):
        m=(P[:,2]>171)&(P[:,2]<182)&(P[:,1]>pa[1]-1)&(P[:,1]<-41)
        if m.any():
            Q=P[m]; i=np.argmax(Q[:,1])
            if best is None or Q[i,1]>best[1]: best=Q[i]
    mid=(pa+pb)/2; J[k]=(mid+FR*(best-mid)).tolist(); print(k,best.round(1))
json.dump(J,open(out,'w'))
