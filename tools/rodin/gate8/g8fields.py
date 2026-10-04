# Gate 8: per-vertex anatomical fields for pigmentation on any Gate 7 mesh (full body or head crop), world cm.
# argv: base_mesh(V,F) region(g7regc-type) surf(V,F,disp,edge) out
import sys, os, numpy as np
sys.path.insert(0,'/tmp/claude-0/rodin/g1'); sys.path.insert(0,'/tmp/claude-0/rodin/g8')
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix, diags
import g7geo as G, hand, seedpd
B,RG,SF,OUT=sys.argv[1:5]
z=np.load(B); V=z['V'].astype(float); F=z['F'].astype(np.int64); n=len(V)
r=np.load(RG); FAM=r['FAM']; R=r['R'].astype(float); EL=r['EL'].astype(float); Tf=r['T'].astype(float); N=r['N'].astype(float)
sfz=np.load(SF); edge=sfz['edge'].astype(np.float32)
x,f,u=V.T; ax=np.abs(x); sg=np.where(x>=0,1,-1)
# ---- centreline coordinates
C=np.load('/tmp/claude-0/rodin/g8/axis.npy'); tr=cKDTree(C); _,ci=tr.query(V); ci=np.clip(ci,1,len(C)-2)
tang=C[ci+1]-C[ci-1]; tang/=np.linalg.norm(tang,axis=1,keepdims=True)
S_ax=ci*0.5; rv=V-C[ci]; rv-=tang*np.einsum('ij,ij->i',rv,tang)[:,None]
dors=np.cross(np.array([1.0,0,0]),tang); dors/=np.linalg.norm(dors,axis=1,keepdims=True)
TH=np.arctan2(rv[:,0],np.einsum('ij,ij->i',rv,dors))           # 0 dorsal, +-pi ventral, + = right(+x)
RAD=np.linalg.norm(rv,axis=1)
# girth along the axis (median radius of near-axial verts per station)
gb=np.full(len(C),np.nan)
for k in range(0,len(C)):
    pass
order=np.argsort(ci); cs=ci[order]; rs=RAD[order]; bounds=np.searchsorted(cs,np.arange(len(C)+1))
for k in range(len(C)):
    a,b=bounds[k],bounds[k+1]
    if b-a>20: gb[k]=np.median(rs[a:b])
ok=~np.isnan(gb); gb=np.interp(np.arange(len(C)),np.where(ok)[0],gb[ok])
for _ in range(30): gb[1:-1]=0.25*gb[:-2]+0.5*gb[1:-1]+0.25*gb[2:]
GIR=gb[ci]
# ---- limbs: chain coordinate t (cm from limb root) and limb angle (0 = lateral/extensor side)
LW=np.zeros(n); LT=np.zeros(n); LTN=np.zeros(n); LTH=np.zeros(n); LR=np.ones(n); LID=np.zeros(n,np.int8)
def chain(pts,mask,lat,lid,maxd):
    pts=[np.asarray(p,float) for p in pts]; best=np.full(n,1e9); tt=np.zeros(n); axd=np.zeros((n,3)); acc=0.0; L=[]
    for a,b in zip(pts[:-1],pts[1:]):
        d,t=G.seg_dist(V,a,b); m=d<best; best[m]=d[m]; tt[m]=acc+t[m]*np.linalg.norm(b-a); axd[m]=(b-a)/np.linalg.norm(b-a); acc+=np.linalg.norm(b-a)
    sel=mask&(best<maxd)
    rr=V-0; # angle around limb axis, reference = lateral
    ref=lat-axd*np.einsum('ij,j->i',axd,lat)[:,None]; ref/=np.linalg.norm(ref,axis=1,keepdims=True)+1e-9
    cent=np.zeros((n,3))
    q=V-pts[0]; q=q-axd*np.einsum('ij,ij->i',q,axd)[:,None]   # approx radial (good enough for angle)
    # radial vector from the nearest segment point
    rad=np.zeros((n,3)); best2=np.full(n,1e9)
    for a,b in zip(pts[:-1],pts[1:]):
        d,t=G.seg_dist(V,a,b); p=a+t[:,None]*(b-a); m=d<best2; best2[m]=d[m]; rad[m]=(V-p)[m]
    side=np.cross(axd,ref)
    th=np.arctan2(np.einsum('ij,ij->i',rad,side),np.einsum('ij,ij->i',rad,ref))
    LT[sel]=tt[sel]; LTN[sel]=tt[sel]/acc; LTH[sel]=th[sel]; LR[sel]=np.maximum(best2[sel],0.5); LID[sel]=lid; LW[sel]=1.0
for s_,A_ in G.ARM.items():
    S0,E0,W0=(np.array(A_[k]) for k in ('S','E','W')); a,b,c=hand.frame(W0,E0,s_); tip=W0+a*19.0
    chain([S0,E0,W0,tip],(sg==s_)&(ax>16.5)&(u<150),np.array([s_,0,0.0]),1 if s_>0 else 2,11)
for s_,L_ in G.LEG.items():
    H0,K0,A0=(np.array(L_[k]) for k in ('H','K','A')); ang=np.radians(L_['toe'])*s_; tip=np.array([A0[0]+np.sin(ang)*24,A0[1]+np.cos(ang)*24,1.5])
    chain([H0,K0,A0,tip],(sg==s_)&(u<92)&(f>-26),np.array([s_,0,0.0]),3 if s_>0 else 4,14)
# limb blend weight: ramps over ~12 cm from each limb root along the limb axis, then surface-smoothed (300 its), so no
# colour border appears where the limb coordinate system begins (Gate 8 fix; see fixlw.py)
if LW.any():
    def _ss(a,b,x): t=np.clip((x-a)/(b-a),0,1); return t*t*(3-2*t)
    E_=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); A=coo_matrix((np.ones(len(E_)),(E_[:,0],E_[:,1])),shape=(n,n)).tocsr(); A=((A+A.T)>0).astype(np.float32)
    L=diags(1/np.asarray(A.sum(1)).ravel())@A
    w=np.where(LID>0,np.where(LID<=2,_ss(3,15,LT),_ss(2,14,LT)),0.0).astype(np.float32)
    for _ in range(300): w=L@w
    LW=np.clip(w,0,1)
# per-limb girth (median radius along t)
LG=np.ones(n)
for lid in (1,2,3,4):
    m=LID==lid
    if m.sum()<100: continue
    tb=np.round(LT[m]).astype(int); med=np.zeros(tb.max()+1)
    for k in range(len(med)):
        mm=tb==k; med[k]=np.median(LR[m][mm]) if mm.sum()>10 else np.nan
    okk=~np.isnan(med); med=np.interp(np.arange(len(med)),np.where(okk)[0],med[okk])
    for _ in range(10): med[1:-1]=0.25*med[:-2]+0.5*med[1:-1]+0.25*med[2:]
    LG[m]=med[tb]
# ---- scale cells (same seeds as g7surfc: same rng, same field)
scaly=(FAM!=6)&(FAM!=7); rng=np.random.default_rng(7)
Sd=np.load(os.environ['SEEDS']) if os.environ.get('SEEDS') else seedpd.poisson_seeds(V,R,scaly,rng,c=0.50)
SP=V[Sd]; SR=R[Sd]; SE=EL[Sd]; ST=Tf[Sd]; tree=cKDTree(SP); CELL=np.full(n,-1,np.int64)
for i0 in range(0,n,400000):
    sl=slice(i0,min(n,i0+400000)); P=V[sl]; _,nb=tree.query(P,k=12)
    D=P[:,None,:]-SP[nb]; along=np.einsum('ijk,ijk->ij',D,ST[nb]); perp=np.sqrt(np.maximum((D*D).sum(-1)-along**2,0))
    d=np.sqrt((along/SE[nb])**2+perp**2)/SR[nb]; CELL[sl]=np.take_along_axis(nb,d.argmin(1)[:,None],1)[:,0]
CELLV=Sd[CELL]                       # vertex index of each vertex's scale seed
# ---- keratin: distance to the nearest non-keratin vertex (growth axis from the base)
KD=np.zeros(n); ker=FAM==6
if ker.any(): KD[ker],_=cKDTree(V[~ker]).query(V[ker])
np.savez(OUT,S=S_ax.astype(np.float32),TH=TH.astype(np.float32),RAD=RAD.astype(np.float32),GIR=GIR.astype(np.float32),
 LW=LW.astype(np.float32),LT=LT.astype(np.float32),LTN=LTN.astype(np.float32),LTH=LTH.astype(np.float32),LG=LG.astype(np.float32),LID=LID,
 CELLV=CELLV.astype(np.int32),EDGE=edge,FAM=FAM,KD=KD.astype(np.float32),R=R.astype(np.float32),N=N.astype(np.float32))
print('fields ok',n,'cells',len(Sd),'limb verts',int((LID>0).sum()))
