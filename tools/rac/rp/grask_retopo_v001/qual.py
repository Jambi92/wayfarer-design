import numpy as np, sys, collections
sys.path.insert(0,'/tmp/claude-0/rt'); from common import *
z=np.load(sys.argv[1]); V=z['V']; Q=z['Q']; FP=z['FP']
ang=[]
for i in range(4):
    a=V[Q[:,(i-1)%4]]-V[Q[:,i]]; b=V[Q[:,(i+1)%4]]-V[Q[:,i]]
    ang.append(np.degrees(np.arccos(np.clip((a*b).sum(1)/np.maximum(np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1),1e-12),-1,1))))
ang=np.stack(ang,1); el=np.stack([np.linalg.norm(V[Q[:,(i+1)%4]]-V[Q[:,i]],axis=1) for i in range(4)],1)
asp=(el[:,0]+el[:,2])/np.maximum(el[:,1]+el[:,3],1e-9); asp=np.maximum(asp,1/np.maximum(asp,1e-9))
badA=~((ang>=45)&(ang<=135)).all(1); badR=asp>4
names=np.array([PARTS[p] if not isinstance(p,str) else p for p in FP])
fc=V[Q].mean(1)
for nm,m in (('angle',badA),('aspect',badR)):
    print(nm,m.sum(),collections.Counter(names[m]).most_common(10))
    print(collections.Counter([tuple((np.round(p/4)*4).astype(int)) for p in fc[m]]).most_common(12))
lm=el.max(1)*10; m=(fc[:,2]>186)&(lm>5.45); print('head long edges',m.sum(),collections.Counter([tuple((np.round(p/4)*4).astype(int)) for p in fc[m]]).most_common(8))
