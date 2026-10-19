# blender-python brender.py -- mesh.npz|src box out.png camloc(x,y,z) target(x,y,z) [flipy]
import bpy, numpy as np, sys, mathutils
a=sys.argv[sys.argv.index('--')+1:]
mp,box,outp,cl,tg=a[:5]; flip=len(a)>5
if mp=='src':
    w=np.load('/home/claude/stc/rp1/weld.npz'); V=w['V'].astype(float); F=w['F']
else:
    z=np.load(mp); V=z['V'].astype(float).copy(); F=z['Q'] if 'Q' in z.files else z['F']
    if flip: V[:,1]*=-1
b=np.array([float(t) for t in box.split(',')]).reshape(3,2)
F=np.asarray(F); FF=[f[f>=0] for f in F]
C=np.array([V[f].mean(0) for f in FF]); m=((C>b[:,0])&(C<b[:,1])).all(1)
FF=[FF[i] for i in np.where(m)[0]]; used=np.unique(np.concatenate(FF)); rm={o:n for n,o in enumerate(used)}
bpy.ops.wm.read_factory_settings(use_empty=True)
me=bpy.data.meshes.new('m'); me.from_pydata(V[used].tolist(),[],[[rm[i] for i in f] for f in FF]); me.update()
ob=bpy.data.objects.new('m',me); sc=bpy.context.scene; sc.collection.objects.link(ob)
cam=bpy.data.cameras.new('c'); co=bpy.data.objects.new('c',cam); sc.collection.objects.link(co); sc.camera=co
co.location=[float(t) for t in cl.split(',')]; d=mathutils.Vector([float(t) for t in tg.split(',')])-co.location
co.rotation_euler=d.to_track_quat('-Z','Y').to_euler(); cam.lens=50
sc.render.engine='BLENDER_WORKBENCH'; sc.display.shading.light='STUDIO'; sc.display.shading.color_type='SINGLE'
sc.display.shading.show_cavity=True
sc.render.resolution_x=900; sc.render.resolution_y=700; sc.render.filepath=outp
bpy.ops.render.render(write_still=True)
