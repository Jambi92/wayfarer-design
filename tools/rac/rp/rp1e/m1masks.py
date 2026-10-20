# m1masks.py OUTDIR : explicit frozen source face masks for the R hand B-C slit (order section 5) + derived targets tgx_m1p/
import sys, os, json, numpy as np
from scipy.spatial import cKDTree
out=sys.argv[1]; os.makedirs(out,exist_ok=True)
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64); C=S[SF].mean(1)
cr=np.array(json.load(open("/tmp/claude-0/pants_b1.json"))["crease"])
YM=-40.85
zone=(C[:,0]>-35.6)&(C[:,0]<-29.5)&(C[:,1]>-43.0)&(C[:,1]<-38.6)&(C[:,2]>90.3)&(C[:,2]<96.0)
# tip curve x_tip(z): left boundary of the bar in the mid-plane; outside the crease z-range the bar boundary continues (use bar section extent)
zs=cr[:,2]; xs=cr[:,0]
def xtip(z): return np.interp(z,zs,xs,left=xs[0],right=xs[-1])
d_cr=np.min([np.linalg.norm(C-(cr[i]+t*(cr[i+1]-cr[i])),axis=1) for i in range(4) for t in np.linspace(0,1,6)],axis=0)
crease=zone&(d_cr<0.15)
fused=zone&~crease&(C[:,0]>=xtip(C[:,2]))
Bw=zone&~crease&~fused&(C[:,1]<YM)
Cw=zone&~crease&~fused&(C[:,1]>=YM)
for nm,m in (('Rhand_B_wall_source_faces',Bw),('Rhand_C_wall_source_faces',Cw),('Rhand_shared_crease_source_faces',crease),('Rhand_fused_exterior_source_faces',fused)):
    np.save(os.path.join(out,nm+'.npy'),np.where(m)[0]); print(nm,int(m.sum()))
# targets: 22 (B) minus C-wall faces, 23 (C) minus B-wall faces
kS=cKDTree(S); pre='tgx_m1p'; os.makedirs(pre,exist_ok=True)
for fn in os.listdir('.'):
    if fn.startswith('tg_r3m5_c') and fn.endswith('.npz'):
        dst=os.path.join(pre,'t_'+fn[len('tg_r3m5_'):])
        if not os.path.lexists(dst): os.symlink(os.path.abspath(fn),dst)
fkey={tuple(sorted(f)):i for i,f in enumerate(SF[zone])}
zid=np.where(zone)[0]
for col,exclude in ((22,Cw),(23,Bw)):
    t=np.load('tg_r3m5_c%d.npz'%col); TV=t['V'].astype(float); TF=t['F'].astype(np.int64); _,iv=kS.query(TV)
    sfi=[fkey.get(tuple(sorted(iv[f]))) for f in TF]; bad=np.array([k is not None and exclude[zid[k]] for k in sfi])
    Fc=TF[~bad]; used=np.unique(Fc); mp=-np.ones(len(TV),int); mp[used]=np.arange(len(used))
    dst=os.path.join(pre,'t_c%d.npz'%col)
    if os.path.lexists(dst): os.remove(dst)
    np.savez_compressed(dst,V=TV[used],F=mp[Fc]); print('target',col,'removed opposite-wall faces',int(bad.sum()))
