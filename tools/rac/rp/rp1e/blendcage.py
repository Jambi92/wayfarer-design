"""Extract mesh 'Cylinder' from a .blend to npz (cm, Blender frame) + topology report.
Usage: blender-python blendcage.py -- file.blend OUT.npz"""
import sys, bpy, numpy as np, collections
a = sys.argv[sys.argv.index('--') + 1:]
bpy.ops.wm.open_mainfile(filepath=a[0])
o = bpy.data.objects['Cylinder']; me = o.data
print('matrix identity', np.allclose(np.array(o.matrix_world), np.eye(4)))
V = np.array([v.co[:] for v in me.vertices]) * 100
F = [list(p.vertices) for p in me.polygons]
Fo = np.full((len(F), max(len(f) for f in F)), -1)
for i, f in enumerate(F): Fo[i, :len(f)] = f
np.savez_compressed(a[1], V=V, F=Fo)
E = collections.Counter()
for f in F:
    for j in range(len(f)): E[tuple(sorted((f[j], f[(j + 1) % len(f)])))] += 1
nb = sum(1 for c in E.values() if c == 1); nm = sum(1 for c in E.values() if c > 2)
used = set(x for f in F for x in f); loose = len(V) - len(used)
# components
par = list(range(len(V)))
def fd(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
for e in E: par[fd(e[0])] = fd(e[1])
comps = len(set(fd(x) for x in used))
chi = len(used) - len(E) + len(F)
print('V', len(V), 'F', len(F), 'E', len(E), 'boundary', nb, 'nonmanifold', nm, 'loose', loose, 'comps', comps, 'chi', chi, 'genus', (2 - chi) / 2)
nf = collections.Counter(len(f) for f in F); print('face sizes', dict(nf))
# duplicate faces (same vertex set)
S = collections.Counter(frozenset(f) for f in F); print('dup faces', sum(c - 1 for c in S.values() if c > 1))
