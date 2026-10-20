import numpy as np, json, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
z=np.load(sys.argv[1]);V=z['V'];m=json.load(open(sys.argv[1].replace('.npz','_meta.json')))
fig,ax=plt.subplots(1,3,figsize=(27,9)); cs=['r','g','b','m']
for a,(i,j) in zip(ax,[(0,1),(0,2),(1,2)]):
    for di,rs in enumerate(m['rings']):
        for k,r in enumerate(rs):
            P=V[r+r[:1]]; a.plot(P[:,i],P[:,j],cs[di]+'-',lw=0.6+0.8*(k<3),alpha=0.9)
            if k==0:
                for t,v in enumerate(r): a.text(V[v,i],V[v,j],str(t),fontsize=6,color=cs[di])
    for c in m['crotch']: P=V[c]; a.plot(P[:,i],P[:,j],'k-',lw=2)
    P=V[m['O']+m['O'][:1]]; a.plot(P[:,i],P[:,j],'c-',lw=1.5)
    P=V[m['M']+m['M'][:1]]; a.plot(P[:,i],P[:,j],'y-',lw=1.5)
    a.set_aspect('equal'); a.grid(alpha=.3)
plt.tight_layout(); plt.savefig(sys.argv[2],dpi=60)
