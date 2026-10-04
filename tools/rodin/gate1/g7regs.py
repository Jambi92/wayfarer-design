# Gate 7 CONVERGENCE (structural scale hierarchy) on top of the CLOSURE per-vertex regional scale architecture on the frozen Gate 6 base (upsampled).
# Changes vs g7reg.py (diagnostic): graded family transitions (long-range parameter blending), facial hierarchy
# (finer/subtler expressive units, planar roof/rostral plates, curvature-protected cranial plane edges, smooth recessed tympanic area).
import numpy as np, igl, sys
import g7geo as G
import hand
SRC=sys.argv[1] if len(sys.argv)>1 else 'g7up.npz'; OUTR=sys.argv[2] if len(sys.argv)>2 else 'g7reg.npz'
z=np.load(SRC); V=z['V'].astype(np.float64); F=z['F'].astype(np.int64)
N=igl.per_vertex_normals(V,F); x,f,u=V.T; ax=np.abs(x); n=len(V)
FAM=np.full(n,1,np.int8)          # 1 structural, 2 transitional, 3 expressive, 4 ventral, 5 contact (palm/sole), 6 claw keratin, 7 eye
R=np.full(n,1.1); Hh=np.full(n,0.10); EL=np.full(n,1.25); T=np.zeros((n,3)); T[:,2]=-1.0     # spacing cm, relief cm, elongation along flow, flow dir
PL=np.zeros(n)
def setv(m,fam,r,h,e):
    FAM[m]=fam; R[m]=r; Hh[m]=h; EL[m]=e
sg_of=np.sign(x)+(x==0)
# ---------------- trunk / neck / pelvis default by orientation
nF,nU,nX=N[:,1],N[:,2],N[:,0]
dorsal=nF<-0.35; ventral=nF>0.45
setv(np.ones(n,bool),1,1.15,0.11,1.3)                                   # lateral trunk: selected structural
setv(dorsal,1,1.5,0.14,1.35)                                            # dorsal trunk: largest structural units
setv(ventral&(u>100)&(u<168)&(ax<15),4,1.75,0.07,0.36)                  # ventral field: broad transverse units (not continuous scutes)
setv((u>94)&(u<108)&~dorsal&(ax<18),2,0.6,0.06,1.0)                     # lower trunk flexion
setv((u>150)&(u<170)&~dorsal&~ventral,2,0.6,0.06,1.0)                   # neck flexion (lateral)
setv((u>150)&(u<172)&dorsal,1,1.0,0.10,1.3)                             # upper posterior neck: structural
setv((u>150)&(u<172)&ventral&(ax<10),4,1.2,0.06,0.4)                  # throat / anterior neck ventral field
# ---------------- arms
for sg,S in G.ARM.items():
    Sx,Ex,Wx=(np.array(S[k]) for k in ('S','E','W')); m=(sg_of==sg)
    d1,t1=G.seg_dist(V,Sx,Ex); d2,t2=G.seg_dist(V,Ex,Wx)
    arm=m&((d1<10)|(d2<9))&(ax>17)
    lat=np.einsum('ij,j->i',N,np.array([sg,0,0.0]))
    dirs=np.where((d1<d2)[:,None],(Ex-Sx)/np.linalg.norm(Ex-Sx),(Wx-Ex)/np.linalg.norm(Wx-Ex)); T[arm]=dirs[arm]
    setv(arm&(lat>-0.2),1,0.9,0.08,1.4); setv(arm&(lat<=-0.2),2,0.55,0.05,1.2)             # lateral/dorsal = structural, medial = transitional

    setv(m&(np.linalg.norm(V-Ex,axis=1)<6.0)&(ax>17),2,0.5,0.05,1.0)                         # elbow
    setv(m&(np.linalg.norm(V-Wx,axis=1)<4.0),2,0.4,0.04,1.0)                                  # wrist
    setv(m&((d1<12)&(t1<0.12))&(u<150)&(u>132)&(ax>14)&(ax<24)&(nF>-0.6),2,0.55,0.05,1.0)     # axilla / shoulder transition
import hand  # noqa
for sg,S in G.ARM.items():
    Wx,Ex=np.array(S['W']),np.array(S['E']); a,b,c=hand.frame(Wx,Ex,sg); Q=V-Wx; la=Q@a
    hm=(sg_of==sg)&(la>0.5)&(np.linalg.norm(Q,axis=1)<26)&(ax>24)
    pal=np.einsum('ij,j->i',N,c); T[hm]=a
    setv(hm&(pal<=0.15),1,0.45,0.05,1.3)                                  # dorsal hand: small structural scales
    setv(hm&(pal>0.15),5,0.28,0.025,1.0)                                  # palmar contact field
# ---------------- legs / feet
for sg,S in G.LEG.items():
    Hx,Kx,Ax=(np.array(S[k]) for k in ('H','K','A')); m=(sg_of==sg)
    d1,t1=G.seg_dist(V,Hx,Kx); d2,t2=G.seg_dist(V,Kx,Ax)
    leg=m&((d1<13)|(d2<10))&(u<90)&(u>12)
    dirs=np.where((d1<d2)[:,None],(Kx-Hx)/np.linalg.norm(Kx-Hx),(Ax-Kx)/np.linalg.norm(Ax-Kx)); T[leg]=dirs[leg]
    lat=np.einsum('ij,j->i',N,np.array([sg,0,0.0])); front=nF
    setv(leg&(u<84),1,1.0,0.09,1.35); setv(leg&(u<84)&(lat<-0.3),2,0.6,0.05,1.2)          # thigh/leg lateral structural, medial transitional
    setv(leg&(d2<10)&(front>0.3)&(u<58)&(u>16),1,1.2,0.11,1.5)                            # shin: structural
    setv(m&(np.linalg.norm(V-Kx,axis=1)<8.0),2,0.55,0.05,1.0)                             # knee
    setv(m&(np.linalg.norm(V-Ax,axis=1)<7.0)&(u>4),2,0.45,0.045,1.0)                      # ankle
    ft=m&(u<12)&(np.linalg.norm(V[:,:2]-Ax[:2],axis=1)<34)
    a=np.radians(S['toe'])*sg; fwd=np.array([np.sin(a),np.cos(a),0.0]); T[ft]=fwd
    setv(ft&(nU>-0.35),1,0.55,0.05,1.3)                                                   # dorsal foot: structural
    setv(ft&((nU<=-0.35)|(u<0.9)),5,0.3,0.025,1.0)                                        # plantar contact field
# ---------------- pelvis / inguinal / tail root / tail
setv((u>70)&(u<96)&(ax<16)&(f>-14)&(nU<0.2)&~dorsal,2,0.55,0.05,1.0)                     # pelvis floor / inguinal flexion
tail=(f<-26)&(u>40)
tdir=np.zeros((n,3)); tdir[:,1]=-1.0; tdir[:,2]=-0.15; tdir/=np.linalg.norm(tdir,axis=1,keepdims=True); T[tail]=tdir[tail]
setv(tail&(nU>-0.25),1,1.4,0.13,1.45)                                                     # dorsal / lateral tail: structural
setv(tail&(nU<=-0.25),4,1.6,0.07,0.38)                                                    # underside of tail: ventral field
setv((f<-14)&(f>-40)&(u>70)&(u<104)&(ax>4)&(ax<17),2,0.7,0.06,1.1)                       # tail root / caudofemoral articulation band
# ---------------- head
eyes,er,yaw=G.eyes_world()
hd=(u>170)&(ax<12)&(f>-14)&((f>-5)|(u>177))
T[hd]=np.array([0,-1.0,0])                                                                # head scales flow rostral -> caudal
setv(hd,3,0.36,0.022,1.0)                                                                 # default face: fine expressive (finer, subtler)
setv(hd&(u>180)&(nU>0.35),1,0.85,0.05,1.25)                                                 # dorsal cranium / roof: structural
setv(hd&(f<0)&(nF<-0.2)&(u>176),1,0.85,0.055,1.25)                                          # posterolateral cranium
setv(hd&(f>12)&(nU>0.5),1,0.55,0.03,1.1)                                                  # rostral dorsum: small structural
for c in eyes:
    de=np.linalg.norm(V-c,axis=1)
    setv(hd&(de<er*2.1),3,0.26,0.018,1.0)                                                  # periorbital fine field (lids)
    FAM[de<er*1.03]=7                                                                     # eye
PL[hd&(FAM==1)]=1.0                                                                       # cranial roof / posterolateral / rostral dorsum: planar plates
TYM=np.zeros(n)                                                                           # recessed tympanic (auricular) area: smooth, no rim
for sgn in (-1,1):
    c=np.array([6.11*sgn,-1.38,181.82]); dt=np.linalg.norm(V-c,axis=1); TYM=np.maximum(TYM,np.clip(1-dt/1.0,0,1))
# ---------------- claws (keratin, no scales)
segs,pads=G.world_claws_pads()
for a,b,ra,rb,kind in segs:
    dd,tt=G.seg_dist(V,a,b); rr=ra+(rb-ra)*tt
    FAM[dd<rr+0.18]=6
# keratin display structures (variant heads): smooth keratin, no scales
import os
if os.environ.get('DISPLAY_VARIANT'):
    import wf_saurin_head65 as H65, wf_saurin_head64 as H64
    q=V-G.AT; q=(q-H64.PIV)/H64.S+H64.PIV
    kk=np.where((q[:,2]>2)&(np.abs(q[:,0])<9))[0]
    dd=H65._D(q[kk,0],q[kk,1],q[kk,2])*H64.S; sk=H65.H.head_sdf(q[kk,0],q[kk,1],q[kk,2],H65.RINGS,-59.0)*H64.S
    FAM[kk[(dd<0.35)&(sk>0.05)]]=6
# coherent regions: smooth the family one-hot and the size/relief fields over the surface (no speckled thresholds)
from scipy.sparse import coo_matrix, diags
E_=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); A=coo_matrix((np.ones(len(E_)),(E_[:,0],E_[:,1])),shape=(n,n)).tocsr(); A=((A+A.T)>0).astype(np.float32)
L=diags(1/np.asarray(A.sum(1)).ravel())@A
fixed=(FAM==6)|(FAM==7)
OH=np.zeros((n,6),np.float32); OH[np.arange(n),np.clip(FAM-1,0,5)]=1
for _ in range(40): OH=L@OH
nf=OH[:,:5].argmax(1)+1; FAM=np.where(fixed,FAM,nf).astype(np.int8)
# ---------------- convergence pass: second, larger STRUCTURAL scale/scute order over selected protective/load-bearing fields
# (only family-1 structural fields; articulation/expressive/contact fields keep their fine units; gradients are smoothed below)
from scipy.spatial import cKDTree as _KD
_C=np.load('/tmp/claude-0/rodin/g8/axis.npy'); _ci=_KD(_C).query(V)[1]; sax=_ci*0.5                 # arc length from the tail tip
def _ss(a,b,x): t=np.clip((x-a)/(b-a),0,1); return t*t*(3-2*t)
st1=(FAM==1)
SR=np.zeros(n); SW=np.zeros(n); SH=np.zeros(n); SPL=np.zeros(n)
def scute(m,r,h,pl):
    global SR,SW,SH,SPL
    m=m&st1; SW=np.where(m,1.0,SW); SR=np.where(m,r,SR); SH=np.where(m,h,SH); SPL=np.where(m,pl,SPL)
# dorsal / posterolateral cranium + brow-temporal planes: plates following the brow -> temporal -> jugal flow
scute(hd&(u>179.5)&(nU>0.25)&(np.abs(f-3)<14),1.8,0.09,1.0)
scute(hd&(f<2)&(nF<-0.15)&(u>176),1.9,0.09,1.0)
# nape and upper dorsal thorax / shoulder transition
scute((u>163)&(u<177)&(nF<-0.35)&(ax<9),2.5,0.18,0.7)
scute((u>132)&(u<163)&(nF<-0.35)&(ax<19),3.2,0.22,0.6)
# selected dorsal forearm and dorsal shin
for sg,S_ in G.ARM.items():
    Ex,Wx=np.array(S_['E']),np.array(S_['W']); d2,t2=G.seg_dist(V,Ex,Wx); lat=N[:,0]*sg
    scute((sg_of==sg)&(d2<7)&(t2>0.15)&(t2<0.85)&(lat>0.25),1.9,0.14,0.5)
for sg,L_ in G.LEG.items():
    Kx,Ax=np.array(L_['K']),np.array(L_['A']); d2,t2=G.seg_dist(V,Kx,Ax)
    scute((sg_of==sg)&(d2<9)&(t2>0.12)&(t2<0.85)&(nF>0.35),2.4,0.16,0.55)
# dorsal / dorsolateral tail with a root -> tip size gradient (3.0 cm at the root, ~1.0 cm distally), lateral tail root
tr=(f<-24)&(u>40)&(nU>-0.25)
rt=1.0+2.6*_ss(18,96,sax); ht=0.07+0.17*_ss(18,96,sax)
scute(tr,rt,ht,0.55)
for k in ('SR','SW','SH','SPL'): pass
w=SW*np.clip(1.0,0,1)
R=np.where(w>0,SR,R); Hh=np.where(w>0,SH,Hh); PL=np.maximum(PL,SPL*w)
# graded transitions: medium-range blend on head/hands/feet (protect small structures), long-range blend elsewhere
IMB=((FAM==1)|(FAM==2)).astype(float)
X=np.stack([R,Hh,EL,PL,IMB],1).astype(np.float32)
hm_all=np.zeros(n,bool)
for sg,S in G.ARM.items():
    Wx,Ex=np.array(S['W']),np.array(S['E']); a,b,c=hand.frame(Wx,Ex,sg); hm_all|=(sg_of==sg)&(((V-Wx)@a)>1.5)&(np.linalg.norm(V-Wx,axis=1)<26)&(ax>24)
WP=(hd|hm_all|(u<6)).astype(np.float32)
for i in range(500):
    X=L@X
    if i==99: X100=X.copy()
    if i==19:
        for _ in range(20): WP=L@WP
WP=np.clip(WP*1.4,0,1)[:,None]
X=X100*WP+X*(1-WP); R,Hh,EL,PL,IMB=(X[:,k].astype(np.float64) for k in range(5))
# cranial plane protection: attenuate relief where the skull surface bends sharply (brow shelf, jugal, hinge edges)
lap=np.abs(np.einsum('ij,ij->i',(L@V)-V,N)); k=lap.copy()
for _ in range(15): k=L@k
k0=np.percentile(k[hd],70) if hd.any() else 1.0
ATT=np.clip(1/(1+(k/k0)**2),0.35,1.0); hw=hd.astype(float)
for _ in range(30): hw=L@hw
ATT=1-(1-ATT)*hw
ATT*=1-0.85*TYM                                                                            # tympanic area nearly smooth
# flow direction projected onto the tangent plane
T=T-N*np.einsum('ij,ij->i',T,N)[:,None]; nt=np.linalg.norm(T,axis=1); bad=nt<1e-3
alt=np.cross(N,np.array([1.0,0,0])); T[bad]=alt[bad]; T/=np.linalg.norm(T,axis=1,keepdims=True)+1e-12
np.savez(OUTR,FAM=FAM,PL=PL.astype(np.float32),IMB=IMB.astype(np.float32),ATT=ATT.astype(np.float32),TYM=TYM.astype(np.float32),R=R.astype(np.float32),H=Hh.astype(np.float32),EL=EL.astype(np.float32),T=T.astype(np.float32),N=N.astype(np.float32))
print({int(k):int((FAM==k).sum()) for k in np.unique(FAM)})
