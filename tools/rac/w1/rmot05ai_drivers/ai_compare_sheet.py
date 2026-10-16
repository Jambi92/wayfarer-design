# RM-OT-05AD: torso comparison sheet - 05AD baseline | rejected 05AC AC1 | 05AD AC1 retry | retry defects (front + profile).
import sys, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
sys.argv=['x']; exec(open('/home/claude/wayfarer-design/tools/rac/w1/rmot05ac_drivers/ac1_checks.py').read().split('b, a, pp')[0])
B=np.load('after_VF.npz'); VB,F=B['V'],B['F']; VA=np.load('ac1_VF.npz')['V']
G,GF,_=load_glb('/mnt/user-data/uploads/RaceBodies/source/Gorrund-Neutral-C/05AC/GO-05AC_AC1.glb'); G=np.c_[G[:,0],-G[:,2],G[:,1]]
z0=VB[:,2].min()
def shade(V,F,view):
    T=V[F]*100; n=np.cross(T[:,1]-T[:,0],T[:,2]-T[:,0]); n/=np.maximum(np.linalg.norm(n,axis=1),1e-20)[:,None]; c=T.mean(1)
    return (c[:,0],c[:,2]-z0*100,-c[:,1],-n[:,1]) if view=='F' else (-c[:,1],c[:,2]-z0*100,c[:,0],n[:,0])
# defects: opened pairs, flips, SI not recomputed here -> opened pairs + flips
p=cKDTree(VB).query_pairs(1e-5,output_type='ndarray'); s=np.linalg.norm(VA[p[:,0]]-VA[p[:,1]],axis=1)*1000; op=np.unique(p[s>0.01].ravel())
nrm=lambda V: np.cross(V[F[:,1]]-V[F[:,0]],V[F[:,2]]-V[F[:,0]]); fl=np.flatnonzero((nrm(VB)*nrm(VA)).sum(1)<0)
fig,ax=plt.subplots(2,4,figsize=(20,11),facecolor='#222')
for r,view in enumerate('FP'):
    for c,(V,FF,t) in enumerate([(VB,F,'05AI baseline'),(G,GF,'rejected 05AC AC1'),(VA,F,'05AI AC1 (PASS)'),(VA,F,'05AI AC1 defect overlay: 0 opened pairs, 0 flips')]):
        u,v,dp,nd=shade(V,FF,view); m=(v>110)&(v<182)&(nd>0); o=np.argsort(dp[m]); a=ax[r,c]
        a.scatter(u[m][o],v[m][o],c=np.clip(nd[m][o],0,1),cmap='gray',s=0.12,vmin=0,vmax=1,linewidths=0)
        if c==3:
            q=VA[op]*100; uu,vv=(q[:,0],q[:,2]-z0*100) if view=='F' else (-q[:,1],q[:,2]-z0*100); a.scatter(uu,vv,c='red',s=40,marker='o',facecolors='none')
            q=VA[F[fl]].mean(1)*100; uu,vv=(q[:,0],q[:,2]-z0*100) if view=='F' else (-q[:,1],q[:,2]-z0*100); a.scatter(uu,vv,c='yellow',s=60,marker='x')
        a.set_aspect('equal'); a.set_facecolor('#222'); a.axis('off'); a.set_title(t+(' - front' if view=='F' else ' - profile'),color='w',fontsize=10)
plt.tight_layout(); plt.savefig('ai_ac1_compare.jpg',dpi=100,facecolor='#222',pil_kwargs=dict(quality=85))
