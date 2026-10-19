# cageplot.py CAGE box(x0,x1,y0,y1,z0,z1) out.png [i j] : plot cage faces fully inside box with vertex ids, views (i,j)
import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
z=np.load(sys.argv[1]); V=z['V']; F=[f[f>=0] for f in z['F']]; b=np.array([float(t) for t in sys.argv[2].split(',')]).reshape(3,2); outp=sys.argv[3]
ins=lambda p:((p>b[:,0])&(p<b[:,1])).all()
views=[(0,1),(1,2),(0,2)]
fig,ax=plt.subplots(1,3,figsize=(30,10))
for a,(i,j) in zip(ax,views):
    for f in F:
        if all(ins(V[k]) for k in f):
            q=V[np.r_[f,f[0]]]; a.plot(q[:,i],q[:,j],'b-',lw=0.6)
    for k in range(len(V)):
        if ins(V[k]): a.text(V[k,i],V[k,j],str(k),fontsize=7)
    a.set_aspect('equal'); a.grid(alpha=.3); a.set_title('xyz'[i]+'-'+'xyz'[j])
plt.tight_layout(); plt.savefig(outp,dpi=55)
