"""Per-region mirror-symmetry readings for the Saurin frozen reference (x -> -x nearest vertex distance)."""
import numpy as np, json, sys
from scipy.spatial import cKDTree
d=np.load(sys.argv[1]); V=d['v'] if 'v' in d else d['V']
M=V.copy(); M[:,0]*=-1
dist,_=cKDTree(V).query(M,workers=-1)
x,f,u=V[:,0],V[:,1],V[:,2]
reg={'head':u>170,'tail':(f<-15)&(u<110)&(u>60)&(np.abs(x)<15),'torso':(u>105)&(u<=170)&(np.abs(x)<20),
     'arms':(u>80)&(np.abs(x)>=20),'legs':(u<=95)&~((f<-15)&(np.abs(x)<15))}
out={}
for k,m in reg.items():
    dd=dist[m]; out[k]={'n':int(m.sum()),'median_cm':float(np.median(dd)),'p99_cm':float(np.percentile(dd,99)),'max_cm':float(dd.max())}
L=(x<0)&(u<95); i=np.argmax(np.where(L,dist,-1)); out['worst_vertex']={'x':float(x[i]),'f':float(f[i]),'u':float(u[i]),'dist_cm':float(dist[i])}
json.dump(out,open(sys.argv[2],'w'),indent=1); print(json.dumps(out,indent=1))
