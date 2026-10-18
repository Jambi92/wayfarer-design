import bpy,sys,hashlib
bpy.ops.wm.open_mainfile(filepath=sys.argv[1]); bpy.ops.export_scene.gltf(filepath=sys.argv[2], export_format='GLB')
print('glb sha',hashlib.sha256(open(sys.argv[2],'rb').read()).hexdigest())
