import sys, numpy as np, bpy
bpy.ops.wm.open_mainfile(filepath=sys.argv[1]); o=[x for x in bpy.data.objects if x.type=='MESH'][0]; me=o.data
V=np.zeros(len(me.vertices)*3); me.vertices.foreach_get('co',V); V=V.reshape(-1,3); W=np.array(o.matrix_world); V=V@W[:3,:3].T+W[:3,3]
M=np.zeros(len(V)); me.attributes['.sculpt_mask'].data.foreach_get('value',M)
np.savez(sys.argv[2],V=V,M=M)
