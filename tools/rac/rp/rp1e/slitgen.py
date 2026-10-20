# slitgen.py IN.npz SPEC.json OUT.npz : replace the star of given cage vertices by an explicit slit band
# (lipA / wallA / tip / wallB / lipB rows over C columns) traced from the source in planes normal to the slit line.
# SPEC: {"remove":[vids], "line":[[x,y,z],...] (approximate floor polyline), "out":[ox,oy,oz] (floor -> mouth),
#        "cols":C, "start":d (trace start distance along out from the floor guess), "wallfrac":[0.5], "col":null}
import sys, json, numpy as np
from collections import defaultdict
from scipy.spatial import cKDTree
sys.path.insert(0,'/home/claude/stc/rp1e')
from planeslice import plane_loops
from cleftfloor import trace, ray
from orient import orient_patch, check
inp,specp,out=sys.argv[1:4]; S=json.load(open(specp))
z=np.load(inp); V=z['V'].astype(float); F=[[int(x) for x in f if x>=0] for f in z['F']]; col=np.load(inp.replace('.npz','_col.npy'))
SRC=np.load('/home/claude/stc/rp1/weld.npz')['V'].astype(float); scol=np.load(S.get('srccolfile','/home/claude/stc/rp1e/col_r2.npy')); kS=cKDTree(SRC)
rem=set(S.get('remove',[])); patch=[k for k,f in enumerate(F) if any(set(f)==set(q) for q in S['facev'])] if 'facev' in S else S['faces'] if 'faces' in S else [k for k,f in enumerate(F) if set(f)&rem]
de=defaultdict(int)
for k in patch:
    f=F[k]
    for i in range(len(f)): de[(f[i],f[(i+1)%len(f)])]+=1
bd=[(a,b) for (a,b) in de if (b,a) not in de]; nxt={a:b for a,b in bd}
B=[bd[0][0]]
while nxt[B[-1]]!=B[0]: B.append(nxt[B[-1]])
assert len(B)==len(bd),'patch boundary not one loop'
Lp=np.array(S['line'],float); seg=np.linalg.norm(np.diff(Lp,axis=0),axis=1); s=np.r_[0,np.cumsum(seg)]
C=S['cols']; o=np.array(S['out'],float); o/=np.linalg.norm(o)
NV=[list(p) for p in V]; NC=list(col)
def add(p,c=None):
    if c is None: c=S.get('col') if S.get('col') is not None else int(scol[kS.query(p)[1]])
    NV.append(list(np.asarray(p,float))); NC.append(int(c)); return len(NV)-1
rows=[]   # per column: [lipA, wallA..., tip, ...wallB, lipB]
WF=S.get('wallfrac',[0.5])
for j in range(C):
    u=(j+0.5)/C*s[-1] if S.get('centred',True) else j/(C-1)*s[-1]
    k=int(np.clip(np.searchsorted(s,u),1,len(s)-1)); al=(u-s[k-1])/max(seg[k-1],1e-9); f0=Lp[k-1]+(Lp[k]-Lp[k-1])*al
    t=(Lp[k]-Lp[k-1])/max(seg[k-1],1e-9)
    e2=-(o-(o@t)*t); e2/=np.linalg.norm(e2); e1=np.cross(t,e2)
    L=[P for P,cl in plane_loops(f0,t) if cl and np.linalg.norm(P-f0,axis=1).min()<S.get('rad',4.0)]
    L2=[np.c_[(P-f0)@e1,(P-f0)@e2] for P in L]
    st=np.array([S.get('startx',0.0),-S.get('start',0.8)])
    segs=[(l[q],l[(q+1)%len(l)]) for l in L2 for q in range(len(l))]
    if S.get('fin'):
        # fin (thin positive ridge): e2 points along the fin (base -> tip); tip = highest loop point near the centreline
        A=np.vstack(L2); win=S.get('win',0.4); A=A[(np.abs(A[:,0])<win)&(np.abs(A[:,1])<S.get('finrad',1.0))]; assert len(A),('fin: no loop near column',j)
        fl=A[np.argmax(A[:,1])]; mouth=np.array([fl[0],fl[1]-S.get('findepth',0.4)]); depth=fl[1]-mouth[1]
    else:
        pth=trace(0.0,tuple(st),(0,1),loops2d=L2)
        assert pth and len(pth)>=3,('slit trace failed at column',j,f0)
        fl=pth[-1][0]; mouth=pth[0][0]; depth=fl[1]-mouth[1]
    to3=lambda q: f0+e1*q[0]+e2*q[1]
    def walls(q):
        lft=ray(segs,q,np.array([-1.0,0])); rgt=ray(segs,q,np.array([1.0,0]))
        lft=min(lft,S.get('wallmax',0.6)); rgt=min(rgt,S.get('wallmax',0.6))
        if S.get('fin'):
            pd=S.get('finpad',0.0); return to3(q+np.array([-lft-pd,0])), to3(q+np.array([rgt+pd,0]))
        return to3(q+np.array([-lft*0.95,0])), to3(q+np.array([rgt*0.95,0]))
    lipA,lipB=walls(mouth)
    wa=[];wb=[]
    for w in WF:
        q=np.array([fl[0],mouth[1]+w*depth]); a_,b_=walls(q); wa.append(a_); wb.append(b_)
    tip=to3(fl+np.array([0,S.get('overshoot',S.get('finpad',0.0) if S.get('fin') else 0.0)]))
    rows.append([add(lipA)]+[add(p) for p in wa]+[add(tip)]+[add(p) for p in wb[::-1]]+[add(lipB)])
R=len(rows[0])
G=[f for k,f in enumerate(F) if k not in set(patch)]; Fn=[]
for j in range(C-1):
    a,b=rows[j],rows[j+1]
    for i in range(R-1): Fn.append([a[i],a[i+1],b[i+1],b[i]])
# band boundary loop: lipA row (cols 0..C-1), end column C-1 interior..., lipB row reversed, end column 0 reversed
loop=[rows[j][0] for j in range(C)]+[rows[C-1][i] for i in range(1,R-1)]+[rows[j][R-1] for j in range(C-1,-1,-1)]+[rows[0][i] for i in range(R-2,0,-1)]
cen=np.mean([NV[v] for v in loop],axis=0)
nrm=np.cross(np.array(NV[loop[1]])-cen,np.array(NV[loop[len(loop)//4]])-cen); nrm/=np.linalg.norm(nrm)
ux=np.array(NV[loop[0]])-cen; ux-=(ux@nrm)*nrm; ux/=np.linalg.norm(ux); uy=np.cross(nrm,ux)
ang=lambda p:np.arctan2((np.asarray(p)-cen)@uy,(np.asarray(p)-cen)@ux)
def orient(l):
    t=np.unwrap([ang(NV[v]) for v in l+l[:1]]); return l if t[-1]>t[0] else l[::-1]
Lo=orient(loop); Bo=orient(B)
for ap in S.get('apron',[]):
    newl=[]
    for v in Lo:
        p=np.array(NV[v]); q=p-cen; q-=(q@nrm)*nrm; q/=np.linalg.norm(q)+1e-12; t_=p+q*ap
        newl.append(add(SRC[kS.query(t_)[1]] if S.get('apsnap',True) else t_))
    n_=len(Lo)
    for i in range(n_): Fn.append([Lo[i],Lo[(i+1)%n_],newl[(i+1)%n_],newl[i]])
    Lo=newl
k0=int(np.argmin([np.linalg.norm(np.array(NV[v])-np.array(NV[Lo[0]])) for v in Bo])); Bo=Bo[k0:]+Bo[:k0]
def frac_arc(l):
    P=np.array([NV[v] for v in l]); Q=np.vstack([P,P[:1]]); ss=np.r_[0,np.cumsum(np.linalg.norm(np.diff(Q,axis=0),axis=1))]; return ss[:-1]/ss[-1]
def cells(small,big,fs,fb):
    ms=len(small); n=len(big); dd=lambda x,y: abs(((x-y+0.5)%1.0)-0.5)
    own=[int(np.argmin([dd(fs[i],fb[j]) for i in range(ms)])) for j in range(n)]; Fs=[]
    for j in range(n):
        j2=(j+1)%n; i1,i2=own[j],own[j2]
        if i1==i2: Fs.append([small[i1],big[j],big[j2]])
        else:
            k=i1; steps=(i2-i1)%ms
            if steps==1: Fs.append([small[i1],big[j],big[j2],small[i2]])
            else:
                Fs.append([small[k],big[j],big[j2]])
                while k!=i2: Fs.append([small[k],big[j2],small[(k+1)%ms]]); k=(k+1)%ms
    return Fs
def greedy(A,Bl):
    # shortest-diagonal stitching between closed loops A and Bl (same orientation, A[0]~Bl[0]); quads where two tris pair up
    P=lambda v: np.array(NV[v]); i=j=0; na,nb=len(A),len(Bl); T=[]
    while i<na or j<nb:
        a0,b0=A[i%na],Bl[j%nb]
        if i>=na: T.append([a0,b0,Bl[(j+1)%nb]]); j+=1; continue
        if j>=nb: T.append([a0,b0,A[(i+1)%na]]); i+=1; continue
        da=np.linalg.norm(P(A[(i+1)%na])-P(b0)); db=np.linalg.norm(P(Bl[(j+1)%nb])-P(a0))
        if da<db: T.append([a0,b0,A[(i+1)%na]]); i+=1
        else: T.append([a0,b0,Bl[(j+1)%nb]]); j+=1
    out=[];k=0
    while k<len(T):
        if S.get('pairq',True) and k+1<len(T):
            t1,t2=T[k],T[k+1]
            # t1 advanced one side, t2 the other -> quad
            if t1[2] in A and t2[2] in Bl and t2[0]==t1[2] and t2[1]==t1[1]: out.append([t1[0],t1[1],t2[2],t1[2]]); k+=2; continue
            if t1[2] in Bl and t2[2] in A and t2[1]==t1[2] and t2[0]==t1[0]: out.append([t1[0],t1[1],t1[2],t2[2]]); k+=2; continue
        out.append(T[k]); k+=1
    return out
def stitch2d(A,Bl):
    # project onto the mean patch normal plane; both loops CCW; greedy shortest diagonal with orientation validity
    fn=np.zeros(3)
    for k in patch:
        f=F[k]; P_=V[f]; fn+=np.cross(P_[1]-P_[0],P_[2]-P_[0])
    fn/=np.linalg.norm(fn); a1=np.cross(fn,[1,0,0]); a1=a1 if np.linalg.norm(a1)>0.1 else np.cross(fn,[0,1,0]); a1/=np.linalg.norm(a1); a2=np.cross(fn,a1)
    Q=lambda v: np.array([np.array(NV[v])@a1,np.array(NV[v])@a2])
    def ccw(l):
        P_=np.array([Q(v) for v in l]); ar=0.5*np.sum(P_[:,0]*np.roll(P_[:,1],-1)-np.roll(P_[:,0],-1)*P_[:,1]); return l if ar>0 else l[::-1]
    A=ccw(list(A)); Bl=ccw(list(Bl))
    k0=int(np.argmin([np.linalg.norm(Q(v)-Q(A[0])) for v in Bl])); Bl=Bl[k0:]+Bl[:k0]
    cr2=lambda o,a,b: (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    if S.get('stitch')=='3dn':
        import igl as _igl
        _SF=np.load('/home/claude/stc/rp1/weld.npz')['F'].astype(np.int64); _N=_igl.per_vertex_normals(SRC,_SF)
        # sign so that the global-plane convention matches: sgn = sign(fn . mean source normal of the patch)
        _sg=np.sign(fn@_N[kS.query(np.mean([NV[v] for v in A],axis=0))[1]])
        def cr(o,a,b):
            O,Aa,Bb=[np.array(NV[v]) for v in (o,a,b)]; nn=_N[kS.query((O+Aa+Bb)/3)[1]]*_sg
            return np.cross(Aa-O,Bb-O)@nn
        Qv=lambda v: v
    else:
        cr=cr2; Qv=Q
    i=j=0; na,nb=len(A),len(Bl); T=[]
    while i<na or j<nb:
        a0,b0=A[i%na],Bl[j%nb]; a1_,b1_=A[(i+1)%na],Bl[(j+1)%nb]
        # inner loop A ccw, outer Bl ccw: triangle (a0,b0,b1) must be cw? use consistent: tri (b0,b1,a0) ccw ; (a0,b0... )
        okA=i<na and cr(Qv(a0),Qv(b0),Qv(a1_))<0   # advance on A: tri a0,b0,a1
        okB=j<nb and cr(Qv(a0),Qv(b0),Qv(b1_))<0   # advance on B: tri a0,b0,b1
        dA=np.linalg.norm(Q(a1_)-Q(b0)) if okA else 1e9; dB=np.linalg.norm(Q(b1_)-Q(a0)) if okB else 1e9
        if not okA and not okB:
            if i>=na: okB=True
            elif j>=nb: okA=True
            else: (okA:=True) if dA<=dB else None
            dA=np.linalg.norm(Q(a1_)-Q(b0)) if (i<na) else 1e9; dB=np.linalg.norm(Q(b1_)-Q(a0)) if (j<nb) else 1e9
        if dA<=dB and i<na: T.append([a0,b0,a1_]); i+=1
        else: T.append([a0,b0,b1_]); j+=1
    out=[];k=0
    while k<len(T):
        if k+1<len(T):
            t1,t2=T[k],T[k+1]
            if t2[0]==t1[2] and t2[1]==t1[1] and t1[2] in A and t2[2] in Bl: out.append([t1[0],t1[1],t2[2],t1[2]]); k+=2; continue
            if t2[1]==t1[2] and t2[0]==t1[0] and t1[2] in Bl and t2[2] in A: out.append([t1[0],t1[1],t1[2],t2[2]]); k+=2; continue
        out.append(T[k]); k+=1
    return out
if S.get('stitch') in ('2d','3dn'): Fn+=stitch2d(Lo,Bo)
elif len(Bo)<=len(Lo): Fn+=cells(Bo,Lo,frac_arc(Bo),frac_arc(Lo))
else: Fn+=cells(Lo,Bo,frac_arc(Lo),frac_arc(Bo))
Fn=orient_patch(G,Fn); G+=Fn; d1,b1=check(G)
if d1 or b1: raise SystemExit('topology dup %d bnd %d'%(d1,b1))
used=sorted(set(i for f in G for i in f)); remap={o_:n for n,o_ in enumerate(used)}
V2=np.array([NV[i] for i in used]); G2=[[remap[i] for i in f] for f in G]; C2=np.array([NC[i] for i in used])
Fa=np.full((len(G2),4),-1)
for k,f in enumerate(G2): Fa[k,:len(f)]=f
np.savez_compressed(out,V=V2,F=Fa); np.save(out.replace('.npz','_col.npy'),C2); np.save(out.replace('.npz','_remap.npy'),np.array([remap.get(i,-1) for i in range(len(V))]))
json.dump({'rows':[[remap[v] for v in r] for r in rows],'B':[remap[v] for v in B]},open(out.replace('.npz','_meta.json'),'w'))
print('V',len(V2),'F',len(G2),'B',len(B),'band',C,'x',R)
