import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
# z-sections: source coloured by ownership colour, cage (L0) green, L1 red, L2 orange. Blender frame.
AX=int(__import__("os").environ.get("AX","2")); O=[i for i in range(3) if i!=AX]
zs=[float(v) for v in sys.argv[1].split(",")]; box=[float(v) for v in sys.argv[2].split(',')]; tag=sys.argv[3]; out=sys.argv[4]
w=np.load('/home/claude/stc/rp1/weld.npz'); V=w['V'].astype(float); F=w['F']; col=np.load(sys.argv[5]) if len(sys.argv)>5 else np.ones(len(V),int)
cc={1:'k',2:'b',3:'m',4:'c',5:'y'}
def segs(V,F,c):
    m=(V[:,O[0]]>box[0]-3)&(V[:,O[0]]<box[1]+3)&(V[:,O[1]]>box[2]-3)&(V[:,O[1]]<box[3]+3)&(abs(V[:,AX]-c)<6); F=F[m[F].all(1)]
    d=V[:,AX]-c; s=np.sign(d[F]); F=F[(s.min(1)<0)&(s.max(1)>0)]; out=[]
    for t in F:
        pts=[]
        for i,j in ((0,1),(1,2),(2,0)):
            if d[t[i]]*d[t[j]]<0: u=d[t[i]]/(d[t[i]]-d[t[j]]); pts.append(V[t[i]]+(V[t[j]]-V[t[i]])*u)
        if len(pts)==2: out.append((np.array(pts),t))
    return out
def tri(Q):
    Q=np.asarray(Q); T=[]
    for q in Q:
        q=q[q>=0]
        for k in range(1,len(q)-1): T.append([q[0],q[k],q[k+1]])
    return np.array(T)
meshes=[]
for k,cl in ((0,'g'),(1,'r'),(2,'orange')):
    try:
        P=np.load('sim_%s_L%d.npz'%(tag,k)); meshes.append((P['V']*np.array([1,-1,1]),P['F'],cl))
    except Exception as e: pass
fig,ax=plt.subplots(1,len(zs),figsize=(7*len(zs),7))
for a,c in zip(np.atleast_1d(ax),zs):
    for p,t in segs(V,F,c): a.plot(p[:,O[0]],p[:,O[1]],c=cc[int(np.bincount(col[t]).argmax())],lw=0.8)
    for PV,PF,cl in meshes:
        for p,t in segs(PV,PF,c): a.plot(p[:,O[0]],p[:,O[1]],c=cl,lw=0.9)
    a.set_xlim(box[0],box[1]); a.set_ylim(box[2],box[3]); a.set_aspect('equal'); a.set_title('ax%d=%.1f'%(AX,c)); a.grid(alpha=.3)
plt.savefig(out,dpi=60,bbox_inches='tight')
