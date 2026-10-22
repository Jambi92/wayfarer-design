# stage2_proj.py (bpy python) : project the non-digit-patch hand vertices of v015 onto the accepted rev107 surface
#  ray along the v015 vertex normal (both directions, <=1 cm, hit normal must agree >0.5), else nearest point with agreeing
#  normal; then displacement-field smoothing (bounded, protected vertices fixed) and nearest-point re-projection.
import sys,pickle,numpy as np,json; sys.path.insert(0,'/tmp/claude-0/hand/tools'); from hm import *
import bpy, mathutils
from mathutils.bvhtree import BVHTree
V,Q=load15(); R,F,mat=load107()
d=np.load('/tmp/claude-0/hand/v015_to_r107_d.npy'); prot=d<1e-4
vp=pickle.load(open('/tmp/claude-0/hand/vpatch.pkl','rb'))
# patch interior vertices (draped separately) = vertices of patch quads that are not on the patch's outer (plane) loop
patchv=np.zeros(len(V),bool); outer=np.zeros(len(V),bool)
for k,p in vp.items():
    if k.startswith('_'): continue
    patchv[Q[p['faces']].ravel()]=True
    loops=p['loops'] if 'loops' in p else [p['loop']]
    L=max(loops,key=lambda l: np.linalg.norm(V[l].mean(0)-V[Q[p['faces']]].reshape(-1,3).mean(0)) if False else 0)
for k in vp:
    if k.startswith('_'): continue
patchv[Q[vp['_strip']].ravel()]=True
# outer loops: the loop nearest the digit plane
D=json.load(open('/tmp/claude-0/hand/digits.json')); rp=pickle.load(open('/tmp/claude-0/hand/rpatch.pkl','rb'))
outer_loops={}
for k,p in vp.items():
    if k.startswith('_'): continue
    loops=p['loops'] if 'loops' in p else [p['loop']]
    stripv=np.zeros(len(V),bool); stripv[Q[vp['_strip']].ravel()]=True
    ol=min(loops,key=lambda l: (stripv[np.array(l)].mean(), np.abs((V[l]-rp[k]['p0'])@rp[k]['ax']).mean())); outer_loops[k]=np.array(ol); outer[ol]=True
H=(~prot)&((~patchv)|outer); print('project',H.sum(),'patch-interior',(patchv&~outer).sum(),'protected',prot.sum())
assert not (prot&patchv).any()
# outward normals (Q is in the y-flipped analysis winding: reverse it)
Qo=Q[:,::-1]
fn=np.cross(V[Qo[:,1]]-V[Qo[:,0]],V[Qo[:,2]]-V[Qo[:,0]])+np.cross(V[Qo[:,2]]-V[Qo[:,0]],V[Qo[:,3]]-V[Qo[:,0]])
vn=np.zeros_like(V)
for c in range(4): np.add.at(vn,Qo[:,c],fn)
vn/=np.linalg.norm(vn,axis=1,keepdims=True)+1e-30
vol=np.einsum('ij,ij->i',V[Qo[:,0]],fn).sum(); print('signed volume sign',np.sign(vol))
if vol<0: vn=-vn
bvh=BVHTree.FromPolygons(R.tolist(),F.tolist())
fnr=np.cross(R[F[:,1]]-R[F[:,0]],R[F[:,2]]-R[F[:,0]]); fnr/=np.linalg.norm(fnr,axis=1,keepdims=True)+1e-30
volr=np.einsum('ij,ij->i',R[F[:,0]],fnr).sum(); print('rev107 volume sign',np.sign(volr))
if volr<0: fnr=-fnr
idx=np.where(H)[0]; P=V[idx].copy(); how=np.zeros(len(idx),int)
for j,i in enumerate(idx):
    p=V[i]; n=vn[i]; best=None
    for sg in (1,-1):
        h=bvh.ray_cast(mathutils.Vector(p-sg*1e-5*n),mathutils.Vector(sg*n),1.0)
        if h[0] is not None and fnr[h[2]]@n>0.5 and (best is None or h[3]<best[1]): best=(np.array(h[0]),h[3])
    if best is None:
        h=bvh.find_nearest(mathutils.Vector(p),1.5)
        if h[0] is not None: best=(np.array(h[0]),h[3]); how[j]=2
        else: how[j]=3; best=(p,0)
    else: how[j]=1
    P[j]=best[0]
print('ray',(how==1).sum(),'nearest',(how==2).sum(),'none',(how==3).sum())
disp=np.zeros_like(V); disp[idx]=P-V[idx]
print('disp mm med %.3f p95 %.3f max %.3f'%tuple(np.percentile(np.linalg.norm(disp[idx],axis=1)*10,[50,95,100])))
# smooth the displacement field (protected and patch-interior vertices act as fixed context, 0 / own)
E=edges_q(Q); nbr=[[] for _ in range(len(V))]
A=sp.coo_matrix((np.ones(2*len(E)),(np.r_[E[:,0],E[:,1]],np.r_[E[:,1],E[:,0]])),shape=(len(V),len(V))).tocsr(); deg=np.asarray(A.sum(1)).ravel()
mov=H&~outer
for it in range(int(sys.argv[1]) if len(sys.argv)>1 else 10):
    avg=(A@disp)/deg[:,None]; disp[mov]=0.5*disp[mov]+0.5*avg[mov]
Vp=V.copy(); Vp[H]=V[H]+disp[H]
# re-project onto rev107 (nearest, normal-consistent; else keep)
nfix=0
for i in idx:
    h=bvh.find_nearest(mathutils.Vector(Vp[i]),0.3)
    if h[0] is not None and fnr[h[2]]@vn[i]>0.3: Vp[i]=np.array(h[0])
    else: nfix+=1
print('reprojection skipped',nfix)
np.save('/tmp/claude-0/hand/Vproj.npy',Vp); np.save('/tmp/claude-0/hand/vn15.npy',vn)
pickle.dump(dict(H=H,outer_loops=outer_loops,patch_interior=patchv&~outer),open('/tmp/claude-0/hand/proj_info.pkl','wb'))
print('done')
