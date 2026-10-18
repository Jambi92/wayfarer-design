# top-down ortho render of a foot's toes in foot frame with (v,u) grid labels. usage: toprender.py VF.npz side out.png [mask.npy]
import sys, numpy as np, bpy, mathutils
sys.path.insert(0,'/home/claude/av')
vf,side,out=sys.argv[1:4]; mask=sys.argv[4] if len(sys.argv)>4 else None
D=np.load(vf); V,F=D['V'],D['F']
from avlib import frame
fm,a,p=frame(V,side); c=V[fm].mean(0)
bpy.ops.wm.read_factory_settings(use_empty=True)
me=bpy.data.meshes.new('m'); me.from_pydata(V.tolist(),[],F.tolist()); me.update()
o=bpy.data.objects.new('m',me); sc=bpy.context.scene; sc.collection.objects.link(o)
for pl in me.polygons: pl.use_smooth=True
sc.render.engine='BLENDER_WORKBENCH'; sh=sc.display.shading; sh.light='STUDIO'
if mask:
    M=np.load(mask); ca=me.color_attributes.new('c','FLOAT_COLOR','POINT'); col=np.zeros((len(V),4)); col[:,3]=1
    col[:,0]=0.7+0.3*M; col[:,1]=0.7-0.5*M; col[:,2]=0.7-0.5*M; ca.data.foreach_set('color',col.ravel()); sh.color_type='VERTEX'
else: sh.color_type='SINGLE'; sh.single_color=(0.7,0.7,0.7)
sc.world=bpy.data.worlds.new('w')
cam=bpy.data.cameras.new('c'); cam.type='ORTHO'; co=bpy.data.objects.new('c',cam); sc.collection.objects.link(co); sc.camera=co
ctr=c+a*0.085; ctr[2]=0.3
co.location=mathutils.Vector(ctr.tolist())
R=np.column_stack([-p,a,[0,0,1]])  # camera x=perp(v), y=a(u), looking -z
co.rotation_euler=mathutils.Matrix(R.tolist()).to_euler(); cam.ortho_scale=0.17; cam.clip_end=5
sc.render.resolution_x=sc.render.resolution_y=1400; sc.render.filepath=out; bpy.ops.render.render(write_still=True)
print('MAP centre_u',(ctr-c)@a*100,'centre_v',(ctr-c)@p*100,'scale_cm',17)
