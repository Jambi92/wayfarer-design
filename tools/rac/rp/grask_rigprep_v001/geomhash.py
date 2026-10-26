# geomhash.py (bpy module, read-only) -- python3(bpy) geomhash.py -- BLEND : prints FILESHA / GEOMHASH / OBJ name V F (never saves)
import bpy, sys, hashlib, numpy as np
a = sys.argv[sys.argv.index('--') + 1:]; f = a[0]
print('FILESHA', hashlib.sha256(open(f, 'rb').read()).hexdigest())
bpy.ops.wm.open_mainfile(filepath=f)
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    m = o.data
    co = np.empty(len(m.vertices) * 3, np.float32); m.vertices.foreach_get('co', co)
    lv = np.empty(len(m.loops), np.int32); m.loops.foreach_get('vertex_index', lv)
    print('GEOMHASH', hashlib.sha256(co.tobytes() + lv.tobytes()).hexdigest())
    print('OBJ', o.name, len(m.vertices), len(m.polygons))
