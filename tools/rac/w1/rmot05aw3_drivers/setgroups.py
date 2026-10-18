# Write AV vertex groups into a copy of the frozen source; geometry untouched. Usage: setgroups.py SRC.blend SHA GROUPS.npz OUT.blend
import sys, hashlib, numpy as np, bpy
src,sha,gp,out=sys.argv[1:5]; assert hashlib.sha256(open(src,'rb').read()).hexdigest()==sha
bpy.ops.wm.open_mainfile(filepath=src); o=[x for x in bpy.data.objects if x.type=='MESH'][0]; me=o.data
print('objects',[(x.name,x.type) for x in bpy.data.objects]); print('matrix_world',[list(r) for r in o.matrix_world]); print('modifiers',[m.name for m in o.modifiers]); print('existing vgroups',len(o.vertex_groups))
G=np.load(gp)
for k in G.files:
    w=G[k]; assert len(w)==len(me.vertices); vg=o.vertex_groups.new(name=k); idx=np.flatnonzero(w>0)
    for i in idx: vg.add([int(i)],float(w[i]),'REPLACE')
bpy.ops.wm.save_as_mainfile(filepath=out,compress=True); print('sha',hashlib.sha256(open(out,'rb').read()).hexdigest())
