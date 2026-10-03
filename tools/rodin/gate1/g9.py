# Gate 6: whole-organism integration on the accepted Gate 5 body.
#  - TS6.3 naked skull swapped into the field chain (head seating / Gate 3A blends rebuild around it)
#  - regional low-pass of the CURRENT surface removes procedural grooves, lumps, rims and debris; structure is rebuilt on top
import numpy as np, sys
sys.path.insert(0,'/tmp/claude-0/rb')
import g8
from g1 import ss, smin, smax
import wf_saurin_body8 as B8, wf_saurin_head63 as H63
from g9z import LP, ell_w, away_from_hands, SPath, rss
B8.H=H63
def mix(e,b,w): return e*(1-w)+b*w
def boxfade(X,F,U,box,m=1.2):
    w=np.ones(len(X))
    for i,c in enumerate((X,F,U)): w*=ss(box[2*i]+m,box[2*i]+2.5*m,c)*(1-ss(box[2*i+1]-2.5*m,box[2*i+1]-m,c))
    return w
# ---------------- pelvis / tail root / crotch rebuild
def pelvis_w(X,F,U):
    w=np.maximum(ell_w(X,F,U,(0,-10,88),(21,30,20),0.35),ell_w(X,F,U,(0,-8,68),(17.5,16,14),0.4))*(1-ss(100,108,U))*ss(-44.0,-40.0,F)
    return w
def pelvis_base(X,F,U):
    b=LP("pelvis",X,F,U)+0.15
    # neutral pelvic floor: the low-pass of the existing floor (U ~90) already bridges thighs and tail; no filler volume
    return b
PP=[]
for sg in (-1,1):
    PP+=[SPath(pelvis_base,[(sg*13,-6,100),(sg*8.5,-20,95.5),(sg*4,-32,92)],[5.0,4.6,3.6],[0.9,1.1,0.6],300+sg,edge=0.2),        # iliocaudal
         SPath(pelvis_base,[(sg*5,-31,86),(sg*10,-19,80),(sg*13,-7,72)],[6.5,7.0,4.5],[1.6,2.0,0.8],310+sg,edge=0.15),     # caudofemoral -> femur (broad: fills the tail/thigh crease)
         SPath(pelvis_base,[(sg*3.5,-38,90),(sg*7,-26,88),(sg*11,-14,84),(sg*14,-6,78)],[5.0,5.5,5.0,3.5],[1.0,1.3,1.0,0.4],350+sg,edge=0.15),   # caudofemoral brevis-equivalent, higher fan
         SPath(pelvis_base,[(sg*4,-6,87),(sg*3,-20,83),(sg*2,-33,79)],[2.4,2.2,1.8],[0.30,0.38,0.22],320+sg),             # ventral caudal (ischiocaudal)
         SPath(pelvis_base,[(sg*15,-2,99),(sg*18,2,87),(sg*19,4,75)],[3.4,3.2,2.6],[0.40,0.50,0.25],330+sg)]              # lateral hip stabiliser
PP.append(SPath(pelvis_base,[(-11,-11,97),(0,-16.5,98),(11,-11,97)],[4.0,4.4,4.0],[0.40,0.50,0.40],340,fade=(0.3,0.3)))   # transverse sacral platform
def pelvis_field(X,F,U):
    b=pelvis_base(X,F,U); return b-rss(PP,np.stack([X,F,U],-1))
# ---------------- regional weights for the partial relaxes
def torso_w(X,F,U):
    w=0.65*ss(100,106,U)*(1-ss(148,154,U))*(1-ss(17.0,19.5,np.abs(X)))
    rim=ell_w(X,F,U,(0,8,97),(14,10,7),0.4)                                            # scalloped lower ventral-shield crown
    return np.maximum(w,0.9*rim)
def neck_w(X,F,U): return 0.50*ss(148,152,U)*(1-ss(166,171,U))*(1-ss(13,15,np.abs(X)))
KN={-1:(-17.4,2.8,62.0),1:(15.2,3.0,62.0)}; AN={-1:(-26.4,0.2,9.6),1:(21.6,1.6,9.6)}
# isolated bulges found against a heavy (~3 cm) low-pass of the Gate 5 surface (feet/claws excluded): smooth inward deflation
DEFL=[((16.0,-9.0,66.0),(5.5,5.0,10.0),1.1),      # right posterior thigh/knee ball
      ((-18.3,11.2,59.8),(5.0,3.5,5.5),0.8),((15.6,11.8,60.2),(5.0,3.5,5.5),0.8),   # patellar-like lumps
      ((-25.3,-12.4,48.0),(6.5,5.5,13.0),2.3),((22.2,-11.0,49.0),(6.5,5.5,13.0),1.9),   # calf balls (lengthened into the leg)
      ((-22.5,9.4,79.2),(4.0,4.0,6.0),0.6),((15.6,-17.7,97.0),(4.0,4.0,5.0),0.5)]   # hip patches
def deflate(X,F,U):
    o=np.zeros(len(X))
    for c,r,a in DEFL: o+=a*ell_w(X,F,U,c,r,1.0)
    return o
def shoulder_w(X,F,U):     # Gate 5 shoulder-top crack and posterior armpit creases
    w=np.zeros(len(X))
    for sg in (-1,1):
        w=np.maximum(w,0.8*ell_w(X,F,U,(sg*19.0,-3.0,150.5),(5.0,6.5,5.5),0.5))
        w=np.maximum(w,0.9*ell_w(X,F,U,(sg*17.5,-7.2,143.0),(4.0,4.0,5.0),0.5))
    return w
def jaw_w(X,F,U): return 0.85*ell_w(X,F,U,(0.0,3.0,172.5),(11.0,11.0,4.2),0.5)     # mandible/throat collar shelf
def lowback_w(X,F,U):     # parallel lumbar channels flanking the tail root + the tail/thigh creases
    w=ell_w(X,F,U,(0.0,-13.0,108.0),(14.0,9.0,15.0),0.45)
    for sg in (-1,1): w=np.maximum(w,ell_w(X,F,U,(sg*9.0,-22.0,82.0),(7.0,10.0,10.0),0.45))
    return w
def patch_w(X,F,U): return ell_w(X,F,U,(-21.5,2.0,84.0),(5.0,11.0,10.0),0.4)
def field(X,F,U):
    e=g8.field(X,F,U); X=np.asarray(X,float); F=np.asarray(F,float); U=np.asarray(U,float)
    awh=away_from_hands(X,F,U)
    def zone(wfn,name,box,off):
        nonlocal e
        m=(X>box[0])&(X<box[1])&(F>box[2])&(F<box[3])&(U>box[4])&(U<box[5])
        if not m.any(): return
        w=wfn(X[m],F[m],U[m])*awh[m]*boxfade(X[m],F[m],U[m],box); k=w>1e-4
        if not k.any(): return
        ii=np.where(m)[0][k]; o=off(X[ii],F[ii],U[ii]) if callable(off) else off; e[ii]=mix(e[ii],LP(name,X[ii],F[ii],U[ii])+o,w[k])
    zone(torso_w,"torso",(-24,24,-20,19,94,160),0.10)
    zone(neck_w,"neck",(-16,16,-20,16,146,182),0.06)
    zone(jaw_w,"neck",(-16,16,-20,16,146,182),0.06)
    zone(shoulder_w,"torso",(-24,24,-20,19,94,160),0.10)
    for name,box in (("torso",(-24,24,-20,19,94,160)),("pelvis",(-28,28,-46,16,54,112))):     # groove fill: channels deeper than 0.3 cm under the low-pass are filled
        m=(X>box[0])&(X<box[1])&(F>box[2])&(F<box[3])&(U>box[4])&(U<box[5])
        if not m.any(): continue
        w=lowback_w(X[m],F[m],U[m])*boxfade(X[m],F[m],U[m],box); k=w>1e-4
        if not k.any(): continue
        ii=np.where(m)[0][k]; lp=LP(name,X[ii],F[ii],U[ii]); e[ii]=mix(e[ii],smin(e[ii],lp+0.3,0.6),w[k])
    zone(patch_w,"pelvis",(-28,-10,-16,16,66,102),0.12)
    e=e+deflate(X,F,U)*awh
    m=(np.abs(X)<28)&(F>-46)&(F<16)&(U>54)&(U<112)
    if m.any():
        w=pelvis_w(X[m],F[m],U[m])*awh[m]*boxfade(X[m],F[m],U[m],(-28,28,-46,16,54,112)); k=w>1e-4
        if k.any():
            ii=np.where(m)[0][k]; e[ii]=mix(e[ii],pelvis_field(X[ii],F[ii],U[ii]),w[k])
    return e
B8.sdf=lambda X,F,U: field(X,F,U)
B8.BOX=(-47.0,47.0,-60.0,28.0,-1.0,191.0)
if __name__=="__main__":
    import time; t=time.time()
    if len(sys.argv)>3: B8.BOX=tuple(map(float,sys.argv[3].split(',')))
    v,f=B8.mesh(float(sys.argv[1]),log=lambda *a: None)
    np.savez_compressed(sys.argv[2],v=v,f=f); print("DONE",len(v),len(f),round(time.time()-t,1))
