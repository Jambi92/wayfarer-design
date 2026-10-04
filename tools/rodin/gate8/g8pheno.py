# Gate 8: inherited pigmentation / pattern / material phenotype -> per-vertex linear colour + material channels.
# Colour is computed from anatomical fields (g8fields.py), never painted: patterns live in girth-normalized body/limb
# coordinates (so elements scale with the anatomy and continue trunk -> tail), are optionally quantized to the Gate 7 scale
# cells, and fade (not stop) across the ventral field. Families, values and roughness are DIAGNOSTIC first-pass choices.
import numpy as np
EYES=[np.array([3.56,10.31,183.47]),np.array([-3.56,10.31,183.47])]; ER=1.46; TYMP=[np.array([6.11,-1.38,181.82]),np.array([-6.11,-1.38,181.82])]
def lin(c): c=np.asarray(c,float); return np.where(c<=0.04045,c/12.92,((c+0.055)/1.055)**2.4)
def _h(ix,iy,iz,seed):
    h=(ix.astype(np.int64)*73856093)^(iy.astype(np.int64)*19349663)^(iz.astype(np.int64)*83492791)^(seed*2654435761)
    h=(h^(h>>13))*1274126177; h=h^(h>>16); return (h&0xFFFFFF)/float(0xFFFFFF)
def vnoise(P,seed=0):
    i=np.floor(P).astype(np.int64); t=P-i; t=t*t*(3-2*t); out=0
    for dx in (0,1):
        for dy in (0,1):
            for dz in (0,1):
                w=(t[:,0] if dx else 1-t[:,0])*(t[:,1] if dy else 1-t[:,1])*(t[:,2] if dz else 1-t[:,2])
                out=out+w*_h(i[:,0]+dx,i[:,1]+dy,i[:,2]+dz,seed)
    return out
def fbm(P,seed=0,oct=4,lac=2.03,gain=0.5):
    a=1.0; s=0; tot=0
    for o in range(oct): s=s+a*vnoise(P*(lac**o),seed+17*o); tot+=a; a*=gain
    return s/tot
def ss(e0,e1,x): t=np.clip((x-e0)/(e1-e0),0,1); return t*t*(3-2*t)
def hashcell(c,seed): return _h(c,c*7+3,c*13+5,seed)
def seg_d(P,a,b):
    ab=b-a; t=np.clip(((P-a)@ab)/(ab@ab),0,1); return np.linalg.norm(P-(a+t[:,None]*ab),axis=1),t
def pattern(Fd,V,ph):
    """returns secondary-pigment mask m in [0,1] (per vertex, before cell quantization)"""
    fam=ph['pattern']; n=len(V); S=Fd['S'].astype(float); TH=Fd['TH'].astype(float); G=np.maximum(Fd['GIR'].astype(float),1.5)
    LW=Fd['LW'].astype(float); LT=Fd['LT'].astype(float); LG=np.maximum(Fd['LG'].astype(float),1.0); LTH=Fd['LTH'].astype(float); LID=Fd['LID']
    sc=ph.get('scale',1.0); asym=ph.get('asym',0.15); seed=ph.get('seed',1)
    # girth-normalized axial phase (integral of ds / girth) so elements shrink with the tail and the neck
    st=np.unique(np.round(S*2).astype(int)); Gs=np.zeros(st.max()+2); cnt=np.zeros_like(Gs)
    np.add.at(Gs,np.round(S*2).astype(int),G); np.add.at(cnt,np.round(S*2).astype(int),1); okk=cnt>0
    Gs=np.interp(np.arange(len(Gs)),np.where(okk)[0],Gs[okk]/cnt[okk]); PHs=np.concatenate([[0],np.cumsum(0.5/Gs)])[:-1]
    PH=PHs[np.round(S*2).astype(int)]*12.0                 # ~cm at a 12 cm reference girth
    G0=12.0/sc
    qs=np.stack([PH/sc,G0*np.cos(TH)/2.2,G0*np.abs(np.sin(TH))/2.2],1)            # symmetric body coordinates
    qa=np.stack([PH/sc,G0*np.cos(TH)/2.2,G0*np.sin(TH)/2.2],1)                    # asymmetric
    lofs=np.where(LID<=2,400.0,800.0)[:,None]
    LPH=LT/LG*4.0
    ql=np.stack([LPH/sc,4.5/sc*np.cos(LTH),4.5/sc*np.abs(np.sin(LTH))],1)+lofs*[1,0,0]
    def mix(fn):                                  # evaluate a pattern function on body and limb coordinates, blend smoothly
        b=fn(qs,qa,TH,'body'); l=fn(ql,ql,LTH,'limb') if LW.any() else 0; return b*(1-LW)+l*LW
    dorsal=lambda th: ss(-0.25,0.75,np.cos(th))   # 1 dorsal .. 0 ventral
    lateral=lambda th: ss(0.35,0.95,np.abs(np.sin(th)))
    def noisy(q,qa_,f,sd):
        a=fbm(q*f,seed+sd); b=fbm(qa_*f,seed+sd+91); return a*(1-asym)+b*asym
    if fam=='uniform':
        m=mix(lambda q,qa_,th,k: 0.25*noisy(q,qa_,0.08,1))
    elif fam=='mottled':
        m=mix(lambda q,qa_,th,k: ss(0.45,0.58,noisy(q,qa_,0.30,2))*(0.35+0.65*dorsal(th)))
    elif fam=='blotched':
        m=mix(lambda q,qa_,th,k: ss(0.56,0.64,noisy(q,qa_,0.16,3))*(lateral(th) if k=='body' else 0.6+0.4*np.abs(np.sin(th))))
    elif fam=='banded':
        def fb(q,qa_,th,k):
            p=q[:,0]*(0.16 if k=='body' else 0.075); band=ss(0.30,0.55,0.5+0.5*np.cos(2*np.pi*p+0.4*(noisy(q,qa_,0.1,4)-0.5)))
            return band*(0.25+0.75*dorsal(th)) if k=='body' else band*(0.5+0.5*np.cos(th)**2)
        m=mix(fb)
    elif fam=='broken_banded':
        def fbb(q,qa_,th,k):
            p=q[:,0]*(0.16 if k=='body' else 0.075); band=ss(0.30,0.55,0.5+0.5*np.cos(2*np.pi*p+0.6*(noisy(q,qa_,0.1,5)-0.5)))
            brk=ss(0.42,0.52,noisy(q,qa_,0.22,6)); return band*brk*((0.25+0.75*dorsal(th)) if k=='body' else 1.0)
        m=mix(fbb)
    elif fam=='axial':
        def fa(q,qa_,th,k):
            if k=='body':
                c=0.95+0.06*(noisy(q,qa_,0.12,7)-0.5)
                return np.maximum(ss(0.30,0.18,np.abs(np.abs(th)-c)),0.7*ss(0.16,0.08,np.abs(th)))
            return ss(0.35,0.2,np.abs(np.abs(th)-0.2))*0.8
        m=mix(fa)
    elif fam=='speckled':
        m=np.zeros(n)                              # cell-quantized below
    elif fam=='regional':                          # regional contrast fields: dark dorsal saddle field, dark distal limbs, light flanks
        m=mix(lambda q,qa_,th,k: ss(0.15,0.75,np.cos(th))*(0.8+0.2*noisy(q,qa_,0.1,8)) if k=='body' else ss(0.2,0.9,Fd['LTN'].astype(float)))
    elif fam=='mixed':
        def fm(q,qa_,th,k):
            bl=ss(0.55,0.63,noisy(q,qa_,0.15,9))*(0.4+0.6*dorsal(th))
            p=q[:,0]*(0.16 if k=='body' else 0.075); band=ss(0.35,0.6,0.5+0.5*np.cos(2*np.pi*p+0.8*(noisy(q,qa_,0.1,10)-0.5)))*ss(0.45,0.55,noisy(q,qa_,0.2,11))
            return np.maximum(bl,0.8*band*(0.3+0.7*dorsal(th)))
        m=mix(fm)
    else: raise ValueError(fam)
    return np.clip(m,0,1)
def phenotype(Fd,V,ph,state=None):
    """ph: dict of inherited phenotype parameters. returns C (n,3 linear rgb), M (n,3: roughness, subsurface, coat)"""
    state=state or {}; n=len(V); FAM=Fd['FAM']; CV=Fd['CELLV']; TH=Fd['TH'].astype(float); EDGE=Fd['EDGE'].astype(float)
    LW=Fd['LW'].astype(float); LTN=Fd['LTN'].astype(float); LTH=Fd['LTH'].astype(float); S=Fd['S'].astype(float); KD=Fd['KD'].astype(float)
    seed=ph.get('seed',1); x,f,u=V.T
    P1=lin(ph['primary']); P2=lin(ph['secondary']); PV=lin(ph.get('ventral',ph['primary']))
    m=pattern(Fd,V,ph)
    soft=ph.get('soft',0.5); mc=m[CV]; m=mc*(1-soft)+m*soft                      # scale-quantized vs soft pattern edges
    if ph['pattern'] in ('speckled','mixed') or ph.get('speckle',0)>0:
        dens=ph.get('speckle',0.10 if ph['pattern']=='speckled' else 0.04)
        hc=hashcell(CV,seed+5); m=np.maximum(m,(hc<dens).astype(float)*ph.get('speck_c',0.9))
    head=(u>170)&(np.abs(x)<12)&(f>-14)&((f>-5)|(u>177))
    hw=head.astype(float)
    if ph.get('fail')=='face_noise': hw=hw*0
    m*=1-ph.get('face_soft',0.5)*hw*(1+0.4*ss(10,16,f)).clip(0,1/max(ph.get('face_soft',0.5),1e-3))                                            # face: lower pattern contrast (planes first)
    fail=ph.get('fail')
    import sys as _s; _s.path.insert(0,'/tmp/claude-0/rodin/g1'); import g7geo as _G
    AX=np.load('/tmp/claude-0/rodin/g8/axis.npy'); S_root=0.5*int(np.argmax(AX[:,1]>-27))
    if fail=='paint_mask': m=((u/14.0)%1.0<0.35).astype(float)                         # REJECT: world-plane stripes ignoring anatomy
    if fail=='joint_rings':                                                               # REJECT: dark ring at every joint
        jp=[np.array(A[k]) for A in _G.ARM.values() for k in ('E','W')]+[np.array(L[k]) for L in _G.LEG.values() for k in ('K','A')]+[AX[int(S_root*2)]]
        m=np.zeros(n)
        for p in jp: m=np.maximum(m,(np.linalg.norm(V-p,axis=1)<6.0).astype(float))
    if fail=='tail_seam': m=np.where(S<S_root,0.5+0.5*np.sign(np.cos(2*np.pi*S/9.0)),0.0)    # REJECT: tail-only pattern starting at the root
    if fail=='face_noise':                                                                 # REJECT: high-contrast speckle over the face
        hd_=(u>170)&(np.abs(x)<12)&(f>-14)&((f>-5)|(u>177)); m=np.where(hd_,(hashcell(CV,seed+3)<0.5).astype(float),m); ph=dict(ph,face_soft=0.0)
    con=ph.get('contrast',0.7); col=P1*(1-con*m)[:,None]+P2*(con*m)[:,None]
    # dorsal/ventral value relationship (smooth countershading, pattern fades but continues across the ventral field)
    vent=ss(-0.05,-0.75,np.cos(TH))*(1-LW)+LW*ss(-0.2,-0.85,np.cos(LTH))*0.6
    cs=ph.get('cs',0.35); col=col*(1-cs*vent)[:,None]+PV*(cs*vent)[:,None]
    if fail in ('pale_belly','dragon'):                                                   # REJECT: hard-edged cartoon belly block
        hb=((np.cos(TH)<-0.35)&(LW<0.5)); col[hb]=lin(ph.get('belly',(0.93,0.90,0.80)))
    dd=ph.get('dorsal_dark',0.10); col*= (1-dd*ss(0.3,1.0,np.cos(TH))*(1-LW))[:,None]
    # facial accents (follow planes): postorbital stripe eye -> tympanic recess; lighter labial/gular margin
    fa=ph.get('face_accent',0.0)
    if fa:
        acc=np.zeros(n)
        for e,t in zip(EYES,TYMP):
            d,tt=seg_d(V,e+(t-e)*0.18,t); acc=np.maximum(acc,ss(0.95,0.55,d)*(tt<0.98))
        col=col*(1-0.55*fa*acc)[:,None]+lin(ph['secondary'])[None,:]*0.55*fa*acc[:,None]
    # distal variation (hands, feet, distal tail)
    dv=ph.get('distal',0.0); tailtip=ss(60,0,S)                                   # S=0 at tail tip
    dist=np.maximum(LW*ss(0.62,1.0,LTN),tailtip*0.7); col*=(1-dv*dist)[:,None]
    # natural per-scale variation (value + slight hue), not a multicoloured mosaic
    j=ph.get('jitter',0.07); hc=hashcell(CV,seed+11)-0.5; col*=(1+j*hc)[:,None]
    sj=ph.get('sat_jitter',0.04); grey=col.mean(1,keepdims=True); col=grey+(col-grey)*(1+sj*(hashcell(CV,seed+13)-0.5)*4)[:,None]
    # interstitial skin between scales: slightly lighter, less saturated
    e=ss(0.35,0.95,EDGE); grey=col.mean(1,keepdims=True); col=col*(1-0.25*e)[:,None]+(grey*1.18)*(0.25*e)[:,None]
    # contact fields: slightly paler, desaturated
    ct=(FAM==5).astype(float); grey=col.mean(1,keepdims=True); col=col*(1-0.35*ct)[:,None]+(grey*1.12)*(0.35*ct)[:,None]
    # ---- material channels
    rb=ph.get('rough',0.55)
    rough=np.full(n,rb); rough[FAM==2]+=0.05; rough[FAM==3]+=0.02; rough[FAM==4]+=0.04; rough[FAM==5]=rb+0.18
    rough+=0.15*e; rough+=0.03*(hashcell(CV,seed+17)-0.5)
    sss=np.zeros(n); coat=np.zeros(n)
    # ---- keratin (claws + display): own value/roughness, growth banding, translucent tips
    ker=FAM==6
    if ker.any():
        K=lin(ph.get('keratin',(0.42,0.36,0.28))); rel=ph.get('ker_rel',0.25)
        tip=ss(0.15,2.2,KD[ker]); band=1+0.07*np.sin(2*np.pi*KD[ker]/0.32)
        kc=(K*(1-rel)+col[ker].mean(0)*rel)[None,:]*band[:,None]
        kc=kc*(1-0.45*tip)[:,None]+lin(ph.get('ker_tip',(0.80,0.74,0.62)))[None,:]*(0.45*tip)[:,None]
        col[ker]=kc; rough[ker]=0.40-0.08*tip; sss[ker]=0.15+0.25*tip
    # ---- eyes: iris (radial fibres), vertical pupil, cornea glint, nictitating membrane state
    eye=FAM==7
    if eye.any():
        I1=lin(ph.get('iris',(0.62,0.45,0.15))); I2=lin(ph.get('iris2',(0.30,0.20,0.08)))
        ext=state.get('membrane',0.0)
        for k,c in enumerate(EYES):
            sgn=1 if c[0]>0 else -1; yaw=np.radians(38.0)
            idx=np.where(eye&(np.sign(x)==sgn))[0]
            if len(idx)==0: continue
            Q=V[idx]-c; q=Q/np.linalg.norm(Q,axis=1,keepdims=True)
            ax_=q.mean(0); ax_/=np.linalg.norm(ax_)
            up=np.array([0,0,1.0]); side=np.cross(up,ax_); side/=np.linalg.norm(side)
            cosg=q@ax_; ps=q@side; pu=q@up; ang=np.arctan2(pu,ps)
            ant=np.array([0,1.0,0])-ax_*(ax_@np.array([0,1.0,0])); ant/=np.linalg.norm(ant)+1e-9; pa=q@ant
            rr=np.sqrt(np.maximum(1-cosg**2,0))
            fib=fbm(np.stack([ang*6,rr*8,np.zeros_like(rr)+k*50],1),seed+31,3)
            ic=I1[None,:]*(1-fib[:,None]*0.6)+I2[None,:]*(fib[:,None]*0.6)
            ic*= (1-0.55*ss(0.55,0.75,rr))[:,None]                                  # limbal darkening
            pup=np.exp(-(ps/0.085)**4-(pu/0.52)**4)*(cosg>0.5); ic=ic*(1-pup)[:,None]+np.array([0.01,0.01,0.012])*pup[:,None]
            per=ss(0.80,0.92,rr); ic=ic*(1-per)[:,None]+lin((0.35,0.30,0.24))*per[:,None]
            fold=np.exp(-((pa-0.60)/0.12)**2)*(cosg>0.1); thr=0.62-1.6*ext; memb=np.clip(fold*0.5+(ext>0)*ss(thr,thr+0.07,pa),0,1)          # membrane sweeps from the rostral canthus
            mcol=lin((0.70,0.67,0.60)); a_=0.55*memb; ic=ic*(1-a_)[:,None]+mcol*a_[:,None]
            col[idx]=ic; rough[idx]=0.06+0.25*memb; coat[idx]=1.0; sss[idx]=0.2*memb
    col=np.clip(col,0,1); M=np.stack([np.clip(rough,0.03,1),np.clip(sss,0,1),coat],1)
    return col.astype(np.float32),M.astype(np.float32)
