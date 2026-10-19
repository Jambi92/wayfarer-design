# blender-python brender_sx.py -- sim.npz box out.png cam target : L4 mesh (flip y) with self-x faces in red
import bpy, numpy as np, sys, mathutils
a=sys.argv[sys.argv.index('--')+1:]
mp,box,outp,cl,tg=a[:5]
z=np.load(mp); V=z['V'].astype(float).copy(); V[:,1]*=-1; F=z['Q']
P=np.load(mp.replace('.npz','_pairs.npy')); bad=set(P.ravel().tolist())
b=np.array([float(t) for t in box.split(',')]).reshape(3,2)
FF=[f[f>=0] for f in F]; C=np.array([V[f].mean(0) for f in FF]); m=np.where(((C>b[:,0])&(C<b[:,1])).all(1))[0]
FS=[FF[i] for i in m]; used=np.unique(np.concatenate(FS)); rm={o:n for n,o in enumerate(used)}
bpy.ops.wm.read_factory_settings(use_empty=True)
me=bpy.data.meshes.new('m'); me.from_pydata(V[used].tolist(),[],[[rm[i] for i in f] for f in FS]); me.update()
g=bpy.data.materials.new('g'); g.diffuse_color=(0.7,0.7,0.7,1); r=bpy.data.materials.new('r'); r.diffuse_color=(1,0,0,1)
me.materials.append(g); me.materials.append(r)
for k,i in enumerate(m):
    if int(i) in bad: me.polygons[k].material_index=1
ob=bpy.data.objects.new('m',me); sc=bpy.context.scene; sc.collection.objects.link(ob)
cam=bpy.data.cameras.new('c'); co=bpy.data.objects.new('c',cam); sc.collection.objects.link(co); sc.camera=co
co.location=[float(t) for t in cl.split(',')]; d=mathutils.Vector([float(t) for t in tg.split(',')])-co.location
co.rotation_euler=d.to_track_quat('-Z','Y').to_euler(); cam.lens=float(a[5]) if len(a)>5 else 50
sc.render.engine='BLENDER_WORKBENCH'; sc.display.shading.light='STUDIO'; sc.display.shading.color_type='MATERIAL'
sc.display.shading.show_backface_culling=False
sc.render.resolution_x=900; sc.render.resolution_y=700; sc.render.filepath=outp
bpy.ops.render.render(write_still=True)
