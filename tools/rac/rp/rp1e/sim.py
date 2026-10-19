"""RP1E DIAGNOSTIC simulation of the colour-ownership projection stack on a candidate cage (cloud only, nothing authored).
cage.npz: V (Blender cm), F (quads, -1 padded); colours.npy: per cage vertex colour id; targets: PREFIX_c<id>.npz (V cm, F).
Stack = [SW nearest per colour] + LEVELS x [Subsurf 1, SW project(+-, limit) per colour, SW nearest per colour].
Exports evaluated mesh after each level (analysis frame cm) -> OUT_L<k>.npz with V,F (tris),Q (quads).
Usage: blender-python sim.py -- cage.npz colours.npy TPREFIX LEVELS OUT [limit_m]"""
import sys, numpy as np, bpy
a = sys.argv[sys.argv.index('--') + 1:]
cg, colp, tp, lev, out = a[0], a[1], a[2], int(a[3]), a[4]; lim = float(a[5]) if len(a) > 5 else 0.02
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
def mk(name, V, F):
    me = bpy.data.meshes.new(name); me.from_pydata((V / 100.0).tolist(), [], [list(f[f >= 0]) for f in F]); me.update()
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); return o
z = np.load(cg); cage = mk('cage', z['V'], z['F']); col = np.load(colp)
cols = sorted(set(col.tolist())); tg = {}
for c in cols:
    t = np.load('%s_c%d.npz' % (tp, c)); tg[c] = mk('tgt%d' % c, t['V'], t['F'])
    vg = cage.vertex_groups.new(name='col%d' % c); vg.add([int(i) for i in np.where(col == c)[0]], 1.0, 'REPLACE')
import os
MODE = os.environ.get('SIMMODE', 'PN')
def sw(name, c, mode):
    m = cage.modifiers.new(name, 'SHRINKWRAP'); m.target = tg[c]; m.vertex_group = 'col%d' % c
    if mode == 'P':
        m.wrap_method = 'PROJECT'; m.use_project_z = False; m.use_negative_direction = True; m.use_positive_direction = True; m.project_limit = lim
    elif mode == 'T': m.wrap_method = 'TARGET_PROJECT'
    else: m.wrap_method = 'NEAREST_SURFACEPOINT'
if '--l0' in sys.argv:
    for c in cols: sw('n0_%d' % c, c, 'N')
bpy.context.view_layer.objects.active = cage
def export(k):
    dg = bpy.context.evaluated_depsgraph_get(); oe = cage.evaluated_get(dg); me = oe.to_mesh()
    V = np.array([v.co[:] for v in me.vertices]) * 100.0; V = np.c_[V[:, 0], -V[:, 1], V[:, 2]]
    me.calc_loop_triangles(); T = np.array([t.vertices[:] for t in me.loop_triangles])
    Q = np.full((len(me.polygons), 4), -1)
    for i, p in enumerate(me.polygons): Q[i, :len(p.vertices)] = p.vertices[:]
    np.savez_compressed('%s_L%d.npz' % (out, k), V=V, F=T, Q=Q); oe.to_mesh_clear(); print('LEVEL', k, len(V))
export(0)
BASEMODE = MODE
for k in range(1, lev + 1):
    MODE = os.environ.get('FINALMODE', BASEMODE) if k == lev else BASEMODE
    m = cage.modifiers.new('sub%d' % k, 'SUBSURF'); m.levels = 1; m.render_levels = 1
    if 'P' in MODE:
        for c in cols: sw('p%d_%d' % (k, c), c, 'P')
    if 'T' in MODE:
        for c in cols: sw('t%d_%d' % (k, c), c, 'T')
    if 'N' in MODE:
        for c in cols: sw('n%d_%d' % (k, c), c, 'N')
    for r in range(int(os.environ.get('SMR', '0')) if not (k == lev and 'FINALMODE' in os.environ) else int(os.environ.get('FSMR', '0'))):
        sm = cage.modifiers.new('sm%d_%d' % (k, r), 'SMOOTH'); sm.factor = float(os.environ.get('SMF', '0.5')); sm.iterations = int(os.environ.get('SMI', '2'))
        for c in cols: sw('r%d_%d_%d' % (k, r, c), c, 'N')
    export(k)
