import numpy as np, scipy.sparse as sp, json
from scipy.sparse.csgraph import dijkstra, connected_components
V15='/home/claude/wayfarer-design/reviews/rac-rp1f-evidence/gorrund_v015/design/design_v015_production_L4.npz'
def load15():
    p=np.load(V15); return p['V']*np.array([1,-1,1]), p['Q'].astype(np.int64)
def load107():
    r=np.load('/tmp/claude-0/hand/r107.npz'); return r['V']*100, r['F'].astype(np.int64), r['mat']
def edges_q(Q): 
    E=np.vstack([Q[:,[i,(i+1)%4]] for i in range(4)]); E=np.sort(E,1); return np.unique(E,axis=0)
def edges_t(F):
    E=np.vstack([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); E=np.sort(E,1); return np.unique(E,axis=0)
def graph(V,E):
    w=np.linalg.norm(V[E[:,0]]-V[E[:,1]],axis=1)
    return sp.coo_matrix((np.r_[w,w],(np.r_[E[:,0],E[:,1]],np.r_[E[:,1],E[:,0]])),shape=(len(V),len(V))).tocsr()
def geod(G,src,limit=np.inf):
    return dijkstra(G,indices=src,limit=limit,min_only=True)
def euler_sub(faces,nv=None):
    u=np.unique(faces); E=edges_q(faces) if faces.shape[1]==4 else edges_t(faces)
    return len(u)-len(E)+len(faces)
def frames():
    return json.load(open('/tmp/claude-0/rp1f/hand_frames.json'))
