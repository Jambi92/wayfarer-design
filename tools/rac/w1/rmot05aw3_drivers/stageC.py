import numpy as np, sys, json; sys.path.insert(0,'/home/claude/aw1'); sys.path.insert(0,'/home/claude/aw1/aw3')
import aw1lib as L; from fields import multigeo, ss
c=json.loads(sys.argv[1]); src=sys.argv[2]; tag=sys.argv[3]
X0=np.load(src)['V']; PL=np.load('plates.npy',allow_pickle=True).item(); sup=np.load('support_S.npy')
nail=np.zeros(len(X0),bool)
for P in PL.values(): nail|=P['w']>c.get('c_nailthr',0.03)
dn=multigeo(nail,0.012); keepn=ss((np.nan_to_num(dn,nan=1)-c.get('c_n0',0.0004))/c.get('c_nr',0.0008))   # 0 on/near nail
db=multigeo(~sup,0.01); inner=ss((np.nan_to_num(db,nan=1)-c.get('c_b0',0.001))/c.get('c_br',0.003))
FF=json.load(open('/home/claude/aw1/footframes.json')); vn=L.vnormals(X0); fac=np.zeros(len(X0))
for s_ in 'LR':
    a=np.array(FF[s_]['a']); side=np.sign(X0[:,0])==(1 if s_=='L' else -1); up=vn@np.array([0,0,1.0])+0.8*(vn@a); fac[side]=ss((up[side]-c.get('c_up',0.2))/0.3)
for _ in range(3): fac=L.Avg@fac
w=inner*keepn*fac*(1-ss((np.nan_to_num(dn,posinf=1)-c.get("c_far",0.006))/0.002))
for fid in c.get('pin',[]):
    src=np.zeros(len(X0),bool); src[L.F[fid]]=True; dp=multigeo(src,0.004); w*=ss((np.nan_to_num(dp,posinf=1)-c.get('pin_r',0.0008))/c.get('pin_ramp',0.0012))
w[L.dup_left]=0; w[~sup]=0; M=1-w
X=L.hc_smooth(X0,M,c.get('c_n',15),alpha=0.0,beta=c.get('c_beta',0.6))
np.save(f'MC_{tag}.npy',M); np.savez(f'C_{tag}_VF.npz',V=X,F=L.F)
print(tag,'max move mm %.3f'%(np.linalg.norm(X-X0,axis=1).max()*1000), 'n weighted',(w>0.01).sum())
