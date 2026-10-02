# Render a mesh (canonical frame x,f,u; +f forward) at 5 views, optional per-vertex category colours; emit label pixel coords.
import bpy, numpy as np, math, json, os, sys
NPZ=os.environ["NPZ"]; TAG=os.environ["TAG"]; COLOR=os.environ.get("COLOR","1")=="1"; RES=int(os.environ.get("RES","1400"))
z=np.load(NPZ); v0=z["P"].astype(np.float64); f=z["f"]; R=z["R"] if "R" in z.files else np.zeros(len(v0),int)
CAT={1:"REPLACE",2:"MODIFY",3:"PRESERVE",4:"PRESERVE",5:"PRESERVE",6:"MODIFY",7:"MODIFY",8:"PRESERVE",9:"MODIFY",10:"REBUILD",11:"REBUILD",12:"MODIFY",14:"PRESERVE",15:"MODIFY",16:"REBUILD",0:"NONE",20:"PRESERVE",21:"REBUILD",22:"MODIFY"}
COL={"PRESERVE":(0.33,0.70,0.42),"MODIFY":(0.96,0.72,0.20),"REBUILD":(0.90,0.32,0.24),"REPLACE":(0.33,0.53,0.96),"NONE":(0.66,0.66,0.68)}
for o in list(bpy.data.objects): bpy.data.objects.remove(o,do_unlink=True)
sc=bpy.context.scene; sc.render.engine="BLENDER_WORKBENCH"; sh=sc.display.shading; sh.light="STUDIO"
sh.color_type="VERTEX" if COLOR else "SINGLE"; sh.single_color=(0.66,0.66,0.68); sh.show_cavity=True; sh.cavity_type="BOTH"
sc.render.film_transparent=True; sc.render.image_settings.file_format="PNG"; sc.render.image_settings.color_mode="RGBA"
if sc.world is None: sc.world=bpy.data.worlds.new("W")
cd=bpy.data.cameras.new("C"); cd.type="ORTHO"; cam=bpy.data.objects.new("C",cd); sc.collection.objects.link(cam); sc.camera=cam; cd.clip_end=100
H=np.ptp(v0[:,2]); out={}
cent={int(k):v0[R==k].mean(0) for k in np.unique(R)}
for yaw,nm in ((0,"front"),(90,"profile"),(180,"rear"),(45,"front34"),(150,"rear34")):
    a=math.radians(yaw); ca,sa=math.cos(a),math.sin(a)
    def rot(p):  # rotate body about vertical so camera (looking along +y from -y) sees the requested side
        x,fw,u=p[...,0],p[...,1],p[...,2]; xr=x*ca+fw*sa; fr=-x*sa+fw*ca; return np.stack([xr,-fr,u],-1)
    vb=rot(v0)
    me=bpy.data.meshes.new(nm); me.vertices.add(len(vb)); me.vertices.foreach_set("co",vb.astype(np.float32).ravel())
    me.loops.add(f.size); me.loops.foreach_set("vertex_index",f.ravel().astype(np.int32))
    me.polygons.add(len(f)); me.polygons.foreach_set("loop_start",(np.arange(len(f))*3).astype(np.int32)); me.polygons.foreach_set("loop_total",np.full(len(f),3,np.int32)); me.update()
    me.polygons.foreach_set("use_smooth",np.ones(len(f),bool))
    if COLOR:
        ca_=me.color_attributes.new("Col","FLOAT_COLOR","POINT"); cols=np.array([COL[CAT[int(r)]]+(1.0,) for r in R],np.float32); ca_.data.foreach_set("color",cols.ravel())
        me.color_attributes.active_color=ca_
    ob=bpy.data.objects.new(nm,me); sc.collection.objects.link(ob)
    lo,hi=vb.min(0),vb.max(0); s=max(hi[0]-lo[0],hi[2]-lo[2])*1.06; cx,cz=(lo[0]+hi[0])/2,(lo[2]+hi[2])/2
    cd.ortho_scale=s; cam.location=(cx,lo[1]-10*H,cz); cam.rotation_euler=(math.radians(90),0,0)
    sc.render.resolution_x=RES; sc.render.resolution_y=RES
    sc.render.filepath=os.path.abspath("%s_%s.png"%(TAG,nm)); bpy.ops.render.render(write_still=True)
    lab={}
    for k,p in cent.items():
        q=rot(p); lab[k]=[((q[0]-cx)/s+0.5)*RES,((cz-q[2])/s+0.5)*RES,float(-q[1])]
    out[nm]=lab; bpy.data.objects.remove(ob,do_unlink=True)
json.dump(out,open(TAG+"_labels.json","w"))
print("RMAP_DONE")
