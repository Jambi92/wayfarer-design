import numpy as np,trimesh,sys,json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
W='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/work'
O=np.array([30.5,-1.3,160.4]); d=np.array([-0.29408,-0.05401,0.95425]); d/=np.linalg.norm(d); e1=np.cross([0,1,0],d); e1/=np.linalg.norm(e1); e2=np.cross(d,e1)
def segs(V,F,th):
    nrm=-np.sin(np.radians(th))*e1+np.cos(np.radians(th))*e2; dv=np.cos(np.radians(th))*e1+np.sin(np.radians(th))*e2
    sd=(V-O)@nrm; T=F[(np.abs(V[F]-O).max((1,2))<22)]; sv=sd[T]; cr=(sv.min(1)<0)&(sv.max(1)>0); out=[]
    for f in T[cr]:
        p=[]
        for i,j in ((0,1),(1,2),(2,0)):
            if (sd[f[i]]<0)!=(sd[f[j]]<0): t=sd[f[i]]/(sd[f[i]]-sd[f[j]]); p.append(V[f[i]]+t*(V[f[j]]-V[f[i]]))
        c=np.array(p)-O; out.append(np.c_[c@dv, c@d])
    return [o for o in out if (o[:,0]>0).all() and (o[:,0]<14).all() and (np.abs(o[:,1])<10).all()]
src=trimesh.load(W+'/F1_working.obj',process=False); b2=trimesh.load(W+'/B2.obj',process=False)
ths=[float(t) for t in sys.argv[2:]]
fig,ax=plt.subplots(2,len(ths)//2,figsize=(3.2*len(ths)//2,9),squeeze=False)
for k,th in enumerate(ths):
    a=ax[k//(len(ths)//2)][k%(len(ths)//2)]
    for m,c,lw in ((src,'0.6',2.5),(b2,'b',0.9)):
        for sg in segs(m.vertices,m.faces,th): a.plot(sg[:,0],sg[:,1],color=c,lw=lw)
    a.set_title('theta %g (grey src, blue B2)'%th,fontsize=8); a.set_aspect('equal'); a.grid(alpha=.3); a.set_xlim(4,14); a.set_ylim(-6,10)
plt.tight_layout(); plt.savefig(sys.argv[1],dpi=75)
