import numpy as np, json, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
cg=sys.argv[1]; js=sys.argv[2]; outp=sys.argv[3]
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V']
z=np.load(cg); V=z['V']; F=[f[f>=0] for f in z['F']]; J=json.load(open(js)); c0=V[J['rings'][-1]].mean(0)
fl=np.array([13.0*(1 if J['side']=='L' else -1),-46,196])
box=(abs(S-fl)<[10,15,10]).all(1); P=S[box]
pairs=np.load(cg.replace('.npz','_pairs.npy')) if len(sys.argv)>4 else []
fig,ax=plt.subplots(1,3,figsize=(24,8))
for a,(i,j,nm) in zip(ax,[(0,2,'front x-z'),(1,2,'side y-z'),(0,1,'top x-y')]):
    a.scatter(P[:,i],P[:,j],s=0.2,c='0.75')
    for f in F:
        c=V[f].mean(0)
        if (abs(c-fl)<[10,15,10]).all():
            q=V[np.r_[f,f[0]]]; a.plot(q[:,i],q[:,j],'b-',lw=0.4)
    for r in J['rings']:
        q=V[r+r[:1]]; a.plot(q[:,i],q[:,j],'m-',lw=0.8)
    q=V[J['loop']+J['loop'][:1]]; a.plot(q[:,i],q[:,j],'c-',lw=1.5)
    for pr in pairs:
        for f in pr:
            q=V[np.r_[F[f],F[f][0]]]; a.plot(q[:,i],q[:,j],'r-',lw=2)
    a.set_aspect('equal'); a.set_title(nm)
plt.tight_layout(); plt.savefig(outp,dpi=65)
