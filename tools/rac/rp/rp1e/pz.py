import numpy as np,sys
tag=sys.argv[1]; c0=np.array(eval(sys.argv[2])); R=float(sys.argv[3])
z=np.load('sim_%s_L4.npz'%tag); V=z['V'].copy(); V[:,1]*=-1; Q=z['Q']; P=np.load('sim_%s_L4_pairs.npy'%tag)
X=np.array([0.5*(V[Q[i][Q[i]>=0]].mean(0)+V[Q[j][Q[j]>=0]].mean(0)) for i,j in P])
m=np.linalg.norm(X-c0,axis=1)<R; print('n',m.sum())
if m.sum():
    print('min',X[m].min(0).round(2),'max',X[m].max(0).round(2))
    for ax in (1,2): h=np.histogram(X[m][:,ax],bins=8); print('ax',ax,h[0],h[1].round(2))
