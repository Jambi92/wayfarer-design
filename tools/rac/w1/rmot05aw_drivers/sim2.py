import numpy as np, sys, json, pickle, os; sys.path.insert(0,'/home/claude/aw'); from nails2 import *
D=np.load('/home/claude/aw/src_VF.npz'); V0=D['V']; F=D['F']; N=np.load('/home/claude/aw/N.npy')
import trimesh
kk,ivv=np.unique(np.round(V0,7),axis=0,return_inverse=True); ivv=ivv.ravel(); _m=trimesh.Trimesh(kk,ivv[F],process=False); N=_m.vertex_normals[ivv]
cfg=json.loads(sys.argv[1]); tag=sys.argv[2]; wk=json.dumps(cfg.get('w',{}),sort_keys=True)
cache=f'/home/claude/aw/W3_{abs(hash(wk))%10**8}.pkl'
if cfg.get('Wfile'): W=pickle.load(open(cfg['Wfile'],'rb'))
elif os.path.exists(cache): W=pickle.load(open(cache,'rb'))
else:
    iv,A=weld_adj(V0,F); W={n:nail_weight(V0,F,N,n,iv,A,**cfg.get('w',{})) for n in NAILS}; pickle.dump(W,open(cache,'wb'))
V=V0.copy(); ui={}
for n in NAILS:
    w,fr=W[n]; pr=cfg.get(n,cfg['*']); sx,curl,te,tn=pr
    loc0=np.round(fr['Pp'],5); M0=empty_mat(loc0,[0,0,YAW[n[0]]],[1,1,1])
    loc1=np.round(loc0+fr['e']*te+fr['n']*tn,5); M1=empty_mat(loc1,[curl,0,YAW[n[0]]],[sx,1,1])
    V=apply_hook(V,w,M0,M1); ui[n]=dict(group='AW_'+n,loc0=loc0.tolist(),loc1=loc1.tolist(),rotZ=YAW[n[0]],rotX=curl,scaleX=sx,nverts=int((w>0).sum()))
np.savez(f'/home/claude/aw/{tag}_VF.npz',V=V,F=F); json.dump(ui,open(f'/home/claude/aw/{tag}_ui.json','w'),indent=1)
np.savez(f'/home/claude/aw/{tag}_groups.npz',**{'AW_'+n:W[n][0] for n in NAILS})
sys.path.insert(0,'/home/claude/av'); from avlib import measure
for s in 'LR': m0=measure(V0,s); m1=measure(V,s); print(s,'length %.3f -> %.3f  width %.3f -> %.3f heel %.3f->%.3f minz %.3f'%(m0['length'],m1['length'],m0['width_fp'],m1['width_fp'],m0['heel'],m1['heel'],V[m1 and frame(V,s)[0],2].min()*100))
for n in NAILS: print(n,ui[n]['nverts'],'L %.2f cm'%(W[n][1]['L']*100),'max mm %.2f'%(np.linalg.norm(V-V0,axis=1)[W[n][0]>0].max()*1000))
