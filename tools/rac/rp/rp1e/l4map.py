import numpy as np, sys
cage=np.load(sys.argv[1]); F=[f[f>=0] for f in cage['F']]; Vc=cage['V']
z=np.load(sys.argv[2]);V=z['V']*np.array([1,-1,1]);Q=z['Q']; L=int(sys.argv[3]) if len(sys.argv)>3 else 4
cnt=np.array([len(f)*4**(L-1) for f in F]); off=np.r_[0,np.cumsum(cnt)]; assert off[-1]==len(Q),(off[-1],len(Q))
C=V[Q].mean(1)
for c in eval(sys.argv[4]):
    d=np.linalg.norm(C-np.array(c),axis=1); i=int(np.argmin(d)); k=int(np.searchsorted(off,i,side='right')-1)
    f=F[k]; print(c,'L4 face',i,'dist',round(float(d[i]),3),'cage face',k,list(map(int,f)),'cage edges',np.round(np.linalg.norm(Vc[f]-np.roll(Vc[f],-1,0),axis=1),2))
