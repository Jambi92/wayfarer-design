import sys, json, numpy as np, bpy, mathutils
vf,tag,od=sys.argv[1:4]
D=np.load(vf); V,F=D['V'],D['F']; FR=json.load(open('/home/claude/aw1/footframes.json'))
bpy.ops.wm.read_factory_settings(use_empty=True)
me=bpy.data.meshes.new('m'); me.from_pydata(V.tolist(),[],F.tolist()); me.update()
o=bpy.data.objects.new('m',me); sc=bpy.context.scene; sc.collection.objects.link(o)
for pl in me.polygons: pl.use_smooth=True
sc.render.engine='BLENDER_WORKBENCH'; sh=sc.display.shading; sh.light='STUDIO'; sh.color_type='SINGLE'; sh.single_color=(0.7,0.7,0.7)
sc.world=bpy.data.worlds.new('w')
cam=bpy.data.cameras.new('c'); cam.type='ORTHO'; co=bpy.data.objects.new('c',cam); sc.collection.objects.link(co); sc.camera=co; cam.clip_end=10
def shot(loc,R,scl,name,rx,ry):
    sc.render.resolution_x=rx; sc.render.resolution_y=ry
    if np.linalg.det(R)<0: R[:,0]*=-1
    co.location=mathutils.Vector(loc.tolist()); co.rotation_euler=mathutils.Matrix(R.tolist()).to_euler(); cam.ortho_scale=scl
    sc.render.filepath=f'{od}/{tag}_{name}.png'; bpy.ops.render.render(write_still=True)
z=np.array([0,0,1.0])
for s in 'LR':
    c=np.array(FR[s]['c']); a=np.array(FR[s]['a']); p=np.array(FR[s]['p'])
    m=(np.linalg.norm((V-c)[:,:2],axis=1)<0.2)&(V[:,2]<0.1); tip=(V[m]@a).max(); c=c+a*(tip-c@a-0.025)
    for side,sg in (('lat',1),('med',-1)):
        d=sg*p*(1 if s=='L' else -1); x=np.cross(z,d); shot(c+np.array([0,0,0.03-c[2]])+d*0.5,np.column_stack([x,z,d]),0.12,f'prof{side}_{s}',1400,700)
# whole body front / side
ctr=np.array([0,V[:,1].mean(),np.ptp(V[:,2])/2]); 
shot(ctr+np.array([0,-3,0]),np.column_stack([[1,0,0],[0,0,1],[0,-1,0]]),2.3,'whole_front',900,1100)
shot(ctr+np.array([3,0,0]),np.column_stack([[0,1,0],[0,0,1],[1,0,0]]),2.3,'whole_side',900,1100)
shot(np.array([0,V[:,1].mean(),0.12])+np.array([0,-3,0]),np.column_stack([[1,0,0],[0,0,1],[0,-1,0]]),0.9,'feet_front',1400,700)
