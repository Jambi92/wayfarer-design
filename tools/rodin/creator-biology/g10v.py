# Gate 6 pass 2: posterior pelvic volume + proximal tail re-curve (+ head scale, limb mass redistribution) on Gate 6 pass 1.
import numpy as np, sys
sys.path.insert(0,'/tmp/claude-0/rb')
import g9
from g1 import ss, smin, smax
import wf_saurin_body8 as B8, wf_saurin_head64v as H64
B8.H=H64          # head-scale test wrapper (HEAD_SCALE env, default 1.06) around the TS6.3 skull
# ---------------- proximal free-tail re-curve: exact-length bend about the tail root (rotation in the F-U plane)
PIV=np.array([-26.0,92.0]); TH=np.radians(float(__import__('os').environ.get('TAIL_DEG','22')))
def tail_unwarp(X,F,U):
    """inverse warp: world point -> Gate 6 pass-1 coordinates (rotation angle depends only on radius => exactly invertible)"""
    dF=F-PIV[0]; dU=U-PIV[1]; r=np.sqrt(dF*dF+dU*dU)
    th=TH*ss(3.0,62.0,r)*ss(2.0,10.0,PIV[0]-F)          # pass 3: long ramp (continuous curvature, no kink); nothing forward of F -28 moves
    c,s=np.cos(-th),np.sin(-th)
    F0=PIV[0]+c*dF+s*dU; U0=PIV[1]-s*dF+c*dU
    return X,F0,U0
# ---------------- posterior pelvic volume: one continuous sacral-caudal wedge (no paired lobes, no cleft)
SW=[(-6.0,15.0,95.0,10.5),(-16.0,14.5,94.0,11.0),(-26.0,13.5,92.5,11.5),(-34.0,11.2,90.0,11.8),(-44.0,9.0,87.5,11.2),(-56.0,6.8,85.0,10.0)]  # F, half-width, centre U, half-height
def wedge(X,F,U):
    fs=[s[0] for s in SW][::-1]; Fq=np.clip(F,fs[0],fs[-1])
    hw=np.interp(Fq,fs,[s[1] for s in SW][::-1]); cu=np.interp(Fq,fs,[s[2] for s in SW][::-1]); hh=np.interp(Fq,fs,[s[3] for s in SW][::-1])
    hb=hh; lo=np.interp(F,[-56.0,-36.0,-24.0,-6.0],[1.0,0.9,0.5,0.4])
    hh=hh*(lo+(0.85-lo)*ss(-2.0,2.0,U-cu))                # flatter dorsal platform; ventral half stays above the pelvic floor (continuous blend)
    n=2.6; q=(np.abs(X/hw)**n+np.abs((U-cu)/hh)**n)**(1/n)
    cap=np.where(F>-6.0,(F+6.0)/4.0,np.where(F<-56.0,(-56.0-F)/10.0,0.0))
    return (np.sqrt(q*q+cap*cap)-1)*np.minimum(hw,0.6*hb)
def pelvis_tail_base(X,F,U):
    Xw,Fw,Uw=tail_unwarp(X,F,U)
    e=g9.field(Xw,Fw,Uw)
    w=wedge(X,F,U)-0.6                                    # sits slightly inside: it fills, it does not inflate
    return smin(e,w,5.0)
# pass 3: load paths laid ON the sacral-caudal volume so it reads as pelvic architecture (ilium -> sacrum -> tail; tail -> femur)
from g9z import SPath, rss
CLOSURE=__import__('os').environ.get('CLOSURE','0')=='1'
SP=[]
for sg in (-1,1):
    if CLOSURE:   # closure: iliosacral band starts on the posterior ilium (its old start projected onto the flank and left a hip nub)
        SP+=[SPath(pelvis_tail_base,[(sg*11.5,-11,102),(sg*9,-19,99.5),(sg*5,-32,96),(sg*3,-46,92)],[4.2,4.2,3.4,2.4],[0.7,1.0,0.7,0.3],600+sg,edge=0.25,fade=(0.32,0.25))]
    else:
        SP+=[SPath(pelvis_tail_base,[(sg*14,-4,101),(sg*9.5,-17,99),(sg*5,-32,96),(sg*3,-46,92)],[4.6,4.2,3.4,2.4],[0.8,1.0,0.7,0.3],600+sg,edge=0.25)]          # iliosacral -> dorsal caudal
    if CLOSURE:   # Gate 6 closure: caudofemoral mass redistributed into two longer, lower, tensioned slips (no paired rounded rear masses)
        SP+=[SPath(pelvis_tail_base,[(sg*4.5,-50,87),(sg*9,-32,86),(sg*13,-16,81),(sg*15,-4,72)],[3.0,3.4,3.2,2.3],[0.45,0.62,0.58,0.25],610+sg,edge=0.4),   # caudofemoral longus, dorsal slip
             SPath(pelvis_tail_base,[(sg*4,-47,81),(sg*8.5,-29,80),(sg*12.5,-15,76),(sg*14.5,-4,67)],[2.6,3.0,2.8,2.0],[0.38,0.52,0.48,0.2],615+sg,edge=0.4), # caudofemoral longus, ventral slip
             SPath(pelvis_tail_base,[(sg*3.5,-38,79),(sg*7.5,-24,78),(sg*11,-12,73)],[2.3,2.6,2.0],[0.3,0.38,0.18],620+sg,edge=0.4),                             # caudofemoral brevis, flattened
             SPath(pelvis_tail_base,[(sg*13,-9,96),(sg*14.5,-13,92),(sg*15.5,-16,87)],[2.8,3.0,2.2],[0.25,0.4,0.1],630+sg,edge=0.35,fade=(0.4,0.5))]           # iliofemoral rim: starts behind the hip-stabiliser origin (their overlapping fade-ins made the hip nub)
    else:
        SP+=[SPath(pelvis_tail_base,[(sg*4.5,-46,84),(sg*9,-30,84),(sg*13,-15,79),(sg*15,-4,70)],[4.0,5.0,4.8,3.2],[0.7,1.1,1.0,0.4],610+sg,edge=0.2),
             SPath(pelvis_tail_base,[(sg*3.5,-38,80),(sg*7.5,-24,79),(sg*11,-12,74)],[3.0,3.4,2.6],[0.5,0.7,0.35],620+sg,edge=0.25),
             SPath(pelvis_tail_base,[(sg*12,-2,96),(sg*14.5,-10,92),(sg*15.5,-14,86)],[3.0,3.2,2.6],[0.5,0.6,0.3],630+sg,edge=0.3)]
SP.append(SPath(pelvis_tail_base,[(0,-6,104),(0,-24,101.5),(0,-44,97),(0,-62,92)],[2.2,2.6,2.4,1.8],[0.35,0.45,0.4,0.2],640,edge=0.35,fade=(0.25,0.3)))  # low sacral/caudal neural-spine line
NUBS=[((16.7,-13.9,91.5),(4.2,4.2,4.2),0.33),((-17.2,-14.4,91.5),(4.2,4.2,4.2),0.3)]   # closure: hip nubs (measured; path origins exposed at the narrowed sacral edge)
def pelvis_tail(X,F,U):
    e=pelvis_tail_base(X,F,U)
    if CLOSURE:
        from g9z import ell_w
        for c,r,amp in NUBS: e=e+amp*ell_w(X,F,U,c,r,1.0)
    m=(np.abs(X)<26)&(F<6)&(F>-80)&(U>58)&(U<112)
    if m.any(): e[m]=e[m]-rss(SP,np.stack([X[m],F[m],U[m]],-1))
    return e
# ---------------- upper-arm / thigh mass redistribution: partial mix toward a 3.5 cm low-pass of the Gate 6 limb surface
# (removes the human biceps/triceps and quad belly read) with a small outward offset so girth/strength is kept
from g9z import LP, away_from_hands
from g9 import boxfade
def seg_w(X,F,U,A,B,r0,r1,t0,t1):
    A=np.asarray(A,float); B=np.asarray(B,float); v=B-A; Q=np.stack([X,F,U],-1)-A
    t=np.clip((Q@v)/(v@v),0,1); d=np.linalg.norm(Q-np.outer(t,v),axis=1)
    return (1-ss(r0,r1,d))*ss(t0,t0+0.15,t)*(1-ss(t1-0.15,t1,t))
LIMBS=[("armR",(12,44,-22,16,110,154),(23.0,-5.0,147.0),(28.8,-3.5,117.0),0.50,(11,14),(0.10,0.92)),
       ("armL",(-44,-12,-22,16,110,154),(-23.5,-6.0,147.0),(-30.5,-4.5,117.0),0.50,(11,14),(0.10,0.92)),
       ("thighR",(1,32,-18,22,56,98),(13.0,3.5,86.0),(15.2,3.0,62.0),0.45,(13,16),(0.12,0.88)),
       ("thighL",(-32,-1,-18,22,56,98),(-13.0,3.5,86.0),(-17.4,2.8,62.0),0.45,(13,16),(0.12,0.88))]
def limbs(e,X,F,U):
    for name,box,A,B,amt,(r0,r1),(t0,t1) in LIMBS:
        m=(X>box[0])&(X<box[1])&(F>box[2])&(F<box[3])&(U>box[4])&(U<box[5])
        if not m.any(): continue
        w=amt*seg_w(X[m],F[m],U[m],A,B,r0,r1,t0,t1)*boxfade(X[m],F[m],U[m],box)*away_from_hands(X[m],F[m],U[m])
        if name.startswith("thigh"): w=w*ss(6.0,9.0,np.abs(X[m]))          # keep the pelvic floor / tail root to the pelvis rebuild
        k=w>1e-4
        if not k.any(): continue
        ii=np.where(m)[0][k]; e[ii]=e[ii]*(1-w[k])+(LP(name,X[ii],F[ii],U[ii])-0.25)*w[k]
    return e
def field(X,F,U):
    X=np.asarray(X,float); F=np.asarray(F,float); U=np.asarray(U,float)
    return limbs(pelvis_tail(X,F,U),X,F,U)
B8.sdf=lambda X,F,U: field(X,F,U)
B8.BOX=(-47.0,47.0,-160.0,28.0,-1.0,192.0)
if __name__=="__main__":
    import time; t=time.time()
    if len(sys.argv)>3: B8.BOX=tuple(map(float,sys.argv[3].split(',')))
    v,f=B8.mesh(float(sys.argv[1]),log=lambda *a: None)
    np.savez_compressed(sys.argv[2],v=v,f=f); print("DONE",len(v),len(f),round(time.time()-t,1))
