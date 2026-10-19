import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
s=sys.argv[1]; zs=[float(x) for x in sys.argv[2].split(',')]
w=np.load('/home/claude/stc/rp1/weld.npz'); V=w['V'].astype(float); F=w['F']
m=(w['w_hand_'+s]>0.5)|(w['w_forearm_'+s]>0.5); Fm=F[m[F].all(1)]
vl=np.load('vlab_%s.npy'%s); lab=-np.ones(len(V),int); lab[vl[:,0]]=vl[:,1]
cg=np.load('/home/claude/stc/rp1/ck/v004a.npz'); Vc=cg['Vc']*[1,-1,1]
n=len(zs); fig,ax=plt.subplots(2,(n+1)//2,figsize=(7*((n+1)//2),14)); ax=ax.ravel()
cols=['r','g','b','m','c']
for a,z0 in zip(ax,zs):
    d=V[:,2]-z0; T=Fm[(np.sign(d[Fm]).min(1)<0)&(np.sign(d[Fm]).max(1)>0)]
    for t in T:
        pts=[]
        for i,j in ((0,1),(1,2),(2,0)):
            if d[t[i]]*d[t[j]]<0: u=d[t[i]]/(d[t[i]]-d[t[j]]); pts.append(V[t[i]]+(V[t[j]]-V[t[i]])*u)
        if len(pts)==2:
            l=lab[t[0]]; a.plot([pts[0][0],pts[1][0]],[pts[0][1],pts[1][1]],c=cols[l] if l>=0 else 'k',lw=1)
    cc=(np.abs(Vc[:,2]-z0)<1.5)&(np.linalg.norm(Vc[:,:2]-V[m][:,:2].mean(0),axis=1)<14); a.plot(Vc[cc,0],Vc[cc,1],'x',c='orange')
    a.set_aspect('equal'); hb=V[m&(np.abs(V[:,2]-z0)<12)]; a.set_xlim(hb[:,0].min()-1,hb[:,0].max()+1); a.set_ylim(hb[:,1].min()-1,hb[:,1].max()+1); a.set_title('z=%.1f'%z0); a.grid(True)
plt.savefig('sec_%s.png'%s,dpi=40,bbox_inches='tight')
