# pendepth.py (bpy) -- RIGDIR SIDE POSE_JSON SCALE : classify new intersections of a scaled pose and measure penetration depth
import bpy,sys,numpy as np,math,os,pickle,json,igl
from mathutils.bvhtree import BVHTree
a=sys.argv[sys.argv.index('--')+1:]; rd,side,pj,scale=a[0],a[1],a[2],float(a[3])
bpy.ops.wm.open_mainfile(filepath=os.path.join(rd,'hand_rig_DIAG.blend')); RD=pickle.load(open(os.path.join(rd,'rig_data.pkl'),'rb'))
ob=bpy.data.objects['GO_hand_%s_DIAG'%side]; ao=bpy.data.objects['GO_hand_%s_RIG'%side]
me=ob.data; Q=np.zeros(len(me.polygons)*4,int); me.polygons.foreach_get('vertices',Q); Q=Q.reshape(-1,4)
def ev():
    dg=bpy.context.evaluated_depsgraph_get(); e=ob.evaluated_get(dg); m=e.to_mesh(); P=np.zeros(len(m.vertices)*3); m.vertices.foreach_get('co',P); e.to_mesh_clear(); return P.reshape(-1,3)
def setp(ang):
    for pb in ao.pose.bones: pb.rotation_mode='XYZ'; pb.rotation_euler=(0,0,0)
    for b,(fx,ab,tw) in ang.items(): ao.pose.bones[b].rotation_euler=(math.radians(fx),math.radians(tw),math.radians(ab))
    bpy.context.view_layer.update()
def sx(P):
    t=BVHTree.FromPolygons(P.tolist(),Q.tolist(),all_triangles=False,epsilon=0.0); pr=np.array(t.overlap(t),int).reshape(-1,2); pr=pr[pr[:,0]<pr[:,1]]
    A=Q[pr[:,0]];B=Q[pr[:,1]]; return pr[~(A[:,:,None]==B[:,None,:]).any((1,2))]
S=json.load(open(pj)); ang={b:[scale*x for x in v] for b,v in S['angles'].items()}
setp({}); P0=ev(); r0=set(map(tuple,sx(P0).tolist()))
setp(ang); P=ev(); pr=np.array(sorted(set(map(tuple,sx(P).tolist()))-r0),int).reshape(-1,2)
own=RD[side]['own']; ker=RD[side]['ker']; fown=np.array([np.bincount(own[q]+1,minlength=6).argmax()-1 for q in Q])
from collections import Counter
cnt=Counter(tuple(sorted((int(fown[a_]),int(fown[b_])))) for a_,b_ in pr); print('pairs',len(pr),'by owner (digit idx, -1 palm):',dict(cnt))
# penetration depth: vertices of the intersecting quads vs the surface of the OTHER owner (pseudonormal sign)
T=np.vstack([Q[:,[0,1,2]],Q[:,[0,2,3]]])[:,::-1]; Town=np.r_[fown,fown]
deep={}
for (o1,o2),n in cnt.items():
    for oa,ob_ in ((o1,o2),(o2,o1)):
        qs=np.unique(np.r_[pr[fown[pr[:,0]]==oa,0],pr[fown[pr[:,1]]==oa,1]]); vs=np.unique(Q[qs])
        other=T[Town==ob_] if oa!=ob_ else T
        if len(vs)==0 or len(other)==0: continue
        sd,_,_,_=igl.signed_distance(P[vs],P,other,sign_type=igl.SIGNED_DISTANCE_TYPE_PSEUDONORMAL)
        deep['%d_in_%d'%(oa,ob_)]=float(-sd.min()*1000)
print('max penetration depth mm by (owner in other):',{k:round(v,2) for k,v in deep.items()})
