import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, sys
cage=sys.argv[1]; c0=np.array(eval(sys.argv[2])); R=float(sys.argv[3]); out=sys.argv[4]; views=eval(sys.argv[5]) if len(sys.argv)>5 else [(1,2),(0,2),(0,1)]
z=np.load(cage);V=z['V'];F=[f[f>=0] for f in z['F']]
S=np.load('/home/claude/stc/rp1/weld.npz')['V']; ms=np.all(np.abs(S-c0)<R,axis=1)
fig,ax=plt.subplots(1,len(views),figsize=(8*len(views),8))
for a,(i,j) in zip(np.atleast_1d(ax),views):
    a.scatter(S[ms,i],S[ms,j],s=0.3,c='0.75')
    for f in F:
        P=V[f]
        if np.all(np.abs(P-c0)<R*1.3).any() and np.any(np.all(np.abs(P-c0)<R,axis=1)):
            Q=np.vstack([P,P[:1]]); a.plot(Q[:,i],Q[:,j],'r-',lw=0.6)
    m=np.all(np.abs(V-c0)<R,axis=1)
    for k in np.where(m)[0]: a.text(V[k,i],V[k,j],str(k),fontsize=7,color='b')
    a.set_xlim(c0[i]-R,c0[i]+R); a.set_ylim(c0[j]-R,c0[j]+R); a.set_aspect('equal')
plt.tight_layout(); plt.savefig(out,dpi=70)
