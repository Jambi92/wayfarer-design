import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
# sections of the source by planes y=const, coloured by toe label. usage: ysec.py S y1,y2,.. x0,x1 out
s=sys.argv[1]; ys=[float(v) for v in sys.argv[2].split(',')]; x0,x1=[float(v) for v in sys.argv[3].split(',')]; out=sys.argv[4]
w=np.load('/home/claude/stc/rp1/weld.npz'); V=w['V'].astype(float); F=w['F']
q=np.load('fseg_%s.npz'%s); lab=np.full(len(V),-1); lab[q['used']]=q['lab']
cm={0:'r',1:'g',2:'b',3:'m',4:'c',9:'k',-1:'0.6'}
m=(V[:,0]>x0-1)&(V[:,0]<x1+1)&(V[:,2]<14); Fm=F[m[F].all(1)]
fig,ax=plt.subplots(1,len(ys),figsize=(7*len(ys),5))
for a,y0 in zip(np.atleast_1d(ax),ys):
    d=V[:,1]-y0; T=Fm[(np.sign(d[Fm]).min(1)<0)&(np.sign(d[Fm]).max(1)>0)]
    for t in T:
        pts=[]
        for i,j in ((0,1),(1,2),(2,0)):
            if d[t[i]]*d[t[j]]<0: u=d[t[i]]/(d[t[i]]-d[t[j]]); pts.append(V[t[i]]+(V[t[j]]-V[t[i]])*u)
        if len(pts)==2: p=np.array(pts); a.plot(p[:,0],p[:,2],c=cm[lab[t[0]]],lw=1)
    a.set_aspect('equal'); a.set_xlim(x0,x1); a.set_ylim(-0.5,9); a.grid(True); a.set_title('y=%.1f'%y0)
plt.savefig(out,dpi=50,bbox_inches='tight')
