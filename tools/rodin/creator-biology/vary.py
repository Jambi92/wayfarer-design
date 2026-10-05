# Saurin creator-biology variation diagnostics: smooth region warps DERIVED from the frozen reference (never written back).
# Coordinates: x lateral, f forward, u up (cm), feet on u = 0. Reference = c12/g15_body (base) + c12/g15_surf (scaled surface).
import numpy as np
from scipy.spatial import cKDTree
REF_BASE='/tmp/claude-0/rodin/c12/g15_body.npz'; REF_SURF='/tmp/claude-0/rodin/c12/g15_surf.npz'
AXIS='/tmp/claude-0/rodin/g8/axis.npy'
AT=np.array([0.0,3.0,179.3]); PIV=np.array([0.0,-3.0,8.6]); HS=1.08
EYE_L=None
def ss(x): x=np.clip(x,0,1); return x*x*(3-2*x)
def band(u,a,b,c,d): return ss((u-a)/(b-a))*(1-ss((u-c)/(d-c)))
def ramp_int(t,a,b):
    """integral from -inf to t of smoothstep((t-a)/(b-a))"""
    w=b-a; x=np.clip((t-a)/w,0,1); return np.where(t<b, w*(x**3-x**4/2), w*0.5+(t-b))
S_ROOT=117.0; TIP_EXT=4.4   # caudal-base landmark station (axis crosses the posterior pelvic plane f = -14.8) ; tip lies 4.4 cm past axis[0]

class Labels:
    def __init__(self,V,N):
        x,f,u=V.T; ax=np.abs(x); self.side=np.where(x>=0,1.0,-1.0)
        g=np.interp(u,[78,88,100,110,120,125,130,136,142,150,156,160],[24,24,22,19,16,15.5,17,18.5,19.5,19.5,18,17])
        arm=(u>76)&(u<160)&(ax>g)
        self.arm=ss((ax-g+1.0)/2.0)*((u>76)&(u<162))*ss((158-u)/4.0+0.5)
        C=np.load(AXIS); self.C=C; tr=cKDTree(C); d,k=tr.query(V); s=k*0.5
        self.tail=ss((S_ROOT+3-s)/8.0)*ss((-f-14.0)/4.0)*(d<32)
        self.leg=ss((88-u)/4.0)*(1-self.arm)*(1-self.tail)
        self.head=ss((u-166)/8.0)
        self.torso=np.clip(1-self.arm-self.leg-self.tail-self.head,0,1)
        self.k=k; self.s=s
        # tail local frame offsets (planar axis in x = 0)
        T=np.gradient(C,axis=0); T/=np.linalg.norm(T,axis=1)[:,None]; self.T=T
        Nn=np.stack([np.zeros(len(T)),-T[:,2],T[:,1]],1)    # in-plane normal (f,u)
        self.Nn=Nn; o=V-C[k]; self.ox=o[:,0]; self.on=np.einsum('ij,ij->i',o,Nn[k]); self.ot=np.einsum('ij,ij->i',o,T[k])
        # limb slice centroids (per side, 1 cm u-bins) for radial girth scaling
        self.cen={}
        for nm,w in (('leg',self.leg),('arm',self.arm)):
            for sd in (1,-1):
                m=(w>0.5)&(self.side==sd); ub=np.floor(u[m]).astype(int)
                cx=np.full(200,np.nan); cf=np.full(200,np.nan)
                for b in np.unique(ub): mm=ub==b; cx[b]=x[m][mm].mean(); cf[b]=f[m][mm].mean()
                ok=~np.isnan(cx); ii=np.arange(200); cx=np.interp(ii,ii[ok],cx[ok]); cf=np.interp(ii,ii[ok],cf[ok])
                self.cen[(nm,sd)]=(cx,cf)
        m=self.torso>0.5; ub=np.floor(u[m]).astype(int); cf=np.full(200,np.nan)
        for b in np.unique(ub): cf[b]=f[m][ub==b].mean()
        ok=~np.isnan(cf); ii=np.arange(200); self.torso_cf=np.interp(ii,ii[ok],cf[ok])
        self.N=N
        # composition maps
        fc=np.interp(u,np.arange(200),self.torso_cf)
        arm_mus=self.arm*(band(u,124,130,146,152)+0.8*band(u,100,104,116,120))
        legx,legf=[np.where(self.side>0,np.interp(u,ii,self.cen[('leg',1)][j]),np.interp(u,ii,self.cen[('leg',-1)][j])) for j in (0,1)]
        self.mus=np.clip(arm_mus+self.torso*(0.9*band(u,138,144,152,158)*ss((ax-11)/3)+0.6*band(u,100,108,140,150)*ss((fc-6-f)/4)*ss((10-ax)/3)
                  +0.2*band(u,95,100,122,128))+0.7*self.head*0+self.leg*(band(u,54,62,80,88)+0.8*band(u,16,22,38,44)*ss((legf-f)/3))
                  +ss((u-154)/3)*(1-self.head)*0.7*ss((fc-f)/3),0,1)
        self.fat=np.clip(self.torso*(1.0*band(u,90,98,116,126)*ss((f-fc-2)/4)+0.6*band(u,96,102,116,124)*ss((ax-8)/3)+0.15)
                  +self.leg*0.15*ss((u-20)/10)+(1-self.arm)*(1-self.tail)*0.5*band(u,64,72,98,106)*ss((ax-9)/3)+self.arm*0.25*band(u,122,128,144,150)
                  +0.3*band(u,158,162,170,174)*ss((f-fc)/3)*(1-self.head),0,1)
        snn=np.clip((self.s+TIP_EXT)/(S_ROOT+TIP_EXT),0,1)
        self.mus=np.clip(self.mus*(1-self.tail)+self.tail*0.85*ss((snn-0.30)/0.45),0,1)
        self.fat_tail_graded=self.tail*(0.55*ss((snn-0.30)/0.55)+0.12)     # caudal adipose graded over the proximal ~half (valid)
        self.fat_tail_conc=self.tail*(0.75*ss((snn-0.68)/0.25)+0.12)       # concentrated at the caudal base (diagnostic: invalid)
        self.fat=np.clip(self.fat*(1-self.tail)+self.fat_tail_graded,0,1); self.fat_conc=np.clip(self.fat-self.fat_tail_graded+self.fat_tail_conc,0,1)
        hand=self.arm*ss((99-u)/3); foot=ss((10-u)/2)
        self.mus*=(1-hand)*(1-foot); self.fat*=(1-hand)*(1-foot)

def head_local(P): return (P-AT-PIV)/HS+PIV
def head_world(L): return (L-PIV)*HS+PIV+AT

def warp(V,L,p,eye=None):
    """p: dict of parameters (1.0 / 0.0 = reference). returns new vertex array"""
    P=V.copy(); x,f,u=P.T.copy(); N=L.N
    g=lambda k,d=None: p.get(k,1.0 if d is None else d)
    # 1. composition (normal offsets): muscle +1 -> +0.9 cm, -1 -> -0.45 cm ; fat +1 -> +2.2 cm, -1 -> -0.35 cm
    m=p.get('muscle',0.0); fa=p.get('fat',0.0)
    fmap=L.fat_conc if p.get('tail_fat_conc',0) else L.fat
    off=L.mus*(0.9*m if m>0 else 0.45*m)+fmap*(2.2*fa if fa>0 else 0.35*fa)
    P+= off[:,None]*N
    # 2. tail: radial shape then path (length, curvature)
    sn=np.clip((L.s+TIP_EXT)/(S_ROOT+TIP_EXT),0,1)
    gb=1+(g('tail_base')-1)*sn**1.5                                   # base mass, tip fixed
    gt=1+(g('tail_taper')-1)*np.sin(np.pi*sn)**1.2*(1-0.25*sn)         # mid/distal fullness (root & tip fixed)
    gm=1.0
    gfr=1+(g('tail_frame')-1)*sn**1.2
    gx=gb*gt*gm*gfr*g('tail_lat'); gn=gb*gt*gm*gfr/g('tail_lat')**0.5
    C=L.C; kL=g('tail_len'); curv=p.get('tail_curv',0.0)              # curv: added droop (+) / lift (-) in degrees over the whole tail
    k_root=int(S_ROOT*2); seg=np.diff(C,axis=0)                       # C index increases toward the head
    w=np.clip((S_ROOT+5-np.arange(len(C))*0.5)/10.0,0,1)                # 1 on free tail, 0 above the root zone
    sc=1+(kL-1)*w[:-1]
    ang=np.radians(curv)*np.clip((S_ROOT-np.arange(len(C))*0.5)/S_ROOT,0,1)  # rotation grows toward the tip
    # rebuild path from the root downward: rotate & scale segment vectors
    C2=C.copy(); 
    for i in range(k_root-1,-1,-1):
        a=ang[i]; ca,sa=np.cos(a),np.sin(a); d=-seg[i]*sc[i]          # vector from i+1 to i
        df,du=d[1],d[2]; nf=ca*df-sa*du; nu=sa*df+ca*du   # CCW in (f,u): +angle droops a backward-pointing segment
        C2[i]=C2[i+1]+np.array([0.0,nf,nu])
    p['_C2']=C2
    T2=np.gradient(C2,axis=0); T2/=np.linalg.norm(T2,axis=1)[:,None]; N2=np.stack([np.zeros(len(T2)),-T2[:,2],T2[:,1]],1)
    k=L.k; ox=L.ox+off*N[:,0]; on=L.on+off*np.einsum('ij,ij->i',N,L.Nn[k]); ot=L.ot+off*np.einsum('ij,ij->i',N,L.T[k])
    Pt=C2[k]+(ox*gx)[:,None]*np.array([1.0,0,0])+(on*gn)[:,None]*N2[k]+ot[:,None]*T2[k]
    Pt+= (off*0)[:,None]
    wt=L.tail[:,None]; P=P*(1-wt)+Pt*wt
    # 3. head-local warps
    if any(k_ in p for k_ in ('ros_len','ros_w','ros_aw','ros_d','jaw_d','cran_len','cran_w','cran_d','orbit','head')):
        Lh=head_local(P); X,Fh,U=Lh.T.copy()
        um=0.4
        X2=X*(1+(g('ros_w')-1)*ss((Fh-8.0)/4.0))*(1+(g('ros_aw')-1)*ss((Fh-11.5)/2.5))
        X2=X2*(1+(g('cran_w')-1)*ss((5.0-Fh)/3.0)*ss((U-1.0)/2.0))
        U2=np.where(U>um, um+(U-um)*(1+(g('ros_d')-1)*ss((Fh-8.0)/3.0)), um+(U-um)*(1+(g('ros_d')-1)*ss((Fh-8.0)/3.0)))
        U2=np.where(U<um, um+(U2-um)*(1+(g('jaw_d')-1)*ss((8.0-Fh)/3.0)), U2)
        U2=np.where(U>3.0, 3.0+(U2-3.0)*(1+(g('cran_d')-1)*ss((4.0-Fh)/3.0)), U2)
        F2=Fh+(g('ros_len')-1)*ramp_int(Fh,7.6,9.6)-(g('cran_len')-1)*ramp_int(-Fh,-4.0,-1.0)
        Lh2=np.stack([X2,F2,U2],1)
        if eye is not None and g('orbit')!=1.0:
            for c in eye[0]:
                c=np.array(c); r=np.linalg.norm(Lh2-c,axis=1); R=eye[1]*2.0
                Lh2=c+(Lh2-c)*(1+(g('orbit')-1)*(1-ss(r/R)))[:,None]
        if g('head')!=1.0:
            pv=head_local(np.array([[0.0,-3.0,170.0]]))[0]; Lh2=pv+(Lh2-pv)*g('head')
        Pw=head_world(Lh2); wh=L.head[:,None]; P=P*(1-wh)+Pw*wh
    x,f,u=P.T.copy()
    # 4. frame: limb girth (radial about slice centroid), torso breadth bands, thoracic depth, pelvis width
    ii=np.arange(200); ub=np.clip(u0:=V[:,2],0,199)
    for nm,key,wl in (('leg','leg_girth',L.leg),('arm','arm_girth',L.arm)):
        sg=g(key)
        if sg!=1.0:
            for sd in (1,-1):
                cx=np.interp(ub,ii,L.cen[(nm,sd)][0]); cf=np.interp(ub,ii,L.cen[(nm,sd)][1]); mm=(L.side==sd)
                x=np.where(mm, x+wl*(sg-1)*(x-cx), x); f=np.where(mm, f+wl*(sg-1)*(f-cf), f)
    tor=1-L.arm-L.leg-L.tail; tor=np.clip(tor,0,1)
    sx=1+(g('shoulder')-1)*band(u0,132,142,158,166)+(g('thorax_w')-1)*band(u0,108,118,140,150)+(g('pelvis_w')-1)*band(u0,78,86,100,110)
    x=np.where(tor>0, x*(1+(sx-1)*tor), x)
    cft=np.interp(ub,ii,L.torso_cf); sd_=1+(g('thorax_d')-1)*band(u0,110,120,150,158)+(g('neck_d')-1)*band(u0,154,160,170,176)*(1-L.head)
    f=np.where(tor>0, cft+(f-cft)*(1+(sd_-1)*tor), f)
    x=x+L.arm*L.side*(g('shoulder')-1)*15.8+L.leg*L.side*(g('pelvis_w')-1)*8.8
    # hands / feet size (about wrist / ankle)
    if g('hand')!=1.0:
        hw=L.arm*ss((99-u0)/3)
        for sd in (1,-1):
            cx=np.interp(97,ii,L.cen[('arm',sd)][0]); cf=np.interp(97,ii,L.cen[('arm',sd)][1]); mm=L.side==sd
            x=np.where(mm,x+hw*(g('hand')-1)*(x-cx),x); f=np.where(mm,f+hw*(g('hand')-1)*(f-cf),f); u=np.where(mm,u+hw*(g('hand')-1)*(u-97),u)
    if g('foot')!=1.0:
        fw=ss((10-u0)/3)*(1-L.tail)
        for sd in (1,-1):
            cx=np.interp(5,ii,L.cen[('leg',sd)][0]); mm=L.side==sd
            x=np.where(mm,x+fw*(g('foot')-1)*(x-cx),x); f=np.where(mm,f+fw*(g('foot')-1)*(f-(-2.2)),f); u=np.where(mm,u+fw*(np.sqrt(g('foot'))-1)*u,u)
    # 5. segment lengths: vertical stretch map with arms following the shoulder and the tail following its root
    dens=1+(g('leg_len')-1)*band(u0,8,14,82,88)+(g('trunk_len')-1)*band(u0,88,94,118,124)+(g('thorax_len')-1)*band(u0,118,124,150,156)+(g('neck_len')-1)*band(u0,154,158,168,172)
    grid=np.linspace(0,200,2001); dg=1+(g('leg_len')-1)*band(grid,8,14,82,88)+(g('trunk_len')-1)*band(grid,88,94,118,124)+(g('thorax_len')-1)*band(grid,118,124,150,156)+(g('neck_len')-1)*band(grid,154,158,168,172)
    Phi=np.concatenate([[0],np.cumsum(0.5*(dg[1:]+dg[:-1])*np.diff(grid))])
    dU=np.interp(u0,grid,Phi)-u0
    dSh=np.interp(150.0,grid,Phi)-150.0; dRoot=np.interp(96.0,grid,Phi)-96.0
    ka=g('arm_len')
    shx=L.side*(15.8*g('shoulder')); sh=np.stack([shx,np.full_like(x,-2.0),np.full_like(x,150.0)],1)
    rel=np.stack([x,f,u],1)-sh; dirv=np.stack([L.side*np.sin(np.radians(17)),np.full_like(x,-0.06),-np.cos(np.radians(17))*np.ones_like(x)],1)
    along=np.einsum('ij,ij->i',rel,dirv); armP=np.stack([x,f,u],1)+((ka-1)*np.clip(along,0,None)*ss(along/4))[:,None]*dirv
    wa=L.arm[:,None]; wt=L.tail[:,None]
    Pn=np.stack([x,f,u],1); Pn=Pn*(1-wa)+armP*wa
    Pn[:,2]+= dU*(1-L.arm-L.tail).clip(0,1)+dSh*L.arm+dRoot*L.tail
    C2=p['_C2']; wa_=ss((S_ROOT+3-np.arange(len(C2))*0.5)/8.0); C2=C2.copy(); C2[:,2]+=dRoot*wa_+(np.interp(C2[:,2],grid,Phi)-C2[:,2])*(1-wa_); p['_C2']=C2
    # 6. global stature
    h=Pn[:,2].max() if p.get('_hmeas') is None else p['_hmeas']
    s=p.get('height',187.881473082305)/h; Pn=Pn*s; p['_C2']=p['_C2']*s; p['_s']=s
    return Pn
