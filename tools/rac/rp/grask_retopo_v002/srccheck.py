# srccheck.py (bpy) BLEND : read-only integrity check of the frozen source (file sha256 + geometry hash as in export_v5)
import bpy, numpy as np, sys, hashlib
a=sys.argv[sys.argv.index('--')+1:]
fh=hashlib.sha256(open(a[0],'rb').read()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=a[0])
ob=[o for o in bpy.data.objects if o.type=='MESH'][0]; me=ob.data
co=np.empty(len(me.vertices)*3,np.float32); me.vertices.foreach_get('co',co)
lv=np.empty(len(me.loops),np.int32); me.loops.foreach_get('vertex_index',lv)
print('FILESHA',fh); print('GEOMHASH',hashlib.sha256(co.tobytes()+lv.tobytes()).hexdigest()); print('OBJ',ob.name,len(me.vertices),len(me.polygons))
