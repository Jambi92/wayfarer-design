import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from earsl import slice_loops
z=np.load(sys.argv[1]); V=z['V']; F=[f[f>=0] for f in z['F']]; b=np.array([float(t) for t in sys.argv[2].split(',')]).reshape(3,2); outp=sys.argv[3]
i,j=[int(t) for t in sys.argv[4].split(',')] if len(sys.argv)>4 else (0,2)
ins=lambda p:((p>b[:,0])&(p<b[:,1])).all()
fig,a=plt.subplots(1,1,figsize=(16,14))
S=np.load('/home/claude/stc/rp1/weld.npz')['V']; m=((S>b[:,0])&(S<b[:,1])).all(1); a.scatter(S[m,i],S[m,j],s=0.05,c='0.8')
for f in F:
    if all(ins(V[k]) for k in f):
        q=V[np.r_[f,f[0]]]; a.plot(q[:,i],q[:,j],'b-',lw=0.8)
for k in range(len(V)):
    if ins(V[k]): a.text(V[k,i],V[k,j],str(k),fontsize=8,color='r')
a.set_aspect('equal'); a.grid(alpha=.3)
plt.tight_layout(); plt.savefig(outp,dpi=55)
