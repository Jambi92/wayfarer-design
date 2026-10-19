# usage: cagecu.py -- SRC.npz(V cm blender, F) CAGE.npz(Vc analysis cm,Fc) OUTPREFIX cx cy cz size views...
import sys, numpy as np, bpy, mathutils
a=sys.argv[sys.argv.index('--')+1:]
src,cg,out=a[0],a[1],a[2]; c=np.array([float(x) for x in a[3:6]]); size=float(a[6]); views=a[7:]
bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene
def addmesh(nm,V,F,col,wire=False):
    me=bpy.data.meshes.new(nm); me.from_pydata(V.tolist(),[],[list(f[f>=0]) for f in F]); me.update()
    o=bpy.data.objects.new(nm,me); sc.collection.objects.link(o)
    if wire:
        m=o.modifiers.new('w','WIREFRAME'); m.thickness=0.0012; m.use_replace=True
    mat=bpy.data.materials.new(nm); mat.diffuse_color=col; me.materials.append(mat); return o
d=np.load(src); V=d['V']/100.0; F=d['F']; m=np.linalg.norm(V-c,axis=1)<size*0.9; Fm=F[m[F].all(1)]; u=np.unique(Fm)
addmesh('s',V[u],np.searchsorted(u,Fm),(0.8,0.8,0.8,1))
z=np.load(cg); Vc=(z['V'] if 'V' in z.files else z['Vc']*np.array([1,-1,1]))/100.0; Fc=z['F'] if 'F' in z.files else z['Fc']
mk=np.linalg.norm(Vc-c,axis=1)<size; Fk=Fc[np.array([mk[f[f>=0]].all() for f in Fc])]; uk=np.unique(Fk[Fk>=0]); Fk2=np.where(Fk>=0,np.searchsorted(uk,np.maximum(Fk,0)),-1)
addmesh('c',Vc[uk],Fk2,(1,0.1,0.05,1),wire=True)
sc.render.engine='BLENDER_WORKBENCH'; sh=sc.display.shading; sh.light='STUDIO'; sh.color_type='MATERIAL'; sh.show_xray=True; sh.xray_alpha=0.55
cam=bpy.data.cameras.new('c'); cam.type='ORTHO'; cam.ortho_scale=size; co=bpy.data.objects.new('c',cam); sc.collection.objects.link(co); sc.camera=co; cam.clip_end=20
sc.render.resolution_x=800; sc.render.resolution_y=800
dirs={'px':(1,0,0),'nx':(-1,0,0),'py':(0,1,0),'ny':(0,-1,0),'pz':(0,0,1),'nz':(0,0,-1)}
for v in views:
    dv=np.array(dirs[v],float); co.location=mathutils.Vector((c+dv*3).tolist())
    co.rotation_euler=mathutils.Vector((-dv).tolist()).to_track_quat('-Z','Y' if v in('pz','nz') else 'Z').to_euler()
    sc.render.filepath='%s_%s.png'%(out,v); bpy.ops.render.render(write_still=True)
