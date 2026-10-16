import sys, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.argv=['x']; exec(open('/home/claude/wayfarer-design/tools/rac/w1/rmot05ac_drivers/ac1_checks.py').read().split('b, a, pp')[0])
U='/mnt/user-data/uploads/RaceBodies/source/Gorrund-Neutral-C'
VB,FB,_=load_glb(U+'/05AB1/GO-05AB1_macro_corrected_clean.glb'); VA,FA,_=load_glb(U+'/05AC/GO-05AC_AC1.glb')
kB,ivB=np.unique(np.round(VB,6),axis=0,return_inverse=True); ivB=ivB.ravel(); WB=ivB[FB]
spread=np.load('seam_spread_mm.npy'); bad=spread>0.01
def shade(V,F,view):
    T=V[F]; T=np.stack([T[...,0],-T[...,2],T[...,1]],-1)*100   # x, y(depth, -front), z up
    n=np.cross(T[:,1]-T[:,0],T[:,2]-T[:,0]); n/=np.maximum(np.linalg.norm(n,axis=1),1e-20)[:,None]
    c=T.mean(1)
    if view=='F': u,v,depth,nd=c[:,0],c[:,2],-c[:,1],-n[:,1]
    else: u,v,depth,nd=-c[:,1],c[:,2],c[:,0],n[:,0]   # profile
    return u,v,depth,nd
fig,ax=plt.subplots(2,3,figsize=(15,11),facecolor='#222')
for row,view in enumerate(['F','P']):
    for col,(V,F,t) in enumerate([(VB,FB,'05AB1 baseline'),(VA,FA,'05AC AC1 (UI sculpt)')]):
        u,v,depth,nd=shade(V,F,view)
        m=(v>110)&(v<175)
        if view=='F': m&=(nd>0)
        else: m&=(nd>0)
        o=np.argsort(depth[m]); a=ax[row,col]
        a.scatter(u[m][o],v[m][o],c=np.clip(nd[m][o],0,1),cmap='gray',s=0.15,vmin=0,vmax=1,linewidths=0)
        a.set_aspect('equal'); a.set_facecolor('#222'); a.set_title(f'{t} - {"front" if view=="F" else "profile"}',color='w'); a.axis('off')
    # third column: opened seams in red over after
    u,v,depth,nd=shade(VA,FA,view); m=(v>110)&(v<175)&(nd>0); o=np.argsort(depth[m]); a=ax[row,2]
    a.scatter(u[m][o],v[m][o],c=np.clip(nd[m][o],0,1),cmap='gray',s=0.15,vmin=0,vmax=1,linewidths=0)
    sf=bad[WB].any(1); us,vs,_,ns=shade(VA,FA[sf],view)
    a.scatter(us,vs,c='red',s=1.5,linewidths=0)
    a.set_aspect('equal'); a.set_facecolor('#222'); a.axis('off'); a.set_title('AC1: faces on opened seams (red)',color='w')
plt.tight_layout(); plt.savefig('ac1_compare_sheet.png',dpi=110,facecolor='#222')
