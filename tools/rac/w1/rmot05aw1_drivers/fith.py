import numpy as np,sys;sys.path.insert(0,'/home/claude/aw1');import aw1lib as L
S=np.load(sys.argv[1])['V'];R=np.load(sys.argv[2])['V'];M=np.load(sys.argv[3]);nmax=int(sys.argv[4])
print('moved by this step mm',np.linalg.norm(R-S,axis=1).max()*1000)
for f in (1.0,0.5,0.25):
    X=S.copy();best=None
    for n in range(1,nmax):
        X=L.hc_smooth(X,1-(1-M)*f,1,0.0,0.6);e=np.abs(X-R).max()*1000
        if best is None or e<best[1]: best=(n,e)
    print('fade',f,'best',best)
