# handview.py (bpy) -- MESH(.npz|.blend) SIDE(l|r) OUTDIR TAG VIEWSPEC [WIRE 0|1] [T=tx,tf,tu]
# Isolated-hand orthographic renders in the v005 analysis frame (cm; x subject-left, f forward, u up).
# .blend input = the exported production file: positions are read back and the production-origin translation T is undone.
# VIEWSPEC: name:dx,df,du:cx,cf,cu:halfsize ; several separated by ';'. Writes OUTDIR/TAG_name.png and TAG_name.json (camera basis).
import bpy, sys, numpy as np, json, mathutils, math
a=sys.argv[sys.argv.index('--')+1:]
src,side,O,TAG,VS=a[0],a[1],a[2],a[3],a[4]; WIRE=len(a)>5 and a[5]=='1'; T=np.array([float(v) for v in a[6].split(',')]) if len(a)>6 else np.zeros(3)
sys.path.insert(0,'/tmp/claude-0/rt'); from common import PARTS
import os
PFX=('foot','hallux','toe') if os.environ.get('REGION','hand')=='foot' else ('hand','thumb','index','middle','ring','pinky')
HP=[i for i,p in enumerate(PARTS) if p.endswith('_'+side) and p.startswith(PFX)]
if src.endswith('.blend'):
    bpy.ops.wm.open_mainfile(filepath=src); ob=[o for o in bpy.data.objects if o.type=='MESH'][0]; me=ob.data
    co=np.empty(len(me.vertices)*3,np.float32); me.vertices.foreach_get('co',co); co=co.reshape(-1,3).astype(float)
    V=np.c_[co[:,0],-co[:,1],co[:,2]]*100-T
    lv=np.empty(len(me.loops),np.int32); me.loops.foreach_get('vertex_index',lv); Q=lv.reshape(-1,4)[:,::-1]
    fp=np.empty(len(me.polygons),np.int32); me.attributes['rac_part'].data.foreach_get('value',fp)
    keep=np.isin(fp,HP); F=Q[keep]
else:
    z=np.load(src); V=z['V'].astype(float); F=z['Q']
    lab=z['FP'] if 'FP' in z.files else np.load('/tmp/claude-0/rt/flab.npy'); F=F[np.isin(lab,HP)]
ZM=float(os.environ.get('ZMAX','1e9'))
if ZM<1e8: F=F[(V[F][:,:,2]<ZM).all(1)]
bpy.ops.wm.read_factory_settings(use_empty=True)
P=np.c_[V[:,0],-V[:,1],V[:,2]]/100
me=bpy.data.meshes.new('h'); me.from_pydata(P.tolist(),[],F.tolist()); me.update()
ob=bpy.data.objects.new('h',me); bpy.context.scene.collection.objects.link(ob)
for p in me.polygons: p.use_smooth=True
sc=bpy.context.scene; sc.render.engine='BLENDER_WORKBENCH'; sh=sc.display.shading; sh.light='STUDIO'; sh.show_specular_highlight=False
sh.color_type='MATERIAL'
m1=bpy.data.materials.new('clay'); m1.diffuse_color=(0.78,0.75,0.71,1); ob.data.materials.append(m1)
if WIRE:
    w=ob.copy(); w.data=ob.data.copy(); sc.collection.objects.link(w)
    md=w.modifiers.new('wf','WIREFRAME'); md.thickness=0.00018; md.use_replace=True; md.use_even_offset=False
    m2=bpy.data.materials.new('wire'); m2.diffuse_color=(0.08,0.09,0.14,1); w.data.materials.clear(); w.data.materials.append(m2)
sc.world=bpy.data.worlds.new('w'); sc.world.color=(1,1,1)
cam=bpy.data.cameras.new('c'); cam.type='ORTHO'; co_=bpy.data.objects.new('c',cam); sc.collection.objects.link(co_); sc.camera=co_
sc.render.resolution_x=sc.render.resolution_y=900; sc.render.film_transparent=False
for spec in VS.split(';'):
    nm,d,c,h=spec.split(':'); d=np.array([float(v) for v in d.split(',')]); d/=np.linalg.norm(d); c=np.array([float(v) for v in c.split(',')]); h=float(h)
    up=np.array([0,0,1.0]) if abs(d[2])<0.9 else np.array([0,1.0,0])
    y=up-(up@d)*d; y/=np.linalg.norm(y); x=np.cross(y,d)
    B=lambda v: np.array([v[0],-v[1],v[2]])          # analysis direction -> blender
    M=mathutils.Matrix([list(B(x)),list(B(y)),list(B(d))]).transposed()
    # blender reflection flips handedness: recompute x in blender space so the camera matrix is a rotation
    xb=np.cross(B(y),B(d)); M=mathutils.Matrix([list(xb),list(B(y)),list(B(d))]).transposed()
    co_.matrix_world=mathutils.Matrix.Translation(mathutils.Vector(B(c+d*80)/100))@M.to_4x4()
    cam.ortho_scale=2*h/100; cam.clip_end=5
    sc.render.filepath='%s/%s_%s.png'%(O,TAG,nm); bpy.ops.render.render(write_still=True)
    # image basis in analysis frame: u axis = blender xb mapped back
    xa=np.array([xb[0],-xb[1],xb[2]])
    json.dump(dict(c=c.tolist(),x=xa.tolist(),y=y.tolist(),h=h,px=900),open('%s/%s_%s.json'%(O,TAG,nm),'w'))
