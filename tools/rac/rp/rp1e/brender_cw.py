# blender-python brender_cw.py -- cage.npz box out.png cam target [lens] : source (grey) + cage edges (red tubes) in a box
import bpy, numpy as np, sys, mathutils, bmesh
a=sys.argv[sys.argv.index('--')+1:]
cp,box,outp,cl,tg=a[:5]; lens=float(a[5]) if len(a)>5 else 50
b=np.array([float(t) for t in box.split(',')]).reshape(3,2)
bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F']
C=S[SF].mean(1); m=((C>b[:,0]-1)&(C<b[:,1]+1)).all(1); FS=SF[m]; u=np.unique(FS); rm=-np.ones(len(S),int); rm[u]=np.arange(len(u))
me=bpy.data.meshes.new('s'); me.from_pydata(S[u].tolist(),[],rm[FS].tolist()); me.update()
g=bpy.data.materials.new('g'); g.diffuse_color=(0.75,0.75,0.75,1); me.materials.append(g)
o=bpy.data.objects.new('s',me); sc.collection.objects.link(o)
z=np.load(cp); V=z['V']; F=z['F']; E=set()
for f in F:
    f=f[f>=0]
    for i in range(len(f)): E.add(tuple(sorted((int(f[i]),int(f[(i+1)%len(f)])))))
r=bpy.data.materials.new('r'); r.diffuse_color=(1,0.1,0.1,1)
cu=bpy.data.curves.new('c','CURVE'); cu.dimensions='3D'; cu.bevel_depth=0.04
for i,j in E:
    p,q=V[i],V[j]
    if ((p>b[:,0])&(p<b[:,1])).all() or ((q>b[:,0])&(q<b[:,1])).all():
        s=cu.splines.new('POLY'); s.points.add(1); s.points[0].co=(*p,1); s.points[1].co=(*q,1)
cu.materials.append(r); co_=bpy.data.objects.new('c',cu); sc.collection.objects.link(co_)
cam=bpy.data.cameras.new('cam'); co=bpy.data.objects.new('cam',cam); sc.collection.objects.link(co); sc.camera=co
co.location=[float(t) for t in cl.split(',')]; d=mathutils.Vector([float(t) for t in tg.split(',')])-co.location
co.rotation_euler=d.to_track_quat('-Z','Y').to_euler(); cam.lens=lens
sc.render.engine='BLENDER_WORKBENCH'; sc.display.shading.light='STUDIO'; sc.display.shading.color_type='MATERIAL'
sc.render.resolution_x=900; sc.render.resolution_y=700; sc.render.filepath=outp
bpy.ops.render.render(write_still=True)
