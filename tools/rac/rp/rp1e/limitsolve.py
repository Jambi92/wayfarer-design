# limitsolve.py IN.npz OUT.npz TARGETS.json : choose positions of the listed cage verts so that their level-1 limit points
# (Blender Subdivision level 1, limit surface on) land on the given targets; all other cage verts fixed.
# TARGETS.json: {"vid": [x,y,z], ...}. env DAMP (Tikhonov weight toward current position, default 1e-3)
import sys, os, json, numpy as np, scipy.sparse as sp
from scipy.sparse.linalg import lsqr
sys.path.insert(0,'/home/claude/stc/rp1e')
from ccmat import cc_step, limit_matrix
z=np.load(sys.argv[1]); V=z['V'].astype(float).copy(); F=[list(map(int,f[f>=0])) for f in z['F']]
T={int(k):np.array(v,float) for k,v in json.load(open(sys.argv[3])).items()}
M,F1=cc_step(len(V),F); M=(limit_matrix(M.shape[0],F1)@M).tocsr()
ids=sorted(T); rows=M[ids]; cols=np.array(ids)
A=rows[:,cols].toarray(); other=np.setdiff1d(np.arange(len(V)),cols); B=rows[:,other]
dmp=float(os.environ.get('DAMP','1e-3'))
for d in range(3):
    rhs=np.array([T[i][d] for i in ids])-B@V[other,d]
    AA=np.vstack([A,np.sqrt(dmp)*np.eye(len(ids))]); bb=np.r_[rhs,np.sqrt(dmp)*V[cols,d]]
    V[cols,d]=np.linalg.lstsq(AA,bb,rcond=None)[0]
L=M@V
for i in ids: print(i,'target',T[i].round(2),'limit',L[i].round(2),'cage',V[i].round(2),'moved %.2f'%np.linalg.norm(V[i]-z['V'][i]))
np.savez_compressed(sys.argv[2],V=V,F=z['F'])
import shutil; shutil.copy(sys.argv[1].replace('.npz','_col.npy'),sys.argv[2].replace('.npz','_col.npy'))
