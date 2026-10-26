# loopaudit.py PROD.npz OUT.json : edge loops crossing each joint band (counted along the limb on both sides of the joint
# section), and poles inside crease bands.
import numpy as np, sys, json, trimesh, igl
sys.path.insert(0,'/tmp/claude-0/rt'); sys.path.insert(0,'/tmp/claude-0/src3d/v5/tools')
from common import *
import hands as HM, foot_model as fm
from hand_model import finger_chain
from hand_frame import frame
z=np.load(sys.argv[1]); V=z['V']; Q=z['Q']; FP=z['FP']
T=np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]]; mesh=trimesh.Trimesh(V,T,process=False)
L={k:np.array(v['p']) for k,v in json.load(open('/tmp/claude-0/rt/lm_src.json')).items()}
poles=np.load(sys.argv[1].replace('.npz','_poles.npy')); PV=V[poles]
unit=lambda v: v/np.linalg.norm(v)
import scipy.sparse as sp
from scipy.sparse.csgraph import dijkstra
from scipy.spatial import cKDTree
E=np.unique(np.sort(np.concatenate([Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]),1),axis=0)
wE=np.linalg.norm(V[E[:,0]]-V[E[:,1]],axis=1)
G=sp.coo_matrix((np.r_[wE,wE],(np.r_[E[:,0],E[:,1]],np.r_[E[:,1],E[:,0]])),shape=(len(V),len(V))).tocsr()
VN=np.zeros_like(V); _n=np.cross(V[Q[:,2]]-V[Q[:,0]],V[Q[:,3]]-V[Q[:,1]])
for k in range(4): np.add.at(VN,Q[:,k],_n)
VN/=np.maximum(np.linalg.norm(VN,axis=1),1e-12)[:,None]
kd=cKDTree(V)
def surf(p,dirn,R):
    # surface vertex nearest to the ray p + t*dirn (outermost hit approx): candidates near the ray, pick max t with outward normal
    cand=kd.query_ball_point(p+dirn*R*0.5,R*0.9)
    if not cand: return int(kd.query(p)[1])
    cand=np.array(cand); t=(V[cand]-p)@dirn; off=np.linalg.norm((V[cand]-p)-np.outer(t,dirn),axis=1)
    ok=(VN[cand]@dirn>0.3); sc=np.where(ok,off,1e9); return int(cand[np.argmin(sc)])

NB=[[] for _ in range(len(V))]
for a_,b_ in E: NB[a_].append(b_); NB[b_].append(a_)
VAL=np.array([len(n) for n in NB])
FAC=[[] for _ in range(len(V))]
for fi_,q_ in enumerate(Q):
    for v_ in q_: FAC[v_].append(fi_)
def opp(prev,v):
    # edge continuing straight through valence-4 vertex v coming from prev: the neighbour sharing no face with prev
    if VAL[v]!=4: return -1
    fs=set(FAC[prev])&set(FAC[v])
    for n in NB[v]:
        if n==prev: continue
        if not (set(FAC[n])&fs): return n
    return -1
def trace_ring(v0,d):
    # start along the neighbour edge most perpendicular to d, follow straight until closed
    best=None
    for n in NB[v0]:
        e=unit(V[n]-V[v0]); s_=abs(e@d)
        if best is None or s_<best[0]: best=(s_,n)
    ring=[v0,best[1]]
    for _ in range(4000):
        nx=opp(ring[-2],ring[-1])
        if nx<0: return None
        if nx==v0: return ring
        ring.append(nx)
    return None
def step(ring,d,sgn):
    nxt=[]
    for i_,v in enumerate(ring):
        if VAL[v]!=4: return None
        cand=[n for n in NB[v] if n not in (ring[i_-1],ring[(i_+1)%len(ring)])]
        if len(cand)!=2: return None
        cand.sort(key=lambda n: -sgn*((V[n]-V[v])@d)); nxt.append(cand[0])
    for i_ in range(len(nxt)):
        if nxt[(i_+1)%len(nxt)] not in NB[nxt[i_]]: return None
    return nxt
def rings(a,d,W,c):
    # number of closed edge rings around the limb whose centroid lies within +-W of the joint plane
    d=unit(d); r0=trace_ring(a,d)
    if r0 is None: return -1
    cnt=1 if abs((V[r0].mean(0)-c)@d)<=W else 0
    for sgn in (1,-1):
        r=r0
        for _ in range(60):
            r=step(r,d,sgn)
            if r is None: break
            o=(V[r].mean(0)-c)@d
            if abs(o)<=W: cnt+=1
            elif sgn*o>W: break
    return cnt

def section_count(c,d,side,W,R):
    # longitudinal plane through the joint axis and this side; count transverse (ring) edges it crosses on this side within
    # +-W of the joint plane and on the limb's own surface (radius <= 1.35 x own-surface radius) = edge loops crossing the band
    d=unit(d); s_=side-(side@d)*d; s_=unit(s_); n=unit(np.cross(d,s_))
    m=surf(c,s_,R); r0=np.linalg.norm((V[m]-c)-((V[m]-c)@d)*d)
    sg=(V-c)@n; cr=np.nonzero(np.sign(sg[E[:,0]])!=np.sign(sg[E[:,1]]))[0]
    a,b=E[cr,0],E[cr,1]; t=sg[a]/(sg[a]-sg[b]); X=V[a]+(V[b]-V[a])*t[:,None]
    rel=X-c; ax=rel@d; rad=rel-np.outer(ax,d); sd=rad@s_
    ev=V[b]-V[a]; trans=np.abs(ev@d)<0.5*np.linalg.norm(ev,axis=1)
    keep=(sd>0)&(np.abs(ax)<=W)&(np.linalg.norm(rad,axis=1)<=1.35*r0)&(np.linalg.norm(rad,axis=1)>=0.5*r0)&trans
    return int(keep.sum())
def count(c,d,W,R,perp=None,Rp=None):
    d=unit(d); p=unit(np.cross(d,[0,1.0,0] if abs(d[1])<0.9 else [1.0,0,0])) if perp is None else unit(perp)
    q=unit(np.cross(d,p)); res=[]; merged=[]; cres=[]; sres=[]
    for side in (p,-p,q,-q):
        sres.append(section_count(c,d,side,W,R))
        a=surf(c-d*W,side,R); b=surf(c+d*W,side,R)
        if np.linalg.norm(V[a]-V[b])<0.7*2*W: merged.append(1); sres.pop(); continue      # this side of the joint is merged into a web / neighbour surface
        _,pred=dijkstra(G,indices=a,return_predecessors=True,limit=4*W+3*R)
        if pred[b]<0: continue
        path=[b]
        while path[-1]!=a: path.append(int(pred[path[-1]]))
        P=V[path]; e=np.diff(P,axis=0); along=np.abs(e@d)>0.5*np.linalg.norm(e,axis=1)
        res.append(int(along.sum()))
        m_=surf(c,side,R); cres.append(rings(m_,d,W,c))
    loops_path=min(res) if res else 0; vr=[x for x in cres if x>=0]; loops=max(max(vr) if vr else 0,loops_path)
    # poles: 'on the crease' = within 2 local loops (2 x local edge length) of the joint plane
    near=np.nonzero(np.linalg.norm(V[E[:,0]]-c,axis=1)<R)[0]; h=float(np.median(wE[near])) if len(near) else 0.3
    Rp=R if Rp is None else Rp
    pb=((PV-c)@d); pr=np.linalg.norm((PV-c)-np.outer(pb,d),axis=1); onc=(np.abs(pb)<=2*h)&(pr<=Rp)
    return dict(loops=int(loops),loops_by_side=cres,method='max(closed-ring trace count, min-over-sides surface-path count)',section_by_side=sres,ring_trace_by_side=cres,loops_path_count=int(loops_path),loops_path_by_side=res,web_merged_sides=len(merged),band_cm=float(2*W),local_edge_mm=round(10*h,2),poles_within_2_loops=int(onc.sum()),poles_in_band=int(((np.abs(pb)<=W)&(pr<=R)).sum()))
out={}; req={}
def J(name,c,d,W,R,need,Rp=None):
    r=count(c,d,W,R,Rp=Rp); r['required']=need; r['pass']=bool(r['loops']>=need and r['poles_within_2_loops']==0); out[name]=r
for s,sg in (('l',1),('r',-1)):
    J('neck',L['neck_base']+np.array([0,4.0,-2.5]),np.array([0,0,1.0]),2.0,11,4) if s=='l' else None   # neck flexion band at the throat (below the chin)
    J('shoulder_'+s,L['glenohumeral_'+s],L['elbow_'+s]-L['glenohumeral_'+s],3.0,9,5)
    J('elbow_'+s,L['elbow_'+s],L['wrist_'+s]-L['elbow_'+s],1.5,7,4)
    W_,M_=frame(s.upper())
    J('wrist_'+s,L['wrist_'+s],M_[:,0] if np.dot(M_[:,0],L['middle_mcp_'+s]-L['wrist_'+s])>0 else -M_[:,0],1.0,5,3)
    p=HM.P_
    for nm,f in p['fingers'].items():
        Jc,dirs,_=finger_chain(f['mcp'],f['L'],f['splay'],f['flex']); Jw=[W_+M_@j for j in Jc]
        J('%s_mcp_%s'%(nm,s),Jw[0],Jw[1]-Jw[0],0.8,1.6,3)
        for k in (1,2): J('%s_ip%d_%s'%(nm,k,s),Jw[k],Jw[k+1]-Jw[k-1],0.5,1.3,2)
    Jt,_,_=HM.thumb_chain(); Jw=[W_+M_@j for j in Jt]
    J('thumb_mcp_'+s,Jw[1],Jw[2]-Jw[0],0.8,2.0,3); J('thumb_ip_'+s,Jw[2],Jw[3]-Jw[1],0.5,1.6,2)
    J('hip_'+s,L['hip_'+s],L['knee_'+s]-L['hip_'+s],3.0,12,5)
    J('knee_'+s,L['knee_'+s],L['ankle_'+s]-L['knee_'+s],1.5,9,4)
    J('ankle_'+s,L['ankle_'+s],L['ankle_'+s]-L['knee_'+s],1.5,7,3)
    for t in fm.DEF['toes']:
        Jt,_,_=fm.chain(t); P=np.array(Jt); P[:,0]*=sg
        for k in range(len(P)-1):
            a=P[k+1]-P[k-1] if k>0 else P[1]-P[0]
            J('%s_j%d_%s'%(t['n'],k,s),P[k],a,0.4,max(t['r'])*1.3,2,Rp=1.15*t['r'][min(k,len(t['r'])-1)])   # poles counted on the toe's own surface
ok=all(v['pass'] for v in out.values())
json.dump(dict(all_pass=ok,joints=out),open(sys.argv[2],'w'),indent=1)
for k,v in out.items():
    if not v['pass']: print('FAIL',k,v)
print('all_pass',ok,len(out))
