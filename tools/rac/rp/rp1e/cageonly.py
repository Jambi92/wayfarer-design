# cageonly.py cage.npz box out.png elev_axis... : 2D projection of cage edges in a box onto plane (a,b) with labels optional
import numpy as np,sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
z=np.load(sys.argv[1]); V=z['V']; F=z['F']; b=np.array([float(t) for t in sys.argv[2].split(',')]).reshape(3,2)
a,c=[int(t) for t in sys.argv[4].split(',')]; lab=len(sys.argv)>5
ins=((V>b[:,0])&(V<b[:,1])).all(1)
plt.figure(figsize=(12,12))
for f in F:
    f=f[f>=0]
    if ins[f].all():
        P=V[f]; Q=np.vstack([P,P[:1]]); plt.plot(Q[:,a],Q[:,c],'k-',lw=0.4)
if lab:
    for i in np.where(ins)[0]: plt.text(V[i,a],V[i,c],str(i),fontsize=5,color='r')
plt.gca().set_aspect('equal'); plt.grid(alpha=.2); plt.savefig(sys.argv[3],dpi=100)
