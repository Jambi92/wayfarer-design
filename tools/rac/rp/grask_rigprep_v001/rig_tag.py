# rig_tag.py (bpy module) -- python3(bpy) rig_tag.py -- RIG.blend PROPS.json : writes custom properties (landmark / weight versions, cycle outcome)
# onto the body and armature objects of a DERIVED diagnostic blend and saves that same derived file (never a frozen parent).
import bpy, sys, json
a = sys.argv[sys.argv.index('--') + 1:]; P = json.load(open(a[1]))
assert 'rigdiag' in a[0], 'only derived diagnostic blends'
bpy.ops.wm.open_mainfile(filepath=a[0])
for o in bpy.data.objects:
    if o.type in ('MESH', 'ARMATURE'):
        for k, v in P.items(): o[k] = v if isinstance(v, (str, int, float)) else json.dumps(v)
bpy.ops.wm.save_as_mainfile(filepath=a[0], compress=True, copy=False); print('TAGGED', list(P))
