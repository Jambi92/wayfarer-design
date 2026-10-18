# Write a vertex-ID mask into .sculpt_mask of a copy of the source blend; geometry untouched. Usage: setmask.py SRC.blend SHA MASK.npy OUT.blend
import sys, hashlib, numpy as np, bpy
src,sha,mp,out=sys.argv[1:5]; assert hashlib.sha256(open(src,'rb').read()).hexdigest()==sha
bpy.ops.wm.open_mainfile(filepath=src); o=[x for x in bpy.data.objects if x.type=='MESH'][0]; me=o.data; M=np.load(mp).astype(np.float32)
assert len(M)==len(me.vertices)
a=me.attributes.get('.sculpt_mask') or me.attributes.new('.sculpt_mask','FLOAT','POINT'); a.data.foreach_set('value',M); me.update()
me.calc_loop_triangles(); T=np.empty(len(me.loop_triangles)*3,np.int64); me.loop_triangles.foreach_get('vertices',T); np.save(out.replace('.blend','_F.npy'),T.reshape(-1,3))
bpy.ops.wm.save_as_mainfile(filepath=out,compress=True); print('sha',hashlib.sha256(open(out,'rb').read()).hexdigest())
