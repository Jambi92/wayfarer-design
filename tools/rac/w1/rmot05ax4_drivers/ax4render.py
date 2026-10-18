# AX4 read-only renders of the frozen final: whole body F/P/B/3-4, head, tail root
import sys, numpy as np, bpy, mathutils
vf,od=sys.argv[-2:]; D=np.load(vf); V,F=D['V'],D['F']
bpy.ops.wm.read_factory_settings(use_empty=True)
me=bpy.data.meshes.new('m'); me.from_pydata(V.tolist(),[],F.tolist()); me.update(); o=bpy.data.objects.new('m',me); sc=bpy.context.scene; sc.collection.objects.link(o)
for p in me.polygons: p.use_smooth=True
sc.render.engine='BLENDER_WORKBENCH'; sh=sc.display.shading; sh.light='STUDIO'; sh.color_type='SINGLE'; sh.single_color=(0.7,0.7,0.7); sc.world=bpy.data.worlds.new('w')
cam=bpy.data.cameras.new('c'); cam.type='ORTHO'; co=bpy.data.objects.new('c',cam); sc.collection.objects.link(co); sc.camera=co; cam.clip_end=20
def shot(target,yaw,pitch,scl,name,rx,ry,dist=5):
    sc.render.resolution_x=rx; sc.render.resolution_y=ry
    y=np.radians(yaw); p=np.radians(pitch); d=np.array([np.sin(y)*np.cos(p),-np.cos(y)*np.cos(p),np.sin(p)])
    co.location=mathutils.Vector((np.array(target)+d*dist).tolist()); co.rotation_euler=mathutils.Vector((-d).tolist()).to_track_quat('-Z','Y').to_euler(); cam.ortho_scale=scl
    sc.render.filepath=f'{od}/{name}.png'; bpy.ops.render.render(write_still=True)
H=V[:,2].max(); ctr=[0,V[:,1].mean(),H/2]
for yaw,n in [(0,'front'),(90,'profile'),(180,'back'),(35,'34')]: shot(ctr,yaw,0,2.35,'whole_'+n,700,1000)
hi=V[:,2]>H*0.86; hc=V[hi].mean(0)
shot(hc,0,0,0.42,'head_front',700,700); shot(hc,90,0,0.42,'head_profile',700,700); shot(hc,35,5,0.42,'head_34',700,700)
# tail root: the most posterior vertices around hip height
band=(V[:,2]>H*0.40)&(V[:,2]<H*0.55); back=V[band][np.argsort(V[band][:,1])[-200:]].mean(0)
shot(back,180,0,0.5,'tail_back',700,700); shot(back,90,0,0.5,'tail_profile',700,700); shot(back,135,10,0.5,'tail_34',700,700)
