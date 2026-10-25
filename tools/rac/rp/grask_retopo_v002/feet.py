# feet.py : authored foot cage -- leg tube fanned about an ankle-crease hinge into the foot, forefoot rings, toe ports in the
# distal cap (14 x 2 grid), toe tubes along the v004/v005 construction chains.
import numpy as np, sys, igl, os
sys.path.insert(0,'/tmp/claude-0/rt'); sys.path.insert(0,'/tmp/claude-0/src3d/v5/tools')
from common import *
from cage import loop_dir, unit, fill_misses
from hands import capgrid
import foot_model as fm
NC=14
import os; DBG=os.environ.get('DBG')
def rect_param(nc):
    pts=[]
    for j in range(nc+1): pts.append((-1+2*j/nc,1.0))      # dorsal medial->lateral
    pts.append((1.0,0.0))                                  # lateral mid
    for j in range(nc,-1,-1): pts.append((-1+2*j/nc,-1.0)) # plantar lateral->medial
    pts.append((-1.0,0.0))                                 # medial mid
    return np.array(pts)
def build_foot(C,SN,side,prev,prevP,L):
    s=side; sg=1 if s=='l' else -1
    K=len(prev); assert K==2*NC+4
    a=L['ankle_'+s]
    # hinge: just in front of / above the ankle-front crease (outside the skin), along x
    H=np.array([a[0],2.5,16.8]); X=np.array([1.0,0,0])
    parts=['leg_'+s,'foot_'+s]
    st=[]
    for phi in np.radians([8,22,36,50,63,76,90]):
        st.append(('fan',H,np.array([0,np.sin(phi),-np.cos(phi)])))
    # forefoot planes: normal blends from +f to the MTP-line normal
    toes=fm.DEF['toes']; Jh,_,_=fm.chain(toes[0]); J5,_,_=fm.chain(toes[-1])
    mh=np.array(Jh[0]); m5=np.array(J5[0]); mh[0]*=sg; m5[0]*=sg
    t_=m5-mh; t_[2]=0; nm=unit(np.cross(t_,[0,0,1.0])); nm*=np.sign(nm[1])
    # toe web line: cleft floors between adjacent toes (ray from the MTP midpoint along the mean toe direction)
    subw=SN.sub(['foot_'+s]+['%s_%s'%(t['n'],s) for t in toes]); webs=[]
    global _FULL
    if '_FULL' not in globals(): _FULL=trimesh.Trimesh(SN.V,SN.F,process=False)
    for ta,tb in zip(toes[:-1],toes[1:]):
        Ja=np.array(fm.chain(ta)[0]); Jb=np.array(fm.chain(tb)[0]); Ja[:,0]*=sg; Jb[:,0]*=sg
        if os.environ.get('WEBMARCH','1')=='1':
            # most proximal point of the interdigital slot over the slot height (march the radius-weighted gap centre)
            ua=unit(Ja[1]-Ja[0]); ub=unit(Jb[1]-Jb[0]); best=None
            for dz in np.linspace(-1.0,1.0,11):
                for s_ in np.arange(0.0,5.0,0.05):
                    Pa=Ja[0]+ua*s_; Pb=Jb[0]+ub*s_; dd=np.linalg.norm(Pb-Pa); gc=Pa+(Pb-Pa)/dd*(ta['r'][0]+0.5*(dd-ta['r'][0]-tb['r'][0]))+np.array([0,0,dz])
                    if not _FULL.contains(gc[None])[0]:
                        if best is None or gc[1]<best[1]: best=gc
                        break
            webs.append(best)
        else:
            o=0.5*(Ja[0]+Jb[0]); d=unit(0.5*(unit(Ja[1]-Ja[0])+unit(Jb[1]-Jb[0])))
            loc,_,_=subw.ray.intersects_location([o],[d])
            if len(loc): webs.append(loc[np.argmin(np.linalg.norm(loc-o,axis=1))])
    webs=np.array(webs); beta,alpha=np.polyfit(webs[:,0],webs[:,1],1)
    nm=unit(np.array([-beta,1.0,0])); xm=webs[:,0].mean(); cw=np.array([xm,alpha+beta*xm,4.0])-nm*0.6
    print('web line',s,np.round(webs,1).tolist())
    # forefoot planes: medial and lateral ends advance linearly from f=5 to the web line (uniform spacing on both sides)
    xM=webs[0,0]-sg*3.0; xL=webs[-1,0]+sg*2.0
    fM=alpha+beta*xM-0.6; fL=alpha+beta*xL-0.6
    for w in [float(x) for x in os.environ.get('FFW','0.0,0.2,0.4,0.6,0.8,1.0').split(',')]:
        Mw=np.array([xM,5.0+(fM-5.0)*w,4.0]); Lw=np.array([xL,5.0+(fL-5.0)*w,4.0])
        n=unit(np.cross(Lw-Mw,[0,0,1.0])); n*=np.sign(n[1]); c=0.5*(Mw+Lw)
        st.append(('par',c,n))
    rings=[]; prevP_=prevP; prev_=prev
    RP=rect_param(NC)
    for i,(kind,c,n) in enumerate(st):
        n_,a_,b_=frame_from_normal(n,np.array([0,0,1.0]) if kind=='fan' else np.array([sg*1.0,0,0]))
        if kind=='par' and i<len(st)-1:
            nxt=st[-1]; dn=(prevP_-c)@n_; dl=(prevP_-nxt[1])@unit(nxt[2])
            if dn.max()>-0.3 or ((np.array([0.0])) if False else False): 
                print('skip forefoot station',s,i,'prev ring crosses plane',round(dn.max(),2)); continue
        if kind=='fan':
            sub=SN.sub(parts); segs=trimesh.intersections.mesh_plane(sub,n_,c).reshape(-1,3)
            w=unit(np.cross(X,n_));
            if w@np.array([0,-1.0,-1.0])<0: w=-w
            pts=segs[((segs-c)@w>0.2)&(np.abs(segs[:,0]-a[0])<12)]
            cen=pts.mean(0)
            q=prevP_-cen; q=q-np.outer(q@n_,n_); a0=np.unwrap(np.arctan2(q@b_,q@a_))
            uni=a0[0]+loop_dir(q,a_,b_)*2*np.pi*np.arange(K)/K
            wgt=min(1.0,(i+1)/5); tt=(1-wgt)*a0+wgt*uni
            P,ok=SN.ring(parts,cen,n_,a_,tt); P=fill_misses(P,ok,cen); order=list(range(K))
        else:
            # rectangle targets in (x-lateral, z-up) of this plane; plane basis a_ ~ lateral, b_ = n x a_
            bs=float(np.sign(np.cross(n_,a_)@np.array([0,0,1.0])))
            def tg(bb,allp):
                keep=(np.abs(allp[:,0])<12)&(np.abs(allp[:,1])<12); q=allp[keep]; lo,hi=q.min(0),q.max(0); cc=(lo+hi)/2; hh=(hi-lo)/2
                return np.array([[cc[0]+hh[0]*u*1.05,cc[1]+hh[1]*v*bs*1.05] for u,v in RP])
            pp=parts+(['%s_%s'%(t['n'],s) for t in toes] if i==len(st)-1 else [])
            if i<len(st)-1 and os.environ.get('FFADV','0')=='1':
                P=advance_ring(SN,parts,prevP_,c,n_,mix=0.5)
                cur=C.add(P); C.strip(prev_,cur,'foot_'+s); rings.append(cur); prev_=cur; prevP_=P
                C.tag('forefoot_%s_%d'%(s,i),cur); continue
            if os.environ.get('FFADV','0')=='1':
                # cap ring: continue the columns onto the web plane, then re-slot it as the rect (dorsal / lateral-mid /
                # plantar / medial-mid) layout by arclength between the medial-most and lateral-most points
                R0=advance_ring(SN,pp,prevP_,c,n_,mix=0.0)
                from common import _closest_on_segs
                segs_=trimesh.intersections.mesh_plane(SN.sub(pp),n_,c)
                Rd=np.vstack([R0[k]+(R0[(k+1)%K]-R0[k])*t_ for k in range(K) for t_ in np.linspace(0,1,8,endpoint=False)])
                Rd=_closest_on_segs(Rd,segs_[:,0],segs_[:,1])
                lat=np.array([sg*1.0,0,0]); lat-=(lat@n_)*n_; lat/=np.linalg.norm(lat)
                im=int(np.argmin(Rd@lat)); il=int(np.argmax(Rd@lat)); N_=len(Rd)
                arcA=[(im+k)%N_ for k in range((il-im)%N_+1)]; arcB=[(il+k)%N_ for k in range((im-il)%N_+1)]
                if Rd[arcA,2].mean()<Rd[arcB,2].mean(): arcA,arcB=[(im-k)%N_ for k in range((im-il)%N_+1)],[(il-k)%N_ for k in range((il-im)%N_+1)]
                def samp(idx,n):
                    Pp=Rd[idx]; sg_=np.linalg.norm(np.diff(Pp,axis=0),axis=1); cs_=np.r_[0,np.cumsum(sg_)]; out=[]
                    for t_ in np.linspace(0,cs_[-1],n+1)[1:-1]:
                        j=min(np.searchsorted(cs_,t_,side='right')-1,len(Pp)-2); u_=(t_-cs_[j])/max(sg_[j],1e-12); out.append(Pp[j]+(Pp[j+1]-Pp[j])*u_)
                    return out
                dors=samp(arcA,NC+2); plan=samp(arcB,NC+2)        # dorsal M->L ; plantar L->M
                P=np.array(dors+[Rd[il]]+plan+[Rd[im]])
                P=_closest_on_segs(P,segs_[:,0],segs_[:,1])
            else:
                P=ring_closest(SN,pp,c,n_,a_,tg)
            if st[i-1][0]=='fan' or os.environ.get('FFADV','0')=='1':
                best=None
                for d in (1,-1):
                    for sh in range(K):
                        idx=[(sh+d*k)%K for k in range(K)]
                        cost=np.linalg.norm(prevP_-P[idx],axis=1).sum()
                        if best is None or cost<best[0]: best=(cost,idx)
                perm=best[1]; inv=np.argsort(perm)
            P=P[perm]
        cur=C.add(P); C.strip(prev_,cur,'foot_'+s if kind=='par' else 'leg_'+s); rings.append(cur); prev_=cur; prevP_=P
        C.tag(('ankle_%s_%d' if kind=='fan' else 'forefoot_%s_%d')%(s,i),cur)
    # slot access on the forefoot rings: ring position holding slot k is inv[k]
    last=rings[-1]
    slot_d=lambda j: j; slot_p=lambda j: NC+2+(NC-j); SLOT_L=NC+1; SLOT_M=2*NC+3
    pos=lambda sl: last[int(inv[sl])]
    top=[pos(slot_d(j)) for j in range(NC+1)]; bot=[pos(slot_p(j)) for j in range(NC+1)]
    mid=[pos(SLOT_M)]+[None]*(NC-1)+[pos(SLOT_L)]
    pc=[0,3,6,9,12]; PWs=[3,3,3,3,2]                # hallux medial .. toe5 lateral; adjacent ports share cleft edges
    # cleft floors between toes: most proximal source point between adjacent toe bodies
    chains=[]
    for t in toes:
        J,_,_=fm.chain(t); J=np.array(J); J[:,0]*=sg; chains.append((J,t['r']))
    for j in range(1,NC):
        if any(c<j<c+w for c,w in zip(pc,PWs)): continue
        gi=None
        for g_,(c,w) in enumerate(zip(pc[:-1],PWs[:-1])):
            if j==c+w: gi=(g_,0)
        pt=0.5*(np.array(C.V[top[j]])+np.array(C.V[bot[j]]))
        if gi is not None:
            (Ja,ra),(Jb,rb)=chains[gi[0]],chains[gi[0]+1]
            o=0.5*(Ja[0]+Jb[0]); d=unit(0.5*(unit(Ja[1]-Ja[0])+unit(Jb[1]-Jb[0])))
            subf=SN.sub(['foot_'+s]+['%s_%s'%(t['n'],s) for t in toes])
            # web saddle: march the gap centre between the two toe axes (radius-weighted) until it leaves the body
            if os.environ.get('WEBMARCH','1')=='1':
                ua=unit(Ja[1]-Ja[0]); ub=unit(Jb[1]-Jb[0]); RA=ra[0]; RB=rb[0]; hit=None
                for s_ in np.arange(0.0,5.0,0.05):
                    Pa=Ja[0]+ua*s_; Pb=Jb[0]+ub*s_; dd=np.linalg.norm(Pb-Pa); gc=Pa+(Pb-Pa)/dd*(RA+0.5*(dd-RA-RB))
                    if not _FULL.contains(gc[None])[0]: hit=gc; break
                if hit is not None:
                    _,_,cp=igl.point_mesh_squared_distance(hit[None],subf.vertices,subf.faces); pt=cp[0]-unit(ua+ub)*0.05
                    mid[j]=C.add([pt])[0]; continue
            loc,ri,_=subf.ray.intersects_location([o],[d])
            if len(loc):
                p=loc[np.argmin(np.linalg.norm(loc-o,axis=1))].copy()
                # touching toes: the ray runs far down the seam -- clamp the cleft just distal of the cap
                if (p-pt)@d>0.8:
                    _,_,cp=igl.point_mesh_squared_distance((pt+d*0.8)[None],subf.vertices,subf.faces); p=cp[0]
                pt=p-d*0.1
        mid[j]=C.add([pt])[0]
    # web corners: pull the dorsal / plantar cap vertex of each cleft column part-way toward the cleft floor, so the shared
    # cleft edge is short and the corner quads are not wedges
    al=float(os.environ.get('CLPUSH','0.4'))
    if al>0:
        subf_=SN.sub(['foot_'+s]+['%s_%s'%(t['n'],s) for t in toes])
        for c_,w_ in zip(pc[:-1],PWs[:-1]):
            j=c_+w_; m_=np.array(C.V[mid[j]])
            for row in (top,bot):
                p_=np.array(C.V[row[j]]); q_=p_+al*(m_-p_)
                _,_,cp_=igl.point_mesh_squared_distance(q_[None],subf_.vertices,subf_.faces); C.V[row[j]]=cp_[0]
    G=[top,mid,bot]
    for j in range(NC):
        if any(c<=j<c+w for c,w in zip(pc,PWs)): continue
        for i in range(2): C.quad(G[i][j],G[i][j+1],G[i+1][j+1],G[i+1][j],'foot_'+s)
    for t,c,w,(J,r) in zip(toes,pc,PWs,chains):
        loop=[G[0][c+k] for k in range(w+1)]+[G[1][c+w]]+[G[2][c+k] for k in range(w,-1,-1)]+[G[1][c]]
        _,dirs,dors=fm.chain(t); dirs=[np.array([sg*d[0],d[1],d[2]]) for d in dirs]; dors=[np.array([sg*d[0],d[1],d[2]]) for d in dors]
        Lk=t['L']; n_ph=len(Lk); st=[]
        lab=[]
        for tt in [float(x) for x in os.environ.get('TOEP1','0.3,0.6').split(',')]: st.append((J[0]+dirs[0]*Lk[0]*tt,dirs[0])); lab.append('p1')
        for k in range(1,n_ph):
            b=unit(dirs[k-1]+dirs[k])
            for tt,dd in ((-0.2,dirs[k-1]),(0.0,b),(0.2,dirs[k])): st.append((J[k]+dd*Lk[k-1 if tt<0 else k]*tt,unit(dd))); lab.append('ip%d'%k)
            if k<n_ph-1: st.append((J[k]+dirs[k]*Lk[k]*0.5,dirs[k])); lab.append('p%d'%(k+1))
        for tt in (0.4,0.65,0.85): st.append((J[n_ph-1]+dirs[-1]*Lk[-1]*tt,dirs[-1])); lab.append('p%d'%n_ph)
        prev_=loop; prevP_=np.array([C.V[i] for i in loop]); Kd=len(loop); part='%s_%s'%(t['n'],s)
        # keep only stations distal to the port (a short, set-back toe may have its MTP inside the forefoot cap)
        kk=[i_ for i_,(cc,nn) in enumerate(st) if ((cc-prevP_)@nn).min()>float(os.environ.get('DMARG','0.25'))]; keep=[st[i_] for i_ in kk]; lab=[lab[i_] for i_ in kk]
        C.tag('%s_root_%s'%(t['n'],s),loop)
        if len(keep)<len(st):
            print('toe',t['n'],s,'dropped',len(st)-len(keep),'stations proximal to port')
        st=keep
        for i,(cc,nn) in enumerate(st):
            n_,a_,b_=frame_from_normal(nn,dors[0])
            q=prevP_-cc; q=q-np.outer(q@n_,n_); a0=np.unwrap(np.arctan2(q@b_,q@a_))
            uni=a0[0]+loop_dir(q,a_,b_)*2*np.pi*np.arange(Kd)/Kd
            wgt=1.0 if os.environ.get('DIGUNI','1')=='1' else min(1.0,(i+1)/3); tt=(1-wgt)*a0+wgt*uni
            rad=float(np.mean(t['r']))
            P,ok=SN.ring([part],cc,n_,a_,tt,near=np.full(Kd,rad))
            circ=cc+rad*(np.outer(np.cos(tt),a_)+np.outer(np.sin(tt),b_))
            if P is None: P=circ; ok=np.ones(Kd,bool)
            ok&=np.linalg.norm(P-cc,axis=1)<2.0*rad
            if ok.sum()<Kd//2: P=circ; ok=np.ones(Kd,bool)
            P=fill_misses(P,ok,cc)
            if loop_dir(P-cc,a_,b_)!=loop_dir(q,a_,b_):      # garbled ring (wrong sense) -> ordered circle at the median radius
                rm=float(np.median(np.linalg.norm(P-cc,axis=1))); P=cc+rm*(np.outer(np.cos(uni),a_)+np.outer(np.sin(uni),b_))
            if DBG and part in ('toe5_l','toe5_r'): print('ST',i,np.round(cc,1),np.round(nn,2),'dir',loop_dir(q,a_,b_),'ok',ok.sum(),'r',np.round(np.linalg.norm(P-cc,axis=1),1).tolist(),'newdir',loop_dir(P-cc,a_,b_))
            _sh=min(range(Kd),key=lambda h: np.linalg.norm(np.roll(P,-h,0)-prevP_,axis=1).sum()); P=np.roll(P,-_sh,0)   # cyclic alignment (no twisted strip)
            if i==0 and os.environ.get('TOEADV','0')=='1':
                PA=advance_ring(SN,[part],prevP_,cc,n_,mix=0.5)      # root ring: continue the port's columns (no twist at the cleft corners)
                if PA is not None and loop_dir(PA-cc,a_,b_)==loop_dir(q,a_,b_): P=PA
            cur=C.add(P); C.strip(prev_,cur,part); prev_=cur; prevP_=P; C.tag('%s_%s_%s_%d'%(t['n'],s,lab[i],i),cur)
        capgrid(C,prev_,2,Kd//2-2,part,J[-1])
