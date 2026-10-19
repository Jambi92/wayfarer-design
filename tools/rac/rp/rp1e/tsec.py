import numpy as np, sys, json, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
# vertical sections along a toe's axis (plane containing toe axis & up, offsets across): source black, prod red, cage green
s=sys.argv[1]; toe=sys.argv[2]; prod=sys.argv[3]; cg=sys.argv[4]; offs=[float(x) for x in sys.argv[5].split(',')]; out=sys.argv[6]
dg=json.load(open('digits_F%s.json'%s))[toe]; Cc=np.array(dg['c']); Ta=Cc[-1]-Cc[0]; Ta[2]=0; Ta/=np.linalg.norm(Ta); n=np.cross(Ta,[0,0,1.])
w=np.load('/home/claude/stc/rp1/weld.npz'); V=w['V'].astype(float); F=w['F']
Pm=np.load(prod); PV=Pm['V']*np.array([1,-1,1]); PQ=Pm['Q']; z=np.load(cg); C=z['V']; CF=z['F']
o=Cc[0]
def segs(V,F,c,a,col,lw):
    d=(V-o)@n-c; sel=(np.abs(d)<4)&(np.linalg.norm((V-o)[:,:2],axis=1)<14)&(V[:,2]<14)
    F=F[np.array([sel[f[f>=0]].all() for f in F])]
    for f in F:
        f=f[f>=0]; pts=[]
        for i in range(len(f)):
            a_,b_=f[i],f[(i+1)%len(f)]
            if d[a_]*d[b_]<0: u=d[a_]/(d[a_]-d[b_]); pts.append(V[a_]+(V[b_]-V[a_])*u)
        if len(pts)>=2: p=np.array(pts[:2]); a.plot((p-o)@Ta,p[:,2],c=col,lw=lw)
fig,ax=plt.subplots(1,len(offs),figsize=(9*len(offs),5))
for a,c in zip(np.atleast_1d(ax),offs):
    segs(V,F,c,a,'k',1); segs(PV,PQ,c,a,'r',1); segs(C,CF,c,a,'g',2); a.set_aspect('equal'); a.grid(True); a.set_title('%s off %.1f'%(toe,c)); a.set_xlim(-8,9); a.set_ylim(-0.5,10)
plt.savefig(out,dpi=45,bbox_inches='tight')
