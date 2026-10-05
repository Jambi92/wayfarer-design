# claw-length diagnostic derived from the frozen surface: each claw (FAM 6 component) is stretched along its own axis from its base ring
import numpy as np, igl, json, sys
from scipy.sparse.csgraph import connected_components
from scipy.sparse import coo_matrix
z=np.load('/tmp/claude-0/rodin/c12/g15_surf.npz'); S=z['V'].astype(float); F=z['F'].astype(np.int64)
FAM=np.load('/tmp/claude-0/rodin/c12/g15reg.npz')['FAM']
cl=FAM==6; idx=np.where(cl)[0]; rm=-np.ones(len(S),int); rm[idx]=np.arange(len(idx))
E=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]])
ce=E[cl[E[:,0]]&cl[E[:,1]]]; A=coo_matrix((np.ones(len(ce)),(rm[ce[:,0]],rm[ce[:,1]])),shape=(len(idx),)*2)
n,lab=connected_components(A,directed=False)
bd=np.zeros(len(S),bool); m=cl[E[:,0]]&~cl[E[:,1]]; bd[E[m,0]]=True
claws=[]
for c in range(n):
    vi=idx[lab==c]
    if len(vi)<30: continue
    b=S[vi[bd[vi]]].mean(0) if bd[vi].any() else S[vi].mean(0)
    d=np.linalg.norm(S[vi]-b,axis=1); tip=S[vi[np.argmax(d)]]; a=(tip-b)/np.linalg.norm(tip-b)
    claws.append(dict(v=vi,b=b,a=a,L=float(d.max()),hand=bool(S[vi,2].mean()>40)))
np.save('claw_count.npy',np.array([len(claws)]))
def warp(k_hand,k_foot):
    P=S.copy()
    for c in claws:
        k=k_hand if c['hand'] else k_foot; s=(S[c['v']]-c['b'])@c['a']; P[c['v']]+=((k-1)*np.clip(s,0,None))[:,None]*c['a']
    return P
if __name__=='__main__':
    out={}
    hand=[c for c in claws if c['hand']]; foot=[c for c in claws if not c['hand']]
    out['n_hand']=len(hand); out['n_foot']=len(foot)
    out['hand_claw_len_cm']=[round(c['L'],2) for c in hand]; out['foot_claw_len_cm']=[round(c['L'],2) for c in foot]
    sole=S[(S[:,2]<1.0)&(~cl)]
    for k in (0.8,0.9,1.0,1.15,1.3,1.5):
        P=warp(k,k); fv=np.concatenate([c['v'] for c in foot]); hv=np.concatenate([c['v'] for c in hand])
        r={}
        r['foot_claw_min_u']=round(float(P[fv,2].min()),3)
        r['foot_tip_f_max']=round(float(P[fv,1].max()),2)
        r['foot_length_change_cm']=round(float(P[fv,1].max()-S[fv,1].max()),2)
        r['hand_claw_tip_drop_cm']=round(float(S[hv,2].min()-P[hv,2].min()),2)
        out['k%.2f'%k]=r; print(k,r)
    json.dump(out,open('claws.json','w'),indent=1)
