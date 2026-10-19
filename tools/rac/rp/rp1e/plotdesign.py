import numpy as np, json, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
s=sys.argv[1]; cg=sys.argv[2]; roles=sys.argv[3].split(','); out=sys.argv[4]
q=np.load('segH_%s.npz'%s); u=q['used']; l=q['lab']; V=np.load('/home/claude/stc/rp1/weld.npz')['V'][u]
z=np.load(cg); C=z['V']; meta=json.load(open(cg.replace('.npz','_meta.json')))[s]
rmap={'R':{0:'middle',1:'ring',2:'index',3:'thumb',4:'pinky',9:'palm'},'L':{0:'pinky',1:'thumb',2:'ring',3:'middle',4:'index',9:'palm'}}[s]
cols={'index':'b','middle':'r','ring':'g','pinky':'c','thumb':'m','palm':'0.8'}
fig,ax=plt.subplots(1,3,figsize=(33,12))
for a,(i,j,k,sg) in zip(ax,[(0,1,2,1),(0,2,1,1),(1,2,0,1 if s=='R' else -1)]):
    sel=np.array([rmap[x] in roles for x in l]); X=V[sel]; L_=l[sel]; o=np.argsort(sg*X[:,k])
    a.scatter(X[o,i],X[o,j],c=[cols[rmap[x]] for x in L_[o]],s=2,alpha=0.35)
    for r in roles:
        if r=='palm': continue
        R=meta['tubes'][r]['rings']
        for ring in R:
            P=C[ring+[ring[0]]]; a.plot(P[:,i],P[:,j],'-',c='k',lw=1.5)
        for c_ in range(4):
            P=C[[ring[c_] for ring in R]]; a.plot(P[:,i],P[:,j],'-',c=cols[r],lw=1.5)
    a.set_aspect('equal'); a.grid(True)
plt.savefig(out,dpi=40,bbox_inches='tight')
