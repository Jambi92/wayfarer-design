import numpy as np,sys
z=np.load(sys.argv[1]);V=z['V'];Q=z['Q'];c=np.array([float(t) for t in sys.argv[2].split(',')])
fc=V[Q].mean(1);
ang=[]
for i in range(4):
    a=V[Q[:,(i-1)%4]]-V[Q[:,i]]; b=V[Q[:,(i+1)%4]]-V[Q[:,i]]
    ang.append(np.degrees(np.arccos(np.clip((a*b).sum(1)/np.maximum(np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1),1e-12),-1,1))))
ang=np.stack(ang,1)
m=np.where((np.linalg.norm(fc-c,axis=1)<1.0)&((ang.min(1)<20)|(ang.max(1)>160)))[0]
from collections import Counter
val=Counter(Q.ravel())
for f in m:
    q=Q[f]; print(f,'ang',np.round(ang[f]).astype(int),'val',[val[v] for v in q])
    for v in q: print('   ',v,np.round(V[v],2))
    # planarity
    n=np.cross(V[q[2]]-V[q[0]],V[q[3]]-V[q[1]]); n/=np.linalg.norm(n)
    print('   offplane',np.round((V[q]-V[q].mean(0))@n,3), 'edges',np.round(np.linalg.norm(V[q]-V[np.roll(q,-1)],axis=1),2))
