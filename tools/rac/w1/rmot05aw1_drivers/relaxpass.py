import numpy as np,sys;sys.path.insert(0,'/home/claude/aw1');import aw1lib as L
src,mfile,tag,n=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]);sup=np.load(sys.argv[5])
X=np.load(src)['V'];from scipy.sparse.csgraph import dijkstra
mv=np.linalg.norm(X-L.V0,axis=1)>1e-6
d=dijkstra(L.G,directed=False,indices=np.where(mv)[0],limit=0.005,min_only=True)
wr=1-L.ss((d-0.002)/0.003);wr[~sup]=0;Mr=1-wr;Mr[L.dup_left]=1;np.save(mfile,Mr)
Y=L.relax(X,Mr,n);np.savez(f'{tag}_VF.npz',V=Y,F=L.F);print(tag,'relax verts',(wr>0).sum())
