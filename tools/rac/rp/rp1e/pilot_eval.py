# pilot_eval.py TAG BASE "centre" R [feature_radius] : regional pilot metrics
import sys, numpy as np, re
from scipy.spatial import cKDTree
tag,base=sys.argv[1],sys.argv[2]; c=np.array(eval(sys.argv[3])); R=float(sys.argv[4]); fr=float(sys.argv[5]) if len(sys.argv)>5 else 1.0
S=np.load('/home/claude/stc/rp1/weld.npz')['V']; m=np.linalg.norm(S-c,axis=1)<fr
import igl
def dev(t,L):
    z=np.load('sim_%s_L%d.npz'%(t,L)); V=z['V'].astype(float).copy(); V[:,1]*=-1
    d,_,_=igl.point_mesh_squared_distance(S[m],V,z['F'].astype(np.int64)); return np.sqrt(d).max()*10
def sx(t,L):
    X=np.load('sim_%s_L%d_sx.npy'%(t,L))[:,:3]*np.array([1,-1,1]); return X
out=[]
for L in (1,4):
    X=sx(tag,L); B=sx(base,L); inR=np.linalg.norm(X-c,axis=1)<R; inRb=np.linalg.norm(B-c,axis=1)<R
    far=X[~inR]; d,_=cKDTree(B).query(far) if len(B) else (np.full(len(far),9),None); new_else=int((d>0.3).sum())
    out.append('L%d dev %.2f (base %.2f)  region sx %d (base %d)  new sx elsewhere %d  total %d'%(L,dev(tag,L),dev(base,L),inR.sum(),inRb.sum(),new_else,len(X)))
print('\n'.join(out))
try:
    for l in open('%s.cls'%tag):
        g=re.search(r'c=\[([^\]]+)\] dot=([-0-9.]+)',l)
        if g:
            p=np.array([float(x) for x in g.group(1).split(',')])
            if np.linalg.norm(p-c)<R: print('  cls',l.strip()[:150])
except FileNotFoundError: pass
