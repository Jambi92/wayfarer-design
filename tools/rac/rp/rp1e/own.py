# own.py CAGE.npz SPEC.json OUT.npz : per-sheet projection ownership for a thin-feature region (v014 ruling P1).
# SPEC: {"tag":"ax","regions":[{"centre":[..],"Rc":cage radius,"Rs":source radius,"d":[dx,dy,dz],"ids":[cA,cB],"base":c,"dead":0.15,
#        "crest_both":true}]}
# Source sheets: faces of the base-colour target within Rs of centre, split by sign(n.d) (|n.d|<dead -> both sheets if crest_both).
# Cage verts within Rc: side = sign(n_cage.d); |n_cage.d|<dead keep the base colour (shared crest).
# Writes OUT.npz (=cage), OUT_col.npy, OUT_remap.npy (identity) and targets <TPRE>_c<id>.npz in the prefix dir tgx_<tag>
#   (symlinks to tg_r3m5 for every other colour).  Print TPRE/XFN to use with runc.sh.
import sys, json, os, numpy as np, shutil
from scipy.spatial import cKDTree
inp,specp,out=sys.argv[1:4]; S=json.load(open(specp))
z=np.load(inp); V=z['V'].astype(float); F=[[int(x) for x in f if x>=0] for f in z['F']]; col=np.load(inp.replace('.npz','_col.npy')).copy()
# cage vertex normals
N=np.zeros_like(V)
for f in F:
    P=V[f]; n=np.zeros(3)
    for i in range(len(f)): n+=np.cross(P[i],P[(i+1)%len(f)])
    for v in f: N[v]+=n
N/=np.linalg.norm(N,axis=1)[:,None]+1e-12
pre='tgx_'+S['tag']; os.makedirs(pre,exist_ok=True)
for fn in os.listdir('.'):
    if fn.startswith('tg_r3m5_c') and fn.endswith('.npz'):
        dst=os.path.join(pre,'t_'+fn[len('tg_r3m5_'):])
        if not os.path.exists(dst): os.symlink(os.path.abspath(fn),dst)
newids=[]
for R in S['regions']:
    c0=np.array(R['centre']); d=np.array(R['d'],float); d/=np.linalg.norm(d); dead=R.get('dead',0.15)
    bases=R['base'] if isinstance(R['base'],list) else [R['base']]; TVs=[];TFs=[];off=0
    for b in bases:
        t=np.load('tg_r3m5_c%d.npz'%b); TVs.append(t['V'].astype(float)); TFs.append(t['F'].astype(np.int64)+off); off+=len(t['V'])
    TV=np.vstack(TVs); TF=np.vstack(TFs)
    C=TV[TF].mean(1); n=np.cross(TV[TF[:,1]]-TV[TF[:,0]],TV[TF[:,2]]-TV[TF[:,0]]); n/=np.linalg.norm(n,axis=1)[:,None]+1e-12
    near=np.linalg.norm(C-c0,axis=1)<R['Rs']; s=n@d
    if 'cut' in R:
        cp,cn=np.array(R['cut'][0]),np.array(R['cut'][1]); near&=((C-cp)@cn<0)
    for sgn,cid in zip((1,-1),R['ids']):
        keep=near&((sgn*s>dead)|((np.abs(s)<=dead)&R.get('crest_both',True)))
        # keep the rest of the base target outside the region so the sheet target stays continuous at the region edge
        keep|=~near & (np.linalg.norm(C-c0,axis=1)<R['Rs']+R.get('apron',1.5)) & (sgn*s>-0.3)
        Fc=TF[keep]; used=np.unique(Fc); mp=-np.ones(len(TV),int); mp[used]=np.arange(len(used))
        np.savez_compressed(os.path.join(pre,'t_c%d.npz'%cid),V=TV[used],F=mp[Fc]); newids.append(cid)
    m=(np.linalg.norm(V-c0,axis=1)<R['Rc'])&np.isin(col,bases)
    if 'cut' in R: m&=((V-cp)@cn<0)
    if 'verts' in R: mm=np.zeros(len(V),bool); mm[R['verts']]=True; m&=mm
    sv=N@d
    col[m&(sv>dead)]=R['ids'][0]; col[m&(sv<-dead)]=R['ids'][1]
    print('region',R['centre'],'cage verts A/B',int((m&(sv>dead)).sum()),int((m&(sv<-dead)).sum()),'crest(base)',int((m&(np.abs(sv)<=dead)).sum()))
shutil.copy(inp,out); np.save(out.replace('.npz','_col.npy'),col); np.save(out.replace('.npz','_remap.npy'),np.arange(len(V)))
print('TPRE=%s/t XFN=,%s'%(pre,','.join(map(str,newids))))
