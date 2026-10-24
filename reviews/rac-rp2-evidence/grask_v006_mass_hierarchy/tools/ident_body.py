# ident_body.py : Grask identity edits for hands, feet and skeletal relief carriers (girdle, elbows, knees, wrists, pelvis, shin).
import numpy as np, json
R='/tmp/claude-0/rp2/'
J=json.loads(str(np.load(R+'GR5DE3_r6.npz')['joints']))
def ss(t): t=np.clip(t,0,1); return t*t*(3-2*t)
def jh(k): return np.array(J[k][0],float)
def jt(k): return np.array(J[k][1],float)
FING=['thumb','index','middle','ring','pinky']
def seg_param(V,h,t):
    a=t-h; tt=((V-h)@a)/(a@a); tc=np.clip(tt,0,1); foot=h+tc[:,None]*a; return tt,tc,V-foot,np.linalg.norm(V-foot,axis=1)
def hand_map(V, Wb, s, p):
    """skeleton-driven re-sweep of one hand: hand scale about the wrist, finger elongation, knobby joints, pad broadening."""
    w=jh('hand_'+s); fw=Wb['fingers_'+s]; hw=Wb['hand_'+s]+fw
    out=V.copy()
    # nearest finger segment per vertex
    segs=[(f,i) for f in FING for i in (1,2,3)]
    dist=[]; par=[]
    for f,i in segs:
        tt,tc,o,d=seg_param(V,jh('%s_0%d_%s'%(f,i,s)),jt('%s_0%d_%s'%(f,i,s))); dist.append(d); par.append((tt,tc,o))
    dist=np.array(dist); dmin=dist.min(0)
    SW=np.exp(-(dist-dmin)/p.get('seg_soft',0.35)); SW/=SW.sum(0)
    Fm=np.zeros_like(V)
    e=p['finger_elong']; kj=p['knuckle']; kp=p['pad']; th=p['finger_thick']
    for f in FING:
        newhead=jh('%s_01_%s'%(f,s)).copy()
        for i in (1,2,3):
            k=segs.index((f,i)); h=jh('%s_0%d_%s'%(f,i,s)); t=jt('%s_0%d_%s'%(f,i,s)); a=t-h
            tt,tc,o=par[k]
            ext=e*(1.0 if f!='thumb' else 0.6)
            rad=1+th+kj*(np.exp(-(tc/0.2)**2)*(1.3 if i==1 else 1.0)+np.exp(-((tc-1)/0.2)**2)*(0.0 if i==3 else 1.0))
            if i==3: rad=rad+kp*np.exp(-((tc-0.8)/0.22)**2)
            q=V+(newhead-h)+tt[:,None]*a*ext+o*(rad-1)[:,None]
            Fm+=SW[k][:,None]*q
            if i<3: newhead=newhead+(jh('%s_0%d_%s'%(f,i+1,s))-h)*(1+ext)
    # palm: broaden across the metacarpal heads (perpendicular to the hand axis, in the palm plane), deepen slightly
    ax=jt('hand_'+s)-w; ax/=np.linalg.norm(ax)
    Pm=V.copy(); rel=V-w; along=rel@ax; perp=rel-np.outer(along,ax)
    pb=p['palm_broad']*ss(along/ max(np.linalg.norm(jh('middle_01_'+s)-w),1e-3))
    Pm=w+np.outer(along,ax)+perp*(1+pb)[:,None]
    f_=ss(fw/0.8)
    M=(1-f_)[:,None]*Pm+f_[:,None]*Fm
    M=w+p['hand_scale']*(M-w)
    g=ss(hw/0.6)*ss((V-w)@ax/2.0+0.5)        # fade in from just above the wrist
    out=V+g[:,None]*(M-V)
    return out-V
def foot_map(V, Wb, s, p, N=None):
    fwt=Wb['foot_'+s]+Wb['ball_'+s]; a0=jh('foot_'+s); b0=jh('ball_'+s); toe=jt('ball_'+s)
    g=ss(fwt/0.6)*ss((a0[2]+4-V[:,2])/4)        # foot region below ~ankle+4
    D=np.zeros_like(V); x,f,z=V.T; xc=a0[0]
    # toes: elongate forward from the ball line and splay (fan) about the foot axis
    tz=ss((f-(b0[1]-1.0))/3.0)
    D[:,1]+=tz*(f-(b0[1]-1.0))*p['toe_elong']
    D[:,0]+=tz*(x-xc)*p['toe_splay']*np.clip((f-b0[1])/6,0,1.5)
    # forefoot breadth at the metatarsal heads
    fb=np.exp(-((f-(b0[1]-1.5-p.get('fore_shift',0.0)))/p.get('fore_sig',3.5))**2)
    D[:,0]+=fb*(x-xc)*p['fore_broad']
    # heel: posterior calcaneal projection
    heel=np.exp(-((f-(a0[1]-5.5))/2.5)**2)*np.exp(-((z-3.0)/2.8)**2)
    D[:,1]+=-heel*p['heel_back']
    if N is not None and p.get('toe_thick'):
        b=b0[1]; kn=p.get('toe_knob',0)
        prof=p['toe_thick']*tz+kn*(np.exp(-((f-(b+1.0))/1.2)**2)+np.exp(-((f-(b+5.0))/1.0)**2))*tz
        D+=prof[:,None]*N
    # hallux separation: move the big-toe column medially, growing toward the tip
    if p.get('hallux_sep'):
        med=x<xc-np.sign(xc)*0 if xc>0 else x>xc
        hx=ss((np.abs(x-xc)-2.2)/1.2)*(np.sign(x-xc)==-np.sign(xc))
        D[:,0]+=-np.sign(xc)*p['hallux_sep']*hx*tz*np.clip((f-b0[1])/7,0,1.3)
    return D*g[:,None]
def nearest_surface(V, mask, origin, direction):
    idx=np.nonzero(mask)[0]; sc=(V[idx]-origin)@direction; return V[idx[sc.argmax()]]
def bumps(V, N, p):
    """bony relief: list of (centre, sigma_cm, amp_cm) along outward normals, mirrored left/right."""
    D=np.zeros_like(V)
    for c,sig,amp in p:
        for sgn in (1,-1):
            cc=np.array(c,float)*np.array([sgn,1,1]); d=np.linalg.norm(V-cc,axis=1)
            D+=(amp*np.exp(-0.5*(d/sig)**2))[:,None]*N
    return D
def seg_ridge(V, N, h, t, sig, amp, mask):
    tt,tc,o,d=seg_param(V,h,t); w=np.exp(-0.5*(d/sig)**2)*np.sin(np.pi*np.clip(tc,0,1))*mask
    return (amp*w)[:,None]*N
def landmarks():
    """surface landmark centres for the left side (mirrored in bumps)"""
    Hh=np.load(R+'hstar.npz')['V']; W=dict(np.load(R+'weights_body.npz')); L={}
    def pick(c,d,wk,r=8,slab=2.5):
        m=(np.linalg.norm(Hh-c,axis=1)<r)&(np.abs(Hh[:,2]-c[2])<slab)&(Hh[:,0]>0)
        if wk: m&=sum(W[k] for k in wk)>0.4
        return nearest_surface(Hh,m,c,np.asarray(d,float)/np.linalg.norm(d))
    arm=['upperarm_l','lowerarm_l']; leg=['thigh_l','calf_l']
    el=jh('lowerarm_l'); L['olecranon']=pick(el,[0,-1,0],arm); L['epicondyle_lat']=pick(el,[1,0.2,0],arm); L['epicondyle_med']=pick(el,[-1,0.2,0],arm)
    kn=jh('calf_l'); L['patella']=pick(kn+[0,0,1.0],[0,1,0],leg); L['condyle_lat']=pick(kn,[1,0.3,0],leg); L['condyle_med']=pick(kn,[-1,0.3,0],leg)
    L['tib_tub']=pick(kn+[0,0,-6.5],[0,1,0],['calf_l'])
    wr=jh('hand_l'); L['styloid_ulnar']=pick(wr+[0,0,1.0],[0,-1,0],['lowerarm_l','hand_l'],6,1.5); L['styloid_radial']=pick(wr+[0,0,1.0],[0,1,0],['lowerarm_l','hand_l'],6,1.5)
    an=jh('foot_l'); L['mall_lat']=pick(an+[0,0,-0.5],[1,0,0],['calf_l','foot_l'],6,1.5); L['mall_med']=pick(an+[0,0,0.5],[-1,0,0],['calf_l','foot_l'],6,1.5)
    ac=jt('clavicle_l'); L['acromion']=pick(ac+[0,0,1.0],[0.6,0,1],None,8,3)
    fo=jh('foot_l'); L['instep']=pick(fo+[0,6.5,-2.5],[0,0.35,1],['foot_l'],6,2.5)
    ps=jh('thigh_l'); L['asis']=pick(ps+[-1,0,9.5],[0.25,1,0],['pelvis','spine_01'],9,2.0); L['trochanter']=pick(ps+[0,0,-3],[1,0,0],['thigh_l','pelvis'],10,2.0)
    return L
def _pchip(x,y,t):
    from scipy.interpolate import PchipInterpolator
    return PchipInterpolator(np.asarray(x,float),np.asarray(y,float),extrapolate=False)(np.clip(t,x[0],x[-1]))
def trunk_field(V, Wb, p):
    """continuous trunk breadth/depth field: kx(z), kf(z) front, kb(z) back (PCHIP in z); trunk weights only (no thigh band), arms excluded"""
    z=np.asarray(p['z'],float); kx=_pchip(z,p['kx'],V[:,2]); kf=_pchip(z,p['kf'],V[:,2]); kb=_pchip(z,p['kb'],V[:,2])
    inside=(V[:,2]>=z[0])&(V[:,2]<=z[-1]); kx=np.where(inside,kx,1); kf=np.where(inside,kf,1); kb=np.where(inside,kb,1)
    tw=np.clip(Wb['spine_01']+Wb['spine_02']+Wb['spine_03']+Wb['pelvis']+Wb['neck_01']*p.get('neck_w',0.0),0,1)
    arm=np.clip(sum(Wb[k] for k in Wb if any(a in k for a in ('upperarm','lowerarm','hand','fingers'))),0,1)
    g=tw*(1-arm); fc=p.get('fc',2.5); D=np.zeros_like(V)
    XS=globals().get('_XS'); XS=V if XS is None else XS     # pre-smoothed coordinates: breadth/depth scaled from the primary form, not the local bumps
    # profile retarget: per-height back / front / side extremes of the primary form pulled toward a straight line between two anchor heights
    core=(tw>0.5)&(arm<0.05)
    for key,col,sgn in (('back_line',1,-1),('front_line',1,1),('side_line',0,1)):
        if key not in p: continue
        z0,z1,alpha=p[key][:3]; xw=p[key][3] if len(p[key])>3 else 3.0; zz=np.arange(z0,z1+0.5,1.0); ext=[]
        for zc in zz:
            m=core&(np.abs(XS[:,2]-zc)<0.6)&((np.abs(XS[:,0])<xw) if col==1 else True)
            v=XS[m,col]
            ext.append(np.nan if len(v)==0 else ((v.max() if sgn>0 else v.min()) if col==1 else np.abs(XS[m,0]).max()))
        ext=np.array(ext); ok=~np.isnan(ext); ext=np.interp(zz,zz[ok],ext[ok]); ref=fc if col==1 else 0.0
        line=ext[0]+(ext[-1]-ext[0])*(zz-z0)/(z1-z0)
        tgt=ext+alpha*(line-ext); r=(tgt-ref)/(ext-ref)
        r=np.convolve(np.r_[np.full(3,r[0]),r,np.full(3,r[-1])],np.ones(7)/7,'valid')
        rz=np.interp(V[:,2],zz,r,left=1,right=1); rz=1+(rz-1)*ss((V[:,2]-z0)/4)*ss((z1-V[:,2])/4)
        if key=='back_line': kb=kb*rz
        elif key=='front_line': kf=kf*rz
        else: kx=kx*rz
    D[:,0]=g*(kx-1)*XS[:,0]; df=XS[:,1]-fc; D[:,1]=g*np.where(df>0,kf-1,kb-1)*df
    return D
def masses(V, N, lst):
    """broad anisotropic soft-tissue masses along the normal: [x,f,z,sx,sf,sz,amp], mirrored when x != 0"""
    D=np.zeros_like(V)
    for x_,f_,z_,sx,sf,sz,am in lst:
        for sg in ((1,-1) if abs(x_)>1e-6 else (1,)):
            q=(V-np.array([sg*x_,f_,z_]))/np.array([sx,sf,sz]); D+=(am*np.exp(-0.5*(q*q).sum(1)))[:,None]*N
    return D
def limb_profile(V, Wb, prof):
    """radial breadth profile per bone: {'thigh':[[t,k],...]} applied to both sides; displacement = sum_b w_b (k_b(t)-1) * radial_b"""
    D=np.zeros_like(V); med=float(prof.get('_thigh_medial',1.0))
    for b,cp in prof.items():
        if b.startswith('_'): continue
        cp=np.array(cp,float)
        for s in ('l','r') if b not in ('neck_01','spine_02','spine_03') else ('',):
            k=b+('_'+s if s else ''); h=jh(k); t=jt(k); w=Wb[k] if k in Wb else Wb[b]
            XL=globals().get('_XSL'); tt,tc,o,d=seg_param(V if XL is None else XL,h,t)
            if k=='neck_01':   # spatial neck mask (the neck vertex-group edge is too sharp for a breadth change)
                z=V[:,2]; w=ss((z-float(prof.get('_neck_z0',174)))/float(prof.get('_neck_ramp',7)))*(1-ss((z-float(prof.get('_neck_top',191)))/5))*(1-ss((d-float(prof.get('_neck_r',7.5)))/float(prof.get('_neck_rr',3))))*(1-np.clip(Wb['ears'],0,1))
            kk=_pchip(cp[:,0],cp[:,1],tc) if prof.get('_pchip') else np.interp(tc,cp[:,0],cp[:,1])
            if cp.shape[1]>2:      # anisotropic: column 2 = antero-posterior (f-axis) factor
                ka=_pchip(cp[:,0],cp[:,2],tc) if prof.get('_pchip') else np.interp(tc,cp[:,0],cp[:,2]); oap=np.zeros_like(o); oap[:,1]=o[:,1]; olat=o-oap
                if b=='thigh' and med!=1.0:   # medial side of the thigh widened less (crotch clearance)
                    sg=np.sign(h[0])
                    if prof.get('_pchip'): c_=np.clip(-sg*o[:,0]/(np.linalg.norm(o,axis=1)+1e-9),0,1); olat=olat*(1-(1-med)*ss(c_))[:,None]
                    else: olat=olat*np.where(olat[:,0]*sg<0,med,1.0)[:,None]
                D+=(w*(kk-1))[:,None]*olat+(w*(ka-1))[:,None]*oap
            else:
                D+=(w*(kk-1))[:,None]*o
    return D
def torso_scale(V, Wb, kx, kf, z0, z1):
    """anisotropic trunk breadth/depth about the spine line between z0 and z1 (smooth ends)"""
    tw=Wb['spine_01']+Wb['spine_02']+Wb['spine_03']+0.5*Wb['pelvis']
    sp_=0.5*(jh('spine_02')+jh('spine_03')); z=V[:,2]
    g=tw*ss((z-z0)/6)*ss((z1-z)/6)
    D=np.zeros_like(V); D[:,0]=g*(kx-1)*(V[:,0]-0); D[:,1]=g*(kf-1)*(V[:,1]-sp_[1])
    return D
def arm_shift(V, Wb, sh):
    """lateral shift of the whole arm chain (clavicle lengthening): wider shoulders and arm-trunk clearance"""
    D=np.zeros_like(V)
    for s,sg in (('l',1),('r',-1)):
        w=Wb['upperarm_'+s]+Wb['lowerarm_'+s]+Wb['hand_'+s]+Wb['fingers_'+s]+0.5*Wb['clavicle_'+s]
        D[:,0]+=sg*sh*np.clip(w,0,1)
    return D
def body_delta(V, Wb, N, p):
    D=np.zeros_like(V)
    if p.get('arm_shift'): D+=arm_shift(V,Wb,p['arm_shift'])
    if 'profile' in p: D+=limb_profile(V,Wb,p['profile'])
    if 'profile_extra' in p: D+=limb_profile(V,Wb,p['profile_extra'])     # un-low-passed limb increment (thin limbs lose most of a low-passed radial delta)
    if 'torso' in p: D+=torso_scale(V,Wb,*p['torso'])
    if 'trunk_field' in p: D+=trunk_field(V,Wb,p['trunk_field'])
    if 'masses' in p: D+=masses(V,N,p['masses'])
    for zz in p.get('trunk_zones',[]):     # anisotropic trunk bands about (x=0, f=fc); optional separate back factor
        z0,z1,kx,kf,fc,rmp=zz[:6]; kb=zz[6] if len(zz)>6 else kf
        tw=np.clip(Wb['spine_01']+Wb['spine_02']+Wb['spine_03']+Wb['pelvis']+0.6*(Wb['thigh_l']+Wb['thigh_r'])*(V[:,2]>z0),0,1)
        arm=np.clip(sum(Wb[k] for k in Wb if any(a in k for a in ('upperarm','lowerarm','hand','fingers'))),0,1)
        g=tw*(1-arm)*ss((V[:,2]-z0)/rmp)*ss((z1-V[:,2])/rmp)
        D[:,0]+=g*(kx-1)*V[:,0]; df=V[:,1]-fc; D[:,1]+=g*np.where(df>0,kf-1,kb-1)*df
    if 'hand' in p:
        for s in 'lr': D+=hand_map(V,Wb,s,p['hand'])
    if 'foot' in p:
        for s in 'lr': D+=foot_map(V,Wb,s,p['foot'],N)
    if 'relief' in p:
        L=landmarks(); pr=p['relief']
        D+=bumps(V,N,[(L[k],sig,amp) for k,(sig,amp) in pr['bumps'].items()])
        if 'clavicle' in pr:
            sig,amp=pr['clavicle']
            for s,sg in (('l',1),('r',-1)):
                h=jh('clavicle_'+s)+np.array([sg*2.5,2.0,0.5]); t=jt('clavicle_'+s)+np.array([-sg*0.5,1.0,1.0])
                D+=seg_ridge(V,N,h,t,sig,amp,(V[:,2]>h[2]-5)*(V[:,1]>-2.0))
        for c in pr.get('extra',[]):        # explicit [x,f,z,sigma,amp]; mirrored when x != 0
            x_,f_,z_,sg,am=c
            if abs(x_)<1e-6: D+=(am*np.exp(-0.5*(np.linalg.norm(V-np.array([0,f_,z_]),axis=1)/sg)**2))[:,None]*N
            else: D+=bumps(V,N,[((x_,f_,z_),sg,am)])
        if 'shin' in pr:
            sig,amp=pr['shin']
            for s in 'lr':
                h=jh('calf_'+s)+np.array([0,4.0,-7.0]); t=jt('calf_'+s)+np.array([0,3.5,8.0])
                D+=seg_ridge(V,N,h,t,sig,amp,(V[:,1]>h[1]-4.5).astype(float))
    return D
def new_joints(p):
    """rig joints after the identity edit (arm chain shifted, hands re-swept and scaled, toe tips moved); all others unchanged."""
    J2={k:[list(map(float,v[0])),list(map(float,v[1]))] for k,v in J.items()}
    sh=p.get('arm_shift',0.0)
    if 'hand' in p:
        hp=p['hand']
        for s in 'lr':
            w=jh('hand_'+s); sc=hp['hand_scale']; S=lambda X: (w+sc*(np.asarray(X)-w)).tolist()
            J2['hand_'+s]=[S(jh('hand_'+s)),S(jt('hand_'+s))]
            for f in FING:
                nh=jh('%s_01_%s'%(f,s)).copy(); ext=hp['finger_elong']*(1.0 if f!='thumb' else 0.6)
                pass
                for i in (1,2,3):
                    k='%s_0%d_%s'%(f,i,s); a=jt(k)-jh(k); nt=nh+a*(1+ext)
                    J2[k]=[S(nh),S(nt)]
                    if i<3: nh=nh+(jh('%s_0%d_%s'%(f,i+1,s))-jh(k))*(1+ext)
    if sh:
        for s_,sg in (('l',1),('r',-1)):
            for k in list(J2):
                if k.endswith('_'+s_) and any(a in k for a in ('upperarm','lowerarm','hand','thumb','index','middle','ring','pinky')):
                    J2[k]=[[J2[k][0][0]+sg*sh,J2[k][0][1],J2[k][0][2]],[J2[k][1][0]+sg*sh,J2[k][1][1],J2[k][1][2]]]
            k='clavicle_'+s_; J2[k][1]=[J2[k][1][0]+sg*sh,J2[k][1][1],J2[k][1][2]]
    if 'foot' in p:
        fp=p['foot']
        for s in 'lr':
            b0=jh('ball_'+s); t=jt('ball_'+s).copy(); t[1]+=(t[1]-(b0[1]-1.0))*fp['toe_elong']; J2['ball_'+s]=[b0.tolist(),t.tolist()]
    return J2
