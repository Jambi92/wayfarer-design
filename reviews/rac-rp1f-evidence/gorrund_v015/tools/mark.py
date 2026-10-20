# render v014 with coloured marker spheres: args views.json out marks.json
import bpy, numpy as np, sys, json, mathutils
a=sys.argv[sys.argv.index('--')+1:]; views=json.load(open(a[0])); out=a[1]; marks=json.load(open(a[2]))
bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene
z=np.load('/home/claude/wayfarer-design/reviews/rac-rp1e-evidence/designs/design_v014_production_L4.npz')
V=(z['V']*np.array([1,-1,1])).astype(np.float32); Q=z['Q'][:,::-1].astype(np.int32)
me=bpy.data.meshes.new('m'); me.vertices.add(len(V)); me.vertices.foreach_set('co',V.ravel()); me.loops.add(Q.size); me.loops.foreach_set('vertex_index',Q.ravel())
me.polygons.add(len(Q)); me.polygons.foreach_set('loop_start',np.arange(0,Q.size,4)); me.polygons.foreach_set('loop_total',np.full(len(Q),4)); me.update(); me.polygons.foreach_set('use_smooth',np.ones(len(Q),bool))
ob=bpy.data.objects.new('m',me); sc.collection.objects.link(ob); ob.color=(0.8,0.78,0.74,1)
import os
if os.environ.get('HFILE'):
    H=np.load(os.environ['HFILE']); t=np.clip(H/2.0,-1,1); C=np.ones((len(H),4),np.float32)*0.8; C[:,3]=1
    C[:,0]=0.8+0.2*np.clip(t,0,1)-0.6*np.clip(-t,0,1); C[:,1]=0.8-0.6*np.abs(t); C[:,2]=0.8+0.2*np.clip(-t,0,1)-0.6*np.clip(t,0,1)
    at=me.color_attributes.new('H','FLOAT_COLOR','POINT'); at.data.foreach_set('color',C.ravel())
cols=[(1,0,0),(0,1,0),(0,0.4,1),(1,1,0),(1,0,1),(0,1,1),(1,0.5,0),(0.5,0,1),(1,1,1),(0,0,0)]
for i,(p,r) in enumerate(marks):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r,location=p,segments=12,ring_count=8); o=bpy.context.active_object; c=cols[i%len(cols)]; o.color=(c[0],c[1],c[2],1)
cam=bpy.data.cameras.new('c'); cam.type='ORTHO'; co=bpy.data.objects.new('c',cam); sc.collection.objects.link(co); sc.camera=co; cam.clip_end=2000
sc.render.engine='BLENDER_WORKBENCH'; sh=sc.display.shading; sh.light='STUDIO'; sh.color_type='VERTEX' if os.environ.get('HFILE') else 'OBJECT'; sh.show_cavity=True; sh.background_type='VIEWPORT'; sh.background_color=(0.16,0.17,0.19)
sc.render.resolution_x=1000; sc.render.resolution_y=1000
for v in views:
    t=mathutils.Vector(v['t']); d=mathutils.Vector(v['d']).normalized(); co.location=t+d*400; co.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler(); cam.ortho_scale=v['s']
    sc.render.filepath='%s/%s.png'%(out,v['n']); bpy.ops.render.render(write_still=True)
