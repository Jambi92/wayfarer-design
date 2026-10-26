# ringshow.py PROD.npz LOOPS.json OUTDIR : closed-ring evidence for selected joints (ankles, right elbow): every distinct
# closed edge ring found by the audit's ring trace inside the joint band, its offset from the joint plane, its obliquity,
# its authored-tag name, and nearby poles; wire renders with the rings drawn in colour and the joint plane marked.
import numpy as np, sys, json, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection, LineCollection
sys.path.insert(0,'/tmp/claude-0/rt')
z=np.load(sys.argv[1]); V=z['V']; Q=z['Q']; tags=json.load(open(sys.argv[2])); O=sys.argv[3]
L={k:np.array(v['p']) for k,v in json.load(open('/tmp/claude-0/rt/lm_src.json')).items()}
unit=lambda v: v/np.linalg.norm(v)
E=np.unique(np.sort(np.concatenate([Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]),1),axis=0)
NB=[[] for _ in range(len(V))]
for a_,b_ in E: NB[a_].append(b_); NB[b_].append(a_)
VAL=np.array([len(n) for n in NB]); FAC=[[] for _ in range(len(V))]
for fi_,q_ in enumerate(Q):
    for v_ in q_: FAC[v_].append(fi_)
poles=np.nonzero(VAL!=4)[0]
def opp(prev,v):
    if VAL[v]!=4: return -1
    fs=set(FAC[prev])&set(FAC[v])
    for n in NB[v]:
        if n!=prev and not (set(FAC[n])&fs): return n
    return -1
def trace_ring(v0,d):
    n=min(NB[v0],key=lambda n: abs(unit(V[n]-V[v0])@d)); ring=[v0,n]
    for _ in range(4000):
        nx=opp(ring[-2],ring[-1])
        if nx<0: return None
        if nx==v0: return ring
        ring.append(nx)
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
from scipy.spatial import cKDTree; kd=cKDTree(V)
VN=np.zeros_like(V); n_=np.cross(V[Q[:,2]]-V[Q[:,0]],V[Q[:,3]]-V[Q[:,1]])
for k in range(4): np.add.at(VN,Q[:,k],n_)
VN/=np.maximum(np.linalg.norm(VN,axis=1),1e-12)[:,None]
def surf(p,dirn,R):
    cand=kd.query_ball_point(p+dirn*R*0.5,R*0.9)
    if not cand: return int(kd.query(p)[1])
    cand=np.array(cand); t=(V[cand]-p)@dirn; off=np.linalg.norm((V[cand]-p)-np.outer(t,dirn),axis=1)
    return int(cand[np.argmin(np.where(VN[cand]@dirn>0.3,off,1e9))])
tagsets={k:frozenset(v) for k,v in tags.items()}
J={'ankle_l':(L['ankle_l'],L['ankle_l']-L['knee_l'],1.5,7),'ankle_r':(L['ankle_r'],L['ankle_r']-L['knee_r'],1.5,7),
   'elbow_r':(L['elbow_r'],L['wrist_r']-L['elbow_r'],1.5,7)}
sys.path.insert(0,'/tmp/claude-0/src3d/v5/tools'); import foot_model as fm
for t in fm.DEF['toes']:
    if t['n']=='toe5':
        Jt,_,_=fm.chain(t); P_=np.array(Jt); J['toe5_j0_l']=(P_[0],P_[1]-P_[0],0.4,max(t['r'])*1.3)
audit=json.load(open(sys.argv[1].replace('.npz','_loops_audit.json')))['joints']; REP={}
for name,(c,d,W,R) in J.items():
    d=unit(d); p=unit(np.cross(d,[0,1.0,0] if abs(d[1])<0.9 else [1.0,0,0])); q=unit(np.cross(d,p))
    found={}; sides=[]
    for sn,side in (('p',p),('-p',-p),('q',q),('-q',-q)):
        m_=surf(c,side,R); r0=trace_ring(m_,d); got=[]
        if r0 is None: sides.append(dict(side=sn,start=int(m_),ring_trace='failed (pole on the start loop)')); continue
        seq=[r0]
        for sgn in (1,-1):
            r=r0
            for _ in range(60):
                r=step(r,d,sgn)
                if r is None: break
                o=(V[r].mean(0)-c)@d
                if abs(o)<=W: seq.append(r)
                elif sgn*o>W: break
        for r in seq:
            o=float((V[r].mean(0)-c)@d)
            if abs(o)<=W:
                k=frozenset(r); found.setdefault(k,r); got.append(round(o*10,1))
        sides.append(dict(side=sn,start=int(m_),rings_in_band_offsets_mm=sorted(got)))
    rows=[]
    for k,r in sorted(found.items(),key=lambda kv: (V[kv[1]].mean(0)-c)@d):
        t=(V[r]-c)@d; tag=[n for n,s in tagsets.items() if len(s&k)>=0.8*len(k)]
        dp=np.linalg.norm(V[poles][:,None]-V[r][None],axis=2).min() if len(poles) else 99
        rows.append(dict(offset_mm=round(float(t.mean()*10),1),extent_mm=[round(float(t.min()*10),1),round(float(t.max()*10),1)],verts=len(r),
            authored_tag=tag[0] if tag else 'subdivision loop (between authored rings)',nearest_pole_mm=round(float(dp*10),1),ring=[int(v) for v in r]))
    near=[dict(id=int(v),valence=int(VAL[v]),offset_mm=round(float((V[v]-c)@d*10),1),radial_cm=round(float(np.linalg.norm((V[v]-c)-((V[v]-c)@d)*d)),1)) for v in poles if np.linalg.norm(V[v]-c)<R*1.5]
    REP[name]=dict(joint_centre_cm=np.round(c,2).tolist(),axis=np.round(d,3).tolist(),band_mm=[-W*10,W*10],required=audit[name]['required'],
        distinct_closed_rings_in_band=len(rows),rings=rows,sides=sides,path_count_by_side=audit[name]['loops_path_by_side'],poles_within_1_5R=near)
    # render: two views, rings coloured
    for vn,(az,el) in (('front',(0 if name!='elbow_r' else -60,5 if not name.startswith('toe') else 60)),('side',(90 if name!='ankle_r' else -90,5))):
        a=np.radians(az); e=np.radians(el); cam=np.array([np.cos(e)*np.sin(a),np.cos(e)*np.cos(a),np.sin(e)]); rt=np.cross([0,0,1.0],cam); rt/=np.linalg.norm(rt); up=np.cross(cam,rt)
        m=np.linalg.norm(V-c,axis=1)<(R*1.3 if not name.startswith('toe') else 2.5); F=Q[m[Q].all(1)]; T_=V[F]; N=np.cross(T_[:,2]-T_[:,0],T_[:,3]-T_[:,1]); N/=np.linalg.norm(N,axis=1)[:,None]+1e-12
        vis=N@cam>0; T_=T_[vis]; N=N[vis]; o=np.argsort(T_.mean(1)@cam); T_=T_[o]; N=N[o]; sh=0.5+0.45*np.clip(N@cam,0,1)
        fig=plt.figure(figsize=(9,9),dpi=110); ax=fig.add_axes([0,0,1,1]); ax.set_aspect('equal'); ax.axis('off')
        ax.add_collection(PolyCollection(np.stack([T_@rt,T_@up],-1),facecolors=np.stack([sh*.88,sh*.86,sh*.83],1),edgecolors=(0.2,0.2,0.25,0.35),linewidths=0.3))
        cols=plt.cm.tab10(np.linspace(0,1,10))
        for i,rw in enumerate(rows):
            r=rw['ring']; P=V[r+[r[0]]]; front=(VN[r+[r[0]]]@cam)>-0.05
            seg=np.stack([P[:-1],P[1:]],1); keep=front[:-1]&front[1:]
            ax.add_collection(LineCollection(np.stack([seg[keep]@rt,seg[keep]@up],-1),colors=[cols[i%10]],linewidths=2.6))
            j=np.argmax(np.where(front,(P@rt),-1e9)); ax.text(P[j]@rt+0.3,P[j]@up,'%+.1f mm'%rw['offset_mm'],color=cols[i%10],fontsize=10,weight='bold')
        # joint plane: line through c perpendicular to d in view
        dv=np.array([d@rt,d@up]); pv=np.array([-dv[1],dv[0]]); pv/=np.linalg.norm(pv)+1e-12; cc=np.array([c@rt,c@up])
        for s_,ls in ((0,'-'),(W,'--'),(-W,'--')):
            q_=cc+np.array([d@rt,d@up])*s_; ax.plot([q_[0]-pv[0]*R,q_[0]+pv[0]*R],[q_[1]-pv[1]*R,q_[1]+pv[1]*R],ls,color='red',lw=1.5 if s_==0 else 1)
        for pw in near:
            P_=V[pw['id']]
            if VN[pw['id']]@cam>0: ax.plot(P_@rt,P_@up,'o',color={3:'red',5:'blue'}.get(pw['valence'],'black'),ms=7); ax.text(P_@rt,P_@up,' v%d'%pw['valence'],fontsize=9)
        ax.autoscale_view(); ax.set_title('%s  %s view - %d distinct closed rings inside the +-%d mm band (red dashed; solid = joint plane)'%(name,vn,len(rows),W*10),fontsize=11)
        fig.savefig('%s/rings_%s_%s.png'%(O,name,vn)); plt.close(fig)
for k in REP:
    for r in REP[k]['rings']: r.pop('ring')
json.dump(REP,open(O+'/ring_evidence.json','w'),indent=1)
for k,v in REP.items(): print(k,'rings',v['distinct_closed_rings_in_band'],'req',v['required'],[ (r['offset_mm'],r['extent_mm'],r['authored_tag']) for r in v['rings']],'sides',[s.get('rings_in_band_offsets_mm',s.get('ring_trace')) for s in v['sides']],'paths',v['path_count_by_side'])
