# blender-python dmask.py -- OUT.npz : exterior-visibility mask of the source near the approved D candidates (v014 ruling 2.4).
# A source vertex is interior (D) if none of 162 rays (icosphere directions in its outward hemisphere, from p+0.01n, length 200 cm)
# escapes the source.  Only vertices inside the approved D boxes are tested.
import sys, numpy as np, bpy, bmesh, mathutils
from mathutils.bvhtree import BVHTree
a_=sys.argv[sys.argv.index("--")+1:]; out=a_[0]; DELTA=float(a_[1]) if len(a_)>1 else 0.01; BR=float(a_[2]) if len(a_)>2 else 0.0
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64)
fn=np.cross(S[SF[:,1]]-S[SF[:,0]],S[SF[:,2]]-S[SF[:,0]]); vn=np.zeros_like(S)
for k in range(3): np.add.at(vn,SF[:,k],fn)
vn/=np.linalg.norm(vn,axis=1,keepdims=True)+1e-12
bvh=BVHTree.FromPolygons(S.tolist(),SF.tolist())
bm=bmesh.new(); bmesh.ops.create_icosphere(bm,subdivisions=3,radius=1.0); D=np.array([v.co[:] for v in bm.verts]); D/=np.linalg.norm(D,axis=1,keepdims=True)
BOX={'Laxilla_void':((23.8,-40.5,146.5),3.5),'Lhand_tunnel':((38.6,-50.0,100.5),3.0),'Rhand_fused':((-33.5,-40.5,93.5),3.0)}
res={}
for nm,(c,r) in BOX.items():
    idx=np.where(np.linalg.norm(S-np.array(c),axis=1)<r)[0]; esc=np.zeros(len(idx),int)
    for t,i in enumerate(idx):
        o=mathutils.Vector((S[i]+vn[i]*DELTA).tolist()); n=0
        for dv in D[D@vn[i]>0.05]:
            u=np.cross(dv,[0,0,1.0]) if abs(dv[2])<0.9 else np.cross(dv,[1.0,0,0]); u/=np.linalg.norm(u); v_=np.cross(dv,u)
            ok=True
            for off in ([0,0],[BR,0],[-BR,0],[0,BR],[0,-BR]):
                oo=o+mathutils.Vector((u*off[0]+v_*off[1]).tolist())
                h=bvh.ray_cast(oo,mathutils.Vector(dv.tolist()),200.0)
                if h[0] is not None: ok=False; break
            if ok: n+=1; break
        esc[t]=n
    res[nm+'_idx']=idx; res[nm+'_esc']=esc
    print(nm,'tested',len(idx),'interior (no escape)',int((esc==0).sum()))
np.savez_compressed(out,**res)
