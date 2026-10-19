import numpy as np, json, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
s=sys.argv[1]; out=sys.argv[2]
D=json.load(open('fdesign_%s.json'%s)); ax=np.array(D['ax']); lat=np.array(D['lat']); up=np.array([0,0,1.])
cg=np.load('ui_v005.npz')['V']; A=cg[D['ankle_ring']]
rings=[A]+[np.array(x['pts']) for x in D['sections']]
w=np.load('/home/claude/stc/rp1/weld.npz'); V=w['V']; q=np.load('fseg_%s.npz'%s); X=V[q['used']]; X=X[X[:,2]<17]
fig,axs=plt.subplots(1,3,figsize=(36,12))
pr=[(lambda P:P@ax, lambda P:P[:,2]),(lambda P:P@lat, lambda P:P[:,2]),(lambda P:P@lat, lambda P:P@ax)]
cols=plt.cm.viridis(np.linspace(0,1,len(rings)))
for a,(fx,fy) in zip(axs,pr):
    a.scatter(fx(X)[::7],fy(X)[::7],s=0.3,c='0.8')
    for R,c in zip(rings,cols):
        RR=np.vstack([R,R[:1]]); a.plot(fx(RR),fy(RR),'-o',c=c,ms=3)
        a.text(fx(R[:1])[0],fy(R[:1])[0],'0',color=c)
    for j in range(14):
        Cj=np.array([R[j] for R in rings]); a.plot(fx(Cj),fy(Cj),'-',c='r',lw=0.6)
    for nm,T in D['tubes'].items():
        T=np.array(T)
        for R in T: RR=np.vstack([R,R[:1]]); a.plot(fx(RR),fy(RR),'-',c='k',lw=0.8)
    a.set_aspect('equal'); a.grid(True)
plt.savefig(out,dpi=40,bbox_inches='tight')
