# stage3_drape.py KEY [ITERS] : drape one digit patch (v015 topology; R22/R23 with the cut-bridge hole capped) onto rev107
import sys,pickle,numpy as np,json,time,igl; sys.path.insert(0,'/tmp/claude-0/hand/tools')
from hm import *; from patches import boundary_loops; from drape import drape; from cap import grid_cap, orient_like
k=sys.argv[1]; iters=int(sys.argv[2]) if len(sys.argv)>2 else 3000
V,Q=load15(); Vp=np.load('/tmp/claude-0/hand/Vproj.npy')
vp=pickle.load(open('/tmp/claude-0/hand/vpatch.pkl','rb'))[k]; rp=pickle.load(open('/tmp/claude-0/hand/rpatch.pkl','rb'))[k]
pi=pickle.load(open('/tmp/claude-0/hand/proj_info.pkl','rb')); outer=pi['outer_loops'][k]
Qg=Q[vp['faces']]; loops,_=boundary_loops(Qg)
holes=[np.array(l) for l in loops if set(l)!=set(outer.tolist())]
print(k,'quads',len(Qg),'loops',[len(l) for l in loops],'holes',[len(h) for h in holes])
gid=np.unique(Qg); mp={g:i for i,g in enumerate(gid)}; Ql=np.vectorize(mp.get)(Qg); Pl=V[gid].copy()
newp=[]; nnew=0; capq=[]
for h in holes:
    hl=np.array([mp[x] for x in h]); nqv=np.bincount(Ql.ravel(),minlength=len(Pl)); p,cq=grid_cap(hl,Pl,len(Pl)+nnew,nquads=nqv); newp.append(p); nnew+=len(p); capq.append(cq)
if holes:
    Pl=np.vstack([Pl]+newp); cq=np.vstack(capq); cq,same,opp=orient_like(Ql,cq); print('cap quads',len(cq),'orient same/opp',same,opp)
    Ql=np.vstack([Ql,cq])
loops2,_=boundary_loops(Ql); assert len(loops2)==1, [len(l) for l in loops2]
bl=np.array(loops2[0]); bp=Vp[gid[bl]]
dchk=np.sqrt(igl.point_mesh_squared_distance(bp,rp['X'],rp['F'])[0])
if dchk.max()>1e-3:
    # the rev107 patch must contain the whole fixed boundary: re-clip it further proximally
    from patches import comp_faces; from drape import clip_plane
    R,F,_=load107(); off=min(((bp-rp['p0'])@rp['ax']).min()-0.4,-0.4)
    near=np.linalg.norm(R-rp['p0'],axis=1)<15; fsel=F[near[F].all(1)]
    R2,F2=clip_plane(R,fsel,rp['p0']+off*rp['ax'],rp['ax']); sr=np.argmin(np.linalg.norm(R2-rp['apex'],axis=1)); ft=comp_faces(F2,sr,len(R2))
    ut=np.unique(ft); mt=-np.ones(len(R2),int); mt[ut]=np.arange(len(ut)); rp['X']=R2[ut]; rp['F']=mt[ft]
    lt,_=boundary_loops(rp['F']); print('re-clipped rev107 patch at offset %.2f: loops'%off,[len(l) for l in lt]); assert len(lt)==1; rp['loop']=np.array(lt[0])
    dchk=np.sqrt(igl.point_mesh_squared_distance(bp,rp['X'],rp['F'])[0]); print('boundary->patch max mm %.3f'%(dchk.max()*10))
t0=time.time()
# end-cap grid centre: among the 4 valence-3 poles nearest the old free edge, the vertex equidistant (graph) from them
Eq=np.unique(np.sort(np.vstack([Ql[:,[i,(i+1)%4]] for i in range(4)]),1),axis=0); val=np.bincount(Eq.ravel(),minlength=len(Pl))
import os
H=json.load(open('/tmp/claude-0/rp1f/hand_frames.json')); Told=np.array(H[k]['T'])
isb=np.zeros(len(Pl),bool); isb[bl]=True
poles=np.where((val==3)&~isb)[0]; poles=poles[np.argsort(np.linalg.norm(Pl[poles]-Told,axis=1))[:4]]
Gq=graph(Pl,Eq); gd=geod(Gq,poles); gd=np.atleast_2d(gd) if gd.ndim==1 else gd
from scipy.sparse.csgraph import dijkstra
gd=dijkstra(Gq,indices=poles); cen=int(np.argmin(gd.max(0)+np.where(isb,1e9,0)))
print('end-cap poles',poles.tolist(),'centre',cen,'dist to poles',gd[:,cen].round(2).tolist())
pm=os.environ.get('PINMODE','soft' if ('thumb' in k or k in ('A_R22','A_R23')) else 'cap')
if pm=='T':
    # tip of the old digit: interior vertex nearest the free-edge point projected along the digit axis (most distal skin)
    ax=rp['ax']; cand=np.where(~isb)[0]; cen=int(cand[np.argmax(Pl[cand]@ax)])
HP=[] if pm in ('none','soft') else [(cen,rp['apex'])]
print('pin mode',pm,'vertex',cen)
X3,P2,U=drape(Pl,Ql,bl,bp,rp['X'],rp['F'],rp['loop'],pins=[] if HP else [(None,rp['apex'])],hard_pins=HP,iters=iters,log=print,mix=0.2,shape=0.5)
print('time %.0f s'%(time.time()-t0))
g=np.r_[gid,-np.ones(nnew,int)]
np.savez('/tmp/claude-0/hand/drape_%s.npz'%k,gid=g,X3=X3,Ql=Ql,P2=P2,Xl=rp['X'],Fl=rp['F'],U=U)
