# RAC RM-OT-05I protection overlay, Blender side (run inside Blender on a g_setup scene / working sculpt; coordinates are never touched).
# Adds vertex group NO_TOUCH_hands_digits_guard05i (from regions_05i.json), adds it to NO_TOUCH_all and re-installs the sculpt mask
# (1 = protected) exactly as g_setup.remask() does. Idempotent.
#   GUI:  set OVERLAY below (or define OVERLAY in the console) and run;   CLI: blender -b work.blend --python i_blender_overlay.py -- --overlay regions_05i.json [--save]
import bpy, json, sys
OVERLAY = globals().get('OVERLAY')
KEY = 'NO_TOUCH_hands_digits_guard05i'
def apply(path):
    R = json.load(open(path)); ix = R['regions'][KEY]
    base = bpy.data.objects['GO_SCULPT_BASE']; me = base.data
    if base.mode != 'OBJECT': bpy.ops.object.mode_set(mode='OBJECT')
    g = base.vertex_groups.get(KEY) or base.vertex_groups.new(name=KEY); g.add(ix, 1.0, 'REPLACE')
    na = base.vertex_groups['NO_TOUCH_all']; na.add(ix, 1.0, 'REPLACE')
    gi = na.index
    mask = [1.0 if any(gg.group == gi and gg.weight > 0.5 for gg in v.groups) else 0.0 for v in me.vertices]
    ma = me.attributes.get('.sculpt_mask') or me.attributes.new('.sculpt_mask', 'FLOAT', 'POINT'); ma.data.foreach_set('value', mask); me.update()
    me['rac_protection_overlay_05i'] = R['overlay_05i']['source_rule']
    return {'group': KEY, 'added_group_vertices': len(ix), 'NO_TOUCH_all_vertices': sum(1 for v in me.vertices if any(gg.group == gi and gg.weight > 0.5 for gg in v.groups)), 'masked_vertices': int(sum(mask))}
if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    p = a[a.index('--overlay') + 1] if '--overlay' in a else OVERLAY
    print('RAC_OVERLAY_05I', json.dumps(apply(p)))
    if '--save' in a: bpy.ops.wm.save_mainfile()
