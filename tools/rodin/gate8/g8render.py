# Gate 8 renderer (Cycles, CPU): per-vertex colour + material channels on the frozen Gate 7 closure mesh.
# usage: python3 g8render.py job.json
import bpy, numpy as np, math, json, sys, os, time
sys.path.insert(0,'/tmp/claude-0/rodin/g8'); import g8pheno as GP
from mathutils import Vector
J=json.load(open(sys.argv[1])); RES=J.get('res',900)
z=np.load(J['mesh']); P=z['P'].astype(np.float64); f=z['f']
Bv=np.load(J['base'])['V'].astype(np.float64) if J.get('base') else P
IDX=None
if J.get('crop'): cz=np.load(J['crop']); P=cz['P'].astype(np.float64); f=cz['f']; IDX=cz['idx']
Fd=dict(np.load(J['fields']))
for o in list(bpy.data.objects): bpy.data.objects.remove(o,do_unlink=True)
sc=bpy.context.scene; sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=J.get('samples',40); sc.cycles.use_denoising=True
sc.render.use_persistent_data=True; sc.render.film_transparent=True; sc.render.image_settings.file_format='PNG'; sc.render.image_settings.color_mode='RGBA'
sc.view_settings.view_transform='AgX'; sc.view_settings.look='None'
sc.render.resolution_x=sc.render.resolution_y=RES
vb=np.stack([P[:,0],-P[:,1],P[:,2]],1)
me=bpy.data.meshes.new("m"); me.vertices.add(len(vb)); me.vertices.foreach_set("co",vb.astype(np.float32).ravel())
me.loops.add(f.size); me.loops.foreach_set("vertex_index",f.ravel().astype(np.int32)); me.polygons.add(len(f))
me.polygons.foreach_set("loop_start",(np.arange(len(f))*3).astype(np.int32)); me.polygons.foreach_set("loop_total",np.full(len(f),3,np.int32)); me.update()
me.polygons.foreach_set("use_smooth",np.ones(len(f),bool))
cA=me.color_attributes.new("Col","FLOAT_COLOR","POINT"); mA=me.color_attributes.new("Mat","FLOAT_COLOR","POINT")
ob=bpy.data.objects.new("m",me); sc.collection.objects.link(ob)
mat=bpy.data.materials.new("Saurin"); mat.use_nodes=True; ob.data.materials.append(mat); nt=mat.node_tree; B=nt.nodes['Principled BSDF']
a1=nt.nodes.new('ShaderNodeAttribute'); a1.attribute_name='Col'; a2=nt.nodes.new('ShaderNodeAttribute'); a2.attribute_name='Mat'
sp=nt.nodes.new('ShaderNodeSeparateColor'); nt.links.new(a2.outputs['Color'],sp.inputs['Color'])
nt.links.new(a1.outputs['Color'],B.inputs['Base Color']); nt.links.new(sp.outputs[0],B.inputs['Roughness'])
nt.links.new(sp.outputs[1],B.inputs['Subsurface Weight']); nt.links.new(sp.outputs[2],B.inputs['Coat Weight'])
B.inputs['Subsurface Radius'].default_value=(0.3,0.2,0.12); B.inputs['Subsurface Scale'].default_value=0.15
B.inputs['Coat Roughness'].default_value=0.03; B.inputs['IOR'].default_value=1.45; B.inputs['Specular IOR Level'].default_value=0.45
# lighting: identical studio rig for every render (key, fill, rim, soft grey world)
if sc.world is None: sc.world=bpy.data.worlds.new("W")
sc.world.use_nodes=True; bg=sc.world.node_tree.nodes['Background']; bg.inputs[0].default_value=(0.42,0.43,0.45,1); bg.inputs[1].default_value=0.55
def sun(name,e,rx,rz,size=6):
    L=bpy.data.lights.new(name,"SUN"); L.energy=e; L.angle=math.radians(size); o=bpy.data.objects.new(name,L); sc.collection.objects.link(o); o.rotation_euler=(math.radians(rx),0,math.radians(rz))
sun("key",3.2,48,-35); sun("fill",0.9,70,120,20); sun("rim",1.8,-60,180,4)
if J.get("under_light"): sun("under",2.2,180,0,25); sun("medial",1.6,90,90,25)   # crop-only fill so contact surfaces facing down/medial are visible
cd=bpy.data.cameras.new("C"); cd.type="ORTHO"; cam=bpy.data.objects.new("C",cd); sc.collection.objects.link(cam); sc.camera=cam; cd.clip_end=5000
def setcam(spec):
    nm,yaw,el,cx,cf,cu,s=spec.split(":"); yaw,el,cx,cf,cu,s=map(float,(yaw,el,cx,cf,cu,s))
    a=math.radians(yaw); e=math.radians(el); tgt=np.array([cx,-cf,cu]); d=np.array([math.sin(a)*math.cos(e),-math.cos(a)*math.cos(e),math.sin(e)])
    cam.location=Vector(tgt+d*1500); cam.rotation_euler=(Vector(-d)).to_track_quat("-Z","Y").to_euler(); cd.ortho_scale=s; return nm
ones=np.ones((len(P),1),np.float32)  # P is the rendered mesh (crop or full)
for job in J['jobs']:
    t=time.time()
    if 'ph' in job: C,M=GP.phenotype(Fd,Bv,job['ph'],job.get('state'))
    if IDX is not None: C=C[IDX]; M=M[IDX]
    o=job.get('override',{})
    if o.get('rough') is not None: M[:,0]=o['rough']
    if o.get('coat') is not None: M[:,2]=np.maximum(M[:,2],o['coat'])
    if o.get('flat') is not None: C[:]=GP.lin(o['flat'])
    cA.data.foreach_set("color",np.concatenate([C,ones],1).ravel()); mA.data.foreach_set("color",np.concatenate([M,ones],1).ravel()); me.update()
    B.inputs['Metallic'].default_value=o.get('metallic',0.0); B.inputs['Transmission Weight'].default_value=o.get('transmission',0.0)
    B.inputs['Coat Roughness'].default_value=o.get('coat_rough',0.03)
    for spec in job['views']:
        nm=setcam(spec); sc.render.filepath=os.path.abspath('%s_%s.png'%(job['tag'],nm)); bpy.ops.render.render(write_still=True)
    print('JOB',job['tag'],'%.1fs'%(time.time()-t),flush=True)
print('G8_DONE')
