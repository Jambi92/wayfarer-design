# Close views: VIEWS="name:yaw:elev:cx:cf:cu:scale;..." on mesh NPZ (P canonical x,f,u ; f faces)
import bpy, numpy as np, math, os
z=np.load(os.environ["NPZ"]); v0=z["P"].astype(np.float64); f=z["f"]; TAG=os.environ["TAG"]; RES=int(os.environ.get("RES","1200"))
for o in list(bpy.data.objects): bpy.data.objects.remove(o,do_unlink=True)
sc=bpy.context.scene; sc.render.engine="BLENDER_WORKBENCH"; sh=sc.display.shading; sh.light="STUDIO"; sh.color_type="VERTEX"
sh.single_color=(0.66,0.66,0.68); sh.show_cavity=True; sh.cavity_type="BOTH"; sc.render.film_transparent=True
sc.render.image_settings.file_format="PNG"; sc.render.image_settings.color_mode="RGBA"
if sc.world is None: sc.world=bpy.data.worlds.new("W")
vb=np.stack([v0[:,0],-v0[:,1],v0[:,2]],1)          # blender: y = -f (front faces -y)
me=bpy.data.meshes.new("m"); me.vertices.add(len(vb)); me.vertices.foreach_set("co",vb.astype(np.float32).ravel())
me.loops.add(f.size); me.loops.foreach_set("vertex_index",f.ravel().astype(np.int32)); me.polygons.add(len(f))
me.polygons.foreach_set("loop_start",(np.arange(len(f))*3).astype(np.int32)); me.polygons.foreach_set("loop_total",np.full(len(f),3,np.int32)); me.update()
me.polygons.foreach_set("use_smooth",np.ones(len(f),bool)); R=z["R"]; COL={3:(0.33,0.70,0.42),22:(0.96,0.72,0.20),21:(0.90,0.32,0.24),1:(0.33,0.53,0.96)}
ca_=me.color_attributes.new("Col","FLOAT_COLOR","POINT"); cols=np.array([COL.get(int(r),(0.66,0.66,0.68))+(1.0,) for r in R],np.float32); ca_.data.foreach_set("color",cols.ravel()); me.color_attributes.active_color=ca_
ob=bpy.data.objects.new("m",me); sc.collection.objects.link(ob)
cd=bpy.data.cameras.new("C"); cd.type="ORTHO"; cam=bpy.data.objects.new("C",cd); sc.collection.objects.link(cam); sc.camera=cam; cd.clip_end=5000
sc.render.resolution_x=RES; sc.render.resolution_y=RES
for spec in os.environ["VIEWS"].split(";"):
    nm,yaw,el,cx,cf,cu,s=spec.split(":"); yaw,el,cx,cf,cu,s=map(float,(yaw,el,cx,cf,cu,s))
    # camera direction: yaw 0 = looking at the front (camera at -y), rotate around the body
    a=math.radians(yaw); e=math.radians(el); tgt=np.array([cx,-cf,cu])
    d=np.array([math.sin(a)*math.cos(e),-math.cos(a)*math.cos(e),math.sin(e)])   # from target to camera
    from mathutils import Vector
    cam.location=Vector(tgt+d*1500); cam.rotation_euler=(Vector(-d)).to_track_quat("-Z","Y").to_euler(); cd.ortho_scale=s
    sc.render.filepath=os.path.abspath("%s_%s.png"%(TAG,nm)); bpy.ops.render.render(write_still=True)
print("RCLOSE_DONE")
