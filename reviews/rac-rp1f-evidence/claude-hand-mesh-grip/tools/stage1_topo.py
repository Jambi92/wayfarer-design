# stage1_topo.py : digit patch definitions on v015 and rev107; R22/R23 distal bridge split (rev107 owner) + quad grid caps
import sys; sys.path.insert(0,'/tmp/claude-0/hand/tools'); from hm import *; from patches import comp_faces, boundary_loops; from drape import clip_plane
import igl, pickle
V,Q=load15(); R,F,mat=load107(); D=json.load(open('/tmp/claude-0/hand/digits.json'))
MARGIN=0.4
out={'digits':{}}
rp={}
for k,d in D.items():
    ax=np.array(d['axis']); c1=np.array(d['c1']); p0=c1+(d['claw_s'][0]-1.0)*ax
    apex=np.array(d['claw_tip']); sr=np.argmin(np.linalg.norm(R-apex,axis=1))
    near=np.linalg.norm(R-p0,axis=1)<12; fsel=F[near[F].all(1)]
    mg=1.5 if k in ('A_R22','A_R23') else MARGIN
    R2,F2=clip_plane(R,fsel,p0-mg*ax,ax); ft=comp_faces(F2,sr,len(R2)); ut=np.unique(ft); mt=-np.ones(len(R2),int); mt[ut]=np.arange(len(ut))
    Xl=R2[ut]; Fl=mt[ft]; lt,_=boundary_loops(Fl); assert len(lt)==1, (k,len(lt))
    rp[k]=dict(X=Xl,F=Fl,loop=np.array(lt[0]),p0=p0,ax=ax,apex=apex)
    print(k,'rev107 patch tris',len(Fl))
pickle.dump(rp,open('/tmp/claude-0/hand/rpatch.pkl','wb'))
# v015 patches
newQ=Q.copy(); Vn=V.copy(); delete=np.zeros(len(Q),bool); caps=[]; vpatch={}
for k,d in D.items():
    if k in ('A_R22','A_R23'): continue
    ax=rp[k]['ax']; p0=rp[k]['p0']; T=np.array(d['T']); sv=np.argmin(np.linalg.norm(V-T,axis=1))
    inv=(V-p0)@ax>0; fid=np.where(inv[Q].all(1))[0]
    fq=comp_faces(Q[fid],sv,len(V)); 
    # face ids of the component
    key={tuple(q):i for i,q in zip(fid,Q[fid].tolist())}; ids=np.array([key[tuple(q)] for q in fq.tolist()])
    loops,_=boundary_loops(fq); assert len(loops)==1
    vpatch[k]=dict(faces=ids,loop=np.array(loops[0])); print(k,'v015 patch quads',len(ids))
# R22/R23 union
ks=('A_R22','A_R23'); inv=np.zeros(len(V),bool)
for k in ks: inv|=(V-rp[k]['p0'])@rp[k]['ax']>0
T22=np.array(D['A_R22']['T']); sv=np.argmin(np.linalg.norm(V-T22,axis=1))
fid=np.where(inv[Q].all(1))[0]; fq=comp_faces(Q[fid],sv,len(V)); key={tuple(q):i for i,q in zip(fid,Q[fid].tolist())}; uid=np.array([key[tuple(q)] for q in fq.tolist()])
uv=np.unique(Q[uid])
# separate the fused distal bridge at its narrowest cross-section: minimum s-t edge cut between the two digits
import networkx as nx
ul,_=boundary_loops(Q[uid]); print('union loops',[len(l) for l in ul])
def side(loop):
    c=V[loop].mean(0); return 0 if np.linalg.norm(c-rp['A_R22']['p0'])<np.linalg.norm(c-rp['A_R23']['p0']) else 1
E=edges_q(Q[uid]); G=nx.Graph(); G.add_weighted_edges_from([(int(a),int(b),float(np.linalg.norm(V[a]-V[b]))) for a,b in E],weight='capacity')
dd=[]
for k in ks:
    sd,_,_=igl.point_mesh_squared_distance(V[uv],rp[k]['X'],rp[k]['F']); dd.append(np.sqrt(sd))
conf=[uv[(dd[0]<0.05)&(dd[1]>0.3)], uv[(dd[1]<0.05)&(dd[0]>0.3)]]
print('confident seeds',len(conf[0]),len(conf[1]))
for i,k in enumerate(ks):
    srcs=[int(x) for l in ul if side(l)==i for x in l]+conf[i].tolist()
    node='S' if i==0 else 'T'
    for x in srcs: G.add_edge(node,x,capacity=1e9)
cutval,(Sset,Tset)=nx.minimum_cut(G,'S','T'); print('min cut length cm',cutval)
own=np.full(len(V),-1); own[np.array([x for x in Sset if x!='S'])]=0; own[np.array([x for x in Tset if x!='T'])]=1
oq=own[Q[uid]]; mixed=(oq.min(1)!=oq.max(1)); print('union quads',len(uid),'strip quads',mixed.sum())
for i,k in enumerate(ks):
    T=np.array(D[k]['T']); svk=np.argmin(np.linalg.norm(V-T,axis=1))
    cand=uid[(~mixed)&(oq[:,0]==i)]
    C0=np.array(json.load(open('/tmp/claude-0/rp1f/hand_frames.json'))[k]['C']); cv=np.unique(Q[cand]); svk=cv[np.argmin(np.linalg.norm(V[cv]-C0,axis=1))]
    fq=comp_faces(Q[cand],svk,len(V)); key={tuple(q):j for j,q in zip(cand,Q[cand].tolist())}; ids=np.array([key[tuple(q)] for q in fq.tolist()],int)
    rest=np.setdiff1d(cand,ids)
    loops,nm=boundary_loops(Q[ids]); print(k,'quads',len(ids),'leftover',len(rest),'loops',[len(l) for l in loops],'nonmanifold',nm, 'chi',euler_sub(Q[ids]))
    vpatch[k]=dict(faces=ids,loops=[np.array(l) for l in loops],leftover=rest)
vpatch['_strip']=uid[mixed]
pickle.dump(vpatch,open('/tmp/claude-0/hand/vpatch.pkl','wb'))
