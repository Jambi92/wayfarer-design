# ortho renders in foot frame: usage orthorender.py VF.npz TAG OUTDIR [mask.npy]; views: front(L/R), top(L/R), side34 (L/R)
import sys, json, numpy as np, bpy, mathutils
vf,tag,od=sys.argv[1:4]; mask=sys.argv[4] if len(sys.argv)>4 else None
D=np.load(vf); V,F=D['V'],D['F']; FR=json.load(open('/home/claude/aw1/footframes.json'))
bpy.ops.wm.read_factory_settings(use_empty=True)
me=bpy.data.meshes.new('m'); me.from_pydata(V.tolist(),[],F.tolist()); me.update()
o=bpy.data.objects.new('m',me); sc=bpy.context.scene; sc.collection.objects.link(o)
for pl in me.polygons: pl.use_smooth=True
sc.render.engine='BLENDER_WORKBENCH'; sh=sc.display.shading; sh.light='STUDIO'
if mask:
    M=np.load(mask); ca=me.color_attributes.new('c','FLOAT_COLOR','POINT'); col=np.ones((len(V),4)); col[:,0]=0.7+0.3*M; col[:,1]=0.7-0.5*M; col[:,2]=0.7-0.5*M
    ca.data.foreach_set('color',col.ravel()); sh.color_type='VERTEX'
else: sh.color_type='SINGLE'; sh.single_color=(0.7,0.7,0.7)
sc.world=bpy.data.worlds.new('w')
cam=bpy.data.cameras.new('c'); cam.type='ORTHO'; co=bpy.data.objects.new('c',cam); sc.collection.objects.link(co); sc.camera=co; cam.clip_end=5
sc.render.resolution_x=1400; sc.render.resolution_y=700
for s in 'LR':
    c=np.array(FR[s]['c']); a=np.array(FR[s]['a']); p=np.array(FR[s]['p']); z=np.array([0,0,1.0])
    views={'front':(c+a*0.5+np.array([0,0,0.04-c[2]]),np.column_stack([p,z,a]),0.17),
           'top':(c+a*0.085+np.array([0,0,0.3-c[2]]),np.column_stack([-p,a,z]),0.17)}
    d34=(a+0.8*z)/np.linalg.norm(a+0.8*z); x34=p; y34=np.cross(d34,x34)
    views['f34']=(c+a*0.09+np.array([0,0,0.03-c[2]])+d34*0.5,np.column_stack([x34,y34,d34]),0.15)
    for nm,(loc,R,scl) in views.items():
        if np.linalg.det(R)<0: R[:,0]*=-1
        co.location=mathutils.Vector(loc.tolist()); co.rotation_euler=mathutils.Matrix(R.tolist()).to_euler(); cam.ortho_scale=scl
        sc.render.filepath=f'{od}/{tag}_{nm}_{s}.png'; bpy.ops.render.render(write_still=True)
