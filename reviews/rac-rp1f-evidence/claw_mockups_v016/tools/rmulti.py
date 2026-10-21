# blender: rmulti.py -- views.json OUTDIR tag1=mesh1.npz tag2=mesh2.npz ...
import bpy, numpy as np, sys, json, mathutils
a=sys.argv[sys.argv.index('--')+1:]; views=json.load(open(a[0])); out=a[1]; ms=[x.split('=',1) for x in a[2:]]
bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene
def mk(name,V,F):
    me=bpy.data.meshes.new(name); me.vertices.add(len(V)); me.vertices.foreach_set('co',V.ravel())
    n=F.shape[1]; me.loops.add(F.size); me.loops.foreach_set('vertex_index',F.ravel()); me.polygons.add(len(F))
    me.polygons.foreach_set('loop_start',np.arange(0,F.size,n)); me.polygons.foreach_set('loop_total',np.full(len(F),n)); me.update()
    me.polygons.foreach_set('use_smooth',np.ones(len(F),bool))
    o=bpy.data.objects.new(name,me); sc.collection.objects.link(o); return o
objs=[]
for tag,p in ms:
    z=np.load(p); objs.append((tag,mk(tag,(z['V']*np.array([1,-1,1])).astype(np.float32),z['Q'][:,::-1].astype(np.int32))))
cam=bpy.data.cameras.new('c'); cam.type='ORTHO'; co=bpy.data.objects.new('c',cam); sc.collection.objects.link(co); sc.camera=co
sc.render.engine='BLENDER_WORKBENCH'; sh=sc.display.shading; sh.light='STUDIO'; sh.color_type='SINGLE'; sh.single_color=(0.8,0.78,0.74); sh.show_cavity=True; sh.cavity_type='BOTH'
sh.background_type='VIEWPORT'; sh.background_color=(0.16,0.17,0.19)
sc.render.resolution_x=900; sc.render.resolution_y=900; cam.clip_end=2000
for v in views:
    t=mathutils.Vector(v['t']); d=mathutils.Vector(v['d']).normalized(); co.location=t+d*400
    co.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler(); cam.ortho_scale=v['s']
    for tag,o in objs:
        for _,oo in objs: oo.hide_render=(oo is not o)
        sc.render.filepath='%s/%s__%s.png'%(out,v['n'],tag); bpy.ops.render.render(write_still=True)
