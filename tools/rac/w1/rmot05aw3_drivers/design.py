import numpy as np, sys, json; sys.path.insert(0,'/home/claude/aw1'); sys.path.insert(0,'/home/claude/aw1/aw3')
import aw1lib as L; from fields import multigeo, ss
c=json.loads(sys.argv[1]); tag=sys.argv[2]
X0=np.load('/home/claude/aw1/aw2/real/GO-05AW2_nails_final_VF.npz')['V']; PL=np.load('plates.npy',allow_pickle=True).item()
sup=np.load('support_S.npy'); FF=json.load(open('/home/claude/aw1/footframes.json'))
X=X0.copy()
if c.get('A',1):
    R=np.zeros(len(X0))
    for n,P in PL.items():
        core=P['w']>0.5; d=multigeo(core,0.004)
        r=(1-ss((d-c.get('a_flat',0.0003))/c.get('a_ramp',0.0012)))*(P['w']<0.5)
        r*=ss((P['up']/P['Ln']-c.get('a_tip0',0.22))/0.12)          # keep distal free edge crisp
        r*=1-ss((P['up']/P['Ln']-c.get('a_root',1.05))/0.1)
        r[~np.isfinite(d)]=0; R=np.maximum(R,r)
    for _ in range(c.get('a_diff',1)): R=L.Avg@R
    R[~sup]=0; R[L.dup_left]=0; R=np.clip(R,0,1)
    X=L.inflate(X,1-R,c.get('a_h',0.0004)); np.save(f'MA_{tag}.npy',1-R); np.savez(f'A_{tag}_VF.npz',V=X,F=L.F)
if c.get('B',1):
    W={}
    for s_ in 'LR':
        for k in 'PD': W[s_+k]=np.zeros(len(X))
    for n,P in PL.items():
        hs=np.clip(P['w']/c.get('b_core',0.6),0,1); sc=1.0 if n[1]=='1' else c.get('b_lesser',0.8)
        for k in 'PD':
            t=np.clip(P['up']/(c.get('b_frac'+k,0.33)*P['Ln']),0,1); r=(1-t)**c.get('b_pow'+k,1.5)
            W[n[0]+k]=np.maximum(W[n[0]+k],hs*r*sc)
    for key,w in W.items():
        for _ in range(c.get('b_diff',1)): w=L.Avg@w
        w[~sup]=0; w[L.dup_left]=0; W[key]=np.clip(w,0,1)
    for s_ in 'LR':
        a=np.array(FF[s_]['a'])
        X=X+W[s_+'P'][:,None]*(a*c.get('b_P',0.002))[None,:]+W[s_+'D'][:,None]*(np.array([0,0,-1.0])*c.get('b_D',0.0008))[None,:]
    np.savez(f'WB_{tag}.npz',**W)
    np.savez(f'B_{tag}_VF.npz',V=X,F=L.F)
print(tag,'max move mm %.2f'%(np.linalg.norm(X-X0,axis=1).max()*1000))
