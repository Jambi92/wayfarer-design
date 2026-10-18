import numpy as np,sys;sys.path.insert(0,'/home/claude/aw1');import aw1lib as L
R=np.load(sys.argv[1])['V'];M=np.load(sys.argv[2]);X=L.V0.copy();best=None
for n in range(1,int(sys.argv[3])):
    X=L.smooth(X,M,1);e=np.abs(X-R).max()*1000
    if best is None or e<best[1]: best=(n,e)
print('best',best)
