# regstat.py TAG box(x0,x1,y0,y1,z0,z1) [TAG2 ...] : L4 self-x and source deviation (mm) in a box
import numpy as np,sys
S=np.load('/home/claude/stc/rp1/weld.npz')['V']
b=np.array([float(t) for t in sys.argv[2].split(',')]).reshape(3,2)
mS=((S>b[:,0])&(S<b[:,1])).all(1)
for t in [sys.argv[1]]+sys.argv[3:]:
    X=np.load('sim_%s_L4_sx.npy'%t); X=X.copy(); X[:,1]*=-1 if X.size else 1
    nx=int(((X>b[:,0])&(X<b[:,1])).all(1).sum()) if X.size else 0
    d=np.load('sim_%s_L4_dsp.npy'%t)[mS]
    print('%-8s selfx %5d  dev med %.3f p95 %.3f max %.2f  >1.5 %5d  >3 %5d'%(t,nx,np.median(d),np.percentile(d,95),d.max(),(d>1.5).sum(),(d>3).sum()))
