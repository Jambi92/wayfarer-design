# rbnpz.py (bpy) -- BLEND ORIGIN.json OUT.npz : read back an exported retopo blend into the v005 analysis frame
# (production-origin translation undone) for auditing the exact delivered geometry
import bpy, numpy as np, json, sys
a=sys.argv[sys.argv.index('--')+1:]
bpy.ops.wm.open_mainfile(filepath=a[0]); me=[o for o in bpy.data.objects if o.type=='MESH'][0].data
co=np.empty(len(me.vertices)*3,np.float32); me.vertices.foreach_get('co',co); co=co.reshape(-1,3).astype(float)
T=np.array(json.load(open(a[1]))['translation_analysis_cm'])
V=np.c_[co[:,0],-co[:,1],co[:,2]]*100-T; lv=np.empty(len(me.loops),np.int32); me.loops.foreach_get('vertex_index',lv)
fp=np.empty(len(me.polygons),np.int32); me.attributes['rac_part'].data.foreach_get('value',fp)
np.savez(a[2],V=V,Q=lv.reshape(-1,4)[:,::-1].astype(np.int64),FP=fp); print('readback',V.shape,len(fp))
