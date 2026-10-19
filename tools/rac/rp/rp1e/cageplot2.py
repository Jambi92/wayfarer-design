# cageplot2.py cage.npz axes(e.g. 0,2) box(a0,a1,b0,b1) filt(axis,lo,hi) out.png [labels]
import numpy as np,sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
z=np.load(sys.argv[1]); V=z['V']; F=z['F']
a,b=[int(t) for t in sys.argv[2].split(',')]; bx=[float(t) for t in sys.argv[3].split(',')]
fa,lo,hi=[float(t) for t in sys.argv[4].split(',')]; fa=int(fa)
plt.figure(figsize=(11,11))
for f in F:
    f=f[f>=0]; P=V[f]
    if (P[:,fa]>lo).all() and (P[:,fa]<hi).all() and (P[:,a]>bx[0]).any() and (P[:,a]<bx[1]).any() and (P[:,b]>bx[2]).any() and (P[:,b]<bx[3]).any():
        Q=np.vstack([P,P[:1]]); plt.plot(Q[:,a],Q[:,b],'k-',lw=0.5)
m=(V[:,a]>bx[0])&(V[:,a]<bx[1])&(V[:,b]>bx[2])&(V[:,b]<bx[3])&(V[:,fa]>lo)&(V[:,fa]<hi)
if len(sys.argv)>6:
    for i in np.where(m)[0]: plt.text(V[i,a],V[i,b],str(i),fontsize=6,color='r')
plt.xlim(bx[0],bx[1]); plt.ylim(bx[2],bx[3]); plt.gca().set_aspect('equal'); plt.grid(alpha=.3); plt.savefig(sys.argv[5],dpi=90)
