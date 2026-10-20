# diagnostic render of v014: (a) workbench smooth, no cavity; (b) cycles neutral skin; (c) cycles short-fur stand-in (sheen + fine bump)
import bpy, numpy as np, sys, json, mathutils
a=sys.argv[sys.argv.index('--')+1:]; views=json.load(open(a[0])); out=a[1]; mesh=a[2]
bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene
z=np.load(mesh); V=(z['V']*np.array([1,-1,1])).astype(np.float32); Q=z['Q'][:,::-1].astype(np.int32)
me=bpy.data.meshes.new('m'); me.vertices.add(len(V)); me.vertices.foreach_set('co',V.ravel()); me.loops.add(Q.size); me.loops.foreach_set('vertex_index',Q.ravel())
me.polygons.add(len(Q)); me.polygons.foreach_set('loop_start',np.arange(0,Q.size,4)); me.polygons.foreach_set('loop_total',np.full(len(Q),4)); me.update(); me.polygons.foreach_set('use_smooth',np.ones(len(Q),bool))
ob=bpy.data.objects.new('m',me); sc.collection.objects.link(ob)
cam=bpy.data.cameras.new('c'); cam.type='ORTHO'; co=bpy.data.objects.new('c',cam); sc.collection.objects.link(co); sc.camera=co; cam.clip_end=2000
def mat(fur):
    m=bpy.data.materials.new('fur' if fur else 'skin'); m.use_nodes=True; nt=m.node_tree; b=nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value=(0.62,0.5,0.38,1); b.inputs['Roughness'].default_value=0.75 if fur else 0.55
    if fur:
        b.inputs['Sheen Weight'].default_value=1.0; b.inputs['Sheen Roughness'].default_value=0.4
        tc=nt.nodes.new('ShaderNodeTexCoord'); nz=nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value=60.0; nz.inputs['Detail'].default_value=8
        bp=nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value=0.35; bp.inputs['Distance'].default_value=0.02
        nt.links.new(tc.outputs['Object'],nz.inputs['Vector']); nt.links.new(nz.outputs['Fac'],bp.inputs['Height']); nt.links.new(bp.outputs['Normal'],b.inputs['Normal'])
    return m
skin=mat(False); fur=mat(True)
world=bpy.data.worlds.new('w'); sc.world=world; world.use_nodes=True; world.node_tree.nodes['Background'].inputs['Color'].default_value=(0.25,0.26,0.28,1); world.node_tree.nodes['Background'].inputs['Strength'].default_value=0.6
L=bpy.data.lights.new('key','SUN'); L.energy=3.0; lo=bpy.data.objects.new('key',L); sc.collection.objects.link(lo)
sc.render.resolution_x=900; sc.render.resolution_y=900; sc.cycles.samples=48; sc.cycles.use_denoising=True; sc.cycles.device='CPU'
for v in views:
    t=mathutils.Vector(v['t']); d=mathutils.Vector(v['d']).normalized(); co.location=t+d*400
    co.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler(); cam.ortho_scale=v['s']
    lo.rotation_euler=(-(d+mathutils.Vector((0.4,0,0.6))).normalized()).to_track_quat('-Z','Y').to_euler()
    for mode in v.get('modes',['wb','skin','fur']):
        if mode=='wb':
            sc.render.engine='BLENDER_WORKBENCH'; sh=sc.display.shading; sh.light='STUDIO'; sh.color_type='SINGLE'; sh.single_color=(0.8,0.78,0.74); sh.show_cavity=False
            sh.background_type='VIEWPORT'; sh.background_color=(0.16,0.17,0.19)
        else:
            sc.render.engine='CYCLES'; ob.data.materials.clear(); ob.data.materials.append(skin if mode=='skin' else fur)
        sc.render.filepath='%s/%s_%s.png'%(out,v['n'],mode); bpy.ops.render.render(write_still=True)
