# whisker-pad detail analysis/reduction: region ball(s), Taubin-smoothed base, detail scaled by (1-alpha) with smooth falloff
import numpy as np, sys, json
inp,out=sys.argv[1],sys.argv[2]; cfg=json.loads(sys.argv[3])
z=np.load(inp); V=z['V'].astype(float).copy(); Q=z['Q']; Vb=V*np.array([1,-1,1])
cs=[np.array(c) for c in cfg['centres']]; R=cfg['R']; alpha=cfg['alpha']; NIT=cfg.get('nit',60)
w=np.zeros(len(V))
for c,r in zip(cs,R):
    # ellipsoid radii (x,y,z) in blender cm
    d=np.sqrt((((Vb-c)/np.array(r))**2).sum(1)); w=np.maximum(w,np.clip((1-d)/0.35,0,1))
w=w**2*(3-2*w)  # smoothstep
reg=np.where(w>0)[0]; ext=np.where(np.sqrt(((Vb[:,None,:]-np.array(cs)[None])**2).sum(2)).min(1)<max(max(r) for r in R)*1.6)[0]
loc=-np.ones(len(V),int); loc[ext]=np.arange(len(ext))
Qe=Q[(loc[Q]>=0).all(1)]; nb=[set() for _ in ext]
for q in Qe:
    for i in range(4): nb[loc[q[i]]].update((loc[q[i-1]],loc[q[(i+1)%4]]))
nbl=[np.array(sorted(s)) for s in nb]; deg=np.array([len(s) for s in nbl])
B=V[ext].copy(); inner=np.sqrt(((Vb[ext][:,None,:]-np.array(cs)[None])**2).sum(2)).min(1)<max(max(r) for r in R)*1.35
for it in range(NIT):
    for lam in (0.5,-0.53):
        L=np.array([B[n].mean(0) if len(n) else B[i] for i,n in enumerate(nbl)])-B; B[inner]+=lam*L[inner]
D=V[ext]-B; we=w[ext]
Vn=V.copy(); Vn[ext]=B+D*(1-alpha*we)[:,None]
mv=np.linalg.norm(Vn-V,axis=1)*10
print('mask verts',int((w>0).sum()),'moved>0.001mm',int((mv>1e-3).sum()),'max move mm %.3f'%mv.max(),'detail rms in core mm %.3f'%(np.sqrt((D[we>0.9]**2).sum(1).mean())*10))
np.savez_compressed(out,V=Vn,F=z['F'],Q=Q); np.save(out.replace('.npz','_mask.npy'),np.where(w>0)[0]); np.save(out.replace('.npz','_w.npy'),w)
