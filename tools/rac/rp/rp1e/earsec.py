import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
s=sys.argv[1]; out=sys.argv[2]
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64)
sg=1 if s=='L' else -1
floor=np.array([12.1*sg,-43.5,198.8]) if s=='L' else None
e=np.load('ear_%s.npy'%s); d=np.load('sim_b4_L3_dsp.npy'); P=S[e]; floor=P[d[e]>=np.percentile(d[e],95)].mean(0)
mouth=S[np.load('earroot_%s.npy'%s)].mean(0); A=mouth-floor; A/=np.linalg.norm(A)
u=np.cross(A,[0,0,1.0]); u/=np.linalg.norm(u); v=np.cross(A,u)
box=(abs(S-floor)<[9,11,9]).all(1); Fb=SF[box[SF].all(1)]
fig,axs=plt.subplots(2,4,figsize=(28,14))
for a,th in zip(axs.ravel(),np.linspace(0,2*np.pi,8,endpoint=False)):
    e1=np.cos(th)*u+np.sin(th)*v; n=np.cross(A,e1)   # plane spanned by A,e1 ; normal n
    dd=(S-floor)@n; sgn=np.sign(dd[Fb]); T=Fb[(sgn.min(1)<0)&(sgn.max(1)>0)]
    for t in T:
        q=[]
        for i,j in ((0,1),(1,2),(2,0)):
            if dd[t[i]]*dd[t[j]]<0: al=dd[t[i]]/(dd[t[i]]-dd[t[j]]); q.append(S[t[i]]+(S[t[j]]-S[t[i]])*al)
        if len(q)==2:
            q=np.array(q)-floor; r=q@e1; h=q@A
            if (r>-0.5).all(): a.plot(r,h,'k',lw=0.8)
    a.plot([0],[0],'ro'); a.set_aspect('equal'); a.grid(alpha=.3); a.set_title('theta %d deg'%np.degrees(th)); a.set_xlabel('r (along e)'); a.set_ylabel('h (along axis, out)')
plt.savefig(out,dpi=50,bbox_inches='tight'); print('floor',floor.round(1),'axis',A.round(2),'u',u.round(2),'v',v.round(2))
