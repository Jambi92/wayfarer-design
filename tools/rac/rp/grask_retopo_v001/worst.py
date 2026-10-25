import numpy as np, sys, collections
sys.path.insert(0,'/tmp/claude-0/rt'); from common import *
z=np.load(sys.argv[1]); V=z['V']; Q=z['Q']; FP=z['FP']
ang=[]
for i in range(4):
    a=V[Q[:,(i-1)%4]]-V[Q[:,i]]; b=V[Q[:,(i+1)%4]]-V[Q[:,i]]
    ang.append(np.degrees(np.arccos(np.clip((a*b).sum(1)/np.maximum(np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1),1e-12),-1,1))))
ang=np.stack(ang,1); el=np.stack([np.linalg.norm(V[Q[:,(i+1)%4]]-V[Q[:,i]],axis=1) for i in range(4)],1)
asp=(el[:,0]+el[:,2])/np.maximum(el[:,1]+el[:,3],1e-12); asp=np.maximum(asp,1/np.maximum(asp,1e-12))
m=(ang.min(1)<20)|(ang.max(1)>160)|(asp>8); print('hard-limit violators',m.sum())
names=np.array([PARTS[p] for p in FP]); fc=V[Q].mean(1)
print(collections.Counter(names[m]).most_common(20))
print(collections.Counter([tuple((np.round(p/2)*2).astype(int)) for p in fc[m]]).most_common(25))
