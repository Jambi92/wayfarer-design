# common.py : shared source loading, part labels and planar ray snapping for the RP2 Grask retopo
import numpy as np, trimesh, json, sys
sys.path.insert(0,'/tmp/claude-0/src3d/v5/tools')
SRC='/tmp/claude-0/src3d/v5/v005.npz'
PARTS=['axial','ear_l','ear_r','arm_l','arm_r','hand_l','hand_r']+['%s_%s'%(d,s) for s in 'lr' for d in ('thumb','index','middle','ring','pinky')]+['leg_l','leg_r','foot_l','foot_r']+['%s_%s'%(t,s) for s in 'lr' for t in ('hallux','toe2','toe3','toe4','toe5')]
PID={p:i for i,p in enumerate(PARTS)}
def load_src():
    M=np.load(SRC); return M['V'].astype(float), M['Q'].astype(np.int64)
def capsule_d(P,a,b,ra,rb):
    ab=b-a; t=np.clip(((P-a)@ab)/(ab@ab),0,1); q=a+t[:,None]*ab; return np.linalg.norm(P-q,axis=1)-(ra+(rb-ra)*t)
_EAR=None
def ear_mask(P):
    """ear = source region inside the head-grid ear port window (z 198..208.5, ring columns 25..29 / 11..15 of 40)"""
    global _EAR
    if _EAR is None:
        V,F=load_src(); zs=np.arange(195,212,0.5); fc=[]
        for z in zs:
            m=(np.abs(V[:,2]-z)<0.6)&(np.abs(V[:,0])<6.5); q=V[m]; fc.append(0.5*(q[:,1].min()+q[:,1].max()))
        _EAR=(zs,np.array(fc))
    zs,fc=_EAR; f0=np.interp(P[:,2],zs,fc)
    th=np.degrees(np.arctan2(-P[:,0],P[:,1]-f0))%360
    inz=(P[:,2]>198.0)&(P[:,2]<208.5)
    return inz&(((th>25*9)&(th<29*9)&(P[:,0]>0))|((th>11*9)&(th<15*9)&(P[:,0]<0)))&(np.abs(P[:,0])>4)
def label_points(P, L):
    """part id per point (analysis frame). L = landmark dict (p arrays)."""
    from hand_model import DEF as HDEF, scaled, finger_chain
    from hand_frame import frame
    import foot_model as fm
    lab=np.full(len(P),PID['axial'])
    x,f,z=P.T; ax=np.abs(x)
    for s,sg in (('l',1),('r',-1)):
        side=sg*x>0
        # legs: below the crotch band, lateral of midline
        leg=side&(z<116)&(ax>0.0); lab[leg]=PID['leg_'+s]
        # arms: free below armpit (z<153) and lateral (>|x| 19.5..)  ; above: lateral of shoulder seam plane
        g=np.array(L['glenohumeral_'+s]['p'])
        apath=[np.array(L['glenohumeral_'+s]['p']),np.array(L['elbow_'+s]['p']),np.array(L['wrist_'+s]['p']),np.array(L['middle_mcp_'+s]['p']),np.array(L['middle_tip_'+s]['p'])]
        lpath=[np.array(L['hip_'+s]['p']),np.array(L['knee_'+s]['p']),np.array(L['ankle_'+s]['p'])]
        def pd(path,rad):
            return np.min([capsule_d(P,path[i],path[i+1],rad[i],rad[i+1]) for i in range(len(path)-1)],0)
        da=pd(apath,[5.5,4.5,3.6,2.6,1.0]); dl=pd(lpath,[10.5,6.5,4.5])
        SJ=json.load(open('/tmp/claude-0/rt/shoulder.json'))[s]; A=np.array(SJ['A']); nS=np.array(SJ['n'])
        arm_low=side&(z<A[2]-0.5)&(z>60)&(da<dl)&(ax>15)
        seam=side&(z>=A[2]-0.5)&(z<192)&(((P-A)@nS)>0)
        lab[arm_low|seam]=PID['arm_'+s]
        # hand: distal of wrist plane
        W,M=frame(s.upper()); Lh=(P-W)@M; hand=side&(Lh[:,0]>-0.5)&(Lh[:,0]<32)&(Lh[:,1]>-10)&(Lh[:,1]<15)&(Lh[:,2]>-11)&(Lh[:,2]<7)&(z<112)&(ax>15)&(da<dl); lab[hand]=PID['hand_'+s]
        p=scaled(HDEF); idx=np.nonzero(hand)[0]; Q=Lh[idx]; best=np.full(len(idx),0.9); who=np.full(len(idx),-1)
        names=['thumb','index','middle','ring','pinky']
        for di,nm in enumerate(names):
            if nm=='thumb':
                T=p['thumb']; dth=np.array(T['dir'],float); dth/=np.linalg.norm(dth); J=[np.array(T['cmc'],float)]; J.append(J[0]+T['L'][0]*dth)
                # approximate thumb chain by the hand_model construction
                from hand_model import rot
                dor=np.array(T['dors'],float); dor-=(dor@dth)*dth; dor/=np.linalg.norm(dor); dirs=[dth]; dors=[dor]
                for k in range(2):
                    lat=np.cross(dirs[-1],dors[-1]); R=rot(lat,np.radians(T['flex'][k]))
                    if (R@dirs[-1])@dors[-1]>0: R=rot(lat,-np.radians(T['flex'][k]))
                    dirs.append(R@dirs[-1]); dors.append(R@dors[-1]); J.append(J[-1]+T['L'][k+1]*dirs[-1])
                r=[x*1.1 for x in T['r']]; segs=[(J[1],J[2],r[1],r[3]),(J[2],J[3],r[3],r[5]),(J[0]+(J[1]-J[0])*0.55,J[1],r[0]*0.9,r[1])]
            else:
                f_=p['fingers'][nm]; J,_,_=finger_chain(f_['mcp'],f_['L'],f_['splay'],f_['flex']); r=[v*m for v,m in zip(f_['r'],[1.13,1.10,1.06,1.04])]
                segs=[(J[0]+(J[1]-J[0])*0.12,J[1],r[0],r[1]),(J[1],J[2],r[1],r[2]),(J[2],J[3],r[2],r[3])]
            d=np.min([capsule_d(Q,a,b,ra*1.25,rb*1.25) for a,b,ra,rb in segs],0)
            better=d<best; best[better]=d[better]; who[better]=di
        for di,nm in enumerate(names):
            lab[idx[who==di]]=PID['%s_%s'%(nm,s)]
        # foot
        foot=side&(z<14)&(P[:,1]>-2) & ~((z>9)&(P[:,1]<4)); lab[foot]=PID['foot_'+s]
        idx=np.nonzero(foot)[0]; Q=P[idx].copy(); Q[:,0]*=sg; best=np.full(len(idx),0.6); who=np.full(len(idx),-1)
        for ti,t in enumerate(fm.DEF['toes']):
            J,_,_=fm.chain(t); r=t['r']; segs=[(J[k]+(J[k+1]-J[k])*(0.35 if k==0 else 0),J[k+1],r[k]*1.3,r[k+1]*1.3) for k in range(len(t['L']))]
            d=np.min([capsule_d(Q,a,b,ra,rb) for a,b,ra,rb in segs],0); better=d<best; best[better]=d[better]; who[better]=ti
        for ti,t in enumerate(fm.DEF['toes']): lab[idx[who==ti]]=PID['%s_%s'%(t['n'],s)]
        # ears
        ear=side&ear_mask(P)
        lab[ear]=PID['ear_'+s]
    return lab
ADJ={}
def adj(a,b): ADJ.setdefault(a,set()).add(b); ADJ.setdefault(b,set()).add(a)
for s in 'lr':
    adj('axial','ear_'+s); adj('axial','arm_'+s); adj('arm_'+s,'hand_'+s); adj('axial','leg_'+s); adj('leg_'+s,'foot_'+s)
    for d in ('thumb','index','middle','ring','pinky'): adj('hand_'+s,'%s_%s'%(d,s))
    for t in ('hallux','toe2','toe3','toe4','toe5'): adj('foot_'+s,'%s_%s'%(t,s))
adj('leg_l','leg_r')
def frame_from_normal(n,ref):
    n=n/np.linalg.norm(n); a=ref-(ref@n)*n; a/=np.linalg.norm(a); b=np.cross(n,a); return n,a,b
class Snapper:
    def __init__(self,V,F,flab):
        self.V=V; self.F=F; self.flab=flab; self.cache={}
    def sub(self,parts):
        key=tuple(sorted(parts))
        if key not in self.cache:
            m=np.isin(self.flab,[PID[p] for p in parts]); self.cache[key]=trimesh.Trimesh(self.V,self.F[m],process=False)
        return self.cache[key]
    def ring(self,parts,c,n,a,thetas,rfall=None,near=None):
        """cast in-plane rays from c at angles thetas (basis a,b=n x a); return points on the labelled section (first hit from c outward,
        choosing the contour set nearest to c)."""
        m=self.sub(parts); n,a,b=frame_from_normal(n,a)
        out=np.zeros((len(thetas),3)); ok=np.zeros(len(thetas),bool)
        try: L=trimesh.intersections.mesh_plane(m,n,c)
        except Exception: return None,ok
        if len(L)==0: return None,ok
        q0=L[:,0]-c; q1=L[:,1]-c; S0=np.stack([q0@a,q0@b],1); S1=np.stack([q1@a,q1@b],1)
        for i,t in enumerate(thetas):
            d=np.array([np.cos(t),np.sin(t)]); best=None
            for p0,p1 in ((S0,S1),):
                e=p1-p0
                # solve r*d = p0 + u*e
                den=d[0]*(-e[:,1])-d[1]*(-e[:,0]); den=np.where(np.abs(den)<1e-12,1e-12,den)
                r=(p0[:,0]*(-e[:,1])-p0[:,1]*(-e[:,0]))/den; u=(d[0]*p0[:,1]-d[1]*p0[:,0])/den
                ok_=(u>=0)&(u<=1)&(r>0)
                if ok_.any():
                    rr=r[ok_].min() if near is None else r[ok_][np.argmin(np.abs(r[ok_]-near[i]))]
                    if best is None or (rr<best if near is None else abs(rr-near[i])<abs(best-near[i])): best=rr
            if best is not None: out[i]=c+best*(np.cos(t)*a+np.sin(t)*b); ok[i]=True
        return out,ok
def _seg_closest(P,A,B):
    """P (m,2), segments A,B (n,2) -> closest points (m,2)"""
    out=np.zeros_like(P)
    AB=B-A; L2=np.maximum((AB*AB).sum(1),1e-12)
    for i,p in enumerate(P):
        t=np.clip(((p-A)*AB).sum(1)/L2,0,1); Q=A+t[:,None]*AB; d=((Q-p)**2).sum(1); out[i]=Q[np.argmin(d)]
    return out
def ring_closest(SN,parts,c,n,a,targets2d_fn):
    """section of labelled parts by plane (c,n); targets2d_fn(bbox)->(m,2) in-plane coords; returns 3D closest section points"""
    m=SN.sub(parts); n,a,b=frame_from_normal(n,a)
    L=trimesh.intersections.mesh_plane(m,n,c)
    if len(L)==0: return None
    q0=L[:,0]-c; q1=L[:,1]-c; S0=np.stack([q0@a,q0@b],1); S1=np.stack([q1@a,q1@b],1)
    allp=np.vstack([S0,S1]); bb=(allp.min(0),allp.max(0))
    T=targets2d_fn(bb,allp)
    mid=(S0+S1)/2; ok=(np.abs(mid[:,0]-T[:,0].mean())<1.3*(T[:,0].max()-T[:,0].mean())+0.5)&(np.abs(mid[:,1]-T[:,1].mean())<1.3*(T[:,1].max()-T[:,1].mean())+0.5)
    Q=_seg_closest(T,S0[ok],S1[ok])
    return c+Q[:,0:1]*a+Q[:,1:2]*b
def _closest_on_segs(X,A,B):
    """X (m,3); segments A,B (n,3) -> closest points (m,3)"""
    AB=B-A; L2=np.maximum((AB*AB).sum(1),1e-12); out=np.zeros_like(X)
    for i,x in enumerate(X):
        t=np.clip(((x-A)*AB).sum(1)/L2,0,1); P=A+AB*t[:,None]; j=np.argmin(((P-x)**2).sum(1)); out[i]=P[j]
    return out
def advance_ring(SN,parts,Pprev,c,n,mix=0.35,maxstep=None):
    """next ring on plane (c,n): each column continues from Pprev[k] along the surface direction orthogonal to the
    previous ring (minimises quad shear), snapped to the labelled section; then blended toward arclength-uniform spacing."""
    import igl
    from cage import arc_resample_phase
    m=SN.sub(parts); n=n/np.linalg.norm(n)
    L=trimesh.intersections.mesh_plane(m,n,c)
    if len(L)==0: return None
    if not hasattr(SN,'_fn'):
        SN._fn=np.cross(SN.V[SN.F[:,1]]-SN.V[SN.F[:,0]],SN.V[SN.F[:,2]]-SN.V[SN.F[:,0]]); SN._fn/=np.maximum(np.linalg.norm(SN._fn,axis=1),1e-12)[:,None]
    _,fi,_=igl.point_mesh_squared_distance(Pprev,SN.V,SN.F); Ns=SN._fn[fi]
    T=np.roll(Pprev,-1,0)-np.roll(Pprev,1,0); D=np.cross(Ns,T); D/=np.maximum(np.linalg.norm(D,axis=1),1e-12)[:,None]
    sgn=np.sign((D@n).sum()); D*=sgn
    dn=D@n; s=((c-Pprev)@n)/np.where(np.abs(dn)<0.2,0.2*np.sign(dn+1e-12),dn)
    X=Pprev+D*s[:,None]; X=X-np.outer((X-c)@n,n)
    P=_closest_on_segs(X,L[:,0],L[:,1])
    if mix>0: P=arc_resample_phase(P,mix); P=_closest_on_segs(P,L[:,0],L[:,1])
    # untangle: a column whose ring edge reverses against the previous ring's edge is folded -> re-place by neighbours
    for _ in range(20):
        e_new=np.roll(P,-1,0)-P; e_old=np.roll(Pprev,-1,0)-Pprev
        bad=np.nonzero((e_new*e_old).sum(1)<0.2*np.linalg.norm(e_new,axis=1)*np.linalg.norm(e_old,axis=1))[0]
        if len(bad)==0: break
        idx=np.unique(np.r_[bad,(bad+1)%len(P)])
        P[idx]=0.5*(P[(idx-1)%len(P)]+P[(idx+1)%len(P)]); P[idx]=_closest_on_segs(P[idx],L[:,0],L[:,1])
    return P
