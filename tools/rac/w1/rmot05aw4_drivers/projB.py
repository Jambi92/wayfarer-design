import numpy as np,sys,json; sys.path.insert(0,'/home/claude/aw1/aw4'); from proj import proj, PL, FF
src=sys.argv[1]; tag=sys.argv[2]; target=float(sys.argv[3]); D=float(sys.argv[4])
X0=np.load(src)['V']; W=np.load('/home/claude/aw1/aw3/WB_d3.npz'); p0=proj(X0)
G={'L':np.zeros(len(X0)),'R':np.zeros(len(X0))}
for n,P in PL.items():
    if n[1]=='1': continue
    k=(target-p0[n]['projection_mm'])/D; assert 0<k<=1,(n,k)
    own=(P['w']>0.01)|(np.linalg.norm(X0-P['T'],axis=1)<0.006)     # this nail's neighbourhood
    w=np.where(own,W[n[0]+'P']/0.8,0)*k
    G[n[0]]=np.maximum(G[n[0]],np.clip(w,0,1))
X=X0.copy()
for s in 'LR': X=X+G[s][:,None]*(np.array(FF[s]['a'])*D/1000)[None]
np.savez(f'GB_{tag}.npz',AW4_LP=G['L'],AW4_RP=G['R']); np.savez(f'B_{tag}_VF.npz',V=X,F=np.load(src)['F'])
print({k:v['projection_mm'] for k,v in proj(X).items()})
