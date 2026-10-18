# Freeze: copy of a UI checkpoint with the sculpt-mask attribute removed (geometry untouched). Usage: freeze.py SRC.blend SHA OUT.blend
import sys,hashlib,bpy
src,sha,out=sys.argv[-3:]; assert hashlib.sha256(open(src,'rb').read()).hexdigest()==sha
bpy.ops.wm.open_mainfile(filepath=src); o=[x for x in bpy.data.objects if x.type=='MESH'][0]; me=o.data
a=me.attributes.get('.sculpt_mask')
if a: me.attributes.remove(a)
print('objects',[(x.name,x.type) for x in bpy.data.objects],'modifiers',[m.name for m in o.modifiers])
bpy.ops.wm.save_as_mainfile(filepath=out,compress=True); print('sha',hashlib.sha256(open(out,'rb').read()).hexdigest())
