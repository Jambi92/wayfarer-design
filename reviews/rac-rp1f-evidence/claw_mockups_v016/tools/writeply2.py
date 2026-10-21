# writeply2.py PROD.npz OUTPREFIX : final production mesh (analysis frame cm) -> two binary PLY halves in Blender metres, Z-up,
# outward winding; faces split by index, seam vertices duplicated bit-exactly (rejoined in the UI with Merge by Distance 1e-6 m).
import sys, numpy as np, struct, hashlib, json
z = np.load(sys.argv[1]); V = z['V'].astype(float) * np.array([1, -1, 1]) / 100.0; Q = z['Q'].astype(np.int64)
F = z['F'].astype(np.int64); vol = np.einsum('ij,ij->i', V[F[:, 0]], np.cross(V[F[:, 1]], V[F[:, 2]])).sum() / 6
if vol < 0: Q = Q[:, ::-1].copy()
print('blender-frame volume m3 (before fix) %.5f' % vol)
V32 = V.astype('<f4'); out = {}
h = len(Q) // 2
for k, qs in enumerate((Q[:h], Q[h:])):
    used = np.unique(qs); rm = -np.ones(len(V), np.int64); rm[used] = np.arange(len(used)); qq = rm[qs].astype('<i4')
    fn = '%s_part%d.ply' % (sys.argv[2], k + 1)
    with open(fn, 'wb') as f:
        f.write(('ply\nformat binary_little_endian 1.0\ncomment RP1E v014 production part %d (global vertex ids in order of first use)\nelement vertex %d\nproperty float x\nproperty float y\nproperty float z\nelement face %d\nproperty list uchar int vertex_indices\nend_header\n' % (k + 1, len(used), len(qq))).encode())
        f.write(V32[used].tobytes())
        rec = np.zeros(len(qq), dtype=[('n', 'u1'), ('i', '<i4', 4)]); rec['n'] = 4; rec['i'] = qq; f.write(rec.tobytes())
    out[fn] = dict(vertices=int(len(used)), faces=int(len(qq)), sha256=hashlib.sha256(open(fn, 'rb').read()).hexdigest())
json.dump(out, open(sys.argv[2] + '_ply.json', 'w'), indent=1); print(out)
