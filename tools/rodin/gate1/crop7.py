import sys, numpy as np
sys.path.insert(0,'/tmp/claude-0/rodin/g1')
import g7geo as G, hand
z=np.load('cur_s7.npz'); P=z['P'].astype(np.float64); f=z['f']; R=z['R']
def save(name,Q,m):
    fm=m[f].all(1); ff=f[fm]; idx=np.unique(ff); remap=-np.ones(len(P),np.int64); remap[idx]=np.arange(len(idx))
    np.savez(name,P=Q[idx].astype(np.float32),f=remap[ff].astype(np.int32),R=R[idx]); print(name,len(idx),len(ff))
o=np.load('foot7.npz')['P']; lo,hi=o.min(0)-0.01,o.max(0)+0.01
save('foot7.npz',P,((P>=lo)&(P<=hi)).all(1))
h=np.load('hand7.npz')['P']; lo,hi=h.min(0)-0.01,h.max(0)+0.01
for sg in (1,-1):
    S=G.ARM[sg]; a,b,c=hand.frame(S['W'],S['E'],sg); W=np.asarray(S['W'])
    M=np.stack([a,b,c],1); Q=(P-W)@np.linalg.inv(M).T
    m=((Q>=lo)&(Q<=hi)).all(1); print(sg,m.sum())
    if abs(m.sum()-len(h))<0.1*len(h): save('hand7.npz',Q,m); break
