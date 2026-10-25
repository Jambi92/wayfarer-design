# build_cage.py OUT.npz : authored quad cage (stage 1: axial + legs + arms, hands/feet capped)
import numpy as np, json, sys, os
sys.path.insert(0,'/tmp/claude-0/rt')
from common import *
from cage import *
V,F=load_src(); flab=np.load('/tmp/claude-0/rt/flab.npy'); L={k:np.array(v['p']) for k,v in json.load(open('/tmp/claude-0/rt/lm_src.json')).items()}
SN=Snapper(V,F,flab); C=Cage()
vlab=np.load('/tmp/claude-0/rt/vlab.npy')
KT=40; PA=6; KA=2*(PA+9); KL=32
Z_T=[117,120,123,126,129,132,135,138,141,144,147,150]+list(np.round(np.linspace(153,186,10),3))+[187.5,189]
Z_H=[190.5,192,193.5,195,196.5,198,199.5,201,202.5,204,205.5,207,208.5,210,211.5,213,214.5,216]
PORT_ROW0=12; PORT_ROWS=9
SJ=json.load(open('/tmp/claude-0/rt/shoulder.json'))
def axial_center(z):
    m=(np.abs(V[:,2]-z)<0.8)&(vlab==PID['axial']); q=V[m]
    return np.array([np.median(q[:,0]) if abs(np.median(q[:,0]))<1 else 0.0,0.5*(q[:,1].min()+q[:,1].max()),z])
th=angles_uniform(KT)
rings=[]
for zi,z in enumerate(Z_T+Z_H):
    c=axial_center(z); parts=['axial']
    P,ok=SN.ring(parts,c,np.array([0,0,1.0]),np.array([0,1.0,0]),th)
    if P is None: raise SystemExit('ring fail %s'%z)
    P=fill_misses(P,ok,c); rings.append(C.add(P))
    if 183<z<191: C.tag('neck_%g'%z,rings[-1])
# ---- under-jaw: the z-plane rings jump from the neck to the jaw edge; re-space the jaw rows of each column by surface
# arclength between the 187.5 neck ring and the 195 face ring (mouth columns excluded)
import igl as _igl
_ZA=Z_T+Z_H; _rows=[int(np.argmin(np.abs(np.array(_ZA)-z))) for z in (180.667,183.333,186,187.5,189,190.5,192,193.5,195)]
_ax=SN.sub(['axial'])
_pc=set()
for k in range(KT):
    if k in (37,38,39,0,1,2): continue
    rr=[r for r in _rows if (k not in _pc) or r>=PORT_ROW0+PORT_ROWS]
    P=np.array([C.V[rings[r][k]] for r in rr])
    D=np.vstack([P[j]+(P[j+1]-P[j])*t for j in range(len(P)-1) for t in np.linspace(0,1,12,endpoint=False)]+[P[-1:]])
    for _ in range(3):
        _,_,D=_igl.point_mesh_squared_distance(D,SN.V,_ax.faces)
    seg=np.linalg.norm(np.diff(D,axis=0),axis=1); cs=np.r_[0,np.cumsum(seg)]
    for j,r in enumerate(rr[1:-1],1):
        t=cs[-1]*j/(len(rr)-1); i=min(np.searchsorted(cs,t,side='right')-1,len(D)-2); u=(t-cs[i])/max(seg[i],1e-12)
        C.V[rings[r][k]]=D[i]+(D[i+1]-D[i])*u
# ---- arm-root port loops: section of the body by the arm-root plane, split into 4/9/4/9 edges ----
import trimesh as _tm
fullm=_tm.Trimesh(V,F,process=False)
PORT_COL={}; PORTLOOP={}
for s_,sg in (('l',1),('r',-1)):
    A=np.array(SJ[s_]['A']); n=np.array(SJ[s_]['n'])
    sec=fullm.section(plane_origin=A,plane_normal=n)
    best=None
    for e in sec.discrete:
        if e[:,2].max()<A[2]+10 or e[:,2].min()<A[2]-6: continue
        d=np.linalg.norm(e.mean(0)-A); 
        if best is None or d<best[0]: best=(d,e)
    e=best[1][:-1] if np.allclose(best[1][0],best[1][-1]) else best[1]
    # orientation: walk so that from the lowest point we go toward the front (+f) first
    lo=np.argmin(e[:,2]); e=np.roll(e,-lo,0)
    if e[1,1]<e[-1,1]: e=e[::-1]; e=np.roll(e,1,0)
    seg=np.linalg.norm(np.diff(np.vstack([e,e[:1]]),axis=0),axis=1); cs=np.r_[0,np.cumsum(seg)]; P_=cs[-1]
    hi=np.argmax(e[:,2]); s_hi=cs[hi]
    ab=P_*PA/KA
    # edges: bottom centred on the lowest point (arclength 0), top centred on the highest
    def at(t):
        t=t%P_; i=np.searchsorted(cs,t,side='right')-1; i=min(i,len(e)-1); u=(t-cs[i])/max(seg[i],1e-9); return e[i]+(e[(i+1)%len(e)]-e[i])*u
    BF=ab/2; TF=s_hi-ab/2; TB=s_hi+ab/2; BB=P_-ab/2
    bottom=[at(BB+(BF+P_-BB)*k/PA) for k in range(PA+1)]      # back->front through the lowest point
    front=[at(BF+(TF-BF)*k/9) for k in range(10)]         # bottom->top
    top=[at(TF+(TB-TF)*k/PA) for k in range(PA+1)]            # front->back over the top
    back=[at(TB+(BB-TB)*k/9) for k in range(10)]          # top->bottom
    PORTLOOP[s_]=(bottom,front,top,back)
    # columns: the torso ring at mid height; angle of the front and back edge mid points
    mid=PORT_ROW0+4; cz=np.array(C.V)[rings[mid]].mean(0)
    def ang(p): return np.arctan2(-(p[0]-cz[0]),p[1]-cz[1])%(2*np.pi)
    af=ang(front[4]); ab_=ang(back[5]); kf=int(round(af/(2*np.pi/KT)))%KT; kb=int(round(ab_/(2*np.pi/KT)))%KT
    lo_,hi_=sorted([kf,kb])
    if hi_-lo_>KT//2: lo_,hi_=hi_,lo_+KT
    # force a 4-column window centred between them
    cmid=(lo_+hi_)/2.0; c0=int(round(cmid-PA/2)); PORT_COL[s_]=(c0,c0+PA,kf,kb)
    print('port',s_,'front col',kf,'back col',kb,'window',c0,c0+4,'perimeter',round(P_,1))
# override torso ring vertices on the port boundary with loop points
for s_,(c0,c1,kf,kb) in PORT_COL.items():
    bottom,front,top,back=PORTLOOP[s_]; R0=PORT_ROW0; R1=R0+PORT_ROWS
    # decide which window column is the front one (the column nearer kf)
    cf,cb=(c1,c0) if ((c1-kf)%KT if True else 0) <= ((c0-kf)%KT) else (c0,c1)
    if abs(((c1-kf+KT//2)%KT)-KT//2) <= abs(((c0-kf+KT//2)%KT)-KT//2): cf,cb=c1,c0
    else: cf,cb=c0,c1
    step=1 if cf>cb else -1
    cols=[ (cb+step*k)%KT for k in range(PA+1)]     # back -> front
    for k,cc in enumerate(cols): C.V[rings[R0][cc]]=bottom[k]; C.V[rings[R1][cc]]=top[PA-k]
    for i in range(10): C.V[rings[R0+i][cf%KT]]=front[i]; C.V[rings[R1-i][cb%KT]]=back[i]
    PORT_COL[s_]=(min(c0,c1),max(c0,c1),cf%KT,cb%KT)
from ears import EAR_ROWS, EAR_COLS, build_ear
Zall=Z_T+Z_H; EAR_R=(Zall.index(EAR_ROWS[0]),Zall.index(EAR_ROWS[1]))
FACE_AT={}
# axial strips, skipping the arm-port windows
NR=len(rings)
for i in range(NR-1):
    for k in range(KT):
        inport=False
        for s_,(c0,c1,_a,_b) in PORT_COL.items():
            if PORT_ROW0<=i<PORT_ROW0+PORT_ROWS and (k-c0)%KT<(c1-c0): inport=True
        for s_,(c0,c1) in EAR_COLS.items():
            if EAR_R[0]<=i<EAR_R[1] and c0<=k<c1: inport=True
        if not inport: FACE_AT[(i,k)]=len(C.F); C.quad(rings[i][k],rings[i][(k+1)%KT],rings[i+1][(k+1)%KT],rings[i+1][k],'axial')
# crown cap 10x10 grid
top=rings[-1]; ctop=np.array(C.V)[top].mean(0)
def coons(G,i,j,R,Cc):
    Vv=np.array(C.V); u=j/Cc; v=i/R
    p= (1-v)*Vv[G[0,j]]+v*Vv[G[R,j]]+(1-u)*Vv[G[i,0]]+u*Vv[G[i,Cc]] \
       -((1-u)*(1-v)*Vv[G[0,0]]+u*(1-v)*Vv[G[0,Cc]]+(1-u)*v*Vv[G[R,0]]+u*v*Vv[G[R,Cc]])
    return p
def cap(ring,R,Cc,part,lift=None):
    G=-np.ones((R+1,Cc+1),int); k=0
    for j in range(Cc): G[0,j]=ring[k]; k+=1
    for i in range(R): G[i,Cc]=ring[k]; k+=1
    for j in range(Cc,0,-1): G[R,j]=ring[k]; k+=1
    for i in range(R,0,-1): G[i,0]=ring[k]; k+=1
    for i in range(1,R):
        for j in range(1,Cc):
            p=coons(G,i,j,R,Cc)
            if lift is not None: p=lift(p,i,j)
            G[i,j]=C.add([p])[0]
    for i in range(R):
        for j in range(Cc): C.quad(G[i,j],G[i,j+1],G[i+1,j+1],G[i+1,j],part)
    return G
# crown: ring of 40 -> 10x10; start the boundary walk at ring index 0 (front)
cap(top,10,10,'axial',lift=lambda p,i,j: p+np.array([0,0,1.5*np.sin(np.pi*i/10)*np.sin(np.pi*j/10)]))
import ears as _ears; _ears.SN_=SN
for s_ in 'lr': print('ear',s_,'K',build_ear(C,rings,EAR_R,s_,fullm))
# ---- legs from the crotch split ----
r0=rings[0]; Vv=np.array(C.V); Fp=Vv[r0[0]]; Bp=Vv[r0[20]]
# midsagittal crotch curve
sub=SN.sub(['axial','leg_l','leg_r']); s=sub.section(plane_origin=[0,0,0],plane_normal=[1.0,0,0])
pts=np.concatenate([e for e in s.discrete]); pts=pts[(pts[:,2]<Fp[2]+0.5)&(pts[:,1]<Fp[1]+1)&(pts[:,1]>Bp[1]-1)]
# order along f from front to back, keeping the lowest-z branch
fs=np.linspace(Fp[1],Bp[1],13)[1:-1]; chain=[]
for ff in fs:
    q=pts[np.abs(pts[:,1]-ff)<0.6]; chain.append(q[np.argmin(q[:,2])] if len(q) else np.array([0,ff,105.0]))
chain=C.add(chain)   # 11 points front->back
legs={}
Z_L=[112,108,104,100,96,92,88,84,80,76,73,71,69,66,63,60,57,54,51,48,46,44,42,40,38,36,34,32,30,28,26,24,22.5,21]
for s,sg in (('l',1),('r',-1)):
    half=[r0[0]]+([r0[k] for k in range(39,20,-1)] if s=='l' else [r0[k] for k in range(1,20)])+[r0[20]]
    first=half+chain[::-1]          # 32
    assert len(first)==KL
    prev=first; Vv=np.array(C.V); prevP=Vv[first]; C.tag('groin_split_'+s,first)
    for z in Z_L:
        m=(np.abs(V[:,2]-z)<0.8)&(vlab==PID['leg_'+s]); q=V[m]; c=np.array([np.median(q[:,0]),0.5*(q[:,1].min()+q[:,1].max()),z])
        a0=np.arctan2(-(prevP[:,0]-c[0]),prevP[:,1]-c[1])     # angle in basis a=+f, b=-x
        # blend toward uniform spacing keeping the phase of vertex 0
        u=a0[0]+np.unwrap(a0-a0[0]) if True else a0
        uni=a0[0]+2*np.pi*np.arange(KL)/KL*np.sign(np.unwrap(a0-a0[0])[KL//4]+1e-9)
        w=np.clip((112-z)/12,0,1); t=(1-w)*np.unwrap(a0)+w*uni
        if z<=104:
            P=advance_ring(SN,['leg_'+s],prevP,c,np.array([0,0,1.0]),mix=float(os.environ.get('LEGMIX','0.6')))
        else:
            P,ok=SN.ring(['leg_'+s],c,np.array([0,0,1.0]),np.array([0,1.0,0]),t)
            P=fill_misses(P,ok,c); P=arc_resample(P,float(np.clip((108-z)/8,0,1)))
        cur=C.add(P); C.strip(prev,cur,'leg_'+s); prev=cur; prevP=P
        C.tag(('knee_%s_%g' if 65<z<77 else 'hip_groin_%s_%g' if z>=100 else 'leg_%s_%g')%(s,z),cur)
    legs[s]=prev
# temporary ankle cap 14x2
from feet import build_foot
for s in 'lr': build_foot(C,SN,s,legs[s],np.array(C.V)[legs[s]],L)
# ---- arms through the ports (fan rings hinged at the armpit, then parallel rings) ----
arms={}
for s,sg in (('l',1),('r',-1)):
    c0,c1,cf,cb=PORT_COL[s]; R0=PORT_ROW0; R1=R0+PORT_ROWS
    step=1 if cf>cb or (cb-cf)>KT//2 else -1
    if (cf-cb)%KT==PA: step=1
    else: step=-1
    cols=[(cb+step*k)%KT for k in range(PA+1)]
    loop=[rings[R0][cc] for cc in cols[:-1]]+[rings[R0+i][cols[-1]] for i in range(PORT_ROWS)]+[rings[R1][cc] for cc in cols[::-1][:-1]]+[rings[R1-i][cols[0]] for i in range(PORT_ROWS)]
    assert len(loop)==KA and len(set(loop))==KA,(len(loop),len(set(loop)))
    Vv=np.array(C.V); LP=Vv[loop]; C.tag('shoulder_port_'+s,loop)
    A=np.array(SJ[s]['A']); n0=np.array(SJ[s]['n']); fh=np.array([0,1.0,0])
    g=L['glenohumeral_'+s]; e=L['elbow_'+s]; w=L['wrist_'+s]
    ua=unit(e-np.array([g[0],g[1],A[2]-1]))
    # rotation angle from n0 to ua about fh (sign chosen so that n0 rotates down toward ua)
    def rot_about(v,ax,a):
        ax=unit(ax); return v*np.cos(a)+np.cross(ax,v)*np.sin(a)+ax*(ax@v)*(1-np.cos(a))
    best=None
    for sgn in (1,-1):
        for a_ in np.linspace(0,np.pi,181):
            d=1-rot_about(n0,fh*sgn,a_)@ua
            if best is None or d<best[0]: best=(d,sgn,a_)
    _,sgn,amax=best
    # fan hinge: a line along f through the open arm/torso gap just below the armpit apex (outside the skin, so the fan
    # planes never meet on the surface -> no converging slivers at the armpit)
    zh=A[2]-float(__import__("os").environ.get("HDROP","7")); bandm=(np.abs(V[:,2]-zh)<0.3)&(np.abs(V[:,1]-A[1])<3)
    xt=(sg*V[bandm&(vlab==PID['axial']),0]).max(); xa=(sg*V[bandm&(vlab==PID['arm_'+s]),0]).min()
    Hh=np.array([sg*0.5*(xt+xa),A[1],zh]); print('fan hinge',s,np.round(Hh,2),'gap',round(xa-xt,2))
    st=[]
    for t in np.linspace(0.07,1.0,int(__import__('os').environ.get('NFAN','14'))):
        nk=rot_about(n0,fh*sgn,amax*t)
        if ((LP-Hh)@nk).max()>-0.3: continue        # plane would cut the port loop -> skip
        st.append(('fan',Hh,nk))
    zA=A[2]
    nup=int(max(0,(zA-3-(e[2]+4))//3.0))+1 if zA-3>e[2]+4 else 0
    for zz in list(np.linspace(zA-3,e[2]+4,nup))+[e[2]+2.4,e[2]+0.9,e[2]-0.6,e[2]-2.1]:   # elbow: 3 loops + crease
        t=(zA-zz)/(zA-e[2]); cc=np.array([g[0],g[1],zA])+(e-np.array([g[0],g[1],zA]))*t; st.append(('par',cc,ua))
    uf=unit(w-e)
    for t in list(np.linspace(0.07,0.80,15))+[0.84,0.87,0.895,0.92]: st.append(('par',e+(w-e)*t,unit(ua*(1-min(t*3,1))+uf*min(t*3,1))))
    prev=loop; prevP=LP; sub=SN.sub(['arm_'+s])
    for i,(kind,cc,nk) in enumerate(st):
        n_,a_,b_=frame_from_normal(nk,fh)
        if kind=='par' and ((prevP-cc)@n_).max()>-0.4: continue      # plane would cut the previous ring -> skip station
        segs=trimesh.intersections.mesh_plane(sub,n_,cc)
        if len(segs)==0: raise SystemExit('arm ring miss %d'%i)
        pts=segs.reshape(-1,3)
        if kind=='fan':
            wdir=unit(np.cross(fh,n_)); 
            if wdir@np.array([sg,0,1.0])<0: wdir=-wdir
            pts=pts[(pts-Hh)@wdir>0.3]
        else:
            pts=pts[np.linalg.norm(pts-cc,axis=1)<12]
        cen=pts.mean(0)
        q=prevP-cen; q=q-np.outer(q@n_,n_); a0=np.unwrap(np.arctan2(q@b_,q@a_))
        uni=a0[0]+loop_dir(q,a_,b_)*2*np.pi*np.arange(KA)/KA
        wgt=min(1.0,(i+1)/8); tt=(1-wgt)*a0+wgt*uni
        if i>=1 and (kind=='fan' or i<len(st)-2) and os.environ.get('FANADV','1')=='1':
            P=advance_ring(SN,['arm_'+s],prevP,cc,n_,mix=float(os.environ.get('FANMIX','0.5')) if kind=='fan' else float(os.environ.get('PARMIX','0.85')))
        else:
            P,ok=SN.ring(['arm_'+s]+(['hand_'+s] if i>=len(st)-2 else []),cen,n_,a_,tt)
            if P is None: raise SystemExit('ring none %d'%i)
            P=fill_misses(P,ok,cen)
            if kind=='par' and i<len(st)-2: P=arc_resample(P,0.8)
        cur=C.add(P); C.strip(prev,cur,'arm_'+s); prev=cur; prevP=P
        C.tag(('shoulder_fan_%s_%d' if kind=='fan' else 'elbow_%s_%d' if abs((cc-e)@ua)<2.6 else 'wrist_%s_%d' if i>=len(st)-2 else 'arm_%s_%d')%(s,i),cur)
        if s=="l": print("ARM",i,kind,np.round(cc,1),"cen",np.round(cen,1),"Pmean",np.round(P.mean(0),1),"zrange",np.round(P[:,2].min(),1),np.round(P[:,2].max(),1))
    arms[s]=prev
from hands import build_hand
for s in 'lr':
    build_hand(C,SN,s,arms[s],np.array(C.V)[arms[s]])
# ---- face rings: two insets around each orbit and the mouth (patches on the head grid) ----
def inset(rows,cols,alphas,part='axial',name='inset'):
    i0,i1=rows; ks=[(cols[0]+j)%KT for j in range((cols[1]-cols[0])%KT)]
    fids=[FACE_AT[(i,k)] for i in range(i0,i1) for k in ks]
    # boundary loop of the patch (grid walk)
    kk=ks+[(ks[-1]+1)%KT]
    B=[rings[i0][k] for k in kk[:-1]]+[rings[i][kk[-1]] for i in range(i0,i1)]+[rings[i1][k] for k in kk[::-1][:-1]]+[rings[i][kk[0]] for i in range(i1,i0,-1)]
    inner=set(rings[i][k] for i in range(i0+1,i1) for k in kk[1:-1])
    for al in alphas:
        Vv=np.array(C.V); c=Vv[list(set(B)|inner)].mean(0)
        newB=C.add([Vv[b]+al*(c-Vv[b]) for b in B]); mp=dict(zip(B,newB))
        for fi in fids: C.F[fi]=[mp.get(v,v) for v in C.F[fi]]
        for v in inner: C.V[v]=Vv[v]+al*(c-Vv[v])
        n=len(B)
        for k in range(n): C.quad(B[k],B[(k+1)%n],newB[(k+1)%n],newB[k],part)
        C.tag('%s_ring_%d'%(name,alphas.index(al)),newB)
        B=newB
ZA=Z_T+Z_H
iz=lambda z: ZA.index(z)
inset((iz(202.5),iz(205.5)),(35,39),(0.25,0.3),name='orbit_l')     # left orbit (subject left = +x, ring index ~36.6)
inset((iz(202.5),iz(205.5)),(2,6),(0.25,0.3),name='orbit_r')       # right orbit
inset((iz(193.5),iz(196.5)),(37,3),(0.22,0.28),name='mouth')         # lip line at z~194.7 (stomion)         # mouth
Vc,Fc,FPc=C.arrays(); Fc=fix_quad_winding(Fc)
if signed_volume(Vc,Fc)<0: Fc=Fc[:,::-1]
print('signed volume',signed_volume(Vc,Fc)); np.savez(sys.argv[1],V=Vc,Q=Fc,FP=FPc,tags=json.dumps(C.tags))
import trimesh, collections
T=[];
for f in Fc: T+= [[f[0],f[1],f[2]],[f[0],f[2],f[3]]]
m=trimesh.Trimesh(Vc,np.array(T),process=False); e=np.sort(m.edges,1); u,cnt=np.unique(e,axis=0,return_counts=True)
# quad-edge manifoldness
QE=np.concatenate([Fc[:,[0,1]],Fc[:,[1,2]],Fc[:,[2,3]],Fc[:,[3,0]]]); QE=np.sort(QE,1); uq,cq=np.unique(QE,axis=0,return_counts=True)
print('cage V',len(Vc),'quads',len(Fc),'edge use',collections.Counter(cq), 'euler', len(Vc)-len(uq)+len(Fc))
