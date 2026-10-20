"""RP1E DIAGNOSTIC simulation of the colour-ownership projection stack on a candidate cage (cloud only, nothing authored).
cage.npz: V (Blender cm), F (quads, -1 padded); colours.npy: per cage vertex colour id; targets: PREFIX_c<id>.npz (V cm, F).
Stack = [SW nearest per colour] + LEVELS x [Subsurf 1, SW project(+-, limit) per colour, SW nearest per colour].
Exports evaluated mesh after each level (analysis frame cm) -> OUT_L<k>.npz with V,F (tris),Q (quads).
Usage: blender-python sim.py -- cage.npz colours.npy TPREFIX LEVELS OUT [limit_m]"""
import sys, os, numpy as np, bpy
a = sys.argv[sys.argv.index('--') + 1:]
cg, colp, tp, lev, out = a[0], a[1], a[2], int(a[3]), a[4]; lim = float(a[5]) if len(a) > 5 else 0.02
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
def mk(name, V, F):
    me = bpy.data.meshes.new(name); me.from_pydata((V / 100.0).tolist(), [], [list(f[f >= 0]) for f in F]); me.update()
    o = bpy.data.objects.new(name, me); sc.collection.objects.link(o); return o
z = np.load(cg); cage = mk('cage', z['V'], z['F']); col = np.load(colp)
if os.environ.get('CREASE'):
    import json as _j
    CR = _j.load(open(os.environ['CREASE']))   # {"edges":[[a,b],...],"w":1.0}
    me_ = cage.data; at = me_.attributes.get('crease_edge') or me_.attributes.new('crease_edge', 'FLOAT', 'EDGE')
    key = {tuple(sorted(e.vertices[:])): e.index for e in me_.edges}; nset = 0
    for a_, b_ in CR['edges']:
        k_ = key.get(tuple(sorted((a_, b_))))
        if k_ is not None: at.data[k_].value = CR.get('w', 1.0); nset += 1
    print('CREASE edges set', nset)
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
REGCOLS = [int(x) for x in os.environ.get('REGCOLS', '').split(',') if x]
REGV = [int(t) for t in open(os.environ['REGV']).read().split()] if os.environ.get('REGV') else []
if REGV:
    gnr = cage.vertex_groups.new(name='noreg'); gnr.add([i for i in range(len(z['V'])) if i not in set(REGV)], 1.0, 'REPLACE')
for k in range(1, lev + 1):
    MODE = os.environ.get('FINALMODE', BASEMODE) if k == lev else BASEMODE
    m = cage.modifiers.new('sub%d' % k, 'SUBSURF'); m.levels = 1; m.render_levels = 1
    if os.environ.get('SUBLIM') == '0': m.use_limit_surface = False
    NOP = [int(x) for x in os.environ.get('FINALN', '').split(',') if x] if k == lev else []
    if 'P' in MODE:
        for c in cols:
            if c not in NOP and c not in REGCOLS: sw('p%d_%d' % (k, c), c, 'P')
    if 'T' in MODE:
        for c in cols: sw('t%d_%d' % (k, c), c, 'T')
    if 'N' in MODE:
        for c in cols: sw('n%d_%d' % (k, c), c, 'N')
    nsm = int(os.environ.get('SMR', '0')) if not (k == lev and 'FINALMODE' in os.environ) else int(os.environ.get('FSMR', '0'))
    for r in range(nsm):
        sm = cage.modifiers.new('sm%d_%d' % (k, r), 'SMOOTH'); sm.factor = float(os.environ.get('SMF', '0.5')); sm.iterations = int(os.environ.get('SMI', '2'))
        if REGV: sm.vertex_group = 'noreg'
        for c in cols: sw('r%d_%d_%d' % (k, r, c), c, 'N')
    if k == lev and os.environ.get('FINALPOST'):
        # extra post steps at the final level, e.g. 'PN' = short Project then Nearest, limit FPLIM (m)
        lim0 = lim; lim = float(os.environ.get('FPLIM', '0.003'))
        for step in os.environ['FINALPOST']:
            for c in cols:
                if step == 'P' and c in [int(x) for x in os.environ.get('FPSKIP', '').split(',') if x]: continue
                sw('post%s_%d' % (step, c), c, step)
        lim = lim0
    if k == lev and os.environ.get('FINALN') and nsm == 0:
        # colours listed in FINALN get Smooth+Nearest x2 at the final level (feet), others just the P/N above
        for r in range(int(os.environ.get('FNSMR', '2'))):
            sm = cage.modifiers.new('fsm%d' % r, 'SMOOTH'); sm.factor = 0.5; sm.iterations = 2
            g = cage.vertex_groups.new(name='fsm%d' % r); g.add([int(i) for i in np.where(np.isin(col, NOP))[0]], 1.0, 'REPLACE'); sm.vertex_group = g.name
            for c in NOP: sw('fr%d_%d' % (r, c), c, 'N')
    if k == lev and os.environ.get('FINALSM'):
        # last step: plain Smooth (no re-projection), optional colour list FSMCOL
        fc = [int(x) for x in os.environ.get('FSMCOL', '').split(',') if x]
        sm = cage.modifiers.new('finalsm', 'SMOOTH'); sm.factor = float(os.environ.get('FSMF', '0.5')); sm.iterations = int(os.environ['FINALSM'])
        if fc:
            g = cage.vertex_groups.new(name='finalsm'); g.add([int(i) for i in np.where(np.isin(col, fc))[0]], 1.0, 'REPLACE'); sm.vertex_group = g.name
        if os.environ.get('FSMV'):
            ids = [int(t) for t in open(os.environ['FSMV']).read().split()]
            if REGV: ids = [i for i in ids if i not in set(REGV)]
            g = cage.vertex_groups.new(name='finalsmv'); g.add(ids, 1.0, 'REPLACE'); sm.vertex_group = g.name
    export(k)
