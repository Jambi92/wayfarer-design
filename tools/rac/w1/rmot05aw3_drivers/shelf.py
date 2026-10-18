import numpy as np,sys,json; sys.path.insert(0,'/home/claude/aw1'); sys.path.insert(0,'/home/claude/aw1/aw3'); import aw1lib as L; from fields import multigeo, ss
c=json.loads(sys.argv[1]); src=sys.argv[2]; tag=sys.argv[3]
X0=np.load(src)['V']; PL=np.load('plates.npy',allow_pickle=True).item(); sup=np.load('support_S.npy')
P=PL['L1']; T=P['T']; a=P['a']; vn=L.vnormals(X0)
z=X0[:,2]-T[2]
w=ss((z+c.get('z0',0.013))/0.002)*(1-ss((z+c.get('z1',0.004))/0.0015))*ss(((vn@a)-0.2)/0.2)*(np.linalg.norm((X0-T)[:,:2]@np.array([[1,0],[0,1]]),axis=1)<0.03)
w*=(np.abs((X0-T)@np.array(json.load(open('/home/claude/aw1/footframes.json'))['L']['p']))<c.get('xw',0.013))
for _ in range(3): w=L.Avg@w
db=multigeo(~sup,0.005); w*=ss((np.nan_to_num(db,posinf=1)-c.get('b0',0.0))/c.get('br',0.0008))
nail=np.zeros(len(X0),bool)
for Q in PL.values(): nail|=Q['w']>0.03
dn=multigeo(nail,0.004); w*=ss((np.nan_to_num(dn,posinf=1)-c.get('n0',0.0006))/0.0008)
w[~sup]=0; w[L.dup_left]=0
M0=np.load(c['prevM']) if 'prevM' in c else np.ones(len(X0))
M=np.minimum(M0,1-w)
X=L.smooth(X0,M,c.get("n",20)) if c.get("lap") else L.hc_smooth(X0,M,c.get("n",20),alpha=0.0,beta=0.6)
np.save(f'M_{tag}.npy',M); np.savez(f'{tag}_VF.npz',V=X,F=L.F); print(tag,'max mm %.3f'%(np.linalg.norm(X-X0,axis=1).max()*1000),(w>0.01).sum())
