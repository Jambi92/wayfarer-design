import numpy as np, igl
def hidden_quads(V,Q,off=0.01):
    T=np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]]
    vol=np.einsum('ij,ij->i',V[T[:,0]],np.cross(V[T[:,1]],V[T[:,2]])).sum(); s=1.0 if vol>0 else -1.0
    n=np.cross(V[T[:,1]]-V[T[:,0]],V[T[:,2]]-V[T[:,0]]); n/=np.linalg.norm(n,axis=1)[:,None]+1e-30
    P=V[T].mean(1)+s*n*off; w=np.abs(igl.winding_number(V,T,P)); ht=w>0.5; nq=len(Q)
    return ht[:nq]&ht[nq:], s, ht
if __name__=='__main__':
    z=np.load('sstar.npz'); V=z['V']; Q=z['Q']; h,s,ht=hidden_quads(V,Q); C=V[Q].mean(1)
    print('hidden quads',h.sum(),'any-tri hidden',(ht[:len(Q)]|ht[len(Q):]).sum())
    for nm,m in (('crotch',np.abs(C[:,0])<6),('L',C[:,0]>=6),('R',C[:,0]<=-6)): print(nm,(h&m).sum(), np.round(C[h&m].mean(0),1) if (h&m).any() else '')
    np.save('hq_s.npy',h)
