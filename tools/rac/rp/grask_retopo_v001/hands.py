# hands.py : authored hand cage (palm tube, thumb port on the radial side, 4 finger ports in the distal cap grid)
import numpy as np, sys, os
sys.path.insert(0,'/tmp/claude-0/rt'); sys.path.insert(0,'/tmp/claude-0/src3d/v5/tools')
from common import *
from cage import loop_dir, unit, fill_misses
from hand_model import DEF as HDEF, scaled, finger_chain, rot
from hand_frame import frame
P_=scaled(HDEF)
NCOL=13   # palm cap columns (KA = 2*(13+2) = 30)
def thumb_chain():
    T=P_['thumb']; dth=unit(T['dir']); dor=np.array(T['dors'],float); dor-=(dor@dth)*dth; dor=unit(dor)
    J=[np.array(T['cmc'],float)]; dirs=[dth]; dors=[dor]; J.append(J[0]+T['L'][0]*dth)
    for k in range(2):
        lat=np.cross(dirs[-1],dors[-1]); R=rot(lat,np.radians(T['flex'][k]))
        if (R@dirs[-1])@dors[-1]>0: R=rot(lat,-np.radians(T['flex'][k]))
        dirs.append(R@dirs[-1]); dors.append(R@dors[-1]); J.append(J[-1]+T['L'][k+1]*dirs[-1])
    return J,dirs,dors
def rect_param(nc):
    """local (v,w) unit rectangle walk: dorsal radial->ulnar (nc segs), ulnar side (2), palmar ulnar->radial (nc), radial (2)"""
    pts=[]
    for j in range(nc+1): pts.append((1-2*j/nc,1.0))
    pts.append((-1.0,0.0))
    for j in range(nc,-1,-1): pts.append((1-2*j/nc,-1.0))
    pts.append((1.0,0.0))
    return np.array(pts)   # 2*nc+4 points
def build_hand(C,SN,side,prev,prevP):
    s=side; sg=1 if s=='l' else -1
    W,M=frame(s.upper()); toW=lambda q: W+M@np.asarray(q,float)
    e0,e1,e2=M[:,0],M[:,1],M[:,2]
    K=len(prev); assert K==2*NCOL+4
    RP=rect_param(NCOL)
    def slot_d(j): return j
    def slot_p(j): return NCOL+2+(NCOL-j)
    SLOT_U=NCOL+1; SLOT_R=2*NCOL+3
    hs=float(np.sign(np.cross(e0,e1)@e2))
    def palm_ring(u,parts,wlo):
        c=toW([u,0.3,-0.25])
        def tg(bb,allp,RP=RP):
            ww=allp[:,1]*hs; keep=(np.abs(allp[:,0]-0.3)<8.0)&(ww>wlo)&(ww<3.8)
            q=allp[keep]; lo,hi=q.min(0),q.max(0); cc=(lo+hi)/2; hh=(hi-lo)/2
            return np.array([[cc[0]+hh[0]*a*1.05,cc[1]+hh[1]*b*hs*1.05] for a,b in RP])
        return ring_closest(SN,parts,c,e0,e1,tg)
    fingers=['index','middle','ring','pinky']
    U_pre=[0.8,2.0,3.2,4.4,5.6,6.8,8.0,9.2,10.3]; U_post=[11.3,12.3,13.3,14.3]
    pre=[palm_ring(u,['hand_'+s,'thumb_'+s]+(['arm_'+s] if i==0 else []),-8.0) for i,u in enumerate(U_pre)]
    post=[palm_ring(u,['hand_'+s]+(['%s_%s'%(d,s) for d in fingers] if u>13 else []),-4.2) for u in U_post]
    # align ring 0 with the incoming arm ring
    best=None
    for d in (1,-1):
        for sh in range(K):
            idx=[(sh+d*k)%K for k in range(K)]
            cost=np.linalg.norm(prevP-pre[0][idx],axis=1).sum()
            if best is None or cost<best[0]: best=(cost,idx)
    perm=best[1]
    pre_ids=[C.add(r) for r in pre]
    C.strip(prev,[pre_ids[0][j] for j in perm],'hand_'+s)
    for i in range(len(pre_ids)-1): C.strip(pre_ids[i],pre_ids[i+1],'hand_'+s)
    S=pre_ids[-1]
    for i_,r_ in enumerate(pre_ids): C.tag('wrist_palm_%s_%d'%(s,i_) if i_<2 else 'palm_%s_%d'%(s,i_),r_)
    # split: thumb takes the palmar-radial slots p0..p5; chain of 4 between p5 and p0 over the thumb (first web)
    p0_=np.array(C.V[S[slot_p(0)]]); p5_=np.array(C.V[S[slot_p(5)]])
    subT=SN.sub(['hand_'+s,'thumb_'+s])
    import igl
    ch=[]
    for k in (1,2,3,4):
        q=p5_+(p0_-p5_)*k/5+e2*(3.0*np.sin(np.pi*k/5))+e0*0.9
        d,fi,cp=igl.point_mesh_squared_distance(q[None],SN.V,subT.faces); ch.append(cp[0])
    chain=C.add(ch)                      # c1 (near p5) .. c4 (near p0)
    PP=list(S)
    for j,ci in zip((4,3,2,1),chain): PP[slot_p(j)]=ci
    post_ids=[C.add(r) for r in post]
    C.strip(PP,post_ids[0],'hand_'+s)
    for i in range(len(post_ids)-1): C.strip(post_ids[i],post_ids[i+1],'hand_'+s)
    last=post_ids[-1]; pos=lambda slot: slot
    for i_,r_ in enumerate(post_ids): C.tag('mcp_palm_%s_%d'%(s,i_),r_)
    thumb_first=[S[slot_p(j)] for j in range(6)]+chain
    C.tag('thumb_root_'+s,thumb_first)
    # ---- distal cap grid NCOL x 2 with 4 finger ports ----
    Vv=lambda i: np.array(C.V[i])
    top=[last[pos(slot_d(j))] for j in range(NCOL+1)]
    bot=[last[pos(slot_p(j))] for j in range(NCOL+1)]
    mid=[last[pos(SLOT_R)]]+[None]*(NCOL-1)+[last[pos(SLOT_U)]]
    pc=[0,4,7,10]; PWS=[4,3,3,3]   # finger ports sharing their cleft edges; index spans the radial margin (no corner pole at the MCP crease)
    roots={}
    for nm in fingers:
        f=P_['fingers'][nm]; J,_,_=finger_chain(f['mcp'],f['L'],f['splay'],f['flex']); roots[nm]=J
    sub=SN.sub(['hand_'+s]+['%s_%s'%(d,s) for d in fingers])
    # cleft floors between adjacent fingers: most proximal source point strictly between the finger bodies
    SVl=(SN.V-W)@M
    axes=[]
    for nm in fingers:
        f=P_['fingers'][nm]; J,_,_=finger_chain(f['mcp'],f['L'],f['splay'],f['flex']); axes.append((J[0],J[1],f['r'][0]*1.13))
    cleft={}
    subW=SN.sub(['hand_'+s]+['%s_%s'%(d,s) for d in fingers])
    for gi in range(3):
        (a0,a1,ra),(b0,b1,rb)=axes[gi],axes[gi+1]
        o=W+M@(0.5*(a0+b0)); d=unit(M@(0.5*(unit(a1-a0)+unit(b1-b0))))
        loc,ri,_=subW.ray.intersects_location([o],[d])
        p=loc[np.argmin(np.linalg.norm(loc-o,axis=1))]
        q=(np.linalg.inv(M)@(p-W)); cleft[gi]=(q,0.5*(a0[1]+a1[1]),0.5*(b0[1]+b1[1]))
    for j in range(1,NCOL):
        if any(c<j<c+w for c,w in zip(pc,PWS)): continue      # port interior (removed)
        pt=0.5*(Vv(top[j])+Vv(bot[j]))
        gi=None
        for g_,c in enumerate(pc[:-1]):
            if j==c+PWS[g_]: gi=g_
        if gi is not None:
            q=cleft[gi][0].copy(); q[0]+=0.1; pt=pt+float(os.environ.get('CLW','1.0'))*(W+M@q-pt)
        else:
            o=pt-e0*3.0; loc,ri,_=sub.ray.intersects_location([o],[e0])
            if len(loc): pt=loc[np.argmin(np.linalg.norm(loc-o,axis=1))]
        mid[j]=C.add([pt])[0]
    G=np.array([top,mid,bot],dtype=object)
    for j in range(NCOL):
        if any(c<=j<c+w for c,w in zip(pc,PWS)): continue
        for i in range(2): C.quad(G[i][j],G[i][j+1],G[i+1][j+1],G[i+1][j],'hand_'+s)
    ports={}
    for nm,c in zip(fingers,pc):
        PW=PWS[pc.index(c)]; loop=[G[0][c+k] for k in range(PW+1)]+[G[1][c+PW]]+[G[2][c+k] for k in range(PW,-1,-1)]+[G[1][c]]
        ports[nm]=loop
    ports['thumb']=thumb_first
    # ---- digit tubes ----
    for nm in fingers+['thumb']:
        if nm=='thumb':
            J,dirs,dors=thumb_chain(); r=[x*1.1 for x in P_['thumb']['r']]; Lk=P_['thumb']['L']
        else:
            f=P_['fingers'][nm]; J,dirs,dors=finger_chain(f['mcp'],f['L'],f['splay'],f['flex']); r=f['r']; Lk=f['L']
        loop=ports[nm]; LP=np.array([C.V[i] for i in loop]); Kd=len(loop)
        # stations along the chain: (centre local, normal local)
        st=[]
        if nm=='thumb':
            for t in (0.12,0.22,0.32,0.42,0.62,0.8): st.append((J[1]+dirs[1]*Lk[1]*t,dirs[1]))
        else:
            for t in (0.22,0.4,0.58,0.76): st.append((J[0]+dirs[0]*Lk[0]*t,dirs[0]))
        # joints: 3 loops per IP (before, at, after)
        nj=2
        for k in (range(2,3) if nm=='thumb' else range(1,nj+1)):
            b=unit(dirs[k-1]+dirs[k])
            for t,dd in ((-0.18,dirs[k-1]),(0.0,b),(0.18,dirs[k])): st.append((J[k]+dd*Lk[k-1 if t<0 else k]*t,unit(dd)))
            if k<nj: st.append((J[k]+dirs[k]*Lk[k]*0.5,dirs[k]))
        for t in (0.38,0.6,0.8): st.append((J[nj]+dirs[nj]*Lk[nj]*t,dirs[nj]))
        lab=(['p1']*6+['ip']*3+['p2']*3) if nm=='thumb' else (['p1']*4+['pip']*3+['p2']+['dip']*3+['p3']*3)
        C.tag('%s_root_%s'%(nm,s),loop)
        prev_=loop; prevP_=LP; dsub=['%s_%s'%(nm,s)]
        _kk=[i_ for i_,(cl,nl) in enumerate(st) if ((toW(cl)-LP)@(M@nl)).min()>float(os.environ.get('DMARG','0.25'))]   # station plane distal of the whole port loop
        st=[st[i_] for i_ in _kk]; lab=[lab[i_] for i_ in _kk]
        for i,(cl,nl) in enumerate(st):
            c=toW(cl); n=M@nl; dor=M@dors[min(len(dors)-1,max(0,int(np.searchsorted([0]+[1e9],0))))]
            n_,a_,b_=frame_from_normal(n,M@dors[0] if nm!='thumb' else M@dors[0])
            q=prevP_-c; q=q-np.outer(q@n_,n_); a0=np.unwrap(np.arctan2(q@b_,q@a_))
            uni=a0[0]+loop_dir(q,a_,b_)*2*np.pi*np.arange(Kd)/Kd
            wgt=1.0 if os.environ.get('DIGUNI','1')=='1' else min(1.0,(i+1)/3); tt=(1-wgt)*a0+wgt*uni
            P,ok=SN.ring(dsub+(['hand_'+s] if i==0 else []),c,n_,a_,tt)
            if P is None: P=prevP_+(c-prevP_.mean(0)); ok=np.ones(Kd,bool)
            P=fill_misses(P,ok,c)
            if loop_dir(P-c,a_,b_)!=loop_dir(q,a_,b_):
                rm=float(np.median(np.linalg.norm(P-c,axis=1))); P=c+rm*(np.outer(np.cos(uni),a_)+np.outer(np.sin(uni),b_))
            _sh=min(range(Kd),key=lambda h: np.linalg.norm(np.roll(P,-h,0)-prevP_,axis=1).sum()); P=np.roll(P,-_sh,0)   # cyclic alignment (no twisted strip)
            cur=C.add(P); C.strip(prev_,cur,'%s_%s'%(nm,s)); prev_=cur; prevP_=P; C.tag('%s_%s_%s_%d'%(nm,s,lab[i],i),cur)
        # tip cap
        rows,cols=2,Kd//2-2
        capgrid(C,prev_,rows,cols,'%s_%s'%(nm,s),toW(J[-1]))
def capgrid(C,ring,R,Cc,part,tip,pull=0.6,push=None):
    G=-np.ones((R+1,Cc+1),int); k=0
    for j in range(Cc): G[0,j]=ring[k]; k+=1
    for i in range(R): G[i,Cc]=ring[k]; k+=1
    for j in range(Cc,0,-1): G[R,j]=ring[k]; k+=1
    for i in range(R,0,-1): G[i,0]=ring[k]; k+=1
    Vv=np.array(C.V)
    for i in range(1,R):
        for j in range(1,Cc):
            u=j/Cc; v=i/R
            p=(1-v)*Vv[G[0,j]]+v*Vv[G[R,j]]+(1-u)*Vv[G[i,0]]+u*Vv[G[i,Cc]]-((1-u)*(1-v)*Vv[G[0,0]]+u*(1-v)*Vv[G[0,Cc]]+(1-u)*v*Vv[G[R,0]]+u*v*Vv[G[R,Cc]])
            p=p+(tip-p)*pull
            if push is not None: p=p+push
            G[i,j]=C.add([p])[0]
    for i in range(R):
        for j in range(Cc): C.quad(G[i,j],G[i,j+1],G[i+1,j+1],G[i+1,j],part)
